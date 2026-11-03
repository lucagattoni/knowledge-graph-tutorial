---
type: project
repo: Mirix-AI/MIRIX
trends: [agent-memory]
updated: 20261102 23:17 UTC
---

# MIRIX

MIRIX is a memory system for [agents](../index/agent.md) that sorts what an agent learns into six typed stores, each run by its own agent. This page says how it works, what its authors and others have measured, and what changed when the project dropped its desktop assistant.

| Field | Value |
|---|---|
| Repository | https://github.com/Mirix-AI/MIRIX |
| Licence | Apache-2.0. The `LICENSE` file is the Apache License 2.0 text, with the notice "Copyright 2023, Letta authors"; GitHub classifies it as Apache-2.0 [1][2]. The file's history shows the MIT licence of the first commit (20250416) replaced by this Apache text on 20250711, with the commit title "update LICENSE" [12] |
| Trends | [Agent memory](../trends/agent-memory.md) |

## What it is

MIRIX comes from the paper "MIRIX: Multi-Agent Memory System for LLM-Based Agents" by Yu Wang and Xi Chen (arXiv 2507.07957, 20250710; no venue shown on the arXiv page) [3]. The README titles it a "Multi-Agent Personal Assistant with an Advanced Memory System" [4]. The docs say that from 0.1.6 the `main` branch is "a pure memory system" that plugs into other agents, and that the desktop assistant is deprecated and lives on the `desktop-agent` branch [5]. The README still lists screen activity tracking as a feature [4].

It is built on [Letta](./letta.md): the README thanks Letta for a framework that "served as the foundation" of the memory system, and the paper says its core memory is inspired by MemGPT [4][3].

## How it works

**Six stores.** Core (persona and user facts), Episodic (events), Semantic (concepts), Procedural (step-by-step how-tos), Resource (documents and media) and a Knowledge Vault for verbatim sensitive items such as credentials [3]. The paper criticises [knowledge-graph](../index/knowledge-graph.md) memory such as [Zep](../../kb-kg/projects/zep.md) and [Cognee](./cognee.md) as weak on events and images, and flat vector stores such as [Mem0](./mem0.md) and Letta as lacking structure [3].

**Agents.** A Meta Memory Manager routes each input to six Memory Managers, one per store. Retrieval is "active": the chat agent first writes a topic, and matching memories enter its system prompt [3]. Memory agents call a configured [large language model](../index/large-language-model.md); the README example uses a Google model and Google embeddings. Local-model use is unstated [4].

**Running it.** `docker compose` starts a REST server and a dashboard; a Python `MirixClient` adds messages and retrieves memories [4]. Storage is PostgreSQL 17 (SQLite also named), searched by [BM25](../index/bm25.md) (Best Matching 25, a keyword ranking function) full text plus [vector](../index/vector-search.md) similarity [5]. An `auto_dream` endpoint merges duplicates and resolves stale entries per store [4]. The repository holds an MCP (Model Context Protocol) client module; whether MIRIX itself serves memory over the [Model Context Protocol](../index/model-context-protocol.md) is unstated [6].

## Evidence

MIRIX's authors ran two tests, both first-party. Another group ran a third.

| Date | Result | Who ran it | First-party | Source |
|---|---|---|---|---|
| 20250710 | ScreenshotVQA, the authors' own set (87 questions from three students' screenshots): MIRIX 59.5% against 44.1% for a retrieval baseline (SigLIP, top 50) and 11.7% for Gemini reading the latest 3,600 resized screenshots; Letta and Mem0 were left out because they take no images. Storage 15.89 MB against 15.07 GB. The "35% higher" in the abstract is relative (59.5 / 44.1) | Paper authors | yes | [3][7] |
| 20250710 | [LoCoMo](../datasets/locomo.md), scored by an [LLM judge](../index/llm-as-judge.md), gpt-4.1-mini: MIRIX 85.38%, Zep 79.09%, LangMem 78.05%, Mem0 62.47%; the full-conversation baseline scores 87.52%, above MIRIX. Baselines were run once with the Mem0 and Zep evaluation code on gpt-4.1-mini; MIRIX and the full-conversation baseline three times | Paper authors | yes | [7] |
| 2026 (v4 20260628) | [MemoryAgentBench](../benchmarks/memoryagentbench.md), GPT-4o-mini: MIRIX overall 26.2, below the plain long-context baseline (42.2) and MemGPT (28.3); with GPT-4.1-mini 37.7. Strong at accurate retrieval (47.5), weak at selective forgetting (8.0) | UC San Diego authors | no, but see below | [8] |

Two caveats on the LoCoMo row, both from the paper's appendix [7]. The authors' Zep run through the Mem0 implementation scored only 49.09 with gpt-4.1-mini; they suspected an implementation error and left it out, so the Zep figure above comes from Zep's own code. The appendix table lists LangMem at 79.22 with gpt-4.1-mini against 78.05 in Table 2; the text I read does not explain the difference.

MIRIX's first author is named Yu Wang, and a co-first author of MemoryAgentBench has the same name; the two papers list the same email address for that name [3][8].

## Status and direction

- Not archived. `main` has 7 commits since 20260804: two in August (adaptive session-tag routing) and five merged or rebased on 20261027 and 20261028 (committer date; the earliest was authored 20261008). Their subjects: the merge of the procedural-skill-learning pull request, session-based procedural skill learning, decoupling core from the `skill_bench` harness, fitting the e2e curator batch in its context window, and a fix to image release scope and organization deletion. 11 contributors; 48 open issues and pull requests [1][9].
- Releases: GitHub has no release (the latest-release call returns 404) and six tags, newest `v0.1.6`. PyPI `mirix` is 0.1.7, uploaded 20260201, summary "Mirix Client". The README installs `mirix-client`, but PyPI's JSON for that name returned 404 on 20261102. The reason is unstated [1][10][11].
- Upgrades: existing databases need manual SQL migrations; the server refuses to start while any are pending [4].
- Hosted tier: none named in the README or docs read. Roadmap: unstated.

*Reading:* MIRIX has the most elaborate store design in this chapter but the thinnest independent evidence. Its main results are the authors' own, and its release and install paths are untidy. MemoryAgentBench shares an author name with MIRIX, so I do not count it as independent; it is also the less flattering result. I found no fully independent evaluation.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Letta](letta.md)
- [Projects](README.md)

**Benchmarks**

- [MemoryAgentBench](../benchmarks/memoryagentbench.md)

**Index**

- [Agent memory](../index/agent-memory.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/Mirix-AI/MIRIX : metadata, licence field, archived flag, open issues and pull requests, contributors (read 20261102 20:09 UTC; contributors 20:16 UTC)
2. https://api.github.com/repos/Mirix-AI/MIRIX/license : LICENSE file (Apache 2.0, "Copyright 2023, Letta authors") and GitHub's classification (read 20261102 20:09 UTC)
3. https://arxiv.org/abs/2507.07957 and https://arxiv.org/pdf/2507.07957 : abstract, authors, six stores, agents, active retrieval, results (read 20261102 20:13 UTC; PDF 20:10 UTC)
4. https://api.github.com/repos/Mirix-AI/MIRIX/readme : features, quick start, auto-dream, migrations, licence section, acknowledgement of Letta (read 20261102 20:09 UTC)
5. https://docs.mirix.io : scope of `main` from 0.1.6, desktop-agent branch, storage and search (read 20261102 20:13 UTC)
6. https://api.github.com/search/code?q=mcp+repo:Mirix-AI/MIRIX : files with "mcp" in the repository, among them an `mcp_client` module (read 20261102 20:13 UTC)
7. https://arxiv.org/pdf/2507.07957 : Tables 1 and 2, baseline settings, ScreenshotVQA construction, appendix A (Table 3, Zep re-run note) (read 20261102 20:10 UTC; Tables 1-3 and appendix re-read 20:32 UTC)
8. https://arxiv.org/pdf/2507.05257 and https://arxiv.org/abs/2507.05257 : MemoryAgentBench Table 3, author list (read 20261102 20:10 UTC; abstract page 20:13 UTC)
9. https://api.github.com/repos/Mirix-AI/MIRIX/commits?since=2026-08-04 : the 7 commits, with author and committer dates and subjects (read 20261102 20:09 UTC; dates re-read 20:33 UTC)
10. https://api.github.com/repos/Mirix-AI/MIRIX/releases/latest and /tags : 404 for the release, six tags (read 20261102 20:09 UTC)
11. https://pypi.org/pypi/mirix/json and https://pypi.org/pypi/mirix-client/json : version 0.1.7 and upload date; 404 for `mirix-client` (read 20261102 20:15 UTC)
12. https://api.github.com/repos/Mirix-AI/MIRIX/commits?path=LICENSE and the file text at each commit : two commits, MIT 2025-04-16 (c588cf0b, "initial version") and Apache License 2.0 2025-07-11 06:38 UTC (a5944e0c, "update LICENSE") (read 20261102 22:58 UTC)

Papers: Wang and Chen, "MIRIX: Multi-Agent Memory System for LLM-Based Agents", arXiv 2507.07957 (2025); Hu, Wang and McAuley, "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions", arXiv 2507.05257. The papers chapter groups them under [agent memory](../papers/agent-memory.md).
