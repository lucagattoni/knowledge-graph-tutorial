---
type: index
kind: concept
aliases: [data warehousing, enterprise data warehouse]
updated: 20261102 21:23 UTC
---

# Data warehouse

A data warehouse is a store that integrates data from many operational systems and keeps it for analysis and reporting. Enterprises built them from the mid-1990s. This entry gives the definition and the dated change from row stores to column stores and lakehouses.

## Definition

Chaudhuri and Dayal (SIGMOD Record 26(1), March 1997) quote the definition of Inmon (1992): a data warehouse is a "subject-oriented, integrated, time-varying, non-volatile collection of data that is used primarily in organizational decision making". It is typically kept apart from the operational databases and serves on-line analytical processing (OLAP), whose workloads differ from the transaction processing (OLTP) of operational systems [1][2]. The same authors use "data warehousing" for the wider set of decision-support technologies around it [1].

## How it changed

- **1992.** Inmon's *Building the Data Warehouse* is the source of the definition above [1].
- **Mid-1990s.** Enterprises, retailers first, begin collecting customer-facing sales data into historical warehouses (Stonebraker and Pavlo) [3]. Era: [The Web changes data and search](../history/the-web.md).
- **1997.** Chaudhuri and Dayal cite the META Group projection of a market growing from 2 billion US dollars in 1995 to 8 billion in 1998 [1].
- **Last two decades to 2024.** All vendors active in the warehouse market converted from row stores to column stores; Stonebraker and Pavlo say column stores "have taken over the data warehouse marketplace" [3].
- **2021.** Armbrust, Ghodsi, Xin and Zaharia (Databricks) argue that the warehouse architecture "will wane" and give way to the lakehouse, built on open file formats such as Parquet (first-party: Databricks authors) [4].
- **2024.** Stonebraker and Pavlo describe a move toward data lakes on object stores. Middleware such as Delta Lake, Iceberg and Hudi "make lakehouses look more like a traditional data warehouse", and legacy vendors added reads from object stores [3].

## Where sources disagree

The future of the warehouse. Armbrust et al. predict that the architecture will be replaced [4]. Stonebraker and Pavlo report that lake systems are acquiring warehouse features, and that warehouse vendors are reading from lakes [3]. *Reading:* the sources agree on the direction (open formats, separated storage) and differ on whether the result is still a warehouse. The term also has two scopes: a database [1] and the set of technologies around it [1].

## Related

[Relational model](./relational-model.md), [SQL](./sql.md), [NoSQL](./nosql.md), [data independence](./data-independence.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [The Web changes data and search](../history/the-web.md)

**Index**

- [Relational model](relational-model.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/sigrecord.pdf : Chaudhuri and Dayal, "An overview of data warehousing and OLAP technology": Inmon definition, OLTP against OLAP, META Group projection, reference list (read 20261102 20:46 UTC)
2. https://doi.org/10.1145/248603.248616 : Crossref record of the same paper: ACM SIGMOD Record 26(1), pages 65-74, March 1997 (read 20261102 20:46 UTC)
3. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), 2024, sections 3.1 and 3.3: warehouse origins, column stores, data lakes and lakehouses (read 20261102 20:45 UTC)
4. https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf : Armbrust et al., "Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics", CIDR 2021, abstract and introduction (read 20261102 20:51 UTC)
