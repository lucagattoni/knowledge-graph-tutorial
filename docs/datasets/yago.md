---
type: dataset
kinds: [kg]
updated: 20261102 21:32 UTC
---

# YAGO

This page answers what the YAGO knowledge graph contains, how big each version is, and under which licence each version is released. YAGO started in 2007 as Wikipedia facts placed under the [WordNet](wordnet.md) taxonomy [9]. Since version 4 it is a cleaned subset of [Wikidata](wikidata.md) [2][6]. One subset of it is a standard [link-prediction](../index/link-prediction.md) test.

## What it contains

YAGO holds entities (people, cities, countries, movies, organisations), arranged in a [taxonomy](../index/taxonomy.md) of classes, and facts about them [2]. A manually defined [schema](../index/schema.md) says which relations can hold between which classes, with constraints: disjoint classes, functional relations (at most one birth place), domain and range [2]. The facts are [RDF](../index/rdf.md) [triples](../index/triple.md) using [schema.org](../index/schema-org.md) predicates; facts about facts use [RDF-star](../index/rdf-star.md) [2]. Release 4.6 is a set of Turtle files, with the schema written in [SHACL](../index/shacl.md) [8].

## Size and versions

The licence and the size change with the version, so cite the version. The site's figures:

| Version | Size, as the site states it | Built from | Data licence |
|---|---|---|---|
| paper, 2007 | over 1 million entities, 5 million facts [9] | Wikipedia, WordNet | unstated |
| 1 (2008) | over 2 million entities, 20 million facts [3] | Wikipedia of 20081001, WordNet | GNU FDL [3] |
| 2s | unstated on its page [4] | Wikipedia of 20121201 | CC BY 3.0 [4] |
| 3 | over 17 million entities, over 150 million facts [5] | ten Wikipedias (2013-2014), WordNet, GeoNames | CC BY 3.0 [5] |
| 4 | over 50 million entities, 2 billion facts [6] | Wikidata, schema.org | CC BY-SA, version 3.0 linked [6] |
| 4.5 | 49 million entities, 109 million facts [7] | Wikidata, schema.org | CC BY-SA, version 3.0 linked [7] |
| 4.6 (July 2026 [1]) | 39 million entities, 167 million facts [8] | Wikidata, schema.org | CC BY, version 4.0 linked [8] |

An unofficial 2022 update, YAGO 3.0.3, was not evaluated by hand [5]. The site news lists YAGO on Zenodo in February 2022 and again in October 2026 [1].

## Licence

Each version page states its own data licence (table above) [3][4][5][6][7][8]. The 4.6 code is under CC BY too (repository: CC BY 4.0) [8][16]; the YAGO 3 code is GPL-3.0 [5][16]. YAGO 4 and 4.5 import some facts from schema.org "under the same license", which is CC BY-SA [6][7].

## How it was made

1. **2007.** Facts are extracted from Wikipedia and unified with WordNet. Only Wikipedia's leaf categories are kept as classes; WordNet supplies the class hierarchy [9].
2. **YAGO 3 (2015).** Infoboxes, categories and Wikidata of ten languages are fused with English WordNet. The method learns what infobox attributes mean across languages; it adds 1 million entities and 7 million facts to YAGO [10].
3. **YAGO 4 onward.** A Python project ingests Wikidata facts and transforms them into YAGO; the upper classes and properties are defined by hand with schema.org identifiers [8][2]. YAGO calls itself "a logically consistent subset" of Wikidata [2]. Version 4.5 re-adds a large part of the Wikidata taxonomy: 133 thousand classes against 10 thousand in YAGO 4 [11].

## Used by

| User | What it takes | Page |
|---|---|---|
| YAGO3-10 | a subset of YAGO 3: the entities with at least 10 relations [12]; sizes, flaws and scores are on the benchmark page | [link-prediction benchmark](../benchmarks/kg-link-prediction.md) |
| AIDA CoNLL-YAGO | the CoNLL 2003 text with Wikipedia links added by the YAGO2 system; an [entity-linking](../index/entity-linking.md) set in KILT [14] | [KILT](../benchmarks/kilt.md) |
| [DBpedia](dbpedia.md) | its 2007 release carried YAGO classes as types [15] | |

The fundamental paper is Suchanek et al. 2007, in [the foundations group](../papers/foundations.md). The YAGO site says it won the Seoul Test of Time Award of The Web Conference 2018 [1]. A citation count is **unstated**: the research notes did not retrieve one. No trend source read for this page uses YAGO.

## Known problems

- **Counts conflict.** YAGO 4.5 has 109 million facts on the site [7] and 132 million in its paper; YAGO 4 has "2 billion" on the site [6] and 343 million in the paper, which excludes type, label and some other facts [11]. The site's counting rule is **unstated**.
- **Entities fall, facts rise.** From 4.5 to 4.6 entities drop from 49 to 39 million and facts rise from 109 to 167 million, with no reason given [7][8].
- **Dropped statements.** YAGO 4 abandoned nearly the whole Wikidata class taxonomy, which 4.5 partly restored [11]. Version 4.6 ships "logs of statements that were excluded"; the rule for excluding is **unstated** [8].
- **Accuracy is first-party.** The 95% figures are the authors' own manual evaluations; for YAGO 1 it is "with respect to the extraction source" [3][5].
- **YAGO3-10 has near-duplicate relations.** Two relations, `isAffiliatedTo` and `playsFor`, dominate its training and test triples [13]. The figures and what they do to scores are on the [benchmark page](../benchmarks/kg-link-prediction.md).
- **Frozen snapshots.** Versions 1 to 3 depend on Wikipedia dumps of 2008 to 2014 [3][4][5].

*Reading:* YAGO trades size for consistency; name the version, because content and licence moved with it.

## Sources

1. https://yago-knowledge.org/ : news (4.6 out in July 2026, Zenodo in October 2026), version list, awards (read 20261102 21:27 UTC)
2. https://yago-knowledge.org/getting-started : what YAGO is, schema, constraints, data model, RDF-star (read 20261102 20:50 UTC)
3. https://yago-knowledge.org/downloads/yago-1 : size, sources, accuracy, GNU FDL (read 20261102 20:50 UTC)
4. https://yago-knowledge.org/downloads/yago-2s : accuracy, CC BY 3.0, Wikipedia date (read 20261102 20:52 UTC)
5. https://yago-knowledge.org/downloads/yago-3 : size, ten Wikipedias, CC BY 3.0, GPL code, 2022 revival (read 20261102 20:50 UTC)
6. https://yago-knowledge.org/downloads/yago-4 : size, sources, CC BY-SA (read 20261102 20:50 UTC)
7. https://yago-knowledge.org/downloads/yago-4-5 : size, CC BY-SA (read 20261102 20:50 UTC)
8. https://yago-knowledge.org/downloads/yago-4-6 : size (39 million entities, 167 million facts), files, logs, CC BY; the page shows no release date (read 20261102 21:27 UTC)
9. https://suchanek.name/work/publications/www2007.pdf : Suchanek et al., WWW 2007, full text (read 20261102 20:52 UTC)
10. https://suchanek.name/work/publications/cidr2015.pdf : Mahdisoltani et al., CIDR 2015, full text (read 20261102 20:52 UTC)
11. https://arxiv.org/abs/2308.11884 : YAGO 4.5 paper (SIGIR 2024), full text: Table 1, taxonomy (read 20261102 20:58 UTC)
12. https://arxiv.org/abs/1707.01476 : ConvE paper: YAGO3-10 as "a subset of YAGO3" of entities with at least 10 relations (full text, read 20261102 21:29 UTC)
13. https://arxiv.org/abs/2003.08001 : Akrami et al., SIGMOD 2020: near-duplicate relations in YAGO3-10 (read 20261102 20:58 UTC)
14. https://arxiv.org/abs/2009.02252 : KILT paper: AIDA CoNLL-YAGO (read 20261102 20:58 UTC)
15. https://web.archive.org/web/2012/http://iswc2007.semanticweb.org/papers/715.pdf : Auer et al., ISWC 2007: Yago Types dataset (read 20261102 20:54 UTC)
16. https://api.github.com/repos/yago-naga/yago-4.6 and /yago3 (via `gh api`) : detected code licences (read 20261102 21:00 UTC)
