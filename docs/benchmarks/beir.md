---
type: benchmark
datasets: [hotpotqa, natural-questions, ms-marco]
updated: 20261102 21:26 UTC
---

# BEIR

This page answers how retrieval models are tested on BEIR, which data it holds, and what the results show. BEIR has no dataset page: it collects 18 existing sets, so its data is described here. The paper has 2,235 citations (Semantic Scholar, read 20261102 20:01 UTC) [10]; the newest leaderboard row is dated 20230213 [7].

## What it tests

Zero-shot out-of-distribution generalisation of [retrieval](../index/information-retrieval.md) models: a model is trained elsewhere, mostly on [MS MARCO](ms-marco.md), then scored on 18 sets from 9 tasks without further training [1]. In-domain scores do not predict this: [BM25](../index/bm25.md) trails the neural models by 7 to 18 points on MS MARCO, yet is a strong baseline across BEIR [1].

## Tasks, metrics and protocol

- **Metric.** [nDCG@10](../index/ndcg.md), computed with the TREC evaluation tool. Recall@100 is also reported [1].
- **Systems in the paper.** Ten, from five families: lexical (BM25), sparse, [dense](../index/dense-retrieval.md), late interaction (ColBERT) and [re-ranking](../index/reranking.md) (BM25 plus a cross-encoder). Neural models read the first 512 word pieces [1].

| Task | Datasets |
|---|---|
| Fact checking | FEVER, Climate-FEVER, SciFact |
| Question answering | NQ, HotpotQA, FiQA-2018 |
| Bio-medical | TREC-COVID, NFCorpus, BioASQ |
| News; argument; duplicate question | TREC-NEWS, Robust04; ArguAna, Touché-2020; CQADupStack, Quora |
| Entity; citation; tweet | DBPedia-Entity, SCIDOCS, Signal-1M (RT) [1] |

## Datasets

Corpora run from 3,633 documents (NFCorpus) to 14,914,602 (BioASQ); test sets from 49 queries (Touché-2020) to 13,145 (CQADupStack) [1]. Three sets have their own pages: [HotpotQA](../datasets/hotpotqa.md), [Natural Questions](../datasets/natural-questions.md) and [MS MARCO](../datasets/ms-marco.md), the last only as the in-domain reference [1].

**Licence.** The code is Apache-2.0, from the LICENSE file [4]. The data has no single licence. The paper lists MIT for non-commercial research purposes (MS MARCO), CC BY-SA 3.0 or 4.0, CC BY 4.0, Apache-2.0 (CQADupStack), CC BY-NC 2.0 (SciFact), GPL v3 (SCIDOCS), "under Copyright" (TREC-NEWS, Robust04, BioASQ), a "Dataset License Agreement" (TREC-COVID), and none stated for four sets (NFCorpus, FiQA-2018, Quora, Climate-FEVER) [1]. The Hugging Face card header says `cc-by-sa-4.0`, which does not describe those parts [5]. *Reading:* with non-commercial, GPL and copyright parts, treat the data as a read-only reference.

**Versions.** Paper v1 20210417, v4 20211021; accepted at NeurIPS 2021 Datasets and Benchmarks [2]. Code: `beir-cellar/beir`, last push 20251016 [4]. BioASQ, Signal-1M, TREC-NEWS and Robust04 are not directly downloadable [3].

**How it was made.** By selection of public sets, balanced so that question answering does not dominate. For TREC-COVID the authors added 980 missing relevance judgements by hand [1].

## Results

Scores are nDCG@10. Rows 1 to 3 are the BEIR authors' own, from Table 2 [1]; datasets are TREC-COVID, HotpotQA, NQ, Touché-2020, BioASQ.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| BM25 | 0.656, 0.603, 0.329, 0.367, 0.465 | nDCG@10 | BEIR authors | yes | 20211021 | [1] |
| BM25 + cross-encoder | 0.757, 0.707, 0.533, 0.271, 0.523; +11% mean vs BM25 | nDCG@10 | BEIR authors | yes | 20211021 | [1] |
| TAS-B (dense) | 0.481, 0.584, 0.463, 0.162, 0.383; -2.8% mean | nDCG@10 | BEIR authors | yes | 20211021 | [1] |
| BM25; SPLADE; Contriever; TAS-B | mean over 18 sets: 0.429; 0.474; 0.448; 0.424 | nDCG@10 | Kamalloo et al. (Waterloo, Naver) | no, but shares an author with BEIR | 20230613 | [8] |
| RankT5 on BM25 + SPLADE top 50 (team "nle") | mean 0.5525 | nDCG@10 | submitting team | no, self-reported | 20230128 | [7] |
| InParsv2 (team "ZA+NM+Unicamp") | mean 0.5457 | nDCG@10 | submitting team | no, self-reported | 20230112 | [7] |
| DRAGON+ (team "MetaAI+UW*2"); SPLADE baseline | mean 0.474; 0.474 | nDCG@10 | submitting team; BEIR | no; yes | 20230213; 20221222 | [7] |

Comparing the two Table 2s, the re-run [8] gives the same BM25 scores as the BEIR paper on all five sets; TAS-B on TREC-COVID is 0.505 there against 0.481 in the paper. Every row was run by the BEIR authors, by a group sharing an author with them, or by the model's own team; an independent reproduction is not among the sources read. The three external rows are not verified by the host, and their "data that model was trained on" field is empty, so their zero-shot status is **unstated** [7].

## Known problems

- **Lexical bias.** Judgements came from lexical systems. Adding 980 judgements to TREC-COVID lifted ANCE from 0.654 to 0.735 and BM25 from 0.656 to 0.668 [1].
- **Averages hide it.** The re-run's authors call the macro-average deficient, note that papers report subsets of 11 to 15 datasets, and suspect NQ gains are an MS MARCO transfer artefact [8].
- **Scope.** English only, short documents, text only [1].
- **Stale board.** The EvalAI challenge is marked inactive with an end date of 20260131; the wiki calls the older sheets deprecated since 20230110 [6][7].

## Used by

[HotpotQA](hotpotqa.md), [Natural Questions](natural-questions.md) and [MS MARCO](ms-marco.md) report BEIR rows; the paper contrasts itself with [KILT](kilt.md), which retrieves only from Wikipedia [1]. [EnterpriseRAG-Bench](enterpriserag-bench.md) cites it as a meta-benchmark [9]. See also [language models meet retrieval](../history/language-models-meet-retrieval.md) and [foundations](../papers/foundations.md).

## Sources

1. https://arxiv.org/html/2104.08663 : BEIR paper v4: datasets, Tables 1, 2 and 4, related work (KILT), Appendices B, D, E (read 20261102 20:53 UTC; Table 2 and Appendix E re-read 20261102 21:24 UTC)
2. https://arxiv.org/abs/2104.08663 : submission history, NeurIPS 2021 note (read 20261102 20:53 UTC)
3. https://raw.githubusercontent.com/beir-cellar/beir/main/README.md : download notes (read 20261102 20:53 UTC)
4. https://api.github.com/repos/beir-cellar/beir and its license endpoint : LICENSE is Apache-2.0, last push 20251016 (read 20261102 20:53 UTC)
5. https://huggingface.co/datasets/BeIR/beir/raw/main/README.md : card licence (read 20261102 20:53 UTC)
6. https://github.com/beir-cellar/beir/wiki/Leaderboard : EvalAI link, sheets deprecated 20230110 (read 20261102 20:53 UTC)
7. https://eval.ai/api/jobs/challenge_phase_split/4475/leaderboard/ and https://eval.ai/api/challenges/challenge/1897/ : eight rows, challenge dates (read 20261102 20:55 UTC)
8. https://arxiv.org/html/2306.07471 : Kamalloo et al., Resources for Brewing BEIR, Table 2 and sections 4 and 6 (read 20261102 20:53 UTC; Table 2 re-read 20261102 21:24 UTC)
9. https://arxiv.org/html/2605.05253 : EnterpriseRAG-Bench v2, related work (read 20261102 20:58 UTC)
10. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 2,235 (read 20261102 20:01 UTC, carried from the dataset and benchmark candidate pool)
