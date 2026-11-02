---
type: project
repo: OSU-NLP-Group/HippoRAG
trends: [graph-based-rag, agent-memory]
updated: 20261102 23:17 UTC
---

# HippoRAG

This page answers what HippoRAG is, how its graph and PageRank retrieval works, what has been measured and by whom, and whether the project is still moving. It describes the repository, which now centres on HippoRAG 2.

| Field | Value |
|---|---|
| Repository | https://github.com/OSU-NLP-Group/HippoRAG |
| Licence | MIT, from the `LICENSE` file read through GitHub's licence endpoint; copyright line "Copyright (c) 2025 OSU Natural Language Processing" [2]. The code's default [embedding](../index/embedding.md) model has a different licence (see Status and direction) [7][13]. |
| Trends | [Graph-based RAG](../trends/graph-based-rag.md), [Agent memory](../trends/agent-memory.md) |

## What it is

HippoRAG is a Python framework for [retrieval-augmented generation](../index/retrieval-augmented-generation.md). A [large language model](../index/large-language-model.md) builds a [knowledge graph](../index/knowledge-graph.md) from the passages. At query time, [Personalized PageRank](../index/personalized-pagerank.md) over that graph ranks the passages. The authors present the design as a model of human long-term memory [9][10].

Two papers define it: HippoRAG (Conference on Neural Information Processing Systems, NeurIPS, 2024; arXiv 20240523) and HippoRAG 2, "From RAG to Memory" (International Conference on Machine Learning, ICML, 2025; arXiv 20250220) [9][10]. Version 2 targets a weakness of earlier graph methods: their scores on simple factual questions fell below plain dense retrieval [10].

## How it works

Indexing [11]:

1. An LLM (large language model) extracts [triples](../index/triple.md) from each passage, with no fixed [schema](../index/schema.md). Their subjects and objects become phrase nodes.
2. Each passage also becomes a node, linked to its phrases (new in version 2).
3. An embedding model adds synonym edges between phrase nodes whose similarity passes a threshold, 0.8 in the paper's Table 13 and in the code [7].

Query [7][11]:

1. The query is matched against triple embeddings. The five best triples go to an LLM filter that drops irrelevant ones.
2. The phrases of the surviving triples (at most five) and every passage node become seeds. Passage seeds are scored by dense similarity, multiplied by 0.05.
3. Personalized PageRank runs with damping 0.5. If the filter keeps no triple, the dense ranking is returned.

Code defaults are `gpt-4o-mini` and `nvidia/NV-Embed-v2` [7].

For agents, the README documents an [MCP](../index/model-context-protocol.md) (Model Context Protocol) server, `hipporag-mcp`, with five tools and a Claude Code plugin; its HTTP transport has no authentication [5]. PyPI's newest release is 2.0.0a4, uploaded 20250624; the repository declares 2.0.0a5 [6][8].

## Evidence

First-party: the HippoRAG 2 authors ran every row below, with Llama-3.3-70B-Instruct building the graph and NV-Embed-v2 (7B dense) as retriever [11].

| Measure (paper table) | HippoRAG 2 | NV-Embed-v2 |
|---|---|---|
| Average QA (question answering) F1 (a score that balances precision and recall), seven sets (2) | 59.8 | 57.0 |
| Average passage recall@5, five sets (3) | 78.2 | 73.4 |
| Recall@5 (the share of relevant passages in the top five) on [MuSiQue](../datasets/musique.md) (3) | 74.7 | 69.7 |
| Recall@5 on 2Wiki (3) | 90.4 | 76.5 |
| Recall@5 on [PopQA](../datasets/popqa.md) (3) | 51.7 | 51.0 |

The paper's "5.0%" and "13.9%" gains on MuSiQue and 2Wiki equal these differences (computed). On PopQA a re-run of HippoRAG 1 scores 53.8, higher than both [11]. Removing passage nodes lowers average recall@5 over three [multi-hop](../index/multi-hop-question-answering.md) sets from 87.1 to 81.0 (Table 4) [11].

Indexing 11,656 MuSiQue passages took 9.2M input tokens for HippoRAG 2, against 68.5M for [LightRAG](./lightrag.md), 115.5M for [Microsoft GraphRAG](./microsoft-graphrag.md) and 1.7M for RAPTOR (Table 12). Query time was 1.2 s against 0.3 s for dense retrieval. Against the README's claim of fewer resources than RAPTOR, RAPTOR used fewer tokens and about the same time (100.5 against 99.5 minutes) [5][11].

*Reading:* the LightRAG row in Table 2 averages 6.6 F1, below the no-retrieval row (38.4). The text gives no reason; treat that comparison with caution [11].

Third-party and later papers, read as abstracts only:

| Date | Who | Finding |
|---|---|---|
| 20260817 | Sanchez and Dehnad, third-party audit | NV-Embed-v2 is licensed cc-by-nc-4.0. Of four audited systems (HippoRAG-2, PropRAG, SAG, KET-RAG), three depend on it for their best numbers, unnamed in the abstract. HippoRAG 2's paper does use it [11][12][13] |
| 20260813 | ReFind authors, who propose a rival method that builds no semantic structure (lexical index only) | ReFind 58.2 against HippoRAG 2 53.2 mean accuracy on [MemoryAgentBench](../benchmarks/memoryagentbench.md), GPT-4o-mini backbone [14] |
| 20260508 (v1, revised 20261029) | Shao et al., NeurIPS 2026 datasets track | On [LongMemEval](../datasets/longmemeval.md) HippoRAG stays within a two-call budget but loses 16 to 20 points of budget-compliant reliability as irrelevant sessions are added (abstract read at v2) [15] |

No independent reproduction of the paper's tables was found in the abstracts read. Longer notes: [archive entry](../../kb-kg/projects/hipporag.md). Papers: [graph-based RAG paper page](../papers/graph-based-rag.md).

## Status and direction

- **Release:** GitHub's only release and tag is v1.0.0, "HippoRAG 1", 20250227. HippoRAG 2 has none [3].
- **Activity, 20260804 to 20261102:** 10 commits by three authors, from 20260823 to 20261006, none after. Subjects: OpenAI-compatible endpoints, a gateway provider, JSON-parsing fallbacks, an MCP server update (20261001), the Claude Code plugin (20261006) [4]. 15 contributors, 8 open issues, no open pull request, not archived [1][4].
- **Direction:** the README's three TODO items (embedding models, embedding endpoints, vector-database integration) are all ticked [5]. A roadmap, maintenance mode and hosted tier are **unstated** in the README [5]. Four of the HippoRAG 2 authors co-wrote REMem (International Conference on Learning Representations, ICLR, 2026), a separate episodic [agent-memory](../index/agent-memory.md) graph with an agentic retriever. Its abstract (first-party) reports gains over systems such as [Mem0](./mem0.md) and HippoRAG 2 of 3.4 absolute points on episodic recollection and 13.4 on reasoning tasks [16].
- **Licence caution:** the default embedder NV-Embed-v2 is cc-by-nc-4.0, though the code is MIT [7][13]. The quick start uses `text-embedding-3-small` [5]. Other dependencies' licences: **unstated**.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)
- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)
- [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Cognee](cognee.md)
- [Graphiti](graphiti.md)
- [OpenViking](openviking.md)
- [Projects](README.md)

**Papers**

- [Papers: Graph-based RAG](../papers/graph-based-rag.md)

**Datasets**

- [2WikiMultiHopQA](../datasets/2wikimultihopqa.md)
- [HotpotQA](../datasets/hotpotqa.md)
- [MuSiQue](../datasets/musique.md)
- [Natural Questions](../datasets/natural-questions.md)

**Benchmarks**

- [EnterpriseRAG-Bench](../benchmarks/enterpriserag-bench.md)
- [GraphRAG-Bench (Xiang)](../benchmarks/graphrag-bench-xiang.md)
- [GraphRAG-Bench (Xiao)](../benchmarks/graphrag-bench-xiao.md)
- [HotpotQA](../benchmarks/hotpotqa.md)
- [MemoryAgentBench](../benchmarks/memoryagentbench.md)
- [MultiHop-RAG](../benchmarks/multihop-rag.md)
- [MuSiQue](../benchmarks/musique.md)
- [Natural Questions](../benchmarks/natural-questions.md)
- [RAGSearch](../benchmarks/ragsearch.md)

**Applied to Pinakes**

- [The Pinakes graph approach](../applied-to-pinakes/approach.md)
- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [GraphRAG](../index/graphrag.md)
- [Inverted index](../index/inverted-index.md)
- [Multi-hop question answering](../index/multi-hop-question-answering.md)
- [PageRank](../index/pagerank.md)
- [Personalized PageRank](../index/personalized-pagerank.md)
- [RAPTOR](../index/raptor.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/OSU-NLP-Group/HippoRAG : repository metadata via `gh api` (archived flag, dates, open issues, one tag) (read 20261102 20:10 UTC)
2. https://github.com/OSU-NLP-Group/HippoRAG/blob/main/LICENSE : MIT text, via the licence endpoint (read 20261102 20:10 UTC)
3. https://github.com/OSU-NLP-Group/HippoRAG/releases : latest release v1.0.0, the only one (read 20261102 20:10 UTC)
4. https://github.com/OSU-NLP-Group/HippoRAG/commits/main : 10 commits since 20260804; 15 contributors; 8 issues, 0 pull requests (read 20261102 20:13 UTC)
5. https://github.com/OSU-NLP-Group/HippoRAG/blob/main/README.md : install routes, MCP server, plugin, vector stores, TODO list (read 20261102 20:10 UTC)
6. https://github.com/OSU-NLP-Group/HippoRAG/blob/main/pyproject.toml : version 2.0.0a5, extras (read 20261102 20:10 UTC)
7. https://github.com/OSU-NLP-Group/HippoRAG/blob/main/src/hipporag/utils/config_utils.py : defaults for models, weights, damping, thresholds (read 20261102 20:14 UTC)
8. https://pypi.org/pypi/hipporag/json : newest release 2.0.0a4, 20250624; its requirements (read 20261102 20:13 UTC)
9. https://arxiv.org/abs/2405.14831 : HippoRAG, NeurIPS 2024 note, first version 20240523 (read 20261102 20:11 UTC)
10. https://arxiv.org/abs/2502.14802 : HippoRAG 2, ICML 2025 note, first version 20250220, abstract (read 20261102 20:11 UTC)
11. https://arxiv.org/html/2502.14802v2 : method, Tables 2, 3, 4, 12, 13, appendix G (read 20261102 20:11 UTC)
12. https://arxiv.org/abs/2608.16096 : licence audit of multi-hop retrieval systems (read 20261102 20:14 UTC)
13. https://huggingface.co/nvidia/NV-Embed-v2 : licence tag cc-by-nc-4.0, via the model API (read 20261102 20:14 UTC)
14. https://arxiv.org/abs/2608.12888 : ReFind against HippoRAG 2; lexical index, no semantic structure (read 20261102 20:33 UTC)
15. https://arxiv.org/abs/2605.07313 : scale-conditioned memory evaluation; v1 20260508, v2 20261029, abstract read at v2 (read 20261102 20:33 UTC)
16. https://arxiv.org/abs/2602.13530 : REMem, authors and abstract (read 20261102 20:33 UTC)
