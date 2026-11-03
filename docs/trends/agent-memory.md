---
type: trend
shift: retrieving documents -> remembering across sessions
status: growing
order: 7
updated: 20261102 23:17 UTC
---

# Agent memory: from retrieving documents to remembering across sessions

This page answers three questions: what [agent memory](../index/agent-memory.md) is as a family of approaches, why it appeared, and what is known about whether it works. It covers systems that keep what an agent learned across sessions and decide what to update or drop, where [retrieval-augmented generation](../index/retrieval-augmented-generation.md) (RAG) only reads a fixed document set. Three sub-themes are told below: [temporal knowledge graphs](../index/temporal-knowledge-graph.md), write policies, and governed and attacked memory.

> **Distinctive because** sessions write to the store and a write policy decides what is kept, updated or dropped: Mem0 only adds, Letta's agents rewrite, Graphiti invalidates [3][5][9]. Its nearest neighbour, [graph-based RAG](./graph-based-rag.md), indexes a corpus in batches and updates it on demand.

## Why it emerged

A [large language model](../index/large-language-model.md) (LLM) has a [context window](../index/context-window.md) and no state between calls. RAG fetches from a fixed document set; it does not record what happened in this conversation. Two 2023 papers named the gap. MemGPT proposed "virtual context management", borrowed from operating systems [16]. Generative Agents stored an agent's experiences in natural language, synthesised them into reflections and retrieved them to plan [17]. In January 2025 the Zep paper stated the limit: RAG frameworks "are limited to static document retrieval, enterprise applications demand dynamic knowledge integration" [18]. The Mem0 paper (April 2025) offered a pipeline that extracts, consolidates and retrieves facts from conversations [20]. A survey of December 2025 says the field "has also become increasingly fragmented" and separates agent memory from RAG and context engineering [22]. The earlier step is in [chapter 1](../history/language-models-meet-retrieval.md).

## Why it matters

Activity is high. Stars are signals, not verdicts. The 20261030 19:54 UTC snapshot lists 199 repositories in its agent-memory category that were pushed within 90 days and are not archived; the snapshot's search returns at most 100 results per query, so this is a lower bound [1]. The top three memory layers by stars at that date are [claude-mem](../projects/claude-mem.md) (105,979), [Mem0](../projects/mem0.md) (68,112) and [Hindsight](../projects/hindsight.md) (56,614); claude-mem and Hindsight carry the snapshot's fast-growth flag [1]. Two other repositories of the category rank among them but are not memory layers: MiroFish (82,864; a swarm-prediction engine) and ai-agent-book (56,669; a book repository) [1]. In the category, 123 of the 199 name or describe "memory", "memories", "remember" or "recall"; across all categories the same match finds 173 of 552 active repositories [1]. The share that are memory layers is unstated.

Papers rose faster than the field. The title query for agent-memory wording ("agent memory", "long-term memory", "memory system" and similar in the title, with agent or LLM in the abstract) returns 482 results for submissions from 20251102 to 20261102, against 53 for the year before, a ratio of 9.1. A control for any LLM-agent wording gives a ratio of 2.5 with an LLM clause (15,158 against 6,068) and 2.3 without it (30,534 against 13,438) [2]. These are keyword hits, with hardware "memory" papers as noise, not a count of papers in the field.

A wrong or injected record persists between sessions; that is why governance appears below.

## How it works

Every system answers four questions: what to write after a session, what shape to store it in, how to read it back into the prompt, and what to do with it later. Families differ mostly in the first and last.

| Family | Stores | Update or forget, as the project states it |
|---|---|---|
| Extract and store facts | Fact records, [embedded](../index/embedding.md) and entity-linked [3]; Hindsight keeps four networks: world facts, experiences, entity summaries, beliefs [21] | [Mem0](../projects/mem0.md): "Single-pass ADD-only extraction -- one LLM call, no UPDATE/DELETE" [3]. [Hindsight](../projects/hindsight.md): operations retain, recall, reflect [6][21] |
| Graph with time | Entities, facts with validity windows, source episodes | [Graphiti](../projects/graphiti.md): a changed fact is invalidated, not deleted [5]. [Cognee](../projects/cognee.md): `remember`, `recall`, `improve`, `forget` [7] |
| Self-managed | Notes or files the agent edits | [Letta](../projects/letta.md): agents rewrite their own memory; all context is tracked in git (MemFS) [9]. A-MEM: a new note can update existing ones [19]. [MIRIX](../projects/mirix.md): six memory types with one agent each; an auto-dream call merges duplicates and resolves stale entries [13] |
| Filesystem | A tree of files an agent browses | [OpenViking](../projects/openviking.md): a `viking://` virtual filesystem with `ls`, `tree`, `read`, `write`, `grep` [10]. Anthropic's memory tool: a client-side `/memories` directory [15] |
| Managed service beside open code | The same layer as a hosted product | Mem0 moved graph memory out of its open source; it is now a Platform feature [4]. Zep is the hosted counterpart of Graphiti [5] |

A model is used at write time to extract and consolidate (one call per add in Mem0 [3]); Cognee states that ingestion, retrieval and session storage work without an LLM [7]. A fixed pipeline steers Mem0 and Graphiti; the agent itself steers Letta, A-MEM and MIRIX [3][5][9][19][13].

Two neighbours also update. Graph-based RAG is not static: [LightRAG](../projects/lightrag.md) (40,443 stars at the 20261030 19:54 UTC snapshot [1]) advertises "Incremental Updates & Selective Deletion" [39], and the second [HippoRAG](../projects/hipporag.md) paper is titled "From RAG to Memory" [23]. There the corpus changes, not the session. [Plain-file knowledge](./plain-file-knowledge.md) also keeps files, but as pages a model maintains and a person reads; Mem0, Graphiti and Cognee keep extracted records in vector or graph stores [3][5][7]. OpenViking sits on both pages.

### Temporal knowledge graphs

Graphiti gives every fact a validity window and keeps raw episodes as provenance; its README contrasts GraphRAG's "Basic timestamp tracking" with "Explicit [bi-temporal](../index/bi-temporal-model.md) tracking with automatic fact invalidation" [5]. A fact's validity window runs from "when it became true" to "when (if ever) it was superseded" [5]. Mem0's README adds time-aware ranking on a flat store [3]. *Reading:* this is a sub-theme, not a trend of its own, because time is a design axis of all memory. A keyword query for temporal-graph and stale-fact wording returns 96 results for the last year against 10 the year before [2]. MemStrata keeps a bi-temporal ledger and retires stale values with a rule and no LLM call (single author, own benchmarks) [31]. RoMem rotates obsolete facts out of phase instead of deleting them [32].

### Write policies

Whether a memory layer should overwrite is contested. Mem0 moved to add-only writes in its 20260414 release [3][4]. An audit by authors who are not Mem0's, run on Mem0 1.0.11 (before that release), found UPDATE and DELETE were 4.39% of 33,902 write decisions on [LoCoMo](../datasets/locomo.md); replacing them with ADD and NONE raised accuracy from 67.36% to 69.42% [24]. Memory-R1 goes the other way and trains a manager with [reinforcement learning](../index/reinforcement-learning.md) to choose ADD, UPDATE, DELETE or NOOP [26] (see [learned graph traversal](./learned-graph-traversal.md)). *Reading:* the write choice, "what to keep", is what separates memory from retrieval.

### Governed and attacked memory

Persistent memory is an attack surface and a compliance object. MINJA showed that records can be injected into an agent's memory by queries alone [33]. MemForm is a benchmark for [memory poisoning](../index/memory-poisoning.md) at the point where memories are formed [34]; SAFE-Mem labels each stored claim with authority and scope [35]; GateMem tests access control and forgetting for shared memory [36]. Keyword counts for these themes rose faster than the memory query: 326 against 41 for governance, provenance or audit wording; 133 against 9 for memory poisoning or injection wording [2]. Both are noisy keyword hits. *Reading:* these themes are not a retrieval approach; they act on the same store and write path, so they stay in this family.

## Representative projects

| Project | Approach | Licence (LICENSE file) | Stars at 20261030 19:54 UTC |
|---|---|---|---|
| [claude-mem](../projects/claude-mem.md) | tool-use capture for a coding agent [11] | Apache-2.0 since 20260508; AGPL-3.0 from 20250911 to 20260508 [14][40] | 105,979 [1] |
| [Mem0](../projects/mem0.md) | extract facts, add only [3] | Apache-2.0 [14] | 68,112 [1] |
| [Hindsight](../projects/hindsight.md) | retain, recall, reflect [6] | MIT [14] | 56,614 [1] |
| [OpenViking](../projects/openviking.md) | virtual filesystem [10] | AGPL-3.0 since 20260330; Apache-2.0 before [14][40] | 41,197 [1] |
| [Cognee](../projects/cognee.md) | graph, vector and relational stores [7] | Apache-2.0 [14] | 32,934 [1] |
| [Graphiti](../projects/graphiti.md) | temporal context graph [5] | Apache-2.0 [14] | 32,373 [1] |
| [Letta](../projects/letta.md) | self-managed memory in git [9] | Apache-2.0 [14] | 25,294 (7 commits in 90 days; the old server is retired) [1][8] |
| [MemOS](../projects/memos.md) | memory operating system [12] | Apache-2.0 [14] | 12,200 [1] |
| [MIRIX](../projects/mirix.md) | six memory types, one agent each [13] | Apache-2.0 since 20250711; MIT before [14][40] | 3,456 [1] |

Three of the nine files changed licence in 2025 and 2026 (claude-mem, OpenViking, MIRIX), read from the commit history of each `LICENSE` file [40]; the other six show no change in those years. The moves of claude-mem and OpenViking sit beside hosted or reserved commercial parts and are told on [features in and out](./features-in-and-out.md).

## Fundamental papers

The relations are on [the agent-memory paper group](../papers/agent-memory.md). The chain runs from MemGPT [16] and Generative Agents [17] through Zep [18], A-MEM [19], Mem0 [20] and Hindsight [21] to the December 2025 survey [22]; HippoRAG 2 [23] bridges from graph-based RAG. Benchmarks: LoCoMo [37], [LongMemEval](../datasets/longmemeval.md) [38].

## What is measured, and by whom

Most published scores are first-party, on two conversational benchmarks (LoCoMo, LongMemEval), with setups that differ between projects. Independent studies are fewer.

| Who ran it | Result | First-party? |
|---|---|---|
| Mem0 authors, paper | on LoCoMo, graph variant "around 2% higher overall" than the base; 26% relative gain over OpenAI on the [LLM-as-a-judge](../index/llm-as-judge.md) metric [20] | yes |
| Mem0 authors, README | LoCoMo 92.5 and LongMemEval 94.4 (April 2026 algorithm); scores reflect the managed platform, "proprietary optimizations not available in the open-source SDK" (software development kit) [3] | yes |
| Zep authors, paper | Deep Memory Retrieval (DMR) 94.8% against 93.4% for MemGPT; LongMemEval gains "up to 18.5%" with 90% lower latency [18] | yes |
| Hindsight authors, paper | LongMemEval 91.4% and LoCoMo 89.61% with a scaled backbone; 83.6% with a 20B model [21]. The README says Virginia Tech and The Washington Post reproduced the data [6]; not located here | yes |
| OpenViking authors, README | LoCoMo 80-83% with OpenViking against 24-57% on native memory, with the Doubao 2.0 Pro model [10] | yes |
| [MemoryAgentBench](../benchmarks/memoryagentbench.md) authors (Hu, Wang, McAuley), v4, GPT-4o-mini unless stated | overall: long-context (GPT-4o-mini) 42.2, HippoRAG-v2 41.6, [BM25](../index/bm25.md) 41.5, MemGPT 28.3, MIRIX 26.2 (37.7 with GPT-4.1-mini), Zep 24.0, Mem0 21.1, Cognee 20.6; the table's GPT-5-mini long-context row scores 60.6 [25] | no (the benchmark's authors report all systems) |
| Bao et al. 20261022 | raw dense retrieval plus reranking ranks first in six of seven benchmark-model settings, by 0.13 to 5.53 points over the strongest agentic memory system [24] | no |
| Memory Tax authors 20261025 | "many dedicated memory systems underperform naive RAG in many cases" [28] | no |
| Zhou et al. 20260623 | 12 systems, five workloads: "no single architecture dominates" [27] | no |
| ReFind authors 20260813 | keyword search over raw chat logs, 58.2, above HippoRAG 2 at 53.2, under MemoryAgentBench's incremental setting [30] | yes for ReFind |

Experiments in this documentation that test this trend: none.

## Assessment

*Reading:* Strengths. The problem is real and a 47-author survey maps the design space [22]. Open code is plentiful and mostly permissively licensed [14]. Some designs have a clear mechanism, such as Graphiti's invalidation instead of deletion [5].

*Reading:* Weaknesses. The large scores come from each system's own authors, on setups that differ, and some belong to code that has changed: Mem0's graph evidence concerns a feature its open source removed, and its best 2026 numbers use platform-only optimisations [3][4][20]. Where others ran the systems, plain retrieval is level with or ahead of memory layers [24][25][28], and no design wins everywhere [27][29]. Nothing read here shows that a memory graph beats plain retrieval for agents. Most independent studies are preprints, read at abstract or table level.

*Reading:* Where it is heading. Studies favouring raw history and search (see [agentic search](./agentic-search.md)) pull against products that add structure and governance. One proposal is memory chosen by workload, "substrate routing" [29]. Forgetting and governance are the least measured parts.

## Signals to watch

- A re-run of Graphiti, Zep, Cognee, OpenViking or Hindsight on LoCoMo, LongMemEval or MemoryAgentBench by authors with no stake in the result.
- A second version of Bao et al. [24], or Mem0 stating which of its cells were re-run (latest release read: ts-v3.3.1, 20260925 [3]).
- The Hindsight reproduction its README names [6]; an evaluation of Letta's MemFS [9].
- Kuzu, a Graphiti backend its README marks "deprecated", removed [5]; more on [features in and out](./features-in-and-out.md).
- A second snapshot to compare the 199 active repositories and the star order [1].

## Sources

1. ../../kb-kg/landscape/20261030_1954-github/repos.tsv : stars, push dates, flags and category counts (snapshot 20261030 19:54 UTC; analysed 20261102 20:14 UTC, counts re-run 20261102 20:51 to 20:53 UTC). "Active" means archived is false and days_since_push is at most 90; the 123 and 173 are a case-insensitive match of memor(y|ies), remember or recall in the full_name and description columns, in the agent-memory category and in all categories (552 active); the star order of the category was re-read at the same time
2. https://export.arxiv.org/api/query : counts (field totalResults), window submittedDate 202511020000 to 202611022359 against 202411020000 to 202511012359, read 20261102 20:22 UTC. (a) 482 and 53: `(ti:"agent memory" OR ti:"memory for agents" OR ti:"memory for LLM agents" OR ti:"memory for AI agents" OR ti:"agentic memory" OR ti:"memory system" OR ti:"memory architecture" OR ti:"long-term memory" OR ti:"memory layer") AND (abs:agent OR abs:agents OR abs:LLM OR abs:"language model")`. (b) 326 and 41: `(abs:provenance OR abs:governance OR abs:governed OR abs:"access control" OR abs:auditable OR abs:"audit trail") AND (ti:memory OR ti:"knowledge graph" OR ti:GraphRAG OR ti:"knowledge base") AND (abs:agent OR abs:agents OR abs:LLM)`. (c) 133 and 9: `(abs:"memory poisoning" OR abs:"memory injection" OR abs:"poisoned memory" OR abs:"persistent memory" OR ti:"memory attack") AND (abs:attack OR abs:security OR abs:injection OR abs:vulnerability OR abs:vulnerabilities) AND (abs:agent OR abs:agents)`. (d) 96 and 10, temporal wording: `(abs:"temporal knowledge graph" OR abs:"bi-temporal" OR abs:"temporal memory graph" OR abs:"temporal graph memory" OR abs:Graphiti OR abs:Zep OR abs:"stale facts" OR abs:"fact invalidation" OR abs:"temporal validity") AND (abs:agent OR abs:agents OR abs:memory)`. (e) Control, any LLM-agent wording, with the LLM clause, 15,158 and 6,068: `(abs:agent OR abs:agents OR abs:"LLM agent" OR abs:"LLM agents") AND (abs:LLM OR abs:"language model")`; without the clause, 30,534 and 13,438: `abs:agent OR abs:agents OR abs:"LLM agent" OR abs:"LLM agents"`. Each query was wrapped in parentheses before the date filter was added. All six queries, both windows, were re-run 20261102 20:59 to 21:00 UTC and gave the counts above
3. https://github.com/mem0ai/mem0 : README, April 2026 algorithm table, caveat, ADD-only extraction (read 20261102 20:11 UTC); latest release ts-v3.3.1, 2026-09-25, via the GitHub releases endpoint (read 20261102 20:16 UTC)
4. https://github.com/mem0ai/mem0/blob/main/docs/migration/oss-v2-to-v3.mdx and docs/changelog/sdk.mdx : graph memory removed from open source; v2.0.0 dated 2026-04-14 (read 20261102 20:12 UTC)
5. https://github.com/getzep/graphiti : README: validity windows, invalidation, bi-temporal comparison, Kuzu deprecated (read 20261102 20:11 UTC)
6. https://github.com/vectorize-io/hindsight : README: operations, reproduction statement (read 20261102 20:11 UTC)
7. https://github.com/topoteretes/cognee : README: operations, works without an LLM for ingestion and retrieval (read 20261102 20:11 UTC)
8. https://github.com/letta-ai/letta : README: current source moved to letta-code, V1 server retired (read 20261102 20:11 UTC)
9. https://github.com/letta-ai/letta-code : README: agents rewrite their own memory; MemFS tracks context in git (read 20261102 20:15 UTC)
10. https://github.com/volcengine/OpenViking : README: virtual filesystem, LoCoMo claim (read 20261102 20:11 UTC)
11. https://github.com/thedotmack/claude-mem : README: captures tool usage observations and summaries (read 20261102 20:11 UTC)
12. https://github.com/MemTensor/MemOS : README: memory operating system, LoCoMo and LongMemEval (read 20261102 20:11 UTC)
13. https://github.com/Mirix-AI/MIRIX : README: six memory types, auto-dream; repository metadata (read 20261102 20:12 UTC)
14. https://api.github.com/repos/mem0ai/mem0/license : the licence endpoint (LICENSE file) of Mem0, and the same endpoint for the other eight repositories of the table, whose owner and name are in sources 5 to 13 (read 20261102 20:11 to 20:12 UTC)
15. https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool : memory tool, client-side `/memories` (read 20261102 20:15 UTC)
16. https://arxiv.org/abs/2310.08560 : MemGPT (Packer, Wooders, Lin and 4 more; 20231012) (read 20261102 20:12 UTC)
17. https://arxiv.org/abs/2304.03442 : Generative Agents (Park, O'Brien, Cai and 3 more; 20230407) (read 20261102 20:13 UTC)
18. https://arxiv.org/abs/2501.13956 : Zep (Rasmussen, Paliychuk, Beauvais and 2 more; 20250120) (read 20261102 20:12 UTC)
19. https://arxiv.org/abs/2502.12110 : A-MEM (Xu, Liang, Mei and 3 more; 20250217; NeurIPS 2025) (read 20261102 20:12 UTC)
20. https://arxiv.org/abs/2504.19413 : Mem0 (Chhikara, Khant, Aryan and 2 more; 20250428) (read 20261102 20:12 UTC)
21. https://arxiv.org/abs/2512.12818 : Hindsight (Latimer, Boschi, Neeser and 4 more; 20251214) (read 20261102 20:12 UTC)
22. https://arxiv.org/abs/2512.13564 : Memory in the Age of AI Agents (Hu, Liu, Yue and 44 more; 20251215); abstract quote re-checked (read 20261102 20:13 UTC, again 21:00 UTC)
23. https://arxiv.org/abs/2502.14802 : From RAG to Memory, HippoRAG 2 (Gutierrez, Shu, Qi and 2 more; 20250220; ICML 2025); title re-checked (read 20261102 20:13 UTC, again 21:00 UTC)
24. https://arxiv.org/abs/2610.30755 : Bao et al., Raw-RAG and the Mem0 write audit (20261022); abstract and full text (read 20261102 20:13 UTC)
25. https://arxiv.org/abs/2507.05257 : MemoryAgentBench (Hu, Wang, McAuley; 20250707, v4 20260628); Table 3, "Overall" column, from the HTML version (read 20261102 20:14 UTC, again 21:00 UTC)
26. https://arxiv.org/abs/2508.19828 : Memory-R1 (Yan, Yang, Huang and 10 more; 20250827) (read 20261102 20:13 UTC)
27. https://arxiv.org/abs/2606.24775 : Are We Ready For An Agent-Native Memory System? (Zhou, Zhou, Han and 5 more; 20260623) (read 20261102 20:13 UTC)
28. https://arxiv.org/abs/2610.34073 : Memory Tax (He, Zhoubian, Yang and 8 more; 20261025) (read 20261102 20:13 UTC)
29. https://arxiv.org/abs/2608.15008 : Harness the Memory (Huang, Zhang, Wu and 12 more; 20260815) (read 20261102 20:13 UTC)
30. https://arxiv.org/abs/2608.12888 : ReFind (Li, Zhang, Xu and 3 more; 20260813) (read 20261102 20:15 UTC)
31. https://arxiv.org/abs/2606.26511 : MemStrata (Yadav; 20260625) (read 20261102 20:15 UTC)
32. https://arxiv.org/abs/2604.11544 : RoMem, Time is Not a Label (Li, Zhang, Yang and 2 more; 20260413; EMNLP 2026) (read 20261102 20:15 UTC)
33. https://arxiv.org/abs/2503.03704 : MINJA (Dong, Xu, He and 5 more; 20250305) (read 20261102 20:15 UTC)
34. https://arxiv.org/abs/2610.14431 : MemForm (Pan, Shao, Ma and 4 more; 20261010) (read 20261102 20:13 UTC)
35. https://arxiv.org/abs/2610.22959 : SAFE-Mem (Li, Kang, Hu and 8 more; 20261016) (read 20261102 20:13 UTC)
36. https://arxiv.org/abs/2606.18829 : GateMem (Ren, Yang, Chen and 7 more; 20260617) (read 20261102 20:15 UTC)
37. https://arxiv.org/abs/2402.17753 : LoCoMo (Maharana, Lee, Tulyakov and 3 more; 20240227) (read 20261102 20:13 UTC)
38. https://arxiv.org/abs/2410.10813 : LongMemEval (Wu, Wang, Yu and 3 more; 20241014; ICLR 2025) (read 20261102 20:13 UTC)
39. https://github.com/HKUDS/LightRAG : README feature "Incremental Updates & Selective Deletion" (read 20261102 21:01 UTC)
40. https://api.github.com/repos/OWNER/NAME/commits?path=LICENSE and the file text at each commit (authenticated CLI; OWNER/NAME is each of the nine repositories of the table, named in sources 5 to 13): claude-mem, binary licence 20250906, compiled-form licence 20250909, AGPL-3.0 20250911 and 20251003, Apache-2.0 20260508 (commit 36b0929f); OpenViking, Apache-2.0 20260129, AGPL-3.0 20260330 (commit ce998873); MIRIX, MIT 20250416, Apache-2.0 20250711 (commit a5944e0c); the other six: no change of licence type in 2025 and 2026 (read 20261102 22:56 to 22:59 UTC)
