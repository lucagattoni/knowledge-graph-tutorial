---
type: index
kind: concept
aliases: []
updated: 20261102 21:31 UTC
---

# Ontology

In computing, an ontology is a written-down agreement on the concepts of a domain and how they relate, so that programs and people use the same terms in the same way. This entry gives a much-cited definition, how later sources reworded it, and the dated steps from hand-built ontologies to ones induced by language models.

## Definition

Gruber's 1993 paper in *Knowledge Acquisition* says: "An ontology is an explicit specification of a conceptualization" [1]. He borrows the word from philosophy, "a systematic account of Existence" [1]. Hogan et al. give the computing sense as "a concrete, formal representation of what terms mean within the scope in which they are used", and say its usefulness depends on how widely it is agreed [3].

## How it changed

- **1993.** Gruber's paper (report of September 1992, published 1993) gives the definition quoted above and presents Ontolingua, which translates shared definitions into frame-based and relational systems [1]. Hitzler calls it "a many-cited source from 1993" [4]. When the term was first used in computing: unstated in the sources read. Era: [The Web changes data and search](../history/the-web.md).
- **2000 to 2006.** The DARPA Agent Markup Language programme and the EU project On-To-Knowledge (which yields OIL) merge and lead to [OWL](./owl.md) [4].
- **20040210.** OWL becomes a W3C Recommendation, a revision of DAML+OIL [5]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **Mid-2000s.** Hitzler: over-hyped expectations gave way to a sober view; ontologies "turned out to be often hard to maintain and re-use" [4].
- **Early 2010s.** Hitzler writes, hedged with "Arguably", that "shallow non-expressive schemas" in linked data appeared to be a major obstacle to reuse [4]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **20250529.** AutoSchemaKG is posted: language models extract triples and induce schemas from text with no predefined schema. The authors report 92% semantic alignment with human-crafted schemas (first-party; figure from version 3 of 20250801, the first version not read) [6]. Still moving: see [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

## Where sources disagree

The definition. Gruber 1993 has "explicit specification of a conceptualization" [1]. Hitzler writes that an ontology is a "formal, explicit specification of a shared conceptualization" and cites Gruber 1993 for it [4]. The 1993 paper's sentence has neither "formal" nor "shared"; "shared conceptualization" appears in Gruber's later paper on design criteria [2]. Where the full wording first appears: unstated in the sources read. Hitzler also calls it "rather generic" [4].

## Related

[OWL](./owl.md), [RDF Schema](./rdfs.md), [description logic](./description-logic.md), [semantic web](./semantic-web.md), [linked data](./linked-data.md), [knowledge base](./knowledge-base.md), [knowledge graph](./knowledge-graph.md), [schema.org](./schema-org.md), [SHACL](./shacl.md); the project [OntoGPT](../projects/ontogpt.md); the trend [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md); the [foundational papers](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [The advent: machines that hold knowledge](../history/advent.md)
- [The semantic web and linked data](../history/semantic-web.md)
- [The Web changes data and search](../history/the-web.md)

**Trends**

- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)

**Projects**

- [Cognee](../projects/cognee.md)
- [GraphRAG SDK](../projects/graphrag-sdk.md)
- [OntoGPT](../projects/ontogpt.md)
- [Semantica](../projects/semantica.md)

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Datasets**

- [DBpedia](../datasets/dbpedia.md)

**Benchmarks**

- [Benchmarks](../benchmarks/README.md)
- [GraphRAG-Bench (Xiang)](../benchmarks/graphrag-bench-xiang.md)
- [Text2KGBench](../benchmarks/text2kgbench.md)

**Index**

- [Closed-world assumption](closed-world-assumption.md)
- [Conceptual graph](conceptual-graph.md)
- [Cyc](cyc.md)
- [DBpedia](dbpedia.md)
- [Description logic](description-logic.md)
- [Entity](entity.md)
- [Entity linking](entity-linking.md)
- [Knowledge acquisition bottleneck](knowledge-acquisition-bottleneck.md)
- [Knowledge base](knowledge-base.md)
- [Knowledge engineering](knowledge-engineering.md)
- [Knowledge graph](knowledge-graph.md)
- [Knowledge representation](knowledge-representation.md)
- [Linked data](linked-data.md)
- [LinkML](linkml.md)
- [OWL](owl.md)
- [RDF Schema](rdfs.md)
- [Schema](schema.md)
- [Schema induction](schema-induction.md)
- [schema.org](schema-org.md)
- [Semantic network](semantic-network.md)
- [Semantic Web](semantic-web.md)
- [SHACL](shacl.md)
- [Taxonomy](taxonomy.md)
- [YAGO](yago.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://tomgruber.org/writing/ontolingua-kaj-1993.pdf : Gruber, "A Translation Approach to Portable Ontology Specifications", KSL 92-71 (September 1992, revised April 1993), *Knowledge Acquisition* 5(2):199-220, 1993: abstract and introduction (read 20261102 20:54 UTC; dates and definition re-read 20261102 21:27 UTC)
2. https://tomgruber.org/writing/onto-design.pdf : Gruber, "Toward Principles for the Design of Ontologies Used for Knowledge Sharing", Int. J. Human-Computer Studies 43 (year not printed in the text read), a revision of a March 1993 workshop paper: introduction and design criteria (read 20261102 20:56 UTC)
3. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", ACM Computing Surveys 54(4), arXiv 2003.02320 v6: the passage on ontologies (read 20261102 20:57 UTC)
4. https://par.nsf.gov/servlets/purl/10292869 : Hitzler, "A Review of the Semantic Web Field" (author's version of the CACM article; accepted April 2020): sections 1 and 2.1, DAML, On-To-Knowledge, OIL; the "many-cited source from 1993" and "Arguably" passages re-read (read 20261102 21:25 UTC)
5. https://www.w3.org/TR/2004/REC-owl-features-20040210/ : OWL Web Ontology Language Overview, W3C Recommendation 10 February 2004: introduction ("a revision of the DAML+OIL web ontology language") (read 20261102 20:54 UTC)
6. http://export.arxiv.org/api/query?id_list=2505.23628 : arXiv record of Bai et al., "AutoSchemaKG", first version published 20250529, version 3 updated 20250801; abstract of version 3 only (read 20261102 21:24 UTC)
