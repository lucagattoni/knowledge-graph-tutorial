---
type: index
kind: concept
aliases: [RDF triple, triplet, RDF statement]
updated: 20261103 01:52 UTC
---

# Triple

This entry says what a triple is and how its name and shape changed, from RDF 1999 to RDF 1.2.

## Definition

In RDF 1.1 Concepts, an RDF triple "consists of three components": a subject (an IRI or a blank node), a predicate (an IRI) and an object (an IRI, a literal or a blank node), conventionally in that order [1]. The predicate denotes a property that "can be thought of as a binary relation"; relations among more than two entities "can only be indirectly expressed" [1]. An RDF graph is a set of triples [1]. Hogan et al. give the same shape for knowledge graphs generally: nodes are entities, directed labelled edges are binary relations [10].

## How it changed

- **19990222.** *RDF Model and Syntax* names the unit a statement (subject, predicate, object); its formal model writes it as a triple, {pred, sub, obj} [3]. Era: [The Web changes data and search](../history/the-web.md).
- **20040210.** RDF 1.0 says "The underlying structure of any expression in RDF is a collection of triples" [2]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **2013.** Bordes et al. write "triplets (h, ℓ, t)" of two entities and a relationship [6]. See [knowledge graph embedding](./knowledge-graph-embedding.md).
- **20140225.** RDF 1.1 Concepts becomes a Recommendation [1]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20250529.** AutoSchemaKG has language models extract "knowledge triples" at scale, reporting 5.9 billion edges (first-party) [8]. See [LLM graph construction](../trends/llm-kg-construction.md).
- **20260407.** RDF 1.2 Concepts, a Candidate Recommendation Snapshot, adds the triple term: a triple used as a term in the object position of another triple [4]. W3C's history shows no later step, and RDF 1.1 stays the latest Recommendation [4][5]. See [RDF-star](./rdf-star.md); still moving: [Semantic web standards](../trends/semantic-web-standards.md).

## Where sources disagree

**Name and order.** RDF 1999 calls the unit a statement and, in its formal model, a triple with the predicate first; RDF 1.0 and 1.1 say triple, subject first [3][2][1]. The embedding paper read (Bordes et al.) writes triplet, as does a 2024 extraction paper; a 2025 one writes triples [6][9][8].

**The unit.** Wikidata's data model takes the Statement as its unit: a claim plus references, and a claim may carry extra snaks such as a date [7].

*Reading:* the shape is shared; the name, the order and the extras are not.

## Related

[RDF](./rdf.md), [RDF-star](./rdf-star.md), [triple store](./triple-store.md), [SPARQL](./sparql.md), [property graph](./property-graph.md), [knowledge graph](./knowledge-graph.md), [entity](./entity.md), [knowledge graph embedding](./knowledge-graph-embedding.md), [relation extraction](./relation-extraction.md). Data: [Wikidata](../datasets/wikidata.md). Benchmark: [Text2KGBench](../benchmarks/text2kgbench.md). Trend: [LLM graph construction](../trends/llm-kg-construction.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Semantic web standards: from RDF 1.1 and RDF-star to RDF 1.2](../trends/semantic-web-standards.md)

**Projects**

- [HippoRAG](../projects/hipporag.md)
- [Memori](../projects/memori.md)

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Datasets**

- [2WikiMultiHopQA](../datasets/2wikimultihopqa.md)
- [ConceptNet](../datasets/conceptnet.md)
- [FB15k-237](../datasets/fb15k-237.md)
- [MetaQA](../datasets/metaqa.md)
- [PopQA](../datasets/popqa.md)
- [SimpleQuestions](../datasets/simplequestions.md)
- [WN18RR](../datasets/wn18rr.md)
- [YAGO](../datasets/yago.md)

**Benchmarks**

- [Benchmarks](../benchmarks/README.md)
- [OGB link prediction](../benchmarks/ogb-link-prediction.md)
- [Text2KGBench](../benchmarks/text2kgbench.md)

**Index**

- [Entity](entity.md)
- [Hypergraph](hypergraph.md)
- [Knowledge graph completion](knowledge-graph-completion.md)
- [Link prediction](link-prediction.md)
- [RDF-star](rdf-star.md)
- [Relation extraction](relation-extraction.md)
- [Triple store](triple-store.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.w3.org/TR/rdf11-concepts/ : RDF 1.1 Concepts and Abstract Syntax, W3C Recommendation 25 February 2014: section 3.1 Triples, binary relation, RDF graph (read 20261102 22:06 UTC)
2. https://www.w3.org/TR/rdf10-concepts/ : RDF Concepts and Abstract Syntax, W3C Recommendation 10 February 2004: "collection of triples" (read 20261102 22:16 UTC)
3. https://www.w3.org/TR/1999/REC-rdf-syntax-19990222/ : RDF Model and Syntax Specification, W3C Recommendation 22 February 1999: statements; section 5, formal model {pred, sub, obj} (read 20261102 22:06 UTC)
4. https://www.w3.org/TR/rdf12-concepts/ : RDF 1.2 Concepts and Abstract Data Model, Candidate Recommendation Snapshot 7 April 2026: triple terms; latest Recommendation RDF 1.1 (read 20261102 22:06 UTC)
5. https://www.w3.org/standards/history/rdf12-concepts/ : W3C publication history of RDF 1.2 Concepts: newest entry 7 April 2026, Candidate Recommendation Snapshot (read 20261102 22:06 UTC)
6. https://papers.nips.cc/paper_files/paper/2013/file/1cecc7a77928ca8133fa24680a88d2f9-Paper.pdf : Bordes et al., "Translating Embeddings for Modeling Multi-relational Data", NIPS 2013, section 2: "triplets (h, l, t)" (read 20261102 22:15 UTC)
7. https://www.mediawiki.org/wiki/Wikibase/DataModel : Wikibase data model: Statement, claim, references, snaks (first-party; read 20261102 22:12 UTC)
8. https://arxiv.org/abs/2505.23628 : Bai et al. (20 authors), "AutoSchemaKG: Autonomous Knowledge Graph Construction through Dynamic Schema Induction from Web-Scale Corpora", first submitted 29 May 2025, v3 abstract: "knowledge triples", 900+ million nodes, 5.9 billion edges (first-party; read 20261102 22:16 UTC)
9. https://arxiv.org/abs/2404.03868 : Zhang and Soh, "Extract, Define, Canonicalize: An LLM-based Framework for Knowledge Graph Construction", first submitted 5 April 2024, abstract: "valid triplets" (read 20261102 22:16 UTC)
10. https://ar5iv.labs.arxiv.org/html/2003.02320 : Hogan et al., "Knowledge Graphs" (arXiv 2003.02320, ar5iv rendering; version shown unstated), section 2.1.1: directed edge-labelled graphs and binary relations (read 20261102 22:12 UTC)
