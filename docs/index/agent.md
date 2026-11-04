---
type: index
kind: concept
aliases: [AI agent, LLM agent, LLM-based agent, language agent]
updated: 20261102 20:50 UTC
---

# Agent

An agent, in this documentation, is a program built around a language model that decides its own next steps and calls tools to reach a goal. The word has no single definition in the sources read, and the sources below show where they differ.

## Definition

Xi et al. define AI agents as "artificial entities that sense their environment, make decisions, and take actions" [1]. For language-model systems, Anthropic separates *workflows*, "systems where LLMs and tools are orchestrated through predefined code paths", from *agents*, "systems where LLMs dynamically direct their own processes and tool usage" [2]. OpenAI's guide says: "Agents are systems that independently accomplish tasks on your behalf", and that simple chatbots and single-turn model calls are not agents [3].

## How it changed

- **20221006.** The ReAct preprint has a model interleave reasoning steps with actions that query external sources [4]. It falls in the era [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20230209.** Toolformer shows that a model can learn when and how to call tools such as calculators and search engines [5]. See [tool use](./tool-use.md).
- **20230905.** Sumers et al. describe a language agent with "modular memory components" [6]. See [agent memory](./agent-memory.md).
- **20230914.** Xi et al. publish a survey of agents based on a [large language model](./large-language-model.md), 29 authors [1].
- **20241219.** Anthropic's post draws the workflow/agent line quoted above [2].
- **20251215.** Hu et al. write that in 2023-2024 the community "had no stable or coherent definition" of an LLM agent, and that a unified one has only "begun to emerge" [7].
- **Still moving.** Agents that search raw data, walk graphs by a learned policy or keep memory are on the trend pages [agentic search](../trends/agentic-search.md), [learned graph traversal](../trends/learned-graph-traversal.md) and [agent memory](../trends/agent-memory.md).

## Where sources disagree

They disagree on the test. Anthropic and OpenAI test who controls the steps: the model, not fixed code [2][3]. Xi et al. test sensing and acting in an environment [1]. Hu et al. report that for some authors a model calling a calculator already made an agent, while others required planning, tool use, memory and reflection [7].

## Related

[Tool use](./tool-use.md), [agent memory](./agent-memory.md), [Model Context Protocol](./model-context-protocol.md), [reinforcement learning](./reinforcement-learning.md), [retrieval-augmented generation](./retrieval-augmented-generation.md). Trends: [code knowledge graphs](../trends/code-knowledge-graphs.md), [infrastructure and MCP](../trends/infrastructure-and-mcp.md). Papers: [agentic search group](../papers/agentic-search.md), [agent memory group](../papers/agent-memory.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)
- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)
- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)
- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Projects**

- [Code-Graph-RAG](../projects/code-graph-rag.md)
- [code-review-graph](../projects/code-review-graph.md)
- [CodeGraph](../projects/codegraph.md)
- [Dify](../projects/dify.md)
- [Graphify](../projects/graphify.md)
- [GraphRAG SDK](../projects/graphrag-sdk.md)
- [Letta](../projects/letta.md)
- [LlamaIndex](../projects/llama-index.md)
- [MIRIX](../projects/mirix.md)
- [PageIndex](../projects/pageindex.md)
- [Projects](../projects/README.md)
- [TencentDB Agent Memory](../projects/tencentdb-agent-memory.md)
- [Understand Anything](../projects/understand-anything.md)

**Papers**

- [Papers: Agentic graph retrieval](../papers/learned-graph-traversal.md)
- [Papers: Agentic search over raw data](../papers/agentic-search.md)
- [Papers: Code graphs for coding agents](../papers/code-knowledge-graphs.md)

**Benchmarks**

- [EnterpriseRAG-Bench](../benchmarks/enterpriserag-bench.md)

**Experiments**

- [Experiments evidence: status log](../experiments/evidence/status.md)
- [Instruments](../experiments/instruments.md)
- [X4: a code graph against grep](../experiments/x4-code-graph-vs-grep.md)
- [X5: Wiki size limit](../experiments/x5-wiki-size-limit.md)

**Index**

- [Agent harness](agent-harness.md)
- [Agent memory](agent-memory.md)
- [Chain-of-thought](chain-of-thought.md)
- [Code graph](code-graph.md)
- [Cognitive architecture](cognitive-architecture.md)
- [grep](grep.md)
- [GRPO](grpo.md)
- [Large language model](large-language-model.md)
- [Memory poisoning](memory-poisoning.md)
- [Model Context Protocol](model-context-protocol.md)
- [Multi-hop question answering](multi-hop-question-answering.md)
- [Reinforcement learning](reinforcement-learning.md)
- [Retrieval-augmented generation](retrieval-augmented-generation.md)
- [SHACL](shacl.md)
- [Test-time learning](test-time-learning.md)
- [Tool use](tool-use.md)
- [Vectorless retrieval](vectorless-retrieval.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2309.07864 : Xi et al., "The Rise and Potential of Large Language Model Based Agents: A Survey", 29 authors, v1 20230914, definition of AI agents (read 20261102 20:44 UTC)
2. https://www.anthropic.com/engineering/building-effective-agents : "Building effective agents", 20241219, definitions of workflows and agents (read 20261102 20:44 UTC)
3. https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf : "A practical guide to building agents", page 4, definition of an agent; the text read shows no date, so its date is unstated (read 20261102 20:47 UTC)
4. https://arxiv.org/abs/2210.03629 : Yao et al., "ReAct", 7 authors, v1 20221006 (read 20261102 20:44 UTC)
5. https://arxiv.org/abs/2302.04761 : Schick et al., "Toolformer", 8 authors, v1 20230209 (read 20261102 20:44 UTC)
6. https://arxiv.org/abs/2309.02427 : Sumers et al., "Cognitive Architectures for Language Agents", 4 authors, v1 20230905 (read 20261102 20:44 UTC)
7. https://arxiv.org/abs/2512.13564 : Hu et al., "Memory in the Age of AI Agents", 47 authors, v1 20251215, v2 20260113; the passage on the definition of an LLM agent is in section 2.3.1 of the PDF (read 20261102 20:47 UTC)
