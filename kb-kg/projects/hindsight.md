---
slug: hindsight
repo: vectorize-io/hindsight
tier: card
category: agent-memory
snapshot: 20261030 19:39 UTC
---

# Hindsight

| | |
|---|---|
| Repository | https://github.com/vectorize-io/hindsight [1] |
| Licence | MIT, from the `LICENSE` file (MIT text, "Copyright (c) 2025 Vectorize AI, Inc."); the README badge and licence section also say MIT, so they agree [2][3]. |
| Language | Python (GitHub primary language); the README lists Node, Go and CLI clients [1][3] |
| Stars, forks | 56,612, 6,809 (20261030 19:39 UTC) [1] |
| Created, last push | 20251030 11:49 UTC, 20261030 18:19 UTC [1] |
| Latest release | v1.1.0, 20261021 16:41 UTC; v1.0.0 was 20261013; 74 releases in all [4] |
| Status | active (pushed 1 hour before the read); not archived [1]. Snapshot flag `fast-growth`: 155.09 stars per day, where the flag starts at 150 [8][9]. It is a heuristic (lifetime stars over age) and does not say how the stars arose. Checks: 12.03 forks per 100 stars; 291 contributors (API count, anonymous included) [1][7]. The project's posts give 20,000 stars on 20260814, 40,000 on 20260928 ("We are not launching anything today") and 50,000 on 20261015 [6]. Created 20251030, yet the 20,000-star post dates open-sourcing to December 2025; earlier visibility: unstated [1][6]. The stargazer-timestamp endpoint returned HTTP 404, so the growth curve is unchecked [10]. |
| Paper, docs | arXiv 2512.12818 [5]; docs at https://hindsight.vectorize.io [3] |

## What it is

Hindsight is an agent memory system from Vectorize.io that, in its README's words, is "focused on making agents that learn, not just remember" [3]. Memories live in isolated banks and are reached through three operations: retain, recall and reflect [3]. The README claims state-of-the-art accuracy on LongMemEval and says Virginia Tech's Sanghani Center and The Washington Post independently reproduced the results; I did not locate that reproduction [3]. The paper (14 December 2025) reports 91.4% on LongMemEval and 89.61% on LoCoMo with a larger backbone, and 83.6% overall with a 20B open-source model [5].

## How it works

Retain sends content to an LLM that extracts facts, times, entities and relationships and normalises them into entities, time series and search indexes [3]. Memories are typed as world facts, experiences, observations (consolidated, evidence-backed beliefs) and mental models (standing answers refreshed in the background) [3]. Recall runs four strategies in parallel (vector, BM25, graph, temporal), merges them by reciprocal rank fusion and a cross-encoder rerank, and trims to a token limit [3]. Reflect analyses memories more deeply, shaped by per-bank disposition traits [3]. Storage is PostgreSQL with pgvector, or Oracle [3]. Agents use Python, Node and Go clients, REST, or a per-bank MCP endpoint [3].

## Status and direction

Active. 1,702 commits on main from 20260801 to 20261030, 1,300 of them by two committers [7]. Releases come roughly weekly; the project says 1.0.0 (20261013) makes the API stable, and that Memlake, an object-storage engine, is part of Hindsight Enterprise; whether its source is in this repository: not checked [4][6]. 152 open issues, 8 open pull requests [7]. The 40,000-star post says "No roadmap promises" [6].

## Sources

1. https://github.com/vectorize-io/hindsight : repository metadata via the GitHub API (read 20261030 19:39 UTC)
2. https://github.com/vectorize-io/hindsight/blob/main/LICENSE : MIT text (read 20261030 19:39 UTC)
3. https://github.com/vectorize-io/hindsight/blob/main/README.md : description, operations, memory types, storage, integrations, benchmark claims, licence section (read 20261030 19:39 UTC)
4. https://github.com/vectorize-io/hindsight/releases : 74 releases and the v1.1.0 notes, via the releases API (read 20261030 19:41 UTC)
5. https://arxiv.org/abs/2512.12818 : paper abstract, via the fetch tool (read 20261030 19:43 UTC)
6. https://github.com/vectorize-io/hindsight/tree/main/hindsight-docs/blog : the 20,000-, 40,000- and 50,000-star posts, dated 20260814, 20260928 and 20261015 (read 20261030 19:44 UTC and 19:47 UTC)
7. https://github.com/vectorize-io/hindsight/commits/main : commits since 20260801 and authorship, open issue and pull request counts (search API), contributor count (read 20261030 19:41 UTC)
8. [Landscape snapshot README](../landscape/20261030_1913-github/README.md) : the `fast-growth` flag starts at 150 stars per day (read 20261030 19:47 UTC)
9. [Landscape snapshot data](../landscape/20261030_1913-github/repos.tsv) : this repository's row: 56,608 stars, 155.09 stars per day, 12.03 forks per 100 stars (snapshot 20261030 19:13 UTC, read 20261030 19:39 UTC)
10. https://github.com/vectorize-io/hindsight/stargazers : the stargazers API with timestamps returned HTTP 404 (read 20261030 19:43 UTC)
