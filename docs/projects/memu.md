---
type: project
repo: NevaMind-AI/memU
trends: [agent-memory]
updated: 20261103 02:20 UTC
---

# memU

This page answers what memU is today, how its [agent memory](../index/agent-memory.md) path works, and what has been measured. In mid-2026 the project replaced a model-driven pipeline with an embedding-only service beside desktop coding agents; every score found describes the earlier pipeline [4][5][14][16][25].

| Field | Value |
|---|---|
| Repository | https://github.com/NevaMind-AI/memU [1] |
| Licence | Apache-2.0 text, edited. The file is `LICENSE.txt`; no file named `LICENSE` exists [2]. Section 2 (copyright grant) is replaced by MIT-style words ("use, reproduce, modify, merge, publish, distribute, sublicense, and/or sell copies") with an MIT-style notice condition; sections 1, 4 and 9 differ in wording; the patent grant and the disclaimers (3, 5 to 8) match Apache 2.0; the appendix gives way to "Copyright 2024 MemU Team" [3]. No copyleft, non-commercial or field-of-use clause found; legal effect not assessed. GitHub reports NOASSERTION [1]; the README says Apache-2.0 [4]. |
| Trends | [Agent memory](../trends/agent-memory.md) |

## What it is

memU calls itself "a lightweight, agent-driven memory system that gives users a shared LLM wiki across sessions, agents, and devices" [4]. In practice it is a sidecar for desktop coding agents such as Codex and Claude Code: it reads their session logs, has the host agent write Markdown memories and skills, and returns matches before the agent answers [4]. It runs locally (SQLite or Postgres, plus an [embedding](../index/embedding.md) key) or against hosted MemU Cloud. The repository holds a client for the hosted API and no server code [4][6][7]; what the hosted side does with a query is **unstated**, so the model-free claims below describe the local service.

## How it works

**Record.** A scheduled task slices each host's new session logs into jobs. The host agent chooses to do nothing, patch a file or create one, for memories and for skills (Markdown workflows) [4][8]. `commit` embeds and stores the changed files, writing nothing if embedding fails [5].

**Read.** A standing line in the host's instruction file ([AGENTS.md](../index/agents-md.md) and similar) tells the agent to run a retrieve command before answering; hosts get at most five hits [4]. Retrieval embeds the query once, ranks segments (one per memory line, one per skill) and resources by [vector](../index/vector-search.md) similarity, rolls hits up to files and calls no model; the docstring says "No LLM is involved anywhere" [4][5]. The backend is authoritative; the Markdown folders are temporary working copies [8].

**What leaves the machine.** Embedding requests go to the chosen provider, OpenAI by default [4]; in cloud mode, queries and committed memory files go to the hosted API [6]. Two more channels are on by default in the code at `main` (commit `bca3512`, 20261030) and in the PyPI wheels of `memu-cli` 0.9.0 to 0.11.0b3 [12][13][30]. The CLI was not run here; what the servers receive or keep is **unstated**.

- *Instruction refresh.* The scheduled `prepare` run rewrites the retrieval procedure installed in the host's instruction file from the copy at `memu.pro/sdk/instructions`, and fetches job templates there at most daily; host install guides come from `memu.pro/sdk/docs`. Fetched text is checked only for non-emptiness, placeholders and size. At 20261103 02:16 UTC the template and guide URLs tried returned 404, so the embedded text applies. Off: an empty `MEMU_TEMPLATE_BASE_URL` or `MEMU_DOCS_BASE_URL`, read from the process environment only; the event switches below do not apply [13].
- *Event reporting.* Each `retrieve`, run by the agent every turn, posts one event to `api.memu.so/api/memu/analytics/events`; other events are spooled and sent by later commands. An event holds its name, a random client id, version, OS, host, mode, session id when offered, and counts and latencies. The docstring says "What leaves the machine is counts, never content", but the allowlist also admits an agent-written error report of up to 5,000 characters and, after a crash, the exception type with `module:function:line` frames; a cloud API key, if set, goes in the header. Off: `MEMU_TELEMETRY=0` (file or environment), `DO_NOT_TRACK=1` (environment only) or an empty `MEMU_EVENTS_BASE_URL` [12].

**Before the rewrite.** Release 1.x built items and categories with a model and retrieved with intention routing and sufficiency checks [9][14][24][25]; the current tree has no `llm` or `vlm` package [7]. ADR 0007 (Proposed) describes [BM25](../index/bm25.md) hybrid retrieval; the code has none [9][10][11].

*Against the chapter.* [Claude-Mem](./claude-mem.md) is closest in intent (overlapping hosts); with [Mem0](./mem0.md) it calls a model to turn input into stored memory. memU's service never does; the host agent decides [5][8][29]. In [Letta](./letta.md) the agent edits its own memory; memU's agent is an outside host [29].

## Evidence

**First-party, historical.** The v1.5.1 README (20260323) claimed "92.09% average accuracy" on [LoCoMo](../benchmarks/locomo.md) and linked `memU-experiment` [14][15]. Its `result.json` records 1,420 correct of 1,542 scored questions; the file's own total is 1,986 and 444 were skipped, which leaves out almost all of the adversarial category, as LoCoMo papers usually do (1,540 questions in [23][25]). Answers came from a deployment named `gpt-4.1-mini-2` over memory built earlier by a model that is **unstated**. The [judge](../index/llm-as-judge.md) is not recorded; `locomo_test.py` hard-codes a grader deployment `gpt-4.1`, but its commit is titled "clean: code", so whether that run used it is **unstated**. The grading prompt accepts an answer that "touches on the same topic as the gold answer" [15]. The current README gives no benchmark, and the project's results page says the figure "should not be read as a benchmark of the current architecture" [4][16].

**Third-party runs.** Four papers ran MemU, each by authors who present a method or system of their own, so none is a neutral test. None ran the current service: two predate the new design (the workspace design's first decision record is ADR 0004, dated 20260622) [9], Cai et al. built memory with a model [24], Bao et al. ran 1.5.1 [25].

| Paper (first version) | MemU version | MemU result | Authors' own, same order |
|---|---|---|---|
| MemOS, 2507.03724 (20250704) [22] | **unstated** | LoCoMo 56.55 (overall LLM-judge); [LongMemEval](../benchmarks/longmemeval.md) 38.4; GPT-4o-mini | 75.80; 77.8 |
| EverMemOS, 2601.02163 (20260105) [23] | **unstated**; official API | LoCoMo 61.15 (GPT-4o-mini), 66.67 (GPT-4.1-mini); LongMemEval 38.40, taken from the MemOS results | LoCoMo 86.76; 93.05; LongMemEval 83.00 |
| Cai et al., 2609.33226 (20260927) [24] | **unstated**; memory built with GPT-4.1-mini | LongMemEval 64.20 (GPT-5-nano response model), 71.60 (GPT-5-mini) | 80.6; 90.6 |
| Bao et al., 2610.30755 (20261022) [25] | 1.5.1, defaults | [MemoryAgentBench](../benchmarks/memoryagentbench.md) 26.12; MEME (memory updates) 19.87; GPT-4o-mini; lowest of seven memory systems on both, and again with a second reader (28.27; 18.80) | Raw-RAG, the authors' reference method: 48.32; 39.30 |

Later tables copy cells. T-Mem takes MemU's LoCoMo numbers from the MemOS paper [26]; MindMemOS takes its MemU cells from the EverMemOS paper [32]; Bao et al.'s Table 3 repeats the EverMemOS paper's MemU cells digit for digit (compared here), so only their MEME and MemoryAgentBench cells are new MemU runs [23][25].

**None found:** a run of the current service, or by a party with no system of its own. MemU is absent from the Agent Memory Leaderboard's README and its cycle-1 textual and coding data (cycle 2 results are due in mid-November 2026), and from twelve other memory papers, among them MemoryAgentBench's and Memory Tax (searched 20261103) [28]. EverMind's blog (byline 20251126) says it benchmarked MemU but shows no per-system scores [27].

## Status and direction

*Release.* GitHub's latest release is `v1.5.1` (20260323), the earlier pipeline, last on PyPI as `memu-py` 1.5.1; the newest is the pre-release `v2.0.0-beta.0` (20260723) [17][18]. PyPI `memu-cli` is numbered apart: 0.10.0 (20260805) is its latest stable release and 0.11.0b3 (20260821) its latest pre-release, both older than the October commits; `main` reads 0.11.0-beta.3 [11][18][19][21].

*Code against docs.* The CHANGELOG stops at 2.0.0-beta.0 and lists an LLM gateway and a VLM package (#442) that `src/memu` no longer has; six of 20 decision records are still Proposed [7][9][20]. Event reporting is on by default while ADR 0016 is Proposed and says its disclosure is "still unwritten". A search of the repository's Markdown, the hosted `memu.pro/SKILL.md` and the privacy policy found no mention of this channel beyond that ADR, and the Claude Code install guide says of `report install` that "nothing leaves the machine here" although the command flushes the spool [10][12][31].

*Activity.* Not archived [1]. Commits through 20261030 add Codex prompt retrieval, score cutoffs, a five-hit cap and a pi adapter [21]. Roadmap file: **unstated** [7].

*Reading:* a published score can outlive its system: the 92.09% belongs to a pipeline the project has replaced and now labels historical [14][16]. The new design leaves the write policy to the host agent and keeps the service model-free (on [5][8]), which should make writes cheap and tie memory quality to the host model's judgment; no measurement of that was found [28]. The Markdown form resembles [plain files as agent knowledge](../trends/plain-file-knowledge.md), but the backend holds the truth [8].

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)

**Projects**

- [Projects](README.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/NevaMind-AI/memU : description, archived flag, GitHub licence field NOASSERTION; and https://api.github.com/repos/NevaMind-AI/memU/commits/main : head commit `bca3512` of 20261030 07:56 UTC (read 20261103 02:03 UTC)
2. https://api.github.com/repos/NevaMind-AI/memU/contents/ : root listing: `LICENSE.txt` present, no file named `LICENSE` (read 20261103 02:03 UTC)
3. https://github.com/NevaMind-AI/memU/blob/main/LICENSE.txt : licence text, compared line by line (whitespace ignored) with the standard text at https://api.github.com/licenses/apache-2.0: section 2 replaced and a notice condition added; wording changes in sections 1, 4(c) and 9; sections 3 and 5 to 8 identical; appendix replaced by "Copyright 2024 MemU Team" and the standard notice (read 20261103 02:03 UTC)
4. https://github.com/NevaMind-AI/memU/blob/main/README.md : self-description, hosts, record and inject seams, five hits, storage and embedding defaults, licence line, no benchmark, no mention of events or telemetry (read 20261103 02:03 UTC)
5. https://github.com/NevaMind-AI/memU/blob/main/src/memu/app/service.py and https://github.com/NevaMind-AI/memU/blob/main/src/memu/app/agentic.py : embedding-only service, `progressive_retrieve`, `commit_results`, segment rules (read 20261103 02:04 UTC)
6. https://github.com/NevaMind-AI/memU/blob/main/src/memu/cloud.py and https://github.com/NevaMind-AI/memU/blob/main/docs/adr/0012-cloud-backed-agentic-backend.md : client for the hosted v4 API; search and commit requests carry the query and the recall files (read 20261103 02:04 UTC)
7. https://api.github.com/repos/NevaMind-AI/memU/git/trees/main?recursive=1 : file tree: no server code, no `llm` or `vlm` package under `src/memu`, no roadmap file (read 20261103 02:03 UTC)
8. https://github.com/NevaMind-AI/memU/blob/main/docs/developer.md : agent creates, patches or leaves files; backend authoritative, `memory/` and `skill/` temporary copies (read 20261103 02:04 UTC)
9. https://github.com/NevaMind-AI/memU/blob/main/docs/adr/0007-three-independent-memory-lines-wiki-graph.md : status Proposed (20260701), hybrid embedding and BM25 proposal, earlier retrieval with intention routing and sufficiency checks (read 20261103 02:04 UTC); and the Status and Date lines of all 20 files under https://github.com/NevaMind-AI/memU/tree/main/docs/adr (ADR 0004 dated 20260622; six Proposed; 0019 and 0020 without a status line) (read 20261103 02:05 UTC)
10. https://codeload.github.com/NevaMind-AI/memU/tar.gz/refs/heads/main : text search of the tarball at `main`: "bm25" found in three files, ADR 0007, ADR 0008, `CHANGELOG.md`; "telemetry" or `DO_NOT_TRACK` in Markdown only in ADR 0016 (read 20261103 02:04 UTC)
11. https://github.com/NevaMind-AI/memU/blob/main/pyproject.toml : version 0.11.0-beta.3; seven dependencies, none a BM25 library; console scripts `memu` and the host binaries (read 20261103 02:03 UTC)
12. https://github.com/NevaMind-AI/memU/blob/main/src/memu/events.py : default endpoint, `enabled()`, allowed properties, envelope fields, headers; https://github.com/NevaMind-AI/memU/blob/main/src/memu/hosts/retrieval.py (`retrieve` posts its event inline) and https://github.com/NevaMind-AI/memU/blob/main/src/memu/hosts/host_cli.py (`report`, error handler, flush after `prepare`); https://github.com/NevaMind-AI/memU/blob/main/docs/adr/0016-client-event-reporting.md : status Proposed, "ships opt-out", disclosure "still unwritten"; https://github.com/NevaMind-AI/memU/blob/main/src/memu/hosts/claude_code/INSTALL.md : "nothing leaves the machine here" (read 20261103 02:04 to 02:08 UTC)
13. https://github.com/NevaMind-AI/memU/blob/main/src/memu/hosts/templates.py, https://github.com/NevaMind-AI/memU/blob/main/src/memu/hosts/instruction.py (`refresh`), `_refresh_retrieval` in `host_cli.py`, and https://github.com/NevaMind-AI/memU/blob/main/docs/adr/0013-self-updating-instruction-templates.md (status Accepted): default URLs, validation, once-a-day cooldown, switches; and GET probes of `https://memu.pro/sdk/instructions/<name>.txt` for the four template names and of `https://memu.pro/sdk/docs/<host>/INSTALL.md` for two hosts, all HTTP 404 (read 20261103 02:05 UTC; probes 02:16 UTC)
14. https://github.com/NevaMind-AI/memU/blob/v1.5.1/README.md : the "92.09% average accuracy" claim, category and item store, `llm_profiles`, link to `memU-experiment` (read 20261103 02:07 UTC)
15. https://github.com/NevaMind-AI/memU-experiment : `result.json` (summary: 1,986 questions, 1,420 correct, category totals sum to 1,542; args `gpt-4.1-mini-2`; 272 sessions skipped), `locomo_test.py` (grader deployment `gpt-4.1`), `evaluate_agent.py` grading prompt; commits "clean: code" (20251121 12:04 UTC) and "add: result" (20251121 12:08 UTC); repository created 20251121 (read 20261103 02:07 to 02:09 UTC)
16. https://memu.pro/benchmark : "historical benchmark" notice (read 20261103 02:07 UTC)
17. https://api.github.com/repos/NevaMind-AI/memU/releases and `/releases/latest` : `v1.5.1` latest, `v2.0.0-beta.0` pre-release, dates (read 20261103 02:06 UTC)
18. https://pypi.org/pypi/memu-cli/json and https://pypi.org/pypi/memu-py/json : version lists and upload dates (read 20261103 02:06 UTC)
19. https://github.com/NevaMind-AI/memU/blob/main/.github/workflows/publish-memu-cli.yml : `memu-cli` versions independently of the release train (read 20261103 02:04 UTC)
20. https://github.com/NevaMind-AI/memU/blob/main/CHANGELOG.md : 2.0.0-beta.0 entry, "multi-provider LLM gateway, modular preprocessing, and VLM package" (#442) (read 20261103 02:03 UTC)
21. https://api.github.com/repos/NevaMind-AI/memU/commits?since=2026-08-05 : subjects; latest commit 20261030 07:56 UTC (read 20261103 02:06 UTC)
22. https://arxiv.org/abs/2507.03724 and https://arxiv.org/html/2507.03724 : Li, Xi, Li and 38 more, "MemOS: A Memory OS for AI System", first version 20250704, latest version (v4, 20251203) read; Tables 3 and 4 (LLM-judge scores), GPT-4o-mini backbone, no MemU version given (read 20261103 02:09 UTC)
23. https://arxiv.org/abs/2601.02163 and https://arxiv.org/html/2601.02163 : Hu, Gao, Zhou and 8 more, "EverMemOS: A Self-Organizing Memory Operating System for Structured Long-Horizon Reasoning", 20260105; Tables 1 and 2, baseline setup (official APIs), LongMemEval baselines "from the official MemOS results" (read 20261103 02:09 UTC)
24. https://arxiv.org/abs/2609.33226 and https://arxiv.org/html/2609.33226 : Cai, Deng, Wang and 2 more, "Beyond Memory Construction: Rethinking Memory Access for LLM-based Conversational Agents", 20260927; Table 1, appendix E (MemU run with GPT-4.1-mini as construction model) (read 20261103 02:09 UTC)
25. https://arxiv.org/abs/2610.30755 and https://arxiv.org/html/2610.30755 : Bao, Zhang, Zhang and 3 more, "Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought", 20261022; Tables 3 and 4, section 4.1, appendix D.3.6 (MemU 1.5.1) (read 20261103 02:09 UTC)
26. https://arxiv.org/abs/2606.15405 and https://arxiv.org/html/2606.15405 : "T-Mem: Memory That Anticipates, Not Archives", Table 2 caption (MemU numbers taken from Li et al. 2025) (read 20261103 02:09 UTC)
27. https://evermind.ai/blogs/a-unified-evaluation-framework-for-ai-memory-systems : five systems named, GPT-4.1-mini, no per-system scores in the text, byline 20251126 (read 20261103 02:14 UTC)
28. Searches for "MemU": arXiv HTML full text of 2507.05257 (MemoryAgentBench), 2606.24775, 2608.15008, 2610.34073 (Memory Tax), 2609.22231, 2610.27524, 2608.12888 (no match, read 20261103 02:12 UTC), and 2607.16211, 2602.14038, 2606.14571, 2606.06054, 2510.17281 (no match, read 20261103 02:20 UTC); https://github.com/AML-memory/agent-memory-leaderboard README (no match; "Official leaderboard release: Mid-November 2026") and the files `data/generated/leaderboard_data.json` and `code_leaderboard_data.json` of https://huggingface.co/spaces/agent-memory-leaderboard/leaderboard, last modified 20260818 (64 and 58 system names, no match) (read 20261103 02:11 UTC); web searches for papers with MemU as a baseline, used as leads only: they led to source 32 (read 20261103 02:12 UTC); https://export.arxiv.org/api/query (`all:MemU`: one unrelated 2021 paper) (read 20261103 01:34 UTC, not repeated)
29. The pages [Mem0](./mem0.md), [Claude-Mem](./claude-mem.md) and [Letta](./letta.md) of this documentation, for what each project states about its write and read paths and hosts (read 20261103 02:15 UTC)
30. https://pypi.org/pypi/memu-cli/json (wheel files) : wheels of 0.9.0, 0.10.0 and 0.11.0b3 unpacked and searched: `memu/events.py` with the same default endpoint and `MEMU_TELEMETRY` default; `memu/hosts/templates.py` with the same default URLs; `retrieval.py` posting events inline in 0.10.0 and 0.11.0b3; no `llm` or `vlm` directory; entry points include `memu-codex` and `memu-claude-code` (read 20261103 02:07 UTC)
31. https://memu.pro/SKILL.md and https://memu.pro/privacy-policy : searched for "telemetry", "analytics", `DO_NOT_TRACK`; the SKILL.md has none, the policy mentions "Usage Data" and analytics in general terms and does not name the CLI (read 20261103 02:16 UTC)
32. https://arxiv.org/abs/2608.12428 and https://arxiv.org/html/2608.12428 : "MindMemOS: A Portable and Self-Evolving Memory Operating Layer for AI Agents", 20260812; baseline results "cited from the EverOS paper" (read 20261103 02:12 UTC)

Further reading in the archive: [memU entry](../../kb-kg/projects/memu.md). Papers: [agent memory group](../papers/agent-memory.md).
