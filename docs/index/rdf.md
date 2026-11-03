---
type: index
kind: standard
aliases: [Resource Description Framework, RDF 1.1, RDF 1.2]
updated: 20261103 01:52 UTC
---

# RDF

This entry answers what the Resource Description Framework is and which W3C documents define it. It dates each document and says which version is current.

## Definition

The W3C's RDF 1.1 Concepts calls RDF "a framework for representing information in the Web" [1]. Its data model has two structures. RDF graphs are "sets of subject-predicate-object triples", whose elements may be IRIs, blank nodes or datatyped literals. RDF datasets organise graphs into a default graph and zero or more named graphs [1]. Hitzler describes RDF in essence as a syntax for directed, labelled and typed graphs [2]. The classes and properties of RDF data are described with [RDF Schema](./rdfs.md) [3].

## How it changed

- **19971002.** The first working draft of *RDF Model and Syntax* [4]. See [The Web changes data and search](../history/the-web.md).
- **19990222.** *RDF Model and Syntax* became a W3C Recommendation. It calls RDF "a foundation for processing metadata" [5].
- **20040210.** *RDF Concepts and Abstract Syntax* (RDF 1.0) became a Recommendation, "intended to jointly replace" the 1999 specification and the 2000 draft of RDF Schema [6]. See [The semantic web and linked data](../history/semantic-web.md).
- **20140225.** RDF 1.1 Concepts became a Recommendation. Its status section names the RDF dataset as a new concept [1]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20260407.** RDF 1.2 Concepts is a Candidate Recommendation Snapshot, not a Recommendation. It adds triple terms (a triple as the object of another triple), directional language-tagged strings and a way to state which RDF version data uses [7]. The page says it is "not expected to advance to Recommendation any earlier than 05 May 2026"; W3C's publication history, read on 20261102, shows no later step, and dates the first public working draft 20230516 [7][8]. RDF 1.1 stays the latest Recommendation [7]. Still moving: [Semantic web standards](../trends/semantic-web-standards.md).

## Where sources disagree

**When RDF became a standard.** *RDF Model and Syntax* is a Recommendation of 19990222 [5]. Hitzler writes "Also in 2004, the Ressource Description Framework (RDF) became a W3C standard" [2]; the 2004 document is the RDF 1.0 Concepts that replaced the 1999 one [6]. *Reading:* both are true of different documents; this documentation dates the first Recommendation 1999 and RDF 1.0 as the 2004 revision.

## Related

[RDF Schema](./rdfs.md) · [OWL](./owl.md) · [SPARQL](./sparql.md) · [SHACL](./shacl.md) · [JSON-LD](./json-ld.md) · [URI](./uri.md) · [linked data](./linked-data.md) · [semantic web](./semantic-web.md) · [RDF Dataset Canonicalization](./rdf-dataset-canonicalization.md) · [property graph](./property-graph.md) · [knowledge graph](./knowledge-graph.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [The semantic web and linked data](../history/semantic-web.md)
- [The Web changes data and search](../history/the-web.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Trends**

- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)
- [Semantic web standards: from RDF 1.1 and RDF-star to RDF 1.2](../trends/semantic-web-standards.md)

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Datasets**

- [YAGO](../datasets/yago.md)

**Index**

- [Closed-world assumption](closed-world-assumption.md)
- [DBpedia](dbpedia.md)
- [DCAT](dcat.md)
- [Description logic](description-logic.md)
- [Entity](entity.md)
- [JSON-LD](json-ld.md)
- [Linked data](linked-data.md)
- [LinkML](linkml.md)
- [OWL](owl.md)
- [Property graph](property-graph.md)
- [Provenance](provenance.md)
- [RDF Dataset Canonicalization](rdf-dataset-canonicalization.md)
- [RDF Schema](rdfs.md)
- [RDF-star](rdf-star.md)
- [schema.org](schema-org.md)
- [Semantic Web](semantic-web.md)
- [Semi-structured data](semi-structured-data.md)
- [SHACL](shacl.md)
- [SPARQL](sparql.md)
- [Temporal knowledge graph](temporal-knowledge-graph.md)
- [Triple](triple.md)
- [Triple store](triple-store.md)
- [URI](uri.md)
- [Wikidata](wikidata.md)
- [XML](xml.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.w3.org/TR/rdf11-concepts/ : RDF 1.1 Concepts and Abstract Syntax, W3C Recommendation 20140225: abstract, triples, datasets as a new concept (read 20261102 20:55 UTC)
2. https://par.nsf.gov/servlets/purl/10292869 : Hitzler, "A Review of the Semantic Web Field", CACM 64(2), 2021: "Also in 2004" and "a syntax for expressing directed, labelled and typed graphs" (read 20261102 20:58 UTC)
3. https://www.w3.org/TR/rdf-schema/ : RDF Schema 1.1, W3C Recommendation 20140225, abstract: "a data-modelling vocabulary for RDF data" (read 20261102 20:55 UTC)
4. https://www.w3.org/TR/WD-rdf-syntax-971002/ : RDF Model and Syntax, working draft, version 1, 19971002 (read 20261102 20:57 UTC)
5. https://www.w3.org/TR/1999/REC-rdf-syntax-19990222/ : RDF Model and Syntax Specification, W3C Recommendation 19990222 (read 20261102 20:55 UTC)
6. https://www.w3.org/TR/rdf10-concepts/ : RDF Concepts and Abstract Syntax, W3C Recommendation 20040210: "intended to jointly replace" the 1999 specification and RDF Schema (2000 Candidate Recommendation) (read 20261102 20:55 UTC)
7. https://www.w3.org/TR/rdf12-concepts/ : RDF 1.2 Concepts and Abstract Data Model, Candidate Recommendation Snapshot 20260407: status, "not expected to advance to Recommendation any earlier than 05 May 2026", changes from RDF 1.1, latest Recommendation RDF 1.1 (read 20261102 20:55 UTC)
8. https://www.w3.org/standards/history/rdf12-concepts/ : W3C publication history of RDF 1.2 Concepts: first public working draft 20230516, newest entry the 20260407 snapshot, no Proposed Recommendation or Recommendation (read 20261102 20:55 UTC)
