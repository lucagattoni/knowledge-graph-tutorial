---
type: index
kind: concept
aliases: [class hierarchy, Is-A hierarchy]
updated: 20261102 22:56 UTC
---

# Taxonomy

This entry says what a taxonomy is in knowledge graphs, how the idea reached RDF and YAGO from Porphyry's tree, and how recent papers stretch the word.

## Definition

In knowledge graphs a taxonomy is a hierarchy of classes or concepts [1]. Hogan et al. describe the ontologies of enterprise knowledge graphs as "lightweight, often simple taxonomies representing a hierarchy of classes or concepts" [1]. The YAGO paper treats it as the Is-A hierarchy, apart from non-taxonomic relations [2]. In RDF Schema the link is rdfs:subClassOf: if C is a subclass of C', every instance of C is also an instance of C' [3]. The W3C's SKOS lists taxonomies among knowledge organization systems, beside thesauri, classification schemes and subject heading systems [4].

## How it changed

- **3rd century.** Sowa calls Porphyry's tree "the common core of all modern hierarchies that are used for defining concept types" [5].
- **August 1993.** In the revised introduction to WordNet, nouns are "organized in lexical memory as topical hierarchies"; maple is a hyponym of tree [6]. See [WordNet](./wordnet.md).
- **May 2007.** YAGO joins Wikipedia facts to the WordNet hierarchy, because "concepts have to be arranged in a taxonomy to be of use" [2]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **20090818 and 20140225.** SKOS and RDF Schema 1.1 become W3C Recommendations [4][3]. Eras: [The semantic web and linked data](../history/semantic-web.md), [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20230823.** The YAGO 4.5 paper says YAGO 4 "cut away large parts of the Wikidata taxonomy" and adds a large part back (first-party) [7]. See [YAGO](../datasets/yago.md).
- **20251215.** Hu and 46 co-authors "propose a finer-grained taxonomy" of agent memory functions, a classification of a field [8]. Trend: [Agent memory](../trends/agent-memory.md).
- **20260924.** A research paper's CodeGraph (not the project [CodeGraph](../projects/codegraph.md); the paper's repository is a different one) is an "open-taxonomy" graph of source code with about 63,000 extracted concept entities and roughly 19,800 grounded Wikidata entities, importing the parent-of closure of each resolved identifier (first-party) [9]. Trend: [Code graphs for coding agents](../trends/code-knowledge-graphs.md).

## Where sources disagree

**Two senses.** Hogan et al. and the YAGO paper use the word for a hierarchy of classes [1][2]. Hu et al. mean a classification scheme for a research field [8]. Of the 15 newest arXiv titles with "taxonomy" and "large language models", one (SC-Taxo) is about generating a hierarchy [10][11]. *Reading:* most of the others name classifications of failures or capabilities.

**How sharp the line is.** The SKOS Reference says it "can be hard to draw an absolute distinction between thesauri and classification schemes or taxonomies" [4]. The YAGO paper finds the Wikipedia category hierarchy "barely useful for ontological purposes" and takes WordNet's "clean taxonomy of concepts" instead [2].

## Related

[Ontology](./ontology.md) · [schema](./schema.md) · [schema induction](./schema-induction.md) · [RDFS](./rdfs.md) · [KL-ONE](./kl-one.md) · [WordNet](./wordnet.md) · [YAGO](./yago.md) · data: [WordNet](../datasets/wordnet.md), [YAGO](../datasets/yago.md) · papers: [foundations](../papers/foundations.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Datasets**

- [WordNet](../datasets/wordnet.md)
- [YAGO](../datasets/yago.md)

**Index**

- [Schema](schema.md)
- [Schema induction](schema-induction.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", ACM Computing Surveys 54(4), 2021: section 10.2 (enterprise knowledge graphs, "simple taxonomies") (read 20261102 22:10 UTC)
2. https://suchanek.name/work/publications/www2007.pdf : Suchanek, Kasneci, Weikum, "YAGO: A Core of Semantic Knowledge", WWW 2007 (8 to 12 May): abstract (Is-A hierarchy), introduction (taxonomy, Wikipedia categories against WordNet) (read 20261102 22:11 UTC)
3. https://www.w3.org/TR/rdf-schema/ : RDF Schema 1.1, W3C Recommendation 25 February 2014: rdfs:subClassOf (read 20261102 22:10 UTC)
4. https://www.w3.org/TR/skos-reference/ : SKOS Reference, W3C Recommendation 18 August 2009: abstract and introduction; https://www.w3.org/TR/skos-primer/ : SKOS Primer, abstract (read 20261102 22:10 UTC)
5. https://www.jfsowa.com/pubs/semnet.htm : Sowa, "Semantic Networks", section 1 (Tree of Porphyry, 3rd century AD) (read 20261102 22:10 UTC)
6. https://wordnetcode.princeton.edu/5papers.pdf : Miller, Beckwith, Fellbaum, Gross, Miller, "Introduction to WordNet", revised August 1993: noun hierarchies, hyponymy (read 20261102 22:11 UTC)
7. https://arxiv.org/abs/2308.11884 : Suchanek et al., "YAGO 4.5: A Large and Clean Knowledge Base with a Rich Taxonomy", v1 20230823, abstract (first-party; read 20261102 22:11 UTC)
8. https://arxiv.org/abs/2512.13564 : Hu et al., "Memory in the Age of AI Agents", 47 authors, v1 20251215, v2 20260113, abstract (read 20261102 22:11 UTC)
9. https://arxiv.org/abs/2609.29474 : Pennino et al., "CodeGraph: Open-Taxonomy Knowledge Graph for Source Code with Wikidata Grounding", v1 20260924, abstract (first-party; read 20261102 22:11 UTC): about 63,000 extracted concept entities and roughly 19,800 grounded Wikidata entities; the full text at https://arxiv.org/html/2609.29474 names the paper's repository (read 20261102 22:51 UTC)
10. https://arxiv.org/abs/2605.00620 : SC-Taxo, "Hierarchical Taxonomy Generation under Semantic Consistency Constraints using Large Language Models", v1 20260501, abstract (read 20261102 22:11 UTC)
11. https://export.arxiv.org/api/query?search_query=ti:taxonomy+AND+ti:%22large+language+models%22&max_results=15&sortBy=submittedDate&sortOrder=descending : arXiv API, titles of the 15 newest matches (read 20261102 22:11 UTC); a keyword listing, not the size of the field
