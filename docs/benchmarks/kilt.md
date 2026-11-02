---
type: benchmark
datasets: [wikipedia-dpr-kilt, natural-questions, hotpotqa, triviaqa]
updated: 20261102 21:05 UTC
---

# KILT

This page answers how systems are scored on KILT, which tasks and datasets it holds and what the results show. KILT bundles eleven existing datasets in five tasks over one Wikipedia snapshot, and it scores the answer and the evidence pages together. Its public leaderboard is frozen: the challenge ended on 20260131, and the newest of its 311 rows is dated 20250108 [3][4].

## What it tests

Whether one model and one index can serve many knowledge-intensive tasks, and whether the model can name the Wikipedia pages behind its output [1].

## Tasks, metrics and protocol

- **Tasks.** Fact checking, [entity linking](../index/entity-linking.md), [slot filling](../index/slot-filling.md), [open-domain question answering](../index/open-domain-question-answering.md) and dialogue [1].
- **Downstream metrics.** Accuracy for discrete outputs; [exact match](../index/exact-match.md) for Natural Questions, TriviaQA and HotpotQA; ROUGE-L for ELI5; F1 for Wizard of Wikipedia [1].
- **Retrieval metrics.** Scored per page. [R-precision](../index/r-precision.md) is r/R: R is the number of pages in a gold evidence set, r the relevant ones among the top R retrieved; it equals precision at 1 where one page suffices. Recall@k is also reported [1].
- **KILT scores.** A downstream point counts only if R-precision is 1: KILT-AC, KILT-EM, KILT-RL, KILT-F1 [1]. Systems that return no [provenance](../index/provenance.md) get none [1].
- **Protocol.** Training and development files are public; test inputs are public and test answers hidden. Predictions go to an evaluation server, one phase per dataset, with strict submission limits [2][3][4].

## Datasets

The knowledge source is [the KILT Wikipedia snapshot](../datasets/wikipedia-dpr-kilt.md). Sizes are the files in the repository [2].

| Dataset | Task | Train | Dev | Test |
|---|---|---|---|---|
| FEVER | fact checking | 104,966 | 10,444 | 10,100 |
| AIDA CoNLL-YAGO | entity linking | 18,395 | 4,784 | 4,463 |
| WNED-WIKI, WNED-CWEB | entity linking | none | 3,396; 5,599 | 3,376; 5,543 |
| T-REx | slot filling | 2,284,168 | 5,000 | 5,000 |
| Zero Shot RE | slot filling | 147,909 | 3,724 | 4,966 |
| [Natural Questions](../datasets/natural-questions.md) | open-domain QA | 87,372 | 2,837 | 1,444 |
| [HotpotQA](../datasets/hotpotqa.md) | open-domain QA | 88,869 | 5,600 | 5,569 |
| [TriviaQA](../datasets/triviaqa.md) | open-domain QA | 61,844 | 5,359 | 6,586 |
| ELI5 | open-domain QA | 272,634 | 1,507 | 600 |
| Wizard of Wikipedia | dialogue | 63,734 | 3,054 | 2,944 |

How the data was aligned [1]:

- Each dataset's Wikipedia pages are matched to the snapshot by title and redirect. The span with the highest BLEU against the original evidence becomes the new provenance. Dev and test items with BLEU below 0.5 for any span are dropped (on average 18%, except entity linking). Training sets stay whole.
- A crowd campaign collected evidence pages for ELI5 dev and test from scratch. What it changed for Natural Questions is on [that dataset's page](../datasets/natural-questions.md).
- FEVER keeps only supported and refuted claims.

## Results

Two kinds of rows. The first three are the benchmark authors' own baselines; their date is that of the paper version read (v4, 20210527; first version 20200904), not of a run [1]. The rest are the best row of each board on 20261102, read from the evaluation server: team submissions, scored by its evaluator on the hidden test [4]. None of the 311 rows is marked verified by the host [4]. No independent re-run was found. Team names are self-chosen. The CoRAG rows are matched to the CoRAG paper by team name, by identical numbers and by the board's team link to arxiv.org/pdf/2501.14342 [4][5]. The link of the E5 and LLaMA-3 team points to arxiv.org/abs/2401.00368, a text-embeddings paper; whether it reports these scores is **unstated** (only its title was read) [4][9].

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| RAG | FEVER 86.31; T-REx 59.2; zsRE 44.74; NQ 44.39; HotpotQA 26.97; TriviaQA 71.27 | accuracy (first three), EM (last three) | KILT authors | yes (RAG's authors overlap) | paper v4, 20210527 | [1] Table 3 |
| RAG | FEVER 53.45; T-REx 23.12; zsRE 36.83; NQ 32.69; HotpotQA 3.21; TriviaQA 38.13 | KILT-AC, KILT-EM | KILT authors | yes | paper v4, 20210527 | [1] Table 5 |
| BART large, no retrieval | FEVER 78.93; NQ 21.75; HotpotQA 15.37; TriviaQA 32.39 | accuracy, EM | KILT authors | yes | paper v4, 20210527 | [1] Table 3 |
| CoRAG | AIDA 92.05; WNED-CWEB 74.38; T-REx 76.70; zsRE 85.94 | KILT-AC | the team "CoRAG" | no for KILT; yes for CoRAG | 20250108 | [4] |
| CoRAG | NQ 53.46; HotpotQA 40.71; TriviaQA 73.25 | KILT-EM | same | same | 20250108 | [4] |
| CoRAG, downstream | NQ 63.09; HotpotQA 60.64; TriviaQA 88.29 | EM | same | same | 20250108 | [4]; the paper's Table 2 gives 63.1, 60.6, 88.3 [5] |
| FiD-Light | FEVER 84.50 | KILT-AC | the team "FiD-Light" | no | 20220706 | [4] |
| GENRE | WNED-WIKI 87.44 | KILT-AC | the team "GENRE" | no | 20200904 | [4] |
| Fine-tuned E5 retriever and LLaMA-3 generator | ELI5 5.39; Wizard of Wikipedia 14.88 | KILT-RL | team of that name | no | 20240705 | [4] |

*Reading:* one team holds seven of the eleven boards, and its paper reports the same downstream numbers [5]. The headline gap is between output and evidence. On HotpotQA the best system scores 60.64 EM but 40.71 KILT-EM; on ELI5 the best KILT-RL is 5.39. Evidence naming is the open part of the benchmark.

## Known problems

- **In-knowledge-base only.** Every instance is answerable from the snapshot, so there are no unanswerable items. Evidence is not exhaustive because Wikipedia repeats itself [1].
- **Not the original test sets.** Dev and test were filtered by BLEU, and the crowd-added evidence has weak agreement (kappa 0.3 for Natural Questions, 0.1 for ELI5). KILT numbers do not match the source datasets' own boards [1].
- **Slot filling can be gamed.** A title lookup solves zsRE [1]. Closed-book systems return no pages and so score zero on KILT scores; the board shows this for T5-base [1][4].
- **Small inconsistencies.** The board ranks Wizard of Wikipedia by KILT-RL, where the paper names F1; the best row is the same under either [1][4]. The paper's Table 6 totals (51,460 dev, 50,736 test) exceed its row sums (51,304; 50,591); the reason is **unstated** [1].
- **Frozen and thin.** 33 of 311 rows date from 2024 or later [4]. Whether recent models have seen the public files is **unstated** (see [contamination](../index/data-contamination.md)).
- **Retrieval is secondary.** BEIR notes that KILT's tasks "involve retrieval, but it is not the primary task" and use Wikipedia only [6].

## Used by

- **Benchmarks.** BEIR contrasts itself with KILT [6]. [EnterpriseRAG-Bench](enterpriserag-bench.md) groups it with other multi-task evaluation frameworks and says that the cited benchmarks in general draw their corpora from public sources [7]. The [HotpotQA](hotpotqa.md) and [Natural Questions](natural-questions.md) pages quote KILT numbers.
- **Papers.** RAG and DPR, whose authors overlap KILT's, are in [the foundations group](../papers/foundations.md). CoRAG reports KILT as a main result [5]. The paper has 939 citations in Semantic Scholar (arXiv record) and 357 in OpenAlex (NAACL record), counts that are not comparable [8].
- **Trends.** No chapter 2 trend cites KILT in the sources read here.
- **Datasets.** [Wikipedia snapshots](../datasets/wikipedia-dpr-kilt.md), [Natural Questions](../datasets/natural-questions.md), [HotpotQA](../datasets/hotpotqa.md), [TriviaQA](../datasets/triviaqa.md).

## Sources

1. https://arxiv.org/abs/2009.02252 : KILT paper v4 (27 May 2021; v1 4 Sep 2020), full text at arxiv.org/html/2009.02252: tasks, metrics, mapping, annotation campaign, Tables 3 to 6; first version date from the arXiv record export.arxiv.org/api/query?id_list=2009.02252 (read 20261102 20:53 UTC; text re-read 20261102 21:26 UTC, record 21:28 UTC)
2. https://github.com/facebookresearch/KILT : README (data catalogue with sizes, hidden test answers, submission limits), `gh api` metadata (archived) (read 20261102 20:53 UTC)
3. https://eval.ai/api/challenges/challenge/689/ : challenge record (end date 2026-01-31, inactive, frozen), evaluation details (read 20261102 20:55 UTC)
4. https://eval.ai/api/challenges/689/challenge_phase_split and https://eval.ai/api/jobs/challenge_phase_split/1899/leaderboard/ to .../1909/leaderboard/ : the eleven boards, 311 rows, ranking metric per phase, submission dates, `submission__participant_team__team_url`, `submission__is_verified_by_host` (read 20261102 20:55 UTC; re-read 20261102 21:27 UTC)
5. https://arxiv.org/abs/2501.14342 : CoRAG v3 (10 Oct 2025), full text: Section 4.1 and Table 2 (one downstream score per task, captioned "scores are sourced directly from the official leaderboard"; no KILT-AC or KILT-EM) (read 20261102 20:56 UTC; re-read 20261102 21:26 UTC)
6. https://arxiv.org/abs/2104.08663 : BEIR v4 (21 Oct 2021), full text: related work on KILT (read 20261102 20:59 UTC)
7. https://arxiv.org/abs/2605.05253 : EnterpriseRAG-Bench v2 (19 May 2026), full text: related work, one sentence on KILT and the paragraph after it (read 20261102 20:59 UTC; re-read 20261102 21:26 UTC)
8. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 939 (read 20261102 20:01 UTC); https://api.openalex.org/works/doi:10.18653/v1/2021.naacl-main.200 : 357 (read 20261102 20:03 to 20:04 UTC); both read by the research pool of this documentation and not re-queried because the APIs rate-limited
9. https://export.arxiv.org/api/query?id_list=2401.00368 : arXiv record of the paper the E5 team's link points to, title only: "Improving Text Embeddings with Large Language Models" (read 20261102 21:28 UTC)
