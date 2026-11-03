---
type: index
kind: concept
aliases: [schemas, schemata, database schema, graph schema]
updated: 20261102 22:51 UTC
---

# Schema

This entry answers what a schema is in a database and in a knowledge graph, which kinds a graph can have, and why "who writes it" became a question. Where a model derives the schema from text, see [schema induction](./schema-induction.md).

## Definition

A database textbook separates the logical schema, "the overall logical structure of the database", from the instance, the content at a given moment; the schema resembles the type information of a program variable [1]. For graphs, Hogan et al. note the option to "forgo or postpone the definition of a schema"; when one is used, it prescribes "a high-level structure and/or semantics that the graph follows or should follow" [2]. They name three kinds: a semantic schema (classes, properties, domains and ranges, used to infer), a validating schema (shapes and constraints, used to check) and an emergent schema (structure extracted from the graph itself, also called a graph summary) [2].

## How it changed

- The date the word entered database practice is unstated in the sources read.
- **2004; 20140225.** RDF Schema is "a data-modelling vocabulary for RDF data". Version 1.1, a W3C Recommendation of 25 February 2014, is an edited version of the 2004 Recommendation [3]. See [RDF Schema](./rdfs.md) and [The semantic web and linked data](../history/semantic-web.md).
- **20170720.** SHACL becomes a W3C Recommendation, "a language for validating RDF graphs against a set of conditions" [4]. See [SHACL](./shacl.md) and [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20240405.** Zhang and Soh say that earlier language-model methods put the schema in the prompt, which large schemas can overflow, and that sometimes no predefined schema exists; their method builds "a succinct self-generated schema" [5]. Still moving: [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

## Where sources disagree

**One word, two jobs.** In the textbook the schema is written in a data definition language and settled at the logical design step of building a database [1]. Hogan et al. set graphs against the relational model here: a graph may forgo or postpone the schema [2]. They also give its kinds different work: "semantic schemata allow for inferring new graph data, validating schemata allow for validating existing graph data" [2]. They tie semantic schemas to the open-world assumption and many classical databases to the [closed-world assumption](./closed-world-assumption.md) [2].

## Related

[Ontology](./ontology.md) · [RDF Schema](./rdfs.md) · [SHACL](./shacl.md) · [schema.org](./schema-org.md) · [taxonomy](./taxonomy.md) · [schema induction](./schema-induction.md) · [LinkML](./linkml.md) · [relational model](./relational-model.md) · [data independence](./data-independence.md) · [closed-world assumption](./closed-world-assumption.md) · [property graph](./property-graph.md) · [knowledge graph](./knowledge-graph.md). Projects: [OntoGPT](../projects/ontogpt.md), [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md). Dataset: [YAGO](../datasets/yago.md). Trend: [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)

**Projects**

- [GraphRAG SDK](../projects/graphrag-sdk.md)
- [HippoRAG](../projects/hipporag.md)
- [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md)

**Papers**

- [Papers: Building knowledge graphs with LLMs](../papers/llm-kg-construction.md)

**Datasets**

- [YAGO](../datasets/yago.md)

**Index**

- [Entity](entity.md)
- [LinkML](linkml.md)
- [Schema induction](schema-induction.md)
- [Taxonomy](taxonomy.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.db-book.com/slides-dir/PDF-dir/ch1.pdf : Silberschatz, Korth and Sudarshan, Database System Concepts 7th ed., chapter 1 slides: "Instances and Schemas", "Data Definition Language (DDL)", "Database Design" ("Logical Design - Deciding on the database schema") (read 20261102 22:09 UTC; the DDL and design slides read 20261102 22:50 UTC)
2. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", ACM Computing Surveys 54(4), 2021, arXiv v6 of 11 September 2021: section 3.1 and 3.1.1 to 3.1.3 (read 20261102 22:06 UTC)
3. https://www.w3.org/TR/rdf-schema/ : RDF Schema 1.1, W3C Recommendation 25 February 2014: abstract, status ("an edited version of the 2004 RDF Schema Recommendation") (read 20261102 22:09 UTC)
4. https://www.w3.org/TR/shacl/ : Shapes Constraint Language (SHACL), W3C Recommendation 20 July 2017: abstract (read 20261102 22:09 UTC)
5. https://arxiv.org/abs/2404.03868 : Zhang and Soh, "Extract, Define, Canonicalize" (EDC), v1 5 April 2024, EMNLP 2024: abstract (read 20261102 22:09 UTC)
