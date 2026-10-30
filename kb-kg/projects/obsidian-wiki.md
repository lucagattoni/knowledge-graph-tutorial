---
slug: obsidian-wiki
repo: Ar9av/obsidian-wiki
tier: card
category: markdown-kb
snapshot: 20261030 19:43 UTC
---

# obsidian-wiki

| | |
|---|---|
| Repository | https://github.com/Ar9av/obsidian-wiki [1] |
| Licence | MIT, from the `LICENSE` file (MIT text, "Copyright (c) 2026 Ar9av"; head and tail read) [2]. The README licence section also says MIT [3]. |
| Language | Python (GitHub primary language) [1] |
| Stars, forks | 3,641, 366 (20261030 19:42 UTC; 10.1 forks per 100 stars) [1] |
| Created, last push | 20260406 06:20 UTC, 20261027 07:26 UTC [1] |
| Latest release | v2026.10.4, 20261027 07:26 UTC; 43 releases since v2026.04 (20260424). PyPI `obsidian-wiki` also lists 2026.10.4 as latest [7][8] |
| Status | active: pushed 3 days before the read; the snapshot sets no flag [1][11] |
| Paper, docs | no paper stated; README and a `docs/` folder [3][4] |

## What it is

A set of Markdown "skills" that an AI agent (Claude Code, Cursor, Codex, Gemini CLI and others) follows to turn notes, documents and past agent sessions into a linked Markdown vault that opens in Obsidian [3]. The README names Andrej Karpathy's LLM Wiki gist as the source of the pattern; the repository was created two days after the gist's date [3][10]. The gist is an "idea file" with ingest, query and lint operations, an index and a log, and qmd as an optional search tool [10]. The architecture page lists what the project added: a manifest so only changed sources are re-read, per-project filing, claim tags, history mining for six agents, dedup, cross-linking, graph export and tiered retrieval [3][4]. It also works as agent memory: hooks inject a recap at session start and suggest a capture at the end [3]. The README reports its own test on one 38-page vault: 83% correct answers with the skills, 44% without, two runs per cell, which it calls indicative [3].

## How it works

The 39 skills (the docs' count) are Markdown files an agent runs with its own file tools [4]. Ingest has four stages: read the source, pull out concepts, entities and claims, merge into existing pages, and keep a schema and a `.manifest.json` ledger so later runs handle only the delta [4]. Claims are tagged extracted, inferred or ambiguous [3][4]. A query reads titles, tags and summaries before page bodies; QMD search is optional and off by default [4][5]. A Python package adds a CLI, session hooks and an optional HTTP and MCP server whose container does no LLM work [1][6][8]. The README says its Python API needs no API key, embedding model or vector store [3].

## Status and direction

Active: 132 commits since 20260801, 43 releases in six months, 33 contributors, though the owner made 246 of 364 contributions [1][7][9]. 3 pull requests are open and 189 merged; 1 issue is open and 83 closed [1]. The README says "This is early" and lists no roadmap [3]. October work: a Claude Code plugin install, Open Knowledge Format export, a key-gated MCP endpoint [9].

## Sources

1. https://github.com/Ar9av/obsidian-wiki : repository metadata, file tree, contributors, pull-request and issue counts via the GitHub API (read 20261030 19:42 UTC)
2. https://github.com/Ar9av/obsidian-wiki/blob/main/LICENSE : MIT text (read 20261030 19:42 UTC)
3. https://github.com/Ar9av/obsidian-wiki/blob/main/README.md : description, install, comparison, own test, licence (read 20261030 19:42 UTC)
4. https://github.com/Ar9av/obsidian-wiki/blob/main/docs/architecture.md : four stages, vault structure, "What we added on top of Karpathy's pattern" (read 20261030 19:43 UTC)
5. https://github.com/Ar9av/obsidian-wiki/blob/main/docs/configuration.md : QMD search is optional, collections empty by default (read 20261030 19:43 UTC)
6. https://github.com/Ar9av/obsidian-wiki/blob/main/docs/deployment.md : Docker service, "does no LLM work" (read 20261030 19:43 UTC)
7. https://github.com/Ar9av/obsidian-wiki/releases : 43 releases, v2026.04 to v2026.10.4 (read 20261030 19:43 UTC)
8. https://pypi.org/pypi/obsidian-wiki/json : latest version 2026.10.4, extras including `server` (read 20261030 19:43 UTC)
9. https://github.com/Ar9av/obsidian-wiki/commits/main : subjects and counts since 20260801 (read 20261030 19:43 UTC)
10. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f : Karpathy, "LLM Wiki", created 20260404 16:25 (time zone as shown, unstated); the pattern's original description, traced in [the LLM-era timeline](../llm-era/README.md); raw file read from the gist's raw URL (read 20261030 19:42 UTC)
11. [The first GitHub snapshot](../landscape/20261030_1913-github/repos.tsv) : row for this repository, no flag, 17.58 stars per day (read 20261030 19:43 UTC)
