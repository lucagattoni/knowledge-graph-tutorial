---
type: index
kind: concept
aliases: [LOD, Linked Open Data]
updated: 20261102 21:32 UTC
---

# Linked data

This entry says what linked data is, how its rules and its size changed, and where sources draw its edge differently.

## Definition

Linked data is data published on the web so that a person or a program can follow links from one thing to related things. Berners-Lee's design note, dated 20060727, says the Semantic Web "is about making links, so that a person or machine can explore the web of data". It gives four rules: use [URIs](./uri.md) as names for things; use HTTP URIs so people can look the names up; when someone looks a URI up, provide useful information; include links to other URIs. The note calls them "expectations of behavior" and itself a "personal view only" [1]. In the version last changed 20090618, the third rule adds "using the standards (RDF*, SPARQL)"; a copy archived on 20070107 (last change 20061025) has the third rule without that clause [1][5]. The wording above is therefore the 2006 one, and the clause is a later addition.

## How it changed

- **20060727.** The note is dated. Hitzler dates the "birth" of Linked Data to 2006 and its phase into the early 2010s [2]. See [the semantic web and linked data](../history/semantic-web.md).
- **20070107 to 20090618.** The standards clause appears in the third rule between the archived copy and the version read, which lists 20090618 as its last change. The date of that edit is **unstated** in the sources read [1][5].
- **2007 to 2017.** The Linking Open Data cloud diagram counted 12 datasets on 20070501, 295 on 20110919, 570 on 20140830 and 1,146 on 20170126 [3]. [DBpedia](./dbpedia.md) became a hub [2].
- **2010.** The note gains a five-star scheme, marked "Added 2010": one star for data on the web with an open licence, up to five for data linked to other people's data. It adds that linked data "does not of course in general have to be open" [1].
- **Early 2010s.** Hitzler: the hype "began to give way to a more sober perspective" [2]. See [knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20150226.** The Linked Data Platform 1.0 becomes a W3C Recommendation, for read-write linked data over HTTP [4].
- **20260615.** The newest diagram lists 1,360 datasets [3].

## Where sources disagree

The sources differ on what counts. The note treats its rules as expectations and linked data as not necessarily open [1]. Hitzler describes linked data as a large set of linked [RDF](./rdf.md) graphs and says the cloud omits many RDF sets [2]. The diagram's site lists today's submission rules: URIs that resolve to RDF, at least 1000 triples, and at least 50 RDF links to a dataset already in the diagram [3]. The page does not say whether these rules were applied to the older counts.

*Reading:* the counts therefore measure one reading of the rules, as they stand on the site, not all linked data.

## Related

- Entries: [URI](./uri.md), [RDF](./rdf.md), [SPARQL](./sparql.md), [semantic web](./semantic-web.md), [ontology](./ontology.md), [JSON-LD](./json-ld.md), [schema.org](./schema-org.md), [knowledge graph](./knowledge-graph.md), [DBpedia](./dbpedia.md), [Wikidata](./wikidata.md), [YAGO](./yago.md), [Freebase](./freebase.md).
- Content, size and licence of the big sets: [DBpedia](../datasets/dbpedia.md), [Wikidata](../datasets/wikidata.md), [YAGO](../datasets/yago.md), [Freebase](../datasets/freebase.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [Language models meet retrieval (2018-2022)](../history/language-models-meet-retrieval.md)
- [The semantic web and linked data](../history/semantic-web.md)

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Datasets**

- [Datasets](../datasets/README.md)
- [DBpedia](../datasets/dbpedia.md)

**Index**

- [DBpedia](dbpedia.md)
- [DCAT](dcat.md)
- [JSON-LD](json-ld.md)
- [Ontology](ontology.md)
- [OWL](owl.md)
- [RDF](rdf.md)
- [RDF Dataset Canonicalization](rdf-dataset-canonicalization.md)
- [RDF Schema](rdfs.md)
- [schema.org](schema-org.md)
- [Semantic Web](semantic-web.md)
- [SHACL](shacl.md)
- [SPARQL](sparql.md)
- [Triple store](triple-store.md)
- [URI](uri.md)
- [Wikidata](wikidata.md)

<!-- END GENERATED: appears-in -->

## Sources

Read times are UTC.

1. https://www.w3.org/DesignIssues/LinkedData.html : Berners-Lee, "Linked Data", design note; header "Date: 2006-07-27, last change: 2009/06/18"; four rules with the standards clause; five-star scheme ("Added 2010"); openness (read 20261102 20:45 and 21:23)
2. https://par.nsf.gov/servlets/purl/10292869 : Hitzler, "A Review of the Semantic Web Field", CACM 64(2), 2021, author version, Section 2.2 (read 20261102 20:45)
3. https://lod-cloud.net/ : home of the LOD cloud diagram; the submission rules under "Contributing to the Diagram" (current rules, no history given); history table of dataset counts (read 20261102 20:47 and 21:23)
4. https://www.w3.org/TR/ldp/ : Linked Data Platform 1.0, W3C Recommendation 26 February 2015 (read 20261102 20:45)
5. https://web.archive.org/web/20070107101821/http://www.w3.org:80/DesignIssues/LinkedData.html : archived copy of the same note, header "last change: 2006/10/25"; third rule without the standards clause; no star scheme in that copy (read 20261102 21:24)
