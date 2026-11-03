---
type: index
kind: concept
aliases: [DL, DLs, description logics]
updated: 20261102 21:25 UTC
---

# Description logic

A description logic is a logic for describing the classes of a domain and the relations between them, built so that a program can decide questions about them in finite time. This page defines the term, dates its origin and follows it to the Web Ontology Language.

## Definition

Hogan et al. write that description logics (DLs) were "initially introduced" to "formalise the meaning of frames" and of "semantic networks" [1]. DLs are a family of logics, not one logic: they began as restricted fragments of first-order logic that permit decidable reasoning, and each member trades expressive power against the cost of reasoning [1]. A DL speaks of individuals, classes (concepts) and properties (roles), and states claims about them as axioms [1]. Krötzsch, Simančík and Horrocks give a self-contained introduction built on the DL SROIQ [2].

## How it changed

- **1975, 1979.** Sowa traces DLs to an approach proposed by Woods (1975) and implemented by Brachman (1979) in KL-ONE [3]. Era: [Formal foundations](../history/formal-foundations.md).
- **1977.** Hayes recognises that frame networks can be formalised in first-order logic [4].
- **19840806 to 19840810.** Brachman and Levesque present "The tractability of subsumption in frame-based description languages" at AAAI-84. It is among the first papers to show that more expressive power costs more computation, which gave rise to the family [4]. Era: [Knowledge systems](../history/knowledge-systems.md).
- **1985.** Brachman and Schmolze publish the KL-ONE overview in *Cognitive Science* 9(2) [5].
- **20040210.** The OWL Recommendation names a sublanguage OWL DL after its correspondence with DLs [6]. Gutierrez and Sequeda trace it to DAML+OIL [4]. Era: [The semantic web](../history/semantic-web.md).
- **20091027 and 20121211.** The OWL 2 specification is a W3C Recommendation of 20091027, in a second edition of 20121211 [8][7]. Its Direct Semantics is compatible with SROIQ, and OWL 2 DL names the ontologies that can be translated into a SROIQ knowledge base [7].

## Where sources disagree

The start. Sowa names KL-ONE (1979) [3]; Gutierrez and Sequeda name the 1984 tractability paper as the first development [4]; Hogan et al. name the 1985 KL-ONE overview and the language ALC (1991) [1]. *Reading:* each points to a different artefact (a system, a result, a paper), so the dates are compatible.

## Related

[Frame](./frame.md), [semantic network](./semantic-network.md), [conceptual graph](./conceptual-graph.md), [KL-ONE](./kl-one.md), [knowledge base](./knowledge-base.md), [ontology](./ontology.md), [OWL](./owl.md), [RDF](./rdf.md), [semantic web](./semantic-web.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [The semantic web and linked data](../history/semantic-web.md)

**Index**

- [Closed-world assumption](closed-world-assumption.md)
- [Conceptual graph](conceptual-graph.md)
- [Frame](frame.md)
- [Inference engine](inference-engine.md)
- [KL-ONE](kl-one.md)
- [Knowledge representation](knowledge-representation.md)
- [Ontology](ontology.md)
- [OWL](owl.md)
- [RDF Schema](rdfs.md)
- [Semantic network](semantic-network.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", section 4.3.2 (definition, family of logics, individuals, classes, properties), Appendix A.1 (KL-ONE 1985, ALC 1991) (read 20261102 20:44 UTC)
2. https://arxiv.org/abs/1201.4089 : Krötzsch, Simančík, Horrocks, "A Description Logic Primer", abstract (v1 20120119) (read 20261102 20:50 UTC)
3. https://www.jfsowa.com/pubs/semnet.htm : Sowa, "Semantic Networks": DLs derived from Woods (1975), implemented by Brachman (1979) in KL-ONE (read 20261102 20:49 UTC)
4. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, CACM 64(3), 2021: Hayes 1977, Brachman and Levesque 1984 (reference 4), systems, DAML+OIL and OWL 2004 (read 20261102 20:44 UTC)
5. https://api.crossref.org/works/10.1207/s15516709cog0902_1 : Crossref record of Brachman and Schmolze, "An Overview of the KL-ONE Knowledge Representation System", *Cognitive Science* vol. 9, issue 2, pages 171-216, issued 1985-04 (read 20261102 21:24 UTC)
6. https://www.w3.org/TR/2004/REC-owl-features-20040210/ : OWL Web Ontology Language Overview, W3C Recommendation 10 February 2004: Lite, DL, Full; "so named due to its correspondence with description logics" (read 20261102 20:46 UTC)
7. https://www.w3.org/TR/owl2-overview/ : OWL 2 Document Overview (Second Edition), 11 December 2012: Direct Semantics compatible with SROIQ, profiles EL, QL, RL (read 20261102 20:46 UTC)
8. https://www.w3.org/TR/owl2-syntax/ : OWL 2 Structural Specification (Second Edition), change log "since the Recommendation of 27 October 2009" (read 20261102 20:46 UTC)
