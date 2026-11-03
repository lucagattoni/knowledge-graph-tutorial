---
type: project
repo: supermemoryai/supermemory
trends: [agent-memory]
updated: 20261103 02:21 UTC
---

# Supermemory

This page answers what Supermemory is, how much of it is open, how its memory pipeline works as documented, and who has measured it. Two points matter: the MIT-licensed repository does not hold the memory engine [3][6], and the headline LongMemEval figure has had three values since December 2025 [12][14].

| Field | Value |
|---|---|
| Repository | https://github.com/supermemoryai/supermemory [1] |
| Licence | MIT. The root `LICENSE` file is MIT, "Copyright (c) 2025 supermemory" [2]. The docs call the self-hosted server binary "not open source" and "built from a separate, non-public codebase", free "within its lite license limit of 10,000 stored documents"; its licence text is **unstated** [5]. `skills/supermemory` is Apache-2.0 [4]; the SDKs, in other repositories, are Apache-2.0 [25]. Five of the six plugin repositories the README calls open source have no root `LICENSE` file [7][27]. |
| Trends | [Agent memory](../trends/agent-memory.md) |

## What it is

Supermemory calls itself "the memory and context layer for AI" [7]. One API covers memory (facts extracted from conversations), user profiles, document retrieval ([RAG](../index/retrieval-augmented-generation.md)), connectors and file processing [7]. It comes as a hosted service, as plugins and an [MCP](../index/model-context-protocol.md) (Model Context Protocol) server for coding assistants, and as Supermemory local, a self-hosted binary [7].

The repository holds docs, the MCP server, a web app and SDK helper packages; its tree shows no engine, extraction or search service [3], though its GitHub description reads "Memory and context engine + app" [1]. The local server's source "is not in the public repository" [6], and an outside study calls the hosted backend closed-source [19]. The project's LongMemEval report says its "ingestion pipeline, search implementation, and evaluation work are available through the supermemory GitHub organization" [12]; none of the organization's other 34 repositories is described as the memory engine or server [28].

*Reading:* this does not fit the [open-core](../index/open-core.md) pattern (an open core plus paid extras): the core is the closed part [3][5][6]. [Mem0](./mem0.md), [Graphiti](./graphiti.md) and [Hindsight](./hindsight.md) publish their write logic; Supermemory's is known only from its docs and reports.

## How it works

This is the project's own description; the engine could not be checked in source.

**Write.** Content passes through queued, extracting, [chunking](../index/chunking.md), [embedding](../index/embedding.md) and indexing stages [9]. A second phase, "dreaming", passes the content through a memory model, which merges, arranges and organizes it into the graph [9]. The hosted service uses "proprietary models", and which one extracts is **unstated**; the local server calls a model you supply [5][6].

**Memory model.** The docs call the store a "Temporal vector-graph engine" [9]. A new memory links to older ones as `updates` (supersedes for search; history can remain), `extends` or `derives` (an inference); you define no schema [10]. Types are facts, preferences and episodes; [forgetting](../index/selective-forgetting.md) is by expiry, contradiction and noise filtering [10].

**Read.** `search` defaults to `hybrid` (memories plus document chunks); [reranking](../index/reranking.md) and query rewriting are off by default [11]. The report says a matched memory comes back with its source chunk [12].

## Evidence

Figures are first-party unless marked; none was reproduced here.

**Headline claim.** The README says "#1" on [LongMemEval](../benchmarks/longmemeval.md), [LoCoMo](../benchmarks/locomo.md) and ConvoMem, and gives 95% Recall@15 (relevant items among the top 15; definition **unstated**) on LongMemEval with about 720 added tokens, with no score or rival for the other two [7]. The project's comparison page says its LoCoMo results are "Not in a form we can link here yet" [17]; Mem0's rival page lists them as "Not published" [18].

**One row, three values.** The gpt-4o row of the project's LongMemEval-S report (judge: GPT-4o):

| Read | Overall | Label on the page |
|---|---|---|
| 20251211, Wayback capture (same in the six captures checked, 20251202 to 20260510) | 81.6% | table headed [LLM-as-judge](../index/llm-as-judge.md) evaluation [14] |
| 20260903, Wayback capture (same in the four checked, 20260624 to 20260903) | 95% | "Recall@k=15 with aggregation", about 720 tokens; the README still gives this figure [7][14] |
| 20261103, live (same in the 20261001 and 20261013 captures) | 97% | "Recall@20 with aggregation" [12][14] |

The gpt-5 (84.6%) and Gemini 3 Pro (85.2%) overall figures did not change [12][14]; a project post of 20260322 calls the first report "~85%" [29]. The report defines no recall metric, repeats the numbers in a table headed "LLM-as-judge" and has no change note; why the row moved is **unstated**. Its Zep and full-context columns equal, digit for digit, the gpt-4o rows of Zep's paper, where they are judged answer accuracy and full context has no retrieval step [15]. Earlier versions say "Results for Zep were taken from their paper"; the live version cites the paper but has dropped that sentence [12][14]. *Reading:* the live table sets a recall figure beside two accuracy figures. Hindsight's paper used the 81.6% row as baseline [16]. The project's page says neither its 97 nor Mem0's 94.4 has been "reproduced under a matched setup" [17].

**Another claim.** That post claimed ~99% on LongMemEval-s for an experimental agent flow, "not our main production Supermemory engine (yet)". Its summary says "It was a parody"; its 98.6% run counted a question correct if any of eight prompt variants matched. The URL now redirects to the blog index [29].

**Independent runs.** Searches (arXiv abstracts, web; 20261103) found no preprint that reruns the LongMemEval figures; two quote the report's 85.2% row [22]. A rival memory vendor's blog (20260728) shows SuperMemory at 71.3% on its own LongMemEval harness, in an image table (alt text "ChatGPT Image") that lists the vendor figure as "not published"; the configuration is **unstated** [30].

- SWE-ContextBench (the project calls it independent [17]; no listed affiliation is Supermemory): one coding agent, 99 related tasks. Supermemory, via its hosted service and MCP `recall` tool, resolved 30.30%; no memory 26.26%, Mem0 24.24%, [OpenViking](./openviking.md) 29.20% [19]. The gap to no memory is about four tasks (computed); the run count is **unstated**.
- True Memory, a rival system, ran Supermemory on LoCoMo in its own harness: 65.39% against 61.43% for Mem0; Supermemory's configuration is **unstated** [20]. A single-author preprint by the maker of another compared system (Base Layer), on a personalisation task, gave Supermemory's retrieval the highest retrieval-only mean in its controlled setting [21].

**Tooling.** MemoryBench (first-party) compares Supermemory, Mem0 and Zep; its README shows no results [23]. For SMFS (a separate repository) the research page says "improving task accuracy" [13]; its own table shows correct answers rising from 99 to 100 of 110 on Claude but falling from 105 to 101 on Codex [24].

## Status and direction

*Release.* `server-v0.0.9`, 20261012, is GitHub's latest; all 18 releases are local-server tags, and native Windows stays on 0.0.8 [8]. SDKs ship elsewhere (npm 5.1.2, 20261102; PyPI 5.0.1, 20261026) [25].

*Activity.* 160 commits to `main` from 20260805 to 20261102: 57 `fix`, 46 `docs`, 31 `feat` (computed from message prefixes; 15 have none). 24 pull requests and 19 issues are open; the last commit was 20261102 [26]. Not archived [1].

*Direction.* API v5 renamed container tags to namespaces [11]. Roadmap: **unstated** [3].

*Reading:* active, mostly fixes and docs. The evidence is thin where it matters: the nearest independent run is a coding task with a four-task margin, the other outside runs come from rival makers, and the headline number moved without a stated cause.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)

**Projects**

- [Projects](README.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/supermemoryai/supermemory : repository metadata, description ("Memory and context engine + app that is extremely fast, scalable, and can be run fully locally"), archived flag, created and last-push dates (read 20261103 02:02 UTC)
2. https://api.github.com/repos/supermemoryai/supermemory/license : licence endpoint and the `LICENSE` file text, MIT (read 20261103 01:30 UTC)
3. https://api.github.com/repos/supermemoryai/supermemory/git/trees/main?recursive=1 : file tree: apps (docs, mcp, web, two playgrounds), packages, five `LICENSE` files, no engine directory, no roadmap file (read 20261103 01:30 UTC)
4. https://raw.githubusercontent.com/supermemoryai/supermemory/main/packages/tools/LICENSE, and the same path under `packages/agent-framework-python`, `packages/openai-sdk-python` (all MIT) and `skills/supermemory` (Apache-2.0) : sub-package licences (read 20261103 01:31 UTC)
5. https://raw.githubusercontent.com/supermemoryai/supermemory/main/apps/docs/self-hosting/overview.mdx : binary from a separate non-public codebase; "The server binary is not open source"; lite licence limit of 10,000 documents; models; embeddings (read 20261103 02:03 UTC)
6. https://raw.githubusercontent.com/supermemoryai/supermemory/main/apps/docs/self-hosting/local-vs-enterprise.mdx : server source not in the public repository; lite licence limit; proprietary models (read 20261103 02:03 UTC)
7. https://api.github.com/repos/supermemoryai/supermemory/readme : description, features, plugins, MCP tools, benchmark claims (read 20261103 01:30 UTC)
8. https://api.github.com/repos/supermemoryai/supermemory/releases?per_page=100 : 18 releases, all `server-v` tags; `server-v0.0.9` notes (read 20261103 01:30 UTC)
9. https://raw.githubusercontent.com/supermemoryai/supermemory/main/apps/docs/concepts/how-it-works.mdx : ingest stages, dreaming, storage engine (read 20261103 01:31 UTC)
10. https://raw.githubusercontent.com/supermemoryai/supermemory/main/apps/docs/concepts/graph-memory.mdx : relations, memory types, forgetting, no schema (read 20261103 01:31 UTC)
11. https://raw.githubusercontent.com/supermemoryai/supermemory/main/apps/docs/recall/search.mdx : search modes and defaults, namespace wording (read 20261103 01:35 UTC)
12. https://supermemory.ai/research/longmembench/ : the LongMemEval-S report: architecture, tables, metric wording, citations, the sentence on the GitHub organization; no sentence on where Zep's figures come from, no change note (read 20261103 02:04 UTC)
13. https://supermemory.ai/research : research page: 97%, "#1" on LoCoMo and ConvoMem without scores, SMFS claim (read 20261103 01:32 UTC)
14. https://web.archive.org/web/20251211094135/https://supermemory.ai/research and https://web.archive.org/web/20260903022331/https://supermemory.ai/research/longmembench/ : earlier versions of the report; gpt-4o row 81.6% and 95%, judge gpt-4o, the sentence "Results for Zep were taken from their paper" in both. Also read: the captures of `/research` or `/research/` of 20251202, 20260113, 20260306, 20260410, 20260510 (81.6%), 20260624, 20260726, 20260827 (95%) and 20261001 (97%), and the report capture of 20261013 (97%, no Zep sentence) (read 20261103 02:05 to 02:08 UTC)
15. https://arxiv.org/html/2501.13956 : Rasmussen et al., Zep; Tables 2 and 3, gpt-4o accuracy rows (read 20261103 01:32 UTC)
16. https://arxiv.org/html/2512.12818 : Latimer et al., Hindsight, v1 of 20251214; baselines "taken directly from the Supermemory technical report", Supermemory gpt-4o 81.6% (read 20261103 01:37 UTC)
17. https://supermemory.ai/compare/supermemory-vs-mem0/ : the project's comparison page, "Checked October 1, 2026"; LoCoMo and BEAM not linked; "reproduced under a matched setup"; leads with SWE-ContextBench, which it calls "an independent study" (read 20261103 02:11 UTC)
18. https://mem0.ai/compare/mem0-vs-supermemory : Mem0's rival page ("Published on: Jul 8, 2026"): Supermemory LongMemEval 85.2, LoCoMo and BEAM "Not published" (read 20261103 02:10 UTC)
19. https://arxiv.org/html/2602.08316 : Zhu et al., SWE-ContextBench, v3 of 20260506; Table 4, affiliations, appendix A.2.4 on Supermemory's closed-source backend (read 20261103 01:33 UTC)
20. https://arxiv.org/html/2605.04897 : Adler and Zehavi (Sauron Labs), True Memory; Table 2 LoCoMo, harness settings (read 20261103 01:33 UTC)
21. https://arxiv.org/html/2605.28969 : Gulaya, "Beyond Recall", v2 of 20260819; Supermemory among four commercial systems; Base Layer is the author's own reference implementation; section on helps and hurts: Supermemory's "highest C1 mean across systems" in the controlled setting (read 20261103 02:09 UTC)
22. https://export.arxiv.org/api/query?search_query=abs:supermemory : four results: SuperMemory-VQA (arXiv 2606.00825), a video-question dataset whose abstract names no link to this project; WorldDB (2604.18478v1, abstract and Table 3 quote 85.20% for Supermemory, citing the project's research page); True Memory [20]; Beyond Recall [21]. Also https://arxiv.org/html/2604.22085 (Memanto, Table IX: competitor figures "drawn from their respective published papers or official benchmark reports") (read 20261103 02:09 to 02:13 UTC)
23. https://raw.githubusercontent.com/supermemoryai/memorybench/main/README.md, the same path for `LICENSE`, https://api.github.com/repos/supermemoryai/memorybench and https://raw.githubusercontent.com/supermemoryai/supermemory/main/apps/docs/memorybench/overview.mdx : MIT; providers; provider descriptions; no published results (read 20261103 01:31 to 01:34 UTC)
24. https://smfs.ai : SMFS xAFS benchmark table, tokens and correct answers per agent (Claude 99 to 100, Codex 105 to 101 of 110) (read 20261103 02:11 UTC)
25. https://registry.npmjs.org/supermemory, https://pypi.org/pypi/supermemory/json, https://raw.githubusercontent.com/supermemoryai/sdk-ts/main/LICENSE and https://raw.githubusercontent.com/supermemoryai/python-sdk/main/LICENSE : SDK versions and dates, source repositories, Apache-2.0 files (read 20261103 01:34 to 01:35 UTC)
26. https://api.github.com/repos/supermemoryai/supermemory/commits?since=2026-08-05 and https://api.github.com/search/issues?q=repo:supermemoryai/supermemory+is:open : 160 commits, subjects, last commit, open pull requests and issues (read 20261103 01:35 UTC; counts re-run 02:03 UTC with the same result)
27. https://raw.githubusercontent.com/supermemoryai/claude-supermemory/main/LICENSE and the same path (also `LICENSE.md`, `LICENSE.txt`, `COPYING`, branches `main` and `master`) for `cursor-supermemory`, `codex-supermemory`, `opencode-supermemory`, `openclaw-supermemory`: all absent; `muse-supermemory/LICENSE` present (MIT). The README names these six plugin repositories (read 20261103 02:13 UTC)
28. https://api.github.com/orgs/supermemoryai/repos?per_page=100 : 35 public repositories, names, descriptions, licences; only the repository of this page is described as an engine; `smfs` mentions a "sync engine" in a filesystem for agents; contents of the other repositories were not read (read 20261103 02:05 UTC)
29. https://web.archive.org/web/20260510052109/https://supermemory.ai/blog/we-broke-the-frontier-in-agent-memory-introducing-99-sota-memory-system/ : post dated 22 Mar 2026: "~85%" first report, ~99% experimental flow, "It was a parody", any-of-eight-variants scoring; also the 20260325 and 20260410 captures carry the same summary; the live URL answered HTTP 301 to `https://supermemory.ai/blog/` (read 20261103 02:14 UTC)
30. https://dev.to/gaurav_dadhich/the-state-of-ai-memory-in-2026-claimed-vs-observed-1n94 : post of 20260728 by a rival memory vendor ("Synap, our own product"); its results table is an image (alt text "ChatGPT Image May 27, 2026"), read as an image: SuperMemory 71.3% in the "Independent harness (pre-April-14)" column, vendor figure "not published" (read 20261103 02:15 UTC)

Further reading in the archive: [Supermemory entry](../../kb-kg/projects/supermemory.md). Papers: [agent memory group](../papers/agent-memory.md).
