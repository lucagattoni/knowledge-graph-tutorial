---
type: era
period: 2001-2011
order: 5
updated: 20261102 23:11 UTC
---

# The semantic web and linked data

This page answers: how did knowledge on the web become a set of standards and public datasets, and what did the web companies build for data and search in the same decade? The previous era is [The Web changes data and search](the-web.md); the next is [Knowledge graphs at scale](knowledge-graphs-at-scale.md); the whole span is on the [chapter overview](README.md).

## Dates and boundaries

**The scheme is this documentation's.** No source read gives one periodisation for all four threads. The boundaries are points that at least two sources share. Hitzler, reviewing the [semantic web](../index/semantic-web.md) field, calls his own timeline "subjective" [3].

**Start, 2001.** Hitzler writes that the *Scientific American* article of 2001 "arguably marks the birth of the field", and adds that naming any such point "is of course debateable at best" [3]. The article, by Berners-Lee, Hendler and Lassila, is dated 1 May 2001 [2]; W3C announced it as the cover story on 20010413 [1]. Gutierrez and Sequeda place the Semantic Web in their period "The 2000s" [4], and Sowa cites the 2001 article when he calls the Semantic Web "a large [semantic network](../index/semantic-network.md)" [5].

**End, 16 May 2012.** Google's post "things, not strings" announced its [Knowledge Graph](../index/google-knowledge-graph.md) with "more than 500 million objects" and "more than 3.5 billion facts" (first-party) [14]. Hogan et al., citing Bergman, call it "a watershed moment in terms of adopting the phrase 'knowledge graph'" [15], and Hitzler starts his third phase there [3]. Gutierrez and Sequeda do not treat 2012 as a boundary [4], and Hitzler's phases "overlap" [3]. The period reads 2001-2011 because 2011 is the last full year. Two events sit on the line: [schema.org](../index/schema-org.md) (20110602) [13] and [Wikidata](../index/wikidata.md) (launched 20121029 per Wikimedia Deutschland, first-party [36], and the Wikipedia Signpost of that day, which says "launched this week" [37]; Hitzler and Hogan et al. give the year only [3][15]). This page keeps schema.org and puts Wikidata in the next era.

## What changed

Knowledge on the web became W3C standards: [RDF](../index/rdf.md) and [OWL](../index/owl.md) in 2004 [6][7], [SPARQL](../index/sparql.md) in 2008 [9], SKOS in 2009 [10]. The focus then moved from hand-built [ontologies](../index/ontology.md) to [linked data](../index/linked-data.md) [3]. The first large open graphs appeared ([DBpedia](../index/dbpedia.md), [YAGO](../index/yago.md), [Freebase](../index/freebase.md)) [15]. Web companies built data systems outside SQL and trained search ranking on query logs [19][24].

## The threads

### KB/KG

The main thread shifted from expert-written knowledge bases to graphs extracted or edited at scale. DBpedia started in 2007 and is published as linked data, queryable with SPARQL (first-party) [16]. YAGO extracts from Wikipedia and unifies the result with the hierarchy of [WordNet](../index/wordnet.md) [15]. Freebase took edits from people instead; its 2008 paper (by its own authors) reports more than 125,000,000 tuples, 4000 types and 7000 properties [18]. Google acquired it in 2010; it went read-only in March 2015 and much of its content was moved to Wikidata [15]. [Cyc](../index/cyc.md) is the hand-built common-sense base begun in 1984, on Lenat's account and Cycorp's [38][39] (Hogan et al. write "since 1986": see disputes); it is proprietary and has an open subset, OpenCyc [15]. Hogan et al. give no date for OpenCyc's publication and do not say how Cyc developed in 2001-2011 (**unstated**). The phrase "knowledge graph" "did not permeate widely until the second decade" of the century [4].

### Ontologies and the semantic web

Hitzler's first phase is driven by ontologies and spans the early to mid 2000s [3]. The DAML programme ran from 2000 to 2006; OIL, from an EU project, was later merged with DAML, which led to OWL [3]. OWL has three sublanguages, Lite, DL and Full [7]; its core rests on a [description logic](../index/description-logic.md) [3]. Around the mid-2000s "over-hyped expectations" gave way to a more sober view, because ontologies proved "hard to maintain and re-use" [3].

The second phase starts with the Linked Data note of 20060727 [8]. It gives four rules: use [URIs](../index/uri.md) as names, use HTTP URIs, return useful information in RDF or SPARQL on lookup, and link to other URIs [8]. In the early 2010s the hype eased again, since "shallow non-expressive schemas" hampered reuse [3]. Meanwhile the lighter vocabularies did well: Hitzler names SKOS among the standards near RDF and OWL that gained significant traction [3], and schema.org was announced by Google, Bing and Yahoo! on 20110602 (first-party) [13]. Hitzler says Yandex joined "slightly later" [3]; schema.org's own page lists Yandex among the founding companies (first-party) [34]. A 2015 report found schema.org annotations on over 30% of pages [3].

### Databases and search

Web companies built their own stores: MapReduce was published at OSDI 2004 [20], Hadoop followed in 2005 [19], Bigtable in 2006 [21], Dynamo in 2007 [22]. Gutierrez and Sequeda say Google introduced an infrastructure for large data with MapReduce, and that the boom of non-relational, distributed stores such as CouchDB, Bigtable and Dynamo gave rise to [NoSQL](../index/nosql.md) databases [4]; they do not name Hadoop in that passage. Stonebraker and Pavlo, who argue for the [relational model](../index/relational-model.md), write that Hadoop "died about a decade ago" and that almost every NoSQL system added a [SQL](../index/sql.md) interface by the end of the 2010s [19]. That is their stance (see disputes). On the graph side, [Neo4j](../projects/neo4j.md) 1.0 was reported on 20100225 as a [property graph](../index/property-graph.md) database; "1.0" signalled a stable API [23].

In search, ranking functions had been tuned by hand; [learning to rank](../index/learning-to-rank.md) "only became truly effective" with web query logs in the 2000s [24], and reached "its zenith in the early 2010s" with tree ensembles [25]. [Information retrieval](../index/information-retrieval.md) research also took up question answering through TREC [24].

### RAG and agent memory

Nothing in this era is [retrieval-augmented generation](../index/retrieval-augmented-generation.md) or agent memory (**unstated**: the sources read do not mention either). The precursor is [question answering](../index/question-answering.md): TREC lists QA data from 1999 (TREC-8) to 2007 inside this era, then Live QA tracks for 2015 to 2017 [26], and IBM's Watson beat two Jeopardy! champions in February 2011 [27]. IBM says it generated hypotheses and gathered evidence [27]. *Reading:* Watson is a precursor of retrieval plus answering, not of retrieval plus a language model; no source calls it RAG. What followed is in [Language models meet retrieval](language-models-meet-retrieval.md).

## Dated events

| Date | Event | Thread | Source |
|---|---|---|---|
| 200105 | "The Semantic Web" cover story, *Scientific American* | Ontologies | [2] |
| 20040210 | OWL and RDF 1.0 become W3C Recommendations (later RDF 1.1) | Ontologies | [6][7] |
| 2004 | MapReduce paper, OSDI | Databases and search | [20] |
| 2006 | Bigtable paper, OSDI | Databases and search | [21] |
| 20060727 | Linked Data design note | Ontologies | [8] |
| 2007 | DBpedia project starts; Dynamo paper | KB/KG; Databases and search | [16][22] |
| 20080115 | SPARQL becomes a W3C Recommendation | Ontologies | [9] |
| 2008 | Freebase paper, SIGMOD | KB/KG | [18] |
| 20090818 | SKOS becomes a W3C Recommendation | Ontologies | [10] |
| 20091027 | OWL 2 Recommendation (Second Edition 20121211) | Ontologies | [11] |
| 2010 | Google acquires Freebase | KB/KG | [15] |
| 20100225 | Neo4j 1.0 reported | Databases and search | [23] |
| 201102 | Watson wins Jeopardy! | RAG and memory | [27] |
| 20110602 | schema.org announced | Ontologies | [13] |
| 20120516 | Google Knowledge Graph announced (ends the era) | KB/KG | [14] |

## Systems and projects

| System | Role in the era | Status in this documentation |
|---|---|---|
| DBpedia | Wikipedia as linked data [16] | Era role complete; the project is still active (it lists a snapshot every 3 months and a monthly development version, first-party [16]); see the [projects chapter](../projects/README.md) |
| YAGO | Wikipedia plus WordNet [15] | Era role complete; the project is still active (first-party news lists YAGO 4.6 in July 2026 [17]); see the [projects chapter](../projects/README.md) |
| Freebase | Community-edited graph [18] | Read-only since March 2015; much of its content moved to Wikidata [15] |
| Cyc / OpenCyc | Hand-built common sense [15] | Offered as a product by Cycorp (first-party) [35]; begun 1984 [38][39] |
| Neo4j | Property-graph database [23] | Named the most popular OLTP graph DBMS in 2024 [19]; its place is still open, see [chapter 2](../trends/README.md) |
| MapReduce, Hadoop | Batch processing [19][20] | Replaced, on the authors' account [19] |

## Ideas and disputes

- **RDF's first standard.** W3C published *RDF Model and Syntax* as a Recommendation on 19990222 [12]; Hitzler writes "Also in 2004" RDF became a W3C standard [3], and the 2004 document is RDF 1.0 Concepts [6]. *Reading:* both are true of different documents; this page starts the era at the 2001 article instead.
- **Did ontologies work?** Hitzler: often "hard to maintain and re-use" [3]. Yet he reports SNOMED CT "fully formalized in OWL and widely used" [3], and Gutierrez and Sequeda say description logics became "the underpinning to OWL" [4]. Sowa notes most OWL applications use only the EL subset [5].
- **Is "knowledge graph" new?** Hitzler: "mostly a new framing" of semantic-web ideas [3]; Gutierrez and Sequeda: "a reincarnation of the Semantic Web, and Linked Data" [4]. Hogan et al. call the definition "contentious" [15].
- **Fate of graph databases.** Angles and Gutierrez (2008): such models "took off in the eighties", faded, then regained relevance [28]. Stonebraker and Pavlo question whether specialised systems can overcome their disadvantages, noting SQL:2023 added property-graph queries [19].
- **Cyc's start.** Lenat (1995) and Cycorp say 1984 [38][39]; Hogan et al. write "since 1986" [15]. *Reading:* the two first-hand accounts agree, so this page uses 1984; the survey's reason for 1986 is **unstated** in the passage read.

## Papers and standards

Group page: [foundations](../papers/foundations.md).

- Berners-Lee, Hendler, Lassila, "The Semantic Web", *Scientific American*, May 2001 [2].
- RDF 1.0 and OWL 1.0, W3C Recommendations, 20040210 [6][7]; SPARQL, 20080115 [9]; SKOS, 20090818 [10]; OWL 2, 20091027 [11].
- Berners-Lee, "Linked Data", design note, 20060727 [8].
- Dean and Ghemawat, "MapReduce", OSDI 2004 [20]; Chang et al., "Bigtable", OSDI 2006 [21]; DeCandia et al., "Dynamo", 2007 [22].
- Bollacker et al., "Freebase", SIGMOD 2008 [18].

## Left unsolved

Ontologies stayed costly to reuse, and linked data's schemas were shallow [3]. Combining logic and statistics was open: "little is yet known on how to integrate" them [4]. The standards also kept moving: RDF 1.1 (2014) and SPARQL 1.1 (2013) are the latest Recommendations [29][31], while RDF 1.2 is a Candidate Recommendation Snapshot (7 April 2026), and SPARQL 1.2 and SHACL 1.2 are Working Drafts, all as read on 20261102 [30][32][33]; see [chapter 2](../trends/README.md). What came next is in [Knowledge graphs at scale](knowledge-graphs-at-scale.md).

## Sources

1. https://www.w3.org/news/2001/semantic-web-featured-in-scientific-american : W3C news item of 13 April 2001 naming the May 2001 cover story (read 20261102 19:54 UTC)
2. https://www.scientificamerican.com/article/the-semantic-web/ : article page, 1 May 2001, Vol. 284 No. 5, three authors (read 20261102 19:54 UTC)
3. https://par.nsf.gov/servlets/purl/10292869 : Hitzler, "A Review of the Semantic Web Field", CACM 2021 (author version); phases, 2001 as birth, ontologies, Linked Data, schema.org, Wikidata (read 20261102 20:10 UTC)
4. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 2021; period "The 2000s", MapReduce, CouchDB, Bigtable and Dynamo giving rise to NoSQL, OWL, term "knowledge graph" (read 20261102 20:10 UTC)
5. https://www.jfsowa.com/pubs/semnet.htm : Sowa, "Semantic Networks"; Semantic Web as semantic network, OWL EL subset (read 20261102 19:59 UTC)
6. https://www.w3.org/TR/rdf10-concepts/ : RDF Concepts and Abstract Syntax, Recommendation 10 February 2004, "New Version Available: RDF 1.1" (read 20261102 19:54 UTC)
7. https://www.w3.org/TR/2004/REC-owl-features-20040210/ : OWL Overview, Recommendation 10 February 2004, three sublanguages (read 20261102 19:54 UTC)
8. https://www.w3.org/DesignIssues/LinkedData.html : Berners-Lee, Linked Data, dated 2006-07-27, four rules (read 20261102 19:54 UTC)
9. https://www.w3.org/TR/rdf-sparql-query/ : SPARQL Query Language for RDF, Recommendation 15 January 2008 (read 20261102 19:54 UTC)
10. https://www.w3.org/TR/skos-reference/ : SKOS Reference, Recommendation 18 August 2009 (read 20261102 19:54 UTC)
11. https://www.w3.org/TR/owl2-overview/ : OWL 2 Overview (Second Edition) 11 December 2012, refers to the Recommendation of 27 October 2009 (read 20261102 19:54 UTC)
12. https://www.w3.org/TR/1999/REC-rdf-syntax-19990222/ : RDF Model and Syntax, Recommendation 22 February 1999 (read 20261102 19:54 UTC)
13. https://googleblog.blogspot.com/2011/06/introducing-schemaorg-search-engines.html : Google, "Introducing schema.org", 2 June 2011, Google, Bing and Yahoo! (first-party; read 20261102 19:55 UTC)
14. https://blog.google/products/search/introducing-knowledge-graph-things-not/ : Singhal, 16 May 2012; 500 million objects, 3.5 billion facts (first-party; read 20261102 19:54 UTC)
15. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", section 10.1 and Appendix A; YAGO, Freebase (read-only March 2015, content migrated to Wikidata), Cyc (since 1986, OpenCyc), "watershed moment" (citing Bergman), "contentious" (read 20261102 20:10 UTC)
16. https://www.dbpedia.org/about/ : DBpedia About; project started 2007, Linked Data and SPARQL, snapshot release every 3 months (first-party; read 20261102 20:10 UTC)
17. https://yago-knowledge.org/ : YAGO home; news items to October 2026, including YAGO 4.6 in July 2026 (first-party; read 20261102 20:10 UTC)
18. https://research.google/pubs/freebase-a-collaboratively-created-graph-database-for-structuring-human-knowledge/ : Bollacker et al., SIGMOD 2008 abstract; tuple, type and property counts (first-party; read 20261102 19:55 UTC)
19. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 2024; Hadoop, NoSQL, graph databases (read 20261102 19:54 UTC)
20. https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/ : Dean and Ghemawat, OSDI 2004 (read 20261102 19:55 UTC)
21. https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/ : Chang et al., OSDI 2006 (read 20261102 19:55 UTC)
22. https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store : DeCandia et al., 2007 (read 20261102 19:55 UTC)
23. https://www.infoq.com/news/2010/02/neo4j-10 : InfoQ, 25 February 2010, Neo4j 1.0 (read 20261102 19:55 UTC)
24. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, 2012; learning to rank, query logs, TREC QA (read 20261102 19:54 UTC)
25. https://arxiv.org/pdf/2010.06467 : Lin, Nogueira, Yates, section 1.2.3; learning to rank "zenith" (read 20261102 19:54 UTC)
26. https://trec.nist.gov/data/qamain.html : TREC QA track data list, TREC-8 (1999) to 2007, then Live QA 2015 to 2017 (read 20261102 20:10 UTC)
27. https://www.ibm.com/history/watson-jeopardy : IBM history page; February 2011 match, DeepQA (first-party; read 20261102 19:58 UTC)
28. https://users.dcc.uchile.cl/~cgutierr/papers/surveyGDB.pdf : Angles and Gutierrez, ACM Computing Surveys 2008, abstract (read 20261102 19:58 UTC)
29. https://www.w3.org/TR/rdf11-concepts/ : RDF 1.1 Concepts, Recommendation 25 February 2014 (read 20261102 19:59 UTC)
30. https://www.w3.org/TR/rdf12-concepts/ : RDF 1.2 Concepts, Candidate Recommendation Snapshot 07 April 2026, "not expected to advance to Recommendation any earlier than 05 May 2026" (read 20261102 20:10 UTC)
31. https://www.w3.org/TR/sparql11-query/ : SPARQL 1.1 Query, Recommendation 21 March 2013 (read 20261102 19:59 UTC)
32. https://www.w3.org/TR/sparql12-query/ : SPARQL 1.2 Query, Working Draft 01 November 2026 (read 20261102 20:11 UTC)
33. https://www.w3.org/TR/shacl12-core/ : SHACL 1.2 Core, Working Draft 02 November 2026 (read 20261102 20:11 UTC)
34. https://schema.org/docs/about.html : schema.org About; founding companies Google, Microsoft, Yahoo and Yandex (first-party; read 20261102 19:55 UTC)
35. https://cyc.com/ : Cycorp home page, products on the Cyc platform (first-party; read 20261102 19:55 UTC)
36. https://blog.wikimedia.de/en/2022/10/27/wikidata-birthday-interview/ : Wikimedia Deutschland blog (first-party): "Wikidata was launched on October 29, 2012" (read 20261102 22:53 UTC)
37. https://en.wikipedia.org/wiki/Wikipedia:Wikipedia_Signpost/2012-10-29/Technology_report : Signpost technology report dated 29 October 2012: Wikidata.org "launched this week" (read 20261102 22:53 UTC)
38. https://papers.baulab.info/papers/knowledge/Lenat-1995.pdf : Lenat, CACM 38(11), 1995: "Since 1984, a person-century of effort has gone into building CYC" (read 20261102 22:56 UTC, text extracted from the PDF)
39. https://cyc.com/?p=8999 : "About Cycorp" (first-party): Lenat "founded the Cyc Project in 1984" at MCC (read 20261102 22:56 UTC, WebFetch extraction)
