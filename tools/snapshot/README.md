# GitHub landscape snapshot

`tools/gh_snapshot.py` writes a dated snapshot of the most starred and most active GitHub projects in
four categories of this reference. Each snapshot is a directory in `kb-kg/landscape/`:

```
kb-kg/landscape/<UTC YYYYMMDD_HHMM>-github/
  README.md    tables to read: one ranked and one quiet-or-archived table per category,
               releases/commits/contributors, queries run, failures
  repos.tsv    every repository found, all columns (spreadsheet- and awk-friendly)
  repos.json   the same records plus run metadata (queries, API calls, failures, thresholds)
```

Stars are signals, not verdicts. The snapshot says what was starred and pushed on a date; it does not
say what is good, correct or in scope. Search matches topics and keywords, so the ranking also
promotes awesome lists, tutorials and general agent tools. Read the description first.

## Run it

Needs the GitHub CLI `gh`, already authenticated (`gh auth login`), and `uv`. The script uses only the
Python standard library (3.11 or newer) and calls GitHub through `gh api`. It never reads, stores or
prints a token: `gh` holds the credentials.

```
uv run tools/gh_snapshot.py                  # default output directory, top 25, enrichment on
uv run tools/gh_snapshot.py --top 10 --no-enrich --out kb-kg/landscape/trial-github
uv run tools/gh_snapshot.py --compare kb-kg/landscape/20261030_1913-github
```

| Argument | Default | Meaning |
|---|---|---|
| `--out DIR` | `kb-kg/landscape/<UTC YYYYMMDD_HHMM>-github` | Output directory. Refuses to write into a non-empty one. |
| `--top N` | 25 | Repositories per category in the README tables, and the size of the enriched set. |
| `--no-enrich` | off | Skip latest release, commits in 90 days and contributors. |
| `--compare PREV_DIR` | the newest earlier snapshot next to `--out` | Earlier snapshot to compare with. `--compare none` turns the comparison off. |

A run takes a few minutes, dominated by the 2.5 s pause between searches and one call per enriched
repository. Progress goes to standard error.

## What it does

1. **Search.** For each category it runs every query in `queries.toml` twice, sorted by stars: once for
   repositories pushed within the last 90 days (the *active* pass) and once for those pushed longer ago
   (the *quiet* pass). Two disjoint passes stop a long-dead giant from crowding active projects out of
   the 100-result window. Each query gets `stars:>=min_stars`.
2. **Watchlist.** Every repository in `watchlist.txt` that the search did not return is fetched directly
   (batched GraphQL through `gh api graphql`), so it is always tracked.
3. **Deduplicate and categorise.** Repositories are merged across queries by lowercase `owner/name`. A
   repository keeps every category it was hit in (`also_in`) but has one primary category: the
   watchlist's, otherwise the category whose queries returned it most often, ties broken in the order
   core, agent-memory, markdown-kb, adjacent.
4. **Rank.** Within a category, repositories that are not archived and were pushed within 90 days are
   ranked by stars. Everything else goes to that category's *quiet or archived* table, also by stars.
   An archived repository is never ranked, even if its last push is recent: it takes no new commits.
   Ties break by name.
5. **Enrich** the top N ranked repositories per category and every watchlist repository:
   latest release (tag and date, or `none`), commits on the default branch in the last 90 days
   (**capped at 100**; `commits_90d_capped` is true when 100 or more), and contributor count. Release and
   commits come 25 repositories at a time from GraphQL; contributors come from one REST call per
   repository, reading the `Link` header of `contributors?per_page=1&anon=true` through `gh api -i`
   (the last page number is the count, and it includes anonymous contributors).
6. **Compare** with the previous snapshot, if any: `prev_stars`, `star_delta`, `days_between`, and
   `new_entrant` for repositories absent from the previous snapshot.
7. **Write** the three files.

## Files in `tools/snapshot/`

### `queries.toml`

| Table | Keys | Meaning |
|---|---|---|
| `[flags]` | `quiet_days` (90), `fast_growth_stars_per_day` (150), `low_forks_min_stars` (5000), `low_forks_per_100_stars` (3) | Flag thresholds. `quiet_days` is also the ranking window. |
| `[search]` | `per_page` (100), `pages` (1), `min_stars` (100), `quiet_pass` (true) | Search size. `quiet_pass = false` halves the search calls and leaves the quiet tables with only watchlist and archived repositories. |
| `[core]`, `[agent-memory]`, `[markdown-kb]`, `[adjacent]` | `queries` (list of GitHub repository-search strings), `description` | The four categories. All four must exist. |

Unknown keys and tables are an error, so a typo does not silently change a run.

### `watchlist.txt`

One `owner/repo<TAB>category` per line; `#` starts a comment. A watchlist repository gets its listed
category whatever the search says, is always enriched, and is shown in its table even when ranked
below the top N (marked `(w)`). The category is an editorial choice. If GitHub reports that a listed
repository now has another name, the README notes it under Notes.

## Flags

Heuristics, not verdicts. Thresholds are in `queries.toml`; flags are computed from the rounded values
stored in `repos.tsv`, so you can reproduce them.

| Flag | Rule |
|---|---|
| `archived` | archived on GitHub |
| `quiet` | whole days since last push > `quiet_days` (90) |
| `fast-growth` | `stars_per_day` >= 150 |
| `low-forks` | stars >= 5000 and `forks_per_100_stars` < 3 |

`stars_per_day` = stars / max(age in whole days, 1): a lifetime average, not recent growth. A flag is a
reason to look at the star history and the repository, nothing more. A `fast-growth` repository may be
a genuine viral launch; a `low-forks` one may be an end-user application nobody forks.

## `repos.tsv` columns

`full_name`, `category` (primary), `also_in`, `watchlist`, `table` (`ranked` or `quiet`), `rank` (within
its table), `stars`, `forks`, `open_issues` (issues and pull requests together), `created_at`,
`pushed_at` (ISO 8601 UTC), `license` (SPDX id from GitHub's reading of the LICENSE file; empty when
none detected; `NOASSERTION` when a file exists that matches no single SPDX id), `archived`,
`language`, `description` (one line, at most 120 characters, emails and paths removed), `age_days`,
`stars_per_day`, `forks_per_100_stars`, `days_since_push`, `flags` (comma-separated), `hits` (number of
distinct queries that returned it), `enriched`, `latest_release`, `latest_release_date`,
`commits_90d`, `commits_90d_capped`, `contributors`, `prev_stars`, `star_delta`, `days_between`,
`new_entrant`. Empty means unknown or not applicable. Columns are in a fixed order whether or not a
comparison ran.

## Rate limits, failures and the API-call budget

- Search allows 30 requests a minute: the script waits at least 2.5 s between search calls.
- On a rate-limit error it asks `gh api rate_limit` when the window resets, sleeps until then (a fixed
  60 s for a secondary limit) and retries, up to 3 times per call.
- Nothing is discarded silently. A failed call (a rejected query, a repository that vanished, a
  contributor list GitHub refuses for very large repositories) is recorded and listed under
  **Failures** in the snapshot README and in `repos.json`, and the run continues. A missing or
  unauthenticated `gh` stops the run with exit code 2.
- Call count = searches (queries x passes x pages) + GraphQL batches (watchlist repositories not
  returned by search, plus the enriched set, 25 per call) + one contributors call per enriched
  repository. The default configuration makes about 160 calls. `--no-enrich` removes the GraphQL
  enrichment and all contributor calls.
- Search returns at most 100 results per pass per query, so the quiet tables are a sample of what
  exists, not a census. The query table in each snapshot README shows GitHub's reported match count
  next to what was returned.

## Tests

```
uv run python -m unittest tools/test_gh_snapshot.py
```

Standard-library `unittest`, fake data, no network. They cover the flag logic and its boundaries, the
90-day ranking rule, primary-category assignment, Link-header parsing, search pacing, rate-limit retry,
GraphQL batching, comparison, and a full run against a fake `gh`.

## Public safety

Snapshot files go into a repository that is to become public. Descriptions are scrubbed of email
addresses, local paths and token-like strings; outputs use repository-relative paths only. Run
`tools/check_public_safe.sh` before committing a snapshot.
