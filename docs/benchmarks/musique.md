---
type: benchmark
datasets: [musique]
updated: 20261102 21:22 UTC
---

# MuSiQue

This page answers what the MuSiQue benchmark measures, how it is scored, and what the numbers read so far show. The questions, their construction and the corpora retrieval papers use are on [the MuSiQue dataset page](../datasets/musique.md). Numbers come from the authors' paper (first-party) and two later studies: RAGSearch, which runs other teams' systems, and the HippoRAG 2 paper, first-party only for HippoRAG and HippoRAG 2. The official leaderboards could not be reached.

## What it tests

It tests whether a system answers a [multi-hop](../index/multi-hop-question-answering.md) question by using every reasoning step, not by a shortcut. The authors built the questions so that one step cannot be answered without the answer of the step before it, and they measure shortcut use directly with a "DiRe" score [1]. A harder variant, MuSiQue-Full, also asks the system to say when the context does not contain the answer [1].

## Tasks, metrics and protocol

- **MuSiQue-Ans.** Given a question and 20 paragraphs, predict the answer and the supporting paragraphs. Scores are answer F1 (An) and paragraph-level support F1 (Sp) [1].
- **MuSiQue-Full.** Each answerable item is paired with an unanswerable twin. A system must also predict whether the context suffices. A pair scores zero if the sufficiency call is wrong on either item; otherwise it gets its An (or Sp) score on the answerable item. The metrics are An+Sf and Sp+Sf, averaged over pairs [1].
- **Official script and leaderboards.** `evaluate_v1.0.py` returns `answer_f1` and `support_f1`, and for Full also two group-sufficiency F1 scores. The README names two leaderboards, MuSiQue-Answerable and MuSiQue-Full, taking test predictions [2].
- **Use in retrieval papers.** Later papers drop the fixed context, index passages and score the final answer with exact match or F1 (see Results).

## Datasets

One dataset, [MuSiQue](../datasets/musique.md). Retrieval studies use samples of its questions (RAGSearch: the full dev set) with their own corpus choice.

## Results

Scores on different rows are not comparable: the metric, split, reader and corpus differ. Within a block they are.

**Block A. The original task (answer F1 | support F1), reported by the MuSiQue authors in the paper, Tables 3-5 [1].** Version 3 dated 20220505. The models are Longformer-Large, RoBERTa-large and BART-large pipelines.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Human score (125 sampled questions) | 78.0 / 93.9 | An F1 / Sp F1 | MuSiQue authors | yes | 20220505 | [1] Table 3 |
| Select+Answer, dev | 47.3 / 72.3 | An F1 / Sp F1 | MuSiQue authors | yes | 20220505 | [1] Table 4 |
| Step Execution (Select+Answer), dev | 49.8 / 79.2 | An F1 / Sp F1 | MuSiQue authors | yes | 20220505 | [1] Table 4 |
| One-paragraph model, dev | 32.0 / n.a. | An F1 | MuSiQue authors | yes | 20220505 | [1] Table 4 |
| Select+Answer, test (Ans) | 52.3 / 75.2 | An F1 / Sp F1 | MuSiQue authors | yes | 20220505 | [1] Table 5 |
| Step Execution (Select+Answer), test (Ans) | 49.0 / 80.6 | An F1 / Sp F1 | MuSiQue authors | yes | 20220505 | [1] Table 5 |
| Select+Answer, test (Full) | 34.8 / 42.1 | An+Sf / Sp+Sf | MuSiQue authors | yes | 20220505 | [1] Table 5 |

**Block B. Contain exact match, Qwen2.5-7B, full dev set (2,417), RAGSearch Table 1 [4].** Run by the RAGSearch authors, who also built that benchmark. "Best GraphRAG" is the best of five graph backends per cell.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Single-shot, dense | 20.99 | Contain EM | RAGSearch authors | no (other teams' systems) | 20260401 | [4] |
| Single-shot, best GraphRAG | 47.95 | Contain EM | RAGSearch authors | no | 20260401 | [4] |
| GraphSearch agent, dense / best GraphRAG | 13.33 / 55.26 | Contain EM | RAGSearch authors | no | 20260401 | [4] |
| Search-o1, dense / best GraphRAG | 12.62 / 32.44 | Contain EM | RAGSearch authors | no | 20260401 | [4] |
| Search-R1 (trained) / Graph-R1 (trained) | 14.42 / 40.82 | Contain EM | RAGSearch authors | no | 20260401 | [4] |

**Block C. F1, Llama-3.3-70B reader, sampled questions with a pooled corpus (sample and corpus on the dataset page), HippoRAG 2 Table 2 [5].** Run by the HippoRAG 2 authors. HippoRAG and HippoRAG 2 share three authors (Gutiérrez, Shu, Su) [6]; the other rows are baselines or competitors that those authors re-ran.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| No retrieval | 26.1 | F1 | HippoRAG 2 authors | no (baseline) | 20250619 | [5] |
| BM25 | 28.8 | F1 | HippoRAG 2 authors | no (re-run by a competitor) | 20250619 | [5] |
| NV-Embed-v2 (dense) | 45.7 | F1 | HippoRAG 2 authors | no (re-run by a competitor) | 20250619 | [5] |
| GraphRAG | 38.5 | F1 | HippoRAG 2 authors | no (re-run by a competitor) | 20250619 | [5] |
| LightRAG | 1.6 | F1 | HippoRAG 2 authors | no (re-run by a competitor) | 20250619 | [5] |
| HippoRAG | 35.1 | F1 | HippoRAG 2 authors | yes | 20250619 | [5] |
| HippoRAG 2 | 48.6 | F1 | HippoRAG 2 authors | yes | 20250619 | [5] |

LightRAG's 1.6 is a re-run result. The paper blames LLM-generated noise for the weak showing of GraphRAG and LightRAG in general, and does not examine the 1.6 itself [5].

*Reading:* this page holds no independent ranking of systems on the original task: the numbers there are the authors' own, and the leaderboards were not read. On the retrieval version, Blocks B and C disagree. In B, the best graph backend beats the dense baseline in every row, by 19.8 to 41.9 points depending on the agent (the gaps printed in Table 1; the Graph-R1 row is against Search-R1) [4]. In C, only HippoRAG 2 is ahead of the strong dense retriever (48.6 against 45.7), and GraphRAG, HippoRAG and LightRAG are behind it [5]. The two studies differ in corpus, reader and metric (see Known problems), so neither settles whether graphs help on MuSiQue.

## Known problems

- **Leaderboards unread.** The host `leaderboard.allenai.org` did not resolve on 20261102 20:41 (`ENOTFOUND`). A web-archive copy returned only the title "AI2 Leaderboard", with no rows [3]. The current state of the art on the original task is **unstated**.
- **Old models.** Block A is from 2020-era models. No newer score on the original reading-comprehension task was read.
- **README and paper disagree by 0.1.** For Step Execution (Select+Answer) on dev, the README prints answer F1 0.497 and support F1 0.792; the paper's Table 4 gives 49.8 and 79.2. The support score matches, and so do the README's Select+Answer dev scores (0.473 / 0.723 against 47.3 / 72.3). The cause is **unstated** [1][2].
- **Mixed knowledge sources.** In RAGSearch the dense backend retrieves from a 2018 Wikipedia dump, while the GraphRAG backends use each question's own context as the document [4]. How much of the gap this explains is **unstated** in the paper.
- **Different tasks under one name.** The original task gives each question its own 20 paragraphs [1]; retrieval studies pool passages or swap the context, so their scores cannot be compared with Block A, or with each other where the corpus differs. The corpus facts are on [the dataset page](../datasets/musique.md).
- **Small human sample.** The human score is from 125 questions, 3 annotations each [1].
- **Contamination.** Seed-set overlap is on [the dataset page](../datasets/musique.md).

## Used by

[RAGSearch](ragsearch.md) (a GraphRAG-versus-dense benchmark) [4]; the HippoRAG 2 paper and the [HippoRAG](../projects/hipporag.md) project [5]; a Cognee tuning paper [7]; the trends [Graph-based RAG](../trends/graph-based-rag.md) and [Agentic graph retrieval](../trends/learned-graph-traversal.md). Sibling benchmarks on [HotpotQA](hotpotqa.md) and [2WikiMultiHopQA](2wikimultihopqa.md) are the sets the paper compares against [1].

## Sources

1. https://arxiv.org/html/2108.00573v3 and https://arxiv.org/pdf/2108.00573 : MuSiQue paper v3 (5 May 2022): tasks, metrics (Section 7.1), Tables 3, 4, 5 (read 20261102 21:16 UTC; first read 20:41)
2. https://github.com/StonyBrookNLP/musique : README: evaluation script, example outputs, leaderboard links (read 20261102 21:15 UTC; first read 20:41)
3. https://leaderboard.allenai.org/musique_ans : host not found; https://web.archive.org/web/2024/https://leaderboard.allenai.org/musique_ans : title only (tried 20261102 20:41 and 20:42 UTC)
4. https://arxiv.org/html/2604.09666 : RAGSearch v1 (1 April 2026): Table 1 rows and printed gaps, backends, dense corpus and "context of each question as the document" (read 20261102 21:15 UTC)
5. https://arxiv.org/html/2502.14802 : HippoRAG 2 v2 (19 June 2025): Table 2, baselines re-run with the same reader and retriever, remark on LLM-generated noise (read 20261102 21:15 UTC)
6. https://export.arxiv.org/api/query?id_list=2502.14802,2405.14831 : author lists of HippoRAG 2 and HippoRAG (read 20261102 21:20 UTC)
7. https://arxiv.org/abs/2505.24478 : Cognee tuning paper v1 (30 May 2025): abstract (read 20261102 20:43 UTC)
