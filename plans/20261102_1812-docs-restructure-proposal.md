# Proposal: one live place for papers and projects, and documentation you can navigate

**Superseded on 20261102 19:15 UTC** by [the from-scratch plan](20261102_1915-docs-from-scratch-plan.md): the
owner chose to write a new documentation instead of restructuring this one. Kept for its measurements
(sections 2.1 to 2.4), which the new plan draws on.

**Status: draft for the owner, written 20261102 18:12 UTC. Nothing in the repository has been changed.**
Based on a read-only analysis of the tree at `ddbd4bf` (131 Markdown pages staged for the site). The
scripts that produced every number below were run on that tree on 20261102 between 18:05 and 18:12 UTC.

## 1. Summary

The question "what is the current way of development and research, and which are the notable projects and
papers?" has no single answer page. It is answered, in part and in different words, in **six places**, and
the facts in them have started to drift apart. The proposal:

1. Make **Projects**, **Papers** and **Benchmarks** three *live registries*: generated from data files,
   each with an "as of" line, a recent-changes feed and a one-line "how to add".
2. Turn `directions/README.md` into **"The field now"**: the one-page answer to "what is the state of the art",
   linking into the registries.
3. Give every other page exactly one job (registry, analysis, evidence, history, process) and make it
   **link instead of copy**; enforce that with a freshness check and a duplicate-figure scan in CI.
4. Reorder the site by reader question, rewrite the home page as a front door, and keep process state
   (`RESUME.md`, `DECISIONS.md`) out of the reading path.
5. Do it in three phases that **keep every existing path**, so no link breaks and nothing outside this
   repository needs editing. Phase 3 waits for the experiments session to free `RESUME.md` and `DECISIONS.md`.

## 2. What I found

### 2.1 The same question is answered in six places

| Reader question | Where it is answered today | What is wrong |
|---|---|---|
| Which projects are notable? | `projects/README.md` (generated: name, repo, tier, snapshot time); `landscape/` (2 snapshots, 931 repos, and the *selection* page with 65 starred rows); `llm-era` (a "created in 2026, by stars" table and about 25 repos in the timeline); `literature` §4 (7 repos with July and October stars); `directions/agent-memory.md` (an 18-row project table) | No page ranks or describes them in one view. Five different star tables with five dates. |
| Which papers are notable? | `papers-benchmarks` §1-2 (13 surveys, 55 method papers); `llm-era` timeline (about 25 papers); `literature` §2-3; each project entry's "Paper, docs" row | 152 distinct arXiv ids; **39 appear in two or more files and 15 in three or more**. Eight core papers (RAG vs GraphRAG, HippoRAG, HippoRAG 2, GraphRAG-Bench, GraphRAG, Zep, A-MEM, Mem0) appear in the same four areas. |
| What is the current way of working? | `llm-era` §3 (six "shifts in approach"); `directions/` (nine pages); `literature` §2 | **All six shifts in `llm-era` §3 map onto a direction page** (eager-to-lazy, agent-memory, plain-files, infrastructure, open-core, code graphs). Two statements of one conclusion. |
| Does a graph help? | `papers-benchmarks` §3 (13 study rows); `literature` §2.3 and §3; `directions/evidence-and-claims`; `directions/agent-memory` "Evidence for/against" | Same studies, read to different depths (below). |
| Which benchmarks and datasets? | `papers-benchmarks` §4 (28 rows), the 4th of 5 parts of a 6,500-word page | Hard to find; the owner asked another session exactly this question today. |
| Where does the project stand? | `README.md`, `RESUME.md`, `DECISIONS.md`, `kb-kg/README.md`, `pinakes/README.md`, `kb-kg/experiments/README.md` | "77 entries" is written in 4 files; 19 pages carry their own status banner in 3 different formats; DECISIONS rows D-21 to D-26 run 107 to 215 words (D-1 to D-18 run 12 to 40) and partly repeat `RESUME.md`. |

### 2.2 Drift that has already happened (checked in the pages)

| Same thing | Page A says | Page B says |
|---|---|---|
| Study 2609.18099 (EffiRAG) | `papers-benchmarks` §3.1: "abstract only" | `literature` source 10: "full text via the alphaXiv reader"; it adds the judge model, extra variants and the scaling runs the papers page lacks |
| Study 2610.30755 | `papers-benchmarks` §3.2: abstract only, "whether graph-based ones are among [the memory systems] is unstated"; title "Naive RAG Is Stronger Than We Thought" | `literature` source 11: 12 agentic memory systems compared, graph expansion tested as an ablation; title "Is Complex Agentic Memory Always Needed?". Which title is current: unstated. |
| Stars of `Graphify-Labs/graphify` | `llm-era` table 139,344 and timeline 139,349 | selection 139,356; second snapshot 139,374 |
| Where the facts about a project live | `DECISIONS.md` working rule: "one home per fact" | 79 star figures sit in prose outside the entries and the snapshot pages, in 10 files; 65 of them in three pages (`llm-era` 26, `directions/agent-memory` 21, `directions/plain-files-and-wikis` 18) |
| Projects the first snapshot missed | `landscape/...-selection.md` lists seven (codebase-memory-mcp, MIRIX, Zep, OntoGPT, GLiNER, DeepKE, the OKF specification) as missing, "to be tracked from the next snapshot" | the newest snapshot holds all seven, and holds the repository of every one of the 77 entries (checked 20261102): the page is out of date and says so nowhere |

### 2.3 Navigation

The site navigation is generated from the folder tree (`docs-site/mkdocs_hooks.py`). Today:

| Chapter 1 position | Section | Pages | Comment |
|---|---|---|---|
| 1.1 | Primer | 1 | |
| 1.2 | LLM era | 1 | timeline plus the duplicate "shifts" |
| 1.3 | Literature | 1 | a July review, overlapping 1.6 |
| 1.4 | Projects | 79 | 77 entries, the index and **the template** |
| 1.5 | Landscape | 3 | two snapshots and the selection |
| 1.6 | Papers and benchmarks | 1 | one 6,500-word page |
| **1.7** | **Directions** | 10 | **the answer to "what is the state of the art" is seventh of eight** |
| 1.8 | Experiments | 11 | run logs and proposals |

Also: `_TEMPLATE.md` pages are published and show in the sidebar ("<Project>: what Pinakes takes from it");
`pinakes/experiments` is labelled "Measured" next to `kb-kg/experiments` "Experiments"; the home page is the
project README, which describes the repository's status and conventions but does not say where to start.

### 2.4 Existing machinery that the proposal builds on

| Exists | Use |
|---|---|
| `tools/build_projects_index.py` (front matter to generated index, `--check`) | extend; copy its pattern for papers |
| `tools/gh_snapshot.py` snapshots: `repos.tsv` has stars, forks, licence, last push, release, 90-day commits, contributors, flags, GitHub description for each tracked repository | the *live* numbers; join on `repo`, so no entry has to restate them |
| link rewriting and strict build (`docs-site/`) | catches broken links and anchors after any move |
| **Gap:** `.github/workflows/docs.yml` does **not** run `build_projects_index.py --check` | the generated index can go stale unnoticed today |

## 3. Principles

1. **One home per fact** (already a rule in `DECISIONS.md`); here it becomes enforceable.
2. **Every page has one job**: *registry* (rows, generated), *analysis* (reading of the evidence), *evidence*
   (ledgers with sources and read times), *history*, or *process*. A page that does two is split.
3. **Live means generated from data**, with its date, its counts and its change feed printed by the generator, so a
   count cannot go stale.
4. **Link, do not copy.** Prose names a project or paper and links to its row or entry. A figure that
   argues a point may be quoted with its link; a figure that merely describes (stars, versions, counts) is not.
5. **Gates, not notes.** A generated page has a `--check`; a duplicate-figure scan only ratchets down.
6. **Keep every path.** `kb-kg/...` URLs are already linked from the Pinakes repository (D-23, the 16
   "historical copy" banners). Which paths those banners name: **unstated** (I did not read that repository;
   editing it needs your explicit yes). Renaming is therefore not in this proposal.

## 4. Target structure

No directory is renamed. New files are marked **NEW**, generated files **GEN**.

```
README.md                           front door: three reader paths, what is live, how it is kept   (rewritten)
kb-kg/
  README.md                         one map, by reader question; no counts, no state column         (rewritten)
  changes.tsv                NEW    one row per change: date, kind, subject, one line, source, read time
  directions/README.md              "The field now": one screen per direction + notable projects + key papers
  directions/*.md (9)               analysis; numbers by link, not by copy
  projects/README.md         GEN    LIVE: notable first, then by category; stars etc. from the latest snapshot
  projects/<entry>.md (77)          unchanged body; front matter gains `summary` and `directions`
  papers-benchmarks/README.md       LIVE landing: counts, shortlist, recent changes, how to add     (rewritten)
  papers-benchmarks/papers.tsv NEW  data: ~70 rows today
  papers-benchmarks/papers.md  GEN
  papers-benchmarks/benchmarks.tsv NEW  data: 28 rows today
  papers-benchmarks/benchmarks.md GEN
  papers-benchmarks/studies.md NEW  analysis: "does a graph help" ledger + "what benchmarks do not measure"
  llm-era/README.md                 timeline and sources only
  primer/README.md                  unchanged
  literature/graph-rag-research.md  provenance of the July review; banner, no duplicated tables
  landscape/                        data (snapshots) and nothing else; selection merged into projects landing
  experiments/                      unchanged until phase 3
pinakes/                            tree unchanged; state columns removed from its README
DECISIONS.md, RESUME.md             phase 3
tools/build_papers_index.py  NEW    with tests, same pattern as build_projects_index.py
tools/check_single_home.py   NEW    ratchet scan (section 8)
```

### Page types

| Type | Pages | Rule |
|---|---|---|
| Registry (live) | `projects/README.md`, `papers.md`, `benchmarks.md` | generated; never edited by hand; `--check` in CI |
| Entry | 77 project entries, 12 Pinakes takeaways | one project, full detail; only place for that project's own figures |
| Analysis | 9 direction pages, `studies.md`, `evidence-and-claims.md` | readings, always labelled; point to registries |
| Evidence/provenance | `literature/`, `landscape/`, source lists | kept for audit; banner says "not the current state" |
| History | `primer/`, `llm-era/` | dated events only |
| Process | `DECISIONS.md`, `RESUME.md`, `experiments/` | the notebook; off the main reading path |

## 5. The two live sections

### 5.1 Projects (`kb-kg/projects/README.md`, generated)

**Header printed by the generator**: counts by tier and category, "stars as of <snapshot time> (<N> days old)",
last change from `changes.tsv`, and the "how to update" box.

**Data**: entry front matter (`slug`, `repo`, `tier`, `category` exist; add `summary`, at most 25 words, and
`directions`, a list of the nine direction slugs) joined with the newest `landscape/*/repos.tsv` on `repo`
for stars, last push, licence, release and flags. The repository of every entry is in the newest snapshot
today (checked); if one is ever missing its cells show "not in snapshot" and nothing is invented. Until an
entry has a `summary` the generator falls back to the GitHub description from the snapshot, so the
roll-out can be incremental.

**Layout**: (1) *Notable now*: the 22 deep entries (rule below), grouped by category; (2) the full table by
category with columns Project, one line, direction, stars, last push, licence, tier; (3) a "by direction"
view from the tags; (4) *Recent changes* (last 15 rows of `changes.tsv` with kind `new-entry`, `feature`,
`licence`, `status`); (5) "How the list is chosen" and "Left out" (the 162-line selection page, shortened and brought up to date).

**Notability rule**: *notable = deep tier*, which is decision D-12 ("a deep dive only for those that matter
most"). It is an editorial call, labelled as such; stars are shown as a signal, not used to rank.

### 5.2 Papers and benchmarks (`kb-kg/papers-benchmarks/`)

**Data**: `papers.tsv` columns `arxiv, title, authors, date_v1, venue, kind, direction, idea, repo,
repo_cites_id, depth, read_utc, source_url, notable`. `kind` is survey, method or study; `depth` is
full text, abstract or listing only, so the "abstract only / listing only" caveats of the current page become a
column and cannot contradict a fuller read elsewhere. `benchmarks.tsv` columns `name, task, size, metric,
tests, used_by, link, depth, read_utc`.

**Load**: extracted from the current tables by script; **round trip checked** (every arXiv id, venue, date and
repo in the old page must appear in the TSV; the old page stays in git history).

**Layout**: `README.md` is the landing (counts, the `notable` shortlist with its reason, recent changes, how to
add); `papers.md` is the full table by kind and direction; `benchmarks.md` is the benchmark table;
`studies.md` is the curated ledger of independent graph-versus-plain comparisons (current §3 merged with
`literature` §3, one row per study at its deepest read depth) followed by "what the benchmarks do not
measure" (current §5).

**Notability for papers**: an editorial flag with a stated reason. For orientation only, the papers
referenced most often in this repository today (a measure of how much the repo cites them, not of
importance): 2610.30755 (9 files); 2502.11371, 2502.14802, 2506.05690, 2404.16130, 2405.14831, 2501.13956,
2502.12110, 2504.19413 and 2603.27277 (4 files each; the last one's title not looked up); 2609.18099 and
2508.06105 (3 each). The table's rows would carry a stated reason instead.

### 5.3 How an update is requested and done

| You ask for | The edit | Then |
|---|---|---|
| a new paper or benchmark | one row in `papers.tsv` or `benchmarks.tsv` | `uv run tools/build_papers_index.py` |
| a new project | a new entry from `_TEMPLATE.md` (with `summary`, `directions`) | `uv run tools/build_projects_index.py` |
| a new feature or change of a project or paper | one row in `kb-kg/changes.tsv` (the entry keeps the detail) | rebuild both |
| fresher stars | `uv run tools/gh_snapshot.py` | rebuild |

Freshness is honest: the generator prints the snapshot age and warns when it is over 30 days. It cannot
make the stars newer than the last snapshot. The two existing snapshots are minutes apart (`RESUME.md`), so
today's "stars" column would show one date.

## 6. What moves where

| Current content | New home | Then the old page |
|---|---|---|
| `papers-benchmarks` §1-2 (68 rows) | `papers.tsv` / `papers.md` | landing page |
| `papers-benchmarks` §3 (13 rows) and `literature` §2.3, §3 | `studies.md` | pointer |
| `papers-benchmarks` §4 (28 rows) | `benchmarks.tsv` / `benchmarks.md` | |
| `papers-benchmarks` §5 (13 rows) | `studies.md`, second half | |
| `llm-era` §3 six shifts | the matching direction page (after a diff: only text the direction page lacks moves) | a six-line index |
| `llm-era` §4 open questions | `directions/README.md`, one deduplicated list (together with the questions the experiments page already poses) | pointer |
| `llm-era` "created in 2026 by stars" | the live Projects table | link |
| `literature` §4 prior-art table | the live Projects table | deleted (July stars are stale) |
| `landscape/...-selection.md` | Projects landing, "How the list is chosen" and "Left out" | removed from nav, file kept |
| per-project rows with stars and versions inside direction pages | the entry; the direction page keeps the project's role in that direction | link |
| README layout block, `kb-kg/README` and `pinakes/README` state columns | one map in `kb-kg/README.md`; no state | |

## 7. Navigation and front door

- **Chapter 1 order** (`SECTION_ORDER` in the hook): Directions ("the field now"), Projects, Papers and
  benchmarks, Primer, LLM era, Literature, Landscape, Experiments. Pinakes stays chapter 2.
- **Do not publish `_TEMPLATE.md` pages** (stage them out; links to them already fall back to GitHub through
  the hook). Needs a test in `docs-site/test_stage_docs.py`.
- Rename the label "Measured" to "Pinakes measurements". Put `recommendations-r1-r7.md` right after `approach/`.
- **Home page** (`README.md`): what this is in two sentences; three paths ("what is happening now" ->
  Directions; "names" -> Projects, Papers, Benchmarks; "background" -> Primer, Timeline); one line on what
  is live and how it is kept; licence. Conventions move to `kb-kg/README.md`. No status, no counts.
- Keeping the 77 entries in the sidebar is acceptable: Material collapses nested sections by default, so they
  show only when the Projects node is open (its default behaviour; not checked in a browser). Whether
  Material's `navigation.prune` is available in the pinned version: **unchecked**. Hiding pages from the nav
  would also trip `--strict`, because `mkdocs.yml` sets `omitted_files: warn`; that is why this proposal
  reorders the nav and does not hide pages.

## 8. Keeping it single-home

| Gate | What it does | When it fails |
|---|---|---|
| `build_projects_index.py --check`, `build_papers_index.py --check` as steps in `docs.yml` | the generated pages equal what the data produces | any hand edit or forgotten rebuild. **Today CI runs neither.** |
| `tools/check_single_home.py` | counts (a) star figures in prose outside project entries and snapshots (79 in 10 files today, 65 of them in three pages), (b) entry-count phrases outside generated pages (4 files today) | the count goes **up** against a stored baseline; it may only go down |

Proposed text for the repository `CLAUDE.md` (your call; shown here, not applied):

```
## Live sections
- Projects: new entry from `kb-kg/projects/_TEMPLATE.md`, then `uv run tools/build_projects_index.py`. Papers and benchmarks: a row in `kb-kg/papers-benchmarks/papers.tsv` or `benchmarks.tsv`, then `uv run tools/build_papers_index.py`. A new feature or change: one row in `kb-kg/changes.tsv`.
- Generated pages are never edited by hand; their `--check` must exit 0.
- A star count, a paper's metadata or an entry count lives in one place; elsewhere link to it.
```

## 9. Options

| | A. Minimal | **B. Layered (recommended)** | C. Rebuild as a linear book |
|---|---|---|---|
| What | Generate the two live pages; replace duplicated prose by links | A, plus "The field now", `studies.md`, benchmarks page, nav order, front door, gates, process pages trimmed in phase 3 | Re-chapter the whole repository in tutorial order and rename directories |
| Fixes "I can't find the state of the art" | partly (still seventh in the sidebar) | yes | yes |
| Fixes duplicates and drift | partly (no gate) | yes, with gates | yes |
| Fixes navigation | no | yes | yes |
| Breaks links | none | none (7 anchored links into `papers-benchmarks/README.md` are edited) | most of 131 pages, and links already published from the Pinakes repository |
| Files touched (my estimate) | about 25 | about 40, plus 77 front-matter lines by script | about 130 (all pages) |
| Needs peers' held files | no | phase 3 only | yes, immediately |
| Real cost | small | medium: one generator with tests, one extraction with a round-trip check, about 12 pages written or rewritten (estimate; no token cost measured) | high, and an edit to the Pinakes repository |

**Recommendation: B.** It removes the three symptoms you named without renaming anything. Its real cost is the
papers extraction: the current tables carry judgement in their cells ("README: **no**", "title only"), and the
round-trip check has to prove none of it is lost. Option A is the fallback if you want only the two pages.

## 10. Phases and holds

The experiments sessions hold `RESUME.md`, `DECISIONS.md`, `kb-kg/experiments/**`, `tools/exp/**` and
`tools/metering_gateway.*` until their overnight run is committed (estimate 06:00 to 12:00 UTC on 20261103;
their commit message will say "pass A complete, RESUME/DECISIONS free"). They asked that any move of
`kb-kg/experiments/**` or its anchors land in **one commit announced to them first**, and that their worktree
`worktree-20261030_1852-kb-kg-docs-scaffold` is not touched.

| Phase | Content | Touches held files? | Verification |
|---|---|---|---|
| 1 Registries | `papers.tsv`, `benchmarks.tsv`, `build_papers_index.py` with tests; extend `build_projects_index.py` (snapshot join, `summary`, `directions`); `changes.tsv`; new landing pages; nav hook change; CI `--check` steps | no | round-trip check of the extraction; unit tests; `mkdocs build --strict`; `check_public_safe.sh` |
| 2 De-duplication | `studies.md`; `llm-era` and `literature` trimmed; `directions/README.md` as "The field now"; star figures replaced by links in direction pages; home page and maps rewritten; `check_single_home.py` baseline | no | strict build; before/after counts of the scan; a reader walk-through of the three paths |
| 3 Process pages | `RESUME.md` reduced to state and next step; `DECISIONS.md` rows D-21 to D-26 reduced to the decision plus a pointer (the narrative stays on the experiments pages); experiments README split of plan and log | **yes**, after the experiments session's final commit | one commit, announced beforehand; strict build |

Phases 1 and 2 are independent of the run and can start on your yes. Each is a set of small commits in my
worktree, pushed only after the public-safety gate exits 0.

## 11. Risks and what I did not check

| Risk or gap | Handling |
|---|---|
| The extraction loses judgement kept in table cells | round-trip check; old page stays in git history |
| "Notable" is subjective; stars mislead (63.9% of stars sit in the "adjacent" category per `directions/agent-memory`) | deep tier as the rule, labelled editorial; stars shown but not ranked |
| Live pages are only as fresh as the last snapshot | age printed; 30-day warning |
| A concurrent session edits an entry while I add front matter | front matter is the first lines of each file, so a rebase is trivial; I re-fetch before each commit |
| The safety gate cannot check private names in a fresh worktree (the list is gitignored; open item 3 in `RESUME.md`) | copy the local list into the worktree before any commit; do not print it |
| Not checked: the full text of the nine direction pages and of the 77 entries (I read headings, summaries, `agent-memory` in part, and 6 entries' structure); the `llm-era` to direction mapping is from titles and one example (Mem0's add-only write path appears in both), so phase 2 starts with a diff | stated; no claim relies on the unread parts |
| Not checked: which `kb-kg/` paths the Pinakes banners link to; whether the pinned Material version has `navigation.prune` | read-only check of the Pinakes repository only with your yes |

## 12. Decisions I need from you

1. **Option** A, B or C (recommended: B).
2. **Notability**: deep tier for projects; an editorial flag with a reason for papers.
3. **Benchmarks on their own page** (recommended; matches the question you put to another session).
4. **`CLAUDE.md` text** in section 8: yes or no.
5. **Start phases 1 and 2 now**, on unheld files, or wait for the whole run?
6. Phase 3 edits `DECISIONS.md`, your record of decisions: confirm that shortening D-21 to D-26 to the
   decision plus a pointer is acceptable, or exclude those rows.
