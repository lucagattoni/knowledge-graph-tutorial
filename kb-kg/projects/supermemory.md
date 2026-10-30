---
slug: supermemory
repo: supermemoryai/supermemory
tier: card
category: agent-memory
snapshot: 20261030 19:39 UTC
---

# Supermemory

| | |
|---|---|
| Repository | https://github.com/supermemoryai/supermemory [1] |
| Licence | MIT, from the root `LICENSE` file (MIT text, "Copyright (c) 2025 supermemory") [2]. It covers only the repository: the docs say the server source of Supermemory local "is not in the public repository", the binary is "built from a separate, non-public codebase" and "free within its lite license limit of 10,000 stored documents". The binary's licence text: unstated [4][5]. Sub-packages are MIT, except `skills/supermemory` (Apache-2.0) [3]. npm and PyPI list the `supermemory` SDK as Apache-2.0; its source repository: unstated [11]. |
| Language | TypeScript (GitHub primary language) [1] |
| Stars, forks | 31,471, 2,761 (20261030 19:39 UTC) [1] |
| Created, last push | 20240227 20:10 UTC, 20261029 21:02 UTC [1] |
| Latest release | server-v0.0.9, 20261012 18:59 UTC, "Supermemory Local 0.0.9"; all 18 releases are `server-v` tags [6] |
| Status | active (pushed within 24 hours of the read); not archived [1] |
| Paper, docs | no paper stated; docs at https://supermemory.ai/docs (source in `apps/docs`), plus a research page [1][7][9] |

## What it is

Supermemory describes itself as a memory and context engine for AI: it extracts facts from conversations, keeps user profiles, handles updates and contradictions, and also does document retrieval, connectors and file processing through one API [7]. It comes as a hosted service, as plugins and an MCP server for coding assistants, and as a self-hosted binary, Supermemory local [7]. The repository holds the docs, MCP server, web app, SDK wrappers and UI packages; the memory engine and local server are not in it, and the plugins live in separate repositories [1][4][5][7]. The README claims first place on LongMemEval, LoCoMo and ConvoMem and 95% Recall@15 on LongMemEval with about 720 tokens of added context [7]. The research page gives 97% Recall@20 on LongMemEval-S, judged with gpt-4o, with no third-party evaluation named and no scores for LoCoMo or ConvoMem [9].

## How it works

Content (text, conversations, PDFs, images, audio and video, code, connector items) passes through queued, extracting, chunking, embedding and indexing stages, after which it is searchable [8]. A second phase, "dreaming", passes content through a memory model that merges facts, updates and derived facts into a graph; the docs call the store a temporal vector-graph engine with vector, full-text and graph search built in [8]. A profile call returns static and dynamic facts, and search runs in hybrid (documents plus memories) or memories-only mode [7]. Agents connect through an MCP server (tools `memory`, `recall`, `context`) or plugins for Claude Code, Cursor, Codex, OpenCode, OpenClaw and Hermes [7]. LLM use at query time: unstated.

## Status and direction

Active. 165 commits on main from 20260801 to 20261029 (60, 45 and 60 by month); the newest are mostly documentation alignment and MCP fixes [10]. SDK 5.0.0 reached PyPI on 20261006 [11]. Supermemory local 0.0.9 (20261012) added prebuilt Docker images and API v5 support; native Windows stays on 0.0.8 [6]. 114 contributors (API count, anonymous included), 18 open pull requests, 21 open issues [10]. Roadmap: unstated.

## Sources

1. https://github.com/supermemoryai/supermemory : repository metadata via the GitHub API and the file tree (read 20261030 19:39 UTC)
2. https://github.com/supermemoryai/supermemory/blob/main/LICENSE : MIT text (read 20261030 19:39 UTC)
3. https://github.com/supermemoryai/supermemory/tree/main/packages : first lines of the sub-package LICENSE files (read 20261030 19:45 UTC)
4. https://github.com/supermemoryai/supermemory/blob/main/apps/docs/self-hosting/local-vs-enterprise.mdx : server source not public; lite licence limit (read 20261030 19:40 UTC)
5. https://github.com/supermemoryai/supermemory/blob/main/apps/docs/self-hosting/overview.mdx : binary built from a separate non-public codebase (read 20261030 19:41 UTC)
6. https://github.com/supermemoryai/supermemory/releases : 18 releases and the server-v0.0.9 notes, via the releases API (read 20261030 19:40 UTC)
7. https://github.com/supermemoryai/supermemory/blob/main/README.md : description, benchmark claims, MCP tools, plugins, API (read 20261030 19:39 UTC)
8. https://github.com/supermemoryai/supermemory/blob/main/apps/docs/concepts/how-it-works.mdx : ingest stages, dreaming, storage engine (read 20261030 19:40 UTC)
9. https://supermemory.ai/research : benchmark figures, as summarised by the fetch tool, so second-hand (read 20261030 19:44 UTC)
10. https://github.com/supermemoryai/supermemory/commits/main : commits since 20260801, open pull request and issue counts (search API), contributor count (read 20261030 19:40 UTC)
11. https://pypi.org/pypi/supermemory/json and https://registry.npmjs.org/supermemory : SDK versions, dates, licence metadata (read 20261030 19:45 UTC)
