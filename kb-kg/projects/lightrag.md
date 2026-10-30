---
slug: lightrag
repo: HKUDS/LightRAG
tier: deep
category: core
snapshot: 20261030 18:58 UTC
---

# LightRAG

Reading times: the repository metadata, release list, licence file and README were read at
20261030 18:58 UTC; the source files and directory listings between 19:01 and 19:02 UTC; the arXiv page
and the sibling repositories at 19:02 UTC. Each source below carries its own time.

| | |
|---|---|
| Repository | https://github.com/HKUDS/LightRAG |
| Licence | MIT, from the `LICENSE` file ("Copyright (c) 2025 LightRAG Team") [3]. GitHub's API also reports MIT [1]. The README names no licence, so there is no badge to disagree [4]. |
| Language | Python (GitHub's primary language) [1]; the WebUI is a separate frontend under `lightrag_webui/` [5] |
| Stars, forks | 40,443 and 5,743 (20261030 18:58 UTC) [1] |
| Created, last push | 20241002 11:57 UTC, 20261029 18:05 UTC [1]. The push time covers any branch; the head of `main` is 20261014 14:55 UTC [5]. |
| Latest release | v1.5.7, 20260902 07:23 UTC [2] |
| Status | active (pushed within 90 days); not archived [1] |
| Paper, docs | arXiv 2410.05779, latest version v3 of 20250428 [10]; the repository's `docs/` folder and README [4][16] |

## What it is

LightRAG is a graph-based retrieval-augmented generation (RAG) framework from the HKUDS group [1][10]. The
July note names the University of Hong Kong as its home; that affiliation was not rechecked [14]. It builds a knowledge graph of entities and relations with an LLM at index time,
stores it beside vector embeddings, and retrieves through two keyword levels: specific entity terms
and abstract concept terms [4][14]. The README presents it as "an efficient alternative to Microsoft GraphRAG": it has no community
hierarchy and no community summaries [4][14]. It ships a server with a WebUI and a REST API [4][14].
The repository description credits the paper to EMNLP 2025 [1]; the arXiv page lists no venue [10].

The core is one large `LightRAG` dataclass in `lightrag/lightrag.py` (8,431 lines at the snapshot; about
5.9k in July [14]) that orchestrates pluggable storages whose interfaces are in `lightrag/base.py` [6][8].
The class now inherits three mixins, among them `_PipelineMixin`, and a separate `lightrag/pipeline.py`
exists; the `apipeline_*` methods are called from `lightrag.py` but not defined there, and that module was not
read [8][16].

Related projects from the same organisation, as linked by the LightRAG README: RAG-Anything (multimodal
RAG, "Based on LightRAG"), VideoRAG and MiniRAG [4][12]. In May 2026 the README announces "Merge
RagAnything into LightRAG": multimodal parsing now lives in LightRAG itself [4]. RAG-Anything's own README
lists LightRAG as its base [12].

## How it works

### Storage layer

Four storage abstractions are defined in `lightrag/base.py` [6]:

| Abstraction | Holds |
|---|---|
| `BaseKVStorage` | documents, chunks, the LLM response cache |
| `BaseVectorStorage` | embeddings |
| `BaseGraphStorage` | the graph; its docstring states that edge operations are undirected |
| `DocStatusStorage` | pipeline states per document, including a `content_hash` and `get_doc_by_content_hash` |

Defaults are file-based: `JsonKVStorage`, `NanoVectorDBStorage`, `NetworkXStorage`,
`JsonDocStatusStorage` [8]. The README says these defaults are "suitable only for small-scale testing and
evaluation, not for production" and recommends PostgreSQL for production [4]. The `lightrag/kg/` folder
holds implementations for Postgres, Neo4j, Memgraph, Milvus, Qdrant, MongoDB, OpenSearch, Faiss and
Redis, plus a no-op vector store [16]. A change titled "deprecate redis storage warning" was merged to the
`dev` branch on 20260930 11:18 UTC; only its title was read [5].

The named instances in the July reading were `chunks_vdb`, `entities_vdb`, `relationships_vdb` (three
separate vector indexes), `chunk_entity_relation_graph`, `llm_response_cache` and `doc_status` [14]; the
function signatures of `kg_query` at the snapshot still take `entities_vdb`, `relationships_vdb`,
`text_chunks_db` and `chunks_vdb` [7].

### Indexing: eager, by LLM

1. **Ingest.** `ainsert` enqueues documents through `apipeline_enqueue_documents` (deduplication by content
   hash, a document-status queue) and processes them with `apipeline_process_enqueue_documents` [8][14].
   In July the chunking was fixed-token [14]. That is stale: since May 2026 four chunking strategies exist, `Fixed-length (F)`, `Recursive
   character (R)`, `Vector semantic (V)` and `Paragraph semantic (P)`, and the parser engines are MinerU,
   Docling and a native engine [4]. Which strategy is the default is unstated in what was read.
2. **Extraction.** `extract_entities` (`operate.py`, line 3942 at the snapshot) makes **one LLM call per
   chunk** with the `entity_extraction` prompt (delimiter format or JSON mode), then up to
   `entity_extract_max_gleaning` further "please continue" calls per chunk. Defaults in
   `lightrag/constants.py` at the snapshot: `DEFAULT_MAX_GLEANING = 1`, `DEFAULT_MAX_EXTRACT_INPUT_TOKENS = 20480`,
   `DEFAULT_MAX_EXTRACTION_RECORDS = 100`, `DEFAULT_MAX_EXTRACTION_ENTITIES = 40` [6][7][8].
3. **Merge.** `_merge_nodes_then_upsert` and `_merge_edges_then_upsert` look entities up **by name**, after
   `normalize_entity_name`. The docstring reads "Get existing nodes from knowledge graph use name, if exists,
   merge data, else create". A search of `operate.py` for resolution, alias or fuzzy-matching code found none, so the
   deduplication is exact name match, not embedding-based entity resolution [7]. Descriptions from
   all chunks are concatenated, with `_combine_descriptions_dedup` removing duplicates [7].
4. **Summarise on merge.** `_handle_entity_relation_summary` calls the LLM to rewrite a description when an
   entity has accumulated at least `force_llm_summary_on_merge` fragments (default 8) or exceeds
   `summary_context_size` (12,000 tokens), recursively in a map-reduce fashion [7][8][14]. So merging itself
   costs LLM calls as a corpus grows.
5. **Embed and keep provenance.** Entities and relations are embedded into `entities_vdb` and
   `relationships_vdb`; each node and edge keeps `source_id`, the list of chunk ids it came from [14].

**Incremental updates** are document-level only: content-hash deduplication, a status queue, a resumable
pipeline [14]. **Deletion** (`adelete_by_doc_id`) calls `rebuild_knowledge_from_chunks`, which rebuilds the
affected entities and relations **from cached extraction results** instead of calling the LLM again; this relies
on `enable_llm_cache_for_entity_extract`, default `True` in `lightrag.py` [7][8][14]. The README confirms the
mechanism: "the system can use the LLM cache created during indexing to quickly rebuild the affected entities
and relationships" [4].

### Retrieval: the caller picks the mode

`QueryParam.mode` takes `"local"`, `"global"`, `"hybrid"`, `"naive"`, `"mix"` or `"bypass"`, default
`"mix"` (`lightrag/base.py`) [6]. The README documents five of them, without `bypass`, and also says `mix` is
the default and "generally yields the most ideal query results" [4]. There is **no automatic router**. The only
routing logic is a fallback in `kg_query`: if both keyword lists come back empty and the query is shorter than
50 characters, the raw query becomes the low-level keyword; otherwise the call returns the failure response [7].

1. **Keywords.** `extract_keywords_only` makes **one LLM call per query** that returns JSON
   `{high_level_keywords, low_level_keywords}`; the result is cached in `llm_response_cache` under a hash of
   the arguments [7][8][14]. The call can be skipped: `get_keywords_from_query` returns the values of
   `QueryParam.hl_keywords` and `QueryParam.ll_keywords` directly when either list is non-empty, so a caller that
   supplies keywords pays no keyword call [6][7]. Since May 2026 this step has its own model slot, the `KEYWORD`
   role [4].
2. **Context.** `_build_query_context` runs four stages; `_perform_kg_search` implements the modes [7][14]:
   - **local**: embed the low-level keywords, query `entities_vdb` for the top-k entities, expand one hop in the
     graph (`_get_node_data`).
   - **global**: embed the high-level keywords, query `relationships_vdb` for the top-k relations, take their
     endpoint entities (`_get_edge_data`).
   - **hybrid**: both. **mix**: both plus a raw-query vector search on `chunks_vdb`.
   - **naive**: chunk vector search only; no graph and no keyword call (`naive_query`).
   The query, low-level and high-level embeddings are computed in one batched embedding call [14].
3. **Chunk recovery.** Chunks are recovered from the `source_id` lists of the retrieved entities and relations,
   chosen by `kg_chunk_pick_method`: `"VECTOR"` (default, cosine similarity to the query) or `"WEIGHT"`
   (occurrence-count polling) [6][7][14].
4. **Fusion.** `_merge_all_chunks` interleaves the three chunk streams (vector, entity-derived,
   relation-derived) **round-robin** with first-seen deduplication. Its code comment reads "Round-robin merge
   chunks from different sources with deduplication". There is no reciprocal-rank fusion and no score fusion [7].
5. **Token budgets.** Defaults at the snapshot: `max_entity_tokens` 6,000, `max_relation_tokens` 8,000,
   `max_total_tokens` 30,000, `DEFAULT_TOP_K` 40, `DEFAULT_CHUNK_TOP_K` 20 [6].
6. **Rerank.** `apply_rerank_if_enabled` (`lightrag/utils.py`) runs inside `process_chunks_unified`, followed by
   a `min_rerank_score` filter (default 0.0). The backends in `lightrag/rerank.py` are HTTP clients:
   `cohere_rerank`, `jina_rerank`, `ali_rerank` and `generic_rerank_api`; none loads a cross-encoder in process
   [6][8][9]. `enable_rerank` defaults to true (`RERANK_BY_DEFAULT`) but `DEFAULT_RERANK_BINDING` is `"null"`, so
   rerank does nothing until a binding is configured [6][9]. **Correction to July**, which said "hosted APIs
   only": the endpoint is configurable (`RERANK_BINDING_HOST`), `env.example` says "For rerank model deployed by
   vLLM use cohere binding", and the README recommends deploying a reranker such as `BAAI/bge-reranker-v2-m3`
   locally [4][9]. What is still true: LightRAG does not run the reranker itself.
7. **Answer.** The final answer is one more LLM call. `only_need_context=True` skips it and returns the
   context; `only_need_prompt` is also present [6][14].

### How an agent or program talks to it

- A **REST API server and WebUI** (`lightrag/api/`, `lightrag_webui/`) [4][16]. The WebUI has an admin console
  and a separate `/workspace` entry [4].
- A **Python library** API (`ainsert`, `aquery`, `aquery_data`, `aquery_llm`, `adelete_by_doc_id`) [8].
- **MCP:** the README does not mention it, and no MCP file appears in `docs/` or `lightrag/api/` [4][16]. Four
  closed issues in the project's tracker have MCP in their titles, among them "Feature/mcp support" and "feat: add
  Anthropic LLM binding for API server + MCP server adapter"; whether any was merged is unstated [15]. July's note
  "MCP is third-party" is therefore neither confirmed nor refuted by the sources; who maintains the third-party
  servers is unstated.

## Cost and operating profile

The figures below are arithmetic on the defaults above, not measurements; no cost measurement by the project itself was found
in the sources read. Token counts for LightRAG from other projects' benchmark runs appear in the
[HippoRAG](hipporag.md) entry (its Table 12 comparison) and the [fast-graphrag](fast-graphrag.md) entry
(GraphRAG-Bench); they were not re-measured for this entry.

| Phase | What it spends |
|---|---|
| Index time (the expensive side) | 1 extraction call plus up to 1 gleaning call per chunk (so N to 2N calls for N chunks at the defaults), periodic LLM merge-summaries, and embedding calls for chunks, entities and relations. A corpus of a few thousand chunks therefore means thousands of LLM calls before the first query [7][8][14]. |
| Query time | 1 keyword-extraction LLM call (cached by query hash; skipped when the caller passes keywords), 1 answer LLM call, 1 batched embedding call, and an optional rerank request. `naive` mode skips the keyword call [7][14]. The README says reranking typically adds a delay of 1 to 2 seconds [4]. |
| Caching | `llm_response_cache` covers extraction, keywords and query responses (`enable_llm_cache=True`, `enable_llm_cache_for_entity_extract=True`). It is what makes a delete-and-rebuild cheap, but it lives in internal storage keyed by prompt hash, not in a user-visible or committable form [8][14]. A migration tool for it exists (`lightrag/tools/migrate_llm_cache.py`) [4][16]. |
| Budget controls | Token budgets for context exist everywhere. No spend ledger, cost cap or "free path" was found in the sources read; this is an absence in what was read, not a proven absence [14]. Since May 2026 four role-specific LLMs (`EXTRACT`, `QUERY`, `KEYWORD`, `VLM`) can be set independently, so extraction can point at a cheaper model; the README advises a fast non-thinking model for extraction and a stronger one for answers [4]. |
| Incrementality | Incremental at document level (hash deduplication, resumable pipeline, cached-extraction graph rebuild after deletion). Lazy: nothing; the graph is always built eagerly at insert [14]. |
| Embedding lock-in | The embedding model must be chosen before indexing; changing it means re-embedding all chunks, entities and relationships. The README says LightRAG "does not currently provide a re-embedding tool"; `lightrag/tools/` holds a `rebuild_vdb.py`, and whether it re-embeds is unstated in what was read [4][16]. |

**Local operation.** The README describes local deployment of the embedding model, the reranker and the storage
backends (a setup wizard with Docker, March 2026) and names local LLM options for extraction (for example
Qwen3-30B-A3B-Instruct as "a reasonable minimum") [4]. It also warns that models below about 50 tokens per
second may time out on chunks with many entities [4]. A fully local run is therefore documented; it was not
executed in this study.

## Evidence

All published results found are the authors' own.

- **The paper.** arXiv 2410.05779 (Zirui Guo, Lianghao Xia, Yanhua Yu, Tu Ao, Chao Huang) proposes graph
  structures in text indexing, dual-level retrieval and an incremental-update algorithm, and reports "improved
  retrieval accuracy and efficiency" [10]. The abstract was read in summary only; the full text was not read in
  this study.
- **The README's results table** ("Replicating Findings in the Paper") gives pairwise win shares judged by an
  LLM on three criteria (comprehensiveness, diversity, empowerment) plus an overall winner, over four
  UltraDomain subsets [4][11]. LightRAG's overall win share against each baseline:

  | Baseline | Agriculture | CS | Legal | Mix |
  |---|---|---|---|---|
  | NaiveRAG | 67.6% | 61.2% | 84.8% | 60.0% |
  | RQ-RAG | 67.6% | 62.0% | 85.6% | 60.0% |
  | HyDE | 75.2% | 58.4% | 73.6% | 57.6% |
  | GraphRAG | 54.8% | 52.0% | 52.8% | 49.6% |

  Against GraphRAG on the Mix subset the baseline wins narrowly (50.4% against 49.6%), and on comprehensiveness
  and empowerment in that subset as well [4].
- **How the judging works** (from `docs/Reproduce.md`): queries are generated by an LLM from a dataset
  description (5 users, 5 tasks each, 5 questions each), and an LLM judge compares two answers per criterion and
  names an overall winner [11]. Win share is not factual accuracy. The judge model, the number of runs and any
  variance are unstated in what was read, and the README table was not checked against the paper.
- **In-repo evaluation tooling.** `lightrag/evaluation/` holds a RAGAS-based framework (faithfulness, answer
  relevance, context recall, context precision) and an offline retrieval check [11][16]. No scores produced with
  it were found.
- **Third-party evaluations:** none were fetched in this study.

## Direction

From the README news list, newest first [4]: Smart Heading recognition for Word documents (July 2026); RAG-Anything
merged into LightRAG with MinerU and Docling parsing, four chunking strategies, and role-specific LLMs (May
2026); OpenSearch as a storage backend and a setup wizard (March 2026); RAGAS evaluation and Langfuse tracing
(November 2025); reranker support and document deletion with graph regeneration (August 2025).

From the commit subjects since 20260801 [5]: most work is on storage backends (PostgreSQL/pgvector filtered
approximate-nearest-neighbour fixes, Milvus and OpenSearch fixes), multimodal table handling, tests and frontend
dependency updates. Branches named `dev-lancedb`, `dev-nebula-graph`, `dev-documentdb`, `plan/multi-workspace-authz`
and `feat/json-config-workspace-shards` exist; their contents were not read [5].

Releases: v1.5.0 20260603, v1.5.1 20260609, v1.5.2 20260611, v1.5.3 20260614, v1.5.4 20260624, v1.5.5
20260731, v1.5.6 20260806, v1.5.7 20260902 (release candidates omitted). There has been no release in the 58
days to the snapshot [2].

## Changed since the July 2026 investigation

The investigation is dated 20260725 15:29 UTC [14]. Everything below was read 20261030 18:58 to 19:04 UTC.

- **Popularity.** 40,443 stars and 5,743 forks (20261030 18:58 UTC) [1]. July recorded "about 38k" stars, an
  approximate figure; stars had therefore risen by roughly 2,400.
- **Licence.** Unchanged: MIT, read from `LICENSE` [3]. Not archived; created 20241002; GitHub still serves the
  repository as `HKUDS/LightRAG`, so no rename was found [1].
- **Activity.** Commits on `main` since 20260801: **1,576** (August 785, September 777, October 14), and 319 pull
  requests merged since 20260801 [5]. The head of `main` is 20261014 14:55 UTC, a merge of a pgvector filtered-search
  fix; nothing was committed to `main` in the following 16 days, while the repository's last push (any branch) is
  20261029 18:05 UTC. Why `main` went quiet is unstated; which branch took the later push was not checked [1][5].
  By author login: 970 commits for `danielaskdd`, 293 for an account named `claude`, 82 for `Shizoqua`, 37 for
  `dependabot[bot]`; the sources do not say what the `claude` account is [5]. The repository has 315 listed
  contributors [1]. Total commits on `main`: 10,873 at 19:02 UTC, against 9,064 at the July investigation time (the
  July note said "about 9k"), so 1,809 commits landed in between [5].
- **Releases.** Three stable releases since the investigation: v1.5.5 (20260731), v1.5.6 (20260806) and v1.5.7
  (20260902), with two release candidates for v1.5.7 in between; v1.5.7 is current [2].
- **Size.** `lightrag/lightrag.py` has 8,431 lines (July: about 5.9k). The July line numbers for `operate.py`
  and `utils.py` functions are all out of date. Current ones are given in Sources [8].
- **Defaults rechecked and unchanged:** gleaning 1, extraction records 100, entities 40, forced merge summary at 8
  fragments, summary context 12,000 tokens, extract input 20,480 tokens, token budgets 6,000/8,000/30,000,
  `kg_chunk_pick_method` `"VECTOR"`, default mode `mix`, rerank binding `"null"`, round-robin fusion, exact-name
  entity merge, the fallback for keyword failure, the file-based default storages [6][7][8][9].
- **Claims that were false or stale, corrected in the body:**
  - "Hosted-API-only rerank": rerank is an HTTP call to a configurable endpoint that can be self-hosted; the
    in-process cross-encoder is still absent.
  - "Fixed-token chunking": four strategies now exist.
  - The list of production storage bindings: Faiss and Redis implementations are also present; Redis has a
    deprecation-warning change on `dev`.
  - "MCP is third-party": the sources neither confirm nor refute it.
  - The venue "EMNLP 2025" comes from the repository description; the arXiv page lists none.
- **New since July:** multimodal parsing merged from RAG-Anything, a parser-engine pipeline (MinerU, Docling,
  native), the four chunking strategies, role-specific LLMs, an OpenSearch backend, a setup wizard, a RAGAS
  evaluation tool, and an `/workspace` UI entry [4][16].
- **Paper and successor.** arXiv shows no version after v3 (20250428) [10]. No successor project or paper was
  found: the README names none, and one web search at 19:04 UTC returned none (thin coverage). RAG-Anything
  is a separate repository (MIT licence, 24,322 stars, not archived, last push 20261028 07:20 UTC), whose README
  says it is built on LightRAG [12]. MiniRAG, also linked from the README, had 2,026 stars and its last push
  on 20251016 07:43 UTC [13].

## Sources

1. https://github.com/HKUDS/LightRAG : repository metadata via the GitHub API (stars, forks, licence field,
   archived flag, created and pushed dates, description, topics, open-issue count, contributor count) (read
   20261030 18:58 UTC)
2. https://github.com/HKUDS/LightRAG/releases : latest release and the release list with dates (read 20261030
   18:58 UTC)
3. https://github.com/HKUDS/LightRAG/blob/main/LICENSE : licence text (read 20261030 18:58 UTC)
4. https://github.com/HKUDS/LightRAG/blob/main/README.md : news list, feature descriptions, query modes, model
   guidance, rerank and embedding notes, results table, related projects (read 20261030 18:58 UTC)
5. https://github.com/HKUDS/LightRAG/commits/main : commit list since 20260801, monthly counts, author counts, total
   commit counts, merged pull-request count, branch list and the `dev` head (read 20261030 18:58 to 19:02 UTC)
6. https://github.com/HKUDS/LightRAG/blob/main/lightrag/base.py and
   https://github.com/HKUDS/LightRAG/blob/main/lightrag/constants.py : `QueryParam`, storage abstractions,
   all defaults quoted (read 20261030 19:01 UTC)
7. https://github.com/HKUDS/LightRAG/blob/main/lightrag/operate.py : `extract_entities` (line 3942),
   `_merge_nodes_then_upsert` (2429), `_merge_edges_then_upsert` (2782), `_handle_entity_relation_summary` (372),
   `rebuild_knowledge_from_chunks` (1102), `kg_query` (4693), `get_keywords_from_query` (4975),
   `extract_keywords_only` (5112), `_perform_kg_search` (5280), `_merge_all_chunks` (5765),
   `_build_query_context` (6075), `_find_related_text_unit_from_entities` (6350), `naive_query` (6827); line
   numbers at the snapshot (read 20261030 19:01 UTC)
8. https://github.com/HKUDS/LightRAG/blob/main/lightrag/lightrag.py and
   https://github.com/HKUDS/LightRAG/blob/main/lightrag/utils.py and
   https://github.com/HKUDS/LightRAG/blob/main/lightrag/prompt.py : `LightRAG` class fields and defaults,
   `ainsert`, `aquery*`, `adelete_by_doc_id`, `apply_rerank_if_enabled` (utils, line 6924),
   `process_chunks_unified` (utils, 7055) (read 20261030 19:01 UTC)
9. https://github.com/HKUDS/LightRAG/blob/main/lightrag/rerank.py and
   https://github.com/HKUDS/LightRAG/blob/main/env.example : rerank backends, binding options, vLLM note
   (read 20261030 19:02 UTC)
10. https://arxiv.org/abs/2410.05779 : title, authors, version history v1 to v3, absence of a venue, abstract
    summary (read 20261030 19:02 UTC)
11. https://github.com/HKUDS/LightRAG/blob/main/docs/Reproduce.md and
    https://github.com/HKUDS/LightRAG/tree/main/lightrag/evaluation : judging prompt and procedure, RAGAS
    framework description (read 20261030 19:02 UTC)
12. https://github.com/HKUDS/RAG-Anything : repository metadata and README statements about LightRAG (read
    20261030 19:02 UTC)
13. https://github.com/HKUDS/MiniRAG : repository metadata only (read 20261030 19:02 UTC)
14. Earlier investigation of this project dated 20260725 15:29 UTC, the document this entry was rewritten from
    (historical; no live link). Statements resting on it alone were read from the code at that date and were not all
    re-read on 20261030; those that were re-read cite [6]-[9] as well.
15. https://github.com/HKUDS/LightRAG/issues?q=mcp : titles of four closed issues mentioning MCP (read 20261030
    19:02 UTC)
16. https://github.com/HKUDS/LightRAG/tree/main/lightrag and its `kg/`, `api/`, `tools/` folders, and
    https://github.com/HKUDS/LightRAG/tree/main/docs : directory listings (read 20261030 19:01 to 19:02 UTC)
