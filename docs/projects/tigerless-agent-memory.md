---
type: project
repo: tigerless-labs/agent-memory
trends: [plain-file-knowledge, agent-memory]
updated: 20261102 23:17 UTC
---

# agent-memory (Tigerless Labs)

This page answers what agent-memory is, how it stores and ranks memories as Markdown files, what its authors have measured, and how far it has got in two months. The chapter landing's watch-list table carries stars and push dates.

| Field | Value |
|---|---|
| Repository | https://github.com/tigerless-labs/agent-memory |
| Licence | MIT. GitHub's licence endpoint classifies the `LICENSE` file as MIT; the file reads "MIT License", "Copyright (c) 2026 Tigerless Labs" [1][2] |
| Trends | [Plain files as agent knowledge](../trends/plain-file-knowledge.md), [Agent memory](../trends/agent-memory.md) |

## What it is

agent-memory is a long-term [agent memory](../index/agent-memory.md) runtime. Its description reads "plain Markdown as the source of truth, local ranked retrieval, and an independent sleep-time Manage layer" [1]. One memory is one Markdown file with front matter; a SQLite index beside the files is a cache that can be deleted and rebuilt, and the project's invariants say so first [4][5]. Claude Code, Codex CLI and Muse Code share one store through hooks, a skill and a command-line tool `mem` [4]. The first commit is 20260901 21:52 UTC [6]. Its own claim to distinction is a consolidation pass that runs apart from the writing path [4][5]. [Basic Memory](./basic-memory.md) and [claude-mem](./claude-mem.md) sit on the same trends.

## How it works

**Store.** A directory holds `MEMORY.md` (a one-line-per-memory index, the only text injected at session start), one schema file per memory type, the memories at `<type>/<group>/<name>.md`, an append-only `archive/` of provenance and session traces, and one dream report per consolidation [4]. A memory carries `valid_from` and an optional `invalid_at`; replaced or deleted files stay on disk and answer `recall --as-of <date>` [4].

**Writing.** Hooks fire at conversation boundaries. A detached process runs the host's own command-line agent headless, with a small toolkit (`recall`, `read`, `submit_operations`), to propose memory operations; the library validates and writes them [4]. The library holds no [LLM](../index/large-language-model.md) (large language model) client (invariant 5) [5]. The working agent can also write through `mem` or an [MCP](../index/model-context-protocol.md) (Model Context Protocol) server with nine tools, installed only with `--mcp` [4].

**Retrieval.** Recall is [BM25](../index/bm25.md) (Best Matching 25, a keyword ranking function) over an SQLite FTS5 index. An optional vector index (default model `BAAI/bge-small-en-v1.5`, enabled with `vector_enabled = true`) is fused by reciprocal-rank fusion, as in [hybrid search](../index/hybrid-search.md) [4]. The README's own measurement of that fusion is under Evidence. Recall returns paths with one-line abstracts, and the agent opens a hit at a chosen depth. The default read path calls no model [4].

**The graph.** The README says relations "live as links inside the memories" and that front-matter `links` carry the graph without a graph database [4]. In `recall.py` and `context.py`, read now, no step follows a link; the one match for "link" is a separator constant [8]. *Reading:* here the graph is metadata kept for merging and auditing, not a retrieval path. Other modules were not searched.

**Consolidation ("sleep").** A deterministic pass adjusts weights and dates and adds links; a host-model reviewer may accept or reject drafted proposals [4]. The README says an unattended pass may add and update, that deletion "only ever arrives as a proposal you confirm", and that Manage "cannot delete anything unattended" [4]. Invariant 6 says the model-decided pass only creates new files or marks old ones invalid, and physical removal is a human-run command that Manage cannot reach [5]. The two sources agree: the unattended pass adds, updates and invalidates; physical removal needs a human command.

## Evidence

All published results are first-party. The README reports several, set out below; the [LongMemEval](../datasets/longmemeval.md)-S table is the main one [4]. For independent evaluation, a check made on 20261102 between 20:36 and 20:40 UTC found none, and the check is not exhaustive [15]. The repository holds 120 issues and pull requests; 10 are plain issues, all bug reports or one feature request, and by title none reports a measurement of recall or answer quality [15]. GitHub search for the repository name outside the repository returned catalogue listings, integration proposals and package updates; two read carried no measurement [15]. An alphaXiv paper search by project name returned no paper that names it, and a web search, which is a lead only, returned nothing about the project [15]. The archive's search of 20261030 also found none [14]. Independent results are **unstated**.

**LongMemEval-S study.** The main result: LongMemEval-S with the haystack cut to 12 sessions per episode, 120 episodes, Claude Code with Haiku 4.5 as host, one Sonnet 5 judge [4].

| Arm | Pooled accuracy | Run by |
|---|---|---|
| agent-memory | 127/240 = 52.9% | project (first-party) |
| MemCore | 86/240 = 35.8% | project (first-party) |
| no memory | 7/120 = 5.8% | project (first-party) |

The README says the bounded haystack makes the numbers not comparable with published LongMemEval scores, and that the system-to-system row licenses no attribution to either half of the pipeline [4]. It places the protocol, ledger and raw run records in `docs/experiments.md` and `experiments/` "in the working tree" and says they "ship with the source, not with git history", so the repository does not track them; the current tree holds neither, as that statement predicts [4][7]. The commit of 20260904 (`c5a7fc5`), from before tracking stopped, does hold a ledger [10]:

- Seven configurations of the same system on the same 120 episodes scored from 48.3% to 66.7%; the ledger says rows differing by less than about seven answers "are not distinguishable" [10].
- The 66.7% row is marked "claim retracted" [10].
- The first study of the consolidation layer (P11, 24 episodes) concluded "Not measurably, and this round could not have measured it": at the shipped threshold the drafter produced 10 proposals over about 3,600 entries, and 6 of 24 exam episodes had any accepted decision [10].

**Two further first-party results** [4]:

| Result | Numbers | Run by |
|---|---|---|
| One store, three hosts | all 9 ordered writer/reader pairs across Claude Code, Codex CLI and Hermes pass; pooled net contribution over no memory 2/36 to 13/36, p=0.0074 | project (first-party) |
| Optional vector fusion, fixed 120-query retrieval set | Recall@5 (the share of relevant items in the top five) 79.0% to 86.6%; median retrieval latency 5.1 ms to 139.2 ms; fixed-context answer replays 17/24 against 18/24, and 28/36 against 27/36 on the expanded set | project (first-party) |

The README itself says the answer-level experiments "do not establish an end-to-end accuracy improvement", so vector retrieval stays optional [4]. The three-host result names Hermes, while the README's badge and opening lines name Muse Code as the third host [4]; the reason is **unstated**.

*Reading:* the project documents its own noise floor unusually openly, but the layer it calls its wedge has no measured effect yet.

## Status and direction

- **Latest release.** None. No GitHub release and no tag; the version in `pyproject.toml` is 0.1.0; the README says there is "no release on PyPI yet" [3][4][7]. The name `agent-memory-core` on PyPI belongs to an unrelated project (version 0.1.0, uploaded 20260222) [13].
- **Activity, 20260804 to 20261102.** 324 commits, all since the first commit: 162 in September and 162 in October. The newest, 20261030 14:02 UTC, is a merge; none since [6]. Eighteen contributors are listed; pull requests numbered up to #120 by 20261101 [9]. The last push-triggered CI (continuous integration) run on `main`, 20261030, passed [12].
- **Direction.** The follow-up file lists authorisation for permanent removal, recovery of interrupted multi-file operations, a durable write queue, and a write-side benchmark round; no release plan or date is stated [11].
- **Maintenance mode or hosted tier.** Neither is stated in the sources read [4][11].

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [EverOS](everos.md)
- [Projects](README.md)

**Index**

- [LLM wiki](../index/llm-wiki.md)
- [Reciprocal rank fusion](../index/reciprocal-rank-fusion.md)

<!-- END GENERATED: appears-in -->

## Sources

No paper. The papers chapter group pages for its trends are [Agent memory papers](../papers/agent-memory.md) and [Plain files papers](../papers/plain-file-knowledge.md).

1. https://api.github.com/repos/tigerless-labs/agent-memory : description, licence field (MIT), archived flag (false), created 20260901 (read 20261102 20:16 UTC)
2. https://github.com/tigerless-labs/agent-memory/blob/main/LICENSE : MIT text and copyright line, via the licence endpoint (read 20261102 20:16 UTC)
3. https://api.github.com/repos/tigerless-labs/agent-memory/releases and `/tags` : both empty, no release (read 20261102 20:16 UTC)
4. https://github.com/tigerless-labs/agent-memory/blob/main/README.md : design claims, store layout, interface, install, results (read 20261102 20:16 UTC; re-read for the three-host and vector results and the untracked-experiments statement 20261102 20:36 UTC)
5. https://github.com/tigerless-labs/agent-memory/blob/main/CLAUDE.md : invariants 1 to 9 (read 20261102 20:17 UTC)
6. https://api.github.com/repos/tigerless-labs/agent-memory/commits?since=20260804 : 324 commits, monthly counts, oldest and newest dates (read 20261102 20:16 UTC)
7. https://api.github.com/repos/tigerless-labs/agent-memory/git/trees/HEAD?recursive=1, `.gitignore` and `pyproject.toml` : file list (no `experiments/`), version 0.1.0 (read 20261102 20:17 to 20:18 UTC)
8. https://github.com/tigerless-labs/agent-memory/blob/main/packages/core/src/agent_memory/core/recall.py and `context.py` : no link-following step (read 20261102 20:20 UTC)
9. https://api.github.com/repos/tigerless-labs/agent-memory/issues?state=all and `/contributors` : pull request numbers, 18 contributors (read 20261102 20:17 and 20:19 UTC)
10. https://github.com/tigerless-labs/agent-memory/blob/c5a7fc59452ac29d2be8c653be4f5b71465dce21/experiments/results/index.md and `p11-manage.md` : ledger, retracted row, P11 findings (read 20261102 20:18 UTC)
11. https://github.com/tigerless-labs/agent-memory/blob/main/docs/TODO.md : follow-ups (read 20261102 20:17 UTC)
12. https://api.github.com/repos/tigerless-labs/agent-memory/actions/runs?branch=main&event=push : latest runs, success (read 20261102 20:19 UTC)
13. https://pypi.org/pypi/agent-memory-core/json : unrelated package holding the name (read 20261102 20:20 UTC)
14. Archive page [kb-kg/projects/tigerless-agent-memory.md](../../kb-kg/projects/tigerless-agent-memory.md) : the earlier search for independent studies, which found none (read 20261030 19:34 UTC, carried over; superseded for this page by source 15)
15. https://api.github.com/repos/tigerless-labs/agent-memory/issues?state=all, https://api.github.com/search/issues and https://api.github.com/search/repositories for the repository name, https://github.com/greeves89/AI-Employee/issues/731 and https://github.com/Daily-Nerd/scout/issues/42 (two listings read), an alphaXiv paper search by project name, and a web search (a lead only) : no independent evaluation found (read 20261102 20:36 to 20:40 UTC)
