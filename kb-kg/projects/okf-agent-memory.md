---
slug: okf-agent-memory
repo: okf-memory/okf-agent-memory
tier: card
category: markdown-kb
snapshot: 20261030 19:40 UTC
---

# OKF Agent Memory

| | |
|---|---|
| Repository | https://github.com/okf-memory/okf-agent-memory [1] |
| Licence | MIT, from the `LICENSE` file (head and tail read) [2]. The README badge and licence line say MIT: they agree [3]. |
| Language | Go (GitHub primary language) [1] |
| Stars, forks | 846, 68 (20261030 19:40 UTC; the landscape snapshot of 19:13 UTC shows 845, 68; no heuristic flag) [1] |
| Created, last push | 20260905 21:26 UTC, 20261029 12:37 UTC [1] |
| Latest release | v0.7.2, 20261028 17:06 UTC [1] |
| Status | active (pushed within 90 days); not archived [1] |
| Paper, docs | no paper stated; README and `docs/`; homepage okf-memory.dev (not fetched) [1][3] |

## What it is

A Go library, command-line tool and MCP server (`okf`) that keeps an agent's project memory as a git-tracked folder of Markdown files with YAML frontmatter [3]. The README says it implements Google's Open Knowledge Format (OKF) v0.2, plus a "search before write" convention and a two-layer design: a short always-loaded rules file and the folder, searched on demand [3]. The latency and token figures are the project's own: no source is given for the Mem0 and Letta ranges, the token table reports one local-model run, and seven result files were not read [3][10][1].

**Does it implement OKF v0.2?** Mostly, with two gaps. The project's compatibility note says "100% compliant" [4]. The validator requires frontmatter and a non-empty `type` and checks `log.md` dates, `status`, `generated`, `verified` and `sources`; its own keys (`governance`, `code_refs`) are extensions the specification allows [5][6][7].

1. `stale_after` and `sources[].last_modified`: since 20260820 the specification, still headed "Version 0.2", requires ISO 8601 datetimes [7][8]. The type definition and validator expect `YYYY-MM-DD` and warn on other forms [5][6].
2. Attested Computation: the note claims full support [4]; the code defines a struct, but 13 other files held no reference to it [6][11].

I read the code and did not run it. The README links a specification copy marked a frozen snapshot; on 20261030 it matched the current text [3][9].

## How it works

A bundle is a `knowledge/` folder of concept files with `index.md` and `log.md` [3]. The `okf` binary validates bundles, scores them on a quality scorecard, creates and updates concepts while keeping index and log in step, and searches with in-memory BM25 over frontmatter and body; there are no embeddings and no database [3][11]. Four scopes (project, vendor, user, system) layer bundles, higher ones shadowing lower [3]. `okf mcp` serves six tools over stdio: search, show, validate, create, update, relate [11]. A skill in `.agents/skills/okf-memory/` tells agents to search first [1]. A sync hub and a registry also exist [3].

## Status and direction

Active. 22 releases from v0.1.0 (20260905) to v0.7.2 (20261028); 236 commits since 20260901, 179 in September and 57 in October [1]. One account holds 208 of the contributions listed, among ten accounts including bots [1]. Open: one pull request, two issues [1]. Direction: unstated in the sources read.

## Sources

1. https://github.com/okf-memory/okf-agent-memory : API data: metadata, releases, contributors, commits, issues, file tree (read 20261030 19:40 to 19:45 UTC)
2. https://github.com/okf-memory/okf-agent-memory/blob/develop/LICENSE : MIT text (read 20261030 19:40 to 19:45 UTC)
3. https://github.com/okf-memory/okf-agent-memory/blob/develop/README.md : claims, benchmark table, scopes (read 20261030 19:40 to 19:45 UTC)
4. https://github.com/okf-memory/okf-agent-memory/blob/develop/docs/spec/OKF-COMPATIBILITY.md : compatibility note (read 20261030 19:40 to 19:45 UTC)
5. https://github.com/okf-memory/okf-agent-memory/blob/develop/pkg/okf/validator.go : validation rules (read 20261030 19:40 to 19:45 UTC)
6. https://github.com/okf-memory/okf-agent-memory/blob/develop/pkg/okf/types.go : concept fields (read 20261030 19:40 to 19:45 UTC)
7. https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md : OKF v0.2 text (read 20261030 19:40 to 19:45 UTC)
8. https://github.com/GoogleCloudPlatform/open-knowledge-format/commit/3dc3029 : the date-to-datetime change; issue 24 on the missing version bump (read 20261030 19:40 to 19:45 UTC)
9. https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf : frozen-snapshot banner; its `SPEC.md` compared with source 7 by `diff` (read 20261030 19:40 to 19:45 UTC)
10. https://github.com/okf-memory/okf-agent-memory/blob/develop/benchmarks/README.md : one local-model run (read 20261030 19:40 to 19:45 UTC)
11. 13 files in `pkg/okf/`, `internal/cli/` and the skill, searched for "attest" and "executor"; BM25 comment in `search.go`; `schemas/tools.json` for the tool names (read 20261030 19:40 to 19:45 UTC)
