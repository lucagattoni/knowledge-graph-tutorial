---
type: chapter
updated: 20261103 01:55 UTC
---

# Projects

This chapter holds two things: a page for each project that passes the tests below, and a live watch list of every in-scope project the research has found. In scope means a project about [large language models](../index/large-language-model.md) (LLMs) and [agents](../index/agent.md) that create or query a [knowledge base](../index/knowledge-base.md) or a [knowledge graph](../index/knowledge-graph.md) [2]. A page says what the project is, how it works, who has measured it and where it stands. Stars are signals of attention, not verdicts of quality: the watch list shows them with the date of the snapshot, and no page ranks a project by them.

## Projects with a page

42 pages, grouped by the trend that uses the project as a representative [4]. Five of them (supermemory, TencentDB Agent Memory, Memori, memU and EverOS) were added at the owner's review of 20261103: they are the largest active agent-memory projects that had no page [6]. Each project is listed once. Where a page names more than one trend in its header, the first one decides the group, so a project can serve a trend whose group does not list it. The trend [Asking graphs in natural language](../trends/graph-query-generation.md) has no group of its own: [neo4j-graphrag-python](neo4j-graphrag-python.md) and [Code-Graph-RAG](code-graph-rag.md), listed under other trends, name it in their headers. Each line summarises the project's page, which carries the sources, the read times and the licence evidence. Licences come from the `LICENSE` file, not from a badge.

### [Graph-based RAG](../trends/graph-based-rag.md)

- [Microsoft GraphRAG](microsoft-graphrag.md): Microsoft's pipeline that extracts a graph from text, clusters it into community summaries and answers whole-corpus questions; its README puts it in maintenance mode (read 20261102). Licence: MIT.
- [LightRAG](lightrag.md): HKUDS [retrieval-augmented generation](../index/retrieval-augmented-generation.md) framework that builds a graph and vector index with dual-level keyword retrieval and no community summaries; latest release v1.5.7 (20260902). Licence: MIT.
- [HippoRAG](hipporag.md): builds an open-schema knowledge graph with an LLM and ranks passages with [Personalized PageRank](../index/personalized-pagerank.md), now centred on HippoRAG 2. Licence: MIT; its default [embedding](../index/embedding.md) model, NV-Embed-v2, is cc-by-nc-4.0.
- [RAG-Anything](rag-anything.md): multimodal framework built on LightRAG that parses PDFs, Office files and images into a cross-modal and a text graph; its capability has moved into LightRAG 1.5. Licence: MIT; its default parser, MinerU, is Apache-2.0 plus additional terms.
- [GraphRAG SDK](graphrag-sdk.md): FalkorDB's Python library that builds a knowledge graph from documents and answers from it; its authors report 71.48 overall on GraphRAG-Bench (first-party, SDK 1.3.0). Licence: Apache-2.0.
- [neo4j-graphrag-python](neo4j-graphrag-python.md): Neo4j's official Python package with vector, hybrid, text-to-[Cypher](../index/cypher.md) and tool retrievers plus an experimental LLM graph builder; no published evaluation. Licence: Apache License 2.0 with parts under the Python Software Foundation (PSF) licence version 2, which files are covered is unstated.

### [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md)

- [Neo4j LLM Knowledge Graph Builder](llm-graph-builder.md): Neo4j Labs web app that extracts a knowledge graph from documents with an LLM and offers seven chat modes over it; its own banner says it is no longer actively developed. Licence: Apache-2.0.
- [Hyper-Extract](hyper-extract.md): command-line tool and library that turns documents into nine kinds of knowledge structure (lists to [hypergraphs](../index/hypergraph.md)) from YAML templates; no published evaluation. Licence: the Apache License 2.0 text with 11 small wording changes.
- [GLiNER](gliner.md): a small encoder model family (50M to 0.3B parameters) for [named-entity](../index/named-entity-recognition.md) and [relation extraction](../index/relation-extraction.md) with run-time label sets. Licence: Apache-2.0.
- [OntoGPT](ontogpt.md): Monarch Initiative package whose SPIRES method has an LLM fill a user-supplied LinkML schema and grounds names to ontology terms. Licence: BSD-3-Clause.

### [Vectorless retrieval](../trends/reasoning-over-structure.md)

- [PageIndex](pageindex.md): builds a tree of a document's sections and lets an LLM read the tree to pick pages, with no vector index; its headline 98.7% FinanceBench figure is first-party and measures Mafin 2.5. Licence: MIT.
- [RAGFlow](ragflow.md): self-hosted RAG platform whose knowledge compilation (20260819) builds graphs, trees and PageIndex-style outputs with an LLM; no benchmark results in the sources read. Licence: Apache-2.0.

### [Agent memory](../trends/agent-memory.md)

- [Mem0](mem0.md): memory layer for LLM agents; its open-source library dropped the external graph store in April 2026 and the graph now lives only on the hosted platform. Licence: Apache-2.0.
- [Hindsight](hindsight.md): agent memory server with retain, recall and reflect over four parallel retrieval strategies; its benchmark claims are first-party and its baselines were not re-run. Licence: MIT.
- [Graphiti](graphiti.md): Zep's Python framework that builds a time-aware context graph for agents, with Kuzu deprecated and some Zep features kept out of the open code. Licence: Apache-2.0.
- [Cognee](cognee.md): Python memory platform that turns documents into a self-hosted graph with remember, recall, improve and forget; its published scores are first-party. Licence: Apache-2.0.
- [Letta](letta.md): grew out of MemGPT; its source now lives in letta-ai/letta-code, with memory kept as git-versioned Markdown files and updated by background runs. Licence: Apache-2.0, with a Brand Assets Exclusion for the Letta name and logos in letta-code.
- [MIRIX](mirix.md): sorts agent memory into six typed stores, each run by its own memory-manager agent. Licence: Apache-2.0; the notice reads "Copyright 2023, Letta authors".
- [OpenViking](openviking.md): a context database that keeps an agent's knowledge, memories and skills in one file tree with model-written summaries over a vector index; all published results are first-party. Licence: AGPL-3.0 for the main project (Apache-2.0 until 20260330); read-only reference.
- [Claude-Mem](claude-mem.md): memory plugin for coding agents that records tool use through hooks, compresses it with a model and injects it into later sessions; open core with hosted parts. Licence: Apache-2.0 since 20260508 (AGPL-3.0 from 20250911 to 20260508).
- [MemOS](memos.md): memory layer for LLM agents whose headline [LoCoMo](../datasets/locomo.md) and [LongMemEval](../datasets/longmemeval.md) scores come from its own organisation's framework, run on its hosted service. Licence: Apache-2.0.
- [Supermemory](supermemory.md): hosted memory and context layer whose public repository holds docs, an MCP server and plugins but not the engine; its headline LongMemEval figure moved from 81.6% to 97% and no independent run reproduces it. Licence: MIT for the repository; the self-hosted binary's licence is unstated.
- [TencentDB Agent Memory](tencentdb-agent-memory.md): Tencent's team-level memory hub that keeps four assets (chat memory, skills, a wiki and a code graph) per agent; one independent coding-task evaluation puts it among the leading rows with a gain of about 3.6 points over no memory. Licence: MIT (GitHub shows NOASSERTION).
- [Memori](memori.md): memory layer from Memori Labs with SDKs and a Rust core that sends conversations to the vendor's hosted augmentation endpoint by default, even with your own database; all published scores are first-party, and a competitor-run harness scores it far lower. Licence: reworded Apache 2.0 (GitHub shows NOASSERTION); read-only reference.
- [memU](memu.md): rewritten in 2026 as an embedding-only sidecar for desktop coding agents, where the host agent writes Markdown memories and the local service calls no model; its code reports usage events by default unless switched off (read from the code, not run), and its 92.09% LoCoMo claim is historical. Licence: Apache-2.0 text with an edited copyright grant (GitHub shows NOASSERTION).
- [EverOS](everos.md): renamed from EverMemOS; keeps agent memory as Markdown with SQLite and LanceDB indexes derived from it; first-party scores only, and competitor and third-party runs give lower or mixed figures. Licence: Apache-2.0, with one CC BY-NC test fixture excluded.

### [Plain files as agent knowledge](../trends/plain-file-knowledge.md)

- [LLM Wiki (nashsu)](llm-wiki-nashsu.md): Tauri desktop app that has a model write and maintain a folder of interlinked Markdown pages, following Karpathy's April 2026 gist; its one published result is first-party. Licence: GPL-3.0; read-only reference, no code reused.
- [claude-obsidian](claude-obsidian.md): Claude Code plugin that turns sources into a vault of linked, cited Markdown notes, written through hash-checked transactions with [BM25](../index/bm25.md) (Best Matching 25, a keyword ranking function) retrieval; no quality result is published. Licence: MIT.
- [Basic Memory](basic-memory.md): local-first Markdown store with a SQLite or Postgres index, hybrid search and an [MCP](../index/model-context-protocol.md) (Model Context Protocol) server; the only scores are the maintainers' own and show near-parity retrieval with mem0. Licence: AGPL-3.0.
- [agent-memory (Tigerless Labs)](tigerless-agent-memory.md): long-term agent memory kept as plain Markdown files, with BM25 recall and a sleep-time consolidation pass; all results first-party, none independent found on 20261102. Licence: MIT.

### [Code graphs for coding agents](../trends/code-knowledge-graphs.md)

- [Graphify](graphify.md): builds a knowledge graph of a code base (and docs, media) for coding agents to query without embeddings; benchmarks are first-party, and the README leads with a hosted product. Licence: Apache-2.0; earlier contributions MIT.
- [Understand Anything](understand-anything.md): plugin that turns a codebase into an explorable knowledge graph with a dashboard: a [tree-sitter](../index/tree-sitter.md) parser builds the structure and model agents add summaries and tours. Licence: MIT.
- [CodeGraph](codegraph.md): local SQLite code-graph index built with tree-sitter and served to coding agents over MCP; its README describes no model at index or query time, and its benchmark is first-party. Licence: MIT.
- [codebase-memory-mcp](codebase-memory-mcp.md): a C server that turns a repository into a local SQLite graph with 162 tree-sitter grammars and serves it over MCP; first-party results show a cost saving at some loss of answer quality. Licence: MIT.
- [code-review-graph](code-review-graph.md): Python package that keeps a tree-sitter graph on disk and returns the blast radius of a change over MCP; all published results are first-party. Licence: MIT.
- [Code-Graph-RAG](code-graph-rag.md): builds a code knowledge graph with Tree-sitter and no LLM, stores it in an embedded SQLite graph and exposes 37 MCP tools; its own agent tests tie grep with one model and trail it with another. Licence: MIT.

### [Infrastructure and MCP](../trends/infrastructure-and-mcp.md)

- [Neo4j](neo4j.md): the open-source Community Edition of the Neo4j [graph database](../index/graph-database.md) (a [property graph](../index/property-graph.md) with Cypher, vector and full-text indexes); clustering, backups and native VECTOR storage are Enterprise or Aura. Licence: GPL-3.0; read-only reference.
- [FalkorDB](falkordb.md): a graph database that runs as a Redis module, rewritten in Rust since 20260929 (6.0.0), with a first-party benchmark against Neo4j. Licence: the `LICENSE` file holds the Server Side Public License v1, then the Elastic License 2.0; which applies to what is unstated.
- [Memgraph](memgraph.md): an in-memory C++ graph database with built-in vector and text indexes, released every few weeks. Licence: the `LICENSE` file says the source is variously under the Business Source License 1.1 and the Memgraph Enterprise License; the Change Date is written 2030-21-10.
- [MCP reference servers](mcp-servers.md): reference implementations of the Model Context Protocol; its Memory server is a minimal JSON Lines knowledge graph with substring search, built as a teaching example. Licence: a composite `LICENSE` file with the Apache-2.0 and MIT texts and a CC-BY-4.0 documentation notice.
- [LlamaIndex](llama-index.md): general RAG and agent framework whose optional PropertyGraphIndex builds a property graph with pluggable extractors, retrievers and stores; the company's stated focus has shifted to hosted parsing. Licence: MIT.
- [Dify](dify.md): general LLM app platform whose 1.18.0 beta Agent Knowledge Base claims a knowledge graph built at indexing (first-party docs only); no published measurements. Licence: Dify Open Source License (modified Apache 2.0 with extra conditions); read-only reference, ideas and results only.

## How the list is chosen

A project gets a page when it passes test P-1, applied on 20261102. The test has two parts.

1. **Sustained activity.** The repository was pushed within 90 days of the GitHub snapshot of 20261030 19:54 UTC and is not archived [1]. 63 of the 77 projects in the archive pass [1].
2. **Use by a trend.** A trend of the [Trends](../trends/README.md) chapter uses the project as a representative of a distinct approach.

42 projects have a page: 37 passed both parts when the list was decided on 20261102, and five more were added at the owner's review of 20261103 [6]. The other 21 that pass the first part stay in the watch list, and each carries a reason in the note column: a judgement of this documentation, written on 20261103 by applying the test to the project's archive entry, not a statement by the project [6][7]. Two of them are arguable, and their notes say so: [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format), which the plain-files trend lists as a representative though it is a specification, not software, and [Semantica](https://github.com/semantica-agi/semantica), which has 14,349 stars in the snapshot against 5,289 for the most-starred project with a page under the construction trend. One page passes the first part narrowly: [Neo4j LLM Knowledge Graph Builder](llm-graph-builder.md) was pushed one day before the snapshot, but has one commit on its default branch in the 90 days, and its banner says it is no longer actively developed [1].

### Quiet projects that stay in the watch list

Thirteen projects of the archive fail the first part (more than 90 days since the last push), and one is archived [1]. A quiet repository can be finished rather than abandoned; the snapshot's own text says "Mature, finished projects can look like this" [1]. These stay in the watch list, and their trend page or papers group tells the idea.

| Project | Days since last push (snapshot 20261030) | Told in |
|---|---|---|
| [Graph-R1](../../kb-kg/projects/graph-r1.md) | 182 | [Agentic graph retrieval](../trends/learned-graph-traversal.md) |
| [Youtu-GraphRAG](../../kb-kg/projects/youtu-graphrag.md) | 246 | [Agentic graph retrieval](../trends/learned-graph-traversal.md), [Graph-based RAG](../trends/graph-based-rag.md) |
| [LinearRAG](../../kb-kg/projects/linearrag.md) | 117 | [Graph-based RAG](../trends/graph-based-rag.md) |
| [MiniRAG](../../kb-kg/projects/minirag.md) | 379 | [Graph-based RAG](../trends/graph-based-rag.md) |
| [fast-graphrag](../../kb-kg/projects/fast-graphrag.md) | 362 | [Graph-based RAG](../trends/graph-based-rag.md) |
| [nano-graphrag](../../kb-kg/projects/nano-graphrag.md) | 276 | [Graph-based RAG](../trends/graph-based-rag.md) |
| [KAG](../../kb-kg/projects/kag.md) | 275 | [Graph-based RAG](../trends/graph-based-rag.md) |
| [datastax graph-rag](../../kb-kg/projects/datastax-graph-rag.md) | 543 | [Graph-based RAG](../trends/graph-based-rag.md) |
| [DeepKE](../../kb-kg/projects/deepke.md) | 109 | [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md) |
| [LogicRAG](../../kb-kg/projects/logicrag.md) | 103 | [Vectorless retrieval](../trends/reasoning-over-structure.md) |
| [OpenKB](../../kb-kg/projects/openkb.md) | 100 | [Plain files as agent knowledge](../trends/plain-file-knowledge.md), [Vectorless retrieval](../trends/reasoning-over-structure.md) |
| [karpathy-llm-wiki](../../kb-kg/projects/karpathy-llm-wiki.md) | 99 | [Plain files as agent knowledge](../trends/plain-file-knowledge.md) |
| [A-mem](../../kb-kg/projects/a-mem.md) | 321 | [Agent memory](../trends/agent-memory.md) |
| [Kuzu](../../kb-kg/projects/kuzu.md) | archived; last push 20251010 | [Infrastructure and MCP](../trends/infrastructure-and-mcp.md), [Graph features removed and added](../trends/features-in-and-out.md) |

Kuzu is an embedded graph database that its owners archived: GitHub showed it archived, last pushed 20251010, on 20261102 21:03 UTC [3]. The [Graphiti](graphiti.md) page records that Graphiti has deprecated its Kuzu back end, so Kuzu is told as a dated removal in the features trend and not as a project to follow.

### Trends without a project page

- **[Agentic graph retrieval](../trends/learned-graph-traversal.md)** has papers but no project that passes both parts. Graph-R1 and Youtu-GraphRAG are quiet (above). Four other repositories of this trend were last pushed long before the snapshot of 20261030 19:54 UTC, counted in days to it: Think-on-Graph (DataArcTech/ToG) 950 days [1], GraphSearch 204 days, GraphRAG-R1 244 days and Search-R1 350 days (the last three are not in the snapshot, so their push dates were read live) [3]. GFM-RAG was pushed on 20260908 [1][3], inside the 90 days, but it has no archive entry and so no page; whether it would pass the second part is unstated. The evidence is in the [papers group](../papers/learned-graph-traversal.md).
- **[Agentic search over raw data](../trends/agentic-search.md)** is the approach of building nothing: the agent searches the raw files. The trends research found no snapshot project that matches (the match is unstated beyond that), and no watch-list row carries this trend [5]. The evidence is in the [papers group](../papers/agentic-search.md).

## Watch list

The table is generated from [watchlist.tsv](watchlist.tsv) and the newest GitHub snapshot, and links to a page where one exists.

<!-- BEGIN GENERATED: watchlist -->

Stars, last push, licence (GitHub's detection of the LICENSE file) and flags come from the GitHub snapshot taken 20261030 19:54 UTC (kb-kg/landscape/20261030_1954-github/). Stars are a signal, not a verdict.

| Project | Category | Trends | Stars | Last push | Licence | Flags | Note |
|---|---|---|---|---|---|---|---|
| [Dify](dify.md) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 160,020 | 20261030 | NOASSERTION | none |  |
| [Graphify](graphify.md) | adjacent | [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md), [Graph features removed and added](../trends/features-in-and-out.md) | 139,374 | 20261027 | Apache-2.0 | fast-growth |  |
| [RAGFlow](ragflow.md) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md), [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md) | 93,209 | 20261030 | Apache-2.0 | none |  |
| [MCP reference servers](mcp-servers.md) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 91,700 | 20261029 | NOASSERTION | none |  |
| [Understand Anything](understand-anything.md) | adjacent | [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md) | 89,048 | 20261026 | MIT | fast-growth |  |
| [CodeGraph](codegraph.md) | adjacent | [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md) | 76,004 | 20261030 | MIT | fast-growth |  |
| [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 67,758 | 20261030 | MIT | none | No page: judged adjacent: document-chat application with vector retrieval only, and the entry found no knowledge-graph feature; a general platform like dify, whose graph is at least claimed in beta |
| [LlamaIndex](llama-index.md) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md), [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 52,747 | 20261026 | MIT | none |  |
| [codebase-memory-mcp](codebase-memory-mcp.md) | adjacent | [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md) | 47,853 | 20261029 | MIT | fast-growth |  |
| [khoj-ai/khoj](https://github.com/khoj-ai/khoj) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 37,907 | 20260802 | AGPL-3.0 | none | No page: judged adjacent: personal document search and chat app on pgvector, no graph found; AGPL-3.0; pushed 89 days before the snapshot (the 90-day edge), 2 commits in 90 days |
| [surrealdb/surrealdb](https://github.com/surrealdb/surrealdb) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 33,253 | 20261029 | NOASSERTION | none | No page: judged adjacent: multi-model database where graph is one model; like memgraph, offers graph, vector and text indexes; BSL 1.1; the infrastructure trend lists it only as also named |
| [code-review-graph](code-review-graph.md) | adjacent | [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md) | 32,509 | 20261029 | MIT | none |  |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 26,886 | 20261030 | Apache-2.0 | none | No page: judged adjacent: general RAG and agent framework like llama-index; no graph component in core (path names only); graph, memory and MCP arrive as integrations in a separate repository |
| [Neo4j](neo4j.md) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 17,378 | 20261023 | GPL-3.0 | none |  |
| [FalkorDB](falkordb.md) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 10,507 | 20261030 | NOASSERTION | none |  |
| [HelixDB/helix-db](https://github.com/HelixDB/helix-db) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 6,255 | 20261030 | Apache-2.0 | none | graph-vector database |
| [potpie-ai/potpie](https://github.com/potpie-ai/potpie) | adjacent | [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md) | 5,782 | 20261030 | Apache-2.0 | none |  |
| [Code-Graph-RAG](code-graph-rag.md) | adjacent | [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md), [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md) | 5,303 | 20261030 | MIT | none |  |
| [Memgraph](memgraph.md) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 4,636 | 20261030 | NOASSERTION | none |  |
| [kuzudb/kuzu](https://github.com/kuzudb/kuzu) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md), [Graph features removed and added](../trends/features-in-and-out.md) | 4,018 | 20251010 | MIT | archived,quiet |  |
| [NVIDIA/skills](https://github.com/NVIDIA/skills) | adjacent | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 3,799 | 20261030 | Apache-2.0 | none | skills |
| [redhat-et/ripwire](https://github.com/redhat-et/ripwire) | adjacent | [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md) | 2,495 | 20261030 | Apache-2.0 | none | deterministic call graph |
| [zzet/gortex](https://github.com/zzet/gortex) | adjacent | [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md) | 1,948 | 20261030 | Apache-2.0 | none |  |
| [HelixDB/helix-foundry](https://github.com/HelixDB/helix-foundry) | adjacent | [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md) | 1,854 | 20261030 | Apache-2.0 | none | agent drafts the ontology; created 20261007 |
| [ModernRelay/omnigraph](https://github.com/ModernRelay/omnigraph) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 1,818 | 20261030 | MIT | none |  |
| [GrafeoDB/grafeo](https://github.com/GrafeoDB/grafeo) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 826 | 20261030 | Apache-2.0 | none |  |
| [Pometry/Raphtory](https://github.com/Pometry/Raphtory) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 650 | 20261030 | GPL-3.0 | none | temporal graph engine |
| [turing-db/turingdb](https://github.com/turing-db/turingdb) | adjacent | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 188 | 20261030 | NOASSERTION | none |  |
| [Claude-Mem](claude-mem.md) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 105,979 | 20261030 | Apache-2.0 | fast-growth |  |
| [Mem0](mem0.md) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md), [Graph features removed and added](../trends/features-in-and-out.md) | 68,112 | 20261029 | Apache-2.0 | none |  |
| [Hindsight](hindsight.md) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 56,614 | 20261030 | MIT | fast-growth |  |
| [OpenViking](openviking.md) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md), [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 41,197 | 20261030 | AGPL-3.0 | none |  |
| [Cognee](cognee.md) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 32,934 | 20261030 | Apache-2.0 | none |  |
| [Graphiti](graphiti.md) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md), [Graph features removed and added](../trends/features-in-and-out.md) | 32,373 | 20261028 | Apache-2.0 | none |  |
| [Supermemory](supermemory.md) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 31,471 | 20261029 | MIT | none |  |
| [TencentDB Agent Memory](tencentdb-agent-memory.md) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 30,258 | 20261028 | NOASSERTION | none |  |
| [Letta](letta.md) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 25,294 | 20261018 | Apache-2.0 | none |  |
| [Memori](memori.md) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 17,241 | 20261003 | NOASSERTION | none |  |
| [memU](memu.md) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md), [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 14,581 | 20261030 | NOASSERTION | none |  |
| [EverOS](everos.md) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md), [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 13,721 | 20261030 | Apache-2.0 | none |  |
| [MemOS](memos.md) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 12,200 | 20261029 | Apache-2.0 | none |  |
| [plastic-labs/honcho](https://github.com/plastic-labs/honcho) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 7,837 | 20261030 | AGPL-3.0 | none | No page: judged no distinct approach: background workers extract and consolidate conclusions from stored messages, like hindsight's retain and consolidation; differs by modelling peers (people or agents); AGPL-3.0, read-only reference |
| [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) | agent-memory | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 5,061 | 20261028 | MIT | none |  |
| [getzep/zep](https://github.com/getzep/zep) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md), [Graph features removed and added](../trends/features-in-and-out.md) | 4,984 | 20261020 | Apache-2.0 | none | No page: judged not a representative: the repository holds examples for hosted Zep Cloud and no maintained engine (that is graphiti); the features trend tells its 20250402 demotion |
| [MIRIX](mirix.md) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 3,456 | 20261028 | Apache-2.0 | none |  |
| [MemMachine/MemMachine](https://github.com/MemMachine/MemMachine) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 3,078 | 20261029 | Apache-2.0 | none | No page: judged no distinct approach: layered agent memory (episodic, profile, working) with LLM-extracted profile features, like mirix's typed stores; adds a query-routing retrieval agent; README gives no benchmark results |
| [Dataojitori/nocturne_memory](https://github.com/Dataojitori/nocturne_memory) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 1,412 | 20260922 | MIT | none |  |
| [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 1,212 | 20251212 | MIT | quiet |  |
| [EverMind-AI/SkillCorpus](https://github.com/EverMind-AI/SkillCorpus) | agent-memory | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 694 | 20261029 | Apache-2.0 | none | skills |
| [syncable-dev/memtrace-public](https://github.com/syncable-dev/memtrace-public) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 509 | 20261030 | NOASSERTION | none | bi-temporal graph, no LLM calls |
| [varun29ankuS/shodh-memory](https://github.com/varun29ankuS/shodh-memory) | agent-memory | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 316 | 20261026 | Apache-2.0 | none | LLM-free memory |
| [memoket/memoket-kite](https://github.com/memoket/memoket-kite) | agent-memory | [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md) | 230 | 20261030 | Apache-2.0 | none | vector-free |
| [LightRAG](lightrag.md) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md), [Graph features removed and added](../trends/features-in-and-out.md) | 40,443 | 20261029 | MIT | none |  |
| [PageIndex](pageindex.md) | core | [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md) | 39,913 | 20261029 | MIT | none |  |
| [Microsoft GraphRAG](microsoft-graphrag.md) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md), [Graph features removed and added](../trends/features-in-and-out.md) | 36,498 | 20261029 | MIT | none |  |
| [RAG-Anything](rag-anything.md) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 24,322 | 20261028 | MIT | none |  |
| [semantica-agi/semantica](https://github.com/semantica-agi/semantica) | core | [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md) | 14,349 | 20261030 | MIT | none | No page: judged no distinct approach: ontology-grounded context graph, a subsection the construction trend merges, naming four other projects; bi-temporal facts as in graphiti, plus OWL and SHACL; page arguable |
| [OpenSPG/KAG](https://github.com/OpenSPG/KAG) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 9,140 | 20260128 | Apache-2.0 | quiet |  |
| [xerrors/Yuxi](https://github.com/xerrors/Yuxi) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 7,557 | 20261029 | MIT | none | No page: judged adjacent: multi-tenant agent platform; the knowledge graph is one of six modules, built into Neo4j by a separate administrator job; README credits LightRAG for early graph ideas |
| [Neo4j LLM Knowledge Graph Builder](llm-graph-builder.md) | core | [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md), [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 5,289 | 20261029 | Apache-2.0 | none |  |
| [FlowElement-xinliuyuansu/m_flow](https://github.com/FlowElement-xinliuyuansu/m_flow) | core | [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md), [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 4,510 | 20260901 | Apache-2.0 | none | No page: judged no distinct approach: LLM-built graph and vector memory like cognee, whose patterns its NOTICE acknowledges; adds a cone graph; one commit in 90 days (snapshot) |
| [zjunlp/DeepKE](https://github.com/zjunlp/DeepKE) | core | [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md) | 4,487 | 20260713 | MIT | quiet |  |
| [Hyper-Extract](hyper-extract.md) | core | [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md) | 4,207 | 20261029 | NOASSERTION | none |  |
| [GLiNER](gliner.md) | core | [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md) | 4,184 | 20261024 | Apache-2.0 | none |  |
| [HippoRAG](hipporag.md) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md), [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 4,083 | 20261006 | MIT | none |  |
| [gusye1234/nano-graphrag](https://github.com/gusye1234/nano-graphrag) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 4,006 | 20260127 | MIT | quiet |  |
| [circlemind-ai/fast-graphrag](https://github.com/circlemind-ai/fast-graphrag) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 3,967 | 20251101 | MIT | quiet |  |
| [robert-mcdermott/ai-knowledge-graph](https://github.com/robert-mcdermott/ai-knowledge-graph) | core | [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md) | 3,134 | 20260913 | Apache-2.0 | none | No page: judged no distinct approach: command-line tool turning text into LLM-extracted triples and an HTML graph, like hyper-extract; no database; no default-branch commits 202601 to 202608; 24 in 202609 |
| [pingcap/autoflow](https://github.com/pingcap/autoflow) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 2,978 | 20261023 | Apache-2.0 | none | pushed recently, no commits in 90 days |
| [trustgraph-ai/trustgraph](https://github.com/trustgraph-ai/trustgraph) | core | [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md) | 2,854 | 20261028 | Apache-2.0 | none | No page: judged no distinct approach: ontology-grounded context graph with access policies, the kind the construction trend's merged subsection covers; ontology-guided extraction like ontogpt; only an ingest-speed benchmark |
| [raphaelmansuy/edgequake](https://github.com/raphaelmansuy/edgequake) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 2,292 | 20261030 | Apache-2.0 | none |  |
| [HKUDS/MiniRAG](https://github.com/HKUDS/MiniRAG) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 2,026 | 20251016 | MIT | quiet |  |
| [neo4j-graphrag-python](neo4j-graphrag-python.md) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md), [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md) | 1,326 | 20261030 | NOASSERTION | none |  |
| [apecloud/ApeRAG](https://github.com/apecloud/ApeRAG) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 1,318 | 20261029 | Apache-2.0 | none | multimodal |
| [stair-lab/kg-gen](https://github.com/stair-lab/kg-gen) | core | [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md) | 1,289 | 20260324 | unstated | quiet |  |
| [TencentCloudADP/youtu-graphrag](https://github.com/TencentCloudADP/youtu-graphrag) | core | [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md), [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 1,271 | 20260226 | NOASSERTION | quiet |  |
| [OntoGPT](ontogpt.md) | core | [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md) | 1,080 | 20260910 | BSD-3-Clause | none |  |
| [GraphRAG SDK](graphrag-sdk.md) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 1,029 | 20261030 | Apache-2.0 | none |  |
| [orneryd/NornicDB](https://github.com/orneryd/NornicDB) | core | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 920 | 20261030 | MIT | none |  |
| [HKUST-KnowComp/AutoSchemaKG](https://github.com/HKUST-KnowComp/AutoSchemaKG) | core | [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md) | 845 | 20260429 | MIT | quiet | schema induction |
| [DataArcTech/ToG](https://github.com/DataArcTech/ToG) | core | [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md) | 666 | 20240324 | unstated | quiet | Think-on-Graph |
| [FengZhenfei/carrel](https://github.com/FengZhenfei/carrel) | core | [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md) | 653 | 20261027 | MIT | none | created 2026 |
| [benmaster82/Kwipu](https://github.com/benmaster82/Kwipu) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 612 | 20261022 | MIT | none |  |
| [LHRLAB/Graph-R1](https://github.com/LHRLAB/Graph-R1) | core | [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md) | 599 | 20260430 | MIT | quiet |  |
| [DEEP-PolyU/LinearRAG](https://github.com/DEEP-PolyU/LinearRAG) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 566 | 20260705 | GPL-3.0 | quiet |  |
| [liliang-cn/cortexdb](https://github.com/liliang-cn/cortexdb) | core | [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md) | 474 | 20261029 | MIT | none |  |
| [OpenDCAI/DataMind](https://github.com/OpenDCAI/DataMind) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 456 | 20261023 | Apache-2.0 | none | multimodal |
| [databrickslabs/ontobricks](https://github.com/databrickslabs/ontobricks) | core | [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md) | 455 | 20261030 | NOASSERTION | none | ontology-first |
| [awslabs/graphrag-toolkit](https://github.com/awslabs/graphrag-toolkit) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 451 | 20261030 | Apache-2.0 | none | vendor toolkit |
| [bibinprathap/VeritasGraph](https://github.com/bibinprathap/VeritasGraph) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 326 | 20261030 | MIT | none |  |
| [RManLuo/gfm-rag](https://github.com/RManLuo/gfm-rag) | core | [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md) | 309 | 20260908 | Apache-2.0 | none | graph foundation model retriever |
| [zilliztech/vector-graph-rag](https://github.com/zilliztech/vector-graph-rag) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 263 | 20261016 | MIT | none | LLM triplet extraction, no graph database |
| [neo4j-labs/text2cypher](https://github.com/neo4j-labs/text2cypher) | core | [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md) | 245 | 20261009 | CC0-1.0 | none | datasets and evaluations |
| [chensyCN/LogicRAG](https://github.com/chensyCN/LogicRAG) | core | [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md) | 241 | 20260719 | GPL-3.0 | quiet |  |
| [stevereiner/flexible-graphrag](https://github.com/stevereiner/flexible-graphrag) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 196 | 20261024 | Apache-2.0 | none |  |
| [apache/hugegraph-ai](https://github.com/apache/hugegraph-ai) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 144 | 20261029 | Apache-2.0 | none |  |
| [RaguTeam/RAGU](https://github.com/RaguTeam/RAGU) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 143 | 20261004 | MIT | none |  |
| [namidb/namidb](https://github.com/namidb/namidb) | core | [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md) | 120 | 20261029 | NOASSERTION | none |  |
| [neo4j-contrib/neo4j-skills](https://github.com/neo4j-contrib/neo4j-skills) | core | [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md), [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 118 | 20261026 | MIT | none |  |
| [datastax/graph-rag](https://github.com/datastax/graph-rag) | core | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 91 | 20250505 | Apache-2.0 | quiet |  |
| [DataArcTech/GraphSearch](https://github.com/DataArcTech/GraphSearch) | core | [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md) | not in snapshot | n/a | n/a | n/a | research code |
| [PeterGriffinJin/Search-R1](https://github.com/PeterGriffinJin/Search-R1) | core | [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md) | not in snapshot | n/a | n/a | n/a | plain-text baseline |
| [ycygit/GraphRAG-R1](https://github.com/ycygit/GraphRAG-R1) | core | [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md) | not in snapshot | n/a | n/a | n/a | research code |
| [LLM Wiki (nashsu)](llm-wiki-nashsu.md) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 21,198 | 20261021 | NOASSERTION | none |  |
| [claude-obsidian](claude-obsidian.md) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 16,002 | 20261025 | MIT | none |  |
| [breferrari/obsidian-mind](https://github.com/breferrari/obsidian-mind) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 5,460 | 20261017 | MIT | none | No page: judged no distinct approach: Obsidian vault of Markdown notes that an agent writes, as in claude-obsidian; adds lifecycle hooks that inject notes into sessions and work-oriented templates |
| [VectifyAI/OpenKB](https://github.com/VectifyAI/OpenKB) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md), [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md) | 4,831 | 20260722 | Apache-2.0 | quiet |  |
| [inkeep/open-knowledge](https://github.com/inkeep/open-knowledge) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 4,741 | 20261030 | GPL-3.0 | none | No page: judged no distinct approach: Markdown files under git with BM25 search and an MCP server, like basic-memory; editor and desktop app, no LLM index step; GPL-3.0, read-only reference |
| [Basic Memory](basic-memory.md) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 4,416 | 20261030 | AGPL-3.0 | none |  |
| [agent-memory (Tigerless Labs)](tigerless-agent-memory.md) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md), [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 4,381 | 20261030 | MIT | none |  |
| [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 3,667 | 20261026 | MIT | none | No page: judged no distinct approach: coding-agent skill writing an interlinked Markdown wiki from raw sources, like claude-obsidian; adds a wikilink graph and health check; last non-bot commit 20260917 |
| [Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 3,641 | 20261027 | MIT | none | No page: judged no distinct approach: agent skills turning notes and sessions into a linked Obsidian vault, like claude-obsidian; adds a manifest that skips unchanged sources; its test is first-party |
| [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 2,643 | 20260723 | MIT | quiet |  |
| [atomicstrata/llm-wiki-compiler](https://github.com/atomicstrata/llm-wiki-compiler) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 2,225 | 20261019 | MIT | none | No page: judged no distinct approach: program with its own LLM pipeline compiling sources into a cited Markdown wiki, like llm-wiki-nashsu; command line and SDK instead of a desktop app |
| [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 1,734 | 20261029 | Apache-2.0 | none | No page: judged no distinct approach: web app and Chrome extension letting Claude write a Markdown wiki through ten MCP tools, like claude-obsidian; local or hosted; no releases or tags |
| [yuezhiai/jonex](https://github.com/yuezhiai/jonex) | markdown-kb | [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md) | 1,522 | 20261028 | NOASSERTION | none | multimodal |
| [GoogleCloudPlatform/open-knowledge-format](https://github.com/GoogleCloudPlatform/open-knowledge-format) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 1,177 | 20260821 | Apache-2.0 | none | No page: judged a specification, not software: six commits, one account, no release; the plain-file trend gives it its own section and lists it, so a page is arguable |
| [undefined-ui/second-brain-os](https://github.com/undefined-ui/second-brain-os) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 1,167 | 20261014 | MIT | none |  |
| [kiwifs/kiwifs](https://github.com/kiwifs/kiwifs) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 870 | 20261028 | NOASSERTION | none | No page: judged no distinct approach: Markdown files as source of truth with SQLite search and an MCP server, like basic-memory; adds NFS, S3, WebDAV and FUSE access; BSL 1.1 |
| [okf-memory/okf-agent-memory](https://github.com/okf-memory/okf-agent-memory) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md), [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md) | 846 | 20261029 | MIT | none | No page: judged no distinct approach: agent memory as Markdown files with BM25 recall, like tigerless-agent-memory; adds the OKF v0.2 format and MCP server; created 20260905, no embeddings or database |
| [ussumant/llm-wiki-compiler](https://github.com/ussumant/llm-wiki-compiler) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 329 | 20260821 | MIT | none |  |
| [crow-hq/llm-wiki-v2](https://github.com/crow-hq/llm-wiki-v2) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 250 | 20261028 | AGPL-3.0 | none |  |
| [Emmimal/wiki-compiler](https://github.com/Emmimal/wiki-compiler) | markdown-kb | [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md) | 111 | 20260914 | MIT | none | zero LLM calls |

<!-- END GENERATED: watchlist -->

## Left out

The archive's selection page of 20261030 19:22 UTC lists the repositories its snapshot returned that are out of scope, and why [2]. Condensed:

| Reason the selection gives | Repositories |
|---|---|
| A book | ai-agent-book |
| Tutorials and guides | hello-agents, AgentGuide, happy-llm |
| A converter that turns a book into a skill | book-to-skill |
| General databases | TiDB, Dolt |
| A chat interface | Open WebUI |
| Agent frameworks | LangChain, LangGraph |
| A crawler, a low-code platform, an answer engine | crawl4ai, JeecgBoot, Vane |
| A screen recorder; context compression | screenpipe; headroom |
| A swarm-intelligence prediction engine, not a knowledge base | MiroFish |
| Coding-agent tooling, a security agent, assistants, an agent runtime, an unclear "world model" | five smaller repositories, named on the selection page |
| Awesome lists | used as sources for the papers survey, not as entries |
| Borderline: could be promoted to a page or a watch-list row on request | Milvus (a vector database), Onyx, Quivr, WeKnora, xerj, NebulaGraph, R2R (quiet) |

Several of these have more stars than most projects with a page: the selection page gives Open WebUI 157,264 and LangChain 148,720 stars at 20261030 [2]. Stars did not decide scope. The repository descriptions read on GitHub on 20261102 20:50 UTC are consistent with these reasons for the 23 repositories named in the table [3].

## Changes

The latest changes to this chapter, newest first: projects added, updated, settled, faded or removed.

<!-- BEGIN GENERATED: changes -->

| Date | Kind | Subject | Summary | Source |
|---|---|---|---|---|
| 20261103 | added | Supermemory | Project page added: MIT repository without the engine; the LongMemEval headline moved from 81.6 to 95 to 97 percent; one independent coding-task run. | [source](https://github.com/supermemoryai/supermemory) |
| 20261103 | added | TencentDB Agent Memory | Project page added: MIT licence (GitHub shows NOASSERTION); two branches; first-party results; one independent evaluation (MemDev-Bench). | [source](https://github.com/TencentCloud/TencentDB-Agent-Memory) |
| 20261103 | added | Memori | Project page added: reworded Apache 2.0 licence (GitHub shows NOASSERTION); conversations go to the vendor hosted service by default; first-party LoCoMo 81.95 (paper) and 87.0 (website) against 41.34 in a competitor-run harness. | [source](https://github.com/MemoriLabs/Memori) |
| 20261103 | added | memU | Project page added: embedding-only sidecar for coding agents; the 92.09 percent LoCoMo claim is historical; four third-party runs by rivals, none of the current service; Apache-2.0 text with an edited grant. | [source](https://github.com/NevaMind-AI/memU) |
| 20261103 | added | EverOS | Project page added: Apache-2.0 agent memory runtime renamed from EverMemOS; first-party scores only on LoCoMo and LongMemEval; competitor and third-party runs give lower or mixed figures. | [source](https://github.com/EverMind-AI/EverOS) |
| 20261103 | updated | watch list | The 21 active projects without a page now carry a reason in the note column (a judgement of this documentation). | docs/projects/watchlist.tsv |
| 20261103 | updated | five new project pages | A second agent re-read the primary sources of each page and corrected errors before the pages were merged (for example Memori: licence word-diff and the unmerged branch; memU: the wording of the event reporting and the licence; EverOS: which judge model scored which benchmark; TencentDB Agent Memory: update and forget; Supermemory: a dropped sentence in the vendor report). | docs/projects/README.md |
| 20261102 | added | chapter | First edition: 37 project pages and a watch list of 123 repositories, joined with the GitHub snapshot of 20261030 19:54 UTC. | docs/projects/README.md |

Full list: [changes.tsv](changes.tsv)

<!-- END GENERATED: changes -->

## Sources

1. [kb-kg/landscape/20261030_1954-github/README.md](../../kb-kg/landscape/20261030_1954-github/README.md) and its `repos.tsv` : how the snapshot ranks and flags repositories (the `quiet` flag is more than 90 days since the last push); days since last push, archived flag and commits in 90 days of each archive project; the counts of 63 of 77 and 37 are this documentation's own tally of the file (read 20261102 20:47 to 20:52 UTC).
2. [kb-kg/landscape/20261030_1922-selection.md](../../kb-kg/landscape/20261030_1922-selection.md) : the "Left out, and why" table, the borderline list and the star counts of 20261030 (read 20261102 20:47 UTC).
3. GitHub repository metadata through the authenticated CLI (`gh api repos/OWNER/NAME`) : Kuzu archived and last push 20251010 (read 20261102 21:03 UTC); last push of GFM-RAG 20260908 (read 20261102 21:03 UTC); last push of GraphSearch 20260409, GraphRAG-R1 20260228 and Search-R1 20251113 (read 20261102 21:03 UTC); descriptions of the 23 left-out and borderline repositories (read 20261102 20:50 UTC).
4. The 42 project pages of this chapter, listed above : each line was checked against its page, and the group follows the first trend in the page's header (read 20261102 20:47 to 21:08 UTC for the first 37; the five added on 20261103 were summarised from their pages when they were placed); the pages carry their own sources.
5. [watchlist.tsv](watchlist.tsv) : 123 rows on 20261102, each tagged with its trends; no row carries the trend `agentic-search`; seven carry `learned-graph-traversal` (read 20261102 20:50 UTC).
6. [plans/20261102_1951-docs-catalogue.md](../../plans/20261102_1951-docs-catalogue.md) : the section "The owner's review of the lists (20261103)": the owner went through the six lists on 20261103, chose five new project pages (the largest active agent-memory projects without one) and a stated reason in the watch list for each of the other 21 (decision D-33 in `DECISIONS.md`) (read 20261103 01:55 UTC).
7. [watchlist.tsv](watchlist.tsv) : the note column of 21 rows, each starting "No page:" and written on 20261103 by an assistant that applied test P-1 to the project's archive entry, its snapshot row and the trend pages; the notes are judgements of this documentation, not statements by the projects, and the representative they name is the page of the same approach (read 20261103 01:55 UTC).
