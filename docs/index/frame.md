---
type: index
kind: concept
aliases: [frames, frame system, frame-based representation]
updated: 20261102 20:57 UTC
---

# Frame

A frame is a structure of slots that stands for a typical situation or object and is filled with the details of a particular case. This page gives Minsky's definition, follows the idea into description logics and rule-based systems, and notes how sources describe it.

## Definition

Minsky's memo of 1974 proposes that on meeting a new situation a person selects from memory "a structure called a frame, a remembered framework to be adopted to fit reality by changing details as necessary" [1]. He defines a frame as "a data-structure for representing a stereotyped situation": its top levels are fixed, its lower levels have slots to be filled by specific instances, and related frames are linked into frame-systems [1].

## How it changed

- **19740601.** Minsky's MIT AI Memo 306, "A Framework for Representing Knowledge", is issued [1]. Era: [Formal foundations](../history/formal-foundations.md).
- **1977.** Hayes recognises that frame networks can be formalised in first-order logic [2].
- **1980s.** Early expert systems mixed rules, nets and frames, and the shell S.1 supported frames besides rules (Shadbolt) [3]. See [expert system](./expert-system.md).
- **19840806 to 19840810.** Brachman and Levesque present "The tractability of subsumption in frame-based description languages" at AAAI-84, an early result on the cost of expressive power [2]. Era: [Knowledge systems](../history/knowledge-systems.md).
- **1985.** The KL-ONE overview of Brachman and Schmolze appears; Hogan et al. name conceptual graphs, semantic networks and frames "direct predecessors of Description Logics" [4]. See [description logic](./description-logic.md).
- **20040210.** The OWL Recommendation names a sublanguage after its correspondence with description logics [5], which Hogan et al. say were introduced to formalise frames [4]. Era: [The semantic web](../history/semantic-web.md).

## Where sources disagree

What a frame is. Minsky calls his paper "a partial theory of thinking" that draws on psychology, linguistics and AI [1]. Gutierrez and Sequeda define a frame as "a network of nodes and relations" [2]. Hogan et al. treat it as a knowledge-representation device whose meaning DLs formalise [4]. *Reading:* the later sources keep the representation and drop the psychological claim.

## Related

[Semantic network](./semantic-network.md), [conceptual graph](./conceptual-graph.md), [description logic](./description-logic.md), [KL-ONE](./kl-one.md), [expert system](./expert-system.md), [production rule](./production-rule.md), [knowledge base](./knowledge-base.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)

**Index**

- [Conceptual graph](conceptual-graph.md)
- [Description logic](description-logic.md)
- [Expert system](expert-system.md)
- [KL-ONE](kl-one.md)
- [Knowledge representation](knowledge-representation.md)
- [Production rule](production-rule.md)
- [Semantic network](semantic-network.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://dspace.mit.edu/handle/1721.1/6089 : Minsky, "A Framework for Representing Knowledge", MIT AI Memo 306: date issued 1 June 1974, abstract (read 20261102 20:49 UTC)
2. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, CACM 64(3), 2021: frame defined as a network of nodes and relations, Hayes 1977, Brachman and Levesque 1984 (read 20261102 20:44 UTC)
3. https://eprints.soton.ac.uk/252374/1/A_Natural_History_of_Expert_Systems_1989.pdf : Shadbolt 1989: "rules, nets and frames"; S.1 shell supports frames (read 20261102 20:44 UTC)
4. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", Appendix A.1 (predecessors of DLs, KL-ONE 1985) and section 4.3.2 (read 20261102 20:44 UTC)
5. https://www.w3.org/TR/2004/REC-owl-features-20040210/ : OWL Web Ontology Language Overview, W3C Recommendation 10 February 2004: OWL DL named for its correspondence with description logics (read 20261102 20:46 UTC)
