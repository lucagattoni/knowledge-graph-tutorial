---
type: index
kind: system
aliases: [IBM System R]
updated: 20261102 21:28 UTC
---

# System R

System R was IBM's research database system of the 1970s, built to show that Codd's relational model could work in practice. This entry says what it was, how its project ran, and what came out of it.

## Definition

System R was an experimental relational database management system built at the IBM Research Laboratory in San Jose, California [1][2]. It gave users a high-level relational interface that shielded them from storage structures ([data independence](./data-independence.md)), supported relational views, and added authorization, integrity assertions, logging, recovery and consistency for shared updates [1]. Its authors called it "a vehicle for research in database architecture, and is not planned as a product" [1]. The 1981 summary states the goal: to show that the usability advantages of the [relational model](./relational-model.md) could be had in a system with the full function and speed of everyday production use [2]. Its query language was SEQUEL, later written [SQL](./sql.md) [2].

## How it changed

- **197405.** Chamberlin and Boyce present SEQUEL at an ACM SIGMOD workshop in Ann Arbor [2].
- **1974 to 1975, "Phase Zero".** A one-user prototype of SQL on an existing access method (XRM); its code was later abandoned [2].
- **197606.** Astrahan and 13 co-authors describe the architecture in ACM Transactions on Database Systems 1(2), pages 97 to 137, while the system was "being implemented" [1]. See [Formal foundations](../history/formal-foundations.md).
- **1976 to 1977, "Phase One".** The full multi-user version was designed and built [2].
- **197706.** The first installations take place (stated in the source's Phase Two section) [2].
- **1978 to 1979, "Phase Two".** Evaluation at the San Jose laboratory, at internal IBM sites and at three customer sites, always on an experimental basis [2].
- **198110.** Chamberlin and 15 co-authors publish "A History and Evaluation of System R"; a footnote says the prototype later evolved into SQL/Data System, an IBM product [2].
- **2021.** Gutierrez and Sequeda write that System R and [INGRES](./ingres.md) "were the first to implement the 'vision' of the relational model", with query languages that "would lead to SQL" [3].

## Where sources disagree

No disagreement found in the sources read. The reason for renaming SEQUEL to SQL is **unstated** in them [2][3].

## Related

[relational model](./relational-model.md) · [SQL](./sql.md) · [INGRES](./ingres.md) · [data independence](./data-independence.md) · [entity-relationship model](./entity-relationship-model.md) · [CODASYL](./codasyl.md) · [foundation papers](../papers/foundations.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)

**Index**

- [INGRES](ingres.md)
- [Relational model](relational-model.md)
- [SQL](sql.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.crossref.org/works/10.1145/320455.320457 : Astrahan et al., "System R", ACM Transactions on Database Systems 1(2), June 1976, pages 97-137: Crossref record with the abstract (read 20261102 21:00 UTC)
2. https://people.eecs.berkeley.edu/~brewer/cs262/SystemR.pdf : Chamberlin et al., "A History and Evaluation of System R", Communications of the ACM 24(10), October 1981: summary, three phases, first installations June 1977, footnote on SQL/Data System, reference list (SEQUEL paper, Ann Arbor, May 1974) (read 20261102 21:00 UTC; phase dates and June 1977 re-read 20261102 21:26 UTC)
3. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: System R and INGRES as first implementations of the relational vision (read 20261102 21:00 UTC)
