# Graph, RAG and agents: what the research found

**Status:** moved from a July 2026 literature review, re-verified and extended · **Original date:**
20260725 15:12 UTC (file modification time; the review predates its commit) · **Re-checked:**
20261030 18:59 to 19:00 UTC · **Scope:** when a graph helps retrieval, what it costs, and where the
field is heading. Field-neutral.

How to read the marks. Every load-bearing figure from the July text is listed in the
[verification ledger](#verification-ledger) with one of three marks:

| Mark | Meaning |
|---|---|
| **confirmed** | A source fetched in this run states it. |
| **changed** | A fetched source states something different, or only part of it. The ledger says what. |
| **unverifiable** | No fetched source states it. The figure is kept as the July text had it, flagged, and not relied on. |

Sources are numbered `[n]` and listed at the end with the time each was read. A search-engine
summary is not a source: where a number comes only from one, the text says so.

---

## 1. The question

Relational structure is what lets a retrieval system answer *"which contracts were signed by someone
who also approved the amendment"*. Flat vector similarity cannot reach that: the answer exists only
in the relationships between chunks, never inside any one of them.

The obvious way to get that structure is to extract it up front. An LLM reads the whole corpus, pulls
out entities and relations, builds a knowledge graph, and the graph is queried. That is Microsoft
GraphRAG, and it works. It is also the most expensive thing one can do to a corpus: the cost is
paid at indexing, scales with the corpus rather than with usage, and recurs whenever the corpus changes.

So the question is not whether structure is valuable. It is **how much of it can be had without paying
for LLM extraction over the whole corpus**. A side effect worth naming: a pipeline that treats
re-indexing as free (so that chunking or embedding models can be changed at will) loses that property
once indexing needs LLM calls.

---

## 2. What the research found

### 2.1 Prebuilt graphs are expensive to index

Full GraphRAG's cost is concentrated in indexing and scales with the corpus. July text: a moderately
sized document set runs $5 to $20 in API calls to index, and one reported enterprise case reached about
$47,000 to index 100,000 internal documents, before answering a single question.

Re-check, 20261030 19:00 UTC:

- The cost warning is **confirmed** qualitatively. The GraphRAG README says indexing "can be an
  expensive operation" and to "start small" [16].
- Neither dollar figure is **confirmed** (see the ledger). The nearest published number is an
  order-of-magnitude estimate of about $10,000 for 100,000 documents, from a July 2026 paper that
  assumes about 40,000 tokens per document on a commercial API at $2.50 per million input tokens [9].
  Search summaries mention figures from about $10,000 to over $50,000 for the same scale, depending on
  model and document length [17]. The size of the range, not any single figure, is what the sources support.

### 2.2 The field has moved away from prebuilding

| Work | Claim (July wording) | Re-check |
|---|---|---|
| **LazyGraphRAG** (Microsoft Research, blog 20241125) | Defer LLM summarisation to query time. Index cost about 0.1% of GraphRAG, the same as plain vector RAG, with about 700 times lower global query cost. | **confirmed** for both figures [1]. **Changed:** the June 2025 editor's note says it was integrated into Microsoft Discovery and Azure Local "as part of a public preview", not production [1]. |
| **You Don't Need Pre-built Graphs for RAG** (arXiv 2508.06105, AAAI 2026) | Build only the reasoning structure a query needs, per query. | **confirmed** [3]. Title continues "...: Retrieval Augmented Generation with Adaptive Reasoning Structures". The method is called LogicRAG: it splits a query into sub-problems, models their dependencies as a directed acyclic graph and prunes it. v1 20250808. The abstract gives no numbers. |
| **EcphoryRAG** (arXiv 2510.08958, 2025) | Index entities only, infer relations at query time. About 94% fewer tokens at indexing, state of the art on 2WikiMultiHop, HotpotQA, MuSiQue. | **changed** [4]. The abstract says "up to 94%" fewer tokens than other structured RAG systems, and average exact match 0.474 against 0.392 for HippoRAG on those three benchmarks. The words "state of the art" are not in the abstract as returned by the fetch tool: **unverifiable**. v1 20251010. |
| **HippoRAG 2** (arXiv 2502.14802, ICML 2025) | Light entity graph, work at query time with Personalized PageRank. About 10 times more efficient than GraphRAG, better on multi-hop. | Venue **confirmed**; v1 20250220; title is "From RAG to Memory: Non-Parametric Continual Learning for Large Language Models" [7]. The abstract reports a 7% gain on associative-memory tasks. The "10 times" figure is **unverifiable**: the abstract has no efficiency comparison and the PDF text was not readable by the fetch tool. |
| **SubQRAG** (arXiv 2510.07718, 2025) | Decompose the question, retrieve per sub-question, extract new triples only where the graph fell short. | **confirmed** [5]. v1 20251009. The abstract reports "consistent and significant improvements, especially in Exact Match" on three multi-hop benchmarks, with no numbers. 5 pages. |
| **Graph-R1** (arXiv 2507.21892, ICML 2026) | Train an agent to traverse: think, query, retrieve subgraph, rethink; reinforcement learning end to end. | Venue **confirmed**: "Accepted by ICML 2026 main conference" [6]. v1 20250729, v2 20260602. It builds a lightweight knowledge hypergraph and frames retrieval as multi-turn agent-environment interaction. The abstract gives no numbers. |

The through-line, as the July text put it: **the graph stopped being an artefact built once and became a
structure grown while reasoning.** That reading is an interpretation of the table, not a measured result.

### 2.3 Graph retrieval is not a free win: it is a routing decision

July text: GraphRAG-Bench (ICLR 2026) and related analyses report GraphRAG underperforming vanilla RAG
on ordinary factual lookup, one study measuring about 13% lower accuracy on Natural Questions and worse
on time-sensitive queries. Practitioner benchmarks show the split from the other side: graph retrieval
at about 91% on multi-hop relational queries where vector RAG manages about 34%, while losing badly to
structure-aware chunk retrieval (about 97% against 72%) when the answer is one date or clause in one
known document.

Re-check:

- The direction is **confirmed** by independent sources. The GraphRAG-Bench abstract says GraphRAG
  "frequently underperforms vanilla RAG on many real-world tasks" [2]. On Natural Questions, plain RAG
  has the best F1 in a systematic comparison [8]. The HippoRAG 2 abstract also says recent
  structure-augmented approaches do considerably worse than standard RAG on basic factual memory
  tasks (paraphrase of the abstract) [7].
- The specific numbers are not reproduced (see the ledger). Where a source gives a number it is
  different or on a different metric.
- **Reading, as the July text had it:** a graph layer is best treated as an additive channel chosen per
  query type, not a replacement for a hybrid text pipeline. This is a reading of the evidence above and
  of section 3 below, not a measured result.

---

## 3. Evidence since July 2026

Searched with the alphaXiv paper index on 20261030 at 18:59 UTC, for papers first published from
20260701, ranked by recency [18]. The six rows are the ones read (abstract and results). Results are
as reported by the authors. Dates are the first arXiv version unless a later one is named.

| arXiv id | Date | What was compared | Result | Caveat |
|---|---|---|---|---|
| 2609.18099 [10] | 20260916 | EffiRAG (graph used to locate source chunks, LLM extraction once per chunk, no community summaries) against LightRAG-hybrid, PathRAG, NaiveRAG, HyDE, BM25-vector, on UltraDomain (4 domains, 120 questions) | Preferred over LightRAG-hybrid on 93 questions, lost 7, 20 splits. Total cost $0.408 against $0.952 (57.1% lower). NaiveRAG costs $0.139 and EffiRAG beat it 58/15/47; BM25-vector $0.145, 43/21/56. With LLM extraction replaced by non-LLM noun-phrase extraction the cost was $0.226 and EffiRAG won 44, lost 26, 50 splits. At 10 and 20 documents per domain, with a non-LLM salience filter, 4.2 and 4.5 times cheaper than LightRAG-hybrid ($2.316 against $9.799; $3.238 against $14.608). | Questions are LLM-generated; judging is pairwise by GPT-4o-mini; one answer model; main comparison is 5 documents per domain. The authors write that under tight cost constraints non-graph retrievers "may be more practical" though lower in quality. Dollar costs depend on provider prices and exclude local compute. |
| 2610.30755 [11] | 20261022 | RAW-RAG (dense retrieval plus cross-encoder rerank over raw conversation history, no extraction, no graph) against 12 agentic memory systems, on LoCoMo, LongMemEval, MEME, MemoryAgentBench | First among the compared memory systems in 6 of 7 benchmark-model settings, by 0.13 to 5.53 points. Sequential ingestion of a 1M-token history took 0.3 h against 3.2 to 27.0 h for the others. Adding graph-based retrieval expansion, atomic-fact extraction or summaries to RAW-RAG did not improve its 48.32 on MemoryAgentBench. | Conversation-memory tasks, not document corpora. Graph retrieval is one ablation, not the paper's subject. Full-context prompting beat RAW-RAG by 19.98 points in one setting. The authors state the evidence is limited to offline conversation on public benchmarks. |
| 2610.18410 [12] | 20261013 | Graph structure folded into embeddings offline (five transformations), used without any query-time graph access, against plain vector retrieval | Used as a direct replacement, every transformation recovered less gold evidence than the original embeddings (73.1%): 52.4% to 72.9%. In a multi-stage retriever the best setting recovered 60.8% against 51.0% on 527 harder questions (+9.8 points, 19.2% relative; +25.9% on extremisation questions, +10.0% on relational ones), and matched plain retrieval with 24 returned nodes instead of 40. Controls without graph conditioning reached 54.7% and 55.5%. The three-hop question family (baseline 20.1%) was not improved by either requery schedule; the best strategy added 11.8 points. | Synthetic professional-network benchmark (about 1,200 chunks, 977 validation questions). Metric is evidence recovery, not answer accuracy. One embedding model. Authors are from the company that makes the graph memory framework used. The authors list natural corpora and graphs with errors as untested. |
| 2609.19622 [13] | 20260917 (v2 20261026) | G3RAG: a document graph built from vector geometry with zero LLM tokens, then one diffusion step from LLM-filtered seed documents, against NaiveRAG, LightRAG, RAPTOR, HippoRAG 2, LinearRAG on 1,000 cases from MuSiQue, 2WikiMultiHopQA, HotpotQA | Average F1 66.49 against 64.49 for HippoRAG 2 and 60.62 for naive dense retrieval (one embedding model). LightRAG averaged 28.97, below naive RAG. Graph-construction tokens: LightRAG 86.80 million, HippoRAG 2 14.47 million, G3RAG zero. Personalized PageRank run on the same graph averaged 65.65. | Without the LLM seed-filtering step G3RAG averaged 60.53, no better than naive RAG (60.62), so an LLM is still used at query time. Short Wikipedia-style passages. The dense construction is quadratic in documents; the sparse version was measured for indexing time and latency only, on synthetic copies up to 100,000 documents, not for accuracy. For the alternative search strategies run on the same graph, the edge over HippoRAG 2 shows in average F1 but not in average exact match (Personalized PageRank 53.77 against 54.30). Authors' own method. |
| 2608.28766 [14] | 20260828 | Classical vector RAG against a hybrid of vector search, GraphRAG community summaries and a cross-encoder, on Amazon climate science papers | Reported gains of 160% in contextual relevance and 177% in contextual recall (judge-model metrics). | 22 questions written by the authors, one domain, LLM judges. The two systems differ in more than the graph: embedding model, reranker, chunk size, title injected into chunks, and 2 against 5 chunks passed to the generator. The gain cannot be attributed to the graph alone (reading of the paper's setup). All judges rated correctness below 0.40 for the hybrid. |
| 2607.11683 [9] | 20260713 | RAGU (typed two-stage extraction, consolidation, Leiden communities) against LightRAG and HippoRAG 2 on GraphRAG-Bench (Medical), BioASQ, MuSiQue, 2WikiMultiHopQA | Published 12 days before the July review and not cited by it. On fact retrieval HippoRAG 2 scored answer correctness 72.4 against 54.2 for RAGU and 26.2 for LightRAG; on creative generation RAGU led (59.0 against 56.9) and led on coverage (57.4 against 34.7). With terse answer prompts, MuSiQue: HippoRAG 2 54.4, RAGU 40.1, plain NaiveRAG 36.6; BioASQ: NaiveRAG 71.7, HippoRAG 2 72.4, RAGU 72.9. | Authors' own system. Under verbose prompts HippoRAG 2 led every column, which the authors call largely an answer-format artefact. Indexing costs for MS-GraphRAG are an order-of-magnitude estimate, not a measurement. |

**What the new evidence does to the July conclusions**

| July conclusion | Since July |
|---|---|
| Prebuilt LLM-extracted graphs are costly | Supported. 2609.19622 reports 86.80 million construction tokens for LightRAG against zero for a non-LLM graph [13]. 2609.18099 reports a 57% cost cut from a cheaper graph design [10]. |
| Plain RAG is a strong baseline that graph methods must beat | Supported. 2610.30755 shows a plain dense-plus-rerank baseline ahead of 12 more complex memory systems in most settings [11]. In 2609.19622 and 2607.11683, LightRAG scores below naive RAG on several benchmarks [13][9]. |
| Light, query-time graph use is where the gains are | Partly supported. Personalized PageRank retrieval (HippoRAG 2) leads on single-fact and multi-hop questions in [13] and [9]. A non-LLM graph with PageRank also beat naive retrieval in [13], but that result still used an LLM to choose seeds. |
| Graph retrieval pays only on multi-hop questions | Changed: see the ledger. Gains are also reported on coverage-heavy synthesis tasks [9], and one of the three multi-hop benchmarks in [9] (BioASQ, terse prompt) shows a tie with plain RAG. |
| Cost and quality must be reported together | Supported by [10], which reports both, and by [9], which shows that the answer-prompt format alone can reverse a ranking. |

**Found by the search but not read** (candidates, not evaluated): 2609.10239 LiteRAG, 2610.22818
FuseRAG, 2609.11065 MOSAIC, 2608.16004 LineageRAG, 2610.11370 RIT-RAG, 2609.23315 on graph memory across
graph database engines [18].

---

## 4. Prior art worth tracking

Stars and licence read from the GitHub API on 20261030 at 18:59 UTC [15]. The licence field there is
GitHub's detection from the repository's licence file. The "July description" column is the July text
and was not re-read in this run; per-project facts belong in the project entries of this reference.

| Project | Stars, July (mid-2026) | Stars, 20261030 | Licence | Last push | July description (not re-verified) |
|---|---|---|---|---|---|
| [LightRAG](https://github.com/HKUDS/LightRAG) | ~28k | 40,443 | MIT | 20261029 | Dual-level entity/relation indexing; most actively developed in the space; has retrieval modes chosen per query. |
| [microsoft/graphrag](https://github.com/microsoft/graphrag) | ~31k | 36,498 | MIT | 20261029 | Reference implementation and the cost case study. July: LazyGraphRAG is not yet in the open-source library. The README, read 20261030, does not mention LazyGraphRAG [16]: **unverifiable** beyond that. Latest release v3.3.0, 20261008. |
| [Graphiti](https://github.com/getzep/graphiti) | ~20k | 32,372 | Apache-2.0 | 20261028 | Incremental, bi-temporal graph built for agent memory; no batch summarisation; ships an MCP server. |
| [HippoRAG 2](https://github.com/OSU-NLP-Group/HippoRAG) | ~2k | 4,083 | MIT | 20261006 | Personalized PageRank retrieval over a light entity graph. |
| [fast-graphrag](https://github.com/circlemind-ai/fast-graphrag) | ~800 | 3,967 | MIT | 20251101 | PageRank exploration and incremental updates, about 6 times cheaper than GraphRAG (the project's own wording; the [fast-graphrag entry](../projects/fast-graphrag.md) works out 2.6 times fewer tokens from an independent benchmark's figures, by its own arithmetic). **No push for about a year**; the July star count is far below the current one and cannot be checked. |
| [Graph-R1](https://github.com/LHRLAB/Graph-R1) | ~400 | 599 | MIT | 20260430 | ICML 2026; reinforcement-learned traversal. |
| [Awesome-GraphRAG](https://github.com/DEEP-PolyU/Awesome-GraphRAG) | not given | 2,682 | MIT | 20260602 | Running bibliography. |

**Papers named in the July text**, with what this run could confirm: LazyGraphRAG (Microsoft Research
blog, 20241125) [1] · *You Don't Need Pre-built Graphs for RAG* (arXiv 2508.06105, AAAI 2026) [3] ·
*When to use Graphs in RAG* / GraphRAG-Bench (arXiv 2506.05690, v1 20250606, v3 20260222; venue ICLR 2026
is named by a citing paper [9], not on the arXiv page [2]) · SubQRAG (arXiv 2510.07718) [5] · EcphoryRAG
(arXiv 2510.08958) [4] · Graph-R1 (arXiv 2507.21892) [6] · HippoRAG 2 (arXiv 2502.14802) [7] ·
*RAG vs. GraphRAG: A Systematic Evaluation and Key Insights* (arXiv 2502.11371, v1 20250217, v3 20260304)
[8], added in this run.

---

## 5. Verification ledger

Checked 20261030, 18:59 to 19:00 UTC.

| # | July claim | Mark | What the source says | Source |
|---|---|---|---|---|
| V1 | GraphRAG indexing costs $5 to $20 for a moderately sized document set | **unverifiable** | No fetched source gives this figure. Qualitative cost warning confirmed. A search summary gave "$50 to $200 for a 500-page corpus" from a blog, which is a different scale and was not opened [17]. | [16], [17] |
| V2 | One enterprise case hit about $47,000 to index 100,000 documents | **unverifiable** | The search found no source for the figure. Nearest: about $10,000 per 100,000 documents, an order-of-magnitude estimate (about 40,000 tokens per document, $0.10 per document, commercial API) [9]; search summaries cite over $50,000 per 100,000 pages and $33,000 for large enterprise sets, neither opened [17]. $47,000 sits inside the range of published estimates; none states it. | [9], [17] |
| V3 | LazyGraphRAG: index cost 0.1% of GraphRAG, equal to vector RAG | **confirmed** | "LazyGraphRAG data indexing costs are identical to vector RAG and 0.1% of the costs of full GraphRAG." Published 20241125. | [1] |
| V4 | LazyGraphRAG: about 700 times lower global query cost | **confirmed** | "more than 700 times lower query cost". The excerpt read does not name the baseline for this figure; a separate statement on the page compares against GraphRAG global search ("4% of the query cost of GraphRAG global search"). | [1] |
| V5 | LazyGraphRAG reached Azure production in June 2025 | **changed** | Editor's note dated 20250606: integrated into Microsoft Discovery and Azure Local services "as part of a public preview". Not described as production. | [1] |
| V6 | GraphRAG underperforms vanilla RAG on ordinary factual lookup | **confirmed** (direction) | GraphRAG-Bench abstract: "frequently underperforms vanilla RAG on many real-world tasks". On Natural Questions (Llama-3.1-8B), F1: RAG 64.78, Community-GraphRAG Local 63.01, Global 54.48, KG-GraphRAG triplets plus text 50.27, triplets only 34.28, HippoRAG 2 61.03, RAPTOR 60.04. | [2], [8] |
| V7 | About 13% lower accuracy on Natural Questions | **unverifiable** | The metric in [8] is F1, not accuracy. The gap to plain RAG ranges from 1.8 F1 points (Community-GraphRAG Local) to 30.5 points (KG-GraphRAG triplets only), depending on variant. No variant gives 13%, and it is unknown which study the July text meant. | [8] |
| V8 | GraphRAG-Bench appeared at ICLR 2026 | **confirmed** (secondary) | The arXiv page names no venue. A July 2026 paper cites it as "In International Conference on Learning Representations (ICLR 2026)". | [2], [9] |
| V9 | Worse still on time-sensitive queries | **unverifiable** | Not found in the abstracts read. The last 23,823 characters of [8]'s HTML were not read. | [2], [8] |
| V10 | Graph retrieval about 91% against 34% on multi-hop relational queries; chunk retrieval about 97% against 72% on single-clause lookup | **unverifiable** | The search found no source with these numbers. It surfaced vendor and blog figures that differ: a vendor benchmark with 82.3% (graph) against 41.5% (vector) on multi-hop, a blog with 71.17% against 65.77% on MultiHop-RAG, a vendor-AWS post with 80% against 50.83%. These are search summaries; the pages were not opened [17]. | [17] |
| V11 | Graph retrieval pays only on multi-hop questions | **changed** | Direction confirmed: "GraphRAG methods (e.g., HippoRAG2 and Community-GraphRAG (Local)) excel on multi-hop queries" (HotpotQA, MultiHop-RAG), plain RAG leads single-hop NQ [8]. "Only" is too strong: the same paper says each paradigm has distinct strengths by task, and [9] finds a community-based method leads on coverage-heavy synthesis tasks while a PageRank method leads on fact and chain questions. One of the three multi-hop benchmarks in [9] (BioASQ, terse prompt) shows a tie with plain RAG. | [8], [9] |
| V12 | HippoRAG 2 is about 10 times more efficient than GraphRAG | **unverifiable** | Not in the abstract; PDF text unreadable by the fetch tool. An independent figure: HippoRAG 2 needed 14.47 million construction tokens against 86.80 million for LightRAG (a different system) in [13]. | [7], [13] |
| V13 | EcphoryRAG: about 94% index-time token reduction | **changed** | "up to 94%" against other structured RAG systems. | [4] |

---

## Sources

All reads on 20261030. The time is the read window (UTC). Search-engine summaries are listed as such and
are not treated as sources of numbers.

| # | Source | Read |
|---|---|---|
| 1 | Microsoft Research blog, LazyGraphRAG: Setting a new standard for quality and cost. https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ | 18:59 to 19:00 |
| 2 | arXiv 2506.05690, When to use Graphs in RAG (abstract page). https://arxiv.org/abs/2506.05690 | 18:59 to 19:00 |
| 3 | arXiv 2508.06105, You Don't Need Pre-built Graphs for RAG (abstract page). https://arxiv.org/abs/2508.06105 | 18:59 to 19:00 |
| 4 | arXiv 2510.08958, EcphoryRAG (abstract page). https://arxiv.org/abs/2510.08958 | 18:59 to 19:00 |
| 5 | arXiv 2510.07718, SubQRAG (abstract page). https://arxiv.org/abs/2510.07718 | 18:59 to 19:00 |
| 6 | arXiv 2507.21892, Graph-R1 (abstract page). https://arxiv.org/abs/2507.21892 | 18:59 to 19:00 |
| 7 | arXiv 2502.14802, HippoRAG 2 (abstract page; PDF text unreadable). https://arxiv.org/abs/2502.14802 | 18:59 to 19:00 |
| 8 | arXiv 2502.11371, RAG vs. GraphRAG (abstract page; HTML Table 1, first 100,000 of 123,823 characters). https://arxiv.org/abs/2502.11371 | 18:59 to 19:00 |
| 9 | arXiv 2607.11683, RAGU (full text via the alphaXiv reader). https://arxiv.org/abs/2607.11683 | 18:59 to 19:00 |
| 10 | arXiv 2609.18099, When Is Graph Structure Worth Its Cost? (full text via the alphaXiv reader). https://arxiv.org/abs/2609.18099 | 18:59 to 19:00 |
| 11 | arXiv 2610.30755, Is Complex Agentic Memory Always Needed? (alphaXiv reader). https://arxiv.org/abs/2610.30755 | 18:59 to 19:00 |
| 12 | arXiv 2610.18410, Graph-free Retrieval with Graph-Modified Embeddings (alphaXiv reader). https://arxiv.org/abs/2610.18410 | 18:59 to 19:00 |
| 13 | arXiv 2609.19622, Geometric Gain Graph (alphaXiv reader, v2). https://arxiv.org/abs/2609.19622 | 18:59 to 19:00 |
| 14 | arXiv 2608.28766, Beyond Vector Search (alphaXiv reader). https://arxiv.org/abs/2608.28766 | 18:59 to 19:00 |
| 15 | GitHub REST API, repository metadata for the seven repositories in section 4 (stars, licence, archived flag, last push). https://api.github.com/repos/HKUDS/LightRAG and the six siblings named in section 4 | 18:59 |
| 16 | microsoft/graphrag README (cost warning; no mention of LazyGraphRAG) and latest release v3.3.0. https://github.com/microsoft/graphrag | 18:59 |
| 17 | Web search result summaries for the $47,000 figure and the 91%/34% figures (pages named in the text were not opened). | 18:59 to 19:00 |
| 18 | alphaXiv paper discovery, two queries, papers first published from 20260701, ranked by recency. https://www.alphaxiv.org | 18:59 |
