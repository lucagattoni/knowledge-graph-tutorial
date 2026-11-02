---
type: index
kind: concept
aliases: [graph clustering, community structure detection]
updated: 20261102 21:21 UTC
---

# Community detection

## Definition

Community detection groups the nodes of a graph into clusters, called communities, with many edges inside each cluster and comparatively few edges between clusters. Fortunato's review of the field describes community structure in exactly these terms and adds that the problem "is very hard and not yet satisfactorily solved" [1]. The idea was studied in network science, for example in social and biological networks [2]; where the word itself comes from is **unstated** in the sources read. In [GraphRAG](./graphrag.md)-style systems it splits a [knowledge graph](./knowledge-graph.md) built from documents into groups of related entities, each of which can then be summarised [3].

## How it changed

- 20011207: Girvan and Newman (PNAS, 2002) highlight community structure as a common property of networks and propose a method that uses centrality indices to find community boundaries [2].
- 20080304: Blondel and colleagues publish the Louvain method, a heuristic based on modularity optimisation, tested on a web graph of 118 million nodes [4].
- 20090603: Fortunato's survey (Physics Reports, 2010) gathers the methods [1].
- 20181019: Traag, Waltman and van Eck show that Louvain can give badly connected communities (up to 25% in their tests) and even disconnected ones (up to 16%), and introduce Leiden, which guarantees connected communities [5].
- 20240424: the GraphRAG paper applies Leiden "in a hierarchical manner", detecting sub-communities inside each community until the leaves cannot be split [3]. The project documentation calls the step the Hierarchical Leiden Algorithm [6].

In [retrieval-augmented generation](./retrieval-augmented-generation.md) the step belongs to one family of designs, which the trend [Graph-based RAG](../trends/graph-based-rag.md) compares with others; that line is still moving.

## Where sources disagree

On what a community is. Fortunato writes "No definition is universally accepted" and says the definition depends on the system and the application [1]. The GraphRAG paper says "a variety of community detection algorithms may be used" and cites Fortunato's survey [3]; the choice of Leiden is that pipeline's own. On Louvain: its authors report that it outperforms all other known methods in computation time [4], while a later study shows a defect in the communities it returns [5]. *Reading:* the two claims concern different properties (speed against connectedness), so they do not contradict each other.

## Related

[GraphRAG](./graphrag.md) · [community report](./community-report.md) · [knowledge graph](./knowledge-graph.md) · [personalized PageRank](./personalized-pagerank.md) · [code graph](./code-graph.md) · project [Microsoft GraphRAG](../projects/microsoft-graphrag.md) · project [Graphify](../projects/graphify.md) · trend [Graph-based RAG](../trends/graph-based-rag.md) · papers [Graph-based RAG](../papers/graph-based-rag.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Projects**

- [code-review-graph](../projects/code-review-graph.md)
- [codebase-memory-mcp](../projects/codebase-memory-mcp.md)
- [Graphify](../projects/graphify.md)
- [Hyper-Extract](../projects/hyper-extract.md)
- [LLM Wiki (nashsu)](../projects/llm-wiki-nashsu.md)
- [Microsoft GraphRAG](../projects/microsoft-graphrag.md)
- [Neo4j LLM Knowledge Graph Builder](../projects/llm-graph-builder.md)

**Papers**

- [Papers: Graph-based RAG](../papers/graph-based-rag.md)

**Applied to Pinakes**

- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Code graph](code-graph.md)
- [Community report](community-report.md)
- [GraphRAG](graphrag.md)
- [PageRank](pagerank.md)
- [Personalized PageRank](personalized-pagerank.md)
- [Query-focused summarization](query-focused-summarization.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/0906.0612 : Fortunato, "Community detection in graphs", Physics Reports 486, 2010, v1 20090603, abstract (read 20261102 20:45 UTC); "No definition is universally accepted" is in section III.B.1 of the full text, https://arxiv.org/pdf/0906.0612 (read 20261102 20:49 UTC)
2. https://arxiv.org/abs/cond-mat/0112110 : Girvan and Newman, PNAS 99, 7821-7826, 2002 (journal reference as listed by arXiv, which gives no month), v1 20011207, abstract (read 20261102 20:45 UTC; journal reference read 20261102 21:20 UTC)
3. https://arxiv.org/abs/2404.16130 : Edge and nine co-authors, "From Local to Global: A Graph RAG Approach to Query-Focused Summarization", v1 20240424; section 3.1.4, Leiden used hierarchically (full text, read 20261102 20:49 UTC)
4. https://arxiv.org/abs/0803.0476 : Blondel, Guillaume, Lambiotte, Lefebvre, "Fast unfolding of communities in large networks", J. Stat. Mech. 2008, v1 20080304, abstract (read 20261102 20:45 UTC)
5. https://arxiv.org/abs/1810.08473 : Traag, Waltman, van Eck, "From Louvain to Leiden", Scientific Reports 9, 2019, v1 20181019, abstract (read 20261102 20:45 UTC)
6. https://microsoft.github.io/graphrag/index/default_dataflow/ : "Hierarchical Leiden Algorithm", recursive clustering to a size threshold; the page gives no version or date (read 20261102 20:46 UTC)
