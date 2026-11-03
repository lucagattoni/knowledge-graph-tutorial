---
type: dataset
kinds: [questions, corpus]
benchmark: natural-questions
updated: 20261102 23:19 UTC
---

# Natural Questions

This page answers what the Natural Questions (NQ) data is: where the questions come from, how many there are, who may use them and what is known to be wrong with them. How systems are scored on it, and the results, are on [the Natural Questions benchmark page](../benchmarks/natural-questions.md).

## What it contains

Real, anonymised, aggregated queries sent to the Google search engine. Each query is paired with one Wikipedia page from the top five search results. An annotator marks a long answer (typically a paragraph), a short answer (one or more entities, or yes/no) if the page has one, or null [1]. Every query has eight words or more [1].

Each example holds the rendered HTML of the whole page, a token list, long-answer candidates and the annotations [2]; so the data is both a question set and a corpus of annotated pages. Of the long answers, 72.9% are paragraphs and 19.0% tables [2].

## Size and versions

| Version | Size | Source |
|---|---|---|
| Paper (TACL, 2019) | 307,373 training examples with one annotation; 7,830 development and 7,842 test examples with five annotations each. The test set is sequestered | [1] |
| Training set, detail | 152,148 have a long answer; 110,724 a short answer (106,926 span sets, 3,798 yes/no) | [2] |
| [Open-domain](../index/open-domain-question-answering.md) form used by DPR (question and answer string; splits as in Lee et al. 2019) | 79,168 train, 8,757 dev, 3,610 test; 58,880 train questions kept after matching to passages | [4] |
| KILT version | the test set is a held-out portion obtained from the NQ authors; mean provenance pages per question raised from 1 to 1.57 by crowd annotation of dev and test | [5] |
| BEIR version | 3,452 test queries over 2,681,468 passages; queries without an answer, with a table answer or with conflicting pages removed | [6] |
| HippoRAG 2 sample | 1,000 queries over 9,633 passages | [7] |

The repository README says "307,372" in one sentence and "307,373" in another; the paper and the Hugging Face card say 307,373 [1][2][3]. The Wikipedia snapshot date of the pages is **unstated** in the paper and README [1][2]. The Wikipedia text behind the open-domain form is on [the Wikipedia snapshots page](wikipedia-dpr-kilt.md).

## Licence

- The Hugging Face card gives CC BY-SA 3.0 [3]. The BEIR paper lists NQ under the same licence [6].
- The GitHub repository carries an Apache-2.0 `LICENSE` file. Its README states no data licence, so the file is read as covering the code [2].
- The official data page returned only the word "Loading..." and no licence text [8].
- The paper's CC BY 4.0 notice covers the paper [1].

*Reading:* the data licence is CC BY-SA 3.0 according to two secondary sources (the Hugging Face card and the BEIR paper); no first-party statement could be read. Check before relying on it.

## How it was made

Queries came from the search stream: eight words or more, issued by several users in a short period, and kept if they match one of five heuristics (for example starting with "who", "when" or "where" and a verb form) that discard non-questions. A question is kept if a Wikipedia page appears in its top five results [1].

About 50 annotators worked at 80 seconds per item. One annotator does three steps in order: judge the question, pick the smallest HTML box that answers it, mark the short answer [1].

Quality was checked afterwards by four experts on 139 sampled non-null answers: precision 90% for long answers and 84% for short answers [1]. Annotations by 25 annotators on 302 examples were used to study how annotators vary [1].

## Used by

- **Papers.** [DPR, REALM and RAG](../papers/foundations.md) train or test on open-domain NQ [4][13]. [HippoRAG 2](../papers/graph-based-rag.md), the [RAG versus GraphRAG study](../papers/graph-based-rag.md) and RAGSearch use it as their single-hop set [7][11][12]. MuSiQue was composed partly from NQ questions [10].
- **Datasets.** [MuSiQue](musique.md) seeds from it [10]; [PopQA](popqa.md) was built partly in response to that skew [9].
- **Benchmarks.** [Natural Questions](../benchmarks/natural-questions.md), [KILT](../benchmarks/kilt.md), [BEIR](../benchmarks/beir.md), [RAGSearch](../benchmarks/ragsearch.md).
- **Trends and projects.** [Graph-based RAG](../trends/graph-based-rag.md); the [HippoRAG](../projects/hipporag.md) project.
- **Citations of the paper** (services not comparable): OpenAlex 2,070 (read 20261102 20:03 UTC); Semantic Scholar 5,455 (read 20261102 20:05 UTC). The archive holds no count; both are carried from this documentation's research notes [14].

## Known problems

- **Annotators disagree.** The authors found real ambiguity in whether a page answers a question, and built five-way annotation for that reason [1]. The precision figures rest on a sample of 139 [1].
- **Overlap of pages.** 79% of the Wikipedia pages in the development set also appear in the training set [1].
- **Skew.** The PopQA authors found that NQ is "often dominated by subject entities with high popularity" [9]. The NQ authors name the choice of Wikipedia as a possible bias and leave shorter queries and "how to" questions to later collections [1].
- **Leakage into MuSiQue.** MuSiQue's dev and test sub-questions may occur in NQ's training set; its README releases their IDs to exclude [15].
- **Maintenance.** The GitHub repository is archived; its last push was 20210730 [2]. The Hugging Face card leaves its creation, annotator and bias sections as "[More Information Needed]" [3].
- **Pretraining contamination** of language models is **unstated** in the sources read.

## Sources

1. https://aclanthology.org/Q19-1026.pdf : NQ paper (TACL 7, published 7/2019), full text: collection, sizes, heuristics, quality (read 20261102 20:41 UTC)
2. https://github.com/google-research-datasets/natural-questions : README, `LICENSE`; repository metadata via `gh api` (read 20261102 20:41 and 20:45 UTC)
3. https://huggingface.co/datasets/google-research-datasets/natural_questions : card and API metadata (read 20261102 20:41 UTC); card licence field re-read 20261102 21:22 UTC
4. https://arxiv.org/pdf/2004.04906 : DPR paper v3 (30 Sep 2020), Table 1 and Section 4 (read 20261102 20:41 UTC)
5. https://arxiv.org/pdf/2009.02252 : KILT paper v4 (27 May 2021), Section 3.4 (read 20261102 20:41 UTC)
6. https://arxiv.org/pdf/2104.08663 : BEIR paper v4 (21 Oct 2021), Appendix D and licence list (read 20261102 20:47 and 21:21 UTC)
7. https://arxiv.org/pdf/2502.14802 : HippoRAG 2 v2 (19 Jun 2025), Table 1 (read 20261102 20:44 UTC)
8. https://ai.google.com/research/NaturalQuestions : official page, script-rendered, shows only "Loading..." (read 20261102 20:41 UTC)
9. https://arxiv.org/pdf/2212.10511 : PopQA paper, Section 3.3 (read 20261102 20:44 UTC)
10. https://arxiv.org/pdf/2108.00573 : MuSiQue paper v3, construction from seed sets (read 20261102 20:44 UTC)
11. https://arxiv.org/pdf/2502.11371 : RAG versus GraphRAG v3 (4 Mar 2026), Section 4.1 (read 20261102 20:41 UTC)
12. https://arxiv.org/pdf/2604.09666 : RAGSearch v1 (1 Apr 2026), Section 5.1 and Table 6 (read 20261102 20:41 UTC)
13. https://arxiv.org/pdf/2005.11401 : RAG v4 (12 Apr 2021); https://arxiv.org/pdf/2002.08909 : REALM v1 (10 Feb 2020) (read 20261102 20:44 UTC)
14. https://api.openalex.org/works/doi:10.1162/tacl_a_00276 and https://api.semanticscholar.org/graph/v1/paper/DOI:10.1162/tacl_a_00276 : citation counts, carried over from this documentation's research notes, kept in [`plans/evidence/`](../../plans/evidence/datasets-benchmarks-pool-question-sets-and-corpora.md) (read 20261102 20:03 and 20:05 UTC); not re-queried because both services rate-limit
15. https://github.com/StonyBrookNLP/musique : README, usage caution on seed datasets (read 20261102 20:46 UTC)
