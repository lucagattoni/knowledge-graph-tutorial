---
slug: memgraph
repo: memgraph/memgraph
tier: card
category: adjacent
snapshot: 20261030 19:40 UTC
---

# Memgraph

| | |
|---|---|
| Repository | https://github.com/memgraph/memgraph [1] |
| Licence | GitHub reports NOASSERTION [1]. The `LICENSE` file is five lines: the source "is variously licensed under the Business Source License 1.1 (BSL), the Memgraph Enterprise License (MEL)"; each licence is in the `licenses` directory; a file is under the BSL, copyright The Memgraph Authors, "unless otherwise noted at the beginning of the file" [2]. That directory holds `BSL.txt`, `MEL.pdf` and `APL.txt` (Apache License 2.0 text), and the LICENSE file does not mention the last [3]. `BSL.txt` (dated 1 January 2026): licensor Memgraph Ltd; Licensed Work "Memgraph Community Edition (MCE) version 2.0" (the latest release is v3.14.0; how versions map is unstated); production use is granted "solely for any Authorised Purpose", meaning internal business purposes provided you do not (a) embed or distribute the work to third parties and give them direct access to operate it as a standalone solution or service, (b) host it for third parties as database-as-a-service or an equivalent model, and/or (c) use it to create a competing work; Change Date written "2030-21-10"; Change License Apache 2.0; use outside the terms needs a commercial licence [4]. The README says Community is under the BSL and Enterprise under the MEL [5]. `MEL.pdf` could not be read as text here, so the MEL terms, and which files carry a MEL header, are unstated [11]. No legal advice. |
| Language | C++ (GitHub primary language) [1] |
| Stars, forks | 4,636, 296 (20261030 19:40 UTC; the landscape snapshot of 20261030 19:13 UTC has 4,636 and 295) [1][12] |
| Created, last push | 20200921 10:14 UTC, 20261030 19:10 UTC [1] |
| Latest release | v3.14.0, 20261021 11:05 UTC [9] |
| Status | active: pushed the day it was read; no snapshot flag [12] |
| Paper, docs | memgraph.com/docs [5]; a paper is unstated |

## What it is

Memgraph is an in-memory graph database built in C/C++; its README calls it "fully compatible with Neo4j's Cypher query language" and ACID-compliant [5]. The README presents it as the graph engine for GraphRAG, AI memory and agentic workflows, with text and vector indexes in one query layer [5]. It lists high availability, multi-tenancy, fine-grained access control and SSO under an "Enterprise" heading [5]. A separate MIT-licensed repository, memgraph/ai-toolkit (118 stars), packages Context Graph (memory for coding agents), `unstructured2graph` (entity extraction), LangChain and LightRAG integrations and an MCP server [8]. The snapshot files it as core; this entry files it as adjacent, being a database [12].

## How it works

Data are a graph queried in Cypher [5]. Vector indexes (USearch backend) take client-supplied embeddings, are queried with `vector_search.search`, need `dimension` and `capacity`, are not used by the query planner and run at READ_UNCOMMITTED isolation [6]. Text indexes use Tantivy, are queried with `text_search` procedures and are no longer experimental since 3.6 [7]. The README claims "atomic GraphRAG" as one Cypher query, an LLM utility module, and `SHOW SCHEMA INFO` for Text2Cypher [5]. `mcp-memgraph` exposes seven tools, read-only by default, among them `run_cypher_query` and `search_schema` [8].

## Status and direction

Releases: v3.11.0 (20260617), v3.12.0 (20260715), v3.13.0 (20260909), v3.13.1, v3.13.2, v3.14.0 (20261021) [9]. Commit subjects since 20261015 are query, storage, authorisation and replication fixes; one of 20261021 reads "Update BSL change date to 2030-21-10"; one moves the `llm.complete` default off a model before its shutdown date [10]. The README links a separate roadmap repository, not read here [5].

## Sources

All read on 20261030 between 19:40 and 19:47 UTC.

1. https://github.com/memgraph/memgraph : repository metadata via the GitHub API
2. https://github.com/memgraph/memgraph/blob/master/LICENSE : the five-line licence statement
3. https://github.com/memgraph/memgraph/tree/master/licenses : directory listing (`APL.txt`, `BSL.txt`, `MEL.pdf`)
4. https://github.com/memgraph/memgraph/blob/master/licenses/BSL.txt : BSL parameters, Additional Use Grant, Change Date and Change License
5. https://github.com/memgraph/memgraph/blob/master/README.md : description, feature list, licence section, roadmap link
6. https://memgraph.com/docs/querying/vector-search : vector index backend, metrics, syntax, limits
7. https://memgraph.com/docs/querying/text-search : Tantivy, procedures, status, limits
8. https://github.com/memgraph/ai-toolkit : README (packages, licence field, stars) and `integrations/mcp-memgraph/README.md` (tools, read-only default)
9. https://github.com/memgraph/memgraph/releases : release list via the GitHub API
10. https://github.com/memgraph/memgraph/commits/master : commit subjects since 20260801 via the GitHub API
11. https://github.com/memgraph/memgraph/blob/master/licenses/MEL.pdf : fetched; the text could not be extracted
12. [landscape snapshot](../landscape/20261030_1913-github/repos.tsv) : snapshot row (stars 4,636, forks 295, flags empty, category core), read from this repository
