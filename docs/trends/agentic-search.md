---
type: trend
shift: building structure -> letting the agent search
status: growing
order: 6
updated: 20261102 23:27 UTC
---

# Agentic search over raw data: from building structure to letting the agent search

This page answers one question: when does an [agent](../index/agent.md) that searches raw files, logs or passages itself ([agentic search](agentic-search.md)) do better than one that queries a graph, tree or memory store built beforehand? Most evidence is from 2026 papers. I found no row in the 20261030 snapshot whose description names this as its mechanism [22], so the page is told through papers and the tools they test. Its status is `growing` on the strength of papers only.

> **Distinctive because** no model builds structure in advance: the agent searches the unmodified record with [grep](../index/grep.md) or a lexical index, so a model is used only at query time [1][3]. The nearest neighbour is [vectorless retrieval](./reasoning-over-structure.md), which lets a model steer but builds a document tree first [26].

## Why it emerged

The problem was the build. Standard [GraphRAG](../index/graphrag.md) uses a language model to extract the graph, and [Microsoft GraphRAG](../projects/microsoft-graphrag.md) estimates that extraction is "roughly 75% of indexing cost" [17]. Its README now says the project is "largely in maintenance mode" and that frontier models "have changed dramatically" since July 2024 [18]. Memory systems pay too: streaming a 1,710-message, near-million-token conversation took 0.33 hours into the raw-retrieval baseline (dense retrieval over raw history, no agent loop) and 3.25 to 26.95 hours into the memory systems compared [7]. Two kinds of structure can lose evidence. A fixed top-k retrieval interface can: one team argues that "evidence filtered out early cannot be recovered by stronger downstream reasoning" [3]. Built memory can too: the Memory Tax paper says memory processes "may also remove or obscure evidence" [8]. The earlier era is told in [Language models meet retrieval](../history/language-models-meet-retrieval.md).

The enabling change was the agent loop that [large language models](../index/large-language-model.md) (LLMs) can now run. In it the agent, not a fixed pipeline, steers retrieval. Anthropic wrote on 20250929 that as models improve "the level of autonomy of agents can scale", and that Claude Code uses glob and grep to retrieve files "just-in-time, effectively bypassing the issues of stale indexing and complex syntax trees" [16]. The same post names the cost: runtime exploration "is slower than retrieving pre-computed data" [16].

| Date | Step | Source |
|---|---|---|
| 20221006 | ReAct: reasoning interleaved with actions that query external sources | [14] |
| 20250312 | Search-R1: a model trained by [reinforcement learning](../index/reinforcement-learning.md) to issue several search queries mid-reasoning | [13] |
| 20250929 | Anthropic: the coding agent navigates by glob and grep | [16] |
| 20260503 to 20260514 | Direct corpus interaction (grep and shell on the raw corpus), Pi-Serini ([BM25](../index/bm25.md) plus a capable model), "Is Grep All You Need?" | [3][4][2] |
| 20260729 to 20261030 | Scaling study, ReFind, Raw-RAG, Memory Tax, the [RAGFlow](../projects/ragflow.md) team's harness paper | [6][1][7][8][5] |

## Why it matters

- **It removes the index bill.** Search happens at question time. At the smallest (bedrock) tier of one scaling study a file-system agent used 226K query tokens per question against 5.8K for [BM25](../index/bm25.md), 39 times more [6].
- **It is now the baseline.** Raw-RAG (dense retrieval and reranking over raw history, with no agent loop) ranked first among the compared memory systems in six of seven benchmark-model settings [7]; Memory Tax finds many memory systems below naive [retrieval-augmented generation](../index/retrieval-augmented-generation.md) (RAG) [8]. A trend that builds structure ([graph-based RAG](./graph-based-rag.md), [agent memory](./agent-memory.md)) must beat this.
- **Activity is rising, but the count is noisy.** A keyword probe found 151 arXiv results in 20251102 to 20261102 against 26 in the year before (x5.8); a control for any LLM-agent wording rose x2.50 (15,158 against 6,068) [19]. The probe also catches web-search agents, so it is not a count of this trend's papers.

## How it works

The agent runs a loop: write a query, read results, reformulate, decide when to stop [5]. The 2026 papers vary what it searches with.

| Variant | What exists before the question | Examples |
|---|---|---|
| No index | Raw files; the agent uses grep, glob, file reads, shell | Claude Code [16]; direct corpus interaction [3] |
| Lexical index, agent steers | An [inverted index](../index/inverted-index.md) over unmodified text; no model-built structure | ReFind [1]; Pi-Serini [4]; the RAGFlow team's harness [5], which argues for compiled structure as a supply layer although its BM25-and-grep result belongs here |
| Trained policy | A search engine; the model is trained to use it | Search-R1 [13] |
| Agent after ranking | A global BM25 ranking; the agent works on the shortlist | the Agent+BM25 control in the scaling study, run on 150 questions and not a ranked system [6] |

"Raw" here means no model builds anything semantic. A BM25 index is allowed, because it needs no model [1][6].

### What decides the result

- **The [harness](../index/agent-harness.md) and the model, not only the retriever.** In one study, grep beat [vector search](../index/vector-search.md) for every harness-model pair with inline results; yet the same Claude Opus 4.6 with inline grep scored 93.1% in the authors' harness and 76.7% in Claude Code [2].
- **Corpus size.** In a synthetic enterprise corpus the file-system agent led at the smallest tiers; plain BM25 overtook it around 10 million corpus tokens and led at every larger shared tier, by nearly 20 points at 601 million (50.5 against 30.7 at full scale) [6]. A separate control on 150 of the questions changed only the retrieval tool: the same agent given BM25 search scored 69.4 against 36.9 for the raw-file agent at full scale, at about one ninth of the tokens. The authors treat it as "a mechanism control, not as an eighth system" on the 28-tier ladder [6].
- **Question shape.** Agentic search narrows the gap to GraphRAG, but GraphRAG keeps an edge on complex [multi-hop questions](../index/multi-hop-question-answering.md) [9].

## Where the line falls

No trend is merged into this one. Four neighbours stay separate, each for what is built.

### Vectorless retrieval

In [Vectorless retrieval](./reasoning-over-structure.md), [PageIndex](../projects/pageindex.md) builds a tree from the document layout and a model walks it [26]. Here nothing is built. The two meet in evidence: the RAGFlow team found a PageIndex-style outline gave no accuracy gain on FRAMES and "degraded" at scale under a BM25 and grep harness [5]; a financial study found vector agentic RAG won 68% of comparisons over embedding-free node systems [10].

### Code graphs

In [Code graphs for coding agents](./code-knowledge-graphs.md), [codebase-memory-mcp](../projects/codebase-memory-mcp.md) parses a repository into a graph; the agent here greps instead. Codebase-Memory (first-party) reports 83% answer quality against 92% for a file-exploration agent, at ten times fewer tokens [12]. [Experiment X4](../experiments/x4-code-graph-vs-grep.md) is built to test this pair; nothing has been run on an agent yet [24].

### Plain files and wikis

In [Plain files as agent knowledge](./plain-file-knowledge.md), a model-maintained wiki is compiled in advance. A preregistered comparison (13 questions, 24 papers, one model) found the agent-browsed wiki better at connecting findings and about 21 times costlier per query in tokens [25].

### Agent memory

In [Agent memory](./agent-memory.md), memory layers extract and update records. ReFind keeps the raw archive and searches it [1].

## Representative projects

No project has a page of its own: none passed the project tests for this trend [22]. These tools are what the papers ran or built.

| Project | Role | Licence (LICENSE file) | Stars |
|---|---|---|---|
| Claude Code, [anthropics/claude-code](https://github.com/anthropics/claude-code) | Glob and grep harness [16]; compared in [2] | all rights reserved [20] | not in the snapshot |
| [openai/codex](https://github.com/openai/codex), [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | Other harnesses compared in [2] | Apache-2.0 [27][28] | not in the snapshot |
| [Search-R1](https://github.com/PeterGriffinJin/Search-R1) | Trained search policy [13]; last push 20251113 | Apache-2.0 [29] | not in the snapshot |
| [pi-serini](https://github.com/justram/pi-serini) | BM25 search agent [4]; last push 20260512 | MIT [21] | not in the snapshot |
| [RAGFlow](../projects/ragflow.md) | Its team describes a BM25 and grep harness plus compiled evidence [5] | Apache-2.0 [23] | 93,209 (snapshot 20261030 19:54 UTC) [22] |

Stars are signals, not verdicts, and are shown only from the snapshot; a repository missing from it has no figure here.

## Fundamental papers

The [papers chapter](../papers/agentic-search.md) holds the relations. Candidates, with the test each passes: ReAct (origin of the loop) [14]; Search-R1 (trained policy) [13]; the Agentic RAG survey (survey of record) [15]; direct corpus interaction and "Is Grep All You Need?" (turning points) [3][2]; the scaling study (the crossover) [6]. The papers chapter keeps five for this trend (ReAct, IRCoT, Self-RAG, Lost in the Middle, and RAG or Long-Context LLMs); of the candidates above Search-R1 is in the learned-traversal group, and the rest are in further reading.

## What is measured, and by whom

| Study | Setting | Result | Run by |
|---|---|---|---|
| ReFind [1] | [MemoryAgentBench](../benchmarks/memoryagentbench.md), six benchmarks, about 2,800 questions, GPT-4o-mini | Mean accuracy 58.2 against 53.2 ([HippoRAG 2](../projects/hipporag.md)) and 48.8 (single-shot BM25); baselines reused from the benchmark paper | First-party |
| "Is Grep All You Need?" [2] | 116-question [LongMemEval](../datasets/longmemeval.md)-S subset; five models; four harnesses | Inline grep above vector in all pairs; vector ahead in 5 of 10 pairs with file-based delivery | Authors of one of the harnesses |
| Pi-Serini [4] | BrowseComp-Plus, BM25, gpt-5.5 | 83.1% answer accuracy | First-party |
| RAGFlow team [5] | BM25 and grep, MiniMax M3 | 85% on BrowseComp-Plus; 91% on FRAMES; no confidence intervals | First-party |
| Scaling study [6] | [EnterpriseRAG-Bench](../benchmarks/enterpriserag-bench.md) (synthetic), 500 questions, one reader, 28 tiers | Crossover near 10M tokens; BM25 leads larger shared tiers (50.5 against 30.7 at full scale). Separate 150-question control: same agent with BM25 search 69.4, raw-file agent 36.9 | Authors' own agent; compared systems are others' |
| Raw-RAG, Memory Tax [7][8] | Memory benchmarks; no agent loop | Raw dense retrieval first in 6 of 7 settings; many memory systems below naive RAG. Baseline for this trend, not agentic search | Third party to the memory systems |
| [RAGSearch](../benchmarks/ragsearch.md) [9] | Dense RAG against five GraphRAG backends, agentic | Gap narrowed, not closed | Benchmark authors |
| Small coding agents [11] | SWE-bench Verified (real software issues from GitHub projects), open-weight models | Structured tools (embedding search and graph tools together) double grep-only accuracy for two models (Qwen3-8B, Gemma 4 E4B); gain 17 to 21 points at 1.7 to 4B, 4 to 5 at 32B | Single author |

Direct corpus interaction reports gains over sparse, dense and [reranking](../index/reranking.md) baselines on BRIGHT and [BEIR](../benchmarks/beir.md) sets; scores were not read [3]. The one controlled ablation of grep against structured tools found here used small open-weight models, and I did not read its graph-only and embedding-only splits [11]. None of the sources read runs a frontier coding agent with and without a code graph on the same questions.

## Assessment

*Reading:* the strongest finding is narrower than the shift's title. Searching raw text, by an agent or by plain retrieval, matched or beat elaborate memory structure in conversation memory [1][7][8]; in deep-research benchmarks a BM25 agent beat released agents that use dense retrievers [4], and the RAGFlow team (first-party) finds compiled structure gives no detectable accuracy gain under a competent harness, only a supply layer [5]. In the one scaling study, plain BM25 leads the main ladder at scale and its authors conclude "lexical retrieval is the strongest scalable default"; in a separate 150-question control the same agent given BM25 search scored 69.4 against 36.9, and they conclude agentic reasoning "works best after ranked discovery rather than in place of it" [6]. The shift is therefore from structure as the retrieval path to structure as an optional supply layer, which is how the RAGFlow team frames it [5].

Weaknesses: most results are first-party; most tasks look up facts in a record (conversation recall, BrowseComp-Plus, FRAMES), while the one study with global or multi-hop questions keeps GraphRAG ahead [9]; the one scaling study is synthetic with one reader; the harness moves scores as much as the retriever does [2]; and small models still gain from tools [11]. Cost is not solved: the raw-file agent used 895K tokens per question at full scale [6]. I expect the family to merge into hybrids; whether it settles depends on replication outside benchmark corpora.

## Signals to watch

| Signal | Check |
|---|---|
| A first project that makes raw agentic search its mechanism | The next GitHub snapshot [22] |
| X4 result: code graph against grep with a real agent | [X4 page](../experiments/x4-code-graph-vs-grep.md) |
| The scaling crossover on a non-synthetic corpus | Replications of [6] |
| Code for ReFind or direct corpus interaction | Not found in the pages read: unstated [1][3] |
| Gains of structured tools (embedding and graph) shrinking with model size | Follow-ups to [11] |

## Sources

1. https://arxiv.org/abs/2608.12888 : ReFind: abstract (lexical index, no semantic structure; 58.2 against 53.2), Table 2 notes (baselines reused), subsets of 50 and 15 questions (abstract re-read 20261102 20:31 UTC; other parts read 20261102 20:11 UTC)
2. https://arxiv.org/abs/2605.15184 : "Is Grep All You Need?": 116 questions, harness effect, Tables 1 to 3 text (read 20261102 20:11 UTC)
3. https://arxiv.org/abs/2605.05242 : direct corpus interaction: abstract only; the "evidence filtered out early" quote criticises the fixed top-k similarity interface (read 20261102 20:30 UTC)
4. https://arxiv.org/abs/2605.10848 : Pi-Serini: abstract, 83.1% on BrowseComp-Plus, "outperforming released search agents that use dense retrievers" (read 20261102 20:30 UTC)
5. https://arxiv.org/abs/2610.41172 : RAGFlow team: abstract (search harness loop, 85% and 91%, compilation as "a supply layer", no gain on FRAMES); structural audit and limits section read earlier (abstract read 20261102 20:30 UTC; other parts 20261102 20:11 UTC)
6. https://arxiv.org/abs/2607.26497 : scaling study, full text (arxiv.org/html/2607.26497): abstract; Table 1 text (BM25 50.5 against 30.7 at full scale); 226K and 5.8K tokens per question; Section 5.1 and Table 4 (150-question Agent+BM25 control, 69.4 against 36.9, 101K and 895K tokens, "mechanism control, not as an eighth system"); Section 7 (read 20261102 20:30 UTC)
7. https://arxiv.org/abs/2610.30755 : Raw-RAG: abstract (dense retrieval and reranking over raw history; six of seven settings; re-read 20261102 20:30 UTC); ingestion hours read earlier (20261102 20:11 UTC)
8. https://arxiv.org/abs/2610.34073 : Memory Tax: abstract and setup; "may also remove or obscure evidence" (read 20261102 20:30 UTC)
9. https://arxiv.org/abs/2604.09666 : RAGSearch: abstract (read 20261102 20:10 UTC)
10. https://arxiv.org/abs/2511.18177 : financial study, 68% win rate, 1,200 filings (read 20261102 20:10 UTC)
11. https://arxiv.org/abs/2610.33958 : small coding agents on SWE-bench Verified: abstract ("Structured tools double grep-only accuracy"; arms are grep only, +embedding search, +graph tools, all) (read 20261102 20:30 UTC)
12. https://arxiv.org/abs/2603.27277 : Codebase-Memory: 83% against 92%, ten times fewer tokens (read 20261102 20:10 UTC)
13. https://arxiv.org/abs/2503.09516 : Search-R1: abstract (model learns to generate search queries during reasoning with reinforcement learning); v1 20250312 (read 20261102 20:31 UTC)
14. https://arxiv.org/abs/2210.03629 : ReAct: abstract; v1 20221006 (read 20261102 20:14 UTC)
15. https://arxiv.org/abs/2501.09136 : Agentic RAG survey: abstract; taxonomy (read 20261102 20:10 UTC)
16. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents : published 20250929; glob, grep, "just in time" (read 20261102 20:11 UTC)
17. https://microsoft.github.io/graphrag/index/methods/ : the 75% estimate (read 20261102 20:14 UTC)
18. https://github.com/microsoft/graphrag (README via the GitHub API) : maintenance-mode notice (read 20261102 20:15 UTC)
19. https://export.arxiv.org/api/query : probe query `(abs:grep OR abs:"agentic search" OR abs:"agent-controlled search" OR abs:"raw files" OR abs:"raw logs" OR abs:"raw chat logs" OR abs:"file-system agent" OR abs:"filesystem agent" OR abs:"search tools") AND (abs:memory OR abs:RAG OR abs:retrieval) AND (abs:agent OR abs:agents OR abs:agentic)`, submitted 20251102 to 20261102 (151 results) and 20241102 to 20251101 (26); control `(abs:agent OR abs:agents OR abs:agentic) AND (abs:LLM OR abs:LLMs OR abs:"language model" OR abs:"language models")` (15,158 and 6,068) (read 20261102 20:10 to 20:11 UTC; re-run 20261102 20:31 UTC reproduced 151 for the first window; the other three counts could not be re-run because the service answered HTTP 429, so they rest on the first run)
20. https://github.com/anthropics/claude-code : LICENSE.md ("All rights reserved") (read 20261102 20:13 UTC)
21. https://github.com/justram/pi-serini : MIT LICENSE, last push 20260512 (read 20261102 20:14 UTC)
22. kb-kg/landscape/20261030_1954-github/repos.tsv : snapshot of 20261030 19:54 UTC; RAGFlow 93,209 stars; no row with agentic raw search as its mechanism (read 20261102 20:13 to 20:15 UTC)
23. https://github.com/infiniflow/ragflow : Apache License text in the LICENSE file (read 20261102 20:16 UTC)
24. docs/experiments/x4-code-graph-vs-grep.md : X4 design; no agent or tool has run on it (read 20261102 20:09 UTC)
25. https://arxiv.org/abs/2605.18490 : preregistered wiki comparison: 13 questions, 24 papers, about 21 times more tokens (read 20261102 20:14 UTC)
26. https://github.com/VectifyAI/PageIndex : README (replaces the vector index with a hierarchical tree index; tree extracted from the document layout) and MIT LICENSE (read 20261102 20:18 UTC)
27. https://github.com/openai/codex : Apache License text in the LICENSE file (read 20261102 20:13 UTC)
28. https://github.com/google-gemini/gemini-cli : Apache License text in the LICENSE file (read 20261102 20:13 UTC)
29. https://github.com/PeterGriffinJin/Search-R1 : Apache License text in the LICENSE file; last push 20251113 (read 20261102 20:13 UTC)
