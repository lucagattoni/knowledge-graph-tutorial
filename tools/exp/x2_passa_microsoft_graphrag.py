"""X2 pass A: Microsoft GraphRAG's indexing, answered by a model behind the metering gateway.

The stub rehearsal (`x2_microsoft_graphrag.py`) counted what GraphRAG sends to a stub. This runner sends the same calls
through the metering gateway (`tools/metering_gateway.py`) to an upstream chosen on the command line: the stub (to prove
the plumbing, free) or a local Ollama (a real model). It does not change between the two.

Run it with the Python of the environment GraphRAG was installed into (it reads the installed package):

    ENV=$SCRATCH/microsoft-graphrag
    env -i PATH=/usr/bin:/bin:/opt/homebrew/bin HOME=$SCRATCH/passa-microsoft-graphrag/home \\
        $ENV/venv/bin/python -I tools/exp/x2_passa_microsoft_graphrag.py \\
        --corpus $SCRATCH/exp-data/corpus.json --documents kb-kg/experiments/x2-index-cost/documents.tsv \\
        --repo-root . --upstream-url http://127.0.0.1:11434/v1 --model MY-CHAT-16K --embed-model MY-EMBEDDING \\
        --workdir $SCRATCH/passa-microsoft-graphrag/run1 --out $SCRATCH/passa-microsoft-graphrag/run1.json \\
        --checkpoints 1,5,20 --tiktoken-cache $ENV/tiktoken_cache

What it does.
1. If the upstream answers Ollama's `/api/version`, it runs `passa_common.preflight` (the model exists and its context is
   explicitly at least 16,384); a refusal is recorded and ends the run with status 1. Any other upstream (the stub): skipped.
2. It starts `LocalGateway` (workdir/gateway) in front of the upstream, with exactly two model names: `--model` and
   `--embed-model`. The gateway refuses any other name, so a builder that sent a different name fails at once.
3. It makes one embeddings call through the gateway and reads the vector length; that length, not a constant, goes into the
   project's `vector_store.vector_size`. This call is logged by the gateway but belongs to no checkpoint.
4. For each checkpoint N it writes the first N documents of `documents.tsv` into a fresh GraphRAG project (the settings that
   `graphrag init` writes, plus the gateway address, the two model names, the vector size) and runs `graphrag index` as a
   child process. GraphRAG indexes in batch, so every checkpoint is a separate run from clean directories (its own
   preflight calls, an empty LLM cache); nothing carries over from the smaller checkpoint.
5. From the gateway's log it records, per checkpoint: calls by kind, HTTP statuses, the provider's own input and output
   tokens, summed latency, identical repeated requests (retries show as repeats), and the sizes of GraphRAG's output tables.

Safety, unchanged from the rehearsal: the child gets a minimal environment, a dummy key, an HTTP(S)_PROXY that refuses
connections with loopback excluded, and on macOS a `sandbox-exec` profile that denies every outbound connection except to
loopback (the gateway and the upstream are on 127.0.0.1). The article text goes only into files under --workdir (the project
input, the gateway's body log, GraphRAG's logs); the JSON written to --out holds counts, sizes and hashes, never text.

Pass B (`--hosted-profile PROFILE_JSON`, see `passb_common.py` and `passb_profile.example.json`). The CHAT model (`--model`) is
served by a hosted provider through the same gateway, which holds the key (it reads the file the profile names; neither this
program nor GraphRAG ever does) and refuses past the cap; `--upstream-url` and `--embed-model` stay the LOCAL embedding upstream,
and only the embedding model is checked in Ollama. The JSON gains a `hosted` block (cost, prices with their source, the model
name as the provider reports it, the shared ledger's size before the run; never the key file's path or the ledger's) and, on
every checkpoint, `cost_usd` (that checkpoint's own run) and `cost_usd_cumulative_in_this_run` (everything this run has spent so
far, the dimension probe and the smaller checkpoints included). The gateway log is the profile's shared ledger and `gw.calls()`
returns only this run's records. The gateway's own timeout is the profile's, not `--upstream-timeout-s`. Without the option
nothing in this program changes.

Optional knobs for a slow local model (each defaults to the builder's own default, so the counts stay comparable with the
rehearsal): --concurrency (GraphRAG `concurrent_requests`, 25), --request-timeout-s (the client's per-request timeout, set
as `call_args.timeout` on both models), --child-timeout-s (limit for one `graphrag index` run), --upstream-timeout-s (the
gateway's per-socket-operation timeout towards the upstream). Their values are recorded in the JSON.

Exit status: 0 if every checkpoint indexed all its documents; 1 if a builder or preflight failure was recorded (the JSON
says which); 2 for a usage problem before anything ran. A failed checkpoint stops the run (larger ones would only cost more).

Not tested: a real model. Until a local model is run through it, only the stub has been the upstream.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from types import SimpleNamespace

sys.dont_write_bytecode = True  # keep the repository free of .pyc files
sys.path.insert(0, str(Path(__file__).resolve().parent))

import passa_common  # noqa: E402
import passb_common as pb  # noqa: E402
import x2_microsoft_graphrag as rehearsal  # noqa: E402  the stub rehearsal's classifier, loader and table reader
from stub_llm import message_text  # noqa: E402

RUNNER = "tools/exp/x2_passa_microsoft_graphrag.py"
MIN_CTX = 16384  # passa_common.preflight refuses a local model whose explicit context is below this
PROBE_TEXT = "embedding dimension probe"

# strings GraphRAG 3.3.0 logs when a piece of work is lost or altered (graphrag/index/..., read from the installed package);
# only counts go into the JSON, never the lines: some carry text from a chunk or from the model.
FAILURE_MARKERS = {
    "chunk_extraction_errors": "error extracting graph",
    "extraction_or_summary_on_error_callbacks": "Entity Extraction Error",
    "graph_extraction_failed_no_entities_or_relationships": "Graph Extraction failed",
    "community_report_errors": "Community Report Extraction Error",
    "community_report_exceptions": "error generating community report",
    "community_processing_errors": "Error processing community",
    "communities_without_a_report": "No report found for community",
    "relationships_dropped_for_missing_entities": "referencing non-existent entities",
    "embeddings_skipped_for_none": "rows with None embeddings",
    "vector_size_overridden_by_graphrag": "Overriding vector_size",
}


# ---- reading the gateway's records -----------------------------------------------------------------------------------
def as_stub_call(c: dict) -> SimpleNamespace:
    """The gateway's record of one call, in the shape the rehearsal's classifier reads (path, messages, prompt_text).

    Built as `stub_llm.Stub._record` builds it, from the request body the gateway logged, so the same text is classified.
    """
    body = c.get("request")
    body = body if isinstance(body, dict) else {}
    messages = body.get("messages") or []
    raw_in = body.get("input")
    if raw_in is None:
        inputs: list = []
    elif isinstance(raw_in, list):
        inputs = [x if isinstance(x, str) else json.dumps(x) for x in raw_in]
    else:
        inputs = [raw_in if isinstance(raw_in, str) else json.dumps(raw_in)]
    text = "\n".join(message_text(m) for m in messages) if messages else "\n".join(inputs)
    return SimpleNamespace(path=str(c.get("route") or ""), messages=messages, inputs=inputs, prompt_text=text)


def make_classifier(builder_classifier: "rehearsal.Classifier"):
    def classify(c: dict) -> str:
        if not isinstance(c.get("request"), dict):
            return "no_body"
        return builder_classifier.kind(as_stub_call(c))

    return classify


def prompt_sha256(c: dict) -> str:
    return hashlib.sha256(as_stub_call(c).prompt_text.encode("utf-8")).hexdigest()


def multiset_sha256(calls: list[dict], classify) -> str:
    """The rehearsal's `call_multiset_sha256`: kind, prompt tokens and prompt hash of every call, sorted. Here the prompt
    tokens are the provider's usage as the gateway logged it, so it equals the rehearsal's value only when the upstream is
    the stub with the same responder (the stub's usage is its own count)."""
    return hashlib.sha256("\n".join(sorted(
        f"{classify(c)}|{c.get('input_tokens')}|{prompt_sha256(c)}" for c in calls)).encode()).hexdigest()


def summarise_calls(calls: list[dict], classify, tables: dict) -> dict:
    gw = passa_common.summarize(calls, classify)  # by kind: calls, ok, input_tokens, output_tokens, latency_ms; and a total
    by_kind: dict[str, dict] = {}
    groups: dict[str, list[dict]] = collections.defaultdict(list)
    for c in calls:
        groups[classify(c)].append(c)
    for kind, cs in sorted(groups.items()):
        entry = {
            **gw["by_kind"][kind],
            "statuses": dict(collections.Counter(str(c.get("http_status")) for c in cs)),
            "input_tokens_stats": rehearsal.stats_of([c.get("input_tokens") or 0 for c in cs]),
            "voided": sum(1 for c in cs if c.get("voided")),
            "usage_missing": sum(1 for c in cs if c.get("usage_missing")),
        }
        if kind in ("embedding", "preflight_embedding_test"):
            entry["inputs"] = sum(len(as_stub_call(c).inputs) for c in cs)
            entry["max_inputs_in_one_call"] = max(len(as_stub_call(c).inputs) for c in cs)
        by_kind[kind] = entry

    chat = [c for c in calls if str(c.get("route", "")).endswith("/chat/completions")]
    emb = [c for c in calls if str(c.get("route", "")).endswith("/embeddings")]
    totals = {
        "chat_calls": len(chat),
        "chat_input_tokens": sum(c.get("input_tokens") or 0 for c in chat),
        "chat_output_tokens": sum(c.get("output_tokens") or 0 for c in chat),
        "embedding_calls": len(emb),
        "embedding_inputs": sum(len(as_stub_call(c).inputs) for c in emb),
        "embedding_input_tokens": sum(c.get("input_tokens") or 0 for c in emb),
        "other_calls": len(calls) - len(chat) - len(emb),
        "latency_ms_sum": sum(c.get("latency_ms") or 0 for c in calls),
        "latency_note": "summed over calls that run concurrently, so it is not wall time",
    }

    # Repeats: the same request body (by the gateway's SHA-256) seen more than once. A client retry after a timeout or an
    # error shows as a repeat; so would a duplicate the builder chose to send. The statuses say which.
    seen = collections.Counter(c.get("request_sha256") for c in calls)
    repeats = sum(n - 1 for n in seen.values() if n > 1)
    not_ok = [c for c in calls if c.get("http_status") != 200 or c.get("voided")]
    retries = {
        "distinct_requests": len(seen),
        "identical_repeated_requests": repeats,
        "calls_not_200_or_voided": len(not_ok),
        "statuses": dict(collections.Counter(str(c.get("http_status")) for c in calls)),
        "gateway_refusals": dict(collections.Counter(c["refusal"] for c in calls if c.get("refusal"))),
    }

    # Which field an embedding call belongs to: fields are embedded one after another, so cumulative inputs in arrival
    # order cut at the field boundaries; a boundary inside a call (or an extra call from a retry) shows as a mismatch.
    emb_in_order = [c for c in calls if classify(c) == "embedding"]
    split: dict[str, dict] = {}
    idx, ok = 0, True
    for name, key in (("entity_description", "entities"), ("community_full_content", "community_reports"),
                      ("text_unit_text", "text_units")):
        rows = tables.get(key)
        if rows is None:
            split[name] = {"calls": 0, "inputs": 0, "input_tokens": 0, "note": "table not written"}
            continue
        cs, got = [], 0
        while idx < len(emb_in_order) and got < rows:
            cs.append(emb_in_order[idx])
            got += len(as_stub_call(emb_in_order[idx]).inputs)
            idx += 1
        ok = ok and got == rows
        split[name] = {"calls": len(cs), "inputs": got, "rows_in_table": rows,
                       "input_tokens": sum(c.get("input_tokens") or 0 for c in cs)}
    ok = ok and idx == len(emb_in_order)
    return {
        "gateway_summary": totals, "by_kind": by_kind, "gateway_total": gw["total"], "retries": retries,
        "embedding_by_field": split,
        "embedding_split_matches_tables": (ok if emb_in_order else None),
        "unclassified_chat_calls": len(groups.get("other", [])) + len(groups.get("no_body", [])),
        "call_multiset_sha256": multiset_sha256(calls, classify),
    }


def call_rows(checkpoint: int, calls: list[dict], classify, *, cost: bool = False) -> list[dict]:
    """One line per call for calls.jsonl: no text, only what the gateway logged and the kind (and, in pass B, the cost)."""
    rows = []
    for i, c in enumerate(calls):
        rows.append({
            "checkpoint": checkpoint, "i": i, "kind": classify(c), "route": c.get("route"),
            "model_requested": c.get("model_requested"), "model_reported": c.get("model_reported"),
            "http_status": c.get("http_status"), "input_tokens": c.get("input_tokens"),
            "output_tokens": c.get("output_tokens"), "cached_input_tokens": c.get("cached_input_tokens"),
            "latency_ms": c.get("latency_ms"), "request_sha256": c.get("request_sha256"),
            "n_inputs": len(as_stub_call(c).inputs) if str(c.get("route", "")).endswith("/embeddings") else None,
            "voided": c.get("voided"), "usage_missing": c.get("usage_missing"), "streamed": c.get("streamed"),
            "refusal": c.get("refusal"), "error": c.get("error"),
            **({"cost": c.get("cost")} if cost else {}),
        })
    return rows


# ---- the upstream ----------------------------------------------------------------------------------------------------
def upstream_root(upstream_url: str) -> str:
    return re.sub(r"/v1/?$", "", upstream_url.rstrip("/"))


def maybe_ollama_preflight(upstream_url: str, model: str, embed_model: str) -> dict:
    """Ollama's own checks when the upstream is Ollama; a recorded skip when it is anything else (the stub)."""
    root = upstream_root(upstream_url)
    try:
        with urllib.request.urlopen(f"{root}/api/version", timeout=10) as resp:
            version = json.loads(resp.read()).get("version")
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        return {"skipped": f"no Ollama answer at /api/version ({type(exc).__name__}); the upstream is not Ollama or is down"}
    if not version:
        return {"skipped": "/api/version answered without a version; not treated as Ollama"}
    try:
        return {"ran": True, **passa_common.preflight(root, model, min_ctx=MIN_CTX, embed_model=embed_model)}
    except passa_common.PassAError as exc:
        return {"ran": True, "error": str(exc)}


def probe_embedding_dimension(gateway_base_url: str, embed_model: str) -> int:
    """One embeddings call through the gateway; the length of the vector it returns."""
    payload = json.dumps({"model": embed_model, "input": [PROBE_TEXT]}).encode("utf-8")
    req = urllib.request.Request(f"{gateway_base_url}/embeddings", data=payload,
                                 headers={"Content-Type": "application/json", "Authorization": "Bearer dummy-not-a-key"})
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            body = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        raise passa_common.PassAError(f"embedding probe: HTTP {exc.code} from the gateway: {exc.read()[:300]!r}") from None
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        raise passa_common.PassAError(f"embedding probe failed: {type(exc).__name__}: {exc}") from None
    try:
        dim = len(body["data"][0]["embedding"])
    except (KeyError, IndexError, TypeError):
        raise passa_common.PassAError("embedding probe: the answer has no data[0].embedding") from None
    if dim <= 0:
        raise passa_common.PassAError("embedding probe: an empty vector")
    return dim


# ---- one GraphRAG project --------------------------------------------------------------------------------------------
def make_project(run_dir: Path, template: Path, gateway_url: str, docs: list[dict], *, model: str, embed_model: str,
                 dim: int, concurrency: int | None, request_timeout_s: float | None) -> None:
    if run_dir.exists():
        raise SystemExit(f"{run_dir.name} exists; the work directory must be new")
    run_dir.mkdir(parents=True)
    (run_dir / ".x2-run").write_text("made by x2_passa_microsoft_graphrag.py\n")
    shutil.copytree(template / "prompts", run_dir / "prompts")
    text = (template / "settings.yaml").read_text(encoding="utf-8")

    def replace(pattern: str, fn, expected: int) -> None:
        nonlocal text
        text, n = re.subn(pattern, fn, text, flags=re.M)
        if n != expected:
            raise SystemExit(f"settings template: {pattern!r} matched {n} times, expected {expected}")

    timeout_lines = (lambda ind: f"{ind}call_args:\n{ind}  timeout: {request_timeout_s}\n") if request_timeout_s else (lambda ind: "")
    replace(r"^(\s*)model_provider: openai\n", lambda m: m.group(0) + f"{m.group(1)}api_base: {gateway_url}\n", 2)
    replace(r"^(\s*)model: gpt-4\.1\n", lambda m: f"{m.group(1)}model: {json.dumps(model)}\n" + timeout_lines(m.group(1)), 1)
    replace(r"^(\s*)model: text-embedding-3-large\n",
            lambda m: f"{m.group(1)}model: {json.dumps(embed_model)}\n" + timeout_lines(m.group(1)), 1)
    replace(r"^(\s*)db_uri: output/lancedb\n", lambda m: m.group(0) + f"{m.group(1)}vector_size: {dim}\n", 1)
    if concurrency is not None:
        if re.search(r"^concurrent_requests:", text, flags=re.M):
            raise SystemExit("settings template already sets concurrent_requests")
        text += f"\nconcurrent_requests: {concurrency}\n"
    (run_dir / "settings.yaml").write_text(text, encoding="utf-8")
    (run_dir / "input").mkdir()
    for d in docs:
        (run_dir / "input" / f"{d['rank']:02d}.txt").write_text(d["body"], encoding="utf-8")


def count_markers(log_text: str) -> dict:
    return {name: len(re.findall(re.escape(s), log_text)) for name, s in FAILURE_MARKERS.items()}


def run_checkpoint(n: int, args, dim: int, docs, template, gw, classify, scrub) -> tuple[dict, list[dict]]:
    run_dir = args.workdir / "runs" / f"n{n}"
    make_project(run_dir, template, gw.base_url, docs[:n], model=args.model, embed_model=args.embed_model, dim=dim,
                 concurrency=args.concurrency, request_timeout_s=args.request_timeout_s)
    before = len(gw.calls())
    started = datetime.now(timezone.utc).strftime("%Y%m%d %H:%M UTC")
    t0 = time.time()
    timed_out = False
    try:
        with (run_dir / "run.log").open("wb") as log:
            proc = subprocess.run(rehearsal.wrap([str(args.graphrag), "index", "--root", str(run_dir)], args.sandbox),
                                  env=rehearsal.child_env(args.workdir / "home", args.tiktoken_cache, rehearsal.BLOCKING_PROXY),
                                  stdout=log, stderr=subprocess.STDOUT, timeout=args.child_timeout_s)
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        timed_out, exit_code = True, None
    wall = time.time() - t0
    calls = gw.calls()[before:]
    tables = rehearsal.read_tables(run_dir)
    result = summarise_calls(calls, classify, tables)
    if args.profile is not None:
        result["cost_usd"] = pb.cost_usd(calls)                                    # this checkpoint's own run
        result["cost_usd_cumulative_in_this_run"] = pb.cost_usd(gw.calls())        # the probe and the smaller checkpoints too
    log_files = [run_dir / "run.log", run_dir / "logs" / "indexing-engine.log"]
    log_text = "\n".join(p.read_text(errors="replace") for p in log_files if p.exists())
    markers = count_markers(log_text)
    documents_indexed = tables.get("documents")
    indexed_all = bool(exit_code == 0 and documents_indexed == n and markers["chunk_extraction_errors"] == 0
                       and markers["graph_extraction_failed_no_entities_or_relationships"] == 0)
    result.update({
        "documents": n, "started": started, "wall_seconds": round(wall, 1),
        "command": "graphrag index --root <fresh project directory>",
        "exit_code": exit_code, "timed_out": timed_out, "child_timeout_s": args.child_timeout_s,
        "documents_indexed": documents_indexed, "indexed_all_documents": indexed_all,
        "output_tables": tables, "failure_markers_in_logs": markers,
        # Which calls are per chunk and which are corpus-level (run once over the merged graph of all N documents). Kept
        # from the rehearsal: description summaries and community reports are corpus-level, not per document.
        "scope_of_kinds": {
            "preflight_connectivity_test": "once per run", "preflight_embedding_test": "once per run",
            "extract_graph": "per chunk", "extract_gleaning_continue": "per chunk",
            "extract_gleaning_loop_check": "per chunk (none at the default of one gleaning)",
            "summarize_description_entity": "corpus-level (one per entity seen with 2 or more distinct descriptions)",
            "summarize_description_relationship": "corpus-level (one per relationship seen with 2 or more distinct descriptions)",
            "community_report": "corpus-level (one per community, every level, of the merged graph)",
            "embedding": "per field: chunk text per chunk; entity descriptions and community reports corpus-level",
        },
    })
    if exit_code != 0:
        lines = [ln.strip() for ln in log_text.splitlines() if ln.strip()]
        picked = [ln for ln in lines if re.search(r"Failed to validate|Traceback|Error", ln)][:3] + lines[-2:]
        result["run_log_excerpt_scrubbed"] = [scrub(ln[:200]) for ln in picked]
        result["run_log_excerpt_note"] = "may hold model output; read before publishing"
    return result, call_rows(n, calls, classify, cost=args.profile is not None)


# ---- main ------------------------------------------------------------------------------------------------------------
def parse_args(argv=None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--corpus", type=Path, required=True)
    ap.add_argument("--documents", type=Path, required=True)
    ap.add_argument("--repo-root", type=Path, required=True, help="the repository root (the gateway is tools/metering_gateway.py)")
    ap.add_argument("--upstream-url", required=True, help="OpenAI-compatible base URL on loopback, e.g. http://127.0.0.1:11434/v1")
    ap.add_argument("--model", required=True, help="chat model name, sent verbatim")
    ap.add_argument("--embed-model", required=True, help="embedding model name, sent verbatim")
    passa_common.add_chat_default_argument(ap)
    pb.add_hosted_argument(ap)
    ap.add_argument("--workdir", type=Path, required=True, help="a new, empty scratch directory (not in the repository)")
    ap.add_argument("--out", type=Path, required=True, help="result JSON; must not exist")
    ap.add_argument("--checkpoints", default="1,5,20", help="comma-separated document counts, ascending, at most 20")
    ap.add_argument("--tiktoken-cache", type=Path, default=None,
                    help="tiktoken table cache for the child (default: $TIKTOKEN_CACHE_DIR); the sandbox allows no download")
    ap.add_argument("--no-sandbox", dest="sandbox", action="store_false", help="do not wrap the child in sandbox-exec")
    # optional knobs for a slow local model; each defaults to the builder's own default so the counts stay comparable
    ap.add_argument("--concurrency", type=int, default=None, help="GraphRAG concurrent_requests (builder default: 25)")
    ap.add_argument("--request-timeout-s", type=float, default=None,
                    help="per-request timeout the builder's client uses (builder default: litellm's 6000 s)")
    ap.add_argument("--child-timeout-s", type=int, default=6 * 3600, help="limit for one `graphrag index` run")
    ap.add_argument("--upstream-timeout-s", type=int, default=1800, help="the gateway's per-socket-operation timeout towards the upstream")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    for p in (args.corpus, args.documents):
        if not p.is_file():
            print(f"not a file: {p.name}", file=sys.stderr)
            return 2
    if not (args.repo_root / "tools" / "metering_gateway.py").is_file():
        print("--repo-root does not hold tools/metering_gateway.py", file=sys.stderr)
        return 2
    if args.out.exists():
        print(f"{args.out.name} exists; give a new --out path", file=sys.stderr)
        return 2
    args.workdir = args.workdir.resolve()
    if args.workdir.exists() and any(args.workdir.iterdir()):
        print("--workdir is not empty; give a new, empty directory", file=sys.stderr)
        return 2
    try:
        checkpoints = [int(x) for x in args.checkpoints.split(",")]
    except ValueError:
        print("--checkpoints: comma-separated integers", file=sys.stderr)
        return 2
    if not checkpoints or checkpoints != sorted(set(checkpoints)) or checkpoints[0] < 1 or checkpoints[-1] > 20:
        print("--checkpoints: ascending, unique, between 1 and 20", file=sys.stderr)
        return 2
    if args.model == args.embed_model:
        print("--model and --embed-model must differ", file=sys.stderr)
        return 2
    try:
        args.profile = pb.profile_from_args(args)
    except passa_common.PassAError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    cache = args.tiktoken_cache or (Path(os.environ["TIKTOKEN_CACHE_DIR"]) if "TIKTOKEN_CACHE_DIR" in os.environ else None)
    if cache is None or not cache.is_dir():
        print("give --tiktoken-cache (or set TIKTOKEN_CACHE_DIR): the sandboxed child cannot download its tokenizer tables", file=sys.stderr)
        return 2
    args.tiktoken_cache = cache.resolve()
    args.graphrag = Path(sys.executable).parent / "graphrag"
    if not args.graphrag.exists():
        print("run this with the Python of the environment GraphRAG is installed in", file=sys.stderr)
        return 2
    if args.sandbox and not (sys.platform == "darwin" and Path("/usr/bin/sandbox-exec").exists()):
        print("no sandbox-exec here; the child would run without the network block. Pass --no-sandbox to accept that.", file=sys.stderr)
        return 2
    repo_root = args.repo_root.resolve()

    def scrub(text: str) -> str:
        """No absolute local path may reach the JSON."""
        for real, label in ((str(args.workdir), "<workdir>"), (str(repo_root), "<repo>"), (str(Path.home()), "<home>"),
                            (str(Path(sys.prefix).resolve()), "<venv>"), (str(args.tiktoken_cache), "<tiktoken-cache>")):
            text = text.replace(real, label)
        return text if args.profile is None else args.profile.redact(text)

    docs = rehearsal.load_documents(args.corpus, args.documents)
    if len(docs) != 20:
        print(f"expected 20 documents, found {len(docs)}", file=sys.stderr)
        return 2
    args.workdir.mkdir(parents=True, exist_ok=True)
    (args.workdir / "home").mkdir(exist_ok=True)
    classify = make_classifier(rehearsal.Classifier())

    started_utc = datetime.now(timezone.utc).strftime("%Y%m%d %H:%M UTC")
    result: dict = {
        "runner": RUNNER, "builder": "microsoft/graphrag", "version": metadata.version("graphrag"),
        "upstream_url": args.upstream_url, "model": args.model, "embed_model": args.embed_model,
        "chat_request_defaults": passa_common.chat_defaults(args),
        "embedding_dim": None, "preflight": None,
        "graphrag_versions": {d: metadata.version(d) for d in (
            "graphrag", "graphrag-llm", "graphrag-chunking", "graphrag-cache", "graphrag-storage", "graphrag-vectors",
            "graphrag-input", "graphrag-common", "litellm", "openai", "tiktoken", "lancedb", "pandas", "numpy")},
        "python": platform.python_version(), "machine": platform.machine(), "system": platform.system(),
        "method": "standard (the default of `graphrag index`)",
        "settings": "the file `graphrag init --model gpt-4.1 --embedding text-embedding-3-large` writes, with: api_base "
                    "for both models (the gateway), the two model names given on the command line, "
                    "vector_store.vector_size read from a probe call",
        "settings_overrides": {"concurrency": args.concurrency, "request_timeout_s": args.request_timeout_s,
                               "note": "null means the builder's default"},
        "document_input": "the `body` of each article, one .txt file each, in documents.tsv order, first N",
        "checkpoint_semantics": "each checkpoint is a separate batch run from clean directories and an empty LLM cache, "
                                "with its own preflight calls; nothing carries over from a smaller checkpoint",
        "child_isolation": {
            "env": "env whitelist: PATH, HOME (a scratch dir), a dummy GRAPHRAG_API_KEY, proxy variables, TIKTOKEN_CACHE_DIR",
            "proxy": rehearsal.BLOCKING_PROXY + " (refuses connections), NO_PROXY=127.0.0.1,localhost",
            "os_level_network_block": ("sandbox-exec profile: deny every outbound connection except to loopback"
                                       if args.sandbox else "none (--no-sandbox or not macOS)"),
        },
        "dimension_probe": None, "checkpoints": {}, "calls_jsonl_sha256": None,
        "started_utc": started_utc, "finished_utc": None, "status": "running",
    }

    holder: dict = {}   # the hosted gateway, once it exists, so every write of the result carries its block

    def write_result() -> None:
        if args.profile is not None and holder.get("gateway") is not None:
            result["hosted"] = pb.hosted_block_for(holder["gateway"])
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    def finish(status: str, code: int) -> int:
        result["status"] = status
        result["finished_utc"] = datetime.now(timezone.utc).strftime("%Y%m%d %H:%M UTC")
        write_result()
        return code

    if args.sandbox:
        st = rehearsal.sandbox_selftest()
        result["child_isolation"]["sandbox_selftest"] = st
        if not (st["blocks_non_loopback"] and st["allows_loopback"]):
            print("the sandbox profile does not behave as intended", file=sys.stderr)
            return finish("sandbox self-test failed", 1)

    if args.profile is not None:     # the chat model is hosted: only the embedding model can be checked in Ollama
        try:
            result["preflight"] = pb.embedding_preflight(args.upstream_url, args.embed_model)
        except passa_common.PassAError as exc:
            result["preflight"] = {"ran": True, "error": str(exc)}
    else:
        result["preflight"] = maybe_ollama_preflight(args.upstream_url, args.model, args.embed_model)
    if result["preflight"].get("error"):
        result["preflight"]["error"] = scrub(result["preflight"]["error"])
        return finish("preflight refused", 1)

    all_rows: list[dict] = []
    try:
        holder["gateway"] = pb.make_gateway(args.profile, args.workdir / "gateway", args.upstream_url,
                                            [args.model, args.embed_model], repo_root, timeout_s=args.upstream_timeout_s,
                                            request_defaults={args.model: passa_common.chat_defaults(args)})
        with holder["gateway"] as gw:
            try:
                dim = probe_embedding_dimension(gw.base_url, args.embed_model)
            except passa_common.PassAError as exc:
                result["dimension_probe"] = {"error": scrub(str(exc))}
                return finish("embedding probe failed", 1)
            probe_calls = gw.calls()
            result["embedding_dim"] = dim
            result["dimension_probe"] = {
                "calls": len(probe_calls), "http_status": probe_calls[0].get("http_status"),
                "input_tokens": probe_calls[0].get("input_tokens"),
                "note": "logged by the gateway, belongs to no checkpoint",
            }
            all_rows += [{**r, "checkpoint": 0, "kind": "dimension_probe"}
                         for r in call_rows(0, probe_calls, classify, cost=args.profile is not None)]
            template = args.workdir / "template"
            init = subprocess.run([str(args.graphrag), "init", "--root", str(template), "--model", "gpt-4.1",
                                   "--embedding", "text-embedding-3-large"],
                                  env=rehearsal.child_env(args.workdir / "home", args.tiktoken_cache, rehearsal.BLOCKING_PROXY),
                                  capture_output=True, timeout=300)
            if init.returncode != 0:
                result["init_error"] = scrub(init.stderr.decode(errors="replace")[-300:])
                return finish("graphrag init failed", 1)
            from graphrag.prompts.index import community_report, extract_graph, summarize_descriptions

            packaged = {"extract_graph.txt": extract_graph.GRAPH_EXTRACTION_PROMPT,
                        "summarize_descriptions.txt": summarize_descriptions.SUMMARIZE_PROMPT,
                        "community_report_graph.txt": community_report.COMMUNITY_REPORT_PROMPT}
            result["template_settings_sha256"] = hashlib.sha256((template / "settings.yaml").read_bytes()).hexdigest()
            result["prompt_files_equal_packaged_constants"] = {
                k: (template / "prompts" / k).read_text(encoding="utf-8") == v for k, v in packaged.items()}
            write_result()
            for n in checkpoints:
                print(f"checkpoint {n} ...", flush=True)
                cp, rows = run_checkpoint(n, args, dim, docs, template, gw, classify, scrub)
                result["checkpoints"][str(n)] = cp
                all_rows += rows
                s = cp["gateway_summary"]
                print(f"  exit={cp['exit_code']} indexed={cp['indexed_all_documents']} chat={s['chat_calls']} "
                      f"input_tokens={s['chat_input_tokens']} output_tokens={s['chat_output_tokens']} "
                      f"emb_inputs={s['embedding_inputs']} wall={cp['wall_seconds']}s", flush=True)
                write_result()
                if not cp["indexed_all_documents"]:
                    result["stopped_after_failed_checkpoint"] = n
                    break
            if args.profile is None:
                result["gateway"] = {"log": "<workdir>/gateway/meter.jsonl, and meter.jsonl.bodies.jsonl (holds article text; never commit)",
                                     "prices": "zero (a local model costs nothing); the gateway's job here is the uniform record",
                                     "upstream_timeout_s": args.upstream_timeout_s}
            else:
                result["gateway"] = {"log": "the profile's shared ledger (meter.jsonl and meter.jsonl.bodies.jsonl; holds article text; never commit)",
                                     "prices": "the chat model's are the profile's (see `hosted`); the embedding model's are zero",
                                     "upstream_timeout_s": args.profile.upstream_timeout_s}
    except passa_common.PassAError as exc:
        result["gateway_error"] = scrub(str(exc))
        return finish("gateway failed", 1)

    calls_path = args.workdir / "calls.jsonl"
    calls_path.write_text("".join(json.dumps(r) + "\n" for r in all_rows), encoding="utf-8")
    result["calls_jsonl_sha256"] = hashlib.sha256(calls_path.read_bytes()).hexdigest()
    result["calls_jsonl_note"] = "one line per call (no text), under the work directory; the hash ties this JSON to it"
    ok = all(cp["indexed_all_documents"] for cp in result["checkpoints"].values()) and len(result["checkpoints"]) == len(checkpoints)
    return finish("ok" if ok else "builder failure", 0 if ok else 1)


if __name__ == "__main__":
    sys.exit(main())
