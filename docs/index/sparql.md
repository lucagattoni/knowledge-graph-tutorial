---
type: index
kind: standard
aliases: [SPARQL Query Language for RDF, SPARQL 1.1, SPARQL 1.2]
updated: 20261102 21:26 UTC
---

# SPARQL

SPARQL is the W3C query language for RDF data. This entry gives its definition, the Recommendations of 2008 and 2013, and the SPARQL 1.2 drafts that have run since 2023 without becoming a Recommendation.

## Definition

The W3C Recommendation of 20080115 "defines the syntax and semantics of the SPARQL query language for RDF" [1]. A query can run across data "stored natively as RDF or viewed as RDF via middleware"; it can ask for required and optional graph patterns, with conjunctions and disjunctions, and the results are either result sets or [RDF](./rdf.md) graphs [1]. The RDF Data Access Working Group produced it; Eric Prud'hommeaux and Andy Seaborne edited it [1]. In the survey of Hogan et al., SPARQL uses a homomorphism-based semantics for graph patterns, where Cypher uses an isomorphism-based one on edges [4].

## How it changed

- **20041012.** First Working Draft of the SPARQL Query Language for RDF [2].
- **20060526.** Pérez, Arenas and Gutierrez post a formal semantics of SPARQL's graph patterns, then a W3C candidate recommendation [3].
- **20080115.** SPARQL becomes a W3C Recommendation [1][2]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **20091022.** First Working Draft of SPARQL 1.1 [5].
- **20130321.** SPARQL 1.1 Query Language becomes a Recommendation, one of eleven of the SPARQL Working Group, beside Update, Federated Query and Protocol [5][6]. Its abstract names aggregation, subqueries, negation, creating values by expressions, extensible value testing and constraining queries by source graph [7]. A list of what is new since SPARQL 1.0 was not found on that page and is **unstated**. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20230516.** First Public Working Draft of SPARQL 1.2 Query [8].
- **20251216.** The first version of SPARQL-LLM, a system that generates SPARQL from natural-language questions; its v2 is dated 20260923 [10]. Still moving: [asking graphs in natural language](../trends/graph-query-generation.md).
- **20261101.** The 108th publication of that draft, the latest read, is a Working Draft, one of twelve SPARQL 1.2 documents; it adds functions on triple terms and names SPARQL 1.1 as the latest Recommendation [8][9]. Not settled: see [What has settled since 2023](../history/settled-since-2023.md).

## Where sources disagree

The dates agree across the W3C pages [1][2][6][8]. The wording changed: the 2008 and 2013 abstracts call RDF a "graph data format"; the 2026 draft calls it a "graph data model" [1][7][9]. The 2026 draft names two Working Groups as its publisher [9]. When SPARQL 1.2 becomes a Recommendation is **unstated**.

## Related

[RDF](./rdf.md), [SHACL](./shacl.md), [OWL](./owl.md), [linked data](./linked-data.md), [semantic web](./semantic-web.md), [URI](./uri.md), [SQL](./sql.md), [Cypher](./cypher.md), [GQL](./gql.md), [large language model](./large-language-model.md). Pages: [asking graphs in natural language](../trends/graph-query-generation.md), its [papers](../papers/graph-query-generation.md), the benchmark [LC-QuAD](../benchmarks/lc-quad.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [The semantic web and linked data](../history/semantic-web.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Trends**

- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)
- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)
- [Trends: what the field is doing now](../trends/README.md)

**Papers**

- [Papers: Asking graphs in natural language](../papers/graph-query-generation.md)

**Datasets**

- [ComplexWebQuestions](../datasets/complexwebquestions.md)
- [Datasets](../datasets/README.md)
- [DBpedia](../datasets/dbpedia.md)
- [GrailQA](../datasets/grailqa.md)
- [LC-QuAD](../datasets/lc-quad.md)
- [WebQuestionsSP](../datasets/webquestionssp.md)

**Benchmarks**

- [Benchmarks](../benchmarks/README.md)
- [LC-QuAD](../benchmarks/lc-quad.md)

**Index**

- [Cypher](cypher.md)
- [DBpedia](dbpedia.md)
- [Knowledge-base question answering](knowledge-base-question-answering.md)
- [Linked data](linked-data.md)
- [OWL](owl.md)
- [RDF](rdf.md)
- [RDF Dataset Canonicalization](rdf-dataset-canonicalization.md)
- [RDF Schema](rdfs.md)
- [RDF-star](rdf-star.md)
- [Semantic parsing](semantic-parsing.md)
- [Semantic Web](semantic-web.md)
- [SHACL](shacl.md)
- [SQL](sql.md)
- [SQL/PGQ](sql-pgq.md)
- [Text-to-query](text-to-query.md)
- [Triple](triple.md)
- [Triple store](triple-store.md)
- [Wikidata](wikidata.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.w3.org/TR/rdf-sparql-query/ : SPARQL Query Language for RDF, W3C Recommendation 15 January 2008: abstract, editors, Data Access Working Group (read 20261102 20:57 UTC)
2. https://www.w3.org/standards/history/rdf-sparql-query/ : publication history: first Working Draft 12 October 2004, Recommendation 15 January 2008 (read 20261102 20:58 UTC)
3. https://arxiv.org/abs/cs/0605124 : Pérez, Arenas, Gutierrez, "Semantics and Complexity of SPARQL", submitted 26 May 2006; abstract (read 20261102 20:59 UTC)
4. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", ACM Computing Surveys 2021, section on querying: homomorphism-based and isomorphism-based semantics (read 20261102 20:59 UTC)
5. https://www.w3.org/TR/sparql11-overview/ : SPARQL 1.1 Overview: the set of eleven Recommendations (read 20261102 20:58 UTC)
6. https://www.w3.org/standards/history/sparql11-query/ : publication history of SPARQL 1.1 Query: first Working Draft 22 October 2009, Recommendation 21 March 2013 (read 20261102 20:58 UTC)
7. https://www.w3.org/TR/sparql11-query/ : SPARQL 1.1 Query Language, Recommendation 21 March 2013: abstract; the page has no section on changes since SPARQL 1.0 (read 20261102 20:57 UTC; abstract re-read 20261102 21:25 UTC)
8. https://www.w3.org/standards/history/sparql12-query/ : publication history of SPARQL 1.2 Query: First Public Working Draft 16 May 2023, 108 publications to 1 November 2026 (read 20261102 20:58 UTC)
9. https://www.w3.org/TR/sparql12-query/ : SPARQL 1.2 Query Language, Working Draft 1 November 2026: abstract, status, set of twelve documents, functions on triple terms, latest Recommendation (read 20261102 20:57 UTC)
10. https://arxiv.org/abs/2512.14277 : SPARQL-LLM, submitted 16 Dec 2025, v2 of 23 Sep 2026; abstract (read 20261102 21:06 UTC)
