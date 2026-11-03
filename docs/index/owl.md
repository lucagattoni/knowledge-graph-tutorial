---
type: index
kind: standard
aliases: [Web Ontology Language, OWL 2]
updated: 20261102 21:32 UTC
---

# OWL

OWL is the W3C language for writing [ontologies](./ontology.md) for the Semantic Web, with a defined meaning that programs can reason over. This entry gives the specification's definition, its dated versions and its current status.

## Definition

The OWL 2 Document Overview says OWL 2 "is an ontology language for the Semantic Web with formally defined meaning"; ontologies provide classes, properties, individuals and data values, are stored as Semantic Web documents, and are primarily exchanged as RDF documents [1]. It has two alternative semantics: the Direct Semantics, compatible with the SROIQ description logic, and the RDF-Based Semantics, which applies to any RDF graph [1]. Three profiles trade expressive power for computational benefits: OWL 2 EL, QL and RL [1]. The overview describes EL as particularly suitable where very large ontologies are needed [1]. Sowa writes that OWL is widely used in the Semantic Web but "most applications of OWL use only the EL subset", giving no count in the text read [6].

## How it changed

- **2000 to 2006.** The DAML programme and the EU project On-To-Knowledge (which gave OIL) are merged and lead to OWL [4].
- **20040210.** OWL becomes a W3C Recommendation, "a revision of the DAML+OIL web ontology language", with three sublanguages: OWL Lite, OWL DL and OWL Full [5]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **20091027.** The first edition of OWL 2 is published; the 2004 document's status update of 12 November 2009 says the working group has produced a Recommendation for a new version that adds features while "remaining compatible" [2][3][5].
- **20121211.** The OWL 2 Document Overview, Second Edition, is a W3C Recommendation, with "no substantive changes" since the previous version. All OWL 1 ontologies remain valid OWL 2 ontologies [1]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20261102.** The W3C specification API names this Second Edition as the latest version of the OWL 2 Document Overview [2]. A successor draft: unstated in the sources read.

## Where sources disagree

No disagreement found in the sources read.

## Related

[Ontology](./ontology.md), [RDF](./rdf.md), [RDF Schema](./rdfs.md), [SPARQL](./sparql.md), [SHACL](./shacl.md), [description logic](./description-logic.md), [semantic web](./semantic-web.md), [linked data](./linked-data.md), [Datalog](./datalog.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [The semantic web and linked data](../history/semantic-web.md)
- [The Web changes data and search](../history/the-web.md)

**Trends**

- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)

**Projects**

- [Cognee](../projects/cognee.md)
- [Semantica](../projects/semantica.md)

**Index**

- [Closed-world assumption](closed-world-assumption.md)
- [Datalog](datalog.md)
- [Description logic](description-logic.md)
- [Inference engine](inference-engine.md)
- [KL-ONE](kl-one.md)
- [LinkML](linkml.md)
- [Ontology](ontology.md)
- [RDF](rdf.md)
- [RDF Schema](rdfs.md)
- [Semantic Web](semantic-web.md)
- [SHACL](shacl.md)
- [SPARQL](sparql.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.w3.org/TR/owl2-overview/ : OWL 2 Web Ontology Language Document Overview (Second Edition), W3C Recommendation 11 December 2012: abstract, sections 2 to 3 (definition, semantics, profiles incl. EL, relation to OWL 1) (read 20261102 20:54 UTC; the EL sentence re-read 20261102 21:25 UTC)
2. https://api.w3.org/specifications/owl2-overview and https://api.w3.org/specifications/owl2-overview/versions : W3C specification API: latest version 20121211 "Recommendation"; seven versions listed from 20090327 to 20121211 (read 20261102 20:55 UTC)
3. https://www.w3.org/OWL/ : W3C Semantic Web Standards wiki page "OWL" (last edited 20131211): overview, "Publication date: 2012-12-11 (with a previous version published at: 2009-10-27)" (read 20261102 20:54 UTC)
4. https://par.nsf.gov/servlets/purl/10292869 : Hitzler, "A Review of the Semantic Web Field" (author's version of the CACM article; accepted April 2020): DAML, On-To-Knowledge, OIL (read 20261102 20:57 UTC)
5. https://www.w3.org/TR/2004/REC-owl-features-20040210/ : OWL Web Ontology Language Overview, W3C Recommendation 10 February 2004, with the status update of 12 November 2009: abstract, introduction (read 20261102 20:54 UTC)
6. https://www.jfsowa.com/pubs/semnet.htm : Sowa, "Semantic Networks": the paragraph on description logics and OWL (re-read 20261102 21:25 UTC)
