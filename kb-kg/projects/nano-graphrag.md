---
slug: nano-graphrag
repo: gusye1234/nano-graphrag
tier: card
category: core
snapshot: 20261030 19:40 UTC
---

# nano-graphrag

| | |
|---|---|
| Repository | https://github.com/gusye1234/nano-graphrag [1] |
| Licence | MIT, from the `LICENSE` file (standard MIT text, 21 lines, copyright 2024) [2]. The README has no licence section; GitHub's licence field also says MIT [1][3]. |
| Language | Python (GitHub primary language) [1] |
| Stars, forks | 4,006, 427 (20261030 19:40 UTC; the 19:13 UTC landscape snapshot has the same figures) [1][4] |
| Created, last push | 20240725 07:53 UTC, 20260127 07:50 UTC [1] |
| Latest release | v0.0.8, 20241001 16:00 UTC; four GitHub releases in all, v0.0.5 to v0.0.8 [5]. PyPI lists 0.0.8.2, uploaded 20241019 13:06 UTC [6]. |
| Status | quiet: 276 days since the last push (heuristic flag `quiet` in the snapshot; computed again at read time); not archived [1][4] |
| Paper, docs | no paper of its own; the README links the GraphRAG paper (arXiv 2404.16130, not fetched). `docs/` holds a FAQ, a ROADMAP and benchmark notes [3][7] |

## What it is

nano-graphrag is a small Python reimplementation of GraphRAG. Its README calls it "a simple, easy-to-hack GraphRAG implementation", says the official implementation is hard to read or hack, and puts the code at about 1,100 lines excluding tests and prompts (the project's figure; not counted here) [3]. It lists two differences from the original: no `covariates`, and a global search that by default uses the top 512 central communities instead of a map-reduce over all of them [3]. Its benchmark note covers one book: indexing took more than 5 minutes with the official code and under 4 with nano-graphrag; the project ran it [7]. The README names four projects that used it, including LightRAG [3].

## How it works

`insert` splits text into chunks (default 1,200 tokens, 100 overlap), has an LLM extract entities and relations (up to one gleaning round by default) and merges them into a graph, NetworkX by default and Neo4j optionally [3][8]. The graph is clustered with Leiden (default maximum cluster size 10) and the LLM writes a report per community [3][8]. `query` has local, global and optional naive chunk modes [3]. Two model slots, "best" and "cheap", default to GPT-4o and GPT-4o-mini; Bedrock, Azure, DeepSeek and Ollama are supported [3][8]. Each insert recomputes communities and regenerates reports [3]. No MCP or agent interface is described; it is a library [3].

## Status and direction

Quiet by the heuristic; not archived. Since v0.0.8 (20241001), `main` has gained 22 commits, the last on 20260127; the six newest came from two non-owner accounts, one of them a collaborator [10][11]. Open: 67 issues and 16 pull requests; the newest issue is dated 20260225 [11]. Two pull requests were closed unmerged, on 20260911 and 20260917 [11]. Every ROADMAP item is unchecked, none dated [9]. Reason for the quiet period: unstated. Whether it is maintained: unstated.

## Sources

1. https://github.com/gusye1234/nano-graphrag : repository metadata via the GitHub API (stars, forks, licence field, dates, language, archived flag) (read 20261030 19:40 UTC)
2. https://github.com/gusye1234/nano-graphrag/blob/main/LICENSE : MIT License text (read 20261030 19:40 UTC)
3. https://github.com/gusye1234/nano-graphrag/blob/main/readme.md : description, components, quick start, differences from the original, projects that used it (read 20261030 19:40 UTC)
4. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : the row for this repository: flag `quiet`, 276 days since the last push (read 20261030 19:40 UTC)
5. https://github.com/gusye1234/nano-graphrag/releases : v0.0.5 to v0.0.8, 20240828 to 20241001 (read 20261030 19:40 UTC)
6. https://pypi.org/pypi/nano-graphrag/json : versions and upload times; latest 0.0.8.2 (read 20261030 19:40 UTC)
7. https://github.com/gusye1234/nano-graphrag/blob/main/docs/benchmark-en.md : the indexing-time comparison and its setup; the `docs/` directory listing (read 20261030 19:40 UTC)
8. https://github.com/gusye1234/nano-graphrag/blob/main/nano_graphrag/graphrag.py : default parameters (chunk size, gleaning, clustering, model slots) (read 20261030 19:40 UTC)
9. https://github.com/gusye1234/nano-graphrag/blob/main/docs/ROADMAP.md : all items unchecked: DSPy prompt tuning, a `global_local` query method, a rate limiter, HybridRAG, HippoRAG, a Triplex extraction model, new components (read 20261030 19:40 UTC)
10. https://github.com/gusye1234/nano-graphrag/commits/main : 100 newest commits, 20240826 to 20260127, with authors of the six newest (read 20261030 19:40 UTC)
11. https://github.com/gusye1234/nano-graphrag/pulls : open and closed pull requests, open issue and pull request counts via the issues and search APIs, and the author association labels of recent comments (read 20261030 19:40 UTC)
