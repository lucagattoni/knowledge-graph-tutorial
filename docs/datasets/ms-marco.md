---
type: dataset
kinds: [questions, corpus]
benchmark: ms-marco
updated: 20261102 21:25 UTC
---

# MS MARCO

This page answers what the MS MARCO data holds, how large it is, who may use it, and how it was made. The tasks, protocol, scores and the leaderboard are on [the MS MARCO benchmark page](../benchmarks/ms-marco.md). The data is real search queries with web passages, not a knowledge graph. It matters here because the majority of the approaches evaluated in [BEIR](../benchmarks/beir.md) were trained on it [6].

## What it contains

- **Questions.** Anonymised queries from Bing and Cortana logs. A classifier keeps question-like queries and drops navigational and other intents [1].
- **Passages.** On average 10 per question, picked by Bing's passage retriever from web documents. Editors mark the passages they used (`is_selected`) [1].
- **Answers.** Zero or more, written by editors from the passages only. A question may be unanswerable [1].
- **Well-formed answers.** For some questions a second editor rewrote the answer as a full sentence [1].
- **Documents.** URL, title, body and an automatic question type [1].

MS MARCO is a family of data sets and tasks: QnA, text generation, passage and document ranking, keyphrases, conversational search, crawling and click data [2].

## Size and versions

| Part | Size | Source |
|---|---|---|
| Questions | 1,010,916 | [1] |
| Passages | 8,841,823, from 3,563,535 web documents | [1] |
| Well-formed rewritten answers | 182,669 | [1] |
| Passage-ranking training queries | 502,939 (532,761 relevance labels) | [5] |
| Passage-ranking development queries | 6,980 | [5] |
| Document-ranking corpus | 3,213,835 documents; 367,013 training queries | [3] |

The ranking files split the 1,010,916 queries into 808,731 train, 101,093 dev and 101,092 eval [4]. Releases, from the site changelog (US date order) [2]: V1.0 20161201 (100,000 query-answer pairs); V2.0 20180301; V2.1 20180423 (over 1 million queries); passage-ranking set 20181026; document ranking 20200811. QnA, text generation and keyphrase tasks were retired 20201023, but the data stays online [2]. The code repository is archived, last push 20230612 [4].

## Licence

There is no standard licence, and no `LICENSE` file for the data was found in the sources read. The terms say the data is "intended for non-commercial research purposes only", with no licence or other rights extended, supplied "as is" [2][3]. The site warns that "we may not own the underlying rights in the documents" [2][3]. Rights end automatically on violation, and rights holders can ask for removal [3]. The MIT `LICENSE` in the Passage-Ranking repository covers that repository, not the data [4]. The Hugging Face copy under the Microsoft account leaves its licence field as "More Information Needed" [8]. The sources disagree: BEIR's appendix says "Provided under 'MIT License' for non-commercial research purposes" [6]. This page follows the owner's terms [3]. *Reading:* treat it as a read-only reference; use results and ideas, not the data.

## How it was made

1. Sample queries from Bing logs and keep question-like ones [1].
2. Bing retrieves documents; passages are extracted automatically [1].
3. Editors write answers from the passages, mark supporting passages (not exhaustively) and may flag a question as unanswerable [1].
4. A separate editor rewrites an answer if its grammar is poor, it copies a passage, or it cannot be understood alone [1].
5. Documents were taken from Bing's index afterwards; about 300,000 could no longer be found [1].

For passage ranking, all unique passages were pooled into one collection [4]. For document ranking, the source pages were re-scraped in March 2018; the passage label was copied to the document on the assumption that a document with a relevant passage is relevant [3][4]. How candidates are drawn per query is protocol, on the benchmark page.

## Used by

- **Benchmarks:** [MS MARCO](../benchmarks/ms-marco.md), and [BEIR](../benchmarks/beir.md), which notes that "the majority of the evaluated approaches" train on it [6].
- **Datasets and papers:** the PopQA paper uses Contriever, fine-tuned on MS MARCO, as a retriever; see [PopQA](popqa.md) [7].
- **History and trends:** BERT's entry on the passage board is in [language models meet retrieval](../history/language-models-meet-retrieval.md); no trend page mentions it (searched 20261102 20:49 UTC).
- **Citations:** 1,190 for the paper (OpenAlex, arXiv-DOI record, read 20261102 20:03 to 20:04 UTC; not re-queried) [9]. Counts are not comparable across sources.

## Known problems

- **Sparse labels.** Editors need not mark every supporting passage, so a passage with no label is not known to be wrong [1][4].
- **Many questions have no answer.** Without them the sets would be about 35% smaller [4].
- **Fixed bias.** V2.1 removed answers of the V2.0 eval set that could be found in older sets [2].
- **Construction details.** The ranking site says the original QnA data reveals details of how it was built that a real search engine would not have, so it "should be avoided" in ranking submissions [3].

## Sources

1. https://arxiv.org/pdf/1611.09268 : Bajaj et al., MS MARCO, v3 (31 Oct 2018): contents, sizes, construction, caveats (read 20261102 20:42 UTC)
2. https://microsoft.github.io/msmarco/ : family, changelog, retirement notice, terms (read 20261102 20:41 UTC)
3. https://microsoft.github.io/msmarco/Datasets : ranking datasets, record counts, document labels, terms (read 20261102 21:23 UTC)
4. https://github.com/microsoft/MSMARCO-Passage-Ranking : README (body in an HTML comment): splits, passage pool, document re-scrape; MIT `LICENSE`; repository status via `gh api` (read 20261102 21:23 UTC)
5. https://arxiv.org/pdf/2102.07662 : Craswell et al., TREC 2020 Deep Learning Track overview, Tables 1 and 2 (read 20261102 20:45 UTC)
6. https://arxiv.org/pdf/2104.08663 : Thakur et al., BEIR, v4 (21 Oct 2021): introduction text on training data, appendix E on licences (read 20261102 21:21 UTC)
7. https://arxiv.org/pdf/2212.10511 : Mallen et al., When Not to Trust Language Models (PopQA paper): Contriever fine-tuned on MS MARCO (read 20261102 20:47 UTC)
8. https://huggingface.co/datasets/microsoft/ms_marco : card, licensing section (read 20261102 20:47 UTC)
9. https://api.openalex.org/works/doi:10.48550/arxiv.1611.09268 : citation count 1,190, carried over from the research pool (read 20261102 20:03 to 20:04 UTC)
