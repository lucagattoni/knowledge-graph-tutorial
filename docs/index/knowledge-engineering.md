---
type: index
kind: concept
aliases: [KE]
updated: 20261102 20:54 UTC
---

# Knowledge engineering

This entry says what knowledge engineering is, where the phrase comes from, and how its method changed from 1977 to the language-model papers of 2023.

## Definition

Knowledge engineering is the building of knowledge-based programs by working with domain experts. Feigenbaum's abstract says the knowledge engineer "practices the art of bringing the principles and tools of AI research to bear on difficult applications problems"; in his text she works intensively with an expert to acquire domain-specific knowledge and organize it for use by a program [1]. Studer, Benjamins and Fensel give the aim of the discipline: to turn the construction of knowledge-based systems "from an art into an engineering discipline", as software engineering did for software [2].

## How it changed

- 1965: Feigenbaum, Lederberg and Buchanan begin the DENDRAL program [1].
- 1968: after Feigenbaum describes DENDRAL to Donald Michie, Michie calls it "epistemological engineering"; Feigenbaum simplifies this to "knowledge engineering" [1].
- 1977: Feigenbaum's IJCAI-77 paper presents themes and case studies of the field [1].
- Early 1980s: building a system is seen as a transfer of expert knowledge into a program, mostly as production rules from interviews [2].
- Late 1980s: role-limiting methods and generic tasks are the two prominent developments [2].
- 1998: Studer et al. (March issue) describe a paradigm shift from the transfer view to a modeling view, with the frameworks CommonKADS, MIKE and PROTEGE-II [2][3].
- 20231001: Allen, Stork and Groth argue that large language models raise new questions for the field and name two directions: hybrid neuro-symbolic knowledge systems, and knowledge engineering through natural language [4].

The early period is told in [The advent](../history/advent.md) and [Knowledge systems](../history/knowledge-systems.md); the language-model line in [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

## Where sources disagree

No disagreement found in the sources read. The 1968 origin rests on Feigenbaum's own note; Michie's account was not read.

## Related

[Knowledge acquisition bottleneck](./knowledge-acquisition-bottleneck.md), [knowledge base](./knowledge-base.md), [expert system](./expert-system.md), [DENDRAL](./dendral.md), [MYCIN](./mycin.md), [production rule](./production-rule.md), [inference engine](./inference-engine.md), [ontology](./ontology.md). Papers: [foundations](../papers/foundations.md), [LLM knowledge-graph construction](../papers/llm-kg-construction.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [The advent: machines that hold knowledge](../history/advent.md)

**Index**

- [Cyc](cyc.md)
- [DENDRAL](dendral.md)
- [Expert system](expert-system.md)
- [Inference engine](inference-engine.md)
- [Knowledge acquisition bottleneck](knowledge-acquisition-bottleneck.md)
- [Knowledge base](knowledge-base.md)
- [Knowledge representation](knowledge-representation.md)
- [MYCIN](mycin.md)
- [Production rule](production-rule.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.ijcai.org/Proceedings/77-2/Papers/092.pdf : Feigenbaum, "The Art of Artificial Intelligence: I. Themes and case studies of knowledge engineering", IJCAI-77: abstract, DENDRAL begun 1965, section 2.2 historical note on Michie 1968 (read 20261102 20:45 UTC)
2. https://publikationen.bibliothek.kit.edu/189497/3003 : Studer, Benjamins, Fensel, "Knowledge engineering: Principles and methods", Data & Knowledge Engineering 25(1-2):161-197, 1998 (author copy): abstract, section 1, section 2.1 (read 20261102 20:49 UTC)
3. https://api.crossref.org/works/10.1016/S0169-023X(97)00056-6 : the same paper, issued 1998-03 (read 20261102 20:47 UTC)
4. https://arxiv.org/abs/2310.00637 : Allen, Stork, Groth, "Knowledge Engineering using Large Language Models", first submitted 1 October 2023, listed as accepted in Transactions on Graph Data and Knowledge; abstract only (read 20261102 20:46 UTC)
