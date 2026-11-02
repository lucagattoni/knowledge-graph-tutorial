---
type: index
kind: standard
aliases: [Structured Query Language, ISO/IEC 9075, SEQUEL]
updated: 20261102 21:26 UTC
---

# SQL

SQL is the standard language of relational databases. This entry gives the definition, the IBM origin, the ISO editions and the additions of 2016 and 2023.

## Definition

ISO/IEC 9075, "Database languages SQL", is a multi-part standard. Part 1 describes "the conceptual framework used in other parts of the ISO/IEC 9075 series", which specify the grammar of SQL and the result of processing its statements [1]. Part 2, in its 2016 edition, "defines the data structures and basic operations on SQL-data" [2]. The language began as SEQUEL, the Structured English Query Language, at IBM San Jose Research, adapted from an earlier notation, SQUARE (Specifying Queries as Relational Expressions), which Chamberlin sets against Codd's relational algebra and calculus [3][4].

## How it changed

- **1973 to 1976.** Don Chamberlin and Ray Boyce devise SQUARE at Yorktown, in a "Query Game" about ways to express complicated queries; the group transfers to San Jose in 1973. The date of SQUARE is **unstated**. SEQUEL follows, with a working prototype shown on tape in 1976 [3][4]. Their paper "SEQUEL" is in the proceedings dated 1976 [5]. See [System R](./system-r.md). Era: [Formal foundations](../history/formal-foundations.md).
- **Date unstated.** SEQUEL is renamed SQL after a legal challenge; Chamberlin recalls dropping the vowels [4].
- **198706.** ISO 9075:1987, edition 1, published [6]. **198904.** ISO/IEC 9075:1989, "SQL with integrity enhancement", edition 2 [7]. **199211.** ISO/IEC 9075:1992, edition 3, 587 pages [8]. Era: [Knowledge systems](../history/knowledge-systems.md).
- **Between 1992 and 2016.** The ISO catalogue says the 1992 edition was revised by the multi-part series ISO/IEC 9075-1 to 9075-5:1999 [8]. The other editions between 1992 and 2016 were not read and are **unstated** here, so this list is not complete.
- **201612.** ISO/IEC 9075-1:2016 and 9075-2:2016, edition 5 [2][9]. Stonebraker and Pavlo say the standard added JSON in 2016 [10].
- **Late 2010s.** Almost every [NoSQL](./nosql.md) system adds SQL; MongoDB, the last holdout, does so for Atlas in 2021 [10]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **202306.** ISO/IEC 9075-1:2023 and 9075-2:2023, edition 6, published 20230601 per the Part 1 page; Part 1 lists Part 16, [SQL/PGQ](./sql-pgq.md), among its references [1][11]. Era: [What has settled since 2023](../history/settled-since-2023.md).
- **2026.** Corrigendum 1:2026 to 9075-1:2023 is published; a committee draft of a replacement is in development; days **unstated** [1].

## Where sources disagree

- **What SQL stands for.** The sources read expand SEQUEL, not SQL [4]. The expansion is **unstated**.
- **Who challenged the name.** Chamberlin says "I believe" it was Hawker Siddeley Aircraft; no second source was read [4].
- **First use of SEQUEL.** The date the name first appeared is **unstated**; the proceedings are dated 1976 [5]. The date of SQUARE is **unstated** [3].
- **ANSI.** No primary record of ANSI's adoption was read; its date is **unstated**.

## Related

[relational model](./relational-model.md), [System R](./system-r.md), [INGRES](./ingres.md), [data independence](./data-independence.md), [CODASYL](./codasyl.md), [NoSQL](./nosql.md), [SQL/PGQ](./sql-pgq.md), [GQL](./gql.md), [SPARQL](./sparql.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [The semantic web and linked data](../history/semantic-web.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Index**

- [ACID](acid.md)
- [Bi-temporal model](bi-temporal-model.md)
- [Cypher](cypher.md)
- [Data independence](data-independence.md)
- [Data warehouse](data-warehouse.md)
- [Datalog](datalog.md)
- [Embedded database](embedded-database.md)
- [GQL](gql.md)
- [INGRES](ingres.md)
- [NoSQL](nosql.md)
- [Object-oriented database](object-oriented-database.md)
- [Relational model](relational-model.md)
- [Semantic parsing](semantic-parsing.md)
- [SPARQL](sparql.md)
- [SQL/PGQ](sql-pgq.md)
- [System R](system-r.md)
- [Text-to-query](text-to-query.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://committee.iso.org/es/sites/isoorg/contents/data/standard/07/65/76583.html : ISO catalogue page for ISO/IEC 9075-1:2023 (Spanish-language page; scope text, edition 6, 2023-06-01 published, normative references including Part 16, Cor 1:2026, ISO/IEC CD 9075-1) (read 20261102 21:00 UTC; iso.org itself returned 403)
2. https://committee.iso.org/es/sites/isoorg/contents/data/standard/06/35/63556.html : ISO catalogue page for ISO/IEC 9075-2:2016: edition 5, 2016-12, abstract (read 20261102 21:02 UTC)
3. https://www.mcjones.org/System_R/SQL_Reunion_95/sqlr95-Prehisto.html : "The 1995 SQL Reunion", Chamberlin on the Query Game, SQUARE (no year given), Yorktown in 1971 and the transfer to San Jose in 1973; first-hand transcript (read 20261102 21:02 UTC; re-read 20261102 21:25 UTC)
4. https://www.mcjones.org/System_R/SQL_Reunion_95/sqlr95-System.html : same transcript: SEQUEL as Structured English Query Language, prototype tape of 1976, the rename to SQL (read 20261102 21:02 UTC)
5. https://api.crossref.org/works/10.1145/800296.811515 : Crossref record: Chamberlin and Boyce, "SEQUEL: A structured English query language", proceedings FIDET '76, ACM, 1976, pages 249-264 (read 20261102 21:01 UTC)
6. https://committee.iso.org/es/sites/isoorg/contents/data/standard/01/66/16661.html : ISO catalogue page for ISO 9075:1987: edition 1, 1987-06 (read 20261102 21:01 UTC)
7. https://committee.iso.org/es/sites/isoorg/contents/data/standard/01/66/16662.html : ISO catalogue page for ISO/IEC 9075:1989: edition 2, 1989-04 (read 20261102 21:01 UTC)
8. https://committee.iso.org/es/sites/isoorg/contents/data/standard/01/66/16663.html : ISO catalogue page for ISO/IEC 9075:1992: edition 3, 1992-11, 587 pages; withdrawn 1999-12-16, revised by ISO/IEC 9075-1 to 9075-5:1999 (read 20261102 21:01 UTC; the withdrawal and 1999 series re-read 20261102 21:25 UTC)
9. https://committee.iso.org/es/sites/isoorg/contents/data/standard/06/35/63555.html : ISO catalogue page for ISO/IEC 9075-1:2016: edition 5, 2016-12 (read 20261102 21:02 UTC)
10. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), 2024: SQL interfaces on NoSQL systems, MongoDB 2021, JSON in 2016 (read 20261102 21:00 UTC)
11. https://committee.iso.org/es/sites/isoorg/contents/data/standard/07/65/76584.html : ISO catalogue page for ISO/IEC 9075-2:2023: edition 6, 2023-06 (read 20261102 21:01 UTC)
