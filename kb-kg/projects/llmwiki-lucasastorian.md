---
slug: llmwiki-lucasastorian
repo: lucasastorian/llmwiki
tier: card
category: markdown-kb
snapshot: 20261030 19:46 UTC
---

# LLM Wiki (lucasastorian/llmwiki)

| | |
|---|---|
| Repository | https://github.com/lucasastorian/llmwiki [1] |
| Licence | Apache-2.0, from the `LICENSE` file (Apache License 2.0 text, 202 lines; head and tail read) [2]. The README badge and licence section also say Apache 2.0 [3]. |
| Language | Python (GitHub primary language); the README also names a Next.js web app and a Chrome extension [1][3] |
| Stars, forks | 1,734, 244 (20261030 19:45 UTC; 14.1 forks per 100 stars) [1] |
| Created, last push | 20260404 17:10 UTC, 20261029 23:27 UTC [1] |
| Latest release | none: no releases and no tags [5] |
| Status | active: pushed less than a day before the read; the snapshot sets no flag [1][10] |
| Paper, docs | no paper stated; the README; a hosted app at llmwiki.app (homepage field, not fetched) [1][3] |

## What it is

A web app, a Chrome extension and an MCP server that give Claude (or another MCP client) a workspace of source documents and a `wiki/` folder to write into [3]. The README says it is "heavily inspired by" Andrej Karpathy's LLM Wiki concept, "with an increased emphasis on autonomous maintenance" [3]. Against the original gist [9]: the gist is an idea file that an agent builds out with its user, prefers supervised one-at-a-time ingest and allows batch ingest "with less supervision" [9]. This project ships the whole stack and suggests a scheduled nightly Claude Routine to fold new sources in [3]. The extension also saves highlights and comments for Claude to read [3]. Its guide tells Claude never to keep a manual activity log, where the gist has a `log.md` [4][9]. No benchmark or evaluation appears in the README [3].

## How it works

Two modes: local (SQLite plus your folder, with `wiki/` for generated pages and a hidden `.llmwiki/` index) and hosted (Postgres plus S3) [3]. Files are chunked and indexed for search; PDFs and Office files pass through a converter [3]. Claude writes pages through ten MCP tools (guide, search, read, create, edit, append, delete, lint and two knowledge-base tools) [3]. The `guide` tool plays the schema role: sources read-only, a hub `overview.md`, concept and entity pages with frontmatter and footnote citations [3][4]. `lint` is deterministic [3]. The two requirements files list no LLM SDK; a quiz grader calls Cloudflare Workers AI [6][7].

## Status and direction

Active and owner-driven: 20 commits since 20260801, 11 of them on 20261015 and 20261022; 4 contributors, the owner with 197 of 200 contributions [1][8]. No releases or tags [5]. 17 pull requests are open (7 from Dependabot; the oldest of the other 10 dates from 20260509); 13 issues open, 2 closed [1]. The README's "What's next" lists Slack, Granola, email forward-to-save and a public ingest API with webhooks [3].

## Sources

1. https://github.com/lucasastorian/llmwiki : repository metadata, file tree, contributors, open pull requests, pull-request and issue counts via the GitHub API (read 20261030 19:45 UTC)
2. https://github.com/lucasastorian/llmwiki/blob/master/LICENSE : Apache License 2.0 text (read 20261030 19:45 UTC)
3. https://github.com/lucasastorian/llmwiki/blob/master/README.md : description, features, setup, MCP tools, architecture, roadmap, licence (read 20261030 19:45 UTC)
4. https://github.com/lucasastorian/llmwiki/blob/master/mcp/tools/guide.py : the guide text the MCP server gives Claude (read 20261030 19:46 UTC)
5. https://github.com/lucasastorian/llmwiki/releases : empty; the tags list is also empty (read 20261030 19:46 UTC)
6. https://github.com/lucasastorian/llmwiki/blob/master/api/requirements.txt : and `mcp/requirements.txt`, dependency lists (read 20261030 19:45 UTC)
7. https://github.com/lucasastorian/llmwiki/blob/master/api/services/quiz_grader.py : first 40 lines, Cloudflare Workers AI grader (read 20261030 19:46 UTC)
8. https://github.com/lucasastorian/llmwiki/commits/master : 20 commits since 20260801 (read 20261030 19:46 UTC)
9. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f : Karpathy, "LLM Wiki", created 20260404 16:25 (time zone as shown, unstated); the pattern's original description, traced in [the LLM-era timeline](../llm-era/README.md); raw file read from the gist's raw URL (read 20261030 19:42 UTC)
10. [The first GitHub snapshot](../landscape/20261030_1913-github/repos.tsv) : row for this repository, no flag, 5 contributors (read 20261030 19:46 UTC)
