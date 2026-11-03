---
type: index
kind: concept
aliases: [EM, exact-match accuracy, exact matching]
updated: 20261102 22:54 UTC
---

# Exact match

This entry says what the exact-match score measures and why papers from 2023 to 2026 argue it misjudges generated answers. The words also name a retrieval idea, noted in the definition.

## Definition

Exact match (EM) scores a predicted answer 1 when it equals a reference answer and 0 otherwise, then averages over questions [5]. SQuAD defines it as the percentage of predictions that "match any one of the ground truth answers exactly", ignoring punctuation and articles [1]. A copy of the official v1.1 script also lower-cases and collapses whitespace before comparing [2]. Dense Passage Retrieval scores end-to-end answers by "exact match with the reference answer after minor normalization" [3]. In retrieval the phrase has a second sense: query terms and document terms must match exactly to add to a score, as in [BM25](./bm25.md) [4].

## How it changed

- **20160616.** SQuAD reports EM and F1; humans score 77.0% EM and 86.8% F1 on the test set (first-party) [1]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20200410.** DPR reports end-to-end EM on five question sets, following Chen et al. (2017) and Lee et al. (2019) (first-party) [3]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20230511.** Kamalloo et al. regrade by hand the answers to 301 Natural Questions test questions. InstructGPT zero-shot scores 12.6% EM and 71.4% by human judgement. In the ACL 2023 version (v3, 20230706) the rank correlation with the human ranking is 0.23 for EM; the first version gives 0.22 [5].
- **20241014.** LongMemEval says an exact matching strategy "can result in high error rates" (the ICLR 2025 version says "inaccurate evaluations") and uses a GPT-4o judge instead, with over 97% agreement with human experts (first-party) [6]. See [LLM-as-judge](./llm-as-judge.md).
- **20250920.** Abbood et al. show that for numeric temporal answers EM cannot tell small errors from large ones; the most frequent error is off by one [7].
- **20260724.** A preprint under review reports that, in product attribute extraction, the matching protocol (exact or fuzzy) causes about 23 times the F1 variance of the choice of model [8].

## Where sources disagree

**What counts as the same string.** The SQuAD script strips case, punctuation and articles [2]; DPR says "minor normalization" without listing it [3]. Kamalloo et al. find regex matching ranks models like human judges, though "still suffering from unnecessary strictness" [5].

**Whether a model can replace it.** LongMemEval reports its judge matches experts [6]. Kamalloo et al. find automated evaluation models weak at spotting hallucinated long answers and conclude that "at this time, there appears to be no substitute for human evaluation" [5].

## Related

[LLM-as-judge](./llm-as-judge.md), [open-domain question answering](./open-domain-question-answering.md), [question answering](./question-answering.md), [multi-hop question answering](./multi-hop-question-answering.md), [BM25](./bm25.md), [Boolean retrieval](./boolean-retrieval.md), [dense retrieval](./dense-retrieval.md). Benchmarks: [HotpotQA](../benchmarks/hotpotqa.md), [Natural Questions](../benchmarks/natural-questions.md), [KILT](../benchmarks/kilt.md), [LongMemEval](../benchmarks/longmemeval.md). Data: [TriviaQA](../datasets/triviaqa.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)

**Benchmarks**

- [Benchmarks](../benchmarks/README.md)
- [HotpotQA](../benchmarks/hotpotqa.md)
- [KILT](../benchmarks/kilt.md)
- [Natural Questions](../benchmarks/natural-questions.md)

**Index**

- [LLM-as-judge](llm-as-judge.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/1606.05250 : Rajpurkar, Zhang, Lopyrev, Liang, "SQuAD: 100,000+ Questions for Machine Comprehension of Text", EMNLP 2016, arXiv v1 of 20160616 (date from the arXiv API record, read 20261102 22:08 UTC): section 6.1 (EM and F1 definitions) and 6.2 (human scores); the quoted wording "match any one of the ground truth answers exactly" is from v3, while v1 reads "match one of the ground truth answers exactly" and gives the same 77.0% and 86.8% (first-party; read 20261102 22:51 UTC)
2. https://github.com/allenai/bi-att-flow/blob/master/squad/evaluate-v1.1.py : a copy of "Official evaluation script for v1.1 of the SQuAD dataset" in a third-party repository, read by `gh api`: `normalize_answer` and `exact_match_score` (read 20261102 22:17 UTC)
3. https://arxiv.org/pdf/2004.04906 : Karpukhin et al., "Dense Passage Retrieval for Open-Domain Question Answering", arXiv v1 of 20200410 (date from the arXiv API record, read 20261102 22:17 UTC): section 6.2, Table 4 (first-party; read 20261102 22:17 UTC)
4. https://arxiv.org/pdf/2010.06467 : Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking: BERT and Beyond", arXiv v3 of 20210819: section 1.2.2, "The Challenges of Exact Match" (read 20261102 22:17 UTC)
5. https://arxiv.org/pdf/2305.06984 : Kamalloo, Dziri, Clarke, Rafiei, "Evaluating Open-Domain Question Answering in the Era of Large Language Models", ACL 2023, arXiv v1 of 20230511, v3 of 20230706 (dates from the arXiv API record): abstract; section 3 (EM definition and normalisation); Table 1 and section 4 (sample of 301 questions, Kendall's tau 0.23 for EM in v3 and 0.22 in v1); "still suffering from unnecessary strictness" is in the v3 abstract only; "no substitute for human evaluation" is in both (read 20261102 22:51 UTC)
6. https://arxiv.org/pdf/2410.10813 : Wu et al., "LongMemEval", ICLR 2025, arXiv v1 of 20241014, v2 of 20250304 (dates from the arXiv API record): v1 section 3.4 ("can result in high error rates"; more than 97% agreement with human experts); v2 section 3.3 and appendix A.4 ("can result in inaccurate evaluations"; same agreement figure) (first-party; read 20261102 22:51 UTC)
7. https://arxiv.org/abs/2509.16720 : Abbood, Meng, Collier, "Time to Revist Exact Match" (title as printed), Findings of EMNLP 2025, arXiv v1 of 20250920: abstract only (read 20261102 22:18 UTC)
8. https://arxiv.org/abs/2607.22949 : Dwivedi and Soni, "Beyond Exact Match: How Evaluation Methodology Dominates Model Choice in LLM-Based Product Attribute Extraction", arXiv v1 of 20260724, "preprint under review": abstract only (read 20261102 22:18 UTC)
