---
type: index
kind: concept
aliases: [relational data model]
updated: 20261102 21:30 UTC
---

# Relational model

This entry answers what the relational model is, when Codd proposed it, and how far it has spread. It also records the dispute over graph databases.

## Definition

Codd's paper opens with the aim: "Future users of large data banks must be protected from having to know how the data is organized in the machine" [1]. His model is "based on n-ary relations": a relation on n sets is "a set of n-tuples", one element from each set [1]. The data bank is "a collection of time-varying relations"; drawn as an array, each row is a tuple, row order is immaterial and all rows are distinct [1]. Codd writes that the relational view "appears to be superior in several respects to the graph or network model" then "presently in vogue" [1]. His problem is [data independence](./data-independence.md): programs unaffected by changes in data representation [1].

## How it changed

- **1970.** Codd's paper, received September 1969 and revised February 1970, appears in *Communications of the ACM* 13(6), June 1970 [1]. Era: [Formal foundations](../history/formal-foundations.md).
- **1976.** IBM's [System R](./system-r.md) and Berkeley's [INGRES](./ingres.md) are described; Gutierrez and Sequeda call them the first to implement the "vision" of the model, with query languages SEQUEL and QUEL leading to [SQL](./sql.md) [2]. Same era.
- **198706.** The first ISO edition of SQL is published, as ISO 9075:1987 [3]. Era: [Knowledge systems: boom and bust](../history/knowledge-systems.md).
- **2005 and 2024.** Stonebraker and Pavlo report that their 2005 review found the model "has dominated all comers"; in 2024 they find it "continues to be the dominant data model", with SQL taking in a JSON type (2016) and property-graph queries, [SQL/PGQ](./sql-pgq.md), in SQL:2023 [4]. Eras: [The semantic web and linked data](../history/semantic-web.md) and [What has settled since 2023](../history/settled-since-2023.md).

## Where sources disagree

**Do graph databases have a future of their own?** Stonebraker and Pavlo write: "We do not expect specialized graph DBMSs to be a large market" [4]. Angles and Gutierrez (2008) say graph models lost influence, then "the need to manage information with graph-like nature has reestablished the relevance of this area" [5]. *Reading:* the two are sixteen years apart and the later authors argue for the relational side, so this is a dispute, not a count of products.

## Related

[data independence](./data-independence.md) · [SQL](./sql.md) · [System R](./system-r.md) · [INGRES](./ingres.md) · [entity-relationship model](./entity-relationship-model.md) · [CODASYL](./codasyl.md) · [object-oriented database](./object-oriented-database.md) · [Datalog](./datalog.md) · [data warehouse](./data-warehouse.md) · [NoSQL](./nosql.md) · [property graph](./property-graph.md) · [SQL/PGQ](./sql-pgq.md) · [foundations papers](../papers/foundations.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [The semantic web and linked data](../history/semantic-web.md)
- [The Web changes data and search](../history/the-web.md)

**Index**

- [ACID](acid.md)
- [Bi-temporal model](bi-temporal-model.md)
- [Closed-world assumption](closed-world-assumption.md)
- [CODASYL](codasyl.md)
- [Data independence](data-independence.md)
- [Data warehouse](data-warehouse.md)
- [Datalog](datalog.md)
- [Entity-relationship model](entity-relationship-model.md)
- [Graph database](graph-database.md)
- [INGRES](ingres.md)
- [NoSQL](nosql.md)
- [Object-oriented database](object-oriented-database.md)
- [Schema](schema.md)
- [Semi-structured data](semi-structured-data.md)
- [SQL](sql.md)
- [SQL/PGQ](sql-pgq.md)
- [System R](system-r.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf : Codd, "A Relational Model of Data for Large Shared Data Banks", CACM 13(6), June 1970: abstract, Sections 1.1 and 1.3, received and revised dates (read 20261102 20:59 UTC; the "appears to be superior" sentence re-read 20261102 21:26 UTC)
2. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: System R and INGRES (1976) as the first to implement the "vision" (read 20261102 21:00 UTC)
3. https://committee.iso.org/es/sites/isoorg/contents/data/standard/01/66/16661.html : ISO catalogue page for ISO 9075:1987, edition 1, 1987-06, withdrawn (read 20261102 21:27 UTC; the main page https://www.iso.org/standard/16661.html returned HTTP 403 at 20261102 21:02 UTC and is the page read 20261102 20:10 UTC for the documentation page ../history/knowledge-systems.md)
4. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, "What Goes Around Comes Around... And Around...", SIGMOD Record 53(2), 2024: Section 1 (2005 conclusion), abstract, Section 2 (JSON 2016, SQL/PGQ in SQL:2023, graph DBMS market) (read 20261102 20:59 UTC)
5. https://users.dcc.uchile.cl/~cgutierr/papers/surveyGDB.pdf : Angles and Gutierrez, "Survey of Graph Database Models", ACM Computing Surveys 40(1), 2008, abstract (read 20261102 19:54 UTC, via the documentation page ../history/knowledge-graphs-at-scale.md)
