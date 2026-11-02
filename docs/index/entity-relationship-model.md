---
type: index
kind: concept
aliases: [ER model, ERM, entity-relationship modeling]
updated: 20261102 21:25 UTC
---

# Entity-relationship model

The entity-relationship model is a way to describe data as things (entities) and the links between them (relationships), drawn as a diagram before a database is built. This page gives Chen's definition, dates the model and its uptake, and notes how sources frame it.

## Definition

Chen proposed "a data model, called the entity-relationship model" that "incorporates some of the important semantic information about the real world", with a diagram technique as a tool for database design [1]. The abstract adds that the model "can be used as a basis for unification of different views of data: the network model, the relational model, and the entity set model" [1].

## How it changed

- **19750922 to 19750924.** A first version is presented at the 1st International Conference on Very Large Data Bases, Framingham, Massachusetts [5]; Chen confirms the 1975 presentation [3].
- **197603.** The paper appears in *ACM Transactions on Database Systems* 1(1), pages 9-36 [1][2]. Era: [Formal foundations](../history/formal-foundations.md).
- **Late 1970s.** Chen consults on the data modelling method IDEF1 of the US Air Force's ICAM project (first-party) [3].
- **1979.** The first ER conference is held at UCLA; 250 to 300 people come where 50 were expected (first-party) [3].
- **About 1987.** ANSI adopts the model as the data model of the Information Resource Directory System standards; IBM's Repository Manager for DB2 and DEC's CDD+ were also implemented on it (first-party) [3]. Era: [Knowledge systems](../history/knowledge-systems.md).
- **2001, published 2002.** Chen writes, in a text that treats 2001 as the present year, that object-oriented analysis methods are in part based on ER concepts, but with a narrower idea of relationship; he calls this "commonly acknowledged" (first-party) [3].

## Where sources disagree

Framing. Chen presents the model as a basis for unifying the network, relational and entity set models [1]. Gutierrez and Sequeda describe it as an early attempt to link a conceptual design with a data model, "in this case the relational data model" [4]. *Reading:* the second is narrower than Chen's own claim. The dates agree: Chen's paper is March 1976 [1][2].

## Related

[Relational model](./relational-model.md), [data independence](./data-independence.md), [CODASYL](./codasyl.md), [object-oriented database](./object-oriented-database.md), [knowledge graph](./knowledge-graph.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)

**Index**

- [Entity](entity.md)
- [INGRES](ingres.md)
- [Object-oriented database](object-oriented-database.md)
- [Relational model](relational-model.md)
- [System R](system-r.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.openalex.org/works/doi:10.1145/320434.320440 : OpenAlex record of Chen, "The Entity-Relationship Model: Toward a Unified View of Data", ACM TODS 1(1), March 1976: abstract text and publication date 1976-03-01 (read 20261102 21:25 UTC). The author's PDF on a university server holds page images without text, so the body of the paper was not read
2. https://api.crossref.org/works/10.1145/320434.320440 : Crossref record: TODS vol. 1, issue 1, pages 9-36, issued 1976-03 (read 20261102 20:47 UTC)
3. http://bit.csc.lsu.edu/~chen/pdf/Chen_Pioneers.pdf : Chen, "Entity-Relationship Modeling: Historical Events, Future Trends, and Lessons Learned", Software Pioneers, Springer, 2002 (author's copy; first-party): sections 3.3, 3.4, 4.1, 4.2, 4.3 (read 20261102 20:48 UTC)
4. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, CACM 64(3), 2021, period "Data and Knowledge Foundations" (read 20261102 20:44 UTC)
5. https://api.crossref.org/works/10.1145/1282480.1282492 : Crossref record of Chen, "The entity-relationship model", in Proceedings of the 1st International Conference on Very Large Data Bases (VLDB '75), event 1975-09-22 to 1975-09-24, Framingham, Massachusetts (read 20261102 21:25 UTC)
