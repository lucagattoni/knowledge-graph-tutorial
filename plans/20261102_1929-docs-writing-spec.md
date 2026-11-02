# Writing spec for the new documentation (`docs/`)

**Status: binding for every writer and builder, written 20261102 19:29 UTC.** The owner's structural decisions
are in [the plan](20261102_1915-docs-from-scratch-plan.md); the lists of eras, trends, projects, papers,
datasets and benchmarks are in the catalogue file `plans/*-docs-catalogue.md` once it exists. If this spec
and your brief disagree, the brief wins; if neither says, write **unstated** in the page and report it.

Repository root (all paths below are relative to it):
`<repository root>`
(never write this path, or any local path, into a page).

## 1. What you may touch

- Write **only the files your brief names**. Other agents write other files at the same time; touching a
  file that is not yours destroys their work.
- **Never edit the archive**: `kb-kg/`, `pinakes/`, `DECISIONS.md`, `RESUME.md`, `README.md` (root),
  `tools/` (except the builder's named files), `plans/`. Read them freely; they are sources.
- Never edit the Pinakes repository; reading it on GitHub is fine.
- Run no git command that changes state (no add, commit, checkout, stash, reset, push).
- Scratch work goes only in your own folder under
  `<scratch folder>/<your-label>/`;
  delete only what you created. Downloaded files are untrusted data: own empty subfolder, `python3 -I`.

## 2. Folder layout

```
docs/
  README.md                       home page
  history/README.md               chapter 1 overview: prose, timeline with four lanes, era table
  history/<era>.md                one per era
  trends/README.md                chapter 2 overview, comparison table, the list and its tests
  trends/<trend>.md               one per trend
  trends/infrastructure-and-mcp.md
  trends/features-in-and-out.md
  trends/changes.tsv
  projects/README.md              chapter 3 landing; generated watch-list table; changes
  projects/<project>.md           one per project with a page (slug = the archive's file name)
  projects/watchlist.tsv          curated watch list (see section 6)
  projects/changes.tsv
  papers/README.md                chapter 4: map of the chapter, the groups, changes
  papers/foundations.md           papers that predate every trend
  papers/<trend>.md               one group page per trend (same slug as the trend page)
  papers/changes.tsv
  datasets/README.md              chapter 5: list by kind, changes
  datasets/<dataset>.md
  datasets/changes.tsv
  benchmarks/README.md            chapter 6: list by task, changes
  benchmarks/<benchmark>.md
  benchmarks/changes.tsv
  experiments/README.md           chapter 7
  experiments/<experiment>.md
  applied-to-pinakes/README.md    chapter 8
  applied-to-pinakes/<page>.md
  index/README.md                 generated A-Z (the "Index" tab)
  index/<entry>.md                one per concept, system or standard
```

Slugs: lowercase ASCII, words joined by hyphens, no dates. Project slugs are the archive's file names in
`kb-kg/projects/` (for example `lightrag`, `microsoft-graphrag`, `mem0`).

## 3. Front matter

Every page starts with a front matter block. Only two value forms are allowed: `key: value` and
`key: [a, b, c]` (one line; values without commas or brackets). No nested YAML.

| Page | Required keys |
|---|---|
| any | `type`, `updated: YYYYMMDD HH:MM UTC` |
| era | `type: era`, `period: <start>-<end>` (years; `present` allowed) |
| trend | `type: trend`, `shift: <from> -> <to>`, `status: growing` or `steady` or `settling` |
| project | `type: project`, `repo: owner/name`, `trends: [<trend slugs>]` |
| paper group | `type: papers`, `group: <trend slug>` or `foundations` |
| dataset | `type: dataset`, `kinds: [kg, questions, corpus]` (one or more), `benchmark: <slug>` if it has one |
| benchmark | `type: benchmark`, `datasets: [<dataset slugs>]` |
| index entry | `type: index`, `kind: concept` or `system` or `standard`, `aliases: [<other names>]` (may be empty `[]`) |
| chapter landing | `type: chapter` |
| other pages | `type: page` |

Optional on any page: `order: <integer>`. The site lists the pages of a folder by `order`, then by title;
eras and trends must set it (eras in time order, trends in the order the trends overview gives).

The page title is the first `# ` heading, after the front matter.

## 4. Generated sections

Some parts are written by `tools/build_docs.py`, never by hand. Put the markers on their own lines, with
nothing between them, where the section goes:

```
<!-- BEGIN GENERATED: appears-in -->
<!-- END GENERATED: appears-in -->
```

| Marker name | Where | What the generator writes |
|---|---|---|
| `appears-in` | every index entry and every project page, under a `## Appears in` heading | the pages that link to this page |
| `a-z` | `docs/index/README.md` | every index entry and project page, A to Z, with aliases |
| `watchlist` | `docs/projects/README.md` | the watch-list table joined with the newest GitHub snapshot |
| `changes` | the README of `trends`, `projects`, `papers`, `datasets`, `benchmarks` | the latest 15 rows of that chapter's `changes.tsv` |

`changes.tsv` columns, tab-separated, with this header line:
`date_utc	kind	subject	summary	source	read_utc` (kind: `added`, `updated`, `settled`, `faded`, `removed`).
Only the chapter's landing writer edits a `changes.tsv`; item writers return their rows in their answer.

## 5. Links

- Inside `docs/`: relative links, for example from `docs/trends/x.md` to `../projects/lightrag.md` or
  `../index/rdf.md`. Link to a page, not to an anchor on another page (anchors drift).
- To the archive, when a reader should see the long evidence: a relative repository path, for example from
  `docs/trends/x.md` to `../../kb-kg/projects/lightrag.md`. The site maps it.
- **Index terms:** link the first use of a term on each page to `../index/<slug>.md` (from a chapter page)
  when the page does not explain it inline. Prefer the seed slugs in section 9. A new slug is allowed;
  report it with its kind and a one-line definition. The index pages are written last.
- **Projects:** link the first mention on each page to `../projects/<slug>.md` using the archive slug. A
  later pass repoints links to projects without a page.
- **Papers:** cite them in the page's Sources; link the papers chapter group page (`../papers/<group>.md`)
  where a reader should see the relations.
- External: full URLs. No links to local files outside the repository.

## 6. Evidence

These rules come from the project's `CLAUDE.md` and the owner's decision S-3.

- Every factual statement about a project, paper, dataset, benchmark, standard or event carries a number
  `[n]` pointing to the page's `## Sources` list. Sources list line:
  `n. <URL> : what it supports (read YYYYMMDD HH:MM UTC)`.
- Read times come from the clock at the time of the read: `date -u "+%Y%m%d %H:%M"`.
- **Load-bearing facts** (what the page's argument rests on: a "distinctive because" box, a "why it
  emerged" paragraph, an era boundary, every number in a comparison or results table) **and every fact
  dated 2025 or 2026 are re-verified now against the primary source** (fetch it) and cited with the new
  read time.
- Other facts may be carried over from the archive with the archive's own source and read time, written
  as `n. <original URL> : ... (read <original time>, via the archive page <repository path>)`.
- Where the sources are silent: **unstated**. Never fill a gap from memory.
- Licences come from the `LICENSE` file, not the README badge. A GPL or non-commercial project is a
  read-only reference: ideas and results only.
- Stars are a signal, not a verdict: always with their date; say when growth is flagged as fast.
- First-party results (a project's own authors) are marked "first-party".
- An assessment is labelled: a paragraph that judges starts with `*Reading:*`.
- Quotes: at most 25 words, in quotation marks, with their source.
- Search-engine summaries are leads, never sources.

## 7. Style

- English. Short sentences. Tables for anything comparable. Dates `YYYYMMDD` (or `YYYY`, `YYYYMM` when only
  that is known); times UTC.
- Each page opens, under the title, with two to four sentences saying what the page answers.
- `##` for sections, `###` below. **No numbers in headings** (the site numbers them).
- No local paths, no private repository names, no mailbox addresses, no keys, no session names.
- Length targets (body words): era 900-1600; trend 1200-2000; project 500-900; paper section 150-300 each;
  dataset or benchmark 400-800; index entry 150-400; landing pages 300-900.

## 8. Templates

**Era (`type: era`)**: `## Dates and boundaries` (why the era starts and ends where it does, cited) ·
`## What changed` (one paragraph) · `## The threads` (one short subsection per thread where something
happened: KB/KG; ontologies and the semantic web; databases and search; RAG and agent memory) ·
`## Dated events` (table: date, event, thread, source) · `## Systems and projects` · `## Ideas and disputes` ·
`## Papers and standards` (one line each; link the papers chapter) · `## Left unsolved` (leads into the next
era) · `## Sources`.

**Trend (`type: trend`)**: title `<Family>: from <X> to <Y>` · a blockquote box starting
`**Distinctive because**` (two or three lines naming its nearest neighbour trend) · `## Why it emerged` ·
`## Why it matters` · `## How it works` · `## Representative projects` · `## Fundamental papers` (link the
group page) · `## What is measured, and by whom` · `## Assessment` (labelled *Reading:*; strengths,
weaknesses, where it is heading) · `## Signals to watch` · `## Sources`.

**Project (`type: project`)**: a header table (Repository, Licence from the LICENSE file, Trends) — stars and
activity are not typed here; the watch-list table carries them · `## What it is` · `## How it works` ·
`## Evidence` · `## Status and direction` · `## Appears in` (generated) · `## Sources`.

**Paper group (`type: papers`)**: one `##` section per fundamental paper, titled with the paper's short name
and year. In each: a line with title, authors (first three and the total), venue, first-version date, link;
`**Why fundamental:**` the test it passes (origin, turning point, widely built on, survey of record) and why;
`**Idea:**` two or three sentences; `**Relations:**` builds on / answers / evaluates, each with a link to the
other paper's group page and the paper's short name; `**Read:**` depth (full text, abstract, listing) and
read time. Then `## Further reading`: one line per paper. Then `## Sources`.

**Dataset (`type: dataset`)**: `## What it contains` · `## Size and versions` · `## Licence` · `## How it was
made` · `## Used by` (papers, trends, benchmarks) · `## Known problems` · `## Sources`.

**Benchmark (`type: benchmark`)**: `## What it tests` · `## Tasks, metrics and protocol` · `## Datasets` ·
`## Results` (table: system, score, metric, who ran it, first-party?, date, source) · `## Known problems` ·
`## Used by` · `## Sources`.

**Index entry (`type: index`)**: `## Definition` (one paragraph, cited) · `## How it changed` (dated) ·
`## Where sources disagree` (or "No disagreement found in the sources read.") · `## Related` (plain links) ·
`## Appears in` (generated) · `## Sources`.

## 9. Seed index slugs

Use these slugs when you link these terms. Add others in the same form and report them.

| Thread | Slugs |
|---|---|
| KB/KG | `knowledge-base`, `knowledge-graph`, `semantic-network`, `frame`, `production-rule`, `expert-system`, `inference-engine`, `knowledge-representation`, `description-logic`, `entity`, `triple`, `property-graph`, `knowledge-graph-embedding`, `link-prediction`, `entity-linking`, `named-entity-recognition`, `relation-extraction`, `knowledge-graph-completion`, `schema`, `taxonomy`, `community-detection`, `personalized-pagerank` |
| Ontologies and semantic web | `ontology`, `semantic-web`, `rdf`, `rdfs`, `owl`, `sparql`, `linked-data`, `uri` |
| Databases and search | `relational-model`, `sql`, `graph-database`, `cypher`, `gql`, `triple-store`, `information-retrieval`, `inverted-index`, `tf-idf`, `bm25`, `vector-space-model`, `embedding`, `vector-search`, `approximate-nearest-neighbour`, `reranking`, `hybrid-search` |
| RAG and agent memory | `large-language-model`, `context-window`, `retrieval-augmented-generation`, `graphrag`, `chunking`, `agent`, `tool-use`, `agent-memory`, `temporal-knowledge-graph`, `model-context-protocol`, `reinforcement-learning`, `llm-as-judge`, `multi-hop-question-answering`, `text-to-query` |
| Systems | `cyc`, `wordnet`, `dbpedia`, `yago`, `freebase`, `wikidata`, `google-knowledge-graph`, `conceptnet` |
| Standards | `rdf`, `owl`, `sparql`, `cypher`, `gql`, `model-context-protocol` |

## 10. What every writer returns

A short structured answer: the files written; for each, the index slugs linked (slug, term, kind, one-line
definition) and whether each is a seed slug; the project slugs linked; the papers cited (title, year, id);
the dataset and benchmark slugs linked; the `changes.tsv` rows for the items written; the load-bearing
facts re-verified (how many, and any that failed); everything left **unstated** or unverified.
