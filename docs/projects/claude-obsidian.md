---
type: project
repo: AgriciDaniel/claude-obsidian
trends: [plain-file-knowledge]
updated: 20261102 23:17 UTC
---

# claude-obsidian

This page answers what claude-obsidian is, how it keeps a wiki of Markdown notes, and what is published about its quality. The short answer on evidence is that nothing comparative is published. The project belongs to the plain-files trend: the model writes and reads Markdown, and no database holds the knowledge.

| Field | Value |
|---|---|
| Repository | https://github.com/AgriciDaniel/claude-obsidian [1] |
| Licence | MIT. GitHub classifies the `LICENSE` file as MIT; the file is the standard MIT text, headed "Copyright (c) 2026 AgriciDaniel (AI Marketing Hub)" [2]. The README badge also says MIT [3]. |
| Trends | [Plain files as agent knowledge](../trends/plain-file-knowledge.md) |

## What it is

claude-obsidian is a plugin for Claude Code that turns sources dropped into a folder into a vault of linked, cited Markdown notes [3]. It is also packaged as Agent Skills (the [Agent Skills](../index/agent-skills.md) format) so that Codex, OpenCode, Gemini, ZCode, Cursor and Windsurf can load the same skills [3]. The README says it follows Andrej Karpathy's "LLM Wiki pattern" [3]. The pattern, as the gist states it, is that the model "incrementally builds and maintains a persistent wiki" of interlinked Markdown files, instead of retrieving chunks from raw documents at every question (see [llm-wiki](../index/llm-wiki.md)) [11].

It is not an Obsidian community plugin, and Obsidian is optional: the vault is a folder of Markdown that any editor opens, and Obsidian adds Graph view, Canvas and Bases on top [3]. For another product built on the same pattern, see [llm-wiki-nashsu](../projects/llm-wiki-nashsu.md).

## How it works

*Capture.* Sources go into `inbox/`. The project keeps an untouched copy of each one, named by its content, then writes linked pages in which each important claim points to its source [3]. There are 15 skills (5 to build and use the wiki, 7 extensions, 3 reference) and 3 agents that are read-only: they hand back drafts and reports, and one transaction layer writes to the vault [3].

*Safe writes.* Claude records a SHA-256 hash of every note it will touch, merges the drafts into one plan and applies it as one transaction with a rollback journal. If a person edits a note meanwhile, the hash no longer matches and the write stops with a conflict [3]. The lock covers local writers that cooperate with it; the README says other devices and external editors do not share it [3].

*The "graph".* The README calls the result a "knowledge graph of plain Markdown" and points to Obsidian's Graph view [3]. It mentions no graph database, no vector store and no [MCP](../index/model-context-protocol.md) (Model Context Protocol) server [3]. *Reading:* the graph is therefore the set of links between notes, not a stored graph structure. The contrast with [Basic Memory](../projects/basic-memory.md), which keeps a database index built from the files, is described on that page.

*Retrieval.* `wiki-retrieve` splits pages at paragraph boundaries, adds a short page-level prefix to each chunk, and builds a local [BM25](../index/bm25.md) (Best Matching 25, a keyword ranking function) index kept under `.vault-meta/` [7]. [Reranking](../index/reranking.md) with an Ollama embedding model is optional; prefixes made by a remote model need explicit consent and the `--allow-egress` flag [7]. The README states current limits: PDF and EPUB get metadata only ("no built-in text extraction yet"), web pages are prepared as a plan that a separate runner must fetch, and native Windows can preview but not write [3].

*Filing modes.* `wiki-mode` files new notes as Generic, LYT, PARA or Zettelkasten, and never moves old ones [3].

## Evidence

None published. The README makes no accuracy claim, and no paper is named [3]. The repository has a `bench` command that scores BM25 retrieval against labelled queries the user supplies, and a fixture of 14 queries over 10 invented pages [8]. Its own document says the fixture "establishes executable behavior" and does not establish real-vault quality or an improvement over a previous release [8]. Both are tools, not results.

Two other documents bear on limits, and neither is a quality result. The capacity document says the canonical source and claim ledgers "must fit the 16 MiB reader/writer limit", that transactions reject growth beyond it, and that "No page-count promise or constant latency follows from a passing small fixture" [9]. The prompt evaluator packages four invented Query and Save cases and checks a supplied JSON response offline; it does not run a model and does not validate answer quality [10].

A web search on 20261102 found no independent evaluation. Search results are leads, not sources, so none is cited.

## Status and direction

*Release.* v3.0.1, published 20261021 18:06 UTC, is GitHub's latest release [4]. The repository lists 13 releases, from v1.1 (20260408) [4].

*Activity.* The watch-list on the [projects page](./README.md) carries the live figures. As a dated snapshot read on 20261102: 108 commits on `main` since 20260804, the first on 20260825 and the last on 20261022, so nothing had landed on `main` between then and the read [5]. By subject prefix, 45 are `fix`, 18 `docs`, 17 `chore`, 6 `test`, 6 `release` and 4 `feat`; 10 are merges (computed) [5]. Four releases fall in the window: v2.1.1 (20260825), v2.2.0 (20260910), v3.0.0 and v3.0.1 (both 20261021) [4]. The repository was last pushed to on 20261025, after the last commit on `main` [1].

*Direction.* v3.0.0 was a "hardening release" (recoverable transactions, deterministic lint and retrieval, offline evaluation) and renamed the plugin to `agricidaniel-obsidian`, because Claude Code reserves plugin names that start with `claude-`. v3.0.1, the same day, restored the name `claude-obsidian` as an "owner-approved exception", although the host's validator still reports it as reserved [6]. `[Unreleased]` in the changelog is empty and no roadmap file is named [6].

*Hosted tier.* None appears: the FAQ says "no subscription and no tracking" [3]. The README and the repository's homepage field link a Skool community, "AI Marketing Hub Pro" [1][3]. Whether it is paid is **unstated** in the sources read.

*Reading:* the project is active and engineering effort goes into write safety, capacity limits and packaging, not into retrieval research. It shows how fast the trend's pattern became a product; it gives no evidence on how well the pattern answers questions. The archive page holds the longer notes: [claude-obsidian in the archive](../../kb-kg/projects/claude-obsidian.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Basic Memory](basic-memory.md)
- [LLM Wiki (nashsu)](llm-wiki-nashsu.md)
- [Projects](README.md)

**Index**

- [Agent Skills](../index/agent-skills.md)
- [LLM wiki](../index/llm-wiki.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/AgriciDaniel/claude-obsidian : repository metadata, archived flag, homepage field, last push (read 20261102 20:35 UTC)
2. https://api.github.com/repos/AgriciDaniel/claude-obsidian/license and https://github.com/AgriciDaniel/claude-obsidian/blob/main/LICENSE : licence text and GitHub's classification (read 20261102 20:35 UTC)
3. https://api.github.com/repos/AgriciDaniel/claude-obsidian/readme (the README): description, skills, agents, safety, limits, FAQ, hosts, community link (read 20261102 20:34 UTC)
4. https://api.github.com/repos/AgriciDaniel/claude-obsidian/releases and https://api.github.com/repos/AgriciDaniel/claude-obsidian/releases/latest : v3.0.1 and the 13 releases (list read 20261102 20:16 UTC; latest re-read 20:35 UTC)
5. https://api.github.com/repos/AgriciDaniel/claude-obsidian/commits?since=2026-08-04T00:00:00Z : count, first and last dates, subjects (count and dates re-read 20261102 20:35 UTC; subjects read 20:16 UTC)
6. https://github.com/AgriciDaniel/claude-obsidian/blob/main/CHANGELOG.md : 3.0.0 and 3.0.1 entries, empty `[Unreleased]` (read 20261102 20:16 UTC)
7. https://github.com/AgriciDaniel/claude-obsidian/blob/main/skills/wiki-retrieve/SKILL.md : BM25 pipeline, consent rules, optional reranking (read 20261102 20:17 UTC)
8. https://github.com/AgriciDaniel/claude-obsidian/blob/main/docs/retrieval-evaluation.md : `bench` command, fixture, stated scope (read 20261102 20:17 UTC)
9. https://github.com/AgriciDaniel/claude-obsidian/blob/main/docs/capacity-and-recovery.md : ledger limit, no page-count promise (read 20261102 20:34 UTC)
10. https://github.com/AgriciDaniel/claude-obsidian/blob/main/docs/prompt-evaluation.md : offline evaluator, four invented cases, evidence boundary (read 20261102 20:34 UTC)
11. https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw : the LLM Wiki pattern, first-hand (read 20261102 20:34 UTC)
