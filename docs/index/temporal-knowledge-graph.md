---
type: index
kind: concept
aliases: [TKG, temporal KG]
updated: 20261102 21:28 UTC
---

# Temporal knowledge graph

A temporal knowledge graph ties each fact to time. This entry says what that means in research and in agent-memory systems, where the readings differ, and how the idea developed.

## Definition

A temporal knowledge graph is a [knowledge graph](./knowledge-graph.md) whose facts hold with respect to time, unlike a static one "whose facts do not change with time" [1][2]. A recent survey writes it as G = (E, R, T, F): sets of entities, relations and timestamps, and facts that are (head, relation, tail, timestamp) [1]. Memory systems for agents give each fact a validity window instead, and mark old facts as superseded rather than delete them [4].

## How it changed

- **200702.** Gutierrez, Hurtado and Vaisman publish "Introducing Time into RDF"; Hogan et al. describe Temporal RDF as annotating edges with time intervals [3][5]. See [The semantic web and linked data](../history/semantic-web.md).
- **2018.** The survey's table of recent methods lists TTransE, TA-TransE and HyTE, which add time to the embedding score [1]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20240302.** Cai and five co-authors post the survey (v1): most studies had treated static graphs; temporal ones "have attracted more attention" [2].
- **20250120.** Rasmussen et al. present Zep and its engine Graphiti, "a temporally-aware knowledge graph engine", with a bi-temporal model: one timeline for events, one for the order in which data entered the system [6]. See [Agent memory](../trends/agent-memory.md) and [Graphiti](../projects/graphiti.md).
- **20260113.** A survey of agent memory (v2) describes Zep as a temporal knowledge graph [7].
- **20260605.** Engram, an open-source memory engine on a bi-temporal data model, invalidates facts and never deletes them (first-party description) [8].
- **As read 20261102.** The Graphiti README says its facts "have validity windows" and that old facts are "invalidated — not deleted"; its own term for such a graph is "context graph" [4].

## Where sources disagree

The shape of the time label differs. The survey gives each fact one timestamp, as in its news-event datasets [1]. Hogan et al. describe interval annotation [3], and Graphiti uses a validity range plus a separate system-time pair [4][6]. The Zep authors call their bi-temporal approach "a novel advancement"; that is their own claim [6]. No source read compares the shapes.

## Related

[knowledge graph](./knowledge-graph.md) · [agent memory](./agent-memory.md) · [knowledge graph embedding](./knowledge-graph-embedding.md) · [RDF](./rdf.md) · [Graphiti](../projects/graphiti.md) · [Wikidata](../datasets/wikidata.md) · [LongMemEval](../benchmarks/longmemeval.md) · [agent memory papers](../papers/agent-memory.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)

**Projects**

- [Graphiti](../projects/graphiti.md)

**Papers**

- [Papers: Agent memory](../papers/agent-memory.md)

**Applied to Pinakes**

- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Agent memory](agent-memory.md)
- [Bi-temporal model](bi-temporal-model.md)
- [Knowledge graph](knowledge-graph.md)
- [Selective forgetting](selective-forgetting.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/2403.04782 : Cai et al., "A Survey on Temporal Knowledge Graph: Representation Learning and Applications": section 2.1 definition, Table 3 method years (read 20261102 21:01 UTC)
2. https://arxiv.org/abs/2403.04782 : the same survey, abstract and submission history (v1 20240302) (read 20261102 21:00 UTC)
3. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs" (v6), section 3.3 on context, Temporal RDF, reference 210 (read 20261102 21:01 UTC)
4. https://raw.githubusercontent.com/getzep/graphiti/main/README.md : Graphiti README: temporal context graphs, validity windows, invalidation, the term "context graph" (read 20261102 21:28 UTC)
5. https://api.crossref.org/works/10.1109/tkde.2007.34 : Crossref record: Gutierrez, Hurtado, Vaisman, "Introducing Time into RDF", IEEE TKDE 19(2), February 2007, pages 207-218 (read 20261102 21:05 UTC)
6. https://arxiv.org/html/2501.13956 : Rasmussen et al., "Zep: A Temporal Knowledge Graph Architecture for Agent Memory", v1 20250120: bi-temporal model, edge invalidation, "novel advancement" wording (read 20261102 21:01 UTC)
7. https://arxiv.org/pdf/2512.13564 : Hu et al., "Memory in the Age of AI Agents" (v2, 13 Jan 2026): Zep described as a Temporal Knowledge Graph (read 20261102 21:01 UTC)
8. https://arxiv.org/abs/2606.09900 : "Less Context, More Accuracy: A Bi-Temporal Memory Engine for LLM Agents", submitted 20260605 (v1), abstract: open-source engine on a bi-temporal data model, "invalidating, never deleting" (read 20261102 21:25 UTC)
