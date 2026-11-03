---
type: project
repo: FalkorDB/FalkorDB
trends: [infrastructure-and-mcp]
updated: 20261102 23:17 UTC
---

# FalkorDB

FalkorDB is a [graph database](../index/graph-database.md) that runs as a Redis module and aims at [GraphRAG](../index/graphrag.md), graph retrieval for language models. This page says how it stores and indexes data, what its authors have measured, how its licence file reads, and where the project is heading after a rewrite in Rust.

| Field | Value |
|---|---|
| Repository | https://github.com/FalkorDB/FalkorDB |
| Licence | GitHub cannot classify it: it reports "Other" (NOASSERTION). The `LICENSE` file holds the Server Side Public License v1, then the Elastic License 2.0; which applies to what is unstated [1][2] |
| Trends | [Infrastructure and MCP](../trends/infrastructure-and-mcp.md) |

## What it is

The GitHub description gives the goal as "the best Knowledge Graph for LLM (GraphRAG)" (large language model) [1]. Clients send Redis commands: `GRAPH.QUERY` carries an [OpenCypher](../index/cypher.md) query, from `redis-cli` or any Redis client [3]. The documentation calls FalkorDB "the successor to RedisGraph, built by the team behind the original RedisGraph project", and says RedisGraph reached end of life on 20250131 (first-party) [7].

Version 6.0.0 (20260929) is "the first release of the new FalkorDB engine, written in Rust". It replaces the C engine of every 4.x release; commands, Cypher and client libraries stay the same [6]. The 4.x line continues. The documentation lists four products: the core database, FalkorDB Cloud (managed), FalkorDB Enterprise (self-managed on Kubernetes) and the [GraphRAG SDK](./graphrag-sdk.md) [7][14]. Which features are enterprise-only is unstated. Sources 3, 6 to 11, 14 and 15 are written by FalkorDB itself (first-party).

### Licence terms

The `LICENSE` file has 655 lines. The Server Side Public License v1 (16 October 2018, copyright MongoDB, Inc.) comes first; the Elastic License 2.0 starts at line 563. Nothing in the file says which text covers what [2]. The README names only SSPLv1 [3]. The 4.22.3 tag has a 557-line, SSPL-only `LICENSE.txt` [4]. The 20260802 commit that moved the default branch to the Rust engine removed that file and added the 655-line `LICENSE` [5].

SSPL section 13 requires anyone who offers the program's functionality "to third parties as a service" to release the "Service Source Code", management and hosting software included [2]. The Elastic text forbids providing the software "as a hosted or managed service" that exposes a substantial set of its features, and forbids circumventing licence-key functionality [2]. No legal advice.

## How it works

The README says the engine stores graph adjacency as sparse matrices and runs queries with linear algebra; the model is a [property graph](../index/property-graph.md) with OpenCypher plus proprietary extensions [3]. It claims to be the first queryable property-graph database to do so (first-party; not checked) [3].
**Vectors.** From the first-party documentation: a vector index uses HNSW (hierarchical navigable small world), an [approximate nearest neighbour](../index/approximate-nearest-neighbour.md) method, with cosine or euclidean distance and 1 to 4096 dimensions. Defaults: M 16, efConstruction 200, efRuntime 10. Vectors are inserted with `vecf32` and queried with `db.idx.vector.queryNodes` or `queryRelationships` [8]. The examples pass vectors as literals; the page names no embedding service.

**Text.** Full-text indexes use RediSearch with [TF-IDF](../index/tf-idf.md) (term frequency-inverse document frequency) scoring. 6.0 moved to RediSearch 8.6.1 (from 2.6.23), and scores still default to TFIDF [6][9].

**Agents.** The documentation lists integrations with LangChain, LangGraph, [LlamaIndex](./llama-index.md), AG2, the AWS GraphRAG Toolkit, [Graphify](./graphify.md) and a Text2SQL tool [10]. A separate MCP (Model Context Protocol) server (TypeScript, MIT) exposes Cypher queries and graph management to a [Model Context Protocol](../index/model-context-protocol.md) client over stdio or HTTP. A read-only mode is opt-in, and an agent can override it per call unless a strict flag is also set [11][15]. [Graphiti](./graphiti.md) lists FalkorDB among its supported graph databases, next to [Neo4j](./neo4j.md) [16].

## Evidence

One benchmark, first-party. The README links benchmark.falkordb.com, a page "by FalkorDB" comparing FalkorDB with Neo4j on 10,000 nodes, 121,716 edges and 1,000,000 read queries, at 20 or 40 clients and target rates of 500 to 2,500 messages per second [3][13].

| Measure (run-metrics table) | Platform | FalkorDB | Neo4j |
|---|---|---|---|
| Actual rate against the target | intel | equals the target | 220 to 229 per second |
| | arm | equals the target | 214 to 282 per second |
| p99 latency | intel | 24 to 100 ms | 1.3 to 1.8 s |
| | arm | 24.1 to 99.5 ms | 1.84 to 2.5 s |
| RAM | intel | 15 to 17 MB | 1.6 to 17 GB |
| | arm | 15.2 to 17.4 MB | 1.07 to 1.42 GB |

Each cell spans the table's 10 rows per vendor and platform (20 or 40 clients, target 500 to 2,500 per second) [13]. On Intel the Neo4j RAM column jumps between neighbouring rows (1.6GB, 15GB, 17GB, then 1.6GB again), so no memory figure is compared between vendors; the page gives no reason for the jumps. Neo4j's version, the hardware and the run date are unstated on the page. Independent evaluations were not searched for; none is cited. For retrieval quality see the [GraphRAG SDK](./graphrag-sdk.md) page.

## Status and direction

GitHub's latest-release call returns v6.0.3 (20261022 14:29 UTC); v4.22.3 (20261028) is newer and belongs to 4.x [6]. In the 90 days from 20260804 the repository had 14 releases (one a pre-release) on both lines, and 263 commits from 10 author logins (24 commits by a dependency bot) [6][12]. Of the subjects, 145 start with "fix" (any case), 23 with "perf" and 10 with "feat". Sixteen use one of four phrases for matching the old C engine: "like C" (ten), "as C does" (four), "C-compatible" and "C-parity" (one each). The newest features build a native index to replace RediSearch range fields, behind a flag (20261026 to 20261029) [12].

The 6.0.0 notes say 6.0 has "the same procedures as 4.20.7, and you lose nothing by upgrading". Missing are algorithms developed for the C engine after 4.20: A*, Customizable Contraction Hierarchies and Leiden/Louvain community detection, which are "being ported". The notes say 6.0 publishes no Alpine images and no Alpine, RHEL 8, macOS or debug module builds, and that 4.x and 6.0 nodes cannot replicate to each other [6]. The full-text procedure form does not work on 6.0; the DDL form does [9]. The project is not in maintenance mode. A roadmap is unstated. This trend has no paper group of its own; for graph-database papers see [the foundations papers](../papers/foundations.md).

*Reading:* FalkorDB is a young engine, not yet at feature parity with the C line, under a licence file that has just gained a second text. Its published numbers come from its own benchmark against one rival. The open questions are the licence, the 6.0 migration and the algorithms still being ported.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Graphiti](graphiti.md)
- [GraphRAG SDK](graphrag-sdk.md)
- [LlamaIndex](llama-index.md)
- [Projects](README.md)

**Index**

- [Approximate nearest neighbour](../index/approximate-nearest-neighbour.md)
- [Cypher](../index/cypher.md)
- [Graph database](../index/graph-database.md)
- [HNSW](../index/hnsw.md)
- [Property graph](../index/property-graph.md)
- [tf-idf](../index/tf-idf.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/FalkorDB/FalkorDB : repository metadata through the GitHub API (description, licence field, archived flag, language) (read 20261102 20:18 UTC)
2. https://github.com/FalkorDB/FalkorDB/blob/main/LICENSE : through the API licence endpoint; SSPL v1 text, Elastic License 2.0 from line 563, 655 lines (read 20261102 20:18 UTC)
3. https://github.com/FalkorDB/FalkorDB/blob/main/README.md : description, features, licence statements, developer guide, benchmark link (read 20261102 20:18 UTC)
4. https://github.com/FalkorDB/FalkorDB/tree/v4.22.3 : `LICENSE.txt` (557 lines, SSPL only) and README (read 20261102 20:23 UTC)
5. https://github.com/FalkorDB/FalkorDB/commit/1665fbd98eaf264f13a0891c913345984429d201 : commit of 20260802 18:12 UTC; `LICENSE` added (655 lines), `LICENSE.txt` removed (557) (read 20261102 20:24 UTC)
6. https://github.com/FalkorDB/FalkorDB/releases : release list (14 releases since 20260804, one pre-release; latest v6.0.3) and the v6.0.0 notes through the GitHub API (read 20261102 20:37 UTC)
7. https://docs.falkordb.com/ : successor to RedisGraph, end of life, four products (read 20261102 20:19 UTC)
8. https://docs.falkordb.com/cypher/indexing/vector-index.md : HNSW, distances, dimensions, defaults, query procedures (read 20261102 20:19 UTC)
9. https://docs.falkordb.com/cypher/indexing/fulltext-index.md : RediSearch, TF-IDF, 6.0 warning (read 20261102 20:19 UTC)
10. https://docs.falkordb.com/genai-tools.md : integrations list (read 20261102 20:19 UTC)
11. https://docs.falkordb.com/genai-tools/mcpserver : MCP server, transports, read-only settings (read 20261102 20:19 UTC)
12. https://github.com/FalkorDB/FalkorDB/commits/main : 263 commits since 20260804 through the GitHub API, subject counts by the rules stated in the text (read 20261102 20:37 UTC)
13. https://benchmark.falkordb.com/ : first-party benchmark page, dataset line and the run-metrics table (20 rows per platform, intel and arm), parsed from the page HTML (read 20261102 20:37 UTC)
14. https://docs.falkordb.com/llms.txt : descriptions of FalkorDB Cloud and FalkorDB Enterprise (read 20261102 20:22 UTC)
15. https://github.com/FalkorDB/FalkorDB-MCPServer : repository metadata, MIT licence field, TypeScript (read 20261102 20:24 UTC)
16. https://github.com/getzep/graphiti : README installation requirements (read 20261102 20:23 UTC)
