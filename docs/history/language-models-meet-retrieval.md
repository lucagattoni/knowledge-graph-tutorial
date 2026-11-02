---
type: era
period: 2018-2022
order: 7
updated: 20261102 23:11 UTC
---

# Language models meet retrieval (2018-2022)

This page answers: how did pretrained language models change search and question answering, and what happened to knowledge graphs, ontologies and databases in the same years? It runs from [BERT](../index/bert.md) (October 2018) to ChatGPT (November 2022). The previous era is [Knowledge graphs at scale](knowledge-graphs-at-scale.md); the next is [What has settled since 2023](settled-since-2023.md). The whole span is on the [chapter overview](README.md).

## Dates and boundaries

**The scheme is this documentation's.** No source read gives one periodisation for all four threads.

**Start, 2018.** Lin, Nogueira and Yates write that BERT "arrived on the scene in October 2018", and that the TREC 2019 Deep Learning Track treated BERT-based and earlier neural rankers as "two different 'eras'" [1]. The arXiv record dates the BERT preprint 20181011 [2].

*Disagreement on the start.* Gao et al. say [RAG](../index/retrieval-augmented-generation.md)'s "inception coincided with the rise of the Transformer architecture" [4]; the [Transformer](../index/transformer.md) preprint is dated 20170612 [3]. The archive's LLM-era page starts on 20200522, the RAG paper, and calls its phase boundaries "the author's judgement" [18]. *Reading:* this page starts at BERT because the sources date the change in ranking from BERT (October 2018; January 2019 on [MS MARCO](../datasets/ms-marco.md)) [1]. The start is a judgement, not a source's date. A reader who wants only the named RAG pattern should start at 2020.

**End, 2022.** The era ends with ChatGPT, announced 30 November 2022 [7]. Gao et al. call its arrival "a pivotal moment" for RAG [4]; Stonebraker and Pavlo say LLMs became "mainstream" with it in late 2022 [5]. The period field keeps 2022 whole, as the archive's phase 1 does (to 20221231) [18].

## What changed

Before 2018 the common baseline for text search matched words ([BM25](../index/bm25.md)) [1]. In these years a language model became a part of search. As a ranker, BERT lifted the MS MARCO passage-ranking score (MRR@10, development set) from 0.167 for BM25 and 0.278 for the best earlier neural model to 0.365 in January 2019 [1]. As a reader, a model was given a retriever and a text index, so knowledge sat beside its weights [2]. In the knowledge-graph field the term became industry practice and three reviews took stock [9][10][11]. *Reading:* where knowledge lives, in weights, in text or in a graph, became an open design choice.

## The threads

### KB/KG

- **Industry graphs.** Noy et al. (CACM 62(8), 2019) compare the knowledge graphs at Microsoft (Bing), Google, Facebook, eBay and IBM [12]. Hogan et al. sum up the trends: many sources, often text; millions or billions of nodes and edges [9]. Hitzler notes "no published formal evaluation of their benefits" [11]. See [knowledge graph](../index/knowledge-graph.md), [Google Knowledge Graph](../index/google-knowledge-graph.md) and [Wikidata](../index/wikidata.md).
- **Three reviews.** Hogan et al. (arXiv 20200304; ACM Computing Surveys 2021) call the definition "contentious" and adopt an inclusive one [2][9]. Gutierrez and Sequeda (CACM, March 2021) call it "an evolving project and a vision" [10]. Hitzler's review of the field says it "most needs ... consolidation" [11].
- **Moving.** Language models as a source of knowledge-base content (Petroni et al. 20190903 [2]; COMET 20190612, which targets ATOMIC and [ConceptNet](../index/conceptnet.md) [3]). See [trends](../trends/README.md).

### Ontologies and the semantic web

- **JSON-LD 1.1** became a W3C Recommendation on 16 July 2020 [14]. It is a JSON serialization of [Linked Data](../index/linked-data.md). See [JSON-LD](../index/json-ld.md).
- **Standing.** Hitzler (2020) says the field's "grand goal" has "not been achieved yet" [11]. No other standard of 2018-2022 appears in the pages read.
- **Moving.** RDF 1.2, SPARQL 1.2 and SHACL 1.2 are W3C drafts of 2026, not yet Recommendations [15][16][17]. See [trends](../trends/README.md).

### Databases and search

- **BERT replaced earlier neural ranking.** Nogueira and Cho (arXiv 20190113) report the top MS MARCO entry, 27% relative better in MRR@10 than the earlier best (first-party) [2]; the leaderboard lists it on 20190107 [1]. See [BERT](../index/bert.md) and [reranking](../index/reranking.md).
- **Dense retrieval.** Karpukhin et al. (20200410) report a dense retriever 9-19 points above Lucene-BM25 on top-20 passage accuracy (first-party) [2]. Whether this replaced BM25 is disputed below. See [dense retrieval](../index/dense-retrieval.md).
- **GQL.** The committee page records "GQL inaugurated as an official ISO project" in September 2019, after a manifesto of May 2018 [13]. The standard came in 2024: see the [next era](settled-since-2023.md).
- **Vector databases.** The Milvus repository, described by GitHub as a vector database, was created 20190916 [20]. When the category began is **unstated** in the sources read. See [trends](../trends/README.md).

### RAG and agent memory

- **REALM (20200210).** A retriever trained inside language-model pre-training, with masked language modelling as the learning signal; 4-16 points absolute gain on three open-domain QA benchmarks (first-party) [2].
- **RAG (20200522).** Lewis et al. join a pretrained seq2seq model (parametric memory) to a dense vector index of Wikipedia (non-parametric memory) read by a neural retriever, and set state of the art on three open-domain QA tasks (first-party) [2]. See [retrieval-augmented generation](../index/retrieval-augmented-generation.md).
- **RETRO (20211208).** A 2-trillion-token database, a frozen BERT retriever, results comparable to GPT-3 with 25 times fewer parameters (first-party) [3].
- **Moving.** ReAct (20221006) has a model interleave reasoning with actions that reach external sources such as knowledge bases (first-party) [22]. Agent memory has no event here: Hu et al. date works they now read as early agent memory to "Since 2023" [21]. See [trends](../trends/README.md).

## Dated events

| Date | Event | Thread | Source |
|---|---|---|---|
| 20181011 | BERT preprint (arXiv v1) | RAG and agent memory | [2] |
| 20190107 | BERT enters the MS MARCO passage leaderboard at 0.365 MRR@10 | Databases and search | [1] |
| 20190113 | Passage Re-ranking with BERT (arXiv v1) | Databases and search | [2] |
| 2019 | Noy et al., industry-scale knowledge graphs, CACM 62(8) | KB/KG | [12] |
| 201909 | GQL becomes an ISO project | Databases and search | [13] |
| 20200210 | REALM | RAG and agent memory | [2] |
| 20200304 | Hogan et al., Knowledge Graphs (arXiv v1) | KB/KG | [2][9] |
| 20200410 | Dense Passage Retrieval | Databases and search | [2] |
| 20200522 | Retrieval-Augmented Generation | RAG and agent memory | [2] |
| 20200716 | JSON-LD 1.1 Recommendation | Ontologies and the semantic web | [14] |
| 202103 | Gutierrez and Sequeda, CACM 64(3) | KB/KG | [10] |
| 20210417 | [BEIR](../benchmarks/beir.md) benchmark | Databases and search | [2] |
| 20211208 | RETRO | RAG and agent memory | [3] |
| 20221130 | ChatGPT announced | RAG and agent memory | [7] |

## Systems and projects

- [BERT](../index/bert.md), a [Transformer](../index/transformer.md) model [2]; research systems REALM, DPR, RAG [2] and RETRO [3].
- Industry knowledge graphs of five companies [12]; [Wikidata](../index/wikidata.md) [11].
- Repositories created in the era (creation date only): Milvus 20190916, LangChain 20221017, [LlamaIndex](../projects/llama-index.md) 20221102 [18][19][20].

## Ideas and disputes

**Did dense retrieval replace sparse?** *Yes:* Stonebraker and Pavlo say inverted-index search engines "have been supplanted in recent years" by similarity search on embeddings [5]; the DPR authors report a large gain over BM25 [2]. *No:* Lin et al. (2021) say BM25 "still provides the starting point of many text ranking approaches today" [1]; BEIR finds "BM25 is a robust baseline" and dense and sparse models "often underperform other approaches" in zero-shot tests (the benchmark's own authors) [2]; Gao et al. say sparse and dense embeddings "can benefit from each other by leveraging complementary relevance information" [4]; a 2026 survey lists hybrid sparse-plus-dense retrieval under Modular RAG [8]. No source read settles it.

**What is "naive RAG"?** Gao et al. (2024): documents split into chunks, encoded as vectors in a vector database, top k by semantic similarity [4]. Singh et al. (v4, 1 April 2026): keyword retrieval with TF-IDF and BM25, with DPR under Advanced RAG [8]. The same word names different technology.

**Is a knowledge graph new?** *Reframing:* "mostly a new framing of ideas coming rather directly out of the Semantic Web field" [11]; "a reincarnation of the Semantic Web, and Linked Data" [10]. *Not stated:* Hogan et al. treat Google's 2012 announcement as the moment the phrase was adopted [9]; the passages read do not say whether the idea is new.

**Weights or index?** Petroni et al.: language models "require no schema engineering" and are "easy to extend to more data" [2]. REALM: knowledge in parameters is stored implicitly, "requiring ever-larger networks" [2]. RAG: access is "still limited"; provenance and updating remain "open research problems" [2]. Unresolved; see [trends](../trends/README.md).

## Papers and standards

See the [papers chapter](../papers/README.md).

- BERT, Devlin et al., arXiv 1810.04805 (2018) [2].
- Passage Re-ranking with BERT, Nogueira and Cho, arXiv 1901.04085 (2019) [2].
- Language Models as Knowledge Bases?, Petroni et al., arXiv 1909.01066 (2019) [2].
- REALM, Guu et al., arXiv 2002.08909 (2020) [2].
- Knowledge Graphs, Hogan et al., arXiv 2003.02320 (2020; ACM Computing Surveys 2021) [9].
- Dense Passage Retrieval, Karpukhin et al., arXiv 2004.04906 (2020) [2].
- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, Lewis et al., arXiv 2005.11401 (2020) [2].
- BEIR, Thakur et al., arXiv 2104.08663 (2021) [2].
- Improving language models by retrieving from trillions of tokens (RETRO), Borgeaud et al., arXiv 2112.04426 (2021) [3].
- Standard: JSON-LD 1.1, W3C Recommendation, 20200716 [14].

## Left unsolved

- **Graphs are costly to build and keep current,** and models lack reliable access to facts. Pan et al. (2023) say knowledge graphs are "difficult to construct and evolve by nature", while language models "often fall short of capturing and accessing factual knowledge" [6].
- **Provenance and updating** of knowledge in model weights were open problems in the RAG paper [2].
- **What a graph adds to retrieval**, and what separates retrieval from memory: see the [trends chapter](../trends/README.md). Hu et al. call agent memory "increasingly fragmented" [21].

The next era, [What has settled since 2023](settled-since-2023.md), records what became standard or common practice after ChatGPT.

## Sources

1. https://arxiv.org/pdf/2010.06467 : Lin, Nogueira, Yates, v3 (19 Aug 2021): BERT October 2018, the January 2019 MS MARCO table, TREC 2019 "two eras", BM25 as starting point; Table 1 dates the leaderboard entries January 2nd and January 7th, 2019 (read 20261102 19:55 UTC; Table 1 and the BERT sentence re-read 20261102 20:10 UTC)
2. http://export.arxiv.org/api/query?id_list=1810.04805,1901.04085,2002.08909,2004.04906,2005.11401,2003.02320,1909.01066,2104.08663 : one entry per id, v1 dates and abstracts: 1810.04805 BERT (20181011); 1901.04085 Passage Re-ranking with BERT (20190113); 2002.08909 REALM (20200210); 2004.04906 DPR (20200410); 2005.11401 RAG (20200522; "still limited" and "open research problems" re-read 20261102 20:10 UTC); 2003.02320 Hogan et al. (20200304); 1909.01066 Petroni et al. (20190903); 2104.08663 BEIR (20210417) (read 20261102 19:55 UTC)
3. http://export.arxiv.org/api/query?id_list=2010.06467,2312.10997,2306.08302,2210.03629,1906.05317,2112.04426,1706.03762 : one entry per id: 1906.05317 COMET (20190612); 2112.04426 RETRO (20211208); 2210.03629 ReAct (20221006); 1706.03762 Transformer (20170612, re-read 20261102 20:10 UTC); the surveys 2010.06467, 2312.10997, 2306.08302 (read 20261102 19:56 UTC)
4. https://arxiv.org/pdf/2312.10997 : Gao et al., v5 (27 Mar 2024): inception with the Transformer, ChatGPT "pivotal moment", Naive RAG, sparse and dense embeddings as complementary (read 20261102 19:55 UTC; quotes re-read 20261102 20:11 UTC)
5. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo: "late 2022", "supplanted" (read 20261102 19:55 UTC)
6. https://arxiv.org/pdf/2306.08302 : Pan et al., v3 (25 Jan 2024): REALM and RAG in the method table; the stated need, "difficult to construct and evolve by nature" (read 20261102 19:58 UTC; quotes re-read 20261102 20:11 UTC)
7. https://web.archive.org/web/20221130190000/https://openai.com/blog/chatgpt/ : OpenAI, "ChatGPT: Optimizing Language Models for Dialogue", dated "November 30, 2022" (archived copy; the live page returned HTTP 403) (read 20261102 19:56 UTC)
8. https://arxiv.org/pdf/2501.09136 : Singh et al., v4 (1 Apr 2026): Naive RAG as keyword retrieval; Table 1 (read 20261102 19:58 UTC)
9. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., v6 (11 Sep 2021): "contentious", inclusive definition, Noy et al. trends, 2012 "watershed" (read 20261102 19:55 UTC)
10. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, CACM, March 2021 (read 20261102 19:55 UTC)
11. https://par.nsf.gov/servlets/purl/10292869 : Hitzler, author's version accepted April 2020 (read 20261102 19:55 UTC)
12. https://research.google/pubs/industry-scale-knowledge-graphs-lessons-and-challenges/ : Noy et al., CACM 62(8), 2019, abstract (read 20261102 19:58 UTC)
13. https://www.gqlstandards.org/ : GQL committee page: September 2019 ISO project; manifesto May 2018; the committee's announcement of publication, 17 April 2024 (ISO's own publication date is 2024-04-12: see [What has settled since 2023](settled-since-2023.md)) (read 20261102 19:56 UTC)
14. https://www.w3.org/TR/json-ld11/ : JSON-LD 1.1, Recommendation 16 July 2020; previous Recommendation 16 January 2014 (read 20261102 19:56 UTC)
15. https://www.w3.org/TR/rdf12-concepts/ : RDF 1.2, a Candidate Recommendation Snapshot of 07 April 2026 when read, not a Recommendation (read 20261102 20:11 UTC)
16. https://www.w3.org/TR/sparql12-query/ : SPARQL 1.2, a Working Draft of 01 November 2026 when read (read 20261102 20:11 UTC)
17. https://www.w3.org/TR/shacl12-core/ : SHACL 1.2 Core, a Working Draft of 02 November 2026 when read (read 20261102 20:11 UTC)
18. https://api.github.com/repos/run-llama/llama_index : created_at 2022-11-02 (read 20261102 19:56 UTC); and the archive page [LLM era](../../kb-kg/llm-era/README.md), whose phase 1 runs 20200522 to 20221231 and whose boundaries are "the author's judgement" (read 20261102 19:54 UTC; re-read 20261102 20:11 UTC)
19. https://api.github.com/repos/langchain-ai/langchain : created_at 2022-10-17 (read 20261102 19:56 UTC)
20. https://api.github.com/repos/milvus-io/milvus : created_at 2019-09-16 (read 20261102 19:56 UTC)
21. https://arxiv.org/pdf/2512.13564 : Hu et al., v2 (13 Jan 2026): "Since 2023", "increasingly fragmented" (read 20261102 19:58 UTC)
22. https://arxiv.org/abs/2210.03629 : ReAct, submitted 6 Oct 2022 (v1); abstract: reasoning traces and actions interleaved, actions interface with external sources such as knowledge bases (read 20261102 20:12 UTC)
