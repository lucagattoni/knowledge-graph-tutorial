---
slug: ragflow
repo: infiniflow/ragflow
tier: card
category: adjacent
snapshot: 20261030 19:44 UTC
---

# RAGFlow

| | |
|---|---|
| Repository | https://github.com/infiniflow/ragflow [1] |
| Licence | Apache-2.0, from the `LICENSE` file (Apache License 2.0 text; head and tail read) [2]. The README badge and the GitHub field agree [1][3]. |
| Language | Go (GitHub primary language); the 1.0.0-rc1 notes call it a rewrite in Go, and the Python SDK is unaffected [1][5] |
| Stars, forks | 93,208, 11,183 (20261030 19:41 UTC; the 20261030 19:13 UTC landscape snapshot had 93,206 and 11,183) [1][11] |
| Created, last push | 20231212 06:13 UTC, 20261030 13:10 UTC [1] |
| Latest release | v1.0.0-rc3, 20261030 11:53 UTC; the last non-candidate release is v0.27.3, 20261023 [4] |
| Status | active (pushed within 90 days); not archived; no snapshot flag [1][11] |
| Paper, docs | no paper stated; docs in the repository `docs/` directory and at https://ragflow.io/docs [3][5] |

## What it is

RAGFlow describes itself as "a leading open-source Retrieval-Augmented Generation (RAG) engine that fuses cutting-edge RAG with Agent capabilities to create a superior context layer for LLMs" [3]. On GraphRAG its own documents say three things. A context-engine page lists GraphRAG ("extracting entity networks to find semantically distant connections") as a technique of its knowledge core [8]. The v0.27.0 notes (20260819) say the earlier GraphRAG and RAPTOR features "have been deprecated and are no longer available in the UI", replaced by Graph and Tree in Knowledge Compilation, and that previously generated content "remains searchable" [5]. The current README does not use the word GraphRAG; it lists "Graphs" among compilation outputs [3]. No benchmark or evaluation appears in the sources read: unstated.

## How it works

Files are parsed (layout analysis, OCR and table recognition by DeepDoc), split by a chunk template or a custom ingestion pipeline (Parser, Chunker, Compiler, Indexer), and optionally enriched by an LLM with keywords, questions, summaries and metadata; the Indexer builds embedding and full-text indexes [3][7]. Knowledge Compilation uses an LLM to produce Graph (entities and relations, with configurable types), Tree, PageIndex, Mindmap, Timeline and Wiki artifacts [6]. Retrieval pairs "multiple recall" with fused re-ranking, and Agentic RAG adds Low to Ultra thinking modes [3]. The Go server exposes retrieval, dataset and chat-listing tools as an MCP server, and agents can call external MCP servers [9].

## Status and direction

Active. 1.0.0-rc1 (20260929) is a rewrite in Go with the queue moved from Redis to NATS and an irreversible data upgrade; rc3 (20261030) is called the final candidate before 1.0.0 [5]. Known rc1 issues include CPU-only DeepDoc [5]. The "ROADMAP 2026" issue is open, last updated 20260715; its contents were not read [10]. Open: 899 issues, 409 pull requests [10].

## Sources

All read 20261030 19:41-19:44 UTC (the clock was checked before and after the reads, not per call).

1. https://github.com/infiniflow/ragflow : repository metadata via the GitHub API (stars, forks, licence field, dates, language)
2. https://github.com/infiniflow/ragflow/blob/main/LICENSE : Apache License 2.0 text
3. https://github.com/infiniflow/ragflow/blob/main/README.md : description, key features, latest updates, roadmap link, licence badge
4. https://github.com/infiniflow/ragflow/releases : release list and dates
5. https://github.com/infiniflow/ragflow/blob/main/docs/release_notes.md : v1.0.0-rc3, v1.0.0-rc1 and v0.27.0 notes, including the GraphRAG deprecation
6. https://github.com/infiniflow/ragflow/blob/main/docs/guides/knowledge_compilation/overview.md and built_in_templates_and_dedicated_configuration.md : compilation artifacts and the Graph template
7. https://github.com/infiniflow/ragflow/blob/main/docs/guides/dataset/dataset_overview.md and configuration.md : parsing, Extractor and Indexer settings
8. https://github.com/infiniflow/ragflow/blob/main/docs/basics/agent_context_engine.md : GraphRAG and TreeRAG as knowledge-core techniques
9. https://github.com/infiniflow/ragflow/blob/main/docs/develop/mcp/overview.md : MCP server and client roles
10. https://github.com/infiniflow/ragflow/issues/12241 : "ROADMAP 2026" metadata; open issue and pull request counts via the search API
11. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : first GitHub snapshot (20261030 19:13 UTC); flags column empty for this repository
