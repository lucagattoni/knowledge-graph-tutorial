#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Copy the Markdown the documentation site publishes into docs-src/, ready for MkDocs.

    uv run docs-site/stage_docs.py [--out docs-src]

MkDocs refuses a docs_dir that holds its own config file, and this repository keeps its content in
its own folders, so the site is built from a copy.

What is staged, and where:

* docs/**/*.md with the "docs/" prefix removed: docs/README.md is the home page and
  docs/history/x.md is served at history/x/.
* The archive at its own paths, so its URLs do not change: kb-kg/**/*.md, pinakes/**/*.md and
  DECISIONS.md.
* Not staged: the root README.md (a GitHub-only pointer), RESUME.md, every file whose name starts
  with "_" (templates), and every non-Markdown file. Links to them go to GitHub (see
  mkdocs_hooks.py).
* If docs/ does not exist, the root README.md is the home page (the behaviour before docs/ existed).

A staged path that docs/ and the archive both claim stops staging with an error.

The staged-path to repository-path mapping is written to docs-src/staged-paths.json (excluded from
the site by `exclude_docs` in mkdocs.yml). The hook uses it to resolve links and to point each
page's "edit this page" link at the file that holds it.

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

DOCS_DIR = "docs"
# The archive: staged at its own paths.
ARCHIVE_FILES = ("DECISIONS.md",)
ARCHIVE_DIRS = ("kb-kg", "pinakes")
# The home page when docs/ does not exist.
FALLBACK_HOME = "README.md"
# Site assets, copied beside the pages because mkdocs.yml names them relative to docs_dir.
ASSET_DIRS = ("stylesheets", "javascripts")
# Written into the staged folder; mkdocs.yml excludes it from the published site.
MAP_NAME = "staged-paths.json"


def _markdown_under(folder: Path) -> list[Path]:
    """Every .md file under `folder` whose name does not start with "_", sorted."""
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.rglob("*.md") if p.is_file() and not p.name.startswith("_"))


def plan(repo: Path) -> dict[str, str]:
    """The staged path of every page, mapped to the repository path of the file it is copied from."""
    mapping: dict[str, str] = {}

    for name in ARCHIVE_FILES:
        if (repo / name).is_file():
            mapping[name] = name
    for name in ARCHIVE_DIRS:
        for src in _markdown_under(repo / name):
            rel = src.relative_to(repo).as_posix()
            mapping[rel] = rel

    docs = repo / DOCS_DIR
    if docs.is_dir():
        if not (docs / "README.md").is_file():
            raise SystemExit(f"{DOCS_DIR}/README.md is missing: it is the home page of the site")
        clashes = []
        for src in _markdown_under(docs):
            staged = src.relative_to(docs).as_posix()
            if staged in mapping:
                clashes.append(f"{DOCS_DIR}/{staged} and {mapping[staged]} would both be staged as {staged}")
            else:
                mapping[staged] = f"{DOCS_DIR}/{staged}"
        if clashes:
            raise SystemExit("staging stopped, a page of docs/ collides with the archive:\n  " + "\n  ".join(clashes))
    elif (repo / FALLBACK_HOME).is_file():
        mapping[FALLBACK_HOME] = FALLBACK_HOME

    return dict(sorted(mapping.items()))


def stage(repo: Path, out: Path) -> int:
    """Rebuild `out` from `repo` and return the number of pages copied."""
    if out == repo or repo.is_relative_to(out) or not out.is_relative_to(repo):
        raise SystemExit(f"refusing to wipe {out}: it must be a folder inside {repo}")
    mapping = plan(repo)  # may stop with an error: do it before anything is wiped
    if out.exists():
        shutil.rmtree(out)

    for staged, source in mapping.items():
        dest = out / staged
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(repo / source, dest)

    for name in ASSET_DIRS:
        shutil.copytree(repo / "docs-site" / name, out / name)
    (out / MAP_NAME).write_text(json.dumps(mapping, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return len(mapping)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=Path, default=REPO / "docs-src", help="folder to rebuild (default: docs-src)")
    args = ap.parse_args()
    n = stage(REPO, args.out.resolve())
    print(f"staged {n} pages into {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
