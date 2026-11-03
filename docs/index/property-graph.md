---
type: index
kind: concept
aliases: [labelled property graph, labeled property graph, LPG]
updated: 20261102 23:13 UTC
---

# Property graph

A property graph is a graph whose nodes and edges carry labels and key-value properties. It is the data model of most graph database systems [1] and the one the ISO graph query standards address [7][8]. This entry gives the definition, the dated changes, and the ways published definitions differ.

## Definition

Angles describes a property graph as a directed labelled multigraph in which each node or edge can hold a set of property-value pairs. A node stands for an entity, an edge for a relationship between entities, and a property for a feature of either [1]. Hogan et al. say property graphs were introduced for extra flexibility over directed edge-labelled graphs, and that the two can be translated into each other without loss of information [2].

## How it changed

- **201006.** Rodriguez and Neubauer publish "Constructions from Dots and Lines" (arXiv 20100611; Bulletin of ASIS&T, August 2010). Angles credits them with introducing the notion [1][3]. See [the semantic web era](../history/semantic-web.md).
- **2011.** Neo4j engineers create [Cypher](./cypher.md) [4]. See [Neo4j](../projects/neo4j.md).
- **201805.** Angles gives a formal definition at the AMW workshop (Cali, 21-25 May 2018). He notes that "there is no standard specification of the database model behind such systems" [1][5].
- **20210911.** Hogan et al. give a formal definition in the survey's appendix (arXiv v6) [2].
- **20221120.** Angles and 20 co-authors propose PG-Schema, because schema support is limited in existing systems and in the first version of [GQL](./gql.md) [6].
- **202306 and 202404.** SQL/PGQ (ISO/IEC 9075-16:2023) and GQL (ISO/IEC 39075:2024) standardise property graph queries [7][8]. The day of GQL's publication is given as 20240412 by ISO's lifecycle table and 20240417 by the standards committee's announcement; see the [GQL](./gql.md) entry. See also [what has settled since 2023](../history/settled-since-2023.md) and [SQL/PGQ](./sql-pgq.md).

Query generation for property graphs is still moving: [Graph query generation](../trends/graph-query-generation.md).

## Where sources disagree

The definitions differ in detail. Angles gives nodes and edges sets of labels and allows several values per property [1]. Hogan et al. do the same, note that "some previous definitions" allowed one value, and call an array of values a syntactic variation [2]. Neo4j's model gives a node zero or more labels but a relationship exactly one type [9]. How ISO/IEC 39075 defines the model is **unstated**: the standard is sold and was not read.

## Related

Entries: [Cypher](./cypher.md), [GQL](./gql.md), [SQL/PGQ](./sql-pgq.md), [RDF](./rdf.md), [knowledge graph](./knowledge-graph.md), [NoSQL](./nosql.md). Pages: [Neo4j](../projects/neo4j.md), [Memgraph](../projects/memgraph.md), [FalkorDB](../projects/falkordb.md), [LlamaIndex](../projects/llama-index.md), [Code-Graph-RAG](../projects/code-graph-rag.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [The semantic web and linked data](../history/semantic-web.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Trends**

- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)

**Projects**

- [Code-Graph-RAG](../projects/code-graph-rag.md)
- [FalkorDB](../projects/falkordb.md)
- [LlamaIndex](../projects/llama-index.md)
- [Neo4j](../projects/neo4j.md)
- [Projects](../projects/README.md)

**Papers**

- [Papers: Building knowledge graphs with LLMs](../papers/llm-kg-construction.md)
- [Papers: foundations](../papers/foundations.md)
- [Papers: Semantic web standards](../papers/semantic-web-standards.md)

**Benchmarks**

- [Benchmarks](../benchmarks/README.md)
- [Text2Cypher](../benchmarks/text2cypher.md)

**Index**

- [CODASYL](codasyl.md)
- [Code graph](code-graph.md)
- [Cypher](cypher.md)
- [Embedded database](embedded-database.md)
- [Entity](entity.md)
- [GQL](gql.md)
- [Graph database](graph-database.md)
- [Hypergraph](hypergraph.md)
- [Knowledge graph](knowledge-graph.md)
- [RDF](rdf.md)
- [RDF-star](rdf-star.md)
- [Relational model](relational-model.md)
- [Schema](schema.md)
- [SQL/PGQ](sql-pgq.md)
- [Triple](triple.md)
- [Triple store](triple-store.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://ceur-ws.org/Vol-2100/paper26.pdf : Angles, "The Property Graph Database Model", AMW 2018: abstract, sections 1.1 and 2 (read 20261102 21:01 UTC)
2. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", v6 of 11 Sep 2021: section 2.1.3 and Definition B.5 (read 20261102 21:01 UTC)
3. https://arxiv.org/abs/1006.2361 : Rodriguez and Neubauer, "Constructions from Dots and Lines": submission 20100611 and journal reference (read 20261102 21:01 UTC)
4. https://neo4j.com/docs/cypher-manual/current/introduction/cypher-overview/ : "created in 2011 by Neo4j engineers" (read 20261102 21:04 UTC)
5. https://ceur-ws.org/Vol-2100/ : proceedings page of the 12th Alberto Mendelzon Workshop, Cali, Colombia, May 21-25, 2018 (read 20261102 21:02 UTC)
6. https://arxiv.org/abs/2211.10962 : Angles et al. (21 authors), "PG-Schema: Schemas for Property Graphs", v1 20221120, v4 20230708: abstract (read 20261102 21:02 UTC)
7. https://www.gqlstandards.org/ : GQL committee page, entry of 17 April 2024: ISO/IEC 39075:2024 published; description of SQL/PGQ (read 20261102 21:01 UTC)
8. https://committee.iso.org/es/sites/isoorg/contents/data/standard/07/94/79473.html : ISO/IEC 9075-16:2023, edition 1, published 2023-06 (read 20261102 19:56 UTC by an earlier writer, via the archive page docs/history/settled-since-2023.md)
9. https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/ : Neo4j property graph model: labels, relationship types, properties (read 20261102 21:04 UTC)
