---
type: dataset
kinds: [kg]
updated: 20261102 21:29 UTC
---

# Wikidata

This page answers what Wikidata holds, how big it is, who may reuse it, how it is made, and where it is used. It is an open, community-edited [knowledge graph](../index/knowledge-graph.md); in December 2014 Google offered it the content of [Freebase](freebase.md) [11]. It has no benchmark of its own; other pages pin a snapshot of it.

## What it contains

Wikidata is a "free, collaborative, multilingual, secondary knowledge base" that supports Wikipedia and the other Wikimedia wikis [1]. Its parts [1][2][3]:

- **Items** have an identifier (Q plus a number), a label, a description and aliases.
- **Statements** pair a property (P plus a number) with a value. A statement may carry qualifiers, references (sources) and a rank (normal, preferred or deprecated).
- **Sitelinks** tie an item to pages on client wikis such as Wikipedia. **Identifiers** are properties that point to external databases.

"Secondary" means that it records what a source says, not what is true, so contradictory claims coexist, and ranks mark the preferred one [1][2][3][10].

## Size and versions

| Measure | Value | As of | Source |
|---|---|---|---|
| Items (the site's content-page count, which the Statistics page labels items) | 123,874,216 | read 20261102 | [4][5] |
| Edits since launch; active users | 2,563,447,838; 48,941 | read 20261102 | [4] |
| Size | about 70 million statements on 18 million entities | September 2015 | [10] |
| Statements | **unstated**: no page read gives a count | | [4][5][6] |
| Triples in the query-service graph (RDF triples, not statements) | over 16 billion | before the 9 May 2025 split; the date of the figure is **unstated** | [13] |

The query-service figure is the size of the graph that the split was meant to reduce; the main graph is now smaller by an unstated amount [13]. There are no version numbers: the graph changes every minute, so a data set built from it names a dump date. JSON dumps ("recommended") are created weekly. RDF dumps come in Turtle and N-Triples ("all" statements) and as "truthy" N-Triples that keep only best-rank direct values, with no qualifiers and no references [6]. On 20261102 the compressed files were 156,705,985,721 bytes (all statements, JSON), 509,231,082,342 (all statements, N-Triples) and 71,803,150,133 (truthy N-Triples) [7].

The query service, built on Blazegraph, was split on 9 May 2025 into a main graph and a scholarly-articles graph, because one instance could no longer carry the size, the edits and the queries [13].

## Licence

"All structured data (i.e. the main, Property, Lexeme, and EntitySchema namespaces) is released into the public domain under Creative Commons Zero." Text in other namespaces is CC BY-SA 4.0 [8]. Wikidata accepts only CC0 or public-domain data; no other licence is compatible [8]. Data sets derived from it state their own licences (see [YAGO](yago.md) and the pages below).

## How it was made

It went live on 29 October 2012 [9] and is hosted by the Wikimedia Foundation [10]. Communities of volunteers build it [12]: editors "decide on the rules of content creation and management", and bots also enter data [1]. Editing reaches the schema level, with sub-class and inverse-property axioms and shapes [12]. A tool lets editors approve or reject Freebase-derived statements one by one [10]: see the [Freebase page](freebase.md).

Wikimedia Deutschland's Embedding Project started in 2024 [14]. Its project page gives 1 October 2025 as the launch, citing only a social-media post that was not read, so that date is unverified [14]. Its Vector Database merges [vector search](../index/vector-search.md) with keyword search and names an [MCP](../index/model-context-protocol.md) implementation. It is an alpha release, embedded from the May 2026 snapshot [15].

## Used by

| Use | Which part of Wikidata | Page |
|---|---|---|
| Vrandečić and Krötzsch, CACM 2014 (2,849 citations, Semantic Scholar, read 20261102 20:01 UTC, carried over [27]) | the design paper [16] | [papers: foundations](../papers/foundations.md) |
| ogbl-wikikg2 | all statements, three snapshots of 2015 (May, August, November) [17] | [OGB link prediction](../benchmarks/ogb-link-prediction.md) |
| Wikidata5M | the July 2019 dump; 4,594,485 entities [18] | none |
| CoDEx | 1,156,222 triples before filtering; snapshot date **unstated** [19] | none |
| PopQA | triples from which questions were made [20] | [PopQA](popqa.md) |
| 2WikiMultiHopQA | structured data to build questions and evidence paths [21] | [dataset](2wikimultihopqa.md), [benchmark](../benchmarks/2wikimultihopqa.md) |
| LC-QuAD 2.0 | SPARQL queries over Wikidata and DBpedia 2018 [22] | [LC-QuAD](lc-quad.md) |
| Text2KGBench | its Wikidata-TekGen subset [23] | [benchmark](../benchmarks/text2kgbench.md) |
| YAGO 4.6 | "A Logically Consistent Subset of Wikidata" [24] | [YAGO](yago.md) |
| DBpedia | its extraction bot includes Wikidata among its sources [25] | [DBpedia](dbpedia.md) |
| OntoKG (2026) | a January 2026 dump [26] | [LLM knowledge-graph construction](../trends/llm-kg-construction.md) |

Question-to-query sets over Wikidata belong to [graph query generation](../trends/graph-query-generation.md). The vector database above belongs to [infrastructure and MCP](../trends/infrastructure-and-mcp.md).

## Known problems

- **A moving target.** The sets above fix 2015, 2019 and 2026 graphs. *Reading:* scores on two of them are not comparable, because the graphs differ [17][18][26].
- **Scale.** The 2025 query-service split means the endpoint `query.wikidata.org` no longer holds the full graph; a query that needs both graphs must federate [13].
- **Claims, not facts.** The truthy dump drops qualifiers, references and non-best ranks [6]. *Reading:* a system that reads only truthy triples cannot see disagreement between sources.
- **Open world.** Knowledge graphs hold positive statements; a missing triple is [unseen, not false](../index/closed-world-assumption.md), so evaluation sets must construct negatives [19].
- **Consistency.** YAGO's team calls its release a "simplified, cleaned" version of Wikidata and logs the statements it dropped [24]; this is their claim, not measured here.

## Sources

1. https://www.wikidata.org/wiki/Wikidata:Introduction?action=raw : definition, editors and bots, data model (read 20261102 20:50 UTC)
2. https://www.wikidata.org/wiki/Help:Statements?action=raw : statements, qualifiers, references, ranks, plurality of perspectives (read 20261102 20:50 UTC)
3. https://www.wikidata.org/wiki/Help:Ranking?action=raw : normal, preferred, deprecated ranks (read 20261102 20:50 UTC)
4. https://www.wikidata.org/w/api.php?action=query&meta=siteinfo&siprop=statistics&format=json : articles 123,874,216, edits 2,563,447,838, active users 48,941 (read 20261102 20:48 UTC)
5. https://www.wikidata.org/wiki/Wikidata:Statistics?action=raw : the page prints the article count as the number of items (read 20261102 20:50 UTC)
6. https://www.wikidata.org/wiki/Wikidata:Database_download?action=raw : weekly JSON, RDF all and truthy dumps (read 20261102 20:48 UTC)
7. https://dumps.wikimedia.org/wikidatawiki/entities/ : file listing and byte sizes (read 20261102 20:48 UTC)
8. https://www.wikidata.org/wiki/Wikidata:Licensing?action=raw : CC0 and CC BY-SA 4.0 statement (read 20261102 20:48 UTC)
9. https://www.wikidata.org/wiki/Wikidata:Birthday?action=raw : "Wikidata went live on 29 October 2012" (read 20261102 20:55 UTC)
10. https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/44818.pdf : Pellissier Tanon et al., WWW 2016, full text: Wikidata in September 2015, hosting, claims, migration tool, January 2016 usage (read 20261102 20:49 UTC)
11. https://www.wikidata.org/wiki/Wikidata:WikiProject_Freebase?action=raw : December 2014 offer of Freebase content (read 20261102 20:48 UTC)
12. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., section 10.1.4, schema-level editing, secondary source (read 20261102 20:53 UTC)
13. https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/WDQS_graph_split?action=raw : split on 9 May 2025, Blazegraph, over 16 billion triples (undated in the source), federation (read 20261102 20:54 UTC; re-read 20261102 21:25 UTC)
14. https://www.wikidata.org/wiki/Wikidata:Embedding_Project?action=raw : Embedding Project, started 2024, launch date 1 October 2025 cited to a social-media post (read 20261102 20:54 UTC; re-read 20261102 21:25 UTC)
15. https://www.wikidata.org/wiki/Wikidata:Vector_Database?action=raw : hybrid search with RRF, MCP mention, alpha, May 2026 snapshot, September 2026 update (read 20261102 20:54 UTC)
16. https://api.crossref.org/works/10.1145/2629489 : "Wikidata: a free collaborative knowledgebase", CACM 57(10), published 23 September 2014 (read 20261102 20:50 UTC)
17. https://ogb.stanford.edu/docs/linkprop/ : ogbl-wikikg2 description and snapshots (read 20261102 20:52 UTC)
18. https://arxiv.org/pdf/1911.06136v3 : KEPLER, Table 1 and section 3.1 (read 20261102 20:52 UTC)
19. https://arxiv.org/pdf/2009.07810v2 : CoDEx, sections 3 and 1, open-world assumption (read 20261102 20:52 UTC)
20. https://arxiv.org/pdf/2212.10511v4 : PopQA built from Wikidata triples, 14k questions (read 20261102 20:52 UTC)
21. https://export.arxiv.org/api/query?id_list=2011.01060 : 2WikiMultiHopQA abstract, Wikidata structured data (read 20261102 20:55 UTC)
22. https://huggingface.co/datasets/mohnish/lc_quad/raw/main/README.md : card for LC-QuAD 2.0, `sparql_wikidata` and `sparql_dbpedia18` fields (read 20261102 20:55 UTC)
23. https://export.arxiv.org/api/query?id_list=2308.02357 : Text2KGBench abstract (read 20261102 20:51 UTC)
24. https://yago-knowledge.org/downloads/yago-4-6 : YAGO 4.6, ISWC 2026 demo title, "simplified, cleaned", excluded-statement logs (read 20261102 20:52 UTC)
25. https://www.dbpedia.org/resources/knowledge-graphs/ : Marvin bot releases include Wikidata (read 20261102 20:52 UTC)
26. https://export.arxiv.org/api/query?id_list=2604.02618 : OntoKG abstract, January 2026 dump (read 20261102 20:54 UTC)
27. https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/2629489?fields=citationCount : 2,849 citations for the CACM paper (read 20261102 20:01 UTC; carried over from the research notes of this documentation, not re-queried; DOI checked against source 16)
