---
type: index
kind: system
aliases: [grep utility, GNU grep, g/re/p]
updated: 20261102 22:57 UTC
---

# grep

This entry says what grep is, where the command comes from, and how a 1973 tool became the lookup method that studies of coding agents compare indexes against. Similar tools, such as ripgrep, are named only for dates.

## Definition

The POSIX specification (IEEE Std 1003.1-2024, Issue 8) says the grep utility "shall search the input files, selecting lines matching one or more patterns"; by default a pattern is a basic regular expression, and options select extended expressions or fixed strings [1]. The GNU manual adds that when grep finds a match in a line it copies the line to standard output by default [2].

## How it changed

- **About November 1973.** Thompson's grep appears in the Fourth Edition Unix manual, whose files Ritchie dates to around November 1973 [3][4]. McIlroy says it began when Thompson was asked how to search a file too big for the editor, and was named after the `ed` command g/re/p [3]. Era: [Formal foundations](../history/formal-foundations.md).
- **20160914.** ripgrep 0.1.0 is released: a line-oriented tool that searches a directory recursively and, by default, respects gitignore rules (first-party) [5].
- **20250929.** Anthropic writes that Claude Code uses glob and grep to retrieve files "just-in-time, effectively bypassing the issues of stale indexing and complex syntax trees" (first-party) [6]. Still moving: [Agentic search over raw data](../trends/agentic-search.md).
- **20260514.** "Is Grep All You Need?" finds inline grep above inline vector retrieval for every harness-model pair on a 116-question LongMemEval subset, while with file-based tool results vector retrieval is ahead for five of ten pairs; its first author is also cited as author of one of the harnesses, Chronos [7].
- **20260731.** In the third version of a scaling study, a file-system agent with list_dir, a fixed-string grep and read_doc leads at the smallest corpora; BM25 overtakes it near 10 million corpus tokens. The first version, of 20260729, says only that the agent "matches or slightly exceeds BM25" at the smallest tiers [8].

## Where sources disagree

**Is grep enough for an agent?** Anthropic presents grep as a way to skip indexes [6]. Against that, Bellam (single author, 20261025) finds structured tools double grep-only accuracy for two small models on SWE-bench Verified [9]. Codebase-Memory (first-party, 20260328) says agents "typically" explore code by "repeated file-reading and grep-searching" and reports 83% answer quality for its code graph against 92% for a file-exploration agent, at ten times fewer tokens [10]. *Reading:* the studies differ in task, model size and corpus size, so none settles the question alone. See [Code graphs for coding agents](../trends/code-knowledge-graphs.md) and [experiment X4](../experiments/x4-code-graph-vs-grep.md).

## Related

[Information retrieval](./information-retrieval.md), [BM25](./bm25.md), [vector search](./vector-search.md), [inverted index](./inverted-index.md), [agent harness](./agent-harness.md), [agent](./agent.md), [tool use](./tool-use.md), [tree-sitter](./tree-sitter.md). Trends: [agentic search](../trends/agentic-search.md), [code knowledge graphs](../trends/code-knowledge-graphs.md), [plain files](../trends/plain-file-knowledge.md). Papers: [agentic search](../papers/agentic-search.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)
- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)

**Projects**

- [code-review-graph](../projects/code-review-graph.md)

**Papers**

- [Papers: Agentic search over raw data](../papers/agentic-search.md)
- [Papers: Code graphs for coding agents](../papers/code-knowledge-graphs.md)

**Index**

- [Abstract syntax tree](abstract-syntax-tree.md)
- [Agent harness](agent-harness.md)
- [Impact analysis](impact-analysis.md)
- [Language Server Protocol](language-server-protocol.md)
- [Tree-sitter](tree-sitter.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html : The Open Group Base Specifications Issue 8, IEEE Std 1003.1-2024, grep: description, BRE default, -E and -F (read 20261102 22:09 UTC)
2. https://www.gnu.org/software/grep/manual/grep.html : GNU grep manual, section 1 Introduction (read 20261102 22:09 UTC)
3. https://www.cs.dartmouth.edu/~doug/reader.pdf : McIlroy, "A Research UNIX Reader: Annotated Excerpts from the Programmer's Manual, 1971-1986": entry "GREP (v4 page 24)", "Grep (Thompson, v4)" (read 20261102 22:09 UTC)
4. https://www.tuhs.org/Archive/Distributions/Research/Dennis_v4/Readme.v4man : Unix Heritage Society archive, quoting Ritchie: file dates "around Feb 1973 for the 3rd edition, and Nov 1973 for the 4th" (read 20261102 22:10 UTC)
5. https://github.com/BurntSushi/ripgrep : GitHub releases API (0.1.0 published 20160914) and README (first-party; read 20261102 22:11 UTC)
6. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents : Anthropic, "Effective context engineering for AI agents", published 29 September 2025 (first-party; read 20261102 22:09 UTC)
7. https://arxiv.org/abs/2605.15184 : Sen et al., "Is Grep All You Need? How Agent Harnesses Reshape Agentic Search", v1 20260514: abstract; Section 4.1.3 and Table 1 in the full text at https://arxiv.org/html/2605.15184 (inline grep above inline vector in all ten pairs; file-based vector above file-based grep in five) (read 20261102 22:51 UTC)
8. https://arxiv.org/abs/2607.26497v3 : Wang and 7 more, "BM25 Wins at Scale", v1 20260729, v3 20260731: abstract of v3 ("leads at the smallest shared tiers"; "around 10 million corpus tokens, BM25 overtakes it") and of v1 ("matches or slightly exceeds BM25"; no crossover figure); File-System Agent tools in the full text at https://arxiv.org/html/2607.26497v3 (read 20261102 22:51 UTC)
9. https://arxiv.org/abs/2610.33958 : Bellam, "How Do Small Coding Agents Use Code Graphs and Embeddings?", v1 20261025: abstract (read 20261102 22:11 UTC)
10. https://arxiv.org/abs/2603.27277 : Vogel et al., "Codebase-Memory", v1 20260328: abstract (first-party; read 20261102 22:11 UTC)
