---
type: project
repo: EverMind-AI/EverOS
trends: [agent-memory, plain-file-knowledge]
updated: 20261103 01:45 UTC
---

# EverOS

This page answers what EverOS is, how it keeps memory as Markdown files with derived indexes, and who has measured it. EverOS is the renamed EverMemOS [5][6]. The high scores in its repository and paper are its authors' own; runs by others give lower or mixed figures on other benchmarks [23][24][25][26].

| Field | Value |
|---|---|
| Repository | https://github.com/EverMind-AI/EverOS [1] |
| Licence | Apache-2.0. GitHub classifies the `LICENSE` file as Apache-2.0; the file is the standard text, differing only in the appendix line "Copyright 2025 EverMind AI" [2][3]. The `NOTICE` file excludes one test fixture derived from LoCoMo (CC BY-NC 4.0, non-commercial use only) from that licence [4]. |
| Trends | [Agent memory](../trends/agent-memory.md) · [Plain files as agent knowledge](../trends/plain-file-knowledge.md) |

## What it is

EverOS calls itself "a Python library and local-first memory runtime for agents and makers" that stores conversations, files and agent trajectories as readable Markdown, with SQLite and LanceDB indexes synced from it [5]. The README says it was "formerly called EverMemOS", and the old repository name returns this one [5][6]. Release 1.0.0 (20260606) was "a fresh architecture"; MongoDB, Elasticsearch, Milvus, Redis and Kafka are not part of it [7][19]. Interfaces are an HTTP API, a CLI and `everos-mcp`, a separate [MCP](../index/model-context-protocol.md) server [5][9]. A hosted EverOS Cloud exists; its terms are **unstated** [5][10].

## How it works

**Storage.** Markdown files with YAML front matter are the truth. SQLite holds state, the sync queue and the buffer of messages not yet extracted; LanceDB holds vector and [BM25](../index/bm25.md) columns. The docs call both derived and rebuildable [11]. Since 1.3.0 a remote Milvus or Zilliz Cloud index can replace LanceDB [10][13].

**Write.** `/add` buffers messages; one model call finds where an episode ends, and `/flush` forces it. The episode is on disk before the call returns. Atomic facts, foresight notes, a user profile, agent cases and agent skills follow later, from an in-process engine [11]. User and agent memory are separate tracks [5]. A weekly reflection pass, off by default, merges episode clusters; its page warns that "Each run is a lossy LLM merge" [14].

**Sync and read.** A file watcher, a scanner (default 30 seconds) and a reconciler re-index hand edits [11][12]. Reads lag writes by up to about 10 to 15 seconds under load [11]. Search is keyword, vector, hybrid (default) or agentic [15]; since 1.3.1 also `llm_multiround`, where a separate decider model keeps evidence and asks follow-up queries; the API doc does not list it [10][15]. Extraction needs a model endpoint and hybrid search an embedding provider, so "local-first" is not offline [5][10]. The extraction algorithms sit in separate `everalgo-*` packages [8][16].

**Against its neighbours.**

| Neighbour | Store | Against EverOS |
|---|---|---|
| [Mem0](mem0.md) | vector store; add-only extraction | EverOS keeps Markdown as truth and derives facts, profile and skills later [29] |
| [Hindsight](hindsight.md) | PostgreSQL; four memory types | by default no database server or graph store [5][11][29] |
| [Basic Memory](basic-memory.md), [Tigerless agent-memory](tigerless-agent-memory.md) | Markdown plus SQLite | closest in storage; there a person or the working agent writes the files, here a pipeline with its own model client [11][29] |

## Evidence

Every score is published; none was reproduced here.

| Source | Run by | Setting | EverOS / EverMemOS | Standing |
|---|---|---|---|---|
| Paper (arXiv 20260105; ACL 2026) | EverMind and Shanda Group authors | [LoCoMo](../benchmarks/locomo.md), 1,540 questions, GPT-4o-mini / GPT-4.1-mini reader, three judgments averaged; [LongMemEval](../benchmarks/longmemeval.md)-S, 500 | 86.76 / 93.05 (Zep 81.06 / 85.22); 83.00 (MemOS 77.80, copied from its leaderboard) | first-party [23] |
| `benchmarks/README.md` (20260908) | EverMind | `llm_multiround`, top_k 20, one gpt-4o-mini judge | LoCoMo 94.42, LongMemEval 94.00, EverMemBench (EverMind's own) 66.67, SubtleMemory 71.75 | first-party [5][17][18] |
| OmniMemEval (20261026) | MemTensor, maker of [MemOS](memos.md) | gpt-4.1-mini answer, gpt-4o-mini judge; version unstated | LoCoMo 82.75 (hosted), LongMemEval 80.40, HaluMem 88.66, BEAM 100K 58.64 | competitor [26] |
| Bao et al. (20261022) | authors of the Raw-RAG baseline | MEME, [MemoryAgentBench](../benchmarks/memoryagentbench.md); two readers | 21.57 / 27.24; 36.49 / 42.54 (Raw-RAG 39.30 / 43.19; 48.32 / 53.41) | third party with a stake [24] |
| MobileMem (20260811) | 19 authors; no "EverMind" in the paper text | own benchmark, Qwen3.5-397B judge | 62.93 / 61.18 for GPT-4.1-mini / GPT-5.4-mini (best: A-MEM 79.68 / HippoRAG2 80.06) | independent [25] |

Bao et al. reuse the paper's LoCoMo and LongMemEval figures [24]; RippleMem copies the 83.00 [27]. Agent Memory Leaderboard cycle 1 (20260812, 123 results) has no EverOS entry; whether it was submitted is **unstated** [28]. No independent run of the 93.05 or 94.42 figures was found (searched 20261103).

*Reading:* the LoCoMo figure is 93.05, 94.42 or 82.75 depending on who ran it, each under a different judge, reader and retrieval, so none settles accuracy. The LoCoMo decider is deepseek-v4-flash in the repository table but qwen3.6-27B in a config comment: **unstated** which [17][18]. "MemScene", a term of the paper, is absent from the current docs and changelog, so the paper's link to today's code is **unstated** [10][11][23].

## Status and direction

*Release.* `v1.5.1`, 20261022 13:22 UTC, is the latest; PyPI agrees. `main` says 1.6.0 and the CHANGELOG dates it 20261028, but no tag exists. That commit is breaking: environment switches become settings and imports move to service facades [8][10][19][20]. There have been 22 releases since 1.0.0, 13 since 20260804 (4 release candidates) [19].

*Activity in the last 90 days.* 73 commits to `main` from 20260804 to 20261102: 17 in August (from the 4th), 28 in September, 28 in October, none in November; the last was 20261030. One login holds 51 (69.9%, computed) [20]. Open: 37 pull requests, 29 issues; 9 contributors [21].

*Direction.* The README lists plugins for OpenClaw, Hermes Agent, DeepSeek Harness and Dify [5]. Documentation lags: `docs/overview.md` and `CITATION.md` still name v1.1.4, and the latter says the paper is "coming soon" [22]. Roadmap: **unstated**, beyond a "future v2" sync via EverMe [22].

*Reading:* active, with work concentrated in one login and a breaking release untagged. For the plain-files trend, Markdown is the record and hand edits are re-indexed [11][12], but extraction and search still need model endpoints, and no measurement isolates what the file format adds.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)

**Projects**

- [Projects](README.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/EverMind-AI/EverOS : repository metadata, description, creation date, archived flag, default branch (read 20261103 01:30 UTC)
2. https://api.github.com/repos/EverMind-AI/EverOS/license : `LICENSE` text and GitHub's Apache-2.0 classification (read 20261103 01:30 UTC)
3. https://api.github.com/licenses/apache-2.0 : standard Apache 2.0 text, compared line by line with the `LICENSE` file (read 20261103 01:38 UTC)
4. https://github.com/EverMind-AI/EverOS/blob/main/NOTICE : CC BY-NC 4.0 carve-out for one LoCoMo-derived fixture (read 20261103 01:30 UTC)
5. https://api.github.com/repos/EverMind-AI/EverOS/readme : description, former name, quick start, search methods, tracks, sister projects, integrations (read 20261103 01:30 UTC)
6. https://api.github.com/repos/EverMind-AI/EverMemOS : returned this repository (read 20261103 01:37 UTC)
7. https://github.com/EverMind-AI/EverOS/blob/main/docs/migration-to-1.0.0.md : 1.0.0 "fresh architecture" and the stack that is not part of it (read 20261103 01:30 UTC)
8. https://github.com/EverMind-AI/EverOS/blob/main/pyproject.toml : version 1.6.0, pinned `everalgo-*` packages (read 20261103 01:31 UTC)
9. https://github.com/EverMind-AI/EverOS/blob/main/docs/mcp.md : `everos-mcp` is a separate server and repository (read 20261103 01:30 UTC)
10. https://github.com/EverMind-AI/EverOS/blob/main/CHANGELOG.md : entries 1.0.0, 1.3.0 (Milvus), 1.3.1 (`llm_multiround`), 1.5.0 (`async_mode` matching EverOS Cloud), 1.6.0; the word "MemScene" does not occur (read 20261103 01:30 UTC)
11. https://github.com/EverMind-AI/EverOS/blob/main/docs/how-memory-works.md : storage layers, write path, Offline Memory Engine, cascade, consistency, rebuild; "MemScene" does not occur (read 20261103 01:30 UTC)
12. https://github.com/EverMind-AI/EverOS/blob/main/src/everos/infra/persistence/markdown/_base/writer.py and https://github.com/EverMind-AI/EverOS/blob/main/src/everos/infra/cascade/scanner.py : atomic rename; 30-second scan interval (read 20261103 01:36 UTC)
13. https://github.com/EverMind-AI/EverOS/blob/main/docs/configuration.md : `[index] backend` is `lancedb` or `milvus` (read 20261103 01:30 UTC)
14. https://github.com/EverMind-AI/EverOS/blob/main/docs/reflection.md : weekly schedule, off by default, "lossy LLM merge" (read 20261103 01:30 UTC)
15. https://github.com/EverMind-AI/EverOS/blob/main/docs/api.md : `SearchMethod` table (keyword, vector, hybrid, agentic); no mention of `llm_multiround` (read 20261103 01:41 UTC)
16. https://api.github.com/repos/EverMind-AI/EverAlgo : algorithm library, Apache-2.0 per GitHub metadata (read 20261103 01:31 UTC)
17. https://github.com/EverMind-AI/EverOS/blob/main/benchmarks/README.md : result table, protocol, micro accuracy; the file's history (commits API, path filter) shows the last change 20260908 (read 20261103 01:30 UTC; history 01:32 UTC)
18. https://github.com/EverMind-AI/EverOS/blob/main/benchmarks/configs/locomo.toml and https://github.com/EverMind-AI/EverOS/blob/main/benchmarks/configs/longmemeval.toml : extraction, decider, answer and judge models; top_k; decider comment (read 20261103 01:31 UTC)
19. https://api.github.com/repos/EverMind-AI/EverOS/releases?per_page=30 : 22 releases with dates (read 20261103 01:30 UTC); https://pypi.org/pypi/everos/json : PyPI 1.5.1 (read 20261103 01:30 UTC); tag `v1.6.0` lookup returns 404 (read 20261103 01:44 UTC)
20. https://api.github.com/repos/EverMind-AI/EverOS/commits?since=2026-08-04 : 73 commits, months, committers; head commit message of 20261030 (read 20261103 01:31 UTC)
21. https://api.github.com/repos/EverMind-AI/EverOS/contributors and https://api.github.com/search/issues : 9 contributors; 37 open pull requests and 29 open issues (read 20261103 01:31 UTC)
22. https://github.com/EverMind-AI/EverOS/blob/main/docs/overview.md and https://github.com/EverMind-AI/EverOS/blob/main/CITATION.md : v1.1.4 still named, "future v2", paper "coming soon" (read 20261103 01:30 UTC)
23. https://arxiv.org/abs/2601.02163 : Hu et al. (first three of 11), "EverMemOS: A Self-Organizing Memory Operating System for Structured Long-Horizon Reasoning", v1 20260105 (read 20261103 01:38 UTC); https://arxiv.org/html/2601.02163 : Tables 1 and 2, baselines, judges, affiliations (read 20261103 01:33 UTC); https://aclanthology.org/2026.acl-long.2125/ : ACL 2026 long paper, July 2026 (read 20261103 01:38 UTC)
24. https://arxiv.org/html/2610.30755 : Bao et al., Table 4, Appendix A and D.3.2 (EverMemOS run locally; published baseline scores retained) (read 20261103 01:33 UTC); abstract page https://arxiv.org/abs/2610.30755 (read 20261103 01:38 UTC)
25. https://arxiv.org/html/2608.13606 : MobileMem, Table 1, setup, judge; abstract page https://arxiv.org/abs/2608.13606, v1 20260811 (read 20261103 01:33 UTC; abstract 01:38 UTC)
26. https://github.com/MemTensor/OmniMemEval/blob/main/docs/user_memory/results.md : reproduced EverOS rows, setup, reference-score caveat; file history shows the last change 20261026 (read 20261103 01:39 UTC)
27. https://arxiv.org/html/2608.13334 : RippleMem, Table 2, EverMemOS 83.00 taken from prior work (read 20261103 01:33 UTC)
28. https://agentmemoryleaderboard.ai/results/cycle-1/ : cycle 1 results published 20260812, 123 results, no EverOS or EverMemOS entry (read 20261103 01:35 UTC)
29. [Mem0](mem0.md), [Hindsight](hindsight.md), [Basic Memory](basic-memory.md), [Tigerless agent-memory](tigerless-agent-memory.md) : stores and write paths of the neighbours, as those pages state them from their own sources (read 20261103 01:29 UTC)

Further reading in the archive: [EverOS entry](../../kb-kg/projects/everos.md). Papers: [agent memory group](../papers/agent-memory.md).
