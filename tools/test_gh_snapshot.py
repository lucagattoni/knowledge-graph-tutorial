"""Tests for tools/gh_snapshot.py. Standard library only, fake data, no network.

Run from the repository root:

    uv run python -m unittest tools/test_gh_snapshot.py
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gh_snapshot as gs  # noqa: E402

SNAP = datetime(2026, 10, 30, 19, 0, tzinfo=timezone.utc)
TH = gs.Thresholds()


def iso(days_ago: float) -> str:
    return gs.iso_z(SNAP - timedelta(days=days_ago))


def item(name: str, stars: int = 1000, forks: int = 100, created_days_ago: float = 365,
         pushed_days_ago: float = 5, archived: bool = False, **extra) -> dict:
    """A repository object in the shape GitHub's REST API returns."""
    data = {
        "full_name": name,
        "stargazers_count": stars,
        "forks_count": forks,
        "open_issues_count": 7,
        "created_at": iso(created_days_ago),
        "pushed_at": iso(pushed_days_ago),
        "license": {"spdx_id": "MIT"},
        "archived": archived,
        "language": "Python",
        "description": "A fake repository",
    }
    data.update(extra)
    return data


def rec(name: str, category: str = "core", **kwargs) -> dict:
    record = gs.build_record(item(name, **kwargs), SNAP, TH)
    record["category"] = category
    return record


class FlagTests(unittest.TestCase):
    def test_archived(self):
        self.assertIn("archived", rec("a/b", archived=True)["flags"])
        self.assertNotIn("archived", rec("a/b")["flags"])

    def test_quiet_boundary_is_strictly_more_than_90_days(self):
        self.assertNotIn("quiet", rec("a/b", pushed_days_ago=90)["flags"])
        self.assertIn("quiet", rec("a/b", pushed_days_ago=91)["flags"])

    def test_quiet_uses_whole_days(self):
        # 90 days 23 hours is still 90 whole days; 91 days 0 hours is 91.
        self.assertNotIn("quiet", rec("a/b", pushed_days_ago=90 + 23 / 24)["flags"])
        self.assertIn("quiet", rec("a/b", pushed_days_ago=91)["flags"])

    def test_fast_growth_boundary_is_inclusive(self):
        self.assertIn("fast-growth", rec("a/b", stars=15000, created_days_ago=100)["flags"])  # exactly 150/day
        self.assertNotIn("fast-growth", rec("a/b", stars=14999, created_days_ago=100)["flags"])  # 149.99/day

    def test_fast_growth_young_repository_uses_at_least_one_day(self):
        record = rec("a/b", stars=400, created_days_ago=0.2)
        self.assertEqual(record["age_days"], 0)
        self.assertEqual(record["stars_per_day"], 400.0)
        self.assertIn("fast-growth", record["flags"])

    def test_low_forks_needs_enough_stars_and_a_ratio_under_the_limit(self):
        self.assertIn("low-forks", rec("a/b", stars=5000, forks=149)["flags"])  # 2.98 per 100
        self.assertNotIn("low-forks", rec("a/b", stars=5000, forks=150)["flags"])  # exactly 3.0
        self.assertNotIn("low-forks", rec("a/b", stars=4999, forks=0)["flags"])  # below the star floor

    def test_thresholds_are_editable(self):
        strict = gs.Thresholds(quiet_days=30, fast_growth_stars_per_day=1, low_forks_min_stars=10,
                               low_forks_per_100_stars=50)
        record = gs.build_record(item("a/b", stars=100, forks=10, created_days_ago=10, pushed_days_ago=31),
                                 SNAP, strict)
        self.assertEqual(record["flags"], ["quiet", "fast-growth", "low-forks"])

    def test_flag_order_and_combination(self):
        record = rec("a/b", stars=90000, forks=100, created_days_ago=100, pushed_days_ago=200, archived=True)
        self.assertEqual(record["flags"], ["archived", "quiet", "fast-growth", "low-forks"])

    def test_zero_stars_does_not_divide_by_zero(self):
        record = rec("a/b", stars=0, forks=0)
        self.assertIsNone(record["forks_per_100_stars"])
        self.assertEqual(record["flags"], [])


class MetricTests(unittest.TestCase):
    def test_derived_metrics(self):
        record = rec("a/b", stars=2000, forks=300, created_days_ago=200, pushed_days_ago=12)
        self.assertEqual(record["age_days"], 200)
        self.assertEqual(record["stars_per_day"], 10.0)
        self.assertEqual(record["forks_per_100_stars"], 15.0)
        self.assertEqual(record["days_since_push"], 12)
        self.assertEqual(record["license"], "MIT")

    def test_missing_licence_is_none(self):
        self.assertIsNone(rec("a/b", license=None)["license"])

    def test_description_is_one_line_and_at_most_120_characters(self):
        long = "x" * 300
        self.assertEqual(len(gs.clean_description(long)), 120)
        self.assertTrue(gs.clean_description(long).endswith("..."))
        self.assertEqual(gs.clean_description("two\nlines\tand   spaces"), "two lines and spaces")
        self.assertEqual(gs.clean_description(None), "")

    def test_description_is_scrubbed_of_emails_paths_and_tokens(self):
        # The path is built from parts so that this file passes the public-safety gate itself.
        text = "mail me at someone@example.com or see /" + "Users/someone/code and ghp_" + "a" * 30
        cleaned = gs.clean_description(text)
        self.assertNotIn("@", cleaned)
        self.assertNotIn("/Users", cleaned)
        self.assertNotIn("ghp_", cleaned)

    def test_markdown_cell_escapes_pipes_and_html(self):
        self.assertEqual(gs.md_cell("a | b <c>"), "a \\| b &lt;c&gt;")


class RankingTests(unittest.TestCase):
    def ranked_names(self, records, cat="core"):
        return [r["full_name"] for r in gs.rank_categories(records, 90)[cat]["ranked"]]

    def test_boundary_day_90_is_ranked_and_day_91_is_quiet(self):
        records = [rec("a/day90", pushed_days_ago=90), rec("a/day91", pushed_days_ago=91)]
        tables = gs.rank_categories(records, 90)
        self.assertEqual([r["full_name"] for r in tables["core"]["ranked"]], ["a/day90"])
        self.assertEqual([r["full_name"] for r in tables["core"]["quiet"]], ["a/day91"])

    def test_a_famous_quiet_repository_never_outranks_an_active_one(self):
        records = [
            rec("big/quiet", stars=90000, pushed_days_ago=400),
            rec("mid/active", stars=3000, pushed_days_ago=10),
            rec("small/active", stars=200, pushed_days_ago=1),
        ]
        tables = gs.rank_categories(records, 90)
        self.assertEqual([r["full_name"] for r in tables["core"]["ranked"]], ["mid/active", "small/active"])
        self.assertEqual([r["full_name"] for r in tables["core"]["quiet"]], ["big/quiet"])
        self.assertEqual([r["rank"] for r in tables["core"]["ranked"]], [1, 2])
        self.assertEqual({r["table"] for r in tables["core"]["quiet"]}, {"quiet"})

    def test_archived_repository_goes_to_the_quiet_or_archived_table_even_if_pushed_recently(self):
        records = [rec("a/archived", stars=9000, pushed_days_ago=3, archived=True), rec("a/live", stars=10)]
        tables = gs.rank_categories(records, 90)
        self.assertEqual([r["full_name"] for r in tables["core"]["ranked"]], ["a/live"])
        self.assertEqual([r["full_name"] for r in tables["core"]["quiet"]], ["a/archived"])

    def test_ties_break_by_name_and_categories_are_separate(self):
        records = [rec("b/one", stars=50), rec("a/one", stars=50), rec("z/mem", "agent-memory", stars=1)]
        self.assertEqual(self.ranked_names(records), ["a/one", "b/one"])
        self.assertEqual(self.ranked_names(records, "agent-memory"), ["z/mem"])
        self.assertEqual(self.ranked_names(records, "adjacent"), [])

    def test_enrichment_set_is_top_n_ranked_plus_all_watchlist(self):
        records = [
            rec("a/first", stars=500), rec("a/second", stars=400), rec("a/third", stars=300),
            rec("a/quiet", stars=9999, pushed_days_ago=500),
            rec("w/low", stars=5),
            rec("w/quiet", stars=7, pushed_days_ago=500),
        ]
        for r in records:
            r["watchlist"] = r["full_name"].startswith("w/")
        tables = gs.rank_categories(records, 90)
        chosen = {r["full_name"] for r in gs.select_enrichment(tables, 2)}
        self.assertEqual(chosen, {"a/first", "a/second", "w/low", "w/quiet"})

    def test_readme_rows_show_top_n_plus_watchlist_below_it(self):
        rows = [rec(f"a/r{i}", stars=1000 - i) for i in range(5)]
        rows[4]["watchlist"] = True
        for i, r in enumerate(rows, 1):
            r["rank"] = i
        shown = [r["full_name"] for r in gs.shown_rows(rows, 2)]
        self.assertEqual(shown, ["a/r0", "a/r1", "a/r4"])


class PrimaryCategoryTests(unittest.TestCase):
    def test_watchlist_wins_over_hits(self):
        self.assertEqual(gs.choose_primary({"core": 5, "adjacent": 2}, "agent-memory"), "agent-memory")

    def test_most_hits_wins(self):
        self.assertEqual(gs.choose_primary({"core": 1, "markdown-kb": 3, "adjacent": 2}, None), "markdown-kb")

    def test_ties_break_in_category_order(self):
        self.assertEqual(gs.choose_primary({"adjacent": 2, "agent-memory": 2}, None), "agent-memory")
        self.assertEqual(gs.choose_primary({"adjacent": 2, "core": 2, "markdown-kb": 2}, None), "core")
        self.assertEqual(gs.choose_primary({"adjacent": 1, "markdown-kb": 1}, None), "markdown-kb")

    def test_single_hit(self):
        self.assertEqual(gs.choose_primary({"adjacent": 1}, None), "adjacent")


class LinkHeaderTests(unittest.TestCase):
    LINK = ('<https://api.github.com/repositories/840056306/contributors?per_page=1&anon=true&page=2>; rel="next", '
            '<https://api.github.com/repositories/840056306/contributors?per_page=1&anon=true&page=64>; rel="last"')

    def test_last_page(self):
        self.assertEqual(gs.parse_last_page(self.LINK), 64)

    def test_last_page_absent(self):
        self.assertIsNone(gs.parse_last_page(None))
        self.assertIsNone(gs.parse_last_page(""))
        only_prev = '<https://api.github.com/x?page=1>; rel="prev"'
        self.assertIsNone(gs.parse_last_page(only_prev))

    def test_last_page_with_page_param_not_last_in_url(self):
        link = '<https://api.github.com/x?page=12&per_page=1&anon=true>; rel="last"'
        self.assertEqual(gs.parse_last_page(link), 12)

    def test_parse_http_response_crlf_headers(self):
        text = ("HTTP/2.0 200 OK\nContent-Type: application/json\r\nLink: " + self.LINK + "\r\n"
                "X-Ratelimit-Remaining: 4000\r\n\r\n[{\"login\":\"x\"}]")
        status, headers, body = gs.parse_http_response(text)
        self.assertEqual(status, 200)
        self.assertEqual(headers["link"], self.LINK)
        self.assertEqual(body, '[{"login":"x"}]')

    def test_parse_http_response_lf_only_and_two_blocks(self):
        text = "HTTP/1.1 100 Continue\n\nHTTP/2.0 403 Forbidden\nRetry-After: 30\n\n{\"message\":\"no\"}"
        status, headers, body = gs.parse_http_response(text)
        self.assertEqual(status, 403)
        self.assertEqual(headers["retry-after"], "30")
        self.assertEqual(body, '{"message":"no"}')

    def test_contributors_count_from_link_header(self):
        status, headers, body = gs.parse_http_response("HTTP/2.0 200 OK\nLink: " + self.LINK + "\n\n[{}]")
        self.assertEqual(gs.contributors_from_response(status, headers, body), 64)

    def test_contributors_count_without_link_is_the_list_length(self):
        self.assertEqual(gs.contributors_from_response(200, {}, '[{"login":"x"}]'), 1)
        self.assertEqual(gs.contributors_from_response(200, {}, "[]"), 0)
        self.assertEqual(gs.contributors_from_response(204, {}, ""), 0)

    def test_contributors_unavailable(self):
        self.assertIsNone(gs.contributors_from_response(403, {}, '{"message":"list too large"}'))
        self.assertIsNone(gs.contributors_from_response(200, {}, "not json"))
        self.assertIsNone(gs.contributors_from_response(None, {}, ""))


class GraphqlTests(unittest.TestCase):
    NODE = {
        "nameWithOwner": "Org/Repo", "stargazerCount": 10, "forkCount": 2, "createdAt": iso(30), "pushedAt": iso(1),
        "isArchived": False, "description": "d", "primaryLanguage": {"name": "Go"}, "licenseInfo": {"spdxId": "MIT"},
        "issues": {"totalCount": 3}, "pullRequests": {"totalCount": 4},
        "latestRelease": {"tagName": "v1.2.3", "publishedAt": "2026-10-20T17:25:21Z"},
        "defaultBranchRef": {"target": {"history": {"totalCount": 123}}},
    }

    def test_query_has_one_alias_per_repository_and_balanced_braces(self):
        query = gs.graphql_batch_query(["a/b", "c/d.e"], SNAP)
        self.assertIn('r0: repository(owner: "a", name: "b")', query)
        self.assertIn('r1: repository(owner: "c", name: "d.e")', query)
        self.assertEqual(query.count("{"), query.count("}"))

    def test_query_rejects_names_that_could_inject(self):
        with self.assertRaises(ValueError):
            gs.graphql_batch_query(['a/b") { x } y: repository(owner: "c', "d/e"], SNAP)

    def test_rest_shape_matches_rest_fields_and_sums_issues_and_pulls(self):
        shaped = gs.rest_shape_from_graphql(self.NODE)
        self.assertEqual(shaped["open_issues_count"], 7)
        self.assertEqual(shaped["license"], {"spdx_id": "MIT"})
        record = gs.build_record(shaped, SNAP, TH)
        self.assertEqual(record["stars"], 10)
        self.assertEqual(record["language"], "Go")

    def test_commit_count_is_capped_at_100_and_says_so(self):
        enrich = gs.enrichment_from_graphql(self.NODE)
        self.assertEqual(enrich["commits_90d"], 100)
        self.assertTrue(enrich["commits_90d_capped"])
        self.assertEqual(enrich["latest_release"], "v1.2.3")
        self.assertEqual(enrich["latest_release_date"], "2026-10-20")

    def test_below_the_cap_is_exact_and_no_release_is_none(self):
        node = dict(self.NODE, latestRelease=None, defaultBranchRef={"target": {"history": {"totalCount": 42}}})
        enrich = gs.enrichment_from_graphql(node)
        self.assertEqual((enrich["commits_90d"], enrich["commits_90d_capped"]), (42, False))
        self.assertEqual((enrich["latest_release"], enrich["latest_release_date"]), ("none", None))

    def test_empty_repository_has_unknown_commits(self):
        enrich = gs.enrichment_from_graphql(dict(self.NODE, defaultBranchRef=None))
        self.assertIsNone(enrich["commits_90d"])


class ClientTests(unittest.TestCase):
    def make_client(self, responses):
        calls, sleeps = [], []
        clock = {"t": 1000.0}

        def runner(cmd):
            calls.append(cmd)
            return responses.pop(0)

        def sleep(seconds):
            sleeps.append(seconds)
            clock["t"] += seconds

        client = gs.GhClient(runner=runner, sleep=sleep, monotonic=lambda: clock["t"], wall=lambda: 5000.0)
        return client, calls, sleeps

    def ok(self, payload):
        return gs.Response(0, json.dumps(payload), "")

    def test_search_calls_are_spaced_at_least_2_5_seconds(self):
        empty = {"total_count": 0, "items": []}
        client, calls, sleeps = self.make_client([self.ok(empty), self.ok(empty), self.ok(empty)])
        for _ in range(3):
            client.search("x", "q", 100, 1)
        self.assertEqual(len(sleeps), 2)
        self.assertTrue(all(s >= 2.5 for s in sleeps))
        self.assertEqual(client.calls["search"], 3)

    def test_rate_limit_waits_for_reset_and_retries(self):
        limited = gs.Response(1, "", "gh: API rate limit exceeded for user (HTTP 403)")
        reset = self.ok({"resources": {"search": {"remaining": 0, "reset": 5030}}})
        good = self.ok({"total_count": 1, "items": [{"full_name": "a/b"}]})
        client, calls, sleeps = self.make_client([limited, reset, good])
        data = client.search("x", "q", 100, 1)
        self.assertEqual(data["items"][0]["full_name"], "a/b")
        self.assertIn(31.0, sleeps)  # reset in 30 s, plus one second of margin
        self.assertEqual(client.failures, [])
        self.assertEqual(client.calls["rate_limit"], 1)

    def test_rate_limit_that_never_clears_is_recorded_as_a_failure(self):
        limited = gs.Response(1, "", "You have exceeded a secondary rate limit")
        reset = self.ok({"resources": {"search": {"remaining": 5, "reset": 0}}})
        script = [limited, reset] * gs.RATE_RETRIES + [limited]
        client, _, sleeps = self.make_client(script)
        self.assertIsNone(client.search("my query", "q", 100, 1))
        self.assertEqual(len(client.failures), 1)
        self.assertIn("my query", client.failures[0]["what"])
        self.assertIn(60 + 1, sleeps)  # secondary limit: fixed backoff

    def test_other_errors_are_recorded_not_swallowed(self):
        bad = gs.Response(1, '{"message":"Validation Failed"}', "gh: Validation Failed (HTTP 422)")
        client, _, _ = self.make_client([bad])
        self.assertIsNone(client.search("label", "q", 100, 1))
        self.assertEqual(client.failures, [{"what": "label", "error": "gh: Validation Failed (HTTP 422)"}])

    def test_unauthenticated_is_fatal(self):
        bad = gs.Response(4, "", "To get started with GitHub CLI, please run:  gh auth login")
        client, _, _ = self.make_client([bad])
        with self.assertRaises(gs.FatalError):
            client.search("label", "q", 100, 1)

    def test_search_uses_get_so_gh_does_not_post(self):
        client, calls, _ = self.make_client([self.ok({"items": []})])
        client.search("x", "topic:a", 100, 1)
        self.assertIn("--method", calls[0])
        self.assertEqual(calls[0][calls[0].index("--method") + 1], "GET")
        self.assertEqual(calls[0][:3], ["gh", "api", "search/repositories"])

    def test_contributors_reads_the_link_header_via_include(self):
        text = ("HTTP/2.0 200 OK\r\nLink: " + LinkHeaderTests.LINK + "\r\n\r\n[{}]")
        client, calls, _ = self.make_client([gs.Response(0, text, "")])
        self.assertEqual(client.contributors("a/b"), 64)
        self.assertIn("-i", calls[0])
        self.assertIn("per_page=1&anon=true", calls[0][-1])

    def test_contributors_refused_is_recorded(self):
        text = 'HTTP/2.0 403 Forbidden\r\n\r\n{"message":"The list is too large to list contributors"}'
        client, _, _ = self.make_client([gs.Response(1, text, "gh: too large (HTTP 403)")])
        self.assertIsNone(client.contributors("a/b"))
        self.assertIn("too large", client.failures[0]["error"])


class ComparisonTests(unittest.TestCase):
    def test_star_delta_days_between_and_new_entrants(self):
        before = SNAP - timedelta(days=7, hours=12)
        old = [{"full_name": "A/One", "stars": 100}]
        records = [rec("a/one", stars=130), rec("a/new", stars=50)]
        summary = gs.apply_comparison(records, old, SNAP, before)
        self.assertEqual(summary, {"days_between": 7.5, "new_entrants": 1, "previous_repos": 1})
        self.assertEqual((records[0]["star_delta"], records[0]["prev_stars"], records[0]["new_entrant"]), (30, 100, False))
        self.assertEqual((records[1]["star_delta"], records[1]["new_entrant"]), (None, True))
        self.assertEqual(records[1]["days_between"], 7.5)

    def test_find_previous_picks_the_newest_earlier_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("20261001_1000-github", "20261015_0900-github", "20261101_0000-github"):
                (root / name).mkdir()
                (root / name / "repos.json").write_text("{}")
            (root / "20261020_0000-github").mkdir()  # no repos.json: not a snapshot
            (root / "notes").mkdir()
            found = gs.find_previous(root / "20261030_1900-github")
            self.assertEqual(found.name, "20261015_0900-github")
            self.assertIsNone(gs.find_previous(root / "20260901_0000-github"))


class ConfigTests(unittest.TestCase):
    def test_shipped_config_loads(self):
        config = gs.load_config(gs.CONFIG_DIR / "queries.toml")
        self.assertEqual(set(config.queries), set(gs.CATEGORIES))
        self.assertEqual(config.thresholds, gs.Thresholds())
        self.assertGreaterEqual(config.search.per_page, 1)

    def test_shipped_watchlist_has_valid_categories_and_the_july_projects(self):
        watch = gs.parse_watchlist((gs.CONFIG_DIR / "watchlist.txt").read_text(encoding="utf-8"))
        july = ["microsoft/graphrag", "HKUDS/LightRAG", "getzep/graphiti", "OSU-NLP-Group/HippoRAG",
                "circlemind-ai/fast-graphrag", "LHRLAB/Graph-R1", "datastax/graph-rag", "vitali87/code-graph-rag",
                "HKUDS/MiniRAG", "DEEP-PolyU/LinearRAG", "chensyCN/LogicRAG", "TencentCloudADP/youtu-graphrag"]
        for name in july:
            self.assertIn(name.lower(), watch)
        self.assertTrue(all(cat in gs.CATEGORIES for _, cat in watch.values()))

    def test_watchlist_parsing_rejects_bad_lines(self):
        for bad in ("owner/repo core", "owner/repo\tnonsense", "no-slash\tcore", "a/b\tcore\na/B\tcore"):
            with self.assertRaises(gs.FatalError, msg=bad):
                gs.parse_watchlist(bad)
        self.assertEqual(gs.parse_watchlist("# c\n\nA/b\tcore\n"), {"a/b": ("A/b", "core")})


# ---- end to end with a fake `gh` -------------------------------------------------

FAKE_NOT_FOUND = "stanford-oval/storm"


def fake_gh(cmd: list[str]) -> gs.Response:
    """Answers the four kinds of call the tool makes, with fixed fake data."""
    kind = cmd[2]
    if kind == "rate_limit":
        return gs.Response(0, json.dumps({"resources": {"search": {"remaining": 30, "reset": 0}}}), "")
    if kind == "search/repositories":
        q = next(a for a in cmd if a.startswith("q="))[2:]
        active = "pushed:>=" in q
        items = []
        if active:
            items.append(item("acme/alpha", stars=5000, forks=900, created_days_ago=400, pushed_days_ago=3))
            if "topic:agent-memory" in q or "topic:llm-memory" in q:
                items.append(item("acme/bravo", stars=800, forks=80, created_days_ago=100, pushed_days_ago=10))
        elif "topic:graph-database" in q:
            items.append(item("acme/old", stars=9000, forks=1000, created_days_ago=3000, pushed_days_ago=500))
        return gs.Response(0, json.dumps({"total_count": len(items), "incomplete_results": False, "items": items}), "")
    if kind == "graphql":
        query = next(a for a in cmd if a.startswith("query="))
        names = re.findall(r'repository\(owner: "([^"]+)", name: "([^"]+)"\)', query)
        data, errors = {}, []
        for index, (owner, repo) in enumerate(names):
            full = f"{owner}/{repo}"
            if full == FAKE_NOT_FOUND:
                data[f"r{index}"] = None
                errors.append({"type": "NOT_FOUND", "path": [f"r{index}"], "message": f"Could not resolve {full}"})
                continue
            data[f"r{index}"] = {
                "nameWithOwner": full, "stargazerCount": 2000 + index, "forkCount": 300, "createdAt": iso(500),
                "pushedAt": iso(2), "isArchived": False, "description": "watch me | now",
                "primaryLanguage": {"name": "Python"}, "licenseInfo": {"spdxId": "Apache-2.0"},
                "issues": {"totalCount": 1}, "pullRequests": {"totalCount": 1},
                "latestRelease": {"tagName": "v1.0.0", "publishedAt": "2026-09-01T00:00:00Z"},
                "defaultBranchRef": {"target": {"history": {"totalCount": 250}}},
            }
        payload = {"data": data}
        if errors:
            payload["errors"] = errors
        return gs.Response(1 if errors else 0, json.dumps(payload), "gh: Could not resolve" if errors else "")
    if kind == "-i":
        if "acme/bravo" in cmd[3]:
            return gs.Response(1, 'HTTP/2.0 403 Forbidden\r\n\r\n{"message":"list too large"}', "gh: too large (HTTP 403)")
        return gs.Response(0, "HTTP/2.0 200 OK\r\nLink: " + LinkHeaderTests.LINK + "\r\n\r\n[{}]", "")
    raise AssertionError(f"unexpected call {cmd}")


class EndToEndTests(unittest.TestCase):
    def run_main(self, root: Path, name: str, when: datetime, *extra: str) -> gs.GhClient:
        client = gs.GhClient(runner=fake_gh, sleep=lambda s: None)
        out = root / name
        code = gs.main(["--out", str(out), "--top", "2", *extra], client=client, now=when)
        self.assertEqual(code, 0)
        return client

    def test_full_run_writes_three_files_with_the_expected_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = self.run_main(root, "20261030_1900-github", SNAP, "--compare", "none", "--top", "10")
            out = root / "20261030_1900-github"
            self.assertEqual(sorted(p.name for p in out.iterdir()), ["README.md", "repos.json", "repos.tsv"])

            data = json.loads((out / "repos.json").read_text(encoding="utf-8"))
            by_name = {r["full_name"]: r for r in data["repos"]}
            self.assertEqual(by_name["acme/alpha"]["category"], "core")  # hit by the most core queries
            self.assertEqual(by_name["acme/bravo"]["category"], "agent-memory")
            self.assertEqual(by_name["acme/old"]["table"], "quiet")
            self.assertIn("quiet", by_name["acme/old"]["flags"])
            self.assertTrue(by_name["microsoft/graphrag"]["watchlist"])
            self.assertEqual(by_name["microsoft/graphrag"]["commits_90d"], 100)
            self.assertTrue(by_name["microsoft/graphrag"]["commits_90d_capped"])
            self.assertEqual(by_name["getzep/graphiti"]["category"], "agent-memory")  # watchlist category
            self.assertEqual(by_name["microsoft/graphrag"]["contributors"], 64)
            self.assertIsNone(by_name["acme/bravo"]["contributors"])  # refused by the fake
            self.assertNotIn(FAKE_NOT_FOUND, by_name)

            self.assertEqual(data["meta"]["api_calls"]["total"], client.total_calls)
            failures = {f["what"] for f in data["meta"]["failures"]}
            self.assertIn(f"watchlist {FAKE_NOT_FOUND}", failures)
            self.assertIn("contributors acme/bravo", failures)

            tsv_lines = (out / "repos.tsv").read_text(encoding="utf-8").splitlines()
            widths = {len(line.split("\t")) for line in tsv_lines}
            self.assertEqual(widths, {len(gs.TSV_COLUMNS)})
            self.assertEqual(len(tsv_lines) - 1, len(data["repos"]))

            readme = (out / "README.md").read_text(encoding="utf-8")
            for needle in ("## How to read this", "## Failures", "### core: ranked", "### core: quiet or archived",
                           "### agent-memory: ranked", "### markdown-kb: ranked", "### adjacent: quiet or archived",
                           "Stars are signals, not verdicts", "[acme/alpha](https://github.com/acme/alpha)",
                           "100+", f"watchlist {FAKE_NOT_FOUND}", "no earlier snapshot"):
                self.assertIn(needle, readme)
            self.assertIn("watch me \\| now", readme)  # table cell escaped

    def test_outputs_contain_no_local_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_main(root, "20261030_1900-github", SNAP, "--compare", "none")
            for path in (root / "20261030_1900-github").iterdir():
                text = path.read_text(encoding="utf-8")
                for forbidden in ("/Users/", "/private/", "/home/", tmp):
                    self.assertNotIn(forbidden, text, f"{forbidden} in {path.name}")

    def test_second_run_compares_with_the_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_main(root, "20261023_1900-github", SNAP - timedelta(days=7))
            self.run_main(root, "20261030_1900-github", SNAP)  # default compare: newest earlier directory
            data = json.loads((root / "20261030_1900-github" / "repos.json").read_text(encoding="utf-8"))
            self.assertEqual(data["meta"]["compare"]["days_between"], 7.0)
            self.assertEqual(data["meta"]["compare"]["new_entrants"], 0)
            self.assertTrue(all(r["star_delta"] == 0 for r in data["repos"]))
            readme = (root / "20261030_1900-github" / "README.md").read_text(encoding="utf-8")
            self.assertIn("Compared with `20261023_1900-github`, 7.0 days earlier", readme)
            self.assertIn("| Change |", readme)

    def test_no_enrich_skips_releases_commits_and_contributors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = self.run_main(root, "20261030_1900-github", SNAP, "--compare", "none", "--no-enrich")
            data = json.loads((root / "20261030_1900-github" / "repos.json").read_text(encoding="utf-8"))
            self.assertTrue(all(r["contributors"] is None and r["commits_90d"] is None for r in data["repos"]))
            self.assertEqual(client.calls["rest"], 0)

    def test_refuses_to_overwrite_a_non_empty_output_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "20261030_1900-github"
            out.mkdir()
            (out / "keep.txt").write_text("x")
            code = gs.main(["--out", str(out), "--compare", "none"], client=gs.GhClient(runner=fake_gh), now=SNAP)
            self.assertEqual(code, 2)
            self.assertEqual([p.name for p in out.iterdir()], ["keep.txt"])

    def test_tsv_cells_never_contain_tabs_or_newlines(self):
        record = rec("a/b", description="x\ty\nz")
        record["description"] = "x\ty\nz"
        row = gs.render_tsv([dict(record, flags=["quiet"], also_in=["core"])]).splitlines()[1].split("\t")
        self.assertEqual(len(row), len(gs.TSV_COLUMNS))
        self.assertEqual(row[gs.TSV_COLUMNS.index("description")], "x y z")


if __name__ == "__main__":
    unittest.main()
