---
type: project
repo: VectifyAI/PageIndex
trends: [reasoning-over-structure]
updated: 20261102 23:17 UTC
---

# PageIndex

PageIndex answers questions over long documents without a vector index: it builds a tree of each document's sections and lets a [large language model](../index/large-language-model.md) read the tree to pick the pages it needs. This page says how it works, what has been measured and by whom, and where the project stands.

| Field | Value |
|---|---|
| Repository | https://github.com/VectifyAI/PageIndex |
| Licence | MIT. The `LICENSE` file reads "MIT License", "Copyright (c) 2025 Vectify AI", and GitHub classifies it as MIT [1][2] |
| Trends | [Vectorless retrieval](../trends/reasoning-over-structure.md) |

## What it is

PageIndex is a Python SDK (software development kit) and command-line tool from Vectify AI. Its README states the idea as "similarity ≠ relevance": a hierarchical tree index replaces the vector index, and an LLM (large language model) reasons through it in two steps, index and retrieve [3]. It uses no [embedding](../index/embedding.md) index and no [chunking](../index/chunking.md); the README says "No Vector DB, No Chunking" [3]. The tree follows the document's headings, not extracted entities, so it is not a [knowledge graph](../index/knowledge-graph.md).

Local mode needs only an LLM key. Cloud mode is hosted by Vectify and needs a PageIndex key [3][4]. Local handles text-based PDFs and cites at page level; Cloud adds scanned documents, images and block-level citations [3].

## How it works

**Index.** The default local builder is "Flash". The README says the tree "is extracted from the document layout without an LLM; the index model only summarizes and refines it" [3]. The v0.5.0 notes add that the original LLM pipeline remains as `mode="standard"` and that tree optimisation (a merge pass plus an LLM pass that expands oversized nodes) is on by default [4]. Each node holds a title, id, page range and summary [8].

**Retrieve.** Retrieval is an [agent](../index/agent.md) loop, not a ranking function. Per the archive's reading of the source, the agent has four read tools: list documents, check status, fetch the tree and fetch the text of a page range [8]. It reads the tree first, then asks for narrow page ranges, by [tool use](../index/tool-use.md). The chat engine uses the OpenAI Agents SDK; the SDK also exposes the same tools to other agent frameworks and through the [Model Context Protocol](../index/model-context-protocol.md) [4].

## Evidence

All three Vectify rows are first-party: run by the authors, on their own repositories, with an LLM as judge.

| Claim | Test | Who ran it | First-party | Date | Source |
|---|---|---|---|---|---|
| 98.7% accuracy | FinanceBench public set, "Mafin 2.5" built on PageIndex, on GPT-4o and DeepSeek V3 | Vectify | yes | repository created 20250219 | [5] |
| Best 98.7% (Claude Opus 5.5, max) at $128.49 per 100 questions; lowest 65.7% | Financial QA (question answering): 37 configurations of 21 LLMs, 100 questions, 40 Form 10-K filings; no other retriever in the table | Vectify | yes | README read 20261102 | [6] |
| PageIndex 100.0% against vector search 54.0%, 74.6%, 79.4%, 87.3% (top-k 10, 30, 50, 100) | 63 questions on five NVIDIA 10-K reports; cost per 1,000 queries $110 against $16 to $135 | Vectify, with `pageindex` 0.4.1 | yes | 20261016 | [7] |

Limits:

- The Financial QA row is read from the benchmark repository's own README, which counts 37 configurations of 21 LLMs after additions on 20261024 and 20261027. The main PageIndex README (last changed 20261027) still says "34 configurations of 19 LLMs", the count of the benchmark's first commit of 20261023; the two were read 20261102 22:31 UTC [6][14].
- The 98.7% FinanceBench figure measures Mafin 2.5, not the SDK at v0.5.0. Ambiguous or invalid questions were settled by "expert human annotations" [5]. By the archive's count of the labelled result files, 148 of 150 answers count as correct only if benchmark-error and multiple-valid-approach labels do; counting only "aligned" gives 136 of 150, 90.7% [9].
- Both other runs stay within annual reports. In the cookbook, vector search is priced without prompt caching and PageIndex with cache hits [7].

Three papers by other authors compare tree-based with vector retrieval. None scores the released SDK. Their relations are on the [papers group page](../papers/reasoning-over-structure.md).

| Paper | Finding | Caveat |
|---|---|---|
| Lumer et al., 20251122 [10] | Vector-based agentic RAG (retrieval-augmented generation) won 68% of pairwise comparisons against hierarchical node-based systems; 1,200 SEC (US Securities and Exchange Commission) filings, 150 questions | Abstract does not name PageIndex; the archive reads the node system as modelled on it [9] |
| Hashmi, 20260414, v2 20261028 [11] | Its Tree Reasoning configuration (a baseline, not the proposed method, Adaptive Hybrid Retrieval) scored 0.900 overall, the highest; on the first 50 FinanceBench questions, with the supplied evidence snippets as the corpus, 0.938 against 0.821 for vector RAG | Small corpus; configurations also differ in document access, prompts and output length, so differences "cannot be attributed to retrieval architecture alone" (author) |
| RIT-RAG, 20261008 [12] | Says PageIndex cannot scale to large corpora or recover from a wrong document pick; proposes a competing method | Abstract gives no PageIndex score [9] |

*Reading:* The authors' results are strong but narrow (financial filings, LLM judges). The other papers do not test the SDK and disagree on small or home-built setups: one finds vector retrieval ahead, one a tree. No independent scored run of the released SDK is in the sources read.

## Status and direction

The repository is not archived [1]. The latest release is v0.5.0, published 20261029 22:53 UTC [4]. Stars and activity are in the [watch-list table](./README.md).

Direction, from the README: a unified local and cloud SDK and Flash as the local default (both Aug '26), then a hosted Page Search API (Oct '26) that it says cuts "97% token cost" (first-party claim) [3]. OCR (optical character recognition), metadata, folders, the MCP (Model Context Protocol) server and a File System layer for many documents are Cloud features [3]. [RAGFlow](./ragflow.md) offers a "PageIndex" compilation template; its documents do not name this project [13].

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)
- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)
- [Trends: what the field is doing now](../trends/README.md)
- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Projects**

- [OpenViking](openviking.md)
- [Projects](README.md)
- [RAGFlow](ragflow.md)

**Papers**

- [Papers: Vectorless retrieval](../papers/reasoning-over-structure.md)

**Benchmarks**

- [FRAMES](../benchmarks/frames.md)

**Experiments**

- [X3: Matched-cost comparison](../experiments/x3-matched-cost-comparison.md)

**Index**

- [Embedding](../index/embedding.md)
- [Knowledge compilation](../index/knowledge-compilation.md)
- [Prompt caching](../index/prompt-caching.md)
- [RAPTOR](../index/raptor.md)
- [Tree index](../index/tree-index.md)
- [Vector search](../index/vector-search.md)
- [Vectorless retrieval](../index/vectorless-retrieval.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/VectifyAI/PageIndex : repository metadata through the GitHub API (licence field, archived flag) (read 20261102 20:09 UTC; archived flag re-read 20261102 20:30 UTC)
2. https://github.com/VectifyAI/PageIndex/blob/main/LICENSE : licence text, through the API licence endpoint (read 20261102 20:10 UTC)
3. https://github.com/VectifyAI/PageIndex/blob/main/README.md : idea, modes, Cloud table, Updates list, benchmark claims (read 20261102 20:10 UTC)
4. https://github.com/VectifyAI/PageIndex/releases/latest : v0.5.0 date and notes (read 20261102 20:10 UTC; tag and date re-read through the API 20261102 20:30 UTC)
5. https://github.com/VectifyAI/Mafin2.5-FinanceBench : README, evaluation protocol, 98.7% and its base models; repository creation date re-read through the API (read 20261102 20:10 UTC and 20:30 UTC)
6. https://github.com/VectifyAI/pageindex-benchmarks : financial-qa README, findings and results table (read 20261102 20:10 UTC)
7. https://github.com/VectifyAI/PageIndex/tree/main/cookbook/pageindex-vs-vector-10k : notebook markdown and saved output (read 20261102 20:12 UTC)
8. https://github.com/VectifyAI/PageIndex/tree/main/pageindex : tree node fields, Standard mode, agent tools (read 20261030 19:29 to 19:36 UTC, via the archive page ../../kb-kg/projects/pageindex.md)
9. ../../kb-kg/projects/pageindex.md : the archive page, for the label counts of the 150 Mafin answers and its reading of papers 10 to 12, with the archive's own sources (read 20261030 19:30 to 19:35 UTC)
10. https://arxiv.org/abs/2511.18177 : Lumer et al., "Rethinking Retrieval ...", abstract (read 20261102 20:11 UTC)
11. https://arxiv.org/abs/2604.14222 : Hashmi, "Adaptive Query Routing ...", abstract of v2: three configurations, proposed method, evidence-snippet corpus, caveat (read 20261102 20:29 UTC)
12. https://arxiv.org/abs/2610.11370 : "RIT-RAG: Navigating Document Corpora with Retrieval-Induced Trees", abstract (read 20261102 20:11 UTC)
13. https://github.com/infiniflow/ragflow/blob/main/docs/guides/knowledge_compilation/built_in_templates_and_dedicated_configuration.md : the PageIndex template text (read 20261102 20:11 UTC)
14. https://github.com/VectifyAI/PageIndex/blob/main/README.md : the "Query cost and accuracy" section says "34 configurations of 19 LLMs"; the README was last changed 2026-10-27 14:06 UTC and the benchmark repository's first Financial QA commit (2026-10-23 14:58 UTC) is titled "34 LLM configurations", both through the GitHub API (read 20261102 22:31 UTC)
