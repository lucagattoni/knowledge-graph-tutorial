---
slug: zep
repo: getzep/zep
tier: card
category: agent-memory
snapshot: 20261030 19:40 UTC
---

# Zep (getzep/zep)

| | |
|---|---|
| Repository | https://github.com/getzep/zep [1] |
| Licence | Apache-2.0, from the `LICENSE` file (Apache License 2.0 text; head read) [2]. The GitHub field agrees [1]; the README states no licence [3]. |
| Language | Python (GitHub primary language) [1] |
| Stars, forks | 4,984, 659 (20261030 19:39 UTC). No row in the [landscape snapshot](../landscape/20261030_1913-github/repos.tsv), so no heuristic flag. |
| Created, last push | 20230429 14:06 UTC, 20261020 17:10 UTC [1] |
| Latest release | `zep-ingest-v0.4.0`, 20261014 22:43 UTC; releases are per package, and the last one without a package prefix is `v1.0.2`, 20241128 [4] |
| Status | active (10 days since the last push; 23 commits since 20260731); not archived [1][5] |
| Paper, docs | none in the repository; `benchmarks/README.md` links the paper "Zep: A Temporal Knowledge Graph Architecture for Agent Memory" [11]. |

## What it is

Zep offers a managed agent-memory service, and this repository is not that service. The README says so: "This repository is **not** Zep's product or service". It holds "example code, framework integrations, and tools" for Zep Cloud [3]. The open-source graph engine is a separate repository, [Graphiti](graphiti.md), which the README names as the framework "that powers Zep" [3]. On 20261030 19:40 UTC Graphiti had 32,373 stars against 4,984 here [10].

The repository used to be something else:

| Date (UTC) | Event |
|---|---|
| 20230429 | Created [1] |
| to 20241128 | Plain-version releases, the newest `v1.0.2` (a database connection-string fix) [4] |
| 20250402 | Commit "Deprecation notice". A blog post of that date says Zep stops maintaining Community Edition (CE), the repository stays Apache 2.0 without updates, and Graphiti is the open-source focus [5][6] |
| 20250629 | Commit "reorg" creates `legacy/`. Before it the root held the CE server (`src`, `go.work`, `Dockerfile.ce`, `zep.yaml`) [7] |
| 20261014 | Examples, integrations and tools move to "the Zep v4 SDK" [5] |

The CE README just before the reorg described a temporal knowledge graph whose facts carry `valid_at` and `invalid_at` dates [7]. The post gives open-core compromises and under-investment as reasons; that is the vendor's account [6].

## How it works

No engine is here. Everything calls Zep Cloud through the `zep-cloud` SDK, whose source is in `getzep/zep-python` [3][9]. The contents [3]: `examples/` (Python, TypeScript, Go); `integrations/` (Google ADK, CrewAI, LangGraph, LiveKit, Mastra, Pydantic AI, Strands and others, released separately); `ingestion/` (`zep-ingest`, which chunks, contextualises, canonicalises and submits Slack, document, email, JSON, CSV and fact-triple data [9]); `ontology/`; `benchmarks/` (LoCoMo, LongMemEval) and `zep-eval-harness/`; `legacy/`. The LoCoMo README states no score in the part I read [11]. Cloud internals: unstated.

## Status and direction

Active as a samples repository: five commits on 20261014 moved it to the v4 SDK, and `zep-cloud` 4.0.1 is on PyPI [5][9]. The Zep MCP server in `mcp/` is marked deprecated and points to an "official Zep Memory MCP server" [8]. Issues are disabled; the search API shows 28 open pull requests, the GitHub field 36 open items, a gap I could not explain [1][12]. Roadmap: unstated.

## Sources

1. https://github.com/getzep/zep : repository metadata via the GitHub API (read 20261030 19:39 UTC)
2. https://github.com/getzep/zep/blob/main/LICENSE : Apache License 2.0 text, head (read 20261030 19:39 UTC)
3. https://github.com/getzep/zep/blob/main/README.md : "not Zep's product or service", contents, Graphiti pointer (read 20261030 19:39 UTC)
4. https://github.com/getzep/zep/releases : release list and `v1.0.2` notes (read 20261030 19:39 UTC)
5. https://github.com/getzep/zep/commits/main : commits since 20260731; the 20250402 and 20261014 commits (read 20261030 19:39 UTC)
6. https://www.getzep.com/blog/announcing-a-new-direction-for-zeps-open-source-strategy/ : the CE announcement, dated by page metadata (read 20261030 19:39 UTC, via the fetch tool's summary, not verbatim)
7. https://github.com/getzep/zep/commit/f5f56a0f : the 20250629 reorg; root listing and README at its parent (read 20261030 19:39 UTC)
8. https://github.com/getzep/zep/tree/main/mcp/zep-mcp-server : deprecated MCP server README (read 20261030 19:40 UTC)
9. https://pypi.org/pypi/zep-cloud/json and https://pypi.org/pypi/zep-ingest/json : SDK version, `zep-ingest` summary and licence; `ingestion/README.md` (read 20261030 19:40 UTC)
10. https://github.com/getzep/graphiti : repository metadata via the GitHub API (read 20261030 19:40 UTC)
11. https://github.com/getzep/zep/tree/main/benchmarks : `benchmarks/README.md`, `benchmarks/locomo/README.md` (read 20261030 19:40 UTC)
12. https://github.com/getzep/zep/pulls : open pull request and issue counts via the search API (read 20261030 19:40 UTC)
