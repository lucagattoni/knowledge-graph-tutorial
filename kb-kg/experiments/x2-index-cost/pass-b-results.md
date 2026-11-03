# X2 pass B: results of stages A to D

Written 20261103 19:44 UTC. These are the numbers from the paid pilot's four stages, run 20261103 between 16:12 and 19:01 UTC on OpenAI's
`gpt-6-luna` (reasoning off) through the metering gateway, with the key in a private file and the owner's yes (D-34 for stages A to C,
D-37 for stage D). **The pilot has run to its end**: the spend is far below its USD 3.00 cap, nothing more is approved, and D-37 does not
cover a repeat of D. **Nothing here says which graph is better**: no quality was measured. My readings are kept apart, in the last
section. The plan is [`pass-b-plan.md`](pass-b-plan.md); the run log with stage A is in it. Every number below is in the files under
[`pass-b/`](pass-b): the gateway's record of every call ([`meter.jsonl`](pass-b/meter.jsonl), 2,510 records, no request or response
text), the driver's [`stage-report.json`](pass-b/stage-report.json), one result file per run (`B-r1-*.json`, `C-r1-*.json`, `C-r2-*.json`,
`D-r1-*.json`), the three stage-A result files, and [`stage-totals.json`](pass-b/stage-totals.json), which the tables are built from. The
files passed the path, key, name, e-mail and copied-text scans (no run of eight words from the 20 articles) before they were copied here.

## One correction first: the gateway left out OpenAI's cache-write price

Every answer of OpenAI carried `usage.prompt_tokens_details.cache_write_tokens` beside `cached_tokens`, and the gateway read only the second:
version 1.2.0, which ran stages B to D and stage A's re-test, and the 1.1.0 code of stage A's first two runs (by the plan's file times they came
before the 1.2.0 change; neither version read the field, so no figure differs). It priced the written tokens as plain input, USD 0.10 per million, where OpenAI's model page says
"Cache writes are billed at 1.25x the uncached input token rate", USD 0.125 (page and prompt-caching guide read 20261103; the sources are in
[the gateway's page](../../../tools/metering_gateway.md#where-the-usage-field-names-come-from)). I found it while building stage D's tables, after
the run; the stage-A check "the gateway's cost recomputed from the tokens equals its own" could not show it, because it used the same
fields. Version 1.3.0 of the gateway reads the field. The pilot was **not** re-run: the gateway's figures stay in the ledger as run, and the
tables below give them first, with the price of the written tokens added from the answers' own token counts where a column says so. The
price itself was configured (0.125 in the run profile) but the gateway applied a cache-write price only to Anthropic usage, so it was set and
unused. **The written-token counts are not in the repository's ledger**: `cache_creation_input_tokens` is null in all 2,510 records of
[`meter.jsonl`](pass-b/meter.jsonl), because 1.2.0 did not read the field; the counts come from the gateway's body log, which is outside the
repository, and are summed per run in [`stage-totals.json`](pass-b/stage-totals.json), so they cannot be re-derived from the committed files.

| Stage | Tokens OpenAI reported as written to its cache | The gateway's total (USD) | With the cache-write price (USD) | Difference |
|---|---|---|---|---|
| A | 14,358 | 0.00646 | 0.00682 | 0.00036 |
| B | 107,540 | 0.03735 | 0.04004 | 0.00269 |
| C (both runs) | 478,111 | 0.21952 | 0.23148 | 0.01195 |
| D | 2,540,573 | 0.84204 | 0.90556 | 0.06351 |
| **A to D** | 3,140,582 | **1.10537** | **1.18389** | 0.07851 (7.1% of the gateway's total) |

Which figure holds is for OpenAI's usage page to say: the owner's comparison for stage D (below) will show which of the two it matches, if either. **The earlier
"Agrees" of the owner, for stage A and for stages B and C, was given against the gateway's figures**; I do not know whether those
comparisons covered dollars to the cent or tokens, so they neither confirm nor exclude the write price (it adds 0.01500 to
the 0.26333 of stages A to C). The price is for the default 30-minute lifetime; OpenAI's 12-hour option costs twice as
much, and the pilot's requests did not ask for it (the body log's request keys are `model`, `messages`, `response_format` and, in 17
requests, `max_tokens`). Neither the stop-at and allowance of USD 1.50 nor the cap of USD 3.00 was ever close on either figure.
The ratios between builders move by a few per cent (D: nano-graphrag is 5.27 times LightRAG on the gateway's figures and
5.48 with the write price); the order does not change.

## What ran

| Stage | What | Chat requests answered | The gateway's total (USD) | With the cache-write price (USD) | Limit (USD) |
|---|---|---|---|---|---|
| A | The key (refused at the first call, then replaced), ten requests, a re-test of two shapes through gateway 1.2.0, two refusal tests | 11 (14 reached OpenAI; 3 were rejected with no tokens: one 401, two 400) | 0.00646 | 0.00682 | 0.10 |
| B | One document for each of the four builders | 56 | 0.03735 | 0.04004 | 0.20 |
| C | Five documents for each builder, **twice** (runs r1 and r2) | 376 | 0.21952 | 0.23148 | 0.60 |
| D | Twenty documents for each builder, one run each | 1,308 | 0.84204 | 0.90556 | 1.50 |
| **A to D** | | 1,751 | **1.10537** | **1.18389** | 3.00 for the whole pilot |

Every run of stages B to D (16) ended `completed` with runner exit status 0; the watchdog tripped none of its rules; no process was left
behind; every answer of stages B to D returned HTTP 200 and ended with finish reason `stop` (none by the output limit); every one reported 0
reasoning tokens; no 429 or 5xx came back from OpenAI. The embedding calls (the local `qwen3-embedding:0.6b`) are not billed and not in
these counts. Run times are on the driver's clock and include starting the gateway.

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

## Stage D: twenty documents, one run each

The 20 documents hold 191,571 characters, against 32,458 in the first five (a factor of 5.90, the plan's). One run each, so nothing
here shows the spread between runs; stage C showed Microsoft GraphRAG making 113 calls in one run and 65 in the next on the same five
documents. In the input column, the first bracketed figure is the tokens OpenAI billed at the cached (read) rate and the second the tokens
it reported as written to its cache.

| Builder | Chat calls | Input tokens (read from cache; written) | Output tokens | USD, the gateway | USD, with the cache-write price | USD per document (gateway) | Seconds | What the builder stored |
|---|---|---|---|---|---|---|---|---|
| LightRAG | 99 | 373,403 (216,836; 155,632) | 131,698 | 0.08367 | 0.08756 | 0.00418 | 603 | 1,333 entities, 1,355 relationships |
| fast-graphrag | 96 | 193,540 (140,299; 47,187) | 160,321 | 0.08689 | 0.08807 | 0.00434 | 500 | 1,243 entities, 2,292 relations |
| Microsoft GraphRAG | 558 | 938,420 (125,920; 760,180) | 296,662 | 0.23084 | 0.24984 | 0.01154 | 885 | 1,116 entities, 1,434 relationships, 199 communities |
| nano-graphrag | 555 | 1,719,132 (139,893; 1,577,574) | 562,640 | 0.44064 | 0.48008 | 0.02203 | 1827 | 1,328 nodes, 1,584 edges, 237 communities |
| **All four** | 1,308 | 3,224,495 (622,948; 2,540,573) | 1,151,321 | 0.84204 | 0.90556 | | | |

### Stage D against the arithmetic from stage C

The arithmetic took the mean of C's two runs for each builder and multiplied by 5.90 (it was quoted for the owner's yes as about USD 0.65, in a
range of 0.61 to 0.69). The plan's central estimates are from before any paid run. Costs here are the gateway's.

| Builder | Actual | Arithmetic from C | Actual / arithmetic | The plan's estimate | Actual / plan |
|---|---|---|---|---|---|
| LightRAG | 0.0837 | 0.0862 | 0.97 | 0.108 | 0.77 |
| fast-graphrag | 0.0869 | 0.0981 | 0.89 | 0.095 | 0.91 |
| Microsoft GraphRAG | 0.2308 | 0.1602 | 1.44 | 0.270 | 0.85 |
| nano-graphrag | 0.4406 | 0.3030 | 1.45 | 0.152 | 2.90 |
| **All four** | 0.8420 | 0.6476 | 1.30 | 0.625 | 1.35 |

### Cost per document and per 1,000 characters, C against D

A builder whose cost grows with the text should show the same cost per 1,000 characters at five and at twenty documents (C: the mean of the two
runs; the gateway's figures).

| Builder | USD per document, C | USD per document, D | D / C | USD per 1,000 characters, C | USD per 1,000 characters, D | D / C |
|---|---|---|---|---|---|---|
| LightRAG | 0.00292 | 0.00418 | 1.43 | 0.000450 | 0.000437 | 0.97 |
| fast-graphrag | 0.00333 | 0.00434 | 1.31 | 0.000512 | 0.000454 | 0.89 |
| Microsoft GraphRAG | 0.00543 | 0.01154 | 2.13 | 0.000837 | 0.001205 | 1.44 |
| nano-graphrag | 0.01027 | 0.02203 | 2.14 | 0.001582 | 0.002300 | 1.45 |

### Where stage D's chat calls went (from the runners' own call classification)

- **fast-graphrag**: 80 extraction calls, 13 description summaries, 3 edge groupings (96; the 13 summaries are the 13 that used the labelled
  translation, below).
- **Microsoft GraphRAG**: 199 community reports, 188 entity-description and 76 relationship-description summaries, 47 graph extractions and
  47 gleaning continuations (557, and the pre-flight connectivity test: 558).
- **nano-graphrag**: 457 community reports, 49 entity extractions and 49 gleaning continuations (555).
- **LightRAG**: 99 chat calls for 49 chunks.

## What the numbers are set against

- **The plan's estimates** (arithmetic from pass A's local tokens, at luna's prices): stage B 0.030 against 0.0373 actual; stage C 0.1175
  a run against 0.1135 and 0.1060; stage D 0.625 against 0.842. Per builder the ratios of actual to estimate run from 0.50 to 2.90: LightRAG
  1.28 (B), 0.81 and 0.74 (C), 0.77 (D); fast-graphrag 0.94, 1.13 and 1.10, 0.91; Microsoft GraphRAG 0.68, 0.68 and 0.50, 0.85; nano-graphrag
  2.70, 1.32 and 1.39, 2.90 (the ratios use the unrounded estimates the dry runs print to six places; the tables show four, so a ratio
  worked out from them can differ in the second decimal). nano-graphrag's estimate was a guess, because pass A's local model never got
  past its first document. The estimates priced all input at USD 0.10; OpenAI's implicit caching bills most fresh input as a write (below).
- **Pass A (`granite4.2:8b`, local; the committed result files), chat calls, input tokens, output tokens, against the hosted run**: at five
  documents LightRAG 18, 66,543, 24,290 against 18, 65,285, 24,485 (r1); fast-graphrag 18, 52,264, 19,457 against 15, 34,134, 31,645;
  Microsoft GraphRAG 91, 107,005, 70,204 against 113, 123,319, 43,042. At twenty documents LightRAG 100, 401,109, 135,391 against 99,
  373,403, 131,698. The committed pass-A files have checkpoints at 1, 5 and 20 documents for LightRAG, at 1, 5 and 14 for fast-graphrag, at 1
  and 5 for Microsoft GraphRAG and none for nano-graphrag.
- **What fills the input**: of stage D's input tokens, OpenAI billed as cache reads 58% (LightRAG),
  72% (fast-graphrag), 13% (Microsoft GraphRAG) and 8% (nano-graphrag), and reported as cache writes
  42%, 24%, 81% and 92%. Reads and writes together are 94% to 100% of the input, so almost no input was
  billed at the plain rate.
- **Output tokens carry the bill**: at USD 0.50 against 0.10 per million, output tokens were between 64% (D-r1-nano) and
  98% (C-r2-fast) of each run's cost on the gateway's figures.

## What did and did not happen

- **The labelled departure** (gateway 1.2.0 drops a null `max_tokens` and sends a set one as `max_completion_tokens`, D-35) was
  **never exercised in stages B and C**: no call of those 12 runs had either field. **In stage D it was, by one builder**: all 13 of
  fast-graphrag's description-summary requests carried `max_tokens: null`, the gateway dropped it, and OpenAI answered each with 200 and
  finish `stop`. No other builder's request used it, and no set `max_tokens` was renamed in stages B to D (that happened once, in
  stage A's re-test). The translation is therefore a departure from what fast-graphrag asks for in 13 of its 96 stage-D requests.
- **Builder-side signals**: LightRAG logged 110 warnings in stage D: 97 "LLM output format error" (81 "found #/# fields on RELATION", 4 on
  ENTITY, 12 "find LLM use <|#|> as record s…"), 3 "Complete delimiter can not be found" and 10 "Recovering mis-prefixed relation" (the runner
  keeps the first 80 characters of each message), against 1 and 21 warnings, all format errors, in stage C's two runs; it stored 1333 entities and 1355 relationships. Microsoft GraphRAG found
  199 communities (18 and 10 at five documents) and wrote 199 community reports; nano-graphrag stored 237 community
  reports for 457 community-report calls (26 and 34 for 44 and 52 calls in stage C). fast-graphrag logged no error line and no SDK retry; its
  library logged that it could not load a tokenizer for `gpt-6-luna` and falls back to a naive one (the runner found, by grep of the pinned
  source, that nothing on the indexing path calls it). nano-graphrag logged no warning.
- **Repeated identical requests** inside a run: 0 in every one of the 16 runs, counted again from the ledger (the repeat rule would have
  stopped a run above 5%); the second run of stage C repeats the first run's requests by design, and the window fix of 20261102 is what let it run.
- **No provider error, no refusal by the gateway and no voided call** in any of the 16 runs: every record of every run is HTTP 200, from the ledger.
- **No usage figure was missing**, and in no answer did cache reads plus cache writes exceed the prompt tokens (checked on all 1,751 answered requests).

## For the console comparison (the owner's)

The plan compares OpenAI's usage page with the gateway at the end of each stage. Stage A agreed on 20261103 (recorded in the run log),
and so did stages B and C together (recorded in the plan's run log; against the gateway's figures). **Stage D is the one still to compare**,
and it is the first comparison in which the cache-write price can be told apart: the two figures differ by 0.0635. The figures for the
hosted calls (embeddings are local and not on that page), from the ledger and the answers' own usage:

| | Requests answered | Input tokens (cached; written) | Output tokens | USD, the gateway | USD, with the cache-write price |
|---|---|---|---|---|---|
| A (agreed) | 11 | 16,945 (2,043; 14,358) | 9,893 | 0.00645713 | 0.00681608 |
| B and C (agreed) | 432 | 929,150 (318,730; 585,651) | 385,284 | 0.25687130 | 0.271512575 |
| D (to compare) | 1,308 | 3,224,495 (622,948; 2,540,573) | 1,151,321 | 0.84204468 | 0.905559005 |
| **A to D** | 1,751 | 4,170,590 (943,721; 3,140,582) | 1,546,498 | **1.10537311** | **1.183887660** |

## Corpus-scale arithmetic (not a measurement)

The 609 articles of the corpus hold 6,297,171 characters, 32.87 times the 20 documents of stage D and 194.0 times stage C's five. Scaling a
cost by characters, at this model's prices and with the cache behaviour seen here (USD for the whole corpus, one build):

| Builder | From stage C (mean of two runs) | From stage D, the gateway's figure | From stage D, with the cache-write price |
|---|---|---|---|
| LightRAG | 2.84 | 2.75 | 2.88 |
| fast-graphrag | 3.23 | 2.86 | 2.89 |
| Microsoft GraphRAG | 5.27 | 7.59 | 8.21 |
| nano-graphrag | 9.96 | 14.48 | 15.78 |
| **All four** | 21.29 | 27.68 | 29.77 |

(The stage-C column is the arithmetic of the earlier version of this page done by characters directly; it differs from that version in the
second decimal.) It assumes cost grows linearly with characters. Stage D's table above shows that this held between five and twenty documents
for LightRAG and fast-graphrag and did not for Microsoft GraphRAG and nano-graphrag; if the rise in their cost per character between five and
twenty documents continues, the stage-D column is too low for those two. Nothing here says whether it does.

## My readings (kept apart from the numbers)

1. **The gap between the builders widened with scale.** At five documents nano-graphrag cost about 3.5 times LightRAG per document (the mean of the
   two runs), Microsoft GraphRAG about 1.9 times and fast-graphrag about 1.1 times; at twenty, 5.3, 2.8 and
   1.04 (with the cache-write price 5.5, 2.9, 1.01). Most of nano-graphrag's
   chat calls are community reports (44 of 62 in C r1, 52 of 70 in r2, 457 of 555 in D); most of Microsoft GraphRAG's were entity and relationship
   description summaries in C (76 of 113 in r1, 36 of 65 in r2), and in D 264 of 558 were description summaries and 199 community reports.
2. **Linear growth in characters held for two builders and not for the other two.** Cost per 1,000 characters at twenty documents was 0.97 times
   its value at five for LightRAG and 0.89 times for fast-graphrag, and 1.44 and 1.45 times for Microsoft GraphRAG and nano-graphrag. The number
   of communities, and so of community reports, grew faster than the text (Microsoft GraphRAG: 199 communities in 20 documents against 18 and 10 in
   five; nano-graphrag: 237 stored against 26 and 34). Whether that keeps growing, levels off or accelerates at 609 articles these runs cannot say.
3. **The arithmetic from stage C understated stage D by 1.30 times**, 0.842 against 0.648: inside the limit of USD 1.50 (56% of it) but above the range
   quoted for the owner's yes (0.61 to 0.69). It was close for the two flat builders (the actual cost was 0.97 and 0.89 of it) and about 1.45 times low for the other two. The plan's
   central estimate (0.625) was low by 1.35 times in total, and 2.9 times for nano-graphrag.
4. **Almost all input was billed as a cache read or a cache write.** With reads at USD 0.01 and writes at 0.125 per million, the price of
   fresh input was the write price, not the 0.10 the plan used. The share read from the cache was 58% and 72% for LightRAG and fast-graphrag and
   13% and 8% for Microsoft GraphRAG and nano-graphrag, whose input was 81% and 92% written; why they differ these runs do not show. A
   cheaper-output model, or one with no caching, would rank the builders differently.
5. **The input side is cheap here and the output side is not**, so the ranking of the builders by cost follows their output tokens.
6. **A single run can mislead for Microsoft GraphRAG**: the same five documents gave 113 and 65 chat calls. Part of its C r2 saving is the
   provider's cache and part is a different community structure; I cannot separate them from these runs. Stage D is a single run for each builder.
7. **Pass A's local token counts were a usable guide for LightRAG** (nearly equal at five documents and within 8% at twenty: 100 calls and
   401,109 input tokens against 99 and 373,403) **and within about a factor of 1.6 for fast-graphrag and Microsoft GraphRAG at five**, in both
   directions, which is what the plan said they could do: bracket.
8. **The plan's total for stage C was close (within 10%) because two errors cancelled** (Microsoft GraphRAG over-estimated, nano-graphrag
   under-estimated). The per-builder estimates were not reliable, and stage D's total was not close.
9. **Time**: on the driver's clock nano-graphrag needed 30.4 minutes for the 20 documents, Microsoft GraphRAG 14.8, LightRAG 10.1 and fast-graphrag 8.3.

## What this cannot show

Quality of any graph. A second model or provider. A repeat of stage D, or its run-to-run spread. Behaviour at corpus scale (609 articles) or whether
the community steps keep growing. Whether OpenAI's bill includes the cache-write price (the console decides, above). OpenAI's rate limits (no 429
appeared at concurrency 4; the account's tier is unstated). How much of the cache behaviour belongs to a fresh account and to runs that
followed each other within minutes. Two runs (C) and one run (D) are small samples.
