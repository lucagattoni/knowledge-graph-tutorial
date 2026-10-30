---
slug: graphiti
neutral-entry: ../../kb-kg/projects/graphiti.md
investigated: 20260725
updated: 20261030 19:07 UTC
licence-gate: open
---

# Graphiti: what Pinakes takes from it

The facts about the project itself are in its [neutral entry](../../kb-kg/projects/graphiti.md). This page
holds only the Pinakes-specific reading.

Pinakes facts below were read on 20261030 between 18:58 and 19:05 UTC from a local checkout of the
Pinakes `main` branch whose `STATUS.md` says "Latest release: 0.32.8 · last reviewed 20261029 18:57".
Links go to the public copies.

## Verdict

A reference for retrieval shape and tool ergonomics, not for ingestion: Graphiti's retrieval stack and
its provenance tool influenced the graph work, but its LLM-at-ingest pipeline is the opposite of
Pinakes' free path, and the one idea Pinakes built from it (expansion from search hits) did not pass its
gate.

## What Pinakes takes

The July investigation (20260725 15:29 UTC) recommended these; the next section says what became of each.

- **Confirmation of the retrieval shape.** Graphiti converged on full-text plus vector search fused by
  reciprocal rank fusion (RRF), with a cross-encoder as the premium reranker. Feeds the free pipeline,
  [DESIGN section 4.1](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md#41-the-free-pipeline-every-query-0).
- **Graph expansion as a third retrieval channel, seeded by the other channels' hits** (Graphiti's BFS
  channel), judged cheaper than Personalized PageRank: expand the neighbourhood of the top lexical and
  vector hits and let RRF fuse the result. Feeds the "bounded expansion from hits" stage of the graph
  approach (the graph release in the Pinakes roadmap). The July note proposed a recursive query over the
  existing `links` table.
- **Graph distance from a focal node as a rerank signal** (`center_node_uuid` with
  `node_distance_reranker`), as a free, local alternative or complement to PPR, and an optional "near
  this document" argument on `pinakes_search`.
- **In-degree over the `links` table as a zero-cost salience signal**, the analogue of Graphiti's
  episode-mentions reranker.
- **Invalidation instead of deletion** (the bi-temporal fields `valid_at`/`invalid_at` against
  `created_at`/`expired_at`), noted as matching the "ULIDs are permanent" principle.
- **Named search recipes** as a way to expose tuned configurations without exposing many knobs.
- **MCP result envelopes**: a uniform success shape with plural-named lists, a uniform error shape,
  embeddings always stripped, ids in every row so calls chain.
- **A provenance tool.** Graphiti has `get_episode_entities` (what did this episode create) but no
  neighbour-traversal tool; the July note judged the missing traversal tool its biggest MCP gap and said
  the planned `pinakes_links(doc_id, rel?, direction?, depth?)` was the better design to keep.

## What Pinakes leaves

| Left | July reason | What Pinakes did |
|---|---|---|
| The LLM-at-ingest pipeline (several LLM calls per episode) | Violates the free path; Pinakes had already decided never to call an LLM at sync time | Held. Only two paid entry points exist, both opt-in and capped (`--extract=claude-vision` and `pnk ask --deep`), enforced by an allowlist and CI gates; the free path is run in a fresh subprocess and asserted to load no paid client ([STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md)). |
| A server graph database as a dependency | Neo4j or FalkorDB required; the embedded backend deprecated, so betting local-first on a graph engine looked fragile | Held. The structural graph is two SQLite tables, `nodes` and `edges`, derived at sync ([DESIGN section 3.2](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md#32-the-structural-graph)). The July wording "embedded backend deprecated" is incomplete: an embedded FalkorDB exists (see Changed since July). The decision does not depend on it. |
| A fire-and-forget ingest tool | An opaque queue is the wrong shape for a local CLI where sync can be synchronous and report what changed | Held. `pnk sync` is synchronous and prints a per-kind census; the MCP server has four tools, all of which answer about content in a KB ([STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md), `pnk serve` row). |
| An extracted-entity graph as the unit of retrieval | Graphiti returns facts and entities; Pinakes returns documents and chunks with human-authored typed links; entity extraction, even lazy, belongs behind a budgeted gate | Held. The `[ner]` extra is "not built", gated on the golden set and not scheduled ([STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md), "the graph release, staged"). |
| A 13-tool MCP surface | Keep Pinakes at four or five tools | Held: four tools, `pinakes_search`, `pinakes_get`, `pinakes_links`, `pinakes_list_kbs`. |

## Where it landed in Pinakes

Sources: `STATUS.md`, `ROADMAP.md`, `DESIGN.md` and `RETROSPECTIVES.md` in the Pinakes `docs/` folder.
Searches for "Graphiti" in STATUS, ROADMAP and DESIGN find one mention, in the roadmap's 0.1.1 entry,
which lists Graphiti among the projects whose research landed on 20260727. Everything else below was
matched by idea, not by name.

| Idea | Built? | What exists | Release |
|---|---|---|---|
| RRF fusion with a cross-encoder rerank | Built before the investigation | BM25 and vector search, RRF with k=60, local cross-encoder rerank on by default ([DESIGN 4.1](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md#41-the-free-pipeline-every-query-0)). Release 0.1.0 is stamped 20260725 15:27, two minutes before the Graphiti note, so Graphiti confirmed this shape rather than shaping it. | 0.1.0 |
| Expansion from hits as an RRF channel | Built, shipped **off** | The expansion channel, `[retrieval] graph_channel`, over a derived structural graph (`schema_version` 3: chunk, document, tag, heading and directory nodes, with shared-value relations through hub nodes, plus authored links read from `links` at weight 2.0). This differs from the July suggestion, which was a recursive query over `links` alone. | 0.11.0, 20260805 07:14 |
| Gate result for that channel | Measured | On the 300-document RFC realism corpus (106,806 chunks) the channel improved 0 of 20 multi-hop questions and regressed 3 (7/20 with the channel off, 4/20 with it on; p = 1.0000), so it ships `off`. The stated finding is "reachable is not retrievable": a probe found 9 of the failing questions reachable within two hops, and retrieval lifted none. Latency was not the problem: 2012 ms per query off, 2051 ms on. Bounds the project states: no chunk in that corpus carried a `heading_path`, so three of seven edge kinds derived nothing, and two of the gate's four clauses could not fire on it ([STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md#did-the-expansion-channel-earn-its-default--no-measured-20260804-2252)). This tests Pinakes' own graph, not Graphiti's. | 0.11.0 |
| Graph distance as a rerank signal | Evaluated inside the expansion channel, not shipped as a feature | A link-distance term in the expansion ranking; the leg without it (`expand-no-link-distance`) scored the same as the full channel: 4/20, 0 improved, 3 regressed ([RETROSPECTIVES](https://github.com/lucagattoni/pinakes/blob/main/docs/RETROSPECTIVES.md)). An optional "near this document" argument on `pinakes_search`: **not found** in STATUS, ROADMAP, DESIGN, CLI, GUIDE or MANIFEST (searched for terms such as `center_node`, `near this doc` and `--near`). | 0.11.0 (measurement) |
| In-degree salience | Evaluated, reported, not gated, not shipped | The leg `expand-in-degree` scored 6/20 with 1 improved and 2 regressed (p = 0.8750), the only leg that lifted anything and still a net loss of one question against the channel off; slower, 2237 ms against 2012 ms. The project records it as "reported, never gated", a direction for a later measurement on a corpus that can carry one, not a result ([ROADMAP](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md)). | 0.11.0 (measurement) |
| Provenance and traversal tool | Built | `pnk links` (flags `--rel`, `--direction`, `--depth`, `--query`, `--json`) and the MCP tool `pinakes_links`, which returns a `frontier` and a `score` on every call; `pnk link` writes an authored link. | 0.5.0 (20260731 11:27) and 0.6.0 (20260801 10:51) |
| Invalidation instead of deletion (bi-temporal fields) | **Not built** | No `valid_at`, `invalid_at` or validity-window field appears in STATUS, ROADMAP or DESIGN (searched for `bi-temporal`, `valid_at`, `valid-time`). Documents have an `active` state and a soft delete; ULIDs are permanent and never renumbered. | none |
| Named search recipes | **Not built** as such | Not found. Each retrieval stage's width is a distinct manifest field, and a single `top_k` was rejected as ambiguous ([DESIGN 4.1](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md#41-the-free-pipeline-every-query-0)). | none |
| MCP result envelope (uniform success and error shapes, ids in every row) | Partly, unverified in detail | Search results carry document ids and path:offset citations so that `pinakes_search` then `pinakes_get` chains ([DESIGN 4.3](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md#43-multi-hop-without-paying-for-it)). The invariant "an error carries a remedy, not just a message" is a related rule. A Graphiti-style uniform `{message, list}` envelope: **unstated** in the documents read. | n/a |

## Licence gate

Open. Graphiti is Apache-2.0 (`LICENSE` file, read 20261030 18:59 UTC), the same licence as Pinakes, so
ideas, measured results and source are all usable under the licence's terms. The Pinakes documents read
do not say that any Graphiti source was copied (**unstated**).

## Changed since July 2026

Checked 20261030 19:07 UTC against the [neutral entry](../../kb-kg/projects/graphiti.md).

- **Verdict: unchanged.** The reasons for "leave" still hold: Graphiti still needs an LLM at ingest (the
  bulk path now uses one combined extraction call per episode instead of separate node and edge calls,
  which lowers the count but does not remove it), still needs a graph database, and still has no
  neighbour-traversal MCP tool among its 13 tools. Licence is still Apache-2.0.
- **One July statement here was wrong or stale and is corrected.** The leave-list said the embedded
  backend (Kuzu) was deprecated and a graph database server was "required". An embedded FalkorDB
  (`falkordblite`, Python 3.12 or later) shipped in the same release as the Kuzu deprecation. Every
  Graphiti configuration still depends on a graph database engine, so the SQLite decision is unaffected.
- **The July claim that expansion from hits is "cheaper than PPR" and fits as a free third channel**
  was a design argument. Pinakes' own measurement (above) found that the channel built on that idea did
  not lift multi-hop retrieval on its test corpus. Graphiti's own published results, for the service and
  not for the BFS channel in isolation, say nothing about this, so the July recommendation is neither
  confirmed nor refuted by Graphiti's evidence; Pinakes' result is a null on one corpus with stated
  bounds.
- **Graphiti no longer calls itself an agent-memory product** (README, 20261022 revision). This does not
  change what Pinakes takes from it.
