---
type: dataset
kinds: [questions, corpus]
benchmark: locomo
updated: 20261102 21:18 UTC
---

# LoCoMo

This page answers what the LoCoMo data is: very long conversations between two simulated speakers, with annotated questions. It gives sizes, licence, origin and known faults. Tasks, metrics and scores are on [the LoCoMo benchmark page](../benchmarks/locomo.md).

## What it contains

Each sample is one conversation of many dated sessions between two speakers. Each speaker has a persona and a timeline of life events. Images are not released, only a link, a BLIP caption and the search query [4]. A sample holds: `conversation`, `qa` (annotated: question, answer, `category`, a list of evidence dialogue ids), `event_summary` (annotated), and `observation` and `session_summary` (both generated, used as retrieval stores) [4].

## Size and versions

| | Paper (first release) | Released file `locomo10.json` |
|---|---|---|
| Conversations | 50 [2] | 10 [4][5] |
| Sessions | 19.3 per conversation, on average [2] | 272 in total, 19 to 32 per conversation [5] |
| Turns | about 300 per conversation [2] | 5,882 in total, mean 588.2 [5] |
| Length | 9,209 tokens on average [2] | tokens unstated by the authors; 133,772 words of dialogue text, my count [5] |
| Questions | 7,512 [2] | 1,986 [5] |

The paper's questions by type: single-hop 2,705, multi-hop 1,104, temporal 1,547, open-domain 285, adversarial 1,871 [2]. The released file has five numeric `category` codes, and they do not follow the paper's order. Issue 29 gives the mapping 1 multi-hop, 2 temporal, 3 open-domain, 4 single-hop, 5 adversarial; the issue infers it from the evaluation code, whose comments group the categories only loosely [7]. The counts match it: 1 = 282, 2 = 321, 3 = 96, 4 = 841, 5 = 446 [5][12]. Most papers use codes 1 to 4, which is 1,540 questions [12]. In the file, 444 of the 446 category-5 items have no `answer` key; they carry `adversarial_answer` [5].

The paper is arXiv v1, 20240227, with no later version [1]; it appeared at ACL 2024 [3]. The repository says the public data is a subset of the first release, kept "to retain the longest conversations with high-quality annotations" [4]. Which 10 of the 50 were kept, and whether the other 40 can be had, is **unstated** [4]. The last commit is 20240813; stars are 1,259 (a signal, read 20261102 20:44 UTC) [6].

## Licence

`LICENSE.txt` in the repository is Creative Commons Attribution-NonCommercial 4.0 International [4]. The paper says the data "will be released under the CC BY-NC 4.0 DEED license" [2]. GitHub's API reports no recognised licence (`NOASSERTION`) [6]. This documentation treats LoCoMo as a read-only reference: ideas and results, no reuse of the data. The licence of the MSC persona seeds is **unstated**.

## How it was made

A machine-human pipeline [2]. A persona statement from the MSC dataset is expanded by gpt-3.5-turbo; text-davinci-003 builds a dated event graph per persona; two agents with memory and reflection generate the sessions and share images. In-house annotators then fixed long-range inconsistencies, edited nearly 15% of dialogue turns, replaced or removed about 19% of images and checked grounding to the events [2]. The number of annotators and the per-question annotation procedure are **unstated** in the sections read.

## Used by

| Where | How |
|---|---|
| [Mem0](../projects/mem0.md) paper (2504.19413), see [agent-memory papers](../papers/agent-memory.md) | Its evaluation is on LoCoMo; categories 1 to 4 only [11] |
| Bao et al. (2610.30755), same group page | LoCoMo beside [LongMemEval](../benchmarks/longmemeval.md) and [MemoryAgentBench](../benchmarks/memoryagentbench.md) [12] |
| LoCoMo-Plus (2602.10715) | A separate benchmark of cognitive memory, built on LoCoMo dialogues; it also reports models on the five LoCoMo categories [13] |
| Trend [agent memory](../trends/agent-memory.md) | The memory-system score tables of Mem0, Zep and Bao et al. are all on it [10][11][12] |
| Archive | 32 files mention it, for example [agent memory](../../kb-kg/directions/agent-memory.md) [15] |

The ACL paper has 1,075 citations on Semantic Scholar (read 20261102 20:00 UTC, carried over from the research pool; not re-queried) [14].

## Known problems

- **Subset.** Numbers on the 50-conversation release and on the 10-conversation file are not comparable [4].
- **Category-code trap.** Mapping the codes by the paper's order mislabels four of the five types [7].
- **Answer key.** Penfield audited the 1,540 questions and reports 99 score-corrupting errors (6.4%), including 24 questions with the wrong speaker and a car model taken from an internal image-search string [9]. Penfield describes itself as building an agent-memory product, and I did not read its audit repository (exists, last push 20260402) [9][6]. Two issues in the dataset repository agree in kind: issue 27 (20251206, three errors) was filed by the account that owns the audit repository; issue 44 (20261020, five gold errors and two annotation defects) comes from another account [8]. A fix for the first three (pull request 28) was closed unmerged on 20260130, and the file I counted still holds the disputed answer "Psychology, counseling certification" [8][5]. No official correction was found.
- **Length.** Zep says about 16,000 to 26,000 tokens per conversation, which fits a modern context window; Mem0's paper says about 26,000; the paper says 9K for the 50 [10][11][2]. I did not count tokens.
- **Content gaps.** Zep reports image questions whose caption lacks the answer, ambiguous questions, and none on changing facts [10].

## Sources

1. https://arxiv.org/abs/2402.17753 : title, authors, v1 date 20240227, single version (read 20261102 20:41 UTC)
2. https://arxiv.org/html/2402.17753 : pipeline, Table 5 statistics, annotation figures, Appendix B.2 licence, limitations (read 20261102 20:42 UTC)
3. https://aclanthology.org/2024.acl-long.747/ : ACL 2024 record, pages 13851-13870, DOI 10.18653/v1/2024.acl-long.747 (read 20261102 20:45 UTC)
4. https://github.com/snap-research/locomo : README (subset note, fields, image note), `LICENSE.txt` first line (read 20261102 20:41 UTC)
5. `data/locomo10.json` from the repository, counted with a script (read 20261102 20:41 UTC)
6. GitHub API for snap-research/locomo and dial481/locomo-audit : stars, last push, licence field, commit dates (read 20261102 20:44 UTC)
7. https://github.com/snap-research/locomo/blob/main/task_eval/evaluation.py (comments group categories [2,3,4] and [1] only) and issue 29 (full mapping, inferred from the code) : category codes (read 20261102 21:17 UTC)
8. https://github.com/snap-research/locomo/issues/27 , /issues/28 , /issues/44 and the issue list : label-error reports, pull request 28 closed unmerged (read 20261102 20:44 UTC)
9. https://dev.to/penfieldlabs/we-audited-locomo-64-of-the-answer-key-is-wrong-and-the-judge-accepts-up-to-63-of-intentionally-33lg : audit, published 20260404 (read 20261102 20:43 UTC)
10. https://www.getzep.com/blog/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/ : dataset criticisms, Zep's view (read 20261102 20:44 UTC)
11. https://arxiv.org/html/2504.19413 : Mem0 paper, LoCoMo description and exclusion of category 5 (read 20261102 20:42 UTC)
12. https://arxiv.org/html/2610.30755 : Bao et al., 1,540 questions, category counts (read 20261102 20:42 UTC)
13. https://arxiv.org/abs/2602.10715 and /html/2602.10715 : LoCoMo-Plus, v1 20260211; Level-2 cognitive memory, section 4.6 "Insertion into LoCoMo Dialogues", Table 1 with a separate "LoCoMo (Factual Memory)" block (read 20261102 21:17 UTC)
14. Semantic Scholar citationCount for arXiv 2402.17753 : 1,075 (read 20261102 20:00 UTC, via the research pool of the same day)
15. `grep -rli locomo kb-kg pinakes` in this repository : 32 files (run 20261102 21:18 UTC; changes whenever the archive does)
