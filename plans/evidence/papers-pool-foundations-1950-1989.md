# Foundations 1950-1989: candidate pool for papers/foundations.md

Researcher: foundations-1 (semantic networks, frames, scripts, production rules and expert systems, knowledge engineering, logic programming, KL-ONE and description logics, Cyc origins, relational and entity-relationship models, foundations of information retrieval).
Written 20261102 19:58 UTC. 30 candidates, strongest first, then "Considered and not proposed".

## How the numbers were read (applies to every section)

- **Citation counts.** Semantic Scholar returned HTTP 429 on every single search between 20261102 19:41 and 19:54 UTC; one batch call by DOI (retried every 60 s) succeeded at **20261102 19:55 UTC** and gave `citationCount` for 36 of the 39 DOIs asked [S11]. Those are the table "Semantic Scholar counts" below (the preferred count). The per-section lines give **OpenAlex** (`cited_by_count`, read 20261102 19:43 UTC for the search results, 19:48 to 19:52 UTC for the by-id lookups) and **Crossref** (`is-referenced-by-count`, read 20261102 19:46 UTC) [S1, S2]; they are the cross-check, and the only counts for the papers that have no DOI (Minsky, Schank and Abelson, Gelfond and Lifschitz, Kowalski, Brachman and Levesque, the two books, Feigenbaum, McCarthy, Woods, Chen at Semantic Scholar).
- The sources differ a lot for some papers (for example KL-ONE: Semantic Scholar 2,146, OpenAlex 1,775, Crossref 128). Crossref only counts references deposited with DOIs, so it is the lower bound. Counts are dated and move. Semantic Scholar sometimes gives a wrong first date for a merged record (Spärck Jones: 2021, Reiter: 1987); the dates in the sections come from Crossref, OpenAlex and the publisher listings, not from Semantic Scholar.

### Semantic Scholar counts (batch call by DOI, read 20261102 19:55 UTC)

| Section | Paper | Semantic Scholar `citationCount` |
|---|---|---|
| 1 | Codd 1970 | 3,675 |
| 2 | Salton, Wong, Yang 1975 | 8,535 |
| 3 | Chen 1976 | no record returned for the DOI; use OpenAlex and Crossref |
| 4 | Salton and Buckley 1988 | 11,575 |
| 5 | Minsky 1974 | not asked (no DOI) |
| 6 | Spärck Jones 1972 | 5,628 |
| 7 | Newell 1982 | 3,073 |
| 8 | Schank and Abelson 1977 | not asked (book) |
| 9 | Gelfond and Lifschitz 1988 | not asked (no DOI) |
| 10 | KL-ONE 1985 | 2,146 |
| 11 | Robertson and Spärck Jones 1976 | 2,560 |
| 12 | Hull and King 1987 | 1,278 |
| 13 | Reiter 1978 | 1,272 |
| 14 | Luhn 1957 | 1,199 |
| 15 | Maron and Kuhns 1960 | 1,036 |
| 16 | Kowalski 1974 | not asked (no DOI) |
| 17 | McCarthy 1958 | not asked (no DOI) |
| 18 | Quillian 1967 | 827 |
| 19 | Buchanan and Shortliffe 1984 | not asked (book) |
| 20 | Gallaire et al. 1984 | 834 |
| 21 | Brachman 1979 | 807 |
| 22 | Woods 1975 | no record returned for the DOI |
| 23 | Brachman and Levesque 1984 | not asked (no DOI) |
| 24 | Brachman and Levesque 1985 | not asked (book) |
| 25 | Cyc 1985 | 406 |
| 26 | SEQUEL 1974 | 763 (and Semantic Scholar's own date for it is 19740501, which agrees with the IBM listing) |
| 27 | Feigenbaum 1977 | not asked (no DOI) |
| 28 | Davis et al. 1977 | 635 |
| 29 | Cleverdon 1967 | 661 |
| 30 | Clancey 1985 | 1,280 |

Considered papers with a Semantic Scholar count from the same call: Collins and Loftus 1975 8,418; Robinson 1965 4,758; Reiter 1980 4,589; Rete 1982 2,924; Lenat 1995 2,476; Doyle 1979 2,147; Codd 1979 1,756; van Emden and Kowalski 1976 1,742; Clark 1978 1,282; Schank 1972 1,120; McDermott and Doyle 1980 1,079; R1 1982 1,030; Datalog 1989 825; Kowalski 1979 712; Robertson 1977 1,188. Not returned: Hayes 1979, Collins and Quillian 1969 (the Sowa 1984 review record: 67, not the book).
- OpenAlex splits many old works into several records (the original, a reprint in an anthology, a later republication). The count given is the record for the original venue. Other records are named and **not summed**.
- **Dates.** "First version" is the original publication; where a source gives only a year, the year is written. Where two sources disagree, both are given.
- **Read depth.** "Abstract" means the abstract text was read from the Crossref or OpenAlex record. "Listing" means only bibliographic metadata was read. "Full text" was **not achieved for any paper**: the publisher pages (ACM, Elsevier, DTIC) returned HTTP 403, and the scanned PDFs (IJCAI, Imperial College) had no text layer that the fetch tool could read. Every "idea" below is therefore from an abstract, a publisher blurb, or a named secondary source; where none was read the section says so.
- Search-engine summaries were used only as leads (one, for SEQUEL, and it was then checked against the IBM Research listing).
- "Archive primer" means `kb-kg/primer/README.md`, whose own sources carry their own read times (20261030 18:59 to 19:02 UTC); facts taken from it are marked "via the archive page".

---

## 1. Codd, "A Relational Model of Data for Large Shared Data Banks" (1970)

- **Authors:** E. F. Codd (1 author). **Venue:** Communications of the ACM [S2]. **Published:** 197006 [S2; S1 gives 19700601].
- **Link:** https://doi.org/10.1145/362384.362685
- **Citations:** OpenAlex 5,549 (record W2185907055; a 1983 republication record has 4,796 more and is not summed), Crossref 5,127; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *origin* - the abstract says "A model based on n-ary relations, a normal form for data base relations, and the concept of a universal data sublanguage are introduced" and criticises tree-structured and network models [S3]. *widely built on* - the counts above.
- **Idea:** Users of large data banks should be protected from knowing the internal representation of the data. Data is modelled as n-ary relations with a normal form and a universal data sublanguage, so that applications survive changes in storage [S3].
- **Relations:** builds on nothing in this pool (it criticises the tree and network models of its day [S3]). Answered by Chen 1976 (section 3), whose abstract proposes a model that unifies "the network model, the relational model, and the entity set model" [S3]. Kowalski 1979 (not proposed, see below) writes that the thesis of a "relational component, which defines the logic of the data, and a control component" has been "successfully argued by Codd" [S3, abstract of 10.1145/359131.359136]. Later era, by topic only: the property-graph model of Neo4j 1.0 (20100225) is the graph-shaped counterpart in the databases thread (via the archive page, primer row 20100225); no source read says it answers Codd.
- **Read:** abstract, 20261102 19:48 UTC. Full text not read.

## 2. Salton, Wong and Yang, "A Vector Space Model for Automatic Indexing" (1975)

- **Authors:** G. Salton, A. Wong, C. S. Yang (3 authors [S2]; OpenAlex lists two [S1]). **Venue:** Communications of the ACM. **Published:** 197511 [S2].
- **Link:** https://doi.org/10.1145/361219.361220
- **Citations:** OpenAlex 7,520, Crossref 5,043; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *origin* - the title names the model; this is the paper the field cites for the vector space model. **Caveat:** the abstract describes documents and requests as entities in an "indexing (property) space", argues the best space is one "where each entity lies as far away from the others as possible", and uses "space density computations" to choose an indexing vocabulary [S3]. It does not mention term weights or cosine similarity. The abstract does not itself say this is the first vector space model; "origin" rests on the title and on the citation pattern, not on a claim in the paper that was read. *widely built on* - counts above.
- **Idea:** Retrieval quality can be studied as a property of the geometry of the document space: a good indexing vocabulary spreads documents apart, and retrieval performance may correlate inversely with space density [S3].
- **Relations:** builds on Spärck Jones 1972 (section 6) only by shared subject (term weighting); the abstracts read do not cite each other. Answered by Salton and Buckley 1988 (section 4), which compares weighting schemes inside this model family (title only; abstract not read). Later era: Deerwester et al. 1990 (latent semantic analysis, 12,758 OpenAlex citations) represents documents as vectors and returns those "with supra-threshold cosine values" [S3, abstract of 10.1002/(sici)1097-4571(199009)41:6<391::aid-asi1>3.0.co;2-9]; it belongs to the 1990+ file.
- **Read:** abstract, 20261102 19:48 UTC.

## 3. Chen, "The Entity-Relationship Model - Toward a Unified View of Data" (1976)

- **Authors:** Peter Pin-Shan Chen (1 author). **Venue:** ACM Transactions on Database Systems. **Published:** 197603 [S2].
- **Link:** https://doi.org/10.1145/320434.320440
- **Citations:** OpenAlex 4,710 (a 2002 reprint record has 5,750 and a second 1976 record 595; not summed), Crossref 4,588; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *origin* - the abstract opens "A data model, called the entity-relationship model, is proposed" and introduces "a special diagrammatic technique" for design [S3]. *widely built on* - counts above.
- **Idea:** A data model that "incorporates some of the important semantic information about the real world", with entities and relationships and a diagram notation for database design. It is offered as a basis for unifying the network, relational and entity-set views of data [S3].
- **Relations:** builds on Codd 1970 (section 1): the abstract names "the relational model" among the views it unifies [S3]. Answered by Codd 1979 "Extending the database relational model to capture more meaning" (not proposed; abstract: "several investigators have been exploring 'semantic models' for formatted databases", the extension is "a synthesis of many ideas from the published work in semantic modeling" [S3]) and surveyed by Hull and King 1987 (section 12).
- **Read:** abstract, 20261102 19:44 UTC (Crossref record via the fetch tool) and 19:48 UTC (OpenAlex).

## 4. Salton and Buckley, "Term-Weighting Approaches in Automatic Text Retrieval" (1988)

- **Authors:** Gerard Salton, Christopher Buckley (2 authors). **Venue:** Information Processing & Management. **Published:** 198801 [S2].
- **Link:** https://doi.org/10.1016/0306-4573(88)90021-0
- **Citations:** OpenAlex 9,814, Crossref 6,576; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *widely built on* - the highest count in this pool. *survey of record*: plausible from the title (a comparison of weighting approaches) but **unstated**: no abstract was available from either API and the publisher page returned HTTP 403. *origin* of the tf-idf formula: **unstated**; no source read says this paper introduced it.
- **Idea:** **Unstated from a source read.** The title says it compares term-weighting approaches for automatic text retrieval. A writer must read the paper before stating its recommended weighting scheme.
- **Relations:** builds on Spärck Jones 1972 (section 6) and Salton, Wong and Yang 1975 (section 2) - **by subject only**; the paper's reference list was not read. Evaluated, much later, by the BM25 line: "BM25 Wins at Scale" (arXiv 2607.26497, v1 20260729, v3 20260731) says in its abstract that "graph-based RAG encounters construction walls before deployment scale and its scalable variants remain below BM25 at shared tiers" [S10]. That page does not explain what BM25 is or link it to Robertson; the lineage from section 13 to BM25 is **unstated** in the sources read.
- **Read:** listing only, 20261102 19:46 UTC.

## 5. Minsky, "A Framework for Representing Knowledge" (1974)

- **Authors:** Marvin Minsky (1 author). **Venue:** MIT AI Laboratory Memo 306 (series AIM-306). **Published:** 19740601 [S4].
- **Link:** https://dspace.mit.edu/handle/1721.1/6089
- **Citations:** no single count. OpenAlex has no record for the memo itself; three republication records exist: 4,535 (1988 anthology chapter, W2175268987), 852 (1979 book chapter, W4230553559), 529 (1997 book chapter, W2121773050) [S1]. They are not summed (the same text, counted in different places).
- **Tests:** *origin* - the DSpace abstract introduces "frames": stored structures for stereotyped situations, with fixed top-level facts and open slots, grouped into frame-systems [S4]. The archive primer calls it the start of structured units in representation (via the archive page, primer row 19740601). *widely built on* - the republication counts above. *turning point*: Hayes and later formalisation work treat frames as a thing to be given semantics (see Woods, section 22), but no source read states that this memo changed the field's direction beyond the primer's sentence.
- **Idea:** Knowledge is organised as frames, each a template for a situation with slots to be filled by specifics and expectations about what comes next; related frames form systems that can represent viewpoints and changes of perspective [S4].
- **Relations:** answered by Woods 1975 and Brachman 1979 (sections 22, 21), which ask what a link or a structured unit means; the archive primer says description logics "were introduced to formalise frames and semantic networks" (via the archive page, primer row 19740601, citing the Hogan survey). Related: Schank and Abelson 1977 (section 8) - scripts as larger structures; no sentence read ties the two directly.
- **Read:** abstract, 20261102 19:44 UTC (and 20261030 19:00 UTC via the archive page).

## 6. Spärck Jones, "A Statistical Interpretation of Term Specificity and Its Application in Retrieval" (1972)

- **Authors:** Karen Spärck Jones (1 author). **Venue:** Journal of Documentation. **Published:** 197201 [S2].
- **Link:** https://doi.org/10.1108/eb026526
- **Citations:** OpenAlex 4,524 (a 2004 reprint record has 503), Crossref 2,892; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *origin* - the abstract argues "terms should be weighted according to collection frequency, so that matches on less frequent, more specific, terms are of greater value" and reports "considerable improvements in performance" with "this very simple procedure" on three test collections [S3]. This is the idea later called inverse document frequency; the abstract does not use that name. *widely built on* - counts above.
- **Idea:** Specificity of an index term should be measured statistically, as a function of how often the term is used in the collection, rather than by its meaning. Weighting rare terms higher improves retrieval [S3].
- **Relations:** answers the idea that exhaustivity and specificity are independent (abstract: "usually regarded as independent") [S3]. Built on by Robertson and Spärck Jones 1976 (section 11): its abstract presents relevance weighting as "a natural extension of weighting methods using information about the distribution of index terms in documents in general" [S3]. Built on, by subject, by Salton and Buckley 1988 (section 4).
- **Read:** abstract, 20261102 19:48 UTC.

## 7. Newell, "The Knowledge Level" (1982)

- **Authors:** Allen Newell (1 author). **Venue:** Artificial Intelligence 18(1) [S2]. **First version:** 198107 as a technical report (the AAAI Presidential Address; OpenAlex record W2083137466, dated 19810701) [S3]; journal 198201 [S2]. The date of the address itself is **unstated** in the records read.
- **Link:** https://doi.org/10.1016/0004-3702(82)90012-1
- **Citations:** OpenAlex 2,589 (journal record W2035346816; the technical report record has 153), Crossref 1,393; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *origin* of the "knowledge level" as a named system level - the report abstract says "the paper proposes a theory of the nature of knowledge, namely, that there is another computer system level immediately above the symbol (or program) level" [S3]. *widely built on* - counts above.
- **Idea:** Knowledge is the medium at a computer-system level above the symbol level, where the principle of rationality governs behaviour; a representation is then something at the symbol level that serves a knowledge-level description [S3, abstract of the technical report; the second clause is the writer's reading of the truncated abstract and must be checked against the full text].
- **Relations:** the abstract names a "recent SIGART special issue on Knowledge Representation edited by Ron Brachman and Brian Smith" as evidence the field needed this work [S3]. Related: Brachman and Levesque's Readings (section 24) is the anthology of the same period.
- **Read:** abstract of the technical-report record, 20261102 19:52 UTC; journal version listing only.

## 8. Schank and Abelson, *Scripts, Plans, Goals and Understanding* (1977)

- **Authors:** Roger C. Schank, Robert P. Abelson (2 authors). **Venue:** book, Lawrence Erlbaum (record: Psychology Press reprint, 2013). **Published:** 1977 (the OpenAlex description begins "First Published in 1977") [S1].
- **Link:** https://doi.org/10.4324/9780203781036 (the 2013 reprint DOI; the 1977 edition has no DOI in the records read).
- **Citations:** no single count. OpenAlex: 3,156 (2013 reprint record), 4,536 (a 1988 anthology record, W123366752), 2,944 (a review record) [S1]. Not summed, and the review and anthology records may count other works' citations; treat as "several thousand, composition unknown".
- **Tests:** *origin* of scripts - the title names scripts and plans; Sowa's survey says Schank "later developed scripts for larger structures" after conceptual dependency [S6]. The book's own text was not read. *widely built on* - the counts above, with the caveat stated.
- **Idea:** From the publisher blurb: the book grew from a 1971 workshop at the intersection of psychology, AI and linguistics, on "the representation of large systems of knowledge (or beliefs) based upon an understanding process operating upon information expressed in natural language" [S1]. What a script is: **unstated** in the sources read (the title is the only evidence).
- **Relations:** builds on Schank's conceptual dependency (Sowa: Schank "adopted the dependency approach from Hays and Simmons" and "shifted the emphasis to concepts rather than words" [S6]; see the 1972 paper in "Considered"). Related to Minsky 1974 (section 5) as a structured knowledge unit; no sentence read ties them.
- **Read:** publisher blurb and listing, 20261102 19:52 UTC; Sowa page 19:51 UTC.

## 9. Gelfond and Lifschitz, "The Stable Model Semantics for Logic Programming" (1988)

- **Authors:** Michael Gelfond, Vladimir Lifschitz (2 authors). **Venue:** unstated in the records read (OpenAlex shows no venue). **Published:** 1988 [S1].
- **Link:** OpenAlex https://openalex.org/W1672891595 (no DOI found).
- **Citations:** OpenAlex 3,451; Crossref none (no DOI); read 20261102 19:43 UTC [S1].
- **Tests:** *turning point* - the abstract: "We propose a new declarative semantics for logic programs with negation... more general than the iterated fixed point semantics for stratified programs, and is applicable to some useful programs that are not stratified" [S1, abstract]. *widely built on* - count above. That this paper founded answer-set programming is **not stated** in the abstract and was not checked.
- **Idea:** A semantics for logic programs with negation defined by a simple guess-and-check construction; it covers programs that stratified semantics cannot [S1].
- **Relations:** answers the question of what negation in logic programs means, opened by Clark 1978 "Negation as Failure" (not proposed; 2,112 OpenAlex) - by subject; the abstract names stratified programs, not Clark. Related: Reiter 1978 (section 13), the closed-world reading of absent facts.
- **Read:** abstract, 20261102 19:48 UTC.

## 10. Brachman and Schmolze, "An Overview of the KL-ONE Knowledge Representation System" (1985)

- **Authors:** Ronald J. Brachman, James G. Schmolze (2 authors). **Venue:** Cognitive Science 9(2). **Published:** OpenAlex 198504, Crossref 198506 (both read; unresolved) [S1, S2].
- **Link:** https://doi.org/10.1016/s0364-0213(85)80014-8
- **Citations:** OpenAlex 1,775, Crossref 128; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *origin* of the KL-ONE line from which description logics grew - the archive primer states "Description logics grew from it; they underpin OWL" citing Hogan et al. (via the archive page, primer row 1985); Sowa's survey: KL-ONE is "the basis of the description logics" he discusses [S6]. The abstract: "KL-ONE is a system for representing knowledge in AI programs... we present the kernel ideas... emphasizing its ability to form complex structured descriptions... notions of taxonomy and classification that are central to it" [S3]. *widely built on* - counts, with the discrepancy noted.
- **Idea:** A knowledge representation system built around structured descriptions of concepts, a taxonomy of them, and automatic classification of new descriptions into that taxonomy [S3].
- **Relations:** builds on semantic networks and Woods 1975, Brachman 1979 (sections 22, 21): Sowa says KL-ONE was the system that implemented the approach proposed by Woods and developed by Brachman [S6]. Answered by Brachman and Levesque 1984 (section 23), which studies the cost of reasoning in such description languages. Later era: W3C OWL (20040210), "a Web ontology language based on description logics" (via the archive page, primer row 20040210).
- **Read:** abstract, 20261102 19:48 UTC; Sowa 19:51 UTC.

## 11. Robertson and Spärck Jones, "Relevance Weighting of Search Terms" (1976)

- **Authors:** Stephen E. Robertson, Karen Spärck Jones (2 authors). **Venue:** Journal of the American Society for Information Science. **Published:** 197605 [S2].
- **Link:** https://doi.org/10.1002/asi.4630270302
- **Citations:** OpenAlex 2,093, Crossref 1,214; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *origin* of probabilistic relevance weighting - the abstract: "A series of relevance weighting functions is derived and is justified by theoretical considerations. In particular, it is shown that specific weighted search methods are implied by a general probabilistic theory of retrieval" [S3]. *widely built on* - counts above. That these weights are the root of BM25 is **unstated** in any source read (Robertson and Walker 1994, 1,484 OpenAlex, is the usual link; its abstract was not available, and it lies outside this file's span).
- **Idea:** If relevance judgements are available, weight each search term by the evidence they give; the resulting weights follow from a probabilistic theory of retrieval and extend collection-frequency weighting [S3].
- **Relations:** builds on Spärck Jones 1972 (section 6): "a natural extension of weighting methods using information about the distribution of index terms in documents in general" [S3]. Builds on the probabilistic idea of Maron and Kuhns 1960 (section 15) - by subject; not cited in the abstracts read. Later era: the BM25 comparison in section 4 [S10].
- **Read:** abstract, 20261102 19:48 UTC.

## 12. Hull and King, "Semantic Database Modeling: Survey, Applications, and Research Issues" (1987)

- **Authors:** Richard Hull, Roger King (2 authors). **Venue:** ACM Computing Surveys. **Published:** 198709 [S2].
- **Link:** https://doi.org/10.1145/45072.45073
- **Citations:** OpenAlex 1,146, Crossref 839; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *survey of record* for semantic data models - the abstract: "an in-depth discussion of semantic data modeling... a tutorial introduction to the primary components of semantic models, which are the explicit representation of objects, attributes of and relationships among objects, type constructors for building complex types, ISA relationships, and derived schema components. Next, a survey of the prominent semantic models in the literature is presented" [S3]. That other sources use it as the survey is supported only by the count.
- **Idea:** Semantic modelling gives richer structuring than record-based databases and "complements work on knowledge representation (in artificial intelligence)" and on object-oriented database models [S3].
- **Relations:** surveys the line begun by Chen 1976 (section 3) and Codd 1979 (not proposed); links databases to knowledge representation in the abstract's own words [S3]. Related: Brachman 1983 "What IS-A is and isn't" (not proposed) on the same ISA link from the AI side.
- **Read:** abstract, 20261102 19:48 UTC.

## 13. Reiter, "On Closed World Data Bases" (1978)

- **Authors:** Raymond Reiter (1 author). **Venue:** chapter in *Logic and Data Bases* (Gallaire and Minker, eds.), Plenum [S2]. **Published:** 1978 [S2].
- **Link:** https://doi.org/10.1007/978-1-4684-3384-5_3
- **Citations:** OpenAlex 1,129 (a 1989 and a 1981 anthology record add 69 and 53; not summed), Crossref 368; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *widely built on* - counts above. *origin / turning point* for the closed-world assumption (a database is taken to state everything that is true): supported by the title only; no abstract was available. Treat the origin claim as **unverified**.
- **Idea:** **Unstated from a source read.** The title names closed-world databases. A writer must read the paper before stating its definitions.
- **Relations:** appears in the same 1978 volume as Clark's "Negation as Failure" (Crossref container "Logic and Data Bases" for both [S2]). Surveyed by Gallaire, Minker and Nicolas 1984 (section 20). Later era, by topic: the archive primer notes that OWL keeps open-world semantics and "OWL DL keeps decidability" (via the archive page); no source read links Reiter to OWL.
- **Read:** listing only, 20261102 19:46 UTC.

## 14. Luhn, "A Statistical Approach to Mechanized Encoding and Searching of Literary Information" (1957)

- **Authors:** H. P. Luhn (1 author). **Venue:** IBM Journal of Research and Development 1(4). **Published:** 195710 [S2].
- **Link:** https://doi.org/10.1147/rd.14.0309
- **Citations:** OpenAlex 1,092, Crossref 691; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *origin* of statistical, machine-based encoding and searching - the abstract: "A statistical approach to this problem will be outlined and the various steps of a system based on this approach will be described", from statistical analysis of a collection through a thesaurus-type dictionary to machine encoding and search [S3]. That Luhn introduced term-frequency weighting specifically is **not stated** in the abstract. *widely built on* - counts above.
- **Idea:** Authors choose levels of specificity and words statistically, so different phrasings of the same idea make machine searching hard; Luhn proposes analysing a collection statistically to build a vocabulary of notions and a dictionary, encoding documents automatically and searching the codes [S3].
- **Relations:** precedes Maron and Kuhns 1960 (section 15) and Spärck Jones 1972 (section 6) in the statistical line; no abstract read cites it.
- **Read:** abstract, 20261102 19:48 UTC.

## 15. Maron and Kuhns, "On Relevance, Probabilistic Indexing and Information Retrieval" (1960)

- **Authors:** M. E. Maron, J. L. Kuhns (2 authors). **Venue:** Journal of the ACM. **Published:** 196007 [S2].
- **Link:** https://doi.org/10.1145/321033.321035
- **Citations:** OpenAlex 909, Crossref 517; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *origin* of probabilistic indexing - the abstract: "The notion of relevance is taken as the key concept in the theory of information retrieval and a comparative concept of relevance is explicated in terms of the theory of probability. The resulting technique called 'Probabilistic Indexing' allows a computing machine... to derive a number (called the 'relevance number') for each document" and to return a ranked list [S3]. *widely built on* - counts above.
- **Idea:** Treat the request as a clue from which the system makes a statistical inference and ranks documents by probable relevance; statistical closeness between index terms can replace hand-made "see also" links [S3].
- **Relations:** the line continues in Robertson and Spärck Jones 1976 (section 11) and Robertson 1977 "The probability ranking principle in IR" (not proposed; abstract: the principle that documents be ranked by probability of relevance "has been brought into question by Cooper" and "can be justified under certain assumptions" [S3]).
- **Read:** abstract, 20261102 19:48 UTC.

## 16. Kowalski, "Predicate Logic as Programming Language" (1974)

- **Authors:** Robert Kowalski (1 author). **Venue:** IFIP Congress (OpenAlex venue field) [S1]. **Published:** 1974 [S1].
- **Link:** OpenAlex https://openalex.org/W1578088218 (no DOI found).
- **Citations:** OpenAlex 669; Crossref none; read 20261102 19:43 UTC [S1].
- **Tests:** *origin* of logic programming - supported by the title and by the follow-up paper's abstract, van Emden and Kowalski 1976: "Sentences in first-order predicate logic can be usefully interpreted as programs" [S3]. The 1974 abstract was not available; the origin claim is therefore **inferred from the title and the 1976 abstract**. *widely built on*: modest count; the 1976 follow-up has 1,449 OpenAlex and 1,022 Crossref.
- **Idea:** **Unstated from a source read for the 1974 paper.** The 1976 paper defines "the operational and fixpoint semantics of predicate logic programs" and concludes that "operational semantics is a part of proof theory and that fixpoint semantics is a special case of model-theoretic semantics" [S3].
- **Relations:** answered by van Emden and Kowalski 1976 (not proposed; the formal semantics) and Kowalski 1979 "Algorithm = Logic + Control" (not proposed; abstract: "database systems should be regarded as consisting of a relational component, which defines the logic of the data, and a control component", as "successfully argued by Codd" [S3]). Bridges to Codd 1970 (section 1) and Gallaire et al. 1984 (section 20).
- **Read:** listing only for 1974, 20261102 19:48 UTC; 1976 and 1979 abstracts 19:48 UTC.

## 17. McCarthy, "Programs with Common Sense" (1958)

- **Authors:** John McCarthy (1 author). **Venue:** *Mechanisation of Thought Processes*, Proceedings of the Symposium of the National Physical Laboratory, London, HMSO, pp. 77-84 (author's bibliography entry) [S5]. **Presented:** December 1958 (Teddington conference) [S5]; OpenAlex dates the proceedings record 1960 [S1].
- **Link:** http://www-formal.stanford.edu/jmc/mcc59.html
- **Citations:** OpenAlex 931 (record W2119409989); Crossref none; read 20261102 19:43 UTC [S1].
- **Tests:** *origin* of logical AI. **First-party claim:** McCarthy's own page says the paper "was probably the first paper on logical AI, i.e. AI in which logic is the method of representing information in computer memory and not just the subject matter of the program" [S5]. *widely built on* - modest count.
- **Idea:** From the OpenAlex abstract: certain elementary verbal reasoning processes "so simple that they can be carried" out by people without effort are still beyond programs, which motivates a program that can reason from stored declarative statements [S1; the abstract is cut off in the record - the second half of this sentence is the writer's reading and must be checked against the paper].
- **Relations:** related to Cyc (section 25), which tries to supply the common sense McCarthy asks for: a 1990 OpenAlex record titled "Cyc: toward programs with common sense" (Lenat and Guha, 508 citations) echoes the title [S1].
- **Read:** the author's page (summary of the paper), 20261102 19:50 UTC; OpenAlex abstract (truncated) 19:52 UTC. The paper was not read.

## 18. Quillian, "Word Concepts: A Theory and Simulation of Some Basic Semantic Capabilities" (1967)

- **Authors:** M. Ross Quillian (1 author). **Venue:** Behavioral Science 12(5). **Published:** 196709 [S2].
- **Link:** https://doi.org/10.1002/bs.3830120511
- **Citations:** OpenAlex 778, Crossref 468; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *origin* of the semantic-network line (the archive primer dates the line from Quillian's 1963 report, via the archive page, primer row 1963, citing Hogan et al.). Sowa credits Quillian with combining earlier network ideas and with "the marker passing algorithm for spreading activations" [S6]. Sowa dates Quillian's main work to the 1966 dissertation and the 1968 chapter in Minsky's *Semantic Information Processing*; this 1967 journal paper is the one with a DOI and an abstract. *widely built on* - counts above; the spreading-activation theory by Collins and Loftus 1975 (8,141 OpenAlex; "based on Quillian's theory" [S3]) is the largest descendant.
- **Idea:** A dictionary is "recoded" into "a complex network of elements and associations"; a program uses it to compare and contrast the meanings of word pairs, infer relationships and produce English text, as a theory of how human semantic memory may be formatted and used [S3].
- **Relations:** answered by Collins and Quillian 1969 "Retrieval time from semantic memory" (not proposed; 3,140 OpenAlex) which tests the model on people; answered by Collins and Loftus 1975 (not proposed); formalisation worries follow in Woods 1975 (section 22).
- **Read:** abstract, 20261102 19:48 UTC; Sowa page 19:51 UTC.

## 19. Buchanan and Shortliffe (eds.), *Rule-Based Expert Systems: The MYCIN Experiments of the Stanford Heuristic Programming Project* (1984)

- **Authors:** Bruce G. Buchanan, Edward H. Shortliffe (editors; 2 listed), with many chapter authors. **Venue:** book, Addison-Wesley. **Published:** 198406 (OpenAlex W26924883) [S1].
- **Link:** https://people.dbmi.columbia.edu/~ehs7001/Buchanan-Shortliffe-1984/MYCIN%20Book.htm (contents page; no DOI found).
- **Citations:** OpenAlex 575 for the book record (W26924883); two further records have 1,701 (a 1986 journal listing) and 1,237 (a 1985 review in Artificial Intelligence); not summed, because reviews and listings can carry the book's citations [S1].
- **Tests:** *survey of record* for rule-based expert systems and their knowledge engineering - the contents list has 36 chapters in twelve parts, including "Ch. 2 The Origin of Rule-Based Systems in AI", "Part Three: Building a Knowledge Base" with "Ch. 7 Knowledge Engineering", "Ch. 15 EMYCIN: A Knowledge Engineer's Tool for Constructing Rule-Based Expert Systems", and "Ch. 31 An Evaluation of MYCIN's Advice" [S7]. The evaluation chapter makes it also a *turning point* candidate (evaluation of an expert system against physicians), but it is first-party (Stanford authors) and its result was not read. The archive primer cites the same page as the setting where "knowledge base" is a technical term (via the archive page, primer row 1970s to 1980s).
- **Idea:** A Stanford project's collected experiments on MYCIN, a rule-based consultation system: the rule form, the inference engine, knowledge base building, uncertainty, explanation, tutoring, generalisation to EMYCIN, and evaluation [S7, contents].
- **Relations:** includes Chapter 11, "A Model of Inexact Reasoning in Medicine" (Shortliffe and Buchanan; the 1975 paper, 1,446 OpenAlex; not proposed) and Davis and Buchanan's "Meta-Level Knowledge" chapter [S7]; follows Davis, Buchanan and Shortliffe 1977 (section 28). Feigenbaum's 1977 paper (section 27) names the practice the book's Part Three calls knowledge engineering.
- **Read:** contents page, 20261102 19:52 UTC (and 20261030 19:02 UTC via the archive page). Chapters not read.

## 20. Gallaire, Minker and Nicolas, "Logic and Databases: A Deductive Approach" (1984)

- **Authors:** Hervé Gallaire, Jack Minker, Jean-Marie Nicolas (3 authors). **Venue:** ACM Computing Surveys 16(2). **Published:** 198406 [S2].
- **Link:** https://doi.org/10.1145/356924.356929
- **Citations:** OpenAlex 734, Crossref 520; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *survey of record* for deductive databases - the abstract: "logic provides a convenient formalism for studying classical database problems... two main parts... conventional databases and deductive databases", covering query languages, integrity, query optimisation and more [S3]. Its use as the survey others rely on rests on the venue (Computing Surveys) and the count.
- **Idea:** First-order logic gives one formalism for the classical database problems and for databases that deduce new facts from stored ones [S3].
- **Relations:** builds on Codd 1970 (section 1) and the logic-programming line of Kowalski (section 16); the 1978 volume *Logic and Data Bases* (Gallaire and Minker) holds Reiter and Clark [S2]. Related: Ceri, Gottlob and Tanca 1989 "What you always wanted to know about Datalog" (not proposed; abstract: "Datalog, a database query language based on the logic programming paradigm", with optimisation methods classified [S3]).
- **Read:** abstract (cut off in the record), 20261102 19:48 UTC.

## 21. Brachman, "On the Epistemological Status of Semantic Networks" (1979)

- **Authors:** Ronald J. Brachman (1 author). **Venue:** chapter in *Associative Networks* (N. V. Findler, ed.), Academic Press, pp. 3-50 (Sowa's reference gives the pages) [S2, S6]. **Published:** 1979 [S2]. The archive primer gives "Brachman (1977)" for this line, citing Hogan et al.; the 1977 date probably refers to the earlier BBN report version and is **not verified** here.
- **Link:** https://doi.org/10.1016/b978-0-12-256380-5.50007-4
- **Citations:** OpenAlex 625, Crossref 156; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *turning point* - the archive primer lists "Woods (1975) and Brachman (1977) formalise semantic networks" as attempts to give graph notations a formal meaning (via the archive page, primer row 1975 to 1979); Sowa cites this paper as the basis of KL-ONE [S6]. *widely built on* - counts above.
- **Idea:** **Unstated from a source read** (no abstract). The title poses the question of what epistemological commitments a semantic network makes.
- **Relations:** answers Quillian-style networks (section 18) and builds on Woods 1975 (section 22); leads to KL-ONE (section 10) [S6].
- **Read:** listing only, 20261102 19:46 UTC.

## 22. Woods, "What's in a Link: Foundations for Semantic Networks" (1975)

- **Authors:** William A. Woods (1 author). **Venue:** BBN report; chapter in *Representation and Understanding* (D. G. Bobrow and A. Collins, eds.), Academic Press, pp. 35-82 (Sowa's reference) [S6]. **Published:** 197511 (DTIC/Crossref record) [S2].
- **Link:** https://doi.org/10.21236/ada022584
- **Citations:** OpenAlex 245 (report record W4246055080; a 1988 anthology record adds 39), Crossref 56; read 20261102 19:43 and 19:46 UTC [S1, S2]. Low counts understate its role: it is cited by name in later abstracts.
- **Tests:** *turning point* - an independent paper's abstract (Allen and Frisch 1982, "What's in a semantic network?") says: "Ever since Wood's 'What's in a Link' paper, there has been a growing concern for formalization in the study of knowledge representation" and that "several arguments have been made that frame representation languages and semantic-network languages are syntactic variants of the first-order predicate calculus" [S1, abstract of W2116066570]. Sowa: description logics derive from "an approach proposed by Woods (1975)" [S6]. The archive primer: Sowa, quoting Woods and McDermott, wrote that semantic networks "have no well-defined semantics" (via the archive page).
- **Idea:** **Unstated from a source read** (no abstract). Secondary sources agree that it asks what the links of a semantic network mean and asks for a formal account [S1, S6].
- **Relations:** answers the informal networks of Quillian (section 18) and the frames of Minsky (section 5); answered by Brachman 1979 (section 21) and KL-ONE (section 10); evaluated in Allen and Frisch 1982 (abstract above).
- **Read:** listing, 20261102 19:46 UTC; Allen and Frisch abstract 19:52 UTC; Sowa page 19:51 UTC.

## 23. Brachman and Levesque, "The Tractability of Subsumption in Frame-Based Description Languages" (1984)

- **Authors:** Ronald J. Brachman, Hector J. Levesque (2 authors). **Venue:** unstated in the record (OpenAlex shows none; the paper is usually cited as AAAI-84, **not verified** here). **Published:** 19840806 [S1].
- **Link:** OpenAlex https://openalex.org/W2127140110 (no DOI found).
- **Citations:** OpenAlex 335; Crossref none; read 20261102 19:43 UTC [S1].
- **Tests:** *turning point* - the abstract: "the cost of computing one kind of inference is directly related to the expressiveness of the representation language. As it turns out, this cost is perilously sensitive to small changes in the representation language. Even a seemingly simple frame-based description language can pose intractable computational obstacles" [S1]. *origin* of the expressiveness-versus-tractability trade-off in description languages: supported by the abstract's wording; priority over other work is not checked.
- **Idea:** A representation system computes inferences automatically for the knowledge-based system around it, so the cost of those inferences matters; the paper shows that adding small features to a frame-based description language can make subsumption intractable [S1].
- **Relations:** evaluates KL-ONE-style description languages (section 10) - the title names "frame-based description languages". Later era, by topic: the archive primer lists "a trade-off between expressiveness and decidability: OWL DL keeps decidability, OWL Full has 'no computational guarantees'" (via the archive page, citing W3C OWL Overview). Levesque and Brachman 1987 (not proposed; 321) restates the trade-off.
- **Read:** abstract, 20261102 19:52 UTC.

## 24. Brachman and Levesque (eds.), *Readings in Knowledge Representation* (1985)

- **Authors:** Ronald J. Brachman, Hector J. Levesque (2 editors). **Venue:** book, Morgan Kaufmann. **Published:** 198508 (OpenAlex W1492582005) [S1].
- **Link:** OpenAlex https://openalex.org/W1492582005 (no DOI found).
- **Citations:** OpenAlex 1,031; read 20261102 19:43 UTC [S1].
- **Tests:** *survey of record*, in the sense of a curated map: the publisher blurb says the volume collects "seminal articles, spanning a quarter-century of research", with editors who "introduce each paper, discuss its relevance and context, and provide an extensive bibliography" [S1]. It is an anthology, not a survey article. The volume's table of contents was not read.
- **Idea:** A sourcebook for the representation field: the principles of knowledge representation as they bear on language processing, vision and expert systems [S1].
- **Relations:** an anthology of the papers in this pool; its table of contents was not read, so which candidates it reprints is **unstated**. Related: the 1989 OpenAlex records that republish Forgy, Reiter, Brachman and Schmolze, Shipman and others under one book DOI prefix (10.1016/b978-0-934613-53-8) suggest a companion anthology of the same publisher; not investigated.
- **Read:** publisher blurb, 20261102 19:52 UTC.

## 25. Lenat, Prakash and Shepherd, "CYC: Using Common Sense Knowledge to Overcome Brittleness and Knowledge Acquisition Bottlenecks" (1985)

- **Authors:** Douglas B. Lenat, Mayank Prakash, Mary Shepherd (3 authors) [S8]. **Venue:** AI Magazine 6(4) [S8]. **Published:** 1985 (volume 6, issue 4); OpenAlex dates the record 19860101; the month is **unstated** [S1, S8].
- **Link:** https://doi.org/10.1609/aimag.v6i4.510 (resolves in OpenAlex; Crossref returned 404 for it) and the bibliographic record https://interlisp.org/history/bibliography/qxtftccf/
- **Citations:** OpenAlex 300 (record W2163908084); Crossref none; read 20261102 19:43 UTC [S1].
- **Tests:** *origin* of Cyc - the paper describes "MCC's CYC project, a planned decade-long effort to build a large knowledge base of real-world facts and heuristics, along with methods for reasoning over it" (bibliographic record, summarised by the fetch tool, not quoted) [S8]; the abstract in OpenAlex: "decades of work on such systems have convinced us that each of these approaches has difficulty scaling up for want [of] a substantial base of real world knowledge" [S1]. The project's start year is **unstated** in the sources read (the archive primer notes 1984 is common but not verified).
- **Idea:** Brittleness and the knowledge-acquisition bottleneck limit large software and expert systems; machine learning, automatic programming and language understanding all lack a large base of real-world knowledge, so build that base by hand [S1, S8].
- **Relations:** answers the expert-system problems named in Feigenbaum 1977 and MYCIN-era work (sections 27, 19): the abstract cites "the recent history of expert systems" as evidence of the bottlenecks [S1]. Related to McCarthy 1958 (section 17). Later era: Knowledge Vault (KDD 2014) bets the other way - let extractors read the web and attach probabilities (via the archive page, primer lines on the Cyc and Knowledge Vault end-points). Lenat 1995 (OpenAlex 1,946) and Lenat and Guha 1990 belong to the 1990+ file.
- **Read:** abstract, 20261102 19:44 UTC (bibliographic record) and 19:52 UTC (OpenAlex abstract); also 20261030 19:02 UTC via the archive page.

## 26. Chamberlin and Boyce, "SEQUEL: A Structured English Query Language" (1974)

- **Authors:** Donald D. Chamberlin, Raymond F. Boyce (2 authors) [S4]. **Venue:** ACM SIGFIDET workshop on Data Description, Access and Control, 1974 [S4]. **Published:** 19740501 per the IBM Research listing [S4]. **Date conflict:** Crossref and OpenAlex file the same DOI under "FIDET '76" with year 1976 and the title "SEQUEL" [S1, S2]; the IBM listing and the 1974 workshop name are taken here, and Semantic Scholar's own publication date for the DOI is 19740501 [S11], which agrees with IBM. The Crossref label looks like a metadata error; the ACM page (HTTP 403) could not settle it.
- **Link:** https://doi.org/10.1145/800296.811515
- **Citations:** OpenAlex 584, Crossref 190 (same DOI); read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *origin* of SEQUEL, the language that became SQL. The abstract: "the data manipulation facility for a structured English query language (SEQUEL) which can be used for accessing data in an integrated relational data base... a set of simple operations on tabular structures, which can be shown to be of equivalent power to the first order predicate calculus" [S3, S4]. That SEQUEL was renamed SQL comes from a search-engine summary only (a lead, not a source) and is **unverified**. *widely built on* - counts above.
- **Idea:** A relational query language in keyword English templates, avoiding bound variables and quantifiers, usable by both programmers and occasional users [S4].
- **Relations:** builds on Codd 1970 (section 1): it queries "an integrated relational data base" [S3]. Related: "Implementation of a structured English query language" (Astrahan and Chamberlin, CACM 1975, 154 OpenAlex; not proposed) [S1].
- **Read:** abstract and IBM listing, 20261102 19:49 UTC. The ACM page returned HTTP 403.

## 27. Feigenbaum, "The Art of Artificial Intelligence: Themes and Case Studies of Knowledge Engineering" (1977)

- **Authors:** Edward A. Feigenbaum (1 author). **Venue:** IJCAI-77, Cambridge, MA (the hosting URL is the IJCAI proceedings folder 77-2) [S9]. **Published:** OpenAlex 197708 [S1].
- **Link:** https://www.ijcai.org/Proceedings/77-2/Papers/092.pdf
- **Citations:** OpenAlex 534 (report record W2158270697; a 1978 AFIPS record adds 32); Crossref none; read 20261102 19:43 UTC [S1].
- **Tests:** *origin* (naming) of "knowledge engineering" is the usual claim; the abstract says "The knowledge engineer practices the art of bringing the principles and tools of AI research to bear on difficult applications problems requiring experts' knowledge for their solution" and that "systems that have achieved expert level performance in scientific and medical inference illuminate the art of knowledge [engineering]" [S1]. Whether this is the **first** use of the term is **unstated** in the sources read. *widely built on* - modest count.
- **Idea:** Expert-level performance comes from acquiring, representing and using an expert's knowledge, and building programs that can explain their lines of reasoning [S1].
- **Relations:** draws on DENDRAL and MYCIN (the abstract's "scientific and medical inference" systems; the names are not in the abstract); the MYCIN book's Chapter 7 is titled "Knowledge Engineering" [S7]. Answered by Lenat et al. 1985 (section 25), which blames the "knowledge acquisition bottlenecks" of expert systems [S1].
- **Read:** abstract (OpenAlex), 20261102 19:52 UTC. The scanned PDF at the link was fetched (16 pages, 8 MB) but had no readable text layer, so it was **not read**.

## 28. Davis, Buchanan and Shortliffe, "Production Rules as a Representation for a Knowledge-Based Consultation Program" (1977)

- **Authors:** Randall Davis, Bruce Buchanan, Edward Shortliffe (3 authors) [S2]. **Venue:** Artificial Intelligence 8(1). **Published:** 197702 [S2]; an earlier DTIC report record is dated 197510 [S1].
- **Link:** https://doi.org/10.1016/0004-3702(77)90003-0
- **Citations:** OpenAlex 569, Crossref 385; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *origin* of production rules as the representation of a rule-based consultation program: **supported by the title only**; no abstract was available. The MYCIN book places its chapter "The Origin of Rule-Based Systems in AI" (Davis and King) and "The Evolution of MYCIN's Rule Form" in Parts One and Two [S7]. *widely built on* - counts above.
- **Idea:** **Unstated from a source read.** The title says MYCIN-style production rules are used as the representation for a knowledge-based consultation program.
- **Relations:** the research behind the 1984 MYCIN book (section 19); Davis and Buchanan's meta-level knowledge chapter extends it [S7]. Later era: the rule-engine idea resurfaces in Rete-based engines (Forgy 1982, 2,638 OpenAlex; not proposed).
- **Read:** listing only, 20261102 19:46 UTC.

## 29. Cleverdon, "The Cranfield Tests on Index Language Devices" (1967)

- **Authors:** Cyril W. Cleverdon (1 author). **Venue:** Aslib Proceedings 19(6). **Published:** 196706 [S2].
- **Link:** https://doi.org/10.1108/eb050097
- **Citations:** OpenAlex 488, Crossref 255; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *turning point* - the abstract: "the most important consideration was the specificity of the index terms; within the context of the conditions existing in this test, single-word terms were more effective than concept terms or a controlled vocabulary" [S3]; a result that favoured plain keywords over controlled vocabularies. That Cranfield is the *origin of the test-collection evaluation paradigm* (queries, documents, relevance judgements) is **not stated** in the abstract read.
- **Idea:** An experimental comparison of index-language devices; the effect of the device mattered less than the specificity of the index terms, and single-word terms beat concept terms and controlled vocabularies [S3].
- **Relations:** Spärck Jones 1972 (section 6) is a later "experiments with three test collections" paper on specificity [S3]; whether Cranfield is one of its collections is **unstated**. Later era: the archive benchmark chapter (`kb-kg/papers-benchmarks/README.md`) is the home for modern evaluation sets; no sentence read links it to Cranfield.
- **Read:** abstract, 20261102 19:48 UTC.

## 30. Clancey, "Heuristic Classification" (1985)

- **Authors:** William J. Clancey (1 author). **Venue:** Artificial Intelligence 27(3). **Published:** 198512 [S2].
- **Link:** https://doi.org/10.1016/0004-3702(85)90016-5
- **Citations:** OpenAlex 880, Crossref 754; read 20261102 19:43 and 19:46 UTC [S1, S2].
- **Tests:** *widely built on* - counts above. *turning point* (a problem-solving method abstracted from many expert systems): suggested by the title, **not verified** - no abstract was available and no secondary source read describes the paper.
- **Idea:** **Unstated from a source read.** The title names heuristic classification as a method.
- **Relations:** Clancey is the author of two chapters in the MYCIN book (section 19: "Details of the Revised Therapy Algorithm" and "Use of MYCIN's Rules for Tutoring") [S7]; the paper's own relation to MYCIN is not stated in the sources read.
- **Read:** listing only, 20261102 19:46 UTC.

---

## Considered and not proposed

Count in parentheses is OpenAlex `cited_by_count`, read 20261102 19:43 UTC [S1] unless stated.

| Paper | Why not proposed |
|---|---|
| Collins and Loftus 1975, spreading-activation theory (8,141) | Largest descendant of Quillian; psychology, not KB design. Further reading under Quillian. |
| Collins and Quillian 1969, Retrieval time from semantic memory (3,140) | Psychological test of Quillian's model; covered by the Quillian section. Further reading. |
| Hayes 1979, The Logic of Frames (233 + 49) | The turning-point claim (frames are first-order logic) is not shown by any source read, only hinted at by Allen and Frisch 1982's abstract. Verify before proposing. |
| Schank 1972, Conceptual dependency (996) | Origin of conceptual dependency, the base of scripts; kept as further reading under Schank and Abelson. |
| Sowa 1984, Conceptual Structures (2,748) and Sowa 1976 (367) | Conceptual graphs: passes widely-built-on, but no source read describes it beyond the title; keep for the ontologies chapter if the standards file (Common Logic) is in scope. |
| Bobrow and Winograd 1977, KRL (922) | Frame language; no abstract read; further reading. |
| Brachman 1983, What IS-A is and isn't (571) | Strong on taxonomic links, but the Hull and King and KL-ONE entries cover the ground; further reading. |
| Levesque and Brachman 1987, Expressiveness and tractability (321) | Restates Brachman and Levesque 1984; further reading. |
| McCarthy and Hayes 1969, Some philosophical problems (3,280) | Origin of the frame problem; belongs to AI logic, not to knowledge bases; further reading. |
| Newell and Simon 1972, Human Problem Solving (6,222 across records) | Origin of production systems as a cognitive architecture; book not read; further reading. |
| Shortliffe 1976, Computer-based medical consultations: MYCIN (2,505 on an Annals review record) | Origin of MYCIN; the book was not read and the count sits on a review record; the 1984 volume (proposed) is the readable record. |
| Shortliffe and Buchanan 1975, certainty factors (1,446) | Origin of certainty factors; covered by Chapter 11 of the 1984 volume; further reading. |
| Duda, Hart et al. 1976, Subjective Bayesian methods (543) | Prospector; further reading. |
| Miller, Pople, Myers 1982, INTERNIST-I (1,130) | Medical diagnostic system; no abstract read; further reading. |
| Hayes-Roth, Waterman, Lenat 1983, Building Expert Systems (1,686) | Textbook of record for the era; split across records, no abstract read; strong candidate if the owner wants a second survey. |
| McDermott 1982, R1 (951) and Forgy 1982, Rete (2,638) | R1 is the commercial success, Rete the engine algorithm; neither abstract was available. Rete is a strong widely-built-on candidate for the rules chapter. |
| Hayes-Roth 1985, Rule-based systems (580) | Overview in CACM; no abstract read. |
| Lenat 1990 "Cyc: toward programs with common sense" (508) and Lenat 1995 (1,946) | Outside the 1950-1989 span; belong to the 1990+ file. |
| Robinson 1965, resolution principle (3,916; Crossref 2,548) | Origin of resolution; logic infrastructure behind Prolog; not specific to knowledge bases; further reading. |
| Green 1969, Application of theorem proving to problem solving (341) | Question answering by theorem proving; no abstract read. |
| van Emden and Kowalski 1976 (1,449) and Kowalski 1979 (614) | Semantics of logic programs; abstracts read; kept as further reading beside Kowalski 1974 (could replace it if the 1974 paper's text is never obtained). |
| Clark 1978, Negation as failure (2,112) | Strong count; no abstract read; further reading beside Gelfond and Lifschitz. |
| Reiter 1980, A logic for default reasoning (3,902) | Nonmonotonic reasoning; no abstract read; stronger than several proposed items by count, so the owner may prefer it to Reiter 1978. |
| McDermott and Doyle 1980 (912) and Doyle 1979, truth maintenance (1,784) | Nonmonotonic logic and TMS; no abstract read; further reading. |
| Ceri, Gottlob, Tanca 1989, Datalog (703) | Abstract read; Datalog survey; further reading beside Gallaire et al. |
| Codd 1979, RM/T (1,559) | Abstract read; relational model with more meaning; further reading beside Chen and Hull and King. |
| Astrahan et al. 1976, System R (214) and Stonebraker et al. 1976, INGRES (894) | Relational systems; belong to a database-systems list, not a knowledge list. |
| Bachman 1973, The programmer as navigator (150) | Argues for the navigational model Codd opposed; low count; further reading for the dispute. |
| Peckham and Maryanski 1988 (562), Hammer and McLeod 1981 (753), Shipman 1981 (913), Abiteboul and Hull 1987 (462) | Semantic data models; Hull and King is the survey of record. |
| Salton and Yang 1973 (586) | Early term-value specification; no abstract read. |
| Robertson 1977, probability ranking principle (1,069) | Abstract read; strong for the probabilistic line; could replace Maron and Kuhns if the owner prefers theory to origin. |
| Salton and McGill 1983, Introduction to Modern Information Retrieval (9,706) | Textbook; no abstract; strong survey-of-record candidate. |
| van Rijsbergen 1979, Information Retrieval | No OpenAlex record found by title search (checked 20261102 19:43 UTC); count **unstated**. Verify and add if it can be sourced. |
| Harter 1975, probabilistic keyword indexing (195 + 110 + 146) | Two-Poisson precursor; low counts. |
| Salton, Fox 1983, P-norm queries (106) | Extended Boolean model; low count. |
| Bush 1945, As We May Think (2,984) | Before 1950 and about the memex; outside the span. |
| Deerwester et al. 1990, latent semantic analysis (12,758) and Robertson and Walker 1994 (1,484) | Outside this file's span; belong to the 1990+ retrieval file. |

---

## Sources

Read times are the minute of the tool call, from the clock.

- **S1.** OpenAlex API, `https://api.openalex.org/works?search=<title>` (78 title searches, 20261102 19:42 to 19:43 UTC) and `https://api.openalex.org/works/<id or doi>` (abstracts and counts, 19:48 to 19:52 UTC). Supports every OpenAlex count, record dates and abstracts cited above.
- **S2.** Crossref REST API, `https://api.crossref.org/works/<DOI>` (32 DOIs, 20261102 19:46 UTC; the Cyc DOI returned HTTP 404). Supports Crossref counts, venues, issue dates, author counts.
- **S3.** The abstract fields of the OpenAlex and Crossref records in S1 and S2 for the DOIs cited in each section (read 20261102 19:48 and 19:52 UTC). Abstracts are the publishers' texts as deposited; some are cut off in the record.
- **S4.** MIT DSpace, Minsky AIM-306, `https://dspace.mit.edu/handle/1721.1/6089`, read 20261102 19:44 UTC; IBM Research listing of the SEQUEL paper, `https://research.ibm.com/publications/sequel-a-struciured-english-query-language`, read 20261102 19:49 UTC (the page spells "struciured"; it lists authors as Chamberlin and Boyce with date 1 May 1974 and venue SIGFIDET 1974). A web search at 19:48 UTC was a lead only.
- **S5.** John McCarthy, "Programs with Common Sense" page, `http://www-formal.stanford.edu/jmc/mcc59.html`, read 20261102 19:50 UTC (first-party).
- **S6.** John F. Sowa, "Semantic Networks" (secondary survey by a proponent of conceptual graphs), `http://www.jfsowa.com/pubs/semnet.htm`, read 20261102 19:51 UTC through the fetch tool's summary; quotations are as the tool returned them and should be re-checked against the page.
- **S7.** Buchanan and Shortliffe (eds.) 1984, contents page, `https://people.dbmi.columbia.edu/~ehs7001/Buchanan-Shortliffe-1984/MYCIN%20Book.htm`, read 20261102 19:52 UTC (contents only).
- **S8.** Interlisp bibliography record for the Cyc paper, `https://interlisp.org/history/bibliography/qxtftccf/`, read 20261102 19:44 UTC (record and abstract summary).
- **S9.** IJCAI-77 proceedings PDF for Feigenbaum, `https://www.ijcai.org/Proceedings/77-2/Papers/092.pdf`, fetched 20261102 19:52 UTC; scanned images, text not readable.
- **S11.** Semantic Scholar Graph API, `POST https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,year,venue,citationCount,publicationDate,externalIds,authors`, 39 DOI ids, read 20261102 19:55 UTC (after HTTP 429 on every earlier call from 19:41). Supports the Semantic Scholar counts table.
- **S10.** Wang et al., "BM25 Wins at Scale: A Scaling Study of Retrieval-Augmented Generation Paradigms", `https://arxiv.org/abs/2607.26497`, read 20261102 19:54 UTC (v1 20260729, v3 20260731; abstract only).
- **Archive pages used as leads** (not re-verified here; each carries its own read time): `kb-kg/primer/README.md` (rows 1963, 1974, 1975 to 1979, 1970s to 1980s, 1985, 20040210, 20100225; sources 1, 5, 11, 15, 19, 21), `kb-kg/papers-benchmarks/README.md` (BM25 Wins at Scale row).
- **Not reachable, for the record:** Semantic Scholar API (HTTP 429, 19:41 to 19:54); ACM Digital Library, ScienceDirect, DTIC, dblp (HTTP 403 or bot check); arXiv PDF of the Hogan et al. survey and Imperial/Texas PDFs (no text layer or certificate error).
