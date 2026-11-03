---
type: index
kind: concept
aliases: [AUC, ROC AUC, area under the ROC curve]
updated: 20261102 21:16 UTC
---

# AUROC

AUROC is the area under the receiver operating characteristic (ROC) curve, a single number for how well a score separates positive cases from negative ones. This entry gives its meaning, the dated steps to it, and where sources judge it differently.

## Definition

An ROC graph plots a classifier's true-positive rate against its false-positive rate as the decision threshold moves. Fawcett writes that the AUC "is equivalent to the probability that the classifier will rank a randomly chosen positive instance higher than a randomly chosen negative instance", and that this equals the Wilcoxon test of ranks (Hanley and McNeil, 1982). Random guessing gives the diagonal, with area 0.5, so no realistic classifier should score below 0.5 [1].

## How it changed

- **By 1975.** ROC graphs were long used in signal detection theory to show the trade-off between hit rates and false alarm rates (Egan 1975, as cited by Fawcett) [1].
- **1982.** Hanley and McNeil, Radiology 143(1): the area equals the probability that a diseased subject is ranked as more suspicious than a non-diseased one, which the Wilcoxon statistic estimates; they give formulas for its standard error and sample sizes [2].
- **1997.** Bradley, Pattern Recognition 30(7), on the use of AUC to evaluate machine-learning algorithms (title only read) [3].
- **2001.** Hand and Till generalise AUC to several classes by averaging pairwise AUCs, as Fawcett describes [1].
- **2006.** Fawcett's introduction (online 20051219; Pattern Recognition Letters 27, pages 861-874) lists common pitfalls [1].
- **2009.** Hand, Machine Learning 77(1), proposes "a coherent alternative to the area under the ROC curve" (title only read) [4].
- **2026.** scikit-learn 1.9.1 documents `roc_auc_score` for binary, multiclass and multilabel targets; multiclass needs an explicit one-vs-rest or one-vs-one choice [5].

## Where sources disagree

- **Class skew.** Fawcett calls ROC curves' insensitivity to class distribution an "attractive property", and shows that precision-recall curves change when negatives grow tenfold while ROC curves do not. He does not say which suits a given task [1]. scikit-learn says its one-vs-rest averaging is "sensitive to class imbalance even when `average == 'macro'`", and that one-vs-one with macro averaging is "insensitive" to it [5].
- **Whether AUC is a sound summary.** Hand's title proposes a "coherent alternative" [4]. His argument is **unstated** here: only the record was read.

## Related

[Mean reciprocal rank](./mean-reciprocal-rank.md), [reranking](./reranking.md), [learning to rank](./learning-to-rank.md), [information retrieval](./information-retrieval.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Applied to Pinakes**

- [Measurements](../applied-to-pinakes/measurements.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://people.inf.elte.hu/kiss/11dwhdm/roc.pdf : Fawcett, "An introduction to ROC analysis", Pattern Recognition Letters 27 (2006) 861-874; introduction, sections 4.2 and 5 (read 20261102 20:45 UTC)
2. https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:7063747%20AND%20SRC:MED&format=json&resultType=core : Europe PMC record of Hanley and McNeil, Radiology 143(1):29-36, 1982, with abstract (read 20261102 20:45 UTC)
3. https://api.crossref.org/works/10.1016/S0031-3203(96)00142-2 : Crossref record: Bradley, Pattern Recognition 30(7):1145-1159, 1997 (read 20261102 20:47 UTC)
4. https://api.crossref.org/works/10.1007/s10994-009-5119-5 : Crossref record: Hand, Machine Learning 77(1):103-123, 2009, title "Measuring classifier performance: a coherent alternative to the area under the ROC curve" (read 20261102 20:48 UTC; re-read 20261102 21:16 UTC)
5. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html : scikit-learn 1.9.1 documentation of `roc_auc_score`, `multi_class` parameter (read 20261102 20:47 UTC; re-read 20261102 21:16 UTC)
