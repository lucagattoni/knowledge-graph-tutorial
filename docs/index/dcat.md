---
type: index
kind: standard
aliases: [Data Catalog Vocabulary]
updated: 20261102 21:25 UTC
---

# DCAT

DCAT, the Data Catalog Vocabulary, is the W3C standard way to describe datasets and data services in a catalogue using RDF. It is a vocabulary for metadata about data, not a format for the data itself. This entry follows the three W3C Recommendations of the vocabulary.

## Definition

The specification defines DCAT as "an RDF vocabulary designed to facilitate interoperability between data catalogs published on the Web" [1]. A publisher describes datasets and data services in a catalogue with one model, so metadata from several catalogues can be aggregated and searched together across sites [1]. Terms live in the namespace `http://www.w3.org/ns/dcat#`, with the suggested prefix `dcat` [1]. The current Recommendation is Version 3, dated 20240822 [1]. Turtle, RDF/XML and JSON-LD copies of the specification are non-normative [1]. A non-normative appendix aligns DCAT with schema.org [1].

## How it changed

- **20140116.** The first DCAT is a W3C Recommendation, edited by Fadi Maali and John Erickson; it was later marked superseded (on 20200204) [3]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20200204.** DCAT 2 becomes a Recommendation. It adds data services, time and space properties, qualified relations and packaging. It "supersedes" DCAT without making it obsolete, and keeps the namespace [2].
- **20240822.** DCAT 3 becomes a Recommendation and marks DCAT 2 superseded the same day [1][2]. New in it: versioning properties (`dcat:version`, `dcat:previousVersion`, `dcat:hasCurrentVersion`), a `dcat:DatasetSeries` class, guidance on inverse properties and an SPDX checksum [1]. Its terms keep DCAT 2 meanings, and existing DCAT 2 deployments need no change [1]. Era: [What has settled since 2023](../history/settled-since-2023.md).
- **As of the read (20261102).** The address `https://www.w3.org/TR/vocab-dcat/` serves the 20240822 Recommendation and names no successor [4]. It lists an editor's draft at `w3c.github.io/dxwg/dcat/` and a milestone "DCAT Future Priority Work" collecting issues "believed to be a priority for a future release" [4]; what they contain is unstated.

## Where sources disagree

No disagreement found in the sources read.

## Related

[RDF](./rdf.md), [linked data](./linked-data.md), [schema.org](./schema-org.md), [JSON-LD](./json-ld.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Index**

- [RDF Dataset Canonicalization](rdf-dataset-canonicalization.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.w3.org/TR/vocab-dcat-3/ : DCAT Version 3, W3C Recommendation 22 August 2024: abstract, namespace, status, main changes, backward compatibility, formats, appendix B (read 20261102 20:44 UTC)
2. https://www.w3.org/TR/vocab-dcat-2/ : DCAT Version 2, W3C Recommendation 04 February 2020, marked superseded 22 August 2024: note on supersession, new features (read 20261102 20:44 UTC)
3. https://www.w3.org/TR/vocab-dcat-1/ : DCAT, W3C Recommendation 16 January 2014, marked superseded 4 February 2020; editors (read 20261102 20:44 UTC)
4. https://www.w3.org/TR/vocab-dcat/ : the latest-version address of DCAT, serving Version 3 of 22 August 2024; editor's draft link and future-work milestone (read 20261102 21:22 UTC)
