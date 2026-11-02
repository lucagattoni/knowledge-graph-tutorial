# Plan: a new documentation, written from scratch

**Status: plan for the owner's approval, written 20261102 19:15 UTC. Nothing is written yet.** It replaces
[the restructuring proposal](20261102_1812-docs-restructure-proposal.md): the owner chose not to restructure
the existing pages but to write a new documentation from scratch and use the existing pages as sources.
Every structural choice below is the owner's answer to a question asked on 20261102 after 18:12 and before
19:15 UTC; where this plan proposes something not yet answered, it says **proposed**.

## 1. Decisions recorded

| # | Question | Owner's answer |
|---|---|---|
| S-1 | Approach | Write from scratch. Do not restructure the existing documentation; use it as a source. |
| S-2 | Location | New top-level folder `docs/`. Its landing page is the site's home; the repository README points to it. The existing pages stay, unedited, reachable from an "Archive" link. |
| S-3 | Evidence | Facts a chapter's argument rests on, and every 2026 fact, are re-verified against the primary source and cited with the new read time. Other facts keep the original source and read time. |
| S-4 | Order | 1 History, 2 Trends, 3 Projects, 4 Papers, 5 Datasets, 6 Benchmarks, 7 Experiments, 8 Pinakes. The A-Z index is a tab in every page's header. Archive last. |
| S-5 | Live chapters | Projects, Papers, Datasets and benchmarks, Trends: updated on request, each with a dated list of changes. |
| S-6 | Start | A pilot (chapter 1 overview, one era, one trend, the index pages they need), reviewed in a **local preview** before anything else is written or published. |

**Chapter 1, History**

| # | Question | Owner's answer |
|---|---|---|
| H-1 | Layering | Hybrid: an overview on top, eras as the spine, the index as the second axis. Era pages link to index pages and do not redefine concepts. |
| H-2 | Start | Early AI (roughly the 1950s to 70s). |
| H-3 | Reader | The owner, refreshing; plus a Wikipedia-like index of definitions with links ("like a KB"). |
| H-4 | Threads | KB/KG is the main thread; ontologies and semantic web, databases and search, RAG and agent memory are side threads with lanes of their own. |
| H-5 | Boundary with chapter 2 | Chapter 1 holds what is settled; anything still moving is chapter 2, whatever its date. |
| H-6 | "Settled" | Superseded or standard: it became a standard, was absorbed into common practice, or was replaced by a successor. **Consequence:** a trend that settles moves from chapter 2 to chapter 1. |
| H-7 | Eras | Derived from cited surveys and histories, each boundary with its reason; the owner approves. |
| H-8 | Building blocks of an era | Dated events; systems and projects; ideas and disputes; papers and standards. |
| H-9 | Overview | One-screen prose, a timeline with one lane per thread, and an era summary table. |

**Index (the concept KB)**

| # | Question | Owner's answer |
|---|---|---|
| I-1 | Shape | One page per entry, plus a generated A-Z page and generated "appears in" lists. |
| I-2 | Kinds of entry | Concepts; systems and projects; standards and formats. Not people or organisations. |
| I-3 | Links | Plain links in the text; no relation types. |
| I-4 | Which concepts | Every term the chapters use without explaining it inline; the list is proposed for approval. |
| I-5 | Projects | One page per project, in the projects chapter; the index lists it and links there ("one page, two doors"). |

**Chapter 2, Trends**

| # | Question | Owner's answer |
|---|---|---|
| T-1 | Unit | A family of approaches, told as a shift: each subchapter is a family and opens with the move it represents ("from X to Y"). |
| T-2 | Theme subchapters | Infrastructure and MCP; features removed and added. (Licensing and evidence are not subchapters.) |
| T-3 | Which trends | Two stated tests (sustained activity in the dated sources; an idea no other trend covers); a proposed list with a reason each; the owner approves. |
| T-4 | Distinctive | A comparison table across all trends, and a "distinctive because" box per trend. |
| T-5 | Why | Why it is distinctive, why it emerged, why it matters. |
| T-6 | Evidence and licence | Columns of the comparison table, and a "what is measured, and by whom" section per trend. |
| T-7 | Stance | A labelled verdict: claims, measurements, and a short assessment marked as a reading. |
| T-8 | Projects in trends | Each trend names its representative projects and links to their pages in chapter 3. |

**Chapters 3 to 8**

| # | Question | Owner's answer |
|---|---|---|
| P-1 | Project pages | For projects passing stated tests (sustained activity in dated GitHub snapshots, a distinct approach, use by a trend); proposed list, owner's approval. |
| P-2 | Projects table | Live; a wider watch list from the dated GitHub snapshots, linking to a page where one exists. |
| R-1 | Fundamental papers | Any of: origin of an approach; turning point; widely built on (from a named citation source with its date); survey of record. Proposed list with a reason each; owner's approval. |
| R-2 | Grouping | One group per chapter 2 trend, plus one Foundations group for papers that predate every trend. |
| R-3 | Span | All eras. |
| R-4 | Connections | Relation lines per paper (builds on, answers, evaluates) and one map of the whole chapter. |
| R-5 | Other papers | A further-reading list per group, one line per paper. |
| D-1 | Kinds of dataset | Knowledge graphs as data; question sets; text corpora. Not ontologies or schemas. |
| D-2 | Dataset and benchmark | Split by definition. The dataset page holds the data (content, size, licence, how made); the benchmark page holds the evaluation (tasks, metrics, protocol, results). An item that is both has one of each, linked, nothing repeated. |
| D-3 | Which ones | Used by a fundamental paper, used by a trend, or widely used; proposed list, owner's approval. |
| D-4 | Granularity | A page each; the chapter landing lists them by kind. |
| B-1 | Results | A dated results table: system, score, who ran it (first-party marked), date, source. |
| X-1 | Experiments | Own chapter, written from scratch; each experiment linked from the trend it tests. |
| K-1 | Pinakes | Own final chapter, written from scratch, linking into the field chapters for facts. |

## 2. Structure

```
docs/
  README.md                  home: what this is, the eight chapters, what is live and how it is kept
  history/                   1. History
    README.md                overview: prose, timeline with four lanes, era table
    <era>.md                 one per era (list from step 0, owner approves)
  trends/                    2. Trends
    README.md                overview, comparison table, the trend list with its tests
    <family>.md              one per trend (list from step 0, owner approves)
    infrastructure-and-mcp.md
    features-in-and-out.md
  projects/                  3. Projects
    README.md                live watch-list table (generated) and changes
    <project>.md             one per project passing P-1
  papers/                    4. Papers
    README.md                the map of the chapter, the groups, changes
    foundations.md           papers that predate every trend
    <trend>.md               one per trend: a section per fundamental paper, then further reading
  datasets/                  5. Datasets
    README.md                list by kind (KGs, question sets, corpora), changes
    <dataset>.md             one per dataset
  benchmarks/                6. Benchmarks
    README.md                list by task, changes
    <benchmark>.md           one per benchmark
  experiments/               7. Experiments
  pinakes/                   8. Pinakes
  index/                     the A-Z tab
    README.md                generated A-Z
    <entry>.md               one per concept, system or standard (projects live in projects/)
```

Archive: `kb-kg/`, `pinakes/` (the old one at the repository root) and `DECISIONS.md` stay where they are,
unedited, published under an "Archive" section after the new chapters. The old `pinakes/` and the new
`docs/pinakes/` are different folders.

## 3. Page templates (proposed, for approval)

**Era page (chapter 1)**: dates and why the boundaries sit there · what changed, one paragraph · each
thread in this era (KB/KG; ontologies and semantic web; databases and search; RAG and agent memory), only
where something happened · dated events table · systems and projects · ideas and disputes · papers and
standards (one line each, linking to the papers chapter) · what was left unsolved, leading into the next
era · sources.

**Index page**: front matter (`kind`: concept, system or standard; `aliases`; first appearance with its
source) · definition, one paragraph · how it changed, dated · where sources disagree · related entries
(plain links) · appears in (generated) · sources.

**Trend page (chapter 2)**: title "Family: from X to Y" · distinctive-because box (two or three lines, naming
its nearest neighbour) · why it emerged (the problem or earlier failure, linking to chapter 1) · why it
matters · how it works · representative projects (links to chapter 3) · fundamental papers (link to the
group in chapter 4) · what is measured, and by whom · assessment (labelled as a reading: strengths,
weaknesses, where it is heading) · signals to watch · changes (dated) · sources.

**Comparison table columns (proposed)**: trend · shift (from, to) · what is built or stored · when a model
is used (indexing, query, none) · who steers retrieval (a fixed pipeline or an agent) · cost profile ·
evidence (independent, first-party only, none) · predominant licences of the representative projects ·
status (growing, steady, settling).

**Project page (chapter 3)**: header (repository, licence from the `LICENSE` file, the trend it belongs to;
stars, last push and release taken from the newest snapshot, not typed by hand) · what it is · how it
works · evidence · status and direction · changes · sources.

**Paper section (chapter 4)**: title, authors, venue, first-version date, link · the test it passes (R-1)
and why · the idea in two or three sentences · relation lines: builds on, answers, evaluates (links) ·
read depth (full text, abstract, listing) and read time.

**Dataset page (chapter 5)**: kind · content and size · licence · how it was made, versions · used by
(papers, trends, benchmarks) · known problems · its benchmark page, if any · sources.

**Benchmark page (chapter 6)**: tasks · metrics and protocol · datasets used (links) · results table (B-1) ·
known problems · used by · sources.

## 4. Live chapters (proposed mechanism)

- **Data, not prose, for anything that changes**: one `changes.tsv` per live chapter (date, kind, subject,
  one line, source, read time); the newest snapshot under `kb-kg/landscape/` for stars and activity (the
  snapshot tool stays as it is).
- **One generator** (`tools/build_docs.py`, with tests) writes the projects watch-list table, the change
  lists, the A-Z page and the "appears in" lists. Its `--check` runs in CI, so a stale generated page fails
  the build. Today CI runs no such check for the existing projects index.
- **An update on request** is a row in the chapter's `changes.tsv`, the page edit it describes, and a
  rebuild. A trend that settles (H-6) moves to chapter 1 with a dated change row.

## 5. Site

- The home page becomes `docs/README.md`; the nav lists the eight chapters, then Archive.
- The A-Z index as a tab in every page's header: how to do it in the Material theme (a header link
  through a theme override, or the theme's tabs feature, which turns every top-level section into a tab)
  is **unverified**; the pilot settles it.
- The strict build keeps failing on any broken link or anchor, in the new pages and the archive alike.

## 6. Steps

| Step | What | Needs from you | Touches |
|---|---|---|---|
| 0 Research | (a) the eras, from cited surveys and histories, with boundaries and reasons; (b) the trend list, by the two tests, with reasons and the evidence; (c) the index entries the pilot needs; (d) your verdict on the templates and columns above | approval of (a), (b), (c), (d) | nothing in the repository but `plans/` |
| 1 Pilot | site wiring (home, Archive, index tab); the chapter 1 overview; one era; one trend; their index pages; the generator for the A-Z and "appears in" lists | review in a local preview | `docs/`, `mkdocs.yml`, `docs-site/`, `tools/build_docs.py`, `README.md` |
| 2 Chapters 1-2 | the other eras and trends, the two theme subchapters, the comparison table | approval of the result | `docs/history/`, `docs/trends/`, `docs/index/` |
| 3 Chapters 3-6 | project list (P-1) and pages, the live table; paper list (R-1), groups, map; dataset and benchmark lists (D-3) and pages | approval of each list before its pages are written | `docs/projects/`, `docs/papers/`, `docs/datasets/`, `docs/benchmarks/` |
| 4 Chapters 7-8 | experiments (after the X2 run is recorded); Pinakes | approval of the result | `docs/experiments/`, `docs/pinakes/` |

How each step is done: writer agents on Sonnet, one per page or small group of pages, each briefed with its
template, its sources in the archive and the evidence rule (S-3). I check every page before it is
committed: the load-bearing facts against their primary sources, the links, the strict build, and
`tools/check_public_safe.sh`. Nothing is pushed before you approve the pilot; after that, each step is
pushed when it builds and you have approved it.

## 7. Coordination

- `docs/` is new, so no other session holds it. The archive pages are never edited by this work.
- The site wiring in step 1 changes `mkdocs.yml` and `docs-site/`, which the other sessions do not hold but
  whose strict build they rely on: they are told the file set before it lands.
- The experiments session holds `RESUME.md` and `DECISIONS.md` until its run is recorded (main was at
  `f2e87e6` at 19:15 UTC). This plan's decisions go into `DECISIONS.md` as one row, at the next free
  number, after that hold ends.

## 8. Open, and not checked

- The eras, the trend list and the index entries are not known yet: step 0 produces them for approval.
- How many pages each chapter will have is unknown until step 0; no cost estimate is given.
- The index-tab mechanism (section 5) is unverified.
- `tools/check_public_safe.sh` passes without checking private repository names: the gitignored list it
  reads does not exist in this checkout or in the primary one (open item 3 in `RESUME.md`).
