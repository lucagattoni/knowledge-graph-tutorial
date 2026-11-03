---
type: era
period: 2023-present
order: 8
updated: 20261103 01:52 UTC
---

# What has settled since 2023 (2023-present)

This page answers one question: of everything that happened after ChatGPT, what has already become a standard, been absorbed into common practice, or been replaced? The answer is short: two graph-query standards ([SQL/PGQ](../index/sql-pgq.md) and [GQL](../index/gql.md)) and two W3C Recommendations of 2024. [Retrieval-augmented generation](../index/retrieval-augmented-generation.md) does not qualify on the sources read: one survey calls it widely adopted, which is evidence of adoption and not of a standard or a successor. Everything else is named in one line and left to [the trends chapter](../trends/README.md).

## Dates and boundaries

**Start.** The previous era, [language models meet retrieval](language-models-meet-retrieval.md), ends with ChatGPT. OpenAI's announcement is dated 30 November 2022 [1]. A survey of retrieval-augmented generation calls ChatGPT's arrival "a pivotal moment" [6], and a database history dates the mainstream turn to "late 2022" [4]. This page starts at 2023 for a practical reason: the first settled item is dated 2023 (SQL/PGQ, June) [3]. No event of December 2022 is cited here.

**End.** There is none. "Present" means 20261102, the day this page was read. When a trend in chapter 2 settles, it moves here with a dated change row.

**Whose periodisation.** No source read gives phases for this period. The RAG surveys name paradigms without dates [6][7]. The archive's own seven phases are, in its words, "the author's judgement" [17]. The boundaries on this page are this documentation's, built from points that at least two sources share (ChatGPT as turning point: [4][6]).

## What changed

Two things settled. In databases, graph querying reached ISO publication twice (2023, 2024) [3][2]. In the semantic web, W3C published two Recommendations in 2024, RDF Dataset Canonicalization and DCAT 3 [18][19]. In retrieval and agent memory nothing has settled on the sources read: the newer layers (graph-based retrieval, agent memory, protocols) are described by their own surveys as fragmented [7][8], and the one adoption claim is told as evidence only, under RAG below [6]. Vector indexes in relational systems are reported by one source only [4]; they are discussed under disputes and in Left unsolved, not counted here. *Reading:* what settled is plumbing, namely query languages, a canonical form for RDF datasets and a catalogue vocabulary; what is not settled is how a model should use a knowledge base.

## The threads

### Knowledge bases and knowledge graphs

Nothing in the main thread has settled in this era, in the sources read. Two papers frame the work as open: a 2023 roadmap (arXiv v1 20230614) that calls itself "forward-looking" in its abstract, for combining [knowledge graphs](../index/knowledge-graph.md) with [large language models](../index/large-language-model.md) [16], and the memory survey below [8]. Still moving: see [trends](../trends/README.md).

### Ontologies and the semantic web

The three core specifications still stand at their earlier versions: RDF 1.1 (20140225), SPARQL 1.1 (20130321) and SHACL (20170720) are the latest Recommendations [13][14][15]. Two other W3C Recommendations were published in this era, both in 2024:

- **RDF Dataset Canonicalization**, Recommendation of 20240521 [18]. It defines an algorithm (RDFC-1.0) that turns an RDF dataset into a canonical form, so that datasets can be compared, signed or hashed. It is based on the RDF 1.1 definition [18]. See [RDF Dataset Canonicalization](../index/rdf-dataset-canonicalization.md).
- **DCAT 3**, Recommendation of 20240822 [19]. It is an RDF vocabulary for describing datasets and data services in catalogues. It adds terms for versioning, dataset series and inverse properties without breaking the definitions of DCAT 2 [19]. See [DCAT](../index/dcat.md).

Other W3C Recommendations of 2023 onwards: **unstated**; the W3C list was not surveyed. Updates are under way and are not settled: RDF 1.2 is a Candidate Recommendation Snapshot of 20260407, SPARQL 1.2 a Working Draft of 20261101, SHACL 1.2 Core a Working Draft of 20261102 [10][11][12]. Each draft page names the old version as the "Latest Recommendation". Links: [RDF](../index/rdf.md), [SPARQL](../index/sparql.md), [SHACL](../index/shacl.md). Still moving: see [Semantic web standards](../trends/semantic-web-standards.md).

### Databases and search

This thread holds most of what settled.

- **SQL/PGQ.** ISO/IEC 9075-16:2023, "Property Graph Queries (SQL/PGQ)", edition 1, is listed as published in June 2023; a corrigendum (Cor 1:2026) is published and a successor is in development [3]. A database history says SQL:2023 "introduced" property graph queries in a relational system [4]. See [SQL](../index/sql.md) and [SQL/PGQ](../index/sql-pgq.md).
- **GQL.** ISO's lifecycle table for ISO/IEC 39075:2024 lists stage 60.60, International Standard published ("Norma Internacional publicada" on the Spanish-language page), on 2024-04-12, and the IEC web store gives the same publication date [21][22]. The GQL committee announced the publication on 17 April 2024: the standard "is officially published" [2]. The JTC 1 news item is dated 18 April [23]; openCypher says "published (April 11, 2024)" [24]. See the disputes table. GQL and SQL/PGQ share their graph pattern matching language. In the entry of 20230516 the committee says it worked "to keep GPM in GQL as identical as possible to GPM in SQL/PGQ" (GPM is the graph pattern matching language). In the entry of 20231004 it says GQL must have "the same semantics as SQL/PGQ:2023" on the shared subset [2]. Whether the published texts match: **unstated**. See [GQL](../index/gql.md) and [property graphs](../index/property-graph.md). iso.org itself answered HTTP 403, so the ISO catalogue page was read at the committee.iso.org address [21]. Adoption by products is **unstated**.
- **Vector indexes in relational systems (not settled here).** One source says that within a year of ChatGPT several relational systems added vector indexes, and that in 2023 Oracle, SingleStore, Rockset and ClickHouse did so [4]. I did not read the vendors' pages. The same source calls such indexes "a feature, not the foundation of a new system architecture" [4]. This is one stance, so it is listed under disputes and in Left unsolved, not as settled, and it is not in the dated events. See [vector search](../index/vector-search.md).

### RAG and agent memory

- **Not settled: see chapter 2.** [RAG](../index/retrieval-augmented-generation.md) and [agent memory](../index/agent-memory.md) are still moving; they are told in [graph-based RAG](../trends/graph-based-rag.md) and [agent memory](../trends/agent-memory.md). Evidence of adoption only: one survey (arXiv v5, 20240327) says RAG's integration into language models "has resulted in widespread adoption" [6]. The sentence is about RAG as a whole, it is not in version 1 of the survey [20], and a second source for it is **unstated**. RAG has not become a standard, and it has not been replaced: an agentic-RAG survey says agentic RAG "should not be viewed as a universal replacement" for traditional RAG [7].

## Dated events

| Date | Event | Thread | Source |
|---|---|---|---|
| 20221130 | OpenAI announces ChatGPT as a research preview (closes the previous era) | RAG and memory | [1] |
| 202306 | ISO/IEC 9075-16:2023 (SQL/PGQ) published | Databases and search | [3] |
| 20240412 | ISO/IEC 39075:2024 (GQL) published (ISO lifecycle stage 60.60; the IEC web store gives the same publication date) | Databases and search | [21][22] |
| 20240417 | The GQL committee announces the publication | Databases and search | [2] |
| 20240521 | RDF Dataset Canonicalization becomes a W3C Recommendation | Ontologies and semantic web | [18] |
| 20240822 | DCAT 3 becomes a W3C Recommendation | Ontologies and semantic web | [19] |
| 2026 | Corrigendum Cor 1:2026 to SQL/PGQ published (day **unstated**) | Databases and search | [3] |

## Systems and projects

No project of this era has settled in the sense used here. The standards above are what settled. The syntaxes SQL/PGQ builds on come from Neo4j's Cypher, Oracle's PGQL and TigerGraph's GSQL [4]; see [neo4j](../projects/neo4j.md). Per the same source, SQL/PGQ in DuckDB outperforms a leading graph database by up to ten times [4]. That is a claim from one paper about one comparison.

## Ideas and disputes

Each dispute is shown both ways.

| Question | One side | Other side |
|---|---|---|
| Do specialised graph databases survive? | "We do not expect specialized graph DBMSs to be a large market"; relational systems will add graph APIs [4]. | A 2008 survey: graph models "took off", "died out", and the need for graph data "has reestablished" their relevance [9]. GQL is a standard written for such systems [2]. |
| When was GQL published? | ISO's lifecycle table and the IEC web store: 2024-04-12 [21][22]. | The committee's announcement: 17 April [2]; the JTC 1 news item: 18 April [23]; openCypher: 11 April, with no source given for it [24]. *Reading:* ISO's record is the publication; the committee's own entry of 29 March said it had no official publication date yet [2], so 17 April is its announcement. What the openCypher date marks is **unstated**. |
| Did dense retrieval replace sparse? | Inverted-index search "supplanted in recent years" by embeddings [4]. | BM25 "still provides the starting point of many text ranking approaches" (2021) [5]; Modular RAG combines sparse and dense retrieval [7]. Source [5] is older than [4], so it cannot answer it; [7] is the later source. |
| Will vector databases be absorbed? | They are a feature of relational systems [4]. | No second source read forecasts this. Independent evidence: **unstated**. |

## Papers and standards

See [the papers chapter](../papers/README.md).

- Stonebraker and Pavlo, "What Goes Around Comes Around... And Around...", SIGMOD Record 53(2), 2024: data models since 1970, with vector and graph systems [4].
- Gao et al., RAG survey, arXiv 2312.10997 (v1 20231218; wording of "widespread adoption" read in v5, 20240327): evidence of adoption, not a standard [20][6][16].
- Pan et al., "Unifying Large Language Models and Knowledge Graphs: A Roadmap", arXiv 2306.08302 (v1 20230614; listing and abstract read, full text not) [16].
- Singh et al., Agentic RAG survey, arXiv 2501.09136 (v1 20250115; read in v4, 20260401) [7][16].
- Hu et al., "Memory in the Age of AI Agents", arXiv 2512.13564 (v1 20251215; read in v2, 20260113) [8][16].
- ISO/IEC 9075-16:2023 (SQL/PGQ) [3]; ISO/IEC 39075:2024 (GQL) [2].
- W3C Recommendations: RDF Dataset Canonicalization (20240521) [18]; DCAT 3 (20240822) [19].

## Left unsolved

- **Adoption.** A published standard shows that a standard exists, not that products use it. GQL's uptake is **unstated** in the sources read.
- **The stack's update.** RDF 1.2, SPARQL 1.2 and SHACL 1.2 are drafts; the sources give no rule for a standard with a newer draft. They are told in [Semantic web standards](../trends/semantic-web-standards.md).
- **Evidence.** The vector-index claim rests on one paper. Independent checks are still to be done.

These lead into [the trends](../trends/README.md). The previous era is [language models meet retrieval](language-models-meet-retrieval.md). Earlier pages of this chapter: [the semantic web](semantic-web.md) and [knowledge graphs at scale](knowledge-graphs-at-scale.md).

## Sources

1. https://web.archive.org/web/20221130180000/https://openai.com/blog/chatgpt : OpenAI, "ChatGPT: Optimizing Language Models for Dialogue", dated 30 November 2022, research preview; read as the Internet Archive copy captured 20221130 18:09 because openai.com returned HTTP 403 (read 20261102 19:55 UTC).
2. https://www.gqlstandards.org/ : GQL committee page, entry of 17 April 2024 "The GQL Standard is published", ISO/IEC 39075:2024 (entries of 17 April and 29 March 2024 re-read 20261102 22:52 UTC); entry of 16 May 2023 ("as identical as possible" for graph pattern matching); entry of 4 October 2023 ("the same semantics as SQL/PGQ:2023" on the shared subset) (read 20261102 19:55 UTC; the two 2023 entries re-read 20261102 20:07 UTC).
3. https://committee.iso.org/es/sites/isoorg/contents/data/standard/07/94/79473.html : ISO/IEC 9075-16:2023, edition 1, published 2023-06, Cor 1:2026 published, successor in development (WebFetch extraction of a Spanish-language ISO page; read 20261102 19:56 UTC).
4. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), 2024; SQL/PGQ, graph DBMS, vector indexes, text search, "late 2022" (read 20261102 19:56 UTC).
5. https://arxiv.org/pdf/2010.06467v3 : Lin, Nogueira, Yates (2021), BM25 "starting point" (read 20261102 19:57 UTC).
6. https://arxiv.org/pdf/2312.10997v5 : Gao et al., RAG survey, version 5 (updated 20240327); "pivotal moment", Naive RAG, "widespread adoption" (stated for RAG as a whole), long-context discussion (read 20261102 19:56 UTC; "widespread adoption" and long-context passages re-read 20261102 20:07 UTC).
7. https://arxiv.org/pdf/2501.09136v4 : Singh et al., version 4 (updated 20260401) of a paper first published 20250115; Naive RAG as keyword retrieval, "remains fragmented", "universal replacement", hybrid retrieval, the five paradigms of its Table 1 (read 20261102 19:56 UTC; re-read 20261102 20:08 UTC).
8. https://arxiv.org/pdf/2512.13564 : Hu et al., v2; "increasingly fragmented", boundary with RAG "increasingly blurred" (read 20261102 19:56 UTC).
9. https://users.dcc.uchile.cl/~cgutierr/papers/surveyGDB.pdf : Angles and Gutierrez (2008), abstract on graph database models (read 20261102 19:57 UTC).
10. https://www.w3.org/TR/rdf12-concepts/ : RDF 1.2 Concepts, Candidate Recommendation Snapshot 07 April 2026 (read 20261102 19:56 UTC).
11. https://www.w3.org/TR/sparql12-query/ : SPARQL 1.2 Query, Working Draft 01 November 2026 (read 20261102 19:56 UTC).
12. https://www.w3.org/TR/shacl12-core/ : SHACL 1.2 Core, Working Draft 02 November 2026 (read 20261102 19:56 UTC).
13. https://www.w3.org/TR/rdf11-concepts/ : RDF 1.1 Concepts, Recommendation 25 February 2014 (read 20261102 19:56 UTC).
14. https://www.w3.org/TR/sparql11-query/ : SPARQL 1.1 Query, Recommendation 21 March 2013 (read 20261102 19:56 UTC).
15. https://www.w3.org/TR/shacl/ : SHACL, Recommendation 20 July 2017 (read 20261102 19:56 UTC).
16. http://export.arxiv.org/api/query?id_list=2312.10997,2306.08302,2501.09136,2512.13564 : arXiv records, version-1 dates 20231218, 20230614, 20250115, 20251215; Gao et al. latest version v5 (20240327), Singh et al. latest v4 (20260401); the abstract of Pan et al. (the "forward-looking roadmap" wording) (read 20261102 19:56 UTC; Gao, Singh and Pan records re-read 20261102 20:08 UTC).
17. ../../kb-kg/llm-era/README.md : the archive page; its line 22 says the phase boundaries "are the author's judgement" (read 20261102 19:55 UTC).
18. https://www.w3.org/TR/rdf-canon/ : RDF Dataset Canonicalization, W3C Recommendation 21 May 2024; abstract; algorithm RDFC-1.0; based on the RDF 1.1 definition (read 20261102 20:07 UTC; the date re-read in the page's own metadata, publishDate 2024-05-21, 20261102 22:57 UTC).
19. https://www.w3.org/TR/vocab-dcat-3/ : Data Catalog Vocabulary (DCAT) Version 3, W3C Recommendation 22 August 2024; abstract; new features (versioning, dataset series, inverse properties); previous terms not broken (read 20261102 20:07 UTC; the date re-read in the page's own metadata, publishDate 2024-08-22, 20261102 22:57 UTC).
20. https://arxiv.org/pdf/2312.10997v1 : Gao et al., version 1 (published 20231218), full text searched: names Naive, Advanced and Modular RAG; the "widespread adoption, establishing RAG as a key technology" sentence and the long-context section are not in it (read 20261102 20:07 UTC).
21. https://committee.iso.org/es/sites/isoorg/contents/data/standard/07/61/76120.html : ISO catalogue page for ISO/IEC 39075:2024 (Spanish-language page; iso.org itself answered HTTP 403): edition 1, 2024-04; lifecycle table, stage 60.60 "Norma Internacional publicada" on 2024-04-12; Cor 1:2026 published; ISO/IEC CD 39075 in development (read 20261102 22:52 UTC)
22. https://webstore.iec.ch/publication/94107 : IEC web store, ISO/IEC 39075:2024, edition 1.0, publication date 2024-04-12, 610 pages (read 20261102 22:52 UTC)
23. https://jtc1info.org/slug/gql-database-language/ : JTC 1 news item "GQL Database Language", dated April 18, 2024, on the publication of ISO/IEC 39075:2024 (read 20261102 22:52 UTC)
24. https://opencypher.org/ : openCypher site (first-party for openCypher): "ISO/IEC 39075 GQL published (April 11, 2024)", GQL "a key inspiration" (read 20261102 22:52 UTC)
