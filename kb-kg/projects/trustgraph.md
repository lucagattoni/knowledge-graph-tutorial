---
slug: trustgraph
repo: trustgraph-ai/trustgraph
tier: card
category: core
snapshot: 20261030 19:39 UTC
---

# TrustGraph

| | |
|---|---|
| Repository | https://github.com/trustgraph-ai/trustgraph [1] |
| Licence | Apache-2.0, from the `LICENSE` file (Apache License 2.0 text; head and tail read) [2]. The README licence section says Apache 2.0, so they agree [3]. |
| Language | Python (GitHub primary language); the README also lists TypeScript UI libraries [1][3] |
| Stars, forks | 2,854, 339 (20261030 19:39 UTC; the landscape snapshot of 20261030 19:13 UTC has the same figures) [1] |
| Created, last push | 20240710 19:14 UTC, 20261028 18:56 UTC [1] |
| Latest release | GitHub Releases lists one release: v2.8.17, "TrustGraph 2.8", 20260908 20:38 UTC [4]. The newest tag is v2.11.1 and PyPI has 2.11.1, uploaded 20261027 00:15 UTC [5][6]. |
| Status | active (pushed 2 days before the read; no snapshot flag) [1] |
| Paper, docs | no paper; https://docs.trustgraph.ai [3][7] |

## What it is

A self-hosted platform that, in its README's words, turns enterprise knowledge, systems and business logic into an ontology-grounded context graph and a policy runtime that governs what AI agents can do; it deploys as containers [3]. The docs describe three retrieval modes: Graph RAG, Ontology RAG and Document RAG [7]. The only benchmark published is ingest speed: loading a 1,549,890-token report took 8.5 minutes on eight Gaudi 2 cards with Llama-3.3-70B and 289.3 minutes on CPU with the same model; the page gives no date and no runner, and I found no answer-quality evaluation [8]. The README's headline has changed often: its latest 30 commits span 20260619 to 20261028, with subjects naming "Holonic Context Graph", "Semantic Intelligence Layer" and "The Semantic Agent Governance Platform" [9].

## How it works

Graph RAG chunks text, has an LLM extract subgraphs, and stores entity embeddings. A query gets LLM concept extraction, entity lookup, subgraph traversal, LLM edge scoring and reasoning, provenance tracing and an LLM answer [7]. Ontology RAG picks the relevant part of an ontology for each chunk to guide extraction; Document RAG fuses BM25 and vector search [7]. Stores: Cassandra, Qdrant, Garage, with Pulsar or RabbitMQ messaging [3][7]. Access policies are SHACL shapes with SPARQL rules over a JWT user context; the guide says v2.10 or later and CLI loading only [11]. The `trustgraph-mcp` package registers 31 MCP tools, including `graph_rag`, `agent` and `sparql_query`, over streamable HTTP with bearer-token auth [10].

## Status and direction

Active: 99 commits on master since 20260801 (26, 36 and 37 in August, September and October), nine author names, 31 contributors, 17 open issues, 2 open pull requests [12]. Versions 2.11.0 and 2.11.1 reached PyPI on 20261027, while the Releases page still shows v2.8.17 [4][6]. Roadmap: none found in the README or the docs links read. The MCP integration guide warns that production deployment and authentication may not be ready [11].

## Sources

1. https://github.com/trustgraph-ai/trustgraph : repository metadata via the GitHub API (read 20261030 19:39 UTC)
2. https://github.com/trustgraph-ai/trustgraph/blob/master/LICENSE : Apache License 2.0 text (read 20261030 19:40 UTC)
3. https://github.com/trustgraph-ai/trustgraph/blob/master/README.md : positioning, stores, quickstart, licence section (read 20261030 19:39 UTC)
4. https://github.com/trustgraph-ai/trustgraph/releases : one release, v2.8.17, and its notes (read 20261030 19:42 UTC)
5. https://github.com/trustgraph-ai/trustgraph/tags : newest tags (v2.11.1, v2.11.0, v2.10.18) (read 20261030 19:42 UTC)
6. https://pypi.org/pypi/trustgraph/json : 559 releases, 2.11.1 newest (read 20261030 19:40 UTC)
7. https://docs.trustgraph.ai/architecture/retrieval.html : retrieval modes and steps; also /learn/how-it-works.html and /architecture/storage.html (read 20261030 19:42 UTC)
8. https://docs.trustgraph.ai/benchmarks.html : ingest token-rate table (read 20261030 19:43 UTC)
9. https://github.com/trustgraph-ai/trustgraph/commits/master/README.md : README commit subjects (read 20261030 19:43 UTC)
10. https://github.com/trustgraph-ai/trustgraph/tree/master/trustgraph-mcp : the MCP server source, tool registration (read 20261030 19:47 UTC)
11. https://docs.trustgraph.ai/guides/policy-filtering/ and https://docs.trustgraph.ai/guides/mcp-integration/ : policy filtering and MCP client guides (read 20261030 19:42 UTC)
12. https://github.com/trustgraph-ai/trustgraph/commits/master : commit counts by month and author, contributors, open issues and pull requests (read 20261030 19:40 UTC)
