---
type: index
kind: concept
aliases: [VSM, vector space retrieval]
updated: 20261102 21:25 UTC
---

# Vector space model

This entry says what the vector space model is, who proposed which part of it, and how it relates to learned [embeddings](./embedding.md). It answers where sparse term vectors come from and why the idea outlived its formulas.

## Definition

In the account of Lin, Nogueira and Yates, the vector space model represents documents and queries alike as "bags of words" using sparse vectors under a term weighting scheme such as [tf-idf](./tf-idf.md). Similarity between document and query is the cosine, or more generally an inner product [1]. N, the number of dimensions, is the number of unique terms in the collection [2]. Salton, Wong and Yang (1975) is "frequently cited" as the proposal [1].

## How it changed

- **1963 and 1968.** Sanderson and Croft place the first proposal to view documents and queries as vectors in Switzer's 1963 report, and the cosine coefficient in Salton's 1968 book [2].
- **1960s.** Salton leads an IR group, first at Harvard, then at Cornell [2]. Stonebraker and Pavlo date SMART to the 1960s and say it pioneered the model [3]. See [The advent](../history/advent.md).
- **197511.** Salton, Wong and Yang publish "A vector space model for automatic indexing" in *Communications of the ACM* 18(11) [4]. See [Formal foundations](../history/formal-foundations.md).
- **1980s to mid-1990s.** Weighting variants appear; latent semantic indexing shrinks the space by singular-value decomposition [2]. See [Knowledge systems: boom and bust](../history/knowledge-systems.md).
- **1994.** [BM25](./bm25.md) arrives. Lin et al. write that its inner products over sparse bag-of-words vectors are "operationally identical to the vector space model" [1].
- **2020.** Karpukhin et al. call TF-IDF and BM25 "traditional sparse vector space models". Their dense learned vectors beat "a strong Lucene-BM25 system" by 9% to 19% absolute on top-20 passage accuracy (first-party) [5]. See [dense retrieval](./dense-retrieval.md) and [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **202406.** Stonebraker and Pavlo call the model "now nearly universal in modern search engines" [3].

## Where sources disagree

**What the 1975 paper proposed.** Sanderson and Croft credit Switzer with the vector view and Salton with cosine, and say the 1975 paper synthesised the group's work [2]. Lin et al. say it "did not happen all at once" [1]. The paper's abstract is about space density and choosing an indexing vocabulary [4].

**Still used?** Sanderson and Croft: Salton's ranking formulas "are rarely used", yet the vector view "is still common" [2]. Stonebraker and Pavlo: "nearly universal" [3]. *Reading:* the two fit if the claim is about the view, not the formulas.

## Related

[tf-idf](./tf-idf.md) · [BM25](./bm25.md) · [information retrieval](./information-retrieval.md) · [embedding](./embedding.md) · [dense retrieval](./dense-retrieval.md) · [vector search](./vector-search.md) · [foundation papers](../papers/foundations.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [The advent: machines that hold knowledge](../history/advent.md)

**Index**

- [Approximate nearest neighbour](approximate-nearest-neighbour.md)
- [BM25](bm25.md)
- [Boolean retrieval](boolean-retrieval.md)
- [Embedding](embedding.md)
- [Information retrieval](information-retrieval.md)
- [Inverted index](inverted-index.md)
- [Probability ranking principle](probability-ranking-principle.md)
- [Ranked retrieval](ranked-retrieval.md)
- [Relevance feedback](relevance-feedback.md)
- [tf-idf](tf-idf.md)
- [Vector search](vector-search.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/2010.06467 : Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking: BERT and Beyond", section 1.2.1 and footnote 21: definition, SMART, Salton et al. 1975 "frequently cited", BM25 "operationally identical" (read 20261102 21:05 UTC)
2. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE 100, 2012: Salton's group, Switzer 1963, Salton 1968, 1975 paper, LSI, "rarely used" (read 20261102 21:00 UTC)
3. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), June 2024, section 2.5: SMART and the vector space model, "now nearly universal" (read 20261102 21:00 UTC)
4. https://api.crossref.org/works/10.1145/361219.361220 : Crossref record with the publisher's abstract: Salton, Wong, Yang, CACM 18(11), 613-620, November 1975 (read 20261102 21:01 UTC)
5. https://arxiv.org/abs/2004.04906 : Karpukhin et al., "Dense Passage Retrieval for Open-Domain Question Answering", abstract, v1 20200410 (read 20261102 21:24 UTC)
