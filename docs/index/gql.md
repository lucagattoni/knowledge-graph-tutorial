---
type: index
kind: standard
aliases: [Graph Query Language, ISO/IEC 39075]
updated: 20261102 23:12 UTC
---

# GQL

GQL is the ISO standard for querying and managing property graphs. This entry says what the standard defines, how it was made and what has changed since publication. Whether products implement it is not established by the sources read.

## Definition

ISO/IEC 39075:2024, "Information technology — Database languages — GQL", "defines data structures and basic operations on property graphs". It specifies the syntax and semantics of a data management language for creating, querying, maintaining and controlling [property graphs](./property-graph.md), as a vehicle for portability among implementations. It is edition 1, 610 pages, from ISO/IEC JTC 1/SC 32 [1].

## How it changed

- **Early 2017.** Members of ISO SC32/WG3 raise the idea of a standalone graph query language to complement SQL; a manifesto follows in May 2018 [2].
- **20190910.** ISO registers the project [1]. The committee page dates its start to September 2019 [2]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **July 2022.** The committee says graph pattern matching in [SQL/PGQ](./sql-pgq.md) is "essentially identical" to that of GQL; in May 2023 it says it kept the two "as identical as possible" [2].
- **20211212.** Deutsch et al. (18 authors) publish "Graph Pattern Matching in GQL and SQL/PGQ", on the pattern language the two share [3].
- **2023 to 2024.** The draft passes two ballots: a 12-week DIS vote from 20230524 to 20230817, then an 8-week FDIS vote from 20240126 to 20240323 [1].
- **20240412 and 20240417.** ISO's lifecycle table lists "International Standard published" (stage 60.60) on 20240412, and the IEC web store gives that day as the publication date [1][4]. The committee announces on 20240417 that ISO/IEC 39075:2024 "is officially published" [2]. Era: [What has settled since 2023](../history/settled-since-2023.md).
- **2026.** ISO lists Corrigendum 1:2026 as published, and a committee draft of a replacement, ISO/IEC CD 39075, in development. Their days are **unstated** on the page [1].

The committee's page has no entry for 2025 or 2026 [2]. Product conformance is **unstated**; see [infrastructure and MCP](../trends/infrastructure-and-mcp.md) and [asking graphs in natural language](../trends/graph-query-generation.md).

## Where sources disagree

The publication date differs by source: ISO's lifecycle table and the IEC web store, 2024-04-12 [1][4]; the committee's announcement, 17 April [2]; a JTC 1 news item, 18 April [5]; openCypher, "published (April 11, 2024)", with no source given [6]. *Reading:* ISO's record is the publication. The committee's entry of 29 March said it did not yet know the date, so 17 April is an announcement [2]; what the openCypher date marks is **unstated**. The DIS ballot runs 20230524 to 20230817 in ISO's table [1] and 20230523 to 20230815 in the committee's entry [2]. The committee's home text still calls GQL "upcoming" and "currently being created" [2].

## Related

[Cypher](./cypher.md), [SQL](./sql.md), [SQL/PGQ](./sql-pgq.md), [property graph](./property-graph.md). Pages: [infrastructure and MCP](../trends/infrastructure-and-mcp.md), [asking graphs in natural language](../trends/graph-query-generation.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Trends**

- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Index**

- [Cypher](cypher.md)
- [Graph database](graph-database.md)
- [NoSQL](nosql.md)
- [Property graph](property-graph.md)
- [SPARQL](sparql.md)
- [SQL](sql.md)
- [SQL/PGQ](sql-pgq.md)
- [Text-to-query](text-to-query.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://committee.iso.org/es/sites/isoorg/contents/data/standard/07/61/76120.html : ISO catalogue page for ISO/IEC 39075:2024 (Spanish-language page; scope text, edition 1, 2024-04, lifecycle table with 2019-09-10, 2023-05-24, 2023-08-17, 2024-01-26, 2024-03-23, 2024-04-12; Cor 1:2026; ISO/IEC CD 39075) (read 20261102 21:14 UTC; the lifecycle table re-read 20261102 22:52 UTC; iso.org itself returned 403)
2. https://www.gqlstandards.org/ : GQL committee page; entries of September 2019, July 2022, 16 May 2023, 17 April 2024; no 2025 or 2026 entry (first-party; read 20261102 20:47 UTC; the entries of 17 April and 29 March 2024 re-read 20261102 22:52 UTC)
3. https://arxiv.org/abs/2112.06217 : Deutsch et al. (18 authors), "Graph Pattern Matching in GQL and SQL/PGQ", v1 20211212; abstract (read 20261102 20:47 UTC)
4. https://webstore.iec.ch/publication/94107 : IEC web store, ISO/IEC 39075:2024, edition 1.0, publication date 2024-04-12, 610 pages (read 20261102 22:52 UTC)
5. https://jtc1info.org/slug/gql-database-language/ : JTC 1 news item "GQL Database Language", dated April 18, 2024, on the publication of ISO/IEC 39075:2024 (read 20261102 22:52 UTC)
6. https://opencypher.org/ : openCypher site (first-party for openCypher): "ISO/IEC 39075 GQL published (April 11, 2024)" (read 20261102 22:52 UTC)
