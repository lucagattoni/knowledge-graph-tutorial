---
type: project
repo: HKUDS/LightRAG
trends: [graph-based-rag]
updated: 20261102 23:17 UTC
---

# LightRAG

This page answers what LightRAG is, how it differs from the community-summary design of [Microsoft GraphRAG](../projects/microsoft-graphrag.md), which results its authors publish, and how active the project is. The watch-list table on the chapter landing carries its stars and push dates.

| Field | Value |
|---|---|
| Repository | https://github.com/HKUDS/LightRAG |
| Licence | MIT. GitHub's licence endpoint classifies the `LICENSE` file as MIT; the file reads "MIT License", "Copyright (c) 2025 LightRAG Team" [1][2] |
| Trends | [Graph-based RAG](../trends/graph-based-rag.md) |

## What it is

LightRAG is a [retrieval-augmented generation](../index/retrieval-augmented-generation.md) framework from the HKUDS organisation. A [large language model](../index/large-language-model.md) builds a [knowledge graph](../index/knowledge-graph.md), which is stored beside vector [embeddings](../index/embedding.md) [1][3]. The README calls it "a lightweight knowledge-graph RAG framework and an efficient alternative to Microsoft GraphRAG"; it builds no community hierarchy and writes no community summaries [4][5]. The repository description credits the paper to EMNLP (Empirical Methods in Natural Language Processing) 2025; the arXiv page lists no venue [1][3]. It ships as a Python library and as a server with a web interface and a REST API [4].

## How it works

**Indexing.** The model extracts entities and relations from each [chunk](../index/chunking.md). Entities are merged by exact name, not by embedding similarity; descriptions from different chunks are concatenated and sometimes re-summarised by the model (read in the code on 20261030) [5]. Entities and relations are embedded and keep the list of chunks they came from [5]. Four chunking strategies exist, and documents are parsed by MinerU, Docling or a native engine [4].

**Querying.** The paper's idea is dual-level retrieval: low-level keywords match specific entities, high-level keywords match broad concepts and relations [3][5]. Five modes [4]:

| Mode | Retrieves |
|---|---|
| local | Entities and their direct attributes |
| global | Relationship chains covering broad themes |
| hybrid | Local and global together |
| naive | Chunks by vector similarity only, no graph |
| mix | Local, global and naive together; the default |

A model call extracts keywords (skipped if the caller passes them), an optional reranker call follows, and one more call writes the answer; there is no router that picks a mode [5]. The default storages are, in the README's words, "not suitable for production"; PostgreSQL is recommended, with MongoDB, OpenSearch, Milvus, Qdrant, [Neo4j](../projects/neo4j.md) and [Memgraph](../projects/memgraph.md) as options [4].

**Cost.** Indexing needs at least one model call per chunk. Deleting a document rebuilds the affected graph part from cached extraction results, without new model calls [4][5]. Since May 2026 four roles (extraction, query, keyword, vision) take separate model settings, so extraction can use a cheaper model [4]. The embedding model must be fixed before indexing [4]. In May 2026 the project merged "RagAnything" into itself [4]; [RAG-Anything](../projects/rag-anything.md) is the sibling repository of that name.

## Evidence

All published results are the authors' own (first-party). Third-party evaluations were not fetched: **unstated**.

The paper (arXiv 2410.05779) reports "considerable improvements in retrieval accuracy and efficiency", with no figures in the abstract [3]. The README reproduces pairwise win shares, judged by an LLM (large language model), over four subsets of the [UltraDomain](../datasets/ultradomain.md) dataset. LightRAG's *overall* win share, as run by the LightRAG authors and read from the README on 20261102 [4][6]:

| Baseline | Agriculture | CS | Legal | Mix |
|---|---|---|---|---|
| NaiveRAG | 67.6% | 61.2% | 84.8% | 60.0% |
| RQ-RAG | 67.6% | 62.0% | 85.6% | 60.0% |
| HyDE | 75.2% | 58.4% | 73.6% | 57.6% |
| GraphRAG | 54.8% | 52.0% | 52.8% | 49.6% |

Against GraphRAG on Mix the baseline wins narrowly on the overall figure (50.4% to 49.6%) [4]. An LLM generates the queries from a dataset description and an LLM judges each pair on comprehensiveness, diversity and empowerment [6]. Win share is not factual accuracy. The judge model, the repeat count and the GraphRAG baseline's settings are not stated in the files read [6].

*Reading:* the margin over plain vector retrieval is clear in the authors' own table. The margin over GraphRAG is small and, on one subset, reversed. The sources read contain no cost measurement by the project itself.

## Status and direction

- **Latest release.** v1.5.7, 20260902: a query-only `/workspace` page, branding templates and a global prompt prefix. No release since, 61 days at reading time [7].
- **Activity, 20260804 to 20261102.** 1,515 commits on `main`: 724 in August, 777 in September, 14 in October. The newest on `main` is 20261014, a PostgreSQL vector-search fix. The `dev` branch is 221 commits ahead of `main`, newest 20260930 [8][9]. Not archived [1].
- **Direction.** README news, newest first: Word heading recognition (July 2026); RAG-Anything merge, MinerU and Docling parsing, four chunking strategies (May 2026); OpenSearch backend and setup wizard (March 2026); RAGAS evaluation and Langfuse tracing (November 2025) [4]. Branch names suggest LanceDB, NebulaGraph and DocumentDB backends and multi-workspace access; contents not read. A Redis deprecation warning was merged to `dev` on 20260930 (title only) [9].
- **Hosted tier and MCP (Model Context Protocol).** The README names no hosted tier and does not mention the [Model Context Protocol](../index/model-context-protocol.md) [4].

*Reading:* high activity, a wide storage matrix and frequent releases to September, then a quiet `main`. The project kept adding features through September, where [GraphRAG](../projects/microsoft-graphrag.md) says it will not. Its large core and many branches make stability hard to judge from outside.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [HippoRAG](hipporag.md)
- [Hyper-Extract](hyper-extract.md)
- [LlamaIndex](llama-index.md)
- [Memgraph](memgraph.md)
- [Microsoft GraphRAG](microsoft-graphrag.md)
- [OpenViking](openviking.md)
- [Projects](README.md)
- [RAG-Anything](rag-anything.md)

**Papers**

- [Papers: Graph-based RAG](../papers/graph-based-rag.md)

**Datasets**

- [UltraDomain](../datasets/ultradomain.md)

**Benchmarks**

- [EnterpriseRAG-Bench](../benchmarks/enterpriserag-bench.md)
- [GraphRAG-Bench (Xiang)](../benchmarks/graphrag-bench-xiang.md)
- [GraphRAG-Bench (Xiao)](../benchmarks/graphrag-bench-xiao.md)
- [MultiHop-RAG](../benchmarks/multihop-rag.md)

**Experiments**

- [Experiments](../experiments/README.md)
- [X2: the index cost of cheap graph builders](../experiments/x2-index-cost.md)
- [X3: Matched-cost comparison](../experiments/x3-matched-cost-comparison.md)

**Applied to Pinakes**

- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Community report](../index/community-report.md)
- [Gleaning](../index/gleaning.md)
- [GraphRAG](../index/graphrag.md)

<!-- END GENERATED: appears-in -->

## Sources

Papers: Guo, Xia, Yu and 2 others, "LightRAG: Simple and Fast Retrieval-Augmented Generation", arXiv 2410.05779, 2024 [3]. The papers chapter group page for the trend is [Graph-based RAG papers](../papers/graph-based-rag.md).

1. https://api.github.com/repos/HKUDS/LightRAG : description, licence field (MIT), archived flag (false), created 20241002 (read 20261102 20:09 UTC)
2. https://github.com/HKUDS/LightRAG/blob/main/LICENSE : licence file text via the licence endpoint (read 20261102 20:09 UTC)
3. https://arxiv.org/abs/2410.05779 : title, five authors, abstract, versions v1 20241008 to v3 20250428, no venue listed (read 20261102 20:10 UTC)
4. https://github.com/HKUDS/LightRAG/blob/main/README.md : self-description, news list, query modes, default mode, storage guidance, role-specific models, embedding note, MCP absence, the results table (read 20261102 20:09 UTC)
5. https://github.com/HKUDS/LightRAG/blob/main/lightrag/operate.py and https://github.com/HKUDS/LightRAG/blob/main/lightrag/base.py : exact-name entity merge, keyword call, no router, deletion rebuild from cache, evaluation tool (read 20261030 19:01 UTC, via the archive page [kb-kg/projects/lightrag.md](../../kb-kg/projects/lightrag.md)); the default mode `mix` in `base.py` was re-read on 20261102 20:12 UTC
6. https://github.com/HKUDS/LightRAG/blob/main/docs/Reproduce.md : UltraDomain dataset, query generation, LLM judging prompt, results table (read 20261102 20:11 UTC)
7. https://github.com/HKUDS/LightRAG/releases : release list with dates; v1.5.7 notes (read 20261102 20:10 UTC)
8. https://github.com/HKUDS/LightRAG/commits/main : commits since 20260804, monthly counts, newest commit on `main` (read 20261102 20:10 UTC)
9. https://github.com/HKUDS/LightRAG/branches : branch names; `dev` head and its distance from `main` (read 20261102 20:11 UTC)
