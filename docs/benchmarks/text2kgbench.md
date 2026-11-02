---
type: benchmark
datasets: []
updated: 20261102 21:32 UTC
---

# Text2KGBench

This page answers whether a [language model](../index/large-language-model.md) can turn sentences into [triples](../index/triple.md) that follow a given [ontology](../index/ontology.md), and how Text2KGBench scores that. Its two datasets are used only inside its own protocol, so they are described here. On the original data only the authors' two 2023 baselines were found; newer numbers come from a revised copy.

## What it tests

Given an ontology and a sentence, the system must extract the facts the sentence states, using the ontology's relation names [1]. The paper names three expectations: follow the ontology, stay faithful to the sentence even where pre-training knowledge disagrees, and invent no entities or relations [1]. It is [relation extraction](../index/relation-extraction.md) with the ontology as an input [1]. Accepted at ISWC 2023 (Resources Track); first posted 20230804 [1].

## Tasks, metrics and protocol

- **Input and output.** Ontology (concepts, canonical relation names, domain and range), sentences, and training pairs as examples. Output: triples written `relation(subject, object)` [1].
- **Fact accuracy.** Precision, recall and F1 against the ground truth. Scoring is "locally closed": only relations that occur in the ground truth count, because the gold triples are not exhaustive. An empty output scores 0 [1].
- **Ontology conformance (OC).** The share of output triples whose relation is canonical in the ontology. Domain and range are not yet checked [1].
- **Hallucination.** Subject (SH) and object (OH): the stemmed term is not a substring of the sentence or the ontology concepts. Relation (RH): not in the ontology, so RH equals 1 minus OC [1].
- **Baselines.** A fixed prompt: instruction, ontology, the most similar training sentence (SBERT T5-XXL), the test sentence. Prompts, outputs and scripts are released [1].

## Datasets

- **Wikidata-TekGen.** 10 ontologies, 13,474 aligned sentences [1]. Each ontology was written by hand from [Wikidata](../datasets/wikidata.md) property pages by one author and reviewed by two [1]. Sentences come from the TekGen corpus (distant supervision, 16 million alignments, 663 relations) [1]. Extra test sets: 939 verified alignments and 174 invented "unseen" sentences [1].
- **DBpedia-WebNLG.** 19 ontologies, one per WebNLG category, 4,860 sentences from the WebNLG 3.0 English three-triple split; no fact is in both train and test. WebNLG's crowdsourced checks replaced a manual one [1].
- **Splits and version.** Stratified random folds into train, validation and test [1]. DBpedia-WebNLG: 2,014 test and 2,846 train sentences (6,259 test and 8,623 train triples), from Table 3 of the LettrIA paper, which keeps the same sentence counts [7]. Wikidata-TekGen: the original paper gives per-ontology sentence totals only, so the split sizes are **unstated** [1]. Zenodo record 7916716, v1.0, 20230509, a 5,887,337-byte zip [2].
- **Licence.** Code: Apache-2.0 in the `LICENSE` file [3]. Data: Zenodo says CC BY 4.0 [2]; the README contradicts itself (badge "CC BY 4.0", text "Attribution-ShareAlike 4.0") and says the data derives from TekGen and WebNLG 3.0 [3]. TekGen's README says CC BY-SA 2.0 [4]; WebNLG's says CC BY-NC-SA 4.0 [5]. *Reading:* the WebNLG half is non-commercial, so this documentation uses the benchmark as a read-only reference: ideas and results only.

## Results

The blocks use different data and cannot be compared.

**Block A. Original data, Table 2 of the paper [1].** Averages over ontologies; the authors' own baselines. Score order: P / R / F1; OC; SH / RH / OH.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Vicuna-13B, TekGen, all | .38 / .34 / .35; .83; .17 / .17 / .17 | seven metrics | benchmark authors | yes | 20230804 | [1] |
| Vicuna-13B, TekGen, 939 verified | .42 / .39 / .38; .84; .11 / .16 / .14 | same | same | yes | 20230804 | [1] |
| Vicuna-13B, TekGen, 174 unseen | .32 / .32 / .32; .86; .07 / .14 / .14 | same | same | yes | 20230804 | [1] |
| Alpaca-LoRA-13B, TekGen, all | .32 / .26 / .27; .87; .18 / .13 / .17 | same | same | yes | 20230804 | [1] |
| Vicuna-13B, WebNLG | .34 / .27 / .30; .93; .12 / .07 / .28 | same | same | yes | 20230804 | [1] |
| Alpaca-LoRA-13B, WebNLG | .32 / .23 / .25; .91; .16 / .09 / .38 | same | same | yes | 20230804 | [1] |

**Block B. Text2KGBench-LettrIA, a revised DBpedia-WebNLG part, Table 1 of its paper [7].** Values are entity F1 / relation F1.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Mistral-Small-3.2, fine-tuned | .8837 / .8294 | entity F1 / relation F1 | LettrIA and EURECOM authors | yes, for their revision; not the original authors | 20251102 | [7] |
| Qwen3-14B, fine-tuned | .8688 / .8067 | same | same | same | 20251102 | [7] |
| Qwen3-0.6B, fine-tuned | .8272 / .7059 | same | same | same | 20251102 | [7] |
| GPT-4.1-mini, one-shot | .6866 / .6114 | same | same | same | 20251102 | [7] |
| Gemini 2.5 Pro, one-shot | .6595 / .7076 | same | same | same | 20251102 | [7] |
| Claude Sonnet 4, one-shot | .6487 / .7126 | same | same | same | 20251102 | [7] |

*Reading:* no independent result on the original data was found. Block B's gap mixes two things: the fine-tuned models trained on the benchmark's training split, and the closed models got one example and the authors' production prompt [7].

## Known problems

- **Noisy alignments.** TekGen pairs come from distant supervision; the authors' example is a sentence aligned to the wrong person, hence the 939-sentence subset [1].
- **Memorisation.** Models may have seen the sentences; the 174 unseen ones only partly answer this [1].
- **Hallucination metric.** Stemmed substring matching gives false positives when a model expands an acronym [1]. Independent authors call its reliance on the ground-truth sentence and ontology a possible limit when the two disagree [8].
- **Interested revisers.** LettrIA reports flat ontologies, inconsistent annotation, formatting errors and a complicated URI scheme [7]. The paper is by LettrIA, whose internal production prompt was used for the closed models, and the revised data are "available upon request" [7].
- **Text and table disagree.** LettrIA's text credits the top entity F1, 0.8837, to the "(ext.)" model; its table puts it on the plain row (the "(ext.)" row has 0.8764). This page follows the table [7].
- **Small ontologies.** Kept small to fit prompts [1]; LettrIA lists binary-only relations as a limit [7]. The README names no leaderboard [3].

## Used by

LettrIA revises its DBpedia-WebNLG part [6][7]. Ghanem and Cruz (2025) cite it and critique its hallucination metric, but test on WebNLG+2020 [8]. The trend [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md) and its [papers group](../papers/llm-kg-construction.md) place it. Signals: 149 citations (Semantic Scholar, read 20261102 20:00 UTC, carried over, a floor) [9]; repository 95 stars, last push 20240506, not archived [3].

## Sources

1. https://arxiv.org/abs/2308.02357 and https://arxiv.org/html/2308.02357 : task, metrics, data construction, sizes, split method, Tables 1 and 2, limitations, venue note (read 20261102 21:00 UTC; split method and totals re-read 20261102 21:30 UTC)
2. https://zenodo.org/api/records/7916716 : v1.0, 20230509, file size, licence cc-by-4.0 (read 20261102 21:00 UTC)
3. https://github.com/cenguix/Text2KGBench : `LICENSE` Apache-2.0, README licence text, 95 stars, pushed 20240506, no leaderboard (read 20261102 21:01 UTC)
4. https://github.com/google-research-datasets/KELM-corpus : README, TekGen under CC BY-SA 2.0 (read 20261102 21:06 UTC)
5. https://gitlab.com/shimorina/webnlg-dataset/-/raw/master/release_v3.0/README.md : WebNLG data under CC BY-NC-SA 4.0 (read 20261102 21:06 UTC)
6. https://www.eurecom.edu/en/node/4899768 : LettrIA record, abstract, 20251102 (read 20261102 21:01 UTC)
7. https://ceur-ws.org/Vol-4041/paper3.pdf : Text2KGBench-LettrIA, full text, Table 1, appendix Table 3 (sentence and triple counts per version), section 4.3 (production prompt), availability (read 20261102 21:02 UTC; Table 3 and section 4.3 re-read 20261102 21:29 UTC)
8. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12237976/ : Ghanem and Cruz, Frontiers in Big Data, 20250625, hallucination-metric critique, WebNLG+2020 (read 20261102 21:03 UTC)
9. Semantic Scholar batch API, `citationCount` for arXiv 2308.02357 : 149 (read 20261102 20:00 UTC, carried over from that day's research pool, a working file outside the repository; not re-queried; a floor)
