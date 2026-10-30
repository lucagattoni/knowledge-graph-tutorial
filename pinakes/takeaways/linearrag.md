---
slug: linearrag
neutral-entry: ../../kb-kg/projects/linearrag.md
investigated: 20260725
updated: 20261030 19:04 UTC
licence-gate: read-only reference (GPL-3.0, read from the repository's LICENSE.txt on 20261030 18:58 UTC; Pinakes is Apache-2.0)
---

# LinearRAG: what Pinakes takes from it

The facts about the project itself are in its [neutral entry](../../kb-kg/projects/linearrag.md). This page
holds only the Pinakes-specific reading. Where this page cites a number about LinearRAG, the source
and read time are in that entry. Pinakes facts were read on 20261030 from a checkout of the Pinakes
`main` branch at commit `b1bad68` (dated 20261030 08:02 UTC) and link to the public documents below.

## Verdict

Kept on file, not adopted: one idea (entity co-mention edges) is staged behind an unscheduled,
eval-gated `[ner]` extra; nothing from LinearRAG is built, and the July case for it rested on evidence
that is thinner than the July text recorded.

## What Pinakes takes

Each idea is an idea only: the licence gate below bars the code.

| Idea | Why it matters to Pinakes | Feeds |
|---|---|---|
| **Zero-LLM graph construction can compete with LLM-extraction GraphRAG.** LinearRAG reports higher accuracy than HippoRAG2, GFM-RAG and LightRAG with 0 index tokens, and gives a noise argument for why relation extraction hurts | The July investigation called it the closest published embodiment of R3, the free structural graph channel at sync time: a graph built and queried with no LLM call | R3 in the [recommendations](../recommendations-r1-r7.md); the [approach](../approach/PINAKES_APPROACH.md) |
| **Entity-passage edges as a cross-document edge class.** Two notes in different directories, with different tags and no authored link, that both mention the same entity become two hops apart. Structural edges (sibling, parent, in-section, co-located, shared-tag) never produce this class by themselves | The planned `mentions` edge in the same links table, feeding whatever channel is active. Weighted by the entity's share of occurrences in the chunk, as LinearRAG weights it | Approach §3; the `[ner]` extra |
| **Hybrid reset vector.** Put fused retrieval scores on chunk nodes and activation mass on entity or tag nodes, instead of seeding chunks only | Matches the planned seeds of the PPR channel. LinearRAG's code keeps the passage mass small next to the entity mass (a 0.05 scale on passages) | Approach §4 (PPR recipe) |
| **Query-gated hops.** A hop is followed only through a sentence similar to the question, with a threshold and a used-once set | A cheap alternative to blind expansion that addresses topic drift. Considered only if multi-hop expansion before PPR is ever built | Approach §4 |
| **Incremental NER cache keyed by content hash.** Only new or changed passages are sent to NER | Fits Pinakes' hash-based resync; the plan already says entity edges would be hash-diffed | Approach §3 |
| **Report relevance next to recall.** LinearRAG's own medical-dataset table shows relevance below plain dense retrieval on two of four tasks while recall rises | A graph channel can buy recall by spending relevance. Pinakes' measured outputs include recall@5, MRR and rerank precision ([STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md)); whether that choice came from LinearRAG: unstated | Approach §9 |

## What Pinakes leaves

| Left | Reason |
|---|---|
| **The code.** | GPL-3.0; see the licence gate. |
| **Sentence-level embeddings of the whole corpus as a default.** | LinearRAG embeds every entity-bearing sentence and every entity as well as the passages (about 378,000 such vectors for 7,000 passages in one outside corpus). Pinakes chunks are already small. If used at all, an eval-gated option. |
| **`en_core_web_trf` as a default.** | A 460 MB transformer model conflicts with the light-core rule. It would have to live in an extra, with `en_core_web_sm` (12.8 MB) as the light path. How much recall the small model loses is untested in the paper. |
| **No entity canonicalisation.** | Surface-form nodes fragment aliases. Personal knowledge bases (people, projects, private jargon) will suffer more than Wikipedia text. A cheap mitigation (case-folding plus a high-threshold nearest-embedding merge) is noted; anything larger is out of scope. |
| **The hard-coded attribute-keyword boost.** | A benchmark-shaped patch. Pinakes has lexical search for that job. |
| **Research-code defaults.** | Damping 0.5 in code against 0.85 in the paper, a pruning threshold stated as 4, a hard-coded GPU device, and different defaults in the config class and the driver script. Take the algorithm, re-derive the parameters on Pinakes' own golden set. |
| **Per-query full scan.** | The code scores every passage per query, which the paper states as linear retrieval. Untested at Pinakes scale: the RFC corpus has 106,806 chunks ([STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md)). |

## Where it landed in Pinakes

**Short answer: the structural half was built and measured; the LinearRAG half was not built.**

| Contribution | State | Evidence |
|---|---|---|
| Sibling (adjacent-chunk) edge, the one edge type LinearRAG and Pinakes both have | Built in the graph release, 0.11.0, with the other structural edges. On the 300-RFC corpus `sibling` was 106,506 of 107,411 non-transit edges and dropping it changed neither reachability nor retrieval | [STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md#did-the-expansion-channel-earn-its-default--no-measured-20260804-2252) |
| Expansion channel over structural edges | Shipped 0.11.0, **default off**. Gate run 20260804 22:52: multi-hop score 7/20 with the channel off and 4/20 with it on, 0 improved, 3 regressed, p = 1.0000. Reachability probe found 9 failing questions reachable and retrieval lifted none ("reachable is not retrievable") | [ROADMAP](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#the-graph-release--shipped-0110), STATUS (same anchor as above) |
| Entity `mentions` edges and the `[ner]` extra | **Not built.** Named "the graph release, staged": eval-gated, never scheduled, no implementation plan by design | [ROADMAP](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#the-graph-release-staged--gates-only-not-scheduled), STATUS release table |
| PPR channel and hybrid reset vector | **Not built.** Same staged item. The decision of 20260804 is that PPR's gate does not run at all on a corpus below the heading-coverage floor | ROADMAP (same anchor) |
| Query-gated hops | No trace in `STATUS.md`, `ROADMAP.md` or `DESIGN.md` (searched for "activation", "gating", "per-hop" and "query-gated") | searched 20261030 |
| Hash-diffed entity edges | Pinakes' sync is hash-based generally; the entity-specific part is part of the unbuilt `[ner]` extra | [Staged-gates plan](https://github.com/lucagattoni/pinakes/blob/main/plans/20260804_1016-staged-channel-gates.md) |

What the staged-gates plan says about `[ner]`, in short: it sets five preconditions (N1 to N5). N1
(G3 landed) is met: G3 shipped in 0.11.0. N2 requires a channel licensed to carry the edges; since
the only channel shipped off, my reading is that N2 is not met, so the gate cannot run yet (an
inference from the plan and the 0.11.0 result, not a statement in either). N4 treats model-derived
edges as a reproducibility and `schema_version` question: a change of NER model version silently
changes the edge set, which an "extra" cannot contain. The plan also says LinearRAG's wins come from
a whole system, not from the edges alone, and that no published ablation isolates the edges.
LinearRAG's own ablation text, as read on 20261030, agrees: its two variants remove the two retrieval
stages, not the entity edges.

Re-run of the structural gate on a corpus that has section headings (taken 20260825 18:16, expected to be null): no result found in `STATUS.md`.

## Licence gate

**Read-only reference.** The repository's `LICENSE.txt` is the GPL version 3 text (read 20261030 18:58
UTC); GitHub detects GPL-3.0; the README states no licence. The file was added 20251201 after a user
asked about the licence, and the copyright line is a placeholder ("anonymous"). Pinakes is Apache-2.0
and its server is a network service, so copying or vendoring GPL code would reach every embedder.
Ideas and measured results are free to reuse; source is not. Whether the project means "version 3
only" or "version 3 or later" is unstated, which does not change the rule here. Do not paste or
closely paraphrase code from the repository; re-derive any algorithm from the paper's description.

## Changed since July 2026

- 20260804 22:52: Pinakes' own graph gate did not pass (table above). It tested structural edges, not
  LinearRAG's entity edges, so it does not refute them. My reading is that it lowers the prior that
  a graph channel helps without a corpus that rewards it.
- 20261030: the July framing "independent, peer-reviewed validation of R3" needs softening. The paper
  is a peer-reviewed ICLR 2026 poster, but its benchmark numbers are the authors' own, on passages the
  authors merged and re-split by fixed token length (confirmed by a maintainer, 20260518). An open
  outside issue (#25, opened 20260507, so before the July investigation) reports that EM falls
  by about 5 to 12 points (three datasets) on the original splits. I did not reproduce that. Treat LinearRAG's margin over
  HippoRAG2 as unreplicated for Pinakes' purposes until a Pinakes-side measurement exists.
- 20261030: the project is quiet (last push 20260705, 117 days earlier), has no release, and has no
  successor. Nothing there is moving toward a fix for the points under "leaves".
- 20261030: the July text said the sentence-level embedding cost was "2 to 3 times a passages-only
  index". That was an estimate, and the code stores only entity-bearing sentences. The vector count is
  far higher than the passage count in the one outside corpus with figures. The compute cost is
  unmeasured, so the "leave" above stands on the count, not on the 2 to 3 times.
- The verdict is unchanged in direction (idea on file, not built). It is weaker in confidence than in July.
