# What Pinakes should measure next

**Status: P1 answered; the P4 pilot ran on 20261101 (results in [p4-deep-pilot.md](p4-deep-pilot.md)); P3's
free-path half exists in the public [benchmark repository](datasets-benchmark.md); P2 is blocked.** Each needs the owner's explicit yes, one at a time. This
page continues [what Pinakes has measured](README.md): it takes the items Pinakes' own documents leave
approved, gated or unmeasured, and says what each would cost. Field-neutral experiments are in
[`../../kb-kg/experiments/README.md`](../../kb-kg/experiments/README.md).

Pinakes' own rules apply to anything that touches it. A paid run needs the dedicated key variable, is priced
and refused against three budget windows before its first call, and asks once
([STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md)). Another session works in the
Pinakes repository, so I would tell it the exact files before touching anything there.

| ID | Item | Cost | Source of the item |
|---|---|---|---|
| P1 | Did the approved graph-gate re-run on a corpus with sections happen? | None | Approved 20260825 18:16; no result found |
| P2 | `[ner]` and `mentions` edges (Gate 2) | **Blocked** | Precondition N2: a licensed channel |
| P3 | Public-dataset baselines for the free retrieval path | Free CPU | The [benchmark repository](datasets-benchmark.md), now public; its free-path half exists, a BM25-alone arm is unstated |
| P4 | Pilot of `pnk ask --deep` on 3 of the 20 frozen multi-hop questions | **Ran 20261101: EUR 0.3084 in all** | No accuracy result on that set found; three questions support none |

## P1: Ask whether the sections re-run happened

Pinakes' ROADMAP records that the re-run on a corpus that has sections "was TAKEN by the user 20260825
18:16", would cost "~2.4 h of free CPU", and has an expected result of "another null". I found no result in
STATUS, ROADMAP, DESIGN or the dated plans, and the published RFC corpus repository's newest commit predates
the heading-path work. That does not prove it did not run. **This is the owner's own approved item, not a new
proposal.** The proposed step is only to ask the Pinakes session, which holds that knowledge, whether it ran
and where the result is. Cost: none.

**Answered 20261031 by the Pinakes session: not run, as far as the repository records.** It read
`origin/main` at `c4bf2cb` and reports: ROADMAP still states the re-run in the future tense with no verdict;
the sweep's own liveness test for it ("no verdict recorded means still open") finds no verdict; no commit
since 20260825 touches `tools/graph_gate.py` or `tools/graph_matrix.py`; no commit message since mentions the
re-run; the changelog and retrospectives mention it only as having sat unowned for 21 days; and the published
RFC corpus repository's newest commit is `376b1cb` (20260804). **The limit of that answer:** a run that left
no commit and no note would not show in the repository. Only the owner can say whether one happened.

## P2: Gate 2 is blocked, and the field offers a candidate extractor

Gate 2 defaults `mentions` edges on only if a long list of conditions holds; the first is that a licensed
channel exists, and none is licensed (the `expand` gate failed). So Gate 2 cannot run now. For when it can, the
field-neutral [GLiNER entry](../../kb-kg/projects/gliner.md) describes a small entity extractor that calls no
LLM; its model-weight licences were not verified by the writer. Cost today: none, because nothing runs.

## P3: Public-dataset baselines for the free retrieval path

The owner described a harness that benchmarks Pinakes retrieval against public datasets with ground-truth
evidence, starting with MultiHop-RAG (2,556 queries with evidence in 2 to 4 documents, per the
[papers page](../../kb-kg/papers-benchmarks/README.md)). A first run would be Pinakes' free path (BM25, local
embeddings and reranking) against BM25 alone. **Cost: free local CPU**; **models: local only.**

**Update 20261102 08:56 UTC: that repository is now public and has run the free path on MultiHop-RAG.** It is
[described on its own page](datasets-benchmark.md), with its figures marked as first-party and its limits kept.
The half of P3 that gave the free path a number on a public set exists; a **BM25-alone arm is unstated** in its
README, so the comparison named here is not shown there. The dataset's licence is ODC-By 1.0 per that repository.
Anything further would be run in that repository, not here, and is its owner's call.

## P4: `pnk ask --deep` on the 20 frozen multi-hop questions

**Approved 20261031 as a pilot of 3 questions with a total cap of EUR 10. The plan, written before any paid
call, is [p4-deep-pilot.md](p4-deep-pilot.md). Run 20261101: the three questions cost EUR 0.3084 in all against
EUR 4.92 of estimates, each used all 3 rounds, and the answers and my readings are in
[the pilot's summary](p4-deep-pilot.md#what-the-three-runs-show-and-what-they-do-not).**

Pinakes' documents record what a deep run costs (estimates and measured spend on synthetic corpora) and I
found no accuracy result for it on the RFC multi-hop set; I may have missed one. The 20 multi-hop questions
were frozen before any code ran. The figures below are from STATUS; the arithmetic is mine.

| Quantity | Value | Basis |
|---|---|---|
| Estimator, cheap branch (one synthesis call) | EUR 0.2627 | STATUS, at the shipped defaults |
| Estimator, a three-round loop | EUR 1.6872 | STATUS |
| Per-operation cap | EUR 2.00 | STATUS (decision D-30) |
| Measured spend per run, one-call branch | about EUR 0.0071 | EUR 0.0353 over 5 runs |
| Measured spend per run, calibrated loop | about EUR 0.0271 | EUR 0.0542 over 2 runs |
| Measured spend per run, uncalibrated loop | about EUR 0.0618 | EUR 0.1235 over 2 runs |
| Twenty questions at the uncalibrated-loop rate | about EUR 1.24 | 20 times 0.0618, my arithmetic |
| Twenty questions at the estimator's ceiling | about EUR 33.74 | 20 times 1.6872, my arithmetic |

The measured runs were on small synthetic corpora, so spend on the 300-RFC corpus is **unstated**; the
estimator over-reserved by 22 to 51 times in those measurements, so the ceiling is not the expectation. **Pilot:
3 questions**, then set the cap from what they cost. Pinakes would still refuse any single run whose estimate
exceeds its per-operation cap. This uses Pinakes as built and changes none of its code.

## What I need from you

Nothing in P3 needs doing here; a BM25-alone arm would be a request to the benchmark repository's owner. A larger P4 (more of the 20 questions, or a calibrated KB) would be a new
proposal with its own estimate and cap; none is scheduled. P2 waits for a licensed channel.
