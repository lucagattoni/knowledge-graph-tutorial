---
slug: memos
repo: MemTensor/MemOS
tier: card
category: agent-memory
snapshot: 20261030 19:39 UTC
---

# MemOS

| | |
|---|---|
| Repository | https://github.com/MemTensor/MemOS [1] |
| Licence | Apache-2.0, from the `LICENSE` file: the standard Apache License 2.0 text with the appendix line filled in as "2025 - Present MemTensor Research"; a word-by-word comparison with the text at apache.org found no other difference [2][3]. The README licence section says Apache 2.0, so they agree [4]. |
| Language | TypeScript (GitHub primary language) [1]; the server in `src/memos` is Python, the local plugin in `apps/memos-local-plugin` is a Node.js package [4][5] |
| Stars, forks | 12,200, 1,098 (20261030 19:39 UTC) [1] |
| Created, last push | 20250706 09:51 UTC, 20261029 11:26 UTC [1] |
| Latest release | v2.0.34, 20260923 05:24 UTC, marked latest by GitHub; the notes are one line, "MemoryOS 2.0.34 release" [6]. A second tag family, `memos-local-plugin-v*`, is newer: v2.0.21, 20261029 09:15 UTC [6]. PyPI `MemoryOS` stops at 2.0.33, 20260903 [8]. |
| Status | active (pushed within 24 hours of the read); not archived [1] |
| Paper, docs | arXiv 2507.03724 [7]; docs at https://memos-docs.openmem.net [4] |

## What it is

MemOS presents itself as a "Memory Operating System" for LLMs and agents that unifies storing, retrieving and managing long-term memory, with a graph-structured memory API, multi-modal memory, "memory cubes" for separate knowledge bases, an asynchronous scheduler and natural-language feedback to correct memories [4]. One repository now holds two products: a Python service, run as a hosted Cloud API or self-hosted, and a local-first plugin for OpenClaw, Hermes Agent and DeepSeek Harness [4][5]. The paper's abstract proposes the MemCube as one unit for plaintext, activation and parameter memory and reports no experiments (four versions, 20250704 to 20251203) [7]. The README table (LoCoMo 88.83, LongMemEval 89.20 and eight other scores) lists no competitor scores and cites OmniMemEval, which the same GitHub organisation publishes; no third-party evaluation appears in the sources read [4][9].

## How it works

Self-hosting starts a REST API with Neo4j for the graph and Qdrant for vectors, by docker compose [4]. A client creates a memory cube, adds messages to writable cubes (sync or async) and searches readable ones [4]. Source directories include a memory reader, scheduler, feedback, a "dream" pipeline, and graph, vector and reranker modules; I did not read them [5]. The local plugin keeps four layers in SQLite: L1 step traces, L2 policies induced across traces, L3 world models and callable skills, with FTS5 plus vector retrieval and feedback-driven evolution [4][10]. LLM, embedder and databases are set in a `.env` file; which calls run at index and query time: unstated [4].

## Status and direction

Active. 206 commits since 20260801 (13 dated October); 21 of the 30 newest subjects name the plugin [11]. The Python server's last tag is v2.0.34 (20260923), while the plugin tagged v2.0.21 on 20261029 [6]. 90 open pull requests, 61 open issues, 103 contributors (API count, anonymous included) [11]. Roadmap: unstated.

## Sources

1. https://github.com/MemTensor/MemOS : repository metadata via the GitHub API (read 20261030 19:39 UTC)
2. https://github.com/MemTensor/MemOS/blob/main/LICENSE : Apache License 2.0 text, appendix line "2025 - Present MemTensor Research" (read 20261030 19:39 UTC)
3. https://www.apache.org/licenses/LICENSE-2.0.txt : reference text for the comparison (read 20261030 19:42 UTC)
4. https://github.com/MemTensor/MemOS/blob/main/README.md : description, benchmark table, quick start, plugins, licence section (read 20261030 19:39 UTC)
5. https://github.com/MemTensor/MemOS/tree/main/src/memos : file tree via the GitHub API; directory and module names only (read 20261030 19:44 UTC)
6. https://github.com/MemTensor/MemOS/releases : 60 releases, the v2.0.34 notes and the plugin tags, via the releases API (read 20261030 19:39 UTC)
7. https://arxiv.org/abs/2507.03724 : paper abstract and versions, via the fetch tool (read 20261030 19:44 UTC)
8. https://pypi.org/pypi/MemoryOS/json : PyPI versions and dates (read 20261030 19:45 UTC)
9. https://github.com/MemTensor/OmniMemEval : the evaluation framework the README names; Apache-2.0, 80 stars, created 20260624 (read 20261030 19:44 UTC)
10. https://github.com/MemTensor/MemOS/blob/main/apps/memos-local-plugin/README.md : the plugin's L1, L2, L3 and skill layers (read 20261030 19:44 UTC)
11. https://github.com/MemTensor/MemOS/commits/main : commits since 20260801, subjects, open pull request and issue counts (search API), contributor count (read 20261030 19:41 UTC)
