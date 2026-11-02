---
type: project
repo: infiniflow/ragflow
trends: [reasoning-over-structure, infrastructure-and-mcp]
updated: 20261102 23:17 UTC
---

# RAGFlow

RAGFlow is a self-hosted platform for [retrieval-augmented generation](../index/retrieval-augmented-generation.md): it parses documents, indexes them and answers through chat or agents. This page says why it sits in two trends, what its newest feature does with trees and graphs, and what has and has not been measured.

| Field | Value |
|---|---|
| Repository | https://github.com/infiniflow/ragflow |
| Licence | Apache-2.0. The `LICENSE` file is the Apache License, Version 2.0, January 2004 (head and tail read); GitHub classifies it as Apache-2.0 [1][2] |
| Trends | [Vectorless retrieval](../trends/reasoning-over-structure.md); [Infrastructure and MCP](../trends/infrastructure-and-mcp.md) |

## What it is

The README calls RAGFlow "a leading open-source Retrieval-Augmented Generation (RAG) engine" that fuses RAG with agent capabilities [3]. The GitHub description now reads "an agent-native database" that "grew into context infrastructure" [1]. GitHub lists Go as the language [1]. The 1.0.0-rc1 notes call that release a rewrite in Go, and they say the Python SDK (software development kit) is unaffected [4]. A hosted service exists at cloud.ragflow.io [3].

It is a platform rather than a library: the README describes a Web UI (user interface), a choice of document engines (Elasticsearch or Infinity) and pre-built agent templates [3][6].

*Reading:* That is why it appears under infrastructure as well as under retrieval over structure.

## How it works

**Ingestion.** The knowledge-compilation guide describes a pipeline Parser, Chunker, Compiler, Indexer. The Indexer builds the indexes used for retrieval. The README lists "deep document understanding" for Word, PowerPoint, Excel, PDF, scans and web pages, and template-based [chunking](../index/chunking.md) [3][5]. Elasticsearch is the default document engine in the Docker example; Infinity and others are supported [6].

**Knowledge compilation (20260819).** An LLM (large language model) turns documents into "artifacts" chosen by template. The overview guide lists six templates: Graph (entities and relations), Tree, PageIndex, Mindmap, Timeline and Wiki [5]; the README and the v0.27.0 notes add Skills as a seventh [3][4]. The same release deprecated the earlier [GraphRAG](../index/graphrag.md) and [RAPTOR](../index/raptor.md) features in the interface, replaced by Graph and Tree; content already generated "remains searchable" [4]. The PageIndex template builds a hierarchical index from a document's chapter structure [7]. The files read do not name the Vectify project of the same name, so any link to [PageIndex](./pageindex.md) is unstated.

**Retrieval.** The README names "multiple recall paired with fused re-ranking" ([hybrid search](../index/hybrid-search.md) with [reranking](../index/reranking.md)) [3]. Agentic retrieval arrived in v0.27.0 with four thinking modes; rc2 (20261016) replaced them with an Agentic mode, and rc3 added a decision model that judges whether evidence is sufficient inside the tool loop [4]. The README still lists the four modes [3].

**MCP.** RAGFlow is a [Model Context Protocol](../index/model-context-protocol.md) (MCP) server, exposing retrieval, dataset and chat-listing tools, and an MCP client, letting its agents call external servers [8].

## Evidence

None published, in the sources read. The README, the release notes and the compilation guides carry no benchmark table. The v0.27.2 notes claim that a refactor "significantly" improved "reasoning speed and benchmark performance", with no figures (first-party) [4]. Independent evaluations were not searched for: unstated.

## Status and direction

The repository is not archived [1]. The latest release is v1.0.0-rc3, published 20261030 11:53 UTC; the last stable release is v0.27.3, 20261023 [9]. Stars and activity are in the [watch-list table](./README.md).

1.0.0-rc1 (20260929) moved the queue from Redis to NATS, added Kvrocks for cache and checkpoints, and made the data upgrade from v0.27.2 irreversible [4]. Its known issues were CPU-only document parsing and no Team/Me permission model; rc2 added Team/Me sharing [4]. rc3 is called the final candidate before 1.0.0 [4].

The "ROADMAP 2026" issue is open and was last updated 20260715. It marks the unified knowledge compilation layer in v0.27.0 as done and lists backlog items such as more data sources and agent checkpoints [10]. A repository file says an enterprise build exists whose extensions are empty in the open-source tree; which features are enterprise-only is unstated [11].

*Reading:* RAGFlow is a large, fast-moving platform and not in maintenance mode: its latest release is a 1.0.0 candidate [4][9] and its roadmap issue is open [10]. Its compilation templates build trees and graphs with an LLM, as PageIndex does for trees. The structure features were reworked in August 2026 and the 1.0 line is still at release-candidate stage with an irreversible data upgrade, so its structure features are young.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)
- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)
- [Trends: what the field is doing now](../trends/README.md)
- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Projects**

- [Dify](dify.md)
- [PageIndex](pageindex.md)
- [Projects](README.md)

**Papers**

- [Papers: Agentic search over raw data](../papers/agentic-search.md)
- [Papers: Vectorless retrieval](../papers/reasoning-over-structure.md)

**Benchmarks**

- [EnterpriseRAG-Bench](../benchmarks/enterpriserag-bench.md)
- [FRAMES](../benchmarks/frames.md)

**Index**

- [Agent harness](../index/agent-harness.md)
- [Knowledge compilation](../index/knowledge-compilation.md)
- [RAPTOR](../index/raptor.md)
- [Tree index](../index/tree-index.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/infiniflow/ragflow : repository metadata through the GitHub API (licence field, archived flag, language, description) (read 20261102 20:09 UTC; archived flag re-read 20261102 20:30 UTC)
2. https://github.com/infiniflow/ragflow/blob/main/LICENSE : Apache License 2.0 text, through the API licence endpoint (read 20261102 20:10 UTC)
3. https://github.com/infiniflow/ragflow/blob/main/README.md : description, features, Latest Updates, hosted service, Web UI and agent templates, Skills in the artifact list (read 20261102 20:10 UTC; Skills entry re-read 20261102 20:30 UTC)
4. https://github.com/infiniflow/ragflow/blob/main/docs/release_notes.md : v0.27.0, v0.27.2, v1.0.0-rc1 to rc3 notes; the v0.27.0 line lists "To Skills" (read 20261102 20:11 UTC; re-read 20261102 20:30 UTC)
5. https://github.com/infiniflow/ragflow/blob/main/docs/guides/knowledge_compilation/overview.md : the six templates and the pipeline (read 20261102 20:11 UTC; re-read 20261102 20:30 UTC)
6. https://github.com/infiniflow/ragflow/blob/main/docs/develop/build_docker_image.mdx : document engines (read 20261102 20:11 UTC)
7. https://github.com/infiniflow/ragflow/blob/main/docs/guides/knowledge_compilation/built_in_templates_and_dedicated_configuration.md : the PageIndex template (read 20261102 20:11 UTC)
8. https://github.com/infiniflow/ragflow/blob/main/docs/develop/mcp/overview.md : MCP server and client roles (read 20261102 20:11 UTC)
9. https://github.com/infiniflow/ragflow/releases : tags, dates and stable/pre-release flags of v1.0.0-rc3 and v0.27.3, through the API releases endpoints (read 20261102 20:30 UTC)
10. https://github.com/infiniflow/ragflow/issues/12241 : "ROADMAP 2026" (read 20261102 20:11 UTC)
11. https://github.com/infiniflow/ragflow/blob/main/build_ee.sh : comment on the enterprise build (read 20261102 20:11 UTC)
