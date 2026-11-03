---
type: index
kind: concept
aliases: [physical data independence]
updated: 20261102 21:23 UTC
---

# Data independence

Data independence means that programs and users are shielded from how data is physically organised, so the storage can change without rewriting the programs. It was the stated motivation of Codd's 1970 paper on the relational model. This entry gives the definition and how the idea was used afterwards.

## Definition

Codd's abstract says future users of large data banks "must be protected from having to know how the data is organized in the machine", and that terminal activities and most application programs "should remain unaffected" when the internal representation changes [1]. In the introduction he names the problem: "data independence-the independence of application programs and terminal activities from growth in data types and changes in data representation" [1]. A current textbook states one half of it: "Physical Data Independence – the ability to modify the physical schema without changing the logical schema" [2]. *Reading:* taken together, the term covers any change below the level the programs use, such as storage layout, indexes or access paths.

## How it changed

- **June 1970.** Codd's CACM paper 13(6) argues that the relational view gives "maximal independence" between programs and the machine representation [1][3]. It lists three dependencies still to remove from existing systems: ordering, indexing and access path [1]. He credits C. T. Davies of IBM with convincing him of the need for data independence [1]. Era: [Formal foundations](../history/formal-foundations.md). The [Advent](../history/advent.md) page lists programs tied to storage layout among what the era left unsolved.
- **2024.** Stonebraker and Pavlo argue that higher-level languages are preferred because they "require less code and provide greater data independence", and that denormalisation and prejoining, "an old topic that dates back to the 1970s", have "no data independence" [5]. See [SQL](./sql.md) and [NoSQL](./nosql.md).

Unstated: when the split between physical and logical levels began. A 1978 report on the ANSI/X3/SPARC DBMS framework by Tsichritzis and Klug exists (Information Systems 3(3)), but only its Crossref record was read, not its text [4].

## Where sources disagree

No disagreement found in the sources read. They define the idea at different levels of detail: Codd by what is shielded [1], the textbook by schema layer [2].

## Related

[Relational model](./relational-model.md), [SQL](./sql.md), [CODASYL](./codasyl.md), [NoSQL](./nosql.md). Papers: [foundations group](../papers/foundations.md) (Codd 1970).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [The advent: machines that hold knowledge](../history/advent.md)

**Index**

- [CODASYL](codasyl.md)
- [Data warehouse](data-warehouse.md)
- [Entity-relationship model](entity-relationship-model.md)
- [INGRES](ingres.md)
- [Object-oriented database](object-oriented-database.md)
- [Relational model](relational-model.md)
- [Schema](schema.md)
- [SQL](sql.md)
- [System R](system-r.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf : Codd, "A Relational Model of Data for Large Shared Data Banks", CACM 13(6), June 1970: abstract, Section 1.1, Section 1.2, acknowledgment (read 20261102 20:45 UTC)
2. https://www.db-book.com/slides-dir/PDF-dir/ch1.pdf : Silberschatz, Korth, Sudarshan, Database System Concepts 7th ed., chapter 1 slides: physical data independence (read 20261102 20:51 UTC)
3. https://doi.org/10.1145/362384.362685 : Crossref record of Codd 1970: CACM 13(6), pages 377-387, June 1970 (read 20261102 20:46 UTC)
4. https://doi.org/10.1016/0306-4379(78)90001-7 : Crossref record: Tsichritzis and Klug, "The ANSI/X3/SPARC DBMS framework report of the study group on database management systems", Information Systems 3(3), 1978; metadata only, text not read (read 20261102 20:51 UTC)
5. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), 2024: data independence, prejoining (read 20261102 20:45 UTC)
