# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fill the generated sections of the Markdown pages under docs/.

    uv run tools/build_docs.py                write every generated section
    uv run tools/build_docs.py --check        exit 1 if any generated section would change
    uv run tools/build_docs.py --root PATH    use PATH as the repository root (default: parent of tools/)

Exit codes: 0 everything written or already up to date; 1 (--check only) a generated section would change,
the files are listed; 2 invalid input, each problem printed as "file: reason".

A generated section sits between two marker lines, each alone on its line:

    <!-- BEGIN GENERATED: NAME -->
    <!-- END GENERATED: NAME -->

Everything outside the markers is left byte for byte unchanged. The sections:

    appears-in   every page of type index or project (not README.md): the docs pages that link to it
    a-z          docs/index/README.md: every index and project page, A to Z, with aliases
    watchlist    docs/projects/README.md: docs/projects/watchlist.tsv joined with the newest GitHub snapshot
    changes      README.md of trends, projects, papers, datasets, benchmarks: the 15 newest rows of changes.tsv

Markers inside fenced code blocks are examples and are ignored. The output has no timestamps and a fixed sort
order, so a second run changes nothing. Warnings (a stale snapshot, a README without its markers) go to stderr
and never into a page.
"""

from __future__ import annotations

import argparse
import csv
import posixpath
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import unquote

BEGIN, END = "BEGIN", "END"
SECTION_NAMES = ("appears-in", "a-z", "watchlist", "changes")
CHANGES_FOLDERS = ("trends", "projects", "papers", "datasets", "benchmarks")
CHAPTERS = (
    ("Home", None),
    ("History", "history"),
    ("Trends", "trends"),
    ("Projects", "projects"),
    ("Papers", "papers"),
    ("Datasets", "datasets"),
    ("Benchmarks", "benchmarks"),
    ("Experiments", "experiments"),
    ("Applied to Pinakes", "applied-to-pinakes"),
    ("Index", "index"),
)
OTHER_CHAPTER = "Other"
INDEX_KINDS = ("concept", "system", "standard")
CHANGE_KINDS = ("added", "updated", "settled", "faded", "removed")
CHANGES_HEADER = ["date_utc", "kind", "subject", "summary", "source", "read_utc"]
WATCHLIST_HEADER = ["repo", "category", "trends", "note"]
CHANGES_LIMIT = 15
STALE_DAYS = 30
NO_LINKS = "No page links here yet."
NO_CHANGES = "No changes recorded yet."

MARKER_RE = re.compile(r"^<!-- (BEGIN|END) GENERATED: ([A-Za-z0-9_-]+) -->$")
FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
KEY_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):[ \t]*(.*)$")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
LINK_RE = re.compile(r"\]\(\s*(?:<([^>]*)>|([^)\s]*))")
CODE_SPAN_RE = re.compile(r"(?<!`)(`+)(?!`).+?(?<!`)\1(?!`)", re.DOTALL)
SNAPSHOT_DIR_RE = re.compile(r"^(\d{8})_(\d{4})-github$")
REPO_RE = re.compile(r"^[^/\s]+/[^/\s]+$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}(?:\d{2}(?:\d{2})?)?(?: \d{2}:\d{2}(?: UTC)?)?$")
PUSHED_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")


class InputProblem(Exception):
    """Invalid input: one or more 'file: reason' lines."""

    def __init__(self, *problems: str) -> None:
        super().__init__("; ".join(problems))
        self.problems = list(problems)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


# --------------------------------------------------------------------------------------------- pages


@dataclass
class Section:
    name: str
    begin: int  # index of the BEGIN line
    end: int  # index of the END line


@dataclass
class Page:
    rel: str  # path relative to docs/, forward slashes
    lines: list[str]
    meta: dict[str, str | list[str]] = field(default_factory=dict)
    title: str | None = None
    sections: list[Section] = field(default_factory=list)
    text_lines: list[str] = field(default_factory=list)  # visible text: no front matter, fences, generated sections

    @property
    def name(self) -> str:
        return f"docs/{self.rel}"

    @property
    def type(self) -> str:
        return str(self.meta.get("type", ""))

    @property
    def is_readme(self) -> bool:
        return posixpath.basename(self.rel) == "README.md"

    @property
    def folder(self) -> str:
        return posixpath.dirname(self.rel)

    @property
    def chapter(self) -> str:
        head = self.rel.split("/")[0] if "/" in self.rel else None
        for label, folder in CHAPTERS:
            if folder == head and (head is not None or self.rel == "README.md"):
                return label
        return OTHER_CHAPTER

    @property
    def is_target(self) -> bool:
        """A page that gets an appears-in list."""
        return self.type in ("index", "project") and not self.is_readme

    def require_title(self, why: str) -> str:
        if not self.title:
            raise InputProblem(f"{self.name}: no top-level '# ' heading ({why})")
        return self.title


def parse_front_matter(lines: list[str]) -> tuple[dict[str, str | list[str]], int, list[str]]:
    """Return (meta, index of the closing '---' line, problems). Index is -1 when there is no block."""
    first = lines[0].lstrip("﻿").strip() if lines else ""
    if first != "---":
        return {}, -1, ["no front matter"]
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}, -1, ["front matter is not closed"]
    meta: dict[str, str | list[str]] = {}
    problems: list[str] = []
    for n, raw in enumerate(lines[1:end], start=2):
        line = raw.rstrip()
        if not line.strip():
            continue
        m = KEY_RE.match(line)
        if not m:
            problems.append(f"front matter line {n} is not 'key: value' or 'key: [a, b]': {line!r}")
            continue
        key, value = m.group(1), m.group(2).strip()
        if key in meta:
            problems.append(f"front matter key {key!r} appears twice")
            continue
        if value.startswith("["):
            if not value.endswith("]") or "[" in value[1:-1] or "]" in value[1:-1]:
                problems.append(f"front matter line {n}: list for {key!r} must be one line '[a, b, c]'")
                continue
            meta[key] = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        else:
            meta[key] = value
    return meta, end, problems


def scan_body(lines: list[str], start: int, name: str) -> tuple[list[Section], list[str], str | None, list[str]]:
    """Walk the body once: generated sections, visible text lines, the title, problems."""
    sections: list[Section] = []
    text: list[str] = []
    problems: list[str] = []
    title: str | None = None
    fence: tuple[str, int] | None = None
    open_section: tuple[str, int] | None = None
    seen: set[str] = set()
    for i in range(start, len(lines)):
        line = lines[i]
        stripped = line.strip()
        m = MARKER_RE.match(stripped)
        if open_section is not None:
            if m and m.group(1) == END and m.group(2) == open_section[0]:
                sections.append(Section(open_section[0], open_section[1], i))
                open_section = None
            elif m:
                problems.append(f"{name}: line {i + 1}: marker {stripped!r} inside generated section {open_section[0]!r}")
            continue
        if fence is not None:
            close = re.match(r"^ {0,3}(`+|~+)\s*$", line)
            if close and close.group(1)[0] == fence[0] and len(close.group(1)) >= fence[1]:
                fence = None
            continue
        opener = FENCE_OPEN_RE.match(line)
        if opener and not (opener.group(1)[0] == "`" and "`" in opener.group(2)):
            fence = (opener.group(1)[0], len(opener.group(1)))
            continue
        if m:
            kind, section = m.group(1), m.group(2)
            if kind == END:
                problems.append(f"{name}: line {i + 1}: END marker for {section!r} without a BEGIN")
            elif section not in SECTION_NAMES:
                problems.append(f"{name}: line {i + 1}: unknown generated section {section!r}")
            elif section in seen:
                problems.append(f"{name}: line {i + 1}: generated section {section!r} appears twice")
            else:
                seen.add(section)
                open_section = (section, i)
            continue
        if stripped.startswith("<!--") and "GENERATED" in stripped:
            problems.append(f"{name}: line {i + 1}: malformed generated-section marker {stripped!r}")
            continue
        if title is None and line.startswith("# "):
            title = re.sub(r"\s+#+\s*$", "", line[2:]).strip() or None
        text.append(line)
    if open_section is not None:
        problems.append(f"{name}: BEGIN marker for {open_section[0]!r} (line {open_section[1] + 1}) has no END")
    return sections, text, title, problems


def load_pages(docs: Path) -> list[Page]:
    if not docs.is_dir():
        raise InputProblem(f"docs: folder not found: {docs}")
    pages: list[Page] = []
    problems: list[str] = []
    for path in sorted(docs.rglob("*.md")):
        if not path.is_file():
            continue
        rel = path.relative_to(docs).as_posix()
        try:
            raw = path.read_bytes().decode("utf-8")
        except (UnicodeDecodeError, OSError) as err:
            problems.append(f"docs/{rel}: cannot read as UTF-8: {err}")
            continue
        lines = raw.split("\n")
        meta, end, fm_problems = parse_front_matter(lines)
        page = Page(rel=rel, lines=lines, meta=meta)
        if fm_problems:
            problems += [f"{page.name}: {p}" for p in fm_problems]
            continue
        if not str(meta.get("type", "")).strip():
            problems.append(f"{page.name}: front matter has no 'type'")
            continue
        page.sections, page.text_lines, page.title, body_problems = scan_body(lines, end + 1, page.name)
        problems += body_problems
        pages.append(page)
    if problems:
        raise InputProblem(*problems)
    return pages


# ------------------------------------------------------------------------------------------- helpers


def esc_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|")


def esc_text(value: str) -> str:
    return value.replace("[", "\\[").replace("]", "\\]")


def link(title: str, target: str) -> str:
    return f"[{esc_text(title)}]({target})"


def rel_link(from_rel: str, to_rel: str) -> str:
    return posixpath.relpath(to_rel, posixpath.dirname(from_rel) or ".")


def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))


def name_key(name: str) -> tuple[str, str]:
    return (strip_accents(name).casefold(), name)


def meta_list(page: Page, key: str) -> list[str]:
    value = page.meta.get(key, [])
    if not isinstance(value, list):
        raise InputProblem(f"{page.name}: {key!r} must be a list like [a, b]")
    return value


def read_tsv(path: Path, shown: str, header: list[str]) -> list[list[str]]:
    """Rows of a tab-separated file with an exact header line; blank lines are skipped."""
    try:
        raw = path.read_bytes().decode("utf-8")
    except (UnicodeDecodeError, OSError) as err:
        raise InputProblem(f"{shown}: cannot read: {err}") from err
    lines = [ln.rstrip("\r") for ln in raw.lstrip("﻿").split("\n")]
    if not lines or lines[0].split("\t") != header:
        raise InputProblem(f"{shown}: header must be exactly {chr(9).join(header)!r}")
    rows = []
    for n, line in enumerate(lines[1:], start=2):
        if not line.strip():
            continue
        cells = line.split("\t")
        if len(cells) != len(header):
            raise InputProblem(f"{shown}: line {n} has {len(cells)} columns, expected {len(header)}")
        rows.append([c.strip() for c in cells])
    return rows


# ---------------------------------------------------------------------------------------- appears-in


def extract_links(page: Page) -> list[str]:
    """Inline link targets in the visible text: code fences, code spans and generated sections ignored."""
    text = "\n".join(page.text_lines)
    targets: list[str] = []
    for paragraph in re.split(r"\n[ \t]*\n", text):
        paragraph = CODE_SPAN_RE.sub(" ", paragraph)
        for m in LINK_RE.finditer(paragraph):
            targets.append(m.group(1) if m.group(1) is not None else m.group(2))
    return targets


def resolve_link(page: Page, target: str, known: set[str]) -> str | None:
    """The docs page (path relative to docs/) a link points at, or None."""
    target = target.strip()
    if not target or target.startswith(("#", "/")) or SCHEME_RE.match(target):
        return None
    target = unquote(re.split(r"[#?]", target, maxsplit=1)[0])
    if not target:
        return None
    joined = posixpath.normpath(posixpath.join(page.folder, target))
    if joined == ".." or joined.startswith("../") or joined == ".":
        return None
    if joined in known:
        return joined
    if target.endswith("/") or posixpath.join(joined, "README.md") in known:
        candidate = posixpath.join(joined, "README.md")
        return candidate if candidate in known else None
    return None


def inbound_links(pages: list[Page]) -> dict[str, set[str]]:
    known = {p.rel for p in pages}
    inbound: dict[str, set[str]] = {}
    for page in pages:
        for target in extract_links(page):
            hit = resolve_link(page, target, known)
            if hit is not None and hit != page.rel:
                inbound.setdefault(hit, set()).add(page.rel)
    return inbound


def render_appears_in(target: Page, by_rel: dict[str, Page], inbound: dict[str, set[str]]) -> list[str]:
    sources = [by_rel[r] for r in inbound.get(target.rel, ())]
    if not sources:
        return [NO_LINKS]
    labels = [label for label, _ in CHAPTERS] + [OTHER_CHAPTER]
    groups: dict[str, list[tuple[tuple[str, str], str, str]]] = {label: [] for label in labels}
    for src in sources:
        title = src.require_title(f"needed to list it in the appears-in list of {target.name}")
        groups[src.chapter].append((name_key(title) + (src.rel,), title, rel_link(target.rel, src.rel)))
    out: list[str] = []
    for label in labels:
        items = sorted(groups[label], key=lambda item: item[0])
        if not items:
            continue
        if out:
            out.append("")
        out += [f"**{label}**", ""]
        out += [f"- {link(title, href)}" for _, title, href in items]
    return out


# -------------------------------------------------------------------------------------------- a-z


def render_az(readme: Page, pages: list[Page]) -> list[str]:
    entries: list[tuple[tuple[str, str], str, str]] = []  # sort key, display name, line
    titles: dict[str, str] = {}  # casefolded title -> page name
    aliases: dict[str, str] = {}  # casefolded alias -> owning page name
    for page in pages:
        if not page.is_target:
            continue
        title = page.require_title("needed for the A to Z list")
        key = title.casefold()
        if key in titles:
            raise InputProblem(f"{page.name}: title {title!r} is also the title of {titles[key]}")
        titles[key] = page.name
    for page in pages:
        if not page.is_target:
            continue
        title = page.title or ""
        href = rel_link(readme.rel, page.rel)
        if page.type == "index":
            kind = page.meta.get("kind", "")
            if kind not in INDEX_KINDS:
                raise InputProblem(f"{page.name}: kind must be one of {', '.join(INDEX_KINDS)}, got {kind!r}")
        else:
            kind = "project"
        entries.append((name_key(title) + (href,), title, f"- {link(title, href)} : {kind}"))
        for alias in meta_list(page, "aliases") if page.type == "index" else []:
            akey = alias.casefold()
            if akey in titles:
                raise InputProblem(f"{page.name}: alias {alias!r} equals the title of {titles[akey]}")
            if akey in aliases:
                raise InputProblem(f"{page.name}: alias {alias!r} is also an alias in {aliases[akey]}")
            aliases[akey] = page.name
            entries.append((name_key(alias) + (href,), alias, f"- {alias}, see {link(title, href)}"))
    if not entries:
        return ["No entries yet."]
    entries.sort(key=lambda e: e[0])
    groups: dict[str, list[str]] = {}
    for key, name, line in entries:
        first = strip_accents(name).lstrip()[:1].upper()
        heading = first if "A" <= first <= "Z" else "0-9 and symbols"
        groups.setdefault(heading, []).append(line)
    order = sorted(groups, key=lambda h: ("" if h == "0-9 and symbols" else h))
    out: list[str] = []
    for heading in order:
        if out:
            out.append("")
        out += [f"### {heading}", ""] + groups[heading]
    return out


# ---------------------------------------------------------------------------------------- watchlist


def newest_snapshot(root: Path) -> tuple[Path, datetime] | None:
    base = root / "kb-kg" / "landscape"
    best: tuple[str, Path] | None = None
    if base.is_dir():
        for entry in base.iterdir():
            if SNAPSHOT_DIR_RE.match(entry.name) and (entry / "repos.tsv").is_file():
                if best is None or entry.name > best[0]:
                    best = (entry.name, entry)
    if best is None:
        return None
    m = SNAPSHOT_DIR_RE.match(best[0])
    assert m
    try:
        taken = datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M").replace(tzinfo=timezone.utc)
    except ValueError as err:
        raise InputProblem(f"kb-kg/landscape/{best[0]}: folder name is not a date: {err}") from err
    return best[1], taken


def read_snapshot(path: Path) -> dict[str, dict[str, str]]:
    shown = f"kb-kg/landscape/{path.parent.name}/repos.tsv"
    try:
        with path.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE)
            fields = reader.fieldnames or []
            missing = [c for c in ("full_name", "stars", "pushed_at", "license", "flags") if c not in fields]
            if missing:
                raise InputProblem(f"{shown}: lacks column {', '.join(missing)}")
            rows: dict[str, dict[str, str]] = {}
            for row in reader:
                name = (row.get("full_name") or "").strip()
                if name:
                    rows.setdefault(name.casefold(), {k: (v or "").strip() for k, v in row.items() if k})
            return rows
    except (UnicodeDecodeError, OSError, csv.Error) as err:
        raise InputProblem(f"{shown}: cannot read: {err}") from err


def project_pages_by_repo(pages: list[Page]) -> dict[str, Page]:
    by_repo: dict[str, Page] = {}
    for page in pages:
        if page.type != "project" or page.is_readme:
            continue
        repo = str(page.meta.get("repo", "")).strip()
        if not REPO_RE.match(repo):
            raise InputProblem(f"{page.name}: 'repo' must be owner/name, got {repo!r}")
        if repo.casefold() in by_repo:
            raise InputProblem(f"{page.name}: repo {repo!r} is also on {by_repo[repo.casefold()].name}")
        by_repo[repo.casefold()] = page
    return by_repo


def format_stars(raw: str, repo: str, shown: str) -> tuple[int, str]:
    if not raw.isdigit():
        raise InputProblem(f"{shown}: stars for {repo} is not a whole number: {raw!r}")
    return int(raw), f"{int(raw):,}"


def format_pushed(raw: str, repo: str, shown: str) -> str:
    m = PUSHED_RE.match(raw)
    if not m:
        raise InputProblem(f"{shown}: pushed_at for {repo} is not a date: {raw!r}")
    return "".join(m.groups())


def render_watchlist(root: Path, readme: Page, pages: list[Page], warnings: list[str], now: datetime) -> list[str]:
    docs = root / "docs"
    tsv = docs / "projects" / "watchlist.tsv"
    if not tsv.is_file():
        return ["No watch list yet."]
    rows = read_tsv(tsv, "docs/projects/watchlist.tsv", WATCHLIST_HEADER)
    if not rows:
        return ["No projects on the watch list yet."]
    by_rel = {p.rel: p for p in pages}
    by_repo = project_pages_by_repo(pages)
    snap = newest_snapshot(root)
    if snap is None:
        raise InputProblem("kb-kg/landscape: no <YYYYMMDD_HHMM>-github folder with a repos.tsv, needed for the watch list")
    folder, taken = snap
    shown = f"kb-kg/landscape/{folder.name}/repos.tsv"
    if now - taken > timedelta(days=STALE_DAYS):
        warnings.append(f"the newest GitHub snapshot ({folder.name}) is older than {STALE_DAYS} days")
    snapshot = read_snapshot(folder / "repos.tsv")
    seen: set[str] = set()
    built: list[tuple[str, int, str, str]] = []  # category, -stars, repo, line
    for repo, category, trends, note in rows:
        where = f"docs/projects/watchlist.tsv: {repo}"
        if not REPO_RE.match(repo):
            raise InputProblem(f"docs/projects/watchlist.tsv: repo must be owner/name, got {repo!r}")
        if repo.casefold() in seen:
            raise InputProblem(f"{where}: listed twice")
        seen.add(repo.casefold())
        trend_links = []
        for slug in [t.strip() for t in trends.split(",") if t.strip()]:
            trend = by_rel.get(f"trends/{slug}.md")
            if not SLUG_RE.match(slug) or trend is None:
                raise InputProblem(f"{where}: trend {slug!r} has no page docs/trends/{slug}.md")
            trend_links.append(link(trend.require_title("needed for the watch list"), rel_link(readme.rel, trend.rel)))
        page = by_repo.get(repo.casefold())
        project = link(page.require_title("needed for the watch list"), rel_link(readme.rel, page.rel)) if page else (
            f"[{repo}](https://github.com/{repo})"
        )
        row = snapshot.get(repo.casefold())
        if row is None:
            stars_key, cells = -1, ["not in snapshot", "n/a", "n/a", "n/a"]
        else:
            stars_key, stars = format_stars(row["stars"], repo, shown)
            cells = [stars, format_pushed(row["pushed_at"], repo, shown), row["license"] or "unstated", row["flags"] or "none"]
        line = "| " + " | ".join(
            [project, esc_cell(category), ", ".join(trend_links) or "none"] + [esc_cell(c) for c in cells] + [esc_cell(note)]
        ) + " |"
        built.append((category, -stars_key, repo.casefold(), line))
    built.sort(key=lambda b: (b[0].casefold(), b[0], b[1], b[2]))
    stamp = taken.strftime("%Y%m%d %H:%M")
    return [
        f"Stars, last push, licence (GitHub's detection of the LICENSE file) and flags come from the GitHub snapshot "
        f"taken {stamp} UTC (kb-kg/landscape/{folder.name}/). Stars are a signal, not a verdict.",
        "",
        "| Project | Category | Trends | Stars | Last push | Licence | Flags | Note |",
        "|---|---|---|---|---|---|---|---|",
    ] + [b[3] for b in built]


# ------------------------------------------------------------------------------------------ changes


def url_target(url: str) -> str:
    return url.replace(" ", "%20").replace("(", "%28").replace(")", "%29").replace("|", "%7C")


def render_changes(root: Path, readme: Page) -> list[str]:
    tsv = root / "docs" / readme.folder / "changes.tsv"
    if not tsv.is_file():
        return [NO_CHANGES]
    shown = f"docs/{readme.folder}/changes.tsv"
    rows = read_tsv(tsv, shown, CHANGES_HEADER)
    for n, row in enumerate(rows, start=1):
        if row[1] not in CHANGE_KINDS:
            raise InputProblem(f"{shown}: row {n}: kind must be one of {', '.join(CHANGE_KINDS)}, got {row[1]!r}")
        if not DATE_RE.match(row[0]):
            raise InputProblem(f"{shown}: row {n}: date_utc must look like YYYYMMDD or YYYYMMDD HH:MM, got {row[0]!r}")
    if not rows:
        return [NO_CHANGES]
    newest = sorted(rows, key=lambda r: r[0], reverse=True)[:CHANGES_LIMIT]  # stable: file order within a date
    out = ["| Date | Kind | Subject | Summary | Source |", "|---|---|---|---|---|"]
    for date, kind, subject, summary, source, _read in newest:
        if re.match(r"^https?://\S+$", source):
            src = f"[source]({url_target(source)})"
        else:
            src = esc_cell(source)
        out.append("| " + " | ".join([esc_cell(date), kind, esc_cell(subject), esc_cell(summary), src]) + " |")
    return out + ["", "Full list: [changes.tsv](changes.tsv)"]


# ------------------------------------------------------------------------------------------- driver


def allowed_sections(page: Page) -> set[str]:
    allowed: set[str] = set()
    if page.is_target:
        allowed.add("appears-in")
    if page.rel == "index/README.md":
        allowed.add("a-z")
    if page.rel == "projects/README.md":
        allowed.add("watchlist")
    if page.is_readme and page.folder in CHANGES_FOLDERS:
        allowed.add("changes")
    return allowed


def check_markers(pages: list[Page], warnings: list[str]) -> None:
    problems: list[str] = []
    for page in pages:
        allowed = allowed_sections(page)
        present = {s.name for s in page.sections}
        for name in sorted(present - allowed):
            problems.append(f"{page.name}: generated section {name!r} is not allowed on this page")
        if page.is_target and "appears-in" not in present:
            problems.append(f"{page.name}: lacks the appears-in markers (type {page.type})")
        for name in sorted(allowed - {"appears-in"} - present):
            warnings.append(f"{page.name}: has no '{name}' markers, nothing generated there")
    if problems:
        raise InputProblem(*problems)


def apply_sections(page: Page, content: dict[str, list[str]]) -> str:
    lines = list(page.lines)
    for section in sorted(page.sections, key=lambda s: s.begin, reverse=True):
        if section.name in content:
            lines[section.begin + 1 : section.end] = ["", *content[section.name], ""]
    return "\n".join(lines)


def build(root: Path, warnings: list[str], now: datetime | None = None) -> dict[str, tuple[str, str]]:
    """Return {path relative to root: (old text, new text)} for every page that has generated sections."""
    pages = load_pages(root / "docs")
    check_markers(pages, warnings)
    by_rel = {p.rel: p for p in pages}
    inbound = inbound_links(pages)
    now = now or utcnow()
    result: dict[str, tuple[str, str]] = {}
    for page in pages:
        if not page.sections:
            continue
        content: dict[str, list[str]] = {}
        for section in page.sections:
            if section.name == "appears-in":
                content["appears-in"] = render_appears_in(page, by_rel, inbound)
            elif section.name == "a-z":
                content["a-z"] = render_az(page, pages)
            elif section.name == "watchlist":
                content["watchlist"] = render_watchlist(root, page, pages, warnings, now)
            elif section.name == "changes":
                content["changes"] = render_changes(root, page)
        result[page.name] = ("\n".join(page.lines), apply_sections(page, content))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="exit 1 if any generated section would change; write nothing")
    parser.add_argument("--root", default=None, help="repository root (default: the parent of tools/)")
    args = parser.parse_args(argv)
    root = Path(args.root) if args.root else Path(__file__).resolve().parent.parent
    warnings: list[str] = []
    try:
        result = build(root, warnings)
    except InputProblem as err:
        for w in warnings:
            print(f"build_docs: warning: {w}", file=sys.stderr)
        for problem in err.problems:
            print(f"build_docs: {problem}", file=sys.stderr)
        return 2
    for w in warnings:
        print(f"build_docs: warning: {w}", file=sys.stderr)
    changed = sorted(name for name, (old, new) in result.items() if old != new)
    if args.check:
        if changed:
            print("build_docs: generated sections out of date in:", file=sys.stderr)
            for name in changed:
                print(f"  {name}", file=sys.stderr)
            return 1
        print(f"build_docs: {len(result)} page(s) with generated sections are current")
        return 0
    for name in changed:
        with (root / name).open("w", encoding="utf-8", newline="") as fh:
            fh.write(result[name][1])
        print(f"build_docs: wrote {name}")
    print(f"build_docs: {len(changed)} written, {len(result) - len(changed)} already current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
