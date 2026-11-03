---
type: project
repo: memgraph/memgraph
trends: [infrastructure-and-mcp]
updated: 20261102 23:17 UTC
---

# Memgraph

Memgraph is an in-memory [graph database](../index/graph-database.md) written in C++ and offered as a community edition under the Business Source License and a paid enterprise edition. This page says what it stores, how its vector and text indexes work, what its authors have measured, how its mixed licence reads, and how fast it ships.

| Field | Value |
|---|---|
| Repository | https://github.com/memgraph/memgraph |
| Licence | GitHub cannot classify it: it reports "Other" (NOASSERTION). The five-line `LICENSE` file says the source "is variously licensed under the Business Source License 1.1 (BSL), the Memgraph Enterprise License (MEL)"; a file is under the BSL unless it says otherwise [1][2] |
| Trends | [Infrastructure and MCP](../trends/infrastructure-and-mcp.md) |

## What it is

The README calls Memgraph an in-memory graph database that "powers real-time AI context and graph analytics", built in C/C++ as the graph engine for [GraphRAG](../index/graphrag.md) pipelines, [AI memory](../index/agent-memory.md) and agent workflows (first-party) [6]. It says it is "fully compatible with Neo4j's Cypher query language" and compliant with [ACID](../index/acid.md) (atomicity, consistency, isolation and durability) [6]; compare [Neo4j](./neo4j.md). The README lists high availability, multi-tenancy, fine-grained access control and single sign-on under "Enterprise", and a managed Memgraph Cloud on AWS that runs Enterprise instances [6].

Around the database sit a 40-plus algorithm library (MAGE) and a separate MIT-licensed repository, `ai-toolkit`. The toolkit packages Context Graph (memory for coding agents), `unstructured2graph` (entity extraction with a GLiNER2 backend by default, a project separate from [GLiNER](./gliner.md), or [LightRAG](./lightrag.md) as an alternative), LangChain and LightRAG integrations, and an MCP server [11].

### Licence terms

`BSL.txt`, dated 1 January 2026, names Memgraph Ltd as licensor and "Memgraph Community Edition (MCE) version 2.0" as the Licensed Work. The latest release is v3.14.0; how the versions map is unstated [4][9]. Production use is allowed for internal business purposes, but not if you embed or distribute the work so third parties can operate it, host it as database-as-a-service, or use it to build a competing work. The Change Date is written `2030-21-10` and the Change License is Apache 2.0 [4].

*Reading:* four commits titled "Update BSL change date" (20260909, 20260914, 20261009, 20261021) each match a release date and set the year to 2030 [9][10]. So the Change Date appears to be release date plus four years, written year-day-month. The BSL gives two end points, the Change Date or "the fourth anniversary of the first publicly available distribution" of a version, "whichever comes first", and says the date "may vary for each version" [4].

`MEL.pdf` is an 11-page Enterprise Licence Agreement for proprietary "Memgraph Enterprise Edition", sold as a subscription (a 30-day trial exists; a three-year minimum term applies when an order names none). Its definition of the software excludes the Community Edition [5]. In three source files sampled, two C++ files carry a BSL header (one wraps its code in `#ifdef MG_ENTERPRISE`) and one Python file carries a MEL header; the full split is unstated [15]. No legal advice.

## How it works

Data are a graph queried in [Cypher](../index/cypher.md) [6]. **Vectors:** an index on a label or edge type uses the USearch backend, needs `dimension` and `capacity`, and defaults to squared-euclidean distance and 32-bit floats. The query planner does not use it; searches go through `vector_search.search`, and the index runs at READ_UNCOMMITTED isolation [7]. The client supplies the [embeddings](../index/embedding.md). **Text:** indexes use Tantivy, are searched with `text_search.search`, take a snapshot per search, and have not been experimental since 3.6 [8].

The README claims "atomic GraphRAG", where pivot search, expansion, ranking and prompt assembly are one Cypher query, and `SHOW SCHEMA INFO` for [Text2Cypher](../index/text-to-query.md) [6]. `mcp-memgraph` exposes seven tools, among them `run_cypher_query` and `search_schema`, and is read-only unless `MCP_READ_ONLY=false` [11]. LightRAG's README lists Memgraph as a graph-storage option [16].

## Evidence

Published, first-party, and about the toolkit, not the database. The Context Graph evaluation reports, for version 0.12.0 on 500 [LongMemEval](../datasets/longmemeval.md)-S questions, an answer score of 87.4% and evidence recall of 0.96, and on 400 BEAM 100K questions 63.1% and 0.70. Answers came from gpt-4.1, judged by each benchmark's own judge, on an Apple M2 Pro against Memgraph 3.13.2; the report anchors carry 20261028 [12]. The build uses no LLM (large language model). These are retrieval results for agent memory; they do not rank Memgraph against another database.

The README links "benchgraph", described as a Neo4j and Memgraph comparison of latency, throughput and memory. The page is rendered by script and I read no figures from it: unstated [6][14]. Independent evaluations were not searched for.

## Status and direction

The latest release is v3.14.0 (20261021 11:05 UTC). In the 90 days from 20260804 there were four releases (v3.13.0, v3.13.1, v3.13.2, v3.14.0) and 366 commits from 13 author logins [9][10]. Of the subjects, 171 start with "fix" (any case) and 47 with "feat". Features include conditional `CALL` subqueries, label expressions, transactional auth queries and recovery of asynchronous replicas [10]. Two commits (20260910, 20260921) touch the licence mechanism: a core limit, and tier and validity [10].

The roadmap repository says Memgraph works in six-week release cycles and considers long-term support; its last update is 20260929, with the next promised for 20261020; at the read time (20261102) that update was overdue, and the roadmap repository's newest commit was still 20260929 [13]. The project is not in maintenance mode. Enterprise features sit behind a paid licence and a hosted tier; whether any feature moved there from the Community Edition is unstated. This trend has no paper group of its own; for graph-database papers see [the foundations papers](../papers/foundations.md).

*Reading:* Memgraph ships fast and puts vector and text retrieval inside the database. Its licence mixes two texts and the Change Date moves with every release, so anyone planning to host it for others should read the file itself.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)
- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Code-Graph-RAG](code-graph-rag.md)
- [LightRAG](lightrag.md)
- [Mem0](mem0.md)
- [Projects](README.md)

**Index**

- [ACID](../index/acid.md)
- [Approximate nearest neighbour](../index/approximate-nearest-neighbour.md)
- [Cypher](../index/cypher.md)
- [Graph database](../index/graph-database.md)
- [Property graph](../index/property-graph.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/memgraph/memgraph : repository metadata through the GitHub API (description, licence field, archived flag, language) (read 20261102 20:18 UTC)
2. https://github.com/memgraph/memgraph/blob/master/LICENSE : through the API licence endpoint; five lines (read 20261102 20:18 UTC)
3. https://github.com/memgraph/memgraph/tree/master/licenses : directory listing, `APL.txt`, `BSL.txt`, `MEL.pdf` (read 20261102 20:18 UTC)
4. https://github.com/memgraph/memgraph/blob/master/licenses/BSL.txt : parameters, Additional Use Grant, Change Date, Change License, fourth-anniversary and per-version clauses (read 20261102 20:37 UTC)
5. https://github.com/memgraph/memgraph/blob/master/licenses/MEL.pdf : 11 pages, text extracted locally (read 20261102 20:19 UTC)
6. https://github.com/memgraph/memgraph/blob/master/README.md : description, feature list, Cloud, roadmap link, licence section (read 20261102 20:18 UTC)
7. https://memgraph.com/docs/querying/vector-search : USearch, configuration, planner and isolation notes (read 20261102 20:19 UTC)
8. https://memgraph.com/docs/querying/text-search : Tantivy, procedures, status since 3.6 (read 20261102 20:19 UTC)
9. https://github.com/memgraph/memgraph/releases : release list through the GitHub API (read 20261102 20:18 UTC; v3.13.0 to v3.14.0 dates re-read 20261102 20:39 UTC)
10. https://github.com/memgraph/memgraph/commits/master : 366 commits since 20260804 through the GitHub API; the four BSL commits and the subject counts re-read (read 20261102 20:37 UTC)
11. https://github.com/memgraph/ai-toolkit : README, `integrations/mcp-memgraph/README.md`, licence field MIT (read 20261102 20:21 UTC)
12. https://github.com/memgraph/ai-toolkit/blob/main/context-graph/eval/README.md : "Official numbers" table and set-up (read 20261102 20:21 UTC)
13. https://github.com/memgraph/roadmap : README (last update 20260929, next ETA 20261020), release cycle, newest commit 20260929 (read 20261102 20:37 UTC; commit list 20:38 UTC)
14. https://memgraph.com/benchgraph : page title and description only (read 20261102 20:20 UTC)
15. https://github.com/memgraph/memgraph/blob/master/src/license/license.cpp , `src/coordination/coordinator_cluster_state.cpp` and `src/mage/python/cross_database.py` : file headers (read 20261102 20:20 UTC)
16. https://github.com/HKUDS/LightRAG : README storage-backend sentence (read 20261102 20:23 UTC)
