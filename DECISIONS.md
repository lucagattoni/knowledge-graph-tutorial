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
| D-21 | The P4 runs go ahead without a typed confirmation (20261101) | After two confirmation prompts went unanswered (the tabs were closed before anything was confirmed, so nothing was reserved or spent), the owner authorised the assistant in writing to run all three P4 questions itself with `--yes`, one at a time. Pinakes' budget windows (EUR 2.00 an operation, EUR 10.00 a day and a month) still refuse any run over them. The assistant re-reads each estimate for free before its run and stops on the first failure or refusal, with no retry for a better answer. The authorisation covers these three questions only. |
| D-22 | The repository goes public (20261102) | The owner said "repo public OK" and "full content check OK". The assistant did the check itself over all 60 commits and found nothing: no secret-shaped string, no private repository name (the 13 private repositories of the owner's account and the local list were all searched), no local path, no machine name, no mailbox address in content, no blob over 500 KB except the two public GitHub snapshots. The author address in the commits is already public in the Pinakes repository's history. The branch was fast-forwarded onto `main` (it held only `.gitignore`), then the visibility changed at 08:46 UTC. The P4 key file was deleted at the owner's request first. |
| D-23 | Pinakes' `docs/graph/` copies marked historical (20261102) | The owner gave the go ("add historical banner on Pinakes with links to the researches in this repo"). The 16 files now open with a "Historical copy, moved" banner naming their counterparts here: 68 lines added to `docs/graph/`, none removed or reworded, plus one row in `docs/README.md` and a `changelog.d/` fragment. Done under Pinakes' own rules: a worktree, the sessions told the file set first (the one that replied confirmed no overlap), `check.sh` and `make docs` read by exit status (the first `check.sh` run failed two `test_mutate` tests only because this harness sets `PYTHONDONTWRITEBYTECODE=1`; the rerun with it unset exited 0 with 2,908 passed), `tools/shared_file_overlap.py` reporting none, landed with `tools/land.py` as `dee3f04`, no tag, no release. Pinakes' CI and docs workflows succeeded on `dee3f04` and the published docs site shows the banner. |
| D-24 | Experiment constraints and order (20261102) | The owner set three constraints: experiments run only on the owner's Apple Silicon Macs (another Mac only through an `ssh` command approved each time, no cloud hardware); the repository is public but is the owner's own notebook (no packaging for outside replication, and the public-safety rules still apply); hosted models are acceptable, both OpenAI's and Anthropic's, one model per comparison. The owner delegated the choice between a full plan and a slim one; the assistant chose slim, because each proposal already states its question, method and risks and each paid run gets its own pre-registered plan before its first paid call. After free groundwork (Step 0) the recommended order is X2, X4, X3, X5, with a gate and an explicit yes between steps (D-14). It stays a recommendation until the owner says yes to Step 0. Details: [`kb-kg/experiments/README.md`](kb-kg/experiments/README.md#order-and-gates); the Pinakes follow-ups are in [`pinakes/experiments/next.md`](pinakes/experiments/next.md#order-for-the-follow-ups). |
| D-25 | Step 0 of the experiments is built (20261102) | The owner said "Yes, build Step 0". Seven Sonnet agents and I built it with the owner's constraints (Apple Silicon only; OpenAI or Anthropic models, one per comparison; no model called, no key): the 20 X2 documents (a hash rule written before the result was seen) and the 20 X4 questions with hand-derived answers (Flask, Gin) frozen; a stub model server; a statistics helper; rehearsals of four builders; a metering gateway. I verified each unit myself before committing it: reran every runner, re-derived 9 of 20 X4 answers with a different method, ran my own mutants, and drove the gateway with the real OpenAI and Anthropic SDKs against fake providers. Defects found along the way (a stub undercounting parallel calls, two weak statistics tests, two corrections to my own entries, a broken table row, a red-baseline mutation harness of mine) are in the commit messages. **Not done:** the gateway has never met a real provider or a builder; there is no X4 scoring program; no output tokens are measured, so no cost can be derived; the question wording has not been tried on an agent. The first paid step still needs the owner's yes with model, provider and cap (D-14). Details: [`kb-kg/experiments/README.md`](kb-kg/experiments/README.md#order-and-gates). |
| D-26 | Pass A: a local model, with thinking switched off at the gateway (20261102) | The owner chose "Local pass A" and then `granite4.2:8b`. I had proposed that model because its library card showed no thinking label; the installed model reports a `thinking` capability and, left alone, answered one test question in 17 s and 278 tokens against 0.3 s and 8 with `reasoning_effort: "none"`. The builders cannot send that field, so the metering gateway gained an opt-in `request_defaults` table (local no-key upstreams only; the fields it adds are named in each call's log record), and the four pass-A runners take `--chat-default`. A second derived model caps an answer at 6,144 tokens, after one answer ran past 15,700. Each builder then indexed one document with the real model: output tokens were 4 to 15 times the stub's, and nano-graphrag failed because the model wrote one delimiter wrongly in every relationship. **Not done:** nothing beyond one document has run. My arithmetic puts 5 documents for three builders at about 1.8 h and 20 documents at about 10.5 h, so the next step waits for the owner (options on the pass-A page). Nothing paid ran. Details: [`kb-kg/experiments/x2-index-cost/pass-a-local-model.md`](kb-kg/experiments/x2-index-cost/pass-a-local-model.md). |

## Working rules adopted for this repository

These follow from the decisions above; the owner can overrule any of them.

- **Public from the first line.** The repository has been public since 20261102 (D-22), and the visibility
  change published its whole git history. Every commit is written as public: no private
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
| ~~Full content check, then the explicit yes to make the repository public~~ | done: D-22 | |
| ~~Pinakes side: *historical* banner and link on the 16 files in `docs/graph/`~~ | done 20261102: D-23 | |
| ~~Link to the benchmark repository~~ | done 20261102: [`pinakes/experiments/datasets-benchmark.md`](pinakes/experiments/datasets-benchmark.md) | |
| ~~A project `CLAUDE.md` for this repository~~ | done: added at the owner's yes; its heading changed to "is public" at the owner's yes on 20261102 | |
