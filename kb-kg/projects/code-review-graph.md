---
slug: code-review-graph
repo: tirth8205/code-review-graph
tier: card
category: adjacent
snapshot: 20261030 19:45 UTC
---

# code-review-graph

| | |
|---|---|
| Repository | https://github.com/tirth8205/code-review-graph [1] |
| Licence | MIT, from the `LICENSE` file (head and tail read; copyright Tirth Kanani) [2]. The README badge and licence section also say MIT, so they agree [3]. |
| Language | Python (GitHub primary language); the README gives Python 3.10 or later [1][3] |
| Stars, forks | 32,508, 2,957 (20261030 19:39 UTC; the landscape snapshot of 20261030 19:13 UTC has the same figures) [1][10] |
| Created, last push | 20260226 17:25 UTC, 20261029 10:34 UTC on any branch. The default branch is `staging`, whose newest commit is 20261015 13:23 UTC; `main` last moved 20260918 19:40 UTC [1][5]. |
| Latest release | v2.3.9, 20260918 19:41 UTC; 30 releases, v1.1.0 (20260226) to v2.3.9. PyPI also lists 2.3.9, uploaded the same minute [4][9]. |
| Status | active (pushed one day before the read); not archived [1]. No snapshot flag is set [10]. Context: 9.1 forks per 100 stars, 128 contributors on the contributors API (the snapshot lists 143), 102 open issues, 91 open and 345 merged pull requests [1][7][8][10]. |
| Paper, docs | no paper stated; the README, a `docs/` directory (usage, FAQ, reproduction recipe, roadmap) and the site https://code-review-graph.com (homepage field, not fetched) [1][3][6] |

## What it is

code-review-graph calls itself a local code knowledge graph that gives AI coding tools precise review context over MCP [3]. It parses a repository with Tree-sitter, keeps the graph updated incrementally, and serves compact context so the assistant reads only the files a change touches [3]. Its installer configures 16 named agent platforms, and a GitHub Action posts risk-scored review comments on pull requests [3]. The README reports its own benchmarks on six open-source repositories: a median per-question token reduction of about 63x against a whole-corpus baseline (range 35x to 358x), and an average impact F1 of 0.69 [3]. It states that the baseline is "an upper bound no real agent pays", that impact recall of 1.0 is circular because the ground truth comes from the same graph, and that no canonical agent-baseline capture is published yet [3]. I found no independent evaluation in the sources read [11].

## How it works

Tree-sitter parses the repository into nodes (functions, classes, imports) and edges (calls, inheritance, test coverage) kept in one SQLite file in `.code-review-graph/` [3]. Hooks, a pre-commit hook or watch mode re-parse only files whose SHA-256 hash changed [3]. For a change, a blast-radius step walks callers, dependents and tests to find the smallest set of files to read; Leiden clustering, execution flows and hub detection add structure [3]. Embeddings are optional, local or from cloud providers, and the README says there is no telemetry [3]. Agents use 30 MCP tools and 5 MCP prompts, or the CLI [3].

## Status and direction

Active. Per the README, changes move from `staging` (the default branch) to `main`, from which releases are tagged [3]. `staging` received 362 commits from 20260801 to 20261015, 302 under the name Tirth Kanani; the last release is 42 days old [4][5]. The roadmap lists three planned items: a GitHub App mode, team sync through a git-tracked database, and performance beyond 50,000 files [6]. 91 pull requests are open [7].

## Sources

1. https://github.com/tirth8205/code-review-graph : repository metadata via the GitHub API (read 20261030 19:39 UTC)
2. https://github.com/tirth8205/code-review-graph/blob/staging/LICENSE : MIT licence text, copyright line (read 20261030 19:44 UTC)
3. https://github.com/tirth8205/code-review-graph/blob/staging/README.md : description, architecture, benchmarks, limitations, branching note, licence (read 20261030 19:39 UTC; contributing and licence sections 19:45 UTC)
4. https://github.com/tirth8205/code-review-graph/releases : 30 releases and the v2.3.9 notes (read 20261030 19:44 UTC)
5. https://github.com/tirth8205/code-review-graph/commits/staging : commits since 20260801 (362, confirmed by the pagination header); newest commits on `staging` and `main` (read 20261030 19:44 and 19:45 UTC)
6. https://github.com/tirth8205/code-review-graph/blob/staging/docs/ROADMAP.md : shipped, planned and ongoing items (read 20261030 19:45 UTC)
7. https://github.com/tirth8205/code-review-graph/pulls : pull request and issue counts via the search API (read 20261030 19:44 UTC)
8. https://github.com/tirth8205/code-review-graph/graphs/contributors : contributor count via the contributors API (read 20261030 19:39 UTC)
9. https://pypi.org/pypi/code-review-graph/json : PyPI version 2.3.9 and its upload time (read 20261030 19:45 UTC)
10. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : first landscape snapshot row (snapshot 20261030 19:13 UTC)
11. [papers-benchmarks/README.md](../papers-benchmarks/README.md) : searched for the project name; no mention (searched 20261030 19:42 UTC)
