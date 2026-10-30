---
slug: dify
repo: langgenius/dify
tier: card
category: adjacent
snapshot: 20261030 19:43 UTC
---

# Dify

| | |
|---|---|
| Repository | https://github.com/langgenius/dify [1] |
| Licence | "Dify Open Source License", not an SPDX licence: the `LICENSE` file says Dify "is licensed under a modified version of the Apache License 2.0, with the following additional conditions" [2]. GitHub reports `NOASSERTION` [1]. The README agrees [3]. The conditions: Dify may be used commercially, but "a commercial license must be obtained from the producer" if (a) "Unless explicitly authorized by Dify in writing, you may not use the Dify source code to operate a multi-tenant environment", where one tenant is one workspace; or (b) you remove or modify "the LOGO or copyright information in the Dify console or applications" (this does not apply to uses that do not involve the `web/` frontend). Contributors agree the producer "can adjust the open-source agreement to be more strict or relaxed" and that contributed code may be used commercially, including for cloud business [2]. |
| Language | Python (GitHub primary language) [1] |
| Stars, forks | 160,020, 25,287 (20261030 19:41 UTC; the 20261030 19:13 UTC landscape snapshot had 160,019 and 25,286) [1][14] |
| Created, last push | 20230412 07:40 UTC, 20261030 19:22 UTC [1] |
| Latest release | 1.18.0, 20261023 06:33 UTC [4] |
| Status | active (pushed within 90 days); not archived; no snapshot flag [1][14] |
| Paper, docs | no paper stated; documentation at https://docs.dify.ai [3] |

## What it is

Dify describes itself as an open-source LLM app development platform that combines AI workflow, RAG pipeline, agent capabilities, model management and observability [3]. It is a general application platform, not a knowledge-graph tool. The part that bears on this repository is its knowledge bases: the documentation describes a classic knowledge base and an Agent Knowledge Base, released as an opt-in beta in 1.18.0 [4][5][7]. Only the Agent Knowledge Base is documented as building a knowledge graph [9]. No benchmark or evaluation of either appears in the sources read: unstated.

## How it works

Classic: imported data is chunked, then indexed with an embedding model (High Quality) or as 10 keywords per chunk (Economical); retrieval is vector, full-text or hybrid, with optional rerank, default top 3 and score 0.5 [5][6]. Agent Knowledge Base (beta): a reasoning model builds an outline with section summaries; chunks hold at most 1,200 characters [8]. The docs and UI strings say a knowledge graph is built at indexing; Deep retrieval follows it [9][13]. The backend is a separate KnowledgeFS service whose repository is described as private [10]. Access: a retrieval node, agent configuration, a Service API, a read-only CLI [11]; the MCP page covers exposing apps, not knowledge bases [12].

## Status and direction

Active: last push 20261030 19:22 UTC. Six releases since 20260709 (1.16.0-rc1 to 1.18.0, 20261023) [4]. The 1.18.0 notes introduce the Agent Knowledge Base as an opt-in beta with a separate service and database, and say the classic Knowledge remains available [4]. Open issues and pull requests: 1,141 combined [1]. Roadmap: unstated (no roadmap file read).

## Sources

All read 20261030 19:40-19:43 UTC (the clock was checked before and after the reads, not per call).

1. https://github.com/langgenius/dify : repository metadata via the GitHub API
2. https://github.com/langgenius/dify/blob/main/LICENSE : full licence text, quoted above
3. https://github.com/langgenius/dify/blob/main/README.md : description, licence section
4. https://github.com/langgenius/dify/releases : releases since 20260701 and the 1.18.0 notes
5. https://docs.dify.ai/en/use-dify/knowledge/readme : classic knowledge base overview; no knowledge graph, no MCP
6. https://docs.dify.ai/en/cloud/use-dify/knowledge/create-knowledge/setting-indexing-methods.md : index methods and retrieval settings
7. https://docs.dify.ai/en/cloud/use-dify/knowledge-base/overview.md : Agent Knowledge Base overview (beta)
8. https://docs.dify.ai/en/cloud/use-dify/knowledge-base/review-indexed-documents.md : outline, section summaries, 1,200-character chunks
9. https://docs.dify.ai/en/cloud/use-dify/knowledge-base/retrieval-settings.md : retrieval depths; knowledge graph built at indexing
10. https://github.com/langgenius/dify/blob/main/api/knowledge-fs-contract/README.md and https://github.com/langgenius/dify/blob/main/docker/README.md : KnowledgeFS as a standalone private repository and an optional Compose profile
11. https://docs.dify.ai/en/cloud/use-dify/knowledge-base/use-knowledge-in-apps.md : retrieval node, agents, Service API, `difyctl` access
12. https://docs.dify.ai/en/cloud/use-dify/publish/publish-mcp.md : apps exposed as MCP servers
13. GitHub code search in the repository: no hit for "graphrag"; English UI strings in `web/i18n/locales/en-US/knowledge-tasks.json` mention "building the knowledge graph" and an incomplete knowledge graph
14. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : first GitHub snapshot (20261030 19:13 UTC); flags column empty for this repository
