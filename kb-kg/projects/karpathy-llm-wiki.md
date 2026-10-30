---
slug: karpathy-llm-wiki
repo: Astro-Han/karpathy-llm-wiki
tier: card
category: markdown-kb
snapshot: 20261030 19:39 UTC
---

# karpathy-llm-wiki

| | |
|---|---|
| Repository | https://github.com/Astro-Han/karpathy-llm-wiki [1] |
| Licence | MIT, from the `LICENSE` file (MIT text; head and tail read) [2]. The README badge and licence line also say MIT, so they agree [3]. |
| Language | Python (GitHub primary language); the skill itself is Markdown plus one Python script [1][8] |
| Stars, forks | 2,643, 310 (20261030 19:39 UTC; the landscape snapshot of 20261030 19:13 UTC has the same figures, 11.73 forks per 100 stars) [1] |
| Created, last push | 20260405 06:17 UTC, 20260723 16:57 UTC [1] |
| Latest release | none: zero releases and zero tags [1] |
| Status | quiet: 99 days since the last push at the snapshot (heuristic flag `quiet`); not archived [1] |
| Paper, docs | no paper stated; the README, `SKILL.md` and `examples/` [3][4][8] |

## What it is

An installable "skill" (an instruction file for coding agents such as Claude Code, Cursor and Codex) that implements the wiki workflow from Andrej Karpathy's "LLM Wiki" idea [3]. The README calls it an unofficial community implementation. The agent ingests sources into `raw/`, compiles Markdown pages into `wiki/`, answers questions with citations, and lints the result [3]. The README claims the workflow comes from a production knowledge base maintained daily since April 2026, with 94 articles and 99 sources; this is the author's own claim and was not checked [3]. No benchmark or independent evaluation appears in the README [3]. It says it does not follow the Open Knowledge Format, calling that specification a v0.1 draft to be revisited [3]; see the [Open Knowledge Format card](open-knowledge-format.md).

## How it works

`SKILL.md` is the schema the host agent follows. Ingest saves a source into an immutable `raw/<topic>/` file, then triages it as New, Update, Disputed or No material; it writes or merges articles in `wiki/<topic>/`, updates affected pages, refreshes `index.md` and appends to `log.md` [4]. Query reads the index, searches the wiki and answers with links; it writes nothing unless asked to archive [4]. Lint repairs index and link errors and runs `check_evidence.py`, which reports numbers, dates and quotes missing verbatim from the linked raw files [4][7]. The README lists vector search, graph search and MCP servers as deliberately not built [3].

## Status and direction

Quiet, not archived, no release. All 28 commits are from one account: 14 between 20260405 and 20260413, none until 20260723, then 14 in under three hours that added triage, the evidence checker and fixes to it; none since [1][5]. Why the pause: unstated. There are 5 open issues and 5 open pull requests; the owner's last issue or pull-request comment is dated 20260723 12:05 UTC [6].

## Sources

1. https://github.com/Astro-Han/karpathy-llm-wiki : repository metadata, releases, tags and contributors via the GitHub API (read 20261030 19:39 to 19:40 UTC)
2. https://github.com/Astro-Han/karpathy-llm-wiki/blob/main/LICENSE : MIT licence text (read 20261030 19:39 to 19:40 UTC)
3. https://github.com/Astro-Han/karpathy-llm-wiki/blob/main/README.md : description, usage figures, design boundaries, OKF statement, licence line (read 20261030 19:39 to 19:40 UTC)
4. https://github.com/Astro-Han/karpathy-llm-wiki/blob/main/SKILL.md : ingest, query and lint procedures (read 20261030 19:39 to 19:40 UTC)
5. https://github.com/Astro-Han/karpathy-llm-wiki/commits/main : all 28 commits, authors and timestamps (read 20261030 19:39 to 19:40 UTC)
6. https://github.com/Astro-Han/karpathy-llm-wiki/issues : issues, pull requests and their comments with author roles via the GitHub API (read 20261030 19:39 to 19:40 UTC)
7. https://github.com/Astro-Han/karpathy-llm-wiki/blob/main/scripts/check_evidence.py : docstring of the evidence checker (read 20261030 19:39 to 19:40 UTC)
8. https://github.com/Astro-Han/karpathy-llm-wiki/tree/main : file layout via the git trees API (read 20261030 19:39 to 19:40 UTC)
