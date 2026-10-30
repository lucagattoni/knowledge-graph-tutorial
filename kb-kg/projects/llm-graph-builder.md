---
slug: llm-graph-builder
repo: neo4j-labs/llm-graph-builder
tier: deep
category: core
snapshot: 20261030 19:29 UTC
---

# Neo4j LLM Knowledge Graph Builder

Reading times: repository metadata, releases, `LICENSE` and README at 20261030 19:29 UTC; source files
between 19:30 and 19:34 UTC; Neo4j web pages and searches between 19:31 and 19:34 UTC. Each source carries
its own time. Sources marked "summarised" were read through a fetch tool that summarises the page, so quotes
from them are the tool's rendering, not a copy.

| | |
|---|---|
| Repository | https://github.com/neo4j-labs/llm-graph-builder |
| Licence | Apache-2.0, from the `LICENSE` file: the unmodified Apache 2.0 text with the appendix placeholder "Copyright [yyyy] [name of copyright owner]" left unfilled, so the file names no copyright holder [3]. GitHub's API also says Apache-2.0 [1]. The README has no licence badge or statement, so nothing disagrees [4]. |
| Language | GitHub's primary language is Jupyter Notebook [1]. The README badges name Python, FastAPI and React [4]; the tree shows a Python backend and a React frontend, with large notebooks under `experiments/` [36]. GitHub's language method was not checked. |
| Stars, forks | 5,289 and 884 (20261030 19:29 UTC) [1]. Snapshot row: rank 15 in the ranked table, 5.17 stars per day over 1,023 days, 16.71 forks per 100 stars, no flag set [34]. |
| Created, last push | 20240111 14:31 UTC, 20261029 08:11 UTC [1]. The last push is on `dev`; the head of `main` is 20261023 12:52 UTC [27]. |
| Latest release | v0.8.7, 20260723 06:14 UTC [2] |
| Status | Not archived; pushed within 90 days, so "active" by the snapshot rule [1]. The app's own header banner says "This project is no longer actively developed" [21]. See "Direction". |
| Paper, docs | No paper found. Neo4j's docs page: https://neo4j.com/labs/genai-ecosystem/llm-graph-builder [29]. In-repo docs: `docs/backend/backend_docs.adoc`, `docs/project_docs.adoc` [23]. |

## What it is

The LLM Knowledge Graph Builder is a web application and REST API from the Neo4j Labs organisation. It splits
unstructured sources (PDF and other files, web pages, Wikipedia, YouTube transcripts, S3 and GCS buckets)
into chunks, has an LLM extract entities and relationships from each chunk, and writes chunks and graph into
a Neo4j database [4][23]. A chat panel answers questions over that database in seven modes [11][20]. It is the
vendor's reference implementation of LLM-based graph construction. Extraction itself is delegated to
LangChain's `LLMGraphTransformer`, so the extraction prompt lives in a library, not in this repository
[23][25].

The snapshot sets no flag [34]; flags are heuristics. 22 contributors, 37 open issues against 646 closed [27]
and 16.71 forks per 100 stars show sustained outside use but not how the stars arrived. The sources are silent
on that.

## How it works

### Architecture and interfaces

A FastAPI backend (`backend/score.py`) exposes 33 endpoints, among them `/extract`, `/post_processing`,
`/chat_bot`, `/schema`, `/populate_graph_schema`, `/get_duplicate_nodes`, `/merge_duplicate_nodes` and
`/metric` [18]. A React frontend drives them. Docker Compose, Cloud Run and Cloud Build deployments are
documented [4]. There is no MCP server or agent interface: no path with "mcp" or "agent" is in the file
tree, and `score.py` and `requirements.txt` have no MCP reference [18][19][36]. An agent would call the REST
API.

### From document to graph

| Step | What happens | Source |
|---|---|---|
| Load | PDFs through PyMuPDF; other files through LangChain's `UnstructuredFileLoader`; web, Wikipedia, YouTube, S3 and GCS have their own loaders. YouTube needs a transcript proxy. | [35][4][8] |
| Clean | Double and single quotes are removed and newlines become spaces before splitting; whitespace runs collapse after. | [8][7] |
| Chunk | Fixed-size token splitting. Frontend defaults: 100 tokens per chunk, 20 overlap, 1 chunk per LLM call; menus offer 50 to 1,000 tokens. PDF chunks carry a page number, YouTube chunks start and end times. | [7][20] |
| Cap | Unless the user's email is in Neo4j's own email domain, a file is cut to `MAX_TOKEN_CHUNK_SIZE / tokens-per-chunk` chunks. Default 10,000 tokens: 100 chunks at 100 tokens, 10 at 1,000. With no login the cap applies. | [7][4] |
| Lexical graph | `Document` nodes; `Chunk` nodes keyed by the SHA-1 of the chunk text; relations `PART_OF`, `FIRST_CHUNK`, `NEXT_CHUNK`; one embedding per chunk and a vector index named `vector`. | [9] |
| Extract | `LLMGraphTransformer` on each group of combined chunks; results saved with a base label `__Entity__`; a `HAS_ENTITY` relation links chunk to entity by label plus id. | [6][8][9][10] |
| Batch, resume | 20 chunks at a time (default); a cancel flag; retry modes: start over, delete entities and start over, resume from the last processed chunk. | [8][11][20] |

The README documents `MAX_TOKEN_CHUNK_SIZE` as the "maximum token size to process file content" [4]; the
truncation of long files is visible only in `create_chunks.py`, whose log line reports the cut with the wrong
"from" count [7].

**Extraction prompt.** The backend passes the chosen LLM to `LLMGraphTransformer` with its own
`ADDITIONAL_INSTRUCTIONS` plus any user text [6]. The fixed part says to keep dates, numbers and revenues as
properties, not nodes, and to ignore instructions inside the document [11]. User text is sanitised: braces
become brackets and patterns such as `eval(` are replaced by a marker [6]. The base prompt is LangChain's, read
at tag `libs/neo4j/v0.11.0` of `langchain-neo4j`, the version `requirements.txt` pins [19][25]. It asks for
"basic or elementary" node labels (a person is `person`, never `mathematician`), human-readable node ids from
the text, general and timeless relationship types ("PROFESSOR", not "BECAME_PROFESSOR"), and coreference
resolution (use the most complete name) [25].

**Typing.** The LLM assigns each node a `type` string and each relationship a type; the node type becomes the
Neo4j label and the node `id` is the name [8][10][25]. If the model supports structured output and is not
served through Groq, the backend also asks for a `description` on every node and relationship; otherwise it
turns off tool use, drops descriptions and parses the model's text [6]. Diffbot is not an LLM: it calls a
hosted extraction service for "entities" and "facts" [6]. Types are free text unless constrained.

**Schema constraint.** The user may give allowed node labels (comma-separated) and allowed relationships as
triples of source label, relationship type and target label. The backend rejects a list that is not a
multiple of three or whose source or target is not in the node list [6]. `LLMGraphTransformer` builds an
output schema limited to those types and, because `strict_mode` defaults to true and the backend leaves it
alone, deletes any returned node or relationship outside the lists, comparing lower-cased strings and, for
triples, direction [25]. Without lists nothing limits the types; Neo4j's blog recommends giving a schema
because the LLM otherwise "may generate many entity types" (summarised) [30]. The UI fills the lists from the
connected database (`/schema`), from an LLM reading pasted text (`/populate_graph_schema`) [23][16], and,
judging by file names only, from predefined schemas or a JSON upload [36].

**Deduplication.** There is no single step. Only the first two layers run on their own.

| Layer | Mechanism | Runs |
|---|---|---|
| Prompt | Coreference rule in the LangChain prompt [25] | Every call |
| Write time | Chunks merge on a text hash; the chunk-to-entity step merges on label plus id, so only an exact string under one label merges [9] | Every call |
| Candidate search | `get_duplicate_nodes` pairs same-label nodes with an embedding when one id contains the other, or the edit distance is under a threshold (ids over 5 characters), or cosine similarity is above 0.97 [14] | On request, UI |
| Merge | `merge_duplicate_nodes` merges a list posted from the UI with `apoc.refactor.mergeNodes`, relationships kept, property option "discard" (its meaning was not checked against APOC) [14][18] | On request |
| Schema consolidation | An LLM groups similar labels and relationship types into fewer categories taken from the input, then relabels the graph [11][13] | Optional task |

The candidate search needs entity embeddings, which exist only if `ENTITY_EMBEDDING` is true and the
`materialize_entity_similarities` task has run [13][14][18]. Another optional step deletes entities not
connected to any chunk [18][23].

**Post-processing tasks** (`/post_processing`) [18][20]:

| Task | Effect |
|---|---|
| `materialize_text_chunk_similarities` | `SIMILAR` relations between chunks scoring at least 0.8 on the vector index (six nearest, only for chunks with fewer than five such links) [14] |
| `enable_hybrid_search_and_fulltext_search_in_bloom` | Rebuilds full-text indexes (`keyword`, `entities`, `community_keyword`) and vector indexes (`vector`, `entity_vector`, `community_vector`) [13] |
| `materialize_entity_similarities` | Embeds each entity from id plus description; only if `ENTITY_EMBEDDING` is true [13][18] |
| `enable_communities` | Needs Graph Data Science (GDS). Leiden clustering on the entity graph, up to 3 levels; an LLM writes a title and summary per community and per parent; summaries embedded and indexed [15] |
| `graph_schema_consolidation` | The LLM relabelling above [13] |

### The query side

With more than one message in the history, the LLM first rewrites the conversation into a search query.
Retrieved text is split to 3,000 tokens and filtered by embedding similarity (0.10); the retriever score
threshold is 0.5 [11][12]. The answer prompt says to use only the context, to admit unknowns, and to treat the
context as untrusted [11]. History is kept as `Session` and `User` nodes in the user's database and summarised
by the LLM in a background thread after each answer [12]. The reply carries sources, chunk, entity and
community details and, in graph mode, the generated Cypher [12].

| UI label (backend id) | What it does | Needs |
|---|---|---|
| vector (`vector`) | Vector search on chunk embeddings, top 5, grouped per document; can be limited to selected documents | Chunk vector index |
| fulltext (`fulltext`) | The same query as a hybrid of the vector index and a keyword index on chunk text; no document filter | `keyword` index |
| graph+vector (`graph_vector`) | Vector hit on chunks, then entities linked by `HAS_ENTITY` (top 40 by chunk count), then paths from them: one hop, two when the entity embedding is over 0.9 similar to the question, the entity alone when under 0.3. Chunk text, entities and relationships go to the LLM | Extraction; entity embeddings optional (without them the one-hop branch runs) |
| graph+vector+fulltext (`graph_vector_fulltext`) | The previous mode with the hybrid keyword index; the code's default mode | `keyword` index |
| entity search+vector (`entity_vector`) | Vector search on `__Entity__` nodes (top 10), then the 3 chunks mentioning most matched entities, up to 3 communities, relationships among matches and up to 10 outside neighbours | Entity embeddings; communities for that part |
| global search+vector+fulltext (`global_vector`) | Hybrid search over community summaries (top 10); the summaries are the context | Communities (GDS) |
| graph (`graph`) | Text-to-Cypher: LangChain's `GraphCypherQAChain` writes Cypher from the live schema, runs it, answers from 3 result rows; `validate_cypher` on, `allow_dangerous_requests` true. Does not use the retriever above | The graph |

Sources: [11][12][20]. Modes without a document filter refuse to run while files are selected [12]. I found no
reranker, no agent-driven or iterative retrieval and no query decomposition in the files read; that is
absence from what was read, not proof of absence. Whether write queries can pass the text-to-Cypher chain is
unstated in those files.

### Providers and Neo4j editions

LLMs are chosen by a configuration key `LLM_MODEL_CONFIG_<NAME>` holding the model id and credentials; a
substring of the name picks the provider [6].

| Provider | Notes | Source |
|---|---|---|
| OpenAI, Azure OpenAI, Anthropic, Fireworks, Groq, Amazon Bedrock, Ollama | Direct LangChain chat classes | [6] |
| Gemini | Through Vertex AI with Google default credentials; all safety filters "BLOCK_NONE" | [6] |
| Diffbot | Hosted extraction service, not an LLM | [6] |
| Any other name | Treated as an OpenAI-compatible endpoint with a base URL | [6] |

The README lists OpenAI, Gemini and Diffbot without a qualifier and tags the rest "dev deployed version",
a phrase it does not define [4]. The backend docs list only GPT-3.5, GPT-4, Gemini 1.0 Pro and Diffbot, which
is out of date [23]. Neo4j's docs page lists OpenAI, Gemini, Llama3, Diffbot, Claude and Qwen (summarised)
[29]. Model ids in the example files (`gpt-6-luna`, `gemini-3.8-flash`, `claude-sonnet-5-5` and others) are
quoted as written and were not checked against the providers [19][20]. Embeddings: OpenAI, Gemini, Amazon
Titan or sentence-transformers; the default is `all-MiniLM-L6-v2`, 384 dimensions [10][19].

| Neo4j target | What the sources say | Source |
|---|---|---|
| Version | 5.23 or later with APOC, because the backend uses the `CALL (variable) { ... }` subquery syntax | [4] |
| Aura | Supported, free tier included; the UI marks Aura DB and Aura DS with different icons | [4] |
| Desktop | Supported with backend and frontend run separately; Docker Compose not supported | [4] |
| Community or Enterprise | README silent. The code reads the edition and, for Community, assumes write access | [14] |
| Graph Data Science | Needed for communities only; the connect call tests `gds.version()` and the frontend offers Communities only when GDS is active | [14][20][15] |
| Calendar-versioned releases (2025.x on) | Unstated | |

Neo4j's docs page gives no versions or editions (summarised) [29].

## Cost and operating profile

- **Index time.** The transformer starts one asynchronous task per combined chunk group [8][25]; each is
  one extraction request. With defaults (100-token chunks, 1 per call, cap of 100 chunks) a long file costs
  at most about 100 requests and about 10,000 source tokens. Raising `MAX_TOKEN_CHUNK_SIZE` lifts the cap; a
  larger chunk size cuts the requests for the same tokens. Chunks are embedded one at a time [9]. Optional
  extras: one request per community and per parent community, one for schema consolidation, one embedding per
  entity [13][15].
- **Query time.** One answering request, one rewrite request when history exists, one background
  summarisation request per answer. Graph mode makes a Cypher request and an answering request on the same
  model [12]. The chat-time token-tracking calls are commented out in the code read [12].
- **Needs.** Neo4j 5.23 or later with APOC; an LLM key or local Ollama; an embedding model (the default runs
  locally); GDS for communities; a proxy for YouTube [4][19]. The README documents an Ollama route [4]; I did
  not run it.
- **Controls.** Optional Auth0 login and per-user token limits (example values 250,000 daily and 1,000,000
  monthly) [4][19]. A public-address check helper exists in `common_fn.py`; a commit of 20260810 removed a
  fetch helper from web extraction, so whether the check still guards web loading was not checked [10][27].
  Text-to-Cypher runs with the connection's own credentials [12].

## Labs status, support and licence

The README opens: "This is an experimental Neo4j Labs project and not part of Neo4j's supported product
lineup" [4]. `LABS_DISCLAIMER.txt` says the project is "not an official Neo4j product or supported component
of the Neo4j portfolio"; its "functionality may change, be discontinued, or may never become part of a Neo4j
product"; it is provided "as is" without service-level commitments, maintenance guarantees or security
assurances; and it "is not intended or approved for use in production or pre-production environments" [5].
Both were added on 20261022 (pull request 1640, "matching neo4j-cli") [22].

Neo4j's Labs page says the same (summarised): Neo4j "does NOT offer support for Labs projects"; projects "may
be rough around the edges, with changing APIs"; Neo4j cannot "guarantee longevity"; projects are developed and
maintained without SLAs; each either graduates to a formally maintained product or is deprecated with its
source released. The page also says some customers run Labs projects in production, and that Professional
Services may help without an SLA [28]. The builder's docs page sends questions to the community forum and bugs
to GitHub Issues [29].

For this project: no support commitment, no stability promise, production use not approved [5][28]. The
licence is Apache-2.0, and ownership and permitted use "remain subject to the license" [3][5]. Dependency
licences were not checked.

## Evidence

### Published by the project and Neo4j

All of it is self-reported and small.

**Retriever comparison with RAGAS.** The notebook `experiments/modes_comparison_RAGAS.ipynb` aims to "evaluate
different retrievers used in llm-graph-builder application using RAGAS". Setup: one PDF ("About Amazon"), a
RAGAS synthetic test set with GPT-4 as generator and critic, answers from `openai-gpt-3.5`, `ragas` 0.1.14.
Answers beginning "I don't have" were dropped before scoring, so row counts differ. The text-to-Cypher mode is
not among the six modes compared [24]. The saved CSV has 86 rows over 15 questions [24]. I computed the means
below from the CSV; the project does not publish this table.

| Mode | Rows | Context precision | Context recall | Faithfulness | Answer relevancy | Answer correctness |
|---|---|---|---|---|---|---|
| vector | 15 | 0.867 | 0.964 | 0.782 | 0.951 | 0.707 |
| fulltext | 15 | 0.933 | 0.981 | 0.798 | 0.953 | 0.785 |
| entity search+vector | 14 | 0.714 | 0.433 | 0.423 | 0.962 | 0.706 |
| graph+vector | 15 | 0.933 | 0.981 | 0.825 | 0.879 | 0.732 |
| graph+vector+fulltext | 15 | 0.933 | 0.981 | 0.882 | 0.948 | 0.729 |
| global search+vector+fulltext | 12 | 0.667 | 0.422 | 0.433 | 0.951 | 0.648 |

The notebook's comments say the entity and global modes do poorly on context recall and faithfulness and
that "all modes struggle on simple questions" [24]. With 12 to 15 questions per mode, one document, one
answer model and no repeated runs, the four better modes cannot be told apart by this design; no variance test
is reported. Whether the CSV is the notebook's final output was not checked.

**In-app metrics.** `/metric` and `/additional_metrics` compute RAGAS faithfulness, answer relevancy and
context entity recall, plus ROUGE and semantic similarity; unsupported for Diffbot and Ollama models. In
`get_ragas_metrics` the "reference" field is filled with the answer itself, so those scores do not compare
against a gold answer [17][18].

**Extraction counts.** `experiments/LLM_Results_.csv`, one PDF page: GPT-3.5-turbo-16k 28 nodes and 30
relationships, Diffbot 0 and 0, GPT-4 27 and 21, a human list 22 and 25. `data/llm_comparision.json`, one
football-news PDF: REBEL-large 23 and 16, GPT-3.5-turbo-16k 22 and 27, Diffbot 1 and 0, human 22 and 24 [24].
These count objects and do not score correctness. The files carry no date and use early-period models.

**Other.** Neo4j's blog on the first release of 2025 (byline 20250205; page metadata says 20260604) says
retriever evaluation uses RAGAs, reports no scores and promises "a more detailed blog post on evaluation later
in the series" (summarised) [30]. I did not find that post in the searches run [33]. `experiments/` also holds
notebooks on chunk size, multiple models, Nova models, a Gemini transformer run, GraphRAG and graph-model
cleanup, and two Word reports; only their names were read [36].

### Independent

None found. Searches for an independent evaluation returned no paper, benchmark or comparison naming the tool
[33]. A 2026 University of La Laguna master's thesis compares Neo4j-based GraphRAG configurations; its record
does not name this project, so it is not counted (summarised) [32]. CypherBench, a text-to-Cypher benchmark,
appeared in the results and does not test this tool [33]. For Neo4j's separate Text2Cypher dataset see
[papers and benchmarks](../papers-benchmarks/README.md); whether this code uses it was not checked.

## Direction

The repository's own signals point away from this project.

- **Deprecation banner.** Pull request 1644, "Add deprecation banner for Neo4j Document Intelligence", merged
  20261016 06:03 UTC [22]. `Header.tsx` on `main` shows: "This project is no longer actively developed,
  instead use Neo4j Document Intelligence in Aura for free." [21]. The README does not contain that
  sentence [4].
- **Successor.** Neo4j's Document Intelligence announcement (byline 20260601; page metadata 20260707) says
  Neo4j Labs packaged the approach as the LLM Graph Builder and "Document Intelligence is the next step",
  "available now in preview" in Aura. At launch a job is limited to 20 documents of 10 to 20 pages in text
  formats, the extractor "deduplicates entities through a merge step", and bring-your-own entity resolution is
  on its roadmap (summarised) [31].
- **Releases.** 18 releases, v0.1 (20240516) to v0.8.7 (20260723) [2]. The gap from v0.8.3 (20250624) to v0.8.4
  (20260115) is almost seven months. None since 20260723.
- **Small maintenance continues** after the banner (below) [27].

## Recent changes

Commit subjects on `dev` since 20260730: 19 listed, two of them merges; `main` received two merges. The
snapshot's `commits_90d` of 1 matches `main` alone [34][27].

| Date (UTC) | Change (subject only) |
|---|---|
| 20260807 | Refactor of chat-history summarisation [27] |
| 20260810 | Web extraction no longer uses a custom URL-fetch helper [27] |
| 20260908 | Error handling for empty Wikipedia search results [27] |
| 20261014 | "Updated llm models and backend libraries" (#1643) [27] |
| 20261015 to 20261021 | Warning and banner changes; deprecation banner merged 20261016 [22][27] |
| 20261021 to 20261022 | Fireworks model changes; default model update; embedding-model-change debugging; Node package update; certificate upgrades [27] |
| 20261022 | Neo4j Labs disclaimer (#1640) [22][27] |
| 20261023 | Staging merged to `main` (#1649) [27] |
| 20261028 | Connectivity verification in the data-access class (#1608) [27] |
| 20261029 | Vector-index modal layout fix (#1653) [27] |

## README against code

| Item | README | Code or other file |
|---|---|---|
| Duplicate text-distance default | 5 | 3 in code and `example.env` [14][19] |
| `GRAPH_CLEANUP_MODEL` default | `openai_gpt_5_mini` | `openai_gpt_6_luna` [13][19] |
| `EFFECTIVE_SEARCH_RATIO` default | 1 | 5 in the retriever code [12] |
| Chat modes | Seven ids, and a table listing `hybrid` | Seven ids, no `hybrid` [4][11] |

## Sources

1. https://api.github.com/repos/neo4j-labs/llm-graph-builder: repository metadata (read 20261030 19:29 UTC)
2. https://api.github.com/repos/neo4j-labs/llm-graph-builder/releases: 18 releases (read 20261030 19:29 UTC)
3. https://github.com/neo4j-labs/llm-graph-builder/blob/main/LICENSE: licence text (read 20261030 19:29 UTC)
4. https://github.com/neo4j-labs/llm-graph-builder/blob/main/README.md: features, prerequisites, providers, modes, environment table, Labs note (read 20261030 19:29 UTC)
5. https://github.com/neo4j-labs/llm-graph-builder/blob/main/LABS_DISCLAIMER.txt: disclaimer (read 20261030 19:30 UTC)
6. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/src/llm.py: providers, allowed types, instruction sanitising (read 20261030 19:30 UTC)
7. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/src/create_chunks.py: chunking and cap (read 20261030 19:30 UTC)
8. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/src/main.py: processing flow, cleaning, retry (read 20261030 19:30 UTC)
9. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/src/make_relationships.py: chunk nodes, relations, embeddings (read 20261030 19:30 UTC)
10. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/src/shared/common_fn.py: graph save, embedding models, URL check (read 20261030 19:30 UTC)
11. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/src/shared/constants.py: modes, retrieval queries, prompts (read 20261030 19:30 UTC)
12. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/src/QA_integration.py: retriever chain, graph mode, history (read 20261030 19:30 UTC)
13. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/src/post_processing.py: indexes, entity embeddings, consolidation (read 20261030 19:30 UTC)
14. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/src/graphDB_dataAccess.py: similarity links, GDS and edition checks, duplicates (read 20261030 19:30 UTC)
15. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/src/communities.py: Leiden communities, summaries (read 20261030 19:30 UTC)
16. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/src/shared/schema_extraction.py: schema-from-text prompts (read 20261030 19:30 UTC)
17. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/src/ragas_eval.py: in-app RAGAS metrics (read 20261030 19:30 UTC)
18. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/score.py: endpoints, tasks, chat (read 20261030 19:31 UTC)
19. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/example.env and backend/requirements.txt: defaults, examples, pinned libraries (read 20261030 19:30 UTC)
20. https://github.com/neo4j-labs/llm-graph-builder/blob/main/frontend/src/utils/Constants.ts and frontend/example.env: chunk defaults, mode descriptions, task list (read 20261030 19:31 UTC)
21. https://github.com/neo4j-labs/llm-graph-builder/blob/main/frontend/src/components/Layout/Header.tsx: banner text (read 20261030 19:33 UTC)
22. https://api.github.com/repos/neo4j-labs/llm-graph-builder/pulls/1644 and pulls/1640: titles, merge times (read 20261030 19:33 UTC)
23. https://github.com/neo4j-labs/llm-graph-builder/blob/main/docs/backend/backend_docs.adoc and docs/project_docs.adoc: pipeline and API notes (read 20261030 19:30 UTC)
24. https://github.com/neo4j-labs/llm-graph-builder/tree/main/experiments (`modes_comparison_RAGAS.ipynb`, `RAGAS_evaluation.csv`, `LLM_Results_.csv`) and `data/llm_comparision.json`: in-repo evaluations (read 20261030 19:30 to 19:31 UTC)
25. https://github.com/langchain-ai/langchain-neo4j/blob/libs/neo4j/v0.11.0/libs/neo4j/langchain_neo4j/graph_transformers/llm.py: extraction prompt, strict mode (read 20261030 19:34 UTC)
26. https://api.github.com/repos/langchain-ai/langchain-neo4j/releases: tag v0.11.0, 20261009 (read 20261030 19:34 UTC)
27. https://api.github.com/repos/neo4j-labs/llm-graph-builder/commits (branches `dev`, `staging`, `main`), `/contributors`, issue search counts (read 20261030 19:33 UTC)
28. https://neo4j.com/labs/: what Neo4j says Labs projects are; summarised (read 20261030 19:32 UTC)
29. https://neo4j.com/labs/genai-ecosystem/llm-graph-builder: Neo4j's docs page for the tool; summarised (read 20261030 19:31 to 19:32 UTC)
30. https://neo4j.com/blog/developer/knowledge-graph-builder-first/: first release of 2025; summarised (read 20261030 19:32 UTC)
31. https://neo4j.com/blog/genai/introducing-document-intelligence-from-documents-to-a-knowledge-graph-right-inside-aura/: successor product; summarised (read 20261030 19:34 UTC)
32. https://riull.ull.es/xmlui/handle/915/47862?show=full: thesis record checked for a mention of the tool; summarised (read 20261030 19:32 UTC)
33. Web searches run between 19:32 and 19:34 UTC on 20261030: "Neo4j LLM Knowledge Graph Builder evaluation benchmark results comparison llm-graph-builder"; "llm-graph-builder neo4j-labs paper OR benchmark OR compared GraphRAG evaluation independent"; "Neo4j Document Intelligence Aura console knowledge graph from documents". Used for the absence of independent evaluations.
34. [Snapshot 20261030 19:13 UTC](../landscape/20261030_1913-github/repos.tsv): this repository's row (read 20261030 19:29 UTC)
35. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/src/document_sources/local_file.py: file loaders, loader lines only (read 20261030 19:34 UTC)
36. https://api.github.com/repos/neo4j-labs/llm-graph-builder/git/trees/HEAD?recursive=1: file tree (read 20261030 19:29 UTC)
