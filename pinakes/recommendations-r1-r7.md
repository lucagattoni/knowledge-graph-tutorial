# Pinakes: the seven graph recommendations (R1 to R7)

**Status:** the Pinakes-specific half of a July 2026 literature review, kept as written and annotated ·
**Original date:** 20260725 15:12 UTC (file modification time) · **Annotated:** 20261030 19:00 UTC

The field-neutral half (the question, what the research found, the prior-art list) is in
[`kb-kg/literature/graph-rag-research.md`](../kb-kg/literature/graph-rag-research.md). This file holds
what that review concluded for [Pinakes](https://github.com/lucagattoni/pinakes): where it already
stood (section 3), the seven recommendations (section 4) and the summary (section 6).

**How this file is built.** The original wording of section 3, each recommendation and the summary is
kept unchanged and is not edited to match later events. After each recommendation two annotation lines
are added:

- **Status today**: what Pinakes has built, from its own status and roadmap documents. One of: built
  (release named), built and off by default, gated (not built), not built.
- **Evidence since July**: only where a source read on 20261030 bears on the recommendation. The
  papers are described in the
  [evidence section of the neutral file](../kb-kg/literature/graph-rag-research.md#3-evidence-since-july-2026);
  bracketed numbers like [n] are that file's source numbers.

**Version numbers in the original text** (v0.3, v0.4) follow the convention in use in July. Pinakes
now names unbuilt work instead of numbering it. The authoritative statement of what is built is
[`STATUS.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md); where this file
disagrees with it, STATUS.md wins.

**Pinakes sources**, read 20261030, 18:58 to 19:00 UTC, from a checkout of the `main` branch:
[P1] [`docs/STATUS.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md), stamped
"Latest release: 0.32.8 · last reviewed 20261029 18:57"; [P2]
[`docs/ROADMAP.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md); [P3]
[`docs/CLI.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md); [P4]
[`docs/DESIGN.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md). Where the passages
read do not say, this file writes **unstated**.

Related projects: [LinearRAG](../kb-kg/projects/linearrag.md) (the structural position behind R3),
[HippoRAG](../kb-kg/projects/hipporag.md) (the mechanism behind R4),
[Graph-R1](../kb-kg/projects/graph-r1.md) (the direction behind R6).

---

## 3. Where Pinakes already stands

Worth stating plainly, because it changes what is left to build:

- **The sidecars are already a knowledge graph.** `links: [{to: pnk://…, rel: cites}]` is a typed,
  directed edge, authored by a human, committed to git, portable across machines, and free. It is
  higher-precision than anything an LLM extractor produces, and it never needs recomputing.
- **The `links` table is already the storage layer**, with `src_kb_id`, `rel` and `origin` — enough
  to distinguish inbound from outbound and authored from discovered.
- **RRF over BM25 + vector (§4.1) is the fusion pattern the 2025/26 systems converged on.** Adding a
  graph channel means adding a third ranked list to a fusion that already exists — not a new pipeline.
- **DESIGN §4.3 already made the agentic call**: multi-hop via composable tools driven by the
  caller's agent, not an agent framework inside Pinakes. That is the Graph-R1 loop, executed on
  someone else's token budget. It is the correct architecture and it should not be revisited.

**So the recommendation is not "adopt GraphRAG."** It is: recognise that the cheap 80% of a graph is
already in the design, and spend the remaining effort on traversal and ranking rather than on
extraction.

> **Status today.** Only one bullet could be checked against the documents read: the `origin` field is
> in use, since `pnk ask --deep` prints suggested `links[]` entries with `rel: co-cited` and
> `origin: deep` (STATUS.md, 0.26.0) [P1]. The other bullets, including the claims about the `links`
> table columns, the fusion in §4.1 and §4.3, were not re-read in this run: **unstated**.
> **Evidence since July.** The claim that a similar pipeline "converged" on RRF over BM25 and vector
> is not tested by any source read. On the "authored links are higher precision" claim: none of the
> papers read evaluates human-authored links.

---

## 4. Recommendations

### R1 — Do not add LLM entity/relation extraction to `pnk sync`. Ever, at any version.

The strongest, most load-bearing recommendation here. It breaks the free path, makes `--rebuild`
expensive, and the 2025/26 literature says it buys less than it costs. If entity extraction is ever
wanted, see R5 — but the default answer is no.

> **Status today: held, nothing built.** STATUS.md lists two paid entry points, the `claude-vision`
> document extractor and `pnk ask --deep`; neither is entity or relation extraction at sync [P1]. An
> optional `[ner]` extra is staged, "eval-gated, never scheduled"; whether it would use an LLM is
> **unstated** in the passages read [P1][P2].
> **Evidence since July.** Mixed on the "buys less than it costs" clause, silent on the free-path
> clause. In one 120-question study, replacing LLM extraction with non-LLM noun-phrase extraction cut
> cost from $0.408 to $0.226, and the LLM-extraction system still won 44 questions to 26 with 50 splits
> [10]. A zero-LLM graph beat HippoRAG 2 on average F1 (66.49 against 64.49) but still used an LLM to
> pick seed documents at query time [13]. LightRAG-style extraction scored below naive RAG in two
> studies [13][9]. So the quality side of the clause is not uniform; the cost side is supported.

### R2 — Prioritise v0.3 (`pnk link`, `pinakes_links`, cross-KB traversal).

Currently scheduled fourth. On this analysis it is the highest-value graph work in the whole roadmap,
because it is the only graph capability that costs nothing to build and delivers what vector search
structurally cannot. The prerequisite stated in §8 — "needs two populated KBs to be worth anything" —
is real, so this is an argument for getting two KBs populated sooner, not for reordering blindly.

> **Status today: built, 0.5.0 and 0.6.0.** 0.5.0 shipped `pnk links` and the `pinakes_links` tool plus
> reverse scanning of partner KBs; 0.6.0 shipped `pnk link` (writes one `links[]` entry into the source
> document's sidecar) and `pnk doctor` link coverage. The ROADMAP calls these two cuts "the links
> release" [P1][P2].
> **Evidence since July.** None of the sources read bears on it.

### R3 — Add a free structural graph channel at sync time.

Everything below is already in the index or derivable from it at zero LLM cost:

| Edge type | Source | Cost |
|---|---|---|
| `sibling` | adjacent `chunks.ordinal` within a doc | free |
| `parent`/`child` | `chunks.heading_path` hierarchy | free |
| `co-located` | shared directory in `documents.path` | free |
| `shared-tag` | sidecar `tags` overlap | free |
| `cites`/`supersedes`/… | sidecar `links` (authored) | free |

This is the LinearRAG / structural-GraphRAG position: relation-free graph construction, where topology
comes from document structure rather than from semantic extraction. It costs one pass over data sync
already touches.

> **Status today: built, 0.11.0 ("the graph release"); the channel that reads it is off by default.**
> The release is breaking (`schema_version` 3, forcing a full rebuild). It derives a `nodes`/`edges`
> structure over chunk, document, tag, heading and directory nodes, with edge kinds named in the
> ROADMAP as sibling, parent/child, in-section, co-located and shared-tag; `pnk doctor` reports hubs
> and, since 0.12.0, heading coverage [P1][P2]. On the 300-RFC corpus it produced 107,411 edges over
> 106,806 chunks at 1.02 times the query latency. `sibling` was 99.2% of the edges and changed no
> outcome. No chunk in that corpus carried a heading path, so `in-section`, `parent` and `child`
> derived zero edges; an opt-in `[chunking] headings = "numbered"` setting arrived in 0.13.0 [P2].
> **Evidence since July.** Indirect only. The structures in the papers read are built from vector
> geometry [13] or entity extraction [10], not from document layout, so they do not test this
> design. A zero-LLM document graph did beat naive retrieval, with an LLM choosing the seeds [13].

### R4 — Rank with Personalized PageRank over that graph, as a third RRF channel.

This is HippoRAG 2's core mechanism and the highest value-per-line item on the list. Concretely:

1. Run the existing pipeline; take the fused top-*k* chunks as seed nodes.
2. Run PPR over the edge set from R3, seeded on those nodes.
3. Feed the PPR-ranked list into the *existing* RRF as a third input, alongside BM25 and vector.
4. Rerank as today.

Properties that make it fit: it is pure NumPy/scipy over an adjacency matrix the index already holds,
adds no dependency, no network, no LLM, and no new storage — and it degrades to today's behaviour
when the graph is sparse. It also inherits the §4.4 coherence story unchanged, because nothing about
it is model-specific.

Gate it behind `[retrieval] graph_channel = "off" | "ppr"`, default `off` until the golden set says
otherwise (R7).

> **Status today: gated, PPR not built; a different channel was built and ships off.** What shipped in
> 0.11.0 is an "expansion channel" behind `[retrieval] graph_channel`, default `off`. Its gate ran
> 20260804 22:52 on the 300-RFC corpus: 0 multi-hop questions improved and 3 regressed (p = 1.0000).
> The ROADMAP's own summary is "reachable is not retrievable": a reachability probe called 9 failing
> questions liftable and the retrieval instrument lifted none. The setting refuses the value `"ppr"`
> because that mode is not implemented. PPR and the `[ner]` extra are filed under "the graph release,
> staged": gates only, no implementation plan "by design", not scheduled, and PPR's gate "does not run
> at all on a corpus below the heading-coverage floor" [P1][P2]. The ROADMAP records a re-run on a
> corpus with sections as taken and to be run later, with a null result expected; whether it has run is
> **unstated** in the text read. Whether the shipped channel enters rank fusion as a third list is
> **unstated** in the passages read.
> **Evidence since July.** Supports the mechanism, not Pinakes' graph. HippoRAG 2 (PageRank-based)
> led on single-fact and multi-hop questions in two studies: MuSiQue 54.4 against 36.6 for naive RAG
> with terse prompts [9]; average F1 64.49 against 60.62 [13]. PageRank run on a different, zero-LLM
> graph averaged 65.65 [13]. Offline graph-modified embeddings used as a guide inside a multi-stage
> retriever raised evidence recovery from 51.0% to 60.8%, but replacing the original embeddings
> lowered it [12]. Caveats: all on short-passage or synthetic question sets, none on layout-derived
> edges, and [12] comes from a graph-product vendor. These results do not contradict Pinakes' null
> result, which concerns a different channel on a different corpus.

### R5 — If entity extraction is ever added, make it lazy, agent-driven, and write-back to sidecars.

The SubQRAG pattern, adapted to Pinakes' truth/derived split:

- Never at sync. Only on an explicit, budgeted `--deep` path (v0.4 machinery, already specified).
- Only for the specific gap the current query hit — not the corpus, not the document set.
- **Write discovered triples into the sidecar, not into `.pinakes/`.** They then become committed,
  diffable, human-reviewable, and free forever after — which is exactly the property the design's
  "anything another KB needs to see must live in committed files" rule already demands.

That last point turns a recurring inference cost into a one-time, human-auditable one. It is the only
form of LLM extraction consistent with this design.

> **Status today: not built; the budgeted path it relies on is.** `pnk ask --deep` shipped in 0.24.0,
> worked against the live API from 0.25.1 and was completed in 0.26.0. It decomposes a hard question,
> searches each part and answers from the merged evidence, under spending caps [P1]. It does not
> extract triples. Its nearest feature is E7 (0.26.0): after a run it prints suggested `links[]` entries
> (`rel: co-cited`, `origin: deep`) for the user to review and commit. It never writes them;
> `--write-suggestions` is deferred and "not planned" [P1]. Writing discovered triples to sidecars:
> **not built**.
> **Evidence since July.** Partly relevant to "only for the gap". A salience filter that skipped
> low-value chunks before LLM extraction made a larger corpus 4.2 to 4.5 times cheaper than LightRAG
> and kept the preference over it [10]. In the small 5-document-per-domain setting, extracting fewer
> chunks lowered judged quality every time [10]. Neither tests query-time, gap-driven extraction.
> SubQRAG itself (arXiv 2510.07718) predates July and its abstract gives no numbers [5].

### R6 — Expose the graph to the caller's agent; do not traverse on its behalf.

`pinakes_links(doc_id, rel?, direction?, depth?)` returning neighbours plus the same confidence
signal as `pinakes_search`. The calling agent runs think → traverse → rethink in its own context, on
its own subscription — §4.3's existing bet, extended to edges. Resist adding a traversal *policy*
inside Pinakes; that is the "second, worse agent framework" already flagged in §9.

> **Status today: built, 0.5.0, with one difference from the text.** `pinakes_links` takes `doc_id`,
> `kb?`, `rel?`, `direction?` (`out`, `in`, `both`), `depth?` (capped at 3) and `query?`. It returns
> neighbours, a `frontier`, `unresolved` and `truncated`, and its `confidence` field is "always
> `unknown`", not the `pinakes_search` signal the recommendation named [P3]. DESIGN.md says the derived
> structural edges are read only by the expansion channel, and `pinakes_links` serves the authored link
> graph [P4]. `pnk ask --deep` runs a decompose, search and answer loop inside Pinakes; the passages
> read do not describe link traversal inside that loop [P1].
> **Evidence since July.** Graph-R1, the agent-driven design behind this recommendation, is confirmed
> as accepted at ICML 2026 (main conference) [6]. In the conversation-memory study, adding graph-based
> retrieval expansion to a plain dense-plus-rerank baseline did not improve it [11]; that is evidence
> about expansion inside the retriever, not about exposing edges to an agent.

### R7 — Measure before shipping any of it.

Add a multi-hop and a relational-lookup section to the template golden set *before* R3/R4 land, and
report per-class scores. Given §2.3, the specific risk to watch is regression on simple factual
lookup: if the graph channel costs precision there, it must stay `off` by default or route by query
class. The eval harness already reports false-abstain and false-confidence; this is the same
discipline applied to a new channel.

> **Status today: built, 0.7.0, and used.** 0.7.0 grew the demo KB's golden set from 41 to 74 questions,
> adding 20 `simple-lookup` control questions and 13 single-KB multi-hop ones, with a per-question
> artifact (`eval/outcomes.json`), stable ids and a validated `kind`. That was before the graph
> release (0.11.0), as recommended. The graph release's gate then ran on the 300-RFC corpus, using
> thirteen new multi-hop questions authored from corpus structure and frozen before the probe ran; the
> expansion channel stayed `off` because of that result. The ROADMAP notes the multi-hop class
> failed too rarely on the demo KB for the gate to be reachable (1 of 18 failing against 7 needed),
> while 12 failed on the RFC corpus [P1][P2]. A separate 110-question golden set on another RFC band
> (RFCs 8600 to 8799, 195 documents), frozen 20260806 11:56 and released in 0.16.0, is the instrument
> for later retrieval changes; it was used for the 0.16.0 metadata experiment, not for the graph gate
> [P1].
> **Evidence since July.** Supports per-class reporting. One strategy helped relational questions and
> hurt extremum questions by 0.8, 12.3 and 19.3 points on three families [12]. Answer-prompt format
> alone reversed a ranking between HippoRAG 2 and a consolidation-based system [9]. Cost and quality
> reported together changed which system looked best [10]. A paper that compared two pipelines
> differing in several components credited the graph with a large gain [14]; the confound is a
> caution for how Pinakes attributes a result to one channel.

---

## 6. Summary

| # | Recommendation | Version | Cost |
|---|---|---|---|
| R1 | No LLM extraction in `pnk sync` | all | — |
| R2 | Prioritise authored links (`pnk link`, `pinakes_links`) | v0.3 | €0 |
| R3 | Structural edges from existing index data | v0.3 | €0 |
| R4 | PPR as a third RRF channel, default `off` | v0.3–v0.4 | €0 |
| R5 | Lazy extraction → sidecar write-back, only if ever needed | v0.4+ | budgeted |
| R6 | Expose traversal as a tool; no traversal policy inside Pinakes | v0.3 | €0 |
| R7 | Multi-hop golden-set coverage before R3/R4 ship | v0.3 | €0 |

The short version: **Pinakes does not need GraphRAG, because it already has the part of GraphRAG that
was worth having.** Typed, human-authored, committed links are a better graph than an LLM extractor
produces, and they cost nothing. The work that remains is traversal and ranking over that graph — and
the research consensus of 2025/26 is that this is where the value was all along.

**Status today, at a glance** (Pinakes 0.32.8, STATUS.md reviewed 20261029 18:57 [P1])

| # | State | Release or gate |
|---|---|---|
| R1 | held; nothing built | policy |
| R2 | built | 0.5.0 (`pnk links`, `pinakes_links`), 0.6.0 (`pnk link`) |
| R3 | built; reading channel off by default | 0.11.0; gate run 20260804 22:52 did not pass |
| R4 | gated; PPR not built | staged, not scheduled; no implementation plan by design |
| R5 | not built; budgeted path built | `pnk ask --deep` 0.24.0 to 0.26.0; suggestions printed, never written |
| R6 | built; `confidence` always `unknown` | 0.5.0 |
| R7 | built | 0.7.0 (golden set 41 to 74 questions); later a 110-question golden set (0.16.0) |

The summary paragraph above is the July conclusion, unedited. Two notes on it. Its last sentence says
the value lies in "traversal and ranking over that graph"; the one ranking-side channel Pinakes built
(expansion over derived edges) did not pass its gate on the corpus it was run on, and PPR is not built.
The authored-link half of the conclusion (R2, R6) is built; whether authored links beat extracted ones
is untested here, since no source read evaluates them.
