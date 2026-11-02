# X2 pass B: a plan for the paid pilot

**Plan written 20261102 20:24 UTC and revised at 20:39 UTC after an independent review (the changes are listed at the end). No paid
call has been made, nothing is approved, nothing has been spent.** The owner asked for this plan ("Plan paid pilot") after
[pass A](pass-a-local-model.md). Under D-14 a paid step starts only on the owner's explicit yes with model, provider and cap; this
page says what that yes would unlock, what is fixed in advance, and what has to be built and checked for free first. Everything that
could be chosen after seeing a result is fixed here instead.

**Decided so far (owner, 20261102 20:49 UTC, reply "gpt-6-luna, USD 3"):** decision 1, OpenAI `gpt-6-luna` with reasoning off, and
decision 2, a cap of USD 3 in total with the stage limits below. **Still open:** 3 (article text to the provider), 4 (embeddings), 5
(builders), 6 (a new key and a hard provider-side limit), 7 (one yes or two). Recommended answers stand as written. This is not yet the
yes that starts a paid stage: stage A needs 3 and 6 answered and the free work (stage 0) done. Stage 0 has started; progress is in
[`RESUME.md`](../../../RESUME.md).

## What pass B answers, and what it does not

**Question.** What does it cost, in calls, tokens and money, to build a graph for the same 20 documents with each cheap builder on
one hosted small model, on each builder's own defaults (except the departures listed below)? Pass A measured tokens for two local
models; a hosted model writes differently, and only a hosted run gives a price.

**Does not answer:** which builder is better (no quality measurement), anything about another model, or the cost at corpus scale
beyond arithmetic from the 20 documents. One model per comparison (D-24): a run on the other provider is a separate, labelled run
with its own yes.

## What I need you to decide

| # | Decision | Options | My recommendation, and its cost |
|---|---|---|---|
| 1 | Provider and model | **A. OpenAI `gpt-6-luna`**, reasoning off (`reasoning_effort: none`), Chat Completions. B. Anthropic `claude-haiku-5-5` through its OpenAI-compatibility layer, thinking disabled. C. OpenAI `gpt-5-nano`. D. Stay local (nothing more to run) | **A.** The request shapes seen in pass A are ordinary Chat Completions, and its price equals Haiku 5.5's (up to 100,000-token prompts), so a later Anthropic repeat compares like with like on price. Cost: its reasoning has to be switched off by a field the builders cannot send, which needs a gateway change (F1). B cannot run two of the four builders (see "Facts"). C is cheaper still, but its prices reached me only through a page summariser |
| 2 | Cap | Your number. I propose **USD 3 in total** for the whole pilot, with stage limits A 0.10, B 0.20, C 0.60, D 1.50 (sum 2.40; 0.60 kept for a repeat after a fault, rules below) | The ladder costs about USD 0.9 at the central estimate and about 1.6 with output times 2 (tables below), so 3 is about 3 and 2 times those. A bigger cap buys nothing here; a smaller one makes the gateway's pessimistic reservations refuse calls. State it in the currency your provider bills (both pages I read are in USD; your earlier cap was in EUR) |
| 3 | Sending article text to the provider | Yes or no | The 20 articles go to the provider's API. The dataset is ODC-By 1.0; the publishers' own terms were not checked; the text is never committed. OpenAI's data page (read about 20:36, in the table below): abuse-monitoring logs are kept "up to 30 days", and API data is not used for training unless you opt in; it does not say where the opt-in is. Anthropic's terms are not read yet (needed only for the repeat). If you say no, the answer is option D |
| 4 | Embeddings | **Local `qwen3-embedding:0.6b`** (as in pass A), or OpenAI `text-embedding-3-small` | **Local.** Free, no second key, same for every builder. Hosted would cost about USD 0.002 for LightRAG's 20 documents (116,890 tokens at USD 0.02 per million, arithmetic). The embedding tokens are still recorded and priced by that arithmetic. Cost: "cost per document" is then a sum of a hosted measurement and an arithmetic term |
| 5 | Builders | All four, in this order: LightRAG, fast-graphrag, Microsoft GraphRAG, nano-graphrag | nano-graphrag stopped in document 1 in both of its `granite4.2:8b` runs (a delimiter slip); a hosted model may not slip. If it fails at document 1 again it stops there for cents |
| 6 | Key and a hard limit | A new key for this pilot only, by the D-20 route (a file only you can read, outside any repository, read by the gateway itself, never printed), **and** a hard spending limit at the provider (a project budget or a prepaid balance of at most the cap), or your statement that none exists and the gateway is the only guard | Required before stage A. A timed-out or dropped call counts as zero in the gateway but the provider may still bill a generation it finished, so the gateway cap alone is not a guarantee. Whether OpenAI's console offers a project limit is **unstated** to me (its data page does not mention one). You delete the key afterwards |
| 7 | How many yeses | **Two:** one for stages A to C (about USD 0.3 at the central estimate, at most 0.9 by the limits), then a second for stage D with C's numbers in hand. Or one for everything | Two. Stage D is the largest cost and the first at which a surprise would be expensive |

## Facts the plan stands on

Read 20261102 (UTC). Prices change; they are read again when the gateway config is written, and that time goes into its `read_at`.

| Fact | Source and time |
|---|---|
| Claude Haiku 5.5: USD 0.10 per million input tokens, 0.50 output (prompts up to 100,000 tokens; above that 0.50 and 2.50). Claude Sonnet 5.5: 2 and 10. Quoted table rows | `https://platform.claude.com/docs/en/about-claude/pricing`, 20:19 |
| `gpt-6-luna`: USD 0.10 input, 0.50 output, 0.01 cached input, 0.125 for a 30-minute cache write and 0.25 for a 12-hour one, per million tokens, in the raw page text and on the model's own page. The page also says regional-processing (data residency) endpoints cost a further 10% for models released on or after 5 March 2026. The reviewer also reports a long-context tier above 272,000 input tokens and a doubled "Fast" price; prompts here are a few thousand tokens | `https://developers.openai.com/api/docs/pricing` (raw text) and `/models/gpt-6-luna`, 20:20 and 20:35 |
| `gpt-5-nano` 0.05 and 0.40; `gpt-4o-mini` 0.15 and 0.60; `text-embedding-3-small` 0.02 per million. **Only through a page summariser; the raw page text held only the luna rows** | the pricing page, 20:19 |
| `gpt-6-luna`: Chat Completions supported, embeddings not; context 1,050,000, maximum output 128,000 tokens; reasoning on, default effort `medium`, `none` supported; "structured outputs" listed as supported. Whether `json_object`, `max_tokens`, `temperature` and `seed` are accepted is **not stated** on that page | `https://developers.openai.com/api/docs/models/gpt-6-luna`, between 20:19 and 20:23 |
| Claude Haiku 5.5: thinking is on by default; `thinking: {"type": "disabled"}` is accepted at effort `high` or below; thinking tokens are billed as output tokens even when not returned; a non-default `temperature`, `top_p` or `top_k` returns a 400 error on every request | `https://platform.claude.com/docs/en/build-with-claude/thinking`, between 20:19 and 20:23 |
| Anthropic's OpenAI-compatibility layer: `response_format` accepts only `json_schema` with `strict: true` (`json_object` returns a 400); prompt caching unsupported; `usage.*_details` always empty; `reasoning_effort` ignored; no embeddings endpoint listed; "not considered a long-term or production-ready solution" | `https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk`, between 20:19 and 20:23 |
| OpenAI data use: abuse-monitoring logs "retained for up to 30 days" by default; API data not used for training "unless you explicitly opt in"; the page names no opt-in location and no project spend limit | `https://developers.openai.com/api/docs/guides/your-data`, 20:36 |
| What the builders really send. From pass A's body logs: LightRAG and nano-graphrag's extraction calls only `messages`; **fast-graphrag `response_format: json_object` on all 60 calls**; Microsoft GraphRAG `json_schema` with `strict: true` on 6 of 128 (community reports). From the installed source and the rehearsal pages, not seen in a log because nano-graphrag stopped in document 1: **nano-graphrag sends `max_tokens` 500 on entity summaries and `response_format: json_object` on community reports**; fast-graphrag's summaries send `max_tokens: null`. None sends `temperature` | pass-A runs of 20261102; `nano_graphrag/_op.py` line 145 and `base.py` line 28 (0.0.8.2); [`rehearsal/nano-graphrag.md`](rehearsal/nano-graphrag.md), [`rehearsal/fast-graphrag.md`](rehearsal/fast-graphrag.md) |
| The gateway today: a model needs `source_url` and `read_at`; `request_defaults` is **refused on any upstream that has a key**; no output-limit default is injected, so a call without `max_tokens` is reserved at `default_max_output_tokens` (4,096) and may cost more (recorded as `reserve_exceeded`); a timed-out, dropped or non-2xx call is recorded as zero cost; the default `upstream_timeout_s` is 120; the log holds no `finish_reason` and no reasoning-token count (those are in the response body, which is logged only with `log_bodies`) | [`tools/metering_gateway.md`](../../../tools/metering_gateway.md) |

Three consequences. **Hidden reasoning is the main hazard**: both providers' small models reason by default and bill it as output,
as `granite4.2:8b` did locally (17 s and 278 tokens against 0.3 s and 8 for one question). The builders cannot send the field that
turns it off, so the gateway has to add it, and today it refuses to on a paid upstream, on purpose. **fast-graphrag and
nano-graphrag cannot run on Claude through that layer**, because their `json_object` format is a 400 there. And **the cap is not a
full guard**: a call the gateway voided can still have been billed.

## What it costs: arithmetic, not measurement

Tokens are from pass A (`granite4.2:8b`'s own tokenizer; a hosted model's counts differ). LightRAG is measured at 20 documents.
The others are scaled **by characters**, because the first 5 documents hold 32,458 of the 20's 191,571 characters (factor 5.90)
and the first 13 hold 101,871 (factor 1.88); LightRAG, the one builder measured at both sizes, grew 6.0 times in input and 5.6 in
output from 5 to 20 documents. nano-graphrag has no run past one document: its input is the stub count and its output a guess
between LightRAG's output-to-input ratio (0.34) and its own single document's (0.70, which included a capped answer); the middle
(0.52) is used. Prices are `gpt-6-luna`'s; embeddings are local and free.

| Builder | Input tokens | Output tokens | How scaled | USD for 20 documents, output x0.5 / x1 / x2 |
|---|---|---|---|---|
| LightRAG | 401,109 | 135,391 | measured | 0.074 / 0.108 / 0.176 |
| fast-graphrag | 331,955 | 124,603 | 13-document run x 1.88 | 0.064 / 0.095 / 0.158 |
| Microsoft GraphRAG | 631,330 | 414,204 | 5-document run x 5.90 | 0.167 / 0.270 / 0.477 |
| nano-graphrag | 421,152 | 218,999 | stub input; output ratio 0.52 | 0.097 / 0.152 / 0.261 |
| **All four** | | | | **0.402 / 0.625 / 1.072** |

With nano-graphrag's ratio at 0.34 or 0.70 the central total is 0.587 or 0.663. Microsoft GraphRAG's summaries may grow faster than
characters; that is not in the number.

| Stage | Central estimate (output x1) | Output x2 | Limit | Stop at |
|---|---|---|---|---|
| A (at most 12 calls) | at most 0.02 | | 0.10 | 0.10 |
| B: 1 document, four builders | 0.030 | 0.051 | 0.20 | 0.09 |
| C: 5 documents, four builders, twice | 0.235 | 0.404 | 0.60 | 0.60 |
| D: 20 documents, four builders | 0.625 | 1.072 | 1.50 | 1.50 |
| **Ladder** | **0.91** | **1.55** | 2.40 | |

"Stop at" is the lower of the stage limit and 3 times the stage's central estimate. Stage B uses the measured one-document tokens
of pass A, which carry each builder's fixed costs.

- **Headline unit:** LightRAG at `gpt-6-luna` is about USD 0.0054 per document, 5.4 per thousand documents, and about 3.5 for the
  whole 609-article corpus (extrapolated by characters, 32.9 times the 20).
- **For scale:** at Claude Sonnet 5.5 (USD 2 and 10) the same four builders would cost about 12.5 at the central estimate, so a
  mid-tier model needs a different cap and is not what X2 asks for.
- **The worst single call** at `gpt-6-luna` is a 128,000-token answer, USD 0.064; with the output limit below, 6,144 tokens, USD 0.003.
- **What moves it:** the output length of a hosted model (pass A: 4 to 16 times the stub's, and one run does not repeat another
  exactly), retries (the SDK's and the library's stack; the pass-A agents counted 2 and 7 for Microsoft GraphRAG), billing of
  calls the gateway voided, and reasoning left on.

## The ladder

| Stage | What | Gate to the next |
|---|---|---|
| 0 | **Free work** (list below) and your actions: key, hard limit, a copy of the stage-A requests | The free tests pass |
| A | **The gateway meets a real provider.** At most 12 calls: a ping; one recorded request of each kind from pass A replayed (LightRAG extraction and gleaning, fast-graphrag extraction with `json_object`, Microsoft GraphRAG extraction and its `json_schema` community report); requests I synthesise from the builders' source for the shapes pass A never logged (nano-graphrag's entity summary with `max_tokens` 500 and its `json_object` community report, fast-graphrag's summary with `max_tokens: null`); then a gateway started with a tiny cap, where a call must be refused and nothing forwarded | Every call 200; reasoning off accepted and no reasoning tokens in any response body; `json_object`, `json_schema` and `max_tokens` accepted, or the rejection recorded as the builder being incompatible (no reconfiguration); the usage object checked for cache-write fields; **the console's usage page agrees with the gateway's total to rounding** (the only independent check: the gateway's tokens equal the provider's `usage` by construction) |
| B | **One document per builder**, one builder at a time | All four finish or fail with a recorded reason; spend under its "stop at"; no answer past the output limit |
| C | **Five documents per builder, twice** (independent runs, because one run does not repeat another) | The spread between the two runs is recorded, not hidden. "Passed C" for a builder means both its runs finished, every call returned 200, and no stop rule fired on it |
| D | **Twenty documents per builder** that passed C | Needs the second yes |

Fixed for every stage, so nothing is chosen after a result:
- **One ledger for the whole pilot.** One log directory, each stage starting the gateway with `--resume` and a cap of the lower of the
  stage limit and USD 3 minus what the log already shows spent. Builders run one at a time, in the order of decision 5.
- **Concurrency 4** for every builder, as pass A used 2. The gateway reserves the worst case for each call in flight (a 9 KB prompt
  with 6,144 output tokens is about USD 0.0035 at luna prices), so Microsoft GraphRAG's default of 25 at once would hold about USD
  0.09 in reservations, nearly half of stage B's limit; the account's rate limits are **unstated** to me. This departs from "each
  builder's own defaults"; the results say so. Time is not estimated: pass A's local times are no guide.
- **Output limit 6,144 tokens** injected by the gateway when the builder sets none (F1), the value pass A used, so truncation is
  comparable; it is above the longest answer that ended normally there (3,093).
- **`upstream_timeout_s` 900** (the default of 120 would void long answers the provider may still bill).
- **A request shape the model rejects is a result.** The builder is recorded as incompatible with this model; nobody changes its
  request to make it pass.
- **The repeat after a fault** (the unused USD 0.60) is allowed only when a stop rule fired for a harness or provider reason, the
  cause is fixed and written down, and the earlier numbers are kept and reported. Never to get a better result.

## Free work before the first paid call

| # | Item | Done when |
|---|---|---|
| F1 | **Gateway:** (a) allow `request_defaults` on a keyed upstream only when that upstream's config says so; (b) a **separate** per-model output-limit key, injected as the provider's own field (`max_completion_tokens` for OpenAI-protocol, `max_tokens` for Anthropic) when the client sent neither, **before** `max_out` and the reservation are computed, named in `request_defaults_applied`; (c) `cache_write_per_mtok` set from the pricing page | Tests pass, including that the reservation equals the injected limit and that a client's own limit wins; a deliberate break of each rule turns a test red |
| F2 | **A hosted setup for the four runners:** chat upstream with the key variable, real prices with `source_url` and `read_at`, the cap, `upstream_timeout_s` 900, `log_bodies = true`; the embedding model stays on the local upstream. **The gateway process alone gets the key** (it reads the file itself); the runner and the builders never have it | Each runner completes against a fake paid upstream and reproduces the stub rehearsal's counts. A **canary test** with a distinctive fake key finds it in none of: the builder's environment and argument list, every log, the body logs, the result JSON, stderr |
| F3 | **The stage-A replay script** and a durable copy of the requests it needs (about a dozen) in a mode-600 file outside the repository and outside the session's scratch directory, which does not outlive the session | It sends nothing without the stage's cap loaded; it runs against the fake upstream first |
| F4 | **A free pre-flight** that prints expected tokens times price and the cap for the stage and refuses if the estimate exceeds the stage's "stop at" | It refuses an over-cap case in a test |
| F5 | **Provider terms.** OpenAI's data page is read (above); Anthropic's is read before any repeat | Both quoted with read times |
| F6 | **A dress rehearsal of the whole ladder** against the fake paid upstream, including a run that hits the cap and a run where calls are voided | It stops at the cap and writes a complete log |
| F7 | **A watchdog** that runs beside every paid stage: it polls the gateway's summary and reads the body log, and stops the runner and the gateway the moment a stop rule fires. It reads `usage.completion_tokens_details.reasoning_tokens` and `finish_reason` from response bodies, which the gateway's own log does not hold | A fake upstream that produces each condition (reasoning tokens, a length stop, voided calls, repeated requests) makes it stop within one poll; the SDKs' own retries cannot hold it up |

## Stop rules, fixed in advance

- Stop everything and report on: any provider error other than one retried 429 or 5xx; any gateway refusal; a call whose usage is
  missing; reasoning tokens where none are expected; a stage's spend past its "stop at"; more than 5% of answers ended by the output
  limit; more than 5% of requests repeated identically; more than 3 voided calls in a stage. The percentages and the count are my
  choices, written here before any run.
- A builder that fails by its own fault (exit not zero, the provider answered 200) is a result: record it and continue with the
  other builders of the stage.
- **No run is repeated to get a better result.** The only repeats are the pre-registered second run of stage C and the fault repeat above.

## What is recorded

For every call: the gateway's record (usage as the provider reported it, cost, latency, the fields it added) and, in the body log,
the response (finish reason, usage details). Per run: builder version and pin, the model name the provider reports, the prices with
`source_url` and `read_at`, settings and the departures from defaults, the result JSON as in pass A. The body logs hold article
text and stay outside the repository; only result files that pass the path, key and copied-text scans are committed. Results go
under this directory when a stage ends, with my reading kept apart from the numbers. The console's totals are recorded next to the
gateway's.

## What this cannot show

Quality of any graph. Another model, or the other provider (a separate run). Behaviour at corpus scale, beyond arithmetic. News
text only. A single account's rate limits and tier, which are **unstated** to me. Because builders keep their own chunking and
prompts, the table is not a like-for-like comparison, as the rehearsal table already says. Token counts are the hosted model's, not
granite's, so the pass-A figures only bracket them.

## Risks

| Risk | Mitigation |
|---|---|
| Hidden reasoning bills as output | `reasoning_effort: none` added by the gateway (F1); stage A and the watchdog check it |
| Runaway or very long answers | Output limit 6,144 injected (F1); watchdog on length stops |
| Retries multiply calls and cost | Concurrency 4; stop rules on repeated and voided requests; the console total is compared because failed attempts carry no tokens in the log |
| The provider bills a call the gateway voided | Timeout 900; the hard limit at the provider (decision 6); the voided-call stop rule |
| A request shape is rejected (`json_object`, `max_tokens`, `temperature`) | Stage A, including requests synthesised from source for nano-graphrag; rejection is a recorded result |
| The gateway has never met a real provider | Stage A, with a refused call checked against the provider's console |
| Pessimistic reservations refuse calls | Concurrency 4; stage limits above expected spend plus open reservations |
| Key exposure | D-20 route; only the gateway holds it; the canary test (F2); never printed; deleted afterwards |
| Third-party text sent to a provider | Decision 3; text never committed; the body logs stay outside the repository |
| Price changes between reading and running; a regional endpoint | Re-read when the config is written; `read_at` recorded; the default endpoint is used |
| The provider's bill differs from tokens times price (cache writes, rounding) | The console total is compared in stage A and at the end of each stage |

## The repeat on Anthropic (separate, later, its own yes)

Through the compatibility layer: `claude-haiku-5-5` with `thinking: {"type": "disabled"}` as a gateway default (documented
natively; **untested through the layer**). **fast-graphrag and nano-graphrag excluded** (`json_object` returns a 400). No prompt
caching and no reasoning-token detail in `usage`, so the stage-A and watchdog checks on reasoning tokens would have nothing to read;
the console would be the only check. Embeddings local. The prices equal luna's up to 100,000-token prompts, but the tokenizers
differ, so the cost table applies as arithmetic only.

## What changed in the revision

An independent reviewer (a fresh agent that fetched the sources and recomputed the numbers) found five high and several lesser
problems; I checked each against the files before changing anything. Changes: the 20-document costs now scale by characters (the
first version used a factor of 4, which the data do not support; the totals rose from 0.27 / 0.39 / 0.64 to 0.40 / 0.63 / 1.07);
nano-graphrag's output, which I had wrongly called unmeasured, is now estimated from its one document; nano-graphrag's real request
shapes (`max_tokens` 500, `json_object`) and its exclusion from the Anthropic repeat were added; the cap is no longer called the
guard against billing of voided calls, and a hard provider-side limit became a precondition; the watchdog (F7) and the body-log
checks were added because the gateway's log cannot show reasoning tokens or finish reasons; the output-limit value, the timeout,
"passed C", the fault-repeat rule and the policy for rejected requests were fixed in writing; the ledger across stages and the
key hand-off were specified; F1 was tightened.

## Sources

Read 20261102 (UTC), 20:19 to 20:36: the pages named in "Facts"; pass-A results in [`pass-a/`](pass-a) and
[its page](pass-a-local-model.md); [`tools/metering_gateway.md`](../../../tools/metering_gateway.md); decisions D-14, D-19 to D-21
and D-24 in [`DECISIONS.md`](../../../DECISIONS.md); the first pilot's plan, [`pinakes/experiments/p4-deep-pilot.md`](../../../pinakes/experiments/p4-deep-pilot.md).
