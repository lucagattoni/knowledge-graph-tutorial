---
type: trend
shift: RDF 1.1 plus the RDF-star report -> RDF 1.2 with SPARQL 1.2 and SHACL 1.2
status: steady
order: 10
updated: 20261103 01:52 UTC
---

# Semantic web standards: from RDF 1.1 and RDF-star to RDF 1.2

This page answers one question: what are the W3C standards for [RDF](../index/rdf.md) data, its query language [SPARQL](../index/sparql.md) and its validation language [SHACL](../index/shacl.md) doing now, and how far has the revision from RDF 1.1 to RDF 1.2 got? It also covers what the three share: the triple terms that replace the [RDF-star](../index/rdf-star.md) of a 2021 community report. On 20261103 none of the documents read was a Recommendation [1][6][8], yet two stores already ship parts of RDF 1.2 [15][16].

> **Distinctive because** it is a standard, not a method: no model is used and nothing is retrieved; the specifications fix how a graph is written, queried and checked. There are three nearest neighbours. [Infrastructure and MCP](./infrastructure-and-mcp.md) has a graph-database strand on the ISO query standards [GQL](../index/gql.md) and [SQL/PGQ](../index/sql-pgq.md), published in 2024 and 2023. [Asking graphs in natural language](./graph-query-generation.md) has a model write the SPARQL. [Building knowledge graphs with LLMs](./llm-kg-construction.md) has a model induce the schema [23]. This page is the W3C family that is still being revised: the languages, not the models that write in them.

## Why it emerged

RDF 1.1 (Recommendation 20140225), SPARQL 1.1 (20130321) and SHACL (20170720) are the latest Recommendations: each 1.2 draft names its predecessor under "Latest Recommendation" [1][6][8][22]. The revision has one origin, statements about statements. The first RDF Recommendation modelled them by reification, in a form it calls "rather verbose"; Hartig and Thompson (arXiv, 20140613) proposed a compact alternative; and a community group issued its Final Report on 20211217, which says it is not a W3C Standard [22][12].

The working group's charter says the idea "has become quite popular, especially as a means to provide interoperability between RDF and Property Graphs" and has been implemented "to various extents by a number of vendors and open-source libraries" (first-party) [10]. The first charter began on 20220829 under the name RDF-star; the group renamed itself RDF & SPARQL because the old name confused its scope [10]. First public drafts of the RDF 1.2 and SPARQL 1.2 documents date from 20230516 [2][6]. The Data Shapes group was chartered on 20241216 to update SHACL "in line with 1.2 version updates to RDF & SPARQL" and to add rules, user-interface, profiling and compact-syntax specifications [11]. Why the work started in 2022 and not earlier is **unstated** in the sources read.

## Why it matters

- **Statement-level metadata has a standard form.** A reifier may stand for a claim that a statement holds, the situations in which it holds, or the events that made it hold [1]. The [provenance](../index/provenance.md) of a fact can be written in RDF itself.
- **A bridge to property graphs.** The RDF charter names coordination with the ISO committee on GQL and SQL/PGQ, and with an LDBC group on possible bridges to a unified property-graph model [10]. An October 2026 paper compares three algorithms that translate RDF 1.2 data into property graphs [21].
- **A hook for agents.** SHACL 1.2 Core defines `sh:agentInstruction` for "textual instructions that can be sent to a software agent that understands natural language" [8]. No source read says a tool uses it: **unstated**.
- **Migration cost.** RDF4J 6.0.0 renames its RDF-star classes and needs Java 25; Oxigraph 0.5 migrates databases on first opening and changes the Turtle and N-Triples form of nested triples [15][16].

*Reading:* the family decides how a statement about a statement is written. It is the trend least connected to [large language models](../index/large-language-model.md). The links read are the SPARQL that models write [23] and, by title, papers in which a model writes SHACL shapes [21].

## How it works

One data model, three languages. RDF 1.2 Concepts keeps the graphs and datasets of RDF 1.1 and changes three things: a **triple term** (an RDF [triple](../index/triple.md) used as the object of another triple), directional language-tagged strings, and a way to announce which RDF version a piece of data uses [1]. A triple term is not asserted by itself. A **reifying triple** with the predicate `rdf:reifies` ties it to a **reifier**, which other triples can describe; if the same triple is also asserted, the triples about the reifier form a **triple annotation** [1]. Triple terms are transparent: a term inside one denotes what it denotes outside [1].

| Document | What the draft adds, as it lists the change |
|---|---|
| RDF 1.2 Schema (the [RDFS](../index/rdfs.md) vocabulary) | `rdfs:Proposition`, `rdf:reifies`, `rdf:dirLangString`, `rdf:JSON` [4] |
| SPARQL 1.2 Query | Grammar for triple terms, reifiers and annotations; functions TRIPLE, isTRIPLE, SUBJECT, PREDICATE, OBJECT; LANGDIR, hasLANG, hasLANGDIR, STRLANGDIR; a VERSION declaration; a formal definition of EXISTS [6] |
| SHACL 1.2 Core | Node kind `sh:TripleTerm`; `sh:reifierShape`; list constraints; node expressions; `sh:intent` and `sh:agentInstruction`; `sh:name` and `sh:description` now describe the defining characteristic of a shape, not the shape [8] |
| Other SHACL 1.2 drafts | SPARQL-related features, node expressions, inference rules, profiling, user interfaces, and SPARQL 1.2 RL, "a Datalog-style rules language for RDF" ([datalog](../index/datalog.md)) [8][9] |

The RDF-star report allowed a quoted triple as subject or object and called quoted triples referentially opaque; RDF 1.2 allows a triple term only as an object and calls it transparent [12][1]. The charter says RDF 1.1 data SHOULD remain valid [10]. [RDF Dataset Canonicalization](../index/rdf-dataset-canonicalization.md) is a 2024 Recommendation on the RDF 1.1 definition; the sources give no plan for a 1.2 update: **unstated** [22].

The stage of each document on 20261103, from W3C's pages and publication histories:

| Document | Stage | Newest | Publications since the first draft |
|---|---|---|---|
| RDF 1.2 Concepts | Candidate Recommendation Snapshot | 20260407 | 84 since 20230516 [1][2] |
| RDF 1.2 Semantics | Candidate Recommendation Draft (a Snapshot of 20260407 came before) | 20260924 | 48 since 20230606 [3] |
| RDF 1.2 Schema | Working Draft | 20261023 | 21 since 20230516 [4] |
| Turtle, TriG, N-Triples, N-Quads, RDF/XML | Working Drafts | 20261023 to 20261101 | 213 together [5] |
| SPARQL 1.2 Query | Working Draft | 20261101 | 108 since 20230516 [6] |
| Eight other SPARQL 1.2 documents | Working Drafts | 20241227 (Results XML) to 20261029 | 108 together; the Graph Store Protocol (Working Draft 20260924) is a ninth, its count not read [7] |
| SHACL 1.2 Core | Working Draft | 20261102 | 62 since 20250318 [8] |
| SHACL 1.2 SPARQL-Related Features, Node Expressions, User Interfaces; SPARQL 1.2 RL | Working Drafts | 20261022 to 20261031 | 38, 6, 2 and 51 [9] |

To leave the Candidate Recommendation phase, Concepts needs RDF 1.2 Semantics and at least one syntax specification to meet their own exit criteria; Semantics needs at least two independent implementations to pass each test of its suite [1][3].

## Representative projects

W3C defines the specifications; four implementations were checked for RDF 1.2 on 20261103. None has a page in chapter 3. Licences are from each `LICENSE` file [19].

| Project | Licence | What its own notes say (first-party) | Source |
|---|---|---|---|
| [Eclipse RDF4J](https://github.com/eclipse-rdf4j/rdf4j) | BSD-3-Clause | 6.0.0 (20260810) "adds broad support for the current RDF 1.2 and SPARQL 1.2 specifications"; it needs Java 25 and breaks the RDF-star class names | [15] |
| [Oxigraph](https://github.com/oxigraph/oxigraph) | Apache-2.0 and MIT | 0.5.0-beta.1 (20250720) "RDF-star support is now dropped in favor of RDF 1.2"; 0.5.0 (20250913) puts RDF 1.2 and SPARQL 1.2 behind feature flags; latest 0.5.13 (20261022). Snapshot: 2,014 stars, last push 20261023 | [16][20] |
| [Apache Jena](https://github.com/apache/jena) | Apache-2.0 | Current release 6.2.0. The tracker has 12 issues labelled "RDF 1.2" (2 open); "Support RDF 1.2" is open since 20241028. Which release supports it: **unstated** | [17] |
| [rdflib](https://github.com/RDFLib/rdflib) | BSD-3-Clause | The changelog, newest entry 7.6.0 (20260213), does not mention RDF 1.2, RDF-star or triple terms | [18] |

For SHACL, the Data Shapes charter names pySHACL, Apache Jena, TopBraid, dotNetRDF, Corese, shaclex, GraphDB and RDF4J as implementations to involve; which supports SHACL 1.2 is **unstated** [11].

## Fundamental papers

This family has no group page in the [papers chapter](../papers/README.md): that chapter keeps standards out ("W3C and ISO documents are entries of the index") and ties its groups to trends, and it was not changed for this page [24]. No paper is named as fundamental, because the chapter's tests were not run here (its origin test needs an earlier-work search). The RDF-star entry cites the two candidates, Hartig and Thompson (2014) and Hartig (2017) [22]. The standards are index entries: [RDF](../index/rdf.md), [SPARQL](../index/sparql.md), [SHACL](../index/shacl.md), [RDFS](../index/rdfs.md), [RDF-star](../index/rdf-star.md) and [triple](../index/triple.md).

## What is measured, and by whom

**Publications.** Counts of dated versions in W3C's publication histories, for 23 documents whose history was read (the 20251102 to 20261102 window, the same as the other pages, against the year before) [2] to [9]:

| Documents | Count | Window | Year before |
|---|---|---|---|
| RDF 1.2 (Concepts, Semantics, Schema, five syntaxes, Primer) | 9 | 128 | 136 |
| SPARQL 1.2 (Query and eight others) | 9 | 73 | 61 |
| SHACL 1.2 (four documents) and SPARQL 1.2 RL | 5 | 134 | 25 |
| Total | 23 | 335 | 222 |

The SHACL documents began on 20250318 or later, so their year before is at most seven and a half months. Every publication is a dated snapshot, not a review of quality.

**Conformance.** The RDF Tests Community Group's reports of 20261102 list four test subjects for RDF 1.2: Attean, rdf12conv, N3.js and rdfxml-streaming-parser, which report syntax, evaluation and canonicalization suites; and two for SPARQL 1.2: Comunica SPARQL and Attean [13]. The RDF report lists tests for RDF 1.2 Semantics, and none of the four subjects reports them [13]. RDF4J, Oxigraph and Jena are not test subjects in either report [13]. The developers of rdf12conv, rdfxml-streaming-parser and Comunica SPARQL are also named as editors of W3C drafts [5][6][13]. For SHACL 1.2 the test suite holds one report file, named for TopQuadrant, two of whose staff are among the four Core editors [8][14]. The reports call themselves W3C-internal documents with no official standing [13].

**Papers.** arXiv keyword hits, abstracts, first submission 20251102 to 20261102 against 20241102 to 20251101, run 20261103 [21]:

| Query | Window | Year before | Ratio |
|---|---|---|---|
| RDF 1.2, SPARQL 1.2, SHACL 1.2, RDF-star, SPARQL-star, "triple term(s)" | 5 | 2 | 2.5 |
| SHACL or "Shapes Constraint Language" | 45 | 16 | 2.8 |
| SPARQL | 113 | 64 | 1.8 |
| control: any LLM wording | 44,692 | 32,396 | 1.38 |
| control: any RAG wording | 3,357 | 2,736 | 1.23 |
| control: LLM-agent wording | 15,158 | 6,068 | 2.50 |

These are "N results for query Q", not counts of papers in the field. Reading the abstracts of the five topic hits, three mention RDF-star or RDF 1.2 and two do not (a biomedical-imaging paper and a world-model paper); the year before, both hits do [21]. By title, the SHACL and SPARQL hits include papers in which a model writes or uses the language, so they do not measure the standard [21]. arXiv only; other venues were not searched: **unstated**.

**Openness.** The groups' charters give every deliverable the W3C Software and Document licence, and the Candidate Recommendation text records members' commitments to royalty-free licensing for implementations [10][11][1]. The RDF and SPARQL test suites are dual-licensed (W3C Test Suite License and 3-clause BSD) [13][19]. Drafts and issues are public; the meetings are not [10]. The 2021 report is under the W3C Community Final Specification Agreement [12]. Both "What's New" notes were unfinished when read: the SPARQL one gives "This specification does neat stuff" as its abstract [27].

No [experiment](../experiments/README.md) of this documentation tests this trend.

## Assessment

*Reading:* **Tests.** *Sustained activity* passes, mostly on evidence the other pages do not use. The test names snapshot projects or paper counts. The snapshot holds Oxigraph, ranked and pushed seven days before it, whose releases mention RDF 1.2; Jena, RDF4J and rdflib are not in it [20][16]. The topic papers are 5 against 2 (3 against 2 by abstract), too few to read; SHACL papers are 45 against 16 [21]. The W3C record carries the call: 335 publications against 222, with SHACL work rising and RDF work flat [2] to [9]. *Distinctness* passes. No other trend covers a standard: the infrastructure theme holds the ISO standards, asking-graphs the model that writes SPARQL, and graph construction the model that induces a schema [23]. Here nothing is built, no model is used, and the query author and the engine steer.

*Reading:* **Strengths.** One coordinated revision, in public repositories with test suites. A clean break from RDF-star, already taken by two stores [15][16]. SHACL work is speeding up. **Weaknesses.** Late: the charter of 20250501 planned Recommendations for RDF 1.2 in the third quarter of 2025 and for SPARQL 1.2 in the fourth, and none was one on 20261103 [10][1][6]. Semantics, on which the path to Recommendation depends, has no test results in the report [13]. The SHACL group's charter ends on 20261231 while Core is a Working Draft [11][8]. Implementations are claimed in release notes, not in W3C reports. Data written for the 2021 report is not valid RDF 1.2 where it nests a triple as a subject [12][1][16].

*Reading:* **Status `steady`.** The controls are any LLM wording x1.38, any RAG wording x1.23 and LLM-agent wording x2.50 [25]. Publications rose x1.5, above the LLM and RAG controls and below the agent control, but RDF's own fell to x0.94 and the rise is the new SHACL documents. Not `growing`: the paper counts are too small to carry it. Not `settling`: no part is a Recommendation. When RDF 1.2 Concepts becomes one, `settling` would be earned.

## Signals to watch

| Signal | Where | Baseline |
|---|---|---|
| RDF 1.2 Concepts leaves Candidate Recommendation | W3C history of the document | Snapshot 20260407; "not expected ... any earlier than 05 May 2026" has passed [1][2] |
| Results for the Semantics tests, and for more than parsers | The RDF 1.2 report | No subject reports them (20261102) [13] |
| SHACL 1.2 Core at Candidate Recommendation, or a charter extension | Data Shapes group page | Working Draft 20261102; charter to 20261231 [8][11] |
| The RDF & SPARQL group moves to maintenance mode | Charters page | Charter to 20270430, which plans maintenance afterwards [10] |
| RDF4J, Oxigraph or Jena in the W3C reports; Jena closes "Support RDF 1.2" | Reports; Jena tracker | None is a test subject; issue open [13][17] |
| Papers that use triple terms rather than RDF-star | arXiv | 5 hits against 2, 3 on topic by abstract [21] |

## Sources

Times are UTC, read 20261103; W3C pages and histories 01:23 to 01:24, other pages as stated. Counts from the histories were made from the lists of dated entries on each history page.

1. https://www.w3.org/TR/rdf12-concepts/ : RDF 1.2 Concepts, Candidate Recommendation Snapshot 7 April 2026: abstract, status (exit conditions, "not expected to advance to Recommendation any earlier than 05 May 2026", royalty-free commitments), section 1.5 (triple terms, reifier, annotation, transparency), appendix H (changes), latest Recommendation RDF 1.1 (read 20261103 01:23 UTC)
2. https://www.w3.org/standards/history/rdf12-concepts/ : 84 entries from the first public working draft of 16 May 2023 to the Snapshot of 7 April 2026 (read 20261103 01:24 UTC)
3. https://www.w3.org/TR/rdf12-semantics/ and https://www.w3.org/standards/history/rdf12-semantics/ : Candidate Recommendation Draft 24 September 2026; exit criterion of two independent implementations per test; 48 entries from 6 June 2023, with a Snapshot of 7 April 2026 (read 20261103 01:23 and 01:24 UTC)
4. https://www.w3.org/TR/rdf12-schema/ and its history : Working Draft 23 October 2026; appendix F (changes); 21 entries (read 20261103 01:23 and 01:24 UTC)
5. https://www.w3.org/TR/rdf12-turtle/ , rdf12-trig , rdf12-n-triples , rdf12-n-quads , rdf12-xml , rdf12-primer and their pages under https://www.w3.org/standards/history/ : statuses and newest dates (Turtle 20261101, XML 20261025, others 20261023, Primer Group Note Draft 20260917); entries 63, 32, 45, 43, 30 and 6; editor lists (read 20261103 01:23 and 01:24 UTC)
6. https://www.w3.org/TR/sparql12-query/ and https://www.w3.org/standards/history/sparql12-query/ : Working Draft 1 November 2026; appendix A (changes); latest Recommendation SPARQL 1.1 of 21 March 2013; editors; 108 entries from 16 May 2023 (read 20261103 01:23 and 01:24 UTC)
7. https://www.w3.org/TR/sparql12-update/ , sparql12-service-description , sparql12-federated-query , sparql12-protocol , sparql12-graph-store-protocol , sparql12-results-json , sparql12-results-xml , sparql12-results-csv-tsv , sparql12-entailment and their history pages : statuses (all Working Drafts), newest dates, entries 19, 13, 12, 14, 7, 17, 13 and 13 (the Graph Store Protocol history was not read) (read 20261103 01:23 and 01:24 UTC)
8. https://www.w3.org/TR/shacl12-core/ and https://www.w3.org/standards/history/shacl12-core/ : Working Draft 2 November 2026; abstract; list of SHACL 1.2 specifications; sections 6.10.8.5, 6.11.2 and 6.11.3; 6.18 (changes); editors; latest Recommendation of 20 July 2017; 62 entries from 18 March 2025 (read 20261103 01:23 and 01:24 UTC)
9. https://www.w3.org/TR/shacl12-sparql/ , shacl12-node-expr , shacl12-ui , sparql12-rl and their histories : Working Drafts; abstract of SPARQL 1.2 RL; entries 38, 6, 2 and 51 (read 20261103 01:23 and 01:24 UTC)
10. https://www.w3.org/groups/wg/rdf-star/ , https://www.w3.org/groups/wg/rdf-star/charters/ and https://www.w3.org/2025/04/rdf-star-wg-charter.html : RDF & SPARQL Working Group: chairs, charter 20250501 to 20270430, extensions and recharter note, scope, deliverables, timeline (Recommendations planned Q3 and Q4 2025), success criteria, coordination, licensing, communication (read 20261103 01:24 and 01:26 UTC)
11. https://www.w3.org/groups/wg/data-shapes/ , its charters page and https://www.w3.org/2024/12/data-shapes.html : Data Shapes Working Group: charter 20241216 to 20261231, scope, phases, implementations named, success criteria (read 20261103 01:24 and 01:26 UTC)
12. https://w3c-cg.github.io/rdf-star/cg-spec/2021-12-17.html : RDF-star and SPARQL-star, Final Community Group Report 17 December 2021: not a W3C Standard; quoted triples in subject or object, referentially opaque; Final Specification Agreement (read 20261103 01:26 UTC)
13. https://w3c.github.io/rdf-tests/rdf/rdf12/reports/ and https://w3c.github.io/rdf-tests/sparql/sparql12/reports/ (both dated 02 November 2026), https://w3c.github.io/rdf-tests/ and https://w3c.github.io/rdf-tests/rdf/rdf12/ : test subjects and their compliance, the Semantics test list, the statement of standing, the test licences (read 20261103 01:26 and 01:43 UTC)
14. https://github.com/w3c/data-shapes/tree/gh-pages/shacl12-test-suite : README (conformance criteria) and the `reports` folder, which holds one file, `topquadrant-shacl-earl.ttl` (page read 20261103 01:26 UTC; folder listing through the hosting API 01:29 UTC)
15. https://github.com/eclipse-rdf4j/rdf4j/releases and https://rdf4j.org/release-notes/6.0.0/ : RDF4J 6.0.0, published 20260810: RDF 1.2 and SPARQL 1.2 support, Java 25, RDF-star API renames (read 20261103 01:27 and 01:28 UTC)
16. https://github.com/oxigraph/oxigraph/releases : v0.5.0-beta.1 (20250720), v0.5.0 (20250913), v0.5.13 (20261022): RDF-star dropped for RDF 1.2, feature flags, subject-position triple terms removed, databases migrated, serialisation changed (read 20261103 01:27 UTC)
17. https://jena.apache.org/download/ and the hosting API for https://github.com/apache/jena/issues : release 6.2.0; 12 issues with the label "RDF 1.2" (2 open), the first created 20241028, the newest 20261031; issue 2805 open; the Jena documentation pages on I/O, SHACL and query, and the release pages, do not mention RDF 1.2 (read 20261103 01:28 and 01:29 UTC)
18. https://raw.githubusercontent.com/RDFLib/rdflib/main/CHANGELOG.md : newest entry 7.6.0 of 13 February 2026; no hit for RDF 1.2, RDF-star, triple term or SPARQL 1.2 (read 20261103 01:28 UTC)
19. LICENSE files of oxigraph/oxigraph (LICENSE-APACHE and LICENSE-MIT), apache/jena, eclipse-rdf4j/rdf4j, RDFLib/rdflib, w3c/rdf-tests (dual licensing note), w3c/data-shapes (W3C Software and Document License) (read 20261103 01:39 UTC)
20. kb-kg/landscape/20261030_1954-github/repos.tsv : row oxigraph/oxigraph: category adjacent, ranked, 2,014 stars, last push 20261023 19:40 UTC, 7 days since push; snapshot of 20261030 19:54 UTC (read 20261103 01:42 UTC)
21. https://export.arxiv.org/api/query : counts of `totalResults` for submittedDate 202511020000 to 202611022359 against 202411020000 to 202511012359. Topic: `abs:"RDF 1.2" OR abs:"SPARQL 1.2" OR abs:"SHACL 1.2" OR abs:"RDF-star" OR abs:"SPARQL-star" OR abs:"triple term" OR abs:"triple terms"`: 5 against 2. SHACL: `abs:SHACL OR abs:"Shapes Constraint Language"`: 45 against 16. SPARQL: `abs:SPARQL`: 113 against 64. Controls as in source 25, re-run 20261103 01:33 UTC with the same numbers. Abstracts of the seven topic hits read 20261103 01:45 UTC: 2610.33499 (translating RDF 1.2 to property graphs, 7 authors, v1 20261024) is among the three on topic in the window. Titles of the 45 and 16 SHACL hits read 20261103 01:46 UTC. A first run that included the term "RDF*" gave 136 against 80 and was discarded, because it matches any RDF paper (queries run 20261103 01:33 to 01:44 UTC)
22. The index entries [RDF](../index/rdf.md), [RDF-star](../index/rdf-star.md), [SPARQL](../index/sparql.md), [SHACL](../index/shacl.md), [triple](../index/triple.md) and [RDF Dataset Canonicalization](../index/rdf-dataset-canonicalization.md) : dates and facts of the RDF 1999 and 1.1 era, the RDF-star lineage, the canonicalization status; they cite their own primary sources (read 20261103 01:25 UTC)
23. [Infrastructure and MCP](./infrastructure-and-mcp.md) (page of 20261102 23:17 UTC: GQL and SQL/PGQ dates), [Asking graphs in natural language](./graph-query-generation.md) (SPARQL as a target of model-written queries) and [Building knowledge graphs with LLMs](./llm-kg-construction.md) (its shift is from fixed schemas to induced ones) (read 20261103 01:25 UTC)
24. docs/papers/README.md : "Standards" rule; one group per trend (read 20261103 01:40 UTC)
25. docs/trends/README.md : the two tests, the status values and the controls (read 20261103 01:23 UTC)
26. plans/20261102_1951-docs-catalogue.md : chapter 2 and the owner's review of 20261103, which adds this page (read 20261103 01:41 UTC)
27. https://www.w3.org/TR/rdf12-new/ and https://www.w3.org/TR/sparql12-new/ : What's New in RDF 1.2 and in SPARQL 1.2, Group Note Drafts of 14 July 2026; the SPARQL abstract and introduction are placeholders (read 20261103 01:24 UTC)
