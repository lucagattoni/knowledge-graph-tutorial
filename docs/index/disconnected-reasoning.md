---
type: index
kind: concept
aliases: [DiRe]
updated: 20261102 22:51 UTC
---

# Disconnected reasoning

This entry says what disconnected reasoning is, how it was measured, and how multi-hop question sets were rebuilt to resist it.

## Definition

In [multi-hop question answering](./multi-hop-question-answering.md) a question needs several supporting facts. A model reasons in a disconnected way when it combines its outputs on two subsets of the input, neither of which holds all the supporting facts, without any interaction between the two [1]. Trivedi et al. call this "disconnected reasoning" (DiRe) and give a formal condition for it, which turns into a probe that works on any model [1]. A model that passes by this route gets the right answer without connecting the facts [1].

## How it changed

- **20190427 to 20190617.** Three papers show shortcuts in earlier sets. Chen and Durrett find that sentence-factored models, which "by design" cannot do multi-hop reasoning, still solve many WikiHop and HotpotQA examples (NAACL 2019) [2]. Min et al. get 67 F1 on HotpotQA from a single-hop BERT model (ACL 2019) [3]. Jiang and Bansal add adversarial documents (ACL 2019) [4]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20200502.** Trivedi et al. (EMNLP 2020) formalise the behaviour. For XLNet only 18 of its 72 answer F1 on HotpotQA come from reasoning over several facts, about as for a simpler RNN; their dataset transformation cuts disconnected reasoning by 19 points (first-party) [1].
- **20210802.** MuSiQue (TACL 2022) composes connected single-hop questions into 2 to 4 hop ones; relative to existing datasets, a single-hop model has a 30 point drop in F1 (first-party) [5]. See [MuSiQue](../datasets/musique.md).
- **20221013.** Guo, Gong and Lai propose a counterfactual method to reduce it on HotpotQA (no venue stated on its arXiv page) [6].
- **20251013.** Liu et al. (ECIR 2026) build "uncheatable" unanswerable multi-hop queries, with up to 81.0% lower cheatability scores than earlier RAG benchmarks (first-party) [7]. Multi-hop retrieval systems are in [Graph-based RAG](../trends/graph-based-rag.md).

## Where sources disagree

**How to measure it.** Trivedi et al. call the meaning of a "meaningful synthesis" of facts "somewhat subjective" [1]. The earlier papers probe different shortcuts: a single-hop model [3], sentence-level models [2], adversarial text [4]. No source read compares the probes on one model.

**Which fix works.** Trivedi et al. report that their transformation reduces it more than adversarial augmentation, and adds to it when combined [1]. Jiang and Bansal report their adversarially trained baseline improves but stays limited [4]. No independent comparison is among the sources read.

## Related

[Multi-hop question answering](./multi-hop-question-answering.md) · [data contamination](./data-contamination.md) · [question answering](./question-answering.md) · [HotpotQA dataset](../datasets/hotpotqa.md) and [benchmark](../benchmarks/hotpotqa.md) · [MuSiQue benchmark](../benchmarks/musique.md) · [2WikiMultiHopQA benchmark](../benchmarks/2wikimultihopqa.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Datasets**

- [HotpotQA](../datasets/hotpotqa.md)
- [MuSiQue](../datasets/musique.md)

**Index**

- [Data contamination](data-contamination.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2005.00789 : Trivedi, Balasubramanian, Khot, Sabharwal, "Is Multihop QA in DiRe Condition? Measuring and Reducing Disconnected Reasoning", v1 20200502, EMNLP 2020 per the page; abstract (read 20261102 22:06 UTC); the definition, Figure 1 caption and "somewhat subjective" (sections 1 and 3) from the full text at https://ar5iv.labs.arxiv.org/html/2005.00789 (read 20261102 22:07 UTC)
2. https://arxiv.org/abs/1904.12106 : Chen and Durrett, "Understanding Dataset Design Choices for Multi-hop Reasoning", v1 20190427, NAACL 2019 per the page; abstract (read 20261102 22:06 UTC)
3. https://arxiv.org/abs/1906.02900 : Min et al., "Compositional Questions Do Not Necessitate Multi-hop Reasoning", 6 authors, v1 20190607, ACL 2019 (short) per the page; abstract (read 20261102 22:06 UTC)
4. https://arxiv.org/abs/1906.07132 : Jiang and Bansal, "Avoiding Reasoning Shortcuts", v1 20190617, ACL 2019 per the page; abstract (read 20261102 22:06 UTC)
5. https://arxiv.org/abs/2108.00573 : Trivedi et al., "MuSiQue: Multihop Questions via Single-hop Question Composition", 4 authors, v1 20210802, TACL 2022 per the page; abstract (read 20261102 22:06 UTC)
6. https://arxiv.org/abs/2210.07138 : Guo, Gong, Lai, "Counterfactual Multihop QA: A Cause-Effect Approach for Reducing Disconnected Reasoning", v1 20221013; abstract (read 20261102 22:08 UTC)
7. https://arxiv.org/abs/2510.11956 : Liu et al., "Investigating Retrieval-Augmented Generation Systems on Unanswerable, Uncheatable, Realistic, Multi-hop Queries", 5 authors, v1 20251013, v3 20260114, ECIR 2026 per the page; abstract (read 20261102 22:08 UTC)
