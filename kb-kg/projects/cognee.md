---
slug: cognee
repo: topoteretes/cognee
tier: deep
category: agent-memory
snapshot: 20261030 19:29 UTC
---

# Cognee

Reading times: the repository metadata, licence file and README at 20261030 19:29 UTC; source files between
19:30 and 19:36 UTC; web pages between 19:31 and 19:37 UTC. Each source below carries its own time. Star
and fork counts were re-read at 19:37 UTC (32,933 stars, 3,438 forks) [1].

| | |
|---|---|
| Repository | https://github.com/topoteretes/cognee |
| Licence | Apache-2.0, from the `LICENSE` file ("Copyright 2024 Topoteretes UG" in the appendix notice) [3]. GitHub's API, `pyproject.toml` and PyPI all say Apache-2.0 [1][5][28]. The README carries only a badge that reads the licence from GitHub, so nothing disagrees [4]. |
| Language | Python (GitHub's primary language) [1]. A `cognee-frontend` folder exists; its language was not read [1]. A Rust SDK (`cognee-rs`) and a TypeScript SDK are separate [4][30]. |
| Stars, forks | 32,932 and 3,438 (20261030 19:29 UTC) [1] |
| Created, last push | 20230816 16:16 UTC, 20261030 17:35 UTC (any branch) [1] |
| Latest release | v1.6.6, 20261029 21:33 UTC [2]; PyPI 1.6.6 uploaded 20261029 21:40 UTC [28] |
| Status | active (pushed 0 days before the snapshot); not archived [1][32] |
| Paper, docs | arXiv 2505.24478, v1 only, 20250530 [19]; docs at https://docs.cognee.ai/ [4]; two benchmark reports inside the repository [17][18] |

Snapshot flags: none. The landscape snapshot of 20261030 19:13 UTC gives 28.12 stars per day over 1,171
days and 10.44 forks per 100 stars, and raises neither `fast-growth` (150 stars per day or more) nor
`low-forks` (under 3 forks per 100 stars) [32]. These are heuristics. Live counts at 19:37 UTC: 766 open
issues and 299 open pull requests [30]. The snapshot lists 333 contributors; a paginated live list at 19:35
UTC returned 301 logins, and the difference was not investigated [30][32]. The README's news section lists
releases, not a launch [4]. This entry draws no conclusion about how the stars arose.

## What it is

The README titles Cognee "The Free Open-Source AI Memory Platform for Agents" and says it turns documents,
code and conversations into a self-hosted knowledge graph [4]. The code is a Python SDK with a REST API, a CLI, a
web UI and an MCP server. Data goes in through `remember`, comes out through `recall`, is enriched by
`improve` and removed by `forget` [4][13]. The earlier low-level calls `add`, `cognify` and `search` remain
and are what the memory API calls underneath [13].

It stores three kinds of data side by side: a graph of entities and relations, vector embeddings of chunks,
entities and summaries, and relational metadata (users, datasets, permissions, pipeline runs) [13][21]. A
hosted product, Cognee Cloud, runs the same API [22][23]. The company named in the licence is Topoteretes UG,
Berlin [3][5].

The repository is large. The file tree held 5,646 paths at 19:29 UTC [1], and `remember.py` alone has 2,315
lines [15]. This entry covers the main path; code graphs, document-structure sync, skills and the many
connectors were not read in depth.

## How it works

### From raw data to graph

`remember` without a session runs `add`, `cognify` and then `improve` (the default `self_improvement=True`)
[13][15]. The table follows the order of the code. "LLM" means a generative model call; embedding calls are
listed separately because every storing step embeds.

| Stage | What it does | LLM? |
|---|---|---|
| `add` | Resolves text, local or S3 paths, web URLs, binary streams and git repository URLs; extracts text; writes a Data record per item to the relational database; grants the user permissions. Re-adding identical content is a no-op; changed content under the same name raises and needs `update` [15] | No for text and documents. Images use OCR or a vision model; audio is transcribed [15] |
| Classify, chunk | Wraps each item in a typed Document, then splits it. Default chunker is paragraph-based; chunk size defaults to the smaller of the embedding limit and half the LLM's maximum completion tokens [6] | No |
| Early chunk indexing | A first pipeline run, on by default, writes chunk and document nodes to the graph and embeds the chunk text. Chunk search, BM25 and hybrid retrieval answer before any entity exists [6][7][13] | No (embeddings only) |
| Graph extraction | One structured-output LLM call per chunk, validated against a graph model (default `KnowledgeGraph`: nodes with id, name, type, description; edges). The system prompt asks for basic type labels, for dates as `Timestamp` nodes linked by `..._at` relations, and for coreference resolution. Date hints from the `dateparser` library are computed beforehand and passed in the prompt [8][13] | Yes, one call per chunk. The GLiNER extractor replaces it with a local model [6][7] |
| Ontology step | Optional. Renames and filters the extracted graph (see below) [9] | No |
| Construction | Entity ids are derived from the normalised name (lower case, apostrophes removed), so equal names merge across chunks and documents. The type is not part of the id [8]. Edges that already exist in the store are not attached again [8] | No |
| Summaries | Default `from_extraction`: joins the extracted types and relation texts, so a chunk with no relations gets no summary. `llm` makes one call per chunk [7][8] | No by default |
| `add_data_points` | Flattens data points to nodes and edges, deduplicates, writes the graph, and embeds the indexed fields (chunk text, entity names, summary text, relationship names under an `EdgeType_relationship_name` index). Triplet embeddings were removed [13][15] | No (embeddings) |
| Optional ledgers | `PROVENANCE_TRACKING` is off by default [7]. `EDGE_EVIDENCE_ENABLED` records which chunk supports each edge [12] | No |
| `improve` | Nine stages in fixed order: feedback weights, persist session Q&A, persist agent traces, extract agent context, distill sessions, update user preferences, truth subspace (opt-in), conflict review, global context index. The first seven need session ids. Conflict review is on by default; the guide says it needs an LLM and `EDGE_EVIDENCE_ENABLED=true`, whose default was not determined (the template shows it commented out). The global context index is LLM-free by default and feeds dataset routing [12][13][15] | Yes in three stages (agent context, distillation, conflict review); skipped when no LLM is configured |

Two other ingestion routes skip the text path: tabular and database sources go through `dlt` with
deterministic foreign-key edges and no LLM, and code files and repositories use their own task lists
(`get_code_file_tasks`, `get_code_repo_tasks`) [6]. Whether the code tasks call an LLM was not read:
**unstated**.

Every dataset is locked during a run, so `improve`, `cognify`, `add` and `forget` on one dataset queue one
after another (a process-local lock) [13]. `update` diffs new content against stored text and re-extracts
only the chunks it touched [13].

### Query side

`recall` picks a search type with an ordered, first-match rule table and no LLM call. It routes to a code
search, a count search (`BROAD`), a time-scoped search (`TEMPORAL`) or a quoted-phrase lexical search when the
query text matches; everything else goes to `HYBRID_COMPLETION`. It never routes to `CYPHER` [13][14]. With
no LLM configured it returns the assembled prompt instead of an answer [14]. A search that names no dataset
is routed to the best-scoring dataset (top 1 by default, cosine distance cutoff 0.8) using the global
context index [13].

| Search type | What it does | LLM calls at query time |
|---|---|---|
| `HYBRID_COMPLETION` (default) | Chunk lane plus entity lane, optional global-context lane; defaults of 5 chunks, 5 entities and 5 facts [14] | One answer call [14] |
| `GRAPH_COMPLETION` and variants | Triplet search over the `EdgeType_relationship_name` index, then neighbourhood expansion. Variants: chain-of-thought rounds, iterative context extension, query decomposition [14] | One answer call, more in the variants |
| `TEMPORAL` | Hybrid retrieval, then candidates anchored to `Timestamp` nodes in the question's time window move first [14] | An extra call to extract the window |
| `CHUNKS`, `CHUNKS_LEXICAL`, `SUMMARIES` | Vector search over chunks; BM25 over chunks; vector search over summaries [14] | None |
| `BROAD` | Small datasets are shown whole; large ones are loaded into SQLite and answered by one model-written query [14] | Yes |
| `CYPHER`, `NATURAL_LANGUAGE` | Raw Cypher, or an LLM writes Cypher and runs it. Both off unless `ALLOW_CYPHER_QUERY=true` [14] | Natural language: yes |
| `AGENTIC_COMPLETION` | Tool loop bounded by `max_iter`, with skills and tools [14] | Yes, several |
| `CODE`, `SKILLS`, `CODING_RULES` | Code-graph operations, skill discovery, stored rules [14] | None |

Sessions add a cache of recent Q&A and agent traces, read first when a `session_id` is given [13][15].
`improve` later bridges that cache into the permanent graph [13].

### Stores

| Layer | Default | Other built-in | Other, as stated |
|---|---|---|---|
| Graph | Ladybug, an embedded database [11][13] | Neo4j (three per-dataset isolation handlers), Neptune, Neptune Analytics, remote Ladybug, Turso (local file), Postgres as a "demo, not production-ready" graph with no raw Cypher or natural-language search [11][13] | None named |
| Vector | LanceDB [11] | pgvector, Neptune Analytics, Turso (exact cosine scan, no approximate index) [11][12] | Qdrant, Weaviate, Milvus and ChromaDB as separate community packages [11][12] |
| Relational | SQLite [11][12] | PostgreSQL, Turso (local file) [11][12] | None named |
| Session cache | SQLite [11] | Redis, Postgres, Turso, "tapes" [11] | None named |

The Kuzu entry in this reference records that Kuzu is archived and that a project called Ladybug describes
itself as "formerly known as Kuzu" ([Kuzu](kuzu.md)) [33]. That the `ladybug` package Cognee depends on is
that project was not checked: **unstated**. The code default is `ladybug` and
`kuzu` is accepted as an alias for the same adapter; `.env.template` still sets `kuzu` [11][12]. Per-user,
per-dataset isolation (`ENABLE_BACKEND_ACCESS_CONTROL`, on by default for the API) works only on backends that
register a handler: Ladybug, Neo4j, Postgres, Turso and LanceDB, pgvector and Turso for vectors. Neptune and
unregistered community adapters need it switched off [13][4].

Embeddings default to `openai/text-embedding-3-large`. With no LLM key the code falls back to the local
fastembed model `BAAI/bge-small-en-v1.5` [11]. LLM providers in the code: openai (default), ollama,
anthropic, gemini, mistral, azure, bedrock, llama_cpp, mcp-sampling and a custom endpoint [11]. The default
`llm_model` string in `config.py` is `openai/gpt-5.6-luna`; the name was not checked against any provider
[11]. Structured output defaults to LiteLLM's native path; Instructor and BAML are opt-in [11]. The
maintainers' guide still says extraction uses Instructor, which the config contradicts [11][13].

### Ontologies and schemas

Cognee supports both, and they constrain different things.

| Mechanism | What it constrains | Source |
|---|---|---|
| Custom `graph_model` | A Pydantic `DataPoint` model replaces the generic `KnowledgeGraph`. It becomes the structured-output schema of the extraction call, so the LLM output must fit it. The GLiNER extractor accepts only the generic model [6][8] | [6][8] |
| OWL ontology, `annotate` mode (default) | After extraction, entity types are matched to ontology classes and names to individuals with fuzzy string matching (difflib, cutoff 0.8). Matches are renamed to the canonical term, marked `ontology_valid`, and extended with parent classes and object-property links. Unmatched nodes are kept [9][13][20] | [9][13][20] |
| OWL ontology, `strict` mode | A node survives if its type matched a class or its name matched an individual; other nodes and their edges are dropped. Relationship names are not checked, and there is no domain, range or cardinality reasoning in this check. Chunk text stays stored, so chunk search still returns passages about dropped entities. An empty ontology raises an error [9][20] | [9][20] |
| OWL-RL reasoning | Opt-in (`ONTOLOGY_REASONING=owl_rl`, needs the `owlrl` package): expands inverse, transitive, domain/range, equivalent-class and same-as statements before matching [9][13] | [9][13] |
| GLiNER closed label set | For the local extractor, labels come from the caller, else from the ontology's classes and object properties, else from built-in label banks; at most 20 types per schema [10][12] | [10][12] |

Ontology files are OWL in RDF/XML, read with RDFLib; several paths can be comma-separated [9][20]. In the
LLM extraction path I read, the ontology is not part of the prompt: the call receives the chunk text, the
graph model, an optional custom prompt and date hints, and the ontology is applied afterwards [8]. The
`cognify` docstring says the ontology serves "extraction schema planning and graph integration" [6]. The
only schema planning found is the GLiNER path above [10]. The docs page does not say whether the ontology
enters the prompt [20]. `remember` does not accept `ontology_file_path`; use the environment variable or the
`config` argument [13].

### Agent interfaces

| Interface | What it gives an agent |
|---|---|
| MCP server (`cognee-mcp`) | Three pinned tools, `remember`, `recall`, `forget`, plus `cognify_status` (the maintainers' guide also names a `code_search` tool); stdio, SSE or streamable HTTP; can point at a remote instance. `improve` is reached only through `remember` [16][13] |
| Plugins | Claude Code and Codex memory plugins are set up from the separate `cognee-integrations` repository (Apache-2.0); an OpenClaw plugin is an npm package [4][30] |
| SDKs and HTTP | Python SDK, TypeScript SDK, Rust SDK, REST API and a CLI [4] |
| Migration | A `MemorySource` import reads an exchange format (COGX) from Mem0, Letta, Zep and Graphiti [4][15] |

## Cost and operating profile

**Index time.** One LLM call per chunk for extraction, plus embedding calls for chunks, entity names,
summaries and relationship names. Summaries cost no LLM call by default. `remember` runs `improve` by
default, and `improve` can add LLM calls for conflict review; whether review runs on a default install
depends on the edge-evidence switch noted above: **unstated** [7][12][13][15]. `dry_run=True` returns a stage-level token and cost estimate for the LLM pipeline without
calling the model [6]. No measured cost per document was found: **unstated**.

**Query time.** The default search makes one answer call and one query embedding. Routing is rule-based and
free; some search types add calls (table above) [13][14].

**Needs.** Python 3.10 or later, below 3.15 [5]. The base install pulls in the embedded graph (Ladybug),
LanceDB, SQLite and fastembed, so no database server is required [5][11]. The default LLM is a hosted
OpenAI model, so a key is needed unless a local provider (Ollama, llama.cpp) is set [11]. A GPU is not
mentioned; the README says the keyless path uses the CPU [4].

**Fully local.** Yes, in two ways. With Ollama or llama.cpp models, the whole LLM pipeline runs locally [11].
With no key at all, `GRAPH_EXTRACTOR=auto` picks the local GLiNER model and fastembed, with no LLM call for
extraction or summaries; the template puts the GLiNER download at about 800 MB, and generated answers still
need an LLM [4][12]. The README calls the bundled GLiNER extractor a demo [4].

**Telemetry.** Product telemetry is sent unless `TELEMETRY_DISABLED` is set (it is skipped when `ENV` is
`test` or `dev`). Events carry a machine-level id, the user and tenant ids, and a pseudonymous id derived
from the LLM API key, and go to a proxy URL set in the code [31].

### Open source and hosted

| Part | In the repository (Apache-2.0) | Not in the repository |
|---|---|---|
| Core SDK, API server, CLI, UI, MCP server, Docker images, deployment templates | Yes [4][13][16] | |
| Plugins, integrations, community adapters, Rust SDK | Separate Apache-2.0 repositories: `cognee-integrations`, `cognee-community`, `cognee-rs` [30] | |
| Cognee Cloud | Client side only: `cognee.serve()` connects the SDK to it [22] | Hosted service with a web UI, managed PostgreSQL, LanceDB and Ladybug, role-based access control per dataset, and a "Company Brain" reading Slack, GitHub and Google Drive [22] |
| Pricing | | Free, $0 per month, 1M tokens included; Standard, $1.00 per 1M tokens plus $5 per extra workspace; Enterprise, "contact us", delivered as a bring-your-own-cloud engagement. The page says Cloud runs on `gpt-oss-120b` [23] |
| Production GLiNER extractor | Only a demo version | "Higher accuracy and broader label coverage" under an enterprise licence [12][4] |
| Postgres as the graph store | A demo adapter | "The production-ready version is available as a licensed product" [4] |

The pricing page lists "bi-temporal memory and conflict resolution", provenance on answers and
per-user personalisation under Enterprise [23]. The open repository shipped a conflict-review stage (on by
default) and a conflict-resolution API in v1.6.6, and has provenance and preference features in the code
[2][13]. Whether the Enterprise versions are different implementations is **unstated**. The pricing page
does not say which features are withheld from the open-source version [23].

## Evidence

### Published by the project (self-reported)

| Claim | Where | Setup as the project states it | Limits the project states |
|---|---|---|---|
| BEAM 100K: 0.79 | README and repo report [4][17] | Fixed hybrid retrieval (20 chunks, 20 entities); four evaluation rounds over 20 questions from one held-out conversation; `gpt-5` for ingestion, answering and judging; run standard deviation 0.005 [17] | Two questions per ability, so per-ability numbers are "directional"; the bootstrap interval is not over independent samples [17] |
| BEAM 10M: 0.67 | README and repo report [4][17] | Routing by question type chosen and scored on the same 20 questions; five rounds; ingestion with `gpt-5-mini`; run standard deviation 0.020 [17] | Authors call it exploratory and in-sample; the distributed ingestion cannot be reproduced from public code [17] |
| LoCoMo: about 91% (90.7% and 91.3% in two runs) | Repo report only; the README does not mention it [18] | 1,762 of 1,986 questions. Excluded: 96 open-domain and 143 flagged by two audits (15 overlap). Hybrid retrieval, 20 passages, 20 entities, 20 facts; `gpt-5-mini` answers; `gpt-5.1` judge; Cognee 1.5.4; ingested 20261007 [18] | The ten conversations were used to develop the setup, so it is not held out. The authors say their judge is stricter on dates and factual agreement than some published LoCoMo judges (their Appendix A.5, not read here). At default depth with adapted ingestion: 89.7% (1,580 of 1,761) in one run [18] |
| HotPotQA, 50 random questions, against Mem0 and Zep/Graphiti | cognee.ai evaluation page, published 20250415, updated 20260903 [24] | F1, exact match, DeepEval correctness, human review of failing answers. Results are in images; the text gives no figures [24] | Run by Cognee; gains came from tuning with an internal tool; Graphiti numbers "will be higher in the next iteration"; "LLM as a judge metrics are not reliable" [24] |
| BEAM 10M: 67% against Mem0 at 48.6% (0.48 at top-200 in another passage) | cognee.ai comparison page [25] | No date, no evaluator named; the score widgets on the page show placeholder zeros [25] | Mem0's setting is stated, Cognee's retrieval settings are not [25] |
| Hyperparameter tuning of chunking, graph construction, retrieval and prompts | arXiv 2505.24478 [19] | HotPotQA, TwoWikiMultiHop, MuSiQue; exact match, F1, DeepEval correctness. The abstract page gives no scores [19] | v1 only, marked preliminary. The first author is named on the Cognee site as the company's CEO, so the paper comes from Cognee's own team [19][24] |

The BEAM report says the 0.79 and 0.67 are "not a controlled comparison across scales" [17]. LoCoMo is
described in the [LLM-era timeline](../llm-era/README.md); BEAM is cited here only from Cognee's own report
[17].

### Independent evaluations

None found. What was checked, so the gap is on record:

- arXiv 2610.30755 (20261022) compares 12 agentic memory systems with a plain retrieval baseline on LoCoMo,
  LongMemEval, MEME and MemoryAgentBench. Its baseline list and Tables 3 to 10 have no Cognee row. Only the
  first 100,000 of 232,162 characters of the HTML were read [26].
- A web search at 19:33 UTC found pages from Cognee, Mem0 and Vectorize, and no third-party run [34].
- The Vectorize article (20260315) compares Mem0, Cognee and its own product Hindsight. It gives no Cognee
  scores and says Cognee "has not published a LongMemEval score" [27]. Its publisher sells a competing
  product.
- The reference's [papers and benchmarks page](../papers-benchmarks/README.md) and
  [LLM-era timeline](../llm-era/README.md) hold no Cognee evaluation. That timeline notes that headline memory
  scores in READMEs are the vendors' own.

## Direction

The top level of the file tree has no roadmap file [1]. Direction comes from the README, release notes and
commit subjects. The README leads with "Company Brain", agent memory across runs and ontologies [4]. Release
titles since September name keyless workflows (v1.6.0), Google sync (v1.6.1), temporal search (v1.6.3),
trace processing and code-graph docs (v1.6.5) and conflict resolution (v1.6.6) [2]. Benchmarks now live in
the repository: a BEAM harness and, from 20261013, a LoCoMo harness [18][29]. The GLiNER extractor and the
Postgres graph adapter are labelled demos that point to licensed versions [4][12].

## Recent changes

Window: 20260801 to 20261030. The 30 most recent releases listed span 20260722 to 20261029 and include
dev, release-candidate and pre-release tags [2]. The default branch received 2,821 commits in the window
(by commit date: 682 in August, 1,008 in September, 1,131 in October to the 29th), and 2,387 of them have
non-merge subjects [29]. The most frequent themes in those subjects, by crude keyword count (themes
overlap): session (87), MCP (84), connectors such as Slack, Notion, OneNote, Google and Linear (83), `dlt`
(60), telemetry and observability (59), permissions and tenants (55), temporal and `Timestamp` (54), GLiNER
(33) and conflict (29) [29].

Dated changes, from commit subjects and release notes [2][29]:

- 20260903: low-overhead edge evidence for provenance [29].
- 20260913: LLM-free GLiNER graph extraction backend added; v1.6.0 (20260918) makes keyless text memory work [2][29].
- 20261005: summaries built from extraction instead of an LLM call [29].
- 20261007: v1.6.3 drops the `temporal_cognify` build path and makes dates `Timestamp` nodes by default.
  The release notes say the option was removed; the code keeps the argument as deprecated and ignored [2][6].
- 20261013 and 20261020: LoCoMo benchmark added, then a top-k 5 configuration [29].
- 20261015 to 20261021: Google Calendar, Notion and OneNote connectors [29].
- 20261026: opt-in OWL-RL ontology reasoning and an ontology export endpoint [29].
- 20261029: v1.6.6, a durable conflict-resolution API, conflict review on by default, copying stored
  vectors between stores without re-embedding, and every `dlt` column stored as a value node [2][29].

## Sources

1. https://github.com/topoteretes/cognee : repository metadata and recursive file tree via the GitHub API (stars, forks, licence, dates, topics, 5,646 paths) (read 20261030 19:29 UTC; counts re-read 19:37 UTC)
2. https://github.com/topoteretes/cognee/releases : release list read 19:32 UTC; notes of v1.6.6 and v1.6.3 read 19:35 UTC
3. https://github.com/topoteretes/cognee/blob/main/LICENSE : licence text; header and last 27 lines read, middle not read (read 20261030 19:29 UTC)
4. https://github.com/topoteretes/cognee/blob/main/README.md : self-description, quickstart, interfaces, deployment, benchmark table, news (read 20261030 19:29 UTC)
5. https://github.com/topoteretes/cognee/blob/main/pyproject.toml and NOTICE.md : licence field, Python range, dependencies, company notice (read 20261030 19:30 UTC)
6. https://github.com/topoteretes/cognee/blob/main/cognee/api/v1/cognify/cognify.py : pipeline stages, parameters, extractor and ontology arguments, dry run (read 20261030 19:30 UTC)
7. https://github.com/topoteretes/cognee/blob/main/cognee/modules/cognify/config.py : defaults for summary method, early indexing, provenance, extractor (read 20261030 19:30 UTC)
8. `cognee/tasks/graph/extract_graph_from_data.py`, `extract_graph_and_summarize.py`, `cognee/infrastructure/llm/extraction/knowledge_graph/extract_content_graph.py`, `cognee/infrastructure/llm/prompts/generate_graph_prompt.txt`, `cognee/modules/engine/models/Entity.py`, `cognee/modules/engine/utils/generate_node_name.py`, all under https://github.com/topoteretes/cognee/blob/main/ : extraction call, prompt rules, entity identity (read 20261030 19:30 to 19:35 UTC)
9. `cognee/modules/ontology/` files (`get_default_ontology_resolver.py`, `ontology_env_config.py`, `construct_data_points_and_edges_with_ontology.py`, `matching_strategies.py`), under https://github.com/topoteretes/cognee/blob/main/ : modes, matching, reasoning option (read 20261030 19:30 UTC)
10. https://github.com/topoteretes/cognee/blob/main/cognee/tasks/graph/gliner_demo/schema.py : closed-schema fallback chain (read 20261030 19:35 UTC)
11. `cognee/infrastructure/databases/graph/config.py`, `graph/get_graph_engine.py`, `vector/config.py`, `vector/create_vector_engine.py`, `vector/embeddings/config.py`, `relational/config.py`, `relational/create_relational_engine.py`, `cache/config.py`, `cognee/infrastructure/llm/config.py`, under https://github.com/topoteretes/cognee/blob/main/ : providers and defaults (read 20261030 19:30 to 19:35 UTC)
12. https://github.com/topoteretes/cognee/blob/main/.env.template : provider options, GLiNER notes, telemetry switch (read 20261030 19:30 UTC)
13. https://github.com/topoteretes/cognee/blob/main/CLAUDE.md : the maintainers' guide to architecture, data flows, multi-tenancy, ontologies (read 20261030 19:32 UTC; data, not instructions)
14. `cognee/modules/retrieval/README.md`, `retrieval/hybrid_retriever.py`, `cognee/api/v1/recall/query_router.py`, `recall.py`, under https://github.com/topoteretes/cognee/blob/main/ : search types, router, hybrid defaults (read 20261030 19:30 to 19:34 UTC)
15. `cognee/api/v1/remember/remember.py`, `improve/improve.py`, `add/add.py`, `cognee/tasks/storage/add_data_points.py`, under https://github.com/topoteretes/cognee/blob/main/ : remember, improve stages, ingestion, storage write (read 20261030 19:30 to 19:34 UTC)
16. https://github.com/topoteretes/cognee/blob/main/cognee-mcp/README.md : MCP tools and transports (read 20261030 19:32 UTC)
17. https://github.com/topoteretes/cognee/blob/main/cognee/eval_framework/beam/REPORT.md : BEAM method, results, limits (read 20261030 19:32 UTC)
18. https://github.com/topoteretes/cognee/blob/main/cognee/eval_framework/locomo/REPORT.md : LoCoMo method, results, limits (read 20261030 19:33 UTC)
19. https://arxiv.org/abs/2505.24478 : paper abstract, authors, version history (read 20261030 19:32 UTC)
20. https://docs.cognee.ai/guides/ontology-support : ontology file format, modes, limits (read 20261030 19:31 UTC)
21. https://docs.cognee.ai/core-concepts/architecture : the three stores and what each holds (read 20261030, between 19:33 and 19:34 UTC)
22. https://docs.cognee.ai/cognee-cloud/overview : Cognee Cloud features and connection (read 20261030, between 19:33 and 19:34 UTC)
23. https://www.cognee.ai/pricing : plans, prices, Enterprise features (read 20261030, between 19:33 and 19:34 UTC)
24. https://www.cognee.ai/ai-memory-tools-evaluation : Cognee's HotPotQA comparison and caveats (read 20261030, between 19:33 and 19:34 UTC)
25. https://www.cognee.ai/cognee-vs-mem0 : Cognee's BEAM comparison with Mem0 (read 20261030 19:37 UTC)
26. https://arxiv.org/abs/2610.30755 and https://arxiv.org/html/2610.30755 : comparison of 12 memory systems; Cognee not among the baselines read (read 20261030, between 19:33 and 19:34 UTC; first 100,000 of 232,162 characters)
27. https://vectorize.io/articles/mem0-vs-cognee : third-party comparison by a vendor of a competing product (read 20261030, between 19:33 and 19:34 UTC)
28. https://pypi.org/pypi/cognee/json : release history, licence expression (read 20261030 19:32 UTC)
29. `gh api` commit list for the default branch since 20260801 (2,821 commits), saved and counted locally (read 20261030 19:32 UTC)
30. `gh api` for `topoteretes/cognee-community`, `cognee-integrations`, `cognee-rs`, the contributor list and open issue and pull request counts (read 20261030 19:35 to 19:37 UTC)
31. https://github.com/topoteretes/cognee/blob/main/cognee/shared/utils.py : telemetry sender (read 20261030 19:36 UTC)
32. [`repos.tsv`](../landscape/20261030_1913-github/repos.tsv) : the first landscape snapshot (20261030 19:13 UTC); its row for this repository was read at 19:28 UTC; the flag rules are in its [README](../landscape/20261030_1913-github/README.md)
33. [`kuzu.md`](kuzu.md) : this reference's entry for Kuzu, which records the archive note and the Ladybug fork "formerly known as Kuzu" (read 20261030 19:29 UTC in that entry)
34. A web search for "cognee memory independent evaluation benchmark LoCoMo LongMemEval comparison Mem0 Zep Graphiti" (run 20261030 19:33 UTC): result titles only; the pages named in [24], [25] and [27] were then fetched
