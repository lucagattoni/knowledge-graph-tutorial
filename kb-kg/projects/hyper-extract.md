---
slug: hyper-extract
repo: yifanfeng97/Hyper-Extract
tier: card
category: core
snapshot: 20261030 19:39 UTC
---

# Hyper-Extract

| | |
|---|---|
| Repository | https://github.com/yifanfeng97/Hyper-Extract [1] |
| Licence | Apache License 2.0 text with small wording changes, from the `LICENSE` file; GitHub reports `NOASSERTION`. Terms under "What it is" [1][2]. |
| Language | Python [1] |
| Stars, forks | 4,207, 483 (20261030 19:39 UTC) [1] |
| Created, last push | 20260107 09:44 UTC, 20261029 00:22 UTC [1] |
| Latest release | v0.11.0, 20261029 00:22 UTC; PyPI lists 0.11.0 [4][5] |
| Status | active; not archived. The package classifier reads "Development Status :: 3 - Alpha" [5]. No flag in the landscape snapshot (14.21 stars per day, 11.48 forks per 100 stars; heuristics) [1][9] |
| Paper, docs | no paper stated; a `docs/` directory [3][7] |

## What it is

Hyper-Extract is a command-line tool and Python library that turns documents into structured knowledge with an LLM: graphs, hypergraphs, temporal and spatial graphs, lists and sets [3]. The README names 9 knowledge structures, 80+ YAML templates in six domains, and several extraction methods (a chunk-and-embed baseline, GraphRAG, LightRAG, Hyper-RAG, KG-Gen and others) [3]. The result is a saved directory that can be searched, updated and exported to Obsidian, GraphML, CSV, JSON-LD or Cypher [3]. No benchmark and no independent evaluation was found; the docs call their method-choice page "a decision aid, not an evaluation framework" [7]. The README table comparing it with GraphRAG, LightRAG, KG-Gen and ATOM is the project's own claim [3].

**Licence terms.** The `LICENSE` file (200 lines, read in full) is the Apache License 2.0 with the same 9 sections, grants and conditions [2]. A line diff against the apache.org text shows only small wording changes: the definitions of "Contribution" and "Contributor", clause 4(d) on NOTICE files, the end of section 4 and section 5. The appendix is filled in as "Copyright [2026] [Yifan Feng]", brackets left in [2][8]. Operative terms: a perpetual, royalty-free copyright licence to reproduce, modify, sublicense and distribute; a patent licence that ends if you sue over the Work; redistribution needs a copy of the licence, notices on changed files, retained notices and any NOTICE text; no trademark rights; no warranty [2]. No NOTICE file is in the repository root [6]. The README and `pyproject.toml` also say Apache 2.0 [3][5]. Legal effect of the wording changes: not assessed.

## How it works

A YAML template or named method fixes the structure and fields to extract [3]. Text is split into chunks; an LLM with function calling extracts items from each chunk in parallel, and a merger deduplicates entities [3][7]. Results are indexed with FAISS for semantic search [5][6]. `feed` adds a document under a named source, so its facts can be rolled back or replaced [3]. The `chunk_rag` method only embeds; graph methods pay for LLM extraction at ingest [7]. Providers include OpenAI, Anthropic, Gemini, DeepSeek and local vLLM [3]. Its stdio MCP server only reads and exports (nine tools) [3][7].

## Status and direction

Active. 241 commits since 20260801: 133 by the owner account, 58 and 40 by two others [6]. 21 releases from v0.1.1 (20260404) to v0.11.0, eleven of them between 20260901 and 20260915 [4]. 0 open issues, 6 open pull requests [10]. Roadmap: unstated.

## Sources

1. https://github.com/yifanfeng97/Hyper-Extract : repository metadata via the GitHub API (read 20261030 19:39 UTC)
2. https://github.com/yifanfeng97/Hyper-Extract/blob/main/LICENSE : full licence text (read 20261030 19:44 UTC)
3. https://github.com/yifanfeng97/Hyper-Extract/blob/main/README.md : description, structures, methods, providers, MCP tools, comparison table, licence line (read 20261030 19:44 UTC)
4. https://github.com/yifanfeng97/Hyper-Extract/releases : release tags and dates (read 20261030 19:44 UTC)
5. https://github.com/yifanfeng97/Hyper-Extract/blob/main/pyproject.toml and https://pypi.org/pypi/hyperextract/json : dependencies, classifiers, licence field, version (read 20261030 19:44 UTC)
6. https://github.com/yifanfeng97/Hyper-Extract/commits/main : repository tree, commit count since 20260801 (from the pagination header), authors (read 20261030 19:44 UTC)
7. https://github.com/yifanfeng97/Hyper-Extract/tree/main/docs/en : pages on methods, choosing a method, architecture and MCP (read 20261030 19:44 UTC)
8. https://www.apache.org/licenses/LICENSE-2.0.txt : canonical text used for the line diff (read 20261030 19:44 UTC)
9. [Landscape snapshot](../landscape/20261030_1913-github/repos.tsv) : stars per day, forks per 100 stars, flags (20261030 19:13 UTC)
10. https://github.com/yifanfeng97/Hyper-Extract/pulls : open issues and pull requests via the search API (read 20261030 19:45 UTC)
