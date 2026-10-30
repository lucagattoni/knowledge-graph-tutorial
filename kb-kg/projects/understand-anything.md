---
slug: understand-anything
repo: Egonex-AI/Understand-Anything
tier: card
category: adjacent
snapshot: 20261030 19:41 UTC
---

# Understand Anything

| | |
|---|---|
| Repository | https://github.com/Egonex-AI/Understand-Anything [1] |
| Licence | MIT, from the `LICENSE` file (head and tail read; copyright Yuxiang Lin and Infinite Universe, Inc.) [2]. The README badge and footer also say MIT, so they agree [3]. |
| Language | TypeScript (GitHub primary language) [1] |
| Stars, forks | 89,046, 7,545 (20261030 19:39 UTC; the landscape snapshot of 20261030 19:13 UTC has 89,043 and 7,545) [1][10] |
| Created, last push | 20260315 02:30 UTC, 20261026 07:05 UTC [1] |
| Latest release | v2.9.0, 20260710 09:36 UTC; eight releases in all, v1.2.0 (20260325) to v2.9.0 [4]. The plugin manifest and `package.json` on `main` say 2.9.8, which has no release [6]. |
| Status | active (pushed 4 days before the read); not archived [1]. Snapshot flag `fast-growth`: 388.83 stars a day, a lifetime average over 229 days, so a heuristic and not a trend [10]. Context read live: 8.47 forks per 100 stars, 64 contributors on the contributors API (the snapshot lists 75; the gap is unexplained), 126 open issues, 211 open and 139 merged pull requests [1][8][9][10]. The README shows a Trendshift badge; the v2.9.0 notes do not mention a launch [3][4]. This evidence does not show whether the star count is organic, and no conclusion is drawn. |
| Paper, docs | no paper stated; the README, the homepage https://understand-anything.com/ (not fetched) and a `docs/` directory with a benchmark protocol and incremental-update audits [1][3][7] |

## What it is

Understand Anything describes itself as a way to turn any codebase, knowledge base or docs into an interactive knowledge graph that you can explore, search and ask questions about [1][3]. It is a Claude Code plugin; its compatibility table lists 16 other platforms, among them Codex, Cursor, Copilot and Gemini CLI [3]. The graph is a JSON file in a `.ua/` directory that a team can commit, and a read-only dashboard opens it without an LLM [3]. Besides code it has modes for business-domain flows, Karpathy-pattern LLM wikis and, since v2.9.0, Figma files [3][4]. For a graph kept in a database and queried by tools, see the deeper entry on [Code-Graph-RAG](code-graph-rag.md).

## How it works

Tree-sitter parses files deterministically into imports, definitions, calls and inheritance; LLM agents then add summaries, tags, architectural layers, domain mapping and guided tours [3]. The README lists seven agents, such as `project-scanner`, `file-analyzer` and `graph-reviewer`; the repository holds ten agent files, including a `design-analyzer` [3][6]. File analysis runs in parallel batches, and re-runs touch only changed files [3]. The schema has 27 node types and 38 edge types [6]. The agent interface is slash commands such as `/understand` and `/understand-chat`; the README does not mention MCP [3]. It warns that a first run can use many tokens on a large project [3].

## Status and direction

Active. Main received 100 commits from 20260801 to 20261026 (6 in August, 76 in September, 18 in October; 66 under the name Lum1104) [5]. The last release is 112 days before the read; v2.9.0 added the Figma mode, Dart, Scala, Swift and Kotlin support, and more platforms [4]. 211 pull requests are open [8]. Roadmap: unstated [3].

## Sources

1. https://github.com/Egonex-AI/Understand-Anything : repository metadata via the GitHub API (read 20261030 19:39 UTC)
2. https://github.com/Egonex-AI/Understand-Anything/blob/main/LICENSE : MIT licence text, copyright lines (read 20261030 19:40 UTC)
3. https://github.com/Egonex-AI/Understand-Anything/blob/main/README.md : description, commands, platforms, pipeline and agents, token warning, badges (read 20261030 19:39 UTC; MCP search 19:41 UTC)
4. https://github.com/Egonex-AI/Understand-Anything/releases : eight releases and the v2.9.0 notes (read 20261030 19:40 UTC)
5. https://github.com/Egonex-AI/Understand-Anything/commits/main : commits since 20260801, 100 confirmed by the pagination header (read 20261030 19:40 UTC)
6. https://github.com/Egonex-AI/Understand-Anything/tree/main/understand-anything-plugin : plugin layout, agent files, manifest versions, node and edge types (read 20261030 19:41 UTC)
7. https://github.com/Egonex-AI/Understand-Anything/blob/main/docs/benchmarks/large-monorepo.md : benchmark protocol; it states that it runs no LLM and is not an end-to-end benchmark (read 20261030 19:41 UTC)
8. https://github.com/Egonex-AI/Understand-Anything/pulls : pull request and issue counts via the search API (read 20261030 19:40 UTC)
9. https://github.com/Egonex-AI/Understand-Anything/graphs/contributors : contributor count via the contributors API, 64 pages at one per page (read 20261030 19:39 UTC)
10. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : first landscape snapshot row (snapshot 20261030 19:13 UTC)
