---
type: index
kind: system
aliases: [Text REtrieval Conference]
updated: 20261102 21:25 UTC
---

# TREC

This entry says what TREC is and how its tasks followed the field, from ad hoc document search to question answering and, since 2024, retrieval-augmented generation. It is the main source of shared test collections for [information retrieval](./information-retrieval.md).

## Definition

The Text REtrieval Conference (TREC) is a workshop series co-sponsored by the US National Institute of Standards and Technology (NIST) and the US Department of Defense. It started in 1992 as part of the TIPSTER Text program, to give the retrieval community the infrastructure for large-scale evaluation [1][2]. Each year NIST supplies documents and questions; participants run their own systems and return ranked lists; NIST pools the results, judges them and scores them; a workshop closes the cycle [1]. Work is split into tracks, each a retrieval task with its own test collection [3].

## How it changed

- **1992.** TREC starts [1]. See [Knowledge systems: boom and bust](../history/knowledge-systems.md).
- **First six years.** NIST states: "Retrieval system effectiveness approximately doubled in the first six years of TREC." This is first-party, and the page gives no method [1].
- **Question answering.** NIST says TREC introduced evaluations for open-domain [question answering](./question-answering.md) and gives no year for the start [1]. The earliest data set on its QA data list is from 1999, TREC-8: 200 questions over TREC disks 4 and 5 [4][5]. See [The Web changes data and search](../history/the-web.md).
- **2019.** The Deep Learning Track is new in TREC 2019. Its overview (arXiv v1, 20200317) calls it the first track with large human-labelled training sets. Deep learning runs "significantly outperformed" traditional runs, and the organisers offer two possible causes: the large training data and the pooling [6]. See [Language models meet retrieval](../history/language-models-meet-retrieval.md) and [MS MARCO](../benchmarks/ms-marco.md).
- **2024.** A Retrieval-Augmented Generation track runs with three tasks over the MS MARCO Segment v2.1 collection, and a conference in November 2024 [7].
- **2026, still moving.** The track's own site calls TREC RAG 2026 "the first Agent-first track at TREC", with a new corpus; submissions were due 20260808 [8]. The TREC site lists the 2026 conference for 20261116 to 20261118 [9]. See [the trends](../trends/README.md).

## Where sources disagree

No disagreement found in the sources read.

## Related

[information retrieval](./information-retrieval.md) · [question answering](./question-answering.md) · [BM25](./bm25.md) · [retrieval-augmented generation](./retrieval-augmented-generation.md) · [web search engine](./web-search-engine.md) · [MS MARCO](../benchmarks/ms-marco.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [The Web changes data and search](../history/the-web.md)

**Index**

- [Information retrieval](information-retrieval.md)
- [Learning to rank](learning-to-rank.md)
- [Mean reciprocal rank](mean-reciprocal-rank.md)
- [nDCG](ndcg.md)
- [Question answering](question-answering.md)
- [R-precision](r-precision.md)
- [Stemming](stemming.md)
- [Web search engine](web-search-engine.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://trec.nist.gov/overview.html : NIST, TREC overview: started 1992 within TIPSTER, purpose, yearly cycle, "approximately doubled in the first six years", open-domain question answering, no year given for it (read 20261102 21:24 UTC)
2. https://trec.nist.gov/about.html : NIST, About TREC: same description on the current site (read 20261102 21:01 UTC)
3. https://trec.nist.gov/tracks.html : NIST, TREC tracks: a track is a retrieval task with its own test collection (read 20261102 21:01 UTC)
4. https://trec.nist.gov/data/qamain.html : NIST, QA track data list: earliest entry "TREC-8 (1999) Question Answering Data" (read 20261102 21:00 UTC)
5. https://trec.nist.gov/data/qa/t8_qadata.html : NIST, TREC-8 QA data: 200 test questions, TREC disks 4 and 5 (read 20261102 21:01 UTC)
6. https://arxiv.org/abs/2003.07820 : Craswell et al., "Overview of the TREC 2019 deep learning track", v1 20200317, abstract (read 20261102 21:01 UTC)
7. https://trec-rag.github.io/trec24/ : TREC RAG track site, 2024 page: three tasks over MS MARCO Segment v2.1, conference November 2024 (read 20261102 21:03 UTC)
8. https://trec-rag.github.io/ : TREC RAG track site, 2026: "first Agent-first track at TREC", ClimbMix-400b corpus, submissions due 20260808 (read 20261102 21:01 UTC)
9. https://trec.nist.gov/ : NIST, TREC home: TREC Conference 20261116 to 20261118; the 2026 participation period has ended; tracks listed include Retrieval Augmented Generation (read 20261102 21:00 UTC)
