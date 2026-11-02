---
type: index
kind: system
aliases: [tree sitter, treesitter]
updated: 20261102 22:51 UTC
---

# Tree-sitter

This entry says what Tree-sitter is, what kind of tree it builds, and how code-graph tools came to rely on it. The projects built on it have their own pages.

## Definition

Tree-sitter's documentation calls it "a parser generator tool and an incremental parsing library". It builds a concrete syntax tree for a source file and updates the tree efficiently as the file is edited [1]. It aims to be general enough for any programming language, fast enough to parse on every keystroke, robust to syntax errors, and dependency-free, with a runtime in pure C11 [1]. The code is MIT-licensed, per the LICENSE file [2]. The tree keeps a node for every token; the documentation adds that a distinction between named and anonymous nodes lets the tree work "much like an abstract syntax tree" [3].

## How it changed

- **20131106.** The GitHub repository is created [4]. The LICENSE file's copyright line reads 2018 [2]; why the two years differ is unstated.
- **2017-2018.** The documentation lists three talks: GitHub Universe 2017, FOSDEM 2018 and Strange Loop 2018 [1].
- **20190118.** The earliest entry in GitHub's release list is 0.14.0-beta2; 0.14.0 follows on 20190205 [5].
- **20211209.** GitHub writes that it uses Tree-sitter "in many places across GitHub" and builds its stack graphs, the basis of precise code navigation, on its parsers [6].
- **20231022.** Aider replaces its ctags-based repository map with a tree-sitter one, and notes that many IDEs, editors and LSP servers already use Tree-sitter (first-party) [7]. See [Code graphs for coding agents](../trends/code-knowledge-graphs.md).
- **20260328.** A preprint titled "Codebase-Memory: Tree-Sitter-Based Knowledge Graphs for LLM Code Exploration via MCP" is first submitted [8].
- **20261008.** v0.27.1 is the newest stable release; v0.27.0 was published 20260830. The repository is not archived [4][5].

## Where sources disagree

**The tree's name.** Tree-sitter's documentation says it produces concrete syntax trees [3]; Understand Anything's README repeats "concrete syntax tree" [9]. Graphify's README speaks of "tree-sitter AST" [10], and codebase-memory-mcp's says "Tree-sitter alone gives a syntactic AST" [11]. *Reading:* the tool is the same; "AST" in these READMEs is probably loose usage, since the documentation itself says the tree works much like an abstract syntax tree when anonymous nodes are skipped [3]. Which view each project reads is unstated.

## Related

[Abstract syntax tree](./abstract-syntax-tree.md), [code graph](./code-graph.md), [Language Server Protocol](./language-server-protocol.md), [grep](./grep.md), [impact analysis](./impact-analysis.md), [Model Context Protocol](./model-context-protocol.md). Projects: [codegraph](../projects/codegraph.md), [codebase-memory-mcp](../projects/codebase-memory-mcp.md), [code-review-graph](../projects/code-review-graph.md), [Understand Anything](../projects/understand-anything.md), [Graphify](../projects/graphify.md), [Code-Graph-RAG](../projects/code-graph-rag.md). Trend: [code graphs for coding agents](../trends/code-knowledge-graphs.md). Papers: [code knowledge graphs](../papers/code-knowledge-graphs.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)

**Projects**

- [code-review-graph](../projects/code-review-graph.md)
- [codebase-memory-mcp](../projects/codebase-memory-mcp.md)
- [CodeGraph](../projects/codegraph.md)
- [Projects](../projects/README.md)
- [Understand Anything](../projects/understand-anything.md)

**Papers**

- [Papers: Code graphs for coding agents](../papers/code-knowledge-graphs.md)

**Index**

- [Abstract syntax tree](abstract-syntax-tree.md)
- [grep](grep.md)
- [Impact analysis](impact-analysis.md)
- [Language Server Protocol](language-server-protocol.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://tree-sitter.github.io/tree-sitter/ : Tree-sitter documentation, Introduction: definition, aims, runtime in pure C11, list of talks (first-party; read 20261102 22:06 UTC)
2. https://github.com/tree-sitter/tree-sitter/blob/master/LICENSE : LICENSE file: MIT License, "Copyright (c) 2018 Max Brunsfeld" (read 20261102 22:09 UTC)
3. https://tree-sitter.github.io/tree-sitter/using-parsers/2-basic-parsing.html : Tree-sitter documentation, "Named vs Anonymous Nodes": concrete syntax trees, named nodes "much like an abstract syntax tree" (first-party; read 20261102 22:16 UTC)
4. https://github.com/tree-sitter/tree-sitter : repository metadata through the GitHub API: created 2013-11-06, not archived (read 20261102 22:09 UTC)
5. https://github.com/tree-sitter/tree-sitter/releases : release list through the GitHub API: 0.14.0-beta2 (2019-01-18), 0.14.0 (2019-02-05), v0.27.0 (2026-08-30), v0.27.1 (2026-10-08) (read 20261102 22:10 UTC)
6. https://github.blog/2021-12-09-introducing-stack-graphs/ : GitHub, "Introducing stack graphs", 9 December 2021 (first-party; read 20261102 22:10 UTC)
7. https://aider.chat/2023/10/22/repomap.html : Aider, "Building a better repository map with tree sitter", 22 October 2023: "replaces the ctags based map that aider originally used" (first-party; read 20261102 22:11 UTC)
8. https://arxiv.org/abs/2603.27277 : Vogel et al., "Codebase-Memory", 5 authors, submitted 28 March 2026, title and date only (first-party; read 20261102 22:11 UTC)
9. https://github.com/Egonex-AI/Understand-Anything : README: Tree-sitter "parses source into a concrete syntax tree" (first-party; read 20261102 22:19 UTC)
10. https://github.com/Graphify-Labs/graphify : README: "parsed with tree-sitter AST" (first-party; read 20261102 22:19 UTC)
11. https://github.com/DeusData/codebase-memory-mcp : README: "Tree-sitter alone gives a syntactic AST" (first-party; read 20261102 22:19 UTC)
