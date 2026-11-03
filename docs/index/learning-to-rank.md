---
type: index
kind: concept
aliases: [LTR, machine-learned ranking]
updated: 20261102 21:33 UTC
---

# Learning to rank

This entry says what learning to rank means in text search, when it began, and how it differs from the neural rankers that followed. It marks the step between hand-tuned scoring such as BM25 and neural re-rankers.

## Definition

Learning to rank is a family of techniques, beginning in the late 1980s, that train a supervised model to order search results from many hand-made features such as term statistics, text properties, link scores and user behaviour; a BM25 score is often one feature [1]. Lin, Nogueira and Yates say the name should not be read as "supervised machine-learning approaches to ranking": it refers to techniques of one period and is "characterized by its use of numerous sparse, usually hand-crafted features" [1]. They sort its methods by loss function into pointwise, pairwise and listwise [1].

## How it changed

- **Late 1980s.** Early examples: Fuhr (1989), Wong et al. (1993), Gey (1994) [1].
- **2002.** Joachims trains a Support Vector Machine ranker from search-engine click logs instead of expert judgments (SIGKDD 2002) [2].
- **August 2005.** Burges et al. publish RankNet, a neural network that models the ranking function and is trained by gradient descent (technical report MSR-TR-2005-06) [3].
- **April 2007.** LETOR 1.0, a benchmark package for learning to rank, is released; version 4.0 followed in July 2009 [4].
- **June 2010.** Burges describes LambdaMART; an ensemble of LambdaMART rankers won Track 1 of the 2010 Yahoo! Learning To Rank Challenge [5].
- **Early 2010s.** Lin et al. date the "zenith" here, with tree ensembles [1]. See [knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20190113.** Nogueira and Cho re-rank passages with BERT and top the MS MARCO passage leaderboard, 27% better in relative MRR@10 [6]. Lin et al. say transformer rankers "would not generally be regarded as a learning-to-rank method" [1]. See [language models meet retrieval](../history/language-models-meet-retrieval.md).

## Where sources disagree

When it became effective. Lin et al. begin the approach in the late 1980s with Fuhr [1]. Sanderson and Croft also credit Fuhr with the idea, say it was followed up soon after, and add that it "only became truly effective" with web query logs and better learning methods in the 2000s [7]. The two accounts name the same origin and differ on the date from which the approach worked.

## Related

- Entries: [BM25](./bm25.md), [reranking](./reranking.md), [BERT](./bert.md), [ranked retrieval](./ranked-retrieval.md), [information retrieval](./information-retrieval.md), [relevance feedback](./relevance-feedback.md), [PageRank](./pagerank.md), [TREC](./trec.md), [mean reciprocal rank](./mean-reciprocal-rank.md).
- Data and papers: [MS MARCO data](../datasets/ms-marco.md), [MS MARCO benchmark](../benchmarks/ms-marco.md), [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [The semantic web and linked data](../history/semantic-web.md)

**Index**

- [AUROC](auroc.md)
- [Information retrieval](information-retrieval.md)
- [nDCG](ndcg.md)
- [Probability ranking principle](probability-ranking-principle.md)
- [Reciprocal rank fusion](reciprocal-rank-fusion.md)
- [Reranking](reranking.md)
- [Web search engine](web-search-engine.md)

<!-- END GENERATED: appears-in -->

## Sources

Read times are UTC.

1. https://arxiv.org/pdf/2010.06467 : Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking: BERT and Beyond", Section 1.2.3 (definition, early examples, features, loss types, zenith, scope) (read 20261102 20:45 and 21:26)
2. https://www.cs.cornell.edu/people/tj/publications/joachims_02c.pdf : Joachims, "Optimizing Search Engines using Clickthrough Data", SIGKDD 2002, Edmonton, abstract and copyright line (read 20261102 20:47)
3. https://www.microsoft.com/en-us/research/publication/learning-to-rank-using-gradient-descent/ : Burges et al., "Learning to Rank using Gradient Descent", MSR-TR-2005-06, August 2005, abstract; read via an archived copy (https://web.archive.org/web/2023/https://www.microsoft.com/en-us/research/publication/learning-to-rank-using-gradient-descent/), because the live page returned a bot-check page to a plain fetch (read 20261102 20:45 and 21:27)
4. https://arxiv.org/abs/1306.2597 : Qin and Liu, "Introducing LETOR 4.0 Datasets", release dates of versions 1.0 to 4.0 (read 20261102 20:45)
5. https://www.microsoft.com/en-us/research/publication/from-ranknet-to-lambdarank-to-lambdamart-an-overview/ : Burges, "From RankNet to LambdaRank to LambdaMART: An Overview", MSR-TR-2010-82, June 2010; read via an archived copy (https://web.archive.org/web/2023/https://www.microsoft.com/en-us/research/publication/from-ranknet-to-lambdarank-to-lambdamart-an-overview/), because the live page returned a bot-check page to a plain fetch (read 20261102 20:51 and 21:27)
6. https://arxiv.org/abs/1901.04085 : Nogueira and Cho, "Passage Re-ranking with BERT", v1 20190113 (read 20261102 20:45 and 20:47)
7. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE 2012, section "Learning to rank" (read 20261102 20:54 and 21:26)
