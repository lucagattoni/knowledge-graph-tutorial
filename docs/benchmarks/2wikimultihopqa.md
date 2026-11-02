---
type: benchmark
datasets: [2wikimultihopqa]
updated: 20261102 21:30 UTC
---

# 2WikiMultiHopQA

2WikiMultiHopQA asks whether a system can answer a question that needs several paragraphs, and whether it can show the path it took. This page covers the evaluation: tasks, metrics, protocol and the results found. The data itself (size, licence, construction) is on [the dataset page](../datasets/2wikimultihopqa.md).

## What it tests

[Multi-hop question answering](../index/multi-hop-question-answering.md) with an explicit reasoning path. The authors built it because earlier sets gave no full explanation of how a question leads to its answer, and many HotpotQA examples do not need multi-hop reasoning [1]. Their check: a single-hop BERT model scores 64.6 F1 on [HotpotQA](hotpotqa.md) and 55.9 on this set, which they read as more examples needing multi-hop reasoning [1].

## Tasks, metrics and protocol

Three tasks, given a question and a set of documents [1]:

1. **Answer prediction**: a text span (or yes/no).
2. **Supporting facts**: the sentences used.
3. **Evidence generation**: the set of Wikidata-style triples describing the path.

Each is scored with exact match (EM) and F1. Joint scores combine all three; joint EM is 1 only when all three match exactly [1]. The board scores the test split (sizes on the dataset page); its answers are withheld, so authors send a prediction file to the dataset team [2]. A v1.1 script, with Wikidata aliases, replaced the first one on 20201208 [2].

Protocols differ, so rows do not compare. RAGSearch uses the full dev split and "Contain EM", which counts an answer correct if it appears in the output [4]. HippoRAG 2 uses 1,000 random queries and F1 [5].

## Datasets

One dataset: [2WikiMultiHopQA](../datasets/2wikimultihopqa.md). Its own problems (templates, few inference questions, sparse entity graph) are listed there.

## Results

The board in the dataset's repository is a hand-kept table; its newest dated row is 20230802 [2]. No other board was found in the sources read. Rows marked first-party are the system authors' own numbers.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Dataset baseline (HotpotQA model plus evidence module), first evaluation | answer 36.53 / 43.93; joint F1 5.41 | EM / F1, test | Dataset authors | yes | 20201025 | [1] Table 5; [2] |
| Same baseline, evaluation v1.1 | answer 40.08 / 46.29; joint F1 6.51 | EM / F1, test | Dataset authors | yes | after 20201208 (exact date unstated) | [3] |
| Human upper bound (100 test samples) | answer 91.00 / 91.79; joint F1 75.25 | EM / F1 | Dataset authors | yes | 202011 | [1] Table 7 |
| NA-Reviewer | answer 76.73 / 81.91; joint F1 65.23 | EM / F1, test | Authors of the linked paper (Fu, Wang, Zhou, Zhang); the board names no submitter | yes, by the link | board 20211029; paper 20211223 | [2]; [9] |
| Beam Retrieval | answer 88.47 / 90.87; supporting-fact F1 98.15 | EM / F1, blind test | Beam Retrieval authors | yes | 20230802 | [2]; [6] Table 5 |
| HippoRAG 2 vs NV-Embed-v2 vs BM25 vs no retrieval | 71.0 vs 61.5 vs 51.2 vs 42.8 | F1, 1,000 queries | HippoRAG 2 authors | yes | 20250619 (v2) | [5] Table 2 |
| Qwen2.5-7B single shot: dense vs best of five GraphRAG backends | 35.53 vs 62.56 | Contain EM, dev | Fan et al. (RAGSearch) | no | 20260401 | [4] Table 1 |
| GraphSearch agent: dense vs best GraphRAG | 47.43 vs 79.88 | same | same | no | 20260401 | [4] Table 1 |
| Search-o1 agent: dense vs best GraphRAG | 29.64 vs 65.56 | same | same | no | 20260401 | [4] Table 1 |
| Search-R1 vs Graph-R1 (trained agents) | 33.56 vs 66.25 | same | same | no | 20260401 | [4] Table 1 |

"No" for the RAGSearch rows: none of its four authors (Fan, Xue, Liu, Tan) is on the arXiv author list of the nine systems' papers (Search-o1, GraphSearch, Search-R1, Graph-R1, [GraphRAG](../index/graphrag.md), RAPTOR, HippoRAG 2, HyperGraphRAG, LinearRAG) [10]. Shared institutions were not checked.

*Reading:* the independent results agree in direction. Graph backends beat dense retrieval here by 27 to 36 points in RAGSearch, against gaps of -1 to +2 on the single-hop sets in single-shot mode [4]. The board's highest answer EM (Beam Retrieval, 2023) is first-party; no source read compares it with the 2026 LLM systems on one protocol. HippoRAG scores 71.8 here, above HippoRAG 2 at 71.0 [5].

## Known problems

- **Confounded comparison.** In RAGSearch the dense backend retrieves from a 2018 Wikipedia dump, while every GraphRAG backend uses each question's own context as its document, and the GraphRAG figure is the best of five variants against one dense baseline [4]. How much of the gap this explains is unstated in the paper.
- **Shortcuts.** On a "disconnected reasoning" test, which scores a model without real multi-hop reasoning, MuSiQue's authors got answer 63.4 on a 20K subset of this set against 37.8 on MuSiQue-Ans [7].
- **Board gaps.** The board leaves evidence and joint columns empty for some rows, and its baseline row is the first evaluation [2][3].
- **Setup sensitivity.** In LinearRAG issue 25 (opened 20260507, open when read), an outside user reports 2Wiki EM of 34.0 on the benchmark's original passages against 46.3 on the project's own chunks, both with `top_k_sentence` 5. A project collaborator replied on 20260518 that the project merged the original chunks and re-split them by fixed token length. The figures are the issue author's, not reproduced [8].

## Used by

[HippoRAG 2](../papers/graph-based-rag.md) [5]; [RAGSearch](ragsearch.md) [4]; [GraphRAG-Bench (Xiang)](graphrag-bench-xiang.md), for corpus statistics only [11]; trends [graph-based RAG](../trends/graph-based-rag.md) and [learned graph traversal](../trends/learned-graph-traversal.md) [4].

## Sources

1. https://arxiv.org/pdf/2011.01060 : paper v2: tasks, metrics, Tables 1, 4, 5, 7, single-hop check (read 20261102 20:41 UTC)
2. https://raw.githubusercontent.com/Alab-NII/2wikimultihop/main/README.md : leaderboard, submission guide, update of 20201208 (read 20261102 21:17 UTC)
3. https://raw.githubusercontent.com/Alab-NII/2wikimultihop/main/update_results/table_5.png : updated baseline table, read as an image (read 20261102 20:45 UTC)
4. https://arxiv.org/pdf/2604.09666 : RAGSearch v1 (20260401): Tables 1, 3, 6, Appendix A and B (read 20261102 20:41 UTC); authors and Section 5.1.2 system list re-read at https://arxiv.org/html/2604.09666 (read 20261102 21:19 UTC)
5. https://arxiv.org/pdf/2502.14802 : HippoRAG 2 v2 (20250619): setup and Table 2 (read 20261102 20:43 UTC)
6. https://arxiv.org/pdf/2308.08973 : Beam Retrieval v2, Table 5 (blind test set) (read 20261102 20:43 UTC)
7. https://arxiv.org/pdf/2108.00573 : MuSiQue paper v3, Table 4 (read 20261102 20:41 UTC)
8. https://github.com/DEEP-PolyU/LinearRAG/issues/25 : issue text, 8 comments, state open, last update 20260522; read through the GitHub API (read 20261102 21:17 to 21:21 UTC)
9. https://api.crossref.org/works/10.1049/ell2.12411 : record of "NA-Reviewer: Reviewing the context to improve the error accumulation issue for multi-hop QA", Electronics Letters, 20211223, four authors; abstract says it was tested on 2WikiMultiHopQA (read 20261102 21:21 UTC); the publisher page returned HTTP 403, so the paper text was not read
10. https://export.arxiv.org/api/query : author lists of arXiv 2501.05366, 2509.22009, 2503.09516, 2507.21892, 2404.16130, 2401.18059, 2502.14802, 2503.21322, 2510.10114, compared with the RAGSearch authors (read 20261102 21:20 UTC)
11. https://arxiv.org/pdf/2506.05690 : Xiang et al. v3, corpus-statistics table (read 20261102 20:43 UTC)
