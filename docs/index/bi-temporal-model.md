---
type: index
kind: concept
aliases: [bitemporal, bi-temporal, bitemporal table]
updated: 20261102 22:18 UTC
---

# Bi-temporal model

This entry says what a bi-temporal model stores, where the idea comes from in database research, and how agent-memory systems took the word over.

## Definition

A bi-temporal model keeps two time axes for each fact. The valid time of a fact is "the time when the fact is true in the modeled reality"; its transaction time is when the fact is current in the database and can be retrieved [1]. The consensus glossary of temporal databases defines a bitemporal relation as one with exactly one system-supported valid time and exactly one system-supported transaction time [1]. SQL:2011 offers the two axes as an application-time period (valid time) and system-versioned tables (transaction time); a table with both is called bitemporal [2].

## How it changed

- **1992 to 1998.** A consensus effort on terms starts in early 1992, with versions in SIGMOD Record in September 1992 and March 1994; the February 1998 version (LNCS 1399) defines the bitemporal relation [1]. See [The Web changes data and search](../history/the-web.md).
- **December 2011.** SQL:2011 is published with temporal tables inside Part 2; an ISO temporal part begun in 1995 had been cancelled in 2001. The standard names no term for tables with both periods; Kulkarni and Michels use "bitemporal tables" as the literature does [2]. See [The semantic web and linked data](../history/semantic-web.md).
- **20250120.** Rasmussen et al. write that Zep "implements a bi-temporal model": one timeline for the order of events, one for the order of ingestion. They call it "a novel advancement" in LLM-based graph construction (first-party) [3][4]. See [Graphiti](../projects/graphiti.md) and [Agent memory](../trends/agent-memory.md).
- **20260605, 20260711.** Engram stamps each episode with event time and ingestion time (first-party) [5][6]. TGMS, a graph system for agents, "separates valid time from transaction time" (first-party) [7].
- **As read 20261102.** The Graphiti README sets GraphRAG's "Basic timestamp tracking" against its own "Explicit bi-temporal tracking" (first-party) [8].

## Where sources disagree

**What "bi" counts.** The glossary adopts exactly one valid time and one transaction time, and records an alternative: one or more of each, with "bi" counting kinds of time [1].

**Who supplies the valid time.** In the glossary valid times are usually supplied by the user [1], and in SQL:2011 the user fills the application-time columns [2]. In Zep the system extracts the times of facts from the text of each episode [3]. No source read compares the agent-memory use with the glossary definition.

## Related

[Temporal knowledge graph](./temporal-knowledge-graph.md) · [agent memory](./agent-memory.md) · [relational model](./relational-model.md) · [SQL](./sql.md) · [provenance](./provenance.md) · [Graphiti](../projects/graphiti.md) · [agent memory papers](../papers/agent-memory.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)

**Projects**

- [Graphiti](../projects/graphiti.md)

**Papers**

- [Papers: Agent memory](../papers/agent-memory.md)

**Index**

- [Selective forgetting](selective-forgetting.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www2.cs.arizona.edu/people/rts/pubs/LNCS1399.pdf : Jensen and Dyreson (eds.) with 24 co-authors, "The Consensus Glossary of Temporal Database Concepts, February 1998 Version", LNCS 1399, pp. 367-405, 1998: abstract (1992, 1994 versions), sections 3.1, 3.2, 3.8 (read 20261102 22:10 UTC)
2. https://sigmodrecord.org/publications/sigmodRecord/1209/pdfs/07.industry.kulkarni.pdf : Kulkarni and Michels (IBM), "Temporal features in SQL:2011", SIGMOD Record 41(3), September 2012: sections 1, 2, 2.1, 2.4 and footnote 5 (read 20261102 22:10 UTC)
3. https://arxiv.org/html/2501.13956 : Rasmussen et al., "Zep: A Temporal Knowledge Graph Architecture for Agent Memory": bi-temporal model, "novel advancement", section 2.2.3 four timestamps (read 20261102 22:07 UTC)
4. https://arxiv.org/abs/2501.13956 : the same paper, submission history (v1 20250120) (read 20261102 22:06 UTC)
5. https://arxiv.org/abs/2606.09900 : Wang, "Less Context, More Accuracy: A Bi-Temporal Memory Engine for LLM Agents", v1 20260605, abstract (read 20261102 22:06 UTC)
6. https://arxiv.org/html/2606.09900 : the same paper, section 3.1 "Bi-temporal data model": event time and ingested-at (read 20261102 22:07 UTC)
7. https://arxiv.org/abs/2607.10265 : Zhang, "TGMS: An Agent-Native Bi-Temporal Graph Management System", v1 20260711, abstract (read 20261102 22:16 UTC)
8. https://raw.githubusercontent.com/getzep/graphiti/main/README.md : Graphiti README, comparison table with GraphRAG (read 20261102 22:12 UTC)
