---
type: project
repo: modelcontextprotocol/servers
trends: [infrastructure-and-mcp]
updated: 20261102 23:18 UTC
---

# MCP reference servers

This page answers what the `modelcontextprotocol/servers` repository holds, what its Memory server stores, and how that server finds anything. The repository is a set of reference implementations of the [Model Context Protocol](../index/model-context-protocol.md), not a memory product. The watch-list table on the chapter landing carries its stars and push dates.

| Field | Value |
|---|---|
| Repository | https://github.com/modelcontextprotocol/servers |
| Licence | GitHub cannot classify it: the licence endpoint returns `NOASSERTION` ("Other") [1][2]. The `LICENSE` file is a composite. It opens by saying the project is "undergoing a licensing transition from the MIT License to the Apache License, Version 2.0" [2]. New code and specification contributions are Apache-2.0; documentation (excluding specifications) is CC-BY-4.0; contributions from authors who have not consented to relicensing stay MIT. The file holds the Apache-2.0 and MIT texts and a notice that documentation is CC-BY-4.0, with a link to the licence text [2]. The file's history shows the MIT text of 20241119 and 20250816 replaced by this composite in a commit of 20260112 22:50 UTC titled "chore: update licensing to Apache 2.0 for new contributions" [12]. |
| Trends | [Infrastructure and MCP](../trends/infrastructure-and-mcp.md) |

## What it is

The README calls the repository "a collection of *reference implementations*" of the protocol and says the servers are "educational examples", "not as production-ready solutions" [3]. It holds seven servers: Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking and Time. Thirteen earlier servers sit in a separate archive repository, and the README sends readers who want a list of servers to the MCP Registry [3].

Only one server concerns this documentation. The Memory server is described as a "[knowledge graph](../index/knowledge-graph.md)-based persistent memory system" [3]. Its own README calls it "a basic implementation of persistent memory using a local knowledge graph", so a model can remember facts about the user across chats [4]. It is published on npm as `@modelcontextprotocol/server-memory` [4][6].

Licence for the Memory server: the repository README says new contributions are Apache-2.0 and existing code MIT [3]. The server's own README says MIT, and its `package.json` says "SEE LICENSE IN LICENSE" [4][6]. Which licence covers a given line of the Memory server: **unstated**.

## How it works

The graph has three kinds of item [4]:

| Item | Content |
|---|---|
| Entity | A unique name, an entity type and a list of observations |
| Relation | A directed link: from, to, and a relation type written in active voice |
| Observation | One atomic fact, a string attached to an entity |

Nine tools create, delete, read, search and open these items. A resource, `memory://knowledge-graph`, returns the whole graph, and clients can subscribe to changes [4][5].

**Storage.** One JSON Lines file: `memory.jsonl` by default, or the path in `MEMORY_FILE_PATH`. Each line is an object of type "entity" or "relation" [4][5]. Each client starts its own server process, so every write takes an exclusive lock file beside the memory file. A lock left by a crashed process is cleared at once if its process is known to have exited, otherwise after 30 seconds without refresh, and a write that cannot get the lock within 60 seconds fails instead of overwriting [4].

**Search.** `search_nodes` is a case-insensitive substring match over entity names, types and observations. The source comments it as a "Very basic search function" [5]. It returns the matches and the relations with at least one matching endpoint [5]. A search of the source for embedding, vector and OpenAI terms found none; the calling model decides what to store, and the README gives an example system prompt that tells it what to remember [4][5].

**Transport.** Every server in the repository serves stdio; only Everything also serves Streamable HTTP [3].

*Reading:* this is the smallest useful form of [agent memory](../index/agent-memory.md): a knowledge graph with no extraction step, no [embeddings](../index/embedding.md) and no ranking. Everything that other memory systems automate is left to the model and the prompt. That makes it a baseline and a teaching example, which is what the README says it is.

## Evidence

None published. No benchmark, evaluation or accuracy figure appears in the repository README or the Memory README; the only match for "evaluate" is a warning that developers should evaluate their own security needs [3][4]. No third-party evaluation of the Memory server was fetched: **unstated**.

## Status and direction

- **Latest release.** v2.2.0, 20261028. The release lists seven packages; the Memory package was published at 2.0.1 [8][9]. Its notes add a security notice on CA certificates; the Memory server makes no network connections [9].
- **Release history.** Date-stamped tags ran to 2026.8.31. Then v1.0.0 on 20261011, "the final release of the legacy era servers"; v2.0.0 on 20261019, which "refactors all the servers to support the modern era spec"; v2.1.0 on 20261025; v2.2.0 on 20261028 [8][9].
- **Activity, 20260804 to 20261102.** 792 commits on `main`: 17 in August (the window starts on the 4th; the first commit in it is 20260818), 89 in September, 686 in October [10]. Not archived [1].

*Reading:* the October jump coincides with merges of the `v2` branch into `main` (the v2.0.0 notes list "merge v2/main into main"); the commits were not inspected one by one.
- **Memory server changes.** 2.0.0 moved to version 2 of the TypeScript SDK (software development kit), requires Node.js 24 or later, and serves the 2026-07-28 protocol revision beside the 2025 one. 2.0.1 stops startup when the `memory.json` to `memory.jsonl` migration fails, and keeps stored fields it does not model, which earlier writes dropped [7]. The newest change to `src/memory` is 20261028 [11].
- **Direction.** No roadmap file was read: **unstated**. The README does not say it is in maintenance mode and names no hosted tier [3].

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [LlamaIndex](llama-index.md)
- [Projects](README.md)

**Index**

- [Model Context Protocol](../index/model-context-protocol.md)
- [Tool use](../index/tool-use.md)

<!-- END GENERATED: appears-in -->

## Sources

No paper is cited. The papers chapter group page for the trend is [Infrastructure and MCP papers](../papers/README.md).

1. https://api.github.com/repos/modelcontextprotocol/servers : licence field (`NOASSERTION`), archived flag (false), created 20241119 (read 20261102 20:19 UTC)
2. https://github.com/modelcontextprotocol/servers/blob/main/LICENSE : composite licence text (opening paragraph; Apache-2.0 text, MIT text, and a CC-BY-4.0 notice with a link to the licence text; the licence endpoint reports the file as "Other" (read 20261102 20:36 UTC)
3. https://github.com/modelcontextprotocol/servers/blob/main/README.md : description, warning, server list, archived list, transports, licence section (read 20261102 20:20 UTC)
4. https://github.com/modelcontextprotocol/servers/blob/main/src/memory/README.md : concepts, tools, resource, storage, locking, protocol versions, example prompt, licence line (read 20261102 20:20 UTC)
5. https://github.com/modelcontextprotocol/servers/blob/main/src/memory/index.ts : nine tools and one resource, JSONL entity and relation lines, substring search, no embedding, vector or OpenAI terms (read 20261102 20:20 UTC)
6. https://github.com/modelcontextprotocol/servers/blob/main/src/memory/package.json : package name, version 2.0.1, licence field (read 20261102 20:20 UTC)
7. https://github.com/modelcontextprotocol/servers/blob/main/src/memory/CHANGELOG.md : changes 1.0.0, 2.0.0, 2.0.1 (read 20261102 20:20 UTC)
8. https://github.com/modelcontextprotocol/servers/releases : release list and dates, v2.2.0 latest (read 20261102 20:21 UTC)
9. https://github.com/modelcontextprotocol/servers/releases/tag/v2.2.0 : package table, security notice; the v1.0.0 and v2.0.0 notes on the same releases page (read 20261102 20:21 UTC)
10. https://github.com/modelcontextprotocol/servers/commits/main : commits since 20260804 counted by month through the commits API; August count and first commit date re-read 20261102 20:36 UTC (read 20261102 20:21 UTC)
11. https://github.com/modelcontextprotocol/servers/commits/main/src/memory : newest commits touching the Memory server (read 20261102 20:22 UTC)
12. https://api.github.com/repos/modelcontextprotocol/servers/commits?path=LICENSE and the file text at each commit : MIT 2024-11-19 (37415258) and 2025-08-16 (88a80f37, year edit), composite with Apache-2.0 2026-01-12 22:50 UTC (6b36e3c2) (read 20261102 22:58 UTC)
