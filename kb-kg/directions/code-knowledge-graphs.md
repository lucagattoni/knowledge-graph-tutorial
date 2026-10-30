# Code knowledge graphs for coding agents

**In one paragraph.** Six projects build a graph of a codebase (and sometimes its documents) for coding agents to query: five were created between January and April 2026, and Code-Graph-RAG dates from June 2025. All six parse code with tree-sitter. Five build the code graph with no model; Understand Anything adds model-written summaries and tours, and Graphify adds a model pass for non-code files. Their savings claims run from 62% fewer tokens to ratios of 63x to 136.8x, against different baselines, and were measured by the projects' own authors (one third-party test covers a single lookup). Two sources compare answer quality with a file-reading baseline, and they point in opposite directions: the Codebase-Memory paper's quality is lower than its baseline's, and Graphify's six-question ERPNext coverage is higher. Star counts are large; they are unvetted signals.

## What the direction claims

**Claim (the projects' READMEs and paper).** An agent that explores code by reading files and grepping spends many tool calls and tokens re-deriving structure. A pre-built graph of symbols, calls, imports and inheritance, kept current by a file watcher, lets the agent ask one question and get the relevant source, call paths and the files a change would touch. The graph is built by a parser, so indexing costs no model tokens [codegraph](../projects/codegraph.md), [codebase-memory-mcp](../projects/codebase-memory-mcp.md), [code-review-graph](../projects/code-review-graph.md). The [llm-era note](../llm-era/README.md) files this under "Code graphs and the LLM wiki" (20260101 to 20260727) and lists "does a code graph beat grep for an agent" as an open question.

## Who is doing it

| Project | How it builds the graph, and how agents query it | Status at 20261030 | Evidence it works (and who measured it) |
|---|---|---|---|
| [Graphify](../projects/graphify.md) | Tree-sitter for code, no model. A model "semantic pass" for documents, PDFs and images, on the user's own assistant by default; `GRAPHIFY_BACKEND=none` leaves a code-only graph. A `/graphify` skill, a CLI and an MCP server over a NetworkX `graph.json`. | Active; v0.9.97 (20261027); Apache-2.0 since a relicence from MIT on 20260722; hosted Graphify Cloud. | The maintainer's own `BENCHMARKS.md`: on 6 ERPNext questions, key-fact coverage 82.0% against 70.8% for grep-and-read. One third-party test, one lookup on one repository. |
| [Understand Anything](../projects/understand-anything.md) | Tree-sitter for structure, then model agents add summaries, tags, layers and tours. Slash commands such as `/understand`; a JSON graph in `.ua/`; a read-only dashboard. The README does not mention MCP. | Active; v2.9.0 (20260710), MIT. | No paper. Its benchmark document runs no model and says it is not end-to-end. No savings figure in the README read. |
| [CodeGraph](../projects/codegraph.md) | A Rust kernel with tree-sitter grammars; SQLite with FTS5; no model at index or query time. MCP, with one listed tool, `codegraph_explore`. | Active; v1.6.2 (20261003), MIT; announces a hosted platform (waitlist). | The author's benchmark: 7 repositories, one question each. See the table below. |
| [codebase-memory-mcp](../projects/codebase-memory-mcp.md) | Native C pipeline; vendored tree-sitter plus a "Hybrid LSP" type step; SQLite; no generative model. 17 MCP tools, a Cypher subset, search by structure, BM25 and embeddings. | Active; v0.12.1 (20261016), MIT. | arXiv 2603.27277 (28 March 2026), by the system's developers. See the table below. |
| [code-review-graph](../projects/code-review-graph.md) | Tree-sitter into SQLite; a blast-radius walk finds the files a change touches. 30 MCP tools, a CLI and a GitHub Action that posts review comments. | Active; v2.3.9 (20260918), MIT; default branch `staging`. | The author's benchmarks on 6 repositories. See the table below. |
| [Code-Graph-RAG](../projects/code-graph-rag.md) | Tree-sitter, optional compiler frontends and runtime traces; embedded SQLite by default. 37 MCP tools: typed queries with no model, edit tools, and a natural-language-to-Cypher tool that does call a model. | Active; v0.4.5 (20261030), MIT; offers paid cloud and on-premise deployments. | The author's retrieval tests against grep, scored by a Python `ast` oracle: F1 0.957 against 0.789 on Django. The README says an end-to-end agent harness exists; no results are published. |

### Growth

| Project | Created | Stars (read 20261030) | Lifetime average a day | Snapshot flag | Commits on the default branch since 20260801 |
|---|---|---|---|---|---|
| Graphify | 20260403 | 139,363 | 663.6 | `fast-growth` | 1,297 |
| Understand Anything | 20260315 | 89,046 | 388.83 | `fast-growth` | 100 |
| CodeGraph | 20260118 | 76,002 | 267.6 | `fast-growth` | 999 |
| codebase-memory-mcp | 20260224 | 47,853 | 193.0 (my arithmetic; no snapshot row) | none | 2,810 |
| code-review-graph | 20260226 | 32,508 | 132.15 | none | 362 (to 20261015) |
| Code-Graph-RAG | 20250616 | 5,303 | 10.58 | none | 6,772 (many merge, bot and version commits) |

Sources: the [landscape snapshot](../landscape/20261030_1913-github/README.md) of 20261030 19:13 UTC and each entry. The flag is stars a day of 150 or more, a lifetime average and a heuristic. Only Graphify has dated outside counts: 7,311 stars about 20260407 and 63.2K on 20260608 [Graphify](../projects/graphify.md). Stargazer timestamps could not be read for Graphify or Code-Graph-RAG (HTTP 404), and none was sampled for the others. The entries draw no conclusion on how the stars arose, and neither does this page.

## Evidence for

**Measured, by the authors:** these are the savings claims, with the method each states.

| Source | Claim | Baseline and task | Method stated? | Answer quality reported? |
|---|---|---|---|---|
| Codebase-Memory paper [1][2] | About 10x fewer tokens (90% fewer; about 1,000 against 10,000 per question) and 2.1x fewer tool calls | A file-reading and grep agent; both on one model (Claude Opus 4.6); 31 repositories, one per language, 12 question categories | Yes, in the paper. Token counting and score aggregation are not explained. | Yes: 0.83 against 0.92 |
| CodeGraph README [3] | 62% fewer tokens, 88% fewer tool calls, 44% lower cost, averaged over 7 repositories | Claude Code run headless (Opus 4.8) with and without the MCP server; built-in Read, Grep and Bash kept; one architecture question per repository; median of 4 runs | Yes: arms, counting, questions and a block on the tool's own CLI are given | None in the section read |
| code-review-graph README [4] | About 63x median per-question token reduction (range 35x to 358x; 98.4% fewer, my arithmetic) | The whole corpus, with no agent run; 5 sample questions on 6 repositories | Yes: a formula and pinned commits | No. Impact F1 0.69 against ground truth taken from the same graph |
| Graphify [Graphify](../projects/graphify.md) | 71.5x per query; 136.8x and 83.6x from `graphify benchmark` | Reading every file; the built-in ratio uses an estimated token count | Yes for both. The docs call the baseline "an estimate, not a measured prompt" and say it measures tokens, not quality. | No |
| Graphify `BENCHMARKS.md`, ERPNext arm | About 140K tokens per query; key-fact coverage 82.0% against 70.8% | A fixed coding agent with grep and read; 6 questions; the grep arm's tokens are unstated | Partly | Yes: higher than the baseline |
| Graphify, README banner | "Cut agent token spend by 80%" (5x), tied to Graphify Cloud | Unstated | **No**: no method, baseline or measurer found | No |
| Understand Anything [6] | No savings figure in the README read | | | |

Two further results have a stated method. Code-Graph-RAG's graph finds the callers of a symbol with F1 0.957 on Django against 0.789 for call-tuned grep, on a test whose oracle the entry says favours name-based resolution [Code-Graph-RAG](../projects/code-graph-rag.md). A third-party run of Graphify on `httpx` measured 628 tokens for one `explain` against 13,659 to read the file [Graphify](../projects/graphify.md).

**Reading:** the figures fall into three kinds. Agent runs with and without the tool (the paper, CodeGraph) give 62% and 90% fewer tokens. Whole-corpus ratios with no agent (code-review-graph, Graphify's built-in benchmark) give 98% or more, against a baseline code-review-graph itself calls "an upper bound no real agent pays". One figure (80%) has no stated method. The kinds cannot be compared with each other, and the two quality comparisons differ in model, grader, task and size (31 repositories against 6 questions).

## Evidence against, or limits

- **No independent evaluation.** Every measurement above was made by the project that ships the tool; the paper calls the system "our implementation" [2], and the card for [codebase-memory-mcp](../projects/codebase-memory-mcp.md) records that a commit author sharing the first author's name wrote 2,145 of 2,810 commits since 20260801. A search for the paper's arXiv id and the six project names in [papers-benchmarks](../papers-benchmarks/README.md) and the [graph-RAG research note](../literature/graph-rag-research.md) found no match (searched 20261030 19:59 UTC).
- **The paper's quality figure is lower than its baseline's.** It reports 0.83 against 0.92. As read through a fetch tool, it also lists its own limits: one model, grading by the first author with thresholds "chosen pragmatically", one repository per language, static structure only, and a score of 0.58 against 1.00 on macro-heavy C [2]. Its README repeats the token and tool-call figures and does not state the quality figures [5].
- **Savings can come with a larger context footprint.** CodeGraph's README says its responses leave about 80% more retrieval context resident at the end of a session (67k tokens against 18k on VS Code), and that its earlier published figures were produced without a block on the tool's own CLI: on such a harness the control arm reached the CLI in 26 of 28 runs [3].
- **Baselines are contested.** The [llm-era note](../llm-era/README.md) records that Anthropic describes its own coding agent navigating by grep and glob, that Graphify advertises "Cut agent token spend by 80%", and that it read no independent measurement of either position.
- **The authors flag their own gaps.** code-review-graph says recall 1.0 is circular, its co-change mode returned no predictions in the 20260802 capture, and its formal `token_efficiency` benchmark gives ratios below 1 for small commits [4]. Graphify's built-in ratio moved from 11.0x to 1,893.5x on one graph when the benchmark was changed (a pull request description) [Graphify](../projects/graphify.md).
- **Build cost is not always zero.** Understand Anything warns that a first run can use many tokens [6]. One third-party run measured 1,533,913 tokens for Graphify's semantic build of its own repository (one run, one author) [Graphify](../projects/graphify.md).

## What is unresolved

- Whether an agent solves coding tasks better, not only cheaper, with a graph than with grep and glob. The llm-era note lists this as open question 5; the author-run results above do not settle it.
- Answer quality for CodeGraph, code-review-graph and Graphify's built-in ratios: unstated in the sources read.
- Whether results hold on models other than Opus 4.6 and 4.8: unstated.
- Language counts differ: the paper says 66 languages; the current README says 162, counted by vendored grammar directories, and 64 benchmarked repositories [2][5].
- Whether the star counts are organic: unchecked.

## Signals to watch

Each can be checked against a dated source.

- An evaluation of any of the six by someone other than its authors (search arXiv and [papers-benchmarks](../papers-benchmarks/README.md); today none).
- The codebase-memory-mcp README stating the 0.83 and 0.92 figures, or a revised paper (today the README states neither [5]).
- CodeGraph publishing a quality score beside its tokens (today none in the README section read [3]).
- code-review-graph publishing its first agent-baseline capture (the README of 20261030 says none exists [4]).
- Graphify publishing the method for "80% fewer tokens" (none in the entry's sources at 20261030), or the harness directories its `BENCHMARKS.md` names.
- Code-Graph-RAG publishing results from `evals/agentic_qa.py`.
- The next landscape snapshot: stars and flags against the 20261030 19:13 rows, and a row for codebase-memory-mcp.
- Licence or commercial changes: Graphify moved MIT to Apache-2.0 on 20260722; Graphify Cloud, a CodeGraph platform waitlist and Code-Graph-RAG's paid tiers were all announced by 20261030.

## Sources

Entries: [Graphify](../projects/graphify.md), [Understand Anything](../projects/understand-anything.md), [CodeGraph](../projects/codegraph.md), [codebase-memory-mcp](../projects/codebase-memory-mcp.md), [code-review-graph](../projects/code-review-graph.md), [Code-Graph-RAG](../projects/code-graph-rag.md). Context: [llm-era](../llm-era/README.md), [landscape snapshot](../landscape/20261030_1913-github/README.md) and [repos.tsv](../landscape/20261030_1913-github/repos.tsv).

1. https://arxiv.org/abs/2603.27277 : title, authors, abstract (read 20261030 19:56 UTC, through a fetch tool that summarises the page)
2. https://arxiv.org/html/2603.27277v1 : evaluation design, scoring, tokens, limitations (read 20261030 19:57 UTC, through the same summarising tool, so the figures here are second-hand and should be checked against the paper's tables; the PDF was unreadable to it)
3. https://github.com/colbymchenry/codegraph/blob/main/README.md : benchmark section and methodology (read 20261030 19:58 UTC)
4. https://github.com/tirth8205/code-review-graph/blob/staging/README.md : benchmarks and limitations (read 20261030 19:58 UTC)
5. https://github.com/DeusData/codebase-memory-mcp/blob/main/README.md : Performance and language sections (read 20261030 19:58 UTC)
6. https://github.com/Egonex-AI/Understand-Anything/blob/main/README.md and https://github.com/Egonex-AI/Understand-Anything/blob/main/docs/benchmarks/large-monorepo.md : token warning, no savings figure, benchmark scope (read 20261030 19:58 UTC)
