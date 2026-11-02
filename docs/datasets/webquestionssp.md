---
type: dataset
kinds: [questions]
benchmark: webquestionssp
updated: 20261102 21:27 UTC
---

# WebQuestionsSP

This page answers what the WebQuestionsSP (WebQSP) data contains, how big it is, under which terms it is released and how it was made. It is about 4,700 questions produced by the Google Suggest autocomplete service, each labelled with the [SPARQL](../index/sparql.md) query that answers it over [Freebase](freebase.md). How systems are scored on it, and their results, are on [the WebQuestionsSP benchmark page](../benchmarks/webquestionssp.md).

## What it contains

WebQSP is a re-annotation of WebQuestions, the 2013 question set of Berant and colleagues [1][4]. For each question that Freebase can answer, annotators wrote a [semantic parse](../index/semantic-parsing.md): the topic entity (a Freebase machine id and the mention in the question), the chain of Freebase relations leading to the answer, optional constraints, an optional ordering, and the SPARQL query that expresses them. The answer set is what that query returns on a Freebase dump [3]. About 97% of the questions fit a restricted "staged query graph" form; the other 3% have hand-written SPARQL [3]. A question can carry several parses [3].

Questions that could not be fully parsed go to separate "partial" files, with whatever the annotators could fill in [1][3].

## Size and versions

| File | Questions |
|---|---|
| Primary, train | 3,098 |
| Primary, test | 1,639 |
| Partial, train | 680 |
| Partial, test | 393 |

The primary files hold 4,737 questions with complete parses and the partial files 1,073; together they are the 5,810 questions of WebQuestions, with the same train/test split [1][3][4]. I counted the rows from the released files [3].

Counted from the primary files, first parse of each question [3]: 62% have a one-relation chain, 37% a two-relation chain and 25% constraints; 52% have a single answer and 12% ten or more. Train and test hold 3,453 and 1,815 parses.

Version 1.0, one file `WebQSP.zip` of 4.2 MB, which the Microsoft download page lists as "Date Published 7/15/2024" [2]. Answers were computed on the Freebase dump of 2015-08-09, which the paper calls "the latest and last version of Freebase" [1][3].

## Licence

**Unstated.** The Microsoft page gives no licence or dataset terms [2]. The archive's ReadMe has no licence text, and a search of its two PDF documents for "licen", "copyright", "terms of", "permission" and "creative commons" found nothing [3]. The main document asks users to cite the paper [3]. One later paper's dataset table lists WebQSP as "CC License" with no variant and no source, so it is not evidence [6]. The Hugging Face copy `rmanluo/RoG-webqsp` carries no licence field in its metadata [7]. The terms of the Freebase facts behind the answers are on the Freebase page.

## How it was made

1. **Questions (WebQuestions, 2013).** Berant et al. started from "Where was Barack Obama born?" and walked the Google Suggest API breadth-first until 1 million questions were visited. A random 100,000 went to Amazon Mechanical Turk workers, who gave answers found on the Freebase website [1][4].
2. **Re-annotation (2016).** Five annotators who knew Freebase's design wrote the parses in a staged interface: pick the topic entity from [entity-linking](../index/entity-linking.md) suggestions, pick the relation, add filters. The SPARQL is built from those choices [1]. About 3.1% of queries were edited by hand [1]. Answer sets were produced by running the queries on OpenLink Virtuoso 7.1.0 [3].
3. **Quality check.** On 50 sampled questions, one expert labelled each both ways: parses took 21 seconds and were 94% correct, hand-found answers took 82 seconds and were 92% correct. In the original WebQuestions, 66% of answers were fully correct [1].

## Used by

- **Datasets.** [ComplexWebQuestions](complexwebquestions.md) was built by extending WebQSP's SPARQL queries with conjunctions, superlatives and comparatives [5].
- **Papers.** Think-on-Graph tests prompted language models on it [6] ([papers](../papers/learned-graph-traversal.md)). Reasoning on Graphs trains on it [7]. G-Retriever uses it as one of three GraphQA datasets [8] ([papers](../papers/graph-based-rag.md)). A 2025 audit counts about 30 papers on knowledge-graph RAG from 2022 to 2025 that evaluate on WebQSP or on CWQ [9]. A paper at ACL in July 2026 still does [10].
- **Trend.** [Agentic graph retrieval](../trends/learned-graph-traversal.md) names it among its evaluation sets.
- **Benchmark.** [WebQuestionsSP](../benchmarks/webquestionssp.md).

## Known problems

- **Label quality.** An audit of 16 knowledge-graph QA sets (v4, November 2025) had two annotators check 100 sampled WebQSP test items. Only 52% had a factually correct answer. Examples: a year as the answer to "Where did Andy Murray start playing tennis?"; an outdated "president of Peru now"; subjective questions [9].
- **Frozen in 2015.** "Now" is fixed at 2015-08-10 for questions about the present [3]. The paper calls the dump the last version of Freebase, so answers cannot follow later facts [1].
- **Empty answers.** 37 primary questions (26 train, 11 test) have an empty first-parse answer set [3].
- **Annotator agreement and identity beyond "five annotators":** **unstated**.

## Sources

1. https://aclanthology.org/P16-2033.pdf : WebQSP paper (Yih, Richardson, Meek and two others; ACL 2016, pp. 201-206): 4,737 parses, 18.5%, annotation, Tables 1-2 (read 20261102 20:41 UTC)
2. https://www.microsoft.com/en-us/download/details.aspx?id=52763 : download page: version 1.0, "Date Published 7/15/2024", 4.2 MB, 4,737 and 1,073 questions, no licence text (read 20261102 20:40 UTC)
3. https://download.microsoft.com/download/f/5/0/f5012144-a4fb-4084-897f-cfda99c60bdf/WebQSP.zip : `ReadMe.txt`, `doc/WebQSP.pdf`, `doc/LabelingInstructions.pdf`, `eval/eval.py`, the four data files; row and parse counts computed with a script (downloaded 20261102 20:42 UTC)
4. https://aclanthology.org/D13-1160.pdf : WebQuestions paper (Berant et al., EMNLP 2013): Google Suggest crawl, Mechanical Turk, 5,810 examples (read 20261102 20:46 UTC; Google Suggest crawl re-read 20261102 21:23 UTC)
5. https://arxiv.org/pdf/1803.06643 : ComplexWebQuestions paper (Talmor and Berant): built from WebQuestionsSP queries (read 20261102 20:48 UTC)
6. https://arxiv.org/pdf/2307.07697 : Think-on-Graph (ICLR 2024 version): datasets, Table 9 (read 20261102 20:42 to 20:44 UTC)
7. https://arxiv.org/pdf/2310.01061 : Reasoning on Graphs (ICLR 2024 version); https://huggingface.co/api/datasets/rmanluo/RoG-webqsp : no licence field (read 20261102 20:44 UTC)
8. https://arxiv.org/pdf/2402.07630 : G-Retriever: GraphQA benchmark, Table 2 (read 20261102 20:44 UTC)
9. https://arxiv.org/pdf/2505.23495 : "Diagnosing and Addressing Pitfalls in KG-RAG Datasets" v4 (3 November 2025; NeurIPS 2025 Datasets and Benchmarks): Table 1, Section 3.1, Appendix B (read 20261102 20:45 UTC)
10. https://aclanthology.org/2026.acl-long.489.pdf : OntGQA, ACL 2026 (2-7 July 2026): evaluates on WebQSP (read 20261102 20:47 UTC)