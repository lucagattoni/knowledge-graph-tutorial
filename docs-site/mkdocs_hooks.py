"""MkDocs hooks for the documentation site.

The pages are the repository's own Markdown, written to be read on GitHub. The site is a view over
them, never a second copy, so three things that GitHub does for free are done here:

* Heading anchors match GitHub's. Every cross-document anchor was written against GitHub, so the
  site adopts GitHub's slug algorithm rather than the pages being rewritten to match the site.
  Python-Markdown's default drops the em dash *and* collapses the whitespace either side of it
  (``a — b`` becomes ``a-b``, GitHub keeps ``a--b``), and ``pymdownx.slugs.slugify`` strips an
  angle-bracketed code span as if it were an HTML tag.
* The navigation is generated from the staged folder tree, so a page added to the repository
  appears on the site with no edit to ``mkdocs.yml``. Only the order of the sections is written
  down, in ``SECTION_ORDER``.
* Relative links that GitHub resolves but MkDocs does not are rewritten (see ``rewrite_links``):
  a folder link such as ``primer/`` goes to that folder's README, and a link to a file the site
  does not publish (RESUME.md, the snapshot data, ``tools/``) goes to GitHub.

Not type-checked: mkdocs is installed from ``requirements.txt`` into an ephemeral environment and
is not imported here, so the helpers run under plain ``unittest``.
"""

from __future__ import annotations

import posixpath
import re
import unicodedata
from pathlib import Path
from typing import Any

BRANCH = "main"

# Reading order inside a directory, simple to deep. A directory not listed here sorts by name, and an
# entry not listed sorts after the listed ones, so new material shows up without an edit here.
SECTION_ORDER = {
    "": ("kb-kg", "pinakes"),
    "kb-kg": (
        "primer",
        "llm-era",
        "literature",
        "projects",
        "landscape",
        "papers-benchmarks",
        "directions",
        "experiments",
    ),
    "pinakes": ("takeaways", "approach", "precedent", "experiments"),
}

# Short nav titles, keyed by path inside the site. A section not listed takes the H1 of its README, or
# its directory name when it has none.
SECTION_LABELS = {
    "kb-kg": "KB/KG reference",
    "pinakes": "Pinakes notes",
    "kb-kg/primer": "Primer",
    "kb-kg/llm-era": "LLM era",
    "kb-kg/projects": "Projects",
    "kb-kg/papers-benchmarks": "Papers and benchmarks",
    "kb-kg/directions": "Directions",
    "kb-kg/experiments": "Experiments",
    "pinakes/experiments": "Measured",
}

# The nav numbers the top-level sections and the sections inside them ("1.", "1.1"); deeper pages (one
# per project) stay unnumbered. Only the nav: many pages number their own headings, so the site does
# not number those again.
NUMBERED_DEPTH = 2

_INDEX_NAMES = ("README.md", "index.md")
_DISCARDED = re.compile(r"[^\w\s-]", re.UNICODE)
_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_INLINE = re.compile(r"(?P<code>`+[^`\n]*`+)|\]\((?P<target><[^>\s]*>|[^)\s]*)")
_REFDEF = re.compile(r"^( {0,3}\[[^\]]+\]:[ \t]+)(\S+)")


def _github_slugify(text: str, separator: str) -> str:
    """GitHub's heading-anchor algorithm: strip, lowercase, drop punctuation, spaces to hyphens.

    Whitespace is *not* collapsed: ``a — b`` keeps the two spaces the dropped em dash leaves behind
    and yields ``a--b``, which is what GitHub links against.
    """
    text = unicodedata.normalize("NFC", text).strip().lower()
    return _DISCARDED.sub("", text).replace(" ", separator)


def _title(path: Path) -> str:
    """The page's first H1, or its file name when it has none. YAML front matter is skipped."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if lines and lines[0] == "---":
        end = next((i for i, line in enumerate(lines[1:], 1) if line == "---"), 0)
        lines = lines[end + 1 :]
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip().replace("`", "").replace("**", "")
    return path.stem


def _index_of(directory: Path) -> str | None:
    return next((n for n in _INDEX_NAMES if (directory / n).exists()), None)


def _section_label(directory: Path, root: Path) -> str:
    key = directory.relative_to(root).as_posix()
    if key in SECTION_LABELS:
        return SECTION_LABELS[key]
    index = _index_of(directory)
    if index:
        return _title(directory / index)
    return directory.name.replace("-", " ").replace("_", " ").capitalize()


def _rank(name: str, order: tuple[str, ...]) -> int:
    return order.index(name) if name in order else len(order)


def _entries(directory: Path, root: Path) -> list[Path]:
    """Children of `directory` that belong in the nav, index page excluded, in reading order."""
    order = SECTION_ORDER.get(directory.relative_to(root).as_posix(), ())

    def sort_key(p: Path) -> tuple[int, bool, str]:
        return (_rank(p.name, order), p.name.startswith("_"), p.name)

    return sorted(
        (p for p in directory.iterdir() if (p.is_dir() or p.suffix == ".md") and p.name not in _INDEX_NAMES),
        key=sort_key,
    )


def _nav_for(directory: Path, root: Path, number: str | None) -> list[Any]:
    """Nav entries for the index page, pages and sections of `directory`.

    `number` is the directory's own chapter number ("1", "1.2"), or None when it is below the
    numbered levels. Its children are numbered one level further down, down to NUMBERED_DEPTH.
    """
    items: list[Any] = []
    index = _index_of(directory)
    if index:
        items.append((directory / index).relative_to(root).as_posix())

    numbered_children = number is not None and number.count(".") + 2 <= NUMBERED_DEPTH
    for i, child in enumerate(_entries(directory, root), 1):
        child_number = f"{number}.{i}" if numbered_children else None
        prefix = f"{child_number} " if child_number else ""
        if child.is_dir():
            sub = _nav_for(child, root, child_number)
            if sub:
                items.append({prefix + _section_label(child, root): sub})
        else:
            items.append({prefix + _title(child): child.relative_to(root).as_posix()})
    return items


def build_nav(root: Path) -> list[Any]:
    """The whole nav: Home, one numbered chapter per top-level section, then the remaining pages."""
    nav: list[Any] = [{"Home": _index_of(root)}]
    order = SECTION_ORDER[""]
    chapters = sorted(
        (p for p in root.iterdir() if p.is_dir() and any(p.rglob("*.md"))),
        key=lambda p: (_rank(p.name, order), p.name),
    )
    for i, chapter in enumerate(chapters, 1):
        nav.append({f"{i}. {_section_label(chapter, root)}": _nav_for(chapter, root, str(i))})
    pages = sorted(p for p in root.glob("*.md") if p.name not in _INDEX_NAMES)
    for i, page in enumerate(pages, len(chapters) + 1):
        nav.append({f"{i}. {_title(page)}": page.name})
    return nav


def _github_url(repo_url: str, resolved: str, is_dir: bool, fragment: str) -> str:
    kind = "tree" if is_dir else "blob"
    return f"{repo_url}/{kind}/{BRANCH}/{resolved}{fragment}"


def _rewrite_target(target: str, src_uri: str, docs_dir: Path, repo_root: Path, repo_url: str) -> str:
    if not target or target[0] in "#/" or _SCHEME.match(target) or "?" in target:
        return target
    path, hash_, anchor = target.partition("#")
    fragment = hash_ + anchor
    if "<" in path:
        # A template placeholder such as `<slug>.md` names no file: link the folder that holds them.
        path = path[: path.index("<")].rpartition("/")[0]
        if not path:
            return target
        path += "/"
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(src_uri), path))
    if resolved == "." or resolved.startswith(".."):
        return target

    staged = docs_dir / resolved
    if staged.is_file():
        return target
    if staged.is_dir():
        index = _index_of(staged)
        if index:
            return f"{path.rstrip('/')}/{index}{fragment}"
    in_repo = repo_root / resolved
    if in_repo.exists():
        return _github_url(repo_url, resolved, in_repo.is_dir(), fragment)
    return target


def rewrite_links(markdown: str, src_uri: str, docs_dir: Path, repo_root: Path, repo_url: str) -> str:
    """Rewrite the relative links of one page; fenced code and inline code spans are left alone.

    A link is kept when its target is a published page. A folder with an index page links to that
    page. Anything else that exists in the repository links to GitHub. A target that exists nowhere
    is left as written, so MkDocs reports it.
    """

    def fix(target: str) -> str:
        return _rewrite_target(target, src_uri, docs_dir, repo_root, repo_url)

    def inline(m: re.Match[str]) -> str:
        if m["code"]:
            return m[0]
        target = m["target"]
        if target.startswith("<") and target.endswith(">"):
            return f"](<{fix(target[1:-1])}>"
        return f"]({fix(target)}"

    out: list[str] = []
    fence = ""
    for line in markdown.split("\n"):
        opened = _FENCE.match(line)
        if fence:
            if opened and opened[1][0] == fence[0] and len(opened[1]) >= len(fence):
                fence = ""
            out.append(line)
        elif opened:
            fence = opened[1]
            out.append(line)
        else:
            ref = _REFDEF.match(line)
            if ref:
                line = ref[1] + fix(ref[2]) + line[ref.end() :]
            out.append(_INLINE.sub(inline, line))
    return "\n".join(out)


def on_config(config: Any) -> Any:
    """Install the GitHub slugifier on the `toc` extension and generate the nav from the staged tree.

    The slugifier is set here rather than in ``mkdocs.yml`` because a ``!!python/name:`` tag can only
    name a module on ``sys.path``; hooks are loaded by file path, so this always resolves.
    """
    config["mdx_configs"].setdefault("toc", {})["slugify"] = _github_slugify
    config["nav"] = build_nav(Path(config["docs_dir"]))
    return config


def on_page_markdown(markdown: str, page: Any, config: Any, files: Any) -> str:
    return rewrite_links(
        markdown,
        page.file.src_uri,
        Path(config["docs_dir"]),
        Path(config.config_file_path).parent,
        config["repo_url"],
    )
