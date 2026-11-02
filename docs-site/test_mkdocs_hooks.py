"""Tests for docs-site/mkdocs_hooks.py. Run: uv run python -m unittest discover -s docs-site"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import mkdocs_hooks as hooks  # noqa: E402

REPO_URL = "https://github.com/o/r"


def write(root: Path, rel: str, text: str = "") -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class SlugTest(unittest.TestCase):
    def test_em_dash_keeps_both_hyphens(self):
        self.assertEqual(hooks._github_slugify("The manifest — pinakes.toml", "-"), "the-manifest--pinakestoml")

    def test_angle_bracketed_code_span_keeps_its_word(self):
        self.assertEqual(hooks._github_slugify("The sidecar — `<file>.pnk.yaml`", "-"), "the-sidecar--filepnkyaml")


class RewriteLinksTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        self.docs = self.repo / "docs-src"
        for rel in ("README.md", "kb-kg/README.md", "kb-kg/primer/README.md", "kb-kg/projects/a.md"):
            write(self.docs, rel, "# T\n")
        for root in (self.docs, self.repo):  # a folder with pages but no index, as staging copies it
            write(root, "kb-kg/literature/paper.md", "# T\n")
        write(self.repo, "RESUME.md")
        write(self.repo, "tools/gh_snapshot.py")
        write(self.repo, "kb-kg/landscape/s/repos.tsv")

    def rewrite(self, text: str, src: str = "kb-kg/README.md") -> str:
        return hooks.rewrite_links(text, src, self.docs, self.repo, REPO_URL)

    def test_published_page_is_kept(self):
        self.assertEqual(self.rewrite("[a](projects/a.md#x)"), "[a](projects/a.md#x)")

    def test_folder_with_index_links_to_its_readme(self):
        self.assertEqual(self.rewrite("[p](primer/)"), "[p](primer/README.md)")
        self.assertEqual(self.rewrite("[p](primer)"), "[p](primer/README.md)")

    def test_folder_without_index_goes_to_github(self):
        self.assertEqual(self.rewrite("[l](literature/)"), f"[l]({REPO_URL}/tree/main/kb-kg/literature)")

    def test_unpublished_file_goes_to_github_with_its_anchor(self):
        self.assertEqual(self.rewrite("[r](../RESUME.md#now)"), f"[r]({REPO_URL}/blob/main/RESUME.md#now)")
        self.assertEqual(
            self.rewrite("[t](../../tools/gh_snapshot.py)", "kb-kg/projects/a.md"),
            f"[t]({REPO_URL}/blob/main/tools/gh_snapshot.py)",
        )
        self.assertEqual(
            self.rewrite("[d](landscape/s/repos.tsv)"), f"[d]({REPO_URL}/blob/main/kb-kg/landscape/s/repos.tsv)"
        )

    def test_missing_target_is_left_for_mkdocs_to_report(self):
        self.assertEqual(self.rewrite("[x](nowhere.md)"), "[x](nowhere.md)")
        self.assertEqual(self.rewrite("[x](../../../outside.md)"), "[x](../../../outside.md)")

    def test_template_placeholder_links_to_the_folder_that_holds_such_files(self):
        self.assertEqual(self.rewrite("[e](primer/<slug>.md)"), "[e](primer/README.md)")
        self.assertEqual(self.rewrite("[e](primer/x-<slug>.md)"), "[e](primer/README.md)")
        self.assertEqual(self.rewrite("[e](<slug>.md)"), "[e](<slug>.md)")

    def test_external_anchor_and_absolute_links_are_untouched(self):
        for link in ("[x](https://example.org/a)", "[x](mailto:a@b.c)", "[x](#here)", "[x](/abs)"):
            self.assertEqual(self.rewrite(link), link)

    def test_code_is_not_rewritten(self):
        text = "`[x](primer/)` and\n```\n[x](primer/)\n```\n~~~\n[x](primer/)\n~~~\n[x](primer/)"
        self.assertEqual(self.rewrite(text), text.rsplit("\n", 1)[0] + "\n[x](primer/README.md)")

    def test_longer_fence_is_not_closed_by_a_shorter_one(self):
        text = "````\n```\n[x](primer/)\n```\n````"
        self.assertEqual(self.rewrite(text), text)

    def test_reference_definition_and_angle_target(self):
        self.assertEqual(self.rewrite("[r]: primer/"), "[r]: primer/README.md")
        self.assertEqual(self.rewrite("[p](<primer/>)"), "[p](<primer/README.md>)")

    def test_two_links_on_one_line_and_a_title(self):
        self.assertEqual(
            self.rewrite('[a](primer/) and [b](primer/ "T")'), '[a](primer/README.md) and [b](primer/README.md "T")'
        )


class NavTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        write(self.root, "README.md", "# Home\n")
        write(self.root, "DECISIONS.md", "# Decisions\n")
        write(self.root, "kb-kg/README.md", "# KB\n")
        write(self.root, "kb-kg/primer/README.md", "# Before LLMs\n")
        write(self.root, "kb-kg/projects/README.md", "# Project entries\n")
        write(self.root, "kb-kg/projects/b.md", "---\nslug: b\n---\n\n# `Bee`\n")
        write(self.root, "kb-kg/projects/a.md", "# Ay\n")
        write(self.root, "kb-kg/projects/_TEMPLATE.md", "# Template\n")
        write(self.root, "kb-kg/zzz/note.md", "# A note\n")
        write(self.root, "pinakes/README.md", "# Pinakes development notes\n")
        write(self.root, "pinakes/takeaways/x.md", "# X\n")
        write(self.root, "stylesheets/skip.css")  # assets beside the pages are not chapters

    def test_chapters_are_numbered_in_reading_order_and_assets_skipped(self):
        labels = [next(iter(entry)) for entry in hooks.build_nav(self.root)]
        self.assertEqual(labels, ["Home", "1. KB/KG reference", "2. Pinakes notes", "3. Decisions"])

    def test_index_first_then_listed_sections_then_unlisted_ones(self):
        kb = hooks.build_nav(self.root)[1]["1. KB/KG reference"]
        self.assertEqual(kb[0], "kb-kg/README.md")
        self.assertEqual([next(iter(e)) for e in kb[1:]], ["1.1 Primer", "1.2 Projects", "1.3 Zzz"])

    def test_pages_below_the_numbered_levels_take_their_h1_and_the_template_goes_last(self):
        kb = hooks.build_nav(self.root)[1]["1. KB/KG reference"]
        projects = kb[2]["1.2 Projects"]
        self.assertEqual(projects[0], "kb-kg/projects/README.md")
        self.assertEqual([next(iter(e)) for e in projects[1:]], ["Ay", "Bee", "Template"])

    def test_section_without_index_takes_its_directory_name(self):
        pinakes = hooks.build_nav(self.root)[2]["2. Pinakes notes"]
        self.assertEqual(pinakes[1], {"2.1 Takeaways": [{"X": "pinakes/takeaways/x.md"}]})


if __name__ == "__main__":
    unittest.main()
