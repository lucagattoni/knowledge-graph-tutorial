---
slug: memmachine
repo: MemMachine/MemMachine
tier: card
category: agent-memory
snapshot: 20261030 19:45 UTC
---

# MemMachine

| | |
|---|---|
| Repository | https://github.com/MemMachine/MemMachine [1] |
| Licence | Apache-2.0, from the `LICENSE` file: standard Apache 2.0 text, differing only in the copyright line ("Copyright 2025 MemVerge Inc.") [2][5]. The README agrees [3]. |
| Language | Python; PyPI packages `memmachine-client` and `memmachine-server`; the README also names a TypeScript SDK [1][3][12] |
| Stars, forks | 3,078, 225 (20261030 19:45 UTC); about 7.3 forks per 100 stars [1] |
| Created, last push | 20250815 16:40 UTC, 20261029 11:54 UTC. That push went to branch `security/auto-fix-vulnerabilities`; the default branch last moved 20261012 23:23 UTC [1][6][7] |
| Latest release | v0.4.0, 20261008 00:27 UTC, the first since v0.3.9 on 20260518 [4]; PyPI `memmachine-server` 0.4.0 [12] |
| Status | active by the 90-day push rule; no default-branch commit for about 18 days at the read time; no heuristic flag (landscape snapshot, 20261030 19:13 UTC) [1][7][13] |
| Paper, docs | no paper for MemMachine stated; the README's one reference is the Agent Lightning paper (arXiv:2508.03680), which two retrieval-agent prompts also cite; docs.memmachine.ai not fetched [3][11][16] |

## What it is

MemMachine calls itself "the open-source memory layer for AI agents", with episodic memory ("graph-based conversational context"), profile memory (user facts "stored in SQL") and working memory [3]. The README offers a "free account" on a managed platform, while `USAGE.md` says "MemMachine is not a hosted service" [3][8]. The README places episodic memory in a graph database (Neo4j). The sample Docker Compose configuration defaults instead to an "event" backend on a Qdrant vector store and a relational segment store; the Neo4j "declarative" backend is a second profile [3][9]. The README gives no benchmark results; an `evaluation/` directory holds scripts for LoCoMo, WikiMultiHop, HotpotQA and BEAM [10]. GitHub topics include `knowledge-graph` [1].

## How it works

Clients (Python, TypeScript, REST, MCP) add and search memories scoped by organisation, project, group, agent, user and session [3]. Short-term memory keeps a capped queue of recent turns and has an LLM summarise evicted ones [14]. Long-term episodic memory uses the event or declarative backend [9]. Semantic (profile) memory has an LLM turn episodes into features and consolidate them; `USAGE.md` puts them, with embeddings, in PostgreSQL [8][15]. A retrieval agent routes each query to chain-of-query, split-query or plain retrieval; `RaragQueryAgent` splits multi-hop queries [16]. LLMs include OpenAI, Bedrock and Ollama [3][8].

## Status and direction

Active, with a pause on the default branch: 39 commits since 20260801 (3, 24, 12 for August to October), none after 20261012 [7]. v0.4.0 followed no release from 20260518 to 20261008; its notes list a Milvus vector store, Qdrant in the compose file and Helm chart, a LiteLLM provider, BEAM benchmark support and a multi-hop retrieval agent [4][17]. 49 contributors, 108 open pull requests, 140 open issues [18]. Roadmap: unstated.

## Sources

1. https://github.com/MemMachine/MemMachine : repository metadata, topics, GitHub API (read 20261030 19:39 UTC; stars and forks 19:45 UTC)
2. https://github.com/MemMachine/MemMachine/blob/main/LICENSE : licence text (read 20261030 19:39 UTC)
3. https://github.com/MemMachine/MemMachine/blob/main/README.md : description, quick start, architecture, references, licence section (read 20261030 19:39 UTC)
4. https://github.com/MemMachine/MemMachine/releases : 31 releases with dates (read 20261030 19:39 UTC)
5. https://api.github.com/licenses/apache-2.0 : standard Apache 2.0 text, compared line by line (read 20261030 19:44 UTC)
6. https://api.github.com/repos/MemMachine/MemMachine/events : recent events, including the branch push (read 20261030 19:43 UTC)
7. https://github.com/MemMachine/MemMachine/commits/main : default-branch subjects since 20260801 (read 20261030 19:41 UTC; head 19:45 UTC)
8. https://github.com/MemMachine/MemMachine/blob/main/USAGE.md : "not a hosted service", memory types, installation (read 20261030 19:42 UTC)
9. https://github.com/MemMachine/MemMachine/blob/main/sample_configs/configuration.event.yml : event backend, declarative alternative (read 20261030 19:43 UTC)
10. https://github.com/MemMachine/MemMachine/blob/main/evaluation/README.md : benchmark suites (read 20261030 19:42 UTC)
11. https://github.com/MemMachine/MemMachine/blob/main/packages/server/src/memmachine_server/retrieval_agent/agents/tool_select_agent.py : prompt with the Agent Lightning citation (read 20261030 19:44 UTC)
12. https://pypi.org/pypi/memmachine-server/json : PyPI versions (read 20261030 19:41 UTC)
13. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : first GitHub snapshot row (read 20261030 19:39 UTC)
14. https://github.com/MemMachine/MemMachine/blob/main/packages/server/src/memmachine_server/episodic_memory/short_term_memory/short_term_memory.py : module docstring (read 20261030 19:44 UTC)
15. https://github.com/MemMachine/MemMachine/blob/main/packages/server/src/memmachine_server/semantic_memory/semantic_ingestion.py : episodes to features, LLM consolidation (read 20261030 19:44 UTC)
16. https://github.com/MemMachine/MemMachine/tree/main/packages/server/src/memmachine_server/retrieval_agent/agents : `tool_select_agent.py`, `rarag_query_agent.py` (read 20261030 19:43 UTC)
17. https://github.com/MemMachine/MemMachine/releases/tag/v0.4.0 : release notes (read 20261030 19:43 UTC)
18. https://github.com/MemMachine/MemMachine/pulls : open pull request and issue counts, contributors, via the API (read 20261030 19:41 UTC)
