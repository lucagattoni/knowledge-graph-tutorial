---
type: index
kind: concept
aliases: [knowledge acquisition problem]
updated: 20261102 21:22 UTC
---

# Knowledge acquisition bottleneck

This entry says what the bottleneck is, who used the word first in the sources read, and how the view of it changed. It ends with the question whether language models remove it.

## Definition

The knowledge acquisition bottleneck is the difficulty of getting domain knowledge from human experts into the knowledge base of a program. Feigenbaum, describing why his group began META-DENDRAL, wrote that "the acquisition of domain knowledge was the bottleneck problem" in building applications-oriented intelligent agents [1]. Studer, Benjamins and Fensel describe the early practice: the knowledge was "obtained by interviewing experts", written as production rules, and this transfer approach "failed to produce large, reliable and maintainable knowledge bases" [2].

## How it changed

- 1970s: Gutierrez and Sequeda name the open problem of where to obtain the data and knowledge; "This area would be called knowledge acquisition" [3].
- 1977: Feigenbaum calls it "the bottleneck problem" and, elsewhere, "the knowledge acquisition problem". META-DENDRAL, a program that infers rules of molecular fragmentation from mass-spectrometer data, is his case of automatic acquisition; he also calls explanation "part of the concerted attack" on the problem [1].
- Early 1980s: building a system was seen as a transfer of expert knowledge into a program [2].
- 1985: Lenat, Prakash and Shepherd title the Cyc paper "...Overcome Brittleness and Knowledge Acquisition Bottlenecks" (AI Magazine 6(4)) [4]; see [Cyc](./cyc.md).
- 1998: Studer et al. report a paradigm shift from the transfer view to a modeling view. The assumption that knowledge is a set of existing elements to be collected "was wrong due to the important role of tacit knowledge" [2].
- 20250529: AutoSchemaKG builds knowledge graphs from text without predefined schemas, using language models [5]. The trend is told in [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

The older period is told in [Knowledge systems](../history/knowledge-systems.md). Who first used the exact phrase "knowledge acquisition bottleneck" is **unstated** in the sources read.

## Where sources disagree

The diagnosis differs. Feigenbaum puts the problem in the effort of acquiring domain knowledge [1]. Studer et al. put it in a wrong assumption: that expert knowledge already exists in a form that can be collected [2]. Whether language models remove the bottleneck is **unstated** in the abstract of [5]; it reports construction without predefined schemas, not the effort of acquisition.

## Related

[Knowledge engineering](./knowledge-engineering.md), [knowledge base](./knowledge-base.md), [expert system](./expert-system.md), [production rule](./production-rule.md), [DENDRAL](./dendral.md), [Cyc](./cyc.md), [ontology](./ontology.md). Papers: [foundations](../papers/foundations.md), [LLM knowledge-graph construction](../papers/llm-kg-construction.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [The Web changes data and search](../history/the-web.md)

**Trends**

- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)

**Index**

- [Cyc](cyc.md)
- [Distant supervision](distant-supervision.md)
- [Expert system](expert-system.md)
- [Knowledge base](knowledge-base.md)
- [Knowledge engineering](knowledge-engineering.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.ijcai.org/Proceedings/77-2/Papers/092.pdf : Feigenbaum, "The Art of Artificial Intelligence: I. Themes and case studies of knowledge engineering", IJCAI-77: META-DENDRAL historical note, explanation and the acquisition problem (read 20261102 21:21 UTC)
2. https://publikationen.bibliothek.kit.edu/189497/3003 : Studer, Benjamins, Fensel, "Knowledge engineering: Principles and methods", Data & Knowledge Engineering 25(1-2):161-197, 1998 (author copy): sections 1 and 2.1 (read 20261102 20:49 UTC)
3. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: the 1970s period (read 20261102 20:45 UTC)
4. https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/510 : Lenat, Prakash, Shepherd, AI Magazine 6(4), 1985, title; the day-precise date on the era page was not confirmed (read 20261102 20:11 UTC by the era writer, via the page docs/history/knowledge-systems.md; fetched again at 20:47 UTC and refused by the site's bot check)
5. https://arxiv.org/abs/2505.23628 : AutoSchemaKG, first submitted 29 May 2025, abstract: construction "eliminates the need for predefined schemas" (first-party; read 20261102 20:50 UTC)
