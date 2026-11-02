---
type: project
repo: mem0ai/mem0
trends: [agent-memory, features-in-and-out]
updated: 20261102 23:17 UTC
---

# Mem0

This page answers what Mem0 is, how its memory pipeline works today, and who has measured it. It also records the fact that matters most for the trend pages: the graph store was removed from the open-source code in April 2026 and now exists only on the hosted platform [6][7].

| Field | Value |
|---|---|
| Repository | https://github.com/mem0ai/mem0 [1] |
| Licence | Apache-2.0. GitHub classifies the `LICENSE` file as Apache-2.0 [2]; the README says Apache 2.0 [3]. |
| Trends | [Agent memory](../trends/agent-memory.md) · [Graph features removed and added](../trends/features-in-and-out.md) |

## What it is

Mem0 ("mem-zero") is a memory layer for [LLM](../index/large-language-model.md) (large language model) applications and agents; the repository calls it "The Memory Layer for AI Agents" [1]. An application sends conversation messages, a language model extracts short memories, and they are stored with [embeddings](../index/embedding.md) and searched later by user, agent or run [3][8].

It comes as a library (Python and npm), a self-hosted server, and a hosted Platform [3]. The open-source code and the Platform share an API shape but not all features [7].

## How it works

This describes the open-source library after the 20260414 release (Python 2.0.0, TypeScript 3.0.0), the "V3" algorithm [6][8].

**Write.** `add()` makes one extraction call with one operation, ADD. The earlier pipeline made two calls and could also UPDATE or DELETE; now nothing is overwritten [8]. The library then extracts entities with spaCy (no LLM) and links each to the memories that mention it in a second vector collection, `{collection}_entities` [8].

**Read.** `search()` combines three signals: semantic similarity, [BM25](../index/bm25.md) (Best Matching 25, a keyword ranking function) keyword match and an entity boost, scored together [8]. BM25 and entity matching need the optional `[nlp]` install, and keyword search was added to 15 of the supported [vector stores](../index/vector-search.md) [3][8]. Defaults changed at the same time: `top_k` 100 to 20, `threshold` none to 0.1, and [reranking](../index/reranking.md) is off [6].

**Scope and defaults.** Memories are scoped by `user_id`, `agent_id` and `run_id` [7]. The defaults are OpenAI's `gpt-5-mini` and `text-embedding-3-small` [3].

**What "graph" has meant.** In the open-source library, `enable_graph` plus a `graph_store` block connected an external [graph database](../index/graph-database.md) such as [Neo4j](./neo4j.md) or [Memgraph](./memgraph.md). The V3 release deleted that integration [6][7]; no `mem0/graphs` folder remains in the file tree [9]. On the Platform, "Graph Memory" is built in and always on. The open-source library keeps only the entity links above: the comparison page says there is "no queryable graph and no `relations` field" [7].

**Platform only.** Temporal reasoning, memory decay, background consolidation ("Dream"), custom categories and webhooks [7].

## Evidence

Every score below is published; none was reproduced here.

**First-party, paper (arXiv, 20250428).** On the [LoCoMo](../datasets/locomo.md) benchmark the authors report a 26% relative gain in an [LLM-as-a-judge](../index/llm-as-judge.md) score over OpenAI's memory, a graph variant about 2% above the base one, and, against full context, a 91% lower p95 latency and over 90% less token cost [10]. Accuracy against full context is not in the abstract: **unstated** here.

**First-party, README (2026).** A table headed "New Memory Algorithm (April 2026)" gives LoCoMo 71.4 to 92.5, [LongMemEval](../datasets/longmemeval.md) 67.8 to 94.4, BEAM 64.1 at 1M tokens and 48.6 at 10M. The README states a top_200 retrieval budget for that table only, and adds: "Scores reflect Mem0's managed platform, which includes proprietary optimizations not available in the open-source SDK" (software development kit) [3]. The migration guide gives lower figures for the open-source algorithm, 91.6 on LoCoMo and 93.4 on LongMemEval; the retrieval budget of those runs is **unstated** [6]. The library default is 20 [6]. The README names no extraction or judge model: **unstated**.

**Independent, with a stake of its own.** Bao et al. (arXiv, 20261022) audited Mem0 1.0.11: UPDATE and DELETE were 4.39% of 33,902 write decisions on LoCoMo and 2.46% of 428,858 on LongMemEval. Replacing UPDATE with ADD and DELETE with NONE moved LoCoMo accuracy from 67.36 to 69.42 [11]. Their Table 3 puts Mem0 at 66.40 on LongMemEval against 87.53 for their own baseline, "Raw-RAG", which they propose [11]. The audit covers the older write policy, not the ADD-only pipeline [11].

**First-party, competitors (not replications).** Zep's post (20250506, updated 20260603) gives its own LoCoMo score as 75.14% ± 0.17 (a corrected figure) against 65.99% in Mem0's paper. A banner now announces newer Zep scores, "80% at <200ms latency"; its printed date, "December 9, 2015", cannot be right, so its date is **unstated** [12]. Letta's post (20250812) reports 74.0% for an agent that stores conversations in files, with GPT-4o mini, against Mem0's reported 68.5% for its graph variant [13].

## Status and direction

*Release.* `ts-v3.3.1`, 20260925 17:36 UTC, is GitHub's latest. Python `v2.2.1` came a minute earlier; no later release is listed [4].

*Activity in the last 90 days.* 127 commits to `main` from 20260804 to 20261102: 68 in August (from the 4th), 48 in September, 11 in October; the last was 20261030 [5]. By subject prefix, 59 are `fix` and 33 `docs` (computed) [5]. Whether the falling count means work moved to other branches is **unstated**.

*Direction.* The graph store left the open-source code on 20260414 [6][8], and the Platform-only list is long [7]. Recent commits are mostly fixes, docs, plugins and CLI (command-line interface) work [5]. No roadmap file appears in the repository tree [9].

*Reading:* the project is active, not archived [1], and steers new capability to the hosted tier. For the trend, the clearest data point is the graph removal: the paper's graph variant describes a feature the open-source library no longer has.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Claude-Mem](claude-mem.md)
- [Cognee](cognee.md)
- [Graphify](graphify.md)
- [Graphiti](graphiti.md)
- [Hindsight](hindsight.md)
- [HippoRAG](hipporag.md)
- [Letta](letta.md)
- [MemOS](memos.md)
- [MIRIX](mirix.md)
- [Projects](README.md)

**Papers**

- [Papers: Agent memory](../papers/agent-memory.md)

**Datasets**

- [LoCoMo](../datasets/locomo.md)
- [LongMemEval](../datasets/longmemeval.md)

**Benchmarks**

- [LoCoMo](../benchmarks/locomo.md)
- [LongMemEval](../benchmarks/longmemeval.md)
- [MemoryAgentBench](../benchmarks/memoryagentbench.md)

**Index**

- [Agent memory](../index/agent-memory.md)
- [Hybrid search](../index/hybrid-search.md)
- [Selective forgetting](../index/selective-forgetting.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/mem0ai/mem0 : repository metadata, description, archived flag (read 20261102 20:09 UTC)
2. https://api.github.com/repos/mem0ai/mem0/license : licence file text and GitHub's classification (read 20261102 20:09 UTC)
3. https://api.github.com/repos/mem0ai/mem0/readme : forms, defaults, benchmark table with its top_200 budget and platform caveat, CLI, licence line (read 20261102 20:32 UTC)
4. https://api.github.com/repos/mem0ai/mem0/releases?per_page=6 : latest release `ts-v3.3.1`, Python `v2.2.1`, no later release (read 20261102 20:34 UTC)
5. https://api.github.com/repos/mem0ai/mem0/commits?since=2026-08-04 : activity, subjects, last commit date; 127 commits, paged (read 20261102 20:10 UTC)
6. https://github.com/mem0ai/mem0/blob/main/docs/migration/oss-v2-to-v3.mdx : breaking changes, graph removal, default changes, open-source scores; it states no retrieval budget for them (read 20261102 20:32 UTC)
7. https://github.com/mem0ai/mem0/blob/main/docs/platform/platform-vs-oss.mdx : feature comparison of open source and Platform (read 20261102 20:11 UTC)
8. https://github.com/mem0ai/mem0/blob/main/docs/changelog/sdk.mdx : release notes for 2.0.0 and later (read 20261102 20:11 UTC)
9. https://api.github.com/repos/mem0ai/mem0/git/trees/main?recursive=1 : file tree (no `mem0/graphs`, vector-store modules, no roadmap file) (read 20261102 20:13 UTC)
10. https://arxiv.org/abs/2504.19413 : Chhikara et al., "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory", abstract (read 20261102 20:12 UTC)
11. https://arxiv.org/html/2610.30755v1 : Bao et al., "Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought", abstract and tables; abstract page https://arxiv.org/abs/2610.30755 (read 20261102 20:12 UTC)
12. https://www.getzep.com/blog/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/ : Zep's rebuttal, corrected score, post and update dates, newer-scores banner (read 20261102 20:32 UTC)
13. https://www.letta.com/blog/benchmarking-ai-agent-memory : Letta's file-based agent result, post date 20250812 (read 20261102 20:32 UTC)

Further reading in the archive: [Mem0, long entry](../../kb-kg/projects/mem0.md). Papers: [agent memory group](../papers/agent-memory.md).
