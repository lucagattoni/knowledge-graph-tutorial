---
type: era
period: 1980-1992
order: 3
updated: 20261102 23:11 UTC
---

# Knowledge systems: boom and bust

This page answers three questions. How did explicit knowledge move from labs into products? What did the field build, and what survived the bust? What did the other threads do meanwhile? The previous era is [formal foundations](formal-foundations.md); the next is [the Web](the-web.md).

## Dates and boundaries

The periodisation is this documentation's: no source gives one scheme for all four threads, and Gutierrez and Sequeda say their own periods have "blurry boundaries" [1].

**Start, 1980.** Gutierrez and Sequeda give a period called "The 1980s" [1]. Shadbolt dates the [expert-system](../index/expert-system.md) shell to EMYCIN (1979, 1984), XCON/R1 to 1980, and the national programmes to 1981 (ICOT) and 1982 (Alvey) [2]. He writes that expert systems "appeared as a distinct line around the late 70's" [2], where [formal foundations](formal-foundations.md) ends. [Description logics](../index/description-logic.md) begin in the same years, 1979 to 1985 (see disputes).

**End, 1992.** Sanderson and Croft say the number of web sites "was relatively small until 1993" and that web search engines "started to emerge in late 1993" [6]. Gutierrez and Sequeda start their Web period with the 1990s [1]; this page uses 1993 because [6] gives a dated reason. The last events here are the third SQL edition (November 1992) [16] and TREC, started in 1992 [12].

**The bust is disputed** (mid-1980s [3] or beginning of the 1990s [1]); both dates fall inside the era, so the boundaries do not depend on the answer.

## What changed

Before 1980, knowledge-based programs were research demonstrations. In the 1980s they became products: rule-based shells let a company build an expert system, governments funded knowledge-based computing, and a second line made [knowledge representation](../index/knowledge-representation.md) a formal subject whose computational cost could be measured. Then funding fell. What lasted were the parts: rules and inference moved into mainstream software [1], and the logic line carried on into the [OWL](../index/owl.md) standard [10]. Databases and search stayed on the relational model, now with an ISO SQL standard, and on Boolean queries [8][16][6].

## The threads

### KB/KG

The central object is the expert system: a [knowledge base](../index/knowledge-base.md) of [production rules](../index/production-rule.md) plus an [inference engine](../index/inference-engine.md). EMYCIN was MYCIN stripped of its domain knowledge, leaving a rule language with backward chaining, certainty handling and explanation [2]. "The age of the expert system shell had dawned" [2]. XCON/R1, which configured DEC VAX orders, is "considered one of the most successful in the history of expert systems" [2]. [Knowledge engineering](../index/knowledge-engineering.md) became the craft of filling these bases; Shadbolt notes a move "from a transfer view of acquisition to a model view" [2].

In parallel, description logics grew out of [frames](../index/frame.md) and [semantic networks](../index/semantic-network.md) [4]. Brachman and Levesque showed that more expressive power costs more computation, which produced a family of logics along that trade-off [1]. Systems: KL-ONE, LOOM, CLASSIC [1], and Krypton, which paired KL-ONE with a theorem prover [5].

The large bets were [Cyc](../index/cyc.md) (begun in 1984 by Lenat and Shepherd [17], at MCC per Cycorp [18]; its paper is of 1985 [13]; Gutierrez and Sequeda say it "came out of" the MCC consortium [1]) and the Fifth Generation project, which "sparked world wide activity" in the US, Germany and the UK [1]. The phrase "[knowledge graph](../index/knowledge-graph.md)" appears in other senses (see disputes).

### Ontologies and the semantic web

Little happens under these names; the era supplies the formal base: early logic systems "would become the underpinning to OWL" [1]. Filling knowledge bases later grew into [ontology](../index/ontology.md) engineering [1]; see [the Web era](the-web.md) and [the semantic web](semantic-web.md).

### Databases and search

*Databases.* Relational products grew fast [1]. Around them came [object-oriented databases](../index/object-oriented-database.md), early graph query languages, and deductive databases queried in [Datalog](../index/datalog.md) [1]. [SQL](../index/sql.md) became an ISO standard: ISO 9075 in June 1987, a second edition in April 1989 and a third in November 1992 [14][15][16]. ANSI's adoption date: **unstated** (no primary record read). Stonebraker and Pavlo list extended-relational (1980s) and object-oriented (late 1980s, early 1990s) movements [8]. In their 2005 review they concluded that the [relational model](../index/relational-model.md) with an extendable type system "has dominated all comers"; their 2024 paper argues that SQL "absorbed the best ideas" of the alternatives and that this has continued since 2005 [8].

*Search.* [Information retrieval](../index/information-retrieval.md) research had ranked retrieval ([tf-idf](../index/tf-idf.md) variants, probabilistic models), but almost all commercial systems used [Boolean retrieval](../index/boolean-retrieval.md) until the early to mid-1990s [6]. [Stemming](../index/stemming.md) helped: Porter's rules date from the late 1970s and were published in 1980 [6]. Supervised [learning to rank](../index/learning-to-rank.md) began in the late 1980s [7].

### RAG and agent memory

No source read dates an event in this thread for 1980-1992: **unstated**. The parts of [retrieval-augmented generation](../index/retrieval-augmented-generation.md) existed separately (ranked retrieval [6], rule-queried knowledge bases [2]). [Agent memory](../index/agent-memory.md) has no counterpart. It starts in [language models meet retrieval](language-models-meet-retrieval.md).

## Dated events

| Date | Event | Thread | Source |
|---|---|---|---|
| 1980 | XCON/R1 (McDermott) configures DEC VAX systems | KB/KG | [2] |
| 1981-1982 | Japan's ICOT Fifth Generation initiative; UK Alvey report, then a 350 million pound programme | KB/KG | [2] |
| 1984 | Brachman and Levesque, tractability of subsumption | KB/KG | [1] |
| 1984 | Lenat and Shepherd begin Cyc (Cycorp: founded at MCC) | KB/KG | [17][18] |
| 1985 | KL-ONE overview; the Cyc paper (AI Magazine 6(4), Winter 1985; the day is disputed, see disputes) | KB/KG | [4][13][19] |
| mid-1980s | Interest in AI drops, funding dries up (AI100 date) | KB/KG | [3] |
| 1986-1988 | "Knowledge graph" used by Rada, Bakker (1987), Stokman and de Vries | KB/KG | [4] |
| 198706 | ISO 9075:1987, SQL (first edition) | Databases and search | [14] |
| 198904 | ISO/IEC 9075:1989, SQL with integrity enhancement (second edition) | Databases and search | [15] |
| 1989 | Fuhr: ranking functions learned from data | Databases and search | [6][7] |
| beginning of the 1990s | Expert systems judged costly to update; Fifth Generation goals unmet (date from [1]) | KB/KG | [1] |
| 1992 | TREC started by NIST and the US Department of Defense | Databases and search | [12] |
| 199211 | ISO/IEC 9075:1992, SQL (third edition) | Databases and search | [16] |

## Systems and projects

| Item | What it was | Settled how | Source |
|---|---|---|---|
| Expert-system shells | Reusable rule engines (EMYCIN and others) | Absorbed into mainstream IT tools | [1][2] |
| XCON/R1 | Order configuration at DEC | Still in use in 1989; later status unstated | [2] |
| KL-ONE, LOOM, CLASSIC | Description-logic systems | Their logic line became a standard (OWL, OWL 2) | [1][10][11] |
| [Cyc](../index/cyc.md) | Large common-sense knowledge base | Begun 1984 [17][18]; paper of 1985 [13]; Hogan et al. write effort "since 1986" [4] (see disputes); later status is outside this page, see the index entry | [4][13][17][18] |
| Fifth Generation, Alvey, MCC, ECRC | National and industrial programmes | Ended; Fifth Generation goals unmet | [1] |
| Object-oriented databases | Objects and inheritance in databases | Replaced: relational with types prevailed | [1][8] |
| SQL | Query language of relational products | Survived; three ISO editions 1987-1992 | [14][15][16] |
| TREC | Annual retrieval evaluation | In practice; NIST says most commercial search engines use technology first developed there (first-party) | [12] |

## Ideas and disputes

**When was the bust, and was it a failure?** The AI100 appendix says the field was "forced to take cognizance" of its shortcomings "in the mid-1980s, since interest in AI began to drop, and funding dried up" [3]. Gutierrez and Sequeda write that "at the beginning of the 1990s, expert systems proved expensive and difficult to update", that the Fifth Generation goals "had not been met", and that the experience was "rolled" into mainstream IT tools [1]. Shadbolt in 1989 still describes growth, yet reports funding "so tight" and an Alvey infrastructure "gradually coming apart" [2]. *Reading:* the sources may describe different events, AI as a field [3] against expert systems [1]. Market numbers: **unstated**.

**First use of "knowledge graph".** Hogan and others write "since at least 1972" in the introduction and "Schneider (1973)" in the appendix [4]; they add Rada (1986), Bakker (1987) and Stokman and de Vries (1988) [4]. Gutierrez and Sequeda call Bakker's thesis "the first systematic study with the term" [1].

**Description logics: 1979, 1984 or 1985?** Sowa has KL-ONE implemented in 1979 [5]; Gutierrez and Sequeda start the family with the 1984 tractability paper [1]; Hogan and others say it "stem[s] from" the 1985 KL-ONE paper [4]. These are three events: a system, a result, an overview.

**When did Cyc start, and when was its paper published?** Lenat writes "Since 1984, a person-century of effort has gone into building CYC" and that he and Mary Shepherd "embarked on that task in 1984" [17]; Cycorp's history page says Lenat founded the project at MCC in 1984 (first-party) [18]. Hogan et al. write effort "since 1986" [4] and give no reason in the passage read: **unstated**. *Reading:* two first-hand accounts agree on 1984, so this page uses 1984; the survey's 1986 may count something else. The paper's day is also disputed. *AI Magazine* 6(4) is the Winter 1985 issue, which the publisher's issue record dates 1985-12-15 [19]. The publisher's article record for the Cyc paper says 1985-03-15 [13], while four other articles of that issue carry 1985-12-15 [22]; the Interlisp bibliography copies 1985-03-15 [20]; OpenAlex gives 1986-01-01 [21]. *Reading:* a March date does not fit a winter issue, so this page gives only the year, 1985; the true day is **unstated** in the records read.

**Graph databases.** Angles and Gutierrez see a rise in the 1980s, a decline, and renewed relevance [9]; the recent part is in [chapter 2](../trends/README.md).

## Papers and standards

Standards of the era: ISO 9075 (SQL) in 1987, 1989 and 1992 [14][15][16]. The logic line became the W3C OWL standard later, in 2004, and OWL 2 followed in 2009 and 2012 [10][11]. Papers, with more in [foundations](../papers/foundations.md):

- McDermott, "R1: an expert in the computer systems domain", 1980 [2].
- Brachman and Levesque, "The Tractability of Subsumption in Frame-Based Description Languages", 1984 [1].
- Brachman and Schmolze, "An Overview of the KL-ONE Knowledge Representation System", 1985 [4].
- Lenat, Prakash and Shepherd, "CYC: Using Common Sense Knowledge to Overcome Brittleness and Knowledge Acquisition Bottlenecks", 1985 [13].
- Fuhr, "Optimum polynomial retrieval functions based on the probability ranking principle", 1989 [6].

## Left unsolved

- **The [knowledge acquisition bottleneck](../index/knowledge-acquisition-bottleneck.md):** knowledge was written by hand [1][13].
- **Scale and uncertainty:** "reasoning at large scale was an insurmountable problem" on the hardware of the time [1]; AI100 blames "an overemphasis on Boolean (True/False) logic" [3].
- **Exact match in search:** ranking depended on words shared by query and document [7].
- **Sharing:** the Web showed knowledge should be reused [1].

These lead into [the Web](the-web.md).

## Sources

1. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: period "The 1980s", description logics, expert systems, Fifth Generation, AI Winter, Bakker, limitations (read 20261102 19:54 UTC)
2. https://eprints.soton.ac.uk/252374/1/A_Natural_History_of_Expert_Systems_1989.pdf : Shadbolt, "Expert systems - a natural history", 1989: EMYCIN, shells, XCON/R1, ICOT 1981, Alvey 1982, funding, model view; every quoted phrase re-read in the full text through a browser (read 20261102 20:12 UTC)
3. https://ai100.stanford.edu/2016-report/appendix-i-short-history-ai : Stanford AI100 2016, Appendix I: mid-1980s drop in interest and funding, "AI winter" (read 20261102 19:54 UTC)
4. https://arxiv.org/pdf/2003.02320v6 : Hogan and others, "Knowledge Graphs", arXiv 2003.02320 v6, Appendix A and references: KL-ONE 1985, Cyc "since 1986", Schneider, Rada, Bakker, Stokman and de Vries (read 20261102 19:54 UTC)
5. https://www.jfsowa.com/pubs/semnet.htm : Sowa, "Semantic Networks": KL-ONE 1979, Krypton 1983, Pearl 1988 (read 20261102 19:54 UTC)
6. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", 2012: Boolean systems until the early to mid-1990s, Porter stemmer, Fuhr, Web from 1993 (read 20261102 19:54 UTC)
7. https://arxiv.org/pdf/2010.06467 : Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking", section 1.2: learning to rank from the late 1980s, exact match (read 20261102 19:54 UTC)
8. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, 2024: data-model movements by decade, 2005 conclusion on relational dominance, SQL absorbing alternatives, continuing since 2005 (read 20261102 19:54 UTC)
9. https://users.dcc.uchile.cl/~cgutierr/papers/surveyGDB.pdf : Angles and Gutierrez, "Survey of Graph Database Models", 2008, abstract (read 20261102 19:54 UTC)
10. https://www.w3.org/TR/2004/REC-owl-features-20040210/ : OWL Overview, W3C Recommendation 20040210: OWL DL and description logics (read 20261102 19:54 UTC)
11. https://www.w3.org/TR/owl2-overview/ : OWL 2 Document Overview, W3C Recommendation 20121211, refers to the Recommendation of 20091027 (read 20261102 19:57 UTC)
12. https://trec.nist.gov/overview.html : NIST, TREC overview: started in 1992 (read 20261102 19:57 UTC)
13. https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/510 : Lenat, Prakash, Shepherd, AI Magazine 6(4), 1985, title, abstract; the article record says "Published 1985-03-15" and "Vol. 6 No. 4: Winter 1985" (read 20261102 20:11 UTC; read again 20261102 22:55 UTC as the Internet Archive copy captured 20260216 13:10 UTC, because the publisher's site now answers with a proof-of-work bot check, which was not bypassed)
14. https://www.iso.org/standard/16661.html : ISO catalogue, ISO 9075:1987 "Information processing systems — Database language — SQL", edition 1, published 1987-06, withdrawn, revised by the 1989 edition (read 20261102 20:10 UTC)
15. https://www.iso.org/standard/16662.html : ISO catalogue, ISO/IEC 9075:1989 "Database Language SQL with integrity enhancement", edition 2, published 1989-04, withdrawn (read 20261102 20:10 UTC)
16. https://www.iso.org/standard/16663.html : ISO catalogue, ISO/IEC 9075:1992 "Database languages — SQL", edition 3, published 1992-11, withdrawn (read 20261102 20:10 UTC)
17. https://papers.baulab.info/papers/knowledge/Lenat-1995.pdf : Lenat, "CYC: A Large-Scale Investment in Knowledge Infrastructure", CACM 38(11), 1995: "Since 1984, a person-century of effort has gone into building CYC"; "Mary Shepherd and I embarked on that task in 1984" (read 20261102 22:56 UTC, text extracted from the PDF)
18. https://cyc.com/?p=8999 : "About Cycorp" (first-party): Lenat "founded the Cyc Project in 1984" at MCC; the project spun out of MCC at the end of 1994 as Cycorp, Inc. (read 20261102 22:56 UTC, WebFetch extraction)
19. https://web.archive.org/web/20240317121246/https://ojs.aaai.org/aimagazine/index.php/aimagazine/issue/view/57 : AAAI record of the issue "Vol. 6 No. 4: Winter 1985", "Published: 1985-12-15", listing the Cyc paper at page 65 (Internet Archive copy captured 20240317 12:12 UTC; read 20261102 22:55 UTC)
20. https://interlisp.org/history/bibliography/qxtftccf/ : Medley Interlisp bibliography record of the Cyc paper: date 1985-03-15, volume 6, issue 4, pages "65-65" (read 20261102 22:55 UTC)
21. https://api.openalex.org/works/doi:10.1609/aimag.v6i4.510 : OpenAlex record of the Cyc paper: publication date 1986-01-01, pages 65-85 (read 20261102 22:55 UTC)
22. https://web.archive.org/web/20250915154751/https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/508 and the pages of articles 509, 511 and 513 of the same site (Internet Archive copies captured 20250915, 20250527, 20250319 and 20230529) : the records of four other articles of the issue (Stefik and Bobrow, Colby, Woods, Miller's book review) each say 1985/12/15, volume 6, issue 4 (read 20261102 22:55 UTC)
