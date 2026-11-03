---
type: era
period: 1993-2000
order: 4
updated: 20261102 23:11 UTC
---

# The Web changes data and search

This page answers: what did the arrival of the Web change for knowledge, data and search, and which of those changes became standards or common practice? The previous era is [Knowledge systems: boom and bust](knowledge-systems.md); the next is [The semantic web and linked data](semantic-web.md). Only settled outcomes are told here; what is still moving gets one line and a link to [the trends](../trends/README.md).

## Dates and boundaries

**The scheme is this documentation's.** No source gives one periodisation for all four threads. The boundaries are points that at least two sources share, and Gutierrez and Sequeda call their own boundaries "blurry" [1].

**Start, 1993.** Sanderson and Croft count about 100 web sites in mid-1993 and over four times as many six months later; "Web search engines started to emerge in late 1993 to cope with this growth" [2]. Gutierrez and Sequeda give a period "The 1990s", opened by the Web [1]. Stonebraker and Pavlo date the [semi-structured data](../index/semi-structured-data.md) movement ([XML](../index/xml.md)) to the "late 1990s and 2000s" [4]. The first [RDF](../index/rdf.md) working draft is dated 19971002 [3][8]. 1993 is the earliest point and the only one with a dated reason for search. [TREC](../index/trec.md) began in 1992 and is on the previous page [15].

**End, 2000.** Hitzler writes that the *Scientific American* article of 2001 "arguably marks the birth of the field", and that naming any such point "is of course debateable at best" [3]. The article is dated 20010501 [18]. Gutierrez and Sequeda put the [Semantic Web](../index/semantic-web.md) in their next period, "The 2000s" [1], and Sowa cites the article when he calls the Semantic Web "a large semantic network" [19]. Hitzler starts "from the early 2000s" and treats the 1997 RDF draft as earlier [3]; this page keeps the RDF work of 1997 to 1999 because it opens the standards. So the era ends in 2000.

## What changed

Before the Web, people searched collections "selected and edited from authoritative sources", and almost all commercial systems used Boolean queries until the early to mid 1990s [2]. The Web was unedited, so [search engines](../index/web-search-engine.md) had to crawl it, rank pages by text and by links, and resist spam [2]. Data practice moved with it: the [relational](../index/relational-model.md) database stayed the workhorse and now served e-commerce, while the Web created a need for self-describing, semi-structured data (OEM, XML, RDF) [1]. Knowledge work turned from closed [knowledge bases](../index/knowledge-base.md) to vocabularies shared on the Web: [ontologies](../index/ontology.md) and the first W3C metadata standards [1][3].

## The threads

### KB/KG

The [expert-system](../index/expert-system.md) line ended inside mainstream software: its experience was rolled into tools from IBM, SAP and Oracle [1]. The remaining bottleneck, the [acquisition of knowledge](../index/knowledge-acquisition-bottleneck.md), grew into knowledge and ontology engineering [1].

Two large hand-built resources continue. [Cyc](../index/cyc.md), begun in 1984 [24][25], left MCC and became Cycorp, Inc. at the end of 1994 (first-party) [25]. In November 1995 Lenat reported "a person-century of effort", a schema of roughly 10^5 general concepts and approximately 10^6 hand-entered commonsense axioms [24]. The survey of Hogan et al. (2021) gives today's total, not the state in 2000: over 900 person-years of effort "since 1986" and 2.2 million facts and rules [6]; the two start years are compared in [knowledge systems](knowledge-systems.md). [WordNet](../index/wordnet.md), begun in 1985 at Princeton, groups English nouns, verbs and adjectives into synonym sets joined by relations; its report on the state of 1990 was revised in 199308 [17]. The phrase "[knowledge graph](../index/knowledge-graph.md)" appears in several unrelated senses (De Raedt et al. 1990, Dieng et al. 1992, Shimony et al. 1997), and graphs from 1970 to 2000 "tend to have worked with small graphs" [6].

### Ontologies and the semantic web

Gruber's paper of 1993 defines an ontology as "an explicit specification of a conceptualization" and describes Ontolingua, which translates shared definitions into frame-based and relational systems [12]. Methodologies (CommonKADS), tools (WebODE, Protege) and Web-oriented efforts (SHOE, Ontobroker, KQML, OIL, DAML, OntoWeb) followed [1]. The DAML Program ran from 2000 to 2006 [3] and builds on XML and RDF [22]. The Gene Ontology began in 1998 [3].

The standards came from W3C. The first RDF working draft is dated 19971002 [8]. XML 1.0 became a Recommendation on 19980210 [9]. *RDF Model and Syntax* followed on 19990222 and calls RDF "a foundation for processing metadata" [10]. The 2004 RDF 1.0 documents were "intended to jointly replace" it and the 2000 [RDF Schema](../index/rdfs.md) candidate [11]; RDF 1.1 followed on 20140225 [23]. The semantic web as a named project begins in the next era.

### Databases and search

*Search.* Ranked retrieval had beaten Boolean search in many experiments over earlier decades [2]. The first crawler for web search was JumpStation (late 1993); WebCrawler (1994) was the first full-text engine to use one [2]. The [BM25](../index/bm25.md) function (Okapi, 1994) "still provides the starting point of many text ranking approaches today", wrote Lin et al. in 2021 [5]. Link analysis arrived with anchor text, [PageRank](../index/pagerank.md) and HITS [2]. Brin and Page described a Google prototype over at least 24 million pages and noted that "very little academic research has been done on them" [13]. NIST reports that retrieval effectiveness "approximately doubled in the first six years" of TREC [15].

*Data.* Enterprises began building [data warehouses](../index/data-warehouse.md) from the mid-1990s [4]; research added data integration, OLAP and data mining [1]. The relational model, extended with types, "has dominated all comers" [4]. XML databases had "buzz" in the late 1990s but did not displace it; JSON later overtook XML for web data exchange [4].

### RAG and agent memory

No event of this era is retrieval-augmented generation or [agent memory](../index/agent-memory.md): the sources read mention neither (**unstated**). The precursor is [question answering](../index/question-answering.md): TREC introduced open-domain question answering [15] (TREC-8 data, 1999 [16]), and Sanderson and Croft trace later work on natural-language questions to that task [2]. Gao et al. write that retrieval-augmented generation's inception "coincided with the rise of the Transformer architecture" [21]; that is [Language models meet retrieval](language-models-meet-retrieval.md).

## Dated events

| Date | Event | Thread | Source |
|---|---|---|---|
| 1993 | Gruber: ontology as "explicit specification of a conceptualization" (*Knowledge Acquisition* 5(2); report revised 199304) | Ontologies | [12] |
| late 1993 | JumpStation, first crawler for web search | Databases and search | [2] |
| 1994 | WebCrawler, first full-text engine with a crawler | Databases and search | [2] |
| 1994 | Okapi BM25 (*Okapi at TREC-3*) | Databases and search | [5] |
| end of 1994 | Cyc project spins out of MCC and becomes Cycorp, Inc. (first-party; the day is unstated) | KB/KG | [25] |
| 199511 | Lenat reports Cyc's size: about 10^5 concepts and 10^6 axioms (*CACM* 38(11)) | KB/KG | [24] |
| 19971002 | First RDF working draft | Ontologies | [8] |
| 19980210 | XML 1.0, W3C Recommendation | Ontologies, Databases and search | [9] |
| 1998 | Brin and Page: Google prototype and PageRank | Databases and search | [13] |
| 19990222 | RDF Model and Syntax, W3C Recommendation | Ontologies | [10] |
| 1999 | Kleinberg, HITS (journal year per [2]; preliminary versions: IBM report 199705, SODA 1998) | Databases and search | [14][2] |
| 1999 | TREC-8 question answering data | RAG and memory (precursor) | [16] |

## Systems and projects

Search: JumpStation, WebCrawler, Google prototype, Okapi [2][5][13]. Knowledge: Cyc, WordNet, Ontolingua [6][12][17][24]. No project of the projects chapter dates from this era.

## Ideas and disputes

| Question | One view | Other view | Reading |
|---|---|---|---|
| RDF's first standard | 1999: *RDF Model and Syntax*, a Recommendation [10] | "Also in 2004" RDF became a W3C standard [3] | *Reading:* both are true of different documents; the 2004 set was meant to replace the 1999 one [11]. |
| The ontology definition | 1993 paper: "explicit specification of a conceptualization" [12] | "formal, explicit specification of a shared conceptualization", from "a many-cited source from 1993" [3]; "shared and formal", citing Gruber 1995 [1] | *Reading:* the 1993 sentence has neither "formal" nor "shared"; where those words come from is **unstated** (the 1995 paper was not read). |
| Graph databases | Graph models "took off in the eighties and early nineties", faded with semistructured and XML models, and regained relevance [7] | "We do not expect specialized graph DBMSs to be a large market" [4] | *Reading:* one 2008 survey and one 2024 forecast; both look past this era. |
| Dense against sparse retrieval | Inverted-index search "supplanted in recent years" by embedding similarity search [4] | BM25 is still the starting point [5]; [hybrid search](../index/hybrid-search.md) mixes both [21] | *Reading:* the 1990s ranking functions survive; "replaced" rests on one source. |
| "Knowledge graph" before 2012 | Used in several senses since the 1940s, including the 1990s [6] | "did not permeate widely" until the 2010s [1] | *Reading:* compatible; the 1990s uses are not a line to the modern meaning. |

Whether ontologies "worked" is on [the next page](semantic-web.md).

## Papers and standards

See the papers chapter: [foundations](../papers/foundations.md).

- Gruber 1993, *A translation approach to portable ontology specifications* [12].
- Robertson et al. 1994, *Okapi at TREC-3*, TREC-3 proceedings (via [5]).
- Brin and Page 1998, *The anatomy of a large-scale hypertextual Web search engine* [13].
- Kleinberg 1999, *Authoritative sources in a hyperlinked environment*, J. ACM 46(5) [14][2].
- Voorhees 2001, *The TREC question answering track*, Natural Language Engineering 7(4) (via [2]).
- XML 1.0, 19980210 [9]; RDF Model and Syntax, 19990222 [10].
- Still moving: RDF 1.2 is a W3C Candidate Recommendation Snapshot of 20260407 [20]; see [the trends](../trends/README.md).

## Left unsolved

Computing power was not enough for the new volume of Web data, and "pure logical techniques have complexity bounds" that made scaling hard [1]. Page ranking had to be defended against spam [2]. RDF had no standard schema or ontology language in 1999: RDF Schema was only a 2000 Candidate Recommendation [11], and [OWL](../index/owl.md) came in 2004 [1]. Question answering over text was an evaluation track, not a product [15]. The next era takes these up as [the semantic web](semantic-web.md).

## Sources

All pages read in full or in the parts cited. Downloaded files were handled as untrusted data.

1. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: period "The 1990s", semi-structured data, ontology engineering, expert systems absorbed, Gruber 1995 reference (read 20261102 19:55 UTC)
2. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE 2012: web growth 1993, search engines, Boolean until mid 1990s, PageRank and HITS references, TREC question answering (read 20261102 19:55 UTC)
3. https://par.nsf.gov/servlets/purl/10292869 : Hitzler, "A Review of the Semantic Web Field", CACM 64(2), 2021: 2001 article as birth, RDF draft 1997, DAML 2000-2006, Gene Ontology 1998, "Also in 2004" (read 20261102 19:55 UTC)
4. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), 2024: data-model list, XML databases, data warehouses from mid-1990s, graph and text-search stances (read 20261102 19:55 UTC)
5. https://arxiv.org/pdf/2010.06467 : Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking", section 1.2.2: Okapi BM25 (read 20261102 19:55 UTC)
6. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", Appendix A and section 10: knowledge-graph usages 1990-1999, Cyc "since 1986", 900 person-years, 2.2 million facts and rules as of the 2021 text (read 20261102 20:15 UTC)
7. https://users.dcc.uchile.cl/~cgutierr/papers/surveyGDB.pdf : Angles and Gutierrez, "Survey of Graph Database Models", abstract (read 20261102 19:55 UTC)
8. https://www.w3.org/TR/WD-rdf-syntax-971002/ : RDF Model and Syntax, working draft, version 1, 19971002 (read 20261102 19:58 UTC)
9. https://www.w3.org/TR/1998/REC-xml-19980210 : XML 1.0, W3C Recommendation 19980210 (read 20261102 19:55 UTC)
10. https://www.w3.org/TR/1999/REC-rdf-syntax-19990222/ : RDF Model and Syntax, W3C Recommendation 19990222 (read 20261102 19:55 UTC)
11. https://www.w3.org/TR/rdf10-concepts/ : RDF 1.0 Concepts, W3C Recommendation 20040210: "intended to jointly replace" RDF Model and Syntax (1999) and RDF Schema (2000 Candidate Recommendation) (read 20261102 19:55 UTC)
12. https://tomgruber.org/writing/ontolingua-kaj-1993.pdf : Gruber, "A Translation Approach to Portable Ontology Specifications", KSL 92-71 revised 199304, Knowledge Acquisition 5(2):199-220, 1993 (read 20261102 19:58 UTC)
13. https://snap.stanford.edu/class/cs224w-readings/Brin98Anatomy.pdf : Brin and Page, Computer Networks and ISDN Systems 30 (1998) 107-117: Google prototype, 24 million pages, PageRank (read 20261102 20:00 UTC)
14. https://doi.org/10.1145/324133.324140 : Kleinberg, "Authoritative Sources in a Hyperlinked Environment", J. ACM 46(5), 1999 (the paper's record). The note on its preliminary versions is read from the first page of the author's copy on his Cornell web page: "Preliminary versions of this paper appear in the Proceedings of the ACM-SIAM Symposium on Discrete Algorithms, 1998, and as IBM Research Report RJ 10076, May 1997" (author's copy read 20261102 20:14 UTC; the DOI page refuses automated reads, so the publisher's page was not read)
15. https://trec.nist.gov/overview.html : NIST, TREC overview: started 1992, effectiveness doubled in six years, open-domain question answering (read 20261102 19:58 UTC)
16. https://trec.nist.gov/data/qamain.html : NIST, TREC QA track data list: "TREC-8 (1999) Question Answering Data" (read 20261102 20:00 UTC)
17. https://wordnetcode.princeton.edu/5papers.pdf : Miller et al., "Introduction to WordNet: An On-line Lexical Database", revised 199308: started 1985, state as of 1990 (read 20261102 20:00 UTC)
18. https://www.scientificamerican.com/article/the-semantic-web/ : Berners-Lee, Hendler, Lassila, "The Semantic Web", Scientific American 284(5), dated 20010501 (read 20261102 20:02 UTC)
19. https://www.jfsowa.com/pubs/semnet.htm : Sowa, "Semantic Networks": the Semantic Web as a large semantic network, citing the 2001 article (read 20261102 20:02 UTC)
20. https://www.w3.org/TR/rdf12-concepts/ : RDF 1.2 Concepts, W3C Candidate Recommendation Snapshot 20260407; latest Recommendation is RDF 1.1 (read 20261102 20:01 UTC)
21. https://arxiv.org/pdf/2312.10997 : Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey": RAG's inception and the Transformer; hybrid retrieval (read 20261102 20:01 UTC)
22. http://www.daml.org/about.html : About DAML: the language is an extension of XML and RDF (read 20261102 19:58 UTC)
23. https://www.w3.org/TR/rdf11-concepts/ : RDF 1.1 Concepts, W3C Recommendation 20140225 (read 20261102 20:01 UTC)
24. https://papers.baulab.info/papers/knowledge/Lenat-1995.pdf : Lenat, "CYC: A Large-Scale Investment in Knowledge Infrastructure", CACM 38(11), November 1995: "Since 1984, a person-century of effort", roughly 10^5 general concepts, approximately 10^6 hand-entered commonsense axioms (read 20261102 22:56 UTC, text extracted from the PDF)
25. https://cyc.com/?p=8999 : "About Cycorp" (first-party): founded at MCC in 1984; "At the end of 1994, the Cyc project spun out of MCC, becoming Cycorp, Inc." (read 20261102 22:56 UTC, WebFetch extraction)
