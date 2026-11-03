# Candidate fundamental papers: ontologies, the semantic web, linked data, web-scale knowledge bases, link analysis, graph databases (1990 to 2011, plus two later system papers)

Researcher area: ontology definitions and engineering; the semantic web vision; RDF, RDFS, OWL and SPARQL as standards; linked data; WordNet, ConceptNet, DBpedia, YAGO, Freebase, NELL; PageRank and web-scale search; early graph databases and the property-graph model.
Written 20261102 (UTC). All times below are UTC, read from the clock.

## How the counts were obtained (read this first)

- Semantic Scholar Graph API returned HTTP 429 on every call (first background batch from 19:44; direct tests at 19:58 and 20:05). No Semantic Scholar count is used. [3]
- OpenAlex answered once (Gruber 1993, 12,781) and then reported the free daily budget used up for this network (HTTP 429, "$0 remaining"). Getting an OpenAlex key needs the owner's e-mail address sent to a third party, so I did not. [2]
- **Crossref `is-referenced-by-count`** is the main source: read 20261102 19:59 (title searches) and 20:00 (DOI lookups). It counts only citations from works whose reference lists Crossref holds, so it is a **lower bound** and sits well below Google Scholar or OpenAlex figures (Gruber 1993: Crossref 8,595 against OpenAlex 12,781). Use the numbers to rank within this file, not to quote as "total citations". [1]
- Where a paper has no DOI (W3C documents, technical reports, Banko 2007 IJCAI) the count is **unstated**.
- Where a paper has both a conference/arXiv version and a journal version, the count is for the DOI version named in the entry.

## Candidate list (strongest first)

| # | Short name and year | Tests | Crossref count (read 20261102) |
|---|---|---|---|
| 1 | Gruber 1993, ontology specifications | origin, widely-built-on | 8,595 |
| 2 | WordNet 1990 (Miller et al.) | origin, widely-built-on | 2,249 (1990 paper); 9,187 (1995 CACM overview) |
| 3 | Berners-Lee, Hendler, Lassila 2001, The Semantic Web | origin, widely-built-on | 8,727 |
| 4 | Brin and Page 1998, Google | origin, widely-built-on | 9,354 |
| 5 | Kleinberg 1999, HITS | origin, widely-built-on | 5,838 |
| 6 | Gruber 1995, design principles | widely-built-on, origin | 3,937 |
| 7 | Freebase 2008 | origin, widely-built-on | 3,284 |
| 8 | Bizer, Heath, Berners-Lee 2009, Linked Data | survey-of-record, widely-built-on | 2,525 |
| 9 | YAGO 2007 | origin, widely-built-on | 2,509 |
| 10 | DBpedia 2007 (Auer et al.) | origin, widely-built-on | 2,448 |
| 11 | Uschold and Gruninger 1996 | survey-of-record, widely-built-on | 2,241 |
| 12 | Lehmann et al. 2015, DBpedia | widely-built-on, survey-of-record | 1,893 |
| 13 | ConceptNet 5.5 (2017) | widely-built-on | 1,386 |
| 14 | Horrocks, Patel-Schneider, van Harmelen 2003, OWL | origin, turning-point | 894 |
| 15 | NELL 2010 (Carlson et al.) | origin | 783 |
| 16 | Pérez, Arenas, Gutierrez 2009, SPARQL semantics | origin, widely-built-on | 764 |
| 17 | Angles and Gutierrez 2008, graph database models | survey-of-record | 749 |
| 18 | Francis et al. 2018, Cypher | origin, widely-built-on | 514 |
| 19 | Angles et al. 2017, graph query languages | survey-of-record | 294 |
| 20 | Banko et al. 2007, Open IE | origin | unstated |
| 21 | RDF Model and Syntax 1999 (W3C) | origin, turning-point | unstated (standard) |
| 22 | SPARQL 1.0 2008 (W3C) | origin, turning-point | unstated (standard) |
| 23 | OWL 2004 (W3C) | origin, turning-point | unstated (standard) |
| 24 | RDF Schema (W3C) | origin | unstated (standard) |
| 25 | Linked Data design note 2006 (Berners-Lee) | origin | unstated |

The order inside the file below follows the table.

---

## 1. Gruber 1993, "A Translation Approach to Portable Ontology Specifications"

- **Title:** A Translation Approach to Portable Ontology Specifications
- **Authors:** Thomas R. Gruber (1 author)
- **Venue:** *Knowledge Acquisition* 5(2):199-220 [1][4]
- **First version:** Stanford Knowledge Systems Laboratory Technical Report KSL 92-71, September 1992, revised April 1993; journal issue June 1993 [4][1]
- **Link:** https://doi.org/10.1006/knac.1993.1008
- **Citations:** 8,595 (Crossref, read 20261102 19:59) [1]; 12,781 (OpenAlex, read 20261102 between 19:44 and 19:58; clock not printed at the call) [2]
- **Tests passed:**
  - *Origin.* The abstract defines the term: "A specification of a representational vocabulary for a shared domain of discourse ... is called an ontology" (quote shortened; [4]). Noy and McGuinness cite it for their own definition, "explicit formal specifications of the terms in the domain and relations among them (Gruber 1993)" [7]. Whether the term was used earlier in AI: unstated in the sources read.
  - *Widely built on.* Crossref 8,595; OpenAlex 12,781 [1][2].
- **Idea:** To share and reuse formally represented knowledge, AI systems need a shared vocabulary. Gruber calls a specification of such a vocabulary (classes, relations, functions, other objects) an ontology. The paper describes Ontolingua, which translates definitions written in a standard predicate-calculus format into frame-based and relational systems, so one ontology can be reused across representations [4].
- **Relations:**
  - Cited by "Ontology Development 101" for the definition of ontology (Noy and McGuinness, considered below) [7].
  - Followed by Gruber 1995 (entry 6), which turns the idea into design criteria [5].
  - Later eras: Hogan et al. 2021 survey (other researcher's area) treats ontologies as optional schema for knowledge graphs [33]; whether it cites Gruber 1993 was not checked.
- **Read:** abstract and title page of the full text (27-page PDF; body not read), 20261102 20:02 [4]
- **Sources:** [1][2][4][7]

## 2. WordNet 1990, "Introduction to WordNet: An On-line Lexical Database"

- **Title:** Introduction to WordNet: An On-line Lexical Database
- **Authors:** George A. Miller, Richard Beckwith, Christiane Fellbaum (5 authors; the other two are Derek Gross and Katherine Miller) [20][1]
- **Venue:** *International Journal of Lexicography* 3(4), 1990 (venue and year from Crossref; the PDF read is the "Revised August 1993" report) [1][20]
- **First version:** 1990 [1]. The report states it describes "the state of WordNet as of 1990"; work began in 1985 at Princeton [20].
- **Link:** https://doi.org/10.1093/ijl/3.4.235 ; full report: https://wordnetcode.princeton.edu/5papers.pdf
- **Citations:** 2,249 (Crossref, read 20261102 20:00) for this paper [1]. The later overview "WordNet: a lexical database for English" (Miller, *Communications of the ACM*, Nov 1995, https://doi.org/10.1145/219717.219748) has 9,187 (Crossref, read 20261102 20:00) [1]. **Abstract of the 1995 paper not opened.**
- **Tests passed:**
  - *Origin.* Introduces WordNet: English nouns, verbs and adjectives organised into synonym sets, "each representing one underlying lexical concept", linked by different relations [20].
  - *Widely built on.* 2,249 and 9,187 [1]. YAGO builds on it directly (entry 9) [24]; ConceptNet 5.5 reports comparing against it (entry 13) [21].
- **Idea:** A lexical database designed after psycholinguistic theories of the mental lexicon, organised by meaning rather than alphabet: words grouped into synonym sets, sets joined by relations. It was meant to let people look words up conceptually, next to a conventional dictionary [20].
- **Relations:**
  - Builds on psycholinguistics (Miller and Johnson-Laird 1976, as cited in the report) [20].
  - Built on by YAGO 2007 ("unified with WordNet") [24]; compared with by ConceptNet 5.5 [21].
  - Earlier-era neighbours: semantic networks (Quillian 1963) in the primer lineage [34]; not claimed as a link by the WordNet report (not checked).
- **Read:** first pages of the full text (86-page PDF, "five papers"), 20261102 20:03 [20]
- **Sources:** [1][20][21][24][34]

## 3. Berners-Lee, Hendler, Lassila 2001, "The Semantic Web"

- **Title:** The Semantic Web
- **Authors:** Tim Berners-Lee, James Hendler, Ora Lassila (3 authors)
- **Venue:** *Scientific American* 284(5), May 2001 [8][1]
- **First version:** 1 May 2001 [8]
- **Link:** https://doi.org/10.1038/scientificamerican0501-34
- **Citations:** 8,727 (Crossref, read 20261102 20:00) [1]
- **Tests passed:**
  - *Origin.* The standard statement of the Semantic Web as a vision. Text: "The Semantic Web is not a separate Web but an extension of the current one, in which information is given well-defined meaning" (quotation of the article) [8]. The primer lists it as the general-audience presentation of the Semantic Web [34].
  - *Widely built on.* 8,727 [1]. The W3C RDF, OWL and SPARQL work and Linked Data (entries 21-25) all sit in this programme (the OWL entry says so in its own words, [18]).
- **Idea:** Most Web content is made for humans; the Semantic Web adds structure so that software agents can act on page content. The article introduces the idea through a scenario of agents arranging a family's appointments, and has sections on expressing meaning, knowledge representation, ontologies, agents and the evolution of knowledge [8].
- **Relations:**
  - Motivates RDF (entry 21) and OWL (entries 14, 23) [9][18].
  - Answered by Linked Data (entries 8, 25): Bizer et al. position Linked Data inside the Semantic Web context [17]; Berners-Lee's note gives four rules [16].
  - Later era: LLM-agent work revives "agents acting on structured web content" but no paper-level link was checked here.
- **Read:** the first screens of the full article (copy at inria.fr, 4-page PDF; the scenario and the "Expressing Meaning" section), and the publisher landing page, 20261102 20:01 to 20:04 [8]
- **Sources:** [1][8][9][17][18][34]

## 4. Brin and Page 1998, "The Anatomy of a Large-Scale Hypertextual Web Search Engine"

- **Title:** The Anatomy of a Large-Scale Hypertextual Web Search Engine
- **Authors:** Sergey Brin, Lawrence Page (2 authors)
- **Venue:** *Computer Networks and ISDN Systems* 30, pp. 107-117 [28][1]
- **First version:** 1998 (exact date unstated in the pages read) [28][1]
- **Link:** https://doi.org/10.1016/s0169-7552(98)00110-x
- **Citations:** 9,354 (Crossref, read 20261102 19:59). A 2012 reprint of the paper shows 717 separately [1]. Use the 1998 figure.
- **Tests passed:**
  - *Origin.* Presents Google, "a prototype search engine that relies on the link structure of hypertext"; the prototype database held at least 24 million pages [28] (summary of the abstract, not a quote).
  - *Widely built on.* 9,354 [1]. Bizer et al. cite it as the way search engines "analyse the structure of links between them to infer potential relevance" [17].
- **Idea:** A search engine design that crawls and indexes the Web at scale and uses hyperlink information to improve ranking, with attention to open collections where anyone can publish [28].
- **Relations:**
  - Answered/complemented by Kleinberg 1999 (entry 5): both use link structure for ranking; Kleinberg's abstract defines authority via hub pages [29].
  - Cited by Bizer et al. 2009 as the Web-of-documents baseline that Linked Data extends to data [17].
  - Lead only: PageRank is the ranking method of this prototype; the PageRank technical report (Page, Brin, Motwani, Winograd) was not readable (see "Considered"). Personalized PageRank is reused in HippoRAG (arXiv 2405.14831, 2024), per `kb-kg/papers-benchmarks/README.md` line 63 [35]. The step from Brin-Page to that use was not checked in the papers.
- **Read:** abstract (landing page summary), 20261102 20:05 [28]. The full text could not be fetched (hosts unreachable or blocked).
- **Sources:** [1][17][28][29][35]

## 5. Kleinberg 1999, "Authoritative Sources in a Hyperlinked Environment"

- **Title:** Authoritative Sources in a Hyperlinked Environment
- **Authors:** Jon M. Kleinberg (1 author)
- **Venue:** *Journal of the ACM* 46(5), 1999 (volume and issue not read; year from Crossref) [1]
- **First version:** IBM Research Report RJ 10076, May 1997; ACM-SIAM SODA 1998 (both per the paper's own footnote) [29]
- **Link:** https://doi.org/10.1145/324133.324140
- **Citations:** 5,838 (Crossref, read 20261102 19:59) [1]
- **Tests passed:**
  - *Origin.* "We propose and test an algorithmic formulation of the notion of authority, based on the relationship between a set of relevant authoritative pages and the set of 'hub pages'" (abstract, shortened) [29]. This is the HITS idea.
  - *Widely built on.* 5,838 [1].
- **Idea:** Mine the link structure of a hyperlinked collection to find authoritative pages for a broad query. Authorities and hubs reinforce each other; the formulation connects to eigenvectors of matrices tied to the link graph [29].
- **Relations:**
  - Parallel to Brin and Page 1998 (entry 4): same period, same signal (links) [28][29].
  - Neither builds on a knowledge-graph paper; both are the link-analysis side of "web-scale search" in the lineage the primer calls databases and search (not stated by the primer as such; my grouping).
- **Read:** abstract and introduction of the full text (34-page PDF), 20261102 20:04 [29]
- **Sources:** [1][28][29]

## 6. Gruber 1995, "Toward Principles for the Design of Ontologies Used for Knowledge Sharing"

- **Title:** Toward Principles for the Design of Ontologies Used for Knowledge Sharing
- **Authors:** Thomas R. Gruber (1 author)
- **Venue:** *International Journal of Human-Computer Studies* 43, pp. 907-928 [5][1]
- **First version:** presented at the International Workshop on Formal Ontology, March 1993, Padova; KSL 93-04; revision of 23 August 1993 [5]. Journal year 1995 [1].
- **Link:** https://doi.org/10.1006/ijhc.1995.1081
- **Citations:** 3,937 (Crossref, read 20261102 19:59) [1]
- **Tests passed:**
  - *Widely built on.* 3,937 [1].
  - *Origin.* Treats "formal ontologies ... as designed artifacts, formulated for specific purposes and evaluated against objective design criteria" and presents design criteria; applied to engineering mathematics and bibliographic data (abstract) [5]. Which later works adopt Gruber's named criteria: unstated, not checked.
- **Idea:** An engineering view of ontologies. The paper explains the role of ontologies in knowledge sharing, offers criteria to guide their development, and tests them on two case studies [5].
- **Relations:** builds on Gruber 1993 (entry 1), same author and programme [4][5]. Noy and McGuinness 2001 give a practical guide in the same line (considered) [7].
- **Read:** abstract and introduction start of the full text (23-page PDF), 20261102 20:02 [5]
- **Sources:** [1][4][5][7]

## 7. Freebase 2008, "Freebase: a collaboratively created graph database for structuring human knowledge"

- **Title:** Freebase: a collaboratively created graph database for structuring human knowledge
- **Authors:** Kurt Bollacker, Colin Evans, Praveen Paritosh (first three; 5 authors, plus Tim Sturge and Jamie Taylor) [25]
- **Venue:** SIGMOD 2008 (Proceedings of the 2008 ACM SIGMOD International Conference on Management of Data) [25][1]
- **First version:** 9 June 2008 (Crossref issued date) [1]
- **Link:** https://doi.org/10.1145/1376616.1376746
- **Citations:** 3,284 (Crossref, read 20261102 19:59) [1]
- **Tests passed:**
  - *Origin.* First-party description of a collaboratively edited tuple database: "over 125 million tuples, more than 4,000 types, and more than 7,000 properties", with an HTTP graph-query API using MQL [25]. First-party figures.
  - *Widely built on.* 3,284 [1]. Google's Knowledge Graph announcement (2012) is described by the primer as rooted in sources "such as Freebase" [34].
- **Idea:** A scalable tuple database for general human knowledge, created, structured and maintained collaboratively by users, and exposed through a read/write graph-query API [25].
- **Relations:**
  - Feeds Google's Knowledge Graph (2012) and was replaced by Wikidata (Google announced a shutdown in favour of Wikidata in Dec 2014): both statements from `kb-kg/primer/README.md` lines 79-80, which cites secondary sources; **not re-verified here** [34]. Wikidata paper: Vrandečić and Krötzsch, *CACM* 2014, 2,731 (Crossref, read 20:00) [1] (other researcher's era).
  - Contrast with DBpedia (entry 10) and YAGO (entry 9): those extract from Wikipedia; Freebase is edited directly [25][24][23].
  - Later era: TransE (Bordes et al. 2013) trained on knowledge-graph data of this kind; the primer gives the sizes but does not name Freebase as the source, so no link is claimed [34].
- **Read:** abstract (Google Research page), 20261102 20:05 [25]
- **Sources:** [1][23][24][25][34]

## 8. Bizer, Heath, Berners-Lee 2009, "Linked Data - The Story So Far"

- **Title:** Linked Data - The Story So Far
- **Authors:** Christian Bizer, Tom Heath, Tim Berners-Lee (3 authors)
- **Venue:** *International Journal on Semantic Web and Information Systems* 5(3), 2009 (issue not read; year/month from Crossref) [1][17]
- **First version:** July 2009 per Crossref; the preprint says it "is a preprint of a paper to appear in" the IJSWIS special issue [1][17]
- **Link:** https://doi.org/10.4018/jswis.2009081901
- **Citations:** 2,525 (Crossref, read 20261102 20:00). A book-chapter reprint (2011) shows 418 separately; use the journal figure [1].
- **Tests passed:**
  - *Survey of record.* "We present the concept and technical principles of Linked Data, and situate these within the broader context of related technological developments"; reviews publishing progress and applications and sets a research agenda (abstract, shortened) [17].
  - *Widely built on.* 2,525 [1].
- **Idea:** Defines Linked Data as a set of best practices for publishing and connecting structured data on the Web, reports that three years of adoption created a global data space of billions of assertions (the Web of Data), and maps next steps [17].
- **Relations:**
  - Builds on Berners-Lee's 2006 design note (entry 25) and the Semantic Web vision (entry 3) [16][17][8].
  - Builds on the Web-of-documents baseline of Brin and Page 1998 (cited in its introduction) [17][28].
  - Reports on projects of entries 10 and 12 (DBpedia): Lehmann 2015 calls DBpedia "one of the central interlinking hubs in the Linked Open Data (LOD) cloud" [23].
- **Read:** abstract and first page of the full text (26-page PDF preprint), 20261102 20:03 [17]
- **Sources:** [1][8][16][17][23][28]

## 9. YAGO 2007, "YAGO: A Core of Semantic Knowledge: Unifying WordNet and Wikipedia"

- **Title:** YAGO: A Core of Semantic Knowledge (subtitle: Unifying WordNet and Wikipedia)
- **Authors:** Fabian M. Suchanek, Gjergji Kasneci, Gerhard Weikum (3 authors)
- **Venue:** WWW 2007 (16th International World Wide Web Conference), Banff, 8-12 May 2007 [24][1]
- **First version:** 8 May 2007 [1]
- **Link:** https://doi.org/10.1145/1242572.1242667
- **Citations:** 2,509 (Crossref, read 20261102 19:59) [1]
- **Tests passed:**
  - *Origin.* A "light-weight and extensible ontology with high coverage and quality", automatically extracted from Wikipedia and unified with WordNet: "more than 1 million entities and 5 million facts", "an accuracy of about 95%" (the authors' own figures, first-party), with a "logically clean model, which is decidable, extensible, and compatible with RDFS" (abstract, shortened) [24].
  - *Widely built on.* 2,509 [1].
- **Idea:** Combine Wikipedia's category and infobox facts about individuals with WordNet's clean is-a hierarchy by rule-based and heuristic methods, so the result is "a major step beyond WordNet" in quality and in number of facts [24].
- **Relations:**
  - Builds on WordNet (entry 2) and Wikipedia; compatible with RDFS (entry 24) [24][20][10].
  - Same period and aim as DBpedia (entries 10, 12); DBpedia keeps a crowd-mapped ontology, YAGO ties to WordNet [24][23].
  - Follow-up YAGO2 (Artificial Intelligence 2013) exists; not read.
- **Read:** abstract and introduction start of the full text (10-page PDF), 20261102 20:01 [24]
- **Sources:** [1][10][20][23][24]

## 10. Auer et al. 2007, "DBpedia: A Nucleus for a Web of Open Data"

- **Title:** DBpedia: A Nucleus for a Web of Open Data
- **Authors:** Sören Auer, Christian Bizer, Georgi Kobilarov (first three; 6 authors in Crossref) [1]
- **Venue:** *The Semantic Web* (ISWC/ASWC 2007), Lecture Notes in Computer Science [1]
- **First version:** 2007 [1] (day unstated)
- **Link:** https://doi.org/10.1007/978-3-540-76298-0_52
- **Citations:** 2,448 (Crossref, read 20261102 20:00) [1]
- **Tests passed:**
  - *Origin.* The primer dates the start of the DBpedia project to 2007 and describes it as an early large open knowledge graph built from Wikipedia [34]. The 2007 paper itself is the project's first description by its authors' title; **its abstract and text were not opened** (Springer redirect; PDF hosts failed).
  - *Widely built on.* 2,448 [1].
- **Idea:** (Taken from the authors' 2015 system report, not from the 2007 paper.) The project extracts structured knowledge from Wikipedia and publishes it on the Web with Semantic Web and Linked Data technologies [23].
- **Relations:** continued by Lehmann et al. 2015 (entry 12) [23]; same source and similar aim as YAGO (entry 9); published as Linked Data (entry 8) [17].
- **Read:** **listing only** (title, authors, venue, count). The idea line above is from entry 12. 20261102 20:00
- **Sources:** [1][17][23][34]

## 11. Uschold and Gruninger 1996, "Ontologies: Principles, Methods and Applications"

- **Title:** Ontologies: Principles, Methods and Applications
- **Authors:** Mike Uschold, Michael Gruninger (2 authors)
- **Venue:** *The Knowledge Engineering Review* 11(2), June 1996 (AIAI-TR-191, February 1996) [6][1]
- **First version:** AIAI-TR-191, February 1996 [6]
- **Link:** https://doi.org/10.1017/s0269888900007797
- **Citations:** 2,241 (Crossref, read 20261102 19:59) [1]
- **Tests passed:**
  - *Survey of record (for ontology engineering).* "intended to serve as a comprehensive introduction to the emerging field concerned with the design and use of ontologies" (abstract, shortened) [6].
  - *Widely built on.* 2,241 [1].
- **Idea:** Disparate backgrounds, languages and tools impede communication between people, organisations and software; an explicit shared account of a subject area (an ontology) improves communication, reuse and interoperability. The paper clarifies what ontologies are, outlines a methodology for developing and evaluating them, first informal then formal [6].
- **Relations:** parallels Gruber 1993 and 1995 (entries 1, 6); did not check whether it cites them [6].
- **Read:** abstract and first page of the full text (69-page technical report, scanned font garbled, abstract legible), 20261102 20:04 [6]
- **Sources:** [1][6]

## 12. Lehmann et al. 2015, "DBpedia: a large-scale, multilingual knowledge base extracted from Wikipedia"

- **Title:** DBpedia - A large-scale, multilingual knowledge base extracted from Wikipedia
- **Authors:** Jens Lehmann, Robert Isele, Max Jakob (first three; 11 authors) [23][1]
- **Venue:** *Semantic Web* journal (IOS Press), 2015 (the PDF read carries a 2012 submission header) [23][1]
- **First version:** 2015 per Crossref; submission-draft header says 2012 [1][23]
- **Link:** https://doi.org/10.3233/sw-140134
- **Citations:** 1,893 (Crossref, read 20261102 20:00) [1]
- **Tests passed:**
  - *Widely built on.* 1,893 [1].
  - *Survey of record (for DBpedia).* A "system report" giving "an overview of the DBpedia community project, including its architecture, technical implementation, maintenance, internationalisation, usage statistics and applications" [23].
- **Idea:** Reports 111 Wikipedia language editions extracted; the English KB has "over 400 million facts that describe 3.7 million things"; infobox mappings from 27 languages to one ontology of 320 classes and 1,650 properties; SPARQL access; 27 million RDF links into over 30 external sources (first-party figures, abstract) [23].
- **Relations:** continues Auer et al. 2007 (entry 10); one of the central hubs of the Linked Open Data cloud, which Bizer et al. describe (entry 8) [23][17].
- **Read:** abstract of the full text (29-page PDF), 20261102 20:03 [23]
- **Sources:** [1][17][23]

## 13. Speer, Chin, Havasi 2017, "ConceptNet 5.5: An Open Multilingual Graph of General Knowledge"

- **Title:** ConceptNet 5.5: An Open Multilingual Graph of General Knowledge
- **Authors:** Robyn Speer, Joshua Chin, Catherine Havasi (3 authors)
- **Venue:** AAAI 2017 [1]
- **First version:** arXiv v1, 12 December 2016 (v2, 11 December 2018) [21]
- **Link:** https://arxiv.org/abs/1612.03975
- **Citations:** 1,386 (Crossref for the AAAI DOI, read 20261102 19:59) [1]
- **Tests passed:**
  - *Widely built on.* 1,386 [1].
  - (Not an origin: the predecessor "ConceptNet - a practical commonsense reasoning tool-kit", Liu and Singh, *BT Technology Journal* 2004, 949 (Crossref, read 20:00), https://doi.org/10.1023/b:bttj.0000047600.45421.6d, is the earlier paper; its abstract was **not** opened, so I do not claim origin on its behalf [1].)
- **Idea:** A knowledge graph of words and phrases with labelled edges, built from expert-created resources, crowdsourcing and games with a purpose, released as linked open data. Combined with word embeddings such as word2vec, the authors report state-of-the-art word-relatedness results and SAT-style analogies (first-party claim) [21].
- **Relations:**
  - Evaluated against/with WordNet and DBpedia: "ConceptNet outperforms what either approach achieves alone or with narrower resources like WordNet or DBpedia" (summary of the abstract) [21].
  - Builds on Liu and Singh 2004 (same project; see above) [1].
- **Read:** abstract (arXiv), 20261102 20:05 [21]
- **Sources:** [1][21]

## 14. Horrocks, Patel-Schneider, van Harmelen 2003, "From SHIQ and RDF to OWL: the making of a Web Ontology Language"

- **Title:** From SHIQ and RDF to OWL: the making of a Web Ontology Language
- **Authors:** Ian Horrocks, Peter F. Patel-Schneider, Frank van Harmelen (3 authors)
- **Venue:** *Journal of Web Semantics* 1(1), December 2003 (issue per Crossref date 2003-12) [1][18]
- **First version:** 2003 [1]
- **Link:** https://doi.org/10.1016/j.websem.2003.07.001
- **Citations:** 894 (Crossref, read 20261102 19:59) [1]
- **Tests passed:**
  - *Origin (of the design account).* The authors, who sat on the W3C Web Ontology Working Group, trace OWL's features back to description logics and frames and to RDF, and discuss where these influences clashed (abstract) [18].
  - *Turning point.* It explains the design compromise behind OWL's sublanguages; the W3C overview states OWL Lite, DL and Full as "three sublanguages of increasing expressiveness" [11][18].
  - *Widely built on.* 894 [1].
- **Idea:** OWL is "a new formal language for representing ontologies in the Semantic Web" with features of description logics and frames; it shares many characteristics with RDF, the W3C base of the Semantic Web [18].
- **Relations:** explains the W3C OWL Recommendation (entry 23) [18][11]; builds on RDF (entry 21) and description logics (the primer says description logics grew from KL-ONE, 1985, an earlier-era paper) [18][34].
- **Read:** abstract and introduction of the full text (31-page PDF), 20261102 20:03 [18]
- **Sources:** [1][11][18][34]

## 15. Carlson et al. 2010, "Toward an Architecture for Never-Ending Language Learning" (NELL)

- **Title:** Toward an Architecture for Never-Ending Language Learning
- **Authors:** Andrew Carlson, Justin Betteridge, Bryan Kisiel (first three; 6 authors, including Tom M. Mitchell) [26][1]
- **Venue:** AAAI 2010 (Proceedings of the AAAI Conference on Artificial Intelligence, vol. 24) [1]
- **First version:** 2010 [1] (day unstated)
- **Link:** https://doi.org/10.1609/aaai.v24i1.7519
- **Citations:** 783 (Crossref, read 20261102 19:59) [1]
- **Tests passed:**
  - *Origin.* Proposes a "never-ending language learner" that each day reads the web to populate a growing knowledge base and learns to read better; a partial implementation "learned to extract a knowledge base containing over 242,000 beliefs with an estimated precision of 74% after running for 67 days" (abstract, first-party figures) [26].
- **Idea:** Exploit the redundancy of the web by running a system forever that both extracts facts and improves its own extractors. The paper offers design principles, a partial implementation, and lessons learned [26].
- **Relations:**
  - Followed by "Never-Ending Learning" (Mitchell et al., AAAI 2015; *CACM* 2018, 426 (Crossref, read 20:00), https://doi.org/10.1145/3191513): NELL "has been learning to read the web 24 hours/day since January 2010" and holds "over 80 million confidence-weighted beliefs" (first-party). I read the 2015 version only [1][26].
  - Parallel to Open IE (entry 20): both extract from the web without hand-built rules per relation; Banko et al. compare TextRunner with KnowItAll, not NELL [27].
  - Later era: Knowledge Vault (Dong et al. 2014) extracts facts at web scale with calibrated probabilities (per primer) [34]; no explicit link to NELL was found in the sources read.
- **Read:** abstract and introduction of the full text (8-page PDF, 2010); abstract of the 2015 follow-up, 20261102 20:02 to 20:04 [26]
- **Sources:** [1][26][27][34]

## 16. Pérez, Arenas, Gutierrez 2009, "Semantics and complexity of SPARQL"

- **Title:** Semantics and Complexity of SPARQL
- **Authors:** Jorge Pérez, Marcelo Arenas, Claudio Gutierrez (3 authors)
- **Venue:** *ACM Transactions on Database Systems* 34(3), 2009 [1]
- **First version:** arXiv:cs/0605124, 26 May 2006 [19]
- **Link:** https://arxiv.org/abs/cs/0605124 ; DOI https://doi.org/10.1145/1567274.1567278
- **Citations:** 764 (Crossref for the TODS DOI, read 20261102 19:59) [1]
- **Tests passed:**
  - *Origin (formal semantics).* Studies SPARQL while it was a W3C candidate recommendation: gives a compositional semantics, shows normal forms exist and that evaluating SPARQL patterns is PSPACE-complete (paraphrase of the abstract) [19].
  - *Widely built on.* 764 [1].
- **Idea:** Treat SPARQL's graph pattern facility as a formal language: semantics, complexity and optimisation, and a comparison with an alternative operational semantics [19].
- **Relations:** evaluates the SPARQL 1.0 language (entry 22) [19][14]; SPARQL 1.1 (2013) extends the language (aggregation, subqueries, negation), per its abstract; whether it adopts this paper's semantics: unstated [15].
- **Read:** abstract (arXiv), 20261102 20:00; first pages of the PDF, 20:04 [19]
- **Sources:** [1][14][15][19]

## 17. Angles and Gutierrez 2008, "Survey of graph database models"

- **Title:** Survey of Graph Database Models
- **Authors:** Renzo Angles, Claudio Gutierrez (2 authors)
- **Venue:** *ACM Computing Surveys* 40(1), Article 1, February 2008 [30]
- **First version:** February 2008 [30]
- **Link:** https://doi.org/10.1145/1322432.1322433
- **Citations:** 749 (Crossref, read 20261102 19:59) [1]
- **Tests passed:**
  - *Survey of record.* The survey of graph database modelling: "data structures, query languages, and integrity constraints" [30]. Angles et al. 2017 and Hogan et al. 2021 treat graph data models in the same vocabulary [32][33]; whether they cite it was not checked.
- **Idea:** Graph database models "took off in the eighties and early nineties alongside object-oriented models", faded as other models rose, and were revived by the need to manage graph-like information [30].
- **Relations:** precedes Angles et al. 2017 (entry 19), which covers edge-labelled and property graphs [30][32]; background to Neo4j's property graph (Neo4j 1.0 reported 25 Feb 2010, per primer) [34].
- **Read:** abstract and introduction of the full text (39-page PDF), 20261102 20:01 [30]
- **Sources:** [1][30][32][33][34]

## 18. Francis et al. 2018, "Cypher: An Evolving Query Language for Property Graphs"

- **Title:** Cypher: An Evolving Query Language for Property Graphs
- **Authors:** Nadime Francis, Alastair Green, Paolo Guagliardo (first three; 10 authors) [31]
- **Venue:** SIGMOD 2018 (International Conference on Management of Data) [1]
- **First version:** 2018 [1] (day unstated)
- **Link:** https://doi.org/10.1145/3183713.3190657
- **Citations:** 514 (Crossref, read 20261102 19:59) [1]
- **Tests passed:**
  - *Origin (formal definition).* "We describe Cypher 9, which is the first version of the language governed by the openCypher Implementers Group" and "provide a formal semantic definition of the core read-query features of Cypher, including its variant of the property graph data model" (abstract) [31].
  - *Widely built on.* 514 [1].
- **Idea:** Cypher was "originally designed and implemented as part of the Neo4j graph database" and is used by several commercial products. The paper introduces the language by example, defines its semantics, compares it with other property graph query languages, and previews Cypher 10 [31].
- **Relations:** one of the three languages illustrated by Angles et al. 2017 (SPARQL, Cypher, Gremlin) (entry 19) [32]; the property-graph side of the primer's two traditions [34]. Kuzu (an embedded property-graph database with Cypher) archived October 2025, per `kb-kg/llm-era/README.md` line 83 (other era; not re-verified) [34].
- **Read:** abstract and first pages of the full text (13-page PDF), 20261102 20:03 [31]
- **Sources:** [1][31][32][34]

## 19. Angles et al. 2017, "Foundations of Modern Query Languages for Graph Databases"

- **Title:** Foundations of Modern Query Languages for Graph Databases
- **Authors:** Renzo Angles, Marcelo Arenas, Pablo Barceló (first three; 6 authors) [32]
- **Venue:** *ACM Computing Surveys* 50(5), 2017 (issue not read; year from Crossref) [1]
- **First version:** arXiv 20 October 2016 (v3 15 June 2017) [32]
- **Link:** https://arxiv.org/abs/1610.06264 ; DOI https://doi.org/10.1145/3104031
- **Citations:** 294 (Crossref, read 20261102 19:59) [1]
- **Tests passed:**
  - *Survey of record (graph query languages).* Covers two graph data models (edge-labelled and property graphs), graph patterns and navigational expressions, evaluation semantics and complexity, illustrated with SPARQL, Cypher and Gremlin [32].
- **Idea:** The core of graph query languages is patterns plus recursive path navigation. The paper fixes both data models and compares evaluation costs [32].
- **Relations:** covers SPARQL (entries 22, 16) and Cypher (entry 18) [32]; extends the data-model survey of Angles and Gutierrez 2008 (entry 17) [30][32]; same first author as the 2008 survey.
- **Read:** abstract (arXiv), 20261102 20:05 [32]
- **Sources:** [1][30][32]

## 20. Banko et al. 2007, "Open Information Extraction from the Web"

- **Title:** Open Information Extraction from the Web
- **Authors:** Michele Banko, Michael J. Cafarella, Stephen Soderland (first three; 5 authors) [27]
- **Venue:** IJCAI 2007 (Proceedings, paper 429; venue from the URL path `Proceedings/07`) [27]
- **First version:** 2007 [27] (day unstated)
- **Link:** https://www.ijcai.org/Proceedings/07/Papers/429.pdf
- **Citations:** unstated (no DOI; Semantic Scholar and OpenAlex unavailable) [2][3]
- **Tests passed:**
  - *Origin.* "This paper introduces Open IE (OIE), a new extraction paradigm where the system makes a single data-driven pass over its corpus and extracts a large set of relational tuples without requiring any human input" (abstract) [27].
- **Idea:** Instead of naming target relations and writing rules for each, run one pass over the corpus and extract all relational tuples. TextRunner indexes tuples with probabilities. On 9 million Web pages the authors report a 33% error reduction against KnowItAll on a comparable set (first-party); 11,000,000 highest-probability tuples contain over 1,000,000 concrete facts [27].
- **Relations:** evaluates against KnowItAll (a state-of-the-art Web IE system, per the abstract) [27]; parallels NELL (entry 15) [26].
- **Read:** abstract of the full text (7-page PDF), 20261102 20:03 [27]
- **Sources:** [2][3][26][27]

## 21. W3C 1999, "Resource Description Framework (RDF) Model and Syntax Specification"

- **Title:** Resource Description Framework (RDF) Model and Syntax Specification
- **Authors (editors):** Ora Lassila, Ralph R. Swick (2 editors)
- **Venue:** W3C Recommendation
- **First version:** 22 February 1999 (the page's date; the primer lists it as 19990222) [9][34]
- **Link:** https://www.w3.org/TR/1999/REC-rdf-syntax-19990222/
- **Citations:** unstated (standard; no citation source reachable)
- **Tests passed:**
  - *Origin.* The first W3C Recommendation for RDF: "a model for representing RDF metadata and an XML-based syntax for encoding and transporting it" so independently developed servers and clients can interoperate [9].
  - *Turning point.* The primer states the triple data model (subject, predicate, object) that later knowledge-graph work uses [34]. It was superseded by RDF 1.1 Concepts (25 February 2014; editors Cyganiak, Wood, Lanthaler: graphs of triples plus datasets) [15] and by the RDF Semantics 2004 document, which gives "a precise semantics" for RDF and RDFS [13].
- **Idea:** A way to describe Web resources with properties and values and to exchange those descriptions in XML [9].
- **Relations:** foundation for RDF Schema (entry 24), OWL (entries 14, 23) and SPARQL (entry 22) [9][11][14]; Horrocks et al. say OWL "shares many characteristics with RDF" [18].
- **Read:** first 100,000 of 113,893 characters of the specification, 20261102 19:45 [9]
- **Sources:** [9][11][13][14][15][18][34]

## 22. W3C 2008, "SPARQL Query Language for RDF"

- **Title:** SPARQL Query Language for RDF
- **Authors (editors):** Eric Prud'hommeaux, Andy Seaborne (2 editors)
- **Venue:** W3C Recommendation
- **First version:** 15 January 2008 [14]
- **Link:** https://www.w3.org/TR/2008/REC-rdf-sparql-query-20080115/
- **Citations:** unstated (standard)
- **Tests passed:**
  - *Origin.* The first Recommendation of the query language for RDF: required and optional graph patterns, conjunctions and disjunctions, extensible value tests, constraints by source graph; results as result sets or RDF graphs [14].
  - *Turning point.* Pérez et al. 2009 studied it formally while it was a candidate recommendation (entry 16) [19]. SPARQL 1.1 (21 March 2013; editors Harris and Seaborne) adds aggregation, subqueries and negation [15].
- **Idea:** One standard way to query data held as RDF, natively or exposed by middleware [14].
- **Relations:** queries RDF (entry 21); evaluated by Pérez et al. (entry 16) [19]; illustrated beside Cypher and Gremlin by Angles et al. 2017 (entry 19) [32].
- **Read:** first 100,000 of 198,517 characters of SPARQL 1.0; abstract of SPARQL 1.1, 20261102 19:45 [14][15]
- **Sources:** [14][15][19][32]

## 23. W3C 2004, "OWL Web Ontology Language" (Overview and Semantics)

- **Title:** OWL Web Ontology Language Overview (and OWL Web Ontology Language Semantics and Abstract Syntax)
- **Authors (editors):** Overview: Deborah L. McGuinness, Frank van Harmelen. Semantics: Peter F. Patel-Schneider, Patrick Hayes, Ian Horrocks [11][12]
- **Venue:** W3C Recommendations
- **First version:** 10 February 2004 [11][12]
- **Link:** https://www.w3.org/TR/owl-features/ ; https://www.w3.org/TR/2004/REC-owl-semantics-20040210/
- **Citations:** unstated (standard)
- **Tests passed:**
  - *Origin.* The W3C Recommendation for OWL, "built for applications that must process the content of information, not just present it to people", in three sublanguages: OWL Lite, OWL DL and OWL Full [11].
  - *Turning point.* Sets the expressiveness/decidability trade-off: DL keeps decidability, Full has "no computational guarantees" (per the primer, [34]). OWL 2 followed (Second Edition, 11 December 2012) [15].
- **Idea:** A formal vocabulary and semantics on top of RDF and RDF Schema that lets machines interpret ontologies. The semantics document gives a model-theoretic semantics for OWL DL and OWL Lite and an extension of the RDF semantics for OWL Full [12].
- **Relations:** builds on RDF and RDFS (entries 21, 24) [11]; design history in Horrocks et al. 2003 (entry 14) [18].
- **Read:** abstracts and front matter of the Overview and the Semantics documents, plus OWL 2 Overview, 20261102 19:45 and 20:05 [11][12][15]
- **Sources:** [11][12][15][18][34]

## 24. W3C, "RDF Schema"

- **Title:** RDF Schema 1.1 (the 2004 edition, "RDF Vocabulary Description Language 1.0", was **not read**)
- **Authors (editors):** Dan Brickley, R.V. Guha (2 editors; Brian McBride previous editor) [10]
- **Venue:** W3C Recommendation, 25 February 2014 (status update 1 December 2023) [10]
- **First version:** 2004 edition: date unstated in the pages read
- **Link:** https://www.w3.org/TR/rdf-schema/
- **Citations:** unstated (standard)
- **Tests passed:**
  - *Origin.* "RDF Schema provides a data-modelling vocabulary for RDF data" (first sentence of the abstract) [10]. Gives RDF classes and properties. The RDF Semantics document specifies semantics for RDF and RDFS together [13].
- **Idea:** A small vocabulary for describing classes and properties of RDF data, which OWL extends.
- **Relations:** layer between RDF (entry 21) and OWL (entry 23); YAGO says it is "compatible with RDFS" (entry 9) [24].
- **Read:** abstract and header of the RDF Schema 1.1 document, 20261102 19:45 [10]
- **Sources:** [10][13][24]

## 25. Berners-Lee 2006, "Linked Data" (design note)

- **Title:** Linked Data (W3C Design Issues)
- **Authors:** Tim Berners-Lee (1 author)
- **Venue:** W3C DesignIssues note, not peer reviewed [16]
- **First version:** 27 July 2006 (last changed 18 June 2009) [16]
- **Link:** https://www.w3.org/DesignIssues/LinkedData.html
- **Citations:** unstated (web note)
- **Tests passed:**
  - *Origin.* States the four rules: "Use URIs as names for things"; "Use HTTP URIs so that people can look up those names"; "provide useful information, using the standards (RDF*, SPARQL)"; "Include links to other URIs" (quotes shortened) [16].
- **Idea:** Publish data on the Web so that each thing has an HTTP URI that returns useful RDF and links to other things [16].
- **Relations:** developed in Bizer, Heath, Berners-Lee 2009 (entry 8) [17]; a lowest-common-denominator for open knowledge graphs, per the primer's reading of Ehrlinger and Wöß [34].
- **Read:** the four rules and header, 20261102 19:45 [16]
- **Sources:** [16][17][34]

---

## Considered and not proposed

- **The PageRank citation ranking (Page, Brin, Motwani, Winograd, 1999 Stanford report):** the origin of PageRank, but the Stanford host failed (HTTP 500 and connection refused), the one PDF copy I fetched had unreadable font encoding, and no count was obtainable. Strong candidate once the text and a count are available. Not marked proposed because no test could be evidenced from a source read.
- **Studer, Benjamins, Fensel 1998, "Knowledge engineering: principles and methods" (Data & Knowledge Engineering):** 2,502 (Crossref, read 20:00) [1]; abstract not opened, so no evidence of the tests beyond the count.
- **Noy and McGuinness 2001, "Ontology Development 101":** introduction read [7]; a technical report with no DOI and no obtainable count, so "widely built on" cannot be evidenced. A good practical-guide candidate if a count is found.
- **Guarino 1995, "Formal ontology, conceptual analysis and knowledge representation" (IJHCS):** 527 (Crossref, read 19:59) [1]; abstract not opened.
- **Lenat 1995, "CYC: a large-scale investment in knowledge infrastructure" (CACM):** 981 (Crossref, read 19:59) [1]; belongs to the earlier-KB researcher's area; the primer cites Lenat 1985 [34].
- **Bizer et al. 2009, "DBpedia - a crystallization point for the Web of Data" (J. Web Semantics):** 1,477 (Crossref, read 19:59) [1]; abstract not opened; DBpedia is covered by entries 10 and 12.
- **Jeh and Widom 2003, "Scaling personalized web search":** 739 (Crossref, read 19:59); **Haveliwala 2002, "Topic-sensitive PageRank":** 907 (Crossref, read 20:00) [1]. Abstracts not opened. Relevant as the bridge to HippoRAG's use of Personalized PageRank [35]; the bridge claim is not checked.
- **Rodriguez and Neubauer 2010, "Constructions from dots and lines":** 127 (Crossref, read 19:59) [1]; arXiv 1006.2361 abstract read (a general essay on when graph representations pay off); no evidence that it introduced the property-graph model, so not proposed [read 20:05].
- **SPARQL 1.1 (2013) and OWL 2 (2009, Second Edition 2012):** revisions; mentioned inside entries 22 and 23.
- **RDF 1.1 Concepts (2014) and RDF Semantics (2004):** mentioned inside entry 21; not separate groups.
- **Liu and Singh 2004, ConceptNet (BT Technology Journal):** 949 (Crossref, read 20:00) [1]; abstract not opened; ConceptNet 5.5 carries the entry.
- **Wikidata (Vrandečić and Krötzsch 2014, CACM):** 2,731 (Crossref, read 20:00) [1]; outside this era; belongs to the knowledge-graph-era researcher.
- **Hogan et al. 2021, "Knowledge Graphs" (CSUR):** 1,950 (Crossref, read 20:00); arXiv 2003.02320 abstract read, 20:05 [1][33]; the survey of record for the whole field, so it belongs to the survey-focused researcher, not to this area.
- **Ferrucci et al. 2013 "Watson: Beyond Jeopardy!":** appeared by accident in a DOI lookup (261, Crossref); out of scope.
- **Mitchell et al. 2018, "Never-Ending Learning" (CACM):** folded into entry 15.
- **Neo4j 1.0 (2010), Gremlin, TinkerPop:** no paper read; the primer reports Neo4j 1.0 via InfoQ [34].
- **Classic description-logic and frame papers (KL-ONE 1985, Minsky 1974, Quillian 1963):** earlier-era researcher's area; the primer lists them [34].

## Sources

1. https://api.crossref.org/works (title searches, read 20261102 19:59) and https://api.crossref.org/works/{doi} (DOI lookups, read 20261102 20:00) : `is-referenced-by-count`, titles, authors, venues, issued dates. Lower bound.
2. https://api.openalex.org/works?search=A+Translation+Approach+to+Portable+Ontology+Specifications : cited_by_count 12,781 for Gruber 1993 (read 20261102, between 19:44 and 19:58); later calls refused, daily budget used up.
3. https://api.semanticscholar.org/graph/v1/paper/... : HTTP 429 on every request (19:44 to 20:05); no data.
4. https://tomgruber.org/writing/ontolingua-kaj-1993.pdf : title page, abstract of Gruber 1993 (read 20261102 20:02).
5. https://tomgruber.org/writing/onto-design.pdf : abstract of Gruber 1995 (read 20261102 20:02).
6. http://www.aiai.ed.ac.uk/project/pub/documents/1996/96-ker-intro-ontologies.pdf : abstract of Uschold and Gruninger 1996 (read 20261102 20:04).
7. https://protege.stanford.edu/publications/ontology_development/ontology101.pdf : introduction, cites Gruber 1993 for the definition (read 20261102 20:03).
8. https://www.scientificamerican.com/article/the-semantic-web/ (landing page) and a 4-page copy at https://www-sop.inria.fr/acacia/cours/essi2006/ (article start) : the Semantic Web article (read 20261102 20:01 to 20:04).
9. https://www.w3.org/TR/1999/REC-rdf-syntax-19990222/ : RDF Model and Syntax (read 20261102 19:45).
10. https://www.w3.org/TR/rdf-schema/ : RDF Schema 1.1 (read 20261102 19:45).
11. https://www.w3.org/TR/owl-features/ : OWL Overview (read 20261102 19:45).
12. https://www.w3.org/TR/2004/REC-owl-semantics-20040210/ : OWL Semantics and Abstract Syntax (read 20261102 20:05).
13. https://www.w3.org/TR/2004/REC-rdf-mt-20040210/ : RDF Semantics (read 20261102 20:05).
14. https://www.w3.org/TR/2008/REC-rdf-sparql-query-20080115/ : SPARQL 1.0 (read 20261102 19:45).
15. https://www.w3.org/TR/sparql11-query/ , https://www.w3.org/TR/owl2-overview/ , https://www.w3.org/TR/rdf11-concepts/ : SPARQL 1.1, OWL 2 Overview, RDF 1.1 Concepts (read 20261102 19:45).
16. https://www.w3.org/DesignIssues/LinkedData.html : the four rules (read 20261102 19:45).
17. http://tomheath.com/papers/bizer-heath-berners-lee-ijswis-linked-data.pdf : abstract and introduction (read 20261102 20:03).
18. https://www.cs.ox.ac.uk/ian.horrocks/Publications/download/2003/HoPH03a.pdf : abstract and introduction (read 20261102 20:03).
19. https://arxiv.org/abs/cs/0605124 (read 20261102 20:00) and https://arxiv.org/pdf/cs/0605124 (read 20261102 20:04) : Pérez et al.
20. https://wordnetcode.princeton.edu/5papers.pdf : "Introduction to WordNet", revised August 1993 (read 20261102 20:03).
21. https://arxiv.org/abs/1612.03975 : ConceptNet 5.5 (read 20261102 20:05).
22. (unused)
23. http://jens-lehmann.org/files/2015/swj_dbpedia.pdf : DBpedia system report (read 20261102 20:03).
24. https://suchanek.name/work/publications/www2007.pdf : YAGO (read 20261102 20:01, via the saved PDF).
25. https://research.google/pubs/freebase-a-collaboratively-created-graph-database-for-structuring-human-knowledge/ : Freebase abstract (read 20261102 20:05).
26. https://www.cs.cmu.edu/~acarlson/papers/carlson-aaai10.pdf (NELL 2010, read 20261102 20:02) and https://www.cs.cmu.edu/~tom/pubs/NELL_aaai15.pdf (Never-Ending Learning, read 20261102 20:04).
27. https://www.ijcai.org/Proceedings/07/Papers/429.pdf : Open IE (read 20261102 20:03).
28. https://research.google/pubs/the-anatomy-of-a-large-scale-hypertextual-web-search-engine/ : Brin and Page abstract (read 20261102 20:05).
29. https://www.cs.cornell.edu/&#47;home/kleinber/auth.pdf : Kleinberg (read 20261102 20:04).
30. https://users.dcc.uchile.cl/~cgutierr/papers/surveyGDB.pdf : Angles and Gutierrez (read 20261102 20:01).
31. https://homepages.inf.ed.ac.uk/pguaglia/papers/sigmod18.pdf : Cypher (read 20261102 20:03).
32. https://arxiv.org/abs/1610.06264 : Angles et al. 2017 (read 20261102 20:05).
33. https://arxiv.org/abs/2003.02320 : Hogan et al. (read 20261102 20:05).
34. Repository leads (read 20261102 19:4x, via the worktree): `kb-kg/primer/README.md` lines 65-80 (timeline rows, lineage) and 130+ (traditions); `kb-kg/llm-era/README.md` line 83. These are the archive's own statements with their own sources; I did not re-verify them.
35. `kb-kg/papers-benchmarks/README.md` line 63: HippoRAG row, "LLM + knowledge graph + Personalized PageRank" (read 20261102 19:4x, via the worktree; not re-verified).
