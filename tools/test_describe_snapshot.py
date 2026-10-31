"""Tests for tools/describe_snapshot.py. Run: uv run python -m unittest tools/test_describe_snapshot.py"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import describe_snapshot as ds  # noqa: E402

HEADER = ["full_name", "category", "table", "stars", "stars_per_day", "forks_per_100_stars",
          "open_issues", "contributors", "days_since_push", "flags"]


def tsv(rows: list[list[str]]) -> str:
    return "\n".join("\t".join(r) for r in [HEADER, *rows]) + "\n"


def row(name="o/r", cat="core", table="ranked", stars="100", spd="1", fork="5", issues="2",
        contrib="", days="3", flags="") -> list[str]:
    return [name, cat, table, stars, spd, fork, issues, contrib, days, flags]


class PercentileTests(unittest.TestCase):
    def test_median_of_odd_and_even_lists(self) -> None:
        self.assertEqual(ds.percentile([1, 2, 3], 50), 2)
        self.assertEqual(ds.percentile([1, 2, 3, 4], 50), 2.5)

    def test_extremes_and_single_value(self) -> None:
        self.assertEqual(ds.percentile([5, 9], 0), 5)
        self.assertEqual(ds.percentile([5, 9], 100), 9)
        self.assertEqual(ds.percentile([7], 90), 7)

    def test_interpolates_between_neighbours(self) -> None:
        self.assertAlmostEqual(ds.percentile([0, 10], 25), 2.5)

    def test_empty_list_is_an_error(self) -> None:
        with self.assertRaises(ValueError):
            ds.percentile([], 50)

    def test_percentile_rank_counts_values_at_or_below(self) -> None:
        values = [1, 2, 3, 4]
        self.assertEqual(ds.percentile_rank(values, 3), 75)
        self.assertEqual(ds.percentile_rank(values, 0), 0)
        self.assertEqual(ds.percentile_rank(values, 4), 100)

    def test_percentile_rank_of_a_tie_includes_the_tie(self) -> None:
        self.assertEqual(ds.percentile_rank([2, 2, 2, 5], 2), 75)


class ParseTests(unittest.TestCase):
    def test_number_handles_blank_and_text(self) -> None:
        self.assertIsNone(ds.number(""))
        self.assertIsNone(ds.number("n/a"))
        self.assertEqual(ds.number(" 12.5 "), 12.5)

    def test_column_skips_missing_values_and_sorts(self) -> None:
        rows = [{"x": "3"}, {"x": ""}, {"x": "1"}, {"x": "2"}]
        self.assertEqual(ds.column(rows, "x"), [1, 2, 3])


class RenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def rows(self, data: list[list[str]]) -> list[dict[str, str]]:
        path = self.dir / "repos.tsv"
        path.write_text(tsv(data), encoding="utf-8")
        return ds.load(path)

    def test_only_ranked_repositories_are_described(self) -> None:
        rows = self.rows([row("a/a", stars="100"), row("b/b", stars="300"),
                          row("q/q", table="quiet", stars="99999")])
        text = ds.render("snap", rows)
        self.assertIn("3 repositories were found; 2 are *ranked*", text)
        self.assertNotIn("99,999", text)

    def test_flagged_repository_is_listed_with_its_percentile_rank(self) -> None:
        rows = self.rows([row("a/a", stars="100"), row("b/b", stars="200"),
                          row("hot/repo", stars="900", spd="600", flags="fast-growth")])
        text = ds.render("snap", rows)
        line = next(ln for ln in text.splitlines() if ln.startswith("| hot/repo"))
        self.assertIn("900 (p100)", line)
        self.assertIn("600 (p100)", line)

    def test_missing_contributors_leave_a_blank_cell(self) -> None:
        rows = self.rows([row("a/a"), row("hot/repo", flags="fast-growth", contrib="")])
        line = next(ln for ln in ds.render("snap", rows).splitlines() if ln.startswith("| hot/repo"))
        cells = [c.strip() for c in line.strip("|").split("|")]
        self.assertEqual(cells[2 + 4], "")  # name, category, then stars, spd, forks, issues, contributors

    def test_report_states_it_is_a_description_and_concludes_nothing(self) -> None:
        text = ds.render("snap", self.rows([row()]))
        self.assertIn("This is a description, not a test", text)
        self.assertIn("Nothing below can tell organic growth from inflated growth", text)
        self.assertIn("nothing is concluded about any repository", text)


class MainTests(unittest.TestCase):
    def test_missing_snapshot_exits_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(ds.main(["--snapshot", str(Path(tmp) / "nope"), "--out", str(Path(tmp) / "o.md")]), 2)

    def test_writes_the_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            snap = Path(tmp) / "20260101_0000-github"
            snap.mkdir()
            (snap / "repos.tsv").write_text(tsv([row("a/a")]), encoding="utf-8")
            out = Path(tmp) / "report.md"
            self.assertEqual(ds.main(["--snapshot", str(snap), "--out", str(out)]), 0)
            self.assertIn("X1: Describing the snapshot", out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
