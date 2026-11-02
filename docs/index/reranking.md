---
type: index
kind: concept
aliases: [re-ranking, second-stage ranking]
updated: 20261102 21:31 UTC
---

# Reranking

This entry answers what reranking is, when neural rerankers began to lead search benchmarks, and what it costs. It also records the 2023 finding that instructed language models can rerank, and a 2026 baseline that includes a reranker.

## Definition

In a multi-stage ranking architecture an initial retrieval stage selects candidate documents and each later stage re-ranks the candidates passed along from the one before; that reordering is reranking [1]. Nogueira and colleagues add that increasingly richer models become practical when they see successively smaller candidate sets [1]. The same paper (20191031) shows the design: a pointwise model (monoBERT) and a pairwise model (duoBERT) are "arranged in a multi-stage ranking architecture", and the system can "trade off quality against latency by controlling the admission of candidates into each pipeline stage" [1]. Lin, Nogueira and Yates organise their survey around two categories: "transformer models that perform reranking in multi-stage architectures" and "dense retrieval techniques that perform ranking directly" [2].

## How it changed

- **20190113.** Nogueira and Cho re-rank passages with [BERT](./bert.md); the system reaches the top of the MS MARCO passage leaderboard, a 27% relative gain in MRR@10, and is state of the art on TREC-CAR (first-party) [3]. See [MS MARCO](../benchmarks/ms-marco.md). Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20201013.** Lin and colleagues split transformer text ranking into reranking and dense retrieval [2].
- **20210417.** BEIR reports that "re-ranking and late-interaction-based models on average achieve the best zero-shot performances", "at high computational costs"; BM25 stays "a robust baseline" [4]. See [BEIR](../benchmarks/beir.md).
- **20230419.** Sun and seven co-authors find that "properly instructed LLMs can deliver competitive, even superior results" against state-of-the-art supervised methods on common benchmarks, and distil a 440M model that beats a 3B supervised one on BEIR (first-party) [5].
- **20261022.** Bao and five co-authors report that their own naive baseline, dense retrieval plus reranking over raw history, ranks first among compared memory systems in six of seven benchmark-model settings (first-party); the abstract does not isolate reranking's part [6]. See [agent memory](../trends/agent-memory.md); still moving.

## Where sources disagree

**Is a second stage worth its cost?** BEIR finds rerankers best on average zero-shot but costly, while dense and sparse retrievers are cheaper and "often underperform" [4]. Lin and colleagues treat direct dense ranking as a parallel route, not a stage [2]. How much reranking adds in memory systems is **unstated** in the 2026 abstract [6].

## Related

[information retrieval](./information-retrieval.md) · [BM25](./bm25.md) · [dense retrieval](./dense-retrieval.md) · [hybrid search](./hybrid-search.md) · [reciprocal rank fusion](./reciprocal-rank-fusion.md) · [learning to rank](./learning-to-rank.md) · [BERT](./bert.md) · [retrieval-augmented generation](./retrieval-augmented-generation.md) · [large language model](./large-language-model.md) · projects: [Hindsight](../projects/hindsight.md), [Graphiti](../projects/graphiti.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Language models meet retrieval (2018-2022)](../history/language-models-meet-retrieval.md)

**Trends**

- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)
- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Projects**

- [claude-obsidian](../projects/claude-obsidian.md)
- [Dify](../projects/dify.md)
- [GraphRAG SDK](../projects/graphrag-sdk.md)
- [Hindsight](../projects/hindsight.md)
- [Mem0](../projects/mem0.md)
- [OpenViking](../projects/openviking.md)
- [RAGFlow](../projects/ragflow.md)

**Benchmarks**

- [BEIR](../benchmarks/beir.md)
- [MultiHop-RAG](../benchmarks/multihop-rag.md)
- [STaRK](../benchmarks/stark.md)

**Experiments**

- [X3: Matched-cost comparison](../experiments/x3-matched-cost-comparison.md)

**Applied to Pinakes**

- [Applied to Pinakes](../applied-to-pinakes/README.md)
- [Measurements](../applied-to-pinakes/measurements.md)
- [What Pinakes should measure next](../applied-to-pinakes/next.md)
- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Approximate nearest neighbour](approximate-nearest-neighbour.md)
- [AUROC](auroc.md)
- [BERT](bert.md)
- [BM25](bm25.md)
- [Dense retrieval](dense-retrieval.md)
- [Hybrid search](hybrid-search.md)
- [Learning to rank](learning-to-rank.md)
- [Mean reciprocal rank](mean-reciprocal-rank.md)
- [Ranked retrieval](ranked-retrieval.md)
- [Reciprocal rank fusion](reciprocal-rank-fusion.md)
- [Relevance feedback](relevance-feedback.md)
- [Retrieval-augmented generation](retrieval-augmented-generation.md)
- [Transformer](transformer.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/1910.14424 : Nogueira, Yang, Cho, Lin, "Multi-Stage Document Ranking with BERT", v1 20191031: abstract and Section 2 (staged re-ranking, richer models on smaller candidate sets), monoBERT, duoBERT, quality-latency control (abstract read 20261102 21:05 UTC; full text via https://arxiv.org/pdf/1910.14424 read 20261102 21:26 UTC)
2. https://arxiv.org/abs/2010.06467 : Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking: BERT and Beyond", v1 20201013: abstract, the two categories (read 20261102 21:05 UTC)
3. https://arxiv.org/abs/1901.04085 : Nogueira and Cho, "Passage Re-ranking with BERT", v1 20190113: abstract, MS MARCO and TREC-CAR results (read 20261102 21:05 UTC)
4. https://arxiv.org/abs/2104.08663 : Thakur et al., "BEIR", v1 20210417: abstract (read 20261102 21:05 UTC)
5. https://arxiv.org/abs/2304.09542 : Sun et al., "Is ChatGPT Good at Search? Investigating Large Language Models as Re-Ranking Agents", v1 20230419: abstract (read 20261102 21:05 UTC)
6. https://arxiv.org/abs/2610.30755 : Bao et al., "Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought", v1 20261022: abstract (read 20261102 21:05 UTC; re-read 20261102 21:27 UTC)
