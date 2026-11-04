# Resume

Last updated 20261104 12:13 UTC. Decisions: [`DECISIONS.md`](DECISIONS.md). **The repository has been public
since 20261102 08:46 UTC (D-22).** All of the work branch
`worktree-20261030_1852-kb-kg-docs-scaffold` is in `main`; on 20261104 the owner asked for the branch and its worktree to be deleted, so later work starts from `main`
in a new worktree.

## State

The first full pass is written, reviewed and pushed. Nothing is running. X2 pass A on a local model finished 20261102 19:41 UTC
(free, nothing paid): the owner chose every builder to 20 documents, then narrowed the rest to 5; a second model on LightRAG
followed at 20:02 UTC (D-28). Result files:
[`kb-kg/experiments/x2-index-cost/pass-a/`](kb-kg/experiments/x2-index-cost/pass-a); tables and arguments: [the pass-A
page](kb-kg/experiments/x2-index-cost/pass-a-local-model.md).

| Part | State |
|---|---|
| `docs/` (and `plans/`) | **a new documentation, written from scratch** (D-29): 301 pages in eight chapters and an A to Z index, first edition written 20261102 and merged to `main` on 20261103 01:07 UTC (`804c814`, PR #1) on the owner's instruction, then deployed to the site; the owner reviewed the six lists item by item on 20261103 (D-33): a tenth trend (semantic web standards), six project pages (five on agent memory, Semantica) and a paper group for the new trend (RDF-star and SPARQL/SHACL semantics, five papers) were added, the rest stays; merged to `main` as `ba1247f` (PR 2) and `c31f54e` (PR 3: Semantica, the paper group, a sentence on Open Knowledge Format) and deployed; `docs/experiments/` carries the paid pilot's results (stages A to D; its cost as three figures, 1.10537 by the gateway, 1.18389 at list prices and 0.67 as billed after complimentary daily tokens, D-41) at the archive's `fe72070`, merged as `ad2f0c4` (PR 4, 20261104 10:42 UTC) and `b6064b8` (PR 5, 20261104 11:55 UTC) and deployed, and needs a refresh after any experiments-session commit that changes pilot figures or records; the old pages stay as the Archive tab. How it is kept: [`README.md`](README.md); the decisions, lists and evidence: [`plans/`](plans/) |
| `kb-kg/primer/`, `llm-era/`, `literature/`, `papers-benchmarks/` | first drafts |
| `kb-kg/projects/` | 77 entries (22 deep, 55 cards) and a generated index (`tools/build_projects_index.py`) |
| `kb-kg/landscape/` | two snapshots (19:13 and 19:54 UTC, 20261030) and the approved selection |
| `kb-kg/directions/` | nine pages and an overview, first drafts |
| `kb-kg/experiments/` | five proposals; X1 run; **Step 0 of the order and gates built 20261102** (D-25); X2 pass A on two local models done (D-26, D-27, D-28); X3 to X5 not started |
| `pinakes/` | approach record, recommendations R1 to R7, 12 takeaways, ClaudeKB precedent, what Pinakes has measured, four proposals for what to measure next (P1 answered, the P4 pilot run, P2 blocked, P3's free-path half in the public benchmark repository, described on its own page) |
| `tools/` | `gh_snapshot.py` (57 tests), `build_projects_index.py` (12 tests), `check_public_safe.sh`; `tools/exp/` (stub model server, document selection, statistics, four builder rehearsal runners, two SDK end-to-end checks; 32 tests plus the runners); `metering_gateway.py` 1.3.0 (144 tests); four pass-A runners (`x2_passa_*.py`) and `passa_common.py` (23 tests); the pass-B pieces `passb_common.py` (hosted setup, 49 tests), `passb_watchdog.py` (92), `passb_preflight.py` (54), `passb_stage_a.py` (56) and the stage driver `passb_stage.py` (44); every pass-B tool has met OpenAI (stages A to D, 20261103; the gateway at 1.1.0 and 1.2.0, and 1.3.0, which prices OpenAI's cache writes, has not); the watchdog, live in all 16 runs, tripped nothing, so its stops have only been exercised against fakes |

Subagent cost, from the harness's per-agent totals: wave A about 4.1M tokens, wave B about 5.9M, wave C about
1.5M; about 11.5M in all. Step 0's seven agents: about 1.84M (my sum of their totals).

## Waiting on the owner

1. **Whether to rotate the P4 key.** The key file was deleted at the owner's request on 20261102. The
   variable may still be exported in the owner's own terminal tab (`unset PINAKES_ANTHROPIC_API_KEY` clears it
   there). Its value was once malformed; rotating or revoking the key is the owner's call.
2. **The paid pilot, X2 pass B (D-26 to D-28).** A [plan](kb-kg/experiments/x2-index-cost/pass-b-plan.md) was written 20261102 and
   revised after an independent review. The owner chose OpenAI `gpt-6-luna` with reasoning off and a cap of USD 3 (D-30), answered
   the open questions on 20261103 (D-32) and gave the yes for stages A to C (D-34). **Where it stands: all four stages are done**
   (20261103 16:12 to 19:01 UTC; 1,751 answered requests; USD 1.105 by the gateway, 1.184 with OpenAI's cache-write price, which the gateways up to
   1.2.0 left out, D-39; the stop rules fired nowhere; the numbers and my readings are in
   [`pass-b-results.md`](kb-kg/experiments/x2-index-cost/pass-b-results.md), the run log in the plan). The owner compared the console for stage A
   and for B with C (agrees, against the gateway's figures) and gave the yes for stage D (D-37); stage D ran 17:57 to 19:01 (D-38).
   **The console, read by me in Chrome (D-40, D-41), shows USD 0.67 billed for the whole pilot; that is the list-price value 1.184 (1.105 by
   the gateway, which left out the cache-write price) less complimentary daily tokens, which the organisation gets because "Share inputs and outputs with
   OpenAI" is enabled for all projects (Data controls, Sharing): the pilot's article text and outputs were probably shared with OpenAI for training, against
   the plan's premise that API data is not used for training unless you opt in. The owner chose to leave that setting on (D-42; nothing was changed), so anything sent
   through this organisation's key is shared: a later paid run that would send non-public text must say so in its yes.** **The pilot's key is closed (D-43):** on 20261104 the owner revoked the key at OpenAI and removed the key file from the Mac mini (this session did neither,
   a hard delete and a credential action being the owner's to do; it checked both afterwards: the console lists the project's only key as Revoked, and the
   key file is absent). Still open: the project shows a limit of USD 5.00 against the plan's USD 3,
   unknown whether hard; and whether to keep or delete the private pilot directory `~/.config/kb-kg-pilot/` (profile, builders config, the ledger and its body
   log, the result directories; all outside the repository).
   No further paid step is approved; a repeat of D is not covered by D-37. **The free work (stage 0) is done**, including a dress rehearsal of the whole ladder with
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
   unanswered. A copy of the list is kept outside the repository (`~/.config/kb-kg/public-safe-patterns.local.txt`, saved 20261104 before the worktree
   that held the only copy was removed); copy it to `tools/public-safe-patterns.local.txt` in any new worktree before the first commit.

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

- **Paid pilot, a repeat or anything further (needs its own yes, D-14).** Stages B to D ran with the commands below. From the repository root: `uv run python tools/exp/passb_stage.py --stage B --builder lightrag
  --builder fast --builder ms --builder nano --profile PROFILE --builders-config CONFIG --out-dir OUT` is a dry run (add `--send` to
  run), stage C ran twice (`--stage C --run-label r1`, then `r2`); stage D ran as `--stage D`, dry run first (a repeat needs the state file `ledger/stage_D.json` moved aside and a new `--run-label`). The profile, the builders config, the
  key file and the ledger are in the owner's private pilot directory made on 20261103 (`~/.config/kb-kg-pilot/`: `profile.json`,
  `builders.json`, `openai.key`, `ledger/`; none is in this repository); the builders' throwaway environments and the corpus are in
  the session's scratch directory and must be rebuilt if it is gone. The pre-flight, the gateway's cap and the watchdog run by
  themselves. After a watchdog trip, read the stage report before anything else; the repeat-after-fault procedure is in the
  driver's header.

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
- **Pilot scripts that are not in the repository.** `pass-b-results.md` and `pass-b/stage-totals.json` were generated by one-off scripts in the session's
  scratch directory, which is gone with the session; the files in the repository are the source now. The per-call written-token counts behind the
  cache-write figures exist only in the gateway's body log in the private pilot directory (D-39).
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
