---
type: index
kind: concept
aliases: [semantic parser]
updated: 20261102 22:54 UTC
---

# Semantic parsing

This entry answers what semantic parsing is and how it moved from hand-written rules to learned parsers and then to language models. Its newest form, writing SQL, Cypher or SPARQL, has its own entry: [text-to-query](./text-to-query.md).

## Definition

Kamath and Das (AKBC 2019) say semantic parsing deals with "converting natural language utterances to logical forms" that can be executed on a knowledge base; their running example turns a question about a sports table into SQL [1]. Yih et al. (2016) give a wider definition: "the mapping of text to a meaning representation" [6].

## How it changed

- **1973.** Early systems were rule-based and domain-specific; LUNAR (Woods, 1973) mapped a parse tree to a database query by rules [1]. See [Formal foundations](../history/formal-foundations.md).
- **1996.** Zelle and Mooney (AAAI-96) train on sentences paired with database queries; the learned parsers beat a hand-crafted one on a U.S. geography database [2].
- **2005.** Zettlemoyer and Collins learn from sentences labelled with lambda-calculus expressions (UAI 2005) [3].
- **201310.** Berant et al. (EMNLP 2013, 18-21 October) train on question-answer pairs, not annotated logical forms, and scale to [Freebase](./freebase.md) [4]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **201507.** Yih et al. (ACL-IJCNLP 2015, 26-31 July) reduce parsing to generating a query graph and reach F1 52.5% on WebQuestions (first-party) [5].
- **20160106.** Dong and Lapata replace hand-built features with an attention-based encoder-decoder (first version; ACL 2016) [7].
- **20260716.** SAGA names "semantic parsing into an executable logical form" as one of two common approaches to complex question answering over a knowledge base, and builds SPARQL with language-model agents [8]. Still moving: [Asking graphs in natural language](../trends/graph-query-generation.md).

## Where sources disagree

**Are labelled parses worth it?** Berant et al. learn from answers alone [4]. Yih et al. (2016) say recent work "called into question" parse labels, then report an absolute 5-point gain from learning with them over answers alone [6].

**Must the form be executable?** Kamath and Das, Berant et al. and SAGA speak of forms that run against a knowledge base [1][4][8]; Yih et al. (2016) define the task without execution [6].

## Related

[Text-to-query](./text-to-query.md) · [knowledge-base question answering](./knowledge-base-question-answering.md) · [SPARQL](./sparql.md) · [Cypher](./cypher.md) · [SQL](./sql.md) · [entity linking](./entity-linking.md). Data: [WebQSP](../datasets/webquestionssp.md), [GrailQA](../datasets/grailqa.md), [LC-QuAD](../datasets/lc-quad.md). Benchmark: [WebQSP](../benchmarks/webquestionssp.md). Papers: [graph query generation](../papers/graph-query-generation.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Datasets**

- [ComplexWebQuestions](../datasets/complexwebquestions.md)
- [GrailQA](../datasets/grailqa.md)
- [WebQuestionsSP](../datasets/webquestionssp.md)

**Benchmarks**

- [WebQuestionsSP](../benchmarks/webquestionssp.md)

**Index**

- [Knowledge-base question answering](knowledge-base-question-answering.md)
- [Text-to-query](text-to-query.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/1812.00978 : Kamath and Das, "A Survey on Semantic Parsing", AKBC 2019, arXiv v3 of 29 May 2019: abstract, section 1, Figure 1, sections 3.1 and 3.2 (LUNAR, Zelle and Mooney) (read 20261102 22:09 UTC)
2. https://www.aaai.org/Papers/AAAI/1996/AAAI96-156.pdf : Zelle and Mooney, "Learning to Parse Database Queries Using Inductive Logic Programming", AAAI-96: abstract (read 20261102 22:09 UTC)
3. https://arxiv.org/abs/1207.1420 : Zettlemoyer and Collins, "Learning to Map Sentences to Logical Form", UAI 2005 (arXiv copy posted 4 July 2012): abstract (read 20261102 22:09 UTC)
4. https://aclanthology.org/D13-1160.pdf : Berant et al., "Semantic Parsing on Freebase from Question-Answer Pairs", EMNLP 2013, Seattle, 18-21 October 2013: abstract and introduction (read 20261102 22:09 UTC)
5. https://aclanthology.org/P15-1128.pdf : Yih et al., "Semantic Parsing via Staged Query Graph Generation", ACL-IJCNLP 2015, 26-31 July 2015: abstract (read 20261102 22:09 UTC)
6. https://aclanthology.org/P16-2033.pdf : Yih et al., "The Value of Semantic Parse Labeling for Knowledge Base Question Answering", ACL 2016, 7-12 August 2016: abstract and introduction (read 20261102 22:09 UTC)
7. https://arxiv.org/abs/1601.01280 : Dong and Lapata, "Language to Logical Form with Neural Attention", v1 6 January 2016, ACL 2016: abstract (read 20261102 22:09 UTC)
8. https://arxiv.org/abs/2607.14494 : Zhang and Tsuda, "SAGA: Schema-Aware Grounding for Agentic Text-to-SPARQL Generation", v1 16 July 2026: abstract (read 20261102 22:12 UTC)
