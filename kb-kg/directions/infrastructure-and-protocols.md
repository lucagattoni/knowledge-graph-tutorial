# Graph databases, embedded stores and the Model Context Protocol

**In one paragraph.** Across the 16 entries behind this page, three things moved between October 2025 and October 2026. The embedded graph database Kuzu was archived on 20251010, and its dependents changed course. Four server databases (Neo4j, FalkorDB, Memgraph, SurrealDB) document vector search, text search and an MCP server. Five projects keep knowledge in SQLite, Markdown or JSONL with no graph-database server. By my count from the entries, 13 of the 16 expose an MCP server. No entry measures one storage choice against another. The measured results are for retrieval and memory systems, and most were measured by their own authors.

## What the direction claims

- **Databases as the agent's graph layer.** FalkorDB's GitHub description reads "the best Knowledge Graph for LLM (GraphRAG)" [FalkorDB](../projects/falkordb.md). Memgraph's README claims "atomic GraphRAG" as one Cypher query [Memgraph](../projects/memgraph.md). SurrealDB's README lists "data layer for AI agents, knowledge graphs" among its uses [SurrealDB](../projects/surrealdb.md).
- **Embedded and serverless.** Kuzu's README presents a graph database that runs inside the host application [Kuzu](../projects/kuzu.md).
- **Files as the source of truth, the index as a cache.** Basic Memory, KiwiFS and agent-memory each say the Markdown files are canonical and the SQLite index can be rebuilt [Basic Memory](../projects/basic-memory.md), [KiwiFS](../projects/kiwifs.md), [agent-memory](../projects/tigerless-agent-memory.md).
- **MCP as the door.** Anthropic announced the Model Context Protocol on 20241125 as "an open standard" for connections between data sources and AI tools; the [timeline](../llm-era/README.md) records it. A knowledge base then answers tool calls instead of feeding a fixed pipeline.

## Who is doing it

| Project | How it takes this direction | Status at 20261030 | Evidence it works (and who measured it) |
|---|---|---|---|
| [Neo4j](../projects/neo4j.md) | GPL-3.0 Community database. Vector and full-text indexes; a `SEARCH` clause for vectors from 2026.01 and full text from 2026.09. Official MCP server. | Active; tags 2026.10.0 and 2026.10.1. | Documented features only; no benchmark in the entry. |
| [FalkorDB](../projects/falkordb.md) | Redis-module graph database; HNSW and RediSearch indexes; MCP server in a separate repository. Licence file holds SSPL v1 then Elastic License 2.0, without saying which applies where. | Active; 6.0.0 (20260929) is the first Rust engine; 4.x continues. | None for the database; its SDK is below. |
| [Memgraph](../projects/memgraph.md) | In-memory Cypher database; USearch vector and Tantivy text indexes; `mcp-memgraph` (7 tools, read-only by default) lives in a separate MIT repository. BSL 1.1 and an enterprise licence. | Active; v3.14.0 (20261021). | Claims only; none measured in the entry. |
| [SurrealDB](../projects/surrealdb.md) | Multi-model database, embeddable; BM25, HNSW and DISKANN indexes; built-in MCP server with 14 tools. BSL 1.1. | Active; v3.3.5 (20261029). | Docs describe an "Agent Memory"; no measurement. |
| [Kuzu](../projects/kuzu.md) | Embedded Cypher database with full-text and vector extensions; MIT. | Archived; last push 20251010. Forks: Ladybug (v0.22.1, pushed 20261030), ryugraph (last push 20260120), bighorn (archived). | The README describes no LLM use. |
| [MCP reference servers](../projects/mcp-servers.md) | Memory server: a JSONL file of entities and relations, 9 tools, substring search, no embeddings. | Active; memory package 2.0.1. The README calls the servers "educational examples". | No benchmark published. |
| [Cognee](../projects/cognee.md) | Three stores: graph (default Ladybug), vector (LanceDB), relational (SQLite). Neo4j and others optional. MCP server. | Active; v1.6.6. | Cognee's own BEAM and LoCoMo reports; no independent run found. |
| [Graphiti](../projects/graphiti.md) | Bring your own database: Neo4j, FalkorDB, embedded FalkorDB, Neptune. Kuzu deprecated. 13-tool reference MCP server. | Active; v0.31.2. | The Zep paper, by the vendor's team, on DMR and LongMemEval; no independent run found. |
| [GraphRAG SDK](../projects/graphrag-sdk.md) | Python library that needs FalkorDB. No MCP path in the file tree. | Active; v1.5.0. | README claim: 71.48 on GraphRAG-Bench against 55.39 for vector RAG with reranking. The project ran only its own system; the entry could not check the rows. |
| [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md) | First-party library on Neo4j: retrievers, an experimental graph builder. No MCP module. | Active; 1.23.0. | No benchmark in the README. |
| [Mem0](../projects/mem0.md) | Vector store first (25 supported). External graph store deleted from open source on 20260414; the hosted Platform has a built-in entity graph and a hosted MCP server. | Python 2.2.1 (20260925); no later release listed. | Paper (own): graph variant 68.44, plain 66.88 on LoCoMo. Independent: see below. |
| [Basic Memory](../projects/basic-memory.md) | Markdown plus SQLite (default) or Postgres; FTS5 and sqlite-vec; 12 MCP tools. AGPL-3.0. | Active; v1.0.0 (20261029). | Own, internal, 60 questions: LongMemEval recall@5 0.951 against mem0 0.979. No independent run. |
| [codebase-memory-mcp](../projects/codebase-memory-mcp.md) | Code graph in SQLite (28 node labels, 42 edge types); 17 MCP tools. | Active; v0.12.1. | Paper (arXiv 2603.27277): 83% answer quality against 92% for file exploration, about ten times fewer tokens. The first author shares a name with the main committer. |
| [HippoRAG](../projects/hipporag.md) | Graph held in python-igraph; embeddings in Parquet, Qdrant, Chroma or Milvus. MCP server (5 tools) added 20261001. | Package 2.0.0a5; last push 20261006. | Authors' papers: average QA F1 59.8 against 57.0 for NV-Embed-v2. |
| [agent-memory (Tigerless)](../projects/tigerless-agent-memory.md) | Markdown plus a SQLite FTS5 cache; "links carry the graph without a graph database". 9-tool stdio MCP server. | Created 20260901; no release. | Own LongMemEval-S study: 52.9% against 35.8% for another system; the ledger lists caveats. |
| [KiwiFS](../projects/kiwifs.md) | Markdown folder with git history and SQLite FTS5; REST, MCP, NFS, S3, WebDAV, FUSE. BSL 1.1. | Active; v0.19.81. | No benchmark. |

## Evidence for

**Databases keep adding retrieval and agent hooks.** *Documented:* all four server databases have vector and full-text indexes and an MCP server. SurrealDB's source tree has `search::rrf` and `search::linear` functions to fuse results. Neo4j's vector docs show quantized search from 2026.07. Graphiti supports four non-deprecated backends and Cognee several. Reading: graph databases remain the substrate of the graph-centred libraries; the archive of one embedded engine did not change that.

**Files and SQLite are common.** *Documented:* five of the 16 keep knowledge in SQLite, Markdown or JSONL files. *Measured, by the project, with the haystack cut to 12 sessions per episode:* agent-memory scored 52.9% on LongMemEval-S, a figure the project says is not comparable with published scores [agent-memory](../projects/tigerless-agent-memory.md).

**Vector-only designs are reported to score close to graph variants.** *Measured, by Mem0:* the graph variant gained 1.56 points over plain Mem0 on LoCoMo, and full context scored higher than both [Mem0](../projects/mem0.md). Reading: that result concerns a feature since deleted from the open source.

**MCP is widely adopted.** *Claimed, by Anthropic, 20251209:* over 97 million monthly SDK downloads and 10,000 active servers [timeline](../llm-era/README.md). *Documented:* 13 of 16 entries expose a server.

## Evidence against, or limits

**Engine risk.** *Documented:* Kuzu was archived with no reason stated; BetaKit, citing an EU filing, reports that Apple agreed on 20251009 to buy the shares and hire select employees [Kuzu](../projects/kuzu.md). Graphiti's README says Kuzu "will be removed in a future release" [Graphiti](../projects/graphiti.md). Mem0 listed Kuzu among five graph stores before deleting the feature [Mem0](../projects/mem0.md).

**Licences.** *Documented:* of the five databases, Neo4j Community is GPL-3.0 and its Enterprise parts are closed; Memgraph and SurrealDB use the Business Source License; FalkorDB's file holds two licences; only Kuzu is MIT. Neo4j's native `VECTOR` properties need block format, placed in Enterprise and Aura.

**No head-to-head on storage.** *Measured, independently (Bao et al., arXiv 2610.30755, 20261022):* Mem0 scored 66.40 on LongMemEval against 87.53 for a raw-RAG baseline. The study proposes that baseline and does not mark which Mem0 cells it re-ran [Mem0](../projects/mem0.md). No entry compares a graph database with SQLite or files at one corpus size.

**MCP surfaces vary and the protocol moves.**
- Graphiti's server has no authentication, `add_memory` returns no job id, and no tool lists a node's neighbours [Graphiti](../projects/graphiti.md). HippoRAG's and Basic Memory's HTTP transports have no authentication [HippoRAG](../projects/hipporag.md), [Basic Memory](../projects/basic-memory.md).
- KiwiFS gives its tool count as 62, 69 and 78 in different places [KiwiFS](../projects/kiwifs.md).
- Revision 2026-07-28 removes protocol-level sessions and the `initialize` handshake, and deprecates Roots, Sampling and Logging. Deprecated features "remain fully functional" through a minimum twelve-month window [S1]. Servers that need state "use explicit, server-minted handles passed as ordinary tool arguments" [S1].
- Tigerless's hand-written server reports protocol string "2025-06-18"; the memory reference server serves both the 2026-07-28 and a 2025 revision [agent-memory](../projects/tigerless-agent-memory.md), [MCP servers](../projects/mcp-servers.md).
- Whether tool-based traversal beats a fixed pipeline is unmeasured in the [timeline](../llm-era/README.md).

## What is unresolved

- Is the `ladybug` package Cognee depends on the Kuzu fork? Unstated [Cognee](../projects/cognee.md).
- Why Kuzu stopped, and what Apple intends. BetaKit says the motivation is unclear.
- How memory servers adapt to stateless MCP. Cognee lists `mcp-sampling` as an LLM provider; the effect of the Sampling deprecation on it is unstated.
- Which FalkorDB licence covers which files; the Memgraph enterprise licence PDF could not be read.
- Whether a graph database beats files and SQLite at any corpus size. The [timeline](../llm-era/README.md) lists the wiki-size question as open.
- Whether MCP tools that expose raw Cypher (Neo4j, Memgraph, SurrealDB) serve agents differently from curated memory tools. No entry measures it.

## Signals to watch

| Check | Where | Would show |
|---|---|---|
| Release cadence of Ladybug after v0.22.1 (20261030); whether ryugraph pushes again | The fork repositories | Whether Kuzu's users have a maintained successor |
| Graphiti removes the Kuzu driver; Cognee's `.env.template` still sets `kuzu` | Graphiti README and release notes; Cognee `.env.template` | Dependents finishing the move |
| Memgraph's BSL change date, written "2030-21-10" | `licenses/BSL.txt` | A corrected date |
| SurrealDB docs cite "since v4.0.0" while the latest release is v3.3.5 | Releases page | Whether a v4 appears |
| FalkorDB licence file clarified; 6.0 gap in full-text procedure creation closed | Release notes | Licence clarity; engine parity |
| A revision after 2026-07-28, or a removal date for Sampling, Roots and Logging | MCP changelog | The protocol's pace; earliest removal is 12 months after deprecation (computed: July 2027) |
| Servers' migration notes to 2026-07-28 | Repositories of the 13 projects with an MCP server | Effect of stateless MCP |
| A later version of arXiv 2610.30755 adding Cognee, Graphiti or Basic Memory | arXiv | First independent comparison |
| Mem0 release after 20260925 | Releases | Continued open-source investment |

## Sources

Entries: [Neo4j](../projects/neo4j.md), [FalkorDB](../projects/falkordb.md), [Memgraph](../projects/memgraph.md), [SurrealDB](../projects/surrealdb.md), [Kuzu](../projects/kuzu.md), [MCP servers](../projects/mcp-servers.md), [Cognee](../projects/cognee.md), [Graphiti](../projects/graphiti.md), [GraphRAG SDK](../projects/graphrag-sdk.md), [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md), [Mem0](../projects/mem0.md), [Basic Memory](../projects/basic-memory.md), [codebase-memory-mcp](../projects/codebase-memory-mcp.md), [HippoRAG](../projects/hipporag.md), [agent-memory](../projects/tigerless-agent-memory.md), [KiwiFS](../projects/kiwifs.md). Context: the [timeline](../llm-era/README.md), which holds the Kuzu archive row (20251010), the MCP revision tags 2025-03-26, 2025-06-18, 2025-11-25 and 2026-07-28, and the Anthropic figures; [papers and benchmarks](../papers-benchmarks/README.md).

S1. Model Context Protocol, "Key Changes", revision 2026-07-28: https://modelcontextprotocol.io/specification/2026-07-28/changelog (read 20261030 19:57 UTC).
