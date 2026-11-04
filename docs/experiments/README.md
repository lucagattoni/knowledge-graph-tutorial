---
type: chapter
updated: 20261104 13:18 UTC
---

# Experiments

This chapter holds the experiments the owner runs in this repository to answer questions the trends chapter leaves open. It states the rules every experiment follows, the order in which they may run, and where each one stands. Every result here is first-party: the owner ran it, on a small set, with the setup written down. None is an independent evaluation.

## What this chapter is

The trends chapter keeps meeting the same gaps: a cost that no source measured, a comparison nobody ran on one corpus, a claim that rests on a project's own words. Where a gap can be closed with a small, cheap run, the owner runs it here.

- **First-party by construction.** The repository is the owner's own notebook. There is no packaging for outside replication; the records are enough for the owner to repeat a run [1].
- **Small on purpose.** The paid proposals whose cost is unknown (X2, X4 and, when its turn comes, X5) start as a pilot with a cap. A pilot measures cost and feasibility; it does not produce a result that carries a decision. X2's pass-B plan prices its whole ladder by arithmetic at about USD 0.9 (central estimate) under a cap of USD 3, which the owner chose after the plan (D-30); on 20261103 the owner said yes to stages A to C of it (D-34) and, once they had run, to stage D (D-37); all four have run [9][10][23][31][36]. The ladder figure is an estimate from local-model tokens. What has been measured, over the four stages (1,751 answered requests), is three figures with three meanings. **USD 1.10537** is the gateway's own figure, which left out OpenAI's cache-write price (D-39). **USD 1.18389** is the pilot at list prices, with that price: the gateway was low against list prices by 0.0785, and the console's cache-writes line confirms the price (D-41). **USD 0.67** is what OpenAI's usage page shows as billed: the list price less complimentary daily tokens, which the organisation receives because it shares inputs and outputs with OpenAI (D-41). The archive calls that "the better reading", and I do not read it as a proof, because four points stay open (Status) [44][45]. The same setting means the pilot's article text and the models' outputs were probably shared with OpenAI for training; the owner left it on (D-42) [44][45]. By stage, on the gateway's figure: A to C USD 0.26333, against a central estimate of about 0.3 (D-34); D USD 0.84204, against about 0.65 by arithmetic from C (D-37) [23][36][37]. The owner reports that OpenAI's usage page agreed with the gateway's figures for stage A and for stages B and C, and the archive keeps that word, not the page's figures; it says it does not know what those two comparisons compared [23][24][31][32][33][41]. X1 needed no model and no money, and X3 is priced from X2's figure, so neither is a pilot [2].
- **Linked from the trend it tests.** A trend page names the open question; this chapter holds the run.

## Rules for every experiment

These come from the owner's decisions D-14 and D-24 and from the experiments plan in the archive [1][2][3].

| Rule | What it means |
|---|---|
| One yes at a time | Each experiment needs the owner's explicit yes. Its cost, models and data are stated first. Where a cost cannot be known before a pilot, the proposal asks for a cap on the pilot, not a budget for the whole experiment. While the organisation's sharing setting at OpenAI is on (the owner left it on, D-42), anything sent through its key is shared with OpenAI, so a yes for a run that would send non-public text must say so [44]. |
| Owner's Apple Silicon Macs only | Runs happen on this Mac by default; another Mac only through an `ssh` command the owner approves each time; no cloud or rented hardware. |
| Hosted models are allowed | OpenAI and Anthropic models are both acceptable, and each experiment must be able to run on either. **One model per comparison:** builders compared on different models are confounded. A repeat on the other provider is a separate, labelled run with its own yes. Prices are read from the provider's pages when a run is approved, not taken from memory. |
| A free option | A local model on the owner's Mac is the free alternative to a hosted one. X2 is planned as a free pass on a local model before a paid pass on a hosted model. |
| Third-party code is untrusted | Each experiment runs other projects' code. It is installed in a throwaway environment. A hosted run gives that code a dummy key and the address of the [metering gateway](instruments.md); the gateway reads the real key itself, from its environment or from a file only the owner can read, and never hands it to that code. The key file is still readable by any process of the same user, a residual risk that X2's plan and, since the archive's correction at `d824716`, the gateway's own page both state [8][11]. Projects under GPL, AGPL or non-commercial terms are run for measurement only, and none of their code enters the repository. |
| Costs are measured | [Token](../index/token.md) counts come from the provider's usage fields, recorded per call. A figure derived from them is labelled as arithmetic. |
| Everything is recorded | Tool versions and commit hashes, the model name as the provider reports it, the dataset version and licence, the date, the raw logs. A result without these is not a result. |
| No verdicts | An experiment reports numbers, the setup and what the setup cannot show. A paragraph that judges is labelled *Reading:*. |
| A plan before the first paid call | Each paid experiment gets its own pre-registered plan, fixed before its first paid call. The archive's wording says the plan is written once the owner has approved cost, model and data [2]; X2's pass-B plan was instead drafted first, as the basis for that decision, with nothing approved when it was written [9]. Its first paid calls (stage A) came on 20261103, after the owner's yes (D-34) [23][24]. |

Lessons from the first paid pilot are built into every later run: read the provider's free pre-flight estimate first, check the key's shape without printing it, run long jobs in the background with a log, and stop at the first failure and report it [3].

## Order and gates

The owner delegated the choice between a full plan and a slim one; the assistant chose the slim one, because each proposal already states its question, method and risks. The recommended order is X2, X4, X3, X5 [1][2].

| Step | What | Money |
|---|---|---|
| 0 | Free groundwork: the [instruments](instruments.md), the frozen document and question sets, rehearsals against a stub | None |
| 1 | X2, the index cost of cheap graph builders. Pass A on a local model (free; done), then pass B on a hosted small model under the owner's cap: OpenAI `gpt-6-luna` with reasoning off, USD 3 in total (D-30); article text to OpenAI, local embeddings, all four builders and two yeses answered 20261103 (D-32). **The owner said yes to stages A to C on 20261103 16:12 UTC (D-34); stage D was not covered and got its own yes at 17:57 UTC (D-37).** All four stages have run (20261103 16:12 to 19:01 UTC; stage D from 17:57 UTC, D-38). **The pilot has run to its end: D-37 does not cover a repeat of D, and no further paid step is approved** [36]. **The article text sent to OpenAI was probably shared with it for training; the owner left the sharing setting on (D-41, D-42)** [44][45]. **The pilot's key is revoked and its key file removed (D-43)** [55]. See the [pass-B plan](../../kb-kg/experiments/x2-index-cost/pass-b-plan.md), the archive's [results page](../../kb-kg/experiments/x2-index-cost/pass-b-results.md) and the [X2 page](x2-index-cost.md) [9][10][11][13][14][15][16][17][22][23][24][26][31][32][33][36][37] | The owner's cap: USD 3 in total, with stage limits A 0.10, B 0.20 and C 0.60 (at most USD 0.90 for the yes of D-34; central estimate about 0.3) and USD 1.50 for stage D (D-37). Spent, as the gateway's figure / at list prices with OpenAI's cache-write price: A 0.00646 / 0.00682, B 0.03735 / 0.04004, C 0.21952 / 0.23148, D 0.84204 / 0.90556; total **USD 1.10537 / 1.18389**. OpenAI's usage page shows **USD 0.67 billed** for the whole pilot (read on 20261103 and again on 20261104); the archive's better reading is that it is the list price less complimentary daily tokens, so it is no check on the gateway (D-41). Of the cap, 1.89 or 1.82 is left on those two totals; stage D used 56% or 60% of its limit. The pilot's OpenAI project shows a limit of USD 5.00 against the cap of USD 3; whether it is a hard limit is unknown (D-40) [10][23][24][26][31][32][36][37][40][41][44][45] |
| 2 | X4, a code graph against grep and glob (a pilot of 3 questions in 2 conditions) | The owner's cap |
| 3 | X3, a matched-cost comparison on one corpus; it needs X2's per-document figure | Set from X2 |
| 4 | X5, the size at which an index-only wiki stops working; the heaviest, so last | Set from X2 and X4 |

**Gates.** After each step the owner is given the measured cost and what the instrument could not show. The next step starts only on the owner's explicit yes, with cost, model and data stated. A step does not start because the one before it worked [1][3].

## Where things stand

This section rests on the archive at `b24484e`, committed 20261104 12:14:06 UTC [54]. Every result here is first-party: the owner's own, on a small set, with the setup written down. None is an independent evaluation.

| Page | Status | Money | Measured so far |
|---|---|---|---|
| [Instruments](instruments.md) | Step 0 built, with listed gaps (stage 0 of the pilot done, D-31); used in all four pilot stages [14][16][24][25][32][37] | Free to build [11][14] | Gateways up to 1.2.0 did not price OpenAI's cache writes; 1.3.0 does and has not met a real provider [35][38]. The watchdog tripped no rule in the 16 runs of stages B to D, so its trips have been exercised only against fakes [32][34][37] |
| [X1](x1-snapshot-distributions.md) | Ran 20261031 16:00 UTC [6] | None [6] | A description, not a test of whether growth is organic; the figures are on the X1 page [6] |
| [X2](x2-index-cost.md) | Pass A (one local model) finished 20261102 19:41 UTC; nano-graphrag failed on document 1 and fast-graphrag stopped at 13 of 14 [4][5]. Pass B (hosted) ran stages A to D, 20261103 16:12 to 19:01 UTC [24][37] | Pass A free; pass B under a USD 3 cap [4][10][23] | In stage C (five documents per builder, run twice), USD 0.0028 (LightRAG, second run) to 0.0105 (nano-graphrag, second run) per document, by the gateway's figure; the two runs are not independent for cost [32][37]. No graph quality measured [32][37] |
| [X3](x3-matched-cost-comparison.md) | Not started. The status log says it waits for X2's per-document figure, which stage C now gives for one model and five documents; like every paid step it also needs its own yes (see Order and gates) [3][32] | Set from X2 [2] | Nothing |
| [X4](x4-code-graph-vs-grep.md) | Groundwork only [7] | Unknown before a pilot [2] | 20 questions on two repositories, answers frozen; no agent or code-graph tool has run and no scoring program exists [7] |
| [X5](x5-wiki-size-limit.md) | Proposal only [3] | Unknown before a pilot [2] | Nothing frozen in the record read [3] |

### The paid pilot

Pass B ran on OpenAI `gpt-6-luna`, reasoning off, in four stages, each after the owner's yes (D-34, D-37) [23][31]. By the gateway's figure [24][32][37]:

| Stage | Answered requests | USD |
|---|---|---|
| A | 11 | 0.00646 |
| B | 56 | 0.03735 |
| C | 376 | 0.21952 |
| D | 1,308 | 0.84204 |

Three figures, three meanings:

| Figure | Meaning |
|---|---|
| USD 1.10537 | The gateway's figure as run. It left out OpenAI's cache-write price (D-39) [36][37] |
| USD 1.18389 | At list prices, with that price, on the archive's account; the price is as the gateway's page quotes OpenAI's. The console's cache-writes line fits it (D-41) [37][44][45] |
| USD 0.67 | The spend shown on OpenAI's usage page, as read by the archive's author on 20261103 and 20261104; this page did not open it. The archive explains it as the list price less complimentary daily tokens (D-41) [40][44][45] |

*Reading:* USD 0.67 is no check on the gateway [44][45]. The archive calls its allowance explanation "the better reading" [50]; this page does not read it as a proof. Four points stay open: why the ledger fits a 2.5-million allowance only when the calls are counted in completion order (in start-time order the output line is 0.4% low, and the archive chose the order after seeing the gap) while `gpt-6-luna` is on neither of the console's lists [44][45][50]; whether OpenAI counts in that order [49][50][52]; whether the project's USD 5.00 limit is hard [40][41][46]; and when the sharing setting was turned on [44][45]. Of USD 1.18389, only the sums were checked, not the written-token counts [37][41].

### Data sharing

The console's setting "Share inputs and outputs with OpenAI" is enabled for all projects [44][45]. The pilot's article text, prompts and outputs were therefore probably shared with OpenAI for training, and cannot be recalled (D-41, D-42) [44][49][50]. The plan had relied on OpenAI's data page, which says API data is not used for training "unless you explicitly opt in"; the organisation had opted in [51]. The owner answered "Leave it on" (D-42, 20261104 10:51 UTC); nothing was changed at OpenAI [49].

### The pilot's close

D-43 (20261104 12:13 UTC) records the pilot's OpenAI key as revoked and its key file as removed. That is the archive's record; this page did not read the console or the directory [55]. Still open, and the owner's: the project's limit shows USD 5.00 against the plan's USD 3 (unknown whether hard); whether to keep or delete the private pilot directory, whose body log holds the written-token counts behind USD 1.18389 [55]. The key's permissions were shown as "All", although the plan asked for a restricted key [55].

### What comes next

- No further paid step is approved, and D-37 does not cover a repeat of stage D [36][40].
- *Reading:* the recommended order is X2, X4, X3, X5. It is the assistant's recommendation (D-24), not a ranking by the owner [1].

## Evidence pages

The long record of this chapter, the status log with its dated readings of the archive and the numbered sources, is on pages of its own, so that this page stays short. Nothing was cut: the text of the former page is on them unchanged.

| Page | What it holds |
|---|---|
| [Experiments evidence: status log](evidence/status.md) | The chapter's dated status, experiment by experiment, as read from the archive |
| [Experiments evidence: sources](evidence/experiments-sources.md) | The numbered sources of this page and of the status log |
| [All evidence pages](evidence/README.md) | A map of the evidence pages of every experiment page and of the instruments |

## Sources

The numbers in brackets refer to the list in [Experiments evidence: sources](evidence/experiments-sources.md), which holds every source of this page and of the status log with the time it was read.
