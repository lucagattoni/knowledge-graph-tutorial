---
type: index
kind: concept
aliases: [QA]
updated: 20261102 21:25 UTC
---

# Question answering

This entry answers what question answering is and how it differs from document search. It follows the task from TREC to retrieval plus a reader, and then to retrieval-augmented generation. Where the sources define the answer differently, it says so.

## Definition

Question answering (QA) is the task of returning an answer to a natural-language question, not a list of documents. Zhu et al. say open-domain QA "aims to answer a question in the form of natural language based on large-scale unstructured documents" [1]. Voorhees describes the TREC track as large-scale evaluation of this task: systems return short pieces of text that contain the answer [2]. Chen et al. give the narrowest form: with Wikipedia as the only source, "the answer to any factoid question is a text span in a Wikipedia article" [3]. Zhu et al. call the modern design "Retriever-Reader" [1].

## How it changed

- **1964.** Gutierrez and Sequeda list Raphael's SIR as a milestone under "Retrieving information from unstructured sources". They call it semantic information retrieval; that it was a question-answering system is **unstated** in that source [4]. See [The advent](../history/advent.md).
- **1992 and 1999.** NIST's TREC started in 1992 and later "introduced evaluations for open-domain question answering", with no year on the overview page [5]. NIST's QA data list begins with "TREC-8 (1999)" [6]. The TREC-8 test set had 200 questions over TREC disks 4 and 5 without the Congressional Record [7]. See [The Web changes data and search](../history/the-web.md).
- **2001.** Voorhees's article on the track appeared [2]. Sanderson and Croft trace later natural-language question work to this task [8].
- **201102.** IBM's Watson beat two former Jeopardy! champions; IBM says it ran on DeepQA (first-party) [9]. See [The semantic web and linked data](../history/semantic-web.md).
- **2016 and 2017.** SQuAD was published at EMNLP 2016 [10]. Chen et al. (20170331) combine retrieval with comprehension [3]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **2020.** Karpukhin et al. (20200410) learn a dense retriever for open-domain QA [11]. Lewis et al. (20200522) report that retrieval-augmented generation set the state of the art on three open-domain QA tasks (first-party) [12]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).

## Where sources disagree

**What the answer is drawn from.** Zhu et al. define open-domain QA over "unstructured documents" [1]; TREC returned text snippets [2]; Chen et al. a span [3]. No source read gives one definition for the whole field.

**When TREC began QA.** The overview names no year [5]; the data list starts at 1999 [6].

## Related

[information retrieval](./information-retrieval.md) · [TREC](./trec.md) · [multi-hop question answering](./multi-hop-question-answering.md) · [retrieval-augmented generation](./retrieval-augmented-generation.md) · [dense retrieval](./dense-retrieval.md) · [Natural Questions](../benchmarks/natural-questions.md) · [HotpotQA](../benchmarks/hotpotqa.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [The semantic web and linked data](../history/semantic-web.md)
- [The Web changes data and search](../history/the-web.md)

**Benchmarks**

- [LC-QuAD](../benchmarks/lc-quad.md)

**Index**

- [Disconnected reasoning](disconnected-reasoning.md)
- [Exact match](exact-match.md)
- [Information retrieval](information-retrieval.md)
- [Knowledge-base question answering](knowledge-base-question-answering.md)
- [Mean reciprocal rank](mean-reciprocal-rank.md)
- [Multi-hop question answering](multi-hop-question-answering.md)
- [Named-entity recognition](named-entity-recognition.md)
- [Open-domain question answering](open-domain-question-answering.md)
- [TREC](trec.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2101.00774 : Zhu, Lei, Wang, Zheng, Poria, Chua, "Retrieving and Reading: A Comprehensive Survey on Open-domain Question Answering", v1 20210104: definition of open-domain QA, retriever-reader (read 20261102 20:56 UTC)
2. https://www.cambridge.org/core/product/identifier/S1351324901002789/type/journal_article : Voorhees, "The TREC question answering track", Natural Language Engineering 7(4), pp. 361-378, 2001: the track and its short-answer task, as the abstract page summarises it (read 20261102 20:57 UTC)
3. https://arxiv.org/abs/1704.00051 : Chen, Fisch, Weston, Bordes, "Reading Wikipedia to Answer Open-Domain Questions", v1 20170331: factoid answer as a text span, retrieval plus comprehension (read 20261102 20:56 UTC)
4. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: Raphael's "SIR: A Computer Program for Semantic Information Retrieval" (1964) as a milestone in the item "Retrieving information from unstructured sources"; the text does not call SIR question answering (text extracted and re-read 20261102 21:21 UTC)
5. https://trec.nist.gov/overview.html : NIST, TREC overview: started 1992, "introduced evaluations for open-domain question answering", no year given (read 20261102 20:56 UTC)
6. https://trec.nist.gov/data/qamain.html : NIST, TREC QA data list: TREC-8 (1999) to 2007, Live QA 2015 to 2017 (read 20261102 20:56 UTC)
7. https://trec.nist.gov/data/qa/t8_qadata.html : NIST, TREC-8 QA data: 200 test questions, TREC disks 4 and 5 minus the Congressional Record, questions 131 and 184 left out of the final scores (re-read 20261102 21:21 UTC)
8. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE 100, 2012: natural-language question work "started with the question answering task in TREC" (read 20261102 20:56 UTC)
9. https://www.ibm.com/history/watson-jeopardy : IBM, Watson on Jeopardy!, 201102, DeepQA (first-party; read 20261102 20:58 UTC)
10. https://aclanthology.org/D16-1264/ : Rajpurkar, Zhang, Lopyrev, Liang, "SQuAD: 100,000+ Questions for Machine Comprehension of Text", EMNLP 2016, pp. 2383-2392 (read 20261102 20:57 UTC)
11. https://arxiv.org/abs/2004.04906 : Karpukhin et al., "Dense Passage Retrieval for Open-Domain Question Answering", v1 20200410 (read 20261102 20:57 UTC)
12. https://arxiv.org/abs/2005.11401 : Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", v1 20200522, abstract (first-party result; read 20261102 20:57 UTC)
