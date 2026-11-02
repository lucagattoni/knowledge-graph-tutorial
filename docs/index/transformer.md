---
type: index
kind: concept
aliases: [Transformer architecture, Transformer model]
updated: 20261102 21:29 UTC
---

# Transformer

The Transformer is the neural network design behind BERT and today's large language models. This entry gives its definition and dates, and compares two sources that date its link to retrieval differently.

## Definition

Vaswani et al. propose "a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely" [1]. They first applied it to machine translation, with a new best result on English-German and a new single-model best on English-French in WMT 2014 (first-party) [1]. In the form used for language models, each input [token](./token.md) is turned into an [embedding](./embedding.md) and passes up through layers of multi-head attention and feed-forward blocks; the network predicts the next token from the tokens before it [2]. A 2026 textbook draft calls it "the standard architecture for building large language models" [2].

## How it changed

- **20170612.** The paper "Attention Is All You Need" appears on arXiv (v1); it is published in the proceedings of NIPS 2017 (volume 30) [1][3]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20181011.** Devlin et al. post [BERT](./bert.md), "Bidirectional Encoder Representations from Transformers", with new best results on eleven language tasks (first-party) [4]. Lin et al. date the Transformer to June 2017 and BERT to October 2018 [5]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **201910 and 201911.** Google (October) and Microsoft (November) report that they use BERT or large transformer models in web search, as quoted by Lin et al. [5].
- **20231201.** Gu and Dao write that foundation models are "almost universally based on the Transformer" and propose Mamba, a model without attention that they say matches Transformers twice its size (first-party; v1 abstract) [6].

## Where sources disagree

**Two different starts.** The sources date different things, so this is a difference of subject, not a contradiction. Gao et al. date the inception of retrieval-augmented generation: it "coincided with the rise of the Transformer architecture" [7]. Lin et al. date the change in text ranking: with BERT in October 2018, "everything changed, nearly overnight" [5].
**Replacement.** Mamba's authors claim it beats Transformers of the same size [6]; no source read reports that any other design has replaced the Transformer.

## Related

[BERT](./bert.md) · [large language model](./large-language-model.md) · [token](./token.md) · [embedding](./embedding.md) · [dense retrieval](./dense-retrieval.md) · [reranking](./reranking.md) · [retrieval-augmented generation](./retrieval-augmented-generation.md) · [MS MARCO](../benchmarks/ms-marco.md) · [foundation papers](../papers/foundations.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [Language models meet retrieval (2018-2022)](../history/language-models-meet-retrieval.md)

**Index**

- [BERT](bert.md)
- [Context window](context-window.md)
- [Fine-tuning](fine-tuning.md)
- [Large language model](large-language-model.md)
- [Token](token.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/1706.03762 : Vaswani et al., "Attention Is All You Need": abstract (28.4 BLEU English-German "improving over the existing best results"; English-French "a new single-model state-of-the-art"), submission history (v1 20170612) (read 20261102 21:25 UTC)
2. https://web.stanford.edu/~jurafsky/slp3/7.pdf : Jurafsky and Martin, "Speech and Language Processing", chapter 7, "Transformers and Pretraining" (draft of August 2026): opening paragraph, Figure 7.1 (read 20261102 21:04 UTC)
3. https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html : NeurIPS proceedings page: Advances in Neural Information Processing Systems 30 (NIPS 2017) (read 20261102 21:01 UTC)
4. https://arxiv.org/abs/1810.04805 : Devlin et al., "BERT", submitted 20181011, abstract (read 20261102 21:00 UTC)
5. https://arxiv.org/pdf/2010.06467 : Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking: BERT and Beyond", section 1: dates of the Transformer and BERT ("arrived on the scene in October 2018", section 1.2.5), Google and Microsoft reports (read 20261102 21:00 UTC; BERT wording re-read 20261102 21:27 UTC)
6. https://arxiv.org/abs/2312.00752 : Gu and Dao, "Mamba: Linear-Time Sequence Modeling with Selective State Spaces", abstract of v1 (20231201), compared with v2 (31 May 2024): the quoted wording is the same (read 20261102 21:25 UTC)
7. https://arxiv.org/pdf/2312.10997 : Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey", v5 of 20240327, introduction (read 20261102 21:03 UTC; "coincided" sentence re-read 20261102 21:27 UTC)
