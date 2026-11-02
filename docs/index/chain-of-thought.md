---
type: index
kind: concept
aliases: [CoT, chain of thought, chain-of-thought prompting]
updated: 20261102 22:50 UTC
---

# Chain-of-thought

This entry says what chain-of-thought is, how it moved from a prompting trick to a trained behaviour, and where sources dispute how far the written steps can be trusted.

## Definition

Wei et al. define a chain of thought as "a coherent series of intermediate reasoning steps that lead to the final answer for a problem", and obtain it from a [large language model](./large-language-model.md) by placing a few worked examples with such steps in the prompt [1]. Kojima et al. show that adding "Let's think step by step" before the answer, with no examples, also works [2].

## How it changed

- **20220128.** Wei et al. report gains on arithmetic, commonsense and symbolic tasks, and a new best on GSM8K from a 540B-parameter model with eight examples (first-party). The gain appears only at about 100B parameters: "an emergent ability of model scale" [1]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20220524.** Kojima et al. raise MultiArith accuracy from 17.7% to 78.7% and GSM8K from 10.4% to 40.7% with one fixed prompt (first-party; NeurIPS 2022) [2].
- **20240918.** Sprague et al. review over 100 papers and run 20 datasets on 14 models: the benefit is mostly on math and logic (ICLR 2025) [3].
- **20250122.** DeepSeek-AI posts DeepSeek-R1. The first version of the abstract says DeepSeek-R1-Zero, trained by large-scale reinforcement learning "without supervised fine-tuning (SFT) as a preliminary step", "demonstrates remarkable reasoning capabilities" (first-party) [4].
- **20250917.** Nature publishes the paper. Its abstract says reasoning abilities "can be incentivized through pure reinforcement learning", with no need for human-labelled reasoning trajectories (first-party) [5]. The arXiv abstract has carried the same wording since its revision of 20260104 [4]. See [reinforcement learning](./reinforcement-learning.md).
- **20261020.** Yan and Hewitt report that reward misspecification alone lowers how well a chain of thought can be monitored [6].

## Where sources disagree

**Where it helps.** Wei et al. report gains across three task families [1]. Sprague et al. find strong benefits "primarily on tasks involving math or logic" and much smaller ones elsewhere [3].

**Whether the steps explain the answer.** Turpin et al. (20230507) find that explanations "can systematically misrepresent the true reason for a model's prediction" [7]. Lanham et al. (20230717) conclude CoT "can be faithful" if model size and task are chosen with care, and find larger models less faithful on most tasks [8]. Chen et al. (20250508) report that the rate at which reasoning models mention a hint they used is often below 20% [9]. Korbak et al. (41 authors, 20250715) call monitoring chains of thought imperfect but promising, and the opportunity one that "may be fragile" [10].

## Related

[Large language model](./large-language-model.md) · [agent](./agent.md) · [reinforcement learning](./reinforcement-learning.md) · [multi-hop question answering](./multi-hop-question-answering.md) · [tool use](./tool-use.md). Papers that interleave such steps with search: [agentic search](../papers/agentic-search.md); trend: [agentic search](../trends/agentic-search.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Papers**

- [Papers: Agentic search over raw data](../papers/agentic-search.md)

**Index**

- [LLM-as-judge](llm-as-judge.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2201.11903 : Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", 9 authors, v1 20220128, abstract (read 20261102 22:06 UTC); the definition and the result at about 100B parameters (introduction, section 3, Figure 4) are from the full text at https://ar5iv.labs.arxiv.org/html/2201.11903 (read 20261102 22:08 UTC)
2. https://arxiv.org/abs/2205.11916 : Kojima et al., "Large Language Models are Zero-Shot Reasoners", 5 authors, v1 20220524, NeurIPS 2022 per the page; abstract (read 20261102 22:06 UTC)
3. https://arxiv.org/abs/2409.12183 : Sprague et al., "To CoT or not to CoT?", 10 authors, v1 20240918, ICLR 2025 per the page; abstract (read 20261102 22:08 UTC)
4. https://arxiv.org/abs/2501.12948 : DeepSeek-AI, "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning", v1 20250122, v2 20260104; abstract of v1 at https://arxiv.org/abs/2501.12948v1 and of v2 at https://arxiv.org/abs/2501.12948 (read 20261102 22:43 UTC)
5. https://www.nature.com/articles/s41586-025-09422-z : Nature article page for DeepSeek-R1, "DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning", "Published: 17 September 2025"; abstract wording (read 20261102 22:43 UTC)
6. https://arxiv.org/abs/2610.28303 : Yan and Hewitt, "Reward Misspecification Degrades Chain-of-Thought Monitorability", v1 20261020; abstract (read 20261102 22:16 UTC)
7. https://arxiv.org/abs/2305.04388 : Turpin et al., "Language Models Don't Always Say What They Think", 4 authors, v1 20230507, NeurIPS 2023 per the page; abstract (read 20261102 22:06 UTC)
8. https://arxiv.org/abs/2307.13702 : Lanham et al., "Measuring Faithfulness in Chain-of-Thought Reasoning", 30 authors, v1 20230717; abstract (read 20261102 22:06 UTC)
9. https://arxiv.org/abs/2505.05410 : Chen et al., "Reasoning Models Don't Always Say What They Think", 15 authors, v1 20250508; abstract (read 20261102 22:06 UTC)
10. https://arxiv.org/abs/2507.11473 : Korbak et al., "Chain of Thought Monitorability: A New and Fragile Opportunity for AI Safety", 41 authors, v1 20250715, v2 20251207; abstract (read 20261102 22:08 UTC)
