---
slug: mirix
repo: Mirix-AI/MIRIX
tier: card
category: agent-memory
snapshot: 20261030 19:39 UTC
---

# MIRIX

| | |
|---|---|
| Repository | https://github.com/Mirix-AI/MIRIX [1] |
| Licence | Apache-2.0, from the `LICENSE` file (Apache License, Version 2.0 text; head and tail read) [2]. The README licence section and GitHub's field also say Apache 2.0 [1][3]. |
| Language | Python [1] |
| Stars, forks | 3,456, 272 (20261030 19:39 UTC; the repository is not in the landscape snapshot) [1] |
| Created, last push | 20250411 12:24 UTC, 20261028 03:29 UTC [1] |
| Latest release | none on GitHub (the latest-release call returned 404); 6 tags, newest by name v0.1.6 [1][4]. PyPI `mirix` 0.1.7, uploaded 20260201 20:25 UTC, summary "Mirix Client" [5]. The README installs `pip install mirix-client`; PyPI's index lists that name with no files or versions, and its JSON call returned 404 [3][9]. Reason: unstated. |
| Status | active: 2 days since the last push; not archived [1] |
| Paper, docs | arXiv 2507.07957 [6]; docs https://docs.mirix.io [7]; website https://mirix.io [3] |

## What it is

MIRIX is a memory system for LLM agents; the README title calls it a "Multi-Agent Personal Assistant with an Advanced Memory System" that "builds memory through screen observation and natural conversation" [3]. The docs say that from 0.1.6 the `main` branch is a pure memory system that plugs into existing agents, and that the desktop assistant lives on the `desktop-agent` branch, whose last commit is dated 20251203 [7][8]. The main README still lists screen activity tracking as a feature [3]. The paper (20250710, no venue stated) proposes six memory types coordinated by a multi-agent layer and reports, as its own claims, 35% higher accuracy than a RAG baseline on ScreenshotVQA, 85.4% on LOCOMO, and 99.9% lower storage (baseline unstated in what I read) [6]. Independent evaluation: none read.

## How it works

Six memory components (Core, Episodic, Semantic, Procedural, Resource, Knowledge Vault), each managed by a dedicated agent [3]. A server started with Docker Compose serves a REST API (port 8531) and a dashboard (port 5173); the Python `MirixClient` adds messages and retrieves with a conversation query [3]. Storage is PostgreSQL 17 (SQLite also named), searched by BM25 full text plus vector similarity [3][7]. The memory agents call a configured LLM; provider modules exist for OpenAI, Anthropic, Google, Azure, Bedrock, Cohere and Mistral [3][10]; local-model use: unstated. An `auto_dream` endpoint merges duplicates and resolves stale entries [3]. MCP: unstated.

## Status and direction

Active, not archived. Main has 7 commits since 20260801: two in August (adaptive session-tag routing) and five on 20261027 and 20261028 (session-based procedural skill learning) [11]. 46 open issues and pull requests; 11 contributors by the API count; at least eight open pull requests were last updated on 20260620 [1][12]. README: upgrading an existing database needs manual SQL migrations [3]. Roadmap: unstated.

## Sources

1. https://github.com/Mirix-AI/MIRIX : repository metadata via the GitHub API (stars, forks, licence field, dates, open issue count) and the contributors count (read 20261030 19:39 UTC)
2. https://github.com/Mirix-AI/MIRIX/blob/main/LICENSE : Apache License 2.0 text (read 20261030 19:39 UTC)
3. https://github.com/Mirix-AI/MIRIX/blob/main/README.md : description, features, quick start, auto-dream, migrations, licence section (read 20261030 19:39 UTC)
4. https://github.com/Mirix-AI/MIRIX/tags : six tags; the releases call returned 404 (read 20261030 19:42 UTC)
5. https://pypi.org/project/mirix/ : version 0.1.7, upload time and summary, read through the PyPI JSON API (read 20261030 19:42 UTC)
6. https://arxiv.org/abs/2507.07957 : abstract, date and numeric claims of the paper (read 20261030 19:41 UTC)
7. https://docs.mirix.io : scope of `main`, storage and search (read 20261030 19:41 UTC)
8. https://github.com/Mirix-AI/MIRIX/tree/desktop-agent : last commit date of the branch (read 20261030 19:42 UTC)
9. https://pypi.org/simple/mirix-client/ : index entry with an empty file list; https://pypi.org/pypi/mirix-client/json returned 404 (read 20261030 19:42 UTC)
10. https://github.com/Mirix-AI/MIRIX/tree/main/mirix/llm_api : provider module names (read 20261030 19:42 UTC)
11. https://github.com/Mirix-AI/MIRIX/commits/main : commit subjects since 20260801 (read 20261030 19:40 UTC)
12. https://github.com/Mirix-AI/MIRIX/issues : the 20 most recently updated issues and pull requests (read 20261030 19:40 UTC)
