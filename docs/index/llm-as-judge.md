---
type: index
kind: concept
aliases: [LLM-as-a-judge, LLM judge, LLM-judge]
updated: 20261102 22:53 UTC
---

# LLM-as-judge

This entry says what it means to use a language model as a judge, what two 2023 studies found, and how far later sources trust it. The sources read disagree on how far a judge can be trusted.

## Definition

Zheng et al. (NeurIPS 2023) explore "using strong LLMs as judges to evaluate these models on more open-ended questions" [1]. A judge model reads a question and either two answers (pairwise comparison) or one (single-answer grading) and returns a verdict or a score [4]. Gu et al. describe it as employing language models as evaluators, a scalable, cost-effective alternative to expert evaluation [2].

## How it changed

- **20230329 (arXiv v1).** Liu et al. present G-Eval, which prompts GPT-4 with chain-of-thought and a form-filling scheme: Spearman 0.514 with humans on summarization (first-party). They warn of a bias towards text written by language models [3].
- **20230609 (arXiv v1).** Zheng et al. name "position, verbosity, and self-enhancement biases" and report over 80% agreement between GPT-4 and human preferences, "the same level of agreement between humans" (first-party) [1]. On MT-bench without ties, GPT-4 agrees with humans 85% and humans with each other 81% [4].
- **20241123 (arXiv v1; v6 20251019).** Gu et al. publish a survey; they say that ensuring reliability "remains a significant challenge" [2].
- **20260404 (year inferred: "Posted on Apr 4"; the account joined 2 February 2026).** Penfield, a company whose profile promises agents "persistent recall", blogs that the LoCoMo judge accepted 62.81% of deliberately wrong but topically adjacent answers [6]. See [LoCoMo](../benchmarks/locomo.md).
- **20260911.** Prokopiou et al. calibrate their Text-to-Cypher judge against blind human labels and "find it optimistic by 9 points" (first-party; EMNLP 2026 workshop) [5].

Whether judges are now the standard way to score answers is **unstated** in the sources read.

## Where sources disagree

**How far a judge can be trusted.** Zheng et al. find agreement with humans as high as among humans, on MT-bench [1][4]. Gu et al. call reliability a significant challenge [2]. Prokopiou et al. measure a judge nine points more optimistic than blind human labels [5]. The Penfield post is a company blog, not peer reviewed, and was not rerun here; it finds a judge accepting 62.81% of wrong answers yet catching about 89% of specific factual errors [6].

*Reading:* the numbers measure different things (chat preferences, a survey's view, one query-generation task, adversarial answers). None overturns another, and no source read compares them.

## Related

- Entries: [large language model](./large-language-model.md), [exact match](./exact-match.md), [chain-of-thought](./chain-of-thought.md).
- Benchmarks that use a judge: [LongMemEval](../benchmarks/longmemeval.md), [LoCoMo](../benchmarks/locomo.md), [FRAMES](../benchmarks/frames.md), [CRAG](../benchmarks/crag.md), [EnterpriseRAG-Bench](../benchmarks/enterpriserag-bench.md), [MemoryAgentBench](../benchmarks/memoryagentbench.md).
- Trends: [Agent memory](../trends/agent-memory.md), [Asking graphs in natural language](../trends/graph-query-generation.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Mem0](../projects/mem0.md)
- [memU](../projects/memu.md)
- [MIRIX](../projects/mirix.md)
- [RAG-Anything](../projects/rag-anything.md)
- [Supermemory](../projects/supermemory.md)

**Papers**

- [Papers: Agent memory](../papers/agent-memory.md)

**Benchmarks**

- [CRAG](../benchmarks/crag.md)
- [EnterpriseRAG-Bench](../benchmarks/enterpriserag-bench.md)
- [FRAMES](../benchmarks/frames.md)
- [LoCoMo](../benchmarks/locomo.md)
- [LongMemEval](../benchmarks/longmemeval.md)
- [MemoryAgentBench](../benchmarks/memoryagentbench.md)

**Index**

- [Exact match](exact-match.md)

<!-- END GENERATED: appears-in -->

## Sources

Read times are UTC.

1. https://arxiv.org/abs/2306.05685 : Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", NeurIPS 2023 Datasets and Benchmarks; abstract and submission history (v1 9 June 2023, v4 24 December 2023) (first-party; read 20261102 22:09 UTC)
2. https://arxiv.org/abs/2411.15594 : Gu et al., "A Survey on LLM-as-a-Judge", abstract; v1 23 November 2024, v6 19 October 2025 (read 20261102 22:09 UTC)
3. https://export.arxiv.org/api/query?id_list=2306.05685,2411.15594,2609.12746,2303.16634,2502.11371 : arXiv record of "G-Eval" (Liu et al., v1 29 March 2023): abstract with the Spearman 0.514 and the bias warning (first-party; read 20261102 22:09 UTC)
4. https://arxiv.org/html/2306.05685v4 : Zheng et al., Section 3.1 (pairwise comparison and single answer grading) and Section 4.2: agreement 85% between GPT-4 and humans against 81% among humans on MT-bench, setup without ties (read 20261102 22:10 UTC and 22:48 UTC)
5. https://arxiv.org/abs/2609.12746 : Prokopiou et al., LAST-CQ, v1 11 September 2026; abstract; comment on the EMNLP 2026 workshop REALM (first-party; read 20261102 22:09 UTC)
6. https://dev.to/penfieldlabs/we-audited-locomo-64-of-the-answer-key-is-wrong-and-the-judge-accepts-up-to-63-of-intentionally-33lg : Penfield blog post "We audited LoCoMo": judge test (62.81%, about 89%), "Posted on Apr 4", account profile (joined 2 February 2026) (read 20261102 22:15 UTC)
