---
type: index
kind: concept
aliases: [production rules, production system rule, condition-action rule]
updated: 20261102 21:24 UTC
---

# Production rule

A production rule is an if-then rule: when its condition matches the stored facts, its action is carried out. Rule-based expert systems used such rules to hold domain knowledge [1][4]. This entry gives the definition, the dated changes, and a dispute over whether expert-system rules are production rules.

## Definition

Davis and King describe a production system as a set of rules, a data base and an interpreter. In the simplest design a rule has a left-hand side and a right-hand side; the interpreter finds a rule whose left side matches the data base and replaces the matched symbols with the right side. A rule can also be read as a simple conditional statement [1]. The W3C says production rules "have an if part, or condition, and a then part, or action"; an action may assert, modify or retract facts, unlike a logic rule's conclusion [2].

## How it changed

- **1943.** Davis and King date the first proposal of production systems to Post [1]. His paper appears in the American Journal of Mathematics, April 1943 [3].
- **1972.** Newell and Simon use production rules to model human cognition [1][4].
- **1977.** Feigenbaum's IJCAI-77 paper represents expert knowledge as situation-to-action rules, each a chunk of knowledge meaningful to a domain specialist [4]. Davis and King publish their overview in Machine Intelligence 8 [1]. See [formal foundations](../history/formal-foundations.md).
- **198209.** Forgy publishes the Rete algorithm for matching many patterns against many objects [5].
- **1984.** The MYCIN book collects the experiments. The authors chose rules over a semantic network because experts could examine small chunks of knowledge [6]. See [knowledge systems](../history/knowledge-systems.md).
- **20130205.** W3C publishes the second edition of the RIF Production Rule Dialect, an XML format for exchanging production rules [2]. See [knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).

## Where sources disagree

Davis and King group MYCIN and DENDRAL with Newell and Simon's psychological models as two kinds of production system [1]. Feigenbaum writes that his group's rules "bear only a historical relationship to the production rules used by Newell and Simon (1972)", which he calls "machine-language programming" [4]. Both agree the lineage exists; they differ on whether the later rules are the same thing.

## Related

Entries: [expert system](./expert-system.md), [knowledge base](./knowledge-base.md), [inference engine](./inference-engine.md), [MYCIN](./mycin.md), [DENDRAL](./dendral.md), [knowledge engineering](./knowledge-engineering.md), [semantic network](./semantic-network.md), [frame](./frame.md), [logic programming](./logic-programming.md), [Datalog](./datalog.md). Pages: [foundational papers](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)

**Index**

- [Cognitive architecture](cognitive-architecture.md)
- [DENDRAL](dendral.md)
- [Expert system](expert-system.md)
- [Frame](frame.md)
- [Inference engine](inference-engine.md)
- [Knowledge acquisition bottleneck](knowledge-acquisition-bottleneck.md)
- [Knowledge base](knowledge-base.md)
- [Knowledge engineering](knowledge-engineering.md)
- [Knowledge representation](knowledge-representation.md)
- [Logic programming](logic-programming.md)
- [MYCIN](mycin.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.shortliffe.net/Buchanan-Shortliffe-1984/Chapter-02.pdf : Davis and King, "The Origin of Rule-Based Systems in AI", chapter 2 of Buchanan and Shortliffe (eds.), Rule-Based Expert Systems, 1984, from Machine Intelligence 8 (1977): sections 2.1 and 2.2 (read 20261102 21:00 UTC)
2. https://www.w3.org/TR/rif-prd/ : RIF Production Rule Dialect (Second Edition), W3C Recommendation of 5 February 2013: abstract and section 1.1 (read 20261102 21:01 UTC)
3. https://api.crossref.org/works/10.2307/2371809 : Post, "Formal Reductions of the General Combinatorial Decision Problem", American Journal of Mathematics 65(2), April 1943: record only (read 20261102 21:00 UTC)
4. https://www.ijcai.org/Proceedings/77-2/Papers/092.pdf : Feigenbaum, "The Art of Artificial Intelligence: I. Themes and case studies of knowledge engineering", IJCAI-77 (read 20261102 21:00 UTC)
5. https://api.crossref.org/works/10.1016/0004-3702(82)90020-0 : Forgy, "Rete: A fast algorithm for the many pattern/many object pattern match problem", Artificial Intelligence 19(1), September 1982: record only (read 20261102 21:01 UTC)
6. https://www.shortliffe.net/Buchanan-Shortliffe-1984/Chapter-03.pdf : Buchanan and Shortliffe (eds.), Rule-Based Expert Systems, 1984, chapter 3 "The Evolution of MYCIN's Rule Form"; contents page https://www.shortliffe.net/Buchanan-Shortliffe-1984/MYCIN%20Book.htm (read 20261102 21:00 UTC)
