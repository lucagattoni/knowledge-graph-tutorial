---
type: index
kind: concept
aliases: [CWA]
updated: 20261102 21:28 UTC
---

# Closed-world assumption

This entry answers what a system assumes when it treats missing data as false, where the rule came from, and why knowledge graphs and ontologies often take the opposite view. It does not cover how negation is handled in any one query language. The two 1978 chapters themselves were not read.

## Definition

Under the closed-world assumption (CWA), the data are taken to be a complete description of the world, so whatever is not stated is false [1]. Hogan et al.: with no flight edge between two cities in the graph, a system with the CWA can say with certainty that no such flight exists, as in "many classical database systems" [1]. The opposite is the open-world assumption (OWA): an absent statement may simply be unknown [1]. The OWL 2 Primer states the same contrast: a fact missing from a database is usually considered false, whereas in an OWL 2 document it "may simply be missing (but possibly true)" [2]. Hogan et al. point out a consequence: under the CWA, adding an edge can contradict what was assumed false before, whereas under the OWA a statement proven false stays false when more edges are added [1].

## How it changed

- **1977.** At the workshop "Logic and Data Bases" in Toulouse, organised by Gallaire, Minker and Nicolas, Ray Reiter presented the closed-world assumption and Keith Clark presented negation as failure. Gutierrez and Sequeda call the workshop a landmark event [3]. See [Formal foundations](../history/formal-foundations.md).
- **1978.** The two chapters appeared in the workshop volume *Logic and Data Bases*: Reiter's "On Closed World Data Bases" (pages 55 to 76) and Clark's "Negation as Failure" (pages 293 to 322) [4].
- **20121211.** The OWL 2 specification (Second Edition, a W3C Recommendation of that date) says "OWL 2 has open-world semantics", so negation in it is that of classical logic [5]. See [The semantic web and linked data](../history/semantic-web.md).
- **20200304.** In the first version of their survey (v1), Hogan et al. describe a compromise between the two, the Local Closed World Assumption, where portions of a graph are assumed complete [1][6].

## Where sources disagree

No disagreement found in the sources read. One difference of date only: Gutierrez and Sequeda tie the idea to the 1977 workshop [3], while the bibliographic record of Reiter's chapter reads 1978, the year of the volume [4].

## Related

[description logic](./description-logic.md) · [ontology](./ontology.md) · [OWL](./owl.md) · [RDF](./rdf.md) · [SHACL](./shacl.md) · [logic programming](./logic-programming.md) · [Datalog](./datalog.md) · [relational model](./relational-model.md) · [knowledge graph](./knowledge-graph.md) · [knowledge base](./knowledge-base.md) · [foundation papers](../papers/foundations.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)

**Datasets**

- [Wikidata](../datasets/wikidata.md)

**Index**

- [Datalog](datalog.md)
- [Logic programming](logic-programming.md)
- [Schema](schema.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", arXiv 2003.02320 v6 (20210911): the passages on the CWA and OWA, the Local Closed World Assumption, and the definition of negative edges (read 20261102 20:45 UTC)
2. https://www.w3.org/TR/owl2-primer/ : OWL 2 Web Ontology Language Primer (Second Edition), W3C Recommendation 11 December 2012, "OWL 2 is not a database framework" (read 20261102 20:47 UTC)
3. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: the 1977 Toulouse workshop (read 20261102 20:47 UTC)
4. https://api.crossref.org/works/10.1007/978-1-4684-3384-5_3 and https://api.crossref.org/works/10.1007/978-1-4684-3384-5_11 : Crossref records of Reiter's "On Closed World Data Bases" (pages 55-76) and Clark's "Negation as Failure" (pages 293-322), both in *Logic and Data Bases*, 1978; bibliographic data only, the chapters themselves were not read (searched 20261102 20:48 UTC; the two DOI records fetched 20261102 21:23 UTC)
5. https://www.w3.org/TR/owl2-syntax/ : OWL 2 Web Ontology Language Structural Specification and Functional-Style Syntax (Second Edition), W3C Recommendation 11 December 2012, section on open-world semantics (read 20261102 20:47 UTC)
6. https://arxiv.org/pdf/2003.02320v1 : Hogan et al., "Knowledge Graphs", v1 submitted 20200304: the sentence on the Local Closed World Assumption, section 3.1.1 (read 20261102 21:24 UTC)
