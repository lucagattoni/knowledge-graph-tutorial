---
slug: semantica
repo: semantica-agi/semantica
tier: card
category: core
snapshot: 20261030 19:39 UTC
---

# Semantica

| | |
|---|---|
| Repository | https://github.com/semantica-agi/semantica [1] |
| Licence | MIT, from the `LICENSE` file (21 lines; head and tail read; "Copyright (c) 2026 Semantica") [2]. The README badge and licence line also say MIT, and PyPI lists MIT, so all agree [3][5]. |
| Language | Python [1] |
| Stars, forks | 14,349, 1,687 (20261030 19:39 UTC; the landscape snapshot of 20261030 19:13 UTC has the same figures) [1][9] |
| Created, last push | 20250625 10:41 UTC, 20261030 19:24 UTC [1] |
| Latest release | v0.7.0, 20260922 11:18 UTC; PyPI also lists 0.7.0 as latest [4][5] |
| Status | active; not archived. The landscape snapshot sets no flag (29.16 stars per day over 492 days, 11.76 forks per 100 stars; heuristics) [1][9] |
| Paper, docs | no paper stated; the README links a website and a docs site (not fetched), and the tree holds `CITATION.cff` [3] |

## What it is

Semantica describes itself as "graph-native infrastructure for context and accountable AI systems": it ingests enterprise data, builds a "Context Graph" and knowledge graph, and adds ontology governance, deterministic reasoning, provenance and recorded AI decisions [3]. Its pitch is auditability for regulated domains, and it positions itself as a layer under an existing LLM, vector store and agent framework [3]. The README performance table (node search, deduplication) comes from v0.5.0 on the authors' own 118,000-node graph, and part of it is "historical" figures from the changelog [3]. No retrieval-quality benchmark and no independent evaluation was found [3].

The README disagrees with itself on Python: the badge says 3.11+, the v0.7.0 notes say 3.10+, and PyPI 0.7.0 requires `>=3.10,<3.14` [3][5]. The changelog's unreleased section drops 3.10 [7]. The v0.7.0 notes say the core install shrank from 44 to 22 direct dependencies, with heavy libraries moved to extras [3].

## How it works

A pipeline runs ingest (files, web, databases, Databricks, Snowflake, SAP, streams, MCP), parse, normalize, split, extract (entities, relations, events, triplets), conflict detection and deduplication, then builds the graph with bi-temporal facts [3]. On top sit OWL, SHACL and SKOS ontologies, rule reasoning (forward chaining, Rete, Datalog, SPARQL), W3C PROV-O provenance and decision records [3]. Storage is RDF stores, property graphs (Neo4j, FalkorDB, AGE, Neptune) or vector stores [3]. Retrieval has local, global, DRIFT and hybrid modes, the global ones using LLM-written community reports [3]. The README says no LLM is needed for construction, reasoning or provenance [3]. Agents use a 15-tool MCP server, a REST API or a CLI [3].

## Status and direction

Active: 1,071 commits since 20260801, from many authors (top three: 336, 106 and 66 commits; 33 by dependabot); 134 contributors listed [6][11]. Six releases from v0.6.0 (20260721) to v0.7.0 (20260922), none since [4]. The tree holds `GROWTH.md`, a growth playbook that targets 10,000 active developers and bans fake install traffic [8]. Roadmap: unstated. 78 open issues, 59 open pull requests (20261030 19:45 UTC) [10].

## Sources

1. https://github.com/semantica-agi/semantica : repository metadata via the GitHub API (stars, forks, licence field, dates, open issues) (read 20261030 19:39 UTC)
2. https://github.com/semantica-agi/semantica/blob/main/LICENSE : MIT License text (read 20261030 19:41 UTC)
3. https://github.com/semantica-agi/semantica/blob/main/README.md : description, architecture, storage, MCP tools, performance table, v0.7.0 notes, Python badge, licence line (read 20261030 19:41 UTC)
4. https://github.com/semantica-agi/semantica/releases : release tags and dates (read 20261030 19:41 UTC)
5. https://pypi.org/pypi/semantica/json : PyPI version, Python requirement, licence, upload dates (read 20261030 19:41 UTC)
6. https://github.com/semantica-agi/semantica/commits/main : commit count since 20260801 (from the API pagination header) and commit authors; recent commit subjects (read 20261030 19:41 UTC)
7. https://github.com/semantica-agi/semantica/blob/main/CHANGELOG.md : the unreleased section, including the removal of Python 3.10 (read 20261030 19:42 UTC)
8. https://github.com/semantica-agi/semantica/blob/main/GROWTH.md : growth and distribution playbook (read 20261030 19:42 UTC)
9. [Landscape snapshot](../landscape/20261030_1913-github/repos.tsv) : stars per day, forks per 100 stars, flags (20261030 19:13 UTC)
10. https://github.com/semantica-agi/semantica/pulls : open issues and pull requests via the search API (read 20261030 19:45 UTC)
11. https://github.com/semantica-agi/semantica/graphs/contributors : contributor count from the GitHub contributors API (read 20261030 19:41 UTC)
