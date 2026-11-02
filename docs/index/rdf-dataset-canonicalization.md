---
type: index
kind: standard
aliases: [RDFC-1.0, RDF canonicalization]
updated: 20261102 21:25 UTC
---

# RDF Dataset Canonicalization

This entry answers what the W3C's RDF Dataset Canonicalization standard does and why equal RDF data needs it. It gives the dates of each publication step and says where the standard stands.

## Definition

RDF Dataset Canonicalization, subtitled "A Standard RDF Dataset Canonicalization Algorithm", is a W3C Recommendation of 20240521 [1][2]. Its abstract says it is sometimes necessary to compare sets of graphs and to sign them digitally, and that the document "outlines an algorithm for normalizing RDF datasets" for these operations [1]. The algorithm is called RDFC-1.0 and "will assign deterministic identifiers to any blank nodes in the input dataset", so one dataset yields a single canonical serialisation [1]. The specification lists three uses: telling whether two serialisations are isomorphic, signing graphs independently of serialisation, and finding differences between graphs. It does not define the signature itself [1]. By default it uses SHA-256 [1]. It rests on the dataset definition of RDF 1.1 [1]; see [RDF](./rdf.md).

## How it changed

- **20221124.** First Public Working Draft [2].
- **20231031.** Candidate Recommendation Snapshot [2].
- **20240326.** Proposed Recommendation [2].
- **20240521.** Recommendation, from the RDF Dataset Canonicalization and Hash Working Group. The algorithm was input from the W3C Credentials Community Group, and an appendix compares RDFC-1.0 with the earlier version that group published (URDNA2015) [1][2]. See [What has settled since 2023](../history/settled-since-2023.md).
- **State on 20261102.** The Recommendation page says "Errata exists" and points to a GitHub-hosted errata page, which listed no entry when read [1][3]. The working group is active and its charter runs to 20261218 [4].
- **As published in 20240521.** The status section says work on an updated specification was ongoing in the W3C RDF-star Working Group [1]. The RDF 1.2 Schema page, read on 20261102, names the "RDF & SPARQL Working Group" as producer of the RDF 1.2 documents [5]. The current state of an updated canonicalization specification is **unstated** in the pages read.

## Where sources disagree

**Errata.** The Recommendation page says errata exist [1]; the errata page it links lists none and shows empty counters [3]. The sources read do not explain the difference. The date of the Community Group's earlier report is **unstated** in the pages read.

## Related

[RDF](./rdf.md) · [RDF Schema](./rdfs.md) · [JSON-LD](./json-ld.md) · [SHACL](./shacl.md) · [SPARQL](./sparql.md) · [linked data](./linked-data.md) · [DCAT](./dcat.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Index**

- [JSON-LD](json-ld.md)
- [RDF](rdf.md)
- [RDF-star](rdf-star.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.w3.org/TR/rdf-canon/ : RDF Dataset Canonicalization, W3C Recommendation 20240521: abstract, RDFC-1.0, blank-node identifiers, SHA-256 default, uses, RDF 1.1 dependency, RDF-star note in the status section (as published), Credentials Community Group origin, "Errata exists" (read 20261102 20:55 UTC; quotes and status section re-read 20261102 21:21 UTC)
2. https://www.w3.org/standards/history/rdf-canon/ : W3C publication history: First Public Working Draft 20221124, Candidate Recommendation Snapshot 20231031, Proposed Recommendation 20240326, Recommendation 20240521 (read 20261102 20:55 UTC)
3. https://w3c.github.io/rdf-canon/errata/ : errata page of the specification: no entries, "Latest Publication Date" 20240521 (read 20261102 20:57 UTC)
4. https://www.w3.org/groups/wg/rch/ : RDF Dataset Canonicalization and Hash Working Group: active, charter until 20261218 (read 20261102 20:57 UTC)
5. https://www.w3.org/TR/rdf12-schema/ : RDF 1.2 Schema, Working Draft 20261023: "one of eleven RDF 1.2 and twelve SPARQL 1.2 documents produced by the RDF & SPARQL Working Group" (read 20261102 21:21 UTC)
