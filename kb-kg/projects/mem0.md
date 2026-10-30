---
slug: mem0
repo: mem0ai/mem0
tier: deep
category: agent-memory
snapshot: 20261030 19:29 UTC
---

# Mem0

Reading times: the repository metadata, README, licence, release list, PyPI index, file tree and the migration and
graph-memory documents were read at 20261030 19:29 UTC; source files, the changelog and the benchmark pages between
19:30 and 19:38 UTC. Each source below carries its own time. **(computed)** marks arithmetic done here on figures
quoted from a source. **Unstated** means the sources read say nothing.

| | |
|---|---|
| Repository | https://github.com/mem0ai/mem0 [1] |
| Licence | Apache-2.0, from the `LICENSE` file (the standard Apache text; the appendix line reads "Copyright [2023] [Taranjeet Singh]") [3]. GitHub's API, the README ("Apache 2.0") and `pyproject.toml` agree [1][2][3]. No disagreement found. |
| Language | Python (GitHub primary language) [1]; a TypeScript SDK sits in `mem0-ts/`, a FastAPI server with a dashboard in `server/`, plus a CLI and many integrations [6][30] |
| Stars, forks | 68,112 and 8,073 (20261030 19:29 UTC; identical to the 19:13 snapshot) [1][32] |
| Created, last push | 20230620 08:58 UTC, 20261029 22:00 UTC [1]. The push time covers any branch; the head of `main` is 20261026 14:51 UTC [25]. |
| Latest release | GitHub's latest-release call returns `ts-v3.3.1`, 20260925 17:36 UTC [4]. The Python package `v2.2.1` was released the same minute [4][5]. |
| Status | active (pushed within 90 days); not archived [1]. The snapshot sets no flag for this repository [32]. |
| Paper, docs | arXiv 2504.19413, one version, 20250428, no venue listed [14]; docs at https://docs.mem0.ai, mirrored in the repository's `docs/` folder [6][7] |

## What it is

Mem0 ("mem-zero") is a memory layer for LLM applications and agents. An application sends it conversation
messages; an LLM distils them into short fact-like memories, which are stored with embeddings and searched
later by user, agent or run [2][11]. The project's own description is "The Memory Layer for AI Agents" [1]. The
README links the hosted Mem0 Platform and carries a Y Combinator S24 badge [2].

It comes in three forms: a library (`pip install mem0ai`, `npm install mem0ai`), a self-hosted server
(`docker compose`), and the hosted Platform, which the library's `MemoryClient` calls [2][12]. The open-source
code and the Platform share an API shape but not all features (see "What is open source and what is Platform").
That split matters for reading the project's published numbers.

Star counts for context: 55.47 per day on average since creation, 11.85 forks per 100 stars, 411 contributors
in the snapshot. Live reads: 407 contributors, 892 open items by the API's open-issues count, and 454 open pull
requests from the pulls endpoint (whether the 892 includes the pull requests was not checked) [1][25][32]. The
README does not explain a launch spike, and this entry draws no conclusion from the counts.

## How it works

### Components and defaults

A `Memory` (sync) or `AsyncMemory` object wires together an LLM, an embedder, a vector store, an optional
reranker and a local SQLite history database. Defaults: OpenAI `gpt-5-mini`, OpenAI `text-embedding-3-small`,
a local Qdrant store (default path under the system temp folder), history in a SQLite file in the user's home
folder, no reranker [11][27]. The code lists 25 vector stores, 18 LLM provider modules, 12 embedder modules and
5 reranker modules [6][11]. `mem0/memory/main.py` is 3,912 lines and holds both classes [11].

### Write path now (Python 2.x, algorithm called "V3" in the docs)

`add()` has an `infer` switch. With `infer=False` each message is stored as is. With the default, the code runs
a phased pipeline [11]:

| Phase | What happens | LLM? |
|---|---|---|
| 0 | Read the last 10 messages for this scope from SQLite | no |
| 1 | Embed the new messages, fetch the 10 nearest existing memories | no (embedding) |
| 2 | **One** extraction call. The prompt gets the existing memories, new messages, recent messages and custom instructions. Its only operation is ADD; it may also name existing memories a new one relates to | yes |
| 3 to 5 | Batch-embed the new texts, then drop any whose MD5 hash equals a hash among the 10 retrieved neighbours or earlier in the same batch | no |
| 6 | Batch insert into the vector store, then write ADD rows to the history table | no |
| 7 | Extract entities with spaCy (no LLM), embed them, and link each to the memory ids that mention it in a second collection named `{collection}_entities`; an entity matches an existing one by exact normalised text or a similarity score of at least 0.95 | no |
| 8 | Save the messages to the rolling window | no |

Deduplication is therefore exact-text and limited to neighbours already retrieved; near-duplicates are left to
the LLM seeing the neighbours in its prompt [11]. Nothing is updated or deleted by `add()`. The
`update()` and `delete()` methods still exist but are caller-driven [11][12]. The paper describes a
conversation summary as extraction context [15]; the code path read passes none [11]. The extraction prompt
asks the model for `linked_memory_ids` on each new memory [11]; a search of `main.py` found that field used
only on entity records, so the memory-level links are neither stored nor read in the open-source code [11]. The
changelog says memories "accumulate via `linked_memory_ids`" [9].

If the vector store rejects every extracted memory, v2.2.1 raises `VectorStoreError` instead of reporting ADD
events [9].

### Write path before April 2026 (Python 1.x, TypeScript 2.x)

Read at tag `v1.0.11` [10]: one LLM call extracted facts. For each fact the code embedded it and fetched the
5 nearest memories. A second LLM call then returned, per fact, ADD, UPDATE, DELETE or NONE against those
neighbours, with ids replaced by small integers to resist hallucinated ids [10]. The paper states 10 similar
memories for its runs [15]; the default in the v1.0.11 code is 5 per fact [10]. The paper calls the choice a
"tool call" [15]. An independent audit measured how often the model chose to mutate (see Evidence) [16].

### Read path now

`search()` takes `filters` (it must hold `user_id`, `agent_id` or `run_id`), `top_k` 20, `threshold` 0.1 and
`rerank` False [7][11]. Steps [11]:

1. Lemmatise the query for BM25 and extract its entities with spaCy.
2. Embed the query; run a semantic search for `max(4 x top_k, 60)` candidates.
3. Run the store's keyword search, if it has one; normalise BM25 scores with a sigmoid whose midpoint depends
   on query length.
4. For up to 8 query entities, search the entity collection (top 500, similarity of at least 0.5); each linked
   memory gets a boost of similarity x 0.5, damped when an entity links to many memories.
5. Candidates come **only** from the semantic list. Those below the threshold on the semantic score alone are
   dropped. The rest score `(semantic + bm25 + entity) / max_possible`, where the divisor is 1.0, 1.5, 2.0 or
   2.5 depending on which signals exist [11]. BM25 and entity signals reorder; they do not add candidates [7].
6. Optional reranker (Cohere, Hugging Face, sentence-transformers, ZeroEntropy or an LLM) [6][11].

No LLM runs at query time unless the optional LLM reranker is chosen. Without the `[nlp]` extra (spaCy and a model download, Python 3.10 to 3.12) there
is no entity signal and no lemmatised BM25, so search is semantic only; of the 25 vector stores, 15 gained a
`keyword_search` method, and the rest log a warning and fall back [7][9][11]. The README's hybrid-search
claims therefore depend on an optional install and on the store chosen.

### What "graph memory" has meant

| Period | What it was | Source |
|---|---|---|
| Paper, April 2025 ("Mem0g") | A directed labelled graph in Neo4j. An LLM extracts entities with types, then relation triplets; a node matches an existing one above a similarity threshold; an LLM resolver marks conflicting relations invalid instead of deleting them. Retrieval: entity-centred subgraph plus a "semantic triplet" match of the whole query | [15] |
| Python 0.1.x to 1.x (open source) | `enable_graph` plus a `graph_store` block (Neo4j, Memgraph, Kuzu, Apache AGE, Neptune). In the `v1.0.11` code each `add()` makes three more LLM calls (entities, relations, which old relations to delete); `search()` extracts query entities with the LLM, walks the graph, and re-ranks triples with BM25 (top 5) in a `relations` field. I did not find the paper's triplet-embedding match in that file; the code at the paper's date was not read | [10] |
| 20260414 (Python 2.0.0, TypeScript 3.0.0) | The external graph integration is **deleted** from open source (`mem0/graphs/` and the graph memory modules, about 4,000 lines per the migration guide). `relations` is no longer returned | [7][9] |
| Platform now | "Graph Memory" is built in and always on. Entities (proper nouns, quoted text, noun compounds) are nodes; memories sharing an entity are connected. The docs state it assigns **no typed relationships** (it will not record a "manages" edge). It changes ranking only; there is no graph payload. The interactive Graph view needs the Pro or Enterprise plan | [8][13] |

So the graph in the paper is not the graph in the current product. The current open-source code keeps the same
idea in a reduced form: the `_entities` collection is the shared-entity link structure, without edges or types
[11][12]. The paper's +1.56-point graph result (below) belongs to the first row only.

### What is open source and what is Platform

The repository holds the library, the server, the clients, the CLI, integrations and docs [6]. I found no
Platform server code in the file tree; absence in a listing is not proof [6]. The README says the headline scores
"reflect Mem0's managed platform, which includes proprietary optimizations not available in the open-source SDK"
[2]. The project's comparison page lists the differences [12]:

| Feature | Open source | Platform |
|---|---|---|
| Add, search, get, update, delete, history; scoping by `user_id`, `agent_id`, `run_id` | yes | yes |
| Entity-based ranking, reranking, expiration date, custom instructions, multimodal | yes | yes |
| LLM, embedder, vector store | you provision them | run by Mem0 |
| `app_id`, organisations, projects, member roles, project event feed | no | yes |
| Graph Memory (native) | removed from 20260414 | yes, all plans |
| Temporal Reasoning (`timestamp`, `reference_date`) | raises a "not supported" error; the code confirms it | yes |
| Memory Decay | not supported | opt-in per project |
| Dream (background consolidation: merge duplicates, supersede facts) | no | yes |
| Custom categories, webhooks, export, batch update or delete (1,000), feedback, summaries | no | yes |
| Hosted MCP server (`mcp.mem0.ai`, needs a Platform account) | no | yes [28] |

User Profiles are in the client since 2.2.0; the comparison page leaves them out and calls the feature unfinished [9][12].

Two tensions inside the project's own pages. The comparison page says the two "run the same core
extraction and retrieval logic", while the README and both blog posts say the best scores include optimisations
the open source lacks [2][12][18]. The comparison page also lists a web dashboard as "Not included" in open source,
yet the README and `server/` ship a self-hosted dashboard (149 files under `server/dashboard`) [2][6][12][30].

### Major versions

| Date (UTC) | Release | Change to API and storage | Src |
|---|---|---|---|
| 20240518 | Python 0.0.1 on PyPI | First package. 192 releases to date | [5] |
| 2024 to 2025 | Python 0.1.x | Graph store and `enable_graph` added (earliest commit on `graph_memory.py`: 20240904); output format `v1.1` makes results `{"results": [...]}`, with `relations` when the graph is on | [9][10][25] |
| 20251016 | Python 1.0.0 | Metadata filters and reranker support in open source; assistant-memory retrieval; async mode on by default | [9] |
| 20260414 | Python 2.0.0 (PyPI final 20260416), TypeScript 3.0.0, Platform "V3" | Two LLM calls become one, ADD only; hybrid search; entity collection; SQLite message window; graph store deleted; defaults `top_k` 100 to 20, `threshold` none to 0.1, `rerank` True to False; entity ids move into `filters` for `search`/`get_all` (top-level ids raise `ValueError`); `custom_fact_extraction_prompt` renamed `custom_instructions`; `custom_update_memory_prompt` deprecated; default model `gpt-5-mini`; client calls `/v3/memories/add/` and `/v3/memories/`; `org_id` and `project_id` dropped; TypeScript camelCase and `limit` to `topK` | [5][7][9][29] |
| 20260923, 20260925 | Python 2.2.0, 2.2.1 | User Profiles in the client; `add()` stops reporting rejected inserts | [9] |

The docs call the 20260414 change "v2 to v3" (of the algorithm); SDK numbers differ by language. Scores are
"computed differently", so absolute thresholds need retuning [7]. Whether existing memories get entity links after
an upgrade is unstated in the guide [7].

### Agent interface

Library calls (`Memory`, `MemoryClient`), a REST API from `server/`, a CLI whose first command signs an agent up
for a Platform key, a hosted MCP server, "skills" files for coding assistants, and plugins under `integrations/`
for Claude Code, Codex, Cursor, Kimi, DeepSeek, OpenClaw, Vercel AI SDK, Strands, n8n and Zapier [2][6][28].

## Cost and operating profile

| Operation | Now (2.x) | Before (1.x) | Src |
|---|---|---|---|
| `add()` LLM calls | 1 extraction call; entity linking is local spaCy | 2 calls (facts, then actions); with graph, 3 more | [10][11] |
| `search()` LLM calls | 0 (reranker optional) | 0 for vectors; 1 more for the graph entity step | [10][11] |
| Extra store | second collection `{name}_entities`, SQLite history and message window | optional graph database | [7][11] |

What it needs: an LLM key (OpenAI by default), an embedder, a vector store, and for the entity signal spaCy plus
`en_core_web_sm` [7][27]. It can run locally: the project names Ollama, local vector stores and no usage billing
as the open-source case, and the code has Ollama, LM Studio, vLLM and FAISS modules [6][12]. A fully local run was
not tested here. Telemetry to a PostHog host is on by default (`MEM0_TELEMETRY` unset means true), sampled at 10%
for hot-path events; open-source builds can also print Platform notices, whose committed config has them disabled
with empty text [9][26].

Platform pricing, from the repository's pricing page (added 20261026): Starter, Growth and Pro are no longer sold to
new accounts; the free plan pays for model calls for 30 days (10,000 adds and 1,000 retrievals a month), then
requires the customer's own LLM key. The page estimates about $3.55 to $5.34 per 1,000 adds with the recommended
models [28]. Self-reported benchmark runs average about 7,000 tokens per retrieval call at a top-200 budget [13].

## Evidence

Classes: **first-party** (Mem0), **competitor**, **independent** (no stake stated). The cross-project table is in
[papers-benchmarks section 3.2](../papers-benchmarks/README.md#32-graph-memory-against-plain-retrieval-for-agents).

### First-party: the paper (April 2025)

LoCoMo (10 conversations, about 600 dialogues and 26,000 tokens each, about 200 questions each; the adversarial
category excluded), GPT-4o-mini for all LLM steps, an LLM judge (J) averaged over 10 runs [15]. The judge model's
name is unstated in the sections read. Table 2 [15]:

| Method | Overall J | Memory tokens | Total latency p95 (s) |
|---|---|---|---|
| Full context | 72.90 | 26,031 | 17.117 |
| **Mem0g (graph)** | 68.44 | 3,616 | 2.590 |
| **Mem0** | 66.88 | 1,764 | 1.440 |
| Zep | 65.99 | 3,911 | 2.926 |
| Best RAG (256 tokens, k=2) | 60.97 | n/a | n/a |
| LangMem | 58.10 | 127 | 60.40 |
| OpenAI memory | 52.90 | 4,437 | 0.889 |
| A-Mem (re-run) | 48.38 | 2,520 | 4.374 |

What each claim measures: "26% relative over OpenAI" is 66.88 against 52.90 (computed: 1.264). "Graph about 2% higher" is
+1.56 points (computed). "91% lower p95 latency" compares total latency (retrieval plus answer) with the
full-context baseline, 1.440 s against 17.117 s (computed 91.6%). "Over 90% token saving" compares retrieved memory
tokens with full context (computed 93%). The full-context baseline scores higher than either Mem0 variant [15]. Per
category, the graph variant is higher on open-domain (75.71 against 72.93) and temporal (58.13 against 55.51) and
lower on single-hop (65.71 against 67.13) and multi-hop (47.19 against 51.15) (Table 1) [15]. OpenAI's system was
given all its extracted memories at once, not a retrieved subset [15].

### First-party: the 2026 algorithm

| Claim | Number | Setup stated | Src |
|---|---|---|---|
| LoCoMo, old to new | 71.4 to 92.5; the OSS guide and May post give 91.6 for the April algorithm | single pass, top 200, about 6,956 tokens; LoCoMo size given as 1,540 questions on the research page and blog, but "about 300" in the benchmark repository README | [2][7][13][17][19][23] |
| LongMemEval | 67.8 to 94.4 (93.4 for the April algorithm) | 500 questions; about 6,787 tokens | [13][19] |
| BEAM | 64.1 at 1M tokens, 48.6 at 10M; no old score | about 6,700 to 6,900 tokens | [2][13] |

The +0.9 and +1.0 steps from the April figures to the headline come with Temporal Reasoning, which the May post and
the comparison page place on the Platform [12][19] (computed). The README and the evaluation page say the runs use "the same production-representative model stack"; the
evaluation page and the blog add a ±1 point judge noise; none of the pages names the extraction, answering or
judge model [2][13][17][18]. The README says open-source users "should expect
directionally similar gains but not identical numbers" [2]. The per-category LoCoMo scores differ between pages:
94.6, 95.4, 82.3, 92.5 on the blog and research page; 91.2, 91.3, 72.7, 92.0 on the docs page, all with an overall of 92.5
[13][17][18]; I could not reconcile them. The open-source defaults (top 20) differ from the benchmark budget (200) [7][13].
The harness `mem0ai/memory-benchmarks` (Apache-2.0, 132 stars, created 20260330) runs both Platform and
self-hosted backends [23]. A "DolphinBench" of 600 tool tasks is announced, not read [17].

### Independent

| Study | What it measured | Result for Mem0 | Src |
|---|---|---|---|
| Bao et al. 2610.30755 (20261022, one version) | Audit of Mem0 `1.0.11` write decisions on LoCoMo and LongMemEval; other tests with Mem0 `2.0.11` | UPDATE and DELETE were 4.39% of 33,902 write decisions on LoCoMo and 2.46% of 428,858 on LongMemEval; effective mutations 1.90% and 1.34%. Replacing UPDATE with ADD and DELETE with NONE moved LoCoMo accuracy from 67.36 to 69.42, with no category lower | [16] |
| Same study, main tables | Raw-RAG (dense retrieval plus reranking over raw history) against 12 memory systems in Table 3 | Mem0 LongMemEval 66.40 against Raw-RAG 87.53; MemoryAgentBench 41.28 and 41.95 against 48.32 and 53.41 (two readers); MEME 27.76 and 33.16 against 39.30 and 43.19. The LoCoMo GPT-4o-mini cells for Mem0 equal the paper's published values; the origin of the other Mem0 cells is not marked in what I read | [16] |
| Same study, note | The paper's per-category scores weighted by LoCoMo question counts (841, 282, 321, 96) give 62.14, not the published 66.88; I repeated the arithmetic | | [16] (computed) |
| Penfield audit of LoCoMo (dev.to, posted "April 4", year not shown; the text refers to March 2026) | The benchmark itself | 99 score-corrupting errors in 1,540 questions (6.4%); the judge accepted 62.81% of deliberately wrong, topically close answers. Mem0 is cited only through one issue; the author's affiliation is unstated | [22] |

The Bao study proposes the Raw-RAG baseline that it ranks first, and Table 3 does not mark which Mem0 cells the
authors re-ran [16]. Its write-policy audit used the pre-2026 write policy; it is consistent with the move to
ADD-only but does not test the new pipeline's own write decisions. Issue #3944 (opened 20260128) reports a LoCoMo
score near 0.20 through the Platform, with memories carrying the current date instead of the dataset's dates; a
maintainer replied on 20260324 that the stored text looked fabricated and would be investigated, and another closed
it as fixed on 20260327 [24].

### Competitors (not independent)

Zep's rebuttal says Mem0 ran Zep with both speakers as the same user, appended timestamps to message text, and
searched sequentially; it reports Zep at 75.14 against 65.99 in Mem0's paper (post dated 20250506, modified 20260603)
[20]. Letta reports an agent using a file and GPT-4o-mini at 74.0 against Mem0's graph variant at 68.5, and says Mem0
did not answer questions about how it ran MemGPT (20250812) [21]. Neither is a replication of Mem0's own numbers.

### Where the README or docs go beyond the code

- "Temporal Reasoning" appears in the README's list of what changed, but `search()` in the open source raises an error for
  `reference_date` [2][11].
- "Entity linking" and "BM25" need the `[nlp]` extra and a store with `keyword_search` [7].
- The graph evidence in the paper concerns a feature the open source deleted [7][15].

## Direction

The documented Platform-only features (native graph, temporal reasoning, decay, Dream) keep the Platform ahead of
the open source; the old open-source graph page redirects to the Platform page, and the repository carries a
migration script and a skill for moving projects from open source to the Platform [2][6][8][12][25]. Of the 15 `feat`
commits in the last 90 days, 11 touch integrations, plugins or the CLI (computed from subject lines): coding-agent
plugins, Strands, DeepSeek, Kimi, Hermes, and a CLI with "sign up as an agent" [2][25]. The blog and evaluation page
name the open problems as temporal reasoning, event ordering and multi-session reasoning at 10M tokens [13][18].
A roadmap file: unstated (none in the top-level listing) [6].

## Recent changes

Commits to `main` since 20260801, counted by paging the commits API: 136 (August 79, September 48, October 9 to
the 26th) (computed). By type: fix 59, docs 38, feat 15, chore 8, refactor 3, perf 1, other 12 [25]. October's nine
commits are two dependency security patches, four documentation or README changes and three fixes; the monthly
count fell from 79 to 48 to 9, and whether work moved to other branches is unstated [25]. Releases: Python 2.0.15
(20260801) to 2.2.1 (20260925), with no release listed after 20260925 [4][5].

- 20260805 and 20260811: docs recast graph memory as a Platform feature and redirect the old page [25].
- 20260814: pull requests must link an accepted issue (CI gate) [25].
- 20260923: User Profiles added to the client (Platform) [9].
- 20260925 (Python 2.2.1): `add()` no longer reports rejected inserts as successful [9].
- 20261007: stop writing a Google service-account key to DEBUG logs in one vector store [25].
- 20261026: pricing FAQ added [25][28].

## Sources

1. https://api.github.com/repos/mem0ai/mem0: stars, forks, licence, dates, archived flag (read 20261030 19:29 UTC)
2. https://github.com/mem0ai/mem0 (README via API): features, benchmark table, caveat on platform optimisations, licence line (read 20261030 19:29 UTC)
3. `LICENSE` at the repository root (read 20261030 19:29 UTC); `pyproject.toml` and `mem0-ts/package.json` licence fields (read 19:34 UTC)
4. https://api.github.com/repos/mem0ai/mem0/releases: release list and dates (read 20261030 19:29 UTC)
5. https://pypi.org/pypi/mem0ai/json: 192 releases, version dates (read 20261030 19:29 UTC)
6. https://api.github.com/repos/mem0ai/mem0/git/trees/HEAD?recursive=1: layout, provider modules (read 20261030 19:29 UTC)
7. https://github.com/mem0ai/mem0/blob/main/docs/migration/oss-v2-to-v3.mdx: breaking changes, graph removal, algorithm (read 20261030 19:29 UTC)
8. https://github.com/mem0ai/mem0/blob/main/docs/platform/features/graph-memory.mdx: Platform graph memory (read 20261030 19:29 UTC)
9. https://github.com/mem0ai/mem0/blob/main/docs/changelog/sdk.mdx: release notes (read 20261030 19:30 UTC)
10. `mem0/memory/main.py`, `mem0/memory/graph_memory.py`, `mem0/configs/prompts.py` at tag `v1.0.11` (commit 144627c4): old write and graph paths (read 20261030 19:30 UTC)
11. `mem0/memory/main.py`, `mem0/utils/scoring.py`, `mem0/utils/entity_extraction.py`, `mem0/configs/prompts.py`, `mem0/configs/base.py`, `mem0/vector_stores/configs.py` at `main` head 26cdefb (20261026 14:51 UTC): current pipeline (read 20261030 19:30 to 19:35 UTC)
12. https://github.com/mem0ai/mem0/blob/main/docs/platform/platform-vs-oss.mdx: feature comparison (read 20261030 19:31 UTC)
13. https://github.com/mem0ai/mem0/blob/main/docs/core-concepts/memory-evaluation.mdx: benchmark tables, budget, caveats (read 20261030 19:31 UTC)
14. https://arxiv.org/abs/2504.19413: abstract, version history (read 20261030 19:31 UTC)
15. https://arxiv.org/html/2504.19413v1: method, setup, Tables 1 and 2 (read 20261030 19:32 UTC)
16. https://arxiv.org/abs/2610.30755 (19:31 UTC) and https://arxiv.org/html/2610.30755v1 (19:33 UTC): independent audit and tables (read 20261030)
17. https://mem0.ai/research: LoCoMo, LongMemEval, BEAM claims (read 20261030 19:33 UTC)
18. https://mem0.ai/blog/mem0-the-token-efficient-memory-algorithm: April 2026 post, updated 20260928 (read 20261030 19:34 UTC)
19. https://mem0.ai/blog/the-token-efficient-memory-algorithm-now-has-temporal-reasoning: May 2026 post (read 20261030 19:34 UTC)
20. https://www.getzep.com/blog/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/: competitor rebuttal (read 20261030 19:34 UTC)
21. https://www.letta.com/blog/benchmarking-ai-agent-memory: competitor claim (read 20261030 19:37 UTC)
22. https://dev.to/penfieldlabs/we-audited-locomo-64-of-the-answer-key-is-wrong-and-the-judge-accepts-up-to-63-of-intentionally-33lg: LoCoMo audit (read 20261030 19:34 UTC)
23. https://github.com/mem0ai/memory-benchmarks: evaluation harness, README and metadata (read 20261030 19:34 UTC)
24. https://github.com/mem0ai/mem0/issues/3944: reproduction issue and comments (read 20261030 19:34 and 19:38 UTC)
25. GitHub API: commits since 20260801 (paged, 136), contributors, open pull requests, file history of `graph_memory.py` (read 20261030 19:35 UTC)
26. `mem0/memory/telemetry.py`, `notices.py`, `oss_notices_config.json` on `main`: telemetry and notices (read 20261030 19:35 UTC)
27. https://github.com/mem0ai/mem0/blob/main/docs/open-source/overview.mdx and `mem0/configs/vector_stores/qdrant.py`: defaults (read 20261030 19:35 UTC)
28. `docs/platform/mem0-mcp.mdx` and `docs/platform/pricing.mdx` on `main`: hosted MCP and plans (read 20261030 19:35 UTC)
29. https://github.com/mem0ai/mem0/blob/main/docs/migration/platform-v2-to-v3.mdx: Platform migration (read 20261030 19:36 UTC)
30. `server/README.md` and `server/docker-compose.yaml` on `main`: self-hosted server (read 20261030 19:35 UTC)
31. [papers-benchmarks/README.md](../papers-benchmarks/README.md): section 3.2 and the Mem0 paper row (read 20261030 19:29 UTC)
32. [landscape/20261030_1913-github/repos.tsv](../landscape/20261030_1913-github/repos.tsv): snapshot row, columns for stars per day, forks per 100 stars, flags and contributors (read 20261030 19:29 UTC)
