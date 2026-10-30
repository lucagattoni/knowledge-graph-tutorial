---
slug: logicrag
neutral-entry: ../../kb-kg/projects/logicrag.md
investigated: 20260726
updated: 20261030 19:08 UTC
licence-gate: read-only reference (GPL-3.0; LICENSE file re-read 20261030 18:58 UTC; Pinakes is Apache-2.0 and its server is a network service)
---

# LogicRAG: what Pinakes takes from it

The facts about the project itself are in its [neutral entry](../../kb-kg/projects/logicrag.md). This page
holds only the Pinakes-specific reading. Pinakes facts below come from the public
[`STATUS.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md) (latest release 0.32.8,
last reviewed 20261029 18:57 UTC), [`ROADMAP.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md),
[`DESIGN.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md) and
[`CLI.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md), read 20261030 19:04 UTC from a
checkout of the repository.

## Verdict

LogicRAG was the blueprint for the *shape* of `pnk ask --deep` (a bounded loop that starts with plain
retrieval and carries a fixed-size memory), and that shape was built; its dependency graph, its code and its
benchmark claims were not taken, and its numbers are supporting evidence for the idea, not a validation of the
released code.

## What Pinakes takes

Ideas only. Each row says what the July note proposed and which Pinakes design layer it feeds. Whether and how
it was built is in the next section.

| Idea (July 2026 note) | Feeds |
|---|---|
| Reasoning structure belongs to the *query*, not the corpus: build it lazily at ask time instead of paying for an index-time graph. This matches the stance of recommendations [R5 and R6](../recommendations-r1-r7.md) | The paid path of the [Pinakes graph approach](../approach/); [DESIGN 4.3](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md#43-multi-hop-without-paying-for-it) |
| **Warm-up first**: round 0 is ordinary retrieval and a sufficiency gate; decompose only when the gate fails. In Pinakes the gate is the free calibrated confidence signal, not an LLM self-report, which avoids LogicRAG's documented premature-confidence defect | `pnk ask --deep` branch choice |
| **Flat list, local ordering**: decomposition returns plain strings and local code does the ordering, so no graph library or schema is needed; add the cycle check LogicRAG skipped | the loop's decomposition call (but see "Where it landed": this was changed) |
| **Rolling memory as the budget backbone**: one bounded summary re-folded every round keeps per-round cost constant, so a pre-call cost reservation against the `--deep` cap is predictable | the `[budget]` ledger and the pre-call estimate |
| **Sampling without replacement**: never re-ask a stalled sub-problem; advance the cursor | the loop's anti-stall rule |
| **Round cap with a best-effort answer** rather than a failure | `[deep] max_rounds` |
| **Write-back LogicRAG leaves on the floor**: keep the decomposition and sub-answers as a transcript, and turn document pairs that supported one answer into suggested typed links | run transcript; sidecar `links[]` suggestions |
| **Loop only in the CLI path**: MCP callers compose search and get themselves and never trigger an internal LLM loop (R6) | DESIGN 4.3, the MCP tool surface |
| Measured results as evidence: no index cost; query-time tokens against graph baselines (neutral entry, Table 4); the effect of forcing progress (Figure 4). Use the corrected figures in the neutral entry, not the July ones | design rationale only |

## What Pinakes leaves

| Left | Why |
|---|---|
| LogicRAG's code | GPL-3.0; see "Licence gate". Algorithm-level lessons only |
| An LLM-judged sufficiency check used alone | The paper names premature confidence on long queries. Pinakes' calibrated confidence signal should gate the rounds |
| Dense-only whole-matrix retrieval, no reranking | Weaker than Pinakes' hybrid pipeline (BM25 plus embeddings, rank fusion, rerank); nothing to adopt from the retriever |
| Prompted JSON with regex repair of truncated replies | Pinakes uses structured outputs |
| Per-sub-problem answers discarded into one summary | Pinakes needs each paid run to be auditable: question, cost and result kept per run |
| The paper's rank-merged unified queries and dynamic DAG growth | Not in the released code, so unproven as an artifact; not cited as validated |
| An LLM-built dependency graph with a topological sort | July proposed keeping it with a cycle check; the build did not take it (see below) |
| Any claim that LogicRAG shows this loop is "the efficient frontier" | Not supported by the paper's Table 4 (see "Changed since July 2026") |

## Where it landed in Pinakes

Built, and complete as a named body of work: the deep release finished at
[0.26.0](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#0260--a-paid-run-tells-you-what-it-learned-about-your-kb--20260822-0132)
(20260822 01:32 UTC) [S1][R1]. `pnk ask --deep` was released in 0.24.0 (20260811 22:24 UTC) and, per
STATUS, has **worked against the live API only since 0.25.1** (20260821 07:17 UTC): every `--deep` call in
0.22.0 through 0.25.0 failed on a schema defect before billing [S1][R2].

| July proposal | Built? | Release and date (UTC) | What was built | Evidence |
|---|---|---|---|---|
| Free retrieval as round 0, calibrated gate chooses the branch | Yes | 0.24.0, 20260811 22:24 | High or medium confidence: one synthesis call. Low: the loop, stopping the moment the evidence is judged sufficient. Unknown (no calibration on the KB): the same loop with no early stop, and the output names the bound that ended it | [S1][R1][D1] |
| Decompose, then dependency DAG, cycle check, topological order | **No** (changed) | n/a | A round is two calls: one turns the question plus what earlier rounds established into a flat list of sub-problems, one answers from the merged retrieval with citations. A sub-problem is a plain string; the schema has one field. No pair-generation call, no graph, no topological sort, no cycle check | [D1][C1] |
| Rolling summary, constant per-round cost | Yes | 0.24.0 | The carried memory is re-folded to a fixed budget rather than appended to. The run is priced and refused before the first call against all three `[budget]` windows, then each call is reserved and reconciled | [D1][R1] |
| Estimate as a sound upper bound | Yes, measured | 0.25.3, 20260821 22:34 | Over-reservation measured on synthetic corpora: 29.75x (cheap branch), 50.92x (calibrated loop), 22.35x (uncalibrated loop); no ceiling lowered. These are Pinakes' own estimator results, not a comparison with LogicRAG | [R3] |
| Sampling without replacement | Yes | 0.24.0 | A sub-problem is never re-asked once asked; the cursor advances. Pinakes records no token saving of its own for this rule (unstated) | [D1] |
| Round cap with best-effort answer | Yes | 0.24.0 | `[deep] max_rounds`; the cap ends in a best-effort answer. The output reports `stopped_by` (answered, sufficient, round-cap, no-new-subproblems, no-evidence, budget). A budget halt follows `[budget] on_exceed`: `partial` returns what completed rounds established, `abort` returns nothing. A paid run with no answer exits 1 | [D1][C1][R1] |
| Structured outputs instead of regex repair | Yes | 0.24.0, fixed in 0.25.1 | Schema-constrained decomposition and answer calls. A citation is an index into the passages the call was shown | [D1][C1][R2] |
| Ask transcript | Yes, narrower | 0.25.0, 20260812 05:31 | `.pinakes/deep/<operation_id>.json`: the question, the filters as typed, the confidence reading that chose the branch, the model and prompt version, and the answer object. Whether it also holds each round's sub-problem strings is **unstated** in the docs read. It is KB-local and never leaves `.pinakes/`, so it is not a committed file as July suggested | [C2][R4] |
| Suggested typed links from co-supporting documents | Yes, print-only | 0.26.0, 20260822 01:32 | A run ends by printing `links[]` entries (`rel: co-cited`, `origin: deep`) for documents cited together in one answer, to paste and commit. Sub-problem chains are not involved because there is no chain. `--write-suggestions` is deferred and unplanned | [S1][C3][R5] |
| Loop only in the CLI, never MCP | Yes, gated | 0.24.0 | No `pinakes_*` tool exists for it, and a test asserts the server process never loads the module | [D1][C1] |
| Cycle check | **No** | n/a | Not applicable to the build: with a flat list there is no ordering that could contain a cycle. The July reason for the check no longer applies | [D1] |

No Pinakes document read names LogicRAG: a search of STATUS, ROADMAP, DESIGN and CLI for "logicrag" found
nothing (20261030 19:04 UTC). DESIGN 4.3 says three properties come "from the published systems this shape
comes from, and none of them are code", and that "the two defects the same notes record are designed out"
[D1]. The deep-release plan names the July note as prior art and restates the rule "algorithm-level lessons
only, never ported code" [P1]. No head-to-head run of Pinakes against LogicRAG is recorded in the documents read.
Pinakes' own retrieval benchmark is a separate effort ([DECISIONS](../../DECISIONS.md), D-15).

## Licence gate

**Read-only reference.** The `LICENSE` file is the GNU GPL version 3 text and was re-read on 20261030
18:58 UTC; it was added on 20260719, and the repository had no licence file before then (neutral entry,
"Changed since the July 2026 investigation"). Pinakes is Apache-2.0 and its server is a network service, so a
copyleft licence would reach anyone embedding it. Ideas and measured results are free to reuse; source is not.
This page describes ideas and published results only, and the neutral entry describes the repository's behaviour
in prose without reproducing code. I did not audit the Pinakes source for similarity to LogicRAG's code. The
design record says the borrowed properties "are not code" [D1].

## Changed since July 2026

Checked 20261030 18:58 to 19:08 UTC. Project-side changes are in the
[neutral entry](../../kb-kg/projects/logicrag.md#changed-since-the-july-2026-investigation); only what bears on
the Pinakes reading is repeated here.

- **The verdict was reworded.** July called LogicRAG "a published, benchmarked validation of the `pnk ask --deep`
  shape". Two facts weaken that. (1) The paper's Algorithm 1 and the released code differ: rank-merged queries,
  dynamic DAG growth, per-sub-problem answers and few-shot decomposition are not in the code, and the code's
  warm-up early exit is not in Algorithm 1. Which of the two produced the reported numbers is unstated. (2) Pinakes
  built neither variant: it has a warm-up gate and a rolling memory, but a flat re-planned list rather than a
  dependency graph. The numbers support the cost argument for a query-time loop; they do not validate Pinakes'
  loop.
- **Two July figures in the Pinakes graph approach need softening.** Its paid-path section says the shape "is
  not a compromise, it is the efficient frontier" on the strength of 1,778 against 5,731 tokens per query. In
  Table 4, G-retriever uses 1000.0 tokens, and RAPTOR, HippoRAG and HippoRAG2 answer faster (5.79 s, 6.30 s and 5.89 s
  against 9.83 s). The 1,778 and 5,731 figures themselves are correct. The "about 35% token cut" for
  forcing progress holds for MuSiQue only (18% on 2WikiMQA, 17% on HotpotQA). That document is being moved into
  [`../approach/`](../approach/); its writer should apply both corrections.
- **Licence gate unchanged**, now with a date: GPL-3.0 since 20260719. No licence change since, no archive, no
  release, no commits after 20260719. Nothing in the project's state opens the gate.
- **Pinakes side:** July's "not yet built" items are all built or deliberately dropped, as tabled above. The one
  open question this pass leaves is whether the transcript holds per-round sub-problem strings (unstated).
- **No successor or rename** of LogicRAG found; nothing to add to the reading.

## Sources used on this page

Public Pinakes documents, read 20261030 19:04 UTC from a checkout of the repository (latest release 0.32.8):

- [S1] https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md (row `pnk ask --deep`; release rows 0.23.0 to 0.26.0)
- [R1] https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#0240--pnk-ask---deep-answers--20260811-2224
- [R2] https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#0251--pnk-ask---deep-works-against-the-live-api--20260821-0717 (the STATUS 0.25.1 row)
- [R3] https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#0253--the-deep-loop-is-measured--20260821-2234
- [R4] https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#0250--a-paid-run-leaves-a-record-of-what-it-was-asked--20260812-0531
- [R5] https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md#0260--a-paid-run-tells-you-what-it-learned-about-your-kb--20260822-0132
- [D1] https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md#43-multi-hop-without-paying-for-it
- [C1] https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md#pnk-ask---deep
- [C2] https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md#the-transcript
- [C3] https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md#suggested-links
- [P1] https://github.com/lucagattoni/pinakes/blob/main/plans/20260811_1358-deep-release.md (row M10 and the rows on best-effort answers and the CLI-only rule)
- Latest Pinakes release tag and date: the repository's releases page, read 20261030 19:04 UTC (0.32.8, published 20261029 18:53 UTC)

Project facts (repository, paper, benchmarks) are cited in the neutral entry's source list, not repeated here.
