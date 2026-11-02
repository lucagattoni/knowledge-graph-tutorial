"""X2 rehearsal runner for LightRAG: count the model and embedding calls its INDEXING makes, against a stub.

    python x2_lightrag.py --corpus CORPUS_JSON --documents documents.tsv --out OUT.json --workroot DIR

Run it with the LightRAG virtual environment's Python (`lightrag-hku`, `openai` and `tiktoken` installed) and a
minimal environment so that nothing of the user's reaches the third-party code, for example

    env -i PATH=/usr/bin:/bin:/opt/homebrew/bin HOME=$SCRATCH/home TMPDIR=$SCRATCH/home/tmp \\
        TIKTOKEN_CACHE_DIR=$SCRATCH/tiktoken-cache \\
        HTTP_PROXY=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 NO_PROXY=127.0.0.1,localhost \\
        $SCRATCH/venv/bin/python -I tools/exp/x2_lightrag.py --corpus ... --documents ... --out ... --workroot ...

The driver (default) starts one worker subprocess per scenario, each in a fresh working directory under --workroot:

    B1  shape B responder, the 20 documents indexed one at a time into one working directory; the stub's totals are
        recorded after 1, 5 and 20 documents
    A   shape A responder, the same 20 documents the same way
    B2  the identical run as B1, from a clean working directory (the determinism check)
    H   a probe, not a prediction: shape B plus one extra entity (and one relation to it) in every chunk, so that
        one entity collects many description fragments and LightRAG's summary-on-merge path is exercised

No model is called: LightRAG is pointed at the loopback stub (`stub_llm.Stub`) through its own `OPENAI_API_BASE`
setting with a dummy key. The worker records every socket connection that is not to the stub (an audit hook), so an
attempt to reach the internet, or to start a subprocess such as a package install, shows up in the result.

The stub counts prompt tokens with tiktoken's cl100k_base (or characters/4 if tiktoken cannot load its vocabulary);
neither is any provider's own tokenizer, and LightRAG's own chunker counts with o200k_base.

Response shapes (what the stub answers; counts that depend on the answers are counts for these answers only):
    A  the smallest valid answer: an extraction call gets only the completion delimiter (no entities, no relations),
       and so does a gleaning call.
    B  a plausible answer: from the chunk text, the 6 most frequent capitalised words that do not start a sentence
       (ties by first appearance; padded with the most frequent long lowercase words, title-cased, if fewer than 6)
       become 6 entities, and consecutive pairs of them become 5 relations. A gleaning call gets only the completion
       delimiter (nothing missed). A summary call gets a one-line fixed-form text.
    H  shape B, plus an entity named Hubentity and a relation from the first entity to it, in every chunk.

Article text is never written by this program: the JSON carries counts, sizes and hashes only. Standard library plus
LightRAG's own dependencies.
"""

from __future__ import annotations

import argparse
import asyncio
import collections
import contextlib
import csv
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

sys.dont_write_bytecode = True  # a rehearsal must not leave .pyc files in the repository
sys.path.insert(0, str(Path(__file__).resolve().parent))

PINNED_CORPUS_SHA256 = "20b61b5ab84de84a927420c5d265b7ec8d859ae49980699958a787ade9e4d28f"
COMPLETE = "<|COMPLETE|>"
TUPLE = "<|#|>"
ENTITY_TYPES = ["Person", "Organization", "Location", "Event", "Concept", "Content"]
SCENARIOS = {"B1": "B", "A": "A", "B2": "B", "H": "H"}
SNAPSHOT_AT = (1, 5, 20)


def utc_now() -> str:
    return time.strftime("%Y%m%d %H:%M:%S", time.gmtime())


# ---- documents -------------------------------------------------------------------------------------------------
def load_documents(corpus_path: str, documents_tsv: str) -> list[dict]:
    raw = Path(corpus_path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != PINNED_CORPUS_SHA256:
        raise SystemExit(f"corpus sha256 {digest} differs from the pin {PINNED_CORPUS_SHA256}")
    articles = {a["url"]: a for a in json.loads(raw)}
    docs = []
    with open(documents_tsv, encoding="utf-8") as fh:
        rows = csv.DictReader((ln for ln in fh if not ln.startswith("#")), delimiter="\t")
        for row in rows:
            a = articles[row["url"]]
            if len(a["body"]) != int(row["chars"]):
                raise SystemExit(f"rank {row['rank']}: body has {len(a['body'])} characters, the list says {row['chars']}")
            docs.append({"rank": int(row["rank"]), "url_sha256_16": row["url_sha256_16"], "text": a["body"]})
    docs.sort(key=lambda d: d["rank"])
    return docs


# ---- responder -------------------------------------------------------------------------------------------------
_MEDIAL_CAP = re.compile(r"(?<=[a-z,] )[A-Z][a-z]{3,}")
_LONG_WORD = re.compile(r"\b[a-z]{7,}\b")
_SUMMARY_NAME = re.compile(r"^(Entity|Relation) Name: (.*)$", re.MULTILINE)


def classify(call) -> str:
    """The kind of a chat call, from its prompt. 'other' if it is none of the indexing prompts."""
    from stub_llm import message_text

    system = " ".join(message_text(m) for m in call.messages if m.get("role") == "system")
    last_user = ""
    for m in call.messages:
        if m.get("role") == "user":
            last_user = message_text(m)
    if "responsible for extracting entities and relationships" in system:
        return "extraction_gleaning" if len(call.messages) > 2 else "extraction_initial"
    if "synthesize a list of descriptions" in last_user:
        m = _SUMMARY_NAME.search(last_user)
        return "summary_relation" if m and m.group(1) == "Relation" else "summary_entity"
    if "keyword" in system.lower() or "keyword" in last_user.lower():
        return "keywords"
    return "other"


def chunk_text(prompt_user: str) -> str:
    head = "---Input Text---\n```\n"
    start = prompt_user.index(head) + len(head)
    end = prompt_user.rindex("\n```\n\n---Output---")
    return prompt_user[start:end]


def shape_b_entities(text: str) -> list[str]:
    caps = collections.Counter(_MEDIAL_CAP.findall(text))
    first = {}
    for m in _MEDIAL_CAP.finditer(text):
        first.setdefault(m.group(0), m.start())
    ranked = sorted(caps, key=lambda w: (-caps[w], first[w]))
    names = ranked[:6]
    if len(names) < 6:
        longs = collections.Counter(_LONG_WORD.findall(text))
        firstl = {}
        for m in _LONG_WORD.finditer(text):
            firstl.setdefault(m.group(0), m.start())
        for w in sorted(longs, key=lambda w: (-longs[w], firstl[w])):
            t = w.title()
            if t not in names:
                names.append(t)
            if len(names) == 6:
                break
    return names


def entity_type(name: str) -> str:
    return ENTITY_TYPES[int(hashlib.sha256(name.encode()).hexdigest()[:8], 16) % len(ENTITY_TYPES)]


def shape_b_answer(text: str, hub: bool = False) -> str:
    names = shape_b_entities(text)
    n_words = len(text.split())
    rows = []
    for i, name in enumerate(names):
        nb = names[i + 1] if i + 1 < len(names) else names[i - 1] if i else name
        rows.append(f"entity{TUPLE}{name}{TUPLE}{entity_type(name)}{TUPLE}"
                    f"{name} is discussed in a passage of {n_words} words together with {nb}.")
    pairs = list(zip(names, names[1:]))
    if hub and names:
        rows.append(f"entity{TUPLE}Hubentity{TUPLE}Concept{TUPLE}"
                    f"Hubentity is discussed in a passage of {n_words} words together with {names[0]}.")
        pairs.append((names[0], "Hubentity"))
    for a, b in pairs:
        rows.append(f"relation{TUPLE}{a}{TUPLE}{b}{TUPLE}co-occurrence, discussion{TUPLE}"
                    f"{a} and {b} are discussed in the same passage of {n_words} words.")
    return "\n".join(rows + [COMPLETE])


class Responder:
    def __init__(self, shape: str) -> None:
        assert shape in ("A", "B", "H")
        self.shape = shape
        self.unclassified = 0
        self._lock = threading.Lock()

    def __call__(self, call) -> str:
        from stub_llm import message_text

        kind = classify(call)
        if kind == "extraction_initial":
            if self.shape == "A":
                return COMPLETE
            user = [message_text(m) for m in call.messages if m.get("role") == "user"][-1]
            return shape_b_answer(chunk_text(user), hub=self.shape == "H")
        if kind == "extraction_gleaning":
            return COMPLETE
        if kind in ("summary_entity", "summary_relation"):
            user = [message_text(m) for m in call.messages if m.get("role") == "user"][-1]
            name = _SUMMARY_NAME.search(user).group(2).strip()
            return f"{name} is described across several passages of the indexed articles."
        with self._lock:
            self.unclassified += 1
        return COMPLETE


# ---- audit of outbound attempts ----------------------------------------------------------------------------------
class Audit:
    """Records socket connections and subprocess starts, without changing behaviour."""

    def __init__(self, stub_port: int) -> None:
        self.stub_port = stub_port
        self.connects: collections.Counter = collections.Counter()
        self.resolves: collections.Counter = collections.Counter()
        self.subprocesses: list[str] = []
        self._lock = threading.Lock()

    def hook(self, event: str, args: tuple) -> None:
        try:
            if event == "socket.connect":
                addr = args[1]
                if isinstance(addr, tuple) and len(addr) >= 2:
                    host, port = addr[0], addr[1]
                    if host in ("127.0.0.1", "::1") and port == self.stub_port:
                        return
                    with self._lock:
                        self.connects[f"{host}:{port}"] += 1
            elif event == "socket.getaddrinfo":
                host = args[0]
                if host not in ("127.0.0.1", "localhost", "::1", None):
                    with self._lock:
                        self.resolves[str(host)] += 1
            elif event in ("subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn"):
                frame, mods = sys._getframe(1), []
                while frame is not None and len(mods) < 6:
                    mod = frame.f_globals.get("__name__", "?")
                    if not mods or mods[-1] != mod:
                        mods.append(mod)
                    frame = frame.f_back
                with self._lock:
                    self.subprocesses.append(f"{event}:{str(args[0])[:40]} from {' < '.join(mods)}")
        except Exception:  # noqa: BLE001 - an audit hook must never break the audited program
            pass

    def result(self) -> dict:
        return {
            "connections_not_to_stub": dict(self.connects),
            "name_lookups_not_loopback": dict(self.resolves),
            "subprocess_starts": list(self.subprocesses),
        }


# ---- measuring -------------------------------------------------------------------------------------------------
CHAT_KINDS = ["extraction_initial", "extraction_gleaning", "summary_entity", "summary_relation", "keywords", "other"]
EMB_KINDS = ["chunks", "entities", "relationships", "unlabelled", "mixed"]


def measure(stub, labels: dict[str, set[str]]) -> dict:
    """Totals and per-kind breakdown of the calls the stub has recorded so far."""
    with stub._lock:
        calls = list(stub.calls)
    chat = collections.defaultdict(lambda: {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0})
    emb = collections.defaultdict(lambda: {"calls": 0, "inputs": 0, "tokens": 0})
    for c in calls:
        if c.path.endswith("/chat/completions"):
            k = classify(c)
            chat[k]["calls"] += 1
            chat[k]["prompt_tokens"] += c.prompt_tokens
            chat[k]["completion_tokens"] += c.completion_tokens
        elif c.path.endswith("/embeddings"):
            kinds = set()
            for text in c.inputs:
                ns = labels.get(hashlib.sha256(text.encode("utf-8")).hexdigest())
                kinds.add("unlabelled" if not ns else next(iter(ns)) if len(ns) == 1 else "mixed")
            k = next(iter(kinds)) if len(kinds) == 1 else "mixed"
            emb[k]["calls"] += 1
            emb[k]["inputs"] += len(c.inputs)
            emb[k]["tokens"] += c.prompt_tokens
    return {
        "stub_summary": stub.summary(),
        "chat_by_kind": {k: dict(chat[k]) for k in CHAT_KINDS if k in chat},
        "embeddings_by_kind": {k: dict(emb[k]) for k in EMB_KINDS if k in emb},
    }


class WarnCounter(logging.Handler):
    def __init__(self) -> None:
        super().__init__(level=logging.WARNING)
        self.count = collections.Counter()

    def emit(self, record: logging.LogRecord) -> None:
        msg = re.sub(r"`[^`]*`|'[^']*'|\d+", "#", record.getMessage())[:70]
        self.count[f"{record.levelname}: {msg}"] += 1


# ---- worker ----------------------------------------------------------------------------------------------------
async def run_scenario(name: str, docs: list[dict], workdir: Path, calls_path: Path) -> dict:
    from stub_llm import Stub

    shape = SCENARIOS[name]
    responder = Responder(shape)
    started = utc_now()
    t0 = time.time()
    with Stub(responder, default_dims=1536) as stub:
        audit = Audit(stub._server.server_address[1])
        sys.addaudithook(audit.hook)
        # Tripwire self-test: a connect to the dead proxy port on loopback (nothing leaves the machine) must be
        # recorded, otherwise "no outbound attempt" below would mean nothing. Then the record is cleared.
        import socket

        with contextlib.suppress(OSError):
            socket.create_connection(("127.0.0.1", 9), timeout=1).close()
        tripwire_recorded = audit.connects.get("127.0.0.1:9", 0) >= 1
        audit.connects.clear()
        os.environ["OPENAI_API_BASE"] = stub.base_url
        os.environ["OPENAI_API_KEY"] = "dummy-not-a-key"
        warn = WarnCounter()
        logging.getLogger("lightrag").addHandler(warn)
        logging.getLogger("lightrag").setLevel(logging.WARNING)

        import lightrag
        from lightrag import LightRAG
        from lightrag.kg.nano_vector_db_impl import NanoVectorDBStorage
        from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed

        # Label the text of every vector write with the storage it goes to, so embedding inputs can be told apart
        # as chunks / entities / relationships. This only observes; the original method runs unchanged.
        labels: dict[str, set[str]] = collections.defaultdict(set)
        original_upsert = NanoVectorDBStorage.upsert

        async def labelled_upsert(self, data):
            for v in data.values():
                text = v.get("content")
                if isinstance(text, str):
                    labels[hashlib.sha256(text.encode("utf-8")).hexdigest()].add(self.namespace)
            return await original_upsert(self, data)

        NanoVectorDBStorage.upsert = labelled_upsert

        if workdir.exists() and any(workdir.iterdir()):
            # LightRAG answers a repeated prompt from its cache, so a reused directory would count zero calls.
            raise SystemExit(f"working directory {workdir} is not empty; use a clean --workroot")
        workdir.mkdir(parents=True, exist_ok=True)
        os.chdir(workdir)
        rag = LightRAG(
            working_dir=str(workdir / "rag_storage"),
            llm_model_func=gpt_4o_mini_complete,
            embedding_func=openai_embed,
        )
        config = {
            "chunk_token_size": rag.chunk_token_size,
            "chunk_overlap_token_size": rag.chunk_overlap_token_size,
            "entity_extract_max_gleaning": rag.entity_extract_max_gleaning,
            "force_llm_summary_on_merge": rag.force_llm_summary_on_merge,
            "summary_max_tokens": rag.summary_max_tokens,
            "summary_context_size": rag.summary_context_size,
            "llm_model_max_async": rag.llm_model_max_async,
            "max_parallel_insert": rag.max_parallel_insert,
            "embedding_batch_num": rag.embedding_batch_num,
            "embedding_func_max_async": rag.embedding_func_max_async,
            "entity_extraction_use_json": rag.entity_extraction_use_json,
            "enable_llm_cache": rag.enable_llm_cache,
            "enable_llm_cache_for_entity_extract": rag.enable_llm_cache_for_entity_extract,
            "tiktoken_model_name": rag.tiktoken_model_name,
            "llm_model_name": rag.llm_model_name,
            "chunking": "fixed-token (ainsert always uses it)",
        }
        await rag.initialize_storages()

        snapshots = {}
        per_document = []
        previous = measure(stub, labels)["stub_summary"]
        for i, doc in enumerate(docs, start=1):
            await rag.ainsert(doc["text"], ids=[f"doc-{doc['rank']:02d}"])
            m = measure(stub, labels)
            now = m["stub_summary"]
            per_document.append({
                "doc_rank": doc["rank"],
                "chars": len(doc["text"]),
                "chat_calls": now["chat_calls"] - previous["chat_calls"],
                "chat_prompt_tokens": now["chat_prompt_tokens"] - previous["chat_prompt_tokens"],
                "embedding_inputs": now["embedding_inputs"] - previous["embedding_inputs"],
            })
            previous = now
            if i in SNAPSHOT_AT:
                snapshots[str(i)] = {"documents": i, **m}
        await rag.finalize_storages()

        stub.dump_jsonl(str(calls_path))  # no text
        # What LightRAG stored: chunk and graph sizes, from the working directory (counts only).
        stored = {}
        for fname in ("kv_store_text_chunks.json", "vdb_chunks.json", "vdb_entities.json", "vdb_relationships.json"):
            p = workdir / "rag_storage" / fname
            if p.exists():
                data = json.loads(p.read_text(encoding="utf-8"))
                if fname.startswith("kv_store"):
                    stored["chunks"] = len(data)
                    stored["chunk_tokens_sum_lightrag_tokenizer"] = sum(int(v.get("tokens", 0)) for v in data.values())
                else:
                    stored[fname.removeprefix("vdb_").removesuffix(".json")] = len(data.get("data", []))
        graph = workdir / "rag_storage" / "graph_chunk_entity_relation.graphml"
        if graph.exists():
            xml = graph.read_text(encoding="utf-8")
            stored["graph_nodes"] = xml.count("<node ")
            stored["graph_edges"] = xml.count("<edge ")

        result = {
            "scenario": name,
            "shape": shape,
            "started_utc": started,
            "finished_utc": utc_now(),
            "wall_seconds": round(time.time() - t0, 1),
            "lightrag_version": __import__("importlib.metadata", fromlist=["version"]).version("lightrag-hku"),
            "config_as_constructed": config,
            "snapshots": snapshots,
            "per_document": per_document,
            "stored": stored,
            "responder_unclassified_calls": responder.unclassified,
            "lightrag_warning_counts": dict(warn.count),
            "outbound": audit.result(),
            "tripwire_selftest_recorded_a_connect_to_127.0.0.1:9": tripwire_recorded,
            "openai_api_base_was_set_to_stub": os.environ["OPENAI_API_BASE"].startswith("http://127.0.0.1:"),
            "dependency_versions": {
                d: __import__("importlib.metadata", fromlist=["version"]).version(d)
                for d in ("lightrag-hku", "openai", "tiktoken", "nano-vectordb", "networkx", "numpy", "tenacity", "pipmaster")
            },
            "calls_jsonl_sha256": hashlib.sha256(calls_path.read_bytes()).hexdigest(),
            "calls_multiset_sha256": multiset_hash(calls_path),
        }
    return result


def multiset_hash(calls_path: Path) -> str:
    """Order-free fingerprint of the calls: path, prompt hash, token counts. Equal for two runs that made the same calls."""
    rows = []
    for ln in calls_path.read_text(encoding="utf-8").splitlines():
        r = json.loads(ln)
        rows.append(f"{r['path']}|{r['prompt_sha256']}|{r['prompt_tokens']}|{r['n_inputs']}|{r['n_messages']}")
    return hashlib.sha256("\n".join(sorted(rows)).encode()).hexdigest()


def worker(args: argparse.Namespace) -> None:
    docs = load_documents(args.corpus, args.documents)
    workdir = Path(args.workroot) / args.worker
    calls_path = Path(args.workroot) / f"{args.worker}.calls.jsonl"
    result = asyncio.run(run_scenario(args.worker, docs, workdir, calls_path))
    Path(args.out).write_text(json.dumps(result, indent=1), encoding="utf-8")


# ---- driver ----------------------------------------------------------------------------------------------------
def compare(b1: dict, b2: dict) -> dict:
    out = {}
    for n in ("1", "5", "20"):
        s1, s2 = b1["snapshots"][n], b2["snapshots"][n]
        out[n] = {
            "stub_summary_equal_except_completion_tokens": all(
                s1["stub_summary"][k] == s2["stub_summary"][k]
                for k in s1["stub_summary"] if k != "chat_completion_tokens"),
            "chat_by_kind_equal": {k: v["calls"] for k, v in s1["chat_by_kind"].items()}
            == {k: v["calls"] for k, v in s2["chat_by_kind"].items()},
            "prompt_tokens_by_kind_equal": {k: v["prompt_tokens"] for k, v in s1["chat_by_kind"].items()}
            == {k: v["prompt_tokens"] for k, v in s2["chat_by_kind"].items()},
            "embeddings_by_kind_equal": s1["embeddings_by_kind"] == s2["embeddings_by_kind"],
        }
    out["calls_multiset_sha256_equal"] = b1["calls_multiset_sha256"] == b2["calls_multiset_sha256"]
    out["per_document_equal"] = b1["per_document"] == b2["per_document"]
    out["stored_equal"] = b1["stored"] == b2["stored"]
    return out


def driver(args: argparse.Namespace) -> None:
    workroot = Path(args.workroot)
    workroot.mkdir(parents=True, exist_ok=True)
    started = utc_now()
    results = {}
    for name in SCENARIOS:
        out_path = workroot / f"{name}.result.json"
        cmd = [sys.executable, "-I", str(Path(__file__).resolve()), "--worker", name, "--corpus", args.corpus,
               "--documents", args.documents, "--out", str(out_path), "--workroot", args.workroot]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        (workroot / f"{name}.stderr.txt").write_text(proc.stderr, encoding="utf-8")
        if proc.returncode != 0:
            raise SystemExit(f"scenario {name} failed with exit status {proc.returncode}; stderr is in "
                             f"{workroot / (name + '.stderr.txt')}")
        results[name] = json.loads(out_path.read_text(encoding="utf-8"))
    from stub_llm import make_counter

    summary = {
        "builder": "LightRAG",
        "package": "lightrag-hku",
        "version": results["B1"]["lightrag_version"],
        "python": sys.version.split()[0],
        "machine": __import__("platform").machine(),
        "system": __import__("platform").system(),
        "tokenizer_of_the_stub": make_counter()[0],
        "corpus_sha256": PINNED_CORPUS_SHA256,
        "documents": 20,
        "started_utc": started,
        "finished_utc": utc_now(),
        "scenarios": results,
        "determinism_B1_vs_B2": compare(results["B1"], results["B2"]),
    }
    Path(args.out).write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps(summary["determinism_B1_vs_B2"], indent=1))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus", required=True, help="MultiHop-RAG corpus.json (SHA-256 is checked)")
    ap.add_argument("--documents", required=True, help="documents.tsv listing the 20 documents by url")
    ap.add_argument("--out", required=True, help="result JSON to write")
    ap.add_argument("--workroot", required=True, help="scratch directory for the working directories and call dumps")
    ap.add_argument("--worker", choices=sorted(SCENARIOS), help="internal: run one scenario")
    args = ap.parse_args()
    for field in ("corpus", "documents", "out", "workroot"):  # the worker changes directory, so fix paths first
        setattr(args, field, str(Path(getattr(args, field)).resolve()))
    worker(args) if args.worker else driver(args)


if __name__ == "__main__":
    main()
