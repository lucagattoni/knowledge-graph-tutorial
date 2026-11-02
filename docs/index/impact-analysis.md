---
type: index
kind: concept
aliases: [change impact analysis, software change impact analysis, blast radius]
updated: 20261102 22:52 UTC
---

# Impact analysis

This entry says what impact analysis means for software, where the term comes from, and how code-graph tools for coding agents now offer it. The sources read give more than one definition, and none settles it.

## Definition

Arnold and Bohner define impact analysis as "the activity of identifying what to modify to accomplish a change, or of identifying the potential consequences of a change" [1]. They list ways to do it, among them cross-reference listings, program slicing and traceability links [1]. Li et al. use the same two halves: identifying the effects of a change, or estimating what must be modified to accomplish it [3]. Tools that keep a [code graph](./code-graph.md) answer the question by walking from a changed symbol to its callers, dependents and tests [6].

## How it changed

- **1980s.** Li et al. say investigations of change impact analysis go back to the 1980s [3].
- **1993.** Arnold and Bohner write that the term "is used with many meanings" and offer a framework to compare approaches; they classify five (1993 Conference on Software Maintenance, Montreal) [1][2].
- **1996.** Bohner and Arnold's volume *Software Change Impact Analysis* appears (IEEE Computer Society Press; catalogue record) [4].
- **20120427.** Li et al. find 30 papers on 23 code-based techniques and call surveys on the topic "very few" (online date; *Software Testing, Verification and Reliability* 23(8)) [3].
- **2021.** Kretsou et al. map 111 studies up to 2019 and report that their number rose substantially after 2009 (*Journal of Systems and Software* 174) [5].
- **As read on 20261102.** Code-graph tools sell it to coding agents. [code-review-graph](../projects/code-review-graph.md) (repository created 20260226) traces "every caller, dependent and test that could be affected" [6]; [CodeGraph](../projects/codegraph.md) has `impact` and `affected` commands [7]; [codebase-memory-mcp](../projects/codebase-memory-mcp.md) has `detect_changes` [8]. All three are first-party. code-review-graph's README calls the 1.0 recall of its own impact test "circular", because the ground truth comes from the same graph [6]; its accuracy figures are on its project page. Still moving: [Code graphs for coding agents](../trends/code-knowledge-graphs.md).

## Where sources disagree

**What the term covers.** Arnold and Bohner offer two readings, what to modify and what the consequences are, and note many meanings [1]. Kretsou et al. cite Bohner (1996) for "undesired consequences" and also write "tentative effects" [5]. The tool READMEs say "blast radius" and "impact" for the same feature [6][7]. No source read settles one definition.

## Related

[Code graph](./code-graph.md), [abstract syntax tree](./abstract-syntax-tree.md), [tree-sitter](./tree-sitter.md), [grep](./grep.md), [Language Server Protocol](./language-server-protocol.md), [Model Context Protocol](./model-context-protocol.md). Projects: [CodeGraph](../projects/codegraph.md), [code-review-graph](../projects/code-review-graph.md), [codebase-memory-mcp](../projects/codebase-memory-mcp.md). Trend and papers: [code graphs for coding agents](../trends/code-knowledge-graphs.md), [papers](../papers/code-knowledge-graphs.md). Experiment: [X4, a code graph against grep](../experiments/x4-code-graph-vs-grep.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)

**Projects**

- [code-review-graph](../projects/code-review-graph.md)
- [codebase-memory-mcp](../projects/codebase-memory-mcp.md)
- [CodeGraph](../projects/codegraph.md)

**Index**

- [Abstract syntax tree](abstract-syntax-tree.md)
- [Language Server Protocol](language-server-protocol.md)
- [Tree-sitter](tree-sitter.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.cs.purdue.edu/homes/xyzhang/spring07/Papers/00366933.pdf : Arnold and Bohner, "Impact Analysis - Towards A Framework for Comparison", 1993 IEEE copyright line: abstract ("used with many meanings"), section 2.1 definition and examples (read 20261102 22:09 UTC)
2. https://api.crossref.org/works/10.1109/ICSM.1993.366933 : bibliographic record: 1993 Conference on Software Maintenance, Montreal, pages 292-301, authors Arnold and Bohner (read 20261102 22:10 UTC)
3. https://api.crossref.org/works?query.bibliographic=A+survey+of+code-based+change+impact+analysis+techniques : record and abstract of Li, Sun, Leung and Zhang, *Software Testing, Verification and Reliability* 23(8), DOI 10.1002/stvr.1475, issued 20120427: 30 papers, 23 techniques, "Since the 1980s" (read 20261102 22:11 UTC)
4. https://openlibrary.org/search.json?q=software+change+impact+analysis+bohner : catalogue record, first publication 1996, IEEE Computer Society Press; a catalogue, not the book (read 20261102 22:11 UTC)
5. https://sites.uom.gr/a.ampatzoglou/public_html/papers/kretsou2021jss.pdf : Kretsou et al., "Change impact analysis: A systematic mapping study", abstract, introduction, Table 1 and the results on primary studies (111 studies, until 2019); journal data from https://api.crossref.org/works?query.bibliographic=Change+Impact+Analysis+A+Systematic+Mapping+Study+Kretsou : JSS 174, April 2021, DOI 10.1016/j.jss.2020.110892 (read 20261102 22:10 UTC)
6. https://github.com/tirth8205/code-review-graph/blob/main/README.md : blast-radius analysis, limitations ("circular", ground truth from the same graph); repository creation date 20260226 from the repository API (first-party; read 20261102 22:11 UTC and 22:40 UTC)
7. https://github.com/colbymchenry/codegraph/blob/main/README.md : features table "Impact Analysis"; `codegraph impact` and `codegraph affected` commands (first-party; read 20261102 22:11 UTC)
8. https://github.com/DeusData/codebase-memory-mcp/blob/main/README.md : `detect_changes` maps uncommitted changes to affected symbols with risk classification (first-party; read 20261102 22:11 UTC)
