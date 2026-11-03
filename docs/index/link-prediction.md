---
type: index
kind: concept
aliases: []
updated: 20261102 22:54 UTC
---

# Link prediction

This entry says what link prediction means, why one name covers two tasks, and how it is scored on knowledge graphs. The sources read score it in two different ways.

## Definition

Liben-Nowell and Kleinberg formalised the link prediction problem for social networks: given a snapshot at time t, predict the edges that "will be added" up to a later time t′ [1]. In knowledge graphs the name means something else. Dettmers et al. open with "Link prediction for knowledge graphs is the task of predicting missing relationships between entities" [2]. In the test of Bordes et al., the head and then the tail of each test triple is replaced by every entity in turn and the rank of the true one is recorded; the filtered setting first removes corrupted triples that are known to be true [4].

## How it changed

- **200311.** Liben-Nowell and Kleinberg present the problem at CIKM 2003, with experiments on co-authorship networks; the longer manuscript read here is dated 8 January 2004. The journal version appeared online on 26 March 2007 and was not read [1][7].
- **2013.** Bordes et al. report TransE results "in link prediction on two knowledge bases" (first-party) [4]. See [knowledge graph embedding](./knowledge-graph-embedding.md) and [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20150302 (arXiv v1).** Nickel et al. define it as predicting the existence of typed edges, that is, triples, and say that for knowledge graphs it is "also referred to as knowledge graph completion" [3][6].
- **2017 (v1 20170705; abstract of v6 read).** Dettmers et al. say the WN18 and FB15k test sets leak through inverse relations: a simple rule-based model reaches state-of-the-art results on both (first-party) [2]. See [FB15k-237](../datasets/fb15k-237.md).
- **Undated page, read 20261102.** The Open Graph Benchmark uses the one name for both tasks: its collaboration task predicts "future author collaboration relationships", and its Wikidata task ranks each true triple against 1,000 sampled negative entities [5].

## Where sources disagree

**What the name means.** Liben-Nowell and Kleinberg predict edges that appear later as a network evolves. They set apart inferring missing links in a static snapshot, which "differs from our problem formulation" [1]. Knowledge-graph papers call that static task link prediction [2][3]. The Open Graph Benchmark covers both [5].

**How it is scored.** The TransE protocol ranks the true entity among every entity [4]. The Open Graph Benchmark follows "the standard filtered metric" but with 1,000 sampled negatives [5]. *Reading:* a rank among 1,000 candidates measures something different from a rank among all entities; see [OGB link prediction](../benchmarks/ogb-link-prediction.md).

## Related

- Entries: [knowledge graph completion](./knowledge-graph-completion.md), [knowledge graph embedding](./knowledge-graph-embedding.md), [triple](./triple.md), [mean reciprocal rank](./mean-reciprocal-rank.md).
- Benchmarks: [filtered link prediction](../benchmarks/kg-link-prediction.md), [OGB link prediction](../benchmarks/ogb-link-prediction.md). Data sets: [FB15k-237](../datasets/fb15k-237.md), [WN18RR](../datasets/wn18rr.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Papers**

- [Papers: Building knowledge graphs with LLMs](../papers/llm-kg-construction.md)
- [Papers: foundations](../papers/foundations.md)

**Datasets**

- [Datasets](../datasets/README.md)
- [FB15k-237](../datasets/fb15k-237.md)
- [Freebase](../datasets/freebase.md)
- [WN18RR](../datasets/wn18rr.md)
- [YAGO](../datasets/yago.md)

**Benchmarks**

- [Benchmarks](../benchmarks/README.md)
- [Knowledge graph link prediction](../benchmarks/kg-link-prediction.md)

**Index**

- [Data contamination](data-contamination.md)
- [Knowledge graph completion](knowledge-graph-completion.md)

<!-- END GENERATED: appears-in -->

## Sources

Read times are UTC.

1. https://doi.org/10.1002/asi.20591 : Liben-Nowell and Kleinberg, "The Link Prediction Problem for Social Networks", J. Am. Soc. Inf. Sci. Technol. 58(7), 2007; this DOI is the journal version and was not read. The text read is the authors' manuscript dated 8 January 2004, from the second author's Cornell University page (its address contains a path segment that the repository's safety check rejects, so it is not given here), which says an abbreviated version appeared at CIKM 2003 in November 2003; introduction: definition, the static missing-link case (manuscript read 20261102 22:10 UTC and 22:51 UTC)
2. https://arxiv.org/abs/1707.01476 : Dettmers et al., "Convolutional 2D Knowledge Graph Embeddings", abstract; submission history (v1 5 July 2017, v6 4 July 2018) (read 20261102 22:13 UTC)
3. https://arxiv.org/pdf/1503.00759 : Nickel, Murphy, Tresp and Gabrilovich, "A Review of Relational Machine Learning for Knowledge Graphs", Section on main tasks; four authors on the first page (read 20261102 22:10 UTC and 22:45 UTC)
4. https://papers.nips.cc/paper_files/paper/2013/file/1cecc7a77928ca8133fa24680a88d2f9-Paper.pdf : Bordes et al., TransE, NIPS 2013: abstract; Section 4.2 (evaluation protocol, raw and filtered), Section 4.3 (read 20261102 22:10 UTC)
5. https://ogb.stanford.edu/docs/linkprop/ : Open Graph Benchmark, link property prediction: ogbl-collab and ogbl-wikikg2 tasks and evaluation (undated page; read 20261102 22:13 UTC)
6. https://export.arxiv.org/api/query?id_list=1503.00759,2002.00388,1909.03193,2308.13916,2003.02320,2508.15357,2203.02167 : arXiv record of Nickel et al.: v1 20150302 (read 20261102 22:12 UTC)
7. https://api.crossref.org/works/10.1002/asi.20591 : Crossref record of the journal version: volume 58, issue 7, pages 1019-1031, online 2007-03-26, print May 2007 (read 20261102 22:22 UTC)
