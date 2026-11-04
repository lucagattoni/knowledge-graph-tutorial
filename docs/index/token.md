---
type: index
kind: concept
aliases: [LLM token, subword token]
updated: 20261102 21:29 UTC
---

# Token

A token is the unit of text that a language model reads and writes, and the unit in which cost and length are counted. This entry says what a token is and why counts of the same text can differ.

## Definition

A tokenizer cuts running text into tokens and maps each to an entry of a fixed vocabulary it learned from a corpus [1]. In modern schemes many tokens are whole words, and others are frequent word parts such as "-er"; an unseen word is built from known parts, and in the worst case from single letters [1]. Anthropic's glossary says tokens can be words, subwords, characters or bytes [2]. The two algorithms in wide use are byte-pair encoding and unigram language modelling [1]. For a [large language model](./large-language-model.md), input length and the [context window](./context-window.md) are counted in tokens, and a provider's price list is per million tokens [3][4].

## How it changed

- **1994.** Sennrich et al. date Gage's byte-pair encoding, a data-compression technique, to 1994 [5].
- **2008.** In [information retrieval](./information-retrieval.md), a token is an instance of a character sequence in one document, a type is the class of equal tokens, and a term is a normalised type kept in the dictionary [8].
- **20150831.** Sennrich, Haddow and Birch adapt byte-pair encoding to split rare words into subword units for machine translation [5][6].
- **20180819.** Kudo and Richardson release SentencePiece, a subword tokenizer trained directly on raw sentences [7].
- **20260731.** Version 3 of a scaling study first posted on 20260729 reports retrieval cost in construction and query tokens and places a crossover at "around 10 million corpus tokens" [9]. See [Graph-based RAG](../trends/graph-based-rag.md).
- **As read 20261102.** Anthropic's documentation says Claude 4.7 and later models use a newer tokenizer that gives about 30 percent more tokens for the same text, and tells users not to reuse counts from earlier models [2][3].

## Where sources disagree

The unit differs. The retrieval textbook counts word-like pieces of a document [8]; the language-model sources count pieces of a learned vocabulary, often smaller than words [1][2]. Even within one provider, the count for the same text changed between model generations [2][3]. A token count is comparable only under the same tokenizer.

## Related

[large language model](./large-language-model.md) · [context window](./context-window.md) · [Transformer](./transformer.md) · [BERT](./bert.md) · [embedding](./embedding.md) · [chunking](./chunking.md) · [information retrieval](./information-retrieval.md) · [tf-idf](./tf-idf.md) · [BM25](./bm25.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Experiments**

- [Experiments](../experiments/README.md)
- [Instruments evidence: the metering gateway](../experiments/evidence/instruments-gateway.md)
- [X2: the index cost of cheap graph builders](../experiments/x2-index-cost.md)

**Index**

- [Context window](context-window.md)
- [Large language model](large-language-model.md)
- [Stemming](stemming.md)
- [Transformer](transformer.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://web.stanford.edu/~jurafsky/slp3/2.pdf : Jurafsky and Martin, "Speech and Language Processing", chapter 2, "Words and Tokens" (draft of August 2026): tokenization, subword tokens, BPE and unigram (read 20261102 21:00 UTC)
2. https://platform.claude.com/docs/en/about-claude/glossary : Claude Platform documentation, glossary entry "Tokens" (read 20261102 21:03 UTC)
3. https://platform.claude.com/docs/en/build-with-claude/token-counting : token counting: estimate, newer tokenizer, about 30 percent more tokens, advice on migration (read 20261102 21:01 UTC)
4. https://platform.claude.com/docs/en/about-claude/pricing : pricing table in dollars per million tokens ("MTok"), long-context billing by tokens (read 20261102 21:01 UTC)
5. https://arxiv.org/pdf/1508.07909 : Sennrich, Haddow, Birch, "Neural Machine Translation of Rare Words with Subword Units" (v5): BPE (Gage, 1994) as a compression algorithm adapted to word segmentation (read 20261102 21:03 UTC)
6. https://arxiv.org/abs/1508.07909 : the same paper, submission history (v1 20150831) (read 20261102 21:00 UTC)
7. https://arxiv.org/abs/1808.06226 : Kudo and Richardson, "SentencePiece", v1 20180819, abstract (read 20261102 21:00 UTC)
8. https://nlp.stanford.edu/IR-book/html/htmledition/tokenization-1.html : Manning, Raghavan, Schütze, "Introduction to Information Retrieval" (2008), section 2.2.1; the original host did not answer, so the text was read in the Internet Archive copy https://web.archive.org/web/20250108161907/https://nlp.stanford.edu/IR-book/html/htmledition/tokenization-1.html (read 20261102 21:25 UTC)
9. https://arxiv.org/abs/2607.26497v3 : Wang and 7 more, "BM25 Wins at Scale" (v3 20260731; v1 of 20260729 had the title "Which RAG Paradigm Wins at Scale?"), abstract: "construction and query tokens", "corpus tokens" (read 20261102 21:25 UTC)
