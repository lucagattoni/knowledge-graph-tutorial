---
slug: basic-memory
repo: basicmachines-co/basic-memory
tier: deep
category: markdown-kb
snapshot: 20261030 19:37 UTC
---

# Basic Memory

Reading times: repository metadata, branch head and counts at 20261030 19:37 UTC; README, licence, CHANGELOG
and docs between 19:29 and 19:31 UTC; source files between 19:31 and 19:34 UTC. Each source below carries its own
time. A file fetched without a printed clock carries the minute of the surrounding calls, to within one minute.

| | |
|---|---|
| Repository | https://github.com/basicmachines-co/basic-memory |
| Licence | AGPL-3.0, from the `LICENSE` file. It reads as the standard GNU Affero General Public License version 3 text; I read its start, sections 0, 2, 5, 6, 13 and the closing appendix and did not diff it against the FSF original [5]. GitHub reports AGPL-3.0 [1]; the README says "AGPL v3" and "AGPL-3.0" [4]. `pyproject.toml` and PyPI say `AGPL-3.0-or-later` [6][3]. The `LICENSE` file is the licence text and does not itself name the "or later" option; which version applies is a legal question this entry does not decide (see "Licence and hosted product"). |
| Language | Python 3.12 or later [1][6] |
| Stars, forks | 4,416 and 343 (20261030 19:37 UTC) [1]; the first snapshot read the same at 19:13 [39] |
| Created, last push | 20241202 22:40 UTC, 20261030 14:38 UTC [1]; the head of `main` was committed 20261030 14:38 UTC [1] |
| Latest release | v1.0.0, 20261029 23:45 UTC [2] |
| Status | active (pushed within 90 days); not archived [1]. Snapshot flags: none [39] |
| Paper, docs | No paper is cited in the README [4]. Docs: the repository's `docs/` folder and docs.basicmemory.com [4][28]; homepage field basicmemory.com [1] |

## What it is

Basic Memory is a local-first knowledge store: a folder of Markdown files, a parser, a database index, and three
front ends (an MCP server, a command-line tool and an HTTP API) [4][10]. A file is a "note" with optional YAML front
matter, prose, "observations" (categorised facts as list items) and "relations" (typed wiki links) [7]. The parser
turns these into entity, observation and relation rows in SQLite (default) or Postgres, beside full-text and vector
indexes [4][12]. The project says the Markdown is the source of truth and the database a derived, rebuildable
projection [4][10]. An LLM client reads and writes notes through `bm_*` MCP tools; humans edit the same files in any
editor, with Obsidian named as one [4]. The README names Basic Machines as the builder [4]; the contributor agreement
is with Basic Machines LLC [29]. The README also presents a hosted subscription version of the same engine, Basic
Memory Cloud [4]. The package description reads "Local-first knowledge management combining Zettelkasten with
knowledge graphs" [6].

Where the six questions put to this entry are answered: file format and free editing, index and sync, and MCP tools
and retrieval are the first three parts of "How it works"; cross-project linking is its fourth part; open source,
hosting and the licence are under "Licence and hosted product"; releases are under "Release history".

## How it works

### 1. File format and conventions

The note-format reference [7] defines the grammar; the README calls it "the whole grammar" [4].

**Front matter** is optional YAML. Standard keys: `title` (default: file name stem), `type` (default `note`),
`tags`, `permalink` (generated from the title, "stable even if the file moves"), `created` and `modified` (ISO 8601;
default to file times) and `schema`. Any other key is kept as metadata, indexed and usable as a search filter [7].
YAML aliases and merge keys are unsupported [10].

**Observations** are list items: a category in square brackets, text, optional `#tags`, optional parenthesised
context. Checkboxes, ordinary Markdown links and bare wiki links are not observations [7].

**Relations** are list items with a single-token or quoted relation type before a `[[wiki link]]`. A bare list wiki
link, or a wiki link in prose, becomes an implicit `links_to`. Relation types are conventions, not a fixed set. A
relation may point at a note that does not exist yet and resolves when the target appears [7]. Since v0.24.0 ordinary
Markdown links to files in the same project also become `links_to` [8][11]. The `## Observations` and `##
Relations` headings are conventional; the parser finds the syntax anywhere [7]. A wiki link in inline code makes no
relation [11].

**Time and structure.** Since v0.24.0 an observation can carry an authored qualifier such as `@effective:2026-06-10`,
indexed as valid time and filterable in search [11][17]. A Picoschema block (in front matter or a `type: schema` note)
declares expected observation categories and relation types; `warn` is the default mode, `strict` blocks sync.
`bm_schema` validates, infers a schema from existing notes (present in all notes: required; in 25% or more:
optional) and reports drift [7].

**Can a human edit freely?** Yes, and that is the stated design [4]. The documented conditions:

| Condition | What happens | Source |
|---|---|---|
| A file arrives without a `permalink` | Indexing writes one into the file, plus `title` and `type` while `ensure_frontmatter_on_sync` (default true) is on; the changelog says "Frontmatter is still written" | [11][21] |
| `locked: true` in front matter | MCP, CLI and API writes, edits and deletes are refused (HTTP 423); a direct file edit or delete overrides the lock | [9] |
| `bm_parse_semantics: false` | The note is "graph-silent": no observations or relations are indexed | [8] |
| An invalid `created` or `modified` value | An indexing error for that field, with no silent fallback | [7] |
| A note is moved or renamed | Its permalink is kept unless `update_permalinks_on_move` (default false) | [21] |

### 2. The index, and how it stays in step with the files

**What is stored.** The tables include `entity`, observation and relation tables and `note_content`, which holds
accepted Markdown with its version, checksums and file-write status [10][41]. The search index is raw SQL: an FTS5
virtual table on SQLite, generated `tsvector` columns with GIN indexes on Postgres [27]. Observations and relations
have their own search rows [13]. Vectors live in `search_vector_chunks` (chunk text, keys, SHA-256 source hashes) and
`search_vector_embeddings` (sqlite-vec on SQLite; pgvector with HNSW on Postgres); Milvus is an optional vector store
for Postgres deployments [12]. The changelog places the SQLite file at `~/.basic-memory/memory.db` (stated for
v0.13.0) [11]; the tree holds 42 Alembic migrations [28].

**Embeddings and ranking.** The default is FastEmbed, a local ONNX model, `BAAI/bge-small-en-v1.5`, 384 dimensions,
no key and no network after the first model download [12]. OpenAI, an OpenAI-compatible endpoint, or LiteLLM (an
optional extra since v1.0.0) can replace it [12][11]. Chunking splits at Markdown headers, makes each bullet a chunk,
merges prose up to about 900 characters and overlaps long sections by about 120 [12]. Hybrid search fuses full-text
and vector scores as `max(vec, fts)` plus 0.3 times the smaller; v0.19.0 replaced reciprocal-rank fusion with this
[12][11]. Defaults: 100 vector candidates, similarity floor 0.55 [21]. A cross-encoder reranker is off by default; its
default local model is `jinaai/jina-reranker-v1-tiny-en` [4].

**Derived and rebuildable?** The domain model says full-text rows, embeddings, chunks, observation rows and relation
rows are projections that "must be rebuildable or reconcilable from canonical Markdown state", and that rebuilding
an index "must not mutate canonical content" [10]. `bm reset` deletes the database file and its WAL files, states
that "Your markdown note files will not be affected", and with `--reindex` rebuilds from the filesystem [22]. Three
caveats. (a) Between a write being accepted and its file being written, the database holds the accepted
Markdown [10]. (b) Each entity gets a database-generated UUID `external_id` [41]; I found no statement that it is
written into front matter, so identifiers held by external callers may not survive a reset (not tested). (c) Vector
search needs the sqlite-vec extension to load; otherwise search falls back to keyword only [12].

**Sync.** While the MCP server runs it starts a `watchfiles` watcher ([20][23]), debounced by default at 1,000 ms
and on by default [21]. At start-up each project is indexed in the background [24]. Change detection compares file
checksums with indexed ones and recognises moves by checksum [42]. The project calls derived state "eventually
consistent by design": it converges through the next write, the next index pass, `reindex`, or a scheduled orphan
sweeper in the cloud, and canonical writes are guarded by compare-and-swap checks [15]. `bm doctor` reads a project
and reports a missing path, unfinished indexing, duplicate, orphaned or missing search rows and failed saves, each
with the fixing command [13]. The domain model describes two write flows: file-first, where "direct human edits, CLI
writes, and local MCP/API writes converge on the file", and an accepted-first flow for hosted deployments [10]. The
changelog says local writes and deletes now mark their journal rows once file work settles, "as cloud does" [11].
Which path a local `bm_write` takes was not traced here.

### 3. MCP tools and what retrieval returns

The registry holds twelve tools and an opt-in thirteenth [16][14]. The README says each carries MCP behaviour hints
(read-only, destructive, idempotent, open-world) [4]; `bm_search` does [17].

| Tool | Does | Mutates |
|---|---|---|
| `bm_read` | Exact read of a note or file with line, section and token-budget bounds; JSON includes front matter and a checksum | no |
| `bm_write` | Create a note; overwrite only when asked, guarded by `expected_checksum` | yes |
| `bm_edit`, `bm_move`, `bm_delete` | Incremental edits and front-matter changes (a missing note is refused); move or delete a note or directory | yes |
| `bm_search` | Ranked search; modes `hybrid` (default), `text`, `semantic`, `title`, `permalink`; filters on front matter, note type, category, date, valid time; `lines` returns grep-style matching lines | no |
| `bm_context` | Walks the graph from a note or `memory://` pattern; depth 1 to 5 (default 1), 7-day window, JSON by default | no |
| `bm_list`, `bm_find` | One directory level; recursive file discovery with filters | no |
| `bm_project`, `bm_schema`, `bm_man` | Project `list`, `create`, `recent`; schema `validate`, `infer`, `diff`; installed manual pages | only project `create` |
| `bm_project_delete` | Delete a project; hidden unless `enable_project_delete` is set (default false) | yes |

**What comes back.** A search hit carries title, item type (note, observation or relation), score, permalink, file
path, a content preview of up to 4,000 characters with its length and a truncation flag, and for vector matches the
`matched_chunk`. It also carries category or relation fields, valid-time metadata and project ids; the response adds
`total`, `has_more` and paging [12][19]. `compact=true` drops bodies and keeps identifiers and scores [17].
`bm_context` returns primary results with their observations and related entities and relations, each with permalink
and file path; an unresolved target shows its written text [18]. Failures are MCP errors with typed codes such as
`NOT_FOUND`, `ALREADY_EXISTS`, `REVISION_CONFLICT`, `LOCKED` and `OUTSIDE_PROJECT` [14]. The server also ships MCP
prompts and resources [28]. Transport is stdio by default; the HTTP transports have no authentication and bind to
`127.0.0.1` by default since v0.24.0 [11].

**Agent packages.** The repository ships a Claude Code plugin (session-start briefings, pre-compaction checkpoints),
framework-neutral `SKILL.md` files, and Codex, Hermes and OpenClaw integrations [4]. The ChatGPT `search` and `fetch`
adapters "are registered by Cloud only" [4].

### 4. Linking across projects or vaults

A project is "the core knowledge and isolation boundary": every entity, observation, relation and search record
belongs to exactly one project, and a local project maps to a configured directory [10]. One install can hold many
projects, each its own folder; an Obsidian vault can be one [4][10]. What crosses a boundary:

- **Search.** Since v1.0.0 a search names `project`, `projects` or `all_projects=true`, and hits carry their
  project [11][19]. **Context.** v0.22.0 notes that `build_context` allows cross-project traversal [11].
- **Links.** The resolver treats `project::note` as an explicit cross-project reference and resolves it inside that
  project; a `project/path` form is tried when local resolution fails [25]. The bulk resolver used at index time parses
  the same `::` form [26]. The domain model says "a qualified reference may select another target project" and also
  that a relation's source and resolved target "belong to the same project graph" [10]. The note-format reference does
  not document a cross-project link syntax [7]. I read the resolver but did not run a cross-project link, so
  end-to-end behaviour is unverified.
- **Moves.** `move` has a cross-project guard; moving a note across projects is unsupported (v0.14.0; extended to
  directory moves in v0.24.0) [11].
- **Hosted.** Cloud adds workspaces (Personal, Team); a project can be named `workspace/project` [14][40]. Per-project
  routing sends chosen projects to Cloud while others stay local [4].

## Cost and operating profile

| Aspect | What the sources say |
|---|---|
| LLM calls at index time | The documents read describe none; structure comes from authored syntax, embeddings from local FastEmbed unless an API provider is set [7][12] |
| LLM calls per query | None in the engine; the client's LLM chooses tools. An optional reranker is a local cross-encoder or a LiteLLM API model [4] |
| Needs | Python 3.12 or later; `uv tool install basic-memory --prerelease=allow` [4]. Intel Macs need an `onnxruntime` pin or an OpenAI provider [12]. No API key for defaults [12] |
| Fully local? | The README claims "air-gapped friendly" [4]; the embedding model downloads on first use [12], so one network fetch is needed unless it is cached |
| Background behaviour | CLI installs check for updates every 24 hours and apply them silently (`uv tool`, Homebrew; not `uvx`) [4]. The README says telemetry covers only cloud-promo and login events [4] |
| Latency | Project harness: mean search latency 754 ms (LongMemEval-60) and 140 ms (ConvoMem-274), local provider [32] |

The README says `--prerelease=allow` is needed because of a FastMCP 4 pre-release [4], but `pyproject.toml` pins
`fastmcp==4.1.3` and `mcp>=2,<3` [6], and on PyPI both resolve to final releases (read 20261030 19:37 UTC) [3]. The
README may be stale; I did not test an install without the flag.

## Licence and hosted product

**Open source.** This repository holds the engine (parser, indexer, search, MCP server, API, CLI), the cloud client
commands (login, push, pull, share, snapshots) and the agent packages, under AGPL-3.0 [4][28]. The README's comparison
table lists "Source code: AGPL-3.0" for both Cloud and Local [4]; that is the project's claim. Whether the hosted
service's own code (web app, billing, authentication, Teams) is public is **unstated**: a code search of this
repository for "stripe" found nothing, "workos" appears only in the README and the CLI's login code, and the
organisation's public repository list shows none named for the web app, though private repositories would not
appear in it [36].

**Hosted.** Basic Memory Cloud: "we host the database, run the sync, and put it on your phone", on WorkOS AuthKit,
Neon Postgres and Tigris S3, with snapshots, a web app and a Teams workspace with real-time shared editing. Price:
$15.00 a month "locked in" for beta subscribers (regular $19), 7-day trial, a code for open-source users [4]. Managed
agents (notes with `type: agent`) run in Cloud [11].

**Contributor agreement.** Contributors accept a CLA that assigns copyright to Basic Machines LLC, which "may license
the Contributions under any license terms, including copyleft, permissive, commercial, or proprietary licenses"
(section 3) [29]; CONTRIBUTING says it lets the company "relicense accepted contributions" [30].

**The licence file, as written** (not legal advice; section numbers are the licence's own) [5]:

| Topic | Text of the licence |
|---|---|
| Running | "unlimited permission to run the unmodified Program"; you may "make, run and propagate covered works that you do not convey, without conditions so long as your license otherwise remains in force" (section 2) |
| Network use is not conveying | "Mere interaction with a user through a computer network, with no transfer of a copy, is not conveying" (section 0) |
| Conveying a modified work | License "the entire work, as a whole, under this License" (5c); modification notices (5a); Corresponding Source with object code (section 6) |
| Network clause | "if you modify the Program, your modified version must prominently offer all users interacting with it remotely through a computer network ... an opportunity to receive the Corresponding Source of your version" (section 13) |
| Aggregates | Separate and independent works, not combined with the Program "such as to form a larger program", in an "aggregate" are not made subject to the licence by that inclusion (section 5) |
| "Work based on the Program" | Copying or adapting "all or part of the work in a fashion requiring copyright permission" (section 0) |

For someone embedding it, the text turns on "modify", "convey" and "work based on". I saw no exception or additional
permission in the parts of `LICENSE` I read, and the repository states no position on whether calling Basic Memory
over MCP or the CLI differs from importing it as a library. That question is **unstated** here and is for a lawyer.
The four source files I sampled (`__init__.py`, `config.py`, `db.py`, `link_resolver.py`) carry no licence header [25][41]. Model licences are separate: the project's own benchmark
excludes one embedding model because its licence "requires separate Cloud clearance" [33].

## Evidence

All numbers below are the project's own. I found no independent evaluation: this repository's
[papers and benchmarks page](../papers-benchmarks/README.md) has no entry, and a web search at 20261030 19:35 UTC
returned nothing about Basic Memory [37].

| Source | What it measured | Result |
|---|---|---|
| `matrix-v2-summary.md` in the benchmarks folder, last changed 20260625 [32] | Local Basic Memory against mem0 (raw-add), a grep baseline and full context, on LongMemEval (60 questions), ConvoMem (274) and a LoCoMo subset (300). Answerer `claude-haiku-4-5`, judge `claude-sonnet-4-6` | LongMemEval recall@5: 0.951 (Basic Memory), 0.979 (mem0), 0.846 (grep); MRR 0.900, 0.876, 0.832. ConvoMem recall@5: 0.982, 0.996, 0.954. QA accuracy, LongMemEval: 0.583, 0.450, 0.333, full context 0.217; ConvoMem: 0.755, 0.464, 0.380, full context 0.799 |
| `docs/multilingual-embedding-benchmark.md`, run 20260830 [33] | Default English model against multilingual MiniLM, 17 notes and 23 judged queries | SQLite vector: recall@5 0.8947 for both; MRR@10 0.7684 and 0.8684. The file calls the corpus small and directional |

The matrix file's own caveats: "internal-only"; mem0 ran with `infer=false`; QA depends on a small answerer;
judge agreement with humans "not yet measured"; the LoCoMo answer key is documented as imperfect; samples are modest.
It reads retrieval as near-parity with mem0 and attributes the QA gap to how answerable the returned context is,
not to recall; on ConvoMem full context scored higher than Basic Memory [32]. The 1.0 docs say historical results
"should not be relabeled as 1.0 results" [14]; this file predates 1.0.

**Star and fork signals.** The snapshot shows 6.34 stars a day over 696 days and 7.77 forks per 100 stars, no flag
[39]; both are heuristics. Live: 54 contributors in GitHub's list (the snapshot recorded 57), the top one with 1,619
contributions, then 142 and 39; 80 open and 736 closed issues; 3 open pull requests [35]. Nothing here says whether
the stars are organic.

## Direction

The repository has no roadmap file [28]; direction is read from the 1.0 migration guide, the changelog and the domain
model.

- **Narrower agent surface.** v1.0.0 removes the older tools with no aliases, requires `project` on scoped calls, and
  makes the CLI call the same tools [11][14].
- **Explicit cloud transfers.** `sync` and `bisync` give way to `push` and `pull`, which never delete on the
  destination and stop on conflicts [11][14].
- **Change journal.** The domain model calls the accepted-change journal the "canonical temporal record" and says
  journaling file-first reconciliation "is the intended direction" [10].
- **Integrations, structure, documents.** Plugins and `bm hook` capture for agent harnesses; schemas; deterministic
  `index.md` and `log.md` pages (`bm wiki`); a static "OKF v0.2" export (`bm okf export`); optional PDF ingestion [4][11][38].

## Release history since 20241202

The repository was created 20241202; the first PyPI upload was 20250204 (0.0.0) and the first GitHub release, v0.1.0,
20250207 [3][2]. GitHub lists 93 releases, including a rolling `skills-latest` tag, v0.13.0b1 to b6 and v0.13.8-dev1
[2]. PyPI lists 122 versions, 101 plain `x.y.z` [3]. Stable PyPI releases per quarter: 2025 Q1 39, Q2 13, Q3 4, Q4 10;
2026 Q1 20, Q2 9, Q3 3, Q4 so far 3. The longest gaps were 71 days (0.22.1 to 0.23.0) and 58 days (0.23.2 to 0.24.0)
[3]. Dates are GitHub release dates [2]; changelog headings differ by up to two days [11].

| Release | Date | Headline, from the CHANGELOG [11] |
|---|---|---|
| v0.1.0 | 20250207 | First GitHub release; memory-json importer |
| v0.13.0 | 20250611 | Multiple projects, incremental `edit_note`, moves with database consistency, OAuth, one app-level database |
| v0.15.0 | 20251004 | Cloud upload; fix for a case where creating "Node C" overwrote "Node A.md" through fuzzy matching |
| v0.16.0 | 20251111 | README announces the Cloud launch |
| v0.17.0 | 20251228 | Anonymous usage telemetry; format-on-save |
| v0.19.0 | 20260307 | Semantic search (FastEmbed, sqlite-vec, pgvector), schema system, per-project cloud routing, FastMCP 3.0 |
| v0.22.0 | 20260611 | Team-safe `bm cloud push` and `pull` |
| v0.23.0 | 20260824 | Opt-in reranking, Milvus, compare-and-swap writes, retrieval inspector; `canvas` tool removed; FastMCP 4 beta |
| v0.24.0 | 20261023 | Wiki projection, OKF export, valid-time qualifiers, Markdown path links, security fixes, semantic search always on |
| v1.0.0 | 20261029 | Only `bm_*` tools; cloud mirror sync removed |

## Recent changes (last 90 days, from 20260801)

- **Volume and concentration.** 880 commits since 20260801 (245 in August, 296 in September, 339 in October); one
  login authored 800 of them [34]. The snapshot's `commits_90d` shows 100 with a cap flag [39]; the live figure
  paginates the API.
- **Security.** The v0.24.0 notes record a high-severity DNS-rebinding flaw: a web page could reach an HTTP-transport
  MCP server bound to localhost and call every tool, including reading and deleting notes; releases before v0.24.0 are
  affected, stdio is not [11]. I could not find the advisory ID in GitHub's global advisory database (HTTP 404 at
  20261030 19:35 UTC) [37]. `SECURITY.md` still lists only "0.x.x" as supported [31].
- **Breaking changes in v0.24.0.** Refused writes and edits became MCP errors; HTTP transports bind to `127.0.0.1`;
  semantic search can no longer be turned off [11].
- **After v1.0.0** (20261030): fixes to `bm_schema`, onboarding and missing-project messages [34].

## Sources

1. https://api.github.com/repos/basicmachines-co/basic-memory and `/branches/main`: counts, licence field, dates, head commit (read 20261030 19:37 UTC; first read 19:29)
2. https://api.github.com/repos/basicmachines-co/basic-memory/releases?per_page=100 and `/releases/latest`: releases (read 20261030 19:30 and 19:34 UTC)
3. https://pypi.org/pypi/basic-memory/json, and pypi.org/pypi/mcp/json, pypi.org/pypi/fastmcp/json: versions, upload times, licence field (read 20261030 19:30 and 19:37 UTC)
4. https://github.com/basicmachines-co/basic-memory/blob/main/README.md: claims, install, cloud, pricing, tools, packages (read 20261030 19:29 UTC)
5. https://github.com/basicmachines-co/basic-memory/blob/main/LICENSE: AGPL version 3 text; its only commit is the initial one of 20241202 (read 20261030 19:29 and 19:31 UTC)
6. https://github.com/basicmachines-co/basic-memory/blob/main/pyproject.toml: dependencies, licence field (read 20261030 19:29 UTC)
7. https://github.com/basicmachines-co/basic-memory/blob/main/docs/NOTE-FORMAT.md: front matter, observations, relations, schemas (read 20261030 19:29 UTC)
8. https://github.com/basicmachines-co/basic-memory/blob/main/docs/MARKDOWN_RELATIONS.md: Markdown path links, `bm_parse_semantics` (read 20261030 19:29 UTC)
9. https://github.com/basicmachines-co/basic-memory/blob/main/docs/LOCKED_NOTES.md: `locked: true` (read 20261030 19:29 UTC)
10. https://github.com/basicmachines-co/basic-memory/blob/main/docs/DOMAIN_MODEL.md: projects, projections, source of truth, journal (read 20261030 19:29 UTC)
11. https://github.com/basicmachines-co/basic-memory/blob/main/CHANGELOG.md: release notes, security note, history (read 20261030 19:29 UTC)
12. https://github.com/basicmachines-co/basic-memory/blob/main/docs/semantic-search.md: embeddings, chunking, fusion, reindex, backends (read 20261030 19:29 UTC)
13. https://github.com/basicmachines-co/basic-memory/blob/main/docs/DOCTOR.md: `bm doctor` (read 20261030 19:32 UTC)
14. https://github.com/basicmachines-co/basic-memory/blob/main/docs/1.0.md: 1.0 tools, migration, refusals (read 20261030 19:29 UTC)
15. https://github.com/basicmachines-co/basic-memory/blob/main/AGENTS.md: consistency model (read 20261030 19:29 UTC)
16. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/mcp/tools/__init__.py: tool registry (read 20261030 19:31 UTC)
17. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/mcp/tools/ranked_search.py: `bm_search` contract (read 20261030 19:31 UTC)
18. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/mcp/tools/context.py: `bm_context` output (read 20261030 19:31 UTC)
19. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/schemas/search.py: search result fields (read 20261030 19:32 UTC)
20. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/mcp/server.py: server starts the watcher (read 20261030 19:31 UTC)
21. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/config_models.py: defaults (read 20261030 19:32 UTC)
22. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/cli/commands/db.py: `bm reset` (read 20261030 19:32 UTC)
23. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/index/watch_service.py: `watchfiles` watcher (read 20261030 19:32 UTC)
24. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/services/initialization.py: start-up indexing (read 20261030 19:33 UTC)
25. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/services/link_resolver.py: `project::note` (read 20261030 19:32 UTC)
26. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/services/bulk_link_resolver.py: bulk relation targets (read 20261030 19:32 UTC)
27. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/models/search.py: search-index DDL (read 20261030 19:32 UTC)
28. https://api.github.com/repos/basicmachines-co/basic-memory/git/trees/HEAD?recursive=1: file layout, migrations (read 20261030 19:29 UTC)
29. https://github.com/basicmachines-co/basic-memory/blob/main/CLA.md: copyright assignment (read 20261030 19:31 UTC)
30. https://github.com/basicmachines-co/basic-memory/blob/main/CONTRIBUTING.md: DCO and CLA (read 20261030 19:31 UTC)
31. https://github.com/basicmachines-co/basic-memory/blob/main/SECURITY.md: supported versions (read 20261030 19:29 UTC)
32. https://github.com/basicmachines-co/basic-memory/blob/main/benchmarks/benchmarks/results/matrix-v2-summary.md: project benchmark matrix; date from the commits API (read 20261030 19:33 UTC)
33. https://github.com/basicmachines-co/basic-memory/blob/main/docs/multilingual-embedding-benchmark.md: embedding comparison (read 20261030 19:33 UTC)
34. https://api.github.com/repos/basicmachines-co/basic-memory/commits?since=2026-08-01T00:00:00Z: commit count, authors, subjects (read 20261030 19:33 UTC)
35. https://api.github.com/repos/basicmachines-co/basic-memory/contributors and the issue search API: contributors, issues (read 20261030 19:33 UTC)
36. https://api.github.com/orgs/basicmachines-co/repos and the code search API for "workos" and "stripe" in this repository (read 20261030 19:31 UTC)
37. WebSearch for independent evaluations (20261030 19:35 UTC); https://api.github.com/advisories/GHSA-4gfv-c2mm-mvj2 returned HTTP 404 (20261030 19:35 UTC)
38. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/man/man1/okf-export(1).md: OKF export (read 20261030 19:33 UTC)
39. [`../landscape/20261030_1913-github/repos.tsv`](../landscape/20261030_1913-github/repos.tsv) and [`README.md`](../landscape/20261030_1913-github/README.md): snapshot row and flags (snapshot 20261030 19:13 UTC)
40. https://github.com/basicmachines-co/basic-memory/blob/main/docs/ai-assistant-guide-extended.md: project and workspace addressing (read 20261030 19:31 UTC)
41. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/models/knowledge.py and `src/basic_memory/__init__.py`: entity model, `external_id` default; also `src/basic_memory/__init__.py`, `config.py` and `db.py`, checked for licence headers (read 20261030 19:32 UTC)
42. https://github.com/basicmachines-co/basic-memory/blob/main/src/basic_memory/indexing/change_detector.py: checksum change detection (read 20261030 19:32 UTC)
