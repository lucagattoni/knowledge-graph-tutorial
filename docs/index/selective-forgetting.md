---
type: index
kind: concept
aliases: [conflict resolution, SF]
updated: 20261102 22:53 UTC
---

# Selective forgetting

This entry answers what "selective forgetting" means for an agent's memory, where the name comes from, and why one word covers different mechanisms. The benchmark that makes it a named competency first called it something else, and its dataset card still does.

## Definition

Hu, Wang and McAuley introduce selective forgetting (SF) as one of four competencies of a memory agent: "the skill to revise, overwrite, or remove previously stored information when faced with contradictory evidence" [1]. Their appendix defines it as the agent's ability "to detect and resolve contradictions between out of date knowledge and newly acquired information" [1]. Accurate retrieval keeps all related content; SF "requires overwriting prior facts" so that answers follow the newest information [1]. The authors ground the name in interference in cognitive psychology and relate it to model editing [1].

## How it changed

- **20230524.** MQuAKE (EMNLP 2023) tests whether a model's answers change when a fact is edited; MemoryAgentBench's FactConsolidation sets reuse its edit pairs [1][2].
- **20241014.** LongMemEval lists "knowledge updates" among five abilities: recognising changes in a user's personal information [3]. See [LongMemEval](../benchmarks/longmemeval.md).
- **2025.** Zep (20250120) invalidates an edge that a new edge contradicts [4]. Mem0 (20250428) lets the model pick ADD, UPDATE, DELETE or NOOP, DELETE for memories that new information contradicts [5]. Both first-party. See [Graphiti](../projects/graphiti.md), [Mem0](../projects/mem0.md).
- **20250707 to 20260628.** MemoryAgentBench v1 (20250707) names its fourth core competency "conflict resolution"; the abstract of v2 (20250926) says "selective forgetting", and v4 (20260628) keeps it [1]. See [MemoryAgentBench](../benchmarks/memoryagentbench.md).
- **20251215.** The survey "Memory in the Age of AI Agents" treats updating and forgetting as separate steps of memory evolution [6].
- **20261029.** Cognee 1.6.6 ships a durable API for resolving conflicting facts and makes conflict review the default (first-party). Whether it does what SF tests is unstated [9]. See [Cognee](../projects/cognee.md).

Still moving: [Agent memory](../trends/agent-memory.md).

## Where sources disagree

**Name.** The MemoryAgentBench paper said conflict resolution in v1 and says selective forgetting from v2 on [1]; its dataset card and README still say conflict resolution for the same overwritten-facts task [7][8].

**Meaning.** The survey defines forgetting as "deliberate removal of outdated, redundant, or low-value information to free capacity" and says updates, unlike forgetting, "resolve conflicts between memories" [6]. *Reading:* MemoryAgentBench's SF matches the survey's updating, not its forgetting.

**How hard.** The card says multi-hop accuracy is at most 7% [7]; the paper's v4 text says at most 28% [1]. The card does not say which paper version its figure comes from.

## Related

[Agent memory](./agent-memory.md) · [temporal knowledge graph](./temporal-knowledge-graph.md) · [bi-temporal model](./bi-temporal-model.md) · [test-time learning](./test-time-learning.md). Benchmark: [MemoryAgentBench](../benchmarks/memoryagentbench.md). Project: [Cognee](../projects/cognee.md). Papers: [agent memory](../papers/agent-memory.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Projects**

- [Supermemory](../projects/supermemory.md)

**Benchmarks**

- [MemoryAgentBench](../benchmarks/memoryagentbench.md)

**Index**

- [Test-time learning](test-time-learning.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/html/2507.05257 : Hu, Wang and McAuley, "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions", v4 text: section 1 (competencies), section 4.2, Appendix B.4.1 (definition), B.4.2 (MQuAKE pairs), B.5 (cognitive science); https://arxiv.org/abs/2507.05257 for versions v1 7 July 2025 to v4 28 June 2026 (read 20261102 22:09 UTC); https://arxiv.org/html/2507.05257v1 for v1 ("conflict resolution") and https://arxiv.org/abs/2507.05257v2 for the v2 abstract ("selective forgetting"; v2 dated 26 September 2025) (read 20261102 22:50 UTC)
2. https://arxiv.org/abs/2305.14795 : Zhong et al., "MQuAKE", v1 24 May 2023, EMNLP 2023: abstract (read 20261102 22:09 UTC)
3. https://arxiv.org/abs/2410.10813 : Wu et al., "LongMemEval", v1 14 October 2024: abstract; https://arxiv.org/html/2410.10813 for the definition of knowledge updates (read 20261102 22:09 and 22:13 UTC)
4. https://arxiv.org/html/2501.13956 : Rasmussen et al., "Zep", v1 20 January 2025: section 2.2.3 "Temporal Extraction and Edge Invalidation" (first-party; read 20261102 22:13 UTC)
5. https://arxiv.org/html/2504.19413 : Chhikara et al., "Mem0", v1 28 April 2025: memory update operations (first-party; read 20261102 22:13 UTC)
6. https://arxiv.org/html/2512.13564 : Hu et al., "Memory in the Age of AI Agents", v1 15 December 2025, v2 13 January 2026: sections 5.2.2 Updating and 5.2.3 Forgetting; https://arxiv.org/abs/2512.13564 for versions and author count (read 20261102 22:09 UTC)
7. https://huggingface.co/datasets/ai-hyz/MemoryAgentBench : dataset card: "Conflict Resolution" competency and split, key findings (first-party; read 20261102 22:09 UTC)
8. https://raw.githubusercontent.com/HUST-AI-HYZ/MemoryAgentBench/main/README.md : repository README: "Conflict Resolution (CR)" (first-party; read 20261102 22:12 UTC)
9. https://github.com/topoteretes/cognee/releases/tag/v1.6.6 : release v1.6.6, published 20261029 21:33 UTC, notes "Conflict resolution & stability", read through gh api (first-party; read 20261102 22:13 UTC)
