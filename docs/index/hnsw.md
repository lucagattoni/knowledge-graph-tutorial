---
type: index
kind: concept
aliases: [Hierarchical Navigable Small World, Hierarchical Navigable Small World graphs, Hierarchical NSW]
updated: 20261102 22:59 UTC
---

# HNSW

This entry says what HNSW is, where it came from, whether its hierarchy is needed, and where it is built into databases. The wider problem is in [approximate nearest neighbour](./approximate-nearest-neighbour.md).

## Definition

Malkov and Yashunin present HNSW as an approach to approximate K-nearest-neighbour search that is "fully graph-based": it builds a multi-layer structure of proximity graphs over nested subsets of the stored elements, where an element's top layer is chosen at random with an exponentially decaying probability [1]. Search starts in the upper layer; the authors claim logarithmic complexity scaling and note the likeness to a skip list (first-party) [1].

## How it changed

- **201409.** Malkov, Ponomarenko, Logvinov and Krylov publish "Approximate nearest neighbor algorithm based on navigable small world graphs" in Information Systems 45, pages 61-68. The HNSW paper lists it with two earlier papers by the same authors (2012 and 2011, as printed in its references) as the proposal of the Navigable Small World (NSW) algorithm, and says its graphs resemble NSW structures [1][2]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20160330.** The HNSW preprint appears (v1); version 4 follows on 20180814, and IEEE TPAMI 42(4) prints the paper in April 2020, pages 824-836 [1][3]. Eras: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md) for the preprint, [Language models meet retrieval](../history/language-models-meet-retrieval.md) for the 2018 revision and the 2020 journal version.
- **20230828.** pgvector 0.5.0 adds an HNSW index type to Postgres [4]. Its README says HNSW has better query performance than IVFFlat (speed against recall) but slower builds and more memory (first-party) [5].
- **20241202.** Munyampirwa et al. report that a flat navigable small-world graph keeps HNSW's benefits on high-dimensional data (v3 20250703) [6].
- **2026.** Neo4j's manual lists HNSW settings for its Lucene-based vector indexes, with M defaulting to 16; FalkorDB documents HNSW with M also 16; pgvector's change log lists asynchronous I/O for HNSW in an unreleased 0.9.0, after 0.8.7 of 20261001 [4][7][8]. Still moving: [Infrastructure and MCP](../trends/infrastructure-and-mcp.md).

## Where sources disagree

**Is the hierarchy needed?** Malkov and Yashunin say starting from the upper layer "boosts the performance compared to NSW" [1]. Munyampirwa et al. find a flat graph has latency and recall "essentially identical" to HNSW on high-dimensional datasets, with less memory [6]. The HNSW text motivates the hierarchy by NSW's "severe performance degradation on low dimensional datasets" [1]; Munyampirwa et al. test high-dimensional ones [6]. *Reading:* the two claims may be compatible, since they cover different data.

## Related

[Approximate nearest neighbour](./approximate-nearest-neighbour.md), [vector search](./vector-search.md), [embedding](./embedding.md), [dense retrieval](./dense-retrieval.md), [hybrid search](./hybrid-search.md), [graph database](./graph-database.md). Projects: [Neo4j](../projects/neo4j.md), [FalkorDB](../projects/falkordb.md). Trend: [Infrastructure and MCP](../trends/infrastructure-and-mcp.md). Experiment: [X2, the index cost of cheap graph builders](../experiments/x2-index-cost.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)

**Index**

- [Embedded database](embedded-database.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/1603.09320 : Malkov and Yashunin, "Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs", v1 20160330, v4 20180814: abstract and submission history (read 20261102 22:12 UTC); full text at https://arxiv.org/pdf/1603.09320, section 2.1 and references 25 (2012), 26 (2014) and 30 (2011), the three NSW papers (first-party; read 20261102 22:51 UTC)
2. https://api.crossref.org/works/10.1016/j.is.2013.10.006 : Crossref record: Malkov, Ponomarenko, Logvinov, Krylov, "Approximate nearest neighbor algorithm based on navigable small world graphs", Information Systems 45, 2014-09, pages 61-68 (read 20261102 22:12 UTC)
3. https://api.crossref.org/works/10.1109/TPAMI.2018.2889473 : Crossref record: IEEE TPAMI 42(4), 2020-04, pages 824-836 (read 20261102 22:12 UTC)
4. https://raw.githubusercontent.com/pgvector/pgvector/master/CHANGELOG.md : pgvector change log: "0.5.0 (2023-08-28) Added HNSW index type"; 0.8.7 (2026-10-01); 0.9.0 (unreleased) asynchronous I/O for HNSW (first-party; read 20261102 22:13 UTC)
5. https://raw.githubusercontent.com/pgvector/pgvector/master/README.md : pgvector README, HNSW section (first-party; read 20261102 22:13 UTC)
6. https://arxiv.org/abs/2412.01940 : Munyampirwa, Lakshman, Coleman, "Down with the Hierarchy: The 'H' in HNSW Stands for 'Hubs'", v1 20241202, v3 20250703: abstract (read 20261102 22:12 UTC)
7. https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/ : Neo4j Cypher manual, vector indexes: Lucene, vector.hnsw.m default 16 (first-party; read 20261102 22:13 UTC)
8. https://docs.falkordb.com/cypher/indexing/vector-index.md : FalkorDB documentation: HNSW, M default 16 (first-party; read 20261102 22:13 UTC)
