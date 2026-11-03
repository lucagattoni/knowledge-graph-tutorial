---
type: page
order: 2
updated: 20261102 20:17 UTC
---

# X1: Snapshot distributions

X1 asks how unusual the repositories flagged as fast-growing are, among the repositories of one dated GitHub snapshot. It ran on 20261031 at no cost, with no model and no network. Its result is a description of that set of repositories. It does not say whether any growth is organic.

## The question

The archive's evidence page flagged nine repositories as fast-growing in the first snapshot and could not say whether their growth was organic [1]. The flag is a rule: stars divided by age in days at or above 150 [2]. Counting the flag in the two committed snapshot files now gives nine repositories in the first (924 rows, taken 20261030 19:13 UTC) and ten in the second (931 rows, 20261030 19:54 UTC) [3][4]. The tenth, [codebase-memory-mcp](../projects/codebase-memory-mcp.md), is absent from the first file and is marked a new entrant in the second, so the change from nine to ten comes from the set of repositories tracked, not from growth between two snapshots [3][4].

The question X1 answers: how do the ten sit among the 552 ranked repositories of the newest snapshot on stars per day, forks per 100 stars, open issues and pull requests, contributors, and days since the last push [5]?

## Why it matters

A flagged number alone has no context. Whether 250 stars per day is rare among the repositories this project tracks cannot be read from the number. The trends and projects chapters quote stars as a signal of attention, and the snapshot's own notes say stars measure attention, not quality, and can be bought, boosted by a viral post or earned by a list or tutorial [2]. X1 gives the flag a reference frame without adding any claim about why the stars arrived.

## Method

- Read `repos.tsv` of the newest snapshot with `tools/describe_snapshot.py`. No model, no network, no new API calls [5].
- The set described is the *ranked* repositories: pushed within the last 90 days and not archived. That is 552 of the 931 found [3][6].
- For each of six measures, print the 10th, 25th, 50th, 75th, 90th and 99th percentile and the maximum, by linear interpolation [5].
- For each flagged repository, print its value and its percentile rank. The rank is the share of ranked repositories at or below the value, so the flagged repositories are part of the set they are ranked in [5].
- The tool has 14 tests. Run again now, all 14 pass. A deliberate break of the tie rule (changing "at or below" to "below" in the rank function) turns 3 of the 14 red, which reproduces the archive's record [7][11].
- The report was regenerated now from the committed file and is byte-identical to the committed report [5][8].

## Data

| Item | Value | Source |
|---|---|---|
| Snapshot | `20261030_1954-github`, taken 20261030 19:54 UTC by `tools/gh_snapshot.py` 1.0.0 | [3] |
| How repositories were found | 17 search queries, each run twice (recently pushed, and not), one page of up to 100 results per search, a stars floor of 100 | [2][3][9] |
| Found / ranked / flagged `fast-growth` | 931 / 552 / 10 | [3][4] |
| Contributors | recorded for 106 of the 552: the top 25 ranked repositories of each category and every watch-list repository | [3][5][10] |

The repositories are what the searches returned, with a stars floor and a cap per query. They are not a random sample of GitHub [8].

## Models

None.

## Cost

None beyond local compute. The run is one command, `uv run tools/describe_snapshot.py`; the regeneration above is the check [5][8].

## Status

Ran 20261031 16:00 UTC, as the archive records [11]. Checked again on 20261102: the tests pass, the mutation reproduces, and the report regenerates identically [7][8]. It has not been run on a later snapshot, because none exists: the two committed snapshots are minutes apart (the second says "0.0 days earlier") [3]. The archive's plan is to take a new snapshot after a few weeks, so that the star comparison means something, and to re-run the tool then [13].

## Result

Percentiles of the 552 ranked repositories, snapshot of 20261030 19:54 UTC [8]:

| Measure | n | p10 | p25 | p50 | p75 | p90 | p99 | max |
|---|---|---|---|---|---|---|---|---|
| Stars | 552 | 134 | 230 | 723 | 3,750 | 21,698 | 92,439 | 160,020 |
| Stars per day of age | 552 | 0.42 | 0.83 | 2.54 | 9.13 | 31.68 | 224 | 664 |
| Forks per 100 stars | 552 | 5.7 | 8.27 | 11.3 | 15.12 | 22.24 | 53.62 | 98.02 |
| Open issues and pull requests | 552 | 1 | 4 | 14 | 54 | 235 | 1,155 | 7,473 |
| Contributors (enriched repositories only) | 106 | 8 | 19.25 | 51 | 138 | 366 | 1,986 | 3,749 |
| Days since the last push | 552 | 0 | 0 | 2 | 17.25 | 51 | 85.98 | 89 |

The ten flagged repositories, each value followed by its percentile rank among the 552 [8]. Names link to a project page where the archive has one.

| Repository | Stars | Stars per day | Forks per 100 stars | Contributors |
|---|---|---|---|---|
| [Graphify-Labs/graphify](../projects/graphify.md) | 139,374 (p99) | 664 (p100) | 9.54 (p35) | 374 (p91) |
| [Egonex-AI/Understand-Anything](../projects/understand-anything.md) | 89,048 (p99) | 389 (p100) | 8.47 (p27) | 75 (p61) |
| [colbymchenry/codegraph](../projects/codegraph.md) | 76,004 (p98) | 268 (p100) | 6.61 (p15) | 51 (p51) |
| headroomlabs-ai/headroom | 78,365 (p98) | 266 (p99) | 7.79 (p22) | 359 (p90) |
| [thedotmack/claude-mem](../projects/claude-mem.md) | 105,979 (p99) | 250 (p99) | 8.81 (p29) | 315 (p85) |
| 666ghj/MiroFish | 82,864 (p98) | 245 (p99) | 15.12 (p75) | 19 (p25) |
| datawhalechina/hello-agents | 85,424 (p98) | 204 (p99) | 12.44 (p61) | 123 (p75) |
| virgiliojr94/book-to-skill | 36,582 (p95) | 201 (p99) | 10.6 (p44) | 54 (p54) |
| [DeusData/codebase-memory-mcp](../projects/codebase-memory-mcp.md) | 47,853 (p96) | 194 (p99) | 8.22 (p24) | 208 (p81) |
| [vectorize-io/hindsight](../projects/hindsight.md) | 56,614 (p97) | 155 (p98) | 12.03 (p57) | 291 (p83) |

In words, for this set of 552 [8]:

- **Stars:** the ten sit between the 95th and 99th percentile.
- **Stars per day:** between the 98th and 100th percentile. This is by construction. The flag selects the ten with the highest stars per day, and ten of 552 is 1.8%.
- **Forks per 100 stars:** between the 15th and 75th percentile. Seven of the ten are at or below the median of 11.3. The lowest ratio is 6.61, above the 3 per 100 that the snapshot's separate `low-forks` flag uses [2].
- **Contributors, where recorded:** between the 25th and 91st percentile.
- **Open issues and pull requests:** between the 60th and 100th percentile. Days since the last push: between the 36th and 74th percentile.

*Reading:* on the measures that are not part of the flag, the ten stand out on stars and on issue counts and sit in the ordinary range on forks per 100 stars and on push recency. That is a statement about where they sit in this set. It is not evidence that their stars were earned or bought.

## What it would change

It gives the `fast-growth` flag a context a reader can use: the flag marks the top 1.8% on one measure, the same repositories are at or above the 95th percentile on stars, and all of them are at or below the 75th percentile on forks per 100 stars [8]. The archive's evidence page can point to it instead of listing the nine or ten repositories without a reference [1]. It changes no assessment of any project.

## What it cannot show

- **Why.** The tool's own notes say a repository can be far from the middle on every measure because of a launch, a newsletter, a trend, a list or a tutorial, and also for other reasons [8]. Nothing here separates organic from inflated growth. The archive's notes on the nine repositories of the first snapshot record that no star timeline was obtained for any of them: the endpoint that lists who starred a repository returned 404 for three (claude-mem, graphify, hindsight), and the other six were not examined or are unstated [1].
- **Anything outside this set.** A percentile means "among these 552". The searches are keyword and topic queries with a stars floor, so the set depends on the queries [8][9].
- **A trend.** One snapshot is one moment. Stars per day is stars divided by age, an average over the repository's whole life, so a repository that gained most of its stars in a week looks the same as one that gained them steadily [2]. A spot check on 20261102 19:39 UTC found the ten gaining between 148 and 4,569 stars in about three days after the snapshot, against lifetime averages of 155 to 664 per day. The check is outside X1 and is not part of its result [12].
- **A like-for-like contributor rank.** Contributors are recorded only for the repositories the tool enriched, which are the top 25 by stars in each category and the watch list [5][10]. *Reading:* the contributor percentile therefore compares each flagged repository with other well-starred ones, which is a more popular group than the one used for the other columns.
- **Independence.** The owner ran it on the owner's own snapshot. It is first-party and small.

## Sources

1. [Evidence-and-claims page of the archive](../../kb-kg/directions/evidence-and-claims.md) : the nine flagged repositories, the 404 from the stargazer endpoint, stars as unvetted signals (read 20261102 19:45 UTC; the page cites the snapshot data as read 20261030 19:59 UTC)
2. [Snapshot README](../../kb-kg/landscape/20261030_1954-github/README.md) : the flag rules, the 150 stars-per-day threshold, how stars per day is computed, the warnings on stars (read 20261102 19:44 UTC)
3. [Newest snapshot data](../../kb-kg/landscape/20261030_1954-github/repos.tsv) : 931 rows, 552 ranked, 10 flagged, 106 with contributors, new-entrant mark on codebase-memory-mcp, counted by script (read 20261102 19:38 UTC)
4. [First snapshot data](../../kb-kg/landscape/20261030_1913-github/repos.tsv) : 924 rows, 9 flagged, no row for codebase-memory-mcp, counted by script (read 20261102 19:38 UTC)
5. [Tool source](../../tools/describe_snapshot.py) : method, percentile and rank definitions, the set described (read 20261102 19:36 UTC)
6. [Snapshot tool notes](../../tools/snapshot/README.md) : the ranking rule and the enrichment rule (read 20261102 19:44 UTC)
7. [Tool tests](../../tools/test_describe_snapshot.py) : 14 pass; with the rank function changed from "at or below" to "below", 3 fail, both run in a copy outside the repository (read 20261102 19:38 UTC; the first run was at 19:37)
8. [Committed X1 report](../../kb-kg/experiments/x1-snapshot-distributions/README.md) : the tables above; byte-identical to a regeneration made for this page (read 20261102 19:37 UTC)
9. [Snapshot queries and thresholds](../../tools/snapshot/queries.toml) : stars floor of 100, one page of 100 per search, 90 quiet days, 150 stars per day (read 20261102 19:44 UTC)
10. [Snapshot README, enrichment line](../../kb-kg/landscape/20261030_1954-github/README.md) : top 25 per category, enrichment on (read 20261102 19:44 UTC)
11. [Experiments record of the archive](../../kb-kg/experiments/README.md) : X1's question, method, cost and run time of 20261031 16:00 UTC (read 20261102 19:36 UTC, on the archive's main branch at `f2e87e6`)
12. https://api.github.com/repos/Graphify-Labs/graphify (and the same endpoint for each of the other nine flagged repositories) : creation dates equal the snapshot's for all ten; all ten public; live star counts higher than the snapshot's by 148 to 4,569 (read 20261102 19:39 UTC)
13. [Resume file of the archive](../../RESUME.md) : the plan to re-run the snapshot tool after a few weeks (read 20261102 19:36 UTC, from the archive's main branch at `f2e87e6`)
