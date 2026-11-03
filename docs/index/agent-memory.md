---
type: index
kind: concept
aliases: [agentic memory, LLM agent memory, memory for LLM agents]
updated: 20261102 21:16 UTC
---

# Agent memory

Agent memory is what a language-model agent keeps from its own past interactions and uses in later steps, within a task or across tasks. This entry gives the definition and the dated steps.

## Definition

Hu et al. treat agent memory as an evolving memory state of an [agent](./agent.md). Its structure is not fixed: it may be "a text buffer, key-value store, vector database, graph structure, or any hybrid representation". Three operators act on it: formation (turning tool outputs, reasoning traces and feedback into memory candidates), evolution (consolidating, resolving conflicts, discarding) and retrieval of a context-dependent signal at each step [1]. Their taxonomy has three forms (token-level, parametric, latent), three functions (factual, experiential, working) and the dynamics of formation, evolution and retrieval [1].

## How it changed

- **20230407.** Generative Agents keeps a full natural-language log of an agent's experiences [2].
- **20230905.** CoALA describes language agents with "modular memory components" [3].
- **20231012.** MemGPT proposes "virtual context management", moving information between memory tiers borrowed from operating systems, to extend a model's effective [context window](./context-window.md) [4].
- **20240421.** Zhang et al. survey the memory mechanism of LLM-based agents and call memory "the key component to support agent-environment interactions" [5].
- **20250428.** The Mem0 paper, by the authors of [Mem0](../projects/mem0.md) (first-party), proposes extracting, consolidating and retrieving key information from conversations [6].
- **20251215.** Hu et al. call the field "increasingly fragmented" and say long/short-term taxonomies "have proven insufficient" (v2 20260113) [1].
- **Still moving.** See the trend [Agent memory](../trends/agent-memory.md).

## Where sources disagree

- **Boundary with retrieval.** Hu et al. say the line between [retrieval-augmented generation](./retrieval-augmented-generation.md) and agent memory has become "increasingly blurred", and that HippoRAG has been read by both communities as work on long-term memory [1].
- **Taxonomy.** Hu et al. call the long/short-term split the traditional taxonomy and argue it is insufficient; they treat the two as temporal patterns of one memory state, not separate modules [1]. Whether Zhang et al. use that split is **unstated** in the abstract read [5].
- **Naming.** Hu et al. say early systems such as MemGPT "framed their contributions as providing LLM memory" and reclassify them as "instances of agent memory" [1]. MemGPT's own abstract frames its work as virtual context management across memory tiers and does not use the phrase "LLM memory" [4].

## Related

[Agent](./agent.md), [context window](./context-window.md), [retrieval-augmented generation](./retrieval-augmented-generation.md), [temporal knowledge graph](./temporal-knowledge-graph.md), [GraphRAG](./graphrag.md). Projects: [Mem0](../projects/mem0.md), [Letta](../projects/letta.md), [Graphiti](../projects/graphiti.md), [Hindsight](../projects/hindsight.md), [Cognee](../projects/cognee.md), [MIRIX](../projects/mirix.md), [claude-mem](../projects/claude-mem.md). Benchmarks: [LoCoMo](../benchmarks/locomo.md), [LongMemEval](../benchmarks/longmemeval.md), [MemoryAgentBench](../benchmarks/memoryagentbench.md). Papers: [agent memory group](../papers/agent-memory.md). Trends: [Agent memory](../trends/agent-memory.md), [Plain files as agent knowledge](../trends/plain-file-knowledge.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [The Web changes data and search](../history/the-web.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [agent-memory (Tigerless Labs)](../projects/tigerless-agent-memory.md)
- [Hindsight](../projects/hindsight.md)
- [HippoRAG](../projects/hipporag.md)
- [MCP reference servers](../projects/mcp-servers.md)
- [Memgraph](../projects/memgraph.md)
- [Memori](../projects/memori.md)
- [MemOS](../projects/memos.md)
- [memU](../projects/memu.md)
- [OpenViking](../projects/openviking.md)

**Papers**

- [Papers: Agent memory](../papers/agent-memory.md)
- [Papers: Building knowledge graphs with LLMs](../papers/llm-kg-construction.md)
- [Papers: Plain files as agent knowledge](../papers/plain-file-knowledge.md)

**Benchmarks**

- [Benchmarks](../benchmarks/README.md)
- [LoCoMo](../benchmarks/locomo.md)
- [LongMemEval](../benchmarks/longmemeval.md)
- [MemoryAgentBench](../benchmarks/memoryagentbench.md)

**Index**

- [Agent](agent.md)
- [Agent harness](agent-harness.md)
- [Bi-temporal model](bi-temporal-model.md)
- [Cognitive architecture](cognitive-architecture.md)
- [Context window](context-window.md)
- [Embedding](embedding.md)
- [LLM wiki](llm-wiki.md)
- [Memory poisoning](memory-poisoning.md)
- [Model Context Protocol](model-context-protocol.md)
- [Open-core](open-core.md)
- [Provenance](provenance.md)
- [Reinforcement learning](reinforcement-learning.md)
- [Retrieval-augmented generation](retrieval-augmented-generation.md)
- [Selective forgetting](selective-forgetting.md)
- [Temporal knowledge graph](temporal-knowledge-graph.md)
- [Test-time learning](test-time-learning.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2512.13564 : Hu et al., "Memory in the Age of AI Agents", 47 authors, v1 20251215, v2 20260113; abstract and PDF sections 2.2 and 2.3 for the definition, operators, taxonomy, fragmentation and the RAG boundary; section 2.3.1 on naming (read 20261102 20:47 UTC; section 2.3.1 re-read 20261102 21:16 UTC)
2. https://arxiv.org/abs/2304.03442 : Park et al., "Generative Agents", 6 authors, v1 20230407 (read 20261102 20:44 UTC)
3. https://arxiv.org/abs/2309.02427 : Sumers et al., "Cognitive Architectures for Language Agents", 4 authors, v1 20230905 (read 20261102 20:44 UTC)
4. https://arxiv.org/abs/2310.08560 : Packer et al., "MemGPT: Towards LLMs as Operating Systems", 7 authors, v1 20231012 (read 20261102 20:44 UTC; abstract re-read 20261102 21:16 UTC)
5. https://arxiv.org/abs/2404.13501 : Zhang et al., "A Survey on the Memory Mechanism of Large Language Model based Agents", 9 authors, v1 20240421; abstract only (read 20261102 20:44 UTC)
6. https://arxiv.org/abs/2504.19413 : Chhikara et al., "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory", 5 authors, v1 20250428 (read 20261102 20:44 UTC)
