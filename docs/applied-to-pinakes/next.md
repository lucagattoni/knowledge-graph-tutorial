---
type: page
order: 4
updated: 20261102 20:16 UTC
---

# What Pinakes should measure next

This page answers one question in three parts: which measurements of Pinakes are still open, in what order the follow-ups should come, and what each one needs from the owner before it can start. It continues [what Pinakes has measured](measurements.md) and uses the four proposals, P1 to P4, that the archive made [16]. **Nothing on this page is scheduled: each step needs the owner's explicit yes, one at a time** [17].

## The four proposals

| ID | Item | Status on 20261102 | Cost | What blocks it |
|---|---|---|---|---|
| P1 | Did the approved re-run of the graph gate, on a corpus that has sections, happen? | **Answered 20261031:** not run, as far as Pinakes' repository records [16][3] | None | Only the owner can say whether an unrecorded run happened |
| P2 | The `[ner]` extra and `mentions` edges (Gate 2) | **Blocked** [5][4] | None today: nothing can run | Precondition N2: a retrieval channel that is licensed on |
| P3 | Public-dataset baselines for the free retrieval path | **Half done** in a separate public benchmark repository [6][7] | Free local CPU | A [BM25](../index/bm25.md)-alone arm is **unstated** there |
| P4 | A pilot of `pnk ask --deep` on 3 of the 20 frozen [multi-hop questions](../index/multi-hop-question-answering.md) | **Ran 20261101:** EUR 0.3084 in all [15] | Paid, capped | A wider run needs its own yes, key and cap |

Pinakes' latest release is 0.32.9; the pilot and the benchmark both ran on 0.32.8 [4][6][15]. A release number is a snapshot: re-read Pinakes' STATUS file before relying on it.

## The sections re-run (P1)

Pinakes' ROADMAP says the re-run of the graph gate on a corpus that has sections "was TAKEN by the user 20260825 18:16", costs "~2.4 h of free CPU" and has an expected result of "another null" [1]. Pinakes' own decision brief ranks it last of ten items and says: "If session time rather than CPU is the binding constraint, decline it" [2].

The session that works in the Pinakes repository answered on 20261031: no recorded run. I re-checked three of its grounds on 20261102 against the repository at its newest commit, `d2f0d53`, pushed 20261102 15:29 UTC [3]:

- The ROADMAP passage still states the re-run in the future tense [1].
- The newest commit touching `tools/graph_gate.py` is dated 20260810 and the newest touching `tools/graph_matrix.py` 20260804, both before the approval [3].
- Of 721 commits since the approval, nine subjects match "re-run", "graph gate", "sections" or "heading"; none concerns the gate re-run [3].

*Reading:* this is evidence of absence in the repository, not proof. A run that left no commit and no note would not show. The expected gain is small. The first gate found `expand` worse than off, 4 of 20 against 7 of 20 multi-hop questions, with p = 1.0 [4]. The re-run would remove only one of the gate's two stated bounds: `[retrieval.confidence]` is still commented out in the published RFC corpus manifest, so two of the gate's four clauses stay unexercised [4][2][13].

## Gate 2 is blocked (P2)

Gate 2 would turn `mentions` edges on by default only if every clause of a list holds: zero lost simple-lookup questions, a sign test with p below 0.05 on a licensed channel, a sync-time budget, and at least 25% and at least 20 document pairs that no other edge kind connects [5]. Its second precondition, N2, requires "A channel is licensed on" [5]. *Reading:* no channel is, because `expand` ships off after its gate failed and the [personalized-PageRank](../index/personalized-pagerank.md) channel is "eval-gated, never scheduled" [4].

The plan sized the extractor at a 440 MB spaCy model [5]. The archive suggested a lighter candidate, [GLiNER](../projects/gliner.md), which trains and runs small [named-entity-recognition](../index/named-entity-recognition.md) models and whose README lists CPU deployment [14]. Its repository is Apache-2.0 by its `LICENSE` file [14]. Two model cards I read, for `gliner_medium-v2.1` and `gliner-bi-base-v2.0`, state apache-2.0 [14]. The licence of any other checkpoint is **unstated**. Cost today is none, because nothing can run.

## Baselines for the free path (P3)

The free path is BM25, local embeddings and local [reranking](../index/reranking.md) [6]. A separate public repository, `pinakes-datasets-benchmark`, has run it on [MultiHop-RAG](../datasets/multihop-rag.md): 2,255 answerable and 301 null questions, 8,497 searches [6]. When I read it, on 20261102 20:14 UTC, its `main` was `7bbed5f`, committed 20:02 UTC [6][7]. All figures below are first-party.

| Measure, answerable questions | First 5 passages | First 8 (default) | First 20 (reranker pool) |
|---|---|---|---|
| At least one gold article found | 91.5% | 96.8% | not computed |
| **Every** gold article found | 33.8% | **43.4%** (95% interval 41.3 to 45.4) | 61.0% (58.9 to 63.0) |

The README puts "every gold article" in bold as the headline and notes that "at least one" is what Pinakes' own harness counts as a hit [6]. Its limits: one dataset whose questions a language model generated, default settings, one machine, and the graph channel, the paid `--deep` loop and a real provider switch "not run yet" [6].

**The gap:** the comparison P3 named, the free path against BM25 alone, is not shown. The README does not describe a BM25-alone arm, and the repository's `configs/` holds `baseline`, `baseline-fastembed`, `metadata-prefix` and the model pins [6][7]. *Reading:* it is also not a configuration switch. Pinakes' manifest documents `fusion` as `rrf`, "The only value", and `rerank` as `local` or `none`; I found no key that removes the vector source [9]. A BM25-alone arm would be new scoring code in the benchmark repository, which is its owner's decision.

The benchmark repository also lists candidates for further datasets, ranked by properties and **not run**. One, BrowseComp-Plus, is described as a testbed for the `--deep` loop [8].

## The deep-loop pilot (P4)

The owner approved a pilot of three questions, in file order from a set of 20 frozen before any code ran, with a total cap of EUR 10 [17][15]. It ran on 20261101 with a hosted model.

| Quantity | Value | Source |
|---|---|---|
| Spend | EUR 0.3084 in all (the three rounded per-run figures sum to 0.3083) | [15] |
| Free pre-flight estimates | EUR 1.64 each, EUR 4.92 in all; actual spend about one sixteenth | [15] |
| Paid calls and rounds | 6 calls and all 3 rounds in every run, because the KB has no calibration | [15] |
| Parts of the questions answered correctly in some printed block | Q1: the document, not the amended specification; Q2: all three, spread over blocks that disagree; Q3: both, in round 1 | [15], labelled readings |
| Cap and per-operation limit | EUR 10 total; EUR 2.00 per operation | [15][4] |

Pinakes' own estimates differ with the KB's settings and its price table: STATUS gives EUR 1.6872 for a three-round loop at shipped defaults, and its ROADMAP records EUR 1.33 for an uncalibrated `pnk ask` in the Guide's example of release 0.28.2, whose KB settings are unstated here [4][21]. Use the free pre-flight of the run in hand, not a figure from a page.

**What the pilot cannot show:** an accuracy rate, any comparison with the free path's 7 of 20, whether calibration would stop the loop earlier or cheaper, or anything about the other 17 questions [15]. The raw logs are not committed; I did not re-derive the figures from them.

## Order of the follow-ups

The first two follow-ups do not wait for the field-neutral experiments [16]. X3, the matched-cost comparison, needs "a baseline that uses BM25 alone" [19], so step 1 also feeds [X3](../experiments/x3-matched-cost-comparison.md).

| Step | Follow-up | Cost | Depends on | Needs from the owner |
|---|---|---|---|---|
| 1 | A BM25-alone arm in the benchmark repository (the P3 gap) | Free | Nothing | Whether to send the request to that repository's owner |
| 2 | A calibrated deep run on the same three questions, as a new labelled experiment | **Unstated** until calibration changes how many rounds run | A way to calibrate (below) | A yes, a new key, a cap |
| 3 | A wider P4 on more of the 20 questions | Unstated | Step 2, because cost per question depends on whether the loop can stop early | A new proposal with its own estimate and cap |
| 4 | Gate 2 (P2) | Unstated | A licensed channel | Nothing now |

### The calibration gap behind the calibrated run

Each pilot run printed the remedy for an `unknown` confidence: fit `[retrieval.confidence]` with `python -m pinakes.calibrate <kb>` [10]. The archive called that free local CPU [16]. Four facts from the files change that:

- `calibrate.fit` raises an error, "the golden set has no `no-answer` questions", when the set has none [11].
- A question is answerable unless its `kind` is `no-answer` [12].
- The RFC corpus's `eval/questions.yaml` holds 20 questions, all `kind: multi-hop` [13].
- Both thresholds are fitted on the no-answer questions' scores; the answerable ones are not used for them [11].

*Reading:* calibration cannot run on that KB with its shipped question file. It needs a set of no-answer questions first. How many are enough is **unstated** in the files read. Thresholds fitted under one reranker provider do not carry to the other, because the scores sit on different scales and `fitted_for` cannot tell; Pinakes advises re-fitting after a provider change [9].

| Option | Pros | Cons |
|---|---|---|
| **A. Author a small no-answer set for the RFC corpus, frozen before use** (recommended) | Keeps the three pilot questions and the frozen 20; the thresholds do not touch the multi-hop questions [11] | Authoring work; the set should be written blind and frozen, as Pinakes' rule for question sets suggests (authored blind, frozen before any code exists) [22] |
| B. Calibrate on the benchmark's news corpus, which has 301 null questions | Null questions already exist [6] | A different corpus, so it is not the same three questions; the deep loop's cost there is unstated |

## What each item needs from the owner

| Item | Needs |
|---|---|
| P1 | An answer to whether a run happened without a trace; or a decision to ask for the run, or to decline it as Pinakes' brief allows [2] |
| P2 | Nothing until a channel is licensed |
| BM25-alone arm | A decision to send the request |
| Calibrated deep run | A yes with model, provider and cap; a new key (the pilot's key file was deleted, and whether to rotate or revoke the old key is the owner's call [18]); a choice between options A and B |

Rules that bind all of it: experiments run one at a time, each stating cost, models and data first [17]. Runs happen only on the owner's Apple Silicon Macs, with hosted models acceptable and one model per comparison [17]. The written authorisation to run the pilot's questions without a typed confirmation covered those three questions only [17]. Nothing here edits the Pinakes repository without the owner's explicit yes at that step [20].

## Sources

1. https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md : the passage on re-running the gate against a corpus that has sections (quotes; "TAKEN by the user 20260825 18:16", ~2.4 h, another null, `expand` stays off) (read 20261102 19:37 UTC)
2. https://github.com/lucagattoni/pinakes/blob/main/plans/20260825_1803-open-decisions.md : the re-run ranked last of ten; the "decline it" sentence; `[retrieval.confidence]` still commented out (read 20261102 19:38 UTC)
3. https://github.com/lucagattoni/pinakes/commits/main : newest commit `d2f0d53` (20261102 15:29 UTC); newest commits touching `tools/graph_gate.py` (`5b2047f`, 20260810) and `tools/graph_matrix.py` (`57028f9`, 20260804); 721 commits since 20260825 18:16 UTC, subjects scanned (read 20261102 20:14 UTC, via the GitHub API)
4. https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md : latest release 0.32.9; the gate result (7/20, 4/20, p = 1.0000, `expand` ships off); "the graph release, staged" row; two stated bounds; estimator row and the EUR 2.00 per-operation cap (D-30) (read 20261102 19:37 UTC)
5. https://github.com/lucagattoni/pinakes/blob/main/plans/20260804_1016-staged-channel-gates.md : Gate 2 preconditions N1 to N5 and the gate clauses; the 440 MB spaCy model (read 20261102 19:38 UTC)
6. https://github.com/lucagattoni/pinakes-datasets-benchmark/blob/main/README.md : 215 lines, the results table, the limits, the "not run yet" list, no BM25-alone arm described (read 20261102 20:14 UTC, `main` at `7bbed5f`)
7. https://github.com/lucagattoni/pinakes-datasets-benchmark : repository metadata, commit list and the `configs/` and `runs/` listings (read 20261102 20:15 UTC)
8. https://github.com/lucagattoni/pinakes-datasets-benchmark/blob/main/datasets/README.md : candidates for the next datasets, none run (read 20261102 20:14 UTC)
9. https://github.com/lucagattoni/pinakes/blob/main/docs/MANIFEST.md : the `[retrieval]` and `[embedding]` tables (`fusion`, `rerank`, `provider`); the paragraph on thresholds across reranker providers (read 20261102 19:43 UTC)
10. https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md : the `unknown` row of the `pnk ask` confidence table (read 20261102 19:40 UTC)
11. https://github.com/lucagattoni/pinakes/blob/main/src/pinakes/calibrate.py : `fit`, its error for a set without no-answer questions, the fit on unanswerable scores (read 20261102 19:40 UTC)
12. https://github.com/lucagattoni/pinakes/blob/main/src/pinakes/eval.py : `Question.answerable` (read 20261102 19:41 UTC)
13. https://github.com/lucagattoni/pinakes-corpus-rfc : `eval/questions.yaml` (20 questions, all `kind: multi-hop`, counted), `eval/multihop-questions.yaml`, `pinakes.toml` with `[retrieval.confidence]` commented out; newest commit `376b1cb`, 20260804 (read 20261102 20:14 UTC)
14. https://github.com/urchade/GLiNER : repository metadata, `LICENSE` file (Apache License 2.0), README description and CPU note; model cards https://huggingface.co/urchade/gliner_medium-v2.1 and https://huggingface.co/knowledgator/gliner-bi-base-v2.0 (licence field apache-2.0, via the Hugging Face API) (read 20261102 20:15 UTC)
15. [pinakes/experiments/p4-deep-pilot.md](../../pinakes/experiments/p4-deep-pilot.md) : the pilot's plan, results and labelled readings; the raw logs are not committed, so no primary record of the runs is public (read 20261102 19:36 UTC, via the archive page)
16. [pinakes/experiments/next.md](../../pinakes/experiments/next.md) : the proposals P1 to P4, the P1 answer, the order of follow-ups (read 20261102 19:36 UTC, via the archive page)
17. [DECISIONS.md](../../DECISIONS.md) : D-14, D-19 to D-21 and D-24 (read 20261102 19:36 UTC)
18. [RESUME.md](../../RESUME.md) : the owner's open question on rotating the pilot key (read 20261102 19:36 UTC, `main` at `f2e87e6`)
19. [kb-kg/experiments/README.md](../../kb-kg/experiments/README.md) : X3 and the order and gates (read 20261102 19:36 UTC)
20. [CLAUDE.md](../../CLAUDE.md) : the rule that the Pinakes repository is not edited without the owner's explicit yes (read 20261102 19:36 UTC)
21. https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md : the 0.28.2 section, the table of re-run Guide blocks (`pnk ask`, uncalibrated, EUR 1.69 to EUR 1.33) (read 20261102 19:37 UTC)
22. [pinakes/experiments/README.md](../../pinakes/experiments/README.md) : Pinakes' rule that questions are authored blind and frozen before any code exists (read 20261102 19:36 UTC, via the archive page)
