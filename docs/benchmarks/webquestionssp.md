---
type: benchmark
datasets: [webquestionssp]
updated: 20261102 21:27 UTC
---

# WebQuestionsSP

This page answers what the WebQuestionsSP (WebQSP) benchmark measures, how it is scored, and what the numbers read so far show. The questions, their size, licence and construction are on [the WebQuestionsSP dataset page](../datasets/webquestionssp.md). Each result row is either the scored system's own authors' number (first-party) or a baseline printed in another system's paper; I read no leaderboard.

## What it tests

It tests [knowledge-base question answering](../index/knowledge-base-question-answering.md): given a short question, return the set of [Freebase](../datasets/freebase.md) entities or values that answers it. The 2016 paper asked whether labelling [semantic parses](../index/semantic-parsing.md) beats labelling only answers [1]. Since 2023 it mostly scores systems that pair a [large language model](../index/large-language-model.md) with a graph [3][8].

## Tasks, metrics and protocol

- **Original protocol.** The dataset's own train/test split (counts on the dataset page). Per question: precision, recall and F1 of the answer set. The average F1 is the headline; "accuracy" is exact match of the whole set [1].
- **Official script `eval.py`.** Scores each question on the best F1 over its gold parses; an empty gold set with an empty prediction counts as correct. Written for Python 2 [2].
- **RoG split.** RoG, GCR and OntGQA train on 2,826 questions and test on 1,628; RoG's copy adds a 246-question validation set [4][7][9][10]. G-Retriever takes that copy [5]. GNN-RAG uses 2,848 train, 250 development and the full original test set [6].
- **Metric names differ.** RoG defines Hits@1 as the share of questions whose top-1 prediction is correct [4]. GCR defines Hit as "any correct answer exists in the generated predictions" [7]. GNN-RAG's table puts RoG at 85.7 under Hit and 80.0 under Hits@1 [6].
- **Knowledge source.** Freebase, or a subgraph within the question's reasoning hops [5][7].

## Datasets

One dataset, [WebQuestionsSP](../datasets/webquestionssp.md), usually reported next to [ComplexWebQuestions](../datasets/complexwebquestions.md).

## Results

Compare only within a block: splits, metrics and models differ. Dates are the first arXiv version (venue date for STAGG, OntGQA); the numbers were read in the later versions named in Sources.

**A. Original protocol, original test set, STAGG semantic parser.**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| STAGG, trained on answers | 66.8 (accuracy 58.8) | avg F1 | WebQSP authors | yes | 2016 (ACL, 7-12 Aug) | [1] Table 1 |
| STAGG, trained on parses | 71.7 (accuracy 63.9) | avg F1 | WebQSP authors | yes | 2016 (ACL, 7-12 Aug) | [1] Table 1; [2] |

**B. Prompting without training, exact-match Hits@1, original test set [3].**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| ChatGPT, no graph | 63.3 | Hits@1 | ToG authors | no (baseline) | 20230715 | [3] Table 1 |
| ToG, ChatGPT | 76.2 | Hits@1 | ToG authors | yes | 20230715 (ICLR 2024) | [3] Table 1 |
| ToG, GPT-4 | 82.6 | Hits@1 | ToG authors | yes | 20230715 | [3] Table 1 |

**C. Fine-tuned or trained systems (splits as in the protocol list).**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| RoG, Llama-2-7B | 85.7 / 70.8 | Hits@1 / F1 | RoG authors | yes | 20231002 | [4] Table 1 |
| G-Retriever, Llama-2-7B (prompt tuning; LoRA) | 70.49; 73.79 | Hit@1 | its authors | yes | 20240212 | [5] Table 3 |
| RoG, in GNN-RAG's table | 85.7 / 80.0 / 70.8 | Hit / H@1 / F1 | GNN-RAG authors | no (baseline) | 20240530 | [6] Table 2 |
| GNN-RAG+RA | 90.7 / 82.8 / 73.5 | Hit / H@1 / F1 | its authors | yes | 20240530 | [6] Table 2 |
| GCR, Llama-3.1-8B + ChatGPT | 92.6 / 73.2 | Hit / F1 | its authors | yes | 20241016 (ICML 2025) | [7] Table 1 |
| GCR, Llama-2-7B + GPT-4o, in OntGQA's table | 87.5 / 71.5 | Hit@1 / F1 | OntGQA authors | no (baseline) | 2026 | [9] Table 2 |
| OntGQA, Llama-2-7B | 91.5 / 77.1 | Hit@1 / F1 | its authors | yes | ACL 2026 (20260702-07) | [9] Table 2 |

Whether the baseline rows were re-run or copied: **unstated** in [3], [6] and [9]. A third-party audit lists RoG 85.7, GCR 92.2, ToG 82.6 and PoG 87.3 on WebQSP, "taken from the respective original papers"; it re-ran them only on its own set [8].

*Reading:* among these rows, the best F1 on the original test set is 73.5 (GNN-RAG+RA, 2024, first-party; STAGG 71.7 in 2016), and on the RoG split 77.1 (OntGQA, 2026). The best Hit is 92.6 (GCR, 2024), above OntGQA's 91.5 Hit@1, though the metric names and baselines differ. One system moves by 5.7 points with the metric (RoG, 85.7 against 80.0 [6]). A gap of a few points between papers is not a ranking.

## Known problems

- **No independent ranking.** Every row is first-party or a baseline inside another system's paper; the audit re-ran nothing on WebQSP [8].
- **Label noise.** An audit judged 52% of its sampled test items correct (dataset page, [8]). *Reading:* scores near 90 then measure agreement with the labels more than answer correctness; an inference, since the audit's rubric and the metrics differ.
- **Test sets differ.** ToG and GNN-RAG use the original test set; RoG, GCR and OntGQA use the RoG copy's 1,628 questions [3][6][9][10]. G-Retriever's Table 2 lists a size that does not match the RoG copy it follows [5]. *Reading:* each part of the RoG copy is smaller than the matching primary file by the empty-answer questions of that part (dataset page; my subtraction); its papers do not say whether that is the cause.
- **Exact match is strict.** In an audit example "AUD" is gold and "Australian dollar" fails [8].

## Used by

The systems in the tables: Think-on-Graph and Reasoning on Graphs ([papers](../papers/learned-graph-traversal.md)), G-Retriever ([papers](../papers/graph-based-rag.md)), GNN-RAG, GCR and OntGQA [3][4][5][6][7][9]. Trend: [Agentic graph retrieval](../trends/learned-graph-traversal.md).

## Sources

1. https://aclanthology.org/P16-2033.pdf : WebQSP paper (ACL 2016, Berlin, 7-12 August 2016): metrics, Table 1 (read 20261102 21:23 UTC)
2. https://download.microsoft.com/download/f/5/0/f5012144-a4fb-4084-897f-cfda99c60bdf/WebQSP.zip : `ReadMe.txt`, `doc/WebQSP.pdf`, `eval/eval.py` (downloaded 20261102 20:42 UTC)
3. https://arxiv.org/pdf/2307.07697 : Think-on-Graph, v6 of 24 March 2024 (ICLR 2024 version), Tables 1 and 9; first version 15 July 2023 per https://arxiv.org/abs/2307.07697 (read 20261102 21:24 UTC)
4. https://arxiv.org/pdf/2310.01061 : Reasoning on Graphs, v2 of 24 February 2024, Table 1, Table 6, metric definitions; first version 2 October 2023 (read 20261102 21:24 UTC)
5. https://arxiv.org/pdf/2402.07630 : G-Retriever, v3 of 27 May 2024, Tables 2 and 3, Appendix C; first version 12 February 2024 (read 20261102 21:24 UTC)
6. https://arxiv.org/pdf/2405.20139 : GNN-RAG, v1 of 30 May 2024 (the only version), Tables 2 and 7 (read 20261102 21:24 UTC)
7. https://arxiv.org/pdf/2410.13080 : Graph-constrained Reasoning, v2 of 28 May 2025, Table 1, Table 11, Hit definition; first version 16 October 2024; "Accepted by ICML 2025" per https://arxiv.org/abs/2410.13080 (read 20261102 21:24 UTC)
8. https://arxiv.org/pdf/2505.23495 : KG-RAG dataset audit v4 (3 November 2025), Tables 1 and 8, Section 3 and Appendix on cross-dataset evaluation (read 20261102 21:23 UTC)
9. https://aclanthology.org/2026.acl-long.489.pdf : OntGQA, ACL 2026 (2-7 July 2026), Tables 1 and 2 (read 20261102 21:25 UTC)
10. https://huggingface.co/api/datasets/rmanluo/RoG-webqsp : splits 2,826, 246 and 1,628 (read 20261102 20:44 UTC)
