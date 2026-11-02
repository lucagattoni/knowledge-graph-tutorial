---
type: benchmark
datasets: [longmemeval]
updated: 20261102 21:42 UTC
---

# MemoryAgentBench

MemoryAgentBench (arXiv July 2025, v4 June 2026) scores [agent memory](../index/agent-memory.md) on four competencies: long texts are fed to an agent in chunks and questions come afterwards [1][2]. This page says what is asked, how it is scored and what studies found; its data is described here. The numbers mix papers, readers and versions, so they are not a ranking.

## What it tests

Four competencies the authors take from memory science: accurate retrieval (AR), [test-time learning](../index/test-time-learning.md) (TTL), long-range understanding (LRU) and [selective forgetting](../index/selective-forgetting.md) (SF), meaning dropping facts that later input overwrites [1][2]. The dataset card and README call the fourth "conflict resolution" [3][4].

## Tasks, metrics and protocol

Each set is cut into chunks; each chunk is a user message asking the agent to memorise it, and questions follow the last chunk [2]. Agent classes: long-context, simple RAG ([BM25](../index/bm25.md)), embedding RAG, structure-augmented RAG, agentic memory. GPT-4o-mini is the default backbone and 10 chunks are retrieved, of 512 tokens for the document-QA, LongMemEval (S*) and SF sets and 4,096 elsewhere [2]. The overall score is the mean of the four competency averages (GPT-5-mini: 60.55, printed 60.6), computed from Table 3 and stated by Bao et al. [2][5].

## Datasets

| Competency | Sets (questions) | Metric |
|---|---|---|
| AR | SH-Doc QA (100), MH-Doc QA (100), LongMemEval (S*) (300), EventQA (500) | substring match; [LLM judge](../index/llm-as-judge.md) (GPT-4o); multiple choice |
| TTL | BANKING77, CLINC150, NLU, TREC coarse, TREC fine (100 each), movie recommendation (200) | accuracy; Recall@5 |
| LRU | InfiniteBench summarisation (100), DetectiveQA (71) | F1 times fluency (GPT-4o); accuracy |
| SF | FactConsolidation single-hop and multi-hop (100 each) | substring match |

Table 6 sums to 2,071 questions [2]. Two sets are new: EventQA (choose the next event in a novel) and FactConsolidation, built from MQuAKE counterfactual edit pairs; the rest are reshaped existing sets. LongMemEval (S*) joins history segments of the [LongMemEval dataset](../datasets/longmemeval.md) into five histories, so its scores differ from [LongMemEval](longmemeval.md) proper [2]. Licence: MIT (repository `LICENSE`, card); the reused sets' licences are unstated [3][4].

## Results

Higher is better. Rows 1 to 3 are Table 3 of v4, run by the benchmark authors, not the systems' vendors; the MIRIX paper shares an author (see Known problems).

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Long context: GPT-5-mini; Claude-3.7-Sonnet; GPT-4o; GPT-4.1-mini; GPT-4o-mini (reference) | 60.6; 49.6; 48.8; 46.9; 42.2 | overall | benchmark authors | no | 20260628 | [2] |
| [HippoRAG](../projects/hipporag.md)-v2; BM25 | 41.6; 41.5 | overall | same | no | 20260628 | [2] |
| [MIRIX](../projects/mirix.md) (GPT-4.1-mini); MemGPT ([Letta](../projects/letta.md)); Zep ([Graphiti](../projects/graphiti.md)); [Mem0](../projects/mem0.md); [Cognee](../projects/cognee.md) | 37.7; 28.3; 24.0; 21.1; 20.6 | overall | same | MIRIX: yes, shared author; others no | 20260628 | [2][8] |
| Raw-RAG; Memora; Mem0 (reader GPT-4o-mini) | 48.32; 43.84; 41.28 | mean of four competency macros | Bao et al. | Raw-RAG: yes, their method; others no | 20261022 | [5] |
| Same three (reader DeepSeek-V4-Flash) | 53.41; 47.88; 41.95 | same | same | same | 20261022 | [5] |
| ReFind; HippoRAG 2; BM25-RAG | 58.2; 53.2; 48.8 | macro-mean, six AR and SF sets | ReFind authors | yes; baselines reused | 20260816 | [6] |
| Gemini-3-Flash; GPT-5-mini; DeepSeek-V3.2; BM25; Mem0 | rank 1.00; 3.00; 5.50; 4.17; 4.50 | overall rank on InEp-Know, lower is better | EvoMemBench authors | no | 20261030 | [7] |
| Same five | 58.0; 24.0; 10.0; 7.0; 7.0 | multi-hop FactConsolidation accuracy | same | no | 20261030 | [7] |

*Reading:* BM25 and plain long-context models beat Mem0, Zep, Cognee and MemGPT in the authors' table; Raw-RAG tops the systems Bao et al. compare. On multi-hop forgetting, DeepSeek-V3.2 run as a long-context model (10.0) is level with BM25 and Mem0 on the same backbone (7.0 each), so the gap to Gemini-3-Flash (58.0) follows the model, not the memory design [7].

## Known problems

- **No official leaderboard** in the README or on the card [3][4].
- **Versions differ.** The card says samples were removed and one added (20250929). ReFind states 2,800 questions (EventQA 1,500), against 500 in Table 6; the card's split sizes differ from Table 6 too. Unreconciled [2][3][6].
- **Same system, different score.** Mem0 is 21.1 in Table 3 and 41.28 in Bao et al., both with GPT-4o-mini, but the runs differ: Bao et al. pass retrieved evidence to their own reader prompts (Appendix G.7). They do not reconcile the two numbers [2][5].
- **Mixed metrics** in one average, GPT-4o judging for two sets, and strict TTL parsing ("label: 43" fails for "43") [2][4].
- **Multi-hop forgetting** peaked at 28% in Table 3; o4-mini scored 80.0 on a 6K version and 14.0 at 32K [2].
- **Independence.** The abstract page says "Y. Hu and Y. Wang contribute equally"; both this paper's and the MIRIX paper's front matter give Yu Wang the same institutional mailbox handle (not copied here), which indicates one person [1][2][8]. The MIRIX row is partly first-party.

## Used by

EvoMemBench builds InEp-Know from the AR and SF sets [7]; Bao et al. ([agent memory](../papers/agent-memory.md)) and ReFind ([agentic search](../papers/agentic-search.md)) report on it [5][6]. Trend: [agent memory](../trends/agent-memory.md). Attention: 298 citations (Semantic Scholar, carried over) [9]; 484 stars on 20261102; ICLR 2026 acceptance per the README [4].

## Sources

1. https://arxiv.org/abs/2507.05257 : abstract page: authors, "Y. Hu and Y. Wang contribute equally", versions v1 20250707 to v4 20260628 (read 20261102 21:34 UTC)
2. https://arxiv.org/html/2507.05257 : v4 full text: Tables 2, 3, 6, 16, section 4.2 and 4.3.4, Appendix B and C, author front matter (read 20261102 21:30 UTC)
3. https://huggingface.co/datasets/ai-hyz/MemoryAgentBench : card (`license: mit`), splits, update notes, last modified 20260621 (read 20261102 20:59 UTC)
4. https://github.com/HUST-AI-HYZ/MemoryAgentBench : `LICENSE` MIT, README (metric table, ICLR note), 484 stars, last push 20260925 (stars and push re-read 20261102 21:33 UTC; README read 21:00 UTC)
5. https://arxiv.org/html/2610.30755 : Bao et al., 20261022: Table 4 and caption, section 4.1, Appendices A.4.3 and G.7 (read 20261102 21:30 UTC)
6. https://arxiv.org/html/2608.12888 : ReFind v2 (20260816): Table 2, section 4 (read 20261102 21:06 UTC)
7. https://arxiv.org/html/2605.18421 : EvoMemBench v3 (20261030): section 4.1, Table 3 incl. the DeepSeek-V3.2 row (read 20261102 21:30 UTC)
8. https://arxiv.org/html/2507.07957 : MIRIX paper (v1 20250710): authors and front matter (read 20261102 21:30 UTC)
9. https://api.semanticscholar.org/graph/v1/paper/arXiv:2507.05257?fields=citationCount : 298, carried over from the same day's research (read 20261102 20:00 UTC, not re-queried)
