---
type: benchmark
datasets: [locomo]
updated: 20261102 21:18 UTC
---

# LoCoMo

This page answers how LoCoMo scores a system's memory of a very long conversation, and what the published scores are worth. Most recent numbers come from memory-system vendors with different pipelines. The conversations and questions themselves are described on [the LoCoMo dataset page](../datasets/locomo.md).

## What it tests

Memory of a dialogue spread over up to 35 sessions: answering questions about it, summarising its events, and keeping a persona consistent when generating the next turn [1][2]. The papers of Mem0, Zep and Bao et al. all report scores on it for [agent memory](../index/agent-memory.md) layers [5][8][6].

## Tasks, metrics and protocol

| Task | Metric | Where it is run |
|---|---|---|
| Question answering, five types | F1 on normalised answers; recall@k of evidence for retrieval models [2] | Scripts in the repository [3] |
| Event summarisation | ROUGE and FactScore (atomic-fact precision, recall, F1) [2] | "Coming soon!" in the repository [3] |
| Multimodal dialogue generation | MMRelevance and other generation metrics [2] | "Coming soon!" in the repository [3] |

The paper tested truncated-context models, a long-context model, and [retrieval-augmented](../index/retrieval-augmented-generation.md) generation (retriever DRAGON, reader gpt-3.5-turbo-16k) over three stores: dialogue turns, generated observations, session summaries [2]. The official scorer gives category 1 partial F1 over sub-answers, categories 2 to 4 plain F1 (category 3 gold answers are cut at the first semicolon), and category 5 a point when the output contains "no information available" or "not mentioned" [4].

Later work changed the protocol. Mem0 and Bao et al. score categories 1 to 4 with an [LLM judge](../index/llm-as-judge.md) [5][6]. LoCoMo-Plus reports an average over the five LoCoMo categories in a "LoCoMo (Factual Memory)" block; how it computes that average, and the judge settings of those columns, are **unstated** in the parts I read [7]. F1, judge and LoCoMo-Plus scores are three groups and cannot be compared with each other.

## Datasets

It uses the [LoCoMo dataset](../datasets/locomo.md). The F1 protocol scores all five categories of the released file; Mem0 and Bao et al. use categories 1 to 4. Sizes are on the dataset page.

## Results

The README shows no leaderboard [3]; the issue tracker holds self-reported submissions, not listed here. Groups use different metrics: compare within a group, not across. "First-party" means the system's own authors ran it; "benchmark authors" ran their baselines on their own benchmark.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Human | 87.9 | F1, all five types | benchmark authors | reference | 20240227 | [2] |
| GPT-4-turbo, 4,096 context | 32.1 | F1 | benchmark authors | no | 20240227 | [2] |
| GPT-3.5-turbo-16K, 16K context | 37.8 | F1 | benchmark authors | no | 20240227 | [2] |
| GPT-3.5-turbo-16K, top-5 observations | 41.4 | F1 | benchmark authors | no | 20240227 | [2] |
| gemini-2.5-pro | 71.78 | "average" column of Table 1, LoCoMo (Factual Memory) block; computation unstated | LoCoMo-Plus authors | no | 20260211 | [7] |
| gpt-4o | 62.99 | same | same | no | 20260211 | [7] |
| A-Mem (GPT-4o) | 59.64 | same | same | no | 20260211 | [7] |
| Mem0 (GPT-4o) | 57.24 | same | same | no | 20260211 | [7] |
| Raw-RAG, GPT-4o-mini / GPT-4.1-mini reader | 89.07 / 93.70 | judge accuracy, categories 1-4 | Bao et al. | yes, their own baseline | 20261022 | [6] |
| [MemMachine](https://github.com/MemMachine/MemMachine) | 88.12 / 91.69 | same | Bao et al. | no | 20261022 | [6] |
| EverMemOS | 86.76 / 93.05 | same | not marked in the table | unstated | 20261022 | [6] |
| Full context | 72.30 / 80.60 | same | not marked in the table | unstated | 20261022 | [6] |
| Mem0 | 66.88 / 64.20 | same | 66.88 is Mem0's published value | partly | 20261022 | [6] |
| Mem0 / Mem0 with graph / full context | 66.88 / 68.44 / 72.90 | judge score, categories 1-4 | Mem0 authors | yes (first two) | 20250428 | [5] |
| [Zep](https://github.com/getzep/zep) | 65.99 | same | Mem0 authors | no, run by a competitor | 20250428 | [5] |
| Zep | 75.14 | same | Zep authors | yes | 20250506, updated 20260603 | [8] |
| Zep | 58.44 | accuracy, categories 1-4 | Mem0's CTO | no, a competitor; Zep disputes it | 20250508 | [9] |

Bao et al. say Raw-RAG leads LoCoMo by 0.65 to 0.95 points [6]. Mem0's headline claim is "26% relative improvements" over OpenAI's memory [5].

## Known problems

- **No common pipeline.** Each vendor uses its own ingestion, answer prompt and sometimes model, so tables compare pipelines, not memory designs. Penfield, an interested party, says so [10]; the Zep and Mem0 dispute shows it. Mem0's CTO says Zep first reported 84% because its numerator counted category 5 and its denominator did not; Zep's own blog post, published two days earlier, gives 75.14 and does not contain the 84% [8][9]; Zep disputes the CTO's account.
- **Lenient judge.** Penfield reports that the judge accepted 62.81% of deliberately wrong but topical answers on the category 1 to 4 questions; I did not rerun it [10].
- **Mixed provenance.** Bao et al. keep published baseline scores and measure Raw-RAG themselves; they also note that Mem0's category scores, weighted by question counts, give 62.14, not the published 66.88 [6].
- **Paper inconsistency.** The text of the paper gives the best truncated-context model as 32.4; its Table 2 gives 32.1 [2].
- **Category 5.** Mem0, Zep and Bao et al. drop it, LoCoMo-Plus keeps it [5][6][8][7].
- **Full context is a strong baseline.** It beats Mem0 in Mem0's own table and in Bao et al.'s (rows above) [5][6].

*Reading:* Raw-RAG's 93.70 is above the 93.6% ceiling Penfield estimates for a perfect system [10][6]. Either the ceiling or the judge is loose; the headroom is small. A gain of a few points on this benchmark is not evidence of better memory.

## Used by

[Mem0](../projects/mem0.md) paper and Bao et al. ([agent-memory papers](../papers/agent-memory.md)) [5][6]; LoCoMo-Plus [7]; trend [agent memory](../trends/agent-memory.md). Bao et al. also run [LongMemEval](./longmemeval.md) and [MemoryAgentBench](./memoryagentbench.md) [6].

## Sources

1. https://arxiv.org/abs/2402.17753 : tasks, authors, v1 20240227 (read 20261102 20:41 UTC)
2. https://arxiv.org/html/2402.17753 : tasks, metrics, Tables 2, 3 and 4, text of section 6.1 (read 20261102 20:42 UTC)
3. https://github.com/snap-research/locomo : README, scripts, "Coming soon!" notes (read 20261102 20:41 UTC)
4. https://github.com/snap-research/locomo/blob/main/task_eval/evaluation.py : scorer by category, category 3 truncation at ";" (read 20261102 21:17 UTC)
5. https://arxiv.org/html/2504.19413 : Mem0 paper, Tables 1 and 2, headline claim, category 5 excluded (read 20261102 20:42 UTC)
6. https://arxiv.org/html/2610.30755 : Bao et al., Table 3, Appendix A (v1 20261022; read 20261102 20:42 UTC)
7. https://arxiv.org/html/2602.10715 : LoCoMo-Plus Table 1 (columns: five LoCoMo categories, average, LoCoMo-Plus, gap; average computation not defined), v1 20260211 (read 20261102 21:17 UTC)
8. https://www.getzep.com/blog/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/ : Zep 75.14, category 5 note, published 20250506 (read 20261102 20:44 UTC)
9. https://github.com/getzep/zep-papers/issues/5 : Mem0 CTO's 58.44, the 84% figure as the CTO states it, opened 20250508 (read 20261102 21:17 UTC)
10. https://dev.to/penfieldlabs/we-audited-locomo-64-of-the-answer-key-is-wrong-and-the-judge-accepts-up-to-63-of-intentionally-33lg : judge test, pipeline critique, published 20260404; author describes an agent-memory product (read 20261102 20:43 UTC)
