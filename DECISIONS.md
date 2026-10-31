# Decisions

Taken by the owner on 20261030 between 18:15 and 18:50 UTC, in the session that started this
repository's content. Each row is the owner's answer to a question asked with its options spelled
out; nothing here is inferred.

| # | Decision | Answer |
|---|---|---|
| D-1 | Audience and shape | An own research notebook. Pinakes is taken into account but kept **separate**: one pure KB/KG section, one distinct section for Pinakes development. |
| D-2 | What "which directions are being tested" means | All three: what the field is trying, what Pinakes tests, and what should be tested next. |
| D-3 | How far back | A short primer on the pre-LLM lineage, then the LLM era. |
| D-4 | Where it lives | Markdown in this repository. |
| D-5 | Project categories in scope | Core (GraphRAG, KG construction, KG querying); agent memory and temporal KGs; Markdown / LLM-wiki KBs; adjacent (code graphs, graph databases, RAG platforms). |
| D-6 | Ranking of "most active and starred" | Stars among repositories pushed in the last 90 days; also record stars per day, contributors and releases; flag growth that looks inorganic. |
| D-7 | Beyond GitHub | Papers and benchmarks are in scope. |
| D-8 | The 13 investigations in Pinakes `docs/graph/` | Copied here and updated; **this repository becomes the only source**. Pinakes' copies are marked *historical* and point here. |
| D-9 | Pointer from Pinakes | This repository is to become **public**, then Pinakes links to it. The visibility change is a separate, explicit step after a full content check (see open items). |
| D-10 | Which files move | All 16 files of Pinakes `docs/graph/`: the investigations and the literature review go to `kb-kg/`; the Pinakes approach document and the index go to `pinakes/`. |
| D-11 | Mixed content | Each investigation is split in two: a neutral project entry in `kb-kg/projects/`, and the Pinakes-specific takeaways in `pinakes/takeaways/`. |
| D-12 | Depth | Tiered: a short card for every project in scope, a deep dive only for those that matter most. |
| D-13 | Tracking over time | A reusable script run on demand, writing dated snapshots. |
| D-14 | Experiments | Decided one at a time: each states its cost, models and data first and runs only after an explicit yes. |
| D-15 | Benchmark | Pinakes retrieval is benchmarked against public datasets with ground-truth evidence, in its own repository. This repository describes the benchmark and links to it once that repository is public; Pinakes benchmark runs happen there. |
| D-16 | Parallel research | Maximum parallelism is allowed. Builder agents run on Sonnet. |
| D-17 | Licence (20261031) | **Apache-2.0 for everything**, text and code, with a `NOTICE` saying that quoted third-party text and fetched data keep their own terms. Chosen from four options. The visibility change is still a separate step. |
| D-18 | Free experiments (20261031) | X1 (describe the snapshots) and P1 (ask the Pinakes session whether the sections re-run happened) approved, run and recorded. |
| D-19 | A paid pilot (20261031) | P4 (the deep loop on 3 of the 20 frozen multi-hop questions) approved with a hosted model and a **total cap of EUR 10**. The owner sets the API key in their own terminal; no secrets file is read. X2, X4 and P3 are not started. |
| D-20 | Where the P4 key lives (20261031) | The owner chose to keep the API key in a file only they can read, outside any repository, so a terminal tab opened by the assistant can use it. This replaces the "set in the terminal only" part of D-19. The assistant never opens the file; the run script reads one line into its own process and refuses a file others can read. The owner deletes the file when P4 ends and may rotate the key. |

## Working rules adopted for this repository

These follow from the decisions above; the owner can overrule any of them.

- **Public from the first line.** The repository will become public, and a visibility change
  publishes its whole git history. So every commit is written as if public already: no private
  repository names, no local paths, no mailbox addresses, no keys. `tools/check_public_safe.sh`
  runs before every commit.
- **English** throughout, because every source document and the owner's other repositories are English.
- **One home per fact.** A fact about an external project lives in `kb-kg/projects/`; the `pinakes/`
  section links to it instead of repeating it.
- **Pinakes facts link to the public Pinakes repository** by absolute URL.

## Open items

| Item | Owner | Blocks |
|---|---|---|
| ~~Licence for this repository's text~~ | done: D-17 (the copyright line in `NOTICE` uses the git author name "Luca Gattoni"; the owner may change it) | |
| Full content check, then the explicit yes to make the repository public | owner | the pointer from Pinakes |
| Pinakes side: *historical* banner and link on the 16 files in `docs/graph/` | owner's go, then a separate change in the Pinakes repository under its own rules | nothing here; do it after the visibility change so the link does not dangle |
| Link to the benchmark repository | verify it reports public first | the `pinakes/experiments/` benchmark page |
| A project `CLAUDE.md` for this repository | owner's yes | nothing |
