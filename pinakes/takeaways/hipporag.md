---
slug: hipporag
neutral-entry: ../../kb-kg/projects/hipporag.md
investigated: 20260725
updated: 20261030 19:06 UTC
licence-gate: open
---

# HippoRAG: what Pinakes takes from it

The facts about the project itself are in its [neutral entry](../../kb-kg/projects/hipporag.md). This page
holds only the Pinakes-specific reading. Pinakes-side statements below were read from a local checkout
of the public Pinakes repository at commit `b1bad68` (committed 20261030 08:02 UTC), on 20261030 19:02
UTC; the links point to the same files on GitHub.

## Verdict

HippoRAG 2 is the reference recipe for a PPR graph channel (recommendation R4, see
[`../recommendations-r1-r7.md`](../recommendations-r1-r7.md)). Pinakes has written that recipe down and
gated it but has **not built it**; what Pinakes built instead is a structural graph and an expansion
channel that failed its own gate and ships off.

## What Pinakes takes

The July investigation (20260725) kept these ideas on file. Parameters are HippoRAG's, with the source in
the neutral entry's "PPR mechanism" section.

| Idea | HippoRAG's value | Why it was kept | Feeds |
|---|---|---|---|
| Independent support for the architecture-level bet | graph signal helps multi-hop; keeping the original passages in the walk avoids regressing simple lookups | Pinakes' fused top-k as seeds plus chunk nodes in the graph is the same shape as HippoRAG 2's passage nodes | R4; the approach document in [`../approach/`](../approach/) |
| PPR as the whole query-time graph machinery | no LLM call for the walk itself | consistent with a free path | R4 |
| Damping 0.5, undirected, weighted | 0.5 in both versions; tuned on 100 MuSiQue training examples in v1 | start the sweep there (0.3 to 0.7), not at the textbook 0.85 | R4 |
| Two-part reset vector | at most 5 high-precision non-passage seeds, plus every passage node weighted by score times `passage_node_weight = 0.05` | seeding all chunks, not only the top k, is the authors' route to multi-hop flow | R4; the staged PPR gate |
| Node-specificity damping | divide a seed's weight by the number of passages it links to; about 2 R@5 points in v1 | damp shared-tag and co-located hub nodes | R4 |
| Score averaging for seeds | a node's weight is the mean score of the query-matched items it appears in | not max, not sum | R4 |
| Empty seed set skips the graph | the dense ranking is returned when the filter yields zero triples | the graph can only abstain; make the path silent and free | R4 |
| Structure may substitute for LLM relations | synonym and context edges are embedding-only or mechanical | Pinakes' structural edges (sibling, parent and child, co-located, shared tag, authored links) could stand in for relation edges; tags and headings play the phrase-node role | R4; the graph release |

Two July design stances that stay on file: PPR enters Pinakes as a **third fusion channel** rather than as
the final ranker (safer for the abstention signal), and "PPR as final ranker" is a cheap variant to test
because it is the same computation. The July implementation note (a power iteration on the row-normalised
adjacency, converging in about 20 to 40 iterations at d = 0.5, no igraph dependency) was a plan, not a
measurement, and has not been run.

## What Pinakes leaves

Recorded in July; not re-checked against Pinakes' current retrieval stack.

| Left | Reason recorded in July |
|---|---|
| LLM OpenIE at index time | about 1,000 LLM tokens per passage, which breaks the free path and free rebuilds. The REBEL ablation (cheap extraction scored 58.4 against 72.9 for the full configuration) was read as support for skipping triples entirely rather than approximating them badly |
| The recognition-memory filter | a query-time LLM call; its job (precision-filtering the seeds) is done in Pinakes by cross-encoder rerank scores. The July notes called it HippoRAG's top error source even with an LLM; the paper's wording is that triple filtering and graph search are "the two main sources of errors" |
| The fact (triple) embedding store | its biggest memory cost, irrelevant without triples |
| Expecting graph gains on simple lookups | even with a 70B-class LLM at index time, HippoRAG 2 only roughly ties strong dense baselines on NQ and PopQA; R4's default-off-until-evaluated stance matches that |

## Where it landed in Pinakes

Sources: [`docs/STATUS.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md),
[`docs/ROADMAP.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md),
[`docs/DESIGN.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md) and the plan
[`plans/20260804_1016-staged-channel-gates.md`](https://github.com/lucagattoni/pinakes/blob/main/plans/20260804_1016-staged-channel-gates.md).
I searched STATUS, ROADMAP and DESIGN for "HippoRAG", "PPR", "pagerank" and "R4".

| Idea or component | State | Evidence |
|---|---|---|
| **PPR graph channel** (the idea HippoRAG contributed) | **Not built.** Listed as "the graph release, staged": eval-gated, never scheduled, with deliberately no implementation plan. The `[retrieval] graph_channel` setting refuses the value `"ppr"` ("a setting the code does not implement is not a setting") | [STATUS, release roadmap](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md#release-roadmap); [ROADMAP, the graph release, staged](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#the-graph-release-staged--gates-only-not-scheduled); [DESIGN](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md) (the `vector_tier` passage that cites the `"ppr"` rule) |
| The `[ner]` extra (entity nodes, the closest analogue of HippoRAG's phrase nodes) | **Not built**; staged and eval-gated together with PPR | same |
| Structural graph: `nodes` and `edges` tables with hub nodes for tags, directories and headings | **Built, release 0.11.0** (`schema_version` 3). Hub spoke weights are `1/section-size`, `1/dir-size` and `1/tag-degree`, so hub size damps flow. This resembles HippoRAG's node-specificity damping; the sources read do not say it was taken from HippoRAG (**unstated**) | [DESIGN, the edge table](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md); [STATUS, 0.11.0](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md#release-roadmap) |
| Expansion channel (`[retrieval] graph_channel = "expand"`) | **Built in 0.11.0 and ships `off`.** Its gate, run on the RFC realism corpus on 20260804, found 0 multi-hop questions improved and 3 regressed (4 of 20 against 7 of 20 with the channel off), sign-test p = 1.0000. It is a different mechanism from PPR, so the result does not test HippoRAG's recipe | [STATUS, "Did the expansion channel earn its default? no"](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md#did-the-expansion-channel-earn-its-default--no-measured-20260804-2252) |
| Damping 0.5, `passage_node_weight` 0.05, all-chunk seeding, seed averaging, fallback | **Not built**, because the channel they parameterise is not built. They are recorded in the approach document and quoted in the gates plan | gates plan, sections on the personalization vector |
| LLM OpenIE and the recognition-memory filter | **Not built**, as decided in July | this page |

What the Pinakes records say about PPR's gate, in their own terms:

- The gate "does not run at all on a corpus below the heading-coverage floor" (decided 20260804): the
  recipe's non-passage seeds come from tags and headings, and the RFC realism corpus had **0 of 106,806
  chunks** carrying a heading path when measured. The plan's proposed floors are at least 50% of chunks
  with a heading path and no single tag on more than 20% of documents (proposals, marked as such in the
  plan; the RFC corpus passes the tag floor at 11%).
- Release 0.13.0 added an opt-in `[chunking] headings = "numbered"` setting so plain text can carry a
  heading path, but the published RFC corpus's manifest does not set it (STATUS, 0.12.0 and 0.13.0 rows).
- A second leg is conditional: under a future `sqlite-vec` tier only the vector scan's top-N carry cosine
  scores. The plan quotes the July approach document as calling that "precisely the top-k-only seeding
  HippoRAG 2 warns against", so a PPR gate passed on the NumPy tier would not license PPR there. That tier
  is itself not built.
- The expansion-channel finding "reachable is not retrievable" (9 failing questions reachable within two
  hops, none lifted) is recorded in the ROADMAP as a result that "licenses neither PPR nor the `[ner]`
  extra".

## Licence gate

**Open.** The `LICENSE` file is MIT (`Copyright (c) 2025 OSU Natural Language Processing`), and the API
field and package manifests agree ([neutral entry](../../kb-kg/projects/hipporag.md), sources 1, 2, 12 and
13, read 20261030 18:58 to 19:01 UTC). MIT allows copying with the notice preserved. Ideas and measured
results are free to reuse in any case. A case-insensitive text search of the Pinakes repository
(Markdown, TOML and Python files, excluding the July research folder and the built site; 20261030 19:02
UTC) found "HippoRAG" only in `CHANGELOG.md`, `docs/ROADMAP.md` and two files under `plans/`, so no
HippoRAG source code appears to be in Pinakes.

## Changed since July 2026

Checked 20261030 19:06 UTC. Project changes are in the neutral entry's "Changed since the July 2026
investigation"; only what bears on the Pinakes reading is repeated here.

- **The verdict is not changed.** The retrieval algorithm, and every parameter the July takes rely on, is
  identical at the July baseline and now (damping 0.5, `passage_node_weight` 0.05, `linking_top_k` 5,
  undirected graph, prpack PPR, dense fallback). No successor paper or project was found, and the
  repository is active, MIT, not archived.
- **Corrections to the July reading, in order of how much they matter for an implementation:**
  1. **The passage seed is not the raw dense score times 0.05.** HippoRAG min-max normalises the dense
     scores per query to [0, 1] first (all ones when every score is equal), then multiplies by 0.05. The
     July recipe, "all chunk nodes weighted by `fused_score x passage_node_weight`", must therefore
     normalise the fused scores the same way. Fused reciprocal-rank scores are not cosines and sit on a
     much smaller scale, so skipping this changes the balance between the two seed groups. This is an
     inference about Pinakes' scores, not a measurement.
  2. **"Cliff above 0.3" was an overstatement.** The paper's sweep (Table 5) falls gradually: MuSiQue
     79.9 / 80.5 / 79.8 / 78.4 / 77.9 and NQ 75.6 / 76.9 / 76.9 / 76.7 / 76.4 at 0.01 / 0.05 / 0.1 / 0.3 /
     0.5. The total spread is 2.6 points on MuSiQue and 1.3 on NQ. A sweep of 0.01 to 0.1 is still
     reasonable; there is no evidence of a cliff.
  3. **"igraph PPR on a graph of about 1.4M edges runs in well under a second" has no source.** The paper
     reports 1.2 s total query time (including one LLM filter call) against 0.3 s for dense retrieval, on
     four H100 GPUs for the LLM; the PPR share alone is **unstated**. Do not rely on a sub-second PPR
     figure for a latency budget.
  4. **Llama-3.1-8B is not "nearly on par".** It scores 67.8 against 72.9 for the full configuration; the
     70B model scores 72.5. The July argument that "local OpenIE works" holds for 70B, and costs about 5
     points at 8B. It does not change the decision to skip LLM triples.
  5. **The "18% of errors" fallback figure** is 18% of 100 analysed failing samples, not of all queries,
     so it is a weak basis for saying the fallback path is common in general.
  6. **Damping convention.** The v1 paper describes 0.5 as a restart probability. At exactly 0.5 the two
     conventions coincide, but a sweep away from 0.5 should check which convention the chosen solver
     uses (not verified here for igraph or for a hand-written power iteration).
- **A reason to read HippoRAG's code with care if it is ever consulted:** at the July baseline its
  recognition-memory filter parsed LLM output with `eval()`; this was fixed on 20260728. No Pinakes change
  follows from it, since no HippoRAG code is used.
- **Possible new use, not decided:** HippoRAG now ships an MCP server and a Claude Code plugin that expose
  `retrieve`, `rag_qa`, `index`, `delete` and `index_stats`, with the retrieval tool making no LLM call.
  That makes it a candidate comparison target for a future benchmark of agent-facing retrieval; nothing
  in the Pinakes records read here mentions it (**unstated**).
- **Pinakes side, since July:** release 0.11.0 shipped the structural graph and the expansion channel
  (off); 0.12.0 and 0.13.0 addressed heading coverage; PPR remains unbuilt and unscheduled as of the
  commit read.
