# Documentation site

The Markdown in this repository is published at <https://lucagattoni.github.io/knowledge-graph-tutorial/>
(MkDocs Material, the same setup as the Pinakes site). The site is a view over the files, never a
second copy: nothing is written for the site that is not also what GitHub shows.

## What is published

| Published | Left out (links to it go to GitHub) |
|---|---|
| `README.md` (the home page), `DECISIONS.md` | `RESUME.md` (working state) |
| every `.md` under `kb-kg/` and `pinakes/` | `repos.json`, `repos.tsv` and every other non-Markdown file |
| | `tools/`, `LICENSE`, `NOTICE` |

The list is `ROOT_FILES` and `ROOT_DIRS` in `stage_docs.py`.

## How it is built

1. `stage_docs.py` copies those files, keeping every path, into `docs-src/` (ignored). MkDocs
   refuses a `docs_dir` that holds its own config file, and the content lives at the repository
   root, so it is built from a copy.
2. `mkdocs build --strict` reads `mkdocs.yml` and `mkdocs_hooks.py`, and writes `site/` (ignored).
3. `.github/workflows/docs.yml` runs both on every pull request that touches these files, and
   deploys to GitHub Pages on push to `main`. **Strict**: a broken relative link or anchor in any
   page fails the build, and the site stays on its previous version.

## Writing pages that build

Write for GitHub; the hook adapts the rest. Relative links are resolved like this:

| The link points at | On the site |
|---|---|
| a published page (`.md`), with or without `#anchor` | kept, and the anchor is checked |
| a folder with a `README.md` (`primer/`) | that folder's `README.md` |
| a folder without one, or any file the site does not publish (`../../tools/x.py`, `RESUME.md`, a `.tsv`) | the same path on GitHub (`blob` or `tree`) |
| a template placeholder (`<slug>.md`) | the folder that holds such files |
| nothing in the repository | left as written, and the build fails |

Links inside code spans and fenced code blocks are not touched. Anchors use GitHub's rules (see
`mkdocs_hooks.py`), so a heading `## 5. Verification ledger` is `#5-verification-ledger`.

The navigation is generated from the folder tree: a new page appears under its section with no
edit here. Only the order of sections (`SECTION_ORDER`) and a few short section titles
(`SECTION_LABELS`) are written down in `mkdocs_hooks.py`; a page's nav label is its first `# ` heading.

## Preview and test

```bash
uv run docs-site/stage_docs.py
uv run --no-project --with-requirements docs-site/requirements.txt mkdocs serve
uv run python -m unittest discover -s docs-site
```

`mkdocs serve` does not re-stage: run `stage_docs.py` again after editing a page.
