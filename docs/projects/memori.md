---
type: project
repo: MemoriLabs/Memori
trends: [agent-memory]
updated: 20261103 01:49 UTC
---

# Memori

This page answers what Memori is, how its pipeline works, and who has measured it. Three points matter: the licence file is reworded Apache 2.0 [2][3]; extraction runs on the vendor's hosted service even when the data sits in your own database [12][13]; and the high scores are the authors' own, while the one third-party run found is far lower [16][20].

| Field | Value |
|---|---|
| Repository | https://github.com/MemoriLabs/Memori [1] |
| Licence | Not the standard Apache text. GitHub reports `NOASSERTION` [1][2]. The `LICENSE` file is Apache License 2.0 reworded, in this form since 20250803 apart from a one-word variant from 20251109 to 20251202 [2][17]. Against apache.org [3] it differs in the copyright grant (it omits "sublicense"), the "Work" and "Derivative Works" definitions (separate works that use only public interfaces are excluded), section 9 (no "While redistributing" condition) and minor rewordings; sections 3 and 5 to 8 match. README, PyPI and npm say Apache 2.0 [4][6]. A reading, not legal advice: until the project's authors clarify it, treat the code as a read-only reference, ideas and results only. |
| Trends | [Agent memory](../trends/agent-memory.md) |

## What it is

Memori is [agent memory](../index/agent-memory.md) infrastructure from Memori Labs: an [LLM](../index/large-language-model.md)-agnostic layer that turns agent execution and conversation into persistent, structured state [1]. Python and TypeScript SDKs wrap an LLM client; a Rust core serves both [4][12]. Storage is Memori Cloud (hosted, an API key) or BYODB, your own database [4][11]. There is also an [MCP](../index/model-context-protocol.md) (Model Context Protocol) endpoint and plugins for OpenClaw and Hermes [4]. Nearest chapter pages:

| Project | Alike | Differs |
|---|---|---|
| [Mem0](mem0.md) | per-user fact extraction at write time, vector ranking, a hosted tier [4][9] | extraction is a hosted call here, a library call in Mem0's open-source code (its page) [12][13] |
| [Hindsight](hindsight.md) | background extraction, a hosted tier | one vector search plus a BM25 re-rank over one fact store [12]; no consolidation step described: **unstated** |
| [Graphiti](graphiti.md) | a "knowledge graph" from conversations | triples with a mention count; no invalidation described [10] |

## How it works

**Capture and scope.** `llm.register(client)` wraps the provider client and every call is captured. Memories are scoped by entity (user), process (agent) and session [4][9].

**Write.** In the background, "Advanced Augmentation" extracts facts, preferences, skills, process attributes, [semantic triples](../index/triple.md) ([named-entity recognition](../index/named-entity-recognition.md), deduplicated with a mention count) and conversation summaries [9][10][16]. In BYODB mode the Python and Rust code post the conversation, with hashed entity and process IDs, to the vendor's `sdk/augmentation` endpoint unless a base URL is set, and write the reply to the local database [12][13]. Without an account extraction is rate-limited; a free key gives 5,000 a month [4][11]. The BYODB page nonetheless says "All data stays on your infrastructure" [11]. The extraction model is **unstated**.

**Read.** In the open-source core, before each call Memori scores the entity's stored fact embeddings against the query by cosine similarity, re-ranks the candidates with [BM25](../index/bm25.md) at 0.85 cosine and 0.15 lexical weight (0.70 and 0.30 for queries of two tokens or fewer), and injects the top facts into the system prompt [9][12]. The hosted recall engine's internals are **unstated**. The docs promise "intelligent ranking and decay"; the ranking code read has no decay term [9][12]. No update or delete of a stored fact is described in the concept pages read: **unstated**.

## Evidence

Every score below is published; none was reproduced here.

| Run | [LoCoMo](../datasets/locomo.md) | [LongMemEval](../datasets/longmemeval.md) | Who ran it |
|---|---|---|---|
| Paper, v1, 20260320 | 81.95 (1,294 tokens) [19] | not reported | Memori Labs: first-party |
| Website results page and README | 87.0 (721 tokens) [4][16] | not reported | Memori Labs: first-party |
| OmniMemEval results page | 41.34 [20] | 20.80 [20] | MemTensor, maker of [MemOS](memos.md) |

**First-party, paper.** All five authors are at Memori Labs Inc.; answers and judging use GPT-4.1-mini, Memori's score averages three runs and the adversarial category is excluded [19]. Table 1's caption says its baseline rows (Zep, LangMem, Mem0) were "retrieved from Du et al. (2025)", another paper, while section 3.6 says official implementations were used; no versions are given [19].

**First-party, website and README.** A commit of 20260728 changed the README and the benchmark pages [7][16]. They now give 87.0 with the baseline rows unchanged; what changed from 81.95 is **unstated**, and the arXiv paper still carries 81.95 [16][18][19]. The README's "roughly 67% vs. Zep" is the paper's old saving; the docs say 82% [4][16][19]. The `benchmarks` notebooks download the extracted memories ready-made and embed with EmbeddingGemma-300M, not the default all-MiniLM-L6-v2, so extraction cannot be reproduced from the repository [11][12][15].

**Independent, with a stake of its own.** OmniMemEval, run by MemTensor, scores Memori's cloud service at 41.34% on LoCoMo (1,540 questions, GPT-4.1-mini answers, GPT-4o-mini judge) and 20.80% on LongMemEval; MemOS leads that table [20]. Its adapters follow public documentation and are not claimed optimal; the Memori one targets SDK v3.3.2 and its run date is **unstated** [20][21]. Mnemon (20260928) copies the row [22]. Nine of the ten systems with both a published and a reproduced LoCoMo score fall in this harness (Letta's rises); Memori's drop, 40.6 points, is the second largest [20] (computed). *Reading:* a lead, not a verdict: the judge and the retrieval path differ from the authors' (hosted recall against their local index), and a competitor wrote the adapter [19][20][21].

**None found otherwise.** A run by authors with no stake in the result: none found, 20261103. Of 26 papers searched for "Memori", two only cite the paper and one repeats the OmniMemEval row [22][23].

## Status and direction

*Release.* `v3.3.6`, 20260528, is GitHub's latest of 38; PyPI also ends at 3.3.6 [5][6]. `pyproject.toml` on `main` has read 3.3.7 since 20260610, unreleased [14].

*Activity in the last 90 days.* 3 commits to `main` from 20260804 to 20261103 (two README edits to the Enterprise section, one fix; the last on 20260918). By month since March: 64, 53, 91, 17, 2, 1, 2, then none in October [7]. 30 pull requests and 22 issues are open; no open pull request comes from an owner or member [8].

*Direction.* The README leads with Memori Cloud and has an Enterprise section; the extraction service behind them is not in the repository [4][12]. Roadmap: **unstated** [12]. *Reading:* the open repository is nearly dormant while the hosted product is promoted, a pattern like [open-core](../index/open-core.md). Work in private repositories is **unstated**.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)

**Projects**

- [Projects](README.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/MemoriLabs/Memori : repository metadata, description, creation date, archived flag, GitHub licence classification NOASSERTION (read 20261103 01:30 UTC)
2. https://api.github.com/repos/MemoriLabs/Memori/license : text of the `LICENSE` file (read 20261103 01:30 UTC)
3. https://www.apache.org/licenses/LICENSE-2.0.txt : reference text for the word-level comparison (read 20261103 01:30 UTC)
4. https://api.github.com/repos/MemoriLabs/Memori/readme : tagline, Cloud and BYODB, MCP and plugins, 87% and 721 tokens, "roughly 67% vs. Zep", Cloud and Enterprise emphasis, rate-limit wording, licence line (read 20261103 01:31 UTC)
5. https://api.github.com/repos/MemoriLabs/Memori/releases?per_page=100 : 38 releases, latest `v3.3.6` with its date (read 20261103 01:31 UTC)
6. https://pypi.org/pypi/memori/json and https://registry.npmjs.org/@memorilabs/memori : latest PyPI version and upload time, licence fields (read 20261103 01:31 UTC)
7. https://api.github.com/repos/MemoriLabs/Memori/commits?since=2026-03-01T00:00:00Z : 230 commits on `main`, monthly counts, subjects, last commit; the 20260728 commit lists the README, benchmark pages and plots as changed (read 20261103 01:31 UTC; the 20260728 file list 01:44 UTC)
8. https://api.github.com/search/issues?q=repo:MemoriLabs/Memori+is:pr+is:open (and the matching query for issues) : open counts, author association (read 20261103 01:40 UTC)
9. https://github.com/MemoriLabs/Memori/tree/main/docs/memori-cloud/concepts : `architecture.mdx` and `how-memory-works.mdx` (attribution, memory types, recall steps, default limit and threshold, "ranking and decay") (read 20261103 01:32 UTC)
10. https://github.com/MemoriLabs/Memori/tree/main/docs/memori-cloud/concepts : `advanced-augmentation.mdx` and `knowledge-graph.mdx` (extraction types, triples, mention count, per-entity scope) (read 20261103 01:32 UTC)
11. https://github.com/MemoriLabs/Memori/tree/main/docs/memori-byodb : `concepts/architecture.mdx`, `concepts/advanced-augmentation.mdx`, `support/faq.mdx` ("All data stays on your infrastructure", fastembed all-MiniLM-L6-v2, 5,000 a month with a free key) (read 20261103 01:32 UTC; FAQ 01:35 UTC)
12. https://github.com/MemoriLabs/Memori/tree/main/core : `README.md`, `src/search/api.rs`, `src/search/lexical.rs`, `src/embeddings/models.rs`, `src/retrieval/pipeline.rs`, `src/augmentation/pipeline.rs`, `src/network/client.rs` (cosine plus BM25 blend and weights, default embedder, post to `sdk/augmentation` with hashed IDs); and the repository file tree, which shows no roadmap or `NOTICE` file (read 20261103 01:32 UTC to 01:36 UTC)
13. https://github.com/MemoriLabs/Memori/tree/main/memori : `_network.py` and `memory/augmentation/augmentations/memori/_augmentation.py` (Python SDK posts to the hosted `sdk/augmentation` endpoint unless a base URL is set) (read 20261103 01:35 UTC)
14. https://github.com/MemoriLabs/Memori/blob/main/pyproject.toml and its commit list : version 3.3.7, set by the commit of 20260610 (read 20261103 01:35 UTC)
15. https://github.com/MemoriLabs/Memori/tree/main/benchmarks : `README.md` and `01_load_indexes.ipynb` (downloaded memories, EmbeddingGemma-300M, FAISS plus BM25, GPT-4.1-mini) (read 20261103 01:35 UTC)
16. https://github.com/MemoriLabs/Memori/tree/main/docs/memori-cloud/benchmark : `overview.mdx`, `results.mdx`, `experiments.mdx` (87.0 row, baseline rows, token table, "82% fewer tokens", setup) (read 20261103 01:32 UTC)
17. https://api.github.com/repos/MemoriLabs/Memori/commits?path=LICENSE : the four commits of the `LICENSE` file and its text at each, compared with the current text (read 20261103 01:40 UTC)
18. https://arxiv.org/abs/2603.19935 : Borro, Macarini, Tindall, Montero, Struck, "Memori: A Persistent Memory Layer for Efficient, Context-Aware LLM Agents", one version, 20260320 (read 20261103 01:33 UTC)
19. https://arxiv.org/html/2603.19935 : affiliations, Tables 1 and 2 with captions, section 3.6, GPT-4.1-mini, three runs, adversarial exclusion, no baseline versions (read 20261103 01:33 UTC)
20. https://github.com/MemTensor/OmniMemEval/blob/main/docs/user_memory/results.md : setup, Memori rows, published-reference row, adapter disclaimer, other systems' scores (read 20261103 01:39 UTC)
21. https://github.com/MemTensor/OmniMemEval/blob/main/scripts/client_factory/memori_client.py : Memori adapter, "aligned with SDK v3.3.2" (read 20261103 01:39 UTC)
22. https://arxiv.org/html/2609.36059 : Mnemon (20260928), Table 1 with the Memori row taken from OmniMemEval (read 20261103 01:38 UTC)
23. https://arxiv.org/html/ followed by each identifier: 2608.02613 and 2609.05339 (cite the Memori paper, no Memori result); 2610.30755, 2610.34073, 2606.24775, 2507.05257, 2610.29823, 2608.11879, 2608.13883, 2608.29606, 2608.12365, 2604.20006, 2602.16313, 2606.18829, 2606.30306, 2609.23570, 2610.31303, 2610.27524, 2610.22196, 2610.34673, 2610.39790, 2609.08273, 2609.34227, 2610.26433, 2610.25179 (no match for "Memori"); with source 22 these are the 26 papers : whole-word search of each paper's text (read 20261103 01:34 UTC to 01:38 UTC)

Further reading in the archive: [Memori, long entry](../../kb-kg/projects/memori.md).
