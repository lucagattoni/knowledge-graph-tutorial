# Resume: the new documentation (`docs/`)

Last updated 20261104 11:57 UTC. **Fifth merge: PR 5 (`docs/experiments/` brought from the archive's `56aaece` to `fe72070`: the console's USD 0.67 explained as the list price less complimentary daily tokens, "the better reading", not a proof (D-41); the data-sharing finding and the owner's "Leave it on" (D-42); the free-token fit exact in completion order, the finding this documentation made and the archive adopted in `6f59c99`, with its own caveat that two orders were tried and the second chosen after seeing the gap) was merged to `main` on 20261104 11:55 UTC as `b6064b8` on the owner's instruction "Merge now"; the docs workflow run 41824877689 for that commit succeeded (build and deploy), and the deployed X2 page carries the section "Data handling: what the pilot probably shared with OpenAI" and names `fe72070`. Three things on the X2 page are this documentation's own and not the archive's: the reading that the owner's earlier "Agrees" for stages A to C probably compared requests or tokens, the observation that the completion-order match is narrow (2 of 1,751 starting calls), and a sum check of input less cached. Next for the pages: a refresh after any experiments-session commit that changes pilot figures or records; closing the pilot (key file, key, project) is the owner's.**
**Fourth merge: PR 4 (`docs/experiments/` with the paid pilot's results, stages A to D, at the archive's `56aaece`; the pilot's cost shown as open between USD 1.10537, 1.18389 and the console's 0.67) was merged to `main` on 20261104 10:42 UTC as `ad2f0c4` on the owner's instruction "Merge now"; the docs workflow run for that commit succeeded (build and deploy) and the deployed X2 page carries the section "What the console showed".**
**Third merge: PR 3 (the owner's answers to the four cases left open by the review: a Semantica page, a
paper group for the new trend, a sentence on Open Knowledge Format; the RDF-star Index entry corrected) was merged to `main` on
20261103 10:45 UTC as `c31f54e` on the owner's instruction "Merge now"; the docs workflow run for that commit succeeded (build and
deploy), and the deployed Semantica page, the new paper group and the corrected RDF-star entry answered 200 with the new content.**
**Second merge: PR 2 (the owner's review of the lists, item 2 below: a tenth trend, five project
pages, the experiments pages at `37c922c`, each new page re-read against its sources by a second agent) was merged to `main` on
20261103 08:47 UTC as `ba1247f` on the owner's instruction "Merge now"; the docs workflow run for that commit succeeded (build and
deploy), and the deployed trend page, a new project page and the trends overview answered 200 with the new content.**
**First merge, 20261103 01:07 UTC as `804c814`
([PR #1](https://github.com/lucagattoni/knowledge-graph-tutorial/pull/1)) on the owner's instruction "merge it"; the docs workflow
run for that commit succeeded (build and deploy) and the deployed site's home page and a deeper page answered 200, the deeper one
with the newest wording.** The branch was `worktree-20261102_1805-docs-restructure-proposal`; before the merge the experiments
session's commits up to `6a2e30e` were merged into it and `docs/experiments/` follows them. Auto-fix was not enabled (the app
refused: the session does not run on this computer). Decisions: row D-29 in [`DECISIONS.md`](../DECISIONS.md);
the owner's structure answers: [`20261102_1915-docs-from-scratch-plan.md`](20261102_1915-docs-from-scratch-plan.md); the lists
and the evidence for them: [`20261102_1951-docs-catalogue.md`](20261102_1951-docs-catalogue.md) and [`evidence/`](evidence/);
the rules every page follows: [`20261102_1929-docs-writing-spec.md`](20261102_1929-docs-writing-spec.md).

## State

| What | State |
|---|---|
| Chapters | History (8 eras), Trends (10 families, 2 themes), Projects (43 pages, 123-row watch list), Papers (73 in 11 groups), Datasets (26), Benchmarks (24), Experiments, Applied to Pinakes, Index (157 entries); 301 pages (counted 20261103) |
| Checked | every page was written, then checked by an agent that re-fetched its sources, then fixed; an independent audit against the owner's decisions ranked 15 gaps; most were fixed, some only in part, and the rest are listed under "Waiting on the owner" and "Known limits" below |
| Verified by the main session | strict site build exits 0; `tools/build_docs.py --check` exits 0; 70 generator tests and 44 site tests pass; no missing link target in 293 pages; 0 alias problems; `tools/check_public_safe.sh` exits 0 on its generic patterns |
| Live chapters | Projects, Papers, Datasets, Benchmarks, Trends: a `changes.tsv` each (one first-edition row) and generated sections |

## Waiting on the owner

1. **Review in a local preview** (the owner's condition S-6): the preview was served; the owner then asked for the push, the PR and
   the merge; how much of the 293 pages was read is unstated. The site is now published.
2. **The lists were reviewed item by item on 20261103** (D-33; record in `20261102_1951-docs-catalogue.md`, section "The owner's
   review of the lists"). Answered later the same day: **Open Knowledge Format** gets a sentence in the Projects chapter
   and no page; **Semantica** gets a page and is named in the construction trend; the Papers chapter gets a group for the new
   trend (five papers; the owner chose it over stating an exception); the five agent-memory pages keep their length (1,200 to
   1,550 words against the 500 to 900 target: a known limit). Still open: Honcho, SurrealDB and MemMachine are borderline (the writer of the
   reasons leaned towards no page; MemMachine has one of the few independent agent-memory scores, on the LoCoMo benchmark
   page) and TrustGraph is the weaker twin of Semantica; the watch list notes say why none has a page.
3. **Done:** the merge to `main` (above). Each later change to a fact that `docs/experiments/` quotes needs the page refreshed;
   the experiments session was told the file set and to tell the documentation session the paths it changes. A push to `main`
   deploys the site when it touches `docs/**`, `DECISIONS.md`, `kb-kg/**`, `pinakes/**`, `tools/build_docs.py`,
   `tools/test_build_docs.py`, `mkdocs.yml`, `docs-site/**` or `.github/workflows/docs.yml` (the workflow's own path filter).
4. **Done 20261103 01:14 UTC, at the owner's yes:** `CLAUDE.md` now has the title "KB/KG documentation: project instructions" and
   Structure bullets for `docs/` and the archive, how to add a page and run the generator, the `docs/experiments/` refresh rule
   and the fact that a push to `main` which touches the site's paths deploys it.
5. **Safety gate false positive:** the pattern for local paths (`/home/<name>/`) matches real web addresses that contain
   `/home/` (two author copies of papers on a university site were replaced by DOIs). A narrower pattern is the owner's call.
6. **Private-name list:** `tools/public-safe-patterns.local.txt` does not exist in either checkout, so the gate does not check
   private repository names (open item 3 in `RESUME.md`).

## Known limits (from the audit and the checkers)

- The six project pages written on 20261103 (supermemory, TencentDB Agent Memory, Memori, memU, EverOS, Semantica) run about
  1,200 to 1,550 words against the 500 to 900 target, because a second check added verified corrections; the owner chose to
  leave them. The new trend page and the new paper group are also over their length targets.
- The new paper group places Pérez et al. (2006, SPARQL semantics) beside the RDF-star papers, where the Papers chapter's rule
  would send a SPARQL-semantics paper to Foundations; the group page gives its reason.

- Index entries and some other pages run over their length targets (index entries 400 to 490 words against 150 to 400).
- `Foundations` is one 8,600-word page; the Papers map is not clickable (links inside a Mermaid diagram are not rewritten).
- `graph-query-generation`, `plain-file-knowledge` have one fundamental paper each; the other papers in the pools are in
  "Further reading".
- The comparison table in the Trends overview has sentence-length cells.
- Hand-typed star and release figures on trend pages are dated; the watch list and project pages carry the live values.
- Several 2026 arXiv records show a first-version date earlier than the identifier suggests; pages cite the record's date and say so.
- Citation counts come from Semantic Scholar, OpenAlex or Crossref as each source line says; counts from different sources are never compared.

## To continue

```bash
uv run tools/build_docs.py                # rebuild generated sections (A to Z, appears-in, watch list, change lists)
uv run tools/build_docs.py --check        # exit 1 if stale
uv run docs-site/stage_docs.py            # stage; then: uv run --no-project --with-requirements docs-site/requirements.txt mkdocs serve
bash tools/check_public_safe.sh           # before every commit
```
