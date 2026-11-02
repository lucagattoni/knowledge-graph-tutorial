---
type: papers
group: agent-memory
order: 8
updated: 20261102 23:19 UTC
---

# Papers: Agent memory

This page holds the papers a reader needs to follow [agent memory](../index/agent-memory.md): systems that keep what an agent learned across sessions. It has eight fundamental papers, from three of 2023 to a survey of December 2025, then a further-reading list. The Naive RAG study of October 2026, listed in the first edition, is in the further reading: it was 11 days old at the read, has no citation, and no paper read builds on it. This page applies no citation threshold: each paper passes on a count with its source and read time, or on the later papers that use it. The line of work is told on [the trend page](../trends/agent-memory.md). The designs below start with arXiv papers of 2023; the sources read name no blog post or gist as the origin.

## Generative Agents (2023)

*Generative Agents: Interactive Simulacra of Human Behavior.* Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai (6 authors in total). ACM UIST 2023 [3]. First version 20230407 [1]. [arXiv 2304.03442](https://arxiv.org/abs/2304.03442).

**Why fundamental:** Widely built on; no origin is claimed. 6,297 citations (Semantic Scholar, read 20261102 19:47 UTC) [24]. MemGPT cites it in related work [7], CoALA casts it into its framework [5], and both memory surveys of this group tabulate or cite it [10][21]. The abstract describes an architecture that stores "a complete record of the agent's experiences using natural language", turns it into "higher-level reflections" and retrieves it to plan [1]; the full text calls the record the memory stream and scores retrieval as a weighted sum of recency, relevance and importance [2]. It is the earliest paper on this page by date; whether an earlier design did the same was not established.

**Idea:** An agent writes every observation to a list of timestamped text records, retrieves records by recency, relevance and importance, and from time to time has the model write reflections that go back into the same list [2]. In a sandbox of 25 agents the full architecture scored 29.89 on a TrueSkill believability scale, against 26.88 without reflection and 22.95 for human crowdworkers (first-party) [2]. *Reading:* the memory is a flat list built to make simulated people believable, not to answer questions about a user.

**Relations:** None.

**Read:** abstract page and targeted passages of the ar5iv text (memory stream, retrieval score, ablation); not read end to end. Read 20261102 20:41 to 20:45 UTC [1][2].

## CoALA (2023)

*Cognitive Architectures for Language Agents.* Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan (4 authors in total). TMLR, per the arXiv comment on version 3 [4]. First version 20230905 [4]. [arXiv 2309.02427](https://arxiv.org/abs/2309.02427).

**Why fundamental:** Widely built on, by citation count. The paper proposes a memory taxonomy for language agents taken from [cognitive architectures](../index/cognitive-architecture.md) such as Soar: a working memory and three long-term memories, episodic, semantic and procedural [5]. It uses the framework "to retrospectively survey and organize a large body of recent work" [4]. The only evidence of use is its 575 citations (Semantic Scholar, read 20261102 19:47 UTC) [24]. The page does not claim that anyone adopted its vocabulary: the two memory surveys of this group (Zhang 2024, Hu 2025) do not cite it, and searching their texts for its first author and its title found nothing [10][21].

**Idea:** A language agent has memory modules, an action space (internal actions such as reasoning, retrieval and learning; external actions that act on an environment) and a decision cycle. Working memory "maintains active and readily available information as symbolic variables for the current decision cycle" [5]. A table places ReAct, Voyager, Generative Agents and others in this frame [5]. It casts [Generative Agents (2023)](./agent-memory.md) as an agent with episodic and semantic memory, places [ReAct (2022)](./agentic-search.md) in the same table as an agent with no episodic or semantic memory, and cites [Lewis et al. (2020)](./foundations.md) for retrieval-augmented methods under semantic memory [5].

**Relations:** Builds on: [Lewis et al. (2020)](./foundations.md), [ReAct (2022)](./agentic-search.md), [Generative Agents (2023)](./agent-memory.md).

**Read:** abstract page and targeted passages of the arXiv HTML text (memory modules, Soar, Table 2); not read end to end. Read 20261102 20:42 to 20:43 UTC; the abstract quote re-read 21:00 UTC [4][5].

## MemGPT (2023)

*MemGPT: Towards LLMs as Operating Systems.* Charles Packer, Sarah Wooders, Kevin Lin (7 authors in total). No venue in the arXiv record [6]. First version 20231012 [6]. [arXiv 2310.08560](https://arxiv.org/abs/2310.08560).

**Why fundamental:** Widely built on; no origin is claimed. 1,753 citations (Semantic Scholar, read 20261102 19:47 UTC) [24]. The A-MEM and Mem0 papers use it as a baseline [16][18], the Zep paper reports against its DMR task [13], and the 2025 survey calls it an operating-system metaphor "inspiring subsequent works" [21]. It proposes "virtual context management", with a main context analogous to RAM and an external context analogous to disk, and it introduces the Deep Memory Retrieval (DMR) task [6][7]. The project that continues it is Letta, "f.k.a. MemGPT" [8]; see [Letta](../projects/letta.md).

**Idea:** Treat the [context window](../index/context-window.md) of a [large language model](../index/large-language-model.md) as fast memory and move data to and from slower external storage, with the model itself issuing the moves. On DMR, GPT-4 Turbo with MemGPT reached 93.4% accuracy, against 35.3% for the fixed-context baseline (first-party) [7]. Its related work cites Generative Agents as work that proposes "adding memory to LLMs and using the LLM as a planner" [7]. Its external memory "builds upon much prior work" on external retrievers, and the paper cites [Lewis et al. (2020)](./foundations.md), [Karpukhin et al. (2020)](./foundations.md) and [Guu et al. (2020)](./foundations.md) for it [7].

**Relations:** Builds on: [Guu et al. (2020)](./foundations.md), [Karpukhin et al. (2020)](./foundations.md), [Lewis et al. (2020)](./foundations.md).

**Read:** abstract page and targeted passages of the arXiv HTML text (design, DMR table, related work); not read end to end. Read 20261102 20:42 to 20:43 UTC [6][7].

## Memory mechanism survey (2024)

*A Survey on the Memory Mechanism of Large Language Model based Agents.* Zeyu Zhang, Xiaohe Bo, Chen Ma (9 authors in total). ACM Transactions on Information Systems 43(6), 2025, DOI 10.1145/3748302; the journal lists the first authors as Zhang, Dai, Bo [11]. First version 20240421 [9]. [arXiv 2404.13501](https://arxiv.org/abs/2404.13501).

**Why fundamental:** survey of record. The abstract says earlier memory mechanisms "are scattered in different papers" and that no systematic review existed; it covers what memory is, why agents need it, how to design and evaluate it, and applications [9]. The 2025 survey names it, with one other, among recent surveys of agent memory [21]. It has 889 citations (Semantic Scholar, read 20261102 19:47 UTC) [24].

**Idea:** The text sorts the field by memory source (inside-trial, cross-trial, external knowledge), by form (textual or parametric) and by operation (writing, management, reading), then reviews evaluation and applications [10]. *Reading:* it is the map of the 2023 and early 2024 designs; it predates Zep, A-MEM and Mem0, so it cannot say how graph and note-based memories compare. It tabulates and describes [Generative Agents (2023)](./agent-memory.md) (similarity, time interval and importance for reading; reflection for processing) and describes [MemGPT (2023)](./agent-memory.md) as a working context holding recent history inside virtual context management [10].

**Relations:** Builds on: [Generative Agents (2023)](./agent-memory.md), [MemGPT (2023)](./agent-memory.md).

**Read:** abstract page and targeted passages of the arXiv HTML text (tables of sources and forms); not read end to end. Read 20261102 20:42 to 20:43 UTC; venue from the Crossref record, read 20:48 UTC [9][10][11].

## Zep (2025)

*Zep: A Temporal Knowledge Graph Architecture for Agent Memory.* Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais (5 authors in total). No venue in the arXiv record [12]. First version 20250120 [12]. [arXiv 2501.13956](https://arxiv.org/abs/2501.13956).

**Why fundamental:** Widely built on, with a narrow origin claim. 456 citations (Semantic Scholar, read 20261102 19:47 UTC) [24]. The Mem0 paper compares against it [18], the 2025 survey lists it among graph-based memory practices [21], and the [Graphiti](../projects/graphiti.md) README links the paper [14]. The 2026 Naive RAG study (further reading) does not run it: Zep is not among that study's twelve baselines, and its scores in the appendix tables are copied from other papers [23]. The paper introduces Graphiti, "a temporally-aware knowledge graph engine", and states that "Zep implements a bi-temporal model" [12][13]; see [bi-temporal model](../index/bi-temporal-model.md) and [temporal knowledge graph](../index/temporal-knowledge-graph.md). The novelty claim is the authors'. An arXiv search made for this page (records before 20250120; source 32) found earlier temporal graph memory built for other uses: "Temporal Knowledge-Graph Memory in a Partially Observable Environment" (20240811) and "Bitemporal Property Graphs to Organize Evolving Systems" (20211126), seen by title. As far as the titles show, neither is a memory for conversation agents, so the claim is narrowed to a bi-temporal graph engine for the memory of language-model agents.

**Idea:** Conversations and business data become a graph of episodes, entities, facts and communities. Each fact carries four timestamps, two for when it was true and two for when the system recorded or expired it, and a changed fact is invalidated, not deleted [13]. On DMR it scored 94.8% against 93.4% for MemGPT, but a full-conversation baseline scored 94.4% and each conversation has only 60 messages; on [LongMemEval](../datasets/longmemeval.md), gpt-4o-mini scored 63.8% in 3.20 s against 55.4% in 31.3 s for full context (first-party) [13]. Its community nodes and summaries follow [GraphRAG (2024)](./graph-based-rag.md), with label propagation instead of the Leiden algorithm [13]. It answers [MemGPT (2023)](./agent-memory.md) on MemGPT's own DMR task [12][13]. It is scored on the [LongMemEval benchmark](../benchmarks/longmemeval.md) [13].

**Relations:** Builds on: [GraphRAG (2024)](./graph-based-rag.md). Answers: [MemGPT (2023)](./agent-memory.md).

**Read:** abstract page and targeted passages of the arXiv HTML text (bi-temporal model, Tables 1 and 2, DMR limits); not read end to end. Read 20261102 20:42 to 20:43 UTC; the README read 20:47 UTC [12][13][14].

## A-MEM (2025)

*A-MEM: Agentic Memory for LLM Agents.* Wujiang Xu, Zujie Liang, Kai Mei (6 authors in total). NeurIPS 2025, per the arXiv comment [15]. First version 20250217; latest version 20251008 [15]. [arXiv 2502.12110](https://arxiv.org/abs/2502.12110).

**Why fundamental:** Widely built on; no origin is claimed. 1,332 citations (Semantic Scholar, read 20261102 19:47 UTC) [24]; the Mem0 paper reports it as a baseline [18], and the 2026 Naive RAG study (further reading) lists it among its twelve baselines, with scores taken from a published paper in the table read [23]. It builds memory on the Zettelkasten method. Each new memory becomes a note with context, keywords and tags, linked to related notes, and new notes can "trigger updates" to old ones [15].

**Idea:** Let the model organise memory instead of following fixed insert and retrieve steps: write a structured note, link it to neighbours, and let new notes revise older ones [15]. First-party results on [LoCoMo](../datasets/locomo.md) and DialSim against LoCoMo's own baseline, ReadAgent, MemoryBank and MemGPT; the authors report no error bars, because repeated calls to the model API cost too much [16]. In the Mem0 paper's own run with an LLM judge, A-Mem scores 48.38 overall against 66.88 for Mem0; the setups differ [18]. It answers the graph-database memory of the [Mem0](../projects/mem0.md) project, whose "reliance on predefined schemas and relationships fundamentally limits their adaptability"; the current version cites the project's repository of 2024, not the Mem0 paper of April 2025 [16]. It runs [MemGPT (2023)](./agent-memory.md) as a baseline, with its own system, on the [LoCoMo benchmark](../benchmarks/locomo.md) [16].

**Relations:** Answers: also: Mem0 project (repository of 2024). Evaluates: [MemGPT (2023)](./agent-memory.md).

**Read:** abstract page and targeted passages of the arXiv HTML text (related work, baselines, checklist); not read end to end. Read 20261102 20:42 to 20:43 UTC [15][16].

## Mem0 (2025)

*Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory.* Prateek Chhikara, Dev Khant, Saket Aryan (5 authors in total). ECAI 2025, DOI 10.3233/FAIA251160 [19]. First version 20250428 [17]. [arXiv 2504.19413](https://arxiv.org/abs/2504.19413).

**Why fundamental:** Widely built on; no origin is claimed. 862 citations (Semantic Scholar, read 20261102 19:47 UTC) [24]; a named baseline in the 2026 Naive RAG study (further reading), which lists a configuration for it among the systems it ran [23]. The authors give an affiliation at mem0.ai and point to mem0.ai/research for code [18]; for the project, see [Mem0](../projects/mem0.md). The abstract introduces Mem0 and "an enhanced variant", Mem0g, that uses graph memory [17]; the novelty claim is the authors'.

**Idea:** Extract salient facts from each exchange, compare them with stored facts by [embedding](../index/embedding.md) similarity, and let the model choose ADD, UPDATE, DELETE or NOOP; Mem0g keeps entities and relations in a Neo4j graph and marks outdated relations invalid [18]. On LoCoMo with an [LLM judge](../index/llm-as-judge.md) it scores Mem0 66.88, Mem0g 68.44, Zep 65.99 and full context 72.90, at a p95 latency 91% lower than full context (first-party) [17][18]. Scores of one system differ between papers: Zep reads 65.99 in the Mem0 paper [18] and 81.06 in Table 11 of the Naive RAG study, which copies it from the EverMemOS paper's run; that table uses Qwen3 embedding and reranker models, while the Mem0 paper used an OpenAI embedding model, text-embedding-small-3 [18][23]. The Naive RAG study's own Table 12 repeats the Mem0 paper's 65.99 [23]. It runs [Zep (2025)](./agent-memory.md), [A-MEM (2025)](./agent-memory.md) and [MemGPT (2023)](./agent-memory.md) as baselines, with its own system, on the [LoCoMo benchmark](../benchmarks/locomo.md) [18].

**Relations:** Evaluates: [MemGPT (2023)](./agent-memory.md), [Zep (2025)](./agent-memory.md), [A-MEM (2025)](./agent-memory.md).

**Read:** abstract page and targeted passages of the arXiv HTML text (baselines, operations, Table 2, token footprint); not read end to end. Read 20261102 20:42 to 20:43 UTC and again 20:59 to 21:01 UTC (abstract, embedding model); venue from the Crossref record, read 20:48 UTC [17][18][19].

## Memory in the Age of AI Agents (2025)

*Memory in the Age of AI Agents.* Yuyang Hu, Shichun Liu, Yanwei Yue (47 authors in total). No venue in the arXiv record [20]. First version 20251215; second version 20260113 [20]. [arXiv 2512.13564](https://arxiv.org/abs/2512.13564).

**Why fundamental:** survey of record. The abstract separates agent memory from LLM memory, [retrieval-augmented generation](../index/retrieval-augmented-generation.md) and context engineering, organises it by forms, functions and dynamics, and compiles memory benchmarks and open-source frameworks [20]. It has 314 citations (Semantic Scholar, read 20261102 19:47 UTC); it is under a year old [24].

**Idea:** Three forms (token-level, parametric, latent), three functions (factual, experiential, working memory) and three dynamics (how memory is formed, evolved and retrieved) [20]. The authors say earlier taxonomies such as long-term against short-term memory "have proven insufficient" [20]. It names [Memory mechanism survey (2024)](./agent-memory.md) among recent surveys whose taxonomies "were developed prior to a number of rapid methodological advances" [21]. It calls [MemGPT (2023)](./agent-memory.md) an operating-system metaphor that inspired later work, and lists [Zep (2025)](./agent-memory.md), [A-MEM (2025)](./agent-memory.md) and [Mem0 (2025)](./agent-memory.md) as graph-based memory practices (Mem0g for the last) [21].

**Relations:** Builds on: [MemGPT (2023)](./agent-memory.md), [Zep (2025)](./agent-memory.md), [A-MEM (2025)](./agent-memory.md), [Mem0 (2025)](./agent-memory.md). Answers: [Memory mechanism survey (2024)](./agent-memory.md).

**Read:** abstract page and targeted passages of the arXiv HTML text (scope, surveys, graph memory, tables of systems); not read end to end. Read 20261102 20:42 to 20:44 UTC [20][21].

## Further reading

- MemoryBank (2023), [arXiv 2305.10250](https://arxiv.org/abs/2305.10250): memory updating "inspired by the Ebbinghaus Forgetting Curve theory"; a baseline in the A-MEM and Mem0 papers [16][18][25].
- MemOS (2025), [arXiv 2507.03724](https://arxiv.org/abs/2507.03724): "A Memory OS for AI System", which calls RAG "a stateless workaround"; one of the twelve systems in the Naive RAG study; 153 citations (Semantic Scholar, read 20261102 19:47 UTC) [23][24][26].
- Hindsight (2025), [arXiv 2512.12818](https://arxiv.org/abs/2512.12818): four logical networks (world facts, experiences, entity summaries, beliefs) and the operations retain, recall and reflect; first-party scores of 91.4% on LongMemEval and 89.61% on LoCoMo with a scaled backbone [27].
- Naive RAG Is Stronger (2026), [arXiv 2610.30755](https://arxiv.org/abs/2610.30755): "Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought", Zhengye Bao, Shengtao Zhang, Haokai Zhang and 3 others (6 authors in total); first version 20261022. The two titles in the catalogue are halves of one title: the arXiv record and the HTML page show only the long form, in a single version [22][23]. A plain baseline, Raw-RAG (dense retrieval and reranking over raw history), "ranks first among the compared memory systems in six of seven benchmark-model settings", by 0.13 to 5.53 points, against twelve memory systems, among them Mem0 and A-MEM; Zep is not one of them, and some baseline scores are copied from other papers (Table 10 text, from Dai et al.) [22][23]. Raw history covers more of the evidence a question needs, which can offset how little of it the reader uses [22]; the authors limit the claim to offline conversation on public benchmarks [23]. Scored on [LoCoMo](../benchmarks/locomo.md), [LongMemEval](../benchmarks/longmemeval.md) and [MemoryAgentBench](../benchmarks/memoryagentbench.md), and MEME. 0 citations (Semantic Scholar, read 20261102 19:47 UTC) at 11 days old [24]. Moved from the fundamental list: it cites [Mem0](./agent-memory.md) and A-MEM as baselines and [RAG (Lewis et al., 2020)](./foundations.md) for its baseline, but no paper read builds on it or cites it; Memory Tax, three days later, finds the same direction and does not cite it [28][33].
- Memory Tax (2026), [arXiv 2610.34073](https://arxiv.org/abs/2610.34073): finds "many dedicated memory systems underperform naive RAG in many cases", the same direction as the Naive RAG study, three days later, 20261025 [28]. Not the one-author [MemoryTax: The Bitter Lesson of Agent Memory](https://arxiv.org/abs/2610.29823), which uses one LoCoMo conversation [31].
- Agent-native memory study (2026), [arXiv 2606.24775](https://arxiv.org/abs/2606.24775): "Are We Ready For An Agent-Native Memory System?"; 12 memory systems and two baselines on five workloads over 11 datasets, finding that "no single architecture dominates" [29].
- Bi-Temporal Memory Engine (2026), [arXiv 2606.09900](https://arxiv.org/abs/2606.09900): one author; Engram, an open-source engine on a bi-temporal data model with no model call on its write path; first-party [30].

## Sources

All reads on 20261102 (UTC). Reads of the arXiv HTML pages were targeted passages, not end-to-end readings. Citation counts are Semantic Scholar's, carried over from the papers research of the same day and never compared with counts from another source (item 24).

1. https://arxiv.org/abs/2304.03442 : Generative Agents title, authors, first version, abstract (read 20261102 20:41 UTC)
2. https://ar5iv.labs.arxiv.org/html/2304.03442 : memory stream, retrieval score, ablation scores (read 20261102 20:45 UTC)
3. https://api.crossref.org/works/10.1145/3586183.3606763 : Generative Agents at ACM UIST 2023 (read 20261102 20:48 UTC)
4. https://arxiv.org/abs/2309.02427 : CoALA title, authors, first version, TMLR comment, abstract (read 20261102 20:42 UTC, abstract quote re-read 21:00 UTC)
5. https://arxiv.org/html/2309.02427 : memory modules, Soar, working-memory definition, Table 2 (read 20261102 20:43 UTC)
6. https://arxiv.org/abs/2310.08560 : MemGPT title, authors, first version, abstract (read 20261102 20:42 UTC)
7. https://arxiv.org/html/2310.08560 : main and external context, DMR task and table, related work (read 20261102 20:43 UTC)
8. https://raw.githubusercontent.com/letta-ai/letta/main/README.md : "Letta (f.k.a. MemGPT)" (read 20261102 20:47 UTC)
9. https://arxiv.org/abs/2404.13501 : memory survey title, authors, first version, abstract (read 20261102 20:42 UTC)
10. https://arxiv.org/html/2404.13501 : classification by source, form and operation, tables (read 20261102 20:43 UTC)
11. https://api.crossref.org/works/10.1145/3748302 : ACM TOIS 43(6), 2025 (read 20261102 20:48 UTC)
12. https://arxiv.org/abs/2501.13956 : Zep title, authors, first version, abstract (read 20261102 20:42 UTC)
13. https://arxiv.org/html/2501.13956 : bi-temporal model, timestamps, GraphRAG communities, DMR and LongMemEval tables (read 20261102 20:43 UTC)
14. https://raw.githubusercontent.com/getzep/graphiti/main/README.md : Graphiti README links the Zep paper (read 20261102 20:47 UTC)
15. https://arxiv.org/abs/2502.12110 : A-MEM title, authors, versions, NeurIPS comment, abstract (read 20261102 20:42 UTC, abstract re-read 20:59 UTC)
16. https://arxiv.org/html/2502.12110 : related work on Mem0, baselines, DialSim, checklist (read 20261102 20:43 UTC)
17. https://arxiv.org/abs/2504.19413 : Mem0 title, authors, first version, abstract (read 20261102 20:42 UTC, abstract re-read 20:59 UTC)
18. https://arxiv.org/html/2504.19413 : operations, Neo4j graph, baselines, LoCoMo tables, token footprint, embedding model (read 20261102 20:43 UTC, embedding model re-read 21:01 UTC)
19. https://api.crossref.org/works/10.3233/FAIA251160 : Mem0 at ECAI 2025 (read 20261102 20:48 UTC)
20. https://arxiv.org/abs/2512.13564 : survey title, authors, versions, abstract (read 20261102 20:42 UTC)
21. https://arxiv.org/html/2512.13564 : prior surveys, MemGPT, graph-based memory practices, citations of this group's papers (read 20261102 20:43 UTC)
22. https://arxiv.org/abs/2610.30755 : title, authors, version, abstract of the Naive RAG study (read 20261102 20:42 UTC, re-read 20:59 UTC)
23. https://arxiv.org/html/2610.30755 : compared systems, benchmarks, LoCoMo tables, limitations, references (read 20261102 20:43 UTC); baseline list, Tables 10 to 12 and their source notes, appendix D headings (re-read 20:59 UTC)
24. https://api.semanticscholar.org/graph/v1/paper/batch : citation counts (Semantic Scholar Graph API), carried over from the papers research of the same day, not re-queried (read 20261102 19:47 UTC)
25. https://arxiv.org/abs/2305.10250 : MemoryBank abstract (read 20261102 20:47 UTC)
26. https://arxiv.org/abs/2507.03724 : MemOS abstract (read 20261102 20:47 UTC)
27. https://arxiv.org/abs/2512.12818 : Hindsight abstract (read 20261102 20:47 UTC)
28. https://arxiv.org/abs/2610.34073 : Memory Tax abstract and submission date (read 20261102 20:47 UTC, re-read 20:59 UTC)
29. https://arxiv.org/abs/2606.24775 : agent-native memory study abstract (read 20261102 20:47 UTC)
30. https://arxiv.org/abs/2606.09900 : Bi-Temporal Memory Engine abstract (read 20261102 20:47 UTC)
31. https://arxiv.org/abs/2610.29823 : MemoryTax, the similarly named paper (read 20261102 20:49 UTC)
32. https://export.arxiv.org/api/query : arXiv searches for earlier work before the first version of Zep (submission date up to 20250119; title, abstract and comment): `temporal knowledge graph` with `memory` and agent or LLM (2 records: "Temporal Knowledge-Graph Memory in a Partially Observable Environment", 2408.05861 of 20240811, and a story-generation paper, 2412.13575 of 20241218); `bi-temporal` or `bitemporal` (129 records, mostly remote-sensing change detection; among the knowledge-graph ones "Bitemporal Property Graphs to Organize Evolving Systems", 2111.13499 of 20211126) (read 20261102 22:57 to 23:03 UTC). Titles only; a search of titles and abstracts, not exhaustive
33. https://arxiv.org/html/2610.34073 and the other renderings listed in source 27 of the page [Agentic search over raw data](./agentic-search.md) (read 20261102 22:59 to 23:17 UTC): no rendering searched mentions the Naive RAG study by title or arXiv id; Memory Tax (2610.34073) does not. A name search of the text; a paper may cite a work without the name appearing in the rendering
