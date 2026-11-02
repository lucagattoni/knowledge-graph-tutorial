---
type: project
repo: neo4j/neo4j-graphrag-python
trends: [graph-based-rag, graph-query-generation]
updated: 20261102 23:17 UTC
---

# neo4j-graphrag-python

The official Python package from [Neo4j](./neo4j.md) for building [retrieval-augmented generation](../index/retrieval-augmented-generation.md) on a [graph database](../index/graph-database.md). This page says what the package contains, how its retrievers and graph builder work, what evidence exists, and how actively it is kept up. It belongs to two trends: it is a vendor library for graph-based RAG (retrieval-augmented generation), and it ships a named text-to-[Cypher](../index/cypher.md) retriever.

| Field | Value |
|---|---|
| Repository | https://github.com/neo4j/neo4j-graphrag-python [1] |
| Licence | Apache License 2.0, with parts under the Python Software Foundation (PSF) License Version 2. GitHub cannot classify it (the licence endpoint returns `NOASSERTION`, "Other"), and there is no file named `LICENSE` [1][2][15]. The licence file GitHub points to, `LICENSE.txt`, says: unless stated otherwise Apache 2.0 (full text in `LICENSE.APACHE2.txt`); parts under PSF v2 (`LICENSE.PYTHON.txt`), "marked as such" in the code [2][3]. Which files are PSF-covered: not located; a GitHub code search for the phrase finds only the two licence files, and such a search is not exhaustive [4]. `pyproject.toml` and PyPI say Apache License, Version 2.0 [5][6]. The README states no licence for the code [7]. |
| Trends | [Graph-based RAG](../trends/graph-based-rag.md), [Asking graphs in natural language](../trends/graph-query-generation.md) |

## What it is

The README calls it "the official Neo4j GraphRAG package for Python", a first-party library with long-term support from Neo4j [7]. The documentation says it continues the renamed `neo4j-genai` package, which is deprecated [8]. It supports Neo4j 5.18.1 or later, Aura 5.18.0 or later, and Neo4j 2026.01 or later for the Cypher `SEARCH` clause with in-index filtering [8]. Python 3.10 to 3.14 is supported [7].

It has two parts. The first holds retrievers and a `GraphRAG` class that combine a retriever with a [large language model](../index/large-language-model.md) (LLM) to answer from a Neo4j database [7][9]. The second is a [knowledge-graph](../index/knowledge-graph.md) builder pipeline in which an LLM extracts a graph from text, PDF or Markdown and writes it to Neo4j. The builder sits in the `experimental` namespace, which the README says may change without notice and is not recommended for production; it also needs the APOC core library [7]. `SimpleKGPipeline` itself still lives under `neo4j_graphrag.experimental.pipeline.kg_builder`, but its components are imported from `neo4j_graphrag.components` [14]. The 1.19.0 changelog entry ("Preparation for 2.0") says all components were moved out of `experimental`, that the old imports raise a deprecation warning, and that imports from the experimental namespace will be removed in 2.0 [12].

## How it works

The exported retrievers are `VectorRetriever`, `VectorCypherRetriever`, `HybridRetriever`, `HybridCypherRetriever`, `Text2CypherRetriever` and `ToolsRetriever`, plus retrievers that keep vectors in Weaviate, Pinecone or Qdrant and the graph in Neo4j [10]. The hybrid retrievers combine a [vector index](../index/vector-search.md) with a full-text index ([hybrid search](../index/hybrid-search.md)) [20]. The "Cypher" variants append a user-supplied Cypher query that can traverse the graph from each retrieved node [19][20].

`Text2CypherRetriever` asks an LLM to turn the question into Cypher, using a [schema](../index/schema.md) (passed in, or read from the database) and optional example pairs, then runs the query [11]. Since 1.16.0 it runs `EXPLAIN` first and refuses anything that is not read-only; the changelog gives prompt injection as the reason [12][11]. `ToolsRetriever` lets an LLM pick among retrievers wrapped as tools and returns the combined results [13].

For construction, `SimpleKGPipeline` wraps a customisable `Pipeline` of components: load, [split](../index/chunking.md) (fixed-size by default), [embed](../index/embedding.md), schema extraction, entity and relation extraction, pruning, entity resolution and writing [7][15]. The schema may be given, set to `FREE` (no guiding schema) or set to `EXTRACTED`, where the LLM extracts the schema [14][21]. When no schema is given, the LLM extracts one by default; the changelog says so for version 1.8.0 (published 20250703), and the current code describes `EXTRACTED` as "same as no schema" [22][23]. By default entities with the same label and name are merged, and a failed chunk is ignored [14]. A Parquet writer, added in 1.14.0, exports one file per node label and relationship type [12]. LLM providers include OpenAI, Anthropic, Gemini, Vertex AI, Cohere, Mistral, Bedrock and Ollama [7]. The repository file tree has no MCP (Model Context Protocol) module [15].

## Evidence

None published. The README, the documentation index page and the file tree contain no benchmark or evaluation: no path mentions one, and a GitHub code search for "benchmark" returned zero hits (not exhaustive) [7][8][15][16]. No third-party evaluation of this package was found. *Reading:* the package is infrastructure; its retrieval quality depends on the user's graph, prompts and LLM, and nothing in the sources measures it.

## Status and direction

The latest release is 1.23.0, published 20261028 10:40 UTC; the repository has 39 releases since 0.3.0 (20240702), 14 of them in 2026 [17]. Four came in the last 90 days: 1.19.0 (20260826), 1.21.0 (20260923), 1.22.0 (20261001) and 1.23.0 (20261028) [17]. The changelog has a 1.20.0 heading, but no 1.20.0 tag or release exists; its 1.21.0 heading is empty, although a 1.21.0 tag and release exist [12][17]. There are 103 commits on the default branch since 20260804, of which 48 come from the dependency bot `renovate[bot]` [18]. The repository is not archived [1].

Recent changelog entries cover pipeline observers (listed under the 1.20.0 heading; the release that first shipped them is unstated), lazy imports of provider modules (1.22.0), schema prompts that steer the LLM toward connected graphs (1.22.0), a rule that each node type is defined once (1.23.0), and Parquet export fixes [12]. The changelog's "Next" section adds an `embedding_model_name` property to embedders [12]. Breaking changes still land inside the experimental builder, for example in 1.15.0 and 1.18.0 [12]. *Reading:* the retrieval side is stable and the construction side is still being shaped.

A roadmap is unstated: no roadmap file exists in the file tree and the README gives none [7][15]. The one forward statement is in the 1.19.0 changelog entry: imports from the experimental namespace will be removed in 2.0, with no date given [12]. No statement of maintenance mode or of features moved to a hosted tier was found in the sources read.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)
- [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Neo4j](neo4j.md)
- [Neo4j LLM Knowledge Graph Builder](llm-graph-builder.md)
- [Projects](README.md)

**Index**

- [Cypher](../index/cypher.md)
- [GraphRAG](../index/graphrag.md)
- [Schema](../index/schema.md)
- [Schema induction](../index/schema-induction.md)
- [Text-to-query](../index/text-to-query.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/neo4j/neo4j-graphrag-python : repository metadata and licence classification via the GitHub API; not archived (read 20261102 20:09 UTC)
2. https://github.com/neo4j/neo4j-graphrag-python/blob/main/LICENSE.txt : the licence statement, 423 bytes; the licence endpoint names this file; no file named `LICENSE` in the tree (read 20261102 20:09 UTC)
3. https://github.com/neo4j/neo4j-graphrag-python/blob/main/LICENSE.APACHE2.txt and https://github.com/neo4j/neo4j-graphrag-python/blob/main/LICENSE.PYTHON.txt : Apache 2.0 text and PSF text (read 20261102 20:12 UTC)
4. https://github.com/neo4j/neo4j-graphrag-python : GitHub code search for "Python Software Foundation" (two licence files) (read 20261102 20:14 UTC)
5. https://github.com/neo4j/neo4j-graphrag-python/blob/main/pyproject.toml : version 1.23.0, licence text (read 20261102 20:12 UTC)
6. https://pypi.org/pypi/neo4j-graphrag/json : version 1.23.0, licence field (read 20261102 20:13 UTC)
7. https://github.com/neo4j/neo4j-graphrag-python/blob/main/README.md : description, extras, experimental namespace, APOC requirement, providers (read 20261102 20:09 UTC)
8. https://neo4j.com/docs/neo4j-graphrag-python/current/ : renamed continuation of neo4j-genai, supported Neo4j versions (read 20261102 20:13 UTC)
9. https://github.com/neo4j/neo4j-graphrag-python/blob/main/src/neo4j_graphrag/generation/graphrag.py : `GraphRAG` class (read 20261102 20:12 UTC)
10. https://github.com/neo4j/neo4j-graphrag-python/blob/main/src/neo4j_graphrag/retrievers/__init__.py : exported retrievers (read 20261102 20:12 UTC)
11. https://github.com/neo4j/neo4j-graphrag-python/blob/main/src/neo4j_graphrag/retrievers/text2cypher.py : LLM-to-Cypher flow, `EXPLAIN` read-only check (read 20261102 20:12 UTC)
12. https://github.com/neo4j/neo4j-graphrag-python/blob/main/CHANGELOG.md : entries from 1.14.0 to 1.23.0, the unreleased section, the empty 1.21.0 heading, the 1.20.0 observer entry, the 1.19.0 "Preparation for 2.0" entry (read 20261102 20:12 and 20:33 UTC)
13. https://github.com/neo4j/neo4j-graphrag-python/blob/main/src/neo4j_graphrag/retrievers/tools_retriever.py : tool-selecting retriever (read 20261102 20:12 UTC)
14. https://github.com/neo4j/neo4j-graphrag-python/blob/main/src/neo4j_graphrag/experimental/pipeline/kg_builder.py : `SimpleKGPipeline` arguments and defaults; its imports of components come from `neo4j_graphrag.components` (read 20261102 20:12 and 20:33 UTC)
15. https://github.com/neo4j/neo4j-graphrag-python/tree/main : file tree of 458 files; no path with "mcp", "bench" or "roadmap" (read 20261102 20:13 UTC)
16. https://github.com/neo4j/neo4j-graphrag-python : GitHub code search for "benchmark": zero results (read 20261102 20:13 UTC)
17. https://github.com/neo4j/neo4j-graphrag-python/releases : 39 releases; no 1.20.0 tag; the tags and releases lists name 1.19.0, 1.21.0, 1.22.0 and 1.23.0 (read 20261102 20:09, 20:13 and 20:33 UTC)
18. https://github.com/neo4j/neo4j-graphrag-python/commits/main : 103 commits since 20260804, authors (read 20261102 20:13 UTC)
19. https://github.com/neo4j/neo4j-graphrag-python/blob/main/src/neo4j_graphrag/retrievers/vector.py : `VectorCypherRetriever` appends a retrieval query for graph traversal (read 20261102 20:16 UTC)
20. https://github.com/neo4j/neo4j-graphrag-python/blob/main/src/neo4j_graphrag/retrievers/hybrid.py : vector plus full-text retrieval; `HybridCypherRetriever` (read 20261102 20:16 UTC)
21. https://github.com/neo4j/neo4j-graphrag-python/blob/main/src/neo4j_graphrag/experimental/pipeline/config/template_pipeline/simple_kg_builder.py : meaning of `FREE` and `EXTRACTED` (read 20261102 20:16 UTC)
22. https://github.com/neo4j/neo4j-graphrag-python/blob/main/CHANGELOG.md : 1.8.0 (release published 2025-07-03 15:05 UTC through the GitHub API): "when the user provides no schema, the automatic schema extraction is enabled by default" (read 20261102 22:24 UTC)
23. https://github.com/neo4j/neo4j-graphrag-python/blob/main/src/neo4j_graphrag/experimental/pipeline/config/template_pipeline/simple_kg_builder.py : `EXTRACTED` is "same as no schema, schema will be extracted by LLM" (read 20261102 22:30 UTC)
