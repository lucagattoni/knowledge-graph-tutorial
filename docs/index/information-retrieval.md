---
type: index
kind: concept
aliases: [IR]
updated: 20261102 21:22 UTC
---

# Information retrieval

This entry says what information retrieval (IR) is and marks the dated turns in its history: the name, ranked retrieval, shared test collections, the web, and neural ranking.

## Definition

An information retrieval system locates information that is relevant to a user's query. In the history by Sanderson and Croft, such a system typically searches collections of unstructured or semi-structured data, for example web pages, documents, images and video, and is needed when a collection grows beyond what manual cataloguing can handle [1].

## How it changed

- **About 1950.** The term "information retrieval" is first used around the time of Luhn's punch-card selector, whose prototypes date from 1950; Mooers wrote of "machine searching and retrieval of information" in a March paper [1]. See [the advent](../history/advent.md).
- **1950s.** Luhn proposes, and Maron, Kuhns and Ray test, giving each document a relevance score instead of the exact match of [Boolean retrieval](./boolean-retrieval.md) [1]. See [ranked retrieval](./ranked-retrieval.md) and [formal foundations](../history/formal-foundations.md) for the weighting schemes of the 1970s ([tf-idf](./tf-idf.md), the [vector space model](./vector-space-model.md)).
- **1992.** TREC starts, co-sponsored by NIST and the US Department of Defense, to support IR research [2]. Almost all commercial systems still used Boolean search until the early to mid 1990s [1]. See [knowledge systems](../history/knowledge-systems.md).
- **Late 1993.** Web search engines begin to emerge as the number of web sites grows [1]. See [the Web era](../history/the-web.md) and [web search engine](./web-search-engine.md).
- **2018-2020.** BERT is first submitted to arXiv in October 2018 [3]. The book by Lin, Nogueira and Yates (arXiv 20201013) reports that after the TREC 2019 Deep Learning Track the organisers saw a distinction that "separated two different 'eras'" of neural text ranking, and that [BM25](./bm25.md) "still provides the starting point of many text ranking approaches" [4]. See [language models meet retrieval](../history/language-models-meet-retrieval.md).

## Where sources disagree

The sources scope the field differently, which is a difference of scope, not a dispute. Sanderson and Croft include images and video [1]. Lin and colleagues study "text ranking", which they say reaches beyond IR into question answering, recommendation and entity linking, and name it that way because the ranked units are often sentences or paragraphs, not documents [4]. On the dates above the sources read do not conflict.

## Related

[Boolean retrieval](./boolean-retrieval.md), [ranked retrieval](./ranked-retrieval.md), [tf-idf](./tf-idf.md), [BM25](./bm25.md), [vector space model](./vector-space-model.md), [relevance feedback](./relevance-feedback.md), [learning to rank](./learning-to-rank.md), [TREC](./trec.md), [question answering](./question-answering.md), [dense retrieval](./dense-retrieval.md), [hybrid search](./hybrid-search.md), [retrieval-augmented generation](./retrieval-augmented-generation.md); papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [The advent: machines that hold knowledge](../history/advent.md)
- [The semantic web and linked data](../history/semantic-web.md)

**Benchmarks**

- [BEIR](../benchmarks/beir.md)
- [MS MARCO](../benchmarks/ms-marco.md)

**Index**

- [Approximate nearest neighbour](approximate-nearest-neighbour.md)
- [AUROC](auroc.md)
- [BM25](bm25.md)
- [Boolean retrieval](boolean-retrieval.md)
- [Dense retrieval](dense-retrieval.md)
- [grep](grep.md)
- [Hybrid search](hybrid-search.md)
- [Inverted index](inverted-index.md)
- [Learning to rank](learning-to-rank.md)
- [PageRank](pagerank.md)
- [Probability ranking principle](probability-ranking-principle.md)
- [Question answering](question-answering.md)
- [R-precision](r-precision.md)
- [Ranked retrieval](ranked-retrieval.md)
- [Relevance feedback](relevance-feedback.md)
- [Reranking](reranking.md)
- [Retrieval-augmented generation](retrieval-augmented-generation.md)
- [Stemming](stemming.md)
- [tf-idf](tf-idf.md)
- [Token](token.md)
- [TREC](trec.md)
- [Vector space model](vector-space-model.md)
- [Web search engine](web-search-engine.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE 2012 (author manuscript): definition, first use of the term, Mooers, ranked retrieval, Boolean until the early to mid 1990s, web search from late 1993 (read 20261102 20:49 UTC)
2. https://trec.nist.gov/overview.html : NIST, TREC overview: began in 1992, co-sponsors, purpose (read 20261102 20:50 UTC)
3. https://arxiv.org/abs/1810.04805 : Devlin et al., BERT, first submitted October 2018 (read 20261102 20:57 UTC)
4. https://arxiv.org/abs/2010.06467 : Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking: BERT and Beyond", v1 20201013 (abstract read 20261102 20:50 UTC); sections 1, 1.1, 1.2.2, 1.2.4 via https://ar5iv.labs.arxiv.org/html/2010.06467 (read 20261102 20:58 UTC); the TREC 2019 Deep Learning Track passage is in section 1.2.4
