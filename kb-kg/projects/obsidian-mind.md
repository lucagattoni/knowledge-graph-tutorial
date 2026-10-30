---
slug: obsidian-mind
repo: breferrari/obsidian-mind
tier: card
category: markdown-kb
snapshot: 20261030 19:43 UTC
---

# Obsidian Mind

| | |
|---|---|
| Repository | https://github.com/breferrari/obsidian-mind [1] |
| Licence | MIT, from the `LICENSE` file ("Copyright (c) 2026 Brenno Ferrari"; head read) [2]. The README badge and licence section say MIT, and so does the GitHub field: all agree [1][3]. |
| Language | TypeScript (GitHub primary language) [1] |
| Stars, forks | 5,460, 611 (20261030 19:42 UTC) [1]. The [landscape snapshot](../landscape/20261030_1913-github/repos.tsv) of 20261030 19:13 UTC shows 22.47 stars per day, 11.19 forks per 100 stars, 13 contributors, and no flag. |
| Created, last push | 20260228 21:41 UTC, 20261017 23:34 UTC [1] |
| Latest release | v10.0.0, 20261012 16:19 UTC; the newest 30 releases span v3.6.0 (20260407) to v10.0.0 [4] |
| Status | active (13 days since the last push); not archived [1] |
| Paper, docs | no paper stated; README, `ARCHITECTURE.md`, `CHANGELOG.md` [3][5][7] |

## What it is

Obsidian Mind is a template Obsidian vault that, in its own words, "gives AI coding agents persistent memory" [3]. It targets Claude Code (full support) and, with hooks and commands, Codex CLI and Gemini CLI [3]. The examples are work-oriented: stand-ups, 1:1 notes, incidents, decision records and a "brag doc" for performance reviews [3]. It installs with `shardmind install` or `git clone` [3]. No benchmark appears in the README. It reports one observation: a session with the vault's MCP server wired but no instruction in the calling repository made no vault calls and implemented a design the vault had recorded as rejected [3].

## How it works

Notes are Markdown with wikilinks in folders such as `brain/`, `work/`, `org/` and `perf/` [3]. Lifecycle hooks (SessionStart, UserPromptSubmit, PostToolUse, PreCompact, Stop) classify messages, validate frontmatter and links, and inject goals, active work and a file list under a byte budget; the agent writes the notes [3]. Optional QMD search runs three small local models (embedding, query expansion, reranking); without it the agent uses grep and the Obsidian CLI [3]. An `om` MCP server exposes tools including `search`, `expand`, `recall`, `remember`, `record_work`, `reason` and `health` to sessions in other repositories; `reason` calls a second Claude session [3].

## Status and direction

Active and fast-moving: at least 100 commits since 20260801 (one API page) [5]. v10.0.0 made `AGENTS.md` the single instruction file; October fixes cover Gemini, Windows and QMD handling [5]. One author has 237 of the listed contributions, the Actions bot 30, eleven others 1 to 7 [6]. 16 issues and 1 pull request are open [6]. The README's Roadmap section lists no items; it states that code pull requests are accepted only for assigned issues [3].

## Sources

1. https://github.com/breferrari/obsidian-mind : repository metadata via the GitHub API (read 20261030 19:42 UTC)
2. https://github.com/breferrari/obsidian-mind/blob/main/LICENSE : MIT text, head (read 20261030 19:43 UTC)
3. https://github.com/breferrari/obsidian-mind/blob/main/README.md : description, hooks, QMD, agents table, `om` MCP server, roadmap, licence section (read 20261030 19:42 UTC)
4. https://github.com/breferrari/obsidian-mind/releases : release list, v3.6.0 to v10.0.0 (read 20261030 19:42 UTC)
5. https://github.com/breferrari/obsidian-mind/blob/main/CHANGELOG.md : v10.0.0 and v9.1.0 entries; recent commit subjects (read 20261030 19:42 UTC)
6. https://github.com/breferrari/obsidian-mind/graphs/contributors : contributor counts and open issue and pull request counts via the API (read 20261030 19:42 UTC)
7. https://github.com/breferrari/obsidian-mind/tree/main : top-level listing, which shows `ARCHITECTURE.md` and `.mcp.json` (read 20261030 19:42 UTC)
