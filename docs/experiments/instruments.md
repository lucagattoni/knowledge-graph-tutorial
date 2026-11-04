---
type: page
order: 1
updated: 20261104 13:18 UTC
---

# Instruments

This page describes the measuring tools built before any money is spent on an experiment: a metering gateway, a stub model server, a statistics helper, the frozen document and question sets and, for the paid pilot, a hosted setup for the four runners, a watchdog, a free pre-flight, a stage-A script and a stage driver. It says how each was tested, what it has met so far and what is still missing. The state is as of the archive's main branch at `b24484e` (committed 20261104 12:14:06 UTC, read 20261104 10:50 to 12:31 UTC) [69][75][81][82]. The tools are as at `c960df7`, where the tests were run (read 19:19 to 19:38 UTC) [56]; between that commit and `b24484e` only the gateway's page differs in `tools/`, and the gateway's 144 tests were run again at `5f0c5d2` and at `6f59c99` [73][75][79][81][82].

## Why they come first

Every paid step reuses the same tools, and the free rehearsals remove the largest unknown (calls and input tokens per document) before a cap is asked for. This is Step 0 of the [order and gates](README.md) [1]. The owner approved building it and it was built on 20261102 (decision D-25) [2]. No model was called and no key was used while building it [2]. The pass-B plan has a "stage 0" of its own, the free work before its first paid call; all of it was done at `9885a3d`, and the section on the paid pilot's tools below says what each part is [22][32]. Stages A to D, the four paid steps, were then run with these tools on 20261103 (below) [41][42][50][58].

## The metering gateway, in brief

The gateway is a local HTTP proxy through which every hosted model call passes. It computes each call's cost from the usage fields it reads and its configured prices, and refuses a call when its own worst-case estimate would pass a cap. It keeps the real key out of the builders' environment, arguments and logs; but a key file is readable by any process of the same user, the gateway does not authenticate its clients, and key files were tested on macOS only [3][22]. At the archive commit `b24484e` it is version 1.3.0 with the code of `c960df7`; stages B to D ran on 1.2.0 [57][58][63][82].

### Records, cap and refusal

Each call leaves one JSON line: tokens, models, cost, reservation, outcome, timing, request hash [3][57]. Usage comes from the provider's response fields: OpenAI's `prompt_tokens`, `completion_tokens`, `cached_tokens` and, from 1.3.0, `cache_write_tokens`; for Anthropic, a stream's start and last delta events (non-streamed usage unstated). No real Anthropic response has been observed [3][4][6][22][57].

Before forwarding, it reserves a worst case (body size over an assumed minimum bytes per token, plus the maximum output) and answers HTTP 429 if spend so far, open reservations and that reserve would pass the cap. Afterwards the reservation is replaced by the cost from usage (the whole reservation if usage is unusable; zero, `voided`, on a provider error). The cap bounds spend as the gateway computes it, not the provider's bill: a call can cost more than its reservation (`reserve_exceeded`), and a voided call is recorded at zero though a provider may bill it [3].

### Request defaults and the paid run

An opt-in table adds fields such as `reasoning_effort: "none"` to requests that lack them. On a paid upstream it needs `allow_request_defaults = true`; `gpt-6-luna` accepted the switch [3][41][51][58].

| Version, commit, committed (UTC) | Added |
|---|---|
| 1.1.0, `1e1b37c`, 20261102 21:12 | Paid-upstream defaults, an output limit, a key file [3][7][25] |
| 1.2.0, `a446479`, 20261103 16:38:51 | A labelled `max_tokens` translation: stage A drew a 400 for a set and a null one (D-35) [39][40][41][42] |
| 1.3.0, `dc58d11`, 20261103 19:14:09 | Pricing of OpenAI's cache writes [56][57] |

Versions up to 1.2.0 did not price OpenAI's cache writes: they ignored `cache_write_tokens` and charged written tokens as plain input; 1.3.0 prices them. OpenAI reported 3,140,582 written tokens over the 1,751 answers; the stage-A cost check could not show the gap. The committed ledger holds no write count (`cache_creation_input_tokens` is null in all 2,510 records); the counts come from the stage totals, which come from a body log outside the repository [57][58][59][65][67].

### Tests, and what it has met

144 tests pass (20261104 11:19 UTC, `6f59c99`); code and tests are unchanged since `c960df7` [79][82]. Mutants (47, 12, 42, 22, 12) are the archive's record of its builder's and its own checks: all killed but two it calls equivalent [3][12][25][39][40][57]. This page re-ran only the cap mutant: with the cap check removed from a copy (green before), 6 of 136 tests failed at `257c9d5`; not repeated at `c960df7` [10][44][56]. The fake providers were written by the gateway's author and share its reading of the protocols [3].

Beyond fakes, it has met one real provider, OpenAI's `gpt-6-luna`, on 20261103 [41][50][51][58][59]. Not met: streaming, the embeddings route, a 429 or 5xx, a timeout, Anthropic's servers, and 1.3.0 on a real provider [3][22][40][41][50][51][52][58][59].

[Instruments evidence: the metering gateway](evidence/instruments-gateway.md).

## The stub model server

A loopback server that speaks the OpenAI chat and [embeddings](../index/embedding.md) protocols, needs no key and reaches nothing beyond `127.0.0.1`. A builder is pointed at it instead of a model; it records every call and answers with whatever a responder function returns. It therefore counts a builder's calls and prompt sizes for given documents without spending anything [13].

What it can and cannot show is stated in its own header. Prompt sizes and any call count that does not depend on what the model says are exact for the given input. Anything driven by the output (gleaning loops, retries, summaries triggered by growing descriptions, community reports) is a count for the responder's answers only. Token counts use a public tokenizer (`cl100k_base`) or characters divided by four, neither of which is any provider's own [13]. Pass A later showed how far this can be from a real model: one local model wrote 4.1 to 14.7 times the stub's output tokens in the three builders that indexed a document, and Microsoft GraphRAG made 27 chat calls where the stub run made 9, on one document each. At 5 documents the ratios were 4.2 to 15.9 for the three builders that got there, and the second local model wrote 6.9 times the stub's output on LightRAG [8].

Eight tests pass (run 20261103 16:44 UTC at `257c9d5`, in 3.0 s; the stub's last commit is `8edc27c`, committed 20261102 10:24 UTC) [10][39][44]. The archive records that one failed on first run because the listen queue held 5 and a burst of 20 parallel calls was undercounted; the queue is now 256 and breaking that on purpose turns the test red [14].

## The statistics helper

Four functions for the later comparisons, standard library only [15]:

| Function | Computes |
|---|---|
| `paired_counts` | The questions only one of two runs got right |
| `sign_test` | The exact two-sided p-value for those pairs, under "each discordant pair is a fair coin" |
| `wilson` | A Wilson interval for a proportion |
| `bootstrap_mean_diff` | A seeded, paired, percentile bootstrap of a mean difference |

Its header says what it does not do: it says nothing about whether a comparison is fair, whether questions are independent, or whether the sample is large enough to matter [15]. Seventeen tests pass (run 20261103 16:44 UTC at `257c9d5`; the helper's last commit is `f64ad55`, committed 20261102 10:29 UTC), each checked in the archive record against an independent oracle such as brute-force enumeration [10][14][39][44].

## The frozen sets

### X2: twenty documents

The rule was fixed before the result was looked at and involves no choice: rank every article of the [MultiHop-RAG](../datasets/multihop-rag.md) corpus (a news dataset for [multi-hop question answering](../index/multi-hop-question-answering.md)) by the SHA-256 of its URL and keep the 20 smallest. The selection tool refuses a corpus file whose hash differs from the pinned one [16].

Re-checked for this page: the corpus file at the pinned Hugging Face revision hashes to the pinned value (`20b61b5a...e4d28f`), and running the selection tool on it reproduces the committed list of 20 rows byte for byte (20261102 19:38 UTC) [17]. The article text is never committed, because the news text comes from publishers whose own terms were not checked; only identifiers and sizes are [14]. Seven tests pass (run 20261103 16:44 UTC at `257c9d5`; the tool's last commit is `8edc27c`) [10][39][44]. The dataset itself has its own page in the datasets chapter: [MultiHop-RAG](../datasets/multihop-rag.md).

### X4: twenty questions

Ten questions on each of two public repositories, with answers a person can check, fixed before any [agent](../index/agent.md) or [code-graph](../index/code-graph.md) tool has seen them [18].

| | Flask | Gin |
|---|---|---|
| Pinned commit | `49943b5a...e620e`, committed 20261030 15:05 UTC | `0f09c3a9...ab646`, committed 20261010 04:20 UTC |
| Licence, as GitHub's licence detection reads the `LICENSE` file | BSD-3-Clause | MIT |
| Language | Python | Go |
| Questions | 10 | 10 |

Both commits exist and carry those dates. GitHub's licence detection returns those identifiers for each repository's default branch, and the `LICENSE` text at each pinned commit opens as BSD-3-Clause (Flask) and MIT (Gin) (read 20261102 20:11 UTC) [19]. The pilot is the first three questions of each file, chosen by position and never by result. The answers were derived by independent methods that had to agree (text search and reading the code; program analysis; a third check on a fresh clone for the pilot), with no code-graph tool involved. The archive records that the assistant that froze the sets re-derived nine of the twenty (20261102 10:44 to 10:50 UTC) by a method sharing no code with the agents' tools, including all six pilot answers; this page did not repeat that [18].

Limits the archive states: the questions test static structure only; independence is partial (one agent ran all methods per repository); the question wording has not been tried on any agent; and the helper programs that derived the answers live in a scratch directory and are not committed [18].

## The paid pilot's tools, in brief

The archive says builder agents wrote these tools and its author checked them: tests re-run, pieces driven against a real gateway process and a fake provider [22][25][28][32]. On 20261103 each met one real provider, OpenAI's `gpt-6-luna`, in 16 runs (the stage-A script in stage A) [41][50][51][58]. The test counts passed at `257c9d5` (20261103 16:42 to 16:44 UTC); the files are unchanged since [44][56][82].

| Tool | What it does | Tests | Real run |
|---|---|---|---|
| Hosted setup for the four runners | A profile (with the key file's path, never a key) starts a gateway for chat, embeddings local at price zero, one ledger [25][26] | 49 | Used by all four runners in 16 runs (counts matched the rehearsals only against a fake paid upstream) [25][51][58] |
| Free pre-flight | Prints the expected cost, limits and cap to write; exits 1 if the estimate does not fit [25][26] | 54 | Before each of 16 runs; none refused. Actual spend was 24% above its estimate in stage B, 3% and 10% under in the two stage-C runs, and 35% above in stage D (estimates: arithmetic from local-model tokens) [51][58] |
| Watchdog | Reads the gateway's logs and applies eight stop rules (among them provider errors, repeats, spend); on a trip it stops the processes [26] | 92 | Beside all 16 runs, tripped nothing. No run held a fault it is meant to catch, so this does not show it would stop one [51][52][54][58][59] |
| Stage-A script | At most 12 calls and USD 0.10 per run [27][28][46] | 56 | Three runs: 14 requests reached OpenAI, 11 answered, USD 0.00645713 by the gateway [41][46] |
| Stage driver | Runs one stage builder by builder with pre-flight and watchdog [30] | 44 | 16 runs, all `completed`. None tripped, was refused by the pre-flight or failed by its own fault, so those paths have met only fakes [51][58] |

Not tested: the watchdog on Linux (the key file was exercised on macOS only); a watchdog trip, a pre-flight refusal or a driver stop on a trip under a real provider; a builder's own set `max_tokens` on the hosted path [3][25][26][30][33][51][52][58][59].

### The dress rehearsal

Run 20261102 23:48 to 23:58 UTC, free, with the real tools against a fake provider: 573 checks (295 over the whole ladder, 278 over 16 injected faults, one per run) [32][34]. It found a design error in the watchdog's repeat rule. It also showed that the cap does not check what a provider reports: two runs against a fake that reported 3,000 times the tokens a real output limit allows spent USD 1.18 and 1.11 against an allowance of USD 0.20. The archive does not expect a real provider to do this [31][32][33].

### Where the pilot stands

At the archive commit `b24484e` the pilot has run to its end: stages A to C under the owner's yes of D-34 (recorded 20261103 16:12 UTC) [39][42], and stage D, 20 documents for each of the four builders, one run each, under D-37 [54][58][60][83]. D-37 covers no repeat of stage D, other model or provider; no further paid step is approved [58][60]. On 20261104 the archive found the organisation's data-sharing setting on for all projects, so the pilot's article text and outputs were probably shared with OpenAI (when it was turned on is unknown to the archive). The owner left it on (D-42); while it stays on, traffic through this organisation's key is shared [58][60][70][71].

[Instruments evidence: the paid pilot's tools](evidence/instruments-pilot-tools.md).

## How each instrument is tested before money is spent

This is the plan in the archive's experiments record (decision D-24), with the state of each line [1][18].

| Instrument | Test before money | State |
|---|---|---|
| Gateway | Counted usage equals the stub's reported usage; the call that would pass the cap is refused and nothing is forwarded; an upstream error or a 401 counts as zero; a builder given only the gateway's address and a dummy key cannot reach the provider another way; break the cap check on purpose and the test must turn red | Done against fake providers (144 tests at `c960df7`, `5f0c5d2` and `6f59c99`); the red-on-break check re-run above (6 tests red of 136, at `257c9d5`). Version 1.1.0 was also driven by hand against a fake provider: the key arrived in the header, the body carried the reasoning switch and the output limit, a client's own limit and effort won, the recorded reservation equalled the author's formula to the last digit, and no file or output held the key [25]. **The first meeting with a real provider, stage A of the pass-B plan (at most 12 calls), has been run** (20261103; above), and the gateway (1.2.0) then carried the 1,740 answered chat requests of stages B to D. The owner reports that the comparison with OpenAI's console agrees for stage A and for stages B and C, against the gateway's figures. **This test before money missed one fault:** the check that the cost recomputed from the tokens equals the gateway's used the fields the gateway reads, so it could not show that OpenAI's `cache_write_tokens` was left out. **The console is the check that the gateway's own arithmetic cannot be, but here it measured something else:** USD 0.67 is what OpenAI billed after complimentary daily tokens (D-41), so it could not settle the gateway's pricing. What it did check is the counts: requests, input tokens and the cache hit rate equal the ledger. The pilot's dollars at list prices (1.18389) were settled by other means, the console's cache-writes line, which fits USD 0.125 per million, and the allowance reading (a fit, not a proof, as above). Version 1.3.0 reads the field (8 tests, 12 mutants killed) and has met no real provider [41][42][51][54][57][58][64][65][76][77]. The dress rehearsal drove the real gateway through the stage driver, for all four builders, against a fake provider [22][28][32] |
| Builders | Calls and prompt tokens per document identical across two runs against the stub; each installs and runs on Apple Silicon | Done for four builders (see the [X2 page](x2-index-cost.md)). Through the hosted setup against a fake paid upstream the four runners reproduce their rehearsals' counts [25]. In the dress rehearsal all four builders ran the whole ladder through the stage driver against a fake provider (16 runs, all completed) [32]. Against a real provider, requests of the four builders' shapes were sent one by one in stage A; then all four builders ran through the gateway at OpenAI: one document, five documents twice, then twenty documents once, 16 runs, all completed (this measures calls and cost, not quality: no graph was scored) [41][51][58] |
| Pilot tools | The plan's "done when" for each (see the X2 page): the hosted setup reproduces the rehearsal counts through a fake paid upstream and hides a canary key; the watchdog stops within one poll when a fake upstream produces a stop condition; the pre-flight refuses an over-cap case; the stage-A script sends nothing without the stage's cap loaded and runs against a fake upstream first; the dress rehearsal of the whole ladder stops at the cap and writes a complete log | Marked done in the archive's plan at `9885a3d` for every item: the hosted setup (49 tests now), the watchdog (92 tests), the pre-flight (54), the stage-A script (56 tests now; a run against the author's fake provider that sent 10 calls, with a refusal test that forwarded nothing), the stage driver (44 tests now) and the dress rehearsal (573 checks against a fake provider, which changed one stop rule); the counts are those of `257c9d5`; they equal the test functions counted in the files at `c960df7` (no test or code file other than the gateway's changed since) and the numbers in RESUME.md and the X2 README there [44][48][49][54][55][56][62]. All of them have since run against a real provider: the stage-A script and the hosted gateway in stage A, the stage driver, the watchdog, the pre-flight and the four runners' hosted setup in stages B to D [22][28][32][41][50][51][58] |
| Scoring | Answer keys derived by hand; a perfect answerer scores 100% and a random one lands near chance; the paired sign test matches a known table | **Not done for X4:** no scoring program exists |
| Habits | Read the free pre-flight estimate; check the key's shape without printing it; run long jobs in the background with a log; stop at the first failure | Applied to every run |

## State and what is still missing, in brief

This section rests on the archive at `b24484e`, committed 20261104 12:14:06 UTC [82].

### The pilot's cost and what each figure means

| Figure | Meaning |
|---|---|
| USD 1.10537 | The gateway's figure as run, 0.0785 low against list prices; the versions that ran the pilot did not read the cache-write field [58][64][65][76][77] |
| USD 1.18389 | The pilot at list prices: written tokens at USD 0.125 per million, not 0.10. That price is the model page's, as the gateway's page records it; this page did not read OpenAI's pages. The console's cache-writes line fits 0.125 (0.2751 for the calls beyond the allowance; 0.22 at 0.10), but that rests on the allowance fit below, a fit and not a proof. The written-token counts come from a body log outside the repository and cannot be re-derived here [57][58][65][76][77] |
| USD 0.67 | The console's spend, read by the archive as what OpenAI billed after complimentary daily tokens; not a check on the gateway [58][76][77] |

The owner's earlier "Agrees" (stage A; stages B and C) was given against the gateway's figures [58][60].

### The console reading and its cause

This page did not read the console; the figures are as the archive records them in D-40 and D-41 [64][65][76][77]. The usage page showed 1,751 requests, 4,170,590 input tokens and a 22.6% cache hit rate, all equal to the ledger, and a spend of USD 0.67 (cache writes 0.275), the same on every read (20261103; 20261104 10:43 UTC); its smallest bucket is a day, so it covers the whole pilot [64][65][76][77].

The archive attributes the gap to the console's settings: data sharing is on for all projects, and the organisation is enrolled for complimentary daily tokens, up to 250 thousand a day on larger models and up to 2.5 million on a list of mini and nano models. The tooltip's lists do not name `gpt-6-luna`, and the archive does not know whether it is on the program's list [70][71]. The ledger fits a 2.5 million allowance all the same. The archive finds that, counted in completion order, all four console lines fall inside the rounding; in start-time order the output line is 0.4% low. It tried two orders, start times first, chose the second after the gap showed, and cannot tell which one OpenAI counts in [75][76]. This page re-derived only the output and cached-input lines from the committed ledger; the plain-input and cache-writes lines need the body log [72][74][80]. The archive's results page calls the allowance "the better reading" [71].

*Reading:* this page takes the allowance as a fit, not a proof: a fit exact in one of two orders tried is weaker than one fixed in advance, and the output line (USD 0.38852) sits 0.00002 above the lower edge of its rounding [72][74][80].

### The pilot's close

D-43 (20261104 12:13 UTC) records that the owner reported the key revoked and its file removed. The archive's existence-only check found the key listed as Revoked and the file absent; this page did not read the console or the directory. The key's permissions were shown as "All" although the plan asked for a restricted key. Open, and the owner's: the project's USD 5.00 limit against the plan's USD 3 (unknown whether hard); whether to keep or delete the private pilot directory, which holds the body log, the only source of the per-call written-token counts behind 1.18389 (the committed stage totals hold per-run sums only); and the archive's other resume items [58][83].

### What is still missing

- Any provider but OpenAI; with OpenAI, streaming, the embeddings route, a 429 or 5xx and a timeout; and 1.3.0 on a real provider [3][40][41][52][53][57][59].
- A builder route to Anthropic: as the plan reads it, fast-graphrag and nano-graphrag cannot use its compatibility layer; the other two are untested [1][3][22].
- A check of the gateway's dollars against a bill without complimentary tokens; and confirmation that the provider's hard limit is the plan's USD 3 [42][46][64][76][77][83].
- For X4, a scoring program, an agent client and tried question wording; for X5, nothing frozen [18][20].

[Instruments evidence: state, changes and open points](evidence/instruments-state.md).

## Where the evidence is

The full text of the former page is on four pages of its own. Nothing was cut.

| Page | What it holds |
|---|---|
| [Instruments evidence: the metering gateway](evidence/instruments-gateway.md) | What the gateway records, where it reads usage from, the cap and the refusal, request defaults, what changed for a paid run, how it was tested, what it has and has not met |
| [Instruments evidence: the paid pilot's tools](evidence/instruments-pilot-tools.md) | The hosted setup, the free pre-flight, the watchdog, the stage-A script, the stage driver, the dress rehearsal, where the pilot stands |
| [Instruments evidence: state, changes and open points](evidence/instruments-state.md) | What changed commit by commit since the page was written, the pilot's cost and the console's reading, and what is still missing |
| [Instruments evidence: sources](evidence/instruments-sources.md) | The numbered sources of the page |

## Sources

The numbers in brackets refer to the list in [Instruments evidence: sources](evidence/instruments-sources.md), which holds every source of the instruments pages with the time it was read.
