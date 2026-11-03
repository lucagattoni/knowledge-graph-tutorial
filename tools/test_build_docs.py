"""Tests for tools/build_docs.py. Run: uv run python -m unittest tools/test_build_docs.py"""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import build_docs as bd  # noqa: E402

AI_BEGIN, AI_END = "<!-- BEGIN GENERATED: appears-in -->", "<!-- END GENERATED: appears-in -->"
SNAP = "20261030_1954-github"
SNAP_HEADER = "full_name\tcategory\tstars\tpushed_at\tlicense\tflags\n"


def page(ptype: str, title: str | None, body: str = "", **meta: str) -> str:
    fm = "".join(f"{k}: {v}\n" for k, v in {"type": ptype, "updated": "20261102 12:00 UTC", **meta}.items())
    head = f"# {title}\n\n" if title is not None else ""
    return f"---\n{fm}---\n\n{head}{body}"


def with_appears(text: str) -> str:
    return text.rstrip("\n") + f"\n\n## Appears in\n\n{AI_BEGIN}\n{AI_END}\n"


def project(title: str, body: str = "", repo: str = "o/r") -> str:
    return with_appears(page("project", title, body, repo=repo, trends="[]"))


def index_entry(title: str, body: str = "", kind: str = "concept", aliases: str = "[]") -> str:
    return with_appears(page("index", title, body, kind=kind, aliases=aliases))


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "docs").mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def put(self, rel: str, text: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def doc(self, rel: str) -> str:
        return (self.root / "docs" / rel).read_bytes().decode("utf-8")

    def run_main(self, *extra: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = bd.main(["--root", str(self.root), *extra])
        return code, out.getvalue(), err.getvalue()

    def generate(self) -> None:
        code, _, err = self.run_main()
        self.assertEqual(code, 0, err)

    def section(self, rel: str, name: str) -> str:
        text = self.doc(rel)
        a = text.index(f"<!-- BEGIN GENERATED: {name} -->")
        b = text.index(f"<!-- END GENERATED: {name} -->")
        return text[a:b].split("\n", 1)[1].strip("\n")

    def snapshot(self, rows: list[str], name: str = SNAP) -> None:
        self.put(f"kb-kg/landscape/{name}/repos.tsv", SNAP_HEADER + "".join(r + "\n" for r in rows))


class FrontMatterTests(Fixture):
    def problems(self) -> list[str]:
        with self.assertRaises(bd.InputProblem) as cm:
            bd.load_pages(self.root / "docs")
        return cm.exception.problems

    def test_scalar_and_list_forms(self) -> None:
        self.put("docs/a.md", "---\ntype: page\nshift: A -> B\ntrends: [x, y ,z]\nempty: []\n---\n\n# A\n")
        (p,) = bd.load_pages(self.root / "docs")
        self.assertEqual(p.meta["shift"], "A -> B")
        self.assertEqual(p.meta["trends"], ["x", "y", "z"])
        self.assertEqual(p.meta["empty"], [])
        self.assertEqual(p.title, "A")

    def test_page_without_front_matter_is_invalid(self) -> None:
        self.put("docs/a.md", "# A\n")
        self.assertIn("docs/a.md: no front matter", self.problems())

    def test_page_without_type_is_invalid(self) -> None:
        self.put("docs/a.md", "---\nupdated: x\n---\n# A\n")
        self.assertTrue(any("no 'type'" in p for p in self.problems()))

    def test_unclosed_block_nested_yaml_and_bad_list_are_invalid(self) -> None:
        self.put("docs/a.md", "---\ntype: page\n")
        self.put("docs/b.md", "---\ntype: page\nnest:\n  - a\n---\n")
        self.put("docs/c.md", "---\ntype: page\nl: [a, b\n---\n")
        self.put("docs/d.md", "---\ntype: page\ntype: page\n---\n")
        problems = self.problems()
        self.assertEqual(len([p for p in problems if p.startswith("docs/")]), 4, problems)

    def test_all_problems_are_reported_together(self) -> None:
        self.put("docs/a.md", "# A\n")
        self.put("docs/b.md", "# B\n")
        self.assertEqual(len(self.problems()), 2)

    def test_missing_docs_folder_is_invalid(self) -> None:
        with self.assertRaises(bd.InputProblem):
            bd.load_pages(self.root / "nope")


class LinkExtractionTests(Fixture):
    def links(self, body: str) -> list[str]:
        self.put("docs/x.md", page("page", "X", body))
        (p,) = bd.load_pages(self.root / "docs")
        return bd.extract_links(p)

    def test_inline_links_found(self) -> None:
        self.assertEqual(self.links("See [a](a.md) and [b](../b.md#frag) and <![i](c.png)>."), ["a.md", "../b.md#frag", "c.png"])

    def test_fenced_code_ignored(self) -> None:
        body = "```\n[a](a.md)\n```\n\n~~~md\n[b](b.md)\n~~~\n\n[c](c.md)\n"
        self.assertEqual(self.links(body), ["c.md"])

    def test_longer_fence_needs_matching_close(self) -> None:
        body = "````\n```\n[a](a.md)\n```\n````\n[c](c.md)\n"
        self.assertEqual(self.links(body), ["c.md"])

    def test_inline_code_ignored(self) -> None:
        self.assertEqual(self.links("`[a](a.md)` and ``[b](b.md)`` and [c](c.md)"), ["c.md"])

    def test_link_around_code_span_kept(self) -> None:
        self.assertEqual(self.links("[`rdf`](rdf.md)"), ["rdf.md"])

    def test_unmatched_backtick_does_not_swallow_next_paragraph(self) -> None:
        self.assertEqual(self.links("a ` stray\n\n[c](c.md) and `x`"), ["c.md"])

    def test_links_in_generated_sections_ignored(self) -> None:
        body = "<!-- BEGIN GENERATED: changes -->\n[a](a.md)\n<!-- END GENERATED: changes -->\n\n[b](b.md)\n"
        self.put("docs/trends/README.md", page("chapter", "T", body))
        pages = {p.rel: p for p in bd.load_pages(self.root / "docs")}
        self.assertEqual(bd.extract_links(pages["trends/README.md"]), ["b.md"])

    def test_markers_inside_a_fence_are_examples(self) -> None:
        body = "```\n<!-- BEGIN GENERATED: appears-in -->\n```\n\n[b](b.md)\n"
        self.put("docs/x.md", page("page", "X", body))
        (p,) = bd.load_pages(self.root / "docs")
        self.assertEqual(p.sections, [])
        self.assertEqual(bd.extract_links(p), ["b.md"])


class ResolveTests(Fixture):
    def resolve(self, from_rel: str, target: str, known: list[str]) -> str | None:
        p = bd.Page(rel=from_rel, lines=[])
        return bd.resolve_link(p, target, set(known))

    def test_relative_same_folder_and_parent(self) -> None:
        known = ["index/rdf.md", "trends/x.md"]
        self.assertEqual(self.resolve("index/a.md", "rdf.md", known), "index/rdf.md")
        self.assertEqual(self.resolve("trends/x.md", "../index/rdf.md", known), "index/rdf.md")
        self.assertEqual(self.resolve("trends/x.md", "./../index/rdf.md", known), "index/rdf.md")

    def test_anchor_and_query_stripped(self) -> None:
        self.assertEqual(self.resolve("trends/x.md", "../index/rdf.md#def", ["index/rdf.md"]), "index/rdf.md")
        self.assertEqual(self.resolve("a.md", "index/rdf.md?x=1", ["index/rdf.md"]), "index/rdf.md")

    def test_external_anchor_only_absolute_and_outside_are_none(self) -> None:
        known = ["index/rdf.md", "a.md"]
        for t in ("https://x.org/a.md", "mailto:a@b.c", "#top", "/index/rdf.md", "../../kb-kg/x.md", ""):
            self.assertIsNone(self.resolve("trends/x.md", t, known), t)

    def test_unknown_target_and_folder_link(self) -> None:
        self.assertIsNone(self.resolve("a.md", "missing.md", ["a.md"]))
        self.assertEqual(self.resolve("a.md", "index/", ["index/README.md"]), "index/README.md")

    def test_percent_encoding(self) -> None:
        self.assertEqual(self.resolve("a.md", "my%20page.md", ["my page.md"]), "my page.md")


class AppearsInTests(Fixture):
    def setUp(self) -> None:
        super().setUp()
        self.put("docs/README.md", page("page", "Home", "Start with [RDF](index/rdf.md) and [Lightrag](projects/lightrag.md).\n"))
        self.put("docs/index/rdf.md", index_entry("RDF", "Related: [Lightrag](../projects/lightrag.md)."))
        self.put("docs/projects/lightrag.md", project("LightRAG"))
        self.put("docs/trends/b-trend.md", page("trend", "Zeta trend", "Uses [rdf](../index/rdf.md#x) and [L](../projects/lightrag.md)."))
        self.put("docs/trends/a-trend.md", page("trend", "Alpha trend", "Uses [rdf](../index/rdf.md)."))
        self.put("docs/history/era.md", page("era", "An era", "[rdf](../index/rdf.md)"))
        self.put("docs/applied-to-pinakes/p.md", page("page", "Pinakes use", "[l](../projects/lightrag.md)"))

    def test_groups_in_chapter_order_sorted_by_title(self) -> None:
        self.generate()
        expected = "\n".join(
            [
                "**Home**",
                "",
                "- [Home](../README.md)",
                "",
                "**History**",
                "",
                "- [An era](../history/era.md)",
                "",
                "**Trends**",
                "",
                "- [Alpha trend](../trends/a-trend.md)",
                "- [Zeta trend](../trends/b-trend.md)",
            ]
        )
        self.assertEqual(self.section("index/rdf.md", "appears-in"), expected)

    def test_project_page_lists_its_inbound_links_relative_to_itself(self) -> None:
        self.generate()
        got = self.section("projects/lightrag.md", "appears-in")
        self.assertIn("- [Home](../README.md)", got)
        self.assertIn("- [RDF](../index/rdf.md)", got)
        self.assertIn("**Applied to Pinakes**\n\n- [Pinakes use](../applied-to-pinakes/p.md)", got)
        self.assertLess(got.index("**Home**"), got.index("**Trends**"))
        self.assertLess(got.index("**Trends**"), got.index("**Applied to Pinakes**"))
        self.assertLess(got.index("**Applied to Pinakes**"), got.index("**Index**"))

    def test_chapter_order_is_the_documented_one(self) -> None:
        labels = [label for label, _ in bd.CHAPTERS]
        self.assertEqual(
            labels,
            ["Home", "History", "Trends", "Projects", "Papers", "Datasets", "Benchmarks", "Experiments", "Applied to Pinakes", "Index"],
        )

    def test_no_inbound_link(self) -> None:
        self.put("docs/index/lonely.md", index_entry("Lonely"))
        self.generate()
        self.assertEqual(self.section("index/lonely.md", "appears-in"), "No page links here yet.")

    def test_page_does_not_list_itself(self) -> None:
        self.put("docs/index/self.md", index_entry("Self", "See [me](self.md) and [me again](./self.md#a)."))
        self.generate()
        self.assertEqual(self.section("index/self.md", "appears-in"), "No page links here yet.")

    def test_one_page_linking_twice_is_listed_once(self) -> None:
        self.put("docs/index/twice.md", index_entry("Twice"))
        self.put("docs/trends/c.md", page("trend", "C", "[a](../index/twice.md) [b](../index/twice.md#x)"))
        self.generate()
        self.assertEqual(self.section("index/twice.md", "appears-in").count("- [C]"), 1)

    def test_links_in_code_do_not_count(self) -> None:
        self.put("docs/index/hidden.md", index_entry("Hidden"))
        self.put("docs/trends/c.md", page("trend", "C", "`[a](../index/hidden.md)`\n\n```\n[a](../index/hidden.md)\n```\n"))
        self.generate()
        self.assertEqual(self.section("index/hidden.md", "appears-in"), "No page links here yet.")

    def test_generated_sections_never_count_as_links(self) -> None:
        # The A to Z page links to every entry inside its generated section; it must not appear in any list.
        self.put("docs/index/README.md", page("chapter", "Index", "<!-- BEGIN GENERATED: a-z -->\n<!-- END GENERATED: a-z -->\n"))
        self.generate()
        self.assertNotIn("[Index]", self.section("index/rdf.md", "appears-in"))
        self.assertNotIn("[Index]", self.section("projects/lightrag.md", "appears-in"))
        # And the lists do not feed each other: RDF links to LightRAG by hand, LightRAG's list must show RDF once.
        self.assertEqual(self.section("projects/lightrag.md", "appears-in").count("- [RDF]"), 1)

    def test_target_without_markers_is_invalid(self) -> None:
        self.put("docs/index/bare.md", page("index", "Bare", kind="concept", aliases="[]"))
        self.put("docs/projects/bare.md", page("project", "Bare P", repo="a/b"))
        code, _, err = self.run_main()
        self.assertEqual(code, 2)
        self.assertIn("docs/index/bare.md: lacks the appears-in markers", err)
        self.assertIn("docs/projects/bare.md: lacks the appears-in markers", err)

    def test_readme_of_index_and_projects_needs_no_appears_in(self) -> None:
        self.put("docs/index/README.md", page("chapter", "Index"))
        self.put("docs/projects/README.md", page("chapter", "Projects"))
        code, _, err = self.run_main("--check")
        self.assertNotEqual(code, 2, err)

    def test_appears_in_on_an_ordinary_page_is_invalid(self) -> None:
        self.put("docs/trends/c.md", with_appears(page("trend", "C")))
        code, _, err = self.run_main()
        self.assertEqual(code, 2)
        self.assertIn("not allowed on this page", err)

    def test_listing_page_without_title_is_invalid(self) -> None:
        self.put("docs/trends/c.md", page("trend", None, "[a](../index/rdf.md)"))
        code, _, err = self.run_main()
        self.assertEqual(code, 2)
        self.assertIn("docs/trends/c.md: no top-level", err)


class MarkerValidationTests(Fixture):
    def test_unterminated_unknown_and_mismatched_markers_are_invalid(self) -> None:
        self.put("docs/a.md", page("page", "A", "<!-- BEGIN GENERATED: changes -->\n"))
        self.put("docs/b.md", page("page", "B", "<!-- BEGIN GENERATED: nope -->\n<!-- END GENERATED: nope -->\n"))
        self.put("docs/c.md", page("page", "C", "<!-- END GENERATED: changes -->\n"))
        self.put("docs/d.md", page("page", "D", "<!--BEGIN GENERATED: changes-->\n"))
        code, _, err = self.run_main()
        self.assertEqual(code, 2)
        for name in ("docs/a.md", "docs/b.md", "docs/c.md", "docs/d.md"):
            self.assertIn(name, err)

    def test_section_on_the_wrong_page_is_invalid(self) -> None:
        self.put("docs/trends/x.md", page("trend", "X", "<!-- BEGIN GENERATED: changes -->\n<!-- END GENERATED: changes -->\n"))
        self.put("docs/other/README.md", page("chapter", "O", "<!-- BEGIN GENERATED: a-z -->\n<!-- END GENERATED: a-z -->\n"))
        code, _, err = self.run_main()
        self.assertEqual(code, 2)
        self.assertIn("docs/trends/x.md", err)
        self.assertIn("docs/other/README.md", err)

    def test_missing_optional_markers_only_warn(self) -> None:
        self.put("docs/trends/README.md", page("chapter", "Trends"))
        code, _, err = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("warning", err)
        self.assertIn("docs/trends/README.md", err)


class AzTests(Fixture):
    def az_readme(self) -> None:
        self.put("docs/index/README.md", page("chapter", "Index", "Intro.\n\n<!-- BEGIN GENERATED: a-z -->\n<!-- END GENERATED: a-z -->\n\nOutro.\n"))

    def test_letters_sorting_kinds_aliases_and_symbols(self) -> None:
        self.az_readme()
        self.put("docs/index/sparql.md", index_entry("SPARQL", kind="standard", aliases="[SPARQL Protocol]"))
        self.put("docs/index/owl.md", index_entry("OWL", kind="standard", aliases="[Web Ontology Language]"))
        self.put("docs/index/bm25.md", index_entry("BM25", kind="concept"))
        self.put("docs/index/cyc.md", index_entry("Cyc", kind="system", aliases="[]"))
        self.put("docs/index/a1.md", index_entry("3D graph", kind="concept"))
        self.put("docs/index/eclair.md", index_entry("Éclair", kind="concept"))
        self.put("docs/projects/lightrag.md", project("LightRAG"))
        self.put("docs/projects/mem0.md", project("mem0", repo="mem0ai/mem0"))
        self.generate()
        expected = "\n".join(
            [
                "### 0-9 and symbols",
                "",
                "- [3D graph](a1.md) : concept",
                "",
                "### B",
                "",
                "- [BM25](bm25.md) : concept",
                "",
                "### C",
                "",
                "- [Cyc](cyc.md) : system",
                "",
                "### E",
                "",
                "- [Éclair](eclair.md) : concept",
                "",
                "### L",
                "",
                "- [LightRAG](../projects/lightrag.md) : project",
                "",
                "### M",
                "",
                "- [mem0](../projects/mem0.md) : project",
                "",
                "### O",
                "",
                "- [OWL](owl.md) : standard",
                "",
                "### S",
                "",
                "- [SPARQL](sparql.md) : standard",
                "- SPARQL Protocol, see [SPARQL](sparql.md)",
                "",
                "### W",
                "",
                "- Web Ontology Language, see [OWL](owl.md)",
            ]
        )
        self.assertEqual(self.section("index/README.md", "a-z"), expected)
        self.assertTrue(self.doc("index/README.md").startswith("---\ntype: chapter"))
        self.assertTrue(self.doc("index/README.md").endswith("\nOutro.\n"))

    def test_sorting_is_case_insensitive(self) -> None:
        self.az_readme()
        self.put("docs/index/a.md", index_entry("alpha"))
        self.put("docs/index/b.md", index_entry("Beta"))
        self.put("docs/index/c.md", index_entry("Alps"))
        self.generate()
        got = self.section("index/README.md", "a-z")
        self.assertLess(got.index("alpha"), got.index("Alps"))
        self.assertLess(got.index("Alps"), got.index("Beta"))
        self.assertEqual(got.count("### A"), 1)

    def test_duplicate_titles_are_invalid(self) -> None:
        self.az_readme()
        self.put("docs/index/a.md", index_entry("RDF"))
        self.put("docs/projects/b.md", project("rdf"))
        code, _, err = self.run_main()
        self.assertEqual(code, 2)
        self.assertIn("title", err)

    def test_alias_equal_to_another_title_is_invalid(self) -> None:
        self.az_readme()
        self.put("docs/index/a.md", index_entry("Web Ontology Language"))
        self.put("docs/index/b.md", index_entry("OWL", aliases="[web ontology language]"))
        code, _, err = self.run_main()
        self.assertEqual(code, 2)
        self.assertIn("alias", err)

    def test_duplicate_alias_across_entries_is_invalid(self) -> None:
        self.az_readme()
        self.put("docs/index/a.md", index_entry("A one", aliases="[Same]"))
        self.put("docs/index/b.md", index_entry("B one", aliases="[Same]"))
        code, _, err = self.run_main()
        self.assertEqual(code, 2)
        self.assertIn("alias", err)

    def test_bad_kind_is_invalid(self) -> None:
        self.az_readme()
        self.put("docs/index/a.md", index_entry("A", kind="gadget"))
        code, _, err = self.run_main()
        self.assertEqual(code, 2)
        self.assertIn("kind", err)

    def test_empty_list(self) -> None:
        self.az_readme()
        self.generate()
        self.assertEqual(self.section("index/README.md", "a-z"), "No entries yet.")


class WatchlistTests(Fixture):
    def setUp(self) -> None:
        super().setUp()
        self.put("docs/projects/README.md", page("chapter", "Projects", "<!-- BEGIN GENERATED: watchlist -->\n<!-- END GENERATED: watchlist -->\n"))
        self.put("docs/projects/lightrag.md", project("LightRAG", repo="HKUDS/LightRAG"))
        self.put("docs/trends/graph-rag.md", page("trend", "GraphRAG: from chunks to graphs"))
        self.put("docs/trends/memory.md", page("trend", "Agent memory"))
        self.now = datetime(2026, 11, 2, 12, 0, tzinfo=timezone.utc)

    def watch(self, rows: list[str]) -> None:
        self.put("docs/projects/watchlist.tsv", "repo\tcategory\ttrends\tnote\n" + "".join(r + "\n" for r in rows))

    def render(self) -> str:
        self.generate()
        return self.section("projects/README.md", "watchlist")

    def test_table_join_links_and_formats(self) -> None:
        self.snapshot(
            [
                "HKUDS/LightRAG\tcore\t40443\t2026-10-29T18:05:03Z\tMIT\t",
                "mem0ai/mem0\tagent-memory\t12000\t2026-10-01T00:00:00Z\tApache-2.0\tfast-growth",
            ]
        )
        self.watch(["hkuds/lightrag\tcore\tgraph-rag, memory\tSimple | fast", "mem0ai/mem0\tagent-memory\tmemory\t"])
        got = self.render()
        lines = got.split("\n")
        self.assertEqual(
            lines[0],
            "Stars, last push, licence (GitHub's detection of the LICENSE file) and flags come from the GitHub snapshot "
            "taken 20261030 19:54 UTC (kb-kg/landscape/20261030_1954-github/). Stars are a signal, not a verdict.",
        )
        self.assertEqual(lines[1], "")
        self.assertEqual(lines[2], "| Project | Category | Trends | Stars | Last push | Licence | Flags | Note |")
        self.assertEqual(lines[3], "|---|---|---|---|---|---|---|---|")
        self.assertEqual(
            lines[4],
            "| [mem0ai/mem0](https://github.com/mem0ai/mem0) | agent-memory | [Agent memory](../trends/memory.md) | 12,000 | 20261001 | Apache-2.0 | fast-growth |  |",
        )
        self.assertEqual(
            lines[5],
            "| [LightRAG](lightrag.md) | core | [GraphRAG: from chunks to graphs](../trends/graph-rag.md), [Agent memory](../trends/memory.md)"
            " | 40,443 | 20261029 | MIT | none | Simple \\| fast |",
        )

    def test_join_ignores_case_in_both_directions(self) -> None:
        self.snapshot(["Foo/BAR\tcore\t1234\t2026-10-01T00:00:00Z\tMIT\t", "baz/qux\tcore\t99\t2026-10-02T00:00:00Z\tMIT\t"])
        self.watch(["FOO/bar\tcore\t\t", "Baz/Qux\tcore\t\t"])
        got = self.render()
        self.assertIn("| 1,234 | 20261001 |", got)
        self.assertIn("| 99 | 20261002 |", got)
        self.assertNotIn("not in snapshot", got)

    def test_repo_missing_from_snapshot(self) -> None:
        self.snapshot(["x/y\tcore\t1\t2026-10-01T00:00:00Z\tMIT\t"])
        self.watch(["ghost/repo\tcore\t\tnot seen"])
        row = self.render().split("\n")[4]
        self.assertEqual(row, "| [ghost/repo](https://github.com/ghost/repo) | core | none | not in snapshot | n/a | n/a | n/a | not seen |")

    def test_sort_by_category_then_stars_descending(self) -> None:
        self.snapshot(
            [
                "a/low\tz-cat\t5\t2026-10-01T00:00:00Z\tMIT\t",
                "a/high\tz-cat\t5000\t2026-10-01T00:00:00Z\tMIT\t",
                "a/mid\tb-cat\t50\t2026-10-01T00:00:00Z\tMIT\t",
                "a/big\tB-cat\t9999\t2026-10-01T00:00:00Z\tMIT\t",
            ]
        )
        self.watch(["a/low\tz-cat\t\t", "a/high\tz-cat\t\t", "a/mid\tb-cat\t\t", "a/gone\tz-cat\t\t", "a/big\tB-cat\t\t"])
        order = [ln.split("|")[1].strip() for ln in self.render().split("\n")[4:]]
        self.assertEqual(
            order,
            [
                "[a/big](https://github.com/a/big)",
                "[a/mid](https://github.com/a/mid)",
                "[a/high](https://github.com/a/high)",
                "[a/low](https://github.com/a/low)",
                "[a/gone](https://github.com/a/gone)",
            ],
        )

    def test_newest_snapshot_is_chosen_and_folders_without_repos_tsv_are_skipped(self) -> None:
        self.snapshot(["a/b\tcore\t1\t2026-09-01T00:00:00Z\tMIT\t"], name="20260901_0900-github")
        self.snapshot(["a/b\tcore\t2\t2026-10-01T00:00:00Z\tMIT\t"], name="20261030_1954-github")
        (self.root / "kb-kg/landscape/20261101_0000-github").mkdir(parents=True)  # newer but empty
        self.put("kb-kg/landscape/20261101_0100-selection.md", "x")
        self.watch(["a/b\tcore\t\t"])
        got = self.render()
        self.assertIn("20261030 19:54 UTC (kb-kg/landscape/20261030_1954-github/)", got)
        self.assertIn("| 2 |", got)

    def test_unknown_trend_is_invalid(self) -> None:
        self.snapshot(["a/b\tcore\t1\t2026-09-01T00:00:00Z\tMIT\t"])
        self.watch(["a/b\tcore\tno-such-trend\t"])
        code, _, err = self.run_main()
        self.assertEqual(code, 2)
        self.assertIn("no-such-trend", err)

    def test_bad_header_repo_and_duplicates_are_invalid(self) -> None:
        self.snapshot(["a/b\tcore\t1\t2026-09-01T00:00:00Z\tMIT\t"])
        self.put("docs/projects/watchlist.tsv", "repo\tcategory\ttrends\n")
        self.assertEqual(self.run_main()[0], 2)
        self.watch(["not-a-repo\tcore\t\t"])
        self.assertEqual(self.run_main()[0], 2)
        self.watch(["a/b\tcore\t\t", "A/B\tcore\t\t"])
        self.assertEqual(self.run_main()[0], 2)
        self.put("docs/projects/watchlist.tsv", "repo\tcategory\ttrends\tnote\na/b\tcore\n")
        self.assertEqual(self.run_main()[0], 2)

    def test_no_snapshot_with_rows_is_invalid(self) -> None:
        self.watch(["a/b\tcore\t\t"])
        code, _, err = self.run_main()
        self.assertEqual(code, 2)
        self.assertIn("kb-kg/landscape", err)

    def test_missing_or_empty_watchlist(self) -> None:
        self.assertEqual(self.render(), "No watch list yet.")
        self.watch([])
        self.assertEqual(self.render(), "No projects on the watch list yet.")

    def test_stale_snapshot_warns_on_stderr_only(self) -> None:
        self.snapshot(["a/b\tcore\t1\t2026-09-01T00:00:00Z\tMIT\t"], name="20260901_0900-github")
        self.watch(["a/b\tcore\t\t"])
        warnings: list[str] = []
        result = bd.build(self.root, warnings, now=self.now)
        stale = [w for w in warnings if "older than" in w]
        self.assertEqual(len(stale), 1)
        self.assertIn("older than 30 days", stale[0])
        self.assertNotIn("older than", result["docs/projects/README.md"][1])
        fresh: list[str] = []
        bd.build(self.root, fresh, now=datetime(2026, 9, 20, tzinfo=timezone.utc))
        self.assertEqual([w for w in fresh if "older than" in w], [])

    def test_stale_warning_reaches_stderr_from_main(self) -> None:
        self.snapshot(["a/b\tcore\t1\t2026-09-01T00:00:00Z\tMIT\t"], name="20200101_0000-github")
        self.watch(["a/b\tcore\t\t"])
        code, out, err = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("older than 30 days", err)
        self.assertNotIn("older than", out)

    def test_nonnumeric_stars_invalid(self) -> None:
        self.snapshot(["a/b\tcore\tmany\t2026-09-01T00:00:00Z\tMIT\t"])
        self.watch(["a/b\tcore\t\t"])
        self.assertEqual(self.run_main()[0], 2)

    def test_snapshot_descriptions_with_quotes_are_tolerated(self) -> None:
        self.put(
            f"kb-kg/landscape/{SNAP}/repos.tsv",
            "full_name\tcategory\tstars\tpushed_at\tlicense\tflags\tdescription\n"
            'a/b\tcore\t7\t2026-10-01T00:00:00Z\tMIT\t\t"quoted\tstuff\n',
        )
        self.watch(["a/b\tcore\t\t"])
        self.assertIn("| 7 |", self.render())


class ChangesTests(Fixture):
    HEADER = "date_utc\tkind\tsubject\tsummary\tsource\tread_utc\n"

    def setUp(self) -> None:
        super().setUp()
        self.put("docs/trends/README.md", page("chapter", "Trends", "<!-- BEGIN GENERATED: changes -->\n<!-- END GENERATED: changes -->\n"))

    def tsv(self, rows: list[str]) -> None:
        self.put("docs/trends/changes.tsv", self.HEADER + "".join(r + "\n" for r in rows))

    def test_missing_changes_file(self) -> None:
        self.generate()
        self.assertEqual(self.section("trends/README.md", "changes"), "No changes recorded yet.")

    def test_header_only(self) -> None:
        self.tsv([])
        self.generate()
        self.assertEqual(self.section("trends/README.md", "changes"), "No changes recorded yet.")

    def test_newest_first_then_file_order_and_source_link(self) -> None:
        self.tsv(
            [
                "20261001\tadded\tFirst\tone\thttps://example.org/a\t20261002 10:00",
                "20261030\tupdated\tSecond\ttwo\thttps://example.org/b_(x)\t20261030 10:00",
                "20261030\tsettled\tThird\tthree | pipe\tarchive page\t20261030 11:00",
                "20260901\tfaded\tOld\tfour\t\t20261030 11:00",
            ]
        )
        self.generate()
        self.assertEqual(
            self.section("trends/README.md", "changes"),
            "\n".join(
                [
                    "| Date | Kind | Subject | Summary | Source |",
                    "|---|---|---|---|---|",
                    "| 20261030 | updated | Second | two | [source](https://example.org/b_%28x%29) |",
                    "| 20261030 | settled | Third | three \\| pipe | archive page |",
                    "| 20261001 | added | First | one | [source](https://example.org/a) |",
                    "| 20260901 | faded | Old | four |  |",
                    "",
                    "Full list: [changes.tsv](changes.tsv)",
                ]
            ),
        )

    def test_only_fifteen_rows(self) -> None:
        self.tsv([f"202610{d:02d}\tadded\tS{d}\tx\t\t20261030" for d in range(1, 21)])
        self.generate()
        got = self.section("trends/README.md", "changes")
        self.assertEqual(got.count("| added |"), 15)
        self.assertIn("| S20 |", got)
        self.assertIn("| S6 |", got)
        self.assertNotIn("| S5 |", got)

    def test_bad_kind_header_columns_and_date_are_invalid(self) -> None:
        self.tsv(["20261001\tinvented\tS\tx\t\t20261001"])
        self.assertEqual(self.run_main()[0], 2)
        self.put("docs/trends/changes.tsv", "date\tkind\tsubject\tsummary\tsource\tread_utc\n")
        self.assertEqual(self.run_main()[0], 2)
        self.tsv(["20261001\tadded\tS\tx"])
        self.assertEqual(self.run_main()[0], 2)
        self.tsv(["2026-10-01\tadded\tS\tx\t\t20261001"])
        self.assertEqual(self.run_main()[0], 2)

    def test_all_five_chapters_have_their_own_changes(self) -> None:
        for folder in bd.CHANGES_FOLDERS:
            self.put(f"docs/{folder}/README.md", page("chapter", folder.title(), "<!-- BEGIN GENERATED: changes -->\n<!-- END GENERATED: changes -->\n"))
            self.put(f"docs/{folder}/changes.tsv", self.HEADER + f"20261001\tadded\t{folder}-subject\tx\t\t20261001\n")
        self.generate()
        for folder in bd.CHANGES_FOLDERS:
            self.assertIn(f"{folder}-subject", self.section(f"{folder}/README.md", "changes"))


class RunTests(Fixture):
    """Idempotence, --check and exit codes, byte preservation."""

    def populate(self) -> None:
        self.put("docs/README.md", page("page", "Home", "[RDF](index/rdf.md)"))
        self.put("docs/index/README.md", page("chapter", "Index", "<!-- BEGIN GENERATED: a-z -->\n<!-- END GENERATED: a-z -->\n"))
        self.put("docs/index/rdf.md", index_entry("RDF", kind="standard"))
        self.put("docs/trends/README.md", page("chapter", "Trends", "<!-- BEGIN GENERATED: changes -->\n<!-- END GENERATED: changes -->\n"))

    def snapshot_files(self) -> dict[str, bytes]:
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in sorted(self.root.rglob("*")) if p.is_file()}

    def test_second_run_changes_nothing(self) -> None:
        self.populate()
        self.generate()
        first = self.snapshot_files()
        code, out, _ = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("0 written", out)
        self.assertEqual(self.snapshot_files(), first)

    def test_check_does_not_write_and_returns_1_listing_files(self) -> None:
        self.populate()
        before = self.snapshot_files()
        code, _, err = self.run_main("--check")
        self.assertEqual(code, 1)
        self.assertEqual(self.snapshot_files(), before)
        self.assertIn("docs/index/README.md", err)
        self.assertIn("docs/index/rdf.md", err)
        self.assertIn("docs/trends/README.md", err)
        self.assertNotIn("docs/README.md", err)

    def test_check_after_generate_is_0(self) -> None:
        self.populate()
        self.generate()
        self.assertEqual(self.run_main("--check")[0], 0)

    def test_check_detects_a_later_change(self) -> None:
        self.populate()
        self.generate()
        self.put("docs/trends/x.md", page("trend", "X", "[rdf](../index/rdf.md)"))
        code, _, err = self.run_main("--check")
        self.assertEqual(code, 1)
        self.assertIn("docs/index/rdf.md", err)

    def test_hand_edit_inside_a_section_is_overwritten_outside_is_kept(self) -> None:
        self.populate()
        self.generate()
        text = self.doc("index/rdf.md")
        edited = text.replace(AI_END, "handwritten junk\n" + AI_END).replace("## Appears in", "## Appears in\n\nMy own intro.")
        self.put("docs/index/rdf.md", edited)
        self.assertEqual(self.run_main("--check")[0], 1)
        self.generate()
        fixed = self.doc("index/rdf.md")
        self.assertNotIn("handwritten junk", fixed)
        self.assertIn("My own intro.", fixed)

    def test_bytes_outside_markers_are_preserved(self) -> None:
        odd = "---\ntype: index\nkind: concept\naliases: []\n---\n\n# Odd\n\ttab é trailing   \r\n\n\n" + AI_BEGIN + "\nold\n" + AI_END + "\nno newline at end"
        self.put("docs/index/odd.md", odd)
        self.generate()
        new = self.doc("index/odd.md")
        self.assertTrue(new.startswith(odd.split(AI_BEGIN)[0] + AI_BEGIN + "\n"))
        self.assertTrue(new.endswith(AI_END + "\nno newline at end"))
        self.assertIn("\ttab é trailing   \r\n", new)

    def test_invalid_input_exit_2_names_the_file(self) -> None:
        self.populate()
        self.put("docs/broken.md", "# no front matter\n")
        code, _, err = self.run_main()
        self.assertEqual(code, 2)
        self.assertIn("docs/broken.md: no front matter", err)
        self.assertEqual(self.run_main("--check")[0], 2)

    def test_invalid_input_writes_nothing(self) -> None:
        self.populate()
        self.put("docs/broken.md", "# no front matter\n")
        before = self.snapshot_files()
        self.run_main()
        self.assertEqual(self.snapshot_files(), before)

    def test_output_is_deterministic_across_runs_and_page_order(self) -> None:
        self.populate()
        self.put("docs/trends/b.md", page("trend", "Beta", "[rdf](../index/rdf.md)"))
        self.put("docs/trends/a.md", page("trend", "Alpha", "[rdf](../index/rdf.md)"))
        self.generate()
        one = self.section("index/rdf.md", "appears-in")
        self.assertLess(one.index("Alpha"), one.index("Beta"))
        self.assertNotRegex(self.doc("index/README.md"), r"\d{8}_\d{4}-\d{2}")

    def test_missing_docs_folder_exit_2(self) -> None:
        empty = tempfile.TemporaryDirectory()
        self.addCleanup(empty.cleanup)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            self.assertEqual(bd.main(["--root", empty.name]), 2)


if __name__ == "__main__":
    unittest.main()
