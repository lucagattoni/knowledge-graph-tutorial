---
slug: letta
repo: letta-ai/letta
tier: deep
category: agent-memory
snapshot: 20261030 19:29 UTC
---

# Letta (formerly MemGPT)

Reading times: `letta-ai/letta` metadata, files and commits at 20261030 19:29 UTC; `letta-ai/letta-code`,
the docs site and package indexes 19:30 to 19:32; the paper, benchmark papers and blog posts 19:33 to 19:36.
Each source below carries its own time.

**Read this first.** The repository this entry is named for no longer holds the project's code. Its `main`
branch is a landing page of 12 files in 3 directories (15 tree entries). The Letta V1 Python server sits on an `archive` branch, declared retired
and unsupported. The current implementation is a different repository, `letta-ai/letta-code` (TypeScript)
[2][4][5][6]. The 25k stars belong to the older repository. This entry keeps three things apart: the MemGPT
paper, the retired V1 server (historical) and Letta Code (current).

| | |
|---|---|
| Repository | https://github.com/letta-ai/letta (landing page and `archive` branch). Current code: https://github.com/letta-ai/letta-code [2][8] |
| Licence | Apache License 2.0, from the `LICENSE` file of `letta-ai/letta` (appendix notice "Copyright 2023, Letta authors") [3]. GitHub's API also reports Apache-2.0 [1]. The README names no licence and shows no badge, so nothing disagrees [2]. `letta-ai/letta-code` is also Apache-2.0 ("Copyright 2025, Letta authors") with an added "Brand Assets Exclusion": the Letta and Letta Code names, logo, wordmark, images and ASCII art are Letta, Inc. assets that are not licensed under Apache-2.0 [10]. The API field does not show that exclusion [8]. |
| Language | GitHub reports no primary language for `letta-ai/letta`; its languages endpoint returns an empty object [1]. From the tree: `main` holds only Markdown, YAML and a citation file [2]. The `archive` branch is Python (878 `.py` files, about 10.4 MB by tree sizes) [6]. The current code in `letta-ai/letta-code` is TypeScript (20.5 MB by the languages endpoint) [8]. |
| Stars, forks | `letta-ai/letta`: 25,294 and 2,662 (20261030 19:29 UTC) [1]. `letta-ai/letta-code`: 3,741 and 456 (19:30 UTC) [8]. |
| Created, last push | `letta-ai/letta`: 20231011 07:38 UTC, 20261018 22:28 UTC [1]. `letta-ai/letta-code`: 20251025 04:17 UTC, 20261030 19:02 UTC [8]. |
| Latest release | `letta-ai/letta`: 0.16.8, 20260514 17:14 UTC [5]. Current line: `letta-code` v0.34.34, 20261030 18:34 UTC [8]. |
| Status | `letta-ai/letta`: not archived on GitHub and pushed within 90 days, but every commit since 20260730 is a documentation, policy, issue-guard or archive change [5]; the server code is declared retired [4]. `letta-ai/letta-code`: active, 999 commits listed since 20260801 [12]. |
| Paper, docs | MemGPT: arXiv 2310.08560, v1 20231012, v2 20240212 18:59 UTC [22]. Docs: https://docs.letta.com [13]. |

**Snapshot flags.** The 20261030 19:13 UTC snapshot row for `letta-ai/letta` carries no flag [36]. Its
numbers are averages: 22.69 stars per day over 1,115 days and 10.52 forks per 100 stars (live 2,662 of 25,294
gives the same) [36][1]. Both are heuristics. Live contributors: 139, or 155 with anonymous commits [1]. GitHub
issue search returns 0 open issues for `letta-ai/letta` and 193 for `letta-code` [1][8]; the sources do not
explain the 0. The evidence supports "an old, large, now-superseded repository" and no conclusion about how
the stars were earned.

## What it is

Letta is an AI lab and company based in San Francisco. The docs use "Letta" as the umbrella name for the
company, the hosted platform and the open-source products [14]. It began as MemGPT, a UC Berkeley research
system in which an LLM manages its own memory tiers [22]. A post dated 20240923 set the names: "MemGPT" for
the original agent design pattern of the paper, "Letta" for the framework and the company [23]. The
repository README still says "Letta (f.k.a. MemGPT)" and `CITATION.cff` cites the paper [2][4].

Today the project calls itself a "stateful agent harness": agents with a persistent identity, memory and
message history, driven from a terminal UI, a web app, chat channels or an SDK [9][14]. The memory idea has
moved from "a model edits tiers in a database" to "an agent edits a git repository of Markdown files". The
repository's `AGENTS.md` says not to infer current Letta behaviour from `letta-ai/letta` and not to use its
archived code for benchmarks, comparisons or copying into other projects [4]. This entry follows that:
archived code was read only to describe history.

## How it works

### Memory architecture today (Letta Code)

The current system prompt for a git-backed agent names the architecture in its own words. Message history
("experience") is stored automatically as **recall memory** and cannot be mutated; the context window holds
the most recent messages of the current conversation plus a summary of older evicted messages [11]. Memory
the agent controls is split into **core memory** (in the system prompt) and **external memory** (outside it)
[11]. The docs describe the storage as **MemFS**, also called a context repository [14].

| Tier | What it holds | In context? | Who writes it | Where it is stored |
|---|---|---|---|---|
| Recall (message history) | Every message of every conversation of the agent | Recent messages of the current conversation, plus a summary of older ones | The harness, automatically; the agent cannot change it | Letta Cloud, or local disk on the local backend [11][13][20] |
| Core memory | Markdown files at the MemFS root, each with `name` and `description` front matter (for example `persona.md`, `human.md`), plus a root `MEMORY.md` index | Yes, compiled into the system prompt on every turn | The agent, with ordinary file tools, and background "dreaming" subagents | The agent's own git repository [11][14] |
| Deferred (external) memory | Directories that carry their own `MEMORY.md` index, and files below them | No. Only the file tree and descriptions are listed; the agent opens one level at a time | Same as core | Same git repository [11][14] |
| Skills (procedural memory) | `skills/<name>/SKILL.md` folders in MemFS; global (`~/.letta`) and project (`.agents/skills`) skills also exist | Loaded on demand | Agent, or `letta skills install` | MemFS for agent-scoped skills [9][14] |
| Shared memory (Cloud only) | Repositories attached to several agents | As a file tree it reads from, not inlined | Agents; the harness auto-pushes committed changes after each turn | Letta-hosted repositories [11][15] |

Points that follow from the sources:

- **Budgets.** The code defaults to a directory depth of 2, 20,000 characters per file and 65,536 characters
  for all core memory; a tracked config file can override them, per path pattern too [11]. The hosted service
  caps each memory repository at 5 MiB (Free) or 50 MiB (Pro), counted on the latest snapshot, not on git
  history [13][17].
- **No vector index in memory.** MemFS "does not include a semantic or vector index by default"; agents use
  ordinary file search and read tools. Keyword search comes from an optional mod; semantic or hybrid search
  needs an external indexer (QMD) over the memory directory [14][17].
- **Message search is separate.** The recall subagent runs a CLI search in `vector`, `fts` or `hybrid` mode
  (hybrid is the default: vector similarity plus full-text search, combined by reciprocal-rank-fusion
  scoring) [11]. The docs say Cloud supports all three and local backends full-text only [14].
- **Reading deferred memory.** A tool named `Memory` opens a directory or file from the deferred part, listing
  up to 10 entries per directory, most recently edited first; its description calls it a read tool [11].
  Commits titled "remove memory and memory_apply_patch" (20260925) and "add Memory tool for MemFS v2 agents"
  (20261008) mark the change; only the titles were read [12].
- **Two layouts.** The MemFS page says newer agents keep core files at the root and older agents in `system/`
  [14]. The Agent SDK memory page says files under `system/` are in the prompt every turn [15]. The sources do
  not reconcile the two.
- **Non-MemFS agents.** The docs say all agents use MemFS [14]. The prompt README still lists a prompt "for
  non-memfs agents" that pins plain `persona` and `human` blocks into the system prompt, and the code loads
  those two default blocks [11]. Which agents still run without MemFS is unstated.

### How the agent edits memory

The agent edits memory the way it edits code. MemFS projects the agent's git repository onto the computer
where the agent runs, as a real checkout, and the agent uses ordinary file tools in that directory [14]. Every
memory edit is committed; edits are local until committed and pushed, and then become the agent's memory on
every computer [14]. The system prompt adds two rules: an edit does not change behaviour in the current turn,
because that turn's prompt was compiled at its start; and secrets must not be written to memory, because it
is git-tracked and may sync off the machine [11]. Memory subagents use git worktrees so they can write
without blocking the main agent [14]. The code also has front-matter and budget checks and a background worker
that repairs post-turn git conflicts; the check files were read in part only [11][12].

### Background learning and compaction

- **Dreaming (reflection).** Background subagents review recent conversations, consolidate lessons and update
  memory without interrupting the active work [13]. A built-in `reflection` subagent reads a transcript,
  ranks candidate learnings (mistakes and corrections first, then preferences, facts, contradictions and
  repeatable procedures), edits memory files and commits them under a distinct author [11]. The CLI default
  trigger is context compaction, with a step count of 25 for the step trigger; the SDK offers triggers `off`,
  `step-count` and `compaction-event`, and behaviours `reminder` or `auto-launch` [11][15]. An option adds a
  second background conversation that reviews proposed updates; the docs say it costs more tokens and does not
  ask the user for approval [13]. Automatic client-side dreaming is off by default on native Windows [9].
- **Compaction.** Near the model's limit, older messages are summarised and recent ones kept; a summary can
  lose exact wording, so the agent can search the history [14]. The local backend's code has modes `all` and
  `sliding_window` and defaults to a sliding window with a 0.3 constant [11]. The Cloud setting is unstated.
- **Maintenance commands.** `/init` bootstraps memory, `/remember` teaches a lesson, `/doctor` audits placement,
  duplication and prompt size [13].

### Where state lives

On Letta Cloud the memory repository, messages, conversations and configuration are stored by Letta, and tools
run on whichever computer the agent is pointed at [14]. On the local backend everything is on the user's disk
(the App Server uses a directory under `~/.letta`), with no account, no backup and no web-app access [13][16].
The on-disk format of the local record was not read (`unstated`).

### From the MemGPT paper to Letta Code

| | MemGPT paper (v2) [22] | Retired V1 server (history) [6][7] | Letta Code today [11][14] |
|---|---|---|---|
| In-context memory | System instructions (read-only), working context (a fixed-size read/write text block, writable only through functions) and a FIFO queue of messages with a recursive summary at index 0 | Core memory blocks: label, description, value, character limit, read-only flag | Root Markdown files compiled into the system prompt, with character budgets |
| Out-of-context memory | Recall storage (message database) and archival storage (read/write text database searched by embedding, paged) | Conversation search; archival memory with insert and semantic-search functions (tags, date range, `top_k`) over an embedding column (pgvector or sqlite-vec options) | Message history searched by `letta messages search`; "archival" appears in neither current system prompt nor the memory docs read; deferred files are the external store |
| How memory is edited | LLM output parsed as function calls; a memory-pressure warning at a set share of the window (for example 70%), then a flush that evicts a share (for example 50%) | Memory tools: append, replace, insert, rethink, apply-patch, finish-edits | Ordinary file tools and git commits in a memory checkout |
| Control flow | `request_heartbeat` chains calls; interrupts manage control between user and agent | Heartbeat language in the v2 prompt | "Heartbeats and crons" now appear as scheduling features [9]; function chaining is unstated |
| Background work | None | Sleep-time multi-agent groups in four versions (file names) [6] | Dreaming subagents in git worktrees [14] |
| Git | Not part of it | A git-backed block manager and memory-repository schemas exist (file names and one docstring) [7] | Central: memory is a git repository |

In order: the 20240923 rename; a Python server with database-backed blocks and an embedding-backed archival
store; sleep-time compute (an April 2025 paper, "now called dreaming" per the Letta Code README) [31][9]; active
development moving to the TypeScript `letta-code` repository (created 20251025); and the server's retirement
on 20260816 [8][5].

### What is open source and what is hosted

| Component | Where | Licence and status |
|---|---|---|
| Letta Code harness, CLI, App Server | `letta-ai/letta-code`; npm `@letta-ai/letta-code` | Apache-2.0 plus the brand exclusion [10][20] |
| Letta Agent SDK (TypeScript only) | `letta-ai/letta-agent-sdk` (113 stars); npm `@letta-ai/letta-agent-sdk` 0.8.63 | Apache-2.0 [20][15] |
| PyPI `letta` | Python wheels that bundle a Node runtime and install the `letta` command | Latest 0.34.12 (20261012 20:47 UTC); the licence field in the PyPI metadata is empty (`unstated` there) [19] |
| API client SDKs | Repositories `letta-python` and `letta-node` are described as SDKs for the Letta API; the FAQ names generated clients `@letta-ai/letta-client` (npm) and `letta-client` (PyPI) | Apache-2.0 repositories; the docs advise against building applications directly on the clients [21][14] |
| Retired V1 server (Python) | `archive` branch; PyPI `letta` up to 0.16.8; the `letta/letta` Docker image | Apache-2.0 by the `LICENSE` file. Declared "unsupported", with no fixes or security updates. `AGENTS.md` asks that it not be copied into new projects; the sources do not reconcile that with the licence [3][4][6][19] |
| Letta Cloud | `api.letta.com`, `platform.letta.com`, `chat.letta.com` | Hosted service under Terms of Service in `TERMS.md`. Source of the hosted API server: none found among the 30 most-starred repositories of the organisation; whether it is published is unstated [4][14][21] |

Features the docs mark "Cloud only": shared memory, the remote client API, the hosted MCP server and dynamic
workflows; secrets and remote computers need a Letta sign-in [9][16][18]. Plans, as read: Free at $0 (3 agents,
5 MiB per memory repository, bring-your-own keys), Pro at $20 per month (up to 20 agents, 50 MiB), and an API
plan at $20 per month plus $0.10 per active agent per month and $0.00015 per second of tool execution [17].

### How an agent or developer talks to it

| Interface | What it is | Source |
|---|---|---|
| CLI `letta` | Terminal UI; headless mode `letta -p`; `letta server` starts the App Server | [9][16] |
| Letta Agent SDK | TypeScript client around the harness: `createAgent` once, `resumeSession` later; backend `cloud` or `local`; no Python version ("run App Server and use its WebSocket protocol from Python") | [14][15] |
| App Server | `letta server --listen`: one bidirectional WebSocket at `/ws`; many clients; optional `--openai-api` exposes OpenAI-compatible Models, Chat Completions and Responses endpoints | [14][16] |
| Letta REST API | `api.letta.com` for Cloud agents with an API key; generated clients exist, but the docs steer application developers to the Agent SDK | [14] |
| Hosted MCP server | `https://api.letta.com/mcp` with a bearer key; six tools (`list_agents`, `list_models`, `create_agent`, `send_agent_message`, `get_run`, `get_reply`) that let another agent create and message Letta agents. Messages run on a Cloud computer in unrestricted permission mode | [16] |
| MCP in the SDK | Client-side: stdio, HTTP or SSE servers passed per session; tools are session-scoped and not stored on the agent. The docs recommend skills over MCP | [14][15] |
| ACP adapter, channels | `letta-acp` for editors such as Zed; Slack, Telegram, Discord, Signal, WhatsApp and custom channels | [14][18] |

## Cost and operating profile

- **No index-time LLM cost in the RAG sense.** There is no corpus index. The model spends tokens when it reads
  and writes memory through tool calls, when it summarises on compaction, and when background dreaming
  subagents run (a review pass adds more) [11][13].
- **Query time.** Core memory costs prompt tokens on every turn, bounded by the core budget (65,536 characters
  by default); deferred memory costs a tool call per directory opened; recall search is a CLI call [11].
- **Needs.** The npm install needs Node.js: the docs say 22.19 or newer, while `package.json` lists
  `^22.23.4`, `^24.22.1` or `^26.12.1`, a mismatch the sources do not explain [16][20]. A Python wheel with a
  bundled runtime avoids Node [9]. Also git and a model provider (own keys, or Letta-provided models on Cloud)
  [9][16]. A Letta account is optional.
- **Fully local?** Yes by design: "all agent state ... stays on-device, and no Letta account is required"; a
  local Ollama or LM Studio server can supply inference [16]. Local agents have no built-in web search or
  image generation, and no automatic backup [16][14].

## Evidence

Every row below comes from someone with a stake. The repository's `AGENTS.md` says results from the retired
server "describe a retired system" and cannot be presented as current Letta results [4]. For shared benchmark
definitions and other projects' memory claims see [papers and benchmarks](../papers-benchmarks/README.md) [37].

### Claims by Letta (first party)

| Date | Claim | Setup as stated | Source |
|---|---|---|---|
| 20231012 (v2 20240212) | Deep memory retrieval accuracy: GPT-3.5 Turbo 38.7% to 66.9% with MemGPT; GPT-4 32.1% to 92.5%; GPT-4 Turbo 35.3% to 93.4%. In nested key-value retrieval GPT-4 and GPT-4 Turbo fall to 0% by 3 nesting levels while MemGPT with GPT-4 is unaffected by nesting depth | Multi-Session Chat data; baselines are fixed-context models; authors' own runs and LLM judge | [22] |
| 20250417 | Sleep-time compute lowers test-time compute for the same accuracy by about 5x on two modified reasoning tasks; up to 13% and 18% higher accuracy when scaled | Stateful GSM-Symbolic and Stateful AIME, built by the authors | [31] |
| 20250529 and October 2025 | Letta Leaderboard (models ranked on reading, writing and updating memory) and Context-Bench (agentic context engineering; top scores in the post text 74.0% and 72.67%) | Both by Letta. Leaderboard: prompted GPT-4.1 grader with a penalty for extra memory operations, synthetic facts, scores only in images. Context-Bench: open-sourced; read through a fetch summariser, not checked against the raw page | [26][27] |
| 20250805 | 42.5% on Terminal-Bench, "4th overall and 2nd among agents using Claude 4 Sonnet" | A terminal agent built on Letta's 2025 stateful-agents SDK, before Letta Code existed (repository created 20251025); benchmark version, run configuration and who ran it unstated | [30] |
| 20250812 | 74.0% on LoCoMo for an agent with file tools over the conversation file, against the 68.5% that Mem0 reported for its graph variant (the [mem0 entry](mem0.md) tabulates 68.44) | GPT-4o mini; tool rules force `search_files` first; Mem0's figure is the one it reported, not rerun by Letta; the post names no judge and does not say whether all of LoCoMo was used; the benchmark code is linked from the post (the repository `letta-leaderboard` is now archived [21]) | [25] |
| 20260728 | A comparison of model families on memory use and memory generation | Private benchmark, "Context-Bench V2"; no numbers; LLM judge; no code | [28] |
| October 2026 | FrontierMemory 1.0, 15 tasks: with one matched model pair, "Letta Dream" scored 73.3%, against 64.4% for Hermes Agent, 55.6% for Claude Managed Agents and 53.3% for Prime Agent | Published by Letta Research; mean of 3 runs; each system in its native task harness; 53% of the source tasks had broken verifiers that the authors repaired. The post does not say the code is public; an Apache-2.0 repository `letta-ai/frontiermemory` (25 stars) exists [21] | [29] |

The 20250812 post also says its authors could not find a way to backfill LoCoMo into MemGPT/Letta without
significant refactoring, calls results it attributes to Mem0 "controversial", and says Mem0 did not respond
to requests for clarification [25]. The Mem0 paper describes its MemGPT row as one of the "previously
benchmarked" methods with "published results", and the row's values match the A-MEM paper's MemGPT row (for
example 26.65, 17.72, 9.15 and 7.44) [34][33]. Whether Mem0 ran MemGPT itself is not shown in what was read.

### Evaluations by others

None of these evaluates the current Letta Code memory. Each that ran MemGPT or Letta ran the legacy library.
A web search at 20261030 found no independent evaluation of Letta Code or MemFS [38].

| Who | What was run | Result for MemGPT / Letta | Caveat | Source |
|---|---|---|---|---|
| UC San Diego authors, MemoryAgentBench (ICLR 2026) | Long-context, RAG, structure-augmented and agentic-memory agents (22 rows in the main table) on a GPT-4o-mini backbone: accurate retrieval, test-time learning, long-range understanding, selective forgetting. MemGPT was loaded through its archival-memory insert function and queried through its send-message function | Overall 28.3. Long-context GPT-4o-mini 42.2; BM25 41.5; HippoRAG-v2 41.6; MIRIX 26.2; Zep 24.0; Mem0 21.1; Cognee 20.6; Self-RAG 18.7. MemGPT by competency: retrieval 34.3, test-time learning 40.8, long-range 22.4, forgetting 15.5 | Letta version unstated; third party to Letta | [32] |
| A-MEM authors (a competing method) | LoCoMo, with MemGPT as a baseline | MemGPT uses about 16,900 tokens per operation against about 1,200 for A-MEM (text; its table lists 1,126 to 2,520); A-MEM reports higher F1 in most categories, with MemGPT strong in some (open-domain, adversarial) for GPT-based models | Competitor-run; how the baseline was run is not described in what was read | [33] |
| Zep authors (a competing product) | Deep Memory Retrieval (the MemGPT paper's task) | Zep 94.8% against MemGPT's reported 93.4% with GPT-4 Turbo, and a full-conversation baseline of 94.4%. They could not reproduce MemGPT with GPT-4o mini ("insufficient methodological details") and could not make MemGPT answer LongMemEval after loading messages into archival memory | Competitor-run; each conversation has 60 messages, which fit in current context windows | [35] |

In MemoryAgentBench the agentic MemGPT ranks below the plain long-context baseline and below BM25 on the
overall score, and its test-time-learning average is below the baseline's (40.8 against 48.6) [32]. No result
in the sources read measures the 2026 Letta Code memory.

## Direction

From the README, docs and commits [9][12][14]: agents that learn "through rewriting their own memory, skills,
prompts, and even the harness itself (through mods)"; dreaming as the main learning loop; MemFS as the single
memory format; Letta Cloud as the place where one agent's state follows it across computers; channels,
schedules and remote computers; a TypeScript Agent SDK as the application interface. Retired recently: the V1
server (20260816), AgentFile (`.af`) import and export in Letta Code, the Electron desktop app (deprecated
20261012 per the FAQ) and the `lettabot` repository (archived, replaced by channels) [5][9][14][21]. The
research page lists memory-model and continual-learning posts through October 2026 [24].

## Recent changes

Commit titles only; messages and diffs were not read. Dates are commit times in UTC [12][5].

- 20260816: "archive the legacy server repository" on `letta-ai/letta` (#3430) [5].
- 20260828 and 20260908: "configurable memory layout", "enforce configurable memory limits", "enforce default
  MemFS v2 budgets" [12].
- 20260918: "remove legacy server-side memory tool handling" [12].
- 20260923: "create new cloud agents on the MemFS v2 root layout"; a background worker for memory upkeep and
  git-conflict repair [12].
- 20260925 and 20260926: "remove memory and memory_apply_patch"; local agents created with root MemFS [12].
- 20260929 and 20260930: a "Memory Palace" experiment and skill, made Cloud-only [12].
- 20261008: "add Memory tool for MemFS v2 agents" [12].
- 20261019: built-in skills `maintaining-core-memory` and `maintaining-deferred-memory` [12].
- 20261028: "hide the memory subagent from agents; keep it for automatic repair" [12].
- 112 stable npm versions of `@letta-ai/letta-code` since 20260801, the latest 0.34.34 [20].
- PyPI `letta`: no release between 0.16.8 (20260514) and 0.32.13 (20260917); the current summary reads "Letta
  Code: stateful agents in your terminal". Which release first changed the contents is unstated [19].

## Sources

1. https://api.github.com/repos/letta-ai/letta : metadata, licence field, languages (empty), topics, contributors (139 and 155), open-issue count (read 20261030 19:29 UTC; contributors and issues 19:36 and 19:38 UTC)
2. https://github.com/letta-ai/letta : `README.md` and the 15-entry tree of `main` (read 20261030 19:29 UTC)
3. https://github.com/letta-ai/letta/blob/main/LICENSE : Apache-2.0 text and copyright notice (read 20261030 19:29 UTC)
4. https://github.com/letta-ai/letta/blob/main/AGENTS.md , `CONTRIBUTING.md`, `SECURITY.md`, `CITATION.cff`, `TERMS.md` on `main` : retirement of the V1 server, prohibited uses, citation of the MemGPT paper, hosted terms (read 20261030 19:29 UTC)
5. https://api.github.com/repos/letta-ai/letta/commits and /releases : commits since 20260730, release list (0.16.8, 20260514) (read 20261030 19:29 UTC)
6. https://github.com/letta-ai/letta/tree/archive : tree (1,282 entries, 878 `.py`), `README.md`, `pyproject.toml`, recent commits (read 20261030 19:29 to 19:33 UTC)
7. https://github.com/letta-ai/letta/tree/archive/letta : `functions/function_sets/base.py`, `prompts/system_prompts/memgpt_v2_chat.py`, `schemas/block.py`, `orm/passage.py`, `schemas/memory_repo.py`; historical reading only (read 20261030 19:33 UTC)
8. https://api.github.com/repos/letta-ai/letta-code : metadata, languages, releases, contributors (51) (read 20261030 19:30 UTC; contributors 19:36 UTC)
9. https://github.com/letta-ai/letta-code : `README.md` (read 20261030 19:30 UTC)
10. https://github.com/letta-ai/letta-code/blob/main/LICENSE : Apache-2.0 plus Brand Assets Exclusion (read 20261030 19:30 UTC)
11. https://github.com/letta-ai/letta-code/tree/main/src : `tools/descriptions/Memory.md`, `agent/memory.ts`, `agent/prompts/` (`letta_root_memfs.md`, `letta_no_memfs.md`, `README.md`, `recall_subagent.md`), `agent/subagents/builtin/` (`reflection-v2.md`, `memory.md`, `recall.md`), `backend/local/compaction.ts`, `memory-constraints.ts`, `agent/memory-constraints.ts`, `cli/helpers/memory-reminder.ts`, `reflection-settings.ts`, tree listing (read 20261030 19:30 to 19:37 UTC)
12. https://api.github.com/repos/letta-ai/letta-code/commits : 999 commits since 20260801 (subjects read; messages of four read) (read 20261030 19:30 UTC and 19:37 UTC)
13. https://docs.letta.com/configuration/memory/ and https://docs.letta.com/concepts/conversations/ : memory and dreaming, storage limits, compaction (read 20261030 19:31 UTC)
14. https://docs.letta.com/concepts/memfs/ , /concepts/stateful-agents/ , /reference/terminology/ , /reference/faq/ : MemFS, backends, products, interfaces, SDKs, search (read 20261030 19:31 to 19:32 UTC)
15. https://docs.letta.com/agent-sdk/ , /agent-sdk/memory/ , /agent-sdk/mcp/ : SDK, memory settings, dreaming options, client-side MCP (read 20261030 19:31 UTC)
16. https://docs.letta.com/platform/hosted-mcp/ , /self-hosting/ , /self-hosting/app-server/ : hosted MCP server, local runtime, App Server (read 20261030 19:31 UTC)
17. https://docs.letta.com/pricing/ : plans and storage caps (read 20261030 19:31 UTC)
18. https://docs.letta.com/llms.txt : page index (read 20261030 19:31 UTC)
19. https://pypi.org/pypi/letta/json : release history and current summary (read 20261030 19:32 UTC)
20. https://registry.npmjs.org/@letta-ai/letta-code , https://registry.npmjs.org/@letta-ai/letta-agent-sdk , https://api.github.com/repos/letta-ai/letta-agent-sdk , `package.json` of `letta-code` : versions, licence, SDK repository, Node engine range (read 20261030 19:32 UTC)
21. https://api.github.com/orgs/letta-ai/repos : repository list with licences, stars and archive flags (read 20261030 19:37 UTC)
22. https://arxiv.org/abs/2310.08560 and https://arxiv.org/pdf/2310.08560 : MemGPT abstract, v2 date, tiers, eviction policy, tables 2 and 3, nested key-value results (read 20261030 19:33 and 19:34 UTC)
23. https://www.letta.com/blog/memgpt-and-letta/ : rename of 20240923 and what each name means; read through a fetch summariser (read 20261030 19:36 UTC)
24. https://www.letta.com/research : list of research posts and Letta's own numeric claims; read through a fetch summariser (read 20261030 19:34 UTC)
25. https://www.letta.com/blog/benchmarking-ai-agent-memory/ : LoCoMo 74.0% setup and caveats; raw page checked (read 20261030 19:35 UTC)
26. https://www.letta.com/blog/letta-leaderboard/ : leaderboard scope and grader; fetch summariser (read 20261030 19:35 UTC)
27. https://www.letta.com/blog/context-bench/ : Context-Bench scores; fetch summariser (read 20261030 19:35 UTC)
28. https://www.letta.com/blog/evaluating-memory-in-production-agents/ : private benchmark post; fetch summariser (read 20261030 19:35 UTC)
29. https://www.frontiermemory.com/blog/v1/ : FrontierMemory 1.0 results; raw page checked (read 20261030 19:36 UTC)
30. https://www.letta.com/blog/terminal-bench/ : Terminal-Bench claim; raw page checked (read 20261030 19:36 UTC)
31. https://arxiv.org/abs/2504.13171 : sleep-time compute abstract (read 20261030 19:36 UTC)
32. https://arxiv.org/abs/2507.05257 : MemoryAgentBench, table of overall scores, MemGPT run description (read 20261030 19:35 UTC)
33. https://arxiv.org/abs/2502.12110 : A-MEM, MemGPT baseline on LoCoMo, token counts (read 20261030 19:35 UTC)
34. https://arxiv.org/abs/2504.19413 : Mem0 paper, MemGPT row described as published results (read 20261030 19:35 UTC)
35. https://arxiv.org/abs/2501.13956 : Zep paper, DMR comparison and failed LongMemEval attempt (read 20261030 19:35 UTC)
36. [`repos.tsv`](../landscape/20261030_1913-github/repos.tsv) : snapshot row for `letta-ai/letta` (read 20261030 19:29 UTC)
37. [`papers-benchmarks/README.md`](../papers-benchmarks/README.md) : benchmark definitions and the entry for the MemGPT paper (read 20261030 19:29 UTC)
38. Web search, 20261030 about 19:38 UTC : query for independent evaluations of Letta Code memory; no study found (read 20261030 19:38 UTC)
