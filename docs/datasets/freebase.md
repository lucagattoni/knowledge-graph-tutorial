---
type: dataset
kinds: [kg]
updated: 20261102 21:29 UTC
---

# Freebase

This page answers what Freebase held, how big it was, under which licence its last dump is shared, how it ended, and which data sets still stand on it. Freebase was a community-edited [knowledge graph](../index/knowledge-graph.md) that Google shut down in 2015; its content partly moved to [Wikidata](wikidata.md). Benchmarks from 2013 to 2026 still use subsets of it.

## What it contains

Its authors described "a practical, scalable tuple database used to structure general human knowledge", created and maintained collaboratively and read or written through an HTTP query API in the Metaweb Query Language (MQL) [2]. Every object has an identifier (a "mid"), one or more types, and properties taken from those types [4]. A compound value type (CVT) stores a relation among more than two things, such as a political office with start and end dates, as an object of its own; other objects are "topics" [4]. Unlike [DBpedia](dbpedia.md) and [YAGO](yago.md), Freebase took contributions directly from human editors [8].

## Size and versions

Sources count in different units:

| Date | Count | Unit as worded | Source |
|---|---|---|---|
| 2008 | more than 125,000,000; 4,000 types; 7,000 properties | tuples | [2] |
| 2013 | around 1.2 billion; more than 80 million entities | triplets | [6] |
| 20150331 (read-only) | more than 3 billion; almost 50 million entities | facts | [4] |
| last dump page | 1.9 billion; 22 GB gzipped, 250 GB uncompressed | triples | [1] |

*Reading:* the units differ, and no source read explains two gaps: 1.2 against 1.9 billion [6][1], and the dump page's 1.9 billion against "more than 3 billion facts" in the migration paper [1][4]. The dump page also labels the dump "Updated: Weekly" while saying elsewhere that the dumps are not maintained [1]; the label sits oddly with a dump the page calls unmaintained. The same page offers 63,036,271 triples deleted until March 2013, and 2.1 million triples of Freebase to Wikidata mappings based on the Wikidata dump of 28 October 2013 [1].

Benchmarks use subsets. Their sizes are on the pages named in the last column, except FB1M, which has no page of its own:

| Subset | What it is | Sizes on |
|---|---|---|
| FB15k | entities of Freebase that are also in the Wikilinks database and have at least 100 mentions [6] | [FB15k-237](fb15k-237.md) |
| FB1M | the most frequent 1 million entities; Table 2 gives 23,382 relationships, the text of the same paper "around 25k", and the paper does not reconcile them [6] | here |
| FB2M, FB5M | extracts of Freebase [9] | [SimpleQuestions](simplequestions.md) |
| FB15k-237 | FB15k reduced to 237 relations [7] | [FB15k-237](fb15k-237.md) |
| Commons | the 86 domains of Freebase behind GrailQA [11] | [GrailQA](grailqa.md) |

## Licence

The dump page's License section says the dumps are "distributed, like Freebase itself, under the Creative Commons Attribution (aka CC-BY) and use is subject to the Terms of Service"; the Wikidata mappings are CC0 [1]. The visible text names no version, but the links behind "CC-BY" point to CC BY 2.5 [1], which matches the migration paper [4]. That paper says Google did not own parts such as images and long descriptions taken from Wikipedia. Removing them cut about 42 million of 3 billion facts (1.4%) before a CC0 dump could be made [4]. The subsets above carry no licence statement in the papers read: **unstated**.

## How it was made

Google's page calls it a "data-sharing project that ran from 2007 to 2015" [1]. Part of the content was imported from sources such as Wikipedia and the licence-compatible part of MusicBrainz; the community and Google then maintained it [4]. Google acquired Freebase in 2010 and used its content in the Knowledge Graph announced in 2012 [8].

| Date | Event | Source |
|---|---|---|
| 20141216 | Freebase announces it will close and offer its content to Wikidata | [3] |
| 20150331 | read-only; the MQL write API retired | [3][4] |
| 2015, planned third quarter | website closure planned | [3] |
| August 2016 | main address redirected to a developer page | [3] |

The migration (Pellissier Tanon et al., WWW 2016 [5]) merged four mappings into 4.56 million mapped items and built the Primary Sources Tool, where editors approve or reject proposed statements; about 90,000 actions were made by January 2016 [4]. Wikidata editors judged the quality too low for a direct import [4]. An import in 2015 worked through over 10% of the collection; the project page says the rest was unprocessed as of 2018 [3]. The Google page now says the API is shut down and the dumps "aren't maintained and no support can be provided" [1].

## Used by

| Use | What it takes from Freebase | Page |
|---|---|---|
| Bollacker et al., SIGMOD 2008 (6,061 citations, Semantic Scholar, read 20261102 20:05 UTC, carried over [14]) | the design paper | [papers: foundations](../papers/foundations.md) |
| Bordes et al., NeurIPS 2013 | FB15k and FB1M for [link prediction](../index/link-prediction.md) [6] | [papers: foundations](../papers/foundations.md) |
| FB15k-237 | FB15k, reduced to 237 relations [7] | [dataset](fb15k-237.md), [benchmark](../benchmarks/kg-link-prediction.md) |
| SimpleQuestions | questions paired with facts of the FB2M extract [9] | [SimpleQuestions](simplequestions.md) |
| WebQuestionsSP | questions with SPARQL queries for Freebase [10] | [dataset](webquestionssp.md), [benchmark](../benchmarks/webquestionssp.md) |
| ComplexWebQuestions | questions made from WebQuestionsSP queries [10] | [ComplexWebQuestions](complexwebquestions.md) |
| GrailQA | questions over the Commons domains [11] | [GrailQA](grailqa.md) |
| Search-on-Graph-R1 (2026) | evaluated on WebQSP, CWQ and GrailQA; each search call "executes against a live Freebase server" [13] | [learned graph traversal](../trends/learned-graph-traversal.md) |

The migration paper has 245 citations (Semantic Scholar, read 20261102 20:24 UTC, carried over [15]). Question-to-query work on these sets is in [graph query generation](../trends/graph-query-generation.md).

## Known problems

- **Frozen and unsupported.** GrailQA's authors write that Freebase "has stopped getting updated" yet "is still one of the largest publicly available KBs" [11]. The 2026 abstract names no host for its live server: **unstated** [13].
- **Quality.** The CoDEx authors write that "Freebase had known quality issues" and that outdated subsets are still most used [12].
- **Leakage.** FB15k "was shown to have train/test leakage" [12]. [FB15k-237](fb15k-237.md) is the repair [7].

## Sources

1. https://developers.google.com/freebase : dump page: API shut down, 1.9 billion triples, "Updated: Weekly" label, deleted triples, mappings, License section (CC-BY, links to CC BY 2.5, Terms of Service; CC0 for mappings), "not maintained" (read 20261102 20:48 UTC; License section and links re-read 20261102 21:25 UTC)
2. https://research.google/pubs/freebase-a-collaboratively-created-graph-database-for-structuring-human-knowledge/ : SIGMOD 2008 abstract: tuples, types, properties, MQL; authors Bollacker, Evans, Paritosh, Sturge, Taylor (read 20261102 20:49 UTC)
3. https://www.wikidata.org/wiki/Wikidata:WikiProject_Freebase?action=raw : closure dates, planned website closure, redirect, 2015 import share (read 20261102 20:48 UTC)
4. https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/44818.pdf : Pellissier Tanon et al., WWW 2016, full text: data model and CVTs, imports, more than 3 billion facts, CC BY 2.5, 42 million facts removed, quality examples, 4.56 million mappings, Primary Sources Tool figures (read 20261102 20:49 UTC; CC BY 2.5, 3 billion and 42 million re-read 20261102 21:27 UTC)
5. https://research.google/pubs/from-freebase-to-wikidata-the-great-migration/ : abstract and authors of the migration paper (read 20261102 20:49 UTC)
6. https://papers.nips.cc/paper_files/paper/2013/file/1cecc7a77928ca8133fa24680a88d2f9-Paper.pdf : Bordes et al., NeurIPS 2013, full text: 1.2 billion triplets, FB15k, FB1M ("around 25k" relationships in section 4; 23,382 in Table 2) (read 20261102 20:49 UTC; both FB1M figures re-read 20261102 21:27 UTC)
7. https://aclanthology.org/W15-4007.pdf : Toutanova and Chen, 2015: 401 relations, near-duplicate and inverse removal, 237 relations, filtered test pairs (read 20261102 20:52 UTC)
8. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., section 10.1: editor contributions, MQL, acquisition in 2010, Knowledge Graph (read 20261102 20:53 UTC)
9. https://arxiv.org/pdf/1506.02075v1 : Bordes et al., SimpleQuestions, section 3, Table 2: FB2M, FB5M, 108,442 questions (read 20261102 20:52 UTC)
10. https://arxiv.org/pdf/1803.06643v1 : Talmor and Berant, section 4.1: WebQuestionsSP 4,737 questions with Freebase SPARQL; 34,689 questions (read 20261102 20:52 UTC)
11. https://arxiv.org/pdf/2011.07743v6 : Gu et al., GrailQA: 64,331 questions, Commons 86 domains, 2,038 classes, 45 million entities, "stopped getting updated" (read 20261102 20:52 UTC)
12. https://arxiv.org/pdf/2009.07810v2 : Safavi and Koutra, CoDEx, introduction: quality issues, FB15k leakage (read 20261102 20:52 UTC)
13. https://export.arxiv.org/api/query?id_list=2607.18481 : Search-on-Graph-R1 abstract, 20 July 2026 (read 20261102 20:54 UTC)
14. https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/1376616.1376746?fields=citationCount : 6,061 citations for Bollacker et al., SIGMOD 2008 (read 20261102 20:05 UTC; carried over from the research notes of this documentation, not re-queried; DOI checked against Crossref 20261102 21:27 UTC)
15. https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/2872427.2874809?fields=citationCount : 245 citations for Pellissier Tanon et al., WWW 2016 (read 20261102 20:24 UTC; carried over from the research notes of this documentation, not re-queried; DOI checked against Crossref 20261102 21:27 UTC)
