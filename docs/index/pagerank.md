---
type: index
kind: concept
aliases: [Google PageRank]
updated: 20261102 21:24 UTC
---

# PageRank

PageRank is a score for the nodes of a graph, first used to rank Web pages by their links [1]. This entry gives the definition, the dated changes, and two points where sources differ. The seeded variant has [its own entry](./personalized-pagerank.md).

## Definition

Page, Brin, Motwani and Winograd define PageRank as a way to rate Web pages from the link graph alone. A page has high rank if the pages that link to it have high rank, and each page shares its rank evenly among its outgoing links [1]. A rank-source vector keeps rank from piling up in loops without outgoing links and models a "random surfer" who sometimes jumps to another page [1]. Brin and Page write the score with a damping factor d, usually 0.85, and describe it as a probability distribution over pages, computed by iteration [2]. A 2021 survey lists it among node centrality measures [3].

## How it changed

- **19970110.** Priority date of Lawrence Page's patent for Stanford. The application is filed on 19980109 and the patent granted on 20010904; Google lists it as "Expired - Lifetime" and says the legal status and the priority date are assumptions, not legal conclusions [4].
- **1998.** Brin and Page describe PageRank inside the Google prototype and say scoring 26 million pages takes a few hours on a medium-size workstation [2]. See [the Web era](../history/the-web.md).
- **20020507.** Haveliwala replaces the single score by several topic-biased scores [5].
- **20160308.** Google tells Search Engine Land that it is removing Toolbar PageRank, the public score, and says it still uses PageRank data internally [6].
- **20251210.** Google's ranking-systems guide (page last updated that day) says PageRank "continues to be part of our core ranking systems" (first-party) [7].
- **20240523.** Graph-based retrieval reuses the seeded variant [8]; see [Graph-based RAG](../trends/graph-based-rag.md).

## Where sources disagree

- **Date of the report.** The text of the technical report is dated January 29, 1998 [1]. The Stanford record lists it as 1999 [9].
- **What d means.** Brin and Page call d "the probability at each page the 'random surfer' will get bored and request another random page", yet their formula multiplies the link term by d and sets d to 0.85 [2]. Hogan et al. also weight links by d [3]. HippoRAG calls its damping factor of 0.5 the probability of restarting the walk [8]. Check the convention before comparing values.

## Related

Entries: [personalized PageRank](./personalized-pagerank.md), [web search engine](./web-search-engine.md), [information retrieval](./information-retrieval.md), [knowledge graph](./knowledge-graph.md), [community detection](./community-detection.md), [GraphRAG](./graphrag.md). Pages: [HippoRAG](../projects/hipporag.md), [Graph-based RAG](../trends/graph-based-rag.md), [foundational papers](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [The Web changes data and search](../history/the-web.md)

**Index**

- [Learning to rank](learning-to-rank.md)
- [Personalized PageRank](personalized-pagerank.md)
- [Web search engine](web-search-engine.md)

<!-- END GENERATED: appears-in -->

## Sources

1. http://ilpubs.stanford.edu:8090/422/1/1999-66.pdf : Page, Brin, Motwani, Winograd, "The PageRank Citation Ranking: Bringing Order to the Web", technical report dated January 29, 1998: sections 2 and 6 (read 20261102 20:55 UTC, through an Internet Archive copy of the file)
2. https://snap.stanford.edu/class/cs224w-readings/Brin98Anatomy.pdf : Brin and Page, Computer Networks and ISDN Systems 30 (1998) 107-117: section 2.1 (read 20261102 20:54 UTC)
3. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", v6 of 11 Sep 2021: sections on graph analytics (read 20261102 21:01 UTC)
4. https://patents.google.com/patent/US6285999B1/en : US6285999B1, "Method for node ranking in a linked database", priority, filing and grant dates and legal status as listed by Google (read 20261102 21:24 UTC)
5. https://api.crossref.org/works/10.1145/511446.511513 : Haveliwala, "Topic-Sensitive PageRank", WWW 2002, issued 20020507 (read 20261102 20:56 UTC); paper text through an Internet Archive copy of http://www-cs-students.stanford.edu/~taherh/papers/topic-sensitive-pagerank.pdf (read 20261102 20:56 UTC)
6. https://searchengineland.com/google-reintroduce-toolbar-pagerank-extension-244230 : Schwartz, "Google has confirmed it is removing Toolbar PageRank", 8 March 2016, secondary report of a Google statement (read 20261102 20:58 UTC, through an Internet Archive copy)
7. https://developers.google.com/search/docs/appearance/ranking-systems-guide : section "Link analysis systems and PageRank", first-party, page last updated 2025-12-10 UTC (read 20261102 20:57 UTC)
8. https://arxiv.org/html/2405.14831v3 : Gutierrez et al., HippoRAG, arXiv 2405.14831 (v1 20240523), damping factor 0.5 described as restart probability (read 20261102 20:57 UTC)
9. http://ilpubs.stanford.edu:8090/422/ : Stanford InfoLab record of the same report, year 1999 (read 20261102 20:55 UTC, through an Internet Archive copy)
