---
slug: minirag
repo: HKUDS/MiniRAG
tier: deep
category: core
snapshot: 20261030 18:58 UTC
---

# MiniRAG

| | |
|---|---|
| Repository | https://github.com/HKUDS/MiniRAG |
| Licence | MIT, from the `LICENSE` file (copyright line: "2024 Gustavo Ye"). The README carries no licence badge, so there is nothing to disagree with. [4][5] |
| Language | Python [1] |
| Stars, forks | 2,026 stars, 258 forks (read 20261030 18:58 UTC) [1] |
| Open issues and pull requests | 59 as the API counts them: 29 issues and 30 pull requests (read 20261030 19:01 UTC) [1][13] |
| Created, last push | 20250111 13:24 UTC, 20251016 07:43 UTC [1] |
| Latest release | `v0.0.2`, published 20250227 09:11 UTC; the only other tag is `v0.0.1` [2] |
| Status | quiet. The last push is 379 days before the snapshot; no commit since 20260801 (0 returned, read 20261030 18:58 UTC). Not archived. [1][3] |
| Paper, docs | arXiv 2501.06713 (v3, 20250126) [9]; ACL 2026 version, ACL Anthology 2026.acl-long.1721 [11]; benchmark LiHua-World in the repository [8] |

## What it is

MiniRAG is a RAG framework from the HKUDS GitHub organisation (University of Hong Kong, per the paper's
author affiliation, which also hosts LightRAG), designed so that small language models (SLMs, 1.5B to
4B parameters in the paper) can both build and query a graph index [5][10]. The README says the code is
based on LightRAG and names nano-graphrag as a foundation [5]. The paper's two ideas are a *semantic-aware heterogeneous graph* that
holds text-chunk nodes and named-entity nodes together, so raw chunks stay retrievable and the SLM does
not have to summarise well, and a *topology-enhanced retrieval* that replaces precise semantic matching
(which SLMs do badly) with entity matching plus path and edge counting on the graph [10][12]. It also
introduces the LiHua-World benchmark [5][8].

The codebase is a small LightRAG derivative. A `MiniRAG` dataclass in `minirag/minirag.py` sits over
pluggable storages defined in `minirag/base.py`. The directory `minirag/kg/` holds implementations for
JSON key-value, NanoVectorDB, NetworkX, Neo4j, PostgreSQL, Milvus, MongoDB, Redis, Weaviate, Chroma,
Oracle, Gremlin and Apache AGE; no file named for TiDB is in that listing, although the README news
item lists TiDB among supported databases [5][6][7]. The default `llm_model_name` in the dataclass is
`meta-llama/Llama-3.2-1B-Instruct`; `llm_model_func` and `embedding_func` default to `None` and the
caller must supply them [6]. The package is `minirag-hku`, version `0.0.2` [7].

Three titles are in use for one work. The arXiv paper, README and `pyproject.toml` say "MiniRAG: Towards
Extremely Simple Retrieval-Augmented Generation" [5][7][9]. The ACL Anthology entry says "MiniRAG: A
Lightweight RAG system with Small Language Models" [11]. The GitHub description now says
`[ACL2026] "MiniRAG: Making RAG Simpler with Small and Open-Sourced Language Models"` [1].

## How it works

### The heterogeneous graph

The paper defines the graph as `G = ({V_c, V_e}, {E_alpha, (e_beta, d_e_beta) in E_beta})` (Eq. 1; §2.1 in
arXiv v3, §3.1 in the ACL version) [10][12].

- **Nodes.** Text chunks `V_c` (1200 tokens, 100 overlap) and named entities `V_e`. Chunk size and
  overlap are the dataclass defaults and match the paper's implementation details [6][12]. Entity
  nodes carry name, type and an LLM-written description; the default types are
  `["organization", "person", "location", "event"]` (`PROMPTS["DEFAULT_ENTITY_TYPES"]`) [6].
- **Edges.** Entity-entity edges `E_alpha` carry an LLM description, keywords and a numeric strength.
  Entity-chunk edges `E_beta` carry a text description `d_e_beta` of the entity in that chunk [10][12].
- **In code**, entity-chunk edges are not explicit graph edges. Provenance `source_id` fields (chunk
  hashes joined by the `<SEP>` separator `GRAPH_FIELD_SEP`) on every node and edge play that role;
  `_merge_nodes_then_upsert` and `_merge_edges_then_upsert` in `minirag/operate.py` build them [6].
- **Vector indexes.** `minirag_query` takes four: `entities_vdb`, `entity_name_vdb`, `relationships_vdb` and
  `chunks_vdb` [6]. The July investigation read their contents as entity name plus description
  (`entities_vdb`), entity name only (`entity_name_vdb`, the query-side workhorse), relationship keywords
  plus source, target and description (`relationships_vdb`) and chunk text (`chunks_vdb`); in this run
  `extract_entities` was confirmed to upsert into `entity_name_vdb` and `relationships_vdb`, and the other
  two were not traced. Embeddings come from whatever model the caller plugs in; the paper uses
  `all-MiniLM-L6-v2` in the SLM setting and `text-embedding-3-small` with `gpt-4o-mini` [12].

### What the small model does at index time

`extract_entities` in `minirag/operate.py` runs per 1200-token chunk [6]:

1. One LLM call with `PROMPTS["entity_extraction"]`. The shipped prompt is the full LightRAG/GraphRAG-style
   one: entity name, type and description, plus relationships with description, keywords and strength,
   plus content keywords [6]. The paper says the indexing "focuses on basic entity extraction and
   heterogeneous relationship mapping" and that descriptions are generated for entity-chunk edges [10][12],
   so the code and the paper's "simple extraction" framing diverge. A commented-out line in
   `operate.py` refers to `PROMPTS["entity_extraction_noDes"]`; no such prompt is defined in
   `prompt.py` (searched 20261030 19:03 UTC) [6].
2. A gleaning loop. `entity_extract_max_gleaning` defaults to `1`. With that value the loop runs once:
   one continuation call (the "MANY entities were missed" prompt), then it breaks **before** the yes/no
   `entiti_if_loop_extraction` call, which is reached only when the setting is 2 or more [6]. So the
   default is **2 LLM calls per chunk**, plus summarisation calls (below). The July investigation
   counted 2 to 3; see the changes section.
3. Delimiter parsing. Output is a tuple format (`("entity"<|>NAME<|>type<|>description)` records separated
   by delimiters, `DEFAULT_TUPLE_DELIMITER` is `<|>`), parsed by pattern matching rather than JSON, so
   it tolerates sloppy SLM output [6]. Duplicates are merged across chunks; descriptions longer than
   `entity_summary_to_max_tokens` (default 500) trigger an LLM summarisation call [6].
4. `enable_llm_cache` defaults to `True`, and the class creates an LLM response cache when it is on [6].
   The July investigation read this as making re-runs over unchanged input free; the cache-lookup logic
   was not re-read in this run. Incremental insertion with document-status tracking exists
   (`doc_status_storage` defaults to `JsonDocStatusStorage`) [6]; the July notes also name
   `apipeline_enqueue_documents` and `apipeline_process_enqueue_documents` (content-hash de-duplication),
   which were not re-checked.

The paper's Fig. 2 (arXiv v3) is a single worked example, not a measurement: for the entity
"HOUSE RULES" both `gpt-4o-mini` and Phi-3.5-mini name the entity, Phi-3.5-mini's description "lacks
specific details", and in the answering step Phi-3.5-mini replies "I don't have enough information" where
`gpt-4o-mini` answers [10]. The design is meant to survive weak descriptions because retrieval leans on
names, types and topology rather than description quality [10]. Whether 1 to 4B models can run the
pipeline is supported by Table 1: the indexes built and queried by GLM-Edge-1.5B and Phi-3.5-mini (3.8B)
score within about one point of each other on LiHua-World (arXiv v3: 52.51 vs 53.29; ACL: 51.65 vs
50.71) [10][12]. In the paper's setup one model does everything: "using a single model to construct the index, generate search queries, and answer
questions" [12]. A small indexer paired with a different, stronger answering model is not a configuration
the paper reports (unstated).

### How retrieval works

`minirag_query` calls `_build_mini_query_context` in `minirag/operate.py` [6]. The paper describes it in
§2.2 (arXiv v3) and §3.2 (ACL) with Eq. 2 (edge relevance `omega_e`: a count of seed and answer nodes inside
the k-hop subgraph around an edge) and Eq. 3 (path score
`omega_p = omega_v * (1 + sum omega_e + sum count)`) [10][12]. The code does this:

1. **One SLM call** with `PROMPTS["minirag_query2kwd"]` returns JSON with `answer_type_keywords` (at most 3,
   chosen from the graph's own pool of observed types) and `entities_from_query`. It is parsed with
   `json_repair` [6].
2. Each query entity is looked up in `entity_name_vdb` (top-k); the hits are the seed nodes [6].
3. `get_neighbors_within_k_hops(key, 2)` collects paths for each seed. Seeds with no path are dropped
   except the top 20% by score (minimum 1) [6].
4. `get_node_from_types` returns candidate answer nodes for the predicted types; each path is scored by how
   many of them it contains (`cal_path_score_list` in `minirag/utils.py`) [6].
5. `relationships_vdb` is queried with the raw query. Edges touching seed or answer entities vote for the
   paths that contain them (`edge_vote_path`, `minirag/utils.py`) [6].
6. `path2chunk` maps paths to chunk ids through `source_id`, with `max_chunks=3`. For a node with more than
   5 associated text units it keeps the best `max(5, n/2)` by `calculate_similarity`, whose default
   method is `"levenshtein"` (string edit distance on entity descriptions, not embeddings) [6].
7. `kwd2chunk` counts votes per chunk id. The first scored path of each query entity is weighted x2. If a
   path's first chunk id is also among the top dense hits of `chunks_vdb`, the path's score is
   multiplied by 10 and that score is added to every chunk id in the path. `chunks_vdb` is queried with
   `top_k / 2`, and `top_k / 2` chunks are kept [6]. The constants are hard-coded.
8. The context is an entities table plus a sources (chunks) table, passed to one generation call [6]
   (the generation call itself was not re-read in this run).

So query time uses two LLM calls (keyword extraction, then the answer), a bounded 2-hop walk and counting;
there is no personalised PageRank and no beam search [6]. Dense retrieval and graph voting are fused at
step 7. The ACL text describes the final chunk step as a similarity between the query and the
concatenation of chunk and edge descriptions, over candidates in the intersection of path-linked chunks
and the path set [12]; the code read here uses vote counting and Levenshtein filtering instead, and no
embedding of that concatenation was found (not exhaustively searched). The paper's hyperparameters are
path length `n` and `k` (used for the k-hop subgraph and for top-k paths); the code fixes 2 hops [6][12].

## Cost and operating profile

- **Index-time LLM calls.** 2 per chunk at the default settings (initial extraction and one gleaning
  call) plus summarisation calls for long entity descriptions [6]. The cost is time, not money, with a
  local model. No measured per-chunk time is given in the sources.
- **Measured indexing time (ACL Table 3).** Cumulative total time 146 s at document index 5, 608 s at 10,
  943 s at 15, 1181 s at 20, 1418 s at 25, 1816 s at 30 and 2153 s at 35. The paper reads this as linear
  growth. The model, hardware and document sizes for this table are unstated ("varying document sizes"
  only) [12]. Not measurable from the paper: any index time for a corpus of a given token count.
- **Rebuilds.** The LLM response cache (`enable_llm_cache`) is on by default [6]; see the caveat on cache
  lookup above.
- **Storage.** The paper claims 25% of the storage of "baselines like LightRAG w/ gpt-4o-mini" at
  competitive accuracy (abstract, §3.2 text and Fig. 3 in arXiv v3, §4.5 and Fig. 2 in ACL) [10][12]. The ACL
  version defines storage as "the additional storage overhead introduced by the method, including generated
  edges, node descriptions, vector indexes, and method-specific artifacts such as community reports and
  clustering metadata in GraphRAG" [12]. The text gives no absolute size; the figure content was not
  readable in this run.
- **Query latency (ACL Table A6, end-to-end inference, seconds; per-query or total unstated).**

  | Model | NaiveRAG | LightRAG | MiniRAG | GraphRAG |
  |---|---|---|---|---|
  | gpt-4o-mini | 6.444 | 47.780 | 51.713 | 59.134 |
  | Phi-3.5 | 28.459 | 62.301 | 67.497 | N/A |

  MiniRAG's latency is close to LightRAG's and above the chunk-only baseline [12]. The paper's own wording
  is "inference speed comparable to that of LightRAG" [12].
- **What it needs.** Python 3.9 or later [7]. Defaults need no database: JSON, NanoVectorDB and NetworkX
  files in a working directory [6]. Docker and a FastAPI server exist (see below) [7]. An LLM function and
  an embedding function must be supplied [6]. The paper's experiments ran on 64 Intel Xeon Silver 4314 CPU
  cores and four RTX 3090 GPUs [12]. Fully local operation is possible in principle (the SLM setting uses
  open models and a sentence-transformer embedder [12]); the paper does not report a run on a phone,
  laptop or other constrained device (unstated).
- **How an agent talks to it.** A Python library call (`MiniRAG(...)`, `insert`, `query`) and an optional
  FastAPI server, `minirag/api/minirag_server.py`, which mixes LLM and embedding bindings (Ollama,
  OpenAI-style, Azure OpenAI) [7]. A search for "mcp" in the repository returned no result (GitHub code
  search, 20261030 19:01 UTC), and the API README does not mention MCP [7][13].
- **Installation caveat.** The README's install-from-PyPI instruction reads `pip install lightrag-hku`,
  the LightRAG package, while its news item says `pip install minirag-hku`; `pyproject.toml` names the
  package `minirag-hku` [5][7].

## Evidence

All results below are the authors' own; no third-party evaluation of MiniRAG was found in the sources
read. The judge is `GPT-4o`; each evaluation was repeated three times with order randomisation [12].
The arXiv v3 introduction claims "1.3-2.5x higher effectiveness while using only 25% of the storage
space" than existing lightweight RAG systems, an accuracy reduction "from merely 0.8% to 20%" when moving
from LLMs to SLMs, and that MiniRAG "consistently achieves state-of-the-art performance across all
evaluation settings" [10]. The last claim does not match that paper's own Table 1, where LightRAG leads
with `gpt-4o-mini` on LiHua-World (below).

### LiHua-World, accuracy (%)

LiHua-World is the authors' benchmark: one year of chat records of a virtual user, with single-hop,
multi-hop and summary questions, each with a manually annotated answer and supporting documents [5][8].
Question counts are unstated in the README files read.

**arXiv v3 Table 1 (identical to the README table)** [5][10]:

| Model | NaiveRAG | GraphRAG | LightRAG | MiniRAG |
|---|---|---|---|---|
| Phi-3.5-mini (3.8B) | 41.22 | fails | 39.81 | **53.29** |
| GLM-Edge-1.5B | 42.79 | fails | 35.74 | **52.51** |
| Qwen2.5-3B | 43.73 | fails | 39.18 | **48.75** |
| MiniCPM3-4B | 43.42 | fails | 35.42 | **51.25** |
| gpt-4o-mini | 46.55 | 35.27 | **56.90** | 54.08 |

MiniRAG minus NaiveRAG: +12.07, +9.72, +5.02, +7.83 for the four SLMs, and +7.53 with gpt-4o-mini
(computed from the table).

**ACL 2026 Table 1** (means; the paper also prints standard deviations of roughly 2 to 6 points, for
example MiniRAG with gpt-4o-mini 52.28 +/- 3.14). The baselines changed: a BM25 column takes the place of
the NaiveRAG column (Table A5 labels it "NaiveRAG (BM25)", while Table A1 lists NaiveRAG and BM25 as
separate methods; the paper does not reconcile the two), and RAPTOR and HippoRAG v2 are added [12]:

| Model | BM25 | RAPTOR | HippoRAG v2 | GraphRAG | LightRAG | MiniRAG |
|---|---|---|---|---|---|---|
| Phi-3.5-mini | 41.60 | 37.23 | 36.77 | fails | 40.03 | **50.71** |
| GLM-Edge-1.5B | 42.39 | 43.20 | 33.92 | fails | 34.85 | **51.65** |
| Qwen2.5-3B | 40.97 | 37.49 | 36.58 | fails | 41.76 | **46.78** |
| MiniCPM3-4B | 41.44 | 41.76 | 35.79 | fails | 36.26 | **51.18** |
| gpt-4o-mini | 42.54 | 52.62 | **66.28** | 37.68 | 55.89 | 52.28 |

MiniRAG minus BM25: +9.11, +9.26, +5.81, +9.74 for the SLMs and +9.74 with gpt-4o-mini (computed). With
gpt-4o-mini, HippoRAG v2 leads MiniRAG by 14.0 points; LightRAG (55.89) leads by 3.6 and RAPTOR (52.62)
by 0.3, both within about one standard deviation. With the SLMs, HippoRAG v2 is below BM25 in every
row [12].

### MultiHop-RAG and 2WikiMultihopQA, accuracy (%)

arXiv v3, MultiHop-RAG [5][10]: with SLMs MiniRAG scores 47.77 to 51.41 against NaiveRAG 39.24 to 44.44,
while LightRAG scores 19.48 to 27.03 or fails; with gpt-4o-mini MiniRAG scores 68.43 against LightRAG
64.91, GraphRAG 60.92 and NaiveRAG 53.60.

ACL Table 1 [12]:

| MultiHop-RAG | BM25 | RAPTOR | HippoRAG v2 | GraphRAG | LightRAG | MiniRAG |
|---|---|---|---|---|---|---|
| Phi-3.5-mini | 38.03 | 40.15 | 30.58 | fails | 26.76 | **52.74** |
| GLM-Edge-1.5B | 41.55 | 42.59 | 38.51 | fails | fails | **52.39** |
| Qwen2.5-3B | 38.58 | 39.50 | 38.56 | fails | 21.87 | **50.94** |
| MiniCPM3-4B | 41.90 | 44.78 | 37.12 | fails | 19.99 | **50.23** |
| gpt-4o-mini | 39.79 | 56.42 | **72.46** | 59.27 | 66.55 | 68.54 |

| 2WikiMultihopQA | BM25 | RAPTOR | HippoRAG v2 | GraphRAG | LightRAG | MiniRAG |
|---|---|---|---|---|---|---|
| Phi-3.5-mini | 44.42 | 44.86 | 36.65 | fails | 24.21 | **45.91** |
| GLM-Edge-1.5B | 47.08 | 44.77 | 39.20 | fails | fails | **53.26** |
| Qwen2.5-3B | 46.32 | 43.80 | 45.02 | fails | 28.29 | **52.30** |
| MiniCPM3-4B | 42.84 | 45.69 | 37.58 | 29.72 | 22.55 | **59.92** |
| gpt-4o-mini | 44.08 | 63.72 | **72.36** | 55.22 | 62.37 | 61.67 |

Appendix A.1 (ACL), Phi-3.5-mini as base model, 500-question corpora and 100 test questions each: Natural
Questions NaiveRAG 49, LightRAG 37, MiniRAG 63, BM25 57, Contriever 53, ColBERTv2 60, direct `gpt-4o` 56;
TriviaQA NaiveRAG 74, LightRAG 50, MiniRAG 78, BM25 76, Contriever 73, ColBERTv2 76, direct `gpt-4o` 69 (%).
On NQ, ColBERTv2 (60) and BM25 (57) are not far below MiniRAG (63) on 100 test questions [12].

### Where it loses, and where the evidence is thin

- With a strong model on LiHua-World, other graph methods beat it: LightRAG in the arXiv table (56.90 vs
  54.08), and in the ACL table HippoRAG v2 (66.28), LightRAG (55.89) and RAPTOR (52.62) against 52.28 [10][12].
  The paper's Limitations section says that when other methods and MiniRAG both use larger API-based
  models "the performance advantage may diminish" [12].
- MiniRAG's gap over the chunk-only baseline did **not** shrink with the strong model on LiHua-World (+7.5
  over NaiveRAG, +9.7 over BM25, against +5.0 to +12.1 and +5.8 to +9.7 for the SLMs). What disappears is
  its lead over the other graph methods (computed from the tables above).
- Error rates are sometimes higher than the chunk-only baseline's: Qwen2.5-3B on MultiHop-RAG 33.10 vs 31.69
  (arXiv v3); on LiHua-World MiniCPM3-4B 21.79 vs 17.08 [5][10]. Abstention ("I don't know") on
  MultiHop-RAG is lowest for MiniRAG with SLMs (13.6 to 26.4%) against 62.4 to 67.6% for LightRAG (ACL
  Table A5) [12]; the paper reads this as better use of retrieved context.
- The MiniRAG query path has no community-report or global-summary stage; the inherited LightRAG query
  functions (`local_query`, `global_query`, `hybrid_query`, `naive_query`) remain in `operate.py` [6].
  The tables read report accuracy in aggregate, with no breakdown by question type (single-hop,
  multi-hop, summary) [10][12]. The Limitations section names English-only evaluation, a benchmark that "may lead to a
  mismatch" with real user needs, and the privacy risk of an explicit entity-relation graph stored on a
  device [12].
- Each cell rests on a small test set (100 questions for the appendix datasets; main-table sizes are
  unstated in the sources read), and standard deviations across three judge repeats are 2 to 6 points.
- Judge reliability (ACL §4.2): GPT-4o self-agreement 98%; GPT-4o and Claude-3.7-Sonnet agreed on 93% of
  100 sampled pairs; against three PhD-student raters, 28 of 30 GPT-4o "correct" and 30 of 30 "incorrect"
  labels were confirmed [12].

### Ablations (LiHua-World, accuracy %)

| Variant | arXiv v3 Table 2 (4 SLMs) | ACL Table 2 (4 SLMs) |
|---|---|---|
| Full MiniRAG | 53.29, 52.51, 48.75, 51.25 | 50.71, 51.65, 46.93, 51.18 |
| `-I` (description-driven indexing, as in LightRAG/GraphRAG) | 26.02, 25.08, 24.14, 26.18 | 28.26, 26.84, 21.66, 24.96 |
| `-R_chunk` (chunk nodes removed) | 48.90, 46.24, 40.91, 46.39 (loses 4.4 to 7.8) | 47.88, 45.05, 42.07, 47.10 (loses 2.8 to 6.6) |
| `-R_edge` (edge voting removed) | 50.47, 47.81, 48.43, 48.59 (loses 0.3 to 4.7) | 47.57, 45.53, 45.05, 46.62 (loses 1.9 to 6.1) |

Sources [10][12]; the "loses" ranges are computed. The ACL table prints Qwen2.5-3B MiniRAG as 46.93 in
Table 2 and 46.78 in Table 1. The `-I` variant roughly halves accuracy, which the authors read as SLMs
being unable to do description-based indexing. The paper does not say how `-I` was implemented, and the
shipped code still extracts descriptions (above), so `-I` is not a test of "descriptions removed" alone
(unstated). Sensitivity (ACL A.3, dataset and model unstated): accuracy 48, 54, 64% for k = 4, 10, 50; 52,
54, 50% for path length n = 2, 4, 8 [12].

## Direction

No roadmap file is in the repository (root listing, 20261030 18:58 UTC) [5][7]. The last commits are
README, `Communication.md`, translated READMEs and asset uploads, the latest on 20251016 [3]. The
README's news section ends on 20250227 [5]. Since 20260801 there are no commits [3]. The one
visible movement in 2026 is publication: the ACL 2026 camera-ready appeared in the ACL Anthology in July 2026
under a new title with a changed results table (below), and the GitHub description was updated to say
"ACL2026" [1][11][12]. Whether the ACL results can be reproduced with the code in the repository is
unstated.

## Changed since the July 2026 investigation

The July investigation (20260726 08:52 UTC) recorded about 2.0k stars, 255 forks, 36 open issues, licence
MIT, created 20250111, last push 20251016, status quiet. Checked 20261030 18:58 to 19:03 UTC:

**Repository**

- Stars 2,026 (from about 2.0k), forks 258 (from 255). Open count 59, made of 29 issues and 30 pull
  requests; July's "36 open issues" has an unstated basis, and the API figure includes pull requests, so
  the two are not comparable. No issue was created after 20260726 (search returned 0) [1][13].
- No push since 20251016 (379 days at the snapshot) and 0 commits since 20260801. Still quiet [1][3].
- Licence: MIT, unchanged, confirmed from the `LICENSE` file [4]. Not archived, not renamed (`full_name` is
  still `HKUDS/MiniRAG`), not a fork [1]. Latest release still `v0.0.2` (20250227) [2]. No successor
  project is named in the README or description; the HKUDS organisation was not searched for one
  (unstated).
- The README is unchanged in substance: title, citation block (arXiv only) and Table 1 still show the
  arXiv-era numbers, and its code-structure listing names `minirag/storage.py`, which is not in the
  repository [5][7].

**Paper**

- The ACL 2026 camera-ready (July 2026, pages 37121 to 37144) is a changed paper: new title; baselines RAPTOR and
  HippoRAG v2 added and a BM25 column in place of NaiveRAG; 2WikiMultihopQA added to the main text and NQ,
  TriviaQA to the appendix; means with standard deviations from three judge repeats; a judge-reliability
  study; an abstention analysis; latency and indexing-time tables; sensitivity analysis. The method text is
  the same two components, with section numbers 3.1 and 3.2 [11][12]. arXiv still shows v3 (20250126) with
  no comment field [9].

**July claims corrected in the body above**

- **"~2 to 3 LLM calls per chunk, gleaning gated by a yes/no call."** Wrong for the default settings. With
  `entity_extract_max_gleaning=1` the code makes 2 calls per chunk and never reaches the yes/no call. The
  code has not changed since 20251016, so this was a July misreading, not a repository change [6].
- **"A `entity_extraction_noDes` variant sits commented out."** Only a commented-out reference exists in
  `operate.py`; the prompt is not defined in `prompt.py` [6].
- **"With gpt-4o-mini MiniRAG wins outright on MultiHop-RAG (68.4 vs LightRAG 64.9)."** True of the
  arXiv table. In the ACL table HippoRAG v2 scores 72.46 against MiniRAG's 68.54 [12].
- **"Builds a graph that lifts accuracy ~9 to 13 points over chunk-only retrieval."** Only two of the four SLMs
  fall in that range (arXiv v3: +12.07, +9.72, +5.02, +7.83; ACL vs BM25: +5.81 to +9.74).
- **"The gap shrinks with a strong reader."** Not supported on LiHua-World (above): the gap over the
  chunk-only baseline is the same size. The supported statement is that other graph methods overtake it.
- **"Query compute: cheap."** The ACL latency table puts MiniRAG near LightRAG and above the chunk-only
  baseline (above).
- **"GLM-Edge-1.5B builds an index that scores 52.5%."** In the paper the same model also answers; the
  score is for the combined role (above).

**Open**

- Storage: still a single percentage with no absolute figure in the text.
- Whether the ACL numbers are reproducible with the published repository code, and how `-I` was
  implemented: unstated.

## Sources

1. https://api.github.com/repos/HKUDS/MiniRAG (GitHub REST API repository record): stars, forks, licence key, archived flag, created and pushed dates, description, homepage, default branch, language, open count (read 20261030 18:58 UTC)
2. https://github.com/HKUDS/MiniRAG/releases (API: latest release and tags): `v0.0.2`, `v0.0.1` (read 20261030 18:58 UTC)
3. https://github.com/HKUDS/MiniRAG/commits/main (API commit list, `since=2026-08-01` and latest 8): 0 commits since 20260801, last commit 20251016 (read 20261030 18:58 UTC)
4. https://github.com/HKUDS/MiniRAG/blob/main/LICENSE: MIT text, copyright 2024 Gustavo Ye (read 20261030 18:58 UTC)
5. https://github.com/HKUDS/MiniRAG/blob/main/README.md: abstract, news, install, Table 1, code structure, citation, acknowledgements (read 20261030 18:59 UTC)
6. https://github.com/HKUDS/MiniRAG/tree/main/minirag (`minirag.py`, `operate.py`, `utils.py`, `prompt.py` at the last commit `e204d23942`): defaults, `extract_entities`, `_build_mini_query_context`, `path2chunk`, `kwd2chunk`, `minirag_query`, prompts (read 20261030 18:59 to 19:03 UTC)
7. https://github.com/HKUDS/MiniRAG (directory listings, `minirag/api/README.md`, `pyproject.toml`, `requirements.txt`): storage bindings, API server, package metadata, Python version (read 20261030 19:02 UTC)
8. https://github.com/HKUDS/MiniRAG/blob/main/dataset/LiHua-World/README.md: LiHua-World description and question types (read 20261030 19:03 UTC)
9. https://arxiv.org/abs/2501.06713: title, versions v1 to v3 and dates, no comment field (read 20261030 18:59 UTC)
10. https://arxiv.org/pdf/2501.06713v3: sections, Eq. 1 to 3, Tables 1 and 2, storage claim (read 20261030 19:01 UTC)
11. https://aclanthology.org/2026.acl-long.1721/: ACL 2026 title, venue, pages, DOI 10.18653/v1/2026.acl-long.1721 (read 20261030 19:00 UTC)
12. https://aclanthology.org/2026.acl-long.1721.pdf: ACL camera-ready text, Tables 1 to 3, A1 to A6, implementation details, limitations (read 20261030 19:00 UTC)
13. https://api.github.com/search/issues and /repos/HKUDS/MiniRAG/contributors (GitHub REST API): open issue and pull request counts, 15 contributors listed, no issue created after 20260726, no code-search hit for "mcp" (read 20261030 19:01 UTC)
