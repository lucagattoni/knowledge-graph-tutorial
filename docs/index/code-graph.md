---
type: index
kind: concept
aliases: [code knowledge graph, repository graph]
updated: 20261102 21:21 UTC
---

# Code graph

## Definition

A code graph is a graph built from a code base in which nodes stand for parts of the code and edges for relations between them, such as calls, containment or dependence, so that a tool can answer structural questions by walking the graph. No source read gives one definition; the term covers several designs (see below). Ferrante and colleagues present an early one, the program dependence graph, an intermediate program representation that "makes explicit both the data and control dependences" of each operation [1]. Yamaguchi and colleagues' code property graph merges abstract syntax trees, control flow graphs and program dependence graphs into one data structure [2].

## How it changed

- 198707: the program dependence graph is published (ACM TOPLAS 9(3)) [1].
- 201405: the code property graph is stored in a graph database and used to find 18 previously unknown vulnerabilities in the Linux kernel, per its authors [2].
- 20240807: CodexGraph (first version) lets a model agent write queries against a graph database extracted from a repository, arguing that similarity retrieval "often has low recall in complex tasks" [3].
- 20241003: RepoGraph (first version) adds a repository-level graph as a plug-in module and reports gains on SWE-bench [4].
- 20260113 and 20260328: a study compares syntax-tree graphs with model-extracted ones [5]; Codebase-Memory serves a tree-sitter graph over the [Model Context Protocol](./model-context-protocol.md) and reports 83% answer quality against 92% for file exploration, at ten times fewer tokens (its own authors) [6].

No era page covers this line, and it is still moving: see the trend [Code graphs for coding agents](../trends/code-knowledge-graphs.md).

## Where sources disagree

The unit of a node differs. RepoGraph uses each line of code as a node, labelled definition or reference [7]. CodexGraph uses symbols: module, class, method, function, field and global variable [8]. The code property graph merges three program-analysis graphs [2].

How to build it is also disputed. One single-author study of three Java code bases reports that a deterministic syntax-tree graph is more reliable and far cheaper to index than a model-extracted one [5]. Whether any code graph beats plain file search is open: Codebase-Memory's own figures show lower answer quality for the graph [6].

## Related

[knowledge graph](./knowledge-graph.md) · [property graph](./property-graph.md) · [Cypher](./cypher.md) · [agent](./agent.md) · [community detection](./community-detection.md) · [trend](../trends/code-knowledge-graphs.md) · [papers](../papers/code-knowledge-graphs.md) · [Graphify](../projects/graphify.md) · [CodeGraph](../projects/codegraph.md) · [codebase-memory-mcp](../projects/codebase-memory-mcp.md) · [Code-Graph-RAG](../projects/code-graph-rag.md) · [code-review-graph](../projects/code-review-graph.md) · [Understand Anything](../projects/understand-anything.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)

**Projects**

- [code-review-graph](../projects/code-review-graph.md)
- [codebase-memory-mcp](../projects/codebase-memory-mcp.md)
- [CodeGraph](../projects/codegraph.md)
- [TencentDB Agent Memory](../projects/tencentdb-agent-memory.md)

**Papers**

- [Papers: Code graphs for coding agents](../papers/code-knowledge-graphs.md)

**Experiments**

- [Experiments evidence: status log](../experiments/evidence/status.md)
- [Instruments](../experiments/instruments.md)
- [X4: a code graph against grep](../experiments/x4-code-graph-vs-grep.md)

**Index**

- [Abstract syntax tree](abstract-syntax-tree.md)
- [Community detection](community-detection.md)
- [Impact analysis](impact-analysis.md)
- [Language Server Protocol](language-server-protocol.md)
- [Tree-sitter](tree-sitter.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.crossref.org/works/10.1145/24039.24041 : Ferrante, Ottenstein, Warren, "The program dependence graph and its use in optimization", ACM TOPLAS 9(3), July 1987, abstract (read 20261102 20:48 UTC)
2. https://www.ieee-security.org/TC/SP2014/papers/ModelingandDiscoveringVulnerabilitieswithCodePropertyGraphs.pdf : Yamaguchi, Golde, Arp, Rieck, IEEE Symposium on Security and Privacy 2014 (Crossref date 201405, read 20261102 20:48 UTC), abstract: merged representation, graph database, 18 vulnerabilities (read 20261102 20:49 UTC)
3. https://arxiv.org/abs/2408.03910 : CodexGraph, Liu and seven co-authors, v1 20240807, abstract (read 20261102 20:45 UTC)
4. https://arxiv.org/abs/2410.14684 : RepoGraph, Ouyang and eight co-authors, v1 20241003, abstract (read 20261102 20:45 UTC)
5. https://arxiv.org/abs/2601.08773 : Chinthareddy (one author), "Reliable Graph-RAG for Codebases: AST-Derived Graphs vs LLM-Extracted Knowledge Graphs", v1 20260113, abstract (read 20261102 20:45 UTC)
6. https://arxiv.org/abs/2603.27277 : Codebase-Memory, Vogel and four co-authors, v1 20260328, abstract: 66 languages, 31 repositories, 83% against 92%, ten times fewer tokens (read 20261102 20:45 UTC)
7. https://arxiv.org/html/2410.14684 : RepoGraph section 3.1, "each node is a code line" (read 20261102 20:49 UTC, via a fetch-tool extraction)
8. https://arxiv.org/html/2408.03910 : CodexGraph section 3.1, schema node types MODULE, CLASS, METHOD, FUNCTION, FIELD, GLOBAL_VARIABLE (read 20261102 20:49 UTC, via a fetch-tool extraction)
