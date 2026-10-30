---
slug: khoj
repo: khoj-ai/khoj
tier: card
category: adjacent
snapshot: 20261030 19:46 UTC
---

# Khoj

| | |
|---|---|
| Repository | https://github.com/khoj-ai/khoj [1] |
| Licence | AGPL-3.0. The `LICENSE` file is the GNU Affero General Public License, Version 3, of 19 November 2007 (head, section 13 and tail read) [2]. Section 13 requires a modified version to offer remote network users its Corresponding Source [2]. `pyproject.toml` declares `AGPL-3.0-or-later`, a small difference from the GitHub field `AGPL-3.0` [1][3]. The README has no licence statement [4]. |
| Language | Python (GitHub primary language); the web app is Next.js [1][6] |
| Stars, forks | 37,907, 2,529 (20261030 19:41 UTC; the [landscape snapshot](../landscape/20261030_1913-github/repos.tsv) of 19:13 UTC has 37,906 and 2,529) [1] |
| Created, last push | 20210816 01:48 UTC, 20260802 01:55 UTC [1] |
| Latest release | 2.0.0-beta.28, 20260326 03:36 UTC, not marked a pre-release on GitHub [5]. PyPI's version field reads 1.42.10; its newest uploads are 2.0.0b29.dev11 and dev12 of 20260802 [8]. |
| Status | active by the 90-day rule, at its edge: 89 days 17 hours since the last push at 20261030 19:46 UTC; it passes 90 days at 20261031 01:55 UTC. The landscape snapshot raised no flag [1] |
| Paper, docs | no paper stated; docs at https://docs.khoj.dev [4] |

## What it is

Khoj calls itself "your AI second brain": a self-hostable personal AI app that answers from the web and from the user's documents (PDF, Markdown, org-mode, Word, Notion, images), with custom agents and scheduled automations, reachable from a browser, Obsidian, Emacs, desktop, phone and WhatsApp [4]. It is a document search and chat application, not a graph system; no file path in the repository mentions a graph (path names only) [7]. The README links a post, dated 22 November 2024, that reports FRAMES and SimpleQA runs where the agent searches the web and runs code, so it measures the research modes, not retrieval over a personal knowledge base [4][9]. A hosted cloud app and an Enterprise offer are advertised [4].

## How it works

Per-format processors (Markdown, org-mode, PDF, DOCX, plain text, images, Notion, GitHub) split documents into entries [7]. A bi-encoder embeds the chunks into a pgvector column; the constructor default in code is `thenlper/gte-small`, replaceable by Hugging Face or OpenAI-compatible endpoints [7][10]. A query is embedded, the nearest chunks are fetched, and a cross-encoder can rerank them [7][10]. User memories are stored with their own embeddings [7]. `mcp.py` defines an `MCPClient`, so Khoj can call MCP servers; I did not look for a server side [7].

## Status and direction

Commits dated since March 2026: 25 in March, 10 in June, 2 on 20260802, none after [6]. The last merged pull request closed 20260802; 60 are open [11]. Commits of 20260325 and 20260326, before releases 2.0.0-beta.26 to beta.28, add a banner for hosted-cloud users: "Khoj Cloud is being deprecated on April 15, 2026", which mentions self-hosting [5][6][12]. The README points to Pipali, a separate Apache-2.0 repository pushed 20261030 [4][13]. Maintainer intent: unstated.

## Sources

1. https://github.com/khoj-ai/khoj : repository metadata via the GitHub API (read 20261030 19:41 UTC)
2. https://github.com/khoj-ai/khoj/blob/master/LICENSE : AGPL v3 text, 661 lines (read 20261030 19:44 UTC)
3. https://github.com/khoj-ai/khoj/blob/master/pyproject.toml : licence field (read 20261030 19:45 UTC)
4. https://github.com/khoj-ai/khoj/blob/master/README.md : description, formats, offers, Pipali (read 20261030 19:44 UTC)
5. https://github.com/khoj-ai/khoj/releases : releases to 2.0.0-beta.28 and its notes (read 20261030 19:44 UTC)
6. https://github.com/khoj-ai/khoj/commits/master : 37 commits since 20260301 (read 20261030 19:44 UTC)
7. https://github.com/khoj-ai/khoj/tree/master/src/khoj : file layout, processors, embeddings.py, text_search.py, database models, mcp.py (read 20261030 19:44 UTC)
8. https://pypi.org/pypi/khoj/json : PyPI versions and upload times (read 20261030 19:44 UTC)
9. https://blog.khoj.dev/posts/evaluate-khoj-quality/ : evaluation post (read 20261030 19:44 UTC)
10. https://github.com/khoj-ai/khoj/blob/master/documentation/docs/features/search.md : search implementation overview (read 20261030 19:44 UTC)
11. https://github.com/khoj-ai/khoj/pulls : merged, open and recently closed pull requests via the API (read 20261030 19:45 UTC)
12. https://github.com/khoj-ai/khoj/commit/f7bce4893483e5596f1520af1a9fbfb7302969a7 : banner commit, 20260325 (read 20261030 19:44 UTC)
13. https://github.com/khoj-ai/pipali : repository metadata (read 20261030 19:44 UTC)
