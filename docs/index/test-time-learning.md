---
type: index
kind: concept
aliases: [TTL, test time learning]
updated: 20261102 22:49 UTC
---

# Test-time learning

This entry says what "test-time learning" means for language-model agents, when the phrase appeared, and why one name covers two different mechanisms: learning from the input alone, and updating the model's weights while it runs.

## Definition

MemoryAgentBench's authors define it as "the capacity to incorporate new behaviors or acquire new skills during deployment, without additional training" [1]. Their appendix says it mirrors in-context learning, with the dialogue history in place of the prompt, and describes it as an agent's ability "to learn to perform new tasks directly from the conversation" [1]. They separate it from retrieval: the agent must induce rules from a long run of labelled sentences and label new ones, not fetch stored facts [1]. Wang and three co-authors (20250617) use a looser definition: the capacity to improve performance on experience-based, reasoning-intensive tasks during test time [2].

## How it changed

- **20190929.** Sun and five co-authors propose "test-time training": update the model's parameters on each unlabeled test sample before predicting (first-party) [3].
- **20200528.** GPT-3 is applied "without any gradient updates or fine-tuning", with demonstrations given as text (first-party) [4]. This is the in-context learning that [1] compares test-time learning to. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20210320.** Banerjee and two co-authors call their method "test-time learning": it trains a model on synthetic question-answer pairs made from one test passage (first-party) [5].
- **20250410.** Dynamic Cheatsheet calls its persistent memory "test-time learning" and states that it works "without modifying their underlying parameters" (first-party) [6].
- **20250527.** The TLM paper adapts a model to a target domain with unlabeled test data, updating low-rank (LoRA) weights, and also names this test-time learning (first-party) [7].
- **20250617.** Wang et al. find "measurable" test-time learning in LLMs, but improvement that is less stable under cumulative experience and slower than humans' (first-party) [2].
- **20250707.** MemoryAgentBench lists it as one of four memory competencies; its fourth version is dated 20260628 [1]. See [MemoryAgentBench](../benchmarks/memoryagentbench.md). Still moving: [Agent memory](../trends/agent-memory.md).

## Where sources disagree

**Do the weights change?** MemoryAgentBench and Dynamic Cheatsheet say no: the agent learns from what is in its input or its memory [1][6]. Banerjee et al. and the TLM paper train on test data, so the weights do change [5][7]. *Reading:* the first definition above is therefore one use of the phrase, not the only one. Sun et al. use the separate name "test-time training" for the weight-updating kind [3].

## Related

[Agent memory](./agent-memory.md) · [agent](./agent.md) · [large language model](./large-language-model.md) · [fine-tuning](./fine-tuning.md) · [selective forgetting](./selective-forgetting.md) · [MemoryAgentBench](../benchmarks/memoryagentbench.md) · trend: [Agent memory](../trends/agent-memory.md) · papers: [agent memory](../papers/agent-memory.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Benchmarks**

- [MemoryAgentBench](../benchmarks/memoryagentbench.md)

**Index**

- [Selective forgetting](selective-forgetting.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2507.05257 and https://arxiv.org/html/2507.05257 : Hu, Wang, McAuley, "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions" (MemoryAgentBench): abstract (v1 20250707, v4 20260628), section 3, appendix B.2 (definition, TTL sets) and H.1 (terminology) (first-party; read 20261102 22:06 UTC)
2. https://arxiv.org/abs/2506.14448 : Wang, Guo, Ma, Zhang, "How Far Can LLMs Improve from Experience? Measuring Test-Time Learning Ability in LLMs with Human Comparison", v1 20250617, abstract (first-party; read 20261102 22:12 UTC)
3. https://arxiv.org/abs/1909.13231 : Sun et al., "Test-Time Training with Self-Supervision for Generalization under Distribution Shifts", v1 20190929, abstract (first-party; read 20261102 22:06 UTC)
4. https://arxiv.org/abs/2005.14165 : Brown et al., "Language Models are Few-Shot Learners", v1 20200528, abstract (first-party; read 20261102 22:06 UTC)
5. https://arxiv.org/abs/2103.11263 : Banerjee, Gokhale, Baral, "Self-Supervised Test-Time Learning for Reading Comprehension", v1 20210320, abstract (first-party; read 20261102 22:12 UTC)
6. https://arxiv.org/abs/2504.07952 : Suzgun et al., "Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory", v1 20250410, abstract (first-party; read 20261102 22:12 UTC)
7. https://arxiv.org/abs/2505.20633 : Hu et al., "Test-Time Learning for Large Language Models" (TLM), v1 20250527, abstract (first-party; read 20261102 22:12 UTC)
