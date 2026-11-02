---
type: index
kind: concept
aliases: [PRP]
updated: 20261102 21:24 UTC
---

# Probability ranking principle

The probability ranking principle says that a search system should show documents in decreasing order of their probability of relevance [1]. This entry gives the statement, the dated changes, and a dispute about who first stated it.

## Definition

Robertson and Zaragoza state it for a system that cannot know whether a document is relevant and holds only evidence about it. If retrieved documents are "ordered by decreasing probability of relevance on the data available", the effectiveness is "the best that can be obtained for the data" [1]. They add that it can be justified under further assumptions for specific effectiveness measures, that it is not completely general, and that it is "safe for the case considered: an individual user" [1].

## How it changed

- **196007.** Maron and Kuhns propose probabilistic indexing: a machine derives for each document a number measuring the probability that it satisfies a request, and returns documents ranked by that number [2]. See [the advent era](../history/advent.md).
- **Early 1970s.** Cooper at Berkeley develops the principle independently and does not publish it, according to a 2025 interview article [3].
- **197704.** Robertson publishes "The probability ranking principle in IR" in the Journal of Documentation. The abstract says the principle had been "brought into question by Cooper", can be justified under certain assumptions, and is not valid where they fail; the main problem is that it treats each document independently [4]. See [formal foundations](../history/formal-foundations.md).
- **198907.** Fuhr derives optimum polynomial retrieval functions from the principle [5]. See [knowledge systems](../history/knowledge-systems.md).
- **2009.** Robertson and Zaragoza start the derivation of [BM25](./bm25.md) from the principle and keep it "for the remainder of this work" [1].

## Where sources disagree

Who defined it. Sanderson and Croft write that Robertson "defined" the principle [6]. Robertson's own 1977 abstract treats it as already questioned by Cooper [4]. The 2025 interview article says Cooper developed it first and unpublished, and quotes Robertson on "Cooper's Probability Ranking Principle" [3]. This entry names Robertson's paper as the first publication read, not as the origin.

## Related

Entries: [ranked retrieval](./ranked-retrieval.md), [BM25](./bm25.md), [tf-idf](./tf-idf.md), [vector space model](./vector-space-model.md), [information retrieval](./information-retrieval.md), [relevance feedback](./relevance-feedback.md), [learning to rank](./learning-to-rank.md). Pages: [foundational papers](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)

**Index**

- [BM25](bm25.md)
- [Ranked retrieval](ranked-retrieval.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.staff.city.ac.uk/~sb317/papers/foundations_bm25_review.pdf : Robertson and Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond", Foundations and Trends in Information Retrieval 3(4), 2009: sections 2.3 and 2.4 (read 20261102 20:55 UTC)
2. https://api.crossref.org/works/10.1145/321033.321035 : Maron and Kuhns, "On Relevance, Probabilistic Indexing and Information Retrieval", Journal of the ACM 7(3), July 1960: abstract (read 20261102 21:00 UTC)
3. https://informationmatters.org/2025/04/ir-meets-ai-looking-back-looking-forward-a-conversation-with-stephen-robertson-pioneer-of-information-retrieval/ : Shalini Urs, interview article with Stephen Robertson, 17 April 2025 (the Cooper statement is the article's narration; the quoted words are Robertson's) (read 20261102 20:59 UTC)
4. https://api.crossref.org/works/10.1108/eb026647 : Robertson, Journal of Documentation 33(4), 294-304, April 1977: record and abstract (read 20261102 20:56 UTC)
5. https://api.crossref.org/works/10.1145/65943.65944 : Fuhr, ACM Transactions on Information Systems 7(3), 183-204, July 1989: record and abstract (read 20261102 21:00 UTC)
6. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE, 2012: section "1970s" (read 20261102 20:59 UTC)
