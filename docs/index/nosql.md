---
type: index
kind: concept
aliases: [Not Only SQL]
updated: 20261102 21:28 UTC
---

# NoSQL

NoSQL is the label for data stores that gave up parts of the relational model to scale across many servers. This entry gives the definition and the dated steps from rejecting SQL to adding it back.

## Definition

Cattell's 2010 survey says NoSQL "stands for 'Not Only SQL' or 'Not Relational'" and that the definition "is not entirely agreed upon" [1]. For his survey he gives six features, among them horizontal scaling of simple operations over many servers, a simple call-level interface instead of a SQL binding, and a concurrency model weaker than ACID transactions [1]. He names Bigtable, memcached and Dynamo as the "proof of concept" that inspired many of the systems [1].

## How it changed

- **2000s.** The inability of OLTP relational systems to scale "ushered in dozens of document DBMSs that marketed themselves using the catchphrase NoSQL", with two messages: SQL and joins are slow, and ACID transactions are unnecessary [4].
- **2006.** Google publishes Bigtable at OSDI [2]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **2007.** Amazon publishes Dynamo [3].
- **2010.** Cattell's survey appears (last revised December 2011) [1].
- **2016.** The SQL standard adds a JSON data type and operations [4]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **By the end of the 2010s.** Almost every NoSQL system had added a SQL interface, and many added ACID transactions [4].
- **2021.** MongoDB, the last holdout, adds SQL for its Atlas service [4].
- **2021 (CACM).** Gutierrez and Sequeda say the boom of non-relational stores such as CouchDB, Bigtable and Dynamo "gave rise to" the "NoSQL" databases that "(re-)popularized" column, document, key-value and graph models [5].
- **2024.** Stonebraker and Pavlo write that the message "morphed" from "Do not use SQL" to "Not only SQL", and that such systems are on a path to converge with relational ones [4].

The year the word was first used: unstated in the sources read.

## Where sources disagree

Scope. Gutierrez and Sequeda include graph databases among NoSQL's models [5]. Stonebraker and Pavlo say the word came to stand for stores of records or documents as JSON with a lower-level API and weak transactions, and they discuss graph databases in a separate section; they do not say whether graph stores belong to the label [4]. Cattell notes the term itself is not agreed [1].

## Related

[Relational model](./relational-model.md), [SQL](./sql.md), [object-oriented database](./object-oriented-database.md), [semi-structured data](./semi-structured-data.md), [Cypher](./cypher.md), [GQL](./gql.md); the project [Neo4j](../projects/neo4j.md); the trend [Infrastructure and MCP](../trends/infrastructure-and-mcp.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [The semantic web and linked data](../history/semantic-web.md)

**Index**

- [ACID](acid.md)
- [Data independence](data-independence.md)
- [Data warehouse](data-warehouse.md)
- [Embedded database](embedded-database.md)
- [Object-oriented database](object-oriented-database.md)
- [Property graph](property-graph.md)
- [Relational model](relational-model.md)
- [Semi-structured data](semi-structured-data.md)
- [SQL](sql.md)

<!-- END GENERATED: appears-in -->

## Sources

1. http://www.cattell.net/datastores/Datastores.pdf : Cattell, "Scalable SQL and NoSQL Data Stores", "originally published in 2010, last revised December 2011": abstract and overview (definition, six features, Bigtable, memcached, Dynamo) (read 20261102 20:54 UTC)
2. https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/ : Chang et al., Bigtable, 7th USENIX OSDI, 2006 (read 20261102 20:58 UTC)
3. https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store : DeCandia et al., Dynamo, 2007 (read 20261102 20:58 UTC)
4. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, "What Goes Around Comes Around... And Around...", SIGMOD Record 53(2), June 2024: document DBMSs and the NoSQL catchphrase, SQL interfaces, MongoDB 2021, JSON 2016, convergence (read 20261102 21:25 UTC)
5. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), March 2021: the "Data" paragraph of the Big Data period (read 20261102 20:57 UTC)
