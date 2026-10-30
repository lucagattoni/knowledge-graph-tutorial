---
slug: graphiti
repo: getzep/graphiti
tier: deep
category: agent-memory
snapshot: 20261030 18:59 UTC
---

# Graphiti

Source notes: this entry began as an investigation made on 20260725 15:29 UTC (call it "the July
note", marked **[J]** where a detail is carried over without being re-read). It was re-checked against
the live repository on 20261030 between 18:59 and 19:02 UTC. Where the July note is now wrong or stale,
the body below carries the corrected statement and the section "Changed since the July 2026
investigation" says what moved.

| | |
|---|---|
| Repository | https://github.com/getzep/graphiti |
| Licence | Apache-2.0. The `LICENSE` file is the standard Apache License 2.0 text [3]; the root `pyproject.toml` also declares `license = "Apache-2.0"` [12]. The README carries no licence badge [4], so there is nothing to disagree with. |
| Language | Python, `requires-python >=3.10,<4` [12] |
| Stars, forks | 32,372 stars, 3,321 forks (20261030 18:59 UTC) [1] |
| Created, last push | 20240808 22:08 UTC, 20261028 23:22 UTC [1] |
| Latest release | v0.31.2, 20261020 17:25 UTC [2]. The reference MCP server is versioned separately: 1.1.3 in `mcp_server/pyproject.toml` (20261030 19:00 UTC) [11]; the latest GitHub release tag with the `mcp-` prefix is `mcp-v1.1.0`, 20260901 [5]. |
| Status | active (pushed 2 days before the snapshot; not archived) [1] |
| Paper, docs | arXiv:2501.13956, "Zep: A Temporal Knowledge Graph Architecture for Agent Memory" [16]; docs at https://help.getzep.com/graphiti [1] |

## What it is

Graphiti is a Python framework for building and querying temporal graphs for AI agents. The project's
current README calls them "context graphs": entities, facts (edges with validity windows) and
"episodes", the raw inputs from which every fact was derived [4]. An LLM extracts the entities and
facts from each episode (a message, a block of text or JSON), and the result is served through hybrid
search [4][7]. The user supplies the graph database, the LLM and the embedder and builds the
surrounding service (ingestion, tenancy, access control, operations) [4].

The project describes itself as the graph-construction framework inside Zep, a commercial product [4].
Its README now states that "neither is an agent memory product" [4]; the paper's title and the July
note both used the "agent memory" label [16]. The category used in this reference is therefore the
field's label, not the project's own.

### Open source versus hosted

The paper evaluates Zep, the service, with Graphiti as "its core component" [16]. What the open
repository ships and what only the vendor's service provides are not the same, and the project says so.

| Aspect | Graphiti (open source, this repository) | Zep (vendor service) |
|---|---|---|
| Licence | Apache-2.0 [3] | The graph database, Konig, is described on the vendor's page as "proprietary" [18]. Terms for the rest of the service: unstated in the sources read. |
| What it is | A framework: `graphiti-core` library, plus a reference MCP server (`mcp_server/`) and a reference FastAPI REST service (`server/`) [4] | "The unified context layer for enterprises" [4] |
| Graph database | Bring your own: Neo4j, FalkorDB, Amazon Neptune (Kuzu deprecated) [4] | Konig, "no third-party graph database required"; "Available under Zep cloud and BYOC plans" [4][18] |
| Users, threads, ingestion | "Build your own" [4] | Built in, for messages and business data [4] |
| Retrieval and performance | "Custom implementation required; performance depends on your setup" [4] | "Sub-200ms performance at scale" is the vendor's own claim; no measurement was read [4] |
| Developer tools | None beyond the library and examples [4] | Dashboard with graph visualisation, debug and API logs, CLI, SDKs for Python, TypeScript and Go [4] |
| Enterprise features | Self-managed [4] | SLAs, support, security guarantees (vendor statement) [4] |
| Deployment | Self-hosted only [4] | Fully managed or in the customer's cloud (BYOC) [4] |
| Authentication | The reference servers have none, by design: "no authentication, no authorization, and no prompt-injection protection"; a production deployment must supply these in its own service or use Zep [4] | Provided (vendor statement) [4] |

Three further facts mark the boundary:

- Zep keeps an internal fork of Graphiti. A pull request merged on 20261009 describes itself as moving
  "the improvements from Zep's internal Graphiti fork into upstream" and says it "does not include the
  features that Zep releases behind feature flags (hyperedges, the entity type hierarchy, and the batch
  extraction modes" nor "the hooks that need Zep services" [14]. How far the hosted product's
  behaviour differs from the open code is unstated.
- Zep also once had an open-source server, Zep Community Edition. The vendor stopped maintaining it,
  announced on 20250402 per the page's metadata; the repository stays open under Apache-2.0 "but we
  will no longer provide updates or active support", and the vendor says its open-source effort now
  concentrates on Graphiti [19].
- The paper's results (below) are for Zep as it was in January 2025, with `gpt-4o-mini-2024-07-18`
  for graph construction and BGE-m3 for embeddings and reranking [17]. They are not a measurement of
  the library as released in October 2026.

### Which graph databases it supports now

Read from the README, `pyproject.toml` extras and the repository tree on 20261030 [4][12][5].

| Backend | Status | Notes |
|---|---|---|
| Neo4j | supported; the default dependency (`neo4j>=5.26.0`) [12] | README requires Neo4j 5.26 [4]. A 20260901 release (v0.30.0) changed Neo4j query routing so that the configured database name is honoured; this affects only Neo4j Enterprise users who set a non-default database [5]. |
| FalkorDB | supported (`falkordb>=1.1.2,<2.0.0`) [12] | README requires FalkorDB 1.1.2 [4]. Reference MCP server default [11]. |
| FalkorDB embedded ("falkordblite") | supported, optional extra, Python 3.12+ only [12] | Added in v0.29.2 (20260608) [5]. This corrects the July note, which called Kuzu "the only embedded option". |
| Amazon Neptune | supported (Neptune Database Cluster or Neptune Analytics) [4] | Needs an Amazon OpenSearch Serverless collection for full-text search [4]. |
| Kuzu | **deprecated** | Marked deprecated in v0.29.2 and dropped from the default test matrix (PR #1548) [5]. The README says the upstream Kuzu project is no longer maintained, that the driver "emits a `DeprecationWarning`" and that Kuzu "will be removed in a future release" [4]. The README names Kuzu 0.11.2 while the extra pins `kuzu>=0.11.3` [4][12]. |
| Neo4j with OpenSearch | optional extra `neo4j-opensearch` [12] | Purpose beyond the extra's name: unstated. |

The repository tree has one driver package per backend (`falkordb`, `kuzu`, `neo4j`, `neptune`), each
with a set of per-entity operation modules, plus a design file named `driver-operations-redesign.md`
under `spec/` (tree listing only; the spec file was not read) [22].

## How it works

### Indexing: from episode to graph

`Graphiti.add_episode(name, episode_body, source_description, reference_time, source, group_id,
entity_types, edge_types, edge_type_map, custom_extraction_instructions, saga, ...)` runs the pipeline
below [7]. Stage helpers live in `graphiti_core/utils/maintenance/` [8][9]. Read from the live code on
20261030 19:00 UTC.

| Step | What happens | LLM? |
|---|---|---|
| 1. Context | `retrieve_episodes()` loads the last prior episodes as extraction context (or `previous_episode_uuids` if given) [7] | no |
| 2. Entity extraction | `extract_nodes()`; `_collapse_exact_duplicate_extracted_nodes` merges exact normalised-name duplicates within the pass [8] | yes |
| 3. Entity resolution | `resolve_extracted_nodes()` gathers candidates three ways: identity properties (optional), exact normalised name, and semantic search (`NODE_DEDUP_CANDIDATE_LIMIT = 15`, `NODE_DEDUP_COSINE_MIN_SCORE = 0.6`). It resolves by identity property first, then deterministically by similarity; only unresolved nodes are sent to `_resolve_with_llm` [8] | only for unresolved nodes |
| 4. Edge extraction | `extract_edges()` extracts facts with endpoints and optional `valid_at`/`invalid_at` dates [9] | yes |
| 5. Edge resolution | `resolve_extracted_edges()`: fetches same-endpoint edges for duplicates and wider candidates for contradictions. An edge whose normalised fact text and endpoints already exist is reused with no LLM call. Otherwise one `dedupe_edges.resolve_edge` call returns duplicate and contradicted fact indices [9] | per edge that has candidates and is not a verbatim duplicate |
| 6. Dating | `_extract_edge_timestamps`: a lightweight small-model call that dates a new edge if extraction left it undated [9] | only for new, undated edges |
| 7. Attributes and summaries | `extract_attributes_from_nodes()`: typed-attribute extraction runs only for nodes whose custom entity type has fields. Summaries: a node with a short summary gets edge facts appended with no LLM call; the rest are summarised in flights of `MAX_NODES = 30` [8] | conditional |
| 8. Save | Embeddings are created for nodes and edges; episodic edges link the episode to what it produced; saga links (`NEXT_EPISODE`, `HAS_EPISODE`) are written if a saga is named; optional `update_community()` adds LLM community summaries [7] | embeddings; communities optional |

`add_episode_bulk` batches the same stages. Since v0.31.0 (20261014) it uses *combined extraction* by
default: one LLM call per episode returns nodes and edges together, with `use_combined_extraction=False`
to restore separate calls; `add_episode` itself is unchanged [14][7]. The default combined prompt was
replaced on 20261013 by a shorter "C2" prompt (see Evidence) [15]. `add_triplet` (also an MCP tool)
bypasses extraction and writes a fact directly; the tool's docstring says graphiti-core resolves its
endpoint nodes against existing entities [11]. `remove_episode` deletes an episode and, as of v0.31.2, keeps restated facts and
rebuilds the summaries of affected nodes [2][7]. A `GLiNER2Client` can run entity extraction locally on
CPU (205M-340M parameter model); every other operation (edges, dedup, summaries) is delegated to a
separate LLM client [21].

### The bi-temporal model

Two independent timelines per entity edge [9]:

- **Ingest time:** `created_at` (when Graphiti learned the fact) and `expired_at` (when Graphiti learned
  it no longer holds).
- **Valid time:** `valid_at` / `invalid_at` (when the fact was true in the world), extracted by the LLM
  relative to the episode's `reference_time`.

Contradictions never delete. In `edge_operations`, the new edge is dated first, then
`_apply_temporal_invalidation` runs [9]: an edge that arrives with an end date is expired at once; an
edge is expired if a candidate that starts later supersedes it; and `resolve_edge_contradictions` sets
`invalid_at = new_edge.valid_at` and `expired_at = now` on an older edge that the new edge supersedes.
Time normalisation was added in v0.31.0: future-tense plans use the reference time as `valid_at`, and
soft deadlines do not set `invalid_at` [14]. History stays queryable; the MCP search tool filters on
`valid_at_after/before` and `invalid_at_after/before` [11]. Deletion exists only as explicit tooling
(`delete_entity_edge`, `delete_episode`, `remove_episode`) [11][7].

### Retrieval

`graphiti_core/search/search.py::search()` runs four scopes in parallel: edges, nodes, episodes and
communities [10]. Each scope runs its configured channels, each fetching `2 * limit` candidates [10]:

- **bm25:** the database's full-text index.
- **cosine:** vector similarity over node or edge embeddings.
- **bfs:** graph expansion from `bfs_origin_node_uuids`. If BFS is enabled with no origins given, the
  origins are the source nodes of the bm25 and cosine hits, and BFS runs on them [10].

Rerankers: reciprocal rank fusion (`rrf`), maximal marginal relevance, cross-encoder, graph distance
from a `center_node_uuid` (`node_distance_reranker`), and episode mentions (rank by the number of
episodes that mention an edge) [10]. `search_config_recipes.py` defines 16 named recipes, unchanged in
count from the July note [10]. `Graphiti.search()` returns `list[EntityEdge]` (facts) and uses
`EDGE_HYBRID_SEARCH_RRF`, or `EDGE_HYBRID_SEARCH_NODE_DISTANCE` when a `center_node_uuid` is passed;
`search_()` returns nodes, edges, episodes and communities and defaults to
`COMBINED_HYBRID_SEARCH_CROSS_ENCODER` [7]. Cross-encoder clients exist for BGE (local), OpenAI and
Gemini [10]; the per-query cost of each is **[J]**, not re-read.

### The reference MCP server, tool by tool

`mcp_server/src/graphiti_mcp_server.py` (FastMCP; `config.yaml` sets the transport to `http`, with
stdio also supported; settings use `${ENV}` expansion) [11]. It is a reference implementation, not a
production deployment, with no authentication; since v0.31.2 it listens on localhost by default [4][2].
Its database setting defaults to FalkorDB, with Neo4j as the alternative [11]. There are 13 tools
(same count and names as in the July note); errors return `{error: str}` and mutations
`{message: str}` [11].

| Tool | Arguments (defaults) | Returns |
|---|---|---|
| `add_memory` | `name`, `episode_body`, `group_id?`, `source='text'`, `source_description=''`, `uuid?`, `reference_time?`, `excluded_entity_types?`, `custom_extraction_instructions?`, `previous_episode_uuids?`, `update_communities=False`, `saga?`, `saga_previous_episode_uuid?` | SuccessResponse. Does not process inline: it "returns immediately and processes the episode addition in the background"; episodes of one `group_id` are processed sequentially. The caller never receives the resulting nodes or edges. |
| `search_nodes` | `query`, `group_ids?`, `max_nodes=10`, `entity_types?`, `center_node_uuid?` | `{message, nodes: [{uuid, name, labels, created_at, summary, group_id, attributes}]}` |
| `search_memory_facts` | `query`, `group_ids?`, `max_facts=10`, `center_node_uuid?`, `edge_types?`, `valid_at_after?`, `valid_at_before?`, `invalid_at_after?`, `invalid_at_before?` | `{message, facts: [...]}`; a fact carries uuid, relation name, the fact as a sentence, source and target node uuids, group, and the four time fields |
| `get_entity_edge` | `uuid`, `group_id?` | the edge as a dict |
| `delete_entity_edge`, `delete_episode` | `uuid`, `group_id?` | SuccessResponse |
| `get_episodes` | `group_ids?`, `max_episodes=10` | recent episodes, by recency, not by search |
| `get_episode_entities` | `episode_uuids`, `group_id?` | `{message, nodes, edges}`: everything the episodes created (provenance) |
| `add_triplet` | `source_node_name`, `edge_name`, `fact`, `target_node_name`, `group_id?`, `source_node_uuid?`, `target_node_uuid?` | `{message, nodes, edges}`; direct write, no extraction |
| `summarize_saga` | `saga_name`, `group_id?` | `{message, uuid, name, summary}` |
| `build_communities` | `group_ids?` | `{message, community_count, edge_count, communities}` |
| `clear_graph` | `group_ids?` | SuccessResponse |
| `get_status` | none | `{status, message}`; a non-MCP `GET /health` route also exists |

Observable properties of the surface (facts read from the code, no judgement): every tool speaks entity
and relation vocabulary; the argument lists are flat with defaults; node and edge results carry uuids,
so calls chain (search, then `get_entity_edge`, then `get_episode_entities`); embeddings are stripped
from payloads (the fact payload excludes `fact_embedding`) [11][J]; `center_node_uuid` is a single
optional parameter that reranks by graph distance [11]; time arguments are ISO-8601 strings; `group_ids`
accepts `str | list[str]` on the read tools; there is no tool that lists a node's neighbours or
traverses edges, so structure is reached only through rerankers and the provenance tool; and `add_memory`
returns no job id, so an agent can only learn what an episode produced by polling `get_episodes` or
`get_episode_entities` [11].

## Cost and operating profile

- **LLM at ingest.** Every episode needs at least the entity-extraction and edge-extraction calls in
  `add_episode` (one combined call in `add_episode_bulk`); edge resolution, dating, node-dedup
  escalation, typed attributes, summaries and communities add calls under the conditions in the table
  above [7][8][9]. The July note's figure of "4-6+ LLM calls per episode even when nothing new is
  learned" **[J]** was a count of call sites, not a measurement, and overstated the floor: a verbatim
  duplicate fact, an entity with no dedup candidates and a node with a short summary each skip their
  call [8][9]. The project publishes no per-episode call count or dollar figure (**unstated**). There
  is no ingestion mode without an LLM: even the GLiNER2 option replaces only entity extraction [21].
- **Embeddings.** Created for every node and edge [7]. Default providers and models change between
  releases; release titles name `gpt-5.5` (v0.29.2) and a later change of the OpenAI defaults (PR
  #1999) [5][6].
- **Query time.** bm25, cosine, BFS, RRF, MMR, node-distance and episode-mentions reranking need only
  the database and arithmetic. A cross-encoder rerank adds a model call per query unless the local BGE
  client is used (**[J]**, not re-read). `README` says concurrency is bounded by `SEMAPHORE_LIMIT`
  (default 10) to avoid provider rate-limit errors [4].
- **Needs.** A running graph database, an LLM key (OpenAI by default) and an embedder; a Neptune
  deployment also needs OpenSearch Serverless [4].
- **Local models.** Supported through OpenAI-compatible endpoints (Ollama, vLLM, llama.cpp, LM Studio)
  using `OpenAIGenericClient`, which offers `structured_output_mode` `json_schema` (default) or
  `json_object`. The README warns that "very small models frequently emit JSON that doesn't match the
  requested schema, which surfaces as extraction failures" and that Graphiti "works best with LLM
  services that support Structured Output" [4]. It can run with no cloud API if a capable local model is
  used; how capable is **unstated**.
- **Telemetry.** Anonymous usage statistics via PostHog are on by default and are disabled with
  `GRAPHITI_TELEMETRY_ENABLED=false`; the README lists the fields collected (random UUID, OS, Python and
  Graphiti versions, provider and backend names) [4].

## Evidence

| Result | Source |
|---|---|
| Deep Memory Retrieval (DMR, 500 conversations of the Multi-Session Chat dataset): Zep 94.8% with gpt-4-turbo vs MemGPT 93.4% (reported in the MemGPT paper) and full-conversation baseline 94.4%; with gpt-4o-mini, Zep 98.2% vs full conversation 98.0% | paper tables [17] |
| LongMemEval_s (conversations of about 115k tokens): gpt-4o-mini, full context 55.4% in 31.3 s with 115k tokens vs Zep 63.8% in 3.20 s with 1.6k tokens; gpt-4o, full context 60.2% in 28.9 s vs Zep 71.2% in 2.58 s | paper tables [17] |
| Per question type, Zep lost to full context on `single-session-assistant` (gpt-4o-mini 81.8% to 75.0%; gpt-4o 94.6% to 80.4%) and gained most on `single-session-preference` and `temporal-reasoning` | paper tables [17] |
| Extraction prompt "C2" vs previous default, on a Zep internal evaluation with GPT-6 Luna: test semantic F1 0.638 vs 0.628 (455 rows); train 0.633 vs 0.654 (400 rows); runs that produced at least one fact 96% vs 89%. The PR itself calls the F1 differences "inside the noise of the evaluation (about plus or minus 0.025)" | PR #1997 [15] |

Caveats the paper states about itself [17]: DMR is small, uses single-turn fact-retrieval questions and
has conversations of about 60 messages that fit in a context window, so the authors call it inadequate
(the full-conversation baseline already scores 94.4%); MemGPT could not be run on LongMemEval and its
gpt-4o-mini DMR result could not be reproduced; Zep's latency included network latency from a
residential laptop in Boston to AWS us-west-2, which the baselines did not have; Zep fell below the
baseline on `single-session-assistant`; weaker models understood Zep's temporal data less well. The
paper says top-20 edges and nodes are retrieved in one place and top-10 in the DMR section. The
extraction tool used to read the HTML summarised it and flagged identical `single-session-user` rows for
both models as a possible copy error in the paper; that was not checked against the PDF.

A dispute over a later benchmark: on 20250508 Mem0's CTO opened an issue on `getzep/zep-papers`
claiming Zep's published LoCoMo score of 84% was an error and that a replication gave 58.44% [20]. A Zep
maintainer replied on 20250512 that "the corrected score is 75.14% +/- 0.17 (over 10 runs)", conceded the
calculation error and stood by its criticism of the other side's method; the issue was closed for
inactivity on 20250519 [20]. Both figures are vendor-reported. A web search on 20261030 19:01 UTC
returned vendor blogs and secondary write-ups with conflicting numbers; none was verified here, so no
independent evaluation is cited. Published results from independent evaluators: **none found in this
run**.

## Direction

There is no roadmap file in the repository (tree listing, 20261030 19:00 UTC) [22]. From releases and
commits since 20260801 [5][6]:

- The vendor is merging its internal fork into the open code: extraction, deduplication, temporal edges,
  saga summaries and prompt routing (PR #1964, 20261009) [14].
- New plug-in points: `LLMRuntime` for per-prompt model routing (20261006) and client classes that send
  node and edge dedup to external "decision" models (Jev, OpenAI Decisions; 20261013) [6][4].
- Positioning has shifted from "temporal knowledge graph" and "agent memory" toward "context graph" and
  a clear Zep/Graphiti split; the README was rewritten on 20260826 and 20261022 [6][4].
- The reference servers are now explicitly out of scope for security reports and pull requests that add
  authentication [4].
- Kuzu will be removed [4]. Release cadence: v0.29.3 on 20260727, then no release until v0.30.0 on
  20260901, then v0.30.2 (20260908), v0.31.0 (20261014), v0.31.1 (20261015), v0.31.2 (20261020) [5].

## Changed since the July 2026 investigation

All bullets checked on 20261030 between 18:59 and 19:02 UTC.

- **Numbers.** Stars 32,372 (20261030 18:59 UTC) against "about 29.2k" in the July note (20260725 15:29
  UTC): about +3.2k in 97 days, roughly 33 a day, which is close to the lifetime average of about 40 a
  day since creation and shows no abnormal jump in this comparison. Forks 3,321 (no July figure). Open
  issues and pull requests combined: 529 [1]. The contributors listing has 64 entries (last page of a
one-per-page listing, 20261030 19:00 UTC) [1].
- **Licence and status.** Apache-2.0 (LICENSE file), not archived, no rename, same repository name and
  owner [1][3]. No successor project found; the paper has only version 1 (20250120) and no journal
  reference [16].
- **Releases.** July note: latest v0.29.2, MCP server 1.0.2. Now v0.31.2 and MCP server 1.1.3. Seven tags
  since: v0.29.3 (20260727), v0.30.0 and mcp-v1.1.0 (20260901), v0.30.2 (20260908), v0.31.0 (20261014),
  v0.31.1 (20261015), v0.31.2 (20261020) [5][11].
- **Commit activity since 20260801.** 123 commits listed on the default branch, of which 66 are an
  automated CLA-signature bot; the other 57 fall in August (5), September (22) and October (30). They
  come from 14 distinct author names, one of which is an AI-assistant bot account (7 commits) [6].
- **README.** Reframed on 20260826 and again on 20261022 [6]. The README at v0.29.3 (20260727) said
  Zep was "powered by a proprietary graph database", linked a blog titled "State of the Art in Agent
  Memory" and called Graphiti an "open-source temporal context graph engine"; the current README
  names the database Konig, drops the "State of the Art" line, and says neither Graphiti nor Zep is an
  agent-memory product [13][4].
- **July claim corrected: embedded backends.** The July note called Kuzu "the only embedded option".
  Embedded FalkorDB (`falkordblite`, Python 3.12+) was added in the same release that deprecated Kuzu,
  v0.29.2 [5][12]. Body corrected.
- **July claim corrected: LLM call count.** "4-6+ LLM calls even when nothing new is learned" was a count
  of call sites; several are conditional. Body corrected.
- **July claim updated: entity resolution.** The July note described one cosine candidate search. The
  code now also uses identity properties and exact-name lookup before semantic search, and runs
  identity-property resolution before similarity resolution [8]. Constants (`15`, `0.6`, `MAX_NODES = 30`)
  are unchanged [8].
- **July claims that still hold.** 13 MCP tools with the same names, `add_memory` still queues in the
  background, no neighbour-traversal tool, 16 search recipes, four search scopes, BFS seeded by the first
  channels' hits, Kuzu deprecated [11][10].
- **New since July.** Combined extraction in the bulk path and the C2 prompt; `LLMRuntime` and
  Jev/OpenAI-Decisions dedup clients; `GLiNER2Client`; Neo4j database routing fix with a behaviour change
  for Enterprise users; reference servers listen on localhost by default and are declared reference-only
  with no authentication [5][6][14][15][21][4].

## Sources

All reads on 20261030 UTC; times are when each was fetched.

1. https://api.github.com/repos/getzep/graphiti : stars, forks, licence, archived flag, dates (read 20261030 18:59 UTC)
2. https://api.github.com/repos/getzep/graphiti/releases/latest : v0.31.2 and its notes (read 20261030 18:59 UTC)
3. https://github.com/getzep/graphiti/blob/main/LICENSE : Apache License 2.0 text (read 20261030 18:59 UTC)
4. https://github.com/getzep/graphiti/blob/main/README.md : positioning, Zep vs Graphiti, backends, Kuzu deprecation, reference servers, local models, telemetry (read 20261030 18:59 UTC)
5. https://github.com/getzep/graphiti/releases : release list and notes for v0.29.2, v0.29.3, v0.30.0, v0.31.0 and mcp-v1.1.0 (read 20261030 18:59 to 19:00 UTC)
6. https://github.com/getzep/graphiti/commits/main : commits since 20260801 (read 20261030 19:00 UTC)
7. https://github.com/getzep/graphiti/blob/main/graphiti_core/graphiti.py : `add_episode`, `add_episode_bulk`, `search`, `search_`, `remove_episode` (read 20261030 19:00 UTC)
8. https://github.com/getzep/graphiti/blob/main/graphiti_core/utils/maintenance/node_operations.py : extraction, resolution, summaries (read 20261030 19:00 UTC)
9. https://github.com/getzep/graphiti/blob/main/graphiti_core/utils/maintenance/edge_operations.py : edge extraction, resolution, invalidation, dating (read 20261030 19:00 UTC)
10. https://github.com/getzep/graphiti/blob/main/graphiti_core/search/search.py and .../search_config_recipes.py : channels, rerankers, 16 recipes (read 20261030 19:00 UTC)
11. https://github.com/getzep/graphiti/tree/main/mcp_server : `src/graphiti_mcp_server.py`, `src/models/response_types.py`, `config/config.yaml`, `pyproject.toml` (read 20261030 19:00 to 19:01 UTC)
12. https://github.com/getzep/graphiti/blob/main/pyproject.toml : version, licence, extras, Python range (read 20261030 19:00 UTC)
13. https://github.com/getzep/graphiti/blob/v0.29.3/README.md : the README as of 20260727 (read 20261030 19:01 UTC)
14. https://github.com/getzep/graphiti/pull/1964 : "Upstream extraction, dedup, and temporal fixes from the Zep fork", merged 20261009 (read 20261030 19:02 UTC)
15. https://github.com/getzep/graphiti/pull/1997 : "Make the C2 prompt the default combined extraction prompt" (read 20261030 19:02 UTC)
16. https://arxiv.org/abs/2501.13956 : title, authors, single version v1 (20250120), abstract (read 20261030 19:01 UTC)
17. https://arxiv.org/html/2501.13956v1 : DMR and LongMemEval tables, caveats, models; read through a summarising fetch tool, so table values are as summarised and not checked against the PDF (read 20261030 19:01 UTC)
18. https://www.getzep.com/platform/context-graph-engine/ : Konig described as proprietary, "Available under Zep cloud and BYOC plans" (read 20261030 19:01 UTC)
19. https://www.getzep.com/blog/announcing-a-new-direction-for-zeps-open-source-strategy/ : Zep Community Edition discontinued, effort moved to Graphiti (read 20261030 19:01 UTC)
20. https://github.com/getzep/zep-papers/issues/5 : LoCoMo dispute, 20250508 to 20250519 (read 20261030 19:01 UTC)
21. https://github.com/getzep/graphiti/blob/main/graphiti_core/llm_client/gliner2_client.py : local entity-extraction client (read 20261030 19:02 UTC)
22. https://api.github.com/repos/getzep/graphiti/git/trees/main?recursive=1 : file listing of the default branch, used for driver packages, `spec/` and the absence of a roadmap file (read 20261030 19:00 UTC)
- **[J]** The July 2026 investigation of Graphiti, made 20260725 15:29 UTC at a v0.29.x state. Details marked [J] are carried over from it and were not re-read in this run.
