---
type: index
kind: concept
aliases: [vectorless RAG, reasoning-based RAG, reasoning-based retrieval]
updated: 20261102 22:52 UTC
---

# Vectorless retrieval

This entry says what "vectorless" means in retrieval, where the word first appears, and how its use spread. Whether the method works is on the trend page.

## Definition

Vectorless retrieval picks what to read without a vector index: a [language model](./large-language-model.md) reasons over a structure, such as a tree of a document's sections, and chooses what to open [1]. The README of PageIndex, the earliest use found, calls PageIndex "a vectorless, reasoning-based RAG engine" with "no vector DBs or chunking"; it "replaces the vector index with a hierarchical tree index" that, in the current README, is extracted from the document's layout without a model [1]; the v0.5.0 release notes keep the classic LLM pipeline as `mode="standard"` [11]. Lumer and colleagues describe the family without the word: "hierarchical node-based systems that traverse document structure without embeddings" [3]. A standard or survey definition: **unstated**; none was found.

## How it changed

- **20240131.** [RAPTOR](./raptor.md) clusters chunk embeddings and summarises them into a tree [4]. *Reading:* it embeds to build the tree, so it does not meet the definition above.
- **20250401.** The PageIndex repository is created [5]. Its README of 20250820 says "Reasoning-based RAG" and "No Vector DB", not "vectorless"; the oldest revision with the word is of 20250824, in a notebook's name [6].
- **20250919.** The PageIndex blog post "Next-Generation Vectorless, Reasoning-based RAG" appears (first-party). It calls the tree an "in-context index" that the model reads [2]; the README asks readers to cite the post [1].
- **20251122.** Lumer et al. call their vector against non-vector comparison the first systematic one (their claim) [3].
- **20260628 and 20260908.** Two arXiv abstracts use the word: "vectorless document tree" and "vectorless hierarchical RAG pipeline" [7][8]. Affiliations were not read.
- **20261008.** RIT-RAG says methods such as PageIndex cannot scale to structures of large corpora that exceed the model's context, and adds content retrieval to tree navigation [9].

Still moving: [Vectorless retrieval](../trends/reasoning-over-structure.md).

## Where sources disagree

**Where the line falls.** PageIndex excludes the vector database and chunking [1]; RAPTOR's tree is built from embeddings [4]; KITE calls itself "vector-free" yet runs fixed lookups over a topic index, with sparse lexical retrieval [10]. Three names are in use: "vectorless" [1][7][8], "non-vector" [3], "vector-free" [10]. No source read says which systems each covers.

**Scale.** The README lists a Cloud-only layer that reasons over a whole corpus [1]; the RIT-RAG authors say tree methods first commit to one document [9]. No source read tests that layer.

## Related

[Tree index](./tree-index.md) · [RAPTOR](./raptor.md) · [retrieval-augmented generation](./retrieval-augmented-generation.md) · [vector search](./vector-search.md) · [embedding](./embedding.md) · [chunking](./chunking.md) · [agent](./agent.md) · [tool use](./tool-use.md). Project: [PageIndex](../projects/pageindex.md). Trend: [agentic search](../trends/agentic-search.md). Papers: [group page](../papers/reasoning-over-structure.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Index**

- [Knowledge compilation](knowledge-compilation.md)
- [RAPTOR](raptor.md)
- [Tree index](tree-index.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/VectifyAI/PageIndex (README, read through the GitHub API) : "vectorless, reasoning-based RAG engine", no vector DB or chunking, tree from layout without a model, Cloud-only File System layer, request to cite the blog post (first-party; read 20261102 22:06 UTC)
2. https://pageindex.ai/blog/pageindex-intro : Zhang and Tang, "PageIndex: Next-Generation Vectorless, Reasoning-based RAG", published 19 September 2025; JSON table-of-contents tree as an "in-context index" (first-party; read 20261102 22:06 UTC)
3. https://arxiv.org/abs/2511.18177 : Lumer et al., "Rethinking Retrieval: From Traditional Retrieval Augmented Generation to Agentic and Non-Vector Reasoning Systems in the Financial Domain for Large Language Models", v1 20251122, abstract (read 20261102 22:07 UTC)
4. https://arxiv.org/abs/2401.18059 : Sarthi et al., RAPTOR, v1 20240131, abstract: recursive embedding, clustering and summarising into a tree (read 20261102 22:07 UTC)
5. https://github.com/VectifyAI/PageIndex (repository data through the GitHub API) : created 2025-04-01T10:53:54Z (read 20261102 22:06 UTC)
6. https://github.com/VectifyAI/PageIndex/commits/main/README.md : README history through the GitHub API: list of 210 commits touching README.md; the file was read at each of the oldest 68, in date order, up to 06f13dd3e2 of 20250824, the first with the word "vectorless" (in a notebook's name); the one before it, 912d461701 of 20250820, has "Reasoning-based RAG" and "No Vector DB" but not the word (first-party; read 20261102 22:41 UTC)
7. https://arxiv.org/abs/2606.29399 : Jeon et al., "LLM-Guided Planning for Multi-hop Reasoning over Multimodal Nuclear Regulatory Documents", v1 20260628, abstract: "vectorless document tree"; found by an arXiv API query for the word "vectorless" in any field, which returned 6 records, 2 on topic (read 20261102 22:06 UTC)
8. https://arxiv.org/abs/2609.08364 : Kumar et al., SentryLine, v1 20260908, abstract: "vectorless hierarchical RAG pipeline" (read 20261102 22:06 UTC)
9. https://arxiv.org/abs/2610.11370 : RIT-RAG, v1 20261008, v2 20261016, abstract (read 20261102 22:07 UTC)
10. https://arxiv.org/abs/2610.41521 : KITE, v1 20261030, abstract: "vector-free framework", governed topic index, fixed lookups, sparse lexical retrieval (read 20261102 22:07 UTC)
11. https://github.com/VectifyAI/PageIndex/releases/tag/v0.5.0 : release notes, published 20261029, through the GitHub API: Flash engine is the local default and `mode="standard"` keeps the classic LLM pipeline (first-party; read 20261102 22:49 UTC)
