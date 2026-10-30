---
slug: llm-wiki-nashsu
repo: nashsu/llm_wiki
tier: deep
category: markdown-kb
snapshot: 20261030 19:29 UTC
---

# LLM Wiki (nashsu/llm_wiki)

Repository metadata, README, LICENSE and the gist were read at 20261030 19:29 UTC; source files at 19:30 to 19:31;
commit, contributor and issue data at 19:32 to 19:35. Each source below carries its own time. Source files were read
on `main` at commit `e08cfce65a` (20261021 11:17 UTC), still the branch head at 19:35 [1].

| | |
|---|---|
| Repository | https://github.com/nashsu/llm_wiki |
| Licence | GPL version 3, from the `LICENSE` file: the line "LLM Wiki — Copyright (C) 2024-2026 Yong Su", then the unmodified GNU GPL v3 text [4]. GitHub's API reports `NOASSERTION` ("Other") [1]. The README says "GNU General Public License v3.0" and agrees with the file [3]. "Only" or "or later": **unstated** (see Licence below). |
| Language | TypeScript by GitHub's count [1]. A Tauri v2 desktop app: Rust backend, React 19 frontend [3][14]. |
| Stars, forks | 21,197 and 2,404 (20261030 19:29 UTC; unchanged at 19:35) [1] |
| Created, last push | 20260408 11:24 UTC, 20261021 11:17 UTC [1] |
| Latest release | v0.6.13, 20261022 01:21 UTC [2] |
| Status | active (pushed 9 days before the read); not archived [1]. No commit to `main` after the v0.6.13 release commit; pull requests keep arriving (newest 20261027) [16][26]. |
| Paper, docs | No paper. The README, in English, Chinese, Japanese and Korean [3]. The homepage field is empty and the tree holds no `docs/` folder [1]. The design source is Karpathy's gist [5]. |

## What it is

LLM Wiki is a cross-platform desktop application that turns imported documents (PDF, Office files, e-books, web
clips) into a folder of interlinked Markdown pages, written and kept current by an LLM [3]. It implements a pattern
that Andrej Karpathy published as a gist on 20260404. The README calls the project "based on Karpathy's LLM Wiki
pattern", the gist "an abstract design pattern", and itself "a concrete implementation with substantial
extensions" [3]. It ranks first by stars in the snapshot's `markdown-kb` table [19]. It is a one-maintainer project:
87% of the last 90 days of commits are by the owner [16].

### The "LLM wiki" pattern, and what this application adds

**The pattern.** The gist (page: "Created April 4, 2026 at 16:25", time zone not stated) says that most LLM use on
documents looks like RAG, where "the LLM is rediscovering knowledge from scratch on every question". Its
alternative: "the LLM **incrementally builds and maintains a persistent wiki**", a "structured, interlinked
collection of markdown files that sits between you and the raw sources", so that "the knowledge is compiled once
and then *kept current*, not re-derived on every query" [5]. The [timeline](../llm-era/README.md) records the gist
and the wave of implementations after it [6].

| Element | What the gist says [5] |
|---|---|
| Three layers | Raw sources (immutable); the wiki ("the LLM owns this layer entirely"); a schema document such as `CLAUDE.md` or `AGENTS.md` with conventions and workflows. |
| Ingest | The LLM reads a source, writes a summary page, updates the index and the entity and concept pages, and appends to the log. "A single source might touch 10-15 wiki pages." |
| Query | The LLM searches, reads and answers with citations; "good answers can be filed back into the wiki as new pages". |
| Lint | A periodic check for contradictions, stale claims, orphan pages and missing cross-references. |
| `index.md`, `log.md` | The index is a catalogue the LLM reads first; it "avoids the need for embedding-based RAG infrastructure" at "moderate scale (~100 sources, ~hundreds of pages)". The log is append-only. |
| Scale | "at small scale the index file is enough, but as the wiki grows you want proper search." No threshold is given. |

The gist calls itself "intentionally abstract" [5]. The repository holds a copy as `llm-wiki.md`, byte-identical
to the raw gist text I read at 19:29; the commit that added it is dated 20260405 09:27 UTC [5][1].

**What the application adds.** The README keeps the three layers, the three operations, `index.md`, `log.md`,
wikilinks and Obsidian compatibility, and lists its own additions [3]. Those I confirmed in the code:

| Addition (README's claim [3]) | Where confirmed |
|---|---|
| A desktop app instead of a document pasted into an agent | Tauri app [14] |
| `purpose.md`, a file for the wiki's goals, put into prompts | Ingest prompts [7] |
| Two-step ingest (analysis, then generation), hash cache, persistent queue | [7] |
| Graph with a four-signal relevance score and Louvain communities | [10] |
| Optional vector search, review queue, Deep Research | [9][7][12] |
| Local HTTP API, MCP server, agent skill | [15] |

I did not read the web clipper or the cascade deletion beyond their presence. The idea is the gist's. This
repository adds engineering around it: a queue, a cache, a merge step, a search backend and an agent and MCP
surface.

## How it works

### Data model: a folder of files

A project is a folder [3]:

| Path | Holds |
|---|---|
| `purpose.md`, `schema.md` | Goals and page-type rules, both put into prompts [3][7] |
| `raw/sources/`, `raw/assets/` | Imported originals ("immutable") and local images |
| `wiki/index.md`, `log.md`, `overview.md` | Catalogue, chronological log, global summary |
| `wiki/entities/`, `concepts/`, `sources/`, `queries/`, `synthesis/`, `comparisons/` | Generated pages by type |
| `.obsidian/`, `.llm-wiki/` | Vault settings; app state (cache, queue, chats, reviews, vector index) |

The generation prompt allows the types source, entity, concept, comparison, query, synthesis, thesis, methodology
and finding. A `schema.md` section named "Page types" can map custom types to folders, and the app moves a page to
the folder its type requires [22]. Five templates (Research, Reading, Personal Growth, Business, General) pre-fill
`purpose.md` and `schema.md` [3][22].

**Page format.** Each page starts with YAML front matter: `type`, `title`, `created`, `updated`, `tags`, `related`
(bare slugs) and `sources` (source file names, which must include the file being ingested). Links are `[[wikilinks]]`
in the body. File names are kebab-case for Latin scripts; Chinese, Japanese and Korean titles keep their
characters [7]. The parser tolerates a code fence or a stray first line around the front matter [22].

### Ingestion

| Stage | What happens | LLM? |
|---|---|---|
| Parse | Format-specific extraction (PDF, DOCX, PPTX, XLSX, EPUB/MOBI, images); optional MinerU for complex PDFs [3][14] | No |
| Cache | SHA-256 of the content; an unchanged source is skipped (`.llm-wiki/ingest-cache.json`) [7] | No |
| Images | Embedded images are extracted and, if configured, captioned by a vision model [3][7] | Per image |
| 1. Analysis | One call at temperature 0.1: entities (at most 25), concepts (25), arguments (15), links to existing pages, contradictions, recommendations. Each entity is marked "Page-worthy: yes/no", and only "yes" earns a page. Inputs: schema, purpose, and the index cut to 32,000 characters [7] | Yes |
| Long sources | Over a budget derived from the context window, the text is split into overlapping chunks, each analysed with a running "global digest" and checkpointed [7] | One call per chunk |
| 2. Generation | One call that must output only `FILE` blocks (path plus full page) and optional `REVIEW` blocks. The prompt forbids writing `index.md` and `overview.md` [7] | Yes |
| Review stage | A third call proposing review items, only if the output is 10,000 characters or more, has four or more file blocks, or already holds a review block [7] | Conditional |
| Write | `log.md` entries are appended; an existing content page is merged (below); a truncated file triggers a repair call [7] | Conditional |
| Index, overview | Updated by code: a `[[target]] — title` bullet per new page and a bounded "recent" section [7] | No |
| Embeddings | If enabled, each written page is chunked and embedded [7][23] | Embedding model |

The queue is saved in `.llm-wiki/ingest-queue.json`; a failed task is retried up to three times [7]. An interrupted
generation can resume (commit 20260927, shipped in v0.6.12) [16]. An interactive `startIngest` path streams the
analysis into the chat before a later call writes files; I read only its opening lines [7].

**Merging.** When another source produces a page that exists, three layers apply [8]. The arrays `sources`, `tags`
and `related` are unioned in code. If the bodies differ, an LLM merges them, told to preserve "every factual claim
from both inputs"; a result shorter than 70% of the longer input is rejected. The fields `type`, `title` and
`created` stay as they were. On failure the new body wins and the old page is backed up in `.llm-wiki/page-history/`.
One exception: when a changed source is re-ingested, a page that lists only that source is replaced, not merged [7].

**Calls per source:** at least two (analysis, generation), plus calls for long sources, a long output, a truncated
file, each merge and each captioned image. The maintainer accepts the cost: on 20260429 he wrote that ingest is slower
than other knowledge-base tools because the AI analyses and links the content, "which is the value of the karpathy
llm_wiki methodology" (my translation) [18].

### Links and the graph

No LLM extracts the graph. The maintainer's reply speaks of "knowledge graph extraction" during ingest [18], but I
found no separate extraction call in the ingest flow [7]. Edges are the `[[wikilinks]]` in bodies plus the `related`
front-matter list [10]. They are untyped but weighted. A relevance score sums four signals: direct links (weight
3.0), shared files in `sources` (4.0), common neighbours by the Adamic-Adar measure (1.5) and same page type (1.0)
[10]. Louvain groups pages into communities; the README says the app flags isolated pages, sparse communities and
bridge nodes as "knowledge gaps" [3]. A separate "enrich wikilinks" call asks the model only for term-to-target
substitutions and applies them in code, so the model cannot rewrite the page [22].

### Querying

Retrieval runs in the Rust backend [9]:

1. **Keyword scoring** over the Markdown files in `wiki/`: an exact file-name match scores 200, the phrase in the
   title 50, each body occurrence 20 (up to 10), each matching title token 5, each body token 1. CJK text is split
   into two-character pieces and single characters. The scan stops after 10,000 files.
2. **Vector search** (off by default): embeddings in an embedded LanceDB table, `.llm-wiki/lancedb`. With both on,
   the two ranked lists are merged by reciprocal rank fusion with k = 60 [9][23].
3. **Graph blending**: pages linked to top hits fill 15% to 30% of the result slots, fewer as vector coverage rises.

Chat goes through a Rust agent (`agent_start_turn`); the chat panel also keeps a path that streams an answer from
retrieved context [12]. A model-driven planner picks tools: wiki search and read, raw-source search, graph search,
web search, a desktop-search tool (AnyTXT), a deep-research run, a page write, skills, file tools in an
`agent-workspace/` folder, and shell commands (external ones need approval). The loop is capped at 4, 8 or 12 tool
steps by mode, and at 8, 16 or 20 when skills are used. A chat search returns 5 pages by default, 10 at most [12].
The README says answers cite pages by number [3]. "Save to Wiki" files an answer under `wiki/queries/` and
re-ingests it, which is the gist's "file answers back" step [3].

**Lint** has a structural part (orphan pages, broken links, pages with no outgoing links), which is plain code, and a
semantic part that sends each page's first 500 characters to an LLM for contradictions, stale claims and missing
pages; findings about pages that already exist are filtered out in code [21].

### Interface for other tools

The app serves a JSON API on `127.0.0.1:19828`, token-protected (a setting allows unauthenticated local access),
covering projects, files, hybrid search, graph, reviews, source rescan, chat with optional streaming, and page write
and embed [3][15]. A bundled Node MCP server calls it. The MCP README lists 10 tools; the code registers 12, adding
`llm_wiki_embed_page` and `llm_wiki_write_page`, the latter returning success "only after byte-for-byte
persistence verification" [15]. A separate repository, `nashsu/llm_wiki_skill`, installs an agent skill for Claude
Code or Codex; GitHub reports 152 stars, no licence, last push 20260519 [25].

## Cost and operating profile

| Question | Answer |
|---|---|
| Local? | The app and its files are local [3]. Inference is local only if the user picks Ollama or a local custom endpoint. |
| Models | Provider types: OpenAI, Anthropic, Google, Azure OpenAI, Ollama, MiniMax, custom (OpenAI- or Anthropic-compatible), and two local CLIs. Presets add DeepSeek, Atlas Cloud, Groq, xAI, NVIDIA NIM, Kimi, Zhipu, Alibaba Bailian, Xiaomi MiMo, Volcengine Ark and Ollama Cloud [13]. |
| Local inference | "Ollama (Local)" points at `http://localhost:11434` and suggests no model; "Custom" takes any base URL, so a local OpenAI-compatible server fits [13]. |
| "Local CLI" | "Claude Code CLI (local)" and "Codex CLI (local)" run the installed binary without an API key. A preset comment says the Claude CLI "forwards to the same Anthropic backend": "local" is the program, not the model [13]. |
| Embeddings | Own endpoint, key and model; any OpenAI-compatible `/v1/embeddings` URL per the README, with Google and Volcengine request shapes in code [3][9]. Off by default [13]. No bundled embedding model in the dependency list [14]. |
| Context window | 4K to 1M per the README [3]; default 204,800, **counted in characters** per a source comment [11][13]. |
| Network | The update check calls the GitHub releases API [24]. Web search (README: Tavily, SerpApi, SearXNG) is optional [3]. I searched `package.json`, `Cargo.toml`, `main.tsx` and the update checker for analytics libraries and found none; other code was not searched [14][24]. |
| Keys | The LLM configuration, which has an `apiKey` field, is saved under `llmConfig` in the Tauri store `app-state.json` [13][24]. Encrypted or not: **unstated**. |
| Platforms | v0.6.13 assets: Windows x64; macOS Apple Silicon only; Linux deb, rpm and AppImage for amd64 and arm64 [2]. At least three open issues ask for an Intel Mac build (#68, #95, #375) [18]. |
| Build | Node 20+, Rust 1.88+, protoc [3]. |
| Spend | See the call table. Per question: the planner and answer calls plus tools. No cost figures published: **unstated**. |

### State on disk, and whether a human can edit it

The knowledge is plain Markdown with YAML front matter in `wiki/**/*.md` [3][7]. It opens in Obsidian (the app
writes a vault config) or in the app's Milkdown editor [3][14]. There is no SQL database. App state lives in
`.llm-wiki/`:

| Item | Format | Human-editable? |
|---|---|---|
| `ingest-cache.json`, `ingest-queue.json`, `image-caption-cache.json`, `chats/{id}.json`, `ingest-progress/` | JSON | Readable, not meant to be edited [7][3] |
| `lancedb` | LanceDB vector tables, optional | No [23] |
| `page-history/`, `ingest-warnings.log` | Markdown backups; text | Yes [7] |

The graph is rebuilt from the Markdown files and cached in memory [10]. Two limits on hand editing. Re-ingesting a
changed source replaces any page that lists only that source, edits included [7]. And the vector index follows
the files only through the app or the API: the README offers an endpoint to index "one externally created or updated"
page; whether an Obsidian edit is picked up automatically is **unstated** [3].

### Licence

The file is GPL version 3 with one line of copyright notice ahead of it. After that line and one blank line, its 674
lines are identical to the text at gnu.org (read 19:32) [4]. `NOASSERTION` is probably caused by the extra line; that
is my inference, not GitHub's statement. Operative terms, quoted from the file [4]:

- Section 2: "This License explicitly affirms your unlimited permission to run the unmodified Program." You may
  "make, run and propagate covered works that you do not convey, without conditions". Output "is covered by this
  License only if the output, given its content, constitutes a covered work".
- Section 4: verbatim copies may be conveyed if the notices are kept and you "give all recipients a copy of this
  License"; "You may charge any price or no price for each copy".
- Section 5: a modified work needs "prominent notices stating that you modified it", and "You must license the
  entire work, as a whole, under this License to anyone who comes into possession of a copy".
- Section 6: object code must come with the "machine-readable Corresponding Source".

Gaps. I found no "any later version" wording in the README, the licence line or the source files read [3][4][7].
`package.json` and `Cargo.toml` carry no licence field [14]. `extension/Readability.js` has an Apache-2.0 header
(Arc90); `Turndown.js` shows none in its first lines; the bundled pdfium libraries were not examined, so their
terms are **unstated** here [28]. This reference treats GPL projects as read-only: ideas and measured results are
reusable, source code is not. This is a reading of the file, not legal advice.

## Evidence

**Published results.** One: the README says "overall recall improved from 58.2% to 71.4% with vector search
enabled" [3]. It names no dataset, question set, count or definition of recall. A GitHub code search at 19:34 for
"58.2" in the repository found only the four README files [27]. It stands as an unexplained claim.

**Maintainer statements.** In issue #5 he answers, on 20260413, a question about hundreds of thousands of documents:
with vector search retrieval latency "should be a few seconds at most"; on 20260428, that with a vector index search
performance and accuracy "are optimal" (my translations from Chinese). The thread holds no measurement. A user with
a repository of 50 GB or more reported a very long load at each start (20260626); the maintainer said he would
think about optimising, and none of the 15 comments follows up [18]. The keyword scan in code stops at 10,000
Markdown files; the vector path is separate [9].

**Independent evaluation.** None found. A web search at 19:34 returned blog posts and directory listings; I cited
none. A search of this reference's `kb-kg` folder for the repository name finds it only in the landscape snapshot
and selection files, not in the papers-and-benchmarks file. Where an index-based wiki stops working is still an
open question in the [timeline](../llm-era/README.md) [6].

**Tests.** 152 files with `.test.` in the path; npm scripts separate mock tests from tests that call real models
[1][14]. The CI workflow builds the frontend and the Rust code on three systems and has no test step [20].

**Where the README is older than the code.**

| README says [3] | Code says |
|---|---|
| Step 2 yields "Updated index.md, log.md, overview.md" | The prompt forbids the model from writing `index.md` and `overview.md`; code updates them [7] |
| Context split 60% pages, 20% history, 5% index, 15% system | 50% pages, 5% index, 15% response reserve; history and system prompt are not budgeted [11] |
| Search "searches both `wiki/` and `raw/sources/`" | `search_project` scans `wiki/` only; raw sources are a separate agent tool [9][12] |
| Web search: Tavily, SerpApi, SearXNG | Also Firecrawl, Ollama, Brave, Bocha [12] |
| English and Chinese interface | Locale files for English, Italian, Russian, Chinese [1] |
| A four-phase query pipeline in the chat flow | Search is in Rust and chat runs through the agent [9][12] |

None of these changes the main finding. They mean the README is not a safe description of current behaviour.

## Direction

There is no roadmap. `plans/multimodal-images.md` still says "Spec, not started" although image ingestion has
shipped, so it is stale [1][16]. The last 90 days of commits point three ways [16]:

- **Ingest at scale:** a concurrent worker pool, a resumable queue and generation, bounded prompts, checks for
  truncated model output.
- **More ways in:** standalone images, a MinerU 4 API, multi-project source watching, a streaming chat API, an MCP
  page-write tool.
- **Model breadth:** per-task reasoning controls, fixes to the Claude and Codex CLI transports, contributed Italian
  and Russian translations. Open pull requests add Vietnamese and a GitHub Copilot provider [26].

### Maturity

| Measure | Value (read 20261030, UTC) |
|---|---|
| Age | 205 days since 20260408 [1] |
| Contributors | 35 named accounts, 43 with anonymous [17]; the owner has 778 of 894 commits credited to named accounts (87%) [17] |
| Last 90 days | 134 commits: August 91, September 27, October 16 (to 20261021); 117 by the owner [16] |
| Releases | 62 since v0.3.0 (20260412). Per month: April 22, May 11, June 15, July 7, August 5, September 1, October 1. Seven in the last 90 days; about 34 days between v0.6.11 and v0.6.12 [2] |
| Issues | 188 open, 362 closed [17] |
| Pull requests | 98 open, 149 closed, 81 merged [17] |
| CI | Builds only; the newest five runs show the status `action_required` [20] |
| Adoption signals | 2,404 forks (11.34 per 100 stars); 86 watchers; 3,671 downloads summed over the 12 assets of v0.6.13 in 8 days, including the extension zip and an `.app.tar.gz` [1][2] |

Both releases and commits per month fall after the first months. Eighteen of the 25 most-discussed open issues are
titled in Chinese; some report crashes or failures, ask for an Intel Mac build, or ask for a headless server mode
(#231, #762) [18]. Open issue #486 asks whether the project is built on `Ar9av/obsidian-wiki`; its two replies are
not from the owner account [18].

**Snapshot flags.** None was raised. The flags are heuristics: `fast-growth` at 150 stars per day or more, `low-forks`
below 3 forks per 100 stars for repositories with 5,000+ stars. This repository has 103.4 and 11.34 [19]. The README
explains no launch beyond the link to the gist. The gist (20260404) and the first commit of its copy (20260405)
precede the repository's creation date (20260408) [1][5]. The evidence read does not support a conclusion about how
the stars arose.

## Recent changes

Selected from 134 commit subjects since 20260731 19:00 UTC [16]. Dates are commit dates.

| Date | Change |
|---|---|
| 20260802 | v0.6.7: recoverable ingest queue controls; bounded concurrent source parsing; optional kept parsed Markdown |
| 20260810 | Concurrent ingest worker pool; ingest preparation split from commit; configurable structural lint |
| 20260814 | v0.6.9: single-page vector indexing API; MinerU 3.x backend names |
| 20260820 | Batch deep research for reviews; knowledge filtered by source; chat model routed into the backend agent |
| 20260916 | Verified MCP page writes; truncated-analysis detection; ingest queue resumes after restart |
| 20260927 | v0.6.12 (published 20260928): resumable generation; standalone image sources; grounded entity pages |
| 20261021 | v0.6.13 (published 20261022): MinerU 4 API; path-style wiki links; bounded index prompt; preview history |

## Sources

1. https://api.github.com/repos/nashsu/llm_wiki, its `main` branch, git tree and the commit list for `llm-wiki.md`: stars, forks, issues, licence field, dates, language, head commit `e08cfce65a`, layout (read 20261030 19:29 UTC; counts and head re-read 19:35 UTC)
2. https://api.github.com/repos/nashsu/llm_wiki/releases: 62 releases and dates (read 20261030 19:29 UTC); latest release, assets and download counts (19:32 UTC)
3. https://github.com/nashsu/llm_wiki/blob/main/README.md: features, layout, API, claims, benchmark sentence, licence line (read 20261030 19:29 UTC)
4. https://github.com/nashsu/llm_wiki/blob/main/LICENSE (read 20261030 19:29 UTC), compared with https://www.gnu.org/licenses/gpl-3.0.txt (read 19:32 UTC)
5. Karpathy's gist, https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f: page for the creation time (read 20261030 19:29 UTC); text from https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw (19:29 UTC), equal to the repository's `llm-wiki.md` read through the contents API (19:29 UTC). The gist API returned HTTP 502 at 19:34 UTC.
6. [LLM-era timeline](../llm-era/README.md): the 20260404 gist row and the LLM-wiki wave (read 20261030 19:28 UTC)
7. https://github.com/nashsu/llm_wiki/blob/main/src/lib/ingest.ts: prompts, ingest flow, merging, index and overview updates, queue (read 20261030 19:30 UTC)
8. https://github.com/nashsu/llm_wiki/blob/main/src/lib/page-merge.ts: page merge rules (read 20261030 19:30 UTC)
9. https://github.com/nashsu/llm_wiki/blob/main/src-tauri/src/commands/search.rs: scoring, fusion, graph blending (read 20261030 19:31 UTC)
10. https://github.com/nashsu/llm_wiki/blob/main/src/lib/graph-relevance.ts and https://github.com/nashsu/llm_wiki/blob/main/src/lib/wiki-graph.ts: relevance weights, edges (read 20261030 19:30 and 19:33 UTC)
11. https://github.com/nashsu/llm_wiki/blob/main/src/lib/context-budget.ts: context budget constants (read 20261030 19:31 UTC)
12. https://github.com/nashsu/llm_wiki/blob/main/src-tauri/src/agent/runtime.rs, `tools.rs` and `router.rs` in the same folder, and https://github.com/nashsu/llm_wiki/blob/main/src/components/chat/chat-panel.tsx: agent loop, tools, limits, web search providers, chat paths (read 20261030 19:31 UTC)
13. https://github.com/nashsu/llm_wiki/blob/main/src/components/settings/llm-presets.ts, https://github.com/nashsu/llm_wiki/blob/main/src/stores/wiki-store.ts and `src/lib/llm-providers.ts`: providers, presets, defaults (read 20261030 19:30 and 19:31 UTC)
14. https://github.com/nashsu/llm_wiki/blob/main/src-tauri/Cargo.toml and https://github.com/nashsu/llm_wiki/blob/main/package.json: version 0.6.13, dependencies, test scripts (read 20261030 19:31 UTC)
15. https://github.com/nashsu/llm_wiki/blob/main/mcp-server/README.md, `mcp-server/src/index.ts` and `src-tauri/src/api_server.rs`: MCP tools, API port and routes (read 20261030 19:33 UTC)
16. https://api.github.com/repos/nashsu/llm_wiki/commits?since=2026-07-31T19:00:00Z: 134 commits, authors, subjects (read 20261030 19:32 UTC)
17. https://api.github.com/repos/nashsu/llm_wiki/contributors (with and without `anon`) and https://api.github.com/search/issues counts for issues and pull requests (read 20261030 19:32 UTC)
18. https://github.com/nashsu/llm_wiki/issues/5 and its comments, issue #486, and the open-issue list sorted by comments (read 20261030 19:33 UTC)
19. [Landscape snapshot 20261030 19:13](../landscape/20261030_1913-github/README.md), its `repos.tsv`, and the flag thresholds in [`tools/gh_snapshot.py`](../../tools/gh_snapshot.py) (read 20261030 19:28 UTC)
20. https://github.com/nashsu/llm_wiki/blob/main/.github/workflows/ci.yml and https://api.github.com/repos/nashsu/llm_wiki/actions/runs (read 20261030 19:33 UTC)
21. https://github.com/nashsu/llm_wiki/blob/main/src/lib/lint.ts and `lint-structural-core.ts` (read 20261030 19:31 UTC)
22. https://github.com/nashsu/llm_wiki/blob/main/src/lib/frontmatter.ts, `wiki-page-types.ts`, `wiki-schema.ts`, `templates.ts` and `enrich-wikilinks.ts` (read 20261030 19:30 to 19:33 UTC)
23. https://github.com/nashsu/llm_wiki/blob/main/src-tauri/src/commands/vectorstore.rs and https://github.com/nashsu/llm_wiki/blob/main/src/lib/text-chunker.ts: LanceDB path, Markdown-aware chunking (read 20261030 19:31 UTC)
24. https://github.com/nashsu/llm_wiki/blob/main/src/lib/update-check.ts and `src/lib/project-store.ts`: update check, settings store (read 20261030 19:31 and 19:35 UTC)
25. https://api.github.com/repos/nashsu/llm_wiki_skill: stars, licence field, last push (read 20261030 19:35 UTC)
26. https://api.github.com/repos/nashsu/llm_wiki/pulls?state=open: newest open pull requests (read 20261030 19:33 UTC)
27. GitHub code search API, query `"58.2" repo:nashsu/llm_wiki` (read 20261030 19:34 UTC)
28. https://github.com/nashsu/llm_wiki/blob/main/extension/Readability.js and `extension/Turndown.js`, first lines (read 20261030 19:35 UTC)
