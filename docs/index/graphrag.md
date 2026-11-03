---
type: index
kind: concept
aliases: [Graph RAG]
updated: 20261102 21:16 UTC
---

# GraphRAG

GraphRAG is retrieval-augmented generation that retrieves through a graph. The name began as Microsoft's method and is now also used for the whole family. This entry gives both meanings and the dated changes; the family is still moving and is told on the trend page.

## Definition

Edge et al. (Microsoft) propose GraphRAG as "a graph-based approach to question answering over private text corpora". A language model builds a graph index in two stages: first an entity knowledge graph from the source documents, then summaries for all groups of closely related entities (see [community report](./community-report.md)). At query time each summary yields a partial answer, and the partial answers are merged. The authors aim it at global questions about a whole corpus, which plain [retrieval-augmented generation](./retrieval-augmented-generation.md) "fails" on (first-party) [1].

## How it changed

- **20240424.** The paper appears on arXiv (v1; 10 authors) [1].
- **20240702.** Microsoft Research posts "GraphRAG is now available on GitHub" (first-party) [2]. See [Microsoft GraphRAG](../projects/microsoft-graphrag.md).
- **20240815.** Peng et al. survey the field and use the name for a framework that "leverages external structured knowledge graphs" to help models answer [3].
- **20241125.** Microsoft's LazyGraphRAG replaces model-based extraction with noun-phrase extraction and defers model use to query time; the authors claim indexing costs "identical to vector RAG and 0.1% of the costs of full GraphRAG" (first-party) [4].
- **20260814.** Microsoft puts its repository in maintenance mode [5][6]; the details are on the [Microsoft GraphRAG](../projects/microsoft-graphrag.md) page.

Later work is on the trend page [Graph-based RAG](../trends/graph-based-rag.md); the papers are in [that group](../papers/graph-based-rag.md).

## Where sources disagree

The scope of the name. Edge et al. build the graph from the user's documents with a model [1]. Peng et al. describe a retrieval process over a graph database that is identified or constructed for the task [3]. Microsoft's own LazyGraphRAG builds its index without model-based extraction yet keeps the name [4]. This documentation uses "GraphRAG" for the family and says "Microsoft GraphRAG" for the method.

## Related

Entries: [knowledge graph](./knowledge-graph.md), [retrieval-augmented generation](./retrieval-augmented-generation.md), [community detection](./community-detection.md), [community report](./community-report.md), [gleaning](./gleaning.md), [personalized PageRank](./personalized-pagerank.md), [large language model](./large-language-model.md). Pages: [Microsoft GraphRAG](../projects/microsoft-graphrag.md), [LightRAG](../projects/lightrag.md), [HippoRAG](../projects/hipporag.md), [neo4j-graphrag](../projects/neo4j-graphrag-python.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md)

**Projects**

- [FalkorDB](../projects/falkordb.md)
- [GraphRAG SDK](../projects/graphrag-sdk.md)
- [Memgraph](../projects/memgraph.md)
- [Microsoft GraphRAG](../projects/microsoft-graphrag.md)
- [RAGFlow](../projects/ragflow.md)

**Papers**

- [Papers: Agentic graph retrieval](../papers/learned-graph-traversal.md)

**Benchmarks**

- [2WikiMultiHopQA](../benchmarks/2wikimultihopqa.md)
- [Benchmarks](../benchmarks/README.md)
- [EnterpriseRAG-Bench](../benchmarks/enterpriserag-bench.md)
- [GraphRAG-Bench (Xiang)](../benchmarks/graphrag-bench-xiang.md)
- [GraphRAG-Bench (Xiao)](../benchmarks/graphrag-bench-xiao.md)
- [MultiHop-RAG](../benchmarks/multihop-rag.md)
- [Natural Questions](../benchmarks/natural-questions.md)
- [RAGSearch](../benchmarks/ragsearch.md)

**Experiments**

- [X3: Matched-cost comparison](../experiments/x3-matched-cost-comparison.md)

**Index**

- [Agent memory](agent-memory.md)
- [Chunking](chunking.md)
- [Community detection](community-detection.md)
- [Community report](community-report.md)
- [Gleaning](gleaning.md)
- [Hypergraph](hypergraph.md)
- [Knowledge compilation](knowledge-compilation.md)
- [Knowledge graph](knowledge-graph.md)
- [Multi-hop question answering](multi-hop-question-answering.md)
- [Named-entity recognition](named-entity-recognition.md)
- [PageRank](pagerank.md)
- [Personalized PageRank](personalized-pagerank.md)
- [Query-focused summarization](query-focused-summarization.md)
- [RAPTOR](raptor.md)
- [Retrieval-augmented generation](retrieval-augmented-generation.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/html/2404.16130v2 : Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization", abstract and introduction (v1 20240424, 10 authors; first-party; read 20261102 20:45 UTC)
2. https://www.microsoft.com/en-us/research/blog/graphrag-new-tool-for-complex-data-discovery-now-on-github/ : Edge, Trinh, Truitt, Larson, 20240702 (first-party; read 20261102 20:46 UTC)
3. https://arxiv.org/html/2408.08921 : Peng et al. (8 authors), "Graph Retrieval-Augmented Generation: A Survey", v1 20240815; section 4 (read 20261102 20:46 UTC)
4. https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ : Edge, Trinh, Larson, 20241125 (first-party; read 20261102 20:46 UTC)
5. https://github.com/microsoft/graphrag : README warning on maintenance mode (read 20261102 20:46 UTC)
6. https://github.com/microsoft/graphrag/commit/21f7bdf6bdbfec3617719528c42fb729c0c173cd : commit "Add notice." of 20260814 that adds the warning to the README (read 20261102 20:46 UTC)
