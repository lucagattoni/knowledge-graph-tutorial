#!/usr/bin/env python3
"""X2 pass A for fast-graphrag: the builder indexes the 20 frozen documents through the metering gateway.

    VENV_PYTHON tools/exp/x2_passa_fast_graphrag.py \\
        --corpus CORPUS_JSON --documents kb-kg/experiments/x2-index-cost/documents.tsv --repo-root . \\
        --upstream-url http://127.0.0.1:PORT/v1 --model CHAT_MODEL --embed-model EMBED_MODEL \\
        --workdir NEW_EMPTY_DIR --out RESULT_JSON [--checkpoints 1,5,20] [--tiktoken-cache DIR] \\
        [--preflight-min-ctx 16384] [--llm-timeout-s 1800] [--llm-concurrency N] [--continue-after-failure]
        [--hosted-profile PROFILE_JSON]

VENV_PYTHON is the python of the throwaway environment that holds fast-graphrag (the same one the stub rehearsal
`x2_fast_graphrag.py` uses). The upstream is whatever speaks the OpenAI protocol at `--upstream-url`: the stub
(`stub_llm.Stub`) to check the plumbing for free, a local Ollama later. The runner is the same for both.

What it does. The parent process (standard library only) starts the metering gateway (`passa_common.LocalGateway`) in
`WORKDIR/gateway`, makes one embeddings call through it to learn the embedding model's vector length, then starts one
child process with a minimal environment (no inherited variables; proxies pointed at a closed port with loopback
excluded; a dummy key; a socket guard that refuses and records anything beyond loopback). The child points
fast-graphrag at the gateway with the REAL model names, builds `GraphRAG` with the vector length it was given, and
indexes the documents one at a time with `GraphRAG.insert`, on the library's configuration. It changes only what is
named under `builder_settings.changed_from_library_defaults` in the output. After the child exits, the parent reads
the gateway's own log (the provider's usage as logged) and builds the checkpoints from it.

Pass B (`--hosted-profile PROFILE_JSON`, see `passb_common.py` and `passb_profile.example.json`). The CHAT model (`--model`) is
served by a hosted provider through the same gateway, which holds the key (it reads the file the profile names; neither this
parent nor the child ever does) and refuses past the cap; `--upstream-url` and `--embed-model` stay the LOCAL embedding
upstream, and only the embedding model is checked in Ollama. The output gains a `hosted` block (cost, prices with their source,
the model name as the provider reports it, the shared ledger's size before the run; never the key file's path or the ledger's)
and a `cost_usd` on every checkpoint and document row. The gateway log is the profile's shared ledger and `gw.calls()` returns
only this run's records, so every number below is this run's. The gateway's own timeout is the profile's. Without the option
nothing in this program changes.

What the numbers are. Calls by kind, HTTP statuses, `input_tokens`, `output_tokens` and `latency_ms` are the
gateway's record of each call: the tokens are the provider's own usage fields (for the stub, what the stub counted).
A call is attributed to a document by the time it arrived at the gateway: documents are indexed one after another, and
a call that arrived before the child started is the one-call embedding probe, not the builder's. Retries show in
three places: `retry_calls` (instructor re-asking after an answer it could not parse; the request ends with the failed
answer), `repeated_identical_requests` (the same request body sent again, which is what an SDK retry after a timeout
or a 5xx looks like; identical EMBEDDING requests can also be legitimate) and `sdk_retries_logged` (the OpenAI SDK's
own log line, counted in the child).

What it does not change between upstreams: the prompts, the user-side inputs (domain sentence, example queries and
entity types are imported from `x2_fast_graphrag.py`, so they are the rehearsal's, by construction), the call
classification, the network guard, and the minimal environment.

Exit status 0 only if every document was indexed. A document counts as indexed only if `insert` did not raise AND
the chunk count of the graph grew by the number of chunks the library's own chunker made for it: fast-graphrag
swallows an extraction error for a whole document (one chunk the model cannot answer in valid JSON drops the document's
chunks, with an ERROR log line and no exception), so a missing chunk count is how a silent drop shows. The run stops at
the first document that was not indexed, unless `--continue-after-failure` is given. Failures are recorded in the
output as the exception TYPE, the message length and a short hash of the message; the message itself can contain
model output (and so article text), so it is written only to `WORKDIR/child_failures.log`.

Files. Everything the run writes goes under WORKDIR (outside the repository: `gateway/meter.jsonl.bodies.jsonl` holds
article text and must never be committed) and to `--out`, which holds no article text and no absolute local path.

Defaults this runner changes, and why (also recorded in the output under builder_settings):
  --llm-timeout-s 1800  The library's OpenAI client times out a chat request after 180 s (a constant in the library).
      That time includes the time a request waits in the server's queue. An insert sends all of a document's chunks at
      once (up to 1024 requests in flight); a local server that answers one or a few at a time queues the rest, a queued
      request can pass 180 s, and the SDK then sends it again (up to twice) while the server may still be working on
      the first. The library's own retry loop (3 attempts, around the SDK) repeats that, so one chunk can cost up to 9
      requests (measured against a stub that answers slower than the timeout: 27 requests for 3 chunks). The timeout
      is only a bound on a stuck request, so it is raised; the gateway's own timeout towards the upstream is 1800 s too.
  --llm-concurrency N   NOT changed unless given: the library's own limit (1024 requests in flight) stays, so the
      failure path behaves as it did in the stub rehearsal. Reason to leave it: with 1 request at a time, a chunk
      whose answer cannot be parsed ends the document's gather at once, and the document's other chunk tasks (still
      waiting their turn) are not cancelled but run later, during the NEXT document's window; their calls are then
      attributed to the wrong document (seen against the stub with an unparseable answer: one request at a time gave 3
      calls in the failing document's window, all requests at once gave the 9 of the stub rehearsal's probe). Reason
      to set it: a server that thrashes
      under many parallel requests. Either way `latency_ms` of a call includes any time it waited in the server's queue,
      so with a slow local model the sum of `latency_ms` is not compute time; the wall time of the run is.
  One more thing to know: when a document is dropped (see above), calls of its chunk tasks that are still running can
  arrive after `insert` returned and are attributed by arrival time to the next document, or to "after the last
  document".
"""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True  # importing the siblings must not write bytecode into the repository
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import x2_fast_graphrag as rehearsal  # noqa: E402  (standard library only at import: classifier, inputs, guard, loader)
import passb_common as pb  # noqa: E402
from passa_common import PassAError, add_chat_default_argument, chat_defaults, preflight, summarize  # noqa: E402

RUNNER = "x2_passa_fast_graphrag.py"
DUMMY_KEY = "dummy-not-a-key"
TOKEN_KEYS = ("calls", "ok", "input_tokens", "output_tokens", "latency_ms")
SETTLE_SECONDS = 3.0
LONG_SETTLE_SECONDS = 30.0  # used when the SDK retried a request: the first attempt may still be running upstream


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d %H:%M:%S")


def scrub(text: str, limit: int = 300) -> str:
    """A free-text error message made fit for the output: file paths replaced, cut short, first lines only."""
    one_line = " | ".join(line.strip() for line in str(text).splitlines() if line.strip())
    return re.sub(r"(?:~|\.{0,2})?(?:/[^\s\"'|:]+){2,}", "<path>", one_line)[:limit]


# ---------------------------------------------------------------------------------------------------------------------
# Reading the gateway's record (parent side; pure functions of the call dicts)
# ---------------------------------------------------------------------------------------------------------------------


def classify_call(c: dict) -> str:
    """The kind of one gateway record: 'embedding', or the stub rehearsal's classification of the chat request."""
    if str(c.get("route", "")).endswith("/embeddings"):
        return "embedding"
    req = c.get("request")
    if isinstance(req, dict) and isinstance(req.get("messages"), list):
        return rehearsal.classify(req["messages"])[0]
    return "other"


def is_retry_call(c: dict) -> bool:
    """instructor re-asking: the request does not end with the prompt (the failed answer and an error follow it)."""
    req = c.get("request")
    if isinstance(req, dict) and isinstance(req.get("messages"), list) and not str(c.get("route", "")).endswith("/embeddings"):
        return rehearsal.classify(req["messages"])[1]
    return False


def arrival(c: dict) -> float:
    """Seconds since the epoch of the call's arrival (the gateway's `ts`, millisecond resolution, truncated)."""
    return datetime.strptime(c["ts"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).timestamp()


def attribute(calls: list[dict], t_spawn: float, ends: list[float]) -> tuple[list[dict], list[list[dict]], list[dict]]:
    """(before the child started, one list per document, after the last document ended).

    The documents are indexed one after another, so a call belongs to the first document whose end time is not before
    the call's arrival. A call that arrived before the child was started is the parent's own embedding probe."""
    before: list[dict] = []
    per_doc: list[list[dict]] = [[] for _ in ends]
    after: list[dict] = []
    for c in calls:
        t = arrival(c)
        if t <= t_spawn:
            before.append(c)
            continue
        i = bisect.bisect_left(ends, t)
        (per_doc[i] if i < len(ends) else after).append(c)
    return before, per_doc, after


def repeated(calls: list[dict]) -> int:
    """Calls whose request body was already sent earlier in this list (excess over the first of each)."""
    counts = Counter(c.get("request_sha256") for c in calls)
    return sum(n - 1 for n in counts.values() if n > 1)


def window(calls: list[dict]) -> dict:
    """The numbers for a list of calls, from the gateway's record."""
    s = summarize(calls, classify_call)
    retry_by_kind = Counter(classify_call(c) for c in calls if is_retry_call(c))
    by_kind = {}
    for kind, v in sorted(s["by_kind"].items()):
        by_kind[kind] = dict(v)
        if kind != "embedding":
            by_kind[kind]["retry_calls"] = retry_by_kind.get(kind, 0)
    zero = {k: 0 for k in TOKEN_KEYS}
    emb = s["by_kind"].get("embedding", zero)
    chat = {k: s["total"][k] - emb[k] for k in TOKEN_KEYS}
    emb_calls = [c for c in calls if classify_call(c) == "embedding"]
    chat_calls = [c for c in calls if classify_call(c) != "embedding"]
    per_request = Counter(
        str(len(c["request"]["input"]) if isinstance(c.get("request"), dict) and isinstance(c["request"].get("input"), list) else 1)
        for c in emb_calls)
    return {
        "total": s["total"],
        "chat": {**chat, "retry_calls": sum(retry_by_kind.values())},
        "embedding": {**emb, "requests": len(emb_calls),
                      "inputs": sum(int(k) * n for k, n in per_request.items()),
                      "inputs_per_request": dict(sorted(per_request.items(), key=lambda kv: int(kv[0])))},
        "by_kind": by_kind,
        "http_statuses": dict(sorted(Counter(str(c.get("http_status")) for c in calls).items())),
        "repeated_identical_requests": {"chat": repeated(chat_calls), "embedding": repeated(emb_calls)},
        "voided": sum(1 for c in calls if c.get("voided")),
        "usage_missing": sum(1 for c in calls if c.get("usage_missing")),
        "refused_by_gateway": sum(1 for c in calls if c.get("refusal")),
    }


def first_request_of_each_kind(calls: list[dict]) -> dict:
    """What the builder sends, without its text: body keys, roles, response_format, max_tokens, dimensions, model."""
    shapes: dict = {}
    for c in calls:
        kind = classify_call(c)
        req = c.get("request")
        if kind in shapes or not isinstance(req, dict):
            continue
        msgs = req.get("messages") if isinstance(req.get("messages"), list) else []
        shapes[kind] = {"route": c.get("route"), "request_body_keys": sorted(req), "n_messages": len(msgs),
                        "roles": [m.get("role") for m in msgs if isinstance(m, dict)],
                        "response_format": req.get("response_format"), "model": req.get("model"),
                        "max_tokens": req.get("max_tokens", "absent"), "dimensions": req.get("dimensions", "absent"),
                        "stream": req.get("stream", False), "http_status": c.get("http_status")}
    return dict(sorted(shapes.items()))


# ---------------------------------------------------------------------------------------------------------------------
# Child: one run of the builder, pointed at the gateway
# ---------------------------------------------------------------------------------------------------------------------


class CountingHandler(logging.Handler):
    """Counts the log records that matter for the call count and keeps no message text beyond a head: the OpenAI SDK's
    own retries, tokenizer failures, and ERROR lines (only what precedes the first colon is kept; the rest of a
    library error message can carry model output)."""

    def __init__(self) -> None:
        super().__init__(level=logging.INFO)
        self.sdk_retries = 0
        self.error_total = 0
        self.error_heads: Counter = Counter()
        self.tokenizer_failures: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        msg = record.getMessage()
        if record.name.startswith("openai") and msg.startswith("Retrying request"):
            self.sdk_retries += 1
        if "failed to load tokenizer" in msg:
            self.tokenizer_failures.append(msg[:160])
        if record.levelno >= logging.ERROR:
            self.error_total += 1
            self.error_heads[f"{record.name}: {msg.split(':', 1)[0][:80]}"] += 1


def package_fingerprint(package_dir: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(package_dir.rglob("*.py")):
        h.update(p.relative_to(package_dir).as_posix().encode("utf-8"))
        h.update(hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


def failure_record(exc: BaseException, log_path: Path, doc_n: int) -> dict:
    text = str(exc)
    with log_path.open("a", encoding="utf-8") as fh:  # the message can hold model output; it stays in the workdir
        fh.write(f"--- document {doc_n}: {type(exc).__name__}\n{text}\n")
    return {"exception_type": type(exc).__name__, "message_chars": len(text),
            "message_sha256_16": hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]}


def write_json(path: Path, obj: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def run_child(args: argparse.Namespace) -> None:
    net_log: list = []
    rehearsal.install_network_guard(net_log)
    handler = CountingHandler()
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)

    docs = rehearsal.load_documents(Path(args.corpus), Path(args.documents), args.n)
    run_dir = Path(args.run_dir)
    graph_dir = run_dir / "graph_working_dir"
    if graph_dir.exists():
        raise SystemExit("the graph working directory exists; a run starts clean")
    failures_log = run_dir / "child_failures.log"
    started = utc_now()
    base_url = args.base_url
    os.environ["OPENAI_BASE_URL"] = base_url  # anything that builds a client without being given the address
    os.environ["OPENAI_API_KEY"] = DUMMY_KEY

    import importlib.metadata as md

    import fast_graphrag
    from fast_graphrag import GraphRAG
    from fast_graphrag._llm import OpenAIEmbeddingService, OpenAILLMService
    from fast_graphrag._llm import _llm_openai as llm_module
    from fast_graphrag._llm._base import BaseLLMService
    from fast_graphrag._services._chunk_extraction import DefaultChunkingService
    from fast_graphrag._types import TDocument
    from fast_graphrag._utils import get_event_loop

    library_timeout = llm_module.TIMEOUT_SECONDS
    library_concurrency = BaseLLMService.__dataclass_fields__["max_requests_concurrent"].default
    applied_concurrency = args.llm_concurrency if args.llm_concurrency is not None else library_concurrency
    llm_module.TIMEOUT_SECONDS = float(args.llm_timeout_s)  # read when the client is built, just below
    llm = OpenAILLMService(model=args.model, base_url=base_url, api_key=DUMMY_KEY,
                           max_requests_concurrent=applied_concurrency)
    embedder = OpenAIEmbeddingService(model=args.embed_model, base_url=base_url, api_key=DUMMY_KEY,
                                      embedding_dim=args.embedding_dim)
    rag = GraphRAG(working_dir=str(graph_dir), domain=rehearsal.DOMAIN,
                   example_queries="\n".join(rehearsal.EXAMPLE_QUERIES), entity_types=rehearsal.ENTITY_TYPES,
                   config=GraphRAG.Config(llm_service=llm, embedding_service=embedder))
    cfg = rag.config
    result: dict = {
        "started_utc": started,
        "fast_graphrag_version": md.version("fast-graphrag"),
        "package_files_sha256": package_fingerprint(Path(fast_graphrag.__file__).resolve().parent),
        "defaults_seen": {
            "llm_class": type(cfg.llm_service).__name__, "llm_model": cfg.llm_service.model,
            "llm_max_requests_concurrent": cfg.llm_service.max_requests_concurrent,
            "llm_rate_limit_per_minute_enabled": cfg.llm_service.rate_limit_per_minute,
            "embedding_model": cfg.embedding_service.model, "embedding_dim": cfg.embedding_service.embedding_dim,
            "embedding_max_elements_per_request": cfg.embedding_service.max_elements_per_request,
            "embedding_max_requests_concurrent": cfg.embedding_service.max_requests_concurrent,
            "embedding_rate_limit_per_minute_enabled": cfg.embedding_service.rate_limit_per_minute,
            "max_gleaning_steps": rag.information_extraction_service.max_gleaning_steps,
            "chunk_token_size": rag.chunking_service.config.chunk_token_size,
            "chunk_token_overlap": rag.chunking_service.config.chunk_token_overlap,
            "chunk_size_chars": rag.chunking_service._chunk_size,
            "chunk_overlap_chars": rag.chunking_service._chunk_overlap,
            "max_node_description_size": cfg.node_upsert_policy.config.max_node_description_size,
            "edge_merge_threshold": cfg.edge_upsert_policy.config.edge_merge_threshold,
            "insert_similarity_score_threshold": rag.state_manager.insert_similarity_score_threshold,
        },
        "changed_from_library_defaults": {
            "llm_max_requests_concurrent": {"library": library_concurrency, "applied": applied_concurrency},
            "llm_timeout_s": {"library": library_timeout, "applied": float(args.llm_timeout_s)},
            "model_names": "the real names given on the command line instead of gpt-4o-mini / text-embedding-3-small",
            "embedding_dim": {"library": 1536, "applied": args.embedding_dim},
            "base_url_and_key": "the gateway's address and a dummy key, passed to both services",
        },
        "documents": [],
    }
    chunks_before = 0
    stopped_at = None
    wall0 = time.time()
    for i, doc in enumerate(docs, 1):
        # What the chunker will produce, measured with the library's own chunker on a copy (sizes only; no model call).
        probe = get_event_loop().run_until_complete(DefaultChunkingService().extract([TDocument(data=doc["body"], metadata={})]))
        chunk_lengths = [len(c.content) for c in list(probe)[0]]
        time.sleep(0.01)  # keeps the last call of the previous document and the first call of this one apart in time
        errors_before, retries_before = handler.error_total, handler.sdk_retries
        t_start = time.time()
        failure = None
        try:
            totals = rag.insert(doc["body"], show_progress=False)
        except Exception as exc:  # noqa: BLE001 - the failure is the result
            totals = (None, None, None)
            failure = failure_record(exc, failures_log, i)
        t_end = time.time()
        time.sleep(0.01)
        stored = None if failure else totals[2] - chunks_before
        dropped = failure is None and stored != len(chunk_lengths)
        if failure is None:
            chunks_before = totals[2]
        row = {"n": i, "rank": doc["rank"], "url_sha256_16": doc["url_sha256_16"], "chars": doc["chars"],
               "chunks_by_library_chunker": len(chunk_lengths),
               "chunk_chars_min": min(chunk_lengths), "chunk_chars_max": max(chunk_lengths),
               "graph_totals_after": {"entities": totals[0], "relations": totals[1], "chunks": totals[2]},
               "chunks_stored_for_this_document": stored,
               "seconds": round(t_end - t_start, 3), "t_start": t_start, "t_end": t_end,
               "error_log_lines_in_document": handler.error_total - errors_before,
               "sdk_retries_logged_in_document": handler.sdk_retries - retries_before,
               "indexed": failure is None and not dropped}
        if failure:
            row["insert_failed"] = failure
        elif dropped:
            row["silently_dropped"] = ("insert returned, but the number of chunks stored is not the number the library's "
                                       "chunker made for this document")
        result["documents"].append(row)
        print(f"document {i}/{len(docs)}: {'indexed' if row['indexed'] else 'NOT INDEXED'} in {row['seconds']} s, "
              f"{row['error_log_lines_in_document']} error log lines", file=sys.stderr, flush=True)
        write_json(Path(args.result), {**result, "complete": False})
        if not row["indexed"]:
            stopped_at = stopped_at or i
            if not args.continue_after_failure:
                break
            if failure:  # the graph's chunk count is unknown after an exception; re-read it for the next comparison
                try:
                    chunks_before = get_event_loop().run_until_complete(rag.state_manager.get_num_chunks())
                except Exception:  # noqa: BLE001 - keep the last known count; the next row then says what it saw
                    pass
    result["stopped_at_document"] = stopped_at
    result["wall_seconds_all_documents"] = round(time.time() - wall0, 3)
    result["finished_utc"] = utc_now()
    result["outbound_attempts"] = net_log
    result["openai_sdk_retries_logged"] = handler.sdk_retries
    result["tokenizer_failures_logged_by_library"] = handler.tokenizer_failures
    result["error_log_lines"] = {"count": handler.error_total, "by_head": dict(handler.error_heads)}
    result["environment_variable_names"] = sorted(os.environ)
    result["files_in_graph_dir"] = (
        sorted(p.relative_to(graph_dir).as_posix() for p in graph_dir.rglob("*") if p.is_file()) if graph_dir.exists() else [])
    write_json(Path(args.result), {**result, "complete": True})


# ---------------------------------------------------------------------------------------------------------------------
# Parent: gateway, probe, child, result
# ---------------------------------------------------------------------------------------------------------------------


def embedding_dimension(gateway_base_url: str, model: str) -> int:
    """One embeddings call through the gateway; the length of the vector it returns. The input is a fixed short string."""
    body = json.dumps({"model": model, "input": ["dimension probe"], "encoding_format": "float"}).encode("utf-8")
    req = urllib.request.Request(gateway_base_url + "/embeddings", data=body,
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {DUMMY_KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            obj = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        raise PassAError(f"embedding probe: HTTP {exc.code}: {exc.read()[:200].decode('utf-8', 'replace')}") from None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise PassAError(f"embedding probe: {type(exc).__name__}: {exc}") from None
    try:
        vec = obj["data"][0]["embedding"]
    except (KeyError, IndexError, TypeError):
        raise PassAError("embedding probe: the answer has no data[0].embedding") from None
    if not isinstance(vec, list) or not vec or not all(isinstance(x, (int, float)) for x in vec):
        raise PassAError("embedding probe: data[0].embedding is not a non-empty list of numbers")
    return len(vec)


def settle(log_path: Path, seconds: float = SETTLE_SECONDS) -> None:
    """Wait until the gateway's log has not grown for `seconds`: a request the client gave up on can still be answered."""
    def size() -> int:
        return log_path.stat().st_size if log_path.exists() else 0

    last, since = size(), time.time()
    while time.time() - since < seconds:
        time.sleep(0.25)
        now = size()
        if now != last:
            last, since = now, time.time()


def child_command(args: argparse.Namespace, base_url: str, dim: int, run_dir: Path, result: Path) -> list[str]:
    cmd = [sys.executable, str(Path(__file__).resolve()), "--child", "--base-url", base_url, "--embedding-dim", str(dim),
           "--model", args.model, "--embed-model", args.embed_model, "--n", str(max(args.checkpoint_list)),
           "--corpus", args.corpus, "--documents", args.documents, "--run-dir", str(run_dir), "--result", str(result),
           "--llm-timeout-s", str(args.llm_timeout_s)]
    if args.llm_concurrency is not None:
        cmd += ["--llm-concurrency", str(args.llm_concurrency)]
    if args.continue_after_failure:
        cmd.append("--continue-after-failure")
    return cmd


def last_exception_type(stderr_text: str) -> str | None:
    for line in reversed(stderr_text.splitlines()):
        m = re.match(r"^([A-Za-z_][\w.]*(?:Error|Exception|Exit|Interrupt))\b", line)
        if m:
            return m.group(1)
    return None


def build_output(args, docs, preflight_facts, dim, child, calls, before, per_doc, after, env_names, child_exit,
                 child_stderr, started, calls_sha) -> dict:
    rows = child.get("documents", []) if child else []
    n_done = len(rows)
    ordered = list(calls)
    # Every document row: the gateway's numbers for the calls that arrived during it, with the child's own numbers.
    per_document = []
    for k, row in enumerate(rows):
        w = window(per_doc[k])
        entry = {key: row[key] for key in ("n", "rank", "url_sha256_16", "chars", "chunks_by_library_chunker",
                                           "chunk_chars_min", "chunk_chars_max", "graph_totals_after",
                                           "chunks_stored_for_this_document", "seconds", "error_log_lines_in_document",
                                           "sdk_retries_logged_in_document", "indexed")}
        for key in ("insert_failed", "silently_dropped"):
            if key in row:
                entry[key] = row[key]
        entry.update(w)
        if args.profile is not None:
            entry["cost_usd"] = pb.cost_usd(per_doc[k])
        per_document.append(entry)
    checkpoints: dict = {}
    stop = child.get("stopped_at_document") if child else None
    marks = [m for m in args.checkpoint_list if m <= n_done]
    if n_done and n_done < max(args.checkpoint_list) and n_done not in marks:
        marks.append(n_done)  # the run ended early: what it had by then
    for m in marks:
        w = window([c for k in range(m) for c in per_doc[k]])
        w["documents_run"] = m
        if args.profile is not None:
            w["cost_usd"] = pb.cost_usd([c for k in range(m) for c in per_doc[k]])         # cumulative, documents 1..m
        w["documents_indexed"] = sum(1 for r in rows[:m] if r["indexed"])
        w["sdk_retries_logged"] = sum(r["sdk_retries_logged_in_document"] for r in rows[:m])
        w["graph_totals"] = rows[m - 1]["graph_totals_after"]
        w["extraction_calls_equal_chunker_count"] = (
            w["by_kind"].get("extract", {}).get("calls", 0) - w["by_kind"].get("extract", {}).get("retry_calls", 0)
            == sum(r["chunks_by_library_chunker"] for r in rows[:m]))
        if m not in args.checkpoint_list:
            w["stopped_here"] = True
        checkpoints[str(m)] = w
    failed_docs = [r["n"] for r in rows if not r["indexed"]]
    complete = bool(child) and child.get("complete") is True
    ok = complete and child_exit == 0 and n_done == len(docs) and not failed_docs
    builder_calls = [c for k in range(len(per_doc)) for c in per_doc[k]] + after
    warnings = []
    if any(c.get("usage_missing") for c in builder_calls):
        warnings.append("some calls have no usage in the provider's answer (usage_missing): their tokens are not measured")
    if any(c.get("voided") for c in builder_calls):
        warnings.append("some calls were voided (upstream error status, refused connection or timeout): see http_statuses")
    if any(c.get("refusal") for c in builder_calls):
        warnings.append("the gateway refused some calls (for example a model name it was not given): see http_statuses")
    if after:
        warnings.append(f"{len(after)} calls arrived after the last document ended and are in no checkpoint")
    if child and child.get("openai_sdk_retries_logged"):
        warnings.append("the OpenAI SDK retried requests (timeout, 429 or 5xx): a request it gave up on may have been "
                        "answered by the upstream after the gateway stopped; check the upstream is idle (ollama ps) and "
                        "compare `calls_in_log` with the upstream's own count")
    if child and child.get("tokenizer_failures_logged_by_library"):
        warnings.append("the library could not load a tokenizer for the model name; it falls back to a naive one "
                        "(no code in the package calls it on the indexing path: grep of the pinned source)")
    out = {
        "runner": RUNNER,
        "builder": "fast-graphrag",
        "version": (child or {}).get("fast_graphrag_version"),
        "package_files_sha256": (child or {}).get("package_files_sha256"),
        "upstream_url": args.upstream_url,
        "model": args.model,
        "embed_model": args.embed_model,
        "chat_request_defaults": chat_defaults(args),
        "embedding_dim": dim,
        "preflight": preflight_facts,
        "documents": {"count": len(docs), "source": "documents.tsv", "total_chars": sum(d["chars"] for d in docs)},
        "inputs_given_to_the_builder": {"domain": rehearsal.DOMAIN, "example_queries": rehearsal.EXAMPLE_QUERIES,
                                        "entity_types": rehearsal.ENTITY_TYPES},
        "builder_settings": {"defaults_seen": (child or {}).get("defaults_seen"),
                             "changed_from_library_defaults": (child or {}).get("changed_from_library_defaults")},
        "ok": ok,
        "stopped_at_document": stop,
        "documents_not_indexed": failed_docs,
        "child_exit_status": child_exit,
        "checkpoints": checkpoints,
        "per_document": per_document,
        "first_request_of_each_kind": first_request_of_each_kind(builder_calls),
        "gateway": {"calls_in_log": len(ordered), "calls_before_the_builder_started": len(before),
                    "calls_after_the_last_document": len(after),
                    "embedding_probe_calls": sum(1 for c in before if classify_call(c) == "embedding"),
                    "models_requested": dict(sorted(Counter(str(c.get("model_requested")) for c in ordered).items())),
                    "routes": dict(sorted(Counter(str(c.get("route")) for c in ordered).items()))},
        "calls_jsonl_sha256": calls_sha,
        "request_multiset_sha256": hashlib.sha256(
            "\n".join(sorted(str(c.get("request_sha256")) for c in builder_calls)).encode("utf-8")).hexdigest(),
        "wall_seconds_all_documents": (child or {}).get("wall_seconds_all_documents"),
        "outbound_attempts": (child or {}).get("outbound_attempts"),
        "openai_sdk_retries_logged": (child or {}).get("openai_sdk_retries_logged"),
        "tokenizer_failures_logged_by_library": (child or {}).get("tokenizer_failures_logged_by_library"),
        "error_log_lines": (child or {}).get("error_log_lines"),
        "environment_variable_names": (child or {}).get("environment_variable_names"),
        "minimal_environment_variable_names": env_names,
        "proxy_setting": rehearsal.PROXY_CLOSED,
        "warnings": warnings,
        "started_utc": started,
        "finished_utc": utc_now(),
    }
    if child is None or not complete:
        out["child_failed"] = {"exit_status": child_exit, "exception_type": last_exception_type(child_stderr),
                               "detail": "see child_stderr.log and child_failures.log in the workdir"}
    return out


def parse_checkpoints(text: str) -> list[int]:
    try:
        values = sorted({int(x) for x in text.split(",") if x.strip()})
    except ValueError:
        raise SystemExit(f"--checkpoints: not a list of integers: {text!r}") from None
    if not values or values[0] < 1:
        raise SystemExit("--checkpoints: positive integers, for example 1,5,20")
    return values


def run_parent(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    if not (repo_root / "tools" / "metering_gateway.py").is_file():
        raise SystemExit("--repo-root: tools/metering_gateway.py not found under it")
    workdir = Path(args.workdir).resolve()
    if workdir == repo_root or repo_root in workdir.parents:
        raise SystemExit("--workdir is inside the repository; the gateway's body log holds article text. Use a scratch path")
    if workdir.exists() and any(workdir.iterdir()):
        raise SystemExit("--workdir exists and is not empty; a run starts clean")
    if args.model == args.embed_model:
        raise SystemExit("--model and --embed-model must differ")
    args.checkpoint_list = parse_checkpoints(args.checkpoints)
    docs = rehearsal.load_documents(Path(args.corpus), Path(args.documents), max(args.checkpoint_list))  # fails early
    if len(docs) < max(args.checkpoint_list):
        raise SystemExit(f"--checkpoints asks for {max(args.checkpoint_list)} documents; documents.tsv has {len(docs)}")
    # The parent talks to loopback only; a proxy set in the caller's environment must not intervene.
    urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler({})))
    started = utc_now()

    preflight_facts = None
    if args.preflight_min_ctx or args.profile is not None:
        ollama_url = re.sub(r"/v1/?$", "", args.upstream_url.rstrip("/"))
        try:
            if args.profile is not None:   # the chat model is hosted: only the embedding model can be checked in Ollama
                preflight_facts = pb.embedding_preflight(args.upstream_url, args.embed_model)
            else:
                preflight_facts = preflight(ollama_url, args.model, min_ctx=args.preflight_min_ctx, embed_model=args.embed_model)
        except PassAError as exc:
            out = {"runner": RUNNER, "builder": "fast-graphrag", "upstream_url": args.upstream_url, "model": args.model,
                   "embed_model": args.embed_model, "ok": False, "preflight": {"refused": scrub(exc, 400)},
                   "started_utc": started, "finished_utc": utc_now()}
            write_json(Path(args.out), out)
            print(f"preflight refused: {scrub(exc, 400)}", file=sys.stderr)
            return 1

    workdir.mkdir(parents=True, exist_ok=True)
    run_dir = workdir / "child"
    run_dir.mkdir()
    result_path = run_dir / "child_result.json"
    gw = pb.make_gateway(args.profile, workdir / "gateway", args.upstream_url, [args.model, args.embed_model], repo_root,
                         request_defaults={args.model: chat_defaults(args)})
    child_exit, child_stderr, child, dim, t_spawn, setup_error = None, "", None, None, time.time(), None
    env = rehearsal.minimal_env(run_dir, args.tiktoken_cache)
    try:
        gw.start()
        print(f"gateway at {gw.base_url}; upstream {args.upstream_url}", file=sys.stderr)
        dim = embedding_dimension(gw.base_url, args.embed_model)
        print(f"embedding length {dim} (one call through the gateway)", file=sys.stderr)
        env["OPENAI_BASE_URL"] = gw.base_url
        t_spawn = time.time()
        with open(run_dir / "child_stdout.log", "w", encoding="utf-8") as out_fh, \
                open(run_dir / "child_stderr.log", "w", encoding="utf-8") as err_fh:
            proc = subprocess.run(child_command(args, gw.base_url, dim, run_dir, result_path), env=env, cwd=str(run_dir),
                                  stdout=out_fh, stderr=err_fh, text=True)
        child_exit = proc.returncode
        child_stderr = (run_dir / "child_stderr.log").read_text(encoding="utf-8", errors="replace")
        if result_path.exists():
            child = json.loads(result_path.read_text(encoding="utf-8"))
        # A request the client gave up on (timeout, then retry) can still be answered by the upstream later.
        gave_up = bool(child and child.get("openai_sdk_retries_logged"))
        settle(gw.log_path, LONG_SETTLE_SECONDS if gave_up else SETTLE_SECONDS)
    except PassAError as exc:  # the gateway did not start, or the embedding probe failed: nothing was indexed
        setup_error = scrub(exc, 400)
    finally:
        gw.stop()

    calls = gw.calls()
    ends = [r["t_end"] for r in (child or {}).get("documents", [])]
    before, per_doc, after = attribute(calls, t_spawn, ends)
    calls_sha = hashlib.sha256(gw.log_path.read_bytes()).hexdigest() if gw.log_path.exists() else None
    with open(workdir / "calls_without_text.jsonl", "w", encoding="utf-8") as fh:
        doc_of = {id(c): k + 1 for k in range(len(per_doc)) for c in per_doc[k]}
        for seq, c in enumerate(calls, 1):
            fh.write(json.dumps({"seq": seq, "ts": c.get("ts"), "document": doc_of.get(id(c)), "kind": classify_call(c),
                                 "retry": is_retry_call(c), "route": c.get("route"), "model": c.get("model_requested"),
                                 "http_status": c.get("http_status"), "input_tokens": c.get("input_tokens"),
                                 "output_tokens": c.get("output_tokens"), "latency_ms": c.get("latency_ms"),
                                 "request_sha256": c.get("request_sha256"), "voided": c.get("voided"),
                                 "usage_missing": c.get("usage_missing"), "refusal": c.get("refusal"),
                                 "error": c.get("error"),
                                 **({"cost": c.get("cost")} if args.profile is not None else {})}) + "\n")
    out = build_output(args, docs, preflight_facts, dim, child, calls, before, per_doc, after, sorted(env), child_exit,
                       child_stderr, started, calls_sha)
    if args.profile is not None:
        out["hosted"] = pb.hosted_block_for(gw)
    if setup_error:
        out["ok"] = False
        out["setup_failed"] = setup_error
        out.pop("child_failed", None)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    write_json(Path(args.out), out)
    print(f"wrote the result; ok={out['ok']}", file=sys.stderr)
    return 0 if out["ok"] else 1


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--documents", required=True)
    ap.add_argument("--repo-root")
    ap.add_argument("--upstream-url")
    ap.add_argument("--model", required=True)
    ap.add_argument("--embed-model", required=True)
    add_chat_default_argument(ap)
    pb.add_hosted_argument(ap)
    ap.add_argument("--workdir")
    ap.add_argument("--out")
    ap.add_argument("--checkpoints", default="1,5,20")
    ap.add_argument("--tiktoken-cache")
    ap.add_argument("--preflight-min-ctx", type=int, default=0,
                    help="ask the Ollama behind --upstream-url (native API, same host) for the model's Modelfile and refuse "
                         "unless its num_ctx is explicitly at least this (use 16384 against Ollama; 0 skips, for the stub)")
    ap.add_argument("--llm-concurrency", type=int, default=None,
                    help="chat requests in flight at once (default: the library's own, 1024; see the docstring before setting it)")
    ap.add_argument("--llm-timeout-s", type=float, default=1800.0,
                    help="the OpenAI client's timeout per chat request, queue time included (the library's own is 180)")
    ap.add_argument("--continue-after-failure", action="store_true",
                    help="keep indexing after a document that was not indexed (default: stop at the first)")
    ap.add_argument("--child", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--base-url", help=argparse.SUPPRESS)
    ap.add_argument("--embedding-dim", type=int, help=argparse.SUPPRESS)
    ap.add_argument("--n", type=int, help=argparse.SUPPRESS)
    ap.add_argument("--run-dir", help=argparse.SUPPRESS)
    ap.add_argument("--result", help=argparse.SUPPRESS)
    args = ap.parse_args()
    if (args.llm_concurrency is not None and args.llm_concurrency < 1) or args.llm_timeout_s <= 0:
        ap.error("--llm-concurrency must be at least 1 and --llm-timeout-s positive")
    args.profile = None   # the child is given no profile: it only ever sees the gateway's address and a dummy key
    if args.child:
        run_child(args)
        return
    missing = [name for name in ("repo_root", "upstream_url", "workdir", "out") if not getattr(args, name)]
    if missing:
        ap.error("required: " + ", ".join("--" + m.replace("_", "-") for m in missing))
    try:
        args.profile = pb.profile_from_args(args)
    except PassAError as exc:
        ap.error(str(exc))
    if args.profile is not None and args.preflight_min_ctx:
        ap.error("--preflight-min-ctx checks the chat model in Ollama, and with --hosted-profile the chat model is hosted "
                 "(only the embedding model is checked)")
    try:
        code = run_parent(args)
    except PassAError as exc:
        print(f"failed: {exc}", file=sys.stderr)
        code = 1
    sys.exit(code)


if __name__ == "__main__":
    main()
