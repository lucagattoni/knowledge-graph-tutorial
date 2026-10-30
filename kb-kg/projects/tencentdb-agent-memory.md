---
slug: tencentdb-agent-memory
repo: TencentCloud/TencentDB-Agent-Memory
tier: card
category: agent-memory
snapshot: 20261030 19:33 UTC
---

# TencentDB Agent Memory

| | |
|---|---|
| Repository | https://github.com/TencentCloud/TencentDB-Agent-Memory [1] |
| Licence | MIT, from the `LICENSE` file [2]. GitHub's detector reports `NOASSERTION` ("Other") [1]; the file is 26 lines, read in full. It opens with a preamble ("Copyright (C) 2026 Tencent. All rights reserved.", "licensed under the MIT") and then gives the MIT terms [2]. Operative terms: free use, copy, modify, merge, publish, distribute, sublicense and sell, without restriction; the one condition is that the copyright and permission notice stay in all copies or substantial portions; the software is provided "AS IS", with no warranty and no liability [2]. The README badge says MIT and links to the file, so they agree [3]. No other licence file is in the repository tree [9]. |
| Language | TypeScript (GitHub primary language) [1] |
| Stars, forks | 30,258, 2,934 (20261030 19:33 UTC; the landscape snapshot of 20261030 19:13 UTC has the same figures) [1] |
| Created, last push | 20260407 06:34 UTC, 20261028 14:33 UTC [1] |
| Latest release | v2.0.3, 20261026 14:09 UTC [1] |
| Status | active (pushed within 90 days); the snapshot sets no flag on this repository |
| Paper, docs | no paper stated; README, INSTALL.md, ROADMAP.md and API documents in the repository; documentation site https://tencentcloud.github.io/TencentDB-Agent-Memory/ (homepage field, not fetched) [1][3] |

## What it is

TencentDB Agent Memory describes itself as "a team-level memory hub for AI Agents" that turns conversations, documents and code into four memory assets: Chat Memory, Skill, LLM-Wiki and Code-Graph [1]. Several agents share one memory server through a proxy, which the README says needs no plugin, hook or MCP server; it lists DeepSeek Harness, Claude Code, Codex, CodeBuddy, WorkBuddy, Hermes and OpenClaw [3]. The README says its Wiki is "inspired by Karpathy's LLM knowledge base" [3]. Its only published result is a README table, the project's own claim: PersonaMem 48% without the system and 76% with it, labelled +59%; the figures shown give +58% (computed), and the table names no model, setup or run count [3]. This card did not look for an independent evaluation.

## How it works

Conversations are saved as L0, then refined asynchronously into L1 atoms (facts, preferences, events), L2 scenarios and L3 core/persona profiles [3]. Retrieval is layered: L2 and L3 give quick context, and BM25 plus vector retrieval with rank fusion fall back to L1 and L0, capped by item count, character budget and timeout [3]. Wiki builds pages with a link graph; CodeGraph indexes symbols, files and call relationships [3]. Agents use `/v3/tools/list` and `/v3/tools/call`, or the proxy [3]. Access is fixed binding plus ACL: private, team, restricted, agent [3]. Install needs two sets of LLM parameters, a memory group and a proxy group; which model does which job is unstated [3].

## Status and direction

Active: pushed 20261028 14:33 UTC; v2.0.3 released 20261026 14:09 UTC; 22 releases since v0.1.4 (20260423) and 33 contributors, anonymous excluded [1][4][7]. `ROADMAP.md` lists next items (admin-defined Agent templates, `mem:` Task commands, editable L1-L3 memories, L0/L1 search) but still names v2.0.1-beta.1 as current, behind the latest release [5]. Recent commits are panel, SDK and permission fixes [8].

## Sources

1. https://github.com/TencentCloud/TencentDB-Agent-Memory : repository metadata via the GitHub API (stars, forks, licence field, dates, description, latest release) (read 20261030 19:33 UTC)
2. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/main/LICENSE : full licence text (read 20261030 19:33 UTC)
3. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/main/README.md : description, installation, memory layers, access model, benchmark table, licence badge (read 20261030 19:33 UTC)
4. https://github.com/TencentCloud/TencentDB-Agent-Memory/releases : release list (22 entries, oldest v0.1.4 20260423) (read 20261030 19:33 UTC)
5. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/main/ROADMAP.md : next items and the stated current release (read 20261030 19:33 UTC)
6. https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/main/CHANGELOG.md : v2.0.3 entry dated 20261026 (read 20261030 19:33 UTC)
7. https://github.com/TencentCloud/TencentDB-Agent-Memory/graphs/contributors : contributor count via the contributors API (read 20261030 19:33 UTC)
8. https://github.com/TencentCloud/TencentDB-Agent-Memory/commits/main : recent commit subjects (read 20261030 19:33 UTC)
9. https://github.com/TencentCloud/TencentDB-Agent-Memory : repository tree listing, searched for licence and notice files (read 20261030 19:33 UTC)
