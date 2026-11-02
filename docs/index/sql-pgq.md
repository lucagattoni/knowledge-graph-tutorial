---
type: index
kind: standard
aliases: [Property Graph Queries, ISO/IEC 9075-16]
updated: 20261102 21:26 UTC
---

# SQL/PGQ

SQL/PGQ is Part 16 of the SQL standard: it defines property graphs over SQL tables and queries them with graph patterns inside SQL. This entry gives the definition, the road to publication in 2023 and the tie to GQL. Product conformance is mostly unstated in the sources read.

## Definition

ISO/IEC 9075-16:2023, "Property Graph Queries (SQL/PGQ)", "defines ways for the SQL language to represent property graphs and to interact with them"; it is edition 1, 269 pages, from ISO/IEC JTC 1/SC 32 [1]. Deutsch et al. (18 authors, 2021) say it "specifies how to define graph views over an SQL tabular schema, and to run read-only queries against them" [2]. The standards committee names two capabilities: syntax to create a [property graph](./property-graph.md) view over existing SQL tables, and syntax to put a graph query in a GRAPH_TABLE function in an SQL FROM clause [3].

## How it changed

- **20190913.** ISO lists a new project for Part 16 as approved [1]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20211212.** Deutsch et al. describe the graph pattern language that SQL/PGQ and [GQL](./gql.md) share [2].
- **202207.** The committee finishes the work needed to start a Draft International Standard (DIS) ballot on eleven parts of ISO/IEC 9075, Part 16 among them; the documents are to go to ISO at the beginning of 202208. It calls the pattern language "essentially identical" to GQL's [3].
- **20221004 to 20221228.** The 12-week DIS vote [1].
- **20230516.** The committee says it kept GQL's pattern language "as identical as possible" to SQL/PGQ's [3].
- **20230601.** ISO lists the International Standard as published [1]. Era: [What has settled since 2023](../history/settled-since-2023.md).
- **2024.** Stonebraker and Pavlo say SQL:2023 introduced it, its syntax builds on [Cypher](./cypher.md), PGQL and GSQL, and cited work has it in DuckDB beating a leading graph database by up to 10 times (second-hand) [4].
- **20260212.** Text2GraphQuery-Bench, a first-party "first benchmark" of Cypher, GQL and SQL/PGQ, appears; still moving: [asking graphs in natural language](../trends/graph-query-generation.md) [5].
- **2026.** Corrigendum 1:2026 is published and a committee draft of a replacement is in development; days **unstated** [1].

## Where sources disagree

- **Length of the DIS stage.** The committee expects a DIS process of 20 weeks, 8 of preliminary ISO time and 12 of ballot, ending by December 2022 [3]; ISO lists a 12-week ballot from 20221004 to 20221228, after DIS registration on 20220805 [1].
- **Publication.** The committee hoped in 202305 for publication "by the end of May, 2023" [3]; ISO lists 2023-06-01 [1].
- **What it covers.** ISO says "interact with" property graphs [1]; Deutsch et al. say read-only queries [2]. Whether it defines updates is **unstated**.
- **Implementations.** Beyond the DuckDB result [4], product conformance is **unstated**.

## Related

[SQL](./sql.md), [GQL](./gql.md), [Cypher](./cypher.md), [property graph](./property-graph.md), [relational model](./relational-model.md), [SPARQL](./sparql.md). Page: [infrastructure and MCP](../trends/infrastructure-and-mcp.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Trends**

- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)

**Index**

- [Cypher](cypher.md)
- [GQL](gql.md)
- [Graph database](graph-database.md)
- [Property graph](property-graph.md)
- [Relational model](relational-model.md)
- [SQL](sql.md)
- [Text-to-query](text-to-query.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://committee.iso.org/es/sites/isoorg/contents/data/standard/07/94/79473.html : ISO catalogue page for ISO/IEC 9075-16:2023 (Spanish-language page; abstract, edition 1, 269 pages, lifecycle table with 2019-09-13, 2022-10-04, 2022-12-28, 2023-06-01; Cor 1:2026; ISO/IEC CD 9075-16) (read 20261102 21:00 UTC; lifecycle re-read 20261102 21:25 UTC, also DIS registered 2022-08-05; iso.org itself returned 403)
2. https://arxiv.org/abs/2112.06217 : Deutsch et al. (18 authors), "Graph Pattern Matching in GQL and SQL/PGQ", v1 12 Dec 2021; abstract (read 20261102 21:03 UTC)
3. https://www.gqlstandards.org/ : GQL committee page; entries of July 2022 and 16 May 2023 on SQL/PGQ, the DIS ballot, GRAPH_TABLE (first-party; read 20261102 21:03 UTC; July 2022 entry re-read 20261102 21:25 UTC)
4. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), 2024, section on graph databases: SQL:2023, Cypher, PGQL, GSQL, DuckDB (read 20261102 21:00 UTC)
5. https://arxiv.org/abs/2602.11745 : Text2GraphQuery-Bench, v1 12 Feb 2026, v2 5 Aug 2026; abstract (first-party; read 20261102 21:07 UTC)
