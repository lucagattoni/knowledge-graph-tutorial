---
type: index
kind: concept
aliases: [data leakage, benchmark contamination, test set contamination]
updated: 20261102 22:51 UTC
---

# Data contamination

This entry says what data contamination and data leakage mean, in model evaluation and in dataset construction, and how much it matters.

## Definition

Golchin and Surdeanu define data contamination as "the presence of test data from downstream tasks in the training data" of language models [1]. Sainz et al. call the worst case a model trained on the test split of a benchmark and then evaluated on it, which overstates its performance [2]. "Leakage" is the older word from data mining: information about the target "that should not be legitimately available to mine from" [3]. Knowledge-graph papers use it for overlap inside one dataset, such as test triples recoverable from training triples through inverse relations [4].

## How it changed

- **201212.** Kaufman et al. publish a formal treatment of leakage in data mining (*ACM TKDD* 6(4)) [3]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **201507.** Toutanova and Chen find that 94.0% of WN18 and 80.9% of FB15k test triples have their entity pair directly linked in the training graph, and build FB15k-237 without such pairs [12]. See [FB15k-237](../datasets/fb15k-237.md).
- **20170705.** Dettmers et al. call this test-set leakage through inverse relations, show that a simple rule-based model reaches state-of-the-art results on WN18 and FB15k, and build WN18RR [4]. See [WN18RR](../datasets/wn18rr.md).
- **20200528.** The GPT-3 paper devotes a section to benchmark test sets in web-scale training data; a bug left some detected overlap in (first-party) [5]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **2023.** Golchin and Surdeanu (20230816) detect it by asking a model to complete benchmark items [1]; Sainz et al. (20231027) argue it must be measured for each benchmark [2].
- **2024.** LiveCodeBench (20240312) draws on new contest problems [6]. GSM1k (20240501) finds accuracy drops of up to 8% on a fresh set [7]. Singh et al. (20241106) tie a measure to downstream effect [8].
- **2026.** Spiesberger et al. (20260212) find semantic duplicates of benchmark items in an open training corpus, such as 78% of CodeForces problems [9]. Wang et al. (20260603) define search-time contamination, where an agent finds answers on the web [10]. See [agentic search](../trends/agentic-search.md).

## Where sources disagree

**How much it matters.** Brown et al. expected contamination "likely to be frequent, but that its effects may not be as large as feared" [5]. Singh et al. find it "may have a much larger effect than reported in recent LLM releases" [8]. Xiao and Cheng report that it inflates absolute scores but left a leaderboard's order almost unchanged (rank correlation 0.997; their own method) [11].

**What counts.** Singh et al. call it "surprisingly difficult to define precisely" which samples are contaminated [8]; Spiesberger et al. say n-gram filters miss semantic duplicates [9].

## Related

[Large language model](./large-language-model.md) · [disconnected reasoning](./disconnected-reasoning.md) · [link prediction](./link-prediction.md) · [FB15k-237](../datasets/fb15k-237.md) · [MuSiQue](../datasets/musique.md) · [ComplexWebQuestions](../datasets/complexwebquestions.md) · [HotpotQA benchmark](../benchmarks/hotpotqa.md) · [KILT](../benchmarks/kilt.md) · [Text2Cypher](../benchmarks/text2cypher.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Datasets**

- [ComplexWebQuestions](../datasets/complexwebquestions.md)
- [HotpotQA](../datasets/hotpotqa.md)
- [MuSiQue](../datasets/musique.md)
- [Wikipedia snapshots of DPR and KILT](../datasets/wikipedia-dpr-kilt.md)

**Benchmarks**

- [HotpotQA](../benchmarks/hotpotqa.md)
- [KILT](../benchmarks/kilt.md)

**Index**

- [Disconnected reasoning](disconnected-reasoning.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2308.08493 : Golchin and Surdeanu, "Time Travel in LLMs: Tracing Data Contamination in Large Language Models", 2 authors, v1 20230816, ICLR 2024 per the page; abstract (read 20261102 22:08 UTC)
2. https://arxiv.org/abs/2310.18018 : Sainz et al., "NLP Evaluation in trouble", 6 authors, v1 20231027, EMNLP 2024 Findings per the page; abstract (read 20261102 22:06 UTC)
3. https://api.crossref.org/works/10.1145/2382577.2382579 : Crossref record and abstract: Kaufman, Rosset, Perlich, Stitelman, "Leakage in data mining: formulation, detection, and avoidance", ACM TKDD 6(4), December 2012 (read 20261102 22:08 UTC)
4. https://arxiv.org/html/1707.01476 : Dettmers et al., "Convolutional 2D Knowledge Graph Embeddings", v1 20170705: abstract (a simple rule-based model reaches state-of-the-art results on WN18 and FB15k) and the sections on test leakage through inverse relations and WN18RR (read 20261102 22:08 UTC; submission date from https://arxiv.org/abs/1707.01476, read 22:08; the v1 text at https://arxiv.org/pdf/1707.01476v1, which credits Toutanova and Chen with first noting the problem, read 22:46)
5. https://arxiv.org/abs/2005.14165 : Brown et al., "Language Models are Few-Shot Learners", v1 20200528; section 4 "Measuring and Preventing Memorization Of Benchmarks" read in the full text at https://ar5iv.labs.arxiv.org/html/2005.14165 (read 20261102 22:08 UTC)
6. https://arxiv.org/abs/2403.07974 : Jain et al., "LiveCodeBench", v1 20240312; abstract (read 20261102 22:08 UTC)
7. https://arxiv.org/abs/2405.00332 : Zhang et al., "A Careful Examination of Large Language Model Performance on Grade School Arithmetic", 15 authors, v1 20240501; abstract (read 20261102 22:08 UTC)
8. https://arxiv.org/abs/2411.03923 : Singh et al., "Evaluation data contamination in LLMs: how do we measure it and (when) does it matter?", 7 authors, v1 20241106; abstract (read 20261102 22:06 UTC)
9. https://arxiv.org/abs/2602.12413 : Spiesberger et al., "Soft Contamination Means Benchmarks Test Shallow Generalization", 7 authors, v1 20260212; abstract (first-party analysis; read 20261102 22:16 UTC)
10. https://arxiv.org/abs/2606.05241 : Wang et al., "Search-Time Contamination in Deep Research Agents", 7 authors, v1 20260603, "Under Review"; abstract (read 20261102 22:16 UTC)
11. https://arxiv.org/abs/2609.02899 : Xiao and Cheng, "Contamination Inflates Scores but Rarely Reorders Large Language Model Leaderboards", v1 20260705 per the page; abstract (read 20261102 22:16 UTC)
12. https://aclanthology.org/W15-4007.pdf : Toutanova and Chen, "Observed versus latent features for knowledge base and text inference", 3rd Workshop on Continuous Vector Space Models and their Compositionality, Beijing, 26-31 July 2015: datasets table with "% Test Linked" (FB15K 80.9, WN18 94.0), construction of FB15k-237 (read 20261102 22:46 UTC)
