---
type: page
order: 3
updated: 20261104 13:18 UTC
---

# X2: the index cost of cheap graph builders

This page answers one question: how many model calls, how many [tokens](../index/token.md) and how many dollars does each of four cheap [knowledge-graph](../index/knowledge-graph.md) builders use per document, on the same documents with the same model? It records the frozen inputs, the free rehearsals against a stub model, pass A (complete: two small local models answered the builders) and pass B, the paid pilot on one hosted model: a written plan, its free work, and the results of all four stages. **Stages A to D of pass B have run (20261103, 16:12 to 19:01 UTC; 1,751 answered chat requests). The pilot's cost has three figures, and each means something different: USD 1.10537 is what the gateway priced as it ran (it ignored OpenAI's cache-write field); USD 1.18389 is the pilot at OpenAI's list prices, cache writes at USD 0.125 per million; USD 0.67 is what OpenAI's usage page shows as billed, which the archive explains as the list price less complimentary daily tokens that come with sharing inputs and outputs with OpenAI (D-41; the archive calls this "the better reading", and it is not a proof). So 0.67 is not a check on the gateway. The same sharing setting means the pilot's article text and the models' outputs were probably shared with OpenAI for training, which the plan had assumed would not happen; the owner chose to leave the setting on (D-42), and nothing was changed at OpenAI (subsection "Data handling").** The section "Pass B results: stages A to D" gives calls, tokens and USD per document for the four builders at one document, at five documents (twice) and at twenty documents. These are this repository's own measurements through its own gateway, on one hosted model (`gpt-6-luna`, reasoning off). No quality was measured; the numbers are not independent of the authors and are not a ranking of the builders' quality [98][99][100][112][113].

## The question

The archive's survey of cheaper graph building lists five ways to cut the cost of building a graph with a [large language model](../index/large-language-model.md), and finds that "measured index cost is absent from most card entries" [51][52]. X2 fills that gap for four builders: [LightRAG](../projects/lightrag.md), [nano-graphrag](../../kb-kg/projects/nano-graphrag.md), [Microsoft GraphRAG](../projects/microsoft-graphrag.md) and [fast-graphrag](../../kb-kg/projects/fast-graphrag.md). It measures calls, input and output tokens, and wall-clock time per document. It does not measure quality, and it does not rank the builders [51]. Its per-document figure is what a later matched-cost comparison (X3) would be priced from [51]. The chapter's other experiments are on the [chapter page](README.md).

## Method

The design, as the proposal states it [51]:

- **Same documents, one model per comparison.** Each builder indexes the same documents, with one fixed small model and each builder's own default settings. "Same settings" therefore means each builder's own defaults, which differ.
- **Counted by a gateway, not by the builder.** Every call passes through a local metering gateway that logs the provider's own usage fields in one common record, so tokens are not estimated from text [5][51].
- **Two passes.** Pass A uses a local model, which costs no money; it is done. Pass B uses a hosted small model under a spending cap the owner set: OpenAI `gpt-6-luna` with reasoning off, USD 3 in total (D-30). Its free work (stage 0) was done at archive commit `9885a3d` (decision D-31): the gateway change, the hosted setup for the four runners, the watchdog, the pre-flight, the stage-A script and the stage driver, built and checked against fake providers, with a dress rehearsal of the whole stage ladder against a fake one. The owner answered the open decisions on 20261103 (D-32, `37c922c`) and said yes to stages A to C at 16:12 UTC (D-34, `5ebbbef`). Stage A ran between 16:12 and 16:32 UTC. After the owner's comparison of OpenAI's usage page with stage A's totals (`b5545ff`), stages B and C ran from 17:19 to 17:50 UTC (D-36, `c3dec4d`). The owner then gave the yes for stage D at 17:57 UTC (D-37, `96d9007`), and stage D ran from 17:57 to 19:01 UTC (D-38, `c960df7`). Afterwards the archive found that the gateway had not priced OpenAI's cache writes (D-39; version 1.3.0, `dc58d11`), and its author read OpenAI's usage page, which showed USD 0.67 and matched neither total (D-40, `56aaece`). The archive then explained the 0.67 as the list price less complimentary daily tokens (D-41, `caf863a`) and recorded the owner's answer to leave the data-sharing setting on (D-42, `5f0c5d2`). After this documentation's notes it counted the free-token fit in the ledger file's own order, completion order (D-41 as edited, `6f59c99`). **The pilot has run to its end.** See the section "Pass B results: stages A to D", the [pass-B plan](../../kb-kg/experiments/x2-index-cost/pass-b-plan.md) and the section on pass B below [51][53][55][68][69][78][81][82][84][85][90][93][96][98][100][101][107][112][117].
- **Free groundwork first.** Before any model ran, the 20 documents were frozen, the four builders were installed in throwaway environments with pinned versions, and each was rehearsed against a stub model server that counts what arrives [5][51].

The instruments that the archive lists for this (a stub server, a statistics helper, the gateway, four pass-A runners and, for pass B, a hosted setup, a watchdog, a pre-flight, a stage-A script and a stage driver) were tested and deliberately broken by their authors. This page re-ran only the unit tests of the gateway and of the five pass-B files, one file at a time, on 20261103 16:42 to 16:44 UTC at `257c9d5`, and they pass: gateway 136 tests, hosted setup 49, stage driver 44, stage-A script 56, watchdog 92, pre-flight 54 [88]. Between `257c9d5` and `c960df7` the only code or test files under `tools/` that changed are the gateway's code and tests (`dc58d11`: version 1.3.0, which prices OpenAI's cache writes, with 8 new tests), so the counts of the other five files stand; the test functions counted at `c960df7` equal them [92][97][102][103]. From `c960df7` to `6f59c99` the only file under `tools/` that differs is the gateway's page, so no code or test file changed [106][115][120]. The gateway's tests were run again at `c960df7` (20261103 19:23 UTC): 144 tests, all pass, 11.8 s [103]; and again in a checkout holding `6f59c99` (20261104 11:19 UTC): 144 tests, all pass, 11.5 s [122]. Stages A to D put the gateway (version 1.2.0 for stage A's re-test and stages B to D; the 1.1.0 code for stage A's first two runs, which the archive infers from the plan's file times; not 1.3.0), the hosted setup, the stage-A script, the stage driver (which runs the pre-flight and starts the watchdog beside each runner) and the four runners with their builders in front of OpenAI. The watchdog was live in all 16 runs of B to D and tripped no rule, so its trips have only been exercised against fakes [94][97][99]. Version 1.3.0 has not met a real provider [101]. The [instruments page](instruments.md) has the counts of every instrument and what was not re-run [5][57][69][74].

## The frozen documents

The documents are articles from the corpus of [MultiHop-RAG](../datasets/multihop-rag.md), a news dataset built for [multi-hop question answering](../index/multi-hop-question-answering.md) [3]. The data is hosted as the Hugging Face dataset `yixuantt/MultiHopRAG`, whose files include `corpus.json`, and its card states the licence ODC-By [1]. X2 uses the corpus documents and takes no quality measurement, so the benchmark's queries are not used (this page's inference from the proposal's method and data lines [51]). See also the [dataset page](../datasets/multihop-rag.md).

**The rule.** Rank every article by the SHA-256 of its URL, written as lowercase hexadecimal, and keep the 20 smallest. It needs no random generator and no judgement. The archive says the rule was fixed before the result was looked at; that ordering cannot be checked from the repository [5]. The file `corpus.json` at revision `71ac0d0bd1f951d2d6b70311f7d2ae404e1ffa82` has SHA-256 `20b61b5ab84de84a927420c5d265b7ec8d859ae49980699958a787ade9e4d28f`, and the dataset's current revision is still that one [1][2].

**Re-checked.** An independent script re-ranked the 609 articles on 20261102 and reproduced the 20 URLs in the frozen order [2][4]. The same script gave these totals, which match the archive [2][5]:

| Item | Value |
|---|---|
| Articles in the corpus | 609, 6,297,171 characters of body text; median article 7,836 characters |
| The 20 documents | 191,571 characters and 32,453 words; mean 9,579 characters; shortest 5,112, median 8,156.5, longest 22,011 |
| Share of the corpus | about 3.0% by characters (arithmetic) |
| Mix by category | technology 6, sports 6, science 3, entertainment 3, business 2 |
| Publication dates | 20230928 to 20231224 [4] |

The list holds identifiers and sizes only. The article text comes from publishers whose terms were not checked, so it is never committed, here or in any log [5]. This documentation did not check those terms either. The paid pilot sent the 20 articles' text to OpenAI's API, and the organisation's data-sharing setting there means it was probably shared with OpenAI for training (subsection "Data handling") [112][113].

*Reading:* a rule that cannot see the text cannot favour a builder, but 20 news articles of about 1,600 words each (mean; 32,453 words over 20 articles) are one small, homogeneous sample. They say little about long documents, code or tables.

## The four builders

Versions and licences were re-read on 20261102 19:40 to 19:41 UTC; the PyPI entries of nano-graphrag and fast-graphrag and the GitHub release pages were read again at 20:15 UTC. The `LICENSE` file of each project was fetched at the exact tag or commit that was run, and its SHA-256 equals the hash the archive recorded for the installed copy [6][7][8][9][20][21][22][23].

| Builder | Version run | Released or committed | Licence (from the `LICENSE` file) | State on 20261102 |
|---|---|---|---|---|
| LightRAG | `lightrag-hku` 1.5.7, tag commit `28ff1b0` | 20260902 07:23 UTC | MIT, "Copyright (c) 2025 LightRAG Team" [6] | Still the latest release; last push 20261029 [10][16] |
| nano-graphrag | PyPI 0.0.8.2 (head of `main` is `acb35c0`) | PyPI 20241019; latest GitHub release v0.0.8 20241001 | MIT, "Copyright (c) 2024 Gustavo Ye" [8] | Last push 20260127 [12][14][17] |
| Microsoft GraphRAG | `graphrag` 3.3.0, tag commit `5faaaf4` | 20261008 18:28 UTC | MIT, "Copyright (c) Microsoft Corporation." [7] | Still the latest release; last push 20261102 07:24 UTC [11][18] |
| fast-graphrag | commit `23b3a1b` (no release or tag) | 20251101 20:45 UTC | MIT, "Copyright (c) 2024 circlemind-ai" [9] | No release or tag; PyPI 0.0.5 from 20250404; last push 20251101 [13][15][19] |

What each does at its defaults, from the archive's rehearsals:

| Builder | Chunks | Model calls per chunk | Corpus-level calls |
|---|---|---|---|
| LightRAG [20] | 1,200 tokens, overlap 100 | 1 extraction, 1 [gleaning](../index/gleaning.md) | Summaries only when a merged description has many fragments or grows long |
| nano-graphrag [21] | 1,200 tokens, overlap 100 | 1 extraction, 1 "continue" | [Community reports](../index/community-report.md) for the largest connected component |
| Microsoft GraphRAG [22] | 1,200 tokens, overlap 100 | 1 extraction, 1 continuation | Description summaries; one report per community at every level |
| fast-graphrag [23] | 3,200-character windows, overlap 400 | 1 extraction | Summaries when a merged description exceeds 512 characters; no communities |

All four were tested on Python 3.12 on Apple Silicon and installed from wheels, except `hnswlib` (nano-graphrag and fast-graphrag), which was built locally [20][21][22][23].

## The stub rehearsals side by side

Each builder indexed the 20 documents against a loopback stub that answers in the builder's own format and counts what it receives. No model, no key, no network, no money [20][21][22][23]. The stub's "shape B" answer is a plausible one: about 6 entities and 5 relations per chunk, written separately for each builder's format [5]. Every figure below was checked against the committed result files on 20261102 19:45 UTC [24][25][26][27].

| Builder | Chunks | Chat calls | Chat prompt tokens | Per document (arithmetic) | Embedding inputs |
|---|---|---|---|---|---|
| LightRAG | 49 | 98 | 299,901 | 4.9 calls, 14,995 tokens | 497 |
| nano-graphrag | 49 | 146 | 421,152 | 7.3 calls, 21,058 tokens | 234 |
| Microsoft GraphRAG | 47 | 207 | 400,764 | 10.3 calls, 20,038 tokens (without the command line's one connectivity test) | 305 |
| fast-graphrag | 80 | 80 | 187,783 | 4.0 calls, 9,389 tokens | 374 |

**How to read it.** The table is not like for like: chunk sizes differ, so fast-graphrag makes 80 chunks from the same text where the others make 47 to 49. Prompt tokens are the stub's own count (`cl100k_base`), not any provider's, and only the input side is counted, so no cost follows from it [5][20][21][22][23]. Chunk counts and extraction calls do not depend on what a model says; summaries, community reports and the size of "continue" prompts do, and are counts for the stub's answers only [20][21][22][23].

**Three findings from reading the code and the runs:**

- LightRAG's gleaning is one extra pass whatever the setting, not up to n passes; its source comment says the pass runs "only 1 time when entity_extract_max_gleaning is greater than zero" [30][20].
- fast-graphrag's gleaning never adds a call at the pinned commit. The continuation prompt is formatted with empty arguments while its system text needs a `{domain}` value, so the call fails and is caught [28][29][23].
- The smallest valid answer, with no entities, is not valid for two builders: fast-graphrag raises on it and Microsoft GraphRAG stops after extraction [22][23].

## What was found

This summary rests on the archive at commit `b24484e` (committed 20261104 12:14:06 UTC) [125][126]. All figures are first-party and not independent of the authors: this repository's own measurements, through its own gateway, on two small local models and one hosted model, except USD 0.67 and OpenAI's list prices, which are the archive's author's reading of OpenAI's pages. No quality was measured, so nothing here ranks the builders' graphs [31][51][98].

### Pass A: local models

Pass A ran two small local models through the gateway, at no cost: `granite4.2:8b` on all four builders and `gemma4:12b` on LightRAG alone [31].

**The hidden thinking.** The installed granite reports a `thinking` capability, and the builders cannot send a field that switches it off [31][32][38][39][40]. On one test question the default took 17.1 s and 278 completion tokens; with `reasoning_effort: "none"` it took 0.3 s and 8 tokens (one question, one run per setting) [31]. An opt-in gateway setting therefore adds the field to every chat request, so the builders see a model answering without its reasoning step, as a small non-thinking hosted model would [5][31][59].

**The runs on granite** [26][32][33][34][35]:

| Builder | Reached | What happened |
|---|---|---|
| LightRAG | 20 documents: 100 chat calls, 401,109 input and 135,391 output tokens | The only 20-document result |
| fast-graphrag | 13 documents | Document 14 silently stored nothing; the runner stopped |
| Microsoft GraphRAG | 5 documents: 91 chat calls | The stub's answers had triggered 29 |
| nano-graphrag | none | Stopped at document 1: a delimiter slip left no edges |

On LightRAG alone, gemma wrote 25,070 output tokens at 5 documents against granite's 24,290, with 5 wrong-field lines against 64 [32][36]. Gemma ran on a different backend than granite (MLX against llama.cpp), so model and backend are confounded [31].

*Reading:* three things stand out, each from one machine, a few models and one sample. The stub's output was too small: granite wrote 4.2 to 15.9 times the stub's output tokens at 5 documents [24][26][27][32][33][34]. Calls that depend on the model's text can dominate: Microsoft GraphRAG made 69 description summaries where the stub triggered 6 [26][34]. Formatting slips cost builders unequally: nano-graphrag stopped, fast-graphrag lost a document silently, and LightRAG logged 338 wrong-field lines over 20 documents and carried on [32][33][35].

The full tables: [X2 evidence: pass A on local models](evidence/x2-pass-a.md).

### Pass B: the paid pilot, four stages

Pass B ran four stages on 20261103, 16:12 to 19:01 UTC, on OpenAI `gpt-6-luna` with reasoning off, through this repository's metering gateway (version 1.2.0 for stage A's re-test and stages B to D; the 1.1.0 code for stage A's first two runs, which the archive infers from the plan's file times). Embeddings were local and are not counted [98][99][107][108]. The owner's yes came at 16:12 UTC for stages A to C (D-34) and at 17:57 UTC for stage D (D-37); the cap was USD 3.00 [85][96][100][107].

| Stage | What ran | Chat requests answered | USD, the gateway's figure | Stage limit (USD) |
|---|---|---|---|---|
| A | What the provider accepts; 14 requests reached OpenAI | 11 | 0.00646 | 0.10 |
| B | One document per builder | 56 | 0.03735 | 0.20 |
| C | Five documents per builder, run twice | 376 | 0.21952 | 0.60 |
| D | Twenty documents per builder, one run each | 1,308 | 0.84204 | 1.50 |
| **A to D** | | **1,751** | **1.10537** | 3.00 for the pilot |

Sources: [98][99].

**Stage D against stage C.** The arithmetic multiplied each builder's five-document cost by 5.90 (191,571 characters over 32,458) and was quoted for the owner's yes as about USD 0.65, in a range of 0.61 to 0.69 [96][100]. Stage D cost USD 0.84204 by the gateway's figure (0.90556 at list prices): 1.30 times the arithmetic's 0.648 (from the mean of the two stage-C runs, which are not independent for cost) and 1.23 times the top of the range [93][95][98][104]. For LightRAG and fast-graphrag the actual was 0.97 and 0.89 of the arithmetic; for Microsoft GraphRAG and nano-graphrag it was 1.44 and 1.45 times it [98]. Per document, on the gateway's figures, stage D cost USD 0.00418 (LightRAG), 0.00434 (fast-graphrag), 0.01154 (Microsoft GraphRAG) and 0.02203 (nano-graphrag) [98][104].

*Reading:* each stage-D figure is one run, and stage C showed Microsoft GraphRAG making 113 calls in one run and 65 in the next on the same five documents, so these are single draws, not rates [93][98]. The per-document costs fall in three bands; LightRAG and fast-graphrag are within 4% of each other and are not ordered here. It is a cost ordering on each builder's own defaults except the archive's labelled departures (concurrency 4, a 6,144-token output limit where a builder sets none, and a `max_tokens` translation used by 15 requests, 13 of them fast-graphrag's in stage D), not a quality one [84][85][99][104].

The full tables: [X2 evidence: pass B results](evidence/x2-pass-b-results.md) and [X2 evidence: pass B plan](evidence/x2-pass-b-plan.md).

### What the pilot cost: three figures

The pilot has three cost figures with three meanings; the third is not a check on the first two.

| Figure | USD | What it is |
|---|---|---|
| The gateway's, as run | 1.10537 | The 1,751 answers priced at 0.10 (input), 0.01 (cached input) and 0.50 (output) per million tokens. The gateway read only `cached_tokens`, so it priced the 3,140,582 tokens OpenAI reported as written to its cache as plain input [98][99][104] |
| At list prices | 1.18389 | The same tokens with cache writes at 0.125 per million (1.25 times the input rate), as the archive's author read OpenAI's pages on 20261103 (this documentation did not). The gateway's figure was low against it by 0.0785 (7.1% of the gateway's figure) [98][101][113] |
| Billed | 0.67 | What OpenAI's usage page shows for the whole pilot, as the archive's author read it. The archive's better reading, not a proof: the list price less complimentary daily tokens [108][112][113] |

The gateway applied a cache-write price only to Anthropic usage, so the price sat unused in the run profile. Version 1.3.0 reads the field but has not met a real provider; the pilot was not re-run [100][101][107][109][111].

**Why the billed figure is lower.** The archive's author read the console's Data controls as showing the organisation sharing inputs and outputs with OpenAI and enrolled for complimentary daily tokens [112][113]. The ledger fits a 2.5-million-token allowance when the calls are counted in the ledger file's order, which is completion order: all four console lines then fall inside the console's rounding [117][118]. A 250-thousand-token allowance does not fit [116]. The archive calls the 2.5-million reading "the better reading", not a proof [113][118].

**Settled, as far as the archive's and this documentation's checks go.** 0.67 is a billed amount, not a check on the gateway. The console's cache-writes line fits 0.125 per million (0.2751 on the tokens after the 2.5-million crossing, against the console's 0.275; 0.10 would give 0.22), so 1.18389 is the pilot's value at list prices. A re-read on 20261104 gave the same 0.67 [112][113].

**Not settled:**

- The fit depends on the order: in start-time order the output line is 0.4% low. The archive tried two orders, chose the second after the gap showed in the first, and cannot tell whether OpenAI counts by completion [112][117][118].
- `gpt-6-luna` is on neither list of models in the console's tooltip [113].
- Whether the crossing call is billed in part or in full: the output line is 0.3885 or 0.3893 either way, both inside the rounding [118].
- The cache-writes and plain-input lines rest on a body log outside the repository; this documentation could check only their sum [117][118][121].
- The project's limit shows USD 5.00 against the plan's USD 3; whether it is hard is unstated [107][108].
- When the sharing setting was turned on is unstated. The allowance applied on 20261103, which suggests the setting was on before the pilot [113].
- The owner's earlier "Agrees" for stages A to C were against the gateway's figures, and no file holds the console's figures for them [96][100][108].

*Reading:* the gap between the gateway's figure and list price is 5.4% to 7.5% of the gateway's figure in each stage and does not change the order of the builders [104]. *Reading:* the match in completion order is narrow: two tails, one at the edge of the console's rounding [121].

### Data handling

The plan assumed that OpenAI's API data is not used for training unless the owner opts in (OpenAI's data page, read by the plan's author at 20:36 UTC on 20261102; this documentation did not read it). The owner answered yes to sending the 20 articles' text (D-32) [53][81].

The archive found afterwards (D-41, 20261104) that "Share inputs and outputs with OpenAI" is enabled for all projects of the organisation, and that the tooltip ties the complimentary daily tokens to shared traffic [112][113]. So the pilot's article text, the builders' prompts and the models' outputs were probably shared with OpenAI for improving and training its models. The archive writes "probably", and this documentation keeps the word [112][113]. Only chat requests went to OpenAI; embeddings were local [93][98].

The archive records that the owner chose to leave the setting on: "Leave it on" (D-42, 20261104 10:51 UTC). It stays enabled, the complimentary tokens continue, nothing was changed at OpenAI (the archive's statement), and what was sent cannot be recalled [112]. While it is on, anything sent through this organisation's OpenAI key is shared, so a later paid run that would send non-public text must say so in its yes (D-14) [112].

Unknown or unchecked:

- When the setting was turned on. The archive's author read the console's Sharing page as saying only traffic sent after that is shared [113][123].
- The publishers' terms. The archive describes the articles as the corpus's public text; the dataset's card states ODC-By [1][112]. Neither the archive (D-32) nor this documentation checked the publishers' own terms [112][113].

### The pilot's close

The archive records the pilot's key as revoked and its file as removed (D-43, 20261104 12:13 UTC). The owner reported both done. The archive's author checked at 12:13 UTC that the project's only key is listed as Revoked and that the file is absent (existence only; it was never opened). This documentation did not read the console [125].

The key's permissions were shown as "All", although the plan asked for a restricted key [125].

Still open, and the owner's:

- The project's limit shows USD 5.00 against the plan's USD 3; whether it is hard is unknown [125].
- Whether to keep or delete the private pilot directory, which holds the ledger and the body log with the written-token counts behind the cache-write correction (D-39); the committed ledger's written-token field is empty [98][125].

No further paid step is approved, and D-37 does not cover a repeat of stage D [100][112][125].

## What the experiment cannot show

- **Output tokens of another model.** Pass A measures two local models, quantised, with thinking off: granite (8.8 billion parameters) on four builders and gemma (12.4 billion) on LightRAG only, on two different backends. Stages B to D measure one hosted model, `gpt-6-luna` with reasoning off, at 1, 5 and 20 documents; at five documents its output was 0.61 to 1.63 times granite's for the three builders granite reached, and at twenty 0.97 times for LightRAG, the one builder granite reached at that size. Another model, or this one with reasoning on, writes differently [31][93][95][98][104].
- **Quality.** A weaker model extracts less, so graph size and everything downstream (summaries, reports) may differ from a hosted run's. X2 has no quality measurement by design [31][51].
- **A ranking.** Each builder runs on its own defaults, in its own chunk sizes, and nano-graphrag has no result on granite at all [20][21][22][23][35]. The cost ordering at five and at twenty documents (results section) is a cost ordering, not a quality one [93][98].
- **A rate.** The rows are single draws on 20 (or 5, or 13) news articles, and the same document gave different counts on a repeat. A second model agreed within 3% at 5 documents and not at 1, so neither "a rate" nor "model-independent" is shown [31][32][36]. On the hosted model the same five documents gave 113 and 65 calls for Microsoft GraphRAG in two runs, and the two runs are not independent for cost; stage D is one run per builder, so its spread is unknown [93][98].
- **Model against backend.** The second model changed both at once [31].
- **Speed elsewhere.** Wall time is for one machine; speed on another machine, or while other work uses this one, is unknown, and the cap on answer length bites at an unmeasured frequency [31].
- **The bill, exactly.** The pilot is USD 1.10537 as the gateway priced it, 1.18389 at OpenAI's list prices (cache writes at 0.125 per million, which the gateway, 1.1.0 and 1.2.0, left out) and USD 0.67 as OpenAI billed it, per the archive's better reading: the list price less complimentary daily tokens. The archive read OpenAI's usage page on 20261103 and again on 20261104 (this page did not), and requests, input tokens and cache hit rate equal the ledger's. What is not shown: that the allowance is the reason (the archive does not call it a proof); whether OpenAI counts the allowance in completion order, which the fit needs for all four lines (in start-time order the output line is 0.4% low; this page found the file's order and the archive recorded both orders, second *Reading:* in "What the console showed"); how OpenAI applied the allowance to a model that its tooltip does not list; the split of the cache-writes and plain-input lines, which rests on the body log; and the sharing setting's start date. The page's smallest bucket is a day, so it cannot say which stage or builder a difference belongs to. The owner's earlier "Agrees" for stages A to C was against the gateway's figures, and no file holds the console's figures for them [96][98][100][107][108][112][113][117][118].
- **Where the pilot's text went.** The 20 articles' text, the builders' prompts and the models' outputs were probably shared with OpenAI for improving and training its models, because the organisation's sharing setting is on for all projects (D-41); the plan had assumed API data is not used for training unless the owner opts in. The owner chose to leave the setting on (D-42), and the archive writes that what was sent cannot be recalled. When the setting was turned on is unstated, and the publishers' terms were checked neither by the archive nor by this page (subsection "Data handling") [112][113].
- **Money beyond twenty documents.** Cost per document is measured at 1, 5 and 20 documents on one hosted model, through the repository's own gateway (16 runs of B to D). Stage D is one run per builder on 20 articles. Nothing is measured at corpus scale (609 articles, 32.9 times the 20), where every figure is arithmetic, and for Microsoft GraphRAG and nano-graphrag the cost per character was still rising between five and twenty documents. The first five documents average 6,492 characters against 10,340 for the corpus and the twenty 9,579, so a per-document figure from either is not a corpus average [93][95][98][104].
- **Anything about a real provider beyond stages A to D.** The gateway (version 1.2.0, and the 1.1.0 code in stage A's first two runs), the hosted setup, the stage-A script, the stage driver, the watchdog and the four runners have met OpenAI's chat completions endpoint only in these four stages; gateway 1.3.0 has met no provider. Streaming, the embeddings route (local in this pilot), Anthropic, a 429 or 5xx, timeouts, the account's rate-limit tier and the effect of the provider's prompt cache on a cold start are unobserved; the watchdog was live in 16 runs and tripped nothing, so its trips have only been exercised against fakes [31][53][68][84][86][93][97][98][101].
- **Maintenance.** nano-graphrag's last GitHub release is 20241001 (PyPI 20241019), and fast-graphrag has no GitHub release or tag (PyPI 0.0.5, 20250404); the numbers say nothing about whether either will be updated [12][13][14][15][17][19].
- **Query-time cost.** Only indexing is counted [20][21][22][23].

## Where the evidence is

The full text of the former page is on five pages of its own. Nothing was cut.

| Page | What it holds |
|---|---|
| [X2 evidence: pass A on local models](evidence/x2-pass-a.md) | The local runs, the first model and why its hidden thinking was switched off, one document each, the second model, what the runs showed |
| [X2 evidence: pass B results, stages A to D](evidence/x2-pass-b-results.md) | The paid pilot's four stages, the correction for the gateway's missing cache-write price, the console comparison, the allowance fit, data handling, corpus-scale arithmetic, the readings, and what this page checked |
| [X2 evidence: pass B, the plan and how it ran](evidence/x2-pass-b-plan.md) | The plan, its decisions and facts, the cost arithmetic, the ladder, the free work, the stage-A procedure, the stage driver and the dress rehearsal |
| [X2 evidence: sources](evidence/x2-sources.md) | The numbered sources of the X2 pages |
| [All evidence pages](evidence/README.md) | A map of the evidence pages of every experiment page and of the instruments |

## Sources

The numbers in brackets refer to the list in [X2 evidence: sources](evidence/x2-sources.md), which holds every source of the X2 pages with the time it was read.
