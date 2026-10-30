---
slug: microsoft-graphrag
repo: microsoft/graphrag
tier: deep
category: core
snapshot: 20261030 18:58 UTC
---

# Microsoft GraphRAG (and LazyGraphRAG)

First investigated 20260725 15:33 UTC (release v3.1.1). Re-read against the live repository on
20261030 (release v3.3.0). Where the July text was wrong or is now stale, the body below carries the
corrected statement and the last section lists each correction.

| | |
|---|---|
| Repository | https://github.com/microsoft/graphrag |
| Licence | MIT. The `LICENSE` file reads "MIT License, Copyright (c) Microsoft Corporation" and GitHub's licence field agrees [1][2]. The README carries no licence badge [4]. |
| Language | Python [1] |
| Stars, forks | 36,498 stars, 3,868 forks (20261030 18:58 UTC) [1] |
| Created, last push | 20240327 17:57 UTC, 20261029 16:25 UTC. The last push touched some branch: the newest commit on `main` is dated 20261020 15:21 UTC [1][5]. |
| Latest release | v3.3.0, 20261008 18:28 UTC [3] |
| Status | Active by the 90-day rule, not archived [1]. The README has said since 20260814 15:08 UTC that the project is "largely in maintenance mode" and "won't be accepting new PRs or implementing new features" [4][6]. |
| Paper, docs | [From Local to Global (arXiv 2404.16130)](https://arxiv.org/abs/2404.16130), v1 20240424, v2 20250219 [26]. [Documentation](https://microsoft.github.io/graphrag/). [LazyGraphRAG blog, 20241125](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/) [24]. No LazyGraphRAG paper appears on the Microsoft Research project page, which lists the blog only [25]. |

## What it is

GraphRAG is an LLM-built knowledge-graph RAG pipeline. At index time an LLM extracts an entity and
relationship graph from every text chunk, hierarchical Leiden clustering turns the graph into a
community hierarchy, and an LLM writes a report for every community. At query time the system answers
from the community reports, the graph, and the source chunks, using one of four search modes [26][33].
Since v3.0 (first v3 release 20260128) the repository is a Python monorepo: `packages/graphrag` plus
seven helper packages (`graphrag-llm`, `-storage`, `-vectors`, `-cache`, `-chunking`, `-common`,
`-input`) [3][7]. The README describes the code as "a demonstration" and "not an officially supported
Microsoft offering" [4].

All source paths below are under `packages/graphrag/graphrag/` on `main`, read 20261030.

## How it works

### Indexing: the Standard method

The Standard pipeline is the default [9][19]. Its workflows run in this order: `create_base_text_units`,
`create_final_documents`, `extract_graph`, `finalize_graph`, `extract_covariates`, `create_communities`,
`create_final_text_units`, `create_community_reports`, `generate_text_embeddings` [9].

| Stage | Where | LLM use | Notes |
|---|---|---|---|
| Chunking | `index/workflows/create_base_text_units.py` | none | Default 1,200 tokens, overlap 100 [8]. |
| Graph extraction | `index/operations/extract_graph/graph_extractor.py`, `GraphExtractor._process_document` | one extraction call per chunk, plus gleaning calls | Default `max_gleanings: 1` [8][10]. See the call count below. |
| Claim extraction | `index/operations/extract_covariates/claim_extractor.py` | another per-chunk pass | Optional, off by default (`ExtractClaimsDefaults.enabled: False`) [8][19]. |
| Entity merge | `index/operations/extract_graph/extract_graph.py`, `_merge_entities` | none | Entities are grouped on the pair (`title`, `type`); titles are uppercased at parse time (`clean_str(record_attributes[1].upper())`). Relationships are grouped on (`source`, `target`) [10][11]. There is no further entity resolution in these files. |
| Description summarisation | `index/operations/summarize_descriptions/` | one call per entity and per relationship that has more than one distinct description | Descriptions are de-duplicated first; a single one is passed through without a call. When the combined descriptions exceed the input limit they are summarised in several passes [12]. Defaults: 500 tokens out, 4,000 in [8]. |
| Community detection | `index/operations/cluster_graph.py` | none | Hierarchical Leiden; `max_cluster_size: 10`, `use_lcc: True` (keep the largest connected component) by default [8][13]. |
| Community reports | `index/operations/summarize_communities/` | one call per community at every hierarchy level | Structured report (title, summary, findings, rating). Defaults: report at most 2,000 tokens, input at most 8,000 [8][14]. Reports are then embedded [9][20]. |

LLM calls per chunk at the default settings. The extractor makes one extraction call. For each of
`max_gleanings` rounds it makes a continuation call; between rounds (not after the last) it makes a
Y/N loop-check call [10]. At the default of one gleaning that is exactly **two calls per chunk**. In
general: 1 call when gleanings are 0, and up to 2 times `max_gleanings` calls when gleanings are 1 or
more. (The July text said "2 to 3 calls per chunk at defaults" and a cost of O(chunks x (1 + 2 x
gleanings)). Both overstate what the code on `main` does.)

Where the cost concentrates: per-chunk extraction is the largest term, then description summarisation
(proportional to entities plus relationships), then community reports (communities times levels). The
project's own documentation estimates "graph extraction to constitute roughly 75% of indexing cost"
[19]. The README warns that "GraphRAG indexing can be an expensive operation" [4].

### Indexing: the Fast method

`IndexingMethod.Fast` registers a different workflow list: `extract_graph_nlp` and `prune_graph` replace
`extract_graph` and `extract_covariates`, and `create_community_reports_text` replaces
`create_community_reports` [9]. The graph comes from `build_noun_graph/build_noun_graph.py`: noun
phrases become nodes, co-occurrence within a text unit becomes an edge, and edges get a
pointwise-mutual-information weight (`calculate_pmi_edge_weights` in `graphs/edge_weights.py`) [15].
The documentation states that entities have no description (the source text unit stands in), that
relationships have no description, and that no entity or relationship summarisation is needed [19].
The default noun-phrase extractor is NLTK plus regular expressions, English only; spaCy-based
extractors are optional [8][19]. The documentation also recommends much smaller chunks for this method,
50 to 100 tokens [19]. Community reports still use the LLM, one call per community, built from the text
units instead of from entity descriptions [9][19]. The documentation's own trade-off: Fast is "much
cheaper", but the graph is "less directly relevant for use outside of GraphRAG" and "quite a bit
noisier" [19].

### Indexing: incremental update and cache

`graphrag update` selects the `StandardUpdate` or `FastUpdate` pipelines, which append eight `update_*`
workflows (documents, entities and relationships, text units, covariates, communities, community
reports, embeddings, state cleanup) [9]. LLM calls go through a cache keyed on prompt and tuning
parameters, so a repeated identical request returns the stored result [20]. The default cache type is
JSON on file storage; v3.2.0 added SQLite as a built-in cache provider next to JSON, memory and no-op
[5][8][20][3].

### Query: four search modes

- **Local search** (`query/structured_search/local_search/mixed_context.py`,
  `LocalSearchMixedContext.build_context`). Embed the query, map it to entities by similarity over
  entity-description embeddings (`top_k_mapped_entities` 10, oversample factor 2), then fill one context
  window with a fixed split, and make one answer call [16]. With the configuration defaults that the CLI
  and API pass in (`query/factory.py`), the window is 12,000 tokens: 50% text units, 15% community
  reports, and the remaining 35% entities, relationships and covariates [8][16].
- **Global search** (`global_search/search.py`, `GlobalSearch.search`). Map-reduce over community
  reports: parallel `_map_response_single_batch` calls score points per batch of reports, then one
  `_reduce_response` call composes the answer. The cost grows with the number of reports at the chosen
  level [17]. **Dynamic community selection** is optional (`--dynamic-community-selection`, off by
  default) [17]. `DynamicCommunitySelection.select` starts from root communities and calls
  `rate_relevancy` on each. Each call returns a 0 to 10 rating as JSON and the mode over `num_repeats`
  repeats wins. A community whose rating is at or above `threshold` has its children queued. Defaults:
  `threshold` 1, `num_repeats` 1, `max_level` 2, `keep_parent` false [8][17]. Call and token counts are
  returned in `llm_info` and are not capped.
- **DRIFT search** (`drift_search/primer.py`, `search.py`). `PrimerQueryProcessor.expand_query` writes a
  hypothetical answer (HyDE style) and embeds it. `DRIFTPrimer` then splits the top community reports
  into `primer_folds` (default 5) and makes one call per fold, each returning an intermediate answer and
  "at least five" follow-up queries. The search loop then runs up to `n_depth` epochs (default 3), each
  running up to `drift_k_followups` (default 20) follow-ups as a full local search, each of which can
  spawn more follow-ups; a final reduce call composes the answer [8][18]. It is an agentic multi-hop
  loop inside the library and the most expensive mode.
- **Basic search** (`basic_search/`). Plain vector RAG over chunks, `k` 10, one answer call [8][7].

### LazyGraphRAG: what is published and what is open source

**Availability, re-checked 20261030.** No path in the `main` tree contains "lazy" (1,148 paths) [7]. A
code search for "LazyGraphRAG" in the repository returns two files: `docs/blog_posts.md`, which links
to the blog, and a code comment in `regex_extractor.py` [28][29][30]. The comment says the regex
noun-phrase extractor "is the extractor used in the first benchmarking of LazyGraphRAG" [30]. A search of
the `microsoft` organisation for "graphrag" returns only `microsoft/graphrag` and
`microsoft/graphrag-benchmarking-datasets`; repositories matching "lazygraphrag" belong to third
parties [28]. The latest release is v3.3.0 [3]. So no LazyGraphRAG query engine is open source as of
v3.3.0, and neither was one at v3.1.1.

What Microsoft says about availability:

- Discussion [#1490](https://github.com/microsoft/graphrag/discussions/1490), opened 20241209: a
  maintainer (AlonsoGuevara) wrote that day that it was "the next top priority item to release". The
  discussion stayed open and was last updated 20260710 [22].
- Issue [#1512](https://github.com/microsoft/graphrag/issues/1512) "When will LazyGraphRAG arrive?":
  on 20251118 20:46 UTC a collaborator (natoverse) wrote "At this point we have no ETA so I'm going to
  close the issue", and closed it as not planned [23].
- The blog carries an editor's note dated 20250606: the technology "has been integrated into Microsoft
  Discovery" and into Azure Local services "as part of a public preview" [24]. The Microsoft Research
  project page says "GraphRAG and LazyGraphRAG technology is now available through Microsoft
  Discovery", with no date and no mention of Azure Local [25].
- Since 20260814 the README says the repository will not implement new features [4][6]. Whether this
  rules out a later LazyGraphRAG release is not stated anywhere read. Inference: it makes one less
  likely.

**Published mechanism** (blog, 20241125) [24]:

- Index: NLP noun-phrase extraction for concepts and co-occurrences, graph statistics to optimise the
  concept graph and extract a hierarchical community structure. No LLM at index time. The blog states
  "data indexing costs are identical to vector RAG and 0.1% of the costs of full GraphRAG".
- Query: a best-first step ranks chunks by embedding similarity and then ranks communities through
  chunk-to-community membership. A breadth-first step uses an LLM-based sentence-level relevance
  assessor on the top-k untested chunks, and iterative deepening recurses into sub-communities after z
  successive communities yield zero relevant chunks. An LLM then extracts subquery-relevant claims from
  community-grouped chunks and map-reduces them.
- One cost knob, the **relevance test budget**, tested at 100, 500 and 1,500. The 100 level uses a
  low-cost LLM throughout; the 500 and 1,500 levels use a low-cost LLM for the tests and a stronger one
  for query refinement and answer generation.

**Published versus inferred.** The pipeline sketch, the budget levels and the cost ratios are published
[24]. The exact prompts, the allocation of the budget across subqueries, and the claim-extraction
format are unstated. The open-source repository holds ingredients, not the engine: the noun-phrase
graph with PMI weights (Fast method), `rate_relevancy`, and dynamic community selection [15][17]. That
the Fast index is "essentially" the LazyGraphRAG index is an inference from the blog's description plus
the code comment in [30]; no source states it.

## Cost and operating profile

- **Index time.** Dominated by per-chunk extraction (two calls per chunk at defaults), then
  per-entity and per-relationship summarisation, then per-community reports. Leiden and embeddings are
  the cheap parts [10][12][14]. The Fast method removes the extraction and summarisation calls but keeps
  one report call per community [9][19].
- **Rebuild.** A full rebuild re-spends unless the LLM cache is kept [20]. The cost mitigation is the
  cache, not a free path.
- **Cost knobs in the open-source code.** `IndexingMethod.Fast`; `max_gleanings`; `graphrag prompt-tune`
  (generates domain-adapted prompts; the README recommends it) [4]; incremental indexing through
  `graphrag update` [9]; dynamic community selection to cut global-search cost [17]. `prune_graph` is
  registered in the Fast pipeline only, not in Standard [9].
- **Spend limit.** No spend cap or budget setting appears in `config/defaults.py` or in the query and
  indexing files read [8][10][17]. Token and call counts are reported and never limited. A model price
  table exists in `graphrag-llm` (`model_cost_registry`, input and output cost per token) [21]. That no
  enforcement exists elsewhere in the repository was not exhaustively checked.
- **Local operation.** Models are called through a LiteLLM wrapper behind a factory, so providers are
  pluggable [20]. Whether a fully local model gives usable quality is unstated. Defaults need no
  database server: file storage and an embedded LanceDB vector store, with Azure AI Search and CosmosDB
  as options [8][20].
- **Agent interface.** A CLI (`graphrag init`, `index`, `update`, `query`, `prompt-tune`) and a Python
  API layer in `graphrag/api/` [7][31]. The breaking-changes document says changes to the API layer
  follow semantic versioning and that internals may change at any time [31]. No path in the repository
  tree contains "mcp", so an MCP server is not part of the repository; support by other means is
  unstated [7].

## Evidence

| Claim | Source | Caveat |
|---|---|---|
| GraphRAG gives "substantial improvements" over a conventional RAG baseline in comprehensiveness and diversity of answers to global sensemaking questions, on datasets in the 1 million token range | arXiv 2404.16130 abstract [26] | Authors' own evaluation. The abstract gives no figures. |
| Graph extraction is roughly 75% of indexing cost | project documentation [19] | The project's own estimate; method not given. |
| Dynamic community selection cuts total token cost by 77% on average against static global search, both at community level 1, with no statistically significant quality difference | MSR blog, 20241115 [27] | 50 global questions on AP news data; LLM-judged win rates on comprehensiveness, diversity and empowerment. At level 3 the dynamic search cost 34% more on average. |
| LazyGraphRAG index cost equals vector RAG and is 0.1% of full GraphRAG | MSR blog, 20241125 [24] | Authors' own claim. |
| LazyGraphRAG answers global queries at comparable quality to GraphRAG global search at more than 700 times lower query cost; at a 500-test budget it "significantly outperforms all conditions" at about 4% of the query cost | MSR blog [24] | 5,590 AP news articles, 100 synthetic queries, LLM head-to-head judging. The blog states the 4% against "GraphRAG global search" in the introduction and against "C2" in the results, so the two baselines differ. The blog's own definition of C2 was not captured. No code, prompts or paper behind the numbers. |

Third-party evaluations: none were searched for in this run (unstated, not "none exist"); the [fast-graphrag](fast-graphrag.md) entry does hold token and time figures for Microsoft GraphRAG from the GraphRAG-Bench comparison, a benchmark not run by this project. Discussion #1490
mentions KET-RAG (arXiv 2502.09304), a framework built on GraphRAG that targets cheaper indexing; it
was not evaluated here [22].

## Direction

- **Maintenance mode.** The README notice added 20260814 15:08 UTC says the project "explores the
  functional use of graphs to form a targeted context for question answering", that "the capabilities
  of frontier models have changed dramatically" since July 2024, and that Microsoft's "portfolio of
  research projects has diversified". It promises "bug fixes and dependency updates as appropriate,
  particularly to address CVEs" and no new features or PRs [4][6].
- **What the commits show.** 20 commits on `main` between 20260801 and 20261030: dependency sweeps,
  an automated dependency-update script, a docs spelling sweep, a local-search notebook, pinned GitHub
  Actions, the new SQLite cache (v3.2.0) and a SQLite performance fix (v3.3.0). By author login: 12
  `dworthen`, 4 `gaudyb`, 4 `Copilot` [3][5].
- **Releases since July.** v3.1.2 (20260821), v3.2.0 (20260924), v3.3.0 (20261008) [3].
- **Related Microsoft Research items.** The project page lists later items that it does not call
  successors: Claimify (20250319), BenchmarkQED (20250605), VeriTrail (20250805) [25]. No successor
  or rename of the repository was found: the repository name, owner and description are unchanged [1].

## Changed since the July 2026 investigation

Checked 20261030 18:58 to 19:04 UTC.

- **Numbers.** Stars 36,498 (July: about 34.8k at 20260725, so about +1,700, +4.9%, in 97 days; the July
  figure was rounded). Forks 3,868 (not recorded in July). Open issues 58 (GitHub's count includes open
  PRs; July: about 60). Release v3.3.0 (July: v3.1.1). Licence unchanged: MIT [1][2][3].
- **Not archived, not renamed, no licence change.** [1][2]
- **Maintenance mode (new).** Added to the README 20260814, after the July investigation. The July
  text "Actively maintained mid-2026" is stale as a description of intent: the code is still patched
  but the project says no new features [4][6].
- **LazyGraphRAG: still not open source.** Re-checked at v3.3.0 (see the section above). One July
  statement is wrong: "there has been no maintainer update since" 20241209. A collaborator closed
  issue #1512 on 20251118 as not planned, with "no ETA" [23]. The count "19 months of 'next priority'"
  is now almost 23 months since 20241209.
- **New cache provider.** SQLite, v3.2.0 (20260924), performance fix v3.3.0 [3][5].
- **README and architecture otherwise.** Package layout (eight packages) and every source path named in
  the July document still exist on `main` [7]. The Standard and Fast pipeline lists match the July
  description [9].
- **New paper versions.** None found: arXiv 2404.16130 has v1 and v2 only; v2 is dated 20250219,
  before the July investigation [26].

Corrections to July statements, checked against `main` on 20261030. Commit history filtered by path
shows that `graph_extractor.py`, `extract_graph.py`, `index/workflows/factory.py`, `cluster_graph.py`,
`mixed_context.py`, `query/factory.py`, `dynamic_community_selection.py` and `global_search/search.py`
were not modified after the v3.1.1 release day (20260718); `config/defaults.py` gained one cache line
(`database_name`, commit 150c697f) [32]. So these rows are errors or simplifications in the July text,
not code changes.

| July statement | Now | Source |
|---|---|---|
| "2 to 3 LLM calls per chunk at defaults"; cost O(chunks x (1 + 2 x gleanings)) | Exactly 2 at the default of one gleaning; at most 2 x `max_gleanings` for one or more | [10] |
| Entities "merge on uppercased exact title match" | Grouped on (`title`, `type`), both uppercased | [10][11] |
| Local search: 8,000-token context, 50% text units, 25% community reports | These are the method's argument defaults. The configuration defaults actually passed are 12,000 tokens, 50% text units, 15% community reports | [8][16] |
| Fast pipeline uses "spaCy/regex noun-phrase extraction" | Default is NLTK plus regex; spaCy extractors are optional | [8][19] |
| `prune_graph` listed as an open-source cost knob in general | Registered in the Fast pipeline only | [9] |
| "Actively maintained mid-2026" | README: "largely in maintenance mode" from 20260814 | [4][6] |
| LazyGraphRAG: "no maintainer update since" 20241209 | Issue #1512 closed as not planned, "no ETA", 20251118 | [23] |

## Sources

1. https://github.com/microsoft/graphrag (GitHub API repository record: stars, forks, licence field, archived flag, created and pushed dates, open issues, language, description): read 20261030 18:58 UTC
2. https://github.com/microsoft/graphrag/blob/main/LICENSE (MIT text, "Copyright (c) Microsoft Corporation"): read 20261030 18:58 UTC
3. https://github.com/microsoft/graphrag/releases (release list; bodies of v3.3.0, v3.2.0 and v3.1.2): list read 20261030 18:58 UTC, bodies 20261030 19:00 UTC
4. https://github.com/microsoft/graphrag/blob/main/README.md (maintenance-mode notice, repository guidance, prompt-tuning advice): read 20261030 18:58 UTC
5. https://github.com/microsoft/graphrag/commits/main (20 commits since 20260801; author logins): read 20261030 18:58 UTC and 19:01 UTC
6. https://github.com/microsoft/graphrag/commit/21f7bdf6 ("Add notice", 20260814 15:08 UTC; diff adds the README warning): read 20261030 19:00 UTC
7. https://github.com/microsoft/graphrag/tree/main (full tree, 1,148 paths; package list, file existence, no "lazy" or "mcp" path): read 20261030 18:58 UTC
8. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/config/defaults.py (all configuration defaults quoted): read 20261030 18:59 UTC
9. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/index/workflows/factory.py (Standard, Fast and update workflow lists): read 20261030 18:59 UTC
10. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/index/operations/extract_graph/graph_extractor.py (gleaning loop, uppercase titles): read 20261030 18:59 UTC
11. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/index/operations/extract_graph/extract_graph.py (`_merge_entities`, `_merge_relationships`): read 20261030 19:00 UTC
12. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/index/operations/summarize_descriptions/ (`summarize_descriptions.py`, `description_summary_extractor.py`: single-description pass-through): read 20261030 19:00 UTC
13. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/index/operations/cluster_graph.py (hierarchical Leiden, `use_lcc`): read 20261030 18:59 UTC
14. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/index/operations/summarize_communities/ and `index/workflows/create_community_reports.py` (per-level report generation): read 20261030 19:00 UTC
15. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/index/operations/build_noun_graph/build_noun_graph.py, `index/workflows/extract_graph_nlp.py`, `graphs/edge_weights.py` (noun graph, PMI): read 20261030 18:59 UTC
16. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/query/structured_search/local_search/mixed_context.py and `query/factory.py` (local-search context split and the configuration values passed in): read 20261030 18:59 UTC and 19:00 UTC
17. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/query/structured_search/global_search/search.py, `query/context_builder/dynamic_community_selection.py`, `query/context_builder/rate_relevancy.py`, `cli/main.py` (global search, dynamic selection, the `--dynamic-community-selection` option, default false): read 20261030 18:59 UTC and 19:03 UTC
18. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/query/structured_search/drift_search/primer.py and `search.py` (HyDE expansion, folds, follow-ups, epochs): read 20261030 18:59 UTC
19. https://github.com/microsoft/graphrag/blob/main/docs/index/methods.md (Standard and Fast methods, 75% estimate, trade-offs); `docs/index/default_dataflow.md` and `docs/query/` were also fetched: read 20261030 18:59 UTC
20. https://github.com/microsoft/graphrag/blob/main/docs/index/architecture.md (LLM caching, provider factories, LiteLLM wrapper, storage and vector-store options): read 20261030 18:59 UTC
21. https://github.com/microsoft/graphrag/blob/main/packages/graphrag-llm/graphrag_llm/model_cost_registry/model_cost_registry.py (price table): read 20261030 19:03 UTC
22. https://github.com/microsoft/graphrag/discussions/1490 (created 20241209, last updated 20260710; maintainer reply of 20241209; later comments; KET-RAG mention): read 20261030 18:58 UTC
23. https://github.com/microsoft/graphrag/issues/1512 (closed as not planned 20251118 by a collaborator, "no ETA"): read 20261030 19:01 UTC
24. https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ (mechanism, cost claims, budgets, test set, editor's note of 20250606): read 20261030 19:00 UTC
25. https://www.microsoft.com/en-us/research/project/graphrag/ (Microsoft Discovery statement, list of related items, no successor named): read 20261030 19:01 UTC
26. https://arxiv.org/abs/2404.16130 (title, abstract, version history v1 20240424 and v2 20250219): read 20261030 19:01 UTC
27. https://www.microsoft.com/en-us/research/blog/graphrag-improving-global-search-via-dynamic-community-selection/ (77% cost reduction, 50 questions, AP news data; published 20241115): read 20261030 19:01 UTC
28. GitHub code search for "LazyGraphRAG" in `microsoft/graphrag` and repository searches for "lazygraphrag" and "graphrag org:microsoft" (API search endpoints): run 20261030 19:01 UTC
29. https://github.com/microsoft/graphrag/blob/main/docs/blog_posts.md (links the LazyGraphRAG blog; no code reference): read 20261030 19:00 UTC
30. https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/index/operations/build_noun_graph/np_extractors/regex_extractor.py (code comment on LazyGraphRAG benchmarking): read 20261030 19:01 UTC
31. https://github.com/microsoft/graphrag/blob/main/breaking-changes.md (versioning surfaces, v3 notes): read 20261030 19:00 UTC
32. https://github.com/microsoft/graphrag/commits/main (GitHub API commit list filtered by path, since 20260718, for the nine files named above; one hit, `config/defaults.py`, commit 150c697f, whose patch adds the cache `database_name` line): run 20261030 19:05 UTC
33. https://github.com/microsoft/graphrag/blob/main/docs/index.md (the index process and the four query modes: Global, Local, DRIFT, Basic): read 20261030 19:00 UTC
