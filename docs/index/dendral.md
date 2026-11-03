---
type: index
kind: system
aliases: []
updated: 20261102 21:25 UTC
---

# DENDRAL

DENDRAL is a Stanford program, begun in 1965, that proposes the molecular structure of an organic compound from instrument data. It is an early case of a program whose power came from encoded expert knowledge, and it is one of the contenders for the first expert system.

## Definition

Feigenbaum describes DENDRAL, begun in 1965 as a collaboration with the Stanford Mass Spectrometry Laboratory, as a program that enumerates plausible structures (atom-bond graphs) for organic molecules, given data from a mass spectrometer and a nuclear magnetic resonance spectrometer plus constraints from the user [1]. Its method is heuristic search in three stages: plan, generate (a program called CONGEN) and test [1]. Its knowledge of mass spectrometry is held as rules that pair an atomic configuration with a probability and a fragmentation [1]. Shadbolt gives the same function in one line: to infer the molecular structure of unknown compounds from mass-spectral and nuclear-magnetic-resonance data [2].

## How it changed

- **1965.** Feigenbaum, Lederberg and Buchanan begin the project, to study scientific discovery and to build programs useful to working scientists [1]. Era: [The advent](../history/advent.md).
- **About 1967.** New knowledge accumulated so fast that the system was close to "ossification"; the answer was a rule-based representation, which the team kept in later projects [1].
- **1968.** Feigenbaum describes DENDRAL to Donald Michie, who calls it "epistemological engineering"; Feigenbaum shortens this to [knowledge engineering](./knowledge-engineering.md) [1].
- **1970.** The first major summary of results states that general problem-solvers are too weak for high performance, so specialists' knowledge is needed (cited by Feigenbaum with the year 1971) [1].
- **1977.** Feigenbaum calls it one of the longest-lived continuous efforts in AI and "an early herald of AI's shift to the knowledge-based paradigm" [1]. Era: [Formal foundations](../history/formal-foundations.md).
- **After 1977.** The sources read are silent on when work on DENDRAL ended: unstated.

## Where sources disagree

Whether it was the first expert system. Shadbolt writes that many regard [MYCIN](./mycin.md) as the first and original one; "some would argue in favour of" DENDRAL, citing "Buchanan et al 1978" (its reference list has a 1978 Buchanan and Feigenbaum paper in Artificial Intelligence 11; text not read), and MIT's MACSYMA is a third contender [2]. Feigenbaum does not make the claim; he calls DENDRAL a herald of the knowledge-based shift [1].

## Related

[Expert system](./expert-system.md), [production rule](./production-rule.md), [knowledge engineering](./knowledge-engineering.md), [MYCIN](./mycin.md), [knowledge base](./knowledge-base.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)

**Index**

- [Expert system](expert-system.md)
- [Knowledge acquisition bottleneck](knowledge-acquisition-bottleneck.md)
- [Knowledge engineering](knowledge-engineering.md)
- [MYCIN](mycin.md)
- [Production rule](production-rule.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.ijcai.org/Proceedings/77-2/Papers/092.pdf : Feigenbaum, "The Art of Artificial Intelligence: I. Themes and case studies of knowledge engineering", IJCAI-77, section 3.1 on DENDRAL, section 2.2 on the term, conclusion on DENDRAL (read 20261102 20:49 UTC)
2. https://eprints.soton.ac.uk/252374/1/A_Natural_History_of_Expert_Systems_1989.pdf : Shadbolt, "Expert systems - a natural history", 1989: section 2 "Origins" and reference list (read 20261102 20:50 UTC; reread 20261102 21:22 UTC)
