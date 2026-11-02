"""X2 Step 0 rehearsal: Microsoft GraphRAG's indexing against a stub model. No key, no model, no outbound network.

Run it with the Python of the environment GraphRAG was installed into (the runner reads the installed package):

    ENV=$SCRATCH/microsoft-graphrag
    env -i PATH=/usr/bin:/bin:/opt/homebrew/bin HOME=$ENV/home \\
        $ENV/venv/bin/python -I tools/exp/x2_microsoft_graphrag.py \\
        --corpus $SCRATCH/exp-data/corpus.json \\
        --documents kb-kg/experiments/x2-index-cost/documents.tsv \\
        --workdir $ENV/work --tiktoken-cache $ENV/tiktoken_cache \\
        --out kb-kg/experiments/x2-index-cost/rehearsal/microsoft-graphrag.json

What it does. For each run it writes the first N documents of `documents.tsv` (body text from the corpus, one .txt
file each) into a fresh project directory, starts a loopback stub model server (`stub_llm.Stub`) with a responder that
answers in the format GraphRAG's prompts demand, and runs `graphrag index` (default settings, the Standard method) as
a child process. The child gets a minimal environment, a dummy key, the stub as its only model endpoint, an
HTTP(S)_PROXY that refuses connections, and, on macOS, a `sandbox-exec` profile that denies every outbound connection
except to loopback. Calls are then counted by kind from the stub's records.

GraphRAG indexes in batch (a corpus-level pipeline), so N = 1, 5 and 20 are three separate runs from clean directories.

One-time preparation, done by hand with network access and outside this runner: fill the tiktoken cache so the child
needs no download. In the same environment, with TIKTOKEN_CACHE_DIR set to the cache directory:
`python -c "import tiktoken; tiktoken.get_encoding('o200k_base'); tiktoken.get_encoding('cl100k_base')"`.

The article text goes only into the project directories under --workdir and the child's logs there. The JSON written
to --out holds counts, sizes and hashes of prompts, never text. The `hand_recorded` key of --out is kept across runs.

Standard library plus what the GraphRAG environment brings (pandas and pyarrow to count output rows, tiktoken).
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
import socketserver
import statistics
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

PINNED_CORPUS_SHA256 = "20b61b5ab84de84a927420c5d265b7ec8d859ae49980699958a787ade9e4d28f"
ENTITY_TYPES = ["organization", "person", "geo", "event"]  # GraphRAG's default entity_types
BLOCKING_PROXY = "http://127.0.0.1:9"
SANDBOX_PROFILE = (
    '(version 1)(allow default)(deny network-outbound (remote ip "*:*"))'
    '(allow network-outbound (remote ip "localhost:*"))'
)

# name -> (documents N, response shape, cache on, record outbound attempts with a sink proxy)
RUNS: dict[str, dict] = {
    "b-n1": dict(n=1, shape="B"),
    "b-n5": dict(n=5, shape="B"),
    "b-n20": dict(n=20, shape="B"),
    "a-n20": dict(n=20, shape="A"),
    "a2-n20": dict(n=20, shape="A2"),
    "b-n20-repeat": dict(n=20, shape="B"),
    "b-n20-nocache": dict(n=20, shape="B", cache=False),
    "b-n1-sink": dict(n=1, shape="B", sink=True),
    # the same 20 documents again, starting from the LLM cache that run b-n20 left behind
    "b-n20-rerun-cached": dict(n=20, shape="B", cache_from="b-n20"),
}

SHAPES = {
    "B": (
        "Per chunk the first answer holds 6 entities and 5 relationships; the gleaning answer adds none (it is just "
        "the completion marker); a loop-check answer is 'N'; a description summary is a fixed one-sentence text; a "
        "community report is a fixed-size JSON report with 5 findings. Entity names are the 6 capitalised words of "
        "the chunk with the smallest SHA-256, so chunks that share words share entities. Each entity's type is one of "
        "the 4 default types picked from the hash of its name, so a repeated name always has the same type. The 5 "
        "relationships chain the 6 entities in hash order, with a weight of 5 to 9 from the hash of the pair. Every "
        "description carries the chunk's SHA-256 prefix, so the same entity or pair seen in two chunks gets two "
        "different descriptions (which is what makes GraphRAG's summarisation step fire)."
    ),
    "A": (
        "Every extraction and gleaning answer is the bare completion marker: no entities, no relationships. The "
        "connectivity test answer is 'Hello World'."
    ),
    "A2": (
        "Supplementary, not the brief's shape A: every extraction answer is the same 2 entities and 1 relationship "
        "with identical descriptions (the smallest answer that lets this pipeline complete); the gleaning answer is "
        "the completion marker. Community reports are the same fixed-size JSON report as in shape B."
    ),
}


# ---- responders ---------------------------------------------------------------------------------------------------
def _h(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _chunk_of(prompt_text: str) -> str:
    m = re.search(r"-Real Data-\n#+\nEntity_types: .*?\nText: (.*)\n#+\nOutput:", prompt_text, re.S)
    if not m:
        raise ValueError("extraction prompt not in the expected shape")
    return m.group(1)


def _pick_entities(chunk: str, k: int = 6) -> list[str]:
    caps = sorted({t.upper() for t in re.findall(r"\b[A-Z][A-Za-z]{2,}\b", chunk)}, key=_h)
    if len(caps) < k:
        low = sorted({t.upper() for t in re.findall(r"\b[a-z]{4,}\b", chunk)} - set(caps), key=_h)
        caps += low[: k - len(caps)]
    return caps[:k]


def _record_entity(name: str, etype: str, desc: str) -> str:
    return f'("entity"<|>{name}<|>{etype}<|>{desc})'


def _record_rel(a: str, b: str, desc: str, w: int) -> str:
    return f'("relationship"<|>{a}<|>{b}<|>{desc}<|>{w})'


def _join(records: list[str]) -> str:
    # The prompt's own examples: "##" between records, the completion marker on its own line at the end.
    return "\n##\n".join(records) + "\n<|COMPLETE|>"


def extraction_answer_b(chunk: str) -> str:
    fp = _h(chunk)[:8]
    names = _pick_entities(chunk)
    recs = []
    for n in names:
        etype = ENTITY_TYPES[int(_h(n)[:8], 16) % 4]
        recs.append(_record_entity(n, etype, f"{n} is discussed in passage {fp}"))
    for a, b in zip(names, names[1:]):
        w = 5 + int(_h(a + "|" + b)[:8], 16) % 5
        recs.append(_record_rel(a, b, f"{a} and {b} are linked in passage {fp}", w))
    return _join(recs)


def extraction_answer_a2() -> str:
    return _join([
        _record_entity("ALPHA", "ORGANIZATION", "An entity"),
        _record_entity("BETA", "ORGANIZATION", "An entity"),
        _record_rel("ALPHA", "BETA", "A link", 5),
    ])


def community_report_answer(prompt_text: str) -> str:
    tag = _h(prompt_text)[:6]
    findings = [
        {"summary": f"Finding {i}", "explanation": "The community has a clear structure and its members are related. " * 2}
        for i in range(1, 6)
    ]
    return json.dumps({
        "title": f"Community {tag}",
        "summary": "This community groups related entities and describes how they connect to one another.",
        "rating": 5.0,
        "rating_explanation": "The impact is moderate because the members are loosely connected.",
        "findings": findings,
    })


class Classifier:
    """Names what a call is, from the installed package's own prompt constants."""

    def __init__(self) -> None:
        from graphrag.prompts.index.extract_graph import CONTINUE_PROMPT, LOOP_PROMPT

        self.continue_prompt = CONTINUE_PROMPT
        self.loop_prompt = LOOP_PROMPT

    def kind(self, call) -> str:
        from stub_llm import message_text

        if call.path.endswith("/embeddings"):
            if "This is an LLM Embedding Test String" in call.prompt_text:
                return "preflight_embedding_test"
            return "embedding"
        if not call.path.endswith("/chat/completions"):
            return "other"
        last = message_text(call.messages[-1]) if call.messages else ""
        text = call.prompt_text
        if last == self.continue_prompt:
            return "extract_gleaning_continue"
        if last == self.loop_prompt:
            return "extract_gleaning_loop_check"
        if "-Real Data-" in text and "Entity_types:" in text:
            return "extract_graph"
        if "Description List:" in text and "generating a comprehensive summary" in text:
            # the entity name is JSON-dumped: a string for an entity, a two-item list for a relationship
            is_pair = re.search(r"Entities: \[", text)
            return "summarize_description_relationship" if is_pair else "summarize_description_entity"
        if "Write a comprehensive report of a community" in text:
            return "community_report"
        if "This is an LLM connectivity test" in text:
            return "preflight_connectivity_test"
        return "other"


class Responder:
    def __init__(self, shape: str, classifier: Classifier) -> None:
        self.shape = shape
        self.classifier = classifier

    def __call__(self, call) -> str:
        kind = self.classifier.kind(call)
        if kind == "preflight_connectivity_test":
            return "Hello World"
        if kind == "extract_graph":
            if self.shape == "B":
                return extraction_answer_b(_chunk_of(call.prompt_text))
            if self.shape == "A2":
                return extraction_answer_a2()
            return "<|COMPLETE|>"
        if kind == "extract_gleaning_continue":
            return "<|COMPLETE|>"
        if kind == "extract_gleaning_loop_check":
            return "N"
        if kind.startswith("summarize_description"):
            return "A consolidated description of the entity, written in the third person."
        if kind == "community_report":
            return community_report_answer(call.prompt_text)
        return "OK"


# ---- outbound-attempt sink ----------------------------------------------------------------------------------------
class _Sink(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True
    attempts: collections.Counter


class _SinkHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        try:
            line = self.rfile.readline(4096).decode("latin-1").strip()
        except OSError:
            return
        parts = line.split(" ")
        method = parts[0] if parts else "?"
        target = parts[1] if len(parts) > 1 else "?"
        host = target.split("//", 1)[-1].split("/", 1)[0] if "://" in target else target
        self.server.attempts[f"{method} {host}"] += 1  # type: ignore[attr-defined]
        try:
            self.wfile.write(b"HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
        except OSError:
            pass


# ---- one run ------------------------------------------------------------------------------------------------------
def load_documents(corpus_path: Path, documents_tsv: Path) -> list[dict]:
    raw = corpus_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PINNED_CORPUS_SHA256:
        raise SystemExit("corpus.json does not match the pinned SHA-256")
    by_url = {a["url"]: a for a in json.loads(raw)}
    rows = [ln.split("\t") for ln in documents_tsv.read_text(encoding="utf-8").splitlines()
            if ln and not ln.startswith("#")]
    header, body = rows[0], rows[1:]
    url_col = header.index("url")
    docs = []
    for r in body:
        art = by_url[r[url_col]]
        docs.append({"rank": int(r[header.index("rank")]), "url_sha256_16": r[header.index("url_sha256_16")],
                     "chars": len(art["body"]), "body": art["body"]})
    return docs


def child_env(home: Path, tiktoken_cache: Path, proxy: str) -> dict[str, str]:
    env = {
        "PATH": "/usr/bin:/bin:/opt/homebrew/bin",
        "HOME": str(home),
        "GRAPHRAG_API_KEY": "dummy-not-a-key",
        "HTTP_PROXY": proxy, "HTTPS_PROXY": proxy, "http_proxy": proxy, "https_proxy": proxy,
        "NO_PROXY": "127.0.0.1,localhost", "no_proxy": "127.0.0.1,localhost",
        "TIKTOKEN_CACHE_DIR": str(tiktoken_cache), "CUSTOM_TIKTOKEN_CACHE_DIR": str(tiktoken_cache),
        "PYTHONUNBUFFERED": "1",
    }
    return env


def wrap(cmd: list[str], use_sandbox: bool) -> list[str]:
    if use_sandbox:
        return ["/usr/bin/sandbox-exec", "-p", SANDBOX_PROFILE, *cmd]
    return cmd


def make_project(run_dir: Path, template: Path, base_url: str, docs: list[dict]) -> None:
    if run_dir.exists():
        if not (run_dir / ".x2-run").exists():
            raise SystemExit(f"{run_dir} exists and was not made by this runner; not touching it")
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)
    (run_dir / ".x2-run").write_text("made by x2_microsoft_graphrag.py\n")
    shutil.copytree(template / "prompts", run_dir / "prompts")
    settings = (template / "settings.yaml").read_text(encoding="utf-8")
    settings, n_sub = re.subn(r"^(\s*)model_provider: openai\n", rf"\g<0>\1api_base: {base_url}\n", settings, flags=re.M)
    if n_sub != 2:
        raise SystemExit(f"expected to point 2 models at the stub, changed {n_sub}")
    (run_dir / "settings.yaml").write_text(settings, encoding="utf-8")
    (run_dir / "input").mkdir()
    for d in docs:
        (run_dir / "input" / f"{d['rank']:02d}.txt").write_text(d["body"], encoding="utf-8")


def sandbox_selftest() -> dict:
    """Prove the profile does what it claims: loopback connects, an address that is not loopback is refused at once.
    The second address is in the RFC 5737 documentation range, which no host answers, so even a failed block would
    send nothing useful; a block shows as EPERM, a missing block as a timeout."""
    import socket

    probe = (
        "import socket,sys\n"
        "s=socket.socket(); s.settimeout(3)\n"
        "try:\n"
        "    s.connect((sys.argv[1], int(sys.argv[2]))); print('connected')\n"
        "except Exception as e:\n"
        "    print(type(e).__name__, getattr(e, 'errno', None))\n"
    )
    srv = socket.socket()
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]
    out = {}
    for label, host, p in (("loopback", "127.0.0.1", port), ("non_loopback_documentation_address", "192.0.2.1", 443)):
        r = subprocess.run(wrap([sys.executable, "-I", "-c", probe, host, str(p)], True), capture_output=True,
                           text=True, timeout=30)
        out[label] = r.stdout.strip() or r.stderr.strip()[-120:]
    srv.close()
    out["blocks_non_loopback"] = out["non_loopback_documentation_address"].startswith("PermissionError")
    out["allows_loopback"] = out["loopback"] == "connected"
    return out


def stats_of(values: list[int]) -> dict:
    if not values:
        return {"n": 0}
    return {"n": len(values), "sum": sum(values), "min": min(values), "median": statistics.median(values),
            "max": max(values)}


def summarise_calls(stub, classifier: Classifier, tables: dict) -> dict:
    calls = list(stub.calls)
    kinds: dict[str, dict] = {}
    by_kind: dict[str, list] = collections.defaultdict(list)
    for c in calls:
        by_kind[classifier.kind(c)].append(c)
    for k, cs in sorted(by_kind.items()):
        kinds[k] = {
            "calls": len(cs),
            "prompt_tokens": stats_of([c.prompt_tokens for c in cs]),
            "completion_tokens_sum": sum(c.completion_tokens for c in cs),
        }
        if k == "embedding":
            kinds[k]["inputs"] = sum(len(c.inputs) for c in cs)
            kinds[k]["max_inputs_in_one_call"] = max(len(c.inputs) for c in cs)
    # Split embedding calls by field. Fields are embedded one after another, so cumulative inputs in arrival order
    # cut at the field boundaries; a boundary that falls inside a call would show as a mismatch.
    emb_rest = sorted(by_kind.get("embedding", []), key=lambda c: c.seq)
    fields = [(name, tables.get(key)) for name, key in (
        ("entity_description", "entities"), ("community_full_content", "community_reports"),
        ("text_unit_text", "text_units"))]
    split: dict[str, dict] = {}
    idx = 0
    ok = True
    for name, rows in fields:
        if rows is None:
            split[name] = {"calls": 0, "inputs": 0, "tokens": 0, "note": "table not written"}
            continue
        cs, got = [], 0
        while idx < len(emb_rest) and got < rows:
            cs.append(emb_rest[idx])
            got += len(emb_rest[idx].inputs)
            idx += 1
        if got != rows:
            ok = False
        split[name] = {"calls": len(cs), "inputs": got, "rows_in_table": rows,
                       "tokens": sum(c.prompt_tokens for c in cs)}
    if idx != len(emb_rest):
        ok = False
    if not emb_rest:
        ok = None  # the embedding step was never reached (the pipeline stopped earlier)
    digest = hashlib.sha256("\n".join(sorted(
        f"{classifier.kind(c)}|{c.prompt_tokens}|{hashlib.sha256(c.prompt_text.encode()).hexdigest()}"
        for c in calls)).encode()).hexdigest()
    return {"stub_summary": stub.summary(), "by_kind": kinds, "embedding_by_field": split,
            "embedding_split_matches_tables": ok, "unclassified_chat_calls": len(by_kind.get("other", [])),
            "call_multiset_sha256": digest}


def read_tables(run_dir: Path) -> dict:
    import pandas as pd

    out: dict = {}
    d = run_dir / "output"
    for name in ("documents", "text_units", "entities", "relationships", "communities", "community_reports"):
        p = d / f"{name}.parquet"
        if p.exists():
            out[name] = int(len(pd.read_parquet(p)))
    p = d / "communities.parquet"
    if p.exists():
        out["communities_by_level"] = {str(k): int(v) for k, v in pd.read_parquet(p).groupby("level").size().items()}
    if (d / "entities.parquet").exists() and (d / "relationships.parquet").exists():
        e, r = pd.read_parquet(d / "entities.parquet"), pd.read_parquet(d / "relationships.parquet")
        out["entities_seen_in_2_or_more_chunks"] = int((e["frequency"] >= 2).sum())
        out["relationships_seen_in_2_or_more_chunks"] = int((r["text_unit_ids"].map(len) >= 2).sum())
    if (d / "communities.parquet").exists() and (d / "entities.parquet").exists():
        c = pd.read_parquet(d / "communities.parquet")
        out["entities_in_a_level0_community"] = len({x for ids in c[c["level"] == 0]["entity_ids"] for x in ids})
    p = d / "text_units.parquet"
    if p.exists():
        tu = pd.read_parquet(p)
        out["chunk_tokens_o200k"] = stats_of([int(x) for x in tu["n_tokens"]])
        out["chunks_per_document"] = [int(x) for x in tu.groupby("document_id").size().sort_values().tolist()]
    p = d / "stats.json"
    if p.exists():
        s = json.loads(p.read_text())
        out["graphrag_stats"] = {"num_documents": s.get("num_documents"), "total_runtime_s": s.get("total_runtime"),
                                 "workflow_seconds": {k: round(v.get("overall", 0), 2) if isinstance(v, dict) else None
                                                      for k, v in (s.get("workflows") or {}).items()}}
    return out


def do_run(name: str, spec: dict, args, docs: list[dict], template: Path, classifier: Classifier, Stub) -> dict:
    run_dir = args.workdir / "runs" / name
    n, shape = spec["n"], spec["shape"]
    sink = None
    proxy = BLOCKING_PROXY
    if spec.get("sink"):
        sink = _Sink(("127.0.0.1", 0), _SinkHandler)
        sink.attempts = collections.Counter()
        threading.Thread(target=sink.serve_forever, daemon=True).start()
        proxy = f"http://127.0.0.1:{sink.server_address[1]}"
    t0 = time.time()
    started = datetime.now(timezone.utc).strftime("%Y%m%d %H:%M UTC")
    with Stub(Responder(shape, classifier), default_dims=3072) as stub:
        make_project(run_dir, template, stub.base_url, docs[:n])
        if spec.get("cache_from"):
            src = args.workdir / "runs" / spec["cache_from"] / "cache"
            if not src.exists():
                raise SystemExit(f"run {name} needs the cache of run {spec['cache_from']}; run that one first")
            shutil.copytree(src, run_dir / "cache")
        cmd = [str(args.graphrag), "index", "--root", str(run_dir)]
        if spec.get("cache") is False:
            cmd.append("--no-cache")
        home = args.workdir / "home"
        home.mkdir(exist_ok=True)
        with (run_dir / "run.log").open("wb") as log:
            proc = subprocess.run(wrap(cmd, args.sandbox), env=child_env(home, args.tiktoken_cache, proxy),
                                  stdout=log, stderr=subprocess.STDOUT, timeout=args.timeout)
        wall = time.time() - t0
        tables = read_tables(run_dir)
        result = summarise_calls(stub, classifier, tables)
        stub.dump_jsonl(str(run_dir / "calls.jsonl"))  # no text; stays under the work directory
    log_text = (run_dir / "run.log").read_text(errors="replace") + "\n" + (
        (run_dir / "logs" / "indexing-engine.log").read_text(errors="replace")
        if (run_dir / "logs" / "indexing-engine.log").exists() else "")
    errors = [ln.strip()[:200] for ln in log_text.splitlines() if "Graph Extraction failed" in ln][:1]
    result.update({
        "documents": n, "shape": shape, "cache": spec.get("cache", True), "started": started,
        "command": "graphrag index --root <fresh project directory>" + (" --no-cache" if spec.get("cache") is False else ""),
        "cache_started_from": spec.get("cache_from"),
        "exit_code": proc.returncode, "wall_seconds": round(wall, 1), "output_tables": tables,
        "known_error_line": errors[0] if errors else None,
        "proxy_or_connection_errors_in_logs": len(re.findall(r"ProxyError|Connection refused|ConnectError|APIConnectionError",
                                                             log_text)),
    })
    if sink is not None:
        sink.shutdown()
        sink.server_close()
        result["outbound_attempts_seen_by_sink_proxy"] = dict(sink.attempts)
    return result


def compare(a: dict, b: dict) -> dict:
    diffs = []
    for k in ("chat_calls", "chat_prompt_tokens", "chat_completion_tokens", "embedding_calls", "embedding_inputs",
              "embedding_tokens"):
        if a["stub_summary"][k] != b["stub_summary"][k]:
            diffs.append({k: [a["stub_summary"][k], b["stub_summary"][k]]})
    if a["by_kind"] != b["by_kind"]:
        diffs.append({"by_kind": "differs"})
    same_multiset = a["call_multiset_sha256"] == b["call_multiset_sha256"]
    return {"counts_and_tokens_identical": not diffs, "prompt_hash_multiset_identical": same_multiset, "differences": diffs}


def main() -> None:
    sys.dont_write_bytecode = True  # keep the repository free of .pyc files
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--corpus", type=Path, required=True)
    ap.add_argument("--documents", type=Path, required=True)
    ap.add_argument("--workdir", type=Path, required=True, help="scratch directory for projects and logs (not in the repository)")
    ap.add_argument("--tiktoken-cache", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--runs", default="all", help="comma-separated run names, or all: " + ",".join(RUNS))
    ap.add_argument("--no-sandbox", dest="sandbox", action="store_false", help="do not wrap the child in sandbox-exec")
    ap.add_argument("--timeout", type=int, default=1800)
    args = ap.parse_args()
    args.workdir = args.workdir.resolve()
    args.tiktoken_cache = args.tiktoken_cache.resolve()
    args.sandbox = args.sandbox and sys.platform == "darwin" and Path("/usr/bin/sandbox-exec").exists()
    args.graphrag = Path(sys.executable).parent / "graphrag"
    os.environ["TIKTOKEN_CACHE_DIR"] = str(args.tiktoken_cache)  # the stub's tokenizer must not download

    from stub_llm import Stub

    docs = load_documents(args.corpus, args.documents)
    if len(docs) != 20:
        raise SystemExit(f"expected 20 documents, found {len(docs)}")
    args.workdir.mkdir(parents=True, exist_ok=True)
    (args.workdir / "home").mkdir(exist_ok=True)

    # the project template: what `graphrag init` writes with its defaults
    template = args.workdir / "template"
    if not template.exists():
        r = subprocess.run([str(args.graphrag), "init", "--root", str(template), "--model", "gpt-4.1",
                            "--embedding", "text-embedding-3-large"],
                           env=child_env(args.workdir / "home", args.tiktoken_cache, BLOCKING_PROXY),
                           capture_output=True, timeout=300)
        if r.returncode != 0:
            raise SystemExit("graphrag init failed: " + r.stderr.decode(errors="replace")[-300:])

    classifier = Classifier()
    from graphrag.prompts.index import community_report, extract_graph, summarize_descriptions

    packaged = {"extract_graph.txt": extract_graph.GRAPH_EXTRACTION_PROMPT,
                "summarize_descriptions.txt": summarize_descriptions.SUMMARIZE_PROMPT,
                "community_report_graph.txt": community_report.COMMUNITY_REPORT_PROMPT}
    prompts_match = {k: (template / "prompts" / k).read_text(encoding="utf-8") == v for k, v in packaged.items()}
    names = list(RUNS) if args.runs == "all" else args.runs.split(",")
    measured: dict = {
        "runner": "tools/exp/x2_microsoft_graphrag.py",
        "graphrag_versions": {d: metadata.version(d) for d in (
            "graphrag", "graphrag-llm", "graphrag-chunking", "graphrag-cache", "graphrag-storage", "graphrag-vectors",
            "graphrag-input", "graphrag-common", "litellm", "openai", "tiktoken", "lancedb", "pandas", "numpy")},
        "python": platform.python_version(), "machine": platform.machine(), "system": platform.system(),
        "method": "standard (the default of `graphrag index`)",
        "settings": "the file `graphrag init --model gpt-4.1 --embedding text-embedding-3-large` writes, plus one "
                    "api_base line per model pointing at the stub",
        "template_settings_sha256": hashlib.sha256((template / "settings.yaml").read_bytes()).hexdigest(),
        "prompt_files_equal_packaged_constants": prompts_match,
        "document_input": "the `body` of each article, one .txt file each, in documents.tsv order, first N",
        "shapes": SHAPES,
        "child_isolation": {
            "env": "env whitelist: PATH, HOME (a scratch dir), a dummy GRAPHRAG_API_KEY, proxy variables, "
                   "TIKTOKEN_CACHE_DIR",
            "proxy": BLOCKING_PROXY + " (refuses connections), NO_PROXY=127.0.0.1,localhost",
            "os_level_network_block": ("sandbox-exec profile: deny every outbound connection except to loopback"
                                       if args.sandbox else "none (--no-sandbox or not macOS)"),
        },
        "runs": {},
    }
    if args.sandbox:
        measured["child_isolation"]["sandbox_selftest"] = sandbox_selftest()
        if not (measured["child_isolation"]["sandbox_selftest"]["blocks_non_loopback"]
                and measured["child_isolation"]["sandbox_selftest"]["allows_loopback"]):
            raise SystemExit("the sandbox profile does not behave as intended: " + json.dumps(measured["child_isolation"]))
    for name in names:
        print(f"run {name} ...", flush=True)
        measured["runs"][name] = do_run(name, RUNS[name], args, docs, template, classifier, Stub)
        r = measured["runs"][name]
        s = r["stub_summary"]
        print(f"  exit={r['exit_code']} chat={s['chat_calls']} prompt_tokens={s['chat_prompt_tokens']} "
              f"emb_inputs={s['embedding_inputs']} wall={r['wall_seconds']}s", flush=True)
    tk = {r["stub_summary"]["tokenizer"] for r in measured["runs"].values()}
    measured["stub_tokenizer"] = sorted(tk)
    if tk != {"tiktoken:cl100k_base"}:
        raise SystemExit(f"stub tokenizer fell back: {tk}")
    runs = measured["runs"]
    if "b-n20" in runs and "b-n20-repeat" in runs:
        measured["determinism_b_n20_vs_repeat"] = compare(runs["b-n20"], runs["b-n20-repeat"])
    measured["finished"] = datetime.now(timezone.utc).strftime("%Y%m%d %H:%M UTC")

    out: dict = {}
    if args.out.exists():
        out = json.loads(args.out.read_text())
    out["measured"] = measured
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print("wrote", args.out.name)


if __name__ == "__main__":
    main()
