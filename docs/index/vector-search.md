---
type: index
kind: concept
aliases: [vector similarity search, similarity search, vector retrieval, embedding search]
updated: 20261102 21:25 UTC
---

# Vector search

This entry says what vector search is, dates the steps that made it a standard part of data systems, and records the dispute over whether it needs systems of its own. It answers how a search by meaning, begun with sparse term vectors, became a feature of databases.

## Definition

Vector search finds the stored vectors that lie closest to a query vector. In the account of Stonebraker and Pavlo, a database holds [embeddings](./embedding.md) made by an AI model; the same model turns the query into a vector; the system returns the records whose vectors lie nearest to it. To avoid scanning every vector, it builds an index for [approximate nearest neighbour](./approximate-nearest-neighbour.md) search [1]. The authors of the Faiss library call vector similarity search "a core functionality of vector databases" [2].

## How it changed

- **1975.** The [vector space model](./vector-space-model.md) already ranks documents by closeness of sparse term vectors [3]. See [Formal foundations](../history/formal-foundations.md).
- **201101.** Jégou, Douze and Schmid publish "Product Quantization for Nearest Neighbor Search" [4]. Pan et al. name quantization a vector-compression technique [5].
- **20170228.** Johnson, Douze and Jégou report a nearest-neighbour graph connecting 1 billion vectors, built in under 12 hours on four GPUs (first-party) [6]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20200522.** Lewis et al. use a dense vector index of Wikipedia as the memory of a generator [7]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20210420.** pgvector, a Postgres extension, has its first release, 0.1.0 [8].
- **2023.** After ChatGPT, Oracle, SingleStore, Rockset and ClickHouse add vector indexes [1]. Pan et al. (20231021) count over 20 commercial vector database systems, all under five years old [5].
- **2026, still moving.** The pgvector README offers exact and approximate search with HNSW or IVFFlat indexes [9]; Neo4j documents vector indexes on Lucene [10]. PageIndex "replaces the vector index with a hierarchical tree index" (first-party) [11]. See [Infrastructure and MCP](../trends/infrastructure-and-mcp.md) and [vectorless retrieval](../trends/reasoning-over-structure.md).

## Where sources disagree

**New kind of system, or a feature?** Stonebraker and Pavlo call vector databases "essentially document-oriented DBMSs with specialized ANN indexes" and write that such indexes are "a feature, not the foundation of a new system architecture" [1]. Pan et al. count five obstacles, among them large vectors and hybrid queries on attributes and vectors [5].

**Is similarity relevance?** The PageIndex README argues "similarity ≠ relevance" and drops vectors (first-party) [11]. The sources read give no measurement that settles it.

## Related

[embedding](./embedding.md) · [approximate nearest neighbour](./approximate-nearest-neighbour.md) · [dense retrieval](./dense-retrieval.md) · [hybrid search](./hybrid-search.md) · [vector space model](./vector-space-model.md) · [retrieval-augmented generation](./retrieval-augmented-generation.md) · [Neo4j](../projects/neo4j.md) · [PageIndex](../projects/pageindex.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Trends**

- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)
- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)

**Projects**

- [codebase-memory-mcp](../projects/codebase-memory-mcp.md)
- [Dify](../projects/dify.md)
- [GraphRAG SDK](../projects/graphrag-sdk.md)
- [Hindsight](../projects/hindsight.md)
- [Hyper-Extract](../projects/hyper-extract.md)
- [Letta](../projects/letta.md)
- [LlamaIndex](../projects/llama-index.md)
- [LLM Wiki (nashsu)](../projects/llm-wiki-nashsu.md)
- [Mem0](../projects/mem0.md)
- [memU](../projects/memu.md)
- [MIRIX](../projects/mirix.md)
- [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md)
- [OpenViking](../projects/openviking.md)
- [RAG-Anything](../projects/rag-anything.md)

**Papers**

- [Papers: Agentic search over raw data](../papers/agentic-search.md)
- [Papers: Graph-based RAG](../papers/graph-based-rag.md)

**Datasets**

- [Wikidata](../datasets/wikidata.md)

**Benchmarks**

- [EnterpriseRAG-Bench](../benchmarks/enterpriserag-bench.md)
- [RAGSearch](../benchmarks/ragsearch.md)

**Experiments**

- [X3: Matched-cost comparison](../experiments/x3-matched-cost-comparison.md)

**Applied to Pinakes**

- [Measurements](../applied-to-pinakes/measurements.md)
- [The Pinakes graph approach](../applied-to-pinakes/approach.md)

**Index**

- [Approximate nearest neighbour](approximate-nearest-neighbour.md)
- [Dense retrieval](dense-retrieval.md)
- [Embedded database](embedded-database.md)
- [Embedding](embedding.md)
- [grep](grep.md)
- [HNSW](hnsw.md)
- [Hybrid search](hybrid-search.md)
- [Inverted index](inverted-index.md)
- [Reciprocal rank fusion](reciprocal-rank-fusion.md)
- [Retrieval-augmented generation](retrieval-augmented-generation.md)
- [Vector space model](vector-space-model.md)
- [Vectorless retrieval](vectorless-retrieval.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), June 2024, section 2.7 Vector Databases: similarity search, ANN indexes, 2023 relational vector indexes, "a feature, not the foundation" (read 20261102 21:00 UTC)
2. https://arxiv.org/abs/2401.08281 : Douze et al., "The Faiss library", abstract, v1 20240116 (v4 20251023): vector similarity search as "a core functionality of vector databases" (read 20261102 21:00 UTC)
3. https://arxiv.org/pdf/2010.06467 : Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking", section 1.2.1: Salton et al. 1975 cited for the vector space model, with sparse term vectors (read 20261102 21:05 UTC)
4. https://api.crossref.org/works/10.1109/TPAMI.2010.57 : Crossref record: Jégou, Douze, Schmid, "Product Quantization for Nearest Neighbor Search", IEEE TPAMI 33(1), January 2011 (read 20261102 21:01 UTC)
5. https://arxiv.org/abs/2310.14021 : Pan, Wang, Li, "Survey of Vector Database Management Systems", abstract, submitted 20231021 (read 20261102 21:00 UTC)
6. https://arxiv.org/abs/1702.08734 : Johnson, Douze, Jégou, "Billion-scale similarity search with GPUs", abstract, submitted 20170228 (read 20261102 21:03 UTC)
7. https://arxiv.org/abs/2005.11401 : Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", abstract, v1 20200522 (read 20261102 21:03 UTC)
8. https://raw.githubusercontent.com/pgvector/pgvector/master/CHANGELOG.md : pgvector changelog: "0.1.0 (2021-04-20) First release" (read 20261102 21:01 UTC)
9. https://raw.githubusercontent.com/pgvector/pgvector/master/README.md : pgvector README: exact and approximate nearest neighbour search; HNSW and IVFFlat (read 20261102 21:01 UTC)
10. https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/ : Neo4j Cypher manual: "Neo4j vector indexes are powered by the Apache Lucene indexing and search library" (read 20261102 21:03 UTC)
11. https://raw.githubusercontent.com/VectifyAI/PageIndex/main/README.md : PageIndex README: "replaces the vector index with a hierarchical tree index"; "similarity ≠ relevance" (read 20261102 21:04 UTC)
