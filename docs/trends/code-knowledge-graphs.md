---
type: trend
shift: grep and file reads -> parsed code graphs
status: growing
order: 9
updated: 20261102 23:27 UTC
---

# Code graphs for coding agents: from grep and file reads to parsed code graphs

This page answers one question: should a coding [agent](../index/agent.md) be given a pre-built graph of a repository's functions, classes and calls, or is it enough to let it search the files? It covers six open-source projects and the research around them, set against [retrieval-augmented generation](../index/retrieval-augmented-generation.md) (RAG) over text, where a graph is also built. The projects are large and growing fast. Every saving they report was measured by their own authors, and whether the graph also gives better answers is still open.

> **Distinctive because** a parser, not a language model, builds the graph: five of the six projects use no [large language model](../index/large-language-model.md) (LLM) at index time [7][11][12][14][15][16]. The nearest neighbours are [agentic search](./agentic-search.md), where nothing is built, and [graph-based RAG](./graph-based-rag.md), where a model extracts the graph.

## Why it emerged

Coding agents usually find code by "repeated file-reading and grep-searching", which the authors of one tool say costs thousands of tokens per query without structural understanding [1]. A pre-built map is an older idea than these products. In October 2023 [Aider](https://github.com/Aider-AI/aider) described a repository map built with [tree-sitter](https://github.com/tree-sitter/tree-sitter) and cut to the token budget by a graph-ranking algorithm over file dependencies [2]. Research followed. CodexGraph (v1 20240807) put a graph database behind an agent, arguing that similarity retrieval "often has low recall in complex tasks" [3]. RepoGraph (v1 20241003) added a repository-level [code graph](../index/code-graph.md) as a plug-in module [4].

The products came in 2026. Of the six projects below, five were created between 20260118 and 20260403, and [Code-Graph-RAG](../projects/code-graph-rag.md) dates from 20250616 [5]. Why the wave came then is **unstated** in the sources read. The opposite design is also a deliberate product choice: Anthropic describes Claude Code as a hybrid: instruction files are loaded up front, while glob and [grep](../index/grep.md) fetch files "just-in-time, effectively bypassing the issues of stale indexing and complex syntax trees" [6]. For the retrieval background see the era [Language models meet retrieval](../history/language-models-meet-retrieval.md).

## Why it matters

- **Cost claims.** In agent runs the authors report 62% fewer tokens ([CodeGraph](../projects/codegraph.md)) and about 10 times fewer tokens ([codebase-memory-mcp](../projects/codebase-memory-mcp.md)) [7][8].
- **Adoption.** The snapshot flags four of the six as `fast-growth`, a heuristic of 150 or more stars a day averaged over the repository's life. Flags and stars are signals, not verdicts [5].
- **Research volume.** A keyword search finds 13 results in the window 20251102 to 20261102 against 1 in the year before. By title, only about 5 of the 13 are clearly about code graphs or code structure, and 2 more are borderline, so the ratio rests on a base of one and on a small, noisy count (queries in Sources). The same window shows LLM wording at x1.38 and LLM-agent wording at x2.50 [9][10].
- **The wider choice.** *Reading:* this is where the choice between building structure and searching at query time is easiest to test, because the baseline (grep) ships in the leading agents [6]. *Reading:* research on code graphs for agents looks early: few on-topic papers, none yet independent of the projects (see below) [9][24].

## How it works

Parse, store, serve. A parser such as [tree-sitter](../index/tree-sitter.md) turns each file into a syntax tree (what the projects call it varies; the [abstract syntax tree](../index/abstract-syntax-tree.md) entry records the naming). Extractors keep definitions and the relations between them: calls, imports, inheritance. A resolution pass links each call to its definition. codebase-memory-mcp adds type resolution above the tree-sitter pass, and Code-Graph-RAG adds compiler frontends and runtime traces where installed [11][12]. The graph sits in SQLite or a JSON file. The agent reaches it through the [Model Context Protocol](../index/model-context-protocol.md) (MCP), a command line or a skill, and asks for a symbol's source, its callers, or the files a change touches (its "blast radius", or [impact analysis](../index/impact-analysis.md)) [7][13]. Most keep it current with a file watcher or a git hook [7][14]. The agent's own model steers retrieval by choosing which tool to call. No trend is merged into this one.

| Project | Parses with | Stored as | Reached through | Models at build time |
|---|---|---|---|---|
| [Graphify](../projects/graphify.md) | tree-sitter, about 40 languages | `graph.json` | skill, command-line interface (CLI), MCP server | no LLM for code, and the README says "No embeddings, no vector store"; a model pass for documents, PDFs, images [14] |
| [Understand Anything](../projects/understand-anything.md) | tree-sitter, then model agents | JSON in `.ua/` | slash commands; README mentions no MCP | LLM: summaries, tags, layers, tours [15] |
| [CodeGraph](../projects/codegraph.md) | tree-sitter in a Rust kernel, 20 languages | SQLite | MCP, one tool | no LLM or embedding model described in the README; "No API keys" [7] |
| [codebase-memory-mcp](../projects/codebase-memory-mcp.md) | 162 vendored tree-sitter grammars | SQLite | 17 MCP tools, CLI | no generative model ("does not require a generative model"); bundled `nomic-embed-code` embeddings compiled into the binary for semantic search [11] |
| [code-review-graph](../projects/code-review-graph.md) | tree-sitter | SQLite | MCP, CLI, GitHub Action | no LLM described; optional vector embeddings, local or from a cloud API [16] |
| [Code-Graph-RAG](../projects/code-graph-rag.md) | tree-sitter, optional compiler frontends | SQLite; [Memgraph](../projects/memgraph.md) or [Neo4j](../projects/neo4j.md) opt-in | MCP, CLI | no LLM to build the graph; optional `semantic` extra (UniXcoder embeddings), part of the README's install command; plain-English questions call a model to write [Cypher](../index/cypher.md) [12] |

That last row links this trend to [Graph query generation](./graph-query-generation.md). Graphify also sells the same graph as agent memory and benchmarks it on memory suites, which links it to [Agent memory](./agent-memory.md) [14][20].

## Representative projects

Stars and flags are from the snapshot of 20261030 19:54 UTC [5]. Latest releases are GitHub's latest-release values, read 20261102 22:54 UTC, and are the values on the project pages [27]; the snapshot's own release column is older (v0.9.97 for Graphify, v0.4.5 for Code-Graph-RAG). Licences are from each `LICENSE` file, read 20261102 [7][11][12][14][15][16].

| Project | Stars | Created | Licence | Latest release | Snapshot flag |
|---|---|---|---|---|---|
| [Graphify](../projects/graphify.md) | 139,374 | 20260403 | Apache-2.0 | v0.9.101, 20261102 | fast-growth |
| [Understand Anything](../projects/understand-anything.md) | 89,048 | 20260315 | MIT | v2.9.0, 20260710 | fast-growth |
| [CodeGraph](../projects/codegraph.md) | 76,004 | 20260118 | MIT | v1.6.2, 20261003 | fast-growth |
| [codebase-memory-mcp](../projects/codebase-memory-mcp.md) | 47,853 | 20260224 | MIT | v0.12.1, 20261016 | fast-growth |
| [code-review-graph](../projects/code-review-graph.md) | 32,509 | 20260226 | MIT | v2.3.9, 20260918 | none |
| [Code-Graph-RAG](../projects/code-graph-rag.md) | 5,303 | 20250616 | MIT | v0.4.19, 20261101 | none |

Graphify moved from MIT to Apache-2.0 on 20260722 [14]. Two smaller tools in the same snapshot fit the trend and have no page: [ripwire](https://github.com/redhat-et/ripwire) (a deterministic call graph; 2,495 stars) and [gortex](https://github.com/zzet/gortex) (1,948 stars); GitHub's licence field says Apache-2.0 for both, and their `LICENSE` files were not read [5][18]. This documentation's catalogue counts 28 of the snapshot's 552 active rows as code-graph projects, by hand tagging. The list of those 28 is not committed, so the count cannot be re-derived from the archive; it is **unstated** which rows they are [5]. The snapshot is a capped keyword search, so the count is a lower bound.

## Fundamental papers

The group is [Code graphs for coding agents](../papers/code-knowledge-graphs.md); it keeps CodexGraph and RepoGraph as fundamental, and the other candidates below are in its further reading. Candidates:

- Codebase-Memory (arXiv 2603.27277, 20260328): the system paper behind codebase-memory-mcp [1].
- CodexGraph (2408.03910) and RepoGraph (2410.14684): the 2024 origin of code graphs for LLM agents [3][4].
- Reliable Graph-RAG for Codebases (2601.08773): a parser-built graph against an LLM-built one [17].
- How Do Small Coding Agents Use Code Graphs and Embeddings? (2610.33958): the first study here of how agents use such tools [19].

## What is measured, and by whom

Every figure for the six projects below was produced by the project's own authors: all are first-party. None uses the same baseline.

| Source | Result | Baseline and task |
|---|---|---|
| Codebase-Memory paper [8] | answer quality 0.83 against 0.92; about 1,000 against 10,000 tokens a question; 2.3 against 4.8 tool calls | a file-reading and grep agent; 31 repositories, one per language; Claude Opus 4.6; graded by the first author |
| CodeGraph README [7] | 62% fewer tokens, 88% fewer tool calls, 44% lower cost; no quality score | with and without the tool; 7 repositories, one question each; median of 4 runs; Claude Opus 4.8; measured 20260805 |
| Graphify `BENCHMARKS.md` [20] | key-fact coverage 82.0% against 70.8%; about 140K tokens a query | grep and read baseline; 6 questions on one repository; Claude Opus 4.8; last updated 20260705 |
| code-review-graph README [16] | about 63x median token reduction; impact F1 0.69 (F1 balances precision and recall) | whole-corpus baseline, which the README calls "an upper bound no real agent pays"; ground truth taken from the same graph |
| Code-Graph-RAG `evals/` [12] | F1 0.957 against 0.789 for call-tuned grep | file-level callers on Django; a Python `ast` oracle; no agent |
| Graphify README banner [14] | "cut agent token spend by 80%", tied to a hosted product | method not found |

Understand Anything's README gives no savings figure [15]. CodeGraph also reports that its answers leave about 80% more retrieval context resident at the end of a session [7]. The Codebase-Memory paper lists its own limits: one model, one repository per language, static structure only, and 0.58 against 1.00 on macro-heavy C [8].

Research prototypes outside the six report their own methods, so they are first-party for those methods:

- **Small models.** Structured tools doubled grep-only accuracy for two small models on SWE-bench Verified (real software issues from GitHub projects). The gain peaks at 17 to 21 points at 1.7 to 4 billion parameters and falls to 4 to 5 points at 32 billion. Agents chain graph expansions in only 12 to 14% of episodes. One author [19].
- **Parser against model.** On one Java project (Shopizer) a deterministic tree-sitter graph scored the highest correctness, ahead of an LLM-built graph and a vector baseline, and was much cheaper to build. One author, 15 queries a repository [17].
- **Context policies.** With CodeNib's candidate-context policy an agent resolves 79 of 200 SWE-bench Verified tasks, against 66 for on-demand exploration and 56 for Aider's repository map [21].
- **Localisation.** LARGER (Lexically Anchored Repository Graph Exploration and Retrieval) gains 13.9 points of file-level Acc@5 (accuracy within the top five results) on LocBench, a localisation benchmark, over its strongest baseline, with tuned settings [22]; RepoAtlas gains 2.4 points of resolve rate on SWE-bench Verified [23].

Apart from the Codebase-Memory paper, written by the authors of codebase-memory-mcp, none of the other 19 of the 20 distinct arXiv records fetched for this page (title and abstract: 11 looked up by number, 13 query hits, 4 in both) names any of the six projects [1][9][24]. No record found here is an independent evaluation of one. The experiment [X4: a code graph against grep](../experiments/x4-code-graph-vs-grep.md) is built to test one of them on lookup questions. It is groundwork only: nothing has been run, so it adds no result yet [25].

## Assessment

*Reading:* the strengths are real but narrow. A parser-built graph has no LLM token cost at index time (the cost of the optional or bundled embeddings is **unstated**), runs locally, updates in place, and plugs into agents through MCP. The research hints that the gain is largest for small models [19] and that a parser-built graph can beat a model-built one on a Java project [17], but in [19] the graph tools mostly add name lookup and one hop. The weaknesses are in the evidence. All six sets of figures are first-party, and they compare different things: agent runs, whole-corpus ratios and one unexplained percentage. The only quality comparison against a file-reading baseline, from the Codebase-Memory paper, favours the baseline (0.83 against 0.92) [8]. Graphify's six-question result favours the graph, but at a size that cannot carry a conclusion [20]. The gain shrinks as models grow [19], and Anthropic describes Claude Code as a hybrid that navigates with glob and grep rather than a pre-built index [6]. The direction of travel is toward hosted features: Graphify Cloud, a CodeGraph platform waitlist and paid Code-Graph-RAG deployments are all on offer [7][12][14]. Whether the free graph survives as a commodity layer is not answered by any source read.

## Signals to watch

- An evaluation of any of the six by people who do not ship it.
- A quality score beside tokens for CodeGraph, code-review-graph or Graphify's built-in benchmark.
- The X4 result [25].
- A coding-agent vendor shipping a built-in code graph, or dropping grep-only navigation.
- Whether the small-model gain in [19] repeats on other benchmarks.
- The next snapshot: stars, the `fast-growth` flags, and the new October 2026 entrants.
- Licence or commercial changes, as with Graphify on 20260722 [14].

## Sources

The long evidence is in the archive: [code-knowledge-graphs](../../kb-kg/directions/code-knowledge-graphs.md) [26]. Every figure above was read again from the sources below on 20261102, except where a source line says it is carried from the archive, and except the count of 28 code-graph rows in source 5, which is a hand count recorded only in the catalogue.

1. https://arxiv.org/abs/2603.27277 : Codebase-Memory, Vogel and four co-authors, v1 20260328; abstract and the file-reading and grep quotation (read 20261102 20:10 UTC, via the arXiv API)
2. https://aider.chat/2023/10/22/repomap.html : Aider repository map with tree-sitter and graph ranking, 20231022 (read 20261102 20:12 UTC)
3. https://arxiv.org/abs/2408.03910 : CodexGraph, Liu, Lan, Hu and five more, v1 20240807 (read 20261102 20:10 UTC)
4. https://arxiv.org/abs/2410.14684 : RepoGraph, Ouyang, Yu, Ma and six more, v1 20241003 (read 20261102 20:10 UTC)
5. kb-kg/landscape/20261030_1954-github/repos.tsv and README.md of the same folder : snapshot of 20261030 19:54 UTC; stars, creation dates, flags (`fast-growth` is stars a day of 150 or more), licence fields, 552 active rows, capped keyword search (read 20261102 20:11 UTC); the count of 28 code-graph rows is a hand tagging recorded only as a number in this documentation's catalogue (plans/20261102_1951-docs-catalogue.md, trend 9); the row list is **unstated**
6. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents : Anthropic, published 20250929; "Claude Code is an agent that employs this hybrid model": instruction files loaded up front, glob and grep just-in-time (read 20261102 20:37 UTC)
7. https://github.com/colbymchenry/codegraph : repository API, `LICENSE` (MIT), README: one tool, "No API keys", no LLM or embedding model mentioned in the README, file watcher, benchmark and methodology, context note, platform waitlist (read 20261102 20:11 to 20:15 UTC; the model and embedding check was made again 20261102 20:35 UTC)
8. https://arxiv.org/html/2603.27277v1 : Table 6, single backend Claude Opus 4.6, grading by the first author, threats to validity, 0.58 on macro-heavy C (read 20261102 20:13 UTC)
9. https://export.arxiv.org/api/query : 13 results for `(abs:"code graph" OR abs:"code graphs" OR abs:"repository graph" OR abs:"code knowledge graph" OR abs:"call graph") AND (abs:"coding agent" OR abs:"coding agents" OR abs:"code agent" OR abs:"code agents" OR abs:"software engineering agent")` submitted 20251102 to 20261102, 1 result for 20241102 to 20251101; keyword hits; by title, 5 of the 13 are clearly about code graphs or code structure and 2 more are borderline (reading of titles, made on the hits fetched 20261102 20:10 UTC); the two counts were run again 20261102 20:51 and 20:52 UTC with the same results (13 and 1)
10. https://export.arxiv.org/api/query : growth controls, counts of `totalResults`, same windows as source 9 (`submittedDate:[202511020000 TO 202611022359]` against `submittedDate:[202411020000 TO 202511012359]`). (a) any LLM wording `(abs:LLM OR abs:LLMs OR abs:"large language model" OR abs:"large language models")`: 44,692 against 32,396 (x1.38). (b) LLM-agent wording `(abs:agent OR abs:agents OR abs:agentic) AND (abs:LLM OR abs:LLMs OR abs:"language model" OR abs:"language models")`: 15,158 against 6,068 (x2.50). Both pairs were run again for this page: (a) 20261102 20:53 and 20:58 UTC, (b) 20:53 and 20:48 UTC. The first counts of both pairs (19:46 to 19:47 UTC) came from this documentation's catalogue and were not used as sources. The count of 13 against 1 in source 9 was run again 20:51 and 20:52 UTC.
11. https://github.com/DeusData/codebase-memory-mcp : repository API, `LICENSE` (MIT), README: 17 MCP tools, 162 grammars, type resolution, "does not require a generative model", semantic search by bundled `nomic-embed-code` embeddings compiled into the binary, no API key (read 20261102 20:11 to 20:15 UTC; the model and embedding lines were read again 20261102 20:35 UTC)
12. https://github.com/vitali87/code-graph-rag : repository API, `LICENSE` (MIT), README (SQLite default, MCP server, natural language to Cypher, cloud and on-premise offers, the `semantic` (vector search) extra in the install command), `docs/sdk/semantic-search.md` (UniXcoder embeddings, vectors in a SQLite file by default) and `evals/README.md` (F1 0.957 against 0.789) (read 20261102 20:11 to 20:15 UTC; the README's install lines and the semantic-search page were read 20261102 20:35 UTC)
13. https://github.com/tirth8205/code-review-graph/blob/staging/README.md : blast-radius analysis, incremental updates (read 20261102 20:11 UTC)
14. https://github.com/Graphify-Labs/graphify : repository API, `LICENSE` (Apache-2.0), README (tree-sitter, "no LLM" for code, "No embeddings, no vector store", model pass for documents, hooks, banner, Graphify Cloud), the relicence commit of 2026-07-22 22:50 UTC (read 20261102 20:11 to 20:14 UTC; the model and embedding lines were read again 20261102 20:35 UTC)
15. https://github.com/Egonex-AI/Understand-Anything : repository API, `LICENSE` (MIT), README: tree-sitter and model agents, `.ua/`, no MCP mention, no savings figure (read 20261102 20:11 to 20:15 UTC)
16. https://github.com/tirth8205/code-review-graph : repository API, `LICENSE` (MIT), README: 63x median, "upper bound", F1 0.69, "Optional vector embeddings" from sentence-transformers or cloud embedding APIs (read 20261102 20:11 to 20:15 UTC; the embedding lines were read again 20261102 20:34 UTC)
17. https://arxiv.org/abs/2601.08773 : Reliable Graph-RAG for Codebases, Chinthareddy (one author), v1 20260113 (read 20261102 20:10 UTC)
18. https://github.com/redhat-et/ripwire, https://github.com/zzet/gortex, https://github.com/tree-sitter/tree-sitter and https://github.com/Aider-AI/aider : repository API; the first two have licence field Apache-2.0; tree-sitter and Aider exist and are not archived (read 20261102 20:14 UTC)
19. https://arxiv.org/abs/2610.33958 : How Do Small Coding Agents Use Code Graphs and Embeddings?, Bellam (one author), v1 20261025 (read 20261102 20:10 UTC)
20. https://github.com/Graphify-Labs/graphify/blob/v8/BENCHMARKS.md : ERPNext result, harness, last updated 2026-07-05 (read 20261102 20:14 UTC)
21. https://arxiv.org/abs/2607.25431 : CodeNib, Yu, Yu, Yuan and 12 more, v1 20260728, v2 20260928; the 79, 66 and 56 figures are from the v2 abstract (read 20261102 20:37 UTC)
22. https://arxiv.org/abs/2605.16352 : LARGER, Hu, Su, Zhao and two more, v1 20260508 (read 20261102 20:10 UTC)
23. https://arxiv.org/abs/2609.16936 : RepoAtlas, Zhang, Wang, Guo and five more, v1 20260915 (read 20261102 20:10 UTC)
24. https://export.arxiv.org/api/query?id_list=2603.27277,2610.33958,2601.08773,2605.16352,2609.16936,2605.15184,2410.14684,2408.03910,2610.36153,2607.24882,2607.25431 : the 11 records looked up by number; no project name appears in any title or abstract (read 20261102 20:10 UTC)
25. docs/experiments/x4-code-graph-vs-grep.md : the X4 page; status: nothing run (read 20261102 20:13 UTC)
26. kb-kg/directions/code-knowledge-graphs.md : archive survey, used as a lead; its figures were re-checked above (archive page; its own read times are 20261030 19:56 to 19:58 UTC)
27. https://api.github.com/repos/OWNER/NAME/releases/latest (authenticated CLI; OWNER/NAME is each of Graphify-Labs/graphify, Egonex-AI/Understand-Anything, colbymchenry/codegraph, DeusData/codebase-memory-mcp, tirth8205/code-review-graph and vitali87/code-graph-rag) : latest release tag and date: v0.9.101 (2026-11-02 19:38 UTC), v2.9.0 (2026-07-10), v1.6.2 (2026-10-03), v0.12.1 (2026-10-16), v2.3.9 (2026-09-18), v0.4.19 (2026-11-01 20:01 UTC; git tags run ahead to v0.4.25) (read 20261102 22:52 to 22:54 UTC)
