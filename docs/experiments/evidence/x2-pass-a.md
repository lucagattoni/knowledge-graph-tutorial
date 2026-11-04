---
type: page
order: 7
updated: 20261104 12:47 UTC
---

# X2 evidence: pass A on local models

This page holds the section "Pass A on local models" of the former X2 page. The text is unchanged: it was moved here on 20261104, and only the relative links were adjusted for the folder. The numbers in brackets refer to the one list in [X2 evidence: sources](x2-sources.md). Words such as "above", "below" and "the next subsection" can point to a section that is now on another page of the same experiment.

## Pass A on local models

Pass A lets a real local model answer through the gateway, so that output tokens, retries and the calls that depend on the model's text become measurable. It costs no money, and its numbers are for two small local models: `granite4.2:8b` on all four builders, and `gemma4:12b` on LightRAG alone [31].

### The first model, and why its hidden thinking was switched off

The owner chose `granite4.2:8b` from a shortlist the archive built by size and family, not by measured quality [31]. The Ollama library lists it at 5.3 GB with a 128K context window under the Apache 2.0 licence, and the first line of the licence layer in the registry reads "Apache License Version 2.0, January 2004" (whitespace normalised) [41][42][43]. The installed copy has 8.8 billion parameters at Q4_K_M quantisation and reports `tools`, `thinking` and `completion` among its capabilities [31][32]. Embeddings come from `qwen3-embedding:0.6b` (639 MB); the Ollama page and manifest state no licence for it, so its licence is **unstated** here [44][45].

Two traps in Ollama's documentation would have distorted the numbers [31]:

1. **Context length.** Ollama's default depends on video memory: 4k tokens under 24 GiB, 32k from 24 to 48 GiB, 256k from 48 GiB [37]. By that table a 32 GiB Mac falls in the 32k band; the archive nevertheless treats it as sitting "at the boundary" and does not rely on the default, and this page cannot say how much memory the GPU may use on that machine [31]. The OpenAI-compatible endpoint the builders use cannot set the context per request [31]. The fix was a derived model with an explicit 16,384-token [context window](../../index/context-window.md), and the runners refuse to start unless the model reports at least that [31].
2. **Thinking.** Many recent models write reasoning before the answer. Ollama's Modelfile reference has no parameter to switch this off, and its native chat API has a `think` field that the OpenAI-compatible endpoint the builders use does not take [39][40][38]; the builders send neither. The archive read the model's library card as showing no thinking label and proposed the model for that reason; that was wrong, because the installed model reports `thinking` [31][32]. The card's text now lists thinking among the family's features [41]. The gateway therefore gained an opt-in table of request defaults, valid in the version used for pass A only for local upstreams without a key (gateway 1.1.0 can allow it on a keyed upstream; see pass B), which adds `reasoning_effort: "none"` to every chat request and names the added field in each call's record [5][31][59]. Ollama's compatibility page lists `reasoning_effort` as a supported request field [38].

The archive measured the effect with one question, "list three prime numbers greater than 50", on the derived model at 20261102 14:27 UTC [31]:

| Setting | Time | Completion tokens |
|---|---|---|
| Default | 17.1 s | 278 |
| `reasoning_effort: "none"` | 0.3 s | 8 |
| `"low"` | 0.8 s | 15 |
| `"medium"` | 22.7 s | 598 |
| `"high"` | 9.5 s | 253 |

One question, one run per cell, so the sizes are not a measurement of real work: "none" and "low" are short, the default, "medium" and "high" are long and slow [31]. The consequence for reading everything below is stated by the archive: the builders see a model answering without its reasoning step, as a small non-thinking hosted model would [31]. The archive repeated the question on `gemma4:12b` at 19:50 UTC: 243 tokens by default, 10 tokens with `"none"`, and 207 to 262 with `"low"`, `"medium"` or `"high"`; for that model only "none" was short [31].

A derived model caps an answer at 6,144 tokens, because one Microsoft GraphRAG answer kept generating past 15,700 tokens before the cap existed and the builders set no output limit [31].

### One document each

Each builder indexed the first document of the frozen list (two to three chunks) on granite, 20261102 14:42 to 15:31 UTC [31].

| Builder | Result | Chat calls (stub) | Prompt tokens (stub) | Output tokens (stub) | Wall time |
|---|---|---|---|---|---|
| LightRAG | indexed | 4 (4) | 14,595 (11,558) | 3,296 (798) | 162 s |
| nano-graphrag | **failed** | 4 (7) | 15,570 (17,930) | 5,891 (1,810) | 266 s |
| Microsoft GraphRAG | indexed | 27 (9) | 30,479 (17,246) | 22,463 (1,525) | 1,090 s |
| fast-graphrag | indexed | 4 (3) | 13,901 (6,831) | 5,609 (932) | 272 s |

nano-graphrag needs five fields in a relationship record. The model wrote the last delimiter as `|>` instead of `<|>` in every one, so no relationship was parsed, the graph had no edges and the clustering step raised `EmptyNetworkError` [31]. The same failure occurred again at document 1 in the full run [35].

### The full run, and the owner's narrowing

The owner chose every builder to 20 documents (option B in the archive), one builder at a time, with two concurrent requests; the run started at 20261102 15:38 UTC [31][50]. The archive's arithmetic estimated 66 minutes for LightRAG's 20 documents. It took 105 minutes, and the archive then put the rest of option B at about 16 hours. At 18:28 UTC the owner replied "5 docs only", so Microsoft GraphRAG was restarted with checkpoints at 1 and 5 documents and a second fast-graphrag run was cancelled [31][50]. The 20-document figure therefore exists for LightRAG alone.

### What landed on the first model

The first model finished at 20261102 19:41 UTC [34]. These figures are read from the result files committed in the archive's `pass-a/` folder, one per builder, at archive commit `66fe6c0` on 20261102 20:15 UTC; the four files are unchanged since commit `8f780f8`, the version this page first used (checked with `git diff`, 20:16 UTC), and the whole `pass-a/` folder is unchanged at the pass-B plan's commit `9d61077` [32][33][34][35][54]. The archive page has the full tables [31]. In every run below, every call returned HTTP 200, no usage field was missing and no call was voided [32][33][34].

**At 5 documents, the same five documents for the three builders that got there**

| Builder | Chat calls | Input tokens | Output tokens | Embedding inputs | Wall time | Stub: calls, input, output | Output vs stub |
|---|---|---|---|---|---|---|---|
| LightRAG | 18 | 66,543 | 24,290 | 398 | 1,161 s | 18, 53,448, 3,636 | 6.7 times |
| fast-graphrag | 18 (3 were retries) | 52,264 | 19,457 | 176 | 874 s | 15, 34,125, 4,670 | 4.2 times |
| Microsoft GraphRAG | 91 (1 is the connectivity test) | 107,005 | 70,204 | 126 | 3,242 s | 29, 59,050, 4,418 | 15.9 times |
| nano-graphrag | stopped at document 1 | | | | | | |

Sources: result files [32][33][34][35], stub figures [24][26][27]; ratios are arithmetic. fast-graphrag's wall time is the sum of its per-document times. Microsoft GraphRAG indexes in batch, so its 5-document figure is a separate fresh run, not a continuation of its 1-document run [31]. Its 91 calls include 69 description summaries (63 for entities, 6 for relationships) where the stub's answers triggered 6, and 3 community reports where the stub's graph gave 4 [34][26].

**LightRAG to 20 documents** (the only builder with a 20-document result)

| Documents | Chat calls | Input tokens | Output tokens | Wall time | Entities stored | Embedding inputs |
|---|---|---|---|---|---|---|
| 1 | 4 | 14,595 | 3,296 | 158 s | 29 | 59 |
| 5 | 18 | 66,543 | 24,290 | 1,161 s | 203 | 398 |
| 20 | 100 (49 extraction, 49 gleaning, 2 summaries) | 401,109 | 135,391 | 6,321 s | 1,023 | 2,107 |
| Stub at 20 | 98 | 299,901 | 19,371 | | 207 | 497 |

Sources: [32], stub row [24]. At 20 documents that is 5.0 calls, 20,055 input tokens and 6,770 output tokens per document (arithmetic). The real output is 7.0 times the stub's. The run logged 234 entity lines and 104 relation lines with the wrong number of fields (dropped, nothing asked again), and 3 answers cut at the 6,144-token cap [32][20]. Across the whole granite pass, 11 of 292 chat answers hit the cap [49].

**fast-graphrag to 13 documents**

| Documents | Chat calls | Input tokens | Output tokens | Wall time | Entities stored |
|---|---|---|---|---|---|
| 1 | 4 (1 retry) | 13,902 | 5,601 | 262 s | 42 |
| 5 | 18 (3 retries) | 52,264 | 19,457 | 874 s | 176 |
| 13 | 53 (8 retries) | 154,525 | 56,380 | 2,533 s | 504 |

The 13-document row is the 14-document checkpoint minus document 14 (arithmetic); the archive's row for that checkpoint (60 calls, 176,572 input and 66,278 output tokens, 49.7 minutes) includes document 14's wasted calls [31][33]. Document 14 made 7 calls (22,047 input and 9,898 output tokens) in 449 s and stored nothing: the library's `insert` returned without an exception while none of the document's 4 chunks was stored. The runner flags that and stopped, so fast-graphrag has no 20-document figure [33]. The archive's rehearsal had shown this mode with the stub: one chunk answered in invalid JSON drops the whole document silently while the other chunks' calls are still paid for [23][31].

**Microsoft GraphRAG, 1 document, twice.** The archive's first run made 27 chat calls and 30,479 input tokens in 1,090 s. The run inside the full pass, on the same document, same model and same listed settings, made 37 calls (23 entity and 6 relationship summaries, 3 community reports, 2 extraction, 2 continuation, 1 connectivity test), 43,594 input and 22,889 output tokens in 1,097 s [31][34]. Nano-graphrag's two failed one-document runs differ in output too (5,891 and 10,815 tokens), while LightRAG's two were identical in tokens [31][32][35]. The model file fixes temperature 0 and seed 42 [32]. Why runs differ is **unstated**: it was not investigated.

### A second model, on LightRAG only

After the first model finished, the owner chose a second local model. The archive picked `gemma4:12b`: a different family (Google, where granite is IBM's), 12.4 billion parameters, and a licence layer whose opening reads "Apache License Version 2.0, January 2004" (whitespace normalised; only the opening was read, here and in the archive) [31][46][48]. It ran **LightRAG only**, to 1 and 5 documents, 20261102 19:51 to 20:02 UTC, with the same derived-copy parameters (16,384 context, 6,144-token cap, temperature 0, seed 42), the same thinking switch and the same LightRAG arguments as granite [31][36]. The decision log records it as D-28 [49].

**The two models differ in backend as well as in model.** The pull installed an MLX build (safetensors, NVFP4, 7.7 GB, runner `mlx`), where the tag's registry manifest lists the GGUF Q4_K_M build of 8.02 GB. The registry shows the plain tag `12b` with the same layers and 8.02 GB total as `12b-it-q4_K_M`, and `12b-mlx` at 7.71 GB (sums of layer sizes, read 20:16 UTC) [46][47]. That the installed copy is the MLX build, and that granite runs on llama.cpp, come from the archive's `ollama show` and server log, which this page did not re-run [31]. So a difference between the two models is not only the model. Two further consequences, from the archive [31]:

- The MLX runner logged that structured output is unavailable. LightRAG sends no `response_format`, so this run is unaffected; Microsoft GraphRAG and fast-graphrag ask for one, so they were not run on this build.
- The MLX runner honoured the Modelfile's answer cap: two answers ended at exactly 6,144 tokens although LightRAG sends no `max_tokens`.

| LightRAG | granite4.2:8b (llama.cpp, Q4_K_M) | gemma4:12b (MLX, NVFP4) |
|---|---|---|
| 1 document: chat calls, input, output tokens | 4, 14,595, 3,296 | 4, 18,673, 7,788 |
| 5 documents: chat calls | 18 | 18 |
| 5 documents: input tokens | 66,543 | 72,098 |
| 5 documents: output tokens | 24,290 | 25,070 |
| 5 documents: output in first extraction, in gleaning | 13,176, 11,114 | 19,401, 5,669 |
| 5 documents: entities, relationships stored | 203, 186 | 271, 218 |
| 5 documents: wall time | 1,161 s | 669 s |
| Answers cut at the cap, of 18 | 1 (3 of 100 at 20) | 2 |
| Lines with the wrong number of fields | 64 (40 entity lines, 24 relation lines; 338 over 20 documents) | 5 (all relation lines) |

Sources: [32][36]. The cap and wrong-field rows are the `lightrag_warning_counts` of each result file's checkpoint-5 snapshot, which count from the start of the run; granite's 20-document snapshot equals the run total of 338 and 3 truncations, which is how the 5-document counts were read as cumulative. The archive page says granite's 338 lines "cannot be compared at 5 documents" because the warnings are not split by checkpoint [31]; the result file does hold them per checkpoint, so this page gives them [32][36]. Arithmetic: gemma's 5-document output is 3.2% above granite's (25,070 against 24,290), its input is 1.35 times the stub's 53,448 against granite's 1.25 times, its output is 6.9 times the stub's 3,636 against granite's 6.7 times, and its 1-document output is 2.4 times granite's.

*Reading:* the two models differed about 13 times in format slips at 5 documents (64 wrong-field lines against 5, arithmetic) while their output volume agreed within about 3%, so equal volume does not mean equally well-formed answers. Granite's 64 include 40 entity lines; gemma logged none of that kind. The counts are LightRAG's own warnings, one draw each, with model and backend confounded.

*Reading:* at 5 documents the two models agree on output volume within about 3% and on the call count, even though they split the output differently (gemma wrote longer first answers and shorter gleaning answers, and stored more entities). At 1 document they do not agree, because two of gemma's first answers were long. One draw each, on one builder, with model and backend confounded: this shows that output volume was not wildly model-specific for LightRAG at 5 documents, not that it is stable. Nothing separates model from backend; the archive lists a run of the same model on the llama.cpp build as an open option [31].

### What the runs showed

*Reading:* three things stand out, each from one machine, a few models and one sample.

- **The stub's output was too small, by a factor of 4 to 16.** The earlier tables could count input but not output, and granite wrote 4.2 to 15.9 times the stub's output tokens at 5 documents. Gemma on LightRAG wrote 6.9 times. A hosted model will differ again.
- **Calls that depend on the model's text can dominate.** LightRAG's call count tracks the chunk count (about 2 per chunk) and matched the stub, on both models. Microsoft GraphRAG's grew with description summaries, 69 where the stub triggered 6.
- **A small model's formatting slips cost builders unequally.** nano-graphrag stopped, fast-graphrag silently lost a document, LightRAG logged 338 lines with the wrong number of fields over 20 documents on granite (64 within the first 5, against 5 on gemma) and carried on [32][33][35][36].

Wall time, first call to last call, is the honest time figure, because summed per-call latency includes waiting in Ollama's queue [31]. It is still a time on one machine, not a cost.

### Per document, for planning, and what the archive lists next

The archive gives per-document figures at each builder's largest checkpoint "for planning a paid run": the local model's own tokens, rounded, including each builder's fixed costs, so not a per-chunk rate [31]. The 20 documents hold 49 chunks [31].

| Builder and model | Checkpoint | Input tokens per document | Output tokens per document |
|---|---|---|---|
| LightRAG, granite | 20 documents | about 20,100 | about 6,800 |
| fast-graphrag, granite | 5 documents | about 10,500 | about 3,900 |
| Microsoft GraphRAG, granite | 5 documents | about 21,400 | about 14,000 |
| LightRAG, granite and gemma | 5 documents | 13,300 to 14,400 | 4,900 to 5,000 |
| nano-graphrag | none | no figure: it stopped in document 1 | |

The same page ends with four options, none started when it was written: (A) the same gemma model on the llama.cpp backend (`gemma4:12b-it-q4_K_M`, 8.02 GB), LightRAG to 5 documents, free, about 25 minutes, which would separate model from backend; (B) plan the paid pilot, which needs nothing until the owner approves a cap; (C) another builder on gemma, after checking that the MLX runner copes with `response_format`; (D) move on to X4 [31]. Option B became the plan described below, which the owner asked for, and has been run. At archive commit `c960df7` the resume file still points to the pass-A page for the other options and records no later run of them [50][85][91][96][100].
