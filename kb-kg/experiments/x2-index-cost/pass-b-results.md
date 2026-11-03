# X2 pass B: results of stages A to C

Written 20261103 17:54 UTC. These are the numbers from the paid pilot's first three stages, run 20261103 between 16:12 and 17:50 UTC on OpenAI's
`gpt-6-luna` (reasoning off) through the metering gateway, with the key in a private file and the owner's yes (D-34). Stage D has **not**
run and needs its own yes. **Nothing here says which graph is better**: no quality was measured. My readings are kept apart, in the
last section. The plan is [`pass-b-plan.md`](pass-b-plan.md); the run log with stage A is in it. Every number below is in the
files under [`pass-b/`](pass-b): the gateway's record of every call ([`meter.jsonl`](pass-b/meter.jsonl), 687 records, no request or response
text), the driver's [`stage-report.json`](pass-b/stage-report.json), one result file per run (`B-r1-*.json`, `C-r1-*.json`,
`C-r2-*.json`), the three stage-A result files, and [`stage-totals.json`](pass-b/stage-totals.json), which the tables are built from. The
files passed the path, key, name, e-mail and copied-text scans (no run of eight words from the 20 articles) before they were copied here.

## What ran

| Stage | What | Chat requests answered | Spent (USD, the gateway's figure) | Limit |
|---|---|---|---|---|
| A | The key (refused at the first call, then replaced), ten requests, a re-test of two shapes through gateway 1.2.0, two refusal tests | 11 (14 reached OpenAI; 3 were rejected with no tokens: one 401, two 400) | 0.00646 | 0.10 |
| B | One document for each of the four builders | 56 | 0.03735 | 0.20 |
| C | Five documents for each builder, **twice** (runs r1 and r2) | 376 | 0.21952 | 0.60 |
| **A to C** | | 443 | **0.26333** | 3.00 for the whole pilot |

Every run ended `completed` with runner exit status 0; the watchdog tripped none of its rules; no process was left behind; every
answer of stages B and C returned HTTP 200 and ended with finish reason `stop` (none by the output limit); every one reported 0 reasoning
tokens; no 429 or 5xx came back from OpenAI. The embedding calls (the local `qwen3-embedding:0.6b`) are not billed and not in these
counts. Run times are on the driver's clock and include starting the gateway.

## Stage B: one document

| Builder | Chat calls | Input tokens (cached) | Output tokens | USD | The plan's estimate | Seconds | What the builder stored |
|---|---|---|---|---|---|---|---|
| LightRAG | 4 | 14,872 (5,032) | 5,908 | 0.00399 | 0.0031 | 36 | 61 entities, 67 relationships |
| fast-graphrag | 3 | 6,810 (3,268) | 7,135 | 0.00395 | 0.0042 | 28 | 56 entities, 103 relations |
| Microsoft GraphRAG | 24 | 40,669 (4,921) | 14,100 | 0.01067 | 0.0158 | 84 | 57 entities, 74 relationships, 9 communities |
| nano-graphrag | 25 | 65,889 (5,347) | 25,247 | 0.01873 | 0.0069 | 122 | 84 nodes, 106 edges, 21 communities |
| **All four** | 56 | 128,240 (18,568) | 52,390 | 0.03735 | 0.0300 | | |

## Stage C: five documents, twice

| Builder | Run | Chat calls | Input tokens (cached) | Output tokens | USD | USD per document | The plan's estimate | Seconds | What the builder stored |
|---|---|---|---|---|---|---|---|---|---|
| LightRAG | r1 | 18 | 65,285 (39,177) | 24,485 | 0.01525 | 0.00305 | 0.0188 | 150 | 281 entities, 278 relationships |
| LightRAG | r2 | 18 | 65,941 (46,870) | 23,223 | 0.01399 | 0.00280 | 0.0188 | 141 | 248 entities, 232 relationships |
| fast-graphrag | r1 | 15 | 34,134 (26,409) | 31,645 | 0.01686 | 0.00337 | 0.0150 | 117 | 251 entities, 447 relations |
| fast-graphrag | r2 | 15 | 34,134 (34,089) | 32,118 | 0.01640 | 0.00328 | 0.0150 | 110 | 266 entities, 473 relations |
| Microsoft GraphRAG | r1 | 113 | 123,319 (27,854) | 43,042 | 0.03135 | 0.00627 | 0.0458 | 154 | 216 entities, 310 relationships, 18 communities |
| Microsoft GraphRAG | r2 | 65 | 95,755 (45,866) | 35,038 | 0.02297 | 0.00459 | 0.0458 | 125 | 198 entities, 251 relationships, 10 communities |
| nano-graphrag | r1 | 62 | 182,869 (30,197) | 69,037 | 0.05009 | 0.01002 | 0.0379 | 309 | 293 nodes, 386 edges, 26 communities |
| nano-graphrag | r2 | 70 | 199,473 (49,700) | 74,306 | 0.05263 | 0.01053 | 0.0379 | 340 | 282 nodes, 382 edges, 34 communities |
| **r1, all four** | | 208 | | | 0.11354 | | 0.1175 | | |
| **r2, all four** | | 168 | | | 0.10599 | | 0.1175 | | |

The same five documents were used in both runs, and r2 followed r1 within minutes. **The
two runs are not independent for cost**: r2 repeated r1's prompts, and OpenAI billed more of r2's input at the cached rate (below).

### Run 1 to run 2

| Builder | Chat calls | Output tokens | USD | Cached share of input |
|---|---|---|---|---|
| LightRAG | 18 to 18 | 24,485 to 23,223 | 0.01525 to 0.01399 | 60% to 71% |
| fast-graphrag | 15 to 15 | 31,645 to 32,118 | 0.01686 to 0.01640 | 77% to 100% |
| Microsoft GraphRAG | 113 to 65 | 43,042 to 35,038 | 0.03135 to 0.02297 | 23% to 48% |
| nano-graphrag | 62 to 70 | 69,037 to 74,306 | 0.05009 to 0.05263 | 17% to 25% |

## What the numbers are set against

- **The plan's estimates** (arithmetic from pass A's local tokens, at luna's prices): stage B 0.030 against 0.0373 actual; stage C 0.1175
  a run against 0.1135 and 0.1060. Per builder the ratios of actual to estimate run from 0.50 to 2.70: LightRAG 1.28 (B), 0.81 and 0.74 (C);
  fast-graphrag 0.94, 1.13 and 1.10; Microsoft GraphRAG 0.68, 0.68 and 0.50; nano-graphrag 2.70, 1.32 and 1.39. nano-graphrag's estimate was
  a guess, because pass A's local model never got past its first document.
- **Pass A at five documents** (`granite4.2:8b`, local; the committed result files), chat calls, input tokens, output tokens, against the
  hosted run r1: LightRAG 18, 66,543, 24,290 against 18, 65,285, 24,485. fast-graphrag 18, 52,264, 19,457 against 15, 34,134, 31,645.
  Microsoft GraphRAG 91, 107,005, 70,204 against 113, 123,319, 43,042. nano-graphrag had no five-document local run.
- **Cost without the cache discount**: the same tokens at the full input price of USD 0.10 per million would have cost, for r1, LightRAG
  0.01877, fast-graphrag 0.01924, Microsoft GraphRAG 0.03385, nano-graphrag 0.05281 (the actual costs are in the table above).
- **Output tokens carry the bill**: at USD 0.50 against 0.10 per million, output tokens were between 66% (stage B, Microsoft GraphRAG) and
  98% (r2, fast-graphrag) of each run's cost.

## What did and did not happen

- **The labelled departure** (gateway 1.2.0 drops a null `max_tokens` and sends a set one as `max_completion_tokens`, D-35) was
  **never exercised** in these 12 runs: no call of any run had either field. It was exercised only in stage A's re-test. The two builders'
  summary calls that use it need longer descriptions than five documents produce; stage D may reach them.
- **Builder-side signals**: LightRAG logged 1 "LLM output format error" warning in r1 and 21 in r2 (18 of them about relation fields), and
  stored 281 entities and 278 relationships in r1 against 248 and 232 in r2. Microsoft GraphRAG found 18 communities in r1 and 10 in r2
  (18 and 10 community reports), with 113 and 65 chat calls in all; fast-graphrag and nano-graphrag logged no failure and no retry.
- **Repeated identical requests** inside a run: 0 in every one of the 12 runs, counted again from the ledger (the repeat rule would have
  stopped a run above 5%); the second run of stage C repeats the first run's requests by design, and the window fix of 20261102 is what let it run.
- **No provider error, no refusal by the gateway and no voided call** in any of the 12 runs: every record of every run is HTTP 200, from the ledger.

## For the console comparison (the owner's)

The plan compares OpenAI's usage page with the gateway at the end of each stage. Stage A agreed on 20261103 (recorded in the run log).
The figures for the hosted calls (embeddings are local and not on that page), from the ledger:

| | Requests answered | Input tokens (cached) | Output tokens | USD |
|---|---|---|---|---|
| A (agreed) | 11 | 16,945 (2,043) | 9,893 | 0.00645713 |
| B | 56 | 128,240 (18,568) | 52,390 | 0.03734788 |
| C | 376 | 800,910 (300,162) | 332,894 | 0.21952342 |
| **A to C** | 443 | 946,095 (320,773) | 395,177 | **0.26332843** |

## Arithmetic for stage D (not a measurement)

Stage D is 20 documents; the 20 hold 191,571 characters against 32,458 in the first five (a factor of 5.90, the plan's). Scaling the
five-document cost by 5.90: r1 gives LightRAG 0.090, fast-graphrag 0.099, Microsoft GraphRAG 0.185, nano-graphrag 0.296, **0.670 in all**;
the mean of r1 and r2 gives 0.648. The plan's central estimate was 0.625 and its limit 1.50. This assumes cost grows with characters;
the graph builders' community steps may grow faster, and stage D is where that would show. The dry run of the driver for stage D passes the pre-flight with an
allowance of USD 1.50 for the first builder, a cap for the gateway of 1.763 and 2.74 left of the pilot's 3.00. If D is run, its cost
would be the largest single spend of the pilot, and it needs the owner's yes.

## My readings (kept apart from the numbers)

1. **At five documents nano-graphrag cost about 3.5 times LightRAG per document** (0.0103 against 0.0029, the mean of the two runs),
   Microsoft GraphRAG about 1.9 times and fast-graphrag about 1.1 times. Most of nano-graphrag's and Microsoft GraphRAG's calls are
   community reports (nano-graphrag: 44 of 62 chat calls in r1 and 52 of 70 in r2).
2. **The input side is cheap here and the output side is not**, because of the cache and the 5-to-1 price ratio; so the ranking of the
   builders by cost follows their output tokens. A cheaper-output model or one with no caching would rank them differently.
3. **A single run can mislead for Microsoft GraphRAG**: the same five documents gave 113 and 65 chat calls. Part of its r2 saving is the
   provider's cache and part is a different community structure; I cannot separate them from these runs.
4. **Pass A's local token counts were a usable guide for LightRAG** (nearly equal) and **within about a factor of 1.6 for fast-graphrag
   and Microsoft GraphRAG**, in both directions, which is what the plan said they could do: bracket.
5. **The plan's total for stage C was close (within 10%) because two errors cancelled** (Microsoft GraphRAG over-estimated, nano-graphrag
   under-estimated). The per-builder estimates were not reliable.
6. **Corpus-scale arithmetic**, for the headline only: the mean five-document cost times the 609 articles gives about USD 1.78 for LightRAG,
   2.03 for fast-graphrag, 3.31 for Microsoft GraphRAG and 6.26 for nano-graphrag. Linear growth is an assumption stage D is meant to test.

## What this cannot show

Quality of any graph. A second model or provider. Behaviour at 20 documents or at corpus scale (stage D, if the owner says yes). Whether the
labelled departure changes what fast-graphrag and nano-graphrag do (it was not used). OpenAI's rate limits (no 429 appeared at concurrency 4;
the account's tier is unstated). The effect of the provider's prompt cache on a fresh account (r2's input was cached because r1 had just run).
Two runs are two runs: the spread between them says little about the spread of a third.
