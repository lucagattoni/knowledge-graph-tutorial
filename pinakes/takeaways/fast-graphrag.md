---
slug: fast-graphrag
neutral-entry: ../../kb-kg/projects/fast-graphrag.md
investigated: 20260725
updated: 20261030 19:07 UTC
licence-gate: open
---

# fast-graphrag: what Pinakes takes from it

The facts about the project itself are in its [neutral entry](../../kb-kg/projects/fast-graphrag.md). This page
holds only the Pinakes-specific reading. It was split out of the July 2026 investigation (20260725 15:30 UTC)
and checked against the Pinakes documents on 20261030. Bracketed numbers such as [P1] point to the Sources
list at the end of this page.

## Verdict

Take the ideas, never depend on the package. July's finding stands: fast-graphrag's query-time stage (graph
scoring, then a score cascade to chunks) needs no LLM, which confirmed that Pinakes' recommendation R4 (rank
with Personalized PageRank as a third RRF channel, see [the recommendations](../recommendations-r1-r7.md))
costs nothing in LLM calls. Its insert-time stage (LLM extraction on every chunk) is what Pinakes declines.

## What Pinakes takes

These are the July 2026 takes, each with the Pinakes design area it fed. The July reading is kept as
written; the "Where it landed" section below says which ones were built.

| Idea in fast-graphrag | July reading for Pinakes | Design area it fed |
|---|---|---|
| Personalized PageRank (damping 0.85, undirected) seeded from the query's entities | Run PPR over the existing `links` graph as a third channel in reciprocal-rank fusion (RRF), seeded from BM25 and embedding top hits. Human-authored links make better seeds than LLM-extracted entities. July estimated a few hundred lines with `scipy` and no igraph | The graph channel (PPR recipe, stage B of the Pinakes graph approach) |
| Score cascade by sparse products (node scores to relation scores to chunk scores) | The clean way to turn graph relevance into chunk-level input for RRF | The graph channel |
| `RankingPolicy_Elbow` (cut at the largest gap in the sorted scores) | A free way to choose how many graph results deserve fusion, instead of a fixed k | The graph channel |
| Named versus generic query entities, with different thresholds | Named maps to an exact or FTS5 title match with a tight threshold; generic maps to embedding search with a loose one. Decide by heuristic (capitalisation, quotes, title-index hit), with no LLM call | Free-path query handling |
| Content-hash chunk ids (xxh3), so unchanged chunks cost nothing on re-insert | Pinakes should already hash; fast-graphrag shows a fast non-cryptographic hash is enough | Incremental sync |
| Alias handling as explicit `is` edges, not destructive merges | Fits the invariant that ULIDs are permanent and never renumbered | Identity and links |
| `domain`, `example_queries`, `entity_types` templated into prompts | A `pnk ask --deep` agent could carry KB-level "domain, typical queries, link types" from `pinakes.toml` to steer query-scoped extraction, with results written back to sidecars. Consistent with "lazy, budgeted, written to committed files" | The deep path |

**One support for these takes is weaker than July wrote.** July said fast-graphrag "validates that the
cascade works and wins on multi-hop questions (93% vs 42% for pure vectors)". Both numbers come from the
vendor's own benchmark on 51 and 101 questions of one dataset, and the vendor's "GraphRAG" baseline is
`nano-graphrag`. An independent benchmark (GraphRAG-Bench, ICLR 2026) has fast-graphrag below a reranked vector
baseline on fact retrieval and below HippoRAG2 on most cells; details and sources are in the
[neutral entry](../../kb-kg/projects/fast-graphrag.md#evidence). Neither benchmark runs on a link graph, so
neither measures what Pinakes would build.

## What Pinakes leaves

| Left | Why (July reasoning) |
|---|---|
| LLM extraction at sync time | The whole insert pipeline (an extraction call per chunk, optional gleaning, summarise-on-merge) breaks the free path and the "never LLM extraction at sync time" decision. It also makes a rebuild expensive, which conflicts with `.pinakes/` being disposable |
| Pickle-everything storage (`igraph_data.pklz`, pickled key-value stores) | Opaque and version-fragile; contradicts one SQLite index plus committed files. Edges belong in the `links` table; PPR can load them into `scipy` at query time |
| `igraph` and `hnswlib` as dependencies, and the `vertexai` and `voyageai` SDKs as hard dependencies | Redundant with SQLite FTS5 and the existing embedding index; vendor SDKs are weight Pinakes' core avoids |
| Exact-name node merging | Brittle; the ULID plus sidecar identity is stronger |
| Depending on the package | Maintenance. July: "no commits since 2025-11-01, version 0.0.5, unimplemented stubs". Still true on 20261030, see below |

## Where it landed in Pinakes

Read from the Pinakes `STATUS.md`, `ROADMAP.md` and `DESIGN.md` on 20261030 19:03 UTC [P1][P2][P3]. Short
answer: **the PPR channel was not built; a different graph channel was built, measured, and ships off.**

| July take | Outcome in Pinakes | Where it says so |
|---|---|---|
| PPR as a third RRF channel | **Not built.** It is "the graph release, staged": the PPR channel and the `[ner]` extra, "eval-gated, never scheduled". There is deliberately no implementation plan. The setting `[retrieval] graph_channel` refuses the value `"ppr"`, because a setting the code does not implement is not a setting. Decided 20260804: PPR's gate does not run at all on a corpus below the heading-coverage floor. What exists is a written gate plan, [`plans/20260804_1016-staged-channel-gates.md`](https://github.com/lucagattoni/pinakes/blob/main/plans/20260804_1016-staged-channel-gates.md) | [STATUS, release roadmap](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md#release-roadmap); [ROADMAP, the graph release, staged](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#the-graph-release-staged--gates-only-not-scheduled); [DESIGN](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md) |
| Graph-to-chunk score cascade | **Not built** as such (it belongs to the PPR channel). The channel that was built expands from first-stage hits; it does not use fast-graphrag's cascade | same as above |
| Elbow cutoff | No mention found in `STATUS.md`, `ROADMAP.md` or `DESIGN.md` (searched for "elbow"). Treat as not built | [P1][P2][P3] |
| Named versus generic split | No mention found (searched "named" with "generic"). Treat as not built | [P1][P2][P3] |
| Content-hash identity | Pinakes keeps a content hash per **document** (`documents.content_hash`) and compares it with the file on disk during sync. Chunk-level hash skipping is not described in the passages read, and the hash function was not stated there. Whether this idea came from fast-graphrag is not recorded | [DESIGN, sidecar and schema sections](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md) |
| `is` alias edges | No mention found. Treat as not built | [P3] |
| `domain` and `example_queries` in `pinakes.toml` for `--deep` | Not found: no occurrence of `example_queries` or `entity_types` in the three documents. `pnk ask --deep` shipped in 0.24.0 (20260811) and was completed in 0.26.0, as a budgeted loop of retrieve and answer over the same free-path search, with no KB-level domain setting found. It prints suggested links for the user to commit; it does not write a graph | [ROADMAP, 0.24.0](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#0240--pnk-ask---deep-answers--20260811-2224); [STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md) |

**What was built instead, and what it measured.** The graph release shipped structural edges and an
**expansion channel** behind `[retrieval] graph_channel`. Its gate ran on the RFC realism corpus on 20260804.
Multi-hop questions answered: 7 of 20 with the channel off, 4 of 20 with it on (all edge kinds, and without
authored edges). Improved 0, regressed 3, exact sign-test p = 1.0000. So `expand` ships `off`. The finding the
Pinakes documents draw is "reachable is not retrievable": 9 of the failing questions were reachable within two
hops, and the channel lifted none. The same document says the result "licenses neither PPR nor the `[ner]`
extra" [P1][P2]. Link: [Did the expansion channel earn its default?](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md#did-the-expansion-channel-earn-its-default--no-measured-20260804-2252).

**Not measured.** PPR itself, on Pinakes' graph, has never been run, so nothing in Pinakes tests the July
claim that authored links make better seeds than extracted entities. The Pinakes documents also record that two
of the gate's four clauses could not fire on that corpus and that no chunk in it carried a heading path [P1].

## Licence gate

Open. The `LICENSE` file is MIT (copyright line "2024 circlemind-ai"), the README badge agrees, and Pinakes is
Apache-2.0, so copying code with the notice would be permitted. July nevertheless advised ideas only, never
code or dependency, for engineering reasons (storage, dependencies, maintenance), not for licence. Ideas and
measured results are free to reuse in any case.

## Changed since July 2026

Checked 20261030 19:03 to 19:07 UTC.

- **Project side: no change to the verdict.** Still no commit since 20251101; the project does not look
  maintained, and its managed-service docs address now redirects to a different product's docs. See the
  [neutral entry](../../kb-kg/projects/fast-graphrag.md#changed-since-the-july-2026-investigation). The "never
  depend on the package" rule is reinforced, not changed.
- **Evidence side: the case for the take is thinner.** The July sentence quoted above relied on the vendor
  benchmark alone; the independent benchmark is more mixed. This does not change the verdict, because Pinakes
  already treats PPR as eval-gated and unbuilt, but it removes the July claim that fast-graphrag
  "validates" the cascade.
- **Pinakes side: a gate result arrived after the July investigation.** The expansion channel failed its gate
  on 20260804, ten days after the investigation. It is a different channel from PPR, and the Pinakes documents
  say it does not license PPR [P1][P2].
- **July corrections that touch this page:** fast-graphrag's default extraction is one LLM call per chunk, not
  "2+", and only entities are embedded, not chunks. Neither changes a take or a leave; the leave on LLM
  extraction at sync time holds at one call per chunk. Details are in the neutral entry.

## Sources

Read 20261030 19:03 UTC from a local checkout of the Pinakes repository (its HEAD commit is dated 20261030
08:02 UTC). Whether the public `main` branch the links point to is identical was not checked.

- [P1] https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md : release roadmap, 0.20.1 entry, the expansion-channel measurement
- [P2] https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md : "The graph release, staged", the expansion-channel gate, the deep release
- [P3] https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md : `graph_channel` and `"ppr"`, `documents.content_hash`, the staged-channel row
- The July 2026 investigation of this project (internal, superseded; no URL): the takes, leaves and quoted sentences above
