---
type: trend
shift: RDF 1.1 plus the RDF-star report -> RDF 1.2 with SPARQL 1.2 and SHACL 1.2
status: steady
order: 10
updated: 20261103 02:19 UTC
---

# Semantic web standards: from RDF 1.1 and RDF-star to RDF 1.2

This page answers one question: what are the W3C standards for [RDF](../index/rdf.md) data, its query language [SPARQL](../index/sparql.md) and its validation language [SHACL](../index/shacl.md) doing now, and how far has the revision from RDF 1.1 to RDF 1.2 got? It also covers what the three share: the triple terms that replace the [RDF-star](../index/rdf-star.md) of a 2021 community report. On 20261103 none of the documents read was a Recommendation [1][6][8], yet two stores already ship parts of RDF 1.2 [15][16]. The page was added at the owner's review of the trend list on 20261103, because about ten other pages pointed to the trends for these drafts and no trend covered them [26].

> **Distinctive because** it is a standard, not a method: no model is used and nothing is retrieved; the specifications fix how a graph is written, queried and checked. There are three nearest neighbours. [Infrastructure and MCP](./infrastructure-and-mcp.md) has a graph-database strand on the ISO query standards [GQL](../index/gql.md) and [SQL/PGQ](../index/sql-pgq.md), published in 2024 and 2023. [Asking graphs in natural language](./graph-query-generation.md) has a model write the SPARQL. [Building knowledge graphs with LLMs](./llm-kg-construction.md) has a model induce the schema [23]. This page is the W3C family that is still being revised: the languages, not the models that write in them.

## Why it emerged

RDF 1.1 (Recommendation 20140225), SPARQL 1.1 (20130321) and SHACL (20170720) are the latest Recommendations: each 1.2 draft names its predecessor under "Latest Recommendation" [1][6][8][22]. The revision has one origin, statements about statements. The first RDF Recommendation (19990222) modelled them by reification, in a form it calls "rather verbose" [28]. Hartig and Thompson (arXiv, 20140613) proposed a compact alternative [29], and a community group issued its Final Report on 20211217, which says it is "not a W3C Standard" [12]. The [RDF-star](../index/rdf-star.md) entry dates the lineage [22].

The working group's charter says the idea "has become quite popular, especially as a means to provide interoperability between RDF and Property Graphs" and has been implemented "to various extents by a number of vendors and open-source libraries" (first-party) [10]. The first charter began on 20220829 under the name RDF-star; the group renamed itself RDF & SPARQL because the old name confused its scope [10]. The first public drafts of RDF 1.2 Concepts and SPARQL 1.2 Query date from 20230516 [2][6]. The Data Shapes group was chartered on 20241216 to update SHACL "in line with 1.2 version updates to RDF & SPARQL" and to add rules, user-interface, profiling and compact-syntax specifications [11]. Why the work started in 2022 and not earlier is **unstated** in the sources read.

## Why it matters

- **Statement-level metadata has a standard form.** A reifier may stand for a claim that a statement holds, the situations in which it holds, or the events that made it hold [1]. The [provenance](../index/provenance.md) of a fact can be written in RDF itself.
- **A bridge to property graphs.** The RDF charter names coordination with the ISO committee on GQL and SQL/PGQ, and with an LDBC group on possible bridges to a unified property-graph model [10]. An October 2026 paper compares three algorithms that translate RDF 1.2 data into property graphs [21].
- **A hook for agents.** SHACL 1.2 Core defines `sh:agentInstruction` for "textual instructions that can be sent to a software agent that understands natural language" [8]. No source read says a tool uses it: **unstated**.
- **Migration cost.** RDF4J 6.0.0 renames its RDF-star classes and needs Java 25; Oxigraph 0.5 migrates databases on first opening and changes the Turtle and N-Triples form of nested triples [15][16].

*Reading:* the family decides how a statement about a statement is written. It is the trend least connected to [large language models](../index/large-language-model.md). The links read are the SPARQL that models write [23] and, by title, papers in which a model writes SHACL shapes [21].

## How it works

One data model, three languages. RDF 1.2 Concepts keeps the graphs and datasets of RDF 1.1. Its abstract names three additions (the appendix of changes lists more): a **triple term** (an RDF [triple](../index/triple.md) used as the object of another triple), directional language-tagged strings, and a way to announce which RDF version a piece of data uses [1]. A triple term is not asserted by itself. A **reifying triple** with the predicate `rdf:reifies` ties it to a **reifier**, which other triples can describe; if the same triple is also asserted, the triples about the reifier form a **triple annotation** [1]. Triple terms are transparent: a term inside one denotes what it denotes outside [1].

| Document | What the draft adds, as it lists the change |
|---|---|
| RDF 1.2 Schema (the [RDFS](../index/rdfs.md) vocabulary) | `rdfs:Proposition`, `rdf:reifies`, `rdf:dirLangString`, `rdf:JSON` [4] |
| SPARQL 1.2 Query | Grammar for triple terms, reifiers and annotations; functions TRIPLE, isTRIPLE, SUBJECT, PREDICATE, OBJECT; LANGDIR, hasLANG, hasLANGDIR, STRLANGDIR; a VERSION declaration; a formal definition of EXISTS [6] |
| SHACL 1.2 Core | Node kind `sh:TripleTerm`; `sh:reifierShape`; list constraints; node expressions; `sh:intent` and `sh:agentInstruction`; `sh:name` and `sh:description` now describe the defining characteristic of a shape, not the shape [8] |
| Other SHACL 1.2 drafts | SPARQL-related features, node expressions, inference rules, profiling, user interfaces, and SPARQL 1.2 RL, "a Datalog-style rules language for RDF" ([datalog](../index/datalog.md)) [8][9] |

The 2021 report allowed a quoted triple as subject or object and called it referentially opaque; RDF 1.2 allows a triple term only as an object and calls it transparent [12][1]. The charter says RDF 1.1 data SHOULD remain valid [10]. [RDF Dataset Canonicalization](../index/rdf-dataset-canonicalization.md) is a 2024 Recommendation on the RDF 1.1 definition, whose status section expects "a future update" to refer to the updated RDF specifications; a plan or date is **unstated** [30].

The stage of each document on 20261103, from W3C's pages and publication histories:

| Document | Stage | Newest | Publications since the first draft |
|---|---|---|---|
| RDF 1.2 Concepts | Candidate Recommendation Snapshot | 20260407 | 84 since 20230516 [1][2] |
| RDF 1.2 Semantics | Candidate Recommendation Draft (a Snapshot of 20260407 came before) | 20260924 | 48 since 20230606 [3] |
| RDF 1.2 Schema | Working Draft | 20261023 | 21 since 20230516 [4] |
| Turtle, TriG, N-Triples, N-Quads, RDF/XML | Working Drafts | 20261023 to 20261101 | 213 together [5] |
| RDF 1.2 Primer, Interoperability; What's New in RDF 1.2 and in SPARQL 1.2 | Group Note Drafts | 20260917, 20260723; 20260714 | 6, 4; 1 and 1 [5][27][31] |
| SPARQL 1.2 Query | Working Draft | 20261101 | 108 since 20230516 [6] |
| Nine other SPARQL 1.2 documents | Working Drafts | 20241227 (Results XML) to 20261029 | 115 together [7] |
| SHACL 1.2 Core | Working Draft | 20261102 | 62 since 20250318 [8] |
| SHACL 1.2 SPARQL-Related Features, Node Expressions, Inference Rules, User Interfaces; SPARQL 1.2 RL | Working Drafts | 20261022 to 20261031 | 38, 6, 2, 2 and 51 [9] |
| SHACL 1.2 Profiling | First Public Working Draft | 20260702 | 1 [9] |

SPARQL 1.2 Concepts, and SHACL 1.2 Overview and Compact Syntax, are Editor's Drafts with no publication history [27][8].

To leave the Candidate Recommendation phase, Concepts needs RDF 1.2 Semantics and at least one syntax specification to meet their own exit criteria; Semantics needs at least two independent implementations to pass each test of its suite [1][3].

## Representative projects

W3C defines the specifications; four implementations were checked for RDF 1.2 on 20261103. None has a page in chapter 3. Licences are from each `LICENSE` file [19].

| Project | Licence | What its own notes say (first-party) | Source |
|---|---|---|---|
| [Eclipse RDF4J](https://github.com/eclipse-rdf4j/rdf4j) | BSD-3-Clause | 6.0.0 (20260810) "adds broad support for the current RDF 1.2 and SPARQL 1.2 specifications"; it needs Java 25 and breaks the RDF-star class names. The notes say the implementation "includes the emerging W3C conformance suites"; RDF4J is not a subject in the W3C reports | [15][13] |
| [Oxigraph](https://github.com/oxigraph/oxigraph) | Apache-2.0 and MIT | 0.5.0-beta.1 (20250720) "RDF-star support is now dropped in favor of RDF 1.2"; 0.5.0 (20250913) puts RDF 1.2 and SPARQL 1.2 behind feature flags, off by default in the Rust crate and on in the CLI and the Python and JS bindings; latest 0.5.13 (20261022). Snapshot: 2,014 stars, last push 20261023 | [16][20] |
| [Apache Jena](https://github.com/apache/jena) | Apache-2.0 | Current release 6.2.0. The tracker has 12 issues (2 open) and 3 merged pull requests labelled "RDF 1.2", none with a release milestone; "Support RDF 1.2" is open since 20241028. Which release supports it: **unstated** | [17] |
| [rdflib](https://github.com/RDFLib/rdflib) | BSD-3-Clause | The changelog, newest entry 7.6.0 (20260213), does not mention RDF 1.2, RDF-star or triple terms. The tracker has an open issue "Tracking: RDF 1.2 support" (created 20260822) and an open, unmerged pull request "Add initial RDF 1.2 support" (created 20260614) | [18] |

For SHACL, the Data Shapes charter names pySHACL, Apache Jena, TopBraid, dotNetRDF, Corese, shaclex, GraphDB and RDF4J as implementations to involve; which supports SHACL 1.2 is **unstated** [11].

## Fundamental papers

This family has no group page in the [papers chapter](../papers/README.md): that chapter keeps standards out ("W3C and ISO documents are entries of the index") and ties its groups to trends, and it was not changed for this page [24]. No paper is named as fundamental, because the chapter's tests were not run here. The RDF-star entry cites the two candidates, Hartig and Thompson (2014) and Hartig (2017) [22]. The standards are index entries: [RDF](../index/rdf.md), [SPARQL](../index/sparql.md), [SHACL](../index/shacl.md), [RDFS](../index/rdfs.md), [RDF-star](../index/rdf-star.md) and [triple](../index/triple.md).

## What is measured, and by whom

**Publications.** Counts of dated versions in W3C's publication histories, for the 29 documents that the two groups' publication pages list for RDF 1.2, SPARQL 1.2 and SHACL 1.2 (the 20251102 to 20261102 window, the same as the other pages, against the year before) [2] to [9][27][31]:

| Documents | Count | Window | Year before |
|---|---|---|---|
| RDF 1.2 (Concepts, Semantics, Schema, five syntaxes, Primer, Interoperability, What's New) | 11 | 133 | 136 |
| SPARQL 1.2 (Query, nine others, What's New) | 11 | 75 | 64 |
| SHACL 1.2 (six documents) and SPARQL 1.2 RL | 7 | 137 | 25 |
| Total | 29 | 345 | 225 |

SHACL 1.2 Core and SPARQL-Related Features began on 20250318, so their year before is at most seven and a half months; the other four SHACL drafts and SPARQL 1.2 RL began between 20251209 and 20260917, with nothing in the year before. Every publication is a dated snapshot, not a review of quality.

**Conformance.** The RDF Tests Community Group's reports of 20261102 list four test subjects for RDF 1.2: Attean, rdf12conv, n3 (N3.js) and rdfxml-streaming-parser, which report syntax, evaluation and canonicalization suites; and two for SPARQL 1.2: Comunica SPARQL and Attean [13]. The RDF report lists tests for RDF 1.2 Semantics, and none of the four subjects reports them [13]. RDF4J, Oxigraph and Jena are not test subjects in either report [13]. The developers of rdf12conv, rdfxml-streaming-parser and Comunica SPARQL are also named as editors of W3C drafts, and one of them edits both reports [5][6][13]. For SHACL 1.2 the test suite holds one report file, named for TopQuadrant, two of whose staff are among the four Core editors [8][14]. The reports call themselves W3C-internal documents with no official standing [13].

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

**Openness.** The groups' charters give every deliverable the W3C Software and Document licence, and the Candidate Recommendation text records members' commitments to royalty-free licensing for implementations [10][11][1]. The RDF and SPARQL test suites are dual-licensed (W3C Test Suite License and 3-clause BSD) [13][19]. Drafts and issues are public; the meetings are not [10]. The 2021 report is under the W3C Community Final Specification Agreement [12]. Both "What's New" notes were unfinished when read: the SPARQL one gives "This specification does neat stuff" as its abstract, and the RDF one has an empty section on the abstract syntax [27].

No [experiment](../experiments/README.md) of this documentation tests this trend.

## Assessment

*Reading:* **Tests.** *Sustained activity* passes, mostly on evidence the other pages do not use. The snapshot holds Oxigraph, ranked and pushed seven days before it, whose releases mention RDF 1.2; Jena, RDF4J and rdflib are not in it, and its other RDF projects were not read for RDF 1.2: **unstated** [20][16]. The topic papers are 5 against 2 (3 against 2 by abstract), too few to read; SHACL papers are 45 against 16 [21]. The W3C record carries the call: 345 publications against 225, with SHACL work rising and RDF work flat [2] to [9][27][31]. *Distinctness* passes. No other trend covers a standard: the infrastructure theme holds the ISO standards, asking-graphs the model that writes SPARQL, and graph construction the model that induces a schema [23]. Here nothing is built, no model is used, and the query author and the engine steer.

*Reading:* **Strengths.** One coordinated revision, in public repositories with test suites. A clean break from RDF-star, already taken by two stores [15][16]. SHACL work is speeding up: Core publications rose from 15 to 47, and five more drafts began in the window [8][9]. **Weaknesses.** Late: the charter of 20250501 planned Recommendations for RDF 1.2 in the third quarter of 2025 and for SPARQL 1.2 in the fourth, and none was one on 20261103 [10][1][6]. Semantics, on which the path to Recommendation depends, has no test results in the report [13]. The SHACL group's charter ends on 20261231 while Core is a Working Draft [11][8]. Implementations are claimed in release notes, not in W3C reports. Data written for the 2021 report is not valid RDF 1.2 where it nests a triple as a subject [12][1][16].

*Reading:* **Status `steady`.** The controls are any LLM wording x1.38, any RAG wording x1.23 and LLM-agent wording x2.50 [25]. Publications rose x1.5 (345 against 225), above the LLM and RAG controls and below the agent control, but RDF's own held at x0.98 and the rise is the new SHACL documents. Not `growing`: the paper counts are too small to carry it. Not `settling`: no part is a Recommendation. When RDF 1.2 Concepts becomes one, `settling` would be earned.

## Signals to watch

| Signal | Where | Baseline |
|---|---|---|
| RDF 1.2 Concepts leaves Candidate Recommendation | W3C history of the document | Snapshot 20260407; "not expected to advance to Recommendation any earlier than 05 May 2026" has passed [1][2] |
| Results for the Semantics tests, and for more than parsers | The RDF 1.2 report | No subject reports them (20261102) [13] |
| SHACL 1.2 Core at Candidate Recommendation, or a charter extension | Data Shapes group page | Working Draft 20261102; charter to 20261231 [8][11] |
| The RDF & SPARQL group moves to maintenance mode | Charters page | Charter to 20270430, which plans maintenance afterwards [10] |
| RDF4J, Oxigraph or Jena in the W3C reports; Jena closes "Support RDF 1.2"; rdflib merges its RDF 1.2 work | Reports; Jena and rdflib trackers | None is a test subject; Jena issue, rdflib issue and pull request open [13][17][18] |
| Papers that use triple terms rather than RDF-star | arXiv | 5 hits against 2, 3 on topic by abstract [21] |

## Sources

Times are UTC, read 20261103; W3C pages and histories 01:23 to 01:24, other pages as stated. Counts from the histories were made from the lists of dated entries on each history page. An independent check the same day re-read the W3C histories and pages (02:02 to 02:04), the charters, reports and licences (02:06 to 02:08), the release pages and trackers (02:08 to 02:11) and the arXiv counts (02:12), recounted every history, and added the Graph Store Protocol, SHACL Inference Rules and Profiling, RDF 1.2 Interoperability and the two "What's New" histories (sources 7, 9, 27, 31) and sources 28 to 31.

1. https://www.w3.org/TR/rdf12-concepts/ : RDF 1.2 Concepts, Candidate Recommendation Snapshot 7 April 2026: abstract, status (exit conditions, "not expected to advance to Recommendation any earlier than 05 May 2026", royalty-free commitments), section 1.5 (triple terms, reifier, annotation, transparency), appendix H (changes), latest Recommendation RDF 1.1 (read 20261103 01:23 UTC)
2. https://www.w3.org/standards/history/rdf12-concepts/ : 84 entries from the first public working draft of 16 May 2023 to the Snapshot of 7 April 2026 (read 20261103 01:24 UTC)
3. https://www.w3.org/TR/rdf12-semantics/ and https://www.w3.org/standards/history/rdf12-semantics/ : Candidate Recommendation Draft 24 September 2026; exit criterion of two independent implementations per test; 48 entries from 6 June 2023, with a Snapshot of 7 April 2026 (read 20261103 01:23 and 01:24 UTC)
4. https://www.w3.org/TR/rdf12-schema/ and its history : Working Draft 23 October 2026; appendix F (changes); 21 entries (read 20261103 01:23 and 01:24 UTC)
5. https://www.w3.org/TR/rdf12-turtle/ , rdf12-trig , rdf12-n-triples , rdf12-n-quads , rdf12-xml , rdf12-primer and their pages under https://www.w3.org/standards/history/ : statuses and newest dates (Turtle 20261101, XML 20261025, others 20261023, Primer Group Note Draft 20260917); entries 63, 32, 45, 43, 30 and 6; editor lists (read 20261103 01:23 and 01:24 UTC)
6. https://www.w3.org/TR/sparql12-query/ and https://www.w3.org/standards/history/sparql12-query/ : Working Draft 1 November 2026; appendix A (changes); latest Recommendation SPARQL 1.1 of 21 March 2013; editors; 108 entries from 16 May 2023 (read 20261103 01:23 and 01:24 UTC)
7. https://www.w3.org/TR/sparql12-update/ , sparql12-service-description , sparql12-federated-query , sparql12-protocol , sparql12-graph-store-protocol , sparql12-results-json , sparql12-results-xml , sparql12-results-csv-tsv , sparql12-entailment and their history pages : statuses (all Working Drafts), newest dates, entries: Update 19, Service Description 13, Federated Query 12, Protocol 14, Graph Store Protocol 7, Results JSON 17, Results XML 13, Results CSV/TSV 13, Entailment Regimes 7; 115 together (read 20261103 01:23 and 01:24 UTC; the Graph Store Protocol history added 02:03 UTC)
8. https://www.w3.org/TR/shacl12-core/ and https://www.w3.org/standards/history/shacl12-core/ : Working Draft 2 November 2026; abstract; list of SHACL 1.2 specifications; sections 6.10.8.5, 6.11.2 and 6.11.3; 6.18 (changes); editors; latest Recommendation of 20 July 2017; 62 entries from 18 March 2025 (read 20261103 01:23 and 01:24 UTC)
9. https://www.w3.org/TR/shacl12-sparql/ , shacl12-node-expr , shacl12-ui , shacl12-inference-rules , shacl12-profiling , sparql12-rl and their histories : Working Drafts (Profiling: First Public Working Draft 2 July 2026); abstract of SPARQL 1.2 RL; entries 38, 6, 2, 2, 1 and 51 (read 20261103 01:23 and 01:24 UTC; Inference Rules and Profiling added 02:03 and 02:04 UTC)
10. https://www.w3.org/groups/wg/rdf-star/ , https://www.w3.org/groups/wg/rdf-star/charters/ and https://www.w3.org/2025/04/rdf-star-wg-charter.html : RDF & SPARQL Working Group: chairs, charter 20250501 to 20270430, extensions and recharter note, scope, deliverables, timeline (Recommendations planned Q3 and Q4 2025), success criteria, coordination, licensing, communication (read 20261103 01:24 and 01:26 UTC)
11. https://www.w3.org/groups/wg/data-shapes/ , its charters page and https://www.w3.org/2024/12/data-shapes.html : Data Shapes Working Group: charter 20241216 to 20261231, scope, phases, implementations named, success criteria (read 20261103 01:24 and 01:26 UTC)
12. https://w3c-cg.github.io/rdf-star/cg-spec/2021-12-17.html : RDF-star and SPARQL-star, Final Community Group Report 17 December 2021: not a W3C Standard; quoted triples in subject or object, referentially opaque; Final Specification Agreement (read 20261103 01:26 UTC)
13. https://w3c.github.io/rdf-tests/rdf/rdf12/reports/ and https://w3c.github.io/rdf-tests/sparql/sparql12/reports/ (both dated 02 November 2026), https://w3c.github.io/rdf-tests/ and https://w3c.github.io/rdf-tests/rdf/rdf12/ : test subjects and their compliance, the Semantics test list, the statement of standing, the test licences (read 20261103 01:26 and 01:43 UTC)
14. https://github.com/w3c/data-shapes/tree/gh-pages/shacl12-test-suite : README (conformance criteria) and the `reports` folder, which holds one file, `topquadrant-shacl-earl.ttl` (page read 20261103 01:26 UTC; folder listing through the hosting API 01:29 UTC)
15. https://github.com/eclipse-rdf4j/rdf4j/releases and https://rdf4j.org/release-notes/6.0.0/ : RDF4J 6.0.0, published 20260810: RDF 1.2 and SPARQL 1.2 support, Java 25, RDF-star API renames (read 20261103 01:27 and 01:28 UTC)
16. https://github.com/oxigraph/oxigraph/releases : v0.5.0-beta.1 (20250720), v0.5.0 (20250913), v0.5.13 (20261022): RDF-star dropped for RDF 1.2, feature flags, subject-position triple terms removed, databases migrated, serialisation changed (read 20261103 01:27 UTC)
17. https://jena.apache.org/download/ and the hosting API for https://github.com/apache/jena/issues : release 6.2.0; 12 issues and 3 merged pull requests with the label "RDF 1.2", 2 issues open (2805 and 3146), the first created 20241028, the newest 20261031, none with a milestone; the Jena documentation pages on I/O, SHACL and query, and the release pages, do not mention RDF 1.2 (read 20261103 01:28 and 01:29 UTC; counts re-run 02:09 and 02:10 UTC)
18. https://raw.githubusercontent.com/RDFLib/rdflib/main/CHANGELOG.md : newest entry 7.6.0 of 13 February 2026; no hit for RDF 1.2, RDF-star, triple term or SPARQL 1.2 (read 20261103 01:28 UTC). The hosting API for https://github.com/RDFLib/rdflib : issue 3524 "Tracking: RDF 1.2 support", open, created 20260822, last updated 20260922; pull request 3447 "Add initial RDF 1.2 support", open, not merged, created 20260614; issue 3439 "Support for RDF 1.2", closed 20260605; no release after 7.6.0 (read 20261103 02:10 UTC)
19. LICENSE files of oxigraph/oxigraph (LICENSE-APACHE and LICENSE-MIT), apache/jena, eclipse-rdf4j/rdf4j, RDFLib/rdflib, w3c/rdf-tests (dual licensing note), w3c/data-shapes (W3C Software and Document License) (read 20261103 01:39 UTC)
20. kb-kg/landscape/20261030_1954-github/repos.tsv : row oxigraph/oxigraph: category adjacent, ranked, 2,014 stars, last push 20261023 19:40 UTC, 7 days since push; snapshot of 20261030 19:54 UTC (read 20261103 01:42 UTC)
21. https://export.arxiv.org/api/query : counts of `totalResults` for submittedDate 202511020000 to 202611022359 against 202411020000 to 202511012359. Topic: `abs:"RDF 1.2" OR abs:"SPARQL 1.2" OR abs:"SHACL 1.2" OR abs:"RDF-star" OR abs:"SPARQL-star" OR abs:"triple term" OR abs:"triple terms"`: 5 against 2. SHACL: `abs:SHACL OR abs:"Shapes Constraint Language"`: 45 against 16. SPARQL: `abs:SPARQL`: 113 against 64. Controls as in source 25, re-run 20261103 01:33 UTC with the same numbers. A further re-run at 02:12 UTC gave topic 5 against 2, SHACL 45 against 16, SPARQL 114 against 64 and controls 44,757 against 32,397, 3,361 against 2,735 and 15,188 against 6,068: the same ratios, with the small differences those of late-indexed submissions; the table keeps the first run. Abstracts of the seven topic hits read 20261103 01:45 UTC: 2610.33499 (translating RDF 1.2 to property graphs, 7 authors, v1 20261024) is among the three on topic in the window. Titles of the 45 and 16 SHACL hits read 20261103 01:46 UTC. A first run that included the term "RDF*" gave 136 against 80 and was discarded, because it matches any RDF paper (queries run 20261103 01:33 to 01:44 UTC)
22. The index entries [RDF](../index/rdf.md), [RDF-star](../index/rdf-star.md), [SPARQL](../index/sparql.md), [SHACL](../index/shacl.md), [triple](../index/triple.md) and [RDF Dataset Canonicalization](../index/rdf-dataset-canonicalization.md) : dates and facts of the RDF 1999 and 1.1 era, the RDF-star lineage, the canonicalization status; they cite their own primary sources (read 20261103 01:25 UTC)
23. [Infrastructure and MCP](./infrastructure-and-mcp.md) (page of 20261102 23:17 UTC: GQL and SQL/PGQ dates), [Asking graphs in natural language](./graph-query-generation.md) (SPARQL as a target of model-written queries) and [Building knowledge graphs with LLMs](./llm-kg-construction.md) (its shift is from fixed schemas to induced ones) (read 20261103 01:25 UTC)
24. docs/papers/README.md : "Standards" rule; one group per trend (read 20261103 01:40 UTC)
25. docs/trends/README.md : the two tests, the status values and the controls (read 20261103 01:23 UTC)
26. plans/20261102_1951-docs-catalogue.md : chapter 2 and the owner's review of 20261103, which adds this page (read 20261103 01:41 UTC)
27. https://www.w3.org/TR/rdf12-new/ and https://www.w3.org/TR/sparql12-new/ : What's New in RDF 1.2 and in SPARQL 1.2, Group Note Drafts of 14 July 2026, one history entry each; the SPARQL abstract and introduction are placeholders; the RDF note has an empty "Abstract Syntax" section; the RDF note counts "eleven RDF 1.2 and twelve SPARQL 1.2 documents" and its reference list gives SPARQL 1.2 Concepts as an Editor's Draft, which has no W3C publication page (read 20261103 01:24 UTC; re-read 02:04 UTC, histories 02:03 UTC)
28. https://www.w3.org/TR/1999/REC-rdf-syntax-19990222/ : RDF Model and Syntax Specification, W3C Recommendation 22 February 1999, reification: "Syntactically this is rather verbose" (read 20261103 02:07 UTC)
29. https://arxiv.org/abs/1406.3399 : Hartig and Thompson, "Foundations of an Alternative Approach to Reification in RDF", first submitted 13 June 2014 (arXiv API read 20261103 02:15 UTC)
30. https://www.w3.org/TR/rdf-canon/ : RDF Dataset Canonicalization, W3C Recommendation 21 May 2024: status section ("work on an updated specification is ongoing within the W3C RDF-star Working Group", "a future update to this specification will replace those with normative references to updated RDF specifications"); based on the RDF 1.1 definition (read 20261103 02:06 UTC)
31. https://www.w3.org/groups/wg/rdf-star/publications/ , https://www.w3.org/groups/wg/data-shapes/publications/ , https://www.w3.org/TR/rdf12-interop/ and https://www.w3.org/standards/history/rdf12-interop/ : the groups' lists of publications (11 RDF 1.2 documents and 11 SPARQL 1.2 documents for the RDF & SPARQL group; SHACL 1.2 Core, SPARQL-Related Features, Node Expressions, User Interfaces, Inference Rules, Profiling and SPARQL 1.2 RL for the Data Shapes group; older SHACL notes of 2017 left out); RDF 1.2 Interoperability, Group Note Draft 23 July 2026, 4 entries from 16 December 2025, editor Pierre-Antoine Champin (read 20261103 02:18 UTC)
