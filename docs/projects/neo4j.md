---
type: project
repo: neo4j/neo4j
trends: [infrastructure-and-mcp]
updated: 20261102 23:17 UTC
---

# Neo4j

A [graph database](../index/graph-database.md) that other knowledge-graph tools can use as a backend. This page covers only the open-source Community Edition in the repository: what it stores, which retrieval features matter for LLM (large language model) work, where the free and paid editions differ, and how often it ships. It sits in the infrastructure trend, not in a retrieval trend: it is a layer other tools build on.

| Field | Value |
|---|---|
| Repository | https://github.com/neo4j/neo4j [1] |
| Licence | GPL-3.0, from `LICENSE.txt` on the default branch: the GNU General Public License version 3 text of 29 June 2007, 675 lines, with no Neo4j-specific terms found by a text search [2]. GitHub classifies it GPL-3.0 [1]. The README states the scope: Community Edition is "licensed under GPLv3"; Enterprise Edition "includes additional closed-source components not available in this repository" [3]. A GPL project is a read-only reference here: ideas and results only. |
| Trends | [Infrastructure and MCP](../trends/infrastructure-and-mcp.md) |

## What it is

Neo4j is a database written in Java [1]. The README says the programmer "works with a flexible network structure of nodes and relationships rather than static tables", with ACID (atomicity, consistency, isolation and durability) transactions and a query language [3]. Data form a [property graph](../index/property-graph.md), and the language is [Cypher](../index/cypher.md), which the manual says "was created in 2011 by Neo4j engineers" [8]. The repository was created in 2012 [1].

The repository holds the Community Edition. Enterprise Edition adds closed-source components; the operations manual lists backups, clustering, failover and role-based access control as Enterprise features, and describes Community as a single-instance edition [3][9]. Aura is the fully managed service [3].

## How it works

Two retrieval features matter for [retrieval-augmented generation](../index/retrieval-augmented-generation.md) and agent memory.

**Vector indexes.** The manual says the index uses Lucene's HNSW (hierarchical navigable small world) graph, an [approximate-nearest-neighbour](../index/approximate-nearest-neighbour.md) structure; similarity is cosine (default) or euclidean; dimensions run from 1 to 4096 [4]. The client supplies the [embeddings](../index/embedding.md) [4]. A Cypher `SEARCH` clause is the preferred way to query them from Neo4j 2026.01 [4]. A quantization-type setting was introduced in 2026.06, when the older on/off setting was deprecated; binary became the default from 2026.08, and the manual says the default "was 'scalar'" before that [4]. One limit separates the editions: Community can index embeddings kept as list properties, while the manual says storing them as native `VECTOR` properties "requires block format, which is available in Enterprise Edition and Aura" [4].

**Full-text indexes.** They run on Apache Lucene and return a relevance score [5]. The `SEARCH` clause for them was introduced in 2026.09 (Cypher 25 only) and is the preferred way to query them from that version; the older procedures are deprecated in Cypher 25 as of 2026.10 [5]. Neo4j's own Python package for GraphRAG is a separate project: [neo4j-graphrag-python](./neo4j-graphrag-python.md).

**Agents.** An official MCP server (a separate repository, `neo4j/mcp`, latest release v2.0.0 on 20261028) gets the graph schema, runs read and write Cypher and, with a plugin, graph algorithms, over stdio or HTTP [6][7]. The [Model Context Protocol](../index/model-context-protocol.md) page of Neo4j's developer site also lists Labs servers, among them a memory server that "stores and updates entities with observations and relationships" [6]. A module in this repository, `genai-plugin`, builds a JAR that adds GenAI functions and procedures [10]. Other projects use Neo4j as a backend, for example [Code-Graph-RAG](./code-graph-rag.md), where it is an opt-in alternative to an embedded store [11].

## Evidence

None published. The README makes one first-party claim, with no source or measurement: "For many applications, Neo4j offers orders of magnitude performance benefits compared to relational DBs" [3]. No benchmark of the vector or full-text features appears in the repository README or the two manual pages read [3][4][5]. No third-party evaluation was sought for this page. *Reading:* for a knowledge-graph builder the database is a dependency whose retrieval quality is set by the embeddings, prompts and queries on top of it; the sources here measure nothing about that.

## Status and direction

Versions are calendar-based. The newest tags read are 2026.10.1 (commit dated 20261020), 2026.10.0 (20261009), 2026.09.0 (20260914), 2026.08.1 (20260907) and 2026.08.0 (20260820) [12]. The API lists 15 tags whose names start with 2026 [12]. The repository's GitHub Releases are not used for this: the latest-release call returns 3.2.0-alpha08 of 20170411, and none of the 72 releases listed is dated 2026 [12]. The default branch is named `2026.10` [1]. Commit counts and push dates belong to the watch-list table, not to this page.

Commit subjects on the default branch since 20260804 include dependency bumps, fixes for CVEs (two commits, eight distinct identifiers in their subjects), a Cypher-injection fix in an administration command, a checkpoint fix in the index tree (GBPTree) and a tracer for concurrent transactions [13].

*Reading:* the project is not in maintenance mode on the evidence read: the manual pages show features added in 2026.01, 2026.06, 2026.07, 2026.08 and 2026.09 [4][5]. Whether features were moved from Community to Enterprise or Aura is unstated; the one visible split is native `VECTOR` storage [4]. A roadmap is unstated: none appears in the README or the manual pages read [3][4][5].

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [The semantic web and linked data](../history/semantic-web.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Trends**

- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)
- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Code-Graph-RAG](code-graph-rag.md)
- [FalkorDB](falkordb.md)
- [Graphiti](graphiti.md)
- [LightRAG](lightrag.md)
- [LlamaIndex](llama-index.md)
- [Mem0](mem0.md)
- [Memgraph](memgraph.md)
- [MemOS](memos.md)
- [Neo4j LLM Knowledge Graph Builder](llm-graph-builder.md)
- [neo4j-graphrag-python](neo4j-graphrag-python.md)
- [Projects](README.md)

**Benchmarks**

- [Text2Cypher](../benchmarks/text2cypher.md)

**Index**

- [ACID](../index/acid.md)
- [Approximate nearest neighbour](../index/approximate-nearest-neighbour.md)
- [CODASYL](../index/codasyl.md)
- [Cypher](../index/cypher.md)
- [Graph database](../index/graph-database.md)
- [HNSW](../index/hnsw.md)
- [Model Context Protocol](../index/model-context-protocol.md)
- [NoSQL](../index/nosql.md)
- [Property graph](../index/property-graph.md)
- [Triple store](../index/triple-store.md)
- [Vector search](../index/vector-search.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/neo4j/neo4j : repository metadata and licence classification through the GitHub API; language Java; default branch `2026.10`; not archived; created 20121112 (read 20261102 20:37 UTC)
2. https://github.com/neo4j/neo4j/blob/2026.10/LICENSE.txt : GPLv3 text, 675 lines; text search for "Commons Clause" and "neo4j" found nothing (read 20261102 20:19 UTC)
3. https://github.com/neo4j/neo4j/blob/2026.10/README.asciidoc : description, editions, Aura, licensing, the performance claim (read 20261102 20:18 UTC)
4. https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/ : algorithm, similarity, dimensions, `SEARCH` and quantization versions, binary default from 2026.08, edition note (read 20261102 20:38 UTC; downloaded page, tags stripped, text searched directly)
5. https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/full-text-indexes/ : Lucene, relevance score, `SEARCH` introduced in 2026.09 and preferred from then, deprecation in 2026.10 (read 20261102 20:38 UTC; same method)
6. https://neo4j.com/developer/genai-ecosystem/model-context-protocol-mcp/ : official MCP server, Labs servers (read 20261102 20:20 UTC; same method)
7. https://github.com/neo4j/mcp : repository `neo4j/mcp` and its latest release v2.0.0, published 20261028 16:21 UTC, through the API; GitHub cannot classify its licence (`NOASSERTION`) and its `LICENSE.txt` opens with a notice about mixed licences, so its licence is not stated here (read 20261102 20:20 UTC)
8. https://neo4j.com/docs/cypher-manual/current/introduction/cypher-overview/ : Cypher created in 2011 by Neo4j engineers (read 20261102 20:21 UTC; same method as 4)
9. https://neo4j.com/docs/operations-manual/current/introduction/ : Community and Enterprise features (read 20261102 20:21 UTC; same method as 4)
10. https://github.com/neo4j/neo4j/tree/2026.10/community/genai-plugin : module README (read 20261102 20:19 UTC)
11. https://github.com/vitali87/code-graph-rag/blob/main/docs/architecture/embedded-graph.md : Neo4j 5 listed as an opt-in backend (read 20261102 20:19 UTC)
12. https://github.com/neo4j/neo4j/tags : tag names and tagged-commit dates; latest-release call and release list, through the API (read 20261102 20:22 UTC)
13. https://github.com/neo4j/neo4j/commits/2026.10 : commit subjects since 20260804, including two CVE-fix commits naming eight distinct identifiers, through the API (read 20261102 20:37 UTC)

Papers: none cited. Papers on the trend: [infrastructure-and-mcp group](../papers/README.md). Long evidence: [archive entry](../../kb-kg/projects/neo4j.md).
