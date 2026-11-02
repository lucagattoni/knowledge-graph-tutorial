NOTE ON THE FILE. The harness refused my write of `findings.md` ("Subagents should return findings as text, not write report files"), and I did not work around it. The complete findings are in PART 2 below; save them as `step0-trends/findings.md` if you want the file. Raw data, scripts and downloads are on disk under <scratch folder>/step0-trends/ (scripts/, out/, arxiv1 to arxiv6/, dl-gh/, dl-web/). The repository was not touched.

=====================================================================
PART 1: SUMMARY (about 540 words)
=====================================================================

Window 20251102 to 20261102. Snapshot 20261030 19:54 (active = pushed within 90 days). arXiv counts are keyword hits, noisy; read times 20261102 19:26 to 19:47.

| # | Candidate | Active repos (top) | arXiv in window (prior year) | Preliminary status |
|---|---|---|---|---|
| 1 | Eager LLM-built KGs | 20 (LightRAG 40,443; GraphRAG 36,498) | 48 narrow (29); family 272 (167) | Passes both; settled evidence partial (GraphRAG README "maintenance mode" since 20260814; vendor SDKs) |
| 2 | Cheaper or lazy build | 2 (none states a cheaper build); 6 quiet | 32 (13) | Papers pass, snapshot fails; unclear; fold into 1 as one shift |
| 3 | Agentic/RL graph retrieval | 0 (7 quiet) | 44 (18) | Passes via papers only |
| 4 | Reasoning over structure | 2 (+2 E): PageIndex 39,913 | 19 (4) | Passes; overlaps C7 and N-A |
| 5 | Memory layers | about 117 est. (claude-mem 105,979; mem0 68,112; hindsight 56,614) | 482 (53) | Passes; umbrella |
| 6 | Temporal KGs | 3 (Graphiti 32,373) | 21 (2); 96 broad (10) | Fails Test 2: merge into 5 |
| 7 | Markdown / LLM wiki | about 58 est. (llm_wiki 21,198; claude-obsidian 16,002) | 21 "LLM wiki" (0); 77 (8) | Passes; of 48 April-wave repos 20 still active |
| 8 | Code KGs | 22 (+6) (Graphify 139,374; Understand-Anything 89,048; codegraph 76,004, all fast-growth) | 13 (1); 63 (16) | Passes both |
| 9 | KG construction, schema induction | 8 (+GLiNER) | 75 (64) | Test 2 partial: variant of 1? |
| 10 | NL to graph query | 6 (snapshot blind) | 52 (38) | Passes; partly productised |
| 11 | Multimodal graph RAG | 4 (RAG-Anything 24,322) | 33 (15) | Fails Test 2: merge into 1 |

Growth controls (same API): LLM wording x1.38, RAG x1.23, LLM agents x2.50.

New candidates (evidence in Part 2, Section 5):
- N-A: agentic search over raw data with no built structure (ReFind 2608.12888, Raw-RAG 2610.30755, "Is Grep All You Need?" 2605.15184, RAGFlow-team paper 2610.41172, Anthropic's glob/grep post).
- N-B: knowledge compilation (RAGFlow README 20260819: Wikis, Graphs, Trees, PageIndex, Skills as templates). Umbrella across 1, 4, 7, 9.
- N-C: governed, auditable, attacked agent memory (326 and 133 results; x8 and x15).
- N-D: skills as procedural knowledge (1,106 results; scope question).
- N-E: RL-trained controllers for retrieval and memory (merge with 3).

Merges proposed: 11 into 1 (LightRAG README: "[2026.05] Merge RagAnything into LightRAG"); 6 into 5; 1 and 2 as one shift; 3 with N-E; 9 as a variant of 1 or "schema-first"; decide the boundary of 4, 7 and N-A (all have a model read an index instead of a vector lookup).

Archive leads re-checked: GraphRAG maintenance notice confirmed (commit 2026-08-14 15:08 UTC); LightRAG merge confirmed; gist date confirmed (2026-04-04T16:25:13Z); Neo4j llm-graph-builder "no longer actively developed" NOT found in its README (unverified).

Main gaps: the snapshot has no query for C3, C4, C6, C9, C10, C11, and caps agent memory at 100; push date is not commit activity; keyword recall is low (alphaXiv found at least 14 on-topic C4 papers against 18 keyword hits); two broken queries discarded; abstracts only.

=====================================================================
PART 2: FULL FINDINGS (content for step0-trends/findings.md)
=====================================================================

# Step 0 findings: evidence for the "Current trends" chapter

Written 20261102 (UTC), clock 19:22 to 19:58. Evidence only; the main session applies the tests and the owner approves the list.

Conventions. Dates are YYYYMMDD, UTC. "v1" is the arXiv first-submission date (API field `published`), not the id month: id 2602.23372 has v1 20251227. Window = 20251102 to 20261102. Prior = 20241102 to 20251101. Where sources are silent: **unstated**.

## 1. Method

### 1.1 Snapshot (Test 1a)
- File: `kb-kg/landscape/20261030_1954-github/repos.tsv` (worktree). Snapshot time 20261030 19:54 UTC. Read and analysed locally 20261102 19:22 to 19:54 with `python3 -I` scripts.
- 931 rows (core 238, agent-memory 244, markdown-kb 107, adjacent 342). 556 have days_since_push at most 90 (552 not archived). Flags: quiet 375, archived 26, fast-growth 10, low-forks 1.
- Active = days_since_push at most 90 and not archived (the snapshot's own ranking rule).
- Matching. TSV descriptions are cut at about 120 characters, no topics. I read all 556 active and 375 quiet rows and tagged by hand. D = snapshot description or name states the mechanism; E = mechanism from a README or the archive; C = component or borderline. For the two big families (memory, Markdown) I used a regex count plus a seeded random sample for precision (hand-tagging 170 rows each was not defensible as an exact count). Lists: scripts/classify.py, rx_multi.py, rx_sample.py.
- Blind spots (snapshot README, "Search queries"): 34 searches, stars >= 100, max 100 results per pass. topic:agent-memory active reports 202 matches and returns 100; topic:ai-memory 103 and 100; topic:rag topic:llm 379 and 100. Only one query touches text-to-Cypher (5 active matches). None for temporal graphs, schema induction, multimodal graphs, vectorless retrieval. So counts for C3, C4, C6, C9, C10, C11 are lower bounds; C5 is capped; new low-star repos (October 2026) are under-represented.
- Push is not commit. commits_90d and contributors exist for only 124 enriched rows. pingcap/autoflow: d7 but 0 commits in 90 d; neo4j-labs/llm-graph-builder: d1 but 1 commit.

### 1.2 arXiv (Test 1b)
- Tool: arXiv API (export.arxiv.org/api/query) called with Python urllib under `python3 -I` (more exact than WebFetch summaries). Each query used submittedDate:[202511020000 TO 202611022359], newest first; count = opensearch:totalResults; a second call counted the prior year. Quarter split from `published` of fetched entries (P1 20251102 to 20260131, P2 to 20260430, P3 to 20260731, P4 to 20261102). Raw XML kept, one folder per query.
- Read times: batch 1 (12 queries) 19:26 to 19:27; batch 2 19:31 to 19:37; id lookups 19:37 to 19:38 and 19:47; batch 4 (5 queries) 19:44 to 19:45; controls 19:46 to 19:47.
- Noisy counts. For each query I read the newest 20 to 45 titles and judged the on-topic share. Examples were checked by reading the abstract text the API returned. Exact strings: scripts/spec1.json, spec2.json, spec4.json, spec5_controls.json; primary ones in Appendix A.
- Two queries discarded: c2b_llm_free_graph (928 results) and c4b_vectorless (1,011); newest results were unrelated. My reading, not verified: quoted phrases with stop words ("no vector", "without LLM") degrade to one generic word.
- Recall is low where wording varies: the first code-graph query (c8) missed the Codebase-Memory paper 2603.27277; later queries found it.
- Growth controls (count only): any LLM wording 44,692 vs 32,396 prior (x1.38); any RAG wording 3,357 vs 2,736 (x1.23); LLM-agent wording 15,158 vs 6,068 (x2.50).

### 1.3 alphaXiv
Six discover_papers calls with published_after=2025-11-02 and prioritize=recency (C4 and C6 about 19:44; C7 and C8 about 19:45; C2 and C3 about 19:49; the tool returns no timestamps). Ranked lists, no totals; used to check recall and find examples. Ids it surfaced were verified against the arXiv API (batch 6, 19:47).

### 1.4 Primary sources fetched (20261102 UTC)
| Source | Time |
|---|---|
| READMEs via GitHub API: PageIndex, GraphRAG, LightRAG, Graphiti, Mem0, Graphify | 19:37 |
| Karpathy "LLM Wiki" gist (raw); GraphRAG README commit list; LazyGraphRAG blog; Basic Memory, neo4j-graphrag-python, RAGFlow READMEs | 19:42 |
| GraphRAG docs "Indexing Methods" | 19:43 |
| GitHub metadata: GraphRAG-R1, RAGSearch, GraphSearch, Search-R1 | 19:48 |
| READMEs: vector-graph-rag, ripwire, memoket-kite | 19:49 |
| Anthropic "Effective context engineering for AI agents" | 19:50 |
| Gist HTML (creation datetime); gist API returned HTTP 502 | 19:51 |
| Neo4j llm-graph-builder README | 19:52 |

### 1.5 Archive leads re-checked
| Lead | Result |
|---|---|
| GraphRAG maintenance notice 20260814 | Confirmed: README commit "Add notice. (#2486)" 21f7bdf, 2026-08-14 15:08 UTC |
| LightRAG merged RAG-Anything (2026.05) | Confirmed in the LightRAG README news |
| Mem0 April 2026 ADD-only algorithm; best scores need "proprietary optimizations not available in the open-source" | Confirmed in README |
| Gist created 20260404 | Confirmed: 2026-04-04T16:25:13Z |
| Codebase-Memory paper 2603.27277, 28 March 2026 | Confirmed, v1 20260328 |
| Neo4j llm-graph-builder "no longer actively developed" | NOT confirmed: README (19:52) has none of: no longer, actively developed, maintenance, deprecat, successor |
| LazyGraphRAG not in the open-source package | Consistent: docs methods page lists only Standard and Fast |

## 2. Summary table

| # | Candidate | Core idea | Shift | Active projects n; top 3 (stars, days since push, flags) | Papers in window n (query), prior | Nearest neighbour: difference | Preliminary status |
|---|---|---|---|---|---|---|---|
| 1 | LLM-built (eager) KGs | LLM extracts entities and relations from every chunk at index time; graph is the index | flat chunks to graph index | 20 (17 D, 3 E). LightRAG 40,443 d1; GraphRAG 36,498 d1; llm-graph-builder 5,289 d1. No flags | 48 narrow (c1), prior 29; family 272 (c0), prior 167 | C2: when a model is used | Passes both. Settled evidence partial |
| 2 | Cheaper or lazy build | Noun-phrase/NER graphs, no LLM, or LLM deferred to query time | eager extraction to cheap/deferred | 2 (0 D): GLiNER 4,184 d6 (component); HippoRAG 4,083 d23. 6 quiet | 32 (c2c), prior 13; 39 (c2), prior 24 | C1; also C8. Lever recurs in C5, C7, C8 | Papers pass; snapshot fails. Unclear |
| 3 | Agentic/RL graph retrieval | A (RL-trained) model picks next hop over a graph | one-shot retrieval to multi-turn policy | 0 strict; gfm-rag 309 d52 borderline. 7 quiet | 44 (c3b), prior 18; broad 259, prior 111 | C4: trained policy over graph vs prompted LLM over tree | Passes via papers only |
| 4 | Reasoning over structure | LLM reads a tree built from document structure | similarity search to LLM reasoning over a tree | 2 D (+2 E, +2 C): PageIndex 39,913 d0; memoket-kite 230 d0; RAGFlow 93,209 and Dify 160,020 by E | 19 (c4d), prior 4; 18 (c4), prior 5; 82 broad (c4c), prior 32 | C7 and N-A: what is built | Passes both; overlap risk |
| 5 | Memory layers | Keep facts/notes across sessions; decide update or drop | documents to agent memory | 173 regex, about 117 on-topic. claude-mem 105,979 d0 fast-growth; mem0 68,112 d0; hindsight 56,614 d0 fast-growth | 482 (c5_full), prior 53 | C6, C7 | Passes both; umbrella |
| 6 | Temporal KGs | Facts have validity windows; contradiction invalidates | overwrite/static to bi-temporal | 3: Graphiti 32,373 d1; Zep 4,984 d10; memtrace-public 509 d0 | 21 (c6), prior 2; 96 (c6c), prior 10 | C5: time is a design axis | Passes Test 1; fails Test 2 (merge into C5) |
| 7 | Markdown / LLM wiki | LLM compiles sources into linked Markdown once | re-derive per query to compile at ingest | 84 regex, about 58 on-topic. llm_wiki 21,198 d9; claude-obsidian 16,002 d4; EverOS 13,721 d0 | 21 (c7b), prior 0; 77 (c7), prior 8; 59 (c7d), prior 2 | C5, C4 | Passes both; overlaps |
| 8 | Code KGs | Parse repo into graph; serve to coding agents | grep/file reads to code graph | 22 D (+6 C). Graphify 139,374 d3 fast-growth; Understand-Anything 89,048 d4 fast-growth; codegraph 76,004 d0 fast-growth | 13 (c8c), prior 1; 63 (c8b), prior 16 | C2 (parser instead of LLM) | Passes both |
| 9 | KG construction, schema induction | LLMs extract triples and induce the schema | predefined to induced schema | 8 D (+GLiNER). llm-graph-builder 5,289 d1; Hyper-Extract 4,207 d1; ai-knowledge-graph 3,134 d46. 8 quiet | 75 (c9), prior 64; 116 (c9b), prior 50 | C1: same extraction step | Test 2 partial; unclear |
| 10 | NL to graph query | Model writes Cypher/SPARQL; DB executes | hand-written to LLM-written queries | 6 (snapshot blind). code-graph-rag 5,303 d0 (E); neo4j-graphrag-python 1,326 d0 (E); text2cypher 245 d21 | 52 (c10b), prior 38; 57 (c10), prior 34 | C3: translate once vs walk | Passes both; partly productised |
| 11 | Multimodal graph RAG | Images/tables/equations become graph nodes | text-only to multimodal | 4: RAG-Anything 24,322 d2; jonex 1,522 d2; ApeRAG 1,318 d1 | 33 (c11), prior 15; 73 (c11b), prior 32 | C1: absorbed (LightRAG 2026.05) | Fails Test 2 (merge into C1) |

## 3. Cross-cutting observations

### 3.1 Test 2 axes (what is built or stored; when a model is used; who steers)
| # | Built or stored | Model used when | Steering |
|---|---|---|---|
| 1 | Entity-relation graph by LLM extraction, plus community summaries | Index time per chunk; answer time | Fixed pipeline or algorithm |
| 2 | Cheaper graph (noun phrases, NER plus embeddings, none) | Reduced or removed at index; deferred to query in LazyGraphRAG | Pipeline |
| 3 | Graph/hypergraph built beforehand | Query time, multi-turn; RL at training | Trained model |
| 4 | Tree from document layout | Query time: LLM reasons over tree | Prompted model |
| 5 | Facts/notes/episodes in a store, plus consolidation | Write and read time | Pipeline or the agent |
| 6 | Facts with validity windows plus episodes | Ingestion; retrieval | Hybrid retrieval |
| 7 | LLM-written Markdown pages, index.md, log.md | Ingest (compile), query (navigate), lint | Model reads index then pages |
| 8 | Code graph from a parser | None at index; agent queries | Coding agent calls tools |
| 9 | KG plus induced schema | Construction | Not a retrieval design |
| 10 | Nothing new: existing graph DB | Query time: model writes the query | DB engine executes |
| 11 | Graph over text, image, table, equation nodes | Index time (parser, VLM) | Pipeline |

Pairs sharing most axes: C1/C2, C4/C7, C3/C4, C5/C6/C7, C1/C11.

### 3.2 Baselines
- GraphRAG family (c0): 272 vs 167 (x1.63), per quarter 45 / 66 / 84 / 77; RAG overall x1.23.
- Far above the agent baseline (x2.5): C5 x9.1, C6 x10, C7, C8 x3.5 to 13, C4 x3.6 to 4.8. About at baseline: C3 x2.4, C10 x1.4 to 1.7, C1 x1.6, C9 x1.2 narrow. Small prior counts (C4, C6, C7, C8) make ratios unstable.

### 3.3 Fast-growth flags
Ten repos: four code graphs (Graphify, Understand-Anything, codegraph, codebase-memory-mcp), two memory (claude-mem, hindsight), four off-topic (MiroFish, headroom, hello-agents, book-to-skill). Heuristic only; star timelines not examined.

### 3.4 Overlap inside the snapshot (regex, 552 active rows)
Memory 173, Markdown/wiki 84, coding-agent wording 91, graph wording 138, MCP 52. Memory and wiki: 25 (30% of wiki). Wiki and coding-agent: 23. Memory and coding-agent: 44. All three: 10.

## 4. Evidence per candidate

### 4.1 Candidate 1: LLM-built (eager) knowledge graphs
Core idea: an LLM reads every chunk at index time, extracts entities and relations; the graph (often with community summaries) is the index.
Shift as sources put it: GraphRAG abstract (2404.16130, read 19:37): "Our approach uses an LLM to build a graph index in two stages: first, to derive an entity knowledge graph from the source documents, then to pregenerate community summaries". LightRAG abstract (2410.05779): existing RAG has "reliance on flat data representations"; LightRAG "incorporates graph structures into text indexing and retrieval processes".

Test 1a. Match: description names GraphRAG, graph RAG, LightRAG or an LLM KG builder (17 D) plus 3 E (LightRAG, TrustGraph, HippoRAG). Active n = 20.
| Repo | Stars | Days | Flags | Release; commits 90 d; contributors |
|---|---|---|---|---|
| HKUDS/LightRAG | 40,443 | 1 | none | v1.5.7 20260902; 100+; 353 |
| microsoft/graphrag | 36,498 | 1 | none | v3.3.0 20261008; 20; 51 |
| neo4j-labs/llm-graph-builder | 5,289 | 1 | none | v0.8.7 20260723; 1; 22 |
Others active: m_flow, Hyper-Extract, HippoRAG, ai-knowledge-graph, autoflow, TrustGraph, edgequake, neo4j-graphrag-python (100+ commits), ApeRAG, FalkorDB GraphRAG-SDK (100+), Kwipu, awslabs/graphrag-toolkit, VeritasGraph, vector-graph-rag, flexible-graphrag, hugegraph-ai, RAGU. Quiet (12 listed; 48 regex matches): KAG 9,140 d275; nano-graphrag 4,006 d276; Youtu-GraphRAG 1,271 d246. vector-graph-rag uses an LLM for triplet extraction (README 19:49: "Documents → Triplet Extraction (LLM) → Entities + Relations → Embedding → Milvus"); "pure vector search" means no graph database.

Test 1b. Family c0: 272, prior 167; 45 / 66 / 84 / 77; about 15 of newest 20 on-topic. Narrow c1: 48, prior 29; 10 / 8 / 17 / 13; about 17 of newest 25 on-topic. Examples (abstracts read): 2605.28004 (20260527) Beyond Chunk-Local Extraction: Cross-Chunk Graph Augmentation for GraphRAG; 2603.25152 (20260326) OMD-GraphRAG; 2607.11683 (20260713) RAGU; 2511.05549 (20251102) AGRAG.

Test 2. Nearest C2. Difference: C1 uses a model on every chunk at index time; C2 reduces, replaces or defers it. Source: GraphRAG docs (19:43): "Standard uses a language model for all reasoning tasks: entity extraction, relationship extraction, entity summarization ... community report generation"; "We estimate graph extraction to constitute roughly 75% of indexing cost."

Settled evidence. For: GraphRAG README (19:37): "largely in maintenance mode, and won't be accepting new PRs or implementing new features ... Since our first release in July 2024 the capabilities of frontier models have changed dramatically" (notice 20260814). Vendor layer: neo4j-graphrag-python v1.23.0 d0, FalkorDB GraphRAG-SDK v1.5.0 d0, awslabs/graphrag-toolkit, pingcap/autoflow, apache/hugegraph-ai; Memgraph describes itself as a graph database "for GraphRAG, AI memory, agentic AI". Against: LightRAG v1.5.7, 100+ commits in 90 d, README news through 2026.07; family papers x1.63. Not re-verified: llm-graph-builder banner.
Status: passes both; settled flag partial. C1 is the "from" side of the C1 to C2 shift.
Representative projects (candidates): microsoft/graphrag; HKUDS/LightRAG; neo4j-labs/llm-graph-builder; OSU-NLP-Group/HippoRAG (4,083 d23); OpenSPG/KAG (9,140, quiet d275).
Fundamental papers (candidates): 2404.16130; 2410.05779; 2405.14831 and 2502.14802; 2409.13731; 2506.05690 (evaluation).

### 4.2 Candidate 2: cheaper or lazy graph construction
Core idea: lower the cost of building the graph: noun phrases/co-occurrence, NER plus embeddings, no LLM, or LLM deferred to query time.
Shift: LazyGraphRAG blog (Microsoft Research, published 20241125, read 19:42): "a radically different approach to graph-enabled RAG that requires no prior summarization of the source data, avoiding the up-front indexing costs"; "the 'lazy' approach defers all LLM use until query time"; "data indexing costs are identical to vector RAG and 0.1% of the costs of full GraphRAG" (Microsoft's figures). Graph-R1 abstract: GraphRAG "still face[s] challenges in high construction cost". LinearRAG abstract (2510.10114): methods "rely on unstable and costly relation extraction".

Test 1a. No active prose-graph project states a cheaper or LLM-free build as its mechanism. Active: GLiNER 4,184 d6 (non-generative extractor, 47 commits; component); HippoRAG 4,083 d23 (E, fewer LLM calls). GraphRAG's own "Fast" method is inside C1's repo. Quiet (6): nano-graphrag 4,006 d276; fast-graphrag 3,967 d362 (no release); MiniRAG 2,026 d379; LinearRAG 566 d117; LogicRAG 241 d103; datastax/graph-rag 91 d543. LazyGraphRAG is a blog and product (editor's note 20250606: "integrated into Microsoft Discovery ... and into Azure Local"), not a repo; docs methods page lists only Standard and Fast. The same lever appears elsewhere: shodh-memory ("Local, LLM-free memory", 316 d4), Emmimal/wiki-compiler ("zero LLM calls", 111 d46), memtrace-public ("zero LLM calls", 509 d0), all code-graph tools.

Test 1b. c2c: 32, prior 13 (x2.5); 6 / 10 / 7 / 9; about 12 to 14 of 32 on-topic. c2: 39, prior 24; 6 / 10 / 14 / 9. alphaXiv: 12 returned, at least 9 on-topic (LiteRAG 2609.10239; Matryoshka Hierarchical RAG 2610.01767). Examples (abstracts read): 2609.19622 (20260917) Geometric Gain Graph, zero-token; 2604.16350 (20260316) LiteSemRAG, LLM-free; 2602.23372 (v1 20251227) SPRIG, "CPU-only, linear-time, token-free GraphRAG pipeline that replaces LLM graph building with lightweight NER"; 2605.19735 (20260519) ContextRAG, extraction-free; 2609.18099 (20260916) EffiRAG. No arXiv paper for LazyGraphRAG (title/abstract search, 6 unrelated hits, 19:37).

Test 2. Nearest C1 (same structure, cheaper). Also C8: Graphify README (19:37) "Code is parsed with tree-sitter AST: deterministic, no LLM"; 2601.08773 (v1 20260113): AST-derived graphs build "in seconds", LLM-extracted ones "much longer". Weakness: the lever is cross-cutting, so C2 is a property more than a family.
Settled: none for the idea; LazyGraphRAG product-integrated; open-source cheap-GraphRAG projects are quiet.
Status: papers pass Test 1, snapshot fails; Test 2 holds against C1, weak against C8. Unclear; option: one shift with C1 (as the archive's eager-to-lazy-graphs.md does).
Representative projects (candidates): LazyGraphRAG (blog); GraphRAG Fast method; LinearRAG; fast-graphrag; HippoRAG.
Fundamental papers (candidates): 2502.09304 KET-RAG (v1 20250213); 2510.10114 LinearRAG (20251011, before window); 2501.06713 MiniRAG; 2609.18099; 2609.19622.

### 4.3 Candidate 3: agentic or reinforcement-learned graph retrieval
Core idea: a model, often RL-trained, picks the next hop or query over a graph/hypergraph across turns.
Shift: Graph-R1 abstract (2507.21892, 19:37): GraphRAG has "fixed one-time retrieval"; Graph-R1 "models retrieval as a multi-turn agent-environment interaction".

Test 1a. Strict n = 0 active. Borderline: gfm-rag 309 d52. Quiet (7): Youtu-GraphRAG 1,271 d246; ToG 666 d950; Graph-R1 599 d182 (0 commits, 1 contributor); HyperGraphRAG 460 d171; arag 364 d266; graph-constrained-reasoning 268 d528; MemGraphRAG 233 d131. Not in snapshot (GitHub API 19:48): GraphRAG-R1 15 stars pushed 20260228; RAGSearch 17 stars pushed 20260825; GraphSearch 100 stars pushed 20260409; Search-R1 5,561 stars pushed 20251113.
Test 1b. c3b: 44, prior 18 (x2.4; agent control x2.5); 13 / 7 / 14 / 10; about 18 of 44 on-topic. c3 broad: 259, prior 111; 40 / 66 / 91 / 62. alphaXiv: 15 returned, all on-topic, five dated 20261015 to 20261027 (2610.37405, 2610.35598, 2610.21345). Examples (abstracts read): 2603.28533 (20260330) GraphWalker, COLM 2026; 2606.16409 (20260615) PathRouter; 2607.18481 (20260720) Search-on-Graph-R1; 2610.28010 (20261020) RANGER; 2601.17755 (20260125) HyperGraphPro; 2610.25384 (20261018).
Test 2. Nearest C4: both let a model steer retrieval over a built structure. C3 trains the policy and walks a graph/hypergraph; C4 prompts a general model over a document tree. Also overlaps N-E.
Settled: none. Status: passes Test 1 through papers only; Test 2 passes with overlap.
Representative projects (candidates): LHRLAB/Graph-R1; ycygit/GraphRAG-R1; TencentCloudADP/youtu-graphrag; DataArcTech/GraphSearch; FanDongzhe123/RAGSearch (benchmark).
Fundamental papers (candidates): 2507.21892 (v1 20250729); 2507.23581 (20250731); 2509.22009; 2603.28533; 2503.09516 Search-R1 (plain-text baseline).

### 4.4 Candidate 4: reasoning over structure without vectors or graph algorithms
Core idea: build a hierarchy from the document's own structure; an LLM decides which node to open.
Shift: PageIndex README (19:37): "replaces the vector index with a hierarchical tree index and lets an LLM reason its way through it"; "similarity ≠ relevance".
Test 1a. D: PageIndex 39,913 d0 (v0.5.0 20261029; 100+ commits; 16 contributors; README updates Aug and Oct 2026); memoket-kite 230 d0 (README "vector-free"; v0.1.0 20260813; paper 2610.41521). E: RAGFlow 93,209 d0 (README 19:42: "2026-08-19 Introduced Knowledge Compilation to generate Wikis, Graphs, Trees, PageIndex, Mind Maps, Timelines, and Skills"); Dify 160,020 d0 (archive lead, not re-read). Borderline: nocturne_memory 1,412 d37; llm-wiki-memory 129 d51. Quiet: OpenKB 4,831 d100; LogicRAG 241 d103. Snapshot has no query here: lower bound.
Test 1b. c4d: 19, prior 4 (x4.8); 3 / 3 / 4 / 9; about 9 or 10 of 19 on-topic. c4: 18, prior 5. c4c: 82, prior 32; 13 / 12 / 27 / 30; about 9 of newest 30 on-topic. alphaXiv: 18 returned, at least 14 on-topic (2610.35868 DecisionRAG, 49 votes; 2605.27123; 2610.06902; 2609.33322; 2606.18381; 2608.07994). PageIndex named in five abstracts (20260414 to 20261030). Examples (abstracts read): 2610.11370 (20261008) RIT-RAG; 2610.35868 (20261026) DecisionRAG; 2511.18177 (20251122) Lumer et al., "hierarchical node-based systems that traverse document structure without embeddings"; 2604.14222 (20260414); 2610.41172 (20261030).
Test 2. Nearest C7 (LLM reads an index; gist: reads "the index first to find relevant pages") and N-A (nothing built). Difference: tree built from layout, mostly without an LLM at index (PageIndex README: "The tree structure itself is extracted from the document layout without an LLM; the index model only summarizes and refines it"). The archive's reasoning-retrieval.md already files the LLM Wiki under C4 variants: soft boundary.
Settled: none. Counter: Lumer, vector agentic RAG won 68% of comparisons; 2610.41172: "a PageIndex-style outline degraded at scale".
Status: passes both; overlap risk with C7 and N-A.
Representative projects (candidates): VectifyAI/PageIndex; VectifyAI/OpenKB (quiet); RAGFlow Tree/PageIndex outputs; chensyCN/LogicRAG (quiet); memoket-kite.
Fundamental papers (candidates): PageIndex has no paper (unstated). 2508.06105 LogicRAG (v1 20250808); 2511.18177; 2610.11370; 2610.35868; 2401.18059 RAPTOR (ancestor, uses embeddings).

### 4.5 Candidate 5: memory layers for agents
Core idea: keep what an agent learned across sessions as facts, notes or episodes; decide what to update or drop.
Shift: Zep abstract (2501.13956): RAG frameworks "are limited to static document retrieval, enterprise applications demand dynamic knowledge integration". HippoRAG 2 title: "From RAG to Memory". Survey 2512.13564 (v1 20251215): the field "has become increasingly fragmented"; distinguishes agent memory from "LLM memory, retrieval augmented generation (RAG), and context engineering".
Test 1a. Category agent-memory: 199 active. Regex memory|memories|remember|recall: 173 active; 27 of 40 seeded-sample judged on-topic, so about 117 (range 90 to 140).
| Repo | Stars | Days | Flags | Release; commits 90 d |
|---|---|---|---|---|
| thedotmack/claude-mem | 105,979 | 0 | fast-growth | v15.7.0 20261030; 100+ |
| mem0ai/mem0 | 68,112 | 0 | none | ts-v3.3.1 20260925; 100+; 411 contributors |
| vectorize-io/hindsight | 56,614 | 0 | fast-growth | v1.1.0 20261021; 100+ |
Next: OpenViking 41,197 (AGPL-3.0); cognee 32,934 (v1.6.6 20261029); supermemory 31,471; letta 25,294 d11 (7 commits). Creation months of the regex set: 2026-02 22, 03 30, 04 24, 05 19, 06 11, 07 12, 08 16, 09 7, 10 1 (tail partly the 100-star floor).
Test 1b. c5_full: 482, prior 53 (x9.1); 58 / 86 / 165 / 173. 44 of newest 45 titles on-topic; about 31 of oldest 35 (hardware "memory" papers are the noise). c5b (graph): 122, prior 15. Examples (abstracts read): 2512.12818 (20251214) Hindsight; 2512.13564 (20251215) survey; 2610.30755 (20261022) "Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought"; 2610.29671 (20261021) Uni-Mem; 2610.34073 (20261025) Memory Tax. Also 2606.24775 (20260623): "no single architecture dominates across all scenarios".
Test 2. Nearest C6, C7. The archive's agent-memory.md lists five families; C6 and C7 are two of them. Mem0 README: "Single-pass ADD-only extraction -- one LLM call, no UPDATE/DELETE. Memories accumulate"; Graphiti README: invalidation instead.
Settled: none; highest activity of all; contested by independent audits (Raw-RAG, Memory Tax).
Status: passes both; umbrella overlapping C6, C7, N-C, N-D, N-E.
Representative projects (candidates): mem0ai/mem0; letta-ai/letta; topoteretes/cognee; vectorize-io/hindsight; thedotmack/claude-mem.
Fundamental papers (candidates): 2310.08560 MemGPT (v1 20231012); 2504.19413 Mem0 (20250428); 2502.12110 A-MEM; 2512.12818 Hindsight (in window); 2512.13564 survey (in window).

### 4.6 Candidate 6: temporal knowledge graphs for agents
Core idea: each fact has a validity window; a contradiction ends the old fact instead of deleting it; raw episodes stay as provenance.
Shift: Graphiti README (19:37): "Unlike static knowledge graphs, Graphiti's context graphs track how facts change over time, maintain provenance to source data"; its table: GraphRAG "Basic timestamp tracking" vs Graphiti "Explicit bi-temporal tracking with automatic fact invalidation".
Test 1a. Active n = 3: getzep/graphiti 32,373 d1 (v0.31.2 20261020; 100+ commits; 64 contributors); getzep/zep 4,984 d10 (examples/integrations for the hosted service; 22 commits); syncable-dev/memtrace-public 509 d0 ("Bi-temporal graph ... zero LLM calls", coding agents). Borderline databases: NornicDB 920, Raphtory 650. Graphiti README lists "Kuzu 0.11.2 (deprecated)".
Test 1b. c6: 21, prior 2 (x10.5); 3 / 2 / 11 / 5; about 9 on-topic. c6c: 96, prior 10; 8 / 15 / 36 / 37; about 25 to 30 on-topic (the topic widens to "temporal validity of agent memory"). alphaXiv: 15 returned, at least 10 on-topic (2609.27279, 2607.27773, 2609.34242, 2608.24921, 2607.20560, 2609.36457). Examples (abstracts read): 2608.08055 (20260808) SodaMem; 2606.09900 (20260605) Bi-Temporal Memory Engine; 2606.26511 (20260625) Temporal Validity in Retrieval Memory; 2607.10265 (20260711) TGMS; 2604.11544 (20260413) Time is Not a Label (EMNLP 2026).
Test 2. Nearest C5. Distinct mechanism: validity windows on graph edges with invalidation. But time handling is a design axis of all memory (Mem0 README adds "Temporal Reasoning -- time-aware retrieval" on a flat store; several 2026 papers address staleness without graphs).
Settled: none; relabelling visible (Graphiti "temporal context graphs"; Zep "unified context layer for enterprises").
Status: passes Test 1; fails Test 2 as stand-alone (merge into C5); option: short sub-section.
Representative projects (candidates): getzep/graphiti; getzep/zep; syncable-dev/memtrace-public.
Fundamental papers (candidates): 2501.13956 Zep (v1 20250120, before window); 2606.09900; 2608.08055; 2607.10265; 2604.11544.

### 4.7 Candidate 7: Markdown / plain-file / LLM wiki knowledge bases
Core idea: the LLM compiles sources into linked Markdown pages once and keeps them current; a person can read and edit the files.
Shift: Karpathy gist (created 2026-04-04T16:25:13Z; raw read 19:42): "the LLM is rediscovering knowledge from scratch on every question"; "the LLM incrementally builds and maintains a persistent wiki ... The knowledge is compiled once and then kept current, not re-derived on every query"; index.md "works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and avoids the need for embedding-based RAG infrastructure"; "as the wiki grows you want proper search".
Test 1a. Regex (wiki, obsidian, markdown, vault, second brain, git-native, karpathy, ...): 84 active; 31 of 45 sampled on-topic, so about 58 (range 45 to 70). Category markdown-kb: 64 active of 107. Top 3: nashsu/llm_wiki 21,198 d9 (v0.6.13 20261022; 100+ commits; licence NOASSERTION); AgriciDaniel/claude-obsidian 16,002 d4 (v3.0.1 20261021; MIT); EverMind-AI/EverOS 13,721 d0 (also C5). Next: obsidian-mind 5,460; obsidian-second-brain 5,061; open-knowledge 4,741; basic-memory 4,416 (v1.0.0 20261029; AGPL-3.0; README: "Your knowledge lives as Markdown files that both you and your AI can read, write, and search"). No fast-growth flags.
April wave: 48 repos matching wiki/karpathy were created 20260404 to 20260430 (at least 100 stars); at the snapshot 20 are active and 28 quiet. 17 more created from 20260501; 11 active. September creations include tigerless-labs/agent-memory, okf-agent-memory, second-brain-os, llm-wiki-v2.
Test 1b. c7b ("LLM wiki" etc.): 21, prior 0; 0 / 3 / 11 / 7; about 13 on-topic. First on-topic papers v1 20260413, nine days after the gist: 2604.11243 and 2604.12034, whose abstract says "a visible cluster of personal wiki-style memory architectures emerged in April 2026 -- design proposals from Karpathy, MemPalace, and LLM Wiki v2". c7 broad: 77, prior 8; 4 / 19 / 32 / 22 (about one third on-topic). c7c (files/Markdown/git as memory, title): 39, prior 6. c7d (AGENTS.md, CLAUDE.md, cursorrules, context files): 59, prior 2; 2 / 8 / 18 / 31; mostly on-topic. alphaXiv: 15 returned, at least 11 on-topic (adds 2608.27454 WikiSkill, 2609.25991, 2605.15184). Examples (abstracts read): 2607.26637 (20260729) Filesystem-Based Memory for LLM Agents; 2605.18490 (20260518) Single-Round Vector RAG vs an LLM-Compiled Wiki; 2607.04576 (20260706) Progressive Disclosure for LLM-Maintained Wiki Knowledge Bases; 2605.07068 (20260508) WiCER; 2607.26604 (20260729) WikiLoop.
Test 2. Nearest C5 (25 of 84 wiki-regex repos are also memory repos; 2607.26637: agents "keep their long-term memory as a filesystem: a directory tree of markdown files") and C4 (model reads index.md then pages). Difference: the artifact is a human-readable, human-editable page set compiled at ingestion; memory layers store extracted records.
Settled: none, too new. Decay visible (28 of 48 April-wave repos quiet); the gist itself gives no size threshold.
Status: passes both; overlaps with C5, C4 and the AGENTS.md strand to be decided.
Representative projects (candidates): Karpathy gist (not a repo); nashsu/llm_wiki; AgriciDaniel/claude-obsidian; basicmachines-co/basic-memory; VectifyAI/OpenKB (quiet d100).
Fundamental papers (candidates): no founding paper (a gist, 20260404). Papers: 2607.26637; 2605.18490; 2607.04576; 2604.12034; 2512.05470 (v1 20251205).

### 4.8 Candidate 8: code knowledge graphs for coding agents
Core idea: parse a repository into a graph (symbols, calls, imports) and serve it to a coding agent through MCP, CLI or skill.
Shift: Codebase-Memory abstract (2603.27277, v1 20260328, read 19:33): agents "typically explore codebases through repeated file-reading and grep-searching, consuming thousands of tokens per query without structural understanding"; builds "a persistent, Tree-Sitter-based knowledge graph via the Model Context Protocol". Graphify README: "Code is parsed with tree-sitter AST: deterministic, no LLM"; "Not a vector index".
Test 1a. Active n = 28 (22 D, 6 C).
| Repo | Stars | Days | Flags | Release; commits 90 d; contributors |
|---|---|---|---|---|
| Graphify-Labs/graphify | 139,374 | 3 | fast-growth | v0.9.97 20261027; 100+; 374 |
| Egonex-AI/Understand-Anything | 89,048 | 4 | fast-growth | v2.9.0 20260710; 100+; 75 |
| colbymchenry/codegraph | 76,004 | 0 | fast-growth | v1.6.2 20261003; 100+; 51 |
Next: codebase-memory-mcp 47,853 d1 fast-growth (v0.12.1 20261016); code-review-graph 32,509 d1; code-graph-rag 5,303 d0; ripwire 2,495 d0 (README "Ranked, deterministic call graph"); gortex 1,948. Creation months run 2026-01 to 2026-10 (Graphicle 202610).
Test 1b. c8c: 13, prior 1 (x13); 0 / 2 / 3 / 8. c8b: 63, prior 16; 5 / 14 / 14 / 30; about 25 of 63 on-topic. c8 (first wording): 52, prior 15 (missed 2603.27277). alphaXiv: 14 returned, at least 9 on-topic (2610.36153, 2607.24882, 2607.25431). Examples (abstracts read): 2603.27277 (20260328); 2610.33958 (20261025) How Do Small Coding Agents Use Code Graphs and Embeddings?; 2601.08773 (20260113); 2605.16352 (20260508) LARGER; 2609.16936 (20260915) RepoAtlas.
Test 2. Nearest C2 (graph without an LLM, here by parser) and C1. Difference: domain is code, construction deterministic, consumer is a coding agent calling graph tools.
Settled: none; value over grep contested: 2610.33958: "no tool set flattens that gradient"; 2605.15184: grep "generally yields higher accuracy than vector retrieval" in its LongMemEval comparison; Anthropic (published 20250929, read 19:50): Claude Code uses glob and grep "just-in-time, effectively bypassing the issues of stale indexing and complex syntax trees".
Status: passes both.
Representative projects (candidates): Graphify-Labs/graphify; Egonex-AI/Understand-Anything; colbymchenry/codegraph; DeusData/codebase-memory-mcp; tirth8205/code-review-graph.
Fundamental papers (candidates): 2603.27277; 2601.08773; 2610.33958; before the window 2410.14684 RepoGraph (v1 20241003) and 2408.03910 CodexGraph (20240807). Archive lead not re-fetched: Aider repo-map post (20231022).

### 4.9 Candidate 9: KG construction with LLMs and schema induction
Core idea: LLMs extract triples and induce the schema or ontology instead of using a predefined one.
Shift: AutoSchemaKG abstract (2505.23628, v1 20250529): "fully autonomous knowledge graph construction that eliminates the need for predefined schemas"; "92% semantic alignment with human-crafted schemas".
Test 1a. Active n = 9 (8 D + GLiNER): llm-graph-builder 5,289 d1 (1 commit); Hyper-Extract 4,207 d1 (100+); GLiNER 4,184 d6; ai-knowledge-graph 3,134 d46 (24); helix-foundry 1,854 d0 (created 20261007); ontogpt 1,080 d50 (38); carrel 653 d3 (created 20260928); cortexdb 474 d1; ontobricks 455 d0. Quiet (8): kg-gen 1,289 d219; AutoSchemaKG 845 d184; llmgraph 509 d384. Three actives are also C1 tools.
Test 1b. c9: 75, prior 64 (x1.2, below LLM control x1.38); 21 / 11 / 24 / 19; about 65% on-topic. c9b: 116, prior 50; 15 / 25 / 39 / 37. Challenge series: 2608.27101 (LLMs4OL 2026 entry). Examples (abstracts read): 2603.20059 (20260320) DIAL-KG; 2607.21610 (v1 20260520) SCOPE and SCION, "Schema graphs are an upstream bottleneck"; 2605.29168 (20260527); 2604.02618 (20260403) OntoKG; 2609.31663 (20260915).
Test 2. Nearest C1 (identical first step). Difference: output is the typed graph/ontology as a reusable asset judged against human schemas, not an index judged on answers. Schema-first is the distinct part.
Settled: extraction step standard inside GraphRAG tools; schema-induction research continues.
Status: passes Test 1 (papers; small active repos); Test 2 partial; unclear (variant of C1, or "schema-first/ontology-first").
Representative projects (candidates): HKUST-KnowComp/AutoSchemaKG (quiet); stair-lab/kg-gen (quiet); monarch-initiative/ontogpt; yifanfeng97/Hyper-Extract; HelixDB/helix-foundry.
Fundamental papers (candidates): 2505.23628; 2502.09956 KGGen (v1 20250214); 2404.03868 EDC (20240405); 2603.20059; 2607.21610.

### 4.10 Candidate 10: natural language to graph query
Core idea: the model translates a question into Cypher or SPARQL; the database engine runs it.
Shift: Text2Cypher abstract (2412.10064, v1 20241213): "using Cypher requires specialized knowledge, which can present a challenge". CypherGuard abstract (2610.41755, v1 20261030): "Graph database systems increasingly adopt this translation as a native query interface. Large language models generate fluent Cypher but stay unreliable."
Test 1a. One snapshot query touches this (5 active hits). Active n = 6: neo4j-labs/text2cypher 245 d21 (CC0; datasets, evaluations) and neo4j-contrib/neo4j-skills 118 d4 (D); GustoBot 413 d62 (component); neo4j-graphrag-python 1,326 d0 (E: README links "Effortless RAG With Text2CypherRetriever"); code-graph-rag 5,303 d0 (E, archive lead: NL-to-Cypher tool); braindb 115 d18. Text-to-SQL siblings outside this definition: WrenAI 18,020 d0; SQLBot 7,034 d1; vanna 23,802 (archived, quiet).
Test 1b. c10b: 52, prior 38 (x1.4); 10 / 9 / 17 / 16; about 70 to 80% on-topic. c10: 57, prior 34; 11 / 8 / 23 / 15. 2610.13648 is an entry to the "Second International TEXT2SPARQL Challenge". Examples (abstracts read): 2610.41755 (20261030) CypherGuard; 2609.36987 (20260929) CypherTurn, EMNLP 2026 oral; 2607.14494 (20260716) SAGA; 2606.27742 (20260626) KG2Cypher; 2602.11745 (20260212) Text2GraphQuery-Bench.
Test 2. Nearest C3. Difference: translate once, engine executes, vs model walks the graph. SAGA abstract: KBQA is approached "through either information retrieval over a question-specific subgraph or semantic parsing into an executable logical form. We study the latter."
Settled (partial): Text2CypherRetriever is a named retriever in Neo4j's official GraphRAG package (README links); CypherGuard sentence above. Research still growing.
Status: passes both (snapshot blind); flag partly productised.
Representative projects (candidates): neo4j-labs/text2cypher; neo4j/neo4j-graphrag-python; vitali87/code-graph-rag.
Fundamental papers (candidates): 2412.10064; 2506.21445; 2512.14277 SPARQL-LLM (20251216); 2602.11745; 2609.36987.

### 4.11 Candidate 11: multimodal graph RAG
Core idea: images, tables and equations become nodes in the same graph as text.
Shift: RAG-Anything abstract (2510.12323, v1 20251014): "existing RAG frameworks are limited to textual content, creating fundamental gaps when processing multimodal documents"; it "reconceptualizes multimodal content as interconnected knowledge entities".
Test 1a. Active n = 4 (3 D, 1 E): HKUDS/RAG-Anything 24,322 d2 (v1.4.4 20261028; 100+ commits; 77 contributors; MIT); jonex 1,522 d2; ApeRAG 1,318 d1; DataMind 456 d7. Quiet: SimpleMem 3,858 d98.
Test 1b. c11: 33, prior 15 (x2.2); 4 / 6 / 9 / 14. c11b: 73, prior 32; 10 / 20 / 16 / 27; about 20 of newest 33 on-topic. Examples (abstracts read): 2610.09360 (20261007) TopoGraphRAG-Bench, NeurIPS; 2607.24861 (20260726) HVM-GraphRAG; 2606.26458 (20260624) MKG-RAG-Bench, KDD 2026; 2512.20626 (v1 20251126) MegaRAG, ACL 2026; 2609.35304 (20260928).
Test 2. Nearest C1. Fails through absorption. LightRAG README (19:37): "[2026.05] Merge RagAnything into LightRAG. Multimodal content parsing and extraction via MinerU / Docling" and "Starting with v1.5, LightRAG seamlessly integrates multimodal processing into its document pipeline and query flow". Same team (HKUDS); RAG-Anything remains active as its own repo.
Settled: absorbed into C1's flagship.
Status: fails Test 2 (merge into C1 as variant: modality parsing); the paper strand is sizable, so a short sub-section is an option.
Representative projects (candidates): HKUDS/RAG-Anything; HKUDS/LightRAG (v1.5 multimodal); apecloud/ApeRAG.
Fundamental papers (candidates): 2510.12323 (before window); 2512.20626; 2512.20136 M3KG-RAG (v1 20251223, CVPR 2026); 2606.26458; 2610.09360.

## 5. New candidates found
| Id | Candidate and shift | Why missing | Evidence |
|---|---|---|---|
| N-A | Agentic search over raw data without a built structure ("from building structure to letting an agent search") | All eleven candidates build something; this is the opposite pole and recurs in 2026 audits | 2608.12888 ReFind (v1 20260813): "builds no semantic structure at all ... highest mean accuracy (58.2) ... above the strongest graph- and tree-based memory systems (HippoRAG 2, 53.2)"; 2610.30755 Raw-RAG (20261022): first in six of seven settings; 2605.15184 "Is Grep All You Need?" (20260514); 2610.41172 (20261030): BM25/grep harness "answers 85% of BrowseComp-Plus ... without compiled or vector indexes"; 2610.34073 Memory Tax (20261025). Probe n4: 151, prior 26 (x5.8), 11 / 31 / 55 / 54, noisy. Anthropic post (20250929). Snapshot: no direct match (ripwire is a call graph): unstated. Overlaps C4, C3 on "who steers" |
| N-B | Knowledge compilation: LLM compiles sources at ingestion into several artifact types | Cuts across C1, C4, C7, C9; one mainstream product now offers the types side by side | RAGFlow README (19:42): "2026-08-19 Introduced Knowledge Compilation to generate Wikis, Graphs, Trees, PageIndex, Mind Maps, Timelines, and Skills"; 2610.41172 (RAGFlow team) also reports "structural artifacts gave no detectable accuracy gain on FRAMES" under a competent harness; 2605.07068 WiCER; 2606.09877; 2608.29612; llm-wiki-compiler ("The knowledge compiler", 2,225 d10). Umbrella or merge frame |
| N-C | Governed, auditable and attackable agent memory | Cross-cutting; grew faster than the field; possibly a theme subchapter | n5 (governance, provenance, audit AND memory/KG in title): 326, prior 41 (x8.0), 19 / 57 / 113 / 137; n9 (poisoning, injection, security): 133, prior 9 (x14.8), 8 / 30 / 49 / 46. Examples: 2610.22959 SAFE-Mem (20261016); 2610.14431 MemForm (20261010); 2610.17719; 2610.37237 GraphRAGProv. Snapshot: trustgraph 2,854 d2 ("Governance Platform for Agents, Knowledge, and Context"), caura, halofy, remnic |
| N-D | Skills as the unit of agent knowledge (procedural memory as SKILL.md files) | Scope question: knowledge for agents, but not facts or documents | n6: 1,106, prior 136 (x8.1); only newest 400 fetched (all Aug to Oct 2026); noisy. 2608.27454 WikiSkill (20260827; Google Research); 2609.25991; 2609.00065. Snapshot: SkillCorpus 694 d1; NVIDIA/skills 3,799 d0; neo4j-skills 118; RAGFlow compiles Skills |
| N-E | RL-trained controllers for retrieval and memory (merge with C3) | C3's technique recurs for memory writes | n8: 183, prior 34 (x5.4), 34 / 39 / 56 / 54, noisy. 2610.29671 Uni-Mem; 2610.21091 MemComposer; 2508.19828 Memory-R1 (20250827) |

Minor probes: hypergraph RAG n1: 31, prior 11, almost all on-topic, a variant of C1/C3 (Hyper-Extract 4,207 d1); GNN/graph-foundation-model retrievers n2: 42, prior 30, noisy; "context graph" wording n11: 34, prior 9, about 8 on-topic, mostly a label (Graphiti, potpie 5,782 d0); memory benchmarks n7: 173, prior 21 (x8.2), an evaluation theme; KGQA with LLMs n10: 66, prior 53, the older line behind C3/C10; repository context files (c7d, 59, prior 2) fit C7 or N-A. Long-context instead of retrieval (n3): probe returned 2 results, inconclusive. Not probed: text-to-SQL and semantic layers (WrenAI 18,020; SQLBot 7,034 in the snapshot).

## 6. Merges proposed
| Merge | Reason | Cost |
|---|---|---|
| C11 into C1 | LightRAG README 2026.05 and v1.5 multimodal; same extraction-to-graph mechanism | Loses a visible paper strand (33 to 73 results) |
| C6 into C5 | Archive lists temporal graphs as one of five memory families; validity handled without graphs too (2606.26511; Mem0 README) | Graphiti (32k stars) is the largest single project; keep a short sub-section |
| C1 and C2 as one shift | C1 is the "from" side; archive tells it as eager-to-lazy-graphs.md; C2's lever is cross-cutting | None found; snapshot supports C2 weakly |
| C3 with N-E | Same technique (RL policy over retrieval or memory operations) | C3 is graph-specific |
| C9 into C1 (variant) or keep as "schema-first" | Same first step; distinct part is schema induction and ontology governance | Ontology-first is active in 2026 (helix-foundry, carrel, ontobricks) |
| Boundary of C4, C7, N-A | All three have a model read or search instead of a vector lookup | Merging hides the structure axis |

## 7. Pointers for the two chosen themes (not tested)
Infrastructure and MCP: 52 of 552 active snapshot descriptions contain "MCP" (lower bound). modelcontextprotocol/servers 91,700 d1. Databases built for agents or GraphRAG: Memgraph, FalkorDB, HelixDB/helix-db 6,255, GrafeoDB/grafeo, namidb, ModernRelay/omnigraph, TuringDB. kuzudb/kuzu archived (d385 in quiet table); Graphiti README lists Kuzu as deprecated.
Graph features removed and added: Mem0 README (19:37) describes entity linking and no graph store (archive lead: graph store removed 20260414, not re-verified). LightRAG added OpenSearch (2026.03) and multimodal (2026.05). GraphRAG entered maintenance mode (20260814). Graphify moved MIT to Apache-2.0 on 20260722 (archive lead, not re-verified) and leads its README with Graphify Cloud. Graphiti deprecated Kuzu.

## 8. Gaps and cautions
1. Snapshot recall (1.1): C3, C4, C6, C9, C10, C11 are lower bounds; C5 is capped; low-star October 2026 repos are missing.
2. Push date versus work: only 124 rows have commit counts; several "active" repos have almost no commits (autoflow 0, llm-graph-builder 1, m_flow 1).
3. Tagging is mine: D, E, C rest on 120-character descriptions plus the READMEs I fetched; the C5 (117) and C7 (58) estimates have wide ranges.
4. arXiv: keyword search misses papers and includes unrelated ones (precision 36% to 97% by query); stop-word phrases broke two queries; abstracts only, no full papers.
5. Growth ratios use v1 dates and one control per topic; small prior counts make them unstable.
6. Archive leads not re-verified: Neo4j llm-graph-builder banner; Mem0 graph-store removal date; Graphify licence change; Letta MemFS and retired server; Anthropic memory tool; BM25 Wins at Scale (2607.26497) and GraphRAG-Bench tables; Dify Agent Knowledge Base.
7. Stars and fast-growth are signals; star timelines not checked.
8. The snapshot is 3 days older than my reads; alphaXiv gave no timestamps.
9. Not done: no ranking or recommendation on the final list; no probe for text-to-SQL, licence trends, or a conclusive long-context-versus-RAG query.

## Appendix A: primary queries (arXiv API, window 20251102 to 20261102)
| Id | Query | N | Prior | P1 / P2 / P3 / P4 | Read (UTC 20261102) |
|---|---|---|---|---|---|
| c0 | abs:GraphRAG OR abs:"graph rag" OR abs:"graph-based RAG" OR abs:"graph retrieval-augmented" OR abs:"graph retrieval augmented" OR ti:GraphRAG | 272 | 167 | 45 / 66 / 84 / 77 | 19:26 |
| c1 | (abs:GraphRAG OR abs:"graph rag" OR abs:"graph-based RAG") AND (abs:"graph construction" OR abs:"knowledge graph construction" OR abs:"graph index" OR abs:"graph indexing" OR abs:"entity extraction" OR abs:"extract entities" OR abs:"entities and relations" OR abs:"entity-relation") | 48 | 29 | 10 / 8 / 17 / 13 | 19:26 |
| c2c | (abs:"LLM-free" OR abs:"zero-token" OR abs:"token-free" OR abs:"extraction-free" OR abs:"CPU-only" OR abs:"indexing cost" OR abs:"construction cost" OR abs:"cost-efficient" OR abs:"cost-effective" OR abs:lightweight) AND (abs:GraphRAG OR abs:"graph rag" OR abs:"graph-based RAG") | 32 | 13 | 6 / 10 / 7 / 9 | 19:44 |
| c3b | (abs:"reinforcement learning" OR abs:GRPO OR abs:"policy optimization") AND (abs:"knowledge graph" OR abs:GraphRAG OR abs:"graph retrieval" OR abs:"graph-based RAG") AND (abs:agent OR abs:agentic OR abs:"multi-turn") | 44 | 18 | 13 / 7 / 14 / 10 | 19:31 |
| c4d | (abs:vectorless OR abs:"embedding-free" OR abs:"vector-free" OR abs:"reasoning-based retrieval" OR abs:"reasoning-based RAG" OR abs:PageIndex OR abs:"non-vector" OR abs:"index-free") AND (abs:RAG OR abs:retrieval) | 19 | 4 | 3 / 3 / 4 / 9 | 19:45 |
| c5_full | (ti:"agent memory" OR ti:"memory for agents" OR ti:"memory for LLM agents" OR ti:"memory for AI agents" OR ti:"agentic memory" OR ti:"memory system" OR ti:"memory architecture" OR ti:"long-term memory" OR ti:"memory layer") AND (abs:agent OR abs:agents OR abs:LLM OR abs:"language model") | 482 | 53 | 58 / 86 / 165 / 173 | 19:31 |
| c6 | (abs:"temporal knowledge graph" OR abs:"temporal graph" OR abs:"bi-temporal" OR abs:"temporal knowledge graphs") AND abs:memory AND (abs:LLM OR abs:agent OR abs:agents OR abs:"language model") | 21 | 2 | 3 / 2 / 11 / 5 | 19:27 |
| c7b | (abs:"LLM wiki" OR abs:"LLM-wiki" OR abs:"LLM-maintained wiki" OR abs:"LLM-compiled wiki" OR abs:"LLM-built wiki" OR abs:"LLM-curated wiki" OR abs:"wiki-based memory" OR ti:wiki) AND (abs:LLM OR abs:agent OR abs:agents) | 21 | 0 | 0 / 3 / 11 / 7 | 19:32 |
| c7d | abs:"AGENTS.md" OR abs:"CLAUDE.md" OR abs:cursorrules OR abs:"context files" OR abs:"instruction files" OR ti:"context files" OR ti:"AGENTS.md" | 59 | 2 | 2 / 8 / 18 / 31 | 19:45 |
| c8c | (abs:"code graph" OR abs:"code graphs" OR abs:"repository graph" OR abs:"code knowledge graph" OR abs:"call graph") AND (abs:"coding agent" OR abs:"coding agents" OR abs:"code agent" OR abs:"code agents" OR abs:"software engineering agent") | 13 | 1 | 0 / 2 / 3 / 8 | 19:45 |
| c9 | (abs:"schema induction" OR abs:"ontology induction" OR abs:"schema-free" OR abs:"schema generation" OR abs:"ontology generation" OR abs:"knowledge graph construction" OR abs:"ontology learning" OR abs:"schema discovery") AND (abs:LLM OR abs:LLMs OR abs:"large language model" OR abs:"large language models") | 75 | 64 | 21 / 11 / 24 / 19 | 19:27 |
| c10b | ti:Cypher OR ti:SPARQL OR ti:Text2Cypher OR ti:"Text-to-Cypher" OR ti:Text2SPARQL OR ti:"Text-to-SPARQL" OR ti:NL2SPARQL OR ti:NL2Cypher OR ti:"graph query" | 52 | 38 | 10 / 9 / 17 / 16 | 19:33 |
| c11 | (abs:multimodal OR abs:multi-modal) AND (abs:GraphRAG OR abs:"graph rag" OR abs:"graph-based RAG" OR abs:"multimodal knowledge graph" OR abs:"multi-modal knowledge graph") AND (abs:retrieval OR abs:RAG OR abs:"retrieval-augmented") | 33 | 15 | 4 / 6 / 9 / 14 | 19:27 |

Other queries (strings in scripts/spec*.json), N/prior: c2 39/24; c3 259/111; c4 18/5; c4c 82/32; c5b 122/15; c6b 85/22; c6c 96/10; c7 77/8; c7c 39/6; c8 52/15; c8b 63/16; c9b 116/50; c10 57/34; c11b 73/32; n1 31/11; n2 42/30; n3 2/1; n4 151/26; n5 326/41; n6 1,106/136 (400 fetched); n7 173/21; n8 183/34; n9 133/9; n10 66/53; n11 34/9. Discarded: c2b 928/530; c4b 1,011/529. Controls: LLM 44,692/32,396; RAG 3,357/2,736; agents 15,158/6,068.

## Appendix B: files on disk (absolute paths)
Base folder: <scratch folder>/step0-trends/
- scripts/ (classify.py, rx_multi.py, rx_sample.py, arxiv_run2.py, period_table.py, overlap.py, created_hist.py, spec1.json to spec6_ids.json)
- out/ (active.txt, quiet.txt, classify_out.txt, arxiv*.log, lazygraphrag.txt, graphrag_methods.txt, anthropic_ctx.txt)
- arxiv1/ to arxiv6/ (parsed JSON; dl/<qid>/ raw XML); dl-gh/<name>/ (GitHub downloads); dl-web/<name>/ (web pages); dl-arxiv-test/ (my first connectivity test)