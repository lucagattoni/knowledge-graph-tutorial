---
type: dataset
kinds: [questions, corpus]
updated: 20261102 21:27 UTC
---

# TriviaQA

This page answers what TriviaQA contains, how large each of its common cuts is, who may use it and what is wrong with it. Most retrieval papers use a questions-and-answers cut of it, not the full release. It has no benchmark page of its own: scores appear on [the KILT page](../benchmarks/kilt.md) and [the RAGSearch page](../benchmarks/ragsearch.md).

## What it contains

Trivia questions with answers, written by trivia enthusiasts and scraped from 14 trivia and quiz-league sites, paired with evidence documents gathered afterwards [1]. The paper counts 95,956 question-answer pairs and 662,659 evidence documents, six per question on average [1]. Evidence comes from the Wikipedia pages of entities that an [entity linker](../index/entity-linking.md) found in the question, and from web pages returned by the Bing search API [1].

In a hand-checked sample of 200 questions, 92.85% of the answers are Wikipedia titles [1]. In 100 sampled Wikipedia question-evidence pairs, 40% need reasoning over several sentences [1]. The data is both a question set and a corpus of evidence.

## Size and versions

| Cut | Contents | Source |
|---|---|---|
| Paper, Wikipedia domain | 61,888 train, 7,993 dev, 7,701 test questions | [1] |
| Paper, Web domain | 76,496 train, 9,951 dev, 9,509 test questions | [1] |
| Paper, unfiltered release | 110,495 question-answer pairs, 740K documents | [1] |
| Hugging Face `unfiltered` | 87,622 train, 11,313 validation, 10,832 test rows | [4] |
| Open-domain cut of [DPR](../papers/foundations.md) | 78,785 train, 8,837 dev, 11,313 test; Bing evidence discarded | [5] |
| KILT | Wikipedia case only, with KILT's own splits; the counts are on [the KILT page](../benchmarks/kilt.md) | [6] |

The project page lists two archives: `triviaqa-rc.tar.gz` (2.5G) and `triviaqa-unfiltered.tar.gz` (604M) [2]. DPR's train plus dev (87,622) and its test (11,313) equal the Hugging Face `unfiltered` train and validation rows (computed); Lewis et al. say the open-domain splits are the unfiltered ones [8]. The introduction says the clean subset has 1,975 triples; Table 6's verified subsets sum to 1,936 questions (computed), unreconciled [1]. The paper has two versions, 20170509 and 20170513 [1]. The repository was last pushed 20240405 [3]. Newer data releases: **unstated**.

## Licence

The sources disagree.

- The project page states no licence, only that the University of Washington "does not own the copyright of the questions and documents included in TriviaQA" [2]. The Hugging Face card repeats this and sets `license: unknown` [4].
- The GitHub repository has an Apache-2.0 `LICENSE`, and its README says it "applies to both the code and the data" [3].

*Reading:* the Apache-2.0 grant covers what the maintainers hold. They also say they do not hold the copyright of the questions and web pages, so the right to redistribute that content is **unstated**.

## How it was made

Questions under four tokens were dropped [1]. For each question the authors took the top 50 Bing results, removed trivia sites and any URL containing "trivia", "question" or "answer", and crawled the top 10 [1]. They added the Wikipedia pages found by the entity linker TAGME, then dropped every document lacking the answer string [1]. The evidence is therefore [distant supervision](../index/distant-supervision.md). The split was random: 80% train, 10% dev, 10% test [1].

## Used by

- **Papers.** [DPR](../papers/foundations.md) trains and tests on the open-domain cut [5]. [RAG](../papers/foundations.md) evaluates on it with prior work's splits [12]. [Self-RAG](../papers/agentic-search.md) says the unfiltered test set is "not publicly available" and scores 11,313 queries from prior work's split [9]. [Search-R1 and Graph-R1](../papers/learned-graph-traversal.md) evaluate on it [10][11]. RAGSearch uses it as one of three general QA sets; the cut it scores is described on [its page](../benchmarks/ragsearch.md) [7].
- **Datasets.** One of KILT's 11, with [Natural Questions](natural-questions.md) and [HotpotQA](hotpotqa.md) [6]; its Wikipedia text is on [the Wikipedia snapshots page](wikipedia-dpr-kilt.md). [PopQA](popqa.md) sits beside it in the same papers [7][10].
- **Benchmarks.** [KILT](../benchmarks/kilt.md), [RAGSearch](../benchmarks/ragsearch.md).
- **Trends.** [Graph-based RAG](../trends/graph-based-rag.md), [Agentic graph retrieval](../trends/learned-graph-traversal.md), [Agentic search](../trends/agentic-search.md).
- **Citations of the paper:** OpenAlex 1,651 for the ACL 2017 record (read 20261102 20:03 UTC; carried over from this documentation's research notes, not re-queried) [13]. Semantic Scholar: **unstated**, not obtained.

## Known problems

- **Noisy evidence.** First-party, from the paper's authors: their qualitative analysis finds that the evidence holds the answer for 79.7% (Wikipedia) and 75.4% (Web) of questions [1]. In their error analysis of 100 sampled wrong predictions of their own BiDAF baseline, 19 had no evidence in any document and 3 a wrong ground truth [1]. These describe the data; the baseline is used only to find the errors, and its scores are not reported here.
- **Test-train overlap.** On the open-domain splits, 71.7% of test answers also occur in the training answers; in 1,000 annotated test pairs, 33.6% had a paraphrase in the training set [8].
- **Cuts are not comparable.** Row counts differ across the paper, Hugging Face, DPR, KILT and RAGSearch (the last two on their benchmark pages). Name the cut with every score.
- **Small samples.** Graph-R1 tests on 128 questions per dataset [11].
- **Age.** Evidence was gathered before May 2017; the crawl date is **unstated** [1].
- **Pretraining contamination** of language models is **unstated** in the sources read.

## Sources

1. https://arxiv.org/pdf/1705.03551 : TriviaQA paper v2 (13 May 2017), full text: contents, Tables 2 and 6, construction, error analysis; arXiv API for versions (read 20261102 21:25 UTC)
2. http://nlp.cs.washington.edu/triviaqa/ : project page: copyright sentence, archive names and sizes (read 20261102 20:52 UTC)
3. https://github.com/mandarjoshi90/triviaqa : README and `LICENSE` (Apache-2.0); repository metadata via `gh api` (read 20261102 20:52 UTC)
4. https://huggingface.co/datasets/mandarjoshi/trivia_qa : card (`license: unknown`) and API metadata; row counts from https://datasets-server.huggingface.co/size?dataset=mandarjoshi/trivia_qa (read 20261102 20:52 and 20:53 UTC)
5. https://arxiv.org/pdf/2004.04906 : DPR v3 (30 Sep 2020), Table 1 and footnote 6 (read 20261102 20:53 UTC)
6. https://arxiv.org/pdf/2009.02252 : KILT v4 (27 May 2021), dataset description, snapshot, Table 6 (read 20261102 20:53 UTC)
7. https://arxiv.org/pdf/2604.09666 : RAGSearch v1 (1 Apr 2026), Section 5.1.1, Appendix A and Table 6 (read 20261102 20:53 UTC)
8. https://arxiv.org/pdf/2008.02637 : Lewis, Stenetorp, Riedel, Question and Answer Test-Train Overlap, v1 (6 Aug 2020), Table 1 and Section 2 (read 20261102 20:54 UTC)
9. https://arxiv.org/pdf/2310.11511 : Self-RAG v1 (17 Oct 2023), Section 4 (read 20261102 20:54 UTC)
10. https://arxiv.org/pdf/2503.09516 : Search-R1 v5 (5 Aug 2025), Section 4.1 (read 20261102 20:54 UTC)
11. https://arxiv.org/pdf/2507.21892 : Graph-R1 v2 (2 Jun 2026), Section 5 and Appendix D (read 20261102 20:54 UTC)
12. https://arxiv.org/pdf/2005.11401 : RAG v4 (12 Apr 2021), Section 3.1 (read 20261102 20:54 UTC)
13. https://api.openalex.org/works/doi:10.18653/v1/p17-1147 : OpenAlex citation count for the ACL 2017 record, carried over from this documentation's research notes (read 20261102 20:03 UTC); not re-queried because the service rate-limits. No archive page holds it
