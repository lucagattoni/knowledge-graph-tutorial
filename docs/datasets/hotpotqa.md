---
type: dataset
kinds: [questions, corpus]
benchmark: hotpotqa
updated: 20261102 21:23 UTC
---

# HotpotQA

This page answers what the HotpotQA data contains, how big it is, under which licence it is released and how it was made. It is the best-known English set of [multi-hop](../index/multi-hop-question-answering.md) questions over Wikipedia. Scoring and results are on [the HotpotQA benchmark page](../benchmarks/hotpotqa.md).

## What it contains

About 113 thousand question-answer pairs. Each question needs two Wikipedia paragraphs, and comes with the sentences ("supporting facts") the crowd worker used [1]. There are two types [1]:

- **Bridge:** one entity links two paragraphs. The paper's example asks for the former band of the Mother Love Bone member who died just before its debut album; it needs the paragraph on that band and one on the album Return to Olympus.
- **Comparison:** two entities are compared on a shared property; by design half are yes/no questions.

Each record has `_id`, `question`, `answer`, `supporting_facts` (paragraph title and sentence number), `context`, `type` and `level` (easy, medium, hard) [3]. In the authors' sample of 100 dev and test questions, 42% were chain reasoning through a bridge entity (Type I in the paper) and 27% were comparisons [1]. The kinds are *questions* and *corpus* (Wikipedia paragraphs) [5].

## Size and versions

| Split | Examples |
|---|---|
| train-easy / train-medium / train-hard | 18,089 / 56,814 / 15,661 |
| dev | 7,405 |
| test-distractor / test-fullwiki | 7,405 / 7,405 |

The total is 112,779 [1]. Two context formats exist [1][3]:

- **Distractor:** 2 gold paragraphs plus 8 distractors found with bigram [tf-idf](../index/tf-idf.md).
- **Fullwiki:** the first paragraphs of all Wikipedia articles (over 5,000,000). The dev and test files hold the authors' top-10 retrieved paragraphs, which may miss the gold ones.

The test-fullwiki file has no answers. No distractor test file is listed; distractor test scoring runs submitted code [3]. The source is the English Wikipedia dump of 1 October 2017 [1]. The processed dump is 7,413,895,794 bytes; an archive of the introductory paragraphs (added 14 January 2019) is 1,553,565,403 bytes [5]. The paper is dated 25 September 2018 (EMNLP 2018); the files are train v1.1, dev v1 and test v1; the repository's last push was 20210426 [1][3][4].

**Count conflict.** The three train subsets sum to 90,564 [1]. The Hugging Face card and a 2026 paper list 90,447 [6][14]. The reason for the difference of 117 is **unstated**.

## Licence

The data is "distributed under a CC BY-SA 4.0 License" [2]. The repository README, the Hugging Face card and the processed Wikipedia release agree [3][5][6]. The code is Apache-2.0: the repository's `LICENSE.txt` is the Apache text [4]. There is no separate licence file for the data. The licence of the underlying Wikipedia text was not read: **unstated**.

## How it was made

1. Take the October 2017 dump and build a directed graph from hyperlinks in the first paragraphs [1].
2. Restrict bridge entities to 591 hand-curated categories; draw comparison pairs from 42 curated lists of similar entities [1].
3. Show each pair to Amazon Mechanical Turk workers (a pair was bridge with probability 0.75, else comparison). Workers wrote a question that needs both paragraphs and marked the supporting sentences [1].
4. Split by difficulty. Top contributors, who wrote over 70% of the data, gave train-easy (mostly single-hop). A model trained with three-fold cross-validation answered 60% of the rest with high confidence: train-medium. The remainder became train-hard, dev and the two tests [1].

## Used by

- **Papers (all use it as an evaluation or training set).** ReAct [16] and IRCoT [15] (see [agentic search](../papers/agentic-search.md)); KAG [17], HippoRAG [10] and HippoRAG 2 [20] (see [graph-based RAG](../papers/graph-based-rag.md)); Search-R1, which trains on it [18], and Graph-R1 [19] (see [learned traversal](../papers/learned-graph-traversal.md)).
- **Derived sets.** [2WikiMultiHopQA](2wikimultihopqa.md) builds templates from its comparison questions [9]; [MuSiQue](musique.md) was designed against its shortcuts [8]; BeerQA includes it [2]; [KILT](../benchmarks/kilt.md) and [BEIR](../benchmarks/beir.md) re-use it [12][13].
- **Trends and project.** [Graph-based RAG](../trends/graph-based-rag.md), [agentic graph retrieval](../trends/learned-graph-traversal.md), [agentic search](../trends/agentic-search.md); [HippoRAG](../projects/hipporag.md).
- **Citations.** 1,807 in OpenAlex (read 20261102 20:03, carried over from this documentation's research notes; the arXiv-DOI record shows 97; unverified in the last check) [21].

## Known problems

- **Many questions are not multi-hop.** In the authors' dev and test sample, 6% were single-hop and 2% unanswerable [1]. Min et al. show that most distractor-setting questions can be answered by reading one paragraph at a time, and that humans shown only some of the needed paragraphs still answered over 80% [7] (the score is on [the benchmark page](../benchmarks/hotpotqa.md)). MuSiQue's authors call it "largely solvable without multihop reasoning" [8] (see [disconnected reasoning](../index/disconnected-reasoning.md)); HippoRAG's authors call it "a much weaker test for multi-hop reasoning" [10].
- **Difficulty is relative to a 2018 model.** Dev and test hold only examples that model could not answer; train-medium has a different mix of types [1].
- **Little graph structure.** A 2026 study measures an average entity-graph degree of 0.65 (2.27 in its own novel corpus) and 78.2% fact-retrieval questions, and argues such sets cannot test graph structure [11].
- **Frozen and public.** The snapshot is from 2017 [1]. Pretraining overlap and [contamination](../index/data-contamination.md) are **unstated**.

## Sources

1. https://arxiv.org/abs/1809.09600 : HotpotQA paper v1 (25 Sep 2018), full text at arxiv.org/html/1809.09600: construction, Tables 1-3, appendix A, C (read 20261102 20:41 UTC; Section 4 and Table 3 re-read 20261102 21:20 UTC)
2. https://hotpotqa.github.io/ : project page: description, licence sentence, files, BeerQA remark (read 20261102 20:41 UTC)
3. https://raw.githubusercontent.com/hotpotqa/hotpot/master/README.md : files, JSON fields, test-set notes, licence (read 20261102 20:41 UTC; files and submission re-read 20261102 21:20 UTC)
4. https://api.github.com/repos/hotpotqa/hotpot (via `gh api`) and `LICENSE.txt` : Apache-2.0, last push 20210426 (read 20261102 20:44 UTC)
5. https://hotpotqa.github.io/wiki-readme.html : processed Wikipedia, sizes, CC BY-SA 4.0 (read 20261102 20:45 UTC)
6. https://huggingface.co/datasets/hotpotqa/hotpot_qa : card: licence, splits (read 20261102 20:41 UTC)
7. https://arxiv.org/abs/1906.02900 : Min et al., ACL 2019: abstract and Section 3: most distractor-setting questions answerable with a single-hop model; humans over 80% on part-paragraph input (read 20261102 21:22 UTC)
8. https://arxiv.org/abs/2108.00573 : MuSiQue paper v3, full text: related work, Figure 1 (read 20261102 20:42 UTC)
9. https://arxiv.org/abs/2011.01060 : 2WikiMultiHopQA paper v2, full text: templates from HotpotQA comparison questions (read 20261102 20:42 UTC)
10. https://arxiv.org/abs/2405.14831 : HippoRAG v3, full text: datasets, "much weaker test" (read 20261102 20:42 UTC)
11. https://arxiv.org/abs/2506.05690 : Xiang et al. v3 (22 Feb 2026), full text: degree 0.65, 78.2% (read 20261102 20:42 UTC)
12. https://arxiv.org/abs/2104.08663 : BEIR v4: HotpotQA among the datasets (read 20261102 20:42 UTC)
13. https://arxiv.org/abs/2009.02252 : KILT v4: HotpotQA among the datasets (read 20261102 20:42 UTC)
14. https://arxiv.org/abs/2604.09666 : RAGSearch v1 (1 Apr 2026), Table 6: train 90,447 (read 20261102 20:42 UTC)
15. https://arxiv.org/abs/2212.10509 : IRCoT abstract: four datasets incl. HotpotQA (read 20261102 20:42 UTC)
16. https://arxiv.org/abs/2210.03629 : ReAct abstract: HotpotQA and FEVER (read 20261102 20:42 UTC)
17. https://arxiv.org/abs/2409.13731 : KAG abstract: HotpotQA among the evaluation sets (read 20261102 20:42 UTC)
18. https://arxiv.org/abs/2503.09516 : Search-R1 v5, full text: NQ and HotpotQA training sets merged (read 20261102 20:42 UTC)
19. https://arxiv.org/abs/2507.21892 : Graph-R1 v2 (2 Jun 2026), full text: six datasets (read 20261102 20:42 UTC)
20. https://arxiv.org/abs/2502.14802 : HippoRAG 2 v2, full text: HotpotQA among the sampled sets (read 20261102 20:42 UTC)
21. https://api.openalex.org/works/doi:10.18653/v1/d18-1259 : 1,807 citations (read 20261102 20:03 UTC, via the research notes of this documentation; not re-queried)
