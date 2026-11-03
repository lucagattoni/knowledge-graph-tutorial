---
type: project
repo: TencentCloud/TencentDB-Agent-Memory
trends: [agent-memory]
updated: 20261103 02:15 UTC
---

# TencentDB Agent Memory

This page answers what TencentDB Agent Memory is, how it stores memory and hands it to coding [agents](../index/agent.md), and who has measured it. The repository holds two product lines on two branches, so each claim names its branch [3][4][5]. Most scores are the project's own; one outside benchmark, MemDev-Bench, includes it [3][17][20].

| Field | Value |
|---|---|
| Repository | https://github.com/TencentCloud/TencentDB-Agent-Memory [1] |
| Licence | MIT, from the `LICENSE` file, identical on `main`, `feat/server` and `feat/server_team`; it says "TencentDB Agent Memory is licensed under the MIT." [2][5]. GitHub reports `NOASSERTION`: a Tencent preamble replaces the "MIT License" title, though from "Permission is hereby granted" on the text equals GitHub's MIT template (compared here) [2]; *Reading:* the header probably explains it. The only licence file in the tree [13]. Keep the copyright and permission notice. |
| Trends | [Agent memory](../trends/agent-memory.md) |

## What it is

The repository calls it "a team-level memory hub for AI Agents" that turns conversations, documents and code into four assets: Chat Memory, Skill, [LLM-Wiki](../index/llm-wiki.md) and [Code-Graph](../index/code-graph.md) [1]. A team gives each named agent its own loadout of assets, which have owners, versions and visibility [3].

The default branch, `feat/server_team`, holds the 2.x hub. Its README shows seven clients, among them Claude Code, Codex and OpenClaw, that connect through a proxy and need no plugin, hook or [MCP](../index/model-context-protocol.md) (Model Context Protocol) server; INSTALL.md lists nine, adding OpenCode and Pi, and Pi uses a `pi-plugin` extension [3][9]. `main` holds the earlier plugin line for OpenClaw and Hermes; the branches share no common ancestor [4][5]. Releases follow the branches: `main` to v0.3.6, `feat/server` for v1.x, `feat/server_team` from v2.0.0-beta.1 (20260722) [6].

| Nearest page | How this project differs |
|---|---|
| [Mem0](./mem0.md) | Mem0 scopes by user, agent and run; here four layers are scoped by team, agent and user, with Skill, Wiki and code assets beside them [10][25] |
| [Hindsight](./hindsight.md) | Hindsight types memory by content; here layers run from raw text to persona; recall is similar (keyword, vector, rank fusion) [3][25] |
| [Claude-Mem](./claude-mem.md) | Captures through hooks and a local worker; here a proxy does [3][25] |

## How it works

Four services run in three containers; the hub image holds the Panel (web UI) and the Knowledge service [7][9][12]. **MemoryCore** keeps memory and metadata in SQLite behind an HTTP gateway; extraction needs an OpenAI-compatible model, and recall defaults to [BM25](../index/bm25.md) with remote [embeddings](../index/embedding.md) off [10]. **MemoryKnowledge** builds the Wiki (a model extracts pages) and the Code-Graph (symbols, calls, files) [12]; the README says the latter "uses code from" [CodeGraph](./codegraph.md), MIT like this project [3][24]. **MemoryProxy** forwards OpenAI and Anthropic requests unchanged; per turn it injects Skills, Knowledge and L2/L3 memory, offers L0/L1 as read-only tools and writes the turn back [11]. Setup asks for two model settings, one for memory and one for the proxy's upstream [9].

**Layers.** L0 raw conversation, L1 atoms (facts, preferences, events), L2 scenarios, L3 persona, refined asynchronously. Recall starts at L2/L3; BM25, vector search and [reciprocal rank fusion](../index/reciprocal-rank-fusion.md) fall back to L1/L0, capped by items, characters and time [3].

**Access.** Visibility is private, team, restricted (user, role or agent ACL) or agent; "Fixed Binding + ACL" narrows scope before retrieval [3].

**Update and forget.** The default-branch README states no rule for replacing a stale fact [3], but the code has one, on by default [4][26]: a model compares each new L1 memory with recalled candidates and picks store, skip, update or merge; update overwrites older records when the new fact is more specific, later or a correction (prompt in Chinese; translation mine) [26]. Age-based forgetting: **unstated** (none found in the READMEs or file names). The 2.0.1 changelog (Chinese; translation mine) adds memory search and overwrite-editing [7]. Storage is SQLite; MongoDB is experimental and off [9].

## Evidence

Every score is the authors' own unless marked independent; none was reproduced here.

**First-party, README.** One row, PersonaMem: 48% without, 76% with, labelled +59% (+58.3% computed); no model, run count or judge is named [3]. The README cites no paper; the name matches PersonaMem (Jiang et al., COLM 2025), a four-choice test of whether a chatbot picks the response that fits a user's current profile [19]. A blog gives 589 questions and a baseline of the agent's native memory below 48% (translation mine), which would explain the +59%; how the set was drawn is **unstated** [17]. The repository holds no harness for it and no LoCoMo or LongMemEval score, so nothing here sits beside the [LoCoMo](../datasets/locomo.md) or [LongMemEval](../datasets/longmemeval.md) figures on other pages [13][17][18].

**First-party, blog posts.** The docs site is script-rendered; I read its three posts from the `gh-pages` scripts [16]. The post of 20260522 tests the plugin line's short-term compression in chained multi-task sessions and says its scores are not comparable with public leaderboards [17]. SWE-bench (500 tasks): 58.4% to 61.8-64.2% by offload model; run counts unstated [17]. The `main` README repeats its headline figures but its SWE-bench row mixes two arms: success and tokens from one (64.2%, 2375.4M), the saving from another (33.09%; the first arm's own is 31.63%) [4][17]. For WideSearch the README gives 33% to 50%, while the post's text gives 8.5% to 12% for the same Opus arm; the headline's basis is **unstated** [4][17]. The post of 20260818 tests the team hub: related-task SWE-bench cases 60% to 80% (case count unstated); the 50 hardest cases 17% to 20% passed, cost $887.64 to $717.78 (17% of 50 is not a whole number of tasks). It says sample counts and confidence intervals are still to be reported [18]. A third post (20260121) gives one internal recall figure, about 45% to 88%, with no setup [28].

**Independent.** MemDev-Bench (Chen et al.; Southeast University, SUSTech, MemoraX AI; arXiv 20261020) runs Claude Code with DeepSeek-V4-Flash on a SWE-bench Verified subset, its only setup. Its Appendix F ranks 29 rows on 150 tasks, one run each, against NoMem, a no-memory baseline (three-run mean, 47.78% resolved, SD 1.54). TencentDB Agent Memory scores 51.33%, 4th after tie-breaks, level with five rows including Hindsight; a "4o-mini" variant scores 49.33%, its change **unstated**. The top is 52.67%; 22 of 29 rows beat NoMem; input tokens 5.86M against 5.92M, steps 184.7 against 176.9. The version is **unstated**; the reference says only "Accessed: 2026-08-24", when v2.0.0 was the latest stable release [6][20].

*Reading:* one task is 0.67 points and the nine leading rows span two tasks, so this shows a gain of about 3.6 points over no memory, not a ranking. Each memory row is one run; NoMem's spread over three was 1.54 points, this system's is unmeasured.

No other independent evaluation found (searched 20261103: the arXiv API for the name, which would miss a full-text mention, and the web [21]). Three blog posts ran no benchmark of it: two by makers of competing projects, one by a services firm [22][23][27]. The competing service's review says the PersonaMem figures cannot be reproduced from the repository [22].

## Status and direction

*Release.* `v2.0.3`, 20261026 14:09 UTC, is GitHub's latest of 22 releases, the first v0.1.4 (20260423) [6].

*Activity.* 76 commits to the default branch, 20260722 to 20261028; 70 in the 90 days from 20260805 (20 in August, 27 in September, 23 in October; none in November); 33 contributors, anonymous excluded [14][15].

*Documents lag.* The README says "Current release is v2.0.0" and shows seven clients; ROADMAP names v2.0.1-beta.1 and lists next items that the 2.0.1 entry (20260825) appears to cover; Cursor support is not in the changelog [3][7][8][9]. 2.0.3-beta.1 added a pluggable decision service and on-demand skill choice, both off by default [7].

*Reading:* active and permissively licensed. Its quality evidence is first-party, on PersonaMem and SWE-bench rather than the LoCoMo and LongMemEval used elsewhere in the chapter; the one outside run shows a small gain, within the two-task spread of the leading rows.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)

**Projects**

- [Projects](README.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory : description, homepage, default branch `feat/server_team`, creation date, last push, licence field NOASSERTION, not archived (read 20261103 01:30 UTC)
2. https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory/license : `LICENSE` text and GitHub's classification; compared with https://api.github.com/licenses/mit (read 20261103 01:37 UTC); file sha equal on `main`, `feat/server` and `feat/server_team` via the contents endpoint with `ref` (read 20261103 01:30 UTC)
3. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/README.md : default-branch README: assets, clients, layers, access, PersonaMem table, acknowledgements, "Current release is v2.0.0" (read 20261103 01:30 UTC)
4. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/main/README.md : `main` README: plugin line, four-row benchmark table, dedup setting (read 20261103 01:30 UTC)
5. https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory/branches : branches and last commits; https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory/compare/main...feat/server_team returns "No common ancestor"; `LICENSE` history of both branches via the commits endpoint with `path` (read 20261103 01:30 and 01:37 UTC)
6. https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory/releases?per_page=100 : 22 releases, dates, target branches, latest v2.0.3 (read 20261103 01:30 UTC)
7. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/CHANGELOG.md : entries 2.0.0 to 2.0.3, in Chinese (read 20261103 01:30 UTC)
8. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/ROADMAP.md : "Current release: v2.0.1-beta.1" and the next-release list (read 20261103 01:30 UTC)
9. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/INSTALL.md : two model groups, three containers and four ports, nine agent clients (OpenCode and Pi beyond the README's seven; Pi via `pi-plugin`), SQLite default, experimental MongoDB (read 20261103 01:31 UTC)
10. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/MemoryCore/README.md : SQLite, BM25 default, embeddings off, model requirement, v3 isolation ids (read 20261103 01:31 UTC)
11. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/MemoryProxy/README.md : proxy pipeline, injection, tools, write-back (read 20261103 01:31 UTC)
12. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/MemoryKnowledge/README.md : Wiki and Code-Graph engines, in Chinese (read 20261103 01:31 UTC)
13. https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory/git/trees/feat%2Fserver_team?recursive=1 : 1,576 entries, one licence file, no benchmark harness (read 20261103 01:31 UTC); the `main` tree (216 entries) likewise (read 20261103 02:05 UTC); https://api.github.com/search/code with queries PersonaMem, LoCoMo and LongMemEval on this repository (two README files; none; none), default branch only and not exhaustive (read 20261103 01:32 and 01:40 UTC)
14. https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory/commits?sha=feat/server_team&since=2026-08-05T00:00:00Z : 70 commits, monthly counts, last date (read 20261103 01:31 UTC); the same call without `since`: 76 commits, first 20260722 (read 20261103 02:08 UTC)
15. https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory/contributors?anon=0 : 33 contributors (read 20261103 01:30 UTC)
16. https://tencentcloud.github.io/TencentDB-Agent-Memory/ : documentation site; a plain fetch returned only the title (read 20261103 01:30 UTC); blog list (three posts) from `assets/BlogListPage-CJbHEJCY.js` on the `gh-pages` branch (read 20261103 01:33 UTC)
17. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/gh-pages/assets/MermaidCanvasContextOffloadPage-WYcFjBb6.js : post of 20260522, route `/community/blog/mermaid-canvas-context-offload`, benchmark tables and text (SWE-bench, Toolathlon, WideSearch, AA-LCR, PersonaMem), in Chinese (read 20261103 01:34 UTC)
18. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/gh-pages/assets/TeamMemoryPracticePage-CKPE3qxD.js : post of 20260818, route `/community/blog/team-memory-practice`, SWE-bench results and caveats, in Chinese (read 20261103 01:34 UTC)
19. https://arxiv.org/abs/2504.14225 : Jiang et al., "Know Me, Respond to Me: Benchmarking LLMs for Dynamic User Profiling and Personalized Responses at Scale", COLM 2025 (arXiv comment field), v1 20250419 (read 20261103 01:33 UTC); four-choice format from the full text https://arxiv.org/html/2504.14225v2 (read 20261103 02:08 UTC)
20. https://arxiv.org/abs/2610.27524 : Chen et al., "MemDev-Bench: Does Memory Help Code Agents? Benchmarking Memory Systems over Real Repository Histories", v1 20261020, abstract; full text https://arxiv.org/html/2610.27524v1: affiliations, setup and single-configuration limitation, Appendix F Table 9 (29 rows, 150 tasks, one run each, NoMem three runs), reference "Accessed: 2026-08-24" (read 20261103 01:36 UTC; Table 9 re-read 20261103 02:06 UTC)
21. https://export.arxiv.org/api/query?search_query=all:%22TencentDB-Agent-Memory%22+OR+all:%22TencentDB+Agent+Memory%22 : zero results; same for all:%22TencentDB%22+AND+all:memory (read 20261103 01:33 UTC); repeated with all:%22TencentDB%22 and abs:%22Agent+Memory%22+AND+abs:Tencent, zero results (read 20261103 02:09 UTC); web searches for the name with LoCoMo, LongMemEval, "independent" and Chinese keywords surfaced no evaluation (read 20261103 02:09 UTC)
22. https://www.maximem.ai/blog/tencentdb-agent-memory-review : code review of commit `badbd21`, 20261013 (update note 20261028), reads the code and runs no benchmark of this project (it reports scores for its own product), says the PersonaMem figures cannot be reproduced from the repository; its company sells a competing service (read 20261103 01:32 UTC; re-read 20261103 02:12 UTC)
23. https://wavect.io/blog/tencentdb-agent-memory-sqlite-review/ : review of 20261030 reading commits `a3c2d860` and `ecc01a54`; no deployment measurements (read 20261103 01:32 UTC)
24. https://api.github.com/repos/colbymchenry/codegraph/license : MIT (read 20261103 01:37 UTC)
25. ./mem0.md, ./hindsight.md, ./claude-mem.md : the neighbouring project pages, for the comparison table (read 20261103 01:36 UTC)
26. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/MemoryCore/src/core/record/l1-dedup.ts : L1 conflict detection (store, skip, update, merge; skipped without a search backend); with `MemoryCore/src/core/prompts/l1-dedup.ts` (the prompt, in Chinese), `MemoryCore/src/config.ts` (`enableDedup` default true), `MemoryCore/src/core/record/l1-extractor.ts` (the call) and `deploy/global-images/start-memory-core.sh` (sets it true) (read 20261103 02:10 UTC)
27. https://dev.to/_24569b2abcc8f3fa4c094/nylonme-vs-tencentdb-agent-memory-a-collision-of-two-memory-philosophies-1ekc : comparison by the apparent maker of a competing project (NylonME); no benchmark of TencentDB Agent Memory, says Tencent published no LoCoMo result (read 20261103 02:09 UTC)
28. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/gh-pages/assets/ContextEngineeringEntropyPage-BYspGjm1.js : post of 20260121, route `/community/blog/context-engineering-entropy`, one internal recall figure, in Chinese (read 20261103 02:08 UTC)

Re-checked against the sources by a second reader, 20261103 02:02 to 02:15 UTC: numbers, quotations, code and branch claims, and the paper tables.

Further reading in the archive: [TencentDB Agent Memory, short entry](../../kb-kg/projects/tencentdb-agent-memory.md). Papers: [agent memory group](../papers/agent-memory.md).
