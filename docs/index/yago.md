---
type: index
kind: system
aliases: []
updated: 20261102 21:26 UTC
---

# YAGO

YAGO is a knowledge base that began as Wikipedia facts attached to the hierarchy of WordNet and is now a cleaned subset of Wikidata. This entry gives the definition and the version history; for content, size and licence, see the dataset page.

## Definition

The founding paper presents YAGO as "a light-weight and extensible ontology with high coverage and quality", built on entities and relations, with facts "automatically extracted from Wikipedia and unified with WordNet" [1]. The project site now calls it "a large knowledge base with general knowledge about people, cities, countries, movies, and organizations" [2]. From YAGO 4 on, its facts come from [Wikidata](./wikidata.md), its higher classes and its properties from schema.org, and its lower classes are a selection from Wikidata [3][4].

## How it changed

- **May 2007.** Suchanek, Kasneci and Weikum publish YAGO in the proceedings of WWW 2007, held 8 to 12 May in Banff; Crossref gives an issue date of 20070508, the first day of the conference, and the day of the talk is **unstated** [1][5]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **20121016.** YAGO2s is released [2]. The YAGO2 article, a "spatially and temporally enhanced" base, appears in *Artificial Intelligence* 194 in January 2013 [6].
- **20150324.** YAGO3 is released for download [2]. Its paper fuses the Wikipedias of several languages with English WordNet [7]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20170831.** The code becomes open source [2].
- **March 2020.** YAGO 4 is released [2]. It keeps schema.org's top-level classes, takes facts from Wikidata and omits facts whose predicates could not be mapped [3].
- **May 2023.** YAGO 4.5 adds "a much richer taxonomy" [2]; its paper appears at SIGIR on 20240710 [8].
- **July 2026.** YAGO 4.6 is out, with files on statements left out of Wikidata; a demo paper is accepted at ISWC 2026 [2][9].

## Where sources disagree

The home page news says YAGO 4.6 lists statements "removed from Wikidata" [2]; the download page says files hold statements "excluded from Wikidata" [9]. Whether Wikidata deleted them or YAGO left them out is **unstated** in both. Also, the 2007 abstract calls YAGO an "ontology", the home page now calls it a "knowledge base", and the YAGO 4 page read does not mention WordNet: its classes come from schema.org and Wikidata [1][2][3].

## Related

Entries: [Wikidata](./wikidata.md), [WordNet](./wordnet.md), [DBpedia](./dbpedia.md), [Freebase](./freebase.md), [knowledge graph](./knowledge-graph.md), [ontology](./ontology.md), [schema.org](./schema-org.md), [SHACL](./shacl.md). Dataset: [YAGO](../datasets/yago.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [The semantic web and linked data](../history/semantic-web.md)

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Index**

- [DBpedia](dbpedia.md)
- [Freebase](freebase.md)
- [Knowledge graph embedding](knowledge-graph-embedding.md)
- [Linked data](linked-data.md)
- [Taxonomy](taxonomy.md)
- [Wikidata](wikidata.md)
- [WordNet](wordnet.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://suchanek.name/work/publications/www2007.pdf : Suchanek, Kasneci, Weikum, "YAGO: A Core of Semantic Knowledge", WWW 2007; abstract; footer "WWW 2007, May 8-12, 2007, Banff" (read 20261102 21:25 UTC)
2. https://yago-knowledge.org/ : YAGO home page, description and news list from 20121016 to October 2026 (first-party; read 20261102 21:07 UTC)
3. https://yago-knowledge.org/downloads/yago-4 : YAGO 4: Wikidata facts, schema.org classes and properties, higher classes from schema.org, lower classes a selection from Wikidata, unmapped predicates omitted (first-party; read 20261102 21:24 UTC)
4. https://yago-knowledge.org/getting-started : "a logically consistent subset" of Wikidata, schema.org relations (first-party; read 20261102 21:07 UTC)
5. https://doi.org/10.1145/1242572.1242667 : Crossref record of the WWW 2007 paper, issued 20070508, 3 authors (read 20261102 21:24 UTC)
6. https://doi.org/10.1016/j.artint.2012.06.001 : Crossref record of Hoffart, Suchanek, Berberich, Weikum, "YAGO2: A spatially and temporally enhanced knowledge base from Wikipedia", AIJ 194, 28-61, January 2013 (read 20261102 21:07 UTC)
7. https://suchanek.name/work/publications/cidr2015.pdf : Mahdisoltani, Biega, Suchanek, "YAGO3: A Knowledge Base from Multilingual Wikipedias", abstract (read 20261102 21:08 UTC)
8. https://doi.org/10.1145/3626772.3657876 : Crossref record of Suchanek and five co-authors, "YAGO 4.5", SIGIR 2024, issued 20240710 (read 20261102 21:07 UTC)
9. https://yago-knowledge.org/downloads/yago-4-6 : YAGO 4.6 page, statements "excluded from Wikidata" (first-party; read 20261102 21:08 UTC)
