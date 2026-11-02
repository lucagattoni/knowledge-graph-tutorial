---
type: benchmark
datasets: []
updated: 20261102 21:08 UTC
---

# STaRK

This page answers what STaRK measures, how its three knowledge bases and queries were made, and what the published scores show. STaRK has no dataset page of its own, because its data is used mainly inside its own protocol (one 2026 paper reuses the Prime human queries with other metrics, see Results); the data is described below. Its paper has 94 citations (Semantic Scholar, read 20261102 20:01 UTC) [13]. The official leaderboard could not be read, so the results come from papers.

## What it tests

It tests retrieval when a query has a text part and a relation part together, for example "papers by a given author on a given topic". Each knowledge base is a [knowledge graph](../index/knowledge-graph.md) plus free text for every node, and the answer is a set of nodes. The authors say earlier work treated text-only retrieval, SQL and graph queries as separate problems [1].

## Tasks, metrics and protocol

- **Task:** given the graph, the documents and a query, return the matching nodes. **Metrics:** Hit@1, Hit@5, Recall@20 and [MRR](../index/mean-reciprocal-rank.md) [1].
- **Baselines:** [BM25](../index/bm25.md), small and LLM-based [dense retrievers](../index/dense-retrieval.md), multivector retrievers, and [reranking](../index/reranking.md) of the top 20 ada-002 results by GPT-4 Turbo or Claude 3 Opus, run on a random 10% of the test queries because of cost [1]. Human-written queries are test only [1].

## Datasets

**Contents.**

| Knowledge base | Entities | Relations | Text tokens | Synthesised queries (train / val / test) | Human-written |
|---|---|---|---|---|---|
| Amazon (products) | 1,035,542 | 9,443,802 | 592M | 9,100 (0.65 / 0.17 / 0.18) | 81 |
| MAG (papers) | 1,872,968 | 39,802,116 | 213M | 13,323 (0.60 / 0.20 / 0.20) | 84 |
| Prime (biomedicine) | 129,375 | 8,100,498 | 32M | 11,204 (0.55 / 0.20 / 0.25) | 98 |

Sources: Amazon reviews and Q&A; ogbn-mag with the Microsoft Academic Graph; PrimeKG with text from other biomedical databases [1].

**Made.** Four steps: sample a relation template, have an LLM extract text properties of a sampled gold node, merge both into a query with two LLMs, then keep only candidates that several LLMs verify against the text part. The gold answer passes this check in 86.6%, 98.9% and 92.3% of cases; what happens to the rest is unstated. 63 raters rated 94.1% of queries neutral or better on naturalness, 85.3% on diversity, 89.4% on practicality. 31 participants wrote the 263 human queries [1].

**Versions.** First arXiv version 20240419 [6]; human queries added May 2024; v3 and the leaderboard, October 2024; NeurIPS 2024 Datasets and Benchmarks track [3][6]. Dataset card last changed 20241020 [5]; code last pushed 20260206 [4].

**Licence.** The Hugging Face card says CC BY 4.0 and the code is MIT [2][3][4]. The paper says the authors "adhered to the licenses of each public resource"; whether CC BY 4.0 fits every source's terms is unstated [1].

## Results

Hit@1 on Amazon / MAG / Prime. The 10% sample rows are the fair comparison for the rerankers. Rows are comparable only inside a block.

| System | Score | Metric, set | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| BM25; ada-002; GritLM-7b; ColBERTv2 | 44.94 / 25.85 / 12.75; 39.16 / 29.08 / 12.63; 42.08 / 37.90 / 15.57; 46.10 / 31.18 / 11.75 | full synthesised test | STaRK authors | yes | 20241020 | [1] |
| BM25 on the 10% sample | 42.68 / 27.81 / 13.93 | 10% sample | STaRK authors | yes | 20241020 | [1] |
| GPT-4 reranker; Claude 3 reranker | 44.79 / 40.90 / 18.28; 45.49 / 36.54 / 17.79 | 10% sample | STaRK authors | yes | 20241020 | [1] |
| AF-Retriever (zero-shot, GPT OSS 120B) | 61.2 / 78.6 / 46.2 | synthesised test sets | its authors | independent of the STaRK authors; first-party for its system | 20250514 (v4 20260514) | [9] |
| ARK (training-free, GPT-4.1) | 55.82 / 73.40 / 48.20 | synthesised test sets (size of the evaluated set unstated) | its authors | same | 20260120 (v2 20260428) | [10] |
| GRASP (trained planner and reranker) | 75.5 / 89.1 / 77.3 | full synthesised test (1,642 / 2,665 / 2,801 queries) | its authors | same | 20260528 (v3 20261015) | [11] |
| Claude 3.7 Sonnet, documents only; with 1-hop relation lists | 0.6147; 0.6972 | Prime human queries; Hit@1 of the model's final entity list | Chen et al. (AWS, Cisco) | independent; not comparable with rows above | 20260624 | [12] |
| same, agent with a document tool only; agent with document tool plus graph tool | 0.6881; 0.6055 | same | same | same | 20260624 | [12] |
| GraphRAG with the predefined graph only (Scenario 3, not an agent; at most 100 paths) | 0.1376 | same | same | same | 20260624 | [12] |
| Papr v2; Papr v1 | 83.19; 80.53 (MAG only) | `test-0.1` split, as recorded in the submission file | the vendor | yes (vendor's own submission); status "approved", not recomputed; v1 note: ran 1,000 queries and padded short lists by repeating the last id | 20260108; 20250205 | [8] |

*Reading:* the 2024 baselines were far from saturated. Later systems add an LLM that parses the query into relational constraints, plans graph steps or controls search, and gain most on MAG and Prime. All numbers come from the systems' own authors, and trained and training-free methods sit side by side, so the table ranks no method. Chen et al. find that adding a graph tool to a document agent lowers Hit@1 (0.6881 to 0.6055), and that search over the graph alone scores 0.1376 [12].

## Known problems

- **Leaderboard down.** The Hugging Face leaderboard space returned HTTP 503 and shows a build error on 20261102; its rows are unread [7]. Its repository holds two approved, one pending and one rejected self-submitted entry; the note about 1,000 queries and padded lists belongs to Papr v1 (80.53) [8]. Papr v2 records Recall@20 and MRR as 0.0, so only Hit@1 and Hit@5 are usable [8].
- **Small human sets.** 81, 84 and 98 queries, so one query moves Hit@1 by about one point [1].
- **Paper inconsistencies.** The introduction says 274 human queries, Section 2.6 says 263 (81 + 84 + 98 = 263). Table 7 lists BM25 on Amazon with MRR 18.79 below Hit@1 27.16, which cannot hold [1].
- **Unlike metrics.** Chen et al. score the final entity list; their Hit@1 values are multiples of 1/109, so their test set is not the 98 queries the paper lists (my inference) [1][12].

## Used by

Chen et al. [12], discussed in [Agentic graph retrieval](../trends/learned-graph-traversal.md); AF-Retriever, ARK and GRASP [9][10][11].

## Sources

1. https://arxiv.org/html/2404.13207 : STaRK paper v3 (20241020): Tables 2, 3, 6, 7, Sections 2 and 3, licence note (read 20261102 20:54 UTC)
2. https://huggingface.co/datasets/snap-stanford/stark/raw/main/README.md : card, `cc-by-4.0` (read 20261102 20:54 UTC)
3. https://raw.githubusercontent.com/snap-stanford/stark/main/README.md and https://raw.githubusercontent.com/snap-stanford/stark/main/LICENSE : news, NeurIPS, MIT (read 20261102 20:54 UTC)
4. GitHub API for snap-stanford/stark : MIT, last push 20260206 (read 20261102 20:54 UTC)
5. https://huggingface.co/api/datasets/snap-stanford/stark : last modified 20241020 (read 20261102 21:00 UTC)
6. arXiv API record of 2404.13207 : first version 20240419, comment "NeurIPS 2024 Track on Datasets and Benchmarks" (read 20261102 21:01 UTC)
7. https://snap-stanford-stark-leaderboard.hf.space/ : HTTP 503; https://huggingface.co/api/spaces/snap-stanford/stark-leaderboard : stage BUILD_ERROR (read 20261102 20:57 UTC)
8. https://huggingface.co/spaces/snap-stanford/stark-leaderboard : files under `submissions/` (metadata files of Papr v2 and Papr v1, one pending entry, one rejected test entry) (read 20261102 21:28 UTC)
9. https://arxiv.org/html/2505.09246v4 : AF-Retriever, Table 3 (read 20261102 20:59 UTC)
10. https://arxiv.org/html/2601.13969v2 : ARK, Table 1 (read 20261102 20:59 UTC)
11. https://arxiv.org/html/2605.30237v3 : GRASP, Table 1, test sizes (read 20261102 20:59 UTC)
12. https://arxiv.org/html/2606.25656 : Chen et al., Table 1 (Scenarios 1 to 9), Section 3 and setup (read 20261102 21:28 UTC)
13. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 94 for arXiv 2404.13207 (read 20261102 20:01 UTC, carried over from the research notes)
