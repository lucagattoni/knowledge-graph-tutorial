---
type: index
kind: concept
aliases: [MRR, MRR@k, reciprocal rank]
updated: 20261102 21:25 UTC
---

# Mean reciprocal rank

Mean reciprocal rank (MRR) scores a ranked list by how high the first correct item sits. This entry gives the definition, dated uses, and the argument over averaging reciprocal ranks.

## Definition

In the TREC-8 question answering track report, a system returned up to five ranked answer strings per question. A question scored the reciprocal of the rank of the first correct response, or 0 if none of the five was correct. A run's score was the mean over questions [1]. With r the rank of the first relevant item, the reciprocal rank is 1/r [2]. MRR@K averages the reciprocal rank of the first relevant chunk per query "considering the top-K retrieved set" [3]. The report names three advantages: it is closely related to average precision, it lies between 0 and 1, and it averages well [1].

## How it changed

- **19991117 to 19991119.** The TREC-8 conference is held [4]. Its question answering track scores 45 runs on 198 questions by MRR [1]. Era: [The Web changes data and search](../history/the-web.md).
- **201712.** Fuhr argues that MRR should not be computed (see below) [2]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20190113.** Nogueira and Cho report a re-ranker "outperforming the previous state of the art by 27% (relative) in MRR@10" on MS MARCO passage ranking (first-party) [5]. The task's README says evaluation uses MRR [6]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20210417.** BEIR computes nDCG@10 for all its datasets (version 4 read) [7].
- **20231220.** Moffat posts "The Case for Reciprocal Rank" (full title in the sources) [8].
- **20240127.** MultiHop-RAG scores retrieval with MAP@K, MRR@K and Hit@K [3].

## Where sources disagree

Fuhr holds that reciprocal rank is only an ordinal scale, because ranks 1 and 2 differ as much as ranks 2 and infinity, so its mean is not allowed. In his example, system A finds the first relevant item at ranks 1, 2 and 4, system B at rank 2 each time. A wins on MRR (0.58 against 0.5) but loses on average rank. He proposes the mean first-relevant rank instead [2]. Moffat's abstract takes the opposite position: categorical-to-numeric mappings may be averaged when "an argued connection" supports them [8]. The abstract does not name Fuhr, so whether it replies to him is unstated; only the abstract was read.

## Related

[Ranked retrieval](./ranked-retrieval.md), [TREC](./trec.md), [question answering](./question-answering.md), [reranking](./reranking.md), [reciprocal rank fusion](./reciprocal-rank-fusion.md), [multi-hop question answering](./multi-hop-question-answering.md). Benchmarks: [MS MARCO](../benchmarks/ms-marco.md), [MultiHop-RAG](../benchmarks/multihop-rag.md), [BEIR](../benchmarks/beir.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Benchmarks**

- [Benchmarks](../benchmarks/README.md)
- [Knowledge graph link prediction](../benchmarks/kg-link-prediction.md)
- [MS MARCO](../benchmarks/ms-marco.md)
- [OGB link prediction](../benchmarks/ogb-link-prediction.md)
- [STaRK](../benchmarks/stark.md)

**Applied to Pinakes**

- [Measurements](../applied-to-pinakes/measurements.md)

**Index**

- [AUROC](auroc.md)
- [BERT](bert.md)
- [Knowledge graph embedding](knowledge-graph-embedding.md)
- [Learning to rank](learning-to-rank.md)
- [Link prediction](link-prediction.md)
- [Multi-hop question answering](multi-hop-question-answering.md)
- [nDCG](ndcg.md)
- [R-precision](r-precision.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://trec.nist.gov/pubs/trec8/papers/qa_report.pdf : Voorhees, "The TREC-8 Question Answering Track Report", in NIST Special Publication 500-246 (the proceedings page lists it at page 77); scoring, 45 runs, 198 questions (scanned file, read by OCR; read 20261102 21:02 UTC)
2. http://sigir.org/wp-content/uploads/2018/01/p032.pdf : Fuhr, "Some Common Mistakes In IR Evaluation, And How They Can Be Avoided", section 2.1; issue listing at http://sigir.org/forum/issues/december-2017/ gives SIGIR Forum 51(3), December 2017, pages 32-41 (read 20261102 20:56 UTC)
3. https://arxiv.org/pdf/2401.15391 : Tang and Yang, "MultiHop-RAG", v1 20240127, evaluation section defining MAP@K, MRR@K, Hit@K (read 20261102 21:03 UTC)
4. https://trec.nist.gov/proceedings/proceedings.html : NIST SP 500-246, TREC-8, "held in Gaithersburg, Maryland, November 17-19, 1999" (read 20261102 20:56 UTC)
5. https://arxiv.org/abs/1901.04085 : Nogueira and Cho, "Passage Re-ranking with BERT", v1 20190113, abstract (read 20261102 21:02 UTC)
6. https://github.com/microsoft/MSMARCO-Passage-Ranking : README, "Evaluation will be done using MRR" (read 20261102 20:56 UTC)
7. https://arxiv.org/pdf/2104.08663 : Thakur et al., "BEIR", 5 authors, v1 20210417 (version 4 read), "compute nDCG@10 for all datasets" (read 20261102 21:02 UTC)
8. https://arxiv.org/abs/2312.12672 : Moffat, "Categorical, Ratio, and Professorial Data: The Case for Reciprocal Rank", v1 20231220, abstract, re-read through the arXiv API (read 20261102 21:24 UTC)
