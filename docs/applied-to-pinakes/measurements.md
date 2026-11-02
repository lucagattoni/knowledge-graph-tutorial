---
type: page
order: 3
updated: 20261102 20:16 UTC
---

# Measurements

This page answers four questions about Pinakes' own evidence: how it decides what to build, what it has measured and what each number decided, what its public-dataset benchmark added, and what the first paid test of its deep loop showed. Every result here is **first-party**: the project ran the instruments, had the questions written and published the numbers, and I found no independent re-run in the sources read. The long evidence is in the archive ([the experiments notebook](../../pinakes/experiments/README.md), [the benchmark note](../../pinakes/experiments/datasets-benchmark.md), [the pilot record](../../pinakes/experiments/p4-deep-pilot.md)). [The approach page](approach.md) and [the next-steps page](next.md) are the neighbours of this one.

**State, read 20261102 19:37 UTC.** Pinakes' STATUS file says the latest release is 0.32.9, last reviewed 20261102 15:19; the repository's `main` was at `d2f0d53` (committed 20261102 15:29 UTC) [1][10]. Where this page and STATUS disagree, STATUS wins [1]. The benchmark and the deep-loop pilot below ran on 0.32.8 [12][21]. STATUS lists no change to ranking in 0.32.9, but I did not diff the code [1]. Numbers are copied as Pinakes gives them, with commas for thousands. Anything the sources do not give is marked **unstated**.

## How Pinakes decides

The pattern repeats in every experiment: write the test down, build the instrument, prove the instrument can see a change, run it once, publish the number, let the number decide. Six rules recur in Pinakes' own documents.

| Rule | Pinakes says | Source |
|---|---|---|
| The pass criterion is fixed in writing before the number is known. | The metadata screen was pre-registered on 20260806 05:30, "before the screen has been run". Its criterion: "fixed in advance: proceed to 2e if the vector-only leg shows strictly more rank improvements than regressions". It adds "No p-value" and calls the criterion deliberately loose. Thresholds for later graph gates are committed as proposals: "A wrong number is arguable; no number is not." | [5][6] |
| Questions are written blind and frozen before the mechanism exists. | The 110-question set was "written by authors who had not read this repository, before any injection code existed". The 13 extra [multi-hop](../index/multi-hop-question-answering.md) questions were "authored from corpus structure and frozen before the probe ran". | [1] |
| Controls prove the instrument can see a change. | A null is trusted because both legs share one corpus hash, the injection reached the vectors (mean cosine 0.8398, none unchanged), and the uninjected index reproduced the frozen baseline 110 rows out of 110. Without the second control, "a silent no-op and a true null would have produced identical artifacts." | [1] |
| The cheap, reversible measurement runs before the expensive, irreversible change. | The reachability probe ran first: "The measurement was deliberately sequenced before the schema change", so no forced rebuild could land for a channel that might never be licensed. | [1] |
| Results are published when null, and the feature ships off. | The graph channel is "an eval-gated feature that is built, measured and off by construction". The metadata option ships with default `off`. An earlier pair of figures (19.0x and 16.5x) was withdrawn: "Those are withdrawn, not corrected." | [1][2] |
| Nothing is tuned after seeing a result. | "Nothing was tuned after seeing the number." The one graph leg that lifted anything was "reported, never gated". | [1][2] |

Two habits sit beside the rules. When a headline number moves, Pinakes says why: "Twice now the headline numbers have moved without retrieval changing." [1] And a defect in a measuring tool is published: one defect in the deep-loop report tool moved a published figure from 29.75x to 4.40x at exit 0 until it was fixed [1].

## Every measured experiment

Ordered as in the experiments notebook, not strictly by date (rows 12 and 13 are dated before row 11). All numbers are Pinakes' own. "Synthetic" means a corpus written for testing; the "RFC corpus" is the 300-document set of real standards documents Pinakes' author published in a separate repository [1][19].

| # | Date | Question | Result | Decision | Source |
|---|---|---|---|---|---|
| 1 | 20260725 13:49 | How fast is in-memory [vector search](../index/vector-search.md)? | NumPy exact cosine over 50,000 vectors of 384 dimensions: 2.25 ms/query, 77 MB resident. Checked upstream the same day: `sqlite-vec` "is **not an ANN index**" (exhaustive search), so no tier searches in sublinear time. See [approximate nearest neighbour](../index/approximate-nearest-neighbour.md). | Only the NumPy tier is built; the `sqlite-vec` tier is deferred. | [1][3] |
| 2 | 20260729 03:17 | Does the paid PDF extractor read scanned pages, and does the free one? | Live API, `claude-opus-5`, synthetic scanned set (3 fixtures, 10 pages). Paid: 1.000 character recall, order fidelity and word coverage, 0.000 junk. Free path: 0.000 on all four. On text-layer twins the two were identical on 3 of 4 measures; on a bordered table the paid path reads order better (+0.119) and adds 29% junk. Run cost EUR 0.43 of a EUR 4.23 worst case. | Paid extraction shipped in 0.3.0. Kept in the open: measured on synthetic rasters, "not a substitute for a real 300-DPI scan of a degraded page". | [1][3][4] |
| 3 | 20260729 03:17 | Is the spend reservation accurate? | First live call over-reserved 11.5x (USD 0.3515 reserved, 0.0306 spent). `PROMPT_TOKENS` measured 571 against an estimate of 300, "wrong in the unsafe direction". Page cost about 1,574 tokens against a 6,000 ceiling. The refusal branch fired for real: one fixture refused twice, the other four extracted. | Prompt constant raised to 700. Page ceiling deliberately not lowered (synthetic rasters). | [1] |
| 4 | 20260729 03:36 | Do the hand-written API test fixtures match the real API? | Four branches re-recorded live for EUR 0.26. The authored bodies were right about control flow and wrong about the response shape in five ways (for example a refusal bills 1 output token, not 0). A sixth finding was a defect: the extractor discarded a refusal's structured reason. One open question, n=1 on one document: a refused retry may spend about EUR 0.04 per slice for nothing. | Fixtures now declare their provenance. The retry question was recorded, not acted on. | [1] |
| 5 | 20260801 00:35 | Can a question change its answer for reasons unrelated to retrieval? | Real `[light]` models: identical in all three comparisons (same index twice, incremental against rebuild, rebuild against from-scratch). A tie-heavy fake: 1 of 41 questions differed. Adding documents reordered tied entries in 500 of 500 random arrays. "The shipped models were reproducible, and only by luck." | Ordering made total on (document path, [chunk](../index/chunking.md) ordinal). No baseline rewritten. A gate and a cross-OS CI job now hold it. | [1] |
| 6 | 20260801 12:14 | Baseline quality on the synthetic demo KB | 74 questions, `[light]` models: recall@5 0.939, [MRR](../index/mean-reciprocal-rank.md) 0.881, [rerank](../index/reranking.md) precision 0.849, false-abstain 0.015. Per class: paraphrase 0.75, multi-hop 0.944, the rest 1.00. The earlier 41-question figures moved because the set grew and, before that, a scorer was fixed, not because retrieval changed. | "Nothing should be tuned against this corpus until it is larger"; this blocked the graph release for three days. | [1] |
| 7 | 20260801 12:14 | How often does the confidence heuristic wrongly sound sure? | False-confidence 0.25 (one no-answer question in four) on 8 no-answer questions, thresholds fitted on the same set. On the 110-question RFC set (row 11): 0.1429 over 14 no-answer questions, again fitted on the scoring set. | Published as a floor, not an estimate. | [1] |
| 8 | 20260804 08:00 | Is the synthetic corpus realistic enough for the graph work? Build one that is. | The RFC corpus: 300 documents, 106,806 chunks. 53.3% of documents (160/300) carry an authored link, against 27% and 29% in the two synthetic KBs. Worst out-degree 86 (one RFC updates 86 documents); median out-degree 1. Relation kinds: `updates` 296, `supersedes` 95. The prediction recorded beforehand (density above the 35% cap, perhaps the degree cap of 4) was right. | It falsified a design premise: "authored links are sparse, precious signal" is "half right". 106,806 chunks is also 2x past the NumPy tier's 50,000 threshold. | [1] |
| 9 | 20260804 08:00 | Does the chunker give each chunk a heading path on that corpus? | 0 of 106,806. The chunker chose by source type and never tried a heading grammar on plain text, so three of the seven edge kinds derived zero edges. The first diagnosis recorded was wrong and is corrected in the record. | Found silent. `pnk doctor` reports heading coverage (0.12.0); an opt-in `headings = "numbered"` setting shipped in 0.13.0. The published corpus manifest does not set it. | [1][2] |
| 10 | 20260804 | Can the graph gate be reached at all? | Needed: at least 7 failing multi-hop questions, at least 7 of them reachable within 2 hops without authored edges. Demo KB: 1 failing, 1 reachable. RFC corpus: 12 failing, 9 reachable without authored edges, 12 with. Dropping `co-located` costs 3, `shared-tag` 6 (disjoint, sum 9), `sibling` nothing. The 9 is a floor: no chunk had a heading path. | "So G3 starts" (decision 20260804 13:50). | [1] |
| 11 | 20260806 11:56 | Build a second question set on a corpus that can license a result. | RFCs 8600-8799: 195 documents, 43,353 chunks, 110 questions (32 lexical, 32 simple-lookup, 32 paraphrase, 14 no-answer). recall@5 0.9271, MRR 0.8767, rerank precision 0.8438, false-abstain 0.0104, false-confidence 0.1429. **Improvable pool 15** (11 paraphrase, 2 lexical, 2 simple-lookup). | Frozen. "not a claim that retrieval improved"; it exists to make the metadata test falsifiable. | [1] |
| 12 | 20260804 22:52 | **Does graph expansion earn a default-on?** | 20 multi-hop questions on the 106,806-chunk RFC index, exact one-sided sign test. `off` 7/20. `expand` 4/20 with or without authored edges: 0 improved, 3 regressed, p = 1.0000. Latency 2012 ms against 2051 ms per query (1.02x). | `expand` ships `off`. No weight moved, no threshold revisited. | [1] |
| 13 | 20260804 22:52 | Does "reachable" mean "retrieved"? | The probe called 9 failing questions reachable; the retrieval instrument lifted none. | A reachability precondition is "necessary and nowhere near sufficient". The result licenses neither [personalized PageRank](../index/personalized-pagerank.md) nor the `[ner]` extra. | [1][2] |
| 14 | 20260807 11:39 | **Is document metadata (title, heading path) retrieval context?** | 195 RFCs, 43,353 chunks. 110 blind questions, 96 answerable, rerank off, vector channel only: **6 improved, 6 regressed, 84 unchanged**. The pre-set criterion (strictly more improvements than regressions) was not met. Controls passed (see the rules above). | No-go. `schema_version` stays at 3; PDF layout heuristics and paid title inference stay unapproved. The option ships `off`. | [1][5] |
| 15 | 20260811 | Does a second KB template pass its gate? | Leg 3 fails: "every divergence in every admissible KB is a manifest value". Leg 2 fails too: the only owner-chosen divergences are two provider settings with one reason. How many KBs were examined is **unstated** in what I read. | No-go. The gate's own redirect was taken: `pnk init --backend` (0.22.0). | [2] |
| 16 | 20260821 | **How far above real spend is the deep loop's reservation?** | Live API, `claude-opus-5`, synthetic corpora, EUR 0.2131 of a EUR 5.1836 worst case. Over-reservation: `synthesis` (the common case) 29.75x (EUR 1.0500 reserved, 0.0353 spent, 5 runs of 1 call); `decomposition` (calibrated loop) 50.92x (2 runs); `unknown` (uncalibrated loop) 22.35x (2 runs). Output ceiling 8,000 tokens against a widest observed 660 over 22 calls (12.12x). | No ceiling lowered, because the corpus is synthetic. Released in 0.25.3. | [1] |
| 17 | 20260821 | Does `pnk ask --deep` work against the live API? | **No, and it never had.** Every `--deep` call got an HTTP 400 before billing: the request schemas used keywords the API does not accept. Cost to users EUR 0.00. Green tests missed it because every test used recorded fixtures. | Fixed in 0.25.1; a gate now checks the schemas against the documented unsupported keywords. | [1] |
| 18 | 20260825 | Is "arity requirement 3" (a conditional that fires "IF the ceiling is alarming") still live? | A decision brief measured parent-child edge rows per chunk: 3.80 on the 300 RFCs, 4.95 on Pinakes' own docs, and none of the 300 RFCs reaching the synthetic corpus's 53.42. The antecedent is false on every real corpus measured. This figure comes from a decision analysis, not from STATUS. | Closed; the owner took the recommendation on 20260825 18:16 UTC. | [7] |
| 19 | 20260904 | Are the project's written development rules followed? (process, not retrieval) | A framework audit found 9 followed, 5 broken, 12 not auditable. I read only the handover that quotes it. | Development paused for a process review; resumed 20261102. | [8][9] |

Two flags on the table. First, STATUS counts the `sibling` edges as "106 506 of the corpus's 107 411 non-transit structural edges" for the gate (row 12) and as "106 506 of 107 802 edges" for the probe (row 10), and does not say why the denominators differ [1]. Second, row 17: STATUS says the failure held for `--deep` calls "in 0.22.0 through 0.25.0", but its own release rows have `--deep` arriving in 0.24.0 (in 0.23.0 it was a usage error) [1]. I give no release count.

### Approved or gated, and not run

| Item | State, as recorded | Source |
|---|---|---|
| Re-run of the graph gate on a corpus that has sections | The owner took it on 20260825 18:16 as its own three-leg gate, "~2.4 h of free CPU", expected result "another null". ROADMAP, read now, still lists it as what "remains". I found no result in STATUS or ROADMAP, and the RFC corpus repository's last push is 20260804 13:49 UTC, so it holds no rebuild with heading paths. That is not proof the run never happened elsewhere. | [2][19] |
| Personalized PageRank channel and `[ner]` extra | Gates only, not scheduled, deliberately no implementation plan. Thresholds are proposals: "None is derived from a measurement". The PPR gate does not run on a corpus below the heading-coverage floor. | [2][6] |
| `sqlite-vec` tier | Deferred behind a written trigger: a KB that "is actually queried crosses ~50 000 chunks and its search latency is a felt problem". A manifest naming it is refused at load time. | [1][2] |

### What the experiments cannot show

- **One corpus family.** The metadata answer is "no", but only "through one channel, on one corpus"; the graph verdict is "the edge kinds that worked did not help this corpus", never "graph structure does not help" [1][2].
- **A degraded chunker under the graph test.** Three of seven edge kinds derived zero edges, so the arms measured "the value of size-slice adjacency on a corpus whose structural chunking had silently degraded" [1].
- **Two of the gate's four clauses could not fire.** The corpus manifest has `[retrieval.confidence]` commented out [1].
- **Little statistical room.** The improvable pool is 15 questions; the graph gate used 20 [1].
- **Vector channel only.** The metadata test never covered the lexical channel, and the screen's legs are "not committed", so the 6 / 6 / 84 cannot be re-derived from a committed file [5].
- **Synthetic corpora for money.** The deep-loop and extractor runs used synthetic material, "precisely the one that cannot contain the case a ceiling exists for" [3].
- **Age.** STATUS says to "re-measure and re-date these whenever retrieval or extraction changes" [1]. The newest measured result in the table is 20260821.

*Reading:* the record is unusually candid, and its value is the discipline, not the scores. Most verdicts are nulls on one corpus with a known defect, and Pinakes states that itself. The numbers support "this design did not help here", not "this design cannot help". The only large effects are about cost control and bugs found by running against the real API (rows 3, 4, 16, 17), not about retrieval quality.

## The public-datasets benchmark

A separate public repository, `pinakes-datasets-benchmark`, builds a Pinakes knowledge base from a public dataset that ships ground-truth evidence, asks every question and scores what comes back [12]. This chapter's decision record (D-15) says such benchmarks run there, not in this repository [22]. Its first dataset is [MultiHop-RAG](../datasets/multihop-rag.md) [18]; the dataset and its protocol are summarised in [the archive's benchmark note](../../pinakes/experiments/datasets-benchmark.md). Four run directories and three paired comparisons are kept there [23]. This section reports what the benchmark repository itself says, **first-party**, read at its `main` commit `caa195c` (committed 20261102 14:04 UTC) on 20261102 19:41 UTC. I re-checked the figures below against the committed run reports [13][14][15][16]. I did not re-run the benchmark.

| Item | Value | Source |
|---|---|---|
| Repository | Public; Apache-2.0 | [11] |
| Dataset | MultiHop-RAG, pinned to revision `71ac0d0bd1`: 609 English news articles, 2,556 questions with evidence in two to four articles, 301 of them "null" questions the corpus cannot answer. Dataset licence ODC-By 1.0; the dataset is fetched, not redistributed. Paper: Tang and Yang, 2024. | [12][13][17][18] |
| Pinakes under test | 0.32.8 from PyPI, defaults, installed-code hash `ad0db0547b7e`; a switch exists for `main` | [12][13] |
| Models | `BAAI/bge-small-en-v1.5` ([embedding](../index/embedding.md)) and `BAAI/bge-reranker-base` (rerank) through the `sentence-transformers` provider, pinned to Hub commits | [12][13] |
| Settings | 510-token chunks, 64 overlap, 50 [BM25](../index/bm25.md) and 50 vector candidates fused by [reciprocal rank fusion](../index/reciprocal-rank-fusion.md), best 20 reranked, 8 returned. Plain text is cut one paragraph per chunk: 609 articles become 28,748 chunks, median 38 tokens. | [12][13] |
| Run | 8,497 searches in all (base 2,556 plus filtered variants); Apple-silicon GPU; 3 workers | [13] |

### First full run

Run `20261030_1826-baseline-pypi-0.32.8`: 2,255 answerable and 301 null questions [13]. The headline is the strict measure, "every gold article found", because a multi-hop question needs all its evidence. Pinakes' own harness counts a hit when any one is found, which is the loose measure and is never the headline [12].

| Share of answerable questions where... | First 5 passages | First 8 (default of `pnk search`) | First 20 (the reranker's pool) |
|---|---|---|---|
| at least one gold article is found | 91.5% | 96.8% | not computed |
| **every** gold article is found | 33.8% | **43.4%** (95% interval 41.3 to 45.4) | 61.0% (58.9 to 63.0) |

- **By evidence needed**, every gold article in the first 8: two articles 67.1%, three 22.1%, four 7.4%. By type: comparison 60.3%, temporal 43.9%, inference 25.2% [13].
- **Where the rest go:** for 39.0% of answerable questions at least one gold article is missing from the whole pool of 20; for a further 17.6% all are in the pool but not all in the first 8 [12].
- **Telling null from answerable by the top rerank score:** [AUROC](../index/auroc.md) 0.944 (0.929 to 0.957). On the 18 null questions without wording tells: 0.945 (0.882 to 0.982), a small sample [13].
- **Confidence labels:** on the held-out half, a null question is labelled high-confidence 16.2% of the time (11.2 to 22.9, n=154), against 10.9% on the half the thresholds were fitted on [13].
- **Filters:** 5,941 filtered searches, none returned an article the filter excludes. The filters are oracles built from the gold articles' own metadata, so they test the machinery, not a user's choice. With an oracle filter, every gold article in the first 10 articles rose from 57.5% to 72.7% for a date window [12][13].
- **Metadata-prefix variant:** embedding each chunk's title does not help: first 8 passages 42.3% against 43.4% (79 questions gained, 104 lost, p = 0.0758), pool of 20 55.7% against 61.0% (71 gained, 191 lost, p < 0.0001). The variant also lowers `max_tokens` to 459, which re-splits 11 articles; setting those and the 48 questions that need them aside changes nothing [12][16].

### The same Pinakes on its other provider

Run `20261031_1646-baseline-fastembed-pypi-0.32.8` uses the same Pinakes code through the `fastembed` provider on CPU. It loads other model files for the same two names (a float16 export of the embedding model from a different Hub repository, and the reranker's own ONNX file) [14].

| | sentence-transformers (GPU) | fastembed (CPU) |
|---|---|---|
| every gold article in the first 8 passages | 43.4% | 43.3% |
| every gold article in the first 20 passages | 61.0% | 60.9% |
| AUROC, answerable against null | 0.944 | 0.944 |
| thresholds fitted (`low_below`, `high_above`) | 0.0124, 0.1565 | -4.3787, -1.6845 |

The two providers rank alike: paired on the same questions, fastembed found none that sentence-transformers missed and missed one it found (p = 1.0) [15]. The confidence thresholds do not transfer. Labelling fastembed's held-out scores with the other run's thresholds calls 90.3% of the null questions low-confidence and 26.7% of the answerable ones; the other way round, every question is labelled high [15]. Speed is not compared: CPU against GPU, and another job ran beside one run, so the README says not to read a ratio [12].

### Limits

- **Scope:** one dataset whose questions and answers a language model generated (per the dataset's paper); Pinakes 0.32.8 with defaults; one machine; nothing tuned [12][17].
- **Null questions are worded differently.** 144 of 301 (47.8%) mention a "letter", against 0 of 2,255 answerable; 184 (61.1%) contain "Considering the information", against 2; 211 (70.1%) name no news outlet, against 14 [17]. Hence the re-check on 18 null questions without these tells.
- **Not run:** the graph channel, the paid `--deep` loop, and a real switch of a knowledge base from one provider to the other with thresholds fitted by `pnk calibrate` [12].
- **No BM25-alone arm.** I searched the README, the dataset notes and the run reports for one and found none; the configurations directory holds `baseline`, `baseline-fastembed`, `metadata-prefix` and the model pins, all of them the full pipeline [12][24]. The benchmark therefore cannot say what the dense and rerank stages add over [BM25](../index/bm25.md).
- **A stale sentence.** The README says the `pnk doctor` change about pinning under `fastembed` is "in no release yet"; STATUS lists it in the 0.32.9 release. STATUS wins [1][12]. STATUS's command table still labels the same change "On `main`, unreleased (P1)", which its release row contradicts [1].

*Reading:* with the defaults, Pinakes' free search returns all the evidence for fewer than half of the multi-hop questions in the first eight passages, and "at least one" (96.8%) hides that. The paragraph-sized chunks are the likely cause the benchmark itself points to: 20 passages cover about 10 articles. This is one dataset and one machine, and it is not comparable with the RFC experiments above, which used a different corpus and instrument.

## The deep-loop pilot

The pilot ran `pnk ask --deep`, Pinakes' paid reasoning loop, on three frozen multi-hop questions. Its plan was written 20261031 16:06 UTC, before any paid call, and fixed everything that could be chosen after seeing a result [21]. The owner approved a total cap of EUR 10 (decision D-19) [22]. The record lives in this repository's archive ([the pilot record](../../pinakes/experiments/p4-deep-pilot.md)); the ledger and the transcripts are not committed, so I could not re-derive the spend figures [21].

| Item | Value |
|---|---|
| Software | `pinakes` 0.32.8 from PyPI, unmodified |
| Corpus | A scratch copy of the published RFC corpus (300 documents); index built fresh: 300 documents, 106,806 chunks |
| Questions | The first three, in file order, of the 20 questions in the corpus repository's `eval/multihop-questions.yaml`, authored 20260804 and frozen. I confirmed the file, the order and the three identifiers. |
| Budget | EUR 2.00 per operation, EUR 10.00 a day and a month |
| Calibration | None. Confidence reads `unknown`, so the loop has no early stop and ends at its round cap or the budget |
| Model | **unstated** in the pilot record |
| Rule | One question at a time; no question re-run to get a better answer; stop if one estimate exceeds EUR 2.00 |

### Results

"Found" in the free round 0 means at least one of the 8 returned passages comes from a listed evidence document, not that the passage holds the needed fact [21].

| Question | Free retrieval found | Estimate | Spend (calls) | Rounds | The question's parts that appear correctly in a printed answer (the pilot author's reading) |
|---|---|---|---|---|---|
| `http-rate-limit-status-code-provenance` | 2 of 3 evidence documents (RFC 2616 missing) | EUR 1.64 | EUR 0.0815 (6) | 3 of 3, at the cap | The document that added 429 (RFC 6585). The amended specification (RFC 2616): in no round. The other codes: 431 and 511, never 428. |
| `uri-ipv6-literal-bracket-lineage` | 3 of 3 | EUR 1.64 | EUR 0.0910 (6) | 3 of 3, at the cap | All three parts, spread over three printed blocks. No block holds all three, and the blocks disagree. |
| `sip-invite-2xx-retransmission-defect` | 2 of 2 | EUR 1.64 | EUR 0.1358 (6) | 3 of 3, at the cap | Both parts, in round 1. The free round 0 already held the abstract in its first passage. |

Total spend EUR 0.3084 from `pnk budget`, against EUR 4.92 of estimates (about one sixteenth) and 3.1% of the EUR 10 cap. Every run made 6 paid calls and used all 3 rounds [21]. Before the first answer, two confirmation prompts went unanswered (nothing was spent) and the first run failed with HTTP 401 on a malformed key file; that call cost EUR 0.0000 [21].

I checked the readings' RFC facts against the RFC Editor's text now. RFC 6585 carries `Updates: 2616` and defines 428, 429, 431 and 511. RFC 2616 contains neither "429" nor "Too Many Requests". RFC 3986 carries `Obsoletes: 2732, 2396, 1808` and defines `IP-literal` and `host`. RFC 2732 says it updates the generic syntax defined in RFC 2396. RFC 6026 updates RFC 3261, modifies the INVITE state machines and changes how unmatched responses are handled [20].

What the three runs do not show, in the pilot's own words: an accuracy rate, any comparison with the free path's 7 of 20 (row 12 used a different instrument and all 20 questions), whether calibration would stop the loop earlier or cheaper, or anything about the other 17 questions [21]. "If these three were representative", which three runs cannot show, twenty questions would cost about EUR 2.06; a larger run needs its own approval [21].

*Reading:* two findings survive the sample size. Without calibration the loop runs to its round cap whether or not an earlier round already answered: all three runs used 3 of 3 rounds. And the log prints one answer block per round without merging them, so the last block does not always hold what an earlier block found (questions 1 and 2). The cost is small against the estimate, but three questions on one corpus with an uncalibrated KB bound nothing about other runs. Whether the loop answers more of these questions than the free path is **unstated**: the pilot did not measure it.

## Sources

1. https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md : latest release 0.32.9, last reviewed 20261102 15:19; measured numbers, golden sets, reproducibility, realism corpus, graph gate and probe, metadata result, extractor and deep-loop runs, release rows (read 20261102 19:37 UTC)
2. https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md : what the graph gate settled, the sections re-run, the template release (second template, `sqlite-vec` trigger), staged gates, 0.22.0 (read 20261102 19:38 UTC)
3. https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md : NumPy tier and the `sqlite-vec` correction (section 3.1), scanned-PDF measurement and its synthetic-raster caveat (section 9) (read 20261102 19:38 UTC)
4. https://github.com/lucagattoni/pinakes/blob/main/docs/MEASUREMENT-RUN.md : extractor run, EUR 4.23 worst case (read 20261102 19:38 UTC)
5. https://github.com/lucagattoni/pinakes/blob/main/plans/20260805_1721-metadata-as-retrieval-context.md : the pre-registered criterion, the answer, the legs not committed (read 20261102 19:38 UTC)
6. https://github.com/lucagattoni/pinakes/blob/main/plans/20260804_1016-staged-channel-gates.md : thresholds committed as proposals; "A wrong number is arguable" (read 20261102 19:38 UTC)
7. https://github.com/lucagattoni/pinakes/blob/main/plans/20260825_1803-open-decisions.md : the arity census and the decisions taken 20260825 18:16 (read 20261102 19:38 UTC)
8. https://github.com/lucagattoni/pinakes/blob/main/plans/20260904_1027-development-paused-handover-and-evidence.md : the pause, the 9 / 5 / 12 audit, the note that development resumed (read 20261102 19:38 UTC)
9. https://github.com/lucagattoni/pinakes/commit/3a25b5d : "Lift the development pause", 20261102 (read 20261102 19:40 UTC)
10. https://github.com/lucagattoni/pinakes : repository metadata: public, default branch `main` at `d2f0d53`, committed 20261102 15:29 UTC (read 20261102 19:37 UTC)
11. https://github.com/lucagattoni/pinakes-datasets-benchmark : repository metadata: public, Apache-2.0; `main` at `caa195c`, committed 20261102 14:04 UTC (read 20261102 19:37 UTC)
12. https://github.com/lucagattoni/pinakes-datasets-benchmark/blob/caa195c/README.md : results, the other-provider comparison, limits, the measures, settings, choices, the `max_tokens = 459` requirement and the 11 re-split articles (read 20261102 20:14 UTC)
13. https://github.com/lucagattoni/pinakes-datasets-benchmark/blob/caa195c/runs/20261030_1826-baseline-pypi-0.32.8/report.md : every figure of the first full run, the run's pins and environment (read 20261102 19:41 UTC)
14. https://github.com/lucagattoni/pinakes-datasets-benchmark/blob/caa195c/runs/20261031_1646-baseline-fastembed-pypi-0.32.8/report.md : the fastembed run, its model files (read 20261102 19:41 UTC)
15. https://github.com/lucagattoni/pinakes-datasets-benchmark/blob/caa195c/runs/compare--20261030_1826-baseline-pypi-0.32.8--20261031_1646-baseline-fastembed-pypi-0.32.8.md : the paired provider comparison and the threshold-transfer table (read 20261102 19:42 UTC)
16. https://github.com/lucagattoni/pinakes-datasets-benchmark/blob/caa195c/runs/compare--20261030_1826-baseline-pypi-0.32.8--20261030_1910-metadata-prefix-pypi-0.32.8.md : the metadata-prefix paired comparison, its `max_tokens` row and the set-aside of 11 articles and 48 questions (read 20261102 20:14 UTC)
17. https://github.com/lucagattoni/pinakes-datasets-benchmark/blob/caa195c/datasets/multihop-rag/README.md : who generated the questions, how null questions differ, the dataset licence line (read 20261102 19:41 UTC)
18. https://arxiv.org/abs/2401.15391 : MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries, Tang and Yang, first version 20240127 (read 20261102 19:41 UTC)
19. https://github.com/lucagattoni/pinakes-corpus-rfc : the RFC corpus repository (public; last push 20260804 13:49 UTC) and its `eval/multihop-questions.yaml`: 20 questions, authored 20260804, frozen; the first three identifiers (read 20261102 19:39 UTC)
20. https://www.rfc-editor.org/rfc/rfc6585.txt , https://www.rfc-editor.org/rfc/rfc2616.txt , https://www.rfc-editor.org/rfc/rfc2732.txt , https://www.rfc-editor.org/rfc/rfc3986.txt , https://www.rfc-editor.org/rfc/rfc6026.txt : the header fields (`Updates`, `Obsoletes`) and sections cited in the pilot readings (read 20261102 20:14 UTC)
21. The deep-loop pilot's plan, ledger and transcripts (the ledger and transcripts are not committed) : plan, results, spend and readings; run times 20261031 to 20261101 as the page gives them (read 20261102 19:37 UTC, via the archive page `pinakes/experiments/p4-deep-pilot.md`)
22. The owner's decision record : D-15 (benchmark in its own repository), D-19 to D-21 (the pilot's cap, key handling, authorisation) (read 20261102 19:38 UTC, via the archive page `DECISIONS.md`)
23. https://github.com/lucagattoni/pinakes-datasets-benchmark/tree/caa195c/runs : directory listing: four run directories and three paired comparisons (read 20261102 19:39 UTC)
24. https://github.com/lucagattoni/pinakes-datasets-benchmark/tree/caa195c/configs : directory listing: `baseline`, `baseline-fastembed`, `metadata-prefix`, `models` (read 20261102 19:39 UTC)
