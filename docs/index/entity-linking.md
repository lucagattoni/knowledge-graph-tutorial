---
type: index
kind: concept
aliases: [grounding, entity disambiguation, named entity disambiguation, EL]
updated: 20261102 22:26 UTC
---

# Entity linking

This entry says what entity linking is, which other names cover the same step, and how its methods moved from Wikipedia-based ranking to language models. Without this step, graphs built from text can end up with several nodes for one thing [2].

## Definition

Entity linking is "the task to link entity mentions in text with their corresponding entities in a knowledge base" (Shen, Wang and Han) [1]. Hogan et al. name two difficulties: one entity has several mentions, and one mention can name several entities. Their linking therefore includes a disambiguation phase in which candidate nodes are ranked and the likeliest one is chosen [2]. It usually follows [named-entity recognition](./named-entity-recognition.md) [2]. OntoGPT's SPIRES paper calls the same step grounding: named entities "mapped to an identifier in an existing vocabulary, ontology, or database" [3].

## How it changed

- **200604.** Bunescu and Pasca use Wikipedia to detect and disambiguate named entities (EACL 2006) [4]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **200706.** Cucerzan's system recognises and disambiguates entities from Wikipedia data and notes that the task resembles word sense disambiguation (EMNLP-CoNLL, Prague) [5].
- **2014 to 2015.** Shen et al. publish a survey; OpenAlex dates it 20140530, Crossref the issue 201502 (IEEE TKDE 27(2)) [1][6].
- **20191110.** BLINK links with a bi-encoder for retrieval and a cross-encoder for re-ranking, with each entity given only a short description (first-party) [7]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20201002.** GENRE retrieves entities by generating their names token by token (first-party) [8].
- **20240220 (accepted).** The SPIRES paper uses grounding for ontology identifiers [3]. See [OntoGPT](../projects/ontogpt.md).
- **20260108.** LELA applies language models without any fine-tuning and reports results competitive with fine-tuned linkers (first-party) [9]. Still moving: [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

## Where sources disagree

**Name and scope.** "Entity linking" [1][2], "named entity disambiguation" [4][5] and "grounding" [3] cover overlapping tasks. Cucerzan's system does recognition and disambiguation together [5]; Hogan et al. treat them as two steps [2]. GENRE separates entity disambiguation from end-to-end linking [8].

**A name with no entry.** Hogan et al. let a recognised name become a new node, an "emerging entity", instead of linking it [2]. OntoGPT marks a name it cannot ground with an `AUTO:` prefix, not a guess [10].

## Related

[Entity](./entity.md), [named-entity recognition](./named-entity-recognition.md), [relation extraction](./relation-extraction.md), [word sense disambiguation](./word-sense-disambiguation.md), [knowledge graph](./knowledge-graph.md), [Wikidata](./wikidata.md), [ontology](./ontology.md), [distant supervision](./distant-supervision.md). Benchmark: [KILT](../benchmarks/kilt.md). Data: [YAGO](../datasets/yago.md). Trend: [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Graph features removed and added](../trends/features-in-and-out.md)

**Projects**

- [OntoGPT](../projects/ontogpt.md)

**Datasets**

- [MuSiQue](../datasets/musique.md)
- [TriviaQA](../datasets/triviaqa.md)
- [WebQuestionsSP](../datasets/webquestionssp.md)
- [YAGO](../datasets/yago.md)

**Benchmarks**

- [KILT](../benchmarks/kilt.md)

**Index**

- [Distant supervision](distant-supervision.md)
- [Entity](entity.md)
- [LinkML](linkml.md)
- [Relation extraction](relation-extraction.md)
- [Semantic parsing](semantic-parsing.md)
- [Slot filling](slot-filling.md)
- [Word sense disambiguation](word-sense-disambiguation.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.openalex.org/works/doi:10.1109/tkde.2014.2327028 : OpenAlex record of Shen, Wang, Han, "Entity Linking with a Knowledge Base: Issues, Techniques, and Solutions": abstract text and publication date 2014-05-30; the paper's body was not read (read 20261102 22:16 UTC)
2. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", ACM Computing Surveys 54(4), 2021 (arXiv v6 of 11 September 2021): section 6.2.2 and 6.2.3, named-entity recognition and entity linking, the two challenges, emerging entities (read 20261102 22:08 UTC)
3. https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10924283/fullTextXML : Caufield et al., "Structured Prompt Interrogation and Recursive Extraction of Semantics (SPIRES)", Bioinformatics 40(3), btae104, 2024 (received 4 May 2023, accepted 20 February 2024): methods, grounding of named entities (read 20261102 22:16 UTC)
4. https://aclanthology.org/E06-1002.pdf : Bunescu and Pasca, "Using Encyclopedic Knowledge for Named Entity Disambiguation", EACL 2006 (Trento, April 2006; venue and month from the anthology page https://aclanthology.org/E06-1002/): abstract (read 20261102 22:15 UTC)
5. https://aclanthology.org/D07-1074.pdf : Cucerzan, "Large-Scale Named Entity Disambiguation Based on Wikipedia Data", EMNLP-CoNLL 2007 (Prague, June 2007): abstract; introduction, similarity to word sense disambiguation (read 20261102 22:07 UTC)
6. https://api.crossref.org/works/10.1109/tkde.2014.2327028 : Crossref search record: IEEE TKDE vol. 27, issue 2, pages 443-460, issued 2015-02 (read 20261102 22:16 UTC)
7. https://arxiv.org/abs/1911.03814 : Wu et al., "Scalable Zero-shot Entity Linking with Dense Entity Retrieval", arXiv v1 of 20191110 (EMNLP 2020): abstract (first-party; read 20261102 22:16 UTC)
8. https://arxiv.org/abs/2010.00904 : De Cao et al., "Autoregressive Entity Retrieval", arXiv v1 of 20201002 (ICLR 2021): abstract (first-party; read 20261102 22:16 UTC)
9. https://arxiv.org/abs/2601.05192 : Haffoudhi, Suchanek, Holzenberger, "LELA: an LLM-based Entity Linking Approach with Zero-Shot Domain Adaptation", arXiv v1 of 20260108, v2 of 20260806 (ISWC 2026): abstract (first-party; read 20261102 22:16 UTC)
10. https://github.com/monarch-initiative/ontogpt : OntoGPT README by `gh api`, "Grounding without hallucination": a name that cannot be grounded gets the `AUTO:` prefix (read 20261102 22:23 UTC)
