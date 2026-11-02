---
type: dataset
kinds: [questions]
updated: 20261102 21:31 UTC
---

# SimpleQuestions

This page answers what SimpleQuestions contains, how it was made and what limits its use. It is 108,442 English questions, each answered by one [Freebase](freebase.md) fact, released by Facebook AI Research with an arXiv paper of June 2015 [1]. It is the large single-fact set of [knowledge-base question answering](../index/knowledge-base-question-answering.md).

## What it contains

Each item is a question written by a human annotator and the [triple](../index/triple.md) (subject, relationship, object) of Freebase that answers it; the answer is the object [1]. Example from the paper: "What does Jimmy Neutron do?" with (jimmy neutron, fictional character occupation, inventor) [1].

Each question carries a whole fact, so the paper counts a prediction as correct when the subject and the relationship are right ("path-level accuracy"); the object is not checked [1]. A later study uses "subject-relation pair accuracy" [5].

## Size and versions

The paper shuffled the questions and cut them 70%, 10% and 20%: 75,910 for training, 10,845 for validation and 21,687 for test, 108,442 in all [1]. Questions are tied to FB2M, an extract of Freebase; the paper also uses the larger FB5M [1].

| Freebase extract | Entities | Relationships | Grouped facts |
|---|---|---|---|
| FB2M | 2,150,604 | 6,701 | 10,843,106 |
| FB5M | 4,904,397 | 7,523 | 12,010,500 |

Grouped facts merge all objects of one subject and relationship [1]. Versions: the authors' downloads page, archived 20200102, offers "SimpleQuestions (v2)" and says v2 adds the Freebase subsets used in the paper (the note reads "Dec. 15", with no year); the file was `SimpleQuestions_v2.tgz` on Dropbox [2]. A Hugging Face mirror lists a download of about 423 MB (not downloaded) [4]. Releases after v2: **unstated**.

## Licence

**Unstated.** The authors' page, archived 20200102, has no licence text in its SimpleQuestions section [2]. The address `fb.ai/babi` and the Facebook research download addresses now redirect to a general Meta page that does not mention SimpleQuestions [3]. A Hugging Face mirror carries the tag `cc-by-3.0`, but its card body says "More Information Needed" and it is an uploader's copy, not the authors' statement [4]. Think-on-Graph's table lists "CC License" with no variant and no source, so it is no evidence [6]. Terms of the Freebase facts are on the Freebase page.

## How it was made

1. **Shortlist.** Start from FB2M. Drop facts with an undefined relationship type (the name contains "freebase"). Drop facts whose subject and relationship pair has more than 10 objects, which would give questions such as "Name a person who is an actor?" [1].
2. **Sample.** Each fact gets a probability that falls with how often its relationship occurs, to favour variety [1].
3. **Write.** Annotators saw the fact with links to freebase.com, wrote a question whose answer is the object, were told to vary the wording across similar relationships, and could skip a fact [1].

Number of annotators, pay and quality checks: **unstated** [1].

## Used by

- **Papers.** Think-on-Graph tests prompted models on 1,000 randomly chosen test questions, with Freebase as the graph, beside [ComplexWebQuestions](complexwebquestions.md), [WebQuestionsSP](webquestionssp.md) and [GrailQA](grailqa.md) [6] ([papers](../papers/learned-graph-traversal.md)). Petrochuk and Zettlemoyer study its ceiling [5]. A September 2026 paper names SimpleQuestions among three sets for paraphrase robustness; its abstract does not say which release, or whether Freebase is used [8].
- **Datasets.** The paper co-trains on WebQuestions, the set behind WebQuestionsSP [1]. An audit lists SimpleDBpediaQA, a remap of SimpleQuestions to [DBpedia](dbpedia.md) [7].
- **Trend.** [Agentic graph retrieval](../trends/learned-graph-traversal.md), through Think-on-Graph; the trend page does not name the set.
- **Citations.** 528 in OpenAlex (read 20261102 20:04, not re-queried; the count moves with time) [9].

## Known problems

- **Ambiguity ceiling.** Petrochuk and Zettlemoyer find 3,675 of 10,845 examples (the validation size) unanswerable from the wording, since several subject-relation pairs fit; guessing by frequency lifts the ceiling to 85.2%. Another 1,587 of 86,755 questions do not name the subject. The bound is 83.4% on FB2M [5]. They judge the set "nearly solved" [5].
- **Close to the ceiling.** In the same paper, the authors' own CRF tagger plus BiLSTM baseline reaches 78.1% subject-relation accuracy [5]. This is a first-party result, a separate one from their ceiling analysis, and it is not an independent run.
- **A retired knowledge base.** A 2025 audit says Freebase "ceased maintenance in 2016" [7]. The DBpedia remap scored 43.33% factually correct on 60 sampled items [7]; that is a different set and no measure of SimpleQuestions itself.
- **Unreliable copies.** The mirror's metadata lists 75,910 examples for all three splits, which contradicts the paper [1][4]. Think-on-Graph's table gives 14,894 training questions without explanation [6].
- **Home page gone.** The authors' downloads address now redirects to a general Meta page [3].

*Reading:* a historical set. It still runs, but it measures one lookup against a frozen Freebase extract, and its ceiling is documented.

## Sources

1. https://arxiv.org/pdf/1506.02075 : SimpleQuestions paper v1 (Bordes, Usunier, Chopra, Weston; arXiv 20150605): sections 2 and 6, Tables 1 to 4 (read 20261102 20:51 to 20:52 UTC)
2. https://web.archive.org/web/20200102082609/https://research.fb.com/downloads/babi/ : authors' downloads page as archived 20200102: SimpleQuestions section, v2 note, Dropbox link, no licence text (read 20261102 20:52 to 20:55 UTC)
3. https://fb.ai/babi , https://research.facebook.com/downloads/babi/ , https://ai.meta.com/resources/ : redirect chain; page text searched for "SimpleQuestions" and "bAbI" (read 20261102 20:52 to 20:53 UTC)
4. https://huggingface.co/datasets/fbougares/simple_questions_v2 : mirror card and metadata: licence tag, split counts, download size (read 20261102 20:54 to 20:55 UTC)
5. https://arxiv.org/abs/1804.08798 : Petrochuk and Zettlemoyer, "SimpleQuestions Nearly Solved" (arXiv 20180424): full text (read 20261102 20:54 to 20:58 UTC); abstract re-read for the 83.4% bound and the 78.1% baseline (read 20261102 21:28 UTC)
6. https://arxiv.org/pdf/2307.07697 : Think-on-Graph, v6 of 20240324 (ICLR 2024): datasets, Tables 1, 9 and 14 (read 20261102 20:57 to 20:58 UTC)
7. https://arxiv.org/pdf/2505.23495v4 : "Diagnosing and Addressing Pitfalls in KG-RAG Datasets" v4 (20251103): Table 1, Appendix A and B (read 20261102 20:58 UTC)
8. https://arxiv.org/abs/2609.21227 : Hallucination-R1, abstract, submitted 20260918, via the arXiv API (read 20261102 21:00 UTC)
9. https://api.openalex.org/works/doi:10.48550/arxiv.1506.02075 : 528 citations (read 20261102 20:04 UTC; carried over from this chapter's research pool, which is not in the archive; not re-queried)
