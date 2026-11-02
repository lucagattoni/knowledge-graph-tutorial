---
type: index
kind: concept
aliases: [Boolean search]
updated: 20261102 21:28 UTC
---

# Boolean retrieval

This entry answers what exact-match Boolean search is, why it was the first style of computer search, and where it still sits next to ranked methods. It does not describe how ranked scores are computed. The one historical source read is a single survey.

## Definition

In Boolean retrieval a query is a logical combination of terms (words), and the result is the set of documents that exactly match that combination [1]. Documents either match or do not, so the result is a set without an order. Sanderson and Croft contrast this with ranked retrieval, where every document gets a score and the top ones are returned [1]. Both the electro-mechanical and the first computer search systems worked in the Boolean style [1].

## How it changed

- **1918 and the 1920s to 1930s.** Mechanical search devices already matched exact patterns: a 1918 patent describes catalogue cards with holes that, laid over each other, showed whether entries had a particular combination of categories, and Goldberg's machines matched patterns on microfilm [1]. See [The advent](../history/advent.md).
- **Late 1940s and 1950.** The first computer searches appear in the late 1940s, and the term "information retrieval" is first used in March 1950 [1].
- **1957 to 1959.** Luhn proposed giving each document a relevance score (reference dated 1957) [1]. Maron, Kuhns and Ray (technical memorandum, June 1959) tested a ranked method on 200 documents and 39 queries and found it better than Boolean search [1]. Luhn's word-frequency remark is dated differently (see below) [1].
- **1960s to early 1990s.** Experiments over the following decades kept showing ranked retrieval to be more effective, yet almost all commercial systems used Boolean search [1].
- **Early to mid 1990s.** Sanderson and Croft date the change to this period, naming WESTLAW's WIN system and the growth of web search engines [1]. See [The Web changes data and search](../history/the-web.md).
- **Today.** Boolean combinations remain in at least one search library. The Lucene 10.0.0 API describes `BooleanQuery` as matching "boolean combinations of other queries", and its `FILTER` clause works like a required clause "except that these clauses do not participate in scoring" [2][3]. So an exact-match condition can sit beside a score [2][3]. Use in other engines is unstated in the sources read.

## Where sources disagree

One date inconsistency inside the one source: Sanderson and Croft's references date Luhn's score-based proposal 1957 and his word-frequency paper 1958, but the text puts the word-frequency remark in "the same year" as the June 1959 memorandum [1]. Which is right is unstated.

## Related

[ranked retrieval](./ranked-retrieval.md) · [information retrieval](./information-retrieval.md) · [BM25](./bm25.md) · [tf-idf](./tf-idf.md) · [vector space model](./vector-space-model.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Knowledge systems: boom and bust](../history/knowledge-systems.md)

**Index**

- [BM25](bm25.md)
- [Exact match](exact-match.md)
- [Information retrieval](information-retrieval.md)
- [Inverted index](inverted-index.md)
- [Ranked retrieval](ranked-retrieval.md)
- [Stemming](stemming.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE 100, 2012: Boolean retrieval defined, 1918 and 1928 devices, Mooers 1950, Luhn and Maron et al., commercial Boolean systems until the early to mid 1990s, references [19] to [21] (read 20261102 20:45 UTC; re-read 20261102 21:23 UTC)
2. https://lucene.apache.org/core/10_0_0/core/org/apache/lucene/search/BooleanQuery.html : Lucene 10.0.0 API, `BooleanQuery` (read 20261102 20:52 UTC)
3. https://lucene.apache.org/core/10_0_0/core/org/apache/lucene/search/BooleanClause.Occur.html : Lucene 10.0.0 API, `BooleanClause.Occur`, `FILTER` (read 20261102 20:52 UTC)
