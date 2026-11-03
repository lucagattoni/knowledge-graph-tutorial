---
type: dataset
kinds: [kg]
benchmark: kg-link-prediction
updated: 20261102 21:26 UTC
---

# WN18RR

This page answers what the WN18RR data contains, how it was cut from [WordNet](wordnet.md), and what its licence status is. It is a set of about 93 thousand [triples](../index/triple.md) between word senses, used to test [link prediction](../index/link-prediction.md). It replaced WN18, whose test set leaked answers through inverse relations. Scores and protocol are on [the link-prediction benchmark page](../benchmarks/kg-link-prediction.md).

## What it contains

Each line is a triple of two WordNet synsets (word senses) and a lexical relation [3]. There are 11 relation types. Counted in the training file [3]:

| Relation | Training triples |
|---|---|
| hypernym | 34,796 |
| derivationally related form | 29,715 |
| member meronym | 7,402 |
| has part | 4,816 |
| synset domain topic of | 3,116 |
| instance hypernym | 2,921 |
| also see | 1,299 |
| verb group | 1,138 |
| member of domain region | 923 |
| member of domain usage | 629 |
| similar to | 80 |

Hypernym and derivationally related form together make 74% of the training triples (own sum from the counts) [3]. The parent set WN18 "tends to follow a strictly hierarchical structure" [4].

## Size and versions

| Split | Triples |
|---|---|
| Train | 86,835 |
| Validation | 3,034 |
| Test | 3,134 |
| Total | 93,003 |

There are 40,943 entities and 11 relations, counted from the files [3]. The ConvE paper gives the same totals [4], as does Rossi et al.'s dataset table [7].

Unseen entities: 210 validation and 210 test triples contain an entity absent from training; 209 distinct test entities are unseen [3]. The ConvE README says "212 entities" and about 6.7% of the test set; 210 of 3,134 is 6.7% [2]. The gap between 209 and 212 is unexplained here.

The predecessor WN18 has 18 relations, 40,943 entities and 151,442 triples (141,442 / 5,000 / 5,000) [4][5]. The TransE paper calls it "WN", the data version of an earlier paper; the WordNet release is unstated [5]. WN18RR has no version number. Its paper is ConvE, arXiv v1 5 July 2017, v6 4 July 2018 [4][12].

## Licence

**Unstated** for the dataset. The ConvE repository that redistributes it has an MIT `LICENSE` file; whether it covers the data is unstated [2].

For context only: WordNet's own licence, read through SPDX, grants use, copying, modification and distribution "for any purpose and without fee or royalty" if the copyright notice and disclaimer are kept. It names WordNet 3.0, copyright 2006 [8]. Princeton's own licence page answered HTTP 403 [8]. Which WordNet release WN18RR comes from, and whether the notice duty carries over, is unstated.

## How it was made

Dettmers et al. first measured the leak. A rule-based "inverse model", which only guesses that a test triple is the reverse of a training triple, matched the state of the art on WN18 and FB15k [4]. Toutanova and Chen had found that 94% of WN18 test triples (81% for FB15k) had their entity pair linked in training [1][4]. The authors then built WN18RR "to reclaim WN18 as a dataset" [4]. Rossi et al. describe the pipeline as similar to the one for [FB15k-237](fb15k-237.md) [7]. The exact removal rule is not given in the passages read.

The inverse model still does well on WN18RR; its scores are on the [benchmark page](../benchmarks/kg-link-prediction.md). The authors blame symmetric relations such as "similar to", which the procedure does not remove [4].

## Used by

- **Papers.** ConvE introduced it and recommends it over WN18 [4]. Sun et al. [6], Rossi et al. [7], the LibKGE results [9] and SimKGC [10] report on it. The parent set comes from the [TransE paper](../papers/foundations.md) [5].
- **Trends.** No trend page of this documentation is built on it (checked in the trends folder, 20261102).
- **Benchmarks.** [Knowledge graph link prediction](../benchmarks/kg-link-prediction.md).
- **Citations.** The ConvE paper has 3,294 citations in Semantic Scholar (read 20261102 19:51 UTC; carried over from the research notes of this documentation, not re-queried here and not checked against the API by this page) [11].

## Known problems

- **Unseen entities.** About 6.7% of test triples have an entity with no training embedding, so they are hard to predict [2][3]. Dropping them from the test set raises scores in LibKGE's experience; the size of the effect is on the [benchmark page](../benchmarks/kg-link-prediction.md) [9].
- **Narrow graph.** Three relations carry 83% of the training triples (own sum from the table above), and 11 relations is a small vocabulary [3].
- **Pre-trained inputs.** CapsE starts from GloVe word vectors on WN18RR, which Sun et al. call unfair to the other models [6].
- **Evaluation.** Tie handling changed published numbers; see the benchmark page [6].
- **Age.** The licence text names WordNet 3.0 of 2006 [8]; the release behind WN18RR is unstated.

## Sources

1. https://aclanthology.org/W15-4007.pdf : Toutanova and Chen, CVSC 2015: "% test linked" for WN18 (94.0), FB15k, FB15k-237 (full text, read 20261102 20:49 UTC)
2. https://github.com/TimDettmers/ConvE : README: 212 entities, 6.7%, "do not use" note for WN18; MIT `LICENSE`; GitHub API: MIT (read 20261102 20:50 UTC)
3. `WN18RR.tar.gz` from the repository in 2, extracted and counted with a script (read 20261102 20:50 UTC)
4. https://arxiv.org/pdf/1707.01476 : Dettmers et al., ConvE v6: datasets, inverse model, WN18RR (full text, read 20261102 20:49 UTC)
5. https://papers.nips.cc/paper_files/paper/2013/file/1cecc7a77928ca8133fa24680a88d2f9-Paper.pdf : Bordes et al., TransE: "WN" data and Table 2 (full text, read 20261102 20:51 UTC)
6. https://arxiv.org/pdf/1911.03903 : Sun et al., v3 (8 July 2020): CapsE and GloVe note (read 20261102 20:48 UTC)
7. https://arxiv.org/pdf/2002.00819 : Rossi et al., v4 (21 January 2021): Table 2 and dataset descriptions (read 20261102 20:50 UTC)
8. https://spdx.org/licenses/WordNet.html : WordNet licence text; https://wordnet.princeton.edu/license-and-commercial-use returned HTTP 403 (read 20261102 20:52 UTC)
9. https://raw.githubusercontent.com/uma-pi1/kge/master/README.md : LibKGE results and the unseen-entity note (read 20261102 20:51 UTC)
10. https://arxiv.org/pdf/2203.02167 : SimKGC, Table 3 (full text, read 20261102 20:51 UTC)
11. https://api.semanticscholar.org/graph/v1/paper/arXiv:1707.01476?fields=citationCount : lookup that returns the citation count of the ConvE paper; the count 3,294 comes from the research notes of this documentation (read 20261102 19:51 UTC; one note gives 20:00 UTC for the same count; no archive page holds it)
12. https://export.arxiv.org/api/query?id_list=1707.01476 : arXiv versions of ConvE (read 20261102 20:51 UTC)
