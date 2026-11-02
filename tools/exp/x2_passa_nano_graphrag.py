"""X2 pass A, nano-graphrag: INDEXING the 20 frozen documents through the metering gateway, at an upstream chosen by argument.

The stub rehearsal (`x2_nano_graphrag.py`) counted what the builder sends. This runner points the same builder at the
metering gateway (`tools/metering_gateway.py`, started here through `passa_common.LocalGateway`) and the gateway at an
upstream of your choice: the stub now (free, to check the plumbing), a local Ollama later. Nothing in the runner changes
between the two. Every call is then recorded by the gateway with the provider's own usage (`input_tokens`,
`output_tokens`), status and latency; the runner adds the calls by kind (the same classification of a request by the
builder's prompt templates as the stub runner) and the builder's own graph sizes, at each checkpoint.

    python tools/exp/x2_passa_nano_graphrag.py --corpus CORPUS_JSON --documents DOCUMENTS_TSV --repo-root REPO \\
        --upstream-url http://127.0.0.1:PORT/v1 --model CHAT_MODEL --embed-model EMBED_MODEL \\
        --workdir NEW_EMPTY_DIR --out RESULT_JSON [--checkpoints 1,5,20] [--tiktoken-cache DIR]

Free check of the plumbing (no model, no key): add `--stub-shape B` instead of `--upstream-url`. The runner then hosts
the stub model server of `stub_llm.py` itself, with the SAME responder (shape A or B) as `x2_nano_graphrag.py`, and
compares, at every checkpoint, the counts the gateway logged with the counts the stub saw directly. A difference is
recorded under `gateway_vs_stub` and makes the exit status 1. `--stub-dims N` makes the stub answer embeddings with
N-long vectors (default 1536), to show that the dimension is read, not assumed.

The environment must be stripped by the caller, as for the stub runner (the runner also refuses to start when a variable
whose name looks like a credential is present, and sets a dead HTTP proxy with loopback excluded itself):

    env -i PATH=/usr/bin:/bin:/opt/homebrew/bin HOME=$SCRATCH/home \\
      $SCRATCH/venv/bin/python tools/exp/x2_passa_nano_graphrag.py ...

What it does, in order
  1. Reads the 20 documents (the corpus file is checked against its pinned SHA-256).
  2. If the upstream answers `GET /api/version` (an Ollama server), runs `passa_common.preflight` on it and refuses to
     start unless the chat model has an explicit `num_ctx` of at least `--min-ctx`. Against any other upstream (the stub)
     the check is recorded as skipped. `--preflight require` makes a non-Ollama upstream an error; `skip` omits it.
  3. Starts the gateway (`workdir/gateway`) with exactly two model names, `--model` and `--embed-model`; the gateway
     refuses any other name, and the builder is configured to send exactly those two (nano-graphrag hard-codes gpt-4o,
     gpt-4o-mini and text-embedding-3-small by default; here the builder's own `openai_complete_if_cache` is called with
     `--model` for both of its model slots, and an embedding function with the builder's own retry policy sends
     `--embed-model`).
  4. Makes one embeddings call through the gateway to read the vector length, and configures the builder with it. That
     call is logged by the gateway like any other; it is left out of every count below and recorded under
     `dimension_probe`.
  5. Indexes the documents one at a time into one working directory (`workdir/rag`), as the stub runner's `perdoc`
     scenario does, up to the largest checkpoint; at each checkpoint it records the gateway's log (see below).
  6. Writes `--out` after every document (`status` "running"), and finally with `status` "complete" or "failed". It also
     writes `OUT.calls.jsonl` next to it: one text-free line per call, whose SHA-256 is `calls_jsonl_sha256`.

Exit status 0 only if every planned document was indexed, the model names the gateway saw are exactly the two given, no
connection other than to the gateway was attempted, and (with `--stub-shape`) the gateway and the stub agree. Otherwise 1
(a builder failure is recorded in the JSON under `failure`). Exit status 2: bad arguments or environment.

What a checkpoint holds (from the gateway's own log, `meter.jsonl`, plus its body log for the request):
    by_kind[kind]   calls, ok, input_tokens, output_tokens, latency_ms (sum), models, http_statuses; embedding: inputs
    total           the same, over all kinds
    repeats         requests whose body hash occurs more than once (a retry or a concurrent duplicate: the log cannot
                    tell which), and how many of the extra calls follow an attempt that did not end in HTTP 200
    graph           the builder's own graph sizes, as the stub runner records them
Tokens are whatever the upstream reported in `usage`; a call with no usable usage shows as `usage_missing` (zero prices
make the gateway price it at zero, so check that count: tokens of such a call are not measured, and `warnings` says so).
    client_side_retries  the OpenAI SDK's own "Retrying request" log lines, and an estimate of first attempts the client
                    abandoned (timeout) that the gateway is still waiting on. Before each checkpoint and at the end the
                    runner waits up to `--settle-s` for them, because the gateway logs a call only when the upstream
                    answers. Per-document rows are slices of the log in arrival order, so a late call can land in a later row.
`warnings` (not failures): calls without usage, calls that did not end in 200, repeated requests, unlogged abandoned calls.

Nothing written to `--out` or beside it contains article text or an absolute local path. The working directory (the
gateway's body log, the builder's storage) does hold article text, and so can the runner's own stdout/stderr (the builder
logs its progress, and on a bad JSON answer the model's text): redirect them to a scratch file, keep the working directory
outside the repository, and never commit either.
Standard library plus the builder's own environment.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata as md
import json
import logging
import os
import platform
import re
import signal
import sys
import time
import traceback
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True  # importing the helpers must not leave a __pycache__ next to them in the repository
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import passa_common as pc  # noqa: E402  (standard library only)
import x2_nano_graphrag as base  # noqa: E402  (the stub runner: corpus loading, network guard, classifier, shape-B responder)

RUNNER_FILE = "tools/exp/x2_passa_nano_graphrag.py"
DEAD_PROXY = "http://127.0.0.1:9"
PROBE_TEXT = "dimension probe"
CREDENTIAL_NAME = re.compile(r"KEY|TOKEN|SECRET|PASSW|CREDENTIAL|AUTH", re.IGNORECASE)
LOCAL_PATH = re.compile(r"/(?:Users|private|var|tmp|home|opt)/[^\s'\"):,\]}]*")
DOCUMENT_COUNT = 20


# ---------------------------------------------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------------------------------------------
def utc_now() -> str:
    return base.utc_now()


def fail_args(message: str) -> "SystemExit":
    print(f"x2_passa_nano_graphrag: {message}", file=sys.stderr)
    return SystemExit(2)


def parse_checkpoints(text: str) -> list[int]:
    try:
        values = sorted({int(x) for x in text.split(",") if x.strip()})
    except ValueError:
        raise fail_args(f"--checkpoints must be comma-separated integers, got {text!r}") from None
    if not values or values[0] < 1 or values[-1] > DOCUMENT_COUNT:
        raise fail_args(f"--checkpoints must lie in 1..{DOCUMENT_COUNT}, got {text!r}")
    return values


def harden_environment(tiktoken_cache: str | None) -> dict:
    """Refuse a credential-looking variable, then fix the proxy settings (dead proxy, loopback excluded) and the dummy key.

    The caller is expected to start the runner under `env -i`; this is the second line of defence. The gateway is started
    with its own minimal environment by `passa_common.LocalGateway`, so nothing here reaches it.
    """
    flagged = sorted(n for n in os.environ if CREDENTIAL_NAME.search(n))
    if flagged:
        raise fail_args(f"refusing to start: variables whose names look like credentials are set ({', '.join(flagged)}); "
                        "start the runner under `env -i PATH=... HOME=...`")
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
        os.environ[name] = DEAD_PROXY
    for name in ("NO_PROXY", "no_proxy"):
        os.environ[name] = "127.0.0.1,localhost"
    if tiktoken_cache:
        os.environ["TIKTOKEN_CACHE_DIR"] = str(Path(tiktoken_cache).resolve())
    os.environ["OPENAI_API_KEY"] = base.DUMMY_KEY
    # The runner's own loopback requests (preflight, summary) must not go through any proxy.
    urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler({})))
    return {"http_proxy": DEAD_PROXY, "no_proxy": "127.0.0.1,localhost", "tiktoken_cache_dir_set": bool(tiktoken_cache),
            "api_key": "dummy (not a key)"}


def get_json(url: str, timeout: float = 10.0):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read())


def run_preflight(mode: str, upstream_url: str, model: str, embed_model: str, min_ctx: int) -> dict:
    """Ollama's own checks when the upstream is an Ollama server; recorded as skipped for anything else."""
    if mode == "skip":
        return {"mode": "skip"}
    ollama_url = re.sub(r"/v1/?$", "", upstream_url.rstrip("/"))
    try:
        version = get_json(ollama_url + "/api/version")
        is_ollama = isinstance(version, dict) and "version" in version
        reason = "" if is_ollama else "GET /api/version did not return a version"
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        is_ollama, reason = False, f"GET /api/version failed: {type(exc).__name__}"
    if not is_ollama:
        if mode == "require":
            raise pc.PassAError(f"--preflight require, but the upstream is not an Ollama server ({reason})")
        return {"mode": mode, "ollama": False, "skipped": reason}
    facts = pc.preflight(ollama_url, model, min_ctx=min_ctx, embed_model=embed_model)  # raises PassAError when unsafe
    return {"mode": mode, "ollama": True, "min_ctx": min_ctx, "facts": facts}


def describe_exception(exc: BaseException) -> dict:
    """The exception's class and where it was raised. Not its message: a message can quote the model's text, which can
    quote an article. The full traceback goes to a file in the working directory instead."""
    frames = []
    for fs in traceback.extract_tb(exc.__traceback__)[-6:]:
        name = fs.filename
        frames.append(f"{name.split('site-packages/')[-1] if 'site-packages/' in name else Path(name).name}:{fs.lineno} {fs.name}")
    return {"type": f"{type(exc).__module__}.{type(exc).__name__}", "raised_at": frames, "message_chars": len(str(exc))}


class Scrubber:
    """Any absolute local path that reaches a written file is replaced and counted; a count above zero is a defect."""

    def __init__(self) -> None:
        self.count = 0

    def __call__(self, text: str) -> str:
        text, n = LOCAL_PATH.subn("<path>", text)
        self.count += n
        return text


def write_json(path: Path, obj: dict, scrub: Scrubber) -> None:
    text = scrub(json.dumps(obj, indent=1, sort_keys=True)) + "\n"
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


# ---------------------------------------------------------------------------------------------------------------
# Reading the gateway's log
# ---------------------------------------------------------------------------------------------------------------
class RequestView:
    """What `x2_nano_graphrag.make_classifier` reads from a stub call (`path`, `messages`), taken from a gateway call."""

    def __init__(self, call: dict) -> None:
        request = call.get("request")
        self.path = call.get("route") or ""
        messages = request.get("messages") if isinstance(request, dict) else None
        self.messages = messages if isinstance(messages, list) else []


def gateway_classifier(classify):
    def classify_call(call: dict) -> str:
        if not isinstance(call.get("request"), dict):
            return "unparsed_request"
        return classify(RequestView(call))

    return classify_call


def by_kind_from_gateway(calls: list[dict], classify_call) -> dict:
    summary = pc.summarize(calls, classify_call)
    extra: dict[str, dict] = defaultdict(lambda: {"models": Counter(), "http_statuses": Counter(), "inputs": 0})
    for c in calls:
        kind = classify_call(c) if c.get("request") is not None else "no_body"
        e = extra[kind]
        e["models"][str(c.get("model_requested"))] += 1
        e["http_statuses"][str(c.get("http_status"))] += 1
        request = c.get("request")
        if isinstance(request, dict) and kind == "embedding":
            value = request.get("input")
            e["inputs"] += len(value) if isinstance(value, list) else (1 if value is not None else 0)
    for kind, row in summary["by_kind"].items():
        row["models"] = dict(extra[kind]["models"])
        row["http_statuses"] = dict(extra[kind]["http_statuses"])
        if kind == "embedding":
            row["inputs"] = extra[kind]["inputs"]
    return summary


def repeats(calls: list[dict]) -> dict:
    """Requests whose body is byte-identical to an earlier one. A retry after a failure looks like this, and so does a
    second, concurrent request for the same prompt; the log alone cannot tell them apart, so the second count says how
    many of the extra calls came after an attempt that did not end in HTTP 200."""
    statuses: dict[str, list] = defaultdict(list)
    for c in calls:
        statuses[c.get("request_sha256")].append(c.get("http_status"))
    repeated = {h: s for h, s in statuses.items() if len(s) > 1}
    return {
        "distinct_requests": len(statuses),
        "repeated_requests": len(repeated),
        "extra_calls": sum(len(s) - 1 for s in repeated.values()),
        "extra_calls_after_a_non_200_attempt": sum(
            sum(1 for i in range(1, len(s)) if any(x != 200 for x in s[:i])) for s in repeated.values()),
    }


def request_params_by_kind(calls: list[dict], classify_call) -> dict:
    """For each kind of call, the request's keys and the distinct values of every key except the text itself: the
    request surface a local server must accept."""
    seen: dict = defaultdict(lambda: defaultdict(set))
    for c in calls:
        request = c.get("request")
        if not isinstance(request, dict):
            continue
        kind = classify_call(c)
        for key, val in request.items():
            seen[kind][key].add("<text>" if key in ("messages", "input") else json.dumps(val, sort_keys=True))
    return {k: {key: sorted(vals) for key, vals in sorted(d.items())} for k, d in sorted(seen.items())}


def request_multiset_digest(calls: list[dict], classify_call) -> str:
    rows = sorted((classify_call(c), c.get("route"), c.get("request_sha256")) for c in calls)
    return hashlib.sha256(json.dumps(rows).encode("utf-8")).hexdigest()


def sanitized_call_rows(calls: list[dict], classify_call) -> list[dict]:
    keep = ("ts", "route", "model_requested", "model_reported", "http_status", "input_tokens", "output_tokens",
            "cached_input_tokens", "latency_ms", "voided", "usage_missing", "streamed", "refusal", "error",
            "request_sha256", "bytes_in", "bytes_out")
    return [{"seq": i, "kind": classify_call(c) if c.get("request") is not None else "no_body", **{k: c.get(k) for k in keep}}
            for i, c in enumerate(calls, start=1)]


class RetryLines(logging.Handler):
    """Counts the OpenAI SDK's own "Retrying request" log lines (client side: it sees a retry even when the first attempt
    was abandoned on a timeout and has not reached the gateway's log yet)."""

    def __init__(self) -> None:
        super().__init__(logging.INFO)
        self.count = 0

    def emit(self, record: logging.LogRecord) -> None:
        if "Retrying request" in record.getMessage():
            self.count += 1


def settle(calls_now, retries: RetryLines, max_s: float) -> dict:
    """Wait for calls the client abandoned (on a timeout, say) and the gateway is still waiting on. The gateway writes a
    call's record when the upstream answers, and the SDK's retry of an abandoned call is a new request, so a client-side
    retry that the log shows no repeat for may be a first attempt still in flight. The estimate is
    max(0, SDK retry lines - repeated requests in the log); it undercounts when concurrent duplicates also repeat."""
    t0 = time.time()
    while True:
        pending = retries.count - repeats(calls_now())["extra_calls"]
        if pending <= 0 or time.time() - t0 >= max_s:
            return {"sdk_retry_log_lines": retries.count, "pending_estimate": max(pending, 0),
                    "waited_s": round(time.time() - t0, 1)}
        time.sleep(1.0)


def graph_state(rag) -> dict:
    import networkx as nx

    g = rag.chunk_entity_relation_graph._graph
    comps = [len(c) for c in nx.connected_components(g)]
    return {
        "nodes": g.number_of_nodes(),
        "edges": g.number_of_edges(),
        "connected_components": len(comps),
        "largest_component_nodes": max(comps) if comps else 0,
        "nodes_with_cluster_data": sum(1 for _, dta in g.nodes(data=True) if "clusters" in dta),
        "communities_in_report_store": len(rag.community_reports._data),
        "documents_stored": len(rag.full_docs._data),
        "chunks_stored": len(rag.text_chunks._data),
    }


def compare_with_stub(gateway_kinds: dict, stub_kinds: dict) -> dict:
    """Gateway-side counts against the stub's own counts, kind by kind: calls, input tokens (the stub's prompt tokens),
    output tokens (its completion tokens) and embedding inputs."""
    diffs = []
    for kind in sorted(set(gateway_kinds) | set(stub_kinds)):
        g, s = gateway_kinds.get(kind), stub_kinds.get(kind)
        if g is None or s is None:
            diffs.append({"kind": kind, "field": "present", "gateway": g is not None, "stub": s is not None})
            continue
        pairs = [("calls", g["calls"], s["calls"]), ("input_tokens", g["input_tokens"], s["prompt_tokens"]),
                 ("output_tokens", g["output_tokens"], s["completion_tokens"])]
        if kind == "embedding":
            pairs.append(("inputs", g.get("inputs"), s.get("inputs")))
        diffs.extend({"kind": kind, "field": f, "gateway": a, "stub": b} for f, a, b in pairs if a != b)
    return {"identical": not diffs, "differences": diffs}


# ---------------------------------------------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------------------------------------------
def make_builder_functions(llm, model: str, embed_model: str, dim: int):
    """The builder's model slots with real model names. The chat functions call the builder's own
    `openai_complete_if_cache` (its cache key, message layout, retry policy and SDK client are unchanged); only the
    hard-coded model name differs. The embedding function repeats `openai_embedding` from the builder's `_llm.py`
    (same SDK client, same call, same retry policy) with the embedding model's name and dimension."""
    import numpy as np
    from nano_graphrag._utils import wrap_embedding_func_with_attrs
    from openai import APIConnectionError, RateLimitError
    from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

    async def complete(prompt, system_prompt=None, history_messages=None, **kwargs) -> str:
        return await llm.openai_complete_if_cache(
            model, prompt, system_prompt=system_prompt, history_messages=history_messages or [], **kwargs)

    @wrap_embedding_func_with_attrs(embedding_dim=dim, max_token_size=8192)
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10),
           retry=retry_if_exception_type((RateLimitError, APIConnectionError)))
    async def embed(texts: list[str]):
        client = llm.get_openai_async_client_instance()
        response = await client.embeddings.create(model=embed_model, input=texts, encoding_format="float")
        return np.array([dp.embedding for dp in response.data])

    return complete, embed


def probe_embedding_dimension(gateway_url: str, embed_model: str) -> int:
    """One embeddings call through the gateway; the vector length is the builder's embedding dimension."""
    from openai import OpenAI

    client = OpenAI(base_url=gateway_url, api_key=base.DUMMY_KEY, max_retries=0, timeout=600)
    response = client.embeddings.create(model=embed_model, input=[PROBE_TEXT], encoding_format="float")
    return len(response.data[0].embedding)


def run(args: argparse.Namespace) -> int:
    scrub = Scrubber()
    started = time.time()
    checkpoints = parse_checkpoints(args.checkpoints)
    planned = checkpoints[-1]
    if bool(args.upstream_url) == bool(args.stub_shape):
        raise fail_args("give exactly one of --upstream-url and --stub-shape")
    # Absolute paths: the gateway is started with the working directory as its own cwd, so a relative one would not resolve.
    workdir, out_path = Path(args.workdir).resolve(), Path(args.out).resolve()
    repo_root = Path(args.repo_root).resolve()
    environment = harden_environment(args.tiktoken_cache)
    if workdir.exists() and any(workdir.iterdir()):
        raise fail_args("--workdir must be new or empty (the gateway log and the builder's storage must start clean)")
    workdir.mkdir(parents=True, exist_ok=True)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    calls_path = out_path.with_name(out_path.stem + ".calls.jsonl")

    docs = base.load_documents(args.corpus, args.documents)
    if len(docs) != DOCUMENT_COUNT:
        raise fail_args(f"expected {DOCUMENT_COUNT} documents, got {len(docs)}")
    docs = docs[:planned]

    result: dict = {
        "runner": {"file": RUNNER_FILE, "checkpoints": checkpoints, "documents_planned": planned},
        "builder": "nano-graphrag",
        "version": md.version("nano-graphrag"),
        "upstream_url": args.upstream_url or "stub (hosted by the runner)",
        "model": args.model,
        "embed_model": args.embed_model,
        "chat_request_defaults": pc.chat_defaults(args),
        "corpus_sha256": base.CORPUS_SHA256,
        "environment": environment,
        "status": "starting",
        "started_utc": utc_now(),
        "finished_utc": None,
        "checkpoints": {},
        "per_document": [],
        "failures": [],
    }
    failures: list[str] = result["failures"]

    def save() -> None:
        write_json(out_path, result, scrub)

    def on_term(signum, frame):  # noqa: ANN001
        raise KeyboardInterrupt(f"signal {signum}")

    signal.signal(signal.SIGTERM, on_term)

    upstream_url = args.upstream_url
    if upstream_url:
        try:
            result["preflight"] = run_preflight(args.preflight, upstream_url, args.model, args.embed_model, args.min_ctx)
        except pc.PassAError as exc:
            result.update(status="failed", finished_utc=utc_now())
            failures.append("preflight refused to start")
            result["failure"] = {"stage": "preflight", "message": scrub(str(exc))}
            save()
            print(f"preflight: {scrub(str(exc))}", file=sys.stderr)
            return 1
    else:
        result["preflight"] = {"mode": args.preflight, "ollama": False, "skipped": "the upstream is the stub hosted by the runner"}

    guard = base.NetGuard()
    guard.install()  # from here on a connect to anything but the gateway is recorded, and a non-loopback one refused
    stub = None
    gw = None
    try:
        import nano_graphrag
        import nano_graphrag._llm as llm
        from nano_graphrag import GraphRAG
        from nano_graphrag.prompt import PROMPTS

        classify_stub = base.make_classifier(PROMPTS)  # reads a stub_llm.Call
        classify_call = gateway_classifier(classify_stub)  # the same classification, reading a gateway log entry
        produced = None
        if args.stub_shape:
            from stub_llm import Stub

            responder, produced = base.make_responder(args.stub_shape, PROMPTS, classify_stub)
            stub = Stub(responder, default_dims=args.stub_dims).start()
            upstream_url = stub.base_url
            result["runner"]["stub_shape"] = args.stub_shape
            result["runner"]["stub_dims"] = args.stub_dims

        gw = pc.LocalGateway(workdir / "gateway", upstream_url, [args.model, args.embed_model], repo_root,
                                request_defaults={args.model: pc.chat_defaults(args)}).start()
        guard.stub_port = gw.port
        os.environ["OPENAI_BASE_URL"] = gw.base_url

        # ---- the embedding dimension, from one call through the gateway
        dim = probe_embedding_dimension(gw.base_url, args.embed_model)
        first = gw.calls()
        if len(first) != 1 or first[0].get("route") != "/v1/embeddings" or (first[0].get("request") or {}).get("input") != [PROBE_TEXT]:
            raise RuntimeError("the first logged call is not the dimension probe")
        probe_n = len(first)
        stub_probe_n = len(stub.calls) if stub else 0
        result["embedding_dim"] = dim
        result["dimension_probe"] = {key: first[0].get(key) for key in ("http_status", "input_tokens", "latency_ms", "usage_missing")}
        result["dimension_probe"]["excluded_from_all_counts"] = True
        print(f"[{utc_now()}] gateway on port {gw.port}; embedding dimension {dim}; "
              f"{probe_n} probe call excluded from counts", flush=True)

        # ---- the builder
        retry_lines = RetryLines()
        sdk_logger = logging.getLogger("openai._base_client")
        sdk_logger.setLevel(logging.INFO)
        sdk_logger.addHandler(retry_lines)
        best, embed = make_builder_functions(llm, args.model, args.embed_model, dim)
        if args.client_timeout_s:
            from openai import AsyncOpenAI

            llm.global_openai_async_client = AsyncOpenAI(timeout=args.client_timeout_s)
        options = {}
        if args.max_async:
            options = {"best_model_max_async": args.max_async, "cheap_model_max_async": args.max_async,
                       "embedding_func_max_async": args.max_async}
        rag = GraphRAG(working_dir=str(workdir / "rag"), best_model_func=best, cheap_model_func=best,
                       embedding_func=embed, **options)
        defaults = {k: getattr(rag, k) for k in (
            "chunk_token_size", "chunk_overlap_token_size", "tiktoken_model_name", "entity_extract_max_gleaning",
            "entity_summary_to_max_tokens", "graph_cluster_algorithm", "max_graph_cluster_size", "embedding_batch_num",
            "embedding_func_max_async", "best_model_max_async", "cheap_model_max_async", "enable_local", "enable_naive_rag",
            "enable_llm_cache")}
        result["defaults_observed"] = defaults
        result["builder_overrides"] = {
            "chat_model_for_both_slots": args.model, "embedding_model": args.embed_model, "embedding_dim": dim,
            "max_async": args.max_async, "client_timeout_s": args.client_timeout_s,
            "note": "every other setting is the builder's default"}

        def calls_now() -> list[dict]:
            return gw.calls()[probe_n:]

        def snapshot(n_docs: int, index_seconds: float) -> dict:
            settled = settle(calls_now, retry_lines, args.settle_s)
            calls = calls_now()
            summary = by_kind_from_gateway(calls, classify_call)
            snap = {
                "n_docs": n_docs,
                "indexing_seconds_so_far": round(index_seconds, 1),
                "calls": len(calls),
                "by_kind": summary["by_kind"],
                "total": summary["total"],
                "http_statuses": dict(Counter(str(c.get("http_status")) for c in calls)),
                "refusals": dict(Counter(c["refusal"] for c in calls if c.get("refusal"))),
                "errors": dict(Counter(c["error"] for c in calls if c.get("error"))),
                "voided": sum(1 for c in calls if c.get("voided")),
                "usage_missing": sum(1 for c in calls if c.get("usage_missing")),
                "repeats": repeats(calls),
                "client_side_retries": settled,
                "request_multiset_sha256": request_multiset_digest(calls, classify_call),
            }
            try:
                snap["graph"] = graph_state(rag)
            except Exception as exc:  # noqa: BLE001 - a half-built graph must not hide the call counts
                snap["graph"] = {"unavailable": describe_exception(exc)}
            if stub:
                stub_kinds = base.kind_table(stub.calls[stub_probe_n:], classify_stub)
                snap["stub_side_by_kind"] = stub_kinds
                snap["gateway_vs_stub"] = compare_with_stub(summary["by_kind"], stub_kinds)
            return snap

        # ---- indexing, one document at a time
        result["status"] = "running"
        save()
        index_seconds = 0.0
        indexed = 0
        failure = None
        for i, d in enumerate(docs, start=1):
            before = len(calls_now())
            t0 = time.time()
            try:
                rag.insert(d["body"])
            except Exception as exc:  # noqa: BLE001 - recorded, then the run stops
                (workdir / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
                failure = {"stage": "index", "document_index": i, "rank": d["rank"], **describe_exception(exc),
                           "traceback_file": "failure.txt in the working directory (holds the message, which may quote text)"}
                index_seconds += time.time() - t0
                result["failure_snapshot"] = snapshot(i - 1, index_seconds)
                break
            seconds = time.time() - t0
            index_seconds += seconds
            indexed = i
            new_calls = calls_now()[before:]
            row_kinds = by_kind_from_gateway(new_calls, classify_call)
            result["per_document"].append({
                "rank": d["rank"], "url_sha256_16": d["url_sha256_16"], "chars": d["chars"], "seconds": round(seconds, 2),
                "by_kind": row_kinds["by_kind"], "total": row_kinds["total"], "graph_after": graph_state(rag)})
            if i in checkpoints:
                result["checkpoints"][str(i)] = snapshot(i, index_seconds)
            print(f"[{utc_now()}] document {i}/{planned} indexed in {seconds:.1f} s; "
                  f"{row_kinds['total']['calls']} calls ({row_kinds['total']['ok']} ok)", flush=True)
            save()

        # ---- the end: totals, summary, a closing list of what to check
        result["final_settle"] = settle(calls_now, retry_lines, args.settle_s)
        final_calls = calls_now()
        try:
            gateway_summary = get_json(f"http://127.0.0.1:{gw.port}/_meter/summary")
        except (urllib.error.URLError, ValueError, OSError) as exc:
            gateway_summary = {"unavailable": type(exc).__name__}
        try:
            client = llm.get_openai_async_client_instance()
            result["openai_sdk_in_use"] = {"max_retries": client.max_retries, "timeout_seconds": str(client.timeout)}
        except Exception as exc:  # noqa: BLE001
            result["openai_sdk_in_use"] = {"unavailable": type(exc).__name__}
        try:
            result["chunking_arithmetic"] = base.chunking_arithmetic(docs, defaults)
        except Exception as exc:  # noqa: BLE001 - needs the tokenizer vocabulary (see --tiktoken-cache)
            result["chunking_arithmetic"] = {"unavailable": describe_exception(exc)}
        result["request_params_by_kind"] = request_params_by_kind(final_calls, classify_call)
        result["gateway_summary"] = gateway_summary
        if produced is not None:
            result["answers_produced_by_responder"] = dict(produced)
        warnings = []
        no_usage = sum(1 for c in final_calls if c.get("usage_missing"))
        if no_usage:
            warnings.append(f"{no_usage} calls have no usable usage from the upstream: their tokens are NOT measured")
        not_ok = Counter(str(c.get("http_status")) for c in final_calls if c.get("http_status") != 200)
        if not_ok:
            warnings.append(f"calls that did not end in HTTP 200: {dict(not_ok)}")
        again = repeats(final_calls)
        if again["extra_calls"]:
            warnings.append(f"{again['extra_calls']} requests repeat an earlier identical one (a retry or a concurrent duplicate; "
                            f"{again['extra_calls_after_a_non_200_attempt']} follow a non-200 attempt)")
        if result["final_settle"]["pending_estimate"]:
            warnings.append(f"about {result['final_settle']['pending_estimate']} abandoned call(s) were still unlogged when "
                            "the settle wait ended: the log may be incomplete")
        result["warnings"] = warnings
        names_sent = Counter((classify_call(c) == "embedding", c.get("model_requested")) for c in final_calls)
        wrong_names = {f"{'embeddings' if emb else 'chat'}: {name}": n for (emb, name), n in names_sent.items()
                       if name != (args.embed_model if emb else args.model)}
        result["model_name_check"] = {"chat_names_sent": sorted({n for (e, n) in names_sent if not e}),
                                      "embedding_names_sent": sorted({n for (e, n) in names_sent if e}),
                                      "calls_with_an_unexpected_name": wrong_names}
        if wrong_names:
            failures.append(f"calls with an unexpected model name: {wrong_names}")
        if failure:
            result["failure"] = failure
            failures.append(f"the builder failed on document {failure['document_index']} of {planned}")
        elif indexed != planned:
            failures.append(f"only {indexed} of {planned} documents were indexed")
        if stub:
            mismatches = [n for n, s in result["checkpoints"].items() if not s["gateway_vs_stub"]["identical"]]
            if mismatches or (failure and not result["failure_snapshot"]["gateway_vs_stub"]["identical"]):
                failures.append(f"gateway and stub counts differ (checkpoints {mismatches or 'failure snapshot'})")
        report = guard.report()
        result["network_guard"] = report
        if report["connect_attempts"]:
            failures.append("the builder process attempted a connection other than to the gateway")
        result["runtime"] = {
            "python": platform.python_version(), "machine": platform.machine(),
            "nano_graphrag_version": getattr(nano_graphrag, "__version__", "unstated"),
            "packages": {p: md.version(p) for p in ("openai", "tiktoken", "networkx", "graspologic", "nano-vectordb", "numpy",
                                                   "tenacity", "httpx")}}
        gw_rows = sanitized_call_rows(final_calls, classify_call)
    except KeyboardInterrupt as exc:
        result["status"] = "interrupted"
        failures.append(f"interrupted ({exc})")
        gw_rows = None
    except Exception as exc:  # noqa: BLE001 - setup failures (gateway, builder import, dimension probe) end here
        if workdir.exists():
            (workdir / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
        result["failure"] = {"stage": "setup", **describe_exception(exc),
                             "traceback_file": "failure.txt in the working directory"}
        failures.append("setup failed before indexing")
        gw_rows = None
    finally:
        if gw is not None:
            gw.stop()
        if stub is not None:
            stub.stop()

    if gw_rows is not None:
        calls_text = "".join(json.dumps(r, sort_keys=True) + "\n" for r in gw_rows)
        calls_path.write_text(calls_text, encoding="utf-8")
        result["calls_jsonl"] = calls_path.name
        result["calls_jsonl_sha256"] = hashlib.sha256(calls_text.encode("utf-8")).hexdigest()
    if result["status"] in ("starting", "running"):
        result["status"] = "failed" if failures else "complete"
    result["finished_utc"] = utc_now()
    result["wall_seconds"] = round(time.time() - started, 1)
    save()
    if scrub.count:
        failures.append(f"{scrub.count} absolute local path(s) were replaced by <path> in the result file")
        save()
    exit_code = 0 if not failures and result["status"] == "complete" else 1
    print(f"[{utc_now()}] {result['status']}; wrote {out_path.name}; failures: {failures or 'none'}; "
          f"warnings: {result.get('warnings') or 'none'}", flush=True)
    return exit_code


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus", required=True, help="corpus.json (checked against its pinned SHA-256)")
    ap.add_argument("--documents", required=True, help="documents.tsv (the 20 frozen documents, selected by the url column)")
    ap.add_argument("--repo-root", required=True, help="the repository root (tools/metering_gateway.py is started from it)")
    ap.add_argument("--upstream-url", help="the upstream's OpenAI-compatible base URL, e.g. http://127.0.0.1:11434/v1")
    ap.add_argument("--model", required=True, help="chat model name; the builder sends exactly this for both its model slots")
    ap.add_argument("--embed-model", required=True, help="embedding model name; the builder sends exactly this")
    pc.add_chat_default_argument(ap)
    ap.add_argument("--workdir", required=True, help="new or empty directory: the gateway's logs and the builder's storage (hold article text)")
    ap.add_argument("--out", required=True, help="result JSON (rewritten after every document); OUT.calls.jsonl is written beside it")
    ap.add_argument("--checkpoints", default="1,5,20", help="document counts at which to record; indexing stops after the largest (default 1,5,20)")
    ap.add_argument("--tiktoken-cache", help="directory holding the tokenizer vocabularies (the builder's chunker needs o200k_base; offline)")
    ap.add_argument("--preflight", choices=["auto", "require", "skip"], default="auto",
                    help="Ollama context check: auto = when the upstream answers /api/version (default), require = error otherwise, skip")
    ap.add_argument("--min-ctx", type=int, default=16384, help="smallest explicit num_ctx the preflight accepts (default 16384)")
    ap.add_argument("--max-async", type=int, help="override the builder's concurrency (16 per slot by default) for chat and embeddings")
    ap.add_argument("--client-timeout-s", type=float, help="override the OpenAI SDK's read timeout (600 s by default)")
    ap.add_argument("--settle-s", type=float, default=120.0,
                    help="at each checkpoint and at the end, wait up to this long for calls the client abandoned on a timeout "
                         "and the gateway is still waiting on (default 120; no wait when the SDK retried nothing)")
    ap.add_argument("--stub-shape", choices=["A", "B"], help="host the stub model server as the upstream (free check); replaces --upstream-url")
    ap.add_argument("--stub-dims", type=int, default=1536, help="embedding length the hosted stub answers with (default 1536)")
    args = ap.parse_args()
    if not args.stub_shape and not args.upstream_url:
        ap.error("give --upstream-url (or --stub-shape for the free check)")
    sys.exit(run(args))


if __name__ == "__main__":
    main()
