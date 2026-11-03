---
type: index
kind: concept
aliases: [cognitive architectures]
updated: 20261102 22:24 UTC
---

# Cognitive architecture

This entry says what a cognitive architecture is, which systems the name covers, and how language-agent research took its memory vocabulary from the tradition.

## Definition

Kotseruba and Tsotsos report that most surveys define a cognitive architecture as "a blueprint for intelligence": a proposal about the mental representations, and the computational procedures that operate on them, that enable a range of intelligent behaviours [1]. The Soar project calls Soar "a general cognitive architecture for developing systems that exhibit intelligent behavior" [2]. Sumers et al. describe the shared design as a production system plus sensory grounding, long-term memory and a decision procedure for choosing actions [3]. See [production rule](./production-rule.md).

## How it changed

- **From the 1950s.** Research on cognitive architectures is part of general AI, which began then; its stated aim is to model the human mind [1]. See [The advent](../history/advent.md).
- **198709.** Laird, Newell and Rosenbloom publish "SOAR: An architecture for general intelligence" (*Artificial Intelligence* 33(1)) [4]. See [Knowledge systems: boom and bust](../history/knowledge-systems.md).
- **20161027.** Kotseruba and Tsotsos post a survey (v1). Its current abstract counts 84 architectures, 49 still actively developed, and over 900 practical projects [1]. It appeared online on 20180728 and in print in 2020 [5]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20230905.** Sumers et al. propose CoALA: a language agent with modular memory components, a structured action space and a decision-making process, drawing on cognitive science and symbolic AI [3]. See [Agent memory](../trends/agent-memory.md).
- **20260413.** Roynard argues that CoALA and JEPA lack an explicit knowledge layer and proposes four layers with different persistence rules (first-party, one author; v2 20260612) [6].
- **20260506.** Soar 9.6.5 is released, after 9.6.4 on 20250722 [7].

## Where sources disagree

What counts as one. Kotseruba and Tsotsos report that Laird excludes toolkits for building agents, such as GOMS and BDI, while the authors of Pogamut, a toolkit, count it as one; Sun separates psychology-based architectures from engineering ones [1]. They also note that "no clear definition and general theory of cognition" exists, so architectures rest on different premises and are hard to compare [1].

## Related

[Agent](./agent.md) · [agent memory](./agent-memory.md) · [production rule](./production-rule.md) · [expert system](./expert-system.md) · [knowledge base](./knowledge-base.md) · [large language model](./large-language-model.md) · [agent memory papers](../papers/agent-memory.md) · [plain files as agent knowledge papers](../papers/plain-file-knowledge.md) · [agent memory trend](../trends/agent-memory.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Papers**

- [Papers: Agent memory](../papers/agent-memory.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/1610.08602v3 : Kotseruba and Tsotsos, "A Review of 40 Years of Cognitive Architecture Research", v1 20161027, v3 13 January 2018: abstract; section 2 (aim, "no clear definition", Laird, Pogamut, Sun, the blueprint definition) (read 20261102 22:06 UTC; abstract page https://arxiv.org/abs/1610.08602 read 22:06 UTC)
2. https://soar.eecs.umich.edu/ : Soar homepage, definition sentence and news "Soar 9.6.5 available for download" (read 20261102 22:12 UTC)
3. https://arxiv.org/abs/2309.02427 : Sumers, Yao, Narasimhan, Griffiths, "Cognitive Architectures for Language Agents", v1 20230905, v3 TMLR camera-ready; abstract (read 20261102 22:06 UTC); production-system description (introduction, Figure 2 caption) from https://arxiv.org/html/2309.02427 (read 20261102 22:07 UTC)
4. https://api.crossref.org/works/10.1016/0004-3702(87)90050-6 : Crossref record: Laird, Newell, Rosenbloom, "SOAR: An architecture for general intelligence", *Artificial Intelligence* 33(1), pp. 1-64, September 1987 (read 20261102 22:13 UTC)
5. https://api.crossref.org/works/10.1007/s10462-018-9646-y : Crossref record: Kotseruba and Tsotsos, *Artificial Intelligence Review* 53(1), pp. 17-94; online 20180728, print January 2020 (read 20261102 22:13 UTC)
6. https://arxiv.org/abs/2604.11364 : Roynard, "The Missing Knowledge Layer in Cognitive Architectures for AI Agents", v1 20260413, v2 20260612; abstract (read 20261102 22:08 UTC)
7. https://github.com/SoarGroup/Soar/releases : GitHub releases "releases/9.6.5", published 2026-05-06, and "releases/9.6.4", published 2025-07-22, read through the GitHub API (read 20261102 22:14 UTC)
