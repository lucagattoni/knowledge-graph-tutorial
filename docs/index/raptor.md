---
type: index
kind: system
aliases: [Recursive Abstractive Processing for Tree-Organized Retrieval]
updated: 20261102 22:50 UTC
---

# RAPTOR

This entry answers what RAPTOR is, when it appeared, and how later work treats it. RAPTOR has no project page here: it is a research method with released code.

## Definition

RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval) is a retrieval method by Sarthi, Abdullah, Tuli, Khanna, Goldie and Manning. It cuts a corpus into chunks of about 100 tokens, embeds them, groups them with Gaussian mixture models, has a language model summarise each group, and repeats on the summaries until a tree stands [1][2]. At query time it walks the tree layer by layer or, in the "collapsed tree" variant, compares the query with all nodes at once by cosine similarity, so one answer can draw on detail and on theme summaries [2]. The authors found the collapsed tree better on 20 QASPER stories [2]. First-party result: with GPT-4, a 20% absolute gain on QuALITY over the best earlier result [1].

## How it changed

- **20240131.** The paper is posted to arXiv (one version) [1]. OpenReview lists it as an ICLR 2024 poster [3]. See [What has settled since 2023](../history/settled-since-2023.md).
- **20240227.** The official code repository is created; its last commit is 20240903 (read 20261102) [4].
- **20250220.** The HippoRAG 2 paper (second version 20250619) uses RAPTOR as a baseline and reports its indexing cost on a corpus built from [MuSiQue](../datasets/musique.md) (size on that page) [5].
- **20260819.** RAGFlow v0.27.0 deprecates its RAPTOR and GraphRAG features in favour of Tree and Graph in a "knowledge compilation" feature; content already generated "remains searchable" [6]. See [RAGFlow](../projects/ragflow.md).
- **Still moving.** [Vectorless retrieval](../trends/reasoning-over-structure.md) names RAPTOR as the tree ancestor that still searches by embeddings (every node is embedded with SBERT) [2].

## Where sources disagree

**Indexing cost.** The HippoRAG 2 README (first-party, a competing method) claims "significantly fewer resources for offline indexing" than GraphRAG, RAPTOR and LightRAG [7]. The paper's Table 12 gives RAPTOR 1.7 million input tokens against 9.2 million for HippoRAG 2, and 100.5 against 99.5 minutes of indexing; its text compares token use with LightRAG and GraphRAG only [5]. The paper also blames noise from RAPTOR's summaries for weak results on simple and multi-hop questions [5]; RAPTOR's own tests use NarrativeQA, QASPER and QuALITY [2].

**Venue.** The arXiv record names none [1]; OpenReview names ICLR 2024 [3].

**RAGFlow.** The v0.27.0 notes call the feature deprecated, yet pull-request titles in the same notes still name RAPTOR (for example "Align Go knowledge compiler RAPTOR with Python"). Whether the method lives on inside Tree is unstated [6].

## Related

[GraphRAG](./graphrag.md) · [tree index](./tree-index.md) · [vectorless retrieval](./vectorless-retrieval.md) · [knowledge compilation](./knowledge-compilation.md) · [query-focused summarization](./query-focused-summarization.md) · [chunking](./chunking.md) · [embedding](./embedding.md). Projects: [RAGFlow](../projects/ragflow.md), [HippoRAG](../projects/hipporag.md), [PageIndex](../projects/pageindex.md). Papers: [Vectorless retrieval papers](../papers/reasoning-over-structure.md), [Graph-based RAG papers](../papers/graph-based-rag.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Projects**

- [RAGFlow](../projects/ragflow.md)

**Index**

- [Knowledge compilation](knowledge-compilation.md)
- [Query-focused summarization](query-focused-summarization.md)
- [Tree index](tree-index.md)
- [Vectorless retrieval](vectorless-retrieval.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2401.18059 : Sarthi et al., "RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval", submitted 20240131, one version, abstract; no venue named (first-party; read 20261102 22:07 UTC)
2. https://arxiv.org/html/2401.18059 : RAPTOR full text: method (100-token chunks, Gaussian mixture models, UMAP, tree traversal and collapsed tree, SBERT embeddings), QASPER comparison, datasets (first-party; read 20261102 22:07 UTC)
3. https://openreview.net/forum?id=GN921JHCRw : OpenReview record of the paper: venue "ICLR 2024 poster", read through the OpenReview search API (read 20261102 22:11 UTC)
4. https://github.com/parthsarthi03/raptor : repository metadata and commit list via `gh api`: described as the official implementation, created 20240227, last commit 20240903 (read 20261102 22:10 UTC)
5. https://arxiv.org/html/2502.14802v2 : Gutiérrez et al., HippoRAG 2 ("From RAG to Memory"), Table 12 and text on RAPTOR (first-party for HippoRAG 2); first version 20250220, v2 20250619 per https://arxiv.org/abs/2502.14802 (read 20261102 22:12 UTC)
6. https://github.com/infiniflow/ragflow/releases/tag/v0.27.0 : RAGFlow v0.27.0 release notes, published 20260819: deprecation of RAPTOR and GraphRAG features, pull-request titles naming RAPTOR (first-party; read 20261102 22:11 UTC)
7. https://github.com/OSU-NLP-Group/HippoRAG/blob/main/README.md : HippoRAG README, claim of fewer indexing resources (first-party; read 20261102 22:12 UTC)
