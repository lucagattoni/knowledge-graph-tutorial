---
type: index
kind: concept
aliases: [graph DBMS, graph DB, graph database management system]
updated: 20261102 22:56 UTC
---

# Graph database

This entry says what a graph database is, when the idea and the first products appeared, and what is disputed about their future. Products have their own pages.

## Definition

Angles and Gutierrez (ACM Computing Surveys 40(1), February 2008) define graph database models as those in which "data structures for the schema and instances are modeled as graphs or generalizations of them" [1]. Stonebraker and Pavlo name two ways to represent graphs, RDF and property graphs, and discuss only the latter because they are "more common" and "a superset of RDF" [2].

## How it changed

- **1980s to 2008.** Graph database models "took off" in the eighties and early nineties alongside object-oriented models; their influence "gradually died out" as other models appeared, among them geographical, spatial, semistructured and XML ones. The 2008 survey says the need to manage graph-like information has "reestablished the relevance" of the area [1]. Eras: [Knowledge systems: boom and bust](../history/knowledge-systems.md), [The Web changes data and search](../history/the-web.md).
- **Early 2010.** Neo4j announces the general release of Neo4j 1.0. A Neo4j blog of 20191231 says that at that point the world's leading graph database "was still the world's only graph database" (first-party; a retrospective claim, not checked here) [4].
- **20230601.** ISO lists SQL/PGQ, ISO/IEC 9075-16:2023, as published: graph queries inside SQL [5]. See [SQL/PGQ](./sql-pgq.md).
- **20240417.** The standards committee announces ISO/IEC 39075:2024, [GQL](./gql.md), as published [6]. Era: [What has settled since 2023](../history/settled-since-2023.md).
- **20251010.** Kuzu, "an embedded graph database", has its last push and release (v0.11.3); its README announces archiving, and GitHub marks it archived (read 20261102) [7]. The reason is **unstated**. See [Features in and out](../trends/features-in-and-out.md).
- **20260920.** Nguyen et al. compare eight systems, one of them the engine of Corvic AI, employer of three authors; "no system in this sample is categorically fastest", and bulk-ingest throughput ranges from 5.0k to 4.3M rows/s (first-party in part) [8]. Still moving: [Infrastructure and MCP](../trends/infrastructure-and-mcp.md).

## Where sources disagree

**Do specialised graph databases have a future?** Stonebraker and Pavlo (June 2024): "We do not expect specialized graph DBMSs to be a large market"; relational systems will serve most operational graph work, and DuckDB's SQL/PGQ is cited, second-hand, as up to 10 times faster than a leading graph database [2]. The 2026 comparison finds a SQL/PGQ system "measurably slower" in its test [8]. *Reading:* the workloads differ, so these are not one test. The dispute is also told in [relational model](./relational-model.md).

**Which models count.** Stonebraker and Pavlo treat property graphs as the superset of RDF [2]; Hogan et al. say property graphs can be translated to and from directed edge-labelled graphs, the family that includes RDF, "without loss of information" [3]. See [triple store](./triple-store.md).

## Related

[Property graph](./property-graph.md), [triple store](./triple-store.md), [Cypher](./cypher.md), [GQL](./gql.md), [SQL/PGQ](./sql-pgq.md), [relational model](./relational-model.md), [embedded database](./embedded-database.md), [knowledge graph](./knowledge-graph.md). Projects: [Neo4j](../projects/neo4j.md), [FalkorDB](../projects/falkordb.md), [Memgraph](../projects/memgraph.md). Trend: [Infrastructure and MCP](../trends/infrastructure-and-mcp.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)

**Projects**

- [Cognee](../projects/cognee.md)
- [FalkorDB](../projects/falkordb.md)
- [Mem0](../projects/mem0.md)
- [Memgraph](../projects/memgraph.md)
- [Neo4j](../projects/neo4j.md)
- [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md)
- [Projects](../projects/README.md)

**Papers**

- [Papers: Asking graphs in natural language](../papers/graph-query-generation.md)
- [Papers: foundations](../papers/foundations.md)

**Benchmarks**

- [Text2Cypher](../benchmarks/text2cypher.md)

**Index**

- [ACID](acid.md)
- [Embedded database](embedded-database.md)
- [HNSW](hnsw.md)
- [Text-to-query](text-to-query.md)
- [Triple store](triple-store.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://users.dcc.uchile.cl/~cgutierr/papers/surveyGDB.pdf : Angles and Gutierrez, "Survey of Graph Database Models", ACM Computing Surveys 40(1), Article 1, February 2008: abstract (definition; "took off in the eighties and early nineties alongside object-oriented models"; influence "gradually died out"; relevance "reestablished"), DOI 10.1145/1322432.1322433 (read 20261102 22:51 UTC)
2. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), June 2024, section 2.8 and summary: RDF and property graphs, forecast, DuckDB (read 20261102 22:07 UTC)
3. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", section 2.1.1 (RDF as a standardised data model based on directed edge-labelled graphs) and section 2.1.3 (property graphs in graph databases; translation to and from directed edge-labelled graphs without loss of information) (read 20261102 22:51 UTC)
4. https://neo4j.com/blog/news/neo4j-top-10-biggest-moments-of-2010s/ : Neo4j blog, 31 December 2019: "2010: Neo4j 1.0 is released"; "In early 2010, we were proud to announce the GA release of Neo4j 1.0"; "the world's leading graph database was still the world's only graph database" (first-party; read 20261102 22:51 UTC)
5. https://committee.iso.org/es/sites/isoorg/contents/data/standard/07/94/79473.html : ISO catalogue page for ISO/IEC 9075-16:2023 (Spanish-language page): edition 1, 2023-06, lifecycle row 60.60 on 2023-06-01 (read 20261102 22:08 UTC)
6. https://www.gqlstandards.org/ : GQL committee page: "April 17, 2024 - The GQL Standard is published!" (first-party; read 20261102 22:07 UTC)
7. https://github.com/kuzudb/kuzu : GitHub API (archived flag true; last push 20251010; release v0.11.3 published 20251010; read 20261102 22:09 UTC) and README (archiving note; "an embedded graph database"; read 20261102 22:15 UTC)
8. https://arxiv.org/abs/2609.23315 : Nguyen et al., graph database engines comparison, v1 20260920: abstract; affiliations in the full text at https://arxiv.org/html/2609.23315 (read 20261102 22:07 UTC and 22:09 UTC)
