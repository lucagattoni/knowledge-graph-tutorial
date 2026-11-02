---
type: project
repo: Egonex-AI/Understand-Anything
trends: [code-knowledge-graphs]
updated: 20261102 23:17 UTC
---

# Understand Anything

This page answers what Understand Anything is, how it builds a graph of a codebase, what evidence its authors publish, and whether it is still moving. It sits in the trend [Code graphs for coding agents](../trends/code-knowledge-graphs.md). Unlike [CodeGraph](./codegraph.md), and unlike the code pass of [Graphify](./graphify.md), model agents read the code itself at build time [4]. Its README addresses a person who wants to learn a codebase, through a dashboard [4].

| Field | Value |
|---|---|
| Repository | https://github.com/Egonex-AI/Understand-Anything |
| Licence | MIT, from the `LICENSE` file: the MIT text, 1,111 bytes, with two copyright lines, "2026 Yuxiang Lin" and "2026 Infinite Universe, Inc." [2]. GitHub classifies it as MIT too [2]. |
| Trends | [Code graphs for coding agents](../trends/code-knowledge-graphs.md) |

## What it is

Understand Anything is a plugin for coding [agents](../index/agent.md) that turns a project into an interactive [knowledge graph](../index/knowledge-graph.md) that a person can explore, search and ask questions about [4]. Claude Code is the native host. The README's compatibility table lists 16 other platforms, among them Codex, Cursor, GitHub Copilot, Gemini CLI and OpenCode [4].

The graph is a JSON file in a `.ua/` directory that a team can commit. Anyone can then open it in a read-only dashboard started with `npx`, with no Claude Code, no [LLM](../index/large-language-model.md) (large language model) and no API key [4]. Beyond code, the README names a business-domain view (domains, flows, steps) and a mode for wikis in the pattern Karpathy described in a gist [4]. The v2.9.0 release notes add a Figma mode, `/understand-figma`; the README does not mention it [3][4].

*Reading:* most of the trend serves the agent: its tools return code to a model. This project serves the reader. Its commands (`/understand-chat`, `/understand-onboard`, `/understand-diff`) and its dashboard are for learning a codebase, and the README opens with a new team member facing 200,000 lines of code [4]. The price is a model pass at build time, which the README itself warns can consume "a significant number of tokens" on large projects [4].

## How it works

Two layers share the work [4]. A [tree-sitter](../index/tree-sitter.md) parser deterministically extracts imports, exports, definitions, call sites and inheritance. It also fingerprints files, so a re-run touches only changed ones. Model agents then read the parsed structure and the source and add what a parser cannot: plain-English summaries, tags, architectural layers, domain mapping and guided tours. The README says the structural side is reproducible: the same code gives the same edges [4].

The README lists seven agents, such as `project-scanner` and `graph-reviewer`; the plugin folder holds ten agent files [4][9]. File analysis runs in parallel, up to 5 workers and 20 to 30 files per batch [4]. An optional post-commit hook (`/understand --auto-update`) patches the graph on each commit [4].

The schema in the source has 27 node types and 38 edge types. Nodes cover code, infrastructure and data (service, table, endpoint), business domains, wiki articles and claims, and Figma design elements; edges include `imports`, `calls`, `tested_by` and `contradicts` [6]. The agent interface is slash commands. The README does not mention the [Model Context Protocol](../index/model-context-protocol.md) [4]. A code search of the repository for "mcp" matched nine files: two benchmark scripts, a benchmark document, a schema, a sample, two tests and two lock files. In all nine, the letters sit inside `systemCPUTime` field names or inside package checksums, so no MCP (Model Context Protocol) server or client was found [11].

## Evidence

None published for the question the trend asks: whether an agent does better with the graph than without it. The README gives no savings figure and no answer-quality score [4]. The project's benchmark document describes a harness for scale and speed, not for answers. It runs no LLM, counts no tokens, and says its results must not be presented as an end-to-end benchmark. The TensorFlow commands in it are "a reproduction recipe, not a claim that a TensorFlow benchmark was run" [7].

Two first-party design documents on incremental updates are engineering records. One says its fixtures "simulate analyzer output" and do not measure how often a live model omits a symbol. The other records a failure, "not a claim that the source-evidence layer is finished" [8].

No independent evaluation was found. One arXiv query for the project name returned four papers, none about it [12]. That is one query, not an exhaustive search. For the research around code graphs, see the [papers group](../papers/code-knowledge-graphs.md) and the trend page.

## Status and direction

Active, with no release for 115 days. The latest release is v2.9.0, 20260710 [3]. Eight releases exist, from v1.2.0 (20260325); none is in the last 90 days [3]. The plugin's `package.json` on `main` reads 2.9.8, a version with no release [9]. The v2.9.0 notes list the Figma mode, the move of the data directory to `.ua/` (old directories keep working), Dart, Scala, Swift and Kotlin support, and Kiro, Nanobot and Trae as platforms [3].

In the 90 days since 20260804, `main` took 100 commits: 6 in August, 76 in September and 18 in October. 17 of them are merge commits [5]. 66 commits carry the name Lum1104 and 20 carry Yuxiang Lin, the copyright holder; whether these are one person is **unstated** [2][5]. The contributors API lists 64 accounts [10]. 216 pull requests are open and 139 are merged; about 127 issues are open [1][10].

The snapshot of 20261030 19:54 UTC flags the repository `fast-growth`, a lifetime average of stars per day and not a trend; the watch-list table on the [chapter page](./README.md) carries the counts and push dates [13]. The README shows no maintenance-mode notice and no hosted tier; it links to a second site, egonex.ai, under the tagline "Understand Anyone" [4]. Roadmap: **unstated**.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [codebase-memory-mcp](codebase-memory-mcp.md)
- [CodeGraph](codegraph.md)
- [Graphify](graphify.md)
- [Projects](README.md)

**Experiments**

- [X1: Snapshot distributions](../experiments/x1-snapshot-distributions.md)

**Index**

- [Code graph](../index/code-graph.md)
- [Tree-sitter](../index/tree-sitter.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/Egonex-AI/Understand-Anything : repository metadata by `gh api` (created, last push, archived, open issues and pull requests) (read 20261102 20:17 UTC)
2. https://github.com/Egonex-AI/Understand-Anything/blob/main/LICENSE : licence file by `gh api .../license`: MIT text, copyright lines, size, GitHub classification (read 20261102 20:17 UTC)
3. https://github.com/Egonex-AI/Understand-Anything/releases : latest release v2.9.0 with its notes, among them the Figma mode; the eight releases and their dates (latest release and notes re-read 20261102 20:37 UTC; the list of eight read 20261102 20:17 UTC)
4. https://github.com/Egonex-AI/Understand-Anything/blob/main/README.md : description, platforms, `.ua/`, viewer, modes, pipeline, agents, token warning, local-model note, no MCP mention (read 20261102 20:17 UTC; re-read 20261102 20:37 UTC for the dashboard sentence "no Claude Code, no LLM, no API key", the domain and wiki modes, and the absence of any Figma or MCP mention)
5. https://github.com/Egonex-AI/Understand-Anything/commits/main : 100 commits since 20260804 by month, author names, merge commits (counted again 20261102 20:44 UTC: same numbers)
6. https://github.com/Egonex-AI/Understand-Anything/blob/main/understand-anything-plugin/packages/core/src/types.ts : 27 node types and 38 edge types (read 20261102 20:19 UTC)
7. https://github.com/Egonex-AI/Understand-Anything/blob/main/docs/benchmarks/large-monorepo.md : benchmark scope, no LLM, not end-to-end, the TensorFlow recipe (read 20261102 20:19 UTC)
8. https://github.com/Egonex-AI/Understand-Anything/tree/main/docs/incremental : `symbol-loss-validation.md` and `source-evidence-audit.md`, the statements quoted (read 20261102 20:20 UTC)
9. https://github.com/Egonex-AI/Understand-Anything/tree/main/understand-anything-plugin : plugin layout, ten agent files, `package.json` version 2.9.8 (read 20261102 20:19 UTC)
10. https://github.com/Egonex-AI/Understand-Anything/pulls : open and merged pull request counts by the search API; contributor count by the contributors API (read 20261102 20:19 UTC)
11. https://github.com/Egonex-AI/Understand-Anything : code search for "mcp" (9 files matched), then each of the nine files fetched and checked: every match is inside `systemCPUTime` or a package checksum (read 20261102 20:38 UTC)
12. https://export.arxiv.org/api/query?search_query=all:%22Understand-Anything%22 : 4 results, none about the project (read 20261102 20:21 UTC)
13. kb-kg/landscape/20261030_1954-github/repos.tsv : the row for this repository, flag `fast-growth` (read 20261102 20:20 UTC)
