---
type: index
kind: concept
aliases: [slot-filling, KBP slot filling]
updated: 20261102 22:55 UTC
---

# Slot filling

This entry says what slot filling means in knowledge-base work, where the task came from, and why the same two words name an unrelated task in dialogue systems. It follows the knowledge-base sense, which the KILT benchmark uses.

## Definition

The KILT paper states the goal of slot filling as "collect information on certain relations (or slots) of entities" from large collections of natural-language text; its example is the entity Albert Einstein and the relation educated_at [1]. A system must disambiguate the input entity and acquire relational knowledge about it, and the paper names knowledge-base population as an application [1]. In KILT the input is a string "subject entity [SEP] relation" and the output is a list of equally valid object entities, each with the evidence where the fact appears [1]. In the shared task it came from, the attributes ("slots") were derived from Wikipedia infoboxes [2].

## How it changed

- **2009.** NIST's Text Analysis Conference runs a Knowledge Base Population track with two tasks, Entity Linking and Slot Filling; 13 teams from 6 countries take part [3]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **2010.** The track has 23 teams in one or both sub-tasks; Ji and Grishman survey its methods at ACL in June 2011 [2].
- **20170613.** Levy and three co-authors turn relation extraction into reading comprehension, with questions per relation slot and zero-shot transfer to unseen relations (first-party) [4]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20200904.** KILT adds two slot-filling datasets, T-REx and Zero Shot RE [1][5]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20210831.** Glass and three co-authors present a zero-shot system on dense retrieval and [retrieval-augmented generation](./retrieval-augmented-generation.md), ranked first on the KILT leaderboard by their account (first-party) [6].
- **Since 2021.** Scores on the two slot-filling boards, the newest submission and the end of the KILT challenge are on the benchmark page, not here: [KILT](../benchmarks/kilt.md).

## Where sources disagree

**What the words name.** The KILT paper and Ji and Grishman use "slot filling" for filling an entity's relation values from a corpus [1][2]. A 2021 survey of natural language understanding uses it for labelling each word token of a spoken or written request, beside intent detection [7]. The two share only the name. This entry covers the first.

## Related

[Relation extraction](./relation-extraction.md) · [entity linking](./entity-linking.md) · [open-domain question answering](./open-domain-question-answering.md) · [distant supervision](./distant-supervision.md) · [knowledge base](./knowledge-base.md) · [knowledge graph completion](./knowledge-graph-completion.md) · [KILT](../benchmarks/kilt.md) · [KILT Wikipedia snapshot](../datasets/wikipedia-dpr-kilt.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Benchmarks**

- [KILT](../benchmarks/kilt.md)

**Index**

- [Relation extraction](relation-extraction.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/html/2009.02252 : Petroni et al., "KILT: a Benchmark for Knowledge Intensive Language Tasks", section 3.3 (goal, input and output format), Table 1 (T-REx and Zero Shot RE as slot filling) (read 20261102 22:06 UTC)
2. https://aclanthology.org/P11-1115.pdf : Ji and Grishman, "Knowledge Base Population: Successful Approaches and Challenges", ACL 2011: abstract, section on the 2010 track, definition of the Slot Filling task, 23 teams (read 20261102 22:07 UTC)
3. https://aclanthology.org/L10-1435/ : McNamee, Dang et al., "An Evaluation of Technologies for Knowledge Base Population", LREC 2010, abstract: 2009 track, two tasks, 13 teams from 6 countries (read 20261102 22:08 UTC)
4. https://arxiv.org/abs/1706.04115 : Levy et al., "Zero-Shot Relation Extraction via Reading Comprehension", v1 20170613, abstract (first-party; read 20261102 22:06 UTC)
5. https://arxiv.org/abs/2009.02252 : arXiv record of KILT: v1 4 September 2020, v4 27 May 2021 (read 20261102 22:06 UTC)
6. https://arxiv.org/abs/2108.13934 : Glass et al., "Robust Retrieval Augmented Generation for Zero-shot Slot Filling", v1 20210831, abstract (first-party; read 20261102 22:06 UTC)
7. https://arxiv.org/abs/2101.08091 : Weld et al., "A survey of joint intent detection and slot-filling models in natural language understanding", v1 20210120, abstract (read 20261102 22:06 UTC)
