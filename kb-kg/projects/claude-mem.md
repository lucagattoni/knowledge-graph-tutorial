---
slug: claude-mem
repo: thedotmack/claude-mem
tier: card
category: agent-memory
snapshot: 20261030 19:32 UTC
---

# Claude-Mem

| | |
|---|---|
| Repository | https://github.com/thedotmack/claude-mem [1] |
| Licence | Apache-2.0, from the `LICENSE` file (Apache License 2.0 text) [2]. The README badge, the README licence section and `NOTICE` agree [3][4]. It is open core: `docs/license.md` and `docs/ip-boundary.md` say the hosted cloud, team sync, admin and enterprise features, premium knowledge agents and managed evals are reserved outside the Apache-2.0 code [5][6]. `ragtime/LICENSE` is also Apache 2.0 text [7]. |
| Language | TypeScript (GitHub primary language) [1] |
| Stars, forks | 105,952, 9,337 (20261030 19:31 UTC; the landscape snapshot of 20261030 19:13 UTC has 105,932 and 9,334) [1] |
| Created, last push | 20250831 20:50 UTC, 20261030 19:01 UTC [1] |
| Latest release | v15.7.0, 20261030 18:18 UTC [1] |
| Status | active (pushed within 90 days). Snapshot flag `fast-growth`: 249.84 stars a day over 424 days. The flag is a heuristic from stars over age. Evidence read here, none of which settles whether the stars are organic: 9,337 forks per 105,952 stars is 8.81 per 100 (computed); 300 contributors, anonymous excluded [8]; 2,320 issues of which 2,268 are closed, and 1,548 merged pull requests [9]; 381 releases, the oldest listed v3.5.4 on 20250909, nine days after creation (computed) [10]. The README carries a Trendshift badge, a star-history chart and sponsor logos, and has no launch explanation, benchmark or paper [3]. It also has a section saying a token named CMEM was "created by a 3rd party but officially embraced by the creator", acting as a "community catalyst for growth"; the token was not checked [3]. Stargazer timestamps could not be read (the endpoint returned 404), so the growth curve is unchecked. |
| Paper, docs | docs.claude-mem.ai (linked from the README, not fetched); no paper stated [3] |

## What it is

Claude-Mem is a memory plugin for coding agents. It captures what an agent does during a session, compresses it with AI (the repository's words), and injects relevant context into later sessions [1][3]. The README calls it "built for Claude Code"; the repository description lists Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot and OpenCode as hosts [1][3]. The data it stores is a log of observations and summaries; the README describes no graph [3]. The README also offers hosted parts: a "claude-mem observer" with a 30-day free trial, Cloud Sync to cmem.ai, and an optional TeamBrain shared workspace [3].

## How it works

Lifecycle hooks (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop, SessionEnd) capture tool use [3]. A local worker service, run by Bun, serves an HTTP API and a web viewer [3]. Observations and semantic summaries are stored in SQLite with FTS5 search, and a Chroma vector store adds hybrid semantic and keyword search [3]. Agents search through MCP tools in three steps: `search` returns a compact index, `timeline` gives surrounding context, `get_observations` returns full detail for chosen IDs [3]. The user picks the memory provider: the hosted claude-mem observer, their own OpenRouter or Gemini key, or the Anthropic plan [3]. LLM use at query time: unstated.

## Status and direction

Active: pushed 20261030 19:01 UTC; v15.7.0 released 20261030 18:18 UTC [1]. 381 releases and 1,400 commits since 20260801 (both computed from list pagination) [10][11]. The README states no roadmap [3]. The latest commits are security fixes, a "My Work" fix and a change of the default note-taking model to the newest Haiku [11].

## Sources

1. https://github.com/thedotmack/claude-mem : repository metadata via the GitHub API (stars, forks, licence field, dates, description, latest release) (read 20261030 19:31 UTC)
2. https://github.com/thedotmack/claude-mem/blob/main/LICENSE : Apache License 2.0 text (read 20261030 19:31 UTC)
3. https://github.com/thedotmack/claude-mem/blob/main/README.md : description, install paths, hooks, search tools, hosted parts, licence section, CMEM section (read 20261030 19:31 UTC)
4. https://github.com/thedotmack/claude-mem/blob/main/NOTICE : Apache-2.0 notice (read 20261030 19:31 UTC)
5. https://github.com/thedotmack/claude-mem/blob/main/docs/license.md : licence scope and reserved commercial areas (read 20261030 19:31 UTC)
6. https://github.com/thedotmack/claude-mem/blob/main/docs/ip-boundary.md : open-core boundary (read 20261030 19:32 UTC)
7. https://github.com/thedotmack/claude-mem/blob/main/ragtime/LICENSE : licence of the `ragtime/` directory (read 20261030 19:32 UTC)
8. https://github.com/thedotmack/claude-mem/graphs/contributors : contributor count via the contributors API (read 20261030 19:31 UTC)
9. https://github.com/thedotmack/claude-mem/issues : issue and pull request counts via the search API (read 20261030 19:32 UTC)
10. https://github.com/thedotmack/claude-mem/releases : release list, count and oldest tag (read 20261030 19:32 UTC)
11. https://github.com/thedotmack/claude-mem/commits/main : recent commit subjects and the count since 20260801 (read 20261030 19:32 UTC)
