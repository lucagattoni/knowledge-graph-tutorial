# KB/KG reference: project instructions

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
- `kb-kg/` is field-neutral. Pinakes-specific reading goes in `pinakes/`, which links into `kb-kg/` for facts about other projects. One home per fact.
- Entries follow `kb-kg/projects/_TEMPLATE.md` and `pinakes/takeaways/_TEMPLATE.md`.
- Timestamps are UTC, read from the clock (`date -u "+%Y%m%d %H:%M"`). New dated files are named `YYYYMMDD_HHMM-<name>`.
- Landscape snapshots come from `uv run tools/gh_snapshot.py`; never hand-edit one.

<!-- Added at the owner's yes, 20261030 19:16 UTC, from the text proposed in the session that scaffolded this repository. -->
<!-- Heading and last bullet changed at the owner's yes, 20261102 08:57 UTC, after the repository went public (DECISIONS D-22). -->
<!-- Checked against the CLAUDE.md hygiene rules 20261102 08:57 UTC: 21 lines, about 215 words; no tidy proposed. -->
