---
type: index
kind: concept
aliases: [RRF, rank fusion]
updated: 20261102 21:30 UTC
---

# Reciprocal rank fusion

This entry answers what reciprocal rank fusion is, where it came from, and whether its fixed constant is safe. It also dates its adoption in search products and records a 2026 project that moved away from it.

## Definition

Cormack, Clarke and Büttcher introduced Reciprocal Rank Fusion (RRF) as "a simple method for combining the document rankings from multiple IR systems" [1]. Each document scores the sum, over all input rankings, of 1 / (k + rank), where rank is its position in that ranking; documents are then sorted by the sum [1]. The authors fixed k = 60 "during a pilot investigation" and did not change it afterwards [1]. Only positions are used, never the scores the systems gave, and no list is weighted [1]. They say the constant "mitigates the impact of high rankings by outlier systems" [1].

## How it changed

- **2009.** Cormack and colleagues publish RRF at SIGIR. They report that it beat any individual system and Condorcet Fuse on combined TREC runs, and that an RRF meta-learner ranked the LETOR 3 dataset "better than any previously reported method" (first-party) [1]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **20221021.** Bruch, Gai and Ingber find RRF "sensitive to its parameters" and a convex combination of scores better, in and out of domain [2]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20230525.** Elastic's announcement of Elasticsearch 8.8 offers RRF as "excellent zero shot blending of ranking methods" (first-party, a vendor describing its own feature) [3]; its reference page gives a default constant of 60 [4]. This date falls in [What has settled since 2023](../history/settled-since-2023.md).
- **20260307.** Basic Memory v0.19.0 lists "Score-based fusion replacing RRF for better ranking" in its changelog (first-party) [5].

## Where sources disagree

**Is RRF robust?** Cormack and colleagues kept k = 60 and found RRF "consistently" at least as good as the other methods they tried; their pilot found k = 60 "near-optimal" but "not critical" [1]. Bruch and colleagues report that "NDCG swings wildly" with its parameters, that a tuned RRF "generalizes poorly" out of domain, and that this contradicts Chen et al., who found RRF "better and more reliably" than a convex combination [2]. The inputs differ: several retrieval systems in Cormack's case, lexical and semantic rankings in Bruch's [1][2].

## Related

[hybrid search](./hybrid-search.md) · [BM25](./bm25.md) · [vector search](./vector-search.md) · [reranking](./reranking.md) · [learning to rank](./learning-to-rank.md) · [personalized PageRank](./personalized-pagerank.md) · projects: [Graphiti](../projects/graphiti.md), [Hindsight](../projects/hindsight.md), [LLM Wiki (nashsu)](../projects/llm-wiki-nashsu.md), [Tigerless Agent Memory](../projects/tigerless-agent-memory.md), [Basic Memory](../projects/basic-memory.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Projects**

- [Hindsight](../projects/hindsight.md)

**Applied to Pinakes**

- [Measurements](../applied-to-pinakes/measurements.md)
- [The Pinakes graph approach](../applied-to-pinakes/approach.md)
- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Hybrid search](hybrid-search.md)
- [Mean reciprocal rank](mean-reciprocal-rank.md)
- [Reranking](reranking.md)

<!-- END GENERATED: appears-in -->

## Sources

1. http://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf : Cormack, Clarke, Büttcher, "Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods", SIGIR'09, Boston, July 2009: abstract, formula, k = 60, role of k (read 20261102 20:56 UTC; passage on k re-read 20261102 21:26 UTC)
2. https://arxiv.org/abs/2210.11934 : Bruch, Gai, Ingber, "An Analysis of Fusion Functions for Hybrid Retrieval", v1 20221021: RRF sensitive to parameters, convex combination better, disagreement with Chen et al. (abstract read 20261102 20:56 UTC; full text via https://ar5iv.labs.arxiv.org/html/2210.11934 read 20261102 21:06 UTC)
3. https://www.elastic.co/blog/whats-new-elasticsearch-8-8-0 : Elastic, "What's new in Elasticsearch 8.8.0", post dated 20230525: RRF as zero-shot blending (read 20261102 20:57 UTC)
4. https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion : Elastic reference: RRF description and `rank_constant` default 60 (read 20261102 20:57 UTC)
5. https://raw.githubusercontent.com/basicmachines-co/basic-memory/main/CHANGELOG.md : Basic Memory changelog, v0.19.0 (2026-03-07): "Score-based fusion replacing RRF for better ranking" (read 20261102 20:58 UTC)
