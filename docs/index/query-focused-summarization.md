---
type: index
kind: concept
aliases: [QFS, query-based summarization, question-focused summarization]
updated: 20261102 22:50 UTC
---

# Query-focused summarization

This entry answers what query-focused summarization (QFS) is, where the task comes from, and why the GraphRAG paper put the name in its title.

## Definition

Query-focused summarization writes a summary that answers a given question or topic, instead of summarising a text generically [1][4]. NIST's DUC 2005 task, which Baumel et al. name as where the task was first introduced [4], asked systems to "piece together information from multiple documents to answer a question or set of questions" stated in a topic, with 25 to 50 documents per topic and a 250-word allowance for each answer [1]. Edge et al. say that a global question over a corpus, such as "What are the main themes in the dataset?", is "inherently a query-focused summarization (QFS) task, rather than an explicit retrieval task" [3].

## How it changed

- **2001-2004.** The Document Understanding Conferences (DUC) evaluate "generic and focused summaries" of newspaper and newswire text [1]. See [The semantic web and linked data](../history/semantic-web.md).
- **2005.** DUC has one task, user-oriented and question-focused: 50 topics, 31 participants with runs, repeated in 2006 [1]. NIST's DUC site covers 2001 to 2007; in 2008 DUC became a summarization track of the Text Analysis Conference [2].
- **20180123.** Baumel, Eyal and Elhadad note that QFS "has been addressed mostly using extractive methods" and adapt sequence-to-sequence abstractive models to it [4]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20240424.** Edge et al. (first-party) post "From Local to Global: A Graph RAG Approach to Query-Focused Summarization" (version 2, 20250219). [GraphRAG](./graphrag.md) summarises communities of a graph, then answers a query with a final round of QFS over them; its test corpora hold about 1 and 1.7 million tokens [3]. See [What has settled since 2023](../history/settled-since-2023.md).
- **2025-2026.** The phrase is still in new titles: an arXiv title search read on 20261102 lists FG-RAG, on QFS with graph RAG (20250313), and a paper on building QFS datasets (20260506) [5]. See [Graph-based RAG](../trends/graph-based-rag.md).

## Where sources disagree

**Name and scale.** DUC says "question-focused" [1]; Baumel et al. and Edge et al. say "query-focused" [3][4]; the QMSum benchmark (20210413) says "query-based" [6]. DUC fixed 25 to 50 documents per topic [1]; Edge et al. use the name for corpora of a million tokens and more, and say earlier QFS methods "do not scale to the quantities of text indexed by typical RAG systems" [3]. *Reading:* the GraphRAG paper stretches the task name from a few dozen documents to a whole corpus.

**Origin.** Baumel et al. say the QFS task "was first introduced in DUC 2005" [4]. DUC's own overview calls the 2005 task "question-focused" and says DUC 2001-2004 evaluated "generic and focused summaries" [1]. *Reading:* the two accounts do not obviously agree on what DUC 2005 introduced. Who first used the phrase "query-focused" is unstated in the sources read.

## Related

[GraphRAG](./graphrag.md) · [community report](./community-report.md) · [community detection](./community-detection.md) · [RAPTOR](./raptor.md) · [retrieval-augmented generation](./retrieval-augmented-generation.md). Project: [Microsoft GraphRAG](../projects/microsoft-graphrag.md). Papers: [Graph-based RAG papers](../papers/graph-based-rag.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Papers**

- [Papers: Graph-based RAG](../papers/graph-based-rag.md)

**Index**

- [RAPTOR](raptor.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www-nlpir.nist.gov/projects/duc/pubs/2005papers/OVERVIEW05.pdf : Dang, "Overview of DUC 2005" (NIST): abstract, introduction (DUC 2001-2004 generic and focused summaries), section 2 (task, 50 topics, 25-50 documents), section 3 (31 participants), section 5 (task repeated in 2006) (read 20261102 22:09 UTC)
2. https://duc.nist.gov/ : NIST, Document Understanding Conferences home: DUC 2001-2007; in 2008 a summarization track in TAC (read 20261102 22:09 UTC)
3. https://arxiv.org/abs/2404.16130 : Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization", v1 20240424, v2 20250219 (first-party); abstract, section 3 and Figure 1, section 4.1 (corpus sizes), full text at https://arxiv.org/html/2404.16130v2 (read 20261102 22:09 UTC)
4. https://arxiv.org/abs/1801.07704 : Baumel, Eyal and Elhadad, "Query Focused Abstractive Summarization", v1 20180123, abstract; the introduction (PDF https://arxiv.org/pdf/1801.07704v2, read 20261102 22:47 UTC) says the task "was first introduced in DUC 2005" and describes its input and output (abstract read 20261102 22:10 UTC)
5. https://export.arxiv.org/api/query?search_query=ti:%22query-focused+summarization%22&sortBy=submittedDate&sortOrder=descending&max_results=8 : arXiv API title search, newest records: 2605.05392 (20260506), 2604.10687 (20260412), 2504.07103 FG-RAG (20250313); titles only (read 20261102 22:18 UTC)
6. https://arxiv.org/abs/2104.05938 : Zhong et al., "QMSum: A New Benchmark for Query-based Multi-domain Meeting Summarization", submitted 20210413, title and abstract (read 20261102 22:10 UTC)
