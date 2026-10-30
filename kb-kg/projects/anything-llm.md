---
slug: anything-llm
repo: Mintplex-Labs/anything-llm
tier: card
category: adjacent
snapshot: 20261030 19:47 UTC
---

# AnythingLLM

| | |
|---|---|
| Repository | https://github.com/Mintplex-Labs/anything-llm [1] |
| Licence | MIT, from the `LICENSE` file ("The MIT License", copyright "Mintplex Labs Inc."; head and tail read) [2]. The README says "This project is MIT licensed" and the GitHub field agrees [1][3]. |
| Language | JavaScript (GitHub primary language); a monorepo with a React frontend and NodeJS server and collector [1][3] |
| Stars, forks | 67,758, 7,626 (20261030 19:41 UTC; the 20261030 19:13 UTC landscape snapshot had the same figures) [1][9] |
| Created, last push | 20230604 02:29 UTC, 20261030 19:37 UTC [1] |
| Latest release | v1.19.0, 20261026 16:14 UTC [4] |
| Status | active (pushed within 90 days); not archived; no snapshot flag [1][9] |
| Paper, docs | no paper stated; docs at https://docs.anythingllm.com [3] |

## What it is

The README calls AnythingLLM "the all-in-one AI application that lets you build a private, fully-featured ChatGPT": connect a local or cloud LLM, ingest documents and chat with them [3]. It ships as a desktop app and as a Docker server with multiple users [3]. It is a document-chat application, not a knowledge-graph tool. No knowledge graph or GraphRAG feature was found: the documentation pages read describe only vector retrieval [5][6], and a code search finds no "graphrag" [10]. The one "knowledge graph" phrase is example response text in the API definition [10]. No benchmark or evaluation appears in the sources read: unstated.

## How it works

A separate collector process parses uploaded files into text [3]. Embedding a document into a workspace splits it into chunks, embeds each, and stores the vectors with their text in a vector database, LanceDB by default [3][5]. Attached documents are by default inserted whole into the chat; if they exceed the context window the user is asked whether to embed them instead [6]. A legacy page says a query returns typically 4 to 6 chunks above a similarity threshold [5]; an "Accuracy Optimized" option searches more chunks and re-ranks them, with LanceDB only [6]. Agents use external MCP servers as tools (client role only documented) [7]. The API has workspace chat, vector search and document upload [8].

## Status and direction

Active. Six releases from v1.16.0 (20260813) to v1.19.0 (20261026) [4]. The twelve newest commit subjects (20261027 to 20261030) are fixes, provider support and a Node 18 to 24 bump [11]. The README lists model routing, memories, scheduled tasks and MCP compatibility as features [3]. 24 open pull requests, 321 open issues [12]. Roadmap: unstated.

## Sources

All read 20261030 19:41-19:47 UTC (the clock was checked before and after the reads, not per call).

1. https://github.com/Mintplex-Labs/anything-llm : repository metadata via the GitHub API (stars, forks, licence field, dates, language)
2. https://github.com/Mintplex-Labs/anything-llm/blob/master/LICENSE : MIT licence text
3. https://github.com/Mintplex-Labs/anything-llm/blob/master/README.md : description, features, architecture, supported embedders and vector databases, licence section
4. https://github.com/Mintplex-Labs/anything-llm/releases : release dates since 20260701
5. https://docs.anythingllm.com/chatting-with-documents/rag-in-anythingllm : chunking, embedding, workspaces, retrieval (page marked legacy; says nothing of graphs or reranking)
6. https://docs.anythingllm.com/chatting-with-documents/introduction : attaching versus RAG, "Accuracy Optimized" re-ranking
7. https://docs.anythingllm.com/mcp-compatibility/overview : MCP client role
8. https://github.com/Mintplex-Labs/anything-llm/blob/master/server/swagger/openapi.json : API paths (workspace chat, `vector-search`, document upload); https://docs.anythingllm.com/features/api describes the API only at a high level
9. [repos.tsv](../landscape/20261030_1913-github/repos.tsv) : first GitHub snapshot (20261030 19:13 UTC); flags column empty for this repository
10. GitHub code search in the repository: no hit for "graphrag"; two hits for "knowledge graph", the same example response in `server/swagger/openapi.json` and `server/endpoints/api/system/index.js`
11. https://github.com/Mintplex-Labs/anything-llm/commits/master : commit subjects since 20260801
12. https://github.com/Mintplex-Labs/anything-llm/pulls : open pull request and issue counts via the search API
