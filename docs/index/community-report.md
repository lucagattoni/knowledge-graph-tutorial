---
type: index
kind: concept
aliases: [community summary]
updated: 20261102 21:21 UTC
---

# Community report

## Definition

A community report is a summary, written by a language model, of one community (a cluster of closely related entities) in a graph built from documents. The GraphRAG paper introduced the idea under the name "community summaries": the model first derives an entity graph from the source documents and then pre-generates summaries for all groups of closely related entities [1]. The project documentation calls the same objects community reports and says they "contain an executive overview" and refer to the key entities, relationships and claims of the community [2]. A community comes from [community detection](./community-detection.md).

## How it changed

- 20240424: the GraphRAG paper (first version) builds the summaries bottom-up along the community hierarchy. At query time each summary yields a partial answer, and the partial answers are combined into a final one (map-reduce) [1]. The paper adds that a user can also scan the summaries at one level without any query [1].
- Undated in the documentation: the report text is embedded by default and the reports are exported as their own table [2]. Global search takes the reports of a chosen level, splits them into chunks, rates the points in each chunk and merges the most important ones; lower levels give more detail and cost more time and model calls [3].
- Undated in the documentation: the cheaper Fast method still makes the reports with the model, but builds them from the source text units, not from model-written entity descriptions [4].

Designs that skip the reports are compared in the trend [Graph-based RAG](../trends/graph-based-rag.md); the step is not settled practice.

## Where sources disagree

No disagreement found in the sources read. Only the name differs: "community summaries" in the paper [1], "community reports" in the documentation [2]. The paper itself describes them as "report-like summaries" [1].

## Related

[community detection](./community-detection.md) · [GraphRAG](./graphrag.md) · [knowledge graph](./knowledge-graph.md) · [retrieval-augmented generation](./retrieval-augmented-generation.md) · [large language model](./large-language-model.md) · [context window](./context-window.md) · [embedding](./embedding.md) · project [Microsoft GraphRAG](../projects/microsoft-graphrag.md) · project [LightRAG](../projects/lightrag.md) · trend [Graph-based RAG](../trends/graph-based-rag.md) · papers [Graph-based RAG](../papers/graph-based-rag.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md)

**Experiments**

- [X2: the index cost of cheap graph builders](../experiments/x2-index-cost.md)

**Index**

- [Community detection](community-detection.md)
- [GraphRAG](graphrag.md)
- [Query-focused summarization](query-focused-summarization.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2404.16130 : Edge and nine co-authors, "From Local to Global: A Graph RAG Approach to Query-Focused Summarization", v1 20240424, v2 20250219; abstract (read 20261102 20:45 UTC) and full text, sections 3.1.5 and 3.1.6, "report-like summaries" (read 20261102 20:49 UTC); the sentence on scanning summaries without a query was re-read in the v2 full text (arXiv:2404.16130v2, 19 Feb 2025) on 20261102 21:20 UTC, and the bullet's date is that of v1, whose text was not compared
2. https://microsoft.github.io/graphrag/index/default_dataflow/ : community reports phase, "executive overview", embedding by default; the page gives no version or date, footer "2025" (read 20261102 20:46 UTC, via a fetch-tool extraction)
3. https://microsoft.github.io/graphrag/query/global_search/ : global search over community reports, map and reduce, hierarchy level (read 20261102 20:46 UTC, via a fetch-tool extraction)
4. https://microsoft.github.io/graphrag/index/methods/ : Standard against Fast method; Fast builds reports from text units (read 20261102 20:50 UTC, via a fetch-tool extraction)
