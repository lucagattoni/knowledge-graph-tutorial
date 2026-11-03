---
type: benchmark
datasets: [hotpotqa]
updated: 20261102 21:23 UTC
---

# HotpotQA

This page answers how systems are scored on HotpotQA, what the official leaderboards show, and what independent studies since 2025 report. The questions, size, licence and construction are on [the HotpotQA dataset page](../datasets/hotpotqa.md). The current rank-1 entries on the official boards are dated 20230807 (distractor) and 20210510 (fullwiki) [2]; recent numbers come from retrieval-augmented generation (RAG) studies with their own subsets and metrics.

## What it tests

Whether a system can answer a [multi-hop](../index/multi-hop-question-answering.md) question from several documents and also name the sentences that support the answer, so that its reasoning can be checked [1].

## Tasks, metrics and protocol

- **Task.** Predict an answer (a span or yes/no) and the supporting sentences, in the distractor or the fullwiki setting (both described on the dataset page) [1][2].
- **Metrics.** Answer and supporting-fact [exact match](../index/exact-match.md) (EM) and F1. Joint F1 multiplies the answer and supporting-fact precisions, and the recalls, then takes the harmonic mean. Joint EM is 1 only if both are exact [1].
- **Submission.** Script `hotpot_evaluate_v1.py`. Fullwiki: upload predictions. Distractor: submit code and a Docker environment, through CodaLab [3].
- **Variants in later work (not official).** Contain EM, a more lenient score that counts an answer found anywhere in the output [5]; F1 on a generated answer [4]; [nDCG@10](../index/ndcg.md) for paragraph retrieval in [BEIR](beir.md) [7]; EM that also requires the right evidence pages in [KILT](kilt.md) [8].
- **Subsets.** The full dev set [5]; 1,000 hard bridge dev questions [4]; 1,000 sampled questions with a corpus pooled from their passages [6].

## Datasets

One dataset: [HotpotQA](../datasets/hotpotqa.md). The subset used changes the score.

## Results

Rows are not comparable across studies. Leaderboard rows are submitted by the teams themselves: for the distractor setting the organisers run the submitted code on the test set; for fullwiki they score an uploaded prediction file [3]. Whether any row was reproduced independently is **unstated**.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Baseline, distractor test | answer 45.46 / 58.99; support 22.24 / 66.62; joint 12.04 / 41.37 | EM / F1 | HotpotQA authors | yes | 20180925 | [1] Table 4 |
| Baseline, fullwiki test | answer 25.23 / 34.40; support 5.07 / 40.69; joint 2.63 / 17.85 | EM / F1 | HotpotQA authors | yes | 20180925 | [1] Table 4 |
| Human, 1,000 sampled questions | answer 83.60 / 91.40; support 61.50 / 90.04; joint 52.30 / 82.55 | EM / F1 | HotpotQA authors | yes | 20180925 | [1] Table 8 |
| Single-paragraph BERT, distractor dev; open (fullwiki) | 67.08; 38.40 | F1 | Min et al. | independent | 20190607 | [10] Table 1 |
| Beam Retrieval, distractor rank 1 | answer 72.69 / 85.04; support 66.25 / 90.09; joint 50.53 / 77.54 | EM / F1 | BUPT and Tencent | no (team submission) | 20230807 | [2][3] |
| AISO, fullwiki rank 1 | answer 67.46 / 80.52; support 61.17 / 86.02; joint 44.87 / 72.00 | EM / F1 | ICT, Chinese Academy of Sciences | no (team submission) | 20210510 | [2][3] |
| RAG; HippoRAG 2; Community-GraphRAG (Local), with Llama 3.1-8B; with 70B | 60.04; 63.01; 61.66; with 70B 63.88; 64.93; 64.60 | F1 | Han et al. | independent | 20260304 | [4] Tables 1, 8 |
| Dense vs best of five GraphRAG backends: Qwen2.5-7B single-shot; GraphSearch-7B; Search-R1-7B vs Graph-R1-7B | 19.00 vs 46.70; 38.22 vs 58.64; 35.76 vs 53.42 | Contain EM | Fan et al. (RAGSearch) | independent | 20260401 | [5] Table 1 |
| Paragraph retrieval: BM25; DPR; BM25 + cross-encoder | 0.603; 0.391; 0.707 | nDCG@10 | BEIR authors | yes (for BEIR) | 20211021 | [7] Table 2 |
| KILT knowledge source, test: RAG; BART + DPR; BART alone (implicit knowledge) | 26.97; 25.18; 15.37 | downstream EM | KILT authors | yes (for KILT) | 20210527 | [8] Table 3 |
| Same, RAG with the right evidence pages required | 3.21 | KILT-EM | KILT authors | yes (for KILT) | 20210527 | [8] Table 5 |

The Han et al. sample is 1,000 hard bridge dev questions [4]. Each graph entry in Fan et al. is the best of five GraphRAG variants [5].

*Reading:* on trained readers the distractor joint F1 rose from 41.37 (2018 baseline) to 77.54 (20230807), against a human 82.55 on a sample [1][2]. For LLM-based RAG the picture depends on setup. Han et al. see graph methods ahead of plain RAG by 1.6 to 3.0 F1 points with an 8B reader and 0.7 to 1.1 with a 70B reader [4]. Fan et al. see gaps of 17.7 to 27.7 points, from a setup that favours the graph side (below) [5].

## Known problems

- **Confounded gap in RAGSearch.** The dense backend retrieves from the 2018 Wikipedia dump; the GraphRAG backends use "the context of each question as the document" [5]. Each graph score is the maximum over five variants, and the RL agents are trained on HotpotQA and NQ [5]. *Reading:* the gaps mix a corpus difference and a best-of-five selection with the effect of the graph.
- **Inconsistent figure.** Graph-R1-7B scores 53.42 in Table 1 and 51.75 in Table 4 of the same paper; the reason is **unstated** [5].
- **Graph coverage.** In Han et al., only 65.8% of answer entities appear in the knowledge graph one pipeline builds for HotpotQA [4].
- **Board.** The newest dated fullwiki row is 20240625 [2]. The board's baseline row (answer 45.60 / 59.02, dated 20181010) differs slightly from the paper's Table 4; the reason is **unstated** [1][2]. Some fullwiki rows show 0.00 for supporting facts and joint scores [2].
- **Shortcuts and contamination.** Shortcut questions are on the dataset page. Whether current models saw the questions in training is **unstated** (see [contamination](../index/data-contamination.md)).

## Used by

- **Benchmarks:** [KILT](kilt.md), [BEIR](beir.md), [RAGSearch](ragsearch.md); [GraphRAG-Bench](graphrag-bench-xiang.md) argues existing sets cannot test graph structure [9].
- **Studies:** [RAG vs GraphRAG](../papers/graph-based-rag.md) (Han et al.); RAGSearch (Fan et al.).
- **Systems scored:** [HippoRAG 2](../projects/hipporag.md), [Microsoft GraphRAG](../projects/microsoft-graphrag.md) [4][5].
- **Trends:** [graph-based RAG](../trends/graph-based-rag.md), [agentic graph retrieval](../trends/learned-graph-traversal.md), [agentic search](../trends/agentic-search.md).

## Sources

1. https://arxiv.org/abs/1809.09600 : HotpotQA paper v1 (25 Sep 2018), full text at arxiv.org/html/1809.09600: metrics, Tables 4 and 8 (read 20261102 20:41 UTC)
2. https://hotpotqa.github.io/ : distractor and fullwiki leaderboards, rows and dates (read 20261102 20:41 UTC)
3. https://raw.githubusercontent.com/hotpotqa/hotpot/master/README.md : evaluation script, prediction format, submission (read 20261102 20:41 UTC; re-read 20261102 21:20 UTC)
4. https://arxiv.org/abs/2502.11371 : Han et al., "RAG vs. GraphRAG", v3 (4 Mar 2026), full text: Tables 1 and 8, appendices A and C (read 20261102 20:42 UTC)
5. https://arxiv.org/abs/2604.09666 : Fan et al., "Do We Still Need GraphRAG?" (RAGSearch), v1 (1 Apr 2026), full text: Table 1 and its caption (best of five GraphRAG variants), Table 4, setup, appendices (read 20261102 20:42 UTC; Tables 1 and 4 and the setup re-read 20261102 21:20 UTC)
6. https://arxiv.org/abs/2405.14831 : HippoRAG v3, full text: 1,000-question samples and pooled corpus (read 20261102 20:42 UTC)
7. https://arxiv.org/abs/2104.08663 : BEIR v4 (21 Oct 2021), full text: Table 2, HotpotQA row (read 20261102 20:42 UTC)
8. https://arxiv.org/abs/2009.02252 : KILT v4 (27 May 2021), PDF: Table 3 (downstream test scores, HotpotQA column: 26.97, 25.18, 15.37), Table 5 (KILT scores on test: 3.21), Table 14 (HotpotQA appendix) (read 20261102 21:20 UTC)
9. https://arxiv.org/abs/2506.05690 : Xiang et al., GraphRAG-Bench, v3 (22 Feb 2026), full text: existing benchmarks "fail to adequately evaluate" graph structures (read 20261102 20:42 UTC)
10. https://arxiv.org/abs/1906.02900 : Min et al., ACL 2019, arXiv v1 (7 Jun 2019), PDF: Table 1 (single-paragraph BERT 67.08 distractor F1 on the validation set, 38.40 open F1) (read 20261102 21:22 UTC)
