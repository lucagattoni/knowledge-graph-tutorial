---
type: index
kind: standard
aliases: [Uniform Resource Identifier, Uniform Resource Locator, URL]
updated: 20261102 21:25 UTC
---

# URI

This entry says what a URI is, how its definition moved from a 1994 memo to the current Internet standard, and where RDF and linked data use it. It also records the dispute over the words "URI", "URL" and "IRI".

## Definition

RFC 3986 (STD 66, January 2005) opens: a URI is "a compact sequence of characters that identifies an abstract or physical resource" [1]. A resource is whatever a URI might identify: a document, a service, even a person or an abstract concept, whether or not it can be reached on the Internet [1]. A URI can be a locator, a name or both. A URL is the subset that also says how to locate the resource; a URN is a URI of the "urn" scheme, or any URI with the properties of a name [1]. RFC 3986 asks future documents to say "URI", not "URL" [1].

## How it changed

- **1990.** The Web's use of such identifiers "dates from 1990", say RFC 3986 and RFC 1738 [1][3].
- **199406.** RFC 1630, by Berners-Lee at CERN, expands the acronym as "Universal Resource Identifiers". It is informational and "does not specify an Internet standard of any kind" [2]. See [The Web changes data and search](../history/the-web.md).
- **199412.** RFC 1738 defines URLs on the standards track [3].
- **199808.** RFC 2396 gives one generic URI syntax, replacing the generic parts of RFC 1738 and RFC 1808 [4].
- **20040210.** RDF 1.0 builds triples from "RDF URI references" [7]. See [RDF](./rdf.md).
- **200501.** RFC 3986 obsoletes RFC 2396. The RFC Editor lists it as an Internet Standard, updated by RFC 7320 and RFC 8820 [1][5]. RFC 3987 adds IRIs, the same idea over Unicode characters [6]. See [The semantic web and linked data](../history/semantic-web.md).
- **20060727.** Berners-Lee's first linked-data rule: "Use URIs as names for things" [10]. See [linked data](./linked-data.md).
- **20140225.** RDF 1.1 uses IRIs, "a generalization of URIs" [8].
- **20260407, still moving.** The RDF 1.2 Candidate Recommendation Snapshot keeps IRIs per RFC 3987 and requires resolution per RFC 3986 [9]. See [the trends](../trends/README.md).

## Where sources disagree

**URI or URL?** RFC 3986 prefers "URI" [1]. The WHATWG URL Standard, a living standard last updated 20261019, aims to "obsolete the RFCs" and says "Standardize on the term URL. URI and IRI are just confusing." [11] RDF specifications keep to IRI [8][9].

## Related

[RDF](./rdf.md) · [linked data](./linked-data.md) · [semantic web](./semantic-web.md) · [JSON-LD](./json-ld.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [The semantic web and linked data](../history/semantic-web.md)

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Index**

- [JSON-LD](json-ld.md)
- [Language Server Protocol](language-server-protocol.md)
- [Linked data](linked-data.md)
- [RDF](rdf.md)
- [SPARQL](sparql.md)
- [Web search engine](web-search-engine.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.rfc-editor.org/rfc/rfc3986.txt : RFC 3986, STD 66, January 2005: abstract, section 1.1 (resource, URL, URN), "dates from 1990", obsoletes RFC 2396 (read 20261102 21:00 UTC)
2. https://www.rfc-editor.org/rfc/rfc1630.txt : RFC 1630, June 1994, "Universal Resource Identifiers in WWW", informational (read 20261102 21:00 UTC)
3. https://www.rfc-editor.org/rfc/rfc1738.txt : RFC 1738, December 1994, "Uniform Resource Locators (URL)", standards track, use "dates from 1990" (read 20261102 21:00 UTC)
4. https://www.rfc-editor.org/rfc/rfc2396.txt : RFC 2396, August 1998: abstract, "revises and replaces the generic definitions in RFC 1738 and RFC 1808" (read 20261102 21:00 UTC)
5. https://www.rfc-editor.org/info/rfc3986 : RFC Editor record: Internet Standard; "updated, see RFC 7320, RFC 8820" (read 20261102 21:03 UTC)
6. https://www.rfc-editor.org/rfc/rfc3987.txt : RFC 3987, January 2005, IRIs, abstract (read 20261102 21:00 UTC)
7. https://www.w3.org/TR/rdf10-concepts/ : RDF 1.0 Concepts, W3C Recommendation 20040210, section 6.1: triples of "RDF URI reference" (read 20261102 21:03 UTC)
8. https://www.w3.org/TR/rdf11-concepts/ : RDF 1.1 Concepts, W3C Recommendation 20140225: "IRIs are a generalization of URIs" (read 20261102 21:03 UTC)
9. https://www.w3.org/TR/rdf12-concepts/ : RDF 1.2 Concepts, Candidate Recommendation Snapshot 20260407, section 3.3 IRIs (read 20261102 21:03 UTC)
10. https://www.w3.org/DesignIssues/LinkedData.html : Berners-Lee, "Linked Data", design note dated 20060727: four rules (read 20261102 21:03 UTC)
11. https://url.spec.whatwg.org/ : WHATWG, URL Standard, Living Standard, last updated 19 October 2026: Goals (read 20261102 21:00 UTC)
