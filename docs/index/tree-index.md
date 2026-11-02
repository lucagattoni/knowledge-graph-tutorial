---
type: index
kind: concept
aliases: [tree-structure index, index tree]
updated: 20261102 22:51 UTC
---

# Tree index

This entry says what a tree index is and how the sources build one. It is the structure behind [vectorless retrieval](./vectorless-retrieval.md).

## Definition

No standard or survey definition was found in the sources read. The README of PageIndex says the project "replaces the vector index with a hierarchical tree index" that a model searches by reasoning; the tree is "extracted from the document layout without an LLM", and a model only summarises and refines it [1]. That is the current README: the v0.5.0 release notes (20261029) make the Flash engine the local default and keep the classic LLM pipeline as `mode="standard"` [8]. Its blog describes a JSON structure in which "The ToC acts as an index tree that organizes content into hierarchical nodes", each with an id, a name, metadata and child nodes [2]. An example output gives each node a title, a start index, an end index and an id [3]. LlamaIndex uses the same name for another structure: its tree index "builds a hierarchical tree from a set of Nodes", which become the leaves [5].

## How it changed

- **20240131.** RAPTOR is first submitted: it recursively embeds, clusters and summarises chunks into a tree, bottom up, and retrieves from several levels [4]. See [RAPTOR](./raptor.md).
- **Undated.** LlamaIndex documents a tree index that a query walks from root to leaf [5]. Its introduction date is unstated; the repository dates from 20221102 [6].
- **20250401.** The PageIndex repository is created [1]; its blog post of 20250919 presents the table-of-contents tree [2].
- **20251122.** Lumer et al. publish what they call the first systematic comparison of vector-based agentic RAG with node-based systems that traverse document structure without embeddings [7].
- **2026.** The PageIndex README makes "Flash", a fast tree-index builder, the default local method from August 2026 (first-party) [1]; see [PageIndex](../projects/pageindex.md). Still moving: [Vectorless retrieval](../trends/reasoning-over-structure.md).

## Where sources disagree

**What the tree is made from.** The document's layout, in PageIndex's current default (PageIndex [1][8]); clustered chunk embeddings and their summaries (RAPTOR [4]); chunk Nodes as leaves, with the upper levels unstated in the passage read (LlamaIndex [5]).

**Whether it beats vector search.** The PageIndex README reports 98.7% on FinanceBench and says it is "vastly outperforming vector-based RAG" (first-party) [1]; what the figure measures is on the [PageIndex](../projects/pageindex.md) page. Lumer et al. report a 68% win rate for vector-based agentic RAG over node-based systems on 1,200 filings and 150 questions; their abstract does not name PageIndex [7]. *Reading:* different systems were tested; no source read settles it.

## Related

[Vectorless retrieval](./vectorless-retrieval.md), [RAPTOR](./raptor.md), [retrieval-augmented generation](./retrieval-augmented-generation.md), [chunking](./chunking.md), [embedding](./embedding.md), [tool use](./tool-use.md). Projects: [PageIndex](../projects/pageindex.md), [RAGFlow](../projects/ragflow.md), [LlamaIndex](../projects/llama-index.md). Trend: [vectorless retrieval](../trends/reasoning-over-structure.md). Papers: [reasoning over structure](../papers/reasoning-over-structure.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Index**

- [Knowledge compilation](knowledge-compilation.md)
- [RAPTOR](raptor.md)
- [Vectorless retrieval](vectorless-retrieval.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/VectifyAI/PageIndex : README (hierarchical tree index, layout-based tree, Flash default from August 2026, 98.7% FinanceBench claim) and repository metadata (created 2025-04-01), read through the GitHub API (first-party; read 20261102 22:09 UTC)
2. https://pageindex.ai/blog/pageindex-intro : PageIndex blog, "PageIndex: Next-Generation Vectorless, Reasoning-based RAG", 19 September 2025: the table-of-contents tree and its node fields (first-party; read 20261102 22:11 UTC)
3. https://github.com/VectifyAI/PageIndex/blob/main/examples/results/2023-annual-report-truncated_structure.json : example output of the project: nodes with title, start_index, end_index, node_id and nested nodes (first-party; read 20261102 22:12 UTC)
4. https://arxiv.org/abs/2401.18059 : "RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval", submitted 31 January 2024, abstract (read 20261102 22:11 UTC)
5. https://developers.llamaindex.ai/python/framework/module_guides/indexing/index_guide/ : LlamaIndex documentation, section "Tree Index" (first-party; read 20261102 22:11 UTC)
6. https://github.com/run-llama/llama_index : repository metadata, created 2022-11-02, read through the GitHub API (read 20261102 22:09 UTC)
7. https://arxiv.org/abs/2511.18177 : Lumer et al., "Rethinking Retrieval: From Traditional Retrieval Augmented Generation to Agentic and Non-Vector Reasoning Systems in the Financial Domain for Large Language Models", 9 authors, submitted 22 November 2025, abstract (read 20261102 22:11 UTC)
8. https://github.com/VectifyAI/PageIndex/releases/tag/v0.5.0 : release notes, published 20261029, through the GitHub API: Flash engine is the local default and `mode="standard"` keeps the classic LLM pipeline (first-party; read 20261102 22:49 UTC)
