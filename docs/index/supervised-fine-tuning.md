---
type: index
kind: concept
aliases: [SFT, supervised finetuning]
updated: 20261102 22:16 UTC
---

# Supervised fine-tuning

This entry says what supervised fine-tuning (SFT) is, how it became the first step of training a language-model assistant, and what is disputed about what it adds before or beside reinforcement learning.

## Definition

Ouyang and 19 co-authors use the term for the first of three steps in training InstructGPT: "We fine-tune GPT-3 on our labeler demonstrations using supervised learning" [1]. The model is trained to reproduce example answers written for example prompts; a reward model and reinforcement learning then start from it [1]. The wider idea is older: pre-train on unlabelled text, then fine-tune on labelled data. BERT's authors say the pre-trained model "can be fine-tuned with just one additional output layer" [2]. See [fine-tuning](./fine-tuning.md).

## How it changed

- **20180118 and 20181011.** ULMFiT fine-tunes a pre-trained language model for text classification; with 100 labelled examples it matches training from scratch on 100 times more data (first-party) [3]. BERT then sets new results on eleven tasks by fine-tuning (first-party) [2]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20210903.** FLAN fine-tunes a 137B model on over 60 tasks written as instructions and improves zero-shot results on unseen tasks; the authors call this instruction tuning (first-party) [4].
- **20220304.** InstructGPT adds the supervised step before a reward model and reinforcement learning; its 1.3B model is preferred to the 175B GPT-3 (first-party) [1].
- **20230518.** LIMA fine-tunes a 65B model on 1,000 curated examples with no reinforcement learning, and its authors conclude that "almost all knowledge in large language models is learned during pretraining" (first-party) [5].
- **20250122.** DeepSeek-R1's v1 abstract trains R1-Zero by reinforcement learning "without supervised fine-tuning (SFT) as a preliminary step"; R1 itself adds cold-start data before reinforcement learning (first-party) [6].
- **2026.** GraphWalker (v1 20260330) and Search-on-Graph-R1 (20260720) run SFT on synthetic or teacher trajectories, then a reinforcement-learning stage, for question answering over a knowledge graph (first-party) [7][8]. Still moving: [Agentic graph retrieval](../trends/learned-graph-traversal.md).

## Where sources disagree

**What SFT adds next to reinforcement learning.** Chu and eight co-authors (20250128) find that SFT "tends to memorize" while reinforcement learning generalizes, yet SFT stays essential because it stabilizes the output format [9]. The v2 abstract of DeepSeek-R1 (20260104) says reasoning can be incentivized by pure reinforcement learning, "obviating the need for human-labeled reasoning trajectories" [6]. GraphWalker says staged SFT raises the ceiling for the later reinforcement-learning stage; Search-on-Graph-R1 finds the two stages give complementary gains [7][8]. All four are first-party, on different tasks; no source read settles it.

## Related

[Fine-tuning](./fine-tuning.md) · [reinforcement learning](./reinforcement-learning.md) · [GRPO](./grpo.md) · [large language model](./large-language-model.md) · [BERT](./bert.md) · papers: [learned graph traversal](../papers/learned-graph-traversal.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)

**Index**

- [Fine-tuning](fine-tuning.md)
- [GRPO](grpo.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2203.02155 : Ouyang et al., "Training language models to follow instructions with human feedback", v1 20220304: abstract; full text at https://arxiv.org/pdf/2203.02155, Figure 2 and section 3 (SFT defined, 1.3B against 175B) (first-party; read 20261102 22:06 UTC)
2. https://arxiv.org/abs/1810.04805 : Devlin et al., BERT, v1 20181011, abstract (first-party; read 20261102 22:06 UTC)
3. https://arxiv.org/abs/1801.06146 : Howard and Ruder, ULMFiT, v1 20180118, abstract (first-party; read 20261102 22:06 UTC)
4. https://arxiv.org/abs/2109.01652 : Wei et al., "Finetuned Language Models Are Zero-Shot Learners", v1 20210903, abstract (first-party; read 20261102 22:06 UTC)
5. https://arxiv.org/abs/2305.11206 : Zhou et al., "LIMA: Less Is More for Alignment", v1 20230518, abstract (first-party; read 20261102 22:10 UTC)
6. https://arxiv.org/abs/2501.12948v1 and https://arxiv.org/abs/2501.12948 : DeepSeek-AI, DeepSeek-R1: v1 20250122 abstract (R1-Zero without SFT, cold-start data) and v2 20260104 abstract (read 20261102 22:10 UTC and 22:06 UTC)
7. https://arxiv.org/abs/2603.28533 : GraphWalker, v1 20260330, abstract: two-stage SFT then lightweight reinforcement learning (first-party; read 20261102 22:10 UTC)
8. https://arxiv.org/abs/2607.18481 : Search-on-Graph-R1, v1 20260720, abstract: SFT then reinforcement learning, complementary gains (first-party; read 20261102 22:10 UTC)
9. https://arxiv.org/abs/2501.17161 : Chu et al., "SFT Memorizes, RL Generalizes", v1 20250128, abstract (first-party; read 20261102 22:06 UTC)
