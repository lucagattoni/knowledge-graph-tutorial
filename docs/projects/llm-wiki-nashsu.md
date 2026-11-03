---
type: project
repo: nashsu/llm_wiki
trends: [plain-file-knowledge]
updated: 20261102 23:17 UTC
---

# LLM Wiki (nashsu)

This page answers what the desktop application "LLM Wiki" does, how it turns documents into a folder of Markdown pages, and what is known about how well it works. It implements a pattern that Andrej Karpathy published as a gist on 20260404 [3][6]. Its licence is GPL, so it is a read-only reference here.

| Field | Value |
|---|---|
| Repository | https://github.com/nashsu/llm_wiki [1] |
| Licence | GPL version 3, from the `LICENSE` file: the line "LLM Wiki — Copyright (C) 2024-2026 Yong Su", then the GNU GPL v3 text, which equals the text at gnu.org line for line (whitespace ignored). GitHub cannot classify it: the API says `NOASSERTION` ("Other"). The README says "GNU General Public License v3.0". "Only" or "or later": **unstated** [1][2][3]. |
| Trends | [Plain files as agent knowledge](../trends/plain-file-knowledge.md) |

## What it is

LLM Wiki is a cross-platform desktop application. It imports documents (PDF, Office files, e-books, web clips) and has a [large language model](../index/large-language-model.md) (LLM) write and maintain interlinked Markdown pages from them. The stack is Tauri v2 with a Rust backend and a React 19 front end [3].

The idea is Karpathy's. His gist says that most LLM use on documents is [retrieval-augmented generation](../index/retrieval-augmented-generation.md), which rediscovers knowledge on every question, and proposes instead that "the LLM incrementally builds and maintains a persistent wiki" [6]. He names three layers (raw sources, the wiki, a schema file) and three operations (ingest, query, lint), and calls the text "intentionally abstract" [6]. The README says the project is "based on" the pattern and "a concrete implementation with substantial extensions" [3]. Other projects in the same trend: [claude-obsidian](./claude-obsidian.md) and [Basic Memory](./basic-memory.md).

## How it works

**Data model.** A project is a folder: `purpose.md` (goals) and `schema.md` (page-type rules), `raw/sources/` (imported originals), `wiki/` with `index.md`, `log.md`, `overview.md` and subfolders for entities, concepts, sources, queries, synthesis and comparisons, plus app state in `.llm-wiki/`. The wiki opens as an Obsidian vault [3].

**Ingest.** The README names two steps: an analysis (entities, concepts, arguments, contradictions), then a generation that outputs page files [3]. The code runs more model calls than that [7]. After generation, a separate review-suggestion call runs only when the generated text is at least 10,000 characters or holds at least four file blocks; it asks for "high-value REVIEW blocks" (follow-up research, knowledge gaps) [7]. Wiki files whose output was cut off are retried in another call [7]. The README also lists a vision-model call that captions images found in PDFs [3]. The number of calls per source is therefore not fixed. A hash of each source skips unchanged files; a persistent queue retries a failed task up to three times [3][7]. The generation prompt forbids the model from writing `index.md` and `overview.md`; code updates them. The README still says step two yields them, so the README is older than the code here [3][7].

**Graph.** No model extracts the graph. Edges come from `[[wikilinks]]` and the `related` front-matter list. Each page pair gets a score from four signals: direct links (weight 3.0), shared sources (4.0), common neighbours by the Adamic-Adar measure (1.5) and same page type (1.0) [3][8]. The Louvain method groups pages into [communities](../index/community-detection.md), and the README says the app flags isolated pages and sparse clusters as "knowledge gaps" [3].

**Query.** Search runs in the Rust backend: keyword scoring, plus optional [vector search](../index/vector-search.md) over [LanceDB](https://github.com/lancedb/lancedb) (off by default). With both on, the two ranked lists are merged by reciprocal rank fusion, which adds 1/(60 + rank) per list to each page's score [9]. Linked pages then fill part of the result slots [3]. Chat runs through a tool-using agent that can search the wiki, raw sources, graph and web [3].

**Other tools.** A local HTTP API on `127.0.0.1:19828`, token-protected, serves projects, files, hybrid search, graph and chat; a bundled server speaks the [Model Context Protocol](../index/model-context-protocol.md) over it [3].

## Evidence

**Published results: one, first-party.** The README says "Benchmark: overall recall improved from 58.2% to 71.4% with vector search enabled" [3]. It names no dataset, question set, count or definition of recall. A code search of the repository for "58.2" returns four files, the README in four languages and nothing else [11].

**Independent evaluation: none found** on 20261102. Three searches turned up no measurement of the application: an arXiv search for "llm_wiki" or the author's handle (zero results) [12], an arXiv search for "LLM Wiki" with Karpathy's name (three papers listed, submitted April and May 2026; their titles do not name this application, and I did not read the papers, so none is ruled out as an evaluation) [13], and a web search, which returned feature descriptions and aggregator listings only [14]. This is a negative result from a limited search, not proof that none exists.

**Maintainer statements.** In issue 5, asked about collections of hundreds of thousands of documents, the maintainer replies (translated from Chinese) that with vector search "retrieval latency should be a few seconds at most", and later advises configuring a vector database for the best search speed and precision. No measurement is given [11][15]. The same thread holds a user report that the app crashed when importing about 50 PDFs (20260412); the maintainer answered "it's definitely our problem" and promised to test [15]. How the thread ended: **unstated** (I read it up to 20260626, where a user reports slow loading of a 50 GB-plus folder).

*Reading:* the application is well documented as a feature list and poorly documented as a measurement. The gist gives a rough figure for where the index works, "surprisingly well at moderate scale (~100 sources, ~hundreds of pages)", and says "at small scale the index file is enough, but as the wiki grows you want proper search" [6]. It gives no measured limit. No source read shows where an index-based wiki stops working, or how the vector-search option changes that.

## Status and direction

*Release.* `v0.6.13`, 20261022 01:21 UTC, is GitHub's latest; its notes only point to the download assets [4]. Six releases fell in the last 90 days (computed from the release list) [4].

*Activity in the last 90 days.* 120 commits from 20260806 to 20261021: 76 in August, 27 in September, 17 in October (computed). The owner made 105 of them. Nothing was pushed after 20261021, so no commit for 12 days at the time of reading; the repository is not archived [1][5]. Open pull requests keep arriving, the newest on 20261027 [10].

*Direction.* No roadmap was found. Recent commit subjects concern ingest at scale (queue, truncated model output, resume), more input formats and per-task model settings [5]. A hosted tier: none appears in the README [3]. Maintenance mode: not stated by the project.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [claude-obsidian](claude-obsidian.md)
- [Projects](README.md)

**Index**

- [LLM wiki](../index/llm-wiki.md)
- [Reciprocal rank fusion](../index/reciprocal-rank-fusion.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/nashsu/llm_wiki (via `gh api`) : metadata, archived flag, licence field `NOASSERTION`, push date (read 20261102 20:16 UTC)
2. `gh api repos/nashsu/llm_wiki/license`, https://github.com/nashsu/llm_wiki/blob/main/LICENSE and https://www.gnu.org/licenses/gpl-3.0.txt : file text and comparison (read 20261102 20:16 and 20:19 UTC)
3. https://github.com/nashsu/llm_wiki/blob/main/README.md (via `gh api repos/nashsu/llm_wiki/readme`) : features, folder layout, ingest, graph, search, API, results sentence, licence line (read 20261102 20:16 UTC)
4. `gh api repos/nashsu/llm_wiki/releases/latest` and the releases list : v0.6.13 and release dates (read 20261102 20:16 and 20:18 UTC)
5. `gh api repos/nashsu/llm_wiki/commits?since=2026-08-04` (paged, 120 commits) : counts, authors, subjects (read 20261102 20:18 UTC)
6. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f and its raw text : creation time 2026-04-04 16:25 UTC (page, read 20261102 20:19 UTC), three layers, quoted sentences, scale remark "~100 sources, ~hundreds of pages" and "at small scale the index file is enough" (raw text re-read 20261102 20:36 UTC)
7. https://github.com/nashsu/llm_wiki/blob/main/src/lib/ingest.ts : prompts forbidding index and overview, deterministic index update (read 20261102 20:18 UTC); the review-suggestion call, its trigger (10,000 characters or four file blocks) and the retry of truncated files (re-read 20261102 20:36 UTC)
8. https://github.com/nashsu/llm_wiki/blob/main/src/lib/graph-relevance.ts : the four signal weights (read 20261102 20:18 UTC)
9. https://github.com/nashsu/llm_wiki/blob/main/src-tauri/src/commands/search.rs : reciprocal rank fusion with k = 60 (read 20261102 20:18 UTC)
10. `gh api repos/nashsu/llm_wiki/pulls?state=open` : newest open pull requests (read 20261102 20:18 UTC)
11. `gh api -X GET search/code -f q='"58.2" repo:nashsu/llm_wiki'` : four files, all README files (read 20261102 20:37 UTC; the archive's earlier search of 20261030 19:34 UTC agrees, via the archive page kb-kg/projects/llm-wiki-nashsu.md)
12. https://arxiv.org/search/?query=%22llm_wiki%22+OR+nashsu&searchtype=all : zero results (read 20261102 20:37 UTC)
13. https://arxiv.org/search/?query=%22LLM+Wiki%22+Karpathy&searchtype=all : three papers listed, titles only (read 20261102 20:37 UTC)
14. A web search for "nashsu/llm_wiki" with the words comparison, review, tested, benchmark : feature descriptions and listings, no measurement; a lead, not a source (20261102 20:37 UTC)
15. https://github.com/nashsu/llm_wiki/issues/5 (`gh api repos/nashsu/llm_wiki/issues/5` and its comments) : questions on very large collections, maintainer replies of 20260413 and 20260428, crash report of 20260412, last comment read 20260626 (read 20261102 20:36 UTC; the archive's read of 20261030 19:33 UTC is the earlier source, via the archive page kb-kg/projects/llm-wiki-nashsu.md)

Further reading in the archive: [LLM Wiki, long entry](../../kb-kg/projects/llm-wiki-nashsu.md). Papers: [plain-file knowledge group](../papers/plain-file-knowledge.md).
