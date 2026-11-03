---
type: index
kind: standard
aliases: [RDF*, RDF-star and SPARQL-star, quoted triples, triple terms]
updated: 20261102 22:50 UTC
---

# RDF-star

This entry answers what RDF-star is, why it was proposed, and how it turned into the triple terms of RDF 1.2. The name belongs to a 2021 community specification; the W3C standard that followed uses other words and other rules.

## Definition

RDF-star extends RDF "with a convenient way to make statements about other statements" [1]. A triple may be the subject or object of another triple; this nested triple is a quoted triple, and it is not asserted unless the graph also states it [1]. The report offers this as a compact alternative to standard RDF reification [1], which needs four extra triples to describe one statement [2]. Turtle-star and SPARQL-star extend the syntaxes and the query language [1]. The report says it is not a W3C Standard and not on the Standards Track [1].

## How it changed

- **19990222.** The first RDF Recommendation already has reification, a statement modelled as a resource with four properties, in a form it calls "rather verbose" [3]. See [The Web changes data and search](../history/the-web.md).
- **2014-2017.** Hartig and Thompson (arXiv, 20140613) propose a backwards-compatible alternative to reification [4]. Hartig's workshop paper (AMW, June 2017) names it RDF\* and SPARQL\*, and lists provenance among the uses of statement-level metadata [1][2]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20211217.** The RDF-DEV Community Group issues the Final Community Group Report "RDF-star and SPARQL-star" [1]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20220829.** The first charter of the W3C working group for statements about statements in RDF and SPARQL begins; its page is titled "RDF & SPARQL" (shortname rdf-star) and its current charter runs to 20270430 [5].
- **20260407.** RDF 1.2 Concepts is a Candidate Recommendation Snapshot (first public working draft 20230516) that adds triple terms, reifiers and the property rdf:reifies. The history read on 20261102 shows no later step [6][7]. See [RDF](./rdf.md).
- **20230928 and 20261101.** The SPARQL 1.2 Query working draft of 20230928 already has TRIPLE and isTRIPLE, under the heading "Functions on Quoted Triples"; the draft of 20261101 has them under "Functions on Triple Terms" [10][8]. See [SPARQL](./sparql.md).
- **Read 20261102.** YAGO's documentation says it uses "the RDF\* format" for facts about facts [9].

## Where sources disagree

**Where the nested triple may sit.** The 2021 report allows subject or object [1]. RDF 1.2 says "An RDF triple used as the object of another triple is called a triple term": object only [6].

**Opaque or transparent.** The report says quoted triples are referentially opaque [1]; RDF 1.2 says triple terms are transparent [6].

**Name.** RDF 1.2 Concepts uses "RDF-star" only in its feedback address; it speaks of triple terms, reifiers and reifying triples [6]. *Reading:* RDF-star names the 2021 design, and RDF 1.2 is a successor with different rules. Which tools support which is unstated in the sources read.

## Related

[RDF](./rdf.md) · [SPARQL](./sparql.md) · [triple](./triple.md) · [triple store](./triple-store.md) · [property graph](./property-graph.md) · [provenance](./provenance.md) · [RDF Dataset Canonicalization](./rdf-dataset-canonicalization.md). Data: [YAGO](../datasets/yago.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Datasets**

- [YAGO](../datasets/yago.md)

**Index**

- [Hypergraph](hypergraph.md)
- [Provenance](provenance.md)
- [Triple](triple.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://w3c-cg.github.io/rdf-star/cg-spec/2021-12-17.html : RDF-star and SPARQL-star, Final Community Group Report 20211217, RDF-DEV Community Group: abstract, status section (not a W3C Standard), sections 1.1 to 1.3 (reification, overview, quoted and asserted triples, referential opacity), reference list (Hartig, AMW, June 2017); the editor's draft at https://w3c.github.io/rdf-star/cg-spec/editors_draft.html has the same abstract and overview (read 20261102 22:15 UTC and 22:07 UTC)
2. http://ceur-ws.org/Vol-1912/paper12.pdf : Hartig, "Foundations of RDF\* and SPARQL\*", AMW 2017 (CEUR Vol. 1912): abstract, introduction (reification needs four extra triples; uses of statement-level metadata) (read 20261102 22:15 UTC)
3. https://www.w3.org/TR/1999/REC-rdf-syntax-19990222/ : RDF Model and Syntax Specification, W3C Recommendation 19990222: section 4, reification, "rather verbose" (read 20261102 22:15 UTC)
4. https://arxiv.org/abs/1406.3399 : Hartig and Thompson, "Foundations of an Alternative Approach to Reification in RDF", v1 20140613, v3 20211216, abstract (read 20261102 22:15 UTC)
5. https://www.w3.org/groups/wg/rdf-star/ and https://www.w3.org/groups/wg/rdf-star/charters/ : W3C RDF & SPARQL Working Group page: mission, shortname rdf-star, charters 20220829 to 20240828 (extended to 20250430) and 20250501 to 20270430 (read 20261102 22:13 UTC and 22:14 UTC)
6. https://www.w3.org/TR/rdf12-concepts/ : RDF 1.2 Concepts and Abstract Data Model, Candidate Recommendation Snapshot 20260407: sections 1.5 and 3.6, appendix of changes, status, feedback address (read 20261102 22:07 UTC)
7. https://www.w3.org/standards/history/rdf12-concepts/ : publication history of RDF 1.2 Concepts: first public working draft 20230516, newest entry the 20260407 snapshot (read 20261102 22:07 UTC)
8. https://www.w3.org/TR/sparql12-query/ : SPARQL 1.2 Query Language, Working Draft 20261101: section 17.4.6, functions on triple terms (read 20261102 22:19 UTC)
9. https://yago-knowledge.org/getting-started : YAGO, "Getting started": facts about facts use the RDF\* format (first-party; read 20261102 22:16 UTC)
10. https://www.w3.org/TR/2023/WD-sparql12-query-20230928/ : SPARQL 1.2 Query Language, Working Draft 28 September 2023: section 17.4.6 "Functions on Quoted Triples", TRIPLE and isTRIPLE (read 20261102 22:49 UTC)
