---
type: index
kind: concept
aliases: [data provenance, lineage, pedigree]
updated: 20261102 22:49 UTC
---

# Provenance

This entry answers what "provenance" means in databases, in the W3C PROV standard and in retrieval benchmarks such as KILT. The three senses are related but not the same.

## Definition

The W3C PROV family defines provenance as "information about entities, activities, and people involved in producing a piece of data or thing", which can be used to judge its quality, reliability or trustworthiness [1]. Buneman, Khanna and Tan call it "the description of the origins of a piece of data and the process by which it arrived in a database", and note that it is sometimes called lineage or pedigree [2]. In retrieval benchmarks the word narrows: KILT defines provenance as "a set of textual spans in Wikipedia that contain evidence for producing an output given a specific input" [3].

## How it changed

- **2001.** Buneman, Khanna and Tan (ICDT 2001) split provenance into "why" (the source data that influenced a result) and "where" (the locations in the source databases it was extracted from) [2]. See [The semantic web and linked data](../history/semantic-web.md).
- **20130430.** PROV-DM, the PROV data model, became a W3C Recommendation; W3C's publication history for it runs from a Working Draft of 20111018 to that Recommendation and shows no later step [4]. The overview of the same date lists PROV-O, an OWL 2 ontology that maps the model to RDF, among the Recommendations [1]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **June 2017.** Hartig's workshop paper on RDF\* and SPARQL\* lists provenance information among the uses of statement-level metadata [5]. See [RDF-star](./rdf-star.md).
- **20200904.** The KILT paper is first posted; its text (read at version 4, 20210527) gives every instance a provenance and awards KILT scores only when the right Wikipedia pages are found [3]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **Read 20261102.** The Graphiti README (first-party) says its context graphs "maintain provenance to source data" and that every derived fact traces back to the raw episodes that produced it [6]. See [agent memory](../trends/agent-memory.md).

## Where sources disagree

**What provenance records.** PROV and Buneman et al. describe where data came from and how it got there: the entities, activities and people, or the origin and the process [1][2]. KILT's provenance is evidence for an output, a set of spans, and holds no process [3]. *Reading:* three senses of one word, not three rival definitions; a page that says "provenance" should be read for which one it means. Graphiti's use, a link from a derived fact back to source records, is nearest to the database sense [2][6].

## Related

[RDF-star](./rdf-star.md) · [R-precision](./r-precision.md) · [knowledge graph](./knowledge-graph.md) · [RDF](./rdf.md) · [agent memory](./agent-memory.md). Benchmark: [KILT](../benchmarks/kilt.md). Data: [KILT Wikipedia snapshot](../datasets/wikipedia-dpr-kilt.md). Projects: [Graphiti](../projects/graphiti.md), [Hyper-Extract](../projects/hyper-extract.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Semantic web standards: from RDF 1.1 and RDF-star to RDF 1.2](../trends/semantic-web-standards.md)

**Projects**

- [Semantica](../projects/semantica.md)

**Benchmarks**

- [KILT](../benchmarks/kilt.md)

**Index**

- [Bi-temporal model](bi-temporal-model.md)
- [R-precision](r-precision.md)
- [RDF-star](rdf-star.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.w3.org/TR/prov-overview/ : PROV-Overview, W3C Working Group Note 20130430: abstract (definition of provenance), the family of documents with PROV-DM and PROV-O as Recommendations (read 20261102 22:06 UTC)
2. https://repository.upenn.edu/cis_papers/210/ : Buneman, Khanna and Tan, "Why and Where: A Characterization of Data Provenance", ICDT 2001, LNCS 1973 pp. 316-330: abstract (why and where), introduction (definition, "lineage", "pedigree"); record read 20261102 22:16 UTC, postprint PDF read 22:17 UTC
3. https://arxiv.org/abs/2009.02252 : Petroni et al., "KILT: a Benchmark for Knowledge Intensive Language Tasks", v1 20200904, v4 20210527 (first-party for KILT): section 2 (definition of provenance), introduction and section 5 (KILT scores); full text at https://arxiv.org/html/2009.02252 (read 20261102 22:07 UTC)
4. https://www.w3.org/TR/prov-dm/ : PROV-DM, W3C Recommendation 20130430, abstract (read 20261102 22:07 UTC); https://www.w3.org/standards/history/prov-dm/ : publication history, Working Drafts from 20111018, Recommendation 20130430, no later entry (read 20261102 22:17 UTC)
5. http://ceur-ws.org/Vol-1912/paper12.pdf : Hartig, "Foundations of RDF\* and SPARQL\*", AMW 2017 (CEUR Vol. 1912): introduction, statement-level metadata and its uses (read 20261102 22:15 UTC)
6. https://github.com/getzep/graphiti/blob/main/README.md : Graphiti README, provenance to source data, episodes (first-party; read 20261102 22:17 UTC)
