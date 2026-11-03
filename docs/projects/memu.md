---
type: project
repo: NevaMind-AI/memU
trends: [agent-memory]
updated: 20261103 01:45 UTC
---

# memU

This page answers what memU is today, how its [agent memory](../index/agent-memory.md) path works, and what has been measured. In mid-2026 the project replaced a model-driven pipeline with an embedding-only service beside desktop coding agents; every score found describes the earlier pipeline [4][5][14][16][25].

| Field | Value |
|---|---|
| Repository | https://github.com/NevaMind-AI/memU [1] |
| Licence | Apache-2.0 text, edited. The file is `LICENSE.txt`; no file named `LICENSE` exists [2]. Section 2 (copyright grant) is replaced by MIT-style words ("use, reproduce, modify, merge, publish, distribute, sublicense, and/or sell copies"); the patent grant, redistribution terms and disclaimers read as in Apache 2.0 [3]. No copyleft, non-commercial or field-of-use clause found; legal effect not assessed. GitHub reports NOASSERTION [1]; the README says Apache-2.0 [4]. |
| Trends | [Agent memory](../trends/agent-memory.md) |

## What it is

memU calls itself "a lightweight, agent-driven memory system that gives users a shared LLM wiki across sessions, agents, and devices" [4]. In practice it is a sidecar for desktop coding agents such as Codex and Claude Code: it reads their session logs, has the host agent write Markdown memories and skills, and returns matches before the agent answers [4]. It runs locally (SQLite or Postgres, plus an [embedding](../index/embedding.md) key) or against hosted MemU Cloud; the repository holds a client for the hosted API, and no server code appears in its file tree [4][6][7].

## How it works

**Record.** A scheduled task slices each host's new session logs into jobs. The host agent chooses to do nothing, patch a file or create one, for memories and for skills (Markdown workflows) [4][8]. `commit` embeds and stores the changed files, writing nothing if embedding fails [5].

**Read.** A standing line in the host's instruction file ([AGENTS.md](../index/agents-md.md) and similar) tells the agent to run a retrieve command before answering; hosts get at most five hits [4]. Retrieval embeds the query once, ranks segments (one per memory line) and resources by [vector](../index/vector-search.md) similarity, rolls hits up to files and calls no model; the docstring says "No LLM is involved anywhere" [4][5]. The backend is authoritative; the Markdown folders are temporary working copies [8].

**What leaves the machine.** Embedding requests go to the chosen provider, OpenAI by default [4]. By default the SDK also refreshes its agent-instruction templates from memu.pro and sends usage events to a memU endpoint (counts only, per its docstring; not audited here). Switches: an empty `MEMU_TEMPLATE_BASE_URL`, `MEMU_TELEMETRY=0`, `DO_NOT_TRACK=1` [12][13].

**Before the rewrite.** Release 1.x built items and categories with a model and retrieved with intention routing and sufficiency checks [9][14][24][25]; the current tree has no `llm` or `vlm` package [7]. ADR 0007 (Proposed) describes [BM25](../index/bm25.md) hybrid retrieval; the code has none [9][10][11].

*Against the chapter.* [Claude-Mem](./claude-mem.md) is closest in intent (the same hosts); with [Mem0](./mem0.md) it calls a model to turn input into stored memory. memU's service never does; the host agent decides [5][8][29]. In [Letta](./letta.md) the agent edits its own memory; memU's agent is an outside host [29].

## Evidence

**First-party, historical.** The v1.5.1 README (20260323) claimed "92.09% average accuracy" on [LoCoMo](../benchmarks/locomo.md) and linked `memU-experiment` [14][15]. Its `result.json` records 1,420 correct of 1,542 scored questions, answered with `gpt-4.1-mini`. The [judge](../index/llm-as-judge.md) model is **unstated**; the repository's grading prompt accepts an answer that "touches on the same topic as the gold answer" [15]. The current README gives no benchmark, and the project's results page says the figure "should not be read as a benchmark of the current architecture" [4][16].

**Third-party runs.** Four papers ran MemU, each by authors with a system of their own, so none is a neutral test. None ran the current service: two predate the new design (its decision records start with ADR 0004, dated 20260622) [9], Cai et al. built memory with a model [24], Bao et al. ran 1.5.1 [25].

| Paper (first version) | MemU version | MemU result | Authors' own system, same order |
|---|---|---|---|
| MemOS, 2507.03724 (20250704) [22] | **unstated** | LoCoMo 56.55; [LongMemEval](../benchmarks/longmemeval.md) 38.4; GPT-4o-mini | 75.80; 77.8 |
| EverMemOS, 2601.02163 (20260105) [23] | **unstated**; official API | LoCoMo 61.15 (GPT-4o-mini), 66.67 (GPT-4.1-mini); LongMemEval 38.40, copied from the MemOS leaderboard | LoCoMo 86.76; 93.05 |
| Cai et al., 2609.33226 (20260927) [24] | **unstated** | LongMemEval 64.20 (GPT-5-nano), 71.60 (GPT-5-mini) | 80.6; 90.6 |
| Bao et al., 2610.30755 (20261022) [25] | 1.5.1, defaults | [MemoryAgentBench](../benchmarks/memoryagentbench.md) 26.12; MEME (memory updates) 19.87; GPT-4o-mini; lowest memory system on both, with both readers | 48.32; 39.30 |

Later tables copy cells. T-Mem takes MemU's LoCoMo numbers from the MemOS paper [26]; Bao et al.'s Table 3 repeats the EverMemOS paper's MemU cells digit for digit (compared here), so only their MEME and MemoryAgentBench cells are new runs [23][25].

**None found:** a run of the current service, or by a party with no system of its own. MemU is absent from the Agent Memory Leaderboard's README and coding-track data, and from seven other memory papers, among them MemoryAgentBench's and Memory Tax (searched 20261103) [28]. EverMind's blog (byline 20251126) says it benchmarked MemU but shows no per-system scores [27].

## Status and direction

*Release.* GitHub's latest release is `v1.5.1` (20260323), the earlier pipeline; the newest is the pre-release `v2.0.0-beta.0` (20260723) [17]. PyPI `memu-cli` is numbered apart: 0.10.0 (20260805) is its latest stable release and 0.11.0b3 (20260821) its latest pre-release; `main` reads 0.11.0-beta.3 [11][18][19].

*Code against docs.* The CHANGELOG stops at 2.0.0-beta.0 and lists a model gateway (#442) that `src/memu` no longer has; six of 20 decision records are still Proposed [7][9][20].

*Activity.* Not archived [1]. Commits through 20261030 add Codex prompt retrieval, score cutoffs, a five-hit cap and a pi adapter [21]. Roadmap file: **unstated** [7].

*Reading:* a published score can outlive its system: the 92.09% belongs to a pipeline the project has replaced and now labels historical [14][16]. The new design leaves the write policy to the host agent and keeps the service model-free, which makes writes cheap and ties memory quality to the host model's judgment; no measurement of that was found [28]. The Markdown form resembles [plain files as agent knowledge](../trends/plain-file-knowledge.md), but the backend holds the truth [8].

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)

**Projects**

- [Projects](README.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/NevaMind-AI/memU : description, archived flag, GitHub licence field NOASSERTION (read 20261103 01:30 UTC)
2. https://api.github.com/repos/NevaMind-AI/memU/contents/ : root listing: `LICENSE.txt` present, no file named `LICENSE` (read 20261103 01:30 UTC)
3. https://github.com/NevaMind-AI/memU/blob/main/LICENSE.txt : licence text, compared word by word with the standard text at https://api.github.com/licenses/apache-2.0 (read 20261103 01:30 UTC)
4. https://github.com/NevaMind-AI/memU/blob/main/README.md : self-description, hosts, record and inject seams, five hits, storage and embedding defaults, licence line, no benchmark (read 20261103 01:30 UTC)
5. https://github.com/NevaMind-AI/memU/blob/main/src/memu/app/service.py and https://github.com/NevaMind-AI/memU/blob/main/src/memu/app/agentic.py : embedding-only service, `progressive_retrieve`, `commit_results`, segment rules (read 20261103 01:33 UTC)
6. https://github.com/NevaMind-AI/memU/blob/main/src/memu/cloud.py and https://github.com/NevaMind-AI/memU/blob/main/docs/adr/0012-cloud-backed-agentic-backend.md : client for the hosted v4 API (read 20261103 01:33 UTC)
7. https://api.github.com/repos/NevaMind-AI/memU/git/trees/main?recursive=1 : file tree: no server code, no `llm` or `vlm` package under `src/memu`, no roadmap file (read 20261103 01:32 UTC)
8. https://github.com/NevaMind-AI/memU/blob/main/docs/developer.md : agent creates, patches or leaves files; backend authoritative, `memory/` and `skill/` temporary copies (read 20261103 01:41 UTC)
9. https://github.com/NevaMind-AI/memU/blob/main/docs/adr/0007-three-independent-memory-lines-wiki-graph.md : status Proposed (20260701), hybrid embedding and BM25 proposal, earlier retrieval with intention routing and sufficiency checks (read 20261103 01:32 UTC); and the Status and Date lines of all 20 files under https://github.com/NevaMind-AI/memU/tree/main/docs/adr (ADR 0004 dated 20260622; six Proposed; 0019 and 0020 without a status line) (read 20261103 01:40 UTC)
10. https://api.github.com/search/code?q=bm25+repo:NevaMind-AI/memU : "bm25" found in three files: ADR 0007, ADR 0008, `CHANGELOG.md` (read 20261103 01:32 UTC)
11. https://github.com/NevaMind-AI/memU/blob/main/pyproject.toml : version 0.11.0-beta.3; seven dependencies, none a BM25 library (read 20261103 01:30 UTC)
12. https://github.com/NevaMind-AI/memU/blob/main/src/memu/events.py : event reporting on by default, counts-only claim, switches; with https://github.com/NevaMind-AI/memU/blob/main/docs/adr/0016-client-event-reporting.md, status Proposed (read 20261103 01:41 UTC)
13. https://github.com/NevaMind-AI/memU/blob/main/src/memu/hosts/templates.py and https://github.com/NevaMind-AI/memU/blob/main/docs/adr/0013-self-updating-instruction-templates.md : template refresh from memu.pro, switch, status Accepted (read 20261103 01:41 UTC)
14. https://github.com/NevaMind-AI/memU/blob/v1.5.1/README.md : the "92.09% average accuracy" claim, category and item store, link to `memU-experiment` (read 20261103 01:31 UTC)
15. https://github.com/NevaMind-AI/memU-experiment : `result.json` (1,420 of 1,542 scored questions, `gpt-4.1-mini`), `evaluate_agent.py` grading prompt; created 20251121 (read 20261103 01:32 UTC)
16. https://memu.pro/benchmark : "historical benchmark" notice (read 20261103 01:38 UTC)
17. https://api.github.com/repos/NevaMind-AI/memU/releases : `v1.5.1` latest, `v2.0.0-beta.0` pre-release, dates (read 20261103 01:30 UTC; again 01:43 UTC)
18. https://pypi.org/pypi/memu-cli/json and https://pypi.org/pypi/memu-py/json : version lists and upload dates (read 20261103 01:31 UTC)
19. https://github.com/NevaMind-AI/memU/blob/main/.github/workflows/publish-memu-cli.yml : `memu-cli` versions independently of the release train (read 20261103 01:33 UTC)
20. https://github.com/NevaMind-AI/memU/blob/main/CHANGELOG.md : 2.0.0-beta.0 entry, gateway item #442 (read 20261103 01:31 UTC)
21. https://api.github.com/repos/NevaMind-AI/memU/commits?since=2026-08-05 : subjects; latest commit 20261030 07:56 UTC (read 20261103 01:33 UTC; head re-read 01:43 UTC)
22. https://arxiv.org/abs/2507.03724 and https://arxiv.org/html/2507.03724 : Li, Xi, Li and 38 more, "MemOS: A Memory OS for AI System", first version 20250704, latest version (v4, 20251203) read; Tables 3 and 4, GPT-4o-mini backbone, no MemU version given (read 20261103 01:36 UTC)
23. https://arxiv.org/abs/2601.02163 : Hu, Gao, Zhou and 8 more, "EverMemOS: A Self-Organizing Memory Operating System for Structured Long-Horizon Reasoning", 20260105; Table 1, baseline setup, LongMemEval from the MemOS leaderboard (read 20261103 01:38 to 01:40 UTC)
24. https://arxiv.org/abs/2609.33226 : Cai, Deng, Wang and 2 more, "Beyond Memory Construction: Rethinking Memory Access for LLM-based Conversational Agents", 20260927; Table 1, MemU set-up (read 20261103 01:37 UTC)
25. https://arxiv.org/abs/2610.30755 : Bao, Zhang, Zhang and 3 more, "Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought", 20261022; Tables 3 and 4, appendix D.3.6 (MemU 1.5.1) (read 20261103 01:37 UTC)
26. https://arxiv.org/abs/2606.15405 : "T-Mem: Memory That Anticipates, Not Archives", Table 2 caption (MemU numbers taken from Li et al. 2025) (read 20261103 01:34 UTC)
27. https://evermind.ai/blogs/a-unified-evaluation-framework-for-ai-memory-systems : five systems named, GPT-4.1-mini, no per-system scores in the text, byline 20251126 (read 20261103 01:44 UTC)
28. Searches for "MemU": https://export.arxiv.org/api/query (`all:MemU`: one unrelated 2021 paper); arXiv HTML full text of 2507.05257 (MemoryAgentBench), 2606.24775, 2608.15008, 2610.34073 (Memory Tax), 2609.22231, 2610.27524, 2608.12888 (no match); https://github.com/AML-memory/agent-memory-leaderboard README and its coding-track data file (no match) (read 20261103 01:34 to 01:39 UTC)
29. The pages [Mem0](./mem0.md), [Claude-Mem](./claude-mem.md) and [Letta](./letta.md) of this documentation, for what each project states about its write and read paths (read 20261103 01:46 UTC)

Further reading in the archive: [memU entry](../../kb-kg/projects/memu.md). Papers: [agent memory group](../papers/agent-memory.md).
