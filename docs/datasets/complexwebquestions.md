---
type: dataset
kinds: [questions]
updated: 20261102 21:31 UTC
---

# ComplexWebQuestions

This page answers what ComplexWebQuestions (CWQ) contains, which of its two versions matters, and what is known to be wrong with it. It is 34,689 complex questions built from the [WebQuestionsSP](webquestionssp.md) questions, each with a [SPARQL](../index/sparql.md) query over [Freebase](freebase.md), its answers and web snippets [1][3].

## What it contains

Each question has its text, the machine-generated question it was paraphrased from, a SPARQL query, answers with Freebase ids and aliases, the seed question's id, and an unchecked type estimate (composition, conjunction, comparative or superlative) [5]. 70% of questions have one answer, and the mean answer set has 2.3 members [1]. The share of each type in the released file is **unstated** in the sources read; the generation shares are under How it was made.

The data serves three uses: search-engine question answering, reading comprehension over 12,725,989 released web snippets (366.8 per question on average), and [semantic parsing](../index/semantic-parsing.md) with the SPARQL [3]. Snippets are about 100 per query, in Google's order [5]. Test answers are withheld; predictions are scored by email submission [3][5].

## Size and versions

34,689 examples [1]. There are two versions. **1.0** (the NAACL 2018 paper [2]) cut the data at random into 80% train, 10% dev and 10% test; **1.1** repartitioned it by seed question after a leak was found (see Known problems) [1][4]. The repartition report was submitted to arXiv on 20180725 [4]. The project page's news line announcing 1.1 reads "1/7/2018"; the order of day and month is not stated, so the release date of 1.1 is **unstated** [3].

| Copy | Train | Dev | Test | Source |
|---|---|---|---|---|
| 1.1 as quoted in an uploader's card | 27,734 | 3,480 | 3,475 | [5] |
| Copy used by RoG, GNN-RAG and OntGQA | 27,639 | 3,519 | 3,531 | [8][9][10] |

Both sum to 34,689. Why they differ, and where the second copy's test answers come from, is **unstated** in the sources read; Think-on-Graph's table mixes the two (27,734 train, 3,531 test) [7]. Snippet counts: 10,035,571 train, 1,350,950 dev, 1,339,468 test [5]. Answers were computed on the Freebase dump `freebase-rdf-2015-08-02-00-00` [3].

## Licence

**Unstated.** The project page, as archived 20250107, asks users to cite the paper and gives no licence [3]. The code repository has none either (GitHub reports none) [6]. An uploader's Hugging Face card says `apache-2.0` in its metadata and "Not specified" under Licensing Information [5]. Terms of the third-party snippets: **unstated**. Freebase terms are on the Freebase page.

## How it was made

1. **Seeds.** Question-query pairs sampled from WebQuestionsSP, which has 4,737 questions [1].
2. **Harder queries.** Rules add a composition step, a conjunction, a superlative or a comparative to a seed query, and the new query is run on Freebase. The paper gives the shares used when generating: composition 45% of the times, conjunctions 45%, superlatives 5%, comparatives 5% [1].
3. **Machine questions.** 687 hand-written templates, covering 462 Freebase predicates, turn each new query into an awkward question [1].
4. **Paraphrase.** On Amazon Mechanical Turk, 200 workers took part; one paraphrased each machine question, one or two validated, and a bonus rewarded large edits. Cost averaged $0.11 per question [1]. The snippets were harvested by the authors' own model through Google [1][5].

## Used by

- **Papers.** Think-on-Graph evaluates prompted models on it with Freebase as the graph [7] ([papers](../papers/learned-graph-traversal.md)). Reasoning on Graphs trains on it with WebQuestionsSP [8]. GNN-RAG and OntGQA (ACL 20260702-07) use it [9][10]. GraphWalker (COLM 2026) and Search-on-Graph-R1 (20260720) name it in their abstracts [14]. A 2025 audit counts about 30 papers from 2022 to 2025 that use WebQuestionsSP or CWQ [11].
- **Datasets.** HotpotQA and 2WikiMultiHopQA cite it as a multi-hop set built from a knowledge base [12][13].
- **Trend.** [Agentic graph retrieval](../trends/learned-graph-traversal.md).
- **Citations.** 520 in OpenAlex (read 20261102 20:04, not re-queried; the count moves with time) [15].

## Known problems

- **Train-test [leak](../index/data-contamination.md) in 1.0.** Questions made from one seed could land in both train and test, with high probability [4]. The report trained a reader on the CWQ training data and scored precision@1 on dev. With the paper's question-splitting method (SplitQA) the score was 55.0 on 1.0 and 31.1 on 1.1; with the question sent whole (SimpQA) it was 47.8 on 1.0 and 30.6 on 1.1. A reader pretrained on SQuAD, not trained on CWQ, barely moved: SimpQA 20.4 on 1.0, 20.5 on 1.1 [4].
- **Wrong labels.** An audit sampled 300 of 3,531 test questions, two annotators each: 49.33% had a correct answer. Examples: "current queen" answered Elizabeth II, and a film question with an incomplete answer set [11].
- **Artificial questions.** The authors say the "question distribution is artificial from a semantic perspective" [1].
- **Frozen Freebase.** Answers date from August 2015 [3], and an audit says Freebase "ceased maintenance in 2016" [11].
- **Missing home.** Three project addresses (`nlp.cs.tau.ac.il`, `tau-nlp.org`, `tau-nlp.sites.tau.ac.il`) refused the connection or returned 404 on 20261102; only the archived page could be read [3].

*Reading:* still the usual second Freebase set, but read its scores with the audit in mind.

## Sources

1. https://arxiv.org/pdf/1803.06643 : CWQ paper v1 (Talmor, Berant; arXiv 20180318): sections 4 to 6, Table 4 (read 20261102 20:51 to 20:52 UTC); generation shares in section 4.2 re-read in the HTML version https://ar5iv.labs.arxiv.org/html/1803.06643 (read 20261102 21:28 UTC)
2. https://aclanthology.org/N18-1059/ : NAACL 2018, pp. 641-651 (read 20261102 21:00 UTC)
3. https://web.archive.org/web/20250107065453/https://www.tau-nlp.org/compwebq : project page as archived 20250107 (news line "1/7/2018", uses, counts, Freebase dump, no licence); the three live addresses were tried in the same window (read 20261102 20:54 to 20:56 UTC; news line re-read 21:27 UTC)
4. https://arxiv.org/abs/1807.09623 : "Repartitioning of the ComplexWebQuestions Dataset" (arXiv 20180725, one version), full text, Tables 3 and 4 (read 20261102 20:55 to 20:57 UTC; Tables 3 and 4 and the leak passage re-read in https://ar5iv.labs.arxiv.org/html/1807.09623 at 21:28 UTC)
5. https://huggingface.co/datasets/drt/complex_web_questions : uploader's card: fields, split and snippet counts, licence lines (read 20261102 20:56 to 20:57 UTC)
6. https://raw.githubusercontent.com/alontalmor/WebAsKB/master/README.md : code README; GitHub API licence field null (read 20261102 20:55 to 20:56 UTC)
7. https://arxiv.org/pdf/2307.07697 : Think-on-Graph v6: Tables 1 and 9 (read 20261102 20:57 to 20:58 UTC)
8. https://arxiv.org/pdf/2310.01061 : Reasoning on Graphs: Table 6; https://huggingface.co/api/datasets/rmanluo/RoG-cwq : copy's split counts (read 20261102 20:57 to 20:58 UTC)
9. https://arxiv.org/pdf/2405.20139 : GNN-RAG: datasets, appendix C (read 20261102 20:57 to 20:58 UTC)
10. https://aclanthology.org/2026.acl-long.489.pdf : OntGQA (ACL 20260702-07): Tables 1 and 2 (read 20261102 20:59 UTC)
11. https://arxiv.org/pdf/2505.23495v4 : audit of KGQA datasets v4 (20251103): Table 1, Appendix B (read 20261102 20:58 UTC)
12. https://arxiv.org/pdf/1809.09600 : HotpotQA paper, introduction and related work (read 20261102 20:59 UTC)
13. https://arxiv.org/pdf/2011.01060 : 2WikiMultiHopQA paper, related work (read 20261102 20:59 UTC)
14. https://export.arxiv.org/api/query : counts of abstracts naming "ComplexWebQuestions" or "CWQ", and the abstracts of 2603.28533 and 2607.18481 (read 20261102 20:59 to 21:00 UTC)
15. https://api.openalex.org/works/doi:10.18653/v1/n18-1059 : 520 citations (read 20261102 20:04 UTC; carried over from this chapter's research pool, which is not in the archive; not re-queried)
