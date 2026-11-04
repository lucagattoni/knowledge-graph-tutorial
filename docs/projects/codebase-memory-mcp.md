---
type: project
repo: DeusData/codebase-memory-mcp
trends: [code-knowledge-graphs]
updated: 20261102 23:17 UTC
---

# codebase-memory-mcp

codebase-memory-mcp turns a source repository into a local graph of code, documents and deployment files, and serves it to coding agents over the [Model Context Protocol](../index/model-context-protocol.md). This page says how it works, what has been measured and by whom, and where the project stands.

| Field | Value |
|---|---|
| Repository | https://github.com/DeusData/codebase-memory-mcp |
| Licence | MIT. The `LICENSE` file starts "MIT License" and "Copyright (c) 2025 DeusData"; GitHub classifies it as MIT [1][2] |
| Trends | [Code graphs for coding agents](../trends/code-knowledge-graphs.md) |

## What it is

codebase-memory-mcp is an MCP (Model Context Protocol) server and command-line tool written in C. GitHub's description calls it "Local code intelligence for developers and AI agents" [1]. It builds a persistent graph of a repository's code, Markdown and PDF text, architecture decision records, and Docker, Kubernetes, Helm, Terraform and Ansible files [3]. The README lists 17 MCP tools and 45 supported agent clients, and says indexing and queries need no hosted service or API key [3]. An optional browser interface, CBM Lens, is described as an open beta (v0.0.1) [3].

It belongs to the [code graph](../index/code-graph.md) family: the graph is built by a parser, not by a language model. Close neighbours are [codegraph](../projects/codegraph.md), [graphify](../projects/graphify.md), [understand-anything](../projects/understand-anything.md), [code-graph-rag](../projects/code-graph-rag.md) and [code-review-graph](../projects/code-review-graph.md).

## How it works

**Parse.** A native pipeline walks the files, honouring `.gitignore` and `.cbmignore`, and parses them with 162 vendored [tree-sitter](../index/tree-sitter.md) grammars compiled into the binary [3]. Passes then extract structure, definitions, calls, HTTP links, configuration and tests [3]. A "Hybrid LSP" (Language Server Protocol) pass resolves types for languages such as Python, TypeScript, Go, Java and Rust, in the manner of a [language server](../index/language-server-protocol.md) but without running one [3].

**Store.** The graph lives in SQLite in a local cache directory. The README lists 28 node labels and 42 edge types: calls, imports and inheritance, plus HTTP and gRPC calls, `DEPLOYS` and `CONFIGURES` for infrastructure, and cross-repository links [3]. [Community detection](../index/community-detection.md) uses Louvain clustering [3].

**Query.** Search is structural (name patterns, labels, degree), full-text ([BM25](../index/bm25.md), Best Matching 25, a keyword ranking function) and semantic ([vector search](../index/vector-search.md) over an embedding model compiled into the binary) [3]. A read-only subset of [Cypher](../index/cypher.md) is supported, and `trace_path` follows callers, callees, data flow and deployment paths [3]. `detect_changes` maps a diff to affected symbols with a risk class, a form of [impact analysis](../index/impact-analysis.md) [3].

**Who reasons.** The README says the backend "does not require a generative model" and the agent is the intelligence layer [3]. A background watcher re-indexes projects registered by active sessions [3].

## Evidence

All published results are first-party. The system paper, "Codebase-Memory", has five authors and was submitted on 20260328 [4]. Its first author, Martin Vogel, is the name on the public profile of the `DeusData` account that owns the repository [5]. The paper says the responses "were graded by the first author" [6].

| Claim | Test | Who ran it | First-party | Date | Source |
|---|---|---|---|---|---|
| Answer quality 0.83 against 0.92 for a file-exploration agent | 12 question categories, one repository for each of 31 languages; both agents on Claude Opus 4.6; paper's version of the tool had 14 tools | Paper authors; graded by the first author | yes | 20260328 | [4][6] |
| About 1,000 against about 10,000 tokens, and 2.3 against 4.8 tool calls, per question | same | same | yes | 20260328 | [6] |
| Linux kernel full index in 3 minutes; Django in about 6 seconds | Apple M3 Pro; 75,000 files, 4.81M nodes | Project README | yes | README read 20261102 | [3] |

The paper states its limits [6]:

- one model and one repository per language;
- the explorer wins on full source context (16 of 31 languages) and exhaustive call-site search (10 of 31);
- macro-heavy C scores 0.58 against 1.00;
- comparison with embedding-based retrieval, ctags, language servers and other graph systems "remains future work".

The README's 162 languages and 17 tools describe a later version than the paper's 66 languages and 14 tools, so the paper's numbers do not describe the current release [3][6].

*Reading:* the result is a cost saving at some loss of answer quality, measured by the authors on structural questions. It says nothing about whether an agent solves coding tasks better. No independent evaluation appears in the sources read: an arXiv listing search for the exact name returned no result on 20261102 20:20, which covers listed metadata only [7].

## Status and direction

The repository is active and not archived [1]. The latest release is v0.12.1, published 20261016 23:35 UTC; it fixed npm, PyPI, Go and Homebrew installs and linked Helm charts to the objects they deploy [8]. The API lists 49 releases, from v0.0.2 (20260225), and 12 of them fall in the 90 days since 20260804 [8]. In the same window the default branch received 3,081 commits, merge commits included [9]. The `DeusData` account holds 3,357 contributions and the next contributor 210 [5].

The sources read show no maintenance-mode notice and no hosted or paid tier; the README describes local processing and MIT licensing [1][3]. Its roadmap is **unstated**: the README invites ideas on Discord and lists no plan [3]. The README presents two parts as unfinished: CBM Lens is "in open beta (v0.0.1)", and Smart CI (continuous integration) for test selection is "experimental" and covers supported C and C++ test harnesses [3].

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)
- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [code-review-graph](code-review-graph.md)
- [CodeGraph](codegraph.md)
- [Projects](README.md)

**Papers**

- [Papers: Code graphs for coding agents](../papers/code-knowledge-graphs.md)

**Experiments**

- [Experiments evidence: status log](../experiments/evidence/status.md)
- [X1: Snapshot distributions](../experiments/x1-snapshot-distributions.md)
- [X4: a code graph against grep](../experiments/x4-code-graph-vs-grep.md)

**Index**

- [Abstract syntax tree](../index/abstract-syntax-tree.md)
- [Code graph](../index/code-graph.md)
- [Impact analysis](../index/impact-analysis.md)
- [Language Server Protocol](../index/language-server-protocol.md)
- [Model Context Protocol](../index/model-context-protocol.md)
- [Tree-sitter](../index/tree-sitter.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/DeusData/codebase-memory-mcp : repository metadata through the GitHub API (description, language, licence field, archived flag, creation date) (read 20261102 20:18 UTC)
2. https://github.com/DeusData/codebase-memory-mcp/blob/main/LICENSE : licence text and copyright line, through the API licence endpoint (read 20261102 20:18 UTC)
3. https://github.com/DeusData/codebase-memory-mcp/blob/main/README.md : features, tools, data model, performance table, language support, agent setup, licence section (read 20261102 20:18 to 20:20 UTC)
4. https://arxiv.org/abs/2603.27277 : Vogel, Meyer-Eschenbach, Kohler, Grünewald and Balzer, "Codebase-Memory: Tree-Sitter-Based Knowledge Graphs for LLM Code Exploration via MCP", submitted 20260328, abstract (read 20261102 20:19 UTC)
5. https://api.github.com/users/DeusData : public profile name of the account owning the repository ("Martin Vogel"); and https://api.github.com/repos/DeusData/codebase-memory-mcp/contributors : contributions per account, 3,357 and 210 for the first two (read 20261102 20:36 UTC)
6. https://arxiv.org/html/2603.27277v1 : full text of version 1, sections 4 and 5 (benchmark protocol, Table 6, threats to validity) (read 20261102 20:21 UTC)
7. https://arxiv.org/search/?query=%22codebase-memory-mcp%22&searchtype=all : exact-name search, no results (read 20261102 20:20 UTC)
8. https://github.com/DeusData/codebase-memory-mcp/releases : latest release notes and the release list through the GitHub API (read 20261102 20:19 UTC)
9. https://api.github.com/repos/DeusData/codebase-memory-mcp/commits?since=2026-08-04T00:00:00Z&per_page=1 : with one entry per page, the last page number in the `Link` header is the commit count, 3,081 (read 20261102 20:36 UTC)
