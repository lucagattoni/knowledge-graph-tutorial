---
type: index
kind: system
aliases: [Actian Ingres]
updated: 20261102 21:22 UTC
---

# INGRES

This entry says what INGRES was, who built it, and what it led to. It is one of the two first implementations of the relational model, next to IBM's [System R](./system-r.md) [5].

## Definition

INGRES is a relational database management system built at the University of California, Berkeley, by Michael Stonebraker, Eugene Wong, Peter Kreps and Gerald Held. The paper that describes it, in *ACM Transactions on Database Systems* 1(3), September 1976, covers the version operational in March 1976: a multiuser system with a relational view of data and two high-level, nonprocedural query sublanguages, running on UNIX on PDP-11 computers. The authors discuss design trade-offs in process structure, access methods, concurrency and recovery, and system catalogs [1][2][3].

## How it changed

- **1976.** Berkeley issues the report UCB/ERL M577, "The Design and Implementation of Ingres"; the page shows the year 1976 and its BibTeX record gives January [3]. See [formal foundations](../history/formal-foundations.md).
- **197609.** The journal version appears, pages 189 to 222 [1].
- **2021 (a retrospective).** Gutierrez and Sequeda write that System R and INGRES "were the first to implement the 'vision' of the relational model", with the query languages SEQUEL and QUEL, which led to [SQL](./sql.md) [5]. The vision is Codd's [relational model](./relational-model.md).
- **1986.** Stonebraker and Rowe present POSTGRES at SIGMOD '86 as "the successor to the INGRES relational database system" [4]. The PostgreSQL project dates the start of the POSTGRES implementation to 1986 and the addition of an SQL interpreter to 1994 [6]. See [knowledge systems](../history/knowledge-systems.md).
- **2026 (read 20261102).** Actian sells a product called Ingres; its page says the product "includes the product formerly known as Actian X" and gives no founding year [7].
- **Unstated in the sources read:** when work on INGRES began, when QUEL was first defined, and the date of the first commercial release.

## Where sources disagree

No disagreement found in the sources read. The Berkeley report and the Crossref record of the journal paper list the same four authors in different orders [1][3]; the report is dated 1976 (January in its BibTeX record) and the journal paper September 1976, which are two publications of one system, not two dates for one event.

## Related

[System R](./system-r.md), [relational model](./relational-model.md), [SQL](./sql.md), [data independence](./data-independence.md), [entity-relationship model](./entity-relationship-model.md), [CODASYL](./codasyl.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)

**Index**

- [Relational model](relational-model.md)
- [SQL](sql.md)
- [System R](system-r.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.crossref.org/works/10.1145/320473.320476 : Stonebraker, Held, Wong, Kreps, "The design and implementation of INGRES", ACM TODS 1(3), 189-222, September 1976; abstract (read 20261102 20:47 UTC)
2. https://api.openalex.org/works/doi:10.1145/320473.320476 : same paper, publication date, UNIX on PDP-11, design trade-offs (read 20261102 20:47 UTC)
3. https://www2.eecs.berkeley.edu/Pubs/TechRpts/1976/29338.html : Berkeley technical report UCB/ERL M577, dated 1976 (BibTeX month: Jan), authors Stonebraker, Wong, Kreps, Held (read 20261102 20:47 UTC, re-read 20261102 21:22 UTC)
4. https://api.openalex.org/works/doi:10.1145/16894.16888 : Stonebraker and Rowe, "The design of POSTGRES", SIGMOD 1986; the abstract's first words (read 20261102 20:48 UTC)
5. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021, the passage on System R and INGRES (read 20261102 21:22 UTC, re-read from the PDF text)
6. https://www.postgresql.org/docs/current/history.html : PostgreSQL documentation, history: POSTGRES implementation began 1986, SQL interpreter added 1994; the page does not mention INGRES (read 20261102 20:47 UTC)
7. https://www.actian.com/databases/ingres/ : Actian product page, footer 2026 (read 20261102 20:48 UTC)
