---
type: index
kind: concept
aliases: []
updated: 20261102 21:25 UTC
---

# Datalog

Datalog is a rule language for databases in which a rule may use the relation it defines, so a query can follow paths of any length through stored facts. It was the query language of deductive databases, and the rules used to reason over graphs correspond to it.

## Definition

A textbook chapter introduces datalog by adding recursion to conjunctive queries [1]. Two rules show the form: `T(x,y) <- G(x,y)` and `T(x,y) <- G(x,z), T(z,y)` compute the transitive closure of a graph stored in the relation G [1]. A program is read as a mapping from the relations that appear only in rule bodies to the relations defined in rule heads [1]. Hogan et al. say rules of this shape correspond to positive Datalog in databases and to Horn clauses in logic programming [3].

## How it changed

- **1977.** The Toulouse workshop "Logic and Data Bases" presented the [closed-world assumption](./closed-world-assumption.md); Gutierrez and Sequeda call it "the birth of the logical approach to data" [2]. Era: [Formal foundations](../history/formal-foundations.md).
- **1980s.** Logic programming was layered on [relational](./relational-model.md) databases; this gave deductive databases, and Datalog "became the query language" for them [2]. A lesson drawn: logic and data must be tightly coupled, not layered [2]. Era: [Knowledge systems](../history/knowledge-systems.md).
- **1986.** Tsur and Zaniolo present the LDL system at the 12th VLDB conference (pages 33 to 41); Gutierrez and Sequeda call it "one of the first deductive databases systems" [2].
- **Year unstated.** The name was coined, "to our knowledge", by David Maier [1].
- **19890301.** Ceri, Gottlob and Tanca publish their survey in IEEE Transactions on Knowledge and Data Engineering 1(1) [4][3].
- **2018.** The Vadalog system, "Datalog-based reasoning for knowledge graphs", appears in PVLDB 11(9) [3]. A history chapter by Maier, Tekle, Kifer and Warren is dated 20180901 [5].
- **202003.** The knowledge-graph survey of Hogan et al. (March 2020 by its arXiv number; v6 read) names Datalog± (existentials) and disjunctive Datalog as rule languages that go beyond plain rules [3].

## Where sources disagree

No disagreement found in the sources read. They differ in emphasis: the textbook places datalog among many earlier languages [1], Gutierrez and Sequeda call it "a subset of Prolog" [2].

## Related

[Logic programming](./logic-programming.md), [closed-world assumption](./closed-world-assumption.md), [relational model](./relational-model.md), [SQL](./sql.md), [expert system](./expert-system.md), [OWL](./owl.md), [knowledge graph](./knowledge-graph.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Knowledge systems: boom and bust](../history/knowledge-systems.md)

**Trends**

- [Semantic web standards: from RDF 1.1 and RDF-star to RDF 1.2](../trends/semantic-web-standards.md)

**Index**

- [Closed-world assumption](closed-world-assumption.md)
- [Inference engine](inference-engine.md)
- [Logic programming](logic-programming.md)
- [OWL](owl.md)
- [Production rule](production-rule.md)
- [Relational model](relational-model.md)

<!-- END GENERATED: appears-in -->

## Sources

1. http://webdam.inria.fr/Alice/pdfs/Chapter-12.pdf : chapter 12 "Datalog" of the online edition of the textbook "Foundations of Databases" (authors and year unstated in the pages read): part introduction, rule example, bibliographic notes on the name (read 20261102 20:48 UTC; reread 20261102 21:21 UTC)
2. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: Toulouse 1977, deductive databases, LDL, lessons of the period, reference 37 (Tsur and Zaniolo, 1986) (read 20261102 20:48 UTC; reread 20261102 21:20 UTC)
3. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", arXiv 2003.02320 v6: rules section and reference list (Ceri et al. 1989; Bellomarini et al. 2018) (read 20261102 20:47 UTC; reread 20261102 21:21 UTC)
4. https://api.openalex.org/works/doi:10.1109/69.43410 : record of "What you always wanted to know about Datalog (and never dared to ask)", publication date 1989-03-01; text not read (read 20261102 20:47 UTC)
5. https://doi.org/10.1145/3191315.3191317 : Crossref record (api.crossref.org/works) of Maier, Tekle, Kifer, Warren, "Datalog: concepts, history, and outlook", 2018-09-01; text not read (read 20261102 20:46 UTC)
