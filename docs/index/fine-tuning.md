---
type: index
kind: concept
aliases: [finetuning, fine tuning, model fine-tuning]
updated: 20261102 22:55 UTC
---

# Fine-tuning

This entry says what fine-tuning is, how it became the usual way to adapt a pre-trained language model, and where the word is stretched. It dates the main steps from 2018 to 2026.

## Definition

The LoRA paper describes the usual setting as "large-scale pre-training on general domain data and adaptation to particular tasks or domains"; full fine-tuning "retrains all model parameters" [1]. A survey of parameter-efficient methods defines the aim as adapting a pre-trained model to a task or domain with few added parameters [2].

## How it changed

- **20180118.** Howard and Ruder post a method, first called FitLaM, for fine-tuning a pre-trained language model for any NLP task. The revised version of 20180523, named ULMFiT, adds that 100 labelled examples match training from scratch on 100 times more data (first-party) [4]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20181011.** BERT, fine-tuned with "just one additional output layer", reports new state-of-the-art results on eleven tasks (first-party) [3].
- **20210617.** LoRA freezes the pre-trained weights and trains small added matrices, with 10,000 times fewer trainable parameters than fine-tuning GPT-3 175B (first-party) [1].
- **20220304.** InstructGPT fine-tunes GPT-3 by supervised learning, then by reinforcement learning from human feedback; the 1.3B model is preferred to the 175B GPT-3 (first-party) [5].
- **20231210.** Ovadia et al. compare unsupervised fine-tuning with [retrieval-augmented generation](./retrieval-augmented-generation.md) for adding knowledge; RAG "consistently outperforms it" [6].
- **20241213.** The Text2Cypher authors combine public datasets into one for fine-tuning and evaluation (size and versions: [Text2Cypher](../benchmarks/text2cypher.md)); fine-tuned models beat baselines on Google-BLEU and Exact Match (first-party) [7]. Still moving: [graph query generation](../trends/graph-query-generation.md).
- **20250122.** DeepSeek-R1-Zero is trained by reinforcement learning "without supervised fine-tuning (SFT) as a preliminary step" (first-party) [8]. See [GRPO](./grpo.md).
- **20260626.** KG2Cypher reports that LoRA supervised fine-tuning lifts execution-result F1 from 0.806 to 0.950 on one set of queries (first-party; Korean enterprise graphs) [9].

## Where sources disagree

**What counts as fine-tuning.** InstructGPT calls both its stages fine-tuning, the reinforcement-learning one included [5]; DeepSeekMath speaks of PPO as "widely used in the RL fine-tuning stage of LLMs" [10]. DeepSeek-R1's abstract uses "supervised fine-tuning" for the step R1-Zero skips, so there reinforcement learning stands apart [8]. See [supervised fine-tuning](./supervised-fine-tuning.md).

**Does it add knowledge?** Ovadia et al. find that models "struggle to learn new factual information" through unsupervised fine-tuning [6]. The Text2Cypher and KG2Cypher gains come from fine-tuning for Cypher generation [7][9]. *Reading:* those are task gains, not added facts, so the sources do not contradict each other. Whether supervised fine-tuning on facts would match RAG is **unstated** in the abstracts read.

## Related

[Supervised fine-tuning](./supervised-fine-tuning.md), [reinforcement learning](./reinforcement-learning.md), [GRPO](./grpo.md), [large language model](./large-language-model.md), [BERT](./bert.md), [transformer](./transformer.md), [retrieval-augmented generation](./retrieval-augmented-generation.md), [text-to-query](./text-to-query.md). Trend: [graph query generation](../trends/graph-query-generation.md). Benchmark: [Text2Cypher](../benchmarks/text2cypher.md). Papers: [graph query generation](../papers/graph-query-generation.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)

**Index**

- [GRPO](grpo.md)
- [Supervised fine-tuning](supervised-fine-tuning.md)
- [Test-time learning](test-time-learning.md)
- [Text-to-query](text-to-query.md)
- [Tool use](tool-use.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2106.09685 : Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models", v1 20210617: abstract (read 20261102 22:06 UTC)
2. https://arxiv.org/abs/2403.14608 : Han et al., "Parameter-Efficient Fine-Tuning for Large Models: A Comprehensive Survey", v1 20240321: abstract, definition of PEFT (read 20261102 22:06 UTC)
3. https://arxiv.org/abs/1810.04805 : Devlin et al., "BERT", v1 20181011: abstract, one additional output layer, eleven tasks (read 20261102 22:06 UTC)
4. https://arxiv.org/abs/1801.06146 : Howard and Ruder, "Universal Language Model Fine-tuning for Text Classification", v1 20180118 (then titled "Fine-tuned Language Models for Text Classification"; method named FitLaM; "any task in NLP"), v5 20180523 (ULMFiT; "only 100 labeled examples" matches training from scratch on "100x more data"; absent from v1): abstracts of v1 and v5 (read 20261102 22:51 UTC)
5. https://arxiv.org/abs/2203.02155 : Ouyang et al., "Training language models to follow instructions with human feedback", v1 20220304: abstract, two fine-tuning stages, 1.3B against 175B (read 20261102 22:06 UTC)
6. https://arxiv.org/abs/2312.05934 : Ovadia et al., "Fine-Tuning or Retrieval? Comparing Knowledge Injection in LLMs", v1 20231210: abstract (read 20261102 22:06 UTC)
7. https://arxiv.org/abs/2412.10064 : Ozsoy et al., "Text2Cypher: Bridging Natural Language and Graph Databases", v1 20241213: abstract (combined public datasets; fine-tuned models improve Google-BLEU and Exact Match over baselines) (first-party; read 20261102 22:51 UTC)
8. https://arxiv.org/abs/2501.12948v1 : DeepSeek-AI, "DeepSeek-R1", v1 20250122: abstract of v1 (read 20261102 22:07 UTC)
9. https://arxiv.org/abs/2606.27742 : Choi et al., "KG2Cypher", v1 20260626: abstract, LoRA SFT, F1 0.806 to 0.950 (read 20261102 22:07 UTC)
10. https://arxiv.org/pdf/2402.03300 : Shao et al., "DeepSeekMath", v1 20240205: section 4.1.1, PPO "widely used in the RL fine-tuning stage of LLMs" (read 20261102 22:12 UTC)
