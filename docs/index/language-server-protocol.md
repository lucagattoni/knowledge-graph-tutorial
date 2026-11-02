---
type: index
kind: standard
aliases: [LSP, language server]
updated: 20261102 22:53 UTC
---

# Language Server Protocol

This entry says what the Language Server Protocol is, how its versions changed, and why the name turns up in tools for coding agents. One such tool uses the protocol; another uses the name for something that is not the protocol.

## Definition

The Language Server Protocol (LSP) is the protocol between an editor or IDE and a language server, a separate process that supplies language features such as completion, go to definition and find all references [1][2]. One server can then serve many tools, and each tool can support many languages with little work [1]. Tool and server exchange JSON-RPC messages and announce what they support as "capabilities" [2]. The messages carry document URIs and text positions, not syntax trees or compiler symbols, which the overview says simplifies the protocol significantly [2]. The specification is hosted on a Microsoft site (copyright 2026 Microsoft) and takes edits by pull request [3].

## How it changed

- **20160627.** The VS Code team announces, with Red Hat and Codenvy, that the protocol "is now being adopted by tool creators and language providers across the industry", and puts the specification in a public GitHub repository (first-party) [4].
- **Version 3.0, undated.** The oldest change-log entry adds client feature flags and the registering of capabilities after start-up [3]. The first dated entry is 3.1.0, 28 February 2017 [3].
- **20201214 (3.16).** Semantic tokens and call hierarchy [3].
- **20220510 (3.17).** Type hierarchies, inlay hints, notebook documents, pull diagnostics, and a machine-readable meta model [3].
- **20260604 (3.18).** Inline completions, snippets in workspace edits and dynamic text document content [3]. The home page names 3.18 the latest version [1].
- **20261102 (read date; the page is undated).** Claude Code's tool reference lists an LSP tool that gives "code intelligence from a running language server"; it stays inactive until a code intelligence plugin is installed (first-party) [5]. See [Code graphs for coding agents](../trends/code-knowledge-graphs.md).
- **20261102 (read date).** The [codebase-memory-mcp](../projects/codebase-memory-mcp.md) README calls one layer "Hybrid LSP" but describes a C implementation of type-resolution algorithms with "No language server process": the name does not mean the protocol (first-party) [6].

Dates of versions before 3.1.0 are **unstated** in the sources read. The change log writes dates as month/day/year; an entry such as 12/14/2020 shows it [3].

## Where sources disagree

No disagreement found in the sources read.

## Related

- Entries: [URI](./uri.md), [abstract syntax tree](./abstract-syntax-tree.md), [tree-sitter](./tree-sitter.md), [code graph](./code-graph.md), [impact analysis](./impact-analysis.md), [grep](./grep.md), [Model Context Protocol](./model-context-protocol.md).
- Trend: [Code graphs for coding agents](../trends/code-knowledge-graphs.md). Project: [codebase-memory-mcp](../projects/codebase-memory-mcp.md). Experiment: [a code graph against grep](../experiments/x4-code-graph-vs-grep.md), which used the Go language server `gopls` as one method.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Projects**

- [codebase-memory-mcp](../projects/codebase-memory-mcp.md)

**Index**

- [Abstract syntax tree](abstract-syntax-tree.md)
- [Impact analysis](impact-analysis.md)
- [Tree-sitter](tree-sitter.md)

<!-- END GENERATED: appears-in -->

## Sources

Read times are UTC.

1. https://microsoft.github.io/language-server-protocol/ : official page: what LSP is, "latest version of the LSP specification is version 3.18" (first-party; read 20261102 22:06 UTC)
2. https://microsoft.github.io/language-server-protocol/overviews/lsp/overview/ : overview: separate process, JSON-RPC, capabilities, URIs and positions instead of syntax trees (first-party; read 20261102 22:06 UTC)
3. https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/ : specification 3.18.x: change log (3.0 to 3.18.0 with dates), meta model since 3.17, pull-request edits, copyright line (first-party; read 20261102 22:07 UTC)
4. https://code.visualstudio.com/blogs/2016/06/27/common-language-protocol : "A Common Protocol for Languages", VS Code team, 27 June 2016 (first-party; read 20261102 22:07 UTC)
5. https://code.claude.com/docs/en/tools-reference : Claude Code tool reference, section "LSP tool behavior" (first-party; undated page; read 20261102 22:08 UTC)
6. https://github.com/DeusData/codebase-memory-mcp : repository README, section "Hybrid LSP", read through the GitHub API (first-party; read 20261102 22:08 UTC)
