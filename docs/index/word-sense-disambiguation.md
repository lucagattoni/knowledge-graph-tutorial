---
type: index
kind: concept
aliases: [WSD, word-sense disambiguation, sense disambiguation]
updated: 20261102 22:52 UTC
---

# Word sense disambiguation

This entry says what word sense disambiguation (WSD) is, when the task was posed, and how its accuracy compares with the human ceiling.

## Definition

Navigli's survey (ACM Computing Surveys 41(2), 200902) defines WSD as "the ability to identify the meaning of words in context in a computational manner" and calls it an "AI-complete problem" [1]. The output is a sense for the word in context, chosen from a pre-defined sense inventory; Princeton WordNet is the de facto standard one [2]. Word sense induction is a different task: it clusters instances into groups that "may have no relation to standard sense partitions" [3]. Hogan et al. treat WSD as a pre-processing step linking a word to a lexicon sense; [entity linking](./entity-linking.md) links a mention to a knowledge-graph node [4].

## How it changed

- **19490715.** Weaver's memorandum "Translation" poses the problem: "Fast" may mean "rapid" or "motionless", and N neighbouring words might settle which [5]. Bevilacqua et al. trace the task to him [2]. See [The advent](../history/advent.md) (from 1950).
- **1986 and 199506.** Lesk matches a word's context against dictionary definitions [6][7]. Yarowsky's unsupervised algorithm "rivals the performance of supervised techniques" (first-party) [3]. See [Knowledge systems](../history/knowledge-systems.md) and [The Web changes data and search](../history/the-web.md).
- **2017 to 2021.** On five pooled test sets, the best overall F1 of the systems compared was 69.7 in 2017 [7]; the 2021 survey lists 80.7 for ESCHER and says pretrained language models play a crucial role [2]. See [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md) and [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20250311.** Basile et al. note that interest in the classical task "has decreased" since LLMs; zero-shot LLMs "cannot surpass" the best earlier methods, a fine-tuned medium-sized one does [10].
- **20260719.** Philippov et al. (first-party benchmark) report frontier LLMs near 95% on a corrected, multiple-choice set [8].

## Where sources disagree

**The human ceiling.** Navigli (2006) puts a credible bound for fine-grained WSD "around 70%" [9]. Bevilacqua et al. give 67 to 80% (citing Navigli 2009) and call 80% a "glass ceiling" [2]. Philippov et al. call fine-grained senses "partly ill-posed even for experts" [8].

**Solved or not.** The 2021 survey: the best systems are "close to or superior to" the human bound, yet the task "is still not solved" [2]. The 2026 authors: labels, not models, are the bottleneck [8]. *Reading:* the figures do not compare: 80.7 F1 on the Raganato benchmark, against about 95% accuracy when the model picks from supplied senses [2][8].

## Related

[WordNet](./wordnet.md) · [entity linking](./entity-linking.md) · [BERT](./bert.md) · [large language model](./large-language-model.md). Datasets: [WordNet](../datasets/wordnet.md), [ConceptNet](../datasets/conceptnet.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Datasets**

- [WordNet](../datasets/wordnet.md)

**Index**

- [Entity linking](entity-linking.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.crossref.org/works/10.1145/1459352.1459355 : Crossref record of Navigli, "Word sense disambiguation: A survey", ACM Computing Surveys 41(2), February 2009: abstract (definition, "AI-complete"). The full text could not be fetched: the author's hosts timed out (read 20261102 22:10 UTC)
2. https://www.ijcai.org/proceedings/2021/0593.pdf : Bevilacqua, Pasini, Raganato, Navigli, "Recent Trends in Word Sense Disambiguation: A Survey", IJCAI-21: abstract, introduction (Weaver, sense inventory), section 2.1 (WordNet as de facto standard), section 4.1 (agreement 67-80%), Table 1 (ESCHER 80.7), section 4.2, conclusion (full text read 20261102 22:11 UTC)
3. https://aclanthology.org/P95-1026.pdf : Yarowsky, "Unsupervised Word Sense Disambiguation Rivaling Supervised Methods", ACL 1995 (June, Cambridge, Massachusetts per the Anthology record https://aclanthology.org/P95-1026/, read 20261102 22:14 UTC): abstract, footnote 1 on sense induction (first-party; PDF read 20261102 22:11 UTC)
4. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", sections 6.2.1 (pre-processing, WSD) and 6.2.3 (entity linking) (read 20261102 22:14 UTC)
5. https://www.mt-archive.net/50/Weaver-1949.pdf : Weaver, "Translation", memorandum signed 15 July 1949, section 5 "Meaning and Context" (first-party; read 20261102 22:11 UTC)
6. https://api.crossref.org/works/10.1145/318723.318728 : Crossref record of Lesk, "Automatic sense disambiguation using machine readable dictionaries", SIGDOC '86, Toronto, pages 24-26 (read 20261102 22:14 UTC)
7. https://aclanthology.org/E17-1010.pdf : Raganato, Camacho-Collados, Navigli, EACL 2017 (3-7 April): abstract, section 2.2 (Lesk overlap with definitions), Tables 2 and 4 (best overall F1 69.7: IMS-s+emb trained on SemCor plus OMSTI) (full text read 20261102 22:11 UTC)
8. https://arxiv.org/abs/2609.17554 : Philippov et al., "English Word Sense Disambiguation in 2026: When the Labels Become the Bottleneck", abstract: about 95% (best 95.6%) on lexEN-v1, multiple choice among supplied WordNet senses, Fleiss kappa 0.537; the arXiv record dates the first version 20260719 (first-party; read 20261102 22:14 UTC)
9. https://aclanthology.org/P06-1014.pdf : Navigli, "Meaningful Clustering of Senses Helps Boost Word Sense Disambiguation Performance", ACL 2006: introduction (agreement 72.5% and 67.3%, bound around 70%) (read 20261102 22:10 UTC)
10. https://arxiv.org/abs/2503.08662 : Basile et al., "Exploring the Word Sense Disambiguation Capabilities of Large Language Models", v1 20250311, abstract (read 20261102 22:14 UTC)
