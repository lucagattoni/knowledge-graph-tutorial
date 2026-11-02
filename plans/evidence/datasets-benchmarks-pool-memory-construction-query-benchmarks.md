# Candidate pool: agent-memory, KG-construction, text-to-graph-query and KG-completion benchmarks and datasets

Researcher output for the datasets and benchmarks chapters. Written 20261102 20:1x UTC (clock read at 20:08 while writing). All times UTC.
Every number below was read from the source named in `[n]`; numbers I computed from a downloaded data file say "counted". Where a source is silent the text says **unstated**. Search-engine summaries were used only to find sources and are never cited as evidence.

## Reading guide

- **Role** follows decision D-2: a dataset page holds the data, a benchmark page the evaluation; "both" means one page of each, linked.
- **First-party** = the system's own authors ran it. A benchmark paper that runs other people's systems is not first-party for those systems; it is first-party for its own baselines and proposed method.
- **Citation count** = Semantic Scholar `citationCount` for the arXiv id (or DOI), batch call read 20261102 20:00 UTC [S2]. Recent papers are likely undercounted; the number is a floor on attention, not a verdict.
- **Archive pages** = pages of `kb-kg/` and `pinakes/` that mention the item, by a text search read 20261102 20:06 UTC [A1].
- Licence rule from the project: LICENSE file or the dataset's own card, not a README badge. Non-commercial or GPL items are read-only references (ideas and results only, no data or code copied).

## Cross-cutting findings (these are load-bearing for several pages)

| # | Finding | Evidence |
|---|---|---|
| X1 | The agent-memory benchmarks are run mostly by the vendors being compared. Independent re-runs exist for only a few settings: the MemoryAgentBench authors ran the third-party agents of its Table 3 (long-context, RAG and memory agents), and Bao et al. (20261022) ran 12 memory systems on four benchmarks, with the caveat that for LoCoMo and LongMemEval most baseline scores were copied from other papers. | [3], [8] |
| X2 | LoCoMo scores are disputed twice over: a vendor audit reports 99 wrong answer-key entries in 1,540 questions (6.4%) and a lenient judge; and Zep and Mem0 published conflicting scores for the same system (84%, 75.14 plus or minus 0.17, 58.44%). | [P1], [Z1], [Z2] |
| X3 | Full-context or plain-retrieval baselines are strong on every agent-memory benchmark read: Raw-RAG first in 6 of 7 settings; long-context models first in EvoMemBench and in MemoryAgentBench test-time learning and long-range understanding. | [8], [6], [3] |
| X4 | Headline sizes can be multiplied counts: Text2GraphQuery-Bench's "267,276 pairs" is 22,273 verified examples times 3 languages times 4 question annotations. | [9] |
| X5 | Several text-to-query metrics reward the wrong thing: TEXT2SPARQL scores are set-comparison of results (queries that fake the answer with VALUES/BIND scored well; valid queries scored 0); Text2Cypher headline metrics are Google-BLEU and Exact Match. | [TS1], [TC1] |
| X6 | KG-completion numbers depend on tie-breaking in ranking: a scorer that returns one constant gets a perfect score under the "Top" rule; three models' published FB15k-237 MRR dropped from .396/.523/.518 to .243/.150/.157 under random tie-breaking. | [SU1] |

---

## 1. longmemeval

**Role:** both. **Dataset kinds:** questions, corpus (chat histories). **Proposed front matter (dataset):** `kinds: [questions, corpus]`, `benchmark: longmemeval`. **(benchmark):** `datasets: [longmemeval]`.

### Dataset role

- **What it contains.** 500 questions, each with a timestamped user-assistant chat history ("haystack") and answer; evidence turns carry `has_answer: true`. Fields include `question_type`, `haystack_sessions`, `answer_session_ids` [1][2]. Question types in the released oracle file, counted: temporal-reasoning 133, multi-session 133, knowledge-update 78, single-session-user 70, single-session-assistant 56, single-session-preference 30; 30 ids end in `_abs` (abstention) and sit inside those types [2][D1].
- **Size and versions.** Three files: `longmemeval_s` (about 115k tokens, about 40 sessions per history for Llama 3), `longmemeval_m` (about 500 sessions; the paper says about 1.5M tokens) and `longmemeval_oracle` (evidence sessions only) [1][2]. Counted in the oracle file: 500 instances, mean 1.9 sessions per instance [D1]. README news: a cleaned version replaced the first release in 2025/09 (history sessions cleaned "to prevent interference on answer correctness"), hosted as `xiaowu0162/longmemeval-cleaned`; a follow-up `LongMemEval-V2` (agentic context) is announced for 2026/05 and was **not read** [2][H1]. Paper v1 20241014, v2 20250304; ICLR 2025 [1][S2].
- **Licence.** MIT in the code repository LICENSE file (Copyright 2024 Di Wu) and `license: mit` on the Hugging Face dataset card [2][H1]. The filler sessions come from ShareGPT and UltraChat [1]; their licences are **unstated** in these sources.
- **How it was made.** 164-attribute user ontology (five categories); Llama 3 70B proposes background paragraphs and seed questions; human experts rewrite most questions and decompose answers into evidence statements; each statement is embedded in a self-chat evidence session that is human-screened; per question a history is compiled by inserting evidence sessions among filler sessions (25% ShareGPT, 25% UltraChat, 50% simulated) with plausible timestamps [1].
- **Used by.** Zep paper (2501.13956) [Z3]; MemoryAgentBench reuses it as LongMemEval (S*) [3]; EvoMemBench's InEp-Know [6]; Bao et al. 2610.30755 [8]. Archive: 20 pages, mostly project pages (mem0, zep, graphiti, letta, memos, cognee, hindsight, supermemory, others) plus `kb-kg/papers-benchmarks`, `kb-kg/literature/graph-rag-research.md`, `kb-kg/directions/agent-memory.md` [A1].
- **Known problems.** (1) Vendor claim, not verified by me: the 115k-token S setting fits current context windows, so it tests context windows more than memory (Penfield post; Mastra's full-context baseline 60.20% with gpt-4o is quoted there) [P1]. The paper itself shows the drop from oracle to S for long-context models (GPT-4o 0.870 to 0.606) [1]. (2) The judge is `gpt-4o-2024-08-06` with more than 97% agreement with humans overall, but it deviates for preference and abstention items (90% or higher agreement everywhere) [1]. (3) The first release was superseded by a cleaned one in 2025/09, so scores on the two files are not comparable unless the file is named [2].

### Benchmark role

- **What it tests.** Five long-term memory abilities of chat assistants: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, abstention [1].
- **Tasks, metrics and protocol.** Sessions are fed one by one, then the question is asked; answers graded by an LLM judge (accuracy); retrieval-stage Recall@k and NDCG@k if the system exposes retrieval [1]. The paper frames memory as indexing, retrieval and reading and reports design optimisations (round-level values, fact-expanded keys: +9.4% recall@k and +5.4% accuracy on average; time-aware query expansion; Chain-of-Note) [1].
- **Datasets.** [longmemeval](longmemeval.md) (this item) in S, M and oracle forms.
- **Results.** Dates are paper dates.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| GPT-4o, full history offline | 0.9184 | accuracy, 97-question pilot with 3-6 session histories | benchmark authors | first-party (own benchmark) | 20241014 (runs Aug 2024) | [1] |
| ChatGPT memory (GPT-4o) | 0.5773 | same pilot | benchmark authors | independent of OpenAI | same | [1] |
| Coze (GPT-4o) | 0.3299 | same pilot | benchmark authors | independent of Coze | same | [1] |
| GPT-4o long context, oracle vs S | 0.870 vs 0.606 | accuracy | benchmark authors | independent | 20241014 | [1] |
| Raw-RAG (256-token windows, 128 dense candidates, rerank top 15), GPT-4.1-mini reader | 87.53 | accuracy over 500 questions | Bao et al., proposed method, measured | first-party for Raw-RAG | 20261022 | [8] |
| Memora | 87.40 | same | copied published score | first-party (Memora authors) | 20261022 | [8] |
| EMem / EverMemOS | 83.00 / 83.00 | same | copied published scores | first-party | 20261022 | [8] |
| Mem0 | 66.40 | same | listed in Bao Table 3; whether run or copied is not marked per row | not stated | 20261022 | [8] |
| Full-context (GPT-4.1-mini) | 65.60 | same | Bao et al. | independent | 20261022 | [8] |
| Zep, gpt-4o on LongMemEval_s | 71.2% vs full-context 60.2% | accuracy (paper table, re-read 20261102 20:06) | Zep authors | first-party | 20250120 (arXiv v1) | [Z3] |
| Zep, gpt-4o-mini on LongMemEval_s | 63.8% vs full-context 55.4% | accuracy | Zep authors | first-party | 20250120 | [Z3] |
| Zep headline claim | "accuracy improvements of up to 18.5%" with 90% lower latency | accuracy | Zep authors | first-party | 20250120 | [Z3] |
| Gemini-3-Flash / BM25 / Mem0 / A-MEM on LME (S*) subset | 83.00 / 50.33 / 52.00 / 51.00 | accuracy, DeepSeek-V3.2 backbone for memory methods | EvoMemBench authors | independent of those systems | 20261030 | [6] |

- **Known problems.** The benchmark has no official leaderboard that I could read; scores are scattered across vendor pages and papers with different readers, judges and subsets. In Bao et al. the LongMemEval baselines are mostly published scores [8]. Reader model, judge and which file (original or cleaned) are not always stated.
- **Used by.** As in the dataset role.
- **Usage evidence.** Semantic Scholar citationCount 861 (paper 2410.10813, venue ICLR 2024 per S2) read 20261102 20:00 UTC [S2]. Repository 1,191 stars, last push 20260511 22:49 UTC, read 20261102 19:51 [2]. Hugging Face downloads field 30,935 on the cleaned dataset, read 20261102 19:51 [H1].

---

## 2. locomo

**Role:** both. **Dataset kinds:** questions, corpus. **Front matter:** `kinds: [questions, corpus]`, `benchmark: locomo`; benchmark `datasets: [locomo]`.

### Dataset role

- **What it contains.** Very long two-speaker conversations between LLM agents with personas and a temporal event graph, over up to 35 sessions, with images shared (only URLs, captions and search queries are released, not images). Annotations: question-answer pairs with evidence dialogue ids, event summaries, and generated observations and session summaries [7][L1].
- **Size and versions.** Paper (arXiv v1 20240227): 50 conversations of 300 turns and 9K tokens on average [7]. The public release is a **10-conversation subset** (`data/locomo10.json`) "to retain the longest conversations with high-quality annotations"; the first release held 50 [L1]. Counted in the released file: 10 conversations, 19 to 32 sessions each, mean 588 turns, 1,986 QA pairs: category 1 = 282, 2 = 321, 3 = 96, 4 = 841, 5 (adversarial) = 446, of which 444 have no `answer` field [D2]. The category codes in the file are 1 multi-hop, 2 temporal, 3 open-domain, 4 single-hop, 5 adversarial (from the counts matched against Bao et al.'s listing: single-hop 841, multi-hop 282, temporal 321, open-domain 96) [8]; the paper lists the five reasoning types in a different order [7], so mapping by position is a trap. The 1,540 questions most papers use are categories 1-4 [8][D2].
- **Licence.** `LICENSE.txt` in the repository is Creative Commons Attribution-NonCommercial 4.0 International (GitHub reports NOASSERTION) [L1]. Non-commercial: read-only reference for this project. The conversations also derive from MSC personas [7]; licence **unstated** here.
- **How it was made.** Persona statements from MSC expanded by gpt-3.5-turbo; temporal event graph per agent from text-davinci-003; agents with memory and reflection generate sessions; human annotators edited about 15% of dialogue turns and removed or replaced about 19% of images [7].
- **Used by.** Mem0 paper 2504.19413 (its evaluation is on LoCoMo; abstract read 20261102 20:06) [M1]; Zep's rebuttal [Z1]; LoCoMo-Plus [LP1]; Bao et al. [8]. Archive: 28 pages (project pages mem0, zep, graphiti, memos, cognee, letta, mirix, memmachine, supermemory and others; `kb-kg/directions/*`, `kb-kg/literature/graph-rag-research.md`) [A1].
- **Known problems.** (1) Category 5 has no answers in the released file (counted: 444 of 446) and was dropped by Mem0 and Zep [D2][Z1]. (2) Penfield (a memory-product vendor by its own profile) reports 99 score-corrupting errors in 1,540 questions (6.4%): e.g. an answer key naming "Ferrari 488 GTB" taken from an internal image-search string, 24 questions attributing statements to the wrong speaker; and its judge test accepted 62.81% of deliberately wrong, topically close answers. Treat as a self-published audit by an interested party; the post links an audit repository I did not read [P1]. Zep's blog lists similar issues (multimodal captions missing information, wrong speaker, underspecified questions) [Z1]. A 2026 paper (LazyMem, 2607.22690) is said by a search lead to find about 6% erroneous gold answers; **not verified**. (3) Short for modern windows: Zep says conversations average about 16,000-26,000 tokens [Z1]; I did not count tokens. (4) No official correction from the authors was found in the sources read.

### Benchmark role

- **What it tests.** Memory of very long dialogue: question answering, event summarisation and multimodal dialogue generation [7].
- **Tasks, metrics and protocol.** QA with five reasoning categories scored by F1 on normalised answers, plus recall@k of evidence for RAG; event summarisation scored with ROUGE and FactScore; dialogue generation scored with MMRelevance and NLG metrics [7]. Later work mostly uses LLM-as-judge accuracy (Mem0, Bao et al.) [M1][8], so numbers from the F1 protocol and the judge protocol are not comparable.
- **Datasets.** [locomo](locomo.md).
- **Results.**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Human | 87.9 | QA F1 overall | benchmark authors | n/a | 20240227 | [7] |
| GPT-4-turbo (4,096 context) | 32.1 | QA F1 overall | benchmark authors | independent | 20240227 | [7] |
| GPT-3.5-turbo-16K, 16K context | 37.8 | QA F1 overall | benchmark authors | independent | 20240227 | [7] |
| GPT-3.5-turbo-16K + RAG over observations, top-5 | 41.4 | QA F1 overall | benchmark authors | independent | 20240227 | [7] |
| Raw-RAG, GPT-4o-mini / GPT-4.1-mini reader | 89.07 / 93.70 | LLM-judge accuracy, 1,540 questions | Bao et al., measured | first-party for Raw-RAG | 20261022 | [8] |
| MemMachine | 88.12 / 91.69 | same | published or measured per Appendix A; row not marked | first-party (MemMachine authors) if published | 20261022 | [8] |
| EverMemOS | 86.76 / 93.05 | same | same | same | 20261022 | [8] |
| Mem0 | 66.88 / 64.20 | same | published score retained for the 66.88 (Mem0 paper's own figure) | first-party | 20261022 | [8] |
| Full-context | 72.30 / 80.60 | same | Bao et al. | independent | 20261022 | [8] |
| Mem0 best configuration | about 68 vs full-context about 73 | J score (LLM judge) | Mem0 authors, as quoted by Zep | first-party; quoted by a competitor | 20250506 | [Z1] |
| Zep | 75.14 plus or minus 0.17 (corrected), after an earlier 84% | J score | Zep authors | first-party | blog 20250506, updated 20260603 | [Z1] |
| Zep, as measured by Mem0's CTO | 58.44 | accuracy, categories 1-4 | Mem0 | first-party of a competitor | issue opened 20250508 | [Z2] |
| Mem0 paper headline | "26% relative improvements in the LLM-as-a-Judge metric over OpenAI"; graph variant "around 2% higher overall" | LLM judge | Mem0 authors | first-party | 20250428 (arXiv v1) | [M1] |

- **Known problems.** As dataset role, plus: each vendor uses its own ingestion, answer prompt and sometimes model, so tables compare different pipelines (Penfield; and the Zep/Mem0 dispute above) [P1][Z1][Z2]. Bao et al. report that Mem0's UPDATE and DELETE actions are 4.39% of 33,902 write decisions and that ADD/NONE-only raises Mem0's LoCoMo accuracy from 67.36 to 69.42 [8].
- **Used by.** As above.
- **Usage evidence.** citationCount 1,075 (2402.17753, ACL per S2) read 20261102 20:00 UTC [S2]. Repository 1,259 stars, last push 20240813 03:21 UTC, read 20261102 19:51 [L1].

---

## 3. memoryagentbench

**Role:** both. **Kinds:** questions, corpus. **Front matter:** `kinds: [questions, corpus]`, `benchmark: memoryagentbench`; benchmark `datasets: [memoryagentbench]`.

### Dataset role

- **What it contains.** Long contexts split into incremental multi-turn inputs, with questions, in four competency groups: accurate retrieval (SH-Doc QA, MH-Doc QA, LongMemEval S*, EventQA), test-time learning (BANKING77, CLINC150, NLU, TREC coarse and fine, movie recommendation), long-range understanding (InfiniteBench summarisation, Detective QA), selective forgetting (FactConsolidation single and multi hop) [3].
- **Size and versions.** Sequence:QA counts from the paper's Table 6 sum to 2,071 questions (1,000 AR, 700 TTL, 171 LRU, 200 SF); average context from 103K to 1.44M tokens; LongMemEval (S*) is 5 histories (355K tokens) with 300 questions [3]. Paper v1 20250707, v4 20260628 [3]. HF dataset `ai-hyz/MemoryAgentBench` last modified 20260621 [H2].
- **Licence.** MIT in the repository LICENSE file and on the dataset card [MA1][H2]. Many sub-datasets are reconstructions of others (RULER, InfiniteBench, MQuAKE, ReDial and so on) whose own licences are **unstated** here.
- **How it was made.** Existing long-context datasets are converted into incremental multi-turn form; two are new (EventQA from novels by a fully automated pipeline; FactConsolidation from MQuAKE counterfactual edit pairs, contexts of 6K to 262K tokens) [3].
- **Used by.** EvoMemBench (InEp-Know, 1,200 questions) [6]; Bao et al. [8]. Archive: `kb-kg/papers-benchmarks`, `graph-rag-research`, `directions/agent-memory`, `plain-files-and-wikis`, projects letta, mem0, graphiti, cognee [A1].
- **Known problems.** The LongMemEval subset is re-cut (5 long histories rather than per-question histories) so its scores differ from LongMemEval proper [3]. LLM-judge or string-match details per sub-dataset are in the paper; I did not audit them.

### Benchmark role

- **What it tests.** Four competencies of "memory agents": accurate retrieval, test-time learning, long-range understanding, selective forgetting [3].
- **Tasks, metrics and protocol.** Accuracy for most sets, Recall@5 for movie recommendation, F1 for summarisation; agents grouped as long-context, simple RAG (BM25), embedding RAG, structure-augmented RAG, agentic memory; GPT-4o-mini is the backbone unless stated [3].
- **Datasets.** [memoryagentbench](memoryagentbench.md).
- **Results.** "Overall" is the last column of the paper's Table 3 (paper version v4, read 20261102 19:50). The benchmark authors ran the systems of Table 3, so they are independent of the memory-system vendors.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| GPT-5-mini (400K context) | 60.6 | overall | benchmark authors | independent | v4 20260628 | [3] |
| Claude-3.7-Sonnet (200K) | 49.6 | overall | same | independent | same | [3] |
| GPT-4o (128K) | 48.8 | overall | same | independent | same | [3] |
| GPT-4.1-mini (1M) | 46.9 | overall | same | independent | same | [3] |
| GPT-4o-mini (reference backbone) | 42.2 | overall | same | independent | same | [3] |
| HippoRAG-v2 | 41.6 | overall | same | independent | same | [3] |
| BM25 | 41.5 | overall | same | independent | same | [3] |
| MIRIX (GPT-4.1-mini) | 37.7 | overall | same | independent | same | [3] |
| MemGPT | 28.3 | overall | same | independent | same | [3] |
| Zep | 24.0 | overall | same | independent | same | [3] |
| Mem0 | 21.1 | overall | same | independent | same | [3] |
| Cognee | 20.6 | overall | same | independent | same | [3] |
| Raw-RAG (GPT-4o-mini / DeepSeek-V4-Flash) | 48.32 / 53.41 | mean of four capability macros | Bao et al. | first-party for Raw-RAG | 20261022 | [8] |
| Memora (same two readers) | 43.84 / 47.88 | same | Bao et al., "all systems follow the same evaluation procedure" | independent | 20261022 | [8] |
| Mem0 (same two readers) | 41.28 / 41.95 | same | Bao et al. | independent | 20261022 | [8] |

  The two Mem0 figures (21.1 and 41.28/41.95) come from different papers, versions of the scoring and readers; they are not reconciled here [3][8].
- **Known problems.** Authors' finding: all methods fail on multi-hop selective forgetting (at most 28% accuracy) [3]. The overall score averages heterogeneous metrics. The benchmark authors released the sets but I found no official leaderboard.
- **Usage evidence.** citationCount 298 (2507.05257; S2 lists the venue as arXiv) read 20261102 20:00 UTC [S2]. Repository 484 stars, last push 20260925 06:11 UTC, read 20261102 19:51 [MA1].

---

## 4. locomo-plus

**Role:** both. **Kinds:** questions, corpus. **Front matter:** `kinds: [questions, corpus]`, `benchmark: locomo-plus`.

### Dataset role

- **What it contains.** 401 "cognitive memory" cue-trigger instances (counted in `locomo_plus.json`: relation types causal 101, state 100, goal 100, value 100; each with a cue dialogue, a trigger query and a time gap such as "two months later") that are stitched into the LoCoMo conversations; no reference answer is stored for them [LP1][D3]. The released benchmark merges LoCoMo's five categories with this sixth, "Cognitive" [LP1].
- **Size and versions.** 401 samples counted; paper v1 20260211 only [LP2][D3]. Evaluation inherits the LoCoMo questions unchanged (Penfield's criticism) [P1].
- **Licence.** No LICENSE file (GitHub licence endpoint returned 404); README says "See the repository for license information"; **unstated**. Because it ships `locomo10.json` it also inherits LoCoMo's CC BY-NC 4.0 terms for that file (inference from the README listing it, not a stated licence) [LP1][L1].
- **How it was made.** LLM-generated implicit cue dialogues, manual verification of "memory-worthy" cues, LLM-generated trigger queries with low surface similarity, BM25 and MPNet similarity filtering, final human validation of cue elicitation [LP2].
- **Used by.** None found outside its own paper; the 2609.03467 "When Users Don't Ask" paper derives from LoCoMo, not LoCoMo-Plus (archive row). Archive: `kb-kg/papers-benchmarks` only [A1].
- **Known problems.** Small by design (the authors prioritise diagnostic coverage over scale); judge sensitivity acknowledged in the paper's limitations [LP2]. Penfield says the improved judging "was only validated on the new cognitive questions" and that the original 1,540 questions keep their answer-key errors [P1].

### Benchmark role

- **What it tests.** Whether a model keeps and applies latent user constraints (state, goal, value, causal) when the later query is semantically unlike the earlier cue ("cue-trigger semantic disconnect") [LP2].
- **Tasks, metrics and protocol.** Unified input, no task disclosure; LLM judge on constraint consistency (correct 1, partial 0.5, wrong 0 per the repository); human-judge agreement reported in the paper's Table 2 and stability across two judge backbones in Table 3 (values not read) [LP1][LP2].
- **Datasets.** [locomo-plus](locomo-plus.md) plus LoCoMo.
- **Results (Table 1 of the paper; LoCoMo = average of its five categories; Gap = LoCoMo minus LoCoMo-Plus).**

| System | LoCoMo-Plus | LoCoMo avg | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|---|
| gemini-2.5-pro (full context) | 26.06 | 71.78 | judge score | benchmark authors | independent | 20260211 | [LP2] |
| gemini-2.5-flash | 24.67 | 69.25 | same | same | independent | same | [LP2] |
| gpt-4o | 21.05 | 62.99 | same | same | independent | same | [LP2] |
| Qwen3-14B | 19.09 | 59.65 | same | same | independent | same | [LP2] |
| A-Mem (GPT-4o) | 17.20 | 59.64 | same | same | independent | same | [LP2] |
| Mem0 (GPT-4o) | 15.80 | 57.24 | same | same | independent | same | [LP2] |
| SeCom (GPT-4o) | 14.90 | 57.53 | same | same | independent | same | [LP2] |
| text-embedding-large RAG (GPT-4o) | 15.55 | 45.32 | same | same | independent | same | [LP2] |

- **Known problems.** As above; plus judge dependence. Whether the 401 instances are the whole benchmark or a sample is not stated in the text I read.
- **Usage evidence.** citationCount 23 (2602.10715; S2 lists ACL 2026) read 20261102 20:00 UTC [S2]. Repository 43 stars, last push 20260213 04:28 UTC, read 19:51 [LP1]. arXiv record gives no venue; README says "ARR 2026 (January)" [LP1][LP2].

---

## 5. ama-bench

**Role:** both. **Kinds:** questions, corpus (agent trajectories). **Front matter:** `kinds: [questions, corpus]`, `benchmark: ama-bench`.

### Dataset role

- **What it contains.** Agent-environment trajectories (action and observation per turn) with open-ended memory questions, in two subsets: a real-world subset in six domains (web, open-world QA, text-to-SQL, software engineering, gaming, embodied AI) with expert-written QA, and a synthetic subset in TextWorld and BabyAI with rule-based QA that scales to arbitrary horizons [5].
- **Size and versions.** Paper: 2,496 QA pairs in the real-world subset, 1,200 QA in the synthetic subset (two tasks, five lengths 8K-128K tokens, 240 per length) [5]. Counted in the Hugging Face file `test/open_end_qa_set.jsonl`: 208 episodes, 2,496 QA pairs; domains TEXT2SQL 51, SOFTWARE 36, WEB 31, Game 30, EMBODIED_AI 30, OPENWORLD_QA 30; question types A recall 839, B causal inference 596, C state updating 647, D state abstraction 414; mean 64,512 tokens per episode (max 1,029,331) [D4]. The HF dataset has a test split only, and the synthetic subset is not in it (generation scripts are in the repository) [AB1]. Paper v1 20260226, v4 20260527; repository says ICML 2026 acceptance [5][AB1].
- **Licence.** MIT: repository LICENSE file and Hugging Face card (`license: mit`) [AB1][H3]. Source benchmarks of the trajectories are named in the paper's appendix; their licences are **unstated** here.
- **How it was made.** Trajectories from representative agent benchmarks run with agent frameworks or taken as expert trajectories; graduate-level annotators write 12 memory-intensive QA per trajectory with a cross-review by a second annotator; synthetic subset built from executable environments with latent states [5].
- **Used by.** No other paper found in this run. Archive: `kb-kg/papers-benchmarks` only [A1].
- **Known problems.** Accuracy is judged by a Qwen3-32B LLM judge (cross-judge agreement and human validation are in the paper's appendix, not read) [5]. The authors also propose AMA-Agent, so the top score is by the benchmark's authors.

### Benchmark role

- **What it tests.** Long-horizon memory over agent trajectories: recall, causal inference, state updating, state abstraction [5].
- **Tasks, metrics and protocol.** Open-ended QA, accuracy by LLM judge (Qwen3-32B) and F1; methods share a two-stage interface, `memory_construction` then `memory_retrieve` [5][AB1]. A Hugging Face leaderboard exists (not read) [AB1].
- **Datasets.** [ama-bench](ama-bench.md).
- **Results (real-world subset, accuracy, F1 in parentheses; Table 4 and Table 5).**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| GPT 5.2 | 0.7226 (0.3988) | accuracy (F1) average | benchmark authors | independent | v4 20260527 | [5] |
| GPT-5-mini | 0.6784 (0.3464) | same | same | independent | same | [5] |
| Gemini 2.5 flash | 0.5168 (0.2878) | same | same | independent | same | [5] |
| Qwen3-32B (base for memory runs) | 0.5181 (0.3545) | same | same | independent | same | [5] |
| AMA-Agent (Qwen3-32B) | 0.5722 (0.2992) | same | benchmark authors, own method | first-party | same | [5] |
| MemoRAG | 0.4606 (0.1822) | same | benchmark authors | independent | same | [5] |
| HippoRAG2 | 0.4480 (0.2048) | same | same | independent | same | [5] |
| Qwen3-Emb-4B RAG | 0.4227 (0.1522) | same | same | independent | same | [5] |
| BM25 | 0.3436 (0.1475) | same | same | independent | same | [5] |
| MemGPT / GraphRAG | 0.3304 / 0.3258 | same | same | independent | same | [5] |
| Mem0 | 0.2104 (0.2343) | same | same | independent | same | [5] |

  The abstract states AMA-Agent reaches 57.22% and beats the strongest baseline by 11.16% [5].
- **Known problems.** Real-trajectory annotation is human but small-team; accuracy rankings of memory methods in the paper put several named memory systems below plain embedding RAG [5].
- **Usage evidence.** citationCount 58 (2602.22769) read 20261102 20:00 UTC [S2]. Repository 85 stars, last push 20260615 01:22 UTC, read 19:51 [AB1]. HF downloads field 1,051, read 19:56 [H3].

---

## 6. evomembench

**Role:** benchmark (it repackages other datasets). **Front matter:** `datasets: [memoryagentbench]` plus the reused sources named in the paper (CL-Bench, BFCL multi-turn, xbench-DeepSearch, WebWalkerQA, ALFWorld, which have no page in my pool).

- **What it tests.** Agent memory from a self-evolving view, two axes: scope (in-episode vs cross-episode) and content (knowledge vs execution), giving six datasets [6].
- **Tasks, metrics and protocol.** Answer accuracy for knowledge settings; success rate and token or step efficiency for execution settings; 15 memory methods (retrieval: BM25, Qwen3-Emb-4B, GraphRAG; short-term: MemAgent, MemoBrain; general long-term: Mem0, A-MEM, MemOS, MemoryOS; procedural: AWM, SkillWeaver, AgentKB, ACE, ReasoningBank; plus a meta-evolution method) against memory-free LLMs; all memory methods use DeepSeek-V3.2 as backbone; top-k 10 for knowledge and 3 for execution tasks [6].
- **Datasets.** InEp-Know from MemoryAgentBench (1,000 AR + 200 SF samples); InEp-Exec from BFCL-MultiTurn-LongContext (200, reconstructed with GPT-5-mini and manually checked); CrossEp-Know from CL-Bench (120 contexts, 884 samples); CrossEp-Tool from BFCL-MultiTurn-Base (200); CrossEp-Web from xbench-DeepSearch (100) and WebWalkerQA (170); CrossEp-Emb from ALFWorld (200) [6]. The repository README states the same sizes, total 2,954 [EV1 (sum counted)].
- **Licence of the repository data.** No LICENSE file (404); **unstated**. The reused sources keep their own licences, **unstated** here [EV1].
- **Results (InEp-Know, answer accuracy; paper v3 20261030).** The extracted table lost the average cells, so only unambiguous columns are given.

| System | Score (EventQA / LongMemEval S*) | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Gemini-3-Flash (no memory) | 98.20 / 83.00 | accuracy %, overall rank 1 | benchmark authors | independent | 20261030 | [6] |
| GPT-5-mini (no memory) | 80.60 / 62.33 | same, overall rank 3 | same | independent | same | [6] |
| DeepSeek-V3.2 (no memory) | 83.00 / 32.33 | same, overall rank 5.5 | same | independent | same | [6] |
| BM25 memory | 88.80 / 50.33 | same, overall rank 4.17 | same | independent | same | [6] |
| Mem0 | 79.20 / 52.00 | same, overall rank 4.5 | same | independent | same | [6] |
| A-MEM | 91.20 / 51.00 | same, overall rank 4.83 | same | independent | same | [6] |
| GraphRAG | 74.20 / 22.00 | same, overall rank 10.17 | same | independent | same | [6] |

  Findings stated by the authors: strong long-context baselines remain highly competitive; memory methods help retention more than revision; memory helps more when the context budget is constrained or tasks are hard and can hurt easy tasks [6].
- **Known problems.** Very new (v1 20260518); a derived benchmark whose results depend on the DeepSeek-V3.2 backbone; no licence statement; I did not audit the reconstruction of BFCL items [6][EV1].
- **Used by.** None found. Archive: `kb-kg/papers-benchmarks` only [A1].
- **Usage evidence.** citationCount 19 (2605.18421) read 20261102 20:00 UTC [S2]. Repository 14 stars, last push 20261027 12:27 UTC, read 19:51 [EV1].

---

## 7. text2kgbench

**Role:** both. **Dataset kinds:** corpus (sentences aligned to triples under an ontology). **Front matter:** `kinds: [corpus]`, `benchmark: text2kgbench`.

### Dataset role

- **What it contains.** Sentences aligned to ground-truth triples that conform to a given ontology, plus the ontologies themselves (OWL in Turtle and compact JSON). Two datasets: Wikidata-TekGen and DBpedia-WebNLG [T1].
- **Size and versions.** Wikidata-TekGen: 10 ontologies, 13,474 sentences; DBpedia-WebNLG: 19 ontologies, 4,860 sentences. Extra test sets for TekGen: a manually verified subset of 939 sentence-triple alignments and 174 invented "unseen" sentences. Splits are stratified random folds (train, validation, test) [T1]. arXiv 20230804; Zenodo record 7916716 v1.0 dated 20230509, file `Text2KGBench.zip` (5.9 MB) [T1][ZE1]. A 2025 refinement, **Text2KGBench-LettrIA**, re-annotates the 4,860 DBpedia-WebNLG sentences into over 14,000 triples and revises the 19 ontologies (ISWC 2025 KBC-LM workshop); I read its abstract only [LE1].
- **Licence.** Code: Apache-2.0 LICENSE file. Data: Zenodo record states CC BY 4.0 [ZE1]; the repository README is inconsistent (badge "CC BY 4.0", text "Attribution-ShareAlike 4.0 ... (CC BY 4.0)") and notes that it derives from TekGen (CC BY-SA 2.0) and WebNLG 3.0 (CC BY-NC-SA 4.0) [T2]. The WebNLG-derived half is therefore non-commercial: read-only reference for this project.
- **How it was made.** TekGen: ontologies written by hand from Wikidata property constraints; TekGen's Wikidata-triple-to-Wikipedia-sentence alignments (distant supervision, 16M alignments over 663 relations) reused, then filtered per ontology. WebNLG: WebNLG 3.0 English 3-triple split, relations grouped into 19 DBpedia ontologies, train and test kept fact-disjoint [T1].
- **Used by.** Text2KGBench-LettrIA [LE1]; no other use read in this run. Archive: `kb-kg/papers-benchmarks` only [A1].
- **Known problems.** TekGen alignments are noisy (distant supervision), hence the 939-sentence cleaned subset; models may have seen Wikipedia sentences in pre-training, hence the unseen set [T1]. The LettrIA authors say Text2KGBench has "shortcomings in data quality, ontological consistency, and structural design" [LE1]. Test-set sizes per split: **unstated** in what I extracted.

### Benchmark role

- **What it tests.** Whether an LM extracts facts from text that follow the given ontology and the sentence, and does not hallucinate [T1].
- **Tasks, metrics and protocol.** Input: ontology plus sentences (plus optional examples); output: triples. Seven metrics: precision, recall, F1 against gold; ontology conformance (OC); subject, relation, object hallucination (SH, RH, OH) [T1].
- **Datasets.** [text2kgbench](text2kgbench.md).
- **Results (Table 2, averages across ontologies).**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Vicuna-13B, TekGen all test cases | P .38, R .34, F1 .35, OC .83, SH .17, RH .17, OH .17 | seven metrics | benchmark authors | first-party (own baseline) | 20230804 | [T1] |
| Vicuna-13B, TekGen selected | F1 .38, OC .84 | same | same | first-party | same | [T1] |
| Alpaca-LoRA-13B, TekGen all | F1 .27, OC .87 | same | same | first-party | same | [T1] |
| Vicuna-13B, DBpedia-WebNLG | P .34, R .27, F1 .30, OC .93 | same | same | first-party | same | [T1] |
| Alpaca-LoRA-13B, DBpedia-WebNLG | F1 .25, OC .91 | same | same | first-party | same | [T1] |

  Only the authors' two baselines are in the paper. Independent results exist in the LettrIA paper (proprietary and open-weights, zero-shot and fine-tuned) but I did not read its tables; its abstract says smaller fine-tuned open-weights models beat larger proprietary ones on F1 [LE1]. The authors run a company (Lettria) that sells a Text2Graph product; a vendor blog on the topic was seen only as a search lead and not used.
- **Known problems.** The 2023 baselines are far from current models; no maintained leaderboard found; see dataset role for data issues [T1][LE1].
- **Usage evidence.** citationCount 149 (2308.02357; S2 venue "International Workshop on the Semantic Web") read 20261102 20:00 UTC [S2]. Repository 95 stars, last push 20240506, read 19:51 [T2].

---

## 8. text2cypher

**Role:** both. **Dataset kinds:** questions (question, schema, Cypher triples). **Front matter:** `kinds: [questions]`, `benchmark: text2cypher`.

### Dataset role

- **What it contains.** Rows of natural-language question, graph database schema and reference Cypher query, with a source alias and an optional database reference alias; English only [TC1][H4].
- **Size and versions.** Neo4j-Text2Cypher (2024) `neo4j/text2cypher-2024v1`: 44,387 instances, 39,554 train and 4,833 test; with database access: 22,093 train (55.85%) and 2,471 test (51.12%) [TC1][H4]. A multilingual test and train sample (Spanish, Turkish translations of the questions, same Cypher) is released separately [TC2]. A `neo4j/text2cypher-2025v1` dataset also exists on Hugging Face; its card holds only the licence line, so its size is **unstated** [H5].
- **Licence.** Hugging Face card: `apache-2.0`. The repository `neo4j-labs/text2cypher` LICENSE file is CC0-1.0. The two statements differ; the rows also come from twelve sources whose own licences the card does not state (**unstated**) [H4][TC3].
- **How it was made.** Twelve public sources pooled (synthetic sets generated by GPT-4o, GPT-4 Turbo, Gemini and Claude Opus over demo databases, a functional Cypher generator, crowdsourced questions, Neo4j-Text2Cypher'23, three Hugging Face sets, Cy-Spider); manual cleaning (remove back-ticks, remove irrelevant questions such as "Lorem ipsum", deduplicate on question and Cypher); syntax validation by running `EXPLAIN` on a local Neo4j; files named train go to train, files named test or dev go to test, the rest split 90:10 [TC1].
- **Used by.** Text2Cypher Across Languages (2506.21445) [TC2]; Text2GraphQuery-Bench fine-tunes and compares a `text2cypher-gemma-2-9b` model trained on it [9]; Neo4j's own follow-up analysis [NB1]. Archive: `kb-kg/llm-era/README.md`, projects memgraph, neo4j-graphrag-python, llm-graph-builder, `kb-kg/papers-benchmarks`, and the two landscape snapshots [A1].
- **Known problems.** Neo4j's own error analysis finds many per-instance outliers across all metrics; models struggle most with the synthetic sources `functional`, `gemini` and `gpt4o` and with the recommendations, companies and neoflix databases; some questions can be answered through several relationships; equivalent queries use different idioms (e.g. MAX versus ORDER BY with top element) [NB1]. Only about half of the instances can be executed against a database [TC1]. No quantified noise rate found.

### Benchmark role

- **What it tests.** Translation of a question plus schema into Cypher [TC1].
- **Tasks, metrics and protocol.** Google-BLEU (translation-style) and Exact Match on the test split; execution-based checks only for rows with database access; many other text metrics computed but not headline [TC1]. 15 or so foundational and previously fine-tuned models benchmarked, then six fine-tuned [TC1].
- **Datasets.** [text2cypher](text2cypher.md) test split.
- **Results (Table 5, improvement of fine-tuned over baseline; the paper's Figure 4 absolute scores are not in the extracted text).**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Gemini-1.0-Pro-002, fine-tuned vs baseline | +about 0.34 / +about 0.11 | change in Google-BLEU / Exact Match | Neo4j authors | first-party (dataset owner) | 20241213 | [TC1] |
| Gemini-1.5-Flash-001 | +about 0.27 / +about 0.09 | same | same | first-party | same | [TC1] |
| Llama-3.1-8B-instruct | +about 0.14 / +about 0.11 | same | same | first-party | same | [TC1] |
| GPT-4o | +about 0.18 / +about 0.01 | same | same | first-party | same | [TC1] |
| `text2cypher-gemma-2-9b` on Text2GraphQuery-Bench Cypher, zero-shot | execution accuracy 0.184 (Qwen3-8B zero-shot 0.263) | EX | Text2GraphQuery-Bench authors | independent | 20260805 | [9] |

  Only first-party absolute results exist in what I read; independent absolute results on this test split: **unstated**.
- **Known problems.** The headline metrics are string-similarity (GLEU, Exact Match), which penalise equivalent queries; Neo4j plans parse-tree evaluation and further cleaning [NB1]. A 2026 preprint (PIPE-Cypher, abstract and discussion read) argues that outputs that parse and match the schema can still answer the wrong graph question, and proposes private enterprise benchmarks instead of static corpora [PC1].
- **Usage evidence.** citationCount 73 (2412.10064; S2 venue COLING Workshops) read 20261102 20:00 UTC [S2]. Repository `neo4j-labs/text2cypher` 245 stars, last push 20261009, read 19:51 [TC3]. HF downloads field 413 for 2024v1, read 19:51 [H4]. Companion paper "Text2Cypher Across Languages" citationCount 3 [S2].

---

## 9. text2graphquery-bench

**Role:** both. **Dataset kinds:** questions. **Front matter:** `kinds: [questions]`, `benchmark: text2graphquery-bench`.

### Dataset role

- **What it contains.** (Question, graph query) pairs over 34 graph databases in 13 domains, for three declarative property-graph languages (Cypher, ISO GQL, SQL/PGQ), with four question phrasings (original plus three abstraction levels), a four-tier graph-native difficulty label, and schema aliases [9].
- **Size and versions.** The abstract's 267,276 pairs are 22,273 verified examples times 3 query languages times 4 question annotations (table footnote). The 22,273 examples split into train 12,861 (10 DBs, 4 domains), dev 5,585 (18 DBs, 10 domains), test 3,827 (6 DBs, 5 domains). The repository README of the generation toolkit quotes a different total, 178,184 pairs, without explaining the difference. Paper v1 20260212, v2 20260805 [9][TG1].
- **Licence.** Toolkit code: Apache-2.0 LICENSE file. Dataset licence: **unstated** (README links a download on an Alibaba object store; the paper page itself shows CC BY 4.0 for the paper text) [TG1][9].
- **How it was made.** Schemas parsed from existing databases or synthesised from domain descriptions into an intermediate representation (SchemaGraph); data synthesised; queries by template adaptation plus LLM evolution; execution on real engines (queries that fail to execute are discarded); semantic dedup at 0.98 embedding similarity; for the test set 700 examples (18.3%) were scored by expert and model for alignment (average 4.81 of 5, 92.9% pass) [9].
- **Used by.** None found beyond the paper. Archive: `kb-kg/papers-benchmarks` only [A1].
- **Known problems.** (1) Headline count is multiplied, not 267k independent questions (see above). (2) Only 2,783 of the 3,827 test examples run on all three engines; the other 1,044 cannot run on Spanner Graph, which does not return graph elements [9]. (3) Expert verification covers a 700-example test sample, not the whole set [9].

### Benchmark role

- **What it tests.** Natural language to graph query across languages, under question abstraction and schema aliasing [9].
- **Tasks, metrics and protocol.** Grammar (parses), Google-BLEU, Jaro-Winkler similarity, execution accuracy (EX, result equality) on TuGraph-DB (Cypher), Spanner Graph (GQL), Oracle DB (SQL/PGQ) and SQLite (SQL); zero-shot, 3-shot fixed examples, LoRA fine-tuning; non-thinking mode [9].
- **Datasets.** [text2graphquery-bench](text2graphquery-bench.md).
- **Results (Table 5, execution accuracy; model names as printed in the paper).**

| System | Score (Cypher / GQL / SQL-PGQ) | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Claude Opus 4.8, few-shot | .576 / .582 / .509 | EX | benchmark authors | independent of Anthropic | v2 20260805 | [9] |
| Claude Opus 4.8, zero-shot | .512 / .458 / .029 | EX | same | independent | same | [9] |
| GPT-5.5, few-shot | .553 / .549 / .512 | EX | same | independent | same | [9] |
| Qwen3.7-Max, few-shot | .553 / .548 / .209 | EX | same | independent | same | [9] |
| Gemini-3.5-Flash, few-shot | .540 / .536 / .506 | EX | same | independent | same | [9] |
| Qwen3-8B, LoRA fine-tuned | .358 / .451 / .401 | EX | same | independent | same | [9] |
| `text2cypher-gemma-2-9b`, zero-shot (Cypher only; fine-tuned on this benchmark for GQL and SQL/PGQ) | .184 / (.317 fine-tuned GQL) / (.296 fine-tuned SQL/PGQ) | EX | same | independent | same | [9] |

- **Known problems.** The authors note GQL and SQL/PGQ syntax is unfamiliar to models (zero-shot grammar scores as low as 0.054 for SQL/PGQ with Qwen3.7-Max), so cross-language gaps mix syntax and reasoning effects; alias perturbation drops EX by only 1.26% on average, which they say understates real-world naming drift [9].
- **Usage evidence.** citationCount 2 (2602.11745) read 20261102 20:00 UTC [S2]. Repository (toolkit) 104 stars, last push 20260727 12:23 UTC, read 19:51 [TG1].

---

## 10. cypherturn

**Role:** both. **Dataset kinds:** questions, kg (seven synthetic KGs). **Front matter:** `kinds: [questions, kg]`, `benchmark: cypherturn`.

### Dataset role

- **What it contains.** 721 conversational sessions (5,927 turns) of natural-language utterances with gold Cypher, over seven purpose-built synthetic knowledge graphs, covering 13 conversational phenomena (e.g. refine, contrast, aggregation), 9 chain modes and 10 user personas [CT1].
- **Size and versions.** 721 sessions, 5,927 turns, 7 KGs (66 to 77 sessions per persona) [CT1]. arXiv v1 20260929 only; accepted as an oral paper at EMNLP 2026 per the record's comment [CT1].
- **Licence.** No LICENSE file (GitHub endpoint 404). README: "released for research purposes. See the accompanying paper for terms." The paper terms: **unstated** in what I read [CT2].
- **How it was made.** Seven synthetic worlds (e.g. Ancient Empire, Magic Academy, Ocean Kingdom, Stellar Colony) so answers must come from the graph; sessions generated then reviewed by two Cypher-proficient annotators on three criteria (pooled inter-annotator kappa 0.83, measured; the per-criterion split is a retrospective decomposition) [CT1].
- **Used by.** None found beyond the paper. Archive: `kb-kg/papers-benchmarks` only [A1].
- **Known problems.** All graphs are synthetic, so scores do not extrapolate to real enterprise graphs (authors' limitation); an RL-trained model, CypherRI-7B, was excluded because of a format failure [CT1].

### Benchmark role

- **What it tests.** Multi-turn text-to-Cypher with anaphora and refinement, under two protocols [CT1].
- **Tasks, metrics and protocol.** Guided oracle protocol (the system gets guidance each turn) and fully autonomous agentic protocol (5-action space, budgets x3, x5, x10 per turn, user simulator by an LLM); execution accuracy (EX), session-level correctness (SEM), a structural similarity score (PSJS); 15 models; 10,000-resample bootstrap significance [CT1].
- **Datasets.** [cypherturn](cypherturn.md).
- **Results.**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Claude Opus 4.7 | 0.647 (guided); session-level SEM 0.046 (33 of 721 sessions) | EX | benchmark authors | independent | 20260929 | [CT1] |
| STRuCT-LLM-Novo | 0.526 (guided) | EX | same | independent | same | [CT1] |
| Gemini-3.1-Flash-Lite | 0.432 (agentic x3), first under autonomy; fourth guided | EX | same | independent | same | [CT1] |
| Claude Opus 4.7 / GPT-5.5 (agentic) | tie within 0.001, behind Gemini | EX | same | independent | same | [CT1] |
| Qwen3-235B | 0.199 (agentic), fifth guided | EX | same | independent | same | [CT1] |
| Llama-3.1-8B, budget x10 | 0.261 | EX | same | independent | same | [CT1] |

- **Known problems.** Rankings reorder under autonomy (the authors' "Autonomy Divergence"); newer models will shift absolute scores; harness does not ship per-model outputs [CT1][CT2].
- **Usage evidence.** citationCount 0 (2609.36987; one month old) read 20261102 20:00 UTC [S2]. Repository 1 star, last push 20260827 08:35 UTC, read 19:51 [CT2].

---

## 11. text2sparql-challenge

**Role:** benchmark (the question sets and the corporate KG are the challenge's own data, but the official site was unreachable, so the dataset side is thinly sourced). **Front matter:** `datasets: []` until a dataset page is justified.

- **What it tests.** Translation of natural-language questions into SPARQL for a well-known KG (DBpedia) and for an unknown, undocumented corporate KG, in several languages. The challenge's editions: first 20250601 (Portoroz, co-located with Text2KG at ESWC25, six participating approaches), second 20260510 (Dubrovnik, ESWC26, eight approaches) [TS1][TS2][CE1].
- **Tasks, metrics and protocol.** Each registered system exposes an HTTP service taking `question` and `dataset` and returns a SPARQL query within ten minutes; the organisers run it against hidden questions and compare the **result sets** of the generated and gold queries (precision, recall, F1; the 2026 tables add an NDCG column) [TS1][TS2]. 2025: 250 queries per endpoint over a five-day test phase [TS1].
- **Datasets (as described by participants, not by the organisers).** 2025: DB25, English and Spanish subset of DBpedia 2015-10, 200 questions split equally; CK25, a corporate KG built by the organisers, 50 English questions written in consultation with stakeholders [TS1]. 2026: DBpedia task (English and Spanish) and Corporate task (English and German), "50" questions each as rendered in the HTML (the text duplicates the number, so I read it as 50 per task; **not verified**); the participant also says the 2025 DBpedia test set has "100" questions in English and Spanish, which conflicts with the 200 stated by the 2025 participant (**unresolved**) [TS2][TS1]. The corporate ontology has 13 classes and 30 properties [TS2]. Question and query data hosting, licence and version: **unstated** (official site `text2sparql.aksw.org` refused the connection when fetched 20261102 19:5x UTC; the 2025 CEUR proceedings Vol-4094 page lists six papers and does not describe the data) [CE1].
- **Results (2026 edition, F1; English DBpedia / Spanish DBpedia / English Corporate / German Corporate).**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| SPARQL-LLM (GPT-5.2, retrieval-based) | .7192 / .7810 / .8510 / .8104 | F1 | organisers' metric tool; table reported by the system's authors | first-party (authors of SPARQL-LLM) | 20261009 | [TS2] |
| ARUQULA v1 (best other) | .6142 / .4904 / .6437 / .6230 | F1 | same | not stated for this row | same | [TS2] |
| GRASP | .3296 / .3288 / .5262 / .4892 | F1 | same | not stated | same | [TS2] |
| LiberAI v1 | .3235 / .3730 / .3215 / .3510 | F1 | same | not stated | same | [TS2] |
| IRIS | .2897 / .2914 / .2896 / .1460 | F1 | same | not stated | same | [TS2] |

  (The Corporate values are from the separate "F1" column of Tables 4 and 5; the paper's headings are "F1/NDCG, Recall, Precision, F1, NDCG", and the combined "F1/NDCG" column differs slightly, e.g. .8539 for SPARQL-LLM in English.) The paper states SPARQL-LLM ranks first overall among eight approaches, with up to 59% higher F1 than the second best, at under 3 US dollars of LLM cost [TS2]. The official leaderboard was not reachable; independent confirmation: **unstated**.
- **Known problems.** From a 2025 participant (ARUQULA authors) who compared their outputs with the organisers' evaluation artefact: (a) result-set comparison scores valid queries as 0 when projection differs (labels versus IRIs, extra rank column); (b) queries that return Spanish-DBpedia entities instead of English ones score 0; (c) several DBpedia properties give different results for the same question (population: `dbo:population`, `dbo:populationTotal`, `dbp:population`, `dbp-es:población`); (d) queries that fake the answer with VALUES and BIND can score well; (e) some gold question-result pairs have false empty result sets; they conclude that the dataset and evaluation "require refinement" [TS1]. The same paper's author list belongs to a participating team, so this is a participant's view.
- **Used by.** The challenge papers themselves; SPARQL-LLM uses LC-QuAD, QALD-9+ and the 2025 test set as examples [TS2]. Archive: `kb-kg/papers-benchmarks` (lists the SPARQL-LLM paper) [A1].
- **Usage evidence.** citationCount: SPARQL-LLM challenge paper 2610.13648 = 0; ARUQULA 2510.02200 = 11; SPARQL-LLM journal paper 2512.14277 = 7 (ACM Transactions on the Web per S2); read 20261102 20:00 UTC [S2]. Repository `sib-swiss/sparql-llm` 131 stars, MIT LICENSE.txt, last push 20261102 16:35 UTC, read 19:51 [SL1].

---

## 12. lc-quad (LC-QuAD 1.0)

**Role:** both. **Dataset kinds:** questions (the target KG, DBpedia 2016-04, is not shipped). **Front matter:** `kinds: [questions]`, `benchmark: lc-quad`.

### Dataset role

- **What it contains.** 5,000 complex questions with SPARQL queries over DBpedia, each with a template id, an automatically generated "intermediary question" and a manually corrected final question [LQ1][LQ1s].
- **Size and versions.** 5,000 pairs; 80:20 train and test; target DBpedia version 04-2016 (the public endpoint no longer serves that version, so many queries return nothing; the maintainers recommend a local copy) [LQ1]. ISWC 2017 [LQ1s].
- **Licence.** GPL-3.0: README says the dataset "released with a GPL 3.0 License" and the repository LICENSE.txt is GPL-3.0 (on the `data` branch) [LQ1]. GPL: read-only reference for this project.
- **How it was made.** SPARQL queries generated automatically from templates, converted to intermediary natural-language questions, then manually corrected into final questions [LQ1].
- **Used by.** Many KGQA systems (leaderboard lists dozens) [KB1]; used as example pool by the TEXT2SPARQL 2026 participant SPARQL-LLM [TS2]. Archive: no page mentions it [A1].
- **Known problems.** Template-generated (low linguistic variety, per the TEXT2SPARQL participant's description "a template-generated KGQA corpus") [TS2]; endpoint version drift [LQ1].

### Benchmark role

- **What it tests.** Question to SPARQL over DBpedia; also used for answer-level KGQA [LQ1].
- **Tasks, metrics and protocol.** Precision, recall, F1 on answers or on queries depending on the reporting paper; no official leaderboard (maintainers say they benchmark manually on request) [LQ1][KB1].
- **Datasets.** [lc-quad](lc-quad.md).
- **Results (community leaderboard "Tracking Progress in KGQA", entries reported by the cited papers; page date unstated).**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| T5-Base | 91 | F1 | Banerjee et al. | independent of the T5 authors | 2022 | [KB1] |
| T5-Small | 90 | F1 | same | independent | 2022 | [KB1] |
| mBERT (English) | 85.50 | F1 | Zhou et al. | not stated | 2021 | [KB1] |
| PGN-BERT-BERT | 88 | F1 | Banerjee et al. | not stated | 2022 | [KB1] |
| ValueNet4SPARQL | 85 | F1 | Kosten et al. | not stated | 2023 | [KB1] |
| KGQAn | 52.03 | F1 | Omar et al. | first-party (system's own report) | 2023 | [KB1] |

  Scores mix settings (gold entities given or not, query match or answer match); the board does not enforce one protocol for v1.
- **Known problems.** Community aggregate, not an audited leaderboard; protocol differences across rows; no result newer than 2023 in the rows I read [KB1].
- **Usage evidence.** citationCount 308 (DOI 10.1007/978-3-319-68204-4_22) read 20261102 20:00 UTC [S2]. Repository `AskNowQA/LC-QuAD` 98 stars, last push 20230905, read 19:51 [LQ1].

## 13. lc-quad-2 (LC-QuAD 2.0)

**Role:** both. **Kinds:** questions. **Front matter:** `kinds: [questions]`, `benchmark: lc-quad-2`.

### Dataset role

- **What it contains.** Question, paraphrase and SPARQL triples for Wikidata and for DBpedia 2018, with template ids and subgraph labels [LQ2][LQ2h].
- **Size and versions.** Paper abstract: 30,000 questions with paraphrases and SPARQL (ISWC 2019). The Hugging Face mirror `mohnish/lc_quad` loads 19,293 train and 4,781 test rows (24,074 in all), fewer than 30,000 (the card gives no reason) [LQ2s][LQ2h]. The figshare "training set for lcquad 2.0" (`train.json`, 26.6 MB) was published 20190702 [FG1].
- **Licence.** Figshare record for the training set: CC BY 4.0. The Hugging Face mirror card says `cc-by-3.0`. The GitHub repository has no LICENSE file (404) [FG1][LQ2h][LQ2]. Use CC BY 4.0 from the primary host, and flag the mismatch.
- **How it was made.** Question and query generation framework with verbalisation and paraphrasing; details are in the paper, which is paywalled, so only its abstract was read [LQ2s].
- **Used by.** Banerjee et al. (T5 and others), Tan et al. (ChatGPT) and others on the leaderboard [KB1]. Archive: no page mentions it [A1].
- **Known problems.** The 30,000 headline versus 24,074 rows in the mirror; separate gold-entity and no-gold-entity leaderboards signal that results are not comparable across systems [KB1][LQ2h].

### Benchmark role

- **What it tests.** Question to SPARQL over Wikidata and DBpedia 2018; complex questions [LQ2s].
- **Tasks, metrics and protocol.** F1 (query-string token match for some systems, answers for others) [KB1].
- **Datasets.** [lc-quad-2](lc-quad-2.md).
- **Results (community leaderboard; two lists).**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| T5-Small, gold entities/relations given | 92 | F1 | Banerjee et al. | not stated | 2022 | [KB1] |
| SGPT_Q,K, gold given (token match, answers not fetched) | 89.04 | F1 | Al Hasan Rony et al. | first-party (system's authors) | 2022 | [KB1] |
| SGPT_Q, no gold input | 83.45 | F1 | same | first-party | 2022 | [KB1] |
| ChatGPT, no gold input | 42.76 | F1 | Tan et al. | independent | 2023 | [KB1] |
| GPT-3.5v3 | 39.04 | F1 | same | independent | 2023 | [KB1] |
| FLAN-T5 | 30.14 | F1 | same | independent | 2023 | [KB1] |

- **Known problems.** Gold-input leaderboards can overstate; query-string matching does not fetch answers [KB1].
- **Usage evidence.** citationCount 276 (DOI 10.1007/978-3-030-30796-7_5) read 20261102 20:00 UTC [S2]. Repository `AskNowQA/LC-QuAD2.0` 23 stars, last push 20230905 [LQ2]. HF downloads 261, read 20:03 [LQ2h].

---

## 14. fb15k-237 (dataset), wn18rr (dataset) and the link-prediction protocol (benchmark)

These two datasets may be covered by the KG-datasets researcher; I describe them because the benchmark depends on them. Sizes are counted from the files shipped in the ConvE repository.

### fb15k-237

**Role:** dataset (benchmark: `link-prediction-fb15k-237-wn18rr`). **Kinds:** kg. **Front matter:** `kinds: [kg]`, `benchmark: link-prediction-fb15k-237-wn18rr`.

- **What it contains.** Triples of Freebase entities (MIDs) and 237 relation types, including compound-value-type paths [D5][BE1].
- **Size and versions.** Counted: 272,115 train, 17,535 validation, 20,466 test triples; 14,541 entities; 237 relations; 37 validation or test triples have an entity not seen in training [D5]. Derived from FB15k by removing near-duplicate and inverse relations (Toutanova and Chen 2015) [BE1][RO1].
- **Licence.** The Microsoft download page and the original release's terms were **not read**. The ConvE repository (MIT) redistributes the files [CE2]; the data licence is **unstated** in the sources read. Freebase content was CC BY, but I did not verify that for this release.
- **How it was made.** Sampled from FB15k, itself a Freebase subset (Bordes et al. 2013), after observing that FB15k suffers test leakage through inverse relations; per ConvE, 81% of FB15k test triples have a leaking inverse [BE1].
- **Used by.** Every KG-embedding paper cited here; Archive: no page mentions it [A1].
- **Known problems.** Reified Freebase CVT nodes were flattened into concatenated relations, creating redundant edges, only partly removed by the 237 filter [RO1]. Evaluation depends on tie-breaking (see benchmark). Over-represented entities dominate aggregate metrics [RO1].

### wn18rr

**Role:** dataset (same benchmark). **Kinds:** kg. **Front matter:** `kinds: [kg]`.

- **What it contains.** WordNet synsets and 11 lexical relations [D5].
- **Size and versions.** Counted: 86,835 train, 3,034 validation, 3,134 test; 40,943 entities; 11 relations; 420 validation or test triples have an entity unseen in training [D5]. Built by Dettmers et al. (arXiv 1707.01476, AAAI 2018) as WN18 minus inverse-relation leakage (94% leakage in WN18 per the paper) [BE1].
- **Licence.** Unstated in sources read (ConvE repository is MIT; WordNet's own licence not read) [CE2].
- **How it was made.** Removal of inverse relations from WN18 after a rule-based "inverse model" matched state of the art on WN18 and FB15k [BE1].
- **Used by.** As above.
- **Known problems.** The 420 test or validation triples with unseen entities cannot be predicted by embedding methods that need a training embedding [D5 counted]. Skewed structure: more than 60% of predictions involve fewer than one source or target peer [RO1].

### Benchmark: link-prediction-fb15k-237-wn18rr

**Role:** benchmark.

- **What it tests.** Ranking of the true head or tail among all entities for each test triple, i.e. KG completion by embeddings or rules [BE1][SU1].
- **Tasks, metrics and protocol.** For each test triple (h, r, t) rank t among all candidate tails (and h among heads) in the filtered setting (other known true triples removed), report MRR, Hits@1/3/10 and mean rank [SU1][RO1]. **Tie-breaking** matters: Sun et al. define Top, Bottom and Random and show the "Top" rule gives a perfect score to a model that always outputs a constant; they recommend Random [SU1]. Rossi et al. add that in the standard protocol some entities are over-represented, and that rankings with a "min" tie policy can inflate (CapsE, ConvKB, CrossE) [RO1].
- **Datasets.** [fb15k-237](fb15k-237.md), [wn18rr](wn18rr.md).
- **Results (filtered MRR, Random tie-breaking, from the re-evaluation by Sun et al.; "reported" = the figure in the original model paper).**

| System | Score (FB15k-237 MRR; reported) | Score (WN18RR MRR; reported) | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| TuckER | .353 (.358) | .461 (.470) | Sun et al. | independent of TuckER authors | 20200708 (v3) | [SU1] |
| RotatE | .336 (.338) | .473 (.476) | same | partly: the paper's first author also wrote RotatE | same | [SU1][RT1] |
| ConvE | .324 (.325) | .444 (.43) | same | independent | same | [SU1] |
| ConvKB | .243 (.396) | .249 (.248) | same | independent | same | [SU1] |
| CapsE | .150 (.523) | .415 (.415) | same | independent | same | [SU1] |
| KBAT | .157 (.518) | .412 (.440) | same | independent | same | [SU1] |

  Rossi et al. (2002.00819, v4 20210121) ran 16 embedding models plus a rule-based baseline on FB15k, FB15k-237, WN18, WN18RR and YAGO3-10 with full rankings; the per-model table was not machine-readable in my extraction, so no numbers are copied [RO1].
- **Known problems.** Tie handling (above); Hits@k and MRR average over a skewed test set; FB15k-237 and WN18RR come from a Freebase and a WordNet subset from the early 2010s, and entity-unseen triples exist in both [D5][RO1]. Sampled-negative variants (OGB) are not comparable to full-ranking numbers (next item).
- **Used by.** Papers listed; Archive: none [A1].
- **Usage evidence.** citationCount: ConvE (1707.01476) 3,294; Toutanova and Chen 2015 "Observed versus latent features" 1,252; Toutanova et al. 2015 EMNLP "Representing text for joint embedding of text and knowledge bases" 846; RotatE 3,024; Sun et al. re-evaluation 197; read 20261102 20:00 UTC [S2]. ConvE repository 690 stars, MIT, last push 20240329, read 19:51 [CE2].

---

## 15. ogb-link-prediction

**Role:** both. **Dataset kinds:** kg (for the KG-completion members ogbl-wikikg2 and ogbl-biokg); the other members are plain graphs. **Front matter:** `kinds: [kg]`, `benchmark: ogb-link-prediction`; benchmark `datasets: [ogbl-wikikg2, ogbl-biokg]`.

### Dataset role

- **What it contains.** Seven link-property datasets: ogbl-ppa (576,289 nodes, 30,326,273 edges), ogbl-collab, ogbl-ddi, ogbl-citation2, ogbl-vessel (externally contributed) and the two KGs ogbl-wikikg2 (Wikidata subset, 2,500,604 entities, 535 relation types, 17,137,181 edges, time split from Wikidata snapshots May, August and November 2015) and ogbl-biokg (five entity types, 93,773 nodes, 51 relation types, 5,088,434 edges, random split) [OG1].
- **Size and versions.** As above. `ogbl-wikikg` was deprecated for a bug in the validation and test negative samples; ogbl-wikikg2 replaces it (package version at least 1.2.4) [OG1]. OGB paper arXiv 20200502 (NeurIPS 2020) [OGp].
- **Licence.** Code: MIT LICENSE file. Datasets: per-dataset statement on the OGB page: ogbl-wikikg2 CC-0, ogbl-biokg CC-0, ogbl-ppa CC-0, ogbl-collab ODC-BY; others on the page not extracted [OG1][OGr].
- **How it was made.** wikikg2: all relational statements retrieved from three Wikidata snapshots, only entities and relations present in the earliest kept, training on May triples and validation or test on August or November additions. biokg: pooled from biomedical repositories with confidence levels from experimental readouts to automatic extraction [OG1].
- **Used by.** Leaderboard submitters (below). Archive: no page mentions it [A1].
- **Known problems.** Evaluation ranks the true entity against 1,000 sampled negatives (500 head, 500 tail), not against all entities, so MRR is not comparable to full-ranking MRR on FB15k-237 or WN18RR [OG1]; biokg ranks only against entities of the same type [OG1].

### Benchmark role

- **What it tests.** Link property prediction at scale with realistic splits (time, protein throughput, protein target) [OGp][OG1].
- **Tasks, metrics and protocol.** Per-dataset metric: Hits@100 (ppa), Hits@50 (collab), Hits@20 (ddi), MRR (citation2, wikikg2, biokg), ROC-AUC (vessel); unified evaluator [OG1].
- **Datasets.** [ogbl-wikikg2](ogbl-wikikg2.md), [ogbl-biokg](ogbl-biokg.md) are the KG members.
- **Results (leaderboard rows; submitters are the method authors, rows marked "OGB team" are the organisers' baselines).**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| RelEns (ogbl-wikikg2) | 0.7392 plus or minus 0.0011 | test MRR | Quanming Yao (Tsinghua), submitted | first-party | 20231015 | [OGr] |
| StarGraph + TripleRE + Text, external data (wikikg2) | 0.7305 | test MRR | Liang Yao (Tencent) | first-party | 20230104 | [OGr] |
| InterHT+ (wikikg2) | 0.7293 | test MRR | Baoxin Wang (HFL) | first-party | 20221223 | [OGr] |
| RelEns (ogbl-biokg) | 0.9618 | test MRR | Quanming Yao | first-party | 20231015 | [OGr] |
| ComplEx^2 (biokg) | 0.8583 | test MRR | Lorenzo Loconte (Edinburgh) | first-party | 20231028 | [OGr] |
| ComplEx (biokg), organisers' baseline | 0.8095 | test MRR | OGB team | first-party baseline | 20200610 | [OGr] |

  The leaderboard rows are self-submitted with reported hardware and parameter counts; I did not check for reproduction. The newest dated row I saw is December 2023; whether later rows exist beyond the page snapshot read 20261102 20:05: **unstated**.
- **Known problems.** Self-reported; sampled-negative evaluation; deprecated predecessor [OG1][OGr].
- **Usage evidence.** citationCount 4,139 (2005.00687, NeurIPS 2020) read 20261102 20:00 UTC [S2]. Repository `snap-stanford/ogb` 2,100 stars, MIT, last push 20250506, read 19:51 [OGB1].

---

## Sources

Read times are UTC from the clock; "WebFetch" reads were not individually time-stamped (between 19:54 and 19:58).

Papers (arXiv abstract page and HTML full text, fetched by script):
1. https://arxiv.org/abs/2410.10813 and /html/2410.10813 : LongMemEval paper (read 20261102 19:50)
3. https://arxiv.org/abs/2507.05257 and /html/2507.05257 : MemoryAgentBench, v4 (read 20261102 19:50)
5. https://arxiv.org/abs/2602.22769 and /html/2602.22769 : AMA-Bench, v4 (read 20261102 19:50)
6. https://arxiv.org/abs/2605.18421 and /html/2605.18421 : EvoMemBench, v3 (read 20261102 19:50)
7. https://arxiv.org/abs/2402.17753 and /html/2402.17753 : LoCoMo paper (read 20261102 19:50)
8. https://arxiv.org/abs/2610.30755 and /html/2610.30755 : Bao et al., "Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought", v1 (read 20261102 19:50)
9. https://arxiv.org/abs/2602.11745 and /html/2602.11745 : Text2GraphQuery-Bench, v2 (read 20261102 19:50)
TC2. https://arxiv.org/abs/2506.21445 : Text2Cypher Across Languages (read 20261102 19:50); the same tag is used for its Hugging Face translated test set below
LP2. https://arxiv.org/abs/2602.10715 and /html/2602.10715 : LoCoMo-Plus (read 20261102 19:50)
T1. https://arxiv.org/abs/2308.02357 and /html/2308.02357 : Text2KGBench paper (read 20261102 19:50)
TC1. https://arxiv.org/abs/2412.10064 and /html/2412.10064 : Text2Cypher paper (read 20261102 19:50)
CT1. https://arxiv.org/abs/2609.36987 and /html/2609.36987 : CypherTurn (read 20261102 19:50)
TS2. https://arxiv.org/abs/2610.13648 and /html/2610.13648 : SPARQL-LLM in the TEXT2SPARQL 2026 Challenge (read 20261102 19:50)
TS1. https://arxiv.org/abs/2510.02200 and /html/2510.02200 : ARUQULA, TEXT2SPARQL 2025 participant (read 20261102 19:54)
PC1. https://arxiv.org/abs/2606.08481 : PIPE-Cypher (read 20261102 19:54)
-. https://arxiv.org/abs/2607.22690, https://arxiv.org/abs/2512.14277 : fetched 19:54, used only as leads or for citation counts
M1. https://arxiv.org/abs/2504.19413 : Mem0 paper abstract (read 20261102 20:06)
Z3. https://arxiv.org/abs/2501.13956 : Zep paper abstract and LongMemEval section (read 20261102 20:06)
SU1. https://arxiv.org/abs/1911.03903 : Sun et al., A Re-evaluation of KGC Methods (read 20261102 20:04)
RO1. https://arxiv.org/abs/2002.00819 : Rossi et al., KGE for link prediction, comparative analysis (read 20261102 20:04)
BE1. https://arxiv.org/abs/1707.01476 : ConvE / WN18RR paper (read 20261102 20:04)
RT1. https://arxiv.org/abs/1902.10197 : RotatE (read 20261102 20:04)
OGp. https://arxiv.org/abs/2005.00687 : Open Graph Benchmark paper (read 20261102 20:04)

Repositories (GitHub API metadata, LICENSE file and README, read 20261102 19:51):
2. https://github.com/xiaowu0162/LongMemEval (MIT)
L1. https://github.com/snap-research/locomo (LICENSE.txt: CC BY-NC 4.0)
MA1. https://github.com/HUST-AI-HYZ/MemoryAgentBench (MIT)
LP1. https://github.com/xjtuleeyf/Locomo-Plus (no LICENSE file)
AB1. https://github.com/AMA-Bench/AMA-Bench (MIT)
EV1. https://github.com/DSAIL-Memory/EvoMemBench (no LICENSE file)
T2. https://github.com/cenguix/Text2KGBench (Apache-2.0)
TC3. https://github.com/neo4j-labs/text2cypher (CC0-1.0)
TG1. https://github.com/ldbc/Text2GraphQuery-DataGen (Apache-2.0)
CT2. https://github.com/BarryQ/CypherTurn (no LICENSE file)
SL1. https://github.com/sib-swiss/sparql-llm (MIT)
LQ1. https://github.com/AskNowQA/LC-QuAD (GPL-3.0)
LQ2. https://github.com/AskNowQA/LC-QuAD2.0 (no LICENSE file)
OGB1. https://github.com/snap-stanford/ogb (MIT)
CE2. https://github.com/TimDettmers/ConvE (MIT; ships FB15k-237.tar.gz and WN18RR.tar.gz)
Z2. https://github.com/getzep/zep-papers/issues/5 : "Revisiting Zep's 84% LoCoMo Claim", opened 20250508 by a Mem0 co-founder (read 20261102 20:06)

Hugging Face (API metadata and dataset card):
H1. xiaowu0162/longmemeval-cleaned (license mit; read 20261102 19:51)
H2. ai-hyz/MemoryAgentBench (license mit; read 19:51)
H3. AMA-bench/AMA-bench (license mit; read 19:56)
H4. neo4j/text2cypher-2024v1 (apache-2.0; splits 39,554 and 4,833; read 19:51)
H5. neo4j/text2cypher-2025v1 (apache-2.0; card otherwise empty; read 19:56)
TC2. mgoNeo4j/translated_text2cypher24_testset (apache-2.0; read 19:51)
LQ2h. https://huggingface.co/api/datasets/mohnish/lc_quad (cc-by-3.0; splits; read 20:03)

Downloaded data files (own folder, read with `python3 -I`, counted):
D1. longmemeval_oracle.json from the cleaned HF repo (read 20261102 19:53)
D2. data/locomo10.json from snap-research/locomo (read 19:53)
D3. data/locomo_plus.json from Locomo-Plus (read 19:56)
D4. test/open_end_qa_set.jsonl from AMA-bench/AMA-bench (read 19:57)
D5. FB15k-237.tar.gz and WN18RR.tar.gz from the ConvE repository (read 20:04)

Web pages:
P1. https://dev.to/penfieldlabs/we-audited-locomo-64-of-the-answer-key-is-wrong-and-the-judge-accepts-up-to-63-of-intentionally-33lg : Penfield LoCoMo audit post (read 20261102 19:54). Author's profile on the page describes a memory product.
Z1. https://blog.getzep.com/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/ : Zep blog, 20250506, updated 20260603 (read 20261102 19:54)
NB1. https://neo4j.com/blog/developer/text2cypher-model-struggles-dataset-improvements/ : Neo4j blog, 20250303 (read 20261102 19:54)
CE1. https://ceur-ws.org/Vol-4094/ : proceedings of the First International TEXT2SPARQL Challenge (WebFetch, about 19:55)
ZE1. https://zenodo.org/api/records/7916716 : Text2KGBench record, license cc-by-4.0 (read 20261102 20:07)
LE1. https://www.eurecom.edu/en/node/4899768 : Text2KGBench-LettrIA abstract (read 20261102 20:07)
KB1. https://raw.githubusercontent.com/KGQA/leaderboard/gh-pages/dbpedia/lcquad.md : community KGQA leaderboard page for LC-QuAD (read 20261102 20:03)
LQ1s. https://link.springer.com/chapter/10.1007/978-3-319-68204-4_22 : LC-QuAD 1.0 abstract (read 20:03)
LQ2s. https://link.springer.com/chapter/10.1007/978-3-030-30796-7_5 : LC-QuAD 2.0 abstract (read 20:03)
FG1. https://api.figshare.com/v2/articles/8479055 : LC-QuAD 2.0 training set, license CC BY 4.0 (read 20261102 20:08)
OG1. https://ogb.stanford.edu/docs/linkprop/ : OGB link property prediction page (read 20261102 20:05)
OGr. https://ogb.stanford.edu/docs/leader_linkprop/ : OGB link-prediction leaderboards (read 20261102 20:05)
S2. Semantic Scholar batch API, `citationCount` per paper id (read 20261102 20:00; three 429 retries before success)
A1. grep over `kb-kg/`, `pinakes/`, `DECISIONS.md`, `README.md` in the repository worktree (read 20261102 20:06)

Not reachable: https://text2sparql.aksw.org (connection refused, 20261102 19:5x), http://lc-quad.sda.tech (no response, 20:03), Spider4SPARQL on Hugging Face (401).

## Items I did not cover or could not verify

- TEXT2SPARQL official results page and dataset licence (site unreachable).
- LongMemEval-V2 (named in the LongMemEval README, not read); Text2KGBench-LettrIA result tables; Rossi et al.'s per-model tables; the AMA-Bench Hugging Face leaderboard; the Penfield audit repository; the LazyMem claim about LoCoMo errors; OpenAlex counts (Semantic Scholar only).
- Licences of the upstream sources of many derived sets (ShareGPT, UltraChat, MSC, WebNLG for non-Text2KGBench uses, MQuAKE, CL-Bench, BFCL, ALFWorld, Freebase and WordNet releases).
