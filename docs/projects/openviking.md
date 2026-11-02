---
type: project
repo: volcengine/OpenViking
trends: [agent-memory, plain-file-knowledge]
updated: 20261102 23:17 UTC
---

# OpenViking

OpenViking is an open-source "context database" that keeps an agent's knowledge, memories and skills in one file tree. This page covers what it stores, how agents reach it, what its authors have measured, and what its licence and hosted edition mean for reuse. Read on 20261102, 20:10 to 20:35 UTC, unless a source line says otherwise.

| Field | Value |
|---|---|
| Repository | https://github.com/volcengine/OpenViking |
| Licence | AGPL-3.0: GitHub classifies the `LICENSE` file as GNU AGPL v3.0 [2]. It equals the GNU reference text except five word-level differences, one an added phrase; legal effect not assessed [3]. The README's licence section lists other components under their own licences: the CLI (command-line interface) crate and examples Apache-2.0, the Hermes plugin example and the Microsoft Agent Framework adapter MIT, the LangChain/LangGraph adapter AGPL-3.0, and third-party code under its original licences [4]. Copyleft for the main project, so a read-only reference here. |
| Trends | [Agent memory](../trends/agent-memory.md), [Plain files as agent knowledge](../trends/plain-file-knowledge.md) |

## What it is

The README calls it "one filesystem for everything an agent knows: knowledge, memory, and skills" [4]. Resources, memories and skills sit under `viking://` addresses. Agents browse them with file commands such as `ls`, `tree` and `grep`, and every directory carries a generated summary [4]. A vector index sits beside the files [6]. It reaches agents through an HTTP API, a CLI, Python, Go and TypeScript SDKs (software development kits), an [MCP](../index/model-context-protocol.md) (Model Context Protocol) endpoint and plugins for Claude Code, Codex, Cursor, OpenCode and others [4]. Volcano Engine, the README's copyright holder, also sells a managed edition [4].

Its own description is a file tree plus a vector index [4][6], not a [knowledge graph](../index/knowledge-graph.md) store. The README mentions graphs only for an optional `ov compile` job that can organise sources into a wiki, a knowledge graph or a report [4].

## How it works

| Part | Behaviour | Source |
|---|---|---|
| Storage | Two layers: a file store (RAGFS) for content, and a vector index holding URIs, vectors, metadata and abstracts | [6] |
| Summaries | L0 abstract (default 256 characters) and L1 overview (4,000), kept as hidden files per directory; L2 is the original. A background queue writes them bottom-up | [6][7] |
| Memory | Committing a session archives the messages, then a background step extracts memories by type (`profile`, `preferences`, `entities`, `events` and others). `cases`, `trajectories` and `experiences` belong to an Agent Evolution pipeline with its own switch | [9] |
| Retrieval | `find` runs one [vector search](../index/vector-search.md) inside the permitted scope. `search` can add an LLM (large language model) intent step that generates zero or more typed queries, then runs one vector search each. With a [reranker](../index/reranking.md) configured, `search` recalls twice the limit and reranks once. The docs say retrieval "does not navigate directories recursively" | [6][8] |
| Models | Index time: summaries. Commit: memory extraction. Query: optional intent step and rerank. The calling agent writes the answer | [6][8][9] |

Working memory (a summary generated at commit) is off by default; a commit then stores raw messages and schedules extraction [10].

*Reading:* a file tree with model-written summaries over a flat vector search. It sits between [agent memory](../index/agent-memory.md) layers that store extracted records and wikis a model maintains as files, hence two trends.

## Evidence

All published results are first-party, from the OpenViking Team's report of 20260529 [12].

| Test | Result | Source |
|---|---|---|
| [LoCoMo](../datasets/locomo.md) accuracy, agent's own memory to agent plus OpenViking | OpenClaw 24.20% to 82.08%; Hermes 33.38% to 82.86%; Claude Code 57.21% to 80.32% | [12] |
| tau2-bench task success, same model without and with experience memory | Retail 70.94% to 77.81%; airline 54.38% to 66.25% | [12] |
| [HotpotQA](../datasets/hotpotqa.md) accuracy and tokens per question | OpenViking top-20 91.00%, 12,533; [LightRAG](./lightrag.md) 89.00%, 28,443; naive RAG (retrieval-augmented generation) 62.50%; [HippoRAG 2](./hipporag.md) 61.00% | [12] |
| Five single-turn sets (FinanceBench, NaturalQuestions, ClapNQ, Qasper, SyllabusQA), average accuracy | LightRAG 76.00%; OpenViking 66.87%; naive RAG 53.93%; HippoRAG 2 44.50%; [PageIndex](./pageindex.md) 36.75%. Indexing tokens: OpenViking 8,671,538, LightRAG 62,705,469 | [12] |

*Reading:* the LoCoMo baselines are each agent's built-in memory, not other memory systems, so the gain shows OpenViking beats three built-in memories under the project's setup. On the five-set average LightRAG scores higher. Against LightRAG and HippoRAG 2, OpenViking needs fewer indexing tokens (LightRAG 62,705,469 above; HippoRAG 2 124,963,618); against LightRAG, HippoRAG 2 and PageIndex it needs less retrieval time (0.19s against 9.19s, 18.83s and 84.60s). Naive RAG and PageIndex index with fewer tokens (2,755,356 and 5,609,206), and naive RAG retrieves faster (0.13s here; 0.11s against OpenViking's 0.22s to 0.23s on HotpotQA) [12].

The README names Doubao 2.0 Pro and Doubao-embedding-vision-251215 for the memory run [4]; the report names no judge model and no question counts [12]; the repository's guide says it "does not pin every runtime parameter" [13].

Three papers the README lists under Research [4] are not independent evaluations (abstracts only): VikingMem, "up to 30%" better memory retrieval, accepted at VLDB (Very Large Data Bases conference) 2026, not naming OpenViking [15]; Directory-Aware Query and Maintenance in Vector Databases, whose trie index "has been integrated into OpenViking" [16]; VikingRAG, 11.6% to 51.9% of other methods' tokens at matching accuracy [17].

Independent evaluation: none found. An arXiv search for the name returned one of those papers, an unrelated one, and a framework paper analysing OpenViking among four systems without measurements [18][19]. The Agent Memory Leaderboard files read list no OpenViking entry [20].

## Status and direction

Active: pushed to within 90 days, not archived [1]. Latest release v0.5.3, 20261102: 98 commits adding a Rules service (Beta), path-lock fixes and a multi-replica gateway, and removing legacy session paths [5]. Since 20260804: 1,199 commits and 18 version releases, v0.4.13 to v0.5.3 [21]. The roadmap lists two items, "Further distributed-storage development" and "More agent-framework adapters", without dates [11].

**Hosted tier and licence.** The `LICENSE` file was Apache-2.0 until commit `ce998873f9` of 20260330, which changed it to AGPL-3.0 [14]. A maintainer's post of 20260326 said Apache-2.0 "imposes weak restrictions on commercial service providers" and announced a managed cloud [22]. The README now sells Managed SaaS (software as a service) and a Self-Managed edition "activated by a license key", and says the open-source server needs no key [4]. It also adds a sentence outside `LICENSE` that "wholesale rewriting and subsequent re-open-sourcing" is prohibited; whether that is a licence term is unstated [4].

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Projects](README.md)

**Index**

- [LLM wiki](../index/llm-wiki.md)

<!-- END GENERATED: appears-in -->

## Sources

Agent-memory papers as a field: [group page](../papers/agent-memory.md). Archive entry with longer notes: [kb-kg/projects/openviking.md](../../kb-kg/projects/openviking.md).

1. https://api.github.com/repos/volcengine/OpenViking : description, creation, not archived (read 20261102 20:10 UTC)
2. https://api.github.com/repos/volcengine/OpenViking/license : GitHub's classification of `LICENSE` as AGPL-3.0 (read 20261102 20:10 UTC)
3. https://github.com/volcengine/OpenViking/blob/main/LICENSE : word-level comparison with https://www.gnu.org/licenses/agpl-3.0.txt (read 20261102 20:15 UTC)
4. https://github.com/volcengine/OpenViking/blob/main/README.md : pitch, `viking://`, integrations, evaluation setup, editions, per-component licence section, research list (read 20261102 20:10 UTC; licence section re-read 20261102 20:34 UTC)
5. https://github.com/volcengine/OpenViking/releases/tag/v0.5.3 : latest release and its notes (read 20261102 20:10 UTC)
6. https://github.com/volcengine/OpenViking/blob/main/docs/en/concepts/01-architecture.md : modules, storage layers, data flows (read 20261102 20:11 UTC)
7. https://github.com/volcengine/OpenViking/blob/main/docs/en/concepts/03-context-layers.md : L0, L1, L2 (read 20261102 20:11 UTC)
8. https://github.com/volcengine/OpenViking/blob/main/docs/en/concepts/07-retrieval.md : `find`, `search`, intent ("zero or more TypedQueries"), rerank (read 20261102 20:11 UTC; re-read 20261102 20:34 UTC)
9. https://github.com/volcengine/OpenViking/blob/main/docs/en/concepts/08-session.md : commit, memory types (read 20261102 20:11 UTC)
10. https://github.com/volcengine/OpenViking/blob/main/docs/en/guides/working-memory-default-off.md : working memory off by default (read 20261102 20:11 UTC)
11. https://github.com/volcengine/OpenViking/blob/main/docs/en/about/03-roadmap.md : stated roadmap (read 20261102 20:11 UTC)
12. https://blog.openviking.ai/post/openviking-benchmark-results/ : all first-party results in the Evidence tables, including indexing tokens and retrieval latency of every system in the five-set table (read 20261102 20:10 UTC; re-read 20261102 20:35 UTC)
13. https://github.com/volcengine/OpenViking/blob/main/benchmark/README.md : reproduction caveat (read 20261102 20:11 UTC)
14. https://github.com/volcengine/OpenViking/commit/ce998873f9 : licence change; `LICENSE` history lists two commits, the first Apache-2.0 (read 20261102 20:15 UTC)
15. https://arxiv.org/abs/2605.29640 : VikingMem, v1 20260528, "Accepted by VLDB26" (read 20261102 20:10 UTC, abstract via the arXiv API)
16. https://arxiv.org/abs/2606.16903 : Directory-Aware Query and Maintenance in Vector Databases, 20260615 (read 20261102 20:10 UTC, abstract)
17. https://arxiv.org/abs/2609.11390 : VikingRAG, 20260910 (read 20261102 20:10 UTC, abstract)
18. https://arxiv.org/abs/2603.20578 : Context Cartography, 20260321, analyses OpenViking among four systems (read 20261102 20:10 UTC, abstract)
19. https://export.arxiv.org/api/query?search_query=all:OpenViking : three entries (read 20261102 20:10 UTC)
20. https://github.com/AML-memory/agent-memory-leaderboard : README and `data/generated` JSON files at the commit it links, searched for the name (read 20261102 20:14 UTC)
21. https://api.github.com/repos/volcengine/OpenViking/commits?since=2026-08-04T00:00:00Z and `/releases` : 1,199 commits; 18 version tags (read 20261102 20:10 UTC)
22. https://github.com/volcengine/OpenViking/discussions/992 : "Plan to change lisence", 20260326 (read 20261102 20:11 UTC)
