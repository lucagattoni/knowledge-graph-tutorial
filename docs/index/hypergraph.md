---
type: index
kind: concept
aliases: [knowledge hypergraph, set system]
updated: 20261102 22:54 UTC
---

# Hypergraph

This entry says what a hypergraph is and why knowledge-graph work turned to it. Its use in retrieval systems dates from 2025 and is still moving.

## Definition

A hypergraph is a set of vertices with a family of subsets of them, called hyperedges [1]. A simple graph is the case where every hyperedge has two vertices [1]; Feng et al. say a hyperedge "connects two or more vertices" [2]. In a knowledge graph a hyperedge can stand for one n-ary fact joining more than two entities, which a [triple](./triple.md) would split into pairs [3].

## How it changed

- **1970 and 1973.** Berge's *Graphes et hypergraphes* (Dunod, 1970) and *Graphs and Hypergraphs* (North-Holland, 1973), by catalogue record [4]. Who first defined the object is **unstated** in the sources read. Bretto lists "set systems" and "families of sets" as other names [5]. See [Formal foundations](../history/formal-foundations.md).
- **20160428.** Wen et al. argue that turning n-ary data into triples, as the FB15K set does, loses structure (IJCAI 2016) [6]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20180925.** Feng et al. propose hypergraph neural networks (AAAI 2019) [2]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20250327 to 20260125.** HyperGraphRAG builds a hypergraph of n-ary facts for retrieval (NeurIPS 2025) [3]. Graph-R1 (20250729) trains an agent by reinforcement learning to retrieve from one (ICML 2026) [7]. HyperGraphPro (20260125) adds stepwise rewards and is marked "in progress" [8]. All first-party. Still moving: [Graph-based RAG](../trends/graph-based-rag.md), [Agentic graph retrieval](../trends/learned-graph-traversal.md).
- **As read on 20261102.** [Hyper-Extract](../projects/hyper-extract.md) lists hypergraphs among nine knowledge structures [9]. [Graphify](../projects/graphify.md)'s prompt asks for a hyperedge when "3 or more nodes" participate together, at most 3 per chunk [10].

## Where sources disagree

**Size.** MathWorld says conventions differ on empty, singleton and repeated hyperedges [1]. Feng et al. and HyperGraphRAG require two or more vertices [2][3]. Graphify asks for three or more [10].

**Content.** In the mathematical definition a hyperedge is a plain subset [1]. In HyperGraphRAG it also carries a natural-language description of the fact [3].

## Related

[Knowledge graph](./knowledge-graph.md), [triple](./triple.md), [property graph](./property-graph.md), [RDF-star](./rdf-star.md), [entity](./entity.md), [GraphRAG](./graphrag.md). Projects: [Hyper-Extract](../projects/hyper-extract.md), [Graphify](../projects/graphify.md). Benchmark: [RAGSearch](../benchmarks/ragsearch.md). Papers: [graph-based RAG](../papers/graph-based-rag.md), [agentic graph retrieval](../papers/learned-graph-traversal.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)

**Projects**

- [Hyper-Extract](../projects/hyper-extract.md)
- [Projects](../projects/README.md)

**Papers**

- [Papers: Agentic graph retrieval](../papers/learned-graph-traversal.md)

**Index**

- [GRPO](grpo.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://mathworld.wolfram.com/Hypergraph.html : definition as vertices plus a family of subsets; 2-uniform case is a simple graph; conventions differ on empty, singleton and repeated hyperedges (read 20261102 22:08 UTC)
2. https://arxiv.org/pdf/1809.09401 : Feng et al., "Hypergraph Neural Networks", v3 of 23 Feb 2019, section "Hypergraph learning statement" (read 20261102 22:07 UTC); https://arxiv.org/abs/1809.09401 : first version 25 Sep 2018, "Accepted in AAAI'2019" (read 20261102 22:07 UTC)
3. https://arxiv.org/pdf/2503.21322 : Luo et al., "HyperGraphRAG", v3 of 21 Oct 2025, abstract and introduction: n-ary relations, hyperedge connects n entities (n >= 2), natural-language descriptions (first-party; read 20261102 22:07 UTC); https://arxiv.org/abs/2503.21322 : first version 27 Mar 2025, journal reference NeurIPS 2025 (read 20261102 22:06 UTC)
4. https://openlibrary.org/search.json?q=berge+hypergraphs : catalogue records of Berge's books, first-publication years 1970 (Dunod) and 1973 (North-Holland); a catalogue, not the books (read 20261102 22:08 UTC)
5. https://link.springer.com/book/10.1007/978-3-319-00080-0 : Bretto, "Hypergraph Theory: An Introduction", 2013, book description: other names "set systems" and "families of sets"; plain HTTP requests get a client challenge, the text reads only after following the cookie redirect (read 20261102 22:08 UTC and 22:42 UTC)
6. https://arxiv.org/abs/1604.08642 : Wen et al., "On the representation and embedding of knowledge bases beyond binary relations", 28 Apr 2016, "to appear in IJCAI 2016", abstract (read 20261102 22:09 UTC)
7. https://arxiv.org/abs/2507.21892 : Luo et al., "Graph-R1", first submitted 29 Jul 2025, "Accepted by ICML 2026", abstract (first-party; read 20261102 22:07 UTC)
8. https://arxiv.org/abs/2601.17755 : Park et al., "HyperGraphPro", submitted 25 Jan 2026, comment "In progress", abstract (first-party; read 20261102 22:07 UTC)
9. https://github.com/yifanfeng97/Hyper-Extract/blob/main/README.md : nine knowledge structures including Hypergraph (first-party; read 20261102 22:08 UTC)
10. https://github.com/Graphify-Labs/graphify/blob/v8/graphify/skills/claude/references/extraction-spec.md : hyperedge rule, "3 or more nodes", maximum 3 per chunk (first-party; read 20261102 22:09 UTC)
