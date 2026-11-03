---
type: index
kind: concept
aliases: [logic programs, programming in logic]
updated: 20261102 21:25 UTC
---

# Logic programming

Logic programming is the use of logic as a programming language: logical statements are the program, and running it means proving a goal. This entry gives the originators' definition, dated steps to the ISO Prolog standard, and the two senses of the word.

## Definition

In 1974 Kowalski proposed reading an implication "B if A1 and ... and An" as a procedure declaration, where B is the procedure name and A1 to An are the calls that make up its body. An axiomatisation of a problem domain is then a program, and a problem is posed as a theorem to be proved [1]. In 1988 he described it as using logic to represent knowledge and deduction to derive consequences. It "allows us to view the same knowledge both declaratively and procedurally" [2]. The plainest case is Horn clauses with backward reasoning embedded in resolution [2].

## How it changed

- **Summer 1971.** Kowalski's first visit to the Marseilles group, who were building a natural-language question-answering system, yields work on parsing with resolution. Because of it 1971 "is sometimes given as the year Prolog was born" [2].
- **Summer 1972.** Roussel and Colmerauer designed and implemented the first Prolog system in Algol-W. The name abbreviates *programmation en logique* [2].
- **1974.** Kowalski's "Predicate logic as programming language" appears in *Information Processing 74* [1]. Era: [Formal foundations](../history/formal-foundations.md).
- **1982.** Shadbolt, writing in 1989, notes that Prolog "requires little augmentation" to serve as an expert-system shell and names APES (Hammond 1982) as one of the first such products [3]. Era: [Knowledge systems](../history/knowledge-systems.md).
- **19950601.** ISO/IEC 13211-1:1995 (Prolog, part 1, general core) is approved. A standards retailer lists it as valid, corrected in 2007, 2012 and 2017 [4]. Era: [The Web changes data and search](../history/the-web.md).
- **20220126.** Körner and ten co-authors post a survey, "Fifty Years of Prolog and Beyond", accepted for *Theory and Practice of Logic Programming*. It follows Prolog's evolution up to the ISO standard and after [5].

## Where sources disagree

The word is used in two senses. Kowalski reserves "Prolog" for the language and notes that claims for the general concept do not always hold for the language, and the reverse [2]. The birth year differs by what is counted: 1971 for the first Marseilles collaboration, summer 1972 for the first system [2]. Kowalski recalls that most North American AI researchers then thought resolution discredited (a participant's account) [2].

## Related

[Expert system](./expert-system.md), [production rule](./production-rule.md), [inference engine](./inference-engine.md), [Datalog](./datalog.md), [closed-world assumption](./closed-world-assumption.md), [MYCIN](./mycin.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)

**Index**

- [Closed-world assumption](closed-world-assumption.md)
- [Datalog](datalog.md)
- [Expert system](expert-system.md)
- [Inference engine](inference-engine.md)
- [Production rule](production-rule.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.doc.ic.ac.uk/~rak/papers/IFIP%2074.pdf : Kowalski, "Predicate logic as programming language", Information Processing 74, North-Holland, 1974; abstract and introduction (scanned file, read by OCR; read 20261102 21:02 UTC)
2. https://www.doc.ic.ac.uk/~rak/papers/the%20early%20years.pdf : Kowalski, "The early years of logic programming", Communications of the ACM 31(1), January 1988; characterisation, 1971 and 1972 events, Edinburgh climate (scanned file, read by OCR; read 20261102 21:02 UTC)
3. https://eprints.soton.ac.uk/252374/1/A_Natural_History_of_Expert_Systems_1989.pdf : Shadbolt, "Expert systems - a natural history", 1989; Prolog shells, APES (Hammond 1982) (read 20261102 21:24 UTC)
4. https://www.sis.se/en/produkter/information-technology-office-machines/languages-used-in-information-technology/isoiec132111/ : Swedish Institute for Standards record of ISO/IEC 13211-1:1995, approved 1995-06-01, valid, Cor 1:2007, Cor 2:2012, Cor 3:2017; a retailer's record of the ISO standard, whose own page refused access (read 20261102 21:02 UTC)
5. https://arxiv.org/abs/2201.10816 : Körner et al., "Fifty Years of Prolog and Beyond", 11 authors, v1 20220126; abstract; accepted for TPLP per the page's comments (read 20261102 21:02 UTC)
