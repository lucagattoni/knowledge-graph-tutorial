---
type: project
repo: run-llama/llama_index
trends: [infrastructure-and-mcp]
updated: 20261102 23:17 UTC
---

# LlamaIndex

This page answers what LlamaIndex is, how its property graph index builds and queries a graph, whether any results are published, and how much the project still invests in the framework. LlamaIndex is a general [RAG](../index/retrieval-augmented-generation.md) (retrieval-augmented generation) and [agent](../index/agent.md) framework in which the graph is one optional index. The watch-list table on the chapter landing carries its stars and push dates.

| Field | Value |
|---|---|
| Repository | https://github.com/run-llama/llama_index |
| Licence | MIT. GitHub's licence endpoint classifies the `LICENSE` file as MIT; the file reads "The MIT License" and "Copyright (c) Jerry Liu" [1][2]. The licences of the 300-plus integration packages were not checked: **unstated**. |
| Trends | [Infrastructure and MCP](../trends/infrastructure-and-mcp.md) |

## What it is

The README calls LlamaIndex "an open-source framework to build agentic applications", published by the company behind LlamaParse [3]. It lists data connectors, ways to "structure your data (indices, graphs)" and a retrieval and query interface. A starter package, `llama-index`, bundles the core with some integrations; `llama-index-core` plus chosen integration packages is the other route, from a pool the README puts at over 300 [3]. The GitHub description now reads "LlamaIndex is the document processing platform for AI" [1].

The graph part is the `PropertyGraphIndex`: a labelled [property graph](../index/property-graph.md) built from the documents and used for retrieval beside the usual [vector](../index/vector-search.md) index [4].

## How it works

**Construction.** A list of `kg_extractors` runs over each [chunk](../index/chunking.md) and attaches entities and relations to the node. The defaults are `SimpleLLMPathExtractor`, where a [language model](../index/large-language-model.md) returns single-hop (entity, relation, entity) paths, and `ImplicitPathExtractor`, which needs no model because it reads relationships already on the nodes. `DynamicLLMPathExtractor` takes optional allowed types as guidance; `SchemaLLMPathExtractor` follows a strict schema [4].

**Retrieval.** Sub-retrievers can be combined. The defaults are `LLMSynonymRetriever`, where a model proposes keywords and synonyms, and `VectorContextRetriever`, which matches embedded graph nodes and follows relations to a set depth. Optional ones are `TextToCypherRetriever`, where a model writes a [Cypher](../index/cypher.md) query from the graph schema, and `CypherTemplateRetriever`, where a model fills the parameters of a template you write [4]. The guide warns that "Executing arbitrary cypher has its risks" [4]. No community summaries and no graph algorithms appear in the guide [4].

**Storage.** The default store is in memory, persists to disk and cannot run Cypher. Stores for [Neo4j](./neo4j.md), Nebula, TiDB and [FalkorDB](./falkordb.md) are listed; Neo4j, TiDB and FalkorDB support embeddings natively [4].

**Agents and MCP (Model Context Protocol).** The `llama-index-tools-mcp` package lets an agent call tools of a [Model Context Protocol](../index/model-context-protocol.md) server, including servers such as [MCP reference servers](./mcp-servers.md). Its client speaks Streamable HTTP, SSE (Server-Sent Events) and stdio, supports OAuth, and can turn a LlamaIndex `Workflow` into an MCP app [5].

*Reading:* the graph here is a toolkit, not a design. You choose extractors, retrievers and a store. Projects built around the graph, for example [LightRAG](./lightrag.md) and [Microsoft GraphRAG](./microsoft-graphrag.md), have pages of their own; this one cannot be judged as a single method.

## Evidence

None published for the property graph index. The guide and the README contain no benchmark, and the guide only links an example notebook called "Comparing KG Extractors", which was not read [3][4]. The README names two benchmarks of the company's own, ParseBench and ExtractBench, for parsing and extraction (first-party); they do not test graph retrieval [3]. Third-party evaluations were not fetched: **unstated**.

## Status and direction

- **Focus.** A README note says the "current focus" is document parsing and extraction, that LlamaParse is the "enterprise platform", and that "our primary focus has shifted towards LlamaParse, along with liteparse and our benchmarking efforts". The framework stays "available as an open toolkit" [3]. LlamaParse asks readers to sign up and get an API key, which suggests a hosted service (an inference from the sign-up text); its Index product covers ingest and RAG pipelines [3]. The README does not use the words "maintenance mode".
- **Latest release.** v0.14.25, 20260921. Earlier: v0.14.24 on 20260819, v0.14.23 on 20260624, v0.14.22 on 20260514 [6]. No release since, 42 days at reading time.
- **Activity, 20260804 to 20261102.** 88 commits on `main`: 44 in August (from the 4th), 33 in September, 11 in October [7]. The newest is 20261014. All ten newest commit subjects read concern model-provider integrations, dependency bounds or documentation; none touches the property graph code [7]. Open: 833 pull requests and 353 issues [10]. Not archived [1].
- **Property graph code.** The newest change to the `property_graph` package and to the guide is 20260720, an option to raise on model API errors in the LLM (large language model) extractors [8][9].
- **Direction.** Roadmap: **unstated**.

*Reading:* the repository is active but its activity is integration upkeep, and the company says its attention is on the hosted parsing platform. The graph index last changed in July, so it looks maintained but is not where the work goes.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Language models meet retrieval (2018-2022)](../history/language-models-meet-retrieval.md)

**Trends**

- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [FalkorDB](falkordb.md)
- [Projects](README.md)

**Index**

- [Property graph](../index/property-graph.md)
- [Retrieval-augmented generation](../index/retrieval-augmented-generation.md)
- [Tree index](../index/tree-index.md)

<!-- END GENERATED: appears-in -->

## Sources

No paper is cited; the README gives only a software citation. The papers chapter group page for the main trend is [Infrastructure and MCP papers](../papers/README.md).

1. https://api.github.com/repos/run-llama/llama_index : description, licence field (MIT), archived flag (false), created 20221102; licence endpoint (read 20261102 20:19 UTC)
2. https://github.com/run-llama/llama_index/blob/main/LICENSE : MIT licence text, whole file (read 20261102 20:20 UTC)
3. https://github.com/run-llama/llama_index/blob/main/README.md : self-description, focus note, LlamaParse, integrations, benchmarks named (read 20261102 20:20 UTC)
4. https://github.com/run-llama/llama_index/blob/main/docs/src/content/docs/framework/module_guides/indexing/lpg_index_guide.md : property graph index guide (extractors, retrievers, stores, warning), read in full (read 20261102 20:20 UTC)
5. https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/tools/llama-index-tools-mcp/README.md : MCP tool spec, client transports, OAuth, `workflow_as_mcp` (read 20261102 20:20 UTC)
6. https://github.com/run-llama/llama_index/releases : release tags and dates, v0.14.25 latest (read 20261102 20:21 UTC)
7. https://github.com/run-llama/llama_index/commits/main : commits since 20260804 counted by month, ten newest subjects, via the commits API (read 20261102 20:21 UTC)
8. https://github.com/run-llama/llama_index/commits/main/docs/src/content/docs/framework/module_guides/indexing/lpg_index_guide.md : history of the property graph guide (read 20261102 20:21 UTC)
9. https://github.com/run-llama/llama_index/commits/main/llama-index-core/llama_index/core/indices/property_graph : history of the property graph package (read 20261102 20:21 UTC)
10. https://github.com/run-llama/llama_index/issues : open pull request and issue counts via the search API (read 20261102 20:21 UTC)
