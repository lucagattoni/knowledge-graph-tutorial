---
type: index
kind: concept
aliases: [KGC, KG completion, knowledge base completion]
updated: 20261102 22:53 UTC
---

# Knowledge graph completion

This entry says what knowledge graph completion is, how it relates to link prediction, and how its methods moved from embeddings to language models. The sources read disagree on whether completion and link prediction are one task.

## Definition

Hogan et al. (ACM Computing Surveys 54(4), 2021) place completion under graph refinement and say it aims at "filling in the missing edges (aka missing links) of a knowledge graph" [1]. The edges sought are those "deemed correct" but neither given nor entailed by the graph [1]. Correction is the opposite task: it finds and removes incorrect edges [1].

## How it changed

- **2013.** Bordes et al. present TransE and report that it "significantly outperforms state-of-the-art methods in link prediction on two knowledge bases" (first-party) [3]. See [knowledge graph embedding](./knowledge-graph-embedding.md) and [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20190907 (arXiv v1).** Yao et al. treat triples as text sequences and score them with a pre-trained language model, KG-BERT (first-party) [5]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **2020.** Ji et al. (v1 20200202) sort methods into embedding-based ranking, relation-path reasoning, rule-based reasoning and meta relational learning [2][5]. Hogan et al. (v1 20200304) name embeddings and rule mining as the usual techniques [1][5].
- **20230826 (arXiv v1).** Yao et al. prompt large language models with entity and relation descriptions and report state-of-the-art results on triple classification and relation prediction; fine-tuned smaller models outperform ChatGPT and GPT-4 (first-party; ICASSP 2025) [5].
- **20250821.** Gul et al. note that MRR and Hit@1 "can yield conflicting rankings" and propose a meta-metric (first-party) [5].
- **20260312.** Ieng et al. say graphs built with language models are often incomplete or noisy; their method OMNIA proposes candidate triples by clustering and checks them with an embedding filter and a language model (first-party) [6]. Still moving: [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

Whether language-model methods have replaced embedding methods is **unstated** in the sources read.

## Where sources disagree

**How completion and link prediction relate.** Nickel et al. write that "In the context of knowledge graphs, link prediction is also referred to as knowledge graph completion": one task, two names [4]. Hogan et al. treat completion as the aim and link prediction as the family of techniques for it [1]. Ji et al. make link prediction one of three completion subtasks, beside entity prediction and relation prediction [2]. See [link prediction](./link-prediction.md).

## Related

- Entries: [link prediction](./link-prediction.md), [knowledge graph embedding](./knowledge-graph-embedding.md), [knowledge graph](./knowledge-graph.md), [triple](./triple.md), [relation extraction](./relation-extraction.md), [large language model](./large-language-model.md).
- Benchmarks: [filtered link prediction](../benchmarks/kg-link-prediction.md), [OGB link prediction](../benchmarks/ogb-link-prediction.md). Data sets: [FB15k-237](../datasets/fb15k-237.md), [WN18RR](../datasets/wn18rr.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Benchmarks**

- [Benchmarks](../benchmarks/README.md)
- [Knowledge graph link prediction](../benchmarks/kg-link-prediction.md)
- [OGB link prediction](../benchmarks/ogb-link-prediction.md)

**Index**

- [Link prediction](link-prediction.md)
- [Slot filling](slot-filling.md)

<!-- END GENERATED: appears-in -->

## Sources

Read times are UTC.

1. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", ACM Computing Surveys 54(4), 2021, version 6: Section 8 (refinement), 8.1 (completion, link prediction techniques), 8.2 (correction) (read 20261102 22:10 UTC)
2. https://arxiv.org/pdf/2002.00388 : Ji et al., "A Survey on Knowledge Graphs: Representation, Acquisition and Applications", IEEE TNNLS 2021: Section on knowledge graph completion and the overview of its categories (read 20261102 22:10 UTC)
3. https://papers.nips.cc/paper_files/paper/2013/file/1cecc7a77928ca8133fa24680a88d2f9-Paper.pdf : Bordes et al., "Translating Embeddings for Modeling Multi-relational Data", NIPS 2013, abstract (read 20261102 22:10 UTC)
4. https://arxiv.org/pdf/1503.00759 : Nickel, Murphy, Tresp and Gabrilovich, "A Review of Relational Machine Learning for Knowledge Graphs", Section on main tasks (link prediction, completion); four authors on the first page (read 20261102 22:10 UTC and 22:45 UTC)
5. https://export.arxiv.org/api/query?id_list=1503.00759,2002.00388,1909.03193,2308.13916,2003.02320,2508.15357,2203.02167 : arXiv records: first-version dates, comments and abstracts of Ji et al. (v1 20200202), KG-BERT (v1 20190907), Yao et al. (v1 20230826, ICASSP 2025 note), Hogan et al. (v1 20200304), KG-EDAS (v1 20250821) (read 20261102 22:12 UTC)
6. https://export.arxiv.org/api/query?id_list=2603.11820 : arXiv record of "OMNIA: Closing the Loop by Leveraging LLMs for Knowledge Graph Completion", v1 20260312, abstract (first-party; read 20261102 22:15 UTC)
