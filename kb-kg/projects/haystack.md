---
slug: haystack
repo: deepset-ai/haystack
tier: card
category: adjacent
snapshot: 20261030 19:45 UTC
---

# Haystack

| | |
|---|---|
| Repository | https://github.com/deepset-ai/haystack [1] |
| Licence | Apache-2.0, from the `LICENSE` file (Apache License 2.0 text, with the appendix notice "Copyright 2021 deepset GmbH") [2]. The README has a licence badge that links to the file and no licence section, so nothing disagrees [3]. |
| Language | Python (GitHub primary language) [1] |
| Stars, forks | 26,886, 3,368 (20261030 19:41 UTC; the [landscape snapshot](../landscape/20261030_1913-github/repos.tsv) of 20261030 19:13 UTC has the same figures) [1] |
| Created, last push | 20191114 09:05 UTC, 20261030 11:37 UTC [1] |
| Latest release | v3.4.1, 20261021 19:10 UTC [4] |
| Status | active (pushed the day of the read); the landscape snapshot raised no flag [1] |
| Paper, docs | no paper stated; docs at https://docs.haystack.deepset.ai [3] |

## What it is

Haystack, from deepset, is an open-source Python framework that its README calls an AI orchestration framework for LLM applications, with "explicit control over retrieval, routing, memory, and generation" [3]. It is a RAG and agent toolkit, not a knowledge base or a graph system: the user picks a Document Store, and the core package has no graph, entity or triple component (checked by file path names only, not exhaustively) [5][7]. Graph, memory and MCP features come as integrations kept in a separate repository (haystack-core-integrations) [9][11][12][13]. The README lists large organisations as users and sells a paid Haystack Enterprise (support, managed or self-hosted platform); both are the project's claims [3]. No benchmark appears in the README [3].

## How it works

A Pipeline connects components; an Agent runs a tool-calling loop [3]. Converters and splitters (recursive, hierarchical, Markdown header, embedding-based) feed embedders and a writer into a Document Store [7]. A Document holds text, blob, metadata, score and embeddings (dense or sparse) [8]. A store implements count, filter, write and delete; retrievers do the searching [5]. Core ships only an in-memory store [7]. FalkorDB stores documents as graph nodes with vector search; its text-to-OpenCypher retriever has a chat model write read-only queries against a sampled schema [9][10]. ArangoDB offers vector search in AQL [11]. A Cognee memory store writes to an LLM-extracted knowledge graph [12]. MCPToolset gives an Agent any MCP server's tools; Hayhooks serves pipelines over MCP or REST [3][13].

## Status and direction

Active. The default branch took 739 commits from 20260801 to 20261030 [6]. v3.0.0 came 20260720; six stable releases followed, v3.1.0 (20260824) to v3.4.1 (20261021), most after release candidates [4]. Recent subjects are fixes, documentation syncs and agent features; the FalkorDB text-to-Cypher retriever was documented on 20261029 [6]. Roadmap: unstated.

## Sources

1. https://github.com/deepset-ai/haystack : repository metadata via the GitHub API (stars, forks, licence field, dates, language) (read 20261030 19:41 UTC)
2. https://github.com/deepset-ai/haystack/blob/main/LICENSE : Apache License 2.0 text and appendix (read 20261030 19:42 UTC)
3. https://github.com/deepset-ai/haystack/blob/main/README.md : description, features, MCP and Hayhooks note, Enterprise offer (read 20261030 19:42 UTC)
4. https://github.com/deepset-ai/haystack/releases : v3.0.0 to v3.4.1 with release candidates (read 20261030 19:41 UTC)
5. https://github.com/deepset-ai/haystack/blob/main/docs-website/docs/concepts/document-store.mdx : Document Store protocol (read 20261030 19:43 UTC)
6. https://github.com/deepset-ai/haystack/commits/main : 739 commits since 20260801 and their subjects (read 20261030 19:43 UTC)
7. https://github.com/deepset-ai/haystack/tree/main/haystack : source layout (components, document_stores, retrievers, preprocessors, extractors) via the git trees API (read 20261030 19:45 UTC)
8. https://github.com/deepset-ai/haystack/blob/main/haystack/dataclasses/document.py : Document fields (read 20261030 19:43 UTC)
9. https://github.com/deepset-ai/haystack/blob/main/docs-website/docs/document-stores/falkordbdocumentstore.mdx : FalkorDB document store (read 20261030 19:43 UTC)
10. https://github.com/deepset-ai/haystack/blob/main/docs-website/docs/pipeline-components/retrievers/falkordbtexttocypherretriever.mdx : text-to-Cypher retriever (read 20261030 19:43 UTC)
11. https://github.com/deepset-ai/haystack/blob/main/docs-website/docs/document-stores/arangodocumentstore.mdx : ArangoDB document store (read 20261030 19:43 UTC)
12. https://github.com/deepset-ai/haystack/blob/main/docs-website/docs/memory-stores/cogneememorystore.mdx : Cognee memory store (read 20261030 19:43 UTC)
13. https://github.com/deepset-ai/haystack/blob/main/docs-website/docs/tools/mcptoolset.mdx : MCPToolset transports (read 20261030 19:43 UTC)
