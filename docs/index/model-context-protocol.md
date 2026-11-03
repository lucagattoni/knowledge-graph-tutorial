---
type: index
kind: standard
aliases: [MCP]
updated: 20261102 21:25 UTC
---

# Model Context Protocol

The Model Context Protocol (MCP) is the open protocol through which language-model applications reach tools and data. This entry gives its definition, the dated revisions from 2024 to the current one, and what its dates mean.

## Definition

The specification calls MCP "an open protocol that enables seamless integration between LLM applications and external data sources and tools". Messages are JSON-RPC 2.0, exchanged between hosts (LLM applications that start connections), clients (connectors inside a host) and servers (services that provide context and capabilities). Servers offer resources, prompts and tools [1]. Revisions carry a `YYYY-MM-DD` identifier, "the last date backwards incompatible changes were made" [2]. "Standard" here means an openly specified protocol, not a W3C, ISO or IETF standard: the sources read name the project's own specification and, since 20251209, a Linux Foundation fund as its home [1][7].

## How it changed

- **20241125.** Anthropic announces MCP as an open standard for secure, two-way connections between data sources and AI tools; Block and Apollo are named early adopters (first-party) [3].
- **20250326.** Revision 2025-03-26 adds an OAuth 2.1 authorization framework, replaces HTTP+SSE with Streamable HTTP, and adds tool annotations [4].
- **20250618.** Revision 2025-06-18 adds structured tool output and elicitation, and classifies MCP servers as OAuth resource servers [5].
- **20251125.** Revision 2025-11-25 adds experimental tasks, URL elicitation and Client ID Metadata Documents, and formalises governance [6].
- **20251209.** MCP is donated to the Agentic AI Foundation, a directed fund of the Linux Foundation (first-party). The post's download and server figures are on the trend page [7].
- **20260728.** Revision 2026-07-28, current when read, removes the `initialize` handshake and protocol-level sessions, adds `server/discover`, moves tasks into an extension, and deprecates Roots, Sampling and Logging [1][2][8]. A release candidate was tagged 20260529 [9].

Still moving: see the trend [Infrastructure and MCP](../trends/infrastructure-and-mcp.md) and the era page [What has settled since 2023](../history/settled-since-2023.md).

## Where sources disagree

No disagreement found in the sources read. Dates need care, though. A revision name is not a release date: the 2024-11-05 revision became a GitHub release on 20250117, after the 20241125 announcement, and a `2024-11-05-final` release followed on 20250326 [9]. The 2025-03-26 changelog names it as the previous revision [4].

## Related

[Agent](./agent.md), [agent memory](./agent-memory.md), [large language model](./large-language-model.md), [retrieval-augmented generation](./retrieval-augmented-generation.md). Projects: [mcp-servers](../projects/mcp-servers.md), [codebase-memory-mcp](../projects/codebase-memory-mcp.md), [neo4j](../projects/neo4j.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [agent-memory (Tigerless Labs)](../projects/tigerless-agent-memory.md)
- [Basic Memory](../projects/basic-memory.md)
- [Claude-Mem](../projects/claude-mem.md)
- [claude-obsidian](../projects/claude-obsidian.md)
- [Code-Graph-RAG](../projects/code-graph-rag.md)
- [code-review-graph](../projects/code-review-graph.md)
- [codebase-memory-mcp](../projects/codebase-memory-mcp.md)
- [CodeGraph](../projects/codegraph.md)
- [Cognee](../projects/cognee.md)
- [Dify](../projects/dify.md)
- [EverOS](../projects/everos.md)
- [FalkorDB](../projects/falkordb.md)
- [Graphify](../projects/graphify.md)
- [GraphRAG SDK](../projects/graphrag-sdk.md)
- [Hindsight](../projects/hindsight.md)
- [HippoRAG](../projects/hipporag.md)
- [Hyper-Extract](../projects/hyper-extract.md)
- [LightRAG](../projects/lightrag.md)
- [LlamaIndex](../projects/llama-index.md)
- [LLM Wiki (nashsu)](../projects/llm-wiki-nashsu.md)
- [MCP reference servers](../projects/mcp-servers.md)
- [Memori](../projects/memori.md)
- [MIRIX](../projects/mirix.md)
- [Neo4j](../projects/neo4j.md)
- [OpenViking](../projects/openviking.md)
- [PageIndex](../projects/pageindex.md)
- [Projects](../projects/README.md)
- [RAG-Anything](../projects/rag-anything.md)
- [RAGFlow](../projects/ragflow.md)
- [Semantica](../projects/semantica.md)
- [Supermemory](../projects/supermemory.md)
- [TencentDB Agent Memory](../projects/tencentdb-agent-memory.md)
- [Understand Anything](../projects/understand-anything.md)

**Papers**

- [Papers: Code graphs for coding agents](../papers/code-knowledge-graphs.md)

**Datasets**

- [Wikidata](../datasets/wikidata.md)

**Experiments**

- [X4: a code graph against grep](../experiments/x4-code-graph-vs-grep.md)

**Applied to Pinakes**

- [Applied to Pinakes](../applied-to-pinakes/README.md)
- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Agent](agent.md)
- [Agent harness](agent-harness.md)
- [Agent Skills](agent-skills.md)
- [AGENTS.md](agents-md.md)
- [Code graph](code-graph.md)
- [Impact analysis](impact-analysis.md)
- [Language Server Protocol](language-server-protocol.md)
- [Tool use](tool-use.md)
- [Tree-sitter](tree-sitter.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://modelcontextprotocol.io/specification/latest : specification overview, schema 2026-07-28, JSON-RPC 2.0, hosts, clients, servers, features (read 20261102 20:52 UTC)
2. https://modelcontextprotocol.io/specification/versioning : version format, Current/Final/Draft, current is 2026-07-28 (read 20261102 20:52 UTC)
3. https://www.anthropic.com/news/model-context-protocol : Anthropic, 20241125 announcement; Block and Apollo (read 20261102 20:52 UTC)
4. https://modelcontextprotocol.io/specification/2025-03-26/changelog : changes since 2024-11-05 (read 20261102 20:52 UTC)
5. https://modelcontextprotocol.io/specification/2025-06-18/changelog : changes since 2025-03-26 (read 20261102 20:52 UTC)
6. https://modelcontextprotocol.io/specification/2025-11-25/changelog : changes since 2025-06-18 (read 20261102 20:52 UTC)
7. https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/ : donation to the Agentic AI Foundation, 20251209 (read 20261102 20:52 UTC)
8. https://modelcontextprotocol.io/specification/2026-07-28/changelog : changes since 2025-11-25; deprecations (read 20261102 20:52 UTC)
9. https://api.github.com/repos/modelcontextprotocol/modelcontextprotocol/releases : release tags and publication times: 2024-11-05 on 20250117, 2024-11-05-final on 20250326, 2025-03-26 on 20250326, 2025-06-18 on 20250618, 2025-11-25 on 20251125, 2026-07-28-RC on 20260529, 2026-07-28 on 20260728 (read 20261102 21:02 UTC)
