---
type: trend
shift: hand-written queries -> model-written Cypher and SPARQL
status: steady
order: 3
updated: 20261102 23:17 UTC
---

# Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL

This page answers one question: when the knowledge is already in a [graph database](../index/graph-database.md), can a [language model](../index/large-language-model.md) turn a user's question into the database's own query, so that the engine, not the model, finds the answer? It covers the [Cypher](../index/cypher.md) and [SPARQL](../index/sparql.md) side of the field, the three open-source projects that carry it, and the research of the past year. The research is steady, and all the reported scores are first-party (the authors' own).

> **Distinctive because** nothing new is built: the graph already exists, the model translates each question into a query once, and the database engine runs it. The nearest neighbour is [agentic graph retrieval](./learned-graph-traversal.md), where a trained policy walks the graph step by step.

## Why it emerged

A graph database answers exact questions well, but only if the asker writes the query. The Text2Cypher paper (v1 20241213) opens on that obstacle: "using Cypher requires specialized knowledge" [1]. Turning questions into formal queries over a knowledge base is not new. The Empirical Methods in Natural Language Processing conference (EMNLP) in 2013 had "Semantic Parsing on Freebase from Question-Answer Pairs", and the Association for Computational Linguistics meeting (ACL) in 2015 had "Semantic Parsing via Staged Query Graph Generation" (titles only; the abstracts were not on the pages read) [2][3]. The Text2Cypher abstract says a language model can be used for the translation but often misses complex nuances, and it points to fine-tuning on domain data [1]. None of the sources read says why the task came back with [large language models](../index/large-language-model.md) (LLMs), or why it reached [retrieval-augmented generation](../index/retrieval-augmented-generation.md) (RAG) tooling; that cause is **unstated**.

*Reading:* my inference, not a finding of any source, is that a general model can write the query without a parser trained for one knowledge base, which would make the older idea cheap to try inside RAG tooling.

Two query-language facts set the stage. SPARQL became a World Wide Web Consortium (W3C) Recommendation on 20080115 (see [The semantic web and linked data](../history/semantic-web.md)) [4]. GQL (Graph Query Language), the ISO property-graph query language, was published in April 2024: ISO's lifecycle table and the IEC web store give 20240412, and the GQL committee announced it on 20240417 [5][26]; the [GQL](../index/gql.md) entry holds the full account, and [What has settled since 2023](../history/settled-since-2023.md) tells the era. The standards group stated in July 2022 that the graph pattern matching language in [SQL/PGQ](../index/sql-pgq.md) was "essentially identical" to the one in GQL, and in May 2023 that it aimed to keep the two "as identical as possible" [5]. Why the research wave came in 2024 and 2025, and not earlier, is **unstated** in the sources read. The prior-year list includes Text2Cypher, Auto-Cypher and NAT-NL2GQL, all dated December 2024, and a November 2024 evaluation of models for graph query generation (titles only) [6]. Earlier years were not searched.

## Why it matters

- **No index to pay for.** [Graph-based RAG](./graph-based-rag.md) builds its graph with a model before the first question; Microsoft's documentation estimates graph extraction at "roughly 75% of indexing cost" [24]. This route makes one model call per question, in the code read, on a graph that is already there [7].
- **Exact answers.** *Reading:* a database query can count, filter and aggregate, which a retrieved text snippet cannot. This reasoning is mine, not a source's finding.
- **Research keeps pace with the field.** An arXiv API title search finds 52 papers for 20251102 to 20261102 against 38 in the year before (x1.37). The controls in the same API move by x1.38 (any LLM wording), x1.23 (any RAG wording) and x2.50 (LLM-agent wording) [6][8]. A wider query on abstracts, whose exact wording was not kept, gave 57 against 34 (x1.68) [6]. The arXiv search page, read later with other settings (computer science only, first-submission date), gives 51 against 37 (x1.38) for the same title words and x1.37 for LLM wording in abstracts [25]. *Reading:* the topic grows about as fast as the LLM control, no faster, which is why the status is "steady"; these are keyword counts. By my reading of titles, 34 of the 52 and 20 of the 38 are about generating graph queries from questions; the rest are unrelated words (object detection, music, query-engine theory) [6].
- **Standards widen the target.** One benchmark now covers three languages at once: Cypher, GQL and SQL/PGQ. Its authors call it the first to cover all mainstream declarative property graph query languages [9].

## How it works

A pipeline of five steps, shown with the code of Neo4j's `Text2CypherRetriever`, the most direct example [10]:

1. **Describe the graph.** The prompt carries the database schema (labels, relationship types, properties), read from the database or passed in, and optionally question-and-query examples.
2. **Translate.** The model returns one query. The default prompt says "Do not use any properties or relationships not included in the schema" [10].
3. **Check.** The retriever asks the database to `EXPLAIN` the query and refuses to run anything whose query type is not read-only [10].
4. **Execute.** The engine runs the query. The records, and the query itself, come back as the result [10].
5. **Answer or repair.** A [RAG](../index/retrieval-augmented-generation.md) layer writes the final answer from the records. Research adds repair loops that feed errors back to the model (see below).

The model can be a small, separate one. Code-Graph-RAG lets the user set a provider and model only for its Cypher generator [11]. [Fine-tuning](../index/fine-tuning.md) is the other lever: The Text2Cypher paper's dataset of 44,387 instances, merged from public sets, was built to train and score models on this task [1].

### Two target families

| Target | Graph model | Examples read |
|---|---|---|
| Cypher, GQL, SQL/PGQ | [property graph](../index/property-graph.md) | Text2Cypher, CypherTurn, CypherGuard, KG2Cypher [1][12][13][14] |
| SPARQL | [RDF](../index/rdf.md) (Resource Description Framework) triples in a [triple store](../index/triple-store.md) | SPARQL-LLM, SAGA, Learning to Refine [15][16][17] |

A 2025 paper says GraphRAG research has focused mostly on RDF and SPARQL, and builds a text-to-Cypher system for property graphs on [Memgraph](../projects/memgraph.md) [18].

### Text-to-SPARQL challenges

Merged here because the mechanism is the same (translate once, the engine executes) and only the target language differs. The Second International TEXT2SPARQL Challenge was co-located with Text2KG at the European Semantic Web Conference (ESWC) 2026 on 20260510 [19]. It had two subtasks, a [DBpedia](../index/dbpedia.md) one (English and Spanish) and one over a corporate graph (English and German), 50 questions each [19]. One entrant's paper (v1 20261009) reports ranking first "among eight competing approaches" [19]. The paper is not consistent on three points: its abstract says accuracy while its tables use F1 (a score that balances precision and recall); its body says the entrant was evaluated against four other systems, two of them submitted with several variants, so "eight" probably counts variants (my inference from the tables, not stated); and it names a scoring tool, T2S-Metrics, without saying who ran it [19]. The challenge's own site could not be reached, so the organisers and who ran the scoring are **unstated** here.

### Agentic and learned variants

The model still emits a query for the engine to run. Four lines of work add a loop around that step. The learned-repair line borders on [Agentic graph retrieval](./learned-graph-traversal.md), where the catalogue places reinforcement-learned controllers; it is kept here because the learned model's output is still a query:

- **Execution feedback.** LAST-CQ runs a five-agent, training-free loop and finds that detecting a failure and retrying matters more than how rich the feedback is [20].
- **Learned repair.** A 3B-parameter model, trained by outcome-driven [reinforcement learning](../index/reinforcement-learning.md), builds and repairs SPARQL over several steps [17].
- **Schema grounding.** SAGA tracks entity types and filters properties that do not fit them before the model chooses [16].
- **Tools.** One study gives agents SPARQL access through the [Model Context Protocol](../index/model-context-protocol.md) for federated questions [21].

These stay in this family because the answer still comes from one executable query per attempt. They are the border with [Agentic graph retrieval](./learned-graph-traversal.md), where the model's moves are over graph nodes.

## Representative projects

| Project | Role | Stars (snapshot 20261030 19:54 UTC) | Licence (LICENSE file) | Latest release |
|---|---|---|---|---|
| [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md) | `Text2CypherRetriever`, one retriever among several in Neo4j's own GraphRAG library | 1,326 | Apache-2.0, with some files under the Python Software Foundation (PSF) licence [10] | 1.23.0, 20261028 |
| [Code-Graph-RAG](../projects/code-graph-rag.md) | English to Cypher over a graph of source code | 5,303 | MIT [11] | v0.4.19, 20261101 |
| text2cypher (Neo4j Labs, [repository](https://github.com/neo4j-labs/text2cypher)) | datasets, evaluation and fine-tuning notebooks; "experimental", outside Neo4j's supported products | 245 | CC0-1.0 [22] | none |

Stars come from the dated snapshot and carry no fast-growth flag for any of the three [23]. The snapshot's search is thin here: one query, `text2cypher` in name, description or README, returned 5 active and 7 quiet repositories [23]; the snapshot README states no star threshold for it. The graph databases underneath are [Neo4j](../projects/neo4j.md) and [Memgraph](../projects/memgraph.md). Text-to-SQL tools sit next door and are out of scope; for example [Wren AI](https://github.com/Canner/WrenAI) has 18,020 stars in the same snapshot [23].

## Fundamental papers

The list of record is the [group page for this trend](../papers/graph-query-generation.md). The papers read here: Text2Cypher (20241213), a dataset and fine-tuning study named for the task [1]; Text2GraphQuery-Bench (20260212), 267,276 question-query pairs over 34 databases in Cypher, GQL and SQL/PGQ [9]; and SPARQL-LLM (20251216), the SPARQL system that went on to the 2026 challenge [15][19]. The semantic-parsing papers of 2013 and 2015 are the older line [2][3].

## What is measured, and by whom

No experiment of this documentation tests this trend (see [Experiments](../experiments/README.md)). The scores below come from the papers, on different data and metrics, and cannot be ranked against each other.

| Result | Metric | Who ran it | First-party? | Date (paper v1) | Source |
|---|---|---|---|---|---|
| 88.50% | execution accuracy, CypherBench, seven graphs (CypherGuard) | the method's authors | yes | 20261030 | [13] |
| 64.7% best of 15 models; session-level correctness under 5% | execution accuracy, CypherTurn multi-turn | the benchmark's authors | yes, for their own benchmark | 20260929 | [12] |
| first of eight (variants included); 59% above the second-best on Spanish DBpedia | F1 in the tables, "accuracy" in the abstract; TEXT2SPARQL 2026 (challenge 20260510) | the system's authors; scorer unstated | yes | 20261009 | [19] |
| F1 0.806 to 0.950 and 0.70 to 0.92 after fine-tuning | execution-result F1, Korean enterprise graphs | the method's authors | yes | 20260626 | [14] |
| 49.7%, 17.5 points over the best iterative zero-shot baseline | accuracy after entity linking, curated subset of [LC-QuAD](../datasets/lc-quad.md) 2.0 | the method's authors | yes | 20251114 | [17] |

Other findings in the same papers: spending the same call budget on parallel sampling lowered quality by 10 to 11% (the abstract does not name the comparator), and an [LLM judge](../index/llm-as-judge.md) was about nine points more optimistic than blind human labels [20]. Independent replication of any row above: **unstated** (none found in the sources read).

## Assessment

*Reading:* the strength is economy and exactness. The graph stays where it is, the answer comes from the engine, and the query can be read and checked. The weaknesses are in the evidence and the failure rate. All the scores above are first-party, and the multi-turn benchmark's best model gets under two thirds of turns right and under 5% of sessions [12]. Quality depends on the schema in the prompt, so a changing or undocumented schema is a risk; SAGA names a failure it calls "type-blind grounding" [16]. A generated query is also code run against a database, which is why Neo4j's retriever refuses non-read-only queries [10]. The direction of travel is toward correction layers, fine-tuned small models and agent loops. As agents take over the repair step, this trend will merge into [Agentic graph retrieval](./learned-graph-traversal.md). Productisation is partial: one named retriever in one vendor's package, and a code-graph tool where it is one capability beside editing and tracing [10][11].

## Signals to watch

- Whether the 2026 results are repeated by someone other than the authors, on the same data.
- A third TEXT2SPARQL challenge, and whether its scoring is published by its organisers (unstated for 2026).
- Whether GQL and SQL/PGQ become standard targets in tools, as Text2GraphQuery-Bench already treats them [9].
- Whether retrievers like `Text2CypherRetriever` gain agent loops, or stay one-shot.
- The next snapshot: the search above is thin, and this trend is under-counted in it [23].

## Sources

1. https://arxiv.org/abs/2412.10064 : Text2Cypher (Ozsoy, Messallem, Besga, 4 authors; v1 20241213); quote on specialised knowledge; 44,387 instances; fine-tuned models beat baselines on Google-BLEU and Exact Match; the abstract says models often miss complex nuances and does not mention RAG (re-read 20261102 20:35 UTC)
2. https://aclanthology.org/D13-1160/ : Berant et al., "Semantic Parsing on Freebase from Question-Answer Pairs", EMNLP 2013; title and venue only, abstract not on the page (read 20261102 20:20 UTC)
3. https://aclanthology.org/P15-1128/ : Yih et al., "Semantic Parsing via Staged Query Graph Generation", ACL-IJCNLP 2015; title and venue only (read 20261102 20:20 UTC)
4. https://www.w3.org/TR/rdf-sparql-query/ : SPARQL Recommendation, 15 January 2008 (read 20261102 19:54 UTC, via the era page `docs/history/semantic-web.md`)
5. https://www.gqlstandards.org/ : GQL, ISO/IEC 39075:2024, announced as published 17 April 2024; July 2022 update: graph pattern matching in SQL/PGQ "essentially identical" to GQL's; May 2023 update: GQL's kept "as identical as possible" (re-read 20261102 20:34 UTC)
6. https://export.arxiv.org/api/query : arXiv API, query `ti:Cypher OR ti:SPARQL OR ti:Text2Cypher OR ti:"Text-to-Cypher" OR ti:Text2SPARQL OR ti:"Text-to-SPARQL" OR ti:NL2SPARQL OR ti:NL2Cypher OR ti:"graph query"` with submittedDate 202511020000 to 202611022359: 52 results; 202411020000 to 202511012359: 38 results. A second, wider query on abstracts (wording not kept) gave 57 and 34. Titles read for the on-topic share (read 20261102 20:10 UTC). These counts were not re-run in the repair pass: the API answered HTTP 429 at 20:33 UTC, so they stand on the first read; [25] is a cross-check on another engine. These are keyword counts, not the size of the field
7. https://github.com/neo4j/neo4j-graphrag-python/blob/main/src/neo4j_graphrag/retrievers/text2cypher.py : one model call per question, then query execution (read 20261102 20:12 UTC)
8. https://export.arxiv.org/api/query : growth controls, same date windows: any-LLM wording 44,692 against 32,396; any-RAG wording 3,357 against 2,736; LLM-agent wording 15,158 against 6,068 (any-LLM and any-RAG counts read twice, 20261102 20:22 UTC, with the same numbers; the LLM-agent count was read 20261102 19:46 to 19:47 UTC and its re-read was refused with HTTP 429; none of the three could be re-run at 20:33 UTC for the same reason)
9. https://arxiv.org/abs/2602.11745 : Text2GraphQuery-Bench (Lyu, Ban, Wu, 15 authors; v1 20260212): 267,276 pairs, 34 databases, 13 domains, Cypher, GQL, SQL/PGQ, 8 LLMs (read 20261102 20:18 UTC)
10. https://github.com/neo4j/neo4j-graphrag-python : `retrievers/__init__.py` exports `Text2CypherRetriever`; `text2cypher.py` (schema, examples, `EXPLAIN`, read-only check); `prompts.py` default prompt; `LICENSE.txt` (Apache 2.0, parts PSF v2; the GitHub API reports NOASSERTION); latest release 1.23.0 published 20261028 (read 20261102 20:12 UTC; the latest-release call was run again 20261102 22:52 UTC with the same result)
11. https://github.com/vitali87/code-graph-rag : README ("turns natural language into Cypher queries"; SQLite default, Memgraph and Neo4j opt-in), `docs/sdk/cypher-generator.md` (separate Cypher provider and model), `LICENSE` MIT, latest release v0.4.19 published 20261101 20:01 UTC (read 20261102 20:12 UTC; the latest-release call was run again 20261102 22:54 UTC with the same result; git tags run ahead, to v0.4.25)
12. https://arxiv.org/abs/2609.36987 : CypherTurn (Zhang, Zhu, Yang et al.; v1 20260929; EMNLP 2026 oral): 721 sessions, 5,927 turns, 15 models, best 64.7% (read 20261102 20:18 UTC)
13. https://arxiv.org/abs/2610.41755 : CypherGuard (Chen, Wen, Ozsoy, 4 authors; v1 20261030): 88.50% execution accuracy on CypherBench (read 20261102 20:18 UTC)
14. https://arxiv.org/abs/2606.27742 : KG2Cypher (Choi, Kim, Seo, 6 authors; v1 20260626): F1 figures (read 20261102 20:18 UTC)
15. https://arxiv.org/abs/2512.14277 : SPARQL-LLM (Smeros, Emonet, Wang, 5 authors; v1 20251216) (read 20261102 20:18 UTC)
16. https://arxiv.org/abs/2607.14494 : SAGA (Zhang, Tsuda; v1 20260716): "type-blind grounding" (read 20261102 20:18 UTC)
17. https://arxiv.org/abs/2511.11770 : Learning to Refine (Vossebeld, Wang; v1 20251114): 3B model, GRPO, 49.7% (read 20261102 20:18 UTC)
18. https://arxiv.org/abs/2511.08274 : Multi-Agent GraphRAG, text-to-Cypher on Memgraph (Gusarov, Volkova, Khrulkov, 6 authors; v1 20251111) (read 20261102 20:18 UTC)
19. https://arxiv.org/abs/2610.13648 and https://arxiv.org/html/2610.13648 : SPARQL-LLM in the TEXT2SPARQL 2026 Challenge (v1 20261009): subtasks, 50 questions each, F1, eight approaches, ESWC 2026 on 20260510; Co-located with Text2KG at ESWC26, 10 May 2026; abstract: "among eight competing approaches" and "up to 59% higher accuracy"; Table 3 (Spanish DBpedia): .7810 against .4904 for the second-best, an F1; body: "four other systems, two of which were submitted with multiple variants"; Figure 1 credits the T2S-Metrics tool; the paper does not say who ran the scoring. https://text2sparql.aksw.org/ was unreachable (abstract page and HTML re-read 20261102 20:34 UTC; challenge site read 20261102 20:19 UTC)
20. https://arxiv.org/abs/2609.12746 : LAST-CQ (Prokopiou, Aidinis, Kyrmpatsos, 4 authors; v1 20260911): five-agent, training-free; 2,471 live-database queries; parallel sampling at the same call budget "degrades quality by 10-11%"; LLM judge "optimistic by 9 points" (abstract re-read 20261102 20:35 UTC)
21. https://arxiv.org/abs/2603.06582 : Agentic SPARQL (Dobriy, Bauer, Azzam, 5 authors; the page gives submission 20260120 and an online date of 20260409, while the identifier prefix 2603 would fit March 2026; the cause is unstated): SPARQL-MCP agents; the abstract gives no figures (re-read 20261102 20:34 UTC)
22. https://github.com/neo4j-labs/text2cypher : README ("experimental Neo4j Labs project"), `LICENSE` CC0-1.0 (read 20261102 20:12 UTC)
23. https://github.com/lucagattoni/knowledge-graph-tutorial/tree/main/kb-kg/landscape/20261030_1954-github : the snapshot of 20261030 19:54 UTC; `README.md` search-query table (the `text2cypher` rows give 5 and 7 and no star threshold) and the rows of `repos.tsv` beside it for stars, flags and push dates (read 20261102 20:08 UTC; search rows re-read 20261102 20:35 UTC)
24. https://microsoft.github.io/graphrag/index/methods/ : "We estimate graph extraction to constitute roughly 75% of indexing cost." (read 20261102 20:35 UTC)
25. https://arxiv.org/search/advanced : abstract-page search, computer science, first-submission date 20251102-20261102 against 20241102-20251101; title words as in [6]: 51 against 37; abstract wording `"large language model" OR LLM`: 43,946 against 32,020 (read 20261102 20:34 UTC). Differs from the API counts in [6][8]; which setting explains the difference is unstated
26. https://committee.iso.org/es/sites/isoorg/contents/data/standard/07/61/76120.html and https://webstore.iec.ch/publication/94107 : ISO catalogue page for ISO/IEC 39075:2024, lifecycle table with "International Standard published" (stage 60.60) on 2024-04-12; IEC web store, publication date 2024-04-12 (iso.org itself returned 403; read 20261102 22:52 to 22:57 UTC; the dates are reconciled on the GQL index entry)
