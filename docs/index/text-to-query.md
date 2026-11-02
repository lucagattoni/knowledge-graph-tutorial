---
type: index
kind: concept
aliases: [text-to-Cypher, text-to-SQL, text-to-SPARQL, NL2SQL, natural language interface to databases, NLIDB]
updated: 20261102 22:50 UTC
---

# Text-to-query

This entry says what text-to-query means, how it grew from natural-language database interfaces of the 1970s to language models that write Cypher and SPARQL, and what newer papers blame for its failures.

## Definition

Text-to-query translates a natural-language question into a formal query that a database engine then runs. The Text2Cypher authors give the reason for Cypher: "using Cypher requires specialized knowledge", so they translate natural-language queries into Cypher for non-expert users [1]. The Seq2SQL authors say the same of SQL [2]. The Text2GraphQuery-Bench authors call such systems "Text-to-Graph-Query", with language models acting as interfaces to graph database systems [3]. The target may be [SQL](./sql.md), [Cypher](./cypher.md), [GQL](./gql.md) or [SPARQL](./sparql.md) [1][2][3][7]. The translator need not be a language model [4].

## How it changed

- **Late 1960s and 1970s.** Prototype natural-language interfaces to databases appear; the best known, LUNAR, answers questions on chemical analyses of moon rocks, and each early system was built for one database [4]. Era: [Formal foundations](../history/formal-foundations.md).
- **October 2013.** Berant et al. publish "Semantic Parsing on Freebase from Question-Answer Pairs" at EMNLP; the abstract was not on the page read [5]. See [semantic parsing](./semantic-parsing.md).
- **20170831.** Seq2SQL translates questions to SQL with reinforcement learning and releases WikiSQL (80,654 examples); execution accuracy rises from 35.9% to 59.4% against a sequence-to-sequence baseline (first-party) [2].
- **20180924.** Spider (10,181 questions, 200 databases) puts new databases in the test set; the best model scores 12.4% exact match (first-party) [6]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20241213.** Text2Cypher merges public datasets into one cleaned set; fine-tuned models beat baselines (first-party) [1]. Size and splits: [Text2Cypher](../benchmarks/text2cypher.md). Trend: [Asking graphs in natural language](../trends/graph-query-generation.md).
- **20260212.** Text2GraphQuery-Bench holds 267,276 question-query pairs over 34 databases in Cypher, GQL and SQL/PGQ (first-party) [3].
- **20261009.** SPARQL-LLM reports ranking first among eight approaches in the TEXT2SPARQL 2026 challenge (first-party) [7].

## Where sources disagree

**What blocks the model.** The Text2Cypher authors say language models "often struggle to capture complex nuances" and that fine-tuning is the more promising route [1]. The Text2GraphQuery-Bench authors find few-shot prompting largely recovers zero-shot GQL and SQL/PGQ grammar scores, and an 8B fine-tuned model matches large zero-shot ones, which they read as "unfamiliarity - rather than model capacity" being the main barrier [3]. Both are first-party, 14 months apart; no source read compares them directly.

**The name.** The older line is called semantic parsing or NLIDB, the SQL line text-to-SQL, the 2024 line Text2Cypher [1][4][5][6]. None of the sources read uses "text-to-query" as a name; it is this documentation's label for the family.

## Related

[Semantic parsing](./semantic-parsing.md) · [knowledge-base question answering](./knowledge-base-question-answering.md) · [graph database](./graph-database.md) · [SQL/PGQ](./sql-pgq.md) · [large language model](./large-language-model.md) · [fine-tuning](./fine-tuning.md) · benchmarks: [Text2Cypher](../benchmarks/text2cypher.md), [LC-QuAD](../benchmarks/lc-quad.md) · trend: [graph query generation](../trends/graph-query-generation.md) · papers: [graph query generation](../papers/graph-query-generation.md) · projects: [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md), [Code-Graph-RAG](../projects/code-graph-rag.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Projects**

- [Code-Graph-RAG](../projects/code-graph-rag.md)
- [Memgraph](../projects/memgraph.md)
- [Neo4j LLM Knowledge Graph Builder](../projects/llm-graph-builder.md)

**Papers**

- [Papers: Asking graphs in natural language](../papers/graph-query-generation.md)

**Benchmarks**

- [LC-QuAD](../benchmarks/lc-quad.md)

**Index**

- [Fine-tuning](fine-tuning.md)
- [Knowledge-base question answering](knowledge-base-question-answering.md)
- [Semantic parsing](semantic-parsing.md)
- [Tool use](tool-use.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2412.10064 : Ozsoy et al., "Text2Cypher: Bridging Natural Language and Graph Databases", v1 20241213, abstract (first-party; read 20261102 22:13 UTC)
2. https://arxiv.org/abs/1709.00103 : Zhong, Xiong, Socher, "Seq2SQL", v1 20170831, abstract (first-party; read 20261102 22:13 UTC)
3. https://arxiv.org/abs/2602.11745 : Lyu et al., "Text2GraphQuery-Bench", v1 20260212, v2 20260805, abstract (first-party; read 20261102 22:13 UTC)
4. https://arxiv.org/pdf/cmp-lg/9503016 : Androutsopoulos, Ritchie, Thanisch, "Natural Language Interfaces to Databases - An Introduction", arXiv March 1995, section 2 (history: LUNAR, late sixties and early seventies) (read 20261102 22:13 UTC)
5. https://aclanthology.org/D13-1160/ : Berant, Chou, Frostig, Liang, "Semantic Parsing on Freebase from Question-Answer Pairs", EMNLP 2013, Seattle: title and venue only (read 20261102 22:13 UTC)
6. https://arxiv.org/abs/1809.08887 : Yu et al., "Spider", v1 20180924, abstract (first-party; read 20261102 22:13 UTC)
7. https://arxiv.org/abs/2610.13648 : Smeros et al., "SPARQL-LLM in the TEXT2SPARQL 2026 Challenge", v1 20261009, abstract (first-party; read 20261102 22:13 UTC)
