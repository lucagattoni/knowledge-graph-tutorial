---
type: project
repo: thedotmack/claude-mem
trends: [agent-memory]
updated: 20261102 23:17 UTC
---

# Claude-Mem

Claude-Mem is a memory plugin for coding agents: it records what an agent does, compresses it with a model, and feeds the result into later sessions. This page covers how it works, what has been measured and by whom, and how its licence and hosted parts fit together. Read on 20261102, 20:10 to 20:35 UTC, unless a source line says otherwise.

| Field | Value |
|---|---|
| Repository | https://github.com/thedotmack/claude-mem |
| Licence | Apache-2.0: GitHub classifies the `LICENSE` file as Apache License 2.0 [2]; the README and `docs/license.md` agree [4][5]. Open core: hosted cloud, team sync, admin and enterprise features, premium knowledge agents and managed evals are reserved outside the Apache code [5]. The file's history on GitHub shows earlier terms: a binary licence plus MIT hook files (20250906), then a compiled-form-only licence (20250909), then AGPL-3.0 (20250911 to 20260508), then Apache-2.0 [3]. |
| Trends | [Agent memory](../trends/agent-memory.md) |

## What it is

The repository describes it as "Persistent Context Across Sessions for Every Agent" [1]. It "Captures everything your agent does during sessions, compresses it with AI, and injects relevant context back into future sessions" [1]. Listed hosts include Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot and OpenCode [1][4]. What it stores are observations and session summaries; neither the README nor the architecture pages describe a graph [4][6].

## How it works

| Part | Behaviour | Source |
|---|---|---|
| Capture | Lifecycle hooks (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop, SessionEnd) pass tool use to a local worker service with an HTTP API and web viewer, run by Bun | [4] |
| Compression | The worker has a model turn tool events into observations, and at Stop a session summary. The model is the Claude Agent SDK, Gemini or OpenRouter; the user picks the hosted observer, an OpenRouter or Gemini key, or the Anthropic plan | [4][6] |
| Storage | SQLite with FTS5 full-text search; Chroma adds [hybrid search](../index/hybrid-search.md). SQLite holds current content, Chroma a search copy | [4][7] |
| Injection | At SessionStart a hook injects context from earlier sessions, with a configurable observation count | [6] |
| Search | Four [MCP](../index/model-context-protocol.md) (Model Context Protocol) tools. The pattern is three steps: `search` returns a compact index with IDs, `timeline` gives context around a hit, `get_observations` returns full detail for chosen IDs. The fourth tool, `important_workflow`, documents the pattern | [4][7] |

The README claims "~10x token savings" from filtering before fetching [4]. That is first-party, and the pages read give no measurement. The documented search path is an FTS5 query behind an HTTP endpoint with no model call of its own; whether the Chroma path calls one is unstated [7].

Hosted parts, per the README: a "claude-mem observer" with a 30-day free trial, after which memory falls back to the user's Anthropic plan unless they subscribe; Cloud Sync to cmem.ai; and an optional TeamBrain shared workspace [4].

## Evidence

No paper is stated [4]. A GitHub code search of the repository for "LoCoMo" and "LongMemEval" returned no files (not exhaustive) [9], and an arXiv search for the name returned no entries [16].

| Result | Who ran it | Source |
|---|---|---|
| Smart Explore, a tree-sitter code-exploration tool, against the standard Glob, Grep and Read agent: discovery about 14,200 against 252,500 tokens (17.8x); targeted reads about 5,650 against 109,400 (19.4x). Five queries on the project's own `src/`, Claude Opus 4.6; page added 20260226 | Project, first-party | [8] |
| Agent Memory Leaderboard (AML), cycle 1, Coding Memory, commercial division, share of 150 tasks solved: MemoraX v0.5 62.00%; claude-mem v12.1.1 52.00%; [MemOS](./memos.md) v2.0.1 52.00%; [Mem0](./mem0.md) API v3 51.33%; [Cognee](./cognee.md) v1.4.0 50.67%; Vectorize [Hindsight](./hindsight.md) Cloud v1.0.1 46.67% | A third-party platform; who submitted claude-mem's entry is unstated | [10][11] |

The AML README describes its Coding Memory track, in the Cycle 2 table, as "retrieval, filtering, and reuse of engineering experience from the same repository" [10]. It gives no separate definition of the Cycle 1 track, and its Cycle 2 text says each evaluation runs 150 base tasks under a "relevant" and a "noisy" history condition; which condition the Cycle 1 figures cover is unstated [10]. The README says cycle 1 leaderboards appeared 20260812 and the cycle 2 release is due in mid-November 2026 [10]. The entries carry the labels "Submitted (API)" (claude-mem) and "Evaluated" (MemOS, Mem0 API, Cognee); the README does not define them [10][11]. The Mem0 and Hindsight entries are named "Mem0 API" and "Vectorize Hindsight Cloud"; which code they ran is unstated.

*Reading:* Smart Explore tests code exploration, not memory recall. In the AML table, 52.00% of 150 is 78 tasks. Claude-mem, MemOS and one other entry tie at 78, and Mem0 API is one task behind, so this track does not separate them. The version tested is v12.1.1; the repository has since moved to v15 [12]. Neither result measures long-conversation recall, and the other data file in that folder lists no claude-mem entry [11].

## Status and direction

Active: pushed to within 90 days, not archived [1]. Latest release v15.9.0, 20261102 18:03 UTC, adds Devin support, a "Refresh now" button for the My Work view, a `CLAUDE_MEM_WORKER_URL` setting for remote workers, and more secret redaction [12]. Since 20260804: 1,479 commits and 82 releases [12][13]. The README states no roadmap [4].

The Apache-2.0 file arrived in the commit "Server-beta: Postgres storage + independent runtime + BullMQ queue (Phases 1–3)" (#2351) on 20260508. The first 900 characters of its message do not mention licensing [14]. `docs/license.md` gives the aim: broad embedding in developer tools, local agents and MCP clients [5].

**Hosted tier.** The project is open core and offers hosted memory on subscription; the "Grok Bot" install path defaults to "CMEM Pro, the hosted memory" [4][5].

**Attention.** The archive's snapshot of 20261030 19:13 UTC flagged fast star growth, a heuristic from stars over age (figures are in the watch-list table) [15]. The README includes a section on a token "created by a 3rd party but officially embraced by the creator" [4].

*Reading:* whether the stars are organic is unchecked here; the growth flag is a heuristic, not a verdict.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [agent-memory (Tigerless Labs)](tigerless-agent-memory.md)
- [memU](memu.md)
- [Projects](README.md)
- [TencentDB Agent Memory](tencentdb-agent-memory.md)

**Experiments**

- [X1: Snapshot distributions](../experiments/x1-snapshot-distributions.md)

**Index**

- [Agent memory](../index/agent-memory.md)

<!-- END GENERATED: appears-in -->

## Sources

Agent-memory papers as a field: [group page](../papers/agent-memory.md). Archive entry with longer notes: [kb-kg/projects/claude-mem.md](../../kb-kg/projects/claude-mem.md).

1. https://api.github.com/repos/thedotmack/claude-mem : description, hosts, not archived (read 20261102 20:10 UTC)
2. https://api.github.com/repos/thedotmack/claude-mem/license : GitHub's classification of `LICENSE` as Apache-2.0 (read 20261102 20:10 UTC)
3. https://api.github.com/repos/thedotmack/claude-mem/commits?path=LICENSE : five commits and the `LICENSE` text at each (read 20261102 20:12 UTC; the 20250906 and 20250909 texts re-read 20261102 20:35 UTC)
4. https://github.com/thedotmack/claude-mem/blob/main/README.md : hooks, worker, search tools, hosted parts, licence section, CMEM section (read 20261102 20:10 UTC)
5. https://github.com/thedotmack/claude-mem/blob/main/docs/license.md and https://github.com/thedotmack/claude-mem/blob/main/docs/ip-boundary.md : open-core boundary (read 20261102 20:11 UTC)
6. https://github.com/thedotmack/claude-mem/blob/main/docs/public/architecture/overview.mdx : components, data flow, injection (read 20261102 20:11 UTC)
7. https://github.com/thedotmack/claude-mem/blob/main/docs/public/architecture/search-architecture.mdx : search pipeline, SQLite and Chroma (read 20261102 20:11 UTC)
8. https://github.com/thedotmack/claude-mem/blob/main/docs/public/smart-explore-benchmark.mdx : first-party benchmark; commit 44a7b2fcb9 of 20260226 (read 20261102 20:13 UTC)
9. https://api.github.com/search/code?q=LoCoMo+repo:thedotmack/claude-mem : zero results, and the same for LongMemEval (read 20261102 20:13 UTC)
10. https://github.com/AML-memory/agent-memory-leaderboard : README, track description (Cycle 2 table and Cycle 2 text), cycle dates (read 20261102 20:13 UTC; re-read 20261102 20:34 UTC)
11. https://huggingface.co/spaces/agent-memory-leaderboard/leaderboard/blob/d01a32165aef2124b9732bd0fda7f79380b931dc/data/generated/code_leaderboard_data.json : scores, versions, labels, 150 tasks (read 20261102 20:14 UTC)
12. https://api.github.com/repos/thedotmack/claude-mem/releases : v15.9.0 and its notes; 82 releases since 20260804 (read 20261102 20:11 UTC)
13. https://api.github.com/repos/thedotmack/claude-mem/commits?since=2026-08-04T00:00:00Z : 1,479 commits by page count (read 20261102 20:10 UTC)
14. https://github.com/thedotmack/claude-mem/commit/36b0929fae : the commit that replaced `LICENSE` (read 20261102 20:12 UTC)
15. https://github.com/thedotmack/claude-mem : growth flag from the archive snapshot of 20261030 19:13 UTC (read 20261030 19:32 UTC, via the archive page kb-kg/projects/claude-mem.md)
16. https://export.arxiv.org/api/query?search_query=all:%22claude-mem%22 : no entries (read 20261102 20:10 UTC)
