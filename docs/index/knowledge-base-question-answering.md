---
type: index
kind: concept
aliases: [KBQA, KGQA, knowledge graph question answering, question answering over knowledge bases]
updated: 20261102 22:53 UTC
---

# Knowledge-base question answering

This entry says what knowledge-base question answering (KBQA) is and how the task and its test sets developed from 2013 to 2026. It also records an audit of the test sets.

## Definition

Lan et al. write that KBQA "aims to answer a question over a knowledge base (KB)" [1]. Their survey (first posted 20210815) sorts methods into semantic-parsing-based and information-retrieval-based [1]. A semantic parser maps the question to a logical form that is executed on the knowledge base to produce the answer [2]. Papers on knowledge graphs use the name KGQA [7][8].

## How it changed

- **20131018 to 20131021.** Berant et al. train a semantic parser for Freebase from question-answer pairs, not annotated logical forms, and collect WebQuestions (EMNLP 2013) [2]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20150605.** Bordes et al. introduce a dataset for simple question answering [3]: [SimpleQuestions](../datasets/simplequestions.md).
- **201608.** Yih et al. report that learning from labelled semantic parses beats learning from answers by 5 points absolute, and release WebQSP (ACL 2016; first-party) [4].
- **20180318 and 20201116.** Talmor and Berant create ComplexWebQuestions [5]. Gu et al. release [GrailQA](../datasets/grailqa.md), with i.i.d., compositional and zero-shot test levels [6]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20230715.** Sun et al. let a language model explore a knowledge graph step by step, without extra training (Think-on-Graph, ICLR 2024) [9]. Still moving: [Asking graphs in natural language](../trends/graph-query-generation.md), [Agentic graph retrieval](../trends/learned-graph-traversal.md).
- **20250529.** Zhang et al. audit 16 KGQA datasets by hand: average factual correctness "only 57 %" (NeurIPS 2025) [7].
- **20260702 to 20260707.** Shan et al. (ACL 2026) report Hit@1 of 91.5% on WebQSP against 87.7% before (first-party) [8].

## Where sources disagree

**Names and categories.** Lan et al. say KBQA and split methods into semantic-parsing-based and retrieval-based [1]. The 2025 and 2026 papers say KGQA [7][8]; Shan et al. split path-based multi-hop methods into ontology-guided and subgraph-based [8]. No source read says whether KBQA and KGQA differ.

**How far the benchmarks can be trusted.** Zhang et al. name WebQSP and ComplexWebQuestions among sets with "critical quality issues" [7], yet new systems are still scored on them [8]. *Reading:* a gain of a few points on these sets is weak evidence.

## Related

[Knowledge base](./knowledge-base.md), [knowledge graph](./knowledge-graph.md), [semantic parsing](./semantic-parsing.md), [text-to-query](./text-to-query.md), [question answering](./question-answering.md), [multi-hop question answering](./multi-hop-question-answering.md), [SPARQL](./sparql.md), [Freebase](./freebase.md), [large language model](./large-language-model.md). Datasets: [WebQuestionsSP](../datasets/webquestionssp.md), [ComplexWebQuestions](../datasets/complexwebquestions.md), [GrailQA](../datasets/grailqa.md), [MetaQA](../datasets/metaqa.md), [LC-QuAD](../datasets/lc-quad.md). Benchmark: [WebQuestionsSP](../benchmarks/webquestionssp.md). Papers: [graph query generation](../papers/graph-query-generation.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)

**Datasets**

- [GrailQA](../datasets/grailqa.md)
- [SimpleQuestions](../datasets/simplequestions.md)

**Benchmarks**

- [WebQuestionsSP](../benchmarks/webquestionssp.md)

**Index**

- [Open-domain question answering](open-domain-question-answering.md)
- [Semantic parsing](semantic-parsing.md)
- [Text-to-query](text-to-query.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2108.06688 : Lan et al., "Complex Knowledge Base Question Answering: A Survey", first submitted 15 Aug 2021, abstract: definition and the two method groups; published in IEEE Transactions on Knowledge and Data Engineering 35 per https://api.crossref.org/works?query.bibliographic=Complex+Knowledge+Base+Question+Answering+A+Survey+Lan+He+Jiang (read 20261102 22:16 UTC and 22:18 UTC)
2. https://aclanthology.org/D13-1160.pdf : Berant et al., "Semantic Parsing on Freebase from Question-Answer Pairs", EMNLP 2013, Seattle, 18-21 October 2013: abstract and introduction (read 20261102 22:17 UTC)
3. https://arxiv.org/abs/1506.02075 : Bordes et al., "Large-scale Simple Question Answering with Memory Networks", submitted 5 Jun 2015, abstract: introduces a new dataset for simple question answering (read 20261102 22:16 UTC)
4. https://aclanthology.org/P16-2033.pdf : Yih et al., "The Value of Semantic Parse Labeling for Knowledge Base Question Answering", ACL 2016, Berlin, 7-12 August 2016: abstract (read 20261102 22:18 UTC)
5. https://arxiv.org/abs/1803.06643 : Talmor and Berant, "The Web as a Knowledge-base for Answering Complex Questions", submitted 18 Mar 2018, NAACL 2018, abstract (read 20261102 22:16 UTC)
6. https://arxiv.org/abs/2011.07743 : Gu et al., "Beyond I.I.D.: Three Levels of Generalization for Question Answering on Knowledge Bases", submitted 16 Nov 2020, abstract (read 20261102 22:16 UTC)
7. https://arxiv.org/abs/2505.23495 : Zhang et al., "Diagnosing and Addressing Pitfalls in KG-RAG Datasets", submitted 29 May 2025, v4 3 Nov 2025, NeurIPS 2025 Datasets and Benchmarks, abstract (read 20261102 22:16 UTC)
8. https://aclanthology.org/2026.acl-long.489.pdf : Shan et al., "Reasoning with Ontology Graph: Toward Type-Constrained Knowledge Graph Question Answering", ACL 2026, 2-7 July 2026: abstract and introduction (first-party; read 20261102 22:18 UTC)
9. https://arxiv.org/abs/2307.07697 : Sun et al., "Think-on-Graph", first submitted 15 Jul 2023, "Accepted by ICLR 2024", abstract (first-party; read 20261102 22:17 UTC)
