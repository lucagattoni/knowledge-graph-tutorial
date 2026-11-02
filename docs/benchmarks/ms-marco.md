---
type: benchmark
datasets: [ms-marco]
updated: 20261102 21:27 UTC
---

# MS MARCO

This page answers what the MS MARCO benchmark measures, how it is scored, and what the numbers show. The queries, passages, sizes and licence are on [the MS MARCO dataset page](../datasets/ms-marco.md). Scores come from three kinds of source: a leaderboard hosted by Microsoft, with runs submitted by the system authors and scored on held-out labels; the TREC Deep Learning overviews, written by track organisers (three of whom also wrote the MS MARCO paper) with NIST judges; and a BEIR re-run by its authors [3][6][7][8][12]. A crowd study by other authors questions the leaderboard itself.

## What it tests

It tests how well a system puts a passage that answers a real search query near the top, when it can train on hundreds of thousands of sparse human labels [4][7]. It started as a reading-comprehension test, where a system writes an answer from passages [1]. Passage ranking was added 20181026, document ranking 20200811, and by 2020 the organisers refocused on those two tasks [2]. The task is plain text [information retrieval](../index/information-retrieval.md); no graph is involved.

## Tasks, metrics and protocol

| Task | What the system does | Metric | Status |
|---|---|---|---|
| Passage re-ranking | Re-order the [BM25](../index/bm25.md) top 1,000 supplied for each query [4][11] | [MRR@10](../index/mean-reciprocal-rank.md) [11] | Board labelled retired [2] |
| Passage full ranking | Search the whole collection, return up to 1,000 [4] | MRR@10 | same [2] |
| Document ranking | Re-rank 100 supplied candidates, or search the whole collection and return up to 100 [4] | **unstated** | same [2] |
| QnA, NLGEN, OpenKP | Answer from passages (Rouge-L, Bleu-1); return key phrases (F1) | see [2] | closed 20201023 [2] |

- **Splits and scoring.** The public dev split is for development. The organisers keep the eval labels and score submitted runs; submissions are encrypted before upload [3][4][11].
- **Rules.** Outside data is allowed, but not other msmarco.org datasets. A team that uses the Bing passages shipped with each query must say so, and the run is marked special [4][11].
- **TREC Deep Learning Track, 2019 and 2020.** Same corpus and training data, new test queries judged by NIST on four relevance levels. Main metric [nDCG@10](../index/ndcg.md). In 2019, 43 passage queries were judged; in 2020, 54 [6][7].
- **Board status.** The page marks both ranking tasks "RETIRED" with end date 01/01/2023, though the October 2020 notice had said submissions "will continue as usual" [2]. The newest board row is dated 20221113; the submissions repository is archived (last push 20230421) [3].

## Datasets

One dataset: [MS MARCO](../datasets/ms-marco.md).

## Results

Dates are the board entry date, the TREC cycle or the paper version, not the read date. Scores of different blocks are not comparable. "First-party" means the system's own authors ran it.

**Block A. Passage ranking board, MRR@10, eval (held-out labels) then dev [3].** Read from the board's data file. Every system row was submitted by the authors of the system; the Okapi row is the organisers' own baseline.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| BM25 (Okapi, implemented by the MS MARCO team) | 0.165 / 0.167 | MRR@10 | MS MARCO team | yes (Microsoft) | 20181101 | [3] |
| BERT Large re-ranker | 0.359 / 0.365 | MRR@10 | Nogueira and Cho | yes (system authors) | 20190107 | [3][5] |
| RocketQA + ERNIE | 0.426 / 0.439 | MRR@10 | Baidu NLP | yes (system authors) | 20200918 | [3] |
| AliceMind SLM + HLAR (top eval row) | 0.450 / 0.463 | MRR@10 | Alibaba DAMO NLP | yes (system authors) | 20220317 | [3] |

**Block B. TREC Deep Learning, passage task, nDCG@10 with NIST labels.** Runs are by track participants; the labels are independent of them, and the tables are in the organisers' overviews [6][7].

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Best run 2019 (idst_bert_p1, BERT) | 0.7645 | nDCG@10 | IDST | yes (participant) | TREC 2019 | [6] |
| Best traditional run 2019 (srchvrs_ps_run3) | 0.5558 | nDCG@10 | srchvrs | yes (participant) | TREC 2019 | [6] |
| Best run 2020 (pash_r3) | 0.8031 | nDCG@10 | PASH | yes (participant) | TREC 2020 | [7] |
| Best traditional run 2020 (bl_bcai_mdl1_vt) | 0.5667 | nDCG@10 | bl_bcai | yes (participant) | TREC 2020 | [7] |

**Block C. BEIR in-domain row, nDCG@10, on the dataset's public dev set [8].** Run by the BEIR authors (UKP Lab), not by the systems' authors. A double dagger marks in-domain results.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| BM25 | 0.228 | nDCG@10 | BEIR authors | no | 20211021 (v4) | [8] |
| BM25 + cross-encoder‡ | 0.413 | nDCG@10 | BEIR authors | no | 20211021 | [8] |

*Reading:* on this evidence the large gain comes from pretrained language models, which independent NIST labels confirm: the best neural run beats the best traditional run by about 38% in 2019 (computed here from Table 4 of [6]) and by about 42% in 2020 (stated in the 2020 overview [7]). Results after 20221113 are **unstated**.

## Known problems

- **"Better than perfect".** Crowd workers preferred a neural ranker's top result to the judged relevant passage often enough that a perfect MRR ranker would lose. The authors doubt the sparse-label board can still show real gains (authors outside the MS MARCO paper, first version 20210831) [9]. The organisers agree that the goal is robust usefulness, not the top score [10].
- **One run, two labels.** The same 2019 run scores reciprocal rank 0.4635 on MS MARCO labels and 0.9283 on NIST labels [6].
- **Unverifiable.** Eval runs are encrypted and labels are held out, so readers cannot re-score them [3][11]. Of 168 rows, 36 are anonymous and 89 are re-rankers (counted from the data file read 20261102 20:43 UTC) [3].

## Used by

[BEIR](beir.md) reports the dev set in-domain [8]. The TREC Deep Learning Track is built on it [6][7]. See [language models meet retrieval](../history/language-models-meet-retrieval.md). No trend page cites it (searched 20261102 20:49 UTC).

## Sources

1. https://arxiv.org/pdf/1611.09268 : MS MARCO paper v3: original tasks (read 20261102 20:42 UTC)
2. https://microsoft.github.io/msmarco/ : tasks, retirement dates and notice, QnA board rows (read 20261102 20:41 UTC)
3. https://github.com/microsoft/MSMARCO-Passage-Ranking-Submissions : `leaderboard/leaderboard.csv` (168 rows, read 20261102 20:43 UTC) and README (re-read 20261102 21:22 UTC: official board, encrypted submissions, blind eval set), via `gh api`; the rendered board page showed only a title
4. https://microsoft.github.io/msmarco/Datasets : tasks, candidate depth, outside-data rule (read 20261102 21:23 UTC)
5. https://arxiv.org/pdf/1901.04085 : Nogueira and Cho, Passage Re-ranking with BERT, Table 1 (read 20261102 20:45 UTC)
6. https://arxiv.org/pdf/2003.07820 : TREC 2019 Deep Learning overview, Table 4 and text (read 20261102 21:21 UTC)
7. https://arxiv.org/pdf/2102.07662 : TREC 2020 Deep Learning overview, Table 5 and text (read 20261102 21:21 UTC)
8. https://arxiv.org/pdf/2104.08663 : BEIR v4, Table 2 and appendix C (read 20261102 21:21 UTC)
9. https://arxiv.org/abs/2109.00062 : Arabzadeh et al., Shallow pooling for sparse labels, abstract (read 20261102 20:46 UTC)
10. https://arxiv.org/abs/2105.04021 : Craswell et al., Benchmarking Ranking Models in the Large-Data Regime, abstract (read 20261102 20:46 UTC)
11. https://github.com/microsoft/MSMARCO-Passage-Ranking : README (body in an HTML comment): top-1000 BM25 candidates, MRR@10, held-out eval (read 20261102 21:23 UTC)
12. https://export.arxiv.org/api/query?id_list=1611.09268,2003.07820,2102.07662 : author lists of the MS MARCO paper and the two TREC overviews; Craswell, Mitra and Campos appear in all three (read 20261102 21:24 UTC)
