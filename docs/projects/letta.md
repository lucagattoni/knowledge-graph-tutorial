---
type: project
repo: letta-ai/letta
trends: [agent-memory]
updated: 20261102 20:34 UTC
---

# Letta

Letta is the project that grew out of the MemGPT paper: an [agent](../index/agent.md) whose [large language model](../index/large-language-model.md) manages its own memory. This page says how its memory works, what has been measured and by whom, and why the repository named `letta` no longer holds the code.

| Field | Value |
|---|---|
| Repository | https://github.com/letta-ai/letta (landing page and retired server on the `archive` branch). Current code: https://github.com/letta-ai/letta-code |
| Licence | Apache-2.0. The `LICENSE` file of `letta-ai/letta` is the Apache License 2.0 text with the notice "Copyright 2023, Letta authors", and GitHub classifies it as Apache-2.0 [1][2]. `letta-ai/letta-code` is also Apache-2.0 ("Copyright 2025, Letta authors") with an added "Brand Assets Exclusion": the Letta name, logo, images and ASCII art are Letta, Inc. assets not licensed under Apache-2.0. GitHub's classification does not show that exclusion [6][7] |
| Trends | [Agent memory](../trends/agent-memory.md) |

## What it is

Letta began as MemGPT, a research system from UC Berkeley described in arXiv 2310.08560 (first version 20231012) [13]. Letta is now also a company, Letta, Inc., with a hosted service, Letta Cloud [7][9]. The `letta-ai/letta` README says the current source lives in `letta-ai/letta-code`, a TypeScript harness with a terminal interface, an App Server and chat channels [3]. Its `main` branch is a landing page. The retired Python V1 server sits on the `archive` branch, which `AGENTS.md` calls unsupported, with no fixes or security updates [3][4].

The same file forbids using that archived code for benchmarks or comparisons [4]; this page treats the archive as history and Letta Code as the project. The README of [MIRIX](./mirix.md) says Letta's open-source framework "served as the foundation" for its memory system [20].

## How it works

**The 2023 design.** MemGPT gave the model a fixed prompt split into instructions, a read-write working context and a message queue, plus recall and archival storage outside the prompt. The model moved data between them by function calls. The queue manager warned the model when the prompt passed a set share of the [context window](../index/context-window.md) (the paper's example is 70%). At the flush limit (example: 100% of the window) it evicted a set count of messages (example: 50% of the window) and wrote a new recursive summary [13].

**Today (MemFS).** Each agent owns a git repository of Markdown files with YAML front matter, checked out on whichever computer it runs on. Files at the root go into the system prompt on every turn. Directories with their own `MEMORY.md` stay out of context until opened. The agent edits with ordinary file tools; every edit is a commit [10].

**Search.** MemFS has no semantic or vector index by default. Keyword, semantic and hybrid search come from an optional mod, and the semantic modes need the QMD indexer [10]. Message history is searched separately: full-text, [vector](../index/vector-search.md) and hybrid on Letta Cloud, full-text only on local backends [10].

**Dreaming.** Background subagents review recent conversations and update memory, after a set number of steps or when the context is compacted [11]. The README says the April 2025 sleep-time compute paper is "now called" dreaming [9].

## Evidence

Four of five results below are first-party.

| Date | Result | Who ran it | First-party | Source |
|---|---|---|---|---|
| 20231012 | Deep memory retrieval accuracy: GPT-4 32.1% to 92.5% with MemGPT; GPT-4 Turbo 35.3% to 93.4%; GPT-3.5 Turbo 38.7% to 66.9%. Baselines are fixed-context models | Paper authors | yes | [13] |
| 20250417 | Sleep-time compute cuts test-time compute about 5x for equal accuracy on two modified reasoning tasks | Paper authors | yes | [14] |
| 20250812 | 74.0% on [LoCoMo](../datasets/locomo.md) for an agent searching a conversation file (GPT-4o mini), against the 68.5% reported for the graph variant of [Mem0](./mem0.md); Letta did not rerun Mem0 | Letta | yes | [15] |
| 202610 | FrontierMemory 1.0, 15 tasks, full-pass rate at max task effort, mean of 3 runs, each memory system on its own task harness. With Opus 5.5 as memory and task model: "Letta Dream" 73.3%, Hermes Agent 64.4%, Claude Managed Agents 55.6%, Prime Agent 53.3%. With the second pair (memory model GPT-6.1 Sol, task model GPT-6 Sol, as the source labels them): Letta Dream 42.2%, OpenAI Agents SDK 26.7%, Prime Agent 13.3%, Hermes Agent 4.4%. Letta Research's own benchmark; memory runs on Letta Code | Letta Research | yes | [16] |
| 2026 (v4 20260628) | [MemoryAgentBench](../benchmarks/memoryagentbench.md): MemGPT overall 28.3, against 42.2 for the plain GPT-4o-mini long-context baseline and 26.2 for MIRIX | UC San Diego authors | no, but see below | [17] |

MemoryAgentBench ran MemGPT through its archival-insert and send-message functions, so it tested the legacy library; the version is unstated [17]. A co-first author named Yu Wang on that paper has the same name as the first author of the MIRIX paper, and both papers list the same email address for that name [17][19].

## Status and direction

- `letta-ai/letta`: not archived on GitHub. Its latest release is 0.16.8, 20260514 [5]. Since 20260804 it has had 7 commits, all documentation, policy, spam-guard or the 20260816 "archive the legacy server repository" change [5].
- `letta-ai/letta-code`: latest release v0.34.38, 20261102 07:09 UTC. It has 1,015 commits since 20260804; two bot accounts authored 498 of them, so the raw count overstates human activity [8].
- PyPI `letta` now ships Letta Code: latest 0.34.12, 20261012. The `license` field is empty, `license_expression` is Apache-2.0, and there is no licence classifier [18].
- Hosted tier: remote computers and secrets need a Letta sign-in [9]; shared memory is for cloud-hosted agents [10]; agents made without an account live on local disk, out of reach of the web app [12]. Cloud memory repositories are capped at 5 MiB (Free) or 50 MiB (Pro) [11].
- Roadmap: unstated.

*Reading:* Letta rebuilt its memory design, from database-backed tiers to files in git with learning in background runs, but the evidence has not followed: the only results on the current design come from Letta itself. The MemoryAgentBench run is third-party to Letta, but one of its co-first authors has the same name as the first author of a competing system's paper (MIRIX), so I do not count it as independent. I found no independent evaluation of Letta Code's memory.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [MemOS](memos.md)
- [MIRIX](mirix.md)
- [Projects](README.md)

**Papers**

- [Papers: Agent memory](../papers/agent-memory.md)

**Benchmarks**

- [MemoryAgentBench](../benchmarks/memoryagentbench.md)

**Index**

- [Agent memory](../index/agent-memory.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/letta-ai/letta : repository metadata, licence field, archived flag, dates, description (read 20261102 20:09 UTC)
2. https://api.github.com/repos/letta-ai/letta/license : LICENSE file content (Apache 2.0, "Copyright 2023, Letta authors") and GitHub's classification (read 20261102 20:09 UTC)
3. https://api.github.com/repos/letta-ai/letta/readme : README, pointer to `letta-ai/letta-code`, `archive` branch (read 20261102 20:09 UTC)
4. https://github.com/letta-ai/letta/blob/main/AGENTS.md : retirement of the V1 server, prohibited uses (read 20261102 20:11 UTC)
5. https://api.github.com/repos/letta-ai/letta/releases/latest and /commits?since=2026-08-04 : release 0.16.8 and the 7 commits (read 20261102 20:09 UTC)
6. https://api.github.com/repos/letta-ai/letta-code : metadata and licence field (read 20261102 20:09 UTC)
7. https://api.github.com/repos/letta-ai/letta-code/license : LICENSE text with the Brand Assets Exclusion (read 20261102 20:09 UTC)
8. https://api.github.com/repos/letta-ai/letta-code/releases/latest and /commits?since=2026-08-04 : v0.34.38 and 1,015 commits by month and author (read 20261102 20:09 UTC)
9. https://github.com/letta-ai/letta-code : README (company, features, Cloud-only features, dreaming, AgentFile removal, research links) (read 20261102 20:10 UTC)
10. https://docs.letta.com/concepts/memfs/ : MemFS structure, search, versioning, shared memory (read 20261102 20:10 UTC)
11. https://docs.letta.com/configuration/memory/ : dreaming, review option, storage caps (read 20261102 20:10 UTC)
12. https://docs.letta.com/concepts/stateful-agents/ : where agents are stored (read 20261102 20:10 UTC)
13. https://arxiv.org/abs/2310.08560 and https://arxiv.org/pdf/2310.08560v2 : MemGPT abstract, memory tiers, warning and flush thresholds and eviction count in section 2.2, Table 2 (read 20261102 20:10 UTC; section 2.2 re-read 20:31 UTC)
14. https://arxiv.org/abs/2504.13171 : sleep-time compute abstract and numbers (read 20261102 20:10 UTC)
15. https://www.letta.com/blog/benchmarking-ai-agent-memory/ : LoCoMo 74.0% setup and the comparison with Mem0's "top-performing graph variant" (read 20261102 20:11 UTC; re-read 20:32 UTC)
16. https://www.frontiermemory.com/blog/v1/ : FrontierMemory 1.0 setup and both model-pair panels of Figure 2 (read 20261102 20:11 UTC; re-read 20:32 UTC)
17. https://arxiv.org/pdf/2507.05257 and https://arxiv.org/abs/2507.05257 : MemoryAgentBench Table 3, MemGPT run description (read 20261102 20:10 UTC; abstract page 20:13 UTC)
18. https://pypi.org/pypi/letta/json : latest version and upload date; `info.license` empty, `info.license_expression` Apache-2.0, no licence classifier (read 20261102 20:31 UTC)
19. https://arxiv.org/pdf/2507.07957 : MIRIX paper, first-author name and first page (read 20261102 20:10 UTC)
20. https://github.com/Mirix-AI/MIRIX : README acknowledgement that Letta's framework was the foundation of the memory system (read 20261102 20:09 UTC)

Papers: Packer et al., "MemGPT: Towards LLMs as Operating Systems", arXiv 2310.08560 (2023); Lin et al., "Sleep-time Compute: Beyond Inference Scaling at Test-time", arXiv 2504.13171 (2025); Hu et al., "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions", arXiv 2507.05257. The papers chapter groups them under [agent memory](../papers/agent-memory.md).
