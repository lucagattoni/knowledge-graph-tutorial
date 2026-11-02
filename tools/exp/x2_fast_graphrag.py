#!/usr/bin/env python3
"""X2 rehearsal for fast-graphrag: count its indexing calls against a stub model, with no key and no network.

    VENV_PYTHON tools/exp/x2_fast_graphrag.py \\
        --corpus CORPUS_JSON --documents kb-kg/experiments/x2-index-cost/documents.tsv \\
        --out kb-kg/experiments/x2-index-cost/rehearsal/fast-graphrag.json \\
        --scratch SCRATCH_DIR [--source-dir GIT_CHECKOUT_OF_THE_PINNED_COMMIT] [--tiktoken-cache DIR] \\
        [--facts FACTS_JSON] [--no-probes]

VENV_PYTHON is the python of the throwaway environment that holds fast-graphrag. The parent process only orchestrates
(standard library). It starts one child per run, each in a fresh working directory and with a minimal environment
(no inherited variables; proxies pointed at a closed port; a dummy key). The child imports `stub_llm` (next to this
file), starts the stub on loopback, points fast-graphrag at it with OPENAI_BASE_URL, and indexes the documents one
at a time with `GraphRAG.insert`, on the library's default configuration.

Runs: B (shape B, cumulative summaries after 1, 5 and 20 documents), A1, B again from a clean working directory
(determinism), and probes: shape A (fails), BL, E6, gleaning set to 1 and to 2, and an answer the library cannot
parse. The probes check the code reading; they are not defaults.

Response shapes (the stub's answers; every number below is "for these answers"):
  A  the smallest valid answer: no entities, no relationships; a one-character summary; no edge groups. The library
     cannot complete an insert on it (an empty entity list reaches its vector index as a one-dimensional array), so A is
     run as a probe and its failure is the result.
  A1 the smallest answer that lets the library finish: one entity per chunk (name ENTITY, type ENTITY_TYPES[0],
     description "."), no relationships; a one-character summary; no edge groups.
  B  about 6 entities and 5 relationships per chunk. Candidates are the distinct capitalised words of at least four
     letters that do not also occur in lower case in the same chunk, in order of first appearance; the first six are the
     entities (padded with synthetic names if a chunk yields fewer than two). Entity i has type
     ENTITY_TYPES[i % len(ENTITY_TYPES)] and a fixed-template description; relationship i links entity i to entity
     i+1. A summary request is answered with the first 256 characters of the text it was asked to summarise; an
     edge-grouping request is answered with no groups.
  BL  shape B with entity descriptions of 200 characters instead of about 35 (a sensitivity probe: the summary step
     triggers on description length, not on the number of chunks).
  E6  two entities (ALPHA, BETA) and six relationships between them in every chunk (a probe that makes the library's
     edge-grouping step run; run on one document).

Article text is never written to any file this tool is asked to write; it stays in memory and, for debugging, in the
scratch directory.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import logging
import os
import re
import socket
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINNED_CORPUS_SHA256 = "20b61b5ab84de84a927420c5d265b7ec8d859ae49980699958a787ade9e4d28f"

# User-side inputs of fast-graphrag (it has no defaults for them). Chosen for a news corpus; they are part of the prompt,
# so they change prompt tokens. Generic, not taken from the dataset's questions.
DOMAIN = (
    "Analyze news articles and identify the organizations, people, products, places and events they report on, "
    "and how these relate to each other."
)
EXAMPLE_QUERIES = [
    "Which company announced the product described in the article?",
    "Who is quoted in the article, and what organization do they belong to?",
    "What event does the article report, and where and when did it take place?",
]
ENTITY_TYPES = ["Organization", "Person", "Product", "Place", "Event"]

SNAPSHOTS = (1, 5, 20)
PROXY_CLOSED = "http://127.0.0.1:9"

# ---------------------------------------------------------------------------------------------------------------------
# Classifying calls and answering them (child side)
# ---------------------------------------------------------------------------------------------------------------------

SENTINELS = [
    ("extract", "<<ENTITY_TYPES_START>>"),
    ("gleaning_continue", "MANY entities were missed in the last extraction"),
    ("gleaning_done_check", "Retrospectively check if all entities"),
    ("summarize_description", "responsible for generating a summary of the data provided below"),
    ("edge_grouping", "responsible for maintaining a list of facts"),
    ("query_entities", "your task is to extract all entities relevant to perform information retrieval"),
    ("answer", "You are a helpful assistant analyzing the given input data"),
]


def _text(message: dict) -> str:
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)
    return ""


def classify(messages: list) -> tuple[str, bool, str]:
    """(kind, is_retry, text of the matching user message). A retry is a call whose last message is not the prompt:
    instructor appends the failed answer and an error message and asks again."""
    for idx in range(len(messages) - 1, -1, -1):
        m = messages[idx]
        if m.get("role") != "user":
            continue
        text = _text(m)
        for kind, needle in SENTINELS:
            if needle in text:
                return kind, idx != len(messages) - 1, text
    return "other", False, ""


def chunk_text_of(user_text: str) -> str:
    start = user_text.rfind("**Document**:\n")
    end = user_text.rfind("\n<<DOCUMENT_END>>")
    if start < 0 or end < 0:
        return ""
    return user_text[start + len("**Document**:\n"):end]


CANDIDATE_RE = re.compile(r"\b[A-Z][A-Za-z0-9]{3,}\b")


def shape_b_entities(chunk: str) -> list[str]:
    lower_words = set(re.findall(r"\b[a-z][A-Za-z0-9]*\b", chunk))
    seen: list[str] = []
    for w in CANDIDATE_RE.findall(chunk):
        if w.lower() in lower_words or w in seen:
            continue
        seen.append(w)
        if len(seen) == 6:
            break
    if len(seen) < 2:
        tag = hashlib.sha1(chunk.encode("utf-8")).hexdigest()[:6].upper()
        seen += [f"CHUNK{tag}ITEM{k}" for k in range(len(seen), 2)]
    return seen


def make_responder(shape: str):
    """shape: 'A', 'A1', 'B', or 'malformed' (an answer that is not JSON, for the retry probe)."""

    def responder(call):
        kind, _is_retry, user_text = classify(call.messages)
        if shape == "malformed" and kind in ("extract", "gleaning_continue"):
            return "I cannot answer in the requested format."
        if kind in ("extract", "gleaning_continue"):
            if shape == "A":
                return json.dumps({"entities": [], "relationships": [], "other_relationships": []})
            if shape == "A1":
                return json.dumps({"entities": [{"name": "ENTITY", "type": ENTITY_TYPES[0], "desc": "."}],
                                   "relationships": [], "other_relationships": []})
            if shape == "E6":
                return json.dumps({
                    "entities": [{"name": "ALPHA", "type": ENTITY_TYPES[0], "desc": "."},
                                 {"name": "BETA", "type": ENTITY_TYPES[1], "desc": "."}],
                    "relationships": [{"source": "ALPHA", "target": "BETA", "desc": f"Fact number {k}."}
                                      for k in range(6)],
                    "other_relationships": []})
            names = shape_b_entities(chunk_text_of(user_text) if kind == "extract" else _first_chunk(call.messages))

            def describe(n: str) -> str:
                if shape == "BL":
                    return (f"{n} is discussed in the passage. " * 7)[:200]
                return f"{n} is discussed in the passage."

            entities = [{"name": n, "type": ENTITY_TYPES[i % len(ENTITY_TYPES)], "desc": describe(n)}
                        for i, n in enumerate(names)]
            relations = [
                {"source": names[i], "target": names[i + 1],
                 "desc": f"{names[i]} is related to {names[i + 1]} in the passage."}
                for i in range(len(names) - 1)
            ]
            return json.dumps({"entities": entities, "relationships": relations, "other_relationships": []})
        if kind == "gleaning_done_check":
            return json.dumps({"status": "done"})
        if kind == "summarize_description":
            if shape in ("A", "A1", "E6"):
                return json.dumps({"description": "."})
            start = user_text.find("Current:\n")
            end = user_text.rfind("\n\nUpdated:")
            current = user_text[start + len("Current:\n"):end] if start >= 0 and end > start else ""
            return json.dumps({"description": current[:256]})
        if kind == "edge_grouping":
            return json.dumps({"grouped_facts": []})
        if kind == "query_entities":
            return json.dumps({"named": [], "generic": []})
        if kind == "answer":
            return json.dumps({"answer": "stub"})
        return "{}"

    return responder


def _first_chunk(messages: list) -> str:
    for m in messages:
        if m.get("role") == "user" and "<<ENTITY_TYPES_START>>" in _text(m):
            return chunk_text_of(_text(m))
    return ""


# ---------------------------------------------------------------------------------------------------------------------
# Network guard (child side)
# ---------------------------------------------------------------------------------------------------------------------

LOOPBACK = {"127.0.0.1", "::1", "localhost"}


def install_network_guard(log: list) -> None:
    """Record every connection and name lookup the process attempts beyond loopback, and refuse them.
    A connection to the closed proxy port (127.0.0.1:9) is how a proxy-aware client reaches 'the internet' here; the
    destination is then known only to the caller, so the innermost library frames are recorded instead."""
    real_connect = socket.socket.connect
    real_getaddrinfo = socket.getaddrinfo

    def where() -> list[str]:
        frames = []
        for fs in reversed(traceback.extract_stack(limit=40)):
            if "site-packages" in fs.filename:
                frames.append(f"{fs.filename.split('site-packages/')[-1]}:{fs.lineno}:{fs.name}")
            if len(frames) == 10:
                break
        return frames

    def record(kind: str, target: str) -> None:
        log.append({"t": datetime.now(timezone.utc).strftime("%Y%m%d %H:%M:%S"), "kind": kind, "target": target,
                    "innermost_library_frames": where()})

    def guarded_connect(self, address):  # type: ignore[no-untyped-def]
        host = address[0] if isinstance(address, tuple) else str(address)
        port = address[1] if isinstance(address, tuple) and len(address) > 1 else None
        if host in LOOPBACK:
            if port == 9:
                record("connect-to-closed-proxy-port", f"{host}:{port}")
            return real_connect(self, address)
        record("connect-refused-by-guard", f"{host}:{port}")
        raise OSError(f"network guard: connection to {host}:{port} refused")

    def guarded_getaddrinfo(host, *args, **kwargs):  # type: ignore[no-untyped-def]
        if isinstance(host, bytes):
            host_s = host.decode("ascii", "replace")
        else:
            host_s = str(host) if host is not None else ""
        if host_s and host_s not in LOOPBACK and not _is_ip(host_s):
            record("name-lookup-refused-by-guard", host_s)
            raise socket.gaierror(-2, f"network guard: lookup of {host_s} refused")
        return real_getaddrinfo(host, *args, **kwargs)

    socket.socket.connect = guarded_connect  # type: ignore[method-assign]
    socket.getaddrinfo = guarded_getaddrinfo  # type: ignore[assignment]


def _is_ip(s: str) -> bool:
    try:
        socket.inet_pton(socket.AF_INET, s)
        return True
    except OSError:
        pass
    try:
        socket.inet_pton(socket.AF_INET6, s)
        return True
    except OSError:
        return False


# ---------------------------------------------------------------------------------------------------------------------
# Shared loading
# ---------------------------------------------------------------------------------------------------------------------


def load_documents(corpus_path: Path, documents_tsv: Path, n: int) -> list[dict]:
    raw = corpus_path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != PINNED_CORPUS_SHA256:
        raise SystemExit(f"corpus sha256 {digest} differs from the pin {PINNED_CORPUS_SHA256}")
    by_url = {a["url"]: a for a in json.loads(raw)}
    rows = []
    for line in documents_tsv.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or line.startswith("rank\t"):
            continue
        f = line.split("\t")
        rows.append({"rank": int(f[0]), "url_sha256_16": f[1], "chars": int(f[2]), "url": f[7]})
    rows.sort(key=lambda r: r["rank"])
    docs = []
    for r in rows[:n]:
        body = by_url[r["url"]]["body"]
        if len(body) != r["chars"]:
            raise SystemExit(f"document rank {r['rank']}: {len(body)} characters, documents.tsv says {r['chars']}")
        docs.append({"rank": r["rank"], "url_sha256_16": r["url_sha256_16"], "chars": r["chars"], "body": body})
    return docs


# ---------------------------------------------------------------------------------------------------------------------
# Child: one run
# ---------------------------------------------------------------------------------------------------------------------


def tally(calls: list, count) -> dict:
    """Totals by kind over a list of stub Call objects. Retries are counted inside their kind and also separately.
    `count` is the stub's token counter. The stub counts an embedding request as ONE text (its inputs joined by
    newlines), so `tokens` can move by a token with the order of the inputs in a batch; `tokens_sum_of_inputs` counts
    each input alone and does not."""
    by_kind: dict[str, dict] = {}
    emb = {"requests": 0, "inputs": 0, "tokens": 0, "tokens_sum_of_inputs": 0, "inputs_per_request": {}}
    for c in calls:
        if c.path.endswith("/embeddings"):
            emb["requests"] += 1
            emb["inputs"] += len(c.inputs)
            emb["tokens"] += c.prompt_tokens
            emb["tokens_sum_of_inputs"] += sum(count(t) for t in c.inputs)
            k = str(len(c.inputs))
            emb["inputs_per_request"][k] = emb["inputs_per_request"].get(k, 0) + 1
            continue
        kind, is_retry, _ = classify(c.messages)
        d = by_kind.setdefault(kind, {"calls": 0, "retry_calls": 0, "prompt_tokens": 0, "completion_tokens": 0})
        d["calls"] += 1
        d["retry_calls"] += 1 if is_retry else 0
        d["prompt_tokens"] += c.prompt_tokens
        d["completion_tokens"] += c.completion_tokens
    chat = {"calls": sum(d["calls"] for d in by_kind.values()),
            "prompt_tokens": sum(d["prompt_tokens"] for d in by_kind.values()),
            "completion_tokens": sum(d["completion_tokens"] for d in by_kind.values())}
    return {"chat": chat, "chat_by_kind": dict(sorted(by_kind.items())), "embedding": emb}


class CountingHandler(logging.Handler):
    """Counts log records that matter for the call count: the OpenAI SDK's own retries of a request, and the library's
    error lines. Messages are cut short; full logs stay in the scratch directory."""

    def __init__(self) -> None:
        super().__init__(level=logging.INFO)
        self.sdk_retries = 0
        self.errors: list[dict] = []
        self.tokenizer_failures: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        msg = record.getMessage()
        if record.name.startswith("openai") and msg.startswith("Retrying request"):
            self.sdk_retries += 1
        if "failed to load tokenizer" in msg:
            self.tokenizer_failures.append(msg[:300])
        if record.levelno >= logging.ERROR:
            self.errors.append({"logger": record.name, "message_start": msg[:120]})


def run_child(args: argparse.Namespace) -> None:
    net_log: list = []
    install_network_guard(net_log)
    handler = CountingHandler()
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    sys.path.insert(0, str(HERE))
    from stub_llm import Stub, make_counter  # noqa: E402

    docs = load_documents(Path(args.corpus), Path(args.documents), args.n)
    run_dir = Path(args.run_dir)
    work = run_dir / "graph_working_dir"
    if work.exists():
        raise SystemExit(f"working directory {work} exists; a run starts clean")
    started = datetime.now(timezone.utc)

    responder = make_responder(args.shape)
    result: dict = {"run": args.run_name, "shape": args.shape, "gleaning_steps": args.gleaning,
                    "started_utc": started.strftime("%Y%m%d %H:%M:%S"), "documents": [], "snapshots": {}}
    with Stub(responder, default_dims=1536) as stub:
        os.environ["OPENAI_BASE_URL"] = stub.base_url
        os.environ["OPENAI_API_KEY"] = "dummy-not-a-key"
        result["tokenizer"] = stub.tokenizer
        count = make_counter()[1]
        import importlib.metadata as md

        from fast_graphrag import GraphRAG
        from fast_graphrag._services._chunk_extraction import DefaultChunkingService
        from fast_graphrag._types import TDocument
        from fast_graphrag._utils import get_event_loop

        result["fast_graphrag_version"] = md.version("fast-graphrag")
        rag = GraphRAG(working_dir=str(work), domain=DOMAIN, example_queries="\n".join(EXAMPLE_QUERIES),
                       entity_types=ENTITY_TYPES)
        if args.gleaning:
            rag.information_extraction_service.max_gleaning_steps = args.gleaning
        cfg = rag.config
        result["defaults_seen"] = {
            "llm_class": type(cfg.llm_service).__name__, "llm_model": cfg.llm_service.model,
            "llm_max_requests_concurrent": cfg.llm_service.max_requests_concurrent,
            "llm_rate_limit_per_minute_enabled": cfg.llm_service.rate_limit_per_minute,
            "embedding_model": cfg.embedding_service.model, "embedding_dim": cfg.embedding_service.embedding_dim,
            "embedding_max_elements_per_request": cfg.embedding_service.max_elements_per_request,
            "embedding_rate_limit_per_minute_enabled": cfg.embedding_service.rate_limit_per_minute,
            "max_gleaning_steps": rag.information_extraction_service.max_gleaning_steps,
            "chunk_token_size": rag.chunking_service.config.chunk_token_size,
            "chunk_token_overlap": rag.chunking_service.config.chunk_token_overlap,
            "chunk_size_chars": rag.chunking_service._chunk_size,
            "chunk_overlap_chars": rag.chunking_service._chunk_overlap,
            "max_node_description_size": cfg.node_upsert_policy.config.max_node_description_size,
            "edge_merge_threshold": cfg.edge_upsert_policy.config.edge_merge_threshold,
            "insert_similarity_score_threshold": rag.state_manager.insert_similarity_score_threshold,
        }
        seen = 0
        wall0 = time.time()
        for i, doc in enumerate(docs, 1):
            # What the chunker will produce, measured with the library's own chunker on a copy (sizes only).
            # (the builder's own event loop, not asyncio.run: that would close the loop the SDK client is bound to)
            probe = get_event_loop().run_until_complete(
                DefaultChunkingService().extract([TDocument(data=doc["body"], metadata={})]))
            chunk_lengths = [len(c.content) for c in list(probe)[0]]
            t0 = time.time()
            failure = None
            try:
                totals = rag.insert(doc["body"], show_progress=False)
            except Exception as exc:  # noqa: BLE001 - the failure is the result
                totals = (None, None, None)
                failure = f"{type(exc).__name__}: {str(exc)[:200]}"
            seconds = time.time() - t0
            new_calls = stub.calls[seen:]
            seen = len(stub.calls)
            row = {"n": i, "rank": doc["rank"], "url_sha256_16": doc["url_sha256_16"], "chars": doc["chars"],
                   "chunks_by_library_chunker": len(chunk_lengths),
                   "chunk_chars_min": min(chunk_lengths), "chunk_chars_max": max(chunk_lengths),
                   "graph_totals_after": {"entities": totals[0], "relations": totals[1], "chunks": totals[2]},
                   "seconds_against_stub": round(seconds, 3)}
            if failure:
                row["insert_failed"] = failure
            row.update(tally(new_calls, count))
            extraction_calls = row["chat_by_kind"].get("extract", {}).get("calls", 0) - \
                row["chat_by_kind"].get("extract", {}).get("retry_calls", 0)
            row["extraction_calls_equal_chunker_count"] = extraction_calls == len(chunk_lengths)
            result["documents"].append(row)
            if failure:
                result["stopped_at_document"] = i
                result["snapshots"][str(i)] = {"stub_summary": stub.summary(), **tally(list(stub.calls), count)}
                break
            if i in SNAPSHOTS or i == len(docs):
                snap = {"stub_summary": stub.summary()}
                snap.update(tally(list(stub.calls), count))
                result["snapshots"][str(i)] = snap
        result["wall_seconds_all_documents"] = round(time.time() - wall0, 3)
        result["final_stub_summary"] = stub.summary()
        result["prompt_sha256_sorted"] = sorted(
            hashlib.sha256(c.prompt_text.encode("utf-8")).hexdigest() for c in stub.calls)
        # Per-call records without text, in the scratch directory only (this is not a file of the repository).
        stub.dump_jsonl(str(run_dir / "calls_without_text.jsonl"))
        stub.dump_jsonl(str(run_dir / "calls_with_text_DEBUG.jsonl"), with_text=True)
        shapes: dict = {}
        for c in stub.calls:
            if c.path.endswith("/embeddings"):
                key = "embeddings"
            else:
                key = classify(c.messages)[0]
            if key not in shapes:
                shapes[key] = {"path": c.path, "request_body_keys": sorted(c.raw), "n_messages": len(c.messages),
                               "roles": [m.get("role") for m in c.messages], "response_format": c.raw.get("response_format"),
                               "model": c.model, "max_tokens": c.raw.get("max_tokens", "absent"),
                               "dimensions": c.raw.get("dimensions", "absent"), "stream": c.stream}
        result["first_request_of_each_kind"] = shapes
        entity_counts = []
        chunk_tokens = 0
        n_extract_first = 0
        for c in stub.calls:
            kind, retry, text = classify(c.messages)
            if kind == "extract" and not retry:
                chunk_tokens += count(chunk_text_of(text))
                n_extract_first += 1
        result["extraction_prompts"] = {
            "first_attempt_calls": n_extract_first, "tokens_of_the_chunk_text_alone": chunk_tokens,
            "note": "arithmetic: prompt tokens minus chunk-text tokens is the fixed part (instructions, example, "
                    "JSON schema) plus join effects of the tokenizer"}
        if args.shape in ("B", "BL"):
            for c in stub.calls:
                kind, retry, _ = classify(c.messages)
                if kind == "extract" and not retry:
                    entity_counts.append(len(shape_b_entities(chunk_text_of(_text(c.messages[-1])))))
        if entity_counts:
            result["shape_b_entities_per_chunk"] = {"min": min(entity_counts), "max": max(entity_counts),
                                                    "mean": round(sum(entity_counts) / len(entity_counts), 3),
                                                    "chunks": len(entity_counts)}
    result["finished_utc"] = datetime.now(timezone.utc).strftime("%Y%m%d %H:%M:%S")
    result["outbound_attempts"] = net_log
    result["openai_sdk_retries_logged"] = handler.sdk_retries
    result["tokenizer_download_failures_logged_by_library"] = handler.tokenizer_failures
    result["error_log_lines"] = {"count": len(handler.errors), "first_five": handler.errors[:5]}
    result["environment_variable_names"] = sorted(os.environ)
    result["files_in_working_dir"] = sorted(
        str(p.relative_to(work)) for p in work.rglob("*") if p.is_file()) if work.exists() else []
    Path(args.result).write_text(json.dumps(result, indent=1), encoding="utf-8")


# ---------------------------------------------------------------------------------------------------------------------
# Parent: orchestrate
# ---------------------------------------------------------------------------------------------------------------------


def minimal_env(scratch: Path, tiktoken_cache: str | None) -> dict:
    home = scratch / "home"
    tmp = scratch / "tmp"
    home.mkdir(parents=True, exist_ok=True)
    tmp.mkdir(parents=True, exist_ok=True)
    env = {
        "PATH": "/usr/bin:/bin:/opt/homebrew/bin",
        "HOME": str(home),
        "TMPDIR": str(tmp),
        "HTTP_PROXY": PROXY_CLOSED, "HTTPS_PROXY": PROXY_CLOSED, "ALL_PROXY": PROXY_CLOSED,
        "http_proxy": PROXY_CLOSED, "https_proxy": PROXY_CLOSED, "all_proxy": PROXY_CLOSED,
        "NO_PROXY": "127.0.0.1,localhost", "no_proxy": "127.0.0.1,localhost",
        "OPENAI_API_KEY": "dummy-not-a-key",
        "PYTHONDONTWRITEBYTECODE": "1",  # the child must not write bytecode into the repository's tools directory
    }
    if tiktoken_cache:
        env["TIKTOKEN_CACHE_DIR"] = tiktoken_cache
    return env


def run_one(args, name: str, shape: str, n: int, gleaning: int, env: dict) -> dict:
    run_dir = Path(args.scratch) / "runs" / name
    if run_dir.exists():
        raise SystemExit(f"{run_dir} exists; remove it to re-run (runs start from a clean directory)")
    run_dir.mkdir(parents=True)
    result_path = run_dir / "result.json"
    cmd = [sys.executable, str(Path(__file__).resolve()), "--child", "--run-name", name, "--shape", shape,
           "--n", str(n), "--gleaning", str(gleaning), "--corpus", args.corpus, "--documents", args.documents,
           "--run-dir", str(run_dir), "--result", str(result_path)]
    t0 = time.time()
    proc = subprocess.run(cmd, env=env, cwd=str(run_dir), capture_output=True, text=True)
    (run_dir / "child_stdout.log").write_text(proc.stdout, encoding="utf-8")
    (run_dir / "child_stderr.log").write_text(proc.stderr, encoding="utf-8")
    print(f"run {name}: exit {proc.returncode} in {time.time() - t0:.1f}s", file=sys.stderr)
    if proc.returncode != 0 or not result_path.exists():
        tail = "\n".join(proc.stderr.splitlines()[-15:])
        return {"run": name, "shape": shape, "failed": True, "exit_status": proc.returncode,
                "stderr_tail_first_lines": tail[:3000]}
    return json.loads(result_path.read_text(encoding="utf-8"))


def first_lines(path: Path, n: int) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()[:n]


ENV_FACTS_SNIPPET = """
import hashlib, importlib.metadata as md, json, pathlib, platform, sys
dist = md.distribution("fast-graphrag")
lic = [pathlib.Path(dist.locate_file(f)) for f in dist.files if "LICEN" in str(f).upper()]
print(json.dumps({
    "python": sys.version.split()[0], "machine": platform.machine(), "system": platform.system(),
    "fast_graphrag_version": dist.version,
    "distributions": sorted((d.metadata["Name"], d.version) for d in md.distributions()),
    "license_files_in_distribution": [str(f).split("site-packages/")[-1] for f in lic],
    "license_first_lines": lic[0].read_text().splitlines()[:3] if lic else [],
    "license_sha256": hashlib.sha256(lic[0].read_bytes()).hexdigest() if lic else None,
}))
"""


def environment_facts() -> dict:
    out = subprocess.run([sys.executable, "-c", ENV_FACTS_SNIPPET], capture_output=True, text=True,
                         env={"PATH": "/usr/bin:/bin"})
    return json.loads(out.stdout) if out.returncode == 0 else {"error": out.stderr[-500:]}


def source_facts(source_dir: str | None) -> dict:
    if not source_dir:
        return {}
    d = Path(source_dir)

    def git(*a: str) -> str:
        return subprocess.run(["git", "-C", str(d), *a], capture_output=True, text=True).stdout.strip()

    lic = d / "LICENSE"
    return {"commit": git("rev-parse", "HEAD"), "commit_date": git("log", "-1", "--format=%cI"),
            "commit_subject": git("log", "-1", "--format=%s"),
            "pyproject_version": next((ln.split('"')[1] for ln in (d / "pyproject.toml").read_text().splitlines()
                                       if ln.startswith("version =")), None),
            "license_first_lines": first_lines(lic, 3), "license_sha256": hashlib.sha256(lic.read_bytes()).hexdigest()}


def compare_determinism(a: dict, b: dict) -> dict:
    out: dict = {"runs": [a["run"], b["run"]]}
    if a.get("failed") or b.get("failed"):
        return {**out, "identical": False, "note": "a run failed"}
    last = str(max(int(k) for k in a["snapshots"]))
    final_a, final_b = a["snapshots"][last], b["snapshots"][last]
    same_by_kind = final_a["chat_by_kind"] == final_b["chat_by_kind"]
    same_emb = final_a["embedding"] == final_b["embedding"]  # includes the stub's joined-batch token count
    per_doc = [(x["chat_by_kind"], x["embedding"]) == (y["chat_by_kind"], y["embedding"])
               for x, y in zip(a["documents"], b["documents"])]
    same_prompts = a["prompt_sha256_sorted"] == b["prompt_sha256_sorted"]
    totals_same = [x["graph_totals_after"] for x in a["documents"]] == [y["graph_totals_after"] for y in b["documents"]]
    out.update({"calls_and_prompt_tokens_by_kind_identical": same_by_kind, "embedding_identical": same_emb,
                "per_document_identical": all(per_doc), "documents_identical": sum(per_doc),
                "multiset_of_prompt_sha256_identical": same_prompts, "graph_totals_identical": totals_same,
                "identical": same_by_kind and same_emb and all(per_doc) and same_prompts})
    return out


def run_parent(args: argparse.Namespace) -> None:
    scratch = Path(args.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    docs = load_documents(Path(args.corpus), Path(args.documents), args.n)  # fail early on a wrong corpus
    env = minimal_env(scratch, args.tiktoken_cache)
    started = datetime.now(timezone.utc)
    runs: dict[str, dict] = {}
    plan = [("shape_B_run1", "B", args.n, 0), ("shape_A1_one_entity", "A1", args.n, 0),
            ("shape_B_run2_clean_dir", "B", args.n, 0)]
    if not args.no_probes:
        plan += [("probe_shape_A_empty", "A", 1, 0), ("probe_shape_BL_long_descriptions", "BL", args.n, 0),
                 ("probe_shape_E6_six_edges_one_pair", "E6", 1, 0), ("probe_gleaning_1", "B", 1, 1), ("probe_gleaning_2", "B", 1, 2),
                 ("probe_unparseable_answer", "malformed", 1, 0)]
    for name, shape, n, gl in plan:
        runs[name] = run_one(args, name, shape, n, gl, env)
    out = {
        "builder": "fast-graphrag",
        "repository": "https://github.com/circlemind-ai/fast-graphrag",
        "documents": {"count": len(docs), "source": "documents.tsv", "total_chars": sum(d["chars"] for d in docs)},
        "inputs_given_to_the_builder": {"domain": DOMAIN, "example_queries": EXAMPLE_QUERIES, "entity_types": ENTITY_TYPES},
        "minimal_environment_variable_names": sorted(env),
        "proxy_setting": PROXY_CLOSED,
        "source": source_facts(args.source_dir),
        "installed": environment_facts(),
        "started_utc": started.strftime("%Y%m%d %H:%M:%S"),
        "finished_utc": datetime.now(timezone.utc).strftime("%Y%m%d %H:%M:%S"),
        "runs": runs,
    }
    if args.facts:
        out["recorded_by_hand"] = json.loads(Path(args.facts).read_text(encoding="utf-8"))
    if "shape_B_run1" in runs and "shape_B_run2_clean_dir" in runs:
        out["determinism"] = compare_determinism(runs["shape_B_run1"], runs["shape_B_run2_clean_dir"])
    # The sorted prompt hashes are long and only needed for the comparison above.
    for r in runs.values():
        r.pop("prompt_sha256_sorted", None)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {args.out}", file=sys.stderr)
    failed = [k for k, v in runs.items() if v.get("failed")]
    if failed:
        print(f"FAILED runs: {failed}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--documents", required=True)
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--out")
    ap.add_argument("--scratch")
    ap.add_argument("--source-dir")
    ap.add_argument("--tiktoken-cache")
    ap.add_argument("--facts", help="a JSON file of facts recorded by hand (sources and UTC read times, install notes); "
                                    "copied into the output under 'recorded_by_hand', not produced by this tool")
    ap.add_argument("--no-probes", action="store_true")
    ap.add_argument("--child", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--run-name", help=argparse.SUPPRESS)
    ap.add_argument("--shape", default="B", help=argparse.SUPPRESS)
    ap.add_argument("--gleaning", type=int, default=0, help=argparse.SUPPRESS)
    ap.add_argument("--run-dir", help=argparse.SUPPRESS)
    ap.add_argument("--result", help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.child:
        run_child(args)
    else:
        if not (args.out and args.scratch):
            ap.error("--out and --scratch are required")
        run_parent(args)


if __name__ == "__main__":
    main()
