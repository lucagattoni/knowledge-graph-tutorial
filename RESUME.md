# Resume

Last updated 20261102 08:50 UTC. Decisions: [`DECISIONS.md`](DECISIONS.md). **The repository has been public
since 20261102 08:46 UTC (D-22).** `main` was fast-forwarded to the work branch
`worktree-20261030_1852-kb-kg-docs-scaffold` at `14c154d` before the change; later commits go to both.

## State

The first full pass is written, reviewed and pushed. Nothing is running.

| Part | State |
|---|---|
| `kb-kg/primer/`, `llm-era/`, `literature/`, `papers-benchmarks/` | first drafts |
| `kb-kg/projects/` | 77 entries (22 deep, 55 cards) and a generated index (`tools/build_projects_index.py`) |
| `kb-kg/landscape/` | two snapshots (19:13 and 19:54 UTC, 20261030) and the approved selection |
| `kb-kg/directions/` | nine pages and an overview, first drafts |
| `kb-kg/experiments/` | five proposals; X1 run, the other four not started |
| `pinakes/` | approach record, recommendations R1 to R7, 12 takeaways, ClaudeKB precedent, what Pinakes has measured, four proposals for what to measure next (P1 answered, the P4 pilot run, P2 blocked, P3's free-path half in the public benchmark repository, described on its own page) |
| `tools/` | `gh_snapshot.py` (57 tests), `build_projects_index.py` (12 tests), `check_public_safe.sh` |

Subagent cost, from the harness's per-agent totals: wave A about 4.1M tokens, wave B about 5.9M, wave C about
1.5M; about 11.5M in all.

## Waiting on the owner

1. **Whether to rotate the P4 key.** The key file was deleted at the owner's request on 20261102. The
   variable may still be exported in the owner's own terminal tab (`unset PINAKES_ANTHROPIC_API_KEY` clears it
   there). Its value was once malformed; rotating or revoking the key is the owner's call.
2. **The *historical* banner and link on Pinakes' `docs/graph/`.** The link now resolves. It is a separate
   change in the Pinakes repository: the assistant messages the Pinakes session with the file list first and
   needs the owner's go.
3. **Experiments.** X2, X3, X4 and X5 are not started and each needs its own yes (D-14). A larger P4 would be a
   new proposal; a BM25-alone arm for P3 would be a request to the benchmark repository's owner. The `NOTICE`
   copyright line uses the git author name "Luca Gattoni"; the owner may change it.

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
- **`CLAUDE.md`** now says the repository is public (the owner's yes, 20261102 08:57 UTC).
- **Benchmark repository** described and linked: [`pinakes/experiments/datasets-benchmark.md`](pinakes/experiments/datasets-benchmark.md),
  at its commit `9941f58`, with its limits kept; the owning session confirmed the framing.

## Next, once the owner answers

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
  approved 20260825, no labelled re-extraction trigger in `audit.py`, a defect count of five against six for the
  deep-loop report tool.
- **A rename in Pinakes.** A session in the Pinakes repository is renaming "the template release". This
  repository's `pinakes/approach/PINAKES_APPROACH.md` and `pinakes/recommendations-r1-r7.md` use the old name
  in places; re-read them against Pinakes' `STATUS.md` once the rename lands.
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
