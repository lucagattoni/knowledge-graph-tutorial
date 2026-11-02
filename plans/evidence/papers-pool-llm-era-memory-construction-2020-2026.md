# Candidate pool: agent memory, KG construction, LLM+KG, graph query, code graphs, plain-file KBs (2020 to 2026)

Researcher output for the papers chapter. Written 20261102 (UTC). Area: agent memory; temporal KGs for agents; KG
construction with LLMs; unifying LLMs and KGs; natural language to graph query; code knowledge graphs; plain-file or
wiki knowledge bases. Tests: origin, turning point, widely built on, survey of record (definitions in the brief).

How to read the entries
- Citation counts are Semantic Scholar Graph API `citationCount` [1] [2], read at the time stated in each entry.
  They count citing works Semantic Scholar knows; they are not Google Scholar counts. Counts below 20 are marked
  "too new to count" and are not used as evidence for any test.
- "Read depth": **abstract** = the arXiv API record [3]; **html** = the arXiv HTML or ar5iv rendering read through a
  fetch tool that summarises to a prompt (so quotes below are the tool's extracts, spot-checks of the paper text,
  not a full read); **alphaXiv full text** = the extracted text of the paper, partly read. No paper here was read
  end to end. Where a relation rests on an abstract only, it says so.
- Clock: all read times are UTC from `date -u`; batch times are given where individual readings were not taken.
- "First-party" marks results run by a system's own authors.
- Reference ids are arXiv ids. Sources are numbered at the end.

Summary table (strongest first)

| # | Key | Short name | Year | Tests | Citations (S2) |
|---|---|---|---|---|---|
| 1 | 2304.03442 | Generative Agents | 2023 | origin, widely-built-on | 6297 |
| 2 | 2310.08560 | MemGPT | 2023 | origin, widely-built-on | 1753 |
| 3 | 2306.08302 | Unifying LLMs and KGs | 2023 | survey-of-record, widely-built-on | 1927 |
| 4 | 2504.19413 | Mem0 | 2025 | widely-built-on, origin (Mem0g variant) | 862 |
| 5 | 2502.12110 | A-MEM | 2025 | origin, widely-built-on | 1332 |
| 6 | 2402.17753 | LoCoMo | 2024 | widely-built-on, turning-point | 1075 |
| 7 | 2410.10813 | LongMemEval | 2024 | widely-built-on | 861 |
| 8 | 2404.13501 | Memory mechanism survey | 2024 | survey-of-record | 889 |
| 9 | 2309.02427 | CoALA | 2023 | origin, survey-of-record | 575 |
| 10 | 2501.13956 | Zep / Graphiti | 2025 | origin, widely-built-on | 456 |
| 11 | 2305.10250 | MemoryBank | 2023 | origin, widely-built-on | 854 |
| 12 | 2305.13168 | LLMs for KG construction and reasoning | 2023 | turning-point, widely-built-on | 337 |
| 13 | 2512.13564 | Memory in the Age of AI Agents | 2025 | survey-of-record | 314 |
| 14 | 2508.19828 | Memory-R1 | 2025 | origin | 246 |
| 15 | 2404.03868 | EDC | 2024 | origin, widely-built-on | 181 |
| 16 | 2308.02357 | Text2KGBench | 2023 | origin | 149 |
| 17 | 2010.11967 | Language Models are Open KGs | 2020 | origin | unstated |
| 18 | 2410.14684 | RepoGraph | 2024 | origin | 149 |
| 19 | 2408.03910 | CodexGraph | 2024 | origin | 114 |
| 20 | 2412.10064 | Text2Cypher | 2024 | origin | 73 |
| 21 | 2510.20345 | LLM-empowered KGC survey | 2025 | survey-of-record | 51 |
| 22 | 2505.23628 | AutoSchemaKG | 2025 | origin | 38 |
| 23 | 2610.30755 | Naive RAG Is Stronger | 2026 | turning-point | 0 (too new) |
| 24 | 2610.34073 | Memory Tax | 2026 | turning-point | unstated |
| 25 | 2606.24775 | Agent-native memory study | 2026 | turning-point | unstated |
| 26 | 2605.15184 | Is Grep All You Need? | 2026 | turning-point | unstated |
| 27 | 2607.26637 | Filesystem-based memory | 2026 | origin, turning-point | unstated |
| 28 | 2603.27277 | Codebase-Memory | 2026 | origin | unstated |

---

## 1. Generative Agents (2023)

- **Title:** Generative Agents: Interactive Simulacra of Human Behavior
- **Authors:** Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai (6 in total) [3]
- **Venue:** ACM Symposium on User Interface Software and Technology (UIST), per the Semantic Scholar venue field [1]; the arXiv record names none [3].
- **First version:** 20230407 [3]
- **Link:** https://arxiv.org/abs/2304.03442
- **Citations:** 6297, Semantic Scholar Graph API [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Origin.* The abstract describes "an architecture that extends a large language model to store a complete record of the agent's experiences using natural language, synthesize those memories over time into higher-level reflections, and retrieve them dynamically to plan behavior" [3]. The full text defines the memory stream and a retrieval score from recency, importance and relevance, summed with equal weights, and reflections stored back in the stream [6]. This is the earliest of the LLM agent-memory designs in this pool.
  - *Widely built on.* 6297 citations [1]. MemGPT's related-work section cites it ("Park et al. (2023) propose adding memory to LLMs and using the LLM as a planner") [4]; CoALA cites it as an example of retrieval from episodic memory [7].
- **Idea:** Agents keep every observation as a timestamped natural-language record, periodically write higher-level reflections from them, and retrieve by a weighted score of recency, importance and relevance. In a 25-agent sandbox, removing observation, planning or reflection each lowered believability (TrueSkill: full architecture 29.89, no reflection 26.88, no reflection or planning 25.64, human crowdworkers 22.95, no memory/planning/reflection 21.21) [6]. First-party result.
- **Relations:**
  - *Built on by* MemGPT (#2): cited as prior work on memory plus planning [4]. Same-sentence fact: "Park et al. (2023) propose adding memory to LLMs and using the LLM as a planner".
  - *Built on by* CoALA (#9): cited as an agent that "retrieves relevant events from episodic memory" [7].
  - *Contrast, other era:* it keeps memory as plain text records, not as a graph; the graph-shaped memory systems of 2025 (Zep #10, A-MEM #5) answer a gap the abstract does not mention (unstated whether the authors discuss it).
- **Read:** abstract [3] plus first 100,000 characters of the ar5iv text [6]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [1] [3] [4] [6] [7]

## 2. MemGPT (2023)

- **Title:** MemGPT: Towards LLMs as Operating Systems
- **Authors:** Charles Packer, Sarah Wooders, Kevin Lin (7 in total) [3]
- **Venue:** none stated in the arXiv record [3] (Semantic Scholar lists "arXiv.org" [1]).
- **First version:** 20231012 [3]
- **Link:** https://arxiv.org/abs/2310.08560
- **Citations:** 1753, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Origin.* Introduces "virtual context management", drawing on hierarchical memory in operating systems, with a "main context (analogous to main memory/physical memory/RAM)" and an "external context (analogous to disk memory/disk storage)" [4]. Also introduces the Deep Memory Retrieval (DMR) task ("We introduce a new 'deep memory retrieval' (DMR) task based on the MSC dataset") [4] that Zep later reports against [5].
  - *Widely built on.* 1753 citations [1]. It is a named baseline in A-MEM (compared with LoCoMo, ReadAgent, MemoryBank and MemGPT) [8], in the Mem0 paper [9], and a rival in Zep's DMR table [5]. The archive page records that the Letta repository is the successor ("Letta (f.k.a. MemGPT)") [10].
- **Idea:** Treat the model's limited context window like fast memory and move data to and from slower external storage, with the model itself issuing the moves and interrupts handling control flow. Evaluated on document analysis and multi-session chat; DMR accuracy with GPT-4 Turbo 93.4% against 35.3% for the fixed-context baseline [4]. First-party result.
- **Relations:**
  - *Builds on* Generative Agents (#1): cited as prior memory-plus-planning work [4].
  - *Answered / evaluated by* Zep (#10): Zep reports "94.8% vs 93.4%" on DMR against MemGPT [3] [5], and calls DMR the benchmark "the MemGPT team established" [3].
  - *Evaluated by* A-MEM (#5), Mem0 (#4): both list it as a baseline on LoCoMo [8] [9].
  - *Evaluated by* the Agent-native study (#25): Letta (MemGPT) is among the systems tested [11].
- **Read:** abstract [3] plus html extract (introduction, DMR table, related work) [4]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [1] [3] [4] [5] [8] [9] [10] [11]

## 3. Unifying LLMs and KGs: a Roadmap (2023)

- **Title:** Unifying Large Language Models and Knowledge Graphs: A Roadmap
- **Authors:** Shirui Pan, Linhao Luo, Yufei Wang (6 in total) [3]
- **Venue:** IEEE Transactions on Knowledge and Data Engineering (TKDE) 2024, per the arXiv journal reference [3].
- **First version:** 20230614 [3]
- **Link:** https://arxiv.org/abs/2306.08302
- **Citations:** 1927, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Survey of record.* The abstract sets out "a forward-looking roadmap" with three frameworks: "KG-enhanced LLMs", "LLM-augmented KGs" (embedding, completion, construction, graph-to-text, question answering) and "Synergized LLMs + KGs" [3]. The archive's survey list gives the same three-way split [12].
  - *Widely built on.* 1927 citations [1], the highest count of any LLM+KG survey in this pool.
- **Idea:** LLMs are fluent but black-box and weak on facts; KGs store facts explicitly but are hard to build and keep current. The paper reviews work in three families, pairing each with open problems [3].
- **Relations:**
  - *Frames* LLM-for-construction work such as Zhu et al. (#12), EDC (#15), AutoSchemaKG (#22): these are instances of the "LLM-augmented KGs: construction" family. This mapping is my reading; the roadmap's abstract names construction as a task [3] but the pages read do not say these papers are covered (EDC and AutoSchemaKG are later than it).
  - *Succeeded by* the construction survey (#21), which restates the field in 2025 as a shift from "rule-based and statistical pipelines to language-driven and generative frameworks" [3].
  - *Cross-era:* the "KG-enhanced LLMs" family continues the 2020 idea of keeping knowledge in an explicit store next to the model (RAG, 2005.11401, another researcher's area).
- **Read:** abstract [3]; read 20261102 19:57 UTC.
- **Sources:** [1] [3] [12]

## 4. Mem0 (2025)

- **Title:** Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory
- **Authors:** Prateek Chhikara, Dev Khant, Saket Aryan (5 in total) [3]
- **Venue:** European Conference on Artificial Intelligence (ECAI), per Semantic Scholar [1]; the arXiv record names none [3].
- **First version:** 20250428 [3]
- **Link:** https://arxiv.org/abs/2504.19413
- **Citations:** 862, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Widely built on.* 862 citations [1]. A named baseline in Memory-R1 [13], in the Naive-RAG study [14], the Agent-native study [11] and Hindsight [15].
  - *Origin (partial).* The abstract introduces Mem0, which extracts, consolidates and retrieves salient information, and Mem0g, "an enhanced variant that leverages graph-based memory representations" [3]. Details of the update operations (ADD, UPDATE, DELETE, NOOP chosen by the LLM) and of the Neo4j graph with outdated relations marked invalid come from the alphaXiv generated report only, a lead not checked in the paper text [24].
- **Idea:** Extract salient facts from each message pair, compare them with stored facts by vector similarity, and let the LLM pick the memory operation. Mem0g keeps entities and relation triplets. On LoCoMo (LLM-as-judge): Mem0 66.88, Mem0g 68.44, Zep 65.99, best RAG 60.97, full context 72.90; p95 latency 91% lower than full context [9] [3]. First-party result.
- **Relations:**
  - *Evaluates* Zep (#10), A-MEM (#5), MemGPT (#2), MemoryBank (#11), LangMem, ReadAgent, LoCoMo's own baselines, and OpenAI's memory [9]. It says Zep's memory graph "consumes in excess of 600k tokens" and needed hours before memories were retrievable [9]; this is a competitor's claim about Zep.
  - *Answered by* A-MEM (#5): its introduction says Mem0 "incorporates graph databases" but that "reliance on predefined schemas and relationships fundamentally limits their adaptability" [8].
  - *Disagreement:* Zep scores 65.99 in Mem0's own run [9], but 75.14 in Hindsight's LoCoMo table, whose baseline numbers are "claimed" figures taken from another vendor's report and not reproduced by Hindsight's authors [15]. The sources do not settle which Zep number is right.
  - *Evaluated by* independent studies #23, #24, #25, which test Mem0 against plain retrieval [11] [14].
- **Read:** abstract [3] plus html extract (baselines, Table 2, Zep comparison) [9]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [1] [3] [8] [9] [11] [13] [14] [15]

## 5. A-MEM (2025)

- **Title:** A-MEM: Agentic Memory for LLM Agents
- **Authors:** Wujiang Xu, Zujie Liang, Kai Mei (6 in total) [3]
- **Venue:** NeurIPS 2025, from the arXiv comment [3].
- **First version:** 20250217 [3]
- **Link:** https://arxiv.org/abs/2502.12110
- **Citations:** 1332, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Origin.* Introduces Zettelkasten-style agent memory: each memory is a note with LLM-generated keywords, tags and context, linked to similar notes, and old notes are rewritten when new ones arrive ("memory evolution") [3].
  - *Widely built on.* 1332 citations [1]; a baseline in Mem0 [9], Memory-R1 [13], the Naive-RAG study [14], Memory Tax [16] and the Agent-native study [11].
- **Idea:** Let the agent organise its own memory instead of following fixed insert/retrieve operations: create a structured note, link it to neighbours by embedding similarity plus an LLM check, and let new notes trigger updates to old ones [3]. First-party results on LoCoMo and DialSim, compared with LoCoMo (no memory), ReadAgent, MemoryBank and MemGPT [8]; the authors report no error bars [8].
- **Relations:**
  - *Answers* graph-database memory (Mem0): "reliance on predefined schemas and relationships fundamentally limits their adaptability" [8].
  - *Evaluates / builds on* MemGPT (#2) and MemoryBank (#11) as baselines [8].
  - *Evaluated by* Memory Tax (#24), which lists A-MEM among its flat-store systems and finds many dedicated memory systems "underperform naive RAG in many cases" [16]; in one results table every A-MEM score carries a negative delta (from -0.3 to -8.7 points); that the delta is measured against the RAG reference was not confirmed in the text read [16].
- **Read:** abstract [3] plus html extract (baselines, limitations) [8]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [1] [3] [8] [9] [11] [13] [14] [16]

## 6. LoCoMo (2024)

- **Title:** Evaluating Very Long-Term Conversational Memory of LLM Agents
- **Authors:** Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov (6 in total) [3]
- **Venue:** Annual Meeting of the ACL, per Semantic Scholar [1]; the arXiv record names none [3].
- **First version:** 20240227 [3]
- **Link:** https://arxiv.org/abs/2402.17753
- **Citations:** 1075, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Widely built on.* 1075 citations [1]. Mem0, A-MEM, Memory-R1, Hindsight, the Naive-RAG study and the Agent-native study all report on it [8] [9] [13] [14] [15].
  - *Turning point (benchmark).* Before it, long-term dialogue work "focus[ed] on evaluating model responses within contexts spanning no more than five chat sessions"; it supplies conversations of about 300 turns and 9K tokens over up to 35 sessions and finds that long-context LLMs and RAG "still substantially lag behind human performance" [3].
- **Idea:** A machine-human pipeline generates very long dialogues grounded in personas and event graphs; the benchmark has question answering, event summarisation and multimodal dialogue tasks [3].
- **Relations:**
  - *Evaluates* RAG and long-context models (abstract) [3].
  - *Used by* Mem0 (#4), A-MEM (#5), Memory-R1 (#14) and the independent comparisons #23 to #25 [9] [8] [13] [14] [11].
  - *Sibling of* LongMemEval (#7).
  - Belongs equally to the benchmarks chapter; only one home per fact (see the brief): this entry proposes the paper, not a benchmark page.
- **Read:** abstract [3]; read 20261102 19:57 UTC.
- **Sources:** [1] [3] [8] [9] [11] [13] [14] [15]

## 7. LongMemEval (2024)

- **Title:** LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory
- **Authors:** Di Wu, Hongwei Wang, Wenhao Yu (6 in total) [3]
- **Venue:** ICLR 2025, from the arXiv comment [3].
- **First version:** 20241014 [3]
- **Link:** https://arxiv.org/abs/2410.10813
- **Citations:** 861, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Widely built on.* 861 citations [1]. Zep, Hindsight, Memory-R1, the Naive-RAG study, Is-Grep-All-You-Need and the Agent-native study all report on it [5] [15] [13] [14] [17] [11].
- **Idea:** 500 questions embedded in scalable chat histories that test five abilities (extraction, multi-session reasoning, temporal reasoning, knowledge updates, abstention); commercial chat assistants and long-context LLMs show "a 30% accuracy drop on memorizing information across sustained interactions". It also proposes a three-stage framing (indexing, retrieval, reading) and optimisations such as session decomposition and time-aware query expansion [3].
- **Relations:**
  - *Used by* Zep (#10) as its "more challenging" evaluation beyond DMR [3] [5].
  - *Used by* #23, #24, #25, #26. The grep study draws a 116-question sample of LongMemEval and finds, with inline tool output, grep above vector retrieval in every harness-model pair it ran [17].
  - *Sibling of* LoCoMo (#6).
- **Read:** abstract [3]; read 20261102 19:57 UTC.
- **Sources:** [1] [3] [5] [11] [13] [14] [15] [17]

## 8. Memory mechanism survey (2024)

- **Title:** A Survey on the Memory Mechanism of Large Language Model based Agents
- **Authors:** Zeyu Zhang, Xiaohe Bo, Chen Ma (9 in total) [3]
- **Venue:** ACM Transactions on Information Systems, per Semantic Scholar [1]; the arXiv record names none [3].
- **First version:** 20240421 [3]
- **Link:** https://arxiv.org/abs/2404.13501
- **Citations:** 889, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Survey of record.* The abstract says previous memory mechanisms "are scattered in different papers, and there lacks a systematical review"; it covers what memory is, why agents need it, how to design and evaluate it, and applications [3]. It is the earliest agent-memory survey in this pool and the one with the highest count (889 [1]).
- **Idea:** A systematic map of memory design and evaluation for LLM agents, with a repository of papers [3].
- **Relations:**
  - *Succeeded by* the 2025 survey "Memory in the Age of AI Agents" (#13), whose abstract says the field "has become increasingly fragmented" and that traditional long/short-term taxonomies "have proven insufficient" [3].
  - *Builds on* CoALA (#9) as a framework: unstated; the abstract does not name it.
- **Read:** abstract [3]; read 20261102 19:57 UTC.
- **Sources:** [1] [3]

## 9. CoALA (2023)

- **Title:** Cognitive Architectures for Language Agents
- **Authors:** Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan (4 in total) [3]
- **Venue:** Transactions on Machine Learning Research (TMLR); the arXiv comment says v3 is the "TMLR camera ready version" [3].
- **First version:** 20230905 [3]
- **Link:** https://arxiv.org/abs/2309.02427
- **Citations:** 575, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Origin.* Names a memory taxonomy for language agents: working memory ("active and readily available information as symbolic variables for the current decision cycle"), episodic ("experience from earlier decision cycles"), semantic ("knowledge about the world and itself") and procedural (in the weights or in the agent's code) [7].
  - *Survey of record (framework).* The abstract says it "draw[s] on the rich history of cognitive science and symbolic artificial intelligence" and uses CoALA "to retrospectively survey and organize a large body of recent work" [3].
- **Idea:** A conceptual framework: modular memories, a structured action space (internal memory actions and external actions) and a decision cycle [3].
- **Relations:**
  - *Builds on* Generative Agents (#1) as an example of episodic retrieval [7].
  - *Cross-era:* it deliberately reaches back to symbolic-AI cognitive architectures (production systems, expert-system era) per its abstract [3]; the specific systems it names were not read.
  - *Used by* the 2024 and 2025 surveys (#8, #13): unstated in the abstracts.
- **Read:** abstract [3] plus first 100,000 characters of html [7]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [1] [3] [7]

## 10. Zep / Graphiti (2025)

- **Title:** Zep: A Temporal Knowledge Graph Architecture for Agent Memory
- **Authors:** Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais (5 in total) [3]
- **Venue:** none stated [3] (Semantic Scholar lists "arXiv.org" [1]).
- **First version:** 20250120 [3]
- **Link:** https://arxiv.org/abs/2501.13956
- **Citations:** 456, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Origin.* The abstract presents Graphiti, "a temporally-aware knowledge graph engine that dynamically synthesizes both unstructured conversational data and structured business data while maintaining historical relationships" [3]; the paper says "Zep implements a bi-temporal model" [5]. It is the one temporal-KG design for agent memory that the other papers in this pool name.
  - *Widely built on.* 456 citations [1]; a baseline in Mem0 [9], Hindsight [15] and the Agent-native study [11].
- **Idea:** Store conversations and business data as a graph in which every fact has time information, invalidate rather than delete changed facts, and retrieve over the graph. First-party results: DMR 94.8% against MemGPT's 93.4%; on LongMemEval, with full-context prompting as the baseline, gpt-4o-mini 63.8% against 55.4% accuracy and 3.20 s against 31.3 s latency, gpt-4o 71.2% against 60.2% and 2.58 s against 28.9 s [3] [5]. The authors state the DMR conversations hold only 60 messages, "easily fitting within current LLM context windows" [5].
- **Relations:**
  - *Answers / evaluates* MemGPT (#2) on its own DMR benchmark [3] [5].
  - *Evaluates on* LongMemEval (#7) [3] [5].
  - *Evaluated by* Mem0 (#4): 65.99 judge score on LoCoMo, with a memory footprint over 600k tokens, both Mem0's claims [9]. In the Agent-native study Zep "leads Knowledge Update with 44.4 Substring EM" and "needs 155.1 s to exceed 84 utility" [11] (as summarised by the fetch tool).
  - *Cross-era:* the bi-temporal model is a database-field idea (valid time and transaction time); the paper's pages read do not cite its origin, so the link to the databases thread is **unstated**.
  - *Archive note:* the open-source weight of Zep sits in the Graphiti repository; the `getzep/zep` repository is now examples for Zep Cloud [10].
- **Read:** abstract [3] plus html extract (Sections 2.1, 4.2, 4.3.2, Table 2) [5]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [1] [3] [5] [9] [10] [11] [15]

## 11. MemoryBank (2023)

- **Title:** MemoryBank: Enhancing Large Language Models with Long-Term Memory
- **Authors:** Wanjun Zhong, Lianghong Guo, Qiqi Gao (5 in total) [3]
- **Venue:** AAAI Conference on Artificial Intelligence, per Semantic Scholar [1]; the arXiv record names none [3].
- **First version:** 20230517 [3]
- **Link:** https://arxiv.org/abs/2305.10250
- **Citations:** 854, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Origin.* A memory updating mechanism "inspired by the Ebbinghaus Forgetting Curve theory", so the model forgets and reinforces memory by time elapsed and relative significance [3].
  - *Widely built on.* 854 citations [1]; a baseline in A-MEM [8] and Mem0 [9].
- **Idea:** Store dialogue, summarise it into events and a user portrait, retrieve relevant memories, and decay or reinforce them over time; demonstrated with a companion chatbot, SiliconFriend, on ChatGPT and ChatGLM [3]. Evaluation is by simulated dialogues and a small qualitative study; first-party.
- **Relations:**
  - *Parallel to* Generative Agents (#1), same year; whether either cites the other: unstated.
  - *Evaluated by* A-MEM (#5) and Mem0 (#4) as a baseline on LoCoMo [8] [9].
- **Read:** abstract [3]; read 20261102 19:57 UTC.
- **Sources:** [1] [3] [8] [9]
- **Note:** weakest of the "origin" entries in this pool; the forgetting-curve idea does not recur in the independent studies read (#23 to #25). Keep or drop at the owner's call.

## 12. LLMs for KG construction and reasoning (2023)

- **Title:** LLMs for Knowledge Graph Construction and Reasoning: Recent Capabilities and Future Opportunities
- **Authors:** Yuqi Zhu, Xiaohan Wang, Jing Chen (9 in total) [3]
- **Venue:** World Wide Web journal, from the arXiv comment [3].
- **First version:** 20230522 [3]
- **Link:** https://arxiv.org/abs/2305.13168
- **Citations:** 337, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Turning point (independent evaluation).* "An exhaustive quantitative and qualitative evaluation" over eight datasets and four tasks (entity and relation extraction, event extraction, link prediction, question answering). Finding: GPT-4 is "more suited as inference assistants rather than few-shot information extractors" [3].
  - *Widely built on.* 337 citations [1].
- **Idea:** Test ChatGPT and GPT-4 on construction and reasoning tasks, introduce a Virtual Knowledge Extraction task (VINE dataset), and propose AutoKG, a multi-agent approach [3].
- **Relations:**
  - *Framed by* the Roadmap (#3), whose "LLM-augmented KGs" family it tests [3].
  - *Answered by* EDC (#15) and AutoSchemaKG (#22), which target the limit that LLM extraction struggles to scale: EDC says prior LLM methods "are currently limited to small and domain-specific scenarios" [18]. Whether EDC cites this paper: unstated.
  - *Cross-era:* the extractors it is compared with (fine-tuned supervised models) are the pre-LLM information-extraction line; the specific baselines were not read.
- **Read:** abstract [3]; read 20261102 19:57 UTC.
- **Sources:** [1] [3] [18]

## 13. Memory in the Age of AI Agents (2025)

- **Title:** Memory in the Age of AI Agents
- **Authors:** Yuyang Hu, Shichun Liu, Yanwei Yue (47 in total) [3]
- **Venue:** none stated [3].
- **First version:** 20251215 [3]
- **Link:** https://arxiv.org/abs/2512.13564
- **Citations:** 314, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Survey of record.* Separates agent memory from "LLM memory, retrieval augmented generation (RAG), and context engineering", then organises it by forms (token-level, parametric, latent), functions (factual, experiential, working) and dynamics (formation, evolution, retrieval), and compiles benchmarks and open-source frameworks [3]. Memory Tax shares an author with it (Yuyang Hu is on both author lists) [3] [16]; the archive's timeline uses it to separate agent memory from RAG and context engineering [12].
- **Idea:** A unified taxonomy for a field it calls "increasingly fragmented" [3].
- **Relations:**
  - *Succeeds* the 2024 survey (#8) by its own framing [3].
  - *Cites / maps* Generative Agents (#1), MemGPT (#2), Zep (#10), Mem0 (#4), A-MEM (#5): expected for a survey but not checked in the text read (abstract only).
- **Read:** abstract [3]; read 20261102 19:57 UTC.
- **Sources:** [1] [3] [12] [16]

## 14. Memory-R1 (2025)

- **Title:** Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning
- **Authors:** Sikuan Yan, Xiufeng Yang, Zuchao Huang (13 in total) [3]
- **Venue:** Annual Meeting of the ACL, per Semantic Scholar [1]; the arXiv record (v5) names none [3].
- **First version:** 20250827 [3]
- **Link:** https://arxiv.org/abs/2508.19828
- **Citations:** 246, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Origin.* Learns memory management by reinforcement learning: a Memory Manager that learns ADD, UPDATE, DELETE, NOOP and an Answer Agent, both trained with PPO or GRPO on outcome rewards, "with only 152 training QA pairs" [3].
- **Idea:** Replace the heuristic, prompt-driven write path (as in Mem0) with a policy trained on question-answering reward [3]. First-party: against the strongest baseline named in Section 4.2 (MemoryOS), Memory-R1-GRPO on LLaMA-3.1-8B improves overall F1 by 28.5%; but in Table 1 a supervised variant, Memory-SFT, scores 42.81 F1 against MemoryOS's 35.04, so MemoryOS is not the strongest baseline and the real GRPO gain over Memory-SFT is about 5% (fetch-tool reading of the paper; not re-checked against the table) [13].
- **Relations:**
  - *Builds on* Mem0 (#4): its Memory Manager learns the operation set ADD/UPDATE/DELETE/NOOP [3]; the alphaXiv generated report of the Mem0 paper lists the same four operations for Mem0 (a lead, not checked in the Mem0 paper text) [24].
  - *Evaluates* A-MEM (#5), Mem0 (#4), MemoryOS and a RAG baseline; MemGPT only as the source of the MSC data [13].
  - *Cross-trend:* the reinforcement-learning approach parallels Search-R1 (another researcher's area).
- **Read:** abstract [3] plus first 100,000 characters of html [13]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [1] [3] [9] [13]

## 15. EDC (2024)

- **Title:** Extract, Define, Canonicalize: An LLM-based Framework for Knowledge Graph Construction
- **Authors:** Bowen Zhang, Harold Soh (2 in total) [3]
- **Venue:** EMNLP 2024, from the arXiv comment [3].
- **First version:** 20240405 [3]
- **Link:** https://arxiv.org/abs/2404.03868
- **Citations:** 181, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Origin.* A three-phase pattern, open information extraction, then schema definition, then post-hoc canonicalization, so the schema need not sit in the prompt and can be induced when none exists [3].
  - *Widely built on.* 181 citations [1]; the archive records that the `clear-nus/edc` repository README cites the paper [12]; AutoSchemaKG cites EDC in its introduction [19].
- **Idea:** Avoid the context-window limit on large schemas by extracting first and aligning later, with an optional trained schema retriever ("EDC+R") [3]. First-party: on REBEL, partial F1 with GPT-4 0.601 against GenIE 0.385; on Wiki-NRE 0.713 against 0.484; on WebNLG (GPT-3.5-turbo) 0.794 against REGEN 0.767; human-rated precision on REBEL 0.867 against CESI's 0.504. The authors note automatic scores are pessimistic because reference annotations are incomplete [18].
- **Relations:**
  - *Answers* the limit stated for earlier LLM construction: "these methods are currently limited to small and domain-specific scenarios" [18].
  - *Evaluates against* GenIE, REGEN, CESI, ChatIE, CodeKGC [18].
  - *Built on by* AutoSchemaKG (#22): EDC appears in its introduction's citation list, not in a comparison [19].
  - *Cross-era:* open IE (the "Extract" phase) and schema canonicalization are pre-LLM tasks; CESI is a canonicalization baseline named in the paper (its year was not read) [18].
- **Read:** abstract [3] plus html extract (benchmarks, baselines, results) [18]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [1] [3] [12] [18] [19]

## 16. Text2KGBench (2023)

- **Title:** Text2KGBench: A Benchmark for Ontology-Driven Knowledge Graph Generation from Text
- **Authors:** Nandana Mihindukulasooriya, Sanju Tiwari, Carlos F. Enguix (4 in total) [3]
- **Venue:** ISWC 2023, Resources Track, from the arXiv comment [3].
- **First version:** 20230804 [3]
- **Link:** https://arxiv.org/abs/2308.02357
- **Citations:** 149, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Origin.* The first benchmark in this pool that scores ontology conformance and hallucination of LLM-generated KGs: Wikidata-TekGen (10 ontologies, 13,474 sentences) and DBpedia-WebNLG (19 ontologies, 4,860 sentences), seven metrics [3].
- **Idea:** Give a model an ontology and sentences; score fact extraction, conformance to concepts, relations, domain and range, and faithfulness. Baselines Vicuna-13B and Alpaca-LoRA-13B "show that there is room for improvement" [3].
- **Relations:**
  - *Links the semantic-web thread to the LLM era:* the task is defined over ontologies (Wikidata, DBpedia, both older KGs).
  - *Evaluates* LLMs of the 2023 generation (Vicuna-13B, Alpaca-LoRA-13B) [3].
  - *Not used by* EDC, which chose WebNLG, REBEL, Wiki-NRE [18].
  - The archive records "none in this run" for uses [20].
- **Read:** abstract [3]; read 20261102 20:04 UTC.
- **Sources:** [1] [3] [18] [20]

## 17. Language Models are Open Knowledge Graphs (2020)

- **Title:** Language Models are Open Knowledge Graphs
- **Authors:** Chenguang Wang, Xiao Liu, Dawn Song (3 in total) [3]
- **Venue:** none stated in the arXiv record [3]; venue from Semantic Scholar not read (see Citations)
- **First version:** 20201022 [3]
- **Link:** https://arxiv.org/abs/2010.11967
- **Citations:** unstated (not read: Semantic Scholar returned HTTP 429 on every try, see source 2). The paper is from 2020, so a count would be informative; none is asserted here.
- **Tests:**
  - *Origin.* Shows how to build KGs "from pre-trained language models (e.g., BERT, GPT-2/3), without human supervision", in "a single forward pass" with no fine-tuning, comparing the result with Wikidata and TAC KBP [3]. It is the earliest paper in this pool on LM-driven KG construction.
- **Idea:** Match-and-Map: a beam search over the model's attention weights produces candidate (head, relation, tail) facts (Match); facts are linked to an existing schema when possible and otherwise kept as an open schema (Map) [14]. First-party: best model MaMa-GPT-2XL scores 29.72 F1 on TAC KBP and 22.39 F1 on Wikidata against 16.77 F1 for Stanford OpenIE on Wikidata [14].
- **Relations:**
  - *Answers* the cloze-style fact recall of LAMA (Petroni et al.; outside the 2020 to 2026 window): "instead of conducting fact recall in cloze statements, MaMa directly generates the whole fact" [14].
  - *Evaluates against* the human-made KGs Wikidata and TAC KBP 2013 slot filling and the open-IE systems OpenIE 5.1 and Stanford OpenIE [14]. These are earlier-era systems.
  - *Precursor of* the LLM-prompting construction line (#12, #15): whether those papers cite it is unstated.
- **Read:** abstract [3] plus first 100,000 characters of ar5iv [14]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [1] [2] [3] [14]

## 18. RepoGraph (2024)

- **Title:** RepoGraph: Enhancing AI Software Engineering with Repository-level Code Graph
- **Authors:** Siru Ouyang, Wenhao Yu, Kaixin Ma (9 in total) [3]
- **Venue:** ICLR 2025, from the arXiv comment [3].
- **First version:** 20241003 [3]
- **Link:** https://arxiv.org/abs/2410.14684
- **Citations:** 149, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Origin.* A "plug-in module that manages a repository-level structure" for software-engineering agents; plugged into four methods of two kinds on SWE-bench it "substantially boosts the performance of all systems, leading to a new state-of-the-art among open-source frameworks" (as of the paper) [3].
  - *Widely built on.* 149 citations [1]; cited in Codebase-Memory's related work [21].
- **Idea:** Parse a repository into a graph of definitions and references, and give the agent sub-graphs around the lines relevant to an issue [3] (details beyond the abstract not read). First-party results.
- **Relations:**
  - *Parallel to* CodexGraph (#19, same year) and LocAgent (considered); Codebase-Memory says it "exposed code graphs to LLM agents via graph database interfaces" for CodexGraph and "boost[ed] existing agents on SWE-bench" for RepoGraph [21].
  - *Cross-era / cross-thread:* Aider's repository map (a blog post, 20231022; archive source) is the earlier tree-sitter graph-ranked map; Codebase-Memory cites it and says repo-map approaches "lack structural queries and persistence" [21] [12].
  - *Contrast:* Agentless (2407.01489, considered) reaches the highest open-source SWE-bench Lite score of its date without a graph ("without letting the LLM decide future actions or operate with complex tools") [3].
- **Read:** abstract [3]; read 20261102 19:57 UTC.
- **Sources:** [1] [3] [12] [21]

## 19. CodexGraph (2024)

- **Title:** CodexGraph: Bridging Large Language Models and Code Repositories via Code Graph Databases
- **Authors:** Xiangyan Liu, Bo Lan, Zhiyuan Hu (8 in total) [3]
- **Venue:** North American Chapter of the ACL, per Semantic Scholar [1]; the arXiv comment says "work in progress" [3].
- **First version:** 20240807 [3]
- **Link:** https://arxiv.org/abs/2408.03910
- **Citations:** 114, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Origin.* Puts a graph database and its query language between the agent and the repository: the LLM agent "construct[s] and execute[s] queries, allowing for precise, code structure-aware context retrieval and code navigation" [3]. It is the first paper in this pool that has a code agent write graph queries (compare Text2Cypher #20).
- **Idea:** Extract a repository into a unified-schema graph database and let the agent query it, instead of "similarity-based retrieval" (low recall in complex tasks) or "manual tools and APIs" (task-specific) [3]. Assessed on CrossCodeEval, SWE-bench, EvoCodeBench; first-party.
- **Relations:**
  - *Answers* similarity-based retrieval for code (abstract) [3].
  - *Applies* the text-to-graph-query idea of #20 to code (my reading; the abstract names the "graph query language", not Cypher).
  - *Cited by* Codebase-Memory [21].
  - *Contrast:* Codebase-Memory finds its graph agent scores 0.83 against 0.92 for a file-read and grep agent, at about ten times fewer tokens [21].
- **Read:** abstract [3]; read 20261102 19:57 UTC.
- **Sources:** [1] [3] [21]

## 20. Text2Cypher (2024)

- **Title:** Text2Cypher: Bridging Natural Language and Graph Databases
- **Authors:** Makbule Gulcin Ozsoy, Leila Messallem, Jon Besga (4 in total) [3]
- **Venue:** COLING workshops, per Semantic Scholar [1]; the arXiv record names none [3].
- **First version:** 20241213 [3]
- **Link:** https://arxiv.org/abs/2412.10064
- **Citations:** 73, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Origin.* Names natural-language-to-Cypher as a task with its own dataset: "combined, cleaned and organized several publicly available datasets into a total of 44,387 instances", scored with Google-BLEU and Exact Match; fine-tuned models improve over baselines [3]. First-party (Neo4j).
- **Idea:** LLMs "often struggle to capture complex nuances" in Cypher; fine-tuning on a curated dataset helps [3].
- **Relations:**
  - *Cross-era:* applies LLMs to Cypher (introduced with Neo4j 2.0 in 2013, per the archive primer) and sits beside Text2SQL and Text2SPARQL, which the listing of the follow-up 2506.21445 names as sibling tasks [25]; Neo4j's follow-ups are under Considered.
  - *Succeeded by* Text2GraphQuery-Bench (2602.11745, 267,276 pairs across languages, per the archive) [20].
  - *Used by:* "none in this run" per the archive [20].
- **Read:** abstract [3]; read 20261102 19:57 UTC.
- **Sources:** [1] [3] [20]

## 21. LLM-empowered KG construction: a survey (2025)

- **Title:** LLM-empowered knowledge graph construction: A survey
- **Authors:** Haonan Bian (1 in total) [3]
- **Venue:** none stated [3].
- **First version:** 20251023 [3]
- **Link:** https://arxiv.org/abs/2510.20345
- **Citations:** 51, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Survey of record (provisional).* Analyses "how LLMs reshape the classical three-layered pipeline of ontology engineering, knowledge extraction, and knowledge fusion", split into schema-based and schema-free paradigms [3]. It is the only dedicated LLM construction survey found in the searches done (alphaXiv listing, 20261102); its count (51 in about a year) and single authorship are modest, so "of record" is provisional.
- **Idea:** Shows construction moving "from rule-based and statistical pipelines to language-driven and generative frameworks", and names dynamic memory for agents as a direction [3].
- **Relations:**
  - *Maps* EDC (#15) and AutoSchemaKG (#22) to the schema-based and schema-free paradigms (my reading, not read in the text).
  - *Succeeds* the Roadmap (#3) for the construction family.
  - *Links* to agent memory by its own future-directions list ("dynamic knowledge memory for agentic systems") [3].
- **Read:** abstract [3]; read 20261102 19:57 UTC.
- **Sources:** [1] [3]

## 22. AutoSchemaKG (2025)

- **Title:** AutoSchemaKG: Autonomous Knowledge Graph Construction through Dynamic Schema Induction from Web-Scale Corpora
- **Authors:** Jiaxin Bai, Wei Fan, Qi Hu (20 in total) [3]
- **Venue:** Annual Meeting of the ACL, per Semantic Scholar [1]; the arXiv comment says "preprint" [3].
- **First version:** 20250529 [3]
- **Link:** https://arxiv.org/abs/2505.23628
- **Citations:** 38, Semantic Scholar [1], read 20261102 19:47 UTC.
- **Tests:**
  - *Origin (scale).* Builds KGs with induced schemas and no predefined ontology; over 50 million documents it constructs ATLAS, "900+ million nodes and 5.9 billion edges"; "92% semantic alignment with human-crafted schemas" [3]. Whether it is the first to induce schemas is not established; EDC (#15) already induces one on small corpora.
  - Count is 38, so the weaker end of "widely built on"; included for the scale result.
- **Idea:** Extract triples and induce a schema together, conceptualising entities and events into categories [3]. First-party: on MuSiQue, HotpotQA, 2Wiki (1,000 questions each) it is compared with HippoRAG, HippoRAG2, GraphRAG, LightRAG, MiniRAG, RAPTOR, BM25 and Contriever [19]. Stated cost: "78,400+ GPU hours" [19].
- **Relations:**
  - *Builds on / differs from* EDC (#15): EDC is only cited in the introduction, not compared [19].
  - *Evaluates against* graph-RAG systems (another researcher's area) [19].
  - *Linked to the survey* (#21) schema-free paradigm (my reading).
- **Read:** abstract [3] plus first 100,000 of 133,146 characters of html [19]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [1] [3] [19]

## 23. Naive RAG Is Stronger Than We Thought (2026)

- **Title:** Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought
- **Authors:** Zhengye Bao, Shengtao Zhang, Haokai Zhang (6 in total) [3]
- **Venue:** none stated [3].
- **First version:** 20261022 [3]
- **Link:** https://arxiv.org/abs/2610.30755
- **Citations:** 0, Semantic Scholar [1], read 20261102 19:47 UTC; too new to count.
- **Tests:**
  - *Turning point (independent evaluation).* "Raw-RAG ranks first among the compared memory systems in six of seven benchmark-model settings, outperforming the strongest compared agentic memory system by 0.13-5.53 points" on LoCoMo, LongMemEval, MEME and MemoryAgentBench [3]. Provisional: one week old; no one has yet built on or contradicted it in the sources read.
- **Idea:** Dense retrieval plus reranking over raw conversation history is a stronger baseline than twelve agentic memory systems (EverMemOS, MemOS, EMem, SimpleMem, MemU, MemMachine, Mem0, Memora, Nemori, MemoryOS, A-MEM, RecMem) [14]. Evidence: "higher coverage of necessary evidence can offset lower utilization" [3].
- **Relations:**
  - *Evaluates* Mem0 (#4) and A-MEM (#5); Zep and HippoRAG are cited only in related work, not compared [14].
  - *Answers* the claims of the first-party papers (#4, #5, #10) with a third-party harness.
  - *Agrees with* Memory Tax (#24), dated three days later.
  - **Caveat from the paper itself:** the abstract says 0.13-5.53 points, but in the main table the LongMemEval gap is 0.65 (93.70 against 93.05) and the LoCoMo gap 0.95 (89.07 against 88.12); the fetch-tool reading flags the table layout as ambiguous. Limits stated: offline conversation on public benchmarks, short histories, few models, LLM-judged coverage [14].
- **Read:** abstract [3] plus first 100,000 of 232,162 characters of html [14]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [1] [3] [14]

## 24. Memory Tax (2026)

- **Title:** Memory Tax: Dissecting the Net Value of Agent Memory
- **Authors:** Xuan He, Sining Zhoubian, Ruozhen Yang (11 in total) [3]
- **Venue:** none stated [3].
- **First version:** 20261025 [3]
- **Link:** https://arxiv.org/abs/2610.34073
- **Citations:** unstated (not read: Semantic Scholar returned HTTP 429 on every try, see source 2). Under eight months old, so a count would not be evidence for any test.
- **Tests:**
  - *Turning point (independent evaluation).* "Through a large-scale evaluation across multiple benchmarks and model backbones, we find many dedicated memory systems underperform naive RAG in many cases, indicating a negative net value" [3]. The paper adds a vocabulary (memory benefit, memory tax) for the per-query gains and losses against raw retrieval [3].
- **Idea:** Take RAG over raw history as the reference; a system's gains are "memory benefit", its losses "memory tax" (memory "may also remove or obscure evidence") [3]. Systems tested, by group: flat store A-MEM, SimpleMem, MemOS; hierarchical MemoryOS, LightMem, OpenViking; graph-based HippoRAG2, PlugMem, MAGMA; trained policies Mem-T, Memory-R2; run on Qwen3.5-4B, Qwen3.6-27B and a third backbone [16].
- **Relations:**
  - *Evaluates* A-MEM (#5), MemOS, and graph-based HippoRAG 2 (considered) against RAG [16]; cites Mem0, Zep, MemGPT in its references [16].
  - *Agrees with* #23 (three days earlier). Beware: a different paper, "MemoryTax: The Bitter Lesson of Agent Memory" (2610.29823, 20261021), has a near-identical name; only the listing was seen [22]. Do not conflate the two.
  - *Observation by the authors:* many memory designs compare mainly against other memories, so "naive RAG is often overlooked" [16].
- **Read:** abstract [3] plus the opening of the alphaXiv full text (introduction, baselines) [16]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [2] [3] [16] [22]

## 25. Are We Ready For An Agent-Native Memory System? (2026)

- **Title:** Are We Ready For An Agent-Native Memory System?
- **Authors:** Wei Zhou, Xuanhe Zhou, Shaokun Han (8 in total) [3]
- **Venue:** none stated [3].
- **First version:** 20260623 [3]
- **Link:** https://arxiv.org/abs/2606.24775
- **Citations:** unstated (not read: Semantic Scholar returned HTTP 429 on every try, see source 2). Under eight months old, so a count would not be evidence for any test.
- **Tests:**
  - *Turning point (independent evaluation).* "A systematic experimental study of agent memory from a data management perspective": four modules (representation and storage, extraction, retrieval and routing, maintenance); "12 representative memory systems and two reference baselines across five benchmark workloads spanning 11 datasets"; "no single architecture dominates across all scenarios" [3].
- **Idea:** Judge memory as a data system: cost, update correctness and long-horizon stability, not only end-task score [3]. From the fetch-tool reading of the text: Zep leads Knowledge Update (44.4 Substring EM) but "needs 155.1 s to exceed 84 utility"; on LoCoMo, Embedding RAG drops from 37.1 to 7.4 Answer F1 as the evidence gap widens; SimpleMem stays nearly flat on LongBench (35.2 to 34.9) [11]. Systems named: Mem0, MemoChat, Cognee, Zep, MemTree, Letta (MemGPT), LightMem, SimpleMem, MemOS, MemoryOS, A-MEM; the twelfth was not identified in the portion read [11].
- **Relations:**
  - *Evaluates* MemGPT/Letta (#2), Zep (#10), Mem0 (#4), A-MEM (#5) [11].
  - *Differs in conclusion from* #23: it finds no single winner among systems or baselines (for example Long Context has the best Exact Match on DB-Bench, and Embedding RAG degrades as the evidence gap widens) rather than a plain baseline on top [3] [11].
  - *Cross-era (databases thread):* frames agent memory as data management (storage, update, maintenance), echoing database-systems evaluation.
- **Read:** abstract [3] plus first 100,000 of 104,656 characters of html [11]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [2] [3] [11]

## 26. Is Grep All You Need? (2026)

- **Title:** Is Grep All You Need? How Agent Harnesses Reshape Agentic Search
- **Authors:** Sahil Sen, Akhil Kasturi, Elias Lumer (5 in total) [3]
- **Venue:** none stated [3].
- **First version:** 20260514 [3]
- **Link:** https://arxiv.org/abs/2605.15184
- **Citations:** unstated (not read: Semantic Scholar returned HTTP 429 on every try, see source 2). Under eight months old, so a count would not be evidence for any test.
- **Tests:**
  - *Turning point (independent evaluation, plain-file side).* Compares grep and vector retrieval inside agent harnesses on a 116-question LongMemEval sample: "grep generally yields higher accuracy than vector retrieval", but "overall scores still depend strongly on which harness and tool-calling style is used" [3].
- **Idea:** Under inline tool output, grep beat vector retrieval in every harness-model pair (for example Claude Opus 4.6 in the authors' Chronos harness 93.1 against 83.6; GPT-5.4 in Codex CLI 93.1 against 75.9); under file-based ("programmatic") delivery the order varies and vector leads in five of ten pairs [17]. Authors' stated limits: lexical tools may help more on conversation QA with verbatim spans; "we do not claim grep beats vector in general" [17]. Answers were graded by GPT-4o [17].
- **Relations:**
  - *Evaluates* the retrieval choice behind plain-file KBs against vector stores, on LongMemEval (#7) [17].
  - *Complements* Filesystem-based memory (#27) and the Naive-RAG result (#23): all three favour keeping raw material searchable.
  - *Contrast with* Codebase-Memory (#28), which argues a graph beats repeated file reading and grep for code exploration but scores lower (0.83 against 0.92) [21].
  - *Origin of the plain-file idea:* the LLM-wiki pattern comes from a gist (Karpathy, 20260404; archive source), not a paper; no foundational paper was found (see Considered) [12].
- **Read:** abstract [3] plus html extract (Table 1, limitations) [17]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [2] [3] [12] [17]

## 27. Filesystem-Based Memory for LLM Agents (2026)

- **Title:** Filesystem-Based Memory for LLM Agents: Organization, Evolution, and Sustainability
- **Authors:** Sizhe Zhou, Sheldon Yu, Hui Wei (11 in total) [3]
- **Venue:** none stated [3] (59 pages, per the arXiv comment).
- **First version:** 20260729 [3]
- **Link:** https://arxiv.org/abs/2607.26637
- **Citations:** unstated (not read: Semantic Scholar returned HTTP 429 on every try, see source 2). Under eight months old, so a count would not be evidence for any test.
- **Tests:**
  - *Origin (as a study).* Says "research has largely passed over this medium" and presents "the first systematic exploration of filesystem-based memory for LLM agents", a directory tree of markdown files that the agent reads and reorganises with generic file tools [3].
  - *Turning point (independent evaluation).* "What organization reliably buys is search economy: organized stores roughly halve retrieval cost where material is large", but "no agent we measure converts organization itself into better answers" and "organization erodes for all but the strongest management agent" [3].
- **Idea:** Three agent roles (management, search, execution) around one memory filesystem. Compared shapes: closed-book, BM25 chunk retrieval, verbatim dump, foldered sessions, reorganised store, agent-curated store, on LoCoMo, PersonaMem, REALTALK and ALFWorld. Example: on PersonaMem 32k the agent-curated store scored 37.5% against 78.1% for the verbatim dump; on LoCoMo it scored 86.1% [23]. Limits stated: single build draws, one 42-question conversation for the model ladder, judge re-runs moving scores by about 1.3 points on LoCoMo [23].
- **Relations:**
  - *Evaluates* the "markdown files as memory" default that the archive links to Anthropic's memory tool and the LLM-wiki wave [12].
  - *Agrees with* #23, #24 and #26 that raw material beats elaborate reorganisation on these benchmarks.
  - *Cross-era:* a file hierarchy as knowledge store returns to the pre-database, pre-graph form; not discussed in the pages read.
- **Read:** abstract [3] plus first 100,000 of 207,535 characters of html [23]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [2] [3] [12] [23]

## 28. Codebase-Memory (2026)

- **Title:** Codebase-Memory: Tree-Sitter-Based Knowledge Graphs for LLM Code Exploration via MCP
- **Authors:** Martin Vogel, Falk Meyer-Eschenbach, Severin Kohler (5 in total) [3]
- **Venue:** none stated; the arXiv comment says "preprint" [3].
- **First version:** 20260328 [3]
- **Link:** https://arxiv.org/abs/2603.27277
- **Citations:** unstated (not read: Semantic Scholar returned HTTP 429 on every try, see source 2). Under eight months old, so a count would not be evidence for any test.
- **Tests:**
  - *Origin (measured).* The only paper in this pool that measures a code knowledge graph served over MCP against a plain file-exploration agent: "83% answer quality versus 92% for a file-exploration agent, at ten times fewer tokens and 2.1 times fewer tool calls" over 31 repositories, 66 languages [3].
  - Passes no other test; included because the archive flags "does a code graph beat grep?" as open question 5 and this is the only measurement found [12].
- **Idea:** A persistent tree-sitter graph (no LLM extraction) with call-graph traversal, impact analysis and community discovery, exposed through 14 MCP tools [21]. First-party. Reported limits: one LLM backend (Claude Opus 4.6), one repository per language, the first author graded responses, the graph holds structure not source lines [21].
- **Relations:**
  - *Builds on / cites* RepoGraph (#18), CodexGraph (#19), LocAgent (considered), Aider's repo map [21].
  - *Evaluates against* the file-reading plus grep Explorer agent; the contrast with Is-Grep-All-You-Need (#26) is one of method: here the plain tool scores higher on answer quality, there it scores higher on accuracy [21] [17].
  - *Cross-era:* tree-sitter parsing and call graphs are program-analysis staples; no link is drawn in the pages read.
- **Read:** abstract [3] plus html extract (related work, benchmark, limits) [21]; read 20261102, between 19:57 and 20:04 UTC.
- **Sources:** [2] [3] [12] [21]

---

## Considered and not proposed

| Paper | Count / read | Why not |
|---|---|---|
| MemOS, 2507.03724 | 153 [1] | Fails origin: its OS framing follows MemGPT (#2); no evidence yet of others building on MemCube. A baseline in #23, #24, #25. Revisit if citations grow. |
| Hindsight, 2512.12818 | unstated (429) | First-party; its baseline numbers are taken from other vendors' reports and "could not be independently reproduced" [15]. Not an origin the other papers name. |
| SimpleMem, 2601.02553 | unstated (429) | Compression, not a graph; a baseline in #23 to #25 but no test passed on the evidence read. |
| From Human Memory to AI Memory (survey), 2504.15965 | 140 [1] | A second survey beside #8 and #13; adds a three-dimension, eight-quadrant categorisation; not the one others use to map the area (unstated). |
| Graph-based Agent Memory survey, 2602.05665 | 26 [1] | Survey of record for the graph slice only; nine months old, count too low. Natural pick if the owner wants a graph-memory survey. |
| Harness the Memory, 2608.15008 | 4 [1] | Independent and useful ("no single substrate consistently dominates"), but overlaps #25 and #23; too new. |
| Memory-related reasoning: Reflexion 2303.11366; Agent Workflow Memory 2409.07429; MIRIX 2507.07957; Think-in-Memory 2311.08719; MemoryOS 2506.06326 | counts unstated (429) | Agent-memory neighbours; not dependencies of the chosen papers except MemoryOS, a baseline in #14 and #23. Add if the owner widens the memory group. |
| HippoRAG 2 (From RAG to Memory), 2502.14802 | 284 [1] | Strong, but sits in the graph-RAG area (another researcher). Relation: it renames the shift "from RAG to memory" and is a graph baseline in #24. |
| Think-on-Graph 2307.07697 (373); Reasoning on Graphs 2310.01061 (591) | [1] | KG-augmented LLM reasoning, graph-RAG researcher's area; they are the "KG-enhanced LLMs" family of the Roadmap (#3). |
| LLMs on Graphs survey, 2312.02783 | 376 [1] | About LLMs with graphs in general (including non-KG graphs); too broad for a KB/KG chapter. |
| LLMs and KGs: Opportunities and Challenges, 2308.06374 | 170 [1] | 16-author position paper (TGDK); overlaps the Roadmap's role. |
| KGGen, 2502.09956 | 92 [1] | Introduces MINE, a construction benchmark and a clustering step; NeurIPS; not named by other chosen papers. A reasonable swap for AutoSchemaKG. |
| Are LLMs Effective KG Constructors?, 2510.11297 | 1 [1] | Independent evaluation of zero-shot construction; too new to count. |
| LocAgent, 2503.09089 | 141 [1] | Code localisation with graph-guided agents (92.7% file-level accuracy, abstract); comparable to #18 and #19; dropped only to keep the pool within 30. |
| Agentless 2407.01489; SWE-agent 2405.15793 | unstated (429) | Plain-tool baselines for code, not KG papers; cited here as contrast in #18. |
| LLM-assisted KG Engineering: Experiments with ChatGPT, 2307.06917 | 105 [1] | Early (July 2023) ChatGPT experiments for KG engineering, a workshop-level report; the only early text-to-SPARQL-adjacent item, but no test clearly passed. |
| Spider4SPARQL 2309.16248; LLM-based SPARQL over federated KGs 2410.06062; Leveraging LLMs in Scholarly KGQA 2311.09841 | unstated (429) | Text-to-SPARQL: **no fundamental paper identified.** Candidates are benchmark or system papers with modest counts; the TEXT2SPARQL 2026 challenge entry 2610.13648 is 20261009 and unscored. A gap to report, not to fill from memory. |
| Text2Cypher Across Languages 2506.21445 (3); Text2GraphQuery-Bench 2602.11745 (2); Neo4j follow-ups 2505.05118, 2505.05122 | [1] | Follow-ups; too new or too small. |
| MemoryAgentBench, 2507.05257 | 298 [1] | A benchmark with real use (4 competencies, used by #23); belongs to the benchmarks chapter. |
| Context engineering survey, 2507.13334 | unstated (429) | Covers memory only as one part of context engineering; abstract claims analysis of over 1400 papers [3]. Not specific to KBs. |
| Single-Round Vector RAG vs an LLM-Compiled Wiki, 2605.18490; Progressive Disclosure for LLM-Maintained Wiki KBs, 2607.04576 | [3] | The only wiki-pattern studies found (13 questions over 24 papers; one 709-page wiki); one author each; their own limits: judges disagree, results depend on baseline, scorer and judge. Not strong enough. **No foundational paper on the plain-file LLM wiki exists in the sources read**; its origin is a gist (archive) [12]. |
| Other 2026 text-to-SPARQL / Cypher systems (SAGA, GRASP 2507.08107, SPARQL-LLM 2512.14277, PIPE-Cypher, KG2Cypher, CypherTurn) | listings only [20] | New system papers; no test passed. |
| Aider repository map (blog, 20231022); Karpathy LLM Wiki (gist, 20260404); Anthropic memory tool (blog, 20250929) | archive [12] | Not papers. Standards and posts belong to the projects or trends chapters. |

## Gaps and cautions for the writer

1. **Counts are not comparable across ages.** A 2023 paper has had three years to collect citations; the 2026 entries (#23 to #28) are admitted on the *turning point* or *origin* test only, and all are less than eight months old.
2. **Independent evidence is thin and recent.** The "plain retrieval matches memory systems" result (#23, #24, #25) comes from three studies between 20260623 and 20261025, two of them three days apart (20261022 and 20261025); they use overlapping benchmarks (LoCoMo, LongMemEval), and #23's abstract and main table disagree on the gap size.
3. **First-party results dominate** the older memory papers (#2, #4, #5, #10, #11, #14): each reports its own wins. The Zep versus Mem0 LoCoMo scores disagree (65.99 [9] against 75.14 [15]).
4. **Text-to-SPARQL has no fundamental paper in this pool;** Text2Cypher (#20) is the only query-generation entry.
5. **Plain-file KB:** the pattern has no founding paper; the evidence is #26 and #27 (and the single-author wiki studies in Considered).
6. **Not read in full.** Every entry rests on the abstract and, for most, one fetch-tool extract of the paper's HTML. No full-text read was done; relations marked "unstated" were not found in the part read.
7. **Similarly named papers:** "Memory Tax" (2610.34073) and "MemoryTax: The Bitter Lesson of Agent Memory" (2610.29823); two "GraphRAG-Bench" papers (archive).

## Sources

All reads on 20261102 (UTC).

1. Semantic Scholar Graph API, POST `https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,year,venue,citationCount,publicationDate,externalIds,authors`, 40 arXiv ids (batch 1). Counts and venues for #1 to #22 as marked. Read 20261102 19:47 UTC.
2. Semantic Scholar Graph API, same endpoint, batch 2 (ids listed in the working notes). Not obtained: the call returned HTTP 429 on all 8 tries (19:50 to 20:10 UTC), and two later retries (a 13-id batch and one-by-one GETs, 20:10 to 20:37 UTC) also returned 429. No count in this file comes from this source. OpenAlex also returned HTTP 429 with a Retry-After of 14167 seconds (read about 20:00 UTC), so it was not used.
3. arXiv API records (titles, authors, v1 dates, journal references, comments, abstracts): `http://export.arxiv.org/api/query?id_list=...`. Read 20261102 19:57 UTC (first batch) and 20:04 UTC (second batch).
4. MemGPT, html: https://arxiv.org/html/2310.08560 : virtual context management, main/external context, DMR task and table, citation of Park et al. (read 20261102, between 19:57 and 20:04 UTC).
5. Zep, html: https://arxiv.org/html/2501.13956 : MemGPT/DMR 93.4%, bi-temporal model, LongMemEval Table 2, DMR limitation (same window).
6. Generative Agents, ar5iv: https://ar5iv.labs.arxiv.org/html/2304.03442 : memory stream, retrieval score, reflection, TrueSkill ablation (same window; first 100,000 of 144,380 characters).
7. CoALA, html: https://arxiv.org/html/2309.02427 : memory modules, Generative Agents cited (same window; first 100,000 of 151,098 characters).
8. A-MEM, html: https://arxiv.org/html/2502.12110 : baselines, benchmarks, relation to Mem0 and graph databases, limitations (same window).
9. Mem0, html: https://arxiv.org/html/2504.19413 : baselines, Table 2 scores, Zep footprint and latency claims (same window). 
10. Archive page `kb-kg/llm-era/README.md` (rows on Letta, Graphiti, `getzep/zep`), originally read 20261030 18:59 to 19:03 UTC; read again in this run, 20261102 between 19:45 and 20:00 UTC.
11. Agent-native memory study, html: https://arxiv.org/html/2606.24775 : systems, workloads and findings (same window; first 100,000 of 104,656 characters).
12. Archive pages `kb-kg/llm-era/README.md`, `kb-kg/papers-benchmarks/README.md`, read in this run (leads; their own source read times are 20261030 18:58 to 19:04 UTC).
13. Memory-R1, html: https://arxiv.org/html/2508.19828 : baselines, headline numbers, Table 1 caveat (same window; first 100,000 of 103,525 characters).
14. Naive-RAG study, html: https://arxiv.org/html/2610.30755 : compared systems, main-table scores, limitations (same window; first 100,000 of 232,162 characters).
15. Hindsight, html: https://arxiv.org/html/2512.12818 : LoCoMo and LongMemEval tables, provenance of baseline numbers (same window; first 100,000 of 121,061 characters).
16. Memory Tax, alphaXiv extracted text of https://arxiv.org/abs/2610.34073 : introduction and baselines (same window).
17. Is Grep All You Need?, html: https://arxiv.org/html/2605.15184 : Table 1, models, limitations (same window).
18. EDC, html: https://arxiv.org/html/2404.03868 : benchmarks, baselines, results, positioning (same window).
19. AutoSchemaKG, html: https://arxiv.org/html/2505.23628 : related work, QA baselines, ATLAS size, limits (same window; first 100,000 of 133,146 characters).
20. Archive page `kb-kg/papers-benchmarks/README.md` sections 2.5, 4.4 (query-generation and construction rows).
21. Codebase-Memory, html: https://arxiv.org/html/2603.27277 : related work, benchmark, results, limitations (same window).
22. alphaXiv discovery listing (titles, dates, first lines): https://www.alphaxiv.org/abs/2610.29823 and others; a lead, not a source of facts (read 20261102, between 19:50 and 20:10 UTC).
23. Filesystem-based memory, html: https://arxiv.org/html/2607.26637 : benchmarks, shapes, findings, limitations (same window; first 100,000 of 207,535 characters).
24. alphaXiv AI-generated report of Mem0 (2504.19413), via the alphaXiv paper-content tool: used only as a lead for the update operations and the Neo4j graph; not a primary source (read 20261102, between 19:57 and 20:04 UTC).
25. alphaXiv discovery listing for Neo4j's Text2Cypher follow-ups (2506.21445 first line names "Text2SQL, Text2SPARQL, and Text2Cypher"): a lead (read 20261102, between 19:50 and 20:10 UTC).
