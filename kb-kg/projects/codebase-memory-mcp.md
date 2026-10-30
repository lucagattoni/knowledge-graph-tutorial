---
slug: codebase-memory-mcp
repo: DeusData/codebase-memory-mcp
tier: card
category: adjacent
snapshot: 20261030 19:44 UTC
---

# codebase-memory-mcp

| | |
|---|---|
| Repository | https://github.com/DeusData/codebase-memory-mcp [1] |
| Licence | MIT, from the `LICENSE` file (head and tail read; copyright 2025 DeusData) [2]. The README badge and licence section also say MIT, so they agree [3]. |
| Language | C (GitHub primary language); the README also lists a React, Monaco and Three.js browser frontend in `graph-ui/`, which the file tree confirms [1][3][6] |
| Stars, forks | 47,853, 3,935 (20261030 19:39 UTC). The repository has no row in the landscape snapshot of 20261030 19:13 UTC, so every figure here was read live and no snapshot flag applies [1][10]. |
| Created, last push | 20260224 22:01 UTC, 20261029 06:53 UTC [1] |
| Latest release | v0.12.1, 20261016 23:35 UTC; 49 releases in all, v0.0.2 (20260225) to v0.12.1 [4] |
| Status | active (pushed one day before the read); not archived [1]. Context: 8.22 forks per 100 stars (my arithmetic: 3,935 / 47,853), 188 contributors on the contributors API, 477 open issues, 116 open and 1,027 merged pull requests [1][7][8]. |
| Paper, docs | arXiv 2603.27277, "Codebase-Memory: Tree-Sitter-Based Knowledge Graphs for LLM Code Exploration via MCP", submitted 20260328 [9]; the README; a docs site at https://deusdata.github.io/codebase-memory-mcp/ (homepage field, not fetched) [1][3] |

## What it is

codebase-memory-mcp is an MCP server and command-line tool, written in C, that builds a persistent local knowledge graph of a repository's code, documentation, configuration and infrastructure [1][3]. Besides source it indexes Markdown, PDF text and architecture decision records, and Docker, Kubernetes, Helm and Terraform files. It offers 17 MCP tools and an optional browser interface, CBM Lens, which the README calls an open beta (v0.0.1) [3]. The README claims 162 languages and 45 agent integrations [3]. The paper by Vogel and four co-authors reports, over 31 repositories, 83% answer quality against 92% for a file-exploration agent, at about ten times fewer tokens and 2.1 times fewer tool calls, and describes 66 languages [9]. The README repeats the token and tool-call figures and links the paper, but does not state the quality figures [3]. A commit author named Martin Vogel, the same name as the paper's first author, wrote 2,145 of the 2,810 commits since 20260801 [5][9].

## How it works

A native pipeline discovers files (honouring `.gitignore` and `.cbmignore`) and runs passes for structure, definitions, calls, HTTP links, configuration and tests [3]. Vendored tree-sitter grammars parse; a "Hybrid LSP" step resolves types for languages such as Python, TypeScript, Go, Java and Rust [3]. The graph is SQLite with 28 node labels and 42 edge types, plus Louvain clustering [3]. Search is structural, BM25 and semantic, with an embedding model bundled in the binary; a read-only Cypher subset is supported [3]. The README says the backend needs no generative model or API key, and the agent is the intelligence layer [3]. A background watcher re-indexes changed projects [3].

## Status and direction

Active and fast-moving: 2,810 commits on main from 20260801 to the read, of which 1,061 have a merge subject [5]. v0.12.1 fixed npm, PyPI, Go and Homebrew installs and linked Helm charts to what they deploy [4]. 116 pull requests are open [7]. Roadmap: unstated; the README invites ideas on Discord [3].

## Sources

1. https://github.com/DeusData/codebase-memory-mcp : repository metadata via the GitHub API (read 20261030 19:39 UTC)
2. https://github.com/DeusData/codebase-memory-mcp/blob/main/LICENSE : MIT licence text, copyright line (read 20261030 19:43 UTC)
3. https://github.com/DeusData/codebase-memory-mcp/blob/main/README.md : description, features, MCP tools, data model, performance section, architecture, licence section (read 20261030 19:39 UTC; searched for the quality figures 19:44 UTC)
4. https://github.com/DeusData/codebase-memory-mcp/releases : 49 releases and the v0.12.1 notes (read 20261030 19:43 UTC)
5. https://github.com/DeusData/codebase-memory-mcp/commits/main : commits since 20260801, 2,810 confirmed by the pagination header (read 20261030 19:43 UTC)
6. https://github.com/DeusData/codebase-memory-mcp/tree/main : repository layout (`src/`, `internal/`, `graph-ui/`) (read 20261030 19:44 UTC)
7. https://github.com/DeusData/codebase-memory-mcp/pulls : pull request and issue counts via the search API (read 20261030 19:43 UTC)
8. https://github.com/DeusData/codebase-memory-mcp/graphs/contributors : contributor count via the contributors API (read 20261030 19:39 UTC)
9. https://arxiv.org/abs/2603.27277 : title, authors, submission date and abstract, read through the arXiv API (read 20261030 19:44 UTC)
10. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : searched for the repository name; no row found (searched 20261030 19:39 UTC)
