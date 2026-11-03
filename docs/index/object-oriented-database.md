---
type: index
kind: concept
aliases: [OODB, OODBS, object database]
updated: 20261102 21:30 UTC
---

# Object-oriented database

An object-oriented database stores objects, with identity and inheritance, instead of rows in tables. This entry gives the defining paper, the dated steps of its rise, and what later sources say of its outcome.

## Definition

"The Object-Oriented Database System Manifesto" (Atkinson, Bancilhon, DeWitt, Dittrich, Maier, Zdonik) tries to define such a system by the features it must have [1]. The mandatory ones are complex objects, object identity, encapsulation, types or classes, inheritance, overriding with late binding, extensibility, computational completeness, persistence, secondary storage management, concurrency, recovery and an ad hoc query facility [1]. The authors tie the interest to design-support applications such as CAD and CASE [2].

## How it changed

- **1970.** Codd's paper gave a clear specification of a relational system; the manifesto's authors say no such specification existed for object-oriented ones [2].
- **1980s.** Gutierrez and Sequeda say the relational revolution's separation of programs from data created the need to combine object-oriented languages with databases. Research systems included Encore-Observer, EXODUS, IRIS, ODE, ORION and Zeitgeist, and "led to several commercial offerings" [3]. Era: [Knowledge systems: boom and bust](../history/knowledge-systems.md).
- **1990 (record date).** The manifesto is printed in the proceedings volume "Deductive and Object-Oriented Databases" (Crossref: issued 1990). Its newest references date from 1989; its own date is not printed on the page read [4][5]. It names three traits of the field: no common data model, no formal foundations, strong experimental activity [2].
- **2005.** A chapter co-written by one of the 2024 paper's authors concluded that the relational model with an extendable type system (object-relational) "has dominated all comers" [6].
- **2024.** Stonebraker and Pavlo place the object-oriented movement in the late 1980s and early 1990s, and write that document DBMSs are "essentially the same as object-oriented DBMSs from the 1980s", making the same argument about the impedance mismatch with relational storage [6]. See [NoSQL](./nosql.md).

## Where sources disagree

No disagreement found in the sources read. The two later sources answer different questions. Stonebraker and Pavlo judge the market fate of the non-relational systems covered in 2005: they say those systems are in "legacy maintenance mode" and nobody is building new applications on them [6]. Gutierrez and Sequeda describe which features entered data research: objects, identifiers, relationships and inheritance, features that "would become central in the future of data" [3].

## Related

[Relational model](./relational-model.md), [SQL](./sql.md), [NoSQL](./nosql.md), [semi-structured data](./semi-structured-data.md), [data independence](./data-independence.md), [entity-relationship model](./entity-relationship-model.md), [CODASYL](./codasyl.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Knowledge systems: boom and bust](../history/knowledge-systems.md)

**Index**

- [Entity-relationship model](entity-relationship-model.md)
- [NoSQL](nosql.md)
- [Relational model](relational-model.md)
- [Semi-structured data](semi-structured-data.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.cs.cmu.edu/~clamen/OODBMS/Manifesto/htManifesto/Manifesto.html : Atkinson et al., "The Object-Oriented Database System Manifesto": authors and abstract (mandatory, optional and open features) (read 20261102 20:54 UTC)
2. https://www.cs.cmu.edu/~clamen/OODBMS/Manifesto/htManifesto/node1.html : the same paper, introduction (three traits of the field, comparison with Codd 1970, design-support applications) (read 20261102 20:57 UTC)
3. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: the 1980s "Data" paragraph (read 20261102 20:57 UTC)
4. https://api.crossref.org/works?query.bibliographic=The+Object-Oriented+Database+System+Manifesto+Atkinson+Bancilhon&rows=3 : Crossref record of the manifesto (DOI 10.1016/b978-0-444-88433-6.50020-4), issued 1990, container "Deductive and Object-Oriented Databases", Elsevier (read 20261102 20:58 UTC)
5. https://www.cs.cmu.edu/~clamen/OODBMS/Manifesto/htManifesto/node30.html : the same paper, references (newest entries of 1989) (read 20261102 20:57 UTC)
6. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), June 2024: introduction (movements by decade; 2005 conclusion; legacy maintenance mode) and the document-DBMS discussion (read 20261102 20:57 UTC; the legacy-maintenance wording re-read 20261102 21:25 UTC)
