---
type: project
repo: MemoriLabs/Memori
trends: [agent-memory]
updated: 20261103 02:21 UTC
---

# Memori

This page answers what Memori is, how its pipeline works, and who has measured it. Three points matter: the licence file is reworded Apache 2.0 [2][3]; extraction runs on the vendor's hosted service even when the results are stored in your own database [12][13]; and the high scores are the authors' own, while the one third-party run found, by a competitor, is far lower [16][20].

| Field | Value |
|---|---|
| Repository | https://github.com/MemoriLabs/Memori [1] |
| Licence | Not the standard Apache text; GitHub reports `NOASSERTION` [1][2]. The `LICENSE` file is Apache 2.0 reworded. Its terms are unchanged since 20250803 (the first commit holds an empty file; only the appendix copyright line differed, 20251109 to 20251202) [2][17]. Compared word by word with apache.org [3], it changes the copyright grant (adds "use" and "modify", drops "sublicense", and "in all media and formats whether now known or hereafter devised" replaces "in Source or Object form"), the "Work" and "Derivative Works" definitions (both exclude separate works that communicate with the Work solely through its public interfaces) and section 9 (retitled "Accepting Warranty or Support", no "While redistributing" condition), and rewords the "Licensor" definition and section 4(c). Sections 3 and 5 to 8 match. README, PyPI and npm say Apache 2.0 [4][6]. *Reading:* the text is not the standard one and GitHub's detector does not match it, so this archive treats the code as a read-only reference (ideas and results only) until the authors say which licence applies. That is a working rule, not legal advice. |
| Trends | [Agent memory](../trends/agent-memory.md) |

## What it is

Memori is [agent memory](../index/agent-memory.md) infrastructure from Memori Labs: an [LLM](../index/large-language-model.md)-agnostic layer that turns agent execution and conversation into persistent, structured state [1]. Python and TypeScript SDKs wrap an LLM client; a Rust core serves both [4][12]. Storage is Memori Cloud (hosted, an API key) or BYODB, your own database [4][11]. There is also an [MCP](../index/model-context-protocol.md) (Model Context Protocol) endpoint and plugins for OpenClaw and Hermes [4]. Nearest chapter pages:

| Project | Alike | Differs |
|---|---|---|
| [Mem0](mem0.md) | per-user fact extraction at write time, vector ranking, a hosted tier [4][9] | extraction is a hosted call here, a library call in Mem0's open-source code (its page) [12][13] |
| [Hindsight](hindsight.md) | extraction at write time, a hosted tier [4][13] | recall here is one vector search plus a BM25 re-rank over stored facts [12]; Hindsight fuses four strategies and consolidates in the background (its page); consolidation here: **unstated** |
| [Graphiti](graphiti.md) | a "knowledge graph" from conversations | triples with a mention count, no invalidation described [10]; recall ranks fact text and does not query the triples [12][13] |

## How it works

**Capture and scope.** `llm.register(client)` wraps the provider client and every call is captured. Memories are scoped by entity (user), process (agent) and session [4][9].

**Write.** In the background, "Advanced Augmentation" extracts facts, preferences, skills, process attributes, [semantic triples](../index/triple.md) ([named-entity recognition](../index/named-entity-recognition.md), deduplicated with a mention count) and conversation summaries (the README adds events, people, relationships and rules) [4][9][10][13][16]. The extraction model is **unstated**.

*Where the call goes.* In BYODB mode (a database connection passed to `Memori`), the code at `main` (574b1ea) posts the call's conversation messages in plain text, with SHA-256-hashed entity and process IDs, to `https://api.memorilabs.ai/v1/sdk/augmentation` and writes the reply to the local database [12][13]. The Rust core makes the call by default (`core/src/network/client.rs`; it is on unless `MEMORI_DISABLE_RUST_CORE`, `MEMORI_USE_RUST_CORE` or the `use_rust_core` argument turns it off). With it off, Python makes the same call (`memori/_network.py`); the TypeScript SDK uses the Rust engine. Only the base URL can be redirected (`MEMORI_API_URL_BASE`, or Python's `base_url`); no setting that turns the call off was found. Without an account the call is rate-limited; a free key gives an Advanced Augmentation quota of 5,000 a month [4][11].

*What the docs say.* The BYODB architecture page says "All data stays on your infrastructure" [11]. No file under `docs/` (85 read) names `sdk/augmentation`, and the BYODB pages do not say conversation text is sent out; the Cloud architecture page says each call "is captured and sent to Memori Cloud" [9][11]. What the vendor keeps is **unstated**. *Reading:* taken literally, the architecture sentence does not match the code, since the messages leave the machine; it holds if "data" means stored data. The BYODB index page's narrower "no third-party storage" cannot be tested from the code.

**Read.** In the open-source core, before each call Memori scores up to 1,000 of the entity's most recently seen fact embeddings (SQLite driver read) against the query by cosine similarity, re-ranks them with [BM25](../index/bm25.md) at 0.85 cosine and 0.15 lexical weight (0.70 and 0.30 for queries of two tokens or fewer after stop-word removal), and injects the top 5 facts above a 0.1 threshold (defaults) into the system prompt. The triples are not queried [12][13]. The hosted recall engine is **unstated**. The docs promise "intelligent ranking and decay"; the ranking code has no decay term, only that recency cut-off [9][11][12][13]. The `Memori` class has no per-fact edit or delete; `delete_entity_memories` (BYODB) removes all of one entity's facts and triples [13].

## Evidence

Every score below is published; none was reproduced here.

| Run | [LoCoMo](../datasets/locomo.md) | [LongMemEval](../datasets/longmemeval.md) | Who ran it |
|---|---|---|---|
| Paper, v1, 20260320 | 81.95 (1,294 tokens) [19] | not reported | Memori Labs: first-party |
| Website results page and README | 87.0 (721 tokens) [4][16] | not reported | Memori Labs: first-party |
| OmniMemEval results page | 41.34 [20] | 20.80 [20] | MemTensor, maker of [MemOS](memos.md) |

**First-party, paper.** All five authors are at Memori Labs Inc.; the arXiv comment reads "white paper". Answers and judging use GPT-4.1-mini, Memori's score averages three runs and the adversarial category is excluded [18][19]. Table 1's caption says the baselines (Zep, LangMem, Mem0) were "retrieved from Du et al. (2025)", another paper, while section 3.6 says official implementations were used; no versions are given. Table 2's Mem0, Zep and full-context rows come from the Mem0 paper (Chhikara et al., 2025) [19].

**First-party, website and README.** A commit of 20260728, "New LoCoMo benchmark numbers and plots to latest results", replaced the Memori row and token figures; the baseline rows are unchanged [7][16]. What changed since 81.95 is **unstated**; the arXiv paper still carries 81.95 [16][18][19]. The README's "roughly 67% vs. Zep" is the paper's old saving; the docs say 82% [4][16][19]. The `benchmarks` notebooks download extracted memories ready-made and embed with EmbeddingGemma-300M, not the default all-MiniLM-L6-v2, so they do not run the hosted extraction [11][12][15].

**Independent, with a stake of its own.** OmniMemEval, run by MemTensor, scores Memori's cloud service at 41.34% on LoCoMo (1,540 questions, GPT-4.1-mini answers, GPT-4o-mini judge) and 20.80% on LongMemEval; MemOS tops both columns [20]. Its adapters follow public documentation and are not claimed optimal; the Memori one targets SDK v3.3.2 and the run date is **unstated** [20][21]. Mnemon (20260928) reuses the numbers [22]. Of ten systems with a published and a reproduced LoCoMo score, nine fall (Letta rises); Memori's drop from the 81.95 reference row, 40.6 points, is the second largest [20] (computed). *Reading:* a lead, not a verdict. The judge and retrieval path differ from the authors' (hosted recall against their local index), a competitor wrote the adapter, and the LongMemEval categories are uneven (84.14 on single-session-user, 1.79 on single-session-assistant), which leaves a set-up cause open [19][20][21].

**None found otherwise.** A run by authors with no stake in the result: none found, 20261103. Of 44 papers whose full text was searched for "Memori", four only cite or describe the paper and one repeats the OmniMemEval row [22][23]. Web searches (leads only) found no reproduction.

## Status and direction

*Release.* `v3.3.6`, 20260528, is GitHub's latest of 38; PyPI also ends at 3.3.6 [5][6]. `pyproject.toml` on `main` has read 3.3.7 since 20260610, unreleased [14].

*Activity in the last 90 days.* 3 commits to `main` from 20260805 to 20261103 (two README edits to the Enterprise section, one CI fix; the last on 20260918); by month since March: 64, 53, 91, 17, 2, 1, 2, then none in October [7]. All five pull requests merged since July come from one account [8]. Of 30 open pull requests (and 22 issues), GitHub marks none as from an owner or member and 22 as from accounts with no prior association; the newest is from 20261031 [8]. A branch, `feat/enterprise-docs`, is 75 commits ahead of `main` (20260731 to 20261003), adds a `docs/memori-enterprise/` section and is not merged [24].

*Direction.* The README leads with Memori Cloud and has an Enterprise section; the extraction service is not in the repository file tree [4][12]. There is no roadmap file; the BYODB docs index has a "Roadmap" line: "Support for Hermes Agent BYODB Implementation; Support for OpenClaw BYODB Implementation; Turbo-charging Advanced Augmentation; Exciting optimizations to Agent-Native Recall" [11]. *Reading:* `main` has been close to idle since July (5 commits in four months, no release since 20260528) and outside pull requests wait unmerged, while recent visible work is README and Enterprise documentation, mostly on an unmerged branch [7][8][24]. That fits maintenance mode for the open code with effort on the hosted product, a shape like [open-core](../index/open-core.md); the cause is **unstated**, and "dormant" would overstate it. Work in private repositories is **unstated**.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)

**Projects**

- [Projects](README.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/MemoriLabs/Memori : repository metadata, description, creation date, archived flag, GitHub licence classification NOASSERTION (read 20261103 02:02 UTC)
2. https://api.github.com/repos/MemoriLabs/Memori/license : text of the `LICENSE` file at `main` (read 20261103 02:02 UTC)
3. https://www.apache.org/licenses/LICENSE-2.0.txt : reference text for the word-level comparison, redone with a word diff of sections 1 to 9 and the appendix (read 20261103 02:02 UTC)
4. https://api.github.com/repos/MemoriLabs/Memori/readme : tagline, Cloud and BYODB, MCP and plugins, extraction types, 87% and 721 tokens, "roughly 67% vs. Zep", Cloud and Enterprise emphasis, rate-limit wording, licence line (read 20261103 02:03 UTC)
5. https://api.github.com/repos/MemoriLabs/Memori/releases?per_page=100 : 38 releases, latest `v3.3.6` with its date (read 20261103 02:09 UTC)
6. https://pypi.org/pypi/memori/json and https://registry.npmjs.org/@memorilabs/memori : latest PyPI version and upload time, licence fields (read 20261103 02:09 UTC)
7. https://api.github.com/repos/MemoriLabs/Memori/commits?sha=main : 230 commits on `main` since 20260301, monthly counts, subjects, authors, last commit (574b1ea, 20260918); the 20260728 commit (6c126655) with its message and diff of the README and benchmark pages (read 20261103 02:09 UTC; the 20260728 diff 02:10 UTC)
8. https://api.github.com/search/issues?q=repo:MemoriLabs/Memori+is:pr+is:open (and the matching queries for open issues and for merged pull requests since 20260701) : counts, author association, authors, dates (read 20261103 02:13 UTC)
9. https://github.com/MemoriLabs/Memori/tree/main/docs/memori-cloud/concepts : `architecture.mdx` ("is captured and sent to Memori Cloud", "ranking and decay") and `how-memory-works.mdx` (attribution, memory types, recall steps) (read 20261103 02:06 UTC)
10. https://github.com/MemoriLabs/Memori/tree/main/docs/memori-cloud/concepts : `advanced-augmentation.mdx` and `knowledge-graph.mdx` (extraction types, triples, mention count, per-entity scope; no invalidation or supersession wording) (read 20261103 02:06 UTC)
11. https://github.com/MemoriLabs/Memori/tree/main/docs/memori-byodb : `concepts/architecture.mdx` ("All data stays on your infrastructure", "ranking and decay"), `concepts/advanced-augmentation.mdx` (fastembed all-MiniLM-L6-v2), `support/faq.mdx` and `support/troubleshooting.mdx` (5,000 a month with a free key), `index.mdx` ("no third-party storage", the Roadmap line); the live page memorilabs.ai/docs/memori-byodb/concepts/architecture carries the same sentence (read 20261103 02:06 UTC; live page 02:15 UTC)
12. https://github.com/MemoriLabs/Memori/tree/main/core : `README.md`, `src/search/api.rs`, `src/search/lexical.rs`, `src/embeddings/models.rs`, `src/retrieval/pipeline.rs`, `src/augmentation/pipeline.rs`, `src/augmentation/models.rs`, `src/network/client.rs`, `src/lib.rs`, `bindings/python/src/lib.rs` (cosine plus BM25 blend and weights, default embedder, post to `sdk/augmentation` with hashed IDs and the base URL from `MEMORI_API_URL_BASE`; the mock flag defaults to false); and the repository file tree, which shows no roadmap or `NOTICE` file and no server code for the augmentation service (read 20261103 02:04 UTC to 02:08 UTC)
13. https://github.com/MemoriLabs/Memori/tree/main/memori : `_network.py`, `_config.py`, `__init__.py`, `memory/augmentation/_handler.py`, `memory/augmentation/augmentations/memori/_augmentation.py`, `native/_adapter.py`, `memory/recall.py`, `llm/pipelines/recall_injection.py`, `storage/drivers/sqlite/_driver.py`, and `memori-ts/src/engines/augmentation.ts` (BYODB turns go to the Rust engine or, with it off, to the hosted `sdk/augmentation` endpoint; Rust core on by default; recall reads facts only; `delete_entity_memories`; 1,000 most recent fact embeddings; limit 5 and threshold 0.1) (read 20261103 02:04 UTC to 02:08 UTC)
14. https://github.com/MemoriLabs/Memori/blob/main/pyproject.toml and its commit list : version 3.3.7, set by the commit of 20260610 (read 20261103 02:04 UTC; commit list 02:13 UTC)
15. https://github.com/MemoriLabs/Memori/tree/main/benchmarks : `README.md` and `01_load_indexes.ipynb` (downloaded memories, EmbeddingGemma-300M, FAISS plus BM25, GPT-4.1-mini) (read 20261103 02:04 UTC to 02:07 UTC)
16. https://github.com/MemoriLabs/Memori/tree/main/docs/memori-cloud/benchmark : `overview.mdx`, `results.mdx`, `experiments.mdx` (87.0 row, baseline rows, token table, "82% fewer tokens", setup) (read 20261103 02:06 UTC)
17. https://api.github.com/repos/MemoriLabs/Memori/commits?path=LICENSE : the four commits of the `LICENSE` file and its text at each (raw file at each commit), compared word by word with the current text (read 20261103 02:04 UTC)
18. https://arxiv.org/abs/2603.19935 and the arXiv API record : Borro, Macarini, Tindall, Montero, Struck, "Memori: A Persistent Memory Layer for Efficient, Context-Aware LLM Agents", one version, 20260320, comment "9 pages; 2 figures; white paper" (read 20261103 02:10 UTC)
19. https://arxiv.org/html/2603.19935 : affiliations, Tables 1 and 2 with captions, section 3.6, GPT-4.1-mini, three runs, adversarial exclusion, no baseline versions (read 20261103 02:10 UTC)
20. https://github.com/MemTensor/OmniMemEval/blob/main/docs/user_memory/results.md : setup, Memori rows, published-reference row, adapter disclaimer, other systems' scores (read 20261103 02:10 UTC)
21. https://github.com/MemTensor/OmniMemEval/blob/main/scripts/client_factory/memori_client.py : Memori adapter, "aligned with SDK v3.3.2" (read 20261103 02:10 UTC)
22. https://arxiv.org/html/2609.36059 : Mnemon (20260928), Table 1 with the Memori row (41.34, 20.8) taken from OmniMemEval's published numbers (read 20261103 02:11 UTC)
23. https://arxiv.org/html/ followed by each identifier: 2608.02613, 2609.05339, 2608.15008 and 2605.11325 (cite or describe the Memori paper, no Memori result); 2610.30755, 2610.34073, 2606.24775, 2507.05257, 2610.29823, 2608.11879, 2608.13883, 2608.29606, 2608.12365, 2604.20006, 2602.16313, 2606.18829, 2606.30306, 2609.23570, 2610.31303, 2610.27524, 2610.22196, 2610.34673, 2610.39790, 2609.08273, 2609.34227, 2610.26433, 2610.25179, 2610.09348, 2610.08586, 2610.41521, 2610.19472, 2610.23313, 2610.02002, 2610.05343, 2606.06036, 2607.21503, 2609.16053, 2609.03915, 2608.13334, 2606.29914, 2609.10413, 2608.12990, 2605.28969 (no match for "Memori"); with source 22 these are the 44 papers : whole-word search of each paper's text; candidates from an alphaXiv search, an arXiv API query and web-search leads (read 20261103 01:34 UTC to 01:38 UTC, then 02:11 UTC to 02:13 UTC)
24. https://api.github.com/repos/MemoriLabs/Memori/compare/main...feat/enterprise-docs and the repository activity feed : the branch is 75 commits ahead and 3 behind `main`, 20260731 to 20261003, adding `docs/memori-enterprise/`; pushes to it on 20260821 and 20261003 (read 20261103 02:14 UTC)

Further reading in the archive: [Memori, long entry](../../kb-kg/projects/memori.md).
