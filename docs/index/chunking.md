---
type: index
kind: concept
aliases: [chunk, text splitting]
updated: 20261102 21:28 UTC
---

# Chunking

This entry answers what it means to cut documents into chunks, why retrieval systems do it, and how far the choice of cutting method is settled. It does not cover the retrieval step that follows. The newest evidence is from 2026 and still moving.

## Definition

Chunking is the step that cuts a document into smaller pieces, called chunks, that are indexed and retrieved separately. Gao et al. place it in indexing for retrieval-augmented generation: text is "segmented into smaller, digestible chunks" to fit the limits of a language model, and each chunk is encoded as a vector and stored; at query time the top K chunks by similarity are returned [1]. Units range from token and sentence up to whole document; a fixed number of tokens (for example 100, 256 or 512) is the usual method [1].

## How it changed

- **20200410.** Karpukhin et al. split Wikipedia into disjoint 100-word passages as "basic retrieval units"; fixed-length passages beat natural paragraphs, and overlap gave no advantage [2].
- **20200522.** Lewis et al. cut Wikipedia into disjoint 100-word chunks for their retrieval-augmented generation model [3]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md); the snapshot is on [its dataset page](../datasets/wikipedia-dpr-kilt.md).
- **20231218 (v5 20240327).** Gao et al. list refinements of fixed-size cutting (recursive splits, sliding windows, Small2Big) and state that they "still cannot strike a balance between semantic completeness and context length" [1].
- **20241016.** Qu, Tu and Bao find that the extra cost of semantic chunking (segments chosen by meaning) is "not justified by consistent performance gains" over fixed-size chunking [4].
- **20261022.** Bian et al. measure a cost static tests miss: after an edit, chunks whose boundary moved must be embedded again. On 120 pairs of Wikipedia revisions, fixed-size chunking recomputed 57 to 68 percent of the embedding work, recursive 38 to 56, content-defined 43 to 54 [5].
- **20261027.** Zhao et al. propose a chunker that picks boundaries by optimising over question and evidence pairs (supervised; no model training is stated), claiming better complete-evidence recall than existing chunkers in nearly all evaluated settings (first-party) [6]. Still moving.

## Where sources disagree

**Does the cutting method matter?** In the revision study, evidence recall of the three chunkers differed by less than two points within each language at the settings tested [5]. Qu et al. found no consistent gain from the costlier method [4]. Zhao et al. report that theirs beats existing chunkers (first-party, other data and metric) [6]. The tests differ, so no source read settles it.

## Related

[retrieval-augmented generation](./retrieval-augmented-generation.md) · [embedding](./embedding.md) · [context window](./context-window.md) · [GraphRAG](./graphrag.md) · [Graph-based RAG](../trends/graph-based-rag.md) · [Experiments](../experiments/README.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md)
- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Projects**

- [Dify](../projects/dify.md)
- [GraphRAG SDK](../projects/graphrag-sdk.md)
- [Hyper-Extract](../projects/hyper-extract.md)
- [LightRAG](../projects/lightrag.md)
- [LlamaIndex](../projects/llama-index.md)
- [Microsoft GraphRAG](../projects/microsoft-graphrag.md)
- [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md)
- [PageIndex](../projects/pageindex.md)
- [RAGFlow](../projects/ragflow.md)
- [Supermemory](../projects/supermemory.md)

**Papers**

- [Papers: Vectorless retrieval](../papers/reasoning-over-structure.md)

**Benchmarks**

- [MultiHop-RAG](../benchmarks/multihop-rag.md)

**Applied to Pinakes**

- [Measurements](../applied-to-pinakes/measurements.md)

**Index**

- [Context window](context-window.md)
- [Gleaning](gleaning.md)
- [Knowledge compilation](knowledge-compilation.md)
- [RAPTOR](raptor.md)
- [Retrieval-augmented generation](retrieval-augmented-generation.md)
- [Token](token.md)
- [Tree index](tree-index.md)
- [Vectorless retrieval](vectorless-retrieval.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/2312.10997 : Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey", v5 20240327: indexing, retrieval granularity, chunking strategy (read 20261102 20:51 UTC)
2. https://arxiv.org/pdf/2004.04906 : Karpukhin et al., "Dense Passage Retrieval for Open-Domain Question Answering", v3 20200930, first version 20200410: 100-word passages, footnotes 3 and 5 (read 20261102 20:51 UTC)
3. https://arxiv.org/pdf/2005.11401 : Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", first version 20200522: disjoint 100-word chunks (read 20261102 20:51 UTC)
4. https://arxiv.org/abs/2410.13070 : Qu, Tu, Bao, "Is Semantic Chunking Worth the Computational Cost?", submitted 20241016, abstract (read 20261102 20:51 UTC)
5. https://arxiv.org/abs/2610.31019 : Bian et al., "Chunk Recomputation under Real Document Revisions", submitted 20261022, abstract (read 20261102 20:51 UTC)
6. https://arxiv.org/abs/2610.36557 : Zhao et al., "QESChunker", submitted 20261027, abstract (read 20261102 20:51 UTC; re-read 20261102 21:23 UTC)
