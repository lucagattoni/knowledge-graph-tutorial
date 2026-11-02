---
type: dataset
kinds: [questions, corpus]
benchmark: musique
updated: 20261102 21:22 UTC
---

# MuSiQue

This page answers what the MuSiQue data contains, how it was built, and under which licence it is released. It is a set of 2- to 4-hop questions, each with 20 paragraphs of context, made by composing single-hop questions. How systems are scored on it, and the results, are on [the MuSiQue benchmark page](../benchmarks/musique.md).

## What it contains

Each item is a multi-hop question, 20 Wikipedia paragraphs (supporting ones plus distractors), the answer, and the list of supporting paragraphs [1]. Because the questions are composed bottom-up, each also carries its decomposition into single-hop questions with answers, in one of six reasoning-graph shapes [1].

Two variants share the answerable questions [1]:

- **MuSiQue-Ans**: the answerable questions.
- **MuSiQue-Full**: each answerable question is paired with an unanswerable twin. In the twin, the answer to one randomly chosen single-hop question appears in none of the context paragraphs [1].

It is an English, Wikipedia-based set [1].

## Size and versions

| Split | 2-hop | 3-hop | 4-hop | Total |
|---|---|---|---|---|
| Train | 14,376 | 4,387 | 1,175 | 19,938 |
| Dev | 1,252 | 760 | 405 | 2,417 |
| Test | 1,271 | 763 | 425 | 2,459 |

MuSiQue-Ans has 24,814 questions in all. MuSiQue-Full has twice as many in each cell (one answerable, one unanswerable) [1]. The whole set draws on 21,020 distinct single-hop questions and 7,676 supporting paragraphs [1].

The paper is in its third arXiv version (5 May 2022) and appeared in TACL, volume 10, pages 539-554, in 2022 [1][4]. Files are named `v1.0`; the last push was 20240612 [2]. The release also holds the IDs of the single-hop questions used in dev and test [2]. Test scores come from uploading predictions to a leaderboard [2]; whether the test answers are public is **unstated**. Hugging Face copies (for example `dgslibisey/MuSiQue`) are not the authors' release and carry no licence field [5].

## Licence

The authors state that "MuSiQue is distributed under a CC BY 4.0 License" [2]. The repository's `LICENSE` file is the Creative Commons Attribution 4.0 text, and GitHub's licence endpoint reports `cc-by-4.0` [3]. The ACL Anthology licenses its post-2016 materials, the paper among them, under CC BY 4.0 as a site-wide rule [4]. The licences of the five seed datasets (SQuAD, Natural Questions, MLQA, T-REx, Zero Shot RE) were not read: **unstated** here.

## How it was made

The paper's pipeline has eight steps, S1 to S8 [1]:

1. Start from about 2.0 million single-hop questions from the five Wikipedia-based seed sets (Figure 2 of [1] shows "2017K"). Five trained QA models remove likely annotation errors; 760 thousand remain.
2. Find composable pairs: the answer of one question is a named entity mentioned in the other. This gives 12 million 2-hop candidates. Three same-entity checks confirm both mentions are one entity: a spaCy entity-type match, the same top Wikipedia search result, and the same result from a Wikification ([entity linking](../index/entity-linking.md)) model.
3. Filter disconnected pairs with two filters. The head filter keeps a first question only if two trained Longformer models answer it with a mean answer F1 below 0.5 without context. The tail filter keeps a second question only if models score low on it with the bridge entity masked (answer F1 at most 0.25, or at most 0.75 with imperfect support), given one gold and nine distractor paragraphs retrieved with [BM25](../index/bm25.md) via Elasticsearch. About 3.2 million connected pairs remain (Figure 2).
4. Chain pairs into 2- to 4-hop graphs of six shapes, with caps on reuse.
5. Split into train, dev and test with minimal overlap of questions, answers and paragraphs.
6. Build a 20-paragraph context: the supporting paragraphs plus distractors retrieved from other questions' gold paragraphs. The paper does not name the retrieval algorithm here (*Reading:* probably the BM25 setup of step 3, an inference).
7. Have 17 qualified Mechanical Turk workers write each composed question (about 11 thousand USD). Workers pruned 8% of pairs.
8. For Full, add the unanswerable twin.

The aim was a set where answering needs every step ("connected reasoning"), not a shortcut ([disconnected reasoning](../index/disconnected-reasoning.md)) [1].

## Used by

- **Papers.** [RAGSearch](../benchmarks/ragsearch.md) uses the full dev set (2,417) as one of six QA sets [6]. The HippoRAG 2 paper samples 1,000 questions and uses a corpus of 11,656 passages (its Table 1) [7]; 1,000 questions with 20 paragraphs each would give up to 20,000, so passages are probably shared across questions (*Reading:* an inference from the counts). A Cognee tuning paper names MuSiQue in its abstract [8].
- **Projects.** [HippoRAG](../projects/hipporag.md) reports retrieval and cost figures on it (Tables 3 and 12 of [7]). [Cognee](../projects/cognee.md) is the system tuned in [8].
- **Trends.** [Graph-based RAG](../trends/graph-based-rag.md) lists it among its benchmarks; [Agentic graph retrieval](../trends/learned-graph-traversal.md) quotes RAGSearch's MuSiQue figures.
- **Benchmarks.** [MuSiQue](../benchmarks/musique.md) and [RAGSearch](../benchmarks/ragsearch.md). The paper compares it with the sibling [multi-hop](../index/multi-hop-question-answering.md) sets [HotpotQA](hotpotqa.md) and [2WikiMultiHopQA](2wikimultihopqa.md) [1].
- **Citations.** The paper has 286 citations in OpenAlex (read 20261102 20:04, not re-queried; the count moves with time) [9].

## Known problems

- **Seed leakage.** MuSiQue was composed from questions in SQuAD, Natural Questions and others. Single-hop questions in its dev and test sets may occur in those sets' training data. The authors ask users of the seed sets to avoid the released IDs [2]. See [data contamination](../index/data-contamination.md).
- **Model-filtered.** Pair selection used Longformer, RoBERTa and UnifiedQA models, so the set may inherit their blind spots (*Reading:* from the pipeline in [1], not measured).
- **Reused as a retrieval set.** It was designed for a fixed 20-paragraph context [1]; retrieval papers pool or swap the context. See [the benchmark page](../benchmarks/musique.md).
- **Pretraining overlap.** Whether current models saw the Wikipedia text or the seed sets: **unstated**.

## Sources

1. https://arxiv.org/html/2108.00573v3 and https://arxiv.org/pdf/2108.00573 : MuSiQue paper v3 (5 May 2022): construction steps S1 to S8, Table 2 sizes, Figure 2 counts (PDF), crowdsourcing, quality checks (read 20261102 21:16 UTC; first read 20:41)
2. https://github.com/StonyBrookNLP/musique : README: licence sentence, usage caution, files, leaderboards; GitHub API: last push 20240612 (read 20261102 21:15 UTC; first read 20:41)
3. https://github.com/StonyBrookNLP/musique/blob/main/LICENSE : CC BY 4.0 text; GitHub licence endpoint `cc-by-4.0` (read 20261102 20:41 UTC)
4. https://aclanthology.org/2022.tacl-1.31/ : TACL volume 10, pages 539-554, 2022; page footer: post-2016 materials under CC BY 4.0 (read 20261102 21:15 UTC)
5. https://huggingface.co/api/datasets/dgslibisey/MuSiQue and https://huggingface.co/api/datasets/bdsaglam/musique : community copies, download counts, no licence field (read 20261102 20:41 and 20:43 UTC)
6. https://arxiv.org/html/2604.09666 : RAGSearch v1 (1 April 2026): six QA sets, Musique dev 2,417 (Table 6) (read 20261102 21:15 UTC)
7. https://arxiv.org/html/2502.14802 : HippoRAG 2 v2 (19 June 2025): 1,000 queries and 11,656 passages (Table 1), Tables 3 and 12 (read 20261102 21:15 UTC)
8. https://arxiv.org/abs/2505.24478 : Cognee tuning paper v1 (30 May 2025), abstract names the three sets (read 20261102 20:43 UTC)
9. https://api.openalex.org/works/doi:10.1162/tacl_a_00475 : 286 citations (read 20261102 20:04 UTC; carried over from this chapter's research pool, which is not in the archive; not re-queried)
