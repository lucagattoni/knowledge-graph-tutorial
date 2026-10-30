---
slug: ai-knowledge-graph
repo: robert-mcdermott/ai-knowledge-graph
tier: card
category: core
snapshot: 20261030 19:39 UTC
---

# AI Powered Knowledge Graph Generator

| | |
|---|---|
| Repository | https://github.com/robert-mcdermott/ai-knowledge-graph [1] |
| Licence | Apache-2.0, from the `LICENSE` file (Apache License 2.0 text; head and tail read) [2]. `pyproject.toml` points to that file and lists the Apache classifier [6]. The README has no licence section [3]. |
| Language | Python [1] |
| Stars, forks | 3,134, 421 (20261030 19:39 UTC; the landscape snapshot of 20261030 19:13 UTC has the same figures) [1] |
| Created, last push | 20250323 04:38 UTC, 20260913 23:17 UTC [1] |
| Latest release | v0.8.0, 20260912 20:39 UTC [4]. `pyproject.toml` on the default branch still says 0.7.0 [6]. PyPI returned 404 for the package name [5]. |
| Status | active: pushed 46 days before the read; no snapshot flag [1] |
| Paper, docs | no paper; the README, a docs site of sample graphs, and a Medium article named in the homepage field (not fetched) [1][3] |

## What it is

A small command-line tool that sends a text document to an LLM of the user's choice, collects Subject-Predicate-Object triples with entity types, and renders them as an interactive HTML graph, per the README [3]. Optional commands answer questions from the graph (`graph-chat`) and serve a local web interface (`graph-serve`) [3]. It stores nothing in a database: output is a JSON file of triples plus HTML, with optional CSV, GraphML and Cypher exports [3]. No benchmark appears in the README. The repository's own improvement plan reports an earlier test run with 1,058 inferred edges against 414 extracted, 962 of them from the transitive rule; the README says rule-based inference made about 70% of all edges in testing, so it is now off by default [3][7].

## How it works

Text is split into overlapping chunks of about 500 words. The LLM extracts typed triples from each chunk, each keeping its source sentence [3]. Standardisation merges case, plural and stop-word variants, with an optional LLM grouping call. Inference adds capped edges by LLM bridging, LLM hub enrichment and a taxonomy rule, each tagged with its method [3]. NetworkX finds communities; an LLM names them [3]. `graph-chat` matches entities named in the question, takes a two-hop subgraph and shortest paths, and asks the LLM to answer from those facts; the code matches words, with an optional LLM entity pick, and uses no embeddings [3][8]. The README says any OpenAI-compatible endpoint works [3]. The README describes no MCP or agent interface [3].

## Status and direction

Bursty. Default-branch commits: 53 in 202503, 11 across 202505 to 202512, none in 202601 to 202608, and 24 in 202609, all 24 by one author [9]. Releases: 0.6.3 (20251228), then v0.7.0 and v0.8.0 on 20260912 [4]. Three contributors, six open issues, two open pull requests [9][10]. The plan marks waves 1 to 15 done and leaves four items open, among them merging new documents into an existing graph [7].

## Sources

1. https://github.com/robert-mcdermott/ai-knowledge-graph : repository metadata via the GitHub API (read 20261030 19:39 UTC)
2. https://github.com/robert-mcdermott/ai-knowledge-graph/blob/main/LICENSE : Apache License 2.0 text (read 20261030 19:39 UTC)
3. https://github.com/robert-mcdermott/ai-knowledge-graph/blob/main/README.md : features, configuration, pipeline, commands (read 20261030 19:39 UTC)
4. https://github.com/robert-mcdermott/ai-knowledge-graph/releases : 18 releases, 0.1.0 (20250323) to v0.8.0, and notes for v0.7.0 and v0.8.0 (read 20261030 19:41 UTC)
5. https://pypi.org/pypi/ai-knowledge-graph/json : HTTP 404 (read 20261030 19:40 UTC)
6. https://github.com/robert-mcdermott/ai-knowledge-graph/blob/main/pyproject.toml : version, dependencies, licence field (read 20261030 19:41 UTC)
7. https://github.com/robert-mcdermott/ai-knowledge-graph/blob/main/IMPROVEMENT_PLAN.md : the author's audit, wave status, open items (read 20261030 19:41 UTC)
8. https://github.com/robert-mcdermott/ai-knowledge-graph/blob/main/src/knowledge_graph/query.py : question matching and subgraph retrieval (read 20261030 19:41 UTC)
9. https://github.com/robert-mcdermott/ai-knowledge-graph/commits/main : commits per month, authors since 20260801, contributor count (read 20261030 19:41 UTC)
10. https://github.com/robert-mcdermott/ai-knowledge-graph/issues : open issues and pull requests via the search API (read 20261030 19:42 UTC)
