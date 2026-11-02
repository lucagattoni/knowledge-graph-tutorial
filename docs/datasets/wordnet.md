---
type: dataset
kinds: [kg]
updated: 20261102 21:28 UTC
---

# WordNet

This page answers what WordNet contains, how large it is, under which licence it is distributed, and how it was made. It is a lexical database of English whose nodes are word senses. Many later resources were built on it: [ConceptNet](conceptnet.md), the [YAGO](yago.md) taxonomy and the [WN18RR](wn18rr.md) test set. No benchmark page is its own; the link-prediction subsets are scored on [the link-prediction benchmark page](../benchmarks/kg-link-prediction.md).

## What it contains

Princeton describes it as a large lexical database of English: nouns, verbs, adjectives and adverbs are grouped into "sets of cognitive synonyms (synsets)", each expressing one concept, and the synsets are linked by conceptual-semantic and lexical relations [2]. A synset carries a short gloss and, mostly, example sentences. A word with several meanings appears in several synsets [2].

The relations differ by part of speech [2]:

- **Nouns:** hypernymy and hyponymy ("is a"), with all hierarchies ending at the root {entity}; instances (specific persons, countries and places, always leaves); part-whole (meronymy).
- **Verbs:** hierarchies of manner (troponyms) and entailment links.
- **Adjectives:** antonymy, plus links to derived nouns ("pertainyms").
- **Across parts of speech:** few links, mostly morphosemantic ones such as observe, observant, observation.

WordNet is in effect four sub-networks, one per part of speech, with few cross-links [2]. The noun hierarchy is a [taxonomy](../index/taxonomy.md).

## Size and versions

Counts for WordNet 3.0, from Princeton's `wnstats` page, as captured by the Internet Archive on 20261003 and re-read on 20261102 [4]:

| Part of speech | Synsets | Unique strings | Word-sense pairs |
|---|---|---|---|
| Noun | 82,115 | 117,798 | 146,312 |
| Verb | 13,767 | 11,529 | 25,047 |
| Adjective | 18,156 | 21,479 | 30,002 |
| Adverb | 3,621 | 4,481 | 5,580 |
| Total | 117,659 | 155,287 | 206,941 |

A Debian copy of the same manual prints 120,982 as the synset total, which is not the sum of its rows [5]; the Archive copy of Princeton's page and the row sums agree on 117,659. That page adds that the unique strings across all four categories number 147,278, because a string unique within one category can occur in several [4]. The 1990 state of the project was about 95,600 word forms in 70,100 meanings [6].

| Release | Date | Form |
|---|---|---|
| 2.1 | March 2005 | Windows package |
| 3.0 | December 2006 | Unix-like source and database |
| 3.1 | undated | database files only, "currently available only online" [3] |

Princeton states that it "is no longer developed" and that no future release is planned [2]. Its community successor, Open English Wordnet, published a 2025 edition on 20251231 and was last pushed on 20261020 [9].

## Licence

Princeton calls WordNet "unencumbered" and usable commercially under its licence, and advises that a lawyer review the licence for the intended use [1]. The licence for release 3.0 grants permission to use, copy, modify and distribute the software and database "for any purpose and without fee or royalty", provided the notice "WordNet 3.0 Copyright 2006 by Princeton University" and the disclaimer appear on all copies, including modified ones. It forbids using Princeton's name in advertising or publicity [1]. Whether the 3.1 files carry the same text is **unstated**. Open English Wordnet is a fork under the WordNet licence plus CC BY 4.0 [9].

## How it was made

In 1985 a group of psychologists and linguists at Princeton began a lexical database based on psycholinguistic findings about the mental lexicon [6]. The first aim was to search dictionaries by concept instead of alphabetically [6]. Lexicographers code the "is a" pointer between senses explicitly, and the inverse pointers are added when their files are converted into the database [6]. Revisions of two print thesauri were "helpful tools" [6]. The founding report is Miller et al., describing the state of 1990 and revised in August 1993 [6]. The journal article is Miller, "WordNet: a lexical database for English", Communications of the ACM 38(11), November 1995, pages 39 to 41 [7].

## Used by

- **Papers.** Miller 1995 is in the [Foundations group](../papers/foundations.md). TransE built its WN set from WordNet senses; the WordNet version is **unstated** in the TransE paper [8]. YAGO 1 combined Wikipedia with "the taxonomy of WordNet" [10]. ConceptNet 5.5 imports it through Open Multilingual WordNet, a linked-data form of WordNet [11].
- **Datasets.** WN18 and WN18RR are cut from WordNet; their sizes, the leakage and the fix are on [the WN18RR page](wn18rr.md) [8][12]; [YAGO](yago.md); [ConceptNet](conceptnet.md).
- **Benchmarks.** [Knowledge graph link prediction](../benchmarks/kg-link-prediction.md).
- **Trends.** No trend page of this documentation uses it as data (checked in the trends folder, 20261102).
- **Citations.** Miller 1995 has 9,187 citing works in Crossref (read 20261102 21:25 UTC) [7]. A Semantic Scholar count was not re-queried.

## Known problems

- **Development stopped.** No release since 3.0 of 2006 except the 3.1 files [2][3].
- **Fine senses.** Navigli calls WordNet "a fine-grained resource" and reports human agreement of 72.5% and 67.3% on two sense-tagging exercises, so about 70% is a credible ceiling for fine-grained [word sense disambiguation](../index/word-sense-disambiguation.md) [13].
- **English only.** Other languages come from separate wordnets, such as the one ConceptNet imports [11].

## Sources

1. https://wordnet.princeton.edu/license-and-commercial-use : licence text, commercial-use statement. The live page returned HTTP 403 to a script on 20261102 20:49 UTC; read as the Internet Archive copy of 20261004 11:34 UTC (read 20261102 20:51 UTC). The same text is at https://spdx.org/licenses/WordNet.html (read 20261102 20:49 UTC)
2. https://wordnet.princeton.edu/ : description, relations, "no longer developed", no planned releases; Internet Archive copy of 20261006 (read 20261102 20:53 UTC)
3. https://wordnet.princeton.edu/download/current-version : versions 2.1, 3.0, 3.1; Internet Archive copy of 20241119 (read 20261102 20:53 UTC)
4. https://wordnet.princeton.edu/documentation/wnstats7wn : WordNet 3.0 statistics; Internet Archive capture of 20261003 00:37 UTC, the live page not fetched; re-read 20261102 21:25 UTC
5. https://manpages.debian.org/jessie/wordnet/wnstats.7wn.en.html : the same manual in the Debian package (read 20261102 20:49 UTC)
6. https://wordnetcode.princeton.edu/5papers.pdf : Miller, Beckwith, Fellbaum, Gross, Miller, "Introduction to WordNet", revised August 1993 (full text read 20261102 20:54 UTC)
7. https://api.crossref.org/works/10.1145/219717.219748 : Miller 1995 record and citing-works count, 9,187 (read 20261102 21:25 UTC)
8. https://papers.nips.cc/paper_files/paper/2013/file/1cecc7a77928ca8133fa24680a88d2f9-Paper.pdf : Bordes et al., TransE, NIPS 2013: section 4.1 and Table 2 (full text read 20261102 20:53 UTC)
9. https://raw.githubusercontent.com/globalwordnet/english-wordnet/main/README.md and LICENSE.md ; `gh api repos/globalwordnet/english-wordnet` : fork, 2025 edition, licence, last push (read 20261102 20:53 UTC)
10. https://yago-knowledge.org/downloads/yago-1 : YAGO 1 built from Wikipedia and the WordNet taxonomy (read 20261102 20:53 UTC)
11. https://arxiv.org/pdf/1612.03975 and https://github.com/commonsense/conceptnet5/wiki/Copying-and-sharing-ConceptNet : WordNet via Open Multilingual WordNet in ConceptNet (read 20261102 20:49 UTC)
12. https://arxiv.org/pdf/1707.01476 : Dettmers et al., ConvE: WN18 and WN18RR as subsets cut from WordNet (full text read 20261102 20:53 UTC)
13. https://aclanthology.org/P06-1014.pdf : Navigli, ACL 2006, introduction (read 20261102 20:55 UTC)
