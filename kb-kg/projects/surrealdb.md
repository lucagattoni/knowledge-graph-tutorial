---
slug: surrealdb
repo: surrealdb/surrealdb
tier: card
category: adjacent
snapshot: 20261030 19:40 UTC
---

# SurrealDB

| | |
|---|---|
| Repository | https://github.com/surrealdb/surrealdb [1] |
| Licence | GitHub reports NOASSERTION [1]. The `LICENSE` file is the Business Source License 1.1 (SPDX BUSL-1.1) with these parameters: licensor SurrealDB Ltd.; Licensed Work "SurrealDB 3.0"; Additional Use Grant: "You may make use of the Licensed Work, provided that you may not use the Licensed Work as a Database Service", defined as a product, service, platform or commercial offering in which the work provides database functionality to third parties (not your direct employees or contractors) that lets them create, manage or control schemas or tables; Change Date 2030-01-01; Change License Apache 2.0 [2]. The text says the licence applies separately to each version and takes effect on the Change Date or the fourth anniversary of a version's first public distribution, whichever comes first [2]. The file names version 3.0 only; the terms for the 2.x line, which still publishes releases (v2.7.0), are unstated here [2][4]. The README agrees: BSL 1.1 for core code in this repository, Apache 2.0 or MIT for SDKs and certain core components in separate repositories [3]. No legal advice. |
| Language | Rust (GitHub primary language) [1] |
| Stars, forks | 33,252, 1,397 (20261030 19:40 UTC; the landscape snapshot of 20261030 19:13 UTC has the same figures) [1][11] |
| Created, last push | 20211209 15:03 UTC, 20261029 00:36 UTC [1] |
| Latest release | v3.3.5, 20261029 00:36 UTC [4] |
| Status | active: 1 day since the last push (computed); no snapshot flag [11] |
| Paper, docs | surrealdb.com/docs [3][6]; a paper is unstated |

## What it is

SurrealDB is a multi-model database written in Rust: document, graph, relational, time-series, geospatial and key-value data in one engine, queried in SurrealQL, an SQL-like language, with full-text, vector and hybrid search [3]. It runs embedded, in the browser through WebAssembly, as one server or as a distributed cluster [3]. The README lists "data layer for AI agents, knowledge graphs" among its uses [3]. The docs describe a "SurrealDB Agent Memory" built on the database: typed memory, a knowledge graph of entities and typed relationships, and provenance with time, where a superseded belief is "end-dated rather than overwritten" [10]. The snapshot files SurrealDB as adjacent [11].

## How it works

Graph edges are records in their own tables, created with `RELATE`, able to hold fields, and traversed with arrows such as `->wrote->article` [7]. `DEFINE INDEX` supports full-text (analyzer, optional BM25), HNSW and DISKANN vector indexes [6]; the source tree has `hnsw`, `diskann` and full-text modules and `search::rrf` and `search::linear` functions to fuse results [9]. Whether it generates embeddings is unstated. A built-in MCP server ships with `surreal start` (HTTP at `/mcp`) and as `surreal mcp` (stdio); it has 14 tools, among them `query`, `select`, `create`, `relate`, `run` and `graphql`, and applies the database's own permissions [8].

## Status and direction

Releases: v3.3.0 (20260928), v3.3.1 to v3.3.4 (20261019), v3.3.5 (20261029); v3.2.6 and v2.7.0 also appear [4]. The commits API lists 3 commits on `main` since 20260801, the latest dated 20260904, while v3.3.5 targets `main`; the sources do not explain the gap [4][5]. The index docs cite features "since v4.0.0", though the latest release is v3.3.5 [6]. A roadmap is unstated.

## Sources

All read on 20261030 between 19:40 and 19:47 UTC.

1. https://github.com/surrealdb/surrealdb : repository metadata via the GitHub API
2. https://github.com/surrealdb/surrealdb/blob/main/LICENSE : BSL 1.1 parameters and text
3. https://github.com/surrealdb/surrealdb/blob/main/README.md : description, features, licence section
4. https://github.com/surrealdb/surrealdb/releases : release list via the GitHub API
5. https://github.com/surrealdb/surrealdb/commits/main : commits since 20260801 via the GitHub API
6. https://surrealdb.com/docs/surrealql/statements/define/indexes : index kinds, BM25, HNSW, DISKANN, version notes
7. https://surrealdb.com/docs/surrealql/statements/relate : edge records and arrow traversal
8. https://github.com/surrealdb/surrealdb/blob/main/surrealdb/mcp/README.md and `surrealdb/mcp/src/service.rs` : transports, security model, tool list
9. https://github.com/surrealdb/surrealdb/tree/main/surrealdb/core/src : directory listings of `idx/trees`, `idx/ft` and `fnc`, and the function names in `fnc/search.rs`
10. https://surrealdb.com/docs/surrealdb/mcp : page text on Agent Memory and retrieval (HNSW, BM25, graph traversal, reciprocal rank fusion); the pages it links were not fetched
11. [landscape snapshot](../landscape/20261030_1913-github/repos.tsv) : snapshot row (stars 33,252, forks 1,397, flags empty), read from this repository
