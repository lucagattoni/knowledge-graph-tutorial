# Resume

Last updated 20261030 19:16 UTC. Decisions: [`DECISIONS.md`](DECISIONS.md). Branch:
`worktree-20261030_1852-kb-kg-docs-scaffold` (private remote; nothing is on `main` yet).

## Done and committed

| Commit | What |
|---|---|
| `2d95ad9` | Scaffold, templates, public-safety gate |
| `718d8e8` | `kb-kg/`: primer, LLM-era timeline, literature review, papers and benchmarks |
| `ddf740c` | 12 July investigations, each split into `kb-kg/projects/` and `pinakes/takeaways/` |
| `f1ddbfd` | `pinakes/`: approach record, recommendations R1 to R7, ClaudeKB precedent |
| `c8bf9c2` | Project `CLAUDE.md`, added at the owner's yes |

## Running when this was written

- The landscape snapshot tool (`tools/gh_snapshot.py`, its tests, and the first snapshot under
  `kb-kg/landscape/`). Its test file `tools/test_gh_snapshot.py` line 121 holds a fake path and
  token on purpose and **fails the public-safety gate**; the fix is to build those strings by
  concatenation so the literal is never in the file. Do not commit the file until the gate passes.
- `pinakes/experiments/README.md` (what Pinakes has measured).

## Next, in order

1. Review both, run `tools/check_public_safe.sh` (must exit 0) and the link check, commit.
2. Choose the project list for wave B from the first snapshot: cards for every project in the four
   categories that is starred and pushed within 90 days, deep dives for about ten.
3. Wave B writes the entries; wave C writes `kb-kg/directions/` and the experiments to run next
   (each states its cost, models and data first and waits for the owner's yes).
4. Licence for this repository's text, a full content check, then the owner's explicit yes to make it
   public. Only after that: the *historical* banner and link on Pinakes' `docs/graph/`.

## Debts that are written down so they are not lost

- **Unverified items.** Every entry lists its own "not verified" items. Across entries the largest are:
  six literature figures marked unverifiable (`kb-kg/literature/`); whether LazyGraphRAG is in the
  open-source package; many 2026 papers read as title or abstract only; whether the star growth of the
  fastest repositories is organic; the primer's first-use dates for "knowledge base" and for Cyc.
- **Gate coverage.** `tools/check_public_safe.sh` scans the working tree, not the staged set.
- **Benchmark repository.** Describe it, link it only once the API reports it public.

## Not to do

- Do not make the repository public, or touch the Pinakes repository, without the owner's explicit
  yes at that step.
- Do not name private repositories anywhere in this repository.
