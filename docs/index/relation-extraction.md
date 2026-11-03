---
type: index
kind: concept
aliases: [RE, relationship extraction, open information extraction, OIE]
updated: 20261102 22:50 UTC
---

# Relation extraction

This entry answers what relation extraction is, how its closed and open settings differ, and how language models changed it. It is the step that turns sentences into the edges of a graph.

## Definition

Hogan et al. (ACM Computing Surveys 54(4), 2021) write that the relation extraction (RE) task "extracts relations between entities in the text" [1]. The simplest case is binary relations in a closed setting, with a fixed set of relation types [1]. In their pipeline RE follows [named-entity recognition](./named-entity-recognition.md) and [entity linking](./entity-linking.md) [1]. Wadhwa et al. call it "the core NLP task of inferring semantic relationships between entities from text" [6].

## How it changed

- **1998.** MUC-7 (29 April to 1 May) evaluated Template Relations: employee_of, product_of, location_of [2].
- **200405.** The ACE overview (LREC 2004) lists a relation task with five general types, 24 types and subtypes in all [3].
- **2007.** Banko et al. introduce Open IE: one pass over a corpus, no relations named in advance. TextRunner cuts errors by 33% against KnowItAll (first-party) [4].
- **200908.** Mintz et al. train a relation classifier on sentences labelled by [Freebase](./freebase.md) relations, with no hand-labelled corpus. See [distant supervision](./distant-supervision.md) [5].
- **20230508.** Wadhwa et al.: few-shot GPT-3 roughly matches fully supervised models under human evaluation (first-party) [6].
- **20230522.** Zhu et al.: GPT-4 is "more suited as inference assistants rather than few-shot information extractors" (first-party) [7].
- **20251011.** LinearRAG's authors call relation extraction "unstable and costly" and build a graph without it (first-party) [8]. Still moving: [Graph-based RAG](../trends/graph-based-rag.md), [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

Eras: [The Web changes data and search](../history/the-web.md), [The semantic web and linked data](../history/semantic-web.md).

## Where sources disagree

**Is open extraction part of it?** Hogan et al. treat Open IE as RE in an open setting, where relations are "not pre-defined" [1]. Banko et al. present it as "a new extraction paradigm" [4]; ACE fixes its types in advance [3]. Whether "relation extraction" means only the closed task depends on the author.

**Can a prompted model do it?** Wadhwa et al. say yes, near fully supervised models [6]; Zhu et al. rank GPT-4 better at inference than at few-shot extraction [7]. The abstracts name different models, data and scoring.

## Related

[Named-entity recognition](./named-entity-recognition.md) · [entity linking](./entity-linking.md) · [triple](./triple.md) · [slot filling](./slot-filling.md) · [distant supervision](./distant-supervision.md) · [schema induction](./schema-induction.md) · [knowledge graph](./knowledge-graph.md). Project: [GLiNER](../projects/gliner.md). Benchmark: [Text2KGBench](../benchmarks/text2kgbench.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)

**Projects**

- [GLiNER](../projects/gliner.md)
- [Projects](../projects/README.md)

**Benchmarks**

- [Text2KGBench](../benchmarks/text2kgbench.md)

**Index**

- [Distant supervision](distant-supervision.md)
- [Entity linking](entity-linking.md)
- [Knowledge graph completion](knowledge-graph-completion.md)
- [Schema induction](schema-induction.md)
- [Slot filling](slot-filling.md)
- [Triple](triple.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", ACM Computing Surveys 54(4), 2021, arXiv v6 of 11 September 2021: section 6.2.4 (definition, closed and open settings) and Figure 31 (read 20261102 22:06 UTC)
2. https://aclanthology.org/M98-1001.pdf : Chinchor, "Overview of MUC-7/MET-2": Template Relations task and its three relations; conference dates from https://aclanthology.org/M98-1001/ (read 20261102 22:09 UTC)
3. https://aclanthology.org/L04-1011.pdf : Doddington et al., "The Automatic Content Extraction (ACE) Program", LREC 2004: relation detection and characterization, 5 types, 24 types and subtypes (read 20261102 22:09 UTC); the month, May 2004, is from https://aclanthology.org/L04-1011/, which lists "Month: May Year: 2004" (read 20261102 22:49 UTC)
4. https://www.ijcai.org/Proceedings/07/Papers/429.pdf : Banko et al., "Open Information Extraction from the Web", IJCAI-07: abstract, introduction (read 20261102 22:09 UTC)
5. https://aclanthology.org/P09-1113.pdf : Mintz et al., "Distant supervision for relation extraction without labeled data", ACL-IJCNLP 2009, 2-7 August 2009: abstract (read 20261102 22:09 UTC)
6. https://arxiv.org/abs/2305.05003 : Wadhwa, Amir and Wallace, "Revisiting Relation Extraction in the era of Large Language Models", v1 8 May 2023, ACL 2023: abstract (read 20261102 22:06 UTC)
7. https://arxiv.org/abs/2305.13168 : Zhu et al., "LLMs for Knowledge Graph Construction and Reasoning", v1 22 May 2023: abstract (read 20261102 22:10 UTC)
8. https://arxiv.org/abs/2510.10114 : Zhuang et al., "LinearRAG", v1 11 October 2025: abstract (read 20261102 22:06 UTC)
