---
type: index
kind: concept
aliases: [search engine, web search]
updated: 20261102 21:25 UTC
---

# Web search engine

This entry says what a web search engine is and dates the steps that shaped it: the crawler, link analysis, query logs, entity graphs and, since 2024, model-written answers. It answers how the Web turned search from a lookup in a fixed collection into a system built on crawling, links and logs.

## Definition

A web search engine gathers pages from the Web, indexes them and ranks them for queries. Brin and Page, who describe Google in 1998, present "a prototype of a large-scale search engine which makes heavy use of the structure present in hypertext", designed to crawl and index the Web efficiently [1]. Sanderson and Croft add what changed: earlier collections were selected from authoritative sources, but a crawler gathers most pages. That invited spam, so engines turned to link analysis and to anchor text, the text of links pointing at a page [2].

## How it changed

- **Late 1993.** Web search engines start to emerge as the number of sites grows: about 100 in mid-1993, over four times that six months later. JumpStation has the first crawler for web search [2]. In 1994 WebCrawler is the first full-text engine to use one [2]. See [The Web changes data and search](../history/the-web.md).
- **1998.** The Google prototype holds a full-text and hyperlink database of at least 24 million pages [1]. Anchor text was "a key feature" of Google from its early development, along with [PageRank](./pagerank.md) [2].
- **2000s.** Query logs from web users supply the training data that make [learning to rank](./learning-to-rank.md) "truly effective" [2]. See [The semantic web and linked data](../history/semantic-web.md).
- **20120516.** Google announces its Knowledge Graph in search, "things, not strings", (first-party) [3]; the figures are in the Google Knowledge Graph entry. See [Google Knowledge Graph](./google-knowledge-graph.md) and [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20240514.** Google says AI Overviews, a quick overview of a topic with links, begin to roll out to everyone in the US (first-party) [4].
- **20250305, still moving.** Google says AI Overviews are "now used by more than a billion people" (first-party) and introduces an experimental AI Mode; its post names web content, "fresh, real-time sources like the Knowledge Graph" and shopping data [5]. How these answers are built from the search index is **unstated** in the pages read. See [the trends](../trends/README.md).

## Where sources disagree

No disagreement found in the sources read.

## Related

[information retrieval](./information-retrieval.md) · [PageRank](./pagerank.md) · [learning to rank](./learning-to-rank.md) · [BM25](./bm25.md) · [TREC](./trec.md) · [Google Knowledge Graph](./google-knowledge-graph.md) · [URI](./uri.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [The Web changes data and search](../history/the-web.md)

**Index**

- [Google Knowledge Graph](google-knowledge-graph.md)
- [Information retrieval](information-retrieval.md)
- [Inverted index](inverted-index.md)
- [PageRank](pagerank.md)
- [TREC](trec.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://snap.stanford.edu/class/cs224w-readings/Brin98Anatomy.pdf : Brin and Page, "The anatomy of a large-scale hypertextual Web search engine", Computer Networks and ISDN Systems 30, 1998: abstract, at least 24 million pages (read 20261102 21:00 UTC)
2. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE 100, 2012: web search section and footnote 3, learning to rank, query logs (read 20261102 21:00 UTC)
3. https://blog.google/products/search/introducing-knowledge-graph-things-not/ : Singhal, Google, "Introducing the Knowledge Graph: things, not strings", 20120516 (read 20261102 21:06 UTC)
4. https://blog.google/products/search/generative-ai-google-search-may-2024/ : Reid, Google, 20240514: AI Overviews begin rolling out to everyone in the US (read 20261102 21:06 UTC)
5. https://blog.google/products/search/ai-mode-search/ : Stein, Google, 20250305: AI Overviews "more than a billion people"; AI Mode experiment; web content, Knowledge Graph and shopping data as sources (read 20261102 21:24 UTC)
