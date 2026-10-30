---
slug: neo4j-graphrag-python
repo: neo4j/neo4j-graphrag-python
tier: card
category: core
snapshot: 20261030 19:41 UTC
---

# neo4j-graphrag-python

| | |
|---|---|
| Repository | https://github.com/neo4j/neo4j-graphrag-python [1] |
| Licence | Apache-2.0 for the code; some parts are under the Python Software Foundation (PSF) License Version 2. GitHub's API reports `NOASSERTION` and there is no file named `LICENSE` [1][2]. `LICENSE.txt` (6 lines) says: unless stated otherwise, Apache License 2.0 (text in `LICENSE.APACHE2.txt`); parts under the PSF License Version 2 (`LICENSE.PYTHON.txt`), "marked as such" in the code. Which files: not located. `pyproject.toml` and PyPI say Apache License 2.0; the README states no licence [2][3][4][5]. |
| Language | Python (GitHub primary language) [1] |
| Stars, forks | 1,326, 259 (20261030 19:41 UTC; the 19:13 UTC landscape snapshot has the same figures). The snapshot sets no flag; it computes 1.36 stars per day and 19.53 forks per 100 stars [1][6] |
| Created, last push | 20240227 11:49 UTC, 20261030 14:09 UTC [1] |
| Latest release | 1.23.0, 20261028 10:40 UTC; PyPI `neo4j-graphrag` lists 1.23.0 [4][7] |
| Status | active: 102 commits since 20260731 (the 90 days before the read), newest 20261030 14:08 UTC; not archived [1][8] |
| Paper, docs | no paper stated; documentation at neo4j.com/docs/neo4j-graphrag-python (homepage field, not fetched); `docs/source` holds reStructuredText guides; `CHANGELOG.md` [1][9] |

## What it is

The README calls it "the official Neo4j GraphRAG package for Python", a first-party library for graph retrieval-augmented generation on Neo4j with "long-term support and maintenance directly from Neo4j" [5]. It has two parts: retrievers and a `GraphRAG` class that answer questions over a Neo4j database, and a knowledge-graph builder pipeline in which an LLM extracts a graph from text or PDFs and writes it to Neo4j [5]. The builder lives in the `experimental` namespace, which the README says may change without notice and is not recommended for production; it also needs the APOC core library [5]. No benchmark or evaluation appears in the README [5]. Releases 0.3.0 to 0.5.0 were titled "Neo4j GenAI package for Python" [7].

## How it works

The public exports include `VectorRetriever`, `VectorCypherRetriever`, `HybridRetriever`, `HybridCypherRetriever`, `Text2CypherRetriever` and `ToolsRetriever`, plus retrievers pairing Weaviate, Pinecone or Qdrant vectors with Neo4j [10]. The README's linked posts describe vector search enriched by graph traversal, hybrid retrieval and LLM-written Cypher [5]. `GraphRAG` combines a retriever with an LLM to answer [5]. For construction, `SimpleKGPipeline` wraps a customisable `Pipeline`; the source tree names components for loading, splitting, embedding, schema extraction, entity and relation extraction, pruning, resolving and writing [5][9]. LLM providers include OpenAI, Anthropic, Vertex AI, Gemini, Cohere, Mistral, Bedrock and Ollama [5]. The file tree has no MCP module [9].

## Status and direction

Active. 39 GitHub releases since 0.3.0 (20240702), 14 of them in 2026; the CHANGELOG has a 1.20.0 section, but no 1.20.0 release is in that list [7][11]. Recent entries cover pipeline observers (1.20.0), lazy provider imports (1.22.0) and Parquet export fixes (1.22.0, 1.23.0) [11]. Open: 16 issues and 39 pull requests; the oldest open issue is dated 20240923 [12]. Roadmap: unstated.

## Sources

1. https://github.com/neo4j/neo4j-graphrag-python : repository metadata via the GitHub API (read 20261030 19:41 UTC)
2. https://github.com/neo4j/neo4j-graphrag-python/blob/main/LICENSE.txt : the licence statement; `LICENSE.APACHE2.txt` (Apache 2.0 text, 202 lines), `LICENSE.PYTHON.txt` (PSF text) and `NOTICE.txt` also read; a request for `LICENSE` returned not found (read 20261030 19:41 UTC)
3. https://github.com/neo4j/neo4j-graphrag-python/blob/main/pyproject.toml : version 1.23.0, licence text (read 20261030 19:41 UTC)
4. https://pypi.org/pypi/neo4j-graphrag/json : version 1.23.0, licence field (read 20261030 19:42 UTC)
5. https://github.com/neo4j/neo4j-graphrag-python/blob/main/README.md : description, extras, experimental namespace, examples (read 20261030 19:42 UTC)
6. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : the row for this repository: no flag, 1.36 stars per day, 19.53 forks per 100 stars (read 20261030 19:41 UTC)
7. https://github.com/neo4j/neo4j-graphrag-python/releases : 39 releases, 0.3.0 (20240702) to 1.23.0 (20261028), and their titles (read 20261030 19:41 UTC)
8. https://github.com/neo4j/neo4j-graphrag-python/commits/main : 102 commits since 20260731; newest 20261030 (read 20261030 19:42 UTC)
9. https://github.com/neo4j/neo4j-graphrag-python/tree/main : file tree (`src/neo4j_graphrag`, `docs/source`, `CHANGELOG.md`); no path contains "mcp" (read 20261030 19:41 UTC)
10. https://github.com/neo4j/neo4j-graphrag-python/blob/main/src/neo4j_graphrag/retrievers/__init__.py : exported retrievers (read 20261030 19:42 UTC)
11. https://github.com/neo4j/neo4j-graphrag-python/blob/main/CHANGELOG.md : entries for 1.20.0 to 1.23.0 (read 20261030 19:42 UTC)
12. https://github.com/neo4j/neo4j-graphrag-python/issues : open issue and pull request counts via the search API; the oldest open issue (read 20261030 19:42 UTC)
