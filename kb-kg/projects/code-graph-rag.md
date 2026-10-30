---
slug: code-graph-rag
repo: vitali87/code-graph-rag
tier: deep
category: adjacent
snapshot: 20261030 18:58 UTC
---

# Code-Graph-RAG (`cgr`)

| | |
|---|---|
| Repository | https://github.com/vitali87/code-graph-rag |
| Licence | MIT (read from the `LICENSE` file [3]; the README [5] and `pyproject.toml` [14] also say MIT: no disagreement) |
| Language | Python [1] |
| Stars, forks | 5,303, 708 (20261030 18:58 UTC) [1] |
| Created, last push | 20250616 14:31 UTC, 20261030 18:31 UTC [1] |
| Latest release | v0.4.5, published 20261030 11:01 UTC [2]. `pyproject.toml` on `main` says 0.4.7 [14] (see "Which version" below) |
| Status | active (pushed within 90 days); not archived [1] |
| Paper, docs | no paper found in the sources read. Docs site: https://docs.code-graph-rag.com (linked from the README [5]); docs live in `docs/` in the repository [28] |

## What it is

Code-Graph-RAG parses a multi-language code repository with Tree-sitter, optionally sharpened by compiler-grade frontends and runtime traces, and stores a structural knowledge graph of it in an embedded graph database [5]. A user or an agent then queries, edits and optimises the code in plain English through a CLI (`cgr`) and through an MCP server that Claude Code and other MCP clients can use [5][6]. One graph holds many projects under a single language-agnostic schema, so a monorepo of mixed languages is one graph [5][9]. Indexing uses no LLM: the structure comes from parsers, symbol registries and, where installed, compiler frontends [5][6]. The project is MIT-licensed and also offers paid cloud-hosted and on-premise deployments, support and consulting [5].

The July 2026 investigation (20260726 08:52 UTC) [31] described a smaller tool: 15 MCP tools, a Docker-hosted Memgraph as a hard requirement, about 2.4k stars. Much of that has changed; each change is listed in "Changed since the July 2026 investigation" and the body below states the current position.

## How it works

### Graph construction (deterministic, no LLM)

`GraphUpdater.run()` in `codebase_rag/graph_updater.py` is a multi-pass pipeline [21]:

1. **Structure pass.** `identify_structure()` builds the Project / Folder / File / Package / Module hierarchy.
2. **Definitions pass (Pass 2).** Tree-sitter queries extract Class, Function, Method and, in the current schema, Interface, Enum, Type and Union nodes [9][21]. Optional compiler-grade frontends add exact facts where a toolchain exists: libclang for C and C++, `go/types` for Go, and opt-in Roslyn (C#), `javac` (Java) and Jedi (Python) [5].
3. **Calls pass (Pass 3).** Call sites are resolved against a `FunctionRegistryTrie` of qualified names plus per-language type inference (`parsers/*/type_inference.py`, `parsers/call_resolver.py`) [21][28].
4. **Embeddings pass (optional).** `_generate_semantic_embeddings()` runs when the semantic extra is installed [21][10].

Edges record where they were produced (line, column, argument count) and how they were bound: the `resolution` property is one of `exact`, `overload`, `heuristic`, `trace_confirmed` or `dynamic` [9]. A runtime trace (`cgr trace`) can merge calls that actually happened into the graph, which exposes dispatch static analysis cannot see; the README says Tree-sitter stays the backbone because a trace only sees code that ran [5].

**Schema.** Node labels (default index) include Project, Package, Folder, File, Module, Class, Function, Method, Interface, Enum, Type, Union, ExternalPackage, ExternalModule and Section; relationships include CONTAINS_\*, DEFINES, DEFINES_METHOD, IMPORTS, INHERITS, IMPLEMENTS, OVERRIDES, RETURNS, ACCEPTS, CALLS, REFERENCES, INSTANTIATES and LINKS_TO [9]. Opt-in capture groups add: `io` (Resource nodes; READS_FROM, WRITES_TO, FLOWS_TO taint and data-flow edges; EXPOSES / RESOLVES_TO linking HTTP endpoints to callers), `findings` (ast-grep Pattern, CodeSmell, SecurityIssue), `glosses`, `parameters`, `fields`, `enum_variants` and `constants` [9]. Markdown documents are indexed too: headings become `Section` nodes, and relative links between documents become `LINKS_TO` edges (with the link text, anchor and position), with unresolved targets listed in `broken_links` on the document's Module node [9].

**Languages.** Python, TypeScript, TSX, JavaScript, Rust, Go, Java, C, C++, C#, PHP, Lua, Dart and Julia are listed as fully supported; Scala is in development; Ruby, Kotlin, Swift, Elixir, Haskell, Solidity, Bash and Nix have structural support through an ast-grep tier [5].

**Incremental updates.** The mechanism the July investigation described is still in the code [21]:

- A per-file MD5 hash cache (`_load_hash_cache`, `_save_hash_cache`) lets `_is_already_in_sync()` skip a run when nothing changed.
- For a changed file, `_capture_inbound_edges()` snapshots the edges that arrive from unchanged files, `_delete_module_entities()` drops the file's subgraph, the file is re-parsed, and `_restore_inbound_edges()` replays the snapshot. `_rehydrate_registry_from_graph()` reloads unchanged files' symbols from the graph so cross-file calls still resolve.
- A run takes a sync lock around the whole run (`holds_sync_lock`); a second writer is refused before anything is written [21].

Since July there is also a scoped path, `GraphUpdater.reingest(paths)`, exposed as the MCP tool `reingest` and used by `cgr watch`. It re-parses the named files plus the files that depend on them (one level, found through CALLS, REFERENCES, INSTANTIATES, IMPORTS, INHERITS, IMPLEMENTS, RETURNS and ACCEPTS edges), resolves calls in that set only, and restores every other inbound edge [6][12][25]. Repository-wide passes (code-quality findings, URL-to-endpoint links) are rebuilt only by `update_repository` [6].

### Graph storage

The graph lives in an embedded SQLite file by default (`~/.cgr/graph.sqlite`); Memgraph and Neo4j 5 are opt-in backends that take the same Cypher [5][8]. `codebase_rag/embedded_graph` is a Cypher engine over SQLite: nodes and relationships sit in two tables with JSON property maps, a node's unique key is lifted into an indexed column, a read query compiles to one SQL statement of chained CTEs, and variable-length patterns become recursive CTEs [8]. Graph procedures run under Memgraph's MAGE names (`pagerank.get`, `nxalg.simple_cycles`, `graph_util.descendants`, and others) [8]. A Rust extension, `cgr-graph-rs`, is a prebuilt wheel dependency on Linux, macOS and Windows x64 CPython; elsewhere the Python implementation runs [8][14]. The engine does not support path variables (`MATCH p = ...`) or more than one label per node [8].

### The tool surface

`codebase_rag/mcp/server.py` is an MCP server over stdio, or over streamable HTTP behind a bearer token [15]. The MCP guide lists **37 tools** [6] (15 in July [31]). The groups:

| Group | Tools | Notes [6] |
|---|---|---|
| Typed graph queries | `resolve`, `definition`, `callers`, `callees`, `implementors`, `overrides`, `importers`, `tests_reaching`, `endpoints`, `endpoint_callers`, `remote_dependencies`, `glosses` | "Deterministic: fixed graph queries, no LLM, same graph gives the same JSON." `depth` > 1 follows callers/callees/subtypes transitively. A name the graph does not hold is refused with `isError: true` and close matches, so `[]` means the name exists and nothing matches |
| Flow and failure analysis | `flow_verdict`, `explain_traceback`, `rank_root_causes` | Source-to-sink reachability returns FOUND / NO_FLOW / UNKNOWN (UNKNOWN when part of the project is outside flow-analysis coverage); needs indexing with the `io` capture group. Whether these call an LLM: unstated |
| Context | `context` | A graph-ranked, token-budgeted slice around a symbol, location or free text [11] (see below) |
| Open-ended questions | `query_code_graph`, `ask_agent` | `query_code_graph` turns English into Cypher with an LLM; `ask_agent` delegates to the internal pydantic-ai orchestrator |
| Retrieval | `get_code_snippet`, `get_function_source`, `semantic_search`, `structural_search`, `find_duplicate_code` | `get_code_snippet(qualified_name)` returns source, file path, line span and docstring. `structural_search` uses ast-grep syntax. `find_duplicate_code` compares AST fingerprints stored in the graph |
| Index and lifecycle | `index_repository`, `update_repository`, `reingest`, `list_projects`, `delete_project`, `wipe_database` | `index_repository` clears the project's data first; `wipe_database` removes every project |
| Files and edits | `read_file`, `list_directory`, `write_file`, `surgical_replace_code`, `structural_replace`, `rename`, `change_signature`, `annotate` | After a write on an indexed project, the touched files are re-ingested and a structural delta (symbols added/removed/renamed, dangling callers, signature changes, new import cycles, tests reaching the edit) is appended to the result. `rename` and `change_signature` refuse heuristically resolved sites unless `allow_heuristic` is set, and support `dry_run` |

**Read-only mode.** `cgr mcp-server --read-only` (or `MCP_READ_ONLY=true`) removes `write_file`, the edit tools, indexing, `annotate`, `delete_project` and `wipe_database` from the list and refuses them by name. Every tool carries MCP annotations (`readOnlyHint`, `destructiveHint`, `openWorldHint: false`). `read_file` refuses files that look like credentials unless an environment variable overrides it [6].

**Glosses.** `annotate` attaches a durable note to one definition, stored in the graph and not in the source file. Each note is anchored by the definition's content hash and graded after each sync as EXACT, STALE, MOVED, AMBIGUOUS or LOST; a text-quote anchor lets it follow a renamed definition [6][9].

**Natural-language-to-Cypher, and its guardrails.** The open-ended verb is still NL-to-Cypher: `CypherGenerator` (`services/llm.py`, a pydantic-ai agent) emits Cypher against a schema prompt (`prompts.py`) [17][18]. The tool descriptions now steer the caller to the typed tools first ("Use this instead of query_code_graph whenever you know the exact name or location") [6]. Defences around the generated query are layered:

1. **Prompt rules** [18]: never use unbounded variable-length paths (cap them, for example `[:CALLS*1..6]`); always add `LIMIT 50` to listing queries; never return whole nodes, return aliased properties; match short names with `ENDS WITH` on `qualified_name`; constrain by project with `STARTS WITH '<projectName>.'`. Algorithmic questions are steered to graph procedures instead of variable-length paths. A separate local-model prompt exists for Ollama [17].
2. **Text validators** [17]: `_validate_cypher_read_only`, `_validate_no_unbounded_paths`, `_validate_call_procedures`, run on the generated query.
3. **Plan check** [16]: the query is planned with `EXPLAIN` and refused unless every operator is a known read operator and every procedure is allowed; an empty plan is refused. The module docstring states that Neo4j's read access mode is routing, not access control, so the plan check is the boundary on both engines. On the embedded graph the query then runs on a connection SQLite opened read-only [8].
4. **Result caps** [19][20]: rows are cut to `QUERY_RESULT_ROW_CAP` (default 500), then results are cut to `QUERY_RESULT_MAX_TOKENS` (default 16,000 tokens), and a `summary` field tells the caller that truncation happened. `QUERY_TIMEOUT_S` defaults to 60 s. A `project` argument is applied to results before the caps [6][19][20].

The result carries `query_used`, the generated Cypher, which is the caller's only way to debug a miss [19]. Each `query_code_graph` call costs an extra LLM round trip and can fail with a translation, timeout or database error summary [19].

### How graph and text retrieval combine

Embeddings are optional (the `semantic` extra). The default encoder is UniXcoder run locally (torch and transformers; 768-dimensional vectors); alternatively any OpenAI-compatible embeddings endpoint (OpenAI, Ollama, vLLM, LM Studio) computes them, which removes the torch dependency [10][14]. The default vector store is now **sqlite-vec** in `~/.cgr/vectors.sqlite`; Qdrant (the previous default) and Milvus Lite are opt-in [10][14]. `semantic_search` embeds the query, the store returns node ids and scores, and the hits are enriched from the graph (qualified name, type) so they can be passed to `get_code_snippet` or a graph tool [22]. Project scoping uses client-side filtering with adaptive over-fetch (`_PROJECT_OVERFETCH = 4`, capped) [22].

There is still no fused ranking inside search. Graph query, semantic search and ast-grep are separate tools, and the calling agent chooses among them using tool-description wording [6]. Two newer pieces touch this:

- **`context(target, budget_tokens)`** (default budget 4,000 tokens) resolves a name, `path:line` or free text, then assembles the target's source, the call lines of its direct callers, its callees' signatures, the types it accepts and returns, the tests that reach it and linked documentation sections. Pieces are ranked by graph distance, then trace hotness, then embedding similarity, then name, taken in order while they fit the budget, and each piece records why it is included; pieces that did not fit are listed in `omitted` [11].
- **`tools/graph_rerank.py`** reranks semantic hits by their graph proximity to the other hits. Its docstring says it is deliberately not integrated: integration is conditional on a measured retrieval-quality comparison, and no labelled retrieval corpus exists in the repository [23].

## Cost and operating profile

| Item | Current position |
|---|---|
| Index time | Zero LLM calls. The MCP guide says the server starts without a model and that "indexing and the deterministic tools ... work with no LLM configured or reachable" [6]. Embeddings are optional and can be computed locally [10] |
| Query time | The typed tools, `semantic_search` (with local UniXcoder), `structural_search` and `context` need no LLM [6][11]. `query_code_graph` needs the Cypher model and `ask_agent` the orchestrator model. A role with neither provider nor model set uses a local Ollama default (`llama3.2`) [13] |
| Infrastructure | Default: none beyond Python 3.12 or newer and `ripgrep` (no database server, no Docker, no `cmake`); the graph and the vectors are files under `~/.cgr` [5][10][14]. Opt-in: Memgraph plus Qdrant through `cgr daemon up` (Docker), or a Neo4j 5 server [5][8] |
| Core dependencies | `mcp` 2.3 or newer (below 3), `pydantic-ai-slim`, `tree-sitter` 0.26.0, the `cgr-graph-rs` wheel; `pymgclient` is no longer a core dependency (the `memgraph` extra) [14]. The `semantic` extra adds `torch` 2.6 or newer, `transformers` 5 or newer, `sqlite-vec` and `qdrant-client`; per-language grammars are in `treesitter-full` and ast-grep support in `ast-grep` [14] |
| Fully local | Each part has a local option: the embedded graph, local UniXcoder or a local OpenAI-compatible embedder, and Ollama for the two LLM roles [5][10][13]. Whether the whole stack was run offline end to end, and the answer quality with a local model, are unstated |
| Index cost measured by the project | Kubernetes (2.9M lines) indexed into Memgraph in 27.6 min, bounded by Memgraph accepting about 1,000 relationships a second; the same graph loaded into SQLite in 21.9 s [8] |

## Evidence

All figures below are **published by the project itself, on its own corpora**. No third-party evaluation was found in the sources read (no dedicated search for one was run).

| What | Result | Source |
|---|---|---|
| Retrieval, graph versus grep: for each first-party symbol, find the files that call it, scored against a Python `ast` oracle, on the project's own `codebase_rag` package | graph: precision 0.8457, recall 0.9886, F1 0.9116; call-tuned grep: precision 0.3659, recall 1.0, F1 0.5358; bare-name grep: precision 0.2350, F1 0.3806 | [26] |
| Same task on `django/django` (about 2,900 files) | graph: precision 0.977, recall 0.938, F1 0.957; grep_call F1 0.789; grep_name F1 0.506 | [26] |
| Structure (L1) on `codebase_rag` | nodes and `DEFINES` / `DEFINES_METHOD` / `INHERITS` / `IMPORTS` edges all precision and recall 1.0; 6,800 of 6,800 spans exact. The target is the tool's own Python code | [26] |
| `CALLS` recall (L3) against an execution trace of the project's own code driven by a fixture | 634 of 634 traced edges present. The README calls it a lower bound; multi-language recall is "future work pending a SCIP-based oracle" | [26] |
| Incremental versus clean re-index, 25 neutral file edits | `CALLS` precision 0.9998, recall 0.9978; 10 of 25 edits reproduce a clean re-index exactly | [26] |
| Embedded SQLite graph versus Memgraph 3.3 | 154 of 154 shipped read queries return the same rows on a 38,183-node, 166,107-relationship graph; total run time 39.9 s embedded (33.0 s with the Rust extension) against 221.5 s on Memgraph; 53 semantics probe queries match | [8] |
| Scale of the embedded graph | the graph replicated 100 times (3.77M nodes, 16.6M relationships) served per-project queries at flat latency in 595 MB; Memgraph held 3.98 GiB at 50 times | [8] |
| Scoped re-ingest latency (cgr 0.0.804, Apple silicon laptop, 20260830, in-memory ingestor, no database round trips) | typical module, 2 dependents: p50 194 ms, p95 445 ms against 2,934 ms for the whole-tree path; a hub imported by 54 files: p50 3,492 ms against 6,992 ms | [25] |
| End-to-end agent effect (same model and loop, with and without the graph tools) | a harness exists (`evals/agentic_qa.py`, `evals/first_tool.py`); **no results are published** in the README read. The README attributes the idea to a GitLab Knowledge Graph work item and says that item contains no "8% over grep" figure, and that its headline was an agentic SWE-bench-Lite pass rate of roughly 6 to 7 of 23 issues. That work item was not fetched here | [26] |

Caveats the sources themselves give: the retrieval oracle counts `ast.Call` nodes with first-party callee names, so it favours name-based resolution; the retrieval residuals are name collisions and property getters [26]. The numbers measure whether the right files are found, not whether an agent solves tasks better.

## Direction

- **From retriever to agent-facing code-intelligence server.** The tool surface grew from 15 to 37 tools [6][31]: typed navigation, impact queries (`tests_reaching`, endpoint callers), data-flow verdicts, edit tools with postconditions (`rename`, `change_signature` refuse unproven sites and undo on a failed postcondition), and agent-written notes.
- **Local-first by default.** The default graph and vector backends moved to embedded SQLite files [8][10]. NEWS says the default became the SQLite vector store and "Docker: no longer starts Docker without embeddings" [24].
- **Security hardening.** Recent NEWS and release notes list repository approval before a repository's `.cgr.md` reaches the agent's system prompt, prompts before reading credential files, MCP tool annotations and a read-only mode, fuzz targets for the Rust crate, and an SBOM with each release [24].
- **Performance work.** A Rust engine for Cypher parsing and graph algorithms, and Rust hashing in the indexer [8][24].
- **Commercial layer.** The README offers managed cloud and on-premise deployments and support contracts; the repository carries a `GOVERNANCE.md` file [5][28].
- **Cadence.** 6,772 commits on `main` since 20260801 and 23 GitHub Releases in the same window (see below) [2][4]. No roadmap file exists at the repository root [28]; the project's open issues are the closest published plan: 369 open issues and 152 open pull requests at 20261030 19:02 UTC [27].

**Which version.** The README says three version lines differ by design: git tags (every merge), GitHub Releases and PyPI (every 50th version, plus security fixes, breaking changes and merges labelled `release now`) [5]. So `pyproject.toml` on `main` (0.4.7) runs ahead of the latest GitHub Release (v0.4.5) [2][14].

**Other code-graph tools for coding agents.** A web search on 20261030 19:03 UTC for alternatives surfaced several small projects; only one was checked against a primary source. *Codebase-Memory* (`DeusData/codebase-memory-mcp`) is an MIT-licensed (from its `LICENSE` file) tree-sitter code graph exposed over MCP, created 20260224, pushed 20261029, 47,853 stars at 20261030 19:03 UTC [30]; its paper (arXiv 2603.27277, 28 March 2026) reports 66 languages, 31 repositories, 83% answer quality against 92% for a file-exploration agent, and about ten times fewer tokens and 2.1 times fewer tool calls [29]. Its star growth was not assessed here. The project's own eval notes also mention GitLab's Knowledge Graph work item, not fetched here [26].

## Changed since the July 2026 investigation

Checked 20261030 18:58 to 19:05 UTC against the live repository. The July note was written 20260726 08:52 UTC [31].

- **Popularity and activity.** Stars 2,355 (GitHub API, July) to 5,303 (20261030 18:58 UTC): +2,948 in about 96 days, about 31 a day, against about 10.6 a day over the repository's life (computed). Forks 708. Stargazer timestamps could not be read (the API returned 404), so the growth shape was **not checked** for signs of inorganic growth [1]. Open issues were 12 in July; now 369 open issues and 152 open pull requests, with 965 issues closed [27]. 6,772 commits since 20260801: 5,330 by the owner's account, 636 by `github-actions[bot]`, 537 by a GitHub account named `claude`, 116 by `dependabot[bot]`, the remainder by 25 other named accounts and one commit with no login; 67 contributors in total. Many are merge and version-bump commits, so the count is not a measure of work [4].
- **Version.** July: v0.0.502. Now: latest release v0.4.5 (20261030 11:01 UTC); 36 GitHub Releases in total, 23 of them since 20260801 [2].
- **Licence.** Unchanged: MIT in the `LICENSE` file, the README and `pyproject.toml` [3][5][14].
- **No rename, no archive, no successor found.** The repository keeps its name, is not archived, and is the same repository created 20250616 [1].
- **July claim now false: "Docker'd Memgraph required".** The default graph is an embedded SQLite file with a Cypher engine; Memgraph and Neo4j are opt-in [5][8]. Some docs lag: `docs/architecture/overview.md` still shows "Memgraph Knowledge Graph" and "13 programming languages", and several tool rows in the MCP guide still say "Memgraph" [6][7]. The body above follows the README, the embedded-graph page, `config.py` and `pyproject.toml`, which agree [5][8][14][20].
- **July claim now false: "Qdrant/Milvus for vectors".** The default vector store is sqlite-vec; Qdrant (the previous default) and Milvus Lite are opt-in [10][14].
- **July claim now false: "no `get_callers` / `get_definition`; the central graph verb is NL-to-Cypher, not typed navigation".** The MCP guide lists `resolve`, `definition`, `callers`, `callees`, `implementors`, `overrides`, `importers` and `tests_reaching` as deterministic, LLM-free tools, and tells the caller to prefer them [6]. `query_code_graph` remains for open-ended questions.
- **July claim stale: "fifteen tools".** 37 are listed [6].
- **July claim stale: "pymgclient is a core dependency; Docker'd Memgraph, Qdrant/Milvus heavy infra".** The default install needs no server; `pymgclient` moved to the `memgraph` extra [5][14].
- **July claim extended, not false: validators.** The three text validators named in July still exist; a plan-based read-only check and a read-only SQLite connection were added [16][17][8].
- **July claim extended, not false: "no fused ranking, routing 100% the agent's decision".** Still true for search; `context` ranks by graph distance, and a graph-proximity reranker exists as an unintegrated prototype [11][23].
- **July claim extended: "write tools in the same surface".** Still true by default; a `--read-only` mode was added [6].
- **July claim extended: node labels, languages.** The schema has roughly three times as many labels and opt-in capture groups; Markdown sections and links are indexed; Julia is fully supported, Scala is in development, and Ruby, Kotlin, Swift, Elixir, Haskell, Solidity, Bash and Nix have structural support [5][9].
- **July claim unchanged: incremental updates.** The MD5 hash cache, inbound-edge capture and restore and registry rehydration are still in `graph_updater.py`; a scoped `reingest` path was added [21][25].
- **July claim unchanged: index time uses no LLM; `ask_agent` still exists; Python 3.12 or newer** [6][14].
- **README and architecture changed materially.** The README headline moved from "RAG for your monorepo" to "embedded graph that needs no server", with runtime tracing, dead-code detection, data-flow edges and an enterprise services section [5]. These affect the July analysis wherever it assumed heavy infrastructure or a query-language-only graph surface.

## Sources

1. https://github.com/vitali87/code-graph-rag: repository metadata from the GitHub API (stars, forks, subscribers, licence field, archived flag, created and pushed dates, language, default branch, topics) (read 20261030 18:58 UTC)
2. https://github.com/vitali87/code-graph-rag/releases: latest release v0.4.5 and the list of 36 releases, 23 dated since 20260801, from the GitHub API (read 20261030 18:58 UTC)
3. https://github.com/vitali87/code-graph-rag/blob/main/LICENSE: MIT licence text (read 20261030 18:58 UTC)
4. https://github.com/vitali87/code-graph-rag/commits/main: 6,772 commits dated since 20260801 and their authors, from the GitHub API; contributor count from the API's contributors list (read 20261030 18:58 UTC)
5. https://github.com/vitali87/code-graph-rag/blob/main/README.md: description, languages, embedded graph default, version lines, enterprise services, runtime tracing (read 20261030 18:58 UTC)
6. https://github.com/vitali87/code-graph-rag/blob/main/docs/guide/mcp-server.md: the 37 MCP tools, read-only mode, LLM roles, deterministic tools (read 20261030 18:59 UTC)
7. https://github.com/vitali87/code-graph-rag/blob/main/docs/architecture/overview.md: architecture overview, which still names Memgraph and 13 languages (read 20261030 18:59 UTC)
8. https://github.com/vitali87/code-graph-rag/blob/main/docs/architecture/embedded-graph.md: backends, the SQLite Cypher engine, parity and scale measurements, Rust extension (read 20261030 18:59 UTC)
9. https://github.com/vitali87/code-graph-rag/blob/main/docs/architecture/graph-schema.md: node and relationship types, edge properties, document links, capture groups (read 20261030 18:59 UTC)
10. https://github.com/vitali87/code-graph-rag/blob/main/docs/sdk/semantic-search.md: vector stores, embedding providers (read 20261030 19:00 UTC)
11. https://github.com/vitali87/code-graph-rag/blob/main/docs/architecture/context-slice.md: the `context` tool (read 20261030 19:03 UTC)
12. https://github.com/vitali87/code-graph-rag/blob/main/docs/guide/realtime-updates.md: `cgr watch` and scoped re-ingest (read 20261030 18:59 UTC)
13. https://github.com/vitali87/code-graph-rag/blob/main/docs/getting-started/configuration.md: provider settings, Ollama default (read 20261030 19:01 UTC)
14. https://github.com/vitali87/code-graph-rag/blob/main/pyproject.toml: version 0.4.7 on `main`, dependencies, extras, Python 3.12 or newer, MIT (read 20261030 18:59 UTC)
15. https://github.com/vitali87/code-graph-rag/blob/main/codebase_rag/mcp/server.py: stdio and streamable-HTTP transports, bearer auth, read-only refusal (read 20261030 19:00 UTC)
16. https://github.com/vitali87/code-graph-rag/blob/main/codebase_rag/services/cypher_guard.py: EXPLAIN-plan read-only check (read 20261030 19:00 UTC)
17. https://github.com/vitali87/code-graph-rag/blob/main/codebase_rag/services/llm.py: `CypherGenerator`, the three text validators, orchestrator factory (read 20261030 19:01 UTC)
18. https://github.com/vitali87/code-graph-rag/blob/main/codebase_rag/prompts.py: Cypher generation rules (read 20261030 19:01 UTC)
19. https://github.com/vitali87/code-graph-rag/blob/main/codebase_rag/tools/codebase_query.py: row cap, token truncation, summary field, error summaries (read 20261030 19:00 UTC)
20. https://github.com/vitali87/code-graph-rag/blob/main/codebase_rag/config.py: default backends, caps and timeouts (read 20261030 19:01 UTC)
21. https://github.com/vitali87/code-graph-rag/blob/main/codebase_rag/graph_updater.py: pipeline passes, hash cache, edge capture and restore, sync lock (read 20261030 19:00 UTC)
22. https://github.com/vitali87/code-graph-rag/blob/main/codebase_rag/vector_store.py and `codebase_rag/tools/semantic_search.py`: project over-fetch and graph enrichment of hits (read 20261030 19:00 UTC)
23. https://github.com/vitali87/code-graph-rag/blob/main/codebase_rag/tools/graph_rerank.py: graph-proximity reranker, not integrated (read 20261030 19:01 UTC)
24. https://github.com/vitali87/code-graph-rag/blob/main/NEWS.md and the latest release notes: recent headline changes (read 20261030 19:01 UTC)
25. https://github.com/vitali87/code-graph-rag/blob/main/docs/reports/REINGEST_BENCHMARK.md: scoped re-ingest latency (read 20261030 19:03 UTC)
26. https://github.com/vitali87/code-graph-rag/blob/main/evals/README.md: evaluation harness and latest results (read 20261030 19:03 UTC)
27. https://github.com/vitali87/code-graph-rag/issues: open and closed issue and open pull request counts from the GitHub search API (read 20261030 19:02 UTC)
28. https://github.com/vitali87/code-graph-rag: repository file tree (2,358 files) from the GitHub API (read 20261030 19:00 UTC)
29. https://arxiv.org/abs/2603.27277: Codebase-Memory paper abstract (read 20261030 19:03 UTC)
30. https://github.com/DeusData/codebase-memory-mcp: repository metadata and `LICENSE` file from the GitHub API (read 20261030 19:03 UTC)
31. The earlier investigation of this project (dated 20260726 08:52 UTC), now superseded by this entry. Cited only for what it claimed in July.
