---
type: index
kind: concept
aliases: [Group Relative Policy Optimization, Group Relative Policy Optimisation]
updated: 20261102 22:58 UTC
---

# GRPO

This entry says what GRPO is, where it came from, and how it came to train retrieval agents. It dates the main steps from 2024 to 2026 and records two points on which the sources differ.

## Definition

Shao and ten co-authors introduce Group Relative Policy Optimization in DeepSeekMath as "a variant of Proximal Policy Optimization (PPO)" [1]. For each question, a group of outputs is sampled from the old policy and scored; the rewards are normalised by subtracting the group average and dividing by the group standard deviation [2]. The method "foregoes the critic model, instead estimating the baseline from group scores", which cuts training resources [2]. It is a form of [reinforcement learning](./reinforcement-learning.md) used to fine-tune language models [2].

## How it changed

- **20240205.** DeepSeekMath introduces GRPO; applied to an instruction-tuned 7B model it lifts MATH from 46.8% to 51.7% (first-party) [1][2].
- **20250122.** DeepSeek-R1-Zero uses GRPO as its reinforcement-learning framework on DeepSeek-V3-Base; AIME 2024 pass@1 rises from 15.6% to 71.0% (first-party) [3].
- **20250312.** Search-R1 trains a model to write search queries while reasoning, with PPO or GRPO and a final-answer reward (first-party) [4].
- **20250326.** Liu and seven co-authors report an optimization bias in GRPO that "artificially increases response length" and propose Dr. GRPO [5].
- **20250724.** Zheng and eleven co-authors propose GSPO, which moves importance ratios and clipping from tokens to sequences and reports better training efficiency than GRPO (first-party) [6].
- **20250729.** Graph-R1 trains a retrieval agent over a knowledge hypergraph; its README documents GRPO, REINFORCE++ and PPO training [7][8].
- **20260615.** PathRouter uses "differentiated GRPO advantage scaling" so that outcome-only rewards stop reinforcing shortcut answers (first-party) [9]. Still moving: [Agentic graph retrieval](../trends/learned-graph-traversal.md).

## Where sources disagree

**Is it better than PPO?** DeepSeekMath presents the dropped critic as a saving [2]. Search-R1, in its version of 20250805, finds GRPO "converges faster" but "leads to reward collapse after training for many steps, whereas PPO remains stable"; final rewards are comparable. Its first version names one case, reward collapse "when applied to the LLaMA3.2-3B-Instruct model" [4].

**Is the objective sound?** Liu et al. identify an optimization bias in GRPO [5]; Zheng et al. replace its token-level importance ratios with sequence-level ones [6]. Whether reinforcement learning adds reasoning ability at all is disputed on the [reinforcement learning](./reinforcement-learning.md) entry.

## Related

[Reinforcement learning](./reinforcement-learning.md), [fine-tuning](./fine-tuning.md), [supervised fine-tuning](./supervised-fine-tuning.md), [large language model](./large-language-model.md), [agent](./agent.md), [hypergraph](./hypergraph.md). Trends: [agentic graph retrieval](../trends/learned-graph-traversal.md), [asking graphs in natural language](../trends/graph-query-generation.md). Papers: [learned graph traversal](../papers/learned-graph-traversal.md). Benchmark: [RAGSearch](../benchmarks/ragsearch.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)
- [Trends: what the field is doing now](../trends/README.md)

**Papers**

- [Papers: Agentic graph retrieval](../papers/learned-graph-traversal.md)

**Index**

- [Fine-tuning](fine-tuning.md)
- [Supervised fine-tuning](supervised-fine-tuning.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2402.03300 : Shao et al., "DeepSeekMath", v1 20240205: abstract, GRPO as a variant of PPO (read 20261102 22:11 UTC)
2. https://arxiv.org/pdf/2402.03300 : DeepSeekMath full text, introduction and sections 4.1.1 and 4.1.2: critic model dropped, group normalisation, MATH 46.8% to 51.7% (read 20261102 22:12 UTC)
3. https://arxiv.org/pdf/2501.12948v1 : DeepSeek-AI, "DeepSeek-R1", v1 20250122: introduction and section 2.2.1 (GRPO), AIME 2024 15.6% to 71.0% (read 20261102 22:12 UTC)
4. https://arxiv.org/pdf/2503.09516 : Jin et al., "Search-R1", v1 20250312, v5 20250805 (COLM 2025): introduction (PPO and GRPO), section 5.1 (PPO against GRPO; the quoted wording is v5's, while v1 names reward collapse on one model); abstract at https://arxiv.org/abs/2503.09516 (read 20261102 22:51 UTC)
5. https://arxiv.org/abs/2503.20783 : Liu et al., "Understanding R1-Zero-Like Training: A Critical Perspective", v1 20250326: abstract (read 20261102 22:11 UTC)
6. https://arxiv.org/abs/2507.18071 : Zheng et al., "Group Sequence Policy Optimization", v1 20250724: abstract (read 20261102 22:11 UTC)
7. https://arxiv.org/abs/2507.21892 : Luo et al., "Graph-R1", v1 20250729: abstract (read 20261102 22:11 UTC)
8. https://github.com/LHRLAB/Graph-R1 : repository README, heading "Run GRPO/REINFORCE++/PPO training" and the GRPO command (read 20261102 22:12 UTC)
9. https://arxiv.org/abs/2606.16409 : Wang et al., "PathRouter", v1 20260615: abstract (first-party; read 20261102 22:11 UTC)
