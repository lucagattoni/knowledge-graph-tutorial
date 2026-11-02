---
type: index
kind: system
aliases: [Bidirectional Encoder Representations from Transformers]
updated: 20261102 21:16 UTC
---

# BERT

BERT is a pretrained language model, first posted as a preprint in October 2018, that reads text in both directions and is adapted to a task by adding one output layer. Later work used it to rerank search results and to build text embeddings.

## Definition

Devlin, Chang, Lee and Toutanova present BERT, "Bidirectional Encoder Representations from Transformers", as a language representation model that pretrains deep bidirectional representations from unlabeled text, using context from both directions in every layer. A pretrained BERT is fine-tuned for a task by adding one output layer. The authors report state-of-the-art results on eleven tasks, among them a GLUE score of 80.5%, 86.7% on MultiNLI and F1 of 93.2 on SQuAD v1.1 (first-party) [1]. It is built on the [Transformer](./transformer.md).

## How it changed

- **20181011.** The preprint appears on arXiv [1]. NAACL printed it in June 2019, pages 4171-4186 [2]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20190113.** Nogueira and Cho use BERT to rerank passages and report the top entry on the MS MARCO passage-retrieval leaderboard at the time (first-party) [3]; the figures are on the benchmark page. See [reranking](./reranking.md) and [MS MARCO](../benchmarks/ms-marco.md).
- **20190827.** Sentence-BERT notes that feeding sentence pairs to BERT makes finding the most similar pair among 10,000 sentences take about 65 hours, and gets it to about 5 seconds with [embeddings](./embedding.md) that keep BERT's accuracy (first-party) [4].
- **20191025.** Google says it is applying BERT to Search ranking, helping with one in ten U.S. English searches (first-party) [5].
- **20201013.** Lin, Nogueira and Yates survey transformers for text ranking, with BERT as the best-known example, covering reranking and [dense retrieval](./dense-retrieval.md) [6].
- **20241218.** ModernBERT presents a new encoder-only model, noting that encoders like BERT "offer a great performance-size tradeoff" for retrieval and classification [7].

## Where sources disagree

No disagreement found in the sources read, beyond dating: the preprint is 2018 [1] and the proceedings 2019 [2].

## Related

[Transformer](./transformer.md), [embedding](./embedding.md), [reranking](./reranking.md), [dense retrieval](./dense-retrieval.md), [large language model](./large-language-model.md), [mean reciprocal rank](./mean-reciprocal-rank.md). Datasets and benchmarks: [MS MARCO dataset](../datasets/ms-marco.md), [MS MARCO benchmark](../benchmarks/ms-marco.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [Language models meet retrieval (2018-2022)](../history/language-models-meet-retrieval.md)

**Index**

- [Dense retrieval](dense-retrieval.md)
- [Embedding](embedding.md)
- [Fine-tuning](fine-tuning.md)
- [Large language model](large-language-model.md)
- [Learning to rank](learning-to-rank.md)
- [Named-entity recognition](named-entity-recognition.md)
- [Reranking](reranking.md)
- [Supervised fine-tuning](supervised-fine-tuning.md)
- [Token](token.md)
- [Transformer](transformer.md)
- [Word sense disambiguation](word-sense-disambiguation.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/1810.04805 : Devlin et al., "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", v1 20181011, v2 20190524; abstract (read 20261102 20:49 UTC)
2. https://aclanthology.org/N19-1423/ : NAACL 2019, June 2019, pages 4171-4186, DOI 10.18653/v1/N19-1423 (read 20261102 20:46 UTC)
3. https://arxiv.org/abs/1901.04085 : Nogueira and Cho, "Passage Re-ranking with BERT", v1 20190113 (read 20261102 20:46 UTC)
4. https://arxiv.org/abs/1908.10084 : Reimers and Gurevych, "Sentence-BERT", v1 20190827 (read 20261102 20:46 UTC)
5. https://blog.google/products/search/search-language-understanding-bert/ : Google, 20191025, BERT in Search ranking (read 20261102 20:46 UTC)
6. https://arxiv.org/abs/2010.06467 : Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking: BERT and Beyond", v1 20201013 (read 20261102 20:46 UTC)
7. https://arxiv.org/abs/2412.13663 : Warner et al., "Smarter, Better, Faster, Longer" (ModernBERT), 14 authors, v1 20241218 (read 20261102 20:46 UTC)
