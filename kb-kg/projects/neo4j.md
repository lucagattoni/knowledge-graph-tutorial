---
slug: neo4j
repo: neo4j/neo4j
tier: card
category: adjacent
snapshot: 20261030 19:40 UTC
---

# Neo4j

| | |
|---|---|
| Repository | https://github.com/neo4j/neo4j [1] |
| Licence | GPL-3.0, from `LICENSE.txt`: the GNU General Public License version 3 text of 29 June 2007, with no Neo4j-specific terms found by a text search [2]; the `genai-plugin` and `lucene-index` copies are GPLv3 too [2]. The README states the scope: "Neo4j Community Edition is an open source product licensed under GPLv3"; Enterprise Edition "includes additional closed-source components not available in this repository and requires a commercial license"; Aura is the fully managed service [3]. File, README and GitHub field agree [1][2][3]. No legal advice. |
| Language | Java (GitHub primary language) [1] |
| Stars, forks | 17,378, 2,795 (20261030 19:40 UTC; the landscape snapshot of 20261030 19:13 UTC has 17,378 and 2,792) [1][12] |
| Created, last push | 20121112 08:46 UTC, 20261023 07:54 UTC [1] |
| Latest release | GitHub's latest-release call returns 3.2.0-alpha08 (20170411), so it is not current. Newest tags: 2026.10.1 (commit 20261020 08:27 UTC), 2026.10.0 (20261009 15:25 UTC); default branch `2026.10` [1][4] |
| Status | active: 7 days since the last push (computed); no snapshot flag [12] |
| Paper, docs | Cypher manual at neo4j.com/docs [5][6]; a paper is unstated |

## What it is

Neo4j is a graph database written in Java. Its README describes "a flexible network structure of nodes and relationships", ACID transactions and a "friendly query language"; the manual documents it as Cypher [3][5]. This repository is the Community Edition under GPLv3 [2][3]. Vector and full-text indexes, the two retrieval features that matter for LLM work, are in the Community Edition, with one limit: the docs say native `VECTOR` properties need block format, which they place in Enterprise Edition and Aura, while Community can index `LIST` properties [5]. A first-party GraphRAG package for Python lives in a separate repository, whose README says it "enables developers to build graph retrieval augmented generation (GraphRAG) applications"; its licence was not read here (GitHub reports NOASSERTION) [11].

## How it works

Data are nodes and relationships; indexes are declared on their properties [5][6]. Queries use Cypher. The `SEARCH` clause (Cypher 25) queries vector indexes from 2026.01 and full-text indexes from 2026.09; the older procedures are deprecated [5][6]. Vector indexes use Lucene's HNSW graph, cosine (default) or euclidean similarity, 1 to 4096 dimensions; the client supplies embeddings [5]. Full-text indexes use Lucene and return a relevance score [6]. A `genai-plugin` module in this repository builds a JAR whose functions call external providers (OpenAI, Azure OpenAI, VertexAI, Amazon Bedrock) for embeddings and text [7][8]. Agents connect through the official Neo4j MCP Server (schema, read and write Cypher, graph algorithms) or Labs servers, one of which stores memory as a knowledge graph [9].

## Status and direction

Releases are calendar-versioned: tags 2026.08.1, 2026.09.0, 2026.10.0, 2026.10.1 [4]. The API lists 515 commits on the default branch since 20260801 and 417 contributors, anonymous ones included [10]. Recent subjects include vector `SEARCH` planning, vector procedure error handling and CVE fixes [10]. The vector docs show a feature history: `SEARCH` in 2026.01, quantized search in 2026.07, binary quantization as default since 2026.08 [5]. A roadmap is unstated in the sources read.

## Sources

All read on 20261030 between 19:40 and 19:47 UTC.

1. https://github.com/neo4j/neo4j : repository metadata via the GitHub API (stars, forks, licence field, dates, language, default branch)
2. https://github.com/neo4j/neo4j/blob/2026.10/LICENSE.txt : GPLv3 text; also the `LICENSE.txt` heads in `community/genai-plugin` and `community/lucene-index`
3. https://github.com/neo4j/neo4j/blob/2026.10/README.asciidoc : description, editions, Aura, licensing statement
4. https://github.com/neo4j/neo4j/tags : tag list via the GitHub API, tagged-commit dates, and the latest-release call (2017 result)
5. https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/ : vector index algorithm, similarity, dimensions, `SEARCH`, edition and version notes
6. https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/full-text-indexes/ : Lucene engine, analyzers, scoring, `SEARCH` from 2026.09
7. https://github.com/neo4j/neo4j/tree/2026.10/community/genai-plugin : module README ("provide GenAI functions and procedures")
8. https://neo4j.com/docs/genai/plugin/current/ : providers named by the plugin docs
9. https://neo4j.com/developer/genai-ecosystem/model-context-protocol-mcp/ : official MCP server and Labs servers
10. https://github.com/neo4j/neo4j/commits/2026.10 : commit subjects and count since 20260801, and the contributors count (anonymous included), via the GitHub API
11. https://github.com/neo4j/neo4j-graphrag-python : README line and licence field via the GitHub API
12. [landscape snapshot](../landscape/20261030_1913-github/repos.tsv) : snapshot row (stars 17,378, forks 2,792, flags empty), read from this repository
