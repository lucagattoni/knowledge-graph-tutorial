---
slug: graphrag-sdk
repo: FalkorDB/GraphRAG-SDK
tier: card
category: core
snapshot: 20261030 19:39 UTC
---

# GraphRAG SDK (FalkorDB)

| | |
|---|---|
| Repository | https://github.com/FalkorDB/GraphRAG-SDK [1] |
| Licence | Apache-2.0, from the `LICENSE` file (Apache License 2.0 text; head and tail read) [2]. README and `pyproject.toml` agree [3][9]. The database it needs, FalkorDB, is under SSPL v1 [10]. |
| Language | Python [1] |
| Stars, forks | 1,029, 147 (20261030 19:39 UTC; the landscape snapshot of 20261030 19:13 UTC has the same figures) [1] |
| Created, last push | 20240125 05:54 UTC, 20261030 14:16 UTC [1] |
| Latest release | v1.5.0, 20261022 13:38 UTC [4]. PyPI's newest version is 1.4.0 (20260810 13:57 UTC); the 1.5.0 page returned 404 [5]. |
| Status | active (pushed within 90 days; no snapshot flag) [1] |
| Paper, docs | no paper; docs in `docs/` and at docs.falkordb.com/graphrag [3][6] |

## What it is

A Python library from FalkorDB that turns documents into a knowledge graph in FalkorDB and answers questions from it with source citations, per its README [3]. The README claims "benchmark-leading accuracy": 71.48 overall on GraphRAG-Bench ([background](../papers-benchmarks/README.md)) against 55.39 for vector RAG with reranking [3]. The project ran its own system (SDK 1.3.0, `gpt-4o-mini`, August 2026) and took competitor figures from the leaderboard without re-running them; it lists judge variance and two domains as limits, and says "Overall" is its own average [8]. I could not check the rows: the leaderboard page returned empty tables and neither it nor the benchmark README names FalkorDB [11]. No evaluation by anyone else was found in the sources read. The SDK needs FalkorDB server 4.20 or later [3].

## How it works

Ingestion runs nine steps: load, chunk, lexical graph (Document and Chunk nodes), extract, prune to the schema, resolve, write, then mention links and chunk embeddings [6]. The extraction page and code make a local GLiNER model the default first step, with an LLM verifying entities and extracting relationships [7][9]; the architecture page says only "LLM" [6]. Cross-document deduplication runs in `finalize()` with an LLM judge [3][6]. Retrieval starts with an LLM keyword step, combines relationship-vector search, entity discovery, four chunk paths, two-hop expansion and cosine reranking, then makes one LLM answer call [6]. The interface is a Python API with an optional ontology; no path in the repository tree mentions MCP [3][12].

## Status and direction

Active: 388 commits on the default branch since 20260731, 32 releases (20240606 to 20261022), 11 contributors, 40 open issues and 32 open pull requests [4][12]. The README roadmap lists "Agentic GraphRAG" for 2026-Q3 and dynamic traversal plus a temporal graph for Q4 [3]. The agentic work is still open: issue #338 (20261011) and three pull requests from 20260622 to 20260712 [13]. `CHANGELOG.md` has no 1.5.0 section [14].

## Sources

1. https://github.com/FalkorDB/GraphRAG-SDK : repository metadata via the GitHub API (read 20261030 19:39 UTC)
2. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/LICENSE : Apache License 2.0 text (read 20261030 19:40 UTC)
3. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/README.md : description, benchmark table, pipeline, roadmap (read 20261030 19:39 UTC)
4. https://github.com/FalkorDB/GraphRAG-SDK/releases : 32 releases, v1.5.0 notes (read 20261030 19:40 UTC)
5. https://pypi.org/pypi/graphrag-sdk/json : PyPI versions; the 1.5.0 JSON URL returned 404 (read 20261030 19:39 and 19:40 UTC)
6. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/architecture.mdx : ingestion steps, graph schema, retrieval flow (read 20261030 19:40 UTC)
7. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/extraction.mdx : GLiNER default plus LLM step (read 20261030 19:40 UTC)
8. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/graphrag-accuracy-benchmark.mdx : benchmark setup and limitations (read 20261030 19:40 UTC)
9. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/graphrag_sdk/pyproject.toml : licence field, dependencies, and `graph_extraction.py` default extractor (read 20261030 19:41 UTC)
10. https://github.com/FalkorDB/FalkorDB : its `LICENSE` file begins with the Server Side Public License v1; the README says SSPLv1 (read 20261030 19:40 UTC)
11. https://graphrag-bench.github.io/ and https://github.com/GraphRAG-Bench/GraphRAG-Benchmark : leaderboard page and README (read 20261030 19:45 UTC)
12. https://github.com/FalkorDB/GraphRAG-SDK/commits/main : commit count since 20260731, contributors, file tree, open issues and pull requests (read 20261030 19:40 UTC)
13. https://github.com/FalkorDB/GraphRAG-SDK/issues/338 : open issue, and open pull requests #274 to #276, found by search (read 20261030 19:45 UTC)
14. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/CHANGELOG.md : section headings (read 20261030 19:45 UTC)
