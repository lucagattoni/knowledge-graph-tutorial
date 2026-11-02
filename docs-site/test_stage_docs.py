"""Tests for docs-site/stage_docs.py. Run: uv run python -m unittest discover -s docs-site"""

from __future__ import annotations

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


class StageTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        for rel in ("README.md", "DECISIONS.md", "RESUME.md", "NOTICE", "kb-kg/a/b.md", "kb-kg/a/data.tsv", "pinakes/p.md"):
            write(self.repo, rel)
        write(self.repo, "tools/t.md")
        write(self.repo, "docs-site/stylesheets/s.css")
        write(self.repo, "docs-site/javascripts/j.js")

    def staged(self, out: Path) -> list[str]:
        return sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())

    def test_copies_published_markdown_and_assets_only(self):
        out = self.repo / "docs-src"
        self.assertEqual(sd.stage(self.repo, out), 4)
        self.assertEqual(
            self.staged(out),
            ["DECISIONS.md", "README.md", "javascripts/j.js", "kb-kg/a/b.md", "pinakes/p.md", "stylesheets/s.css"],
        )

    def test_rebuild_drops_what_the_source_no_longer_has(self):
        out = self.repo / "docs-src"
        sd.stage(self.repo, out)
        (self.repo / "kb-kg/a/b.md").unlink()
        write(out, "stale.md")
        sd.stage(self.repo, out)
        self.assertNotIn("kb-kg/a/b.md", self.staged(out))
        self.assertNotIn("stale.md", self.staged(out))

    def test_refuses_to_wipe_the_repo_or_a_folder_outside_it(self):
        for bad in (self.repo, self.repo.parent, Path(tempfile.gettempdir()) / "elsewhere"):
            with self.assertRaises(SystemExit):
                sd.stage(self.repo, bad)


if __name__ == "__main__":
    unittest.main()
