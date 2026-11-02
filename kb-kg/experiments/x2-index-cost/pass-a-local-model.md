# X2 pass A: a local model answers the builders

**Status: plan and candidates. No model has been downloaded and nothing has run.** The stub [rehearsals](README.md) counted
what each builder sends. Pass A lets a real local model answer, through the [metering gateway](../../../tools/metering_gateway.md),
so that output tokens, retries and the calls that depend on the model's text become measurable. It costs no money. Its
numbers are for one small local model, not for a hosted one; what it can and cannot show is at the end.

## The machine

Read 20261102 13:59 UTC: Apple Silicon Mac, 32 GiB of memory, 294 GiB of free disk. Ollama's server is 0.40.11 and its
command-line client 0.40.13 (it prints a version warning; unrelated to this work). Installed models: `qwen3-embedding:0.6b`
(639 MB, usable for the builders' embedding calls) and no chat model.

## Candidates

Every model on the live Ollama library page (266, read 20261102 13:59 UTC) that was updated within about three months, is
not an embedding model and lists sizes: 34. The table covers nine whose sizes could fit this machine's memory; I chose them
by size and by family, not by measured quality. Download sizes are the sums of
each tag's layers in the registry manifest (read 14:02 UTC); context windows and capability labels are from the library
pages (read 14:00 UTC); the licence is the text of the licence layer, whose opening I read.

| Tag | Download | Context | Labels on its card | Licence (opening of the licence text) | Notes |
|---|---|---|---|---|---|
| `granite4.2:8b` | 5.3 GB | 128K | none (no thinking, no tools label) | Apache 2.0 | 8.8B parameters, Q4_K_M quantisation |
| `granite4.2:30b` | 17.7 GB | 128K | none | Apache 2.0 | |
| `gpt-oss:20b` | 13.8 GB | 128K | tools, thinking | Apache 2.0 | 20.9B parameters, MXFP4 |
| `gemma4:26b-a4b` | 18.7 GB | 256K | vision, tools, thinking | Apache 2.0 | |
| `qwen3.8:27b` | 17.7 GB | 256K | vision, tools, thinking | Apache 2.0 | updated 2 days before the read |
| `qwen3.5:35b-a3b` | 22.1 GB | 256K | vision, tools, thinking | Apache 2.0 | close to the memory limit |
| `qwen3.6:35b-a3b` | 22.6 GB | 256K | vision, tools, thinking | Apache 2.0 | close to the memory limit |
| `lfm2.5:8b` | 5.2 GB | 125K | tools, thinking | "LFM Open License v1.0"; not read beyond its opening | |
| `nemotron-3-nano:30b-a3b` | 24.3 GB (its page says 18 GB; the manifest sums to 24.3) | 256K | tools, thinking | "NVIDIA Open Model License Agreement" (24 October 2025); not read beyond its opening | too large for comfort |

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
   latency. Ollama's Modelfile reference has no parameter to turn it off; the OpenAI-compatible endpoint accepts
   `reasoning_effort`, but the builders do not send it. So a thinking model would run in its default thinking mode, and
   its output tokens would not resemble those of the non-thinking small hosted models (such as the `gpt-4o-mini` or
   Haiku class) that these builders are normally run with. That is why the first candidate is a model with no thinking label.

## Proposed pass A

1. Pull one model (a download of a few GB) and create a derived model with `num_ctx 16384` and a fixed seed and temperature as
   defaults. The first proposal is `granite4.2:8b`: smallest, no thinking label, Apache 2.0, and small enough that a harness
   fault should show up quickly (speed is not yet measured). A second model for sensitivity (`gpt-oss:20b` as a thinking model, or `granite4.2:30b` as a
   larger non-thinking one) only if the first run says the counts depend heavily on the model.
2. Run `preflight` and `probe_speed` (both in `passa_common.py`) and turn the measured tokens per second into a time
   estimate per builder, labelled as arithmetic, **before any full run**. If it comes to hours, stop and ask.
3. Adapt the four runners to point at the gateway instead of the stub, and check each against the stub through the gateway
   first (free, no model). This is the first time a builder talks to the gateway.
4. Run one builder at a time (the GPU is shared) on 1, 5 and 20 documents. Record, from the gateway's log: calls by kind,
   input and output tokens as Ollama reports them, per-call latency, failures and retries; and from the builder: graph size,
   parse errors, cache hits. Compare with the stub counts for the same builder.
5. Report, and stop. Nothing paid starts without its own yes.

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
