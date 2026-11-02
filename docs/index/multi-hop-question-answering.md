---
type: index
kind: concept
aliases: [multi-hop QA, multihop question answering, MHQA]
updated: 20261102 21:25 UTC
---

# Multi-hop question answering

Multi-hop question answering is answering a question whose answer needs facts combined from more than one place. This entry gives the definition, the dated datasets that fixed the task, and the dispute over whether the datasets really test multiple hops.

## Definition

A survey of the field, posted in 2022, describes multi-hop question answering as answering natural-language questions that require "extracting and combining multiple pieces of information and doing multiple steps of reasoning" [1]. The early datasets state the same need in their own terms. Welbl and colleagues describe a task where "a model learns to seek and combine evidence" across documents [2]. The HotpotQA authors require "finding and reasoning over multiple supporting documents" [3].

## How it changed

- **20171017.** Welbl, Stenetorp and Riedel build datasets for multi-hop reading comprehension across documents (*Transactions of the ACL* 6, 2018) [2]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20180925.** HotpotQA (7 authors, EMNLP 2018) adds sentence-level supporting facts [3]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20190607.** Min and five co-authors show that single-hop reasoning solves much of HotpotQA [4].
- **20201102.** 2WikiMultiHopQA (COLING 2020) adds evidence information that contains a reasoning path [5].
- **20210802.** MuSiQue builds 2 to 4 hop questions from connected single-hop questions [6].
- **20220419.** Mavi, Jangra and Jatowt post the survey [1].
- **20240127.** MultiHop-RAG benchmarks retrieval-augmented generation on multi-hop queries and ships a knowledge base [7].
- **20240523.** HippoRAG reports gains over state-of-the-art methods on multi-hop question answering (first-party); see [hipporag](../projects/hipporag.md) [8].

Graph-based retrieval and agents that retrieve in several turns still move: see [Graph-based RAG](../trends/graph-based-rag.md).

## Where sources disagree

Whether the datasets test several hops is disputed. Min and colleagues report that a single-hop BERT-based model is comparable to state-of-the-art multi-hop models on HotpotQA (the F1 figure is on the [HotpotQA dataset page](../datasets/hotpotqa.md)) [4]. The MuSiQue authors write that existing multi-hop benchmarks are "largely solvable via shortcuts" and build theirs to resist disconnected reasoning [6]. Both are written by dataset or method authors and neither is a neutral audit.

## Related

[Question answering](./question-answering.md), [retrieval-augmented generation](./retrieval-augmented-generation.md), [GraphRAG](./graphrag.md), [knowledge graph](./knowledge-graph.md), [personalized PageRank](./personalized-pagerank.md), [agent](./agent.md), [mean reciprocal rank](./mean-reciprocal-rank.md). Datasets and benchmarks: [HotpotQA](../datasets/hotpotqa.md) ([benchmark](../benchmarks/hotpotqa.md)), [MuSiQue](../datasets/musique.md) ([benchmark](../benchmarks/musique.md)), [2WikiMultiHopQA](../datasets/2wikimultihopqa.md) ([benchmark](../benchmarks/2wikimultihopqa.md)), [MultiHop-RAG](../datasets/multihop-rag.md) ([benchmark](../benchmarks/multihop-rag.md)). Papers: [graph-based RAG](../papers/graph-based-rag.md), [learned graph traversal](../papers/learned-graph-traversal.md), [agentic search](../papers/agentic-search.md). Project: [hipporag](../projects/hipporag.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)
- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)
- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [HippoRAG](../projects/hipporag.md)

**Papers**

- [Papers: Agentic search over raw data](../papers/agentic-search.md)

**Datasets**

- [2WikiMultiHopQA](../datasets/2wikimultihopqa.md)
- [Datasets](../datasets/README.md)
- [HotpotQA](../datasets/hotpotqa.md)
- [MetaQA](../datasets/metaqa.md)
- [MultiHop-RAG](../datasets/multihop-rag.md)
- [MuSiQue](../datasets/musique.md)

**Benchmarks**

- [2WikiMultiHopQA](../benchmarks/2wikimultihopqa.md)
- [Benchmarks](../benchmarks/README.md)
- [CRAG](../benchmarks/crag.md)
- [HotpotQA](../benchmarks/hotpotqa.md)
- [MuSiQue](../benchmarks/musique.md)
- [RAGSearch](../benchmarks/ragsearch.md)

**Experiments**

- [Instruments](../experiments/instruments.md)
- [X2: the index cost of cheap graph builders](../experiments/x2-index-cost.md)

**Applied to Pinakes**

- [Measurements](../applied-to-pinakes/measurements.md)
- [The Pinakes graph approach](../applied-to-pinakes/approach.md)
- [What Pinakes should measure next](../applied-to-pinakes/next.md)
- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Chain-of-thought](chain-of-thought.md)
- [Disconnected reasoning](disconnected-reasoning.md)
- [Exact match](exact-match.md)
- [Knowledge-base question answering](knowledge-base-question-answering.md)
- [Mean reciprocal rank](mean-reciprocal-rank.md)
- [Open-domain question answering](open-domain-question-answering.md)
- [Personalized PageRank](personalized-pagerank.md)
- [Question answering](question-answering.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2204.09140 : Mavi, Jangra, Jatowt, "Multi-hop Question Answering", 3 authors, v1 20220419; abstract (read 20261102 20:56 UTC)
2. https://arxiv.org/abs/1710.06481 : Welbl, Stenetorp, Riedel, "Constructing Datasets for Multi-hop Reading Comprehension Across Documents", v1 20171017; TACL 6, pp. 287-302 per the page; abstract (read 20261102 20:56 UTC)
3. https://arxiv.org/abs/1809.09600 : Yang et al., "HotpotQA", 7 authors, v1 20180925, EMNLP 2018 per the page; abstract (read 20261102 20:56 UTC)
4. https://arxiv.org/abs/1906.02900 : Min et al., "Compositional Questions Do Not Necessitate Multi-hop Reasoning", 6 authors, v1 20190607, ACL 2019 per the page; abstract (read 20261102 20:56 UTC)
5. https://arxiv.org/abs/2011.01060 : Ho et al., "Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps", 4 authors, v1 20201102, COLING 2020 per the page; abstract (read 20261102 21:02 UTC)
6. https://arxiv.org/abs/2108.00573 : Trivedi et al., "MuSiQue: Multihop Questions via Single-hop Question Composition", 4 authors, v1 20210802; abstract (read 20261102 20:56 UTC)
7. https://arxiv.org/abs/2401.15391 : Tang and Yang, "MultiHop-RAG", v1 20240127; abstract (read 20261102 21:02 UTC)
8. https://arxiv.org/abs/2405.14831 : Jiménez Gutiérrez et al., "HippoRAG", 5 authors, v1 20240523, NeurIPS 2024 per the page; abstract (read 20261102 21:02 UTC)
