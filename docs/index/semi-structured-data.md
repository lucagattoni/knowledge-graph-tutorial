---
type: index
kind: concept
aliases: [semistructured data, self-describing data]
updated: 20261102 21:27 UTC
---

# Semi-structured data

This entry answers what semi-structured data means and why the idea appeared in the 1990s. It follows the term from two database papers of 1997 to XML and JSON. It also shows that the sources differ on its boundary and on how much it mattered.

## Definition

Abiteboul calls data semi-structured when it is, from a particular viewpoint, "neither raw data nor strictly typed": not table-oriented as in the [relational model](./relational-model.md), and not a sorted graph as in [object-oriented databases](./object-oriented-database.md) [1]. Buneman defines it by where the structure lives: the information normally tied to a schema is contained within the data, which is why it is sometimes called "self-describing". In some forms there is no separate schema; in others a schema exists but sets only loose constraints [2].

## How it changed

- **1997.** Abiteboul's paper at ICDT '97 (8-10 January 1997) surveys the topic [1][3]. Its motive is data integration across differing formats and the Web [1]. It says the topic "has no precise boundary" and that a theory is missing. It finds the labelled-graph models of Stanford and Penn very similar [1].
- **Undated in the copy read, written in 1997 or later (inference).** Buneman's tutorial paper calls Abiteboul's survey "recent", and its reference list runs to May 1997 ("in press"). It gives three motives: the Web, flexible data exchange, and browsing structured data as if it were not [2].
- **19980210.** [XML](./xml.md) 1.0 becomes a W3C Recommendation [4]. See [The Web changes data and search](../history/the-web.md).
- **Late 1990s and 2000s.** Stonebraker and Pavlo list "Semi-structured (e.g., XML)" as one of the data-model movements since the 1960s, and write that they predicted in 2005 that XML databases would not supplant relational systems [5].
- **2000s to 2024.** The same authors report that JSON "has since overtaken XML" for web data exchange. Key-value systems such as DynamoDB moved to JSON values, and document systems store JSON natively [5]. See [NoSQL](./nosql.md).
- **Later use.** Hogan et al. use the phrase for the data in Wikipedia articles from which [DBpedia](./dbpedia.md) builds a graph [6].

## Where sources disagree

**Name and boundary.** Buneman writes that the topic is "also called unstructured data" [2]; Abiteboul separates semi-structured data from raw data, and admits the boundary is vague [1]. Stonebraker and Pavlo tie the label to XML in the late 1990s but later apply it to JSON values [5].

**Did it matter for databases?** Stonebraker and Pavlo say XML databases did not supplant relational systems, and see document databases as repeating the object-oriented and XML pattern [5]. Abiteboul and Buneman present the data as a new object of study that conventional models do not fit [1][2]. None of the sources read weighs these views against each other.

## Related

[XML](./xml.md) · [JSON-LD](./json-ld.md) · [RDF](./rdf.md) · [relational model](./relational-model.md) · [NoSQL](./nosql.md) · [DBpedia](./dbpedia.md) · [knowledge graph](./knowledge-graph.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [The Web changes data and search](../history/the-web.md)

**Index**

- [NoSQL](nosql.md)
- [Object-oriented database](object-oriented-database.md)
- [XML](xml.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://ntrs.nasa.gov/api/citations/20050061322/downloads/20050061322.pdf : Abiteboul, "Querying Semi-Structured Data" (INRIA-Rocquencourt), a copy found through NASA NTRS and matched to the ICDT '97 paper by title via Hogan et al. reference [3] (source 3); the copy itself names no venue and gives its report date as 1997: definition, boundary, Stanford and Penn models (read 20261102 21:01 UTC, re-read 20261102 21:25 UTC; the proceedings version may differ)
2. https://homepages.inf.ed.ac.uk/opb/papers/PODS1997a.pdf : Buneman, "Semistructured Data" (tutorial paper): abstract and section 1; the copy read gives no venue or date, so both are **unstated** here; its reference list runs to May 1997 (read 20261102 21:01 UTC, re-read 20261102 21:25 UTC)
3. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", ACM Computing Surveys 54(4), reference list: Abiteboul 1997, ICDT '97, 8-10 January 1997 (read 20261102 20:58 UTC)
4. https://www.w3.org/TR/1998/REC-xml-19980210 : Extensible Markup Language (XML) 1.0, W3C Recommendation 10 February 1998 (read 20261102 21:01 UTC)
5. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, "What Goes Around Comes Around... And Around...", SIGMOD Record 53(2), 2024: introduction and the key-value and document sections (read 20261102 21:01 UTC)
6. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", section 10.1.1, DBpedia: "semi-structured data embedded in Wikipedia articles" (read 20261102 20:58 UTC)
