---
slug: datastax-graph-rag
neutral-entry: ../../kb-kg/projects/datastax-graph-rag.md
investigated: 20260726
updated: 20261030 19:07 UTC
licence-gate: open
---

# datastax/graph-rag: what Pinakes takes from it

The facts about the project itself are in its [neutral entry](../../kb-kg/projects/datastax-graph-rag.md). This page
holds only the Pinakes-specific reading. The Pinakes side was read from the `docs/` of the Pinakes
repository (`STATUS.md`, `ROADMAP.md`, `DESIGN.md`) on 20261030 between 18:58 and 19:06 UTC (the clock was read at the start and the end of that span only).

## Verdict

A quarry for traversal mechanics and for a LazyGraphRAG blueprint; never a dependency. The July
verdict stands, and the reason for "never a dependency" is now stronger (see the last section).

## What Pinakes takes

Structural twin: metadata-defined edges over an existing store is the sidecar position, with the
graph held in per-document metadata and joined at query time. The July reading was that this
"validates" the `links` table plus tag columns with no graph database. See the correction under
"Changed since July 2026": the project shows the approach is workable, not that it retrieves better.

| # | Idea, as the July investigation listed it | What it was meant to feed |
|---|---|---|
| 1 | The `(source_field, target_field)` vocabulary expresses every planned Pinakes edge type: sidecar `links` is `("links.cites", "$id")`, shared tag is `("tags", "tags")`, co-located is `("dir", "dir")`, sibling and parent-child are id edges; direction is the flipped pair, and `rel` becomes which spec is enabled. | The edge-type design for `links` and the structural graph |
| 2 | **Query-ranked expansion.** Neighbours are fetched per edge but kept only as the top `adjacent_k` by similarity to the query, which stops hub edges such as popular tags from flooding the traversal: bounded fan-out with relevance-ordered truncation. Apply it to the shared-tag and co-located edges, which are Pinakes' hub risks. | The traversal tool behind `pinakes_links` at depth above 1 |
| 3 | **Visited-edge dedup.** Dedupe on `(edge type, value)`, not only on document ID, so a shared value expands once globally. | Same traversal |
| 4 | The knob set `select_k`, `start_k`, `adjacent_k`, `max_depth`, plus per-edge minimum-depth tracking (`select_next_edges`): proven, minimal, sufficient. | `pinakes_links` depth above 1 |
| 5 | `NodeTracker`'s two verbs, `select` (return this) and `traverse` (expand this): the right abstraction if traversal strategies ever become pluggable. | A possible pluggable-strategy API |
| 6 | Best-first MMR traversal (`Mmr._next`) as a free-path option: pure numpy, no model call, diversity-aware multi-hop expansion. | The free retrieval path |
| 7 | The LazyGraphRAG chain as a blueprint for `pnk ask --deep`: traverse for free, then budgeted claim extraction and logprob ranking over communities of the retrieved subgraph only. Girvan-Newman until modularity peaks on about 100 nodes is cheap and gives the unit of claim extraction; the logprob of `True` is a one-token relevance scorer. | `pnk ask --deep` |

On cost, July placed the LazyGraphRAG chain as strictly a `--deep`-shaped workload: it makes dozens of
gpt-4o calls per query (the call count is the July estimate from the notebook's structure, not a
measurement), which is cheap next to eager graph construction and expensive next to Pinakes' free
path. Index time (embeddings plus local NER, no LLM) matches Pinakes' sync-time position.

## What Pinakes leaves

| What | Why |
|---|---|
| Query-time filter-join adjacency | The project's store has no edge table, so every hop is an ANN query with a metadata filter. Pinakes has SQLite: precomputed `links` rows and SQL joins are cheaper, exact and support PPR. Take the ranking and truncation, not the join mechanism. |
| The LangChain layering (`GraphRetriever`, transformers) | Integration glue only. |
| Per-claim LLM ranking calls | Cost grows linearly with the number of claims; Pinakes' local cross-encoder does the same job for free on the free path. Reserve logprob ranking for `--deep`, if at all. |
| Vector-only seeding | The project has no BM25 or hybrid search in the files read; July judged Pinakes' RRF seeding strictly stronger. That is a judgement, not a measurement. |
| `max_traverse` and the deprecated `Id` and `k` shims | Dead code and API-churn artifacts. |
| A dependency on the library | Not archived, but silent since 20250505 and at 91 stars (20261030 18:58 UTC) no community carries it. Quarry only. |

## Where it landed in Pinakes

No Pinakes document names this project: a search of `STATUS.md`, `ROADMAP.md` and `DESIGN.md` for
"datastax" found no match (20261030, 18:58 to 19:06 UTC). Which shipped feature owes something to it is
therefore **unstated**. What can be said is what was built beside each idea, in the three documents
that say what Pinakes has built: [`STATUS.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md),
[`ROADMAP.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md) and
[`DESIGN.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md).

| # | Idea | Landed? | Evidence |
|---|---|---|---|
| structural twin | A graph without a graph database | Built, as a derived `nodes`/`edges` table in SQLite, not as metadata joins. Shipped in 0.11.0, `schema_version` 3, with chunk, document, tag, heading and directory nodes. | STATUS, the 0.11.0 row; DESIGN section 3.2 |
| 1 | Two-field edge vocabulary | Not built as a vocabulary. Edge kinds are fixed in a table (`membership`, `sibling`, `parent-child`, `in-section`, `co-located`, `shared-tag` and authored links), each with a read-time weight. | DESIGN section 3.2 |
| 2 | Bounded, ranked fan-out | Partly. `pnk links` shipped in 0.5.0 (20260731 11:27 UTC) with depth capped at 3 server-side and fan-out capped. DESIGN section 4 specifies `[retrieval] adjacent_k` as the fan-out cap per expansion, applied after ranking. Whether the ranking is by similarity to the query is unstated in the lines read, and neither STATUS nor ROADMAP mentions `adjacent_k`, so whether it ships as a setting is unstated. | ROADMAP, 0.5.0; DESIGN section 4 |
| 2 (hub control) | Stop hubs flooding | Built a different way: damping. Hub spokes carry weights of 1/tag-degree, 1/dir-size and 1/section-size, so a large hub damps superlinearly. | DESIGN section 3.2 |
| 3 | Visited-edge dedup | In the design: a hub node exists so that "the channel's visited-edge dedup" expands a shared value "once globally instead of once per encounter". | DESIGN section 3.2 |
| 4 | Knob set | Partly: a depth bound counted in logical hops and `adjacent_k`. Per-edge minimum-depth tracking and the other knobs: not found. | DESIGN section 4 |
| 5 | Two-verb strategy API | Not built. No pluggable traversal strategy appears in the three documents. | search of DESIGN, STATUS |
| 6 | Best-first MMR traversal | Not built. No "MMR" or "maximal marginal" in the three documents. | search of DESIGN, STATUS, ROADMAP |
| 7 | LazyGraphRAG-style `--deep` | Not built. `pnk ask --deep` shipped in 0.24.0 (20260811 22:24 UTC) as "one synthesis call when confident, decompose-search-answer-refold when not". The three documents contain no match for "community", "Girvan" or "logprob". | STATUS, `pnk ask`; ROADMAP, [0.24.0](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#0240--pnk-ask---deep-answers--20260811-2224) |
| channel | The expansion channel itself | Built, measured, and **off**. `[retrieval] graph_channel` ships `off` in 0.11.0 (20260805 07:14 UTC). | STATUS, [the numbers](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md#did-the-expansion-channel-earn-its-default--no-measured-20260804-2252) |

**What the gate measured** (STATUS, "Did the expansion channel earn its default?", measured 20260804 22:52
UTC, on the RFC realism corpus): with the channel off, 7 of 20 multi-hop questions answered; with it on,
4 of 20, with 0 improved and 3 regressed (one-sided sign test p = 1.0000). Latency was 2012 ms per
query off against 2051 ms on (1.02 times). The channel's extra candidates displaced three answers that
two-list fusion already had. STATUS locates the harm in the document-level path: `membership` transit
into the `co-located` (262 edges) and `shared-tag` (643) hubs pulls whole documents' chunks into the
fusion, and the `sibling` edges (106,506 of 107,411 non-transit structural edges) were inert. STATUS
states two bounds: two of the gate's four clauses could not fire on that corpus, and no chunk in it
carried a `heading_path`. What would change the result is "a corpus or a different channel design, never
a more expensive one" (Pinakes
[decision record](https://github.com/lucagattoni/pinakes/blob/main/plans/20260804_1442-decision-g3-go.md)).

Read against this project, the measurement bears on idea 2: the hub risk July flagged for shared-tag and
co-located edges did show up in Pinakes' own numbers. Pinakes answered it with degree damping; the
project's mechanism (keep only the top `adjacent_k` by similarity to the query) was **not tested**
against the same gate, as far as the three documents say. That is an open experiment, not a finding.

## Licence gate

Open. The `LICENSE` file at the repository root is the Apache License 2.0, and the GitHub licence field
agrees ([neutral entry](../../kb-kg/projects/datastax-graph-rag.md), sources 1 and 3). Pinakes is also
Apache-2.0 (DESIGN, header). Ideas and measured results are free to reuse; if source is ever copied, read
the attribution and notice conditions in the `LICENSE` file first. The standing posture is stricter than
the licence requires, and for a different reason: dormancy, not licence, is why this is a quarry and
never a dependency.

## Changed since July 2026

Checked 20261030 19:07 UTC (project data snapshot 20261030 18:58 UTC).

- **Dormancy confirmed and deeper.** No push since 20250505 (543 days at the
  snapshot), no release since v0.8.0, and a top contributor wrote on 20251113 that they no longer have
  write access; community pull requests on a Chroma import break sit unmerged
  ([neutral entry, "Changed since the July 2026 investigation"](../../kb-kg/projects/datastax-graph-rag.md)).
  The verdict does not change; the reason for "never a dependency" is firmer. No archival, deprecation
  or successor notice was found.
- **July's "validates" was too strong.** The July text said the project's conclusion "validates the
  `links` table + tag columns design". The project shows that metadata-defined edges are workable as a
  library; it publishes no retrieval-quality benchmark (neutral entry, Evidence). Pinakes' own gate on
  its RFC realism corpus found no gain from graph expansion (above). The "takes" section is reworded
  accordingly.
- **July's dormancy timing was loose.** "Right after IBM's acquisition" is corrected in the neutral
  entry: the last push came about ten weeks after the announcement and about three weeks before the
  close. No source read says the acquisition caused it.
- **July's size figure was wrong.** About 10 files and 2k lines became 24 files and 3,132 lines in the
  core package, plus 19 files and 2,559 lines in the LangChain package. For a quarry this raises the
  reading cost, not the value.
- **Open item from July's take 2.** Applying the similarity-ranked fan-out cap "verbatim" to shared-tag
  and co-located edges has not been shown tried. It is the one July recommendation that the later
  measurement leaves open rather than answers.
