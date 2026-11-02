---
type: benchmark
datasets: []
updated: 20261102 21:40 UTC
---

# GraphRAG-Bench (Xiao)

This page answers whether a graph improves the reasoning of a language model, not only its retrieval, on college-level computer-science textbook questions, according to Xiao et al. (arXiv 2506.02404) [1][2]. Its data is described here, as it is used only in its own protocol. A different benchmark has the same name: [GraphRAG-Bench (Xiang)](./graphrag-bench-xiang.md). They share one author (Xiao Huang), and the authors' lab site lists both; it calls this one "Education" [2][5].

## What it tests

The authors ask: "Does graph augmentation truly enhance reasoning capabilities beyond simple retrieval?" They argue that [HotpotQA](../datasets/hotpotqa.md), [2WikiMultiHopQA](../datasets/2wikimultihopqa.md) and [MuSiQue](../datasets/musique.md) ask short factoid questions that a model may know already [1]. So each question carries a gold rationale, and a method is scored on its reasoning as well as its answer [1].

## Tasks, metrics and protocol

- **Formats.** Fill-in-blank, multiple choice (4 options), multi-select (2 to 4 of 4), true or false, open-ended [1].
- **Accuracy.** Fill-in-blank and open-ended are scored by an LLM against the gold answer; multiple choice and true or false 1 or 0; multi-select 1, 0.5 or 0 [1]. The released evaluator calls gpt-4o; whether the paper's runs used it is **unstated** [3].
- **Reasoning.** R compares the produced rationale with the gold one; AR is the rationale score when the answer is right [1].
- **Pipeline.** Graph construction (time, tokens, share of non-isolated nodes), retrieval (indexing and retrieval time), generation, rationale [1].
- **Setup.** Nine [GraphRAG](../index/graphrag.md) methods plus three baselines (GPT-4o-mini alone, [TF-IDF](../index/tf-idf.md), [BM25](../index/bm25.md)); GPT-4o-mini everywhere, top-k 5 where used, 1,200-token chunks, other settings from each method's paper [1]. Graph-construction cost ranges from 10.1M tokens (RAPTOR) to 83.9M (LightRAG) [1].

## Datasets

- **Questions.** 1,018 across 16 topics [1]. The released files hold 105 fill-in-blank, 217 multiple-choice, 111 multi-select, 269 open-ended and 316 true-or-false (my count), with 31 distinct top-level topic labels, including case variants and a typo ("Meaching learning") [4].
- **Corpus.** 7 million words from 20 textbooks, parsed to markdown and structured JSON; 40 files, about 81 MB [1][4].
- **Construction.** From over 100 publications in 16 subfields the authors chose 20 textbooks; PDFs were parsed (PyMuPDF, OCR, LayoutLMv3, MinerU); domain experts screened the questions and wrote the rationales [1].
- **Licence.** No LICENSE file in the repository [3]. The data card says the data "can only be used for academic research" and "prohibited to distribute or modify" it. A read-only reference. The textbooks' own licences: **unstated** [4].
- **Versions.** Paper v1 20250603, v3 20250620. The code is in a personal-account repository that calls itself official; the lab site does not link it; last push 20250801. The data moved to the Awesome-GraphRAG organisation on Hugging Face (redirect seen 20261102) [2][3][4][5].

## Results

Average accuracy over the five formats, GPT-4o-mini base (Table 4), with average R and AR (Table 5). "First-party" means run by the method's own authors. All rows are the benchmark authors' runs of other groups' methods, so none is first-party; the official leaderboard repeats these 12 rows and has no later entries [1][5]. Date is that of paper v3, not of the run.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| RAPTOR | 73.58 (R 60.81, AR 45.53) | accuracy | benchmark authors | no | 20250620 | [1][5] |
| HippoRAG | 72.64 (60.90, 44.55) | same | same | no | same | [1][5] |
| GraphRAG (Microsoft) | 72.50 (59.43, 43.30) | same | same | no | same | [1][5] |
| GFM-RAG; KGP; ToG | 72.10; 71.86; 71.71 | same | same | no | same | [1][5] |
| TF-IDF; BM25 | 71.71 (57.61, 42.38); 71.66 (59.18, 44.15) | same | same | no (baselines) | same | [1][5] |
| LightRAG | 71.22 (60.46, 43.81) | same | same | no | same | [1][5] |
| GPT-4o-mini, no retrieval | 70.68 (55.45, 39.78) | same | same | no (baseline) | same | [1][5] |
| G-Retriever; DALK | 69.84 (60.17, 43.66); 69.30 (58.89, 42.12) | same | same | no | same | [1][5] |

Results by a method's own authors or by an independent group: **unstated**. The leaderboard's Date column (for example RAPTOR 2025-01-31) is not defined on the page.

*Reading:* the spread in accuracy is 4.3 points, with TF-IDF and BM25 inside it. Every method beats no retrieval on both rationale scores; DALK and G-Retriever fall below it on accuracy [1]. Five of nine graph methods exceed both plain retrievers, one ties TF-IDF, three fall below (my count from Table 4). The paper's "most" is a narrow majority.

## Known problems

- **One run, one generator.** Number of runs: **unstated**. The paper text read has no limitations section [1].
- **Maths.** The authors find all GraphRAG methods lower accuracy on mathematics; some questions need computation or code, which graph retrieval does not supply [1].
- **Uneven topics.** One label holds 112 questions (Cybersecurity), the ethics label 4 (my count) [4].

## Used by

[Graph-based RAG](../trends/graph-based-rag.md) comparisons; it scores [Microsoft GraphRAG](../projects/microsoft-graphrag.md), [LightRAG](../projects/lightrag.md) and [HippoRAG](../projects/hipporag.md). The [group page](../papers/graph-based-rag.md) lists the paper under further reading; it has 36 citations (Semantic Scholar) [7]. WildGraphBench cites it as a GraphRAG benchmark, but its graph analysis of "GraphRAG-Bench" names a Novel subset, which belongs to the other benchmark [6]. A third-party use with scores: **unstated**.

## Sources

1. https://arxiv.org/html/2506.02404 : full text: questions, corpus, metrics, setup, Tables 2 to 5 (read 20261102 20:57 UTC; Tables 4 and 5 re-read 20261102 21:32 UTC)
2. https://arxiv.org/abs/2506.02404 : authors (8), versions v1 20250603, v2 20250611, v3 20250620 (read 20261102 20:57 UTC)
3. https://github.com/jeremycp3/GraphRAG-Bench : README ("official repo"), file list without LICENSE, licence null, created 20250610, last push 20250801; `evaluator.py` calls gpt-4o (read 20261102 21:05 UTC; README and licence field re-read 20261102 21:28 UTC)
4. https://huggingface.co/datasets/Awesome-GraphRAG/GraphRAG-Bench : card with licence text, last modified 20250801, file list; question files counted; the older address redirects here (read 20261102 21:03 UTC)
5. https://deep-polyu.github.io/RAG/ : official leaderboard, 12 rows, lab site naming both benchmarks and linking the DEEP-PolyU organisation, not the personal repository (read 20261102 21:27 UTC)
6. https://arxiv.org/html/2602.02053 : WildGraphBench, related work and Section 4.3 with Table 4 (read 20261102 21:27 UTC)
7. https://api.semanticscholar.org/graph/v1/paper/batch?fields=citationCount (id arXiv:2506.02404) : 36 citations (read 20261102 20:01 UTC in this documentation's research pass; carried over, not re-queried; no archive page holds the count)
