# Resume

Last updated 20261103 01:27 UTC. Decisions: [`DECISIONS.md`](DECISIONS.md). **The repository has been public
since 20261102 08:46 UTC (D-22).** `main` was fast-forwarded to the work branch
`worktree-20261030_1852-kb-kg-docs-scaffold` at `14c154d` before the change; later commits go to both.

## State

The first full pass is written, reviewed and pushed. Nothing is running. X2 pass A on a local model finished 20261102 19:41 UTC
(free, nothing paid): the owner chose every builder to 20 documents, then narrowed the rest to 5; a second model on LightRAG
followed at 20:02 UTC (D-28). Result files:
[`kb-kg/experiments/x2-index-cost/pass-a/`](kb-kg/experiments/x2-index-cost/pass-a); tables and arguments: [the pass-A
page](kb-kg/experiments/x2-index-cost/pass-a-local-model.md).

| Part | State |
|---|---|
| `docs/` (and `plans/`) | **a new documentation, written from scratch** (D-29): 299 pages in eight chapters and an A to Z index, first edition written 20261102 and merged to `main` on 20261103 01:07 UTC (`804c814`, PR #1) on the owner's instruction, then deployed to the site; the owner reviewed the six lists item by item on 20261103 (D-33): a tenth trend (semantic web standards) and five project pages (agent memory) were added, the rest stays, merged to `main` as `ba1247f` (PR 2) and deployed; two arguable projects (Open Knowledge Format, Semantica) wait for the owner; the old pages stay as the Archive tab. How it is kept: [`README.md`](README.md); the decisions, lists and evidence: [`plans/`](plans/) |
| `kb-kg/primer/`, `llm-era/`, `literature/`, `papers-benchmarks/` | first drafts |
| `kb-kg/projects/` | 77 entries (22 deep, 55 cards) and a generated index (`tools/build_projects_index.py`) |
| `kb-kg/landscape/` | two snapshots (19:13 and 19:54 UTC, 20261030) and the approved selection |
| `kb-kg/directions/` | nine pages and an overview, first drafts |
| `kb-kg/experiments/` | five proposals; X1 run; **Step 0 of the order and gates built 20261102** (D-25); X2 pass A on two local models done (D-26, D-27, D-28); X3 to X5 not started |
| `pinakes/` | approach record, recommendations R1 to R7, 12 takeaways, ClaudeKB precedent, what Pinakes has measured, four proposals for what to measure next (P1 answered, the P4 pilot run, P2 blocked, P3's free-path half in the public benchmark repository, described on its own page) |
| `tools/` | `gh_snapshot.py` (57 tests), `build_projects_index.py` (12 tests), `check_public_safe.sh`; `tools/exp/` (stub model server, document selection, statistics, four builder rehearsal runners, two SDK end-to-end checks; 32 tests plus the runners); `metering_gateway.py` 1.1.0 (124 tests); four pass-A runners (`x2_passa_*.py`) and `passa_common.py` (23 tests); the pass-B pieces `passb_common.py` (hosted setup, 45 tests), `passb_watchdog.py` (92), `passb_preflight.py` (54), `passb_stage_a.py` (55) and the stage driver `passb_stage.py` (43); none has met a real provider |

Subagent cost, from the harness's per-agent totals: wave A about 4.1M tokens, wave B about 5.9M, wave C about
1.5M; about 11.5M in all. Step 0's seven agents: about 1.84M (my sum of their totals).

## Waiting on the owner

1. **Whether to rotate the P4 key.** The key file was deleted at the owner's request on 20261102. The
   variable may still be exported in the owner's own terminal tab (`unset PINAKES_ANTHROPIC_API_KEY` clears it
   there). Its value was once malformed; rotating or revoking the key is the owner's call.
2. **The paid pilot, X2 pass B (D-26 to D-28).** A [plan](kb-kg/experiments/x2-index-cost/pass-b-plan.md) was written 20261102 and
   revised after an independent review; nothing has been spent. The owner chose OpenAI `gpt-6-luna` with reasoning off and a cap of
   USD 3 (D-30). On 20261103 the owner answered "go wit your recommendations": article text may go to OpenAI, embeddings local,
   all four builders, two yeses (D-32). **Still needed from the owner:** the key file and the hard limit at OpenAI (decision 6; the
   steps are in [`pass-b-owner-steps.md`](kb-kg/experiments/x2-index-cost/pass-b-owner-steps.md)), then the explicit yes for stages A
   to C once I have shown the dry runs with their numbers. No paid call starts before that. **The free work (stage 0) is done**, including a dress rehearsal of the whole ladder with
   the real driver, runners and builders against a fake provider (573 checks; it found and fixed one error, D-31). The other options
   from pass A are on [the pass-A page](kb-kg/experiments/x2-index-cost/pass-a-local-model.md#where-this-leaves-the-owner). To
   rerun a pass-A builder, use the command line in its runner's header (`tools/exp/x2_passa_*.py`) and the arguments on the
   page; the builders' throwaway virtual environments were in the session's scratch directory and must be rebuilt at the pins
   on each builder's rehearsal page; the derived models are in Ollama (`ollama list`). None of X3 to X5 is started and each
   paid step needs its own yes with model, provider and cap (D-14). Pinakes follow-ups (a BM25-alone
   arm request, a calibrated deep run) are in [`pinakes/experiments/next.md`](pinakes/experiments/next.md#order-for-the-follow-ups).
   The `NOTICE` copyright line uses the git author name "Luca Gattoni"; the owner may change it.
3. **Whether the safety gate should fail when its private-name list is missing.** A new worktree has no copy of the
   gitignored list; the gate warns but still exits 0, so it passes without checking private names. Asked on 20261102;
   unanswered.

## Done since the first pass

- **X1** ran 20261031 (`kb-kg/experiments/x1-snapshot-distributions/`).
- **P1** answered by the Pinakes session 20261031: the sections re-run is not recorded as run.
- **Licence** chosen and added (`LICENSE`, `NOTICE`).
- **P4 pilot** ran 20261101 under D-19 to D-21: three frozen multi-hop questions, EUR 0.3084 in all against EUR 4.92
  of estimates, each run using all 3 rounds. Plan, results and my labelled readings:
  [`pinakes/experiments/p4-deep-pilot.md`](pinakes/experiments/p4-deep-pilot.md). The raw logs and Pinakes'
  transcripts are in the session scratchpad and are not committed; whether to keep them is the owner's call.
- **P4 key file** deleted 20261102 at the owner's request.
- **Full content check** over all 60 commits, then **the repository made public** 20261102 08:46 UTC (D-22).
- **Step 0 of the experiments** built 20261102 (D-25): the 20 X2 documents and 20 X4 questions frozen; a stub model
  server; a statistics helper; rehearsals of LightRAG, nano-graphrag, Microsoft GraphRAG and fast-graphrag against the
  stub ([side by side](kb-kg/experiments/x2-index-cost/README.md#the-rehearsals-side-by-side)); a metering gateway
  for both providers with SDK end-to-end checks. No model was called and no key was used. The scratch environments
  and raw logs live in the session scratchpad and are not committed.
- **Pinakes' `docs/graph/` marked historical** with links here, landed in Pinakes as `dee3f04` on 20261102 (D-23);
  its CI and docs workflows succeeded and the published site shows the banner.
- **`CLAUDE.md`** now says the repository is public (the owner's yes, 20261102 08:57 UTC).
- **Benchmark repository** described and linked: [`pinakes/experiments/datasets-benchmark.md`](pinakes/experiments/datasets-benchmark.md),
  at its commit `9941f58`, with its limits kept; the owning session confirmed the framing.

## Next, once the owner answers

- **Paid pilot, stage A (needs answers 3 to 7 above and the owner's explicit yes with model, provider and cap, D-14).** The owner's
  steps are in [`pass-b-owner-steps.md`](kb-kg/experiments/x2-index-cost/pass-b-owner-steps.md). The owner prepares a key file by the D-20 route (mode 600, one line, outside the repository and the scratch directory) and sets the hard
  limit at the provider; then, from the repository root: `tools/exp/passb_stage_a.py extract` (free; the pass-A gateway
  directories and the builders' throwaway environments must exist, or be rebuilt at the pins on the rehearsal pages), then
  `passb_stage_a.py run` without `--send` (prints the plan, starts nothing), then with `--send`. Stages B, C and D run with
  `tools/exp/passb_stage.py` the same way (dry run first); both scripts' headers hold the arguments and the config shapes
  (`passb_profile.example.json`, `passb_builders.example.json`). After a watchdog trip, read the stage report before anything
  else; the repeat-after-fault procedure is in the driver's header.

- Run an approved experiment: throwaway environment under the scratch directory, one scoped key in that
  process's environment only, raw logs and tool versions recorded, no verdicts. A pilot first, with the cap the
  owner sets.
- Re-run `uv run tools/gh_snapshot.py` after a few weeks so the star and activity comparison means something
  (the two snapshots so far are minutes apart), then re-read every direction page's "signals to watch".
- Regenerate the index with `uv run tools/build_projects_index.py` when an entry changes
  (`--check` tells you if it is stale).

## Debts that are written down so they are not lost

- **Unverified items.** Every entry lists its own. The largest: six literature figures marked unverifiable;
  whether LazyGraphRAG is in the open-source package; many 2026 papers read as title or abstract only; whether
  any star growth is organic (the stargazers endpoint returned 404 in several entries); the primer's first-use
  dates for "knowledge base" and for Cyc; the headline benchmark numbers inside most entries, which rest on
  the sources each cites and were not re-derived.
- **Length.** Most deep entries and direction pages exceed their length target by 20% to 80%.
- **Snapshot recall.** The search missed seven expected projects (now on the watchlist). Treat any snapshot as a
  dated sample.
- **Inconsistencies in Pinakes' own documents**, to report upstream when the owner allows editing Pinakes:
  the scanned-PDF run costs EUR 0.43 in `STATUS.md` and `MEASUREMENT-RUN.md` but EUR 0.11 in `DESIGN.md`
  (confirmed); `STATUS.md` gives 107 411 non-transit edges at line 586 and 107 802 at line 631 for the same
  106 506 sibling edges (confirmed); not re-derived by me: no recorded result for the graph-gate re-run
  approved 20260825 (the Pinakes session confirmed on 20261031, P1: not run as far as its repository records), no labelled re-extraction trigger in `audit.py`, a defect count of five against six for the
  deep-loop report tool.
- **The rename in Pinakes is landed and re-read (20261102 10:05 UTC).** Pinakes closed "the template release"
  at 0.22.0 and named its leftover *the `sqlite-vec` tier, staged* (commits `7beac4c`, `de3e506`, merged
  `75f71d8`). `pinakes/approach/PINAKES_APPROACH.md` has a dated update that says how its four old-wording
  passages now read; `pinakes/experiments/README.md` has the new name in its `sqlite-vec` row; the other pages
  hold no stale wording (`recommendations-r1-r7.md` has none, `claudekb.md` quotes a dated note correctly).
- **Gate coverage.** `tools/check_public_safe.sh` scans the working tree, not the staged set, and cannot know a
  private name that is not in its gitignored local list.
- **Entries edited after review.** The consistency pass (`60cab7c`) changed eleven entries and pages after they
  were committed; the index was checked current afterwards.

## Not to do

- Do not touch the Pinakes repository without the owner's explicit yes at that step.
- The repository is public: run `tools/check_public_safe.sh` before every commit, and never write a private
  name, a path or a key into it.
- Do not name private repositories anywhere in this repository.
- Do not start an experiment, or any paid run, without the owner's yes for that experiment.
