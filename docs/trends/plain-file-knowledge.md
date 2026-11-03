---
type: trend
shift: databases and indexes -> Markdown the model maintains
status: growing
order: 8
updated: 20261102 23:27 UTC
---

# Plain files as agent knowledge: from databases and indexes to Markdown the model maintains

This page answers one question: what changed when builders started to keep an agent's knowledge as ordinary Markdown files that a model writes and a person can read, instead of rows, vectors and graph nodes behind a service. It covers the family that grew from one April 2026 gist, the neighbouring practices that use the same medium, and what has been measured.

> **Distinctive because** the stored thing is human-readable pages that a [large language model](../index/large-language-model.md) (LLM) compiles once and keeps current, not extracted records in a store. The nearest neighbour is [agent memory](./agent-memory.md): [Mem0](../projects/mem0.md) stores extracted records [32]; here the files are the source of truth [5][6][9].

## Why it emerged

The trigger is dated. A gist titled "LLM Wiki", published under the GitHub account karpathy (an [LLM wiki](../index/llm-wiki.md)), was created on 20260404 at 16:25 UTC [1][2]. It starts from [retrieval-augmented generation](../index/retrieval-augmented-generation.md) as most people meet it, where the model "is rediscovering knowledge from scratch on every question", with "no accumulation" [1]. It proposes that the model instead "incrementally builds and maintains a persistent wiki" of linked Markdown files, so that knowledge is "compiled once and then kept current" [1].

*Reading:* two practices were already in place, though the gist cites neither. Anthropic's memory tool, announced 20250929, lets a model create, read, update and delete files in a directory the developer stores [14]; its [Agent Skills](../index/agent-skills.md), announced 20251016, are folders of instructions and resources [13]; on 20261022 Anthropic announced that it was donating the standard (its name and logo, the GitHub organization and the `agentskills.io` domain) to the Agentic AI Foundation, and states more than 70 agent platforms, 1 million published skills and nearly 280 million installs (Anthropic's own figures) [36]. The [AGENTS.md](../index/agents-md.md) convention, a "README for agents", is described at its own site, which gives no start date [12]. A December 2025 paper proposed a file-system abstraction for context [29]. The gist reuses one of these: its "schema" is a `CLAUDE.md` or `AGENTS.md` file [1]. No source read ties the gist's appearance to these practices.

The response was fast. Two papers dated 20260413 already describe it [15][16]; one says that "a visible cluster of personal wiki-style memory architectures emerged in April 2026", and lists Karpathy's design among them [15]. In the 20261030 GitHub snapshot, 48 matching repositories (name or description containing "wiki" or "karpathy", some unrelated to the gist) were created between 20260404 and 20260430; 20 had been pushed within 90 days and 28 had not [3]. *Reading:* a fashion that large and that fast also decays fast, so the 28 quiet repositories are as much part of the story as the 20 active ones.

Chapter 1 gives the older version of the problem. In the era of expert systems, [Knowledge systems: boom and bust](../history/knowledge-systems.md), knowledge was written by hand, and the history lists this as the [knowledge acquisition bottleneck](../index/knowledge-acquisition-bottleneck.md), left unsolved. What the history adds is that older problem, the cost of writing knowledge down, which a model-maintained wiki now tries to move from people to a model.

## Why it matters

A person can open, edit, diff and version the knowledge, and no database has to run. The gist notes that the wiki "is just a git repo of markdown files" [1]. For a builder, the cost shifts from every query to every ingest: the model pays once to integrate a source, and later questions read pages that already hold the cross-references [1]. *Reading:* the same properties raise questions that databases answer by design (size, concurrent edits, provenance), so this trend tests how far an index page and a file tree can go.

## How it works

The gist describes three layers and three operations [1].

- **Raw sources** stay immutable. **The wiki** is a directory of model-written pages. **The schema** is an instruction file such as `CLAUDE.md` or `AGENTS.md` that tells the model how to maintain the wiki [1].
- **Ingest:** the model reads a source and updates summary, entity and concept pages; one source "might touch 10-15 wiki pages" [1]. **Query:** the model searches the pages, reads them and answers with citations; good answers can be filed back as pages. **Lint:** the model checks for contradictions, stale claims and orphan pages [1].
- **`index.md`** catalogues every page with a one-line summary and is read first; **`log.md`** is an append-only record. The gist says the index "works surprisingly well at moderate scale (~100 sources, ~hundreds of pages)" and that "as the wiki grows you want proper search"; it names no threshold [1].

Two neighbours differ in who writes the stored thing. In [agent memory](./agent-memory.md), Mem0 extracts memories with one model call and retrieves them with vector or hybrid search [32], while in [Basic Memory](../projects/basic-memory.md), [Tigerless agent-memory](../projects/tigerless-agent-memory.md) and EverOS the files are the source of truth and the indexes are derived from them [5][6][9]. In [vectorless retrieval](./reasoning-over-structure.md) a model also reads an index and then opens pages, but [PageIndex](../projects/pageindex.md) extracts its tree "from the document layout without an LLM" (an LLM then summarizes the nodes) [33], and here the model writes the pages.

### Variation among projects

Projects differ on what the files are and how they are indexed (READMEs, last column).

| Project | What the files are | Index | README |
|---|---|---|---|
| [llm-wiki-nashsu](../projects/llm-wiki-nashsu.md) | A personal wiki a desktop app builds from documents | keyword search, with optional vector search (LanceDB) | [4] |
| [claude-obsidian](../projects/claude-obsidian.md) | Linked notes in an Obsidian vault, written by Claude Code skills | local [BM25](../index/bm25.md) search with optional reranking | [4] |
| [Basic Memory](../projects/basic-memory.md) | Markdown notes that "humans and LLMs both read and write" | a local SQLite index beside the files | [5] |
| [Tigerless agent-memory](../projects/tigerless-agent-memory.md) | Model-written memory files; the files are "the single source of truth" | a SQLite index that "you can delete at any time" | [6] |
| [OpenViking](../projects/openviking.md) | A virtual filesystem (`viking://`) with a generated summary per directory | summaries first, plus search | [7] |
| [Letta](../projects/letta.md) | Agent context tracked in git (MemFS) | unstated in the README read | [8] |

### LLM wikis

Five strands share the mechanism (the model reads or writes files instead of querying a store) and are not trends of their own. The first is the core above, with no founding paper: the source is the gist [1]. An arXiv keyword query for LLM-wiki wording (source 30) returns 21 results submitted from 20251102 to 20261102 against 0 in the year before [30]. That is a noisy keyword count, not a count of papers in the field.

### Context files

`AGENTS.md` describes itself as "a simple, open format for guiding coding agents" and is used, by its own count, by over 60k open-source projects [12]. A census of 22,854 popular GitHub repositories found agent instructions in 26.3% of them and in 59.6% of the most-starred [23]. These files are the hand-written end of the same medium. An arXiv keyword query for these file names (source 30) returns 59 results in the same window against 2 in the year before [30].

### Skills as procedural knowledge

A skill is a folder of instructions and resources that Claude "can load when needed" [13]. Letta's agents store skills in their own memory repository [8], and a paper (WikiSkill) compiles agent experience into a wiki that guides skill updates [25]. The files hold procedures, not facts, but the storage and the editing by a model are the same.

### Knowledge compilation in products

[Knowledge compilation](../index/knowledge-compilation.md) is a term used here: a model turns sources into reusable artifacts at ingestion. [RAGFlow](../projects/ragflow.md)'s README has a news line dated 2026-08-19: "Introduced Knowledge Compilation to generate Wikis, Graphs, Trees, PageIndex, Mind Maps, Timelines, and Skills" [11]. The wiki is one output among several.

### The Open Knowledge Format

The [Open Knowledge Format](../../kb-kg/projects/open-knowledge-format.md) (OKF) v0.2 specifies "a directory of markdown files with YAML frontmatter" with "no schema registry, no central authority, and no required tooling", and adds provenance, trust and lifecycle fields for knowledge that agents write [10]. It is a format, not a tool, and exists because many incompatible conventions are emerging, in the spec's words [10].

## Representative projects

Stars are a signal from the 20261030 19:54 UTC snapshot [3]. Licences, creation dates and releases were read from GitHub on 20261102 21:05 UTC [35].

| Project | Licence | Stars (20261030) | Note |
|---|---|---|---|
| [llm-wiki-nashsu](../projects/llm-wiki-nashsu.md) | GPL-3.0 text (GitHub reports no match) | 21,198 | read-only reference |
| [claude-obsidian](../projects/claude-obsidian.md) | MIT | 16,002 | created 20260407 |
| [Basic Memory](../projects/basic-memory.md) | AGPL-3.0 | 4,416 | created 20241202, so it predates the gist; read-only reference |
| [Tigerless agent-memory](../projects/tigerless-agent-memory.md) | MIT | 4,381 | created 20260901; no release |
| [Letta](../projects/letta.md) | Apache-2.0 | 25,294 | overlap case with agent memory; current code is in `letta-code` [8] |
| [OpenViking](../projects/openviking.md) | AGPL-3.0 | 41,197 | overlap case with agent memory; read-only reference |
| [EverOS](https://github.com/EverMind-AI/EverOS) | Apache-2.0 | 13,721 | "Markdown source of truth" with derived indexes [9] |
| [OKF](https://github.com/GoogleCloudPlatform/open-knowledge-format) | Apache-2.0 | 1,177 | specification [10] |

Letta and OpenViking are chiefly [agent memory](./agent-memory.md) projects; they appear here because their stored medium is files.

## Fundamental papers

No founding paper exists. The group page [Papers on plain-file knowledge](../papers/plain-file-knowledge.md) sets out the relations. The group page keeps one paper, Knowledge Compounding (2026); the papers this page rests on, named here, are in its further reading or not listed. They are Zhou and others on filesystem memory (arXiv 2607.26637) [17], Cochran's two preregistered comparisons (2605.18490, 2607.04576) [18][19], and Miteski's design paper (2604.12034) [15].

## What is measured, and by whom

Every quality figure in the projects' own READMEs is first-party. An earlier archive review found no independent run of any project on this page as of 20261030 [31]; this page did not repeat that search. Basic Memory's benchmark file (first-party) calls itself "Internal-only" and retrieval "near-parity": on [LongMemEval](../datasets/longmemeval.md)-60, recall@5 is 0.951 for Basic Memory, 0.979 for mem0 and 0.846 for grep, "a strong lexical baseline here" in the file's words [34]. Its answer accuracy favours Basic Memory (0.583 against 0.450 for mem0); the file's diagnostic puts that gap on the answering model, not on retrieval [34]. The studies below test the idea, not the projects.

| Study | Who | Result |
|---|---|---|
| Filesystem memory, 11 authors | relation to the projects unstated | organized stores "roughly halve retrieval cost where material is large"; "no agent we measure converts organization itself into better answers" [17] |
| Vector retrieval-augmented generation (RAG) against an LLM-compiled wiki, 13 questions over 24 papers, preregistered | one author | wiki better at connecting findings, but its organization advantage fell below the registered threshold with both judges combined; about 21 times more tokens per query; a decomposition-retrieval RAG variant closed most of the synthesis gap at lower cost; the winner depends on "the retrieval baseline, the scoring method, and the judge" [18] |
| Progressive disclosure on a 709-page wiki, preregistered | same author | answer quality held within a preset margin; cost fell [19] |
| Compilation quality, RepLiQA, 6,800 questions | the author of WiCER (first-party for the fix) | blind compilation scored 2.14 to 2.32 against 3.46 for raw context, a 53 to 60% catastrophic failure rate [20] |
| Four sequential queries on one wiki implementation | the implementation's authors (first-party) | 47K tokens against 305K for a matched RAG baseline [16] |
| BM25 and grep harness against structural artifacts | the RAGFlow team (first-party) | BM25/grep alone answers 85% of BrowseComp-Plus; artifacts gave "no detectable accuracy gain on FRAMES" [21] |
| Context files for coding agents | Gloaguen and others | no general gain on SWE-bench tasks (real software issues from GitHub projects); cost up over 20% [22]; a 288-run ablation (Khatri) finds no measurable effect [24] |

Three further studies find raw retrieval strong without any compiled structure: grep over vector retrieval on LongMemEval [26], raw-history RAG first in six of seven settings [27], and BM25 ahead of a file-exploring agent above about 10 million corpus tokens [28]. Their abstracts do not show authorship of any project named here. None tests a model-compiled wiki.

Experiment [X5, wiki size limit](../experiments/x5-wiki-size-limit.md) is the proposed test of the open question. Nothing has run.

## Assessment

*Reading:* the family answers a real complaint, that retrieval forgets, and the evidence for the benefit is thin. The one preregistered head-to-head shows a synthesis gain at a high token cost, and the winner depends on the retrieval baseline and the judge: a decomposition-retrieval RAG variant closed most of the gap at lower cost [18]. The multi-author study finds that organization buys cheaper search at scale but not better answers [17]. A vendor team whose product compiles wikis reports no accuracy gain from structure under a good harness [21]. Strengths: files are portable, inspectable and cheap to run. Weaknesses: quality depends on the compiling model, with blind compilation losing facts [20]; the studies are small and mostly single-author; the 709-page study varies how the agent reaches pages, not wiki against retrieval [19]; and no study compares a compiled wiki with plain retrieval at scale. Over the same window the keyword counts outgrew the controls: 59 against 2 for context files is x29.5 on a small base, against x1.38 (any LLM wording), x1.23 (any RAG wording) and x2.50 (LLM-agent wording); 21 against 0 for LLM wikis has no ratio [30]. Yet 28 of the 48 matching April repositories had not been pushed in 90 days at the snapshot [3]. Likely direction: the wiki becomes one artifact among several that products compile [11], with files as the interchange format [10].

## Signals to watch

- An independent run of any project above, on LongMemEval or [LoCoMo](../datasets/locomo.md).
- A size sweep of an index-only wiki, which X5 proposes.
- Whether the 20 active April repositories are still pushing at the next snapshot.
- OKF reaching a first release (its repository showed none on 20261102 21:05 [35]).
- Whether EverOS keeps Markdown as its source of truth [9], and how Letta's MemFS (git-tracked context) develops [8].

## Sources

Read times are UTC.

1. https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw : the gist's full text (read 20261102 21:03)
2. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f : account karpathy, creation time 2026-04-04T16:25:13Z (read 20261102 21:05)
3. kb-kg/landscape/20261030_1954-github/repos.tsv : stars, creation and push dates; the April count recomputed from the file (name or description matching "wiki" or "karpathy", created 20260404 to 20260430: 48, of which 20 pushed within 90 days and not archived); snapshot 20261030 19:54, file read 20261102 20:11
4. https://github.com/AgriciDaniel/claude-obsidian and https://github.com/nashsu/llm_wiki : READMEs, index of each (read 20261102 20:22)
5. https://github.com/basicmachines-co/basic-memory : README, files as the shared medium, SQLite index, "the source of truth is always your files" (read 20261102 21:04)
6. https://github.com/tigerless-labs/agent-memory : README, source of truth and deletable cache (read 20261102 21:04)
7. https://github.com/volcengine/OpenViking : README, virtual filesystem and directory summaries (read 20261102 20:22)
8. https://github.com/letta-ai/letta and https://github.com/letta-ai/letta-code : READMEs, current code location, git-tracked context, skills in memory (letta-code read 20261102 21:03; letta read 20261102 20:22)
9. https://github.com/EverMind-AI/EverOS : README, Markdown as source of truth, SQLite and LanceDB indexes synced from it (read 20261102 21:04)
10. https://github.com/GoogleCloudPlatform/open-knowledge-format : README and SPEC.md v0.2 (read 20261102 20:22)
11. https://github.com/infiniflow/ragflow : README, Knowledge Compilation entry of 2026-08-19 (read 20261102 20:22)
12. https://agents.md : the AGENTS.md convention and its stated use (read 20261102 20:22)
13. https://claude.com/blog/skills : Agent Skills announcement, 20251016 (read 20261102 20:22)
14. https://claude.com/blog/context-management : memory tool announcement, 20250929 (read 20261102 20:22)
15. https://arxiv.org/abs/2604.12034 : Miteski, "Memory as Metabolism", v1 20260413 (abstract read 20261102 21:06)
16. https://arxiv.org/abs/2604.11243 : Wen and Ku, "Knowledge Compounding", v1 20260413 (abstract read 20261102 20:23)
17. https://arxiv.org/abs/2607.26637 : Zhou and others (11 authors), "Filesystem-Based Memory for LLM Agents", v1 20260729 (abstract read 20261102 21:06)
18. https://arxiv.org/abs/2605.18490 : Cochran, "Single-Round Vector RAG vs an LLM-Compiled Wiki", v1 20260518; the abstract read is that of v3, 20261002 (read 20261102 21:03)
19. https://arxiv.org/abs/2607.04576 : Cochran, "Progressive Disclosure for LLM-Maintained Wiki Knowledge Bases", v1 20260706 (abstract read 20261102 20:23)
20. https://arxiv.org/abs/2605.07068 : Huerta, "WiCER", v1 20260508 (abstract read 20261102 20:23)
21. https://arxiv.org/abs/2610.41172 : Yu and others (18 authors), "Context as Infrastructure", v1 20261030, RAGFlow team (abstract read 20261102 20:23)
22. https://arxiv.org/abs/2602.11988 : Gloaguen and others (5 authors), "Evaluating AGENTS.md", v1 20260212 (abstract read 20261102 20:24)
23. https://arxiv.org/abs/2610.31715 : Zarzycki, census of AGENTS.md and CLAUDE.md, v1 20261022 (abstract read 20261102 20:24)
24. https://arxiv.org/abs/2607.27250 : Khatri, context-file ablation, v1 20260728 (abstract read 20261102 20:24)
25. https://arxiv.org/abs/2608.27454 : Tang and others (6 authors), "WikiSkill", v1 20260827 (abstract read 20261102 20:23)
26. https://arxiv.org/abs/2605.15184 : Sen and others (5 authors), "Is Grep All You Need?", v1 20260514 (abstract read 20261102 21:06)
27. https://arxiv.org/abs/2610.30755 : Bao and others (6 authors), "Is Complex Agentic Memory Always Needed?", v1 20261022 (abstract read 20261102 20:23)
28. https://arxiv.org/abs/2607.26497 : Wang and others (8 authors), "BM25 Wins at Scale", v1 20260729 (abstract read 20261102 20:23)
29. https://arxiv.org/abs/2512.05470 : Xu and others (6 authors), "Everything is Context", v1 20251205 (abstract read 20261102 20:23)
30. arXiv API keyword counts by submission date, window 20251102 to 20261102 against 20241102 to 20251101 (the earlier window replaces the date range in the `submittedDate` clause with `[202411020000 TO 202511012359]`). q1, LLM-wiki wording: https://export.arxiv.org/api/query?search_query=%28%28abs%3A%22LLM%20wiki%22%20OR%20abs%3A%22LLM-wiki%22%20OR%20abs%3A%22LLM-maintained%20wiki%22%20OR%20abs%3A%22LLM-compiled%20wiki%22%20OR%20abs%3A%22LLM-built%20wiki%22%20OR%20abs%3A%22LLM-curated%20wiki%22%20OR%20abs%3A%22wiki-based%20memory%22%20OR%20ti%3Awiki%29%20AND%20%28abs%3ALLM%20OR%20abs%3Aagent%20OR%20abs%3Aagents%29%29%20AND%20submittedDate%3A%5B202511020000%20TO%20202611022359%5D&max_results=1 : 21 against 0 (read 20261102 21:07). q2, context-file wording: https://export.arxiv.org/api/query?search_query=%28abs%3A%22AGENTS.md%22%20OR%20abs%3A%22CLAUDE.md%22%20OR%20abs%3Acursorrules%20OR%20abs%3A%22context%20files%22%20OR%20abs%3A%22instruction%20files%22%20OR%20ti%3A%22context%20files%22%20OR%20ti%3A%22AGENTS.md%22%29%20AND%20submittedDate%3A%5B202511020000%20TO%20202611022359%5D&max_results=1 : 59 against 2 (read 20261102 21:07). The control ratios used in the Assessment (any LLM wording x1.38, any RAG wording x1.23, LLM-agent wording x2.50, same windows; query strings unstated) are carried over from the earlier research behind plans/20261102_1951-docs-catalogue.md (read 20261102 19:26 to 19:47)
31. https://github.com/basicmachines-co/basic-memory : the archive's finding that no independent evaluation of the projects was found (read 20261030, via the archive page kb-kg/directions/plain-files-and-wikis.md)
32. https://github.com/mem0ai/mem0 : README, single-pass ADD-only extraction and hybrid search (read 20261102 20:26)
33. https://github.com/VectifyAI/PageIndex : README, model recommendations: tree extracted from the layout without an LLM, index model summarizes and refines it (read 20261102 21:03)
34. https://github.com/basicmachines-co/basic-memory/blob/main/benchmarks/benchmarks/results/matrix-v2-summary.md : Basic Memory's internal benchmark matrix v2, retrieval and answer-accuracy tables, diagnostic and caveats; first-party (read 20261102 21:03)
35. GitHub API, license endpoints: https://api.github.com/repos/nashsu/llm_wiki/license https://api.github.com/repos/AgriciDaniel/claude-obsidian/license https://api.github.com/repos/basicmachines-co/basic-memory/license https://api.github.com/repos/tigerless-labs/agent-memory/license https://api.github.com/repos/letta-ai/letta/license https://api.github.com/repos/volcengine/OpenViking/license https://api.github.com/repos/EverMind-AI/EverOS/license https://api.github.com/repos/GoogleCloudPlatform/open-knowledge-format/license : licence of each LICENSE file (for nashsu/llm_wiki the file text is the GNU GPL, GitHub reports no match). Repository records: https://api.github.com/repos/nashsu/llm_wiki https://api.github.com/repos/AgriciDaniel/claude-obsidian https://api.github.com/repos/basicmachines-co/basic-memory https://api.github.com/repos/tigerless-labs/agent-memory https://api.github.com/repos/letta-ai/letta https://api.github.com/repos/volcengine/OpenViking https://api.github.com/repos/EverMind-AI/EverOS https://api.github.com/repos/GoogleCloudPlatform/open-knowledge-format : creation dates. Latest-release endpoints (the releases/latest path of the same repositories) : releases present for all but tigerless-labs/agent-memory and GoogleCloudPlatform/open-knowledge-format, which return Not Found (read 20261102 21:05 to 21:08)
36. https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation : Anthropic, 22 Oct 2026: donating Agent Skills to the Agentic AI Foundation; what is transferred; adoption figures (first-party) (read 20261102 22:32 UTC)
