---
type: index
kind: concept
aliases: [entities, real-world entity]
updated: 20261102 22:53 UTC
---

# Entity

This entry says what an entity is in a knowledge graph and where sources draw the line between a node, a thing and a record. It is the base term for linking and extraction.

## Definition

Hogan et al. define a knowledge graph as a graph whose nodes "represent entities of interest" and whose edges represent relations between them [1]. In their formal reading, a node of the data graph is mapped to an entity of a domain graph, so a node names an entity and is not the entity [1]. Wikidata gives an operational definition: an entity is the content of a Wikidata page in a data namespace (for example an item, a property or a lexeme) and has a unique ID [2]. RDF 1.1 says a resource, which may be a physical thing, a document, an abstract concept, a number or a string, is synonymous with "entity" as RDF Semantics uses the word [3].

## How it changed

- **197603.** Chen's entity-relationship model, published in *ACM Transactions on Database Systems*, makes entity and relationship its basic concepts. Chen's 2002 account separates entities from entity types and calls the concepts of entity and relationship "very fundamental" [4]. See [Entity-relationship model](./entity-relationship-model.md). Era: [Formal foundations](../history/formal-foundations.md).
- **20120516.** Google's launch post says its Knowledge Graph "understands real-world entities and their relationships": things, not strings. It counts more than 500 million objects and 3.5 billion facts (first-party) [5]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20140225.** The RDF 1.1 Concepts Recommendation states the resource-entity equivalence [3].
- **20240424.** The GraphRAG paper has a language model extract entities, each with a short description, from text chunks. Its default prompt takes the broad class of "named entities", and its analysis reconciles names by exact string matching (first-party) [6]. See [Graph-based RAG](../trends/graph-based-rag.md).
- **20260826 and 20260930 (last-edit dates).** The Wikidata glossary lists items, properties and lexemes, among other kinds, as entities; the Wikibase data model page counts items and properties [2][7].

## Where sources disagree

**Node or thing.** Hogan et al. keep nodes and entities apart [1]. Wikidata equates the entity with a page's content and ID [2]. RDF gives each IRI a referent, the resource [3].

**What counts.** RDF counts numbers and strings as resources [3]. The Wikibase data model says "All Entities are Values", but numbers, strings and coordinates are not entities, while properties are [7]. In Hogan et al., relations are edges, not entities [1].

## Related

[Knowledge graph](./knowledge-graph.md), [triple](./triple.md), [property graph](./property-graph.md), [RDF](./rdf.md), [Wikidata](./wikidata.md), [ontology](./ontology.md), [schema](./schema.md), [entity linking](./entity-linking.md), [named-entity recognition](./named-entity-recognition.md), [knowledge graph embedding](./knowledge-graph-embedding.md). Data: [Wikidata](../datasets/wikidata.md). Project: [Microsoft GraphRAG](../projects/microsoft-graphrag.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Projects**

- [Neo4j LLM Knowledge Graph Builder](../projects/llm-graph-builder.md)
- [RAG-Anything](../projects/rag-anything.md)

**Index**

- [Entity linking](entity-linking.md)
- [Hypergraph](hypergraph.md)
- [Triple](triple.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", ACM Computing Surveys 54(4), 2021 (arXiv v6 of 11 September 2021): introduction (definition); section 2.1.1 (nodes represent entities); section 4.1.1 (data graph, domain graph, interpretation) (read 20261102 22:08 UTC)
2. https://www.wikidata.org/wiki/Wikidata:Glossary : Wikidata glossary, "Entity" ("such as an item, property or lexeme"; forms, senses and MediaInfo are also called entities) (page last edited 26 August 2026) (read 20261102 22:51 UTC)
3. https://www.w3.org/TR/rdf11-concepts/ : RDF 1.1 Concepts and Abstract Syntax, W3C Recommendation 25 February 2014, section 1.2, "Resources and Statements" (read 20261102 22:14 UTC)
4. http://bit.csc.lsu.edu/~chen/pdf/Chen_Pioneers.pdf : Chen, "Entity-Relationship Modeling: Historical Events, Future Trends, and Lessons Learned", Software Pioneers, Springer, 2002 (author's copy; first-party): section 2.3 (March 1976 publication), section 2.4 (entities and types), conclusions ("the concepts of entity and relationship are very fundamental"); book details (Software Pioneers, Springer, 2002) from the Crossref record https://api.crossref.org/works/10.1007/978-3-642-59412-0_17 (read 20261102 22:51 UTC)
5. https://blog.google/products/search/introducing-knowledge-graph-things-not/ : Singhal, Google, 16 May 2012 (first-party): "real-world entities", 500 million objects, 3.5 billion facts (read 20261102 22:18 UTC)
6. https://arxiv.org/pdf/2404.16130 : Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization", arXiv v1 of 20240424 (date from the arXiv API record): section 3.1.2 and 3.1.3, entity extraction and exact string matching (first-party; read 20261102 22:15 UTC)
7. https://www.mediawiki.org/wiki/Wikibase/DataModel : Wikibase data model, "Values" and "Items" sections (page last edited 30 September 2026) (read 20261102 22:07 UTC)
