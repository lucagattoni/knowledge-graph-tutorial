---
type: index
kind: standard
aliases: [JSON-LD 1.1]
updated: 20261102 21:22 UTC
---

# JSON-LD

This entry says what JSON-LD is, which W3C Recommendation is current, and where it is used. It is the way [linked data](./linked-data.md) is written in ordinary JSON.

## Definition

JSON-LD is "a lightweight syntax to serialize Linked Data in JSON", in the words of the W3C Recommendation JSON-LD 1.1, "A JSON-based Serialization for Linked Data" [1]. A JSON-LD document is always a valid JSON document, so existing JSON parsers can read it [2]. Its data model is the model of [RDF](./rdf.md): the specification calls a document a serialization of an RDF dataset and says it can be used as RDF alongside other Linked Data technologies [2].

## How it changed

- **20140116.** JSON-LD 1.0 becomes a W3C Recommendation [3]. See [knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20200716.** JSON-LD 1.1 becomes a W3C Recommendation, published by the JSON-LD Working Group. It is meant to supersede 1.0 [1]. See [language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20201103.** The 1.0 Recommendation is marked superseded, and the notice recommends 1.1 for new adoption [3].
- **2026 (read 20261102).** Google lists JSON-LD, Microdata and RDFa as supported structured-data formats and says all three are equally fine for Google. It recommends the format easiest to implement and maintain, which "in most cases" is JSON-LD [4]. The W3C JSON-LD Working Group is chartered until 20280131 to maintain the JSON-LD 1.1 family; its page mentions no JSON-LD 1.2 draft or new charter [5].

## Where sources disagree

No disagreement found in the sources read.

## Related

[RDF](./rdf.md), [linked data](./linked-data.md), [schema.org](./schema-org.md), [semantic web](./semantic-web.md), [URI](./uri.md), [RDF Dataset Canonicalization](./rdf-dataset-canonicalization.md), [SHACL](./shacl.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [Language models meet retrieval (2018-2022)](../history/language-models-meet-retrieval.md)

**Index**

- [DCAT](dcat.md)
- [Linked data](linked-data.md)
- [LinkML](linkml.md)
- [RDF](rdf.md)
- [RDF Dataset Canonicalization](rdf-dataset-canonicalization.md)
- [schema.org](schema-org.md)
- [Semantic Web](semantic-web.md)
- [Semi-structured data](semi-structured-data.md)
- [URI](uri.md)
- [XML](xml.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.w3.org/TR/json-ld11/ : JSON-LD 1.1, W3C Recommendation 16 July 2020: definition, status, intent to supersede 1.0, JSON-LD Working Group (read 20261102 20:52 UTC)
2. https://www.w3.org/TR/json-ld11/ : same specification, section 1.5 (compatibility with JSON) and the introduction on RDF and the RDF data model (read 20261102 20:53 UTC)
3. https://www.w3.org/TR/2014/REC-json-ld-20140116/ : JSON-LD 1.0, W3C Recommendation 16 January 2014, marked superseded on 03 November 2020 by JSON-LD 1.1 (read 20261102 20:52 UTC)
4. https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data : Google Search Central, introduction to structured data; the page shows no date (read 20261102 20:53 UTC, re-read 20261102 21:22 UTC)
5. https://www.w3.org/groups/wg/json-ld/ : W3C JSON-LD Working Group page: mission, charter end 31 January 2028, chairs (read 20261102 20:52 UTC)
