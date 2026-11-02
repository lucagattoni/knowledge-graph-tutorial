"""Tests for docs-site/mkdocs_hooks.py. Run: uv run python -m unittest discover -s docs-site"""

from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).parent))

import mkdocs_hooks as hooks  # noqa: E402
import stage_docs as sd  # noqa: E402

REPO_URL = "https://github.com/o/r"


def write(root: Path, rel: str, text: str = "") -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def page(title: str, **meta: object) -> str:
    front = "".join(f"{k}: {v}\n" for k, v in meta.items())
    return (f"---\n{front}---\n\n" if front else "") + f"# {title}\n"


class SlugTest(unittest.TestCase):
    def test_em_dash_keeps_both_hyphens(self):
        self.assertEqual(hooks._github_slugify("The manifest — pinakes.toml", "-"), "the-manifest--pinakestoml")

    def test_angle_bracketed_code_span_keeps_its_word(self):
        self.assertEqual(hooks._github_slugify("The sidecar — `<file>.pnk.yaml`", "-"), "the-sidecar--filepnkyaml")


class RewriteLinksTest(unittest.TestCase):
    """A repository as it is on disk, staged by the real plan(): docs/ without its prefix, the archive as is."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        for rel in (
            "README.md",  # the root README: a GitHub-only pointer
            "docs/README.md",
            "docs/history/README.md",
            "docs/trends/README.md",
            "docs/trends/x.md",
            "docs/projects/lightrag.md",
            "docs/index/rdf.md",
            "kb-kg/README.md",
            "kb-kg/primer/README.md",
            "kb-kg/projects/a.md",
            "kb-kg/projects/b.md",
            "kb-kg/literature/paper.md",  # a folder with pages but no README
            "DECISIONS.md",
            "RESUME.md",
            "tools/gh_snapshot.py",
            "docs/trends/changes.tsv",
            "kb-kg/projects/_TEMPLATE.md",
            "kb-kg/landscape/s/repos.tsv",
        ):
            write(self.repo, rel, "# T\n")
        self.mapping = sd.plan(self.repo)

    def rewrite(self, text: str, src: str = "trends/x.md") -> str:
        return hooks.rewrite_links(text, src, self.repo, REPO_URL, self.mapping)

    def test_staged_paths_differ_from_repository_paths(self):
        self.assertEqual(self.mapping["trends/x.md"], "docs/trends/x.md")
        self.assertEqual(self.mapping["kb-kg/projects/a.md"], "kb-kg/projects/a.md")
        self.assertEqual(self.mapping["README.md"], "docs/README.md")

    def test_link_between_docs_pages_keeps_its_anchor(self):
        self.assertEqual(self.rewrite("[l](../projects/lightrag.md#how)"), "[l](../projects/lightrag.md#how)")
        self.assertEqual(self.rewrite("[r](../index/rdf.md)"), "[r](../index/rdf.md)")

    def test_link_from_docs_to_the_archive_is_resolved_against_the_repository_path(self):
        # From docs/trends/x.md, ../../kb-kg/... is the repository's kb-kg; on the site it is ../kb-kg/...
        self.assertEqual(self.rewrite("[a](../../kb-kg/projects/a.md#n)"), "[a](../kb-kg/projects/a.md#n)")
        self.assertEqual(self.rewrite("[d](../../DECISIONS.md)"), "[d](../DECISIONS.md)")

    def test_link_from_the_archive_to_docs(self):
        self.assertEqual(
            self.rewrite("[x](../../docs/trends/x.md#h)", "kb-kg/projects/a.md"), "[x](../../trends/x.md#h)"
        )

    def test_link_inside_the_archive_still_works(self):
        self.assertEqual(self.rewrite("[b](b.md)", "kb-kg/projects/a.md"), "[b](b.md)")
        self.assertEqual(self.rewrite("[p](../primer/README.md#z)", "kb-kg/projects/a.md"), "[p](../primer/README.md#z)")
        self.assertEqual(self.rewrite("[d](../../DECISIONS.md)", "kb-kg/projects/a.md"), "[d](../../DECISIONS.md)")

    def test_link_from_the_home_page(self):
        self.assertEqual(self.rewrite("[t](trends/x.md)", "README.md"), "[t](trends/x.md)")
        self.assertEqual(self.rewrite("[k](kb-kg/README.md)", "README.md"), "[k](kb-kg/README.md)")

    def test_folder_with_a_staged_readme_links_to_that_readme(self):
        self.assertEqual(self.rewrite("[h](../history/)"), "[h](../history/README.md)")
        self.assertEqual(self.rewrite("[h](../history)"), "[h](../history/README.md)")
        self.assertEqual(self.rewrite("[p](../../kb-kg/primer/)", "trends/x.md"), "[p](../kb-kg/primer/README.md)")
        self.assertEqual(self.rewrite("[p](primer/)", "kb-kg/README.md"), "[p](primer/README.md)")

    def test_the_docs_folder_itself_is_the_home_page(self):
        self.assertEqual(self.rewrite("[h](../../docs/)"), "[h](../README.md)")

    def test_folder_without_a_staged_readme_goes_to_github(self):
        self.assertEqual(
            self.rewrite("[l](literature/)", "kb-kg/README.md"), f"[l]({REPO_URL}/tree/main/kb-kg/literature)"
        )

    def test_unstaged_repository_files_go_to_github_with_their_anchor(self):
        self.assertEqual(self.rewrite("[r](../../RESUME.md#now)"), f"[r]({REPO_URL}/blob/main/RESUME.md#now)")
        self.assertEqual(
            self.rewrite("[t](../../tools/gh_snapshot.py)"), f"[t]({REPO_URL}/blob/main/tools/gh_snapshot.py)"
        )
        self.assertEqual(self.rewrite("[c](changes.tsv)"), f"[c]({REPO_URL}/blob/main/docs/trends/changes.tsv)")
        self.assertEqual(
            self.rewrite("[d](landscape/s/repos.tsv)", "kb-kg/README.md"),
            f"[d]({REPO_URL}/blob/main/kb-kg/landscape/s/repos.tsv)",
        )
        self.assertEqual(
            self.rewrite("[t](_TEMPLATE.md)", "kb-kg/projects/a.md"),
            f"[t]({REPO_URL}/blob/main/kb-kg/projects/_TEMPLATE.md)",
        )

    def test_the_root_readme_is_not_the_home_page_so_it_goes_to_github(self):
        # docs/README.md is staged as README.md, but ../../README.md from docs/trends/x.md is the root one.
        self.assertEqual(self.rewrite("[r](../../README.md)"), f"[r]({REPO_URL}/blob/main/README.md)")
        self.assertEqual(self.rewrite("[r](../README.md)", "README.md"), f"[r]({REPO_URL}/blob/main/README.md)")

    def test_missing_target_is_left_for_mkdocs_to_report(self):
        self.assertEqual(self.rewrite("[x](nowhere.md)"), "[x](nowhere.md)")
        self.assertEqual(self.rewrite("[x](../../../outside.md)"), "[x](../../../outside.md)")
        self.assertEqual(self.rewrite("[x](../../)"), "[x](../../)")  # the repository root

    def test_template_placeholder_links_to_the_folder_that_holds_such_files(self):
        self.assertEqual(  # docs/projects has no README in this fixture
            self.rewrite("[e](../projects/<slug>.md)"), f"[e]({REPO_URL}/tree/main/docs/projects)"
        )
        self.assertEqual(self.rewrite("[e](primer/<slug>.md)", "kb-kg/README.md"), "[e](primer/README.md)")
        self.assertEqual(self.rewrite("[e](primer/x-<slug>.md)", "kb-kg/README.md"), "[e](primer/README.md)")
        self.assertEqual(self.rewrite("[e](<slug>.md)"), "[e](<slug>.md)")

    def test_external_anchor_and_absolute_links_are_untouched(self):
        for link in ("[x](https://example.org/a)", "[x](mailto:a@b.c)", "[x](#here)", "[x](/abs)"):
            self.assertEqual(self.rewrite(link), link)

    def test_code_is_not_rewritten(self):
        text = "`[x](../history/)` and\n```\n[x](../history/)\n```\n~~~\n[x](../history/)\n~~~\n[x](../history/)"
        self.assertEqual(self.rewrite(text), text.rsplit("\n", 1)[0] + "\n[x](../history/README.md)")

    def test_longer_fence_is_not_closed_by_a_shorter_one(self):
        text = "````\n```\n[x](../history/)\n```\n````"
        self.assertEqual(self.rewrite(text), text)

    def test_reference_definition_and_angle_target(self):
        self.assertEqual(self.rewrite("[r]: ../history/"), "[r]: ../history/README.md")
        self.assertEqual(self.rewrite("[p](<../history/>)"), "[p](<../history/README.md>)")

    def test_two_links_on_one_line_and_a_title(self):
        self.assertEqual(
            self.rewrite('[a](../history/) and [b](../history/ "T")'),
            '[a](../history/README.md) and [b](../history/README.md "T")',
        )


class NavTest(unittest.TestCase):
    """The nav of a staged tree: chapters, Index and Archive."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        r = self.root
        write(r, "README.md", page("Welcome", type="chapter"))
        # Chapters 1 (History), 2 (Trends), 3 (Projects) and 5 (Datasets) exist; 4 (Papers) does not.
        write(r, "history/README.md", page("How it evolved"))
        write(r, "history/late.md", page("Late era", order=2))
        write(r, "history/early.md", page("Early era", order=1))
        write(r, "trends/README.md", page("Trends overview"))
        write(r, "trends/zeta.md", page("Zeta"))  # no order: after the ordered pages
        write(r, "trends/alpha.md", page("Alpha"))
        write(r, "trends/ten.md", page("Ten", order=10))
        write(r, "trends/nine.md", page("Nine", order=9))  # 9 before 10, not "10" before "9"
        write(r, "trends/tie-b.md", page("Beta", order=3))
        write(r, "trends/tie-a.md", page("Able", order=3))  # same order: by title
        write(r, "projects/README.md", page("The projects"))
        write(r, "projects/lightrag.md", page("`LightRAG`"))
        write(r, "datasets/README.md", page("Datasets landing"))
        write(r, "datasets/d.md", page("D"))
        write(r, "index/README.md", page("A to Z"))
        write(r, "index/rdf.md", page("RDF"))
        write(r, "index/agent.md", page("Agent"))
        write(r, "index/20-newsgroups.md", page("20 Newsgroups"))
        write(r, "kb-kg/README.md", page("KB"))
        write(r, "kb-kg/primer/README.md", page("Before LLMs"))
        write(r, "kb-kg/projects/README.md", page("Project entries"))
        write(r, "kb-kg/projects/b.md", page("`Bee`", slug="b"))
        write(r, "kb-kg/projects/a.md", page("Ay"))
        write(r, "kb-kg/projects/_TEMPLATE.md", page("Template"))
        write(r, "kb-kg/zzz/note.md", page("A note"))
        write(r, "pinakes/README.md", page("Pinakes development notes"))
        write(r, "pinakes/takeaways/x.md", page("X"))
        write(r, "DECISIONS.md", page("Decisions log"))
        write(r, "stylesheets/skip.css")  # assets beside the pages are not chapters
        self.nav = hooks.build_nav(r)

    @staticmethod
    def labels(entries: list) -> list[str]:
        return [next(iter(e)) if isinstance(e, dict) else e for e in entries]

    def section(self, label: str) -> list:
        return next(e[label] for e in self.nav if label in e)

    def test_tabs_in_order_home_chapters_index_archive_with_fixed_chapter_numbers(self):
        self.assertEqual(
            self.labels(self.nav), ["Home", "1. History", "2. Trends", "3. Projects", "5. Datasets", "Index", "Archive"]
        )
        self.assertEqual(self.nav[0], {"Home": "README.md"})

    def test_chapter_pages_follow_front_matter_order_then_title(self):
        trends = self.section("2. Trends")
        self.assertEqual(trends[0], "trends/README.md")
        self.assertEqual(
            self.labels(trends[1:]),
            ["2.1 Able", "2.2 Beta", "2.3 Nine", "2.4 Ten", "2.5 Alpha", "2.6 Zeta"],
        )
        self.assertEqual(self.labels(self.section("1. History")[1:]), ["1.1 Early era", "1.2 Late era"])

    def test_chapter_page_titles_come_from_the_h1_after_the_front_matter(self):
        self.assertEqual(self.section("3. Projects")[1], {"3.1 LightRAG": "projects/lightrag.md"})

    def test_a_missing_chapter_folder_is_skipped_without_renumbering(self):
        self.assertNotIn("4. Papers", self.labels(self.nav))
        self.assertIn("5. Datasets", self.labels(self.nav))

    def test_a_non_integer_order_is_an_error(self):
        write(self.root, "trends/bad.md", page("Bad", order="soon"))
        with self.assertRaises(ValueError):
            hooks.build_nav(self.root)

    def test_index_is_unnumbered_readme_first_then_entries_by_title(self):
        index = self.section("Index")
        self.assertEqual(index[0], "index/README.md")
        self.assertEqual(self.labels(index[1:]), ["20 Newsgroups", "Agent", "RDF"])

    def test_archive_is_unnumbered_and_keeps_the_old_labels_and_order(self):
        archive = self.section("Archive")
        self.assertEqual(self.labels(archive), ["KB/KG reference", "Pinakes notes", "Decisions"])
        kb = archive[0]["KB/KG reference"]
        self.assertEqual(kb[0], "kb-kg/README.md")
        self.assertEqual(self.labels(kb[1:]), ["Primer", "Projects", "Zzz"])
        self.assertEqual(archive[2], {"Decisions": "DECISIONS.md"})

    def test_archive_pages_below_a_section_take_their_h1_and_the_template_goes_last(self):
        projects = self.section("Archive")[0]["KB/KG reference"][2]["Projects"]
        self.assertEqual(projects[0], "kb-kg/projects/README.md")
        self.assertEqual(self.labels(projects[1:]), ["Ay", "Bee", "Template"])

    def test_archive_section_without_index_takes_its_directory_name(self):
        pinakes = self.section("Archive")[1]["Pinakes notes"]
        self.assertEqual(pinakes[1], {"Takeaways": [{"X": "pinakes/takeaways/x.md"}]})

    def test_without_docs_the_nav_is_home_and_archive(self):
        root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(root))
        write(root, "README.md", page("Home"))
        write(root, "DECISIONS.md", page("D"))
        write(root, "kb-kg/README.md", page("KB"))
        self.assertEqual(self.labels(hooks.build_nav(root)), ["Home", "Archive"])

    def test_only_chapter_and_page_labels_carry_a_number(self):
        def numbered(entries, found):
            for e in entries:
                if isinstance(e, dict):
                    (label, value), = e.items()
                    if re.match(r"\d+\.", label):
                        found.append(label)
                    if isinstance(value, list):
                        numbered(value, found)
            return found

        for tab in ("Index", "Archive", "Home"):
            self.assertEqual(numbered([e for e in self.nav if tab in e], []), [], tab)
        self.assertEqual(len(numbered([e for e in self.nav if re.match(r"\d+\.", next(iter(e)))], [])), 4 + 2 + 6 + 1 + 1)  # chapters, then their pages


class HookEventsTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        write(self.repo, "docs/README.md", page("Home"))
        write(self.repo, "docs/trends/x.md", page("X"))
        write(self.repo, "kb-kg/projects/a.md", page("A"))
        write(self.repo, "docs-site/stylesheets/s.css")
        write(self.repo, "docs-site/javascripts/j.js")
        self.out = self.repo / "docs-src"
        sd.stage(self.repo, self.out)
        self.addCleanup(hooks._MAPPING.clear)

    def config(self) -> dict:
        return {"docs_dir": str(self.out), "mdx_configs": {}, "repo_url": REPO_URL, "edit_uri": "edit/main/"}

    def test_on_config_loads_the_mapping_installs_the_slugifier_and_sets_the_nav(self):
        config = hooks.on_config(self.config())
        self.assertEqual(config["mdx_configs"]["toc"]["slugify"], hooks._github_slugify)
        self.assertEqual(config["nav"][0], {"Home": "README.md"})
        self.assertEqual(hooks._MAPPING["trends/x.md"], "docs/trends/x.md")

    def test_on_config_without_the_mapping_file_says_to_stage_first(self):
        (self.out / hooks.MAP_NAME).unlink()
        with self.assertRaises(FileNotFoundError) as raised:
            hooks.on_config(self.config())
        self.assertIn("stage_docs.py", str(raised.exception))

    def test_edit_link_points_at_the_repository_path_not_the_staged_one(self):
        self.assertEqual(
            hooks.edit_url(REPO_URL, "edit/main/", "docs/trends/x.md"), f"{REPO_URL}/edit/main/docs/trends/x.md"
        )
        hooks.on_config(self.config())
        for src, expected in (
            ("trends/x.md", "docs/trends/x.md"),
            ("README.md", "docs/README.md"),
            ("kb-kg/projects/a.md", "kb-kg/projects/a.md"),
        ):
            p = SimpleNamespace(file=SimpleNamespace(src_uri=src), edit_url="staged-default")
            hooks.on_page_context({}, p, self.config(), None)
            self.assertEqual(p.edit_url, f"{REPO_URL}/edit/main/{expected}", src)

    def test_edit_link_is_left_alone_when_the_site_has_no_edit_uri(self):
        hooks.on_config(self.config())
        p = SimpleNamespace(file=SimpleNamespace(src_uri="trends/x.md"), edit_url=None)
        config = self.config() | {"edit_uri": ""}
        hooks.on_page_context({}, p, config, None)
        self.assertIsNone(p.edit_url)


if __name__ == "__main__":
    unittest.main()
