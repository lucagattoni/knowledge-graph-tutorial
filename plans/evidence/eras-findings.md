# Step 0 findings: evidence for the eras of the History chapter

**Delivery note.** The harness refused to let me write `step0-eras/findings.md` ("Subagents should return findings as text, not write report files"), so I did not work around it. The full findings are below, inline, in the five requested sections. Supporting material is on disk in my folder `<scratch folder>/step0-eras/`: `notes/` (per-source quote notes, S3 to S15), `dl/<name>/` (each download in its own folder, with the extracted `.txt` beside it), `scripts/` (three small helper scripts). Nothing in the repository or any git worktree was touched.

## Summary (about 480 words)

**Sources read (23, plus 15 W3C pages).** Archive leads: the primer and llm-era pages (S1, S2). Explicit periodisations: Gutierrez and Sequeda, CACM 2021 (S3, five periods); Hitzler, CACM 2021 (S14, three phases); Gao et al. (S5) and Singh et al. (S18) for RAG; Stonebraker and Pavlo 2024 (S7) for data models; Sanderson and Croft 2012 (S9) and Lin et al. 2021 (S10) for IR. Other histories: Hogan et al. (S4, Appendix A, no era scheme), Sowa (S12), Stanford AI100 (S13), Shadbolt 1989 (S15), Feigenbaum 1977 (S22), Dartmouth 1955 (S11), Codd 1970 (S8), Angles and Gutierrez 2008 (S23), agent-memory survey (S6), LLM+KG roadmap (S19), W3C status pages (S16), arXiv dates (S20), Google 2012 (S17), GQL page (S21).

**Independence caveat.** S3, S4 and S23 share authors (Gutierrez; Sequeda on S3 and S4) and a Dagstuhl origin. The independent pre-2010 sources are S12, S13, S14, S15, S22 for knowledge, S7 for databases, S9 and S10 for IR.

**Shared boundary points (two or more sources).** About 1950 to 1956 (AI named, semantic networks, "information retrieval" coined). The 1970s as formal foundations (relational model 1970; frames, networks; "expert systems appeared as a distinct line around the late 70's"). 1979 to 1985 (description logics, expert-system boom). 1993 to 1997 (Web search, semistructured data, first RDF draft). 2001 (Semantic Web). 2004 (OWL, RDF 1.0). 2006 (Linked Data). 2008 (SPARQL). 2011 to 2012 (schema.org, Google KG 20120516, Wikidata). 2018 to 2020 (BERT, REALM, RAG). Late 2022 (ChatGPT; exact date unstated in every fetched page).

**Most important disagreements.**
1. The expert-system bust: mid-1980s (S13) versus about 1990 (S3).
2. First use of "knowledge graph": 1972 versus 1973 inside S4 itself; Bakker's late-1980s thesis (S3); "modern" from 2012.
3. RDF's first standard: W3C Recommendation 19990222 (S16a) versus "2004" (S14, which matches RDF 1.0, S16b).
4. KL-ONE and description logics dated 1979, 1984 or 1985; conceptual graphs 1976 or 1979.
5. "Naive RAG" means embeddings plus a vector database in S5 but keyword TF-IDF/BM25 in S18.
6. Sparse retrieval "supplanted" by dense (S7) versus BM25 still the starting point (S10) and hybrid retrieval (S5, S18).
7. Graph databases: rise, decline, revival (S23) versus "we do not expect specialized graph DBMSs to be a large market" (S7).

**Key finding for the 2020 to 2026 era.** No survey read gives dated phases there. The archive's seven phases are its author's judgement and, from 2024 on, rest on repositories and vendor posts. Surveys of 2025 and 2026 call agent memory "increasingly fragmented" (S6) and Agentic RAG "fragmented" with "inconsistent terminology" (S18). W3C's 1.2 drafts (RDF 1.2 Candidate Recommendation Snapshot 20260407; SPARQL 1.2 and SHACL 1.2 Core Working Drafts, 20261101 and 20261102) show the semantic-web stack is both settled (1.1-era Recommendations) and still moving.

**Archive checks.** Every W3C date and 17 arXiv dates I re-read from the archive pages matched the primary pages.

**Path.** `findings.md` could not be written; the content follows. Notes: `.../scratchpad/step0-eras/notes/`.

---

Compiled 20261102 19:48 UTC. Evidence only: no eras are proposed here. Dates are written `YYYYMMDD`, or `YYYYMM` / `YYYY` where only that is known. Where a source is silent the text says **unstated**.

How this was read. Each PDF was downloaded into its own folder and turned into text with pypdf (run with `python3 -I`); quotes were checked against that text (the Dartmouth PDF has garbled spacing; its quote is normalised). Raw W3C and Stanford HTML was stripped to text with the standard library. Pages marked "WebFetch extraction" were summarised by the fetch tool's small model, so their quotes are as returned and not checked against raw HTML. Read times are the clock at the batch of calls (accuracy about 2 minutes). Web-search summaries were used only to find URLs and are not cited.

Two cautions that apply to everything below.
1. **S3, S4 and S23 are not independent of each other.** Gutierrez is an author of all three, Sequeda of S3 and S4, and S3 and S4 both thank the Dagstuhl seminars. The independent knowledge-and-AI histories read are S12 (Sowa), S13 (AI100, drawn from Nilsson), S14 (Hitzler), S15 (Shadbolt) and S22 (Feigenbaum).
2. **Most "periodisations" are the authors' own choice.** S3 says so ("blurry boundaries"), S14 says "subjective timeline", S2 says its phase boundaries are "the author's judgement". No source read gives a single scheme covering all four threads.

## 1. Sources read

| # | Source | URL | Read UTC | Depth |
|---|---|---|---|---|
| S1 | Archive lead: `kb-kg/primer/README.md` (pre-LLM lineage, 21 numbered sources) | local file in the worktree | 20261102 19:22 | full text (local file) |
| S2 | Archive lead: `kb-kg/llm-era/README.md` (2020-2026; section 1 has 7 phases) | local file in the worktree | 20261102 19:22 | full text (local file) |
| S3 | Gutierrez and Sequeda, "Knowledge Graphs", *CACM* 64(3):96-104, March 2021 (DOI 10.1145/3418294) | https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf | 20261102 19:24 | full text (9 pages) |
| S4 | Hogan et al., "Knowledge Graphs", arXiv 2003.02320 v6 (11 Sep 2021); *ACM Computing Surveys* 54(4) | https://arxiv.org/pdf/2003.02320v6 | 20261102 19:27 | full text (135 pages); Intro, sections 10 and 11, Appendix A read in full, rest searched |
| S5 | Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey", arXiv 2312.10997 v5 (27 Mar 2024) | https://arxiv.org/pdf/2312.10997 | 20261102 19:28 | full text (21 pages); Intro, sections II, VII, VIII read |
| S6 | Hu et al., "Memory in the Age of AI Agents", arXiv 2512.13564 v2 (13 Jan 2026) | https://arxiv.org/pdf/2512.13564 | 20261102 19:29 | full text (107 pages); abstract, section 1, section 2.3 read, rest searched |
| S7 | Stonebraker and Pavlo, "What Goes Around Comes Around... And Around...", *SIGMOD Record* 53(2), June 2024 | https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf | 20261102 19:30 | full text (17 pages); all data-model sections read |
| S8 | Codd, "A Relational Model of Data for Large Shared Data Banks", *CACM* 13(6), June 1970 | https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf | 20261102 19:30 | full text (11 pages); abstract and sections 1.1-1.2 read |
| S9 | Sanderson and Croft, "The History of Information Retrieval Research", *Proc. IEEE* 100, May 2012 (author manuscript; still has the draft marker "BM25 (Robertson et al, 199?)") | https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 | 20261102 19:30 | full text (10 pages) |
| S10 | Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking: BERT and Beyond", arXiv 2010.06467 v3 (19 Aug 2021) | https://arxiv.org/pdf/2010.06467 | 20261102 19:30 | full text (204 pages); abstract, section 1.2 (history), opening of section 5 read |
| S11 | McCarthy, Minsky, Rochester, Shannon, "A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence", 31 Aug 1955 | http://jmc.stanford.edu/articles/dartmouth/dartmouth.pdf | 20261102 19:32 | full text (13 pages); first page read |
| S12 | Sowa, "Semantic Networks" (updated from the 1987/1992 encyclopedia article; no revision date on the page) | https://www.jfsowa.com/pubs/semnet.htm | 20261102 19:31 | WebFetch extraction (secondary processing of a primary page) |
| S13 | Stanford AI100 (2016), Appendix I "A Short History of AI" ("based primarily on Nilsson's book") | https://ai100.stanford.edu/2016-report/appendix-i-short-history-ai | 20261102 19:34 | full text of the appendix (raw HTML) |
| S14 | Hitzler, "A Review of the Semantic Web Field", *CACM* 64(2), Feb 2021 (text read is the April 2020 author's version) | https://par.nsf.gov/servlets/purl/10292869 | 20261102 19:35 | full text (7 pages) |
| S15 | Shadbolt, "Expert systems - a natural history", in *Research and Development in Expert Systems VI*, Proc. Expert Systems 89, 20-22 Sep 1989 | https://eprints.soton.ac.uk/252374/1/A_Natural_History_of_Expert_Systems_1989.pdf | 20261102 19:36 | full text (13 pages) |
| S16 | W3C documents (a to o below) | see below | 20261102 19:36 to 19:43 | status block of each page only |
| S17 | Singhal, "Introducing the Knowledge Graph: things, not strings", Google blog | https://blog.google/products/search/introducing-knowledge-graph-things-not/ | 20261102 19:37 | WebFetch extraction (primary page) |
| S18 | Singh et al., "Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG", arXiv 2501.09136 v4 (1 Apr 2026) | https://arxiv.org/abs/2501.09136 (read through the alphaXiv PDF tool) | 20261102 19:38 | full text of pages 1-8, 29, 32, 36 |
| S19 | Pan et al., "Unifying Large Language Models and Knowledge Graphs: A Roadmap", arXiv 2306.08302 v3 (25 Jan 2024) | https://arxiv.org/abs/2306.08302 (read through the alphaXiv PDF tool) | 20261102 19:38 | full text of pages 1-2, 5-7, 21, 28 |
| S20 | arXiv API records (version-1 `published` dates, titles, abstract start) for 28 papers | http://export.arxiv.org/api/query?id_list=... (two calls) | 20261102 19:38 and 19:41 | API record (abstract only) |
| S21 | GQL standards committee page | https://www.gqlstandards.org/ | 20261102 19:39 | WebFetch extraction |
| S22 | Feigenbaum, "The Art of Artificial Intelligence: I. Themes and case studies of knowledge engineering", IJCAI-77 vol. 2 | https://www.ijcai.org/Proceedings/77-2/Papers/092.pdf | 20261102 19:39 | full text (16 pages); introduction and sections 2-3 read |
| S23 | Angles and Gutierrez, "Survey of Graph Database Models", *ACM Computing Surveys* 40(1), Feb 2008 | https://users.dcc.uchile.cl/~cgutierr/papers/surveyGDB.pdf | 20261102 19:39 | abstract and first page read (39 pages) |

W3C documents (S16), status block read on 20261102:

| # | Document | URL | Status line as read |
|---|---|---|---|
| S16a | RDF Model and Syntax Specification | https://www.w3.org/TR/1999/REC-rdf-syntax-19990222/ | W3C Recommendation 22 February 1999 (WebFetch extraction; page does not say it is superseded) |
| S16b | RDF: Concepts and Abstract Syntax (RDF 1.0) | https://www.w3.org/TR/rdf10-concepts/ | W3C Recommendation 10 February 2004; "New Version Available: RDF 1.1" |
| S16c | OWL Web Ontology Language Overview | https://www.w3.org/TR/2004/REC-owl-features-20040210/ | W3C Recommendation 10 February 2004; "New Version Available: OWL 2 (12 November 2009)" |
| S16d | SPARQL Query Language for RDF | https://www.w3.org/TR/rdf-sparql-query/ | W3C Recommendation 15 January 2008; "New Version Available: SPARQL 1.1 (26 March 2013)" |
| S16e | SKOS Reference | https://www.w3.org/TR/skos-reference/ | W3C Recommendation 18 August 2009 |
| S16f | OWL 2 Document Overview (Second Edition) | https://www.w3.org/TR/owl2-overview/ | W3C Recommendation 11 December 2012; refers to "the Recommendation of 27 October 2009" |
| S16g | SPARQL 1.1 Query Language | https://www.w3.org/TR/sparql11-query/ | W3C Recommendation 21 March 2013 |
| S16h | RDF 1.1 Concepts and Abstract Syntax | https://www.w3.org/TR/rdf11-concepts/ | W3C Recommendation 25 February 2014 |
| S16i | JSON-LD 1.1 | https://www.w3.org/TR/json-ld11/ | W3C Recommendation 16 July 2020; previous Recommendation JSON-LD 1.0 of 16 January 2014 |
| S16j | SHACL | https://www.w3.org/TR/shacl/ | W3C Recommendation 20 July 2017 |
| S16k | RDF 1.2 Concepts and Abstract Data Model | https://www.w3.org/TR/rdf12-concepts/ | W3C Candidate Recommendation Snapshot, 07 April 2026 (raw HTML); "Latest Recommendation" is RDF 1.1 |
| S16l | SPARQL 1.2 Query Language | https://www.w3.org/TR/sparql12-query/ | W3C Working Draft, 01 November 2026 (raw HTML); "Latest Recommendation" is SPARQL 1.1 of 21 March 2013 |
| S16m | SHACL 1.2 Core | https://www.w3.org/TR/shacl12-core/ | W3C Working Draft, 02 November 2026 (raw HTML); "Latest Recommendation" is SHACL of 20 July 2017 |
| S16n | W3C Semantic Web Activity page | https://www.w3.org/2001/sw/ | "this Activity has been subsumed, in December 2013, by the W3C Data Activity"; page frozen 11 December 2013 (WebFetch extraction) |
| S16o | Berners-Lee, Linked Data (Design Issues) | https://www.w3.org/DesignIssues/LinkedData.html | Created 2006-07-27; last changed 2009-06-18 (WebFetch extraction) |

Tried and not reached (see section 5): Nilsson's *The Quest for Artificial Intelligence* (connection refused), Buchanan 2005 in *AI Magazine* and AAAI pages (bot wall), ISO catalogue pages (HTTP 403), OpenAI's ChatGPT page (HTTP 403), Wikidata:History (HTTP 404), the CIKM 2020 tutorial PDF by Gutierrez and Sequeda (the repository link returned an HTML stub).

## 2. Per-source periodisation

### S1 Archive primer (lead)
- **Periodisation.** The text says "three overlapping stretches stand out" and then lists four: (1) up to the 1980s, "how to write knowledge down" (networks, frames, logics, rule bases, Cyc); (2) 1999 to 2008, W3C RDF, OWL, SPARQL and the Linked Data rules; (3) 2007 to 2014, large graphs (DBpedia, Freebase, Google KG, Wikidata, Knowledge Vault; Neo4j on the property-graph side); (4) learning methods (TransE 2013) and retrieval-augmented language models (2020) "come last". The boundaries are the author's reading of its own timeline table; no source is cited for them.
- **Looks authoritative:** Hogan et al. (S4; my read confirms every use the primer makes of it, including the 1972 versus 1973 discrepancy); the W3C pages (I re-checked 19990222, 20040210, 20080115 and the Linked Data note created 20060727: all match); Google's 20120516 post (re-checked); arXiv dates for REALM (20200210) and RAG (20200522) (re-checked in S20).
- **Weaker:** Wikipedia for the Wikidata launch date (tertiary; the primer says so); InfoQ and a Neo4j blog for Neo4j 1.0 (secondary and vendor); the Lenat 1985 and Noy 2019 entries (bibliographic records with abstracts only); the MYCIN book (contents page only). The primer marks all of these itself.

### S2 Archive llm-era (lead)
- **Periodisation (7 phases, "the author's judgement ... not a date the sources state"):** (1) 20200522 to 20221231 retrieval attached to language models; (2) 20230101 to 20231231 agents and memory-as-a-system; (3) 2024 graph-based RAG and the protocol (MCP 20241125); (4) 20250101 to 20250928 cost correction, then agent memory; (5) 20250929 to 20251231 files, skills and standards; (6) 20260101 to 20260727 code graphs and the LLM wiki; (7) 20260728 to 20261030 consolidation and commercialisation.
- **Looks authoritative:** arXiv `published` dates (primary; I re-verified 17 of them in S20, all matched); GitHub `created_at` dates (primary for the repository, not for the idea); vendor posts and specification changelogs (primary but self-reported).
- **Weaker:** README claims, star counts, one news item (BetaKit) and one commentary (Willison). Every phase boundary from 2024 onward is set by repository, vendor and protocol events, not by a survey. Phases 4 to 7 (20250101 onward) rest almost entirely on vendor and repository material.

### S3 Gutierrez and Sequeda (2021): explicit scheme, five periods
Quote on method: "For pedagogical considerations, we periodized the relevant ideas, techniques, and systems into five themes: Advent, Foundations, Coming-of-Age, Web Era, and Large Scale." And: "They follow a timeline, although with blurry boundaries." Scope: "developments after the advent of computing in its modern sense (1950s)". Each period is split into data, knowledge and data+knowledge, and ends with "realizations" and "limitations".

| Period (section title) | Span as printed | Opening sentence (closest thing to a stated boundary reason) | Events, systems, ideas placed in it |
|---|---|---|---|
| Advent of the Digital Age | none printed; dates cited run 1956 to 1968 (inference) | "The beginnings are marked by the advent and spread of digital computers and the first programming languages" | Logic Theorist 1956, GPS 1958; Richens semantic networks 1956; Quillian 1963/1967; Dijkstra 1956, A* 1968; IDS (Bachman) 1963; COBOL 1959; Raphael SIR 1964 |
| Data and Knowledge Foundations | "The 1970s" | "The 1970s witnessed much wider adoption of computing in industry." | Codd 1970; Chen ER 1976; System R and INGRES 1976 (to SQL); Woods 1975 critique; Minsky frames 1974; Sowa conceptual graphs 1976; Hayes 1977; Kowalski/Prolog; MYCIN; 1977 Toulouse workshop "Logic and Data Bases" |
| Coming-of-Age of Data and Knowledge | "The 1980s" | "The 1980s saw the evolution of computing as it transitioned from industry to homes through the boom of personal computers." | object-oriented DBs; description logics (Brachman and Levesque tractability paper 1984; KL-ONE, LOOM, CLASSIC); F-logic; Japanese 5th Generation; MCC and Cyc; expert systems (OPS5, Rete, XCON); deductive DBs (Datalog, LDL); Bakker thesis "Knowledge Graphs" at the end of the decade; "AI Winter" |
| Data, Knowledge, and the Web | "The 1990s" | "The 1990s witnessed two phenomena that would change the world." (the Web; digitisation) | semistructured data (OEM, XML, RDF); mediators and wrappers; warehouses, OLAP, data mining; knowledge acquisition bottleneck, then knowledge and ontology engineering; Gruber's ontology definition; Ontolingua, Protege; SHOE, OIL, DAML, KQML |
| Data and Knowledge at Large Scale | "The 2000s", running to 2012 and "Where Are We Now?" | "The 2000s saw the explosion of e-commerce and online social networks" | MapReduce, Bigtable, Dynamo, NoSQL; Semantic Web 2001; OWL 2004; RDF, OWL, SPARQL; Linked Data 2006; LOD, DBpedia, Freebase, Wikidata; schema.org 2011; deep learning 2012; Google KG 2012 |

- **No explicit reason is given for any boundary.** The "limitations" lists come closest: Advent (hardware limits; gap between graphs and sequential code); Foundations (rigid data structures, which "gave rise to object-oriented and graph data structures"; weak logic for common knowledge, "the motive of the rise of description logics"); Coming-of-Age (negation hard; "reasoning at large scale was an insurmountable problem", the "knowledge acquisition bottleneck"); Web Era (compute too small; pure logical techniques have "complexity bounds"); Large Scale (little known on integrating logical and statistical methods; neural networks opaque).
- Selected statements for marks: "At the beginning of the 1990s, expert systems proved expensive and difficult to update and maintain." ... "Thus the IT world moved on and rolled that experience into mainstream IT tools" (absorbed). "its original impressive list of goals had not been met. Funding dried out and these factors led to what has been called an AI Winter." "The term did not permeate widely until the second decade of the next century." "Today we are seeing a convergence of statistical and logical methods, with the former temporarily overshadowing the latter in the public eye." "today the notion of Knowledge Graph can be considered, more than a precise notion or system, an evolving project and a vision."
- **Reading note.** Its period 5 holds both the Semantic Web (2001 to 2008) and the 2012 Google launch. It does not treat 2012 as a period boundary. Its online appendix of extended references (dl.acm.org/doi/10.1145/3418294) was not fetched.

### S4 Hogan et al. (2021): no era scheme; a historical appendix
Appendix A has three parts: A.1 Historical Perspective, A.2 "Knowledge Graphs": Pre 2012, A.3 "Knowledge Graphs": 2012 Onwards. The only explicit boundary is the second: "this announcement by Google was a watershed moment in terms of adopting the phrase 'knowledge graph'." The implicit sequence in A.1:
1. Diagrams as reasoning aids, "going back at least to Aristotle (~350 BC)"; Sylvester 1878, Peirce 1878, Frege 1879.
2. Digital computers: "Ritchens (1956), Quillian (1963), and Travers and Milgram (1969)"; "limitations ... in terms of the poor computational resources available".
3. The 70s: "frames by Minsky (1974), the formalisation of semantic networks by Brachman (1977) and Woods (1975), and the proposal of conceptual graphs by Sowa (1979)". Key notions "still of relevance today" include "combinations of formal (logical) and statistical forms of reasoning".
4. Description Logics "stem from the KL-ONE system proposed by Brachman and Schmolze (1985)" and ALC (1991); they "formed the underpinnings" of OWL; RDF and OWL are "building blocks of the Semantic Web".
- Term history: "the first reference to a 'knowledge graph' of relevance to the modern meaning was in a paper by Schneider (1973)"; the Introduction says "since at least 1972" (an inconsistency inside the paper). Later uses: Rada 1986, Bakker 1987, Stokman and de Vries 1988. "papers from 1970-2000 tend to have worked with small graphs". "The phrase 'knowledge base' was popularised in the 70's (possibly earlier) in the context of rule-based expert systems" (cites Buchanan and Feigenbaum 1978).
- Status cues: the definition "remains contentious"; open KGs "have either emerged from the Semantic Web community, or would later adopt its standards"; challenges "are unlikely to ever be completely 'solved'".

### S14 Hitzler (2021): explicit scheme for the Semantic Web field, three phases
Quote: "we will group the narrative into three overlapping phases, each driven by a key concept, i.e., under this reconstruction the field has shifted its main focus at least twice."

| Phase | Span | Stated reason for the end of the phase | Items placed in it |
|---|---|---|---|
| Ontologies | "the early to mid 2000s" ("For most of the 2000s") | "initial over-hyped expectations on short-term massive breakthrough results gave way, around the mid-2000s, to a more sober perspective"; ontologies "turned out to be often hard to maintain and re-use" | DAML 2000-2006; OIL; OWL 2004 (OWL 2 in 2012); RDF; SPARQL 2008; Gene Ontology 1998; SNOMED CT; RIF (little traction) |
| Linked Data | 2006 to "the early 2010s" | "During the early 2010s, the initial hype about Linked Data began to give way to a more sober perspective." Reason: "shallow non-expressive schemas ... appeared to be a major obstacle to reuseability" | Linked Data 2006; DBpedia; BBC, NYT, Facebook as adopters; SKOS; schema.org 2011; Wikidata 2012 |
| Knowledge Graphs | "In 2012" onward; "was and is still driven by knowledge graphs" | not ended | Google KG; Microsoft, IBM, Facebook, eBay; "mostly a new framing of ideas coming rather directly out of the Semantic Web field" |

- The field's birth: the 2001 *Scientific American* article "arguably marks the birth of the field"; "Declaring any specific point in time as the birth of a field of research is of course debateable at best." Earlier: RDF first draft 1997, DAML 2000.
- Status (2020): "the grand goal of the Semantic Web field ... has not been achieved yet"; the field "most needs, at this stage, is consolidation".
- Hitzler dates two W3C standards by year only: "In 2004 ... OWL became a W3C standard" and "Also in 2004, ... RDF became a W3C standard". W3C's own pages give RDF Model and Syntax as a Recommendation on 19990222 (S16a) and RDF 1.0 Concepts on 20040210 (S16b); his 2004 for RDF is the RDF 1.0 revision.

### S7 Stonebraker and Pavlo (2024): explicit list of data-model movements
The 2005 chapter's list, restated: Hierarchical (IMS) late 1960s and 1970s; Network (CODASYL) 1970s; Relational 1970s and early 1980s; Entity-Relationship 1970s; Extended Relational 1980s; Semantic late 1970s and 1980s; Object-Oriented late 1980s and early 1990s; Object-Relational late 1980s and early 1990s; Semi-structured (XML) late 1990s and 2000s. Added for 2005-2024: MapReduce, key-value, document, column family, text search, array, vector, graph.
- Boundary logic: no era boundaries, but an outcome claim: the relational model with an extendable type system "has dominated all comers"; "SQL absorbed the best ideas from these alternative approaches". Hierarchical and network systems: "relegated ... to legacy maintenance mode and nobody is building new applications on them".
- Authors' stance: strongly pro-relational; their forecasts (vector and graph systems absorbed into SQL systems) are opinion. The 2005 chapter itself was not read; S7 restates its list.

### S9 Sanderson and Croft (2012): IR history by sections
Pre-history (mechanical devices; patents 1891, 1918, Goldberg 1920s-30s; Bush 1945); early computers (1948 to 1950s); 1960s; 1970s; 1980s to mid 1990s; mid 1990s to present.
- Reasons (quotes): "Work in the 1950s established computers as the definitive tool for search." "The 1960s saw a wide range of activities reflecting the move from simply asking if IR was possible on computers to determining means of improving IR systems." Commercial systems stayed Boolean: "This situation didn't change until the early to mid-1990s". Web: "Web search engines started to emerge in late 1993 to cope with this growth." Learning to rank "only became truly effective when more training data became available in web query logs in the 2000s".
- Items: "information retrieval" first used March 1950 (Mooers); Univac 1948; Uniterm and Cleverdon tests; Luhn and Maron-Kuhns ranked retrieval 1957-60; Salton group (Harvard then Cornell), SMART, relevance feedback 1965; idf 1972; vector space model 1975; probability ranking principle 1977; LSI 1990; Porter stemmer 1980; TREC (late 1980s/early 1990s, year **unstated**); PageRank and HITS 1998-99; language models 1998.
- Covers nothing after about 2011; no neural retrieval.

### S10 Lin, Nogueira, Yates (2021): five stages of text ranking
1.2.1 The Beginnings of Text Ranking (Bush 1945; Holmstrom 1948; Luhn 1958; Maron and Kuhns 1960; Salton 1975); 1.2.2 The Challenges of Exact Match (1980s into the 1990s; BM25, Robertson 1994); 1.2.3 The Rise of Learning to Rank ("beginning in the late 1980s", "zenith in the early 2010s"); 1.2.4 The Advent of Deep Learning; 1.2.5 The Arrival of BERT.
- Reasons (quotes): learning to rank "was driven largely by the growth in importance of search engines as indispensable tools for navigating the web". Deep learning: "continuous vector representations freed text retrieval from the bounds of exact term matching". BERT: "BERT arrived on the scene in October 2018"; first text-ranking use "in January 2019"; "With BERT, though, everything changed, nearly overnight." TREC 2019 Deep Learning Track "recognized this as a meaningful distinction that separated two different 'eras'".
- Status (2021): techniques "represent mature techniques. However, there remain many open research questions."

### S5 Gao et al. (2023, v5 2024): two schemes for RAG
Scheme A (by where retrieval enters, no dates): "Initially, RAG's inception coincided with the rise of the Transformer architecture" (pre-training stage); "The subsequent arrival of ChatGPT marked a pivotal moment" (inference stage, "rapid development"); "As research progressed, the enhancement of RAG was no longer limited to the inference stage but began to incorporate more with LLM fine-tuning techniques."
Scheme B (paradigms): Naive RAG ("gained prominence shortly after the widespread adoption of ChatGPT"; index chunks as vectors, retrieve top K, generate), Advanced RAG (pre- and post-retrieval), Modular RAG (new modules: search, memory, routing; adaptive retrieval). Stated reason: "The development of Advanced RAG and Modular RAG is a response to these specific shortcomings in Naive RAG." The ChatGPT date is **unstated** in the paper.
Status (2024): "RAG ... a key technology"; "This has also sparked discussions on whether RAG is still necessary when LLMs are not constrained by context"; "a fully integrated, comprehensive platform concept is still in the future".

### S18 Singh et al. (2025, v4 2026): five paradigms, no dates
Naive, Advanced, Modular, Graph, Agentic RAG, "key stages of development". Stated reason for the last step: traditional pipelines "are typically static and linear"; "These limitations have spurred the integration of agentic intelligence". Status: "the Agentic RAG field remains fragmented, with diverse architectures, inconsistent terminology"; "Agentic RAG should not be viewed as a universal replacement for traditional RAG." **It defines "Naive RAG" differently from S5:** keyword retrieval ("TF-IDF and BM25"), where S5's Naive RAG already uses embeddings and a vector database.

### S19 Pan et al. (2023, v3 2024): a forward-looking roadmap, not a history
Three frameworks (KG-enhanced LLMs, LLM-augmented KGs, synergized LLMs + KGs) and "multiple stages (milestones)" that the authors "envision": stage 1 the first two frameworks; stage 2 synergy; stage 3 graph-structure understanding, multi-modality, knowledge updating. Its method table puts KGLM 2019, REALM 2020 and RAG 2020 under "KG-enhanced LLM inference". Stated need: KGs "are difficult to construct and evolve by nature"; LLMs "fall short of capturing and accessing factual knowledge".

### S6 Hu et al. (2025, v2 2026): taxonomy, with historical remarks; no era scheme
Forms (token-level, parametric, latent), functions (factual, experiential, working), dynamics (formation, evolution, retrieval). Remarks: "the field has also become increasingly fragmented"; "During 2023-2024, the community had no stable or coherent definition" of an LLM agent; works since 2023 called "LLM memory mechanisms" (MemoryBank, MemGPT) "are more appropriately interpreted ... as early instances of agent memory"; "In early formulations the distinction between RAG and agent memory was relatively clear ... However, this boundary has become increasingly blurred". Cognitive-science roots are cited (Atkinson-Shiffrin, Tulving 1972, Squire 2004, Baddeley 2012) but those works were not fetched.

### S13 Stanford AI100 (2016): periods of AI
"officially born and christened" at Dartmouth 1956; "focal areas ... between the 1950s and the 1970s" (search, vision, NLP, robotics, learning, neural networks, expert systems); "by the 1980s ... no significant practical successes"; "The field was forced to take cognizance of these shortcomings in the mid-1980s, since interest in AI began to drop, and funding dried up. Nilsson calls this period the 'AI winter.'"; "resurgence in the nineties"; statistical methods "in the past two decades". Reasons given: too little grounding in the physical world and "an overemphasis on Boolean (True/False) logic, overlooking the need to quantify uncertainty".

### S15 Shadbolt (1989): a contemporary account of expert systems
"The early origins of A.I. systems can themselves be traced back to the mid '50's. Expert systems appeared as a distinct line around the late 70's. However, there is considerable argument about just when and where the divergence took place." Contenders for the first expert system: MYCIN (1973, 1976), DENDRAL (1978 paper), MACSYMA. Then: XCON/R1 1980; EMYCIN 1979/1984, so "The age of the expert system shell had dawned"; BCS specialist group 1980; ICOT 1981; Alvey report 1982 and a 350 million pound programme; Lighthill report 1973 as a "reverse". Shift in practice: "we have moved from a transfer view of acquisition to a model view". The 1989 view of the future: "embedded expert systems. Such systems will sit within much larger conventional software."

### S22 Feigenbaum (1977), S11 Dartmouth (1955), S8 Codd (1970): primary single events
- S11: "We propose that a 2 month, 10 man study of artificial intelligence be carried out during the summer of 1956 at Dartmouth College".
- S22: DENDRAL began 1965; "DENDRAL was an early herald of AI's shift to the knowledge-based paradigm"; the term: in 1968 Michie called DENDRAL "epistemological engineering", "that I simplified into 'knowledge engineering.'" The paper uses "knowledge base" and "knowledge-based" freely in 1977.
- S8: *CACM* "Volume 13 / Number 6 / June, 1970"; the relational view "appears to be superior in several respects to the graph or network model presently in vogue for non-inferential systems". The paper sits in the CACM "Information Retrieval" department.

### S12 Sowa and S23 Angles and Gutierrez: chronologies
- S12 (WebFetch extraction): "The first published use of the term was in a proposal by Richard Richens (1956)"; Quillian's marker passing 1966; Shapiro's MIND 1971 (to SNePS); Woods 1975; Sowa's conceptual graphs 1976; "Brachman implemented KL-ONE" 1979; Krypton 1983; Pearl's belief networks 1988-2000; UML 1997; "Berners-Lee et al. described the Semantic Web as a large semantic network" 2001. No periods; no replacement claims.
- S23: graph database models "took off in the eighties and early nineties alongside object-oriented models. Their influence gradually died out with the emergence of other database models, in particular geographical, spatial, semistructured, and XML. Recently, the need to manage information with graph-like nature has reestablished the relevance of this area."

## 3. Cross-source comparison

### 3a. Candidate boundary points shared by two or more sources
Listed, not chosen. "Independent?" notes whether the sources share authors (see the two cautions at the top).

| Candidate point | Sources | What each says | Independent? |
|---|---|---|---|
| 1950 to 1956: the field is named and its first formal objects appear | S11, S13, S12, S3, S4, S15, S9 | AI proposal 1955 and workshop 1956 (S11, S13); semantic network term, Richens 1956 (S12, S3, S4); "the mid '50's" (S15); "information retrieval" coined March 1950 (S9); Logic Theorist 1956 (S3) | yes (S3 and S4 aside) |
| 1970 to 1979: formal foundations for data and for representation | S3 (period "the 1970s"), S8, S7, S4, S9, S15, S22 | Codd 1970 (S8, S3; S7: relational 1970s to early 1980s); frames 1974, Woods 1975, Brachman 1977 (S4, S3); idf 1972, vector model 1975, probability ranking 1977 (S9); "Expert systems appeared as a distinct line around the late 70's" (S15); DENDRAL 1965 as the herald of the knowledge-based shift (S22) | yes |
| 1979 to 1985: description logics, expert-system boom | S3, S4, S12, S15, S7, S23 | DL: KL-ONE 1979 (S12), tractability paper 1984 (S3), KL-ONE paper 1985 (S4); shells and funding 1980 to 1982 (S15); S7: extended-relational and semantic movements in the 1980s; S23: graph DB models "took off in the eighties" | yes |
| mid 1980s or about 1990: the expert-system and 5th Generation bust | S13, S3 (S15 as a before-picture) | S13: "mid-1980s ... funding dried up"; S3: "At the beginning of the 1990s" and "A decade after the start of the Japanese 5th Generation project". **Same event, dates about five years apart.** S15 (1989) still describes growth and a coming "second generation" | yes |
| 1993 to 1997: the Web enters data and search | S9, S3, S7, S14 | web search engines "late 1993" (S9); Web Era = 1990s (S3); semi-structured data late 1990s (S7); first RDF draft 1997 (S14) | yes |
| 2001: Semantic Web as a named project | S14, S3, S12 | "arguably marks the birth of the field" (S14); *Scientific American* May 2001 sits in S3's last period; S12 also dates it 2001 | yes |
| 2004: OWL and RDF 1.0 | S14, S3, S16b, S16c | W3C Recommendations 20040210 (S16); S14 and S3 say 2004 | yes |
| 2006: Linked Data | S3, S14, S16o | design note created 20060727 (S16o); S3 and S14 say 2006 | S3, S14 yes |
| 2008: SPARQL | S14, S16d, S3 | W3C Recommendation 20080115 | yes |
| 2011 to 2012: schema.org, Google KG, Wikidata, deep learning | S3, S4, S14, S17 | schema.org 2011 (S3, S14); Google KG 20120516 (S17; S4: "watershed moment"; S14: third phase begins); Wikidata 2012 (S14); deep learning "2012" (S3) | S3 and S4 share authors; S14 and S17 independent |
| 2018 to 2020: pretrained transformers and retrieval-augmented generation | S10, S5, S19, S20 | BERT 20181011, BERT re-ranking January 2019 (S10, S20); REALM 20200210, RAG 20200522 (S19 table, S20, S5 reference list); S5: RAG's inception "coincided with the rise of the Transformer architecture" | yes |
| late 2022: ChatGPT | S5, S7, S2 (S6 weakly) | "pivotal moment" (S5); "mainstream ... in late 2022" (S7); S2 ends its phase 1 on 20221231; S6 dates its "LLM memory" works "Since 2023" and says 2023-2024 had no stable agent definition. The exact ChatGPT date is **unstated** in S5, S6, S7 | yes |

Points where only one source speaks (so not shared): the mid-2000s ontology to Linked Data shift (S14 only); the early-2010s Linked Data to KG shift (S14 only; S3 and S4 treat 2012 as a milestone, not a boundary); the 2009 data-warehouse versus Hadoop study (S7 only); the pre-BERT versus BERT "two eras" (S10 only, citing the TREC organisers).

### 3b. Where the sources differ

| Topic | Disagreement | Sources |
|---|---|---|
| When the expert-system boom ended | mid-1980s (AI winter) versus beginning of the 1990s (systems "expensive and difficult to update"); S15 (1989) still describes the boom as growing | S13, S3, S15 |
| First use of "knowledge graph" | 1972 (Intro) versus 1973 (Appendix A) inside S4; Bakker's thesis, end of the 1980s, as "the first systematic study with the term" (S3); "modern incarnation" from 2012 (S4); "did not permeate widely until the second decade of the next century" (S3) | S4, S3 |
| Date of the first RDF standard | 1999 (W3C Recommendation, RDF Model and Syntax) versus "Also in 2004" (S14) | S16a, S16b, S14 |
| Date of KL-ONE and description logics | KL-ONE implemented 1979 (S12), tractability paper 1984 (S3), "KL-ONE system proposed by Brachman and Schmolze (1985)" (S4) | S12, S3, S4 |
| Date of conceptual graphs | 1976 (S3, S12) versus 1979 (S4) | S3, S12, S4 |
| Start year of Cyc | "since 1986" (S4); the archive's abstract is the 1985 paper (S1); the start year is **unstated** in any page fetched here | S4, S1 |
| What "Naive RAG" means | embeddings and a vector database (S5) versus keyword retrieval with TF-IDF and BM25 (S18). The same word names different technology in two surveys (2024, 2026) | S5, S18 |
| Whether sparse retrieval was replaced by dense | "Inverted index-centric search engines ... have been supplanted in recent years by similarity search using ML-generated embeddings" (S7) versus BM25 "still provides the starting point of many text ranking approaches today" (S10, 2021) and hybrid sparse-plus-dense in Modular RAG (S5, S18) | S7, S10, S5, S18 |
| Fate of graph databases | rise, decline, revival (S23); "golden years" in the 1980s-90s (S3); "We do not expect specialized graph DBMSs to be a large market" (S7); property-graph standards GQL 2024 and SQL/PGQ 2023 (S21, S7) | S23, S3, S7, S21 |
| Whether ontologies "worked" | ontologies hard to maintain and re-use, shift to Linked Data (S14) versus Description Logics "become the underpinning to OWL" (S3) and SNOMED CT "fully formalized in OWL" (S14) | S14, S3 |
| Where the Semantic Web ends and KG begins | "mostly a new framing of ideas" (S14) and "a reincarnation of the Semantic Web, and Linked Data" (S3) versus a KG defined without any ontology or reasoner (S4's inclusive definition) | S14, S3, S4 |
| Archive's boundary at 1999 | S1 starts its standards stretch at RDF 19990222; S14 starts the field "from the early 2000s" and treats 1997-1999 as earlier efforts; S3 places RDF, OWL and the Semantic Web in its 2000s period, not the 1990s one | S1, S14, S3 |
| Archive's phases inside 2020-2026 | The seven phases in S2 are set by repositories, vendor posts and protocol revisions. No survey read gives dated phases for 2020-2026 (S5 and S18 give paradigms without dates; S19's stages are future) | S2, S5, S18, S19 |

## 4. Milestones per thread

Marks. **settled** = a standard exists, or the idea was absorbed into common practice, or a successor replaced it (the evidence cell says which). **moving** = the source calls it changing, fragmented, or only a draft. **borderline** = evidence on both sides, listed, not decided. **unstated** = no source read speaks to its status. Thread codes: KB/KG main; ONTO ontologies and the semantic web; DB/IR databases and search; RAG/MEM RAG and agent memory.

### 4.1 Main thread: KB/KG

| Date | Event | Thread | Mark | Evidence | Source |
|---|---|---|---|---|---|
| 19550831; summer 1956 | Dartmouth proposal and workshop name "artificial intelligence" | KB/KG | settled | a named field with a research community; AI100: "officially born and christened" | S11, S13 |
| 1956 | Richens: first published use of "semantic network" (per Sowa); Logic Theorist | KB/KG | settled (replaced by successors) | semantic networks "have no well-defined semantics" (Sowa 1987, quoted in S4); successors named: frames, description logics, OWL | S12, S3, S4 |
| 1963; 1966; 1967 | Quillian: notation paper 1963 (S3, S4); marker passing 1966 (S12); dissertation 1967 (S3) | KB/KG | settled (absorbed into graph KR) | S4 lists "knowledge representation through diagrams (specifically graphs)" among notions "still of relevance today" | S3, S4, S12 |
| 1965 | DENDRAL begins at Stanford | KB/KG | settled | S22: "an early herald of AI's shift to the knowledge-based paradigm" | S22 |
| 1968 (remark); 1977 (print) | "knowledge engineering" named (Michie's "epistemological engineering", simplified by Feigenbaum) | KB/KG | settled | term used throughout S15 (1989) and S3 | S22, S15, S3 |
| 1973; 1976 | MYCIN papers (Shortliffe et al.) | KB/KG | settled (absorbed) | S15: "Many would regard MYCIN ... as the first and original expert system"; absorption evidence in the 1980s rows below | S15 |
| 1974 | Minsky's frames memo | KB/KG | settled (absorbed) | S3: formalised in logic (Hayes 1977), leading to description logics; S4: DLs are "direct predecessors" | S3, S4 |
| 1975 | Woods, "What's in a Link": critique of semantic networks | KB/KG | settled | S3: "weak logical foundation", and researchers "focused on extending semantic networks with formal semantics" | S3, S4 |
| 1976 or 1979 | Sowa's conceptual graphs | KB/KG | unstated | no source read says what became of them | S3, S12, S4 |
| 1979, 1984, 1985 | Description logics (KL-ONE; tractability result) | KB/KG, ONTO | settled (standard) | OWL, W3C Recommendation 20040210 (S16c), is based on a description logic (S14) | S12, S3, S4, S16c |
| 1980 | XCON/R1 at DEC | KB/KG | settled (absorbed) | S15: "considered one of the most successful in the history of expert systems"; S3: experience "rolled ... into mainstream IT tools" | S15, S3 |
| 1980 to 1989 | Expert-system boom: shells, UK and EU programmes, 5th Generation | KB/KG | settled (replaced / absorbed); end date disputed | S13: "mid-1980s ... interest in AI began to drop, and funding dried up"; S3: expert systems "brittle", 5th Generation goals "had not been met" | S15, S13, S3 |
| 1985 (S1 abstract paper) / "since 1986" (S4); start year unstated | Cyc at MCC | KB/KG | borderline | for: S4 (2021) still lists Cyc among open KGs ("2.2 million facts and rules"). Against / silent: no source read says it became a standard; S3 gives its aim as "the world's largest knowledge base of common sense" without an outcome | S4, S3, S1 |
| 1986 to 1989 | "knowledge graph" used in other senses (Rada 1986; Bakker 1987, "the first systematic study with the term" per S3; Stokman and de Vries 1988) | KB/KG | borderline | for: the term existed for decades (S4); against: "did not permeate widely until the second decade of the next century" (S3) | S4, S3 |
| 2010; 201503 | Freebase acquired by Google (2010); read-only March 2015; content migrated to Wikidata | KB/KG | settled (replaced by successor) | "Much of this content was subsequently migrated to Wikidata" | S4 |
| 20120516 | Google announces its Knowledge Graph ("more than 500 million objects ... 3.5 billion facts") | KB/KG | settled (the term entered common use) | "a watershed moment in terms of adopting the phrase" (S4); third Semantic Web phase (S14) | S17, S4, S14, S3 |
| 2012 (day **unstated** in primary pages read) | Wikidata launches | KB/KG | settled | "has received broad adoption", used by Wikipedia, supported by Google (S4); "over 66 million data items" (S14, 2020) | S14, S4 |
| 2019 | Industry-scale KGs (Noy et al., summarised in S4): six common trends | KB/KG | borderline | for: broad industry uptake (S4); against: "no published formal evaluation of their benefits" (S14); definition "remains contentious" (S4) | S4, S14 |
| 2021 | Three 2021 reviews describe KG as unsettled | KB/KG | moving | "an evolving project and a vision" (S3); "remains contentious" (S4); needs "consolidation" (S14) | S3, S4, S14 |
| 20230614 | LLM + KG roadmap (three frameworks) | KB/KG | moving | "forward-looking roadmap"; the stages are anticipated | S19, S20 |

### 4.2 Side thread: ONTO (ontologies and the semantic web)

| Date | Event | Thread | Mark | Evidence | Source |
|---|---|---|---|---|---|
| 1993 | Ontology defined as an explicit, shared specification of a conceptualisation (S14 cites "a many-cited source from 1993"; S3 cites Gruber 1995) | ONTO | settled | became the central notion of the field "for most of the 2000s" (S14); an ontology is "really a knowledge base" in symbolic AI (S14) | S14, S3 |
| 19971002 | First RDF working draft | ONTO | settled (superseded) | URL in S14 footnote; later Recommendations | S14 |
| 19990222 | RDF Model and Syntax: W3C Recommendation | ONTO | settled (superseded in practice by RDF 1.0 and 1.1) | S16a; S16b says RDF 1.1 is the new version | S16a, S16b |
| 2000 to 2006 | DAML program, OIL, DAML+OIL, leading to OWL | ONTO | settled | OWL Recommendation 20040210 | S14, S3, S16c |
| 200105 | "The Semantic Web", *Scientific American* | ONTO | settled (as the field's start) | "arguably marks the birth of the field" | S14, S3 |
| 20040210 | OWL (1.0) and RDF 1.0 Concepts: W3C Recommendations | ONTO | settled | S16b and S16c; later versions exist: OWL 2, RDF 1.1 | S16b, S16c |
| mid-2000s | Ontology-centred phase ends: "over-hyped expectations ... gave way ... to a more sober perspective" | ONTO | settled (phase over) | S14; RIF's "relatively little traction" supports it | S14 |
| 20060727 | Linked Data design note (four rules) | ONTO | borderline | for: most open KGs are published as Linked Open Datasets (S4); S14 says Linked Data was a driver "until the early 2010s". Against: "hype began to give way to a more sober perspective"; "shallow non-expressive schemas" hampered reuse (S14) | S16o, S14, S4 |
| 20080115 | SPARQL 1.0: W3C Recommendation | ONTO | settled (superseded by 1.1) | S16d | S16d |
| 20090818 | SKOS: W3C Recommendation | ONTO | settled | S14: SKOS "has gained significant traction" | S16e, S14 |
| 20091027; 20121211 | OWL 2 Recommendation; Second Edition | ONTO | settled | S16f (the page read does not mention a successor) | S16f, S14 |
| not dated in the sources read | Rule Interchange Format (RIF) | ONTO | borderline | for: a W3C standard (S14); against: "gained relatively little traction", citations "two orders of magnitude lower" (S14) | S14 |
| 2011 | schema.org (Bing, Google, Yahoo!, then Yandex) | ONTO, KB/KG | settled (adopted) | "over 30% of pages have Schema.org annotations" (a 2015 report, in S14) | S14, S3 |
| 20130321 | SPARQL 1.1: W3C Recommendation | ONTO | settled (latest Recommendation) | S16g; the 1.2 successor is a Working Draft (S16l) | S16g |
| 201312 | W3C Semantic Web Activity "subsumed ... by the W3C Data Activity" | ONTO | settled (absorbed) | S16n: "That activity has a larger scope." | S16n |
| 20140116; 20200716 | JSON-LD 1.0; JSON-LD 1.1 (W3C Recommendations) | ONTO | settled | S16i; S14: Google's KG API is JSON-LD compliant | S16i, S14 |
| 20140225 | RDF 1.1 Concepts and related: W3C Recommendations | ONTO | settled (latest Recommendation) | S16h; RDF 1.2 is a Candidate Recommendation Snapshot (S16k) | S16h |
| 20170720 | SHACL: W3C Recommendation | ONTO | settled (latest Recommendation) | S16j; SHACL 1.2 Core is a Working Draft (S16m) | S16j |
| 20260407; 20261101; 20261102 | RDF 1.2 Concepts (Candidate Recommendation Snapshot); SPARQL 1.2 Query (Working Draft); SHACL 1.2 Core (Working Draft) | ONTO | moving | each page names the 2013/2014/2017 version as "Latest Recommendation" | S16k, S16l, S16m |
| 2020 | Semantic Web field: "the grand goal ... has not been achieved yet"; needs "consolidation" | ONTO | moving | S14 | S14 |

### 4.3 Side thread: DB/IR (databases and search)

| Date | Event | Thread | Mark | Evidence | Source |
|---|---|---|---|---|---|
| 194507 | Bush, "As We May Think" (memex; S10 footnote: "essentially a graph store!") | DB/IR | settled (conceptual origin) | cited as the earliest motivation by S10 and S9 | S10, S9, S3 |
| 1948 | Royal Society conference: first reference to a computer searching content (Univac) | DB/IR | settled | S9: "the first reference to a computer being used to search for content" | S9 |
| 195003 | Mooers: the term "information retrieval" | DB/IR | settled | S9 | S9 |
| 1957 to 1960 | Ranked retrieval: Luhn; Maron, Kuhns and Ray | DB/IR | settled | ranking beat Boolean in experiments; commercial systems moved "until the early to mid-1990s" (S9); S10: "an important conceptual leap" | S9, S10 |
| 1959; 1963 | COBOL; IDS (Bachman), basis of CODASYL | DB/IR | settled (replaced) | hierarchical and network systems "relegated ... to legacy maintenance mode" (S7) | S3, S7 |
| 1960s | SMART (Salton): vector model, relevance feedback | DB/IR | settled | S7: vector space model "now nearly universal in modern search engines" | S9, S7 |
| 197006 | Codd's relational model | DB/IR | settled | S7: the relational model "has dominated all comers"; SQL "absorbed the best ideas" | S8, S7, S3 |
| 1972; 1975; 1977 | idf; vector space model; probability ranking principle | DB/IR | settled | S9: the vector view "is still common" although Salton's formulas "are rarely used" | S9 |
| 1976 | System R, INGRES, then SQL; Chen's ER model | DB/IR | settled | S3: SQL is "the most successful declarative query language in existence" | S3 |
| 1980s to early 1990s | Graph database models "took off", "died out", then revived | DB/IR | borderline | for: renewed need for graph-like data (S23, 2008); property-graph standards SQL/PGQ and GQL (S7, S21). Against: "We do not expect specialized graph DBMSs to be a large market" (S7) | S23, S7, S21 |
| late 1980s / early 1990s | TREC formed | DB/IR | settled | S9; still running with a 2019 Deep Learning Track (S10) | S9, S10 |
| late 1980s to early 2010s | Learning to rank | DB/IR | settled (replaced) | "zenith in the early 2010s, on the eve of the deep learning revolution" (S10) | S10, S9 |
| 1993; 1994 | Web search engines (JumpStation late 1993; WebCrawler 1994); commercial move from Boolean to ranked search in the early to mid 1990s | DB/IR | settled | S9 | S9 |
| 1994 | Okapi BM25 | DB/IR | settled | "still provides the starting point of many text ranking approaches today" (S10) | S10 |
| 1998 | PageRank (Brin and Page); HITS 1999 | DB/IR | settled | S9 | S9 |
| 2003 to 2005 | MapReduce (2003); Hadoop (2005); 2009 study favouring warehouse DBMSs | DB/IR | settled (replaced) | "They died years ago and are, at best, a legacy technology at present." (S7) | S7 |
| late 2000s | NoSQL: Bigtable, Dynamo, CouchDB, MongoDB | DB/IR | borderline | for: "(re-)popularized" column, document, key-value and graph stores (S3). Against / absorbed: "on a collision course with RDBMSs"; many "now expose a SQL-like interface" (S7, one stance) | S3, S7 |
| 20181011; 201901 | BERT; first BERT use for text ranking | DB/IR | settled (replaced pre-BERT neural ranking) | "With BERT, though, everything changed, nearly overnight." (S10); arXiv date of BERT re-ranking 20190113 (S20) | S10, S20 |
| 20200410 | Dense Passage Retrieval (arXiv v1) | DB/IR, RAG/MEM | borderline | for: dense retrieval "mature" (S10, 2021), used in Advanced RAG (S18). Against: "many open research questions" (S10); hybrid sparse plus dense in Modular RAG (S5, S18); S7 says embeddings have supplanted inverted-index search | S20, S10, S7, S5, S18 |
| 2023 | Major RDBMSs add vector indexes; vector DBMSs draw attention | DB/IR | moving | S7: "less than one year" after ChatGPT; vector DBMSs "essentially document-oriented DBMSs with specialized ANN indexes"; forecast: absorbed into relational systems | S7 |
| 2023 | SQL:2023 adds SQL/PGQ (property graph queries) | DB/IR | settled (standard) | S7; S21 lists "9075-16 SQL/PGQ" in a 2022 ballot; a publication date for 9075-16 itself is **unstated** in S21 | S7, S21 |
| 20240417 | GQL: ISO/IEC 39075:2024 "officially published" | DB/IR | settled (standard published; uptake **unstated**) | S21: "April 17, 2024 - The GQL Standard is published!" | S21 |

### 4.4 Side thread: RAG/MEM (RAG and agent memory)

| Date | Event | Thread | Mark | Evidence | Source |
|---|---|---|---|---|---|
| 20170612 | "Attention Is All You Need" (arXiv v1) | RAG/MEM | settled | S5: "RAG's inception coincided with the rise of the Transformer architecture" | S20, S5 |
| 20181011 | BERT (arXiv v1) | RAG/MEM, DB/IR | settled | see DB/IR row | S20, S10 |
| 20200210 | REALM (arXiv v1) | RAG/MEM | settled (origin) | listed with RAG under retrieval-augmented fusion (S19) | S20, S19 |
| 20200522 | RAG (Lewis et al., arXiv v1; NeurIPS 2020) | RAG/MEM | settled (origin of the term) | S5 reference [4] | S20, S5 |
| late 2022 | ChatGPT as the turning point for RAG practice | RAG/MEM | settled (as a boundary in two sources); exact date **unstated** | S5: "pivotal moment"; Naive RAG "gained prominence shortly after the widespread adoption of ChatGPT"; S7: "late 2022" | S5, S7 |
| 20221006 | ReAct (arXiv v1) | RAG/MEM | moving | S2 read only the title; no survey read speaks to it | S20, S2 |
| 20231012; 20231017 | MemGPT; Self-RAG (arXiv v1) | RAG/MEM | moving | S6: MemGPT-type works are "early instances of agent memory"; Self-RAG named among agentic RAG methods (S6, S18) | S20, S6, S18 |
| 20231218 | Gao et al.: Naive, Advanced, Modular RAG | RAG/MEM | borderline | for: the three-paradigm scheme is reused in S18. Against: S18 changes what "Naive RAG" means and adds Graph and Agentic stages | S5, S18 |
| 20240227; 20241014 | LoCoMo; LongMemEval benchmarks | RAG/MEM | moving | used as the agent-memory benchmarks in S6 | S20, S6 |
| 20240424; 20240523 | GraphRAG paper; HippoRAG | RAG/MEM, KB/KG | moving | S6: HippoRAG "interpreted by both RAG and memory communities"; S18: Graph RAG limits "Limited Scalability", "Data Dependency"; S2: GraphRAG v3.3.0 still shipping 20261008 | S20, S6, S18, S2 |
| 20240815 | Graph RAG survey (Peng et al.) | RAG/MEM | moving | cited by S18 and S6 | S20, S18 |
| 20250115 (v4 20260401) | Agentic RAG survey | RAG/MEM | moving | "remains fragmented"; "not ... a universal replacement" | S18, S20 |
| 20250120 | Zep temporal knowledge graph for agent memory | RAG/MEM | moving | S6 lists Zep as a memory graph | S20, S6 |
| 20250717 | Context Engineering survey | RAG/MEM | moving | S6 says agent memory is "often conflated" with RAG and context engineering | S20, S6 |
| 20251215 (v2 20260113) | "Memory in the Age of AI Agents" | RAG/MEM | moving | "increasingly fragmented"; the RAG boundary "has become increasingly blurred" | S6, S20 |
| 2020 to 2026 | RAG as a practice | RAG/MEM | borderline | for settled: "widespread adoption", "a key technology" (S5); a base layer in S18. Against: RAG versus long context still debated in 2024 (S5); "inconsistent terminology" (S18); boundary with memory "blurred" (S6) | S5, S18, S6 |

The archive's 2024-2026 rows (S2) rest on vendor posts, repositories and protocol revisions. The one standardisation-like event in them is the MCP donation to the Agentic AI Foundation (20251209, vendor-reported). I did not re-read those pages, so no mark is given.

## 5. Gaps: what no source read states

1. **No source gives a periodisation that covers all four threads or the whole span 1950 to 2026.** S3 covers KB/KG from 1950 to 2012; S14 covers the Semantic Web from 2000 to 2020; S9 and S10 cover IR; S7 covers databases; S5, S18 and S6 cover RAG and memory without dates for their stages. Nothing read gives dated phases inside 2020-2026 except the archive's own judgement (S2).
2. **First use of "knowledge base" is unstated.** S4: "popularised in the 70's (possibly earlier)". S22 shows ordinary use by 1977.
3. **Start year of Cyc is unstated in any fetched page.** S4 says "since 1986". The AAAI pages (bot wall) were not readable; a web-search lead gave another year and is not cited.
4. **Sources I could not reach:** Nilsson's book (connection refused; S13 is based on it), Buchanan 2005 in *AI Magazine* (bot wall), AAAI OJS pages (bot wall), ISO standard pages (HTTP 403, so the GQL date rests on the committee page S21), OpenAI's ChatGPT page (HTTP 403, so the ChatGPT release date is **unstated** in fetched pages), Wikidata:History (HTTP 404; Wikidata's launch day is **unstated**, only the year 2012 from S14), the CIKM 2020 history tutorial by Gutierrez and Sequeda, and the ACM online appendix of S3.
5. **When the expert-system bust happened is disputed** (mid-1980s S13 versus about 1990 S3), and no source read gives deployment or market numbers that would settle it.
6. **SQL's standardisation year** (1986/87) was not read from a fetched page. **Neo4j and Cypher origins** were not read beyond the archive's secondary sources and a mention in S7. **The 2005 Stonebraker and Hellerstein chapter** was not read; its list is restated in S7.
7. **Adoption evidence for "settled" is thin.** Only schema.org (over 30% of pages, 2015 report, S14) and Wikidata item counts (S14) are quantified. W3C Recommendation status shows a standard exists, not that it is used (S14 says RIF was not).
8. **Agent-memory history before LLMs** (cognitive architectures such as Soar and ACT-R; Atkinson-Shiffrin, Tulving) is cited in S6 but none of those works was fetched. The CoALA paper (arXiv 2309.02427, 20230905) and the 2024 memory-mechanism survey (arXiv 2404.13501, 20240421) were only checked for dates, not read.
9. **No source read gives the start of the "vector database" as a product category.** S7 gives 2023 for relational systems adding vector indexes.
10. **IR between 2012 and 2018** is covered only by S10 section 1.2.4; S9 stops about 2011.
11. **The settled rule and a standard with a newer draft.** RDF 1.2, SPARQL 1.2 and SHACL 1.2 (2026 drafts) mean the 1.1-era Recommendations stand (settled) while an update is under way (moving); the sources give no rule for that, so the owner's rule has to decide.
12. **Independence.** S3, S4 and S23 share authors, so the "at least three independent sources before 2010" are, for knowledge and AI, S12, S13, S14 (2000-2010), S15 and S22; for databases and search, S7, S9, S10. For KB/KG in the 1970s and 1980s the independent confirmations are S12 (semantic networks, DLs), S15 (expert systems), S22 (DENDRAL, knowledge engineering) and S13 (AI winter).
13. **Archive checks that came out clean:** every W3C date and 17 arXiv dates I re-read from S1 and S2 matched the primary page, and S4's own 1972 versus 1973 inconsistency is real.
