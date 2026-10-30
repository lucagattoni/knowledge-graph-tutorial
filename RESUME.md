# Resume

Last updated 20261030 19:05 UTC. The decisions are in [`DECISIONS.md`](DECISIONS.md).

## Done

- Scaffold: section READMEs, the two entry templates, the public-safety gate (proven to fail on
  planted leaks and to pass on the clean tree).

## Running

- **Wave A**, background agents, one writer per file:
  - `tools/gh_snapshot.py` and its inputs (landscape snapshot tool)
  - the 12 external investigations, each split into `kb-kg/projects/<slug>.md` and
    `pinakes/takeaways/<slug>.md`
  - `pinakes/precedent/claudekb.md`
  - `kb-kg/literature/graph-rag-research.md` and `pinakes/recommendations-r1-r7.md`
  - `pinakes/approach/PINAKES_APPROACH.md`
  - `kb-kg/primer/README.md`, `kb-kg/llm-era/README.md`, `kb-kg/papers-benchmarks/README.md`

Nothing from wave A is trusted until it has been read and has passed the gate.

## Next

1. Review each wave A file; run `tools/check_public_safe.sh`; commit one logical unit at a time.
2. Run the snapshot tool; choose the project list for wave B (cards and a few deep dives).
3. Wave B: project entries. Wave C: directions, experiments to run next, Pinakes experiments page.
4. Full content check, licence choice, then ask for the explicit yes to make the repository public.
5. Only after that: the *historical* banner and link on Pinakes' `docs/graph/`.

## Not to do

- Do not make the repository public, and do not touch the Pinakes repository, without the owner's
  explicit yes at that step.
- Do not name private repositories anywhere in this repository.
