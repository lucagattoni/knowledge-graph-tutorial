---
type: era
period: 2012-2017
order: 6
updated: 20261102 23:11 UTC
---

# Knowledge graphs at scale

This page answers: how did "[knowledge graph](../index/knowledge-graph.md)" go from a [Semantic Web](../index/semantic-web.md) topic to a product term, and which parts of that are settled? The previous era is [The semantic web and linked data](semantic-web.md); the next is [Language models meet retrieval](language-models-meet-retrieval.md). See also the [chapter overview](README.md).

## Dates and boundaries

**The scheme is this documentation's.** No source read gives one periodisation for all four threads; the boundaries are points that at least two sources share. The name is ours too: Gutierrez and Sequeda's last period is headed "Data and Knowledge at Large Scale"; its text opens "The 2000s saw the explosion of e-commerce" and does not treat 2012 as a boundary [4].

**Start, 20120516.** Google announced its [Knowledge Graph](../index/google-knowledge-graph.md) that day: "things, not strings" [1]. Hogan et al. split their history at 2012 and, citing Bergman, call the announcement "a watershed moment" for the phrase [2]. Hitzler's section 2.3 opens "In 2012, a new term appeared on the scene", while his second phase "stretches into the early 2010s" [3]. Gutierrez and Sequeda record the event but keep it inside their last period [4].

**End, 2017.** BERT "arrived on the scene in October 2018" (arXiv, 20181011), was first applied to text ranking in January 2019, and the TREC 2019 Deep Learning Track separated "two different 'eras'" [5][22]. Pan et al. list REALM and RAG (2020) after KGLM (2019) as retrieval-augmented fusion [6]; Gao et al. say RAG's inception "coincided with the rise of the Transformer architecture" [7]. *Reading:* only Lin et al. use BERT as a divide, and no source ends the knowledge-graph thread in 2017: Hitzler's third phase "was and is still driven by knowledge graphs" [3]. This end is set by the retrieval and language-model threads. The Transformer paper (20170612) falls inside the era; 2017 against 2018 is a one-year choice.

## What changed

A Semantic Web idea became a product term: companies built large graphs of entities and relations [2][3]. The W3C stack gained revisions ([OWL](../index/owl.md) 2, [SPARQL](../index/sparql.md) 1.1, [RDF](../index/rdf.md) 1.1) and two additions ([JSON-LD](../index/json-ld.md), [SHACL](../index/shacl.md)) [8][9][10][11][12], while [Linked Data](../index/linked-data.md)'s hype gave way to "a more sober perspective" [3]. In databases, Stonebraker and Pavlo date the "Big Data" era to the early 2010s, say the Hadoop market "cratered in the 2010s", and say that by the end of the 2010s almost every [NoSQL](../index/nosql.md) system had added a [SQL](../index/sql.md) interface [25]. In search, neural ranking models that learn vector representations followed [learning to rank](../index/learning-to-rank.md) [5].

## The threads

### KB/KG

- **The term and the product.** At launch the graph held "more than 500 million objects" and "more than 3.5 billion facts", rooted in [Freebase](../index/freebase.md), Wikipedia and the CIA World Factbook (first-party figures, Google's own post) [1]. Hogan et al. list later announcements by Amazon, eBay, Facebook and others, dates unstated there [2]. They write that mentions of the term in the research literature "quickly gained momentum" [2]; Gutierrez and Sequeda say old ideas "achieved worldwide popularity" [4]. The definition is another matter: Hogan et al. (2021) call it something that "remains contentious" [2].
- **Open graphs.** Freebase, bought by Google in 2010, became read-only in March 2015 and "Much of this content was subsequently migrated to Wikidata" [2]; Google's page says the API is shut down [17]. [Wikidata](../index/wikidata.md) was launched on 29 October 2012 (Wikimedia Deutschland, first-party [30]; the Wikipedia Signpost of that day says it "launched this week" [31]; Hitzler gives the year only [3]) and had over 66 million items in 2020 [3]; its statistics page showed 123,865,222 on 20261102 [18]. [DBpedia](../index/dbpedia.md)'s April 2016 release had about 6 million entities and 9.5 billion triples [3].
- **Automatic construction and embeddings.** NELL (from 2010), TransE (NIPS 2013) and Knowledge Vault (KDD, August 2014) date from this era [2][19][20]. Whether they are settled is **unstated**; see [knowledge graph embedding](../index/knowledge-graph-embedding.md) and the [trends](../trends/README.md).
- **Enterprise graphs.** Hogan et al., summarising Noy et al.: many sources, millions or billions of edges, "lightweight" [ontologies](../index/ontology.md) [2].

### Ontologies and the semantic web

- **Linked Data cools.** In the early 2010s "shallow non-expressive schemas" appeared "a major obstacle to reuseability" [3]. schema.org (2011) had annotations on over 30% of pages in a 2015 report [3].
- **The standards are revised.** OWL 2 Second Edition 20121211 [8], SPARQL 1.1 20130321 [9], RDF 1.1 20140225 [10], JSON-LD 1.0 20140116 [11] and SHACL 20170720 [12]. The Semantic Web Activity was "subsumed, in December 2013, by the W3C Data Activity" [13]. The 2026 drafts of RDF 1.2, SPARQL 1.2 and SHACL 1.2 still name RDF 1.1, SPARQL 1.1 and SHACL as the "Latest Recommendation" [14][15][16]; JSON-LD 1.0 has a successor [11]. The drafts themselves are still moving: see [trends](../trends/README.md).

### Databases and search

- **Big Data and NoSQL.** The SQL standard added JSON in 2016 [25]. Gutierrez and Sequeda say NoSQL "(re-)popularized" column, document, key-value and graph models [4].
- **Property graphs.** [Neo4j](../projects/neo4j.md) 2.0 "shipped with the brand-new Cypher query language", and openCypher was announced in 2015, both per Neo4j's own account [26]. The first release date of [Cypher](../index/cypher.md) is **unstated** in the sources read. openCypher now says it evolves toward ISO/IEC 39075 [GQL](../index/gql.md) [27]; see [What has settled since 2023](settled-since-2023.md).
- **Ranking.** Learning to rank "reached its zenith in the early 2010s"; DSSM (2013) was among the earliest neural ranking models, and continuous vectors "freed text retrieval from the bounds of exact term matching" [5].

### RAG and agent memory

- The [Transformer](../index/transformer.md) (20170612) is "based solely on attention mechanisms"; [BERT](../index/bert.md) stands for "Bidirectional Encoder Representations from Transformers" [21][22]. DrQA (20170331) answered questions from Wikipedia alone, combining document retrieval with reading comprehension [24]; its later status is **unstated**.
- No agent-memory work belongs here: Hu et al. date works calling themselves "LLM memory mechanisms" to 2023 and later [29]. Both threads are still moving: see [trends](../trends/README.md).

## Dated events

| Date | Event | Thread | Source |
|---|---|---|---|
| 20120516 | Google announces its Knowledge Graph | KB/KG | [1][2] |
| 20121029 | Wikidata launched (Wikimedia Deutschland, first-party) | KB/KG | [30][31] |
| 20121211 | OWL 2 Second Edition (first edition 20091027) | Ontologies | [8] |
| 2013 | DSSM; Neo4j 2.0 (Neo4j's account: with Cypher) | Databases and search | [5][26] |
| 20130321 | SPARQL 1.1 | Ontologies | [9] |
| 201312 | Semantic Web Activity subsumed by Data Activity | Ontologies | [13] |
| 20140116 | JSON-LD 1.0 | Ontologies | [11] |
| 20140225 | RDF 1.1 | Ontologies | [10] |
| 201503 | Freebase read-only | KB/KG | [2] |
| 2015 | openCypher announced (Neo4j's account) | Databases and search | [26] |
| 20161212 | ConceptNet 5.5 (arXiv v1) | KB/KG | [23] |
| 20170331 | DrQA (arXiv v1) | RAG and memory | [24] |
| 20170612 | Transformer (arXiv v1) | RAG and memory | [21] |
| 20170720 | SHACL | Ontologies | [12] |

## Systems and projects

- [YAGO](../index/yago.md) extracts from Wikipedia and unifies with [WordNet](../index/wordnet.md) concepts [2].
- [Cyc](../index/cyc.md): proprietary; begun in 1984 on Lenat's and Cycorp's accounts [32][33]; as of Hogan et al. (2021), over 900 person-years of effort (they write "since 1986"), 2.2 million facts and rules [2]. [ConceptNet](../index/conceptnet.md) 5.5: an open multilingual graph of words and phrases [23].
- Neo4j: the [property-graph](../index/property-graph.md) database behind Cypher [26].

## Ideas and disputes

1. **New idea or reframing?** Hitzler: "mostly a new framing of ideas coming rather directly out of the Semantic Web field" [3]. Gutierrez and Sequeda: "a reincarnation of the Semantic Web, and Linked Data" [4]. Hogan et al. adopt an inclusive definition needing no ontology or reasoner and say open graphs came from that community "or would later adopt its standards" [2]. Hitzler adds real differences: industry-led, not open [3]. (Gutierrez and Sequeda and Hogan et al. share authors: not independent.)
2. **Did ontologies work?** Hitzler: ontologies "turned out to be often hard to maintain and re-use" [3]. Gutierrez and Sequeda: [description logics](../index/description-logic.md) "would become the underpinning to OWL" [4]; Hitzler says SNOMED CT is "fully formalized in OWL" [3]. In this era the graphs use lightweight schemas [2].
3. **Fate of graph databases.** Angles and Gutierrez (2008): their influence died out, then "the need to manage information with graph-like nature has reestablished the relevance of this area" [28]. Stonebraker and Pavlo (2024), writing for the relational model: "We do not expect specialized graph DBMSs to be a large market" [25].
4. **Sparse or dense?** Stonebraker and Pavlo: inverted-index search has been "supplanted" by similarity search with ML-generated embeddings ([vector search](../index/vector-search.md)) [25]. Lin et al.: [BM25](../index/bm25.md) "still provides the starting point of many text ranking approaches today" [5]. The dispute belongs mostly to the next era.
5. **First use of "knowledge graph".** 1972 in the introduction of Hogan et al., 1973 (Schneider) in their appendix; Bakker's thesis (1987 in Hogan et al.'s appendix) is "the first systematic study with the term" in Gutierrez and Sequeda [2][4]. The modern meaning "stems from" 2012 [2].

## Papers and standards

See [Foundations](../papers/foundations.md) and the [papers chapter](../papers/README.md).

- Bordes et al., TransE (2013) [19]; Dong et al., Knowledge Vault (2014) [20]: named above, status unstated.
- Speer et al., ConceptNet 5.5 (2016); Chen et al., DrQA (2017); Vaswani et al., Transformer (2017) [23][24][21].
- The W3C Recommendations are in the Ontologies thread above.

## Left unsolved

- **No agreed definition** as of Hogan et al. (2021) and Hitzler (2020) [2][3].
- **Cost and openness.** Graphs are "difficult to construct and evolve by nature" [6]; showcases are "not really open" [3].
- **Logic and statistics.** On integrating the two, "little is yet known" [4].
- **Facts in language models.** [Large language models](../index/large-language-model.md) "often fall short of capturing and accessing factual knowledge" [6]: the next era's question, after BERT and the Transformer.

## Sources

1. https://blog.google/products/search/introducing-knowledge-graph-things-not/ : Singhal, Google, 20120516: "things, not strings", 500 million objects, 3.5 billion facts, sources (read 20261102 19:54 UTC)
2. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", Appendix A.2-A.3, sections 10.1-10.2: 2012 split, "watershed moment", "quickly gained momentum", Freebase, Cyc, NELL, enterprise trends, contentious definition, first uses incl. Bakker 1987 (read 20261102 20:11 UTC)
3. https://par.nsf.gov/servlets/purl/10292869 : Hitzler, Semantic Web review (author's version, April 2020; CACM 64(2), 2021): phases, section 2.3 "In 2012", Linked Data phase, schema.org, Wikidata, differences, DBpedia release (read 20261102 20:11 UTC)
4. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, CACM 64(3), 2021: "Data and Knowledge at Large Scale" period, NoSQL, "worldwide popularity", Bakker, description logics (read 20261102 20:11 UTC)
5. https://arxiv.org/pdf/2010.06467 : Lin, Nogueira, Yates, sections 1.2.3-1.2.5: learning to rank, DSSM, BERT October 2018, two "eras", BM25 (read 20261102 19:54 UTC)
6. https://arxiv.org/pdf/2306.08302 : Pan et al., LLM and KG roadmap: KGLM, REALM, RAG as retrieval-augmented fusion; abstract (read 20261102 19:57 UTC)
7. https://arxiv.org/pdf/2312.10997 : Gao et al., RAG survey: inception and the Transformer (read 20261102 19:54 UTC)
8. https://www.w3.org/TR/owl2-overview/ : OWL 2 Overview, Second Edition, 11 December 2012; changes since 27 October 2009 (read 20261102 19:55 UTC)
9. https://www.w3.org/TR/sparql11-query/ : SPARQL 1.1 Query, Recommendation 21 March 2013 (read 20261102 19:55 UTC)
10. https://www.w3.org/TR/rdf11-concepts/ : RDF 1.1 Concepts, Recommendation 25 February 2014 (read 20261102 19:55 UTC)
11. https://www.w3.org/TR/2014/REC-json-ld-20140116/ : JSON-LD 1.0, Recommendation 16 January 2014, superseded 03 November 2020 (read 20261102 19:55 UTC)
12. https://www.w3.org/TR/shacl/ : SHACL, Recommendation 20 July 2017 (read 20261102 19:55 UTC)
13. https://www.w3.org/2001/sw/ : Semantic Web Activity subsumed by the Data Activity, December 2013 (read 20261102 19:55 UTC)
14. https://www.w3.org/TR/rdf12-concepts/ : RDF 1.2, Candidate Recommendation Snapshot 07 April 2026; "Latest Recommendation" RDF 1.1 (read 20261102 19:55 UTC)
15. https://www.w3.org/TR/sparql12-query/ : SPARQL 1.2, Working Draft 01 November 2026; "Latest Recommendation" SPARQL 1.1 (read 20261102 19:55 UTC)
16. https://www.w3.org/TR/shacl12-core/ : SHACL 1.2 Core, Working Draft 02 November 2026; "Latest Recommendation" SHACL 2017 (read 20261102 19:55 UTC)
17. https://developers.google.com/freebase : Freebase API shut down; project ran 2007 to 2015 (read 20261102 19:55 UTC)
18. https://www.wikidata.org/wiki/Wikidata:Statistics : 123,865,222 items at the read (read 20261102 19:56 UTC)
19. https://papers.nips.cc/paper_files/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html : Bordes et al., TransE, NIPS 2013 abstract (read 20261102 20:11 UTC)
20. https://research.google/pubs/knowledge-vault-a-web-scale-approach-to-probabilistic-knowledge-fusion/ : Dong et al., KDD 2014, 24-27 August 2014, abstract (read 20261102 19:55 UTC)
21. https://arxiv.org/abs/1706.03762v1 : Vaswani et al., "Attention Is All You Need", submitted 12 June 2017, abstract (read 20261102 20:13 UTC)
22. https://arxiv.org/abs/1810.04805v1 : Devlin et al., BERT, submitted 11 October 2018, abstract (read 20261102 20:13 UTC)
23. https://arxiv.org/abs/1612.03975v1 : Speer et al., ConceptNet 5.5, submitted 12 December 2016, abstract (read 20261102 20:13 UTC)
24. https://arxiv.org/abs/1704.00051v1 : Chen et al., DrQA, submitted 31 March 2017, abstract (read 20261102 20:13 UTC)
25. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 2024: "Big Data" era, Hadoop, NoSQL and SQL, JSON 2016, graph databases, embeddings (read 20261102 20:11 UTC)
26. https://neo4j.com/blog/news/neo4j-top-10-biggest-moments-of-2010s/ : Neo4j (vendor): Neo4j 2.0 "shipped with the brand-new Cypher query language" 2013, openCypher 2015 (read 20261102 20:11 UTC)
27. https://opencypher.org/ : openCypher evolves toward ISO/IEC 39075 GQL (read 20261102 19:55 UTC)
28. https://users.dcc.uchile.cl/~cgutierr/papers/surveyGDB.pdf : Angles and Gutierrez, ACM Computing Surveys 40(1), 2008, abstract (read 20261102 19:54 UTC)
29. https://arxiv.org/pdf/2512.13564 : Hu et al., "Memory in the Age of AI Agents", section 2.3.1 (read 20261102 19:59 UTC)
30. https://blog.wikimedia.de/en/2022/10/27/wikidata-birthday-interview/ : Wikimedia Deutschland blog (first-party): "Wikidata was launched on October 29, 2012" (read 20261102 22:53 UTC)
31. https://en.wikipedia.org/wiki/Wikipedia:Wikipedia_Signpost/2012-10-29/Technology_report : Signpost technology report dated 29 October 2012: Wikidata.org "launched this week" (read 20261102 22:53 UTC)
32. https://papers.baulab.info/papers/knowledge/Lenat-1995.pdf : Lenat, CACM 38(11), 1995: "Since 1984, a person-century of effort has gone into building CYC" (read 20261102 22:56 UTC, text extracted from the PDF)
33. https://cyc.com/?p=8999 : "About Cycorp" (first-party): Lenat "founded the Cyc Project in 1984" at MCC (read 20261102 22:56 UTC, WebFetch extraction)
