---
slug: a-mem
repo: agiresearch/A-mem
tier: card
category: agent-memory
snapshot: 20261030 19:39 UTC
---

# A-mem

| | |
|---|---|
| Repository | https://github.com/agiresearch/A-mem [1] |
| Licence | MIT, from the `LICENSE` file ("MIT License", copyright 2025 AGI Research; head and tail read) [2]. The README licence section and GitHub's field also say MIT [1][3]. |
| Language | Python [1] |
| Stars, forks | 1,212, 124 (20261030 19:39 UTC; the landscape snapshot of 20261030 19:13 UTC has 1,212 and 123, forks per 100 stars 10.15) [1][4] |
| Created, last push | 20250225 20:13 UTC, 20251212 21:15 UTC [1] |
| Latest release | none: no GitHub release and no tags [1][5]. `pyproject.toml` names the package `agentic-memory`, version 0.0.1; PyPI not checked [9] |
| Status | quiet: 321 days since the last push at the snapshot (heuristic flag `quiet`); not archived [1][4] |
| Paper, docs | arXiv 2502.12110, NeurIPS 2025 per the arXiv comments field [6]; the README is the only documentation found |

## What it is

A-mem is the code released with the paper "A-MEM: Agentic Memory for LLM Agents" [3][6]. The README calls it a memory system to help build agents, and sends readers who want to reproduce the paper's results to a different repository, WujiangXu/AgenticMemory [3]. The abstract describes the method as Zettelkasten-based: a new memory becomes a note with a contextual description, keywords and tags, is linked to related past memories, and may update them [6]. Its only quantitative claim is that experiments on six foundation models show "superior improvement against existing SOTA baselines" [6]. Independent evaluation: none read.

## How it works

A note holds content, keywords, context, tags, links, timestamps and an evolution history, kept in a Python dict and embedded in ChromaDB (default model all-MiniLM-L6-v2) [9]. On add, the five nearest notes are fetched and one LLM call decides whether to link the new note or rewrite its neighbours' context and tags; every 100 evolutions the index is rebuilt [9]. Backends: OpenAI or Ollama; Python class only; MCP unstated [3]. README versus code, read 20261030: the routine that has an LLM write keywords, context and tags (`analyze_content`) has no caller in the package (open issue #10) [8][9]; the default retriever uses a non-persistent ChromaDB client, though the README lists persistent storage [3][9].

## Status and direction

Quiet, not archived (heuristic flag). Main: 31 commits, 12 in March 2025, 12 in October 2025, 2 in December 2025, none since [7]. 20 open issues and 1 open pull request, #36 (20261023) [1][8]. In #10, on 20250714, the top committer says they have no access here and will continue at WujiangXu/A-mem-sys (pushed 20260315); the paper repository was pushed 20261028 [8][10]. #16 asks "Is this project dead already?"; one third-party comment [8]. Reason: unstated.

## Sources

1. https://github.com/agiresearch/A-mem : repository metadata via the GitHub API (stars, forks, licence field, dates, open issue count, tags, contributors) (read 20261030 19:39 UTC)
2. https://github.com/agiresearch/A-mem/blob/main/LICENSE : MIT License text (read 20261030 19:39 UTC)
3. https://github.com/agiresearch/A-mem/blob/main/README.md : description, features, usage, backends, licence section (read 20261030 19:39 UTC)
4. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : the first landscape snapshot row for this repository (read 20261030 19:39 UTC)
5. https://github.com/agiresearch/A-mem/releases : no release; the latest-release call returned 404 (read 20261030 19:39 UTC)
6. https://arxiv.org/abs/2502.12110 : abstract, venue and versions of the paper (read 20261030 19:41 UTC)
7. https://github.com/agiresearch/A-mem/commits/main : commit subjects, authors and commits per month (read 20261030 19:40 UTC)
8. https://github.com/agiresearch/A-mem/issues : the 30 most recently updated issues and pull requests, and the comments on #10 and #16 (read 20261030 19:42 UTC)
9. https://github.com/agiresearch/A-mem/blob/main/agentic_memory/memory_system.py : note model, evolution prompt and logic; also `retrievers.py` and `pyproject.toml` in the same directory tree (read 20261030 19:42 UTC)
10. https://github.com/WujiangXu/A-mem-sys and https://github.com/WujiangXu/AgenticMemory : push dates, stars, licence (read 20261030 19:42 UTC)
