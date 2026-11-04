# X2 pass B: a plan for the paid pilot

**Plan written 20261102 20:24 UTC and revised at 20:39 UTC after an independent review (the changes are listed at the end). When it was
written no paid call had been made and nothing was approved; since then the owner has approved stages A to C (D-34) and stage D (D-37) and all four have
run (USD 1.105 spent by the gateway's count, 1.184 with the cache-write price it left out, D-39; the run log near the end and [the results](pass-b-results.md)).** The owner asked for this plan ("Plan paid pilot") after
[pass A](pass-a-local-model.md). Under D-14 a paid step starts only on the owner's explicit yes with model, provider and cap; this
page says what that yes would unlock, what is fixed in advance, and what has to be built and checked for free first. Everything that
could be chosen after seeing a result is fixed here instead.

**Decided so far (owner, 20261102 20:49 UTC, reply "gpt-6-luna, USD 3"):** decision 1, OpenAI `gpt-6-luna` with reasoning off, and
decision 2, a cap of USD 3 in total with the stage limits below. **Decided 20261103 01:26 UTC** (owner, reply "go wit your
recommendations"): 3 yes, article text may go to OpenAI's API; 4 local embeddings; 5 all four builders; 7 two yeses (one for stages A to
C, one for D). **Decision 6 was done by the owner on 20261103:** a project of its own at OpenAI with a USD 3 hard limit and a restricted key in a
private file (the console later showed USD 5.00 beside the project's spend; whether that is the hard limit is unknown, D-40) ([`pass-b-owner-steps.md`](pass-b-owner-steps.md)). **The yes for stages A to C was given on 20261103 16:12 UTC (D-34),
after the dry runs, and the yes for stage D at 17:57 UTC (D-37); all four stages have run** (run log below; the numbers are in
[`pass-b-results.md`](pass-b-results.md)). Stage 0 is done (below); what is next (closing the pilot; the owner left the data-sharing setting on, D-42) is in [`RESUME.md`](../../../RESUME.md).

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
| 3 | Sending article text to the provider | Yes or no | The 20 articles go to the provider's API. The dataset is ODC-By 1.0; the publishers' own terms were not checked; the text is never committed. OpenAI's data page (read about 20:36, in the table below): abuse-monitoring logs are kept "up to 30 days", and API data is not used for training unless you opt in; it does not say where the opt-in is (**found 20261104, D-41: this organisation had opted in, for all projects**). Anthropic's terms are not read yet (needed only for the repeat). If you say no, the answer is option D |
| 4 | Embeddings | **Local `qwen3-embedding:0.6b`** (as in pass A), or OpenAI `text-embedding-3-small` | **Local.** Free, no second key, same for every builder. Hosted would cost about USD 0.002 for LightRAG's 20 documents (116,890 tokens at USD 0.02 per million, arithmetic). The embedding tokens are still recorded and priced by that arithmetic. Cost: "cost per document" is then a sum of a hosted measurement and an arithmetic term |
| 5 | Builders | All four, in this order: LightRAG, fast-graphrag, Microsoft GraphRAG, nano-graphrag | nano-graphrag stopped in document 1 in both of its `granite4.2:8b` runs (a delimiter slip); a hosted model may not slip. If it fails at document 1 again it stops there for cents |
| 6 | Key and a hard limit | A new key for this pilot only, by the D-20 route (a file only you can read, outside any repository, read by the gateway itself, never printed), **and** a hard spending limit at the provider (a project budget or a prepaid balance of at most the cap), or your statement that none exists and the gateway is the only guard | Required before stage A. A timed-out or dropped call counts as zero in the gateway but the provider may still bill a generation it finished, so the gateway cap alone is not a guarantee. OpenAI documents a project-level hard spend limit ("Spend limits", read 20261103; steps and commands for you in [`pass-b-owner-steps.md`](pass-b-owner-steps.md)); whether **your** account has it is unstated. You delete the key afterwards |
| 7 | How many yeses | **Two:** one for stages A to C (about USD 0.3 at the central estimate, at most 0.9 by the limits), then a second for stage D with C's numbers in hand. Or one for everything | Two. Stage D is the largest cost and the first at which a surprise would be expensive |

## Facts the plan stands on

Read 20261102 (UTC). Prices change; they are read again when the gateway config is written, and that time goes into its `read_at`.

| Fact | Source and time |
|---|---|
| Claude Haiku 5.5: USD 0.10 per million input tokens, 0.50 output (prompts up to 100,000 tokens; above that 0.50 and 2.50). Claude Sonnet 5.5: 2 and 10. Quoted table rows | `https://platform.claude.com/docs/en/about-claude/pricing`, 20:19 |
| `gpt-6-luna`: USD 0.10 input, 0.50 output, 0.01 cached input, 0.125 for a 30-minute cache write and 0.25 for a 12-hour one, per million tokens, in the raw page text and on the model's own page. The page also says regional-processing (data residency) endpoints cost a further 10% for models released on or after 5 March 2026. The reviewer also reports a long-context tier above 272,000 input tokens and a doubled "Fast" price; prompts here are a few thousand tokens | `https://developers.openai.com/api/docs/pricing` (raw text) and `/models/gpt-6-luna`, 20:20 and 20:35 |
| `gpt-6-luna` read again 20261103: Standard USD 0.10 input, 0.50 output, 0.01 cached input, 0.125 (30 min) and 0.25 (12 h) cache write, unchanged; Fast tier (a separate service tier, not used) 0.20 and 1.00; a long-context row exists (0.20 input, 0.75 output); the 10% regional-processing uplift applies to models released on or after 5 March 2026 and the page does not give this model's release date; Chat Completions and Responses supported, embeddings not; `reasoning.effort` accepts `none`; default rate limits by usage tier: Build 5,000 requests and 2,000,000 tokens a minute, Launch 10,000 and 10,000,000, Grow 30,000 and 180,000,000 (**the owner's tier is unstated**) | `https://developers.openai.com/api/docs/pricing` and `/models/gpt-6-luna`, 20261103 01:25 |
| OpenAI project spend limit: **Enforce a hard limit** makes requests fail with a `429` (`project_spend_limit_exceeded`); alerts do not stop anything; "enforcement is not instantaneous, so recorded spend can slightly exceed the configured amount"; a project limit "applies only to API traffic billed to that project" | `https://developers.openai.com/api/docs/guides/spend-limits`, 20261103 |
| `gpt-5-nano` 0.05 and 0.40; `gpt-4o-mini` 0.15 and 0.60; `text-embedding-3-small` 0.02 per million. **Only through a page summariser; the raw page text held only the luna rows** | the pricing page, 20:19 |
| `gpt-6-luna`: Chat Completions supported, embeddings not; context 1,050,000, maximum output 128,000 tokens; reasoning on, default effort `medium`, `none` supported; "structured outputs" listed as supported. Whether `json_object`, `max_tokens`, `temperature` and `seed` are accepted is **not stated** on that page | `https://developers.openai.com/api/docs/models/gpt-6-luna`, between 20:19 and 20:23 |
| Claude Haiku 5.5: thinking is on by default; `thinking: {"type": "disabled"}` is accepted at effort `high` or below; thinking tokens are billed as output tokens even when not returned; a non-default `temperature`, `top_p` or `top_k` returns a 400 error on every request | `https://platform.claude.com/docs/en/build-with-claude/thinking`, between 20:19 and 20:23 |
| Anthropic's OpenAI-compatibility layer: `response_format` accepts only `json_schema` with `strict: true` (`json_object` returns a 400); prompt caching unsupported; `usage.*_details` always empty; `reasoning_effort` ignored; no embeddings endpoint listed; "not considered a long-term or production-ready solution" | `https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk`, between 20:19 and 20:23 |
| OpenAI data use: abuse-monitoring logs "retained for up to 30 days" by default; API data not used for training "unless you explicitly opt in" (**this organisation had opted in, D-41**); the page names no opt-in location and no project spend limit | `https://developers.openai.com/api/docs/guides/your-data`, 20:36 |
| What the builders really send. From pass A's body logs: LightRAG and nano-graphrag's extraction calls only `messages`; **fast-graphrag `response_format: json_object` on all 60 calls**; Microsoft GraphRAG `json_schema` with `strict: true` on 6 of 128 (community reports). From the installed source and the rehearsal pages, not seen in a log because nano-graphrag stopped in document 1: **nano-graphrag sends `max_tokens` 500 on entity summaries and `response_format: json_object` on community reports**; fast-graphrag's summaries send `max_tokens: null`. None sends `temperature` | pass-A runs of 20261102; `nano_graphrag/_op.py` line 145 and `base.py` line 28 (0.0.8.2); [`rehearsal/nano-graphrag.md`](rehearsal/nano-graphrag.md), [`rehearsal/fast-graphrag.md`](rehearsal/fast-graphrag.md) |
| The gateway **before stage 0 (version 1.0.0)**: a model needs `source_url` and `read_at`; `request_defaults` is **refused on any upstream that has a key**; no output-limit default is injected, so a call without `max_tokens` is reserved at `default_max_output_tokens` (1,024 unless the config sets another value; the pass-A and hosted configs set 4,096) and may cost more (recorded as `reserve_exceeded`); a timed-out, dropped or non-2xx call is recorded as zero cost; the default `upstream_timeout_s` is 120; the log holds no `finish_reason` and no reasoning-token count (those are in the response body, which is logged only with `log_bodies`). **Version 1.1.0 (commit `1e1b37c`) adds** `allow_request_defaults` per upstream, `output_limit_default` per model and `key_file` per upstream; **version 1.2.0 adds** `translate_max_tokens` per model (D-35); the plan below describes that version | [`tools/metering_gateway.md`](../../../tools/metering_gateway.md) |

Three consequences. **Hidden reasoning is the main hazard**: both providers' small models reason by default and bill it as output,
as `granite4.2:8b` did locally (17 s and 278 tokens against 0.3 s and 8 for one question). The builders cannot send the field that
turns it off, so the gateway has to add it. Version 1.0.0 refused to on a paid upstream, on purpose; 1.1.0 does it only for an
upstream whose config says so. **fast-graphrag and
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
  request to make it pass. **One exception, decided by the owner on 20261103 after stage A (D-35):** `gpt-6-luna` rejected
  `max_tokens: 500` (nano-graphrag's entity summary) and `max_tokens: null` (fast-graphrag's summary), both with 400. For this model
  the gateway **drops a null `max_tokens` and sends a set one as `max_completion_tokens` with the same value** (`translate_max_tokens`,
  gateway 1.2.0). It is a departure from each builder's own request, so every result from this model says so
  (`hosted.departures_from_the_builders_requests` in the result file, and the translation's name in each call's
  `request_defaults_applied`), and any other rejected shape is still a result.
- **The repeat after a fault** (the unused USD 0.60) is allowed only when a stop rule fired for a harness or provider reason, the
  cause is fixed and written down, and the earlier numbers are kept and reported. Never to get a better result.

## Free work before the first paid call

| # | Item | Done when |
|---|---|---|
| F1 | **Gateway:** (a) allow `request_defaults` on a keyed upstream only when that upstream's config says so; (b) a **separate** per-model output-limit key, injected as the provider's own field (`max_completion_tokens` for OpenAI-protocol, `max_tokens` for Anthropic) when the client sent neither, **before** `max_out` and the reservation are computed, named in `request_defaults_applied`; (c) `cache_write_per_mtok` set from the pricing page (**added after stage D, D-39:** the price was set, 0.125 in the run profile, but gateway 1.2.0 applied a cache-write price only to Anthropic usage and never read OpenAI's `cache_write_tokens`; it was configured and unused for the whole pilot) | Tests pass, including that the reservation equals the injected limit and that a client's own limit wins; a deliberate break of each rule turns a test red |
| F2 | **A hosted setup for the four runners:** chat upstream with the key variable, real prices with `source_url` and `read_at`, the cap, `upstream_timeout_s` 900, `log_bodies = true`; the embedding model stays on the local upstream. **The gateway process alone gets the key** (it reads the file itself); the runner and the builders never have it | Each runner completes against a fake paid upstream and reproduces the stub rehearsal's counts. A **canary test** with a distinctive fake key finds it in none of: the builder's environment and argument list, every log, the body logs, the result JSON, stderr |
| F3 | **The stage-A replay script** and a durable copy of the requests it needs (about a dozen) in a mode-600 file outside the repository and outside the session's scratch directory, which does not outlive the session | It sends nothing without the stage's cap loaded; it runs against the fake upstream first |
| F4 | **A free pre-flight** that prints expected tokens times price and the cap for the stage and refuses if the estimate exceeds the stage's "stop at" | It refuses an over-cap case in a test |
| F5 | **Provider terms.** OpenAI's data page is read (above); Anthropic's is read before any repeat | Both quoted with read times |
| F6 | **A dress rehearsal of the whole ladder** against the fake paid upstream, including a run that hits the cap and a run where calls are voided | It stops at the cap and writes a complete log |
| F7 | **A watchdog** that runs beside every paid stage: it polls the gateway's summary and reads the body log, and stops the runner and the gateway the moment a stop rule fires. It reads `usage.completion_tokens_details.reasoning_tokens` and `finish_reason` from response bodies, which the gateway's own log does not hold | A fake upstream that produces each condition (reasoning tokens, a length stop, voided calls, repeated requests) makes it stop within one poll; the SDKs' own retries cannot hold it up |

## Stage 0 status (updated 20261103 00:26 UTC)

Built by Sonnet builders and verified by me (tests re-run, the new pieces driven against a real gateway process and a fake
provider, deliberate breakages of my own). Nothing here has met a real provider. (True when this section was written; stage A met one on 20261103 and stages B to D ran against it: see the run log.)

| Item | State | Commit |
|---|---|---|
| F1 gateway: `allow_request_defaults`, `output_limit_default`, and `key_file` (added during the work: the gateway reads the key itself) | Done; 124 gateway tests | `1e1b37c` |
| F2 hosted setup for the four runners (`--hosted-profile`), canary of the key | Done; the four runners reproduce their rehearsals through a fake paid upstream | `f4c28b2` |
| F4 free pre-flight | Done; returns the run's allowance and the cumulative cap for the gateway config | `3657dab` |
| F7 watchdog | Done; also stops whole process groups | `3657dab` |
| F5 provider terms | OpenAI's data page read (above); Anthropic's only before a repeat | this page |
| F3 stage-A replay script and the durable copy of the requests | Done; a dry run unless `--send`; the refusal test runs against a dead loopback upstream; driven end to end against a fake provider | `15ccdea` |
| F8 (added) the stage driver `passb_stage.py`: pre-flight, run profile, runner in its own session, watchdog beside it, reports | Done; 43 tests; 52 mutants by the builder and 34 of mine (29 killed, the 5 left are listed in the README); changed once after the rehearsal (below) | `90e8ae3` |
| F6 dress rehearsal of the whole ladder against the fake paid upstream | Done for all four builders (below). It found one design error, in the watchdog | this page |

### What the dress rehearsal showed

Run 20261102 23:48 to 23:58 UTC, free, nothing paid. Real: the stage driver, pre-flight, watchdog, gateway, the four runners and the four builders in their throwaway environments,
real processes, files, locks and signals. Fake: the paid provider (each builder's rehearsal responder, with fault modes) and the
embedding server. A canary key stood in for the real one.

| Run | Checks | Result |
|---|---|---|
| The whole ladder for each builder: stage B, stage C twice, stage D, and a dry run first | 295 | All 16 runs completed; each run's spend equals its ledger rows to the last digit; files mode 600 and directories 700; no process of a run left; the report holds no absolute path; the canary key is in no file outside its own, in no driver output; a used run label is refused before anything starts |
| One fault per run, 16 runs (reasoning tokens; usage missing; dropped connections for all four builders; a bill beyond the allowance and a length stop for LightRAG and Microsoft GraphRAG) | 278 | Every run ended `tripped` with exit status 3, the rule named, the runner's whole group and its gateway stopped, the report complete. Reasoning and length stops hit a live runner and stopped it (runner exit -15 for three builders; nano-graphrag had already exited 1 when its group was swept) |

- **The error it found.** The first ladder run stopped stage C's second run within a second: the watchdog counted a request as
  repeated if any run of the stage had sent it, and the second run sends the first run's requests again by design (5 repeats in
  39 records at the first look). Pass A's own ledgers confirm the premise: 23 of Microsoft GraphRAG's 103 five-document requests
  were identical to its one-document run's. The watchdog now takes `--repeat-since` (the run's start) so the rule looks for a
  retry loop inside one run; every other rule still counts the whole stage. A real second run would have been killed at the first
  poll, after the first run's money was spent. No unit test had seen it, because the builder's fake runner never repeated itself.
- **The cap is not a check on what the provider reports.** With a fake that reported 3,000 times the tokens a real output limit
  allows, a run spent USD 1.18 (LightRAG) and 1.11 (Microsoft GraphRAG) against an allowance of 0.20 before the watchdog's next poll:
  the gateway reserves the worst case it believes, then charges what the provider says. A real provider cannot exceed the limit the
  gateway injected, so this is not expected; it is why decision 6, a hard limit at the provider, stays the one independent guard.
- **Rules that need a sample.** The length-stop rule is not evaluated below 20 chat answers over the stage's window. Stage B never
  reaches that (LightRAG and fast-graphrag make 4 each at one document in pass A). In stage C, pass A's chat calls at 5 documents
  were 18 for LightRAG, 18 for fast-graphrag and 91 for Microsoft GraphRAG (nano-graphrag unmeasured), so the rule guards
  Microsoft GraphRAG from its first run and the other two only from the second run, whose calls add to the first's. A dropped connection tripped `provider_error` (a 5xx beyond the one
  tolerated), not `voided_calls`, and was recorded at zero cost, as the gateway records any call without usage; **a provider may
  still bill it**, which is what the console comparison is for.
- **After a trip, repeating the stage.** The stage's window stays open, so running it again trips at once on the old calls. The
  procedure (also in the driver's help): move `stage_<STAGE>.json` in the ledger directory aside, use a new run label; the new
  window opens at the ledger's spend then, and the total cap of USD 3 still counts everything. A test covers it.
- **Not covered, because it cannot be rehearsed offline:** what the real provider accepts (stage A), its real token counts, rate
  limits, and billing of failed calls. The stub's tokens gave USD 0.19 for stage D against the plan's central 0.625, as the
  stub's outputs are short (pass A: the real ones are 4 to 16 times longer).

Changes to the plan that the work made necessary, all in the direction of safer: the pre-flight returns two numbers, the run's
**allowance** (what it may spend) and the **cap for the gateway config** (the ledger's spend plus the allowance, because a resumed
gateway compares its cap with the whole log); the watchdog takes `--since`, so a stage's counts and spend are cumulative across its
runs and ignore earlier stages; the profile refuses a zero price. **A residual risk, stated plainly:** the key file is readable by any
process of the same user, including the builders, which run as that user; what is guaranteed is that the key is never handed to
them (not in their environment, arguments, logs or results; the canary test checks this), not that a hostile builder could not open
the file.

## Stop rules, fixed in advance

- Stop everything and report on: any provider error other than one retried 429 or 5xx; any gateway refusal; a call whose usage is
  missing; reasoning tokens where none are expected; a stage's spend past its "stop at"; more than 5% of answers ended by the output
  limit; more than 5% of requests repeated identically **within one run** (a first draft counted across the stage, and the dress
  rehearsal showed that stage C's second run, which sends the first run's requests again by design, was stopped within a second);
  more than 3 voided calls in a stage. The percentages and the count are my choices, written here before any run. **Evidence for the
  5%:** in pass A's clean local runs (read from the gateway ledgers of 20261102) the share of repeated requests inside one index
  run was 0 for LightRAG (342 calls at 20 documents; its checkpoints add documents to one index), 0 for fast-graphrag at 1 and 5
  documents and 2 of 81 requests (2.5%; 60 chat and 21 embedding, both repeats chat) at 14, and 0 for Microsoft GraphRAG in both
  its runs (43 calls at 1 document, 102 at 5). The committed result files carry those counts; the next figure comes from the
  session's gateway ledgers, which are not committed: Microsoft GraphRAG indexes each checkpoint again from scratch, and 23 of the
  second run's 103 ledger records (the 102 calls plus a dimension probe) are identical to the first run's, which is the cross-run
  repetition the window removes. Nothing is measured past 14 documents for fast-graphrag or past 5 for Microsoft GraphRAG, so
  stage D could stop a clean run on this rule; that would be a recorded stop, not a result.
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
| The gateway had never met a real provider (until stage A, 20261103) | Stage A, with a refused call checked against the provider's console; the refusal test passed, and the console comparison is the owner's |
| Pessimistic reservations refuse calls | Concurrency 4; stage limits above expected spend plus open reservations |
| Key exposure | D-20 route; only the gateway holds it; the canary test (F2); never printed; deleted afterwards |
| Third-party text sent to a provider | Decision 3; text never committed; the body logs stay outside the repository |
| Price changes between reading and running; a regional endpoint | Re-read when the config is written; `read_at` recorded; the default endpoint is used |
| The provider's bill differs from tokens times price (cache writes, rounding) | The console total is compared in stage A and at the end of each stage. **This happened:** the gateway left out OpenAI's cache-write price (found after stage D; D-39), which the comparisons did not catch because they were made against the gateway's own figures |

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

## Run log (paid attempts, newest last)

| When (UTC) | What | Result | Spent |
|---|---|---|---|
| 20261103 16:12 | Stage A, attempt 1 (the owner's yes, D-34). Ten requests and a refusal test planned | **Stopped at the first call, the ping: HTTP 401, `invalid_api_key`** (type `invalid_request_error`, no parameter, a 262-character message). The stop rule for a key or account fault worked: nothing else was sent; the nine other requests and the refusal test did not run. Four things are now known about the real provider: the gateway reached `api.openai.com` over TLS (a handshake had been tested first, from the interpreters that host the gateway); it added `reasoning_effort` and `max_completion_tokens` to the ping, as recorded in its log; OpenAI answered in its standard error shape, which the stage-A script parsed; and the 401 came back in 383 ms. Whether OpenAI would have accepted those two fields is **not yet known**, because authentication failed first. The 401 is recorded with zero cost and `voided`, as any non-2xx call is | USD 0 (the gateway's figure; the console should show no charge) |
| 20261103 16:18 | Stage A, attempt 2, with a new key (D-34). Ten requests and the refusal test | **Eight requests answered 200; two were rejected with 400 and cost nothing.** Reasoning off (`reasoning_effort: none`) was accepted and every answer reported 0 reasoning tokens and ended `stop`; the gateway's injected `max_completion_tokens` was accepted; `json_object` was accepted (fast-graphrag's extraction, nano-graphrag's community report) and so was strict `json_schema` (Microsoft GraphRAG's community report); usage carries `prompt_tokens_details.cache_write_tokens` and `cached_tokens` and `completion_tokens_details.reasoning_tokens`; the model reported itself as `gpt-6-luna`. **Rejected: nano-graphrag's entity summary (`max_tokens: 500`, `unsupported_parameter`, parameter `max_tokens`) and fast-graphrag's summary (`max_tokens: null`, sent beside the gateway's injected `max_completion_tokens`, `invalid_type`, parameter `max_tokens`).** The refusal test passed: with an allowance of USD 0.0001 the largest request got a 429 `gateway_budget_exceeded`, the throwaway ledger holds one record and nothing was forwarded. Tokens: 16,677 input (2,043 of them cached; the gleaning prompt reused the extraction prompt's prefix) and 9,836 output over the eight answers; the gateway's cost recomputed from those tokens at the profile's prices equals its own to the last digit (that check used the fields the gateway read, so it could not show what the gateway left out: OpenAI's `cache_write_tokens`, D-39). Latency 2 to 31 s. **The console comparison, the only check that is not the gateway's own numbers, is the owner's and was pending when this was written** | USD 0.00640183 (the gateway's figure) |
| 20261103 16:32 | Stage A, re-test of the two rejected shapes (the ping, fast-graphrag's summary and nano-graphrag's entity summary) through gateway 1.2.0 with the translation on, after the owner chose it (D-35). Three requests and the refusal test | **All three answered 200, reasoning 0, `stop`**: the null `max_tokens` was dropped and the injected `max_completion_tokens` accepted; `max_tokens: 500` was accepted as `max_completion_tokens: 500`. All gates yes; the refusal test passed again. Tokens 268 input and 57 output | USD 0.0000553 |
| 20261103 17:19 | **Stage B**, one document for each builder, in the order LightRAG, fast-graphrag, Microsoft GraphRAG, nano-graphrag (the owner's "Agrees", D-34) | All four completed, runner exit 0, no rule tripped, every answer HTTP 200 and finish `stop`, 0 reasoning tokens. 56 chat requests, 128,240 input tokens (18,568 cached), 52,390 output. The labelled translation was not needed by any call. nano-graphrag, which failed on its first document with the local model, finished, at 2.7 times the plan's guess | USD 0.03735 (limit 0.20, stop at 0.09) |
| 20261103 17:24 | **Stage C, run r1**, five documents for each builder | All four completed, no rule tripped, no repeated request, every answer 200 and `stop`. 208 chat requests | USD 0.11354 |
| 20261103 17:38 | **Stage C, run r2** (the pre-registered second run) | All four completed, nothing tripped (the repeat window let it run). 168 chat requests. Microsoft GraphRAG made 65 calls against r1's 113 (10 communities against 18); r2's input was cached more (r1 had just run) | USD 0.10599 (stage C 0.21952 of its limit 0.60) |
| 20261103 17:57 to 19:01 | **Stage D**, 20 documents for each builder, one run each (the owner's "Agrees; yes to D", D-37), in the order LightRAG, fast-graphrag, Microsoft GraphRAG, nano-graphrag | All four completed, runner exit 0, no rule tripped, no repeated request, 1,308 chat requests, every answer 200 and `stop`, 0 reasoning tokens. LightRAG 99 calls, fast-graphrag 96, Microsoft GraphRAG 558, nano-graphrag 555. **The labelled translation was used by a build for the first time:** 13 requests of fast-graphrag carried `max_tokens: null`, the gateway dropped it, all 13 were answered 200. Arithmetic from stage C had expected 0.65; the actual was 1.30 times that, and nano-graphrag alone 1.45 times | USD 0.84204 by the gateway, 0.90556 with the cache-write price (limit and allowance 1.50) |

**Stage A in all, per the gateway's ledger (the figures to hold against OpenAI's usage page, 20261103 16:32 UTC):** 11 requests
answered 200, 16,945 input tokens of which 2,043 cached, 9,893 output tokens, **USD 0.00645713**; two 400 rejections (no tokens) and one
401 from the first key, which was refused before any token was counted. The console comparison, the plan's only check that is not the
gateway's own numbers, is the owner's and is the gate to stage B.

**The gate was passed:** the owner compared OpenAI's usage page with those figures and replied "Agrees" (recorded 20261103 17:18 UTC) (the owner's word; the page's own numbers were not sent to me). Stage B started after it.

**Stage A's call count, its money limit and the code, stated plainly.** The ladder says "at most 12 calls"; that was written for one
run of the script. Three runs happened (a refused key, the ten requests, the re-test) and 14 requests reached OpenAI in all (1 refused
by the key, 10, 3). The script's money limit is also per run (each run may spend up to its allowance of USD 0.10 on top of what the
ledger already holds), while the pilot's USD 3 cap is cumulative; the stage's total was USD 0.0065 against 0.10, so nothing was close,
but the per-run limit is looser than the ladder's wording. The re-test ran on the working tree: by file modification times the gateway,
`passb_common.py`, `passb_stage.py` and `passb_stage_a.py` were last changed at 16:24 and 16:26, before the 16:32 re-test, and no code
file changed between the re-test and the commit (`a446479`).


**Stages A to C in all: USD 0.26333 by the gateway, 443 answered requests, 946,095 input tokens (320,773 cached), 395,177 output
tokens.** The tables, the comparison with the plan's estimates and with pass A, and my readings are in
[`pass-b-results.md`](pass-b-results.md); the per-call record is in [`pass-b/meter.jsonl`](pass-b/meter.jsonl). **The console comparison
for stages B and C is the owner's and is the gate to stage D** (figures in the results page); stage D needs its own yes with C's numbers.

**The owner compared OpenAI's usage page for stages B and C and replied that it agrees, and gave the yes for stage D** (recorded 20261103 17:57 UTC,
D-37): 20 documents for each of the four builders, one run each, in the usual order, allowance and stop-at USD 1.50, the pilot's cap USD 3.00.

**Stage D ran (17:57 to 19:01 UTC) and with it the four stages: USD 1.10537 by the gateway, 1,751 answered requests, 4,170,590 input
tokens (943,721 cached), 1,546,498 output tokens.** The tables, the comparison with the arithmetic from C and my readings are in
[`pass-b-results.md`](pass-b-results.md). **The gateway left out OpenAI's cache-write price (D-39):** OpenAI reported 3,140,582 tokens as written
to its cache (2,540,573 in stage D) and the gateway (1.1.0 in stage A's first two runs, 1.2.0 after) priced them as plain input; at the model page's USD 0.125 per million the four stages
cost 1.18389, not 1.10537. I read the console myself in Chrome (D-40, D-41): it shows USD 0.67 billed for the whole pilot, with requests, input tokens and the cache hit rate equal to the
ledger; that is the list-price value (1.18389) less complimentary daily tokens, which the organisation gets because it shares inputs and outputs with OpenAI (D-41), and its cache-writes line confirms 0.125 per million. The earlier comparisons (A, and B with C) were made against the gateway's figures. No further paid step is approved; a repeat of D is not covered by D-37.

**Data sharing, found 20261104 (D-41):** decision 3 rested on the page the plan read, "API data is not used for training unless you explicitly opt in" (table above). The organisation has "Share inputs and outputs with OpenAI" enabled for all projects, so the pilot's article text and the models' outputs were probably shared for improving and training OpenAI's models; the articles are the corpus's public text (an ODC-By dataset; the publishers' terms were not checked). The owner chose to leave the setting on (D-42); nothing was changed.

A credentials fault is a harness reason, so a repeat of stage A is allowed once the cause is fixed and written down (stop rules,
above). Attempt 1's files are kept under the pilot directory as `stage-a-attempt1`.

## Sources

Read 20261102 (UTC), 20:19 to 20:36: the pages named in "Facts"; pass-A results in [`pass-a/`](pass-a) and
[its page](pass-a-local-model.md); [`tools/metering_gateway.md`](../../../tools/metering_gateway.md); decisions D-14, D-19 to D-21
and D-24 in [`DECISIONS.md`](../../../DECISIONS.md); the first pilot's plan, [`pinakes/experiments/p4-deep-pilot.md`](../../../pinakes/experiments/p4-deep-pilot.md).
