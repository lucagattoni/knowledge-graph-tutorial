"""X2 pass-A runner for LightRAG: index the 20 frozen documents through the metering gateway, at an upstream you choose.

    python x2_passa_lightrag.py --corpus CORPUS_JSON --documents DOCUMENTS_TSV --repo-root REPO \\
        --upstream-url http://127.0.0.1:PORT/v1 --model CHAT_MODEL --embed-model EMBED_MODEL \\
        --workdir NEW_EMPTY_DIR --out RESULT_JSON [--checkpoints 1,5,20] [--tiktoken-cache DIR]
        [--preflight-min-ctx N] [--llm-max-async N] [--llm-timeout SECONDS] [--embedding-use-base64 true|false]
        [--hosted-profile PROFILE_JSON]

The stub rehearsal (`x2_lightrag.py`) counted what LightRAG sends to a loopback stub. This runner sends the same calls
through `tools/metering_gateway.py` (started here, via `passa_common.LocalGateway`) to whatever answers at
`--upstream-url`: the stub (free; validates the plumbing) or a local Ollama (a real model). The program is the same for
both. LightRAG only ever talks to the gateway, with a dummy key; the gateway's log is the record of every call.

Pass B (`--hosted-profile PROFILE_JSON`, see `passb_common.py` and `passb_profile.example.json`): the CHAT model (`--model`) is
served by a hosted provider through the same gateway, which holds the key (it reads the file the profile names; this program
never does) and refuses past the cap; `--upstream-url` and `--embed-model` stay the LOCAL embedding upstream. Only the embedding
model is checked in Ollama. The JSON gains a `hosted` block (cost, prices with their source, model name as the provider reports
it, the shared ledger's size before the run; never the key file's path or the ledger's) and a `cost_usd` per checkpoint. The
gateway log is the profile's shared ledger, and `gw.calls()` returns only this run's records, so every count below is this
run's. Without the option nothing in this program changes.

Run it with the LightRAG virtual environment's Python (`lightrag-hku`, `openai` and `tiktoken` installed), in a minimal
environment, for example

    env -i PATH=/usr/bin:/bin:/opt/homebrew/bin HOME=$SCRATCH/home TMPDIR=$SCRATCH/home/tmp \\
        $SCRATCH/venv/bin/python -I tools/exp/x2_passa_lightrag.py ... --tiktoken-cache $SCRATCH/tiktoken-cache

Safety measures kept from the rehearsal runner, and made independent of how it was started:
  * the process environment is cleared at start to a short allow-list (names only are recorded), so no credential or
    LightRAG setting such as MAX_ASYNC or LLM_TIMEOUT from the invoking shell reaches the builder, and the run changes
    into the new working directory before LightRAG is imported, because its import reads a `.env` file from the current
    directory;
  * HTTP(S)_PROXY point at a closed port, with loopback excluded (NO_PROXY), so nothing can leave the machine through a proxy;
  * a Python audit hook records every socket connection or name lookup that is not to the gateway, and every subprocess
    start (the rehearsal's hook, imported), and a self-test connect proves the hook fires;
  * the upstream must be a loopback address, and the working directory must be outside the repository (the gateway's body
    log holds article text).

What it records at each checkpoint (default 1, 5, 20 documents; documents are indexed one at a time, in rank order, and
indexing stops after the last checkpoint). All "gateway" numbers are the provider's own usage as the gateway logged it:
  * calls by kind (chat: the rehearsal's classification of the prompt; embeddings: which LightRAG storage the text is
    written to), HTTP statuses, input and output tokens, the sum of per-call latency, calls the gateway voided or refused,
    and repeated identical requests (a retry shows as a repeated request body, and as a non-200 status before it);
  * the builder's own sizes (chunks, entities, relations, graph nodes and edges, LLM-cache entries), read from its working
    directory, and its warning counts (a malformed model answer is a warning, not an error);
  * `as_stub_summary`: the same eight quantities the rehearsal reports from the stub, derived from the gateway log, so a
    run against the stub can be compared with the committed rehearsal field by field.
The embedding dimension is read from one embeddings call through the gateway before LightRAG is built; that call is
recorded separately (`dimension_probe`) and is not in any checkpoint. Exit status 0 only if every requested document
reached LightRAG's `processed` status; a failure is recorded in the JSON (`status`, `failure`) and the exit status is 1.

Article text is never written by this program: the JSON carries counts, sizes and hashes only. It is checked before it is
written (no absolute local path, no 40-character run of any document). The gateway's body log, in the working directory,
does hold article text: never commit it.

Standard library plus LightRAG's own dependencies. Not run against a real model as of writing.
"""

from __future__ import annotations

import argparse
import asyncio
import collections
import contextlib
import functools
import hashlib
import importlib.metadata
import json
import logging
import os
import platform
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.dont_write_bytecode = True  # a runner must not leave .pyc files in the repository
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import passa_common as pc
import passb_common as pb
import x2_lightrag as rehearsal  # its prompt classifier, document loader and audit hook are reused, not copied

RUNNER = "x2_passa_lightrag.py"
PROBE_TEXT = "embedding dimension probe"
DEFAULT_CHECKPOINTS = (1, 5, 20)
KEEP_ENV = ("PATH", "HOME", "TMPDIR", "LANG", "LC_ALL", "LC_CTYPE", "TZ", "TIKTOKEN_CACHE_DIR")
DEAD_PROXY = "http://127.0.0.1:9"
LOOPBACK_HOSTS = ("127.0.0.1", "localhost", "::1")
CHAT_ROUTE = "/chat/completions"
EMBED_ROUTE = "/embeddings"
CREDENTIAL_LIKE = re.compile(r"KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL|AUTH", re.IGNORECASE)
PATH_LIKE = re.compile(r"(?:/Users|/private|/var|/tmp|/home|/opt|/Volumes)/[^\s'\"`,;:)\]}]*")
FORBIDDEN_PATH_PREFIXES = ("/Users/", "/private/", "/home/", "/Volumes/")
DEPENDENCIES = ("lightrag-hku", "openai", "tiktoken", "nano-vectordb", "networkx", "numpy", "tenacity", "pipmaster")


def utc_now() -> str:
    return time.strftime("%Y%m%d %H:%M:%S", time.gmtime())


def scrub(text: str, extra: tuple[str, ...] = ()) -> str:
    """Replace absolute local paths in a string; `extra` are known prefixes (working directory, repository, home)."""
    for prefix in sorted((p for p in extra if p and len(p) > 8 and p.startswith("/")), key=len, reverse=True):
        text = text.replace(prefix, "<path>")
    return PATH_LIKE.sub("<path>", text)


def scrub_tree(value, extra: tuple[str, ...] = ()):
    if isinstance(value, str):
        return scrub(value, extra)
    if isinstance(value, dict):
        return {scrub(str(k), extra): scrub_tree(v, extra) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [scrub_tree(v, extra) for v in value]
    return value


# ---- environment -----------------------------------------------------------------------------------------------
def harden_environment(tiktoken_cache: str | None, embedding_use_base64: str | None = None) -> dict:
    """Clear the environment to an allow-list and point every proxy at a closed port, before LightRAG is imported.

    LightRAG reads settings such as MAX_ASYNC, LLM_TIMEOUT, CHUNK_SIZE and ENTITY_EXTRACTION_USE_JSON from the
    environment when it is imported, so they must be gone before then or the defaults would silently change.
    Only names are recorded, never values.
    """
    before = set(os.environ)
    kept = {k: os.environ[k] for k in KEEP_ENV if k in os.environ}
    credential_like = sum(1 for k in before - set(kept) if CREDENTIAL_LIKE.search(k))
    os.environ.clear()
    os.environ.update(kept)
    if tiktoken_cache:
        os.environ["TIKTOKEN_CACHE_DIR"] = str(Path(tiktoken_cache).resolve())
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        os.environ[name] = DEAD_PROXY
    os.environ["NO_PROXY"] = os.environ["no_proxy"] = ",".join(LOOPBACK_HOSTS)
    set_by_flag = {}
    if embedding_use_base64 is not None:  # the one request-format setting that may differ between providers
        os.environ["EMBEDDING_USE_BASE64"] = set_by_flag["EMBEDDING_USE_BASE64"] = embedding_use_base64
    return {
        "python_isolated_mode": bool(sys.flags.isolated),
        "names_kept": sorted(kept),
        "names_removed": len(before - set(kept)),
        "removed_names_that_look_like_credentials": credential_like,
        "proxy": f"{DEAD_PROXY} (closed port), loopback excluded",
        "builder_settings_set_by_flag": set_by_flag,
    }


def tokenizer_selftest() -> dict:
    """LightRAG's chunker and the embedding truncation need tiktoken's vocabularies; offline they must be in the cache."""
    import tiktoken

    out = {}
    for name in ("o200k_base", "cl100k_base"):
        try:
            tiktoken.get_encoding(name)
            out[name] = "available"
        except Exception as exc:  # noqa: BLE001
            raise SystemExit(f"tiktoken vocabulary {name} is not available offline ({type(exc).__name__}); "
                             "pass --tiktoken-cache DIR with the vocabularies downloaded once") from None
    return out


# ---- reading the gateway's log ---------------------------------------------------------------------------------
class _Messages:
    """What the rehearsal's classify() reads from a stub Call: `.messages`."""

    def __init__(self, messages: list) -> None:
        self.messages = messages


def chat_kind(call: dict) -> str:
    """The rehearsal's kind of a chat call, read from the request body in the gateway's body log."""
    request = call.get("request")
    messages = request.get("messages") if isinstance(request, dict) else None
    if not isinstance(messages, list) or not all(isinstance(m, dict) for m in messages):
        return "malformed_request"
    return rehearsal.classify(_Messages(messages))


def embedding_texts(call: dict) -> list[str]:
    request = call.get("request")
    raw = request.get("input") if isinstance(request, dict) else None
    if raw is None:
        return []
    items = raw if isinstance(raw, list) else [raw]
    return [x if isinstance(x, str) else json.dumps(x) for x in items]


def embedding_kind(call: dict, labels: dict[str, set[str]]) -> str:
    """Which storage the embedded texts were written to (chunks, entities, relationships), as in the rehearsal."""
    kinds = set()
    for text in embedding_texts(call):
        namespaces = labels.get(hashlib.sha256(text.encode("utf-8")).hexdigest())
        kinds.add("unlabelled" if not namespaces else next(iter(namespaces)) if len(namespaces) == 1 else "mixed")
    return next(iter(kinds)) if len(kinds) == 1 else "mixed"


def is_route(call: dict, suffix: str) -> bool:
    return str(call.get("route") or "").endswith(suffix)


def body_keys(calls: list[dict]) -> dict:
    """Top-level request-body keys seen, with the number of calls carrying each and the distinct values of the keys
    that are neither the prompt nor the model (for example `stream`, `response_format`, `encoding_format`)."""
    count: collections.Counter = collections.Counter()
    values: dict[str, set[str]] = collections.defaultdict(set)
    for c in calls:
        request = c.get("request")
        if not isinstance(request, dict):
            continue
        for k, v in request.items():
            count[k] += 1
            if k not in ("messages", "input", "model"):
                values[k].add(json.dumps(v, sort_keys=True)[:80])
    return {"keys": dict(sorted(count.items())), "values_of_other_keys": {k: sorted(v) for k, v in sorted(values.items())}}


def tally(calls: list[dict], labels: dict[str, set[str]]) -> dict:
    """Everything the gateway's log says about `calls` (a list of gw.calls() dicts)."""
    chat = [c for c in calls if is_route(c, CHAT_ROUTE)]
    emb = [c for c in calls if is_route(c, EMBED_ROUTE)]
    chat_sum = pc.summarize(chat, chat_kind)
    emb_sum = pc.summarize(emb, lambda c: embedding_kind(c, labels))
    for kind in emb_sum["by_kind"]:
        emb_sum["by_kind"][kind]["inputs"] = 0
    for c in emb:
        kind = embedding_kind(c, labels) if c.get("request") is not None else "no_body"
        emb_sum["by_kind"][kind]["inputs"] += len(embedding_texts(c))
    emb_sum["total"]["inputs"] = sum(v["inputs"] for v in emb_sum["by_kind"].values())
    identical = collections.Counter((c.get("route"), c.get("request_sha256")) for c in calls)
    models: dict[str, collections.Counter] = {"chat": collections.Counter(), "embeddings": collections.Counter()}
    for c in chat:
        models["chat"][str(c.get("model_requested"))] += 1
    for c in emb:
        models["embeddings"][str(c.get("model_requested"))] += 1
    return {
        "calls": len(calls),
        "chat": chat_sum,
        "embeddings": emb_sum,
        "other_calls": len(calls) - len(chat) - len(emb),
        "http_status": dict(sorted(collections.Counter(str(c.get("http_status")) for c in calls).items())),
        "voided": sum(1 for c in calls if c.get("voided")),
        "usage_missing": sum(1 for c in calls if c.get("usage_missing")),
        "refused_by_gateway": sum(1 for c in calls if c.get("refusal")),
        "errors": dict(collections.Counter(str(c.get("error")) for c in calls if c.get("error"))),
        "distinct_requests": len(identical),
        "repeated_identical_requests": sum(n - 1 for n in identical.values() if n > 1),
        "latency_ms_total": sum(c.get("latency_ms") or 0 for c in calls),
        "model_requested": {k: dict(v) for k, v in models.items()},
        "request_body": {"chat": body_keys(chat), "embeddings": body_keys(emb)},
        # the eight quantities the rehearsal reports from the stub (its `stub_summary`), from the gateway's log
        "as_stub_summary": {
            "chat_calls": len(chat),
            "chat_prompt_tokens": chat_sum["total"]["input_tokens"],
            "chat_completion_tokens": chat_sum["total"]["output_tokens"],
            "embedding_calls": len(emb),
            "embedding_inputs": emb_sum["total"]["inputs"],
            "embedding_tokens": emb_sum["total"]["input_tokens"],
            "other_calls": len(calls) - len(chat) - len(emb),
        },
    }


def multiset_hash(calls: list[dict]) -> str:
    """Order-free fingerprint of what was requested: route, request body hash, status, input tokens."""
    rows = [f"{c.get('route')}|{c.get('request_sha256')}|{c.get('http_status')}|{c.get('input_tokens')}" for c in calls]
    return hashlib.sha256("\n".join(sorted(rows)).encode()).hexdigest()


def stored_sizes(workdir: Path) -> dict:
    """What LightRAG stored, from its working directory (counts only), as the rehearsal reports it."""
    stored: dict = {}
    storage = workdir / "rag_storage"
    for fname in ("kv_store_text_chunks.json", "vdb_chunks.json", "vdb_entities.json", "vdb_relationships.json"):
        p = storage / fname
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            if fname.startswith("kv_store"):
                stored["chunks"] = len(data)
                stored["chunk_tokens_sum_lightrag_tokenizer"] = sum(int(v.get("tokens", 0)) for v in data.values())
            else:
                stored[fname.removeprefix("vdb_").removesuffix(".json")] = len(data.get("data", []))
    graph = storage / "graph_chunk_entity_relation.graphml"
    if graph.exists():
        xml = graph.read_text(encoding="utf-8")
        stored["graph_nodes"] = xml.count("<node ")
        stored["graph_edges"] = xml.count("<edge ")
    cache = storage / "kv_store_llm_response_cache.json"
    if cache.exists():
        stored["llm_response_cache_entries"] = len(json.loads(cache.read_text(encoding="utf-8")))
    return stored


# ---- the dimension probe ---------------------------------------------------------------------------------------
def probe_embedding_dimension(base_url: str, embed_model: str) -> int:
    """One embeddings call through the gateway; the length of the vector is the dimension LightRAG is configured with."""
    body = json.dumps({"model": embed_model, "input": [PROBE_TEXT], "encoding_format": "float"}).encode("utf-8")
    req = urllib.request.Request(f"{base_url}/embeddings", data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"embedding dimension probe: HTTP {exc.code} from the gateway") from None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"embedding dimension probe: {type(exc).__name__}") from None
    data = payload.get("data") if isinstance(payload, dict) else None
    vector = data[0].get("embedding") if isinstance(data, list) and data and isinstance(data[0], dict) else None
    if not isinstance(vector, list) or not vector or not all(isinstance(x, (int, float)) for x in vector):
        raise RuntimeError("embedding dimension probe: the answer holds no vector of numbers")
    return len(vector)


# ---- the run ---------------------------------------------------------------------------------------------------
async def build_and_index(args: argparse.Namespace, docs: list[dict], gw: pc.LocalGateway, workdir: Path,
                          dim: int, probe_calls: int, result: dict) -> None:
    """Build LightRAG against the gateway and index the documents one at a time, recording at each checkpoint."""
    os.environ["OPENAI_API_BASE"] = gw.base_url
    os.environ["OPENAI_API_KEY"] = "dummy-not-a-key"
    warn = rehearsal.WarnCounter()
    logging.getLogger("lightrag").addHandler(warn)
    logging.getLogger("lightrag").setLevel(logging.WARNING)

    from lightrag import LightRAG
    from lightrag.kg.nano_vector_db_impl import NanoVectorDBStorage
    from lightrag.llm.openai import openai_complete, openai_embed
    from lightrag.utils import EmbeddingFunc

    logging.getLogger().setLevel(logging.WARNING)  # LightRAG's import sets INFO: one line per HTTP call is noise here

    # Label the text of every vector write with the storage it goes to, so the embedding inputs in the gateway's log
    # can be told apart as chunks / entities / relationships. This only observes; the original method runs unchanged.
    labels: dict[str, set[str]] = collections.defaultdict(set)
    original_upsert = NanoVectorDBStorage.upsert

    async def labelled_upsert(self, data):
        for v in data.values():
            text = v.get("content")
            if isinstance(text, str):
                labels[hashlib.sha256(text.encode("utf-8")).hexdigest()].add(self.namespace)
        return await original_upsert(self, data)

    NanoVectorDBStorage.upsert = labelled_upsert

    # The stock OpenAI embedding binding with only the model name and the dimension replaced; its retry wrapper is kept
    # (`.func` is the undecorated-by-EmbeddingFunc function) and every other attribute is read from the stock object.
    embedding_func = EmbeddingFunc(
        embedding_dim=dim,
        func=functools.partial(openai_embed.func, model=args.embed_model),
        max_token_size=openai_embed.max_token_size,
        send_dimensions=openai_embed.send_dimensions,
        model_name=args.embed_model,
        supports_asymmetric=openai_embed.supports_asymmetric,
    )
    optional: dict = {}
    if args.llm_max_async is not None:
        optional["llm_model_max_async"] = args.llm_max_async
    if args.llm_timeout is not None:
        optional["default_llm_timeout"] = args.llm_timeout
    rag = LightRAG(
        working_dir=str(workdir / "rag_storage"),
        llm_model_func=openai_complete,  # LightRAG's own binding that sends `llm_model_name` as the model
        llm_model_name=args.model,
        embedding_func=embedding_func,
        **optional,
    )
    result["config_as_constructed"] = {
        "chunk_token_size": rag.chunk_token_size,
        "chunk_overlap_token_size": rag.chunk_overlap_token_size,
        "entity_extract_max_gleaning": rag.entity_extract_max_gleaning,
        "force_llm_summary_on_merge": rag.force_llm_summary_on_merge,
        "summary_max_tokens": rag.summary_max_tokens,
        "summary_context_size": rag.summary_context_size,
        "llm_model_max_async": rag.llm_model_max_async,
        "default_llm_timeout_s": rag.default_llm_timeout,
        "worker_timeout_s_arithmetic": rag.default_llm_timeout * 2,
        "max_parallel_insert": rag.max_parallel_insert,
        "embedding_batch_num": rag.embedding_batch_num,
        "embedding_func_max_async": rag.embedding_func_max_async,
        "embedding_dim": rag.embedding_func.embedding_dim,
        "embedding_max_token_size": rag.embedding_func.max_token_size,
        "entity_extraction_use_json": rag.entity_extraction_use_json,
        "enable_llm_cache": rag.enable_llm_cache,
        "enable_llm_cache_for_entity_extract": rag.enable_llm_cache_for_entity_extract,
        "tiktoken_model_name": rag.tiktoken_model_name,
        "llm_model_name": rag.llm_model_name,
        "overridden_by_flag": sorted(optional),
        "chunking": "fixed-token (ainsert always uses it)",
    }
    await rag.initialize_storages()

    checkpoints = result["checkpoints_requested"]
    last = max(checkpoints)
    result["per_document"] = []
    t_start = time.time()
    seen = 0  # gateway calls (after the dimension probe) already attributed to a document
    try:
        for i, doc in enumerate(docs[:last], start=1):
            doc_id = f"doc-{doc['rank']:02d}"
            t_doc = time.time()
            failure = None
            status = None
            try:
                await rag.ainsert(doc["text"], ids=[doc_id])
                row = await rag.doc_status.get_by_id(doc_id)
                raw_status = row.get("status") if isinstance(row, dict) else getattr(row, "status", None)
                status = getattr(raw_status, "value", raw_status)
                if status != "processed":
                    message = row.get("error_msg") if isinstance(row, dict) else getattr(row, "error_msg", None)
                    failure = {"kind": "document_not_processed", "doc_status": status,
                               "error_msg": scrub(str(message or ""), result["_scrub"])[:300]}
            except Exception as exc:  # noqa: BLE001 - recorded, then the run stops
                failure = {"kind": "ainsert_raised", "exception": type(exc).__name__,
                           "message": scrub(str(exc), result["_scrub"])[:300]}
            calls = gw.calls()[probe_calls:]
            new = calls[seen:]
            seen = len(calls)
            delta = tally(new, labels)
            result["per_document"].append({
                "document": i,
                "doc_rank": doc["rank"],
                "chars": len(doc["text"]),
                "doc_status": status,
                "wall_seconds": round(time.time() - t_doc, 1),
                "gateway_calls": delta["calls"],
                "chat_calls": delta["as_stub_summary"]["chat_calls"],
                "chat_input_tokens": delta["as_stub_summary"]["chat_prompt_tokens"],
                "chat_output_tokens": delta["as_stub_summary"]["chat_completion_tokens"],
                "embedding_inputs": delta["as_stub_summary"]["embedding_inputs"],
                "latency_ms_total": delta["latency_ms_total"],
                "non_200_calls": sum(n for s, n in delta["http_status"].items() if s != "200"),
                **({"cost_usd": pb.cost_usd(new)} if args.profile is not None else {}),
            })
            if failure is not None:
                failure["document"] = i
                failure["doc_rank"] = doc["rank"]
                result["failure"] = failure
            if i in checkpoints or failure is not None:
                key = str(i) if failure is None else f"failed_at_{i}"
                result["checkpoints"][key] = {
                    "documents_attempted": i,
                    "documents_processed": i - (1 if failure else 0),
                    "wall_seconds_since_start": round(time.time() - t_start, 1),
                    "gateway": tally(calls, labels),
                    "builder": {
                        "stored": stored_sizes(workdir),
                        "lightrag_warning_counts": dict(warn.count),
                    },
                }
                if args.profile is not None:
                    result["checkpoints"][key]["cost_usd"] = pb.cost_usd(calls)     # cumulative since indexing began
            if failure is not None:
                break
    finally:
        await rag.finalize_storages()
        result["stored_final"] = stored_sizes(workdir)
        result["lightrag_warning_counts"] = dict(warn.count)


def execute(args: argparse.Namespace, docs: list[dict], result: dict) -> None:
    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    # LightRAG reads a `.env` file from the current directory when it is imported (base.py, lightrag.py, utils.py:
    # load_dotenv(".env")), which could bring settings or credentials from wherever the runner was started into the
    # builder. The new, empty working directory has none, so go there before anything is imported.
    os.chdir(workdir)
    gw = pb.make_gateway(args.profile, workdir / "gateway", args.upstream_url, [args.model, args.embed_model], args.repo_root,
                         request_defaults={args.model: pc.chat_defaults(args)})
    gw.start()
    audit = None
    try:
        result["gateway"] = {"base_url": gw.base_url, "models": [args.model, args.embed_model],
                             "upstream_timeout_s": gw.timeout_s,
                             "metering": ("prices are zero; the cap cannot refuse" if args.profile is None else
                                          "the chat model is hosted and priced; the gateway refuses past the cap "
                                          "(the ledger's spend plus the profile's allowance)")}
        if args.profile is not None:
            result["preflight"] = pb.embedding_preflight(args.upstream_url, args.embed_model)
        elif args.preflight_min_ctx:
            root = args.upstream_url.rstrip("/").removesuffix("/v1")
            result["preflight"] = pc.preflight(root, args.model, min_ctx=args.preflight_min_ctx, embed_model=args.embed_model)

        audit = rehearsal.Audit(gw.port)
        sys.addaudithook(audit.hook)
        # Tripwire self-test: a connect to the closed proxy port on loopback (nothing leaves the machine) must be
        # recorded, otherwise "no outbound attempt" would mean nothing. Then the record is cleared.
        with contextlib.suppress(OSError):
            socket.create_connection(("127.0.0.1", 9), timeout=1).close()
        result["tripwire_selftest_recorded_a_connect_to_127.0.0.1:9"] = audit.connects.get("127.0.0.1:9", 0) >= 1
        audit.connects.clear()
        result["tokenizer"] = tokenizer_selftest()

        dim = probe_embedding_dimension(gw.base_url, args.embed_model)
        result["embedding_dim"] = dim
        probe = gw.calls()
        first = probe[0] if probe else {}
        if len(probe) != 1 or not is_route(first, EMBED_ROUTE) or embedding_texts(first) != [PROBE_TEXT]:
            raise RuntimeError("the gateway log does not hold exactly the dimension probe before LightRAG starts")
        result["dimension_probe"] = {"http_status": first.get("http_status"), "input_tokens": first.get("input_tokens"),
                                     "latency_ms": first.get("latency_ms"), "vector_length": dim,
                                     "note": "not counted in any checkpoint"}
        asyncio.run(build_and_index(args, docs, gw, workdir, dim, len(probe), result))
        result["openai_api_base_was_set_to_gateway"] = os.environ.get("OPENAI_API_BASE", "") == gw.base_url
    finally:
        if audit is not None:
            result["outbound"] = {"connections_not_to_gateway": dict(audit.connects),
                                  "name_lookups_not_loopback": dict(audit.resolves),
                                  "subprocess_starts": list(audit.subprocesses)}
        gw.stop()
        with contextlib.suppress(Exception):
            record_gateway_log(gw, result)
        if args.profile is not None:
            result["hosted"] = pb.hosted_block_for(gw)


def record_gateway_log(gw: pc.LocalGateway, result: dict) -> None:
    """After the gateway has stopped, everything it wrote is on disk: take the final record from there."""
    everything = gw.calls()
    counted = everything[1:] if everything else []  # the first record is the dimension probe
    in_largest_checkpoint = max((c["gateway"]["calls"] for c in result["checkpoints"].values()), default=0)
    result["gateway_log_records"] = len(everything)
    result["calls_logged_after_last_checkpoint"] = (len(counted) - in_largest_checkpoint) if result["checkpoints"] else None
    result["calls_jsonl_sha256"] = hashlib.sha256(gw.log_path.read_bytes()).hexdigest()
    result["calls_jsonl_note"] = ("sha256 of the gateway's own log (no bodies); it holds call ids and times, so it differs "
                                  "between runs. calls_multiset_sha256 is the order-free, time-free fingerprint")
    result["calls_multiset_sha256"] = multiset_hash(counted)


# ---- output ----------------------------------------------------------------------------------------------------
def check_output(text: str, docs: list[dict], forbidden: tuple[str, ...]) -> list[str]:
    """Reasons the JSON must not be written: a local path, or a long verbatim run of any document."""
    problems = [f"contains {p!r}" for p in FORBIDDEN_PATH_PREFIXES + forbidden if p and p in text]
    for doc in docs:
        body = doc["text"]
        for start in range(0, max(len(body) - 40, 0), 50):
            if body[start:start + 40] in text:
                problems.append(f"contains a 40-character run of document {doc['rank']}")
                break
    return problems


def write_result(path: Path, result: dict, docs: list[dict], extra: tuple[str, ...]) -> list[str]:
    public = {k: v for k, v in result.items() if not k.startswith("_")}
    public = scrub_tree(public, extra)
    text = json.dumps(public, indent=1)
    problems = check_output(text, docs, extra)
    if problems:
        print("refusing to write the result: " + "; ".join(problems), file=sys.stderr)
        return problems
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)
    return []


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus", required=True, help="MultiHop-RAG corpus.json (SHA-256 is checked)")
    ap.add_argument("--documents", required=True, help="documents.tsv listing the 20 documents by url")
    ap.add_argument("--repo-root", required=True, help="repository root (tools/metering_gateway.py is started from it)")
    ap.add_argument("--upstream-url", required=True,
                    help="OpenAI-compatible base URL on loopback, e.g. http://127.0.0.1:11434/v1")
    ap.add_argument("--model", required=True, help="chat model name, sent exactly as given")
    ap.add_argument("--embed-model", required=True, help="embedding model name, sent exactly as given")
    pc.add_chat_default_argument(ap)
    pb.add_hosted_argument(ap)
    ap.add_argument("--workdir", required=True,
                    help="new empty directory outside the repository (LightRAG storage, gateway log and body log)")
    ap.add_argument("--out", required=True, help="result JSON to write")
    ap.add_argument("--checkpoints", default=",".join(map(str, DEFAULT_CHECKPOINTS)),
                    help="comma-separated document counts at which to record; indexing stops after the last (default 1,5,20)")
    ap.add_argument("--tiktoken-cache",
                    help="directory holding tiktoken's o200k_base and cl100k_base vocabularies (needed offline)")
    ap.add_argument("--preflight-min-ctx", type=int, metavar="N",
                    help="Ollama only: refuse to start unless --model has an explicit num_ctx of at least N "
                         "(passa_common.preflight)")
    ap.add_argument("--llm-max-async", type=int, metavar="N",
                    help="override LightRAG's concurrent model calls (default: its own, 4)")
    ap.add_argument("--embedding-use-base64", choices=("true", "false"),
                    help="LightRAG's EMBEDDING_USE_BASE64 (default: its own, true: asks for base64 vectors, handles floats too)")
    ap.add_argument("--llm-timeout", type=int, metavar="SECONDS",
                    help="override LightRAG's per-call model timeout (default: its own, 240 s; a worker gives up at twice that)")
    args = ap.parse_args(argv)
    try:
        args.checkpoint_list = sorted({int(x) for x in args.checkpoints.split(",") if x.strip()})
    except ValueError:
        ap.error("--checkpoints must be comma-separated integers")
    if not args.checkpoint_list or args.checkpoint_list[0] < 1:
        ap.error("--checkpoints must hold positive integers")
    if args.model == args.embed_model:
        ap.error("--model and --embed-model must differ (the gateway keeps one price entry per name)")
    host = urllib.parse.urlsplit(args.upstream_url).hostname
    if host not in LOOPBACK_HOSTS:
        ap.error(f"--upstream-url must be a loopback address, not {host!r}: pass A never leaves the machine")
    try:
        args.profile = pb.profile_from_args(args)  # read now: the run changes directory later
    except pc.PassAError as exc:
        ap.error(str(exc))
    if args.profile is not None and args.preflight_min_ctx:
        ap.error("--preflight-min-ctx checks the chat model in Ollama, and with --hosted-profile the chat model is hosted "
                 "(only the embedding model is checked)")
    for field in ("corpus", "documents", "repo_root", "workdir", "out"):  # the run changes directory, so fix paths first
        setattr(args, field, str(Path(getattr(args, field)).resolve()))
    if Path(args.workdir).is_relative_to(Path(args.repo_root)):
        ap.error("--workdir must be outside the repository: the gateway's body log holds article text")
    if Path(args.workdir).exists() and any(Path(args.workdir).iterdir()):
        ap.error("--workdir is not empty; LightRAG answers a repeated prompt from its cache and the gateway refuses an old log")
    if not (Path(args.repo_root) / "tools" / "metering_gateway.py").is_file():
        ap.error("--repo-root has no tools/metering_gateway.py")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    started = utc_now()
    t0 = time.time()
    docs = rehearsal.load_documents(args.corpus, args.documents)
    if max(args.checkpoint_list) > len(docs):
        raise SystemExit(f"--checkpoints asks for {max(args.checkpoint_list)} documents, the list has {len(docs)}")
    local_paths = {args.workdir, args.repo_root, str(Path.home()), os.path.dirname(args.out)}
    if args.profile is not None:
        local_paths |= {args.profile.ledger_dir, args.profile.key_file}     # never written, and replaced if one ever got in
    scrub_prefixes = tuple(sorted(local_paths, key=len, reverse=True))
    result: dict = {
        "runner": RUNNER,
        "builder": "LightRAG",
        "package": "lightrag-hku",
        "upstream_url": args.upstream_url,
        "model": args.model,
        "embed_model": args.embed_model,
        "chat_request_defaults": pc.chat_defaults(args),
        "corpus_sha256": rehearsal.PINNED_CORPUS_SHA256,
        "documents_requested": max(args.checkpoint_list),
        "checkpoints_requested": args.checkpoint_list,
        "checkpoints": {},
        "status": "failed",
        "failure": None,
        "started_utc": started,
        "python": sys.version.split()[0],
        "machine": platform.machine(),
        "system": platform.system(),
        "_scrub": scrub_prefixes,
    }
    result["environment"] = harden_environment(args.tiktoken_cache, args.embedding_use_base64)
    try:
        execute(args, docs, result)
        if result["failure"] is None:
            missing = [n for n in args.checkpoint_list if str(n) not in result["checkpoints"]]
            if missing:
                result["failure"] = {"kind": "checkpoints_missing", "checkpoints": missing}
        result["status"] = "ok" if result["failure"] is None else "failed"
    except (Exception, SystemExit, KeyboardInterrupt) as exc:  # noqa: BLE001 - recorded in the JSON, exit status 1
        message = exc.code if isinstance(exc, SystemExit) else str(exc)
        result["failure"] = result["failure"] or {"kind": "runner_error", "exception": type(exc).__name__,
                                                   "message": scrub(str(message), scrub_prefixes)[:300]}
        result["status"] = "failed"
    with contextlib.suppress(Exception):
        result["version"] = importlib.metadata.version("lightrag-hku")
        result["dependency_versions"] = {d: importlib.metadata.version(d) for d in DEPENDENCIES}
    result["finished_utc"] = utc_now()
    result["wall_seconds"] = round(time.time() - t0, 1)
    problems = write_result(Path(args.out), result, docs, scrub_prefixes)
    ok = result["status"] == "ok" and not problems
    if problems:
        print(f"{RUNNER}: result not written", file=sys.stderr)
    else:
        reason = f" ({result['failure']['kind']})" if result["failure"] else ""
        print(f"{RUNNER}: {result['status']}{reason}; wrote {Path(args.out).name}", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
