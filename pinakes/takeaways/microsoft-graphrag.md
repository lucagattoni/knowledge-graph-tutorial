---
slug: microsoft-graphrag
neutral-entry: ../../kb-kg/projects/microsoft-graphrag.md
investigated: 20260725
updated: 20261030 19:07 UTC
licence-gate: open
---

# Microsoft GraphRAG and LazyGraphRAG: what Pinakes takes from them

The facts about the project itself are in its [neutral entry](../../kb-kg/projects/microsoft-graphrag.md).
This page holds only the Pinakes-specific reading. It began as the Pinakes half of the 20260725
investigation and was re-read on 20261030 against the live repository and against Pinakes'
[`STATUS.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md) (latest release 0.32.8,
last reviewed 20261029 18:57; read 20261030 19:02 UTC).

## Verdict

GraphRAG is the strongest outside evidence for Pinakes' standing rules (no LLM extraction at sync, free
structural edges, lazy and budgeted reasoning at query time). Keep its query-time patterns on file as
reference, leave its indexing pipeline, and do not wait for LazyGraphRAG code. The verdict is unchanged
on 20261030.

## What Pinakes takes

The ideas adopted or kept on file, with the Pinakes design section each one feeds
([`DESIGN.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md)).

| Idea | Where it comes from | Feeds |
|---|---|---|
| **Microsoft's own trajectory as support for "no LLM extraction in `pnk sync`".** The open-source library went from the Standard method (LLM extraction per chunk) to the Fast method (noun-phrase graph, no LLM for the graph), and the LazyGraphRAG blog describes an index with no LLM at all and query-time, budgeted assessment [neutral entry]. | Recommendation R1 in [`../recommendations-r1-r7.md`](../recommendations-r1-r7.md) | DESIGN §1 and §4.1 (the free path) |
| **The relevance-test budget as the single cost knob.** LazyGraphRAG's one parameter (tested at 100, 500 and 1,500 relevance tests, spent best-first, hard-stopped) is the model for a single legible cost dial. `rate_relevancy` is a complete reference: a 0 to 10 JSON rating, majority vote over repeats, and per-call accounting of calls and tokens returned to the caller. | LazyGraphRAG blog; `query/context_builder/rate_relevancy.py` | DESIGN §5 (cost control) and §4.3 |
| **Iterative deepening over a cheap hierarchy** (`DynamicCommunitySelection.select`): rate coarse things first, descend only on relevance, fall through a level when nothing matches. The Pinakes analogue is rating documents (titles, abstracts) before chunks inside `--deep`. | `query/context_builder/dynamic_community_selection.py` | DESIGN §4.3 |
| **Best-first seeding, breadth-first testing.** Seed from the existing RRF ranking, then test link-graph neighbours breadth-first under the budget. This is a recipe for the caller's agent composing `pinakes_search` and `pinakes_links`, with no framework inside Pinakes. | LazyGraphRAG blog | DESIGN §4.3 |
| **PMI edge weighting** (`calculate_pmi_edge_weights`), only if Pinakes ever derives free co-occurrence edges to feed a Personalized PageRank channel. | `graphs/edge_weights.py` | DESIGN §3.2; the staged graph release |
| **Golden-set discipline.** Their published win-rate-against-budget curves are the model for how a `--deep` change should be justified, matching Pinakes' existing evaluation rule. | LazyGraphRAG blog | DESIGN §7 |

One further point from the July reading, kept as a hypothesis and not as a finding: Pinakes starts ahead
of the noun graph, because human-authored typed `links:` sidecars should be higher-precision edges than
noun-phrase co-occurrence, at zero build cost. See the table below for what has and has not been tested.

## What Pinakes leaves

| Left | Why |
|---|---|
| **The whole Standard indexing pipeline** (per-chunk extraction, gleanings, per-entity summarisation, per-community reports) | It violates the free path. Because `.pinakes/` is disposable, a rebuild would re-pay every pass. GraphRAG's mitigation is a prompt cache; Pinakes' is never paying. At defaults the extraction alone is two LLM calls per chunk. |
| **Precomputed community reports as index artifacts** | They are paid summaries that go stale and make rebuilds paid. Any summarisation stays query-time and budgeted, with write-back to sidecars. |
| **Map-reduce global search** | The cost grows with the corpus: one call per batch of reports on every question. |
| **DRIFT's in-library agent loop** | Pinakes deliberately leaves multi-hop composition to the caller's agent. An epochs-and-follow-ups loop inside the library would duplicate the MCP client's job. |
| **Entity resolution as GraphRAG does it** | Entities are grouped on uppercased title and type, with no semantic resolution. ULID links make the problem structurally absent in Pinakes, so it should not be reintroduced through extraction. (The July text said "uppercase exact match" on title alone; the code groups on title and type. The reason to leave it is unchanged.) |
| **Waiting for LazyGraphRAG code** | The "next priority" promise dates from 20241209 and no engine has landed in nearly 23 months. Treat the blog as the specification and the open-source ingredients as reference code. Since 20260814 the README says the project is in maintenance mode with no new features. |

## Where it landed in Pinakes

Source: Pinakes [`STATUS.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md),
[`ROADMAP.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md),
[`DESIGN.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md) and
[`MANIFEST.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/MANIFEST.md), all read
20261030 19:02 UTC (STATUS: release 0.32.8). A search of STATUS, ROADMAP and DESIGN for "LazyGraphRAG",
"relevance test", "rate_relevancy", "PMI", "iterative deepening" and "best-first" found none of them.
The only mention of Microsoft GraphRAG by name is in the ROADMAP entry for 0.1.1, which lists it among
the projects investigated. (DESIGN also cites a study from the GraphRAG-Bench line, which is a
different thing.) **So no document says Pinakes built any of these ideas as such; the rows below
compare what was built with the idea.**

| Idea | Built? | What exists |
|---|---|---|
| No LLM extraction in `pnk sync` | **Held** | ROADMAP states the paid-path allowlist is "complete at two entries": the opt-in Claude-vision PDF extractor (0.3.0) and `pnk ask --deep` (0.24.0). Neither extracts entities or relations. The `[ner]` extra is staged: gated on measurement and not scheduled. |
| Free structural edges | **Built, 0.11.0** | A derived `nodes`/`edges` graph over chunk, document, tag, heading and directory nodes, with hub reporting in `pnk doctor`. The expansion channel that uses it **ships off**: on the RFC realism corpus it improved 0 multi-hop questions and regressed 3 (multi-hop 7 of 20 with it off, 4 of 20 with it on, p = 1.0000; measured 20260804 22:52). The finding recorded is that "reachable is not retrievable". |
| Relevance-test budget as the single cost knob | **Not built as described** | `pnk ask --deep` is budgeted in euros, not in relevance tests: `per_operation_eur` 2.00 and `daily_eur` 6.00 are hard ceilings and `[deep] max_rounds` is 3. The whole operation is priced and refused before the first call. A round is two paid calls (decompose, then answer from merged retrieval); there is no per-chunk or per-document relevance-rating pass. |
| Iterative deepening (rate documents before chunks) | **Not built** | Nothing in the `--deep` description in DESIGN §4.3 rates documents before chunks. |
| Best-first seeding and breadth-first testing over link neighbours | **Not built as a budgeted test** | The free path is BM25 plus vector search with fusion and rerank. The nearest thing is the expansion channel above, which is off. `pnk links` and `pinakes_links` exist for a caller's agent to walk links. |
| PMI edge weighting | **Not built** | No co-occurrence edges are derived. The Personalized PageRank channel and the `[ner]` extra are "eval-gated, never scheduled", with deliberately no implementation plan. |
| Golden-set discipline | **Built** | The golden set grew from 41 to 74 questions in 0.7.0, and a 110-question golden set, authored blind and frozen, scores the RFC corpus. Gates use exact sign tests, and results are recorded with "nothing tuned after seeing the number". |
| Authored typed links beat noun co-occurrence | **Untested** | No co-occurrence baseline was built, so there is no comparison. In the expansion measurement the arm with authored edges and the arm without scored the same (4 of 20, 0 improved, 3 regressed), and STATUS records the `authored` weight as "measured, and it changed no outcome". That corpus has authored links on 160 of 300 documents (53.3%) in two relation kinds, with a median out-degree of 1 and one document linking to 86, so authored edges were present in the test. This says nothing about noun-phrase edges, which were never built. |

## Licence gate

**Open.** The `LICENSE` file is MIT, Copyright (c) Microsoft Corporation (read 20261030 18:58 UTC; see the
neutral entry). Pinakes is Apache-2.0. MIT permits copying code if the copyright and permission notice
travel with it. Ideas and measured results are free to reuse. Nothing has been copied: the July decision
was to treat the code as a reference, and the "where it landed" table shows no GraphRAG code in Pinakes.

## Changed since July 2026

- **20261030 (checked).** The README has said since 20260814 that GraphRAG is "largely in maintenance
  mode" and will take no new features or PRs. Effect on this page: the reference code is now
  effectively frozen, which suits a reference and strengthens the "do not wait" row. The verdict is
  unchanged.
- **20261030 (checked).** LazyGraphRAG is still not in the open-source library at v3.3.0. A collaborator
  closed the tracking issue as not planned on 20251118 ("no ETA"). One July sentence in the neutral
  entry ("no maintainer update since 20241209") was wrong and is corrected there.
- **20261030 (checked).** Two July figures behind the "cost case study" were off: at defaults the
  extractor makes exactly two calls per chunk, not two to three, and entity merging uses title plus
  type. The conclusion drawn from them does not change.
- **20261030 (checked).** The July page recommended building `--deep` around the relevance-test budget.
  Pinakes shipped `--deep` on a euro budget with a decompose-and-answer round instead, and no document
  read ties that choice to LazyGraphRAG. The "takes" table above stays as reference, not as a plan.
  Whether a relevance-test mode is worth testing is a question for the experiments section, not
  settled here.
