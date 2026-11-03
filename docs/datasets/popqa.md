---
type: dataset
kinds: [questions]
updated: 20261102 21:27 UTC
---

# PopQA

This page answers what PopQA contains, why its questions are about rare entities, how large and how licensed it is, and what is wrong with it or with how it is described. Each question is a [triple](../index/triple.md) from [Wikidata](wikidata.md) turned into words. It has no benchmark page of its own: scores appear on [the RAGSearch page](../benchmarks/ragsearch.md).

## What it contains

About 14,000 [open-domain](../index/open-domain-question-answering.md) questions about entities of widely varying popularity, most of them rare [1]. A row holds the question, the gold answers, and for the subject and the object their Wikidata ID, URI, aliases and Wikipedia title, plus the Wikipedia monthly page views of each ("popularity") [2][3]. There are 16 relation types, each with one hand-written question template: occupation, place of birth, genre, father, country, producer, director, capital of, screenwriter, composer, color, religion, sport, author, mother and capital [1]. An example is "What is George Rankin's occupation?", answer "politician" [2].

The authors built it to study how far language models memorise rare facts and to compare memory with retrieval [1]. Their own results are in the paper, not repeated here.

## Size and versions

| Cut | Contents | Source |
|---|---|---|
| Release | 14,267 rows, one `test` split, 17 columns, 5.2 MB | [3][4] |
| Paper | "14k questions"; Figure 4 labels the aggregate n=14,267 and shows eight of the 16 relations, for example director 1,999, author 1,514, country 838 | [1] |
| Self-RAG | the long-tail subset: 1,399 queries with fewer than 100 monthly page views | [5] |
| HippoRAG 2 | 1,000 queries over 8,676 passages from a December 2021 Wikipedia dump | [6] |

Appendix B says 14,282 questions were run through GPT-3, unreconciled with 14,267 [1]. The paper appeared 20221220; its fourth version, the ACL 2023 one, 20230702 [1]. The Hugging Face dataset was created 20221222 [3]; the repository, with `data/popQA.tsv`, was last pushed 20250702 [2]. The Wikidata dump date and the page-view period are **unstated**. The paper's retrieval corpus is the December 2018 Wikipedia dump [1].

## Licence

**No data licence is stated.** The repository `LICENSE` is MIT, "Copyright (c) 2023 Alex Mallen"; its README gives no data licence, so the file is read as covering the code [2]. The Hugging Face card has no licence field [3], and the paper states none [1]. Wikidata's structured data is under CC0 [8]; whether that carries over to the questions, and the licence of the page-view counts, is **unstated**.

## How it was made

The authors randomly sampled Wikidata triples of the 16 relation types and verbalised each with its template. The answers are all entities E with the triple (S, R, E) in the knowledge base [1]. Popular entities were given more weight, since the tail alone would leave too few high-popularity questions. A triple is kept only if f > exp(8R − 6), where R is a uniform random number and f the exact-match term frequency of the subject's aliases in an 800 MB sample of C4. No more than 2,000 triples per relation were kept [1]. Popularity is the subject's Wikipedia monthly page views, which the paper notes can be fetched through the Wikipedia API [1]. The motive: Natural Questions is "often dominated by subject entities with high popularity" [1].

## Used by

- **Papers.** Its own paper, which also introduces Adaptive Retrieval [1]. [Self-RAG](../papers/agentic-search.md) uses the long-tail subset [5]. [Search-R1 and Graph-R1](../papers/learned-graph-traversal.md) evaluate on it [9][10]. [HippoRAG 2](../papers/graph-based-rag.md) uses it as a test of factual memory [6]. RAGSearch uses all of it [7].
- **Datasets.** With [TriviaQA](triviaqa.md) and [Natural Questions](natural-questions.md), one of three "general QA" sets in RAGSearch and Search-R1 [7][9].
- **Benchmarks.** [RAGSearch](../benchmarks/ragsearch.md).
- **Trends.** [Graph-based RAG](../trends/graph-based-rag.md), [Agentic graph retrieval](../trends/learned-graph-traversal.md), [Agentic search](../trends/agentic-search.md).
- **Citations of the paper:** OpenAlex 342 for the ACL 2023 record (read 20261102 20:04 UTC; carried over from this documentation's research notes, not re-queried) [11]. Semantic Scholar: **unstated**, not obtained.

## Known problems

- **Synthetic and templated.** The authors call the two datasets they used, PopQA and EntityQuestions, "synthetic" and say transfer to natural questions is not firmly established. Popularity is time-dependent and only one proxy [1].
- **Guessable relations.** Some, such as country, can be answered from clues in the subject's name: accuracy is high with no popularity trend [1].
- **Single-hop.** Every question is one triple [1].
- **Mis-described by later papers.** RAGSearch calls it a "Popular-knowledge question set" and Graph-R1 "popular culture questions sourced from Wikipedia" [7][10]. Its authors built it from Wikidata for the long tail [1].
- **One split, many re-splits.** The release has only a test split [3]. Graph-R1 says it samples 5,120 training instances per dataset, PopQA included; how is **unstated** in the text read [10]. Row counts and corpora differ by paper (table above), so scores are not comparable across papers.
- **Pretraining contamination** of language models is **unstated** in the sources read.

## Sources

1. https://arxiv.org/pdf/2212.10511 : PopQA paper v4 (2 Jul 2023), full text: Sections 1 to 5, Figure 4, Appendices A and B; arXiv API for dates (read 20261102 21:25 UTC)
2. https://github.com/AlexTMallen/adaptive-retrieval : README and `LICENSE` (MIT); repository metadata via `gh api` (read 20261102 20:51 UTC)
3. https://huggingface.co/datasets/akariasai/PopQA : card (no licence field) and API metadata; row count from https://datasets-server.huggingface.co/size?dataset=akariasai/PopQA (read 20261102 20:51 and 20:52 UTC)
4. https://huggingface.co/datasets/akariasai/PopQA/raw/main/README.md : card text, field list, 5.2 MB (read 20261102 20:52 UTC)
5. https://arxiv.org/pdf/2310.11511 : Self-RAG v1 (17 Oct 2023), Section 4 (read 20261102 20:54 UTC)
6. https://arxiv.org/pdf/2502.14802 : HippoRAG 2 v2 (19 Jun 2025), Table 1 and Section 4.2 (read 20261102 20:54 UTC)
7. https://arxiv.org/pdf/2604.09666 : RAGSearch v1 (1 Apr 2026), Section 5.1.1, Appendix A and Table 6 (read 20261102 20:53 UTC)
8. https://www.wikidata.org/wiki/Wikidata:Licensing : CC0 for structured data (read 20261102 20:53 UTC)
9. https://arxiv.org/pdf/2503.09516 : Search-R1 v5 (5 Aug 2025), Section 4.1 (read 20261102 20:54 UTC)
10. https://arxiv.org/pdf/2507.21892 : Graph-R1 v2 (2 Jun 2026), Section 5 and Appendix D (read 20261102 20:54 UTC)
11. https://api.openalex.org/works/doi:10.18653/v1/2023.acl-long.546 : OpenAlex citation count for the ACL 2023 record, carried over from this documentation's research notes (read 20261102 20:04 UTC); not re-queried because the service rate-limits. No archive page holds it
