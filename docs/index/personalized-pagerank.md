---
type: index
kind: concept
aliases: [PPR, personalised PageRank]
updated: 20261102 21:24 UTC
---

# Personalized PageRank

Personalized PageRank is PageRank whose random walk returns to chosen nodes, so the scores measure closeness to them [1][3]. This entry gives the definition, the dated changes from Web search to retrieval for language models, and how the word "personalized" drifted.

## Definition

In the original PageRank report, the rank-source vector E is the distribution of pages a random surfer jumps to. Page et al. call it "a powerful parameter to adjust the page ranks": a uniform E gives a general view of the Web, an E on one page a view from that page. They tested the Netscape home page and John McCarthy's [1]. Brin and Page put it as adding the damping factor to "a single page, or a group of pages", which "allows for personalization" [2]. HippoRAG defines it as "a version of PageRank that distributes probability across a graph only through a set of user-defined source nodes" [3].

## How it changed

- **1998.** The report has a section "Personalized PageRank". It claims such ranks are "virtually immune to manipulation by commercial interests" (first-party) [1]. See [the Web era](../history/the-web.md).
- **20020507.** Haveliwala precomputes one PageRank vector per representative topic and combines them at query time. He reports more accurate rankings than a single vector (first-party) [4]. See [the semantic web era](../history/semantic-web.md).
- **2003.** Haveliwala, Kamvar and Jeh compare three ways to personalize with biased vectors (report deposited 20030619) [5]. Jeh and Widom publish "Scaling personalized web search" at WWW 2003 [6].
- **20240523.** HippoRAG runs it on a model-built [knowledge graph](./knowledge-graph.md), with the entities of the query as seeds. The authors (first-party) report gains of up to 20% over the best earlier methods on multi-hop questions [3].
- **20250220.** HippoRAG 2 "builds upon" it and reports 7% over the best embedding model on associative-memory tasks (first-party) [7].

Still moving: [Graph-based RAG](../trends/graph-based-rag.md), [Learned graph traversal](../trends/learned-graph-traversal.md).

## Where sources disagree

- **Who is personalized.** Page et al. personalize to an individual's view [1]. Haveliwala biases by topic [4]. HippoRAG's seeds are the entities of one query, with no user or topic profile [3].
- **Damping.** HippoRAG's damping factor of 0.5 is the restart probability [3]; in Brin and Page's formula d weights the links [2]. See [PageRank](./pagerank.md).

## Related

Entries: [PageRank](./pagerank.md), [knowledge graph](./knowledge-graph.md), [GraphRAG](./graphrag.md), [community detection](./community-detection.md), [retrieval-augmented generation](./retrieval-augmented-generation.md), [multi-hop question answering](./multi-hop-question-answering.md). Pages: [HippoRAG](../projects/hipporag.md), [Graph-based RAG papers](../papers/graph-based-rag.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)
- [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [HippoRAG](../projects/hipporag.md)
- [Projects](../projects/README.md)

**Papers**

- [Papers: Graph-based RAG](../papers/graph-based-rag.md)

**Applied to Pinakes**

- [Measurements](../applied-to-pinakes/measurements.md)
- [The Pinakes graph approach](../applied-to-pinakes/approach.md)
- [What Pinakes should measure next](../applied-to-pinakes/next.md)
- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Community detection](community-detection.md)
- [GraphRAG](graphrag.md)
- [Multi-hop question answering](multi-hop-question-answering.md)
- [PageRank](pagerank.md)
- [Reciprocal rank fusion](reciprocal-rank-fusion.md)

<!-- END GENERATED: appears-in -->

## Sources

1. http://ilpubs.stanford.edu:8090/422/1/1999-66.pdf : Page, Brin, Motwani, Winograd, technical report dated January 29, 1998: sections 2.4, 2.5 and 6 (read 20261102 20:55 UTC, through an Internet Archive copy of the file)
2. https://snap.stanford.edu/class/cs224w-readings/Brin98Anatomy.pdf : Brin and Page, Computer Networks and ISDN Systems 30 (1998) 107-117: section 2.1.2 (read 20261102 20:54 UTC)
3. https://arxiv.org/html/2405.14831v3 : Gutierrez et al. (5 authors), "HippoRAG", arXiv 2405.14831, v1 20240523, NeurIPS 2024: abstract, introduction, damping factor (read 20261102 20:57 UTC)
4. https://api.crossref.org/works/10.1145/511446.511513 : Haveliwala, "Topic-Sensitive PageRank", WWW 2002, issued 20020507 (read 20261102 20:56 UTC); abstract through an Internet Archive copy of http://www-cs-students.stanford.edu/~taherh/papers/topic-sensitive-pagerank.pdf (read 20261102 20:56 UTC)
5. http://ilpubs.stanford.edu:8090/596/ : Haveliwala, Kamvar, Jeh, "An Analytical Comparison of Approaches to Personalizing PageRank", technical report, deposited 19 Jun 2003 (read 20261102 20:57 UTC, through an Internet Archive copy)
6. https://api.crossref.org/works/10.1145/775152.775191 : Jeh and Widom, "Scaling personalized web search", WWW 2003: bibliographic record only, abstract not read (read 20261102 20:56 UTC)
7. https://arxiv.org/abs/2502.14802 : Gutierrez et al. (5 authors), "From RAG to Memory", arXiv 2502.14802, v1 20250220, ICML 2025: abstract (read 20261102 20:54 UTC)
