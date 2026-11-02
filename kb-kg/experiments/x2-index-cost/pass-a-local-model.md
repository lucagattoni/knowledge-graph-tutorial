# X2 pass A: a local model answers the builders

**Status (20261102 20:20 UTC): done for two local models. `granite4.2:8b` ran all four builders through the gateway, free: the owner
chose every builder to 20 documents, then narrowed the rest to 5 ("5 docs only"); LightRAG reached 20, fast-graphrag 5 (its 14th
document was dropped by the library), Microsoft GraphRAG 5, and nano-graphrag failed on document 1. Then, at the owner's
"Second local model", `gemma4:12b` (which Ollama installed as an MLX build) ran LightRAG to 5 documents: its output tokens came
about 3% from granite's. Result files are in [`pass-a/`](pass-a). Nothing paid ran.**
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

Download sizes and formats above are those of each tag's registry manifest. They are not always what a pull on this Mac
fetches: `ollama pull gemma4:12b` installed a 7.7 GB MLX build (safetensors, NVFP4) where the tag's manifest lists the 8.02 GB
GGUF build (see "A second local model"). The labels in this column come from the library pages and, as the next section shows, one of them was wrong for the model
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

   A second model, `gemma4:12b` (installed as an MLX build), also reports `thinking` and behaved the same way on the same question
(20261102 19:50 UTC): 243 tokens and 14.2 s by default, 10 tokens and 0.6 s with `reasoning_effort: "none"`, and 207 to 262
tokens with `low`, `medium` or `high`. One question, one run each: the pattern (none and low short, medium and high long) is not a measurement of how much
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
  above the longest answer that ended normally (3,093 tokens). Over the full runs it bit in 11 of 292 chat answers (LightRAG
  3 of 100, nano-graphrag 1 of 4, fast-graphrag 0 of 60, Microsoft GraphRAG 7 of 128).
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

## Results of the longer runs

Run 20261102 15:38 to 19:41 UTC, one builder at a time, on `granite4.2-8b-16k-cap`, with `reasoning_effort: none` added by the
gateway. Every figure is from the gateway's own log (Ollama's usage fields); the stub columns are the committed rehearsals'
figures at the same document count. Result files: [`pass-a/`](pass-a) (the one-document runs are in `pass-a/one-document/`).
Prompt tokens are counted by the model's tokenizer, the stub's by another, so only the output column compares like with like.

| Builder | Documents | Chat calls (stub) | Prompt tokens | Output tokens (stub) | Output, times the stub | Wall time |
|---|---|---|---|---|---|---|
| LightRAG | 1 | 4 (4) | 14,595 | 3,296 (798) | 4.1 | 158 s |
| LightRAG | 5 | 18 (18) | 66,543 | 24,290 (3,636) | 6.7 | 19.3 min |
| LightRAG | 20 | 100 (98) | 401,109 | 135,391 (19,371) | 7.0 | 105 min |
| fast-graphrag | 1 | 4 (3) | 13,902 | 5,601 (932) | 6.0 | 262 s |
| fast-graphrag | 5 | 18 (15) | 52,264 | 19,457 (4,670) | 4.2 | 14.6 min |
| fast-graphrag | 13 indexed of 14 | 60 | 176,572 | 66,278 | | 49.7 min |
| Microsoft GraphRAG | 1 | 37 (9) | 43,594 | 22,889 (1,525) | 15.0 | 18.3 min |
| Microsoft GraphRAG | 5 | 91 (29) | 107,005 | 70,204 (4,418) | 15.9 | 54.0 min |
| nano-graphrag | stopped in document 1 | 4 | 15,391 | 10,815 | | 8.1 min |

Per document at the largest checkpoint, for planning a paid run (this model's tokens, rounded; includes each builder's fixed
costs, so it is not a per-chunk rate): LightRAG about 20,100 prompt and 6,800 output tokens (20 documents); fast-graphrag
about 10,500 and 3,900 (5); Microsoft GraphRAG about 21,400 and 14,000 (5). The 20 documents hold 49 chunks.

What came out of them:

- **LightRAG** indexed all 20 documents: all 342 calls returned HTTP 200, none was retried or voided, 1,023 entities and 1,011
  relationships were stored. It logged 234 entity lines and 104 relation lines with the wrong number of fields, 19 relations it
  recovered from a wrong prefix, and 3 truncations at the cap. It made 2 more chat calls than the stub (entity summaries).
- **fast-graphrag** indexed documents 1 to 13 (504 entities, 663 relations, 45 chunks). Document 14 has 4 chunks; the library
  logged "Error during information extraction from document", stored none of its chunks and returned without an exception.
  The runner noticed the missing chunks and stopped (exit status 1). 81 calls, all HTTP 200; the OpenAI client retried none, and the library repeated two identical chat requests.
- **Microsoft GraphRAG** indexed 1 and 5 documents (separate fresh runs). Its calls are mostly description summaries (63 for
  entities and 6 for relationships at 5 documents) and the two extraction passes; 3 community reports each time. Its 7
  truncations at the cap are in the extraction passes. One relationship was dropped for a missing entity at 5 documents.
- **nano-graphrag** stopped in document 1, as in the one-document run: every relationship record had `|>` where `<|>` belongs,
  so the graph had no edges and clustering raised `EmptyNetworkError`. One of its four answers hit the cap this time.
- **The same run does not repeat exactly.** Microsoft GraphRAG on one document made 27 chat calls in the one-document run and
  37 in the full run (22,463 and 22,889 output tokens); nano-graphrag's output went from 5,891 to 10,815 tokens, and the cap
  bit in one run and not the other. LightRAG's one-document result was identical both times (4 calls, 3,296 tokens) and
  fast-graphrag's differed by 8 tokens. The model has a fixed seed and temperature 0, so the cause is outside what I set
  (concurrency and cache effects are my guess); I did not investigate. Read any single figure as one draw.

## The estimate against what happened

My arithmetic (written before the full run, scaling the one-document wall times) against the measured times:

| Builder | Documents | Estimated | Measured |
|---|---|---|---|
| LightRAG | 5 | 12 min | 19.3 min |
| LightRAG | 20 | 66 min | 105 min |
| fast-graphrag | 5 | 23 min | 14.6 min |
| Microsoft GraphRAG | 1, then 5 (fresh runs) | 18 and 52 min | 18.3 and 54.0 min |

Within a factor of two in every case, in both directions. LightRAG ran 1.6 times longer than estimated at 20 documents, and
I raised the estimate for the rest of option B from 10.5 to about 16 hours; the owner then asked for 5 documents only.

## A second local model

The owner chose "Second local model" (option A of the earlier list: the cheapest builder, LightRAG, to 1 and 5 documents, free).
I picked `gemma4:12b`: a different family from granite (Google, not IBM), 12.4 billion parameters, Apache 2.0 (the opening of
the licence layer, read 19:47 UTC), and small enough to sit beside the embedding model in 32 GiB. The 26b-a4b tag would have been
18.7 GB with under 19 GiB of memory free at the time. Pulled 19:48 UTC; a derived copy `gemma4-12b-16k-cap` with the same four
Modelfile parameters as granite's (`num_ctx 16384`, `num_predict 6144`, `temperature 0`, `seed 42`), the same
`--chat-default reasoning_effort=none`, and the same LightRAG arguments as before.

**What was installed is the MLX build, not the GGUF build the tag lists.** Evidence, 20261102 UTC:

| Source | What it says |
|---|---|
| `ollama show` (19:50) | `gemma4:12b`: format safetensors, NVFP4, 12.4B parameters, `"runner": "mlx"`, 7.7 GB. For `granite4.2:8b`: format gguf, Q4_K_M, `"runner": "llamacpp"` |
| Registry manifests (20:01) | The plain tag `gemma4:12b` is the GGUF Q4_K_M build (8.02 GB), the same manifest as `12b-it-q4_K_M`; the MLX build (7.71 GB) is the manifest of `12b-mlx` and `12b-nvfp4`. Others: `12b-mxfp8` (13.30 GB) and `12b-mlx-bf16` (24.83 GB) |
| Ollama server log (19:50) | "starting mlx runner subprocess", then "MLX engine initialized" (MLX 0.32.4, device gpu) |
| Library tags (20:01) | `granite4.2` has 49 tags and none names MLX, NVFP4 or MXFP, so granite has no MLX build in Ollama |

Why the pull chose the MLX build is not something I read; the client did it, and the sizes and the log show it. Consequences:
(1) the two models differ in model and in backend at once (llama.cpp on Metal for granite, MLX for gemma), so a difference between them
is not only the model; (2) the MLX runner logged "Structured output is unavailable" (it could not find `libollama_xgrammar.dylib`,
19:50:36 UTC). LightRAG sends no `response_format`, so this run is unaffected, but Microsoft GraphRAG's community reports and
fast-graphrag's `json_object` format ask for one, so those builders should not be run on an MLX build without checking what the
runner does with it; (3) the Modelfile's `num_predict` cap is honoured by the MLX runner: two answers ended with `finish_reason:
length` at exactly 6,144 tokens although LightRAG sends no `max_tokens`.

LightRAG, 1 and 5 documents (one pass, 19:51 to 20:02 UTC; result file: `pass-a/second-model/lightrag-gemma4-12b.json`):

| | granite4.2:8b (llama.cpp, Q4_K_M) | gemma4:12b (MLX, NVFP4) |
|---|---|---|
| 1 document: chat calls / prompt / output tokens | 4 / 14,595 / 3,296 | 4 / 18,673 / 7,788 |
| 5 documents: chat calls | 18 | 18 |
| 5 documents: prompt tokens | 66,543 | 72,098 |
| 5 documents: output tokens | 24,290 | 25,070 |
| 5 documents: output in first extraction / in gleaning | 13,176 / 11,114 | 19,401 / 5,669 |
| 5 documents: entities / relationships stored | 203 / 186 | 271 / 218 |
| Answers that hit the 6,144 cap, of 18 | not counted at 5 documents (3 of 100 at 20) | 2 |
| Wall time, 5 documents | 19.3 min | 11.1 min |
| Generation speed from the probe | 26.8 tokens/s | 30.5 tokens/s |

Reading it (one draw each, and the two differ in backend):

- **Output volume agrees at 5 documents, about 3% apart** (25,070 against 24,290), and the call count is the same, although the models
  split their output differently: gemma wrote longer first answers and shorter gleaning answers, and stored more entities.
- **One document does not agree:** gemma's output was 2.4 times granite's (7,788 against 3,296), because two of its first
  answers were long. A small run is noisy, as the repeated-run differences above also showed.
- **Format errors differ in kind.** gemma logged 5 relation lines with the wrong number of fields and 2 truncations in 5 documents;
  granite logged 338 wrong-field lines over 20 documents, which cannot be compared at 5 documents because the builder's warnings are
  not split by checkpoint.
- **For planning a paid LightRAG run,** the two models give about 4,900 to 5,000 output tokens and 13,300 to 14,400 prompt tokens per
  document at 5 documents; granite at 20 documents gave 6,800 and 20,100. A hosted model will differ from both. This is only LightRAG.

## How the full run was launched

Decision of 20261102 15:37 UTC (option B). One builder at a time, in this order: nano-graphrag (it is expected to stop at
document 1), LightRAG, fast-graphrag, Microsoft GraphRAG. Each runs under its own interpreter with a stripped environment
(`env -i`, an empty home directory) and the arguments below; the runner headers give the rest.

```
common:   --upstream-url http://127.0.0.1:11434/v1 --model granite4.2-8b-16k-cap --embed-model qwen3-embedding:0.6b
          --checkpoints 1,5,20 --chat-default reasoning_effort=none
nano:     --preflight require --max-async 2 --client-timeout-s 3600
lightrag: --preflight-min-ctx 16384 --llm-max-async 2 --llm-timeout 1800
fast:     --preflight-min-ctx 16384 --llm-concurrency 2 --llm-timeout-s 3600
ms:       --concurrency 2 --request-timeout-s 3600 --child-timeout-s 43200
```

Two settings differ from the one-document runs. fast-graphrag was given a concurrency of 2 (its default sends every chunk
of a document at once, and a queue in Ollama could then exceed the timeout). Microsoft GraphRAG's limit on one index run
was raised from 6 hours to 12, because my estimate for its 20-document run is 6.2 hours. The Mac was kept awake with
`caffeinate -i`.

**Narrowed at 18:28 UTC.** After LightRAG took 105 minutes against my 66-minute estimate, I put the rest of option B at about
16 hours, and the owner replied "5 docs only". So: Microsoft GraphRAG was stopped eight minutes into its first run and restarted
with `--checkpoints 1,5`; a second fast-graphrag run that would have continued past its dropped document to 20 was queued
and then cancelled; LightRAG's finished 20-document result and fast-graphrag's partial one are kept. The 20-document figure
therefore exists for LightRAG alone.

## Where this leaves the owner

Pass A was meant to show what the stub could not: output tokens, retries, and the calls that depend on the model's text. It
did, for two small models: output was 4 to 16 times the stub's, call counts moved with the model's text (Microsoft GraphRAG 3
times the stub's calls at 5 documents), one builder could not run at all, another dropped a document, and the same run did
not repeat exactly. For LightRAG the second model came within about 3% of the first at 5 documents. What pass A cannot do is price a
hosted run: that model writes differently. Next steps, none started:

| Option | Machine time or money | What it gives | Cost |
|---|---|---|---|
| A. The same gemma model on the llama.cpp backend (`gemma4:12b-it-q4_K_M`, 8.02 GB), LightRAG to 5 documents | Free; pull plus about 25 min | Separates the model from the backend, which the last round could not | Another 8 GB of disk; the answer may be "no difference" |
| B. Plan the paid pilot (pass B): model, provider, cap, key | Nothing until you approve a cap | A written plan with measured token ranges per document (LightRAG about 5,000 output and 14,000 prompt tokens per document at 5 documents on two local models) | Only LightRAG has two models behind it; the other builders have one |
| C. Another builder on gemma, with the structured-output hazard checked first | Free; about 30 to 60 min each | Whether the other builders' figures are model-specific | Needs a check that the MLX runner copes with `response_format`; GraphRAG's community reports may fail |
| D. Move on to X4 | none | The scoring program and agent client are the next unbuilt pieces | X2's cost question stays open |

## What pass A cannot show

- Output tokens of a **hosted** model. A small local model writes differently from a hosted one; pass A measures this model.
- Quality. A weaker local model will extract less well than a hosted one, so graph size, and everything downstream of it
  (summaries, community reports), may differ from a hosted run's.
- Speed on any other machine, or while other work is using this one.
- Anything about the Anthropic or OpenAI endpoints themselves: the gateway still has not met a real provider.

## Sources

Added 20261102 (UTC) for the second model: `ollama show` on both models and the Ollama server log (19:50 to 20:01); the registry
manifests and licence layer of `gemma4:12b`, `12b-mlx`, `12b-nvfp4`, `12b-mxfp8`, `12b-mlx-bf16` and `12b-it-q4_K_M`
(`https://registry.ollama.ai/v2/library/gemma4/manifests/<tag>`, 19:47 and 20:01); the tags pages
`https://ollama.com/library/gemma4/tags` and `https://ollama.com/library/granite4.2/tags` (20:01).


Read 20261102 (UTC): the Ollama library page `https://ollama.com/library` (13:59); the tags page of each candidate,
`https://ollama.com/library/<name>/tags` (14:00); the registry manifests and licence layers,
`https://registry.ollama.ai/v2/library/<name>/manifests/<tag>` (14:02); Ollama's documentation pages
`https://docs.ollama.com/context-length`, `/openai`, `/modelfile` and `/capabilities/structured-outputs` (14:01); the local
machine through `ollama --version`, `ollama list`, `sysctl` and `df` (13:59). The helper that enforces the context check is
[`tools/exp/passa_common.py`](../../../tools/exp/passa_common.py) (23 tests today; the first 13 had 7 mutants, all killed after two
weak tests were strengthened, and later additions had 9 more, all killed).
