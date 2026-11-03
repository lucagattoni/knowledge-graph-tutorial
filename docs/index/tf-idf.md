---
type: index
kind: concept
aliases: [TFIDF, term frequency-inverse document frequency]
updated: 20261102 21:29 UTC
---

# tf-idf

tf-idf is the classic way to weight a word in a document for search. This entry gives the definition, the dates of its two parts, and where sources differ.

## Definition

tf-idf is the product of two numbers for a term in a document: the term frequency (tf), how often the term occurs in that document, and the inverse document frequency (idf), which is higher the fewer documents contain the term [1]. In one standard textbook form, tf is 1 + log10 of the count (0 if absent), idf is log10 of N over the document frequency (N documents in all), and the weight is their product [1]. The weight is highest when a term occurs often in few documents, and lowest when it occurs in nearly all [2]. The idf part comes from Spärck Jones (1972) [1][3]. Unlike [dense retrieval](./dense-retrieval.md), it is sparse [1].

## How it changed

- **1958.** Luhn suggests that word frequency measures significance, later called term frequency weighting (year per its reference list) [3].
- **1972.** Spärck Jones publishes the idf idea in the Journal of Documentation 28(1): less common words refer to more specific concepts and weigh more [3][4]. See [Formal foundations](../history/formal-foundations.md).
- **1973 to 1975.** Combining the two weights was quickly adopted (Salton and Yang, 1973); the [vector space model](./vector-space-model.md) followed in 1975 [3].
- **1980s to mid-1990s.** Many variants appeared; Salton and Buckley reviewed many [3]. See [Knowledge systems](../history/knowledge-systems.md).
- **2009.** Robertson and Zaragoza show that, with no relevance information, the weight behind [BM25](./bm25.md) is "a close approximation to classical idf" [5].
- **20260401.** Version 4 of an agentic-RAG survey describes "naive" [RAG](./retrieval-augmented-generation.md) as keyword retrieval with TF-IDF and BM25 [6]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **As read 20261102.** The Jurafsky and Martin draft (August 2026) still calls the cosine of sparse tf-idf vectors "the classic method" [1]; FalkorDB's documentation says its full-text scores are TF-IDF [7].

## Where sources disagree

**The formula.** The textbook notes a tf variant, log10 of count plus 1 [1]. Robertson and Zaragoza give an idf form with 0.5 added to the counts [5]. Many variants were produced [3]; there is no single tf-idf.

**What naive RAG retrieves.** Gao et al. describe chunks encoded as vectors [8]; the 2026 survey says TF-IDF and BM25 keyword retrieval [6].

## Related

[BM25](./bm25.md) · [vector space model](./vector-space-model.md) · [information retrieval](./information-retrieval.md) · [dense retrieval](./dense-retrieval.md) · [FalkorDB](../projects/falkordb.md) · [foundation papers](../papers/foundations.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)

**Projects**

- [FalkorDB](../projects/falkordb.md)

**Datasets**

- [2WikiMultiHopQA](../datasets/2wikimultihopqa.md)
- [HotpotQA](../datasets/hotpotqa.md)

**Benchmarks**

- [GraphRAG-Bench (Xiao)](../benchmarks/graphrag-bench-xiao.md)

**Index**

- [BM25](bm25.md)
- [Boolean retrieval](boolean-retrieval.md)
- [Dense retrieval](dense-retrieval.md)
- [Information retrieval](information-retrieval.md)
- [Inverted index](inverted-index.md)
- [Probability ranking principle](probability-ranking-principle.md)
- [Ranked retrieval](ranked-retrieval.md)
- [Retrieval-augmented generation](retrieval-augmented-generation.md)
- [Stemming](stemming.md)
- [Token](token.md)
- [Vector space model](vector-space-model.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://web.stanford.edu/~jurafsky/slp3/11.pdf : Jurafsky and Martin, "Speech and Language Processing", chapter 11 (draft of August 2026), sections 11.1.1 and 11.1.2: sparse vectors, tf, idf, tf-idf formulas, footnote on the variant (read 20261102 21:03 UTC)
2. https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html : Manning, Raghavan, Schütze, "Introduction to Information Retrieval" (2008), section 6.2.2; the original host did not answer, so the text was read in the Internet Archive copy https://web.archive.org/web/20250312161632/https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html (read 20261102 21:25 UTC)
3. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE 100, 2012: Luhn, Spärck Jones, combination of tf and idf, Salton and Yang, Salton and Buckley, reference list (read 20261102 21:00 UTC)
4. https://api.crossref.org/works/10.1108/eb026526 : Crossref record: Spärck Jones, "A statistical interpretation of term specificity and its application in retrieval", Journal of Documentation 28(1), 1972, pages 11-21 (read 20261102 21:00 UTC)
5. https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf : Robertson and Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond", 2009, formula 3.3 and the sentence before it (read 20261102 21:03 UTC)
6. https://arxiv.org/pdf/2501.09136 : Singh et al., "Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG", v4 of 20260401, section 2.3.1 and Table 1 (read 20261102 21:03 UTC)
7. https://docs.falkordb.com/cypher/indexing/fulltext-index.md : FalkorDB documentation, full-text index: scores are TF-IDF (read 20261102 21:03 UTC)
8. https://arxiv.org/pdf/2312.10997 : Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey", v5 of 20240327, naive RAG paragraph (read 20261102 21:03 UTC)
