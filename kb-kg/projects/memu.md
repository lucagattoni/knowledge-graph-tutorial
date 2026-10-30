---
slug: memu
repo: NevaMind-AI/memU
tier: card
category: agent-memory
snapshot: 20261030 19:45 UTC
---

# memU

| | |
|---|---|
| Repository | https://github.com/NevaMind-AI/memU [1] |
| Licence | GitHub reports `NOASSERTION` [1]. There is no file named `LICENSE`; `LICENSE.txt` is Apache License 2.0 text with edited wording, closing with "Copyright 2024 MemU Team" and an Apache 2.0 notice [2]. Against the standard text [5] the material change is section 2: the copyright grant uses MIT-style words ("use, reproduce, modify, merge, publish, distribute, sublicense, and/or sell copies"), on condition that the copyright and permission notice stay in all copies. The patent grant, redistribution conditions, trademark exclusion and disclaimers read as in Apache 2.0; other changes are rewording and a missing appendix [2][5]. No non-commercial, field-of-use or network clause. The README says Apache-2.0 [3]. Why GitHub does not recognise the file: unstated. |
| Language | Python (GitHub primary language); Python 3.11 or newer [1][6] |
| Stars, forks | 14,581, 1,096 (20261030 19:45 UTC); about 7.5 forks per 100 stars [1] |
| Created, last push | 20250729 01:54 UTC, 20261030 11:22 UTC [1] |
| Latest release | v1.5.1, 20260323 07:38 UTC; pre-release v2.0.0-beta.0, 20260723 04:16 UTC [4]. PyPI `memu-cli`: 0.10.0 latest (20260805), 0.11.0 betas to 20260821 [12]. Mapping between the two version lines: unstated. |
| Status | active (pushed within 90 days); 52 commits in 90 days, no heuristic flag (landscape snapshot, 20261030 19:13 UTC) [8] |
| Paper, docs | no paper stated; README and `docs/` (developer guide, 20 decision records) [3][9] |

## What it is

memU calls itself "a lightweight, agent-driven memory system that gives users a shared LLM wiki across sessions, agents, and devices" and says it distils reusable skills from agent history [3]. It runs as a sidecar to desktop coding agents: it reads their session logs and stores Markdown memories and skills with embeddings [3]. The README says its core memory logic is "only 500 lines"; which files that covers is unstated, and `agentic.py` alone has 673 lines [3][7]. A hosted "MemU Cloud" also exists; whether its server code is in the repository: unstated [3]. The README gives no benchmark [3].

## How it works

One adapter per host agent (Codex, Claude Code, Cursor, OpenClaw, Hermes and others). A scheduled task slices new session logs into jobs; the host agent itself decides whether to write or patch a memory or skill file, and a commit step embeds and stores it [3]. A line in the host's instruction file tells the agent to run a retrieve command before answering; hosts get at most five hits [3]. `MemoryService` is "embedding-only": its only model calls are embeddings, and `progressive_retrieve` ranks segments by vector similarity [7]. Stores: in-memory, SQLite, or Postgres with pgvector [3]. ADR 0007 (status Proposed) describes hybrid embedding plus BM25 retrieval; the code I read does not [7][10].

## Status and direction

Active. Recent commit subjects add Codex prompt retrieval, a pi adapter, retrieval score cutoffs and Windows fixes [11]. The CHANGELOG stops at 2.0.0-beta.0 (20260723); it lists an LLM and VLM gateway (#442) that the current source tree no longer has [4][13]. 49 contributors, 72 open pull requests, 66 open issues [14]. Roadmap: unstated.

## Sources

1. https://github.com/NevaMind-AI/memU : repository metadata, GitHub API (read 20261030 19:39 UTC; stars and forks 19:45 UTC)
2. https://github.com/NevaMind-AI/memU/blob/main/LICENSE.txt : licence text; the API returned 404 for `LICENSE` (read 20261030 19:40 UTC)
3. https://github.com/NevaMind-AI/memU/blob/main/README.md : description, hosts, retrieval, storage, licence section (read 20261030 19:39 UTC)
4. https://github.com/NevaMind-AI/memU/releases : release list (read 20261030 19:39 UTC)
5. https://api.github.com/licenses/apache-2.0 : standard Apache 2.0 text, compared line by line (read 20261030 19:40 UTC)
6. https://github.com/NevaMind-AI/memU/blob/main/pyproject.toml : Python requirement, version 0.11.0-beta.3 (read 20261030 19:40 UTC)
7. https://github.com/NevaMind-AI/memU/tree/main/src/memu/app : `service.py`, `agentic.py` (read 20261030 19:40 UTC)
8. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : first GitHub snapshot row (read 20261030 19:39 UTC)
9. https://github.com/NevaMind-AI/memU/tree/main/docs : file listing (read 20261030 19:39 UTC)
10. https://github.com/NevaMind-AI/memU/blob/main/docs/adr/0007-three-independent-memory-lines-wiki-graph.md : ADR 0007 (read 20261030 19:41 UTC)
11. https://github.com/NevaMind-AI/memU/commits/main : commit subjects since 20260801 (read 20261030 19:40 UTC)
12. https://pypi.org/pypi/memu-cli/json : PyPI versions (read 20261030 19:40 UTC)
13. https://github.com/NevaMind-AI/memU/blob/main/CHANGELOG.md : 2.0.0-beta.0 entry; `src/memu` file list from the tree API (read 20261030 19:40 UTC)
14. https://github.com/NevaMind-AI/memU/pulls : open pull request, issue and contributor counts (read 20261030 19:40 UTC)
