---
type: benchmark
datasets: [wikidata]
updated: 20261102 21:29 UTC
---

# OGB link prediction

This page answers how the Open Graph Benchmark (OGB) scores [knowledge graph completion](../index/knowledge-graph-completion.md) on a Wikidata extract, and what the scores can and cannot show. Its data (`ogbl-wikikg2`) is used only inside this protocol, so it is described below and has no dataset page. The OGB paper has 4,139 citations (Semantic Scholar, read 20261102 20:00 UTC, not re-queried) [9].

## What it tests

OGB groups seven link-property datasets today; two are knowledge graphs, `ogbl-wikikg2` and `ogbl-biokg` [1]. Both test whether a [knowledge graph embedding](../index/knowledge-graph-embedding.md) model can recover held-out [triples](../index/triple.md). Only `ogbl-wikikg2` splits by time: its test triples were added after the training graph was fixed. `ogbl-biokg` has a random split [1]. The OGB authors argue that random splits are unrealistic and give overly optimistic results [5]. [Knowledge graph link prediction](kg-link-prediction.md) ranks against all entities instead.

## Tasks, metrics and protocol

- **Task.** Predict new (head, relation, tail) triples from the training triples [1].
- **Negatives.** Each test triple is corrupted at the head and at the tail. Each side gets 500 random entities, 1,000 in all, chosen so the corrupted triple is not in the graph [1][5].
- **Metric.** [Mean reciprocal rank](../index/mean-reciprocal-rank.md) (MRR) of the true entity among those candidates. Validation and test are called filtered; training MRR is unfiltered [5]. This is not a ranking against every entity.
- **Rules.** Validation labels may tune hyperparameters, not train the model; test labels are for final evaluation only [4].
- **Submission.** Mean and unbiased standard deviation over 10 seeds [3][5], plus code, parameter count, hardware, an external-data flag and an official or unofficial mark. OGB says it removes invalid submissions; whether it re-runs them is **unstated** [3].
- **Version.** `ogb` 1.2.4 or later; the earlier `ogbl-wikikg` is deprecated for a negatives bug [1].

## Datasets

**ogbl-wikikg2** has 2,500,604 entities, 535 relation types and 17,137,181 edges, split 94/3/3 by time [1][5]. The authors took the statements of [Wikidata](../datasets/wikidata.md), dropped rare entities, and kept only entities and relations in the May 2015 graph. May triples train, August additions validate, November additions test [1]. Licence CC-0, stated on the OGB page [1].

**ogbl-biokg** has 93,773 nodes of five types, 51 relation types and 5,088,434 edges from biomedical repositories; random split, candidates of the same type only; CC-0 [1].

## Results

The board (read 20261102 21:28 UTC) has 28 `ogbl-wikikg2` rows: 20 by the method's own authors and 8 by the OGB team, re-implementing existing methods [2][3]. Nothing was re-run here. **A. Leaderboard, `ogbl-wikikg2`** (selected rows; "Submitted" is the board's date):

| System | Score | Metric | Who ran it | First-party? | Submitted | Source |
|---|---|---|---|---|---|---|
| RelEns (2.18 billion parameters) | .7392 ± .0011 | test MRR | Quanming Yao, Tsinghua | yes | 20231015 | [2] |
| StarGraph + TripleRE + Text (uses external data) | .7305 ± .0010 | test MRR | Liang Yao, Tencent | yes | 20230104 | [2] |
| CompoundE3D (newest row) | .7006 ± .0011 | test MRR | Xiou Ge, USC | yes | 20231229 | [2] |
| A*Net (6.8 million) | .6711 ± .0045 | test MRR | Zhaocheng Zhu, Mila | yes | 20230521 | [2] |
| RotatE, 250 dim (1.25 billion) | .4332 ± .0025 | test MRR | OGB team | no: benchmark authors, unofficial implementation | 20210123 | [2][5] |
| TransE, 500 dim | .4256 ± .0030 | test MRR | OGB team | same | 20210123 | [2][5] |

**B. Independent re-runs** (Douglas et al.; five models trained with the OGB code, hidden size 500, gamma partly tuned) [7]. "Uniform" is the OGB protocol; "resampled" draws half the negatives from a model of P(tail | relation):

| System | Score (uniform / resampled) | Metric | Who ran it | First-party? | Posted | Source |
|---|---|---|---|---|---|---|
| PairRE | .56 / .28 | MRR | Douglas et al. | no | 20211019 | [7] Table 4 |
| ComplEx | .48 / .17 | MRR | Douglas et al. | no | 20211019 | [7] |
| TransE | .44 / .13 | MRR | Douglas et al. | no | 20211019 | [7] |

**C. Null model.** Scoring a tail by its training frequency under the relation, ignoring the head, gives a tail-only MRR of .23 (Douglas et al.) [7].

**D. Leaderboard, `ogbl-biokg`** (12 rows): RelEns .9618 (Yao, 20231015); OGB-team ComplEx .8095 (20200610) [2].

No independent re-run of a leaderboard row appears in the sources read here ([2], [7], [8]); no wider search was made, so this does not show that none exists. The nearest check is Cornell et al., who take pretrained ComplEx embeddings from Chen et al. and evaluate them on the `ogbl-wikikg2` test set under full ranking; their number is only in a figure, so it is **unstated** here [8]. The board has a `ComplEx-RP (50dim)` row by Yihong Chen (.6392 ± .0045, 20211123) [2]; whether it is the same checkpoint is **unstated**.

*Reading:* the top of the board sits about .31 MRR above the organisers' best baseline. Size explains part (2.18 against 1.25 billion parameters), but A*Net reaches .6711 with 6.8 million [2]. The metric itself is the weak point: for five models, Douglas et al. found the order under uniform and resampled negatives agreed only moderately (Spearman about .6 here, about .9 on smaller graphs) [7].

## Known problems

- **Easy negatives.** Only about 10% of test triples have any sampled negative with the correct relation type, so a type match alone can put the true entity first. The OGB paper itself notes 500 negatives against about 15,000 for FB15k [5][7].
- *Reading:* scores are not comparable with [FB15k-237](../datasets/fb15k-237.md) or [WN18RR](../datasets/wn18rr.md), because those are ranked against all entities (see [Knowledge graph link prediction](kg-link-prediction.md)) and this is not. The size of the gap is not measured here.
- **Independent critique.** Cornell et al. (arXiv 20240125) report that uniform sampling overestimates full-ranking metrics, "up to 40 percentage points" in their experiments [8].
- **Self-reported, mixed budgets.** Rows range from 6.8 million to 2.18 billion parameters on different GPUs [2].
- **Old snapshot, quiet board.** The graph is Wikidata of 2015 [1]; the newest `ogbl-wikikg2` row is 20231229 [2].

## Used by

Leaderboard methods such as NodePiece and A*Net [2]; the two critiques above [7][8]. No trend page of this documentation uses it (checked 20261102 21:05). The `ogb` repository: MIT licence, 2,100 stars (20261102 21:01), last push 20250506, latest release 1.3.5 of 20221102 [6].

## Sources

1. https://ogb.stanford.edu/docs/linkprop/ : dataset sizes, protocol, splits (wikikg2 time, biokg random), licences, deprecation note (read 20261102 21:28 UTC)
2. https://ogb.stanford.edu/docs/leader_linkprop/ : `ogbl-wikikg2` board (28 rows parsed, official marked in bold) and `ogbl-biokg` board (12 rows); RelEns, RotatE, TransE and ComplEx-RP rows checked again (read 20261102 21:28 UTC)
3. https://ogb.stanford.edu/docs/leader_overview/ : submission form, 10 seeds, unbiased standard deviation, officiality, removal of invalid submissions (read 20261102 21:28 UTC)
4. https://ogb.stanford.edu/docs/leader_rules/ : rules for train, validation and test labels (read 20261102 21:01 UTC)
5. https://arxiv.org/pdf/2005.00687 : Hu et al., Open Graph Benchmark (8 authors), NeurIPS 2020, v7 of 20210225, first version 20200502; sections 1, 5.5, 5.6, Table 13, footnote 22; 94/3/3 ratio and "mean and unbiased standard deviation" re-read (read 20261102 21:28 UTC)
6. https://raw.githubusercontent.com/snap-stanford/ogb/master/LICENSE : MIT licence (read 20261102 21:00 UTC); GitHub API for stars, last push and release (read 20261102 21:01 UTC)
7. https://arxiv.org/pdf/2110.09978 : Douglas et al. (7 authors), What is Learned in Knowledge Graph Embeddings?, v1 20211019, Complex Networks 2021; sections 1.4 to 1.5, Table 4 (read 20261102 21:03 UTC)
8. https://arxiv.org/pdf/2402.00053 : Cornell et al. (4 authors), Are We Wasting Time?, v1 20240125; abstract, sections 1 and 5.3, reference 17 (Chen, Minervini, Riedel, Stenetorp) (read 20261102 21:28 UTC)
9. https://api.semanticscholar.org/graph/v1/paper/arXiv:2005.00687?fields=citationCount : 4,139 (read 20261102 20:00 UTC, taken from the research notes of this documentation, which are not kept in the repository; not re-queried because the service rate-limits)
