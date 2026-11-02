---
type: benchmark
datasets: [natural-questions, popqa, triviaqa, hotpotqa, 2wikimultihopqa, musique]
updated: 20261102 21:25 UTC
---

# RAGSearch

RAGSearch asks one question: once a model can search in several rounds, does it still need an offline-built graph? It compares plain dense retrieval with five [GraphRAG](../index/graphrag.md) backends under single-shot, training-free and reinforcement-learned search. It has no data of its own; it re-uses six public question sets.

## What it tests

Whether "agentic search" (multi-round retrieval chosen by the model) can replace the explicit graph structure of GraphRAG [1]. The paper's answer: agentic search narrows the gap, "particularly in RL-based settings", but GraphRAG stays ahead on complex multi-hop questions [1]. Authors: Fan, Xue, Liu and Tan (New York University Shanghai); arXiv v1 20260401, the only version at read time [1][2]. The venue is **unstated**: the page still carries unfilled template text [2].

## Tasks, metrics and protocol

- **Backends:** one dense retriever (over the 2018 Wikipedia dump) and five graph backends: GraphRAG, RAPTOR, HippoRAG2, HyperGraphRAG, LinearRAG. Graphs are built with GPT-4o-mini, top-5 retrieval [2].
- **Inference modes:** single-shot; training-free agents (Search-o1, GraphSearch) on Qwen2.5-7B and 32B; RL agents (Search-R1, Graph-R1) trained with GRPO on Qwen2.5-3B and 7B, 5,000 samples from the HotpotQA and NQ training sets [2].
- **Metrics:** Contain Exact Match (the gold answer appears in the output) and F1. Offline construction time and cost are reported on NQ only [2].
- **Data:** full test or dev sets, taken from the FlashRAG toolkit [2].

## Datasets

[Natural Questions](../datasets/natural-questions.md), [PopQA](../datasets/popqa.md) and [TriviaQA](../datasets/triviaqa.md) are run on their test sets; [HotpotQA](../datasets/hotpotqa.md), [2WikiMultiHopQA](../datasets/2wikimultihopqa.md) and [MuSiQue](../datasets/musique.md) on their dev sets, in full [2]. Question counts and cut details are on the dataset pages. GraphRAG indexes are built from each question's own context passages, not from Wikipedia [2].

## Results

Contain EM, Qwen2.5-7B, from the paper's Table 1, re-read 20261102. "Best GraphRAG" is the best of five variants per cell [2]. All rows: run by the benchmark authors, first-party for the benchmark, not for the methods; date 20260401; source [2].

| System | HotpotQA | 2Wiki | MuSiQue |
|---|---|---|---|
| Single-shot, dense | 19.00 | 35.53 | 20.99 |
| Single-shot, best GraphRAG | 46.70 | 62.56 | 47.95 |
| Search-o1, dense | 33.76 | 29.64 | 12.62 |
| Search-o1, best GraphRAG | 42.75 | 65.56 | 32.44 |
| GraphSearch, dense | 38.22 | 47.43 | 13.33 |
| GraphSearch, best GraphRAG | 58.64 | 79.88 | 55.26 |
| Search-R1 | 35.76 | 33.56 | 14.42 |
| Graph-R1 | 53.42 | 66.25 | 40.82 |

On NQ, PopQA and TriviaQA, single-shot dense scores 46.62, 32.14 and 58.60; best GraphRAG 48.31, 32.82 and 57.65 [2]. The paper reports a multi-hop gain of +27.23 (average of 27.70, 27.03, 26.96) and +0.47 on general QA [2]. Offline cost per one million tokens on NQ: LinearRAG 0.68 h and $0; HippoRAG2 1.19 h and $2.85; HyperGraphRAG 1.37 h and $3.93; RAPTOR 1.70 h and $6.38; GraphRAG 1.72 h and $13.19 [2].

*Reading:* the single-shot gap is real in the table but its size is not a clean measure of graph structure (see below). Only the paper reports these numbers; no independent replication in the sources read [5].

## Known problems

- **Different knowledge sources.** The dense backend retrieves from the 2018 Wikipedia dump; the graph backends index each question's own context [2]. How much of the gap this explains is **unstated** in the paper.
- **Best of five against one baseline.** The headline gap compares the best graph variant per cell with a single dense baseline [2].
- **The narrowing is not visible for one agent.** From Table 1, GraphSearch's multi-hop gap averages 31.60 points (20.42, 32.45, 41.93), wider than the single-shot 27.23; the paper's 26.59 is the mean over GraphSearch and Search-o1 (21.58) [2]. This is my arithmetic on the table.
- **Search-R1 against Graph-R1 are different agents,** not one agent with two backends [2].
- **No licence** in the repository (GitHub API, null); it holds install steps, offline-construction and quick-start commands and four vendored folders, and no leaderboard, though the paper says leaderboards are released [3][4]. Treat it as a read-only reference.

## Used by

The paper has 1 citation (Semantic Scholar, read 20261102 20:01 UTC) [6]. It scores [Microsoft GraphRAG](../projects/microsoft-graphrag.md) and [HippoRAG](../projects/hipporag.md), plus [RAPTOR](https://github.com/parthsarthi03/raptor), [LinearRAG](https://github.com/DEEP-PolyU/LinearRAG), [Graph-R1](https://github.com/LHRLAB/Graph-R1) (also the HyperGraphRAG code), [Search-R1](https://github.com/PeterGriffinJin/Search-R1), [Search-o1](https://github.com/RUC-NLPIR/Search-o1) and [GraphSearch](https://github.com/DataArcTech/GraphSearch) [2]. The two 2026 scaling studies read, which test graph against plain retrieval, do not cite it [5]; see the [group page](../papers/graph-based-rag.md) for the papers. Trends: [agentic search](../trends/agentic-search.md), [graph-based RAG](../trends/graph-based-rag.md), [learned graph traversal](../trends/learned-graph-traversal.md). Terms: [reinforcement learning](../index/reinforcement-learning.md), [multi-hop question answering](../index/multi-hop-question-answering.md), [vector search](../index/vector-search.md).

## Sources

1. https://arxiv.org/abs/2604.09666 : Fan, Xue, Liu, Tan, abstract, authors, version history (read 20261102 20:59 UTC)
2. https://arxiv.org/html/2604.09666 : full text v1: setup, Table 1, Appendices A, B, C, E (read 20261102 20:59 UTC)
3. https://raw.githubusercontent.com/FanDongzhe123/RAGSearch/main/README.md and https://api.github.com/repos/FanDongzhe123/RAGSearch : install steps, offline construction and quick-start commands; no leaderboard; licence null; last push 20260825 (read 20261102 21:24 UTC); folder listing (read 20261102 21:01 UTC)
4. The paper's introduction (source 2) : "All code, configurations, and leaderboards are released" (read 20261102 20:59 UTC)
5. https://arxiv.org/html/2607.26497 and https://arxiv.org/html/2606.25656 : searched for "RAGSearch" and its arXiv id, no match in either (read 20261102 21:02 UTC)
6. https://api.semanticscholar.org/graph/v1/paper/batch : citationCount 1 for arXiv:2604.09666 (read 20261102 20:01 UTC)
