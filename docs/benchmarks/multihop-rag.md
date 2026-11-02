---
type: benchmark
datasets: [multihop-rag]
updated: 20261102 21:20 UTC
---

# MultiHop-RAG

The MultiHop-RAG benchmark asks how well a [retrieval-augmented generation](../index/retrieval-augmented-generation.md) pipeline finds and combines evidence from several news articles, and whether it refuses when no evidence exists. This page gives the tasks, metrics and published results. The articles and questions are described on [the dataset page](../datasets/multihop-rag.md).

## What it tests

Two abilities, measured separately [1]: **retrieval** (does the system bring back all the evidence a multi-hop query needs?) and **answering** (given retrieved text or the true evidence, is the short answer right, including "insufficient information" for null queries?). The authors say earlier RAG benchmarks mainly test single-evidence queries [1].

## Tasks, metrics and protocol

As published by the authors (v1, 20240127) [1]:

| Part | Setting |
|---|---|
| [Chunking](../index/chunking.md) | 256-token chunks, LlamaIndex; overlap not stated in the paper [1] (200, the LlamaIndex default, according to [2]) |
| Retrieval | cosine similarity, eight [embedding](../index/embedding.md) models; 20 chunks fetched, optionally [reranked](../index/reranking.md) with bge-reranker-large to top-K |
| Retrieval metrics | MAP@K, MRR@K, Hit@K (fraction of evidence found in the top K); null queries excluded |
| Generation, setting 1 | top-6 reranked chunks (at most 2,048 tokens) from the best retriever; all 2,556 queries |
| Generation, setting 2 | the true evidence as context; null queries excluded |
| Answer metric | accuracy against the short gold answer; the matching rule is not defined in the paper |

The repository has moved on [5]: an accuracy metric (20250403), hybrid and agentic RAG workflows (20260716), and a default chunk overlap of 25 instead of 200 (commit 20260915). Today's scripts do not reproduce the 20240127 chunking. Published results for the new workflows: **unstated**.

## Datasets

[MultiHop-RAG](../datasets/multihop-rag.md): all queries in generation setting 1, null queries excluded from retrieval metrics and setting 2 [1].

## Results

Each number re-read from its source on 20261102. Rows use different protocols; do not compare across rows.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| voyage-02 + bge-reranker-large | Hits@10 0.7467, Hits@4 0.6625, MRR@10 0.586 | retrieval | benchmark authors | yes | 20240127 | [1] |
| GPT-4: retrieved chunks / true evidence | 0.56 / 0.89 | accuracy | benchmark authors | yes | 20240127 | [1] |
| Claude-2.1; PaLM; Llama-2-70b-chat (same two settings) | 0.52 / 0.56; 0.47 / 0.74; 0.28 / 0.32 | accuracy | benchmark authors | yes | 20240127 | [1] |
| voyage-02 + reranker, re-run (chunk overlap 32) | Hits@10 0.7419, Hits@4 0.6630 | retrieval | Poliakov and Shvai | not the benchmark's authors | 20240819 | [2] |
| Multi-Meta-RAG (metadata filter) + voyage-02 | Hits@10 0.9042, Hits@4 0.792; GPT-4 accuracy 0.606 (any-word match, see note) | retrieval; accuracy | Poliakov and Shvai | first-party (their method) | 20240819 | [2] |
| gpt-4o-mini: NaiveRAG / [GraphRAG](../index/graphrag.md) / LightRAG / MiniRAG | 53.60 / 60.92 / 64.91 / 68.43 | accuracy % | MiniRAG authors | first-party (their method) | 20250126 | [3] |
| Llama-3.1-8B: RAG / RAPTOR / Community-GraphRAG Local / Global / HippoRAG2 | 67.02 / 68.78 / 69.01 / 64.40 / 70.27 | overall accuracy % | Han et al. | independent | 20260304 | [4] |
| same, null queries | 96.01 / 90.03 / 80.07 / 19.27 / 85.71 | accuracy % | Han et al. | independent | 20260304 | [4] |
| same, temporal queries | 30.70 / 45.28 / 50.60 / 53.34 / 49.91 | accuracy % | Han et al. | independent | 20260304 | [4] |
| Llama-3.1-8B: RAG / Community-GraphRAG Local, graph by GPT-4o-mini / by GPT-4o | 67.02 / 69.01 / 68.74 | overall accuracy % | Han et al. | independent | 20260304 | [4] |
| Llama-3.1-70B: RAG / Community-GraphRAG Local, graph by GPT-4o-mini / by GPT-4o | 65.77 / 71.17 / 75.08 | overall accuracy % | Han et al. | independent | 20260304 | [4] |
| Pinakes 0.32.8 free search | every gold article in the first 8 passages 43.4% (95% interval 41.3 to 45.4); at least one 96.8% | share of 2,255 answerable queries | this documentation's owner | first-party for Pinakes | 20261030 | [6] |

The Pinakes figure counts whole articles, not the fraction of evidence, so it is not comparable with Hit@K [6]. Han et al. use 256-token chunks, top-10 and graphs built by GPT-4o-mini [4]; MiniRAG 1,200-token chunks and top-5 [3]. Poliakov and Shvai score accuracy by "checking if any word in an LLM-generated response is present in the correct gold answer", a lenient rule; their text says 0.63 where their Table 3 says 0.606 [2]. So 0.606 does not compare with the authors' 0.56, whose matching rule is undefined [1].

*Reading:* only Han et al. is independent of every method it scores. It shows a narrow graph lead overall (70.27 against 67.02 on 8B) that comes from temporal and comparison queries; RAG is ahead on inference, and Community-GraphRAG Global is far behind on null queries. A stronger graph builder helps at 70B (65.77 for RAG, 71.17 with a GPT-4o-mini graph, 75.08 with GPT-4o) but not at 8B (69.01 with GPT-4o-mini, 68.74 with GPT-4o) [4]. The MiniRAG row shows how far protocol moves a system class: its NaiveRAG scores 53.60, Han et al.'s RAG 67.02 [3][4].

## Known problems

- **Two query sets in one table.** Retrieved-chunk accuracy includes null queries; true-evidence accuracy excludes them, so the two columns are not like for like [1].
- **Reading and retrieval are mixed** in setting 1 [1].
- **Abstention is scored only in the generation columns.** Null queries are excluded from retrieval metrics and from setting 2 [1]. In Han et al. every other method scores below RAG on null queries [4]. *Reading:* it is a hypothesis, untested here, that the wording difference described on the dataset page inflates abstention scores. The one test found is on a different system: the Pinakes README re-checked its abstention score on 18 null questions without the wording tells and got AUROC 0.945 against 0.944 on all null questions, so "not an artefact of wording" there, from a small sample (n=18) [6].
- **A metadata filter is a shortcut on this data.** Multi-Meta-RAG gains from it; its authors call the filter specific to a domain and question format [2].
- **A weak test of graph structure.** Xiang et al., authors of a competing benchmark, argue that this set and similar ones do not test graph structure well; the density figures are on the dataset page [7].
- **No leaderboard** was found: **unstated**. Comparisons rest on individual papers.

## Used by

[Graph-based RAG](../trends/graph-based-rag.md) comparisons: Han et al. ([group page](../papers/graph-based-rag.md)), which scores HippoRAG 2 ([HippoRAG](../projects/hipporag.md)) [4]; MiniRAG ([GitHub](https://github.com/HKUDS/MiniRAG)), which scores [LightRAG](../projects/lightrag.md) [3]; Multi-Meta-RAG [2]. Related: [GraphRAG-Bench (Xiang)](../benchmarks/graphrag-bench-xiang.md) [7].

## Sources

1. https://arxiv.org/html/2401.15391 : Tang and Yang, v1 20240127: protocol, Tables 5 and 6, limitations; no chunk overlap stated (read 20261102 21:19 UTC)
2. https://arxiv.org/html/2406.13213 : Poliakov and Shvai, Multi-Meta-RAG, v2 revised 20240819: Tables 2 and 3, chunk overlap 32 against the original's 200, any-word accuracy rule, 0.63 in text (read 20261102 21:17 UTC)
3. https://arxiv.org/html/2501.06713 : Fan et al., MiniRAG, v3 revised 20250126: MultiHop-RAG table, settings (read 20261102 20:45 UTC)
4. https://arxiv.org/html/2502.11371 : Han et al., RAG vs. GraphRAG, v3 revised 20260304: Tables 2, 5, 9, 27 and 28, settings (read 20261102 21:17 UTC)
5. https://github.com/yixuantt/MultiHop-RAG : commit list and the diff of commit 8475a31 (20260915) through the GitHub API (read 20261102 21:17 UTC)
6. https://github.com/lucagattoni/pinakes-datasets-benchmark : README of the public repository (run `20261030_1826-baseline-pypi-0.32.8`; main at commit 7bbed5f, 20261102 20:02 UTC) (read 20261102 21:17 UTC)
7. https://arxiv.org/html/2506.05690 : Xiang et al., GraphRAG-Bench, v3, Table 9 and introduction (read 20261102 21:17 UTC)
