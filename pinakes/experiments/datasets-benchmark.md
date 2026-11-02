# The datasets benchmark: Pinakes retrieval against public datasets

Part of the [Pinakes development notes](../README.md). This page describes a separate public repository,
[`pinakes-datasets-benchmark`][1], that measures how well Pinakes' free search finds the right documents when
the correct answers are known. It is the home of the "benchmark" the [decision record](../../DECISIONS.md)
(D-15) says is run outside this repository.

**Every figure below is the benchmark repository's own, copied from its README [2] at commit `9941f58` (`main`,
20261031 23:33 UTC), read 20261102 08:54 UTC. It is first-party. I did not re-run it, re-derive a number or read its
run files.** The README can change, so re-read it before relying on a figure. Where it is silent the text says
`unstated`. The owning session confirmed on 20261102 that it has no pending change to the headline figures.

## What it is

| Item | Value | Source |
|---|---|---|
| Repository | public; Apache-2.0; created 20261030 17:32 UTC; last push 20261031 23:33 UTC | [1] |
| What it does | builds a Pinakes knowledge base from a public dataset that ships ground-truth evidence, asks every question the dataset contains, and scores what comes back | [2] |
| First dataset | MultiHop-RAG: 609 English news articles; 2,556 questions with evidence in two to four articles, of which 301 are "null" questions the corpus cannot answer | [2] |
| Pinakes under test | 0.32.8 from PyPI with its defaults (a switch exists for `main`) | [2] |
| Dataset licence | ODC-By 1.0; the dataset is fetched, not redistributed; the news text comes from publishers whose own terms were not checked | [2][3] |
| Results kept | four run directories (two for the `sentence-transformers` provider, one for `main`, one for `fastembed`) and three paired comparisons | [4] |

## What its first full run reports

Run `20261030_1826-baseline-pypi-0.32.8`: 2,255 answerable and 301 null questions, 8,497 searches in all [2].

| Share of answerable questions where… | first 5 passages | first 8 (the default of `pnk search`) | first 20 (the reranker's pool) |
|---|---|---|---|
| at least one gold article is found | 91.5% | 96.8% | not computed |
| **every** gold article is found | 33.8% | **43.4%** (95% interval 41.3 to 45.4) | 61.0% (58.9 to 63.0) |

- **By evidence needed**, every gold article in the first 8: two articles 67.1%, three 22.1%, four 7.4%. By question
  type: comparison 60.3%, temporal 43.9%, inference 25.2% [2].
- **Where the rest go:** for 39.0% of answerable questions at least one gold article is missing from the whole pool
  of 20; for a further 17.6% all are in the pool but not all in the first 8 [2].
- **Telling null from answerable by the top rerank score:** AUROC 0.944 (0.929 to 0.957); re-checked on the 18 null
  questions without wording tells, 0.945 (0.882 to 0.982), a small sample [2].
- **Confidence labels:** on the held-out half a null question is labelled high-confidence 16.2% of the time
  (11.2 to 22.9, n=154), against 10.9% on the half the thresholds were fitted on [2].
- **Variants:** embedding each chunk's title does not help (first 8: 42.3% against 43.4%; pool of 20: 55.7%
  against 61.0%). The `fastembed` provider ranks alike (43.3% and 60.9% on the same two measures) but its scores
  are on another scale, so fitted confidence thresholds do not carry over between providers [2].
- **Filters:** across 5,941 filtered searches, none returned an article the filter excludes [2]. The filters are
  oracles built from the gold articles' own metadata, so they test the machinery, not a user's choice [2].

## What its README says it cannot show

- **Scope:** MultiHop-RAG only, Pinakes 0.32.8 with its defaults, one machine, nothing tuned [2].
- **The questions:** per the dataset's paper, GPT-4 generated the queries and answers, and the benchmark did not
  check them ("can be wrong or leading") [3]. The 301 null questions are written differently from the 2,255
  answerable ones: 144 (47.8%) mention a "letter" against 0; 184 (61.1%) contain "Considering the information"
  against 2; 211 (70.1%) name no news outlet against 14 [3]. That is why the abstention result was re-checked on the
  18 null questions without these tells [2].
- **The headline measure** is "every gold article in the first 8 passages" (43.4%). "At least one" (96.8%) is
  Pinakes' own harness definition of a hit and is the loose measure; do not quote it alone [2].
- **The filter results use oracle filters** built from the gold articles' own metadata [2].
- **Speed is not compared:** the `sentence-transformers` and `fastembed` runs differ in CPU against GPU, and a
  competing job ran beside one of them for part of the time, so the README says not to read a ratio from the
  latencies, and this page quotes none [2].
- **Not run yet** (its words): Pinakes' graph channel, the paid `--deep` loop, and a **real** switch of a
  knowledge base from one provider to the other. The provider comparison above is two separate runs, not a
  switch, and is not described here as tested [2].

## How it relates to the proposals here

- **P3** in [what to measure next](next.md#p3-public-dataset-baselines-for-the-free-retrieval-path) asked for the
  free path against BM25 alone on a public dataset. The free path now has numbers on MultiHop-RAG in this
  repository. A **BM25-alone arm is unstated** in the README (a search for "BM25 alone" or "BM25-only" found
  none), and the repository's `configs/` holds only `baseline`, `baseline-fastembed` and `metadata-prefix`, plus
  the model pins [5]; all three are the full free pipeline. So the comparison P3 named is not shown there.
- **P4** (the deep-loop pilot) used a different corpus and three questions, so nothing in the two can be compared;
  the benchmark lists the deep loop as not run [2].
- The page [what Pinakes has measured](README.md) is built from Pinakes' own documents and does not include these
  figures.

## Sources

1. https://github.com/lucagattoni/pinakes-datasets-benchmark : repository metadata through the GitHub API; `main` is `9941f58`, committed 20261031 23:33 UTC (read 20261102 08:56 UTC)
2. https://github.com/lucagattoni/pinakes-datasets-benchmark/blob/main/README.md : 215 lines, read in full (read 20261102 08:54 UTC)
3. https://github.com/lucagattoni/pinakes-datasets-benchmark/blob/main/datasets/multihop-rag/README.md : the licence lines, the line saying who generated the questions, and the table of how null questions differ (lines 98 to 108; read 20261102 08:56 and 09:00 UTC)
4. https://github.com/lucagattoni/pinakes-datasets-benchmark/tree/main/runs : directory listing (read 20261102 08:55 UTC)
5. https://github.com/lucagattoni/pinakes-datasets-benchmark/tree/main/configs : directory listing (read 20261102 09:00 UTC)

[1]: https://github.com/lucagattoni/pinakes-datasets-benchmark
[2]: https://github.com/lucagattoni/pinakes-datasets-benchmark/blob/main/README.md
[3]: https://github.com/lucagattoni/pinakes-datasets-benchmark/blob/main/datasets/multihop-rag/README.md
[4]: https://github.com/lucagattoni/pinakes-datasets-benchmark/tree/main/runs
[5]: https://github.com/lucagattoni/pinakes-datasets-benchmark/tree/main/configs
