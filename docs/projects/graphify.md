---
type: project
repo: Graphify-Labs/graphify
trends: [code-knowledge-graphs, features-in-and-out]
updated: 20261102 23:17 UTC
---

# Graphify

This page answers what Graphify builds from a code base, which parts need a model, what its authors and others have measured, and how the open-source tool relates to the hosted product. The chapter landing's watch-list table carries stars and push dates.

| Field | Value |
|---|---|
| Repository | https://github.com/Graphify-Labs/graphify |
| Licence | Apache-2.0. GitHub classifies the `LICENSE` file as Apache License 2.0. `NOTICE` reads "Copyright 2026 Safi Shamsi and the Graphify contributors" and says earlier contributions made under MIT remain available under MIT (`LICENSE-MIT`) [1][2] |
| Trends | [Code graphs for coding agents](../trends/code-knowledge-graphs.md), [Graph features removed and added](../trends/features-in-and-out.md) |

## What it is

Graphify turns a folder of code, documents, PDFs, images and media into a [knowledge graph](../index/knowledge-graph.md) that an AI coding [agent](../index/agent.md) queries instead of searching files [3]. It installs as a `/graphify` skill for Claude Code, Cursor, Codex, Gemini CLI and 20+ more assistants [3]. The README says "Not a vector index. No embeddings, no vector store" [3]. The same organisation sells Graphify Cloud, a hosted product, and the README opens with it [3]. [Understand-Anything](./understand-anything.md) and [codegraph](./codegraph.md) are on the same trend.

## How it works

Three passes [3][4]:

| Pass | Input | Method | Model? |
|---|---|---|---|
| 1 | source code, about 40 languages (33 tree-sitter grammars and 7 built-in parsers) | parse to classes, functions, imports and calls; SQL tables and joins extracted deterministically | no |
| 2 | video and audio | local transcription with faster-whisper | no |
| 3 | Markdown, PDFs, images, transcripts | subagents return JSON fragments of nodes and edges, merged into one graph | yes |

Code files are not sent to the model in the normal pipeline; a code-only corpus skips pass 3 [4]. Pass 3 runs on the user's own assistant, or on a provider chosen with `graphify extract --backend` [4].

[Community detection](../index/community-detection.md) uses the Leiden algorithm on graph structure; the documentation says there is no separate [embedding](../index/embedding.md) step [4]. Every edge carries a label: `EXTRACTED` (found in the source), `INFERRED` (with a score from 0.55 to 0.95) or `AMBIGUOUS` [4]. The README defines `INFERRED` as "resolved by graphify", not as model-made, so the label does not say whether a model was involved [3].

Output is a `graphify-out/` folder with `graph.json` (NetworkX node-link format), an HTML view and a Markdown report [3][4]. An agent queries it by slash command, by command line, or through a [Model Context Protocol](../index/model-context-protocol.md) server with ten tools: `query_graph`, `get_node`, `get_neighbors`, `get_community`, `god_nodes`, `graph_stats`, `shortest_path`, `list_prs`, `get_pr_impact` and `triage_prs` [8]. The only mention of embeddings in the server source is a comment that an external ranker could supply start nodes [8].

## Evidence

All published results are first-party (the project's own harness); no independent evaluation of the results below was found: **unstated**.

| Suite | n | Graphify | Others, as reported |
|---|---|---|---|
| LOCOMO recall@10 (the share of relevant items in the top ten) | 300 | 0.497 | BM25 (Best Matching 25, a keyword ranking function) 0.362, [mem0](./mem0.md) 0.048 |
| LOCOMO QA (question answering) accuracy | 300 | 45.3% | another memory system (supermemory) 49.7%, BM25 31.3%, mem0 27.3% |
| [LongMemEval](../datasets/longmemeval.md)-S QA accuracy | 50 | 76% | dense RAG (retrieval-augmented generation) 76%, mem0 70% |
| ERPNext key-fact coverage | 6 | 82.0% | grep and read baseline 70.8% |
| INFERRED cross-file edges, FastAPI | 12 | all correct (manual spot-check, 20261005) | none |

Source: `BENCHMARKS.md`, run by the project. In the memory suite every system used one model (Kimi K2.6). In the code suite the agent is a fixed coding agent (Claude Opus 4.8, at most 14 turns). Kimi K2.6 grades both, and the judge was checked against a second judge (90.6% agreement, Cohen's kappa 0.81) [5]. The README now repeats the first four rows [3].

Limits:

- The only code result has six questions [5].
- The header reads "Last updated: 2026-07-05" yet the file holds a check dated 20261005. The ERPNext code result is in the file from its first commit, 20260704 [5][9]. On 20260920 an outside user opened issue 3690: `BENCHMARKS.md` returned 404 on `main`, so the code result could not be reached, and the headline numbers measure conversational memory, not code graphs [9]. The fix of 20261005 (`2ce4a20`, cherry-picked from an outside contributor) added the 12-edge FastAPI spot-check to `BENCHMARKS.md` and the ERPNext row to the README table [5][9].
- The reproduction commands name `memory/` and `crosstool/`; neither is in the `v8` tree [5][6].
- `BENCHMARKS.md` credits "hybrid retrieval" and a shared embedder; the README and the server source describe no embeddings [3][5][8].

**Token claims.** The README banner reads "Cut agent token spend by 80%" and ties it to Graphify Cloud; no baseline or method sits beside it in the README [3]. The commit adding it, 20261010, is titled "cost-led Graphify Cloud headline (80% fewer tokens)" [10]. `docs/how-it-works.md` reports 71.5x fewer tokens per query on a 52-file mixed corpus, 5.4x on a 4-file one and about 1x on a 6-file one, and says savings grow with corpus size [4].

**Third party.** A HackerNoon author (20261021) ran the command line on `httpx` without the skill, semantic pass or Cloud: 2,233 nodes, 4,453 edges, 88% `EXTRACTED`; `explain` on one class cost 628 tokens against 13,659 to read its file. It is one lookup on one repository, and he did not test the 80% claim [11].

## Status and direction

- **Latest release.** v0.9.101, 20261102 19:38 UTC [7]. 69 releases since 20260804 [7].
- **Activity, 20260804 to 20261102.** 1,433 commits on `v8`: 287 in August, 394 in September, 672 in October, 80 in November so far; 786 subjects begin with "fix" in any case (775 in lower case only), counted on 20261102 [6]. The newest changelog sections are extractor fixes for Go, Rust, C++ and Python [12].
- **Licence move.** Relicensed from MIT to Apache-2.0 on 20260722 22:50 UTC; the commit cites a patent grant and says earlier contributions remain under MIT. This page does not assess that claim [2].
- **Hosted tier.** The README's Cloud section lists cross-repo graphs, formal verification, code review and Sentry or Jira connectors as Cloud features [3]. Whether any once shipped in the open-source repository is **unstated**.
- **Roadmap.** No roadmap file in the tree [6].

*Reading:* fast, fix-heavy development of the open-source tool, under a README that leads with the paid product. The benefit over plain search rests so far on one six-question run and one outside lookup.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Code graphs for coding agents: from grep and file reads to parsed code graphs](../trends/code-knowledge-graphs.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [code-review-graph](code-review-graph.md)
- [codebase-memory-mcp](codebase-memory-mcp.md)
- [CodeGraph](codegraph.md)
- [FalkorDB](falkordb.md)
- [Projects](README.md)
- [Understand Anything](understand-anything.md)

**Experiments**

- [X1: Snapshot distributions](../experiments/x1-snapshot-distributions.md)

**Index**

- [Abstract syntax tree](../index/abstract-syntax-tree.md)
- [Code graph](../index/code-graph.md)
- [Community detection](../index/community-detection.md)
- [Hypergraph](../index/hypergraph.md)
- [Tree-sitter](../index/tree-sitter.md)

<!-- END GENERATED: appears-in -->

## Sources

No paper. The papers chapter group page for its main trend is [Code knowledge graph papers](../papers/code-knowledge-graphs.md).

1. https://api.github.com/repos/Graphify-Labs/graphify and `/license` : licence field (Apache-2.0), default branch `v8`, archived flag (false) (read 20261102 20:16 UTC)
2. https://github.com/Graphify-Labs/graphify/blob/v8/NOTICE and commit `ba7f9ea` (and the commit list of `LICENSE`) : copyright line, MIT portions, relicense date and message (read 20261102 20:18 to 20:19 UTC)
3. https://github.com/Graphify-Labs/graphify/blob/v8/README.md : pitch, languages, claims, Cloud section, benchmark table (read 20261102 20:16 UTC; table re-read 20261102 20:38 UTC)
4. https://github.com/Graphify-Labs/graphify/blob/v8/docs/how-it-works.md : three passes, Leiden, confidence labels, 71.5x table (read 20261102 20:19 UTC)
5. https://github.com/Graphify-Labs/graphify/blob/v8/BENCHMARKS.md : harness, models, results, header date, reproduction commands (read 20261102 20:18 UTC; re-read, with the version of `9fea1a4`, 20261102 20:37 UTC)
6. https://api.github.com/repos/Graphify-Labs/graphify/commits?since=20260804 and `/git/trees/v8` : commit counts (recounted 20261102 20:38 UTC), no `memory/` or `crosstool/`, no roadmap file (read 20261102 20:17 and 20:18 UTC)
7. https://api.github.com/repos/Graphify-Labs/graphify/releases : latest v0.9.101, 69 releases since 20260804 (read 20261102 20:17 UTC; re-read 20261102 22:54 UTC with the same result: latest v0.9.101 of 20261102 19:38 UTC, 69 releases since 20260804)
8. https://github.com/Graphify-Labs/graphify/blob/v8/graphify/serve.py : ten MCP tools; embeddings appear only in a comment (read 20261102 20:19 UTC)
9. https://github.com/Graphify-Labs/graphify/issues/3690, the commit list of `BENCHMARKS.md` and commits `9fea1a4` (20260704) and `2ce4a20` (20261005) : issue text and date; ERPNext result present in the first version; what the fix added (read 20261102 20:37 to 20:38 UTC)
10. https://github.com/Graphify-Labs/graphify/commit/01d23d06 : commit title and date of the 80% headline (read 20261102 20:19 UTC)
11. https://hackernoon.com/i-tested-graphify-on-a-real-python-repo-heres-what-happened : third-party test (read 20261102 20:20 UTC)
12. https://github.com/Graphify-Labs/graphify/blob/v8/CHANGELOG.md : sections 0.9.99 to 0.9.101 (read 20261102 20:18 UTC)
