---
type: project
repo: langgenius/dify
trends: [infrastructure-and-mcp]
updated: 20261102 23:17 UTC
---

# Dify

Dify is a platform for building applications on [large language models](../index/large-language-model.md). This page says what its knowledge-base feature does, what the licence allows, and what has been measured.

| Field | Value |
|---|---|
| Repository | https://github.com/langgenius/dify |
| Licence | "Dify Open Source License", not an SPDX licence. The `LICENSE` file says Dify "is licensed under a modified version of the Apache License 2.0, with the following additional conditions" [2]. GitHub reports `NOASSERTION` (name "Other") [1][2] |
| Trends | [Infrastructure and MCP](../trends/infrastructure-and-mcp.md) |

## What it is

The README calls Dify "an open-source LLM app development platform" (large language model) that combines AI workflow, a RAG pipeline ([retrieval-augmented generation](../index/retrieval-augmented-generation.md)), [agent](../index/agent.md) capabilities, model management and observability [3]. Agents can use [MCP](../index/model-context-protocol.md) (Model Context Protocol) servers among other tools [3]. It comes as a hosted cloud, a self-hosted Community Edition and an Enterprise edition [3].

**Licence conditions.** Commercial use is allowed, but "a commercial license must be obtained from the producer" in two cases [2]. First, operating a multi-tenant environment from the source without written authorisation; one tenant is one workspace. Second, removing or modifying the logo or copyright information in the console or applications [2]. The producer "can adjust the open-source agreement to be more strict or relaxed" [2]. This documentation takes only ideas and results from it.

**Knowledge bases.** There are two kinds. The classic knowledge base lets users control chunking, indexing and search [11]. The Agent Knowledge Base, an opt-in beta in release 1.18.0, "reads, organizes, and indexes" content for the user [5][7]. Only the second is documented as building a [knowledge graph](../index/knowledge-graph.md) [9].

## How it works

**Classic.** Content is split into chunks ([chunking](../index/chunking.md)). The High Quality method turns chunks into vectors with an [embedding](../index/embedding.md) model; the Economical method uses 10 keywords per chunk and consumes no tokens, with lower accuracy [12]. The High Quality method offers [vector search](../index/vector-search.md), full-text search or [hybrid search](../index/hybrid-search.md); the Economical method offers only an inverted-index keyword search with TopK [12]. A [reranking](../index/reranking.md) model is off by default; the default TopK is 3 and the default score threshold 0.5, and both apply only when a rerank model is enabled [12].

**Agent Knowledge Base (beta).** The documentation (first-party) says a reasoning model reads each document and an embedding model makes it searchable [7]. The contents outline starts from the document's headings, the model adds sub-sections, and each section has a summary; chunks are capped at 1,200 characters [8]. At indexing the model "builds a knowledge graph: a map of the subjects each chunk mentions and how they connect" [9]. Three retrieval depths follow [9]:

| Depth | What the documentation says it does |
|---|---|
| Fast | matches the question against chunks by meaning and by keywords |
| Deep | wider than Fast; follows the knowledge graph to chunks about related subjects |
| Research | splits a complex question into sub-questions and uses section titles and summaries to pick sections |

The graph's schema, storage and traversal are unstated in the sources read. A code search of the repository for "graphrag" returned no hit; "knowledge graph" appears in two interface-string files [15]. The engine is a separate service, KnowledgeFS, kept in a standalone private repository [14]. The Dify repository holds the integration code (configuration, commands, upgrade tasks; 321 Python files match "knowledge_fs" [15]) and a pinned contract directory, which [14] says is all Dify's CI (continuous integration) needs. Default Compose installations keep it off, and it needs its own database [5].

**Access.** Knowledge is reached through a retrieval node in workflows, through agents (always at the Fast depth), through a Service API, and through a read-only command-line client for coding agents [10]. The access page does not mention MCP; the MCP page covers the other direction, exposing apps as MCP servers [10][13].

## Evidence

None published, in the sources read. The documentation, the README and the 1.18.0 notes carry no benchmark or measured results for either knowledge base. The documentation's "Compare the Two Kinds" table is a feature comparison, not a measurement (first-party) [17]. The notes describe an in-product "quality evaluation" view, also a feature, not a result (first-party) [5]. Independent evaluations were not searched: unstated. Papers: [Infrastructure and MCP](../papers/README.md).

## Status and direction

Active. The latest release is 1.18.0, published 20261023 06:33 UTC [4]. Three stable releases fall in the 90 days from 20260804: 1.17.0, 1.17.1 and 1.18.0 [4]. The commits API counts 2,515 commits on the default branch since 20260804 [6]. The repository is not archived [1].

The 1.18.0 headlines include portable `.ifpkg` app packages, nested workflow traces and the Agent Knowledge Base. The notes say the classic knowledge base "remains available" and that the new one is "an opt-in integration with a separate service and database" [5]. Opting in does not automatically migrate all classic datasets [5]. Some classic knowledge bases can be upgraded, with a copy built beside the original; external and pipeline-built ones cannot [17][18].

**Hosted tier.** Several 1.18.0 features are cloud-only: network access groups, agent templates and workflow-log archive deletion; the Agent Knowledge Base "will soon be available on cloud.dify.ai" [5].

**Roadmap.** No roadmap file is in the repository root; issues titled "roadmap" concern backend tests and modernisation, not product direction [16].

*Reading:* Dify is a general application platform, not a knowledge-graph tool. Its graph is new, in beta, partly closed (the engine is in a private repository) and described only in one-line statements. Treat it as a documentation claim until an independent test exists. Compare [RAGFlow](./ragflow.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)
- [Trends: what the field is doing now](../trends/README.md)
- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Projects**

- [Projects](README.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/langgenius/dify : repository metadata through the GitHub API (licence field, archived flag, description) (read 20261102 20:20 UTC)
2. https://github.com/langgenius/dify/blob/main/LICENSE : full licence text, read through the contents API; the API licence endpoint reports key "other", SPDX `NOASSERTION` (read 20261102 20:20 UTC)
3. https://github.com/langgenius/dify/blob/main/README.md : description, editions, agent features, licence section (read 20261102 20:20 UTC)
4. https://github.com/langgenius/dify/releases : releases API, latest release and the list since 20260211 (read 20261102 20:20 UTC)
5. https://github.com/langgenius/dify/releases/tag/1.18.0 : release notes: highlights, upgrade guide, cloud-only features, KnowledgeFS (read 20261102 20:21 UTC)
6. https://api.github.com/repos/langgenius/dify/commits?since=2026-08-04&per_page=1 : commits API, page count of the one-per-page listing (read 20261102 20:21 UTC)
7. https://docs.dify.ai/en/cloud/use-dify/knowledge-base/overview.md : Agent Knowledge Base overview and beta notice (read 20261102 20:22 UTC)
8. https://docs.dify.ai/en/cloud/use-dify/knowledge-base/review-indexed-documents.md : outline, section summaries, 1,200-character chunks (read 20261102 20:22 UTC)
9. https://docs.dify.ai/en/cloud/use-dify/knowledge-base/retrieval-settings.md : Fast, Deep and Research depths; knowledge graph at indexing (read 20261102 20:22 UTC)
10. https://docs.dify.ai/en/cloud/use-dify/knowledge-base/use-knowledge-in-apps.md : access through node, agents, Service API, command-line client; no MCP (read 20261102 20:22 UTC)
11. https://docs.dify.ai/en/use-dify/knowledge/readme.md : classic knowledge base overview (read 20261102 20:22 UTC)
12. https://docs.dify.ai/en/cloud/use-dify/knowledge/create-knowledge/setting-indexing-methods.md : index methods, retrieval strategies per method, defaults, rerank condition (read 20261102 20:35 UTC)
13. https://docs.dify.ai/en/cloud/use-dify/publish/publish-mcp.md : apps exposed as MCP servers (read 20261102 20:22 UTC)
14. https://github.com/langgenius/dify/blob/main/api/knowledge-fs-contract/README.md : KnowledgeFS as a "standalone private" repository, contract directory and its purpose; supports nothing about the rest of the repository (read 20261102 20:36 UTC)
15. https://api.github.com/search/code?q=graphrag+repo:langgenius/dify : no hit for "graphrag"; the same search for "knowledge graph" finds `web/i18n/locales/en-US/knowledge-tasks.json` and `knowledge-errors.json` (read 20261102 20:22 UTC). https://api.github.com/search/code?q=knowledge_fs+repo:langgenius/dify+extension:py : 321 Python hits, among them `api/configs/extra/knowledge_fs_config.py`, `api/commands/knowledge_fs.py`, `api/tasks/knowledge_fs_upgrade_tasks.py` (read 20261102 20:36 UTC)
16. https://github.com/langgenius/dify/issues?q=roadmap : issue search for "roadmap" in titles; the root listing is https://github.com/langgenius/dify (read 20261102 20:22 UTC)
17. https://docs.dify.ai/en/cloud/use-dify/knowledge/overview.md : the two kinds of knowledge base and the "Compare the Two Kinds" feature table; no measurements (read 20261102 20:35 UTC)
18. https://docs.dify.ai/en/cloud/use-dify/knowledge-base/upgrade-from-classic.md : upgrade leaves the classic one in place; external and pipeline-built ones cannot be upgraded (read 20261102 20:36 UTC)
