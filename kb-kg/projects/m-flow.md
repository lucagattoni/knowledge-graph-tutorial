---
slug: m-flow
repo: FlowElement-xinliuyuansu/m_flow
tier: card
category: core
snapshot: 20261030 19:39 UTC
---

# M-flow

| | |
|---|---|
| Repository | https://github.com/FlowElement-xinliuyuansu/m_flow [1] |
| Licence | Apache-2.0, from the `LICENSE` file (Apache License 2.0 text; head and tail read) [2]; the README licence section agrees [3]. |
| Language | Python (GitHub primary language); the README also lists a Next.js web console [1][3] |
| Stars, forks | 4,510, 256 (20261030 19:39 UTC; the 19:13 UTC landscape snapshot has the same figures). The snapshot sets no flag; it computes 21.17 stars per day and 5.68 forks per 100 stars [1][4] |
| Created, last push | 20260331 08:36 UTC, 20260901 22:13 UTC [1] |
| Latest release | v0.3.4, 20260412 19:48 UTC, the only GitHub release [5]. The PyPI package `mflow-ai` lists 0.3.6, uploaded 20260415 20:07 UTC, which has no GitHub release [6]. |
| Status | active: 58 days since the last push, under the 90-day line (computed); not archived [1] |
| Paper, docs | no paper stated; the README and `docs/RETRIEVAL_ARCHITECTURE.md`; the homepage field points to flowelement.ai (not fetched) [1][3][7] |

## What it is

M-flow calls itself "a bio-inspired cognitive memory engine" and "a new paradigm for Graph RAG" [1]. It stores memory as a four-level "cone graph" (Episode, Facet, FacetPoint, Entity) and, in the README's words, lets the graph rather than vector similarity decide relevance at query time [3]. The repository holds a Python API (`add`, `memorize`, `query`), a CLI, a FastAPI backend, a web console and an MCP server [3]. The published results are the project's own: 81.8% LLM-judge on LoCoMo-10 against 79.4% for Cognee Cloud, and 89% on the first 100 LongMemEval questions, from a benchmark repository under the same organisation; no independent evaluation appeared in the sources read [3][8]. A `NOTICE.md` says initial engineering drew on Cognee's architectural patterns and the project has since been "substantially rewritten and extended" [9].

## How it works

The README's diagram has three ingestion stages: extract (chunking and parsing, 50+ file formats), memorize (the LLM builds the graph and embeddings) and load (graph and vector databases) [3]. A coreference step resolves pronouns before indexing [3]. Edges carry natural-language text that is also embedded [10]. At query time the query is searched against seven vector collections, the hits are projected into the graph, cost is propagated along edges, and each Episode is scored by its strongest path; the LLM then answers from that Episode bundle [3][10]. Listed backends: LanceDB, Neo4j, PostgreSQL with pgvector, ChromaDB, KùzuDB, Pinecone [3]. Agents use an MCP server, the CLI or the REST API [3]. LLM calls per document: unstated.

## Status and direction

Active by the heuristic, not archived. Of the 100 newest `main` commits, 98 are dated 20260413 to 20260501; the newest, 20260803, updates repository references after a move to the current organisation [11]. The 20260901 push is later than that commit; which branch took it was not checked. Open: 0 issues and 13 pull requests; 11 issues have been closed [12]. Three pull requests by the top contributor account were closed unmerged on 20260904 [12]. Roadmap: unstated.

## Sources

1. https://github.com/FlowElement-xinliuyuansu/m_flow : repository metadata via the GitHub API (stars, forks, licence field, dates, language, homepage, topics) (read 20261030 19:39 UTC)
2. https://github.com/FlowElement-xinliuyuansu/m_flow/blob/main/LICENSE : Apache License 2.0 text, 191 lines (read 20261030 19:39 UTC)
3. https://github.com/FlowElement-xinliuyuansu/m_flow/blob/main/README.md : description, cone graph, retrieval, benchmarks, features, layout, licence section (read 20261030 19:39 UTC)
4. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : the row for this repository: no flag, 21.17 stars per day, 5.68 forks per 100 stars, 8 contributors counted there (read 20261030 19:39 UTC)
5. https://github.com/FlowElement-xinliuyuansu/m_flow/releases : one release, v0.3.4 (read 20261030 19:39 UTC)
6. https://pypi.org/pypi/mflow-ai/json : versions 0.3.1 to 0.3.6 and upload times (read 20261030 19:39 UTC)
7. https://github.com/FlowElement-xinliuyuansu/m_flow/tree/main/docs : `RETRIEVAL_ARCHITECTURE.md` and `CUSTOM_LLM_PROVIDERS.md` listed (read 20261030 19:39 UTC)
8. https://github.com/FlowElement-xinliuyuansu/mflow-benchmarks : benchmark README and repository metadata (read 20261030 19:40 UTC)
9. https://github.com/FlowElement-xinliuyuansu/m_flow/blob/main/NOTICE.md : copyright and the Cognee acknowledgment (read 20261030 19:39 UTC)
10. https://github.com/FlowElement-xinliuyuansu/m_flow/blob/main/docs/RETRIEVAL_ARCHITECTURE.md : cone levels, edge text, bundle search phases (read 20261030 19:39 UTC)
11. https://github.com/FlowElement-xinliuyuansu/m_flow/commits/main : 100 newest commits, 20260413 to 20260803, and their subjects (read 20261030 19:39 UTC)
12. https://github.com/FlowElement-xinliuyuansu/m_flow/pulls : open pull requests, closed pull requests and the issue counts via the issues and search APIs (read 20261030 19:40 UTC)
