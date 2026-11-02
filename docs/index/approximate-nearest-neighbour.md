---
type: index
kind: concept
aliases: [ANN, ANN search, approximate nearest neighbor, approximate nearest neighbor search]
updated: 20261102 21:16 UTC
---

# Approximate nearest neighbour

Approximate nearest neighbour search finds points close to a query point in a large set of vectors, and accepts that it may miss some of the true nearest ones in exchange for speed.

## Definition

Aumüller, Bernhardsson and Faithfull explain the need. Data points are often vectors of 100 to 1000 dimensions. Because of the curse of dimensionality, finding the true nearest neighbours takes either time linear in the size of the data, or time or space exponential in the dimension, which "rules out efficient and exact nearest neighbor search algorithms" for massive high-dimensional data. Research therefore lets the returned neighbours be an approximation, judged by how close the result set is to the set of true nearest neighbours [1]. Common techniques include trees, graphs built over the data, and hashing [1].

## How it changed

- **1998.** Indyk and Motwani publish "Approximate nearest neighbors: towards removing the curse of dimensionality" at STOC '98 [2]. Era: [The Web changes data and search](../history/the-web.md). The page read gives only the title and venue: its claims are **unstated** here.
- **20160330.** Malkov and Yashunin post the preprint of Hierarchical Navigable Small World graphs (HNSW), a graph-only index of stacked proximity graphs searched from the top layer down; the authors claim logarithmic scaling (first-party) [3]. Journal version: IEEE TPAMI 42(4), April 2020 [4]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20170228.** Johnson, Douze and Jégou report GPU search that builds a graph over 1 billion vectors in under 12 hours on four GPUs (first-party) [5].
- **20180715.** ANN-Benchmarks offers a tool to evaluate in-memory approximate nearest neighbour algorithms on common datasets [1].
- **20240116.** The Faiss library paper calls vector similarity search "a core functionality of vector databases" [6].
- **2026.** Graph databases document HNSW vector indexes: [Neo4j](../projects/neo4j.md) (Lucene, k-ANN) and [FalkorDB](../projects/falkordb.md) [7][8]. See [Infrastructure and MCP](../trends/infrastructure-and-mcp.md).

## Where sources disagree

On how to measure "approximate". Aumüller et al. find the intuitive recall (share of true neighbours returned) fragile when distances tie, so they define recall by distance to the k-th true neighbour, and note that approximate recall in high dimensions "is sometimes criticised" [1].

## Related

[Vector search](./vector-search.md), [embedding](./embedding.md), [dense retrieval](./dense-retrieval.md), [hybrid search](./hybrid-search.md), [reranking](./reranking.md), [vector space model](./vector-space-model.md), [information retrieval](./information-retrieval.md). Projects: [Neo4j](../projects/neo4j.md), [FalkorDB](../projects/falkordb.md), [Memgraph](../projects/memgraph.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)

**Projects**

- [FalkorDB](../projects/falkordb.md)
- [Neo4j](../projects/neo4j.md)

**Applied to Pinakes**

- [Measurements](../applied-to-pinakes/measurements.md)

**Index**

- [Dense retrieval](dense-retrieval.md)
- [Embedding](embedding.md)
- [HNSW](hnsw.md)
- [Hybrid search](hybrid-search.md)
- [Vector search](vector-search.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/1807.05614 : Aumüller, Bernhardsson, Faithfull, "ANN-Benchmarks", v1 20180715; introduction, section 2.1 (read 20261102 20:45 UTC)
2. https://api.crossref.org/works/10.1145/276698.276876 : Crossref record: Indyk and Motwani, STOC '98, 1998, pages 604-613 (read 20261102 20:45 UTC; re-read 20261102 21:16 UTC)
3. https://arxiv.org/abs/1603.09320 : Malkov and Yashunin, HNSW, v1 20160330 (read 20261102 20:44 UTC)
4. https://api.crossref.org/works/10.1109/TPAMI.2018.2889473 : Crossref record: IEEE TPAMI 42(4), April 2020, pages 824-836 (read 20261102 20:45 UTC)
5. https://arxiv.org/abs/1702.08734 : Johnson, Douze, Jégou, "Billion-scale similarity search with GPUs", v1 20170228 (read 20261102 20:45 UTC)
6. https://arxiv.org/abs/2401.08281 : Douze et al., "The Faiss library", 9 authors, v1 20240116 (read 20261102 20:45 UTC)
7. https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/ : Neo4j manual: vector indexes use Lucene, which uses an HNSW graph for a k-ANN query (read 20261102 20:49 UTC)
8. https://docs.falkordb.com/cypher/indexing/vector-index.md : FalkorDB documentation: vector index uses HNSW with cosine or Euclidean distance (read 20261102 20:49 UTC)
