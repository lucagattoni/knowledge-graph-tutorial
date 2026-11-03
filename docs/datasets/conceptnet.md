---
type: dataset
kinds: [kg]
updated: 20261102 21:27 UTC
---

# ConceptNet

This page answers what ConceptNet contains, how large it is, under which licence it may be reused, and how it was made. It is an open [knowledge graph](../index/knowledge-graph.md) of the common-sense meaning of words, not of named entities. It has no benchmark page of its own.

## What it contains

Nodes ("terms") are words and phrases of natural language, kept in an undisambiguated form such as `/c/en/lead`; an optional part-of-speech suffix (`/c/en/lead/n`) gives a little disambiguation [5]. Edges ("assertions") are weighted [triples](../index/triple.md) of start term, relation and end term [5]. The relations are a closed set of 36 core relations (the list printed in the paper names 35), among them IsA, UsedFor, CapableOf, PartOf, Synonym and RelatedTo; seven are symmetric [5]. An `ExternalURL` edge links a term to its page in a source such as Wiktionary or WordNet [5].

The assertions file has five tab-separated fields per line: edge URI, relation, start node, end node, and a JSON object with weight, sources, dataset and licence [3]. ConceptNet Numberbatch, a set of word vectors, is "a separate artifact from ConceptNet itself" [5] and is not covered here.

## Size and versions

Counts for version 5.5, from its paper (first-party): over 21 million edges, over 8 million nodes, about 1,500,000 English nodes, 83 languages with at least 10,000 nodes, and 18.1 million edges from Wiktionary alone [5].

| Version | Download path | File dated on the host | Compressed size |
|---|---|---|---|
| 5.5.0 | 2016 | 20161104 | 419,484,773 bytes |
| 5.5.5 | 2017 | 20170818 | 418,576,509 bytes |
| 5.6.0 | 2018 | 20180416 | 471,053,810 bytes |
| 5.7.0 | 2019 | 20190703 | 497,963,447 bytes |

The dates are file timestamps from the download host, not release announcements [7]. The downloads page still names 5.7.0 the "Current version" [3]; the code repository was last pushed on 20230119 [6]. Edge and node counts for 5.7 are **unstated** in the sources read. *Reading:* the data has not changed since mid-2019; treat it as frozen.

## Licence

The `LICENSE.txt` splits the work in two [1]:

| Part | Licence |
|---|---|
| Data | Creative Commons Attribution-ShareAlike 4.0 |
| Code | Apache 2.0, copyright Luminoso Technologies |

The code and the data "are different works" [1]. The sharing page adds that ConceptNet may not be used "in a data set with an incompatible license" and that restrictions such as "non-commercial" may not be added [2]. Wiktionary and Wikipedia material (via DBpedia) is CC BY-SA 3.0, and the WordNet licence text is reproduced for the WordNet part [2]. That page states no licence for Open Multilingual WordNet, JMDict or OpenCyc [2]. The `DATA-CREDITS.txt` file the licence points to was not read.

## How it was made

ConceptNet began as the crowd-sourced Open Mind Common Sense project, launched in 1999 at the MIT Media Lab [4]. Version 5.5 draws on that project and its sister projects, Wiktionary (parsed with a custom parser), games with a purpose, Open Multilingual WordNet, JMDict, OpenCyc and a subset of [DBpedia](dbpedia.md) [5]. Compared with 5.4 it dropped the lemmatizer and relates inflections with a `FormOf` edge [5]. The build can be reproduced with Snakemake [5]. The sharing page credits the MIT Media Lab, the Commonsense Computing Initiative and Luminoso Technologies as developers [2].

## Used by

| Work | What it does with ConceptNet |
|---|---|
| Speer, Chin, Havasi, AAAI 2017 [5] | retrofits the graph onto word2vec and GloVe vectors, giving the Numberbatch word vectors |
| [Petroni et al. 2019](../papers/foundations.md) [8] | uses English ConceptNet facts with single-token objects, 11,458 facts over 16 relations, as one of four knowledge sources for probing language models |
| Bosselut et al., COMET, ACL 2019 [9] | trains a model to generate new ConceptNet assertions |

Scores for these works are in the cited papers; this documentation holds results only on benchmark pages. [WordNet](wordnet.md) and DBpedia are among ConceptNet's inputs [5]. No trend page of this documentation uses it as data (checked in the trends folder, 20261102). The AAAI paper has 1,386 citations in Crossref (read 20261102 21:25 UTC); no Semantic Scholar count was retrieved [10].

## Known problems

- **Share-alike.** Combining ConceptNet with data under an incompatible licence is not allowed [2].
- **Licence text disagrees.** The credit line the sharing page asks software to display names CC BY SA 3.0, while the same page gives 4.0 as the data licence [2]. The repository's licence metadata is unclassified [6].
- **Crowd noise.** The downloads page warns that the raw sentences "are not necessarily true, useful, or appropriate" [3]. An error rate for the assertions is **unstated** in the sources read.
- **Ambiguous nodes by design.** One term covers all senses of a word; disambiguation stops at part of speech [5].
- **Uneven relations.** Specific relations such as UsedFor connect common words; rarer words get only general ones such as Synonym and RelatedTo [5].

## Sources

1. https://raw.githubusercontent.com/commonsense/conceptnet5/master/LICENSE.txt : data CC BY-SA 4.0, code Apache 2.0, "different works" (read 20261102 20:49 UTC)
2. https://github.com/commonsense/conceptnet5/wiki/Copying-and-sharing-ConceptNet : sharing terms, component licences, credit text (raw Markdown of the wiki page, read 20261102 20:49 UTC)
3. https://github.com/commonsense/conceptnet5/wiki/Downloads : file format, version list, "Current version: 5.7.0", warning on raw sentences (raw Markdown, read 20261102 20:49 UTC)
4. https://conceptnet.io/ : project description, 1999 origin, developer (read 20261102 20:49 UTC)
5. https://arxiv.org/pdf/1612.03975 : Speer, Chin, Havasi, "ConceptNet 5.5", AAAI 2017; v1 20161212, v2 20181211 per https://arxiv.org/abs/1612.03975 (full text read 20261102 20:49 UTC; abstract page 20:53)
6. `gh api repos/commonsense/conceptnet5` : licence field "Other"/NOASSERTION, last push 20230119 (read 20261102 20:52 UTC)
7. HTTP headers of the four assertions files on s3.amazonaws.com/conceptnet : Last-Modified and Content-Length (read 20261102 20:55 UTC)
8. https://arxiv.org/pdf/1909.01066 : Petroni et al., "Language Models as Knowledge Bases?", EMNLP 2019: section 4.1.3 and Table 2 (full text read 20261102 20:53 UTC; re-read in the ar5iv text 21:25 UTC)
9. https://arxiv.org/abs/1906.05317 : Bosselut et al., COMET, v1 20190612: the abstract says the model generates commonsense knowledge for ConceptNet and ATOMIC (read 20261102 21:25 UTC)
10. https://api.crossref.org/works/10.1609/aaai.v31i1.11164 : Crossref record and citing-works count of the AAAI paper, 1,386 (read 20261102 21:25 UTC)
