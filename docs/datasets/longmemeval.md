---
type: dataset
kinds: [questions, corpus]
benchmark: longmemeval
updated: 20261102 21:21 UTC
---

# LongMemEval

This page describes the data of LongMemEval: 500 questions about facts hidden inside long, timestamped chat histories between a user and an AI assistant. It answers what the files contain, which version to use, and under what licence. Scoring and results are on the [LongMemEval benchmark page](../benchmarks/longmemeval.md).

## What it contains

Each of the 500 instances holds a question, its answer, the question date and a "haystack": dated user-assistant sessions in which the evidence is buried [1][3]. Evidence turns carry `has_answer: true`, and `answer_session_ids` names the evidence sessions [3]. Five abilities are probed: information extraction, multi-session reasoning, temporal reasoning, knowledge updates and abstention [1].

`question_type` has six values; an id ending in `_abs` marks an abstention question inside one of them [3]. Counted in the oracle file [5]:

| Type | Questions |
|---|---|
| temporal-reasoning | 133 |
| multi-session | 133 |
| knowledge-update | 78 |
| single-session-user | 70 |
| single-session-assistant | 56 |
| single-session-preference | 30 |

Thirty are abstention items (multi-session 12, others 6 each across three types) [5]: false-premise versions of questions from other types [2].

## Size and versions

| File | History per question | Source |
|---|---|---|
| `longmemeval_s` | about 115k tokens, about 40 sessions (Llama 3 tokenisation) | [2][3] |
| `longmemeval_m` | about 500 sessions, about 1.5M tokens | [2][3] |
| `longmemeval_oracle` | evidence sessions only; mean 1.9 sessions per instance, counted | [3][5] |

The paper has two versions: v1 of 20241014 and v2 of 20250304; it appeared at ICLR 2025 [1][3]. A cleaned release of September 2025 "replaces the original LongMemEval dataset" and "removes noisy history sessions that interfere with the answer correctness". It lives in a separate Hugging Face repository, created 20250919, with the splits `longmemeval_oracle`, `longmemeval_s_cleaned` and `longmemeval_m_cleaned` [3][4]. How many sessions were removed is **unstated**: the card links a change-log spreadsheet that was not opened [4]. The GitHub README still names `longmemeval_s.json`, the Hugging Face files carry `_cleaned` [3][4].

LongMemEval-V2 is a different dataset: 451 questions over web-agent trajectories [11].

## Licence

MIT. The repository `LICENSE` file reads "MIT License, Copyright (c) 2024 Di Wu" [3], and the Hugging Face card says `license: mit` [4]. The filler sessions come from ShareGPT and UltraChat. The paper states that these are Apache 2.0 and MIT respectively, and that questions and evidence sessions are new and human-screened for personal data [2]. Those two licences were not read.

## How it was made

1. A 164-attribute user ontology in five categories is fixed [2].
2. Llama 3 70B Instruct writes a background paragraph per attribute and proposes seed questions. GPT-4o also proposes questions for temporal-reasoning, multi-session and single-session-preference [2]. About 1,000 are generated per type, and about 5% survive human filtering and rewriting [2].
3. Experts decompose each answer into evidence statements, with optional timestamps [2].
4. Each evidence statement goes into a session made by LLM self-chat (at most 10 rounds), then human-screened and edited [2].
5. At test time a history of chosen length is assembled: evidence sessions are shuffled among filler, 25% ShareGPT, 25% UltraChat and 50% simulated, with plausible timestamps [2]. Construction took about 400 human hours [2].

## Used by

- **Papers.** Zep (20250120) uses the roughly 115k-token conversations [9]; Hindsight (20251214) the S setting [10]; Bao et al. (20261022) compare a naive-RAG baseline with published memory systems [8]. See the [agent-memory papers](../papers/agent-memory.md).
- **Derived data.** MemoryAgentBench re-cuts it as "LME (S*)": segments concatenated into five histories of about 355K tokens [6]. EvoMemBench builds InEp-Know from MemoryAgentBench subsets [7]. See [MemoryAgentBench](../benchmarks/memoryagentbench.md).
- **Related.** [LoCoMo](locomo.md), the other widely used conversation-memory set; trend [agent memory](../trends/agent-memory.md); projects [Graphiti](../projects/graphiti.md) (Zep's engine [9]), [Hindsight](../projects/hindsight.md), [Mem0](../projects/mem0.md).
- **Attention.** 861 citations in Semantic Scholar and 4 in OpenAlex, which lacks the ICLR version; both counts are carried over from the candidate pool and not re-queried (read 20261102 20:00 and 20:04 UTC) [12][13], and the two are not comparable. The repository has 1,191 stars (20261102), last push 20260511 [3]; the cleaned dataset shows 30,935 downloads (20261102) [4].

## Known problems

- **Two releases.** Scores on original and cleaned files are not comparable unless the file is named; the Zep paper (January 2025) predates the cleaned release [4][9]. The size of the difference is unstated.
- **Synthetic content.** Evidence sessions are LLM-simulated and half the filler is simulated [2]. MemoryAgentBench's authors, a rival benchmark, call it "synthetic" with "limited topical diversity" [6].
- **It fits in a context window.** The Zep authors note the 115k-token length "remains within the context windows of current frontier models" [9].
- **Few questions per type.** With 30 preference questions, one question moves that type's score by 3.3 points (100 divided by 30).

## Sources

1. https://arxiv.org/abs/2410.10813 : title, authors, abstract, versions v1 20241014 and v2 20250304, 500 questions, five abilities (read 20261102 20:41 UTC)
2. https://arxiv.org/html/2410.10813 : full text v2: construction, filler mix, token sizes, licence statements, human hours (read 20261102 20:41 UTC); question construction (Llama 3 70B and GPT-4o) re-read 20261102 21:18 UTC
3. https://github.com/xiaowu0162/LongMemEval : README (file list, fields, news, ICLR 2025), `LICENSE` (MIT), stars and last push through the GitHub API (read 20261102 20:41 UTC)
4. https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned : card (license mit, cleaned release text, splits), API (created 20250919, downloads) (read 20261102 20:41 UTC)
5. https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned/resolve/main/longmemeval_oracle.json : counts of types, abstention ids, sessions, counted from the file (read 20261102 20:42 UTC)
6. https://arxiv.org/html/2507.05257 : MemoryAgentBench: LME (S*) construction and the "synthetic" remark (read 20261102 20:43 UTC)
7. https://arxiv.org/html/2605.18421 : EvoMemBench: InEp-Know built from MemoryAgentBench subsets (read 20261102 20:42 UTC)
8. https://arxiv.org/abs/2610.30755 : Bao et al., naive RAG against memory systems on LoCoMo and LongMemEval (read 20261102 20:42 UTC)
9. https://arxiv.org/html/2501.13956 : Zep paper, section 4.3 (read 20261102 20:42 UTC); introduction (Zep is powered by Graphiti) read 20261102 21:19 UTC
10. https://arxiv.org/html/2512.12818 : Hindsight paper, section 7.4 (read 20261102 20:44 UTC)
11. https://github.com/xiaowu0162/LongMemEval-V2 and https://arxiv.org/abs/2605.12493 : LongMemEval-V2 description (read 20261102 20:44 UTC)
12. https://api.semanticscholar.org/graph/v1/paper/batch : citationCount 861 for arXiv 2410.10813 (carried over from the candidate pool, read 20261102 20:00 UTC; not re-queried because the API rate-limits)
13. https://api.openalex.org/works : count 4 for the arXiv-DOI record (carried over from the candidate pool, read 20261102 20:04 UTC; not re-queried)
