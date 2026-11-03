"""Tests for docs-site/stage_docs.py. Run: uv run python -m unittest discover -s docs-site"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import stage_docs as sd  # noqa: E402


def write(root: Path, rel: str, text: str = "x") -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def staged_files(out: Path) -> list[str]:
    return sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())


class StageTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        for rel in (
            "README.md",  # the root README: a GitHub-only pointer once docs/ exists
            "DECISIONS.md",
            "RESUME.md",
            "NOTICE",
            "kb-kg/a/b.md",
            "kb-kg/a/data.tsv",
            "kb-kg/projects/_TEMPLATE.md",
            "pinakes/p.md",
            "docs/README.md",
            "docs/history/README.md",
            "docs/history/x.md",
            "docs/trends/changes.tsv",
            "docs/trends/_draft.md",
            "tools/t.md",
        ):
            write(self.repo, rel)
        write(self.repo, "docs-site/stylesheets/s.css")
        write(self.repo, "docs-site/javascripts/j.js")
        self.out = self.repo / "docs-src"

    def test_docs_lose_their_prefix_and_the_archive_keeps_its_paths(self):
        self.assertEqual(sd.stage(self.repo, self.out), 6)
        self.assertEqual(
            staged_files(self.out),
            [
                "DECISIONS.md",
                "README.md",
                "history/README.md",
                "history/x.md",
                "javascripts/j.js",
                "kb-kg/a/b.md",
                "pinakes/p.md",
                "staged-paths.json",
                "stylesheets/s.css",
            ],
        )

    def test_the_home_page_is_docs_readme_not_the_root_readme(self):
        write(self.repo, "docs/README.md", "the new home")
        write(self.repo, "README.md", "the pointer")
        sd.stage(self.repo, self.out)
        self.assertEqual((self.out / "README.md").read_text(), "the new home")

    def test_underscore_files_and_non_markdown_are_not_staged(self):
        sd.stage(self.repo, self.out)
        names = staged_files(self.out)
        for left_out in ("kb-kg/projects/_TEMPLATE.md", "trends/_draft.md", "trends/changes.tsv", "kb-kg/a/data.tsv", "RESUME.md"):
            self.assertNotIn(left_out, names)

    def test_mapping_file_takes_each_staged_path_to_its_repository_path(self):
        sd.stage(self.repo, self.out)
        mapping = json.loads((self.out / sd.MAP_NAME).read_text())
        self.assertEqual(
            mapping,
            {
                "DECISIONS.md": "DECISIONS.md",
                "README.md": "docs/README.md",
                "history/README.md": "docs/history/README.md",
                "history/x.md": "docs/history/x.md",
                "kb-kg/a/b.md": "kb-kg/a/b.md",
                "pinakes/p.md": "pinakes/p.md",
            },
        )

    def test_without_docs_the_root_readme_is_the_home_page(self):
        shutil.rmtree(self.repo / "docs")
        self.assertEqual(sd.stage(self.repo, self.out), 4)
        self.assertEqual(
            json.loads((self.out / sd.MAP_NAME).read_text()),
            {"DECISIONS.md": "DECISIONS.md", "README.md": "README.md", "kb-kg/a/b.md": "kb-kg/a/b.md", "pinakes/p.md": "pinakes/p.md"},
        )

    def test_a_docs_path_that_the_archive_also_has_stops_staging_and_wipes_nothing(self):
        write(self.out, "keep.md")
        for clash in ("docs/DECISIONS.md", "docs/kb-kg/a/b.md"):
            write(self.repo, clash)
            with self.assertRaises(SystemExit) as raised:
                sd.stage(self.repo, self.out)
            self.assertIn(clash, str(raised.exception))
            self.assertTrue((self.out / "keep.md").exists())
            (self.repo / clash).unlink()
        sd.stage(self.repo, self.out)  # the clash is gone

    def test_docs_without_a_readme_stops_staging(self):
        (self.repo / "docs/README.md").unlink()
        with self.assertRaises(SystemExit) as raised:
            sd.stage(self.repo, self.out)
        self.assertIn("docs/README.md", str(raised.exception))

    def test_rebuild_drops_what_the_source_no_longer_has(self):
        sd.stage(self.repo, self.out)
        (self.repo / "docs/history/x.md").unlink()
        write(self.out, "stale.md")
        sd.stage(self.repo, self.out)
        self.assertNotIn("history/x.md", staged_files(self.out))
        self.assertNotIn("stale.md", staged_files(self.out))

    def test_refuses_to_wipe_the_repo_or_a_folder_outside_it(self):
        for bad in (self.repo, self.repo.parent, Path(tempfile.gettempdir()) / "elsewhere"):
            with self.assertRaises(SystemExit):
                sd.stage(self.repo, bad)


if __name__ == "__main__":
    unittest.main()
