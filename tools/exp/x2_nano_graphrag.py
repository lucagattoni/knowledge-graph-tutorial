"""X2 rehearsal, Step 0: nano-graphrag's INDEXING against the stub model server. No key, no model, no money.

What it does. It indexes the 20 frozen X2 documents with nano-graphrag (default settings) while a loopback stub
(`stub_llm.Stub`) stands in for the model, and counts the calls the builder makes: by kind, by model name, with the
prompt tokens and embedding inputs of each. It runs several scenarios, each in its own process (nano-graphrag keeps a
module-level client that remembers the first server address, so one process per scenario is the clean way):

    perdoc-B          the documents inserted one at a time into one working directory, answers in shape B
    perdoc-A          the same, answers in shape A
    perdoc-B-repeat   a clean second run of perdoc-B (determinism check)
    perdoc-B-nocache  perdoc-B with nano-graphrag's own response cache switched off (sensitivity)
    batch-B           all 20 documents in ONE insert call, shape B (sensitivity)

Shapes of the stub's answers (exactly):
    A  the smallest valid answer. Entity extraction and the gleaning prompt both get "<|COMPLETE|>" (no entities, no
       relations); a yes/no loop check gets "NO"; a description summary gets "Summary."; a community report gets a JSON
       object with an empty findings list.
    B  a plausible answer, derived from the chunk text without randomness. For a chunk, the candidate entity names are
       the words that start with a capital letter, are at least 3 letters long and follow a lowercase letter, a comma,
       a semicolon or a colon and one space (so a sentence's first word is skipped). The 6 most frequent in the chunk
       (ties broken alphabetically) are the entities; if the chunk has fewer than 6 distinct candidates the list is
       padded with names built from a hash of the chunk text. The entity type is one of the four default types chosen by
       a hash of the name, so a name has one type everywhere. Each entity's description is one sentence of about 30
       tokens that contains the first 12 words of the chunk (sanitised). The 5 relations join entity i to entity i+1.
       The gleaning prompt gets "<|COMPLETE|>" (nothing more), so a chunk yields 6 entities and 5 relations in all. A
       description summary gets one fixed sentence; a community report gets a JSON object with 5 findings of fixed text.

Run it (the environment is stripped; the runner is meant to be started with `env -i`, see the page next to the results):

    env -i PATH=/usr/bin:/bin:/opt/homebrew/bin HOME=$SCRATCH/home TIKTOKEN_CACHE_DIR=$SCRATCH/tiktoken-cache \\
      HTTP_PROXY=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 NO_PROXY=127.0.0.1,localhost \\
      $SCRATCH/venv/bin/python tools/exp/x2_nano_graphrag.py --corpus $SCRATCH/corpus.json \\
      --documents kb-kg/experiments/x2-index-cost/documents.tsv \\
      --out kb-kg/experiments/x2-index-cost/rehearsal/nano-graphrag.json --scratch $SCRATCH/runs

Nothing it writes into the --out file contains article text. Logs and the working directories (which do) go under
--scratch, outside the repository. The corpus file is checked against its pinned SHA-256 before anything runs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata as md
import json
import os
import platform
import re
import socket
import subprocess
import sys
import time
import traceback
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True  # importing stub_llm must not leave a __pycache__ next to it in the repository
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

CORPUS_SHA256 = "20b61b5ab84de84a927420c5d265b7ec8d859ae49980699958a787ade9e4d28f"
CHECKPOINTS = (1, 5, 20)
DUMMY_KEY = "sk-dummy-not-a-key"

SCENARIOS = [
    # name, mode, shape, cache
    ("perdoc-B", "perdoc", "B", "on"),
    ("perdoc-A", "perdoc", "A", "on"),
    ("perdoc-B-repeat", "perdoc", "B", "on"),
    ("perdoc-B-nocache", "perdoc", "B", "off"),
    ("batch-B", "batch", "B", "on"),
]
# Scenarios run for a secondary build of the builder (e.g. the default branch's latest commit).
SECONDARY_SCENARIOS = ["perdoc-B", "batch-B"]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d %H:%M:%S UTC")


# ---------------------------------------------------------------------------------------------------------------
# Corpus and documents
# ---------------------------------------------------------------------------------------------------------------
def load_documents(corpus_path: str, documents_tsv: str) -> list[dict]:
    raw = Path(corpus_path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != CORPUS_SHA256:
        raise SystemExit(f"corpus hash {digest} differs from the pin {CORPUS_SHA256}")
    by_url = {d["url"]: d for d in json.loads(raw)}
    lines = [ln for ln in Path(documents_tsv).read_text(encoding="utf-8").splitlines() if ln and not ln.startswith("#")]
    rows = list(csv.DictReader(lines, delimiter="\t"))
    docs = []
    for row in rows:
        d = by_url[row["url"]]
        docs.append({"rank": int(row["rank"]), "url_sha256_16": row["url_sha256_16"], "body": d["body"], "chars": len(d["body"])})
    return docs


# ---------------------------------------------------------------------------------------------------------------
# Network guard: record, and refuse, anything that is not loopback. Python-level sockets only.
# ---------------------------------------------------------------------------------------------------------------
class NetGuard:
    LOOPBACK = {"127.0.0.1", "::1", "localhost"}

    def __init__(self) -> None:
        self.stub_port: int | None = None
        self.events: list[dict] = []
        self.dns: list[dict] = []
        self._orig_connect = socket.socket.connect
        self._orig_connect_ex = socket.socket.connect_ex
        self._orig_getaddrinfo = socket.getaddrinfo

    @staticmethod
    def _packages() -> list[str]:
        out: list[str] = []
        for fs in traceback.extract_stack():
            m = re.search(r"site-packages/([^/]+)/", fs.filename)
            if m and m.group(1) not in out:
                out.append(m.group(1))
        return out

    def _check(self, address) -> None:
        if not isinstance(address, tuple) or len(address) < 2:
            return  # AF_UNIX and the like
        host, port = str(address[0]), int(address[1])
        if host in self.LOOPBACK or host.startswith("127."):
            if port != self.stub_port:
                self.events.append({"kind": "loopback_other_port", "host": host, "port": port, "packages": self._packages()})
            return
        self.events.append({"kind": "refused_non_loopback", "host": host, "port": port, "packages": self._packages()})
        raise ConnectionRefusedError(f"x2 guard: refused connect to {host}:{port}")

    def install(self) -> None:
        guard = self
        orig_connect, orig_connect_ex, orig_gai = self._orig_connect, self._orig_connect_ex, self._orig_getaddrinfo

        def connect(sock, address):  # type: ignore[no-untyped-def]
            guard._check(address)
            return orig_connect(sock, address)

        def connect_ex(sock, address):  # type: ignore[no-untyped-def]
            try:
                guard._check(address)
            except ConnectionRefusedError:
                return 61  # ECONNREFUSED on macOS
            return orig_connect_ex(sock, address)

        def getaddrinfo(host, *a, **kw):  # type: ignore[no-untyped-def]
            if host not in guard.LOOPBACK and not str(host).startswith("127."):
                guard.dns.append({"host": str(host), "packages": guard._packages()})
            return orig_gai(host, *a, **kw)

        socket.socket.connect = connect  # type: ignore[method-assign]
        socket.socket.connect_ex = connect_ex  # type: ignore[method-assign]
        socket.getaddrinfo = getaddrinfo  # type: ignore[assignment]

    def report(self) -> dict:
        def tally(rows: list[dict], keys: tuple[str, ...]) -> list[dict]:
            c: Counter = Counter()
            pk: dict = {}
            for r in rows:
                k = tuple(r[x] for x in keys)
                c[k] += 1
                pk[k] = r["packages"]
            return [dict(zip(keys, k), count=n, packages=pk[k]) for k, n in sorted(c.items())]

        return {
            "connect_attempts": tally(self.events, ("kind", "host", "port")),
            "dns_lookups_non_loopback": tally(self.dns, ("host",)),
        }


# ---------------------------------------------------------------------------------------------------------------
# Call classification and the responders (builder-specific)
# ---------------------------------------------------------------------------------------------------------------
def make_classifier(PROMPTS: dict):
    from stub_llm import message_text

    pre = {k: PROMPTS[k].split("{")[0] for k in ("entity_extraction", "summarize_entity_descriptions", "community_report")}
    continue_p = PROMPTS["entiti_continue_extraction"]
    loop_p = PROMPTS["entiti_if_loop_extraction"]

    def classify(call) -> str:
        if call.path.endswith("/embeddings"):
            return "embedding"
        if not call.path.endswith("/chat/completions"):
            return "other"
        msgs = call.messages
        first = message_text(msgs[0]) if msgs else ""
        last = message_text(msgs[-1]) if msgs else ""
        if len(msgs) > 1 and last == continue_p:
            return "gleaning_continue"
        if len(msgs) > 1 and last == loop_p:
            return "gleaning_loop_check"
        if first.startswith(pre["summarize_entity_descriptions"]):
            return "description_summary"
        if first.startswith(pre["community_report"]):
            return "community_report"
        if first.startswith(pre["entity_extraction"]):
            return "entity_extraction"
        return "other"

    return classify


EMPTY_REPORT = '{"title": "Report", "summary": "", "rating": 0, "rating_explanation": "", "findings": []}'
CAND = re.compile(r"(?<=[a-z,;:] )[A-Z][A-Za-z]{2,}\b")


def chunk_text_of(prompt: str, PROMPTS: dict) -> str:
    """The chunk the extraction prompt was built from (between 'Text: ' of the real data and the template's tail)."""
    tail = PROMPTS["entity_extraction"].split("{input_text}")[1]
    start = prompt.index("-Real Data-")
    start = prompt.index("\nText: ", start) + len("\nText: ")
    end = len(prompt) - len(tail) if prompt.endswith(tail) else len(prompt)
    return prompt[start:end]


def shape_b_entities(text: str) -> list[str]:
    counts = Counter(w.upper() for w in CAND.findall(text))
    ranked = [w for w, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))][:6]
    i = 0
    while len(ranked) < 6:
        pad = "ITEM " + hashlib.sha256(f"{text}|{i}".encode("utf-8")).hexdigest()[:6].upper()
        if pad not in ranked:
            ranked.append(pad)
        i += 1
    return ranked


def sanitize(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9 ,.'-]", "", s)


def make_responder(shape: str, PROMPTS: dict, classify):
    """(responder, produced): `produced` tallies what the responder put into its answers, for a cross-check against the
    builder's own progress line."""
    import threading

    lock = threading.Lock()
    produced = {"extraction_answers": 0, "entities_in_answers": 0, "relations_in_answers": 0}
    types = PROMPTS["DEFAULT_ENTITY_TYPES"]
    T, R, C = PROMPTS["DEFAULT_TUPLE_DELIMITER"], PROMPTS["DEFAULT_RECORD_DELIMITER"], PROMPTS["DEFAULT_COMPLETION_DELIMITER"]

    def type_of(name: str) -> str:
        return types[int(hashlib.sha256(name.encode("utf-8")).hexdigest(), 16) % len(types)]

    report_b = json.dumps({
        "title": "Report on a group of related entities",
        "summary": "This community groups entities that are discussed together in the indexed articles and describes how they relate.",
        "rating": 5.0,
        "rating_explanation": "The rating is a fixed value given by the stub.",
        "findings": [
            {"summary": f"Finding {i}", "explanation": f"Explanation {i}. The stub gives the same text for every community."}
            for i in range(1, 6)
        ],
    })

    def responder(call):
        kind = classify(call)
        if shape == "A":
            if kind in ("entity_extraction", "gleaning_continue"):
                return C
            if kind == "gleaning_loop_check":
                return "NO"
            if kind == "description_summary":
                return "Summary."
            if kind == "community_report":
                return EMPTY_REPORT
            return "OK"
        # shape B
        if kind == "entity_extraction":
            from stub_llm import message_text

            text = chunk_text_of(message_text(call.messages[0]), PROMPTS)
            names = shape_b_entities(text)
            snippet = sanitize(" ".join(text.split()[:12]))
            recs = [
                f'("entity"{T}"{n}"{T}"{type_of(n)}"{T}"{n} is a named item of kind {type_of(n)} that is discussed in a passage '
                f'which begins with: {snippet}.")'
                for n in names
            ]
            rels = []
            with lock:
                produced["extraction_answers"] += 1
                produced["entities_in_answers"] += len(names)
                produced["relations_in_answers"] += 5
            for i in range(5):
                a, b = names[i], names[i + 1]
                strength = 1 + int(hashlib.sha256(f"{a}|{b}".encode("utf-8")).hexdigest(), 16) % 9
                rels.append(
                    f'("relationship"{T}"{a}"{T}"{b}"{T}"{a} and {b} are discussed together in a passage that begins with: '
                    f'{snippet}."{T}{strength})'
                )
            return (R + "\n").join(recs + rels) + "\n" + C
        if kind == "gleaning_continue":
            return C
        if kind == "gleaning_loop_check":
            return "NO"
        if kind == "description_summary":
            return "This item is described across several passages of the indexed articles and is discussed together with other items."
        if kind == "community_report":
            return report_b
        return "OK"

    return responder, produced


# ---------------------------------------------------------------------------------------------------------------
# One scenario (child process)
# ---------------------------------------------------------------------------------------------------------------
def kind_table(calls, classify) -> dict:
    t: dict = defaultdict(lambda: {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0, "inputs": 0, "models": Counter()})
    for c in calls:
        k = classify(c)
        r = t[k]
        r["calls"] += 1
        r["prompt_tokens"] += c.prompt_tokens
        r["completion_tokens"] += c.completion_tokens
        r["inputs"] += len(c.inputs)
        r["models"][c.model] += 1
    out = {}
    for k, r in sorted(t.items()):
        row = {"calls": r["calls"], "prompt_tokens": r["prompt_tokens"], "completion_tokens": r["completion_tokens"], "models": dict(r["models"])}
        if k == "embedding":
            row["inputs"] = r["inputs"]
        out[k] = row
    return out


def request_params(calls, classify) -> dict:
    """For each kind of call, the request body's keys and the distinct values of every key except the text itself
    (`messages`, `input`). This is the builder's request surface, which a gateway or a provider adapter must accept."""
    seen: dict = defaultdict(lambda: defaultdict(set))
    for c in calls:
        k = classify(c)
        for key, val in c.raw.items():
            if key in ("messages", "input"):
                seen[k][key].add("<text>")
            else:
                seen[k][key].add(json.dumps(val, sort_keys=True))
    return {k: {key: sorted(vals) for key, vals in sorted(d.items())} for k, d in sorted(seen.items())}


def prompt_digest(calls, classify) -> str:
    rows = sorted(
        (classify(c), c.model, c.path, hashlib.sha256(c.prompt_text.encode("utf-8")).hexdigest(), c.prompt_tokens) for c in calls
    )
    return hashlib.sha256(json.dumps(rows).encode("utf-8")).hexdigest()


def chunking_arithmetic(docs: list[dict], defaults: dict) -> dict:
    """Arithmetic, not a measurement of the builder: the builder cuts a document of n tokens (tiktoken, the model name in
    `tiktoken_model_name`) at a step of chunk_token_size - chunk_overlap_token_size, so it makes ceil(n / step) chunks,
    the last of which can be almost wholly overlap."""
    import math

    import tiktoken

    enc = tiktoken.encoding_for_model(defaults["tiktoken_model_name"])
    step = defaults["chunk_token_size"] - defaults["chunk_overlap_token_size"]
    toks = [len(enc.encode(d["body"])) for d in docs]
    chunks = [math.ceil(n / step) for n in toks]
    return {
        "tokenizer": enc.name,
        "step_tokens": step,
        "tokens_per_document": toks,
        "total_document_tokens": sum(toks),
        "chunks_per_document": chunks,
        "total_chunks": sum(chunks),
    }


def template_tokens(PROMPTS: dict, count) -> dict:
    """Tokens (the stub's counter) of each indexing prompt template with its placeholders left empty or filled with
    the builder's own fixed values: the fixed part of every call of that kind."""
    ext = PROMPTS["entity_extraction"].format(
        tuple_delimiter=PROMPTS["DEFAULT_TUPLE_DELIMITER"], record_delimiter=PROMPTS["DEFAULT_RECORD_DELIMITER"],
        completion_delimiter=PROMPTS["DEFAULT_COMPLETION_DELIMITER"], entity_types=",".join(PROMPTS["DEFAULT_ENTITY_TYPES"]),
        input_text="",
    )
    return {
        "entity_extraction_empty_chunk": count(ext),
        "gleaning_continue_prompt": count(PROMPTS["entiti_continue_extraction"]),
        "gleaning_loop_check_prompt": count(PROMPTS["entiti_if_loop_extraction"]),
        "description_summary_empty": count(PROMPTS["summarize_entity_descriptions"].format(entity_name="", description_list="")),
        "community_report_empty": count(PROMPTS["community_report"].format(input_text="")),
    }


def run_scenario(args: argparse.Namespace) -> None:
    guard = NetGuard()
    guard.install()
    from stub_llm import Stub

    docs = load_documents(args.corpus, args.documents)
    if len(docs) != 20:
        raise SystemExit(f"expected 20 documents, got {len(docs)}")

    # Environment the builder sees: a dummy key, the stub's address. (The stripped environment comes from the caller.)
    os.environ["OPENAI_API_KEY"] = DUMMY_KEY
    import nano_graphrag
    from nano_graphrag import GraphRAG
    from nano_graphrag.prompt import PROMPTS
    from openai import AsyncOpenAI
    from stub_llm import make_counter

    classify = make_classifier(PROMPTS)
    responder, produced = make_responder(args.shape, PROMPTS, classify)
    workdir = Path(args.workdir)
    if workdir.exists():
        raise SystemExit(f"working directory {workdir} already exists; the scenario needs a clean one")

    started = time.time()
    with Stub(responder) as stub:
        guard.stub_port = stub._server.server_address[1]
        os.environ["OPENAI_BASE_URL"] = stub.base_url
        rag = GraphRAG(working_dir=str(workdir), enable_llm_cache=(args.cache == "on"))
        defaults = {
            k: getattr(rag, k)
            for k in (
                "chunk_token_size", "chunk_overlap_token_size", "tiktoken_model_name", "entity_extract_max_gleaning",
                "entity_summary_to_max_tokens", "graph_cluster_algorithm", "max_graph_cluster_size", "embedding_batch_num",
                "embedding_func_max_async", "best_model_max_async", "cheap_model_max_async", "enable_local", "enable_naive_rag",
                "enable_llm_cache",
            )
        }

        def graph_state() -> dict:
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

        def snapshot(n_docs: int) -> dict:
            calls = list(stub.calls)
            return {"n_docs": n_docs, "stub_summary": stub.summary(), "by_kind": kind_table(calls, classify), "graph": graph_state()}

        checkpoints: dict[str, dict] = {}
        per_document: list[dict] = []
        if args.mode == "perdoc":
            for i, d in enumerate(docs, start=1):
                before = len(stub.calls)
                t0 = time.time()
                rag.insert(d["body"])
                row = {"rank": d["rank"], "url_sha256_16": d["url_sha256_16"], "chars": d["chars"], "seconds": round(time.time() - t0, 2),
                       "by_kind": kind_table(stub.calls[before:], classify), "graph_after": graph_state()}
                per_document.append(row)
                if i in CHECKPOINTS:
                    checkpoints[str(i)] = snapshot(i)
        else:
            t0 = time.time()
            rag.insert([d["body"] for d in docs])
            per_document.append({"all_documents_in_one_insert": True, "seconds": round(time.time() - t0, 2)})
            checkpoints["20"] = snapshot(20)
        calls = list(stub.calls)
        sdk = AsyncOpenAI(api_key=DUMMY_KEY)
        dump = Path(args.dump)
        dump.parent.mkdir(parents=True, exist_ok=True)
        stub.dump_jsonl(str(dump))  # no text
        tokenizer_name = stub.tokenizer
        final = checkpoints["20"]
        digest = prompt_digest(calls, classify)

    result = {
        "scenario": args.name,
        "mode": args.mode,
        "shape": args.shape,
        "llm_cache": args.cache,
        "started_utc": datetime.fromtimestamp(started, timezone.utc).strftime("%Y%m%d %H:%M:%S UTC"),
        "wall_seconds": round(time.time() - started, 1),
        "stub_tokenizer": tokenizer_name,
        "defaults_observed": defaults,
        "checkpoints": checkpoints,
        "final": final,
        "per_document": per_document,
        "prompt_multiset_sha256": digest,
        "answers_produced_by_responder": produced,
        "request_params_by_kind": request_params(calls, classify),
        "other_calls": [classify(c) for c in calls].count("other"),
        "chunking_arithmetic": chunking_arithmetic(docs, defaults),
        "prompt_template_tokens": template_tokens(PROMPTS, make_counter()[1]),
        "openai_sdk_defaults": {"max_retries": sdk.max_retries, "timeout_seconds": str(sdk.timeout)},
        "network_guard": guard.report(),
        "runtime": {
            "python": platform.python_version(),
            "machine": platform.machine(),
            "nano_graphrag_version": getattr(nano_graphrag, "__version__", "unstated"),
            "packages": {p: md.version(p) for p in ("openai", "tiktoken", "networkx", "graspologic", "nano-vectordb", "numpy", "tenacity", "httpx")},
        },
    }
    Path(args.result).write_text(json.dumps(result, indent=1, sort_keys=True), encoding="utf-8")


def run_selftest() -> dict:
    """Positive control for the guard: two deliberate outbound attempts to an address in the documentation range
    192.0.2.0/24 (no DNS lookup, nothing can answer). One goes through urllib, which honours the proxy variables (so it
    should reach 127.0.0.1:9 and be refused there); one is a raw socket (so the guard itself must refuse it)."""
    import urllib.request

    guard = NetGuard()
    guard.install()
    outcome = {}
    try:
        urllib.request.urlopen("http://192.0.2.1/", timeout=3)
        outcome["urllib_via_proxy"] = "reached"
    except Exception as e:  # noqa: BLE001
        outcome["urllib_via_proxy"] = f"failed: {type(e).__name__}"
    try:
        socket.create_connection(("192.0.2.1", 80), timeout=2)
        outcome["raw_socket"] = "reached"
    except Exception as e:  # noqa: BLE001
        outcome["raw_socket"] = f"failed: {type(e).__name__}"
    outcome["proxy_env"] = {k: os.environ.get(k) for k in ("HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY")}
    outcome["recorded"] = guard.report()
    return outcome


# ---------------------------------------------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------------------------------------------
def spawn(python: str, name: str, mode: str, shape: str, cache: str, args: argparse.Namespace, tag: str) -> dict:
    runs = Path(args.scratch)
    runs.mkdir(parents=True, exist_ok=True)
    base = f"{tag}-{name}"
    workdir, result, dump, log = (runs / f"{base}.work", runs / f"{base}.result.json", runs / f"{base}.calls.jsonl", runs / f"{base}.log")
    for p in (result, dump, log):
        p.unlink(missing_ok=True)
    if workdir.exists():
        import shutil

        shutil.rmtree(workdir)
    cmd = [python, str(Path(__file__).resolve()), "--child", "--name", name, "--mode", mode, "--shape", shape, "--cache", cache,
           "--corpus", args.corpus, "--documents", args.documents, "--workdir", str(workdir), "--result", str(result), "--dump", str(dump)]
    t0 = time.time()
    with open(log, "wb") as fh:
        rc = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, env=os.environ.copy()).returncode
    if rc != 0 or not result.exists():
        tail = log.read_text(errors="replace")[-1500:] if log.exists() else ""
        return {"scenario": name, "failed": True, "exit_code": rc, "log_tail_chars": len(tail), "log_tail": sanitize_tail(tail)}
    out = json.loads(result.read_text())
    out["child_wall_seconds_incl_imports"] = round(time.time() - t0, 1)
    return out


def sanitize_tail(tail: str) -> str:
    """A failing run's log can contain a traceback; article text is not in tracebacks, but absolute local paths are."""
    return re.sub(r"/(?:Users|private|var|tmp)/[^\s'\"):]*", "<path>", tail)


def compare(a: dict, b: dict) -> dict:
    out = {"identical": True, "differences": []}
    for label, x, y in (("final.by_kind", a["final"]["by_kind"], b["final"]["by_kind"]),
                        ("final.stub_summary", {k: v for k, v in a["final"]["stub_summary"].items()},
                         {k: v for k, v in b["final"]["stub_summary"].items()}),
                        ("final.graph", a["final"]["graph"], b["final"]["graph"]),
                        ("prompt_multiset_sha256", a["prompt_multiset_sha256"], b["prompt_multiset_sha256"])):
        if x != y:
            out["identical"] = False
            out["differences"].append({"field": label, "first": x, "second": y})
    out["compared"] = ["final.by_kind (calls, prompt and completion tokens, models, embedding inputs)", "final.stub_summary", "final.graph",
                       "prompt_multiset_sha256 (every prompt's SHA-256 with kind, model, path and token count, sorted)"]
    return out


def orchestrate(args: argparse.Namespace) -> None:
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    existing = json.loads(out_path.read_text()) if out_path.exists() else {}
    primary = sys.executable
    scenarios: dict = {}
    for name, mode, shape, cache in SCENARIOS:
        print(f"[{utc_now()}] primary {name} ...", flush=True)
        scenarios[name] = spawn(primary, name, mode, shape, cache, args, "primary")
        print(f"    {'FAILED' if scenarios[name].get('failed') else 'ok'}", flush=True)
    secondary: dict = {}
    for label_py in args.secondary or []:
        label, py = label_py.split("=", 1)
        secondary[label] = {}
        for name, mode, shape, cache in SCENARIOS:
            if name not in SECONDARY_SCENARIOS:
                continue
            print(f"[{utc_now()}] secondary {label} {name} ...", flush=True)
            secondary[label][name] = spawn(py, name, mode, shape, cache, args, f"secondary-{label}")
            print(f"    {'FAILED' if secondary[label][name].get('failed') else 'ok'}", flush=True)
    selftest = subprocess.run([primary, str(Path(__file__).resolve()), "--selftest"], capture_output=True, text=True, env=os.environ.copy())
    try:
        guard_selftest = json.loads(selftest.stdout)
    except json.JSONDecodeError:
        guard_selftest = {"failed": True, "exit_code": selftest.returncode, "stderr_tail": sanitize_tail(selftest.stderr[-600:])}
    det = None
    if not scenarios["perdoc-B"].get("failed") and not scenarios["perdoc-B-repeat"].get("failed"):
        det = compare(scenarios["perdoc-B"], scenarios["perdoc-B-repeat"])
    existing.update({
        "runner": {"file": "tools/exp/x2_nano_graphrag.py", "finished_utc": utc_now(), "checkpoints": list(CHECKPOINTS)},
        "corpus_sha256": CORPUS_SHA256,
        "scenarios": scenarios,
        "determinism_perdoc_B_vs_repeat": det,
        "guard_selftest": guard_selftest,
    })
    if secondary:
        existing["secondary_builds"] = secondary
    out_path.write_text(json.dumps(existing, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"[{utc_now()}] wrote {args.out}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus", help="corpus.json (checked against its pinned SHA-256)")
    ap.add_argument("--documents", help="documents.tsv (the 20 frozen documents, selected by the url column)")
    ap.add_argument("--out", help="results JSON (orchestrator)")
    ap.add_argument("--scratch", help="directory for working directories, logs and call dumps (orchestrator); holds article text")
    ap.add_argument("--secondary", action="append", metavar="LABEL=PYTHON",
                    help="also run perdoc-B and batch-B with another python whose environment holds another build of the builder")
    # child-only
    ap.add_argument("--selftest", action="store_true", help="positive control for the network guard; prints JSON")
    ap.add_argument("--child", action="store_true")
    ap.add_argument("--name")
    ap.add_argument("--mode", choices=["perdoc", "batch"])
    ap.add_argument("--shape", choices=["A", "B"])
    ap.add_argument("--cache", choices=["on", "off"])
    ap.add_argument("--workdir")
    ap.add_argument("--result")
    ap.add_argument("--dump")
    args = ap.parse_args()
    if args.selftest:
        print(json.dumps(run_selftest()))
        return
    if not args.corpus or not args.documents:
        ap.error("--corpus and --documents are required")
    if args.child:
        run_scenario(args)
    else:
        if not args.out or not args.scratch:
            ap.error("--out and --scratch are required")
        orchestrate(args)


if __name__ == "__main__":
    main()
