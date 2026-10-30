---
slug: kag
repo: OpenSPG/KAG
tier: card
category: core
snapshot: 20261030 19:40 UTC
---

# KAG

| | |
|---|---|
| Repository | https://github.com/OpenSPG/KAG [1] |
| Licence | Apache-2.0, from the `LICENSE` file (Apache License 2.0 text; head and tail read) [2]; the README licence section agrees [3]. |
| Language | Python (GitHub primary language) [1]; the engine it builds on is Java [8] |
| Stars, forks | 9,140, 719 (20261030 19:40 UTC; the 19:13 UTC landscape snapshot has the same figures) [1][4] |
| Created, last push | 20240921 13:56 UTC, 20260128 13:30 UTC [1] |
| Latest release | v0.8.0, 20250628 04:45 UTC; six GitHub releases, from v0.5 (20241104) [5]. PyPI `openspg-kag` lists 0.8.0, uploaded 20250630 09:20 UTC [6]. |
| Status | quiet: 275 days since the last push (heuristic flag `quiet` in the snapshot; computed again at read time); not archived [1][4] |
| Paper, docs | arXiv 2409.13731, cited by the README; a user guide and a website are linked; none fetched [3] |

## What it is

KAG ("Knowledge Augmented Generation") describes itself as a logical reasoning and Q&A framework "based on the OpenSPG engine and large language models", for vertical-domain knowledge bases [3]. The README says it avoids the ambiguity of vector-similarity RAG and the OpenIE noise of GraphRAG and is "significantly better than the current SOTA method"; the README gives no numbers, and the paper was not read here [3]. On the engine: the install steps start the OpenSPG server from a Docker Compose file in the `OpenSPG/openspg` repository, and a benchmark README calls it KAG's "dependency" [3][9]. That repository describes OpenSPG as a knowledge graph engine developed by Ant Group with OpenKG, with "natively support KAG" among its capabilities; it is also Apache-2.0 [8].

## How it works

The README names three parts, kg-builder, kg-solver and kag-model; only the first two are released [3]. The builder turns structured and unstructured data into a graph with a mutual index between nodes and source chunks, allowing schema-free and schema-constrained extraction on the same types [3]. Version 0.8.0 adds built-in index types (Outline, Summary, KnowledgeUnit, AtomicQuery, Chunk, Table) [3]. The solver turns a question into planning, reasoning and retrieval steps guided by logical forms [3]. Schemas are committed with the `knext` command line; extraction, chat and embedding models are set in YAML [9]. The 0.8.0 notes add MCP support, and the repository has an MCP server module [3][10]. Storage backends: unstated in the files read.

## Status and direction

Quiet by the heuristic; not archived. After v0.8.0, `master` gained nine commits: eight to 20250806, then a merged pull request on 20260128 fixing MCP store-path initialisation [7]. The engine repository's newest default-branch commit and release v0.8 are dated 20250629 [8]. Open: 164 issues and 10 pull requests; none of 12 comments since 20260201 comes from an owner, member or collaborator [11]. "Future Plans" gives no dates [3]. Reason for the quiet period: unstated.

## Sources

1. https://github.com/OpenSPG/KAG : repository metadata via the GitHub API (stars, forks, licence field, dates, language, archived flag, homepage) (read 20261030 19:40 UTC)
2. https://github.com/OpenSPG/KAG/blob/master/LICENSE : Apache License 2.0 text, 201 lines (read 20261030 19:40 UTC)
3. https://github.com/OpenSPG/KAG/blob/master/README.md : description, features, 0.8.0 release notes, quick start, architecture, citation, licence section (read 20261030 19:40 UTC)
4. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : the row for this repository: flag `quiet`, 275 days since the last push (read 20261030 19:40 UTC)
5. https://github.com/OpenSPG/KAG/releases : six releases, v0.5 (20241104) to v0.8.0 (20250628) (read 20261030 19:40 UTC)
6. https://pypi.org/pypi/openspg-kag/json : latest version 0.8.0 and upload times (read 20261030 19:41 UTC)
7. https://github.com/OpenSPG/KAG/commits/master : 100 newest commits, 20250616 to 20260128, and their subjects (read 20261030 19:40 UTC)
8. https://github.com/OpenSPG/openspg : repository metadata (Java, Apache-2.0 field, 2,285 stars, last push), description, newest commits and latest release v0.8; `LICENSE` head read (read 20261030 19:41 UTC)
9. https://github.com/OpenSPG/KAG/blob/master/kag/open_benchmark/hotpotqa/README.md : reproduction steps with `knext`, model configuration names, the OpenSPG server as a dependency (read 20261030 19:41 UTC)
10. https://github.com/OpenSPG/KAG/tree/master/kag/mcp : `kag_mcp_server.py` in the file tree (read 20261030 19:40 UTC)
11. https://github.com/OpenSPG/KAG/issues : open issue and pull request counts via the search API, newest issues and pull requests, and the author association labels of issue and pull request comments since 20260201 (read 20261030 19:41 UTC)
