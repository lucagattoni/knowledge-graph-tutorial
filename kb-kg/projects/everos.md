---
slug: everos
repo: EverMind-AI/EverOS
tier: card
category: agent-memory
snapshot: 20261030 19:45 UTC
---

# EverOS

| | |
|---|---|
| Repository | https://github.com/EverMind-AI/EverOS [1] |
| Licence | Apache-2.0, from the `LICENSE` file: standard Apache 2.0 text, differing only in the copyright line ("Copyright 2025 EverMind AI") [2][5]. The README agrees and points to a `NOTICE` file [3]. |
| Language | Python; the README asks for Python 3.12 or newer [1][3] |
| Stars, forks | 13,721, 958 (20261030 19:45 UTC); about 7.0 forks per 100 stars [1] |
| Created, last push | 20251028 15:09 UTC, 20261030 08:54 UTC [1] |
| Latest release | v1.5.1, 20261022 13:22 UTC; PyPI also 1.5.1 [4][6]. Main already records 1.6.0 (CHANGELOG date 20261028); no 1.6.0 tag, release or PyPI version at 19:45 UTC [7][16]. |
| Status | active (pushed within 90 days); no heuristic flag (landscape snapshot, 20261030 19:13 UTC) [17] |
| Paper, docs | no paper stated; `docs/` directory [1][3] |

## What it is

EverOS calls itself "a Python library and local-first memory runtime for agents and makers" that stores conversations, files and agent trajectories as readable Markdown and syncs local SQLite and LanceDB indexes [3]. User memory (episodes, profile) and agent memory (cases, skills) are separate tracks [3]. Release 1.0.0 (20260606) is "a fresh architecture" that dropped MongoDB, Elasticsearch, Milvus, Redis and Kafka [4][8]. The API resolves the old name EverMemOS to this repository [9]. The README states no benchmark results; a `benchmarks/` runner covers four datasets, including LoCoMo and LongMemEval [3][10].

"Local-first, Markdown-native", checked against code and docs:

- **Markdown is the record.** The writer saves each file through a temporary file and an atomic rename under a per-path lock; the reader parses YAML front matter [11]. SQLite and LanceDB are embedded and derived: no database server, and per the docs deleting `.index/` loses nothing [12].
- **Hand edits are indexed.** A watcher queues changed `.md` files, a scanner (default 30 s) catches missed events, and a reconciler compares modification times [13].
- **Not local by default:** extraction needs an LLM endpoint (`[llm]` is required; the quick start uses OpenRouter, any OpenAI-compatible `base_url` works) [3][14][16]. Vector search needs an embedding provider; the one-key setup has keyword search only [3].

## How it works

Messages are added and flushed per session. Most memory kinds are derived later, off the request path, by an in-process Offline Memory Engine: atomic facts, foresight notes, a user profile, agent cases and skills; a cron strategy, off by default, merges fragmented episodes [12]. Search: keyword, vector, hybrid, or agentic (needs a rerank provider), scoped by user, agent, app, project and session [3]. Interfaces: HTTP API (`/api/v2`), CLI, and an MCP server, `everos-mcp`, named in a commit subject [3][16].

## Status and direction

Active: 74 commits since 20260801 (18, 28, 28 for August to October); 22 releases from v1.0.0, four of them release candidates [4][16]. The 1.6.0 change on main is breaking: environment variables become settings and library imports move to service facades [7][16]. 9 contributors, 33 open pull requests, 28 open issues [15]. Roadmap: unstated.

## Sources

1. https://github.com/EverMind-AI/EverOS : repository metadata, GitHub API (read 20261030 19:39 UTC; stars and forks 19:45 UTC)
2. https://github.com/EverMind-AI/EverOS/blob/main/LICENSE : licence text (read 20261030 19:39 UTC)
3. https://github.com/EverMind-AI/EverOS/blob/main/README.md : description, quick start, search, licence section (read 20261030 19:39 UTC)
4. https://github.com/EverMind-AI/EverOS/releases : 22 releases with dates (read 20261030 19:39 UTC)
5. https://api.github.com/licenses/apache-2.0 : standard Apache 2.0 text, compared line by line (read 20261030 19:44 UTC)
6. https://pypi.org/pypi/everos/json : PyPI versions (read 20261030 19:41 UTC)
7. https://github.com/EverMind-AI/EverOS/blob/main/CHANGELOG.md : 1.6.0 entry (read 20261030 19:43 UTC)
8. https://github.com/EverMind-AI/EverOS/blob/main/docs/migration-to-1.0.0.md : 1.0.0 stack (read 20261030 19:44 UTC)
9. https://api.github.com/repos/EverMind-AI/EverMemOS : returned this repository (read 20261030 19:44 UTC)
10. https://github.com/EverMind-AI/EverOS/blob/main/benchmarks/README.md : datasets (read 20261030 19:44 UTC)
11. https://github.com/EverMind-AI/EverOS/tree/main/src/everos/infra/persistence/markdown/_base : `writer.py`, `reader.py` (read 20261030 19:45 UTC)
12. https://github.com/EverMind-AI/EverOS/blob/main/docs/how-memory-works.md and https://github.com/EverMind-AI/EverOS/blob/main/docs/storage_layout.md : storage, cascade, engine (read 20261030 19:43 UTC)
13. https://github.com/EverMind-AI/EverOS/tree/main/src/everos/infra/cascade : `watcher.py`, `scanner.py`, `reconciler.py` (read 20261030 19:45 UTC)
14. https://github.com/EverMind-AI/EverOS/blob/main/docs/configuration.md : LLM, embedding settings (read 20261030 19:43 UTC)
15. https://github.com/EverMind-AI/EverOS/pulls : open pull request, issue and contributor counts (read 20261030 19:41 UTC)
16. https://github.com/EverMind-AI/EverOS/commits/main : subjects since 20260801 (read 20261030 19:41 UTC); head commit message and tag list (read 19:45 UTC)
17. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : first GitHub snapshot row (read 20261030 19:39 UTC)
