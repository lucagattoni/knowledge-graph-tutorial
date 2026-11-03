---
type: trend
shift: vector-only stores and custom connectors -> vector indexes inside existing databases and one protocol
status: steady
order: 11
updated: 20261103 01:52 UTC
---

# Infrastructure and MCP: what knowledge systems run on, and how agents reach them

This page answers two questions. What do the knowledge systems of the other trends run on? How does an agent reach them? It follows five strands: [graph databases](../index/graph-database.md), embedded stores, vector indexes in relational databases, the [Model Context Protocol](../index/model-context-protocol.md) (MCP) and platforms for [retrieval-augmented generation](../index/retrieval-augmented-generation.md) (RAG). It dates the facts, says who measured what, and ends with a labelled reading.

> **Distinctive because** this is a theme, not a family: it holds no retrieval method, only the layer under the other trends. The nearest neighbour is [graph-based RAG](./graph-based-rag.md), which builds a graph index; this page asks where an index lives and how an agent reaches it.

## Why it emerged

Three developments, each with its own source. First, vector search. Stonebraker and Pavlo (2024) call vector database management systems (DBMSs) "essentially document-oriented DBMSs with specialized ANN indexes" (ANN: [approximate nearest neighbour](../index/approximate-nearest-neighbour.md)) and say that in 2023 Oracle, SingleStore, Rockset and ClickHouse added vector indexes [16]. Second, tool access. Anthropic's announcement says "Every new data source requires its own custom implementation" and offers one protocol to replace "fragmented integrations" (first-party) [5]. Third, graph querying: ISO published SQL/PGQ (SQL Property Graph Queries) in 202306 and [GQL](../index/gql.md) (Graph Query Language) in April 2024: ISO's lifecycle table and the IEC web store give 20240412, and the GQL committee announced it on 20240417 [14][15][40]. *Reading:* the three are independent. No source read says one caused another. Two shifts run through them: vector search became an index inside existing databases [16], and tool access moved from one custom connector per data source to one protocol [5].

Chapter 1 adds the older story: how Neo4j and Cypher arrived (Neo4j 2.0 in 2013, by Neo4j's own account) in [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md), and why GQL and SQL/PGQ count as settled, with the dispute over specialised graph databases, in [What has settled since 2023](../history/settled-since-2023.md).

## Why it matters

This page is a theme chosen by the owner (decision T-2, see the [trends overview](./README.md)), not a family, so it has no growth test of its own. The storage choice sets cost: in one comparison, bulk-ingest throughput ranged from 5.0k to 4.3M rows/s across engines (first-party in part) [34]. It sets licence terms (see the table below). The protocol sets how an agent reaches a memory or a code graph, so its revisions reach [agent memory](./agent-memory.md) and [code graphs](./code-knowledge-graphs.md). It also sets the attack surface [36].

## How it works

### Graph databases and their standards

Two ISO standards define graph querying. For ISO/IEC 39075:2024 (GQL), ISO's lifecycle table and the IEC web store give 20240412 as the publication date, and the committee announced it on 20240417; the committee also says the shared graph pattern language is kept "as identical as possible" with SQL/PGQ [14][40]. The [GQL](../index/gql.md) entry holds the full account of the dates. ISO lists ISO/IEC 9075-16:2023 (SQL/PGQ) as published in 202306, with a 2026 corrigendum and a successor in development [15]. See [GQL](../index/gql.md), [SQL/PGQ](../index/sql-pgq.md) and [property graphs](../index/property-graph.md). Which database implements which standard: **unstated**; no product page read states conformance.

Three server databases document a [Cypher](../index/cypher.md)-style model and a vector index [17][18][19]:

| Database | Vector index, as documented | Source |
|---|---|---|
| [Neo4j](../projects/neo4j.md) | Built on Apache Lucene (HNSW, [hierarchical navigable small world](../index/hnsw.md) graphs). A `SEARCH` clause is "the preferred way" of querying since 2026.01. Native `VECTOR` properties need block format, in Enterprise Edition and Aura | [17] |
| [Memgraph](../projects/memgraph.md) | USearch backend; `CREATE VECTOR INDEX` with `dimension` and `capacity` | [18] |
| [FalkorDB](../projects/falkordb.md) | HNSW; `db.idx.vector.queryNodes` | [19] |

Stonebraker and Pavlo wrote in 2024: "We do not expect specialized graph DBMSs to be a large market" [16].
### Embedded stores and their risks

An [embedded database](../index/embedded-database.md) runs inside the application, so its maintainer's fate becomes the application's. Kuzu is the case: an embedded property-graph database with Cypher, full-text and vector search, MIT-licensed [9]. Its GitHub flag reads archived; the last push and release (v0.11.3) are both 20251010, and the README says it "is working on something new" [9]. BetaKit (20260212) reports, from an EU filing, that Apple agreed on 20251009 to buy Kuzu's shares and hire select employees [12]. The Register (20251014) reports no detailed explanation and a fork, bighorn [13]. [Graphiti](../projects/graphiti.md)'s README says Kuzu "is deprecated and will be removed in a future release" [11]. A fork, [LadybugDB/ladybug](https://github.com/LadybugDB/ladybug), is "formerly known as Kuzu", MIT-licensed; v0.22.1 came out on 20261028 [10]. The fork is not in the 20261030 19:54 UTC snapshot, so no star count is given. Why Kuzu stopped: **unstated**. The dated record of removals is on [features in and out](./features-in-and-out.md).

### Vector indexes in relational databases

Relational systems took over the [vector search](../index/vector-search.md) job as an extension. [pgvector](https://github.com/pgvector/pgvector) is "open-source vector similarity search for Postgres": exact search by default, approximate search through [HNSW](../index/hnsw.md) or IVFFlat, Postgres 13 and later; its licence file is a PostgreSQL-style notice and GitHub's field reads `NOASSERTION` [24]. The SQLite extension [sqlite-vec](https://github.com/asg017/sqlite-vec) says it is "pre-v1, so expect breaking changes"; Apache licence file; last pushed 20260518 [25]. Neither pgvector nor sqlite-vec is in the 20261030 19:54 UTC snapshot, so no star counts are given. No vendor page of the 2023 adopters was read. One 2026 paper, by a single author, builds a graph-RAG engine inside PostgreSQL, with pgvector for search and edge tables for traversal (first-party; abstract only) [37].

### The Model Context Protocol and its revisions

Anthropic announced MCP on 20241125 as "an open standard that enables developers to build secure, two-way connections" between data and AI tools (first-party) [5]. Revisions are named by the date of the last backward-incompatible change [2]:

| Revision | What changed | Source |
|---|---|---|
| 2025-03-26 | OAuth 2.1 authorization framework; Streamable HTTP replaces HTTP+SSE (Server-Sent Events); tool annotations | [4] |
| 2025-11-25 | Experimental tasks; URL elicitation; Client ID Metadata Documents; tool calling inside sampling | [3] |
| 2026-07-28 | Release candidate tagged 20260529, stable 20260728. Stateless: no sessions, no `initialize` handshake, mandatory `server/discover` | [7][1] |

Revision 2025-06-18 is a tag (20250618); contents not read: **unstated** [7]. In 2026-07-28, servers that need state "use explicit, server-minted handles passed as ordinary tool arguments" [1]. *Reading:* a memory server that kept state in a session must change; no server's migration notes were read: **unstated**. Roots, Sampling and Logging are deprecated and "remain fully functional" during the window [1]. The window is at least twelve months, or at least ninety days under an expedited-removal exception for an active security risk [2][38]. Dynamic Client Registration and HTTP+SSE are deprecated too [1].

On 20251209 MCP joined the Agentic AI Foundation, a Linux Foundation directed fund, with goose and AGENTS.md; the post reports "Over 97 million monthly SDK downloads" (SDK: software development kit) and "10,000 active servers" (first-party) [6]. The repository licence file records a move from MIT to Apache-2.0 for new contributions [8].

Database vendors ship servers. Neo4j's `neo4j/mcp` has `get-schema`, `read-cypher`, `write-cypher` and `list-gds-procedures`; its README warns that a procedure wrongly classified as read-only "may bypass" the read-only check [26]. Memgraph lists an `mcp-memgraph` package and FalkorDB an MIT-licensed `FalkorDB-MCPServer` [27]. RAGFlow acts as MCP server and client [29]. The reference repository says its servers are "educational examples", "not as production-ready solutions" [8]. The snapshot lists 53 of 552 active repositories (pushed within 90 days, not archived) with MCP in name or description; one of its 17 queries targets the `mcp-server` topic, so this is a selected count, not a rate [32].

### RAG platforms

Platforms bundle parsing, indexing, [retrieval-augmented generation](../index/retrieval-augmented-generation.md) and agents; graphs are one option.

- **RAGFlow** (Apache-2.0 file) [28]. Release 0.27.0 (20260819) added Knowledge Compilation (Wiki, Graph, Tree, PageIndex, Mindmap, Timeline, Skills). Its notes say the earlier GraphRAG and RAPTOR features "have been deprecated and are no longer available in the UI" (user interface) [29]. 1.0.0-rc1 (20260929) is a rewrite in Go with an irreversible data upgrade [29]. See [vectorless retrieval](./reasoning-over-structure.md).
- **Dify**: modified Apache 2.0; a multi-tenant service, or removing logo and copyright information, needs a commercial licence [31]. Release 1.18.0 (20261023) adds an opt-in beta Agent Knowledge Base; "Classic Knowledge remains available" [31].
- **LlamaIndex** (MIT file): the README says "our primary focus has shifted towards LlamaParse" while the framework stays available [30].

## Representative projects

Stars: snapshot of 20261030 19:54 UTC [32]. Stars are a signal, not a verdict; none of these is flagged fast-growth [32].

| Project | Role | Licence, from the LICENSE file | Stars |
|---|---|---|---|
| [neo4j](../projects/neo4j.md) | Server graph database | GPL-3.0 (Community Edition) [20] | 17,378 |
| [falkordb](../projects/falkordb.md) | Graph database (GraphBLAS) | Server Side Public License v1 (SSPL) text, then Elastic License 2.0 (ELv2) text, in one file; which applies where: **unstated**. The README badge says SSPL [21] | 10,507 |
| [memgraph](../projects/memgraph.md) | In-memory graph database | Business Source License 1.1 (BSL) and Memgraph Enterprise License, "variously" [22] | 4,636 |
| [mcp-servers](../projects/mcp-servers.md) | MCP reference servers | Apache-2.0 for new work, MIT for earlier, CC-BY-4.0 for docs [8] | 91,700 |
| [llama-index](../projects/llama-index.md) | Framework | MIT [30] | 52,747 |
| [ragflow](../projects/ragflow.md) | RAG engine | Apache-2.0 [28] | 93,209 |
| [dify](../projects/dify.md) | [large language model](../index/large-language-model.md) (LLM) app platform | Modified Apache 2.0 with conditions [31] | 160,020 |

Also named: [SurrealDB](https://github.com/surrealdb/surrealdb), Business Source License 1.1, 33,253 stars [23][32].

## Fundamental papers

This theme has no paper group of its own. Its older papers (the relational model, the Cypher language paper, a survey of graph database models) are in [foundations](../papers/foundations.md); the map is in [papers](../papers/README.md).
## What is measured, and by whom

| What | Result | By whom | Source |
|---|---|---|---|
| Eight engines (Corvic AI and seven graph or SQL/PGQ engines), 20-query workload, synthetic graph of 1.02 million nodes | "No system in this sample is categorically fastest"; bulk ingest 5.0k to 4.3M rows/s | Nguyen and three others (20260920). Three authors list Corvic AI Research and the paper calls Corvic AI "our subject system": first-party in part | [34] |
| MCP against a command line with the same operations, six models, three environments | Differences in task performance and cost; structured divergence in 94.3% of 2,004 episodes | Shi and two others (20261025), on their own benchmark MICA (first-party). They also propose a repair method, DART, and report its gains | [35] |
| The authors' own attack, Log-To-Leak, through MCP tool descriptions, on 5 servers and 4 agents | Attack success 62.64 to 100% over 18 model-server pairs; three defences leave above 55% on one pair | Hu and three others (20261026), first-party | [36] |
| MCP downloads and servers | 97 million+ monthly SDK downloads; 10,000 active servers | Anthropic (first-party) | [6] |

arXiv keyword hits (computer-science filter, abstracts, first submission 20251102 to 20261102 against 20241102 to 20251101, read 20261102 20:40 to 20:45) [33]:

| Query | Window | Year before | Ratio |
|---|---|---|---|
| "Model Context Protocol" | 440 | 159 | 2.8 |
| the same, with "security" | 107 | 54 | 2.0 |
| "graph database" | 64 | 76 | 0.8 |
| "vector database" | 161 | 133 | 1.2 |
| control: "LLM agents" | 3,289 | 988 | 3.3 |
| control: "retrieval-augmented generation" | 2,586 | 2,389 | 1.1 |

These are "N results for query Q", not counts of papers in the field. MCP existed for only one month of the earlier year. Not measured by any source read: a graph database against files or SQLite at one corpus size; tool-based traversal against a fixed pipeline. No [experiment](../experiments/README.md) of this documentation tests this trend.

## Assessment

*Reading:* **Strengths.** The three server databases document vector indexes, and pgvector and sqlite-vec put them inside general stores, so a team can start without a new database. MCP gave tools one door; its revision log shows work on authorization, transport and state. **Weaknesses.** An embedded engine with one maintainer carries the risk Kuzu shows. Licences vary (GPL, SSPL with ELv2, BSL), and only the file tells which. MCP revisions arrived three to eight months apart (tag dates), so servers must keep up. A database server that accepts raw Cypher widens the attack surface that the MCP security paper studies. **Heading.** Platforms such as RAGFlow turn graph features into options inside a wider compiler of artifacts. Activity alone does not refute the Stonebraker and Pavlo forecast.

*Reading:* **Status `steady`.** The test compares growth with controls. The trends overview's controls are any-LLM wording x1.38, any-RAG wording x1.23 and LLM-agent wording x2.50 [39]; its query wording is not given there, so why this page's controls differ (3.3 and 1.1) is **unstated**. MCP hits (x2.8) beat the any-LLM and RAG controls and lie between the two agent-control values (x2.5, x3.3). The database queries (x0.8, x1.2) beat no control. So only the MCP strand grows; the theme is `steady`.

## Signals to watch

| Signal | Where | Baseline |
|---|---|---|
| A revision after 2026-07-28; a removal date for Sampling, Roots or Logging | MCP changelog and releases | 2026-07-28 current; earliest removal under the normal rule 20270728 (computed: the revision date plus twelve months); sooner only through an expedited-removal exception [1][2][38] |
| Ladybug's release cadence; Graphiti removing its Kuzu driver | Fork and Graphiti README | v0.22.1 on 20261028; Kuzu "deprecated" (20261102) [10][11] |
| FalkorDB clarifying which licence applies | LICENSE file | SSPL then ELv2 in one file [21] |
| RAGFlow 1.0.0 final | Releases | rc3 on 20261030 [29] |
| GQL implemented by a named database | Vendor documentation | **unstated** today |
| Independent storage comparison, graph database against files or SQLite | arXiv | none found |

## Sources

Read times are from the clock; where several pages were read in one batch, the clock was checked just after.

1. https://modelcontextprotocol.io/specification/2026-07-28/changelog : stateless change, `server/discover`, deprecations, handles (read 20261102 20:46 UTC)
2. https://modelcontextprotocol.io/specification/versioning : date-stamped versions, deprecation floors (twelve months; ninety days under the exception), current revision (read 20261102 20:30 UTC)
3. https://modelcontextprotocol.io/specification/2025-11-25/changelog : tasks, URL elicitation, Client ID Metadata Documents (read 20261102 20:12 UTC)
4. https://modelcontextprotocol.io/specification/2025-03-26/changelog : authorization, Streamable HTTP, annotations (read 20261102 20:12 UTC)
5. https://www.anthropic.com/news/model-context-protocol : announcement of 20241125, custom implementations, fragmented integrations (first-party; read 20261102 20:46 UTC)
6. https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/ : foundation, goose, AGENTS.md, download and server figures (first-party; read 20261102 20:12 UTC)
7. https://github.com/modelcontextprotocol/modelcontextprotocol/releases : tags 2025-03-26, 2025-06-18, 2025-11-25, 2026-07-28 and its release candidate, with publish dates (read 20261102 20:12 UTC)
8. https://github.com/modelcontextprotocol/servers : LICENSE (MIT to Apache-2.0 transition), README "reference implementations" warning, repository metadata (read 20261102 20:10 UTC)
9. https://github.com/kuzudb/kuzu : archived flag, last push, v0.11.3, README note, MIT file (read 20261102 20:10 UTC)
10. https://github.com/LadybugDB/ladybug : README, LICENSE, v0.22.1, creation date (read 20261102 20:10 UTC; the latest-release call was run again 20261102 22:52 UTC with the same result)
11. https://github.com/getzep/graphiti : README Kuzu deprecation and backend list (read 20261102 20:11 UTC)
12. https://betakit.com/apple-strikes-deal-to-acquire-canadian-database-software-startup-kuzu/ : Apple agreement of 20251009 (read 20261102 20:17 UTC)
13. https://www.theregister.com/2025/10/14/kuzudb_abandoned/ : no explanation, bighorn fork (read 20261102 20:17 UTC)
14. https://www.gqlstandards.org/ : ISO/IEC 39075:2024 announced as published 20240417; shared pattern language (read 20261102 20:13 UTC; the announcement re-read 20261102 22:52 UTC)
15. https://committee.iso.org/es/sites/isoorg/contents/data/standard/07/94/79473.html : ISO/IEC 9075-16:2023, Cor 1:2026, successor in development (read 20261102 20:13 UTC; WebFetch extraction of a Spanish-language page)
16. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), 2024; vector DBMS description, 2023 adopters, graph DBMS forecast (read 20261102 20:46 UTC, full text)
17. https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/ : vector index documentation (read 20261102 20:16 UTC)
18. https://memgraph.com/docs/querying/vector-search : vector index documentation (read 20261102 20:16 UTC)
19. https://docs.falkordb.com/cypher/indexing/vector-index.html : vector index documentation (read 20261102 20:16 UTC)
20. https://github.com/neo4j/neo4j : LICENSE.txt (GPL-3.0) (read 20261102 20:10 UTC)
21. https://github.com/FalkorDB/FalkorDB : LICENSE (SSPL v1, then ELv2), README badge, description (read 20261102 20:10 UTC)
22. https://github.com/memgraph/memgraph : LICENSE (BSL 1.1 and MEL), description (read 20261102 20:10 UTC)
23. https://github.com/surrealdb/surrealdb : LICENSE (BSL 1.1) (read 20261102 20:11 UTC)
24. https://github.com/pgvector/pgvector : README, LICENSE, metadata (read 20261102 20:11 UTC; the star count read then is not used)
25. https://github.com/asg017/sqlite-vec : README, LICENSE-APACHE, metadata (read 20261102 20:11 UTC; the star count read then is not used)
26. https://github.com/neo4j/mcp : README tools and warning (read 20261102 20:12 UTC)
27. https://github.com/FalkorDB/FalkorDB-MCPServer and https://github.com/memgraph/ai-toolkit : repository metadata (MIT) and `mcp-memgraph` line in the README (read 20261102 20:12 UTC)
28. https://github.com/infiniflow/ragflow : LICENSE (Apache-2.0), README, description (read 20261102 20:11 UTC)
29. https://github.com/infiniflow/ragflow/blob/main/docs/release_notes.md and docs/develop/mcp/overview.md : releases 0.27.0 to 1.0.0-rc3; MCP server and client (read 20261102 20:12 UTC; the latest-release call was run again 20261102 22:52 UTC and returned v1.0.0-rc3, 20261030)
30. https://github.com/run-llama/llama_index : LICENSE (MIT), README focus note (read 20261102 20:11 UTC)
31. https://github.com/langgenius/dify : LICENSE, release 1.18.0 notes (read 20261102 20:11 UTC; the latest-release call was run again 20261102 22:52 UTC and returned 1.18.0, 20261023)
32. kb-kg/landscape/20261030_1954-github/repos.tsv (repository path): stars, push dates, flags, 17 queries, snapshot of 20261030 19:54 UTC (read 20261102 20:16 UTC)
33. https://arxiv.org/search/advanced : advanced search, abstract field, computer-science filter, first submission 20251102 to 20261102 and 20241102 to 20251101; queries as in the table, all six re-run (read 20261102 20:40 to 20:45 UTC)
34. https://arxiv.org/abs/2609.23315 and https://arxiv.org/html/2609.23315 : Nguyen et al., graph database engines comparison, v1 20260920; abstract, then full text for affiliations and the "subject system" wording (read 20261102 20:30 to 20:31 UTC)
35. https://arxiv.org/abs/2610.34298 : Shi et al., MCP and CLI study (MICA, DART), v1 20261025 (abstract; read 20261102 20:30 UTC)
36. https://arxiv.org/abs/2610.36108 : Hu et al., Log-To-Leak, v1 20261026; five servers, four agents, 18 valid pairs, defences (abstract; read 20261102 20:30 UTC)
37. https://arxiv.org/abs/2608.24921 : Rajah, post-graph-rag, v1 20260814 (abstract; read 20261102 20:30 UTC)
38. https://modelcontextprotocol.io/community/feature-lifecycle : twelve-month floor; expedited removal for an active security risk, at least ninety days (read 20261102 20:31 UTC)
39. plans/20261102_1951-docs-catalogue.md (repository path): chapter 2, controls any LLM x1.38, any RAG x1.23, LLM-agent x2.50 (read 20261102 20:29 UTC)
40. https://committee.iso.org/es/sites/isoorg/contents/data/standard/07/61/76120.html and https://webstore.iec.ch/publication/94107 : ISO catalogue page for ISO/IEC 39075:2024, lifecycle table with "International Standard published" (stage 60.60) on 2024-04-12; IEC web store, publication date 2024-04-12 (iso.org itself returned 403; read 20261102 22:52 to 22:57 UTC; the dates are reconciled on the GQL index entry)
