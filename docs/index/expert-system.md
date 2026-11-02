---
type: index
kind: concept
aliases: [rule-based expert system]
updated: 20261102 21:25 UTC
---

# Expert system

An expert system is a program that solves problems in a narrow field by reasoning over knowledge taken from human experts. This page defines the term, dates its rise and fall, and shows where sources disagree on both its first example and its decline.

## Definition

No source read gives a formal definition, so this paragraph joins three. The AI100 history describes expert systems as "knowledge repositories tailored for specialized domains such as chemistry and medical diagnosis" [1]. Gutierrez and Sequeda call them early knowledge-based systems that "encoded domain knowledge as if-then rules" [2]. Feigenbaum shows the form in MYCIN, whose rules read IF conjunctive clauses THEN implication, and treats the building of such systems as [knowledge engineering](./knowledge-engineering.md) [3].

## How it changed

- **1965.** DENDRAL begins at Stanford; Feigenbaum calls it "an early herald of AI's shift to the knowledge-based paradigm" [3]. Era: [Advent](../history/advent.md).
- **1970s.** MYCIN originates in Shortliffe's doctoral thesis, cited as 1976 [3]; Shadbolt cites MYCIN papers of 1973 and 1976 [4]. Shadbolt writes that expert systems "appeared as a distinct line around the late 70's" [4].
- **1979 to 1980.** EMYCIN, MYCIN without its domain knowledge, opens "the age of the expert system shell"; XCON/R1 configures DEC VAX orders [4]. Era: [Knowledge systems](../history/knowledge-systems.md).
- **1981 and 1982.** Japan's ICOT initiative starts; the UK Alvey Report leads to a 350 million pound programme [4].
- **1987.** Bundy observes success with small commercial rule-based systems, for example fault diagnosis in under 100 rules (quoted by Shadbolt) [4].
- **Mid-1980s or early 1990s.** Interest falls and funding dries up; see below. Afterwards the experience was rolled into mainstream IT tools [2].

## Where sources disagree

The first expert system. Shadbolt: many name MYCIN, others DENDRAL or MACSYMA, and "there is considerable argument" about when the divergence took place [4].

The decline. The AI100 history places the fall of interest and funding in the mid-1980s [1]. Gutierrez and Sequeda place it at the beginning of the 1990s, when such systems proved expensive, hard to update and brittle [2]. *Reading:* the first speaks of AI as a whole, the second of expert systems and the Fifth Generation project.

## Related

[Knowledge base](./knowledge-base.md), [production rule](./production-rule.md), [inference engine](./inference-engine.md), [MYCIN](./mycin.md), [DENDRAL](./dendral.md), [knowledge engineering](./knowledge-engineering.md), [knowledge acquisition bottleneck](./knowledge-acquisition-bottleneck.md), [frame](./frame.md), [logic programming](./logic-programming.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [The advent: machines that hold knowledge](../history/advent.md)
- [The Web changes data and search](../history/the-web.md)

**Index**

- [Cognitive architecture](cognitive-architecture.md)
- [Cyc](cyc.md)
- [Datalog](datalog.md)
- [DENDRAL](dendral.md)
- [Frame](frame.md)
- [Inference engine](inference-engine.md)
- [Knowledge acquisition bottleneck](knowledge-acquisition-bottleneck.md)
- [Knowledge base](knowledge-base.md)
- [Knowledge engineering](knowledge-engineering.md)
- [Knowledge representation](knowledge-representation.md)
- [Logic programming](logic-programming.md)
- [MYCIN](mycin.md)
- [Production rule](production-rule.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://ai100.stanford.edu/2016-report/appendix-i-short-history-ai : Stanford AI100 (2016), Appendix I: expert systems as knowledge repositories; interest fell and funding dried up in the mid-1980s (read 20261102 20:44 UTC)
2. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, CACM 64(3), 2021: expert systems as if-then rules; the beginning of the 1990s; mainstream IT tools (read 20261102 20:44 UTC)
3. https://www.ijcai.org/Proceedings/77-2/Papers/092.pdf : Feigenbaum, "The Art of Artificial Intelligence", IJCAI-77: DENDRAL begun 1965, "herald", MYCIN origin and rule form (read 20261102 20:45 UTC)
4. https://eprints.soton.ac.uk/252374/1/A_Natural_History_of_Expert_Systems_1989.pdf : Shadbolt, "Expert systems - a natural history", 1989: first-system dispute, EMYCIN, XCON/R1, ICOT, Alvey, Bundy 1987 (read 20261102 20:44 UTC)
