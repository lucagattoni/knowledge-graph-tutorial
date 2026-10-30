---
slug: llm-wiki-compiler
repo: atomicstrata/llm-wiki-compiler
tier: card
category: markdown-kb
snapshot: 20261030 19:45 UTC
---

# llm-wiki-compiler (llmwiki)

| | |
|---|---|
| Repository | https://github.com/atomicstrata/llm-wiki-compiler [1] |
| Licence | MIT, from the `LICENSE` file (MIT text, "Copyright (c) 2026 atomicmemory"; head and tail read) [2]. The README badge and the npm package also say MIT [3][6]. The copyright line names a different organisation: the GitHub API resolves `atomicmemory/llm-wiki-compiler` to this repository, so it was renamed or transferred; the date is unstated [1]. |
| Language | TypeScript (GitHub primary language) [1] |
| Stars, forks | 2,225, 237 (20261030 19:44 UTC; 10.7 forks per 100 stars) [1] |
| Created, last push | 20260405 19:53 UTC, 20261019 20:15 UTC [1] |
| Latest release | v1.5.0, 20261019 20:15 UTC; 20 releases since v0.1.0 (20260406) [5]. npm `llm-wiki-compiler` has 1.5.0 on `latest` and 1.5.0-rc.1 on `next` [6]. |
| Status | active: 10 days since the last push; the snapshot sets no flag [1][9] |
| Paper, docs | no paper stated; README, `docs/` folder, docs site named in the homepage field (not fetched) [1][3] |

## What it is

A TypeScript compiler, with a command line, an SDK and an MCP server, that turns raw sources (notes, PDFs, web pages, exported agent sessions) into an interlinked Markdown wiki with source citations [3]. The README says it implements the LLM Wiki pattern and cites Karpathy's gist [3][4]. The gist is an "idea file" that an agent turns into a working wiki with its user, with a catalog index and optional qmd search [8]. This project is a program with its own LLM pipeline instead. Its README feature list adds typed pages, review holds, freshness checks, embedding retrieval, exports, and "Configurable Lifecycle Profiles" that define domain record types and workflows [3][4]. The README reports no benchmark; its `eval` command scores a wiki's health and citations [3].

## How it works

Compile has two phases: the LLM extracts concepts from each changed source, finishing across all sources, then writes typed pages (concept, entity, comparison, overview), merging concepts shared by several sources [3][4]. Source hashes live under `.llmwiki/`, so unchanged sources skip the LLM [3]. Paragraphs cite source files and line ranges; `lint` checks the links [3]. Retrieval combines chunk embeddings, BM25 reranking and wikilink expansion, with a lexical fallback when the provider has no embedding endpoint [3][4]. Agents use `llmwiki serve` (MCP), the SDK or the CLI. Providers include Anthropic, OpenAI and Ollama; the quick start sets `ANTHROPIC_API_KEY` [3].

## Status and direction

Active. The API returned a full page of 100 commits since 20260801; 17 contributors, one with 217 of 256 contributions [1][7]. 2 pull requests are open and 209 merged; 8 issues are open and 36 closed [1]. The README calls it "still early software" and mentions roadmap items; where they are listed is unstated [3]. Release 1.5 separates wiki behaviour from file storage [3][7].

## Sources

1. https://github.com/atomicstrata/llm-wiki-compiler : repository metadata, rename redirect, contributors, pull-request and issue counts via the GitHub API (read 20261030 19:44 UTC)
2. https://github.com/atomicstrata/llm-wiki-compiler/blob/main/LICENSE : MIT text (read 20261030 19:44 UTC)
3. https://github.com/atomicstrata/llm-wiki-compiler/blob/main/README.md : features, quick start, commands, MCP, providers, scale, contributing (read 20261030 19:44 UTC)
4. https://github.com/atomicstrata/llm-wiki-compiler/blob/main/docs/concepts/karpathy-pattern.mdx : the project's account of how it implements the pattern (read 20261030 19:45 UTC)
5. https://github.com/atomicstrata/llm-wiki-compiler/releases : 20 releases, v0.1.0 to v1.5.0 (read 20261030 19:45 UTC)
6. https://registry.npmjs.org/llm-wiki-compiler : dist-tags, 24 versions from 0.1.0 (20260406), licence field (read 20261030 19:45 UTC)
7. https://github.com/atomicstrata/llm-wiki-compiler/commits/main : commit subjects since 20260801 (read 20261030 19:45 UTC)
8. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f : Karpathy, "LLM Wiki", created 20260404 16:25 (time zone as shown, unstated); the pattern's original description, traced in [the LLM-era timeline](../llm-era/README.md); raw file read from the gist's raw URL (read 20261030 19:42 UTC)
9. [The first GitHub snapshot](../landscape/20261030_1913-github/repos.tsv) : row for this repository, no flag (read 20261030 19:45 UTC)
