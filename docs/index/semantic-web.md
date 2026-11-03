---
type: index
kind: concept
aliases: [Web of Data]
updated: 20261103 01:52 UTC
---

# Semantic Web

This entry answers what the Semantic Web is and when it started. It lists the dated steps from the first RDF draft to the RDF 1.2 candidate. It also records that the sources do not agree on what the field covers.

## Definition

The W3C's Semantic Web Activity page says the Semantic Web "provides a common framework that allows data to be shared and reused across application, enterprise, and community boundaries", based on [RDF](./rdf.md). It describes it as a web of data, built from common formats for combining data and a language for recording how the data relates to real-world objects [1]. Hitzler adds the original vision: the Web enhanced with machine-understandable information and intelligent agents. He traces that vision to the May 2001 *Scientific American* article by Berners-Lee, Hendler and Lassila, which "arguably marks the birth of the field" [2].

## How it changed

- **1997.** A first draft of RDF is published [2].
- **200105.** The *Scientific American* article appears [1][2]. See [The semantic web and linked data](../history/semantic-web.md).
- **19990222.** The RDF Model and Syntax Specification becomes a W3C Recommendation [9]. The [RDF](./rdf.md) entry covers the 1999 versus 2004 dating.
- **20040210.** RDF Concepts and Abstract Syntax (RDF 1.0) and the [OWL](./owl.md) overview become W3C Recommendations [3][4].
- **20060727.** Berners-Lee's [Linked Data](./linked-data.md) note says the Semantic Web "is about making links, so that a person or machine can explore the web of data" [5].
- **20080115.** [SPARQL](./sparql.md) becomes a W3C Recommendation [6].
- **20110602.** [schema.org](./schema-org.md) is announced; Hitzler counts it in his second phase [2][7].
- **201312.** The W3C subsumes its Semantic Web Activity into the Data Activity; the page was frozen on 20131211 [1]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **2020 (CACM 2021).** Hitzler groups the field into three overlapping phases, driven by [ontologies](./ontology.md), then linked data, then [knowledge graphs](./knowledge-graph.md) [2].
- **20260407.** RDF 1.2 Concepts is a W3C Candidate Recommendation Snapshot, not yet a Recommendation; it adds triple terms [8]. Still moving: [Semantic web standards](../trends/semantic-web-standards.md).

## Where sources disagree

**What the field is.** Hitzler gives three views and says there is "no clear consensus": building the Semantic Web as an artifact with agents; sharing and integrating data, with or without the Web; or the narrower study of ontologies, linked data and knowledge graphs on RDF, OWL and SPARQL [2]. The W3C page stresses the web of data and does not mention agents [1].

**When it starts.** Hitzler dates the first RDF draft to 1997 but starts his story in the early 2000s, with the 2001 article as the birth [2].

**When RDF became a standard.** The RDF Model and Syntax Specification is a W3C Recommendation of 19990222 [9]; RDF Concepts and Abstract Syntax (RDF 1.0) is a separate Recommendation of 20040210 [3]. The timeline above lists both.

## Related

[RDF](./rdf.md) · [RDFS](./rdfs.md) · [OWL](./owl.md) · [SPARQL](./sparql.md) · [JSON-LD](./json-ld.md) · [linked data](./linked-data.md) · [ontology](./ontology.md) · [semantic network](./semantic-network.md) · [schema.org](./schema-org.md) · [knowledge graph](./knowledge-graph.md) · [DBpedia](./dbpedia.md) · [Wikidata](./wikidata.md) · [foundation papers](../papers/foundations.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [The advent: machines that hold knowledge](../history/advent.md)
- [The semantic web and linked data](../history/semantic-web.md)
- [The Web changes data and search](../history/the-web.md)

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Index**

- [DBpedia](dbpedia.md)
- [Description logic](description-logic.md)
- [Freebase](freebase.md)
- [Google Knowledge Graph](google-knowledge-graph.md)
- [JSON-LD](json-ld.md)
- [Linked data](linked-data.md)
- [Ontology](ontology.md)
- [OWL](owl.md)
- [RDF](rdf.md)
- [RDF Schema](rdfs.md)
- [schema.org](schema-org.md)
- [Semantic network](semantic-network.md)
- [SPARQL](sparql.md)
- [URI](uri.md)
- [XML](xml.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.w3.org/2001/sw/ : W3C Semantic Web Activity homepage, frozen 20131211, subsumed by the Data Activity in December 2013: definition, article listing (read 20261102 20:57 UTC)
2. https://par.nsf.gov/servlets/purl/10292869 : Hitzler, "Semantic Web: A Review of the Field" (author version 2020; CACM 64(2), 2021): perspectives, RDF draft 1997, 2001 article, three phases, schema.org (read 20261102 20:57 UTC)
3. https://www.w3.org/TR/2004/REC-rdf-concepts-20040210/ : RDF Concepts and Abstract Syntax, W3C Recommendation 10 February 2004 (read 20261102 21:02 UTC)
4. https://www.w3.org/TR/2004/REC-owl-features-20040210/ : OWL Web Ontology Language Overview, W3C Recommendation 10 February 2004 (read 20261102 21:02 UTC)
5. https://www.w3.org/DesignIssues/LinkedData.html : Berners-Lee, "Linked Data - Design Issues", dated 20060727 (read 20261102 21:02 UTC)
6. https://www.w3.org/TR/2008/REC-rdf-sparql-query-20080115/ : SPARQL Query Language for RDF, W3C Recommendation 15 January 2008 (read 20261102 21:02 UTC)
7. https://googleblog.blogspot.com/2011/06/introducing-schemaorg-search-engines.html : Google, "Introducing schema.org", 2 June 2011 (first-party; read 20261102 21:01 UTC)
8. https://www.w3.org/TR/rdf12-concepts/ : RDF 1.2 Concepts and Abstract Data Model, W3C Candidate Recommendation Snapshot 07 April 2026 (read 20261102 20:57 UTC)
9. https://www.w3.org/TR/1999/REC-rdf-syntax-19990222/ : RDF Model and Syntax Specification, W3C Recommendation 22 February 1999 (read 20261102 21:25 UTC)
