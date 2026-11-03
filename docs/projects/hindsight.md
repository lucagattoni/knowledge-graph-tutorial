---
type: project
repo: vectorize-io/hindsight
trends: [agent-memory]
updated: 20261102 23:17 UTC
---

# Hindsight

This page answers what Hindsight is, how it stores and retrieves memory, and who has measured it. It also separates the project's own claims from independent evidence, because its paper shares authors with the groups said to have reproduced its results [5][6].

| Field | Value |
|---|---|
| Repository | https://github.com/vectorize-io/hindsight [1] |
| Licence | MIT. GitHub classifies the `LICENSE` file as MIT, "Copyright (c) 2025 Vectorize AI, Inc." [2]; the README agrees [3]. |
| Trends | [Agent memory](../trends/agent-memory.md) |

## What it is

Hindsight is an [agent memory](../index/agent-memory.md) system from Vectorize.io. Its README says it is "focused on making agents that learn, not just remember" [3]. Memories live in isolated *banks* and are reached through three operations: retain, recall and reflect [3]. It ships as a server with Python, Node and Go clients, a CLI (command-line interface), and an [MCP](../index/model-context-protocol.md) (Model Context Protocol) endpoint for each bank [3]. A hosted Hindsight Cloud and an enterprise tier exist beside the open-source code [3][7].

## How it works

**Memory types.** The README names four: world facts, the agent's own experiences, observations (consolidated, evidence-backed beliefs) and mental models (standing answers refreshed in the background) [3].

**Retain.** A language model extracts facts, times, entities and relationships from the input. They are normalised into canonical entities, time series and search indexes [3].

**Recall.** Four strategies run in parallel: semantic ([vector](../index/vector-search.md)), keyword ([BM25](../index/bm25.md), Best Matching 25, a keyword ranking function), graph (entity, temporal and causal links) and temporal range filtering. The results are merged by [reciprocal rank fusion](../index/reciprocal-rank-fusion.md), [reranked](../index/reranking.md) by a cross-encoder and trimmed to a token limit [3]. The graph is one retrieval path among four, not the whole design; compare [Graphiti](./graphiti.md).

**Reflect and consolidation.** Reflect analyses stored memories more deeply, shaped by per-bank "disposition" traits [3]. In the background, related facts are consolidated into observations, which the README says are "refined rather than overwritten" when new evidence arrives [3]. The 1.1.0 post words it differently: "Observations are rebuilt, not versioned". When a source fact is edited, appended to, re-retained or invalidated, its observations are deleted and rebuilt, and a per-document change history now records each rebuild [8]. How the two descriptions relate is **unstated**.

**Operation.** Storage is PostgreSQL with pgvector, or Oracle AI Database 23ai. The README lists 25+ language-model providers and an opt-in "Memory Defense" policy that scans each retain for secrets and personal data [3].

## Evidence

**First-party, with co-authors elsewhere (paper, arXiv, 20251214).** Authors: three at Vectorize.io, one at The Washington Post, three at Virginia Tech [5][6]. With a 20B open-source model the paper reports 83.6% on [LongMemEval](../datasets/longmemeval.md) against 39.0% for full context on the same model; a larger backbone reaches 91.4% on LongMemEval and up to 89.61% on [LoCoMo](../datasets/locomo.md), against 75.78% for the strongest prior open system [5][6]. "Open" is the paper's qualifier: its Table 4 lists Backboard at a claimed 90.00%, higher than 89.61%, and the text calls the result "effectively matching" it [6]. The baselines were not re-run: the paper says it treats them "as reported reference points rather than our independently reproduced baselines" [6]. The LongMemEval baselines come from Supermemory's technical report (its GPT-4o judge), the LoCoMo ones from Backboard's published results; Hindsight's own runs were judged by GPT-OSS-120B [6]. Different judges and harnesses sit in one table.

**First-party, README and blog.** The README calls Hindsight "the most accurate agent memory system ever tested" and states that its results were "independently reproduced" at Virginia Tech and The Washington Post [3]. Staff of both institutions are co-authors of the paper [6], so "independent" is the project's word. A separate reproduction by third parties: **not located** here. The README's comparison table is dated "as of January 2026" [3]. The 20261013 post claims first place on every dataset of an "Agent Memory Benchmark" [7]; the project's results page repeats it (94.6% LongMemEval-S, 92% LoCoMo-10, 64.1% BEAM 10M) with no date, judge or run settings in its text [13]. The benchmark's own site returned only a title [14]; who runs it is **unstated**.

**Independent.** None found. Bao et al.'s audit of [Mem0](./mem0.md) (20261022) does not name Hindsight (searched) [9].

## Status and direction

*Release.* `v1.1.0`, 20261021 16:41 UTC, is the latest; no later release is listed [4][10].

*Activity in the last 90 days.* 1,684 commits to `main` from 20260804 to 20261102: 413 in August (from the 4th), 586 in September, 676 in October and 9 in November so far. One committer name accounts for 986 (58.5%, computed); the latest commit was 20261102 [11].

*Direction.* The 20261013 post says the open-source project reaches 1.0, with the architecture and API stable: "From here, the API is a promise" [7]. The same post announces Memlake, an object-storage engine that is "part of Hindsight Enterprise", and says most of Hindsight Cloud already runs on it. Open-source Hindsight "stays free, on Postgres" [7]. The file listing shows no Memlake source outside the docs folder, which is a listing, not proof, and its licence is **unstated** [12]. The repository was created 20251030 [1]; the post dates open-sourcing to December 2025 [7]; earlier visibility is **unstated**. No roadmap file appears in the listing [12].

*Reading:* the project is active, releasing nine times in 90 days (gaps of 5 to 20 days, none in the 12 days since the last) [10], with a clear open-source and paid split on storage scale. Its accuracy claims rest on the authors' own runs and others' reported baselines: a lead for a matched-cost comparison, not a verdict.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Claude-Mem](claude-mem.md)
- [MemOS](memos.md)
- [Projects](README.md)

**Datasets**

- [LongMemEval](../datasets/longmemeval.md)

**Benchmarks**

- [LongMemEval](../benchmarks/longmemeval.md)

**Experiments**

- [X1: Snapshot distributions](../experiments/x1-snapshot-distributions.md)

**Index**

- [Agent memory](../index/agent-memory.md)
- [Reciprocal rank fusion](../index/reciprocal-rank-fusion.md)
- [Reranking](../index/reranking.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/vectorize-io/hindsight : repository metadata, archived flag, creation date (read 20261102 20:09 UTC)
2. https://api.github.com/repos/vectorize-io/hindsight/license : MIT text and GitHub's classification (read 20261102 20:09 UTC)
3. https://api.github.com/repos/vectorize-io/hindsight/readme : description, memory types, operations, storage, claims, "as of January 2026" table date, "refined rather than overwritten", licence section (read 20261102 20:32 UTC)
4. https://api.github.com/repos/vectorize-io/hindsight/releases/latest : v1.1.0 and its date (read 20261102 20:34 UTC)
5. https://arxiv.org/abs/2512.12818 : Latimer et al., "Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects", abstract, first version 20251214 (read 20261102 20:12 UTC)
6. https://arxiv.org/html/2512.12818 : author affiliations, Table 3 and Table 4 (Backboard 90.00 row), baseline sources, judge, "effectively matching" sentence (read 20261102 20:32 UTC)
7. https://github.com/vectorize-io/hindsight/blob/main/hindsight-docs/blog/2026-10-13-memlake.md : Hindsight 1.0 and Memlake post, benchmark claim, open-sourcing date (read 20261102 20:33 UTC)
8. https://github.com/vectorize-io/hindsight/blob/main/hindsight-docs/blog/2026-10-21-version-1-1-0.md : 1.1.0 notes, "rebuilt, not versioned", document change history (read 20261102 20:32 UTC)
9. https://arxiv.org/html/2610.30755v1 : Bao et al., searched for "Hindsight", no match (read 20261102 20:12 UTC)
10. https://api.github.com/repos/vectorize-io/hindsight/releases?per_page=10 : release list and dates (read 20261102 20:32 UTC)
11. https://api.github.com/repos/vectorize-io/hindsight/commits?since=2026-08-04 : counts by month and committer; 1,684 commits, paged (read 20261102 20:10 UTC)
12. https://api.github.com/repos/vectorize-io/hindsight/git/trees/main?recursive=1 : file listing (read 20261102 20:13 UTC)
13. https://benchmarks.hindsight.vectorize.io/ : the project's results page, scores for eight datasets (read 20261102 20:32 UTC)
14. https://agentmemorybenchmark.ai/ : fetched without scripts; text was only the title "Agent Memory Benchmark" (read 20261102 20:33 UTC)

Further reading in the archive: [Hindsight entry](../../kb-kg/projects/hindsight.md). Papers: [agent memory group](../papers/agent-memory.md).
