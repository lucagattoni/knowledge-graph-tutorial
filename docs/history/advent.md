---
type: era
period: 1950-1969
order: 1
updated: 20261102 23:11 UTC
---

# The advent: machines that hold knowledge

This page answers: when did people first try to make a computer hold, search and use knowledge, and which of those first attempts are still part of the story? The next era is [Formal foundations](formal-foundations.md); the whole span is on the [chapter overview](README.md).

## Dates and boundaries

**The scheme is this documentation's.** No source read gives one periodisation for all four threads. The boundaries here are points that at least two sources share. Gutierrez and Sequeda name a first period, "Advent of the Digital Age", but print no span; the dates they cite run from 1956 to 1968, and their scope is "developments after the advent of computing in its modern sense (1950s)" [1].

**Start, 1950.** Three shared points sit between 1950 and 1956.

- March 1950: Sanderson and Croft say that the term "information retrieval" was first used around the time of Luhn's punch-card selector (prototypes 1950), and then quote Mooers's paper of March 1950, which uses it [2].
- 31 August 1955: the Dartmouth proposal for a study of "artificial intelligence" in summer 1956 [3]. The Stanford AI100 appendix says the field was "officially born and christened" at that 1956 workshop [4].
- 1956: Richens uses "semantic net", the earliest use of the term that Sowa reports [5]. Gutierrez and Sequeda date semantic networks to 1956 [1]. Hogan et al. also place the start of this line of work at Richens (1956), but cite a different Richens paper [6]; see dispute 1.

*Disagreement on the start.* Earlier events exist. Bush's essay of July 1945 described the "memex" [7]. At a 1948 Royal Society conference a "machine called the Univac" was described as searching text; Sanderson and Croft write that this "appears" to be the first reference to a computer searching content, and add that the UNIVAC is not generally thought to have existed until 1951 [2]. This page starts at 1950, the first date at which a source names the field's activity, and treats 1945 and 1948 as precursors. Dating by AI alone would start at 1955 or 1956 [3][4].

**End, 1969.** Codd's relational model appeared in *Communications of the ACM* in June 1970 [8]. It calls the relational view "superior in several respects to the graph or network model [3,4] presently in vogue" [8], so it marks a break in the data thread. Gutierrez and Sequeda start a new period, "The 1970s", on the wider adoption of computing in industry [1]. The knowledge thread turns in the same decade (frames, 1974 [6]). Shadbolt dates the early origins of AI systems to the mid 1950s and the appearance of expert systems "as a distinct line around the late 70's", and notes "considerable argument" about when the divergence took place [12].

## What changed

Machine searching, reasoning and data storage went from proposals to working programs: programs that proved theorems and answered questions about stored sentences [1][4], text indexed by words and ranked by a score [2], and shared files on disk [1]. Hogan et al. list representation "through diagrams (specifically graphs)" among the notions of this era "still of relevance today" [6]. The period also left problems for the 1970s: the graphs had no agreed meaning, and data systems tied programs to the physical layout of the data [6][8].

## The threads

### KB/KG

- **Automated reasoning.** Newell, Shaw and Simon's Logic Theorist (1956) was the first program to process complex information, say Gutierrez and Sequeda; the General Problem Solver followed in 1958 [1][4].
- **Semantic networks.** Sowa reports Richens (1956) as the first published use of the term, in a proposal for the "preprogramming" of machine translation [5]. Quillian's 1963 report proposed a notation for storing conceptual information in a computer, and his 1967 dissertation developed a memory model for language [1]. Sowa adds marker passing (1966) [5]. Hogan et al. trace the lineage of the [knowledge graph](../index/knowledge-graph.md) back to diagrammatic representation, and to this line of work once computers arrived [6]. A 1993 paper groups logic, rules, frames and semantic nets under the name "knowledge representation technologies" [13]. See [knowledge representation](../index/knowledge-representation.md) and [semantic network](../index/semantic-network.md).
- **Question answering.** Raphael's SIR (1964) held relations from English sentences in word associations and property lists [1].
- **Knowledge-based programs.** DENDRAL began at Stanford in 1965; Feigenbaum calls it "an early herald of AI's shift to the knowledge-based paradigm" [9]. Michie's 1968 "epistemological engineering" became "knowledge engineering" [9]. See [knowledge engineering](../index/knowledge-engineering.md) and [expert system](../index/expert-system.md).

### Databases and search

- **Searching text.** Mooers wrote in March 1950 of "machine searching and retrieval of information from storage according to a specification by subject" [2]. Taube's Uniterm (1952) indexed items by keyword; Cleverdon's tests found it as good as classification schemes [2]. See [information retrieval](../index/information-retrieval.md).
- **Ranked retrieval.** Luhn proposed scoring documents (1957), and Maron, Kuhns and Ray tested the idea (1959) and found it beat Boolean search on a 200-document collection [2]. Yet almost all commercial systems stayed Boolean until the early to mid-1990s; Dialog was formed in 1966 from a NASA system [2]. See [ranked retrieval](../index/ranked-retrieval.md).
- **SMART.** Salton's group built the vector-space idea, with Switzer (1963) and Rocchio's relevance feedback (1965) [2]. Stonebraker and Pavlo call the vector space model, which SMART pioneered, "now nearly universal in modern search engines" [10]. See [vector space model](../index/vector-space-model.md) and [relevance feedback](../index/relevance-feedback.md).
- **Data stores.** Bachman's IDS (1963) kept shared files on disk and became the basis for CODASYL [1]; hierarchical systems such as IMS belong to the late 1960s [10]. See [CODASYL](../index/codasyl.md).

### Threads with no event in this era

- **Ontologies and the semantic web.** The sources record no ontology language, schema standard or web data in these years. The link is retrospective: Sowa describes the Semantic Web of 2001 as "a large semantic network" [5]. See [ontology](../index/ontology.md) and [semantic web](../index/semantic-web.md).
- **RAG and agent memory.** No retrieval-augmented system existed. A 2026 survey says agent memory, a limited context window plus an external store, mirrors the Atkinson-Shiffrin model of 1968 [11]. Bush's memex has been read as "essentially a graph store" [7]. Both are later readings, not events. What is moving now is in the [trends chapter](../trends/README.md).

## Dated events

| Date | Event | Thread | Source |
|---|---|---|---|
| 195003 | Mooers's paper on "information retrieval"; the term is first used about now | Databases and search | [2] |
| 19550831 | Dartmouth proposal for a summer 1956 study of AI | KB/KG | [3][4] |
| 1956 | Richens: "semantic net"; Logic Theorist | KB/KG | [1][5] |
| 1957 to 1959 | Luhn proposes, Maron, Kuhns and Ray test ranked retrieval | Databases and search | [2] |
| 1958 | General Problem Solver | KB/KG | [1][4] |
| 1963 | Quillian's notation report; Bachman's IDS | KB/KG; Databases and search | [1] |
| 1964 | Raphael's SIR | KB/KG | [1] |
| 1965 | DENDRAL begins; Rocchio's relevance feedback | KB/KG; Databases and search | [9][2] |
| 1966 | Quillian's marker passing; Dialog formed | KB/KG; Databases and search | [5][2] |
| 1968 | "Knowledge engineering" coined in a remark; Atkinson-Shiffrin model | KB/KG; RAG and memory | [9][11] |

## Systems and projects

No project in the archive dates from this era; the systems above have no live page. DENDRAL was still running when Feigenbaum wrote in 1977 [9].

## Ideas and disputes

1. **Who started semantic networks.** Gutierrez and Sequeda say Richens introduced them in 1956 [1]; Hogan et al. list Richens (1956), Quillian (1963) and Travers and Milgram (1969) [6]; Sowa says Masterman's Cambridge group "designed the first systems to be called semantic networks" and names Ceccato's 1961 nets [5]. The references differ: Gutierrez and Sequeda cite "Preprogramming for mechanical translation" (vol. 3, no. 1) [1]; Hogan et al. spell the name "Ritchens" and cite "General program for mechanical translation between any two languages via an algebraic interlingua" (vol. 3, no. 2, November 1956) [6]. The primary text was not reached, so which paper contains "semantic net" is **unstated** here.
2. **Absorbed or replaced?** Hogan et al. say that diagram-based representation is among the notions "still of relevance today", and also that semantic networks and frames were direct predecessors of description logics, which aimed to give them a well-defined semantics [6]. *Reading:* the two statements fit together: the graph idea persisted, and the 1960s formalisms were given a semantics. The details belong to the next page.
3. **IDS (1963) versus the "1970s" network model.** Gutierrez and Sequeda date IDS to 1963 and link it to CODASYL [1]; Stonebraker and Pavlo date the network movement to the 1970s [10]. *Reading:* the dates may measure different things, the first system and the market movement; neither source says so.
4. **Dating ranked retrieval.** Sanderson and Croft's text puts Luhn and Maron et al. in the same year, their references in 1958 and 1959 [2]; this page gives the range.

## Papers and standards

See [Foundations](../papers/foundations.md). No standard of the settled kind (W3C, ISO) exists in this era.

- Dartmouth proposal (1955) [3]; Richens (1956) [1][5][6]; Quillian (1963, 1967) [1][6]; Raphael, SIR (1964) [1].
- Mooers (1950); Luhn (1957); Maron, Kuhns and Ray (1959); Rocchio (1965) [2].
- Feigenbaum (1977), a later account of DENDRAL and knowledge engineering [9].

## Left unsolved

- **No agreed meaning for the graphs.** Semantic networks had no formal semantics; the response (frames, formalised networks) is the 1970s story [6].
- **Poor computing resources** [1][6].
- **Programs tied to storage layout.** Codd's paper opens by asking that users be "protected from having to know how the data is organized" in the machine [8]; see [data independence](../index/data-independence.md).

Next: [Formal foundations](formal-foundations.md).

## Sources

1. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: the Advent period, its five threads, the realizations and limitations, the scope sentence, the 1970s period opening (read 20261102 19:55 UTC)
2. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE 2012: first use of the term "information retrieval", Mooers March 1950, Univac 1948 with its hedge and footnote, Uniterm, ranked retrieval, SMART, Dialog, Boolean until the 1990s, reference dates (read 20261102 19:55 UTC; the term-use, Mooers and Univac passages re-read 20261102 20:06 UTC)
3. http://jmc.stanford.edu/articles/dartmouth/dartmouth.pdf : Dartmouth proposal, dated August 31, 1955, for a study in the summer of 1956 (read 20261102 19:55 UTC; date re-read 20261102 20:08 UTC)
4. https://ai100.stanford.edu/2016-report/appendix-i-short-history-ai : AI100 appendix: "officially born and christened" 1956; Logic Theorist and General Problem Solver (read 20261102 19:55 UTC)
5. https://www.jfsowa.com/pubs/semnet.htm : Sowa, "Semantic Networks": Richens 1956, Masterman, Ceccato, Quillian 1966, Semantic Web as a large semantic network (read 20261102 19:56 UTC)
6. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", Appendix A and reference [442]: Ritchens 1956 with its title, Quillian 1963, limits, notions still relevant, predecessors of description logics (read 20261102 19:57 UTC; Richens reference and the two quotations re-read 20261102 20:07 UTC)
7. https://arxiv.org/pdf/2010.06467 : Lin, Nogueira and Yates, section 1.2: Bush's memex of July 1945 and footnote 19, "essentially a graph store" (read 20261102 19:56 UTC)
8. https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf : Codd, CACM 13(6), June 1970: abstract and the remark on the network model (read 20261102 19:56 UTC; both quotations re-read 20261102 20:08 UTC)
9. https://www.ijcai.org/Proceedings/77-2/Papers/092.pdf : Feigenbaum, IJCAI-77: DENDRAL begun 1965, "knowledge engineering" anecdote of 1968, "herald" (read 20261102 19:56 UTC)
10. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 2024: IMS and CODASYL dates, legacy status, SMART and the vector space model (read 20261102 19:56 UTC)
11. https://arxiv.org/pdf/2512.13564 : Hu et al., "Memory in the Age of AI Agents" (v2, 2026): the Atkinson-Shiffrin comparison, page 76 (read 20261102 19:57 UTC)
12. https://eprints.soton.ac.uk/252374/1/A_Natural_History_of_Expert_Systems_1989.pdf : Shadbolt 1989, "Expert systems: a natural history", section 2: early origins of AI systems in the mid '50's, expert systems "as a distinct line around the late 70's", "considerable argument" about when (read 20261102 20:08 UTC)
13. https://groups.csail.mit.edu/medg/ftp/psz/k-rep.html : Davis, Shrobe, Szolovits, "What is a Knowledge Representation?", AI Magazine 14(1), 1993 (author-hosted copy): logic, rules, frames and semantic nets called "knowledge representation technologies" (read 20261102 22:56 UTC)
