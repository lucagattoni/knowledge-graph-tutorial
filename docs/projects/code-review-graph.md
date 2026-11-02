---
type: project
repo: tirth8205/code-review-graph
trends: [code-knowledge-graphs]
updated: 20261102 23:17 UTC
---

# code-review-graph

code-review-graph keeps a parsed graph of a codebase on disk and tells a coding assistant which files a change can affect, so the assistant reads those files and not the whole repository. This page says how it works, what has been measured and by whom, and where the project stands.

| Field | Value |
|---|---|
| Repository | https://github.com/tirth8205/code-review-graph |
| Licence | MIT. The `LICENSE` file starts "MIT License" and "Copyright (c) 2026 Tirth Kanani"; GitHub classifies it as MIT [1][2] |
| Trends | [Code graphs for coding agents](../trends/code-knowledge-graphs.md) |

## What it is

code-review-graph is a Python package that describes itself as "A local code knowledge graph that gives AI coding tools precise review context over MCP" (Model Context Protocol) [3]. It parses a repository with [tree-sitter](../index/tree-sitter.md), updates the graph incrementally, and serves compact context over the [Model Context Protocol](../index/model-context-protocol.md) or a command line [3]. The `install` command detects 16 named agent platforms and configures each [3]. A GitHub Action posts a risk-scored comment on each pull request, with an optional merge gate [3]. It targets review and impact analysis. [codebase-memory-mcp](../projects/codebase-memory-mcp.md), [codegraph](../projects/codegraph.md) and [graphify](../projects/graphify.md) are other [code graph](../index/code-graph.md) tools.

## How it works

**Parse and store.** Tree-sitter turns files into nodes (functions, classes, imports) and edges (calls, inheritance, test coverage), kept in one SQLite file in `.code-review-graph/` [3]. Hooks, a pre-commit hook or watch mode re-parse only files whose SHA-256 hash changed [3].

**Blast radius.** For a change, a walk over callers, dependents and tests finds the smallest set of files to read: [impact analysis](../index/impact-analysis.md) on a static graph [3]. Leiden [community detection](../index/community-detection.md), execution flows, hub and bridge nodes add structure [3].

**Search.** Embeddings are optional: local sentence-transformers, Gemini, MiniMax, Voyage or any OpenAI-compatible endpoint. Full-text and vector similarity combine in [hybrid search](../index/hybrid-search.md) [3]. The README says there is no telemetry [3].

**Who reasons.** Parsing needs no [language model](../index/large-language-model.md); only the optional embeddings use a model [3]. The [agent](../index/agent.md) calls 30 MCP tools and 5 MCP prompts [3].

## Evidence

All published results are first-party: the maintainers' own evaluation runner, on six open-source repositories and 13 commits, each pinned to an upstream commit [3]. The token figures were captured on 20260802 with version 2.3.7; the capture date of the impact figures is **unstated** [3]. No paper and no independent evaluation appear in the sources read. An arXiv listing search for the exact name returned no result on 20261102 20:20, which covers listed metadata only [9].

| Claim | Test | Who ran it | First-party | Date | Source |
|---|---|---|---|---|---|
| About 63x median token reduction per question, range 35x to 358x | Graph answer against the whole corpus as input; 5 sample questions; the 358x maximum is one repository (fastapi) | Maintainers | yes | 20260802 | [3] |
| Impact F1 (a score that balances precision and recall) 0.69 on average (precision 0.55), recall 1.0 | 13 commits; ground truth is changed files plus files with edges into them, taken from the same graph | Maintainers | yes | unstated | [3] |
| Multi-hop retrieval score 0.909, up from 0.545 | 11 curated two-step tool-chain tasks, version 2.3.5 | Maintainers | yes | roadmap read 20261102 | [6] |
| Token estimate within about 1% of real tokens | 222 sample files, OpenAI `cl100k_base` tokenizer | Maintainers | yes | README read 20261102 | [3] |

The README states the limits itself:

- the baseline is "an upper bound no real agent pays", since an agent greps for identifiers [3];
- recall of 1.0 is circular, because the ground truth comes from the same graph [3];
- the benchmark that grades against a grep-and-read baseline has no published canonical capture [3];
- the co-change mode predicted no files on any graded commit, so it quotes no number [3];
- small single-file changes can cost more tokens with the graph [3].

The project's own FAQ still quotes about 65x median and a 36x to 376x range, which differ from the README's 63x and 35x to 358x [3][7]. The FAQ says [grep](../index/grep.md) and [agentic search](../trends/agentic-search.md) suit one-hop lookups and the graph wins on multi-hop questions; the passage read gives no measurement [7].

*Reading:* the numbers show that a graph answer is far smaller than a whole corpus, which no agent reads. They do not show that review quality improves, and by the authors' own account the comparison with a grep-using agent is not yet published.

## Status and direction

The repository is active and not archived [1]. The latest release is v2.3.9, published 20260918 19:41 UTC, and the API lists 30 releases from v1.1.0 (20260226) [4]. Two releases (v2.3.8 and v2.3.9) fall in the 90 days since 20260804 [4]. The last release is 45 days old at the read.

The default branch is `staging`; pull requests target it, a daily workflow promotes it to `testing` when checks pass, and promotion to `main` is manual, with releases tagged from `main` [3]. In the 90-day window `staging` received 354 commits and `main` 323 [5]. The newest commit on `staging` is dated 20261015, 18 days before the read, and the newest commits on `main` and `testing` are dated 20260918, the day of v2.3.9 [5][8]. The owner's account holds 885 contributions, the next contributor 23 [8].

The roadmap lists three planned items: a GitHub App or bot mode, team sync through a git-tracked database, and performance beyond 50,000 files [6]. The sources read show no maintenance-mode notice and no hosted or paid tier [1][3].

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [codebase-memory-mcp](codebase-memory-mcp.md)
- [Projects](README.md)

**Index**

- [Code graph](../index/code-graph.md)
- [Impact analysis](../index/impact-analysis.md)
- [Tree-sitter](../index/tree-sitter.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/tirth8205/code-review-graph : repository metadata through the GitHub API (description, language, licence field, archived flag, default branch) (read 20261102 20:18 UTC)
2. https://github.com/tirth8205/code-review-graph/blob/staging/LICENSE : licence text and copyright line, through the API licence endpoint (read 20261102 20:18 UTC)
3. https://github.com/tirth8205/code-review-graph/blob/staging/README.md : description, architecture, features, benchmarks and limitations, branching, licence (read 20261102 20:18 UTC)
4. https://github.com/tirth8205/code-review-graph/releases : latest release and release list through the GitHub API (read 20261102 20:19 UTC)
5. https://api.github.com/repos/tirth8205/code-review-graph/commits?sha=staging&since=2026-08-04T00:00:00Z&per_page=1 and the same URL with `sha=main` : with one entry per page, the last page number in the `Link` header is the commit count, 354 and 323; the same URLs without `since` give the newest commit, 20261015 and 20260918 (read 20261102 20:36 UTC)
6. https://github.com/tirth8205/code-review-graph/blob/staging/docs/ROADMAP.md : shipped, planned and ongoing items; multi-hop benchmark (read 20261102 20:19 UTC)
7. https://github.com/tirth8205/code-review-graph/blob/staging/docs/FAQ.md : comparison with grep and agentic search, the 65x figure (read 20261102 20:19 UTC)
8. https://api.github.com/repos/tirth8205/code-review-graph/commits?sha=testing&per_page=1 : newest commit on `testing`, 20260918; https://api.github.com/repos/tirth8205/code-review-graph/branches : branch list; https://api.github.com/repos/tirth8205/code-review-graph/contributors : contributions per account, 885 and 23 for the first two (read 20261102 20:36 UTC)
9. https://arxiv.org/search/?query=%22code-review-graph%22&searchtype=all : exact-name search, no results (read 20261102 20:20 UTC)
