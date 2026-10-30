# Papers, benchmarks and datasets

Part of the field-neutral [KB/KG reference](../README.md). Companion sections:
[`literature/`](../literature/) (when graphs help retrieval) and [`projects/`](../projects/)
(one entry per project).

**State:** first complete pass, written 20261030. Every fact below carries a source number `[n]`;
the numbered list is at the end with URLs and read times. Where the sources are silent the cell
says **unstated**. Nothing here comes from memory: papers dated 2026 are newer than the author's
training data and were read in this run.

Conventions for all tables:

- **Date** is the arXiv v1 submission date (`YYYYMMDD`), from the arXiv record [1].
- **Venue** is what the arXiv record states (journal reference or the authors' comment). "none
  stated" means the record names no venue, not that the paper is unpublished.
- **Link** is the arXiv abstract page `https://arxiv.org/abs/<id>`.
- Authors are given as first three plus the total from the record [1].
- Metadata and one-line scope come from the arXiv record [1] unless another source number is shown.

## 1. Surveys

### 1.1 GraphRAG and graphs with LLMs

| Title | Authors (total), venue | Date | What it covers | Link |
|---|---|---|---|---|
| Graph Retrieval-Augmented Generation: A Survey | Boci Peng, Yun Zhu, Yongchao Liu et al. (8); none stated | 20240815 | GraphRAG methods across indexing, retrieval, generation, evaluation and industrial use [1] | [2408.08921](https://arxiv.org/abs/2408.08921) |
| Retrieval-Augmented Generation with Graphs (GraphRAG) | Haoyu Han, Yu Wang, Harry Shomer et al. (18); none stated. Affiliations include Michigan State, Oregon, Adobe, Amazon, Meta, Snap [2] | 20241231 | A framework of GraphRAG components, domain-specific techniques and open challenges [1] | [2501.00309](https://arxiv.org/abs/2501.00309) |
| A Survey of Graph Retrieval-Augmented Generation for Customized Large Language Models | Qinggang Zhang, Shengyuan Chen, Yuanchen Bei et al. (12); none stated | 20250121 | GraphRAG for domain-specific LLMs, where flat-text retrieval falls short [1] | [2501.13958](https://arxiv.org/abs/2501.13958) |
| Unifying Large Language Models and Knowledge Graphs: A Roadmap | Shirui Pan, Linhao Luo, Yufei Wang et al. (6); IEEE TKDE 2024 | 20230614 | Three ways to combine them: KG-enhanced LLMs, LLM-augmented KGs, synergized models [1] | [2306.08302](https://arxiv.org/abs/2306.08302) |
| LLM-empowered knowledge graph construction: A survey | Haonan Bian (1); none stated. Xidian University [2] | 20251023 | KG construction with LLMs across ontology engineering, extraction and fusion; schema-based and schema-free [1] | [2510.20345](https://arxiv.org/abs/2510.20345) |
| Integrating Graphs, Large Language Models, and Agents: Reasoning and Retrieval | Authors and venue **unstated** (listing only) [2] | 20260417 | Graph representations used for reasoning, retrieval and decisions in LLM agents; abstract not read beyond its first lines [2] | [2604.15951](https://arxiv.org/abs/2604.15951) |

### 1.2 Agent memory

| Title | Authors (total), venue | Date | What it covers | Link |
|---|---|---|---|---|
| A Survey on the Memory Mechanism of Large Language Model based Agents | Zeyu Zhang, Xiaohe Bo, Chen Ma et al. (9); none stated (39 pages) | 20240421 | How memory is designed and evaluated in LLM agents, plus applications [1] | [2404.13501](https://arxiv.org/abs/2404.13501) |
| From Human Memory to AI Memory: A Survey on Memory Mechanisms in the Era of LLMs | Yaxiong Wu, Sheng Liang, Chen Zhang et al. (8); none stated | 20250422 | Maps human memory categories to AI memory; classifies work by object, form, time [1] | [2504.15965](https://arxiv.org/abs/2504.15965) |
| Graph-Augmented Large Language Model Agents: Current Progress and Future Prospects | Yixin Liu, Guibin Zhang, Kun Wang et al. (5); none stated | 20250729 | Graphs in agent planning, memory and tool use, including multi-agent systems [1] | [2507.21407](https://arxiv.org/abs/2507.21407) |
| Memory in the Age of AI Agents | Yuyang Hu, Shichun Liu, Yanwei Yue et al. (47); none stated | 20251215 | Agent memory by forms, functions and dynamics; compiles benchmarks and frameworks [1] | [2512.13564](https://arxiv.org/abs/2512.13564) |
| Graph-based Agent Memory: Taxonomy, Techniques, and Applications | Chang Yang, Chuang Zhou, Yilin Xiao et al. (18); none stated | 20260205 | Taxonomy and lifecycle of graph-based agent memory, with libraries and benchmarks [1] | [2602.05665](https://arxiv.org/abs/2602.05665) |
| Graph-Based Personalized Memory for LLM Agents: Representation, Evolution, Retrieval, and Evaluation | Dac Duy Anh Nguyen, Zhangchi Qiu, Shigeng Chen et al. (4); ICKG 2026 (accepted, per the record) | 20260908 | Graph memory for personalised agents: representation, evolution, retrieval, evaluation [1] | [2609.08599](https://arxiv.org/abs/2609.08599) |
| Learning to Remember: Advances in Memory Mechanisms for Large Language Models | Chenye Han, Hongche Yu, Mengyue Wu et al. (5); none stated | 20261026 | Memory in three families (nonparametric, parametric, agent-evolution) over the whole lifecycle [1] | [2610.35089](https://arxiv.org/abs/2610.35089) |

## 2. Method papers by direction

"Repo" is the implementing repository. **README cites id** = the repository README contains the
paper's arXiv id (a check made with the GitHub API [9]); **no** means the repository exists but its
README does not cite the id, so it is not confirmed as the official one. **unstated** = no
repository was looked for or found in this run. On 20261030 none of the repositories whose
metadata was read was archived; the exceptions, not checked for that flag, are
`ycygit/GraphRAG-R1` and `yansikuan/memory-r1` [9].

### 2.1 Graph-based RAG (build a graph or tree over a corpus, retrieve through it)

| Paper | Date | Venue | Idea (from the abstract) | Repo |
|---|---|---|---|---|
| [RAPTOR](https://arxiv.org/abs/2401.18059) (2401.18059) | 20240131 | none stated | Recursively embeds, clusters and summarises chunks into a tree; retrieves across levels [1] | `parthsarthi03/raptor` (README cites id) [9] |
| [G-Retriever](https://arxiv.org/abs/2402.07630) (2402.07630) | 20240212 | none stated | Prize-Collecting Steiner Tree retrieval over textual graphs, with soft prompting [1] | `XiaoxinHe/G-Retriever` (README cites id) [9] |
| [From Local to Global: GraphRAG](https://arxiv.org/abs/2404.16130) (2404.16130, Edge et al.) | 20240424 | none stated | Entity graph plus community summaries; partial answers merged for global questions [1] | `microsoft/graphrag` (README cites id) [9] |
| [GNN-RAG](https://arxiv.org/abs/2405.20139) (2405.20139) | 20240530 | none stated | A GNN retrieves answer candidates from KG subgraphs; verbalised paths feed the LLM [1] | `cmavro/GNN-RAG` (README: **no**) [9] |
| [HippoRAG](https://arxiv.org/abs/2405.14831) (2405.14831) | 20240523 | NeurIPS 2024 | Hippocampus-inspired: LLM + knowledge graph + Personalized PageRank [1] | `OSU-NLP-Group/HippoRAG` (README cites id) [9] |
| [KAG](https://arxiv.org/abs/2409.13731) (2409.13731) | 20240910 | none stated | Mutual indexing between KG and text, logical-form-guided hybrid reasoning [1] | `OpenSPG/KAG` (README cites id) [9] |
| [LightRAG](https://arxiv.org/abs/2410.05779) (2410.05779) | 20241008 | none stated | Graph-structured index, dual-level retrieval, incremental update algorithm [1] | `HKUDS/LightRAG` (README cites id) [9] |
| [StructRAG](https://arxiv.org/abs/2410.08815) (2410.08815) | 20241011 | none stated | Chooses a structure type per query, rebuilds documents into it at inference time [1] | `icip-cas/StructRAG` (README: **no**) [9] |
| [MiniRAG](https://arxiv.org/abs/2501.06713) (2501.06713) | 20250112 | none stated | Chunk-entity graph with light retrieval, aimed at small language models [1] | `HKUDS/MiniRAG` (README cites id) [9] |
| [GFM-RAG](https://arxiv.org/abs/2502.01113) (2502.01113) | 20250203 | NeurIPS 2025 | A graph foundation model (GNN) reasons over the graph for retrieval [1] | `RManLuo/gfm-rag` (README cites id) [9] |
| [PathRAG](https://arxiv.org/abs/2502.14902) (2502.14902) | 20250218 | none stated | Flow-based pruning keeps relational paths, verbalised into the prompt [1] | `BUPT-GAMMA/PathRAG` (README: **no**) [9] |
| [HippoRAG 2: From RAG to Memory](https://arxiv.org/abs/2502.14802) (2502.14802) | 20250220 | ICML 2025 | Personalized PageRank with deeper passage integration and online LLM use [1] | `OSU-NLP-Group/HippoRAG` (README cites id) [9] |
| [HyperGraphRAG](https://arxiv.org/abs/2503.21322) (2503.21322) | 20250327 | NeurIPS 2025 | Hyperedges capture n-ary facts in a knowledge hypergraph [1] | `LHRLAB/HyperGraphRAG` (README: **no**; the RAGSearch paper builds this method from the Graph-R1 repository instead [4]) [9] |
| [LogicRAG: You Don't Need Pre-built Graphs for RAG](https://arxiv.org/abs/2508.06105) (2508.06105) | 20250808 | AAAI'26 | No offline graph: builds a query-subproblem DAG at inference time and prunes with it [1] | `chensyCN/LogicRAG` (exists; README not checked for the id) [9] |
| [Youtu-GraphRAG](https://arxiv.org/abs/2508.19855) (2508.19855) | 20250827 | none stated | Schema-bounded agentic extraction, community detection, parallel sub-query retrieval with reflection [1] | `TencentCloudADP/youtu-graphrag` (README cites id) [9] |
| [LinearRAG](https://arxiv.org/abs/2510.10114) (2510.10114) | 20251011 | none stated | Relation-free "Tri-Graph" from entity extraction and semantic linking; two-stage passage retrieval [1] | `DEEP-PolyU/LinearRAG` (README cites id) [9] |

### 2.2 Agentic or reinforcement-learned retrieval and traversal

The first four rows are not graph methods: they are the plain-RAG agent baselines that the graph
agents are compared with.

| Paper | Date | Venue | Idea (from the abstract) | Repo |
|---|---|---|---|---|
| [Search-o1](https://arxiv.org/abs/2501.05366) (2501.05366) | 20250109 | none stated | Agentic search inside a reasoning model, plus a Reason-in-Documents module [1] | `RUC-NLPIR/Search-o1` (README cites id) [9] |
| [Search-R1](https://arxiv.org/abs/2503.09516) (2503.09516) | 20250312 | none stated | The LLM learns multi-turn search with outcome-based reinforcement learning [1] | `PeterGriffinJin/Search-R1` (README cites id) [9] |
| [Search-P1](https://arxiv.org/abs/2602.22576) (2602.22576) | 20260226 | **unstated** | Path-centric reward shaping for agentic RAG training; title and first lines only [2] | **unstated** |
| [GRASP](https://arxiv.org/abs/2607.10463) (2607.10463) | 20260711 | **unstated** | Granularity-aware search policy for agentic RAG; title and first lines only [2] | **unstated** |
| [Knowledge Graph Prompting for Multi-Document QA](https://arxiv.org/abs/2308.11730) (2308.11730) | 20230822 | none stated | An LLM agent traverses a passage graph to collect context [1] | `yuwvandy/KG-LLM-MDQA` (README cites id) [9] |
| [Think-on-Graph](https://arxiv.org/abs/2307.07697) (2307.07697) | 20230715 | ICLR 2024 | Training-free LLM agent runs beam search over KG reasoning paths [1] | `DataArcTech/ToG` (README cites id). The URL tried, `IDEA-FinAI/ToG`, resolved to this name [9] |
| [Graph-R1](https://arxiv.org/abs/2507.21892) (2507.21892) | 20250729 | ICML 2026 | End-to-end RL trains a multi-turn agent that retrieves from a knowledge hypergraph [1] | `LHRLAB/Graph-R1` (README cites id) [9] |
| [GraphRAG-R1](https://arxiv.org/abs/2507.23581) (2507.23581) | 20250731 | The Web Conference 2026 | Process-constrained outcome RL with progressive retrieval and cost-aware rewards [1] | `ycygit/GraphRAG-R1` (README cites id; found by a name search, owner link to the authors not checked) [9] |
| [GraphSearch](https://arxiv.org/abs/2509.22009) (2509.22009) | 20250926 | none stated | Six-module agentic workflow pairing semantic text queries with graph queries [1] | `DataArcTech/GraphSearch` (README cites id) [9] |
| [GraphWalker](https://arxiv.org/abs/2603.28533) (2603.28533) | 20260330 | COLM 2026 | Agentic KG question answering: SFT on random-walk synthetic trajectories, then light RL [1] | **unstated** |
| [PathRouter](https://arxiv.org/abs/2606.16409) (2606.16409) | 20260615 | none stated | Reward and advantage scaling by trajectory category for agentic GraphRAG [1] | **unstated** |
| [Search-on-Graph-R1](https://arxiv.org/abs/2607.18481) (2607.18481) | 20260720 | none stated | Gold-SPARQL-guided teacher trajectories distilled by SFT, then RL, into an 8B model [1] | **unstated** |
| [MOSAIC](https://arxiv.org/abs/2609.11065) (2609.11065) | 20260910 | none stated | Training-free LLM analyser sets per-query bounds for seeds, traversal, stopping, evidence [1] | **unstated** |
| [RANGER](https://arxiv.org/abs/2610.28010) (2610.28010) | 20261020 | **unstated** | Retrieval agent navigating graphs with semantic evaluation rewards; title and first lines only [2] | **unstated** |

### 2.3 Memory for agents

| Paper | Date | Venue | Idea (from the abstract) | Repo |
|---|---|---|---|---|
| [Generative Agents](https://arxiv.org/abs/2304.03442) (2304.03442) | 20230407 | none stated | Agents store experiences, synthesise reflections, retrieve memories to plan [1] | `joonspk-research/generative_agents` (README cites id) [9] |
| [MemGPT](https://arxiv.org/abs/2310.08560) (2310.08560) | 20231012 | none stated | OS-style hierarchical memory tiers with interrupts to extend the context window [1] | `letta-ai/letta`: its README says "Letta (f.k.a. MemGPT)"; it does not cite the id [9] |
| [Zep / Graphiti](https://arxiv.org/abs/2501.13956) (2501.13956) | 20250120 | none stated | Temporal knowledge graph engine fusing conversational and business data [1] | `getzep/graphiti` (README cites id) [9] |
| [A-MEM](https://arxiv.org/abs/2502.12110) (2502.12110) | 20250217 | NeurIPS 2025 | Zettelkasten-style notes with dynamic links and evolving contents [1] | `agiresearch/A-mem` (README cites id) [9] |
| [Mem0](https://arxiv.org/abs/2504.19413) (2504.19413) | 20250428 | none stated | Extracts, consolidates and retrieves dialogue facts; optional graph memory [1] | `mem0ai/mem0` (README cites id) [9] |
| [MemOS](https://arxiv.org/abs/2507.03724) (2507.03724) | 20250704 | none stated | A memory operating system unifying plaintext, activation and parameter memory in "MemCube" units [1] | `MemTensor/MemOS` (README cites id) [9] |
| [Memory-R1](https://arxiv.org/abs/2508.19828) (2508.19828) | 20250827 | none stated | RL-trained Memory Manager and Answer Agent learn memory operations from outcome rewards [1] | **unstated**. A name search returned `yansikuan/memory-r1` (131 stars; name matches the first author); README not checked [9] |
| [SAGE](https://arxiv.org/abs/2605.12061) (2605.12061) | 20260512 | none stated | A writer builds graph memory; a graph foundation model reads it and feeds back [1] | **unstated** |
| [Memory is Reconstructed, Not Retrieved](https://arxiv.org/abs/2606.06036) (2606.06036) | 20260604 | ICML 2026 | Cue-Tag-Content associative memory graph with LLM-guided path exploration and pruning [1] | **unstated** |

### 2.4 Knowledge-graph construction with LLMs

For the benchmark Text2KGBench see section 4. These rows are the construction methods.

| Paper | Date | Venue | Idea (from the listing) | Repo |
|---|---|---|---|---|
| [Extract, Define, Canonicalize (EDC)](https://arxiv.org/abs/2404.03868) (2404.03868) | 20240405 | **unstated** | LLM-based framework for KG construction from text (title: extract, define, canonicalize). National University of Singapore [2] | `clear-nus/edc` (README cites id) [9] |
| [AutoSchemaKG](https://arxiv.org/abs/2505.23628) (2505.23628) | 20250529 | **unstated** | Fully autonomous KG construction with dynamic schema induction from web-scale corpora [2] | `HKUST-KnowComp/AutoSchemaKG` (README cites id) [9] |
| [Are Large Language Models Effective Knowledge Graph Constructors?](https://arxiv.org/abs/2510.11297) (2510.11297) | 20251013 | **unstated** | Evaluation of zero-shot, document-grounded KG construction by LLMs [2] | **unstated** |
| [DIAL-KG](https://arxiv.org/abs/2603.20059) (2603.20059) | 20260320 | **unstated** | Schema-free incremental KG construction with dynamic schema induction [2] | **unstated** |
| [OntoKG](https://arxiv.org/abs/2604.02618) (2604.02618) | 20260403 | **unstated** | Ontology-oriented construction of a typed property graph [2] | **unstated** |
| [Better Later Than Sooner](https://arxiv.org/abs/2605.29168) (2605.29168) | 20260527 | **unstated** | Ontology-grounded correction after extraction, aimed at multi-hop and aggregation questions [2] | **unstated** |
| [From Extraction to Governed Memory](https://arxiv.org/abs/2608.28642) (2608.28642) | 20260812 | **unstated** | Multi-agent KG construction with domain-expert review; records who owns each fact and why it was admitted [2] | **unstated** |

LLM-based graph construction is also the first stage of most methods in 2.1; the cost and noise of
that stage appear in section 3 (rows for [5] and [6]).

### 2.5 Text to graph query (Cypher, SPARQL)

All rows are from the discovery listing [2]; the Text2Cypher dataset sizes are in section 4.

| Paper | Date | Venue | What it is | Repo |
|---|---|---|---|---|
| [Text2Cypher: Bridging Natural Language and Graph Databases](https://arxiv.org/abs/2412.10064) (2412.10064, Neo4j) | 20241213 | none stated [1] | Dataset of 44,387 instances scored with Google-BLEU and Exact Match [1] | `neo4j-labs/text2cypher` (exists; README: **no**) [9] |
| [Text2Cypher Across Languages](https://arxiv.org/abs/2506.21445) (2506.21445, Neo4j) | 20250626 | **unstated** | Multilingual evaluation and fine-tuning | **unstated** |
| [SPARQL-LLM](https://arxiv.org/abs/2512.14277) (2512.14277, SIB / Zurich) | 20251216 | **unstated** | Real-time SPARQL generation from natural language questions | **unstated** |
| [Text2GraphQuery-Bench](https://arxiv.org/abs/2602.11745) (2602.11745) | 20260212 | none stated [1] | Benchmark across graph query languages (see section 4) | **unstated** |
| [PIPE-Cypher](https://arxiv.org/abs/2606.08481) (2606.08481) | 20260607 | **unstated** | Automatic enterprise benchmark generation for text-to-Cypher | **unstated** |
| [KG2Cypher](https://arxiv.org/abs/2606.27742) (2606.27742) | 20260626 | **unstated** | Data-centric pipeline for enterprise text-to-Cypher systems | **unstated** |
| [SAGA](https://arxiv.org/abs/2607.14494) (2607.14494, Tokyo / RIKEN) | 20260716 | **unstated** | Schema-aware grounding for agentic text-to-SPARQL | **unstated** |
| [CypherTurn](https://arxiv.org/abs/2609.36987) (2609.36987) | 20260929 | **unstated** | Multi-turn conversational text-to-Cypher benchmark | **unstated** |
| [SPARQL-LLM in the TEXT2SPARQL 2026 Challenge](https://arxiv.org/abs/2610.13648) (2610.13648) | 20261009 | **unstated** | A challenge submission; shows a TEXT2SPARQL 2026 challenge exists | **unstated** |

## 3. Does a graph help?

The published evaluations that put graph-based and plain retrieval side by side. "Who ran it"
matters: a project's own paper, a paper that introduces a benchmark, and an independent
comparison answer different questions. Numbers are copied from the cited source; "n/r" means not
reported in the pages read.

### 3.1 Graph RAG against plain RAG, over documents

| Study (who ran it) | Setup | Result | Caveats | Src |
|---|---|---|---|---|
| Han et al., *RAG vs. GraphRAG* (MSU, Oregon, UTA, Meta, IBM; authors of the GraphRAG survey above) 2502.11371, v3 20260304 | Unified protocol: Llama-3.1-8B and 70B generators, GPT-4o-mini builds graphs, ada-002 embeddings, 256-token chunks, top-10. QA on NQ, HotpotQA (1,000 hard bridge questions), MultiHop-RAG (2,556 queries), NovelQA; summarisation on SQuALITY, QMSum, ODSum | **NQ F1**: RAG 64.78, Community-Local 63.01, HippoRAG2 61.03, KG-triplets 34.28. **HotpotQA F1**: RAG 60.04, HippoRAG2 63.01, Community-Local 61.66, KG-triplets 25.02. **MultiHop-RAG accuracy (8B)**: RAG 67.02, HippoRAG2 70.27, Community-Local 69.01; **(70B)** RAG 65.77, Community-Local with graph built by GPT-4o-mini 71.17, by GPT-4o 75.08. **Null queries (8B)**: RAG 96.01, Community-Local 80.07, Community-Global 19.27; iterative retrieval cut Community-Local's null accuracy from 80.07 to 50.50. **Cost on MultiHop-RAG**: construction 135 s (RAG), 5,560 s (Community), 7,702 s (KG); retrieved tokens 3,631 (RAG) vs 9,770 (Community). On MultiHop-RAG 13.6% of queries only GraphRAG got right and 11.6% only RAG. Summarisation: RAG matches detailed reference summaries better; Community-Global wins on diversity | Single configuration; top-10 fixed (giving RAG as many tokens as GraphRAG helped RAG slightly, conclusions unchanged). Only about 65.8% (HotpotQA) and 65.5% (NQ) of answer entities appear in the constructed KG. LLM-as-judge showed position bias | [6] |
| Xiang et al., *GraphRAG-Bench* (Xiamen University, PolyU; ICLR 2026) 2506.05690, v3 20260222 | Own benchmark: 4,076 questions, four task levels, two corpora (Novel; Medical = NCCN guidelines). GPT-4o-mini generator. Table 9 has 13 rows: two RAG baselines and 11 GraphRAG entries | Accuracy, Novel, RAG with rerank vs HippoRAG2: fact retrieval 60.92 vs 60.14; complex reasoning 42.93 vs 53.38; summarisation 51.30 vs 64.10; creative 38.26 vs 48.28. Medical: 64.73 vs 66.28; 58.64 vs 61.98; 65.75 vs 63.08; 60.61 vs 68.05. MS-GraphRAG local on Novel fact retrieval 49.29 (below RAG). The abstract cites recent studies reporting that GraphRAG frequently underperforms vanilla RAG on many real-world tasks | The benchmark was built by the authors to have denser entity graphs than HotpotQA-type sets [3]. **Table 17 inconsistency:** it is captioned Novel, but its small-tier RAG row (64.73, 58.64, 65.75, 60.61) equals the Medical RAG row of Table 9, not the Novel row (60.92, 42.93, 51.30, 38.26). The stated RAG decline with corpus size (complex reasoning 58.64 to 43.20) therefore depends on that row; using the Novel figure 42.93 as the small tier gives 42.93, 41.33, 43.20 (my comparison, no decline). HippoRAG2 stays 53.38, 56.67, 54.29 | [3] |
| Fan et al., *RAGSearch* (NYU Shanghai) 2604.09666, 20260401 | Six QA sets from FlashRAG (NQ, PopQA, TriviaQA; HotpotQA, 2Wiki, MuSiQue), full dev/test sets, Qwen2.5-7B; dense RAG against five GraphRAG backends under single-shot, training-free agentic and RL agentic inference. Metric Contain-EM | Single-shot: +0.47 average on general QA, **+27.23 on multi-hop**. With the GraphSearch agent, dense vs best GraphRAG: HotpotQA 38.22 vs 58.64, 2Wiki 47.43 vs 79.88, MuSiQue 13.33 vs 55.26. RL, different agents: Search-R1 vs Graph-R1 35.76 vs 53.42, 33.56 vs 66.25, 14.42 vs 40.82 (the three pairs are not labelled by dataset in the pages read; the [Graph-R1 entry](../projects/graph-r1.md) gives other gaps under a different protocol). The authors conclude agentic search narrows the gap (most with RL) but GraphRAG stays ahead on complex multi-hop | The GraphRAG figure is the **best of five** variants against one dense baseline. The setup text says the dense backend retrieves from the 2018 Wikipedia dump while the GraphRAG backends use each question's context as the document, so the knowledge sources differ; the pages read do not say how much of the gap this explains. Efficiency appendix not read | [4] |
| Wang et al., *BM25 Wins at Scale* (USTC, Metastone) 2607.26497, v3 20260731 | EnterpriseRAG-Bench (synthetic enterprise corpus), 500 questions; 28 nested corpus sizes from 1,144 to 511,959 documents; one reader (Qwen3.6-27B), top-5 chunks; official combined score | At 1,144 docs: BM25 74.7, HippoRAG 2 66.2, DenseRAG 58.1, LightRAG 48.0, LinearRAG 46.2, MS-GraphRAG 45.9. At 131,876 docs: BM25 55.2, DenseRAG 36.0, HippoRAG 2 41.0, LinearRAG 29.8. Full corpus: BM25 50.5, DenseRAG 29.9. **Graph builds stopped**: LightRAG at 2,254 docs, MS-GraphRAG at 8,750, HippoRAG 2 and LinearRAG at 131,876. HippoRAG 2 build: 724M tokens at 155M corpus tokens (fitted 2.9B tokens, about 3 instance-days, at full size); MS-GraphRAG about 50 instance-days; LightRAG super-linear, about 4 instance-years | Questions carry exact lexical anchors and "trap" documents that are semantically close but wrong, which the authors say favours exact matching. Synthetic corpus; one run per question; one reader. A raw-file agent leads below about 10M corpus tokens | [5] |
| Chen et al., *Is GraphRAG Needed?* (AWS, Cisco) 2606.25656, 20260624; ACL 2026 GEM Workshop [1] | STaRK-Prime (129K entities, 8.1M relations), Claude 3.7 Sonnet, nine scenarios | Hit@1: text documents only 0.6147; text plus 1-hop relation lists 0.6972; GraphRAG with predefined KG 0.6422; GraphRAG with a KG computed from the documents 0.5596; KG only 0.1376. Agentic RAG, document tool only 0.6881; same agent with a KG tool 0.6055. The authors state that simple relational augmentation beat their GraphRAG scenario | One dataset, one LLM, a single run each, no hyperparameter sweep. Test-set size **unstated** in the pages read; the Hit@1 values are multiples of 1/109, which suggests about 109 queries (my inference). Metrics are retrieval-oriented | [7] |
| Zarrinkia et al. 2603.14045, 20260314 (under review) | KET-RAG on HotpotQA, MuSiQue, 2Wiki | The gold answer is in the context for 77% to 91% of questions, but accuracy is 35% to 78%; 73% to 84% of errors are reasoning failures | Abstract only; retrieval is not the bottleneck here | [1] |
| Jonah et al. 2607.16604, 20260718 | Five RAG configurations, four multimodal generators, three document corpora | Retrieval-time KG expansion raised gold-evidence completeness from 0.22 to 0.46 (HotpotQA bridge questions) and from 0.50 to 0.72 (SPIQA cross-paper) | Abstract only. The metric is evidence completeness, not answer accuracy | [1] |
| Zhang et al. 2609.18099, 20260916 (EffiRAG) | UltraDomain, 120 open-ended questions | Their lower-cost graph RAG preferred on 93 questions against 7 for LightRAG-hybrid (20 split); cost USD 0.952 to 0.408 | Graph against graph, by the authors of the winning system; abstract only | [1] |
| Authors' own claims (first-party) | GraphRAG paper 2404.16130 (Edge et al.): datasets around 1M tokens. HippoRAG 2 paper 2502.14802 | GraphRAG: "substantial improvements" over conventional RAG in comprehensiveness and diversity (pairwise LLM judging). HippoRAG 2: "7% improvement in associative memory tasks over the state-of-the-art embedding model"; the abstract fragment retrieved also says performance on basic factual memory "drops considerably below standard RAG" (the sentence's subject was not retrieved) | First-party. Han et al. found that LLM-judge order changes verdicts and that reference-based metrics favoured RAG on their summarisation tasks [6] | [1], [6] |

Also seen, abstract only, no numbers read: *Is Agentic RAG worth it?* 2601.07711 (ACL 2026
Industry Track, compares enhanced and agentic RAG on performance and cost); *Towards Robust RAG
Based on Knowledge Graph* 2603.05698 (IEEE SMC 2025, RGB corpus, four robustness scenarios)
[1].

### 3.2 Graph memory against plain retrieval for agents

| Study (who ran it) | Setup | Result | Caveats | Src |
|---|---|---|---|---|
| Bao et al. 2610.30755, 20261022 ("Naive RAG Is Stronger Than We Thought") | Raw dense retrieval plus reranking over raw history, against agentic memory systems; LoCoMo, LongMemEval, MEME, MemoryAgentBench | Raw-RAG ranks first in six of seven benchmark-model settings, ahead of the strongest agentic memory system by 0.13 to 5.53 points | Abstract only. Which systems count as "agentic memory", and whether graph-based ones are among them, is **unstated** in what was read | [1] |
| Huang et al. 2608.15008, 20260815 ("Harness the Memory") | Memory substrates (dense and sparse indices, text records, structural and hierarchical stores) across three backbones, four suites, 26 metrics | No single substrate dominates; the authors propose routing between them | Abstract only; no numbers read | [1] |
| Mem0 team 2504.19413 (first-party) | LOCOMO | Graph-memory variant "around 2% higher overall score" than the base configuration; 26% relative gain over OpenAI on the LLM-as-a-judge metric; 91% lower p95 latency; more than 90% lower token cost | Self-reported by the product's authors | [1] |
| Zep team 2501.13956 (first-party) | Deep Memory Retrieval; LongMemEval | DMR 94.8% vs MemGPT 93.4%; LongMemEval accuracy gains "up to 18.5%" with 90% lower latency | Self-reported; baselines and judge are the authors' choice | [1] |

### 3.3 Reading across the rows

These are observations about the rows above, not recommendations.

- Where graph methods win in the independent studies, the gain is on **multi-hop** questions
  (HotpotQA, MultiHop-RAG, complex reasoning). On single-hop or detail questions plain RAG
  matches or beats them [3], [6]. The size of the multi-hop gain ranges from about 3 points
  (8B generator) to about 9 points (70B generator, graph built by GPT-4o) in [6], about 10 points
  on complex reasoning in [3], and 27 points in [4]; the 27-point comparison has a
  knowledge-source difference (above).
- The studies that vary the corpus find different things: graph methods keep accuracy as a corpus
  grows in [3] (subject to the Table 17 issue), but fall behind BM25 and could not be built at
  scale in [5].
- The graph is only as good as its construction: [6] finds the answer entity missing from the
  constructed KG about a third of the time, and [7] finds a KG computed from documents (0.5596)
  below the same data without one (0.6147), while a predefined KG helped (0.6422).
- Retrieval gains do not always reach the answer: [7] reports ground-truth entity recall of 83.5%
  in retrieval but 47.9% in the LLM's answer; 2603.14045 reports the same pattern [1].

## 4. Benchmarks and datasets

Sizes are quoted from the source named; **unstated** means the abstract (or the page read) gives
none. "Used by" lists only studies read in this run.

### 4.1 Multi-hop and document question answering

| Name | Task | Size | Metric | What it tests | Used by | Link |
|---|---|---|---|---|---|---|
| HotpotQA (EMNLP 2018) | Multi-hop QA over Wikipedia | 113k QA pairs [1]; dev 7,405 [4] | Answer EM/F1; supporting-fact accuracy [1] | Reasoning over several supporting documents; explainable evidence | [4], [6], 2603.14045 | [1809.09600](https://arxiv.org/abs/1809.09600) |
| 2WikiMultiHopQA (COLING 2020) | Multi-hop QA | Abstract gives none; train 15,000, dev 12,576 [4] | Answer EM/F1; evidence path [1] | Reading several paragraphs along a reasoning path | [4], 2603.14045 | [2011.01060](https://arxiv.org/abs/2011.01060) |
| MuSiQue (TACL 2022) | Multi-hop QA built from single-hop questions | 25K questions of 2 to 4 hops [1]; dev 2,417 [4] | Answer EM/F1 | Real multi-step composition: a single-hop model loses 30 F1 [1] | [4], 2603.14045 | [2108.00573](https://arxiv.org/abs/2108.00573) |
| MultiHop-RAG | Multi-hop QA over news, with metadata | 2,556 queries; evidence in 2 to 4 documents [6]; none stated in abstract | Accuracy | Four query types: inference, comparison, temporal, null (no answer) [6] | [6] | [2401.15391](https://arxiv.org/abs/2401.15391) |
| UltraDomain | Open-ended questions over long domain corpora | 2,500 questions [3] (cited there as Qian et al. 2024, the first author of MemoRAG; the MemoRAG paper was not read) | Pairwise LLM preference in 2609.18099 [1] | Global, summary-type questions over large domain text | [3], 2609.18099 | MemoRAG: [2409.05591](https://arxiv.org/abs/2409.05591) |
| FRAMES (NAACL 2025) | Multi-hop RAG over retrieved documents | **unstated** in abstract | Accuracy: 0.40 with no retrieval, 0.66 with multi-step retrieval [1] | Fact, fetch and reason together | none in this run | [2409.12941](https://arxiv.org/abs/2409.12941) |
| CRAG (NeurIPS 2024 D&B) | Factual QA, mixed sources | 4,409 QA pairs; 5 domains, 8 question categories [1] | Accuracy (most LLMs at most 34%; 44% with RAG) [1] | Realistic RAG across question types | none in this run | [2406.04744](https://arxiv.org/abs/2406.04744) |
| STaRK (NeurIPS 2024 D&B) | Retrieval over text-plus-relation knowledge bases | Three domains [1]; STaRK-Prime: 129K entities, 8.1M relations [7] | Hit@1, Hit@5, R@20, MRR [7] | Joint use of text and relations | [7] | [2404.13207](https://arxiv.org/abs/2404.13207) |
| EnterpriseRAG-Bench | RAG over company-internal data (Onyx, UC Berkeley [2]) | 511,957 documents, 600.8M tokens, 500 questions in ten categories [5], [1] | Alignment, atomic-fact entailment, combined score, document recall [5] | Lookups, multi-document reasoning, conflict resolution, absent information [1]; 20 "not found" questions [5]; synthetic company [5] | [5] | [2605.05253](https://arxiv.org/abs/2605.05253) |

### 4.2 GraphRAG-specific

Two unrelated benchmarks share the name **GraphRAG-Bench**. Cite them by first author.

| Name | Task | Size | Metric | What it tests | Used by | Link |
|---|---|---|---|---|---|---|
| GraphRAG-Bench (Xiang et al., ICLR 2026) | Four task levels: fact retrieval, complex reasoning, contextual summarisation, creative generation | 4,076 questions [3]; corpora: NCCN medical guidelines and pre-20th-century novels [3] | Accuracy, ROUGE-L, coverage, faithfulness score, plus stage-wise graph and retrieval metrics [3] | Graph-building quality, retrieval and generation, on corpora denser in entity links than HotpotQA-type sets [3] | [3] | [2506.05690](https://arxiv.org/abs/2506.05690); data and leaderboard: [GraphRAG-Bench/GraphRAG-Benchmark](https://github.com/GraphRAG-Bench/GraphRAG-Benchmark) (README cites id) [9] |
| GraphRAG-Bench (Xiao et al.) | Domain-specific reasoning; five question formats (multiple choice, true/false, multi-select, open-ended, fill-in-the-blank) | 16 disciplines from twenty textbooks; question count **unstated** in abstract [1] | **unstated** in abstract | Nine GraphRAG methods applied to textbook reasoning [1] | none in this run | [2506.02404](https://arxiv.org/abs/2506.02404) |
| WildGraphBench | Single-fact QA, multi-fact QA, section-level summarisation on wild-source corpora | 1,100 questions, 3 complexity levels, 12 top-level topics [1] | **unstated** in abstract | GraphRAG on messy real-world sources | none in this run | [2602.02053](https://arxiv.org/abs/2602.02053) |
| RAGSearch (NYU Shanghai) | Dense RAG vs GraphRAG as retrieval backends under agentic search | Full dev/test sets of six QA datasets [4] | Contain-EM, F1; also offline preprocessing cost and online efficiency [4] | Whether agentic search removes the need for a graph | [4] | [2604.09666](https://arxiv.org/abs/2604.09666); code: `FanDongzhe123/RAGSearch` (named in the paper) [4], [9] |
| TopoGraphRAG-Bench | Multimodal GraphRAG on layout-grounded evidence | **unstated** | **unstated** | Evidence spread across text, tables, figures, captions | none in this run | [2610.09360](https://arxiv.org/abs/2610.09360) (listing only [2]) |
| ENTLORE | Enterprise QA needing latent organisational relations | **unstated** | **unstated** | Graph-grounded organisational reasoning | none in this run | [2608.10679](https://arxiv.org/abs/2608.10679) (listing only [2]) |

### 4.3 Agent memory

| Name | Task | Size | Metric | What it tests | Used by | Link |
|---|---|---|---|---|---|---|
| LongMemEval (ICLR 2025) | Chat-assistant long-term memory QA | 500 questions in scalable chat histories [1] | Accuracy (baseline systems lose 30% on sustained interactions) [1] | Five abilities: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, abstention [1] | Zep paper (2501.13956), 2610.30755 [1] | [2410.10813](https://arxiv.org/abs/2410.10813); code `xiaowu0162/LongMemEval` (README cites id) [9] |
| LoCoMo | Very long conversations: QA, event summarisation, multimodal dialogue | Conversations of about 300 turns, 9K tokens on average, up to 35 sessions; number of conversations and questions **unstated** in abstract [1]. A 2026 paper's title names a 1,540-question "LoCoMo-1540" subset (title only; 2610.05343) [2] | Task-specific; LLM-judge in Mem0 [1] | Memory of long dialogue over many sessions | Mem0 paper (2504.19413), 2610.30755 [1] | [2402.17753](https://arxiv.org/abs/2402.17753); code `snap-research/locomo` [9] |
| MemoryAgentBench | Incremental multi-turn interactions | **unstated** | **unstated** | Four competencies: accurate retrieval, test-time learning, long-range understanding, selective forgetting [1] | 2610.30755 [1] | [2507.05257](https://arxiv.org/abs/2507.05257); code `HUST-AI-HYZ/MemoryAgentBench` (README cites id) [9] |
| LoCoMo-Plus | Beyond-factual (cognitive) memory evaluation | **unstated** | "Constraint consistency" framework in place of string matching [1] | Memory that shapes later behaviour, not only recall | none in this run | [2602.10715](https://arxiv.org/abs/2602.10715) |
| AMA-Bench | Long-horizon memory for agentic applications | **unstated**; expert-curated QA plus synthetic trajectories [1] | Accuracy (the authors' own agent: 57.22%) [1] | Agent trajectories rather than chat | none in this run | [2602.22769](https://arxiv.org/abs/2602.22769); code `AMA-Bench/AMA-Bench` (README cites id) [9] |
| EvoMemBench | Self-evolving agent memory | **unstated**; 15 memory methods compared [1] | **unstated** | Memory scope (in-episode vs cross-episode) by content (knowledge vs execution) [1] | none in this run | [2605.18421](https://arxiv.org/abs/2605.18421) |
| RECON | Compositional reasoning over long contexts | 24 case files in three domains, 50k to 100k tokens each [1] | **unstated** | Six tasks including cascading invalidations, source conflicts, counterfactuals, temporal constraints [1] | none in this run | [2607.16716](https://arxiv.org/abs/2607.16716) |
| GateMem | Memory governance for shared agents | **unstated** | **unstated** | Access control across authorisation boundaries; active forgetting after deletion requests [1] | none in this run | [2606.18829](https://arxiv.org/abs/2606.18829) |
| When Users Don't Ask (EMNLP 2026 Findings) | Context-driven memory retrieval | **unstated**; derived from LoCoMo [1] | **unstated** | Four query styles: dialog, implicit, counterfactual, composed [1] | none in this run | [2609.03467](https://arxiv.org/abs/2609.03467) |

### 4.4 Knowledge-graph construction and graph query

| Name | Task | Size | Metric | What it tests | Used by | Link |
|---|---|---|---|---|---|---|
| Text2KGBench (ISWC 2023) | Ontology-driven KG generation from text | Wikidata-TekGen: 10 ontologies, 13,474 sentences; DBpedia-WebNLG: 19 ontologies, 4,860 sentences [1] | Seven metrics: fact extraction, ontology conformance, hallucination [1] | Whether extracted triples follow the ontology | none in this run | [2308.02357](https://arxiv.org/abs/2308.02357); code `cenguix/Text2KGBench` (README: **no**) [9] |
| Text2Cypher dataset (Neo4j) | Natural language to Cypher | 44,387 instances [1] | Google-BLEU, Exact Match [1] | Query generation for graph databases | none in this run | [2412.10064](https://arxiv.org/abs/2412.10064) |
| Text2GraphQuery-Bench | Natural language to several graph query languages | 267,276 (question, graph query) pairs over 34 databases and 13 domains [1] | Grammar, GLEU, Similarity, execution accuracy [1] | Query generation across graph languages | none in this run | [2602.11745](https://arxiv.org/abs/2602.11745) |
| FinReflectKG-EvalBench | Evaluating financial KGs extracted by LLMs | **unstated** | **unstated** | Multi-dimensional evaluation of extraction | none in this run | [2510.05710](https://arxiv.org/abs/2510.05710) (listing only [2]) |

## 5. What the benchmarks do not measure

Each row says what the sources show about the gap. "Not found" means not found in the sources
read in this run, which is a statement about the search, not about the literature.

| Dimension | State in the sources read | Evidence |
|---|---|---|
| **Cost of building the graph** | Most accuracy benchmarks report none. A few studies meter it: RAGSearch reports offline preprocessing cost; the BM25 study meters build tokens and finds graph builds failing to finish at scale; Han et al. report construction seconds. The BM25 paper's own related-work section says existing RAG benchmarks "rarely meter offline cost" | [4], [5], [6] |
| **Query-time cost and latency** | Reported in few papers: 226K tokens per question for a file-system agent against 5.8K for BM25 [5]; retrieved tokens 9,770 vs 3,631 [6]; Mem0 reports p95 latency [1]. Not part of HotpotQA, 2Wiki, MuSiQue scoring | [1], [5], [6] |
| **Corpus size** | The BM25 study says published evaluations "generally remain at a fixed, relatively small corpus size"; it varies size over 450-fold. The ranking of paradigms changed with size there | [5] |
| **Whether the corpus has graph structure to exploit** | GraphRAG-Bench (Xiang) measured entity-graph density of common sets: average degree 0.60 (MuSiQue), 0.64 (2Wiki), 0.65 (HotpotQA), 0.76 (MultiHop-RAG), 0.86 (UltraDomain), against 1.05 and 2.27 for its two subsets. A benchmark with sparse links gives a graph little to use, and the authors designed theirs to differ | [3] |
| **Abstention** | Only some sets test "no answer": MultiHop-RAG null queries, LongMemEval abstention, 20 "not found" questions in EnterpriseRAG-Bench. The answerable HotpotQA, 2Wiki and MuSiQue variants used in [4] do not. The gap matters: Community-Global scored 19.27 on null queries against 96.01 for RAG, and iterative retrieval or reranking lowered null accuracy [6] | [1], [5], [6] |
| **Freshness and updates** | Few sets change the knowledge over time: LongMemEval (knowledge updates), MemoryAgentBench (selective forgetting), RECON (cascading invalidations), GateMem (forgetting after deletion). LightRAG advertises an incremental update algorithm [1]; a study of answer quality after incremental updates to a graph index was **not found** | [1] |
| **Retrieval quality vs answer quality** | Retrieval metrics can overstate: 83.5% of ground-truth entities retrieved, 47.9% in the answer [7]; the gold answer was in context 77% to 91% of the time yet accuracy was 35% to 78% [1: 2603.14045]. The same retrieval can fail at generation | [1], [7] |
| **Graph construction quality** | Rarely scored on its own in QA sets. [6] measured answer-entity coverage in the built KG (about 65%); GraphRAG-Bench scores graph stages separately [3]; Text2KGBench and the KG-construction survey cover extraction itself [1] | [1], [3], [6] |
| **Judge reliability** | LLM-as-judge verdicts changed with presentation order in [6]. The BM25 study measured 96.2% agreement between two judges [5]. Many GraphRAG wins are judged pairwise by an LLM | [5], [6] |
| **Data contamination** | GraphRAG-Bench picked lesser-known novels to limit overlap with pretraining data [3]. Wikipedia-based sets (HotpotQA, 2Wiki, MuSiQue) have no such control in the sources read; whether it matters is **unstated** | [3], [4] |
| **Synthetic vs real data** | EnterpriseRAG-Bench is a synthetic company [5]; GraphRAG-Bench's ontologies were built with GPT-4.1 [3]. How well results carry to real enterprise corpora is **unstated** | [3], [5] |
| **Security, provenance, permissions** | Listing shows work on attacks on GraphRAG (2610.19549), provenance (2610.37237, 2605.15109) and multi-principal access (GateMem). No common benchmark spanning them was found | [2], [1] |
| **Run-to-run variance** | Several studies run each system once per question (the BM25 study says so [5]; the AWS study reports single runs [7]). Small test sets make single-digit differences hard to read | [5], [7] |

## Sources

All sources were read on 20261030. The column "Read by" is the first clock reading (UTC) at or
after the fetch; the whole run took under ten minutes (clock readings 18:58, 19:02, 19:04).

| # | Source | URL | Read by |
|---|---|---|---|
| 1 | arXiv API records and abstracts (titles, authors, v1 dates, journal references, comments, abstract text) for every arXiv id linked above, fetched in batches | `http://export.arxiv.org/api/query?id_list=<ids>` (ids as linked in the tables) | 20261030 19:02 UTC |
| 2 | alphaXiv paper-discovery listings (dates, affiliations, first lines of abstracts), used where the table says "listing only" or cites [2] | `https://www.alphaxiv.org/abs/<id>` (e.g. 2605.05253) | 20261030 19:02 UTC |
| 3 | Xiang et al., *When to Use Graphs in RAG* (GraphRAG-Bench), v3, full text | https://arxiv.org/pdf/2506.05690 | 20261030 19:02 UTC |
| 4 | Fan et al., *Do We Still Need GraphRAG?* (RAGSearch), v1, full text | https://arxiv.org/pdf/2604.09666 | 20261030 19:02 UTC |
| 5 | Wang et al., *BM25 Wins at Scale*, v3, full text | https://arxiv.org/pdf/2607.26497 | 20261030 19:02 UTC |
| 6 | Han et al., *RAG vs. GraphRAG: A Systematic Evaluation and Key Insights*, v3, full text | https://arxiv.org/pdf/2502.11371 | 20261030 19:02 UTC |
| 7 | Chen et al., *Is GraphRAG Needed?*, v1, full text | https://arxiv.org/pdf/2606.25656 | 20261030 19:02 UTC |
| 8 | Reserved, no source. The number is kept so that the citations of source 9 stay stable | | |
| 9 | GitHub API: repository metadata (`archived`, existence) and README text searched for the arXiv id | `https://api.github.com/repos/<owner>/<repo>` and `/readme` (owner/repo as shown in the tables) | 20261030 19:04 UTC |

Not verified in this run:

- Repositories for 2026 papers marked **unstated** were not searched for.
- Venues are only what the arXiv record states; no publisher page was checked.
- Survey scope sentences summarise the abstract; the surveys themselves were not read.
- Papers marked "abstract only" or "listing only" were not read in full.
- The MemoRAG paper and the Xiao et al. GraphRAG-Bench paper were not read beyond their abstracts.
