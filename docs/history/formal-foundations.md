---
type: era
period: 1970-1979
order: 2
updated: 20261102 23:11 UTC
---

# Formal foundations

This page answers: how did the 1970s give data and knowledge a formal footing, and which of those ideas are still in use? It covers the [relational model](../index/relational-model.md), the first formal answers to the weakness of [semantic networks](../index/semantic-network.md), the first [expert systems](../index/expert-system.md) and the formulas behind ranked search. The previous era is [The advent](advent.md); the next is [Knowledge systems: boom and bust](knowledge-systems.md); the whole span is on the [chapter overview](README.md).

## Dates and boundaries

**The scheme is this documentation's.** No source read gives one periodisation for all four threads. The boundaries are points that at least two sources share, and Gutierrez and Sequeda call their own boundaries "blurry" [1].

**Start, 1970.** Four sources meet here. Two of them, Gutierrez and Sequeda [1] and Hogan et al. [2], share an author [16], so they count as one voice; three independent voices agree.

- Codd's relational model appeared in *Communications of the ACM*, June 1970 [3]. Stonebraker and Pavlo date the relational movement to "the 1970s and early 1980s" [5].
- Gutierrez and Sequeda open their period "Data and Knowledge Foundations" with the 1970s [1].
- Hogan et al. list [frames](../index/frame.md) (1974), the formalisation of semantic networks (Woods 1975, Brachman 1977) and [conceptual graphs](../index/conceptual-graph.md) among the "influential developments" of the 70s [2].
- Sanderson and Croft put inverse document frequency, the [vector space model](../index/vector-space-model.md) and the [probability ranking principle](../index/probability-ranking-principle.md) in their section "1970s" [4].

**End, 1979.** Two shared points sit at the turn of the decade.

- Shadbolt writes that expert systems "appeared as a distinct line around the late 70's", and cites EMYCIN, [MYCIN](../index/mycin.md) stripped of its domain knowledge, as 1979 [7].
- [Description logics](../index/description-logic.md) start from [KL-ONE](../index/kl-one.md): Sowa dates its implementation to 1979, Gutierrez and Sequeda cite the tractability paper of Brachman and Levesque as 1984, Hogan et al. the KL-ONE overview as 1985 [8][1][2].

*Disagreement on the end.* The era ends at 1979 because shells and KL-ONE share that year and Gutierrez and Sequeda's next period is "The 1980s" [1]. A reader who dates description logics by their first theory would end it later.

## What changed

Before 1970 a program that stored data was tied to the layout of that data, and a graph of concepts had no agreed meaning. In the 1970s both got a formal answer. Codd gave data a mathematical model, the relation, so programs would not depend on storage [3]; systems and a query language followed within the decade [1]. Critics showed that semantic networks lacked a logical foundation, and the response was structure (frames) and logic [1][2]. The first rule-based systems showed that domain knowledge could carry a program to expert performance [6]. In search, three formulas turned word counts into ranked results [4].

## The threads

### KB/KG

- **[Frames](../index/frame.md).** Minsky's memo of 1 June 1974 proposes that in a new situation a person retrieves a remembered structure, a frame, and adjusts its details [9]. The memo is titled "A Framework for Representing Knowledge" [9], and a 1993 paper counts frames among the "knowledge representation technologies" [18]; see [knowledge representation](../index/knowledge-representation.md).
- **[Semantic networks](../index/semantic-network.md) under critique.** Woods's 1975 paper "What's in a Link" criticised their weak logical foundation, and researchers set out to give them formal semantics [1]. Sowa wrote that such networks "have no well-defined semantics" (quoted by Hogan et al.) [2]. Hayes (1977) recognised that frame networks could be formalised in first-order logic [1].
- **[Conceptual graphs](../index/conceptual-graph.md).** Sowa's 1976 paper uses them as an intermediate language between natural-language queries and a relational database [1].
- **[Expert systems](../index/expert-system.md) and [knowledge engineering](../index/knowledge-engineering.md).** [DENDRAL](../index/dendral.md) began in 1965; Feigenbaum calls it "an early herald of AI's shift to the knowledge-based paradigm" [6]. [MYCIN](../index/mycin.md) came from Shortliffe's doctoral work [6] and encodes domain knowledge as if-then [production rules](../index/production-rule.md) to select antibiotic therapy [1]. Hogan et al. say "[knowledge base](../index/knowledge-base.md)" was popularised in the 70s in the context of rule-based expert systems [2].
- **[Logic programming](../index/logic-programming.md) and data.** Kowalski (1974) used logic as a declarative and procedural representation of knowledge [1]. The 1977 Toulouse workshop "Logic and Data Bases" presented the [closed-world assumption](../index/closed-world-assumption.md) and negation as failure; Gutierrez and Sequeda call it "the birth of the logical approach to data" [1].

### Ontologies and the semantic web

No ontology language or web data exists yet; the thread is a lineage. Hogan et al. call conceptual graphs, semantic networks and frames "direct predecessors of Description Logics", which "formed the underpinnings" of [OWL](../index/owl.md) [2]. See [description logic](../index/description-logic.md), [KL-ONE](../index/kl-one.md) and [ontology](../index/ontology.md).

### Databases and search

- **The [relational model](../index/relational-model.md).** Codd calls the relational view "superior in several respects to the graph or network model" then in vogue, and asks that users be protected from knowing how data is organised in the machine [3]. See [data independence](../index/data-independence.md).
- **Systems and languages.** IBM's [System R](../index/system-r.md) and Berkeley's [INGRES](../index/ingres.md) "were the first to implement the 'vision' of the relational model", with the query languages SEQUEL and QUEL, which led to [SQL](../index/sql.md) [1][14]. Chen's [entity-relationship model](../index/entity-relationship-model.md) (March 1976) linked a conceptual design to the relational model [1][10].
- **Ranked search.** Spärck Jones's 1972 paper introduced inverse document frequency: less common words refer to more specific concepts and weigh more [4][12]. Salton, Wong and Yang's [vector space model](../index/vector-space-model.md) appeared in November 1975 [11], and Robertson's [probability ranking principle](../index/probability-ranking-principle.md), on how to rank documents optimally, in 1977 [4][13]. The combined weight is [tf-idf](../index/tf-idf.md).

**RAG and agent memory** have no event in this era: none of the sources read for this page names a retrieval-augmented system from it [1][2][4][5][6][7]. A 2026 survey of agent memory cites two 1972 works: TF-IDF, as a representative lexical retrieval method, and Tulving's classification of memory into episodic, semantic and procedural, which it says agent memory resembles [15]. These are later readings, not events. What is moving now is in the [trends chapter](../trends/README.md).

## Dated events

| Date | Event | Thread | Source |
|---|---|---|---|
| 197006 | Codd: relational model | Databases and search | [3] |
| 1972 | Spärck Jones: inverse document frequency | Databases and search | [12][4] |
| 19740601 | Minsky: frames | KB/KG | [9] |
| 1975 | Woods: "What's in a Link" | KB/KG | [1] |
| 197511 | Salton, Wong, Yang: vector space model | Databases and search | [11] |
| 197603 | Chen: entity-relationship model | Databases and search | [10] |
| 197606 | System R published; INGRES in 1976 | Databases and search | [14][1] |
| 1976 | Sowa: conceptual graphs (see disputes) | KB/KG | [1][8] |
| 1976 | Shortliffe: MYCIN | KB/KG | [6][7] |
| 1977 | Robertson: probability ranking principle | Databases and search | [13][4] |
| 1977 | Hayes; Brachman's dissertation; Toulouse workshop | KB/KG | [1][2] |
| 1979 | KL-ONE implemented (per Sowa); EMYCIN | KB/KG | [8][7] |

## Systems and projects

None of the project pages in the archive's list describes a system from this era [17]; these systems are historical.

- **System R and INGRES:** the first systems to implement Codd's vision of the relational model, with the query languages SEQUEL and QUEL [1]. **MYCIN and DENDRAL:** rule-based expert systems; many regard MYCIN as the first [7].
- **SMART:** Salton's retrieval system, begun in the 1960s. Stonebraker and Pavlo say it pioneered the vector space model, "now nearly universal in modern search engines" [5]; the model's 1975 paper dates from this era [11].

## Ideas and disputes

1. **First use of "[knowledge graph](../index/knowledge-graph.md)".** Hogan et al. write "since at least 1972" in the introduction and name Schneider (1973) in the appendix [2]. One reference entry carries both dates: 1973, and a Chicago event of April 1972 [2]. Schneider's graph links course units by dependencies [2]. Gutierrez and Sequeda instead name Bakker's thesis of the late 1980s as "the first systematic study with the term" [1]. The answer depends on whether any use of the words counts.
2. **Conceptual graphs, 1976 or 1979.** Gutierrez and Sequeda and Sowa say 1976 [1][8]; Hogan et al. say 1979 [2]. They cite different papers: "Conceptual Graphs for a Data Base Interface" (1976) [1] and "Semantics of Conceptual Graphs" (ACL meeting, 1979) [2]. *Reading:* each date is right for its paper.
3. **KL-ONE, 1979, 1984 or 1985.** See the end boundary [8][1][2].
4. **The first expert system.** Shadbolt: many name MYCIN, others DENDRAL or MACSYMA (1971), and "there is considerable argument" about when and where the divergence took place [7].
5. **Replaced or absorbed.** *Reading:* semantic networks were replaced by formal successors [1][2]. The relational model was absorbed into practice: it "has dominated all comers" and SQL "absorbed the best ideas" of rivals [5]. The vector space model is both: Salton's formulas are "rarely used" but the vector view is "still common" [4], and Stonebraker and Pavlo call it "nearly universal" in search engines [5].

## Papers and standards

See [Foundations](../papers/foundations.md). None of the sources read names a W3C or ISO standard from this era [1][2][4][5].

- Codd, "A Relational Model of Data for Large Shared Data Banks" (1970) [3].
- Spärck Jones, "A statistical interpretation of term specificity" (1972) [12].
- Minsky, "A Framework for Representing Knowledge" (1974) [9].
- Woods, "What's in a Link" (1975) [1]; Salton, Wong and Yang, vector space model (1975) [11].
- Chen, entity-relationship model (1976) [10]; Astrahan et al., "System R" (1976) [14].
- Robertson, "The probability ranking principle in IR" (1977) [13]; Feigenbaum, "The Art of Artificial Intelligence" (1977) [6].

## Left unsolved

- **Graphs at scale.** Papers using the phrase "knowledge graph" from 1970 to 2000 "tend to have worked with small graphs" [2].
- **Where knowledge comes from.** Gutierrez and Sequeda name the problem of obtaining the data and knowledge, knowledge acquisition [1].
- **Rigid structures, weak common-sense logic.** They list these as limits, leading to object-oriented and graph structures on the data side and to description logics on the knowledge side [1].

Next: [Knowledge systems: boom and bust (1980-1992)](knowledge-systems.md).

## Sources

1. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: the "Data and Knowledge Foundations" period, Woods, Minsky, Sowa 1976, Hayes, Kowalski, Toulouse 1977, System R and INGRES, Chen, MYCIN, Bakker, limits, "blurry" (read 20261102 19:57 UTC; the System R and INGRES wording re-read in a fresh download at 20261102 20:10 UTC)
2. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", Appendix A and the reference list: 1970s developments, Schneider entry, description logics as predecessors of OWL, "knowledge base" in the 70s (read 20261102 19:57 UTC)
3. https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf : Codd, CACM 13(6), June 1970: abstract and sections 1.1-1.2 (read 20261102 19:57 UTC)
4. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE 2012: section "1970s" and reference list (read 20261102 19:57 UTC)
5. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 2024: the movement dates, "dominated all comers", SMART and the vector space model (read 20261102 19:57 UTC; the SMART passage, section 2.5, re-read in a fresh download at 20261102 20:10 UTC)
6. https://www.ijcai.org/Proceedings/77-2/Papers/092.pdf : Feigenbaum, IJCAI-77: DENDRAL begun 1965, "herald", MYCIN note (read 20261102 19:57 UTC)
7. https://eprints.soton.ac.uk/252374/1/A_Natural_History_of_Expert_Systems_1989.pdf : Shadbolt 1989: "distinct line around the late 70's", MYCIN, DENDRAL, MACSYMA, EMYCIN, Lighthill report 1973 (read 20261102 20:10 UTC from a fresh download of this file, HTTP 200; a fetch at 19:57 UTC had returned HTTP 403, so an earlier copy was used until now). A second copy, https://web.archive.org/web/2023/https://eprints.soton.ac.uk/252374/1/A_Natural_History_of_Expert_Systems_1989.pdf, downloaded at 20:09 UTC, is byte-identical to the first and reads the same
8. https://www.jfsowa.com/pubs/semnet.htm : Sowa, "Semantic Networks": Shapiro 1971, Sowa 1976, Brachman 1979 (read 20261102 19:57 UTC; a fetch-tool extraction, not raw text)
9. https://dspace.mit.edu/handle/1721.1/6089 : Minsky, AI Memo 306 record: date issued 1 June 1974, abstract (read 20261102 19:58 UTC)
10. https://api.crossref.org/works/10.1145/320434.320440 : Chen, ACM Transactions on Database Systems, March 1976 (read 20261102 19:58 UTC)
11. https://api.crossref.org/works/10.1145/361219.361220 : Salton, Wong, Yang, CACM, November 1975 (read 20261102 19:58 UTC)
12. https://api.crossref.org/works/10.1108/eb026526 : Spärck Jones, Journal of Documentation, January 1972 (read 20261102 19:58 UTC)
13. https://api.crossref.org/works/10.1108/eb026647 : Robertson, Journal of Documentation, April 1977 (read 20261102 19:59 UTC)
14. https://api.crossref.org/works/10.1145/320455.320457 : Astrahan et al., "System R", ACM Transactions on Database Systems, June 1976 (read 20261102 19:59 UTC)
15. https://arxiv.org/pdf/2512.13564 : Hu et al., "Memory in the Age of AI Agents" (v2, 13 Jan 2026): TF-IDF (Spärck Jones 1972) in lexical retrieval; Tulving 1972 for episodic and semantic memory (read 20261102 20:00 UTC)
16. https://arxiv.org/abs/2003.02320 : author list of Hogan et al., which includes Claudio Gutierrez and Juan Sequeda, the authors of the paper in item 1 (read 20261102 20:10 UTC)
17. kb-kg/projects/ (repository folder, archive) : the 77 project pages of the archive's list, none of them a system from the 1970s (read 20261102 20:10 UTC)
18. https://groups.csail.mit.edu/medg/ftp/psz/k-rep.html : Davis, Shrobe, Szolovits, "What is a Knowledge Representation?", AI Magazine 14(1), 1993 (author-hosted copy): logic, rules, frames and semantic nets called "knowledge representation technologies" (read 20261102 22:56 UTC)
