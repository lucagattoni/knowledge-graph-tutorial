---
type: index
kind: standard
aliases: [RDFS, RDF Schema 1.1, RDF Vocabulary Description Language]
updated: 20261103 01:52 UTC
---

# RDF Schema

This entry answers what RDF Schema adds to [RDF](./rdf.md) and how its W3C documents are dated and named. It also says how RDF Schema relates to OWL.

## Definition

The W3C's RDF Schema 1.1 opens: "RDF Schema provides a data-modelling vocabulary for RDF data" and "is an extension of the basic RDF vocabulary" [1]. It describes groups of related resources and the relationships between them. The group of RDF Schema classes is itself a class, rdfs:Class, and rdfs:subClassOf states that one class is a subclass of another. The properties rdfs:domain and rdfs:range state that resources with a given property are instances of given classes, or that its values are [1]. The document "does not say whether or how an application should use it"; a reasoning application "might use it to infer additional information from instance data" [1]. Its formal meaning is in RDF 1.1 Semantics, which says RDFS entailment "is stronger than RDF entailment" [2]. Hitzler says RDF Schema can give an RDF graph a type structure as OWL can, but is "much less expressive than OWL" [7].

## How it changed

- **20000327.** *Resource Description Framework (RDF) Schema Specification 1.0*, a Candidate Recommendation, offers "a basic type system for use in RDF models" [3]. See [The Web changes data and search](../history/the-web.md).
- **20040210.** The Recommendation *RDF Vocabulary Description Language 1.0* [1][4] appeared with RDF 1.0, whose concepts document says it "jointly" replaces the 1999 RDF specification and the 2000 schema draft [5]. See [The semantic web and linked data](../history/semantic-web.md).
- **20140225.** *RDF Schema 1.1* became a Recommendation, renamed from "RDF Vocabulary Description Language 1.0". Changes were editorial: "URI Reference" became "IRI", rdf:langString and rdf:HTML were added, the out-of-date RDF/XML appendix was removed [1]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20231201.** Both pages carry a status update of this date; for the 2004 page it only corrected the "Latest Version" link [1][4].
- **20261023.** *RDF 1.2 Schema* is a Working Draft, not a Recommendation; its abstract repeats that of 1.1, and the latest Recommendation is RDF 1.1 Schema [6]. It moves with RDF 1.2; see [Semantic web standards](../trends/semantic-web-standards.md).

## Where sources disagree

No disagreement found in the sources read.

## Related

[RDF](./rdf.md) · [OWL](./owl.md) · [description logic](./description-logic.md) · [ontology](./ontology.md) · [SHACL](./shacl.md) · [SPARQL](./sparql.md) · [linked data](./linked-data.md) · [schema.org](./schema-org.md) · [semantic web](./semantic-web.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [The Web changes data and search](../history/the-web.md)

**Trends**

- [Semantic web standards: from RDF 1.1 and RDF-star to RDF 1.2](../trends/semantic-web-standards.md)

**Index**

- [Ontology](ontology.md)
- [OWL](owl.md)
- [RDF](rdf.md)
- [RDF Dataset Canonicalization](rdf-dataset-canonicalization.md)
- [Schema](schema.md)
- [schema.org](schema-org.md)
- [Semantic Web](semantic-web.md)
- [SHACL](shacl.md)
- [Taxonomy](taxonomy.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.w3.org/TR/rdf-schema/ : RDF Schema 1.1, W3C Recommendation 20140225 (status update 20231201): abstract, introduction, rdfs:Class, rdfs:subClassOf, rdfs:domain, rdfs:range, use by applications, Appendix B changes since 2004 (read 20261102 20:55 UTC; domain, range and application-use passages re-read 20261102 20:58 UTC)
2. https://www.w3.org/TR/rdf11-mt/ : RDF 1.1 Semantics, W3C Recommendation 20140225, section 9 "RDFS Interpretations": RDFS entailment (read 20261102 20:58 UTC)
3. https://www.w3.org/TR/2000/CR-rdf-schema-20000327/ : Resource Description Framework (RDF) Schema Specification 1.0, W3C Candidate Recommendation 20000327 (read 20261102 20:57 UTC)
4. https://www.w3.org/TR/2004/REC-rdf-schema-20040210/ : RDF Schema, W3C Recommendation 20040210, status update 20231201 (read 20261102 20:55 UTC)
5. https://www.w3.org/TR/rdf10-concepts/ : RDF Concepts and Abstract Syntax, W3C Recommendation 20040210: "intended to jointly replace" RDF Model and Syntax and RDF Schema (read 20261102 20:55 UTC)
6. https://www.w3.org/TR/rdf12-schema/ : RDF 1.2 Schema, W3C Working Draft 20261023; latest Recommendation RDF 1.1 Schema (read 20261102 20:57 UTC; re-read 20261102 21:21 UTC)
7. https://par.nsf.gov/servlets/purl/10292869 : Hitzler, "A Review of the Semantic Web Field", CACM 64(2), 2021, footnote 13: RDF Schema "is part of the RDF standard", "much less expressive than OWL" (read 20261102 20:58 UTC)
