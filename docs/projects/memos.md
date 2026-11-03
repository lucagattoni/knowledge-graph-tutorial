---
type: project
repo: MemTensor/MemOS
trends: [agent-memory]
updated: 20261102 23:17 UTC
---

# MemOS

This page answers what MemOS is, how its server and its local plugin store and retrieve memory, and who has measured it. The main point for a reader: the headline benchmark scores come from an evaluation framework run by the project's own organisation, on its hosted service [3][8][9].

| Field | Value |
|---|---|
| Repository | https://github.com/MemTensor/MemOS [1] |
| Licence | Apache-2.0. GitHub classifies the `LICENSE` file as Apache-2.0. The file is the standard Apache License 2.0 text; the only difference found against the text at apache.org is the appendix line, "Copyright 2025 - Present MemTensor Research". The README says Apache 2.0 too [2][3]. |
| Trends | [Agent memory](../trends/agent-memory.md) |

## What it is

MemOS ("Memory Operating System") is a memory layer for [LLM](../index/large-language-model.md) (large language model) agents: one API to add, retrieve, edit and delete long-term memory, structured as a graph, with multi-modal memory, separate knowledge bases called memory cubes, an asynchronous scheduler and natural-language feedback to correct memories [3]. The paper that names it proposes the MemCube, one unit holding content and metadata such as provenance and versioning, for plaintext, activation and parameter memory [6]. An earlier paper (20250528) has a different title and abstract [7]. Neither abstract reports a score [6][7].

One repository now holds several products: a Python service, offered as a hosted Cloud API or self-hosted, and plugins for OpenClaw, Hermes Agent and DeepSeek Harness, in cloud and local forms [3][10]. It is [agent memory](../index/agent-memory.md): a store outside the model that persists across sessions. Neighbours with a page: [Mem0](./mem0.md), [Letta](./letta.md), [Hindsight](./hindsight.md), [Cognee](./cognee.md), [Graphiti](./graphiti.md).

## How it works

**Server.** Self-hosting runs `docker compose`, which starts the API with [Neo4j](./neo4j.md) as graph store and [Qdrant](https://github.com/qdrant/qdrant) for vectors [3]. A client creates a cube, adds messages to writable cubes (sync or async) and searches readable ones [3]. The source tree names modules for a memory reader, scheduler, feedback and rerankers. Graph backends are Neo4j, Neo4j community, PolarDB and Postgres; vector backends are Milvus and Qdrant; memory types are textual, activation and parametric. I read names only, not code [11]. Which calls run at write and at query time: **unstated**.

**Dream.** An optional beta plugin, off by default. It captures signals from added memories, builds "Context" nodes, asks the configured model for at most one insight per motive and writes a diary entry, all outside the request path [12].

**Local plugin.** Memory is kept in four layers in SQLite: L1 step traces (action, observation, reflection, value), L2 policies induced across traces, L3 world models, and callable skills. A retriever tries skills first, then traces, then world models. Reward flows back along traces from step-level and task-level feedback [10]. A viewer listens on `127.0.0.1:18801` by default [10].

## Evidence

Every score is a published figure. None was reproduced here.

**First-party, README (20261102).** A table lists MemOS at [LoCoMo](../datasets/locomo.md) 88.83, [LongMemEval](../datasets/longmemeval.md) 89.20, and eight more scores [3]. The README news also says OpenClaw with MemOS rose from 36.63% to 50.87% average task completion over five agent tasks, and that OmniMemEval is "a unified evaluation of 14 commercial memory products across ten datasets" [3]. All are the project's own claims. The README's 88.83 equals the OmniMemEval LoCoMo figure below; the README does not say how the score was produced [3][9].

**First-party, evaluation framework.** OmniMemEval belongs to the same GitHub organisation and is Apache-2.0 [8]. Its results page states one harness for all backends: answer model `gpt-4.1-mini-2025-04-14`, judge `gpt-4o-mini-2024-07-18`, LLM-as-a-judge accuracy for LoCoMo and LongMemEval. It says the adapters follow each product's public documentation and are not claimed to be optimal [9].

| System | LoCoMo | LongMemEval | Run on (LoCoMo / LongMemEval) |
|---|---|---|---|
| MemOS | 88.83 | 89.20 | cloud / cloud |
| Cognee | 83.48 | 51.80 | cloud / self-hosted |
| Hindsight | 81.99 | 72.20 | cloud / self-hosted |
| Mem0 | 77.68 | 56.00 | cloud / cloud |
| Letta | 77.12 | 77.67 | cloud / cloud |
| Zep / Graphiti | 63.83 | 79.80 | cloud / self-hosted |

Source for the table: [9]. Selected rows: the systems that have a page in this documentation. The LoCoMo table in the file lists 15 backends and the LongMemEval table 13 [9]. Both MemOS runs used the hosted service, not the self-hosted server [9]. The LoCoMo set excludes category 5 (adversarial questions) and covers 1,540 questions [9]. On LoCoMo the file reports 5,400 average answer-stage context tokens for MemOS against 17,395 for Mem0 and 24,683 for Hindsight [9]. A contributor row (LCM-X, run by its own maintainers) reaches 87.00 on LongMemEval [9]. The file also lists published reference scores on LoCoMo that are higher than MemOS's 88.83: Mem0 92.5 and Zep 94.7. It says such scores may use different models, prompts and settings, so they are not directly comparable to the reproduced ones [9].

*Reading:* MemOS leads the reproduced LoCoMo and LongMemEval tables of its own league table, with rivals configured by its authors. The self-hosted server is not the measured system. On the published reference scores the order differs for LoCoMo, but those come from other harnesses. An independent run is **not found** in the sources read.

## Status and direction

*Release.* GitHub's latest is `v2.0.34`, 20260923 05:24 UTC, with a one-line note. Plugin tags are newer: `memos-local-plugin-v2.0.21`, 20261029 [4].

*Activity in the last 90 days.* 203 commits to the default branch, 20260804 to 20261102: 152 in August, 36 in September, 13 in October, 2 in November (computed). The last two only edit a README badge; the last code change is 20261029 [5]. By prefix, 99 are `fix` and 9 `feat`; 82 subjects name the plugin or its viewer (computed) [5]. The repository is not archived [1].

*Direction.* *Reading:* work appears to have moved to the plugins. The newest releases are plugin tags, and the Python server's last tag is 36 days older than the plugin's [4][5]. This is an inference from tags and commit subjects, not a statement by the project. The README promotes the Cloud API and two plugin routes [3]. Whether features moved to the hosted tier: **unstated**. Roadmap: **unstated**.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Claude-Mem](claude-mem.md)
- [EverOS](everos.md)
- [Memori](memori.md)
- [Projects](README.md)

**Benchmarks**

- [LongMemEval](../benchmarks/longmemeval.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/MemTensor/MemOS (via `gh api`) : repository metadata, archived flag, default branch (read 20261102 20:16 UTC)
2. `gh api repos/MemTensor/MemOS/license`, https://github.com/MemTensor/MemOS/blob/main/LICENSE and https://www.apache.org/licenses/LICENSE-2.0.txt : classification, file text, word-level comparison (read 20261102 20:16 and 20:19 UTC)
3. https://github.com/MemTensor/MemOS/blob/main/README.md (via `gh api repos/MemTensor/MemOS/readme`) : description, news, score table, entry points, licence line (read 20261102 20:16 UTC); score lines and the OmniMemEval sentence (re-read 20261102 20:38 UTC)
4. `gh api repos/MemTensor/MemOS/releases/latest` and the releases list : v2.0.34 and plugin tags (read 20261102 20:16 UTC)
5. `gh api repos/MemTensor/MemOS/commits?since=2026-08-04` (paged, 203 commits) : counts, prefixes, subjects (read 20261102 20:16 UTC)
6. https://arxiv.org/abs/2507.03724 : Li et al., "MemOS: A Memory OS for AI System", v1 20250704, v4 20251203, abstract (read 20261102 20:17 UTC)
7. https://arxiv.org/abs/2505.22101 : Li et al., "MemOS: An Operating System for Memory-Augmented Generation (MAG) in Large Language Models", 20250528, abstract (read 20261102 20:17 UTC)
8. https://github.com/MemTensor/OmniMemEval : README and licence field of the evaluation framework (read 20261102 20:17 UTC)
9. https://github.com/MemTensor/OmniMemEval/blob/main/docs/user_memory/results.md : setup, summary, LoCoMo and LongMemEval tables, category-5 exclusion, published reference scores, backend counts (re-read 20261102 20:36 UTC; all table values quoted on this page match)
10. https://github.com/MemTensor/MemOS/blob/main/apps/memos-local-plugin/README.md : layers, retriever, viewer, config (read 20261102 20:17 UTC)
11. `gh api repos/MemTensor/MemOS/contents/src/memos` and its `graph_dbs`, `vec_dbs` and `memories` folders : module names (read 20261102 20:19 UTC)
12. https://github.com/MemTensor/MemOS/blob/main/src/memos/dream/README.md : Dream plugin (read 20261102 20:20 UTC)

Further reading in the archive: [MemOS, archive entry](../../kb-kg/projects/memos.md). Papers: [agent memory group](../papers/agent-memory.md).
