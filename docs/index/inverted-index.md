---
type: index
kind: concept
aliases: [inverted file, full-text index]
updated: 20261102 22:52 UTC
---

# Inverted index

This entry says what an inverted index is and why text search engines are built on it. The sources disagree on whether embedding search has displaced it.

## Definition

An inverted index keeps a dictionary of terms and, for each term, a list of the documents that contain it, the postings list [1]. The dictionary also records how many documents contain each term, which ranking models later use, and postings are sorted by document identifier for fast queries [2]. Manning, Raghavan and Schütze call it "essentially without rivals as the most efficient structure for supporting ad hoc text search" [2]. They add that the name is redundant, because "an index always maps back from terms to the parts of a document where they occur", and that "inverted file" is also used [1]. A scoring function such as [BM25](./bm25.md) ranks what the index finds.

## How it changed

- **1960s.** Stonebraker and Pavlo say the SMART system built full-text indexes, "aka inverted indexes", on tokens [3]. Sanderson and Croft describe Taube's Uniterm of 1952, indexing items by keywords, without the term [4]. Who built the first inverted index is **unstated** in the sources read. See [The advent](../history/advent.md).
- **20060725.** Zobel and Moffat publish a tutorial on inverted files for text search engines, saying the technology advanced "dramatically" in the past decade (*ACM Computing Surveys* 38(2)) [5].
- **20080707.** The Manning, Raghavan and Schütze textbook appears [1][6].
- **202406.** Stonebraker and Pavlo name Elasticsearch and Solr, both built on Lucene, as the leading text engines [3].
- **20260511 and 20260813.** Pi-Serini pairs a BM25 retriever with a language model (gpt-5.5) and reports 83.1% answer accuracy on BrowseComp-Plus [7]. ReFind indexes raw chat logs lexically and reports a mean accuracy of 58.2 against 53.2 for [HippoRAG 2](../projects/hipporag.md), in the [MemoryAgentBench](../benchmarks/memoryagentbench.md) setting with a GPT-4o-mini backbone [8]. Both first-party. Still moving: [Agentic search over raw data](../trends/agentic-search.md).

## Where sources disagree

**Has embedding search replaced it?** Manning et al. wrote "without rivals" in 2008 [2]; Stonebraker and Pavlo say inverted-index engines, used for exact-match search, "have been supplanted in recent years" by similarity search on embeddings [3]. Two 2026 studies get strong results from lexical retrieval steered by an agent [7][8]. No source read settles it.

**The name.** "Inverted index", "inverted file" and "full-text index" denote the same structure [1][3].

## Related

[BM25](./bm25.md), [tf-idf](./tf-idf.md), [Boolean retrieval](./boolean-retrieval.md), [ranked retrieval](./ranked-retrieval.md), [information retrieval](./information-retrieval.md), [vector space model](./vector-space-model.md), [vector search](./vector-search.md), [dense retrieval](./dense-retrieval.md), [hybrid search](./hybrid-search.md), [web search engine](./web-search-engine.md). Trend and papers: [agentic search](../trends/agentic-search.md), [papers](../papers/agentic-search.md), [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Index**

- [grep](grep.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://nlp.stanford.edu/IR-book/html/htmledition/an-example-information-retrieval-problem-1.html : Manning, Raghavan and Schütze, "Introduction to Information Retrieval", section 1.1 "An example information retrieval problem": dictionary, postings, "inverted file", name redundant; read from the Internet Archive capture of 20241119 because the origin server refused connections (read 20261102 22:14 UTC)
2. https://nlp.stanford.edu/IR-book/html/htmledition/a-first-take-at-building-an-inverted-index-1.html : same book, section 1.2 "A first take at building an inverted index": document frequency, postings sorted by document identifier, "without rivals"; Internet Archive capture of 20241226 (read 20261102 22:13 UTC)
3. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), June 2024, section 2.5: SMART in the 1960s, Elasticsearch and Solr on Lucene, "supplanted" (read 20261102 22:15 UTC)
4. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", author manuscript: Uniterm (Taube et al., 1952), no mention of inverted files (read 20261102 22:12 UTC); venue Proceedings of the IEEE 100, May 2012, from https://api.crossref.org/works/10.1109/JPROC.2012.2189916 (read 20261102 22:51 UTC)
5. https://api.crossref.org/works/10.1145/1132956.1132959 : record and abstract of Zobel and Moffat, "Inverted files for text search engines", ACM Computing Surveys 38(2), issued 20060725 (read 20261102 22:13 UTC)
6. https://api.crossref.org/works/10.1017/CBO9780511809071 : record of the book, Cambridge University Press, issued 20080707 (read 20261102 22:15 UTC)
7. https://arxiv.org/abs/2605.10848 : Hsu, Yang and Lin, "Rethinking Agentic Search with Pi-Serini", submitted 20260511, abstract: 83.1% answer accuracy with gpt-5.5 (first-party; read 20261102 22:14 UTC and 22:41 UTC)
8. https://arxiv.org/abs/2608.12888 : Li et al., ReFind, submitted 20260813, abstract: mean accuracy 58.2 against 53.2 for HippoRAG 2, MemoryAgentBench setting, GPT-4o-mini backbone (first-party; read 20261102 22:14 UTC and 22:41 UTC)
