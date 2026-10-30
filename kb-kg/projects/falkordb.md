---
slug: falkordb
repo: FalkorDB/FalkorDB
tier: card
category: adjacent
snapshot: 20261030 19:40 UTC
---

# FalkorDB

| | |
|---|---|
| Repository | https://github.com/FalkorDB/FalkorDB [1] |
| Licence | GitHub reports NOASSERTION [1]. The default-branch `LICENSE` file holds two texts in a row: the Server Side Public License v1 (16 October 2018, copyright MongoDB, Inc.), then the Elastic License 2.0 from line 563; nothing in the file says which applies to what [2]. The README names only SSPLv1, in a badge and two statements [3]. The 4.22.3 tag has an SSPL-only `LICENSE.txt` [4]; the 20260802 commit that migrated the default branch to the Rust engine lists `LICENSE` as an added file [5]. SSPL section 13: whoever offers the Program's functionality to third parties as a service must release the "Service Source Code" (the Program plus management, interface, API, automation, monitoring, backup, storage and hosting software) for free network download under the same licence [2]. ELv2 allows use, copying, distribution and derivative works, but not offering the software to third parties as a hosted or managed service giving access to a substantial set of its features, nor circumventing licence-key functionality [2]. No legal advice. |
| Language | Rust (GitHub primary language) [1] |
| Stars, forks | 10,506, 600 (20261030 19:40 UTC; the landscape snapshot of 20261030 19:13 UTC has 10,505 and 600) [1][13] |
| Created, last push | 20230720 10:47 UTC, 20261030 16:46 UTC [1] |
| Latest release | v6.0.3, 20261022 14:29 UTC (GitHub's latest-release call); v4.22.3, 20261028, is newer and belongs to the 4.x line [6] |
| Status | active: pushed the day it was read; no snapshot flag [13] |
| Paper, docs | docs.falkordb.com [7]; the README links a benchmark site, not fetched here [3]; a paper is unstated |

## What it is

FalkorDB is a graph database that runs as a Redis module: any Redis client sends `GRAPH.*` commands such as `GRAPH.QUERY` [3]. The GitHub description states the goal as "the best Knowledge Graph for LLM (GraphRAG)" [1]. Version 6.0.0 (20260929) is "the first release of the new FalkorDB engine, written in Rust", which replaces the C engine of every 4.x release; the commands, Cypher and client libraries are unchanged [6]. The README says this repository is the Rust implementation [3]. The landscape snapshot files it as core; this entry files it as adjacent, being a storage engine, not an LLM pipeline [13].

## How it works

The README says the engine stores adjacency matrices as GraphBLAS sparse matrices and runs queries with linear algebra; the model is a property graph queried in OpenCypher with extensions [3]. Vector indexes use HNSW (euclidean or cosine, 1 to 4096 dimensions) and are queried with `db.idx.vector.queryNodes`; the client supplies the embeddings [8]. Full-text indexes use RediSearch with TF-IDF scoring [9]; in 6.0 both index types run on RediSearch 8.6.1 [6]. The docs list a GraphRAG SDK, LangChain, LangGraph, LlamaIndex, AG2 and a separate MCP server repository, stdio by default with optional HTTP [10][11].

## Status and direction

6.0.0 (20260929) is the first Rust release; the 4.x line continues (4.22.0 to 4.22.3, 20260930 to 20261028) [6]. Commit subjects from 20261025 to 20261029 are mostly fixes described as matching the C engine ("like C"), plus index work [12]. The full-text docs say the older procedure form of index creation does not yet work on 6.0 [9]. A roadmap is unstated.

## Sources

All read on 20261030 between 19:40 and 19:47 UTC.

1. https://github.com/FalkorDB/FalkorDB : repository metadata via the GitHub API
2. https://github.com/FalkorDB/FalkorDB/blob/main/LICENSE : SSPL v1 (section 13) and Elastic License 2.0 (limitations), 655 lines
3. https://github.com/FalkorDB/FalkorDB/blob/main/README.md : description, licence statements, developer guide
4. https://github.com/FalkorDB/FalkorDB/tree/v4.22.3 : `LICENSE.txt` (557 lines, SSPL only) and README licence statement
5. https://github.com/FalkorDB/FalkorDB/commit/1665fbd98eaf264f13a0891c913345984429d201 : commit of 20260802 18:12 UTC, "Migrate the default development branch to the Rust engine (#2279)"
6. https://github.com/FalkorDB/FalkorDB/releases : release list, v6.0.0 and v6.0.3 notes
7. https://docs.falkordb.com/ : documentation home
8. https://docs.falkordb.com/cypher/indexing/vector-index.md : HNSW, metrics, dimensions, query procedure
9. https://docs.falkordb.com/cypher/indexing/fulltext-index.md : RediSearch, TF-IDF, 6.0 note
10. https://docs.falkordb.com/genai-tools.md : list of GenAI integrations
11. https://docs.falkordb.com/genai-tools/mcpserver : MCP server description, transports, repository
12. https://github.com/FalkorDB/FalkorDB/commits/main : commit subjects since 20260801 via the GitHub API
13. [landscape snapshot](../landscape/20261030_1913-github/repos.tsv) : snapshot row (stars 10,505, forks 600, flags empty, category core), read from this repository
