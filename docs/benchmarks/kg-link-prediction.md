---
type: benchmark
datasets: [fb15k-237, wn18rr]
updated: 20261102 21:26 UTC
---

# Knowledge graph link prediction

This page answers how a model is scored when it must fill in a missing entity of a [knowledge graph](../index/knowledge-graph.md) triple, and what the numbers read so far show. The numbers below are independent re-runs from 2019 to 2021, a toolkit table and first-party rows; no independent result newer than 2022 was read, and newer first-party results are unstated here.

## What it tests

It tests [knowledge graph completion](../index/knowledge-graph-completion.md) by [link prediction](../index/link-prediction.md): whether a model that saw the training triples can rank the true entity above all others for a hidden test triple. It uses no text and no questions. The filtered protocol below comes from the TransE paper of 2013 [3].

## Tasks, metrics and protocol

- **Task.** For each test triple (h, r, t), predict t from (h, r, ?), then h from (?, r, t). Every entity is a candidate [3][4].
- **Filtered setting.** Candidates that form another known true triple in train, validation or test are removed first. Without this, valid triples ranked above the test triple count as errors. The unfiltered version is called raw [3].
- **Metrics.** Mean rank, Hits@k (share of ranks at or below k) and [MRR](../index/mean-reciprocal-rank.md), the average inverse rank. Hyperparameters are chosen on the validation set [2].
- **Tie rule.** When candidates share a score, TOP puts the true one first, BOTTOM last, RANDOM at random. TOP gives a perfect score to a model that outputs a constant. Sun et al. recommend RANDOM [4].
- **Scores below** are filtered MRR, FB15k-237 first, then WN18RR (then YAGO3-10 where given).

## Datasets

The tables use the standard train, validation and test files of [FB15k-237](../datasets/fb15k-237.md) and [WN18RR](../datasets/wn18rr.md); their content, versions and flaws are on those pages.

**YAGO3-10** has no page here. It is a subset of YAGO3 (entities with at least 10 relations): 123,182 entities, 37 relations, 1,079,040 training and 5,000 validation and test triples [5]. YAGO 3 is licensed CC BY 3.0 [7]; a licence for the subset is unstated. Two near-duplicate relations, `isAffiliatedTo` and `playsFor`, make up 35% and 30% of training and over 63% of test triples [6].

## Results

No row is a leaderboard entry; each comes from a paper or a README. Rows in different blocks differ in tuning budget, so compare within a block.

**A. Independent re-evaluation, RANDOM tie rule (Sun et al., v1 20191110, v3 20200708) [4].**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| TuckER | .353 / .461 | MRR | Sun et al. | no | 20200708 | [4] Tables 2, 3 |
| RotatE | .336 / .473 | MRR | Sun et al. | partly: Sun is RotatE's first author [10] | 20200708 | [4] |
| ConvE | .324 / .444 | MRR | Sun et al. | no | 20200708 | [4] |
| CapsE | .150 / .415 | MRR (reported .523 / .415) | Sun et al. | no | 20200708 | [4] |
| KBAT | .157 / .412 | MRR (reported .518 / .440; original code leaked test data) | Sun et al. | no | 20200708 | [4] |

**B. Independent comparison, full rankings (Rossi et al., v1 20200203, v4 20210121) [5].** Models whose own code broke ties by "min" are reported under an average policy.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| TuckER | .352 / .459 / .544 | MRR, FB15k-237 / WN18RR / YAGO3-10 | Rossi et al. | no | 20210121 | [5] Table 3 |
| ComplEx | .349 / .458 / .576 | same | Rossi et al. | no | 20210121 | [5] |
| RotatE | .336 / .475 / .498 | same | Rossi et al. | no | 20210121 | [5] |
| AnyBURL (rules, no embeddings) | .324 / .485 / .528 | same; 1,000 s training on FB15k-237 and YAGO3-10 | Rossi et al. | no | 20210121 | [5] |
| ConvE | .305 / .427 / .488 | same | Rossi et al. | no | 20210121 | [5] |
| TransE | .31 / .206 / .501 | same | Rossi et al. | no | 20210121 | [5] |

**C. LibKGE toolkit table, one tuning setup for every model, test set including unseen entities [8].**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| RESCAL | .356 / .467 | MRR | LibKGE team | model no; toolkit yes | undated; repository pushed 20260401 | [8] |
| ComplEx | .348 / .475 | MRR | LibKGE team | same | same | [8] |
| ConvE | .339 / .442 | MRR | LibKGE team | same | same | [8] |
| RotatE | .333 / .478 | MRR | LibKGE team | same | same | [8] |

**D. First-party results and baselines.**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| ConvE | .325 / .43 | MRR | ConvE authors | yes | 20180704 (v6) | [2] Table 4 |
| Inverse-relation rule | .010 / .35 | MRR (v6 numbers, corrected 20180328 after a bugfix) | ConvE authors | yes, a baseline | 20180704 (v6) | [2] Table 4 |
| Frequency baseline, no learning | .236 / n.a. | MRR; RESCAL scores .356 in the same study | CoDEx authors | yes, for a rival dataset | 20200916 | [9] Table 7 |
| SimKGC (IB+PB+SN; uses entity descriptions) | .336 / .666 | MRR; variant IB scores .333 / .671 | SimKGC authors | yes | 20220304 | [11] Table 3 (paper lists WN18RR first) |

*Reading:* for the named models TuckER, ComplEx, RotatE, ConvE and RESCAL, MRR sits between .30 and .36 on FB15k-237 and between .43 and .48 on WN18RR once ties are random. TransE (.206 on WN18RR), CapsE and KBAT fall outside that range. Among those five, the spread on FB15k-237 (about .05) is not much larger than the spread for ConvE alone across three independent setups (.305, .324, .339; its authors report .325). AnyBURL is within .03 of the best embedding on FB15k-237 and above every embedding of block B on WN18RR [5]. SimKGC's .666 on WN18RR uses text the others do not see.

## Known problems

- **Ties.** The advertised .5 on FB15k-237 for CapsE and KBAT fell below .16 under RANDOM [4].
- **Tuning.** Tuned DistMult beat almost all models published on FB15k (Kadlec et al., 20170530) [1]. Rossi et al. hand-tuned within a time budget [5].
- **Skewed test sets.** Aggregate scores are dominated by over-represented entities [5].
- **Unseen entities.** Dropping them raises WN18RR MRR by about 3 points [8].
- **Dataset flaws.** See the [FB15k-237](../datasets/fb15k-237.md) page; YAGO3-10 duplicate relations are above [6].
- **Metrics disagree.** A 2025 paper notes that MRR and Hits@1 can rank models differently and proposes a meta-metric (abstract only read) [12].
- **Not comparable with OGB.** [OGB](ogb-link-prediction.md) ranks the true entity against 1,000 sampled negatives, not all entities [13].

## Used by

Models introduced in [Knowledge graph embedding](../index/knowledge-graph-embedding.md) papers, from TransE (see the [foundations papers](../papers/foundations.md)) to SimKGC. No trend page of this documentation is built on it (checked 20261102).

## Sources

1. https://arxiv.org/abs/1705.10744 : Kadlec et al., Knowledge Base Completion: Baselines Strike Back, v1 20170530 (abstract only, read 20261102 20:52 UTC)
2. https://arxiv.org/pdf/1707.01476v6 : Dettmers et al., ConvE v6 (4 July 2018): metrics, Table 4, inverse model, version list (v1 5 July 2017; inverse-model numbers corrected 28 March 2018) (full text, read 20261102 21:24 UTC)
3. https://papers.nips.cc/paper_files/paper/2013/file/1cecc7a77928ca8133fa24680a88d2f9-Paper.pdf : Bordes et al., TransE, NIPS 2013: raw and filtered settings, mean rank, hits@10 (full text, read 20261102 20:51 UTC)
4. https://arxiv.org/pdf/1911.03903 : Sun et al., A Re-evaluation of Knowledge Graph Completion Methods, v3 (8 July 2020): tie rules, Tables 2 and 3 (full text, read 20261102 20:48 UTC)
5. https://arxiv.org/pdf/2002.00819 : Rossi et al., Knowledge Graph Embedding for Link Prediction: A Comparative Analysis, v4 (21 January 2021): Tables 2 and 3, tie policy, tuning budget, YAGO3-10 statistics (full text, read 20261102 20:50 UTC)
6. https://arxiv.org/pdf/2003.08001 : Akrami et al., Realistic Re-evaluation of Knowledge Graph Completion Methods, v1 20200318: YAGO3-10 duplicate relations (full text, read 20261102 20:52 UTC)
7. https://yago-knowledge.org/downloads/yago-3 : YAGO 3 licence, CC BY 3.0 (read 20261102 20:52 UTC)
8. https://raw.githubusercontent.com/uma-pi1/kge/master/README.md : LibKGE results tables and the unseen-entity note; GitHub API: MIT, last push 20260401 (read 20261102 20:51 UTC)
9. https://arxiv.org/pdf/2009.07810v1 : Safavi and Koutra, CoDEx, v1 20200916: Table 7, frequency baseline and RESCAL (read 20261102 21:24 UTC)
10. https://export.arxiv.org/api/query?id_list=1902.10197,1911.03903,2002.00819,2203.02167,2009.07810,2508.15357 : authors and first-version dates (RotatE authors Sun, Deng, Nie, Tang) (read 20261102 20:51 UTC)
11. https://arxiv.org/pdf/2203.02167 : Wang et al., SimKGC, 20220304: Table 3, variants IB, IB+PB, IB+SN, IB+PB+SN (full text, read 20261102 21:24 UTC)
12. https://arxiv.org/abs/2508.15357 : Gul et al., KG-EDAS, 20250821 (abstract only, read 20261102 20:51 UTC)
13. https://ogb.stanford.edu/docs/linkprop/ : ogbl-wikikg2 protocol, 1,000 sampled negatives (read 20261102 20:55 UTC)
