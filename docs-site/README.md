# Documentation site

The documentation in this repository is published at <https://lucagattoni.github.io/knowledge-graph-tutorial/>
(MkDocs Material, the same setup as the Pinakes site). The site is a view over the files, never a
second copy: nothing is written for the site that is not also what GitHub shows.

## What is published

| Published | At | Left out (links to it go to GitHub) |
|---|---|---|
| every `.md` under `docs/`, with the `docs/` prefix removed (the new documentation) | `docs/README.md` is the home page; `docs/history/x.md` is `history/x/` | `README.md` at the repository root (a pointer for GitHub readers) |
| the archive: every `.md` under `kb-kg/` and `pinakes/`, and `DECISIONS.md` | its own path, so its URLs do not change (`kb-kg/primer/`, `DECISIONS/`) | `RESUME.md` (working state) |
| | | every file whose name starts with `_` (templates, drafts) |
| | | every non-Markdown file (`.tsv`, `repos.json`, images), `tools/`, `LICENSE`, `NOTICE` |

If `docs/` does not exist, staging falls back to the old behaviour: the root `README.md` is the
home page. If `docs/` exists without a `README.md`, staging stops: there would be no home page.

The rules are in `stage_docs.py` (`DOCS_DIR`, `ARCHIVE_FILES`, `ARCHIVE_DIRS`).

## How it is built

1. `tools/build_docs.py` writes the generated sections of `docs/` (A to Z index, watch list,
   changes, "Appears in"). CI runs it with `--check` and fails when they are stale; run it without
   `--check` after editing a page.
2. `stage_docs.py` copies the published files into `docs-src/` (ignored). MkDocs refuses a
   `docs_dir` that holds its own config file, and the content lives in the repository's own folders,
   so it is built from a copy. A page of `docs/` whose staged path equals an archive path (for
   example `docs/DECISIONS.md` or `docs/kb-kg/x.md`) stops staging with an error that names both.
   Staging also writes `docs-src/staged-paths.json`, the map from each staged path to the repository
   file it was copied from. `exclude_docs` in `mkdocs.yml` keeps that file out of the site.
3. `mkdocs build --strict` reads `mkdocs.yml` and `mkdocs_hooks.py`, and writes `site/` (ignored).
4. `.github/workflows/docs.yml` runs all of it on every pull request that touches these files, and
   deploys to GitHub Pages on push to `main`. **Strict**: a broken relative link or anchor in any
   page fails the build, and the site stays on its previous version.

## Links

Write for GitHub; the hook adapts the rest. A relative link is resolved against the page's
**repository path** (from `staged-paths.json`), not its staged path, because `docs/` loses its prefix
on the site. That is why `../../kb-kg/projects/lightrag.md` written in `docs/trends/x.md` works in both
places.

| The link points at (in the repository) | On the site |
|---|---|
| a staged page, with or without `#anchor` | a relative link between the two staged paths; the anchor is kept and checked |
| a folder whose `README.md` is staged (`../history/`, `../../kb-kg/primer/`, `../../docs/`) | that README (`../../docs/` is the home page) |
| a folder without a staged README, or any file that is not staged (`../../tools/x.py`, `RESUME.md`, the root `README.md`, a `.tsv`, a `_TEMPLATE.md`) | the same path on GitHub (`blob` or `tree`) |
| a template placeholder (`<slug>.md`) | the folder that holds such files, resolved as above |
| nothing in the repository | left as written, and the build fails |

Links inside code spans and fenced code blocks are not touched. Anchors use GitHub's rules (see
`mkdocs_hooks.py`), so a heading `## 5. Verification ledger` is `#5-verification-ledger`.

Every page's "edit this page" link points at its repository path (`docs/trends/x.md`, not
`trends/x.md`; `kb-kg/primer/README.md` for the primer), set in `on_page_context`.

## Navigation

The navigation is generated from the staged tree (`build_nav` in `mkdocs_hooks.py`); there is no
`nav:` in `mkdocs.yml`. The top level is shown as tabs (`navigation.tabs`, sticky). In order:

| Tab | Folder | Numbered | Inside |
|---|---|---|---|
| Home | `README.md` | no | the docs landing page |
| 1. History | `history/` | yes | |
| 2. Trends | `trends/` | yes | |
| 3. Projects | `projects/` | yes | |
| 4. Papers | `papers/` | yes | |
| 5. Datasets | `datasets/` | yes | |
| 6. Benchmarks | `benchmarks/` | yes | |
| 7. Experiments | `experiments/` | yes | |
| 8. Applied to Pinakes | `applied-to-pinakes/` | yes | |
| Index | `index/` | no | `README.md` first, then the entries by title |
| Archive | | no | KB/KG reference (`kb-kg/`, in its own order and labels), Pinakes notes (`pinakes/`), Decisions (`DECISIONS.md`) |

* The chapter list is `CHAPTERS` in `mkdocs_hooks.py`. A chapter number is its position in that
  list. A chapter whose folder does not exist (or holds no page) is skipped and the others **keep their
  numbers**, so a missing `experiments/` leaves 6 then 8.
* Inside a chapter: its `README.md` first, then the pages by front-matter `order` (an integer), then
  by title. Pages without `order` come after those with one. A value that is not an integer fails the
  build. The label of a page is its first `# ` heading, after the front matter.
* A folder in a chapter that holds pages is a section of its own, with the same rules.
* A page or folder outside these lists does not appear in the nav, and the strict build reports it
  as not included in the nav.
* The archive's internal order is `SECTION_ORDER` and its short labels are `SECTION_LABELS`.

The nav numbers the chapters and the pages inside them (`3.`, `3.2`).
`javascripts/page-numbering.js` puts that number in front of the page title (`3.2 - LightRAG`), and
numbers the headings below it in the page and in the right-hand contents list (`3.2.1 - …`,
`3.2.1.1 - …`; levels 2 and 3 only). It is done in the browser so the Markdown and its anchors stay
as GitHub renders them. Home, the Index tab and the Archive tab have no number in the nav, so the
script leaves them as written.

A heading that already starts with its own number (`## 3. Shifts in approach`) shows the site's
number instead of its own on a numbered page, so it never carries two; GitHub still shows the
author's. In the docs, headings carry no number at all.

## Diagrams

A fenced block whose language is `mermaid` is drawn as a diagram on the site (the `pymdownx.superfences`
custom fence in `mkdocs.yml`; the theme loads Mermaid itself), as GitHub draws it. The history timeline,
the trends map and the papers map use it. Each diagram is followed by a plain table or list with the same
content, for a reader whose viewer does not draw Mermaid. Links inside a diagram are not rewritten, so a
diagram holds labels, not links.

## Preview and test

```bash
uv run tools/build_docs.py              # refresh the generated sections of docs/
uv run docs-site/stage_docs.py          # copy the published files into docs-src/
uv run --no-project --with-requirements docs-site/requirements.txt mkdocs serve
uv run python -m unittest discover -s docs-site
```

`mkdocs serve` does not re-stage: run `stage_docs.py` again after editing a page. The build fails
with a message that names `stage_docs.py` when `docs-src/staged-paths.json` is missing.
