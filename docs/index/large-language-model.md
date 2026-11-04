---
type: index
kind: concept
aliases: [LLM, LLMs, large language models]
updated: 20261102 20:55 UTC
---

# Large language model

This entry says what the field means by a large language model, how the idea built up, and where the term has no fixed edge.

## Definition

A large language model (LLM) is a language model, usually a Transformer, trained on very large text collections at a scale where new abilities appear. The survey by Zhao et al. says the research community "coined the term large language models (LLM) for the PLMs of significant size", for example models with tens or hundreds of billions of parameters [1]. A PLM is a pre-trained language model.

## How it changed

- **20170612.** Vaswani et al. propose the Transformer, built "solely on attention mechanisms" (arXiv v1) [2]. Zhao et al. say existing LLMs are mainly built on this architecture [1].
- **20181011.** Devlin et al. introduce BERT, which pre-trains deep bidirectional representations (arXiv v1) [3]. The survey of Zhao et al. names BERT as an example of a small-scale model, in contrast to LLMs [1].
- **20200123.** Kaplan et al. report that language-model loss follows a power law in model size, data size and training compute, with some trends spanning more than seven orders of magnitude (arXiv v1) [4].
- **20200528.** Brown et al. train GPT-3, an autoregressive model with 175 billion parameters, and test it with a few examples in the prompt and no weight updates (arXiv v1) [5].
- **20221130.** OpenAI announces ChatGPT as a free research preview [6]. The era page [language models meet retrieval](../history/language-models-meet-retrieval.md) ends here, and [what has settled since 2023](../history/settled-since-2023.md) starts.
- **20230331 to 20260318.** The survey of Zhao et al. first appears on 20230331 and its latest version, v19, is dated 20260318 [1].

## Where sources disagree

The size at which a model counts as large is not fixed. One survey gives three phrasings: "tens or hundreds of billions of parameters" in its abstract [1], "hundreds of billions (or more)" in its background section [1], and a footnote that says "no formal consensus on the minimum parameter scale" and loosely takes models above 10B [1]. No source read gives a single number.

## Related

- Entries: [Transformer](./transformer.md), [BERT](./bert.md), [token](./token.md), [context window](./context-window.md), [embedding](./embedding.md), [retrieval-augmented generation](./retrieval-augmented-generation.md), [agent](./agent.md), [knowledge graph](./knowledge-graph.md).
- Trend and papers: [building knowledge graphs with LLMs](../trends/llm-kg-construction.md), [paper group](../papers/llm-kg-construction.md), [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)
- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)
- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)
- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md)
- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)
- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)
- [Semantic web standards: from RDF 1.1 and RDF-star to RDF 1.2](../trends/semantic-web-standards.md)
- [Trends: what the field is doing now](../trends/README.md)
- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Projects**

- [agent-memory (Tigerless Labs)](../projects/tigerless-agent-memory.md)
- [Basic Memory](../projects/basic-memory.md)
- [code-review-graph](../projects/code-review-graph.md)
- [CodeGraph](../projects/codegraph.md)
- [Cognee](../projects/cognee.md)
- [Dify](../projects/dify.md)
- [GLiNER](../projects/gliner.md)
- [Graphiti](../projects/graphiti.md)
- [GraphRAG SDK](../projects/graphrag-sdk.md)
- [HippoRAG](../projects/hipporag.md)
- [Hyper-Extract](../projects/hyper-extract.md)
- [Letta](../projects/letta.md)
- [LightRAG](../projects/lightrag.md)
- [LlamaIndex](../projects/llama-index.md)
- [LLM Wiki (nashsu)](../projects/llm-wiki-nashsu.md)
- [Mem0](../projects/mem0.md)
- [Memori](../projects/memori.md)
- [MemOS](../projects/memos.md)
- [Microsoft GraphRAG](../projects/microsoft-graphrag.md)
- [MIRIX](../projects/mirix.md)
- [Neo4j LLM Knowledge Graph Builder](../projects/llm-graph-builder.md)
- [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md)
- [OntoGPT](../projects/ontogpt.md)
- [PageIndex](../projects/pageindex.md)
- [Projects](../projects/README.md)
- [RAG-Anything](../projects/rag-anything.md)
- [Semantica](../projects/semantica.md)
- [Understand Anything](../projects/understand-anything.md)

**Papers**

- [Papers: Agent memory](../papers/agent-memory.md)
- [Papers: Agentic search over raw data](../papers/agentic-search.md)
- [Papers: Asking graphs in natural language](../papers/graph-query-generation.md)
- [Papers: Building knowledge graphs with LLMs](../papers/llm-kg-construction.md)
- [Papers: foundations](../papers/foundations.md)
- [Papers: Vectorless retrieval](../papers/reasoning-over-structure.md)

**Datasets**

- [UltraDomain](../datasets/ultradomain.md)

**Benchmarks**

- [LongMemEval](../benchmarks/longmemeval.md)
- [Text2Cypher](../benchmarks/text2cypher.md)
- [Text2KGBench](../benchmarks/text2kgbench.md)
- [WebQuestionsSP](../benchmarks/webquestionssp.md)

**Experiments**

- [Instruments evidence: the metering gateway](../experiments/evidence/instruments-gateway.md)
- [X2: the index cost of cheap graph builders](../experiments/x2-index-cost.md)

**Applied to Pinakes**

- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Agent](agent.md)
- [BERT](bert.md)
- [Chain-of-thought](chain-of-thought.md)
- [Cognitive architecture](cognitive-architecture.md)
- [Community report](community-report.md)
- [Context window](context-window.md)
- [Data contamination](data-contamination.md)
- [Fine-tuning](fine-tuning.md)
- [Gleaning](gleaning.md)
- [GraphRAG](graphrag.md)
- [GRPO](grpo.md)
- [Inference engine](inference-engine.md)
- [Knowledge graph completion](knowledge-graph-completion.md)
- [Knowledge-base question answering](knowledge-base-question-answering.md)
- [LinkML](linkml.md)
- [LLM wiki](llm-wiki.md)
- [LLM-as-judge](llm-as-judge.md)
- [Model Context Protocol](model-context-protocol.md)
- [Named-entity recognition](named-entity-recognition.md)
- [Prompt caching](prompt-caching.md)
- [Reinforcement learning](reinforcement-learning.md)
- [Relevance feedback](relevance-feedback.md)
- [Reranking](reranking.md)
- [Retrieval-augmented generation](retrieval-augmented-generation.md)
- [SPARQL](sparql.md)
- [Supervised fine-tuning](supervised-fine-tuning.md)
- [Test-time learning](test-time-learning.md)
- [Text-to-query](text-to-query.md)
- [Token](token.md)
- [Tool use](tool-use.md)
- [Transformer](transformer.md)
- [Vectorless retrieval](vectorless-retrieval.md)
- [Word sense disambiguation](word-sense-disambiguation.md)

<!-- END GENERATED: appears-in -->

## Sources

Read times are UTC.

1. https://arxiv.org/abs/2303.18223 and https://arxiv.org/pdf/2303.18223 : Zhao et al., "A Survey of Large Language Models"; abstract and listing (v1 20230331, v19 20260318); Section 2.1 and footnote 4 (read 20261102 20:45 and 20:47)
2. https://arxiv.org/abs/1706.03762 : Vaswani et al., "Attention Is All You Need", v1 20170612 (read 20261102 20:45)
3. https://arxiv.org/abs/1810.04805 : Devlin et al., BERT, v1 20181011 (read 20261102 20:45)
4. https://arxiv.org/abs/2001.08361 : Kaplan et al., "Scaling Laws for Neural Language Models", v1 20200123 (read 20261102 20:45)
5. https://arxiv.org/abs/2005.14165 : Brown et al., "Language Models are Few-Shot Learners", v1 20200528 (read 20261102 20:45)
6. https://web.archive.org/web/20221130190000/https://openai.com/blog/chatgpt/ : OpenAI, "ChatGPT: Optimizing Language Models for Dialogue", dated "November 30, 2022" (archived copy; the live page returned a bot-check page) (read 20261102 20:50)
