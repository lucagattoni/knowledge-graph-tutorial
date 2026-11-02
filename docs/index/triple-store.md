---
type: index
kind: concept
aliases: [triplestore, RDF store, RDF database]
updated: 20261102 22:51 UTC
---

# Triple store

This entry says what a triple store is, how the sources name it, and the dated steps from early open frameworks to the 2026 replacement of Wikidata's query engine.

## Definition

A triple store is a database for RDF data, whose stored unit is the [triple](./triple.md). Stonebraker and Pavlo write that "RDF databases (aka triplestores) only model a directed graph with labeled edges" [1]. The SPARQL specification speaks of RDF data stores that hold several RDF graphs [5]. Hogan et al. name one storage design: a single relation of arity three, a triple table [8]. Apache Jena stores RDF triples in memory or on disk [3]; Eclipse RDF4J has an in-memory and a native store [4].

## How it changed

- **2000.** Jena begins at HP Labs in Bristol [3]. Era: [The Web changes data and search](../history/the-web.md).
- **20080115.** SPARQL 1.0, the query language for RDF, becomes a W3C Recommendation [5]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **201108.** Franz reports loading 1 trillion triples into AllegroGraph; vendor-reported, on a W3C wiki page [2].
- **201204.** Jena graduates as an Apache top-level project, after incubation from November 2010 [3].
- **20130321.** SPARQL 1.1 becomes a Recommendation [6]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **201409.** Oracle reports 1.08 trillion triples loaded, inferred and queried on the LUBM benchmark; vendor-reported, on the same W3C wiki page [2].
- **2026.** Wikidata's query service, powered by Blazegraph since its launch, is moving to QLever. Wikimedia says Blazegraph "has gone unmaintained since 2018", records a QLever proposal of May 2026, and aims to decommission the Blazegraph endpoint on 20270630 (first-party) [7]. See [Wikidata](./wikidata.md).

## Where sources disagree

**Name and category.** Stonebraker and Pavlo write "triplestores" [1], the SPARQL specification "RDF data stores" [5], the W3C wiki "triple stores" [2]. Stonebraker and Pavlo place RDF databases among [graph databases](./graph-database.md) but discuss only property graphs, "more common" and "a superset of RDF" [1]; QLever's repository calls itself a "Graph database implementing the RDF and SPARQL standards" [9]. *Reading:* the sources read agree on the category, not on the word.

**When Blazegraph stopped.** Wikimedia says unmaintained since 2018 [7]; its GitHub repository is archived, with a last push on 20230416 [10]. The sources do not say what the later pushes were.

## Related

[Triple](./triple.md), [RDF](./rdf.md), [SPARQL](./sparql.md), [graph database](./graph-database.md), [property graph](./property-graph.md), [linked data](./linked-data.md), [Wikidata](./wikidata.md). Data: [Wikidata](../datasets/wikidata.md). Project: [Neo4j](../projects/neo4j.md). Trends: [graph query generation](../trends/graph-query-generation.md), [Infrastructure and MCP](../trends/infrastructure-and-mcp.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)

**Index**

- [ACID](acid.md)
- [Graph database](graph-database.md)
- [RDF-star](rdf-star.md)
- [Triple](triple.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, "What Goes Around Comes Around... And Around...", SIGMOD Record 53(2), 2024, section 2.8: RDF databases (aka triplestores) (read 20261102 22:12 UTC)
2. https://www.w3.org/wiki/LargeTripleStores : W3C Wiki, "LargeTripleStores", last edited 13 February 2025: vendor-reported deployments, AllegroGraph (August 2011), Oracle (September 2014) (first-party claims by vendors; read 20261102 22:12 UTC)
3. https://jena.apache.org/about_jena/about.html : Apache Jena, "What is Jena?": storage, HP Labs 2000, incubation November 2010, top-level project April 2012 (first-party; read 20261102 22:14 UTC)
4. https://rdf4j.org/about/ : Eclipse RDF4J, "About": memory store, native store, third-party triplestores (first-party; read 20261102 22:14 UTC)
5. https://www.w3.org/TR/rdf-sparql-query/ : SPARQL Query Language for RDF, W3C Recommendation 15 January 2008: "RDF data stores" (read 20261102 22:15 UTC)
6. https://www.w3.org/TR/sparql11-query/ : SPARQL 1.1 Query Language, W3C Recommendation 21 March 2013 (read 20261102 22:15 UTC)
7. https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/WDQS_backend_update/Learn : Wikimedia, WDQS backend migration from Blazegraph to QLever: motivation, May 2026 proposal, timeline to 30 June 2027; page last edited 26 October 2026 (first-party; read 20261102 22:14 UTC)
8. https://ar5iv.labs.arxiv.org/html/2003.02320 : Hogan et al., "Knowledge Graphs" (arXiv 2003.02320, ar5iv rendering; version shown unstated), section 2.1.6, graph stores and the triple table (read 20261102 22:12 UTC)
9. https://github.com/ad-freiburg/qlever : QLever repository description through the GitHub API (first-party; read 20261102 22:15 UTC)
10. https://github.com/blazegraph/database : repository metadata through the GitHub API: archived, last push 2023-04-16 (read 20261102 22:09 UTC)
