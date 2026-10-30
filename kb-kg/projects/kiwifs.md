---
slug: kiwifs
repo: kiwifs/kiwifs
tier: card
category: markdown-kb
snapshot: 20261030 19:42 UTC
---

# KiwiFS

| | |
|---|---|
| Repository | https://github.com/kiwifs/kiwifs [1] |
| Licence | Business Source License 1.1, from the `LICENSE` file; GitHub's API reports `NOASSERTION` [1][2]. The README badge and licence section also say BSL 1.1: they agree [3]. |
| Language | Go (GitHub primary language); the web UI is embedded in the binary [1][3] |
| Stars, forks | 870, 281 (20261030 19:42 UTC; same in the 19:13 landscape snapshot; 32.3 forks per 100 stars; no heuristic flag) [1] |
| Created, last push | 20260422 04:27 UTC, 20261028 05:12 UTC [1] |
| Latest release | v0.19.81, 20261028 05:12 UTC; 109 releases since v0.1.0 (20260424) [1] |
| Status | active (pushed within 90 days); not archived [1] |
| Paper, docs | no paper stated; `docs/`; docs.kiwifs.com (not fetched) [1][3] |

## What it is

A single Go binary that serves a folder of Markdown files as a versioned, searchable knowledge server for agents and people, with git history, full-text and optional vector search, a web UI, and REST, MCP, NFS, S3, WebDAV and FUSE access [3][4]. Files are the source of truth; indexes can be rebuilt [4]. The README names Karpathy's LLM Wiki as an inspiration and calls itself "the production runtime for this pattern" (its claim); no benchmark appears [3]. It gives the MCP tool count as 62 in one table and 69 in another; the server code and FAQ say 78 [3][7]. A hosted "KiwiFS Cloud" is described; who operates it is unstated [3][7].

**Licence terms** (my reading of the text, not legal advice) [2]:
- Copying, modifying, derivative works, redistribution and non-production use are granted; all copies stay under this licence.
- Production use is allowed unless it includes offering the software to third parties as a commercial hosted service substantially similar to it (a "Competing Service"). Permitted by name: own applications or internal services; embedding where it is not the main value; consulting, support and integration.
- Each version converts to Apache-2.0 four years after its release, or on the fourth anniversary of its first public distribution if that comes first; for v0.1.0, by 20300424 (my arithmetic).
- Otherwise a commercial licence is needed; breach ends your rights for all versions. A trademark clause bars the name and logo in forks and derivatives. A contact for other licensing is in the file.

## How it works

Every write, from any protocol, passes one serialised pipeline: validation and schema check, atomic file write, git commit, then updates to the full-text index (SQLite FTS5, BM25), the optional vector index, metadata and the wiki-link index, then events and webhooks [4]. The writer's actor name becomes the git author [3]. Reads can use DQL (a SQL-like query over frontmatter), backlinks and graph tools [3][7]. Embeddings come from OpenAI, Ollama, ONNX and others; I found LLM-provider code only for embeddings, and the memory guide leaves consolidation to the user [5][7]. Agents connect through 78 MCP tools [7].

## Status and direction

Active. 85 commits since 20260730 (40 in August, 6 in September, 39 in October); latest changes: S3 and WebDAV auth enforcement, per-space backup, UI fixes. 14 issues and pull requests are open [1]. The roadmap calls itself a living document; a React component library and hook scripts were unchecked when read [6]. Of 18 contributor accounts, two are bots; the top human account holds 194 of 449 contributions [1].

## Sources

1. https://github.com/kiwifs/kiwifs : API data: metadata, releases (109 counted), contributors, commits, issues (read 20261030 19:42 to 19:44 UTC)
2. https://github.com/kiwifs/kiwifs/blob/main/LICENSE : full Business Source License 1.1 text (read 20261030 19:42 to 19:44 UTC)
3. https://github.com/kiwifs/kiwifs/blob/main/README.md : features, comparison table, licence section (read 20261030 19:42 to 19:44 UTC)
4. https://github.com/kiwifs/kiwifs/blob/main/docs/ARCHITECTURE.md : design principles, write pipeline (read 20261030 19:42 to 19:44 UTC)
5. https://github.com/kiwifs/kiwifs/blob/main/docs/MEMORY.md : memory conventions (read 20261030 19:42 to 19:44 UTC)
6. https://github.com/kiwifs/kiwifs/blob/main/docs/ROADMAP.md : first 70 lines (read 20261030 19:42 to 19:44 UTC)
7. Source archive at commit aeb9a73 (`internal/mcpserver/`, tool-count test, `AGENTS.md`; LLM provider names searched under `internal/`) and https://github.com/kiwifs/kiwifs/blob/main/docs/FAQ.md : 78 tools, hosted offer (read 20261030 19:42 to 19:44 UTC)
