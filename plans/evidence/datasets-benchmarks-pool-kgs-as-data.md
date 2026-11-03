# Candidate pool: public knowledge graphs and the link-prediction sets derived from them

Researcher area: knowledge graphs and knowledge bases used as data. Written 20261102 (UTC), clock readings from `date -u`.
Numbers in square brackets point to the source list at the end. Read times in that list are the nearest clock reading
taken in the same working step, so each is accurate to about plus or minus 3 minutes. Where the sources are silent the
text says **unstated**. The archive leads (`kb-kg/papers-benchmarks/README.md`, `kb-kg/literature/graph-rag-research.md`,
`pinakes/experiments/datasets-benchmark.md`) were searched for these items; only the two pages named under "Archive
pages" below mention any of them [54].

## Overview table

| Slug | Name | Role | Kinds | Licence (own statement) | Citation count of its paper (Semantic Scholar) |
|---|---|---|---|---|---|
| `wikidata` | Wikidata | dataset | kg | CC0 for structured data; CC BY-SA 4.0 for text in other namespaces [1] | 2,849 (CACM 2014, read 20261102 20:01) [53] |
| `dbpedia` | DBpedia | dataset | kg | CC BY-SA 3.0 and GFDL (about page) [12]; per-dataset licences on the Databus unstated [14] | 5,925 (ISWC 2007); 3,738 (SWJ 2015), read 20261102 20:01 [53] |
| `yago` | YAGO | dataset | kg | changes by version: GFDL (1), CC BY 3.0 (3), CC BY-SA (4, 4.5), CC BY 4.0 (4.6) [17-23] | see "Citation counts" at the end |
| `freebase` | Freebase | dataset | kg | CC BY for the dumps; CC0 for the Wikidata mappings [9] | 6,061 (SIGMOD 2008), read 20261102 20:05 [53] |
| `conceptnet` | ConceptNet | dataset | kg | CC BY-SA 4.0 (data); Apache 2.0 (code) [25][26] | see "Citation counts" at the end |
| `wordnet` | WordNet | dataset | kg | WordNet 3.0 licence, permissive with a notice condition [30] | see "Citation counts" at the end |
| `fb15k` | FB15k | both | kg | unstated | see "Citation counts" at the end |
| `wn18` | WN18 | both | kg | unstated | see "Citation counts" at the end |
| `fb15k-237` | FB15k-237 | both | kg | unstated on its download page [44] | see "Citation counts" at the end |
| `wn18rr` | WN18RR | both | kg | unstated | ConvE paper: 3,294 (read 20261102 19:51) [53] |
| `yago3-10` | YAGO3-10 | both | kg | unstated | ConvE paper: 3,294 [53] |
| `wikidata5m` | Wikidata5M | both | kg (with aligned text) | unstated on the dataset page [36] | KEPLER paper: 900 (read 20261102 19:51) [53] |
| `ogbl-wikikg2` | ogbl-wikikg2 | both | kg | CC-0 [39] | see "Citation counts" at the end |
| `codex` | CoDEx (S, M, L) | both | kg | repository MIT [33][34]; data licence unstated | see "Citation counts" at the end |

Suggested slugs for pages: the dataset page and the benchmark page of one item can share the slug, because they sit
in different folders (`docs/datasets/fb15k-237.md` and `docs/benchmarks/fb15k-237.md`).

Archive pages that use these items [54]: `kb-kg/primer/README.md` (timeline rows for DBpedia 2007, Freebase 2008,
Google Knowledge Graph 20120516, Wikidata 20121029, the Freebase shutdown) and `kb-kg/papers-benchmarks/README.md`
(Text2KGBench row: Wikidata-TekGen and DBpedia-WebNLG). No other archive page names FB15k, WN18, YAGO, CoDEx,
ConceptNet, WordNet or OGB. The projects pages only match on the word "Codex" (the coding agent), which is unrelated.

A scope note for the writer: this pool covers KGs as data and the completion subsets. The question sets built on
Wikidata or DBpedia (QALD, LC-QuAD and the like) and Text2KGBench are another researcher's area and were not read.

---

# Datasets: the source graphs

## wikidata

**Role:** dataset (kinds: kg). Not a benchmark.

### What it contains
A collaboratively edited knowledge base. The core unit is the item (identifier Q plus a number); an item has a label,
a description and aliases. Statements consist of a property (P plus a number) and a value, and carry their sources as
references. Sitelinks connect an item to pages on client wikis such as Wikipedia [6]. Lexemes and EntitySchemas are
further structured namespaces [1].

### Size and versions
- The Statistics page reads 123,865,222 items and 2,563,229,601 edits since launch, 48,941 active users [3].
- The MediaWiki API on 20261102 19:47 gave 123,871,360 "articles" (MediaWiki's content-page count, not checked against
  the item count), 2,563,423,620 edits, 8,171,787 registered users, 129,679,520 pages in all namespaces [2].
- **Statement count: unstated** on the pages read (the dump page and the Statistics page give none) [3][5].
- No version numbers; it changes every minute. Full dumps: JSON "created on a weekly basis" [5]; RDF in Turtle and
  N-Triples ("all" dumps), and "truthy" N-Triples that keep only best-rank direct values, without qualifiers and
  references [5].
- Dump files listed on 20261102: `latest-all.json.gz` 156,705,985,721 bytes (27 Oct 2026), `latest-all.json.bz2`
  103,565,615,653, `latest-all.nt.gz` 509,231,082,342, `latest-all.ttl.gz` 309,453,216,156, `latest-truthy.nt.gz`
  71,803,150,133 [4]. For comparison the dump page quotes 130.53 GiB for the 20240101 JSON gz [5].
- Because it moves, every derived benchmark pins a snapshot: ogbl-wikikg2 uses May, August and November 2015 [38];
  Wikidata5M the July 2019 dump [35]. See `ogbl-wikikg2` and `wikidata5m`.

### Licence
"All structured data (i.e. the main, Property, Lexeme, and EntitySchema namespaces) is released into the public domain
under Creative Commons Zero"; text in other namespaces is CC BY-SA 4.0 [1]. Wikidata requires CC0 for what it hosts,
so data under any other licence is not compatible [1].

### How it was made
Edited and maintained by volunteers who "decide on the rules of content creation"; bots also enter data [6]. It
launched on 29 October 2012, developed mainly by Wikimedia Deutschland (tertiary source, Wikipedia; one search summary
showed 30 October on some mirrors, which the Wikipedia text attributes to the mailing-list announcement) [7]. The
first plan had three phases: central interlanguage links, central infobox data, then list articles [7]. Freebase
was folded in: Freebase announced on 16 December 2014 that it was closing and offering its content to Wikidata; it
became read-only on 31 March 2015 [8]. The Freebase-to-Wikidata migration paper (Pellissier Tanon et al., WWW 2016) is
a good source for the move; its abstract (read) gives no counts of facts moved [11].

### Used by
- Derived link-prediction sets: `ogbl-wikikg2`, `wikidata5m`, `codex` [38][35][32].
- Other KGs built on it: YAGO 4, 4.5 and 4.6 take Wikidata as their source [18][19][22]; DBpedia's main knowledge graph
  includes "cleaned data from Wikipedia in all languages and Wikidata" [15].
- Text2KGBench's Wikidata-TekGen part (archive: `kb-kg/papers-benchmarks/README.md`) [54].

### Known problems
- A moving target: the 2015 snapshot in ogbl-wikikg2 and the 2019 snapshot in Wikidata5M are different graphs, so
  scores on the two are not comparable. *Reading:* this follows from the two snapshot dates [38][35].
- Like every KG it holds only positive statements, so unseen is not false (open-world assumption); evaluation sets need
  negatives built or checked by hand [32].
- YAGO's authors describe Wikidata as "much larger (but not consistent)", which is why YAGO 4 keeps a consistent
  subset; YAGO 4.6 also ships the statements it dropped [20][19]. This is the YAGO team's claim, not measured here.

### Usage evidence
Paper: Vrandečić and Krötzsch, "Wikidata: a free collaborative knowledgebase", CACM 2014. Semantic Scholar
citation count **2,849**, read 20261102 20:01 [53]. Archive pages: `kb-kg/primer/README.md` (launch row, Freebase
shutdown), `kb-kg/papers-benchmarks/README.md` (Text2KGBench) [54].

---

## dbpedia

**Role:** dataset (kinds: kg).

### What it contains
Structured content extracted from Wikimedia projects, "a crowd-sourced community effort", published as Linked Data and
queryable with SPARQL [12]. The community ontology has 768 classes and 3,000 properties [13][15]. The home page says
the knowledge graph holds "more than 228 million entities to date" and about 20 language chapters; the Marvin bot
"releases 21 Billion triples per month" from 140 Wikipedia languages; a beta "Largest Diamond" collection has
220 million entities and 1.45 billion triples [14][15]. The 2015 journal paper (a preprint was read) says more than
1.8 billion facts and more than 100 languages [16].

### Size and versions
Versioning runs through the DBpedia Databus. "Latest Core Releases" come as a monthly development version and a
snapshot release every three months [13]. The home page gives no version number [13]. The size figures above are the
project's own and mix different collections (core, all languages, Wikidata-fused); a single comparable number is
**unstated**.

### Licence
The About page says the data is available under CC BY-SA 3.0 and the GNU Free Documentation License [12]. The Resources
page states a licence only for the beta "Fusion" graph (Business Source License 1.1) and none for the other
collections [14]. So the licence of a given Databus artifact is **unstated** in what was read; check the artifact.

### How it was made
Started in 2007 by Sören Auer and Jens Lehmann at the University of Leipzig and Christian Bizer, with OpenLink [12].
Mapping-based infobox extraction uses manually written mappings from Wikipedia infoboxes to the DBpedia ontology; the
raw infobox extraction needs no mappings and gives lower quality [16]. The authors write that extracted data is
"unlikely to reach the quality of completely manually curated data sources" [16].

### Used by
ConceptNet takes a subset of DBpedia [28]. Text2KGBench's DBpedia-WebNLG part (archive) [54].

### Known problems
Extraction quality below curated sources, by the authors' own statement [16]. The raw infobox data is lower quality [16].
Per-dataset licence unclear on the project pages [14].

### Usage evidence
Papers: Auer et al., "DBpedia: A Nucleus for a Web of Open Data", ISWC 2007: **5,925** citations; Lehmann et al.,
"DBpedia - A large-scale, multilingual knowledge base extracted from Wikipedia", Semantic Web journal 2015: **3,738**
(Semantic Scholar, read 20261102 20:01) [53]. Archive: `kb-kg/primer/README.md` (2007 timeline row) [54].

---

## yago

**Role:** dataset (kinds: kg). Versions differ a lot; a page should have one table per version.

### What it contains, size and versions
| Version | Size as the YAGO site states it | Built from | Licence as the site states it |
|---|---|---|---|
| YAGO 1 (2008) | more than 2 million entities, 20 million facts; manually evaluated, "an accuracy of 95% with respect to the extraction source" | Wikipedia (2008-10-01 version, categories and infoboxes) and the WordNet taxonomy | GNU Free Documentation License [23] |
| YAGO 3 | more than 17 million entities, more than 150 million facts; accuracy "manually evaluated" at 95% | Wikipedias in ten languages, WordNet, GeoNames and others; mostly 2013 and 2014 snapshots; paper at CIDR 2015 | data CC BY 3.0; code GPL 3 or later [21] |
| YAGO 4 | more than 50 million entities, 2 billion facts (as read) | facts from Wikidata; schema.org classes; Rust code | data CC BY-SA (3.0); code GPL 3 or later [22] |
| YAGO 4.5 | 49 million entities, 109 million facts | derived from Wikidata, top-level classes and properties from schema.org; Turtle files, SHACL constraints, RDF* fact annotations; SIGIR 2024 resource paper | CC BY-SA [18] |
| YAGO 4.6 | 39 million entities, 167 million facts | based on Wikidata; human-readable identifiers; schema.org top level; SHACL; includes files of statements excluded from Wikidata | CC BY (4.0) [19] |

The size and licence figures in this table were re-read from the raw pages of the five versions on 20261102 20:18 [19][21][22][23][18]. The home page says YAGO 4.6 is out (July 2026) and a newer version is in preparation; no release date appears on the
version pages [17][18][19]. Entities fall from 49 to 39 million between 4.5 and 4.6 while facts rise from 109 to 167
million; the pages give no reason **(unstated)**.

### How it was made
Entities are organised into classes in a taxonomy, and a manually defined schema constrains which relations can hold;
YAGO is "a logically consistent subset" of Wikidata [20]. Facts are RDF with schema.org predicates and RDF* for facts
about facts [20]. Earlier versions (1 to 3) combined Wikipedia with WordNet and GeoNames [21][23].

### Used by
`yago3-10` is a subset of YAGO 3 [41]. Rossi et al. and Akrami et al. use it for link prediction [46][49].

### Known problems
- YAGO 4 and later drop Wikidata statements that break the schema; 4.6 publishes them separately [19][20].
- The licence changed with the version (GFDL, CC BY, CC BY-SA, CC BY); a page must name the version [21-23][18][19].
- The YAGO3-10 subset is dominated by duplicate relations; see `yago3-10`.

### Usage evidence
Papers: Suchanek et al., "YAGO: a core of semantic knowledge", WWW 2007; Mahdisoltani et al., "YAGO3", CIDR 2015.
Citation counts: see the final table of counts (see the table "Citation counts").
Archive pages: none.

---

## freebase

**Role:** dataset (kinds: kg). Shut down; a historical dataset.

### What it contains
"a practical, scalable tuple database used to structure general human knowledge", collaboratively created, with
"more than 125,000,000 tuples, more than 4000 types, and more than 7000 properties" at the 2008 paper; read and write
access through an HTTP graph-query API with MQL [10]. By the TransE paper (2013) it held "around 1.2 billion triplets
and more than 80 million entities" [45]. Its mediator nodes (compound value types) left marks on derived benchmarks;
see `fb15k-237`.

### Size and versions
The last public dump: Freebase Triples 1.9 billion triples (22 GB gzipped, 250 GB uncompressed; the page says
"Updated: Weekly", which conflicts with its own statement that the datasets are not maintained); Deleted Triples 63
million (updated 9 June 2013); Freebase/Wikidata mappings 2.1 million triples (28 October 2013) [9].

### Licence
Freebase data dumps CC BY; the Freebase/Wikidata mappings CC0 [9].

### How it was made
Collaborative editing against a typed schema, per the 2008 paper (Bollacker, Evans, Paritosh, Sturge, Taylor, SIGMOD
2008) [10]. Who ran it from 2010 and what the import sources were are **unstated** in the pages read (the primer in
the archive says it was rooted partly in public sources such as Wikipedia) [54].

### The shutdown
- 16 December 2014: Freebase announced it was closing and would offer its content to Wikidata [8].
- 31 March 2015: Freebase became read-only [8]. The closure of the website was planned for the third quarter of 2015;
  "Since August 2016, the main freebase-URL is redirected" to the Google developers page [8].
- The Google page now reads: the Freebase API has been shut down; the project "ran from 2007 to 2015"; the last dump
  is kept for citation in studies, "aren't maintained and no support can be provided" [9].
- The primary announcement is a Google+ post; its web-archive copy could not be fetched here, so the dates rest on
  the Wikidata project page [8] and the Google page [9].

### Used by
`fb15k`, `fb15k-237` (and the large FB1M) [45][43]; Google's Knowledge Graph used it among its roots (archive primer) [54].

### Known problems
"Freebase had known quality issues" (Tanon et al. 2016, as cited by the CoDEx authors) [32]; dumps are out of date and
unsupported [9]; in a paper summarised by Rossi et al., over 70% of person entities have no place of birth and over 99%
no ethnicity (secondary, not re-checked) [46].

### Usage evidence
Paper: Bollacker et al., SIGMOD 2008: **6,061** citations (Semantic Scholar, read 20261102 20:05) [53]. Archive:
`kb-kg/primer/README.md` (2008 row, 2012 Google row, shutdown) [54].

---

## conceptnet

**Role:** dataset (kinds: kg). Its paper evaluates the derived embeddings, not the graph; no benchmark page is proposed.

### What it contains
"a freely-available semantic network" of words and phrases linked by a closed set of relations. ConceptNet 5.5: over
21 million edges and over 8 million nodes; English vocabulary about 1,500,000 nodes; 83 languages with at least 10,000
nodes; Wiktionary supplies 18.1 million edges; 36 core relations such as IsA, UsedFor, CapableOf [28]. The site menu
lists roughly 78 languages [24].

### Size and versions
Versions on the downloads page: 5.5.0 (2016 path), 5.5.5 (2017), 5.6.0 (2018), "Current version: 5.7.0" (2019 path)
[29]. Size of 5.7: **unstated** on the pages read. Exact release dates: **unstated** (only years inferred from the
download paths) [29].

### Licence
Data: CC BY-SA 4.0 ("The complete data in ConceptNet is available under the Creative Commons Attribution-ShareAlike
4.0 license"); code: Apache 2.0; "The code and data in ConceptNet are different works" [25][26]. The sharing page adds:
"You may not use ConceptNet in a data set with an incompatible license" [25]. Parts: Wiktionary and Wikipedia via
DBpedia are CC BY-SA 3.0; WordNet must keep its Princeton notice; OMW, OMCS, JMDict and OpenCyc have no licence stated
on that page [25]. The GitHub licence API returns `NOASSERTION` for the repository (non-standard text) [27].

### How it was made
Originated in the crowdsourced Open Mind Common Sense project (1999, MIT Media Lab); now combines Wiktionary, Open
Multilingual WordNet, JMDict, OpenCyc, a subset of DBpedia and games with a purpose (Verbosity and Japanese and
English word games) [24][28]. Development is led by Luminoso Technologies [24].

### Used by
Common-sense and word-relatedness work; the 5.5 paper reports first-party results for its derived embeddings
("ConceptNet Numberbatch 16.09", a hybrid system): final MEN-3000 Spearman 0.866, Rare Words 0.601, SAT analogies
56.1% accuracy [28]. These evaluate derived vectors, not the graph, so no benchmark page is proposed for ConceptNet.

### Known problems
Share-alike licence limits combination with incompatible data [25]. Quality of the crowdsourced edges: **unstated**
in the sources read.

### Usage evidence
Paper: Speer, Chin, Havasi, "ConceptNet 5.5: An Open Multilingual Graph of General Knowledge", AAAI 2017 (arXiv
20161212). Citation count in "Citation counts" below. Archive pages: none.

---

## wordnet

**Role:** dataset (kinds: kg).

### What it contains
A lexical database whose entities are synsets (word senses) and whose relationships are lexical relations
(hypernym, part-of and so on) [45]. WordNet 3.0 statistics (from the Debian-packaged manual page of the 3.0
distribution, a mirror, not Princeton): nouns 82,115 synsets / 117,798 unique strings / 146,312 word-sense pairs; verbs
13,767 / 11,529 / 25,047; adjectives 18,156 / 21,479 / 30,002; adverbs 3,621 / 4,481 / 5,580. The sums I computed from
those rows: 117,659 synsets, 155,287 strings, 206,941 word-sense pairs [31]. (The fetch summary printed a different
synset total, 120,982; the by-part-of-speech rows add to 117,659, which is the figure to use.)

### Size and versions
WordNet 3.0 is the version in the licence text ("WordNet 3.0 Copyright 2006 by Princeton University") [30]. Whether a
later release exists and Princeton's own statistics page: **unstated**, because the Princeton site returned HTTP 403 to
the automated fetch (20261102 19:58).

### Licence
The WordNet licence text: permission "to use, copy, modify and distribute this software and database and its
documentation for any purpose and without fee or royalty", provided the copyright notice "WordNet 3.0 Copyright 2006
by Princeton University. All rights reserved." stays on copies; Princeton's name may not be used in advertising or
publicity; "AS IS" without warranty [30]. This was read from the SPDX copy of the text, since Princeton's licence page
could not be fetched.

### How it was made
Built by Princeton University as a dictionary and thesaurus for automatic text analysis [45]. Authors, method and
dates: **unstated** in the sources read (the standard references are Miller 1995 and Fellbaum 1998; neither was read).

### Used by
`wn18`, `wn18rr` (link-prediction subsets) [45][41]; the YAGO taxonomy backbone [23]; ConceptNet through Open
Multilingual WordNet [28].

### Known problems
For link prediction the WN18 subset is 94% test-leaking through inverse relations; see `wn18` and `wn18rr`.

### Usage evidence
Paper: Miller, "WordNet: a lexical database for English", CACM 1995. Count in "Citation counts" below. Archive pages:
none.

---

# Datasets and benchmarks: subsets cut from the graphs for link prediction

All eight items below are used for one task, **link prediction** (also called knowledge graph completion): given
(head, relation, ?) or (?, relation, tail), rank every entity and check where the true one lands. The standard
protocol and metrics, from the original TransE paper: replace the head or the tail of each test triple by every entity,
rank by score, report mean rank and Hits@10; in the "filtered" setting the other triples known to be true are removed
from the candidate list first (raw is the unfiltered setting) [45]. Later papers add MRR (mean reciprocal rank) and
Hits@1 and Hits@3 [41][46]. How ties are broken matters (see `fb15k-237`) [47].

A thread runs through the whole set, and the page should tell it in order: FB15k and WN18 (2013) had test leakage
through inverse relations (Toutanova and Chen's "% test linked" column reads 94.0% for WN18 and 80.9% for FB15k: the
share of test triples whose entity pair is directly linked in training; Dettmers et al. read these as inverse-relation
leakage) [43][41]; FB15k-237 (2015) and WN18RR (2017) removed the inverses [43][41]; YAGO3-10 (2017) was recommended as a third
leak-free set [41]; later audits found duplicate relations, skewed relations and Freebase mediator artifacts in the
"fixed" sets [49][32]; and an evaluation-protocol audit showed that the reported gains of ConvKB, CapsE and KBAT came from tie handling
and a data leak, not from the models [47]. CoDEx (2020), Wikidata5M (2019) and ogbl-wikikg2 (2020) came from Wikidata as larger or
cleaner alternatives [32][35][38].

A note on "who ran it" in the tables: **first-party** means the authors of the system in that row; the dataset's own
authors are named when they ran it. "Independent" means a team that built neither the dataset nor the system.

## fb15k

**Role:** both (kinds: kg). Deprecated; keep as history and as the example of leakage.

### Dataset
- **Contains:** 14,951 entities, 1,345 relations, 592,213 triples (483,142 train, 50,000 validation, 59,071 test) [45].
  Mostly movies, actors, awards and sports [41].
- **How made:** from Freebase. Entities also present in the Wikilinks database and with at least 100 mentions in
  Freebase (as entities and as relationships) were kept; relationships like `!/people/person/nationality`, which only
  reverse head and tail of another, were removed; the 592,213 triples were split at random [45]. A larger FB1M
  (1 million entities, about 25k relationships, 17.5 million training triples) was built in the same paper [45].
- **Licence:** unstated by the dataset's own page. Freebase dumps are CC BY [9]. The ConvE repository tells readers
  "do not use these datasets for your research" [42].
- **Used by:** the TransE paper (Bordes et al., NIPS 2013), then most embedding papers to 2018 [45][46].
- **Known problems:** test leakage: in 80.9% of FB15k test triples the entity pair is directly linked in training (the
  "% test linked" column of Toutanova and Chen) [43]; Dettmers et al. describe this as leakage through inverse
  relations [41]. Akrami et al. add reverse, duplicate and Cartesian-product
  relations: "the performance of all existing embedding models degenerates significantly after reverse triples are
  removed" [49]. A simple inverse model scores MRR .660 on FB15k, level with ConvE at .657 [41].

### Benchmark
- **What it tests / tasks / metrics:** link prediction; filtered and raw mean rank and Hits@10; later MRR, Hits@1,
  Hits@3 [45][41].
- **Datasets used:** FB15k only (this item).
- **Results (a sample; filtered unless marked):**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| TransE | 47.1 (raw 34.9) | Hits@10 % (mean rank 125; raw 243) | Bordes et al. | yes (also dataset authors) | 2013 | [45] |
| ConvE | .657 | MRR (Hits@10 .831) | Dettmers et al. | yes | 20170705 | [41] |
| Inverse model (rule: invert a known inverse relation) | .660 | MRR (Hits@10 .660) | Dettmers et al. | yes (baseline of the same paper) | 20170705 | [41] |
| ComplEx | .848 | MRR (H@1 81.56, H@10 90.53) | Rossi et al. | no, independent | 20200203 | [46] |
| TuckER | .788 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| TransE | .628 | MRR | Rossi et al. | no, independent | 20200203 | [46] |

Rossi et al. state that for models whose code used a tie-favouring ("min") policy they report the average policy, and
that hyperparameters were hand-tuned within a time budget [46].
- **Known problems of the benchmark:** the leakage above, so high scores here say little; tuned DistMult beats 27 of 29
  published models on Hits@10 over WN18 and FB15k (Kadlec et al., independent, 20170530) [48].
- **Used by:** see Dataset.
- **Usage evidence:** TransE paper citation count in "Citation counts".

## wn18

**Role:** both (kinds: kg). Deprecated; same story as FB15k.

### Dataset
- **Contains:** 40,943 entities (synsets), 18 relations, 151,442 triples (141,442 / 5,000 / 5,000) [45]. "Most of the
  151,442 triples consist of hyponym and hypernym relations" and the graph is strictly hierarchical [41].
- **How made:** a subset of WordNet used earlier by Bordes et al. (the "WN" data version of reference [2] in the TransE
  paper); the WordNet version number is **unstated** in the TransE paper [45]. Entities are written word + part of
  speech + sense number, such as `score_NN_1` [45].
- **Licence:** unstated by the dataset; derived from WordNet, whose own licence is in `wordnet`.
- **Known problems:** in 94.0% of test triples the entity pair is directly linked in training ("% test linked") [43],
  which Dettmers et al. describe as inverse-relation leakage [41]; a rule-based
  inverse model reaches MRR .963 on WN18, above ConvE's .943 [41].

### Benchmark
Link prediction, same protocol as `fb15k`.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| TransE | 89.2 (raw 75.4) | Hits@10 % (mean rank 251) | Bordes et al. | yes | 2013 | [45] |
| ConvE | .943 | MRR (Hits@10 .956) | Dettmers et al. | yes | 20170705 | [41] |
| Inverse model | .963 | MRR (Hits@10 .964) | Dettmers et al. | yes (baseline) | 20170705 | [41] |
| TuckER | .951 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| ComplEx | .949 | MRR | Rossi et al. | no, independent | 20200203 | [46] |

Scores near .95 are saturated and leak-driven [41][49]. Citation count: see "Citation counts".

## fb15k-237

**Role:** both (kinds: kg).

### Dataset
- **Contains:** 14,541 entities, 237 relations, 310,116 triples: 272,115 train, 17,535 validation, 20,466 test [43].
  The official release also pairs the triples with textual mentions: about 200 million ClueWeb12 sentences with FACC1
  Freebase annotations [44]; most papers use only the triples.
- **How made:** Toutanova and Chen kept the 401 most frequent relations of FB15k, detected near-duplicate and inverse
  relations (entity-pair sets that overlap by at least 97%, or whose reversed pairs overlap) and kept one relation of
  each set, leaving 237; they also removed validation and test triples whose entity pairs are directly linked in
  training [43].
- **Size and versions:** one version, 1.0, file `FB15K-237.2.zip`, 139.4 MB, on the Microsoft Download Center; the page
  gives two dates that conflict (header "Last published: October 30, 2015", details 7/15/2024) [44].
- **Licence:** **unstated** on the download page (only a generic terms-of-use link) [44]. The underlying Freebase
  dumps are CC BY [9].
- **Used by:** Toutanova and Chen 2015 (CVSC workshop at ACL) [43]; ConvE, RotatE, TuckER and nearly every embedding
  paper after 2017 [41][47]; CoDEx compares itself to it [32].
- **Known problems:**
  - Compound value types: fixed-set relations, such as a climate relation linking each place to the same 12 months,
    make about 12.7% of test queries trivial; 15.98% of test triples sit in relations skewed 50% or more toward one
    entity; a frequency baseline reaches MRR .236 against .356 for the best embedding model [32].
  - Symmetric relations such as "similar to" survived the filtering [41].
  - Tie-handling in evaluation: see the benchmark table [47].

### Benchmark
- **What it tests:** how well a model predicts a missing head or tail of a Freebase triple when inverse leakage has
  been removed; the other model ability tested is plain frequency statistics (see Known problems) [32].
- **Tasks, metrics, protocol:** link prediction, filtered MRR, Hits@1, Hits@3, Hits@10, mean rank; the candidate set is
  every entity (about 15,000) [41][45]. The audit by Sun et al. defines three tie rules: TOP (true triple placed first
  among ties), BOTTOM, and RANDOM, and argues RANDOM is the fair one [47].
- **Datasets used:** this item only.
- **Results (filtered MRR; independent audits first):**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| TuckER | .353 | MRR, RANDOM tie rule | Sun et al. | no, independent | 20191110 | [47] |
| RotatE | .336 | MRR, RANDOM | Sun et al. | no, independent | 20191110 | [47] |
| ConvE | .324 | MRR, RANDOM | Sun et al. | no, independent | 20191110 | [47] |
| ConvKB | .243 | MRR, RANDOM (reported by its authors as .396; TOP rule gives .407) | Sun et al. | no, independent | 20191110 | [47] |
| CapsE | .150 | MRR, RANDOM (reported as .523) | Sun et al. | no, independent | 20191110 | [47] |
| KBAT | .157 | MRR, RANDOM (reported as .518; original code leaked test data) | Sun et al. | no, independent | 20191110 | [47] |
| TuckER | .352 (H@1 25.90, H@10 53.61) | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| ComplEx | .349 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| RotatE | .336 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| AnyBURL (rules, no embeddings) | .324 | MRR (trained 1,000 s; the authors report slightly better at 10,000 s) | Rossi et al. | no, independent | 20200203 | [46] |
| TransE | .31 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| RESCAL | .356 | MRR (H@10 .541) | LibKGE team, common tuned setup | no (not the model or dataset authors), but the README is the toolkit authors' own | date unstated | [50] |
| ComplEx / DistMult / ConvE / RotatE / TransE | .348 / .343 / .339 / .333 / .313 | MRR | LibKGE team | as above | date unstated | [50] |
| ConvE | .325 (H@10 .501) | MRR | Dettmers et al. | yes | 20170705 | [41] |
| frequency baseline (no learning) | .236 | MRR | Safavi and Koutra | yes for CoDEx (a comparison to this set) | 20200916 | [32] |
| SimKGC (text-based, uses descriptions) | .336 | MRR | Wang et al. | yes | 20220304 | [51] |

*Reading:* the independent scores sit between .31 and .36 for plain embeddings; an advertised .5 on this set was an
artifact of tie handling [47]. A rule learner (AnyBURL) is within 0.03 MRR of the best embeddings [46].
- **Known problems:** the tie-rule inflation above; mediator-node triviality [32]; protocols that drop unseen
  entities from the test set raise numbers by a few points (the LibKGE README says about +3 points on WN18RR) [50].
- **Used by:** CoDEx [32], SimKGC [51], Sun et al. [47], Rossi et al. [46].
- **Usage evidence:** Toutanova and Chen 2015 and Dettmers 2018 counts: see "Citation counts" (ConvE paper: 3,294,
  read 20261102 19:51 [53]).

## wn18rr

**Role:** both (kinds: kg).

### Dataset
- **Contains:** 40,943 entities, 11 relations, 93,003 triples [41]: 86,835 train, 3,034 validation, 3,134 test [46].
- **How made:** Dettmers et al. applied to WN18 the same inverse-removal idea as for FB15k-237 and "thus create
  WN18RR to reclaim WN18 as a dataset" [41]; their own recommendation is "FB15k-237, WN18RR, and YAGO3-10" over FB15k
  and WN18 [41].
- **Licence:** unstated; derived from WordNet (see `wordnet`).
- **Known problems:** symmetric relations such as "similar to" were not removed, which explains why a rule-based
  inverse model still scores MRR .35 here [41]; 212 test entities do not appear in training, which makes about 6.7% of
  test facts impossible to predict (Rossi et al., reporting the dataset authors' own acknowledgement) [46]; the CapsE
  model starts from pre-trained GloVe vectors on WN18RR, which Sun et al. say makes the comparison unfair [47].

### Benchmark
- **What it tests:** link prediction on a hierarchy of word senses where inverse leakage has been removed.
- **Tasks, metrics and protocol:** as `fb15k-237`; MRR, Hits@1/3/10, mean rank [41].
- **Results (filtered MRR):**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| RotatE | .473 | MRR, RANDOM tie rule | Sun et al. | no, independent | 20191110 | [47] |
| TuckER | .461 | MRR, RANDOM | Sun et al. | no, independent | 20191110 | [47] |
| ConvE | .444 | MRR, RANDOM (its authors reported .43) | Sun et al. | no, independent | 20191110 | [47] |
| CapsE | .415 | MRR (GloVe-initialised) | Sun et al. | no, independent | 20191110 | [47] |
| KBAT | .412 | MRR (reported .440; original code leaked test data) | Sun et al. | no, independent | 20191110 | [47] |
| ConvKB | .249 | MRR (reported .248) | Sun et al. | no, independent | 20191110 | [47] |
| AnyBURL (rules) | .485 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| RotatE | .475 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| TuckER / ComplEx | .459 / .458 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| DistMult / ConvE / TransE | .433 / .427 / .206 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| RotatE / ComplEx / RESCAL | .478 / .475 / .467 | MRR | LibKGE team | toolkit authors' own table | date unstated | [50] |
| ConvE | .43 (H@10 .52) | MRR | Dettmers et al. | yes | 20170705 | [41] |
| SimKGC (text-based) | .666 | MRR | Wang et al. | yes; uses entity descriptions, so not the same kind of system | 20220304 | [51] |

- **Known problems of the benchmark:** unseen test entities; tie rules [47]; text-based systems use descriptions the
  embedding systems do not, and SimKGC reports them in a separate block for that reason [51].
- **Usage evidence:** the dataset is introduced in the ConvE paper (Dettmers et al., AAAI 2018, arXiv 20170705):
  **3,294** citations, read 20261102 19:51 [53].

## yago3-10

**Role:** both (kinds: kg).

### Dataset
- **Contains:** 123,182 entities, 37 relations, 1,079,040 training triples, 5,000 validation, 5,000 test; mostly
  descriptive attributes of people such as citizenship, gender and profession [41][46][49].
- **How made:** a subset of YAGO3 (Mahdisoltani et al.) keeping entities with at least 10 relations, then all facts of
  those entities, including their neighbours [41][46]. Unlike FB15k it keeps textual-attribute facts [46].
- **Licence:** unstated for the subset; YAGO 3 data is CC BY 3.0 [21].
- **Known problems:** two near-duplicate relations, `isAffiliatedTo` and `playsFor`, make up 35% and 30% of the training
  triples and over 63% of the test set; 557,696 training triples find a duplicate inside the training set; the
  relations `hasNeighbor`, `isConnectedTo` and `isMarriedTo` are symmetric, with 118 test triples whose reverse is in
  training; a simple rule-based model has filtered Hits@1 of 51.6%, above the embedding models (Akrami et al.) [49].
  Safavi and Koutra call it "too easy for link prediction" for the same reason [32]. Akrami et al. release a cleaned
  YAGO3-10-DR [49].

### Benchmark
- **What it tests / protocol:** link prediction as for `fb15k-237`; Safavi and Koutra credit Dettmers et al. (2018)
  with the subset [32], and the ConvE paper describes it and reports results next to Countries [41].
- **Results (filtered):**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| ComplEx | .576 (H@1 50.48, H@10 70.35) | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| TuckER | .544 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| AnyBURL (rules) | .528 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| ConvR | .527 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| TransE / DistMult | .501 / .501 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| RotatE | .498 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| ConvE | .488 | MRR | Rossi et al. | no, independent | 20200203 | [46] |
| ConvE | .44 (H@10 .62) | MRR | Dettmers et al. | yes | 20170705 | [41] |
| DistMult / ComplEx | .34 / .36 | MRR | Dettmers et al. | no (baselines run in the ConvE paper) | 20170705 | [41] |

*Reading:* the same model family scores .44 in the ConvE paper and .49 in Rossi et al.'s re-run; the two papers do
not use the same training budget, so the gap is not a ranking of the papers.
- **Usage evidence:** ConvE paper **3,294** (read 20261102 19:51) [53]; YAGO3 paper: see "Citation counts".

## wikidata5m

**Role:** both (kinds: kg, with an aligned text corpus).

### Dataset
- **Contains:** 4,594,485 entities, 822 relations, 20,624,575 triples, each entity paired with the first section of
  its English Wikipedia page as a description [35]. Transductive split: 20,614,279 train, 5,163 validation, 5,133 test,
  all over the same entities. Inductive split: 20,496,514 training triples over 4,579,609 entities; validation 6,699
  triples over 7,374 entities; test 6,894 triples over 7,475 entities, with entities and triples disjoint across the
  three parts [35][36].
- **How made:** from the July 2019 dumps of Wikidata and Wikipedia; entities with no Wikipedia page or with a
  description under 5 words were discarded; a fact is kept if both entities survive and the relation has a non-empty
  Wikidata page [35]. Inductive evaluation sets are random connected subgraphs [35].
- **Files:** KG 160 MB (transductive and inductive each), raw triples 168 MB, corpus 991 MB, aliases 188 MB [36].
- **Licence:** **unstated** on the dataset page [36]. The KEPLER code repository is MIT [37]. The parts come from
  Wikidata (CC0 for structured data [1]) and Wikipedia text (licence not read here).
- **Used by:** KEPLER (Wang et al., TACL 2021), SimKGC, text-based completion papers [35][51].
- **Known problems:** evaluation sets are small (5,133 transductive test triples) because ranking every one of 4.6
  million entities is expensive; the authors say they had to limit the test sets to thousands of triples to keep evaluation tractable [35]. Inductive metrics rank only 7,475
  entities against 4.6 million in the transductive case, so the two sets of numbers are not comparable [51]. Keeping
  only entities with Wikipedia pages biases the set toward well-known entities. *Reading:* that follows from the
  construction rule [35].

### Benchmark
- **What it tests:** link prediction at scale (transductive) and for unseen entities from their descriptions
  (inductive) [35].
- **Protocol and metrics:** rank all entities for each head or tail; MR, MRR, Hits@1/3/10; averaged over head and tail
  predictions [35]. The embedding baselines were run with the GraphVite multi-GPU toolkit because the originals do not
  scale [35].
- **Results (MRR %, transductive unless marked):**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| SimplE | 29.6 | MRR | Wang et al. (KEPLER) | yes (dataset authors) | 20191113 | [35] |
| RotatE | 29.0 | MRR | Wang et al. (KEPLER) | yes (dataset authors) | 20191113 | [35] |
| ComplEx | 28.1 | MRR | Wang et al. (KEPLER) | yes (dataset authors) | 20191113 | [35] |
| TransE / DistMult | 25.3 / 25.3 | MRR | Wang et al. (KEPLER) | yes (dataset authors) | 20191113 | [35] |
| KEPLER-Cond | 21.0 transductive; 40.2 inductive | MRR | Wang et al. | yes | 20191113 | [35] |
| SimKGC | 35.8 transductive; 71.4 inductive | MRR | Wang et al. (SimKGC) | yes for SimKGC; not by the dataset authors | 20220304 | [51] |
| BLP-SimplE / BLP-ComplEx | 49.3 / 48.9 inductive | MRR | Daza et al. (as quoted by SimKGC) | not the dataset authors; quoted second-hand | 20220304 (quote date) | [51] |

I found no independent re-run of Wikidata5M on the pages read. The OGB leaderboard is the more active large-Wikidata
benchmark (`ogbl-wikikg2`).
- **Usage evidence:** KEPLER paper **900** citations, read 20261102 19:51 [53].

## ogbl-wikikg2

**Role:** both (kinds: kg). Part of the Open Graph Benchmark (OGB).

### Dataset
- **Contains:** 2,500,604 entities, 535 relation types, 17,137,181 edges; split 94/3/3 by time [38].
- **How made:** all relational statements of Wikidata were retrieved and rare entities filtered out. Wikidata was
  downloaded at three snapshots, May, August and November 2015 (archived dumps); only entities and relation types in
  the May graph were kept; May triples are training, new triples in August are validation, new triples in November are
  test [38][39]. This replaces a random split used by earlier Wikidata sets (they cite Wikidata5M's) [38].
- **Version:** `ogbl-wikikg2` needs `ogb>=1.2.4`; the earlier `ogbl-wikikg` is deprecated for a bug in the negative
  samples of validation and test [39].
- **Licence:** CC-0, stated at the end of the dataset's section on the OGB site [39].
- **Used by:** the OGB leaderboard: 28 entries, 8 of them OGB-team baselines [40].
- **Known problems:** the snapshot is from 2015, so it is not today's Wikidata (see `wikidata`); the metric ranks the
  true entity against 500 sampled negatives per query (1,000 for head plus tail), "much less" than the roughly 15,000
  used for FB15k-237 [38], so the MRR cannot be compared with FB15k-237 numbers. Embedding sizes up to 2.2 billion
  parameters appear on the leaderboard [40].

### Benchmark
- **What it tests:** time-split knowledge graph completion at 2.5 million entities.
- **Protocol:** replace the head or tail of each test triple by 500 random negatives (not appearing in the KG), compute
  MRR of the true entity against those negatives [38][39]. Training MRR is unfiltered; validation and test are filtered [38].
- **Results (leaderboard, test MRR; every row is submitted by the team named, not re-run here; the OGB team ran the
  baselines):**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| RelEns | .7392 ± .0011 | test MRR (2.18B parameters) | Quanming Yao (Tsinghua EE) | yes, submitter's own | 20231015 | [40] |
| StarGraph + TripleRE + Text (uses external data) | .7305 ± .0010 | test MRR | Liang Yao (Tencent) | yes | 20230104 | [40] |
| InterHT+ | .7293 ± .0018 | test MRR (156M parameters) | Baoxin Wang (HFL) | yes | 20221223 | [40] |
| StarGraph + TripleRE | .7286 ± .0009 | test MRR (93M) | Linhui Feng (360AI) | yes | 20230103 | [40] |
| A*Net | .6711 ± .0045 | test MRR (6.8M parameters) | Zhaocheng Zhu (Mila) | yes | 20230521 | [40] |
| NodePiece + AutoSF | .5703 ± .0035 | test MRR (6.9M) | Mikhail Galkin (Mila) | yes | 20210717 | [40] |
| RotatE (250 dim) | .4332 ± .0025 | test MRR | OGB team (baselines) | the benchmark authors | 20210123 | [40] |
| TransE (500 dim) | .4256 ± .0030 | test MRR | OGB team | the benchmark authors | 20210123 | [40] |
| ComplEx (250 dim) | .4027 ± .0027 | test MRR | OGB team | the benchmark authors | 20210123 | [40] |
| DistMult (500 dim) | .3729 ± .0045 | test MRR | OGB team | the benchmark authors | 20210123 | [40] |
| TransE (100 dim) | .2622 ± .0045 | test MRR | OGB team | the benchmark authors | 20210123 | [40] |

The page lists 28 entries. Of the 28 entries only the second uses external data [40]. *Reading:* the top entries
differ from the OGB baselines by 0.3 MRR, much of it with hundreds of millions to billions of parameters; the page's
parameter column lets a reader weigh that [40]. No independent re-run is stated.
- **Usage evidence:** OGB paper (Hu et al., arXiv 20200502): citation count in "Citation counts".

## codex

**Role:** both (kinds: kg; with entity types, multilingual text and verified negatives).

### Dataset
- **Contains:** three knowledge graphs from Wikidata with Wikipedia extracts:

| | Entities | Relations | Train | Valid (+) | Test (+) | Valid (-) | Test (-) |
|---|---|---|---|---|---|---|---|
| CoDEx-S | 2,034 | 42 | 32,888 | 1,827 | 1,828 | 1,827 | 1,828 |
| CoDEx-M | 17,050 | 51 | 185,584 | 10,310 | 10,311 | 10,310 | 10,311 |
| CoDEx-L | 77,951 | 69 | 551,193 | 30,622 | 30,622 | none | none |
| raw dump | 380,038 | 75 | 1,156,222 triples | | | | |

  Also entity types from Wikidata `instance of` and `subclass of`; labels, descriptions and Wikipedia introduction
  extracts in Arabic, German, English, Spanish, Russian and Chinese (coverage 61% to 97% by language and set) [32][33].
- **How made:** snowball sampling from seed entity and relation types of 13 domains, retrieving 380,038 entities,
  75 relations and 1,156,222 triples from Wikidata; k-core filtering (k = 15, 10 and 5 for S, M, L); inverse
  relations removed (relations whose entity-pair sets overlap another's by more than 50%); 90/5/5 split; hard negatives:
  triples that a trained model ranked in its top 10 with the right entity type, then labelled by hand for S and M
  (not L) [32]. Quality check: on 100 random candidate negatives, the authors' labels agreed with two independent
  native speakers 89.5% of the time; in 81% of disagreements the authors had labelled true where the annotator said
  false [32].
- **Licence:** the repository is MIT [33][34]. The data licence is **unstated** in the README; the triples come from
  Wikidata (CC0 structured data [1]); the Wikipedia extracts' licence was not read.
- **Used by:** the EMNLP 2020 paper (Safavi and Koutra); LibKGE pretrained models [33].
- **Known problems:** CoDEx-L has no verified negatives [32]; hard negatives were built from the top-10 of the five
  models in the paper, so a different model family may see them differently (*Reading:* inferred from the generation
  procedure [32]). The date of the Wikidata snapshot used is **unstated** in the pages read.

### Benchmark
- **What it tests:** link prediction (all three sets) and triple classification (S and M, with the hard negatives);
  also a comparison with FB15k-237 [32].
- **Protocol and metrics:** link prediction with MRR and Hits@1/3/10; triple classification with accuracy and F1 [33].
- **Results (README of the dataset authors; tuned with LibKGE, link prediction MRR):**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| ComplEx on CoDEx-S | .465 | MRR | Safavi and Koutra | yes (dataset authors) | 20200916 | [33] |
| ConvE / TuckER on CoDEx-S | .444 / .444 | MRR | Safavi and Koutra | yes | 20200916 | [33] |
| TransE on CoDEx-S | .354 | MRR | Safavi and Koutra | yes | 20200916 | [33] |
| ComplEx on CoDEx-M | .337 | MRR | Safavi and Koutra | yes | 20200916 | [33] |
| TuckER / RESCAL on CoDEx-M | .328 / .317 | MRR | Safavi and Koutra | yes | 20200916 | [33] |
| frequency baseline on CoDEx-M | .135 | MRR | Safavi and Koutra | yes | 20200916 | [32] |
| TuckER on CoDEx-L | .309 | MRR | Safavi and Koutra | yes | 20200916 | [33] |
| TransE on CoDEx-L | .187 | MRR | Safavi and Koutra | yes | 20200916 | [33] |
| ConvE on CoDEx-M, triple classification | accuracy .826 (F1 .829) | accuracy | Safavi and Koutra | yes | 20200916 | [33] |

Only first-party results were found in the sources read; I did not look for later papers that use CoDEx.
*Reading:* the benchmark's own argument is the contrast with FB15k-237: the best embedding beats a frequency baseline
by +.202 MRR on CoDEx-M against +.120 on FB15k-237 [32].
- **Known problems of the benchmark:** CoDEx-L evaluates link prediction only; triple classification needs hard
  negatives which exist for S and M only [32].
- **Usage evidence:** CoDEx paper (EMNLP 2020, arXiv 20200916): citation count in "Citation counts".

---

# Citation counts

Semantic Scholar `citationCount`, read through the Graph API at the time shown (HTTP 429 met and retried; OpenAlex had no
budget left). A count is a signal, not a verdict, and it moves daily. `n/r` = not retrieved before this file was closed.

| Paper | Count | Read (UTC) | Items |
|---|---|---|---|
| Vrandecic and Krotzsch, Wikidata: a free collaborative knowledgebase (CACM 2014) | 2849 | 20261102 20:01 | wikidata |
| Auer et al., DBpedia: A Nucleus for a Web of Open Data (ISWC 2007) | 5925 | 20261102 20:01 | dbpedia |
| Lehmann et al., DBpedia - A large-scale, multilingual knowledge base extracted from Wikipedia (SWJ 2015) | 3738 | 20261102 20:01 | dbpedia |
| Suchanek et al., YAGO: a core of semantic knowledge (WWW 2007) | n/r |  | yago |
| Mahdisoltani et al., YAGO3 (CIDR 2015) | n/r |  | yago, yago3-10 |
| Bollacker et al., Freebase (SIGMOD 2008) | 6061 | 20261102 20:05 | freebase |
| Pellissier Tanon et al., From Freebase to Wikidata: the Great Migration (WWW 2016) | 245 | 20261102 20:24 | freebase, wikidata |
| Speer, Chin, Havasi, ConceptNet 5.5 (AAAI 2017) | n/r |  | conceptnet |
| Miller, WordNet: a lexical database for English (CACM 1995; S2 shows another venue string) | 18069 | 20261102 20:17 | wordnet |
| Bordes et al., Translating Embeddings (NIPS 2013) | n/r |  | fb15k, wn18 |
| Toutanova and Chen, Observed versus latent features (CVSC 2015) | 1252 | 20261102 20:17 | fb15k-237 |
| Dettmers et al., Convolutional 2D Knowledge Graph Embeddings (AAAI 2018; arXiv 2017) | 3294 | 20261102 19:51 | wn18rr, yago3-10 |
| Wang et al., KEPLER (TACL 2021; arXiv 2019) | 900 | 20261102 19:51 | wikidata5m |
| Hu et al., Open Graph Benchmark (NeurIPS 2020; arXiv 2020) | n/r |  | ogbl-wikikg2 |
| Safavi and Koutra, CoDEx (EMNLP 2020) | n/r |  | codex |
| Rossi et al., KG embedding for link prediction: a comparative analysis (TKDD 2021) | n/r |  | audit |
| Sun et al., A re-evaluation of KGC methods (ACL 2020) | n/r |  | audit |
| Akrami et al., Realistic re-evaluation of KGC methods (SIGMOD 2020) | 137 | 20261102 20:24 | audit |
| Kadlec et al., Knowledge base completion: baselines strike back (2017) | n/r |  | audit |
| Wang et al., SimKGC (ACL 2022) | n/r |  | wikidata5m, wn18rr, fb15k-237 |


---

# Unstated, unverified and flagged

- **Citation counts not retrieved (n/r)**: Semantic Scholar answered HTTP 429 for nearly every request from 20261102 20:05 to 20:40 despite retries with waits, OpenAlex had no budget left, and no API key was created. Counts marked n/r in the table must be fetched again later.

- **Statement count of Wikidata**: unstated on the pages read.
- **Wikidata launch date** (29 October 2012) rests on Wikipedia, a tertiary source [7]; no primary announcement was read.
- **Freebase closure announcement**: the primary Google+ post exists only in a web archive that this environment could
  not fetch; the dates rest on Wikidata's project page [8] and Google's Freebase page [9].
- **WordNet**: Princeton's licence and statistics pages returned HTTP 403 to automated fetches (20261102 19:58); the
  licence text was read from SPDX [30] and the statistics from a Debian-packaged man page of the 3.0 distribution [31].
  Whether a release after 3.0 exists is unstated. Miller 1995 and Fellbaum 1998 were not read.
- **Licences unstated** by the dataset's own page: FB15k, WN18, FB15k-237 [44], WN18RR, YAGO3-10, Wikidata5M [36],
  CoDEx data [33], and per-artifact DBpedia licences [14]. For each, the licence of the source (Freebase CC BY [9],
  WordNet [30], YAGO 3 CC BY 3.0 [21], Wikidata CC0 [1]) is given only as context, not as the dataset's licence.
- **Dates of leaderboard-style results** in the LibKGE README [50] are unstated.
- **Scores are copied, not re-run.** Every score in the results tables was read from the cited paper, README or
  leaderboard on 20261102; none was re-computed, and the OGB leaderboard rows are self-submitted.
- **Not covered**: question sets derived from Wikidata or DBpedia, Text2KGBench, NELL-995, UMLS, Kinship, Countries,
  Open English WordNet (a community fork; its licence file could not be classified by the GitHub API).
- **Pinakes repository and `kb-kg/literature/graph-rag-research.md`**: searched for these items; no mention found in
  `kb-kg/literature` or `pinakes`.
- **Papers with Code** (the former leaderboard host for these sets) was not used; every table comes from papers,
  repositories and OGB.

# Sources

Read times are the nearest clock reading in the same step (plus or minus about 3 minutes). `date -u "+%Y%m%d %H:%M"`.

1. https://www.wikidata.org/wiki/Wikidata:Licensing?action=raw : licence of structured data and other namespaces (read 20261102 19:47)
2. https://www.wikidata.org/w/api.php?action=query&meta=siteinfo&siprop=statistics&format=json : live statistics (read 20261102 19:47)
3. https://www.wikidata.org/wiki/Wikidata:Statistics : item and edit counts (read 20261102 19:47)
4. https://dumps.wikimedia.org/wikidatawiki/entities/ : file listing with byte sizes (read 20261102 19:47)
5. https://www.wikidata.org/wiki/Wikidata:Database_download : dump formats and frequency (read 20261102 19:47)
6. https://www.wikidata.org/wiki/Wikidata:Introduction : data model, editors and bots (read 20261102 19:47)
7. https://en.wikipedia.org/wiki/Wikidata : launch date 29 October 2012, developer, phases (tertiary; first 100,000 characters read 20261102 20:03)
8. https://www.wikidata.org/wiki/Wikidata:WikiProject_Freebase : Freebase closing announced 16 December 2014, read-only 31 March 2015 (read 20261102 19:57)
9. https://developers.google.com/freebase : API shut down, last dump, sizes, licences (read 20261102 19:57)
10. https://research.google/pubs/freebase-a-collaboratively-created-graph-database-for-structuring-human-knowledge/ : Freebase paper abstract (read 20261102 19:57)
11. https://research.google/pubs/from-freebase-to-wikidata-the-great-migration/ : abstract of the migration paper, no counts (read 20261102 19:58)
12. https://www.dbpedia.org/about/ : what DBpedia is, start 2007, licence CC BY-SA 3.0 and GFDL (read 20261102 19:48; the licence sentence re-read raw 20261102 20:19)
13. https://www.dbpedia.org/resources/ : Databus, release cadence, ontology 768 classes, 3000 properties, about 4,233,000 instances (read 20261102 19:48; re-read raw 20:19)
14. https://www.dbpedia.org/resources/knowledge-graphs/ : Largest Diamond, Marvin bot, Fusion KG licence (read 20261102 19:48; re-read raw 20:19)
15. https://www.dbpedia.org/blog/snapshot-2025-06-release/ : returned the DBpedia home-page text: more than 228 million entities, around 20 language chapters (read 20261102 19:48; home page re-read raw 20:19)
16. https://www.semantic-web-journal.net/system/files/swj499.pdf : Lehmann et al., DBpedia SWJ paper preprint; 1.8 billion facts, extraction and quality statements (read in full text 20261102 20:04)
17. https://yago-knowledge.org/ : YAGO 4.6 out, newer version in preparation (read 20261102 19:48)
18. https://yago-knowledge.org/downloads/yago-4-5 : 49 million entities, 109 million facts, licence (read 20261102 19:48; re-read raw 20:18)
19. https://yago-knowledge.org/downloads/yago-4-6 : 39 million entities, 167 million facts, licence, what is new (read 20261102 20:01; re-read raw 20:18)
20. https://yago-knowledge.org/getting-started : how YAGO is built, version list (read 20261102 20:01)
21. https://yago-knowledge.org/downloads/yago-3 : 17 million entities, 150 million facts, CC BY 3.0, sources (read 20261102 20:00; re-read raw 20:18)
22. https://yago-knowledge.org/downloads/yago-4 : 50 million entities, 2 billion facts, CC BY-SA (read 20261102 20:05; re-read raw 20:18)
23. https://yago-knowledge.org/downloads/yago-1 : 2 million entities, 20 million facts, 95% accuracy, GFDL (read 20261102 20:05; re-read raw 20:18)
24. https://conceptnet.io/ : what ConceptNet is, sources, licence statement (read 20261102 19:57)
25. https://github.com/commonsense/conceptnet5/wiki/Copying-and-sharing-ConceptNet : licence of data and components (read 20261102 19:57)
26. https://raw.githubusercontent.com/commonsense/conceptnet5/master/LICENSE.txt : data CC BY-SA 4.0, code Apache 2.0 (read 20261102 19:58)
27. https://api.github.com/repos/commonsense/conceptnet5/license : returns NOASSERTION (read 20261102 19:58)
28. https://arxiv.org/pdf/1612.03975 : ConceptNet 5.5 paper (AAAI 2017), full text; sizes, sources, results (read 20261102 19:55)
29. https://github.com/commonsense/conceptnet5/wiki/Downloads : versions 5.5.0 to 5.7.0 (read 20261102 20:05)
30. https://spdx.org/licenses/WordNet.html : WordNet licence text (read 20261102 19:59); https://wordnet.princeton.edu/license-and-commercial-use returned HTTP 403 (20261102 19:58)
31. https://manpages.debian.org/jessie/wordnet/wnstats.7wn.en.html : WordNet 3.0 statistics by part of speech, a mirror of the distribution's manual (read 20261102 20:00)
32. https://arxiv.org/pdf/2009.07810 : CoDEx paper (EMNLP 2020), full text (read 20261102 19:55)
33. https://raw.githubusercontent.com/tsafavi/codex/master/README.md : CoDEx statistics, results, MIT licence statement (read 20261102 19:53)
34. https://api.github.com/repos/tsafavi/codex/license : MIT (read 20261102 19:53)
35. https://arxiv.org/pdf/1911.06136 : KEPLER paper (TACL), Wikidata5M construction, statistics, results (full text read 20261102 19:55)
36. https://deepgraphlearning.github.io/project/wikidata5m : Wikidata5M splits, files, no licence statement (read 20261102 19:52)
37. https://raw.githubusercontent.com/THU-KEG/KEPLER/master/README.md and https://api.github.com/repos/THU-KEG/KEPLER/license : code repository MIT, data pointers (read 20261102 20:03)
38. https://arxiv.org/pdf/2005.00687 : Open Graph Benchmark paper, section on ogbl-wikikg2 and Table 13 (full text read 20261102 19:55)
39. https://ogb.stanford.edu/docs/linkprop/ : ogbl-wikikg2 description, version note, "License: CC-0" (read 20261102 20:01)
40. https://ogb.stanford.edu/docs/leader_linkprop/ : ogbl-wikikg2 leaderboard, 28 rows parsed (read 20261102 20:02)
41. https://arxiv.org/pdf/1707.01476 : ConvE paper (extended AAAI 2018): WN18RR, YAGO3-10, inverse model, Tables 3 to 5 (full text read 20261102 19:55)
42. https://raw.githubusercontent.com/TimDettmers/ConvE/master/README.md : "do not use" note on FB15k and WN18 (read 20261102 20:00)
43. https://aclanthology.org/W15-4007.pdf : Toutanova and Chen 2015, FB15k-237 construction and dataset table (full text read 20261102 19:59)
44. https://www.microsoft.com/en-us/download/details.aspx?id=52312 : FB15K-237 download page (read 20261102 20:00)
45. https://papers.nips.cc/paper_files/paper/2013/file/1cecc7a77928ca8133fa24680a88d2f9-Paper.pdf : TransE paper (NIPS 2013): FB15k, WN, protocol, Table 3 (full text read 20261102 20:00)
46. https://arxiv.org/pdf/2002.00819 : Rossi et al., comparative analysis of embedding link-prediction models (TKDD 2021): dataset Table 2, results Table 3 (read 20261102 19:55)
47. https://arxiv.org/pdf/1911.03903 : Sun et al., a re-evaluation of KGC methods (ACL 2020): Tables 2 and 3 (read 20261102 19:55)
48. https://arxiv.org/pdf/1705.10744 : Kadlec et al., baselines strike back (abstract and introduction read 20261102 19:55)
49. https://arxiv.org/pdf/2003.08001 : Akrami et al., realistic re-evaluation (SIGMOD 2020): reverse, duplicate, Cartesian-product relations, YAGO3-10 (read 20261102 19:55)
50. https://raw.githubusercontent.com/uma-pi1/kge/master/README.md : LibKGE results for FB15K-237 and WN18RR, unseen-entity note (read 20261102 20:02)
51. https://arxiv.org/pdf/2203.02167 : SimKGC (ACL 2022): Wikidata5M, WN18RR, FB15k-237 results (read 20261102 20:03)
52. https://export.arxiv.org/api/query?id_list=2203.02167,1911.03903,1705.10744,2003.08001,2002.00819,1707.01476,1911.06136,2005.00687,2009.07810,1612.03975 : first-version dates and authors (read 20261102 20:04)
53. https://api.semanticscholar.org/graph/v1/paper/... : citation counts, each with its own read time in the table "Citation counts" (OpenAlex returned "Rate limit exceeded" at 20261102 20:08 and was not used; HTTP 429 from Semantic Scholar was met repeatedly and retried with waits)
54. Archive pages, repository paths: kb-kg/primer/README.md (DBpedia, Freebase, Google Knowledge Graph, Wikidata rows and sources 12, 16, 17) and kb-kg/papers-benchmarks/README.md (Text2KGBench row) : searched by grep on 20261102 19:50 for all item names; no other page matches
