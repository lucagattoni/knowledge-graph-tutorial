---
type: page
order: 2
updated: 20261102 20:22 UTC
---

# What Pinakes takes from each project

Pinakes is a portable [knowledge base](../index/knowledge-base.md) for AI agents: one directory of documents, a free local search index, and a few read-only tools that an agent calls over the [Model Context Protocol](../index/model-context-protocol.md) [5]. This page answers, for twelve projects that were reviewed in July 2026 and re-checked on 20261030, what Pinakes took from each, what it left, what of that exists in Pinakes today, and whether the project's licence lets code be reused. The facts about each project are in chapter 3; the long evidence is in the archive pages linked at the end of each section.

## How to read this page

"Built" means that Pinakes' own status document lists a matching feature as shipped, at release 0.32.9 (last reviewed 20261102 15:19 UTC) [1]. It does not mean the project caused the feature. Four of the twelve are not named in any of Pinakes' status, roadmap, design or command-line documents: [Code-Graph-RAG](../projects/code-graph-rag.md), [datastax/graph-rag](../../kb-kg/projects/datastax-graph-rag.md), [LogicRAG](../../kb-kg/projects/logicrag.md) and [Youtu-GraphRAG](../../kb-kg/projects/youtu-graphrag.md). The roadmap names the other eight once, in the entry that lists the research that landed in release 0.1.1 [2]. So every "built" row below compares an idea with a feature; where the documents do not connect the two, the page says **unstated**.

Two kinds of statement are kept apart. Facts about a project (what its code, README, paper or issue says) were fetched again on 20261102 between 20:12 and 20:19 UTC from the primary source and carry sources 41 to 85. What Pinakes took or left, and why, is the reading of the July review as re-checked on 20261030; it carries the archive pages 29 to 40, which were unchanged on the main branch at 20261102 20:21 UTC. A point from the review that was not fetched again is marked "review, not re-checked".

Three Pinakes rules explain most of what was left:

- The search path never calls a paid model, and re-indexing is free. The only paid entry points are an opt-in PDF extractor and the `pnk ask --deep` command, and an allowlist that a test enforces keeps it at those two [1][5].
- The index is one SQLite file; the documents and their small metadata files ("sidecars", which carry permanent IDs and human-written links) are the source of truth [3][5].
- The tool surface is four read-only tools: `pinakes_search`, `pinakes_get`, `pinakes_links` and `pinakes_list_kbs` [1].

One measurement frames several rows. Pinakes derives a structural graph (chunks, documents, tags, headings and directories) and ships an expansion channel over it, switched `off`. On its RFC realism corpus (106,806 chunks) the channel answered 4 of 20 [multi-hop questions](../index/multi-hop-question-answering.md) against 7 of 20 with the channel off: 0 improved, 3 regressed, p = 1.0000. Pinakes measured this itself on 20260804 [1]. The [personalized PageRank](../index/personalized-pagerank.md) channel and an extra for [named-entity recognition](../index/named-entity-recognition.md) (`[ner]`) are staged: each is tied to a measurement and none is scheduled [1][2].

## Summary

The table repeats, in short form, what the section of each project below states and sources; the licence column repeats the licence-file lines 7 to 18.

| Project | What Pinakes took | What it left | Built in Pinakes today | Licence gate |
|---|---|---|---|---|
| [Code-Graph-RAG](../projects/code-graph-rag.md) | Typed, bounded graph verbs; capped results with a truncation flag; two-step retrieval; hash-gated reindex | Natural-language-to-[Cypher](../index/cypher.md) in the server; an internal agent; write tools | Mostly built: bounded `pinakes_links`, search then get, hash-gated sync. Not built: link counts on search hits, a budgeted context slice | Open (MIT) [7] |
| [datastax/graph-rag](../../kb-kg/projects/datastax-graph-rag.md) | Capped, ranked fan-out; visited-edge dedup; a lazy-GraphRAG blueprint for the paid loop | Query-time filter joins; the library as a dependency | Partly: SQLite graph tables, hub damping, expansion channel (off). Not built: best-first diverse traversal, community claim ranking | Open (Apache-2.0) [8] |
| [fast-graphrag](../../kb-kg/projects/fast-graphrag.md) | Personalized PageRank as a third fusion channel; score cascade; elbow cutoff | [LLM](../index/large-language-model.md) extraction at sync; pickled storage; the package | Not built: the PageRank channel is staged. A different channel was built and ships off | Open (MIT) [9] |
| [Graph-R1](../../kb-kg/projects/graph-r1.md) | The agent loop as composable tools; readable scores; the caller decides when to stop | [Reinforcement learning](../index/reinforcement-learning.md); LLM graph extraction; its evaluation | Built in a different form: caller-driven tools, and a budgeted `pnk ask --deep` loop. No training | Open (MIT) [10] |
| [Graphiti](../projects/graphiti.md) | Hybrid search with [rank fusion](../index/reciprocal-rank-fusion.md); expansion from hits; a traversal tool | LLM calls at ingest; a graph-database server | Partly: fusion and [rerank](../index/reranking.md) (built before the review), traversal tool, expansion channel (off). Not built: [validity windows](../index/temporal-knowledge-graph.md) | Open (Apache-2.0) [11] |
| [HippoRAG](../projects/hipporag.md) | The PageRank recipe: damping, two-part seed vector, hub damping | LLM triple extraction; the recognition-memory filter | Not built: staged and gated. Hub-size damping exists in the structural graph | Open (MIT) [12] |
| [LightRAG](../projects/lightrag.md) | Caller-supplied keywords; edges as a retrieval channel; context-only retrieval | Eager LLM extraction; a keyword call per query | Not built in its form. No decision recorded on the first two | Open (MIT) [13] |
| [LinearRAG](../../kb-kg/projects/linearrag.md) | Zero-LLM entity edges; hybrid seed vector; query-gated hops (ideas only) | The code; whole-corpus sentence embeddings | Not built: entity edges are staged | Read-only reference (GPL-3.0) [14] |
| [LogicRAG](../../kb-kg/projects/logicrag.md) | The shape of a bounded query-time loop with a rolling memory | The code; a dependency graph; an LLM-only sufficiency check | Built: `pnk ask --deep`, releases 0.24.0 to 0.26.0, without the dependency graph | Read-only reference (GPL-3.0) [15] |
| [Microsoft GraphRAG](../projects/microsoft-graphrag.md) | Support for "no LLM extraction at sync"; a single cost knob; golden-set discipline | The indexing pipeline; community reports; map-reduce search | Held: no extraction at sync. Not built: relevance-test budget, iterative deepening | Open (MIT) [16] |
| [MiniRAG](../../kb-kg/projects/minirag.md) | Entity-mention edges from a small local model, feeding the PageRank channel | The framework; path scoring; model calls in sync | Not built: staged behind the same gate | Open (MIT) [17] |
| [Youtu-GraphRAG](../../kb-kg/projects/youtu-graphrag.md) | A declared seed schema as an extraction budget; abstain-aware evaluation | The code; eager extraction; ungated schema growth | Not built. Nearest: printed link suggestions after a `--deep` run | Read-only reference (custom, academic use only) [18] |

## Code-Graph-RAG

**Took.** Four ideas [29]. Typed verbs with bounds instead of an open query language: the project's MCP guide lists graph tools that run fixed queries with no model (`resolve`, `definition`, `callers`, `callees`, `implementors`, `overrides`, `importers`, `tests_reaching`), several with a `depth` argument [42]. Results capped by rows and then by tokens, with a field that says truncation happened: on its natural-language query path the code cuts rows to a cap (default 500), then tokens (default 16,000), and returns a `summary` that reports the truncation [43]. Retrieval in two steps: `semantic_search` returns matches, and `get_code_snippet` returns the source for a qualified name [42]. A reindex that re-parses only changed files and keeps inbound edges: the updater defines a file-hash cache, a skip when nothing changed, and capture and restore of edges that arrive from unchanged files [44].
**Left.** Natural-language-to-Cypher inside the server (`query_code_graph`), an agent inside the server (`ask_agent`), and write tools on the same surface (`write_file`, `surgical_replace_code`) [42]. The guide also describes a `--read-only` mode that removes the write tools [42]. The July argument that the project needs heavy infrastructure is stale: the README says the graph is stored in an embedded SQLite file by default, with Memgraph and Neo4j as opt-in backends [41][29].
**Built.** `pinakes_links` takes `rel`, `direction` and `depth`, depth is "server-capped at 3", and the reply carries a `truncated` field [4]. Search then get is the retrieval pattern of the four tools [1][5]. `pnk sync` compares content hashes and keeps the ID when only content changed [3]. Not found in the documents read: link counts on search hits, and a budgeted context slice around a document. The project's guide now lists a `context` tool that returns a graph-ranked slice within a token budget [42][45]; the July review did not list it [29]. Whether the depth cap was taken from this project: **unstated**.
**Licence.** MIT [7]. Open.

*Reading:* the closest match to Pinakes' own bet, a deterministic index with the agent doing the traversal: the project's typed tools need no model [42]. How well that works for code, its authors' own retrieval figures included, was not re-checked here [29].

[Takeaway page](../../pinakes/takeaways/code-graph-rag.md) · [neutral entry](../../kb-kg/projects/code-graph-rag.md)

## datastax/graph-rag

**Took.** A quarry for traversal mechanics [30]. Keep only the top few neighbours per edge, ranked by similarity to the query: the traversal asks the store for adjacent content with the query embedding and `k = adjacent_k` [46]. Dedupe visited edges by value: an edge is a field and a value, and the traversal subtracts the set of visited edges before expanding [46][48]. Best-first diverse traversal: the MMR strategy selects the node with the highest maximal marginal relevance at each step, with a `lambda_mult` trade-off [47]. And a chain that traverses for free, then rates claims over [communities](../index/community-detection.md) of the retrieved subgraph: the project's notebook retrieves, finds communities in the sub-graph, extracts claims with an LLM, ranks them and answers; communities come from Girvan-Newman splitting until modularity stops improving [49]. Pinakes reads that chain as a blueprint for the paid loop [30].
**Left.** The library's query-time filter joins: it is built on the metadata search of existing vector stores [50]. That SQLite tables with joins are cheaper is the review's reasoning, not a measurement [30]. Also left: the LangChain layering, per-claim model ranking calls, and any dependency on the library [30].
**Built.** The graph is derived `nodes` and `edges` tables in SQLite, shipped in 0.11.0 [1]. The design caps fan-out per expansion with `[retrieval] adjacent_k`, applied after ranking [3]; whether it ships as a setting is **unstated**, because the status and roadmap documents do not mention it [1][2]. Hub flooding is handled by damping: hub spoke weights are 1/section-size, 1/dir-size and 1/tag-degree [3]. The expansion channel is built and off [1]. Not found in the documents read: best-first diverse traversal and community-based claim ranking. `pnk ask --deep` is decompose, search, answer and re-fold [1]. The similarity-ranked cap has not been tested against Pinakes' gate [30].
**Project state.** The last push was 20250505 and the repository is not archived [19]. No path in its file tree contains "bench" or "eval" [50].
**Licence.** Apache-2.0, the same as Pinakes [8][6]. Open. The reason for "never a dependency" is dormancy, not licence [30].

*Reading:* the project shows that metadata-defined edges are workable as a library. I found no retrieval-quality benchmark in its README, its docs pages read or its file tree [50], so the July wording that it "validates" the design was too strong [30].

[Takeaway page](../../pinakes/takeaways/datastax-graph-rag.md) · [neutral entry](../../kb-kg/projects/datastax-graph-rag.md)

## fast-graphrag

**Took.** Personalized PageRank run as a third channel in reciprocal rank fusion is Pinakes' plan [31]; the project's side of it: its README says it uses personalized PageRank to explore the graph [51], and its code runs it with damping 0.85 on an undirected graph [52]. A score cascade from graph nodes to relationships to chunks, with each named query entity matched to its single nearest entity and generic ones to the top 20 above a similarity of 0.5 [53]. An elbow cutoff: the code sorts the scores and cuts at the largest gap between neighbours [53]. Content-hash chunk IDs (the chunker imports `xxhash`) and aliases as explicit "identity" edges [53][31].
**Left.** The LLM extraction pass on every chunk at insert time (an information-extraction service with gleaning) and the dependencies `igraph` and `hnswlib` [56]; pickled graph storage [52]; exact-name node merging (review, not re-checked) [31]; and the package itself.
**Built.** The PageRank channel is **not built**: it is part of "the graph release, staged", eval-gated and never scheduled, and the `graph_channel` setting refuses the value `"ppr"` [1][2][3]. Searches of the four Pinakes documents for the elbow cutoff and for `example_queries` found nothing [31]. A different channel, expansion from first-stage hits, was built and measured (7 of 20 off, 4 of 20 on) and ships off; the roadmap says that result licenses neither PageRank nor `[ner]` [1][2]. PageRank itself has never been run on Pinakes' graph (review, not re-checked) [31].
**Evidence caveat.** July cited 93% against 42% for the cascade over plain vectors. The project's own benchmark page (first-party) has that row: on 101 queries of 2WikiMultihopQA, the share of queries with perfect retrieval is 0.93 for the project against 0.42 for a plain vector database [54]. An independent benchmark is more mixed: in GraphRAG-Bench, by other authors, Fast-GraphRAG scores below LightRAG in some columns of its tables and above it in others, depending on dataset and task [55].
**Project state.** The last push was 20251101; the repository is not archived [20].
**Licence.** MIT [9]. Open. Ideas only, for engineering reasons [31].

[Takeaway page](../../pinakes/takeaways/fast-graphrag.md) · [neutral entry](../../kb-kg/projects/fast-graphrag.md)

## Graph-R1

**Took.** The shape of the agent loop, not the training [32]. In the paper (first-party) the agent's action has four parts: think, which decides whether to continue or stop; generate a query; retrieve from the graph; and answer [57]. The environment does the graph mechanics, and two retrieval paths (entity-based and direct hyperedge) are merged by rank-based fusion [57]. In the released code each fused fact is returned with a score, written as `<knowledge>` and `<coherence>` [58]. Pinakes also noted a small number of facts per turn over several turns and results that advertise their next hop (review, not re-checked) [32].
**Left.** LLM graph extraction at build time: the README builds a knowledge hypergraph with n-ary relation extraction [59]. Reinforcement learning: the README trains with GRPO, REINFORCE++ or PPO [59]. Also left: per-corpus policy models, its evaluation setup, and the repository as an engineering reference [32].
**Built.** The loop exists in two forms. For an agent over the Model Context Protocol, the design delivers multi-hop retrieval "by making the tools composable rather than by building an agent" [3]. For the command line, `pnk ask --deep` is a budgeted loop: free retrieval first, a fitted confidence signal picks the branch, hard caps stop it, and no MCP tool reaches it [1][4]. There is no training and no LLM graph extraction [1]. `pinakes_links` returns a `frontier` [4]. The graph leg in fusion was built as the expansion channel, whose fusion form is unstated, and it ships off [1]. Per-hit scores in search, and tool text that says "refine instead of raising k": **unstated**.
**Project state.** The archive recorded one commit in 2026 [32]; the commit list now shows three dated 2026, two of them on 20261102 with the message "add". Their content was not read [21].
**Licence.** MIT [10]. Open. The verdict is to read the paper, not the code [32].

[Takeaway page](../../pinakes/takeaways/graph-r1.md) · [neutral entry](../../kb-kg/projects/graph-r1.md)

## Graphiti

**Took.** Confirmation of the retrieval shape [33]. The project's README describes hybrid retrieval that combines semantic embeddings, keyword (BM25) and graph traversal [60]. Its code ships 16 named search recipes and rerankers by rank fusion, maximal marginal relevance, a cross-encoder, graph distance from a centre node and episode-mention counts [61]; the Zep paper (first-party) describes the same three search functions and rerankers [63]. The paper's third search function is a breadth-first search over the graph [63]; the review reads it as graph expansion seeded by the other channels' hits [33]. Invalidation instead of deletion, via validity windows, is in the README [60]. Pinakes also noted that Graphiti's MCP server has no neighbour-traversal tool: its 13 tools add, search, fetch and delete memory and manage the graph, and the two search tools take an optional `center_node_uuid` [62].
**Left.** The LLM work per ingested episode: `add_memory` returns at once and processes the episode in the background to extract entities and relationships [62]. A graph-database server: the README lists Neo4j, FalkorDB and Amazon Neptune, with Kuzu deprecated [60]. The fire-and-forget ingest tool, the extracted-entity graph as the unit of retrieval, and the 13-tool surface [62][33].
**Built.** The free pipeline is [BM25](../index/bm25.md) and vector search, fusion with k=60, and a local rerank [3]; it was released before the Graphiti note, so Graphiti confirmed it rather than shaped it [33]. The traversal tool is `pnk links` and `pinakes_links`, shipped in 0.5.0 on 20260731 [2]. Expansion from hits is the expansion channel, shipped off in 0.11.0 [1]. Not found in the documents read: validity windows (`valid_at`, `invalid_at`, bi-temporal), named recipes, and a "near this document" argument on search [1][2][3].
**Licence.** Apache-2.0, the same as Pinakes [11][6]. Open. Whether any Graphiti source was copied: **unstated**.

*Reading:* Graphiti's main lesson for Pinakes was ergonomic, a provenance tool and a small surface, not its LLM-at-ingest pipeline [33].

[Takeaway page](../../pinakes/takeaways/graphiti.md) · [neutral entry](../../kb-kg/projects/graphiti.md)

## HippoRAG

**Took.** HippoRAG 2 is the reference recipe for a PageRank channel [34]. In its code the walk is a graph library's personalized PageRank, with no model call, default damping 0.5, on an undirected graph [64]. The reset vector has two parts: phrase seeds, each weighted by the mean score of the top facts that contain it and divided by the number of passages it appears in; and every passage node, weighted by its min-max normalised dense score times `passage_node_weight`, default 0.05 [64]. In the paper (first-party) a table of passage weights from 0.01 to 0.5 has 0.05 best on [MuSiQue](../datasets/musique.md) and tied best with 0.1 on NaturalQuestions, on dev sets of 1,000 queries each [65]. When no fact survives reranking, the code returns dense retrieval results and skips the graph [64].
**Left.** LLM triple extraction at index time: the code runs an OpenIE step over the chunks [64]. The model-based recognition-memory filter: the paper's ablation row is named "w/o Filter" [65]. Also left: the fact-embedding store and any expectation of graph gains on simple lookups [34].
**Built.** The PageRank channel is **not built**: it is staged, and its gate "does not run at all on a corpus below the heading-coverage floor" [2]. Release 0.13.0 added an opt-in `[chunking] headings = "numbered"` so plain text can carry a heading path [1]. The structural graph (0.11.0) damps hubs by size [3][1]; that resembles HippoRAG's damping of a seed by the number of passages it links to, but no document says it was taken from there (**unstated**) [64]. The expansion channel is a different mechanism, so its failed gate does not test HippoRAG's recipe [1][34].
**Correction carried from the review.** The code scales dense scores to [0, 1] per query with `min_max_normalize` before multiplying by 0.05, so a recipe using fused rank scores must normalise them the same way [64]; that part is an inference about Pinakes' scores, not a measurement [34].
**Licence.** MIT [12]. Open.

[Takeaway page](../../pinakes/takeaways/hipporag.md) · [neutral entry](../../kb-kg/projects/hipporag.md)

## LightRAG

**Took.** Five ideas [35]. Keywords supplied by the caller: the code returns the caller's high-level and low-level keywords when they are given, and only otherwise asks a model for them [67]. Relations indexed as a retrieval channel: relations have their own vector store [67]. Context-only retrieval: a query parameter `only_need_context` returns the assembled context without an answer [67]. Rebuilding graph state from stored extraction results: the code has a `rebuild_knowledge_from_chunks` function [67]. A per-document status record (`doc_status`) that makes ingest resumable [69][35].
**Left.** Eager per-chunk LLM extraction: the README says extraction "runs on every text chunk" [66]. A keyword call at query time unless the caller supplies keywords; the README says the keyword model must be a non-thinking model to keep latency low [66][67]. July also left its hosted-only rerank; that is stale, because the README advises deploying the rerank model locally and the example configuration shows a vLLM-served reranker [66][68]. Also on the review's list, not re-checked: exact-name entity merging and several query modes pushed onto the caller [35].
**Built.** None in LightRAG's form. The arguments of `pinakes_search` are `query`, `kb`, `tags`, `path_prefix`, `source_type` and `k`; there are no keyword slots [4]. No document records a decision to drop them, so whether they were declined or never scheduled is **unstated** [35]. Edge text was never indexed as a channel; the nearest thing is the expansion channel, which tests graph expansion, not edge text [1][35]. Context-only holds for `pnk search`, the MCP tools and `pnk ask` without `--deep`; `--deep` synthesises an answer and is not an MCP tool [1][4]. The same rebuild-from-cache shape exists for PDF text: "a rebuild never spends" [2].
**Open item.** The first two ideas have no recorded decision in Pinakes. That decision is the owner's [35].
**Licence.** MIT [13]. Open.

[Takeaway page](../../pinakes/takeaways/lightrag.md) · [neutral entry](../../kb-kg/projects/lightrag.md)

## LinearRAG

**Took (ideas only).** Graph construction with no model call can compete with LLM-extraction GraphRAG: the README says the method "eliminates LLM token costs during graph construction" and builds a relation-free graph from entity recognition and semantic links [70]. Entity-to-passage edges as a cross-document edge class that structural edges cannot produce: the code builds entity-to-sentence and sentence-to-entity matrices [71]. A hybrid reset vector: the configuration defaults are `passage_node_weight` 0.05, `damping` 0.5, `max_iterations` 3, `iteration_threshold` 0.5 and `top_k_sentence` 1, which fits hops followed only through sentences similar to the question [71][36]. A named-entity cache keyed by content hash: the code loads earlier NER results by passage hash and processes only new passages [71]. Reporting relevance next to recall (review, not re-checked) [36].
**Left.** The code (see the licence). Sentence embeddings of the whole corpus: the code keeps a sentence embedding store [71]. A transformer pipeline as the default NER model: the README and the configuration name spaCy `en_core_web_trf` [70][71]. A benchmark-shaped keyword boost: a list of words such as "born", "where", "founded" and a `attribute_keyword_boost` of 0.25, behind a switch that defaults to off [71]. Also on the review's list, not re-checked: no entity canonicalisation, research-code defaults that disagree with the paper, and a full scan per query [36].
**Built.** Not built. Entity edges and the `[ner]` extra are staged and eval-gated; so is the PageRank channel [1][2]. The sibling edge, which both designs have, was built in 0.11.0 and was inert in Pinakes' measurement [1].
**Evidence caveat.** The paper's numbers are first-party, on passages the authors merged and re-split; an open outside issue, opened 20260507, reports lower exact-match and F1 scores on the original splits (for example [HotpotQA](../datasets/hotpotqa.md) exact match 34.0 against 44.5 on the authors' split, in the reporter's own run with top-k 5), and a reply on 20260518 says that the original chunks were merged and re-split by a fixed token length [72]. The archive did not reproduce the outside figures, and neither did I. The margin over HippoRAG 2 is unreplicated [36].
**Project state.** The last push was 20260705; the repository is not archived [22].
**Licence.** The `LICENSE.txt` file is the GPL version 3 text with a placeholder copyright line ("anonymous") [14]. Read-only reference: Pinakes is Apache-2.0 and its server is a network service, so copying GPL code would reach every embedder [6][36]. Ideas and measured results are free to reuse; source is not.

[Takeaway page](../../pinakes/takeaways/linearrag.md) · [neutral entry](../../kb-kg/projects/linearrag.md)

## LogicRAG

**Took.** The shape of a bounded loop at query time [37]. In the released code round 0 is plain retrieval followed by a model's warm-up check of whether simple fact retrieval can already answer, and the loop runs only if the check says no; one summary is refined with each round's new contexts, so the memory stays bounded; the dependencies of a question are put in topological order; an option filters chunks already retrieved; and a round cap ends in a best-effort final answer [74]. Pinakes took the shape of that loop, with a flat list and local ordering, and runs it only on the command line, never inside the MCP server [37].
**Left.** The code (see the licence). The dependency graph with its topological sort [74]. An LLM-judged sufficiency check used alone [74]. Dense-only retrieval: the paper's experiments retrieve with one sentence-embedding model for all methods [73]. Prompted JSON repaired after the fact: the code passes model output through `fix_json_response` [74]. The review also left the claim that the loop is "the efficient frontier" (review, not re-checked) [37].
**Built.** `pnk ask --deep` shipped in 0.24.0 on 20260811 and the deep release closed at 0.26.0 on 20260822 [2]. Free retrieval is round 0 and a fitted confidence signal, not a model self-report, picks the branch [1]. The memory is re-folded to a fixed budget [3]. The output reports why it stopped: `answered`, `sufficient`, `round-cap`, `no-new-subproblems`, `no-evidence` or `budget` [4]. Every `--deep` run that returns writes a transcript, and since 0.26.0 a run prints suggested `links[]` entries for documents cited together, for the user to review and commit [1]. No MCP tool runs it, and a test asserts the server never loads the module [4]. The dependency graph was not built: a round is two calls over a flat list [1]. No Pinakes document names LogicRAG; the design says three properties "are taken from the published systems this shape comes from, and none of them are code" [3].
**Licence.** GPL-3.0 [15]. Read-only reference. The repository was last pushed on 20260719 and is not archived [23].

*Reading:* the paper (first-party) argues from the token cost of pre-built graphs and reports a query-time efficiency comparison [73]; that supports the cost argument for a query-time loop, but it does not validate Pinakes' loop, which differs from the released code [37].

[Takeaway page](../../pinakes/takeaways/logicrag.md) · [neutral entry](../../kb-kg/projects/logicrag.md)

## Microsoft GraphRAG

**Took.** Microsoft's own path, as outside support for "no extraction at sync" [38]. Its documentation lists a standard indexing method, in which a language model extracts the graph, and a fast method, in which entities are noun phrases from NLP libraries and relationships are co-occurrence in a text unit, with no summarisation of entities or relationships [75]. LazyGraphRAG goes further: the blog (first-party) says it builds a concept graph from noun phrases and their co-occurrences, has no summarising step at index time, and defers all model use to query time [76]. Overall performance is scaled by one main parameter, the relevance test budget, and the method combines best-first and breadth-first search in an iterative deepening manner [76]. The blog shows win rates against eight competing conditions at budgets of 100, 500 and 1,500 relevance tests, the model for justifying a change by a win-rate-against-budget curve [76][38]. Also taken, per the review and not re-checked: pointwise-mutual-information edge weights [38].
**Left.** The whole standard indexing pipeline and precomputed community reports [75]. Map-reduce global search, the in-library agent loop, its entity resolution, and any wait for LazyGraphRAG code [38].
**Built.** No extraction at sync is held: the paid-path allowlist is complete at two entries, and neither extracts entities or relations [1]. Free structural edges were built in 0.11.0, with the expansion channel off [1]. The relevance-test budget was **not** built: `--deep` is budgeted in euros (the status document records its ceilings raised to 2.00 per operation and 6.00 per day) and a round is two paid calls [1]. Iterative deepening and edge weighting by co-occurrence were not found in the documents read. Golden-set discipline was built: 74 questions in 0.7.0 and a 110-question set authored blind and frozen [1].
**Project state.** The README now says the project "is largely in maintenance mode, and won't be accepting new PRs or implementing new features". The latest release is v3.3.0 of 20261008 [26][27]. LazyGraphRAG is still not offered as an indexing method: the documentation page lists only the standard and the fast methods [75], and the issue "When will LazyGraphRAG arrive?" was closed as not planned on 20251118 [77].
**Licence.** MIT, "Copyright (c) Microsoft Corporation" [16]. Open. Nothing was copied.

[Takeaway page](../../pinakes/takeaways/microsoft-graphrag.md) · [neutral entry](../../kb-kg/projects/microsoft-graphrag.md)

## MiniRAG

**Took.** Evidence that a 1.5 to 4 billion parameter local model can build a usable entity layer [39]: the README's results table (first-party) pairs four small models, GLM-Edge-1.5B, Qwen2.5-3B, MiniCPM3-4B and Phi-3.5-mini, with the framework on the LiHua-World dataset [78][79]. The one idea worth keeping: entity-mention edges, from names and types extracted at sync by a small model, feeding the PageRank channel [39]. Also an extraction cache: the code enables an LLM response cache by default [80]. An index of bare entity names, delimiter-tuple output for small models (the prompts use a tuple delimiter [80]), chunks as first-class retrieval targets, and the LiHua-World dataset as a candidate corpus close to Pinakes' workload [39][78].
**Left.** The bespoke path-scoring code: `operate.py` imports `edge_vote_path` and `cal_path_score_list` [80]. A model call per query in the free path: the prompts include a query-to-keywords prompt, `minirag_query2kwd` [80]. Relationship extraction (the code extracts edge keywords) [80]. Mandatory model extraction in sync, and adoption of the framework [39].
**Built.** Nothing. The entity layer and the PageRank channel are staged and gated [1][2]. The extraction cache that exists was built in 0.2.0 for a different purpose: it caches the text a PDF extractor returns, so `--rebuild` is free [1][2]. Chunks stay first-class, because the only graph channel is off [1].
**Evidence caveat.** The results table lists one small model per row [78]. A small local indexer paired with a strong reader, which is Pinakes' case, is **unstated** [78][79].
**Project state.** The last push was 20251016; the repository is not archived [24].
**Licence.** MIT, copyright line "2024 Gustavo Ye" [17]. Open.

[Takeaway page](../../pinakes/takeaways/minirag.md) · [neutral entry](../../kb-kg/projects/minirag.md)

## Youtu-GraphRAG

**Took.** A declared seed schema (entity types, relations, attribute types) that bounds LLM graph extraction, proposed for any future lazy extraction under `--deep`; schema growth as an explicit, reviewable change; naming the schema types a query touches; and the framing of an evaluation on content the model cannot already know, with abstain accuracy reported apart [40]. On the project's side: the README names a "Seed Graph Schema" that bounds extraction and "Scalable Schema Expansion" [81]; the paper (first-party) adds expansions to the schema when a score reaches a threshold and builds the AnonyRAG dataset for its anonymity-reversion task [85]. The July note read "types must appear in the schema" as how the code works; that is the paper's wording, and the shipped extraction prompt says to prioritise the predefined schema but, if the context does not fit it, to "extract the valuable knowledge as needed", so any Pinakes use would need a check in code [82][40].
**Left.** The code (see the licence), a heavy dependency set, eager whole-corpus extraction, and the four-level tree as storage (attributes, relations, keywords, communities) [40][81]. Also left: ungated schema auto-expansion. An outside issue opened 20261004 reports a run on MuSiQue with Qwen3-14B that started from the seed schema of 10 node types and had 523 node types, 1,539 relation types and 1,198 attribute types after 681 of 11,656 passages; the run was stopped by the reporter's own 20,000-token limit. The issue is open, with no comments [83].
**Built.** The seed schema is **not built**: Pinakes has no LLM entity or relation extraction, `pnk init` ships one template, and a second was ruled a no-go in 0.22.0 [1]. The nearest thing is the printed link suggestions of `--deep` (0.26.0), which are citations, not schema types [1]. Evaluation reports false-abstain and false-confidence rates; this is related to, not the same as, the paper's reject accuracy [1][40]. No anonymised-corpus evaluation was found in the four documents.
**Project state.** The last push was 20260226; the repository is not archived [25].
**Licence.** Custom. The operative term: "only for academic purposes, and refrain from using it for any commercial or production purposes under any circumstances" [18]. The README badge says MIT; the `LICENSE` file governs [28]. Read-only reference. The AnonyRAG dataset has its own non-commercial licence, CC BY-NC 4.0 [84].

[Takeaway page](../../pinakes/takeaways/youtu-graphrag.md) · [neutral entry](../../kb-kg/projects/youtu-graphrag.md)

## Sources

Pinakes documents and facts about Pinakes, read from the public repository:

1. https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md : release 0.32.9 and its date of review, the surface table, the release table, the expansion-channel measurement, the staged graph release, the paid-path allowlist, the two-list fusion wording, the transcript written by every `pnk ask --deep` that returns (read 20261102 19:37 UTC; lines on transcripts and fusion re-read 20261102 20:19 UTC)
2. https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md : the 0.1.1 research entry, 0.5.0, 0.24.0 and 0.26.0 dates, the staged graph release and its gate, decision D-15 (read 20261102 19:37 UTC)
3. https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md : the free pipeline, edge weights, `adjacent_k`, the `"ppr"` rule, the multi-hop section, content-hash sync (read 20261102 19:37 UTC)
4. https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md : the MCP tool arguments, `pnk links` flags and depth cap, `--deep` output fields, no MCP tool for `--deep` (read 20261102 19:37 UTC)
5. https://github.com/lucagattoni/pinakes/blob/main/README.md : what Pinakes is, the free path, the tool pattern (read 20261102 19:40 UTC)
6. https://api.github.com/repos/lucagattoni/pinakes : Pinakes' licence, Apache-2.0 (read 20261102 19:39 UTC)

Licence files of the twelve projects (the `LICENSE` file, not the README badge):

7. https://github.com/vitali87/code-graph-rag/blob/HEAD/LICENSE : MIT (read 20261102 19:38 UTC; re-read 20261102 20:14 UTC)
8. https://github.com/datastax/graph-rag/blob/HEAD/LICENSE : Apache License 2.0 (read 20261102 19:38 UTC)
9. https://github.com/circlemind-ai/fast-graphrag/blob/HEAD/LICENSE : MIT (read 20261102 19:38 UTC)
10. https://github.com/LHRLAB/Graph-R1/blob/HEAD/LICENSE : MIT (read 20261102 19:38 UTC)
11. https://github.com/getzep/graphiti/blob/HEAD/LICENSE : Apache License 2.0 (read 20261102 19:38 UTC)
12. https://github.com/OSU-NLP-Group/HippoRAG/blob/HEAD/LICENSE : MIT (read 20261102 19:38 UTC)
13. https://github.com/HKUDS/LightRAG/blob/HEAD/LICENSE : MIT (read 20261102 19:38 UTC)
14. https://github.com/DEEP-PolyU/LinearRAG/blob/HEAD/LICENSE.txt : GNU GPL version 3, placeholder copyright line (read 20261102 19:38 UTC; re-read 20261102 20:14 UTC)
15. https://github.com/chensyCN/LogicRAG/blob/HEAD/LICENSE : GNU GPL version 3 (read 20261102 19:38 UTC; re-read 20261102 20:14 UTC)
16. https://github.com/microsoft/graphrag/blob/HEAD/LICENSE : MIT (read 20261102 19:38 UTC)
17. https://github.com/HKUDS/MiniRAG/blob/HEAD/LICENSE : MIT (read 20261102 19:38 UTC; re-read 20261102 20:14 UTC)
18. https://github.com/TencentCloudADP/youtu-graphrag/blob/HEAD/LICENSE : the Youtu-GraphRAG License, academic use only (read 20261102 19:38 UTC; re-read 20261102 20:14 UTC)

Project state, read from the GitHub API:

19. https://api.github.com/repos/datastax/graph-rag : last push 20250505, not archived (read 20261102 19:39 UTC; re-read 20261102 20:14 UTC)
20. https://api.github.com/repos/circlemind-ai/fast-graphrag : last push 20251101, not archived (read 20261102 19:39 UTC; re-read 20261102 20:14 UTC)
21. https://api.github.com/repos/LHRLAB/Graph-R1/commits : commits dated 20260430 and two on 20261102 (the other commits in the list of 100 are dated 2025); no releases (read 20261102 19:39 UTC; commit dates re-read 20261102 20:14 UTC)
22. https://api.github.com/repos/DEEP-PolyU/LinearRAG : last push 20260705, not archived (read 20261102 19:39 UTC; re-read 20261102 20:14 UTC)
23. https://api.github.com/repos/chensyCN/LogicRAG : last push 20260719, not archived (read 20261102 19:39 UTC; re-read 20261102 20:14 UTC)
24. https://api.github.com/repos/HKUDS/MiniRAG : last push 20251016, not archived (read 20261102 19:39 UTC; re-read 20261102 20:14 UTC)
25. https://api.github.com/repos/TencentCloudADP/youtu-graphrag : last push 20260226, not archived (read 20261102 19:39 UTC; re-read 20261102 20:14 UTC)
26. https://github.com/microsoft/graphrag/blob/HEAD/README.md : the maintenance-mode statement (read 20261102 19:42 UTC; re-read 20261102 20:12 UTC)
27. https://api.github.com/repos/microsoft/graphrag/releases/latest : v3.3.0, published 20261008 (read 20261102 19:42 UTC; re-read 20261102 20:14 UTC)
28. https://github.com/TencentCloudADP/youtu-graphrag/blob/HEAD/README.md : the README's MIT badge (read 20261102 19:42 UTC; re-read 20261102 20:12 UTC)

Archive pages, the July review's reading of what Pinakes takes and leaves from each project, re-checked 20261030 (each archive page cites its own sources and read times; all twelve were unchanged on the main branch at 20261102 20:21 UTC). The URL is the page in the public repository:

29. https://github.com/lucagattoni/knowledge-graph-tutorial/blob/main/pinakes/takeaways/code-graph-rag.md : the four takes, the leaves, the stale infrastructure argument, the context slice (read 20261030 19:08 UTC, via the archive page pinakes/takeaways/code-graph-rag.md)
30. https://github.com/lucagattoni/knowledge-graph-tutorial/blob/main/pinakes/takeaways/datastax-graph-rag.md : the quarry ideas, leaves, the "validates" correction, the open fan-out question (read 20261030 19:07 UTC, via the archive page pinakes/takeaways/datastax-graph-rag.md)
31. https://github.com/lucagattoni/knowledge-graph-tutorial/blob/main/pinakes/takeaways/fast-graphrag.md : takes, leaves, vendor-benchmark caveat (read 20261030 19:07 UTC, via the archive page pinakes/takeaways/fast-graphrag.md)
32. https://github.com/lucagattoni/knowledge-graph-tutorial/blob/main/pinakes/takeaways/graph-r1.md : takes, leaves, unstated items (read 20261030 19:08 UTC, via the archive page pinakes/takeaways/graph-r1.md)
33. https://github.com/lucagattoni/knowledge-graph-tutorial/blob/main/pinakes/takeaways/graphiti.md : takes, leaves, built-by-idea mapping (read 20261030 19:07 UTC, via the archive page pinakes/takeaways/graphiti.md)
34. https://github.com/lucagattoni/knowledge-graph-tutorial/blob/main/pinakes/takeaways/hipporag.md : the recipe, leaves, the normalisation correction (read 20261030 19:06 UTC, via the archive page pinakes/takeaways/hipporag.md)
35. https://github.com/lucagattoni/knowledge-graph-tutorial/blob/main/pinakes/takeaways/lightrag.md : the five ideas, leaves, the open item (read 20261030 19:06 UTC, via the archive page pinakes/takeaways/lightrag.md)
36. https://github.com/lucagattoni/knowledge-graph-tutorial/blob/main/pinakes/takeaways/linearrag.md : ideas, leaves, the evidence caveat, the licence reasoning (read 20261030 19:04 UTC, via the archive page pinakes/takeaways/linearrag.md)
37. https://github.com/lucagattoni/knowledge-graph-tutorial/blob/main/pinakes/takeaways/logicrag.md : the loop's shape, leaves, the paper-versus-code point (read 20261030 19:08 UTC, via the archive page pinakes/takeaways/logicrag.md)
38. https://github.com/lucagattoni/knowledge-graph-tutorial/blob/main/pinakes/takeaways/microsoft-graphrag.md : the trajectory, takes, leaves (read 20261030 19:07 UTC, via the archive page pinakes/takeaways/microsoft-graphrag.md)
39. https://github.com/lucagattoni/knowledge-graph-tutorial/blob/main/pinakes/takeaways/minirag.md : the entity-layer idea, leaves, the evidence caveat (read 20261030 19:08 UTC, via the archive page pinakes/takeaways/minirag.md)
40. https://github.com/lucagattoni/knowledge-graph-tutorial/blob/main/pinakes/takeaways/youtu-graphrag.md : the seed schema, leaves, the schema-growth point, the dataset licence (read 20261030 19:06 UTC, via the archive page pinakes/takeaways/youtu-graphrag.md)

Primary sources for facts about the projects, fetched again on 20261102. Code-Graph-RAG:

41. https://github.com/vitali87/code-graph-rag/blob/HEAD/README.md : "The graph is stored in an embedded SQLite file by default. Memgraph and Neo4j are opt-in backends" (read 20261102 20:12 UTC)
42. https://github.com/vitali87/code-graph-rag/blob/HEAD/docs/guide/mcp-server.md : the typed tools and their `depth`, `semantic_search`, `get_code_snippet`, `query_code_graph`, `ask_agent`, `write_file`, `surgical_replace_code`, `context`, the read-only mode (read 20261102 20:14 UTC)
43. https://github.com/vitali87/code-graph-rag/blob/HEAD/codebase_rag/tools/codebase_query.py and https://github.com/vitali87/code-graph-rag/blob/HEAD/codebase_rag/config.py : row cap 500 then token cap 16,000, the truncation `summary` (read 20261102 20:14 UTC)
44. https://github.com/vitali87/code-graph-rag/blob/HEAD/codebase_rag/graph_updater.py : the hash-cache, sync-check and inbound-edge capture and restore functions (read 20261102 20:14 UTC)
45. https://github.com/vitali87/code-graph-rag/blob/HEAD/docs/architecture/context-slice.md : the `context` tool and its token budget (read 20261102 20:14 UTC)

datastax/graph-rag:

46. https://github.com/datastax/graph-rag/blob/HEAD/packages/graph-retriever/src/graph_retriever/traversal.py and https://github.com/datastax/graph-rag/blob/HEAD/docs/guide/traversal.md : adjacent fetch with the query embedding and `adjacent_k`; the visited-edge set (read 20261102 20:14 UTC)
47. https://github.com/datastax/graph-rag/blob/HEAD/packages/graph-retriever/src/graph_retriever/strategies/mmr.py and https://github.com/datastax/graph-rag/blob/HEAD/docs/guide/strategies.md : the MMR strategy and `lambda_mult` (read 20261102 20:14 UTC)
48. https://github.com/datastax/graph-rag/blob/HEAD/packages/graph-retriever/src/graph_retriever/edges/_base.py : an edge is a metadata field and a value (read 20261102 20:19 UTC)
49. https://github.com/datastax/graph-rag/blob/HEAD/docs/examples/lazy-graph-rag.ipynb and https://github.com/datastax/graph-rag/blob/HEAD/packages/langchain-graph-retriever/src/langchain_graph_retriever/document_graph.py : the five-step LazyGraphRAG chain; Girvan-Newman until modularity stops improving (read 20261102 20:14 UTC)
50. https://github.com/datastax/graph-rag/blob/HEAD/README.md and https://api.github.com/repos/datastax/graph-rag/git/trees/HEAD?recursive=1 : built on the metadata search of existing vector stores; no file path containing "bench" or "eval" (read 20261102 20:12 and 20:13 UTC)

fast-graphrag:

51. https://github.com/circlemind-ai/fast-graphrag/blob/HEAD/README.md : personalized PageRank to explore the graph (read 20261102 20:12 UTC)
52. https://github.com/circlemind-ai/fast-graphrag/blob/HEAD/fast_graphrag/_storage/_gdb_igraph.py : damping 0.85, undirected, pickled graph file (read 20261102 20:14 UTC)
53. https://github.com/circlemind-ai/fast-graphrag/blob/HEAD/fast_graphrag/_services/_state_manager.py and https://github.com/circlemind-ai/fast-graphrag/blob/HEAD/fast_graphrag/_policies/_ranking.py and https://github.com/circlemind-ai/fast-graphrag/blob/HEAD/fast_graphrag/_services/_chunk_extraction.py : entity-to-relationship-to-chunk scoring, named and generic entities, identity edges, the elbow policy, `xxhash` (read 20261102 20:14 and 20:18 UTC)
54. https://github.com/circlemind-ai/fast-graphrag/blob/HEAD/benchmarks/README.md : the project's own benchmark table, 0.93 against 0.42 on 101 queries (read 20261102 20:14 UTC)
55. https://arxiv.org/html/2506.05690 : GraphRAG-Bench (arXiv 2506.05690), tables listing Fast-GraphRAG, LightRAG, RAPTOR and others (read 20261102 20:15 UTC)
56. https://github.com/circlemind-ai/fast-graphrag/blob/HEAD/pyproject.toml and https://github.com/circlemind-ai/fast-graphrag/blob/HEAD/fast_graphrag/_services/_information_extraction.py : `igraph` and `hnswlib` dependencies; the LLM extraction service (read 20261102 20:18 UTC)

Graph-R1:

57. https://arxiv.org/html/2507.21892 : Graph-R1 (arXiv 2507.21892, v2 of 2 June 2026), the four-part action, the multi-turn loop, dual-path retrieval with rank-based fusion (read 20261102 20:14 UTC)
58. https://github.com/LHRLAB/Graph-R1/blob/HEAD/graphr1/operate.py : fusion by reciprocal rank, output as `<knowledge>` and `<coherence>` (read 20261102 20:14 UTC)
59. https://github.com/LHRLAB/Graph-R1/blob/HEAD/README.md : n-ary relation extraction into a knowledge hypergraph; GRPO, REINFORCE++ and PPO training (read 20261102 20:12 UTC)

Graphiti:

60. https://github.com/getzep/graphiti/blob/HEAD/README.md : hybrid retrieval, validity windows, supported graph databases (read 20261102 20:12 UTC)
61. https://github.com/getzep/graphiti/blob/HEAD/graphiti_core/search/search_config_recipes.py and https://github.com/getzep/graphiti/blob/HEAD/graphiti_core/search/search.py : 16 named recipes and the rerankers (read 20261102 20:14 and 20:15 UTC)
62. https://github.com/getzep/graphiti/blob/HEAD/mcp_server/src/graphiti_mcp_server.py and https://github.com/getzep/graphiti/blob/HEAD/mcp_server/README.md : the 13 MCP tools, `add_memory` processed in the background, `center_node_uuid` on the two search tools (read 20261102 20:14 UTC)
63. https://arxiv.org/html/2501.13956 : the Zep paper (arXiv 2501.13956, 20 January 2025), the three search functions and the rerankers (read 20261102 20:15 UTC)

HippoRAG:

64. https://github.com/OSU-NLP-Group/HippoRAG/blob/HEAD/src/hipporag/HippoRAG.py and https://github.com/OSU-NLP-Group/HippoRAG/blob/HEAD/src/hipporag/utils/misc_utils.py : damping 0.5, undirected, seed weights, `passage_node_weight` 0.05, min-max normalisation, the fallback to dense retrieval, OpenIE (read 20261102 20:14 UTC)
65. https://arxiv.org/html/2502.14802 : HippoRAG 2 (arXiv 2502.14802, 20 February 2025), Table 5 on the passage weight, the "w/o Filter" ablation (read 20261102 20:14 UTC)

LightRAG:

66. https://github.com/HKUDS/LightRAG/blob/HEAD/README.md : extraction on every chunk, the keyword model, local reranking (read 20261102 20:12 UTC)
67. https://github.com/HKUDS/LightRAG/blob/HEAD/lightrag/operate.py : caller-supplied keywords, `only_need_context`, `rebuild_knowledge_from_chunks`, the relationship vector store (read 20261102 20:14 UTC)
68. https://github.com/HKUDS/LightRAG/blob/HEAD/env.example : a reranker served by vLLM through the cohere binding (read 20261102 20:14 UTC)
69. https://github.com/HKUDS/LightRAG/blob/HEAD/lightrag/lightrag.py : the `doc_status` storage and records (read 20261102 20:18 UTC)

LinearRAG:

70. https://github.com/DEEP-PolyU/LinearRAG/blob/HEAD/readme.md : relation-free graph construction, no LLM token cost, spaCy `en_core_web_trf` (read 20261102 20:14 UTC)
71. https://github.com/DEEP-PolyU/LinearRAG/blob/HEAD/src/config.py and https://github.com/DEEP-PolyU/LinearRAG/blob/HEAD/src/LinearRAG.py : configuration defaults, the keyword boost, sentence embeddings, NER results reused by passage hash (read 20261102 20:14 UTC)
72. https://github.com/DEEP-PolyU/LinearRAG/issues/25 : "Reproducibility concerns", opened 20260507, open; the maintainer's reply of 20260518 (read 20261102 20:14 UTC)

LogicRAG:

73. https://arxiv.org/html/2508.06105 and https://github.com/chensyCN/LogicRAG/blob/HEAD/README.md : LogicRAG (arXiv 2508.06105, AAAI 2026), the argument from graph-construction cost, the single embedding model, the efficiency sections (read 20261102 20:18 and 20:12 UTC)
74. https://github.com/chensyCN/LogicRAG/blob/HEAD/src/models/logic_rag.py : the warm-up check, the rolling summary, the topological sort, `max_rounds`, `fix_json_response` (read 20261102 20:14 UTC)

Microsoft GraphRAG:

75. https://microsoft.github.io/graphrag/index/methods/ : the standard and the fast indexing methods (read 20261102 20:14 UTC)
76. https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ : LazyGraphRAG, the relevance test budget, the win rates (read 20261102 20:14 UTC)
77. https://github.com/microsoft/graphrag/issues/1512 : "When will LazyGraphRAG arrive?", closed as not planned on 20251118 (read 20261102 20:14 UTC)

MiniRAG:

78. https://github.com/HKUDS/MiniRAG/blob/HEAD/README.md : the results table with four small models, the LiHua-World dataset (read 20261102 20:12 UTC)
79. https://arxiv.org/html/2501.06713 : MiniRAG (arXiv 2501.06713, 12 January 2025), indexing with small language models (read 20261102 20:15 UTC)
80. https://github.com/HKUDS/MiniRAG/blob/HEAD/minirag/operate.py and https://github.com/HKUDS/MiniRAG/blob/HEAD/minirag/minirag.py and https://github.com/HKUDS/MiniRAG/blob/HEAD/minirag/prompt.py : tuple delimiter, path-scoring imports, the LLM response cache, the query-to-keywords prompt (read 20261102 20:15 and 20:18 UTC)

Youtu-GraphRAG:

81. https://github.com/TencentCloudADP/youtu-graphrag/blob/HEAD/README.md : the seed schema, schema expansion, the four-level tree, the AnonyRAG link (read 20261102 20:12 UTC)
82. https://github.com/TencentCloudADP/youtu-graphrag/blob/HEAD/config/base_config.yaml : the extraction prompt that prioritises the schema but allows other knowledge (read 20261102 20:18 UTC)
83. https://github.com/TencentCloudADP/youtu-graphrag/issues/168 : schema growth on MuSiQue, opened 20261004, open, no comments (read 20261102 20:14 UTC)
84. https://huggingface.co/api/datasets/Youtu-Graph/AnonyRAG : the AnonyRAG dataset, licence cc-by-nc-4.0 (read 20261102 20:18 UTC)
85. https://arxiv.org/html/2508.19855 : Youtu-GraphRAG (arXiv 2508.19855, 27 August 2025), the seed schema, the expansion threshold, the anonymity-reversion task (read 20261102 20:15 UTC)
