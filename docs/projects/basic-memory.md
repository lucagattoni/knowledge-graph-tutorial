---
type: project
repo: basicmachines-co/basic-memory
trends: [plain-file-knowledge]
updated: 20261102 23:17 UTC
---

# Basic Memory

This page answers what Basic Memory is, how it keeps Markdown notes and a database index in step, and what has been measured. It also records its licence and hosted product, which bear on whether it is a plain-files tool or a service with open code. Every score here is the maintainers' own.

| Field | Value |
|---|---|
| Repository | https://github.com/basicmachines-co/basic-memory [1] |
| Licence | AGPL-3.0. GitHub classifies the `LICENSE` file as AGPL-3.0, and the file begins "GNU AFFERO GENERAL PUBLIC LICENSE Version 3, 19 November 2007" [2]. `pyproject.toml` declares `AGPL-3.0-or-later` and the README says AGPL-3.0 [3][11]. Which of the two applies is a legal question this page does not decide. |
| Trends | [Plain files as agent knowledge](../trends/plain-file-knowledge.md) |

## What it is

Basic Memory is a local-first knowledge store for [LLM](../index/large-language-model.md) (large language model) clients: a folder of Markdown files, a parser, a database index, and an [MCP](../index/model-context-protocol.md) (Model Context Protocol) server with a command-line tool [3][9]. Both a person and the model read and write the notes [3]. The builder is Basic Machines [3]. The local install is free; Basic Memory Cloud is a hosted subscription. The README says (first-party) that Cloud runs "the same OSS engine" (open-source software), with sync, snapshots and a Teams workspace [3].

## How it works

*Files.* A note is Markdown with optional YAML front matter. "Observations" are list items with a bracketed category; "relations" are list items with a relation type before a `[[wiki link]]`. The README calls this "the whole grammar" [3].

*Index.* The parser writes rows to SQLite (default) or Postgres, with full-text search through FTS5 or `tsvector` [8]. The domain model says these rows are projections that "must be rebuildable or reconcilable" from the Markdown [9]. The README says "sync keeps them in step" when a person and the model write to the same files [3]. How sync detects an edit is **unstated** in the sources read.

*Search.* Hybrid search fuses full-text and vector scores as `max(vec, fts) + 0.3 * min(vec, fts)`; vectors default to the local model `BAAI/bge-small-en-v1.5` through FastEmbed [8]. A cross-encoder reranker is off by default [3]. *Reading:* [embeddings](../index/embedding.md) with [hybrid search](../index/hybrid-search.md) are the main difference from [claude-obsidian](../projects/claude-obsidian.md), whose retrieval is BM25 (Best Matching 25, a keyword ranking function) only.

*Tools.* The server exposes twelve `bm_*` tools (read, write, edit, move, delete, search, list, find, project, schema, man, and `bm_context`, which walks the link graph) and an opt-in `bm_project_delete` [6]. Whether the engine itself calls an LLM is **unstated** in the sources read now.

## Evidence

*First-party only.* The repository holds an internal benchmark file, last changed 20260625. It compares Basic Memory with mem0 (run with `infer=false`, without LLM fact extraction), a grep baseline and full context. The answerer was `claude-haiku-4-5` and the judge `claude-sonnet-4-6`, the same for every system [7].

| Benchmark | Metric | Basic Memory | mem0 | grep | Full context |
|---|---|---|---|---|---|
| [LongMemEval](../datasets/longmemeval.md), 60 questions | recall@5 | 0.951 | 0.979 | 0.846 | n/a |
| LongMemEval, 60 questions | MRR (mean reciprocal rank) | 0.900 | 0.876 | 0.832 | n/a |
| LongMemEval, 60 questions | QA (question answering) accuracy | 0.583 | 0.450 | 0.333 | 0.217 |
| ConvoMem, 274 questions | recall@5 | 0.982 | 0.996 | 0.954 | n/a |
| ConvoMem, 274 questions | MRR | 0.929 | 0.956 | 0.863 | n/a |
| ConvoMem, 274 questions | QA accuracy | 0.755 | 0.464 | 0.380 | 0.799 |

The file's own caveats: "internal-only", judge-human agreement "not yet measured", QA scores bound to a small answerer, modest samples. It reads retrieval as near-parity with mem0: mem0 leads recall@5 on both benchmarks and MRR on ConvoMem, and Basic Memory leads MRR on LongMemEval [7]. The file also gives recall@10 (0.951 against 0.992 on LongMemEval, 0.996 against 1.000 on ConvoMem) and mean latency, which this table omits [7]. QA is the answerer's work: the file's diagnostic finds nearly every QA failure of both systems is a case where the gold evidence was retrieved and the answer still wrong, so the QA lead is not a recall lead [7]. On ConvoMem, full context scored higher than Basic Memory [7].

A web search on 20261102 found no independent evaluation. Search results are leads, not sources, so none is cited.

## Status and direction

*Release.* v1.0.0, published 20261029 23:45 UTC, is GitHub's latest release. It removes older tools without aliases and replaces `sync` and `bisync` with `push` and `pull` [4][6].

*Activity.* The watch-list on the [projects page](./README.md) carries the live figures. As a dated snapshot read on 20261102: 891 commits to the default branch since 20260804, of which one login authored 809 (computed) [5]. Six releases fall in the window [4].

*Security.* v0.24.0 fixed a high-severity flaw (GHSA-4gfv-c2mm-mvj2): a web page could reach an HTTP-transport server on localhost by DNS rebinding and call every tool. Earlier releases are affected; stdio is not [6]. The repository lists the advisory, published 20261023; GitHub's global database returned 404 for it at read time [12].

*Licence and hosted tier.* The README lists source as AGPL-3.0 for both Cloud and Local [3]; whether the hosted service's own code is public is **unstated**. Two facts point toward the hosted product. The ChatGPT `search` and `fetch` adapters left the local server in v1.0.0 because "the hosted Cloud server provides them" [6]. And contributors sign an agreement assigning copyright to Basic Machines LLC, which "may license the Contributions under any license terms" [10]. Cloud costs $15 a month for beta subscribers (regular $19) [3].

*Direction.* v0.24.0 added wiki projections and a static OKF (Open Knowledge Format) export [6]. No roadmap file is named in the sources read.

*Reading:* the design keeps the Markdown canonical and the index rebuildable, which is the plain-files claim, and development is fast but concentrated in one author (809 of 891 commits). The product around it is a subscription, and the agreement lets the company relicense contributions; the agreement text read does not grant contributors a matching right and does not mention a licence back to them (**unstated**) [10]. The archive page holds the longer notes: [Basic Memory in the archive](../../kb-kg/projects/basic-memory.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [agent-memory (Tigerless Labs)](tigerless-agent-memory.md)
- [claude-obsidian](claude-obsidian.md)
- [LLM Wiki (nashsu)](llm-wiki-nashsu.md)
- [Projects](README.md)

**Index**

- [LLM wiki](../index/llm-wiki.md)
- [Reciprocal rank fusion](../index/reciprocal-rank-fusion.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/basicmachines-co/basic-memory : repository metadata, archived flag (read 20261102 20:15 UTC)
2. https://api.github.com/repos/basicmachines-co/basic-memory/license and https://github.com/basicmachines-co/basic-memory/blob/main/LICENSE : licence text head and GitHub's classification (read 20261102 20:35 UTC)
3. https://api.github.com/repos/basicmachines-co/basic-memory/readme (the README): format, tools, search, reranker, sync, Cloud, pricing, licence table (read 20261102 20:34 UTC)
4. https://api.github.com/repos/basicmachines-co/basic-memory/releases and https://api.github.com/repos/basicmachines-co/basic-memory/releases/latest : v1.0.0 and the six releases since 20260804 (list read 20261102 20:17 UTC; latest re-read 20:35 UTC)
5. https://api.github.com/repos/basicmachines-co/basic-memory/commits?since=2026-08-04T00:00:00Z : commit count and author counts (re-read 20261102 20:35 UTC)
6. https://github.com/basicmachines-co/basic-memory/blob/main/CHANGELOG.md : v1.0.0, v0.24.0 entries, security note, tool list, ChatGPT adapters (read 20261102 20:17 UTC)
7. https://github.com/basicmachines-co/basic-memory/blob/main/benchmarks/benchmarks/results/matrix-v2-summary.md : internal benchmark tables and caveats; last change 20260625 from https://api.github.com/repos/basicmachines-co/basic-memory/commits?path=benchmarks/benchmarks/results/matrix-v2-summary.md (re-read 20261102 20:34 and 20:35 UTC)
8. https://github.com/basicmachines-co/basic-memory/blob/main/docs/semantic-search.md and https://github.com/basicmachines-co/basic-memory/blob/main/docs/multilingual-embedding-benchmark.md : index, embeddings, fusion formula, embedding comparison (read 20261102 20:19 and 20:17 UTC)
9. https://github.com/basicmachines-co/basic-memory/blob/main/docs/DOMAIN_MODEL.md : projections, rebuildability, accepted-write window (read 20261102 20:19 UTC)
10. https://github.com/basicmachines-co/basic-memory/blob/main/CLA.md : copyright assignment in section 3, no licence-back clause in sections 1 to 6 (re-read 20261102 20:34 UTC)
11. https://github.com/basicmachines-co/basic-memory/blob/main/pyproject.toml : licence field (re-read 20261102 20:35 UTC)
12. https://api.github.com/repos/basicmachines-co/basic-memory/security-advisories and https://api.github.com/advisories/GHSA-4gfv-c2mm-mvj2 : advisory listed 20261023; global database 404 (read 20261102 20:17 UTC)
