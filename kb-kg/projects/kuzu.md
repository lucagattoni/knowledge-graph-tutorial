---
slug: kuzu
repo: kuzudb/kuzu
tier: card
category: adjacent
snapshot: 20261030 19:29 UTC
---

# Kuzu

| | |
|---|---|
| Repository | https://github.com/kuzudb/kuzu [1] |
| Licence | MIT, from the `LICENSE` file ("Copyright (c) 2022-2025 Kùzu Inc.") [2]. The README also says MIT, so the two agree [3]. |
| Language | C++ (GitHub primary language) [1] |
| Stars, forks | 4,018, 532 (20261030 19:29 UTC; the landscape snapshot of 20261030 19:13 UTC has the same figures) [1] |
| Created, last push | 20200926 07:43 UTC, 20251010 15:34 UTC [1] |
| Latest release | v0.11.3, 20251010 14:32 UTC [4] |
| Status | archived: the GitHub archived flag is true [1]; 385 days since the last push (computed) |
| Paper, docs | the README links documentation at kuzudb.github.io/docs and says it moved from the project website to GitHub [3]; not fetched here. A paper is unstated in the README. |

## What it is

Kuzu is an embedded property-graph database written in C++ that implements Cypher, with built-in full-text search and vector indices, developed by Kùzu Inc.; the README describes no LLM use [2][3]. The repository is archived, and its README opens with a note: Kuzu "is working on something new", prior releases "will continue to be usable", and the docs and blog move to GitHub; the note gives no reason and names no buyer [3]. BetaKit, citing an EU filing, reports that Apple agreed on 20251009 to buy all shares of Kuzu and hire select employees, and says Apple's motivation is unclear [6]. The University of Waterloo computer science news page (dated 20260224) gives the same outline, and neither source names the employees hired [6][7]. The Register reported on 20251014 that Kùzu Inc. gave no statement beyond the archive note [11].

## How it works

The database is embedded and serverless: it runs inside the host application [3]. The data model is a property graph queried with Cypher [3]. Storage is columnar and disk-based, with adjacency lists in a compressed sparse row layout and join indices [3]. The query processor is vectorised and factorised, runs on multiple cores and gives serialisable ACID transactions [3]. Full-text search and the vector index are extensions; v0.11.3 pre-installs four (`algo`, `fts`, `json`, `vector`) [3]. The official extension server is no longer provided, and the README shows how to self-host one in Docker [3]. Language bindings other than WebAssembly: unstated in the README [3].

## Status and direction

Archived on GitHub; the last two commits are "Update README" and "remove logo" [5]. The repository states no roadmap. Forks read at 20261030 19:29 UTC:

| Fork | Latest release | Last push | State |
|---|---|---|---|
| LadybugDB/ladybug [8] | v0.22.1 | 20261030 | active; README: "formerly known as Kuzu" |
| predictable-labs/ryugraph [9] | v25.9.2 | 20260120 | README says it continues Kuzu |
| Kineviz/bighorn [10] | none | 20260810 | archived |

## Sources

1. https://github.com/kuzudb/kuzu : repository metadata via the GitHub API (stars, forks, archived flag, dates, language) (read 20261030 19:29 UTC)
2. https://github.com/kuzudb/kuzu/blob/master/LICENSE : MIT licence text and copyright line (read 20261030 19:29 UTC)
3. https://github.com/kuzudb/kuzu/blob/master/README.md : archive note, feature list, extension notes, licence statement (read 20261030 19:29 UTC)
4. https://github.com/kuzudb/kuzu/releases : latest release v0.11.3 and release dates (read 20261030 19:29 UTC)
5. https://github.com/kuzudb/kuzu/commits/master : most recent commit subjects (read 20261030 19:29 UTC)
6. https://betakit.com/apple-strikes-deal-to-acquire-canadian-database-software-startup-kuzu/ : the Apple agreement of 20251009 as reported from an EU filing (read 20261030 19:29 UTC)
7. https://uwaterloo.ca/computer-science/news/waterloo-based-graph-database-start-up-kuzu-acquired-apple : the University of Waterloo's account of the acquisition (read 20261030 19:30 UTC)
8. https://github.com/LadybugDB/ladybug : fork metadata, v0.22.1, README (read 20261030 19:29 UTC)
9. https://github.com/predictable-labs/ryugraph : fork metadata, v25.9.2, README (read 20261030 19:29 UTC)
10. https://github.com/Kineviz/bighorn : fork metadata, archived flag, no release (read 20261030 19:29 UTC)
11. https://www.theregister.com/2025/10/14/kuzudb_abandoned/ : news report of 20251014 that Kùzu Inc. gave no statement beyond the archive note and that Kineviz had forked the code as bighorn (read 20261030 19:29 UTC)
