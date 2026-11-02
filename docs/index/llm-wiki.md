---
type: index
kind: concept
aliases: [LLM-compiled wiki, LLM wiki pattern]
updated: 20261102 21:30 UTC
---

# LLM wiki

This entry says what an LLM wiki is, when the idea was published, and what the first studies found. The idea is still moving, so the full story is on the trend page.

## Definition

An LLM wiki is a set of linked Markdown pages that a language model writes and keeps current as new source documents are added; the model reads the sources and never edits them. The gist that named it, "LLM Wiki", says the model "incrementally builds and maintains a persistent wiki", so that knowledge is "compiled once and then kept current" instead of re-derived at each question [1]. It has three layers (immutable raw sources, the wiki, and a schema file such as `CLAUDE.md`), three operations (ingest, query, lint) and two files: `index.md`, a catalogue read first, and `log.md`, an append-only record [1]. The gist calls itself "an idea file" and "intentionally abstract": a pattern, not a specification [1].

## How it changed

- **20260404 16:25 UTC.** The gist is created, with one commit [1][2].
- **20260413.** Two papers discuss wiki-style knowledge systems. Miteski writes that "a visible cluster of personal wiki-style memory architectures emerged in April 2026" [3]. Wen and Ku report, for one system and four sequential queries, 47K tokens against 305K for a matched RAG baseline; the abstract of v1 (20260413) and of v2 (20260415) gives the same figures [4].
- **20260518 (v1).** Cochran's preregistered comparison (13 questions, 24 papers, a wiki browsed by a tool-using agent) finds the wiki much better at connecting findings across papers. The v1 abstract says the wiki "used far more query tokens than RAG", so it could not recover its build cost [5]. The v3 abstract (20261002) puts the figure at about 21 times more LLM tokens per query, says the wiki was cheaper to build, and says an earlier claim-level citation advantage for the wiki does not hold once a scoring error is corrected [5].
- **20260729.** Zhou et al. study filesystem memory, a directory tree of Markdown files kept by the agent, a neighbouring medium [6].

All of this is under eight months old and not settled. See [plain files as agent knowledge](../trends/plain-file-knowledge.md).

## Where sources disagree

Cost. The gist says compiling once avoids re-deriving at every question [1]. Wen and Ku report 84.6% lower cumulative token use over four queries [4]. Cochran finds the wiki cheaper to build but, in v3, about 21 times dearer per query, with no break-even point [5]. Scale: the gist says the index works at "~100 sources, ~hundreds of pages" and that a growing wiki needs "proper search", with no threshold [1].

*Reading:* the set-ups differ and both samples are small (four queries on one system; 13 questions over 24 papers), so the two results do not settle the cost question.

## Related

- Entries: [retrieval-augmented generation](./retrieval-augmented-generation.md), [agent memory](./agent-memory.md), [large language model](./large-language-model.md), [knowledge base](./knowledge-base.md), [hybrid search](./hybrid-search.md).
- Projects: [llm-wiki-nashsu](../projects/llm-wiki-nashsu.md), [claude-obsidian](../projects/claude-obsidian.md), [Basic Memory](../projects/basic-memory.md), [Tigerless agent-memory](../projects/tigerless-agent-memory.md), [OpenViking](../projects/openviking.md).
- Trend, papers, experiment: [plain files as agent knowledge](../trends/plain-file-knowledge.md), [papers](../papers/plain-file-knowledge.md), [wiki size limit](../experiments/x5-wiki-size-limit.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)

**Projects**

- [claude-obsidian](../projects/claude-obsidian.md)

**Experiments**

- [Experiments](../experiments/README.md)
- [X5: Wiki size limit](../experiments/x5-wiki-size-limit.md)

**Index**

- [AGENTS.md](agents-md.md)
- [Knowledge compilation](knowledge-compilation.md)

<!-- END GENERATED: appears-in -->

## Sources

Read times are UTC.

1. https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw : the gist's full text: idea, layers, immutability of raw sources, operations, index and log, scale remarks (read 20261102 20:45 and 21:23)
2. https://api.github.com/gists/442a6bf555914893e9891c11519de94f/commits : one commit, committed_at 2026-04-04T16:25:13Z (read 20261102 20:51)
3. https://arxiv.org/abs/2604.12034 : Miteski, "Memory as Metabolism", v1 20260413, abstract (read 20261102 20:45)
4. https://arxiv.org/abs/2604.11243 : Wen and Ku, "Knowledge Compounding", v1 20260413, v2 20260415; abstracts of v1 (https://arxiv.org/abs/2604.11243v1) and v2 give the same figures; first-party results of a small experiment (read 20261102 20:45 and 21:23)
5. https://arxiv.org/abs/2605.18490 : Cochran, "Single-Round Vector RAG vs an LLM-Compiled Wiki" (the title of v3; v1 was titled "Vector RAG vs LLM-Compiled Wiki"), v1 20260518, v2 20260816, v3 20261002; abstract of v1 (https://arxiv.org/abs/2605.18490v1) and of v3, including the v3 comments on the corrected citation analysis (read 20261102 20:53 and 21:23)
6. https://arxiv.org/abs/2607.26637 : Zhou et al., "Filesystem-Based Memory for LLM Agents", v1 20260729, abstract (read 20261102 20:53)
