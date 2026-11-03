# Metering gateway

`tools/metering_gateway.py` is a small local HTTP proxy that every hosted model call of an experiment passes
through. It exists because the third-party builders an experiment runs cannot do three things the
[experiments plan](../kb-kg/experiments/README.md) needs:

1. **One record per call, whichever provider.** It writes the provider's own usage fields into one common JSONL
   record, so a cost is a measured number, not an estimate.
2. **A cap that is enforced before the money is spent.** A call that could take total spend past the cap is
   answered with HTTP 429 and nothing is forwarded.
3. **The real key stays with the gateway.** The code under test holds a dummy key and the gateway's address; the
   real key is read by the gateway itself, from its own environment or from a file only its owner can read, put on
   the outgoing request, and never printed or logged.

**Status: used against one real provider.** On 20261103 the first three stages of a paid pilot sent 443 answered requests (and three
rejected ones) to OpenAI's `gpt-6-luna` for about USD 0.263; what that showed is in
[What this leaves unchecked](#what-this-leaves-unchecked). Everything else below was tested against fake upstreams on loopback,
with invented prices and made-up keys. Version 1.2.0 adds `translate_max_tokens`.

Standard library only (threaded `http.server`, `http.client`); no dependency to install. Python 3.11 or newer.
Binds `127.0.0.1` and nothing else.

## Run it

```
read -rs GATEWAY_OPENAI_KEY && export GATEWAY_OPENAI_KEY     # types nothing to the screen or the history
uv run tools/metering_gateway.py --config run1/gateway.toml [--port N] [--resume]
uv run tools/metering_gateway.py --summary run1/meter.jsonl  # totals of a finished log
```

The environment is one way to hand the gateway its key. The other is a `key_file` in the upstream's table (below): the
gateway opens the file itself, so a runner script and the builders it starts, which may run in the runner's own
process, never hold the key and need no variable.

| Argument | Meaning |
|---|---|
| `--config FILE` | The TOML config below. |
| `--port N` | Overrides the config's `port`; `0` picks a free port and prints it. |
| `--resume` | Continue a run: the spend is rebuilt from the existing log. Without it, a log that already holds records stops the start (a restart must not reset the cap). |
| `--summary LOGFILE` | Print the totals of a log (the same code as the live endpoint) and exit. The cap comes from the newest `LOGFILE.manifest-*.json` next to it. |

The gateway prints its address, cap and, for each upstream, the *name* of its key variable or the *path* of its key
file at start, and the totals when it stops (Ctrl-C or SIGTERM). Exit status 2 means it did not start.

**Fail closed at start.** It does not start without a cap, without any priced model, with a model that lacks a
price or its `source_url` / `read_at`, with an unknown key in the config (a typo would otherwise be ignored), with a
key variable that is unset (unless that upstream has `dry_run = true`), with a key file that is missing or unsafe (see
`key_file` below), or with a key that is empty, holds whitespace or control characters, or is one key pasted twice. The
messages never contain the key.

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
# key_file = "/path/outside/any/repository/openai.key"   # instead of key_env: a file the gateway reads itself
# allow_request_defaults = true     # lets a model on this PAID upstream carry request_defaults (see below)
# dry_run = true                    # no key needed and none is sent; for fake upstreams and a local model server

[upstreams.anthropic-main]
protocol = "anthropic"
base_url = "https://api.example.invalid/v1"
key_env = "GATEWAY_ANTHROPIC_KEY"

[models."fake-small"]               # the name a client puts in "model"
upstream = "openai-main"
input_per_mtok = 0.15               # per million tokens, in `currency`
output_per_mtok = 0.60
cached_input_per_mtok = 0.075       # optional; without it cached input is priced as plain input
output_limit_default = 4096         # optional; the output limit written into a chat request that sets none
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
- **The key of a paid upstream** comes from exactly one of two places. `key_env` is the *name* of an environment
  variable of the gateway process. `key_file` is a path (used as written; give an absolute one) to a file that the
  gateway opens once, at start. Giving both, or neither, on an upstream that is not `dry_run` stops the start, and so
  does `key_file` on a `dry_run` upstream. The file must be a regular file that neither group nor others can read or
  write (mode 600 or stricter; the message names the path and the mode), at most 4 KiB, and hold one non-empty line:
  the key. One trailing newline is dropped and blank lines are ignored; a second non-empty line, a space, tab or
  carriage return inside the key, an empty file, a missing path, a directory, a pipe, and bytes that are not text are
  all refused. The key then goes through the same shape check as an environment key (not empty, no whitespace or
  control characters, not one key pasted twice) and is redacted everywhere like it. A value of `key_file` that looks
  like a key (20 or more letters, digits, `_` or `-` and no `/` or `.`), or equals the value of an environment
  variable, is refused without being shown; write `./name` for a file in the working directory. No message, the
  manifest or the log ever holds key text. The manifest records `key_file` (the path only, and only for an upstream
  that sets it) the way it records the variable name.
- `request_defaults` (optional, one table per model: `[models."name".request_defaults]`, for example
  `reasoning_effort = "none"`) lists JSON fields the gateway adds to a request for that model **when the client did
  not send them**; a field the client sent, even a falsy one, always wins. It exists for a model that behaves
  differently from what the builder assumes (a model that "thinks" unless asked not to, which a builder cannot ask).
  It is refused on any upstream that is not `dry_run` (a field added to a paid call can change what it costs) **unless
  that upstream's table sets `allow_request_defaults = true`**, and it may not set `model`, `messages`, `input`,
  `stream`, `stream_options`, `n`, `max_tokens` or `max_completion_tokens` (the flag does not change that list). The
  call's log record names the fields that were added (`request_defaults_applied`), the manifest holds each model's
  table, and the body log keeps the request **as the client sent it**; the hash and the size in the record are of that
  request too, while the reservation is made from what was forwarded.
- `allow_request_defaults` (optional boolean in an `[upstreams.NAME]` table, default `false`) is the owner's explicit
  statement that models on this upstream may carry `request_defaults` although the upstream has a key. It belongs to
  one upstream: a flag on one does not open another. The manifest records it for every upstream.
- `output_limit_default` (optional positive whole number in a `[models."name"]` table; zero, a negative number, a
  boolean, a string or a fraction stops the start) bounds the output of a model whose builders send no limit. For a
  chat route (`/v1/chat/completions` and `/v1/messages`; embeddings ignore the key), when the request has neither
  `max_tokens` nor `max_completion_tokens` set to a non-null value, the gateway writes the limit into the forwarded
  body **before the output is bounded and the reservation is made**, so the reservation uses it instead of
  `default_max_output_tokens`. The field is the provider's own: `max_completion_tokens` on an `openai` upstream,
  `max_tokens` on an `anthropic` one. A limit the client sent always wins, even a very large one (nothing is
  clamped), on either field. A `"max_tokens": null`, which fast-graphrag sends on summary calls, counts as not sent:
  the gateway adds the protocol's field and leaves the client's `null` as it was sent. **OpenAI's `gpt-6-luna` rejected
  that combination (HTTP 400, `invalid_type`, parameter `max_tokens`; 20261103), and it rejected a set `max_tokens` too
  (`unsupported_parameter`); `translate_max_tokens` below is the option for such a model.** The injected field's name is added to `request_defaults_applied`, after the names of any
  `request_defaults` fields. The body log, the hash and `bytes_in` are of the client's request, as for
  `request_defaults`, and the manifest holds each model's value. It is a separate key on purpose: `request_defaults`
  still may not set a limit field.
- `translate_max_tokens` (optional boolean in a `[models."name"]` table, default `false`; version 1.2.0) is for a model that
  takes `max_completion_tokens` and rejects `max_tokens`, as OpenAI's reasoning models do. **It applies to an upstream that
  speaks the `openai` protocol (anything else stops the start) and, on a paid upstream, only with `allow_request_defaults`**,
  because it changes a paid request. On a chat request for that model, **before** the output limit is chosen: a `"max_tokens":
  null` is dropped (it then counts as not sent, as above, so `output_limit_default` is injected if the model has one); a set
  `max_tokens` is renamed `max_completion_tokens` with its value, and is then the client's own limit, so it wins over
  `output_limit_default` and is what the reservation uses. A `max_completion_tokens` that is `null` beside a set `max_tokens`
  is replaced by the rename; **a non-null `max_completion_tokens` beside a set `max_tokens` is refused** (400
  `gateway_bad_request`, nothing forwarded), because the gateway will not choose between them. A bad value (zero, negative, a
  string, a boolean, a fraction) is refused as before, after the rename. Embeddings are never touched. The call's record names
  what was done in `request_defaults_applied`: `max_tokens->max_completion_tokens` or `max_tokens(null)-dropped`, first in the
  list. The body log, the hash and `bytes_in` are of the client's request, and the manifest and the summary hold the flag for
  every model. **It is a departure from "the builder's request is forwarded as it is", and a user of the gateway must say so
  wherever a result comes from a model that has it.**

An example in prose, for a paid pilot: the upstream `openai-main` sets `key_file` and `allow_request_defaults = true`,
and the model `gpt-6-luna` on it sets `output_limit_default = 6144` and a `request_defaults` table with
`reasoning_effort = "none"`. A builder that sends only `model` and `messages` then reaches the provider with
`max_completion_tokens: 6144` and `reasoning_effort: "none"` added, the call is reserved at 6144 output tokens, its
record lists `reasoning_effort` and `max_completion_tokens` in `request_defaults_applied`, and the body log shows what
the builder sent.

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
  `max_tokens` (Anthropic); `0` (embeddings); `default_max_output_tokens` when the request sets none. A model's
  `output_limit_default` is written into the request first, so for such a model a request that sets none is reserved
  at that limit, not at `default_max_output_tokens`.
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

A voided call (a refused or failed status from the provider, a dropped connection, a timeout) is recorded at zero
cost, because no usage reached the gateway. **A provider may still bill a generation it completed for such a call**, for
example one the gateway gave up on at `upstream_timeout_s`, so the cap alone is not a guarantee against a bill. Set a
generous `upstream_timeout_s` for long answers, count the voided calls in the summary, and compare the gateway's total
with the provider's own usage page.

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
| `request_defaults_applied` | the names of what the gateway changed or added in this request: first a translation (`max_tokens->max_completion_tokens` or `max_tokens(null)-dropped`) if `translate_max_tokens` applied, then the `request_defaults` fields in the table's order, then the output-limit field if `output_limit_default` was injected (an empty list when none) |

Other files, next to `log_file`:

- `log_file.manifest-<UTC YYYYMMDD_HHMMSS_microseconds>.json`, written at every start: gateway version, SHA-256 of
  the config, cap, currency, spend carried over from a log being resumed, the upstreams (with the *names* of the key
  variables, or the *path* of a `key_file`, and each upstream's `allow_request_defaults` flag) and every model's prices
  with their `source_url` and `read_at`, its `request_defaults` and its `output_limit_default`.
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
- **The real key is in the gateway process's memory** (from the environment, or read from a `key_file`). Third-party code
  run as the same user could try to read it by other means, and a `key_file` is readable by any process of that user; that
  was not tested. What the file route guarantees is that a runner which never reads the file never holds the key. The
  mode check refuses group and other access but does not check who owns the file, and it was not tested as root.
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
- **The request body is forwarded unchanged**, except for what the config asks the gateway to add or change: the model's
  `request_defaults` (on a paid upstream only with `allow_request_defaults`), its `output_limit_default`, its
  `translate_max_tokens` (the same condition), and `stream_options.include_usage`. The recorded hash and `bytes_in` are of the body the client sent, and the body log
  holds that body, so the log does not show what was added; `request_defaults_applied` names it.

## What this leaves unchecked

- It has been used against **one real provider**: OpenAI's `gpt-6-luna`, 20261103, the first three stages of a paid pilot (the
  first ten requests and the re-test are the ones listed here; the later 432 answered requests, from four builders, all returned 200 with finish
  reason `stop`). Observed there: Chat Completions with `reasoning_effort: none`, `max_completion_tokens`, `response_format`
  `json_object` and strict `json_schema` all accepted; `usage` with `prompt_tokens_details.cached_tokens` and
  `.cache_write_tokens` and `completion_tokens_details.reasoning_tokens`; a cost computed from those fields that equals a
  recomputation from the tokens; a 401 `invalid_api_key` answered with a standard error body; a refusal at a tiny cap
  that forwarded nothing. **Not observed:** streaming, the embeddings route, Anthropic, a 429 or 5xx from a provider, a
  timeout, and the provider's own billing (OpenAI's usage page is the only check that is not the gateway's own numbers, and the
  owner makes that comparison by hand).
- The unit tests use `http.client` and raw sockets. The real OpenAI and Anthropic Python SDKs have since been pointed
  at it, but only against fake upstreams written for the purpose (`tools/exp/gateway_sdk_e2e_openai.py`, 17 checks, and
  `tools/exp/gateway_sdk_e2e_anthropic.py`, 12 checks: chat, streaming, embeddings, the key swap, exact cost, the cap).
  Pass A then pointed all four builders at it, against local models and with the stub (each runner records how it was
  pointed); a real provider came afterwards (the first bullet above).
  Behaviour with `Expect: 100-continue` or HTTP/2 is unobserved.
- TLS towards a provider is exercised only by the one real run above (the interpreter's default certificate verification
  worked from five interpreters, tested by a handshake first); the tests use plain `http://` to loopback fake upstreams.
- The suite passed on Python 3.11, 3.12, 3.13, 3.14 and 3.15 in the author's run (20261102 11:43 UTC). A second,
  independent run used one version, 3.13.18 (`uv run python`, 20261102 11:46 UTC). The header says 3.11 or newer.
- The fake upstreams are written by the same author as the gateway, so they share its reading of the protocols.
- `key_file` was exercised on macOS only. Its permission check reads the mode bits of the open file, so it means nothing on
  a file system that does not keep modes, and it cannot see a copy of the key elsewhere (a backup, a synced folder).
  A value that is not a path but is neither key-like nor equal to an environment value would still be named in the
  "does not exist" message.
- `output_limit_default` was accepted by `gpt-6-luna` as `max_completion_tokens` (eight requests); no provider has accepted
  a request that carries it together with a `null` `max_tokens` (`gpt-6-luna` rejected that). `translate_max_tokens` was tested
  against fake upstreams in version 1.2.0; `gpt-6-luna` accepted what it produces in a re-test on 20261103 (the ping and the two shapes, three requests, all answered 200).

## Tests and the mutation check

```
uv run python -m unittest tools/test_metering_gateway.py
```

136 tests, about 11 seconds, no network and no key: fake upstreams are real loopback servers written in the test
file. Green on Python 3.11, 3.12, 3.13, 3.14 and 3.15, one run each, and on three consecutive runs on 3.13
(20261102 21:08 UTC, version 1.1.0). The longer series (10 consecutive runs on 3.13, 16 runs with eight copies going
at once) were made on the earlier 78-test suite and have not been repeated on the 36 tests added since for the
output limit, the `allow_request_defaults` flag and the key file.

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

**Mutation check of version 1.1.0, 20261102 21:01 to 21:08 UTC**, same method (a copy, one anchor per mutant matched
exactly once, the unmodified copy green first, the whole suite on each copy). 42 mutants: 40 killed, 2 survived.

| Mutant | Tests red | One of them |
|---|---|---|
| `allow_request_defaults` check removed | 3 | `test_the_flag_belongs_to_one_upstream` |
| the flag is read from any upstream instead of the model's | 1 | `test_the_flag_belongs_to_one_upstream` |
| the flag missing from the manifest | 1 | `test_the_manifest_shows_the_flag_for_each_upstream` |
| the reservation made without the injected limit | 7 | `test_a_null_limit_counts_as_absent_and_the_clients_null_stays_as_sent` |
| the limit written after the reservation (injection moved below it) | 7 | the same |
| the reservation made from `default_max_output_tokens` | 17 | `test_a_reservation_that_reaches_the_cap_exactly_is_allowed` |
| a streamed request loses the injected limit | 2 | `test_defaults_and_the_injected_stream_options_both_reach_the_upstream` |
| the two field names swapped, or `max_tokens` on OpenAI | 6, 5 | `test_a_null_limit_counts_as_absent_and_the_clients_null_stays_as_sent` |
| the client's limit overwritten, or only `max_tokens` protected | 3, 1 | `test_a_limit_the_client_sent_always_wins_and_nothing_is_rewritten` |
| `null` treated as a limit that was sent | 2 | `test_a_null_limit_counts_as_absent_and_the_clients_null_stays_as_sent` |
| the key honoured on embeddings | 1 | `test_embeddings_ignore_the_key` |
| the body log holds the forwarded body | 2 | `test_the_body_log_and_the_hash_keep_what_the_client_sent` |
| `key_file` permission check removed (or group only, or others only) | 2, 1, 1 | `test_a_file_that_group_or_others_can_read_or_write_is_refused_naming_the_path` |
| the key printed in an error (two-line message, or the shape check) | 2, 4 | `test_content_that_is_not_exactly_one_key_is_refused_without_printing_any_of_it` |
| the key printed in the start banner, or in the manifest instead of the path | 1, 1 | `test_main_starts_with_a_good_key_file_and_says_where_the_key_came_from_not_what_it_is` |
| `key_env` and `key_file` both accepted | 1 | `test_exactly_one_of_key_env_and_key_file_is_needed_on_a_paid_upstream` |
| neither accepted on a paid upstream (both guards removed, or the first only) | 1, 1 | the same |
| `key_file` accepted on a `dry_run` upstream | 1 | `test_a_dry_run_upstream_takes_no_key_file` |
| a file key not redacted | 2 | `test_a_key_echoed_in_a_successful_body_is_replaced_for_a_file_key_too` |
| a pipe as `key_file` (no `O_NONBLOCK`) | hangs | the start never returns; the run was stopped at its 150 s timeout, counted as killed |

Also killed, not in the table: a flag that need not be a boolean, `output_limit_default` not validated or missing from
the manifest, `key_file` missing from the manifest, a size limit off by one in either direction, a non-regular file
accepted, two lines accepted, a key-like or environment-equal `key_file` value not refused, the shape check skipped for
a file key, and the key ignored on the `/v1/messages` route.

The two survivors. *Zero (or another falsy value) treated as an absent limit* is equivalent: the injected field is then
added, but `max_output_tokens` still refuses any non-null value that is not a positive whole number, so the request is
refused all the same and the log record is identical. *Neither key accepted* with one guard changed survived once
because the other, earlier guard still refuses; the two-guard and first-guard versions above kill it.

**Mutation check of version 1.2.0 (`translate_max_tokens`), 20261103**, same method. 22 mutants of the gateway,
the profile and the stage wiring: 21 killed, 1 survived. Killed: the null not dropped; the rename that keeps the old field or loses the
value; both limits set not refused; the flag ignored; embeddings translated too; the names not logged; the body not re-serialised when
only a translation changed it; the flag not required to be a boolean, accepted on an anthropic upstream, or accepted on a paid
upstream without `allow_request_defaults`; the flag missing from the manifest; a null `max_completion_tokens` beside a set
`max_tokens` refused; the translation after the limit choice; and the profile, config, result-block, driver and stage-A copies of the
flag. The survivor is equivalent: a bad `max_tokens` replaced by 1 before the rename leaves the bad value in `max_tokens`, where
`max_output_tokens` refuses it all the same.

Two things the first check showed about the tests themselves. The lock mutant first survived: under CPython's global
interpreter lock the check and the reservation are rarely interleaved by chance, so the concurrency tests now use
a ledger that pauses between them (`SlowLedger`) and a reservation that is held while other threads check. A mutant
that left the IPv4-mapped IPv6 unwrapping out of the loopback test also survived, because the standard library
already treats `::ffff:127.0.0.1` as loopback on 3.12 and 3.13 (measured); that code was removed rather than kept
unproven. The server only binds IPv4 loopback in any case.
