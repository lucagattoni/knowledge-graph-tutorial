#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Dated GitHub landscape snapshot for knowledge-graph and agent-memory projects.

    uv run tools/gh_snapshot.py [--out DIR] [--top N] [--no-enrich] [--compare PREV_DIR]

The tool searches GitHub through `gh api` (the GitHub CLI), ranks repositories per
category, and writes repos.tsv, repos.json and README.md into a dated directory.
It never reads or prints a token: `gh` handles authentication itself.

Standard library only. See tools/snapshot/README.md for the full description.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import tomllib
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

__version__ = "1.0.0"

CATEGORIES = ("core", "agent-memory", "markdown-kb", "adjacent")

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = Path(__file__).resolve().parent / "snapshot"
DEFAULT_LANDSCAPE = REPO_ROOT / "kb-kg" / "landscape"

SEARCH_GAP_SECONDS = 2.5  # GitHub allows 30 search requests a minute
MAX_RATE_WAIT_SECONDS = 3900  # never wait more than a little over an hour for a reset
RATE_RETRIES = 3
COMMIT_WINDOW_DAYS = 90
COMMITS_CAP = 100
GRAPHQL_BATCH = 25
DESCRIPTION_LIMIT = 120
SNAPSHOT_DIR_RE = re.compile(r"^\d{8}_\d{4}-github$")
OWNER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]*$")
REPO_RE = re.compile(r"^[A-Za-z0-9._-]+$")


class FatalError(Exception):
    """The run cannot continue (gh missing, not authenticated, bad config)."""


# --------------------------------------------------------------------------- text


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
LOCAL_PATH_RE = re.compile(r"(?:/Users|/home|/private)/\S+")
TOKEN_RE = re.compile(
    r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-ant-[A-Za-z0-9_-]{10,}|AKIA[0-9A-Z]{16})"
)


def scrub(text: str | None) -> str:
    """Remove anything that must not reach a public file: emails, local paths, tokens."""
    if not text:
        return ""
    text = EMAIL_RE.sub("[email]", text)
    text = LOCAL_PATH_RE.sub("[path]", text)
    text = TOKEN_RE.sub("[token]", text)
    return text


def clean_description(text: str | None, limit: int = DESCRIPTION_LIMIT) -> str:
    """One line, scrubbed, at most `limit` characters."""
    text = " ".join(scrub(text).split())
    if len(text) > limit:
        text = text[: limit - 3].rstrip() + "..."
    return text


def md_cell(value: object) -> str:
    """Make a value safe inside a Markdown table cell."""
    text = " ".join(str(value).split())
    return text.replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")


# --------------------------------------------------------------------------- config


@dataclass(frozen=True)
class Thresholds:
    quiet_days: int = 90
    fast_growth_stars_per_day: float = 150.0
    low_forks_min_stars: int = 5000
    low_forks_per_100_stars: float = 3.0


@dataclass(frozen=True)
class SearchSettings:
    per_page: int = 100
    pages: int = 1
    min_stars: int = 100
    quiet_pass: bool = True


@dataclass(frozen=True)
class Config:
    thresholds: Thresholds
    search: SearchSettings
    queries: dict[str, tuple[str, ...]]  # category -> queries, in file order
    descriptions: dict[str, str]


def load_config(path: Path) -> Config:
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise FatalError(f"cannot read {path.name}: {exc}") from exc

    def section(name: str, allowed: set[str]) -> dict:
        data = raw.get(name, {})
        unknown = set(data) - allowed
        if unknown:
            raise FatalError(f"{path.name} [{name}]: unknown keys {sorted(unknown)}")
        return data

    flags = section("flags", set(Thresholds.__dataclass_fields__))
    search = section("search", set(SearchSettings.__dataclass_fields__))
    thresholds = Thresholds(**flags)
    settings = SearchSettings(**search)
    if not 1 <= settings.per_page <= 100 or settings.pages < 1:
        raise FatalError(f"{path.name} [search]: per_page must be 1..100 and pages >= 1")
    if thresholds.quiet_days < 1:
        raise FatalError(f"{path.name} [flags]: quiet_days must be >= 1")

    unknown_tables = set(raw) - {"flags", "search", *CATEGORIES}
    if unknown_tables:
        raise FatalError(f"{path.name}: unknown tables {sorted(unknown_tables)}")
    queries: dict[str, tuple[str, ...]] = {}
    descriptions: dict[str, str] = {}
    for cat in CATEGORIES:
        table = raw.get(cat)
        if not table or not table.get("queries"):
            raise FatalError(f"{path.name}: category [{cat}] needs a non-empty queries list")
        queries[cat] = tuple(str(q) for q in table["queries"])
        descriptions[cat] = str(table.get("description", ""))
    return Config(thresholds, settings, queries, descriptions)


def parse_watchlist(text: str) -> dict[str, tuple[str, str]]:
    """Return {lowercase full_name: (name as listed, category)}."""
    watch: dict[str, tuple[str, str]] = {}
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) != 2:
            raise FatalError(f"watchlist line {number}: expected owner/repo<TAB>category")
        name, category = parts[0].strip(), parts[1].strip()
        if category not in CATEGORIES:
            raise FatalError(f"watchlist line {number}: unknown category {category!r}")
        if not valid_full_name(name):
            raise FatalError(f"watchlist line {number}: bad repository name {name!r}")
        if name.lower() in watch:
            raise FatalError(f"watchlist line {number}: duplicate {name}")
        watch[name.lower()] = (name, category)
    return watch


def valid_full_name(name: str) -> bool:
    owner, sep, repo = name.partition("/")
    return bool(sep) and bool(OWNER_RE.match(owner)) and bool(REPO_RE.match(repo)) and "/" not in repo


# --------------------------------------------------------------------------- time


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value).astimezone(timezone.utc)


def iso_z(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp(moment: datetime) -> str:
    """YYYYMMDD HH:MM, the repository's timestamp format (always UTC)."""
    return moment.astimezone(timezone.utc).strftime("%Y%m%d %H:%M")


def day_stamp(iso: str | None) -> str:
    return iso[:10].replace("-", "") if iso else "-"


# --------------------------------------------------------------------------- pure logic


def is_quiet(days_since_push: int, quiet_days: int) -> bool:
    """The 90-day rule. Whole days since the last push, strictly greater than the limit."""
    return days_since_push > quiet_days


def is_ranked(record: dict, quiet_days: int) -> bool:
    """Ranked tables hold repositories that are neither quiet nor archived."""
    return not record["archived"] and not is_quiet(record["days_since_push"], quiet_days)


def compute_flags(record: dict, th: Thresholds) -> list[str]:
    """Heuristic signals, not verdicts. Computed from the stored (rounded) values."""
    flags = []
    if record["archived"]:
        flags.append("archived")
    if is_quiet(record["days_since_push"], th.quiet_days):
        flags.append("quiet")
    if record["stars_per_day"] >= th.fast_growth_stars_per_day:
        flags.append("fast-growth")
    ratio = record["forks_per_100_stars"]
    if record["stars"] >= th.low_forks_min_stars and ratio is not None and ratio < th.low_forks_per_100_stars:
        flags.append("low-forks")
    return flags


def build_record(item: dict, snapshot: datetime, th: Thresholds) -> dict:
    """Turn one GitHub repository object (REST shape) into a snapshot record."""
    created = parse_ts(item["created_at"])
    pushed = parse_ts(item.get("pushed_at") or item["created_at"])
    stars = int(item.get("stargazers_count") or 0)
    forks = int(item.get("forks_count") or 0)
    age_days = max((snapshot - created).days, 0)
    days_since_push = max((snapshot - pushed).days, 0)
    licence = item.get("license") or {}
    record = {
        "full_name": item["full_name"],
        "category": None,
        "also_in": [],
        "watchlist": False,
        "table": None,
        "rank": None,
        "stars": stars,
        "forks": forks,
        "open_issues": int(item.get("open_issues_count") or 0),
        "created_at": iso_z(created),
        "pushed_at": iso_z(pushed),
        "license": licence.get("spdx_id"),
        "archived": bool(item.get("archived")),
        "language": item.get("language"),
        "description": clean_description(item.get("description")),
        "age_days": age_days,
        "stars_per_day": round(stars / max(age_days, 1), 2),
        "forks_per_100_stars": round(forks * 100 / stars, 2) if stars > 0 else None,
        "days_since_push": days_since_push,
        "flags": [],
        "hits": 0,
        "enriched": False,
        "latest_release": None,
        "latest_release_date": None,
        "commits_90d": None,
        "commits_90d_capped": None,
        "contributors": None,
        "prev_stars": None,
        "star_delta": None,
        "days_between": None,
        "new_entrant": None,
    }
    record["flags"] = compute_flags(record, th)
    return record


def choose_primary(hit_counts: dict[str, int], watch_category: str | None) -> str:
    """Watchlist wins; otherwise the category with most hits; ties go in CATEGORIES order."""
    if watch_category:
        return watch_category
    best = max((hit_counts.get(c, 0) for c in CATEGORIES), default=0)
    for cat in CATEGORIES:
        if hit_counts.get(cat, 0) == best:
            return cat
    return CATEGORIES[0]  # unreachable: CATEGORIES is non-empty


def rank_categories(records: list[dict], quiet_days: int) -> dict[str, dict[str, list[dict]]]:
    """Split each category into the ranked table and the quiet-or-archived table.

    Ranked: not archived and last push within quiet_days, sorted by stars. Everything
    else goes to the quiet table, also sorted by stars. Sets `table` and `rank` in place.
    """
    result = {cat: {"ranked": [], "quiet": []} for cat in CATEGORIES}
    for rec in records:
        bucket = "ranked" if is_ranked(rec, quiet_days) else "quiet"
        result[rec["category"]][bucket].append(rec)
    for tables in result.values():
        for bucket, rows in tables.items():
            rows.sort(key=lambda r: (-r["stars"], r["full_name"].lower()))
            for index, rec in enumerate(rows, 1):
                rec["table"] = bucket
                rec["rank"] = index
    return result


def select_enrichment(tables: dict[str, dict[str, list[dict]]], top_n: int) -> list[dict]:
    """Top N ranked per category plus every watchlist repository."""
    chosen: dict[str, dict] = {}
    for cat in CATEGORIES:
        for rec in tables[cat]["ranked"][:top_n]:
            chosen[rec["full_name"].lower()] = rec
        for bucket in ("ranked", "quiet"):
            for rec in tables[cat][bucket]:
                if rec["watchlist"]:
                    chosen[rec["full_name"].lower()] = rec
    return list(chosen.values())


def parse_last_page(link_header: str | None) -> int | None:
    """Page number of rel="last" in a GitHub Link header, or None."""
    if not link_header:
        return None
    for match in re.finditer(r'<([^>]+)>\s*;\s*rel="([^"]+)"', link_header):
        if match.group(2) == "last":
            pages = parse_qs(urlparse(match.group(1)).query).get("page")
            if pages and pages[0].isdigit():
                return int(pages[0])
    return None


def parse_http_response(text: str) -> tuple[int | None, dict[str, str], str]:
    """Split `gh api -i` output into (status, lowercase headers, body). Uses the last header block."""
    status: int | None = None
    headers: dict[str, str] = {}
    rest = text
    while True:
        match = re.match(r"HTTP/\S+\s+(\d{3})[^\r\n]*\r?\n", rest)
        if not match:
            break
        status = int(match.group(1))
        rest = rest[match.end():]
        headers = {}
        while rest:
            line, _, rest = rest.partition("\n")
            line = line.rstrip("\r")
            if line == "":
                break
            key, colon, value = line.partition(":")
            if colon:
                headers[key.strip().lower()] = value.strip()
    return status, headers, rest


def contributors_from_response(status: int | None, headers: dict[str, str], body: str) -> int | None:
    """Contributor count from a per_page=1 listing: the last page number, else the list length."""
    if status == 204:
        return 0
    if status != 200:
        return None
    last = parse_last_page(headers.get("link"))
    if last is not None:
        return last
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    return len(data) if isinstance(data, list) else None


def is_rate_limited(returncode: int, stdout: str, stderr: str) -> bool:
    if returncode == 0:
        return False
    text = f"{stderr}\n{stdout}".lower()
    return any(s in text for s in ("rate limit", "secondary rate", "abuse detection", "http 429"))


def is_auth_error(returncode: int, stdout: str, stderr: str) -> bool:
    if returncode == 0:
        return False
    text = f"{stderr}\n{stdout}".lower()
    return "gh auth login" in text or "http 401" in text or "bad credentials" in text


# ---- GraphQL batching ------------------------------------------------------------


def graphql_batch_query(names: list[str], since: datetime) -> str:
    """One query that fetches base fields, latest release and recent commit count per repository."""
    parts = []
    for index, name in enumerate(names):
        if not valid_full_name(name):
            raise ValueError(f"bad repository name {name!r}")
        owner, repo = name.split("/")
        parts.append(
            f"r{index}: repository(owner: {json.dumps(owner)}, name: {json.dumps(repo)}) {{"
            " nameWithOwner stargazerCount forkCount createdAt pushedAt isArchived description"
            " primaryLanguage { name } licenseInfo { spdxId }"
            " issues(states: OPEN) { totalCount } pullRequests(states: OPEN) { totalCount }"
            " latestRelease { tagName publishedAt }"
            " defaultBranchRef { target { ... on Commit {"
            f" history(since: {json.dumps(iso_z(since))}) {{ totalCount }} }} }} }}"
            " }"
        )
    return "query { " + " ".join(parts) + " }"


def rest_shape_from_graphql(node: dict) -> dict:
    """Normalise a GraphQL repository node to the REST field names used by build_record."""
    licence = node.get("licenseInfo") or {}
    language = node.get("primaryLanguage") or {}
    return {
        "full_name": node["nameWithOwner"],
        "stargazers_count": node.get("stargazerCount"),
        "forks_count": node.get("forkCount"),
        # REST open_issues_count counts issues and pull requests together; match it.
        "open_issues_count": (node.get("issues") or {}).get("totalCount", 0)
        + (node.get("pullRequests") or {}).get("totalCount", 0),
        "created_at": node["createdAt"],
        "pushed_at": node.get("pushedAt"),
        "license": {"spdx_id": licence.get("spdxId")} if licence else None,
        "archived": node.get("isArchived"),
        "language": language.get("name"),
        "description": node.get("description"),
    }


def enrichment_from_graphql(node: dict) -> dict:
    release = node.get("latestRelease") or {}
    tag = release.get("tagName")
    commits = None
    capped = None
    history = (((node.get("defaultBranchRef") or {}).get("target")) or {}).get("history")
    if history and isinstance(history.get("totalCount"), int):
        total = history["totalCount"]
        commits = min(total, COMMITS_CAP)
        capped = total >= COMMITS_CAP
    return {
        "latest_release": tag if tag else "none",
        "latest_release_date": (release.get("publishedAt") or "")[:10] or None,
        "commits_90d": commits,
        "commits_90d_capped": capped,
    }


# ---- comparison -------------------------------------------------------------------


def find_previous(out_dir: Path) -> Path | None:
    """Newest snapshot directory next to out_dir whose name sorts before out_dir's."""
    parent = out_dir.parent
    if not parent.is_dir():
        return None
    older = sorted(
        p.name
        for p in parent.iterdir()
        if SNAPSHOT_DIR_RE.match(p.name) and p.name < out_dir.name and (p / "repos.json").is_file()
    )
    return parent / older[-1] if older else None


def apply_comparison(records: list[dict], prev_repos: list[dict], snapshot: datetime, prev_time: datetime) -> dict:
    """Fill prev_stars, star_delta, days_between and new_entrant. Returns a summary."""
    previous = {r["full_name"].lower(): r for r in prev_repos}
    days_between = round((snapshot - prev_time).total_seconds() / 86400, 1)
    new_count = 0
    for rec in records:
        old = previous.get(rec["full_name"].lower())
        rec["days_between"] = days_between
        if old is None:
            rec["new_entrant"] = True
            new_count += 1
        else:
            rec["new_entrant"] = False
            rec["prev_stars"] = old["stars"]
            rec["star_delta"] = rec["stars"] - old["stars"]
    return {"days_between": days_between, "new_entrants": new_count, "previous_repos": len(previous)}


# --------------------------------------------------------------------------- gh client


@dataclass
class Response:
    returncode: int
    stdout: str
    stderr: str

    def error_text(self) -> str:
        text = (self.stderr.strip() or self.stdout.strip()).splitlines()
        first = text[0] if text else f"exit code {self.returncode}"
        return scrub(first)[:200]


def default_runner(cmd: list[str]) -> Response:
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False
        )
    except FileNotFoundError as exc:
        raise FatalError("the GitHub CLI `gh` was not found on PATH") from exc
    return Response(proc.returncode, proc.stdout, proc.stderr)


class GhClient:
    """Calls GitHub through `gh api`, paces search calls, waits out rate limits, records failures."""

    def __init__(self, runner=default_runner, sleep=time.sleep, monotonic=time.monotonic, wall=time.time, log=None):
        self.runner = runner
        self.sleep = sleep
        self.monotonic = monotonic
        self.wall = wall
        self.log = log or (lambda message: None)
        self.calls = {"search": 0, "graphql": 0, "rest": 0, "rate_limit": 0}
        self.failures: list[dict] = []
        self._last_search: float | None = None

    @property
    def total_calls(self) -> int:
        return sum(self.calls.values())

    def fail(self, label: str, message: str) -> None:
        self.failures.append({"what": scrub(label), "error": scrub(message)[:200]})
        self.log(f"FAILURE {label}: {message}")

    def _pace_search(self) -> None:
        if self._last_search is not None:
            wait = SEARCH_GAP_SECONDS - (self.monotonic() - self._last_search)
            if wait > 0:
                self.sleep(wait)
        self._last_search = self.monotonic()

    def _wait_for_reset(self, resource: str) -> None:
        """Sleep until the rate-limit window of `resource` resets (a fixed backoff for secondary limits)."""
        self.calls["rate_limit"] += 1
        resp = self.runner(["gh", "api", "rate_limit"])
        wait = 60.0
        try:
            info = json.loads(resp.stdout)["resources"][resource]
            if info["remaining"] <= 0:
                wait = float(info["reset"]) - self.wall()
        except (ValueError, KeyError, TypeError):
            pass
        wait = min(max(wait, 1.0) + 1.0, MAX_RATE_WAIT_SECONDS)
        self.log(f"rate limited on {resource}: waiting {wait:.0f} s")
        self.sleep(wait)
        if resource == "search":
            self._last_search = self.monotonic()

    def call(self, kind: str, args: list[str], label: str) -> Response | None:
        """Run `gh api *args`. Returns the response, or None when rate-limit retries ran out."""
        resource = {"search": "search", "graphql": "graphql"}.get(kind, "core")
        for attempt in range(RATE_RETRIES + 1):
            if kind == "search":
                self._pace_search()
            self.calls[kind] += 1
            resp = self.runner(["gh", "api", *args])
            if is_auth_error(resp.returncode, resp.stdout, resp.stderr):
                raise FatalError("gh is not authenticated: run `gh auth login`")
            if is_rate_limited(resp.returncode, resp.stdout, resp.stderr):
                if attempt < RATE_RETRIES:
                    self._wait_for_reset(resource)
                    continue
                self.fail(label, f"still rate limited after {RATE_RETRIES} retries")
                return None
            return resp
        return None  # unreachable

    # -- typed calls

    def search(self, label: str, q: str, per_page: int, page: int) -> dict | None:
        resp = self.call(
            "search",
            ["search/repositories", "--method", "GET", "-f", f"q={q}", "-f", "sort=stars", "-f", "order=desc",
             "-f", f"per_page={per_page}", "-f", f"page={page}"],
            label,
        )
        if resp is None:
            return None
        if resp.returncode != 0:
            self.fail(label, resp.error_text())
            return None
        try:
            data = json.loads(resp.stdout)
        except json.JSONDecodeError:
            self.fail(label, "search returned invalid JSON")
            return None
        if not isinstance(data, dict) or not isinstance(data.get("items"), list):
            self.fail(label, "search response has no items list")
            return None
        return data

    def graphql(self, label: str, query: str, count: int) -> dict[int, dict | None]:
        """Run a batched repository query. Returns {index: node or None}; failures are recorded."""
        resp = self.call("graphql", ["graphql", "-f", f"query={query}"], label)
        if resp is None:
            return {}
        try:
            payload = json.loads(resp.stdout)
        except json.JSONDecodeError:
            self.fail(label, resp.error_text() if resp.returncode else "graphql returned invalid JSON")
            return {}
        data = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(data, dict):
            errors = payload.get("errors") if isinstance(payload, dict) else None
            message = errors[0].get("message", "unknown error") if errors else resp.error_text()
            self.fail(label, str(message))
            return {}
        return {i: data.get(f"r{i}") for i in range(count)}

    def contributors(self, full_name: str) -> int | None:
        label = f"contributors {full_name}"
        resp = self.call("rest", ["-i", f"repos/{full_name}/contributors?per_page=1&anon=true"], label)
        if resp is None:
            return None
        status, headers, body = parse_http_response(resp.stdout)
        count = contributors_from_response(status, headers, body)
        if count is None:
            detail = ""
            try:
                parsed = json.loads(body)
                detail = parsed.get("message", "") if isinstance(parsed, dict) else ""
            except json.JSONDecodeError:
                detail = resp.error_text()
            self.fail(label, f"HTTP {status}: {detail}" if status else detail or "no response")
        return count


# --------------------------------------------------------------------------- pipeline


@dataclass
class Snapshot:
    when: datetime
    top_n: int
    thresholds: Thresholds
    search: SearchSettings
    records: list[dict]
    tables: dict[str, dict[str, list[dict]]]
    query_log: list[dict]
    notes: list[str]
    no_enrich: bool
    compare: dict | None = None
    compare_name: str | None = None


def run_snapshot(
    client: GhClient,
    config: Config,
    watch: dict[str, tuple[str, str]],
    when: datetime,
    top_n: int,
    no_enrich: bool,
    log=lambda message: None,
) -> Snapshot:
    th = config.thresholds
    cutoff_day = (when - timedelta(days=th.quiet_days + 1)).date().isoformat()
    passes = [("active", f"pushed:>={cutoff_day}")]
    if config.search.quiet_pass:
        passes.append(("quiet", f"pushed:<{cutoff_day}"))

    # key (lowercase full name) -> {"item": REST-shaped repo, "hits": {category: {queries}}, "enrich": dict|None}
    candidates: dict[str, dict] = {}
    query_log: list[dict] = []

    total_searches = sum(len(q) for q in config.queries.values()) * len(passes) * config.search.pages
    done = 0
    for category in CATEGORIES:
        for query in config.queries[category]:
            for pass_name, date_clause in passes:
                q = f"{query} stars:>={config.search.min_stars} {date_clause}"
                entry = {"category": category, "query": query, "pass": pass_name,
                         "total_count": None, "returned": 0, "incomplete": False}
                query_log.append(entry)
                for page in range(1, config.search.pages + 1):
                    done += 1
                    log(f"search {done}/{total_searches}: [{category}] {query} ({pass_name}, page {page})")
                    data = client.search(f"search [{category}] {query} ({pass_name})", q,
                                         config.search.per_page, page)
                    if data is None:
                        break
                    items = data["items"]
                    entry["total_count"] = data.get("total_count")
                    entry["returned"] += len(items)
                    entry["incomplete"] = entry["incomplete"] or bool(data.get("incomplete_results"))
                    for item in items:
                        slot = candidates.setdefault(
                            item["full_name"].lower(), {"item": item, "hits": {}, "enrich": None})
                        slot["hits"].setdefault(category, set()).add(query)
                    if len(items) < config.search.per_page:
                        break

    notes: list[str] = []
    watch_by_key: dict[str, tuple[str, str]] = {}  # resolved key -> (listed name, category)

    # Watchlist repositories the search did not return are fetched directly.
    missing = [name for key, (name, _) in watch.items() if key not in candidates]
    for key, (name, category) in watch.items():
        if key in candidates:
            watch_by_key[key] = (name, category)
    for start in range(0, len(missing), GRAPHQL_BATCH):
        batch = missing[start:start + GRAPHQL_BATCH]
        log(f"fetching {len(batch)} watchlist repositories directly")
        nodes = client.graphql("watchlist fetch", graphql_batch_query(batch, when - timedelta(days=COMMIT_WINDOW_DAYS)),
                               len(batch))
        for index, name in enumerate(batch):
            node = nodes.get(index)
            category = watch[name.lower()][1]
            if node is None:
                if nodes:
                    client.fail(f"watchlist {name}", "not found or not accessible")
                continue
            resolved = node["nameWithOwner"]
            if resolved.lower() != name.lower():
                notes.append(f"Watchlist entry {name} now resolves to {resolved}.")
            slot = candidates.setdefault(resolved.lower(), {"item": rest_shape_from_graphql(node), "hits": {}, "enrich": None})
            if slot["enrich"] is None and not no_enrich:
                slot["enrich"] = enrichment_from_graphql(node)
            watch_by_key[resolved.lower()] = (name, category)

    # Records, primary category, flags.
    records: list[dict] = []
    by_key: dict[str, dict] = {}
    for key, slot in candidates.items():
        rec = build_record(slot["item"], when, th)
        counts = {cat: len(qs) for cat, qs in slot["hits"].items()}
        watched = watch_by_key.get(key)
        rec["watchlist"] = watched is not None
        rec["category"] = choose_primary(counts, watched[1] if watched else None)
        rec["also_in"] = [c for c in CATEGORIES if counts.get(c) and c != rec["category"]]
        rec["hits"] = sum(counts.values())
        if slot["enrich"]:
            rec.update(slot["enrich"])
            rec["enriched"] = True
        records.append(rec)
        by_key[key] = rec

    tables = rank_categories(records, th.quiet_days)

    if not no_enrich:
        chosen = select_enrichment(tables, top_n)
        need = [r for r in chosen if r["latest_release"] is None]
        since = when - timedelta(days=COMMIT_WINDOW_DAYS)
        for start in range(0, len(need), GRAPHQL_BATCH):
            batch = need[start:start + GRAPHQL_BATCH]
            log(f"enriching {len(batch)} repositories (releases, commits)")
            nodes = client.graphql("enrich releases and commits",
                                   graphql_batch_query([r["full_name"] for r in batch], since), len(batch))
            for index, rec in enumerate(batch):
                node = nodes.get(index)
                if node is None:
                    if nodes:
                        client.fail(f"enrich {rec['full_name']}", "not found or not accessible")
                    continue
                rec.update(enrichment_from_graphql(node))
                rec["enriched"] = True
        for number, rec in enumerate(chosen, 1):
            log(f"contributors {number}/{len(chosen)}: {rec['full_name']}")
            rec["contributors"] = client.contributors(rec["full_name"])
            rec["enriched"] = True

    return Snapshot(when, top_n, th, config.search, records, tables, query_log, notes, no_enrich)


# --------------------------------------------------------------------------- output


TSV_COLUMNS = [
    "full_name", "category", "also_in", "watchlist", "table", "rank", "stars", "forks", "open_issues",
    "created_at", "pushed_at", "license", "archived", "language", "description", "age_days",
    "stars_per_day", "forks_per_100_stars", "days_since_push", "flags", "hits", "enriched",
    "latest_release", "latest_release_date", "commits_90d", "commits_90d_capped", "contributors",
    "prev_stars", "star_delta", "days_between", "new_entrant",
]


def tsv_cell(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return ",".join(str(v) for v in value)
    return " ".join(str(value).split())  # no tabs or newlines inside a cell


def render_tsv(records: list[dict]) -> str:
    lines = ["\t".join(TSV_COLUMNS)]
    for rec in records:
        lines.append("\t".join(tsv_cell(rec[column]) for column in TSV_COLUMNS))
    return "\n".join(lines) + "\n"


def sorted_records(snapshot: Snapshot) -> list[dict]:
    order = {c: i for i, c in enumerate(CATEGORIES)}
    return sorted(
        snapshot.records,
        key=lambda r: (order[r["category"]], r["table"] != "ranked", r["rank"]),
    )


def render_json(snapshot: Snapshot, client: GhClient, out_name: str) -> str:
    th = snapshot.thresholds
    meta = {
        "tool": "tools/gh_snapshot.py",
        "version": __version__,
        "snapshot_utc": iso_z(snapshot.when),
        "directory": out_name,
        "top_n": snapshot.top_n,
        "enrichment": not snapshot.no_enrich,
        "thresholds": {
            "quiet_days": th.quiet_days,
            "fast_growth_stars_per_day": th.fast_growth_stars_per_day,
            "low_forks_min_stars": th.low_forks_min_stars,
            "low_forks_per_100_stars": th.low_forks_per_100_stars,
        },
        "search": {
            "per_page": snapshot.search.per_page,
            "pages": snapshot.search.pages,
            "min_stars": snapshot.search.min_stars,
            "quiet_pass": snapshot.search.quiet_pass,
        },
        "commits_90d_cap": COMMITS_CAP,
        "queries": snapshot.query_log,
        "api_calls": {**client.calls, "total": client.total_calls},
        "failures": client.failures,
        "notes": snapshot.notes,
        "compare": snapshot.compare,
        "repo_count": len(snapshot.records),
    }
    head = json.dumps(meta, indent=2, ensure_ascii=False).replace("\n", "\n  ")
    rows = ",\n".join("    " + json.dumps(r, ensure_ascii=False) for r in sorted_records(snapshot))
    return '{\n  "meta": ' + head + ',\n  "repos": [\n' + rows + "\n  ]\n}\n"


def fmt_int(value: int | None) -> str:
    return "-" if value is None else f"{value:,}"


def fmt_rate(value: float | None) -> str:
    if value is None:
        return "-"
    text = f"{value:,.2f}"
    return text.rstrip("0").rstrip(".")


def change_cell(rec: dict) -> str:
    if rec["new_entrant"]:
        return "new"
    if rec["star_delta"] is None:
        return "-"
    return f"{rec['star_delta']:+,}"


def repo_cell(rec: dict) -> str:
    link = f"[{md_cell(rec['full_name'])}](https://github.com/{rec['full_name']})"
    return link + (" (w)" if rec["watchlist"] else "")


def render_category_table(rows: list[dict], with_change: bool) -> list[str]:
    head = ["Rank", "Repo", "Stars", "Forks", "Stars/day"]
    if with_change:
        head.append("Change")
    head += ["Created", "Last push", "Licence", "Flags", "Description"]
    lines = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    for rec in rows:
        cells = [str(rec["rank"]), repo_cell(rec), fmt_int(rec["stars"]), fmt_int(rec["forks"]),
                 fmt_rate(rec["stars_per_day"])]
        if with_change:
            cells.append(change_cell(rec))
        cells += [day_stamp(rec["created_at"]), day_stamp(rec["pushed_at"]),
                  md_cell(rec["license"] or "none detected"), md_cell(", ".join(rec["flags"]) or "-"),
                  md_cell(rec["description"] or "-")]
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def shown_rows(rows: list[dict], top_n: int) -> list[dict]:
    """The first N rows plus any watchlist repository ranked below N."""
    return rows[:top_n] + [r for r in rows[top_n:] if r["watchlist"]]


def render_readme(snapshot: Snapshot, client: GhClient, out_name: str, config: Config) -> str:
    th = snapshot.thresholds
    when = snapshot.when
    with_change = snapshot.compare is not None
    n_queries = len(snapshot.query_log)
    n_flagged = sum(1 for r in snapshot.records if r["flags"])
    out: list[str] = []
    add = out.append

    add(f"# GitHub landscape snapshot {out_name.removesuffix('-github')}")
    add("")
    add(f"- Snapshot time: {stamp(when)} UTC")
    add(f"- Tool: `tools/gh_snapshot.py` version {__version__}")
    distinct = sum(len(q) for q in config.queries.values())
    passes = 2 if snapshot.search.quiet_pass else 1
    add(f"- Search queries: {distinct} queries x {passes} passes = {n_queries} searches"
        f" ({snapshot.search.pages} page(s) of up to {snapshot.search.per_page} each)")
    calls = client.calls
    add(f"- API calls: {client.total_calls} (search {calls['search']}, GraphQL {calls['graphql']},"
        f" REST {calls['rest']}, rate-limit checks {calls['rate_limit']})")
    add(f"- Repositories found: {len(snapshot.records)}; flagged: {n_flagged}; failures: {len(client.failures)}")
    add(f"- Top N per category: {snapshot.top_n}; enrichment: {'off' if snapshot.no_enrich else 'on'}")
    if snapshot.compare is not None:
        c = snapshot.compare
        add(f"- Compared with `{snapshot.compare_name}`, {c['days_between']} days earlier:"
            f" {c['new_entrants']} new entrants")
    else:
        add("- Compared with: no earlier snapshot")
    add("- Data: `repos.tsv` (all columns, every repository found) and `repos.json` (same records plus run metadata)")
    add("")

    add("## How to read this")
    add("")
    add("Stars are signals, not verdicts. They measure attention, not quality, correctness or fit, and they can be"
        " bought, boosted by a viral post, or earned by a list or tutorial rather than by software. Read a"
        " number with its date and with the other columns, then read the project.")
    add("")
    add(f"- **Ranking rule:** within a category, repositories are ranked by stars among those pushed within the last"
        f" {th.quiet_days} days (whole days since the last push, at most {th.quiet_days}) and not archived."
        " Everything else goes to that category's separate *quiet or archived* table, also sorted by stars.")
    add("- **Category:** each repository has one primary category: the watchlist's if it is listed there, otherwise the"
        " category whose queries returned it most often, ties broken in the order core, agent-memory, markdown-kb,"
        " adjacent. Search hits in other categories are kept in `repos.tsv` (`also_in`).")
    add("- **Relevance is not judged.** Queries match topics and keywords, and the ranking then promotes whatever is"
        " most starred, including awesome lists, tutorials and general agent tools that merely mention the subject."
        " Read the description before treating an entry as in scope.")
    add("- **(w)** marks a watchlist repository, tracked whatever the search returns. It is shown even below the top N.")
    add("- **Stars/day** is stars divided by age in days (at least 1). It is an average over the repository's life.")
    add(f"- **Flags** are heuristics with editable thresholds (`tools/snapshot/queries.toml`), not accusations:")
    add("")
    add("| Flag | Rule | What it suggests, and what it does not |")
    add("|---|---|---|")
    add("| `archived` | the repository is archived on GitHub | It no longer accepts changes. It does not say the ideas are obsolete. |")
    add(f"| `quiet` | more than {th.quiet_days} days since the last push | Little recent development. Mature, finished projects can look like this. |")
    add(f"| `fast-growth` | stars/day >= {th.fast_growth_stars_per_day:g} | Unusually rapid attention. It can be organic (a viral launch) or not; check the star history and who is starring before drawing a conclusion. |")
    add(f"| `low-forks` | stars >= {th.low_forks_min_stars:,} and forks per 100 stars < {th.low_forks_per_100_stars:g} | Many stars but few forks. A common pattern for lists and for bought or boosted stars, and also for end-user apps nobody forks. |")
    add("")
    add("- **Open issues** in `repos.tsv` count issues and pull requests together (GitHub's `open_issues_count`).")
    add(f"- **Commits (90 d)** counts commits on the default branch in the last {COMMIT_WINDOW_DAYS} days and is **capped at"
        f" {COMMITS_CAP}**: `{COMMITS_CAP}+` means {COMMITS_CAP} or more.")
    add("- **Contributors** comes from the last page number of the contributors list (including anonymous ones). GitHub refuses it for some very large repositories; those show `-` and appear under Failures.")
    add("- **Licence** is GitHub's detection from the repository's LICENSE file (SPDX id). `NOASSERTION` means a licence file exists that GitHub could not match to one SPDX id; read it before reusing anything.")
    add("")

    if with_change:
        add("## Change since the previous snapshot")
        add("")
        c = snapshot.compare
        add(f"Previous snapshot `{snapshot.compare_name}`, {c['days_between']} days earlier, held {c['previous_repos']} repositories."
            f" {c['new_entrants']} repositories in this snapshot were not in it (marked `new`)."
            " The `Change` column is stars now minus stars then; compare it with the days between, not with the rank.")
        add("")

    for cat in CATEGORIES:
        ranked = snapshot.tables[cat]["ranked"]
        quiet = snapshot.tables[cat]["quiet"]
        add(f"## {cat}")
        add("")
        if config.descriptions.get(cat):
            add(config.descriptions[cat] + ".")
            add("")
        add(f"### {cat}: ranked (pushed within {th.quiet_days} days)")
        add("")
        rows = shown_rows(ranked, snapshot.top_n)
        if rows:
            out.extend(render_category_table(rows, with_change))
            if len(ranked) > len(rows):
                add("")
                add(f"{len(ranked) - len(rows)} more ranked repositories are in `repos.tsv`.")
        else:
            add("No repositories.")
        add("")
        add(f"### {cat}: quiet or archived")
        add("")
        rows = shown_rows(quiet, snapshot.top_n)
        if rows:
            out.extend(render_category_table(rows, with_change))
            if len(quiet) > len(rows):
                add("")
                add(f"{len(quiet) - len(rows)} more quiet or archived repositories are in `repos.tsv`.")
        else:
            add("No repositories.")
        add("")

    if not snapshot.no_enrich:
        add("## Releases, recent commits and contributors")
        add("")
        add(f"For the top {snapshot.top_n} ranked repositories per category and every watchlist repository."
            f" Commits are on the default branch in the last {COMMIT_WINDOW_DAYS} days, capped at {COMMITS_CAP}.")
        add("")
        add("| Category | Repo | Latest release | Commits (90 d) | Contributors |")
        add("|---|---|---|---|---|")
        for rec in sorted_records(snapshot):
            if not rec["enriched"]:
                continue
            release = rec["latest_release"] or "-"
            if rec["latest_release_date"]:
                release += f" ({day_stamp(rec['latest_release_date'])})"
            commits = "-" if rec["commits_90d"] is None else (
                f"{COMMITS_CAP}+" if rec["commits_90d_capped"] else str(rec["commits_90d"]))
            add(f"| {rec['category']} | {repo_cell(rec)} | {md_cell(release)} | {commits} | {fmt_int(rec['contributors'])} |")
        add("")

    add("## Search queries")
    add("")
    add("| Category | Query | Pass | Matches reported by GitHub | Returned |")
    add("|---|---|---|---|---|")
    for entry in snapshot.query_log:
        returned = str(entry["returned"]) + (" (incomplete)" if entry["incomplete"] else "")
        add(f"| {entry['category']} | `{md_cell(entry['query'])}` | {entry['pass']} | {fmt_int(entry['total_count'])} | {returned} |")
    add("")
    add("Each query is run with `stars:>=" + str(snapshot.search.min_stars) + "`; the *active* pass adds a `pushed:` date"
        " qualifier for the recent window and the *quiet* pass for the older one. A result list is capped at"
        f" {snapshot.search.per_page * snapshot.search.pages} per pass, so the quiet tables are a sample of what exists,"
        " not a census.")
    add("")

    if snapshot.notes:
        add("## Notes")
        add("")
        for note in snapshot.notes:
            add(f"- {md_cell(note)}")
        add("")

    add("## Failures")
    add("")
    if client.failures:
        add("| What | Error |")
        add("|---|---|")
        for failure in client.failures:
            add(f"| {md_cell(failure['what'])} | {md_cell(failure['error'])} |")
    else:
        add("None.")
    add("")
    return "\n".join(out)


# --------------------------------------------------------------------------- main


def display_path(path: Path) -> str:
    """A path for messages and files: relative to the repository root, else just the name."""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.name


def load_previous(prev_dir: Path) -> tuple[datetime, list[dict]]:
    try:
        data = json.loads((prev_dir / "repos.json").read_text(encoding="utf-8"))
        return parse_ts(data["meta"]["snapshot_utc"]), data["repos"]
    except (OSError, ValueError, KeyError) as exc:
        raise FatalError(f"cannot read previous snapshot {prev_dir.name}: {exc}") from exc


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="gh_snapshot.py",
        description="Write a dated GitHub snapshot of knowledge-graph and agent-memory projects.",
    )
    parser.add_argument("--out", metavar="DIR",
                        help="output directory (default: kb-kg/landscape/<UTC YYYYMMDD_HHMM>-github)")
    parser.add_argument("--top", type=int, default=25, metavar="N",
                        help="repositories per category in the README tables and in enrichment (default: 25)")
    parser.add_argument("--no-enrich", action="store_true",
                        help="skip latest release, commits in 90 days and contributor counts")
    parser.add_argument("--compare", metavar="PREV_DIR",
                        help="earlier snapshot directory to compare with (default: the newest earlier one next to"
                             " the output directory; 'none' disables the comparison)")
    args = parser.parse_args(argv)
    if args.top < 1:
        parser.error("--top must be at least 1")
    return args


def main(argv: list[str] | None = None, *, client: GhClient | None = None, now: datetime | None = None) -> int:
    args = parse_args(argv)

    def stderr_log(message: str) -> None:
        print(message, file=sys.stderr, flush=True)

    # A client passed in by a caller (tests) keeps its own, usually silent, log.
    client = client or GhClient(log=stderr_log)
    log = client.log

    try:
        config = load_config(CONFIG_DIR / "queries.toml")
        watch = parse_watchlist((CONFIG_DIR / "watchlist.txt").read_text(encoding="utf-8"))
        when = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).replace(second=0, microsecond=0)
        out_dir = Path(args.out) if args.out else DEFAULT_LANDSCAPE / f"{when:%Y%m%d_%H%M}-github"
        if out_dir.exists() and any(out_dir.iterdir()):
            raise FatalError(f"output directory {display_path(out_dir)} exists and is not empty")

        prev_dir: Path | None
        if args.compare is None:
            prev_dir = find_previous(out_dir)
        elif args.compare.lower() == "none":
            prev_dir = None
        else:
            prev_dir = Path(args.compare)
        previous = load_previous(prev_dir) if prev_dir else None

        snapshot = run_snapshot(client, config, watch, when, args.top, args.no_enrich, log=log)
        if not snapshot.records:
            raise FatalError("no repositories found: every search failed (see messages above)")
        if previous and prev_dir:
            snapshot.compare = apply_comparison(snapshot.records, previous[1], when, previous[0])
            snapshot.compare_name = prev_dir.name

        out_dir.mkdir(parents=True, exist_ok=True)
        records = sorted_records(snapshot)
        (out_dir / "repos.tsv").write_text(render_tsv(records), encoding="utf-8")
        (out_dir / "repos.json").write_text(render_json(snapshot, client, out_dir.name), encoding="utf-8")
        (out_dir / "README.md").write_text(render_readme(snapshot, client, out_dir.name, config), encoding="utf-8")
    except FatalError as exc:
        log(f"error: {exc}")
        return 2

    log(f"wrote {display_path(out_dir)}: {len(snapshot.records)} repositories, {client.total_calls} API calls,"
        f" {len(client.failures)} failures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
