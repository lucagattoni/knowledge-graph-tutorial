---
type: index
kind: concept
aliases: [dense text retrieval]
updated: 20261102 21:25 UTC
---

# Dense retrieval

Dense retrieval finds passages by comparing learned vectors of the query and the passages, not by matching words. It is the retrieval step behind most vector search and retrieval-augmented generation. Whether it has replaced word-matching methods such as BM25 is still argued.

## Definition

Zhao et al.'s survey defines it: a system learns representations of queries and texts and builds a matching function between the dense vectors; "such a retrieval approach is referred to as dense retrieval, since it employs dense vectors (a.k.a., embeddings)" [1]. The origin of the usual form is Karpukhin et al., who show that retrieval "can be practically implemented using dense representations alone", with embeddings learned by "a simple dual-encoder framework", against sparse methods such as [TF-IDF](./tf-idf.md) or [BM25](./bm25.md) as the de facto method [2].

## How it changed

- **20190601.** Lee et al. learn the retriever and reader together, pretraining the retriever with an Inverse Cloze Task; learned retrieval beats BM25 by up to 19 points of exact match where users truly seek an answer (first-party) [3]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20200410.** Karpukhin et al. report their dense retriever 9 to 19 points above a Lucene-BM25 system in top-20 passage accuracy (first-party) [2].
- **20200522.** Lewis et al. use a dense vector index of Wikipedia as the memory of a generator: [retrieval-augmented generation](./retrieval-augmented-generation.md) [4].
- **20201013.** Lin, Nogueira and Yates split transformer text ranking into reranking and dense retrieval, where the latter "perform ranking directly" [5]; see [reranking](./reranking.md).
- **20210417.** BEIR tests 10 systems on 18 datasets zero-shot and finds BM25 robust, with dense models often under-performing [6].
- **20260511 and 20261022.** A BM25 search agent beats released agents that use dense retrievers on BrowseComp-Plus (first-party) [7], while dense retrieval plus reranking ranks first in six of seven memory-benchmark settings [8]. See [agentic search](../trends/agentic-search.md) and [agent memory](../trends/agent-memory.md).

## Where sources disagree

Replacement. Stonebraker and Pavlo write that inverted-index search engines "have been supplanted in recent years" by similarity search on embeddings [9]. BEIR finds BM25 "a robust baseline" zero-shot [6]; Lee et al. find BM25 sufficient where the questioner already knows the answer [3]; the Pi-Serini authors report a tuned BM25 agent ahead of released agents that use dense retrievers [7].

## Related

[BM25](./bm25.md), [TF-IDF](./tf-idf.md), [embedding](./embedding.md), [vector search](./vector-search.md), [approximate nearest neighbour](./approximate-nearest-neighbour.md), [hybrid search](./hybrid-search.md), [reranking](./reranking.md), [BERT](./bert.md), [information retrieval](./information-retrieval.md). Benchmark: [BEIR](../benchmarks/beir.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Language models meet retrieval (2018-2022)](../history/language-models-meet-retrieval.md)

**Trends**

- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Benchmarks**

- [BEIR](../benchmarks/beir.md)
- [STaRK](../benchmarks/stark.md)

**Index**

- [Approximate nearest neighbour](approximate-nearest-neighbour.md)
- [BERT](bert.md)
- [BM25](bm25.md)
- [Embedding](embedding.md)
- [Exact match](exact-match.md)
- [HNSW](hnsw.md)
- [Hybrid search](hybrid-search.md)
- [Information retrieval](information-retrieval.md)
- [Inverted index](inverted-index.md)
- [Question answering](question-answering.md)
- [Ranked retrieval](ranked-retrieval.md)
- [Relevance feedback](relevance-feedback.md)
- [Reranking](reranking.md)
- [Retrieval-augmented generation](retrieval-augmented-generation.md)
- [tf-idf](tf-idf.md)
- [Transformer](transformer.md)
- [Vector search](vector-search.md)
- [Vector space model](vector-space-model.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2211.14876 : Zhao et al., "Dense Text Retrieval based on Pretrained Language Models: A Survey", v1 20221127; abstract (read 20261102 20:50 UTC)
2. https://arxiv.org/abs/2004.04906 : Karpukhin et al., "Dense Passage Retrieval for Open-Domain Question Answering", v1 20200410; abstract (read 20261102 20:45 UTC)
3. https://arxiv.org/abs/1906.00300 : Lee, Chang, Toutanova, "Latent Retrieval for Weakly Supervised Open Domain Question Answering", v1 20190601; abstract (read 20261102 20:50 UTC)
4. https://arxiv.org/abs/2005.11401 : Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", v1 20200522; abstract (read 20261102 20:50 UTC)
5. https://arxiv.org/abs/2010.06467 : Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking: BERT and Beyond", v1 20201013; abstract (read 20261102 20:50 UTC)
6. https://arxiv.org/abs/2104.08663 : Thakur et al., "BEIR", v1 20210417; abstract (read 20261102 20:50 UTC)
7. https://arxiv.org/abs/2605.10848 : Hsu, Yang, Lin, "Rethinking Agentic Search with Pi-Serini", v1 20260511; abstract (read 20261102 20:50 UTC)
8. https://arxiv.org/abs/2610.30755 : Bao et al., "Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought", v1 20261022; abstract (read 20261102 20:50 UTC)
9. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), 2024, section 2.5 (read 20261102 20:51 UTC)
