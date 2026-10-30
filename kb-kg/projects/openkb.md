---
slug: openkb
repo: VectifyAI/OpenKB
tier: card
category: markdown-kb
snapshot: 20261030 19:35 UTC
---

# OpenKB

| | |
|---|---|
| Repository | https://github.com/VectifyAI/OpenKB [1] |
| Licence | Apache-2.0, from the `LICENSE` file (Apache License 2.0 text; head and tail read) [2]. The README licence section says "Apache 2.0", so they agree [3]. |
| Language | Python (GitHub primary language) [1] |
| Stars, forks | 4,831, 503 (20261030 19:34 UTC; the landscape snapshot of 20261030 19:13 UTC has the same figures) [1] |
| Created, last push | 20260404 12:26 UTC, 20260722 03:45 UTC [1] |
| Latest release | v0.4.5, 20260720 10:35 UTC, a dependency-pin hotfix [4]. PyPI lists 0.4.5 as the version and also holds the pre-release 0.5.0rc1, uploaded 20260720 15:27 UTC, which has no GitHub release [6]. |
| Status | quiet: 100 days since the last push at the snapshot (heuristic flag `quiet`); not archived [1] |
| Paper, docs | no paper stated; the README and a `docs/` directory; the homepage field points to pageindex.ai (not fetched) [1][3] |

## What it is

OpenKB is an open-source command-line system that, in its own words, compiles raw documents into a structured, interlinked, wiki-style knowledge base using LLMs, with PageIndex handling long documents [3]. The README says the idea is based on a concept described by Andrej Karpathy: LLMs write and maintain summaries, concept pages and cross-references, so knowledge accumulates instead of being re-derived at each query [3]. The wiki is plain Markdown with cross-links that opens in Obsidian, and the README says its pages follow Google's Open Knowledge Format [3]. No benchmark or evaluation appears in the README [3].

## How it works

Short documents are converted to Markdown and read in full by the LLM; PDFs of 20 pages or more go through PageIndex into a tree index with summaries, and the LLM reads the tree [3]. For each added document the LLM writes a summary page, reads existing concept and entity pages, creates or updates them, and updates an index and a log; one source may touch 10 to 15 pages [3]. The README says "No Vector DB". LLMs are reached through LiteLLM with the user's API key [3]. A local REST API and web UI are bundled [3]. For agents it ships a `SKILL.md`, with "no MCP setup" [3].

## Status and direction

Quiet, not archived. Main had 175 commits (20260401 to 20260722) and 14 releases, five of them release candidates (20260515 to 20260720); since then none, and `dev` stopped on 20260618 [4][5][8]. 37 pull requests are open; the five latest closed were unmerged; none of 41 comments since 20260723 is from an owner, member or collaborator [9][10]. PageIndex was pushed 20261029 [7]. Reason for the pause: unstated. Roadmap: four items unchecked [3].

## Sources

1. https://github.com/VectifyAI/OpenKB : repository metadata via the GitHub API (stars, forks, licence field, dates, language, branches) (read 20261030 19:34 UTC)
2. https://github.com/VectifyAI/OpenKB/blob/main/LICENSE : Apache License 2.0 text (read 20261030 19:34 UTC)
3. https://github.com/VectifyAI/OpenKB/blob/main/README.md : description, architecture, commands, roadmap, licence section (read 20261030 19:35 UTC)
4. https://github.com/VectifyAI/OpenKB/releases : 14 releases from v0.1.4 (20260515) to v0.4.5 (20260720), and the v0.4.5 notes (read 20261030 19:35 UTC)
5. https://github.com/VectifyAI/OpenKB/commits/main : recent commit subjects and commits per month since 20260401 (read 20261030 19:35 UTC)
6. https://pypi.org/pypi/openkb/json : PyPI version and upload times (read 20261030 19:34 UTC)
7. https://github.com/VectifyAI/PageIndex : sibling repository, last push 20261029 22:48 UTC (read 20261030 19:34 UTC)
8. https://github.com/VectifyAI/OpenKB/tree/dev : the `dev` branch, last commit 20260618 18:49 UTC, 9 ahead and 107 behind main; the other five branches were not inspected (read 20261030 19:34 UTC)
9. https://github.com/VectifyAI/OpenKB/pulls : open and closed pull requests via the pulls and search APIs; 37 open pull requests and 47 open issues (read 20261030 19:34 UTC)
10. https://github.com/VectifyAI/OpenKB/issues : issue and pull request comments since 20260723 and their author association labels (read 20261030 19:35 UTC)
