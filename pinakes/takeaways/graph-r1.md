---
slug: graph-r1
neutral-entry: ../../kb-kg/projects/graph-r1.md
investigated: 20260725
updated: 20261030 19:08 UTC
licence-gate: open
---

# Graph-R1: what Pinakes takes from it

The facts about the project itself are in its [neutral entry](../../kb-kg/projects/graph-r1.md). This page
holds only the Pinakes-specific reading. Facts about what Pinakes built come from its public documents,
[STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md),
[ROADMAP](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md),
[DESIGN](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md) and
[CLI](https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md), read on 20261030 between 19:04 and
19:05 UTC from a local checkout. The text at those URLs on the remote branch was not re-fetched and may
differ.

## Verdict

Worth studying for the shape of its tool interface and its loop, not for the reinforcement learning or the
code: Pinakes took the loop as caller-driven composable tools plus a budgeted command-line loop, and left RL,
paid graph extraction and the evaluation setup. (July verdict: "Read the paper, not the code." It stands.)

## What Pinakes takes

Graph-R1 is the trained, formalised version of the loop that Pinakes' recommendation R6 delegates to the
caller agent ([recommendations R1 to R7](../recommendations-r1-r7.md)). That is why the July note studied
it for loop structure. The ideas it put on file, with the Pinakes design section each feeds:

| Idea from Graph-R1 | Why it transfers | Feeds |
|---|---|---|
| **Queries in, scored sentences out.** The agent's only action is a natural-language sub-query; the environment does all graph mechanics. | Keep `pinakes_search` this shape. Graph structure is the server's retrieval index, never the caller's burden. | DESIGN 4.3 (multi-hop without an agent) |
| **A readable score per result.** The `<coherence>` value lets the model judge sufficiency ("top fact 1.8 and on topic: answer; everything below 0.5: query again"). | An untrained caller can make the continue-or-answer decision Graph-R1 had to learn, if the server returns honest scores and the corpus-level confidence signal. | DESIGN 4.2 (confidence) |
| **Termination belongs to the caller.** The environment never says "stop". | Matches R6. Return honest signals (scores, low-confidence abstention), never a "you have enough" verdict. | DESIGN 4.2, 4.3 |
| **Small k per turn, iterate.** About 5 facts per turn over about 2.4 turns beat single-shot top-60 GraphRAG retrieval in the paper. | Keep default limits small; have the tool description say "call again with a refined query rather than raising the limit", which encodes the trained policy in one sentence. | DESIGN 4.3 |
| **Results advertise their frontier.** Each returned fact carries its entity set, which becomes the next query. | Surface each hit's typed outgoing links (or let the links tool accept a hit) so the next hop is visible without a second call. | DESIGN 4.3, 6.2 |
| **A graph leg in rank fusion.** Graph-R1 fuses an entity path and a direct path by reciprocal rank. | The Pinakes analogue is a third ranked list: documents reachable by links from the top lexical and semantic hits. Free, because it reuses authored links, and gated by the retrieval-change rule (measured, not assumed). | DESIGN 4.1, 6.2 |
| **Structure before content.** Graph-R1 pays the answer reward only after a perfect format. | Repurposed as documentation: tool outputs must be strictly and predictably structured so an untrained caller never parses prose. | CLI (tool schemas) |

Evidence kept on file, not built: independent, quantified support for the R6 bet that multi-turn retrieval
over a modest index beats bigger single-shot retrieval with fewer tokens in context; and the
hyperedge-as-sentence design, which shows graph benefit without leaving language space and is close in
spirit to sidecar links over intact documents. Both rest on the paper's own evaluation, with the caveats in
the neutral entry (128 test instances per dataset, one margin smaller than a single question).

## What Pinakes leaves

| Left | Reason |
|---|---|
| LLM-based graph extraction at build time | A paid pass over the whole corpus; it breaks the free path. The extraction buys typed links, which Pinakes already gets from authored `links[]` plus derived structural edges. |
| RL training of any policy | Out of scope by R6. |
| Per-corpus policy models | Graph-R1 trains one model per dataset; its out-of-distribution results needed extra training regimes. Caller-agnostic tools avoid the problem. |
| Its evaluation as a template | Token-level F1 against short gold answers rewards extractive QA, not knowledge-base workflows. The Pinakes golden set (recall at k, MRR, false-abstain) fits better. |
| The repository as an engineering reference | Research code, one commit in 2026, no releases. Read the paper. |
| The inference that RL is replaceable by "a capable model plus well-shaped tool returns" | July's reading, not the paper's. The paper tests nothing above 7B, and its Qwen3-4B observation (a model already tuned with RL over-relies on internal reasoning) does not show that a frontier model already has what GRPO instills. Kept as a hypothesis, not a finding. |

## Where it landed in Pinakes

Checked against STATUS, ROADMAP, DESIGN and CLI (see the note at the top). **None of those documents credits
Graph-R1 for any feature.** The only mention of it is in the list of fourteen investigations that landed in
0.1.1 ([ROADMAP](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md)). The rows below say what
was built that matches each idea, not that Graph-R1 caused it.

| Idea | Built? | What the documents say |
|---|---|---|
| **The agentic multi-turn loop, caller-driven** | **Built, as designed.** | DESIGN 4.3: multi-hop is delivered "by making the tools composable rather than by building an agent". `pinakes_search`, `pinakes_get`, `pinakes_search` is the plan-retrieve-read-refine loop, and Claude Code runs it in its own context. Four MCP tools ship: `pinakes_search`, `pinakes_get`, `pinakes_links`, `pinakes_list_kbs` ([CLI](https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md)). Below a confidence threshold the MCP side returns the passages, a `confidence` and a suggested next search, and the calling agent decides. R6 itself ("expose the graph to the caller's agent; do not traverse on its behalf") is recorded as built in 0.5.0, with `confidence` always `unknown` on the links tool ([recommendations](../recommendations-r1-r7.md)). |
| **The agentic loop, server or command driven** | **Built, as a different thing from Graph-R1's.** | `pnk ask --deep`, shipped in 0.24.0 (20260811 22:24), working since 0.25.1, deep release closed at 0.26.0 (20260822 01:32) ([STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md)). Free retrieval is round 0; its confidence picks the branch: one synthesis call when confident, decompose, search, answer and re-fold when not, stopping at sufficiency. A KB with no calibrated confidence runs the loop with no early stop and names the bound that ended it (`max_rounds` or a budget window). It is a CLI surface only: no `pinakes_*` tool runs it, and a test asserts that `pnk serve` never loads the module. It calls a hosted model under a pre-call spending reservation. There is no RL, no trained policy and no model of Pinakes' own. |
| **Who decides to stop** | **Differs from Graph-R1.** | In Graph-R1 the trained model decides from its own reflection. In `pnk ask --deep` a fitted confidence signal and hard caps decide; in the MCP path the caller does. The July point 6 ("termination belongs to the caller") is built for MCP and not for the command. |
| **What the paid loop cost** | Measured. | The measurement run (0.25.3, 20260821) published an over-reservation factor of 29.75x on the cheap synthesis branch and 50.92x and 22.35x on the two loop branches, for 0.2131 EUR spent against a 5.1836 EUR worst case. It is a cost of the budget design, not a comparison with Graph-R1. |
| **Per-hit score in `pinakes_search`** | **Partly; per-hit score unstated.** | `pinakes_search` returns ranked, cited passages and a corpus-level confidence signal fitted per KB on the top reranker score, `unknown` where the KB is not calibrated. Whether each hit carries its own score is **unstated** in the documents read. `pinakes_links` neighbours do carry a `score`, comparable only within one `scored_by_query`. |
| **Hits advertise their frontier** | **Built for `pinakes_links`; for search hits unstated.** | `pinakes_links` returns neighbours, `frontier`, `unresolved` and `truncated` (links release 0.5.0, 20260731 11:27). Whether `pinakes_search` hits carry outgoing links is **unstated**. |
| **Graph leg in fusion** | **Built, off by default, measured no.** | The graph release (0.11.0, 20260805 07:14) derives a structural graph and ships an expansion channel, `[retrieval] graph_channel`, set to `off`. Gate run on the RFC realism corpus, measured 20260804 22:52: multi-hop 7 of 20 with the channel off and 4 of 20 on, 0 improved, 3 regressed, p = 1.0000; the extra candidates "displaced three answers two-list fusion already had". Caveat in STATUS: three of the seven edge kinds derived zero edges on that corpus, so the verdict is narrower than it reads. Whether the channel is a third reciprocal-rank list is **unstated**; STATUS calls the baseline "two-list fusion". So July's prediction that the leg is cheap and helpful was tested and not supported on that corpus. |
| **Tool-description guidance ("refine, do not raise k")** | **Unstated.** | Not found in STATUS, ROADMAP, DESIGN or CLI. The tool schemas are committed in the Pinakes repository and checked against a live session in CI (CLI); their text was not read. |
| **Strictly structured tool output** | **Unstated as an adopted idea.** | The committed tool schemas and the single `--json` schema for `pnk ask` ("one schema whether or not a loop ever runs", 0.23.0) are related, but no document ties them to Graph-R1. |
| **LLM graph extraction at build time** | **Not built.** | No LLM-extracted entity or relation graph appears in the shipped features in STATUS. The graph is derived structurally (0.11.0) from authored `links[]` (0.5.0 and 0.6.0). A PPR channel and an NER extra are staged, gate-only and not scheduled (ROADMAP). |
| **Reinforcement learning** | **Not built, by design.** | |

## Licence gate

Open. The `LICENSE` file is MIT [(neutral entry)](../../kb-kg/projects/graph-r1.md). Ideas and measured results
are free to reuse; source is not reused here because the verdict is to read the paper, not the code.

## Changed since July 2026

- 20261030 19:08 UTC: **verdict unchanged.** The licence is still MIT, the repository is quiet and not
  archived (last push 20260430, none since 20260801), there is no release, no successor and no rename. The
  neutral entry lists the details.
- Two July numbers behind the "small k" and "quantified validation" arguments needed a caveat. The facts per
  turn are 5 in the paper's table and 10 in the repository's retrieval server, so "k = 5" is the paper's
  statement, not a verified run setting. And the ablation average of 17.8 against 63.9 is a two-dataset
  average. Neither reverses a take; both soften "quantified".
- The paper's evaluation uses 128 test instances per dataset, which bounds how much weight the "independent,
  quantified validation of R6" can carry. This does not change the verdict, because Pinakes did not build
  R6 on that number.
- Since July, Pinakes built the loop twice (caller-driven tools, and `pnk ask --deep`) and measured the
  graph leg, which failed its gate on one corpus. Those are recorded above under "Where it landed".
