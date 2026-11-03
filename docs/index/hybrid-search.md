---
type: index
kind: concept
aliases: [hybrid retrieval]
updated: 20261102 21:22 UTC
---

# Hybrid search

This entry says what hybrid search is, how its fusion methods developed, and where the evidence is mixed.

## Definition

Hybrid search is text retrieval in which lexical and semantic search are fused: Bruch, Gai and Ingber study "hybrid search in text retrieval where lexical and semantic search are fused together" [1]. Lexical search matches the words of a query, typically scored with [BM25](./bm25.md). Semantic search compares learned [embeddings](./embedding.md), as in [dense retrieval](./dense-retrieval.md) and [vector search](./vector-search.md). The premise is that the two are "complementary in how they model relevance" [1].

## How it changed

- **2009.** Cormack, Clarke and Buettcher publish [reciprocal rank fusion](./reciprocal-rank-fusion.md), which sums 1/(60 + rank) over the input rankings, as a method for combining the rankings of several IR systems [3].
- **202004.** Karpukhin and colleagues (DPR, first version 20200410) rerank the union of the top 2000 passages from BM25 and their dense retriever, scoring BM25 plus 1.1 times the dense score [2]. Gains are uneven: for the single-dataset model, top-20 accuracy on SQuAD rises from 63.2 to 71.5 and on Natural Questions falls from 78.4 to 76.6 [2]. See [this era](../history/language-models-meet-retrieval.md).
- **202210.** Bruch, Gai and Ingber (Bruch and Ingber at Pinecone, a vector-database company; Gai, of UC Berkeley, contributed during an internship at Pinecone [1]) report that a weighted convex combination of scores beats RRF in and out of domain [1].
- **202312.** The RAG survey of Gao and colleagues describes sparse and dense retrieval as able to benefit from "complementary relevance information" [4].
- **2025-2026.** Hybrid retrieval is a listed feature of "Modular RAG" in the agentic RAG survey (version 4, 20260401) [5]. Mem0 2.0.0 (label 20260414) fuses semantic similarity, BM25 keyword match and entity signals into one score; first-party [6]. See [Mem0](../projects/mem0.md).

## Where sources disagree

- **RRF or convex combination.** Bruch and colleagues call their finding "in disagreement with" Chen et al. (2022), who found RRF stronger [1].
- **Does fusion help?** DPR's single-dataset model loses top-20 accuracy on two of five datasets when BM25 is added (Natural Questions and WebQuestions) [2]. Bruch and colleagues write that it is "increasingly clear" that hybrid search gives meaningful gains, especially out of domain [1].
- **Is it needed at scale?** A study of 20260729 finds BM25 the strongest scalable default among the paradigms it tests; its abstract does not evaluate hybrid retrieval separately, so its verdict on hybrids is **unstated** [7]. See the [graph-based RAG](../papers/graph-based-rag.md) papers.

## Related

[BM25](./bm25.md), [dense retrieval](./dense-retrieval.md), [reciprocal rank fusion](./reciprocal-rank-fusion.md), [reranking](./reranking.md), [approximate nearest neighbour](./approximate-nearest-neighbour.md), [retrieval-augmented generation](./retrieval-augmented-generation.md), [information retrieval](./information-retrieval.md); papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [The Web changes data and search](../history/the-web.md)

**Trends**

- [Graph features removed and added](../trends/features-in-and-out.md)

**Projects**

- [agent-memory (Tigerless Labs)](../projects/tigerless-agent-memory.md)
- [Basic Memory](../projects/basic-memory.md)
- [Claude-Mem](../projects/claude-mem.md)
- [code-review-graph](../projects/code-review-graph.md)
- [Dify](../projects/dify.md)
- [Graphiti](../projects/graphiti.md)
- [Neo4j LLM Knowledge Graph Builder](../projects/llm-graph-builder.md)
- [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md)
- [RAGFlow](../projects/ragflow.md)

**Experiments**

- [X3: Matched-cost comparison](../experiments/x3-matched-cost-comparison.md)

**Applied to Pinakes**

- [The Pinakes graph approach](../applied-to-pinakes/approach.md)

**Index**

- [Approximate nearest neighbour](approximate-nearest-neighbour.md)
- [BM25](bm25.md)
- [Dense retrieval](dense-retrieval.md)
- [Embedding](embedding.md)
- [HNSW](hnsw.md)
- [Information retrieval](information-retrieval.md)
- [Inverted index](inverted-index.md)
- [LLM wiki](llm-wiki.md)
- [Reciprocal rank fusion](reciprocal-rank-fusion.md)
- [Reranking](reranking.md)
- [Retrieval-augmented generation](retrieval-augmented-generation.md)
- [Stemming](stemming.md)
- [Vector search](vector-search.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2210.11934 : Bruch, Gai, Ingber, "An Analysis of Fusion Functions for Hybrid Retrieval", arXiv 2210.11934, v1 20221021, v2 20230504: definition, convex combination against RRF, disagreement with Chen et al., affiliations (Pinecone, UC Berkeley, internship note), quotes (abstract read 20261102 20:45 UTC; full text via https://ar5iv.labs.arxiv.org/html/2210.11934 read 20261102 20:56 UTC, author block re-read 20261102 21:22 UTC)
2. https://arxiv.org/abs/2004.04906 : Karpukhin et al., "Dense Passage Retrieval for Open-Domain Question Answering", EMNLP 2020, v1 20200410; BM25 plus DPR combination, lambda 1.1, Table 2 (abstract read 20261102 20:45 UTC; full text via https://ar5iv.labs.arxiv.org/html/2004.04906 read 20261102 20:56 UTC)
3. http://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf : Cormack, Clarke, Buettcher, "Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods", SIGIR 2009; the RRF formula with k = 60 (read 20261102 20:46 UTC)
4. https://arxiv.org/pdf/2312.10997 : Gao et al., RAG survey, section III-D1 "Mix/hybrid Retrieval" (read 20261102 20:56 UTC via https://ar5iv.labs.arxiv.org/html/2312.10997)
5. https://arxiv.org/html/2501.09136v4 : Singh et al., agentic RAG survey, version 4 dated 20260401, section 2.3.3 and Table 1 (read 20261102 20:54 UTC)
6. https://raw.githubusercontent.com/mem0ai/mem0/main/docs/changelog/sdk.mdx : Mem0 SDK changelog, v2.0.0 labelled 2026-04-14, hybrid search lines; first-party (read 20261102 20:55 UTC)
7. https://arxiv.org/abs/2607.26497 : Wang et al., "BM25 Wins at Scale", v1 20260729; abstract does not separately evaluate hybrid retrieval (read 20261102 20:46 UTC)
