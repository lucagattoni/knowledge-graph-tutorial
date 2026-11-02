# Metering gateway

`tools/metering_gateway.py` is a small local HTTP proxy that every hosted model call of an experiment passes
through. It exists because the third-party builders an experiment runs cannot do three things the
[experiments plan](../kb-kg/experiments/README.md) needs:

1. **One record per call, whichever provider.** It writes the provider's own usage fields into one common JSONL
   record, so a cost is a measured number, not an estimate.
2. **A cap that is enforced before the money is spent.** A call that could take total spend past the cap is
   answered with HTTP 429 and nothing is forwarded.
3. **The real key stays with the gateway.** The code under test holds a dummy key and the gateway's address; the
   real key is read from the gateway's own environment, put on the outgoing request, and never printed or logged.

**Status: never used against a real provider.** Everything below was tested against fake upstreams on loopback,
with invented prices and made-up keys. See [What this leaves unchecked](#what-this-leaves-unchecked).

Standard library only (threaded `http.server`, `http.client`); no dependency to install. Python 3.11 or newer.
Binds `127.0.0.1` and nothing else.

## Run it

```
read -rs GATEWAY_OPENAI_KEY && export GATEWAY_OPENAI_KEY     # types nothing to the screen or the history
uv run tools/metering_gateway.py --config run1/gateway.toml [--port N] [--resume]
uv run tools/metering_gateway.py --summary run1/meter.jsonl  # totals of a finished log
```

| Argument | Meaning |
|---|---|
| `--config FILE` | The TOML config below. |
| `--port N` | Overrides the config's `port`; `0` picks a free port and prints it. |
| `--resume` | Continue a run: the spend is rebuilt from the existing log. Without it, a log that already holds records stops the start (a restart must not reset the cap). |
| `--summary LOGFILE` | Print the totals of a log (the same code as the live endpoint) and exit. The cap comes from the newest `LOGFILE.manifest-*.json` next to it. |

The gateway prints its address, cap and the *names* of the key variables at start, and the totals when it stops
(Ctrl-C or SIGTERM). Exit status 2 means it did not start.

**Fail closed at start.** It does not start without a cap, without any priced model, with a model that lacks a
price or its `source_url` / `read_at`, with an unknown key in the config (a typo would otherwise be ignored), with a
key variable that is unset (unless that upstream has `dry_run = true`), or with a key that is empty, holds
whitespace or control characters, or is one key pasted twice. The messages never contain the key.

## Config

All prices below are **invented** (`FAKE-USD`, `example.invalid`). Read real prices from the provider's pages
when a run is approved and write the page and the UTC time into `source_url` and `read_at`.

```toml
[gateway]
currency = "FAKE-USD"
cap = 2.50                          # total spend the gateway will allow; required
default_max_output_tokens = 1024    # output bound for a request that sets no limit
input_bytes_per_token = 2           # input bound: body bytes / this, rounded up (smaller = more cautious)
upstream_timeout_s = 120            # per socket operation towards the provider
port = 8089
log_file = "run1/meter.jsonl"       # its directory must exist; relative paths are relative to the working directory
log_bodies = false                  # true: request and response bodies go to a separate file (see below)
# body_log_file = "run1/bodies.jsonl"   # default: log_file + ".bodies.jsonl"

[upstreams.openai-main]
protocol = "openai"                 # "openai" or "anthropic"
base_url = "https://api.example.invalid/v1"        # includes the version prefix, for both protocols
key_env = "GATEWAY_OPENAI_KEY"      # the NAME of an environment variable, never the key itself
# dry_run = true                    # no key needed and none is sent; for fake upstreams

[upstreams.anthropic-main]
protocol = "anthropic"
base_url = "https://api.example.invalid/v1"
key_env = "GATEWAY_ANTHROPIC_KEY"

[models."fake-small"]               # the name a client puts in "model"
upstream = "openai-main"
input_per_mtok = 0.15               # per million tokens, in `currency`
output_per_mtok = 0.60
cached_input_per_mtok = 0.075       # optional; without it cached input is priced as plain input
source_url = "https://example.invalid/pricing"     # where these prices were read
read_at = "20261102 10:00"          # UTC, YYYYMMDD HH:MM

[models."fake-embed"]               # an embedding model has no output: write 0, it is still required
upstream = "openai-main"
input_per_mtok = 0.02
output_per_mtok = 0
source_url = "https://example.invalid/pricing"
read_at = "20261102 10:00"

[models."fake-claude"]
upstream = "anthropic-main"
input_per_mtok = 1.00
output_per_mtok = 5.00
cached_input_per_mtok = 0.10        # Anthropic cache reads
cache_write_per_mtok = 1.25         # optional; Anthropic cache creation; without it priced as plain input
source_url = "https://example.invalid/pricing"
read_at = "20261102 10:00"
```

- Numbers may be written bare (`0.15`); the config is parsed with exact decimals, never floats.
- `source_url` and `read_at` are given once per model and cover all of its prices. They are copied into the
  manifest, so a run records where its numbers came from.
- A request for a model with no `[models.*]` entry is refused (HTTP 400, `gateway_model_not_priced`).
- A model's `upstream` must speak the route's protocol: `openai` upstreams serve `/v1/chat/completions` and
  `/v1/embeddings`, `anthropic` upstreams serve `/v1/messages`.
- Plain `http://` is accepted only for a loopback upstream (otherwise the real key would travel in clear).

## Point a builder at it

The builder is given the gateway's address and a dummy key, never the real key:

```
export OPENAI_BASE_URL=http://127.0.0.1:8089/v1      # OpenAI-protocol clients: the base URL includes /v1
export OPENAI_API_KEY=dummy
# Anthropic-protocol clients: the base URL is http://127.0.0.1:8089 (a client adds /v1/messages itself)
```

Which variable or setting a given builder reads is **not checked here**; it differs per builder and is found in
the rehearsal. The gateway controls only calls that reach it. A builder that ignored the setting and called the
provider directly would send the dummy key and be rejected by the provider, so it would cost nothing, and the
missing records would show it. The gateway does not check the client's key: any value is accepted and discarded.

Routes: `POST /v1/chat/completions`, `POST /v1/embeddings`, `POST /v1/messages` (a query string such as
`?beta=true` is forwarded), and `GET /_meter/summary`. Everything else is 404, for example `GET /v1/models`,
`/v1/responses`, `/v1/messages/count_tokens`. A client that needs one of those at start-up will fail.

Requests are refused before anything else happens when the peer is not a loopback address (403
`gateway_forbidden_peer`), the `Host` header does not name this machine (403 `gateway_forbidden_host`, so a web
page cannot reach the gateway through a rebound name), or a POST is not `Content-Type: application/json` (415, so a
web page cannot post to it across origins). The first two are not logged.

## How the cap works

Before forwarding, the gateway reserves the most the call could cost:

```
reserve = ceil(body_bytes / input_bytes_per_token) x max(input price, cache-write price)
        + max_output x output price
```

- `body_bytes` is the body that is forwarded. `input_bytes_per_token = 2` assumes no token is shorter than two
  bytes on average.
- `max_output` is `max_completion_tokens` or `max_tokens`, whichever is larger (OpenAI chat), multiplied by `n`;
  `max_tokens` (Anthropic); `0` (embeddings); `default_max_output_tokens` when the request sets none.
- If `spent + open reservations + reserve > cap`, the call is answered with **429** and a JSON error that names
  `gateway_budget_exceeded` (OpenAI-shaped or Anthropic-shaped to match the route), and **nothing is forwarded**.
  A reserve that reaches the cap exactly is allowed.
- After the response, the reservation is replaced by the cost computed from the provider's usage fields. One lock
  covers the check, the reservation, the settlement and the log write, so concurrent calls cannot take recorded
  spend past the cap.

| Outcome | Client sees | `cost` | `voided` | `usage_missing` |
|---|---|---|---|---|
| 2xx with usable usage | the response, unchanged | from usage | false | false |
| 2xx, no usable usage (or a stream that never delivered it) | the response | the whole reservation | false | **true** |
| Upstream status outside 2xx (401, 429, 500, ...) | the upstream status, headers and body (key redacted) | 0 | **true** | false |
| Connection refused / closed / cut before a response | 502 `gateway_upstream_unreachable` | 0 | **true** | false |
| Timeout before a response | 504 `gateway_upstream_timeout` | 0 | **true** | false |
| 2xx whose body is cut short | 502 `gateway_upstream_incomplete` | the whole reservation | false | **true** |
| Refused by the gateway (cap, unpriced model, bad request) | 429 / 400 / 411 / 413 / 415 | 0 | false | false (`refusal` is set) |
| Unexpected gateway error after forwarding | 500 `gateway_internal_error` | the whole reservation | false | **true** |
| Log cannot be written | the call is answered; later calls get 503 `gateway_log_failure` | | | |

Codes the gateway itself answers with (the JSON error's `type` and `code`; `refusal` in the log for the first group):

| Code | Status | When |
|---|---|---|
| `gateway_budget_exceeded` | 429 | the reservation would take spend past the cap |
| `gateway_model_not_priced` | 400 | `model` missing, not a string, or without a `[models.*]` entry |
| `gateway_route_mismatch` | 400 | the model's upstream speaks the other protocol than the route |
| `gateway_bad_request` | 400 | body not a JSON object, or a bad `max_tokens` / `max_completion_tokens` / `n` |
| `gateway_length_required` | 411 | no `Content-Length` and no chunked body |
| `gateway_body_too_large` | 413 | body over 32 MiB |
| `gateway_unsupported_media_type` | 415 | `Content-Type` is not `application/json` |
| `gateway_log_failure` | 503 | the log could not be written; nothing more is forwarded |
| `gateway_internal_error` | 500 | a bug in the gateway; if the call had been forwarded, the reservation is counted |
| `gateway_forbidden_peer`, `gateway_forbidden_host` | 403 | not logged |
| `gateway_not_found` | 404 | unknown route, not logged |
| `gateway_upstream_unreachable`, `gateway_upstream_timeout`, `gateway_upstream_incomplete` | 502, 504, 502 | see the table above |

**What the cap does and does not guarantee.** It bounds spend as the gateway computes it, from the configured
prices and the provider's usage fields; it is not the provider's bill. A call can cost more than its reservation
when a request sets no output limit and the answer is longer than `default_max_output_tokens`, when the input has
more tokens than `body_bytes / input_bytes_per_token`, or when a price is stale. The cost is then recorded as it
is, `reserve_exceeded` is true, and spend can pass the cap by that one call; later calls are refused. Keep a
per-project spend limit at the provider as well, as the plan says.

## Streaming

`stream: true` is passed through. For OpenAI chat the gateway adds `stream_options.include_usage = true` when the
client did not set `include_usage` (an explicit `false` is respected and then ends as `usage_missing`). OpenAI usage
comes from the last chunk that carries a `usage` object; Anthropic input comes from `message_start` and output
from `message_delta`, later values replacing earlier ones because the delta counts are cumulative. If the
client hangs up, the gateway keeps reading the stream so the provider's final usage still reaches the log. A
successful stream is passed through byte for byte: the real key is redacted from error bodies, headers and the body
log, but not from the live bytes of a 2xx stream.

## The log

One JSON object per line in `log_file`, written and flushed when the call ends. Money is a decimal string, never a
float. Bodies and the client's headers are never in this file.

| Field | Meaning |
|---|---|
| `ts` | UTC time the request arrived, `YYYY-MM-DDTHH:MM:SS.mmmZ` |
| `call_id` | random 32-hex id |
| `route`, `upstream`, `model_requested`, `model_reported` | the path, the configured upstream, the client's `model`, the `model` the provider reported (null if none) |
| `http_status` | the status the client received |
| `input_tokens` | all prompt tokens, cached ones included (Anthropic: input + cache read + cache creation) |
| `output_tokens` | completion tokens (0 for embeddings); null when no usage |
| `cached_input_tokens` | cached prompt tokens; null if the provider gives none |
| `cache_creation_input_tokens` | Anthropic cache writes; null otherwise |
| `cost`, `currency` | cost in `currency`, from the provider's usage and the configured prices |
| `reserve` | the reservation made before forwarding (null if the call never got that far) |
| `voided`, `usage_missing`, `streamed` | see the table above; `streamed` is true when the response was a stream |
| `reserve_exceeded` | the cost was higher than the reservation |
| `refusal` | the gateway's refusal code, or null; a refused call forwarded nothing |
| `error` | short code such as `upstream_status`, `upstream_timeout`, `stream_interrupted`, or null |
| `latency_ms` | request received until the call was settled |
| `request_sha256`, `bytes_in`, `bytes_out` | SHA-256 and size of the body the client sent; bytes sent back to the client |

Other files, next to `log_file`:

- `log_file.manifest-<UTC YYYYMMDD_HHMMSS_microseconds>.json`, written at every start: gateway version, SHA-256 of
  the config, cap, currency, spend carried over from a log being resumed, the upstreams (with the *names* of the key
  variables) and every model's prices with their `source_url` and `read_at`.
- `log_bodies = true` writes `{call_id, request, response}` per call to the body log (mode 600). Bodies can hold
  third-party text and must not be committed; keep that file outside the repository.

`GET /_meter/summary` (loopback only) and `--summary LOGFILE` return the same totals: `requests` (every record),
`calls` (forwarded), `ok`, `voided`, `usage_missing`, `refused`, token sums, `spent`, `open_reservations`, `cap`,
`remaining` (cap minus spent minus open reservations) and a `by_model` breakdown.

## Where the usage field names come from

Read 20261102 10:30 to 10:31 UTC. None of it was checked against a live response.

| Provider | Source | What it fixes |
|---|---|---|
| Anthropic | `https://platform.claude.com/docs/en/build-with-claude/streaming` (read 20261102 10:30 UTC) | `message_start` carries `message.usage` (`input_tokens`, `output_tokens`); `message_delta` carries `usage` whose counts are cumulative, and an example delta also carries `input_tokens` and the two cache fields |
| Anthropic | `https://platform.claude.com/docs/en/build-with-claude/prompt-caching` (read 20261102 10:30 UTC; the first 100,000 of 165,895 characters) | `input_tokens` counts only tokens after the last cache breakpoint; total input = `cache_read_input_tokens + cache_creation_input_tokens + input_tokens`; cache writes cost 1.25x (5 minute) or 2x (1 hour) of base input, cache reads a fraction of it that differs by model |
| OpenAI | The provider's documentation returned HTTP 403 to the fetch (20261102 10:30 UTC). Used instead: the `openai-python` type definitions on its `main` branch, which carry the header "generated from our OpenAPI spec": `src/openai/types/completion_usage.py`, `src/openai/types/chat/chat_completion_stream_options_param.py`, `src/openai/types/create_embedding_response.py`, `src/openai/types/chat/chat_completion_chunk.py` (read 20261102 10:31 UTC; commit `unstated`) | `usage.prompt_tokens`, `completion_tokens`, `prompt_tokens_details.cached_tokens`; embeddings have `usage.prompt_tokens` only; with `include_usage` an extra chunk with empty `choices` carries the total, other chunks carry `usage: null`, and an interrupted stream may lack it |

Two readings are inferences, not statements of the sources: that OpenAI's `cached_tokens` is a subset of
`prompt_tokens` (the SDK says "Cached tokens present in the prompt"; the gateway treats a larger value as unusable
usage), and that Anthropic cache writes are priced at the single `cache_write_per_mtok` whatever their TTL.

## What it does not do

- **No authentication between client and gateway.** Any program of your user on this Mac that can reach
  `127.0.0.1` can spend the cap through it. The `Host` and `Content-Type` checks only keep web pages out.
- **The real key is in the gateway process's environment.** Third-party code run as the same user could try to
  read it by other means; that was not tested.
- **No TLS on the gateway side** (loopback only) and no keep-alive: one connection per call.
- **A killed gateway loses its open reservations.** Calls in flight at that moment are not in the log, and
  `--resume` cannot know their spend. Check the provider's own usage page after a crash.
- **Client retries are separate calls.** SDKs retry a 429 or a 5xx; every retry is its own record, and a client that
  keeps retrying a refused call fills the log with refusals until it is stopped.
- **Only the three routes.** No Responses API, legacy completions, batch, files, models list or token counting.
- **Prices are the owner's input.** The gateway cannot tell that a price is stale; it records the source and time
  the owner wrote down.
- **Modalities and extras are not priced separately.** Image or audio tokens, Anthropic server tools, and the
  1-hour cache TTL premium are counted only as far as the provider's total token fields cover them.
- **The request body is forwarded unchanged**, except that `stream_options.include_usage` may be added; the
  recorded hash is of the body the client sent.

## What this leaves unchecked

- It has **never been used against a real provider**, so the wire formats are those of the sources above, not of
  an observed response. Field names or status codes that differ would show as `usage_missing` or voided calls, which
  is why the first real run should be a pilot with a small cap.
- The unit tests use `http.client` and raw sockets. The real OpenAI and Anthropic Python SDKs have since been pointed
  at it, but only against fake upstreams written for the purpose (`tools/exp/gateway_sdk_e2e_openai.py`, 17 checks, and
  `tools/exp/gateway_sdk_e2e_anthropic.py`, 12 checks: chat, streaming, embeddings, the key swap, exact cost, the cap).
  No builder has been pointed at it, and which environment variable each builder reads for its base URL is unchecked.
  Behaviour with `Expect: 100-continue` or HTTP/2 is unobserved.
- TLS towards a provider was not exercised: the tests use plain `http://` to loopback fake upstreams. The code uses
  the interpreter's default certificate verification.
- The suite passed on Python 3.11, 3.12, 3.13, 3.14 and 3.15 in the author's run (20261102 11:43 UTC). A second,
  independent run used one version, 3.13.18 (`uv run python`, 20261102 11:46 UTC). The header says 3.11 or newer.
- The fake upstreams are written by the same author as the gateway, so they share its reading of the protocols.

## Tests and the mutation check

```
uv run python -m unittest tools/test_metering_gateway.py
```

78 tests, about 9 seconds, no network and no key: fake upstreams are real loopback servers written in the test
file. Green on Python 3.11, 3.12, 3.13, 3.14 and 3.15 (20261102 11:43 UTC), on 10 consecutive runs on 3.13, and on
16 runs with eight copies going at once.

**Mutation check, 20261102 11:34 to 11:43 UTC.** The tool was copied to a scratch directory and one line at a time
changed there (each anchor matched exactly once); the suite was run without `-x` on each copy. A trivial mutant
(the budget refusal answers 200 instead of 429) was killed first to show that the harness kills. All 47 mutants
were killed and none survived. The harness was a scratch script and is not in the repository. The ones that guard
the main promises:

| Mutant | Tests red | One of them |
|---|---|---|
| remove the cap comparison | 5 | `test_the_call_that_would_cross_the_cap_is_refused_and_nothing_is_forwarded_openai` |
| flip the cap comparison `>` to `<` | 43 | `test_200_that_is_not_json` |
| `>` to `>=` (a reserve that reaches the cap exactly is refused) | 2 | `test_a_reservation_that_reaches_the_cap_exactly_is_allowed` |
| skip reconciliation (the reservation stays as the cost) | 16 | `test_openai_chat_non_streaming_with_cached_tokens` |
| drop the lock | 2 | `test_ledger_never_passes_the_cap_under_a_hammer`, `test_sixty_concurrent_calls_against_a_cap_that_fits_twenty` |
| log the real key | 1 | `test_the_key_is_in_no_file_no_summary_and_no_error_body_even_when_the_upstream_echoes_it` |
| accept a model with no price | 2 | `test_a_model_with_no_price_is_refused_and_nothing_is_forwarded` |
| treat an upstream error status as cost | 5 | `test_upstream_401_is_passed_through_and_counts_zero` |
| treat a connection failure or timeout as cost | 3 | `test_closed_connection_counts_zero` |
| skip the loopback check | 1 | `test_a_non_loopback_peer_is_refused_and_nothing_is_forwarded_or_logged` |

The remaining mutants cover key redaction, header dropping, `stream_options` injection, usage arithmetic, the
start-up checks, the log-failure stop and the chunked-body readers.

Two things the check showed about the tests themselves. The lock mutant first survived: under CPython's global
interpreter lock the check and the reservation are rarely interleaved by chance, so the concurrency tests now use
a ledger that pauses between them (`SlowLedger`) and a reservation that is held while other threads check. A mutant
that left the IPv4-mapped IPv6 unwrapping out of the loopback test also survived, because the standard library
already treats `::ffff:127.0.0.1` as loopback on 3.12 and 3.13 (measured); that code was removed rather than kept
unproven. The server only binds IPv4 loopback in any case.
