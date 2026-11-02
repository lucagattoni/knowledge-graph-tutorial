---
type: index
kind: standard
aliases: [openCypher]
updated: 20261102 23:12 UTC
---

# Cypher

Cypher is a declarative query language for property graphs, created at Neo4j and since 2015 also published as the open openCypher specification (the sense of "standard" in this entry's kind). It is not itself an ISO standard; the ISO property-graph language is [GQL](./gql.md). This entry records its history and two date disputes.

## Definition

Francis and nine co-authors define Cypher as an evolving property graph query language, "originally designed and implemented as part of the Neo4j graph database", and describe Cypher 9 as the first version governed by the openCypher Implementers Group (SIGMOD 2018) [1]. The Neo4j manual calls it "Neo4j's declarative query language" (first-party) [2]. The openCypher site calls it "the most widely adopted query language for property graph databases" (first-party) [3]. The data model is the [property graph](./property-graph.md).

## How it changed

- **Early 2011.** Cypher is largely the invention of Andrés Taylor of Neo4j, inspired by [SQL](./sql.md) and drawing on functional programming, Python and [SPARQL](./sparql.md) (co-author's account) [1].
- **2013.** Neo4j says Neo4j 2.0 "shipped with the brand-new Cypher query language" (first-party) [4]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **Late 2015.** Neo4j announces the openCypher project, with Apache 2.0 grammars and a compatibility kit [1][4].
- **2018.** The SIGMOD paper gives Cypher 9 a formal semantics for core read queries and previews a compositional Cypher 10 [1].
- **2023.** SQL:2023 introduces SQL/PGQ; its syntax builds on Cypher, PGQL and GSQL (Stonebraker and Pavlo, 2024) [5]. See [SQL/PGQ](./sql-pgq.md).
- **April 2024.** ISO/IEC 39075 (GQL) is published; the openCypher site says it was a key inspiration for GQL and aims to become GQL-conformant step by step (first-party) [3]. Era: [What has settled since 2023](../history/settled-since-2023.md).
- **2025 and 2026.** From Neo4j 2025.06 new features go only into Cypher 25, the current version, and Cypher 5 is frozen; from 2026.02 new databases set Cypher 25 explicitly (first-party) [2]. Still moving: [graph query generation](../trends/graph-query-generation.md).

## Where sources disagree

- **First release.** Francis et al. date the invention to early 2011 [1]; Neo4j's retrospective names 2.0 in 2013 as shipping the "brand-new" language [4]. Neither gives the first release. The date is **unstated**.
- **GQL publication.** openCypher gives 11 April 2024 [3] and no source for it. The IEC web store gives 12 April 2024 as the publication date [6], and ISO's lifecycle table lists "International Standard published" on 2024-04-12 [8]. The GQL committee announced the publication on 17 April 2024 [7]. *Reading:* ISO's record is the publication, and the committee's date is an announcement, since its entry of 29 March said it had no official date yet [7]; what the openCypher date marks is **unstated**. See [GQL](./gql.md).

## Related

[GQL](./gql.md), [SQL/PGQ](./sql-pgq.md), [property graph](./property-graph.md), [SPARQL](./sparql.md), [SQL](./sql.md). Projects that speak Cypher: [Neo4j](../projects/neo4j.md), [FalkorDB](../projects/falkordb.md), [Memgraph](../projects/memgraph.md), [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md). Benchmark: [Text2Cypher](../benchmarks/text2cypher.md). Papers: [foundations](../papers/foundations.md), [graph query generation](../papers/graph-query-generation.md). Trend: [graph query generation](../trends/graph-query-generation.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)

**Trends**

- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)
- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Code-Graph-RAG](../projects/code-graph-rag.md)
- [codebase-memory-mcp](../projects/codebase-memory-mcp.md)
- [FalkorDB](../projects/falkordb.md)
- [GraphRAG SDK](../projects/graphrag-sdk.md)
- [Hyper-Extract](../projects/hyper-extract.md)
- [LlamaIndex](../projects/llama-index.md)
- [Memgraph](../projects/memgraph.md)
- [Neo4j](../projects/neo4j.md)
- [Neo4j LLM Knowledge Graph Builder](../projects/llm-graph-builder.md)
- [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md)
- [Projects](../projects/README.md)

**Papers**

- [Papers: Asking graphs in natural language](../papers/graph-query-generation.md)
- [Papers: Code graphs for coding agents](../papers/code-knowledge-graphs.md)
- [Papers: foundations](../papers/foundations.md)

**Benchmarks**

- [Benchmarks](../benchmarks/README.md)
- [Text2Cypher](../benchmarks/text2cypher.md)

**Applied to Pinakes**

- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Code graph](code-graph.md)
- [Embedded database](embedded-database.md)
- [GQL](gql.md)
- [Graph database](graph-database.md)
- [NoSQL](nosql.md)
- [Property graph](property-graph.md)
- [Semantic parsing](semantic-parsing.md)
- [SPARQL](sparql.md)
- [SQL/PGQ](sql-pgq.md)
- [Text-to-query](text-to-query.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.pure.ed.ac.uk/ws/files/56321692/cypher_sigmod18_crc_1.pdf : Francis et al., "Cypher: An Evolving Query Language for Property Graphs", SIGMOD 2018, doi 10.1145/3183713.3190657: abstract, early 2011, late 2015 (read 20261102 20:46 UTC)
2. https://neo4j.com/docs/cypher-manual/current/introduction/ : Neo4j Cypher manual: Cypher 25, Cypher 5 frozen from 2025.06, 2026.02 setting (first-party; read 20261102 20:47 UTC)
3. https://opencypher.org/ : openCypher: widest adoption, key inspiration for GQL, evolves toward GQL conformance, GQL published 11 April 2024 (first-party; read 20261102 20:46 UTC; the date re-read 20261102 22:52 UTC)
4. https://neo4j.com/blog/news/neo4j-top-10-biggest-moments-of-2010s/ : Neo4j blog: 2013 Neo4j 2.0 with Cypher, 2015 openCypher (first-party; read 20261102 20:48 UTC)
5. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), 2024: SQL:2023 SQL/PGQ builds on Cypher, PGQL, GSQL (read 20261102 20:45 UTC)
6. https://webstore.iec.ch/publication/94107 : IEC web store: ISO/IEC 39075:2024 edition 1.0, publication date 2024-04-12 (read 20261102 20:48 UTC; re-read 20261102 22:52 UTC)
7. https://www.gqlstandards.org/ : GQL committee page: "published" 17 April 2024; the entry of 29 March 2024 says no official publication date yet (read 20261102 20:47 UTC; both entries re-read 20261102 22:52 UTC)
8. https://committee.iso.org/es/sites/isoorg/contents/data/standard/07/61/76120.html : ISO catalogue page for ISO/IEC 39075:2024 (Spanish-language page; iso.org itself answered HTTP 403): lifecycle table, stage 60.60 "Norma Internacional publicada" on 2024-04-12 (read 20261102 22:52 UTC)
