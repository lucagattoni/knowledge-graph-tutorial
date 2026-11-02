---
type: index
kind: concept
aliases: [ODQA, open-domain QA, OpenQA]
updated: 20261102 22:49 UTC
---

# Open-domain question answering

This entry says what "open-domain" contrasts with and how the setting moved from TREC snippets to retrievers and generators. The wider task is in [question answering](./question-answering.md).

## Definition

Zhu et al. say open-domain question answering "aims to answer a question in the form of natural language based on large-scale unstructured documents"; machine reading comprehension, by contrast, is given the passage [1]. Lee et al. put the split as evidence that "must be retrieved from an open corpus, rather than being given as input" [2]. Zhu et al. call the modern design "Retriever-Reader": a retriever finds documents and a reader infers the answer [1].

## How it changed

- **1961.** Baseball, designed this year, worked on a restricted domain with stored data [1]. See [The advent](../history/advent.md).
- **1999.** The TREC-8 QA track had 200 test questions [4]. Zhu et al. say open-domain QA was first defined there, with five snippets returned, and exact short answers from TREC-11 in 2002 [1]. See [The Web changes data and search](../history/the-web.md).
- **20170331.** Chen et al. use Wikipedia as the only source and combine retrieval with comprehension [3]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20190601.** Lee et al. learn retriever and reader together over Wikipedia; on genuine information-seeking questions, learned retrieval beats BM25 by up to 19 exact-match points (first-party) [2]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20200210.** Roberts et al. fine-tune models to answer "without access to any external context or knowledge", competitive with systems that retrieve (first-party) [5]. REALM, posted the same day, beats earlier systems by 4-16% absolute on three Open-QA benchmarks (first-party) [6].
- **Later in 2020.** DPR and RAG followed; their dates are in [question answering](./question-answering.md).

## Where sources disagree

**Is retrieval part of the definition?** Zhu et al. say the system usually first searches for documents [1]. Lee et al. write that "the source of evidence is a modeling choice rather than a part of the task definition", and list a model with no evidence under open-domain QA [2]. Roberts et al. use "open-domain systems" for systems that retrieve; whether their no-retrieval model counts is unstated in the abstract [5].

**Which collection.** Zhu et al. allow local repositories and the web [1]; Chen et al. use Wikipedia only [3].

## Related

[question answering](./question-answering.md) · [multi-hop question answering](./multi-hop-question-answering.md) · [knowledge-base question answering](./knowledge-base-question-answering.md) · [retrieval-augmented generation](./retrieval-augmented-generation.md) · [Natural Questions](../benchmarks/natural-questions.md) · [KILT](../benchmarks/kilt.md) · [foundation papers](../papers/foundations.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Datasets**

- [Natural Questions](../datasets/natural-questions.md)
- [PopQA](../datasets/popqa.md)

**Benchmarks**

- [KILT](../benchmarks/kilt.md)
- [Natural Questions](../benchmarks/natural-questions.md)

**Index**

- [Distant supervision](distant-supervision.md)
- [Exact match](exact-match.md)
- [Slot filling](slot-filling.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/2101.00774v3 : Zhu et al., "Retrieving and Reading: A Comprehensive Survey on Open-domain Question Answering", v1 20210104 (v3 read): abstract, sections 1 and 2 (read 20261102 22:09 UTC)
2. https://arxiv.org/pdf/1906.00300v3 : Lee, Chang, Toutanova, "Latent Retrieval for Weakly Supervised Open Domain Question Answering", v1 20190601 (v3 read): introduction, section 2.1, table 1 (first-party; read 20261102 22:09 UTC)
3. https://arxiv.org/abs/1704.00051 : Chen, Fisch, Weston, Bordes, "Reading Wikipedia to Answer Open-Domain Questions", v1 20170331, abstract (read 20261102 22:09 UTC)
4. https://trec.nist.gov/data/qa/t8_qadata.html : NIST, TREC-8 (1999) QA data: 200 questions, TREC disks 4 and 5 minus the Congressional Record (read 20261102 22:10 UTC)
5. https://arxiv.org/abs/2002.08910 : Roberts, Raffel, Shazeer, "How Much Knowledge Can You Pack Into the Parameters of a Language Model?", v1 20200210, abstract (first-party; read 20261102 22:09 UTC)
6. https://arxiv.org/abs/2002.08909 : Guu et al. (5 authors), "REALM", v1 20200210, abstract (first-party; read 20261102 22:09 UTC)
