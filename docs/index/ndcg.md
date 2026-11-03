---
type: index
kind: concept
aliases: [normalised discounted cumulative gain, normalized discounted cumulative gain, nDCG@10]
updated: 20261102 22:48 UTC
---

# nDCG

This entry says what nDCG measures, which formulas are in use, and why nDCG@10 became the usual retrieval-benchmark score. It also records where the sources disagree on the formula.

## Definition

nDCG scores a ranked list with graded relevance. Each document's graded gain is divided by a discount that grows with rank; the sum is the discounted cumulated gain (DCG). Dividing by the DCG of an ideal ordering gives a score where 1 is ideal [1][2]. nDCG@10 stops at rank 10; the TREC 2019 Deep Learning track chose it "since it makes use of our 4-level judgments and focuses on the first results that users will see" [6].

## How it changed

- **2000.** Järvelin and Kekäläinen present cumulated gain and DCG [2]. See [The Web changes data and search](../history/the-web.md).
- **200210.** Their ACM TOIS 20(4) article adds the measure relative to the ideal, tested on 20 TREC-7 queries [1][2]. See [The semantic web and linked data](../history/semantic-web.md).
- **2005.** Burges et al. score rankers by NDCG at rank 15 with gain 2^r - 1 and divisor log(1 + j) [3].
- **20130424.** Wang et al. show that NDCG with a logarithmic discount tends to 1 as the list grows, for any ranking function, yet still tells rankers apart [5]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **2019 to 2025.** TREC 2019 Deep Learning makes NDCG@10 its main metric [6]; BEIR (20210417) computes it for all datasets [7]; MTEB (20221013) and MMTEB (20250219) use it as the main retrieval metric [8][9]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).

## Where sources disagree

**The formula.** The 2002 article takes the grade as gain and a log of base b, with no discount below rank b [2]. trec_eval takes the grade as gain and divides by log2(r + 1) at rank r [4]. With b = 2 the first leaves ranks 1 and 2 undiscounted; the second divides rank 2 by log2(3). Burges et al. use gain 2^r - 1 [3]. *Reading:* scores from different tools need not match.

**First appearance.** The 2002 article says CG and DCG were presented in 2000 [2]; Burges et al. cite 2000 for NDCG [3]. The 2000 paper was not read; its content is unstated.

**Theory.** BEIR cites Wang et al. for the metric's "theoretical advantages" [7]; their abstract calls the limit of 1 "very surprising" [5].

## Related

[mean reciprocal rank](./mean-reciprocal-rank.md) · [ranked retrieval](./ranked-retrieval.md) · [TREC](./trec.md) · [learning to rank](./learning-to-rank.md) · [BEIR](../benchmarks/beir.md) · [MS MARCO](../benchmarks/ms-marco.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Benchmarks**

- [BEIR](../benchmarks/beir.md)
- [Benchmarks](../benchmarks/README.md)
- [HotpotQA](../benchmarks/hotpotqa.md)
- [MS MARCO](../benchmarks/ms-marco.md)

**Index**

- [R-precision](r-precision.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.crossref.org/works/10.1145/582415.582418 : Crossref record of Järvelin and Kekäläinen, "Cumulated gain-based evaluation of IR techniques", ACM TOIS 20(4), pp. 422-446, October 2002; abstract (read 20261102 22:10 UTC)
2. https://www.fi.muni.cz/~xkohout7/Research/clanky_cizi/evaluation/p422-jarvelin.pdf : a university-hosted copy of the same article: CG, DCG (eq. 2), normalisation (eq. 5), "originally presented" in 2000, TREC-7 case study (read 20261102 22:12 UTC)
3. https://icml.cc/Conferences/2005/proceedings/papers/012_LearningToRank_BurgesEtAl.pdf : Burges et al., "Learning to Rank using Gradient Descent", ICML 2005, section 6.1, eq. 16 (read 20261102 22:12 UTC)
4. https://github.com/usnistgov/trec_eval/blob/main/m_ndcg.c : trec_eval source of the ndcg measure, read through the GitHub API (read 20261102 22:13 UTC)
5. https://arxiv.org/abs/1304.6480 : Wang et al. (6 authors), "A Theoretical Analysis of NDCG Type Ranking Measures", 20130424, abstract (read 20261102 22:14 UTC)
6. https://arxiv.org/pdf/2003.07820v2 : Craswell et al., "Overview of the TREC 2019 deep learning track", v1 20200317, "Overall results" (read 20261102 22:14 UTC)
7. https://arxiv.org/pdf/2104.08663v4 : Thakur et al., "BEIR", v1 20210417 (v4 read): section 3, nDCG@10 for all datasets, reference [71] (read 20261102 22:14 UTC)
8. https://arxiv.org/pdf/2210.07316v3 : Muennighoff et al., "MTEB", v1 20221013 (v3 read): retrieval task, "nDCG@10 serves as the main metric" (read 20261102 22:14 UTC)
9. https://arxiv.org/pdf/2502.13595v4 : Enevoldsen et al. (86 authors), "MMTEB", v1 20250219 (v4 read), ICLR 2025, retrieval task construction (read 20261102 22:14 UTC)
