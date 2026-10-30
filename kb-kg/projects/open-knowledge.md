---
slug: open-knowledge
repo: inkeep/open-knowledge
tier: card
category: markdown-kb
snapshot: 20261030 19:45 UTC
---

# OpenKnowledge

| | |
|---|---|
| Repository | https://github.com/inkeep/open-knowledge [1] |
| Licence | GPL-3.0, with a wording split. The `LICENSE` file is the "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007" text (head and tail read) [2]. The README says "GNU General Public License v3.0 or later" [3]. The root and the seven package manifests say `GPL-3.0-or-later` [4]. The GitHub field says `GPL-3.0` [1]. So "or later" comes from the README and manifests, not the licence file. |
| Language | TypeScript (GitHub primary language); the tree also holds a Rust toolchain file [1] |
| Stars, forks | 4,741, 327 (20261030 19:43 UTC) [1]. The [landscape snapshot](../landscape/20261030_1913-github/repos.tsv) of 20261030 19:13 UTC shows 31.82 stars per day, 6.9 forks per 100 stars, 15 contributors, and no flag. |
| Created, last push | 20260603 11:12 UTC, 20261030 18:49 UTC [1] |
| Latest release | v0.89.0, 20261030 13:28 UTC; beta tags (`v0.89.1-beta.2` at 18:22 UTC) follow it [6] |
| Status | active (pushed the day of the read); not archived [1] |
| Paper, docs | no paper stated; docs site at openknowledge.ai/docs, sources in `docs/` [1][3] |

## What it is

OpenKnowledge is a Markdown editor, in the README's words with "integrations with Claude, Codex, and other harnesses", for knowledge bases, LLM wikis, specs and notes; it calls itself "private, local, and free" [3]. It ships as a desktop app (macOS, Windows, Linux) and a local web UI with a link-graph viewer, and opens any folder of Markdown or MDX, including Obsidian vaults [3]. Git and GitHub provide optional sync and sharing [3]. An optional beta plugin checks that a project stays portable to Google's Open Knowledge Format, the format [OpenKB](openkb.md) also names [12]. The CLA names Inkeep, Inc.; it is kept as a record, and contributions now come as issues [5].

## How it works

The files are the database: plain Markdown under git, edited by a person, an agent or a text editor [10]. A local collaboration server starts on the first call that needs it [8]. The MCP server has 19 tools: `exec` (read-only shell whose reads add backlinks, links and history), `search` (title boost, BM25, recency), `links` (backlinks, dead links, orphans, hubs, suggestions), `lint`, `audit`, write verbs, history and restore [8]. The docs describe retrieval as an agent loop with "no vector database"; optional embeddings search is off by default and sends text to the provider you configure [9][11]. No LLM index step is described.

## Status and direction

Very active, version 0.x: stable v0.88.12, v0.88.13 and v0.89.0 were tagged within two days, among beta tags [6]. At least 100 commits since 20260801 (one API page) [7]. Commit subjects carry ticket ids and pull request numbers up to #8353, the public tracker shows 4 open pull requests, and `inkeep-oss-sync[bot]` has 492 contributions: my inference is that the history is synced from another repository; the sources say nothing on it [7]. 53 issues are open [7]. Roadmap: unstated.

## Sources

1. https://github.com/inkeep/open-knowledge : repository metadata via the GitHub API (read 20261030 19:43 UTC)
2. https://github.com/inkeep/open-knowledge/blob/main/LICENSE : GPL version 3 text, head and tail (read 20261030 19:44 UTC)
3. https://github.com/inkeep/open-knowledge/blob/main/README.md : description, install, features, licence section (read 20261030 19:43 UTC)
4. `package.json` at the root and in `packages/` (app, cli, core, desktop, native-config, plugin, server) : `license` fields (read 20261030 19:44 UTC)
5. https://github.com/inkeep/open-knowledge/blob/main/CLA.md : contributor licence agreement, kept as a record (read 20261030 19:44 UTC)
6. https://github.com/inkeep/open-knowledge/releases : release list and latest stable release (read 20261030 19:43 and 19:45 UTC)
7. https://github.com/inkeep/open-knowledge/commits/main : commit subjects, contributor counts, open issue and pull request counts via the API (read 20261030 19:45 UTC)
8. https://github.com/inkeep/open-knowledge/blob/main/docs/content/reference/mcp.mdx : MCP tools (read 20261030 19:44 UTC)
9. https://github.com/inkeep/open-knowledge/blob/main/docs/content/reference/agentic-search.mdx : "no vector database", optional semantic search (read 20261030 19:44 UTC)
10. https://github.com/inkeep/open-knowledge/blob/main/docs/content/reference/core-concepts.md : three-layer model, files as database (read 20261030 19:44 UTC)
11. https://github.com/inkeep/open-knowledge/blob/main/docs/content/reference/configuration.mdx : `search.semantic.*` settings, default off (read 20261030 19:44 UTC)
12. https://github.com/inkeep/open-knowledge/blob/main/docs/content/plugins/okf.mdx : OKF plugin, beta (read 20261030 19:45 UTC)
