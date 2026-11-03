---
type: index
kind: concept
aliases: [embeddings, text embedding, vector embedding]
updated: 20261102 21:25 UTC
---

# Embedding

An embedding is a vector of numbers that stands for a piece of data, usually a word, a passage or an image, so that similar items lie near each other. This page defines the term for text, dates its main steps and records where sources disagree on whether embeddings replaced word-matching search.

## Definition

Stonebraker and Pavlo describe embeddings as made by AI tools that "use learned transformations to convert a record's data (e.g., text, image) into a vector representing its latent semantics" [1]. Lin, Nogueira and Yates call the output of a text encoder a dense representation, typically a fixed-width vector of hundreds of dimensions with non-zero values, unlike a sparse vector with one dimension per vocabulary word [2]. Embeddings of two texts can be compared with cosine similarity [3]. For graphs see [knowledge graph embedding](./knowledge-graph-embedding.md).

## How it changed

- **197511.** Salton, Wong and Yang publish "A vector space model for automatic indexing", the sparse ancestor [4]. Era: [Formal foundations](../history/formal-foundations.md).
- **2003.** Bengio et al. learn a distributed representation of words [5].
- **20130116.** Mikolov et al. post word2vec, continuous vector representations of words [6]. Lin et al. report it is often seen as the start of the "neural revolution" in language processing [2].
- **20181011.** BERT is posted; its output is a contextual embedding for each input token [7][2]. See [BERT](./bert.md).
- **20190827.** Sentence-BERT derives sentence embeddings: finding the most similar pair among 10,000 sentences drops from about 65 hours to about 5 seconds (first-party) [3].
- **20200410.** Karpukhin et al. retrieve passages with learned embeddings alone, 9 to 19 points above Lucene-BM25 on top-20 accuracy (first-party) [8]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **202406.** Stonebraker and Pavlo report dozens of new vector database systems built to store and search embeddings [1].
- **2025 to 2026, still moving.** The README of [PageIndex](../projects/pageindex.md), read 20261102, replaces the vector index with a tree index and argues "similarity ≠ relevance" (first-party) [9]. See [vectorless retrieval](../trends/reasoning-over-structure.md).

## Where sources disagree

Stonebraker and Pavlo write that inverted-index search engines "have been supplanted" by similarity search on embeddings [1]. Lin et al. (2021) say [BM25](./bm25.md) still starts many text-ranking approaches, yet note Facebook's first stage moved to embeddings [2]. *Reading:* embeddings replaced keywords in some pipelines, not as a general fact; [hybrid search](./hybrid-search.md) keeps both.

## Related

[Vector space model](./vector-space-model.md), [dense retrieval](./dense-retrieval.md), [vector search](./vector-search.md), [approximate nearest neighbour](./approximate-nearest-neighbour.md), [retrieval-augmented generation](./retrieval-augmented-generation.md), [agent memory](./agent-memory.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Projects**

- [Basic Memory](../projects/basic-memory.md)
- [Code-Graph-RAG](../projects/code-graph-rag.md)
- [Cognee](../projects/cognee.md)
- [Dify](../projects/dify.md)
- [Graphify](../projects/graphify.md)
- [GraphRAG SDK](../projects/graphrag-sdk.md)
- [HippoRAG](../projects/hipporag.md)
- [Hyper-Extract](../projects/hyper-extract.md)
- [LightRAG](../projects/lightrag.md)
- [MCP reference servers](../projects/mcp-servers.md)
- [Mem0](../projects/mem0.md)
- [Memgraph](../projects/memgraph.md)
- [Neo4j](../projects/neo4j.md)
- [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md)
- [PageIndex](../projects/pageindex.md)
- [Projects](../projects/README.md)

**Papers**

- [Papers: Agent memory](../papers/agent-memory.md)
- [Papers: Vectorless retrieval](../papers/reasoning-over-structure.md)

**Datasets**

- [Wikipedia snapshots of DPR and KILT](../datasets/wikipedia-dpr-kilt.md)

**Benchmarks**

- [MultiHop-RAG](../benchmarks/multihop-rag.md)

**Experiments**

- [Instruments](../experiments/instruments.md)

**Applied to Pinakes**

- [Applied to Pinakes](../applied-to-pinakes/README.md)
- [Measurements](../applied-to-pinakes/measurements.md)

**Index**

- [Approximate nearest neighbour](approximate-nearest-neighbour.md)
- [BERT](bert.md)
- [Chunking](chunking.md)
- [Community report](community-report.md)
- [ConceptNet](conceptnet.md)
- [Dense retrieval](dense-retrieval.md)
- [HNSW](hnsw.md)
- [Hybrid search](hybrid-search.md)
- [Knowledge graph embedding](knowledge-graph-embedding.md)
- [Large language model](large-language-model.md)
- [Memory poisoning](memory-poisoning.md)
- [RAPTOR](raptor.md)
- [Retrieval-augmented generation](retrieval-augmented-generation.md)
- [Token](token.md)
- [Transformer](transformer.md)
- [Tree index](tree-index.md)
- [Vector search](vector-search.md)
- [Vector space model](vector-space-model.md)
- [Vectorless retrieval](vectorless-retrieval.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), June 2024: embeddings, vector DBMSs, "supplanted" (read 20261102 20:50 UTC)
2. https://arxiv.org/pdf/2010.06467 : Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking", v0.99 of 20210820: dense against sparse representations, word2vec, BM25, Facebook search (read 20261102 20:50 UTC)
3. https://arxiv.org/abs/1908.10084 : Reimers and Gurevych, "Sentence-BERT", abstract, v1 20190827 (read 20261102 20:50 UTC)
4. https://api.crossref.org/works/10.1145/361219.361220 : Salton, Wong, Yang, CACM 18(11), November 1975 (read 20261102 20:52 UTC)
5. https://www.jmlr.org/papers/v3/bengio03a.html : Bengio et al., "A Neural Probabilistic Language Model", JMLR 3, 1137-1155, 2003, abstract (read 20261102 20:50 UTC)
6. https://arxiv.org/abs/1301.3781 : Mikolov et al., "Efficient Estimation of Word Representations in Vector Space", v1 20130116 (read 20261102 20:50 UTC)
7. https://arxiv.org/abs/1810.04805 : Devlin et al., BERT, v1 20181011 (read 20261102 20:50 UTC)
8. https://arxiv.org/abs/2004.04906 : Karpukhin et al., "Dense Passage Retrieval for Open-Domain Question Answering", v1 20200410, abstract (read 20261102 20:50 UTC)
9. https://raw.githubusercontent.com/VectifyAI/PageIndex/main/README.md : PageIndex README: tree index in place of a vector index, "similarity ≠ relevance" (read 20261102 20:51 UTC)
