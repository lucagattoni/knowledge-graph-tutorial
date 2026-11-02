---
type: index
kind: concept
aliases: [KR, knowledge representation and reasoning, KR&R]
updated: 20261102 23:12 UTC
---

# Knowledge representation

Knowledge representation is the symbolic encoding of what an agent knows so that a program can use it. This entry gives two working definitions, the dated points where the field is named, and the one disagreement the sources show: what a representation is for.

## Definition

Brachman and Levesque, in lecture slides for their text on knowledge representation and reasoning, define knowledge representation as the "symbolic encoding of propositions believed (by some agent)", and reasoning as the manipulation of such symbols to produce representations of new propositions [1]. Davis, Shrobe and Szolovits (1993) say the question "What is it?" has rarely been answered directly. They answer with five roles: a surrogate for things in the world, a set of ontological commitments, a fragmentary theory of intelligent reasoning, a medium for efficient computation and a medium of human expression [2]. They call logic, rules, frames and semantic nets "knowledge representation technologies" [2].

## How it changed

- **19740601.** Minsky's memo "A Framework for Representing Knowledge" is issued as MIT AI Memo 306 [3]. See [frame](./frame.md). Era: [Formal foundations](../history/formal-foundations.md).
- **198504.** Brachman and Schmolze's "An Overview of the KL-ONE Knowledge Representation System" is issued in *Cognitive Science* 9(2) [4]. See [KL-ONE](./kl-one.md). Era: [Knowledge systems](../history/knowledge-systems.md).
- **19890515 to 19890518.** The first KR conference is held in Toronto; the conference site dates the series from 1989 [5].
- **1993.** Davis et al. publish "What is a Knowledge Representation?" in *AI Magazine* 14(1) [2].
- **20230614.** Pan et al. (arXiv v1) call language models "black-box models" and knowledge graphs "structured knowledge models that explicitly store rich factual knowledge" [6]. See [knowledge graph](./knowledge-graph.md). Era: [What has settled since 2023](../history/settled-since-2023.md).

## Where sources disagree

What a representation is for. Davis et al. say approaches to representation "embed a view of the nature of intelligent reasoning": in the logicist tradition reasoning intelligently means reasoning "in the fashion defined by first order logic", while the psychological tradition takes it to be "a particular variety of human behavior" [2]. They also write that a semantic net is a representation and a graph is a data structure, because only the net has a semantics [2]. The slides define representation by propositions alone [1]. Which view the field holds today is **unstated** in the sources read.

## Related

[Knowledge base](./knowledge-base.md), [frame](./frame.md), [semantic network](./semantic-network.md), [production rule](./production-rule.md), [description logic](./description-logic.md), [ontology](./ontology.md), [expert system](./expert-system.md), [knowledge engineering](./knowledge-engineering.md), [knowledge graph](./knowledge-graph.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [The advent: machines that hold knowledge](../history/advent.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.cse.sc.edu/~mgv/csce781sp11/notes/BL_01.Introduction.pdf : Brachman and Levesque, lecture slides "Knowledge Representation and Reasoning" (copyright 2005), chapter 1: definitions of representation and reasoning (the authors' own slides; read 20261102 22:56 UTC)
2. https://groups.csail.mit.edu/medg/ftp/psz/k-rep.html : Davis, Shrobe, Szolovits, "What is a Knowledge Representation?", AI Magazine 14(1):17-33, 1993 (author-hosted copy): the five roles, "knowledge representation technologies", the logical and psychological views, "a graph is a data structure" passage (read 20261102 22:56 UTC)
3. https://dspace.mit.edu/handle/1721.1/6089 : MIT repository record of Minsky, "A Framework for Representing Knowledge", AI Memo 306, publication date 1974-06-01 (read 20261102 22:57 UTC)
4. https://api.crossref.org/works/10.1207/s15516709cog0902_1 : Crossref record of Brachman and Schmolze, "An Overview of the KL-ONE Knowledge Representation System", Cognitive Science 9(2), 171-216, issued 1985-04 (read 20261102 22:57 UTC)
5. https://www.kr.org/js/data.js : KR Inc. site data: first KR Conference, Toronto, May 15-18, 1989; "Since 1989, the KR Conference Series" (first-party; read 20261102 22:56 UTC)
6. https://arxiv.org/abs/2306.08302 : Pan et al., "Unifying Large Language Models and Knowledge Graphs: A Roadmap", abstract; submitted 14 Jun 2023 (v1) (read 20261102 22:57 UTC)
