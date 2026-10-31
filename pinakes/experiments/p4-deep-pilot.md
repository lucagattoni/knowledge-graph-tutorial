# P4: a pilot of `pnk ask --deep` on three frozen multi-hop questions

**Plan written 20261031 16:06 UTC, before any paid call.** The owner approved this pilot with a total cap of
EUR 10 (decision D-19). Results are added below the line when the run is done. Everything that could be
chosen after seeing a result is fixed here instead.

## What is fixed

| Item | Value |
|---|---|
| Software | `pinakes` 0.32.8 from PyPI, unmodified (`uvx --from "pinakes[light,claude]==0.32.8" pnk ...`) |
| Corpus | A scratch copy of the published RFC corpus repository (300 documents). The repository itself is not touched. |
| Manifest | The corpus's own `pinakes.toml`, except `[budget]`: `per_operation_eur` 2.00, `daily_eur` 10.00, `monthly_eur` 10.00. The owner's EUR 10 total cap is therefore the binding window; the 2.00 per-operation cap is Pinakes' shipped default. |
| Index | Built fresh with `pnk sync` (free, local CPU: `fastembed` `bge-small-en-v1.5` and a local reranker). The old index predates the schema bump and is not used. |
| Questions | The **first three in file order** of `eval/multihop-questions.yaml`: `http-rate-limit-status-code-provenance`, `uri-ipv6-literal-bracket-lineage`, `sip-invite-2xx-retransmission-defect`. The file says its 20 questions were authored 20260804 and frozen at the commit that first pushed it. The rule is file order, fixed now; it is not a choice of favourable questions. |
| Key | `PINAKES_ANTHROPIC_API_KEY`. The plan first said the owner would set it in their own terminal only. At 20261031 23:38 UTC the owner chose instead (D-20) to keep it in a file only they can read, outside any repository, so a terminal tab I open can use it. I never open that file; the run script reads one line of it into its own process and refuses a file others can read. Nothing about the key is written to this repository. |
| Calibration | None. The KB is uncalibrated, so the free retrieval's confidence is `unknown` and, per Pinakes' STATUS, `--deep` takes the loop with no early stop, bounded by its round limit and the budget windows. |

## Stopping rule

- One question at a time. Each run shows its estimate and asks for confirmation; I read the estimate before
  anyone confirms.
- Stop and report if any single estimate exceeds EUR 2.00 (Pinakes would refuse it anyway) or if the three runs
  together would exceed the EUR 10 cap.
- **No question is re-run to get a better answer.** A refusal or a failure is reported as it is.

## Recorded for each question

1. Whether the free retrieval (round 0, `final_k` 8) returns each evidence document the question lists.
2. The run's estimate and reconciled spend (from `pnk budget`) and the path of its transcript.
3. The answer, the passages it cites, and whether the cited passages cover every evidence document.
4. The number of rounds used and which bound ended the run.
5. My reading of whether the answer is right, made by reading the evidence documents. It is labelled as a
   reading; the file gives no gold answer text.

## What this cannot show

- Three questions cannot estimate an accuracy rate, and nothing from them is compared with the free path's
  7 of 20 (the `off` arm of the graph gate): that arm used a different instrument and all 20 questions.
- The cost is for this corpus, these three questions and this version. It does not bound other runs.
- It tests Pinakes as built. It changes none of its code.

---

## Results

*The three questions have not run. No paid call has been made.*

### Index build (free, local CPU), finished 20261031 19:18 UTC

Started 16:05 UTC, exit code 0, so about 3 h 13 min against the roughly two hours I had estimated. Read from the
build's own output and from `pnk doctor` and `pnk budget` (0.32.8) at 19:18 UTC:

| Item | Value |
|---|---|
| Sync result | 300 indexed, 0 removed |
| Index | 300 active documents, 106806 chunks |
| Derived edges | 214217, plus 391 authored (membership 106806, sibling 106506, co-located 262, shared-tag 643) |
| Budget | 0.00 of 10.00 today, 0.00 of 10.00 this month, 0 reservations, per-operation cap 2.00 |
| Doctor warnings | calibration: no fitted thresholds, so confidence reports `unknown`; heading coverage: 0 of 106806 chunks carry a heading path (`[chunking] headings` is unset); embedding and reranker revisions unpinned; scale past the 50000 NumPy-tier threshold |

The two conditions that matter for the questions: the run uses an uncalibrated KB (as the plan states), and the
chunks carry no heading paths, so citations here have no heading component. Both are the corpus manifest's
settings, not choices made for this pilot.

### Round 0 and the estimates, read before any paid call (20261031 23:38 UTC)

`pnk ask --offline -k 8 --json` on each question, with no `--deep` and no key: a local retrieval, no model call,
no spend. "Found" means that at least one of the 8 returned passages comes from the listed document. It does not
mean the passage holds the fact the question needs. The output is not committed.

| Question | Evidence documents found | Missing | Estimate of the deep run |
|---|---|---|---|
| 1 `http-rate-limit-status-code-provenance` | 2 of 3 | `docs/http/rfc2616.txt` | EUR 1.64 |
| 2 `uri-ipv6-literal-bracket-lineage` | 3 of 3 | none | EUR 1.64 |
| 3 `sip-invite-2xx-retransmission-defect` | 2 of 2 | none | EUR 1.64 |

Each retrieval reports `confidence` `unknown` and, in its `escalation` block, `cost_eur` `1.64` with the note
that without a calibrated signal "a run ends at its caps rather than at sufficiency". Each estimate is under the
EUR 2.00 per-operation cap; the three together are EUR 4.92 (my arithmetic), under the EUR 10 total. The
measured spend on earlier synthetic corpora was far below the estimate (see [next.md](next.md)), so the estimate
is a ceiling, not an expectation. Question 1's eight passages come from four documents, five of them from
RFC 6585; question 3's are seven of eight from RFC 6026.
