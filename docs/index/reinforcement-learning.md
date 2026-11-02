---
type: index
kind: concept
aliases: [RL]
updated: 20261102 21:30 UTC
---

# Reinforcement learning

This entry answers what reinforcement learning is, how it came to train language-model agents, and what is disputed about what it adds. It dates the main steps from 1996 to 2025 and cites the abstract or text read for each.

## Definition

Kaelbling, Littman and Moore define it in their 1996 survey: "the problem faced by an agent that learns behavior through trial-and-error interactions with a dynamic environment" [1]. The survey names "learning from delayed reinforcement" and the trade-off between exploration and exploitation among its central issues, and grounds the field in Markov decision theory [1]. The survey's first section adds that no input and output pairs are presented: after an action the agent is told the immediate reward, not which action would have been best in the long term [1].

## How it changed

- **19960501.** The Kaelbling survey appears, covering "the historical basis of the field" [1]. Era: [The Web changes data and search](../history/the-web.md).
- **20131219.** Mnih and six co-authors train a network with a Q-learning variant on raw pixels; it beats earlier approaches on six of seven Atari games and a human expert on three (first-party) [2]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20170612.** Christiano and five co-authors learn goals from human preferences between pairs of behaviour segments [3].
- **20220304.** Ouyang and 19 co-authors fine-tune GPT-3 with "reinforcement learning from human feedback"; their 1.3B-parameter model is preferred to the 175B GPT-3 (first-party) [4]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20240205.** DeepSeekMath presents Group Relative Policy Optimization, "a variant of Proximal Policy Optimization" [5].
- **20250122 and 20260104.** DeepSeek-R1 appears as v1 (Nature 645, 2025). Its v1 abstract introduces R1-Zero, trained by large-scale reinforcement learning without supervised fine-tuning; the v2 abstract (20260104) says reasoning can be "incentivized through pure reinforcement learning (RL)" (first-party) [6].
- **20250312.** Search-R1 trains a model to "autonomously generate (multiple) search queries during step-by-step reasoning", rewarding only the final answer (first-party) [7]. Graph versions are told in [Agentic graph retrieval](../trends/learned-graph-traversal.md), a trend still moving, with its [papers](../papers/learned-graph-traversal.md).

## Where sources disagree

**Does it teach new skills?** DeepSeek-R1's authors (v2 abstract) say reasoning abilities can be incentivized by reinforcement learning, with self-reflection and verification emerging [6]. Yue and seven co-authors (20250418) find trained models better at small k but base models better in pass@k at large k, and conclude the training "does not elicit fundamentally new reasoning patterns" [8]. DeepSeek-R1's tasks are verifiable ones such as mathematics, coding competitions and STEM [6]; whether Yue's result holds for search agents is **unstated** in the abstracts read.

## Related

[agent](./agent.md) · [large language model](./large-language-model.md) · [agent memory](./agent-memory.md) · [retrieval-augmented generation](./retrieval-augmented-generation.md) · trend: [Agentic graph retrieval](../trends/learned-graph-traversal.md) · papers: [learned graph traversal](../papers/learned-graph-traversal.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)
- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)
- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Trends: what the field is doing now](../trends/README.md)

**Papers**

- [Papers: Agentic graph retrieval](../papers/learned-graph-traversal.md)

**Benchmarks**

- [RAGSearch](../benchmarks/ragsearch.md)

**Applied to Pinakes**

- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Agent](agent.md)
- [Chain-of-thought](chain-of-thought.md)
- [Fine-tuning](fine-tuning.md)
- [GRPO](grpo.md)
- [Supervised fine-tuning](supervised-fine-tuning.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/cs/9605103 : Kaelbling, Littman, Moore, "Reinforcement Learning: A Survey", JAIR 4 (1996); arXiv v1 19960501: abstract and Section 1 (definition, central issues, the difference from supervised learning) (abstract read 20261102 20:58 UTC; full text via https://arxiv.org/pdf/cs/9605103 read 20261102 21:26 UTC)
2. https://arxiv.org/abs/1312.5602 : Mnih et al., "Playing Atari with Deep Reinforcement Learning", v1 20131219: abstract, seven games, six outperformed, three above a human expert (read 20261102 21:00 UTC)
3. https://arxiv.org/abs/1706.03741 : Christiano et al., "Deep reinforcement learning from human preferences", v1 20170612: abstract (read 20261102 21:00 UTC)
4. https://arxiv.org/abs/2203.02155 : Ouyang et al., "Training language models to follow instructions with human feedback", v1 20220304: abstract, RLHF, 1.3B against 175B (read 20261102 20:59 UTC)
5. https://arxiv.org/abs/2402.03300 : Shao et al., "DeepSeekMath", v1 20240205: abstract, GRPO as a variant of PPO (read 20261102 20:59 UTC)
6. https://arxiv.org/abs/2501.12948 : DeepSeek-AI, "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning", v1 20250122, v2 20260104; journal reference Nature 645, 633-638 (2025): v1 and v2 abstracts, which differ in wording (v1 and v2 read 20261102 21:26 UTC)
7. https://arxiv.org/abs/2503.09516 : Jin et al., "Search-R1", v1 20250312: abstract (read 20261102 20:59 UTC)
8. https://arxiv.org/abs/2504.13837 : Yue et al., "Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?", v1 20250418: abstract (read 20261102 21:00 UTC)
