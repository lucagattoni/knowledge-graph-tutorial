---
type: project
repo: TencentCloud/TencentDB-Agent-Memory
trends: [agent-memory]
updated: 20261103 01:44 UTC
---

# TencentDB Agent Memory

This page answers what TencentDB Agent Memory is, how it stores memory and hands it to coding [agents](../index/agent.md), and who has measured it. The repository holds two product lines on two branches, so each claim names its branch [3][4][5]. Most scores are the project's own; one outside benchmark, MemDev-Bench, includes it [3][17][20].

| Field | Value |
|---|---|
| Repository | https://github.com/TencentCloud/TencentDB-Agent-Memory [1] |
| Licence | MIT, from the `LICENSE` file, identical on both branches [2][5]. GitHub reports `NOASSERTION` because the file swaps the "MIT License" heading for a Tencent preamble ("Copyright (C) 2026 Tencent. All rights reserved."); from "Permission is hereby granted" on it matches GitHub's MIT template (compared here) [2]. It is the only licence file in the tree [13]. Permissive: keep the notice. |
| Trends | [Agent memory](../trends/agent-memory.md) |

## What it is

The repository calls it "a team-level memory hub for AI Agents" that turns conversations, documents and code into four assets: Chat Memory, Skill, [LLM-Wiki](../index/llm-wiki.md) and [Code-Graph](../index/code-graph.md) [1]. A team gives each named agent its own loadout of assets, which have owners, versions and visibility [3].

The default branch, `feat/server_team`, holds the 2.x hub. Seven clients, among them Claude Code, Codex and OpenClaw, connect through a proxy and need no plugin, hook or [MCP](../index/model-context-protocol.md) (Model Context Protocol) server [3]. `main` holds the earlier plugin line for OpenClaw and Hermes; the branches share no common ancestor [4][5]. Releases follow the branches: `main` to v0.3.6, `feat/server` for v1.x, `feat/server_team` from v2.0.0-beta.1 (20260722) [6].

| Nearest page | How this project differs |
|---|---|
| [Mem0](./mem0.md) | Mem0 scopes by user, agent and run; here four layers are scoped by team, agent and user, with Skill, Wiki and code assets beside them [10][25] |
| [Hindsight](./hindsight.md) | Hindsight types memory by content; here layers run from raw text to persona; recall is similar (keyword, vector, rank fusion) [3][25] |
| [Claude-Mem](./claude-mem.md) | Captures through hooks and a local worker; here a proxy does [3][25] |

## How it works

Four services [9][10][11][12]. **MemoryCore** keeps memory and metadata in SQLite behind an HTTP gateway; extraction needs an OpenAI-compatible model, and recall defaults to [BM25](../index/bm25.md) with remote [embeddings](../index/embedding.md) off [10]. **MemoryKnowledge** builds the Wiki (a model extracts pages) and the Code-Graph (symbols, calls, files) [12]; the README says the latter "uses code from" [CodeGraph](./codegraph.md), MIT like this project [3][24]. **MemoryProxy** forwards OpenAI and Anthropic requests unchanged; per turn it injects Skills, Knowledge and L2/L3 memory, offers L0/L1 as read-only tools and writes the turn back [11]. Setup asks for two model settings, one for memory and one for the proxy's upstream [9].

**Layers.** L0 raw conversation, L1 atoms (facts, preferences, events), L2 scenarios, L3 persona, refined asynchronously. Recall starts at L2/L3; BM25, vector search and [reciprocal rank fusion](../index/reciprocal-rank-fusion.md) fall back to L1/L0, capped by items, characters and time [3].

**Access.** Visibility is private, team, restricted (user, role or agent ACL) or agent; "Fixed Binding + ACL" narrows scope before retrieval [3].

**Update and forget.** The default-branch README states no rule for replacing a stale fact: **unstated** [3]. The 2.0.1 changelog (Chinese; translation mine) adds memory search and overwrite-editing [7]. Storage is SQLite; MongoDB is experimental and off [9].

## Evidence

Every score is the authors' own unless marked independent; none was reproduced here.

**First-party, README.** One row, PersonaMem: 48% without, 76% with, labelled +59% (+58.3% computed); no model, run count or judge is named [3]. PersonaMem (Jiang et al., COLM 2025) tests whether a chatbot picks the response that fits a user's current profile [19]. A blog gives 589 questions and an agent-native-memory baseline; how the set was drawn is **unstated** [17]. The repository holds no harness for it and no LoCoMo or LongMemEval score, so nothing here sits beside the [LoCoMo](../datasets/locomo.md) or [LongMemEval](../datasets/longmemeval.md) figures on other pages [13][17][18].

**First-party, blog posts.** The docs site is script-rendered; I read two posts from its `gh-pages` scripts [16]. The post of 20260522 tests the plugin line's short-term compression: SWE-bench (500 tasks) 58.4% to 61.8-64.2% by offload model; run counts unstated [17]. The `main` README's SWE-bench row mixes two arms: success from one (64.2%), a token saving from another (33.09%; the first arm's own is 31.63%) [4][17]. The post of 20260818 tests the team hub: related-task SWE-bench cases 60% to 80%; the 50 hardest cases 17% to 20% passed, cost $887.64 to $717.78 (17% of 50 is not a whole number of tasks). It says sample counts and confidence intervals are still to be reported [18].

**Independent.** MemDev-Bench (Chen et al.; Southeast University, SUSTech, MemoraX AI; arXiv 20261020) runs Claude Code with DeepSeek-V4-Flash on a SWE-bench Verified subset, its only setup. Its Appendix F ranks 29 rows on 150 tasks, one run each, against NoMem, a no-memory baseline (three-run mean, 47.78% resolved). TencentDB Agent Memory scores 51.33%, 4th with five ties; a "4o-mini" variant 49.33%, its change **unstated**. The top is 52.67%; 22 of 29 rows beat NoMem; input tokens 5.86M against 5.92M. The version tested is **unstated** [20].

*Reading:* one task is 0.67 points here and the nine leading rows span two tasks, so this shows a gain of about 3.6 points over no memory, not a ranking.

No other independent evaluation found (searched 20261103): an arXiv search for the name returned no entries [21]. Two blog code reviews ran no benchmark; one is by a competing service's maker, as it states [22][23].

## Status and direction

*Release.* `v2.0.3`, 20261026 14:09 UTC, is GitHub's latest of 22 releases, the first v0.1.4 (20260423) [6].

*Activity.* 70 commits to the default branch from 20260805 to 20261103 (20 in August from the 5th, 27, 23; none in November), the last on 20261028; 33 contributors, anonymous excluded [14][15].

*Documents lag.* The README says "Current release is v2.0.0"; ROADMAP names v2.0.1-beta.1 and lists next items that the 2.0.1 entry (20260825) appears to cover; Cursor support is not in the changelog [3][7][8]. 2.0.3-beta.1 added a pluggable decision service and on-demand skill choice, both off by default [7].

*Reading:* active and permissively licensed. Its quality evidence is first-party and on benchmarks unlike the rest of the chapter; the one outside run shows a small gain, level with the leading group.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)

**Projects**

- [Projects](README.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory : description, homepage, default branch `feat/server_team`, creation date, last push, licence field NOASSERTION, not archived (read 20261103 01:30 UTC)
2. https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory/license : `LICENSE` text and GitHub's classification; compared with https://api.github.com/licenses/mit (read 20261103 01:37 UTC); file sha equal on both branches via the contents endpoint with `ref` (read 20261103 01:30 UTC)
3. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/README.md : default-branch README: assets, clients, layers, access, PersonaMem table, acknowledgements, "Current release is v2.0.0" (read 20261103 01:30 UTC)
4. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/main/README.md : `main` README: plugin line, four-row benchmark table, dedup setting (read 20261103 01:30 UTC)
5. https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory/branches : branches and last commits; https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory/compare/main...feat/server_team returns "No common ancestor"; `LICENSE` history of both branches via the commits endpoint with `path` (read 20261103 01:30 and 01:37 UTC)
6. https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory/releases?per_page=100 : 22 releases, dates, target branches, latest v2.0.3 (read 20261103 01:30 UTC)
7. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/CHANGELOG.md : entries 2.0.0 to 2.0.3, in Chinese (read 20261103 01:30 UTC)
8. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/ROADMAP.md : "Current release: v2.0.1-beta.1" and the next-release list (read 20261103 01:30 UTC)
9. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/INSTALL.md : two model groups, containers, ports, SQLite default, experimental MongoDB (read 20261103 01:31 UTC)
10. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/MemoryCore/README.md : SQLite, BM25 default, embeddings off, model requirement, v3 isolation ids (read 20261103 01:31 UTC)
11. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/MemoryProxy/README.md : proxy pipeline, injection, tools, write-back (read 20261103 01:31 UTC)
12. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/MemoryKnowledge/README.md : Wiki and Code-Graph engines, in Chinese (read 20261103 01:31 UTC)
13. https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory/git/trees/feat%2Fserver_team?recursive=1 : 1,576 entries, one licence file, no benchmark harness (read 20261103 01:31 UTC); https://api.github.com/search/code with queries PersonaMem, LoCoMo and LongMemEval on this repository (two README files; none; none), default branch only and not exhaustive (read 20261103 01:32 and 01:40 UTC)
14. https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory/commits?sha=feat/server_team&since=2026-08-05T00:00:00Z : 70 commits, monthly counts, last date (read 20261103 01:31 UTC)
15. https://api.github.com/repos/TencentCloud/TencentDB-Agent-Memory/contributors?anon=0 : 33 contributors (read 20261103 01:30 UTC)
16. https://tencentcloud.github.io/TencentDB-Agent-Memory/ : documentation site; a plain fetch returned only the title (read 20261103 01:30 UTC); blog list from `assets/BlogListPage-CJbHEJCY.js` on the `gh-pages` branch (read 20261103 01:33 UTC)
17. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/gh-pages/assets/MermaidCanvasContextOffloadPage-WYcFjBb6.js : post of 20260522, route `/community/blog/mermaid-canvas-context-offload`, benchmark tables and text, in Chinese (read 20261103 01:34 UTC)
18. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/gh-pages/assets/TeamMemoryPracticePage-CKPE3qxD.js : post of 20260818, route `/community/blog/team-memory-practice`, SWE-bench results and caveats, in Chinese (read 20261103 01:34 UTC)
19. https://arxiv.org/abs/2504.14225 : Jiang et al., "Know Me, Respond to Me: Benchmarking LLMs for Dynamic User Profiling and Personalized Responses at Scale", COLM 2025, v1 20250419 (read 20261103 01:33 UTC)
20. https://arxiv.org/abs/2610.27524 : Chen et al., "MemDev-Bench", abstract; full text https://arxiv.org/html/2610.27524v1: setup, Appendix F Table 9, reference to the repository (read 20261103 01:36 UTC)
21. https://export.arxiv.org/api/query?search_query=all:%22TencentDB-Agent-Memory%22+OR+all:%22TencentDB+Agent+Memory%22 : zero results; same for all:%22TencentDB%22+AND+all:memory (read 20261103 01:33 UTC)
22. https://www.maximem.ai/blog/tencentdb-agent-memory-review : code review of commit `badbd21`, 20261013, no benchmark of its own; its company sells a competing service (read 20261103 01:32 UTC)
23. https://wavect.io/blog/tencentdb-agent-memory-sqlite-review/ : review of 20261030 reading commits `a3c2d860` and `ecc01a54`; no deployment measurements (read 20261103 01:32 UTC)
24. https://api.github.com/repos/colbymchenry/codegraph/license : MIT (read 20261103 01:37 UTC)
25. ./mem0.md, ./hindsight.md, ./openviking.md, ./memos.md, ./claude-mem.md : the neighbouring project pages, for the comparison table (read 20261103 01:36 UTC)

Further reading in the archive: [TencentDB Agent Memory, short entry](../../kb-kg/projects/tencentdb-agent-memory.md). Papers: [agent memory group](../papers/agent-memory.md).
