---
type: page
order: 1
updated: 20261102 20:16 UTC
---

# The Pinakes graph approach

This page answers what the Pinakes approach to a [knowledge graph](../index/knowledge-graph.md) and to [multi-hop questions](../index/multi-hop-question-answering.md) is, how much of it exists today and where the seven recommendations (R1 to R7) stand, and what the in-house precedent ClaudeKB taught. Status is judged by Pinakes' own STATUS.md, which wins wherever the archive disagrees; the disagreements are listed.

## The approach

The question was how to get a graph that is lazy, agent-driven and budget-tunable, without paying for an LLM-built graph at index time. The July 2026 decision record answers with three layers, free until the last one [8]:

| Layer | What it does | Cost |
|---|---|---|
| Sync time | derive edges from what the index already holds (document structure, tags, directories) and from links the user authored in sidecars | free |
| Query time | a graph channel fused with the [BM25](../index/bm25.md) and [vector](../index/vector-search.md) lists by [rank fusion](../index/reciprocal-rank-fusion.md); a typed, capped `pinakes_links` tool for the caller's agent | free |
| `--deep` only | a budgeted loop that decomposes a hard question, searches each part and answers from merged evidence | paid, capped |

The three adjectives, as the design uses them [8][5]:

- **Lazy.** Nothing is precomputed that is not free. Nothing paid is spent twice: what a paid run learns is offered back as sidecar entries the user can commit, after which it is free.
- **Agent-driven.** Multi-hop reasoning is not a second agent framework inside Pinakes. `pinakes_search`, `pinakes_get` and `pinakes_links` are composable tools, and the caller's agent runs the plan-retrieve-read-refine loop in its own context. Pinakes' own `--deep` loop is for the command line and cron, where no agent is present, and is not exposed as an MCP tool; a test asserts the server never loads it [5].
- **Budget-tunable.** One number per operation (the per-operation cap), one gate per channel (`[retrieval] graph_channel`), every default set by a measurement on a golden set of questions, not by intuition [8]. At the shipped defaults STATUS prices the cheap `--deep` branch at EUR 0.2627 and a three-round loop at EUR 1.6872, with `per_operation_eur` 2.00 and `daily_eur` 6.00 [1]. Those two EUR figures carry no date and no exchange rate, and the rate in `prices.toml` has moved since (see "Left unstated").

The approach sits on Pinakes' existing [hybrid search](../index/hybrid-search.md), whose BM25 and vector lists are fused with reciprocal rank fusion (k = 60) [5]. It takes the agent-driven loop from [Graph-R1](../../kb-kg/projects/graph-r1.md), the third-channel shape from [Graphiti](../projects/graphiti.md) and the ranking idea from [HippoRAG](../projects/hipporag.md) ([personalized PageRank](../index/personalized-pagerank.md)) [8]. The per-project reading is in [takeaways](takeaways.md).

## Status today, against STATUS.md

STATUS.md names itself the only place that says what is built, and it names unbuilt work instead of numbering it [1]. Read on 20261102 19:37 UTC, when the repository's main branch stood at commit d2f0d53 [6], it states "Latest release: 0.32.9" and "last reviewed 20261102 15:19" [1].

| Part of the approach | State | Release | Source |
|---|---|---|---|
| Authored links: `pnk links`, `pinakes_links`, reverse scan | built | 0.5.0 | [1] |
| Authoring and coverage: `pnk link`, `pnk doctor` link coverage | built | 0.6.0 | [1] |
| Structural edges (`nodes` and `edges` over chunk, document, tag, heading and directory nodes) | built; `schema_version` 3 forces one free rebuild | 0.11.0, "the graph release" | [1] |
| Expansion channel (`graph_channel`) | built and **off by default** after a failed gate | 0.11.0 | [1][3] |
| Personalized PageRank channel | **not built**: staged, eval-gated, not scheduled; a manifest naming `"ppr"` is not accepted | none | [1][2][3] |
| `[ner]` extra (entity mentions) | **not built**: staged, eval-gated, not scheduled | none | [1][2] |
| Heading paths for plain text (`[chunking] headings = "numbered"`) | built, opt-in | 0.13.0 | [1] |
| `pnk ask` (free: evidence, confidence, price of answering) | built | 0.23.0 | [1] |
| `pnk ask --deep` (paid, capped) | built; working against the live API since 0.25.1 | 0.24.0, final cut 0.26.0 | [1] |
| Suggested `links[]` printed after a deep run | built; prints, never writes | 0.26.0 | [1] |
| `--write-suggestions` | deferred, "unplanned" | none | [1] |
| Metadata injection into embedded text (`[chunking] metadata`) | measured, no gain, ships `off` | 0.16.0 | [1] |
| `pnk adopt` (ClaudeKB onboarding) | not built; owning release unanswered | none | [7] |

### The one gate that decided the graph channel

The expansion channel defaults on only if an exact one-sided sign test finds enough multi-hop questions improving [1]. Run on a 300-document RFC corpus (20 multi-hop questions): with the channel off 7 of 20 passed, with it on 4 of 20, with 0 improved and 3 regressed, p = 1.0000 [1]. STATUS states the finding as "`reachable ≠ retrievable`": a reachability probe had found 9 of the failing questions reachable within two logical hops without authored edges, and the retrieval instrument lifted none [1]. Latency was not the cost: 2012 ms per query off, 2051 ms on, on a 106,806-chunk index [1]. The numbers and their bounds are in [measurements](measurements.md).

## Where STATUS.md wins over the archive

| Topic | The archive says | STATUS.md or the primary source says now | Source |
|---|---|---|---|
| Latest release | 0.32.8, last reviewed 20261029 18:57 (R1 to R7 file, approach status block, ClaudeKB page) | 0.32.9, last reviewed 20261102 15:19. The 0.32.9 row changes the `--offline` load of `sync`, `search`, `ask`, `links` and `serve`, a `pnk doctor` hint and the exchange rate in `prices.toml` (`usd_per_eur` 1.113 to 1.1172), the table that prices `--deep`. It does not touch the graph channel | [1][2][8][9] |
| Does the expansion channel enter fusion? | R4 note: "unstated" | The manifest reference says what the channel reaches is "ranked and fused as a **third** input" | [3][9] |
| Version labels (v0.3, v0.4) in the R1 to R7 summary | kept as the July record | STATUS: "Never write `v0.4` for something unbuilt". This page uses release names and numbers only for shipped work | [1][9] |
| Edges on the RFC corpus | R3 note: 107,411 edges | STATUS gives 107,411 non-transit structural edges in the gate section and 107,802 edges in the earlier reachability section for the same corpus. This page uses 107,411 for the gate | [1][9] |
| Re-run on a corpus with sections | recorded as taken, run status unstated | ROADMAP: taken by the user on 20260825 18:16 as its own three-leg gate, to run later, expected null. No result found in STATUS or ROADMAP: still **unstated** whether it ran | [2][8] |
| "The template release" in the July body | an update note already corrects four places | the name left STATUS's unbuilt-work table at 0.22.0; the `sqlite-vec` tier is "staged" under its own name | [1][8] |

## The seven recommendations

The recommendations are the Pinakes-specific half of a July 2026 literature review (original date 20260725; wording kept in the archive file) [9]. The status column is STATUS.md read now. What the field's papers have reported since July is annotated in the [archive file](../../pinakes/recommendations-r1-r7.md) and is not restated here, because each figure there carries a 2026 date and would need its own re-check.

| # | Recommendation (July wording, shortened) | Status today | Release or gate |
|---|---|---|---|
| R1 | No LLM entity or relation extraction in `pnk sync` | held; nothing built | policy |
| R2 | Prioritise authored links | built | 0.5.0, 0.6.0 |
| R3 | Free structural edges at sync | built; reading channel off | 0.11.0; gate 20260804 22:52 not passed |
| R4 | Personalized PageRank as a third fusion channel | not built; a different channel built and off | staged, not scheduled |
| R5 | If extraction is ever added: lazy, agent-driven, written back to sidecars | not built; the budgeted path it needs is built | `--deep` 0.24.0 to 0.26.0 |
| R6 | Expose the graph to the caller's agent; no traversal policy inside Pinakes | built, with one departure | 0.5.0 |
| R7 | Measure before shipping | built, and used | 0.7.0, 0.16.0 |

**R1: held.** STATUS lists two paid entry points, the `claude-vision` extractor and `pnk ask --deep`; neither extracts entities or relations at sync [1]. The staged `[ner]` extra is eval-gated and not scheduled [1][2]. The July approach proposes spaCy for it, not an LLM; STATUS does not say, so what `[ner]` would use is **unstated** [8].

**R2: built.** 0.5.0 shipped `pnk links`, the `pinakes_links` tool and the reverse scan of partner KBs; 0.6.0 shipped `pnk link`, which writes one `links[]` entry into the source document's own sidecar, and the link-coverage report in `pnk doctor` [1].

**R3: built, reading channel off.** The 0.11.0 graph release derives the structure; `pnk doctor` reports the highest-degree hubs [1]. On the RFC corpus, `sibling` edges were 106,506 of 107,411 and removing them changed nothing; the harm came from document-level transit into the `co-located` (262 edges) and `shared-tag` (643 edges) hubs [1]. No chunk on that corpus carried a heading path, so the parent and in-section edge kinds derived zero edges; 0.12.0 added the coverage report and 0.13.0 the opt-in fix [1]. The verdict ROADMAP draws is narrow: the edge kinds that worked did not help this corpus, not that graph structure does not help [2].

**R4: gated, PPR not built.** The setting `graph_channel` takes `"off"` or `"expand"`; `"ppr"` is not accepted, "a setting that silently does nothing" being the reason given [3]. ROADMAP: PPR has no implementation plan "by design", its gate does not run on a corpus below the heading-coverage floor, and the gate result "licenses neither PPR nor the `[ner]` extra" [2]. One variant, `expand-in-degree`, "was the one leg that lifted anything"; it is reported, never gated, and the size of the lift is **unstated** in the passages read [2].

**R5: not built, budgeted path built.** `pnk ask --deep` decomposes a hard question, searches each part and answers from the merged evidence; the free retrieval is round 0 and its confidence picks the branch [1]. It is priced and refused before the first call against all three `[budget]` windows [1]. Triple extraction written to sidecars does not exist; the nearest feature prints suggested `links[]` entries (`rel: co-cited`, `origin: deep`) and never writes them [1].

**R6: built, with one departure.** `pinakes_links` takes `doc_id`, `kb?`, `rel?`, `direction?`, `depth?` (server-capped at 3) and `query?`, and returns neighbours, a `frontier`, `unresolved` and `truncated`. Its `confidence` is "always `unknown`", not the `pinakes_search` signal the recommendation named [4]. DESIGN says the derived structural edges are read only by the expansion channel, while `pinakes_links` serves the authored link graph [5]. The July approach admits that the `--deep` loop is orchestration the free path does not have and amends DESIGN's wording [8]; DESIGN keeps it CLI-only [5].

**R7: built, used.** 0.7.0 grew the demo KB's golden set from 41 to 74 questions, with 20 `simple-lookup` controls and 13 single-KB multi-hop questions [1]. The demo KB could not carry the gate: 1 of 18 multi-hop questions failed where 7 were needed [2]. On the RFC corpus 12 failed and 9 were reachable [1]. A second golden set of 110 blind-authored questions, frozen 20260806 11:56 and released in 0.16.0, was used once, for the metadata experiment: 6 improved, 6 regressed, 84 unchanged over 96 answerable questions, so `[chunking] metadata` ships `off` [1].

## The in-house precedent: ClaudeKB

ClaudeKB is the author's earlier project: "A blueprint for a fleet of self-sufficient, docs-as-code knowledge bases" written and maintained primarily by AI agents [11]. It is public, MIT-licensed (from its `LICENSE` file), at v0.4.0 published 20260712 17:20 UTC, with no commit after 20260712 [10][13][15]. The repository now lives under a separate organisation account; the old address redirects [10]. Its README still says "v0.1.1" as status while the latest release is v0.4.0 [11][13].

Its roadmap lists a unified cross-KB search and an "MCP / RAG retrieval layer" under "Future extensions (designed for, not built)" [12]. The July investigation concluded that Pinakes could be that layer [14]. Neither side has tested it: ClaudeKB built no retrieval layer, and Pinakes has no `pnk adopt` (its docs call it unimplemented, owning release unanswered) [7]. STATUS, ROADMAP and DESIGN do not mention ClaudeKB [1][2][5].

What carried over is the generic lessons, not the path. Authored links are sparse: on the RFC corpus 53.3% of documents (160 of 300) carry one, the median out-degree is 1 and the worst is 86 [1]. Shared-value edges over popular values make noise cliques, which hub reporting now surfaces [1]. Link authoring through a tool shipped as `pnk link`, in a different shape [1].

## Reading

*Reading:* the approach holds where it is free and measured, and is unproven where it ranks. Authored links, the typed link tool and the budget machinery are built and cost nothing at search. The one ranking channel Pinakes built did not pass its gate on one corpus, and the corpus bound is real: no heading paths, two of four gate clauses unable to fire. Whether authored links beat extracted ones is untested, since no source read evaluates them [9]. What would change this reading is the later re-run on a corpus with sections.

## Left unstated

- What the `[ner]` extra would use if built.
- Whether the three-leg re-run on a corpus with sections has run, and the size of the `expand-in-degree` lift.
- Whether the EUR figures for `--deep` (EUR 0.2627 and EUR 1.6872) still hold. STATUS gives them without a date or a rate, and `usd_per_eur` was re-stamped in 0.32.7 (1.1622 to 1.1253), 0.32.8 (to 1.113) and 0.32.9 (to 1.1172); STATUS puts the three moves at about 3.3% higher, 1.1% higher and 0.4% lower for the same USD cost [1][2]. The rate the two figures were computed at is unstated.
- Whether Pinakes reads Markdown links in document bodies as edges.
- Whether any ClaudeKB-templated KB was indexed by hand.

## Sources

1. https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md : latest release, build state of every part, the gate table, 0.7.0, 0.11.0 to 0.13.0, 0.16.0, 0.23.0 to 0.26.0 rows, prices and caps, 53.3% link share (read 20261102 19:37 UTC; the `reachable ≠ retrievable` line, the 0.32.7 to 0.32.9 price-table rows and the 0.32.9 row re-read 20261102 20:12 UTC)
2. https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md : the graph release staged, the re-run record, the demo-KB gate figure, the 0.32.9 release record including `usd_per_eur` 1.113 to 1.1172 (read 20261102 19:37 UTC; the 0.32.9 passages re-read 20261102 20:12 UTC)
3. https://github.com/lucagattoni/pinakes/blob/main/docs/MANIFEST.md : `graph_channel` values, third fusion input, `"ppr"` not accepted (read 20261102 19:38 UTC)
4. https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md : `pinakes_links` arguments, depth cap 3, `confidence` always `unknown` (read 20261102 19:39 UTC)
5. https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md : section 4.3 (composable tools, `--deep` CLI-only and test-enforced), derived edges read only by the expansion channel (read 20261102 19:37 UTC)
6. https://github.com/lucagattoni/pinakes/commits/main : GitHub commits API: head of `main` is d2f0d53, committed 20261102 15:29 UTC (read 20261102 19:38 UTC)
7. https://github.com/lucagattoni/pinakes/blob/main/docs/README.md : `pnk adopt` unimplemented, owning release unanswered (read 20261102 19:38 UTC)
8. `pinakes/approach/PINAKES_APPROACH.md` (repository path; the maintained copy of the July 2026 decision record, the copy in the Pinakes repository being historical) : the three layers, the lazy, agent-driven and budget-tunable wording, and the status block (the record's own Pinakes sources were read 20261030 18:58 to 19:03 UTC and 20261102 10:00 to 10:02 UTC, via the archive page `pinakes/approach/PINAKES_APPROACH.md`; the layer design is this record's own and the record is its primary source; page itself opened 20261102 19:37 UTC)
9. `pinakes/recommendations-r1-r7.md` (repository path; the July 2026 review, original date 20260725 15:12 UTC, a file modification time) : R1 to R7 wording and its annotations (the annotations rest on Pinakes STATUS, ROADMAP, CLI and DESIGN read 20261030 18:58 to 19:00 UTC, via the archive page `pinakes/recommendations-r1-r7.md`; page itself opened 20261102 19:37 UTC)
10. https://github.com/lucagattoni-kb/ClaudeKB : GitHub repository API: public, licence `MIT`, last push 20260712 17:20 UTC, no commits since 20260801 (0 returned), head `1f5694e` (read 20261102 19:38 UTC)
11. https://github.com/lucagattoni-kb/ClaudeKB/blob/main/README.md : one-line description; status line "v0.1.1" (read 20261102 19:40 UTC)
12. https://github.com/lucagattoni-kb/ClaudeKB/blob/main/docs/guide/roadmap.md : "Future extensions (designed for, not built)" (read 20261102 19:40 UTC)
13. https://github.com/lucagattoni-kb/ClaudeKB/releases : latest release v0.4.0, published 20260712 17:20 UTC (read 20261102 19:42 UTC)
14. `pinakes/precedent/claudekb.md` (repository path; the owner's July 2026 investigation) : the conclusion that Pinakes could serve as the deferred retrieval layer (investigated 20260725 15:31 and 20260726 08:52 local time as written then, the ClaudeKB repository read then; ClaudeKB and Pinakes sides re-checked 20261030 18:58 to 19:04 UTC, via the archive page `pinakes/precedent/claudekb.md`; page itself opened 20261102 19:40 UTC)
15. https://raw.githubusercontent.com/lucagattoni-kb/ClaudeKB/main/LICENSE : the `LICENSE` file starts "MIT License", "Copyright (c) 2026" (read 20261102 20:11 UTC)
