---
type: index
kind: concept
aliases: [KB]
updated: 20261102 20:54 UTC
---

# Knowledge base

This entry says what a knowledge base is and how the phrase was used from expert systems to language models. The sources draw the term at different widths, and the entry shows where.

## Definition

In the course slides of Brachman and Levesque, a system is knowledge-based when it holds a separate collection of symbolic structures that we can read as propositions and that determine how the system behaves. That collection is its knowledge base (KB) [1]. For expert systems, Feigenbaum put the weight there: "The interesting action arises from the knowledge base, not the inference engine" [2].

## How it changed

- 1977: Feigenbaum writes of knowledge bases holding rules, models based on theory, and frame-like tables of symbolic data; rule form allows "great flexibility for adding, removing, or changing knowledge". The MOLGEN system's knowledge base is to be "a repository" of its specialty [2]. See [expert system](./expert-system.md) and [production rule](./production-rule.md).
- Early 1980s: rule bases such as MYCIN's mix strategic and domain knowledge, which makes maintenance hard [3].
- 1980s: the Cyc project aims at "the world's largest knowledge base of common sense", per Gutierrez and Sequeda [4]. See [Cyc](./cyc.md).
- 20120516: Google announces its Knowledge Graph; Hogan et al. date the modern use of "knowledge graph" to it [5]. See [knowledge graph](./knowledge-graph.md).
- 2016: Ehrlinger and Woess read a knowledge graph as "superior and more complex" than a knowledge base such as an ontology, because it adds a reasoner [6].
- 20190903: Petroni et al. ask whether pretrained language models can serve as knowledge bases; their abstract compares them with structured ones that need schema engineering [7].

Eras: [Knowledge systems](../history/knowledge-systems.md), [Language models meet retrieval](../history/language-models-meet-retrieval.md).

## Where sources disagree

The width of the term differs. Feigenbaum's knowledge bases are rules, models and tables inside expert systems [2]. For Brachman and Levesque even a handful of Prolog facts and rules, kept apart from the code that uses them, is a knowledge base [1]. Petroni et al. test a trained model as one [7]. No source read gives a rival date.

*Reading:* "knowledge base" names a role (the part that holds what the system knows), not a data structure; the later terms (knowledge graph, ontology, memory) name particular forms.

## Related

[Knowledge graph](./knowledge-graph.md), [knowledge engineering](./knowledge-engineering.md), [knowledge acquisition bottleneck](./knowledge-acquisition-bottleneck.md), [inference engine](./inference-engine.md), [ontology](./ontology.md), [KL-ONE](./kl-one.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [The Web changes data and search](../history/the-web.md)

**Projects**

- [Projects](../projects/README.md)

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Applied to Pinakes**

- [Applied to Pinakes](../applied-to-pinakes/README.md)
- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Closed-world assumption](closed-world-assumption.md)
- [Cognitive architecture](cognitive-architecture.md)
- [Cyc](cyc.md)
- [DENDRAL](dendral.md)
- [Description logic](description-logic.md)
- [Expert system](expert-system.md)
- [Frame](frame.md)
- [Inference engine](inference-engine.md)
- [KL-ONE](kl-one.md)
- [Knowledge acquisition bottleneck](knowledge-acquisition-bottleneck.md)
- [Knowledge engineering](knowledge-engineering.md)
- [Knowledge graph](knowledge-graph.md)
- [Knowledge representation](knowledge-representation.md)
- [Knowledge-base question answering](knowledge-base-question-answering.md)
- [LLM wiki](llm-wiki.md)
- [MYCIN](mycin.md)
- [Ontology](ontology.md)
- [Production rule](production-rule.md)
- [Slot filling](slot-filling.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.cse.sc.edu/~mgv/csce781sp11/notes/BL_01.Introduction.pdf : Brachman and Levesque, lecture slides "Knowledge Representation and Reasoning" (copyright 2005), chapter 1, the two Prolog examples and "knowledge base (or KB)"; slides on a course site, the textbook itself was not read (read 20261102 20:49 UTC)
2. https://www.ijcai.org/Proceedings/77-2/Papers/092.pdf : Feigenbaum, IJCAI-77: the knowledge-base passages and MOLGEN (read 20261102 20:45 UTC)
3. https://publikationen.bibliothek.kit.edu/189497/3003 : Studer, Benjamins, Fensel, Data & Knowledge Engineering 25, 1998 (author copy), section 2.1: MYCIN rule base and the transfer approach (read 20261102 20:49 UTC)
4. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, CACM 64(3), 2021: Cyc "world's largest knowledge base of common sense" (read 20261102 20:45 UTC)
5. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", introduction: the modern phrase "stems from the 2012 announcement" (read 20261102 20:45 UTC)
6. https://ceur-ws.org/Vol-1695/paper4.pdf : Ehrlinger and Woess, "Towards a Definition of Knowledge Graphs", SEMANTiCS 2016 Posters and Demos, section 4 (read 20261102 20:47 UTC)
7. https://arxiv.org/abs/1909.01066 : Petroni et al., "Language Models as Knowledge Bases?", first submitted 3 September 2019, EMNLP 2019; abstract only (read 20261102 20:46 UTC)
