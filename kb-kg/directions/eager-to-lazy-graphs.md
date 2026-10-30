# From eager LLM-built graphs to cheaper ones

**In one paragraph.** Building a knowledge graph with an LLM at index time costs tokens in proportion to the corpus, and again when the corpus changes. Projects in this repository try five ways to cut that cost: smaller or cheaper models, fewer calls per chunk, work moved to query time, no LLM at index time, and structure taken from the text by non-generative tools. Nearly every cost and quality figure is the authors' own, usually on corpora of about 6,000 to 12,000 passages. The few outside measurements read here show a reranked vector baseline ahead on fact lookup. The cost problem is confirmed; whether a cheaper graph pays for itself depends on the question type, and no study compares the five routes on one corpus.

## What the direction claims

The problem. A GraphRAG-style index has an LLM read every chunk, extract entities and relations, and then summarise them. The cost scales with the corpus and recurs on change ([literature](../literature/graph-rag-research.md), sections 1 and 2.1). Microsoft's documentation puts graph extraction at roughly 75% of its indexing cost; that is the project's own estimate and the method is not given ([microsoft-graphrag](../projects/microsoft-graphrag.md)).

The five levers, as the projects state them:

1. **Smaller or cheaper models:** MiniRAG, LightRAG, nano-graphrag.
2. **Fewer calls:** one extraction call per chunk, no community reports (fast-graphrag, Youtu-GraphRAG, LightRAG, HippoRAG).
3. **Query time:** defer summarising, or build only the structure a question needs (LazyGraphRAG, LogicRAG, Graph-R1).
4. **No LLM at index:** a graph from named-entity recognition (LinearRAG), document metadata (datastax-graph-rag) or noun phrases (GraphRAG's Fast method).
5. **Structure from the text or a schema:** small extractors and schemas (GLiNER, DeepKE, OntoGPT, GraphRAG SDK, TrustGraph).

## Who is doing it

| Project | How it takes this direction | Status at 20261030 | Evidence it works (and who measured it) |
|---|---|---|---|
| [Microsoft GraphRAG](../projects/microsoft-graphrag.md) | Eager baseline: 2 extraction calls per chunk at defaults, then community reports. Levers: Fast method (noun-phrase graph, no extraction calls, one report call per community), dynamic community selection. LazyGraphRAG (index cost like vector RAG) is not in the open-source tree. | Active; README says "largely in maintenance mode" since 20260814; v3.3.0; MIT | Microsoft's blog (no code or paper): LazyGraphRAG index cost 0.1% of GraphRAG, over 700 times lower query cost. Dynamic selection: 77% fewer tokens on average at one level, 50 questions, authors. Docs call the Fast graph "quite a bit noisier". No outside evaluation read. |
| [LightRAG](../projects/lightrag.md) | Fewer calls: no communities or summaries; 1 extraction call plus up to 1 gleaning call per chunk; separate extraction model since May 2026. Always built eagerly. | Active; v1.5.7 20260902; MIT | Authors' README: overall win share against GraphRAG 49.6% to 54.8% (LLM judge, UltraDomain). The entry found no published cost measurement; others measured it (below). |
| [nano-graphrag](../projects/nano-graphrag.md) | Small GraphRAG reimplementation with cheap and best model slots. | Quiet; last push 20260127; MIT | Project, one book: indexing over 5 minutes with the official code, under 4 with this one. |
| [fast-graphrag](../projects/fast-graphrag.md) | Fewer calls: 1 extraction call per chunk, entities-only embeddings, Personalized PageRank at query time, no communities. | No push since 20251101; entry: "does not look maintained"; MIT | Vendor README: $0.08 against $0.48, "6x"; model, data and counting unstated. GraphRAG-Bench authors: 251,817 tokens against 654,673 for GraphRAG on one book (entry's arithmetic: 2.6x) and fact-retrieval accuracy below a reranked vector baseline. |
| [HippoRAG](../projects/hipporag.md) | Fewer calls: one LLM extraction pass, Personalized PageRank at query time, one small filter call per query. | Active; last push 20261006; only release v1.0.0; package 2.0.0a5; MIT | Authors, MuSiQue (11,656 passages): 9.2M input tokens against 68.5M (LightRAG) and 115.5M (GraphRAG); RAPTOR 1.7M. |
| [MiniRAG](../projects/minirag.md) | Smaller models: 1.5B to 4B models build the index; chunk nodes beside entity nodes. | Quiet; last push 20251016; MIT | Authors, own benchmark: 25% of LightRAG's storage, accuracy loss "0.8% to 20%" from LLM to small model. Its own Table 1 has LightRAG ahead with gpt-4o-mini. No outside evaluation. |
| [Youtu-GraphRAG](../projects/youtu-graphrag.md) | Fewer calls: one combined extraction call per chunk, a declared schema bounds extraction. | Quiet; last push 20260226; custom licence, academic use only (README badge says MIT) | Authors: abstract "up to 90.71%" token saving, README "33.6%", baseline unstated. One user reports schema growth from 10 to 523 node types. |
| [LogicRAG](../projects/logicrag.md) | Query time: no graph; sub-questions and their dependencies built per question. | Quiet; last push 20260719; GPL-3.0 | Authors: best on 5 of 6 accuracy columns; 1,777.9 tokens per question against 489.7 for plain retrieval (3.6 times). No outside evaluation found. |
| [Graph-R1](../projects/graph-r1.md) | Query time: a small model trained by reinforcement learning traverses a hypergraph; build is one GPT-4o-mini pass. | Quiet; last push 20260430; no release; no trained weights offered; MIT | Authors: average F1 57.82 against 46.19 (Search-R1), 128 test items per set; query spend "$0 per 1K queries", hardware unstated. |
| [datastax-graph-rag](../projects/datastax-graph-rag.md) | No LLM at index: edges from metadata over an existing vector store. | Quiet; last push 20250505; Apache-2.0 | Authors' notebook: a "$70k" estimate for an LLM graph build; no method given; one-question comparison. No benchmark. |
| [LinearRAG](../projects/linearrag.md) | No LLM at index: NER plus embeddings; relations stay in passage text. | Quiet; last push 20260705; GPL-3.0 | Authors: 0 index tokens; 249.78 s against 4,933.22 s for LightRAG on 2Wiki. Issue #25 (open): an outside user reports lower scores on original passage splits (their figures, unreproduced). |
| [KAG](../projects/kag.md) | LLM builder, schema-free or schema-constrained. Cost lever: unstated. | Quiet; last push 20260128; Apache-2.0 | README gives no numbers. |
| [RAG-Anything](../projects/rag-anything.md) | Eager, multimodal, on LightRAG. | Active; v1.4.4; MIT | A user report of about 24 LLM calls per image block, not measured. |
| [Hyper-Extract](../projects/hyper-extract.md) | One tool offering an embed-only baseline and graph methods; graph methods pay extraction at ingest. | Active; v0.11.0; alpha classifier | No benchmark; docs call method choice "a decision aid, not an evaluation framework". |
| [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md) | Eager LLM builder, in the `experimental` namespace. | Active; 1.23.0; Apache-2.0 | None in the README. |
| [GraphRAG SDK](../projects/graphrag-sdk.md) | Text first: local GLiNER model is the default first step; an LLM verifies entities and extracts relations. | Active; v1.5.0; Apache-2.0 | Project's own run: 71.48 overall on GraphRAG-Bench against 55.39 for reranked vector RAG; rows not checkable by the entry. |
| [Neo4j LLM Knowledge Graph Builder](../projects/llm-graph-builder.md) | Eager: one LangChain extraction request per chunk group. | App banner: "no longer actively developed" (merged 20261016); Labs project; Apache-2.0 | Project RAGAS notebook, one PDF, 12 to 15 questions per mode; the entry says the better modes cannot be told apart by it. |
| [TrustGraph](../projects/trustgraph.md) | Eager; an ontology mode picks the relevant ontology part per chunk to guide extraction. | Active; 2.11.1 on PyPI; Apache-2.0 | Ingest speed only: 1,549,890 tokens in 8.5 minutes on eight Gaudi 2 cards, 289.3 minutes on CPU. No answer-quality test. |
| [M-flow](../projects/m-flow.md) | Eager: LLM builds the graph at memorise time; calls per document unstated. | Last push 20260901; Apache-2.0 | Own: 81.8% on LoCoMo-10 against 79.4% for Cognee Cloud. No outside evaluation. |
| [AI Powered Knowledge Graph Generator](../projects/ai-knowledge-graph.md) | Eager, small: LLM triples per chunk, no database; rule-based inferred edges off by default (about 70% of edges in testing). | Bursty; v0.8.0 20260912; Apache-2.0 | No benchmark. |
| [OntoGPT](../projects/ontogpt.md) | Schema-guided: LinkML schema, one class per prompt, ontology grounding. | Active; v1.2.0; BSD-3-Clause | Paper (2024): 98 of 100 GO terms grounded against 3 without it; cost unstated. |
| [GLiNER](../projects/gliner.md) | Small non-generative entity model, labels given at run time. | Active; v0.2.29; Apache-2.0 | Authors: zero-shot average F1 52.7 to 60.9 against 47.5 for ChatGPT; entities, not graphs. |
| [DeepKE](../projects/deepke.md) | Trained supervised extraction models; LLMs only in one example folder. | Quiet; one commit in 2026; last release 2.2.7 (20230921); MIT | No figures in the README; no outside evaluation read. |

## Evidence for

- **Index tokens fall.** HippoRAG 2 authors: GraphRAG input tokens 12.5 times theirs on MuSiQue. G3RAG authors (arXiv 2609.19622, via the [literature page](../literature/graph-rag-research.md), section 3): 86.80M construction tokens for LightRAG, 14.47M for HippoRAG 2, zero for their vector-geometry graph. EffiRAG authors (arXiv 2609.18099, same page): total cost 57.1% below LightRAG-hybrid.
- **Quality held in the authors' tests.** LinearRAG beat HippoRAG 2 on four datasets ([linearrag](../projects/linearrag.md)). G3RAG averaged F1 66.49 against 64.49 for HippoRAG 2 and 60.62 for naive retrieval. EffiRAG was preferred to LightRAG-hybrid on 93 of 120 questions, lost 7, with 20 splits (LLM-generated questions, GPT-4o-mini judge).
- **Microsoft's own claim** that deferring work to query time gives vector-RAG index cost ([microsoft-graphrag](../projects/microsoft-graphrag.md)).
- **Reading:** the cost claims agree in direction across groups; the sizes differ (next section).

## Evidence against, or limits

- **Who measured.** Almost all of it is the authors' own, on baselines they ran themselves. The entries record no outside evaluation for MiniRAG, LogicRAG, Youtu-GraphRAG, Graph-R1 or datastax-graph-rag, and for LinearRAG only an issue thread.
- **Size of the saving varies by measurement.** GraphRAG's input tokens are 12.5 times HippoRAG 2's in HippoRAG 2's paper. In GraphRAG-Bench's one-book run, GraphRAG used 654,673 tokens against 329,993 for HippoRAG 2, about 2.0 times (my arithmetic; different corpus, model and settings). The ledger could not verify the "10 times" efficiency figure for HippoRAG 2, and this page does not use it. The only dollar estimate the literature page found is an order-of-magnitude one (about $10,000 per 100,000 documents, assumptions stated in that paper); the figures from the July text are unverifiable (ledger V1, V2).
- **Cheaper graphs still use an LLM somewhere.** G3RAG without its LLM seed-filtering step averaged 60.53, level with naive retrieval (60.62). EffiRAG with non-LLM extraction won 44, lost 26, 50 splits, against 93, 7, 20 with LLM extraction.
- **Query-time work moves the cost.** LogicRAG used 3.6 times the tokens and 2.3 times the latency of plain retrieval per question. Graph-R1 needs training (4 x A100 reported) and offers no weights. LazyGraphRAG is not open source at v3.3.0.
- **A plain baseline is hard to beat on fact lookup.** GraphRAG-Bench: reranked vector retrieval led fast-graphrag on fact retrieval in both corpora. RAW-RAG (arXiv 2610.30755, no extraction, no graph) came first among 12 compared memory systems in 6 of 7 settings; conversation memory, not documents. EffiRAG's authors write that non-graph retrievers "may be more practical" under tight cost limits.
- **Reproducibility.** LinearRAG issue #25 (above). Graph-R1's text and table disagree (57.28 against 57.82). MiniRAG's summary claim differs from its Table 1. Youtu-GraphRAG's abstract and README give different savings.
- **Reuse limits.** LinearRAG and LogicRAG are GPL-3.0; Youtu-GraphRAG's licence is academic-only. Ten of the 23 entries are marked quiet (no push in 90 days or more), and the fast-graphrag entry says that project "does not look maintained".

## What is unresolved

- Does a cheaper graph beat a plain baseline per question type? The evidence splits by task, answer-prompt format and corpus; RAGU (via the literature page) shows prompt format alone can reverse a ranking.
- Scale. Most tests use 6,000 to 12,000 passages. G3RAG measured its sparse version to 100,000 documents for time only, not accuracy.
- Rebuild cost when documents change. LightRAG is incremental per document, GraphRAG has `update`; per-project update costs are unstated.
- Whether GraphRAG's Fast index equals the LazyGraphRAG index. The entry calls it an inference; no source states it.
- Whether small-model extraction holds up outside MiniRAG's own benchmark: unstated.
- Measured index cost is absent from most card entries (for example KAG, RAG-Anything, neo4j-graphrag-python, M-flow, OntoGPT, GLiNER, DeepKE, Hyper-Extract).

## Signals to watch

Each is checkable after 20261030.

1. A microsoft/graphrag release whose tree contains a LazyGraphRAG query engine (no path with "lazy" at v3.3.0), or a change to the README maintenance notice dated 20260814.
2. An independent evaluation of any of LinearRAG, LogicRAG, MiniRAG or Youtu-GraphRAG; or a reply closing LinearRAG issue #25.
3. A fast-graphrag commit or PyPI release after 20251101 and 0.0.5.
4. Graph-R1 trained weights (open issues #19, #22, #24).
5. A LightRAG release after v1.5.7, or any published LightRAG cost measurement.
6. Neo4j's Document Intelligence leaving preview; a llm-graph-builder release after v0.8.7 (20260723).
7. A leaderboard row naming FalkorDB's GraphRAG SDK on GraphRAG-Bench.
8. A replication of arXiv 2609.18099, 2609.19622 or 2610.30755 by other authors.
9. Datastax-graph-rag: the roadmap item "LazyGraphRAG on retrieved documents" shipping, or any commit after 20250505.

## Sources

Entries (read 20261030, last read 19:57 UTC): [microsoft-graphrag](../projects/microsoft-graphrag.md), [lightrag](../projects/lightrag.md), [fast-graphrag](../projects/fast-graphrag.md), [nano-graphrag](../projects/nano-graphrag.md), [hipporag](../projects/hipporag.md), [minirag](../projects/minirag.md), [linearrag](../projects/linearrag.md), [logicrag](../projects/logicrag.md), [youtu-graphrag](../projects/youtu-graphrag.md), [graph-r1](../projects/graph-r1.md), [datastax-graph-rag](../projects/datastax-graph-rag.md), [kag](../projects/kag.md), [rag-anything](../projects/rag-anything.md), [hyper-extract](../projects/hyper-extract.md), [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md), [graphrag-sdk](../projects/graphrag-sdk.md), [llm-graph-builder](../projects/llm-graph-builder.md), [trustgraph](../projects/trustgraph.md), [m-flow](../projects/m-flow.md), [ai-knowledge-graph](../projects/ai-knowledge-graph.md), [ontogpt](../projects/ontogpt.md), [gliner](../projects/gliner.md), [deepke](../projects/deepke.md).

Also: [what the research found](../literature/graph-rag-research.md) (its section 3 and verification ledger carry the arXiv 2609.18099, 2609.19622, 2610.30755 and 2607.11683 figures); [papers and benchmarks](../papers-benchmarks/README.md) for GraphRAG-Bench background.

No page outside the repository was fetched for this page. Every figure above is taken from the entries or the literature page, which name their own sources and read times.
