#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Copy the Markdown the documentation site publishes into docs-src/, ready for MkDocs.

    uv run docs-site/stage_docs.py [--out docs-src]

MkDocs refuses a docs_dir that holds its own config file, and this repository keeps its content at
the root, so the site is built from a copy. The copy keeps every path: a page's URL, its "edit this
page" link and its relative links all match the repository.

Only Markdown is published. RESUME.md (working state) and the landscape data files (repos.json,
repos.tsv) stay out; links to them go to GitHub (see mkdocs_hooks.py).

Standard library only.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# What the site publishes. Everything else in the repository stays off it.
ROOT_FILES = ("README.md", "DECISIONS.md")
ROOT_DIRS = ("kb-kg", "pinakes")
# Site assets, copied beside the pages because mkdocs.yml names them relative to docs_dir.
ASSET_DIRS = ("stylesheets", "javascripts")


def stage(repo: Path, out: Path) -> int:
    """Rebuild `out` from `repo` and return the number of pages copied."""
    if out == repo or repo.is_relative_to(out) or not out.is_relative_to(repo):
        raise SystemExit(f"refusing to wipe {out}: it must be a folder inside {repo}")
    if out.exists():
        shutil.rmtree(out)

    pages = [repo / name for name in ROOT_FILES]
    for name in ROOT_DIRS:
        pages += sorted((repo / name).rglob("*.md"))
    for src in pages:
        dest = out / src.relative_to(repo)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)

    for name in ASSET_DIRS:
        shutil.copytree(repo / "docs-site" / name, out / name)
    return len(pages)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=Path, default=REPO / "docs-src", help="folder to rebuild (default: docs-src)")
    args = ap.parse_args()
    n = stage(REPO, args.out.resolve())
    print(f"staged {n} pages into {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
