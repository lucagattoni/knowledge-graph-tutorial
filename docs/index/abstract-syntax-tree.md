---
type: index
kind: concept
aliases: [AST]
updated: 20261102 22:49 UTC
---

# Abstract syntax tree

This entry says what an abstract syntax tree is, how it differs from the tree a parser first produces, and why code-graph tools start from it. Where the word "abstract" stops being accurate is under "Where sources disagree".

## Definition

Yamaguchi and colleagues write that abstract syntax trees are "usually among the first intermediate representations produced by code parsers of compilers" [1]. They are ordered trees: inner nodes stand for operators, leaves for operands, and nesting shows how statements and expressions combine [1]. Unlike a parse tree, they "no longer represent the concrete syntax chosen to express the program", so a comma-separated list of declarations and two consecutive declarations can give the same tree [1]. They do not make control flow or data dependence explicit [1]. Python's documentation gives a concrete case: its `ast` module processes trees of "the Python abstract syntax grammar", which "might change with each Python release" [3].

## How it changed

- **1962.** McCarthy's "Towards a Mathematical Science of Computation" was given at IFIP-62 [4]. The copy read, typeset in 1996, has a section on abstract syntax: a syntax that tells how to take a program apart and is "independent of the notation used to represent, say sums" [5]. Whether the 1962 print has that section: unstated. Era: [The advent](../history/advent.md).
- **20060919.** Python 2.5 builds an abstract syntax tree from the parse tree and generates bytecode by walking the AST [6]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **20081001.** Python 2.6 adds the `ast` module, whose `parse()` returns an AST [7].
- **2014 (May).** The code property graph merges abstract syntax trees, control flow graphs and program dependence graphs in one structure [1][2]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **20260113.** A single-author study compares a model-written graph with an "AST-derived" graph built with Tree-sitter, on Java code [8]. On 20260328 the paper on [Codebase-Memory](../projects/codebase-memory-mcp.md) describes a Tree-sitter-based graph that parses 66 languages in the version it covers (first-party; later figures are on the project page) [9]. Still moving: [Code graphs for coding agents](../trends/code-knowledge-graphs.md).

## Where sources disagree

**Concrete or abstract.** Tree-sitter's documentation says it "produces concrete syntax trees", with a node for every token, commas and parentheses included; only its named-node view "functions much like an abstract syntax tree" [10]. The 2026 study nevertheless calls the Tree-sitter graph "AST-derived" [8]. *Reading:* the word is used here for output that its own parser's documentation calls concrete.

## Related

[Tree-sitter](./tree-sitter.md) · [code graph](./code-graph.md) · [impact analysis](./impact-analysis.md) · [Language Server Protocol](./language-server-protocol.md) · [grep](./grep.md) · [trend](../trends/code-knowledge-graphs.md) · [papers](../papers/code-knowledge-graphs.md) · [experiment X4](../experiments/x4-code-graph-vs-grep.md) · [CodeGraph](../projects/codegraph.md) · [codebase-memory-mcp](../projects/codebase-memory-mcp.md) · [Code-Graph-RAG](../projects/code-graph-rag.md) · [Graphify](../projects/graphify.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)

**Index**

- [Impact analysis](impact-analysis.md)
- [Language Server Protocol](language-server-protocol.md)
- [Tree-sitter](tree-sitter.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.ieee-security.org/TC/SP2014/papers/ModelingandDiscoveringVulnerabilitieswithCodePropertyGraphs.pdf : Yamaguchi, Golde, Arp, Rieck, "Modeling and Discovering Vulnerabilities with Code Property Graphs": abstract and section "Abstract Syntax Trees" (read 20261102 22:10 UTC)
2. https://api.crossref.org/works/10.1109/SP.2014.44 : same paper, 2014 IEEE Symposium on Security and Privacy, issued 2014-05 (read 20261102 22:14 UTC)
3. https://docs.python.org/3/library/ast.html : Python documentation, "ast: Abstract syntax trees", opening paragraphs (read 20261102 22:08 UTC)
4. http://jmc.stanford.edu/articles/index.html : McCarthy's article list: "Towards a Mathematical Science of Computation" given at IFIP-62 (read 20261102 22:09 UTC)
5. http://www-formal.stanford.edu/jmc/towards.pdf : McCarthy, section 12 "Abstract Syntax of Programming Languages"; the file is dated 1996 (read 20261102 22:09 UTC)
6. https://docs.python.org/3/whatsnew/2.5.html : What's New in Python 2.5: released 19 September 2006; compiler now walks an AST (read 20261102 22:08 UTC)
7. https://docs.python.org/3/whatsnew/2.6.html : What's New in Python 2.6: released 1 October 2008; the `ast` module (read 20261102 22:08 UTC)
8. https://arxiv.org/abs/2601.08773 : Chinthareddy, "Reliable Graph-RAG for Codebases: AST-Derived Graphs vs LLM-Extracted Knowledge Graphs", submitted 13 January 2026, abstract (read 20261102 22:10 UTC)
9. https://arxiv.org/abs/2603.27277 : Vogel and four co-authors, "Codebase-Memory", submitted 28 March 2026, abstract (first-party; read 20261102 22:10 UTC)
10. https://tree-sitter.github.io/tree-sitter/using-parsers/2-basic-parsing.html : Tree-sitter documentation, "Named vs Anonymous Nodes" (read 20261102 22:08 UTC)
