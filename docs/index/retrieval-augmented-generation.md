---
type: index
kind: concept
aliases: [RAG]
updated: 20261102 21:27 UTC
---

# Retrieval-augmented generation

This entry answers what retrieval-augmented generation (RAG) is and which of its parts are settled. It follows the idea from the two 2020 papers to the graph and agentic variants. It also shows where surveys use the same words for different things.

## Definition

Lewis et al. introduce RAG as "models which combine pre-trained parametric and non-parametric memory for language generation". In their version the parametric memory is a pre-trained seq2seq model, and the non-parametric memory is a dense vector index of Wikipedia read by a neural retriever [1]. In the [large language model](./large-language-model.md) era, Gao et al. describe the same idea as retrieving relevant document [chunks](./chunking.md) from an external knowledge base by semantic similarity and giving them to the model with the question, which reduces factually wrong output [2].

## How it changed

- **20200210.** Guu et al. submit REALM, which trains a retriever inside language-model pre-training; its abstract reports 4-16% absolute gains on three open-domain QA benchmarks (first-party) [3].
- **20200522.** Lewis et al. submit the RAG paper (NeurIPS 2020) and report state of the art on three open-domain QA tasks (first-party) [1]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **After ChatGPT's wide adoption.** Gao et al. call ChatGPT's arrival a "pivotal moment" and place "Naive RAG" shortly after it [2].
- **20231218 (v5 20240327).** The Gao et al. survey sorts the line into Naive, Advanced and Modular RAG [2].
- **20250115 (v4 20260401).** Singh et al. add [Graph RAG](./graphrag.md) and Agentic RAG as later stages and write that agentic designs are not always the right default [4]. *Reading:* this documentation rates the two lines differently: [Graph-based RAG](../trends/graph-based-rag.md) as steady, [Agentic search](../trends/agentic-search.md) as growing.
- **20260514.** Sen et al. report that grep generally beat [vector](./vector-search.md) retrieval in their comparisons on a 116-question LongMemEval sample, with scores depending strongly on the harness [5].

## Where sources disagree

**What "naive" RAG is.** Gao et al. describe it as indexing, [embedding](./embedding.md)-based retrieval and generation, which gained prominence after ChatGPT [2]. Singh et al. describe it as keyword retrieval such as [TF-IDF](./tf-idf.md) and [BM25](./bm25.md) over static datasets [4].

**Where the line starts.** Gao et al. say RAG's inception "coincided with the rise of the Transformer architecture" and began with pre-training work [2]. The earliest dated papers read for this entry are the two of 2020 [1][3]; none of the sources read names a first paper.

## Related

[large language model](./large-language-model.md) · [chunking](./chunking.md) · [embedding](./embedding.md) · [dense retrieval](./dense-retrieval.md) · [vector search](./vector-search.md) · [hybrid search](./hybrid-search.md) · [reranking](./reranking.md) · [GraphRAG](./graphrag.md) · [agent](./agent.md) · [agent memory](./agent-memory.md) · [context window](./context-window.md) · [information retrieval](./information-retrieval.md) · [LlamaIndex](../projects/llama-index.md) · [foundation papers](../papers/foundations.md) · [graph-based RAG papers](../papers/graph-based-rag.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [Language models meet retrieval (2018-2022)](../history/language-models-meet-retrieval.md)
- [The semantic web and linked data](../history/semantic-web.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)
- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)
- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md)
- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)
- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)
- [Trends: what the field is doing now](../trends/README.md)
- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Projects**

- [Dify](../projects/dify.md)
- [HippoRAG](../projects/hipporag.md)
- [LightRAG](../projects/lightrag.md)
- [LlamaIndex](../projects/llama-index.md)
- [LLM Wiki (nashsu)](../projects/llm-wiki-nashsu.md)
- [Microsoft GraphRAG](../projects/microsoft-graphrag.md)
- [Neo4j](../projects/neo4j.md)
- [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md)
- [Projects](../projects/README.md)
- [RAG-Anything](../projects/rag-anything.md)
- [RAGFlow](../projects/ragflow.md)
- [Supermemory](../projects/supermemory.md)

**Papers**

- [Papers](../papers/README.md)
- [Papers: Agent memory](../papers/agent-memory.md)
- [Papers: Agentic search over raw data](../papers/agentic-search.md)
- [Papers: foundations](../papers/foundations.md)
- [Papers: Graph-based RAG](../papers/graph-based-rag.md)
- [Papers: Plain files as agent knowledge](../papers/plain-file-knowledge.md)

**Benchmarks**

- [Benchmarks](../benchmarks/README.md)
- [CRAG](../benchmarks/crag.md)
- [EnterpriseRAG-Bench](../benchmarks/enterpriserag-bench.md)
- [FRAMES](../benchmarks/frames.md)
- [GraphRAG-Bench (Xiang)](../benchmarks/graphrag-bench-xiang.md)
- [LoCoMo](../benchmarks/locomo.md)
- [MultiHop-RAG](../benchmarks/multihop-rag.md)
- [Natural Questions](../benchmarks/natural-questions.md)

**Experiments**

- [X3: Matched-cost comparison](../experiments/x3-matched-cost-comparison.md)
- [X5: Wiki size limit](../experiments/x5-wiki-size-limit.md)

**Index**

- [Agent](agent.md)
- [Agent memory](agent-memory.md)
- [Chunking](chunking.md)
- [Community detection](community-detection.md)
- [Community report](community-report.md)
- [Context window](context-window.md)
- [Dense retrieval](dense-retrieval.md)
- [Embedding](embedding.md)
- [Fine-tuning](fine-tuning.md)
- [GraphRAG](graphrag.md)
- [Hybrid search](hybrid-search.md)
- [Information retrieval](information-retrieval.md)
- [Knowledge compilation](knowledge-compilation.md)
- [Large language model](large-language-model.md)
- [LLM wiki](llm-wiki.md)
- [Memory poisoning](memory-poisoning.md)
- [Model Context Protocol](model-context-protocol.md)
- [Multi-hop question answering](multi-hop-question-answering.md)
- [Open-domain question answering](open-domain-question-answering.md)
- [Personalized PageRank](personalized-pagerank.md)
- [Prompt caching](prompt-caching.md)
- [Query-focused summarization](query-focused-summarization.md)
- [Question answering](question-answering.md)
- [Reinforcement learning](reinforcement-learning.md)
- [Reranking](reranking.md)
- [Slot filling](slot-filling.md)
- [tf-idf](tf-idf.md)
- [Transformer](transformer.md)
- [TREC](trec.md)
- [Tree index](tree-index.md)
- [Vector search](vector-search.md)
- [Vectorless retrieval](vectorless-retrieval.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2005.11401 : Lewis et al. (12 authors), "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", submitted 20200522, v4 20210412, NeurIPS 2020: abstract, definition, results (read 20261102 20:57 UTC)
2. https://arxiv.org/pdf/2312.10997 : Gao et al. (10 authors), "Retrieval-Augmented Generation for Large Language Models: A Survey", v1 20231218, v5 20240327: introduction and section II, Naive RAG (read 20261102 20:57 UTC)
3. https://arxiv.org/abs/2002.08909 : Guu et al., "REALM: Retrieval-Augmented Language Model Pre-Training", submitted 20200210: abstract (read 20261102 20:57 UTC)
4. https://arxiv.org/pdf/2501.09136 : Singh et al., "Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG", v1 20250115, v4 20260401: sections 2.3 and 10.1 (abstract page read 20261102 20:57 UTC, PDF read 20261102 20:57 UTC)
5. https://arxiv.org/abs/2605.15184 : Sen et al., "Is Grep All You Need? How Agent Harnesses Reshape Agentic Search", submitted 20260514: abstract (read 20261102 20:58 UTC)
