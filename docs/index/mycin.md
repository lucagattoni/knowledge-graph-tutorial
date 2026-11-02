---
type: index
kind: system
aliases: [EMYCIN]
updated: 20261102 21:25 UTC
---

# MYCIN

MYCIN is the Stanford rule-based program that advised physicians on antibiotic therapy, built in the 1970s. This entry gives what it was, dated steps to its 1979 evaluation and to EMYCIN, and the dispute over whether it was the first expert system.

## Definition

Its builders call MYCIN an expert system: an AI program meant to give expert-level solutions to complex problems, to be understandable, and to take in new knowledge easily. It advises through a consultative dialogue, with a knowledge base and an inference engine; most knowledge is written as rules of the form IF evidence for A and B, THEN evidence for C [1]. Its task was the selection of antimicrobial therapy. It began with bacteremias and was extended to meningitis [2]. Shadbolt adds cystitis [3].

## How it changed

- **October 1973.** The first grant application describes a collaboration of clinical pharmacology, infectious disease and computer science, under way for "the past year and a half" [1]. Era: [Formal foundations](../history/formal-foundations.md).
- **1976.** Shadbolt's references list Shortliffe's book *Computer-based medical consultations: MYCIN* [3].
- **1979.** A blinded evaluation (*JAMA* 242, 1979) uses ten meningitis cases and eight evaluators, infectious-disease specialists who did not know that a computer program was among the prescribers. 65% of MYCIN's prescriptions are rated acceptable, against a mean of 55.5% for five Stanford faculty specialists (range 42.5% to 62.5%). The authors include the MYCIN team (first-party) [2].
- **1979 to 1984.** Shadbolt cites van Melle's 1979 report on a domain-independent production-rule system and the 1984 EMYCIN paper by van Melle and colleagues; 1979 is the year of that reference. He reads EMYCIN as MYCIN stripped of its domain knowledge, leaving rule-based representation, backward chaining, certainty handling and explanation [3]. It is "based on the domain-independent core of the MYCIN program" [4]. Era: [Knowledge systems](../history/knowledge-systems.md).
- **1984.** Buchanan and Shortliffe edit *Rule-Based Expert Systems: The MYCIN Experiments of the Stanford Heuristic Programming Project* (Addison-Wesley), whose chapters 15 (EMYCIN) and 31 (the evaluation) are cited here [5][2][4].

## Where sources disagree

Which system was the first expert system. Shadbolt writes that "many would regard" MYCIN as the first and original one. He names DENDRAL (Stanford) and MACSYMA (MIT; Martin et al., 1971) as other contenders, and notes that all early systems share strong similarities [3].

## Related

[Expert system](./expert-system.md), [production rule](./production-rule.md), [inference engine](./inference-engine.md), [knowledge base](./knowledge-base.md), [knowledge engineering](./knowledge-engineering.md), [DENDRAL](./dendral.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)

**Index**

- [DENDRAL](dendral.md)
- [Expert system](expert-system.md)
- [Inference engine](inference-engine.md)
- [Knowledge engineering](knowledge-engineering.md)
- [Logic programming](logic-programming.md)
- [Production rule](production-rule.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.shortliffe.net/Buchanan-Shortliffe-1984/Chapter-01.pdf : Buchanan and Shortliffe (eds.), *Rule-Based Expert Systems: The MYCIN Experiments of the Stanford Heuristic Programming Project*, Addison-Wesley, 1984, chapter 1 (scanned file, read by OCR; read 20261102 21:02 UTC)
2. https://www.shortliffe.net/Buchanan-Shortliffe-1984/Chapter-31.pdf : Yu et al., chapter 31, an edited version of JAMA 242:1279-1282 (1979); Table 31-1 and text (scanned file, read by OCR; read 20261102 21:02 UTC)
3. https://eprints.soton.ac.uk/252374/1/A_Natural_History_of_Expert_Systems_1989.pdf : Shadbolt, "Expert systems - a natural history", 1989; MYCIN, DENDRAL, MACSYMA, EMYCIN and its references (read 20261102 21:24 UTC)
4. https://www.shortliffe.net/Buchanan-Shortliffe-1984/Chapter-15.pdf : van Melle, Shortliffe, Buchanan, chapter 15, EMYCIN; a shortened version of a 1981 Infotech report paper (scanned file, read by OCR; read 20261102 21:02 UTC)
5. https://www.shortliffe.net/Buchanan-Shortliffe-1984/MYCIN%20Book.htm : landing page of the book with its chapter list; edited by Buchanan and Shortliffe, Addison-Wesley, 1984 (read 20261102 21:02 UTC)
