---
type: dataset
kinds: [kg]
updated: 20261102 21:33 UTC
---

# DBpedia

This page answers what the DBpedia knowledge graph contains, how large it is, under which licence it is released, and how it is made. DBpedia extracts structured facts from Wikipedia and publishes them as [linked data](../index/linked-data.md) since 2007 [1]. It has no benchmark page of its own; the benchmarks that use it are listed under "Used by".

## What it contains

DBpedia is "a crowd-sourced community effort to extract structured content" from Wikimedia projects, served as linked data and queryable with [SPARQL](../index/sparql.md) [1]. Its community [ontology](../index/ontology.md) has 768 classes and 3,000 properties [2]. Today DBpedia is several collections, not one graph [2][3][5]:

| Collection | What the project says |
|---|---|
| Latest Core ("Tiny Diamond") | English Wikipedia articles and infoboxes, plus labels and abstracts from the largest language editions, links and `rdf:type` statements; the smallest collection [5] |
| Main knowledge graph | "cleaned data from Wikipedia in all languages and Wikidata" [4] |
| Largest Diamond (beta) | 220 million entities, 1.45 billion triples, from DBpedia, GeoNames, DNB, MusicBrainz and others [3] |
| Fusion KG (beta) | a newer dataset, under the Business Source License 1.1 [3] |

## Size and versions

No single comparable size exists: the project's figures mix collections **(unstated: which collection each refers to)**.

| When | Figure | Source |
|---|---|---|
| 2007 paper | 1.95 million "things", about 103 million triples, abstracts in 13 languages | [7] |
| Journal preprint, English edition | 3,769,926 instances; 33,742,015 mapping-based statements; ontology of 320 classes and 1,650 properties; 1.8 billion facts over 100+ languages | [6] |
| Latest Core, January 2021 | about 900 million triples | [5] |
| Home page, read now | "more than 228 million entities"; around 20 language chapters | [4] |

The project states a snapshot release every three months and a monthly development release, both on the DBpedia Databus [2]. A bot, MARVIN, runs the extraction by cron job [5]. The Databus catalogue has a SPARQL endpoint [8]. Its version strings are not uniform (`2018.08.15` in `generic`, `2025-12-01` in `dbpedia-wikipedia-kg-dump`), so the dates here are the `dct:issued` dates, not the strings. The groups `generic`, `mappings`, `text` and `wikidata` of the account `dbpedia` have 20221201 as their newest issue date. The newest issue date under the account is 20251218, in the groups `dbpedia-wikipedia-kg-dump` and `dbpedia-wikidata-kg-dump` [8]. Why the monthly releases do not appear there is **unstated**. The query behind these dates (the licence counts under "Licence" use a second one, shown after it):

```sparql
PREFIX databus: <https://dataid.dbpedia.org/databus#>
PREFIX dct: <http://purl.org/dc/terms/>
SELECT ?group (MAX(?issued) AS ?newest) WHERE {
  ?v a databus:Version ; dct:issued ?issued .
  FILTER(STRSTARTS(STR(?v), "https://databus.dbpedia.org/dbpedia/"))
  BIND(STRBEFORE(STRAFTER(STR(?v), "https://databus.dbpedia.org/dbpedia/"), "/") AS ?group)
} GROUP BY ?group ORDER BY DESC(?newest)
```

The licence query, same prefixes:

```sparql
SELECT ?license (COUNT(DISTINCT ?v) AS ?versions) WHERE {
  ?v a databus:Version ; dct:license ?license .
  FILTER(STRSTARTS(STR(?v), "https://databus.dbpedia.org/dbpedia/"))
} GROUP BY ?license
```

## Licence

The About page says the data is available under "the Creative Commons Attribution-ShareAlike 3.0 License and the GNU Free Documentation License" [1]. The Databus labels each version separately. Of 1,256 versions under the account `dbpedia`, 999 are labelled CC BY 3.0, 203 CC0, 32 CC BY-SA 3.0, 21 CC BY-SA 4.0 and 1 CC BY 4.0 [8]. The About page and the labels disagree; the reason is **unstated**, so check the licence of the artifact you download. The extraction framework's repository has no licence file at its root, so the code licence is **unstated** [17].

## How it was made

1. A Wikipedia dump (or the MediaWiki API) is read and each page is parsed into a syntax tree [6].
2. Extractors turn the tree into RDF statements. They fall in four groups: mapping-based infobox, raw infobox, single-feature, and statistical [6].
3. Mapping-based extraction uses manually written mappings from infoboxes to the ontology, which the community maintains in a Mappings Wiki. Raw extraction needs no mappings and gives lower quality [6].
4. The 2007 version used pattern matching on infobox templates and shipped YAGO-based types [7].

## Used by

| User | What it takes | Page |
|---|---|---|
| BEIR | its DBPedia-Entity v2 task uses the English DBpedia of October 2015; the BEIR paper lists it under CC BY-SA 3.0 [10] | [BEIR](../benchmarks/beir.md) |
| LC-QuAD 1.0 | the DBpedia release of April 2016 [9] | [LC-QuAD](../benchmarks/lc-quad.md), [data](lc-quad.md) |
| Text2KGBench | a part named DBpedia-WebNLG; the paper builds it from the WebNLG 3.0 corpus and does not state a DBpedia version **(unstated)** [11] | [Text2KGBench](../benchmarks/text2kgbench.md); trend [LLM-built graphs](../trends/llm-kg-construction.md) |
| TEXT2SPARQL challenge | a DBpedia task in 2025 (English and Spanish subset of DBpedia 2015-10) and in 2026, where the version is **unstated** in the paper read [13][14] | trend [query generation](../trends/graph-query-generation.md) |
| [ConceptNet](conceptnet.md) | a subset of DBpedia among its sources [12] | |
| [YAGO](yago.md) | the 2007 DBpedia release carried YAGO types [7] | |

The fundamental paper is Auer et al. 2007, in [the foundations group](../papers/foundations.md). Semantic Scholar counted 5,925 citations for it and 3,738 for the 2015 journal paper on 20261102 20:01 UTC; the counts are carried over from the research pass and were not re-queried [18].

## Known problems

- **Quality.** The authors write that extracted data is "unlikely to reach the quality of completely manually curated data sources" [6].
- **Consistency.** The YAGO team, a rival, says DBpedia is "not fully consistent" and that its curated part holds "just 4M instances" [16]; its own site says 5 million [15]. Treat both as rival claims.
- **Duplicate properties.** A 2025 challenge participant found at least four population properties that return different results [13].
- **Version drift.** The public endpoint no longer serves DBpedia 04-2016, so many LC-QuAD queries return nothing [9].
- **Dates.** The journal preprint says the project started in 2006 [6]; the About page says 2007 [1].
- **Test-set size is unclear.** One paper counts the 2025 DBpedia challenge set as 200 questions, 100 per language [13]. Another says it "consists of 100 natural language questions in English and Spanish" [14]; whether that is per language is **unstated**.

## Sources

1. https://www.dbpedia.org/about/ : what DBpedia is, start 2007, licence sentence (read 20261102 20:50 UTC)
2. https://www.dbpedia.org/resources/ : Databus, release cadence, ontology size (read 20261102 20:50 UTC)
3. https://www.dbpedia.org/resources/knowledge-graphs/ : Largest Diamond, Fusion KG licence (read 20261102 20:50 UTC)
4. https://www.dbpedia.org/ : "more than 228 million entities", chapters, main graph (read 20261102 20:50 UTC)
5. https://www.dbpedia.org/resources/latest-core/ : Latest Core content, 900 million triples, MARVIN (read 20261102 20:52 UTC)
6. https://www.semantic-web-journal.net/system/files/swj499.pdf : Lehmann et al., journal preprint, full text: extraction, Table 2, ontology size, quality quote (read 20261102 20:52 UTC)
7. https://web.archive.org/web/2012/http://iswc2007.semanticweb.org/papers/715.pdf : Auer et al., ISWC 2007, full text (read 20261102 20:54 UTC)
8. https://databus.dbpedia.org/sparql : SPARQL queries on version licences and issue dates, query text on this page; counts re-run and equal (read 20261102 21:31 UTC)
9. https://github.com/AskNowQA/LC-QuAD : README: 5,000 pairs, DBpedia 04-2016, endpoint note (read 20261102 20:59 UTC)
10. https://arxiv.org/abs/2104.08663 : BEIR paper, full text: DBPedia-Entity task on the English DBpedia of October 2015, CC BY-SA 3.0 list (read 20261102 21:30 UTC)
11. https://arxiv.org/abs/2308.02357 : Text2KGBench paper, full text: section 3.2, DBpedia-WebNLG built from WebNLG 3.0, no DBpedia version given (read 20261102 21:29 UTC)
12. https://arxiv.org/abs/1612.03975 : ConceptNet 5.5, full text: sources (read 20261102 20:58 UTC)
13. https://arxiv.org/abs/2510.02200 : ARUQULA, a challenge participant: DB25 (DBpedia 2015-10 subset, 200 questions split equally between English and Spanish) and the population-property problem (full text, read 20261102 21:30 UTC)
14. https://arxiv.org/abs/2610.13648 : SPARQL-LLM in TEXT2SPARQL 2026: DBpedia task of 50 questions in 2026, the 2025 test set of "100 natural language questions in English and Spanish" (full text, read 20261102 21:30 UTC)
15. https://yago-knowledge.org/getting-started : YAGO's comparison with DBpedia (read 20261102 20:50 UTC)
16. https://arxiv.org/abs/2308.11884 : YAGO 4.5 paper, full text: DBpedia remark (read 20261102 20:58 UTC)
17. https://api.github.com/repos/dbpedia/extraction-framework (via `gh api`) : no licence file at the root (read 20261102 21:00 UTC)
18. https://api.semanticscholar.org/graph/v1/paper/ : `citationCount`, looked up by title for Auer et al., "DBpedia: A Nucleus for a Web of Open Data" (ISWC 2007), 5,925, and Lehmann et al., "DBpedia - A large-scale, multilingual knowledge base extracted from Wikipedia" (Semantic Web journal 2015), 3,738 (read 20261102 20:01 UTC by the research pass; carried over, not re-queried; counts move daily)
