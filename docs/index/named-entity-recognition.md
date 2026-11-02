---
type: index
kind: concept
aliases: [NER, NERC]
updated: 20261102 21:27 UTC
---

# Named-entity recognition

Named-entity recognition (NER) is the task of finding names in text and giving each a type, such as person, place or organisation. This entry gives the term's origin, its dated steps and where sources differ on what counts as an entity.

## Definition

A 2020 survey defines NER as the task of recognising "mentions of rigid designators from text belonging to predefined semantic types", for example person, location and organization [1]. The term "named entity" was coined for the Sixth Message Understanding Conference (MUC-6) [2]. That evaluation defined the task as identifying the names of all people, organizations and geographic locations in a text, and its final specification added time, currency and percentage expressions [3].

## How it changed

- **1991.** Rau presents one of the first papers on the task, a company-name recogniser built on heuristics and handcrafted rules [2].
- **199509.** The MUC-6 formal evaluation includes a named-entity task. Its best system scored 96% recall and 97% precision on Wall Street Journal texts (first-party report by the organisers) [3]. Era: [The Web changes data and search](../history/the-web.md).
- **2003 (paper posted to arXiv 20030612).** The CoNLL-2003 shared task makes the task language-independent, with English and German data and four types: persons, locations, organizations and a miscellaneous group [4]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **Survey of 1991 to 2006.** Early systems used handcrafted rules; "modern systems most often resort to machine learning" [2]. Its publication year is unstated in the text read.
- **20200318.** A survey (arXiv 1812.09449, first posted 20181222, version 3 of this date) reports that deep learning yields state-of-the-art NER, "starting with Collobert et al." [1]. The year deep-learning NER began is unstated in the sources read. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20231114.** GLiNER, a compact bidirectional-encoder model, is posted to arXiv. It finds entities of any type named at run time, where traditional models are limited to predefined types (first-party) [5]. For its results see the project page [GLiNER](../projects/gliner.md); still moving: see the trend [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

## Where sources disagree

What counts as an entity differs by source. The MUC-6 task includes numeric and time expressions [3]; the 2020 survey restricts the definition to rigid designators of predefined types [1]; CoNLL-2003 uses four types, one of them a catch-all [4]. The GLiNER authors treat "predefined entity types" as the limit of traditional models [5].

## Related

[BERT](./bert.md), [large language model](./large-language-model.md), [knowledge graph](./knowledge-graph.md), [GraphRAG](./graphrag.md), [question answering](./question-answering.md); the project [GLiNER](../projects/gliner.md); the trend [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md) and its [papers](../papers/llm-kg-construction.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md)

**Projects**

- [GLiNER](../projects/gliner.md)
- [Projects](../projects/README.md)

**Datasets**

- [2WikiMultiHopQA](../datasets/2wikimultihopqa.md)

**Applied to Pinakes**

- [What Pinakes should measure next](../applied-to-pinakes/next.md)
- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Distant supervision](distant-supervision.md)
- [Entity](entity.md)
- [Entity linking](entity-linking.md)
- [Gleaning](gleaning.md)
- [Relation extraction](relation-extraction.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/1812.09449 : Li, Sun, Han, Li, "A Survey on Deep Learning for Named Entity Recognition", IEEE TKDE 2020, arXiv 1812.09449 v3 of 20200318: abstract and introduction (definition, term first used at MUC-6, deep learning "starting with Collobert et al."); posting dates 20181222 and 20200318 from the arXiv API record (read 20261102 21:24 UTC)
2. https://nlp.cs.nyu.edu/sekine/papers/li07.pdf : Nadeau and Sekine, "A survey of named entity recognition and classification": introduction and section 1 (term coined for MUC-6; Rau 1991; rules then machine learning) (read 20261102 20:54 UTC)
3. https://aclanthology.org/C96-1079.pdf : Grishman and Sundheim, "Message Understanding Conference-6: A Brief History", COLING proceedings (year printed in the text read: unstated; Nadeau and Sekine cite it as 1996): the named-entity task, formal evaluation of September 1995, results of 96% recall and 97% precision; both authors confirmed from the address block (read 20261102 21:24 UTC)
4. https://arxiv.org/pdf/cs/0306050 : Tjong Kim Sang and De Meulder, "Introduction to the CoNLL-2003 Shared Task: Language-Independent Named Entity Recognition", arXiv cs/0306050 v1 of 20030612 (read 20261102 20:54 UTC)
5. http://export.arxiv.org/api/query?id_list=2311.08526 : arXiv record of Zaratiana et al., "GLiNER: Generalist Model for Named Entity Recognition using Bidirectional Transformer", published 20231114; abstract only (read 20261102 21:24 UTC)
