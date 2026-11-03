"""MkDocs hooks for the documentation site.

The pages are the repository's own Markdown, written to be read on GitHub. The site is a view over
them, never a second copy, so four things that GitHub does for free are done here:

* Heading anchors match GitHub's. Every cross-document anchor was written against GitHub, so the
  site adopts GitHub's slug algorithm rather than the pages being rewritten to match the site.
  Python-Markdown's default drops the em dash *and* collapses the whitespace either side of it
  (``a — b`` becomes ``a-b``, GitHub keeps ``a--b``), and ``pymdownx.slugs.slugify`` strips an
  angle-bracketed code span as if it were an HTML tag.
* The navigation is generated from the staged tree (see ``build_nav``), so a page added to the
  repository appears on the site with no edit to ``mkdocs.yml``. Only the chapter list and the
  archive's section order are written down here.
* Relative links are resolved against the page's *repository* path, not its staged path, because
  ``docs/`` is staged without its prefix (see ``rewrite_links``).
* Each page's "edit this page" link points at the file that holds it in the repository
  (``on_page_context``).

``docs-site/stage_docs.py`` writes ``staged-paths.json`` (staged path to repository path) beside the
pages; this module reads it.

Not type-checked: mkdocs is installed from ``requirements.txt`` into an ephemeral environment and
is not imported here, so the helpers run under plain ``unittest``.
"""

from __future__ import annotations

import json
import posixpath
import re
import unicodedata
from pathlib import Path
from typing import Any, Callable

BRANCH = "main"
MAP_NAME = "staged-paths.json"

# The numbered chapters of the new documentation, in order: (folder, nav label). The number is the
# position in this tuple and is fixed: a chapter whose folder is missing is skipped and the others
# keep their numbers.
CHAPTERS = (
    ("history", "History"),
    ("trends", "Trends"),
    ("projects", "Projects"),
    ("papers", "Papers"),
    ("datasets", "Datasets"),
    ("benchmarks", "Benchmarks"),
    ("experiments", "Experiments"),
    ("applied-to-pinakes", "Applied to Pinakes"),
)
# The "Index" tab: an unnumbered folder of entries.
INDEX_DIR = "index"
INDEX_LABEL = "Index"
# The "Archive" tab: unnumbered. The sections are folders (labels in SECTION_LABELS), the pages are files.
ARCHIVE_LABEL = "Archive"
ARCHIVE_DIRS = ("kb-kg", "pinakes")
ARCHIVE_PAGES = (("DECISIONS.md", "Decisions"),)

# Reading order inside an archive directory, simple to deep. A directory not listed here sorts by
# name, and an entry not listed sorts after the listed ones, so new material shows up without an edit
# here.
SECTION_ORDER = {
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

# The nav numbers a chapter and the pages inside it ("3.", "3.2"); deeper pages stay unnumbered.
# page-numbering.js copies the number onto the page title and numbers the headings below it,
# replacing the numbers that many pages carry in their own headings. Index and Archive are not
# numbered.
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


def _split_front_matter(text: str) -> tuple[dict[str, str], list[str]]:
    """The `key: value` pairs of a leading `---` block, and the lines after it.

    Only single-line `key: value` pairs are read (the documentation allows nothing else); a page
    without a block, or with an unclosed one, has no front matter.
    """
    lines = text.splitlines()
    if not lines or lines[0].rstrip() != "---":
        return {}, lines
    end = next((i for i, line in enumerate(lines[1:], 1) if line.rstrip() == "---"), 0)
    if not end:
        return {}, lines
    meta: dict[str, str] = {}
    for line in lines[1:end]:
        key, colon, value = line.partition(":")
        if colon and key.strip() and not key[0].isspace():
            meta[key.strip()] = value.strip()
    return meta, lines[end + 1 :]


def _title(path: Path) -> str:
    """The page's first H1, or its file name when it has none. YAML front matter is skipped."""
    _, lines = _split_front_matter(path.read_text(encoding="utf-8"))
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip().replace("`", "").replace("**", "")
    return path.stem


def _order(path: Path) -> int | None:
    """The page's front-matter `order`, or None when it has none."""
    meta, _ = _split_front_matter(path.read_text(encoding="utf-8"))
    value = meta.get("order")
    if value is None:
        return None
    if not re.fullmatch(r"-?\d+", value):
        raise ValueError(f"{path.name}: front matter `order` must be an integer, got {value!r}")
    return int(value)


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


def _label(child: Path, root: Path) -> str:
    return _section_label(child, root) if child.is_dir() else _title(child)


def _rank(name: str, order: tuple[str, ...]) -> int:
    return order.index(name) if name in order else len(order)


# A sort key for the children of one directory.
SortKey = Callable[[Path, Path], tuple]


def _chapter_key(child: Path, root: Path) -> tuple:
    """Chapter pages: by front-matter `order` (pages without one last), then by title."""
    page: Path | None = child
    if child.is_dir():
        index = _index_of(child)
        page = child / index if index else None
    order = _order(page) if page else None
    return (order is None, order or 0, _label(child, root).casefold(), child.name)


def _title_key(child: Path, root: Path) -> tuple:
    """Index entries: by title."""
    return (_label(child, root).casefold(), child.name)


def _archive_key(child: Path, root: Path) -> tuple:
    """Archive pages: the listed order of SECTION_ORDER, then by name, templates last."""
    order = SECTION_ORDER.get(child.parent.relative_to(root).as_posix(), ())
    return (_rank(child.name, order), child.name.startswith("_"), child.name)


def _has_pages(directory: Path) -> bool:
    return directory.is_dir() and any(directory.rglob("*.md"))


def _entries(directory: Path, root: Path, key: SortKey) -> list[Path]:
    """Children of `directory` that belong in the nav, index page excluded, in reading order."""
    children = [
        p
        for p in directory.iterdir()
        if p.name not in _INDEX_NAMES and (_has_pages(p) if p.is_dir() else p.suffix == ".md")
    ]
    return sorted(children, key=lambda p: key(p, root))


def _nav_for(directory: Path, root: Path, number: str | None, key: SortKey) -> list[Any]:
    """Nav entries for the index page, pages and sections of `directory`.

    `number` is the directory's own chapter number ("1", "1.2"), or None when it is not numbered
    (the archive and the index, or below the numbered levels). Its children are numbered one level
    further down, down to NUMBERED_DEPTH.
    """
    items: list[Any] = []
    index = _index_of(directory)
    if index:
        items.append((directory / index).relative_to(root).as_posix())

    numbered_children = number is not None and number.count(".") + 2 <= NUMBERED_DEPTH
    for i, child in enumerate(_entries(directory, root, key), 1):
        child_number = f"{number}.{i}" if numbered_children else None
        prefix = f"{child_number} " if child_number else ""
        if child.is_dir():
            items.append({prefix + _section_label(child, root): _nav_for(child, root, child_number, key)})
        else:
            items.append({prefix + _title(child): child.relative_to(root).as_posix()})
    return items


def build_nav(root: Path) -> list[Any]:
    """The whole nav, which Material shows as tabs.

    Home; then the numbered chapters of CHAPTERS ("1. History", with the pages inside numbered
    "1.1", "1.2", ordered by front-matter `order`, then title); then the unnumbered "Index" (entries
    by title); then the unnumbered "Archive" (the old reference, in its own order). A chapter,
    Index or Archive part whose folder has no page is left out, and the chapters keep their numbers.
    """
    nav: list[Any] = []
    home = _index_of(root)
    if home:
        nav.append({"Home": home})

    for number, (folder, label) in enumerate(CHAPTERS, 1):
        if _has_pages(root / folder):
            nav.append({f"{number}. {label}": _nav_for(root / folder, root, str(number), _chapter_key)})

    if _has_pages(root / INDEX_DIR):
        nav.append({INDEX_LABEL: _nav_for(root / INDEX_DIR, root, None, _title_key)})

    archive: list[Any] = []
    for folder in ARCHIVE_DIRS:
        if _has_pages(root / folder):
            archive.append({_section_label(root / folder, root): _nav_for(root / folder, root, None, _archive_key)})
    for name, label in ARCHIVE_PAGES:
        if (root / name).is_file():
            archive.append({label: name})
    if archive:
        nav.append({ARCHIVE_LABEL: archive})
    return nav


def load_mapping(docs_dir: Path) -> dict[str, str]:
    """The staged-path to repository-path mapping that stage_docs.py wrote beside the pages."""
    path = docs_dir / MAP_NAME
    if not path.is_file():
        raise FileNotFoundError(f"{path} is missing: run docs-site/stage_docs.py before building the site")
    return json.loads(path.read_text(encoding="utf-8"))


def _github_url(repo_url: str, resolved: str, is_dir: bool, fragment: str) -> str:
    kind = "tree" if is_dir else "blob"
    return f"{repo_url}/{kind}/{BRANCH}/{resolved}{fragment}"


def _rewrite_target(
    target: str, src_uri: str, repo_path: str, repo_root: Path, repo_url: str, to_staged: dict[str, str]
) -> str:
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
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(repo_path), path))
    if resolved == "." or resolved.startswith(".."):
        return target

    # A staged page, or a folder whose README (index page) is staged: a link between staged paths.
    staged = to_staged.get(resolved) or next(
        (to_staged[f"{resolved}/{n}"] for n in _INDEX_NAMES if f"{resolved}/{n}" in to_staged), None
    )
    if staged:
        return posixpath.relpath(staged, posixpath.dirname(src_uri) or ".") + fragment
    in_repo = repo_root / resolved
    if in_repo.exists():
        return _github_url(repo_url, resolved, in_repo.is_dir(), fragment)
    return target


def rewrite_links(markdown: str, src_uri: str, repo_root: Path, repo_url: str, mapping: dict[str, str]) -> str:
    """Rewrite the relative links of one page; fenced code and inline code spans are left alone.

    `src_uri` is the page's staged path and `mapping` takes every staged path to its repository
    path. A link is resolved against the page's *repository* path, then:

    * a target that is a staged page becomes a relative link between the two staged paths (the
      `#fragment` is kept);
    * a folder whose README is staged links to that README;
    * anything else that exists in the repository (a folder without a README, `tools/`, RESUME.md,
      data files, templates, the root README.md) links to GitHub;
    * a target that exists nowhere is left as written, so MkDocs reports it.
    """
    repo_path = mapping[src_uri]
    to_staged = {repo: staged for staged, repo in mapping.items()}

    def fix(target: str) -> str:
        return _rewrite_target(target, src_uri, repo_path, repo_root, repo_url, to_staged)

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


def edit_url(repo_url: str, edit_uri: str, repo_path: str) -> str:
    """The "edit this page" link of the file at `repo_path` (edit_uri is `edit/main/`)."""
    return f"{repo_url.rstrip('/')}/{edit_uri.strip('/')}/{repo_path}"


# Staged path to repository path, loaded by on_config.
_MAPPING: dict[str, str] = {}


def on_config(config: Any) -> Any:
    """Install the GitHub slugifier on the `toc` extension, load the path mapping and generate the nav.

    The slugifier is set here rather than in ``mkdocs.yml`` because a ``!!python/name:`` tag can only
    name a module on ``sys.path``; hooks are loaded by file path, so this always resolves.
    """
    docs_dir = Path(config["docs_dir"])
    config["mdx_configs"].setdefault("toc", {})["slugify"] = _github_slugify
    _MAPPING.clear()
    _MAPPING.update(load_mapping(docs_dir))
    config["nav"] = build_nav(docs_dir)
    return config


def on_page_markdown(markdown: str, page: Any, config: Any, files: Any) -> str:
    return rewrite_links(
        markdown,
        page.file.src_uri,
        Path(config.config_file_path).parent,
        config["repo_url"],
        _MAPPING,
    )


def on_page_context(context: Any, page: Any, config: Any, nav: Any) -> Any:
    """Point the "edit this page" link at the page's file in the repository, not at its staged path."""
    repo_path = _MAPPING.get(page.file.src_uri)
    if repo_path and config.get("repo_url") and config.get("edit_uri"):
        page.edit_url = edit_url(config["repo_url"], config["edit_uri"], repo_path)
    return context
