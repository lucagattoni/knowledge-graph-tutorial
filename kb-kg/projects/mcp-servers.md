---
slug: mcp-servers
repo: modelcontextprotocol/servers
tier: card
category: adjacent
snapshot: 20261030 19:46 UTC
---

# MCP reference servers (memory server)

| | |
|---|---|
| Repository | https://github.com/modelcontextprotocol/servers [1] |
| Licence | GitHub reports `NOASSERTION` [1]. The `LICENSE` file is a composite: its opening paragraph says the project is "undergoing a licensing transition from the MIT License to the Apache License, Version 2.0"; all new code and specification contributions are Apache-2.0; documentation contributions (excluding specifications) are CC-BY-4.0; contributions with relicensing consent are Apache-2.0; contributions by authors who have not given consent remain MIT. The file then holds the full Apache-2.0 text, an MIT text (Copyright 2024-2025 Model Context Protocol, a Series of LF Projects, LLC) and a CC-BY-4.0 notice [2]. The README licence section agrees [3]. The memory server's own README says MIT, and its `package.json` says "SEE LICENSE IN LICENSE" [4][5]. Which licence covers a given line of the memory server: unstated. |
| Language | TypeScript (GitHub primary); three servers are Python packages [1][3] |
| Stars, forks | 91,700, 11,892 (20261030 19:41 UTC; the [landscape snapshot](../landscape/20261030_1913-github/repos.tsv) of 20261030 19:13 UTC has 91,699 and 11,892) [1] |
| Created, last push | 20241119 01:10 UTC, 20261029 05:27 UTC [1] |
| Latest release | v2.2.0, 20261028 20:57 UTC [6]; the memory package `@modelcontextprotocol/server-memory` is at 2.0.1, published to npm 20261028 21:07 UTC [7] |
| Status | active (pushed within 90 days); no landscape flag [1] |
| Paper, docs | no paper; protocol docs at https://modelcontextprotocol.io [1]; memory server docs in `src/memory/README.md` [4] |

## What it is

The repository is a collection of reference implementations of the Model Context Protocol (MCP) and, by its README, "educational examples", "not production-ready solutions" [3]. It holds seven servers: Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking and Time; thirteen earlier ones sit in a separate archive repository [3]. The Memory server exists today under `src/memory` and is described as a "knowledge graph-based persistent memory system" [3][4]. Its README calls it "a basic implementation of persistent memory using a local knowledge graph", so a model can remember information about the user across chats [4]. No benchmark is published for it [3][4].

## How it works

The graph has entities (unique name, entity type, list of observation strings), directed relations (from, to, relation type in active voice) and observations (atomic facts attached to an entity) [4]. Nine tools create, delete, read, search and open these; a resource `memory://knowledge-graph` returns the whole graph [4]. Storage is one JSONL file, `memory.jsonl` by default or `MEMORY_FILE_PATH`; each line is a JSON object of type "entity" or "relation"; writes use a temporary file and rename, and a lock file orders writers [4][8]. `search_nodes` is a case-insensitive substring match over names, types and observations; the source calls it "very basic" [8]. No LLM call or embedding appears in the source; the calling model decides what to store [4][8].

## Status and direction

Active: 792 commits from 20260801 to 20261030 [9]. Releases moved from date-stamped tags (last 2026.8.31) to v1.0.0 (20261011), v2.0.0 (20261019), v2.1.0 (20261025), v2.2.0 (20261028) [6]. Memory 2.0.0 moved to TypeScript SDK v2 and serves the 2026-07-28 protocol revision beside the 2025 one; 2.0.1 fixes migration and keeps unknown fields [10]. Roadmap: unstated.

## Sources

1. https://github.com/modelcontextprotocol/servers : repository metadata via the GitHub API (stars, forks, licence field, dates) (read 20261030 19:41 UTC)
2. https://github.com/modelcontextprotocol/servers/blob/main/LICENSE : composite licence text, 216 lines; opening paragraph, MIT and CC-BY sections read, Apache text not compared line by line (read 20261030 19:41 UTC)
3. https://github.com/modelcontextprotocol/servers/blob/main/README.md : server list, archived list, warning, licence section (read 20261030 19:41 UTC)
4. https://github.com/modelcontextprotocol/servers/blob/main/src/memory/README.md : concepts, tools, resource, storage, licence line (read 20261030 19:42 UTC)
5. https://github.com/modelcontextprotocol/servers/blob/main/src/memory/package.json : name, version, licence field (read 20261030 19:42 UTC)
6. https://github.com/modelcontextprotocol/servers/releases : v1.0.0 to v2.2.0 and the date-stamped releases before them (read 20261030 19:41 UTC)
7. https://registry.npmjs.org/@modelcontextprotocol/server-memory : npm version history and licence field (read 20261030 19:42 UTC)
8. https://github.com/modelcontextprotocol/servers/blob/main/src/memory/index.ts : storage format, search, locking; searched for embedding terms, none found (read 20261030 19:42 UTC)
9. https://github.com/modelcontextprotocol/servers/commits/main : 792 commits since 20260801 and their subjects (read 20261030 19:42 UTC)
10. https://github.com/modelcontextprotocol/servers/blob/main/src/memory/CHANGELOG.md : memory package changes 1.0.0 to 2.0.1 (read 20261030 19:42 UTC)
