---
slug: openviking
repo: volcengine/OpenViking
tier: deep
category: agent-memory
snapshot: 20261030 19:29 UTC
---

# OpenViking

Reading times: repository metadata, README, `LICENSE` and the licence commit at 20261030 19:29 UTC; concept pages
and source files between 19:30 and 19:36 UTC; the benchmark blog, arXiv pages and web searches between 19:32 and
19:33 UTC. Each source below carries its own time. The first landscape snapshot (20261030 19:13 UTC) is used only
for the growth flag [38].

| | |
|---|---|
| Repository | https://github.com/volcengine/OpenViking |
| Licence | AGPL-3.0, from the `LICENSE` file: the GNU Affero GPL v3 text with a few wording differences from the GNU reference copy (see "Licence and the 20260330 change") [4][5]. GitHub's API, the README badge and PyPI also say AGPL-3.0, so nothing disagrees [1][6][41]. Other parts of the tree: `crates/ov_cli` and `examples/` Apache-2.0 (the README's list; `crates/LICENSE` is an Apache text); the Hermes plugin and the Microsoft Agent Framework adapter MIT; the LangChain adapter AGPL-3.0; `bot/license/LICENSE` is MIT ("nanobot contributors") and is not listed in the README [6][42]. Under this repository's licence rule the code is a read-only reference. |
| Language | Python is GitHub's primary language [1]. The tree also holds a C++ vector engine (`src/index`), Rust crates (`ragfs`, `ov_cli`) and Go and TypeScript SDKs [1]. |
| Stars, forks | 41,196 and 3,343 (20261030 19:29 UTC) [1]. Open issues plus pull requests 1,166: by search, 391 issues and 775 pull requests [1][39]. |
| Created, last push | 20260105 07:11 UTC, 20261030 17:52 UTC (any branch) [1] |
| Latest release | v0.5.2.1, 20261027 13:44 UTC [2] |
| Status | active (pushed within 90 days); not archived [1] |
| Paper, docs | https://docs.openviking.ai/ (linked from the README) and `docs/` in the repository [6]. Three arXiv papers by project-linked authors: 2605.29640, 2606.16903, 2609.11390 [6][33][34][35]. |

## What it is

OpenViking is an open-source "context database for AI agents", "initiated and maintained by the Viking team at
ByteDance's Volcengine" [6][11]. It puts knowledge ("resources"), memories and skills in one virtual filesystem
addressed by `viking://` URIs, with a vector index beside the files and a generated summary on each directory [6][12].
An LLM writes memories when a conversation session is committed [18]. Agents reach it through an HTTP API, a CLI
(`ov`), Python, Go and TypeScript SDKs, an MCP endpoint and plugins for coding agents [6][28]. Volcengine sells a
hosted edition [6]. The project does not call itself a knowledge graph. The store is a file tree plus a vector index;
the only graph-like parts I found are LLM-extracted typed links between memory pages and an optional "compile" job
that writes entity files and an edge file [25][27].

## How it works

### Data model

| Layer | What it holds | Source |
|---|---|---|
| URI space | `viking://resources` (account-wide), `viking://user/{id}/` (memories, resources, skills, peers, sessions), `viking://agent/skills` (account-shared). `viking://~` aliases the caller's own user root. | [19] |
| Content store | Files and directories in AGFS, now a Rust implementation (RAGFS). Backends: local disk, S3-compatible, in-memory. A layer called VikingFS maps URIs to account-scoped paths and keeps the index in step on `rm` and `mv`. | [15] |
| Vector index | One record per indexed URI: `uri`, `parent_uri`, `context_type`, `is_leaf`, dense and sparse vectors, `abstract`, `name`, `description`, `created_at`, `active_count`. Backends: local, HTTP, Volcengine VikingDB; commits add an openGauss adapter in September 2026. The v0.2.14 notes say `parent_uri` was removed from the vector store; the storage page still lists it. Which is current was not checked in code. | [3][15][40] |
| Context and memory types | Resource, memory, skill (a `SKILL.md` package), rule (beta). Memory types: `profile`, `preferences`, `entities`, `events`, `identity`, `soul`, `cases`, `trajectories`, `experiences`; custom types allowed. | [13][18] |
| Sessions | `messages.jsonl`, numbered archives under `history/`, and a `memory_diff.json` audit file of added, updated and deleted memories. | [18] |

**Three tiers.** L0 is a one-sentence abstract (`.abstract.md`, default budget 256 characters), L1 an overview
(`.overview.md`, 4,000 characters), L2 the original content, read only when needed [6][14]. L0 and L1 exist per
directory, not per file; file summaries feed the directory's L1 [14]. The sidecars are Markdown with YAML frontmatter
(directory, source, generator, freshness). The docs call this "OKF Markdown" without expanding the name, so whether it
is the OKF in the [timeline](../llm-era/README.md) is unstated [14]. A large directory refreshes its parent summary only
when pending child changes reach 10% of its entries (default) [14].

**Typed links.** During memory extraction the LLM may emit links between memory pages, each with a type, a weight, a
matching word and a description. They are stored in the memory file, and a separate module renders them as an HTML
force-directed graph [25]. I found no mention of links, relations or graphs in the retrieval modules I read [20][22].

### Ingestion

Parser, tree builder, resource processor, content store, semantic queue, vector index [12][16]. The Markdown parser
splits at headings (default 2,000 characters); code uses tree-sitter skeletons. Processing is asynchronous and returns
a task id [16].

### Retrieval

| Step | Behaviour | Source |
|---|---|---|
| `find` | One query, no session, no LLM: embed the query and run one vector search inside the permitted scope. | [17][20] |
| `search` | With a `session_id` and `retrieval.enable_intent` (default true), an LLM plans zero to five typed queries (memory, resource, skill) from the session summary, the last five messages and the query. Without session content it behaves like `find`. | [17][21][29] |
| Global search | The module docstring reads "Global vector retrieval with optional reranking". Target directories, type, permissions and filters narrow one search. The class is still named `HierarchicalRetriever`, but the docs say "retrieval does not navigate directories recursively" and that directory priority queues and parent-to-child score propagation were removed. | [17][20] |
| Rerank | If a reranker is configured, `search` recalls 2 x `limit` candidates and reranks their abstracts once; on failure it keeps vector scores. | [17][20] |
| Context mode | MCP `search` with `mode="context"` assembles injection-ready text under a token budget, with per-type quotas and cross-turn dedup. | [22][28] |

The README promises "Search a directory, not the whole index" and says a trie-based directory index (TrieHI) resolves
directory scopes before vector ranking [6]. The C++ engine does contain a trie mapping path prefixes to bitmaps [26].
I did not trace the call from the Python retriever to it, so I cannot confirm it serves `target_directories`.

### Where a model is called

| When | Step | Model | Source |
|---|---|---|---|
| Write | Parsing of images, audio and video; some parsers call models | VLM or external parser | [16] |
| Write | Per-file summary: tree-sitter skeleton for code, the LLM only as fallback; LLM for documents and other text. With no VLM available the summary is empty and a warning is logged. | VLM | [16][23] |
| Write | Directory L1 overview, bottom-up, concurrency 32 by default; L0 is cut from the L1 text, not a second call | VLM | [14][16][23] |
| Write | Embedding of L0, L1 and file records; an MCP option (`vectors_only`) skips the VLM step | embedding model | [16][28] |
| Write | Session commit, memory extraction: a bounded tool-using loop. It pre-fetches a listing, an overview and a search, lets the model call read, search and ls tools, then takes the operations (add, update, delete, links) the model returns. The constructor default is 3 iterations; its docstring says 5. The architecture page says an updater writes "LLM merge and deduplication" back as patches; the updater's docstring says it applies the model's final operations. | VLM | [12][24] |
| Write | Archive summary at commit: described on the session page, but working memory is off by default (`working_memory.enabled=false`), so by default a commit stores raw messages and schedules extraction only | VLM | [18][30] |
| Write | Agent Evolution (cases, trajectories, experiences; off by default) and `ov compile` (an agent runtime follows a Skill to write a wiki, knowledge graph, report or memory clean-up) | agent LLM | [18][27][29] |
| Read | Query embedding for semantic searches (a keyword search type skips it) | embedding model | [20] |
| Read | Intent analysis (the query planner; falls back to the main VLM; a fine-tuned 0.8B local model is recommended) | LLM | [21][29] |
| Read | Rerank; optional LLM digest of assembled context ("rewrite", opt-in, fail-closed) | reranker, LLM | [17][20][22] |

OpenViking returns contexts; the calling agent writes the answer. The project's harnesses add their own QA and judge
models [31].

### Agent interface

The MCP endpoint (`/mcp`, same port as the REST API) exposes `find`, `search`, `read`, `download`, `list`, `tree`,
`remember`, `write`, `edit`, `add_resource`, `add_skill`, `grep`, `glob`, `forget`, watch, privacy and ACL tools [28].
The README lists integrations for Claude Code, Codex, Cursor, TRAE, OpenClaw, Hermes, OpenCode, pi, DeerFlow, DSH,
Doubao Work and LangChain, plus an installer script [6]. A gateway that brings memory to any API-key client appeared
in October 2026 (commit title only) [40].

## Cost and operating profile

| Item | What the sources say | Source |
|---|---|---|
| LLM at index time | One call per non-code text file, plus one per directory for the L1 overview (batched when large). Code files skip the call when a skeleton can be extracted. No cost figure per file is stated. | [16][23] |
| LLM at commit | At least one extraction loop of a few calls, plus a merge step; no cost figure stated | [24] |
| LLM per query | None for `find`; one planner call for `search` with session context; optional reranker and digest | [17][22] |
| Project's indexing claim | 8,671,538 tokens over its five single-turn RAG sets, against 62,705,469 for LightRAG ("about 13.8%"), its own comparison | [32] |
| Needs | Python 3.10+, uv, "a model provider with an embedding model and a VLM"; default port 1933 | [6][12] |
| Default embedder | A local GGUF model, `bge-small-zh-v1.5` (512 dimensions, Chinese-language), downloaded on first use; other providers are configurable | [29] |
| Local only? | The docs describe a local embedder, an Ollama VLM and a local query planner. I did not run it, so a fully offline setup is untested here. | [6][29] |
| Hosted | Volcengine service, "first 50 files are free"; BytePlus hosting "planned" | [6] |

## Licence and the 20260330 change

**Commit.** `ce998873f9`, "lisence: change the main lisence to AGPL-3.0 (#1085)", committed 20260330 06:37 UTC [7].
The body says "change the main lisence from Apache-2.0 to AGPL-v3" three times. The pull request changed 614 files
[9]. It replaced `LICENSE` (662 lines added, 201 removed), added Apache `LICENSE` copies under `crates/ov_cli` and
`examples`, and swapped the SPDX header in source files from Apache-2.0 to AGPL-3.0 [7].

**Earlier licence: Apache-2.0.** `LICENSE` in the parent commit is the Apache License, Version 2.0 text [7]. The same
commit rewrites "licensed under the Apache License 2.0" in the README, the FAQ and the headers [7]. `LICENSE` has only
two commits: this one and a "first commit" dated 20260129 [8]. The repository was created 20260105, but the history I
could list starts on 20260129 with pull request numbers from #1. Whether anything preceded it, and under what
licence, is **unstated** [1][8].

| Date (UTC) | Event | Source |
|---|---|---|
| 20260326 03:37 | A maintainer posts "Plan to change lisence" in Discussions: AGPLv3 "starting with version 0.3". Replies the same day: "when?" is answered "early April, once the community has no questions" (my translation of the Chinese); one commenter backs AGPL for the server but asks for a permissive client. | [10] |
| 20260330 06:07 | v0.2.14 published. The licence commit is two commits ahead of its tag, so this is the last release under Apache-2.0. | [3] |
| 20260330 06:37 | Licence commit lands; the README lists per-component licences. | [7][9] |
| 20260330 06:40 | Maintainer in the thread: the Rust CLI and examples are exempted and stay Apache-2.0. | [10] |
| 20260331 07:15 | v0.3.1 published: the first release tag containing the commit. The v0.2.14 and v0.3.1 notes contain no licence line. | [3] |

**Reason the project gives** (the Discussions post, in English and Chinese) [10]:

- The "current Apache-2.0 license ... imposes weak restrictions on commercial service providers"; the team wants "to
  require open-sourcing for high-value commercial derivative works built on OpenViking".
- It plans "a managed public cloud version" and, "as a commercial entity", wants to "balance community advancement
  with sustainable commercial development".
- It describes AGPLv3's principle as "open-source and free; closed-source requires a commercial license" and names
  Redis, Elasticsearch and Grafana as adopters. That is the project's statement; I did not check it.

The pull request body gives no reason, only the component list [9]. The README now offers a "Self-Managed" edition
"activated by a license key" with distributed deployment and official support [6]. Whether that is a commercial licence
of the same code is **unstated**. The pull request carries a CLA-assistant comment, so a contributor licence agreement
service is in use [9]; `CONTRIBUTING.md` has no line matching "CLA" or "licen" [42]. The agreement's terms, and whether
earlier contributors agreed to the change, are **unstated**.

**What the file says today** [4][5][6]:

- `LICENSE` is the AGPL v3 text (661 lines). Against the GNU reference copy it differs in about ten places: a doubled
  "provided", "makes the unnecessary", "PROGRAM" for "PROGRAMS" in the disclaimer, re-wrapped lines, and one phrase,
  "for use in or with those products", that the reference lacks in the patent paragraph. Legal effect was not assessed.
- The README adds a sentence outside the licence text: "any wholesale rewriting and subsequent re-open-sourcing of
  this project is prohibited", and translating "all or a substantial portion" into another language "requires prior
  written authorization from Volcano Engine". The `LICENSE` file contains neither. Whether this is a licence term, a
  notice or a request is **unstated**; when it was added was not traced.

## Relationship to Volcengine and ByteDance

Only what the sources state:

| Statement | Source |
|---|---|
| The GitHub owner `volcengine` is an Organization | [1] |
| "Initiated and maintained by the Viking team at ByteDance's Volcengine". VikingDB was used inside ByteDance from 2019 and offered on Volcengine's public cloud in 2024; MineContext was open-sourced in late 2025 and OpenViking in "early 2026". | [11] |
| README: "Copyright © 2026 Volcano Engine (火山引擎) and the OpenViking contributors". Source headers: "Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd." | [6][20] |
| Volcengine hosts "OpenViking Service" and sells a self-managed edition; hosting outside China is "planned" on BytePlus | [6] |
| Maintainer posts are signed "Volcano Engine Viking Team" and speak of "a commercial entity". A config file touched by the licence commit reads "By ByteDance/Volcengine". | [7][10] |
| An arXiv abstract by project-linked authors refers to "ByteDance's Viking vector search engine" and says TrieHI "has been integrated into OpenViking" | [34] |

**Unstated:** the legal relation between Volcano Engine and ByteDance beyond "ByteDance's Volcengine"; how many
maintainers are employees; who holds copyright in outside contributions. The author addresses on the two licence
commits use a ByteDance email domain (addresses not reproduced) [7][8].

## Evidence

### The project's own claims (self-reported)

| Claim | Figures | Source |
|---|---|---|
| LoCoMo accuracy, agent's native memory to agent plus OpenViking | OpenClaw 24.20% to 82.08%; Hermes 33.38% to 82.86%; Claude Code 57.21% to 80.32%. Query time down 58.45% to 66.10%; input tokens down 34.3% to 91.0%. | [6][32] |
| tau2-bench task success, LLM without memory to with OpenViking experience memory | Retail 70.94% to 77.81%; Airline 54.38% to 66.25% | [6][32] |
| ClawWork | Net income after 50 tasks $2,269.77 to $3,843.74 | [32] |
| HotpotQA: accuracy / tokens per question / latency | OpenViking top-5 72.75% / 3,154 / 0.22 s; top-20 91.00% / 12,533 / 0.23 s. Same table: naive RAG 62.50%; HippoRAG 2 61.00%; LightRAG 89.00% / 28,443 / 75 s; LangChain SQL agent 78.00%. | [32] |
| Five single-turn RAG sets (FinanceBench, NaturalQuestions, ClapNQ, Qasper, SyllabusQA), average accuracy | OpenViking 66.87%; LightRAG 76.00%; naive RAG 53.93%; HippoRAG 2 44.50%; PageIndex 36.75% | [32] |

Setup, as the project describes it:

- The README says the memory evaluation ran on OpenViking 0.3.22 with Doubao 2.0 Pro as the VLM and
  Doubao-embedding-vision-251215 for embeddings, both Volcengine models [6]. Release v0.3.22 is dated 20260529, the day
  of the blog post [3][32].
- The blog (20260529, "OpenViking Team"), as I read it, does not state model names, question counts (except 50
  ClawWork tasks), the judge model, dataset subsets or how baselines were run, and links no scripts [32]. The
  repository's `benchmark/` folder holds scripts [6][31].
- The repository's benchmark guide says the report "does not pin every runtime parameter", that choosing `e2e` alone
  "does not establish an exact reproduction", that the mem0-style comparison uses a more permissive judge so scores
  "are not directly comparable", and that RAG-mode LoCoMo runs are not memory results [31].
- The LoCoMo baselines are each agent's own memory, not other memory systems. The HotpotQA row in bold is top-20;
  LightRAG scores higher than OpenViking on the five-set average [32].

### Independent evaluation: none found

- Two web searches (20261030 19:33 UTC) and this repository's [papers list](../papers-benchmarks/README.md) found no
  third-party re-run of the LoCoMo, tau2 or RAG numbers [37][44].
- A review post dated 20260831 (the page also carries a conflicting 20261030 check date) states "All of the numbers
  are vendor-run" and "nobody independent has re-run them". It shows no measurements of its own [36].
- A single-developer harness, memtrust, lists OpenViking as a backend; per a search summary its sample run skipped it
  for a missing key and gives no scores. I did not fetch the page [37].

### Papers by project-linked authors (abstract pages only)

| Paper | Claim on the abstract page | Source |
|---|---|---|
| VikingMem, 2605.29640, v1 20260528, "Accepted by VLDB26" | Built on the VikingDB engine; "outperforms baselines by up to 30% in memory retrieval effectiveness". The page does not name OpenViking; the README says OpenViking open-sources "a subset". | [6][33] |
| Directory-Aware Query and Maintenance in Vector Databases, 2606.16903, 20260615 | Compares path-expansion designs with a trie index (TrieHI) in ByteDance's Viking engine; says TrieHI is in OpenViking. No numbers. The README says "Accepted by ICDE"; the page lists no venue. | [6][34] |
| VikingRAG, 2609.11390, 20260910 | 11.6% to 51.9% of the tokens of state-of-the-art methods at matching accuracy; 5.1% to 32.5% with trace reuse. The page does not name OpenViking; the README says its core mechanisms are integrated. | [6][35] |

Names the About page thanks as academic collaborators also appear in these author lists, so the papers are not
independent evaluations [11][33][34][35].

## Attention and the growth flag

The snapshot **carries no flag for this repository**: its `flags` field is empty [38].

| Measure | Value | Source |
|---|---|---|
| Stars per day, whole life | 138.24 (41,196 over 298 days). `fast-growth` needs 150 or more. | [38] |
| Forks per 100 stars | 8.11. `low-forks` needs 5,000+ stars and under 3. The median over the 128 snapshot repositories with 5,000+ stars is 10.8 (my computation). | [38] |
| Rank in the agent-memory table; contributors | 6; 324 | [38] |
| Issues and pull requests | 391 open and 1,186 closed issues; 3,186 merged pull requests | [39] |
| Commits since 20260731 | 1,192 by 158 distinct authors; the five most frequent account for 485 | [40] |

These flags are heuristics. Two more points:

- The README does not describe a launch; it carries a Trendshift badge [6]. The release notes I read (the first 900
  characters of v0.2.13, v0.2.14 and v0.3.1; v0.5.2.1 in full) mention none [2][3].
- The 20260326 post says the project "is poised to reach 20k GitHub Stars" [10]. Taking that as about 20,000, the
  average was roughly 250 a day over the first 81 days and roughly 97 a day over the next 218 (my arithmetic).

I could not examine the star timeline or who starred: the REST stargazers endpoint returned 404 and the GraphQL
count returned 0 for this repository and for LightRAG, so the listing appears unavailable here [43]. The evidence
supports a large, busy repository whose lifetime rate sits just under the flag threshold and has slowed. It does not
say whether the stars are organic.

## Direction

- **Stated roadmap.** Two items under future directions: "Further distributed-storage development" and "More
  agent-framework adapters". No dates [45].
- **From commit subjects.** Four themes recur: multi-tenant server features (OIDC and LDAP auth, MySQL and Redis
  account stores, multi-write storage v2); a gateway for memory in any API-key client; `compile` jobs (wiki,
  knowledge graph, memory consolidation, a Map/Shuffle/Reduce pipeline, incremental updates); and agent evolution
  plus a rule service [40].

## Recent changes

Last 90 days, from the commit list and release list (read 19:35 and 19:34 UTC) [3][40]:

| Item | Detail |
|---|---|
| Volume | 1,192 commits by conventional-commit prefix: fix 672, feat 254, docs 116, refactor 39, perf 24, test 14. |
| Releases | 18 `v*` tags, v0.4.12 (20260803) to v0.5.2.1 (20261027), plus CLI, Python SDK and Go SDK tags [3] |
| Breaking | 20260821: the uid-less `viking://user/...` shorthand removed in favour of `viking://~` (#4196, marked breaking) |
| Features | OIDC and LDAP auth (20260806); MCP write, edit and tree tools (20260812); Context Gateway (20261006, renamed OpenViking Gateway 20261009); `compile --skill memory` (20260926); rule service (20261026) |
| Working memory | Now off by default, per a guide whose date was not read [30] |
| Privacy | v0.5.2.1 (20261027): automatic detection of new sensitive values in session messages is "temporarily disabled" because it replaced ordinary content with placeholders; registered values still match [2]. A plugin change on 20261023 redacts secrets in captured transcripts [40]. |

## Gaps

Not read: the full text of the three papers, the `train/` module, `relations` routes, Gateway and VikingBot code,
reranker internals. Not run: any part of the software. The blog and arXiv pages were read through a summarising
fetch tool; blog figures were read twice and match the README.

## Sources

1. https://api.github.com/repos/volcengine/OpenViking and `.../git/trees/HEAD?recursive=1`: metadata, layout (read 20261030 19:29 UTC)
2. https://api.github.com/repos/volcengine/OpenViking/releases/latest: v0.5.2.1 and its notes (read 20261030 19:29 UTC)
3. https://api.github.com/repos/volcengine/OpenViking/releases (102 entries) and `.../compare/<tag>...ce998873f9`: release dates; which tags contain the licence commit (read 20261030 19:34 UTC)
4. https://github.com/volcengine/OpenViking/blob/main/LICENSE: AGPL v3 text (read 20261030 19:29 UTC)
5. https://www.gnu.org/licenses/agpl-3.0.txt: reference copy compared line by line with [4] (read 20261030 19:30 UTC)
6. https://github.com/volcengine/OpenViking/blob/main/README.md: pitch, tiers, integrations, benchmarks, licence section, editions, papers (read 20261030 19:29 UTC)
7. https://github.com/volcengine/OpenViking/commit/ce998873f94da5138c049c17ed40f7499dade4ce and `LICENSE` at its parent 9bcdaf47: message, diff, Apache-2.0 text (read 20261030 19:29 UTC)
8. https://api.github.com/repos/volcengine/OpenViking/commits?path=LICENSE: two commits (read 20261030 19:29 UTC)
9. https://github.com/volcengine/OpenViking/pull/1085: body, 614 changed files, CLA comment (read 20261030 19:29 UTC)
10. https://github.com/volcengine/OpenViking/discussions/992: "Plan to change lisence", reasons, replies (via GraphQL, 20261030 19:29 UTC)
11. `docs/en/about/01-about-us.md` in the repository: team, history, collaborators (read 20261030 19:35 UTC)
12. `docs/en/concepts/01-architecture.md`: modules, data flows (read 20261030 19:30 UTC)
13. `docs/en/concepts/02-context-types.md`: types and memory types (read 20261030 19:30 UTC)
14. `docs/en/concepts/03-context-layers.md`: L0/L1/L2, sidecars, freshness (read 20261030 19:30 UTC)
15. `docs/en/concepts/05-storage.md`: AGFS/RAGFS, index schema, backends (read 20261030 19:30 UTC)
16. `docs/en/concepts/06-extraction.md`: parsers, semantic queue, code skeletons (read 20261030 19:30 UTC)
17. `docs/en/concepts/07-retrieval.md`: `find`, `search`, intent, rerank (read 20261030 19:30 UTC)
18. `docs/en/concepts/08-session.md`: commit, archives, memory extraction (read 20261030 19:30 UTC)
19. `docs/en/concepts/04-viking-uri.md`: scopes, the `~` alias (read 20261030 19:31 UTC)
20. `openviking/retrieve/hierarchical_retriever.py` (read 20261030 19:30 UTC)
21. `openviking/retrieve/intent_analyzer.py` (read 20261030 19:30 UTC)
22. `openviking/retrieve/context_assembler/` `pipeline.py` and `rewrite.py` (19:30 UTC), `gather.py` (19:36 UTC), 20261030
23. `openviking/storage/queuefs/semantic_processor.py`: file summary and overview calls (read 20261030 19:31 UTC)
24. `openviking/session/memory/extract_loop.py` and `tools.py`: the extraction loop (read 20261030 19:31 UTC)
25. `openviking/session/memory/dataclass.py` and `graph_view.py`: typed links, graph rendering (read 20261030 19:31 UTC)
26. `src/index/detail/scalar/bitmap_holder/dir_index.h`: trie of path prefixes (read 20261030 19:31 UTC)
27. `docs/en/context-compilation/01-overview.md` and `03-knowledge-graph.md`: `ov compile` (read 20261030 19:31 UTC)
28. `docs/en/guides/06-mcp-integration.md`: MCP tools (read 20261030 19:31 UTC)
29. `docs/en/guides/01-configuration.md`: embedders, query planner, `enable_intent`, `agent_evolution.enabled` (read 20261030 19:36 UTC)
30. `docs/en/guides/working-memory-default-off.md` (read 20261030 19:36 UTC)
31. `benchmark/README.md` in the repository: evaluation guide and its caveats (read 20261030 19:32 UTC)
32. https://blog.openviking.ai/post/openviking-benchmark-results/: report of 20260529 (two reads via a summarising fetch, 20261030 19:32 UTC)
33. https://arxiv.org/abs/2605.29640: VikingMem abstract page (read 20261030 19:33 UTC)
34. https://arxiv.org/abs/2606.16903: Directory-Aware Query and Maintenance abstract page (read 20261030 19:33 UTC)
35. https://arxiv.org/abs/2609.11390: VikingRAG abstract page (read 20261030 19:33 UTC)
36. https://andrew.ooo/posts/openviking-context-database-ai-agent-memory-review/: third-party review post (read 20261030 19:33 UTC)
37. Two web searches for independent evaluations (result summaries, 20261030 19:33 UTC); memtrust is listed at https://pypi.org/project/memtrust/, not fetched
38. [`repos.tsv`](../landscape/20261030_1913-github/repos.tsv), row `volcengine/OpenViking`, and the thresholds in `tools/gh_snapshot.py` (snapshot 20261030 19:13 UTC; read 19:28 UTC)
39. GitHub issue-search counts for `repo:volcengine/OpenViking` (read 20261030 19:34 UTC)
40. https://api.github.com/repos/volcengine/OpenViking/commits?since=2026-07-31T00:00:00Z: 1,192 subjects (read 20261030 19:35 UTC)
41. https://pypi.org/pypi/openviking/json: version 0.5.2.1, licence expression AGPL-3.0 (read 20261030 19:34 UTC)
42. `CONTRIBUTING.md`, `bot/license/LICENSE`, `crates/LICENSE`, `examples/LICENSE` and the repository's LICENSE-file list (read 20261030 19:29 to 19:35 UTC)
43. `.../stargazers` (REST, 404) and the GraphQL `stargazers` count (0), also tried on HKUDS/LightRAG (20261030 19:33 UTC)
44. [`papers-benchmarks/README.md`](../papers-benchmarks/README.md) in this repository: searched for OpenViking, no hit (read 20261030 19:31 UTC)
45. `docs/en/about/03-roadmap.md`: stated roadmap (read 20261030 19:30 UTC)
