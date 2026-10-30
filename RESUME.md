# Resume

Last updated 20261030 19:23 UTC. Decisions: [`DECISIONS.md`](DECISIONS.md). Branch:
`worktree-20261030_1852-kb-kg-docs-scaffold` (private remote; nothing is on `main` yet).

## Done and committed

| Commit | What |
|---|---|
| `2d95ad9` | Scaffold, templates, public-safety gate |
| `718d8e8` | `kb-kg/`: primer, LLM-era timeline, literature review, papers and benchmarks |
| `ddf740c` | 12 July investigations, each split into `kb-kg/projects/` and `pinakes/takeaways/` |
| `f1ddbfd` | `pinakes/`: approach record, recommendations R1 to R7, ClaudeKB precedent |
| `c8bf9c2` | Project `CLAUDE.md`, added at the owner's yes |
| `abc6be7` | `tools/gh_snapshot.py`, 57 tests, mutation-checked on the 90-day rule |
| `bcd1b3d` | First landscape snapshot, 20261030 19:13 UTC: 924 repositories, data only |
| `d955525` | `pinakes/experiments/`: what Pinakes has measured and how it decides |
| `f49c44d` | Proposed project selection; seven missed projects added to the watchlist |

## Running

Nothing. All twenty wave A writers have reported and been reviewed.

## Waiting on the owner

- **Approve or edit the selection**, [`kb-kg/landscape/20261030_1922-selection.md`](kb-kg/landscape/20261030_1922-selection.md):
  10 new deep entries and 55 cards, about 24 writer runs, about 5M tokens (a guess for the cards; the
  basis is in the file). Wave B does not start before this.

## Next, in order

1. Wave B, once the selection is approved: one Sonnet writer per deep entry, one per four cards, one
   writer per file, each following `kb-kg/projects/_TEMPLATE.md`. Review each against the live API as
   in wave A, run the gate and the link check, commit one unit at a time.
2. Re-run `uv run tools/gh_snapshot.py` after wave B: it picks up the seven watchlist additions and
   produces the first comparison with an earlier snapshot.
3. Wave C: `kb-kg/directions/` (what the field is trying, grouped by direction), the experiments worth
   running next (each states its cost, models and data first and waits for the owner's yes), and the
   Pinakes page on what to test next.
4. Licence for this repository's text, a full content check, then the owner's explicit yes to make it
   public. Only after that: the *historical* banner and link on Pinakes' `docs/graph/`.

## Debts that are written down so they are not lost

- **Unverified items.** Every entry lists its own "not verified" items. Across entries the largest are:
  six literature figures marked unverifiable (`kb-kg/literature/`); whether LazyGraphRAG is in the
  open-source package; many 2026 papers read as title or abstract only; whether the star growth of the
  fastest repositories is organic; the primer's first-use dates for "knowledge base" and for Cyc.
- **Snapshot recall is incomplete.** Seven expected projects were missed by its searches (now on the
  watchlist). Treat the snapshot as a dated sample, not a census.
- **Inconsistencies in Pinakes' own documents**, found while writing `pinakes/experiments/`, to report
  upstream when the owner allows editing Pinakes:
  - the scanned-PDF extraction run costs EUR 0.43 in `STATUS.md` and `MEASUREMENT-RUN.md` but EUR 0.11 in
    `DESIGN.md` (confirmed);
  - `STATUS.md` gives the corpus 107 411 non-transit edges at line 586 and 107 802 at line 631 for the
    same 106 506 sibling edges (confirmed);
  - not re-derived by me: no recorded result for the graph-gate re-run approved 20260825; no labelled
    re-extraction trigger in `audit.py`; a defect count of five against six for the deep-loop report tool.
- **Gate coverage.** `tools/check_public_safe.sh` scans the working tree, not the staged set.
- **Benchmark repository.** Describe it, link it only once the API reports it public (it did not at
  20261030 18:52 UTC).

## Not to do

- Do not make the repository public, or touch the Pinakes repository, without the owner's explicit
  yes at that step.
- Do not name private repositories anywhere in this repository.
