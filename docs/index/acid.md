---
type: index
kind: concept
aliases: [ACID transactions, ACID properties]
updated: 20261102 22:49 UTC
---

# ACID

This entry says what the four letters promise, where they come from, and why a database that calls itself ACID has not said how strongly it isolates concurrent work.

## Definition

Haerder and Reuter (ACM Computing Surveys 15(4), December 1983) say a transaction must have four properties [1]. Atomicity: it is of the "all-or-nothing" type. Consistency: a transaction that reaches its normal end "preserves the consistency of the database", because a successful transaction by definition commits only legal results. Isolation: events inside it "must be hidden from other transactions running concurrently". Durability: once it has committed, the results "survive any subsequent malfunctions" [1]. They name the four "atomicity, consistency, isolation, and durability (ACID)" [1].

## How it changed

- **June 1981.** Gray's Tandem report, which appeared at the Seventh International Conference on Very Large Data Bases in September, defines a transaction by three properties: atomicity, durability and consistency [2]. Era: [Knowledge systems](../history/knowledge-systems.md).
- **December 1983.** Haerder and Reuter add isolation and write the acronym [1]. The paper does not say whether the name was new: unstated.
- **June 1995.** Berenson and five co-authors (SIGMOD 1995) show that the ANSI SQL-92 isolation levels, defined by named phenomena, "fail to characterize several popular isolation levels" [3]. Era: [The Web changes data and search](../history/the-web.md).
- **May 2008.** Pritchett publishes "BASE: An Acid Alternative" (ACM Queue 6(3)); its subtitle says that in partitioned databases, trading some consistency for availability can improve scalability [4][5]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **20130201.** Bailis and five co-authors analyse which existing ACID isolation guarantees can be kept without unavailability during partitions [6]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **2024.** Stonebraker and Pavlo write that many NoSQL systems later added ACID transactions, and that NewSQL systems of the early 2010s sought NoSQL's scale while keeping the relational model and ACID transactions of older systems [5]. See [NoSQL](./nosql.md). Era: [What has settled since 2023](../history/settled-since-2023.md).

## Where sources disagree

**Three properties or four.** Gray (1981) names three; Haerder and Reuter (1983) add isolation [1][2].

**How strong "isolation" is.** The SQL standard defines four levels; only Serializable gives the effect of running transactions one at a time [7]. PostgreSQL 18 makes Read Committed the default and calls its isolation "partial" but "adequate for many applications" [7]. Berenson et al. find the standard's wording ambiguous [3]. *Reading:* the label alone does not fix the guarantee.

**Whether it is needed.** Stonebraker and Pavlo record a NoSQL message that ACID transactions were unnecessary [5]; the same paper reports the reversal above.

## Related

[NoSQL](./nosql.md) · [relational model](./relational-model.md) · [SQL](./sql.md) · [graph database](./graph-database.md) · [triple store](./triple-store.md) · [Neo4j](../projects/neo4j.md) · [Memgraph](../projects/memgraph.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Projects**

- [Memgraph](../projects/memgraph.md)

**Index**

- [Embedded database](embedded-database.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.cs.utexas.edu/~dsb/cs386d/Readings/Recovery/Principles-of-Recovery.pdf : Haerder and Reuter, "Principles of Transaction-Oriented Database Recovery", ACM Computing Surveys 15(4), December 1983: the four properties and the acronym (read 20261102 22:07 UTC)
2. https://jimgray.azurewebsites.net/papers/theTransactionConcept.pdf : Gray, "The Transaction Concept: Virtues and Limitations", Tandem TR 81.3, June 1981; abstract and the note on the VLDB 1981 proceedings (read 20261102 22:06 UTC)
3. https://arxiv.org/abs/cs/0701157 : Berenson, Bernstein, Gray, Melton, O'Neil, O'Neil, "A Critique of ANSI SQL Isolation Levels", Proc. ACM SIGMOD 95, June 1995 (arXiv 25 January 2007), abstract (read 20261102 22:07 UTC)
4. https://api.crossref.org/works/10.1145/1394127.1394128 : Pritchett, "BASE: An Acid Alternative", ACM Queue 6(3), issued 2008-05 (read 20261102 22:08 UTC)
5. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), 2024: NoSQL messages, NewSQL (section 3.4), reference [179] for the BASE subtitle (read 20261102 22:08 UTC)
6. https://arxiv.org/abs/1302.0309 : Bailis et al., "Highly Available Transactions: Virtues and Limitations", submitted 1 February 2013, abstract (read 20261102 22:07 UTC)
7. https://www.postgresql.org/docs/current/transaction-iso.html : PostgreSQL 18 documentation, "Transaction Isolation": four standard levels, Read Committed default (read 20261102 22:07 UTC)
