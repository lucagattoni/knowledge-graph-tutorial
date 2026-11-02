---
type: project
repo: vitali87/code-graph-rag
trends: [code-knowledge-graphs, graph-query-generation]
updated: 20261102 23:17 UTC
---

# Code-Graph-RAG

A tool that turns a source-code repository into a [knowledge graph](../index/knowledge-graph.md) with a parser, not a language model, and lets a person or an [agent](../index/agent.md) query and edit the code through that graph. This page says what it builds, how an agent reaches it, what its authors measured, and how it is released.

| Field | Value |
|---|---|
| Repository | https://github.com/vitali87/code-graph-rag [1] |
| Licence | MIT, read from the `LICENSE` file; GitHub classifies it as MIT; `pyproject.toml` says MIT too [2][13] |
| Trends | [Code graphs for coding agents](../trends/code-knowledge-graphs.md), [Asking graphs in natural language](../trends/graph-query-generation.md) |

## What it is

The README describes a tool that parses a multi-language codebase with Tree-sitter (a parser that builds a syntax tree for each file), adds exact facts from compiler frontends and runtime traces where available, and stores the result in an embedded graph database that needs no server [4]. One graph holds many projects under one schema [4]. The user works through a command-line tool, `cgr`, or through a server for the [Model Context Protocol](../index/model-context-protocol.md) that Claude Code and other clients can call [4][5]. Fourteen languages are fully supported and eight more have structural support [4]. The authors also sell cloud-hosted and on-premise deployments, support and consulting [4].

## How it works

Indexing is deterministic. The MCP (Model Context Protocol) guide says the server starts without a model, and that "indexing and the deterministic tools" work with no LLM (large language model) configured [5]. The graph is a [property graph](../index/property-graph.md) with nodes such as Class, Function and Module, and edges such as CALLS, IMPORTS and INHERITS [4]. Optional steps add runtime traces (`cgr trace`) and vector [embeddings](../index/embedding.md); the README says Tree-sitter stays the backbone because a trace only sees code that ran [4].

The default store is an embedded SQLite file with a [Cypher](../index/cypher.md) engine written for it. [Memgraph](./memgraph.md) and [Neo4j](./neo4j.md) 5 are opt-in backends that run the same queries [4][6]. The default vector store is also SQLite [12][13].

The MCP guide lists 37 tools. They fall into groups [5]:

| Group | Examples | Uses an LLM? |
|---|---|---|
| Typed graph queries | `callers`, `callees`, `definition`, `implementors`, `tests_reaching` | No: fixed queries |
| Open-ended questions | `query_code_graph` (English to Cypher), `ask_agent` | Yes |
| Retrieval | `semantic_search`, `structural_search`, `get_code_snippet` | No; `semantic_search` needs the optional `semantic` extra (embeddings), `structural_search` the `ast-grep` extra |
| Edits | `rename`, `change_signature`, `surgical_replace_code` | No |
| Index lifecycle | `index_repository`, `update_repository`, `reingest` | No |

`query_code_graph` is the [text-to-query](../index/text-to-query.md) step. The embedded-graph page says generated queries are checked with an `EXPLAIN` plan, which refuses a write before it runs, and then run on a read-only SQLite connection [6]. A `--read-only` flag removes the write and edit tools from the list [5].

## Evidence

All results below are **first-party**: the authors ran them on their own harness. No third-party evaluation was found in the sources read; no dedicated search for one was run.

| What | Result | Who ran it |
|---|---|---|
| Find the files that call a symbol, on the project's own Python package, scored against a Python `ast` oracle | graph: precision 0.8457, recall 0.9886, F1 (a score that balances precision and recall) 0.9116; call-tuned grep: precision 0.3659, recall 1.0, F1 0.5358; bare-name grep: F1 0.3806 [7] | first-party |
| Same task on `django/django` | graph F1 0.957; call-tuned grep 0.789; bare-name grep 0.506 [7] | first-party |
| An agent answers 40 call-site questions on Django, same model and loop, with and without graph tools | mean F1 0.975 in both arms; graph arm used 23,777 input tokens per question against 8,625 for grep [8][9] | first-party |
| The same with a multi-hop question type | mean F1 0.9777 in both arms; 35,205 against 17,865 input tokens [8][9] | first-party |
| The same call-site test with a second model | graph arm F1 0.8539 against 0.9134 for grep; mean input tokens 341,356 for the graph arm against 474,564 for grep [8][9] | first-party |

The first two rows measure whether the right files are found, not whether an agent does better. The oracle and the grep conditions are scored on the same unit, a file and the callee's simple name, and the README says "Both grep conditions are name-based, so any called name is present textually" [7]. Grep therefore reaches recall 1.0 by construction in the first row; the graph's recall is below 1.0 where it does not resolve a call [7].

The agent rows are the end-to-end test: the first model ties grep and the second loses. The commit that added them names the models: "Opus 5 ties grep" and "Haiku 4.5 trails grep" [9]. The graph arm used more input tokens than grep with the first model and fewer with the second [8]. The harness README does not report these results; whether the files were re-run after a later hardening commit is unstated [7][9].

*Reading:* graph tools did not beat grep on answer quality in the authors' own agent test. The retrieval rows show a precision gain, but a scoring unit that guarantees grep's recall limits what they can show. The authors' case rests on retrieval precision and on the typed edit tools.

## Status and direction

The latest GitHub Release is v0.4.19, published 20261101 20:01 UTC; the list holds 37 releases, 23 of them since 20260804 [3]. Git tags run ahead: the newest read was v0.4.25, and `pyproject.toml` on `main` says 0.4.25 [3][13]. The README explains that tags follow every merge while releases and PyPI follow every 50th version [4]. Commit counts belong to the watch-list table.

The published roadmap, "a statement of direction rather than a schedule", covers about a year from mid-2026: call-resolution quality, dead-code precision, the evaluation harness, performance and security badges [10]. It lists "A hosted service" among things it does not intend to do, while the README offers managed cloud deployments [4][10]; how the two fit is unstated. The project is pre-1.0 with no API stability promise, and one lead maintainer holds final say [10][11].

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL](../trends/graph-query-generation.md)
- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [codebase-memory-mcp](codebase-memory-mcp.md)
- [Neo4j](neo4j.md)
- [Projects](README.md)

**Applied to Pinakes**

- [What Pinakes takes from each project](../applied-to-pinakes/takeaways.md)

**Index**

- [Abstract syntax tree](../index/abstract-syntax-tree.md)
- [Code graph](../index/code-graph.md)
- [Property graph](../index/property-graph.md)
- [Text-to-query](../index/text-to-query.md)
- [Tree-sitter](../index/tree-sitter.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/vitali87/code-graph-rag : repository metadata through the GitHub API (licence field, not archived, creation date, topics) (read 20261102 20:18 UTC)
2. https://github.com/vitali87/code-graph-rag/blob/main/LICENSE : MIT licence text, 1,071 bytes; the licence endpoint of the API names this file and classifies it MIT (read 20261102 20:19 UTC)
3. https://github.com/vitali87/code-graph-rag/releases : latest release, 37 releases, 23 dated since 20260804, tags, via the API (read 20261102 20:18 UTC; re-read 20261102 22:54 UTC with the same result: latest v0.4.19 of 20261101 20:01 UTC, newest tag v0.4.25)
4. https://github.com/vitali87/code-graph-rag/blob/main/README.md : description, languages, backends, version lines, enterprise services (read 20261102 20:18 UTC)
5. https://github.com/vitali87/code-graph-rag/blob/main/docs/guide/mcp-server.md : 37 tools (counted again), which need an LLM, the optional `semantic` and `ast-grep` extras, read-only mode (read 20261102 20:37 UTC)
6. https://github.com/vitali87/code-graph-rag/blob/main/docs/architecture/embedded-graph.md : embedded Cypher engine, backends table, read-only query checks (read 20261102 20:19 UTC)
7. https://github.com/vitali87/code-graph-rag/blob/main/evals/README.md : retrieval results, scoring unit, "name-based" sentence, oracle description, harness description (read 20261102 20:37 UTC)
8. https://github.com/vitali87/code-graph-rag/tree/main/evals/results : `agentic_qa.json`, `agentic_qa_multihop.json`, `haiku45/agentic_qa.json`: per-arm summaries, including mean input tokens of both arms for each file (read 20261102 20:37 UTC)
9. https://github.com/vitali87/code-graph-rag/commit/adcba33e : commit message of 20260822 naming the models behind the committed agent results (read 20261102 20:19 UTC)
10. https://github.com/vitali87/code-graph-rag/blob/main/docs/roadmap.md : roadmap and "what we do not intend to do" (read 20261102 20:21 UTC)
11. https://github.com/vitali87/code-graph-rag/blob/main/GOVERNANCE.md : maintainer-led governance (read 20261102 20:19 UTC)
12. https://github.com/vitali87/code-graph-rag/blob/main/NEWS.md : "Default to the SQLite vector store" (read 20261102 20:19 UTC)
13. https://github.com/vitali87/code-graph-rag/blob/main/pyproject.toml : version 0.4.25, licence MIT, SQLite vector store as default (read 20261102 20:19 UTC; the version line re-read 20261102 23:11 UTC)

Papers: none cited; no paper was found for this project in the sources read. Papers on the trend: [code-knowledge-graphs group](../papers/code-knowledge-graphs.md). Long evidence: [archive entry](../../kb-kg/projects/code-graph-rag.md).
