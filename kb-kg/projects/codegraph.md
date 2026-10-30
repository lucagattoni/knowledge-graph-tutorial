---
slug: codegraph
repo: colbymchenry/codegraph
tier: card
category: adjacent
snapshot: 20261030 19:42 UTC
---

# CodeGraph

| | |
|---|---|
| Repository | https://github.com/colbymchenry/codegraph [1] |
| Licence | MIT, from the `LICENSE` file (head and tail read; copyright Colby Mchenry) [2]. The README badge and licence section also say MIT, so they agree [3]. |
| Language | TypeScript (GitHub primary language); the repository also holds a Rust kernel in `codegraph-kernel/` [1][6] |
| Stars, forks | 76,002, 5,025 (20261030 19:39 UTC; the landscape snapshot of 20261030 19:13 UTC has 75,999 and 5,025) [1][10] |
| Created, last push | 20260118 21:45 UTC, 20261030 19:31 UTC [1] |
| Latest release | v1.6.2, 20261003 06:41 UTC; 33 releases in all, v0.7.6 (20260513) to v1.6.2. `package.json` on `main` also says 1.6.2 [4][6]. |
| Status | active (pushed on the day of the read); not archived [1]. Snapshot flag `fast-growth`: 267.6 stars a day, a lifetime average over 284 days, so a heuristic and not a trend [10]. Context read live: 6.61 forks per 100 stars, 49 contributors on the contributors API (the snapshot lists 51), 169 open issues, 65 open and 1,272 merged pull requests [1][8][9][10]. The v1.6.2 notes and the README do not explain a launch [3][4]. This evidence does not show whether the star count is organic, and no conclusion is drawn. |
| Paper, docs | no paper stated; the README, a docs site at https://colbymchenry.github.io/codegraph/ (not fetched) and a `docs/` directory with benchmark notes [1][3][6] |

## What it is

CodeGraph is a local code-graph indexer for AI coding agents; its repository description reads "pre-indexed code knowledge graph, auto syncs on code changes" [1]. It stores symbols and the calls, imports and inheritance between them in a SQLite database, and gives Claude Code, Cursor, Codex, Gemini and five other agents a query interface through an MCP server [3]. The README reports its own benchmark (seven repositories, Claude Opus 4.8, median of four runs, 20260805): 88% fewer tool calls, 62% fewer tokens and 44% lower cost on average, and about 80% more retrieval context left resident afterwards [3]. I found no independent evaluation in the sources read [11]. The project says "100% local" and also collects anonymous usage statistics, which can be turned off [3][7].

## How it works

A native Rust kernel with built-in tree-sitter grammars extracts functions, classes and methods and the calls, imports, extends and implements between them for 20 languages; other languages use the same logic on a portable engine [3]. A resolution pass links calls to definitions, imports to files and framework routes to handlers [3]. Storage is SQLite with FTS5 search [3]. A file watcher re-syncs after a 2-second quiet window [3]. The README describes no LLM at index or query time and says no API keys are needed [3]. The MCP server lists one tool, `codegraph_explore`, which returns verbatim source, call paths and a blast-radius summary; seven narrower tools are unlisted by default [3].

## Status and direction

Active and fast-moving. Main received 999 commits from 20260801 to the read: 185 in August, 283 in September, 531 in October, 896 of them under the names Colby Mchenry (750) and Colby McHenry (146) [5]. The last release is 27 days old while commits continue daily [4][5]. The README announces a hosted "CodeGraph platform" for pull-request impact, with a waitlist [3]. A public roadmap: unstated.

## Sources

1. https://github.com/colbymchenry/codegraph : repository metadata via the GitHub API (read 20261030 19:39 UTC)
2. https://github.com/colbymchenry/codegraph/blob/main/LICENSE : MIT licence text, copyright line (read 20261030 19:42 UTC)
3. https://github.com/colbymchenry/codegraph/blob/main/README.md : description, benchmark, architecture, MCP tools, telemetry, licence section, platform announcement (read 20261030 19:39 UTC)
4. https://github.com/colbymchenry/codegraph/releases : 33 releases and the v1.6.2 notes (read 20261030 19:42 UTC)
5. https://github.com/colbymchenry/codegraph/commits/main : commits since 20260801, 999 confirmed by the pagination header (read 20261030 19:42 UTC)
6. https://github.com/colbymchenry/codegraph/tree/main : repository layout and the `package.json` version (read 20261030 19:42 UTC)
7. https://github.com/colbymchenry/codegraph/blob/main/TELEMETRY.md : anonymous usage statistics and how to turn them off (read 20261030 19:42 UTC)
8. https://github.com/colbymchenry/codegraph/pulls : pull request and issue counts via the search API (read 20261030 19:42 UTC)
9. https://github.com/colbymchenry/codegraph/graphs/contributors : contributor count via the contributors API (read 20261030 19:39 UTC)
10. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : first landscape snapshot row (snapshot 20261030 19:13 UTC)
11. [papers-benchmarks/README.md](../papers-benchmarks/README.md) : searched for the project name; no mention (searched 20261030 19:42 UTC)
