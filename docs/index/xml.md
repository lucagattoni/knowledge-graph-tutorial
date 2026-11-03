---
type: index
kind: standard
aliases: [Extensible Markup Language]
updated: 20261102 21:09 UTC
---

# XML

XML is the W3C text format for self-describing, nested data. This entry gives the definition from the specification and the dated editions; it also says where XML sits among data formats.

## Definition

The specification opens: "The Extensible Markup Language (XML) is a subset of SGML that is completely described in this document." Its goal is "to enable generic SGML to be served, received, and processed on the Web" [1]. Its ten design goals include use over the Internet, compatibility with SGML, programs that are easy to write, and documents people can read without great difficulty [1]. Stonebraker and Pavlo list XML as an example of [semi-structured data](./semi-structured-data.md) [5].

## How it changed

- **1996.** The XML Working Group, first called the SGML Editorial Review Board, is formed under the W3C and chaired by Jon Bosak [1]. A Working Draft is dated 19961114, the earliest row of the publication history [2].
- **19980210.** XML 1.0 becomes a W3C Recommendation, edited by Bray, Paoli and Sperberg-McQueen [3]. Era: [The Web changes data and search](../history/the-web.md).
- **Later editions of 1.0.** Recommendations follow on 20001006, 20040204, 20060816 (fourth edition) and 20081126 (fifth edition) [1][2]. The fifth edition "is not a new version of XML" and gathers errata [1].
- **20040204 and 20060816.** XML 1.1 appears and gets a second edition. It is a separate version because its changes affect which documents are well-formed; XML 1.0 processors must keep rejecting documents that use 1.1 features [4].
- **Late 1990s and 2000s.** Stonebraker and Pavlo write that XML databases had "buzz" in the late 1990s and did not displace relational systems, and that JSON "has since overtaken XML" for web data exchange [5].
- **Today.** The W3C's latest-version page is still the fifth edition of 20081126, and its status section names no later edition [1][2].

## Where sources disagree

No disagreement found in the sources read.

## Related

Entries: [semi-structured data](./semi-structured-data.md), [RDF](./rdf.md), [JSON-LD](./json-ld.md), [semantic web](./semantic-web.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [The Web changes data and search](../history/the-web.md)

**Index**

- [Semi-structured data](semi-structured-data.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.w3.org/TR/xml/ : XML 1.0 (Fifth Edition), Recommendation of 20081126: abstract, goals, 1996 working group, status, editions (first-party; read 20261102 21:01 UTC)
2. https://www.w3.org/standards/history/xml/ : publication history of XML 1.0, 19961114 to 20081126 (first-party; read 20261102 21:02 UTC)
3. https://www.w3.org/TR/1998/REC-xml-19980210 : XML 1.0 Recommendation of 19980210, editors (first-party; read 20261102 21:01 UTC)
4. https://www.w3.org/TR/2006/REC-xml11-20060816 : XML 1.1 (Second Edition), first edition dated 20040204 (first-party; read 20261102 21:02 UTC)
5. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), 2024: XML databases, JSON (read 20261102 21:08 UTC)
