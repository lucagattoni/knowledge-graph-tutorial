---
type: index
kind: system
aliases: [Knowledge Language One]
updated: 20261102 21:22 UTC
---

# KL-ONE

This entry says what KL-ONE is and why description logics are traced to it. The sources give three different years around it, and the entry shows each.

## Definition

KL-ONE is a system for representing knowledge in artificial intelligence programs. The abstract of Brachman and Schmolze's overview says it "has been developed and refined over a long period", and names its kernel ideas: complex structured descriptions, with taxonomy and classification at the centre [1]. In Sowa's account a KL-ONE network draws concepts as nodes, joined by subtype-supertype links and by roles, and the description logics are derived from the approach it implemented [2].

## How it changed

- 1975: Woods's "What's in a link" proposes the approach from which KL-ONE is derived, per Sowa [2].
- 1977: Brachman's Harvard thesis, "A structural paradigm for representing knowledge"; Hogan et al. list it with Woods (1975) as a formalisation of semantic networks [3].
- 1979: Sowa writes that the approach was "implemented by Brachman (1979)" in a system called Knowledge Language One. The year is that of a citation, not of a release [2].
- 1983: Krypton pairs a KL-ONE term hierarchy (T-Box) with a theorem prover for first-order assertions (A-Box) [2].
- 1984: Brachman and Levesque's paper on the tractability of subsumption (AAAI, Austin, 6-10 August 1984) is "among the first" to show that more expressive logics cost more to reason with; this gave rise to the description logics, with KL-ONE, LOOM and CLASSIC as standout systems [4].
- April 1985: the overview is published in *Cognitive Science* 9(2), pages 171-216 [1]. Hogan et al. write that description logics "stem from" this system [3].
- 1991: the language ALC of Schmidt-Schauss and Smolka follows [3].
- 20040210: the OWL Recommendation names OWL DL after its correspondence with description logics [5].

Eras: [Formal foundations](../history/formal-foundations.md), [Knowledge systems](../history/knowledge-systems.md).

## Where sources disagree

The year differs: 1979 (Sowa), 1984 (Gutierrez and Sequeda, for the tractability paper that gave rise to description logics) and 1985 (Hogan et al., for the overview) [2][4][3]. Sowa's 1979 is the year attached to Brachman in the sentence on the implementation; the only Brachman 1979 entry in his reference list is a paper, "On the epistemological status of semantic networks" [2]. Sowa gives no other date for the system, and the abstract of the 1985 overview gives none either [1]. The exact year in which the system was first built or released is **unstated** in the sources read.

*Reading:* the three years name three events, not rival dates for one: a system, a result about logics, and a published overview.

## Related

[Description logic](./description-logic.md), [frame](./frame.md), [semantic network](./semantic-network.md), [OWL](./owl.md), [knowledge base](./knowledge-base.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)

**Index**

- [Conceptual graph](conceptual-graph.md)
- [Description logic](description-logic.md)
- [Frame](frame.md)
- [Knowledge base](knowledge-base.md)
- [Knowledge representation](knowledge-representation.md)
- [Semantic network](semantic-network.md)
- [Taxonomy](taxonomy.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.crossref.org/works/10.1207/s15516709cog0902_1 : Brachman and Schmolze, "An Overview of the KL-ONE Knowledge Representation System", Cognitive Science 9(2):171-216, issued 1985-04; abstract only, the full text was not read (read 20261102 20:47 UTC)
2. https://www.jfsowa.com/pubs/semnet.htm : Sowa, "Semantic Networks": Woods 1975, Brachman 1979, Krypton 1983, roles and subtype links, reference list (read 20261102 21:21 UTC)
3. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", ACM Computing Surveys 54(4), Appendix A and references: Brachman 1977 thesis, KL-ONE 1985, ALC 1991 (read 20261102 21:21 UTC)
4. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: the tractability paper (AAAI, 6-10 August 1984), description logics, KL-ONE, LOOM and CLASSIC (read 20261102 21:21 UTC)
5. https://www.w3.org/TR/2004/REC-owl-features-20040210/ : OWL Web Ontology Language Overview, W3C Recommendation 10 February 2004: OWL DL and description logics (read 20261102 20:48 UTC)
