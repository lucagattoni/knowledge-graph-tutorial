---
type: index
kind: concept
aliases: [precision at R, Rprec]
updated: 20261102 22:27 UTC
---

# R-precision

This entry answers what R-precision measures, where it comes from, and how the KILT benchmark changed what the R stands for.

## Definition

For a query with R known relevant documents, R-precision is the precision of the top R results: the share of them that are relevant [1]. Manning, Raghavan and Schütze say it "adjusts for the size of the set of relevant documents": a perfect system can score 1 on every query, while precision at 20 cannot pass 0.4 when only 8 documents are relevant [1]. At rank R precision equals recall, so R-precision is the break-even point, and it is empirically highly correlated with mean average precision [1]. The trec_eval tool describes it as "Precision after R documents have been retrieved" [2].

## How it changed

- **After the first TREC.** The trec_eval source says the measure was "Originally developed for IR rankings by Chris Buckley after TREC 1", and cites Buckley and Voorhees, *TREC: Experiment and Evaluation in Information Retrieval* (MIT Press, 2005) (first-party) [2]. NIST dates the start of [TREC](./trec.md) to 1992 [3]; the year of the measure itself is unstated. See [Knowledge systems: boom and bust](../history/knowledge-systems.md).
- **2008.** The textbook *Introduction to Information Retrieval* (Cambridge University Press) describes it in section 8.4 [1]; the trec_eval source file for it carries a 2008 copyright [2]. See [The semantic web and linked data](../history/semantic-web.md).
- **20200904.** The KILT paper is first posted; its text (read at version 4, 20210527) redefines the measure per Wikipedia page: R is the number of pages in a provenance set, and the best value over an input's provenance sets is reported. KILT scores award points only when R-precision is 1 [4]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md).

## Where sources disagree

**What R is.** The textbook defines R as the size of a set of known relevant documents, which may be incomplete when it comes from pooled judgements [1]. trec_eval takes the total number of relevant documents for the topic [2]. KILT takes the pages of one provenance set, and an input may have several sets [4]. For most KILT datasets R is 1, so R-precision there equals precision at 1; the exceptions are FEVER (about 12% of inputs need more than one page) and HotpotQA (always two pages) [4]. *Reading:* the name is shared, the quantity differs; KILT's version is closer to a pass-or-fail test than to a ranking score.

## Related

[information retrieval](./information-retrieval.md) · [TREC](./trec.md) · [ranked retrieval](./ranked-retrieval.md) · [mean reciprocal rank](./mean-reciprocal-rank.md) · [nDCG](./ndcg.md) · [provenance](./provenance.md). Benchmark: [KILT](../benchmarks/kilt.md). Data: [KILT Wikipedia snapshot](../datasets/wikipedia-dpr-kilt.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Benchmarks**

- [KILT](../benchmarks/kilt.md)

**Index**

- [Provenance](provenance.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://web.archive.org/web/20250215175331/https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html : Manning, Raghavan and Schütze, *Introduction to Information Retrieval* (© 2008 Cambridge University Press), section 8.4: R-precision, size of the relevant set, break-even point, correlation with MAP. The Stanford host did not answer on the read date, so this is an Internet Archive copy of 20250215 17:53 UTC (read 20261102 22:08 UTC)
2. https://github.com/usnistgov/trec_eval/blob/main/m_Rprec.c : trec_eval source file for the measure Rprec: definition, history note, citation of Buckley and Voorhees, copyright 2008 Chris Buckley (first-party; read 20261102 22:08 UTC)
3. https://trec.nist.gov/overview.html : NIST, TREC overview: started in 1992 (read 20261102 22:09 UTC)
4. https://arxiv.org/abs/2009.02252 : Petroni et al., "KILT: a Benchmark for Knowledge Intensive Language Tasks", v1 20200904, v4 20210527: section 5 (R-precision as r/R, maximum over provenance sets, KILT scores, FEVER and HotpotQA), full text at https://arxiv.org/html/2009.02252 (read 20261102 22:07 UTC)
