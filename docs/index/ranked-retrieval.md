---
type: index
kind: concept
aliases: [text ranking, ranked search]
updated: 20261102 21:25 UTC
---

# Ranked retrieval

This entry answers what it means to return documents in an order of relevance instead of as an exact-match set. It says who proposed the idea and why it took until the 1990s to reach commercial search.

## Definition

In ranked retrieval each document in a collection gets a score for how relevant it is to a query. The documents are sorted by that score, and those at the top ranks are returned [1]. Sanderson and Croft set it against [Boolean retrieval](./boolean-retrieval.md), where a query is a logical combination of terms and the result is the set of documents that match exactly [1]. Lin, Nogueira and Yates state the goal for modern systems: "to generate an ordered list of texts retrieved from a corpus in response to a query" [2].

## How it changed

- **1957 to 1959.** Sanderson and Croft say Luhn proposed scoring documents (1957) and that Maron, Kuhns and Ray tested the idea in a technical memorandum of 195906. On 200 documents and 39 queries it beat Boolean search [1]. See [The advent](../history/advent.md).
- **1960s to 1970s.** Salton's group ranked documents by the cosine of the angle between document and query vectors. Spärck Jones added inverse document frequency in the 1970s, and Robertson defined the probability ranking principle [1]. See [Formal foundations](../history/formal-foundations.md).
- **1980s to mid-1990s.** Variations of tf-idf weighting appeared, and work on the probabilistic model ended in [BM25](./bm25.md) [1].
- **Early to mid-1990s.** Experiments had shown ranking to be the more effective method, yet almost all commercial systems stayed Boolean until about then. Sanderson and Croft name WESTLAW's WIN system and web search engines as the change [1]. See [The Web changes data and search](../history/the-web.md).
- **2020 and 2021.** Lin et al. (first version 20201013, third 20210819) survey transformers for ranking in two groups: reranking in multi-stage systems, and dense retrieval that ranks directly [2]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).

## Where sources disagree

**The year.** Sanderson and Croft cite Luhn's 1957 paper for the alternative approach. They then write that "in the same year as Maron et al's work" Luhn suggested that word frequency measures word significance, but cite a 1958 paper for that, while the Maron memorandum is dated 1959 [1]. This entry gives the range 1957 to 1959; the text does not settle which paper first proposed ranking.

## Related

[Boolean retrieval](./boolean-retrieval.md) · [information retrieval](./information-retrieval.md) · [tf-idf](./tf-idf.md) · [BM25](./bm25.md) · [vector space model](./vector-space-model.md) · [probability ranking principle](./probability-ranking-principle.md) · [reranking](./reranking.md) · [dense retrieval](./dense-retrieval.md) · [BEIR](../benchmarks/beir.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [The advent: machines that hold knowledge](../history/advent.md)

**Index**

- [Boolean retrieval](boolean-retrieval.md)
- [Information retrieval](information-retrieval.md)
- [Inverted index](inverted-index.md)
- [Learning to rank](learning-to-rank.md)
- [Mean reciprocal rank](mean-reciprocal-rank.md)
- [nDCG](ndcg.md)
- [Probability ranking principle](probability-ranking-principle.md)
- [R-precision](r-precision.md)
- [Relevance feedback](relevance-feedback.md)
- [Stemming](stemming.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE 100, 2012: section "Ranked retrieval", the 1960s, 1970s, 1980s to mid-1990s, references to Luhn (1957, 1958), Maron, Kuhns and Ray (195906) and Turtle (SIGIR 1994) (read 20261102 20:56 UTC)
2. https://arxiv.org/abs/2010.06467 : Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking: BERT and Beyond", v1 20201013, v3 20210819, abstract: the text-ranking goal and the two groups of methods (read 20261102 20:56 UTC)
