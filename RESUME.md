# Resume

Last updated 20261030 20:09 UTC. Decisions: [`DECISIONS.md`](DECISIONS.md). Branch:
`worktree-20261030_1852-kb-kg-docs-scaffold` (private remote; nothing is on `main` yet). The last content
commit before this update is `9c01d6b`.

## State

The first full pass is written, reviewed and pushed. Nothing is running.

| Part | State |
|---|---|
| `kb-kg/primer/`, `llm-era/`, `literature/`, `papers-benchmarks/` | first drafts |
| `kb-kg/projects/` | 77 entries (22 deep, 55 cards) and a generated index (`tools/build_projects_index.py`) |
| `kb-kg/landscape/` | two snapshots (19:13 and 19:54 UTC, 20261030) and the approved selection |
| `kb-kg/directions/` | nine pages and an overview, first drafts |
| `kb-kg/experiments/` | five proposals, **none run** |
| `pinakes/` | approach record, recommendations R1 to R7, 12 takeaways, ClaudeKB precedent, what Pinakes has measured, four proposals for what to measure next (**none run**) |
| `tools/` | `gh_snapshot.py` (57 tests), `build_projects_index.py` (12 tests), `check_public_safe.sh` |

Subagent cost, from the harness's per-agent totals: wave A about 4.1M tokens, wave B about 5.9M, wave C about
1.5M; about 11.5M in all.

## Waiting on the owner

1. **Experiments.** [`kb-kg/experiments/README.md`](kb-kg/experiments/README.md) and
   [`pinakes/experiments/next.md`](pinakes/experiments/next.md): which to start, with which model, under which
   pilot cap. Each needs its own yes (D-14).
2. **A licence for this repository's text.**
3. **A full content check, then the explicit yes to make the repository public.** The gate and the checks run
   so far do not replace that review.
4. **After the flip only:** the *historical* banner and link on Pinakes' `docs/graph/`.
5. **The benchmark repository.** Describe it; link it only once the API reports it public (it did not at
   20261030 18:52 UTC).

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

- Do not make the repository public, or touch the Pinakes repository, without the owner's explicit yes at that
  step.
- Do not name private repositories anywhere in this repository.
- Do not start an experiment, or any paid run, without the owner's yes for that experiment.
