# X2 pass A: a local model answers the builders

**Status (20261102 15:35 UTC): the owner chose `granite4.2:8b`; the model is installed, the four runners are built and agree
with the stub rehearsals through the gateway, and each builder has indexed one document with the real model (results below).
No longer run has started: the arithmetic below says a full set would take about ten hours, so it waits for the owner.**
The stub [rehearsals](README.md) counted what each builder sends. Pass A lets a real local model answer, through the [metering gateway](../../../tools/metering_gateway.md),
so that output tokens, retries and the calls that depend on the model's text become measurable. It costs no money. Its
numbers are for one small local model, not for a hosted one; what it can and cannot show is at the end.

## The machine

Read 20261102 13:59 UTC: Apple Silicon Mac, 32 GiB of memory, 294 GiB of free disk. Ollama's server is 0.40.11 and its
command-line client 0.40.13 (it prints a version warning; unrelated to this work). Installed then: `qwen3-embedding:0.6b`
(639 MB, usable for the builders' embedding calls) and no chat model; `granite4.2:8b` was pulled after the owner's choice.

## Candidates

Every model on the live Ollama library page (266, read 20261102 13:59 UTC) that was updated within about three months, is
not an embedding model and lists sizes: 34. The table covers nine whose sizes could fit this machine's memory; I chose them
by size and by family, not by measured quality. Download sizes are the sums of
each tag's layers in the registry manifest (read 14:02 UTC); context windows and capability labels are from the library
pages (read 14:00 UTC); the licence is the text of the licence layer, whose opening I read.

| Tag | Download | Context | Labels on its library card (not the model's own capability list) | Licence (opening of the licence text) | Notes |
|---|---|---|---|---|---|
| `granite4.2:8b` | 5.3 GB | 128K | none on the card; **but the installed model reports `tools`, `thinking`, `completion`** (see trap 2) | Apache 2.0 | 8.8B parameters, Q4_K_M quantisation |
| `granite4.2:30b` | 17.7 GB | 128K | none on the card; same family as the 8b, whose card was wrong, so not trusted | Apache 2.0 | |
| `gpt-oss:20b` | 13.8 GB | 128K | tools, thinking | Apache 2.0 | 20.9B parameters, MXFP4 |
| `gemma4:26b-a4b` | 18.7 GB | 256K | vision, tools, thinking | Apache 2.0 | |
| `qwen3.8:27b` | 17.7 GB | 256K | vision, tools, thinking | Apache 2.0 | updated 2 days before the read |
| `qwen3.5:35b-a3b` | 22.1 GB | 256K | vision, tools, thinking | Apache 2.0 | close to the memory limit |
| `qwen3.6:35b-a3b` | 22.6 GB | 256K | vision, tools, thinking | Apache 2.0 | close to the memory limit |
| `lfm2.5:8b` | 5.2 GB | 125K | tools, thinking | "LFM Open License v1.0"; not read beyond its opening | |
| `nemotron-3-nano:30b-a3b` | 24.3 GB (its page says 18 GB; the manifest sums to 24.3) | 256K | tools, thinking | "NVIDIA Open Model License Agreement" (24 October 2025); not read beyond its opening | too large for comfort |

The labels in this column come from the library pages and, as the next section shows, one of them was wrong for the model
that was installed. Only `ollama show` (the `/api/show` capability list) on an installed model is a source for what that
model does; none of the other eight has been installed.

What this table does not say: how well any of them follows these builders' extraction formats, or how fast they run on this
Mac. Neither is known until one is tried. I did not rank them on quality, and I have no measurement of speed.

## Two traps found in the documentation

Both are from Ollama's own pages (read 20261102 14:01 UTC), and both would silently distort the numbers.

1. **Context length.** Ollama's default context depends on memory: 4k tokens under 24 GiB of video memory, 32k from 24 to
   48 GiB. A 32 GiB Mac sits at the boundary, and the OpenAI-compatible endpoint the builders use cannot set the context
   per request. In the stub rehearsals the average chat prompt was about 1,900 to 3,100 tokens per call (arithmetic from the
   rehearsal tables), and continuation and report prompts are larger. The remedy is a derived model with an explicit
   `PARAMETER num_ctx 16384`, and `tools/exp/passa_common.py` refuses to start unless the model's context is explicitly at
   least that. Whether the allocated context really is 16,384 is then checked with `ollama ps`.
2. **Thinking.** Most recent models "think": they emit reasoning before the answer, which inflates completion tokens and
   latency. Ollama's Modelfile reference has no parameter to turn it off, and the builders do not ask. I first read
   `granite4.2:8b`'s library card (no label) as "does not think" and proposed it for that reason. **That was wrong.**
   Measured 20261102 14:27 to 14:28 UTC on the installed model (derived `num_ctx 16384` copy), same question each time
   ("list three prime numbers greater than 50"):

   | Request | Time | Completion tokens | Reasoning text | Answer |
   |---|---|---|---|---|
   | `/api/show` | | | | capabilities `tools`, `thinking`, `completion` |
   | OpenAI endpoint, nothing special | 17.1 s | 278 | 930 characters, in a separate `reasoning` field | `53,59,61` |
   | OpenAI endpoint, `reasoning_effort: "none"` | 0.3 s | 8 | none | `53, 59, 61` |
   | OpenAI endpoint, `reasoning_effort: "low"` | 0.8 s | 15 | 25 characters | `53,59,61` |
   | OpenAI endpoint, `reasoning_effort: "medium"` | 22.7 s | 598 | 2,219 characters | `53,59,61` |
   | OpenAI endpoint, `reasoning_effort: "high"` | 9.5 s | 253 | 863 characters | `53,59,61` |

   One question, one run each: the pattern (none and low short, medium and high long) is not a measurement of how much
   it thinks on real work. The model's chat template (read from `/api/show`) has an `enable_thinking` switch and a branch for
   `reasoning_effort` equal to `low`; how Ollama turns `none` into the first is not something I read, only what the
   answers above show. Remedy used here: the [gateway](../../../tools/metering_gateway.md)
   has an opt-in per-model `request_defaults` table that adds a field to a request that lacks it, only on a no-key upstream,
   and names the added fields in every call's log record. The pass-A runners take `--chat-default reasoning_effort=none`,
   and the result JSON records it. **Consequence for reading the numbers:** the builders then see a model answering without
   its reasoning step, which is what a small non-thinking hosted model does; a run with thinking left on would measure a
   different thing, and would inflate output tokens and time by an amount nobody has measured on these prompts.

## What was done

1. **Model and derived copies.** `granite4.2:8b` (5.3 GB) was pulled. Two derived models were made from it, each with
   `num_ctx 16384`, `temperature 0`, `seed 42`: `granite4.2-8b-16k`, and `granite4.2-8b-16k-cap`, which adds
   `num_predict 6144` (see "A runaway answer"). `preflight` passes on both; `ollama ps` (15:32 UTC) shows the model loaded
   with a 16,384 context, 6.46 GB, all of it in video memory. The second Modelfile, made with `ollama create`:

   ```
   FROM granite4.2:8b
   PARAMETER num_ctx 16384
   PARAMETER num_predict 6144
   PARAMETER temperature 0
   PARAMETER seed 42
   ```
2. **Speed**, from Ollama's own timing fields (`probe_speed`, 14:41 UTC): 619.9 prompt tokens per second (a 3,015-token
   synthetic prompt) and 26.8 generated tokens per second (120 tokens). While two requests ran together Ollama's log
   (read 15:03 UTC) showed about 20.5 generated tokens per second.
3. **Runners.** The four runners take the same command line, start the gateway in front of the upstream, and add
   `--chat-default reasoning_effort=none`. Against the stub through the gateway each reproduces its committed rehearsal
   (calls, input tokens, output tokens at 1, 5 and 20 documents); after the gateway change I re-ran the LightRAG,
   fast-graphrag and Microsoft GraphRAG harnesses, and checked nano-graphrag's runner against a stub. The runs below used `--chat-default reasoning_effort=none`, two concurrent requests
   (`--llm-max-async 2`, `--max-async 2`, `--concurrency 2`) and one builder at a time.
4. **One document each**, 20261102 14:42 to 15:31 UTC, first document of the frozen list (about 2 to 3 chunks). LightRAG
   and nano-graphrag ran on `granite4.2-8b-16k`, Microsoft GraphRAG and fast-graphrag on the `-cap` copy (the cap only
   matters for an answer longer than 6,144 tokens; none of the first two was).

| Builder | Result | Chat calls (stub) | Prompt tokens (stub, a different tokenizer) | Output tokens (stub) | Wall time |
|---|---|---|---|---|---|
| LightRAG 1.5.7 | indexed | 4 (4) | 14,595 (11,558) | 3,296 (798) | 162 s |
| nano-graphrag 0.0.8.2 | **failed**: no relationship was parsed, so the graph had no edges and its clustering step stopped (`EmptyNetworkError`) | 4 (7) | 15,570 (17,930) | 5,891 (1,810) | 266 s |
| Microsoft GraphRAG 3.3.0 | indexed | 27 (9) | 30,479 (17,246) | 22,463 (1,525) | 1,090 s |
| fast-graphrag 23b3a1b | indexed | 4 (3) | 13,901 (6,831) | 5,609 (932) | 272 s |

Wall time is first call to last call in the gateway log. One document is one sample: the stub column is the stub
rehearsal's figure at one document. In all four runs every call returned HTTP 200, no usage field was missing, nothing was
retried, and none of the 39 chat answers carried reasoning text (`passa_common.py facts` on each gateway directory).
Ollama accepted what the builders send: `encoding_format: "base64"` on embeddings (LightRAG), the strict `json_schema`
response format of GraphRAG's community reports, and `reasoning_effort` added by the gateway.

## What the runs showed

- **Output tokens are far above the stub's.** 4.1 times (LightRAG), 14.7 times (Microsoft GraphRAG), 6.0 times (fast-graphrag),
  one sample each. The stub's canned answers were the part of the earlier tables that could not be known; they were too
  small for this model, and a hosted model will differ again.
- **Calls that depend on the model's text differ from the stub's.** Microsoft GraphRAG made 27 chat calls where the stub
  run made 9. The difference is 20 calls that summarise a merged description (11 for entities, 9 for relationships; the
  stub's answers triggered 1), against 2 community reports (the stub run had 3). fast-graphrag made 4 extraction calls
  where the stub made 3. nano-graphrag stopped before its community reports.
- **A format slip stops a builder.** nano-graphrag needs five fields in a relationship record. The model wrote the last
  delimiter as `|>` instead of `<|>` in all of them, so every relationship was dropped and the graph had no edges. This
  is the model's slip, not the harness's. LightRAG logged the same kind of event (15 entity lines and 1 relation line
  with the wrong number of fields) and carried on. So the builders differ in how much a small model's formatting costs.
- **A runaway answer.** Before the cap, one Microsoft GraphRAG answer was still generating after 15,700 tokens (about 13
  minutes) when I stopped the run: Ollama's log showed it, and it stops only at the context limit because the builders set
  no output limit. In the capped rerun two answers hit the 6,144 cap (`finish_reason: length`) and a third stopped at 4,375.
  I read one: the model had written its entity list and then kept writing commentary about it ("No ... only ... is
  referenced", "I'll stop and use ..."). The cap bounds the time lost per event (6,144 tokens is about four to five
  minutes here); it also truncates, so a truncated answer is a different input to the builder. The cap is my choice, set
  above the longest answer that ended normally (3,093 tokens); nobody measured how often it bites.
- **Thinking is off** with the gateway default. Without it, the same model answered the same question in 17 s and 278 tokens
  instead of 0.3 s and 8 (trap 2).

## Builder facts the runner work turned up

From the four agents' reports of 20261102, each tested against the stub, not against a model, except where a row says
otherwise. I confirmed the first row in the installed source myself.

| Builder | Fact |
|---|---|
| LightRAG | `import lightrag` reads a `.env` file from the current directory (`load_dotenv(".env")` in `utils.py`, `lightrag.py`, `base.py`; confirmed in the installed 1.5.7 source), which can change its concurrency and timeouts. The pass-A runner changes into its new empty working directory first; the stub rehearsal runner imports before it does, so a rehearsal run from a directory holding a `.env` would not be comparable |
| LightRAG | Up to 3 attempts per chat and per embeddings call; the OpenAI SDK's own retries are off. An empty answer that was not cut by the length limit is retried. A worker timeout is not retried and fails the document |
| nano-graphrag | Retries stack (5 attempts by its retry library times 2 by the SDK); a community report with invalid JSON raises |
| Microsoft GraphRAG | SDK retries (2) times its own (7) can multiply calls; every checkpoint is a separate fresh index run, so the 5-document figure does not include the 1-document run |
| fast-graphrag | One chunk answered in invalid JSON drops the whole document without an exception, and the other chunks' calls are still paid for (shown with the stub); the runner flags it. Timeouts can multiply calls up to nine times per chunk (27 requests for 3 chunks against a slow stub). The retry message embeds the failed completion, so retry prompts differ by model name |
| All | The gateway voids a failed attempt, so failed or timed-out attempts carry no tokens: token sums understate what Ollama processed when attempts fail, while call counts and statuses include them. Summed latency includes time spent waiting in Ollama's queue, so wall time is the honest figure |

## Time for longer runs (arithmetic, not measurement)

Scaling each builder's one-document wall time by how its stub calls grow from one document to 5 and 20 (LightRAG 4 to 18
to 98 chat calls; fast-graphrag 3 to 15 to 80; Microsoft GraphRAG by stub output tokens 1,525 to 4,418 to 31,371, and each
checkpoint is a fresh index run). One sample each, and the runaway answers do not scale smoothly, so read each as
"within a factor of two either way".

| Builder | 5 documents | 20 documents | Note |
|---|---|---|---|
| LightRAG | about 12 min | about 66 min | one pass gives 1, 5 and 20 |
| fast-graphrag | about 23 min | about 2 h | one pass gives 1, 5 and 20 |
| Microsoft GraphRAG | about 52 min (plus 18 min for the 1-document run) | about 6.2 h | separate fresh runs: 18 min + 52 min + 6.2 h is about 7.4 h |
| nano-graphrag | does not get past document 1 with this model | | |
| **All, to 5 documents** | **about 1.8 h** | | |
| **All, to 20 documents** | | **about 10.5 h** | |

## Decision for the owner

The page's own rule was to stop and ask if the estimate came to hours. Options, with what each costs:

| Option | Machine time | What it gives | Cost |
|---|---|---|---|
| A. Up to 5 documents for LightRAG, fast-graphrag and Microsoft GraphRAG | about 1.8 h | Output tokens and call counts per chunk for three builders; enough to re-estimate pass B | No 20-document figure; nano-graphrag recorded as failing on this model |
| B. Everything to 20 documents | about 10.5 h (overnight) | The full 20-document table for three builders | The Mac is busy for the night; Microsoft GraphRAG alone is 6 h of it |
| C. A different, better-behaved model first | pull time plus a new one-document round | May avoid the format slips and the rambling; nano-graphrag might run | A new unknown: it may be slower, and thinking models need the same check |
| D. Stop pass A here and go to the paid pilot | none | Real hosted-model numbers sooner | Needs model, provider, cap and a new key (D-14); loses the free check of call counts |

## What pass A cannot show

- Output tokens of a **hosted** model. A small local model writes differently from a hosted one; pass A measures this model.
- Quality. A weaker local model will extract less well than a hosted one, so graph size, and everything downstream of it
  (summaries, community reports), may differ from a hosted run's.
- Speed on any other machine, or while other work is using this one.
- Anything about the Anthropic or OpenAI endpoints themselves: the gateway still has not met a real provider.

## Sources

Read 20261102 (UTC): the Ollama library page `https://ollama.com/library` (13:59); the tags page of each candidate,
`https://ollama.com/library/<name>/tags` (14:00); the registry manifests and licence layers,
`https://registry.ollama.ai/v2/library/<name>/manifests/<tag>` (14:02); Ollama's documentation pages
`https://docs.ollama.com/context-length`, `/openai`, `/modelfile` and `/capabilities/structured-outputs` (14:01); the local
machine through `ollama --version`, `ollama list`, `sysctl` and `df` (13:59). The helper that enforces the context check is
[`tools/exp/passa_common.py`](../../../tools/exp/passa_common.py) (13 tests; 7 mutants, all killed after two weak tests were
strengthened).
