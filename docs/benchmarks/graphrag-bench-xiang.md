---
type: benchmark
datasets: []
updated: 20261102 21:38 UTC
---

# GraphRAG-Bench (Xiang)

This page answers when a graph helps [retrieval-augmented generation](../index/retrieval-augmented-generation.md) and at which stage of a [GraphRAG](../index/graphrag.md) pipeline, according to Xiang et al. (ICLR 2026) [1][3]. Its data is described here, as it is used only in its own protocol. A different benchmark has the same name: [GraphRAG-Bench (Xiao)](./graphrag-bench-xiao.md).

## What it tests

Whether graph structure improves RAG, for which kind of question, and in which stage: graph construction, retrieval or generation. The authors start from reports that GraphRAG "frequently underperforms vanilla RAG on many real-world tasks" [1].

## Tasks, metrics and protocol

Four levels: fact retrieval, complex reasoning, contextual summarise, creative generation. Accuracy scores every level; ROUGE-L, coverage and faithfulness score some. Retrieval and graph structure are scored too. The main table uses a GPT-4o-mini generator, two plain-RAG baselines and seven GraphRAG frameworks [1].

## Datasets

- **Corpora.** Medical: NCCN clinical guidelines. Novel: pre-20th-century Project Gutenberg novels, lesser-known works chosen to limit training-data overlap [1].
- **Questions.** The paper counts 4,076; the released files hold 4,072 (my count) [1][5].
- **Size.** Full Novel corpus about 1,132k tokens; Medical tokens **unstated** [1].
- **Graph density** (average degree, Table 9). Novel 2.27, Medical 1.05, against 0.86 for [UltraDomain](../datasets/ultradomain.md), 0.76 [MultiHop-RAG](../datasets/multihop-rag.md), 0.65 [HotpotQA](../datasets/hotpotqa.md), 0.64 [2WikiMultiHopQA](../datasets/2wikimultihopqa.md), 0.60 [MuSiQue](../datasets/musique.md) [1]. This page is the home of these figures.
- **Construction.** Mine an [ontology](../index/ontology.md) with GPT-4.1, collect evidence as subgraphs and chains, generate questions from them, filter by models and human checks, refine with GPT-4.1; ontologies and questions inherit its view (my reading) [1].
- **Licence.** Repository: MIT. The data card has no licence field. NCCN and Gutenberg terms: **unstated** [4][5].
- **Versions.** Paper v1 20250606, v3 20260222; data modified 20250713; code pushed 20260607 [2][4][5].

## Results

Re-read 20261102. Scores are accuracy at levels 1 / 2 / 3 / 4. "First-party" means run by the method's own authors. Date is the source's (paper version or leaderboard column), not the run's; run dates are **unstated**.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| RAG with rerank | Novel 60.92 / 42.93 / 51.30 / 38.26; Medical 64.73 / 58.64 / 65.75 / 60.61 | accuracy per level, GPT-4o-mini generator | benchmark authors | no | 20260222 | [1] |
| HippoRAG 2 | Novel 60.14 / 53.38 / 64.10 / 48.28; Medical 66.28 / 61.98 / 63.08 / 68.05 | same | benchmark authors | no | 20260222 | [1] |
| LightRAG | Novel 58.62 / 49.07 / 48.85 / 23.80; Medical 63.32 / 61.32 / 63.14 / 67.91 | same | benchmark authors | no | 20260222 | [1] |
| MS-GraphRAG local | Novel 49.29 / 50.93 / 64.40 / 39.10; Medical 38.63 / 47.04 / 41.87 / 53.11 | same | benchmark authors | no | 20260222 | [1] |
| HippoRAG 2; LightRAG, Medical | 72.4 / 68.4 / 65.0 / 56.9; 26.2 / 20.2 / 22.6 / 14.4 | answer correctness, GPT-4o-mini generator, 7B index model, gemini-3-flash judge | RAGU authors | no (independent) | 20260713 | [7] |
| KnowCosmos; GraphRAG-SDK | Novel 70.34; 66.09. Medical 80.15; 76.87 | leaderboard average | submitters, unnamed | yes, inferred from each row's link | 2025.09; 2026.08 | [6] |

The leaderboard has 21 rows per corpus, last changed 20261027, and its Date does not follow the commits: GraphRAG-SDK shows 2026.08 and was added 20261008 [6].

*Reading:* the sign of the graph effect depends on corpus, level and method. On Novel, HippoRAG 2 beats RAG at levels 2, 3 and 4 (53.38 against 42.93 at level 2) and trails it by 0.78 at level 1. On Medical, HippoRAG 2 and LightRAG lead RAG at levels 2 and 4, RAG leads at level 3 (65.75 against 63.08 and 63.14), and only HippoRAG 2 leads at level 1 (66.28 against 64.73). LightRAG trails RAG on Novel at levels 3 and 4; MS-GraphRAG local trails it at every Medical level [1]. The independent run puts LightRAG at 26.2 on Medical level 1 against the authors' 63.32: scores do not transfer between pipelines [1][7].

## Known problems

- **Scalability table.** Its Small-tier RAG row is the Medical row of the main table, not the Novel row. The claim that RAG falls from 58.64 to 43.20 depends on it; with the Novel figure, level 2 goes 42.93 to 43.20 (my reading). The main table's HippoRAG 2 Novel row equals the Small row, so its corpus size is **unstated** [1].
- **Density by design.** The paper aims for "richer and more structured entity-relation graphs than existing datasets" (Appendix E), which favours graph methods (my reading). WildGraphBench measures a "GraphRAG-Bench" corpus (1.1M tokens) as sparse under the LightRAG pipeline. Its related work cites the Xiao paper for that name, yet the Novel subset it describes is this page's; I identify it by subset name and size, an inference [1][10].
- **Leaderboard.** The Average column equals the mean of the four accuracy columns (to 0.01) for 37 of 42 rows; for example Medical LightRAG shows 62.59 against 63.92 (my arithmetic). What the Date column means and how many runs were made: **unstated** [6].
- **Scope.** The authors state the framework "operates exclusively within unimodal (text-based) contexts" (Appendix J) [1].

## Used by

[Graph-based RAG](../trends/graph-based-rag.md) comparisons; the paper has a section in [the group page](../papers/graph-based-rag.md) and 60 citations (Semantic Scholar) [11]. It scores [Microsoft GraphRAG](../projects/microsoft-graphrag.md), [LightRAG](../projects/lightrag.md) and [HippoRAG](../projects/hipporag.md); [GraphRAG-SDK](../projects/graphrag-sdk.md) submitted a row [6]. Later: MOSAIC (76.97 Medical, 64.33 Novel, query-weighted) [8], RAGU [7], NexusRAG, HyCE-RAG and RLM-on-KG [9]. WildGraphBench cites it [10].

## Sources

1. https://arxiv.org/html/2506.05690v3 : full text: tasks, metrics, Tables 2, 9 and 12, Appendices C, E, G.5 and J (read 20261102 21:27 UTC)
2. https://arxiv.org/abs/2506.05690 : authors (7), versions v1 20250606, v2 20251007, v3 20260222 (read 20261102 20:57 UTC)
3. https://arxiv.org/pdf/2506.05690v3 : header "Published as a conference paper at ICLR 2026" (read 20261102 21:05 UTC)
4. https://github.com/GraphRAG-Bench/GraphRAG-Benchmark : MIT LICENSE, README, last push 20260607 (read 20261102 20:59 UTC)
5. https://huggingface.co/datasets/GraphRAG-Bench/GraphRAG-Bench : card, last modified 20250713; question files counted (read 20261102 20:59 UTC)
6. https://graphrag-bench.github.io/story_data.csv and https://graphrag-bench.github.io/medical_data.csv : leaderboard rows, links and Average arithmetic (read 20261102 21:27 UTC); commit dates via the GitHub API for the repository GraphRAG-Bench/graphrag-bench.github.io (read 20261102 21:30 UTC)
7. https://arxiv.org/html/2607.11683 : RAGU, Table 1 and setup; submitted 20260713 (read 20261102 21:29 UTC)
8. https://arxiv.org/abs/2609.11065 : MOSAIC abstract, 76.97 and 64.33 (read 20261102 21:30 UTC)
9. http://export.arxiv.org/api/query?search_query=all:%22GraphRAG-Bench%22 : abstracts of 2609.37661, 2607.22597 and 2604.17056 (read 20261102 21:02 UTC)
10. https://arxiv.org/html/2602.02053 : WildGraphBench, related work and Section 4.3 with Table 4 (read 20261102 21:27 UTC)
11. https://api.semanticscholar.org/graph/v1/paper/batch?fields=citationCount (id arXiv:2506.05690) : 60 citations (read 20261102 20:01 UTC in this documentation's research pass; carried over, not re-queried; no archive page holds the count)
