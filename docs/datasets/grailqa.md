---
type: dataset
kinds: [questions]
updated: 20261102 21:27 UTC
---

# GrailQA

This page answers what the GrailQA data contains, how big it is, under which terms it is released, how it was made and where it is weak. GrailQA has 64,331 crowd-worded questions over [Freebase](freebase.md), each with its answer and a logical form, and it is built so that a test question can be new in three different ways. It has no benchmark page in this documentation, so this page describes the splits and the metrics but gives no system results.

## What it contains

Each question comes with its answers and with the query that produces them, written as [SPARQL](../index/sparql.md), as an S-expression and as a graph query [1][2]. Questions cover all 86 domains of Freebase Commons, with up to four relations and one optional function: counting, a superlative or a comparative [2]. This is the task of [knowledge-base question answering](../index/knowledge-base-question-answering.md) by [semantic parsing](../index/semantic-parsing.md). The distribution, from the paper [2]:

| Property | Counts |
|---|---|
| Relations in the query | 1: 44,340; 2: 16,610; 3: 3,254; 4: 127 |
| Function | none: 53,526; count: 3,463; superlative: 4,111; comparative: 3,231 |
| Distinct canonical logical forms | 4,969, over 3,720 relations and 1,534 classes |

Question ids carry the canonical form in their first eight digits, so questions that share them are paraphrases or other groundings of one query. The public test file masks everything except the question [3].

## Size and versions

| Split | Questions | Composition of validation and test |
|---|---:|---|
| Train | 44,337 | |
| Validation | 6,763 | 25% i.i.d., 25% compositional, 50% zero-shot (5 held-out domains) |
| Test | 13,231 | same shares (10 held-out domains) |

I.i.d. questions reuse schema items and logical forms seen in training, compositional ones combine seen items in a new way, and zero-shot ones use items or whole domains not seen in training [2].

The paper's protocol uses two metrics. Exact match (EM) is the share of questions whose predicted and gold logical forms are semantically equivalent, checked by graph isomorphism. F1 compares the predicted and gold answer sets, and gives partial credit to systems that predict answers without a logical form [2]. The project page gives the download as 120 MB and ranks systems on a leaderboard that scores a hidden test set; test labels are not released [4]. The files are named `v1.0`; no other version is stated [4]. The paper appeared at the Web Conference 2021 (arXiv v1 20201116, v6 20210222) [2]. The repository was last pushed on 20251009 [1][5].

## Licence

Three statements apply, for three things. The project page says the dataset is "distributed under the CC BY-SA 4.0 license" [4]. The repository `LICENSE` is Apache-2.0 and covers the code [5]. The paper is CC BY 4.0 [2]. The README itself states no data licence. The terms of the Freebase facts and of the web mention data used for entity names are **unstated** here; see the Freebase page.

## How it was made

1. **Logical forms.** An algorithm samples graph-shaped queries from the Freebase ontology and grounds them on entities. A graduate student keeps a form only if a real user could plausibly ask it; 86.5% were approved [2].
2. **Canonical questions.** Graduate students write one question per form, and a second student cross-checks it [2].
3. **Paraphrases.** Amazon Mechanical Turk workers, native English speakers with a task approval rate of at least 95%, write paraphrases until five pass a check by other workers. 17.4% of paraphrases were discarded [2].
4. **Entity names.** Common surface forms for each entity, such as "Obama", are mined from FACC1, a Freebase annotation of the ClueWeb web corpus. At least three workers judge each mined form, and forms chosen by fewer than 60% of them are dropped [2].
5. **Sampling.** Each canonical form is grounded on several entity sets, and questions are drawn so that wordings and groundings vary [2].

The result is 4,969 canonical forms, 29,457 paraphrases and 64,331 questions, made by 11 graduate students and 6,685 crowd workers [2].

## Used by

- **Papers and trend.** Think-on-Graph prompts a language model to walk a knowledge graph and tests it on GrailQA, among nine sets, using 1,000 questions sampled from the test set "to save computational cost" [6] ([papers](../papers/learned-graph-traversal.md); trend: [agentic graph retrieval](../trends/learned-graph-traversal.md)).
- **Datasets.** The paper's Table 1 compares its size with WEBQ (4,737 questions; the paper describes it as WebQuestions plus later logical-form annotations by Yih et al., which is [WebQuestionsSP](webquestionssp.md); the match is this page's inference), COMPLEX WEBQ ([ComplexWebQuestions](complexwebquestions.md)), SIMPLE Q ([SimpleQuestions](simplequestions.md)), QALD and GRAPH Q, and calls itself "by far the largest dataset on KBQA with complex questions", a first-party claim [2].
- **Audit.** A 2025 audit of 16 knowledge-graph QA sets includes it [7].

## Known problems

- **Label noise.** The authors checked 100 canonical questions and their paraphrases and found a 5.6% error overall [2]. A third-party audit judged 30.00% of 60 sampled test items correct. Its examples: an answer that names a final match, not the league; a list of Eocene fossils that stops at one [7]. The sample is small, and the project page says test labels are not public, so how the audit obtained test answers is **unstated** [4][7].
- **Freebase is frozen.** The paper notes that Freebase "has stopped getting updated" [2], so answers cannot follow later facts.
- **Heavy to run.** Reproducing the baselines needs a local Freebase in a Virtuoso triple store [1]; test scores need a leaderboard submission [4].

## Sources

1. https://github.com/dki-lab/GrailQA : README: size, generalisation levels, setup with Virtuoso, citation; `data/README.md`; folder list (read 20261102 20:53 UTC)
2. https://arxiv.org/abs/2011.07743 : Gu, Kase, Vanni and four others (7 authors), "Beyond I.I.D.: Three Levels of Generalization for Question Answering on Knowledge Bases", WWW 2021; arXiv v1 16 Nov 2020, v6 22 Feb 2021; full text: Sections 2, 3, 5.1, Table 1; Task 3 (surface forms), Table 1 rows and the Evaluation metrics paragraph re-read 20261102 21:24 UTC, the rest read 20261102 20:54 UTC
3. https://github.com/dki-lab/GrailQA/blob/main/Specification.md : data format, masked public test (read 20261102 20:55 UTC)
4. https://dki-lab.github.io/GrailQA/ : project page: CC BY-SA 4.0 sentence, 120 MB, hidden test, news dates (read 20261102 20:54 UTC)
5. https://github.com/dki-lab/GrailQA/blob/main/LICENSE : Apache License 2.0; repository metadata, last push 20251009 (read 20261102 20:53 UTC, via `gh api`)
6. https://arxiv.org/abs/2307.07697 : Think-on-Graph, ICLR 2024 version: Section 3.1.1 and Table 9 (read 20261102 20:55 UTC)
7. https://arxiv.org/abs/2505.23495 : "Diagnosing and Addressing Pitfalls in KG-RAG Datasets" v4 (3 November 2025): Table 1, Section 3.1, Appendix C (read 20261102 20:55 UTC)