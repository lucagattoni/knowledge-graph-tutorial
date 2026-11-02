# Resume: the new documentation (`docs/`)

Last updated 20261102 23:30 UTC. Branch `worktree-20261102_1805-docs-restructure-proposal`, rebased onto `origin/main`
at `3eede85`; **not pushed, not merged, not reviewed by the owner.** Decisions: row D-29 in [`DECISIONS.md`](../DECISIONS.md);
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

1. **Review in a local preview** (the owner's condition S-6) before anything is pushed or published.
2. **The lists** (eras, trends, 37 projects, 68 papers, 26 datasets, 24 benchmarks) were chosen by the assistant under the
   owner's delegation, not approved item by item.
3. **Merging to `main`** deploys the site (CI). Before it lands: fetch, rebase over the experiments session's newest commits,
   re-run the checks, and tell that session the file set (`mkdocs.yml`, `docs-site/**`, `.github/workflows/docs.yml`,
   `tools/build_docs*.py`, `README.md`, `docs/**`, `plans/**`, one `DECISIONS.md` row, one `RESUME.md` row).
4. **`CLAUDE.md` still describes the old structure.** Proposed edit (not applied): the title becomes "KB/KG documentation:
   project instructions"; add to Structure: "`docs/` is the documentation and the site's home; `kb-kg/`, `pinakes/` and
   `DECISIONS.md` are the archive and are never edited to match it. Add a project, paper, dataset, benchmark or trend as a page
   plus a row in its chapter's `changes.tsv`; then `uv run tools/build_docs.py` (never edit a generated section by hand;
   `--check` must exit 0). Page rules: `plans/20261102_1929-docs-writing-spec.md`."
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
