"""Tests for tools/build_projects_index.py. Run: uv run python -m unittest tools/test_build_projects_index.py"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import build_projects_index as idx  # noqa: E402


def entry(slug: str, tier="card", category="core", repo="o/r", title="T", snapshot="20261030 19:00 UTC") -> str:
    return (
        f"---\nslug: {slug}\nrepo: {repo}\ntier: {tier}\ncategory: {category}\nsnapshot: {snapshot}\n---\n\n"
        f"# {title}\n\nBody.\n"
    )


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def put(self, name: str, text: str) -> None:
        (self.dir / name).write_text(text, encoding="utf-8")


class ParseTests(Fixture):
    def test_reads_front_matter_and_title(self) -> None:
        self.put("alpha.md", entry("alpha", title="Alpha Project", repo="a/alpha"))
        meta = idx.parse_entry(self.dir / "alpha.md")
        self.assertEqual(meta["repo"], "a/alpha")
        self.assertEqual(meta["title"], "Alpha Project")

    def test_slug_must_match_file_name(self) -> None:
        self.put("alpha.md", entry("beta"))
        with self.assertRaises(idx.EntryError):
            idx.parse_entry(self.dir / "alpha.md")

    def test_unknown_category_and_tier_are_refused(self) -> None:
        self.put("a.md", entry("a", category="other"))
        self.put("b.md", entry("b", tier="huge"))
        with self.assertRaises(idx.EntryError):
            idx.parse_entry(self.dir / "a.md")
        with self.assertRaises(idx.EntryError):
            idx.parse_entry(self.dir / "b.md")

    def test_missing_or_unclosed_front_matter_is_refused(self) -> None:
        self.put("a.md", "# no front matter\n")
        self.put("b.md", "---\nslug: b\nrepo: o/r\n")
        with self.assertRaises(idx.EntryError):
            idx.parse_entry(self.dir / "a.md")
        with self.assertRaises(idx.EntryError):
            idx.parse_entry(self.dir / "b.md")

    def test_missing_required_key_is_refused(self) -> None:
        self.put("a.md", "---\nslug: a\nrepo: o/r\ntier: card\n---\n\n# A\n")
        with self.assertRaises(idx.EntryError):
            idx.parse_entry(self.dir / "a.md")


class LoadAndRenderTests(Fixture):
    def test_template_and_readme_are_skipped(self) -> None:
        self.put("_TEMPLATE.md", "not an entry")
        self.put("README.md", "old index")
        self.put("a.md", entry("a"))
        self.assertEqual([e["slug"] for e in idx.load_entries(self.dir)], ["a"])

    def test_deep_entries_sort_before_cards_then_by_title(self) -> None:
        self.put("zeta.md", entry("zeta", tier="deep", title="Zeta"))
        self.put("beta.md", entry("beta", tier="card", title="Beta"))
        self.put("alpha.md", entry("alpha", tier="card", title="Alpha"))
        text = idx.render(idx.load_entries(self.dir))
        self.assertLess(text.index("[Zeta]"), text.index("[Alpha]"))
        self.assertLess(text.index("[Alpha]"), text.index("[Beta]"))

    def test_counts_and_groups(self) -> None:
        self.put("a.md", entry("a", tier="deep", category="agent-memory"))
        self.put("b.md", entry("b", tier="card", category="core"))
        text = idx.render(idx.load_entries(self.dir))
        self.assertIn("2 entries: 1 deep and 1 cards", text)
        self.assertIn("## agent-memory (1)", text)
        self.assertIn("## markdown-kb (0)", text)

class CheckModeTests(Fixture):
    def run_main(self, *extra: str) -> int:
        return idx.main(["--dir", str(self.dir), *extra])

    def test_write_then_check_is_current(self) -> None:
        self.put("a.md", entry("a"))
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(self.run_main("--check"), 0)

    def test_check_fails_when_an_entry_changes(self) -> None:
        self.put("a.md", entry("a"))
        self.run_main()
        self.put("b.md", entry("b"))
        self.assertEqual(self.run_main("--check"), 1)

    def test_check_fails_when_the_index_is_missing(self) -> None:
        self.put("a.md", entry("a"))
        self.assertEqual(self.run_main("--check"), 1)

    def test_bad_entry_exits_2(self) -> None:
        self.put("a.md", "# no front matter\n")
        self.assertEqual(self.run_main(), 2)


if __name__ == "__main__":
    unittest.main()
