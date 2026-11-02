---
type: dataset
kinds: [questions, corpus]
benchmark: multihop-rag
updated: 20261102 21:20 UTC
---

# MultiHop-RAG

MultiHop-RAG is a small English news corpus with 2,556 questions whose answers need evidence from two to four articles. This page answers what the data contains, how big it is, under which licence it is released and how it was made. The tasks, metrics and results are on [the benchmark page](../benchmarks/multihop-rag.md).

## What it contains

Two files, released together [4][5]:

- **A knowledge base of 609 English news articles**, each with title, author, source, publication date, category, URL and body. They come from 49 sources in six categories: sports 211, technology 172, entertainment 114, business 81, science 21, health 10 [2][7].
- **2,556 multi-hop questions ("queries")**, each with a short answer and a list of evidence passages [2][7]. The paper names four types [2]:

| Type | Count | What the answer needs |
|---|---|---|
| Comparison | 856 | comparing evidence across articles; typically yes or no |
| Inference | 816 | combining descriptions of one entity; the answer is that entity |
| Temporal | 583 | ordering events; yes, no, or "before"/"after" |
| Null | 301 | nothing: the corpus cannot answer; expected answer "insufficient information" |

Queries name the news outlet they draw on, so answering uses document metadata as well as text [2]. See [multi-hop question answering](../index/multi-hop-question-answering.md).

## Size and versions

| Measure | Paper (v1) | Released files, counted 20261102 |
|---|---|---|
| Articles; queries | 609 (average 2,046 tokens); 2,556 | 609; 2,556 [2][7] |
| Evidence list of 2 / 3 / 4 articles | 1,078 / 779 / 398 | 1,079 / 778 / 398 [2][7] |
| Publication dates | 26 Sep to 26 Dec 2023 | 20230926 to 20231225 [2][7] |

One query sits in a different evidence-count row in the paper and in the file; why is **unstated**. The paper has one arXiv version, submitted 20240127 [1]; the README says it was accepted at COLM 2024 [3]. The Hugging Face record was last modified 20240130 [5]; the code repository (last push 20260916) holds no data files [6]. Changes after 20240130 are **unstated**.

Signals, not verdicts: 353 citations (Semantic Scholar, read 20261102 20:01, carried over) [8]; 476 GitHub stars (20261102 20:42) [6]; 7,781 downloads on Hugging Face (20261102 20:41) [5].

## Licence

The README states "MultiHop-RAG is licensed under ODC-BY" and links ODC-By 1.0 [3]; the Hugging Face card says `license: odc-by` [4]. The repository has no `LICENSE` file: the GitHub API reports no licence and the file listing shows none [6]. The articles are third-party news text; the publishers' terms are **unstated** in the sources read.

## How it was made

1. Articles from the mediastack news API, published 26 September to 26 December 2023 (after the knowledge cut-off of widely used models), kept if at least 1,024 tokens [2].
2. A fact-or-opinion classifier extracted evidence sentences; only articles sharing keywords with others were kept [2].
3. GPT-4 paraphrased each sentence into a claim with a bridge entity and bridge topic; UniEval checked claim against evidence [2].
4. Groups of two to four claims sharing a bridge went to GPT-4, which wrote one query per type. Null queries use non-existent entities and fictional sources [2].
5. Quality control: a manual review of a sample and a GPT-4 check against four criteria [2].

## Used by

- Han et al., "RAG vs. GraphRAG", which evaluate on it (number of queries used: **unstated**) [9]; see the [papers group](../papers/graph-based-rag.md) and the trend [graph-based RAG](../trends/graph-based-rag.md).
- Multi-Meta-RAG, a method that filters on the source and date a query names [12].
- The corpus alone: [GraphRAG-Bench](../benchmarks/graphrag-bench-xiang.md) measured its entity graph [10]; this repository's [index-cost experiment](../../kb-kg/experiments/x2-index-cost/README.md) indexes 20 of its articles [13]; the Pinakes datasets benchmark ([Pinakes chapter](../applied-to-pinakes/README.md)) runs against it [11].

## Known problems

- **Generated, sampled for review.** GPT-4 wrote queries and answers; the authors reviewed "a subset sample" [2].
- **Narrow answers.** The authors limit answers to yes, no, entity names or "before"/"after", and evidence to four items [2]. In the file, 1,343 of 2,255 answerable queries (59.6%) are answered yes or no, there are 107 distinct answers, and one name accounts for 271 and another for 211 of the 816 inference queries (my count, 20261102 20:42) [7].
- **Null queries are worded differently.** "Letter" occurs in 144 of 301 null queries and 0 of 2,255 answerable ones; "Considering the information" in 184 null and 2 answerable (my count, 20261102 20:41) [7]. The Pinakes README reports the same wording difference and tests it on 18 tell-free questions [11]; what it means for abstention scores is on [the benchmark page](../benchmarks/multihop-rag.md).
- **Thin entity graph, like other public sets.** Xiang et al. report average entity degree 0.76 and average component size 2.70 for it; HotpotQA, MuSiQue and 2WikiMultihopQA score 0.60 to 0.65, UltraDomain 0.86, and their own GraphRAG-Bench novel corpus 2.27 [10].
- **Contamination** by later models is not ruled out: **unstated**. Publisher rights are unchecked (see Licence).

*Reading:* a small, useful set for cross-document retrieval; no source read reports an audit of its labels beyond the authors' sample.

## Sources

1. https://arxiv.org/abs/2401.15391 : single arXiv version, submitted 20240127 (read 20261102 20:41 UTC)
2. https://arxiv.org/html/2401.15391 : Tang and Yang, MultiHop-RAG, full text: construction, Tables 2 to 4, limitations (read 20261102 20:41 UTC)
3. https://raw.githubusercontent.com/yixuantt/MultiHop-RAG/main/README.md : ODC-BY statement, COLM 2024 (read 20261102 20:41 UTC)
4. https://huggingface.co/datasets/yixuantt/MultiHopRAG/raw/main/README.md : card, `license: odc-by`, two data files (read 20261102 20:41 UTC)
5. https://huggingface.co/api/datasets/yixuantt/MultiHopRAG : last modified 20240130, downloads, file list (read 20261102 20:41 UTC)
6. https://github.com/yixuantt/MultiHop-RAG : GitHub API (repository, contents, commits): no licence, no `LICENSE` file, last push 20260916, stars (read 20261102 20:42 UTC)
7. https://huggingface.co/datasets/yixuantt/MultiHopRAG/resolve/main/MultiHopRAG.json and corpus.json : my counts of the released files (read 20261102 20:41 UTC, counted 20:42)
8. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 353 for 2401.15391 (read 20261102 20:01 UTC, carried over from the research pool)
9. https://arxiv.org/html/2502.11371 : Han et al., RAG vs. GraphRAG, v3, datasets section (read 20261102 21:17 UTC)
10. https://arxiv.org/html/2506.05690 : Xiang et al., GraphRAG-Bench, v3, Table 9 and appendix text (read 20261102 21:17 UTC)
11. https://github.com/lucagattoni/pinakes-datasets-benchmark : README, public repository: abstention bullet, 18 tell-free questions (read 20261102 21:17 UTC)
12. https://arxiv.org/html/2406.13213 : Poliakov and Shvai, Multi-Meta-RAG, v2 (read 20261102 20:43 UTC)
13. https://huggingface.co/datasets/yixuantt/MultiHopRAG : the 20 articles of the corpus used by this repository's experiment (read 20261102 10:20 UTC, via the archive page kb-kg/experiments/x2-index-cost/README.md)
