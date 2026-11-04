---
type: project
repo: microsoft/graphrag
trends: [graph-based-rag]
updated: 20261102 23:17 UTC
---

# Microsoft GraphRAG

This page answers what Microsoft's GraphRAG is and how it turns a text collection into a graph that answers questions. It then says what has been shown about it, and by whom. It ends with where the project stands now that its authors have put it in maintenance mode.

| Field | Value |
|---|---|
| Repository | https://github.com/microsoft/graphrag |
| Licence | MIT. GitHub's licence endpoint classifies the `LICENSE` file as MIT; the file begins "MIT License", "Copyright (c) Microsoft Corporation." [1][2] |
| Trends | [Graph-based RAG](../trends/graph-based-rag.md) |

## What it is

GraphRAG is a data pipeline and query system for [retrieval-augmented generation](../index/retrieval-augmented-generation.md) built on a [knowledge graph](../index/knowledge-graph.md). A [large language model](../index/large-language-model.md) extracts entities and relationships from every text chunk. The pipeline clusters the graph into a hierarchy of communities and has the model write a summary for each [8][9]. Microsoft Research published the idea in April 2024 as "From Local to Global" (arXiv 2404.16130). It targets *global* questions such as "What are the main themes in the dataset?", which top-k retrieval cannot answer because they are summarisation tasks [9]. The README calls the code "a demonstration" and "not an officially supported Microsoft offering" [4]. The name [GraphRAG](../index/graphrag.md) is now also used for the whole family; this page covers the original project.

## How it works

**Indexing, Standard method (default).** Text units, documents, graph extraction, claims (optional, off by default), communities, community reports, embeddings [6][7]. Defaults: 1,200-token [chunks](../index/chunking.md) with an overlap of 100, one gleaning round (a second extraction pass per chunk), and [community detection](../index/community-detection.md) by hierarchical Leiden clustering with clusters of at most 10 [6]. That makes two model calls per chunk at the defaults [14]. The documentation estimates graph extraction at "roughly 75% of indexing cost" [7].

**Indexing, Fast method.** `--method fast` swaps model-based extraction for noun-phrase extraction with classical language-processing tools. Community reports still use the model [6][7]. The documentation calls it "much cheaper" but says the graph "tends to be quite a bit noisier" [7].

**Querying.** Four modes [8]:

| Mode | Use |
|---|---|
| Global | Whole-corpus questions, answered from community summaries |
| Local | Questions about specific entities and their neighbours |
| DRIFT | Entity questions with community context added |
| Basic | Plain top-k vector search, the baseline |

An optional dynamic community selection has the model rate communities from the top of the hierarchy and drop irrelevant branches [10][15].

**LazyGraphRAG.** A November 2024 blog post describes a variant that uses no model at index time [11]. The repository does not contain it (see Status).

## Evidence

All results below are first-party: run by Microsoft Research authors.

| Claim | Source |
|---|---|
| "Substantial improvements" over a conventional RAG (retrieval-augmented generation) baseline in comprehensiveness and diversity, on global questions over datasets "in the 1 million token range"; the abstract gives no figures | Paper, 2024 [9] |
| Dynamic community selection cut total token cost by 77% on average against static global search at level 1, with no significant quality difference; 50 questions, AP News data, an LLM (large language model) as judge. At level 3 quality rose (win rates 58% and 60% on two measures) but cost was 34% higher | Blog, 20241115 [10] |
| LazyGraphRAG indexing cost "identical to vector RAG and 0.1% of the costs of full GraphRAG"; "more than 700 times lower query cost" at comparable global-query quality. Test set: 5,590 news articles, 100 synthetic queries | Blog, 20241125 [11] |

No code, prompts or paper stand behind the LazyGraphRAG figures in the sources read. An independent evaluation was not searched for: **unstated**, not "none exist". The [LightRAG](../projects/lightrag.md) page holds a competing project's own comparison against GraphRAG.

*Reading:* the evidence is answer quality on one kind of question, judged by a model, plus cost claims from the same team. It supports the idea; it does not compare the pipeline with cheaper methods at matched cost.

## Status and direction

- **Maintenance mode.** The README: "This project is largely in maintenance mode, and won't be accepting new PRs or implementing new features." It promises bug fixes and dependency updates, "particularly to address CVEs" [4]. The commit "Add notice." dates it to 20260814 [5].
- **Latest release.** v3.3.0, 20261008 (a SQLite performance fix). Since the maintenance notice: v3.1.2 (20260821), v3.2.0 (20260924, a new cache implementation), v3.3.0 (20261008). The release before them, v3.1.1, is dated 20260718 [3][5].
- **Activity, 20260804 to 20261102.** 21 commits on `main`: dependency sweeps, a notebook, documentation edits, the cache work, three releases (v3.1.2, v3.2.0, v3.3.0), pinned workflow actions. The newest is 20261102. Not archived [1][5].
- **LazyGraphRAG is not open source.** A code search finds only a documentation link and a code comment; no path in the tree contains "lazy" or "mcp". Issue 1512, "When will LazyGraphRAG arrive?", was closed as not planned on 20251118: "At this point we have no ETA" (estimated time of arrival) [13]. The blog's note of 20250606 says it "has been integrated into Microsoft Discovery" and into Azure Local services "as part of a public preview" [11]; the project page names Microsoft Discovery, an Azure research platform [12]. Part of the lineage thus moved to hosted products; their terms are unstated.
- **Successor.** None found; name, owner and description are unchanged [1][12].

*Reading:* the code stays usable and patched, but its authors say they have moved on. Treat it as a reference implementation of the community-summary design, not as a project to wait on for features. The [features in and out](../trends/features-in-and-out.md) page covers this notice among other dated changes.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)
- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md)
- [Trends: what the field is doing now](../trends/README.md)
- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Projects**

- [HippoRAG](hipporag.md)
- [Hyper-Extract](hyper-extract.md)
- [LightRAG](lightrag.md)
- [LlamaIndex](llama-index.md)
- [Projects](README.md)
- [Semantica](semantica.md)

**Papers**

- [Papers: Graph-based RAG](../papers/graph-based-rag.md)

**Benchmarks**

- [EnterpriseRAG-Bench](../benchmarks/enterpriserag-bench.md)
- [GraphRAG-Bench (Xiang)](../benchmarks/graphrag-bench-xiang.md)
- [GraphRAG-Bench (Xiao)](../benchmarks/graphrag-bench-xiao.md)
- [HotpotQA](../benchmarks/hotpotqa.md)
- [RAGSearch](../benchmarks/ragsearch.md)

**Experiments**

- [Experiments evidence: status log](../experiments/evidence/status.md)
- [X2: the index cost of cheap graph builders](../experiments/x2-index-cost.md)
- [X3: Matched-cost comparison](../experiments/x3-matched-cost-comparison.md)

**Applied to Pinakes**

- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Community detection](../index/community-detection.md)
- [Community report](../index/community-report.md)
- [Entity](../index/entity.md)
- [Gleaning](../index/gleaning.md)
- [GraphRAG](../index/graphrag.md)
- [Query-focused summarization](../index/query-focused-summarization.md)

<!-- END GENERATED: appears-in -->

## Sources

Papers: Edge, Trinh, Cheng and 7 others, "From Local to Global: A Graph RAG Approach to Query-Focused Summarization", arXiv 2404.16130, 2024 [9]. The papers chapter group page for the trend is [Graph-based RAG papers](../papers/graph-based-rag.md).

1. https://api.github.com/repos/microsoft/graphrag : description, licence field (MIT), archived flag (false), created 20240327, language (read 20261102 20:09 UTC)
2. https://github.com/microsoft/graphrag/blob/main/LICENSE : licence file text via the licence endpoint (read 20261102 20:09 UTC)
3. https://github.com/microsoft/graphrag/releases : latest release v3.3.0 (20261008 18:28 UTC) and the release list with dates, including v3.1.1 (20260718) and the v3.3.0 notes (read 20261102 20:31 UTC)
4. https://github.com/microsoft/graphrag/blob/main/README.md : maintenance notice, repository guidance, indexing-cost warning (read 20261102 20:09 UTC)
5. https://github.com/microsoft/graphrag/commits/main : 21 commits since 20260804, titles, the three release commits, newest commit 20261102 (read 20261102 20:31 UTC)
6. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/config/defaults.py and https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/index/workflows/factory.py : chunk size and overlap, gleanings, cluster size, Standard and Fast workflow lists; claim extraction `enabled: bool = False` in `defaults.py` (read 20261102 20:12 UTC; `defaults.py` re-read 20261102 20:31 UTC)
7. https://github.com/microsoft/graphrag/blob/main/docs/index/methods.md : Fast method, the 75% estimate, the trade-off statement; claim extraction listed as "(optional)" (read 20261102 20:12 UTC; re-read 20261102 20:31 UTC)
8. https://github.com/microsoft/graphrag/blob/main/docs/index.md : indexing steps, Leiden hierarchy, the four query modes (read 20261102 20:12 UTC)
9. https://arxiv.org/abs/2404.16130 : title, authors (10), abstract, versions v1 20240424 and v2 20250219 (read 20261102 20:10 UTC)
10. https://www.microsoft.com/en-us/research/blog/graphrag-improving-global-search-via-dynamic-community-selection/ : 77% cost reduction, 50 questions, AP News data, level-3 results (read 20261102 20:10 UTC)
11. https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ : mechanism, cost claims, test set, editor's note of 20250606 naming Microsoft Discovery and Azure Local services (read 20261102 20:10 UTC; the note re-read 20261102 20:31 UTC)
12. https://www.microsoft.com/en-us/research/project/graphrag/ : Microsoft Discovery statement, related items (read 20261102 20:10 UTC)
13. https://github.com/microsoft/graphrag/issues/1512 and the GitHub code, repository and tree search endpoints : issue closed as not planned 20251118; two files mention LazyGraphRAG; no "lazy" or "mcp" path (read 20261102 20:11 UTC)
14. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/index/operations/extract_graph/graph_extractor.py : two calls per chunk at one gleaning (read 20261030 18:59 UTC, via the archive page [kb-kg/projects/microsoft-graphrag.md](../../kb-kg/projects/microsoft-graphrag.md))
15. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/query/structured_search/global_search/search.py : dynamic community selection reads (read 20261030 18:59 UTC, via the archive page [kb-kg/projects/microsoft-graphrag.md](../../kb-kg/projects/microsoft-graphrag.md))
