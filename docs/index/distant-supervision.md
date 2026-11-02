---
type: index
kind: concept
aliases: [DS, weakly labeled data]
updated: 20261102 22:52 UTC
---

# Distant supervision

This entry says what distant supervision is, who named it, and how far the word has moved from its first use.

## Definition

Distant supervision builds training data without hand annotation: an existing database of facts is aligned with text, and the alignment supplies the labels [2][3]. Mintz et al. name it for relation extraction. Their intuition is that a sentence holding a pair of entities that stand in a known Freebase relation probably expresses that relation [1]. The labels are noisy: Surdeanu et al. cite Riedel et al. for up to 31% false positives when Freebase is matched with New York Times articles [2].

## How it changed

- **1999.** Craven and Kumlien train fact extractors on "weakly" labeled data: the Yeast Protein Database's localization facts paired with PubMed abstracts [4]. Month: unstated.
- **20090802 to 20090807 (conference dates).** Mintz et al. align Freebase with Wikipedia: 102 relations, 67.6% precision on 10,000 extracted instances (first-party) [1]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **2010.** Riedel et al. relax the assumption: a bag of sentences about one entity pair needs only "at least one" sentence that expresses the relation [3].
- **20120712 to 20120714 (conference dates).** Surdeanu et al. model all sentences and all labels of an entity pair together [2].
- **20170331 and 20170509.** Chen et al. attach paragraphs to question-answer pairs and discard those without an exact match of the answer [5]. Joshi et al. take the answer string's presence in a document as the label, "valid over 75% of the time" (first-party) [6]. See [TriviaQA](../datasets/triviaqa.md). Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20251008.** Senger et al. use the term for pseudo-labels written by a black-box language model; the abstract and introduction mention no knowledge base (first-party) [7]. Still moving: [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

## Where sources disagree

**Who started it.** Mintz et al. propose the name and call the idea "similar to" weakly labeled data in bioinformatics [1]. W. Hogan's survey says they "coin the term" [3]. Surdeanu et al. write that distant supervision for information extraction was introduced by Craven and Kumlien [2].

**What the label is.** A database fact aligned with text [1][2]; the presence of an answer string [5][6]; a language model's guess [7]. *Reading:* each later use keeps the automatic labelling and drops the knowledge base. No source read defines all three.

## Related

[Relation extraction](./relation-extraction.md), [named-entity recognition](./named-entity-recognition.md), [entity linking](./entity-linking.md), [knowledge graph](./knowledge-graph.md), [Freebase](./freebase.md), [Wikidata](./wikidata.md), [knowledge acquisition bottleneck](./knowledge-acquisition-bottleneck.md), [open-domain question answering](./open-domain-question-answering.md). Dataset: [TriviaQA](../datasets/triviaqa.md). Trend: [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md) and its [papers](../papers/llm-kg-construction.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Datasets**

- [TriviaQA](../datasets/triviaqa.md)

**Index**

- [Entity linking](entity-linking.md)
- [Relation extraction](relation-extraction.md)
- [Slot filling](slot-filling.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://aclanthology.org/P09-1113.pdf : Mintz, Bills, Snow, Jurafsky, "Distant supervision for relation extraction without labeled data", ACL-IJCNLP 2009 (Singapore, 2-7 August 2009): abstract; introduction (the proposal, the intuition, "similar to" weakly labeled data); Freebase and Wikipedia figures (read 20261102 22:07 UTC)
2. https://aclanthology.org/D12-1042.pdf : Surdeanu, Tibshirani, Nallapati, Manning, "Multi-instance Multi-label Learning for Relation Extraction", EMNLP-CoNLL 2012 (Jeju Island, 12-14 July 2012): abstract; introduction (up to 31% false positives, reported by Riedel et al.); related work (Craven and Kumlien 1999) (read 20261102 22:08 UTC)
3. https://arxiv.org/pdf/2207.08286 : W. Hogan, "An Overview of Distant Supervision for Relation Extraction with a Focus on Denoising and Pre-training Methods", arXiv 2207.08286 v1 of 20220717 (date from the arXiv API record): introduction (labels by alignment of a knowledge graph with text); Mintz et al. "coin the term"; Riedel et al. (2010) multi-instance learning (read 20261102 22:10 UTC)
4. https://www.aaai.org/Papers/ISMB/1999/ISMB99-010.pdf : Craven and Kumlien, "Constructing Biological Knowledge Bases by Extracting Information from Text Sources", ISMB-99 (copyright 1999 AAAI): "weakly" labeled training data; the Yeast Protein Database (read 20261102 22:08 UTC)
5. https://arxiv.org/pdf/1704.00051 : Chen, Fisch, Weston, Bordes, "Reading Wikipedia to Answer Open-Domain Questions", ACL 2017, arXiv v1 of 20170331 (date from the arXiv API record, read 20261102 22:09 UTC): section 4.4, distant supervision, paragraphs without an exact match of the answer discarded (read 20261102 22:08 UTC)
6. https://arxiv.org/pdf/1705.03551 : Joshi, Choi, Weld, Zettlemoyer, "TriviaQA", arXiv v1 of 20170509 (date from the arXiv API record, read 20261102 22:09 UTC): the answer-string assumption, "valid over 75% of the time" (read 20261102 22:08 UTC)
7. https://arxiv.org/pdf/2510.06838 : Senger, Campbell, van der Goot, Plank, "Crossing Domains without Labels: Distant Supervision for Term Extraction", arXiv v1 of 20251008: abstract and introduction (pseudo-labels from a black-box LLM; no knowledge base mentioned); venue, EMNLP 2025 Industry Track, from the comment on the arXiv listing https://arxiv.org/abs/2510.06838 (first-party; read 20261102 22:51 UTC)
