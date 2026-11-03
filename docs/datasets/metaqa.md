---
type: dataset
kinds: [questions, kg]
updated: 20261102 21:26 UTC
---

# MetaQA

This page answers what the MetaQA data contains, how big it is, under which terms it is released, how it was made and where it is weak. MetaQA is a set of about 407,500 movie questions of one, two and three hops, written from templates over a small movie [knowledge graph](../index/knowledge-graph.md), in text, paraphrased-text and audio form. It has no benchmark page in this documentation, so this page describes the splits and the metric but gives no system results.

## What it contains

All questions are generated from the WikiMovies knowledge base, which the release ships as `kb.txt`, one [triple](../index/triple.md) per line in the form `subject|relation|object` [1]. In the question text the entity is marked with square brackets, for example `[Joe Thomas] appears in which movies`; a question can have several answers [1].

It is a [multi-hop question answering](../index/multi-hop-question-answering.md) set: a 2-hop question follows two edges, for example from a director to a film to its actors [2]. There are three components [1][2]:

| Component | What it is |
|---|---|
| Vanilla | the template questions; 1-hop is the WikiMovies set, 2-hop has 21 question types and 3-hop has 15, each with 10 templates |
| NTM | each vanilla question translated to French and back to English by a neural translation model, with the entity kept |
| Audio | each vanilla question read by a text-to-speech service, with extracted audio features; the KB entities have audio too |

Question-type files let scores be split by type [1].

## Size and versions

| | 1-hop | 2-hop | 3-hop |
|---|---:|---:|---:|
| Train | 96,106 | 118,980 | 114,196 |
| Dev | 9,992 | 14,872 | 14,274 |
| Test | 9,947 | 14,872 | 14,274 |

The README and the paper's Table 3 give the same counts [1][2]. Their sum (computed here) is 407,513 questions (the paper says "more than 400K") [2]. All components share one split [1]. The 1-hop set drops the WikiMovies questions whose entity names are also ordinary words, so it is "slightly smaller" than WikiMovies [1][2].

The paper's protocol is hits@1 on the test split, in four settings: Vanilla (topic entity labelled), Vanilla-EU (entity unlabelled), NTM-EU and Audio-EU [2].

**Unstated:** the size of the knowledge base; any dataset version number. The repository was last pushed on 20211010 and holds two files, `README.md` and `LICENSE.txt` [3]. The data itself sits in a Google Drive folder [1].

## Licence

The README says "This data is released under the Creative Commons Public License. A copy is included with the data" [1]. The repository's `LICENSE.txt` is the legal text of Creative Commons Attribution 3.0 Unported, headed "THE METAQA DATASET", with a note to read the WikiMovies README, on which the data is partly based [4]. GitHub does not detect a licence for the repository [3]. WikiMovies' own terms are **unstated** in the sources read.

## How it was made

The 1-hop set is the `wiki_entities` branch of WikiMovies, with entities marked automatically by left-to-right longest match of entity names [1][2]. The 2-hop and 3-hop sets are generated from paths in the same knowledge base: one of 10 templates per fixed question type is drawn at random [2]. The NTM and audio sets are produced by machine from the vanilla questions [1][2]. The sources read describe no human writing or checking of the new questions; the 1-hop questions are inherited from WikiMovies.

## Used by

- **Paper.** Zhu et al. test ChatGPT and GPT-4 on MetaQA, with 20 random questions drawn from it, next to FB15k-237 for link prediction [5] ([papers](../papers/llm-kg-construction.md)).
- **Dataset.** The 2WikiMultiHopQA paper names MetaQA as an earlier multi-hop set over a knowledge base ([2WikiMultiHopQA](2wikimultihopqa.md)) [6].
- **Audit.** A 2025 audit of 16 knowledge-graph QA sets includes it [7].

## Known problems

- **Templates.** Language is narrow: the paper itself calls the WikiMovies templates "easy to be exploited by models" and builds the 2-hop and 3-hop sets the same way [2].
- **Memorisation.** The paper's Table 4 gives "New entity pairs in test (%)" as 34.5 (1-hop), 28.6 (2-hop) and 32.2 (3-hop) [2]. Reading "new" as "not in training" (an inference; the paper does not define it), between 65% and 72% of test pairs were seen in training (computed here: 65.5, 71.4, 67.8). The authors say a big portion of questions "can be answered by just memorizing the pairs in training data" [2].
- **Label quality, third party.** The audit judged 20.00% of 60 sampled test items correct, with an example whose film list stops before a 2023 release [7]. Its text says 25% in one place and the table 20.00%; the sample is small [7].
- **One domain.** Only movies [1]. The paper says its 1-hop set "is the same as WikiMovies", while its appendix and the README say it is slightly smaller [1][2].

## Sources

1. https://github.com/yuyuz/MetaQA : README: download link, licence sentence, AAAI 2018 citation, components, counts, `kb.txt` format (read 20261102 20:52 UTC)
2. https://arxiv.org/abs/1709.04071 : Zhang, Dai, Kozareva, Smola, Song, "Variational Reasoning for Question Answering with Knowledge Graph", AAAI 2018; arXiv v1 12 Sep 2017, v5 27 Nov 2017; full text: Tables 1, 2, 3, 4, Section 6.1, Appendix A (Table 4 and the memorising sentence re-read 20261102 21:24 UTC; the rest read 20261102 20:53 UTC)
3. https://api.github.com/repos/yuyuz/MetaQA : licence field "NOASSERTION", last push 20211010, file list (read 20261102 20:52 UTC, via `gh api`)
4. https://github.com/yuyuz/MetaQA/blob/master/LICENSE.txt : Creative Commons Attribution 3.0 Unported text, "THE METAQA DATASET" (read 20261102 20:52 UTC)
5. https://arxiv.org/abs/2305.13168 : Zhu et al., full text of v4: question answering with FreebaseQA and MetaQA, 20 instances each, Appendix B (read 20261102 20:55 UTC)
6. https://arxiv.org/abs/2011.01060 : 2WikiMultiHopQA paper, related work, the sentence on MetaQA (read 20261102 20:55 UTC)
7. https://arxiv.org/abs/2505.23495 : "Diagnosing and Addressing Pitfalls in KG-RAG Datasets" v4 (3 November 2025): Table 1, Section 3.1, Appendix C (read 20261102 20:55 UTC)