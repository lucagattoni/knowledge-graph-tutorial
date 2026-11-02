---
type: index
kind: system
aliases: [ConceptNet 5]
updated: 20261102 20:51 UTC
---

# ConceptNet

## Definition

ConceptNet is a knowledge graph that connects words and phrases of natural language, called terms, with labelled, weighted edges, called assertions [1]. It aims to hold the general knowledge involved in understanding language, collected from expert-built resources, crowd-sourcing and games with a purpose [1][2]. Its focus is the common-sense meaning of words, not named entities, which sets it apart from [DBpedia](./dbpedia.md) and the [Google Knowledge Graph](./google-knowledge-graph.md) [2]. Content, size and licence are on the dataset page [ConceptNet](../datasets/conceptnet.md).

## How it changed

- 1999: the Open Mind Common Sense project, from which ConceptNet originated, is launched at the MIT Media Lab, according to the project site [3].
- 200410: Liu and Singh publish the original ConceptNet in BT Technology Journal 22(4) [4]. The 2017 paper describes it as a parsed representation of Open Mind Common Sense [1].
- 2012: the ConceptNet 5 paper (LREC) sets as goals to take in knowledge mined from Wiktionary and Wikipedia and to link to DBpedia, Freebase and [WordNet](./wordnet.md) [5].
- 20161212: the ConceptNet 5.5 paper (first version) presents a version suited to word embeddings; 5.2 was the last release published before it [1][2]. See the era [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- 20190612: COMET (first version) trains language models to generate new ConceptNet and ATOMIC assertions, with 91.7% precision at top 1 on ConceptNet, per its authors [6]. See the era [Language models meet retrieval](../history/language-models-meet-retrieval.md).

## Where sources disagree

The start year of the origin project: the project site says Open Mind Common Sense was launched in 1999 [3], while the 5.5 paper cites it as Singh 2002 [1]. *Reading:* one date is a launch and the other a publication, but neither source says so; the link is **unstated**. The two sources also name the thing differently: "a freely-available semantic network" on the site [3], "a knowledge graph" in the paper [1].

## Related

[WordNet](./wordnet.md) · [Cyc](./cyc.md) · [DBpedia](./dbpedia.md) · [Freebase](./freebase.md) · [knowledge graph](./knowledge-graph.md) · [semantic network](./semantic-network.md) · [embedding](./embedding.md) · dataset [ConceptNet](../datasets/conceptnet.md) · dataset [WordNet](../datasets/wordnet.md) · papers [Foundations](../papers/foundations.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [Language models meet retrieval (2018-2022)](../history/language-models-meet-retrieval.md)

**Index**

- [Cyc](cyc.md)
- [WordNet](wordnet.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/1612.03975 : Speer, Chin, Havasi, "ConceptNet 5.5: An Open Multilingual Graph of General Knowledge", v1 20161212, v2 20181211; AAAI 2017 copyright line; introduction and related work (read 20261102 20:47 UTC, text extracted from the downloaded PDF); abstract (read 20261102 20:45 UTC)
2. https://arxiv.org/abs/1612.03975 : same paper, abstract and related-work comparison with Cyc, DBpedia and the Google Knowledge Graph (read 20261102 20:47 UTC)
3. https://conceptnet.io/ : project site: "launched in 1999 at the MIT Media Lab", "semantic network" (read 20261102 20:47 UTC, via a fetch-tool extraction)
4. https://api.crossref.org/works/10.1023/B:BTTJ.0000047600.45421.6d : Liu and Singh, "ConceptNet: A Practical Commonsense Reasoning Tool-Kit", BT Technology Journal 22(4), October 2004 (read 20261102 20:50 UTC)
5. https://www.lrec-conf.org/proceedings/lrec2012/pdf/1072_Paper.pdf : Speer and Havasi, "Representing General Relational Knowledge in ConceptNet 5", LREC 2012, section 2 (read 20261102 20:47 UTC, text extracted from the downloaded PDF)
6. https://arxiv.org/abs/1906.05317 : Bosselut and five co-authors, COMET, v1 20190612, abstract (read 20261102 20:50 UTC)
