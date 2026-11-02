---
slug: fast-graphrag
repo: circlemind-ai/fast-graphrag
tier: deep
category: core
snapshot: 20261030 18:58 UTC
---

# fast-graphrag

| | |
|---|---|
| Repository | https://github.com/circlemind-ai/fast-graphrag [1] |
| Licence | MIT, from the `LICENSE` file (copyright line "2024 circlemind-ai"); the README badge also says MIT, so no disagreement [2][3] |
| Language | Python, 30 files under `fast_graphrag/`; `pyproject.toml` allows Python `>=3.10,<3.13` [1][6][21] |
| Stars, forks | 3,967 stars, 258 forks (20261030 18:58 UTC) [1] |
| Created, last push | 20241030 18:05 UTC, 20251101 20:45 UTC [1] |
| Latest release | No GitHub release and no tag (20261030 18:58 UTC). Latest PyPI upload: 0.0.5, 20250404 08:16 UTC [5] |
| Status | Quiet, not archived (`archived: false`). The last push is 363 days old at the snapshot. The evidence under "Direction" says the project does not look maintained [1][4] |
| Paper, docs | No paper of its own. The README points to the HippoRAG paper (arXiv 2405.14831) for why personalized PageRank works [3][26]. Managed-service docs link: see "Changed since the July 2026 investigation" [25] |

## What it is

fast-graphrag is an open-source GraphRAG library from Circlemind, a company that also sells a managed
service [3]. At insert time an LLM extracts typed entities and relations from text chunks and the library
stores them as a graph [12][14]. At query time it seeds a Personalized PageRank (PPR) run from the query's
entities instead of building community reports, as Microsoft GraphRAG does [8][9]. The user steers
extraction with three strings, `domain`, `example_queries` and `entity_types`, which are templated into the
extraction prompts [14][19]. The package version is 0.0.5 [6].

## How it works

### Indexing

- **Chunking** (`_services/_chunk_extraction.py`). A regex splits the text on separators (paragraph breaks and
  sentence punctuation, including Chinese and full-width marks). Chunks are character windows sized from
  `chunk_token_size=800` and `chunk_token_overlap=100`, multiplied by `TOKEN_TO_CHAR_RATIO` (the ratio's
  value is in `_utils.py`, which was not read on 20261030: **unstated** then; read 20261102 10:28 UTC: it is 4, so a window is 3,200 characters with 400 overlap [30]). A text no longer than one window stays one
  chunk [13].
- **Chunk identity.** `id = xxhash.xxh3_64_intdigest(chunk) // 2`. It is a content hash, halved so it fits a
  signed 64-bit integer [13]. A commit titled "Fix signed 64 bit overflow" exists in the history [4].
- **Incremental skip.** `async_insert` calls `state_manager.filter_new_chunks()`, which asks the key-value
  store which chunk ids are new (`mask_new`). Only new chunks are sent to extraction, so re-inserting an
  unchanged chunk costs no LLM call [14][8][20]. No diffing or re-linking pass appears in the files read. The
  public class in `_graphrag.py` exposes `insert`, `query` and `save_graphml`; it has no delete or update
  method [14]. No path that removes an entity or relation was found in the files read.
- **Extraction** (`_services/_information_extraction.py`). For each new chunk, one
  `entity_relationship_extraction` call returns a structured `TGraph`. Entity types are checked against
  `entity_types` after stripping spaces and underscores and upper-casing; a non-matching type is set to
  `UNKNOWN`. Each relation records the chunk id it came from [12].
- **Gleaning (optional extra passes).** `max_gleaning_steps` defaults to **0** in the base service, and
  `GraphRAG` does not override it, so by default there is **one extraction call per chunk** [16][15][12]. If it
  is set to n >= 1, each step makes one `entity_relationship_continue_extraction` call and, except on the last
  step, one `entity_relationship_gleaning_done_extraction` call: 2n calls per chunk in total. The early-stop
  test is `gleaning_status.status == Literal["done"]`, which compares a string with a `typing.Literal`
  object. In Python that comparison is `False` (checked 20261030 19:00 UTC), so, as read, the loop always
  runs all n steps. This was a reading of the code, not an end-to-end run [12]. **Corrected 20261102 10:48 UTC by a stub run:** with `max_gleaning_steps` at 1 and at 2 no extra call was made (the call count stayed equal to the chunk count). Each chunk logged `Error during gleaning: 'domain'`: the continuation prompt is formatted with no arguments while its system text needs `{domain}`. The `KeyError` is caught, `_gleaning` returns `None`, and the caller keeps the first extraction (`_information_extraction.py`, lines 135 to 137 at the pinned commit, re-read 20261102 10:55 UTC). So at that commit gleaning cannot add a call whatever the setting [30].
- **Per-document merge, then global merge.** Each document's chunk graphs are first merged into a small
  igraph graph with `DefaultGraphUpsertPolicy` (node policy `NodeUpsertPolicy_SummarizeDescription`, edge
  policy `EdgeUpsertPolicy_UpsertIfValidNodes`) [12][15]. The state manager then upserts that into the main
  graph with `NodeUpsertPolicy_SummarizeDescription` and
  `EdgeUpsertPolicy_UpsertValidAndMergeSimilarByLLM` [8][15][11].
- **Node merge** (`_policies/_graph_upsert.py`). Nodes merge **by exact name**. Descriptions are joined; when
  the joined text exceeds `max_node_description_size=512` characters, one `summarize_entity_descriptions` LLM
  call compresses it. The node type becomes the most frequent type among the merged nodes [11].
- **Edge merge.** The LLM (`edges_group_similar`) is called only when the existing plus new edges between one
  node pair exceed `edge_merge_threshold=5` [11].
- **Alias handling by identity edges** (`_services/_state_manager.py: upsert`). Each upserted entity is
  embedded and its 3 nearest neighbours are fetched (`get_knn(top_k=3)`). Where similarity is at least
  `insert_similarity_score_threshold=0.9`, an edge with description `"is"` is inserted between the two
  entities (one direction only, and only if they are not already neighbours). Entities are not merged; the
  alias is an edge [8].
- **Only entities are embedded.** The embedding call in `upsert` covers the upserted nodes. Chunks go to an
  indexed key-value store, not to a vector index, so retrieval never searches chunk text by embedding [8][20].
- **Storage** (`_storage/`). The igraph graph is pickled to `igraph_data.pklz`; the key-value store (chunks)
  is a pickle (`kv_data.pkl`); entity vectors are an hnswlib index (`M=64`, `ef_construction=128`,
  `ef_search=96`); the entity-to-relation and relation-to-chunk matrices are pickled blobs. No SQL and no
  server [9][18][20][8].
- **Defaults.** LLM `gpt-4o-mini`; embeddings `text-embedding-3-small`, 1536 dimensions, both through the
  OpenAI client with an optional `base_url` [17].

### Retrieval (personalized PageRank exploration)

All of it is in `_services/_state_manager.py: get_context` and `_graphrag.py: async_query` [8][14].

1. **Query entity extraction.** One LLM call (`extract_entities_from_query`, prompt
   `entity_extraction_query`) splits the query into **named** entities and **generic** ones. The prompt
   receives only the query; `domain`, `example_queries` and `entity_types` are not passed to it [12][19].
2. **Map to nodes by embedding.** One embedding call encodes the named entities (plain), the generic
   entities (prefixed `[NONE] `) and the whole query string. Each named entity goes to its nearest node
   (`top_k=1`, threshold `query_similarity_score_threshold=0.7`). The generic entities **and the full query
   embedding** each go to `top_k=20`, threshold 0.5. Scores are normalized per query entity (divided by
   their sum plus 1e-8) and max-aggregated into one sparse vector over nodes [8].
3. **PPR.** `igraph.personalized_pagerank(damping=0.85, directed=False, reset=<that vector>)` runs over the
   whole graph [9]. Random-walk mass spreads from the seed nodes to multi-hop neighbours. No community
   detection or community report appears in the files read [8][9].
4. **Cascade by sparse matrix products.** Entity scores are cut by the entity ranking policy. Then
   `entity_scores.dot(e2r)` (entity-to-relation incidence) gives relation scores, cut by the relation policy.
   Then `relation_scores.dot(c2r)` (relation-to-chunk matrix) gives chunk scores, cut by the chunk policy [8].
   The matrices are rebuilt at `insert_done` [8].
5. **Ranking policies** (`_policies/_ranking.py`). Three exist: `RankingPolicy_WithThreshold`
   (class defaults threshold 0.05, `max_entities` 128), `RankingPolicy_TopK` (class default 10) and
   `RankingPolicy_Elbow` (sorts the scores, finds the largest gap and drops everything below it).
   `RankingPolicy_WithConfidence` raises `NotImplementedError` [10]. **The defaults the `GraphRAG` class
   actually uses are different:** entities `WithThreshold(threshold=0.005)` (max 128), relations
   `TopK(64)`, chunks `TopK(8)`. `Elbow` is not part of the default configuration [15].
6. **Answer.** Entities, relations and chunks are truncated to token budgets (`QueryParam` defaults: 4,000,
   3,000 and 9,000 tokens) and sent in one LLM call (`generate_response_query_with_references` or
   `..._no_references`). With `only_context=True` the answer call is skipped [14].

### Interface to agents

The interface is a Python SDK: `GraphRAG(working_dir, domain, example_queries, entity_types)` with `insert`,
`query` and async variants [3][14]. The README tagline mentions "agent-driven retrieval workflows" but no MCP
server or tool schema appears in the repository file tree (listing read 20261030 18:59 UTC) [3][21]. The
README's examples cover a custom OpenAI-compatible LLM, checkpoints and query parameters including references
[3]; the tree also holds Gemini examples [21].

## Cost and operating profile

| Aspect | Reading | Source |
|---|---|---|
| Index-time LLM calls | 1 extraction call per new chunk by default (gleaning off), 2n per chunk if gleaning is set to n (as read; measured 20261102: gleaning adds no call at that commit [30]); plus node-description summaries past 512 characters and edge grouping past 5 parallel edges. A stub rehearsal on 20 news articles made 80 extraction calls for 80 chunks and 187,783 stub-counted prompt tokens, with no summary call for short descriptions and 41 for 200-character ones; those counts are for the stub's answers [30] | [12][16][11] |
| Index-time embeddings | Entities only (chunks are not embedded) | [8] |
| Query-time LLM calls | 2: query entity extraction, then answer generation (1 with `only_context=True`). PPR and the matrix cascade run locally | [14][8] |
| Query-time embeddings | One call covering the named entities, generic entities and the query | [8] |
| Needs | An OpenAI-compatible LLM and embedding endpoint (`OPENAI_API_KEY` in the quickstart). No database, no server, no GPU requirement stated | [3][17] |
| Local operation | Any OpenAI-compatible endpoint can be set; no local inference is bundled. The package depends on `openai`, `google-genai`, `vertexai` and `voyageai` SDKs regardless. Also `igraph`, `hnswlib`, `scipy`, `scikit-learn`, `xxhash`, `pydantic`, `instructor`, `tiktoken`; no `torch` | [6][3] |
| Rebuild | A rebuild from scratch pays the full extraction bill again unless the pickled working directory survives | inference from [14][20] |
| Concurrency control | The README suggests `CONCURRENT_TASK_LIMIT` for local models | [3] |

**Published cost figures.**

- The README states: "Using *The Wizard of Oz*, `fast-graphrag` costs $0.08 vs. `graphrag` $0.48 — a 6x
  costs saving that further improves with data size and number of insertions" (read 20261030 18:58 UTC). The
  model, the GraphRAG variant, the chunk count and the counting method are **unstated** [3].
- The benchmark README reports insertion time for the 2wikimultihopqa corpus (about 800 chunks): VectorDB
  about 0.3 min, LightRAG about 25, GraphRAG about 40, fast-graphrag about 1.5 min, and calls it "27x faster
  than GraphRAG" [7].
- A third-party measurement exists: GraphRAG-Bench (see "Evidence") indexed one book of about 56,000 tokens
  with GPT-4o-mini. fast-graphrag used 281.74 s and 251,817 tokens (187,765 input, 64,052 completion).
  Microsoft GraphRAG used 292.45 s and 654,673 tokens; LightRAG 710.32 s and 474,172; HippoRAG 77.42 s and
  177,961; HippoRAG2 96.71 s and 329,993 [27]. By these numbers fast-graphrag used 2.6 times fewer tokens
  than Microsoft GraphRAG (654,673 / 251,817, my arithmetic) and about the same time, not 6 times less.
- AGRAG (arXiv 2511.05549v2) timed indexing with a local Qwen2.5-14B on one A100. fast-graphrag took 106, 48,
  29 and 27 minutes on its four datasets (Novel, Medical, WOS, IFS-REL); GraphRAG 347, 194, 85 and 64;
  LightRAG 166, 116, 42 and 31; HippoRAG2 95, 46, 19 and 15 [28]. That paper proposes a competing method, so
  it is not a neutral party.

**Where a saving could come from (analysis, not a published breakdown).** The July 2026 investigation
attributed the difference to four things: no community detection and no per-community report generation,
which it identified as Microsoft GraphRAG's dominant cost (not re-checked against that project's source in
this run); conditional LLM merging (summaries only past 512 characters, edge grouping only past 5 parallel
edges); content-hash chunk skipping on updates; and two LLM calls per query. The code supports the second,
third and fourth points [11][8][14]. It also shows extraction is still one LLM call per chunk, which July
described as "not cheaper than GraphRAG's". That last comparison is likewise unverified here [29].

## Evidence

### Vendor benchmark (Circlemind, `benchmarks/README.md`)

The benchmark README says it validates the HippoRAG paper's results and compares VectorDB (OpenAI
`text-embedding-3-small`), LightRAG, and "GraphRAG", for which it uses the `nano-graphrag` implementation
"based on the original Microsoft GraphRAG" (local mode in the printed output), not Microsoft's own package
[7]. The metric is retrieval only: "the percentage of queries for which all the required evidence was
retrieved" (printed as "perfect retrieval"). No answer generation is scored [7].

| Dataset, queries | VectorDB | LightRAG | GraphRAG (nano-graphrag) | fast-graphrag |
|---|---|---|---|---|
| 2wikimultihopQA, 51, all queries | 0.49 | 0.47 | 0.75 | 0.96 |
| 2wikimultihopQA, 51, multihop only | 0.32 | 0.32 | 0.68 | 0.95 |
| 2wikimultihopQA, 101, all queries | 0.42 | 0.45 | 0.73 | 0.93 |
| 2wikimultihopQA, 101, multihop only | 0.23 | 0.28 | 0.64 | 0.90 |
| HotpotQA, 101 | 0.78 | 0.55 | crashed after half an hour | 0.84 |

Source: [7]. Caveats stated or visible in the source:

- The benchmark is run by the vendor, on subsets of 51 and 101 questions. No independent replication of these
  numbers was found in the sources read.
- On HotpotQA the margin over a plain vector index is 6 points (0.84 against 0.78).
- The README says the HotpotQA code will be released "soon". The repository tree holds only the
  2wikimultihopqa dataset, questions and results (listing read 20261030 18:59 UTC); HotpotQA code and data
  were not found [7][21].
- To run LightRAG the authors deleted imports of missing dependencies; they say LightRAG and GraphRAG
  "could take over an hour to process and they can be expensive" [7].
- The scripts and preloaded results are in the repository, so the 2wikimultihopqa numbers can be recomputed
  with `evaluate_dbs` [7].

### Third-party evaluation: GraphRAG-Bench (arXiv 2506.05690, ICLR 2026, v3 dated 22 Feb 2026)

Authors from Xiamen University and The Hong Kong Polytechnic University. The benchmark has a Novel corpus
(pre-20th-century Gutenberg novels) and a Medical corpus (NCCN clinical guidelines), with four task levels.
The default generator is GPT-4o-mini [27]. The configuration used for Fast-GraphRAG (version, parameters)
was not stated in the pages read. Selected numbers, answer accuracy (ACC, Table 3) and evidence recall
(Table 4):

| Corpus, task | Metric | Basic RAG (rerank) | MS-GraphRAG (local) | LightRAG | HippoRAG2 | Fast-GraphRAG |
|---|---|---|---|---|---|---|
| Novel, fact retrieval | ACC | 60.92 | 49.29 | 58.62 | 60.14 | 56.95 |
| Novel, complex reasoning | ACC | 42.93 | 50.93 | 49.07 | 53.38 | 48.55 |
| Medical, fact retrieval | ACC | 64.73 | 38.63 | 63.32 | 66.28 | 60.93 |
| Medical, complex reasoning | ACC | 58.64 | 47.04 | 61.32 | 61.98 | 61.73 |
| Novel, fact retrieval | evidence recall | 83.21 | 61.04 | 73.69 | 70.29 | 64.48 |
| Novel, complex reasoning | evidence recall | 64.47 | 73.03 | 85.52 | 69.77 | 73.51 |
| Medical, fact retrieval | evidence recall | 87.83 | 38.06 | 80.32 | 78.70 | 66.82 |
| Medical, complex reasoning | evidence recall | 86.49 | 61.32 | 82.91 | 77.00 | 74.93 |

Source: [27], Tables 3 and 4 (GPT-4o-mini). Reading: on these tasks fast-graphrag does not beat a
reranked vector baseline on fact retrieval, trails HippoRAG2 on three of the four accuracy cells, and on
evidence recall is below the vector baseline on both fact-retrieval cells and on Medical complex reasoning.
The paper's own conclusion is that basic RAG matches or beats GraphRAG methods on simple fact retrieval and
that graph methods help on complex tasks [27]. With Qwen2.5-14B as generator (Table 11), Fast-GraphRAG has
the highest Novel fact-retrieval accuracy (60.08) and ROUGE-L (41.31) among the methods listed [27]. These
results use different data and a different metric from the vendor's 0.93 evidence-recall figure, so the two
do not contradict each other directly.

### Other

- AGRAG (arXiv 2511.05549v2, 17 Mar 2026) includes F.GraphRAG as a baseline with default parameters and top-k
  5. It reports that NaiveRAG beats all tested walking-based baselines, fast-graphrag among them, on
  Contextual Summarization and Creative Generation, and a hallucinated-prediction rate of 6.06% for
  fast-graphrag on the WOS classification set. The effectiveness table did not extract from the PDF text read
  (printed as "Table ??"), so its accuracy numbers are **not read** [28].
- No dedicated independent benchmark of fast-graphrag alone was found; this was one web search plus the two
  papers above, not a systematic review.
- Known open defects in the issue tracker (state at 20261030): #101, an error "Invalid length of reset vector"
  in the PPR step on a broken index (opened 20250818); #103, `max_tokens` sent as null to gpt-5 models
  (20250923); #105, "Invalid vertex ID" when processing many files (20250925); #102, an empty
  `entities_hnsw_metadata.pkl` (20250919) [22].

### Method note: what the project does not state

The README does not state the data volume behind the $0.08 / $0.48 figure, and the benchmark README does not
state which LLM produced the graphs. Both are **unstated**.

## Direction

The repository states no roadmap. The README had a "News (and Coming Soon)" list with one open item, "Support
for IDF weightening of entities"; the last commit (20251101) removed that list [4]. Open issues and pull
requests ask for metadata filtering (PR #109), automatic entity extraction (issue #43) and evaluation metrics
(#111, #112, #113) [22].

**Is it maintained? It does not look maintained.** Read at 20261030 18:58 to 19:03 UTC:

| Signal | Reading | Source |
|---|---|---|
| Last push | 20251101 20:45 UTC, 363 days before the read | [1] |
| Commits since 20260801 | 0 | [4] |
| Last commit that changed code | Merge of PR #98 (structured output), 20250621; the 20251101 commit changed only the README | [4] |
| Commit rate | 48 commits in 2025: 9 in January, 26 in February, 10 in April, 2 in June, 1 in November | [4] |
| Releases | No GitHub release or tag. PyPI 0.0.5 on 20250404; the June 2025 change is later than that upload (by date; the wheel was not inspected), and `pyproject.toml` on `main` still says 0.0.5 | [5][6] |
| Open work | 32 open issues and 6 open PRs (GitHub's `open_issues_count` of 38 counts both). The oldest open PRs date from February 2025. Fix PRs #104 and #106 (September 2025) were never merged | [1][22] |
| Maintainer responses | The last comment by the repository's top-committing account is on PR #104 (20251016). The last issue closure is #108 (20251020), by an account whose role was not checked. The four issues opened 20260504 to 20260617 (#110 to #113), PR #109 (20260126) and a 20251104 request for an update on #43 have no reply from that account; the two 2026 comments are from accounts with no association to the repository | [22] |
| Contributors | 10 accounts; one holds 193 contributions, the next 23 | [1] |
| The company | Its most recently pushed repositories are `smooth-sdk` (20260814) and `smooth-website` (20261013), a browser-automation product; `fast-graphrag` was last pushed 20251101 | [23] |

No single row proves abandonment: a push date alone would not. Together they point one way: no commit for a
year, no release for 19 months, bugs on current models (#101, #103, #105) unfixed with fixes unmerged, no
reply to recent issues, and the company's activity elsewhere. The project is not archived, and the sources
cannot show anything said in private channels such as the Discord linked from the README, so "does not look
maintained" is the supported claim, not "abandoned". Code stubs agree with an unfinished state:
`RankingPolicy_WithConfidence` raises `NotImplementedError`, and `_get_entities_to_num_docs` and the
`node_specificity` option raise `NotImplementedError` as well [10][8].

## Changed since the July 2026 investigation

The July notes were written on 20260725 15:30 UTC. Checked 20261030 18:58 to 19:03 UTC.

- **Stars and forks.** 3,967 stars and 258 forks now [1]. The July notes recorded 3,828 stars on 20260725
  (+139 in 97 days); a forks figure was not recorded in them [29].
- **Licence.** Unchanged: MIT in the `LICENSE` file; the README badge agrees; GitHub reports MIT [1][2][3].
- **Archived.** Still `false` [1].
- **Last push.** The 20251101 date is confirmed (`pushed_at` 2025-11-01T20:45:25Z) [1]. There are no commits
  since 20260801, and none since 20251101 [4]. "No activity through mid-2026", the July wording, now extends to
  20261030.
- **Releases.** None on GitHub; PyPI latest still 0.0.5 [5].
- **Issues.** The July notes said "~38 open issues". The 38 is issues plus pull requests: 32 issues and 6 PRs
  [1][22]. Four issues (#110 to #113) and PR #109 were opened after the last commit, none answered by a
  maintainer [22].
- **README and architecture.** The README last changed in the 20251101 commit, before the July analysis: it
  removed the "News (and Coming Soon)" section and the "Looking for a Managed Service?" link from the tagline.
  The commit message says "remove cost-saving details", but the $0.08 / $0.48 note is still in the README, so
  the July citation of it holds [3][4]. The code at `main` is the code July analysed; the analysis is
  unaffected by any change, because nothing was committed after it [4].
- **"Circlemind ... moved to a hosted product."** Partly stale. The README still points to a managed service
  and to `docs.circlemind.co/quickstart`, but that URL now answers `301 Moved Permanently` to
  `docs.smooth.sh`, the documentation of Smooth, "a browser agent that can go to the web and perform tasks
  autonomously". The `circlemind.co` home page offers Smooth and Zero (a general agent, in beta) and does not
  mention fast-graphrag or GraphRAG. Whether the managed GraphRAG service still runs is **unstated** [3][24][25].
- **"3-person YC company."** Reworded. `pyproject.toml` lists three authors, and the `circlemind.co` footer
  says "Backed by Y Combinator". Headcount is unstated by the sources [6][24].
- **Corrected in the body above (July claims that were wrong or stale):**
  - July: "2 to 1+2·n LLM calls per chunk" and "2+ extraction LLM calls" per new chunk. Correct: 1 by default
    (`max_gleaning_steps=0`); 2n with gleaning, as read; **measured 20261102: gleaning adds no call at that commit [30]**; the early stop never fires [12][16].
  - July: ranking defaults `threshold=0.05`, `top_k=10`. Those are the class defaults; the library's actual
    defaults are 0.005 for entities, `TopK(64)` for relations and `TopK(8)` for chunks, and the Elbow policy
    is not used by default [10][15].
  - July: chunk id is the xxh3 digest. Correct: the digest halved (`// 2`) [13].
  - July: "embedding of every entity and chunk". Correct: entities only [8].
  - July: "GraphRAG 73%". The benchmark's "GraphRAG" is `nano-graphrag` in local mode, not Microsoft's package,
    and the metric is retrieval only [7].
  - July: "evidence-recall 93% ... wins on multi-hop (93% vs 42%)". Kept as the vendor's figure; the
    HotpotQA margin (84% vs 78%) and the independent GraphRAG-Bench results above were missing from the July
    notes [7][27].
- **Papers.** The project has none. The HippoRAG paper the README cites (arXiv 2405.14831, NeurIPS 2024) has
  three versions; v3 (14 Jan 2025) is current, so no new version since July [26]. The top-committing account
  replied on issue #108 (20251016) that the implementation "is based on version 1" of HippoRAG [22].
- **Rename or successor.** None found. The repository name, organisation and description are unchanged, and
  neither the README nor `circlemind.co` points to a successor [1][3][24].

## Sources

All repository sources were read on 20261030 UTC; times are the time of the read.

1. https://api.github.com/repos/circlemind-ai/fast-graphrag : stars, forks, licence field, `archived`, created and pushed dates, open issue count, topics, contributors list (read 20261030 18:58 UTC; contributors 19:00 UTC)
2. https://github.com/circlemind-ai/fast-graphrag/blob/main/LICENSE : MIT licence text (read 20261030 18:58 UTC)
3. https://github.com/circlemind-ai/fast-graphrag/blob/main/README.md : description, cost note, quickstart, managed-service text, HippoRAG reference (read 20261030 18:58 UTC)
4. https://github.com/circlemind-ai/fast-graphrag/commits/main : commit lists (since 20260801: none; latest 8; 48 since 20250101) and the diff of commit 23b3a1b (read 20261030 18:58 and 19:01 UTC)
5. https://github.com/circlemind-ai/fast-graphrag/releases and https://pypi.org/project/fast-graphrag/ : no GitHub release or tag; PyPI release history to 0.0.5 (read 20261030 18:58 and 18:59 UTC)
6. https://github.com/circlemind-ai/fast-graphrag/blob/main/pyproject.toml : version, Python range, dependencies, authors (read 20261030 18:58 UTC)
7. https://github.com/circlemind-ai/fast-graphrag/blob/main/benchmarks/README.md : benchmark method, tables, caveats (read 20261030 19:00 UTC)
8. https://github.com/circlemind-ai/fast-graphrag/blob/main/fast_graphrag/_services/_state_manager.py : upsert, identity edges, `get_context`, scoring cascade (read 20261030 19:00 UTC)
9. https://github.com/circlemind-ai/fast-graphrag/blob/main/fast_graphrag/_storage/_gdb_igraph.py : PPR call, igraph pickle storage (read 20261030 19:00 UTC)
10. https://github.com/circlemind-ai/fast-graphrag/blob/main/fast_graphrag/_policies/_ranking.py : ranking policies (read 20261030 19:00 UTC)
11. https://github.com/circlemind-ai/fast-graphrag/blob/main/fast_graphrag/_policies/_graph_upsert.py : node and edge upsert policies (read 20261030 19:00 UTC)
12. https://github.com/circlemind-ai/fast-graphrag/blob/main/fast_graphrag/_services/_information_extraction.py : extraction, gleaning, query entity extraction (read 20261030 19:00 UTC)
13. https://github.com/circlemind-ai/fast-graphrag/blob/main/fast_graphrag/_services/_chunk_extraction.py : chunking and chunk ids (read 20261030 19:00 UTC)
14. https://github.com/circlemind-ai/fast-graphrag/blob/main/fast_graphrag/_graphrag.py : insert and query orchestration, `QueryParam` (read 20261030 19:00 UTC)
15. https://github.com/circlemind-ai/fast-graphrag/blob/main/fast_graphrag/__init__.py : default configuration (read 20261030 19:00 UTC)
16. https://github.com/circlemind-ai/fast-graphrag/blob/main/fast_graphrag/_services/_base.py : `max_gleaning_steps` default (read 20261030 19:00 UTC)
17. https://github.com/circlemind-ai/fast-graphrag/blob/main/fast_graphrag/_llm/_llm_openai.py : default LLM and embedding models (read 20261030 19:00 UTC)
18. https://github.com/circlemind-ai/fast-graphrag/blob/main/fast_graphrag/_storage/_vdb_hnswlib.py : hnswlib parameters (read 20261030 19:00 UTC)
19. https://github.com/circlemind-ai/fast-graphrag/blob/main/fast_graphrag/_prompt.py : prompt templating of `domain`, `example_queries`, `entity_types` (read 20261030 19:01 UTC)
20. https://github.com/circlemind-ai/fast-graphrag/blob/main/fast_graphrag/_storage/_ikv_pickle.py and `_default.py` in the same folder : pickle key-value store, default storage classes (read 20261030 19:00 and 19:01 UTC)
21. https://api.github.com/repos/circlemind-ai/fast-graphrag/git/trees/main?recursive=1 : file tree (30 Python files in the package; benchmark files; no MCP files) (read 20261030 18:59 UTC)
22. https://github.com/circlemind-ai/fast-graphrag/issues and https://github.com/circlemind-ai/fast-graphrag/pulls : open issues and PRs, comments, events; issues #43, #101, #102, #103, #104, #105, #108, #109, #110, #111, #112, #113 (read through the API 20261030 18:58 to 19:01 UTC)
23. https://api.github.com/orgs/circlemind-ai/repos : repositories by push date (read 20261030 19:01 UTC)
24. https://circlemind.co : current products, footer (read 20261030 18:59 and 19:01 UTC)
25. https://docs.circlemind.co/quickstart (301 to https://docs.smooth.sh/) : redirect and the Smooth docs front page (read 20261030 18:59 and 19:01 UTC)
26. https://arxiv.org/abs/2405.14831 : HippoRAG versions and venue (read 20261030 18:59 UTC)
27. https://arxiv.org/abs/2506.05690 : GraphRAG-Bench, Tables 3, 4, 9 to 11 and 15 (read 20261030 19:02 UTC, via the alphaXiv PDF reader)
28. https://arxiv.org/abs/2511.05549 : AGRAG, Table II and baseline settings (read 20261030 19:02 UTC, via the alphaXiv PDF reader)
29. The July 2026 investigation notes for this project (internal, written 20260725 15:30 UTC, superseded by this entry; no URL). Cited only for what July recorded, and for the July analysis marked as unverified above (read 20261030 18:58 UTC)
30. [The X2 rehearsal of fast-graphrag against a stub model](../experiments/x2-index-cost/rehearsal/fast-graphrag.md) : a local run of commit `23b3a1b` (no release or tag exists; read 20261102 10:27 UTC) and of the PyPI 0.0.5 wheel, whose indexing files are byte-identical; licence file hash equal at the commit, in the dist and in the wheel (read 20261102 10:36 and 10:54 UTC). Counts are for the stub's answers, not a real model's.
