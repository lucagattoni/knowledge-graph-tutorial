---
slug: claude-obsidian
repo: AgriciDaniel/claude-obsidian
tier: card
category: markdown-kb
snapshot: 20261030 19:42 UTC
---

# claude-obsidian

| | |
|---|---|
| Repository | https://github.com/AgriciDaniel/claude-obsidian [1] |
| Licence | MIT, from the `LICENSE` file ("Copyright (c) 2026 AgriciDaniel (AI Marketing Hub)"; head read) [2]. The README badge and the GitHub field also say MIT, so all three agree [1][3]. |
| Language | Python (GitHub primary language) [1] |
| Stars, forks | 16,002, 1,579 (20261030 19:41 UTC) [1]. The [landscape snapshot](../landscape/20261030_1913-github/repos.tsv) of 20261030 19:13 UTC shows 77.68 stars per day, 9.87 forks per 100 stars and no flag (heuristics). Other evidence: 10 contributors listed, the author with 295 contributions, an account named `claude` 46, eight others 1 or 2 [8]; the README has a "Trending Repository of the Day" badge and a section asking readers for a star [3]. I draw no conclusion on how the stars arose. |
| Created, last push | 20260407 08:59 UTC, 20261025 22:24 UTC [1] |
| Latest release | v3.0.1, 20261021 18:06 UTC [4] |
| Status | active (5 days since the last push); not archived [1] |
| Paper, docs | no paper stated; README, `CHANGELOG.md` and a `docs/` directory with 13 guides [3][5][7] |

## What it is

claude-obsidian is a Claude Code plugin, also packaged as Agent Skills for other hosts, that turns sources dropped into a folder into a vault of linked, cited Markdown notes for Obsidian [3]. The README says it follows Andrej Karpathy's "LLM Wiki pattern": the AI maintains a wiki a person can read [3]. It is not an Obsidian community plugin, and Obsidian is optional [3]. The README says the vault is plain Markdown on the user's computer with "no cloud database, no lock-in, no telemetry"; the notes Claude reads go to Claude, as in any Claude Code session [3].

## How it works

The plugin has 15 skills and 3 read-only agents [3]. Sources go to `inbox/`; originals are kept as content-addressed copies; Claude writes linked pages with claims tied to sources [3]. The "graph" is the links between notes, shown by Obsidian's Graph view; no graph database is mentioned [3]. Writes pass one transaction layer: a SHA-256 hash per note read, one plan, one apply, a rollback journal [3]. Search is local BM25 over page chunks, with optional reranking only with consent [6]. The README names no MCP server; PDFs and EPUBs get metadata only: the README says "no built-in text extraction yet" [3].

## Status and direction

Active. 13 releases from v1.1 (20260408) to v3.0.1, and at least 100 commits since 20260801 (one API page) [4][5]. v3.0.0 was a "hardening release"; v3.0.1, the same day, restored the plugin name `claude-obsidian` [5]. `[Unreleased]` is empty and no roadmap is stated [5]. Open: 17 issues, 7 pull requests [8]. No benchmark is published; a `bench` command measures search on the user's own queries [3][7].

## Sources

1. https://github.com/AgriciDaniel/claude-obsidian : repository metadata via the GitHub API (read 20261030 19:41 UTC)
2. https://github.com/AgriciDaniel/claude-obsidian/blob/main/LICENSE : MIT text, head (read 20261030 19:41 UTC)
3. https://github.com/AgriciDaniel/claude-obsidian/blob/main/README.md : description, install, skills, agents, safety, limits, FAQ (read 20261030 19:42 UTC)
4. https://github.com/AgriciDaniel/claude-obsidian/releases : 13 releases, v1.1 to v3.0.1 (read 20261030 19:41 UTC)
5. https://github.com/AgriciDaniel/claude-obsidian/blob/main/CHANGELOG.md : 3.0.0 and 3.0.1 entries; commit subjects since 20261001 (read 20261030 19:42 UTC)
6. https://github.com/AgriciDaniel/claude-obsidian/blob/main/skills/wiki-retrieve/SKILL.md : BM25 pipeline (read 20261030 19:42 UTC)
7. https://github.com/AgriciDaniel/claude-obsidian/tree/main/docs : file list; `retrieval-evaluation.md` head (read 20261030 19:42 UTC)
8. https://github.com/AgriciDaniel/claude-obsidian/graphs/contributors : contributor list and open issue and pull request counts via the API (read 20261030 19:42 UTC)
