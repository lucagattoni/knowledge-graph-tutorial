---
type: papers
group: graph-based-rag
order: 2
updated: 20261102 23:26 UTC
---

# Papers: Graph-based RAG

This page holds the papers behind [graph-based RAG](../trends/graph-based-rag.md): methods that let a language model build a graph from a document collection and use it as the retrieval index, and the studies that tested whether that pays. The earliest items here are two a day apart: G-Retriever (first version 20240212, graphs that already exist) and a Microsoft Research blog post (20240213, graphs built from text), which the GraphRAG paper of 20240424 followed [2][22][1]. The "lazy" branch starts with another blog post, LazyGraphRAG of 20241125, which has no paper and so has no section here [23]. Ten papers are told in order of first version, and results reported by a method's own authors are marked first-party. The working threshold for "widely built on" is 500 citations in Semantic Scholar (a threshold chosen for this edition, not a standard) [14]; below it, a paper needs later papers, read in full, that build on it, run it as a baseline or cite it as the basis of a claim. Three papers of the first edition of this page are in the further reading now, because none of the four tests could be shown for them with a source: KAG, RAGSearch and BM25 Wins at Scale.

*Reading:* the independent tests read here are mixed, not uniformly unfavourable to graphs. RAG vs GraphRAG found "complementary strengths rather than a clear dominance" [27]; GraphRAG-Bench found basic RAG "comparable to or outperforms" GraphRAG on simple fact retrieval, with the graph advantage growing as questions need several passages [16]; [RAGSearch](../benchmarks/ragsearch.md) found GraphRAG "remains advantageous for complex multi-hop reasoning" even under agentic search [12]. The one scaling study found graph methods below BM25 wherever they could be built [13][26].

## G-Retriever (2024)

"G-Retriever: Retrieval-Augmented Generation for Textual Graph Understanding and Question Answering", Xiaoxin He, Yijun Tian, Yifei Sun and 5 others (8 in total). Venue: the arXiv record names none; Semantic Scholar's venue field says NeurIPS (carried over, not checked against the paper) [2][14]. First version 20240212. https://arxiv.org/abs/2402.07630

**Why fundamental:** Origin, narrowed by a search of earlier work, and used by later papers. Its abstract (first-party) claims "the first retrieval-augmented generation (RAG) approach for general textual graphs" [2]. An arXiv search made for this page (titles and abstracts of records before 20240212; queries in source 28) found earlier retrieval-augmented prompting over knowledge graphs for question answering: KAPING (20230607) and Retrieve-Rewrite-Answer (20230920), whose abstracts describe knowledge graphs only, and, over a graph of passages instead of a knowledge graph, KGP (20230822, held in [Agentic graph retrieval](./learned-graph-traversal.md)) [28]. It found no earlier record that retrieves from scene graphs, commonsense graphs and knowledge graphs with one method, so the claim stands, at most, for general textual graphs; the search does not cover full texts. *Reading:* it differs from the rest of the page in one way: the graph already exists (scene graphs, commonsense and [knowledge graphs](../index/knowledge-graph.md)), where GraphRAG and its successors build the graph from raw text; the evidence is the abstract's list of graph types [2]. Its 417 citations are under the 500 threshold (Semantic Scholar, read 20261102 20:20 UTC) [14]; later papers read use it: LinearRAG compares itself with it on index cost [18], and GNN-RAG lists it as a baseline [31].

**Idea:** The user "chats with" a graph whose nodes and edges carry text. Retrieval over the graph is posed as a Prize-Collecting Steiner Tree problem, so graphs larger than the model's [context window](../index/context-window.md) can be used and hallucination is resisted; the model is tuned by soft prompting. The authors (first-party) also release a GraphQA benchmark and report gains over baselines on several textual-graph tasks [2]. It extends the retrieve-then-generate pattern of [Lewis et al. (2020)](./foundations.md): it cites that paper as the proposal of retrieval-augmented generation [32].

**Relations:** Builds on: [Lewis et al. (2020)](./foundations.md).

**Read:** abstract, 20261102 20:41 UTC [2].

## GraphRAG (2024)

"From Local to Global: A Graph RAG Approach to Query-Focused Summarization", Darren Edge, Ha Trinh, Newman Cheng and 7 others (10 in total). Venue: none stated on the arXiv record [1]. First version 20240424 (latest v2, 20250219). https://arxiv.org/abs/2404.16130 Project: [Microsoft GraphRAG](../projects/microsoft-graphrag.md).

**Why fundamental:** Widely built on. The paper gives the approach its name: a model builds an entity graph at index time and the graph, with pregenerated community summaries, answers questions [1]; the team's blog post of 20240213 had presented it to practitioners [22]. No priority is claimed. It has 2,489 citations (Semantic Scholar, read 20261102 20:20 UTC), above the threshold [14], and five later papers read run it as a baseline or backend: LightRAG, RAG vs GraphRAG and GraphRAG-Bench on this page, and RAGSearch and BM25 Wins at Scale in the further reading [17][15][16][20][21].

**Idea:** Plain [RAG](../index/retrieval-augmented-generation.md) "fails on global questions directed at an entire text corpus" such as "What are the main themes in the dataset?", because that is [query-focused summarization](../index/query-focused-summarization.md), not lookup [1]. A model extracts an entity knowledge graph, then pregenerates a summary for every community of closely related entities ([community detection](../index/community-detection.md)). At query time each summary yields a partial answer and the partial answers are summarised into one. On corpora of about one million tokens the authors (first-party) report better comprehensiveness and diversity than a conventional RAG baseline [1]. It answers [Lewis et al. (2020)](./foundations.md): the abstract names global sensemaking questions as the case plain RAG fails on [1].

**Relations:** Answers: [Lewis et al. (2020)](./foundations.md).

**Read:** abstract (arXiv page, 20261102 20:41 UTC) and the blog post (20261102 20:47 UTC); full text not read [1][22].

## HippoRAG (2024)

"HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models", Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu and 2 others (5 in total). Venue: NeurIPS 2024 (arXiv comment) [3]. First version 20240523. https://arxiv.org/abs/2405.14831 Project: [HippoRAG](../projects/hipporag.md).

**Why fundamental:** Widely built on, and an origin narrowed by a search. Its 437 citations are under the 500 threshold (Semantic Scholar, read 20261102 20:20 UTC) [14], but three later papers read build on it or test it: HippoRAG 2 extends it [8], GraphRAG-Bench evaluates it [16], and LinearRAG ranks passages with the same Personalized PageRank algorithm [10][18]. The abstract introduces a model-built knowledge graph walked with the [Personalized PageRank](../index/personalized-pagerank.md) algorithm, which "synergistically orchestrates LLMs, knowledge graphs, and the Personalized PageRank algorithm" [3]. An arXiv search made for this page (titles and abstracts of records before 20240523; source 29) found no earlier record that combines Personalized PageRank with a large language model for retrieval (the query on "personalized pagerank" with "large language models" returns none), so no earlier work contradicts the combination as new; the search does not cover full texts, and the neurobiological framing is the authors' own. *Reading:* beside GraphRAG it is the second method here that later papers build on, and it retrieves by spreading activation over a graph, not by summaries.

**Idea:** Inspired by the hippocampal indexing theory of human long-term memory. A model extracts a graph from the corpus; at query time activation spreads from the entities of the question to the passages that matter. On multi-hop question answering the authors (first-party) report gains of up to 20% over the then state of the art, and single-step retrieval that matches or beats iterative retrieval such as IRCoT while being 10 to 30 times cheaper and 6 to 13 times faster [3]. It answers [IRCoT (2022)](./agentic-search.md): the abstract compares single-step retrieval with it on cost and speed, and adds that combining the two gains further [3].

**Relations:** Answers: [IRCoT (2022)](./agentic-search.md).

**Read:** abstract, 20261102 20:41 UTC; full text not read [3].

## Peng GraphRAG survey (2024)

"Graph Retrieval-Augmented Generation: A Survey", Boci Peng, Yun Zhu, Yongchao Liu and 5 others (8 in total). Venue: none stated; the arXiv comment reads "Ongoing work" [4]. First version 20240815 (latest v2, 20240910). https://arxiv.org/abs/2408.08921

**Why fundamental:** Survey of record, and widely built on. The abstract calls it "the first comprehensive overview of GraphRAG methodologies" and formalises the workflow as graph-based indexing, graph-guided retrieval and graph-enhanced generation [4]. It is the earliest of three GraphRAG surveys read and has the most citations of them: 695 (Semantic Scholar, read 20261102 20:20 UTC), above the threshold [14]. The other two are in the further reading.

**Idea:** After the three-stage workflow, the survey outlines the core technologies and training methods of each stage, then covers downstream tasks, application domains, evaluation methods and industrial use cases, and keeps a public repository of papers [4]. The abstract names no individual paper and the reference list was not read, so its relations to other papers are **unstated**.

**Relations:** None.

**Read:** abstract, 20261102 20:41 UTC; full text not read [4].

## LightRAG (2024)

"LightRAG: Simple and Fast Retrieval-Augmented Generation", Zirui Guo, Lianghao Xia, Yanhua Yu and 2 others (5 in total). Venue: the arXiv record names none; Semantic Scholar's venue field says EMNLP (carried over, not checked) [6][14]. First version 20241008. https://arxiv.org/abs/2410.05779 Project: [LightRAG](../projects/lightrag.md).

**Why fundamental:** Widely built on. It proposes a dual-level retrieval (low-level entity and high-level theme knowledge) and an incremental update that merges new documents into the graph without rebuilding it [6]. It has 577 citations (Semantic Scholar, read 20261102 20:20 UTC), above the threshold [14]. Later studies test it: GraphRAG-Bench includes it, and the scaling study BM25 Wins at Scale (further reading) could build it only up to 2,254 documents and found it did not complete at 2,826 [16][21]; LinearRAG's authors (first-party) report 4,933.22 s of indexing on [2WikiMultiHopQA](../datasets/2wikimultihopqa.md) [18]. RAG-Anything builds on it [19].

**Idea:** A model extracts entities and relations from chunks, profiles each into a key-value pair and merges duplicates. Retrieval is dual-level: low-level keywords match entities, high-level keywords match relations and themes, over [vector search](../index/vector-search.md) of the keys, with one-hop neighbours added [6]. On the [UltraDomain](../datasets/ultradomain.md) Legal set the authors (first-party) put GraphRAG's retrieval at 610 community reports of about 1,000 tokens each, against under 100 tokens and one call for LightRAG [17]. It answers [GraphRAG (2024)](./graph-based-rag.md): it compares itself with it as the top baseline and reports lower retrieval cost and cheaper updates [17]. It is evaluated on [UltraDomain](../datasets/ultradomain.md) (Agriculture, CS, Legal and Mix) [17].

**Relations:** Answers: [GraphRAG (2024)](./graph-based-rag.md).

**Read:** abstract and full text, 20261102 20:42 UTC [6][17].

## RAG vs GraphRAG (2025)

"RAG vs. GraphRAG: A Systematic Evaluation and Key Insights", Haoyu Han, Li Ma, Yu Wang and 9 others (12 in total). Venue: the arXiv record names none (Semantic Scholar's venue field says ACM SIGKDD, carried over, not checked); the text of v3 still carries a template conference placeholder [7][14][15]. First version 20250217 (latest v3, 20260304). https://arxiv.org/abs/2502.11371

**Why fundamental:** Turning point. It is a comparison made outside the teams that built the methods, and the earliest on this page to report that neither side wins everywhere: "RAG excels on detailed single-hop queries", GraphRAG methods such as HippoRAG 2 and Community-GraphRAG (Local) "excel on multi-hop queries", and Community-GraphRAG (Global) "often struggles on QA" [15]. Later papers read take it up: GraphRAG-Bench cites it for the 13.4% lower accuracy of GraphRAG on [Natural Questions](../datasets/natural-questions.md) and widens the tasks [16], and Geometric Gain Graph (further reading) cites it [31]. Its authors also wrote a GraphRAG survey (Han et al., in the further reading), so they are not neutral on the topic. 118 citations (read 20261102 20:20 UTC) [14].

**Idea:** GraphRAG systems for text were tailored to particular tasks and datasets, with different evaluation protocols. The paper fixes preprocessing, retrieval and generation settings and compares RAG with four kinds of GraphRAG on question answering and query-based summarisation, with two Llama 3.1 generators. It adds that a judge model's verdict on summaries changes with the order of presentation, and then explores choosing between, or combining, the two paradigms [7][15]. It evaluates GraphRAG (its community variants) and [RAPTOR (2024)](./reasoning-over-structure.md), and, in version 3 (20260304), [HippoRAG 2 (2025)](./graph-based-rag.md): version 3 lists HippoRAG2 among the methods compared, while version 1 (20250217) predates HippoRAG 2 (20250220) and so cannot have tested it [15][27][8]. It is scored on [Natural Questions](../benchmarks/natural-questions.md), [HotpotQA](../benchmarks/hotpotqa.md) and [MultiHop-RAG](../benchmarks/multihop-rag.md), plus NovelQA [15].

**Relations:** Evaluates: [GraphRAG (2024)](./graph-based-rag.md), [HippoRAG 2 (2025)](./graph-based-rag.md), [RAPTOR (2024)](./reasoning-over-structure.md).

**Read:** abstract and full text, 20261102 20:42 UTC; the method list and findings re-read in the HTML of version 3, 20261102 20:59 UTC [7][15][27].

## HippoRAG 2 (2025)

"From RAG to Memory: Non-Parametric Continual Learning for Large Language Models", Bernal Jiménez Gutiérrez, Yiheng Shu, Weijian Qi and 2 others (5 in total). Venue: ICML 2025 (arXiv comment) [8]. First version 20250220 (latest v2, 20250619). https://arxiv.org/abs/2502.14802

**Why fundamental:** Turning point. Its abstract states the weakness that earlier graph methods showed: their performance on basic factual memory tasks "drops considerably below standard RAG", and it sets out to beat standard RAG on factual, sense-making and associative tasks together [8]. Independent tests then used it as the strongest graph backend: GraphRAG-Bench found it led in context relevance on complex questions of the novel corpus, and under RAGSearch's GraphSearch agent (further reading) it scored highest of the five graph backends on four of six question sets [16][20]; EffiRAG (further reading) evaluates it separately on multi-hop questions [31]. 284 citations (read 20261102 20:20 UTC) [14].

**Idea:** It keeps the Personalized PageRank retrieval of HippoRAG and adds deeper integration of passages and more effective online use of the model. The authors (first-party) report a 7% gain on associative-memory tasks over the best embedding model, with better factual and sense-making memory too [8]. *Reading:* the same page records the cost: a fitted full-scale build of about 2.9 billion generative tokens, and a score of 41.0 against BM25's 55.2 (14.2 points lower) at 155 million corpus tokens, in the 2026 scaling study [21][26]. It builds on [HippoRAG (2024)](./graph-based-rag.md): it "builds upon the Personalized PageRank algorithm used in HippoRAG" [8].

**Relations:** Builds on: [HippoRAG (2024)](./graph-based-rag.md).

**Read:** abstract; results from the full text of the three evaluation papers cited, 20261102 20:42 UTC; the 41.0 and 55.2 figures re-read in the HTML of version 3, 20261102 20:59 UTC [8][16][20][21][26].

## GraphRAG-Bench Xiang (2025)

"When to use Graphs in RAG: A Comprehensive Analysis for Graph Retrieval-Augmented Generation", Zhishang Xiang, Chuanjie Wu, Qinggang Zhang and 4 others (7 in total). Venue: the arXiv comment names none; the v3 text is headed "Published as a conference paper at ICLR 2026" [9][16]. First version 20250606 (latest v3, 20260222). https://arxiv.org/abs/2506.05690

**Why fundamental:** Turning point. It states the question that later studies take up: "recent studies report that GraphRAG frequently underperforms vanilla RAG on many real-world tasks", and builds a graded benchmark to find where graphs help [9]. A later paper read cites it for that question: EffiRAG (further reading, 20260916) writes that it "studies whether the quality gains of graph-based RAG justify its construction cost" [31]. Another benchmark has the same name (Xiao et al., 2506.02404); see the further reading. The benchmark is described at [GraphRAG-Bench (Xiang)](../benchmarks/graphrag-bench-xiang.md). 60 citations (read 20261102 20:20 UTC) [14].

**Idea:** Four levels of task (fact retrieval, complex reasoning, contextual summarisation, creative generation) over two corpora, NCCN medical guidelines and pre-20th-century novels, with metrics for graph construction, retrieval and generation. Seven GraphRAG frameworks are tested. Basic RAG "comparable to or outperforms" GraphRAG on simple fact retrieval; GraphRAG's advantage grows as questions need several passages; and graph retrieval risks large context growth [16]. It evaluates GraphRAG, HippoRAG, HippoRAG 2, LightRAG, [RAPTOR (2024)](./reasoning-over-structure.md) and Fast-GraphRAG (no paper on this page), seven frameworks in all, against basic RAG with and without reranking [16]. It cites [RAG vs GraphRAG (2025)](./graph-based-rag.md) for the 13.4% lower accuracy of GraphRAG on [Natural Questions](../datasets/natural-questions.md) and widens the tasks [16].

**Relations:** Answers: [RAG vs GraphRAG (2025)](./graph-based-rag.md). Evaluates: [GraphRAG (2024)](./graph-based-rag.md), [HippoRAG (2024)](./graph-based-rag.md), [LightRAG (2024)](./graph-based-rag.md), [HippoRAG 2 (2025)](./graph-based-rag.md), [RAPTOR (2024)](./reasoning-over-structure.md); also: Fast-GraphRAG.

**Read:** abstract and full text, 20261102 20:42 UTC [9][16].

## LinearRAG (2025)

"LinearRAG: Linear Graph Retrieval Augmented Generation on Large-scale Corpora", Luyao Zhuang, Shengyuan Chen, Yilin Xiao and 5 others (8 in total). Venue: none stated [10]. First version 20251011 (latest v4, 20251109). https://arxiv.org/abs/2510.10114

**Why fundamental:** Turning point (cost), as a *Reading:*. The abstract (first-party) says it builds a "relation-free hierarchical graph, termed Tri-Graph, using only lightweight entity extraction and semantic linking", which "scales linearly with corpus size and incurs no extra token consumption" [10]. Three later papers read take it up: RAGSearch runs it as one of its five graph backends [20]; the scaling study BM25 Wins at Scale builds it as one of four graph pipelines and finds that only LinearRAG has no generative construction tokens, though it still does local entity recognition and embedding work, and that at 1,144 documents it ends within 1.8 points of MS-GraphRAG and LightRAG [21][26] (both in the further reading); Geometric Gain Graph cites it, with HippoRAG 2, as a design that adds document nodes [31]. Its score at scale is low: 29.8 at 131,876 documents, against 41.0 for HippoRAG 2 and 55.2 for BM25 [26]. It is not the first cost-cutting graph method on this page: MiniRAG (first version 20250112) and KET-RAG (20250213) are earlier (further reading) [25]. 70 citations (read 20261102 20:20 UTC), under the 500 threshold [14].

**Idea:** Relation extraction is unstable and costly and leaves noisy graphs. The Tri-Graph has passage, sentence and entity nodes made with named-entity recognition alone. Retrieval has two stages: activate entities by semantic bridging, then rank passages with Personalized PageRank over the activated entities [10][18]. First-party figures: indexing 249.78 s against 4,933.22 s for LightRAG on 2WikiMultiHopQA, and 12.8 and 15.1 times faster than RAPTOR on 5 and 10 million tokens [18]. It compares itself with [LightRAG (2024)](./graph-based-rag.md), [G-Retriever (2024)](./graph-based-rag.md) and [RAPTOR (2024)](./reasoning-over-structure.md) on index cost in its own efficiency table, and with [HippoRAG 2 (2025)](./graph-based-rag.md) as a baseline [18]. Its ranking step is Personalized PageRank, as in [HippoRAG (2024)](./graph-based-rag.md) (the same algorithm; no source read says it builds on that paper).

**Relations:** Answers: [G-Retriever (2024)](./graph-based-rag.md), [LightRAG (2024)](./graph-based-rag.md), [RAPTOR (2024)](./reasoning-over-structure.md). Evaluates: [HippoRAG 2 (2025)](./graph-based-rag.md).

**Read:** abstract and full text, 20261102 20:42 UTC [10][18].

## RAG-Anything (2025)

"RAG-Anything: All-in-One RAG Framework", Zirui Guo, Xubin Ren, Lingrui Xu and 2 others (5 in total). Venue: none stated [11]. First version 20251014. https://arxiv.org/abs/2510.12323 Project: [RAG-Anything](../projects/rag-anything.md).

**Why fundamental:** Turning point (absorption), which concerns the project more than the paper. The LightRAG README lists "[2026.05] Merge RagAnything into LightRAG" and says that from v1.5 multimodal processing is part of LightRAG's pipeline; the same README records the RAG-Anything project as released in 2025.06, four months before the paper's first version (20251014) [24]. The abstract states the gap the authors address, that existing frameworks "are limited to textual content", and proposes a graph in which images, tables and equations are entities; this is a statement of a gap, not a claim of priority, and no priority is claimed here [11]. Citation count: **unstated** (the paper is not in the citation pool read on 20261102 and the APIs were not queried again), so "widely built on" is not asserted.

**Idea:** A dual-graph construction captures cross-modal relationships and text semantics together; cross-modal hybrid retrieval then combines structural navigation with semantic matching. The text graph follows LightRAG's method (full text). On DocBench and MMLongBench, with GPT-4o-mini and documents parsed by MinerU, the authors (first-party) report gains over baselines, largest on long documents [11][19]. The text knowledge graph is built "following established methodologies similar to LightRAG", and LightRAG is also its baseline [19].

**Relations:** Builds on: [LightRAG (2024)](./graph-based-rag.md).

**Read:** abstract and full text, 20261102 20:42 UTC; README, 20261102 20:58 UTC [11][19][24].

## Further reading

Counts in this list are Semantic Scholar counts carried over from the research pool (read 20261102 20:20 UTC) [14]; a count is never compared across sources. Titles, authors, first-version dates and the comments of every row were re-read from the arXiv API on 20261102 at 20:58 and 21:02 UTC [25]; years are those of the first version. The last three rows are papers moved here from the fundamental list; their records are sources [5], [12] and [13].

| Paper | Year | Link | One clause |
|---|---|---|---|
| Is GraphRAG Needed? | 2026 | https://arxiv.org/abs/2606.25656 | nine standard scenarios on semi-structured knowledge bases; expanded retrieval does not raise generation quality in proportion (ACL 2026 GEM Workshop) |
| KET-RAG | 2025 | https://arxiv.org/abs/2502.09304 | a model builds a graph skeleton on key chunks only, plus a keyword graph from all chunks, to cut index cost (first version 20250213; 60 citations) |
| MiniRAG | 2025 | https://arxiv.org/abs/2501.06713 | graph RAG made simple enough for small models (first version 20250112) |
| When Is Graph Structure Worth Its Cost? (the EffiRAG system) | 2026 | https://arxiv.org/abs/2609.18099 | a graph that locates passages and answers from the original text; reports 57% lower cost than LightRAG-hybrid (first-party, 20260916) |
| Geometric Gain Graph | 2026 | https://arxiv.org/abs/2609.19622 | zero-token graph construction from the embedding space (20260917) |
| PathRAG | 2025 | https://arxiv.org/abs/2502.14902 | prunes retrieved paths by flow; an improvement on LightRAG-style indexes (104 citations) |
| HyperGraphRAG | 2025 | https://arxiv.org/abs/2503.21322 | hypergraph of n-ary facts (NeurIPS 2025; 97 citations); a backend in RAGSearch |
| Han et al., GraphRAG survey | 2024 | https://arxiv.org/abs/2501.00309 | second GraphRAG survey, 18 authors, first version 20241231 (307 citations) |
| Zhang et al., GraphRAG survey | 2025 | https://arxiv.org/abs/2501.13958 | third survey, centred on customised language models (169 citations) |
| GraphRAG-Bench Xiao | 2025 | https://arxiv.org/abs/2506.02404 | a different benchmark with the same name: domain-specific reasoning questions (36 citations); not the paper above |
| In-depth Analysis of Graph-based RAG in a Unified Framework | 2025 | https://arxiv.org/abs/2503.04338 | compares graph-based methods with each other, not graph against plain RAG (76 citations) |
| GNN-RAG | 2024 | https://arxiv.org/abs/2405.20139 | graph neural network retrieval for knowledge-graph question answering (190 citations) |
| StructRAG | 2024 | https://arxiv.org/abs/2410.08815 | chooses the data structure per task (104 citations) |
| HybridRAG | 2024 | https://arxiv.org/abs/2408.04948 | vector retrieval and graph retrieval together (251 citations) |
| GFM-RAG | 2025 | https://arxiv.org/abs/2502.01113 | graph foundation model as the retriever (NeurIPS 2025 per the arXiv comment; 64 citations) |
| KAG | 2024 | https://arxiv.org/abs/2409.13731 | "Knowledge Augmented Generation": a logical-form-guided reasoning engine over a schema-based graph, deployed in two Ant Group services (first-party; 152 citations). Moved from the fundamental list: the name is not new (the abstract of PokeLLMon, 20240202, already lists "knowledge-augmented generation" as a design strategy) [30], and none of the evaluation studies on this page runs it; the only later paper read that mentions it is KITE (20261030), which describes it in one sentence [33] |
| RAGSearch | 2026 | https://arxiv.org/abs/2604.09666 | "Do We Still Need GraphRAG?": five graph backends under four agents on six question sets; agentic search narrows the gap but GraphRAG "remains advantageous for complex multi-hop reasoning"; single-shot the best of the five gains +27.23 on multi-hop QA over dense RAG, and under GraphSearch the averaged gap falls only to +26.59 [12][20]. 1 citation (read 20261102 20:20 UTC). Moved from the fundamental list: none of the later papers read cites it [31]. Benchmark page: [RAGSearch](../benchmarks/ragsearch.md) |
| BM25 Wins at Scale | 2026 | https://arxiv.org/abs/2607.26497 | 28 nested corpus-size tiers (1,144 to 511,959 documents): "around 10 million corpus tokens, BM25 overtakes" the file-system agent, and graph-based RAG "encounters construction walls before deployment scale"; fitted full-scale build costs are about 2.9 billion tokens for HippoRAG 2, 7.9 billion for MS-GraphRAG and about 102 billion, extrapolated, for LightRAG [13][21]. 2 citations (read 20261102 20:20 UTC). Moved from the fundamental list: the only later paper read that cites it is ReFind (further reading of [Agentic search over raw data](./agentic-search.md)), which shares two authors with it and calls its own finding on rank fusion "consistent with the observation" of this study [33]; and it cites none of RAGSearch, GraphRAG-Bench or RAG vs GraphRAG [31] |

## Sources

1. https://arxiv.org/abs/2404.16130 : GraphRAG title, authors, versions, abstract (read 20261102 20:41 UTC)
2. https://arxiv.org/abs/2402.07630 : G-Retriever title, authors, versions, abstract (read 20261102 20:41 UTC)
3. https://arxiv.org/abs/2405.14831 : HippoRAG title, authors, versions, comment (NeurIPS 2024), abstract (read 20261102 20:41 UTC)
4. https://arxiv.org/abs/2408.08921 : Peng survey title, authors, versions, comment, abstract (read 20261102 20:41 UTC)
5. https://arxiv.org/abs/2409.13731 : KAG title, authors, versions, comment, abstract (read 20261102 20:41 UTC)
6. https://arxiv.org/abs/2410.05779 : LightRAG title, authors, versions, abstract (read 20261102 20:41 UTC)
7. https://arxiv.org/abs/2502.11371 : RAG vs GraphRAG title, authors, versions, abstract (read 20261102 20:41 UTC)
8. https://arxiv.org/abs/2502.14802 : HippoRAG 2 title, authors, versions, comment (ICML 2025), abstract (read 20261102 20:41 UTC)
9. https://arxiv.org/abs/2506.05690 : GraphRAG-Bench Xiang title, authors, versions, abstract (read 20261102 20:41 UTC)
10. https://arxiv.org/abs/2510.10114 : LinearRAG title, authors, versions, abstract (read 20261102 20:41 UTC)
11. https://arxiv.org/abs/2510.12323 : RAG-Anything title, authors, version, abstract (read 20261102 20:41 UTC)
12. https://arxiv.org/abs/2604.09666 : RAGSearch title, authors, version, abstract (read 20261102 20:42 UTC)
13. https://arxiv.org/abs/2607.26497 : BM25 Wins at Scale title, authors, versions, abstract (read 20261102 20:42 UTC)
14. https://api.semanticscholar.org/graph/v1/paper/batch : citation counts and venue fields of the papers above, as read by the papers research of 20261102 and carried over, not queried again (read 20261102 20:20 UTC)
15. https://arxiv.org/pdf/2502.11371 : full text of v3: methods compared, datasets, the three findings quoted (read 20261102 20:42 UTC)
16. https://arxiv.org/pdf/2506.05690 : full text of v3: ICLR 2026 header, four levels, two corpora, seven frameworks, observations 1 to 5, Han et al. figure (read 20261102 20:42 UTC)
17. https://arxiv.org/pdf/2410.05779 : full text: UltraDomain sets, comparison with GraphRAG, 610 x 1,000 tokens against under 100 (read 20261102 20:42 UTC)
18. https://arxiv.org/pdf/2510.10114 : full text: Tri-Graph, indexing table with 249.78 s and 4,933.22 s, large-scale table with 12.8 and 15.1 times (read 20261102 20:42 UTC)
19. https://arxiv.org/pdf/2510.12323 : full text: dual-graph construction, LightRAG-like text graph, DocBench and MMLongBench, baselines (read 20261102 20:42 UTC)
20. https://arxiv.org/pdf/2604.09666 : full text: backends, agents, six datasets, +0.47, +27.23, cost table (read 20261102 20:42 UTC)
21. https://arxiv.org/pdf/2607.26497 : full text: 28 tiers, build-cost fits, 155M-token score, LinearRAG within 1.8 points, citation of Robertson and Zaragoza (read 20261102 20:42 UTC)
22. https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/ : post dated February 13, 2024 introducing GraphRAG (read 20261102 20:47 UTC; date re-read 20261102 21:03 UTC)
23. https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ : post of 20241125, "the lazy approach defers all LLM use until query time" (read 20261102 20:47 UTC)
24. https://raw.githubusercontent.com/HKUDS/LightRAG/main/README.md : news line "[2026.05] Merge RagAnything into LightRAG" and the v1.5 multimodal section, and "[2025.06] ... released RAG-Anything" (read 20261102 20:58 UTC)
25. https://export.arxiv.org/api/query?id_list=2606.25656,2609.18099,2609.19622,2502.14902,2503.21322,2501.13958,2506.02404,2503.04338,2405.20139,2410.08815,2408.04948,2502.01113,2501.00309,2502.09304,2501.06713,2402.07630,2510.10114 : titles, authors, first-version dates and comments of the further-reading papers, and the first-version dates of G-Retriever, LinearRAG, MiniRAG and KET-RAG (read 20261102 20:58 UTC, and 20261102 21:02 UTC for the first eight ids)
26. https://arxiv.org/html/2607.26497v3 : version 3 of BM25 Wins at Scale: combined-score table (HippoRAG 2 41.0, LinearRAG 29.8, BM25 55.2 at 131,876 documents), build-cost text, LinearRAG without generative build calls and within 1.8 points at the bedrock (read 20261102 20:59 UTC)
27. https://arxiv.org/html/2502.11371v3 : version 3 of RAG vs GraphRAG: HippoRAG2 among the methods compared, "complementary strengths rather than a clear dominance" (read 20261102 20:59 UTC)
28. https://export.arxiv.org/api/query : three arXiv searches for earlier work before the first version of G-Retriever (submission date up to 20240211; fields searched: title, abstract, comment): `retrieval-augmented` with `graph`, `language model` and `question answering` (7 records); `knowledge graph` with `large language model`, `retrieval`, `prompting` and `question answering` (9 records, among them KAPING 2306.04136 of 20230607, KGP 2308.11730 of 20230822, Retrieve-Rewrite-Answer 2309.11206 of 20230920, KnowledgeNavigator 2312.15880 of 20231226); `textual graph` or `text-attributed graph` (24 records, graph representation learning). Abstracts of KAPING and Retrieve-Rewrite-Answer: retrieval of knowledge-graph facts to prompt a model for knowledge graph question answering (searches read 20261102 22:56 to 22:57 UTC; abstracts 23:02 UTC). A search of titles and abstracts, not of full texts, and not exhaustive
29. https://export.arxiv.org/api/query : arXiv searches for earlier work before the first version of HippoRAG (submission date up to 20240522): `personalized pagerank` with `large language models` (0 records), `personalized pagerank` with `language model` or LLM and `retrieval` (1 record, 2208.07262, keyword extraction), `hippocampal` with `language model`, LLM or `retrieval` and `hippocampal indexing` (neuroscience records only), `knowledge graph` with `retrieval`, `large language models`, `multi-hop` and `question answering` (3 records of 2024, none with Personalized PageRank) (read 20261102 22:56 to 23:00 UTC). Titles and abstracts only, not exhaustive
30. https://export.arxiv.org/api/query and https://export.arxiv.org/api/query?id_list=2402.01118 : search `knowledge augmented generation` before 20240910: three records, among them PokeLLMon (2402.01118, 20240202), whose abstract lists "Knowledge-augmented generation that retrieves external knowledge to counteract hallucination" as a design strategy (read 20261102 22:56 UTC; abstract 23:07 UTC)
31. https://arxiv.org/html/2609.18099, https://arxiv.org/html/2609.19622, https://arxiv.org/html/2606.25656, https://arxiv.org/html/2607.26497, https://arxiv.org/html/2604.09666, https://arxiv.org/html/2405.20139 : renderings searched for the names of earlier papers (read 20261102 22:58 to 23:00 UTC). EffiRAG (2609.18099): "GraphRAG-Bench studies whether the quality gains of graph-based RAG justify its construction cost", reference to Xiang et al. 2506.05690, and HippoRAG2 evaluated separately on multi-hop questions; Geometric Gain Graph (2609.19622): LinearRAG and HippoRAG2 named as designs that add document nodes, and a reference to Han et al., RAG vs GraphRAG (2502.11371); Is GraphRAG Needed? (2606.25656): none of RAGSearch, BM25 Wins, GraphRAG-Bench or RAG vs GraphRAG; BM25 Wins at Scale (2607.26497): none of RAGSearch, GraphRAG-Bench or RAG vs GraphRAG; RAGSearch (2604.09666): no GraphRAG-Bench, and a Han et al. (2024) reference whose author list matches the GraphRAG survey, not RAG vs GraphRAG; GNN-RAG (2405.20139): G-Retriever (He et al., 2024) in its results table as a baseline. A name search of the text: a paper may cite a work without the name appearing in the rendering
32. https://arxiv.org/pdf/2402.07630 : G-Retriever text and reference list: "initially proposed by Lewis et al." with the 2020 RAG paper as reference 21 (read 20261102 21:47 UTC, searched for this passage, not read end to end; carried over from the checks made for the landing page of this chapter)
33. https://arxiv.org/html/2610.41521, https://arxiv.org/html/2608.12888 and the other renderings listed in source 27 of the page [Agentic search over raw data](./agentic-search.md) (read 20261102 23:16 to 23:17 UTC): KITE (2610.41521, v1 20261030) describes KAG ("combines logical-form planning with hybrid retrieval over knowledge graphs and text") in one sentence; ReFind (2608.12888, v1 20260813; authors include Licheng Zhang and Benfeng Xu, who are also authors of BM25 Wins at Scale) cites BM25 Wins at Scale in its discussion of rank fusion ("This is consistent with the observation of Wang et al. (2026)"); no rendering searched mentions RAGSearch, and no other rendering cites BM25 Wins at Scale. A name search of the text; a paper may cite a work without the name appearing in the rendering
