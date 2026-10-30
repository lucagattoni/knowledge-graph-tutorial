---
slug: llama-index
repo: run-llama/llama_index
tier: card
category: adjacent
snapshot: 20261030 19:45 UTC
---

# LlamaIndex

| | |
|---|---|
| Repository | https://github.com/run-llama/llama_index [1] |
| Licence | MIT, from the `LICENSE` file ("The MIT License", copyright "Jerry Liu"; head and tail read) [2]. The GitHub field agrees [1]. |
| Language | Python (GitHub primary language) [1] |
| Stars, forks | 52,747, 8,481 (20261030 19:41 UTC; the 20261030 19:13 UTC landscape snapshot had 52,746 and 8,480) [1][9] |
| Created, last push | 20221102 04:24 UTC, 20261026 21:25 UTC [1] |
| Latest release | v0.14.25, 20260921 16:22 UTC; PyPI `llama-index` 0.14.25 has the same upload time [4][7] |
| Status | active (pushed within 90 days); not archived; no snapshot flag [1][9] |
| Paper, docs | no paper stated; docs at https://developers.llamaindex.ai/python/framework/ [3] |

## What it is

The README calls LlamaIndex "an open-source framework to build agentic applications" from the company behind LlamaParse [3]. A note in it says the company's "primary focus has shifted towards LlamaParse, along with liteparse and our benchmarking efforts", and that the framework remains available as an open toolkit [3]. The README lists data connectors, ways to "structure your data (indices, graphs)" and a retrieval and query interface [3]. The documentation describes a `PropertyGraphIndex`, a labelled property graph built from the documents and queried for retrieval [5]. No benchmark or evaluation appears in the sources read: unstated.

## How it works

`PropertyGraphIndex` runs `kg_extractors` over each chunk and attaches the entities and relations to the nodes. The defaults are an LLM extractor of single-hop (entity, relation, entity) paths and an implicit extractor that needs no LLM; optional extractors follow a dynamic or strict schema [5]. Retrieval combines sub-retrievers: by default LLM-generated synonyms and vector similarity over graph nodes, plus optional text-to-Cypher and Cypher-template retrievers [5]. The default store is in memory, persists to disk and cannot run Cypher; Neo4j, Nebula, TiDB and FalkorDB stores are documented [5]. An agent can call MCP servers through the `llama-index-tools-mcp` package, which can also turn a workflow into an MCP app [6].

## Status and direction

Active. Two releases since July: v0.14.24 (20260819) and v0.14.25 (20260921) [4]. The newest of 12 commit subjects read (20261014) concern model providers and integrations [8]. The README says the focus has shifted to LlamaParse [3]. The property-graph guide last changed 20260720, for an error-handling option [5]. 90 commits in the 90 days to the snapshot; 796 open pull requests, 347 open issues [9][10]. Roadmap: unstated.

## Sources

All read 20261030 19:41-19:45 UTC (the clock was checked before and after the reads, not per call).

1. https://github.com/run-llama/llama_index : repository metadata via the GitHub API (stars, forks, licence field, dates, language)
2. https://github.com/run-llama/llama_index/blob/main/LICENSE : MIT licence text
3. https://github.com/run-llama/llama_index/blob/main/README.md : description, focus note, features
4. https://github.com/run-llama/llama_index/releases : release dates since 20260701
5. https://github.com/run-llama/llama_index/blob/main/docs/src/content/docs/framework/module_guides/indexing/lpg_index_guide.md : the property graph index guide (extractors, retrievers, stores); its change history read through the commits API
6. https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/tools/llama-index-tools-mcp/README.md : MCP tool spec and `workflow_as_mcp`
7. https://pypi.org/pypi/llama-index/json : PyPI version 0.14.25 and upload time
8. https://github.com/run-llama/llama_index/commits/main : commit subjects since 20260801
9. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : first GitHub snapshot (20261030 19:13 UTC); flags column empty, 90 commits in 90 days
10. https://github.com/run-llama/llama_index/issues : open issue and pull request counts via the search API
