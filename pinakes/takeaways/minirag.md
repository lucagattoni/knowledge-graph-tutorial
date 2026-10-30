---
slug: minirag
neutral-entry: ../../kb-kg/projects/minirag.md
investigated: 20260726
updated: 20261030 19:08 UTC
licence-gate: open
---

# MiniRAG: what Pinakes takes from it

The facts about the project itself are in its [neutral entry](../../kb-kg/projects/minirag.md). This page
holds only the Pinakes-specific reading. Source numbers like [n] refer to the neutral entry's source list.

## Verdict

Evidence on file, framework declined: MiniRAG shows that a 1.5 to 4B local model can build a usable entity
layer, but nothing from it was built, and the one idea worth keeping (entity-mention edges feeding a
personalised-PageRank channel) stays an unscheduled, eval-gated option.

## What Pinakes takes

| Idea | Why it was kept on file | Pinakes design it would feed |
|---|---|---|
| **Entity mentions as edges into the existing PPR channel**, not a new retrieval pipeline. A small local model (1.5 to 4B) extracts names and types only at sync, giving an entities table, entity-chunk mention edges and entity-entity co-occurrence edges that join the same RRF/PPR fusion. | July's reading: the unique contribution of an entity layer is **cross-document edges** (the same person or project in unrelated files), whereas the structural edges Pinakes derives (over document, chunk, tag, heading and directory nodes) connect things that are already near each other (same document, directory or tag). The paper's case study (restaurant query, ACL appendix A.2) is a multi-constraint personal query of exactly that kind [12]. | The graph approach's optional entity layer (the `[ner]` extra), see [`../approach/`](../approach/). |
| **Extraction cache keyed by chunk hash.** | MiniRAG's LLM response cache means a rebuild repeats no calls for unchanged input (cache lookup not re-read, see neutral entry) [6]. It is what would make "rebuilds stay free" true with a model in the sync path: only new or changed chunks pay. | Sync and rebuild rules. Applies only if model-based extraction ever enters sync. |
| **Name-only embedding index** (`entity_name_vdb`). | Embedding bare entity names apart from descriptions is what makes query-to-node grounding robust with weak embedders [6]. It maps onto an entity-name vector table using the embedding model Pinakes already ships. | Seed matching for the PPR channel. |
| **Delimiter-tuple output over JSON** for small-model extraction; a JSON-repair step where JSON is unavoidable. | MiniRAG's parsing is pattern matching and tolerates sloppy output [6]. | Extractor output format, if an extractor is built. |
| **Chunks stay first-class retrieval targets.** The graph only re-ranks and expands chunks. | It is MiniRAG's largest ablation effect: removing chunk nodes costs 4.4 to 7.8 points in the arXiv table and 2.8 to 6.6 in the ACL table [10][12]. Pinakes already works this way. | Retrieval architecture; no change. |
| **LiHua-World as the closest public benchmark to the Pinakes workload.** July's characterisation: personal, conversational, entity-dense, temporally scattered. The dataset README confirms chronological chat records with manually annotated answers and supporting documents [8]. | Kept as a candidate corpus, not a plan. | Benchmark choice, see [`../../DECISIONS.md`](../../DECISIONS.md) (D-15). |

How strong the evidence for the first row is, after the October 2026 re-check:

- On LiHua-World the 1.5B GLM-Edge model builds and queries an index that scores 52.51 (arXiv table) or
  51.65 (ACL table), against 42.79 or 42.39 for the chunk-only baseline: +9.7 and +9.3 points [10][12]. The
  gain over the chunk-only baseline across the four small models is +5.0 to +12.1 (arXiv) and +5.8 to +9.7
  (ACL), not the "+9 to +13" the July note gave.
- The paper's one-model-does-everything setup means that gain is for a small model that both indexes and
  answers. A small local indexer paired with Claude as the reader, which is the Pinakes case, is
  **unstated** in the paper.
- The `-I` ablation does not say what the July note took from it. `-I` replaces the whole
  heterogeneous-graph indexing with a LightRAG/GraphRAG-style description-driven design and roughly halves
  accuracy [10][12]. The paper does not say how it was built, and MiniRAG's shipped code still extracts
  descriptions [6]. So "extraction without descriptions is better with small models" is **not** shown. "Small
  models fail at LightRAG-style indexing" is.

## What Pinakes leaves

| Left | Why |
|---|---|
| **The bespoke path-scoring stack** (`edge_vote_path`, `path2chunk`, `kwd2chunk`). | Ad-hoc counting with hard-coded constants (x2 for a first path, x10 when a path's first chunk is a dense hit, a 20% short-path rescue) and Levenshtein matching of descriptions; no principled damping [6]. A real PPR channel on the same graph is simpler and more general. |
| **A query-time LLM call in the free path.** | `minirag_query2kwd` needs one model call per query [6]. Query-to-entity grounding in Pinakes can be an embedding match against a name index. Answer-type prediction is a nice-to-have for the paid `--deep` path, not the free one. |
| **Relationship extraction with descriptions, keywords and strength.** | It is the code's LightRAG inheritance and sits against the paper's own thesis [6][10]. Co-occurrence edges suffice. |
| **Adopting the framework itself.** | Quiet since 20251016 [1][3]; JSON, NetworkX and nano-vectordb storage against Pinakes' single SQLite file; and its answering-side wins matter little when a strong model is the reader. After the ACL re-check, a further reason: with a strong model MiniRAG is overtaken by HippoRAG v2, LightRAG and RAPTOR on LiHua-World (52.28 against 66.28, 55.89 and 52.62) [12]. |
| **Mandatory model extraction in sync.** | It would break the free path if unconditional. It would have to be an optional mode, off by default, with the structural-edges-plus-PPR baseline as the evaluation control, adopted only if golden-set recall@k and MRR beat that baseline. |

## Where it landed in Pinakes

Read from Pinakes [`STATUS.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md) and
[`ROADMAP.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md) on 20261030 19:00 UTC.
STATUS lists 0.32.8 as the latest published version. **Nothing from MiniRAG was built.** The only mention
of MiniRAG in either file is in the 0.1.1 entry of ROADMAP, which lists it among the projects researched.
Neither file nor `DESIGN.md` mentions LiHua-World (searched 20261030).

| Idea | State | Evidence |
|---|---|---|
| Entity layer and entity-mention edges (the `[ner]` extra) | **Not built.** Staged: "gates only, not scheduled", and "there is deliberately no implementation plan". Its gate is not run. | [ROADMAP, "The graph release, staged"](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#the-graph-release-staged--gates-only-not-scheduled); [STATUS, release table row "the graph release, staged"](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md) |
| PPR channel (the consumer MiniRAG's edges would feed) | **Not built.** Staged on the same terms. `graph_channel` refuses the value `"ppr"`, because a setting for a mode the code does not implement would silently do nothing. | [ROADMAP, same section](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#the-graph-release-staged--gates-only-not-scheduled); [ROADMAP, 0.20.1](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#0201--a-tier-that-is-not-built-stops-being-accepted--20260808-0641) |
| Local-model entity extraction at sync | **Not built, not planned** in STATUS or ROADMAP. The paid-path allowlist has two entries, neither of them entity extraction. | [INVARIANTS.md](https://github.com/lucagattoni/pinakes/blob/main/docs/INVARIANTS.md) (free path stays free) |
| Name-only entity index, delimiter-tuple extractor | **Not built**, as they depend on the entity layer. | same |
| Structural graph and expansion channel (what exists instead) | **Built in 0.11.0** (the graph release): a `nodes`/`edges` table over chunk, document, tag, heading and directory nodes. The expansion channel `[retrieval] graph_channel` ships **off**: on the RFC realism corpus it improved 0 multi-hop questions and regressed 3 (p = 1.0000). The roadmap states that this result licenses neither PPR nor the `[ner]` extra. | [STATUS, 0.11.0 row](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md#did-the-expansion-channel-earn-its-default--no-measured-20260804-2252); [ROADMAP, "What would change it"](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md) |
| Extraction cache | **Built in 0.2.0 (I4), for a different purpose.** It caches the text a *document extractor* returns, one file per `<content_hash>-<fingerprint>` under `.pinakes/cache/extract/`, so a PDF is not re-extracted and `--rebuild` is free. It does not cache entity extraction, which does not exist. | [STATUS, extraction cache row](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md); [DESIGN.md](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md) |
| Chunks stay first-class | **Consistent with what was built.** Chunk is one node kind of the graph, and the only graph channel is off by default, so default retrieval is unchanged by the graph. | [STATUS, 0.11.0 row](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md) |

## Licence gate

**Open.** The `LICENSE` file is MIT (read 20261030 18:58 UTC) and the README carries no conflicting
badge [4][5]. Pinakes is Apache-2.0, and MIT is compatible with it provided the copyright notice is kept
on any copied code. Nothing here proposes copying code: the ideas above are free to reuse, and no source
was taken.

## Changed since July 2026

Checked 20261030 18:58 to 19:08 UTC. Details and numbers are in the neutral entry's changes section.

- **Repository: no change that touches the verdict.** Still MIT, not archived, no push since 20251016, no
  commit since 20260801, latest release still `v0.0.2` [1][2][3][4]. "Quiet since 2025-10" in the reasons
  above is now 379 days old.
- **The ACL 2026 camera-ready changed the evidence, not the verdict.** On LiHua-World with `gpt-4o-mini`,
  HippoRAG v2, whose retrieval is built on personalised PageRank, scores 66.28 against MiniRAG's 52.28.
  With the small models it scores 33.92 to 36.77, below the chunk-only baseline in every row, while MiniRAG
  reaches 46.78 to 51.65 [12]. In that paper one model does everything, so this says nothing yet about a
  PPR channel over a graph built by a small model and read by a strong one.
- **Three July premises were wrong or stale and are corrected above:**
  1. "With a strong reader the gap over NaiveRAG shrinks (54.1 vs 46.6)." Not supported: the gap over the
     chunk-only baseline on LiHua-World with `gpt-4o-mini` is +7.5 (arXiv) or +9.7 (ACL), inside the range
     for the small models. What a strong model changes is MiniRAG's rank against other graph methods.
  2. "The `-I` ablation is the licence for names-only extraction." It does not isolate descriptions.
  3. The cost figures: 2 model calls per chunk by default, not 2 to 3, and query latency close to
     LightRAG's, not "cheap".
- **No new work is triggered.** The first row of "What Pinakes takes" stays gated, as the roadmap says
  for the whole staged graph release. An experiment that would test the open question (small local
  indexer, strong reader, public data with ground-truth evidence) belongs in
  [`../experiments/`](../experiments/) and needs the owner's explicit yes first (D-14).
