---
type: chapter
updated: 20261102 21:55 UTC
---

# Benchmarks

A benchmark page holds the evaluation: what is asked, how answers are scored, the protocol, and dated results with who ran each one and whether they are first-party. A [dataset page](../datasets/README.md) holds the data instead: content, size, licence and how it was made. An item that is both has one page of each, linked, and nothing is repeated between them. This chapter has 24 benchmark pages in five task families; no page ranks systems across studies, because each study fixes its own reader, judge, corpus and subset [2].

## How they were chosen

A benchmark gets a page when it passes at least one of three tests (decision D-3): a fundamental paper of the [papers chapter](../papers/README.md) uses it, a [trend](../trends/README.md) uses it, or it is widely used, meaning a citation count of its paper from a named source, with the time it was read [1]. Counts are carried over from the research pass, which read them from Semantic Scholar on 20261102 and could not query again because of rate limits [3]. They include 5,972 (HotpotQA, counted for arXiv 1809.09600), 2,235 (BEIR) and 1 (RAGSearch) [3]. A count depends on the source and on the identifier it was read for: the [HotpotQA dataset page](../datasets/hotpotqa.md) carries 1,807 from OpenAlex for the published version, and an arXiv-DOI record in OpenAlex shows far fewer. *Reading:* a low count on a recent paper says it is new, not weak; such a benchmark can pass on the use of a trend or a paper instead. Two of the benchmarks, GraphRAG-Bench (Xiang) and RAGSearch, report findings and are also papers of the graph-based RAG group in chapter 4 [1]. A count from one source is never compared with a count from another.

The split between a benchmark page and a dataset page follows decision D-2 [1]. The 24 pages fall into four cases:

| Case | Pages | Where the data is described | Benchmarks |
|---|---|---|---|
| Data used beyond the benchmark's own protocol, and the item also defines an evaluation | A dataset page and a benchmark page with the same slug | The dataset page; the benchmark page links to it | HotpotQA, Natural Questions, MuSiQue, 2WikiMultiHopQA, MS MARCO, MultiHop-RAG, LongMemEval, LoCoMo, WebQuestionsSP, LC-QuAD |
| Data that has dataset pages under other names | A benchmark page; the dataset pages link back | The dataset pages | KILT (the Wikipedia snapshots page), knowledge graph link prediction (FB15k-237 and WN18RR) |
| Data used only inside the benchmark's own protocol | A benchmark page only | Its "Datasets" section | BEIR, FRAMES, CRAG, STaRK, both GraphRAG-Benches, EnterpriseRAG-Bench, MemoryAgentBench, Text2KGBench, Text2Cypher, OGB link prediction |
| No data of its own | A benchmark page only | The dataset pages of the sets it re-uses | RAGSearch |

Each benchmark is listed once, under the task its results mainly report. A benchmark that asks for retrieval from a graph together with text (CRAG, STaRK) is under graph-based RAG. A benchmark that answers questions from a knowledge graph (WebQuestionsSP, LC-QuAD) is under construction and query. The two benchmarks called GraphRAG-Bench are unrelated and have separate pages.

## Retrieval and question answering

Benchmarks that score a retriever, a reader, or both, on text. The first four are the question sets that graph-based RAG studies reuse; each page's "Used by" section says which. Each row summarises the linked page [2].

| Benchmark | What it tests | Data | Main metric |
|---|---|---|---|
| [HotpotQA](hotpotqa.md) | Answering a [multi-hop](../index/multi-hop-question-answering.md) question from several documents and naming the sentences that support the answer, in a distractor or a fullwiki setting | [HotpotQA](../datasets/hotpotqa.md) | Answer and supporting-fact [exact match](../index/exact-match.md) and F1, with joint scores |
| [Natural Questions](natural-questions.md) | Finding the short or long answer to a real search query in a Wikipedia page; later work retrieves from Wikipedia and then answers | [Natural Questions](../datasets/natural-questions.md) | Long and short answer F1 on the original task; exact match in open-domain use |
| [MuSiQue](musique.md) | Answering multi-hop questions by using every reasoning step, with shortcut use measured; the Full variant adds unanswerable twins | [MuSiQue](../datasets/musique.md) | Answer F1 and supporting-paragraph F1; sufficiency-adjusted scores for Full |
| [2WikiMultiHopQA](2wikimultihopqa.md) | Multi-hop questions with an explicit reasoning path: the answer, the supporting facts and the evidence triples | [2WikiMultiHopQA](../datasets/2wikimultihopqa.md) | Exact match and F1 for each of the three tasks, with joint scores |
| [MS MARCO](ms-marco.md) | Putting a passage that answers a real search query near the top of a ranking | [MS MARCO](../datasets/ms-marco.md) | [MRR](../index/mean-reciprocal-rank.md)@10 on the retired leaderboard; [nDCG](../index/ndcg.md)@10 in TREC Deep Learning |
| [BEIR](beir.md) | Zero-shot retrieval on 18 existing datasets from 9 tasks, for models trained elsewhere, mostly on MS MARCO | Described on its page; three of the sets have dataset pages: [HotpotQA](../datasets/hotpotqa.md), [Natural Questions](../datasets/natural-questions.md), [MS MARCO](../datasets/ms-marco.md) | nDCG@10; Recall@100 is also reported |
| [KILT](kilt.md) | One model and one index serving eleven datasets in five knowledge-intensive tasks, scoring the answer and the evidence pages together | [Wikipedia snapshots](../datasets/wikipedia-dpr-kilt.md); the QA sets include [Natural Questions](../datasets/natural-questions.md), [HotpotQA](../datasets/hotpotqa.md) and [TriviaQA](../datasets/triviaqa.md) | Accuracy, exact match, ROUGE-L or F1 per task; the KILT scores count a point only if the right evidence page is retrieved |
| [FRAMES](frames.md) | 824 human-written questions that need 2 to 15 Wikipedia articles, testing factuality, retrieval and reasoning in one end-to-end [RAG](../index/retrieval-augmented-generation.md) score | Described on its page | Accuracy judged by an LLM |

## Graph-based RAG

Benchmarks of RAG pipelines, most of them built or used to ask whether a graph helps; the trend is told on [graph-based RAG](../trends/graph-based-rag.md). Several results here were run by the benchmark's own authors; each page marks them. Each row summarises the linked page [2].

| Benchmark | What it tests | Data | Main metric |
|---|---|---|---|
| [GraphRAG-Bench (Xiang)](graphrag-bench-xiang.md) | When, and at which stage of a [GraphRAG](../index/graphrag.md) pipeline, a graph helps, over four task levels and two corpora (Novel, Medical); ICLR 2026 | Described on its page | Accuracy per level; ROUGE-L, coverage and faithfulness for some levels |
| [GraphRAG-Bench (Xiao)](graphrag-bench-xiao.md) | Whether a graph improves a model's reasoning, on 1,018 college-level computer-science textbook questions with gold rationales; a different benchmark with the same name | Described on its page | Accuracy per question format; rationale scores R and AR |
| [RAGSearch](ragsearch.md) | Whether multi-round agentic search removes the need for an offline-built graph, comparing dense retrieval with five GraphRAG backends | Six existing sets: [Natural Questions](../datasets/natural-questions.md), [PopQA](../datasets/popqa.md), [TriviaQA](../datasets/triviaqa.md), [HotpotQA](../datasets/hotpotqa.md), [2WikiMultiHopQA](../datasets/2wikimultihopqa.md), [MuSiQue](../datasets/musique.md) | Contain exact match (the gold answer appears in the output) and F1 |
| [MultiHop-RAG](multihop-rag.md) | Whether a RAG pipeline finds and combines evidence from several news articles, and says so when no evidence exists | [MultiHop-RAG](../datasets/multihop-rag.md) | Hit@K, MAP@K and MRR@K for retrieval; accuracy for answers |
| [EnterpriseRAG-Bench](enterpriserag-bench.md) | RAG over the internal documents of a synthetic company (over 500,000 documents, 500 questions): lookups, multi-document reasoning, conflicts and absent answers | Described on its page | Four scores per question (correctness, completeness, document recall, invalid extra documents); the leaderboard score is completeness if correct, else zero |
| [CRAG](crag.md) | Factual question answering from web pages and mock knowledge-graph APIs, scored so that a wrong answer costs more than "I don't know" | Described on its page | Per-question score of 1, 0.5, 0 or -1, averaged; the automatic evaluation uses 1, 0 and -1 |
| [STaRK](stark.md) | Retrieving the nodes that match a query with a text part and a relation part, over three semi-structured knowledge bases (Amazon, MAG, Prime) | Described on its page | Hit@1, Hit@5, Recall@20 and MRR |

## Agent memory

Benchmarks of [agent memory](../index/agent-memory.md): sessions or long texts arrive first, questions follow. They belong to the [agent memory](../trends/agent-memory.md) trend. *Reading:* on these pages many published scores come from the authors or vendors of the system scored, and plain retrieval or full-context baselines often score as high as the memory systems; each page labels who ran each row. Each row summarises the linked page [2].

| Benchmark | What it tests | Data | Main metric |
|---|---|---|---|
| [LongMemEval](longmemeval.md) | The long-term memory of a chat assistant: timestamped sessions arrive in order, then a dated question, across five abilities | [LongMemEval](../datasets/longmemeval.md) | Accuracy judged by an LLM (gpt-4o); Recall@k and NDCG@k where the system exposes its retrieval |
| [LoCoMo](locomo.md) | Memory of a dialogue spread over up to 35 sessions: question answering, event summarisation and dialogue generation | [LoCoMo](../datasets/locomo.md) | F1 for question answering; later work uses an LLM judge, and the two groups of scores are not comparable |
| [MemoryAgentBench](memoryagentbench.md) | Four competencies of an agent's memory: accurate retrieval, test-time learning, long-range understanding and selective forgetting; 2,071 questions | Described on its page; one set is a re-cut of [LongMemEval](../datasets/longmemeval.md) | Per-set metrics (substring match, LLM judge, accuracy, Recall@5, F1 times fluency); overall is the mean of the four competency averages |

## Knowledge-graph construction and query

Benchmarks for building a graph from text and for asking a graph a question. They serve the trends [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md) and [Asking graphs in natural language](../trends/graph-query-generation.md). Each row summarises the linked page [2].

| Benchmark | What it tests | Data | Main metric |
|---|---|---|---|
| [Text2KGBench](text2kgbench.md) | Turning sentences into [triples](../index/triple.md) that follow a given [ontology](../index/ontology.md), without inventing facts | Two datasets, Wikidata-TekGen and DBpedia-WebNLG, described on its page | Precision, recall and F1; ontology conformance; subject, relation and object hallucination |
| [Text2Cypher](text2cypher.md) | Turning a question and a [property graph](../index/property-graph.md) schema into a [Cypher](../index/cypher.md) query | 44,387 question-schema-query rows, described on its page | Google-BLEU for translation; Exact Match for execution |
| [LC-QuAD](lc-quad.md) | Turning a complex question into a [SPARQL](../index/sparql.md) query, or into the answer it returns, over DBpedia (1.0) or Wikidata (2.0) | [LC-QuAD](../datasets/lc-quad.md) | F1 on answers or queries; five protocols are in use, listed on the page |
| [WebQuestionsSP](webquestionssp.md) | Returning the set of Freebase entities or values that answers a short question | [WebQuestionsSP](../datasets/webquestionssp.md) over [Freebase](../datasets/freebase.md) | Average F1 and Hits@1 |

## Knowledge-graph completion

Benchmarks of [knowledge graph completion](../index/knowledge-graph-completion.md) by [link prediction](../index/link-prediction.md): fill in a missing entity of a triple. They use no text and no questions. The filtered protocol comes from the TransE paper, a paper of the [foundations](../papers/foundations.md) group [2]. Each row summarises the linked page [2].

| Benchmark | What it tests | Data | Main metric |
|---|---|---|---|
| [Knowledge graph link prediction](kg-link-prediction.md) | Ranking the true entity above all others for a held-out triple, in the filtered setting | [FB15k-237](../datasets/fb15k-237.md) and [WN18RR](../datasets/wn18rr.md); YAGO3-10 is described on the page | Filtered MRR, Hits@k and mean rank |
| [OGB link prediction](ogb-link-prediction.md) | Recovering held-out triples of `ogbl-wikikg2`, a Wikidata extract split by time, against sampled negatives | Described on its page, built from [Wikidata](../datasets/wikidata.md) | MRR against 1,000 sampled negatives, averaged over 10 seeds |

## Considered and not given a page

These were read for the chapter and left to this mention. A later change is a dated row in the list of changes below. Citation counts are Semantic Scholar, read 20261102 20:00 UTC, carried over [3].

Benchmarks:

- **LoCoMo-Plus** (arXiv 2602.10715, first posted 20260211): tests whether a model keeps implicit user state, goals and values across a long conversation [4]. No use outside its own paper was found; 23 citations [3]. The [LoCoMo](locomo.md) page quotes its scores for plain LoCoMo.
- **AMA-Bench** (2602.22769, 20260226): memory questions over agent trajectories instead of dialogue [4]. No other paper using it was found; 58 citations [3].
- **EvoMemBench** (2605.18421, 20260518): compares 15 memory methods with long-context baselines along two axes, scope and content [4]. A derived benchmark; no use found; 19 citations [3]. Its LongMemEval rows are on the [LongMemEval](longmemeval.md) page.
- **WildGraphBench** (2602.02053, 20260202): GraphRAG over the external documents cited by Wikipedia articles in 12 top-level topics, with 1,100 questions [9]. No independent use found: a later scaling study, BM25 Wins at Scale, shares its first author [4]. 2 citations [3].
- **Text2GraphQuery-Bench** (2602.11745, 20260212): question and query pairs for Cypher, GQL and SQL/PGQ over 34 databases [4]. Its headline 267,276 pairs are 22,273 verified examples times 3 query languages times 4 question phrasings [5]. No use beyond its own paper found; 2 citations [3].
- **CypherTurn** (2609.36987, 20260929): multi-turn text-to-Cypher, 721 sessions and 5,927 turns [4]. First posted five weeks before it was read; 0 citations [3]; no use found.
- **TEXT2SPARQL challenge** (2025 and 2026 editions): a shared task turning questions into SPARQL; the 2026 participant paper SPARQL-LLM reports that it outperforms four other systems (eight rows in its results table, because two systems sent several variants) and gains up to 59% F1 over the second-best, its own authors' claim [10]. The organisers' site refused the connection on 20261102 21:45 UTC, so the data, protocol and official results could not be read [6]. Participant papers carry 0 to 11 citations [3].

Datasets that also define a link-prediction evaluation:

- **FB15k and WN18**: told inside the [FB15k-237](../datasets/fb15k-237.md) and [WN18RR](../datasets/wn18rr.md) pages, which replaced them because their test sets leaked answers [7].
- **YAGO3-10**: described on the [link prediction](kg-link-prediction.md) page; two near-duplicate relations make up over 63% of its test triples [7].
- **Wikidata5M**: 4,594,485 entities and 20,624,575 triples from the July 2019 Wikidata dump; the KEPLER paper that introduced it has 900 citations [3][8]. Only the dataset authors' results and a later paper's own results were read; no independent re-run was found [8]. *Reading:* by citation count alone it could pass the "widely used" test; the catalogue left it to this mention, and [OGB link prediction](ogb-link-prediction.md) covers Wikidata-scale completion.
- **CoDEx**: three knowledge graphs of different size from Wikidata and Wikipedia, with hard negative triples (EMNLP 2020) [8]. Only first-party results were found; its citation count is unstated.

## Changes

The latest changes to this chapter, newest first: benchmarks added, updated, settled, faded or removed.

<!-- BEGIN GENERATED: changes -->

| Date | Kind | Subject | Summary | Source |
|---|---|---|---|---|
| 20261102 | added | chapter | First edition: 24 benchmark pages with dated results tables; first-party results are marked. | docs/benchmarks/README.md |

Full list: [changes.tsv](changes.tsv)

<!-- END GENERATED: changes -->

## Sources

1. plans/20261102_1951-docs-catalogue.md : chapters 5 and 6: selection rule D-3, split rule D-2, the 24 benchmark pages and the list of items considered. A decision record, not a primary source (read 20261102 21:46 UTC)
2. The 24 pages in this folder, from [hotpotqa.md](hotpotqa.md) to [ogb-link-prediction.md](ogb-link-prediction.md) : each table row, each placement and each count of pages summarises its page, which carries the primary sources and their read times (read 20261102 21:38 to 21:44 UTC)
3. https://api.semanticscholar.org/graph/v1/paper/batch : citation counts of the papers, read by the research pass on 20261102 at 20:00 and 20:01 UTC and carried over; HotpotQA 5,972 (for arXiv 1809.09600), BEIR 2,235, RAGSearch 1, WildGraphBench 2, EvoMemBench 19, LoCoMo-Plus 23, AMA-Bench 58, CypherTurn 0, Text2GraphQuery-Bench 2; the TEXT2SPARQL participant papers 0, 7 and 11; the KEPLER count 900 was read at 19:51 UTC. Not queried again: the interface was rate-limited on 20261102
4. https://export.arxiv.org/api/query : records of 2602.10715, 2602.22769, 2605.18421, 2602.02053, 2602.11745, 2609.36987 and 2607.26497: titles, first-version dates, authors, abstracts and comments (read 20261102 21:43 UTC; 2607.26497 read 21:44 UTC)
5. https://arxiv.org/html/2602.11745v2 : Text2GraphQuery-Bench v2, Table 1 footnote (22,273 examples times 3 query languages times 4 question annotations) and Section 5.1 (read 20261102 21:45 UTC)
6. https://text2sparql.aksw.org : connection refused (tried 20261102 21:45 UTC); https://ceur-ws.org/Vol-4094/ : reachable, workshop proceedings not read for this page (tried 20261102 21:45 UTC)
7. [fb15k-237.md](../datasets/fb15k-237.md), [wn18rr.md](../datasets/wn18rr.md) and [kg-link-prediction.md](kg-link-prediction.md) : test leakage in FB15k and WN18; YAGO3-10 duplicate relations; each page cites the ConvE paper (https://arxiv.org/pdf/1707.01476) and Akrami et al. (read 20261102 21:46 UTC, via these pages)
8. https://arxiv.org/abs/1911.06136 and https://arxiv.org/abs/2009.07810 : KEPLER (first version 20191113, TACL) and CoDEx (first version 20200916, EMNLP 2020): records read 20261102 21:43 UTC; the Wikidata5M entity and triple counts were read in the KEPLER full text by the research pass on 20261102 at 19:55 UTC and carried over, as was its finding that no independent re-run of Wikidata5M appears on the pages it read
9. https://arxiv.org/abs/2602.02053 : WildGraphBench abstract: Wikipedia articles from 12 top-level topics, their external references as the retrieval corpus, 1,100 questions (read 20261102 21:53 UTC)
10. https://arxiv.org/abs/2512.14277 and https://arxiv.org/html/2512.14277v2 : SPARQL-LLM, abstract and Table 3 (TEXT2SPARQL 2026): evaluated against four other systems, two submitted with several variants; up to 59% F1 over the second-best system; the words "first place" do not appear (read 20261102 21:53 UTC)
