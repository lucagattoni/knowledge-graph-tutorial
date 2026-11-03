---
type: benchmark
datasets: [natural-questions]
updated: 20261102 21:25 UTC
---

# Natural Questions

This page answers how systems are scored on Natural Questions (NQ) and what the numbers show. The data is on [the Natural Questions dataset page](../datasets/natural-questions.md). The official leaderboard could not be read, so results come from papers.

## What it tests

The original task: read a whole Wikipedia page and find the smallest passage that answers a real search question, or say there is none [1]. Later work drops the page and asks [open-domain](../index/open-domain-question-answering.md) questions: retrieve from Wikipedia, then answer. Recent [RAG](../index/retrieval-augmented-generation.md) studies use NQ as the single-hop control for multi-hop sets [6][7][8].

## Tasks, metrics and protocol

- **Original task.** Input: a question and a full page. Output: a long answer (an HTML box) or null, and a short answer (spans, yes/no or null) [1].
- **Original metric.** With five annotations per item: if at least two annotators gave a non-null long answer, the system must return one that matches; otherwise it must return null. Precision, recall and F1 follow [1]. The test set is hidden; a Docker image goes to a competition site [2].
- **Human bound.** On the development set, from a sample of five annotations drawn from the 25-way annotated data, a "super-annotator" scores 87.2 F1 (long) and 75.7 (short); one annotator scores 73.4 and 57.5. The paper gives no test-set figures for either [1].
- **Open-domain NQ.** [Exact match](../index/exact-match.md) of the generated answer after normalisation, on the open-domain test split described on the dataset page, over the passages described on [the Wikipedia snapshots page](../datasets/wikipedia-dpr-kilt.md) [3].
- **Retrieval forms.** Top-k accuracy: the share of questions with the answer string in the top k passages [3]. BEIR uses nDCG@10 [5].

## Datasets

[Natural Questions](../datasets/natural-questions.md), with its KILT, BEIR and open-domain versions.

## Results

Rows from different blocks are not comparable: metric, split, corpus and reader differ.

**A. Original task, Table 3 of the NQ paper [1].** All first-party.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| DecAtt + DocReader | long 55.0, short 31.5 (test) | F1 | NQ authors | yes | 201907 | [1] |
| DocumentQA | long 45.7, short 35.1 (test) | F1 | NQ authors | yes | 201907 | [1] |

**B. Open-domain NQ, exact match.** Each method's authors ran their own.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Single ORQA | 33.3 | EM | ORQA authors (Lee et al. 2019), copied by the DPR authors | yes (own authors' number) | reported in DPR v3, 20200930 | [3] |
| Single REALM (News) | 40.4 | EM | REALM authors (Guu et al. 2020), copied by the DPR authors | yes (own authors' number) | reported in DPR v3, 20200930 | [3] |
| DPR | 41.5 | EM | DPR authors | yes | 20200930 | [3] |
| RAG-Sequence; RAG-Token | 44.5; 44.1 | EM | RAG authors | yes | 20210412 | [9] |
| RAG; BART + DPR; BART (no retrieval), KILT held-out test | 44.39; 41.27; 21.75 | EM | KILT authors (overlap with RAG's) | yes (for KILT) | 20210527 | [4] |

**C. Retrieval.**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| DPR against [BM25](../index/bm25.md) | 78.4 against 59.1 (top 100: 85.4 against 73.7) | top-20 accuracy | DPR authors | yes | 20200930 | [3] |
| BM25; DPR (Multi-DPR, trained on NQ among four sets); ColBERT; BM25 + cross-encoder | 0.329; 0.474; 0.524; 0.533 | nDCG@10 | BEIR authors | yes (for BEIR) | 20211021 | [5] |

**D. Dense RAG against [GraphRAG](../index/graphrag.md), 2025 to 2026.**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Vanilla RAG; Community-GraphRAG (Local); HippoRAG 2 (Llama-3.1-8B) | 64.78; 63.01; 61.03 | F1 | Han et al. | no | 20260304 | [6] |
| Dense retriever (NV-Embed-v2); HippoRAG 2; GraphRAG; LightRAG (Llama-3.3-70B, 1,000 queries) | 61.9; 63.3; 46.9; 16.6 | F1 | HippoRAG 2 authors | yes (for HippoRAG 2) | 20250619 | [7] |
| Single-shot, dense; best of five GraphRAG backends (Qwen2.5-7B, 3,610 test) | 46.62; 48.31 | Contain EM | Fan et al. | no | 20260401 | [8] |
| Search-R1; Graph-R1 (trained on NQ and HotpotQA) | 48.72; 46.71 | Contain EM | Fan et al. | no | 20260401 | [8] |

*Reading:* the two independent studies in block D both report small differences on NQ: the best graph method is 1.8 points behind plain RAG in one and 1.7 ahead in the other [6][8]. In [RAGSearch](ragsearch.md) the three multi-hop sets move by about 27 points [8]. Both studies index per-question or per-document context (see Known problems), so NQ here does not show that graphs add little in general. The HippoRAG 2 authors' table shows a dense retriever close behind their method and other graph methods far behind [7]. Setups differ; this is not a ranking.

## Known problems

- **Leaderboard unread.** The official page shows only "Loading...", so the current state of the art on the original task is **unstated**; block A holds 2019 models [10].
- **Not one test.** Open-domain NQ numbers come from different splits, corpora and normalisation: DPR uses the test split of Lee et al. 2019, KILT a held-out test [3][4].
- **String match.** Top-k accuracy counts an answer string in a passage, not whether the passage answers [3].
- **Uneven corpora.** In RAGSearch the dense backend searches a Wikipedia dump, while GraphRAG backends use each question's own context as the document [8]. In Han et al. NQ is one small index per document, and the number of questions is **unstated** [6].
- **In-domain training.** NQ is in-domain for DPR's retriever and the trained agents in RAGSearch [3][8]; BEIR marks DPR's NQ score as in-domain [5].
- **Contamination** by pretraining data is **unstated**.

## Used by

[DPR, REALM and RAG](../papers/foundations.md) (papers) [3][9]; [KILT](kilt.md) and [BEIR](beir.md) [4][5]; [RAGSearch](ragsearch.md), the [HippoRAG 2](../papers/graph-based-rag.md) paper and the [HippoRAG](../projects/hipporag.md) project [7][8]; the [Graph-based RAG](../trends/graph-based-rag.md) trend. Multi-hop siblings: [HotpotQA](hotpotqa.md), [MuSiQue](musique.md).

## Sources

1. https://aclanthology.org/Q19-1026.pdf : NQ paper, Sections 5 and 6, Table 3 (read 20261102 20:41 and 21:21 UTC)
2. https://github.com/google-research-datasets/natural-questions : README, hidden-test protocol (read 20261102 20:41 UTC)
3. https://arxiv.org/pdf/2004.04906 : DPR v3 (30 Sep 2020), Tables 1, 2, 4 and the Table 4 caption (read 20261102 20:41 and 21:21 UTC)
4. https://arxiv.org/pdf/2009.02252 : KILT v4 (27 May 2021), Table 3 and Section 3.4 (read 20261102 20:41 UTC)
5. https://arxiv.org/pdf/2104.08663 : BEIR v4 (21 Oct 2021), Table 2 and Appendix D (read 20261102 20:47 and 21:21 UTC)
6. https://arxiv.org/pdf/2502.11371 : RAG versus GraphRAG v3 (4 Mar 2026), Table 1, Appendix A.1 (read 20261102 20:41 and 21:21 UTC)
7. https://arxiv.org/pdf/2502.14802 : HippoRAG 2 v2 (19 Jun 2025), Tables 1 and 2 (read 20261102 20:44 UTC)
8. https://arxiv.org/pdf/2604.09666 : RAGSearch v1 (1 Apr 2026), Table 1, Section 5.1, Appendix B (read 20261102 20:41 and 21:21 UTC)
9. https://arxiv.org/pdf/2005.11401 : RAG v4 (12 Apr 2021), Table 1 (read 20261102 20:44 UTC)
10. https://ai.google.com/research/NaturalQuestions : script-rendered, only "Loading..." (read 20261102 20:41 UTC)
