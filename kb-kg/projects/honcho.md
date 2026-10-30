---
slug: honcho
repo: plastic-labs/honcho
tier: card
category: agent-memory
snapshot: 20261030 19:45 UTC
---

# Honcho

| | |
|---|---|
| Repository | https://github.com/plastic-labs/honcho [1] |
| Licence | AGPL-3.0. `LICENSE` is the GNU Affero General Public License version 3, identical to the standard text after whitespace normalisation, with no added terms [2][5]. README and docs agree [3][7]. Section 13 as written: if you modify the program, your version must prominently offer all users interacting with it remotely through a computer network the chance to receive its Corresponding Source, at no charge [2]. On hosted use the project says only that Honcho runs "managed" at api.honcho.dev or self-hosted, and is "open source under AGPL-3.0" [3]. I found no statement on hosting obligations and no dual or commercial licence in the README, `CONTRIBUTING.md` or the docs licence page [3][6][7]. Package metadata declares Apache-2.0 for the SDKs and MIT for the CLI, with no separate licence file in those directories [8][9]. |
| Language | Python (FastAPI server), with TypeScript SDK [1][3] |
| Stars, forks | 7,837, 959 (20261030 19:45 UTC); about 12.2 forks per 100 stars [1] |
| Created, last push | 20230910 21:29 UTC, 20261030 19:10 UTC [1] |
| Latest release | v3.5.0, 20261030 19:10 UTC; six GitHub releases, from v3.2.1 on 20260924 [4]. PyPI `honcho-ai` (SDK) 2.8.0 [14]. |
| Status | active (pushed within 90 days); no heuristic flag (landscape snapshot, 20261030 19:13 UTC) [15] |
| Paper, docs | no paper stated; docs in `docs/` and at honcho.dev/docs; evals page and blog posts named in the README, not fetched [3][10] |

## What it is

Honcho calls itself "memory infrastructure for building stateful agents that understand changing people, agents, groups, projects, and ideas over time" [3]. A FastAPI server stores messages from peers (people or agents) in sessions inside workspaces, reasons over them in the background, and answers questions about a peer [3]. It runs as a managed service, as a local stack started by its CLI, or from source [3]. The README says the project "has defined the Pareto Frontier of Agent Memory" and points to an evals page (LongMemEval, LoCoMo and others); figures unchecked [3]. Pull requests are limited to maintainers [6].

## How it works

Messages are stored at once and queued [10]. A background worker, the deriver, extracts explicit and deductive conclusions; the dreamer later consolidates them and adds inductive ones [10]. Summaries and peer cards are also produced [3]. Conclusions are vector-embedded documents keyed by observer and observed peer, in PostgreSQL with pgvector [3]. Reads: a chat endpoint that runs an LLM tool loop, hybrid BM25 and vector search, static representations, and prompt-ready session context [3][12]. Interfaces: SDKs, CLI, MCP server, plugins for Claude Code, Codex, Cursor and others [3]. Each feature defaults to one hosted OpenAI model; other OpenAI-compatible endpoints can be set per feature [3].

## Status and direction

Active and fast-moving: 279 commits since 20260801 (74, 89, 116 for August to October) and six releases since 20260924 [4][11]. Recent work: session scopes, groundwork for soft deletion, source-message citations on conclusions, Claude 5.x support, agent-tool plugins [11][12]. 73 contributors, 68 open pull requests, 97 open issues [13]. Roadmap: unstated.

## Sources

1. https://github.com/plastic-labs/honcho : repository metadata, GitHub API (read 20261030 19:39 UTC; stars and forks 19:45 UTC)
2. https://github.com/plastic-labs/honcho/blob/main/LICENSE : licence text, section 13 (read 20261030 19:39 UTC)
3. https://github.com/plastic-labs/honcho/blob/main/README.md : description, integrations, self-hosting, LLM defaults, licence (read 20261030 19:39 UTC)
4. https://github.com/plastic-labs/honcho/releases : six releases with dates (read 20261030 19:39 UTC)
5. https://api.github.com/licenses/agpl-3.0 : standard AGPL-3.0 text, compared line by line (read 20261030 19:44 UTC)
6. https://github.com/plastic-labs/honcho/blob/main/CONTRIBUTING.md : pull request policy (read 20261030 19:42 UTC)
7. https://github.com/plastic-labs/honcho/blob/main/docs/v3/contributing/license.mdx : docs licence page (read 20261030 19:42 UTC)
8. https://github.com/plastic-labs/honcho/blob/main/sdks/python/pyproject.toml, https://github.com/plastic-labs/honcho/blob/main/sdks/typescript/package.json, https://github.com/plastic-labs/honcho/blob/main/honcho-cli/pyproject.toml : licence fields (read 20261030 19:45 UTC)
9. https://github.com/plastic-labs/honcho : file tree, `LICENSE` files listed (read 20261030 19:39 UTC)
10. https://github.com/plastic-labs/honcho/blob/main/docs/v3/documentation/core-concepts/reasoning.mdx : deriver, dreamer, storage flow (read 20261030 19:42 UTC)
11. https://github.com/plastic-labs/honcho/commits/main : commit subjects since 20260801 (read 20261030 19:41 UTC)
12. https://github.com/plastic-labs/honcho/releases/tag/v3.5.0 : release notes (read 20261030 19:43 UTC)
13. https://github.com/plastic-labs/honcho/pulls : open pull request, issue and contributor counts (read 20261030 19:41 UTC)
14. https://pypi.org/pypi/honcho-ai/json : PyPI versions (read 20261030 19:41 UTC)
15. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : first GitHub snapshot row (read 20261030 19:39 UTC)
