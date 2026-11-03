---
type: index
kind: standard
aliases: [Shapes Constraint Language]
updated: 20261103 01:52 UTC
---

# SHACL

SHACL is the W3C language for writing down what an RDF graph should look like and for checking a graph against it. This entry gives the definition, the 2017 Recommendation, and the 2025 to 2026 drafts of SHACL 1.2, which are not yet a Recommendation.

## Definition

The W3C Recommendation of 20170720 defines SHACL, the Shapes Constraint Language, as "a language for validating RDF graphs against a set of conditions" [1]. The conditions are shapes, written as an [RDF](./rdf.md) graph called the shapes graph; the graph being checked is the data graph [1]. The Recommendation says shapes graphs can also describe data, for user interfaces, code generation and data integration [1]. The RDF Data Shapes Working Group produced it; Holger Knublauch and Dimitris Kontokostas edited it [1]. Hogan and 17 co-authors name two shapes languages for RDF graphs: Shape Expressions (ShEx), a W3C Community Group Report, and SHACL, a W3C Recommendation; they report adoption in health care, scientific literature and spatial data [3].

## How it changed

- **20151008.** First Public Working Draft [2].
- **20170720.** SHACL becomes a W3C Recommendation, after a Proposed Recommendation of 20170608 [1][2]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20250318.** First Public Working Draft of SHACL 1.2 Core [4].
- **20261102.** The 62nd publication of that draft, the latest read, is a Working Draft [4][5]. The 1.2 family lists six SHACL Working Drafts, among them Core, Node Expressions and SPARQL-Related Features [5]. Changes from 2017 include node expressions, SPARQL-based validators moved out of Core, and `sh:agentInstruction`, which holds "textual instructions that can be sent to a software agent" [5]. The draft names the 2017 text as the latest Recommendation [5]. Not settled: see [What has settled since 2023](../history/settled-since-2023.md); still moving: [Semantic web standards](../trends/semantic-web-standards.md).

## Where sources disagree

The W3C's own description changed. The 2017 Recommendation calls SHACL "a language for validating RDF graphs" [1]; the 2026 Core draft calls it "a language for describing the structure of RDF graphs" and lists validating as one of several uses [5]. Which wording the final 1.2 text keeps is **unstated**. The draft warns that it is "inappropriate to cite" it other than as work in progress [5].

## Related

[RDF](./rdf.md), [RDF Schema](./rdfs.md), [OWL](./owl.md), [SPARQL](./sparql.md), [ontology](./ontology.md), [linked data](./linked-data.md), [agent](./agent.md). Papers: Hogan et al. 2021 is in [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Trends**

- [Semantic web standards: from RDF 1.1 and RDF-star to RDF 1.2](../trends/semantic-web-standards.md)

**Datasets**

- [YAGO](../datasets/yago.md)

**Index**

- [Closed-world assumption](closed-world-assumption.md)
- [JSON-LD](json-ld.md)
- [LinkML](linkml.md)
- [Ontology](ontology.md)
- [OWL](owl.md)
- [RDF](rdf.md)
- [RDF Dataset Canonicalization](rdf-dataset-canonicalization.md)
- [RDF Schema](rdfs.md)
- [Schema](schema.md)
- [SPARQL](sparql.md)
- [YAGO](yago.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.w3.org/TR/shacl/ : SHACL W3C Recommendation 20 July 2017: abstract, shapes graph and data graph, editors, Data Shapes Working Group, status (read 20261102 20:57 UTC)
2. https://www.w3.org/standards/history/shacl/ : publication history of SHACL: First Public Working Draft 20151008, Proposed Recommendation 20170608, Recommendation 20170720 (read 20261102 20:58 UTC)
3. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs" (18 authors), ACM Computing Surveys 2021: the passage on shapes languages (ShEx, SHACL, domains of adoption); v6 last revised 11 Sep 2021 per https://arxiv.org/abs/2003.02320 (read 20261102 20:59 UTC and 21:06 UTC)
4. https://www.w3.org/standards/history/shacl12-core/ : publication history of SHACL 1.2 Core: First Public Working Draft 18 March 2025, 62 publications to 2 November 2026 (read 20261102 20:58 UTC)
5. https://www.w3.org/TR/shacl12-core/ : SHACL 1.2 Core Working Draft 2 November 2026: abstract, status, family of specifications, section on changes since the original Core, `sh:intent` and `sh:agentInstruction` (read 20261102 20:57 UTC)
