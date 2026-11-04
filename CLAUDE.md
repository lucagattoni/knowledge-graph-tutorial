# KB/KG documentation: project instructions

Structure and decisions: README.md, DECISIONS.md. Current state and next step: RESUME.md.

## This repository is public
- Run `tools/check_public_safe.sh` before every commit; it must exit 0. Every commit is published with the whole history.
- Never write a local path, mailbox address, key, or the name of a private repository.
- Never edit the Pinakes repository without the owner's explicit yes at that step.

## Evidence
- Every statement about a project, paper or benchmark cites a source and the UTC time it was read. Where sources are silent, write `unstated`.
- Facts about 2026 never come from memory; fetch them.
- Licence comes from the LICENSE file, not the README badge. GPL or non-commercial projects are read-only references: ideas and results only, no code.

## Structure
- `docs/` is the documentation and the site's home. `kb-kg/`, `pinakes/` and `DECISIONS.md` are the archive: sources for `docs/`, never edited to match it.
- Add a project, paper, dataset, benchmark or trend as a page plus a row in its chapter's `changes.tsv`, then `uv run tools/build_docs.py`. Never hand-edit a generated section; `uv run tools/build_docs.py --check` must exit 0. Page rules: `plans/20261102_1929-docs-writing-spec.md`. Build and checks: `docs-site/README.md`.
- `docs/experiments/` quotes `kb-kg/experiments/`, decision rows and `tools/exp/` test counts with commit-pinned read times: refresh it after any change to those. Before landing a refresh, `git fetch` and merge `main` into the branch again, then re-check.
- A push to `main` that touches `docs/`, the archive, `mkdocs.yml`, `docs-site/` or `tools/build_docs.py` deploys the site (`.github/workflows/docs.yml`; CI builds with `--strict`).
- Archive: `kb-kg/` is field-neutral. Pinakes-specific reading goes in `pinakes/`, which links into `kb-kg/` for facts about other projects. One home per fact.
- Archive entries follow `kb-kg/projects/_TEMPLATE.md` and `pinakes/takeaways/_TEMPLATE.md`.
- Timestamps are UTC, read from the clock (`date -u "+%Y%m%d %H:%M"`). New dated files are named `YYYYMMDD_HHMM-<name>`.
- Landscape snapshots come from `uv run tools/gh_snapshot.py`; never hand-edit one.

<!-- Added at the owner's yes, 20261030 19:16 UTC, from the text proposed in the session that scaffolded this repository. -->
<!-- Heading and last bullet changed at the owner's yes, 20261102 08:57 UTC, after the repository went public (DECISIONS D-22). -->
<!-- Title and Structure changed at the owner's yes, 20261103 01:14 UTC, after the new documentation in docs/ was merged (DECISIONS D-29); the text was proposed in plans/20261102_1935-docs-build-resume.md, plus the docs/experiments refresh and deploy bullets. -->
<!-- Checked against the CLAUDE.md hygiene rules 20261103 01:14 UTC: 28 lines, 300 words (own-line comments excluded); no tidy proposed. -->
<!-- Merge-first sentence in the docs/experiments bullet added at the owner's yes, 20261104 12:18 UTC ("go with your recommendations"): the archive moved twice (6f59c99 at 11:15, fe72070 at 11:29 UTC) while PR 5 was open, and each move made statements on the pages false. Re-checked against the hygiene rules in the same edit: 315 words (own-line comments excluded), every path it names exists (changes.tsv is one file per chapter); no tidy proposed. -->
