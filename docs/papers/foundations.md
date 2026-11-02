---
type: papers
group: foundations
order: 1
updated: 20261102 23:25 UTC
---

# Papers: foundations

This page holds the papers that predate every current trend of chapter 2, from the semantic network of Quillian in 1967 to the retrieval-augmented generation survey of 2023. They run across the four threads of this documentation: KB/KG; ontologies and the semantic web; databases and search; and RAG and agent memory. The sections follow the year of the first version, and the eras they belong to are told in [the history chapter](../history/README.md). Each section names the test the paper passes (origin, turning point, widely built on, survey of record); a citation count is given with its source and read time and is never compared with a count from another source.

## Quillian (1967)

**Word Concepts: A Theory and Simulation of Some Basic Semantic Capabilities.** M. Ross Quillian (1 author). *Behavioral Science* 12(5), pp. 410-430. First version: 196709 [1]. Link: https://doi.org/10.1002/bs.3830120511

**Why fundamental:** *Origin* of the semantic network as a working program. The abstract has a dictionary "recoded" into "a complex network of elements and associations" [2]. Miller and colleagues write that the first person to claim explicitly that lexical memory for nouns forms an inheritance system "seems to have been Quillian (1967, 1968)" [3]. Sowa credits Quillian with the marker-passing algorithm for spreading activation [4]. *Widely built on:* 827 citations (Semantic Scholar, read 20261102 19:55 UTC) [5]. Caveat: the surveys date the line from earlier work. Gutierrez and Sequeda say semantic networks were introduced in 1956 by Richens and that the notion was "developed independently by several people", Quillian's 1963 paper among them [7]; Hogan and colleagues list Richens (1956) before Quillian (1963) [6]. So this journal paper is the first of the line with an abstract read here, not the first idea.

**Idea:** A body of dictionary information is turned into a network of elements and associations. A program uses it to compare and contrast the meanings of two words, draw inferences and write English text expressing its conclusions. The authors offer the design as a theory of how human memory for semantic material may be formatted, organised and used [2]. Sowa says Quillian combined Selz's networks with the semantic nets of machine translation [4]; no paper of this chapter precedes it.

**Relations:** None.

**Read:** abstract (Crossref and OpenAlex records), 20261102 20:41 and 20:46 UTC. Full text not read: the publisher page returned HTTP 403.

## Codd (1970)

**A Relational Model of Data for Large Shared Data Banks.** E. F. Codd (1 author). *Communications of the ACM* 13(6), pp. 377-387. First version: 197006 (received 196909, revised 197002, as the paper states) [1][8]. Link: https://doi.org/10.1145/362384.362685

**Why fundamental:** *Origin* of the relational model: the abstract introduces "A model based on n-ary relations, a normal form for data base relations, and the concept of a universal data sublanguage" [8]. *Turning point:* Gutierrez and Sequeda call it the core of "data independence" and say the first relational systems implemented "the 'vision' of the relational model as described by Codd", leading to SQL [7]. *Widely built on:* 3,675 citations (Semantic Scholar, read 20261102 19:55 UTC) [5].

**Idea:** Users of large data banks must be protected from knowing how data is stored. Existing systems gave tree-structured files or slightly more general network models, which tie programs to ordering, indexing and access paths. Codd describes data as n-ary relations with a normal form, so that programs survive changes in storage [8]. The data models it replaces are the tree and network models of its day, whose references the paper gives as Bachman (1965) and McGee (1969); neither is a paper of this chapter [8].

**Relations:** None.

**Read:** full text (11 pages), 20261102 20:41 UTC.

## Sparck Jones (1972)

**A Statistical Interpretation of Term Specificity and Its Application in Retrieval.** Karen Spärck Jones (1 author). *Journal of Documentation* 28(1), pp. 11-21. First version: 197201 [1]. Link: https://doi.org/10.1108/eb026526

**Why fundamental:** *Origin* of inverse document frequency. The abstract argues that "terms should be weighted according to collection frequency, so that matches on less frequent, more specific, terms are of greater value" [2]. It does not use the name idf; Sanderson and Croft say her paper "introduced" the idea and that its combination with term frequency was "quickly adopted" [9]. *Widely built on:* 5,628 citations (Semantic Scholar, read 20261102 19:55 UTC) [5].

**Idea:** Specificity of an index term should be read statistically, as a function of how the term is used in a collection, not of its meaning. Experiments on three test collections show that frequent terms are still needed for good overall performance. Weighting matches on rarer terms higher gave "considerable improvements" by "this very simple procedure" [2]. It answers the view that the exhaustivity of document descriptions and the specificity of index terms are independent, which the abstract says is "usually regarded as independent" [2]. Sanderson and Croft say her work complemented Luhn's term-frequency weights: they cite Luhn's 1958 paper "The automatic creation of literature abstracts" for term-frequency weighting (not a paper of this chapter) and Luhn's 1957 paper, in Further reading as [Luhn (1957)](./foundations.md), for ranked retrieval; the abstract cites nothing [2][9].

**Relations:** None.

**Read:** abstract (OpenAlex record), 20261102 20:45 UTC. Full text not read: the publisher page returned HTTP 403.

## Minsky (1974)

**A Framework for Representing Knowledge.** Marvin Minsky (1 author). MIT Artificial Intelligence Laboratory Memo AIM-306. First version: 19740601 [10]. Link: https://dspace.mit.edu/handle/1721.1/6089

**Why fundamental:** *Origin* of frames: the abstract defines a frame as "a data-structure for representing a stereotyped situation", with fixed top levels and slots filled by instances [10]. *Turning point:* Hogan and colleagues list the introduction of frames by Minsky (1974) among the influential developments of the 1970s and call frames, semantic networks and conceptual graphs "direct predecessors of Description Logics" [6]; Gutierrez and Sequeda also date frames to this memo [7]. *Widely built on:* not claimed. No citation count for the memo itself is available in the sources read: OpenAlex has no record of the memo, only of three republications of its text, which are not counts of it and are not summed (read 20261102 19:43 to 19:52 UTC) [11].

**Idea:** On meeting a new situation, one selects from memory a frame, a remembered framework adapted by changing details. Each frame carries information on how to use it, what to expect next and what to do if expectations fail. Related frames form frame-systems, with transformations between them standing for changes of viewpoint, as in vision [10]. The abstract names no earlier paper; it says only that the memo combines "classical and modern concepts from psychology, linguistics, and AI" [10].

**Relations:** None.

**Read:** abstract (DSpace record), 20261102 20:41 UTC. The memo PDF could not be downloaded (HTTP 429), so full text not read.

## Woods (1975)

**What's in a Link: Foundations for Semantic Networks.** William A. Woods (1 author). BBN report for ARPA (DTIC ADA022584); also a chapter in Bobrow and Collins (eds.), *Representation and Understanding*, Academic Press, pp. 35-82 [1][4]. First version: 19751101 (Crossref issue date of the DTIC DOI) [69]. Link: https://doi.org/10.21236/ada022584

**Why fundamental:** *Turning point* for semantic networks. Gutierrez and Sequeda give it as "a representation of this criticism" of their weak logical foundation [7]. Hogan and colleagues name it, with Brachman, among the formalisations of semantic networks, quoting Sowa: the networks "have no well-defined semantics" [6]. Sowa says description logics derive from "an approach proposed by Woods (1975)" [4]. Counts are low and understate its role: 245 citations (OpenAlex, report record, read 20261102 19:43 UTC) [11]; 56 (Crossref, read 20261102 19:46 UTC [12] and again at 21:21 UTC [69]). The two sources are not compared.

**Idea:** Not read in full. The surveys agree that it asks what the links of a semantic network mean, since networks were drawn and used without a defined semantics, and asks for a formal account of them [4][6][7]. It answers the missing semantics of semantic networks, a line that begins, in this chapter, with [Quillian (1967)](./foundations.md); no source read says that the report cites that paper, and the report text was not read.

**Relations:** None.

**Read:** bibliographic record (Crossref, 20261102 20:41 UTC) and the survey passages above. The DTIC page returned HTTP 403: report text not read.

## Salton, Wong and Yang (1975)

**A Vector Space Model for Automatic Indexing.** G. Salton, A. Wong, C. S. Yang (3 authors). *Communications of the ACM* 18(11), pp. 613-620. First version: 197511 [1]. Link: https://doi.org/10.1145/361219.361220

**Why fundamental:** *Origin* of the vector space model. Sanderson and Croft write that Salton "synthesised the outputs of his group's work on vectors to produce the vector space model", and their reference for it is this paper [9]. Caveat: the abstract speaks of an indexing "property" space and "space density"; it mentions neither term weights nor cosine. The same survey credits the cosine measure to Salton's earlier book [9]. *Widely built on:* 8,535 citations (Semantic Scholar, read 20261102 19:55 UTC) [5]. Viewing documents and queries as vectors "is still common" [9].

**Idea:** In document retrieval the best indexing space is one where each document lies as far as possible from the others, so the value of an indexing system can be expressed through the density of the document space; retrieval performance may correlate inversely with that density. Space-density computations are used to choose an indexing vocabulary [2]. It is related by subject to [Sparck Jones (1972)](./foundations.md), as both concern term weighting for retrieval; Sanderson and Croft credit the tf-idf combination to a 1973 technical report by Salton and Yang, not to this paper [9]. The abstract cites no earlier paper.

**Relations:** None.

**Read:** abstract (Crossref and OpenAlex records), 20261102 20:41 and 20:45 UTC. Full text not read: the publisher page returned HTTP 403.

## Feigenbaum (1977)

**The Art of Artificial Intelligence: I. Themes and Case Studies of Knowledge Engineering.** Edward A. Feigenbaum (1 author). Proceedings of the Fifth IJCAI (IJCAI-77), Cambridge, MA, pp. 1014-1028. First version: 1977; the month is unstated in the pages read [13]. Link: https://www.ijcai.org/Proceedings/77-2/Papers/092.pdf

**Why fundamental:** *Origin* of the name "knowledge engineering", on the author's own account (first-party): Donald Michie called DENDRAL "epistemological engineering" in 1968, "that I simplified into 'knowledge engineering'" [13]. *Turning point:* the paper states the thesis that agents "must be knowledge-rich, even if they are methods-poor" and calls the acquisition of domain knowledge "the bottleneck problem" [13]. Gutierrez and Sequeda trace the fields of knowledge engineering and ontology engineering to the knowledge-acquisition-bottleneck workshops [7], and the title of the Cyc paper of 1985 names the same bottleneck [14]. The count is modest: 534 citations (OpenAlex, report record, read 20261102 19:43 UTC) [11]; "widely built on" is not claimed.

**Idea:** Expert-level performance comes from acquiring an expert's knowledge, representing it and using it to build and explain lines of reasoning. PUFF, for example, holds 55 IF-THEN rules extracted from 100 cases. DENDRAL, META-DENDRAL and MYCIN serve as case studies [13]. The Stanford DENDRAL and MYCIN projects are its case studies, not papers of this chapter. [Lenat et al. (1985)](./foundations.md) name the same bottleneck [13][14].

**Relations:** None.

**Read:** full text (16 pages, text layer with scanning noise), 20261102 20:42 UTC.

## Brachman and Schmolze (1985)

**An Overview of the KL-ONE Knowledge Representation System.** Ronald J. Brachman, James G. Schmolze (2 authors). *Cognitive Science* 9(2), pp. 171-216. First version: 1985 (198504 per OpenAlex, 198506 per Crossref) [1][2]. Link: https://doi.org/10.1016/s0364-0213(85)80014-8

**Why fundamental:** *Origin* of description logics. Hogan and colleagues: "Description Logics stem from the KL-ONE system proposed by Brachman and Schmolze (1985)" [6]. They add that DLs "have heavily influenced the Web Ontology Language" (their Section 4.3.2) and "formed the underpinnings" of the OWL standard (their Appendix B) [28]. Gutierrez and Sequeda list KL-ONE among the systems of the line [7]. Sowa dates the system itself earlier, to an approach of Woods (1975) implemented by Brachman (1979) [4]; this paper is the overview. *Widely built on:* 2,146 citations (Semantic Scholar, read 20261102 19:55 UTC) [5].

**Idea:** KL-ONE represents knowledge as complex structured descriptions of concepts, arranged in a taxonomy. A classifier places each new description in that taxonomy automatically. The paper presents the kernel ideas and an extended recognition example [2]. Sowa says KL-ONE implements the approach of Woods (1975) [4]. Hogan and colleagues call frames, semantic networks and conceptual graphs "direct predecessors of Description Logics" [6], which were "initially introduced as a way to formalise" them [28]; the missing formal semantics of those networks is what description logics "aimed to give" [6].

**Relations:** Builds on: [Woods (1975)](./foundations.md), [Minsky (1974)](./foundations.md).

**Read:** abstract (OpenAlex record), 20261102 20:45 UTC. Full text not read: the publisher page returned HTTP 403.

## Lenat et al. (1985)

**CYC: Using Common Sense Knowledge to Overcome Brittleness and Knowledge Acquisition Bottlenecks.** Douglas B. Lenat, Mayank Prakash, Mary Shepherd (3 authors). *AI Magazine* 6(4), Winter 1985, pp. 65-85 (pages from OpenAlex; the AAAI and Interlisp records give 65 only). First version: 1985, and the records disagree on the date: the AAAI issue record of Vol. 6 No. 4 says 19851215 [71], the AAAI record of the article alone says 19850315 [70], the Interlisp copy also says 19850315 [14], and OpenAlex says 19860101 [2]. Link: https://doi.org/10.1609/aimag.v6i4.510

**Why fundamental:** *Origin* of Cyc, the first published description of MCC's project to build "a large knowledge base (or KB) of real world facts and heuristics" over a decade [14]. Gutierrez and Sequeda say it came out of MCC and aimed at the largest common-sense KB [7]. Lenat's later account dates the project to 1984: "Since 1984, a person-century of effort has gone into building CYC" (*Communications of the ACM* 38(11), 1995) [72]; Hogan and colleagues give 900 person-years and 2.2 million facts and rules since 1986 [6]. Citations are modest, 406 (Semantic Scholar, read 20261102 19:55 UTC) [5]; the test is not claimed.

**Idea:** Brittleness and the manpower to build knowledge are the main limits on large software, and expert-system history shows them. Machine learning, automatic programming and language understanding each fail to scale for want of a large base of real-world knowledge, so the authors propose to build that base by hand, with reasoning methods inside it [2][14]. It is related by subject to [Feigenbaum (1977)](./foundations.md): its title names the knowledge-acquisition bottleneck of expert systems, which Feigenbaum calls "the bottleneck problem", and the abstract cites "the recent history of expert systems" [2][13]; no source read says that it cites that paper, and no earlier paper is cited in the records read.

**Relations:** None.

**Read:** abstract (Interlisp record 20261102 20:41 UTC; OpenAlex record 20:45 UTC), and the AAAI article and issue records as Internet Archive captures (article capture 20260216 13:10 UTC, issue capture 20240317 12:12 UTC), read 20261102 23:13 and 23:14 UTC [70][71]. The full text was not read.

## Miller et al. (1990)

**Introduction to WordNet: An On-line Lexical Database.** George A. Miller, Richard Beckwith, Christiane Fellbaum (5 authors; also Derek Gross, Katherine J. Miller). *International Journal of Lexicography* 3(4), pp. 235-244. First version: 1990 (the report read is revised 199308) [1][3]. Link: https://doi.org/10.1093/ijl/3.4.235. The 1995 overview by Miller alone, "WordNet", is *Communications of the ACM* 38(11), pp. 39-41 [1].

**Why fundamental:** *Origin* of WordNet: the report describes "the state of WordNet as of 1990", with work begun at Princeton in 1985 [3]. *Widely built on:* 2,249 citations for this paper and 9,187 for the 1995 overview (both Crossref, read 20261102 20:00 UTC) [15]. Hogan and colleagues use WordNet as the sense lexicon for word-sense disambiguation [6].

**Idea:** English nouns, verbs and adjectives are organised into synonym sets, each "one underlying lexical concept", linked by relations such as hyponymy and part-whole. The design follows psycholinguistic theories of human lexical memory and arranges words by meaning, not spelling. The 1993 report counts about 95,600 word forms in some 70,100 meanings [3]. It cites Quillian (1967) for the claim that noun memory is an inheritance system [3]. It introduces the resource described on the [WordNet dataset page](../datasets/wordnet.md).

**Relations:** Builds on: [Quillian (1967)](./foundations.md).

**Read:** the introduction and the passage on noun hierarchies of the report (not all 86 pages), 20261102 20:42 UTC; the 1995 abstract (Crossref), 20:41 UTC.

## Gruber (1993)

**A Translation Approach to Portable Ontology Specifications.** Thomas R. Gruber (1 author). *Knowledge Acquisition* 5(2), pp. 199-220. First version: 199209 (Stanford KSL Technical Report 92-71), revised 199304; journal issue 199306 [1][16]. Link: https://doi.org/10.1006/knac.1993.1008

**Why fundamental:** *Origin* of the working definition of "ontology" in AI: "An ontology is an explicit specification of a conceptualization" [16]. Noy and McGuinness cite it for the term [17]. Whether earlier AI papers used the word is unstated in the sources read. Gutierrez and Sequeda quote the later "shared and formal" wording from Gruber's 1995 paper instead [7]. *Widely built on:* 8,595 citations (Crossref, read 20261102 19:59 UTC) [15]; 12,781 (OpenAlex, read the same day between 19:44 and 19:58 UTC) [18]. The two sources are not compared.

**Idea:** Sharing and reusing formal knowledge needs a common vocabulary: an ontology specifies the classes, relations and functions of a domain. Ontolingua writes definitions once in a predicate-calculus format and translates them into frame systems, relational languages and Loom, keeping each target's efficiency [16]. Related by subject only: frame systems and KL-ONE-style systems are the targets of its translations (Loom is "a KL-ONE style system"); it cites neither [Minsky (1974)](./foundations.md) nor [Brachman and Schmolze (1985)](./foundations.md) [16]. It names Cyc's global ontology as an example of a comprehensive content ontology, citing the 1990 book.

**Relations:** None.

**Read:** the technical-report version (27 pages): abstract, introduction, the Ontolingua sections and the discussion, 20261102 20:43 UTC.

## Robertson et al. (1994)

**Okapi at TREC-3.** Stephen E. Robertson, S. Walker, S. Jones and 2 others (5 authors; Hancock-Beaulieu and Gatford complete the list) [19]. Third Text REtrieval Conference (TREC-3), NIST. First version: 1994 (the NIST listing files it under TREC-3 (1994) [20]; the Microsoft Research record dates it 199501 [19]). Link: https://www.microsoft.com/en-us/research/publication/okapi-at-trec-3/

**Why fundamental:** *Origin.* This is the report in which the ranking function [BM25](../index/bm25.md) appears: "we in effect combined BM11 and BM15 into a single function BM25" [19]. A citation count for this report is **unstated** (no source read gives one), so "widely built on" is not claimed for it; the survey of the family, [Robertson and Zaragoza (2009)](./foundations.md), has a count. A later abstract shows use: Karpukhin et al. (2020) call "TF-IDF or BM25" the de facto method of passage retrieval [21].

**Idea:** Score a document by summing per-term weights built from term frequency and document length, on top of the classical probabilistic relevance weight. BM25 merges two earlier variants with one constant: with b = 1 it gives BM11, with b = 0 it gives BM15 [19]. It ranks over an [inverted index](../index/inverted-index.md). The report builds on the "classical" probabilistic model that its system used at TREC-1 [19], which is [Robertson and Spärck Jones (1976)](./foundations.md) in Further reading. [Karpukhin et al. (2020)](./foundations.md) compare a dense retriever with a Lucene BM25 system [21], and cite the survey of the family, [Robertson and Zaragoza (2009)](./foundations.md), for BM25, not this report [23]. The scaling study BM25 Wins at Scale (2026, in the further reading of [Graph-based RAG](./graph-based-rag.md)) reports that BM25 leads at every larger shared tier above about 10 million corpus tokens (that study's own result, v3) [24].

**Relations:** Builds on: also: Robertson and Spärck Jones (1976).

**Read:** full text of the 18-page report, searched for the BM25 passages, 20261102 20:46 UTC [19].

## Brin and Page (1998)

**The Anatomy of a Large-Scale Hypertextual Web Search Engine.** Sergey Brin, Lawrence Page (2 authors). *Computer Networks and ISDN Systems* 30(1-7), pp. 107-117. First version: 199804 [1]. Link: https://doi.org/10.1016/s0169-7552(98)00110-x

**Why fundamental:** *Origin* of Google and of PageRank as a published ranking method: "a prototype of a large-scale search engine which makes heavy use of the structure present in hypertext" [25]. Sanderson and Croft call PageRank the "more famous use of link analysis" [9]. *Widely built on:* 9,354 citations (Crossref, read 20261102 19:59 UTC; a 2012 reprint record is separate) [15]. The paper notes that damping can be applied "to a single page, or a group of pages" for personalization [25]; HippoRAG's abstract combines LLMs, knowledge graphs and "the Personalized PageRank algorithm" [26]. Full PageRank details are in a technical report outside this chapter [25].

**Idea:** Crawl and index the Web at scale and rank pages by the link graph. PageRank extends citation counting: a link counts by the importance of the linking page, divided by its out-links, with damping 0.85 and a "random surfer" reading [25]. It builds on academic citation analysis (no paper of this chapter). It answers the limits of "the standard vector space model" on the Web, the model of [Salton, Wong and Yang (1975)](./foundations.md), which it names but does not cite [25].

**Relations:** None.

**Read:** full text of the printed version (11 pages), 20261102 20:44 UTC.

## Berners-Lee et al. (2001)

**The Semantic Web.** Tim Berners-Lee, James Hendler, Ora Lassila (3 authors). *Scientific American* 284(5), 200105. First version: 20010501 [27]. Link: https://doi.org/10.1038/scientificamerican0501-34

**Why fundamental:** *Origin* of the [Semantic Web](../index/semantic-web.md) as a field, on a survey's account: Hitzler says the article "arguably marks the birth of the field" and gave the nascent field "significant visibility", while noting that dating a field's birth is "debateable at best" [67]. Its standfirst promises "A new form of Web content that is meaningful to computers" [27]. *Widely built on.* 8,727 citations (Crossref, a lower bound, read 20261102 20:00 UTC) [15]. The Hogan et al. survey lists it in its references [28].

**Idea:** Most Web content is written for people. The article proposes adding machine-readable meaning, so that software agents can act on page content. It makes the case through a scenario of agents arranging appointments and through sections on expressing meaning, knowledge representation, [ontologies](../index/ontology.md) and agents [29]. No earlier paper is named in the sources read here (**unstated**). [Auer et al. (2007)](./foundations.md) say that the broader Semantic Web vision "has not yet been realized" and that getting enough useful data into it is a main obstacle [30]; [Bizer et al. (2009)](./foundations.md) place Linked Data inside its context [31].

**Relations:** None.

**Read:** the publisher page (title, authors, date, standfirst), 20261102 20:44 UTC [27]; Hitzler's review, the passages on the 2001 article, 20261102 21:20 UTC [67]. The article's body is carried over from the first reading of a four-page copy, 20261102 20:01 to 20:04 UTC [29]; it was not re-read.

## Suchanek et al. (2007)

**YAGO: A Core of Semantic Knowledge. Unifying WordNet and Wikipedia.** Fabian M. Suchanek, Gjergji Kasneci, Gerhard Weikum (3 authors). 16th International World Wide Web Conference (WWW 2007), Banff, 20070508 to 20070512. First version: 20070508 (conference start; Crossref issue date, carried over) [32]. Link: https://doi.org/10.1145/1242572.1242667

**Why fundamental:** *Origin.* The abstract presents YAGO as "a light-weight and extensible ontology with high coverage and quality": "more than 1 million entities and 5 million facts", an accuracy "of about 95%" (the authors' own figures) [32]. *Widely built on.* 2,509 citations (Crossref, lower bound, read 20261102 19:59 UTC) [15]. The Knowledge Vault abstract names YAGO among the large knowledge bases it wants to outgrow [33], the DBpedia paper uses its classification [30], and the Hogan et al. survey cites it [28].

**Idea:** Take the facts about individuals in Wikipedia (categories and infoboxes) and attach them to the clean is-a hierarchy of WordNet, using rule-based and heuristic methods. The result is a [knowledge base](../index/knowledge-base.md) with "a logically clean model, which is decidable, extensible, and compatible with RDFS" [32] ([YAGO](../index/yago.md)). It builds on WordNet ([Miller et al. (1990)](./foundations.md)) and Wikipedia as its two sources [32]. [Auer et al. (2007)](./foundations.md), written in the same year from the same source, call YAGO "a second project that also works on extracting structured information from Wikipedia" [30]. Data: [YAGO](../datasets/yago.md), [WordNet](../datasets/wordnet.md).

**Relations:** Builds on: [Miller et al. (1990)](./foundations.md).

**Read:** abstract and the first pages of the full text (10 pages), 20261102 20:43 UTC.

## Auer et al. (2007)

**DBpedia: A Nucleus for a Web of Open Data.** Sören Auer, Christian Bizer, Georgi Kobilarov and 3 others (6 authors). *The Semantic Web* (ISWC/ASWC 2007), Springer LNCS, pp. 722-735. First version: 2007; the day is **unstated**. The paper cites YAGO (20070508) and Wikipedia traffic for the third quarter of 2007, so it is later than YAGO [30]. Link: https://doi.org/10.1007/978-3-540-76298-0_52

**Why fundamental:** *Origin.* The abstract describes [DBpedia](../index/dbpedia.md) as "a community effort to extract structured information from Wikipedia and to make this information available on the Web" [30]. It reports 103 million RDF triples, and around 2 billion triples once interlinked with other open datasets (the authors' figures) [30]. *Widely built on.* 2,448 citations (Crossref, lower bound, read 20261102 20:00 UTC) [15]; the Hogan et al. survey cites it [28].

**Idea:** Convert Wikipedia content into [RDF](../index/rdf.md) with an extraction framework, publish it as [Linked Data](../index/linked-data.md) with query interfaces, and link it to other datasets so that it can serve as a hub for a Web of open data [30]. It frames its aim as supplying the broad data that the Semantic Web vision of [Berners-Lee et al. (2001)](./foundations.md) lacked [30]. It uses the YAGO classification of [Suchanek et al. (2007)](./foundations.md) in a "Yago Types" dataset of 1.9 million rdf:type statements for DBpedia instances, and says that YAGO "extracts only 14 relationship types" [30]. Data: [DBpedia](../datasets/dbpedia.md).

**Relations:** Builds on: [Berners-Lee et al. (2001)](./foundations.md), [Suchanek et al. (2007)](./foundations.md).

**Read:** abstract and the first two pages of the full text (14 pages), 20261102 20:45 UTC; the Related Work section and the dataset table re-read 20261102 21:19 to 21:22 UTC. The Crossref count and the Springer record are carried over (the publisher page redirected to a login).

## Bollacker et al. (2008)

**Freebase: a collaboratively created graph database for structuring human knowledge.** Kurt Bollacker, Colin Evans, Praveen Paritosh and 2 others (5 authors; Tim Sturge and Jamie Taylor). SIGMOD 2008. First version: 20080609 (Crossref issue date, carried over) [34]. Link: https://doi.org/10.1145/1376616.1376746

**Why fundamental:** *Origin.* The abstract describes [Freebase](../index/freebase.md) as "a practical, scalable tuple database used to structure general human knowledge", with "more than 125,000,000 tuples, more than 4000 types, and more than 7000 properties" (first-party figures) [34]. *Widely built on.* 3,284 citations (Crossref, lower bound, read 20261102 19:59 UTC) [15]. Google's 2012 Knowledge Graph announcement says the graph "isn't just rooted in public sources such as Freebase" [35]; TransE built its FB15k benchmark data from Freebase [36]; the Knowledge Vault abstract names it [33].

**Idea:** A tuple store that the public can read and write through an HTTP graph-query API, with the Metaweb Query Language (MQL) for object-style queries. Data is created, structured and maintained collaboratively [34]. No earlier paper is named on the page read (**unstated**). Unlike DBpedia and YAGO, which extract from Wikipedia, Freebase is edited directly [30][32]; [Bordes et al. (2013)](./foundations.md) and [Dong et al. (2014)](./foundations.md) later use it as data. Data: [Freebase](../datasets/freebase.md).

**Relations:** None.

**Read:** the Google Research page with the abstract, 20261102 20:43 UTC. The full text was not read.

## Bizer et al. (2009)

**Linked Data: The Story So Far.** Christian Bizer, Tom Heath, Tim Berners-Lee (3 authors). *International Journal on Semantic Web and Information Systems* 5(3), pp. 1-22. First version: 2009 (month **unstated** on the record read) [37]. Link: https://doi.org/10.4018/jswis.2009081901

**Why fundamental:** *Survey of record* for [Linked Data](../index/linked-data.md) at the end of its first three years. Its abstract says: "We present the concept and technical principles of Linked Data, and situate these within the broader context of related technological developments" [31]. *Widely built on.* 2,525 citations for the journal version (Crossref, lower bound, read 20261102 20:00 UTC) [15].

**Idea:** Linked Data is a set of best practices for publishing and connecting structured data on the Web, using [URIs](../index/uri.md) and [RDF](../index/rdf.md). In three years, many data providers adopted them, giving a global data space of billions of assertions, the Web of Data. The paper reviews publishing progress and applications and sets a research agenda [37]. It places Linked Data inside the Semantic Web context of [Berners-Lee et al. (2001)](./foundations.md), and builds on the Linked Data design note by Berners-Lee (2006), a W3C note and not a paper (both carried over from the first reading, not re-verified) [31].

**Relations:** Builds on: [Berners-Lee et al. (2001)](./foundations.md).

**Read:** the EconPapers record (title, authors, volume, pages), 20261102 20:46 UTC [37]. The abstract and first page of the preprint were read in the first pass, 20261102 20:03 UTC, and not re-read because the preprint host had a certificate error today [31].

## Robertson and Zaragoza (2009)

**The Probabilistic Relevance Framework: BM25 and Beyond.** Stephen Robertson, Hugo Zaragoza (2 authors). *Foundations and Trends in Information Retrieval* 4(1-2), pp. 1-174. First version: 20090917 (Crossref issue date; the publisher page gives the same date) [68][22]. Link: https://doi.org/10.1561/1500000019

**Why fundamental:** *Survey of record* for the probabilistic relevance framework and for [BM25](../index/bm25.md). The abstract presents the framework "from a conceptual point of view" and covers "the binary independence model, relevance feedback models, BM25 and BM25F" [68]. Karpukhin et al. (2020) cite it for BM25 [23]. *Widely built on.* 2,759 citations (Crossref, a lower bound, read 20261102 21:21 UTC) [68].

**Idea:** The framework is a formal model of document retrieval, grounded in work of the 1970s and 1980s, and it leads to the ranking function BM25. A later extension, BM25F, takes into account document metadata such as structure and link-graph information. The monograph also relates the framework to other statistical models of retrieval and covers non-textual features and parameter optimisation [68]. It builds on "work done in the 1970-1980s" that the abstract does not name; the reference list was not read (**unstated**) [68]. [Robertson and Spärck Jones (1976)](./foundations.md) in Further reading is of that period but is not shown here to be cited. Whether it cites [Robertson et al. (1994)](./foundations.md), the report in which BM25 appears [19], is **unstated**.

**Relations:** None.

**Read:** abstract (Crossref record), 20261102 21:21 UTC [68]; title, authors, volume, pages and date at the publisher, 20261102 20:47 UTC [22]. Full text (174 pages) not read.

## Bordes et al. (2013)

**Translating Embeddings for Modeling Multi-relational Data.** Antoine Bordes, Nicolas Usunier, Alberto García-Durán and 2 others (5 authors; Jason Weston and Oksana Yakhnenko). Advances in Neural Information Processing Systems 26 (NIPS 2013). First version: 2013 (month **unstated**) [38]. Link: https://papers.nips.cc/paper_files/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html

**Why fundamental:** *Origin* of translation-based [knowledge graph embedding](../index/knowledge-graph-embedding.md). The abstract proposes "a method which models relationships by interpreting them as translations operating on the low-dimensional embeddings of the entities" [38]. The paper also creates the FB15k set from [Freebase](../index/freebase.md) ("This data set is denoted FB15k") [36]. *Widely built on.* 5,724 citations (OpenAlex, record without DOI, read 20261102 19:50 UTC) [39]. The Hogan et al. survey cites it and draws a TransE example [28].

**Idea:** Represent each entity as a vector and each relation as a translation: for a true [triple](../index/triple.md) (head, relation, tail), head + relation should land near tail. The abstract reports better [link prediction](../index/link-prediction.md) than the state of the art on two knowledge bases and training on 1 million entities, 25,000 relations and over 17 million samples [38]. It takes Freebase ([Bollacker et al. (2008)](./foundations.md)) and WordNet ([Miller et al. (1990)](./foundations.md)) as data ("Wordnet and Freebase in this paper") and evaluates on FB15k, WN and a larger Freebase set [36]; see [FB15k-237](../datasets/fb15k-237.md), [WN18RR](../datasets/wn18rr.md) (the pages name FB15k and WN18 as their predecessors) and [link prediction](../benchmarks/kg-link-prediction.md).

**Relations:** Builds on: [Miller et al. (1990)](./foundations.md), [Bollacker et al. (2008)](./foundations.md).

**Read:** abstract page and full text keyword-searched, 20261102 20:44 and 20:49 UTC.

## Dong et al. (2014)

**Knowledge Vault: A Web-Scale Approach to Probabilistic Knowledge Fusion.** Xin Luna Dong, Evgeniy Gabrilovich, Geremy Heitz and 6 others (9 authors). KDD 2014, New York, 20140824 to 20140827, pp. 601-610. First version: 20140824 (conference start; Crossref issue date, carried over) [33]. Link: https://doi.org/10.1145/2623330.2623623

**Why fundamental:** *Widely built on.* 1,533 citations (OpenAlex, read 20261102 19:50 UTC) [39]; 1,080 (Crossref, read 20261102 19:53 UTC) [40]. The two counts come from different sources and are not compared. The Hogan et al. survey cites it [28]. The abstract introduces "a Web-scale probabilistic knowledge base" that combines extractions from text, tables, page structure and human annotations with prior knowledge from existing repositories, and computes "calibrated probabilities of fact correctness" [33]. The authors say it is "substantially bigger than any previously published structured knowledge repository" [33]; no outside source read here confirms that, so no origin or turning point is claimed.

**Idea:** Do not curate facts. Run many extractors over the Web, add priors from existing knowledge bases, fuse them by supervised learning, and keep a probability for each [triple](../index/triple.md) [33]. Its first sentence names Wikipedia, Freebase ([Bollacker et al. (2008)](./foundations.md)), YAGO ([Suchanek et al. (2007)](./foundations.md)), Microsoft's Satori and Google's Knowledge Graph as the large knowledge bases to outgrow [33]. Data: [Freebase](../datasets/freebase.md), [YAGO](../datasets/yago.md).

**Relations:** Builds on: [Suchanek et al. (2007)](./foundations.md), [Bollacker et al. (2008)](./foundations.md).

**Read:** the Google Research page with the full abstract, 20261102 20:44 UTC. The full text was not read.

## Vrandečić and Krötzsch (2014)

**Wikidata: a free collaborative knowledgebase.** Denny Vrandečić, Markus Krötzsch (2 authors). *Communications of the ACM* 57(10), pp. 78-85. First version: 20140923 (Crossref issue date, carried over) [41]. Link: https://doi.org/10.1145/2629489

**Why fundamental:** *Widely built on.* 3,366 citations (OpenAlex, read 20261102 19:50 UTC) [39]; 2,731 (Crossref, read 20261102 19:53 UTC) [40]; not compared. The paper describes [Wikidata](../index/wikidata.md): the abstract presents "a multilingual 'Wikipedia for data'" and gives an overview of the core design decisions, the data model, statistics and application areas (paraphrased from the record) [41]. The project describes itself as "a free, collaborative, multilingual, secondary knowledge base" [42]. [Petroni et al. (2019)](./foundations.md) probe relations between entities stored in Wikidata [43].

**Idea:** One community-edited store of structured statements that the Wikimedia projects, and anyone else, can use as a common source of data [41]. The details of the data model (items, statements, references, ranks) are **unstated** here: the full text was not reachable. No earlier paper is named in the record read (**unstated**); the move of data from Freebase to Wikidata is a lead from the archive and is not verified. [Petroni et al. (2019)](./foundations.md) use its data for cloze probes. Data: [Wikidata](../datasets/wikidata.md).

**Relations:** None.

**Read:** the record and abstract on the TU Dresden page, 20261102 20:48 UTC; the project's introduction page, 20:48 UTC. The full text was not read (ACM pages returned HTTP 403).

## Francis et al. (2018)

**Cypher: An Evolving Query Language for Property Graphs.** Nadime Francis, Alastair Green, Paolo Guagliardo and 7 others (10 authors). SIGMOD 2018, Houston, 20180610 to 20180615 [44]. First version: 20180527 (Crossref issue date, carried over; it precedes the conference days) [44]. Link: https://doi.org/10.1145/3183713.3190657

**Why fundamental:** *Origin* of the formal definition of [Cypher](../index/cypher.md). The abstract describes "Cypher 9, which is the first version of the language governed by the openCypher Implementers Group" and gives a formal semantic definition of its core read queries and its variant of the [property graph](../index/property-graph.md) data model [44]. *Widely built on.* 549 citations (OpenAlex, read 20261102 19:50 UTC) [39]; 514 (Crossref, read 20261102 19:53 UTC) [40]; not compared. The Hogan et al. survey cites it and lists Cypher with Gremlin and G-CORE for property graphs [28].

**Idea:** Cypher began in the Neo4j [graph database](../index/graph-database.md) and is used by several commercial products. The paper introduces it by example, defines the "ASCII Art" pattern matching, compares it with other property-graph query languages, and previews Cypher 10 (graph projections, multiple named graphs) [44]. It builds on the property-graph model of Neo4j and other graph databases, and compares Cypher with other property-graph query languages in the paper itself [44]. See also [GQL](../index/gql.md) for the later standard (not read here). No paper of this chapter answers it (**unstated**).

**Relations:** None.

**Read:** abstract and first pages of the full text (13 pages), 20261102 20:44 UTC.

## Petroni et al. (2019)

**Language Models as Knowledge Bases?** Fabio Petroni, Tim Rocktäschel, Patrick Lewis and 4 others (7 authors; the ACL Anthology lists Sebastian Riedel third instead of Lewis) [45][46]. EMNLP-IJCNLP 2019, 201911 [46]. First version: 20190903 [45]. Link: https://arxiv.org/abs/1909.01066

**Why fundamental:** *Turning point.* It asked whether a pretrained language model can serve as a knowledge base without fine-tuning, and answered with a probe. The abstract finds that "BERT contains relational knowledge competitive with traditional NLP methods that have some access to oracle knowledge" [45]. On open-domain question answering the text reports a precision@10 of 57.1 for BERT-large against 63.5 for DrQA, a supervised system that retrieves with TF-IDF and then reads (Section 5, Table 2) [43]. The introduction describes the 63.5 as "a knowledge base constructed using a task-specific supervised relation extraction system"; the body of the paper contradicts that wording [43]. *Widely built on.* 953 citations (Crossref, EMNLP-IJCNLP record, read 20261102 20:00 UTC) [40]. REALM's introduction cites it [47].

**Idea:** Turn a fact (subject, relation, object) into a fill-in-the-blank sentence and check whether the model predicts the object. The probe covers four corpora: Google-RE relations, T-REx (a subset of Wikidata triples), ConceptNet relations and a subset of SQuAD questions [43]. The authors list advantages of language models over structured knowledge bases: "no schema engineering", an open class of relations, easy extension, no human supervision [45]. It is evaluated on Google-RE, [Wikidata](../datasets/wikidata.md) (through T-REx), [ConceptNet](../datasets/conceptnet.md) and SQuAD [43]. It answers the structured knowledge base, which the abstract compares with language models point by point [45] (for example Wikidata, see [Vrandečić and Krötzsch (2014)](./foundations.md)); no source read shows that it cites that paper. [Guu et al. (2020)](./foundations.md) build on it.

**Relations:** None.

**Read:** abstract and full text keyword-searched, 20261102 20:42 and 20:51 UTC; Section 4, Section 5 and Table 2 re-read 20261102 21:19 to 21:22 UTC.

## Guu et al. (2020)

**REALM: Retrieval-Augmented Language Model Pre-Training.** Kelvin Guu, Kenton Lee, Zora Tung and 2 others (5 authors; Panupong Pasupat and Ming-Wei Chang). ICML 2020, PMLR 119, pp. 3929-3938 [48]. First version: 20200210 [49]. Link: https://arxiv.org/abs/2002.08909

**Why fundamental:** *Origin* of retrieval-augmented language-model pre-training. The abstract claims: "For the first time, we show how to pre-train such a knowledge retriever in an unsupervised manner", using masked language modelling and backpropagation through a retrieval step over millions of documents [49]. It reports gains of 4 to 16 points of absolute accuracy over earlier methods on three open-domain QA benchmarks (first-party) [49]. *Widely built on.* 3,596 citations (Semantic Scholar, read 20261102 20:20 UTC) [50]. RAG and DPR both cite it and compare against it [23][51].

**Idea:** Instead of keeping knowledge only in the weights, a language model retrieves and attends over documents from a corpus such as Wikipedia during pre-training, fine-tuning and inference. The retriever learns from the language-modelling loss alone, with no retrieval labels [49]. Its introduction cites [Petroni et al. (2019)](./foundations.md) for the finding that models hold world knowledge, and ORQA, which uses "a similar latent variable model" (not a paper of this chapter) [47]. It is evaluated on [Natural Questions](../datasets/natural-questions.md) (open), WebQuestions and CuratedTrec [47]. [Lewis et al. (2020)](./foundations.md) answer it, getting strong results "without expensive, specialized 'salient span masking' pre-training" [51].

**Relations:** Builds on: [Petroni et al. (2019)](./foundations.md); also: ORQA (Lee et al. 2019).

**Read:** abstract and full text keyword-searched, 20261102 20:42 and 20:50 UTC; author list re-read 20261102 21:23 UTC.

## Karpukhin et al. (2020)

**Dense Passage Retrieval for Open-Domain Question Answering.** Vladimir Karpukhin, Barlas Oğuz, Sewon Min and 5 others (8 authors). EMNLP 2020, 202011 [52]. First version: 20200410 [21]. Link: https://arxiv.org/abs/2004.04906

**Why fundamental:** *Turning point.* The abstract shows that "retrieval can be practically implemented using dense representations alone" and that the dense retriever "outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy" [21]. The text says dense methods had never been shown to beat TF-IDF/BM25 for open-domain QA before ORQA [23]. *Widely built on.* 7,702 citations (Semantic Scholar, read 20261102 20:20 UTC) [50]. RAG initialises its retriever from it [51].

**Idea:** Two BERT encoders map questions and passages into one vector space, and retrieval is nearest-neighbour search over passage vectors. The encoders are trained from a small number of question-passage pairs, with no extra pre-training stage [21]. This is [dense retrieval](../index/dense-retrieval.md) for [open-domain question answering](../index/open-domain-question-answering.md). ORQA (Lee et al., 2019), not a paper of this chapter, was the first to show dense retrieval beating BM25 in this task; DPR criticises it for two weaknesses [23]. DPR cites the BM25 monograph [Robertson and Zaragoza (2009)](./foundations.md) for BM25 [23]. It is evaluated on [Natural Questions](../datasets/natural-questions.md), [TriviaQA](../datasets/triviaqa.md), WebQuestions, CuratedTREC and SQuAD, over a 201812 Wikipedia dump split into 100-word passages [23] ([passage corpus](../datasets/wikipedia-dpr-kilt.md)); its table also lists REALM [23].

**Relations:** Builds on: also: ORQA (Lee et al. 2019). Answers: [Robertson and Zaragoza (2009)](./foundations.md).

**Read:** abstract and full text keyword-searched, 20261102 20:42 and 20:50 UTC.

## Lewis et al. (2020)

**Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.** Patrick Lewis, Ethan Perez, Aleksandra Piktus and 9 others (12 authors). NeurIPS 2020 (arXiv comment) [53]. First version: 20200522 [53]. Link: https://arxiv.org/abs/2005.11401

**Why fundamental:** *Origin of the recipe* for [retrieval-augmented generation](../index/retrieval-augmented-generation.md). The abstract explores "a general-purpose fine-tuning recipe" combining a pre-trained seq2seq model (parametric memory) with a dense vector index of Wikipedia (non-parametric memory) [53]. Gao et al. cite it (their reference 4) among the "foundational work" of the inception stage of RAG [57]. Whether the term itself first appears here is **unstated** in the sources read. *Widely built on.* 20,475 citations (Semantic Scholar, read 20261102 20:20 UTC) [50]; GraphRAG (2024) names itself "a Graph RAG approach" in its title [54].

**Idea:** A generator is conditioned on passages that a neural retriever fetches from an external index, and the two are trained together with the retrieved document as a latent variable. Two variants are compared: one uses the same passages for the whole output, the other can use different passages per token. The paper sets state of the art on three open-domain QA tasks and reports more specific, diverse and factual text than a parametric-only baseline [53]. It builds on REALM and ORQA, "two recently introduced models" with a differentiable retriever [51], and on DPR: "We use a pre-trained bi-encoder from DPR to initialize our retriever" [51]. It is evaluated on [Natural Questions](../datasets/natural-questions.md), [TriviaQA](../datasets/triviaqa.md), WebQuestions, CuratedTrec, [MS MARCO](../datasets/ms-marco.md), Jeopardy question generation and FEVER [51]. Later papers answer it: [Self-RAG (2023)](./agentic-search.md) objects to retrieving "a fixed number of retrieved passages" regardless of need [55], and [GraphRAG (2024)](./graph-based-rag.md) starts from the case where "RAG fails on global questions directed at an entire text corpus" [54].

**Relations:** Builds on: [Guu et al. (2020)](./foundations.md), [Karpukhin et al. (2020)](./foundations.md); also: ORQA (Lee et al. 2019). Answers: [Guu et al. (2020)](./foundations.md).

**Read:** abstract and full text keyword-searched, 20261102 20:42 and 20:49 UTC.

## Hogan et al. (2021)

**Knowledge Graphs.** Aidan Hogan, Eva Blomqvist, Michael Cochez and 15 others (18 authors). *ACM Computing Surveys* 54(4), article 71. First version: 20200304 (arXiv v1; v6 of 20210911 read) [6]. Link: https://arxiv.org/abs/2003.02320

**Why fundamental:** *Survey of record* for the [knowledge graph](../index/knowledge-graph.md). The abstract covers graph data models and query languages, "the roles of schema, identity, and context", deductive and inductive knowledge, creation, enrichment, quality assessment, refinement and publication, and prominent open and enterprise graphs [6]. Citations: 2,144 (OpenAlex, CSUR record, read 20261102 19:50 UTC) [39]; 1,950 (Crossref, read 20261102 20:00 UTC) [40]; not compared.

**Idea:** A single comprehensive introduction. It contrasts graph data models and query languages, explains how knowledge is represented and extracted with deductive and inductive techniques, summarises creation, enrichment, quality, refinement and publication, surveys open and enterprise graphs, and ends with research directions [6]. Its reference list holds the six papers it builds on here [28]. As a survey it evaluates no system; it covers [property graphs](../index/property-graph.md) and RDF graphs side by side [28].

**Relations:** Builds on: [Berners-Lee et al. (2001)](./foundations.md), [Suchanek et al. (2007)](./foundations.md), [Auer et al. (2007)](./foundations.md), [Bordes et al. (2013)](./foundations.md), [Dong et al. (2014)](./foundations.md), [Francis et al. (2018)](./foundations.md).

**Read:** abstract on the arXiv record and the reference list and passages on Cypher, TransE and the open knowledge graphs in the full text (135 pages), keyword-searched, 20261102 20:42 and 20:50 UTC.

## Gao et al. (2023)

**Retrieval-Augmented Generation for Large Language Models: A Survey.** Yunfan Gao, Yun Xiong, Xinyu Gao and 7 others (10 authors). arXiv preprint, comment "Ongoing Work"; no journal stated [56]. First version: 20231218 (v5 of 20240327 read) [56]. Link: https://arxiv.org/abs/2312.10997

**Why fundamental:** *Survey of record* for RAG over [large language models](../index/large-language-model.md). The abstract sorts the work into "the Naive RAG, the Advanced RAG, and the Modular RAG" and into retrieval, generation and augmentation techniques, then adds evaluation frameworks and benchmarks [56]. *Widely built on.* 4,421 citations (Semantic Scholar, read 20261102 20:20 UTC) [50]. The text says its Naive RAG paradigm "gained prominence shortly after the widespread adoption of ChatGPT" [57].

**Idea:** RAG is a response to hallucination, outdated knowledge and untraceable reasoning. The survey walks through the three paradigms, the techniques in each component, and the downstream tasks, datasets and evaluation tools [56][57]. Its references include [Lewis et al. (2020)](./foundations.md) (reference 4) and [Karpukhin et al. (2020)](./foundations.md) (reference 102) [57]. As a survey it evaluates no system; it tabulates the datasets used by RAG work: [Natural Questions](../datasets/natural-questions.md), [TriviaQA](../datasets/triviaqa.md), [MS MARCO](../datasets/ms-marco.md), [HotpotQA](../datasets/hotpotqa.md) and others [57].

**Relations:** Builds on: [Karpukhin et al. (2020)](./foundations.md), [Lewis et al. (2020)](./foundations.md).

**Read:** abstract and full text keyword-searched, 20261102 20:42 and 20:50 UTC; the inception passage re-read 20261102 21:19 to 21:22 UTC.

## Further reading

These papers passed a test of this chapter but a reader of the chapter would miss them less than those above. Each count carries its source and read time; counts from different sources are not compared. Metadata and clauses were carried over from the candidate pools, except for Schlichtkrull et al. and Borgeaud et al., which were read on 20261102 at 21:01 UTC. Every link below was requested on 20261102 at 21:00 UTC and resolved. The DOI links redirect to the publisher; the ACM, Wiley and Emerald sites answered the script with HTTP 403, which blocks scripts and does not mean a missing page, so for those links only the redirect was checked.

- Luhn (1957), [doi 10.1147/rd.14.0309](https://doi.org/10.1147/rd.14.0309): outlines a statistical approach to encoding and searching documents by machine, from the analysis of a collection to a thesaurus-type dictionary; 1,199 citations (Semantic Scholar, read 20261102 19:55 UTC) [5][58].
- Maron and Kuhns (1960), [doi 10.1145/321033.321035](https://doi.org/10.1145/321033.321035): "probabilistic indexing": a computed "relevance number" for each document gives a ranked list; 1,036 citations (Semantic Scholar, read 20261102 19:55 UTC) [5][58].
- Chen (1976), [doi 10.1145/320434.320440](https://doi.org/10.1145/320434.320440): proposes the entity-relationship model and a diagram technique for database design, offered to unify the network, relational and entity-set views; 4,710 citations (OpenAlex, read 20261102 19:43 UTC) and 4,588 (Crossref, read 19:46 UTC), not compared [11][12][58].
- Robertson and Spärck Jones (1976), [doi 10.1002/asi.4630270302](https://doi.org/10.1002/asi.4630270302): derives relevance-weighting functions from a general probabilistic theory of retrieval, as an extension of collection-frequency weighting; 2,560 citations (Semantic Scholar, read 20261102 19:55 UTC) [5][58].
- Newell (1982), [doi 10.1016/0004-3702(82)90012-1](https://doi.org/10.1016/0004-3702(82)90012-1): proposes a computer-system level above the symbol level, the knowledge level; 3,073 citations (Semantic Scholar, read 20261102 19:55 UTC) [5][58].
- Brachman and Levesque (1984), [OpenAlex record W2127140110](https://openalex.org/W2127140110) (no DOI found): shows that small additions to a frame-based description language can make subsumption intractable; 335 citations (OpenAlex, read 20261102 19:43 UTC) [11][58].
- Banko et al. (2007), [IJCAI-07 paper 429](https://www.ijcai.org/Proceedings/07/Papers/429.pdf): Open Information Extraction: one pass over a corpus extracts relational tuples without human input; citation count **unstated** (no DOI) [59].
- Angles and Gutierrez (2008), [doi 10.1145/1322432.1322433](https://doi.org/10.1145/1322432.1322433): survey of graph database models: data structures, query languages and integrity constraints; 749 citations (Crossref, read 20261102 19:59 UTC) [15][60].
- Carlson et al. (2010), [doi 10.1609/aaai.v24i1.7519](https://doi.org/10.1609/aaai.v24i1.7519): NELL, a never-ending language learner that reads the Web every day to grow a knowledge base; 783 citations (Crossref, read 20261102 19:59 UTC) [15][61].
- Yih et al. (2015), [ACL Anthology P15-1128](https://aclanthology.org/P15-1128/): answers questions over a knowledge base by staged query-graph generation, with an F1 of 52.5% on WebQuestions (first-party); 768 citations (OpenAlex, read 20261102 19:50 UTC) and 363 (Crossref, read 19:53 UTC), not compared [39][40][62].
- Ehrlinger and Wöß (2016), [CEUR-WS Vol-1695, paper 4](https://ceur-ws.org/Vol-1695/paper4.pdf): a four-page poster that lists five definitions of "knowledge graph" and shows "the lack of a common core"; 497 citations (OpenAlex, read 20261102 19:50 UTC) [39][63].
- Schlichtkrull et al. (2017), [arXiv 1703.06103](https://arxiv.org/abs/1703.06103): R-GCN: relational graph convolutional networks for link prediction and entity classification on knowledge bases (published in 2018 in Springer's Lecture Notes in Computer Science, *The Semantic Web*); 5,677 citations (OpenAlex, read 20261102 19:50 UTC) and 3,740 (Crossref, read 20:00 UTC), not compared [39][40][64].
- Wang et al. (2017), [doi 10.1109/TKDE.2017.2754499](https://doi.org/10.1109/TKDE.2017.2754499): survey of knowledge graph embedding, sorted by the information each model uses; 2,642 citations (OpenAlex, read 20261102 19:50 UTC) and 2,192 (Crossref, read 19:53 UTC), not compared [39][40][65].
- Borgeaud et al. (2021), [arXiv 2112.04426](https://arxiv.org/abs/2112.04426): RETRO: a language model conditioned on chunks retrieved from a 2 trillion token database; 2,015 citations (Semantic Scholar, read 20261102 20:20 UTC) [50][66].

## Sources

1. https://api.crossref.org/works/10.1002/bs.3830120511, https://api.crossref.org/works/10.1145/362384.362685, https://api.crossref.org/works/10.1108/eb026526, https://api.crossref.org/works/10.21236/ada022584, https://api.crossref.org/works/10.1145/361219.361220, https://api.crossref.org/works/10.1016/s0364-0213(85)80014-8, https://api.crossref.org/works/10.1006/knac.1993.1008, https://api.crossref.org/works/10.1093/ijl/3.4.235, https://api.crossref.org/works/10.1145/219717.219748, https://api.crossref.org/works/10.1016/s0169-7552(98)00110-x : bibliographic records (title, authors, venue, issue date, pages) of Quillian, Codd, Sparck Jones, Woods, Salton, Brachman, Gruber, Miller (1990 and 1995) and Brin; the Cyc DOI (https://api.crossref.org/works/10.1609/aimag.v6i4.510) returns HTTP 404 there (read 20261102 20:41 UTC)
2. https://api.openalex.org/works/doi:10.1002/bs.3830120511, https://api.openalex.org/works/doi:10.1108/eb026526, https://api.openalex.org/works/doi:10.1016/s0364-0213(85)80014-8, https://api.openalex.org/works/doi:10.1145/361219.361220, https://api.openalex.org/works/doi:10.1609/aimag.v6i4.510, https://api.openalex.org/works/doi:10.1145/219717.219748 : abstracts, dates and pages for Quillian, Sparck Jones, Brachman, Salton, Cyc and Miller 1995 (read 20261102 20:45 and 20:46 UTC)
3. https://wordnetcode.princeton.edu/5papers.pdf : "Introduction to WordNet", revised 199308 (read 20261102 20:42 UTC)
4. http://www.jfsowa.com/pubs/semnet.htm : Sowa, "Semantic Networks", on Quillian, Woods, Brachman and KL-ONE (read 20261102 20:44 UTC)
5. https://api.semanticscholar.org/graph/v1/paper/DOI:10.1002/bs.3830120511?fields=citationCount, https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/362384.362685?fields=citationCount, https://api.semanticscholar.org/graph/v1/paper/DOI:10.1108/eb026526?fields=citationCount, https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/361219.361220?fields=citationCount, https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/s0364-0213(85)80014-8?fields=citationCount, https://api.semanticscholar.org/graph/v1/paper/DOI:10.1609/aimag.v6i4.510?fields=citationCount, https://api.semanticscholar.org/graph/v1/paper/DOI:10.1147/rd.14.0309?fields=citationCount, https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/321033.321035?fields=citationCount, https://api.semanticscholar.org/graph/v1/paper/DOI:10.1002/asi.4630270302?fields=citationCount, https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/0004-3702(82)90012-1?fields=citationCount : `citationCount` for Quillian (827), Codd (3,675), Sparck Jones (5,628), Salton, Wong and Yang (8,535), Brachman and Schmolze (2,146), Cyc (406) and, in Further reading, Luhn (1,199), Maron and Kuhns (1,036), Robertson and Sparck Jones (2,560) and Newell (3,073). Recorded on 20261102 at 19:55 UTC in the foundations candidate pool, a research pool of this documentation's preparation, kept in [`plans/evidence/`](../../plans/evidence/papers-pool-foundations-1950-1989.md) and its sibling files, through one batch request; the URLs are the equivalent single requests, not re-queried because the API rate-limits
6. https://arxiv.org/abs/2003.02320 : Hogan et al., "Knowledge Graphs": title, authors, first-version date, journal reference and abstract (read 20261102 20:42 UTC); v6 PDF, history appendix and references (read 20261102 20:45 UTC); Section 4.3.2 and Appendix B re-read 20261102 21:19 to 21:22 UTC
7. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, CACM 64(3), 2021 (read 20261102 20:45 UTC; the passage on Richens (1956) and Quillian (1963) re-read 20261102 21:19 to 21:22 UTC); shares an author with [6]
8. https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf : Codd 1970, text (read 20261102 20:41 UTC)
9. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE, 2012 (read 20261102 20:46 UTC; the passages on Luhn, idf and tf-idf and references 19, 21, 31 to 33 re-read 20261102 21:19 to 21:22 UTC)
10. https://dspace.mit.edu/handle/1721.1/6089 : Minsky memo record, date and abstract (read 20261102 20:41 UTC)
11. https://api.openalex.org/works/W2175268987, https://api.openalex.org/works/W4230553559, https://api.openalex.org/works/W2121773050 (Minsky republication records), https://api.openalex.org/works/W4246055080 (Woods report record), https://api.openalex.org/works/W2158270697 (Feigenbaum report record), https://api.openalex.org/works/W2127140110 (Brachman and Levesque), https://api.openalex.org/works/doi:10.1145/320434.320440 (Chen) : `cited_by_count`, recorded in the foundations candidate pool ([`plans/evidence/`](../../plans/evidence/papers-pool-foundations-1950-1989.md)) between 20261102 19:43 and 19:52 UTC; not re-queried
12. https://api.crossref.org/works/10.21236/ada022584, https://api.crossref.org/works/10.1145/320434.320440 : Crossref `is-referenced-by-count` for Woods (56) and, in Further reading, Chen (4,588), recorded in the foundations candidate pool on 20261102 at 19:46 UTC; not re-queried (the Woods value was seen again on 20261102 21:21 UTC, see [69])
13. https://www.ijcai.org/Proceedings/77-2/Papers/092.pdf : Feigenbaum 1977, text; https://www.ijcai.org/Proceedings/77-2/ : proceedings listing with pages 1014-1028 (read 20261102 20:42 UTC)
14. https://interlisp.org/history/bibliography/qxtftccf/ : bibliographic record and abstract of the Cyc paper (read 20261102 20:41 UTC)
15. https://api.crossref.org/works/10.1006/knac.1993.1008, https://api.crossref.org/works/10.1093/ijl/3.4.235, https://api.crossref.org/works/10.1145/219717.219748, https://api.crossref.org/works/10.1016/s0169-7552(98)00110-x, https://api.crossref.org/works/10.1038/scientificamerican0501-34, https://api.crossref.org/works/10.1007/978-3-540-76298-0_52, https://api.crossref.org/works/10.1145/1242572.1242667, https://api.crossref.org/works/10.1145/1376616.1376746, https://api.crossref.org/works/10.4018/jswis.2009081901, https://api.crossref.org/works/10.1609/aaai.v24i1.7519, https://api.crossref.org/works/10.1145/1322432.1322433 : `is-referenced-by-count` for Gruber (8,595), Miller et al. (2,249 for 1990, 9,187 for the 1995 overview), Brin and Page (9,354), Berners-Lee et al. (8,727), Auer et al. (2,448), Suchanek et al. (2,509), Bollacker et al. (3,284) and Bizer et al. (2,525) and, in Further reading, Carlson et al. (783) and Angles and Gutierrez (749). Crossref counts only citing works whose references it holds, so each is a lower bound. Recorded in the candidate pool for the web and ontologies period ([`plans/evidence/`](../../plans/evidence/papers-pool-web-and-ontologies-1990-2011.md)) on 20261102 at 19:59 and 20:00 UTC; not re-queried
16. https://tomgruber.org/writing/ontolingua-kaj-1993.pdf : Gruber 1993, text and publication note (read 20261102 20:43 UTC)
17. https://protege.stanford.edu/publications/ontology_development/ontology101.pdf : Noy and McGuinness, "Ontology Development 101", citing Gruber 1993 (read 20261102 20:46 UTC)
18. https://api.openalex.org/works?search=A+Translation+Approach+to+Portable+Ontology+Specifications : OpenAlex `cited_by_count` for Gruber (12,781), recorded in the web and ontologies candidate pool ([`plans/evidence/`](../../plans/evidence/papers-pool-web-and-ontologies-1990-2011.md)) between 20261102 19:44 and 19:58 UTC; not re-queried
19. https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/okapi_trec3.pdf and https://www.microsoft.com/en-us/research/publication/okapi-at-trec-3/ : Okapi at TREC-3 authors, venue, date, BM25 passage (read 20261102 20:46 UTC)
20. https://pages.nist.gov/trec-browser/trec3/proceedings/ : lists "Okapi at TREC-3" under the TREC-3 (1994) proceedings (read 20261102 20:47 UTC)
21. https://arxiv.org/abs/2004.04906 : Karpukhin et al. title, authors, v1 date, comment, abstract (read 20261102 20:42 UTC)
22. https://www.emerald.com/ftinr/article/4/1-2/1/1326508/The-Probabilistic-Relevance-Framework-BM25-and : Robertson and Zaragoza title, authors, journal, volume, pages, date (read 20261102 20:47 UTC; reached from https://doi.org/10.1561/1500000019)
23. https://arxiv.org/pdf/2004.04906 : DPR full text, keyword-searched (read 20261102 20:49 UTC)
24. https://arxiv.org/abs/2607.26497 : BM25 Wins at Scale, v1 20260729, v3 20260731, abstract (read 20261102 20:46 UTC; abstract re-read 20261102 21:21 UTC)
25. https://snap.stanford.edu/class/cs224w-readings/Brin98Anatomy.pdf : printed version of Brin and Page (read 20261102 20:44 UTC); the abstract also appears at https://research.google/pubs/the-anatomy-of-a-large-scale-hypertextual-web-search-engine/ (read 20261102 20:41 UTC)
26. https://arxiv.org/abs/2405.14831 : HippoRAG abstract, first version 20240523 (read 20261102 20:44 UTC)
27. https://www.scientificamerican.com/article/the-semantic-web/ : title, authors, date, issue, standfirst of Berners-Lee et al. (read 20261102 20:44 UTC)
28. https://arxiv.org/pdf/2003.02320v6 : Hogan et al. full text and reference list, keyword-searched (read 20261102 20:50 UTC; Section 4.3.2 and Appendix B re-read 20261102 21:19 to 21:22 UTC)
29. https://www.scientificamerican.com/article/the-semantic-web/ and a four-page copy of the article at https://www-sop.inria.fr/acacia/cours/essi2006/ : the article's scenario and section headings (read 20261102 20:01 to 20:04 UTC; carried over from the candidate pool for the web and ontologies period, kept in [`plans/evidence/`](../../plans/evidence/papers-pool-web-and-ontologies-1990-2011.md))
30. https://www.cis.upenn.edu/~zives/research/dbpedia.pdf : Auer et al. abstract, introduction, authors, figures (author copy; read 20261102 20:45 UTC); the Related Work section, the dataset table ("Yago Types") and reference 16 re-read 20261102 21:19 to 21:22 UTC
31. http://tomheath.com/papers/bizer-heath-berners-lee-ijswis-linked-data.pdf : abstract and introduction of the Linked Data preprint (read 20261102 20:03 UTC; carried over from the same pool; the host showed a certificate error at 20:45 UTC today)
32. https://suchanek.name/work/publications/www2007.pdf : Suchanek et al. abstract, venue line, authors (read 20261102 20:43 UTC)
33. https://research.google/pubs/knowledge-vault-a-web-scale-approach-to-probabilistic-knowledge-fusion/ : Knowledge Vault title, authors, venue, abstract (read 20261102 20:44 UTC)
34. https://research.google/pubs/freebase-a-collaboratively-created-graph-database-for-structuring-human-knowledge/ : Bollacker et al. title, authors, venue, abstract (read 20261102 20:43 UTC)
35. https://blog.google/products/search/introducing-knowledge-graph-things-not/ : Singhal, 20120516, "rooted in public sources such as Freebase" (read 20261102 20:51 UTC)
36. https://proceedings.neurips.cc/paper_files/paper/2013/file/1cecc7a77928ca8133fa24680a88d2f9-Paper.pdf : TransE full text, data sets WN and FB15k (read 20261102 20:49 UTC)
37. https://econpapers.repec.org/RePEc:igg:jswis0:v:5:y:2009:i:3:p:1-22 : Bizer et al. title, authors, journal, volume, issue, pages, DOI (read 20261102 20:46 UTC)
38. https://papers.nips.cc/paper_files/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html : TransE title, authors, venue, abstract (read 20261102 20:44 UTC)
39. https://api.openalex.org/works?search=Translating+Embeddings+for+Modeling+Multi-relational+Data (Bordes, record without DOI), https://api.openalex.org/works/doi:10.1145/2623330.2623623, https://api.openalex.org/works/doi:10.1145/2629489, https://api.openalex.org/works/doi:10.1145/3183713.3190657, https://api.openalex.org/works/doi:10.1109/TKDE.2017.2754499, https://api.openalex.org/works/doi:10.3115/v1/p15-1128, https://api.openalex.org/works?search=Knowledge+Graphs+Hogan+Blomqvist+Cochez (Hogan, CSUR record), https://api.openalex.org/works?search=Modeling+Relational+Data+with+Graph+Convolutional+Networks (Schlichtkrull), https://api.openalex.org/works?search=Towards+a+Definition+of+Knowledge+Graphs (Ehrlinger and Woess, record without DOI) : `cited_by_count` for Bordes et al. (5,724), Dong et al. (1,533), Vrandecic and Kroetzsch (3,366), Francis et al. (549), Hogan et al. (2,144) and, in Further reading, Wang et al. (2,642), Schlichtkrull et al. (5,677), Yih et al. (768) and Ehrlinger and Woess (497). Recorded in the candidate pool for the knowledge-graph period ([`plans/evidence/`](../../plans/evidence/papers-pool-kg-at-scale-2012-2019.md)) on 20261102 at 19:50 UTC; not re-queried. The search URLs return the records in a result list, from which the pool took the one named; the pool did not keep the record identifiers
40. https://api.crossref.org/works/10.1145/2623330.2623623, https://api.crossref.org/works/10.1145/2629489, https://api.crossref.org/works/10.1145/3183713.3190657, https://api.crossref.org/works/10.1109/TKDE.2017.2754499, https://api.crossref.org/works/10.3115/v1/p15-1128, https://api.crossref.org/works?query.bibliographic=Knowledge+Graphs+Hogan+Blomqvist+Cochez&rows=1 (Hogan), https://api.crossref.org/works?query.bibliographic=Language+Models+as+Knowledge+Bases+Petroni&rows=1 (Petroni), https://api.crossref.org/works?query.bibliographic=Modeling+Relational+Data+with+Graph+Convolutional+Networks+Schlichtkrull&rows=1 (Schlichtkrull) : `is-referenced-by-count` for Dong et al. (1,080), Vrandecic and Kroetzsch (2,731), Francis et al. (514), Petroni et al. (953), Hogan et al. (1,950) and, in Further reading, Wang et al. (2,192), Schlichtkrull et al. (3,740) and Yih et al. (363). Recorded in the candidate pool for the knowledge-graph period ([`plans/evidence/`](../../plans/evidence/papers-pool-kg-at-scale-2012-2019.md)) on 20261102 at 19:53 and 20:00 UTC; not re-queried. The query URLs are leads to the records, as the pool did not keep their DOIs
41. https://iccl.inf.tu-dresden.de/web/Article4002/en : Wikidata paper title, authors, journal, volume, issue, pages, year, abstract (read 20261102 20:48 UTC)
42. https://www.wikidata.org/wiki/Wikidata:Introduction : the project's description of itself (read 20261102 20:48 UTC)
43. https://arxiv.org/pdf/1909.01066 : LAMA full text, keyword-searched (read 20261102 20:51 UTC); the introduction (item iv), Section 4.1 to 4.3, Table 2 and Section 5 re-read 20261102 21:19 to 21:22 UTC
44. https://homepages.inf.ed.ac.uk/pguaglia/papers/sigmod18.pdf : Cypher title, authors, venue line, abstract (read 20261102 20:44 UTC)
45. https://arxiv.org/abs/1909.01066 : Petroni et al. title, authors, v1 date, comment, abstract (read 20261102 20:42 UTC)
46. https://aclanthology.org/D19-1250/ : LAMA venue and author order in the ACL Anthology (read 20261102 20:47 UTC)
47. https://arxiv.org/pdf/2002.08909 : REALM full text, keyword-searched (read 20261102 20:50 UTC)
48. https://proceedings.mlr.press/v119/guu20a.html : REALM venue, volume, pages (read 20261102 20:48 UTC)
49. https://arxiv.org/abs/2002.08909 : Guu et al. title, authors, v1 date, abstract (read 20261102 20:42 UTC; author list re-read 20261102 21:23 UTC)
50. https://api.semanticscholar.org/graph/v1/paper/arXiv:2005.11401?fields=citationCount, https://api.semanticscholar.org/graph/v1/paper/arXiv:2004.04906?fields=citationCount, https://api.semanticscholar.org/graph/v1/paper/arXiv:2002.08909?fields=citationCount, https://api.semanticscholar.org/graph/v1/paper/arXiv:2312.10997?fields=citationCount, https://api.semanticscholar.org/graph/v1/paper/arXiv:2112.04426?fields=citationCount : `citationCount` for Lewis et al. (20,475), Karpukhin et al. (7,702), Guu et al. (3,596), Gao et al. (4,421) and, in Further reading, Borgeaud et al. (2,015). Recorded on 20261102 at 20:20 UTC in the candidate pool for retrieval in the language-model period ([`plans/evidence/`](../../plans/evidence/papers-pool-llm-era-retrieval-2020-2026.md)); the URLs are the equivalent single requests, not re-queried
51. https://arxiv.org/pdf/2005.11401 : RAG full text, keyword-searched (read 20261102 20:49 UTC)
52. https://aclanthology.org/2020.emnlp-main.550/ : DPR venue, authors, month (read 20261102 20:48 UTC)
53. https://arxiv.org/abs/2005.11401 : Lewis et al. title, authors, v1 date, comment, abstract (read 20261102 20:42 UTC)
54. https://arxiv.org/abs/2404.16130 : GraphRAG abstract (read 20261102 20:52 UTC)
55. https://arxiv.org/abs/2310.11511 : Self-RAG abstract (read 20261102 20:52 UTC)
56. https://arxiv.org/abs/2312.10997 : Gao et al. title, authors, v1 date, comment, abstract (read 20261102 20:42 UTC)
57. https://arxiv.org/pdf/2312.10997 : Gao et al. full text, keyword-searched (read 20261102 20:50 UTC; the inception passage and references 3 to 5 and 102 re-read 20261102 21:19 to 21:22 UTC)
58. https://api.openalex.org/works/doi:10.1147/rd.14.0309, https://api.openalex.org/works/doi:10.1145/321033.321035, https://api.openalex.org/works/doi:10.1145/320434.320440, https://api.openalex.org/works/doi:10.1002/asi.4630270302, https://api.openalex.org/works/doi:10.1016/0004-3702(82)90012-1, https://api.openalex.org/works/W2127140110 (Brachman and Levesque) : abstract fields of the records for Luhn (1957), Maron and Kuhns (1960), Chen (1976), Robertson and Sparck Jones (1976), Newell (1982; the abstract of the technical-report record) and Brachman and Levesque (1984), carried over from the foundations candidate pool ([`plans/evidence/`](../../plans/evidence/papers-pool-foundations-1950-1989.md); read 20261102 19:48 to 19:52 UTC, not re-read)
59. https://www.ijcai.org/Proceedings/07/Papers/429.pdf : Banko et al., abstract; no DOI, so no citation count (read 20261102 20:03 UTC; carried over from the same pool, not re-read)
60. https://users.dcc.uchile.cl/~cgutierr/papers/surveyGDB.pdf : Angles and Gutierrez, abstract and introduction (read 20261102 20:01 UTC; carried over from the same pool, not re-read)
61. https://www.cs.cmu.edu/~acarlson/papers/carlson-aaai10.pdf : Carlson et al. (NELL) abstract and design principles (read 20261102 20:02 UTC; carried over from the candidate pool for the web and ontologies period, not re-read)
62. https://aclanthology.org/P15-1128.pdf : Yih et al., abstract and introduction (read 20261102 20:01 UTC; carried over from the candidate pool for the knowledge-graph period, not re-read)
63. https://ceur-ws.org/Vol-1695/paper4.pdf : Ehrlinger and Woess, full text of the four-page poster (read 20261102 19:54 UTC; carried over from the candidate pool for the knowledge-graph period, not re-read)
64. https://arxiv.org/abs/1703.06103 : Schlichtkrull et al. title, authors, v1 date 20170317, abstract (read 20261102 21:01 UTC)
65. https://api.openalex.org/works/doi:10.1109/TKDE.2017.2754499 : abstract of Wang et al. (2017) through `abstract_inverted_index` (read 20261102 19:54 UTC; carried over from the same pool, not re-read)
66. https://arxiv.org/abs/2112.04426 : Borgeaud et al. title, authors (28), v1 date 20211208, abstract (read 20261102 21:01 UTC)
67. https://par.nsf.gov/servlets/purl/10292869 : Hitzler, "A Review of the Semantic Web Field", CACM 64(2), 2021: the passages on the 2001 Scientific American article, "arguably marks the birth of the field" and "A Subjective Timeline" (read 20261102 21:20 UTC)
68. https://api.crossref.org/works/10.1561/1500000019 : Crossref record of Robertson and Zaragoza: title, authors, journal, volume, issue, pages, issue date 20090917, abstract, `is-referenced-by-count` 2,759 (read 20261102 21:21 UTC)
69. https://api.crossref.org/works/10.21236/ada022584 : Crossref record of the DTIC report of Woods: issue date 19751101, `is-referenced-by-count` 56 (read 20261102 21:21 UTC)
70. https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/510 : AAAI record of the Cyc paper, read as an Internet Archive capture (captured 20260216 13:10 UTC): "Published 1985-03-15", issue "Vol. 6 No. 4: Winter 1985", citation "6 (4), 65", abstract (read 20261102 23:13 UTC)
71. https://ojs.aaai.org/aimagazine/index.php/aimagazine/issue/view/57 : AAAI issue record of Vol. 6 No. 4: Winter 1985, "Published: 1985-12-15", read as an Internet Archive capture (captured 20240317 12:12 UTC) (read 20261102 23:14 UTC)
72. https://api.crossref.org/works/10.1145/219717.219745 : Crossref record of Lenat, "CYC", Communications of the ACM 38(11), pp. 33-38, 1995; abstract: "Since 1984, a person-century of effort has gone into building CYC" (read 20261102 23:14 UTC)
