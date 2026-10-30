# Markdown files as the knowledge base

**In one paragraph.** Nineteen entries keep knowledge as files a person can read and edit (the MCP memory server, a JSONL file, and OpenViking, a virtual filesystem, are borderline), with an index derived from them and an agent interface, often MCP. Eight were created or repurposed between 20260404 and 20260408 after an "LLM wiki" gist; they and the others differ in who writes the files, what the index is, whether links are followed at query time, and how freely a person can edit. Every quality figure in the entries is first-party, and I found no independent evaluation of any project here. No entry shows where an index-only wiki stops working.

## What the direction claims

The gist says an LLM should "incrementally build and maintain a persistent wiki" between the user and the raw sources, so that knowledge is "compiled once and then kept current, not re-derived on every query". It has three layers (immutable sources, the wiki, a schema file such as `CLAUDE.md`) and three operations (ingest, query, lint). An `index.md` the model reads first "avoids the need for embedding-based RAG infrastructure" at "moderate scale (~100 sources, ~hundreds of pages)"; "as the wiki grows you want proper search", with no threshold given ([nashsu entry](../projects/llm-wiki-nashsu.md), quoting the gist; [timeline](../llm-era/README.md)).

The memory projects add claims. [Basic Memory](../projects/basic-memory.md) says Markdown is the source of truth and the database a rebuildable projection; [Tigerless](../projects/tigerless-agent-memory.md) says the same of its SQLite index. [OpenKnowledge](../projects/open-knowledge.md) says "the files are the database". [OKF](../projects/open-knowledge-format.md) says a bundle needs "no schema registry, no central authority, and no required tooling". The problems named: RAG "rediscovering knowledge from scratch on every question" (the gist), and, in the OKF Agent Memory README, a monolithic `AGENTS.md` or `CLAUDE.md` and facts in a vector database that agents never search ([timeline](../llm-era/README.md)).

## Who is doing it

| Project | How it takes this direction | Status at 20261030 | Evidence it works (and who measured) |
|---|---|---|---|
| [karpathy-llm-wiki](../projects/karpathy-llm-wiki.md) | Skill file for coding agents; `raw/` to `wiki/`, `index.md`, `log.md`; vector, graph and MCP deliberately not built | MIT; quiet since 20260723; no release; 2,643 stars | None measured. README claims a daily-used 94-article wiki (unchecked). Ships `check_evidence.py` |
| [llm-wiki-agent](../projects/llm-wiki-agent.md) | Skill plus Python scripts; agent reads index, then named pages; adds a graph view | MIT; pushed 20261026, last human commit 20260908; 3,667 stars | None |
| [obsidian-wiki](../projects/obsidian-wiki.md) | 39 Markdown skills; manifest so only changed sources are re-read; claim tags | MIT; 43 releases; 3,641 stars | Author's test, one 38-page vault: 83% correct with the skills, 44% without, two runs per cell ("indicative") |
| [claude-obsidian](../projects/claude-obsidian.md) | Claude Code plugin; sources to linked notes; local BM25; transaction layer for writes | MIT; v3.0.1; 16,002 stars | No benchmark; a `bench` command runs on the user's queries |
| [obsidian-mind](../projects/obsidian-mind.md) | Obsidian vault template with lifecycle hooks; `om` MCP server | MIT; v10.0.0; 5,460 stars | No benchmark; one author observation (see limits) |
| [llm-wiki (nashsu)](../projects/llm-wiki-nashsu.md) | Desktop app; two-step LLM ingest; keyword plus optional vector search; 12 MCP tools | GPL-3.0 (read-only reference); v0.6.13; 21,197 stars | README: recall 58.2% to 71.4% with vector search; no dataset or definition. No independent test |
| [llm-wiki-compiler](../projects/llm-wiki-compiler.md) | TypeScript compiler, SDK and MCP server; embeddings, BM25 and wikilink expansion | MIT; v1.5.0; 2,225 stars | No benchmark; `eval` scores wiki health and citations |
| [llmwiki (lucasastorian)](../projects/llmwiki-lucasastorian.md) | Web app, extension, MCP; Claude writes `wiki/` pages through ten tools; nightly fold-in suggested | Apache-2.0; no release; 1,734 stars | None |
| [OpenKB](../projects/openkb.md) | CLI compiles documents to a wiki; tree index for long PDFs; "No Vector DB" | Apache-2.0; quiet since 20260722; 4,831 stars | None |
| [OpenKnowledge](../projects/open-knowledge.md) | Markdown editor and 19-tool MCP server over git-tracked files | GPL-3.0 (read-only); v0.89.0; 4,741 stars | None |
| [Basic Memory](../projects/basic-memory.md) | Notes with observation and relation syntax; SQLite or Postgres index; 12 MCP tools | AGPL-3.0 (read-only); v1.0.0; 4,416 stars | Project's own benchmark vs mem0, grep and full context (see for/against); none independent |
| [agent-memory (Tigerless)](../projects/tigerless-agent-memory.md) | Model-written memory files; SQLite FTS5 cache; hooks, CLI, MCP; sleep-time consolidation | MIT; no release (0.1.0); 4,381 stars | Project's own LongMemEval-S variant; its first consolidation study "could not have measured" the effect |
| [KiwiFS](../projects/kiwifs.md) | Go server over a Markdown folder; every write validated and committed to git; 78 MCP tools | BSL 1.1 (read-only); v0.19.81; 870 stars | No benchmark |
| [EverOS](../projects/everos.md) | Markdown is the record; SQLite and LanceDB indexes derived; hand edits re-indexed | Apache-2.0; v1.5.1; 13,721 stars | README states none; a benchmark runner exists, results unstated |
| [OKF Agent Memory](../projects/okf-agent-memory.md) | Go tool and MCP server over OKF v0.2 bundles; in-memory BM25 | MIT; v0.7.2; 846 stars | Latency and token figures from one local-model run (project's own) |
| [Open Knowledge Format](../projects/open-knowledge-format.md) | Specification for a directory of Markdown files with YAML front matter | Apache-2.0; v0.2, no release; 1,177 stars | A format, not a tool; nothing measured |
| [MCP memory server](../projects/mcp-servers.md) | Not Markdown: one JSONL graph file; calling model decides what to store | Licence composite, memory server's own unstated; package 2.0.1; 91,700 stars (whole repository) | No benchmark; README calls the servers "educational examples" |
| [Letta](../projects/letta.md) | Agent edits a git repository of Markdown with ordinary file tools; no vector index in memory by default | Apache-2.0; old server retired 20260816; current code in `letta-code` | Letta's own LoCoMo and FrontierMemory posts; independent tests ran the legacy MemGPT |
| [OpenViking](../projects/openviking.md) | Virtual filesystem of `viking://` URIs; Markdown summaries per directory plus a vector index | AGPL-3.0 (read-only); v0.5.2.1; 41,196 stars | Project's own LoCoMo, tau2 and RAG figures; none independent found |

### Where they differ

| Axis | Variants found |
|---|---|
| Who writes | A model under a schema the host agent follows: karpathy-llm-wiki, llm-wiki-agent, obsidian-wiki, claude-obsidian, OpenKB, llmwiki. The project's own LLM pipeline: nashsu, llm-wiki-compiler. Mostly a background reasoner or engine: Tigerless, EverOS, OpenViking; Letta (the agent plus background "dreaming" subagents). Person and agent on the same files: Basic Memory, OpenKnowledge, obsidian-mind, KiwiFS |
| The index | An `index.md` the model reads: karpathy-llm-wiki, llm-wiki-agent. A derived search index (BM25, vectors or both): Basic Memory, Tigerless, EverOS, KiwiFS, nashsu, OpenKnowledge, claude-obsidian, llm-wiki-compiler, llmwiki. In-memory BM25: OKF Agent Memory. A summary tree: OpenKB, OpenViking. None by default: Letta |
| Links at query time | The engine follows them: nashsu (linked pages fill 15% to 30% of result slots), llm-wiki-compiler. A tool the agent calls: Basic Memory `bm_context` (depth 1 to 5), OpenKnowledge `links`. Stored, not followed in the code read: Tigerless, OpenViking. Others: unstated |
| Free editing | Stated design: Basic Memory, OpenKnowledge, EverOS (a watcher indexes hand edits). With limits: nashsu replaces a page that lists only a re-ingested source, edits included. Others: unstated |

## Evidence for

**Convergence.** Eight entries here were created, or in one case repurposed, from 20260404 to 20260408 (creation dates in each entry; see also the [timeline](../llm-era/README.md)). Two products moved toward files. Letta retired its Python server on 20260816 and now keeps memory as a git repository of Markdown ([Letta](../projects/letta.md)). EverOS 1.0.0 (20260606) dropped MongoDB, Elasticsearch, Milvus, Redis and Kafka ([EverOS](../projects/everos.md)). **Reading:** this shows where builders are moving, not that the result retrieves better.

**Retrieval, measured by the authors.**
- Basic Memory, internal benchmark: LongMemEval recall@5 0.951, against 0.979 for mem0 and 0.846 for grep; answer accuracy 0.583, 0.450, 0.333, and 0.217 for full context. On ConvoMem, full context (0.799) beat Basic Memory (0.755) ([entry](../projects/basic-memory.md)).
- Tigerless, LongMemEval-S cut to 12 sessions: 52.9% against 35.8% for another system and 5.8% with no memory (its README says the cut makes the numbers not comparable to published LongMemEval scores). Adding vector fusion raised Recall@5 from 79.0% to 86.6% but median latency from 5.1 ms to 139.2 ms ([entry](../projects/tigerless-agent-memory.md)).
- Letta's post of 20250812: 74.0% on LoCoMo for an agent with file tools, against 68.5% that Mem0 reported; Letta did not rerun Mem0's figure ([entry](../projects/letta.md)).

**Context from outside these projects.** One 2026 study found BM25 ahead of dense and graph retrieval from 1,144 to 511,959 documents on a synthetic enterprise corpus, and another found raw retrieval over raw history first in six of seven settings ([papers and benchmarks](../papers-benchmarks/README.md)). **Reading:** plain retrieval without extracted structure was a strong baseline in both studies; one used a synthetic corpus, and the other is an abstract-only entry. Neither tested a wiki an LLM had compiled.

**Safeguards the entries describe** (read in code or docs, not run). [nashsu](../projects/llm-wiki-nashsu.md) rejects a merged page under 70% of the longer input. [claude-obsidian](../projects/claude-obsidian.md)'s README describes a hash, plan, apply and rollback write layer. [KiwiFS](../projects/kiwifs.md) commits every write to git. [Basic Memory](../projects/basic-memory.md) refuses tool writes to a `locked: true` note (a direct file edit overrides it). [Tigerless](../projects/tigerless-agent-memory.md) has two memory-poisoning test files.

## Evidence against, or limits

**Quality.**
- No entry reports an independent run. Letta's outside evaluations ran the legacy MemGPT, not Letta Code: MemoryAgentBench scored MemGPT 28.3 overall, against 42.2 for long-context GPT-4o-mini and 41.5 for BM25 ([Letta](../projects/letta.md)).
- Tigerless's own ledger puts one system between 48.3% and 66.7% across seven configurations and calls rows closer than about seven answers "not distinguishable". Its experiment files were untracked on 20260908, so the README's numbers cannot be checked in the current tree ([entry](../projects/tigerless-agent-memory.md)).
- Basic Memory's benchmark file calls itself "internal-only"; mem0 ran with `infer=false` and the answerer model was small ([entry](../projects/basic-memory.md)).
- nashsu's README is older than its code in six places the entry lists ([entry](../projects/llm-wiki-nashsu.md)).

**Scale.** The gist gives no threshold. nashsu's keyword scan stops at 10,000 files; a user with a 50 GB repository reported a very long load at each start, the maintainer said he would think about optimising, and no later comment follows up ([entry](../projects/llm-wiki-nashsu.md)). Tigerless compares vectors in Python and does not state the corpus behind its latency figure. Letta's code defaults to 65,536 characters of core memory, and hosted repositories are capped at 5 MiB (Free) or 50 MiB (Pro) ([entry](../projects/letta.md)). obsidian-wiki's test used 38 pages. Fourteen of the nineteen repositories were created in 2026, and no entry reports a long-run measurement.

**Safety.**
- The obsidian-mind author reports one session with the MCP server wired but no instruction in the calling repository: it made no vault calls and built a design the vault had recorded as rejected ([entry](../projects/obsidian-mind.md)).
- Tigerless archived bare provider keys verbatim until a fix merged 20261029; another closed issue was an import that could write outside the store. The entry also notes a tension between the README ("deletion only ever arrives as a proposal you confirm") and code that applies an accepted delete verdict during a sleep, which ends validity but keeps the file ([entry](../projects/tigerless-agent-memory.md)).
- Letta's optional second review conversation does not ask the user for approval; its prompt tells the agent not to write secrets to memory because the repository syncs ([entry](../projects/letta.md)).
- Basic Memory's HTTP transports have no authentication and bind to `127.0.0.1` by default ([entry](../projects/basic-memory.md)). KiwiFS's latest changes include S3 and WebDAV auth enforcement ([entry](../projects/kiwifs.md)).
- OKF's v0.2 text changed on 20260820 without a version bump; OKF Agent Memory claims full compliance but its entry finds two gaps ([OKF](../projects/open-knowledge-format.md), [OKF Agent Memory](../projects/okf-agent-memory.md)).

## What is unresolved

1. At what size does an index-only wiki stop working? ([timeline](../llm-era/README.md), question 3.)
2. Does an LLM-compiled wiki answer better than plain retrieval over the same sources? No entry compares them.
3. Does following links improve answers? Two projects store links without following them; two follow them; no entry I read reports an ablation.
4. What happens to a person's edit when the model re-ingests or consolidates? Documented for nashsu (re-ingest replaces the page) and Basic Memory (a lock stops tool writes, not file edits); unstated in the other entries read.
5. Do agents use the memory unprompted? The obsidian-mind observation is one case; OKF Agent Memory ships a "search before write" convention aimed at it.
6. Does consolidation help over months? Tigerless's first test could not tell.
7. Is OKF one format? Whether OpenViking's "OKF Markdown" is the same OKF is unstated ([OpenViking](../projects/openviking.md)); no standards body is named ([OKF](../projects/open-knowledge-format.md)).

## Signals to watch

- A third-party run of any project here on LongMemEval, LoCoMo or MemoryAgentBench, listed on the [papers and benchmarks](../papers-benchmarks/README.md) page after 20261030.
- A size sweep of an index-only wiki with a fixed question set.
- A dataset and definition for nashsu's 58.2% to 71.4% recall figure; any commit to its `main` after 20261021.
- Basic Memory results labelled 1.0; its docs say earlier results "should not be relabeled" as 1.0.
- Tigerless: a first GitHub release, restored experiment files, or a longitudinal consolidation study.
- EverOS: a 1.6.0 tag (main records it dated 20261028; no tag at 20261030 19:45 UTC).
- OKF: a release or version bump, or a named governing body.
- Any evaluation of Letta Code memory, or a reproduction of FrontierMemory.
- Whether karpathy-llm-wiki (last push 20260723) and OpenKB (20260722) resume.

## Sources

Entries: [karpathy-llm-wiki](../projects/karpathy-llm-wiki.md), [llm-wiki-agent](../projects/llm-wiki-agent.md), [obsidian-wiki](../projects/obsidian-wiki.md), [claude-obsidian](../projects/claude-obsidian.md), [obsidian-mind](../projects/obsidian-mind.md), [llm-wiki-nashsu](../projects/llm-wiki-nashsu.md), [llm-wiki-compiler](../projects/llm-wiki-compiler.md), [llmwiki-lucasastorian](../projects/llmwiki-lucasastorian.md), [openkb](../projects/openkb.md), [open-knowledge](../projects/open-knowledge.md), [basic-memory](../projects/basic-memory.md), [tigerless-agent-memory](../projects/tigerless-agent-memory.md), [kiwifs](../projects/kiwifs.md), [everos](../projects/everos.md), [okf-agent-memory](../projects/okf-agent-memory.md), [open-knowledge-format](../projects/open-knowledge-format.md), [mcp-servers](../projects/mcp-servers.md), [letta](../projects/letta.md), [openviking](../projects/openviking.md).

Context pages: [LLM-era timeline](../llm-era/README.md), [papers and benchmarks](../papers-benchmarks/README.md). No new URLs were fetched for this page.
