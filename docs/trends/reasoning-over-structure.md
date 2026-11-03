---
type: trend
shift: similarity search -> a model reasoning over a document tree
status: growing
order: 5
updated: 20261102 23:27 UTC
---

# Vectorless retrieval: from similarity search to a model reasoning over a document tree

This page answers what changes when a retrieval system stops ranking chunks by vector similarity and instead lets a [large language model](../index/large-language-model.md) (LLM) read a tree and decide which part to open (called [vectorless retrieval](../index/vectorless-retrieval.md) by the README of [PageIndex](../projects/pageindex.md) [1]). It says which projects do this, what the evidence is, and who produced it. Almost every positive number comes from the authors of the method, and several outside tests find a plain baseline level or ahead.

> **Distinctive because** the structure is a tree taken from the document's own layout, mostly without a model at index time [1]; a prompted model chooses which node to open at query time. The nearest neighbour is [plain files as agent knowledge](./plain-file-knowledge.md), where a model reads its own pages [21].

## Why it emerged

The starting point is [retrieval-augmented generation](../index/retrieval-augmented-generation.md) (RAG) in its common form: documents are split into [chunks](../index/chunking.md), turned into [embeddings](../index/embedding.md), and the nearest ones are returned, as in the vector baseline of Vectify's cookbook [4] ([how this era came about](../history/language-models-meet-retrieval.md)). PageIndex's README argues that on long professional documents this fails: "similarity ≠ relevance" [1]. It says similarity search "misses what is relevant but not similar" [1]. This is the project's claim, not a measured finding.

The other answer to hard questions was to build a graph first ([graph-based RAG](./graph-based-rag.md)). It costs a lot to build. The documentation of [Microsoft GraphRAG](../projects/microsoft-graphrag.md) estimates that graph extraction is "roughly 75% of indexing cost" [22]. The LogicRAG paper calls the corpus-to-graph step a source of "overwhelming token cost and update latency" [15]. On 20260814 Microsoft's repository added a notice: since July 2024 "the capabilities of frontier models have changed dramatically" and the project is "largely in maintenance mode" [22].

*Reading:* the tree route moves work from index time to query time. It builds a cheap structure once and pays for a strong model on every question. PageIndex's own advice fits this: "a basic model is sufficient" to index, and for answering "use the best model you can afford" [1]. No source read states that stronger models caused the shift; the link is this page's inference.

Two other trends sit close. [Agentic search](./agentic-search.md) builds nothing and lets an agent search raw text [19][20]. [Agentic graph retrieval](./learned-graph-traversal.md) is a different case: a trained policy walks a graph, where here a prompted model reads a tree.

Dates: RAPTOR, an ancestor that builds a tree by clustering embeddings, was posted 20240131 [17]. The PageIndex repository was created 20250401 [2], and its README asks to be cited as a blog post of September 2025 [1][2].

## Why it matters

- **Long structured documents.** Annual reports, filings and manuals have headings a reader uses. The method keeps that structure instead of discarding it [1].
- **Traceability.** Answers point to explicit sections and pages, which a similarity score does not give [1] (first-party claim).
- **Cost moves, it does not vanish.** Vectify says local indexing costs about $0.001 per page [1]. Each question then runs an agent loop: $110 per 1,000 queries in its cookbook, against $16 to $135 for four vector runs [4] (first-party; the pricing rule is under "What is measured").
- **A different failure.** The paper of the team behind [RAGFlow](../projects/ragflow.md) argues that a confident wrong branch is worse than open search, and that routing errors compound with depth (an analytic argument there, not a measured sweep) [11].

## How it works

Two steps [1]: build a tree, then let a model search it.

**Build.** The tree comes from the document's layout (headings, table of contents, page ranges). PageIndex says the structure "is extracted from the document layout without an LLM"; a model only summarises and refines nodes [1]. Other systems take the tree from a table of contents or sitemap [13] or from a model's extraction [9].

**Navigate.** At query time the model sees node titles and summaries, picks nodes, reads the pages they cover, and repeats [1][13]. No embedding is used for the lookup. This is [tool use](../index/tool-use.md) by an [agent](../index/agent.md) over a [tree index](../index/tree-index.md).

| Variant | Built at index time | At query time | Source |
|---|---|---|---|
| PageIndex | tree from layout; model writes summaries | model opens nodes in an agent loop | [1] |
| RIT-RAG | tree per document from table of contents or sitemap | retrieval proposes chunks; their positions induce sub-trees; an agent navigates | [13] |
| DecisionRAG | the corpus's inherent structure | a pretrained decision model (Jev; its size is unstated in the text read) judges candidate branches in one forward pass, no tokens generated | [14] |
| RAGFlow compilation | a model generates Graph, Tree, PageIndex, Mindmap, Timeline or Wiki artifacts | artifacts are "auxiliary information" for retrieval; how is not stated in the docs read | [9] |
| LogicRAG | nothing | a graph of sub-questions is built per question and ordered | [15] |

Boundary cases. LogicRAG builds no corpus structure at all. KITE, a vector-free memory system, builds a governed topic index and compiles each question into a plan that fixed lookup operations execute [18]; nothing walks the structure by reasoning. RAGFlow's Tree template clusters claims extracted from chunks and summarises the nodes [9], and it took the place of its earlier RAPTOR feature [10].

*Reading:* that makes RAGFlow's Tree closer to RAPTOR than to a layout tree.

## Representative projects

Stars are signals from the dated snapshot (20261030 19:54 UTC) [3], not verdicts. Licences are from the LICENSE files [2][8][25][26].

| Project | Licence | Stars | Note |
|---|---|---|---|
| [PageIndex](../projects/pageindex.md) | MIT | 39,913 | Vectify's tree-index SDK (software development kit); v0.5.0 on 20261029; last push 20261029 [2][3] |
| [RAGFlow](../projects/ragflow.md) | Apache-2.0 | 93,209 | a RAG platform, not a tree project; added "Knowledge Compilation" on 20260819 [8][3] |
| [OpenKB](https://github.com/VectifyAI/OpenKB) | Apache-2.0 | 4,831 | Vectify's knowledge-base tool; quiet, last push 20260722 [3][25] |
| [KITE](https://github.com/memoket/memoket-kite) | Apache-2.0 | 230 | vector-free memory engine, a boundary case [3][26] |
| [LogicRAG](https://github.com/chensyCN/LogicRAG) | GPL-3.0 | 241 | boundary case, builds no corpus structure; quiet; read-only reference, ideas and results only [3][25] |

Two cautions. First, RAGFlow's PageIndex template has a model extract sections and an "include" relation [9]. The RAGFlow team's own paper says of its navigation tool and its graph explorer: "In our benchmarks neither tool showed significant value." It also says they are not used when a navigation tree is compiled [11].

*Reading:* RAGFlow is therefore a representative of compiling trees, not of a model walking them.

Second, the [Dify](../projects/dify.md) 1.18.0 notes (20261023) announce an opt-in Agent Knowledge Base beta and do not say it builds a tree: **unstated** [24].

## Fundamental papers

The relations among these papers are on [the group page](../papers/reasoning-over-structure.md), which keeps RAPTOR and Lumer et al. as fundamental; the others named below are, at most, in its further reading. PageIndex has no paper in the sources read; its README asks to be cited as a blog post [1].

- RAPTOR, 2024, the tree ancestor [17].
- LogicRAG, 2025, reasoning structure at query time instead of a built one [15].
- Lumer and others, 2025, the first head-to-head of vector agentic RAG and node-based reasoning [12].
- RIT-RAG and DecisionRAG, 2026, two answers to the scale limit [13][14].
- The RAGFlow team's compilation paper, 2026: no accuracy gain from any structural artifact on FRAMES, and a claim-evidence navigation tree that cut query tokens by 38% on average [11].

## What is measured, and by whom

| Who | Setup | Result | First-party? |
|---|---|---|---|
| Vectify, cookbook, run 20261016 | 63 questions on five annual reports of one company; vector search at top-k 10, 30, 50, 100 | PageIndex 100.0%; vector 54.0, 74.6, 79.4, 87.3% [4] | yes. Vector cost is priced without the [prompt cache](../index/prompt-caching.md), PageIndex with its cache hits [4] |
| Vectify, Financial question-answering (QA) benchmark | 100 questions, 40 filings; PageIndex fixed, model varied | highest 98.7%, lowest 65.7% across 37 configurations [5] | yes. No vector baseline |
| Vectify, FinanceBench | public set | 98.7% for Mafin 2.5, built on PageIndex; ambiguous questions settled by human annotation [7] | yes. The system is Mafin 2.5, not the current SDK |
| Vectify, Page Search benchmark | 80 questions | its newer Page Search API finds evidence pages better than three embedding models [6] | yes. It "reads every page" against the question, so it is not a tree walk [6] |
| Lumer and others, 20251122 | 150 questions over 1,200 filings to the US Securities and Exchange Commission (SEC); their own node-based system, whose node tree cites PageIndex as its basis | vector agentic RAG won 68% of comparisons; node-tree generation $30.62 per average 10-K with GPT-4o in their Table 1 (their later tables give $6.12 with node summaries and $0.97 without, unreconciled) [12] | no, a third party, but the implementation is theirs |
| RIT-RAG authors, 20261008 | their own reimplementation of "PageIndex", where a document retriever first picks one document | RIT-RAG ahead of it by 2.0 to 18.6 points; the top of the range is FinanceBench with induced tables of contents. In the same table, agentic search with no structure beat their PageIndex baseline on QASPER (about 86 against 75 to 77) and on all three FinanceBench settings, and trailed it on WixQA in two of three [13] | no, but their method is the winner |
| DecisionRAG authors, 20261026 | four benchmarks | +13.8 R@1 (recall at the first result) and +17.4 Hit@1 (the first result is correct) over [dense retrieval](../index/dense-retrieval.md) with an 8B [reranker](../index/reranking.md) [14] | yes |
| RAGFlow team, 20261030 | FRAMES, each variant run once; the token figures use 200 questions | no accuracy gain from any structural artifact; the PageIndex-style outline, which RAGFlow built itself (not the PageIndex SDK) and ran with its claim leaves removed, was "neutral at small scale and harmful at FRAMES scale". A navigation tree with claim-evidence leaves cut query tokens by 91% when the evidence sufficed and by 38% on average, and roughly tripled latency on a paired subset of 7 questions [11] | partly: it is their own product's paper |
| Hashmi, v2 20261028 | 22 queries over four short documents, one run; then 50 FinanceBench questions with the benchmark's evidence snippets as corpus | tree 0.900 against vector 0.845 and the author's adaptive hybrid 0.845; on FinanceBench tree 0.938, hybrid 0.901, vector 0.821. The tree was given the target document and longer answers; the author says differences "cannot be attributed to retrieval architecture alone" [16] | no, one author, preliminary |

No scored independent run of the PageIndex SDK was found in the sources read. Nearby tests of other kinds contain no tree and found plain retrieval strong: raw dense retrieval first in six of seven settings in conversation memory [19], and grep above vector retrieval on a 116-question sample [20]. Experiment [X3](../experiments/x3-matched-cost-comparison.md) proposes to compare [BM25](../index/bm25.md), a hybrid retriever, one cheap graph builder and one navigation method at matched cost on one corpus; it had not started on 20261102 [27].

Paper volume: the arXiv query in source 23 returned 19 keyword hits for submissions from 20251102 to 20261102 and 4 for the year before, read 20261102 20:22 [23]. These counts are noisy: about half of the 19 are off-topic by title (video, music, person re-identification, temporal graphs), the 4 of the earlier year were not checked for topic, and DecisionRAG [14] is not among the 19, so recall is also incomplete. A repeat at 20:36 was refused (HTTP 429).

## Assessment

*Reading:* the idea has a plausible case on long documents with clear headings. The positive numbers are first-party and consistent across the vendor's own runs, but the Financial QA benchmark has no vector baseline [5]. Outside tests are mixed and mostly weak for trees:

- a third party found vector agentic RAG ahead [12];
- in the RIT-RAG table, agentic search with no structure beat the authors' PageIndex baseline on QASPER and on FinanceBench, though PageIndex led it on WixQA in two of three settings [13];
- a BM25-and-grep harness reached 91% on FRAMES, and no structural artifact in the RAGFlow team's own test added accuracy to it [11];
- the one small test favouring trees (two comparisons by one author, tree ahead of vector in both) was qualified by its author, because the tree was given the target document and the configurations differed in prompts [16].

The method also struggles where a tree does not exist or does not fit: RIT-RAG's authors say the structure of a large corpus cannot fit in a model's [context window](../index/context-window.md) [13].

Status is `growing`, a low-confidence call. The paper counts are too noisy to rank: 19 keyword hits against 4, about half of the 19 off-topic and the 4 unchecked, set against general rises of 1.2 to 2.5 times [23]. The call rests instead on one large, active project [3] and on three on-topic papers found by hand in October 2026 alone [11][13][14]. Direction: hybrids in which retrieval proposes where to look and a model decides what to read [13], and vendors placing page scoring and compiled artifacts beside the tree walk [6][9].

## Signals to watch

- A scored run of PageIndex's released SDK by someone other than Vectify, and any published test of its Cloud-only File System, the README's answer to corpus scale [1].
- RAGFlow 1.0.0 final (rc3 was 20261030) and documentation of how Tree and PageIndex artifacts are read at query time [8][10].
- Dify's Agent Knowledge Base leaving beta, with a statement of what it builds [24].
- Whether Vectify's tree product or its page-scoring product gets the new work [1][6].
- A result from X3, or a replication of Lumer's 1,200-filing test with a current tree system.

## Sources

Read times are UTC on 20261102.

1. https://github.com/VectifyAI/PageIndex (README via the GitHub API) : description, tree from layout without a model, index-model advice, $0.001 per page, updates of 2026, blog citation (read 20261102 20:09; README reread 20261102 20:36)
2. https://github.com/VectifyAI/PageIndex : creation date 20250401, MIT LICENSE text, v0.5.0 of 20261029 (read 20261102 20:09; creation date and licence field reread 20261102 20:36; the latest-release call was run again 20261102 22:52 UTC with the same result)
3. kb-kg/landscape/20261030_1954-github/repos.tsv, in the [archive](../../kb-kg/landscape/20261030_1954-github/repos.tsv) : stars and push dates of 20261030 19:54 UTC (read 20261102 20:18)
4. https://github.com/VectifyAI/PageIndex/blob/main/cookbook/pageindex-vs-vector-10k/pageindex-vs-vector-10k.ipynb : 63 questions, accuracy, cost per 1,000 queries, pricing rule, run of 20261016 (read 20261102 20:16)
5. https://github.com/VectifyAI/pageindex-benchmarks/blob/main/financial-qa/README.md : 37 configurations, 100 questions, 98.7% and 65.7% (read 20261102 20:16)
6. https://github.com/VectifyAI/page-search-benchmark : Page Search API against embeddings; "reads every page" (read 20261102 20:16)
7. https://github.com/VectifyAI/Mafin2.5-FinanceBench : 98.7%, protocol, human annotation of ambiguous cases (read 20261102 20:17)
8. https://github.com/infiniflow/ragflow (README, repository data, LICENSE) : Apache-2.0, 20260819 compilation entry, v1.0.0-rc3 (read 20261102 20:09; the latest-release call was run again 20261102 22:52 UTC with the same result, published 20261030)
9. https://github.com/infiniflow/ragflow/tree/main/docs/guides/knowledge_compilation : artifact types, Tree and PageIndex templates (read 20261102 20:10; template page reread 20261102 20:36)
10. https://github.com/infiniflow/ragflow/blob/main/docs/release_notes.md : v0.27.0 replaced RAPTOR and GraphRAG features with Tree and Graph (read 20261102 20:10)
11. https://arxiv.org/abs/2610.41172 and https://arxiv.org/html/2610.41172v1 : RAGFlow team, Context as Infrastructure, v1 20261030; FRAMES audit; navigation tool and graph explorer; 91% and 38% token results; latency (read 20261102 20:11; sections 8 and 6 reread 20261102 20:35)
12. https://arxiv.org/abs/2511.18177 and https://arxiv.org/html/2511.18177 : Lumer and others, v1 20251122; Tables 1 to 3 and section 4.2 (read 20261102 20:11; tables reread 20261102 20:35)
13. https://arxiv.org/abs/2610.11370 : RIT-RAG, v1 20261008, v2 20261016; Table 1, section 5, Appendix B (read 20261102 20:17; reread 20261102 20:35)
14. https://arxiv.org/abs/2610.35868 : DecisionRAG, v1 20261026; Jev decision model, task-trained models (read 20261102 20:11; reread 20261102 20:35)
15. https://arxiv.org/abs/2508.06105 : LogicRAG, v1 20250808 (read 20261102 20:11)
16. https://arxiv.org/abs/2604.14222 : Hashmi, v1 20260414, v2 20261028; abstract, Tables 2 and 5, limitations (read 20261102 20:11; v2 reread 20261102 20:35)
17. https://arxiv.org/abs/2401.18059 : RAPTOR, v1 20240131 (read 20261102 20:11)
18. https://arxiv.org/abs/2610.41521 : KITE, v1 20261030 (read 20261102 20:11)
19. https://arxiv.org/abs/2610.30755 : Raw-RAG, v1 20261022 (read 20261102 20:11)
20. https://arxiv.org/abs/2605.15184 : Is Grep All You Need, v1 20260514 (read 20261102 20:11)
21. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f : LLM Wiki gist, index.md read first (read 20261102 20:17)
22. https://github.com/microsoft/graphrag (README) and https://microsoft.github.io/graphrag/index/methods/ : maintenance notice; 75% estimate (read 20261102 20:18)
23. https://export.arxiv.org/api/query : query `(abs:vectorless OR abs:"embedding-free" OR abs:"vector-free" OR abs:"reasoning-based retrieval" OR abs:"reasoning-based RAG" OR abs:PageIndex OR abs:"non-vector" OR abs:"index-free") AND (abs:RAG OR abs:retrieval)` with submittedDate 202511020000 to 202611022359: 19 results; 202411020000 to 202511012359: 4 results (read 20261102 20:22). Growth controls (carried over, not re-run: the arXiv API refused repeated calls with HTTP 429 on 20261102): any LLM wording 1.38 times, any RAG wording 1.23 times, LLM-agent wording 2.50 times, window against the prior year, as read by this documentation's trends research on 20261102 between 19:46 and 19:47 UTC and recorded in its catalogue of the same day. On a repeat at 20:36 the API again answered HTTP 429, so neither count was re-confirmed and the earlier window's 4 results were not checked for topic
24. https://github.com/langgenius/dify/releases/tag/1.18.0 : Agent Knowledge Base beta (read 20261102 20:17)
25. https://github.com/VectifyAI/OpenKB and https://github.com/chensyCN/LogicRAG : repository data and LICENSE files (read 20261102 20:16)
26. https://github.com/memoket/memoket-kite : repository data, LICENSE, "vector-free" README (read 20261102 20:16)
27. [Experiment page X3](../experiments/x3-matched-cost-comparison.md) : proposal, conditions, status of 20261102 (read 20261102 20:09)
