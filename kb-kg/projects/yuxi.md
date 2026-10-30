---
slug: yuxi
repo: xerrors/Yuxi
tier: card
category: core
snapshot: 20261030 19:39 UTC
---

# Yuxi

| | |
|---|---|
| Repository | https://github.com/xerrors/Yuxi [1] |
| Licence | MIT, from the `LICENSE` file (21 lines; head and tail read; "Copyright (c) 2025 Yuxi Project Contributors") [2]. The README licence section also says MIT and adds that third-party components pulled in by Docker Compose keep their own licences [3]. |
| Language | Python (GitHub primary language); the architecture file also describes a Vue front end [1][5] |
| Stars, forks | 7,557, 1,234 (20261030 19:39 UTC; the landscape snapshot of 20261030 19:13 UTC has the same figures) [1][9] |
| Created, last push | 20240705 10:57 UTC, 20261029 13:16 UTC [1] |
| Latest release | GitHub "latest" is v0.7.2, 20260902 02:31 UTC. The newest tag is the pre-release v0.8.0.beta5, 20261028 [4]. |
| Status | active; not archived. The landscape snapshot sets no flag (8.92 stars per day over 847 days, 16.33 forks per 100 stars; heuristics) [1][9] |
| Paper, docs | no paper stated; a `docs/` directory in Chinese (the project site, xerrors.github.io/Yuxi, was not fetched); an English `README.en.md` exists and was not read [1][3][7] |

## What it is

Yuxi (the README also gives a Chinese name) is a self-hosted, multi-tenant "knowledge agent" platform, written up in the README in Chinese [3]. In its own words it combines knowledge-base retrieval, a knowledge graph, LangGraph multi-agent orchestration, MCP and Skills, sandboxed tools and permission management in one workspace [3]. The README lists six modules; the knowledge graph is one of them, beside RAG, agents, sandbox workspace and team governance [3]. The README credits LightRAG for early graph-construction and retrieval ideas, RAGFlow for chunking, DeerFlow for the sandbox design and DeepAgents and LangGraph for agents [3]. It reports no benchmark. It ships a retrieval-evaluation tool that scores recall on question sets the user builds [3]; no independent evaluation was found.

## How it works

Uploaded files are parsed (MinerU, PaddleX or RapidOCR), chunked, embedded and indexed in Milvus; search can be hybrid with reranking [3]. Graph building is a separate administrator job: an LLM extractor reads already-indexed chunks, pulls out entities and relations and writes them to Neo4j; parsing does not trigger it [3][6]. Agents run on LangGraph and can call knowledge bases, tools, Skills, MCP servers and asynchronous sub-agents, and run commands in a container or VM sandbox [3][5]. The API serves a read-only knowledge MCP at `/api/mcp`, a public Agent API and an npm command-line client [5][7]. The compose stack runs PostgreSQL, Redis, MinIO, Milvus and Neo4j [5].

## Status and direction

Active, with a pre-release line. The README quick start installs v0.8.0.beta5 and says 0.8 is for fresh deployments only: old databases, indexes and file layouts are not upgraded automatically [3]. 596 commits since 20260801, 424 of them by the owner account and 106 by one other contributor [8]. Roadmap: unstated. 50 open issues, 1 open pull request (20261030 19:45 UTC) [10].

## Sources

1. https://github.com/xerrors/Yuxi : repository metadata via the GitHub API (stars, forks, licence field, dates, language, open issues) (read 20261030 19:39 UTC)
2. https://github.com/xerrors/Yuxi/blob/main/LICENSE : MIT License text (read 20261030 19:42 UTC)
3. https://github.com/xerrors/Yuxi/blob/main/README.md : description, quick start, feature list, graph-building flow, acknowledgements, licence section; read in Chinese and summarised here in English (read 20261030 19:42 UTC)
4. https://github.com/xerrors/Yuxi/releases : release tags, dates and pre-release marks (read 20261030 19:42 UTC)
5. https://github.com/xerrors/Yuxi/blob/main/ARCHITECTURE.md : services, MCP endpoint, sandbox backends (read 20261030 19:43 UTC)
6. https://github.com/xerrors/Yuxi/tree/main/backend/yuxi/modules/knowledge : repository tree; knowledge module layout (graph extractors, Milvus store, evaluation); file names only, source not read (read 20261030 19:43 UTC)
7. https://github.com/xerrors/Yuxi/blob/main/docs/develop-guides/releases/0.8.0.md : 0.8 release notes: Public API, CLI, knowledge MCP (read 20261030 19:43 UTC)
8. https://github.com/xerrors/Yuxi/commits/main : commit count since 20260801 (from the API pagination header), commit authors and recent subjects (read 20261030 19:43 UTC)
9. [Landscape snapshot](../landscape/20261030_1913-github/repos.tsv) : stars per day, forks per 100 stars, flags (20261030 19:13 UTC)
10. https://github.com/xerrors/Yuxi/pulls : open issues and pull requests via the search API (read 20261030 19:45 UTC)
