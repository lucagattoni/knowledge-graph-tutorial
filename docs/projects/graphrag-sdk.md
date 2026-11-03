---
type: project
repo: FalkorDB/GraphRAG-SDK
trends: [graph-based-rag]
updated: 20261102 23:17 UTC
---

# GraphRAG SDK

A Python library from [FalkorDB](./falkordb.md) that builds a [knowledge graph](../index/knowledge-graph.md) in the FalkorDB database from documents and answers questions from it. This page says what it does, how it is built, who has measured it, and where it is heading. It is one of the vendor-owned libraries in the [graph-based RAG](../trends/graph-based-rag.md) (retrieval-augmented generation) trend.

| Field | Value |
|---|---|
| Repository | https://github.com/FalkorDB/GraphRAG-SDK [1] |
| Licence | Apache-2.0, read from the `LICENSE` file (Apache License 2.0 text); GitHub's licence endpoint, `pyproject.toml` and PyPI agree [1][2][14][15]. The database it needs, FalkorDB, has a `LICENSE` file that begins with the Server Side Public License v1; GitHub does not classify it [17]. The optional `pdf-fast` extra pulls PyMuPDF, which the file's own comment calls AGPL-3.0 [15]. |
| Trends | [Graph-based RAG](../trends/graph-based-rag.md) |

## What it is

The README calls it a modular [GraphRAG](../index/graphrag.md) framework that goes "from raw documents to cited answers" and treats the retrieval harness as more important than the model [3]. It needs FalkorDB server 4.20 or later and refuses an older one [3]. Answers can cite their source chunks through `MENTIONED_IN` edges, and an application can abstain when retrieval finds no evidence [3][4]. The package version is 1.6.0 and the README dates version 1.0 to April 2026 [3][15].

## How it works

Ingestion runs nine steps: load, [chunk](../index/chunking.md), build a lexical graph of Document and Chunk nodes, extract, prune against an optional [schema](../index/schema.md), resolve, write, then link mentions and [embed](../index/embedding.md) chunks [4]. Extraction is two-step: a local [GLiNER](./gliner.md) model finds entities by default, then a [large language model](../index/large-language-model.md) (LLM) verifies them and extracts relationships; an LLM-only extractor is an option [5]. Every extracted relationship is stored as one `RELATES` edge type, with the original type kept as a property [4]. After ingestion, `finalize()` deduplicates new entities across documents with an LLM judge [3][4]. Updates are incremental: `update`, `delete_document` and `apply_changes` re-sync single documents [3].

Retrieval starts with LLM keyword extraction and one question embedding, then runs relationship-[vector search](../index/vector-search.md), entity discovery by name match and full-text search, four chunk paths and a two-hop expansion, and ends with cosine [reranking](../index/reranking.md) and an LLM answer [4]. Text-to-[Cypher](../index/cypher.md) is a further path, off by default and marked experimental [3][6].

The SDK runs no [agent](../index/agent.md) loop. Since v1.6.0 it offers graph tools (`retrieve`, `check_citations` and others) that a caller's own agent can use, plus a `graphrag-mcp` server for the [Model Context Protocol](../index/model-context-protocol.md). The read tools run read-only queries; the write tools (`set_ontology`, `ingest`, `finalize`) are dropped when `read_only` is set [7][12][15].

## Evidence

All results below are first-party unless stated.

| Claim | Setup (as the project states it) | Who ran it |
|---|---|---|
| 71.48 overall against 55.39 for vector RAG with reranking [8] | SDK 1.3.0, `gpt-4o-mini` for graph building and answers, August 2026, the benchmark's own evaluator unmodified [8] | FalkorDB (first-party) [8] |
| 66.09 on GraphRAG-Bench Novel, 76.87 on Medical [8][9] | Two declared deviations from SDK defaults: text-to-Cypher on, 1,024-dimension embeddings; [ontologies](../index/ontology.md) hand-written from the corpus; one graph per corpus document [8] | FalkorDB (first-party) [8] |

The "overall" figure is the project's own average of the two subsets; the leaderboard ranks each separately [8]. Competitor scores were copied from the leaderboard and not re-run [8]. The project lists its limits itself: judge variance, two domains, one duplicate question, and judge failures that left 2,053 of 2,062 Medical and 1,995 of 2,009 Novel answers scored [8]. The runner, the ontology builders and the pinned dependencies are offered "on request"; the ontologies and the full configuration are published [8]. Indexing took about 1.5 hours for the Medical corpus and about 4 hours for Novel on a 24-core machine, dominated by extraction API calls [8].

The benchmark's own leaderboard files now hold a GraphRAG-SDK row dated 2026.08 that links to this repository, with the same scores: rank 4 of 21 on Novel and rank 2 of 21 on Medical [10]. Who checked the row is unstated; the benchmark's README says only that its evaluation code is standardised [18]. The README's table ranks the SDK first, but it lists nine systems; the leaderboard has others above it, for example KnowCosmos at 70.34 and 80.15 [3][10]. *Reading:* the result is a credible self-run on one benchmark and one SDK version (1.3.0, not the current 1.6.0), not an independent comparison. The benchmark's authors open by citing reports that GraphRAG "frequently underperforms vanilla RAG on many real-world tasks" [10][11]. No evaluation by anyone other than FalkorDB was found.

## Status and direction

The latest release is v1.6.0, published 20261102 14:32 UTC, with 33 releases in all; three came in the last 90 days (v1.4.0 20260810, v1.5.0 20261022, v1.6.0 20261102) [12]. The default branch has 530 commits since 20260804, 473 of them from two accounts [13]. The repository is not archived [1]. No statement of maintenance mode or of features moved to a hosted tier was found in the README or docs read.

v1.6.0 adds agentic retrieval (graph-walk, skills, the MCP (Model Context Protocol) server) and agentic ingestion, where a plan picks the chunker, extractor and resolver per file within cheap default limits [7][12][16]. The README roadmap lists "Introduce Agentic GraphRAG" for 2026-Q3 [3]. Its Q4 item is dynamic traversal and a temporal graph [3]. The earlier archive entry, read three days before, recorded v1.5.0 and no MCP path [19].

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [FalkorDB](falkordb.md)
- [Projects](README.md)

**Benchmarks**

- [GraphRAG-Bench (Xiang)](../benchmarks/graphrag-bench-xiang.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/FalkorDB/GraphRAG-SDK : repository metadata and licence classification via the GitHub API; not archived (read 20261102 20:09 UTC)
2. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/LICENSE : Apache License 2.0 text, head and tail read (read 20261102 20:09 UTC)
3. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/README.md : description, FalkorDB 4.20 requirement, benchmark table, incremental updates, roadmap (read 20261102 20:09 UTC)
4. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/architecture.mdx : nine ingestion steps, graph schema, retrieval flow, provenance (read 20261102 20:10 UTC)
5. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/extraction.mdx : GLiNER default plus LLM verification (read 20261102 20:10 UTC)
6. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/retrieval.mdx : `enable_cypher` off by default (read 20261102 20:10 UTC)
7. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/agentic-retrieval.mdx : toolkit, no agent loop, MCP server, cheap ingestion plans (read 20261102 20:10 UTC)
8. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/graphrag-accuracy-benchmark.mdx : setup, scores, deviations, limitations, indexing time; reproduction package "available on request" (runner, ontology builders, pinned dependencies), ontologies and full configuration published (read 20261102 20:10 and 20:33 UTC)
9. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/benchmark.mdx : per-subset scores, 15-system comparison (read 20261102 20:10 UTC)
10. https://graphrag-bench.github.io/story_data.csv and https://graphrag-bench.github.io/medical_data.csv : leaderboard rows read from the files the page loads (read 20261102 20:11 UTC)
11. https://arxiv.org/abs/2506.05690 : Xiang, Wu, Zhang and 4 others, "When to use Graphs in RAG: A Comprehensive Analysis for Graph Retrieval-Augmented Generation", first version 20250606 (read 20261102 20:14 UTC, listing; the quotation is from the benchmark site, https://graphrag-bench.github.io/, read 20261102 20:11 UTC)
12. https://github.com/FalkorDB/GraphRAG-SDK/releases : 33 releases; v1.6.0 notes list agentic retrieval, MCP server, agentic ingestion (read 20261102 20:09 and 20:14 UTC)
13. https://github.com/FalkorDB/GraphRAG-SDK/commits/main : commits and authors since 20260804 (read 20261102 20:12 UTC)
14. https://pypi.org/pypi/graphrag-sdk/json : version 1.6.0, licence Apache-2.0 (read 20261102 20:13 UTC)
15. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/graphrag_sdk/pyproject.toml : version 1.6.0, `mcp` extra, GLiNER dependency, PyMuPDF AGPL comment (read 20261102 20:10 UTC)
16. https://github.com/FalkorDB/GraphRAG-SDK/blob/main/CHANGELOG.md : Unreleased section describing agentic ingestion (read 20261102 20:10 UTC)
17. https://github.com/FalkorDB/FalkorDB : `LICENSE` begins "Server Side Public License"; GitHub licence field NOASSERTION (read 20261102 20:12 UTC)
18. https://github.com/GraphRAG-Bench/GraphRAG-Benchmark : README on standardised evaluation code (read 20261102 20:11 UTC)
19. https://github.com/FalkorDB/GraphRAG-SDK/releases : v1.5.0 as the latest release, and no path mentioning MCP in the file tree (read 20261030 19:40 UTC, via the archive page [kb-kg/projects/graphrag-sdk.md](../../kb-kg/projects/graphrag-sdk.md))
