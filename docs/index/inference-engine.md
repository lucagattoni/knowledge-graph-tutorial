---
type: index
kind: concept
aliases: [rule interpreter]
updated: 20261102 21:22 UTC
---

# Inference engine

This entry explains the part of a rule-based system that applies rules to facts, and why the same words now also name software that serves language models.

## Definition

An inference engine is the program that applies the rules of a [knowledge base](./knowledge-base.md) to the facts of a case to reach conclusions, kept apart from the domain knowledge. The founding statement is the MYCIN team's hypothesis that "domain-specific knowledge could successfully be kept separate from the inference procedures" [1]. The same book describes the rule interpreter of EMYCIN, the domain-independent core of [MYCIN](./mycin.md): it works toward a goal by backward chaining of [production rules](./production-rule.md), retrieves the rules whose conclusions bear on that goal, and applies each rule whose premise holds [2]. The pages read give no one-sentence definition; this paragraph summarises [1] and [2].

## How it changed

- **1974 (autumn).** Bill van Melle starts to test the claim that MYCIN's knowledge can be replaced while the inference procedures stay unchanged [1]. See [formal foundations](../history/formal-foundations.md).
- **1979 and 1984.** Shadbolt cites EMYCIN as "van Melle et al 1979,1984" and describes it as MYCIN stripped of its domain knowledge: a rule language with backward chaining, certainty handling and explanation. He writes that "the age of the expert system shell had dawned" [3]. See [knowledge systems](../history/knowledge-systems.md).
- **1981 and 1984.** The EMYCIN chapter, first printed in 1981 and reprinted in the 1984 book, notes a limit: some of its power comes from the rule-based representation and the backward-chaining structure, so it does not suit every application [2].
- **1980s and early 1990s.** In their account of the 1980s, Gutierrez and Sequeda name KL-ONE, LOOM, CLASSIC and F-Logic among early logic systems that "showed that logical reasoning could be implemented in tractable software" and "would become the underpinning to OWL" [5]. See [OWL](./owl.md) and [description logics](./description-logic.md). At the beginning of the 1990s, they write, expert systems "proved expensive and difficult to update and maintain", and the IT world "rolled that experience into mainstream IT tools from vendors such as IBM, SAP, and Oracle" [5]. They do not say that rules or inference as such moved into those tools.
- **Now (read 20261102).** The phrase also names software that runs a trained model. The vLLM project describes itself as "a high-throughput and memory-efficient inference and serving engine for LLMs" [4]. The date of this second use is **unstated** in the pages read.

## Where sources disagree

The sources do not dispute the idea; they use different names. In one book the chapter title says "inference engine" [1], the section on EMYCIN says "rule interpreter" [2], and its figure labels the part "consultation driver" [2]. A second sense has grown beside the first: in the vLLM description the word "inference" means running a language model, not deriving conclusions from rules [4].

## Related

[knowledge base](./knowledge-base.md), [production rule](./production-rule.md), [expert system](./expert-system.md), [MYCIN](./mycin.md), [knowledge engineering](./knowledge-engineering.md), [logic programming](./logic-programming.md), [Datalog](./datalog.md), [description logic](./description-logic.md), [large language model](./large-language-model.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)

**Index**

- [Expert system](expert-system.md)
- [Knowledge base](knowledge-base.md)
- [Knowledge engineering](knowledge-engineering.md)
- [Logic programming](logic-programming.md)
- [MYCIN](mycin.md)
- [Production rule](production-rule.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.shortliffe.net/Buchanan-Shortliffe-1984/Chapter-14.pdf : the MYCIN book (Buchanan and Shortliffe, Addison-Wesley, 1984; contents page https://www.shortliffe.net/Buchanan-Shortliffe-1984/MYCIN%20Book.htm, read 20261102 20:51 UTC), chapter 14 "Use of the MYCIN Inference Engine": separation of knowledge from inference procedures, van Melle in the fall of 1974 (scanned pages, text by on-device OCR; read 20261102 20:54 UTC)
2. https://www.shortliffe.net/Buchanan-Shortliffe-1984/Chapter-15.pdf : same book, chapter 15 (van Melle, Shortliffe, Buchanan), "EMYCIN", section 15.2.1 "The Rule Interpreter", Figure 15-1, footnote on limits, note that it is an edited version of a 1981 paper (scanned pages, OCR; read 20261102 20:54 UTC)
3. https://eprints.soton.ac.uk/252374/1/A_Natural_History_of_Expert_Systems_1989.pdf : Shadbolt, "Expert systems: a natural history", 1989 (in Research and Development in Expert Systems VI, Cambridge University Press): EMYCIN, the shell (PDF text extracted and read 20261102 21:22 UTC; the "van Melle et al 1979,1984" citation and the shell sentence confirmed then)
4. https://github.com/vllm-project/vllm : vLLM repository description, first-party (read 20261102 20:53 UTC)
5. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: rules and inference in mainstream software, logic systems as the base of OWL (read 20261102 21:22 UTC, re-read from the PDF text)
