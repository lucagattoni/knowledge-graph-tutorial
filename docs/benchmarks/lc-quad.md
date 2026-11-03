---
type: benchmark
datasets: [lc-quad]
updated: 20261102 21:29 UTC
---

# LC-QuAD

This page answers how systems are scored on LC-QuAD and what the published numbers show. The questions, sizes, splits, licence and construction are on [the LC-QuAD dataset page](../datasets/lc-quad.md). No authors' leaderboard is maintained [8], so the numbers come from papers, and their protocols differ.

## What it tests

It tests whether a system turns a natural-language question into a [SPARQL](../index/sparql.md) query, or into the answer that query returns, over [DBpedia](../datasets/dbpedia.md) (version 1.0) or [Wikidata](../datasets/wikidata.md) (version 2.0). It is a [question answering](../index/question-answering.md) and [text-to-query](../index/text-to-query.md) test on "complex" questions: more than one triple, or a count, boolean, ranking or string operation [1][2].

## Tasks, metrics and protocol

Five protocols are in use:

- **Query building with gold input.** The system gets the correct entities and relations and arranges them into a query; it matches if the query's result equals the gold result on a local copy of the graph [3].
- **End-to-end.** The paper calls its own setting end-to-end: the system finds entities and relations itself, and is scored with macro Precision@1 from the query results [4].
- **Query generation, entity input unstated.** A system generates a query and is scored with precision, recall and F1 on results [7]. Whether topic entities are given: **unstated** in [7].
- **LLM answers.** Language models answer from their own knowledge, which the paper calls "unsupervised"; F1 on answers [5].
- **Executed agent.** An LLM agent builds and runs the query in several turns; macro F1 and exact match on answer sets [6].

Each paper chooses its own split and test filter (see the versions table on the dataset page), so scores from different papers are not like for like even on one version. Each block below names the test set where the paper states one.

## Datasets

One dataset in two versions; see [the dataset page](../datasets/lc-quad.md).

## Results

Scores in different blocks are not comparable: input, test set, graph version and metric differ. Copied rows were measured in their authors' own setups, so they are weaker evidence than rows the paper ran itself.

**A. Version 1.0, gold entities and relations given, F1 (all rows of Table 1 of [3]).** Test set: a 3,253-question subset with five-fold cross-validation (Section 4 of [3]). Copied rows are "as reported by Ding et al." (the authors of SubQG) [3]; their Date is the year of the cited work.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| T5-Base | 0.91 | F1 | Banerjee et al. | paper's own comparison | 2022 | [3] |
| T5-Small | 0.90 | F1 | same | paper's own comparison | 2022 | [3] |
| PGN-BERT-BERT | 0.88 | F1 | same | yes (proposed in [3]) | 2022 | [3] |
| SubQG | 0.85 | F1 | copied from Ding et al. | yes (its authors) | 2019 | [3] |
| BART | 0.84 | F1 | Banerjee et al. | paper's own comparison | 2022 | [3] |
| CompQA | 0.77 | F1 | copied from Ding et al. | unstated | 2018 | [3] |
| SQG | 0.75 | F1 | copied from Ding et al. | unstated | 2018 | [3] |
| PGN-BERT | 0.67 | F1 | Banerjee et al. | yes (proposed in [3]) | 2022 | [3] |
| NLIWOD | 0.48 | F1 | copied from Ding et al. | unstated | 2018 (board) | [3][9] |
| Sina | 0.24 | F1 | copied from Ding et al. | unstated | 2015 | [3] |

**B. Version 1.0, as reported in Table IV of [7].** The paper's own split, DBpedia 2016-10. *Reading:* the table calls these "prior state-of-the-art methods"; whether HGNet and STaG-QA were re-run: **unstated**.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| OntoSCPrompt, with constraints | 79.1 | F1 | its authors | yes | 2025 | [7] |
| HGNet | 75.1 | F1 | listed in [7] | no | 2025 | [7] |
| OntoSCPrompt, without constraints | 70.2 | F1 | its authors | yes | 2025 | [7] |
| STaG-QA | 51.4 | F1 | listed in [7] | no | 2025 | [7] |

**C. Version 2.0, gold entities and relations given, F1 (all rows of Table 1 of [3]).** Filtered test set, as in [3]. The three copied rows are "as reported by Zou et al." [3]; their Date is the year of the cited work.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| T5-Small | 0.92 | F1 | Banerjee et al. | paper's own comparison | 2022 | [3] |
| T5-Base | 0.91 | F1 | same | paper's own comparison | 2022 | [3] |
| PGN-BERT-BERT | 0.86 | F1 | same | yes (proposed in [3]) | 2022 | [3] |
| PGN-BERT | 0.77 | F1 | same | yes (proposed in [3]) | 2022 | [3] |
| BART | 0.64 | F1 | same | paper's own comparison | 2022 | [3] |
| CLC | 0.59 | F1 | copied from Zou et al. | unstated | 2021 | [3] |
| Multi-hop QGG | 0.53 | F1 | copied from Zou et al. | unstated | 2020 | [3] |
| AQG-net | 0.45 | F1 | copied from Zou et al. | unstated | 2020 | [3] |

**D. Version 2.0, LLMs answering from their own knowledge, F1 (%, the LC-quad2 column of Table 3 of [5]).** Collected size 26,975 questions (Table 2); how many were scored per model: **unstated**. The SOTA row is copied from the KBQA leaderboard and cited to UNIQORN (an arXiv paper of 2021, its Date).

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| GPT-4 | 54.95 | F1 | Tan et al. | no | 2023 | [5] |
| ChatGPT | 42.76 | F1 | same | no | 2023 | [5] |
| GPT-3.5 v3 | 39.04 | F1 | same | no | 2023 | [5] |
| GPT-3.5 v2 | 33.77 | F1 | same | no | 2023 | [5] |
| SOTA, fine-tuned (UNIQORN) | 33.10 | F1 | copied | unstated | 2021 | [5] |
| GPT-3 | 33.04 | F1 | Tan et al. | no | 2023 | [5] |
| FLAN-T5 | 30.14 | F1 | same | no | 2023 | [5] |

**E. Version 2.0, end-to-end (the paper's own term), Precision@1 (Table 3 of [4]).** 4,921 test questions; the UNIQORN row is copied from its paper, as are the lower rows of the table (QAnswer 0.308, Platypus 0.036, PullNet 0.011, UNIK-QA 0.005).

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| GETT-QA | 0.403 | P@1 | its authors | yes | 2023 | [4] |
| UNIQORN | 0.331 | P@1 | copied | no | 2023 | [4] |

**F. Version 2.0, executed agents, 826 test questions (LC-QuAD 2.0 column of Table 1 of [6]).** Every baseline was run on gpt-oss-120B by the paper's authors, except the second SAGA row.

| System | Score (F1 / EM) | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| SAGA, gpt-oss-120B | 28.25 / 25.39 | F1 / EM | its authors | yes | 20260716 | [6] |
| SAGA, LLaMA 3.1-70B | 26.99 / 24.48 | F1 / EM | its authors | yes | 20260716 | [6] |
| SPINACH | 25.83 / 23.58 | F1 / EM | SAGA authors, re-run | no | 20260716 | [6] |
| GRASP | 20.48 / 17.95 | F1 / EM | same | no | 20260716 | [6] |
| Interactive-KBQA | 19.93 / 15.72 | F1 / EM | same | no | 20260716 | [6] |
| mKGQAgent | 15.15 / 13.42 | F1 / EM | same | no | 20260716 | [6] |
| Data Shapes Prompting | 9.83 / 8.22 | F1 / EM | same | no | 20260716 | [6] |
| OBQC Repair | 9.34 / 7.50 | F1 / EM | same | no | 20260716 | [6] |
| Entity Linking | 5.74 / 4.84 | F1 / EM | same | no | 20260716 | [6] |
| Zero-shot SPARQL | 3.86 / 3.39 | F1 / EM | same | no | 20260716 | [6] |

*Reading:* apart from block D, every row comes from a paper that proposes a system or builds its own comparison, so no independent ranking exists. Gold entities lift 2.0 scores above 0.9 (block C); LLM answers give 30 to 55 (D); agents that must ground their own query on Wikidata score 4 to 28 (F). The gaps come mostly from the protocol, not from the models.

## Known problems

- **No official results.** The 1.0 README says its authors are "in the process of automating the benchmarking process" and run it by hand on request [8]. The 2.0 README has no results text [12]. The community board has no row dated after 2023 [9].
- **Gold input.** Blocks A and C test only query assembly; the community board mixes such rows with others in one list [9].
- **Structure overlap.** The 1.0 test structures all appear in training (dataset page), so a high 1.0 score need not show that a system handles new query shapes. For 2.0, a 2025 paper says second-hand: "a marked drop in accuracy when models are evaluated on reformulated (template-free) questions" [10].
- **Boolean questions.** In block F the gain over SPINACH comes from boolean questions: boolean F1 went from 25.6 to 55.6, factoid F1 fell by 1.0. Their number in the test set: **unstated** [6].
- **Newer LLM results.** Other 2024 to 2026 papers use the data, but their scores were not read: **unstated** beyond [6] and [7].

## Used by

The [graph query generation](../trends/graph-query-generation.md) trend and its [papers](../papers/graph-query-generation.md); the studies cited above [3][4][5][6][7]; the TEXT2SPARQL challenge, which used 1.0 only as an example pool [11].

## Sources

1. http://jens-lehmann.org/files/2017/iswc_lcquad.pdf : LC-QuAD 1.0 paper, question kinds (read 20261102 20:42 UTC)
2. http://jens-lehmann.org/files/2019/iswc_lcquad2.pdf : LC-QuAD 2.0 paper, question types (read 20261102 20:42 UTC)
3. https://arxiv.org/pdf/2204.12793 : Banerjee et al., SIGIR 2022, v3 of 20230914: Table 1 (all rows, both versions), Sections 4 and 5, reference list for the years (re-read 20261102 21:23 UTC)
4. https://arxiv.org/pdf/2303.13284 : GETT-QA, v3 of 20230328: Table 3 and Section 5 (re-read 20261102 21:26 UTC)
5. https://arxiv.org/pdf/2303.07992 : Tan et al., v3 of 20230920: Tables 2 and 3, the sentence on LLMs using "their own knowledge" (re-read 20261102 21:24 UTC)
6. https://arxiv.org/pdf/2607.14494 : SAGA, v1 of 20260716: Datasets, Table 1, Table 3, "Results on Wikidata" (re-read 20261102 21:26 UTC)
7. https://arxiv.org/pdf/2502.03992 : Jiang et al. (2025), OntoSCPrompt: Table II, Table IV, Section III-C and III-D (re-read 20261102 21:24 UTC)
8. https://github.com/AskNowQA/LC-QuAD : `data` branch README, section "Benchmarking/Leaderboard" and changelog (re-read 20261102 21:25 UTC)
9. https://raw.githubusercontent.com/KGQA/leaderboard/gh-pages/dbpedia/lcquad.md : community board; SubQG 2019, CompQA 2018, SQG 2018, NLIWOD 2018, Sina 2015; commit history, last change 20230430 (re-read 20261102 21:23 UTC)
10. 11. https://arxiv.org/pdf/2503.22144 : FRASE, v1 of 20250328, Section 2.1 (Related Works), second-hand statement citing Diallo et al. 2024 and Reyd and Zouaq 2023, not read (re-read 20261102 21:24 UTC)
11. https://arxiv.org/pdf/2512.14277 : SPARQL-LLM, Section 4.1.1 (re-read 20261102 21:25 UTC)
12. https://github.com/AskNowQA/LC-QuAD2.0 : README, one sentence (read 20261102 21:25 UTC)
