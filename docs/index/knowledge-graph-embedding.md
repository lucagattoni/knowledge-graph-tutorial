---
type: index
kind: concept
aliases: [KGE, KG embedding]
updated: 20261102 21:28 UTC
---

# Knowledge graph embedding

This entry says what a knowledge graph embedding is, when the idea appeared, and why its first test sets had to be repaired.

## Definition

A knowledge graph embedding gives every entity and relation of a graph a vector; a scoring function over the vectors says how plausible an edge is. Hogan et al. state the goal as "to create a dense representation of the graph (i.e., embed the graph) in a continuous, low-dimensional vector space" [1]. They sort the methods into translational, tensor-decomposition, neural and language-model families [1]. TransE, the simplest translational model, makes the subject vector plus the relation vector land near the object vector [1][2].

## How it changed

- **2011.** RESCAL factorizes a three-way tensor of multi-relational data (ICML 2011) [3].
- **2013.** Bordes et al. present TransE (NIPS 26): relations act as translations on entity embeddings. They say it can be trained on a data set with 1M entities, 25k relationships and more than 17M training samples [2]. The month is unstated. See [knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **2015 (July).** Toutanova and Chen compare a simple observed-features model, which predicts from edges already in the graph, with latent-feature models on FB15K and WN18. The observed-features model scores much higher than the latent models they trained (a model called E, DistMult, and the two combined) and than the prior-work numbers they list, TransE among them [4]. They also derive a harder FB15K subset, which they call FB15KSelected, by removing near-duplicate and inverse relations; on it the latent models they studied outperform the observed-features model [4]. The subset is the one later called FB15k-237, see [FB15k-237](../datasets/fb15k-237.md) [5].
- **20170705 (arXiv v1).** Dettmers et al. design a model with a single rule that reverses relations, and say it "achieves state-of-the-art results" on WN18 and FB15k [5]. They note that the test sets of both contain mostly reversed triples that are present in the training set, a point they credit to Toutanova and Chen [5]. They derive a subset of WN18, WN18RR, see [WN18RR](../datasets/wn18rr.md), and recommend FB15k-237, WN18RR and YAGO3-10 in place of FB15k and WN18 [5].
- **20200304 (arXiv v1).** Hogan et al. note that an embedding has no vector for an unseen node and "would need to be retrained" [1].

Whether embeddings became standard practice is **unstated** in the sources read.

## Where sources disagree

Bordes et al. say TransE "significantly outperforms state-of-the-art methods in link prediction on two knowledge bases" [2]. Two later papers find that, on the two common sets FB15K and WN18, a simple model that uses the edges already present does as well or better. Toutanova and Chen report that their observed-features model scores much higher than the latent models they trained and than the TransE numbers they list [4]. Dettmers et al. report that a single rule that reverses relations reaches state of the art [5].

Both papers trace this to the test sets. Toutanova and Chen report that 80.9% of FB15K and 94.0% of WN18 test triples have their entity pair directly linked in the training graph [4]. Dettmers et al. say the test sets contain mostly reversed triples from the training set [5]. Toutanova and Chen also report that on their repaired subset the latent models they studied do better than the observed-features model [4].

## Related

- Entries: [embedding](./embedding.md), [knowledge graph](./knowledge-graph.md), [mean reciprocal rank](./mean-reciprocal-rank.md), [Freebase](./freebase.md), [WordNet](./wordnet.md), [YAGO](./yago.md).
- Data sets: [FB15k-237](../datasets/fb15k-237.md), [WN18RR](../datasets/wn18rr.md). Benchmark: [filtered link prediction](../benchmarks/kg-link-prediction.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Benchmarks**

- [Knowledge graph link prediction](../benchmarks/kg-link-prediction.md)
- [OGB link prediction](../benchmarks/ogb-link-prediction.md)

**Index**

- [Embedding](embedding.md)
- [Entity](entity.md)
- [Knowledge graph](knowledge-graph.md)
- [Knowledge graph completion](knowledge-graph-completion.md)
- [Link prediction](link-prediction.md)
- [Temporal knowledge graph](temporal-knowledge-graph.md)
- [Triple](triple.md)

<!-- END GENERATED: appears-in -->

## Sources

Read times are UTC.

1. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", ACM Computing Surveys 54(4), 2021; Section 5.2 (definition, families, TransE) and Section 5.4 (unseen nodes); submission date from https://arxiv.org/abs/2003.02320 (read 20261102 20:45 and 20:51)
2. https://papers.nips.cc/paper_files/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html : Bordes et al., "Translating Embeddings for Modeling Multi-relational Data", NIPS 26, 2013, abstract (read 20261102 20:45 and 21:25)
3. https://icml.cc/2011/papers/438_icmlpaper.pdf : Nickel, Tresp, Kriegel, "A Three-Way Model for Collective Learning on Multi-Relational Data", ICML 2011 (read 20261102 20:51)
4. https://aclanthology.org/W15-4007.pdf : Toutanova and Chen, "Observed versus latent features for knowledge base and text inference", CVSC workshop, July 2015; full text: introduction, results tables for FB15K, WN18 and FB15KSelected, share of linked test triples (read 20261102 20:47 and 21:23)
5. https://arxiv.org/pdf/1707.01476v1 : Dettmers et al., "Convolutional 2D Knowledge Graph Embeddings", arXiv version 1 (full text: reversal-rule model, WN18RR, recommendations, the FB15k-237 name); the date 20170705 of v1 from https://arxiv.org/abs/1707.01476 (read 20261102 20:47); text of v1 read 20261102 21:23
