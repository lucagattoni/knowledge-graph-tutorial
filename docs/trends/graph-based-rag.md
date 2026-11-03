---
type: trend
shift: eager LLM-built graphs -> cheaper, lazier ones
status: steady
order: 1
updated: 20261102 23:27 UTC
---

# Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones

This page answers how a graph built by a [large language model](../index/large-language-model.md) (LLM) became the index of [retrieval-augmented generation](../index/retrieval-augmented-generation.md) (RAG), which answers questions over a document collection, why building it was costly, and how builders are cutting that cost. It names the projects, says who measured what, and gives a labelled reading. Most cost figures come from the authors of the method; the independent tests are fewer and less favourable.

> **Distinctive because** a model reads the corpus once, at index time, and the graph it extracts becomes the retrieval index [13][14]. The nearest neighbour is [building knowledge graphs with LLMs](./llm-kg-construction.md): same extraction step, but there the graph is the product, here a means judged by answer quality and cost.

## Why it emerged

The starting point is [retrieval-augmented generation](../index/retrieval-augmented-generation.md) in its common form: split documents into [chunks](../index/chunking.md), embed them, return the nearest ones ([how that era came about](../history/language-models-meet-retrieval.md)). In 2024 three papers named its limits. The GraphRAG authors wrote that RAG "fails on global questions directed at an entire text corpus" [13]. The LightRAG authors named "reliance on flat data representations" [14]. The HippoRAG authors said models with RAG still struggle to integrate many new experiences, and tested multi-hop question answering [15]. All three answered by having a [large language model](../index/large-language-model.md) build a graph at index time: "an LLM to build a graph index in two stages" [13].

That created a bill. Microsoft's documentation estimates that graph extraction is "roughly 75% of indexing cost" [3], and the README warns that indexing "can be an expensive operation" [1]. The LinearRAG authors call relation extraction "unstable and costly" [26], and the LogicRAG authors say the graph-building step brings "overwhelming token cost and update latency" [32]. An independent study then found plain RAG level or ahead on single-hop, fact-centred questions [20], and the GraphRAG-Bench authors cite reports that GraphRAG "frequently underperforms vanilla RAG on many real-world tasks" [19]; that sentence is their background, not a result of their own. So from 2025 the work turned to cheaper graphs.

*Reading:* the shift answers a bill, not a new idea. No source read says cost alone caused it.

## Why it matters

It is the main route by which [knowledge-graph](../index/knowledge-graph.md) ideas returned to retrieval after RAG; the long background is in [chapter 1](../history/README.md). The cost decides who can use it: a corpus that changes must be re-indexed, which is why LightRAG advertises an incremental update algorithm [14]. Its techniques also feed [agent memory](./agent-memory.md): the second HippoRAG paper is titled "From RAG to Memory" [16]. [Reasoning over a document tree](./reasoning-over-structure.md) is the competing answer to the same weakness of similarity search.

## How it works

1. A model reads each chunk and extracts entities and relations; duplicates are merged and described.
2. Optionally the graph is split into communities, each with a model-written [community report](../index/community-report.md) [13].
3. At query time, local search follows an entity's neighbourhood; global search turns each community summary into a partial answer and merges them [13]; HippoRAG instead runs [Personalized PageRank](../index/personalized-pagerank.md) from the query's entities [15].

Standard [GraphRAG](../index/graphrag.md) uses a model for entity extraction, relationship extraction, entity summarization and community reports [3]. The shift is the set of ways to use the model less:

| Lever | What changes | Example and who measured |
|---|---|---|
| Lighter graph, fewer steps | No community reports; graph plus vector retrieval, incremental update [14] | LightRAG, authors' claims only [14] |
| Model on key chunks only | A small LLM skeleton plus a keyword graph from all chunks [28] | KET-RAG: "over an order of magnitude" lower indexing cost than Microsoft's GraphRAG at comparable retrieval quality, authors [28] |
| Non-LLM extraction | Noun phrases and co-occurrence in GraphRAG's Fast method [3]; relation-free graph from light entity extraction [26]; co-occurrence of entities found by [named-entity recognition](../index/named-entity-recognition.md) (NER) [25] | LinearRAG: "no extra token consumption", authors [26] |
| Zero-token graph | Edge weights from vector geometry [22] | G3RAG, authors [22] |
| Defer to query time | No up-front summaries; LLM used when a question arrives [4]; reasoning structure built per query [32] | LazyGraphRAG, Microsoft [4]; LogicRAG, authors [32] |
| Graph as locator | The graph finds passages; answers use the original text [23] | EffiRAG, authors [23] |

*Reading:* every row moves model calls from index time to query time or removes them. The archive's survey sorts the projects by five levers (cheaper models, fewer calls per chunk, work moved to query time, no model at index time, structure taken from the text by non-generative tools); they overlap with these rows but are grouped differently. It finds almost all cost figures to be the authors' own [35].

### Cheaper or lazy construction

This is the destination of the shift, not a trend of its own: the artefact is still a graph used as an index, built differently. The lever also recurs outside this family, in [code graphs](./code-knowledge-graphs.md), where a parser and not a model builds the graph, and in plain files, so it is a property more than a family. In papers it is rising: 31 results against 13 for "GraphRAG" wording together with cost wording (read 20261102 20:19) [12]. In maintained code it is thin. Microsoft's open-source methods page lists only Standard and Fast [3]; LazyGraphRAG exists as a blog and a product preview (editor's note of 20250606) [4]. The cheap-graph repositories (nano-graphrag, fast-graphrag, MiniRAG [27], LinearRAG [26]) show no push in 90 days at the snapshot [11].

### Multimodal graph RAG

RAG-Anything treats images, tables and equations as entities in the same graph [18]; its README badge says "Based on LightRAG" [7]. LightRAG's news lists "[2026.05] Merge RagAnything into LightRAG" and says v1.5 integrates multimodal processing into its pipeline [6]. It is part of this family because the graph index and the extraction step are the same; only node types and the parser differ, and the flagship absorbed it. RAG-Anything stays active (v1.4.4, 20261028) [5]. Papers: 19 results against 6 [12], for example MegaRAG [34].

### Hypergraph variants

HyperGraphRAG stores n-ary facts as hyperedges [31]. The build is the same eager extraction with a richer edge, so it stays here (31 results against 11 for "hypergraph" with RAG wording [12]). Variants that train a model to walk the graph belong to [agentic graph retrieval](./learned-graph-traversal.md).

## Representative projects

| Project | Licence (LICENSE file) | Stars, 20261030 19:54 UTC [11] | Latest release read [5] |
|---|---|---|---|
| [Microsoft GraphRAG](../projects/microsoft-graphrag.md) | MIT | 36,498 | v3.3.0, 20261008; README: "largely in maintenance mode" [1] |
| [LightRAG](../projects/lightrag.md) | MIT | 40,443 | v1.5.7, 20260902 |
| [HippoRAG](../projects/hipporag.md) | MIT | 4,083 | v1.0.0, 20250227; last push 20261006 |
| [RAG-Anything](../projects/rag-anything.md) | MIT | 24,322 | v1.4.4, 20261028 |
| [GraphRAG SDK](../projects/graphrag-sdk.md) (FalkorDB) | Apache-2.0 | 1,029 | v1.6.0, 20261102 |
| [neo4j-graphrag](../projects/neo4j-graphrag-python.md) | Apache-2.0, parts under the Python Software Foundation licence (PSF-2.0) | 1,326 | 1.23.0, 20261028 |

Stars are a signal, not a verdict. The catalogue records that the trends researcher hand-tagged 20 active repositories in this family in the snapshot [36]; the tagged list is not in the snapshot or in a data file, so the count cannot be re-derived here and its completeness is unstated. HippoRAG's README claims "significantly fewer resources for offline indexing" than GraphRAG, RAPTOR and LightRAG (first-party) [9]. Neo4j calls its package first-party and keeps the graph builder in an `experimental` namespace [10]. Quiet research code, told through papers: [KAG](https://github.com/OpenSPG/KAG), [nano-graphrag](https://github.com/gusye1234/nano-graphrag), [fast-graphrag](https://github.com/circlemind-ai/fast-graphrag), [MiniRAG](https://github.com/HKUDS/MiniRAG), [LinearRAG](https://github.com/DEEP-PolyU/LinearRAG) [11]. LinearRAG and LogicRAG are GPL-3.0 [38]; they are read-only references here, ideas and published results only, no code.

## Fundamental papers

Group page: [papers on graph-based RAG](../papers/graph-based-rag.md). The page cites: GraphRAG (2024), the origin of the community-summary design [13]; LightRAG (2024) [14]; HippoRAG (2024) and HippoRAG 2 (2025) [15][16]; KAG (2024) [17]; KET-RAG (2025) and LinearRAG (2025) for cost [28][26]; GraphRAG-Bench (2025) and Han et al. (2025) as evaluations [19][20]. The papers chapter keeps ten papers on graph-based RAG as fundamental, among them GraphRAG, LightRAG, HippoRAG, HippoRAG 2, LinearRAG, GraphRAG-Bench and Han et al.; KAG, KET-RAG and the others named here are in its further reading.

## What is measured, and by whom

Experiments in this documentation: [X2](../experiments/x2-index-cost.md) counts calls and tokens of four builders per document, with a local model so far; [X3](../experiments/x3-matched-cost-comparison.md) proposes a matched-cost comparison and has not run. The benchmarks are GraphRAG-Bench, [HotpotQA](../datasets/hotpotqa.md), [MuSiQue](../datasets/musique.md), [MultiHop-RAG](../datasets/multihop-rag.md) and [Natural Questions](../datasets/natural-questions.md).

| Study | Who ran it | Finding | First-party? |
|---|---|---|---|
| GraphRAG docs | Microsoft | Extraction about 75% of indexing cost; method not given [3] | yes |
| LazyGraphRAG blog | Microsoft Research | Index cost "identical to vector RAG and 0.1% of the costs of full GraphRAG"; more than 700 times lower global query cost [4] | yes |
| KET-RAG, EffiRAG | their authors | Lower cost; EffiRAG preferred on 93 of 120 questions against LightRAG-hybrid, 7 for LightRAG, 20 splits; USD 0.952 to 0.408 [28][23] | yes |
| Han et al., one protocol, graphs built with GPT-4o-mini by default (Section 3.4) | university and industry authors | Generator Llama 3.1 8B, the main-paper default. [Natural Questions](../datasets/natural-questions.md) (NQ) F1 (a score that balances precision and recall of answer words): RAG 64.78, Community-Local 63.01. [HotpotQA](../datasets/hotpotqa.md) F1: RAG 60.04, HippoRAG2 63.01. [MultiHop-RAG](../datasets/multihop-rag.md) accuracy (Table 2): RAG 67.02, Community-Local 69.01, HippoRAG2 70.27. Build time on MultiHop-RAG (Table 4): RAG 135 s, KG-GraphRAG (the plain knowledge-graph, KG, variant) 7,702 s, Community-GraphRAG 5,560 s [20] | no |
| GraphRAG-Bench leaderboard, as compiled in FalkorDB's README [8]; the leaderboard itself is described in [19] | FalkorDB computed the Overall column; the competitor per-dataset scores are, it says, copied unchanged from the leaderboard, whose own runners are unstated | Overall, FalkorDB's average of the Novel and Medical scores: HippoRAG2 60.67, reranked vector RAG 55.39, LightRAG 53.84, MS-GraphRAG local 48.05; FalkorDB's own SDK 71.48, run August 2026. The leaderboard ranks each dataset separately [8] | yes, the whole row |
| Scaling study, abstract only | Wang et al. | [BM25](../index/bm25.md) overtakes the file-system agent near 10 million corpus tokens and leads at every larger shared tier; scalable graph variants stay below BM25 at shared tiers; graph RAG "encounters construction walls before deployment scale" [21] | no |
| [RAGSearch](../benchmarks/ragsearch.md) | Fan et al. | Agentic search narrows the gap to GraphRAG; GraphRAG still helps on complex multi-hop [29] | no |

Han et al. find the graph methods ahead on multi-hop sets and plain RAG ahead on single-hop ones; in the plain KG variant only about 65.8% (HotpotQA) and 65.5% (NQ) of answer entities were in the graph [20]. Graph-quality dependence is shown by their Llama 3.1 70B run of Community-Local on MultiHop-RAG (Table 5): 65.77 with no graph, 71.17 with a GPT-4o-mini graph, 75.08 with a GPT-4o graph [20]. The GraphRAG-Bench authors open by citing reports that GraphRAG "frequently underperforms vanilla RAG on many real-world tasks"; that is their motivation, and the abstract gives no result of their own [19]. A plain raw-history baseline ranked first in six of seven settings among compared memory systems, but on conversation memory, not documents [24]. No source read compares the cheap routes at matched cost on one corpus.

## Assessment

*Reading:* **Strengths.** On multi-hop and corpus-wide questions the graph pays in the independent comparison [20], and the design ideas (communities, Personalized PageRank) are reusable. **Weaknesses.** Index cost scales with the corpus; extraction quality caps accuracy [20]; the plain baseline is hard to beat on single-hop questions [20]; better retrieval does not always give better answers [30]; build walls appear at scale [21]. Rankings can also turn on answer format: the RAGU authors call HippoRAG2's multi-hop lead "largely an answer-format artifact" (their own system competes) [33]. The cheaper graphs rest mostly on their authors' tests, and the archive notes that a zero-token graph still used a model to filter seeds [37]. **Direction.** The Microsoft flagship is in maintenance mode while LightRAG ships and vendors package the idea [1][5]; research keeps moving: 255 results against 148 for GraphRAG wording (x1.72), above the RAG-wording control (3,357 against 2,736, x1.23), both from one arXiv API run read 20261102 20:31 UTC, and below the LLM-agent control of x2.50, which is the trends researcher's earlier figure with its query unrecorded [12][36]. The catalogue gives 272 against 167 (x1.63) for the family from that earlier run. The runs differ in query wording, category scope and read time, so the counts differ; all put the family at about x1.6 to x1.7 against a RAG control near x1.2 (details in Source 12). Keyword counts are noisy. Hence "steady".

## Signals to watch

- A Microsoft GraphRAG release containing a LazyGraphRAG query engine, or a change to the maintenance notice of 20260814 [2][3].
- A LightRAG release after v1.5.7 [5].
- An independent evaluation of LinearRAG, MiniRAG or KET-RAG, or a replication of EffiRAG or G3RAG [22][23].
- Results of X2 pass B and X3 once approved.
- Whether more vendors move their packages to maintenance, as Microsoft did.

## Sources

1. https://github.com/microsoft/graphrag : README maintenance warning, expensive-indexing warning (read 20261102 20:10 UTC)
2. https://github.com/microsoft/graphrag/commits/main/README.md : commit 21f7bdf "Add notice. (#2486)", 20260814 15:08 UTC (read 20261102 20:11 UTC)
3. https://microsoft.github.io/graphrag/index/methods/ : Standard and Fast methods; "roughly 75% of indexing cost" (read 20261102 20:11 UTC)
4. https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ : LazyGraphRAG, 0.1%, 700 times, editor's note 20250606 (read 20261102 20:11 UTC)
5. GitHub API for microsoft/graphrag, HKUDS/LightRAG, OSU-NLP-Group/HippoRAG, HKUDS/RAG-Anything, FalkorDB/GraphRAG-SDK, neo4j/neo4j-graphrag-python: LICENSE files, latest releases, pushes (read 20261102 20:10 UTC; the latest-release call was run again on all six 20261102 22:52 UTC with the same tags: v3.3.0, v1.5.7, v1.0.0, v1.4.4, v1.6.0, 1.23.0)
6. https://github.com/HKUDS/LightRAG : README news, 2026.05 merge and v1.5 multimodal (read 20261102 20:10 UTC)
7. https://github.com/HKUDS/RAG-Anything : README badge and news (read 20261102 20:10 UTC)
8. https://github.com/FalkorDB/GraphRAG-SDK : README benchmark table and note: Overall is FalkorDB's own average of the leaderboard's two dataset scores; competitor numbers copied from the leaderboard; first-party (read 20261102 20:28 UTC)
9. https://github.com/OSU-NLP-Group/HippoRAG : README (read 20261102 20:10 UTC)
10. https://github.com/neo4j/neo4j-graphrag-python : README, experimental namespace (read 20261102 20:10 UTC)
11. kb-kg/landscape/20261030_1954-github/repos.tsv : stars and push dates, snapshot 20261030 19:54 UTC (rows read 20261102 20:13 UTC)
12. https://arxiv.org/search/advanced and the arXiv API (https://export.arxiv.org/api/query) : keyword counts, window 20251102-20261102 against 20241102-20251101, never papers in the field. Run 1, advanced search, abstract field, computer science, read 20261102 20:18 to 20:20 UTC: GraphRAG OR "graph rag" OR "graph-based RAG" (252, 146); RAG OR "retrieval-augmented generation" (3,307, 2,711); the first plus "indexing cost" OR "construction cost" OR "LLM-free" OR "token-free" OR "zero-token" OR "cost-efficient" OR "cost-effective" OR lightweight (31, 13); hypergraph plus RAG wording (31, 11); multimodal plus the first (19, 6). Run 2, API, abstract field, all categories, submittedDate window, read 20261102 20:31 UTC: the same first two queries gave (255, 148, x1.72) and (3,357, 2,736, x1.23); the cost-wording query gave 32 for the recent window, and the other counts of run 2 were refused with HTTP 429 and not repeated. Run 3 is the catalogue's row (272, 167, x1.63; control x1.23), made by the trends researcher with a query the catalogue does not record, so it cannot be reproduced and the difference from runs 1 and 2 is unexplained beyond query wording, scope and day. The sub-counts in the text (31 against 13, 31 against 11, 19 against 6) come from run 1 only
13. https://arxiv.org/abs/2404.16130 : Edge et al., GraphRAG (read 20261102 20:16 UTC)
14. https://arxiv.org/abs/2410.05779 : Guo et al., LightRAG (read 20261102 20:16 UTC)
15. https://arxiv.org/abs/2405.14831 : Gutierrez et al., HippoRAG (read 20261102 20:16 UTC)
16. https://arxiv.org/abs/2502.14802 : HippoRAG 2 (read 20261102 20:16 UTC)
17. https://arxiv.org/abs/2409.13731 : KAG (read 20261102 20:16 UTC)
18. https://arxiv.org/abs/2510.12323 : RAG-Anything (read 20261102 20:16 UTC)
19. https://arxiv.org/abs/2506.05690 : Xiang et al., GraphRAG-Bench; abstract only: the benchmark and its leaderboard exist; the quoted sentence is background citing other studies (read 20261102 20:29 UTC)
20. https://arxiv.org/abs/2502.11371 : Han et al., RAG vs. GraphRAG, v3; Tables 1, 2, 4 and 5 and Section 3.4 re-read in the HTML full text (read 20261102 20:30 UTC)
21. https://arxiv.org/abs/2607.26497 : Wang et al., BM25 Wins at Scale, abstract only (read 20261102 20:29 UTC)
22. https://arxiv.org/abs/2609.19622 : G3RAG, abstract (read 20261102 20:16 UTC)
23. https://arxiv.org/abs/2609.18099 : EffiRAG, abstract (read 20261102 20:16 UTC)
24. https://arxiv.org/abs/2610.30755 : Bao et al., Raw-RAG, abstract (read 20261102 20:17 UTC)
25. https://arxiv.org/abs/2602.23372 : SPRIG, abstract (read 20261102 20:17 UTC)
26. https://arxiv.org/abs/2510.10114 : LinearRAG, abstract: "unstable and costly relation extraction", relation-free graph, no extra token consumption (read 20261102 20:29 UTC)
27. https://arxiv.org/abs/2501.06713 : MiniRAG, abstract (read 20261102 20:17 UTC)
28. https://arxiv.org/abs/2502.09304 : KET-RAG, abstract (read 20261102 20:17 UTC)
29. https://arxiv.org/abs/2604.09666 : Fan et al., RAGSearch, abstract (read 20261102 20:17 UTC)
30. https://arxiv.org/abs/2606.25656 : Chen et al., Is GraphRAG Needed?, abstract (read 20261102 20:17 UTC)
31. https://arxiv.org/abs/2503.21322 : HyperGraphRAG (read 20261102 20:17 UTC)
32. https://arxiv.org/abs/2508.06105 : LogicRAG, abstract: "overwhelming token cost and update latency" (read 20261102 20:31 UTC)
33. https://arxiv.org/abs/2607.11683 : RAGU, abstract (read 20261102 20:17 UTC)
34. https://arxiv.org/abs/2512.20626 : MegaRAG, abstract (read 20261102 20:17 UTC)
35. kb-kg/directions/eager-to-lazy-graphs.md : five levers and the list of who measured (read by the archive 20261030 19:57 UTC, via the archive page)
36. plans/20261102_1951-docs-catalogue.md : a decision record, not a primary source. It records the trends researcher's hand-tagged count of 20 active repositories, the family count 272 against 167 (x1.63) and the controls (any RAG wording x1.23, LLM-agent wording x2.50), from runs of 20261102 19:26 to 19:54 UTC whose queries and tagged list it does not give (read 20261102 20:28 UTC)
37. kb-kg/literature/graph-rag-research.md : G3RAG falls to naive-RAG level without its LLM seed filter (read by the archive 20261030 18:59 UTC, via the archive page)
38. https://api.github.com/repos/DEEP-PolyU/LinearRAG/license and https://api.github.com/repos/chensyCN/LogicRAG/license (GitHub API, authenticated CLI) : both LICENSE files are GPL-3.0 (read 20261102 20:33 UTC)
