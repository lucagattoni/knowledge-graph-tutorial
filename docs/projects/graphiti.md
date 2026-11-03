---
type: project
repo: getzep/graphiti
trends: [agent-memory, features-in-and-out]
updated: 20261102 23:17 UTC
---

# Graphiti

This page answers what Graphiti is, how it builds and searches a time-aware graph, and what has been measured. It also records how the open library divides work with its vendor's paid service, Zep, and that one of its graph back ends is deprecated.

| Field | Value |
|---|---|
| Repository | https://github.com/getzep/graphiti [1] |
| Licence | Apache-2.0. GitHub classifies the `LICENSE` file as Apache-2.0; the file is the standard Apache 2.0 text, and `pyproject.toml` declares the same [2][3]. |
| Trends | [Agent memory](../trends/agent-memory.md) · [Graph features removed and added](../trends/features-in-and-out.md) |

## What it is

Graphiti is a Python framework (package `graphiti-core`) for building and querying temporal "context graphs" for AI agents. A context graph holds entities, facts (edges with validity windows) and episodes, the raw inputs every fact came from [4]. You supply the graph database, the [language model](../index/large-language-model.md) and the embedder, and you build the service around it [4].

Graphiti is "the graph construction framework inside Zep", the vendor's commercial product; Zep's graph database, Konig, is proprietary [4][5]. The README now says "Neither is an agent memory product" [4]; the paper's title still says agent memory [11]. Zep stopped maintaining its earlier open-source server (post dated 20250402) to concentrate open-source work on Graphiti [6]. Supported back ends are [Neo4j](./neo4j.md), [FalkorDB](./falkordb.md) and Amazon Neptune; [Kuzu](../../kb-kg/projects/kuzu.md) is deprecated [4].

## How it works

**Write.** `add_episode` takes text or JSON and a reference time. A language model extracts entities and resolves them against existing ones, then extracts facts as edges and resolves those too [7]. Entity and edge types can be set with Pydantic models [4]. Bulk loading uses one combined extraction call per episode by default since PR 1964 (merged 20261009); `add_episode` is unchanged [8].

**Time.** Edges carry `valid_at`, `invalid_at` and `expired_at`. When facts contradict, the code sets `invalid_at` and `expired_at` on the edge that the other supersedes, normally the one with the earlier `valid_at`; in this code path the edge is marked, not removed [9]. The README calls this "bi-temporal" tracking ([bitemporal model](../index/bi-temporal-model.md)) [4].

**Search.** The search module can query facts, nodes, episodes and communities with full-text ([BM25](../index/bm25.md), Best Matching 25, a keyword ranking function), cosine-similarity and graph-expansion channels. Results are reranked by reciprocal rank fusion, maximal marginal relevance, a cross-encoder, distance from a chosen node, or episode mentions [10]. This is [hybrid search](../index/hybrid-search.md) over a [temporal knowledge graph](../index/temporal-knowledge-graph.md).

**Reference servers.** An MCP (Model Context Protocol) server in the repository exposes 13 tools, among them `add_memory` (processed in the background), `search_nodes` and `search_memory_facts` [12]. The README warns that the MCP and REST servers have "no authentication, no authorization, and no prompt-injection protection" [4].

## Evidence

All results below are first-party except the last row.

| Result | Who ran it | Source |
|---|---|---|
| Deep Memory Retrieval: Zep 94.8% with gpt-4-turbo against MemGPT 93.4% (reported in its own paper) and a full-conversation baseline of 94.4% | Zep authors, first-party, paper of 20250120 | [11] |
| [LongMemEval](../datasets/longmemeval.md) (about 115k-token conversations): gpt-4o-mini full context 55.4% in 31.3 s, Zep 63.8% in 3.20 s; gpt-4o 60.2% against 71.2% | Zep authors, first-party | [11] |
| [LoCoMo](../datasets/locomo.md): Zep's published 84% disputed by the CTO of [Mem0](./mem0.md) (58.44% on replication, 20250508); Zep answered 75.14% ± 0.17 over 10 runs (20250512), conceding a calculation error | Both vendors | [13] |
| [MemoryAgentBench](../benchmarks/memoryagentbench.md) overall average, GPT-4o-mini backbone: Zep 24.0, against Mem0 21.1, [Cognee](./cognee.md) 20.6, MemGPT 28.3, BM25 41.5, [HippoRAG](./hipporag.md)-v2 41.6 | Hu, Wang and McAuley, not the Zep team; Zep's configuration (service or library) is **unstated** | [14] |

The paper's caveats: the DMR (Deep Memory Retrieval) set is small, its conversations fit in a context window, and the authors call it inadequate; the experiments ran December 2024 to January 2025 on the Zep service, with network latency the baselines did not have; Zep scored below full context on `single-session-assistant` (75.0% against 81.8% for gpt-4o-mini) [11]. These are not measurements of the library as released in October 2026. No independent run of that release was found.

## Status and direction

*Release.* v0.31.2, 20261020 17:25 UTC, is GitHub's latest. Since 20260804 there are six tags: v0.30.0 and `mcp-v1.1.0` (20260901), v0.30.2 (20260908), v0.31.0 (20261014), v0.31.1 (20261015) and v0.31.2 [15].

*Activity.* Snapshot of 20261102; it drifts, and the watch-list carries current figures. Of the 119 commits to `main` since 20260804, 62 are by a licence-signature bot. The other 57 come from 14 author names, one an AI-assistant bot with 7 commits [16].

*Direction.* PR 1964 moves "the improvements from Zep's internal Graphiti fork into upstream", but not features Zep releases "behind feature flags (hyperedges, the entity type hierarchy, and the batch extraction modes)" [8]. Kuzu "will be removed" [4]. Reference servers are declared reference-only, and pull requests adding authentication to them are out of scope [4]. The repository's top level has no roadmap file [17].

*Reading:* the project is active, not archived [1], and maintained by the vendor whose service it feeds. The open code tracks the hosted product with a lag the project itself states; how large the gap is stays **unstated**.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Cognee](cognee.md)
- [FalkorDB](falkordb.md)
- [Hindsight](hindsight.md)
- [Memori](memori.md)
- [MemOS](memos.md)
- [Projects](README.md)
- [Semantica](semantica.md)
- [Supermemory](supermemory.md)

**Papers**

- [Papers: Agent memory](../papers/agent-memory.md)

**Datasets**

- [LongMemEval](../datasets/longmemeval.md)

**Benchmarks**

- [LongMemEval](../benchmarks/longmemeval.md)
- [MemoryAgentBench](../benchmarks/memoryagentbench.md)

**Applied to Pinakes**

- [The Pinakes graph approach](../applied-to-pinakes/approach.md)
- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Agent memory](../index/agent-memory.md)
- [Bi-temporal model](../index/bi-temporal-model.md)
- [Embedded database](../index/embedded-database.md)
- [Knowledge graph](../index/knowledge-graph.md)
- [Open-core](../index/open-core.md)
- [Provenance](../index/provenance.md)
- [Reciprocal rank fusion](../index/reciprocal-rank-fusion.md)
- [Reranking](../index/reranking.md)
- [Selective forgetting](../index/selective-forgetting.md)
- [Temporal knowledge graph](../index/temporal-knowledge-graph.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/getzep/graphiti (via `gh api`) : repository metadata, archived flag (read 20261102 20:09 UTC)
2. https://github.com/getzep/graphiti/blob/main/LICENSE and https://api.github.com/repos/getzep/graphiti/license (via `gh api`) : licence text and GitHub's classification (read 20261102 20:11 UTC)
3. https://github.com/getzep/graphiti/blob/main/pyproject.toml : licence field, version 0.31.2 (read 20261102 20:11 UTC)
4. https://github.com/getzep/graphiti/blob/main/README.md (via `gh api repos/getzep/graphiti/readme`) : positioning, Zep split, back ends, Kuzu deprecation, server warnings, bi-temporal wording (read 20261102 20:09 UTC; Zep and Kuzu lines re-read 20261102 20:33 UTC)
5. https://www.getzep.com/platform/context-graph-engine/ : Konig described as proprietary (read 20261102 20:12 UTC)
6. https://www.getzep.com/blog/announcing-a-new-direction-for-zeps-open-source-strategy/ : Community Edition discontinued, 20250402 (read 20261102 20:14 UTC)
7. https://github.com/getzep/graphiti/blob/main/graphiti_core/graphiti.py : `add_episode` and its extraction and resolution calls (read 20261102 20:11 UTC)
8. https://github.com/getzep/graphiti/pull/1964 (via `gh api`) : upstreamed fork changes, combined extraction, excluded features (read 20261102 20:12 UTC)
9. https://github.com/getzep/graphiti/blob/main/graphiti_core/utils/maintenance/edge_operations.py : temporal invalidation, lines about 727-785 (re-read 20261102 20:33 UTC)
10. https://github.com/getzep/graphiti/blob/main/graphiti_core/search/search.py : scopes, channels, rerankers (read 20261102 20:11 UTC)
11. https://arxiv.org/abs/2501.13956 and https://arxiv.org/html/2501.13956v1 : Rasmussen, Paliychuk, Beauvais and 2 others, "Zep: A Temporal Knowledge Graph Architecture for Agent Memory", v1 20250120; abstract, Tables 1 and 2, models, caveats (read 20261102 20:11 UTC)
12. https://github.com/getzep/graphiti/blob/main/mcp_server/src/graphiti_mcp_server.py : the 13 `@mcp.tool` functions (read 20261102 20:11 UTC)
13. https://github.com/getzep/zep-papers/issues/5 (via `gh api`) : LoCoMo dispute, 20250508 to 20250519 (read 20261102 20:12 UTC)
14. https://arxiv.org/abs/2507.05257 and https://arxiv.org/html/2507.05257 : Hu, Wang, McAuley, "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions", v4 20260628; Table 3 (read 20261102 20:13 UTC)
15. https://api.github.com/repos/getzep/graphiti/releases/latest and https://api.github.com/repos/getzep/graphiti/releases (via `gh api`) : tags and dates (read 20261102 20:09 UTC)
16. https://api.github.com/repos/getzep/graphiti/commits?since=2026-08-04T00:00:00Z (via `gh api`, paged, 119 commits) : counts by author (re-read 20261102 20:34 UTC)
17. https://api.github.com/repos/getzep/graphiti/git/trees/main (via `gh api`) : top-level listing, no roadmap file (read 20261102 20:13 UTC)

Further reading in the archive: [Graphiti, long entry](../../kb-kg/projects/graphiti.md). Papers: [agent memory group](../papers/agent-memory.md).
