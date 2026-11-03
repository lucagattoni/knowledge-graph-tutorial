---
type: chapter
updated: 20261102 21:58 UTC
---

# Datasets

A dataset page holds the data: what is in it, how big it is, who may use it, how it was made and what is known to be wrong with it. It holds no scores. A benchmark page holds the evaluation (tasks, metrics, protocol, results): see [the benchmarks chapter](../benchmarks/README.md). An item that is both has one page of each, with the same name. This chapter lists the 26 datasets by kind and shows the licence each page found; the pages hold the detail.

## How they were chosen

A dataset has a page when it passes at least one of three tests (decision D-3):

- a fundamental paper of [the papers chapter](../papers/README.md) uses it;
- a trend of [the trends chapter](../trends/README.md) uses it;
- it is widely used, judged by the citation count of its paper, given on the dataset page with its source and read time. The catalogue sets no numeric threshold, and counts are never compared across sources.

The kinds are [knowledge graphs](../index/knowledge-graph.md) as data, question sets and text corpora (decision D-1). Ontologies and schemas are not datasets here. The list for the first edition was fixed on 20261102 under the owner's delegation; a later change is a dated row in the changes below.

The split between this chapter and the benchmarks chapter follows decision D-2:

- **Both pages.** The data is used beyond its own protocol and the item also defines an evaluation. HotpotQA is the example: its data appears in [BEIR](../benchmarks/beir.md) and [KILT](../benchmarks/kilt.md) as well as in its own protocol. The two pages share a slug.
- **Benchmark page only.** The data is used only inside the benchmark's own protocol, or the benchmark combines datasets that have pages of their own (BEIR and RAGSearch do). The benchmark page says which in its Datasets section. Twelve benchmark pages are of this kind; none is repeated here.
- **Dataset page only.** Knowledge graphs used as source data, and question sets whose scores sit on other benchmark pages. Such a page gives no system results.

## Knowledge graphs

Graphs of entities and facts, used as source data or cut into link-prediction sets. MetaQA, which also ships a movie knowledge graph, is listed under question sets.

| Dataset | What it is | Licence | Benchmark page |
|---|---|---|---|
| [Wikidata](wikidata.md) | Open, community-edited graph of items and statements, with qualifiers and references. | CC0 (structured data); text elsewhere CC BY-SA 4.0 | none |
| [Freebase](freebase.md) | Community-edited graph that Google shut down in 2015; its subsets still back benchmarks. | CC-BY for the last dump, with terms of service; subsets unstated | none |
| [DBpedia](dbpedia.md) | Facts extracted from Wikipedia and published as [linked data](../index/linked-data.md) since 2007; several collections, not one graph. | CC BY-SA 3.0 and GFDL; per-version labels differ | none |
| [YAGO](yago.md) | Wikipedia facts under a taxonomy (2007); since version 4 a cleaned subset of Wikidata. | Differs by version, from GNU FDL to CC BY 4.0 | none |
| [WordNet](wordnet.md) | Lexical database of English: word senses grouped into synsets and linked by relations. | WordNet 3.0 licence: free use if the notice is kept | none |
| [ConceptNet](conceptnet.md) | Open graph of the common-sense meaning of words; downloads page names 5.7.0 (2019) as current. | CC BY-SA 4.0 (data), Apache-2.0 (code) | none |
| [FB15k-237](fb15k-237.md) | About 310 thousand Freebase triples, cut from FB15k in 2015 to remove test leakage; used for [link prediction](../index/link-prediction.md). | Unstated | [Knowledge graph link prediction](../benchmarks/kg-link-prediction.md) |
| [WN18RR](wn18rr.md) | About 93 thousand WordNet triples, cut from WN18 in 2017 to reduce inverse-relation leakage. | Unstated | [Knowledge graph link prediction](../benchmarks/kg-link-prediction.md) |

Wikidata, Freebase, DBpedia, YAGO and WordNet have no benchmark of their own. Benchmark pages that use them include [OGB link prediction](../benchmarks/ogb-link-prediction.md), [Text2KGBench](../benchmarks/text2kgbench.md), [BEIR](../benchmarks/beir.md), [KILT](../benchmarks/kilt.md), [WebQuestionsSP](../benchmarks/webquestionssp.md) and the link-prediction page above.

## Question sets

Questions with answers, grouped by what they are answered from: text (multi-hop, then open-domain), knowledge graphs, chat histories, long documents. Many also carry the text the answers come from; see Corpora.

| Dataset | What it is | Licence | Benchmark page |
|---|---|---|---|
| [HotpotQA](hotpotqa.md) | About 113 thousand crowd-written English [multi-hop](../index/multi-hop-question-answering.md) questions over Wikipedia, with supporting sentences. | CC BY-SA 4.0 (data), Apache-2.0 (code) | [HotpotQA](../benchmarks/hotpotqa.md) |
| [2WikiMultiHopQA](2wikimultihopqa.md) | 192,606 multi-hop questions over Wikipedia summaries, with Wikidata evidence triples. | Data unstated (code: Apache-2.0) | [2WikiMultiHopQA](../benchmarks/2wikimultihopqa.md) |
| [MuSiQue](musique.md) | 2- to 4-hop questions, each with 20 paragraphs, made by composing single-hop questions. | CC BY 4.0 | [MuSiQue](../benchmarks/musique.md) |
| [MultiHop-RAG](multihop-rag.md) | 2,556 multi-hop questions over 609 English news articles. | ODC-By (README and card); no LICENSE file | [MultiHop-RAG](../benchmarks/multihop-rag.md) |
| [Natural Questions](natural-questions.md) | Real anonymised Google queries paired with Wikipedia pages and long and short answer annotations. | CC BY-SA 3.0 per secondary sources only | [Natural Questions](../benchmarks/natural-questions.md) |
| [TriviaQA](triviaqa.md) | 95,956 trivia question-answer pairs with Wikipedia and web evidence documents. | Disputed: Apache-2.0 on GitHub; the project page says the university holds no copyright in the data | none |
| [PopQA](popqa.md) | About 14,000 questions on entities of varying popularity, one per Wikidata triple. | Data unstated (code: MIT) | none |
| [MS MARCO](ms-marco.md) | About one million anonymised Bing queries with web passages and editor-written answers. | Non-commercial research only | [MS MARCO](../benchmarks/ms-marco.md) |
| [WebQuestionsSP](webquestionssp.md) | About 4,700 Google Suggest questions, each labelled with a [SPARQL](../index/sparql.md) query over Freebase. | Unstated | [WebQuestionsSP](../benchmarks/webquestionssp.md) |
| [ComplexWebQuestions](complexwebquestions.md) | 34,689 complex questions built from WebQuestionsSP, with SPARQL over Freebase and web snippets. | Unstated | none |
| [SimpleQuestions](simplequestions.md) | 108,442 single-fact questions over Freebase, released by Facebook AI Research in 2015. | Unstated | none |
| [GrailQA](grailqa.md) | 64,331 crowd-worded questions over Freebase with logical forms; a test question is i.i.d., compositional or zero-shot. | CC BY-SA 4.0 (code: Apache-2.0) | none |
| [LC-QuAD](lc-quad.md) | Two sets of questions with SPARQL queries: 1.0 (5,000, over DBpedia) and 2.0 (about 30,000, over Wikidata and DBpedia). | CC BY 4.0 per the authors; 1.0 also states GPL-3.0 | [LC-QuAD](../benchmarks/lc-quad.md) |
| [MetaQA](metaqa.md) | About 407,500 template-generated movie questions of 1, 2 and 3 hops over a movie knowledge graph. | A Creative Commons licence; the LICENSE file holds CC BY 3.0 | none |
| [LongMemEval](longmemeval.md) | 500 questions about facts buried in long timestamped user-assistant chat histories. | MIT | [LongMemEval](../benchmarks/longmemeval.md) |
| [LoCoMo](locomo.md) | Very long two-speaker conversations with annotated questions in five categories. | CC BY-NC 4.0 (non-commercial) | [LoCoMo](../benchmarks/locomo.md) |
| [UltraDomain](ultradomain.md) | Very long textbook, financial and legal contexts with GPT-4-written high-level questions (MemoRAG, 2024). | Apache-2.0 on the card; source texts unstated | none |

TriviaQA and PopQA have no benchmark page; their scores are on [KILT](../benchmarks/kilt.md) and [RAGSearch](../benchmarks/ragsearch.md) (TriviaQA) and on RAGSearch (PopQA). The pages of ComplexWebQuestions, SimpleQuestions, GrailQA, MetaQA and UltraDomain give no results.

## Corpora

Text collections that systems retrieve from. One page is a corpus first:

| Dataset | What it is | Licence | Benchmark page |
|---|---|---|---|
| [Wikipedia snapshots of DPR and KILT](wikipedia-dpr-kilt.md) | Two processed copies of English Wikipedia: DPR (December 2018 dump, 21,015,324 passages of 100 words) and KILT (August 2019 dump, 5,903,530 pages). | Wikipedia text GFDL and CC BY-SA 4.0; DPR repository CC BY-NC 4.0; KILT repository MIT | [KILT](../benchmarks/kilt.md) |

Ten question sets above also ship a text corpus: [HotpotQA](hotpotqa.md), [MuSiQue](musique.md), [2WikiMultiHopQA](2wikimultihopqa.md), [MultiHop-RAG](multihop-rag.md), [Natural Questions](natural-questions.md), [TriviaQA](triviaqa.md), [MS MARCO](ms-marco.md), [LongMemEval](longmemeval.md), [LoCoMo](locomo.md) and [UltraDomain](ultradomain.md).

## Considered and not given a page

These were weighed against the tests above. "No paper or trend page uses it" means that a search of the papers, trends, history and experiments folders of `docs/` on 20261102 at 21:46 UTC found no page that uses it as data. "No other use found" means none was found when the list was built on 20261102; that search was not repeated.

- **FB15k and WN18.** The predecessors of FB15k-237 and WN18RR, set aside because of test leakage; the ConvE paper recommends against using them [1]. Each is described on the page of its successor.
- **YAGO3-10.** A link-prediction subset of YAGO 3: the entities with at least 10 relations, 123,182 entities and 37 relations [1]. It is a protocol subset, so it is described on [the link-prediction benchmark page](../benchmarks/kg-link-prediction.md) and the [YAGO](yago.md) page.
- **Wikidata5M.** 4,594,485 entities and 20,624,575 triples (the sum of the three transductive splits) from the July 2019 dump of Wikidata and Wikipedia, with Wikipedia descriptions [2][3]. The dataset page states no licence [2]. No paper or trend page uses it. [The Wikidata page](wikidata.md) lists it among the sets derived from Wikidata.
- **CoDEx.** Three Wikidata graphs (S, M, L) with manually verified hard negatives, EMNLP 2020 [4]. The repository is MIT and states no data licence [5]. No paper or trend page uses it; the [Freebase](freebase.md) and [FB15k-237](fb15k-237.md) pages cite its authors' criticism of those graphs.
- **LoCoMo-Plus.** Adds cue-trigger instances to the LoCoMo conversations (first version 20260211) [6]. The released data file holds 401 instances; the paper's abstract gives no count [7]. No other use found; the repository has no LICENSE file [7]. See [LoCoMo](locomo.md).
- **AMA-Bench.** Real and synthetic agent trajectories with expert-written or rule-based questions (version 4, 20260527) [8]. No other use found; MIT [9]. No other page of this documentation mentions it.
- **EvoMemBench.** Selects or reconstructs six datasets from other benchmarks, MemoryAgentBench among them (version 3, 20261030) [10]. No LICENSE file [11]. Its scores on the LongMemEval and MemoryAgentBench data are quoted on [LongMemEval](../benchmarks/longmemeval.md) and [MemoryAgentBench](../benchmarks/memoryagentbench.md).
- **WildGraphBench.** 1,197 questions (Table 1 of the full text; the abstract says 1,100) over Wikipedia articles sampled from 12 top-level topics, with their reference pages as the corpus; the number of articles is unstated [12]. No independent use found; Apache-2.0 [13]. It is cited on [GraphRAG-Bench (Xiang)](../benchmarks/graphrag-bench-xiang.md).
- **Text2GraphQuery-Bench.** Question and graph-query pairs in Cypher, GQL and SQL/PGQ. Its headline 267,276 pairs are 22,273 verified examples times 3 languages times 4 question wordings; the toolkit README gives 178,184 pairs, a figure not found in version 2 of the paper [14]. No use beyond its paper found; the toolkit repository is Apache-2.0 and its README states no licence for the dataset [15].
- **CypherTurn.** 721 multi-turn sessions (5,927 turns) of questions and Cypher over seven purpose-built synthetic graphs, first version 20260929 [16]. No LICENSE file [17].
- **TEXT2SPARQL challenge.** A question-to-SPARQL challenge held in 2025 and 2026 [18]. The official site refused the connection on every attempt, so the data version and licence are unstated [18].

The [query-generation papers](../papers/graph-query-generation.md) and [trend](../trends/graph-query-generation.md) report Text2GraphQuery-Bench, CypherTurn and the 2026 TEXT2SPARQL challenge as new work.

## Changes

The latest changes to this chapter's list, newest first, are generated from its change list.

<!-- BEGIN GENERATED: changes -->

| Date | Kind | Subject | Summary | Source |
|---|---|---|---|---|
| 20261102 | added | chapter | First edition: 26 dataset pages (knowledge graphs, question sets, corpora). | docs/datasets/README.md |

Full list: [changes.tsv](changes.tsv)

<!-- END GENERATED: changes -->

## Sources

1. https://arxiv.org/html/1707.01476 : ConvE paper: FB15k and WN18 suffer test leakage through inverse relations; YAGO3-10 is a subset of YAGO3 with at least 10 relations per entity, 123,182 entities, 37 relations (read 20261102 21:57 UTC)
2. https://deepgraphlearning.github.io/project/wikidata5m : Wikidata5M dataset page: 4,594,485 entities; transductive splits of 20,614,279, 5,163 and 5,133 triples; no licence statement (read 20261102 21:56 UTC)
3. https://arxiv.org/html/1911.06136 : KEPLER paper: Wikidata5M built from the July 2019 dump of Wikidata and Wikipedia, with first-section descriptions (read 20261102 21:57 UTC)
4. https://arxiv.org/html/2009.07810 : CoDEx paper: three knowledge graphs with manually verified hard negative triples (read 20261102 21:57 UTC)
5. https://github.com/tsafavi/codex : MIT LICENSE file (licence endpoint read 20261102 21:56 UTC); no data licence in the README (read 20261102 21:42 UTC)
6. https://arxiv.org/abs/2602.10715 : LoCoMo-Plus: cue-trigger benchmark on long conversational memory; version 1 dated 20260211; no instance count in the abstract (read 20261102 21:55 UTC)
7. https://github.com/xjtuleeyf/Locomo-Plus : data/locomo_plus.json parses as a list of 401 items; no LICENSE file (licence endpoint answered not found); the README says "See the repository for license information" (all read 20261102 21:56 UTC)
8. https://arxiv.org/abs/2602.22769 : AMA-Bench (v4, 20260527): real-world agent trajectories with expert-curated questions and synthetic trajectories with rule-based questions (read 20261102 21:55 UTC); full text https://arxiv.org/html/2602.22769 confirms the description (read 20261102 21:55 UTC)
9. https://github.com/AMA-Bench/AMA-Bench : MIT LICENSE file (read 20261102 21:56 UTC)
10. https://arxiv.org/abs/2605.18421 and https://arxiv.org/html/2605.18421 : EvoMemBench (v3, 20261030): "we select or reconstruct six datasets"; Table 2 lists MemoryAgentBench among the sources (read 20261102 21:55 UTC)
11. https://github.com/DSAIL-Memory/EvoMemBench : no LICENSE file (licence endpoint answered not found) (read 20261102 21:56 UTC)
12. https://arxiv.org/abs/2602.02053 and https://arxiv.org/html/2602.02053 : WildGraphBench (v2): the abstract says "1,100 questions" from articles "across 12 top-level topics"; the introduction says "1,100+"; Table 1 of the full text gives 667 single-fact, 191 multi-fact and 339 summary questions, 1,197 in total; no article count found in the text (read 20261102 21:55 UTC)
13. https://github.com/BstWPY/WildGraphBench : Apache-2.0 LICENSE file (read 20261102 21:56 UTC)
14. https://arxiv.org/abs/2602.11745 and https://arxiv.org/html/2602.11745 : Text2GraphQuery-Bench (v2): 267,276 pairs; Table 1 footnote "22,273 × 3 query langs × 4 question annotations"; the toolkit README https://github.com/ldbc/Text2GraphQuery-DataGen gives 178,184 pairs (all read 20261102 21:55 UTC, README 21:56 UTC)
15. https://github.com/ldbc/Text2GraphQuery-DataGen : Apache-2.0 LICENSE file; the README links the dataset downloads and gives no dataset licence (read 20261102 21:56 UTC)
16. https://arxiv.org/abs/2609.36987 and https://arxiv.org/html/2609.36987 : CypherTurn: 721 sessions, 5,927 turns, seven purpose-built synthetic knowledge graphs; version 1 dated 20260929 (read 20261102 21:55 UTC)
17. https://github.com/BarryQ/CypherTurn : no LICENSE file (licence endpoint answered not found) (read 20261102 21:56 UTC)
18. https://arxiv.org/abs/2610.13648 (2026 challenge, eight competing approaches) and https://arxiv.org/abs/2510.02200 (2025 challenge) (read 20261102 21:55 UTC); https://text2sparql.aksw.org : the official site, connection refused (the time of the first attempt was not recorded; again 20261102 21:44 UTC and 21:56 UTC)
