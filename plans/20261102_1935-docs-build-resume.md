# Resume: the new documentation (`docs/`)

Last updated 20261103 01:08 UTC. **Merged to `main` on 20261103 01:07 UTC as `804c814`
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
| Chapters | History (8 eras), Trends (9 families, 2 themes), Projects (37 pages, 123-row watch list), Papers (68 in 10 groups), Datasets (26), Benchmarks (24), Experiments, Applied to Pinakes, Index (157 entries); 293 pages |
| Checked | every page was written, then checked by an agent that re-fetched its sources, then fixed; an independent audit against the owner's decisions ranked 15 gaps; most were fixed, some only in part, and the rest are listed under "Waiting on the owner" and "Known limits" below |
| Verified by the main session | strict site build exits 0; `tools/build_docs.py --check` exits 0; 70 generator tests and 44 site tests pass; no missing link target in 293 pages; 0 alias problems; `tools/check_public_safe.sh` exits 0 on its generic patterns |
| Live chapters | Projects, Papers, Datasets, Benchmarks, Trends: a `changes.tsv` each (one first-edition row) and generated sections |

## Waiting on the owner

1. **Review in a local preview** (the owner's condition S-6): the preview was served; the owner then asked for the push, the PR and
   the merge; how much of the 293 pages was read is unstated. The site is now published.
2. **The lists** (eras, trends, 37 projects, 68 papers, 26 datasets, 24 benchmarks) were chosen by the assistant under the
   owner's delegation, not approved item by item.
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
