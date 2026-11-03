---
type: project
repo: topoteretes/cognee
trends: [agent-memory]
updated: 20261102 23:17 UTC
---

# Cognee

This page answers what Cognee is, how it turns data into memory, and who has measured it. It also records which parts are open source and which sit behind licensed or hosted products, and that its own published scores come from its own team.

| Field | Value |
|---|---|
| Repository | https://github.com/topoteretes/cognee [1] |
| Licence | Apache-2.0. GitHub classifies the `LICENSE` file as Apache-2.0; the file is the standard Apache 2.0 text with the notice "Copyright 2024 Topoteretes UG", and `pyproject.toml` declares the same [2][3]. |
| Trends | [Agent memory](../trends/agent-memory.md) |

## What it is

The README titles Cognee "The Free Open-Source AI Memory Platform for Agents" and says it turns documents, code and conversations into a self-hosted [knowledge graph](../index/knowledge-graph.md) that agents search and reuse [4]. It is a Python package (3.10 to 3.14) with a REST API, a command-line tool, a web interface and an MCP (Model Context Protocol) server [3][4]. Four operations make up the memory API: `remember` stores, `recall` retrieves, `improve` enriches memory from feedback and sessions, and `forget` removes [4].

Agents reach it through plugins, any [MCP](../index/model-context-protocol.md) client, and Python, TypeScript and Rust SDKs [4].

## How it works

**Write.** `add` registers the data; `cognify` splits it into chunks, has a [language model](../index/large-language-model.md) extract entities and relationships, summarises, and [embeds](../index/embedding.md) the results. A first pipeline run indexes the chunks, so chunk search answers before any entity exists [5]. `improve` then bridges sessions and feedback into the graph [4].

**Stores.** Cognee keeps a graph, vectors and relational metadata in separate stores. The code defaults are Ladybug for the [graph](../index/graph-database.md), LanceDB for vectors and SQLite for metadata [6][7][8].

**Schemas and ontologies.** A Pydantic model can replace the generic graph schema [5]. An [OWL](../index/owl.md) [ontology](../index/ontology.md) (RDF/XML) grounds extracted entities. In the default `annotate` mode matches are renamed to the ontology's term and unmatched entities are kept; `strict` mode drops them. Grounding reads only classes, types, subclass links and object properties [9].

**Without a cloud key.** With no LLM (large language model) key the README says Cognee extracts with a local [GLiNER](./gliner.md) model and embeds locally. It calls the bundled extractor "a demo" and invites readers to contact the team for a production-ready version; the licence terms of that version are **unstated** [4].

## Evidence

Every score on this page is a published figure; none was reproduced here.

| Result | Who ran it | Limits stated by the runner | Source |
|---|---|---|---|
| BEAM 100K: 0.79; BEAM 10M: 0.67 | Cognee team, first-party | 100K: 20 questions of one held-out conversation, 4 rounds. 10M: routing chosen on the scored questions, so "exploratory" | [4][10] |
| [LoCoMo](../datasets/locomo.md): about 91% (90.7% and 91.3% in two runs) of 1,762 of 1,986 questions | Cognee team, first-party, ingested 20261007 | 96 open-domain and 143 audit-flagged questions excluded; setup developed on the same ten conversations; own judge, stricter than some others | [11] |
| [MemoryAgentBench](../benchmarks/memoryagentbench.md) overall average with a GPT-4o-mini backbone: Cognee 20.6, against Zep 24.0 (see [Graphiti](./graphiti.md)), [Mem0](./mem0.md) 21.1, MemGPT 28.3, [HippoRAG](./hipporag.md)-v2 41.6 | Hu, Wang and McAuley, not the Cognee team | Run with `add`, `cognify` and `search`; Cognee version **unstated** in the passage read | [12] |

The first-party reports say what they are: the BEAM report calls its two scores "not a controlled comparison across scales" [10]. The 2025 paper (Markovic and 3 others, arXiv 20250530) tunes chunking, graph construction, retrieval and prompts on three multi-hop question sets; its abstract gives no scores [13]. The README presents it as Cognee's own research, so it counts as first-party [4].

*Reading:* the only third-party number found puts Cognee near Mem0 (21.1) and Zep (24.0) and well below plain BM25 (Best Matching 25, a keyword ranking function) retrieval (41.5) and GPT-4o-mini, the same backbone, with its 128K context (42.2) in that table [12]. The two first-party reports use other benchmarks, so the three results cannot be compared.

## Status and direction

*Release.* v1.6.6, 20261029 21:33 UTC, is GitHub's latest [14]. Since 20260804 there are 25 tags, 13 of them stable (v1.4.2 to v1.6.6) [14].

*Activity.* Work lands on a `dev` branch, and `main` trails it. Snapshot of 20261102; it drifts, and the watch-list carries current figures. Since 20260804, `dev` has 1,895 non-merge commits by 105 author names and `main` has 1,864 [15].

*Open and hosted.* Cognee Cloud lists a Free plan (1 workspace, 1M tokens), a Standard plan at $1.00 per 1M tokens plus $5 per extra workspace, and an Enterprise plan that includes "Bi-temporal memory & conflict resolution" [16]. The open repository also shipped a conflict-resolution API and made conflict review the default in v1.6.6 [14]. Whether the Enterprise version differs is **unstated**. The README labels the Postgres graph store a demo whose "production-ready version is available as a licensed product" [4].

*Direction.* The README leads with a shared "Company Brain", memory across agent runs and ontologies [4]. Release titles since September name keyless workflows (v1.6.0), temporal search (v1.6.3) and conflict resolution (v1.6.6) [14]. The `temporal_cognify` option was removed in v1.6.3 and the code still accepts it as deprecated and ignored [5][14]. No roadmap file sits at the top level of the repository [17].

*Reading:* Cognee is very active and not archived [1], broad in scope, and draws a visible line between its free core and hosted or separately offered extras, though the licence terms of most of those extras are unstated.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Claude-Mem](claude-mem.md)
- [Graphiti](graphiti.md)
- [MemOS](memos.md)
- [MIRIX](mirix.md)
- [Projects](README.md)
- [Semantica](semantica.md)

**Datasets**

- [MuSiQue](../datasets/musique.md)

**Benchmarks**

- [MemoryAgentBench](../benchmarks/memoryagentbench.md)

**Index**

- [Agent memory](../index/agent-memory.md)
- [Selective forgetting](../index/selective-forgetting.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/topoteretes/cognee (via `gh api`) : repository metadata, archived flag (read 20261102 20:09 UTC)
2. https://github.com/topoteretes/cognee/blob/main/LICENSE and https://api.github.com/repos/topoteretes/cognee/license (via `gh api`) : licence text, notice line, GitHub's classification (read 20261102 20:14 UTC)
3. https://github.com/topoteretes/cognee/blob/main/pyproject.toml : licence field, version 1.6.6, Python range (read 20261102 20:14 UTC)
4. https://github.com/topoteretes/cognee/blob/main/README.md (via `gh api repos/topoteretes/cognee/readme`) : self-description, operations, interfaces, keyless mode, GLiNER demo wording, Postgres demo, BEAM table (read 20261102 20:09 UTC; lines 96, 137 and 282 re-read 20261102 20:33 UTC)
5. https://github.com/topoteretes/cognee/blob/main/cognee/api/v1/cognify/cognify.py : pipeline stages, graph model, ontology argument, deprecated `temporal_cognify` (read 20261102 20:14 UTC)
6. https://github.com/topoteretes/cognee/blob/main/cognee/infrastructure/databases/graph/config.py : default graph provider `ladybug` (read 20261102 20:14 UTC)
7. https://github.com/topoteretes/cognee/blob/main/cognee/infrastructure/databases/vector/config.py : default vector provider `lancedb` (read 20261102 20:14 UTC)
8. https://github.com/topoteretes/cognee/blob/main/cognee/infrastructure/databases/relational/config.py : default `sqlite` (read 20261102 20:14 UTC)
9. https://docs.cognee.ai/guides/ontology-support : ontology format, modes, constructs read (read 20261102 20:14 UTC)
10. https://github.com/topoteretes/cognee/blob/main/cognee/eval_framework/beam/REPORT.md : BEAM method, scores, limits (read 20261102 20:14 UTC)
11. https://github.com/topoteretes/cognee/blob/main/cognee/eval_framework/locomo/REPORT.md : LoCoMo method, scores, exclusions, limits (read 20261102 20:14 UTC)
12. https://arxiv.org/abs/2507.05257 and https://arxiv.org/html/2507.05257 : Hu, Wang, McAuley, "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions", v4 20260628; Table 3 and the Cognee setup paragraph (read 20261102 20:13 UTC; Table 3 values re-read 20261102 20:34 UTC)
13. https://arxiv.org/abs/2505.24478 : Markovic, Obradovic, Hajdu, Pavlovic, "Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning", v1 20250530, abstract (read 20261102 20:14 UTC)
14. https://api.github.com/repos/topoteretes/cognee/releases/latest and https://api.github.com/repos/topoteretes/cognee/releases (via `gh api`; 30 listed, back to 20260722), v1.6.3 and v1.6.6 notes (read 20261102 20:09 UTC)
15. https://api.github.com/repos/topoteretes/cognee/commits?since=2026-08-04T00:00:00Z&sha=main and the same with `sha=dev` (via `gh api`; 2,796 and 2,834 commits including merges), paged (read 20261102 20:10 and 20:15 UTC)
16. https://www.cognee.ai/pricing : plans, prices, Enterprise features (read 20261102 20:14 UTC)
17. https://api.github.com/repos/topoteretes/cognee/git/trees/main (via `gh api`) : top-level listing, no roadmap file (read 20261102 20:13 UTC)

Further reading in the archive: [Cognee, long entry](../../kb-kg/projects/cognee.md). Papers: [agent memory group](../papers/agent-memory.md).
