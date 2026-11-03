---
type: project
repo: colbymchenry/codegraph
trends: [code-knowledge-graphs]
updated: 20261102 23:17 UTC
---

# CodeGraph

This page answers what CodeGraph is, how it builds and serves a [code graph](../index/code-graph.md), what its authors and others measured, and whether it is still moving. It sits in the trend [Code graphs for coding agents](../trends/code-knowledge-graphs.md). Unlike [Understand Anything](./understand-anything.md), its README describes no model at index or query time [4]; [Graphify](./graphify.md) and [codebase-memory-mcp](./codebase-memory-mcp.md) are its nearest neighbours.

| Field | Value |
|---|---|
| Repository | https://github.com/colbymchenry/codegraph |
| Licence | MIT, from the `LICENSE` file: the MIT text, 1,070 bytes, with one copyright line, "2026 Colby Mchenry" [2]. GitHub classifies it as MIT, and the README's licence section says MIT [2][4]. |
| Trends | [Code graphs for coding agents](../trends/code-knowledge-graphs.md) |

## What it is

CodeGraph is a local, pre-built index of a codebase's symbols and their relations, for coding [agents](../index/agent.md) [1]. It stores symbols and the calls, imports and inheritance between them in a SQLite database. It hands an agent the result through the [Model Context Protocol](../index/model-context-protocol.md) [4]. The installer names 18 agents it can wire up [4].

The README says "100% local", with no API keys. It also collects anonymous usage statistics, with an off switch [4].

*Reading:* the design bet is that one strong tool beats a menu. The MCP (Model Context Protocol) server lists a single tool, `codegraph_explore`; seven narrower ones are unlisted by default [4]. No [large language model](../index/large-language-model.md) is described at index or query time [4].

## How it works

Four steps [4]:

1. **Extract.** A native Rust kernel with built-in [tree-sitter](../index/tree-sitter.md) grammars parses 20 languages and pulls out functions, classes and methods and the calls, imports, extends and implements between them.
2. **Store.** Everything goes into `.codegraph/codegraph.db`, a SQLite file with FTS5 full-text search.
3. **Resolve.** A pass links calls to definitions, imports to files and framework routes to handlers, for 17 web frameworks.
4. **Sync.** A file watcher re-indexes after a 2-second quiet window by default.

One `codegraph_explore` call returns verbatim source grouped by file, the call paths between the symbols and a blast-radius summary, a form of [impact analysis](../index/impact-analysis.md) [4]. The command line adds `callers`, `callees`, `impact` and `affected` (the tests a change touches) [4]. The graph lives in SQLite, not in a graph database.

## Evidence

The README's results are first-party. The headline is the author's benchmark: seven open-source repositories, one architecture question each, Claude Code run headless on Claude Opus 4.8, median of 4 runs per arm, re-measured 20260805. The README says its harness blocks the project's own command line in both arms, because on an earlier unblocked harness the control arm used it in 26 of 28 runs [4].

| Codebase | Tool calls, with vs without | Cost, with vs without |
|---|---|---|
| VS Code | 2 vs 28 | $0.53 vs $1.80 |
| Excalidraw | 2 vs 43 | $0.54 vs $2.43 |
| Django | 3 vs 14 | $0.55 vs $0.63 |
| Tokio | 3 vs 29 | $0.66 vs $1.83 |
| OkHttp | 1 vs 6 | $0.39 vs $0.50 |
| Gin | 1 vs 7 | $0.31 vs $0.31 |
| Alamofire | 4 vs 33 | $0.54 vs $1.27 |

Averaged, the README reports 88% fewer tool calls, 62% fewer tokens and 44% lower cost, with zero file reads on all seven [4]. The saving varies with how much searching a question needs: 13% on Django, about even on Gin. The benchmark section reports no score for answer quality. The same README says its responses leave about 80% more retrieval context resident at the end of a session (67k tokens against 18k on VS Code) [4].

An earlier dated record in the repository (20260524, version 0.9.4, 37 cells, one run per arm) found file reads down from 159 to 38 and tool calls down from 321 to 189, but total cost marginally higher with the tool ($15.4 against $13.8) [5]. A September 2026 audit found that `main` had lost call relationships present in the 1.6.0 release; source-grounded paths passed 11 of 12 on the release, 9 of 12 on `main`, and 11 of 12 after repair [6].

### Outside the project

No peer-reviewed or arXiv evaluation of the tool was found. Two outside benchmarks and one user report were found. The first two come from authors of competing tools, and the first did not judge answer quality.

- **LemonCrow run.** The maintainer of LemonCrow ran CodeGraph as one arm of an exploration benchmark: seven repositories, five repetitions, Claude Opus 4.8, results dated 20260629. He posted it as an issue on CodeGraph's repository on 20260721 [12]. Cost was 16.3% lower overall, agent turns 84.1% lower and wall-clock time 22.7% higher. By repository, cost was lower on four, about even on Django, and higher on Tokio (+28.1%) and Gin (+24.9%). He did not record the version. The owner replied (first-party) that the run date matches v1.1.3, about fifteen releases behind the build current on 20260722, and that the control arm's parallel calls explain the wall-clock gap [12].
- **Codemesh README.** The competing tool Codemesh lists CodeGraph beside itself on six repositories with Claude Sonnet 4.6. An LLM (large language model) judge scored CodeGraph 8.4 of 10 against Codemesh's 7.9; average cost was $0.45 against $0.22 [13]. Who ran it and which CodeGraph version: **unstated**.
- **User report.** The owner's reply to a user's small-project test (about 100 files, on 20260519) gives 9 tool calls against 17 and more tokens with the tool. He agreed that token savings depend on size and cited Alamofire, in the README of that date, as the one case with more tokens (57.3k against 52.4k) [14]. The user's own screenshot was not read.

*Reading:* all three agree with the README that tool calls fall sharply. They differ on cost and time, which fits the README's own statement that the saving depends on how much searching a question needs.

Searches behind "none found" were few and are not exhaustive. An arXiv API query for the owner's account name returned 0 results (20261102 20:22) [11]; later arXiv queries were refused with HTTP 429. A search of the alphaXiv paper index for the tool's name (20261102 20:43) returned seven 2026 papers [15]. Four were read in full text and none evaluates the tool. One, by its title and abstract, describes a different system that shares the name. One, a paper on ontology-grounded project memory, uses the documentation of "CodeGraph, a third-party open-source developer tool" as a test corpus; the text read does not name the repository [15]. For research on code graphs see the [papers group](../papers/code-knowledge-graphs.md) and the trend page.

## Status and direction

Active. The latest release is v1.6.2, 20261003, 30 days before the read; v1.6.1 (20260929) and v1.6.0 (20260826) are the other two releases inside the 90 days since 20260804, and 33 releases exist in all [3]. The v1.6.2 notes lead with fewer wrong call links across languages and tell users to re-index [3].

In those 90 days, `main` took 1,068 commits: 179 in August, 283 in September, 570 in October and 36 in November. 953 carry two spellings of the copyright holder's name [2][7]. The contributors API lists 49 accounts [8]. 66 pull requests are open and 1,347 are merged; about 166 issues are open [1][8].

The changelog's unreleased section records a security fix: a link or alternate spelling could sidestep the refusal to index a sensitive system folder, so an agent's query could read files inside [9].

The snapshot of 20261030 19:54 UTC flags the repository `fast-growth`, a lifetime average of stars per day and not a trend; the [chapter page](./README.md) carries the counts and push dates [10].

The README announces a hosted product: "The CodeGraph platform is coming", for pull-request impact, with a waitlist [4]. Whether any feature will leave the MIT tool for it is **unstated**. Roadmap: **unstated**.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [code-review-graph](code-review-graph.md)
- [codebase-memory-mcp](codebase-memory-mcp.md)
- [Graphify](graphify.md)
- [Projects](README.md)
- [TencentDB Agent Memory](tencentdb-agent-memory.md)
- [Understand Anything](understand-anything.md)

**Experiments**

- [X1: Snapshot distributions](../experiments/x1-snapshot-distributions.md)

**Index**

- [Abstract syntax tree](../index/abstract-syntax-tree.md)
- [Code graph](../index/code-graph.md)
- [Impact analysis](../index/impact-analysis.md)
- [Taxonomy](../index/taxonomy.md)
- [Tree-sitter](../index/tree-sitter.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/colbymchenry/codegraph : repository metadata by `gh api` (description, created, archived, open issues and pull requests) (read 20261102 20:17 UTC)
2. https://github.com/colbymchenry/codegraph/blob/main/LICENSE : licence file by `gh api .../license`: MIT text, copyright line, size, GitHub classification (read 20261102 20:17 UTC)
3. https://github.com/colbymchenry/codegraph/releases : latest release v1.6.2 with its notes; the 33 releases and their dates (read 20261102 20:17 UTC)
4. https://github.com/colbymchenry/codegraph/blob/main/README.md : description, agents, MCP tools, architecture, benchmark and its methodology, context note, coverage table, telemetry, licence section, platform waitlist (read 20261102 20:17 UTC; re-read 20261102 20:42 UTC for the headline figures, the seven-repository table, the CLI-blocking note, the context note, telemetry, languages and framework counts, and the platform notice: all unchanged)
5. https://github.com/colbymchenry/codegraph/blob/main/docs/benchmarks/codegraph-ab-matrix.md : the 20260524 A/B matrix, version 0.9.4, headline and cost note (read 20261102 20:20 UTC)
6. https://github.com/colbymchenry/codegraph/blob/main/docs/benchmarks/regression-audit-2026-09.md : the audit of release 1.6.0 against `main`, path results (read 20261102 20:20 UTC)
7. https://github.com/colbymchenry/codegraph/commits/main : 1,068 commits since 20260804 by month and author name (counted again 20261102 20:44 UTC: same numbers, 24 merge commits)
8. https://github.com/colbymchenry/codegraph/pulls : open and merged pull request counts by the search API; contributor count by the contributors API (read 20261102 20:19 UTC)
9. https://github.com/colbymchenry/codegraph/blob/main/CHANGELOG.md : the `[Unreleased]` security entry (read 20261102 20:20 UTC)
10. kb-kg/landscape/20261030_1954-github/repos.tsv : the row for this repository, flag `fast-growth` (read 20261102 20:20 UTC)
11. https://export.arxiv.org/api/query?search_query=all:colbymchenry : 0 results (read 20261102 20:22 UTC); repeat and name queries at 20261102 20:41 to 20:47 UTC returned HTTP 429
12. https://github.com/colbymchenry/codegraph/issues/1393 : the LemonCrow benchmark tables and the owner's reply (read 20261102 20:42 UTC)
13. https://github.com/pyalwin/codemesh/blob/main/README.md : the Codemesh benchmark tables (cost, time, tool calls, LLM-judged quality), model, six repositories (read 20261102 20:41 UTC)
14. https://github.com/colbymchenry/codegraph/issues/185 : a user's small-project report and the owner's reply with the Alamofire figures (read 20261102 20:42 UTC)
15. https://www.alphaxiv.org/abs/2610.33958 and the papers arXiv 2609.29474, 2610.27524 and 2608.13662 (the last read from its 5-page PDF at https://arxiv.org/pdf/2608.13662) : alphaXiv discovery search for the tool's name, then full-text search of four papers for "CodeGraph" and the owner's account name: "How Do Small Coding Agents Use Code Graphs and Embeddings?" (2026), "CodeGraph: Open-Taxonomy Knowledge Graph for Source Code with Wikidata Grounding" (2026), "MemDev-Bench" (2026), "Ontology-Grounded Project Memory for Coding Agents" (2026) (read 20261102 20:43 UTC)
