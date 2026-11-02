---
type: benchmark
datasets: [longmemeval]
updated: 20261102 21:20 UTC
---

# LongMemEval

This page describes how LongMemEval scores [agent memory](../index/agent-memory.md): what is asked, how answers are judged, and what systems have scored. The questions, abilities, evidence labels and file versions are on the [LongMemEval dataset page](../datasets/longmemeval.md). The numbers below use different readers, judges and file versions, so they are not a ranking.

## What it tests

The long-term memory of a chat assistant: sessions arrive one by one, a question follows the last. The questions cover five abilities, listed on the [dataset page](../datasets/longmemeval.md) [1][2].

## Tasks, metrics and protocol

- **Task.** The system gets the timestamped sessions in order, then a dated question, and answers [2][3].
- **Metric.** Accuracy, judged by a [large language model](../index/large-language-model.md) used as a [judge](../index/llm-as-judge.md): `gpt-4o-2024-08-06` with a prompt per question type. The paper reports more than 97% agreement with human experts [2]. The repository script takes the judge as an argument (its example: `gpt-4o`) and reads a JSON-lines file of `question_id` and `hypothesis` [3].
- **Retrieval metrics.** Recall@k and NDCG@k, if the system exposes its retrieval, scored against the evidence labels described on the dataset page [2][3].
- **Paper's design findings.** It splits a memory system into indexing, retrieval and reading. Index keys expanded with extracted user facts raised recall@k by 9.4% and accuracy by 5.4% on average; Chain-of-Note reading gained up to 10 points [2].

## Datasets

The data is the [LongMemEval dataset](../datasets/longmemeval.md). LongMemEval-V2 is a separate benchmark on web-agent trajectories with its own leaderboard [8].

## Results

Dates are paper dates. First-party: the system's authors scored it. Rows from Bao et al. (20261022) are either measured by them (Raw-RAG) or published scores they retained; their Appendix A says "Published baseline scores are retained, and Raw-RAG results are measured in this study" [6]. Their Table 3 does not mark which is which; the appendix and its review of prior work do, as noted per row.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| GPT-4o, full history | 0.9184 | accuracy, 97-question pilot, 3-6 sessions | benchmark authors | own benchmark | 20241014 | [2] |
| ChatGPT memory; Coze (both GPT-4o) | 0.5773; 0.3299 | same pilot | benchmark authors | independent of both | 20241014 | [2] |
| GPT-4o; Llama 3.1 70B, oracle vs S | 0.870 vs 0.606; 0.744 vs 0.334 | accuracy | benchmark authors | own benchmark | 20250304 | [2] |
| Zep vs full context, gpt-4o; gpt-4o-mini | 71.2% vs 60.2%; 63.8% vs 55.4% | accuracy, S | Zep authors | first-party | 20250120 | [4] |
| Hindsight, Gemini-3 Pro / OSS-120B / OSS-20B | 91.4% / 89.0% / 83.6% (full context, OSS-20B: 39.0%) | accuracy, S | Hindsight authors | first-party | 20251214 | [5] |
| Raw-RAG: text-embedding-3-small with Cohere Rerank-v3.5; Qwen3-Embedding-4B with Qwen3-Reranker-4B | 87.53; 89.93 | accuracy, S, 500 questions, GPT-4.1-mini reader, each answer judged three times by GPT-4o-mini and averaged | Bao et al. (measured) | the authors' own baseline | 20261022 | [6] |
| Memora | 87.40 | accuracy, S, 500 questions, GPT-4.1-mini | Memora authors (published result, Memora's own retriever); reused by Bao et al. | first-party | Memora's date unstated; reused 20261022 | [6] |
| EMem | 83.00 | accuracy, S, 470 non-abstention questions | published score retained by Bao et al. (EMem is their ref. 59); source per Appendix A | not marked in Table 3 | unstated; reused 20261022 | [6] |
| EverMemOS; MemOS; Mem0 | 83.00; 77.80; 66.40 | accuracy, S, 500 questions, GPT-4.1-mini | the published EverMemOS baseline set (EverMemOS paper, Appendix A.2.2), retained by Bao et al.; who ran Mem0 and MemOS inside that set is unstated | EverMemOS: first-party, as the set is from its own paper; Mem0, MemOS: unstated | unstated; reused 20261022 | [6] |
| Full context | 65.60 | accuracy, S, 500 questions, GPT-4.1-mini | reported in the Memora paper, per Bao et al. Appendix E | the Memora authors' own baseline | unstated; reused 20261022 | [6] |
| Gemini-3-Flash (long context) | 83.00 | accuracy, LME (S*) subset | EvoMemBench authors | independent | 20261030 | [7] |
| BM25; Mem0; A-MEM (DeepSeek-V3.2) | 50.33; 52.00; 51.00 | same | EvoMemBench authors | independent of those systems | 20261030 | [7] |

The S* subset is MemoryAgentBench's re-cut, not the 500 questions [7][10]. Independent results on the full 500 questions are few: the benchmark authors' pilots and Bao et al.'s measured Raw-RAG rows [6].

*Reading:* in one 2026 study a plain retrieval baseline matched or beat the published memory-system scores in the compared settings: 87.53 against Memora's 87.40 is a margin of 0.13 points (computed), under a three-judgment GPT-4o-mini protocol rather than the official judge [6]. In another study a long-context model topped the other systems on the S* subset, with different underlying models [7]. In the Zep paper, and in Hindsight's smallest-reader row (83.6% against 39.0%), the memory system beat full context, each reported by its own authors under their own reader and judge [4][5]. Gains over full context therefore depend on reader and judge; no row here settles it.

## Known problems

- **No official leaderboard** for this version: the project page and the README name none [3][9]. Scores sit in vendor pages and papers.
- **Judges differ.** The official judge is `gpt-4o`. Hindsight judges its own runs with GPT-OSS-120B and takes its baseline rows from another vendor's report, which used a `gpt-4o` judge [5]. Bao et al. judge Raw-RAG with GPT-4o-mini; the passages read do not name the judges behind the baseline scores they retain [6].
- **Readers, files and subsets differ** across rows (S, S* or oracle; original or cleaned files, see the [dataset page](../datasets/longmemeval.md)).
- **Provenance is only partly marked.** Bao et al.'s appendix marks some rows as published scores (Memora, the EverMemOS baseline set, and the 65.60 full-context figure), but Table 3 does not mark them, and it does not say that EMem's 83.00 belongs to a 470-question setting without abstention items rather than the full 500; that is in Appendix A.2.1 and A.2.3 [6].
- **Headline gains hide losses.** In the Zep paper, Zep with gpt-4o-mini scored below full context on single-session-assistant (75.0% against 81.8%) and knowledge-update (74.4% against 76.9%) [4].

## Used by

Zep, whose engine is [Graphiti](../projects/graphiti.md) [4]; [Hindsight](../projects/hindsight.md) [5]; Bao et al., with [Mem0](../projects/mem0.md) and [MemOS](../projects/memos.md) [6]; [MemoryAgentBench](memoryagentbench.md), which re-cuts it [10]; EvoMemBench [7]. Sibling: [LoCoMo](locomo.md). Trend: [agent memory](../trends/agent-memory.md); papers: [agent-memory papers](../papers/agent-memory.md).

## Sources

1. https://arxiv.org/abs/2410.10813 : abstract, five abilities, versions (read 20261102 20:41 UTC)
2. https://arxiv.org/html/2410.10813 : protocol, judge, pilots, oracle vs S table, design findings (read 20261102 20:41 UTC)
3. https://github.com/xiaowu0162/LongMemEval : README evaluation script and output format (read 20261102 20:41 UTC)
4. https://arxiv.org/html/2501.13956 : Zep paper, Tables 2 and 3, submitted 20250120 (read 20261102 20:42 UTC); introduction (Zep powered by Graphiti) re-read 20261102 21:19 UTC
5. https://arxiv.org/html/2512.12818 : Hindsight paper, Table 3, section 7, submitted 20251214 (read 20261102 20:44 UTC)
6. https://arxiv.org/html/2610.30755 : Bao et al., Table 3 (rows, 500-question columns), Appendix A intro, A.2.1 to A.2.3 (settings, judges, 470-question setting, published-result statements, Raw-RAG 87.53 and 89.93), Appendix E (Memora entry: the 65.60 result belongs to full context), submitted 20261022 (re-read 20261102 21:19 UTC)
7. https://arxiv.org/html/2605.18421 : EvoMemBench v3 (20261030), Table 3 (read 20261102 20:42 UTC)
8. https://github.com/xiaowu0162/LongMemEval-V2 : V2 README (read 20261102 20:44 UTC)
9. https://xiaowu0162.github.io/long-mem-eval/ : project page, no leaderboard (read 20261102 20:43 UTC)
10. https://arxiv.org/html/2507.05257 : MemoryAgentBench, LME (S*) (read 20261102 20:43 UTC)
