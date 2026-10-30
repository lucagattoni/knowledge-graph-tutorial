# GitHub landscape snapshot 20261030_1913

- Snapshot time: 20261030 19:13 UTC
- Tool: `tools/gh_snapshot.py` version 1.0.0
- Search queries: 17 queries x 2 passes = 34 searches (1 page(s) of up to 100 each)
- API calls: 161 (search 34, GraphQL 6, REST 121, rate-limit checks 0)
- Repositories found: 924; flagged: 389; failures: 0
- Top N per category: 25; enrichment: on
- Compared with: no earlier snapshot
- Data: `repos.tsv` (all columns, every repository found) and `repos.json` (same records plus run metadata)

## How to read this

Stars are signals, not verdicts. They measure attention, not quality, correctness or fit, and they can be bought, boosted by a viral post, or earned by a list or tutorial rather than by software. Read a number with its date and with the other columns, then read the project.

- **Ranking rule:** within a category, repositories are ranked by stars among those pushed within the last 90 days (whole days since the last push, at most 90) and not archived. Everything else goes to that category's separate *quiet or archived* table, also sorted by stars.
- **Category:** each repository has one primary category: the watchlist's if it is listed there, otherwise the category whose queries returned it most often, ties broken in the order core, agent-memory, markdown-kb, adjacent. Search hits in other categories are kept in `repos.tsv` (`also_in`).
- **Relevance is not judged.** Queries match topics and keywords, and the ranking then promotes whatever is most starred, including awesome lists, tutorials and general agent tools that merely mention the subject. Read the description before treating an entry as in scope.
- **(w)** marks a watchlist repository, tracked whatever the search returns. It is shown even below the top N.
- **Stars/day** is stars divided by age in days (at least 1). It is an average over the repository's life.
- **Flags** are heuristics with editable thresholds (`tools/snapshot/queries.toml`), not accusations:

| Flag | Rule | What it suggests, and what it does not |
|---|---|---|
| `archived` | the repository is archived on GitHub | It no longer accepts changes. It does not say the ideas are obsolete. |
| `quiet` | more than 90 days since the last push | Little recent development. Mature, finished projects can look like this. |
| `fast-growth` | stars/day >= 150 | Unusually rapid attention. It can be organic (a viral launch) or not; check the star history and who is starring before drawing a conclusion. |
| `low-forks` | stars >= 5,000 and forks per 100 stars < 3 | Many stars but few forks. A common pattern for lists and for bought or boosted stars, and also for end-user apps nobody forks. |

- **Open issues** in `repos.tsv` count issues and pull requests together (GitHub's `open_issues_count`).
- **Commits (90 d)** counts commits on the default branch in the last 90 days and is **capped at 100**: `100+` means 100 or more.
- **Contributors** comes from the last page number of the contributors list (including anonymous ones). GitHub refuses it for some very large repositories; those show `-` and appear under Failures.
- **Licence** is GitHub's detection from the repository's LICENSE file (SPDX id). `NOASSERTION` means a licence file exists that GitHub could not match to one SPDX id; read it before reusing anything.

## core

GraphRAG frameworks, KG construction from text, KG querying including text-to-Cypher.

### core: ranked (pushed within 90 days)

| Rank | Repo | Stars | Forks | Stars/day | Created | Last push | Licence | Flags | Description |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 139,356 | 13,287 | 663.6 | 20260403 | 20261027 | Apache-2.0 | fast-growth | Turn any codebase, with its docs, SQL schemas, configs, and PDFs, into a queryable knowledge graph. A /graphify skill... |
| 2 | [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) (w) | 40,443 | 5,743 | 53.35 | 20241002 | 20261029 | MIT | - | [EMNLP2025] LightRAG: Simple and Fast Retrieval-Augmented Generation |
| 3 | [microsoft/graphrag](https://github.com/microsoft/graphrag) (w) | 36,498 | 3,868 | 38.54 | 20240327 | 20261029 | MIT | - | A modular graph-based Retrieval-Augmented Generation (RAG) system |
| 4 | [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph) | 32,508 | 2,957 | 132.15 | 20260226 | 20261029 | MIT | - | Local-first code intelligence graph for MCP and CLI. Builds a persistent map of your codebase so AI coding tools read... |
| 5 | [HKUDS/RAG-Anything](https://github.com/HKUDS/RAG-Anything) (w) | 24,322 | 2,845 | 47.6 | 20250606 | 20261028 | MIT | - | "RAG-Anything: All-in-One RAG Framework" |
| 6 | [semantica-agi/semantica](https://github.com/semantica-agi/semantica) | 14,349 | 1,687 | 29.16 | 20250625 | 20261030 | MIT | - | Graph-Native Infrastructure for Context and Accountable AI Systems |
| 7 | [vesoft-inc/nebula](https://github.com/vesoft-inc/nebula) | 12,463 | 1,342 | 4.18 | 20180828 | 20260908 | Apache-2.0 | - | A distributed, fast open-source graph database featuring horizontal scalability and high availability |
| 8 | [cocoindex-io/cocoindex](https://github.com/cocoindex-io/cocoindex) | 11,787 | 923 | 19.48 | 20250303 | 20261030 | Apache-2.0 | - | Incremental engine for long horizon agents 🌟 Star if you like it! |
| 9 | [adongwanai/AgentGuide](https://github.com/adongwanai/AgentGuide) | 11,458 | 1,073 | 31.74 | 20251103 | 20260915 | none detected | - | https://adongwanai.github.io/AgentGuide \| AI Agent开发指南 \| LangGraph实战 \| 高级RAG \| 转行大模型 \| 大模型面试 \| 算法工程师 \| 面试题库 \| 强化学习｜数据合成 |
| 10 | [trailhq/Trail-Code](https://github.com/trailhq/Trail-Code) | 10,952 | 972 | 92.03 | 20260703 | 20261030 | MIT | - | Turbocharge Claude Code, Cursor, Codex, Gemini & every coding agent: faster, cheaper, with contextual understanding s... |
| 11 | [FalkorDB/FalkorDB](https://github.com/FalkorDB/FalkorDB) | 10,505 | 600 | 8.77 | 20230720 | 20261030 | NOASSERTION | - | A super fast Graph Database uses GraphBLAS under the hood for its sparse adjacency matrix graph representation. Our g... |
| 12 | [deeplethe/utopia](https://github.com/deeplethe/utopia) | 8,640 | 1,183 | 104.1 | 20260807 | 20261030 | Apache-2.0 | - | World's first open-source enterprise world model. |
| 13 | [xerrors/Yuxi](https://github.com/xerrors/Yuxi) | 7,557 | 1,234 | 8.92 | 20240705 | 20261029 | MIT | - | 可私有部署的多租户知识智能体平台：统一 RAG、知识图谱、多智能体、MCP/Skills、沙盒与权限管理。Yuxi = Cloud Agents + Knowledge RAG, Self-hosted knowledge agent... |
| 14 | [potpie-ai/potpie](https://github.com/potpie-ai/potpie) | 5,782 | 694 | 7.15 | 20240812 | 20261030 | Apache-2.0 | - | Context Graph for AI Native SDLC |
| 15 | [neo4j-labs/llm-graph-builder](https://github.com/neo4j-labs/llm-graph-builder) (w) | 5,289 | 884 | 5.17 | 20240111 | 20261029 | Apache-2.0 | - | Neo4j graph construction from unstructured data using LLMs |
| 16 | [memgraph/memgraph](https://github.com/memgraph/memgraph) | 4,636 | 295 | 2.08 | 20200921 | 20261030 | NOASSERTION | - | High-performance open-source in-memory graph database for GraphRAG, AI memory, agentic AI, and real-time graph analyt... |
| 17 | [FlowElement-xinliuyuansu/m_flow](https://github.com/FlowElement-xinliuyuansu/m_flow) | 4,510 | 256 | 21.17 | 20260331 | 20260901 | Apache-2.0 | - | A bio-inspired cognitive memory engine — a new paradigm for Graph RAG. |
| 18 | [yifanfeng97/Hyper-Extract](https://github.com/yifanfeng97/Hyper-Extract) | 4,207 | 483 | 14.21 | 20260107 | 20261029 | NOASSERTION | - | Hypergraph is more powerful. Transform unstructured text into structured knowledge with LLMs. Graphs, hypergraphs, an... |
| 19 | [OSU-NLP-Group/HippoRAG](https://github.com/OSU-NLP-Group/HippoRAG) (w) | 4,083 | 437 | 4.59 | 20240523 | 20261006 | MIT | - | [NeurIPS'24] HippoRAG is a novel RAG framework inspired by human long-term memory that enables LLMs to continuously i... |
| 20 | [pipeshub-ai/pipeshub-ai](https://github.com/pipeshub-ai/pipeshub-ai) | 3,897 | 627 | 6.46 | 20250306 | 20261030 | Apache-2.0 | - | The open-source context layer for AI agents. PipesHub turns your company's knowledge (Slack, Drive, Jira, GitHub, Mic... |
| 21 | [GH05TCREW/pentestagent](https://github.com/GH05TCREW/pentestagent) | 3,224 | 644 | 6.06 | 20250515 | 20261026 | MIT | - | PentestAgent is an AI agent framework for black-box security testing, supporting bug bounty, red-team, and penetratio... |
| 22 | [robert-mcdermott/ai-knowledge-graph](https://github.com/robert-mcdermott/ai-knowledge-graph) | 3,134 | 421 | 5.35 | 20250323 | 20260913 | Apache-2.0 | - | AI Powered Knowledge Graph Generator |
| 23 | [MemMachine/MemMachine](https://github.com/MemMachine/MemMachine) | 3,078 | 225 | 6.98 | 20250815 | 20261029 | Apache-2.0 | - | Universal memory layer for AI Agents. It provides scalable, extensible, and interoperable memory storage and retrieva... |
| 24 | [pingcap/autoflow](https://github.com/pingcap/autoflow) | 2,978 | 193 | 2.98 | 20240205 | 20261023 | Apache-2.0 | - | pingcap/autoflow is a Graph RAG based and conversational knowledge base tool built with TiDB Serverless Vector Storag... |
| 25 | [trustgraph-ai/trustgraph](https://github.com/trustgraph-ai/trustgraph) | 2,854 | 339 | 3.39 | 20240710 | 20261028 | Apache-2.0 | - | The Governance Platform for Agents, Knowledge, and Context |
| 37 | [neo4j/neo4j-graphrag-python](https://github.com/neo4j/neo4j-graphrag-python) (w) | 1,326 | 259 | 1.36 | 20240227 | 20261030 | NOASSERTION | - | Neo4j GraphRAG for Python |
| 42 | [FalkorDB/GraphRAG-SDK](https://github.com/FalkorDB/GraphRAG-SDK) (w) | 1,029 | 147 | 1.02 | 20240125 | 20261030 | Apache-2.0 | - | Build fast and accurate GenAI apps with GraphRAG SDK at scale 🌟 |

103 more ranked repositories are in `repos.tsv`.

### core: quiet or archived

| Rank | Repo | Stars | Forks | Stars/day | Created | Last push | Licence | Flags | Description |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [memvid/memvid](https://github.com/memvid/memvid) | 17,321 | 1,465 | 33.25 | 20250527 | 20260714 | Apache-2.0 | quiet | Memory layer for AI Agents. Replace complex RAG pipelines with a serverless, single-file memory layer. Give your agen... |
| 2 | [OpenSPG/KAG](https://github.com/OpenSPG/KAG) (w) | 9,140 | 719 | 11.89 | 20240921 | 20260128 | Apache-2.0 | quiet | KAG is a logical form-guided reasoning and retrieval framework based on OpenSPG engine and LLMs. It is used to build... |
| 3 | [gusye1234/nano-graphrag](https://github.com/gusye1234/nano-graphrag) (w) | 4,006 | 427 | 4.84 | 20240725 | 20260127 | MIT | quiet | A simple, easy-to-hack GraphRAG implementation |
| 4 | [circlemind-ai/fast-graphrag](https://github.com/circlemind-ai/fast-graphrag) (w) | 3,967 | 258 | 5.43 | 20241030 | 20251101 | MIT | quiet | RAG that intelligently adapts to your use case, data, and queries |
| 5 | [aiming-lab/SimpleMem](https://github.com/aiming-lab/SimpleMem) | 3,858 | 409 | 12.82 | 20260101 | 20260724 | MIT | quiet | [ICML'26] SimpleMem: Efficient Lifelong Memory for LLM Agents — Text & Multimodal |
| 6 | [DEEP-PolyU/Awesome-GraphRAG](https://github.com/DEEP-PolyU/Awesome-GraphRAG) (w) | 2,682 | 238 | 3.63 | 20241021 | 20260602 | MIT | quiet | Awesome-GraphRAG: A curated list of resources (surveys, papers, benchmarks, and opensource projects) on graph-based r... |
| 7 | [kingjulio8238/Memary](https://github.com/kingjulio8238/Memary) | 2,663 | 206 | 2.86 | 20240410 | 20241022 | MIT | quiet | The Open Source Memory Layer For Autonomous Agents |
| 8 | [RManLuo/Awesome-LLM-KG](https://github.com/RManLuo/Awesome-LLM-KG) | 2,620 | 179 | 2.11 | 20230607 | 20250502 | none detected | quiet | Awesome papers about unifying LLMs and KGs |
| 9 | [heshengtao/comfyui_LLM_party](https://github.com/heshengtao/comfyui_LLM_party) | 2,386 | 210 | 2.57 | 20240413 | 20260729 | AGPL-3.0 | quiet | LLM Agent Framework in ComfyUI includes MCP sever, Omost,GPT-sovits, ChatTTS,GOT-OCR2.0, and FLUX prompt nodes,access... |
| 10 | [1517005260/graph-rag-agent](https://github.com/1517005260/graph-rag-agent) | 2,354 | 322 | 3.77 | 20250212 | 20251105 | MIT | quiet | 拼好RAG：手搓并融合了GraphRAG、LightRAG、Neo4j-llm-graph-builder进行知识图谱构建以及搜索；整合DeepSearch技术实现私域RAG的推理；自制针对GraphRAG的评估框架\| Integra... |
| 11 | [zjukg/KG-LLM-Papers](https://github.com/zjukg/KG-LLM-Papers) | 2,245 | 157 | 1.82 | 20230612 | 20260302 | MIT | quiet | [Paper List] Papers integrating knowledge graphs (KGs) and large language models (LLMs) |
| 12 | [satellitecomponent/Neurite](https://github.com/satellitecomponent/Neurite) | 2,160 | 168 | 1.66 | 20230405 | 20260316 | MIT | quiet | Fractal Graph-of-Thought. Rhizomatic Mind-Mapping for Ai-Agents, Web-Links, Notes, and Code. |
| 13 | [HKUDS/MiniRAG](https://github.com/HKUDS/MiniRAG) (w) | 2,026 | 258 | 3.08 | 20250111 | 20251016 | MIT | quiet | [ACL2026] "MiniRAG: Making RAG Simpler with Small and Open-Sourced Language Models" |
| 14 | [IntelLabs/fastRAG](https://github.com/IntelLabs/fastRAG) | 1,784 | 166 | 1.3 | 20230123 | 20260112 | Apache-2.0 | archived, quiet | Efficient Retrieval Augmentation and Generation Framework |
| 15 | [minsight-ai-info/AI-Search-Hub](https://github.com/minsight-ai-info/AI-Search-Hub) | 1,307 | 113 | 5.63 | 20260312 | 20260427 | none detected | quiet | One Query. All Search Skill. 聚合 Gemini、Grok、豆包、元宝等平台原生 AI 搜索能力，免费获取科技趋势、行业舆情、热点追踪、旅行规划、日常问题统一接进自己的 Agent 与工作流，指定链接免费爬取 |
| 16 | [codefuse-ai/codefuse-chatbot](https://github.com/codefuse-ai/codefuse-chatbot) | 1,296 | 148 | 1.15 | 20230928 | 20240701 | NOASSERTION | quiet | An intelligent assistant serving the entire software development lifecycle, powered by a Multi-Agent Framework, worki... |
| 17 | [stair-lab/kg-gen](https://github.com/stair-lab/kg-gen) | 1,289 | 201 | 1.77 | 20241030 | 20260324 | none detected | quiet | [NeurIPS '25] Knowledge Graph Generation from Any Text |
| 18 | [TencentCloudADP/youtu-graphrag](https://github.com/TencentCloudADP/youtu-graphrag) (w) | 1,271 | 190 | 3 | 20250901 | 20260226 | NOASSERTION | quiet | [ICLR 2026] Youtu-GraphRAG: Vertically Unified Agents for Graph Retrieval-Augmented Complex Reasoning |
| 19 | [beltromatti/get-it](https://github.com/beltromatti/get-it) | 1,141 | 138 | 6.56 | 20260509 | 20260629 | Apache-2.0 | quiet | Read it. See it. Get it. Built at GDG AI Hack Milan 2026 for "Learn Different" track. |
| 20 | [BaranziniLab/KG_RAG](https://github.com/BaranziniLab/KG_RAG) | 947 | 115 | 0.87 | 20231111 | 20241109 | Apache-2.0 | quiet | Empower Large Language Models (LLM) using Knowledge Graph based Retrieval-Augmented Generation (KG-RAG) for knowledge... |
| 21 | [shibing624/ChatPDF](https://github.com/shibing624/ChatPDF) | 862 | 144 | 0.67 | 20230417 | 20250402 | Apache-2.0 | quiet | RAG for Local LLM, chat with PDF/doc/txt files, ChatPDF. 纯原生实现RAG功能，基于本地LLM、embedding模型、reranker模型实现，支持GraphRAG，无须安装任... |
| 22 | [HKUST-KnowComp/AutoSchemaKG](https://github.com/HKUST-KnowComp/AutoSchemaKG) | 845 | 112 | 1.6 | 20250521 | 20260429 | MIT | quiet | This repository contains the implementation of AutoSchemaKG, a novel framework for automatic knowledge graph construc... |
| 23 | [ImprintLab/Medical-Graph-RAG](https://github.com/ImprintLab/Medical-Graph-RAG) | 839 | 144 | 1.03 | 20240808 | 20251018 | MIT | quiet | A Graph RAG System for Evidenced-based Medical Information Retrieval [ACL 2025] |
| 24 | [cocacola-lab/ChatIE](https://github.com/cocacola-lab/ChatIE) | 826 | 67 | 0.61 | 20230216 | 20240528 | NOASSERTION | quiet | The online version is temporarily unavailable because we cannot afford the key. You can clone and run it locally. Not... |
| 25 | [lyon-industries/graphrag-workbench](https://github.com/lyon-industries/graphrag-workbench) | 742 | 91 | 1.76 | 20250904 | 20260718 | MIT | quiet | Interactive 3D visualization of knowledge graphs generated by Microsoft GraphRAG. Explore entities, relationships, an... |
| 34 | [LHRLAB/Graph-R1](https://github.com/LHRLAB/Graph-R1) (w) | 599 | 76 | 1 | 20250311 | 20260430 | MIT | quiet | [ICML 2026] Official resources of "Graph-R1: Towards Agentic GraphRAG Framework via End-to-end Reinforcement Learning". |
| 35 | [DEEP-PolyU/LinearRAG](https://github.com/DEEP-PolyU/LinearRAG) (w) | 566 | 68 | 1.54 | 20251027 | 20260705 | GPL-3.0 | quiet | [ICLR 2026] LinearRAG: Linear Graph Retrieval Augmented Generation on Large-scale Corpora |
| 60 | [chensyCN/LogicRAG](https://github.com/chensyCN/LogicRAG) (w) | 241 | 37 | 0.42 | 20250407 | 20260719 | GPL-3.0 | quiet | Source code of LogicRAG at AAAI'26. |
| 105 | [datastax/graph-rag](https://github.com/datastax/graph-rag) (w) | 91 | 29 | 0.14 | 20250108 | 20250505 | Apache-2.0 | quiet | Graph traversal for improved RAG |

76 more quiet or archived repositories are in `repos.tsv`.

## agent-memory

Memory layers and temporal knowledge graphs for agents.

### agent-memory: ranked (pushed within 90 days)

| Rank | Repo | Stars | Forks | Stars/day | Created | Last push | Licence | Flags | Description |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | 105,932 | 9,334 | 249.84 | 20250831 | 20261030 | Apache-2.0 | fast-growth | Persistent Context Across Sessions for Every Agent – Captures everything your agent does during sessions, compresses... |
| 2 | [666ghj/MiroFish](https://github.com/666ghj/MiroFish) | 82,864 | 12,533 | 245.16 | 20251126 | 20261016 | AGPL-3.0 | fast-growth | A Simple and Universal Swarm Intelligence Engine, Predicting Anything. 简洁通用的群体智能引擎，预测万物 |
| 3 | [mem0ai/mem0](https://github.com/mem0ai/mem0) (w) | 68,112 | 8,073 | 55.47 | 20230620 | 20261029 | Apache-2.0 | - | The Memory Layer for AI Agents - Drop-in memory infrastructure for AI agents and apps. Context that persists. Built f... |
| 4 | [bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book) | 56,669 | 6,531 | 136.22 | 20250909 | 20261008 | Apache-2.0 | - | 《深入理解 AI Agent：设计原理与工程实践》（李博杰 著）开源主仓库：全书正文、编译版 PDF 与按章配套代码 |
| 5 | [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | 56,608 | 6,810 | 155.09 | 20251030 | 20261030 | MIT | fast-growth | Hindsight: Agent Memory That Learns |
| 6 | [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | 41,196 | 3,343 | 138.24 | 20260105 | 20261030 | AGPL-3.0 | - | Self-evolving Context Database for AI Agents. Unify Agent Memory, Knowledge RAG and Skills. |
| 7 | [pingcap/tidb](https://github.com/pingcap/tidb) | 40,690 | 6,284 | 9.99 | 20150906 | 20261030 | Apache-2.0 | - | TiDB is built for agentic workloads that grow unpredictably, with ACID guarantees and native support for transactions... |
| 8 | [topoteretes/cognee](https://github.com/topoteretes/cognee) (w) | 32,932 | 3,438 | 28.12 | 20230816 | 20261030 | Apache-2.0 | - | Cognee is the open-source AI memory platform for agents. Give your AI agents persistent long-term memory with small m... |
| 9 | [getzep/graphiti](https://github.com/getzep/graphiti) (w) | 32,372 | 3,321 | 39.87 | 20240808 | 20261028 | Apache-2.0 | - | Build Real-Time Knowledge Graphs for AI Agents |
| 10 | [supermemoryai/supermemory](https://github.com/supermemoryai/supermemory) | 31,470 | 2,761 | 32.28 | 20240227 | 20261029 | MIT | - | Memory and context engine + app that is extremely fast, scalable, and can be run fully locally. The Memory API for th... |
| 11 | [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | 30,258 | 2,934 | 146.88 | 20260407 | 20261028 | NOASSERTION | - | TencentDB Agent Memory is a team-level memory hub for AI Agents — turning conversations, docs, and code into four reu... |
| 12 | [letta-ai/letta](https://github.com/letta-ai/letta) (w) | 25,294 | 2,662 | 22.69 | 20231011 | 20261018 | Apache-2.0 | - | Platform for stateful agents: AI with advanced memory that can learn and self-improve over time. |
| 13 | [dolthub/dolt](https://github.com/dolthub/dolt) | 24,776 | 905 | 9.33 | 20190724 | 20261030 | Apache-2.0 | - | Dolt – Git for Data |
| 14 | [screenpipe/screenpipe](https://github.com/screenpipe/screenpipe) | 22,175 | 2,262 | 25.7 | 20240619 | 20261030 | NOASSERTION | - | YC (S26) \| Open Computer History \| Continuously record your company computer work, map your workflows, help you find... |
| 15 | [xerj-org/xerj](https://github.com/xerj-org/xerj) | 17,686 | 1,368 | 144.97 | 20260630 | 20261030 | Apache-2.0 | - | AI search engine and MCP server for bots and agents. One Rust binary indexes code, docs, logs, JSONL/CSV and PDFs for... |
| 16 | [MemoriLabs/Memori](https://github.com/MemoriLabs/Memori) | 17,240 | 3,757 | 37.24 | 20250724 | 20261003 | NOASSERTION | - | Memori is agent-native memory infrastructure. A LLM-agnostic layer that turns agent execution and conversation into s... |
| 17 | [NevaMind-AI/memU](https://github.com/NevaMind-AI/memU) | 14,581 | 1,096 | 31.84 | 20250729 | 20261030 | NOASSERTION | - | Personal memory across agents |
| 18 | [EverMind-AI/EverOS](https://github.com/EverMind-AI/EverOS) | 13,721 | 958 | 37.39 | 20251028 | 20261030 | Apache-2.0 | - | One portable memory layer for every AI agent: local-first, Markdown-native, user-owned, and self-evolving across apps... |
| 19 | [MemTensor/MemOS](https://github.com/MemTensor/MemOS) (w) | 12,199 | 1,098 | 25.36 | 20250706 | 20261029 | Apache-2.0 | - | Self-evolving memory OS for LLM & AI Agents: ultra-persistent memory, hybrid-retrieval, and cross-task skill reuse, w... |
| 20 | [TencentCloud/Octop](https://github.com/TencentCloud/Octop) | 11,365 | 1,503 | 99.69 | 20260708 | 20261028 | MIT | - | A smarter, self-hosted AI assistant — multi-user, multi-agent. |
| 21 | [plastic-labs/honcho](https://github.com/plastic-labs/honcho) | 7,836 | 959 | 6.84 | 20230910 | 20261030 | AGPL-3.0 | - | Memory library for building stateful agents |
| 22 | [julep-ai/julep](https://github.com/julep-ai/julep) | 6,575 | 966 | 7 | 20240404 | 20260806 | Apache-2.0 | - | Julep — durable, composable AI agents. Flows that crash and resume, retry safely, and explain every step. |
| 23 | [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) | 5,060 | 622 | 23 | 20260324 | 20261028 | MIT | - | Persistent memory for Claude Code, Codex and 6 other AI agents, stored as plain markdown in your Obsidian vault. New:... |
| 24 | [ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) | 5,006 | 708 | 23.28 | 20260329 | 20261030 | NOASSERTION | - | Awesome list for AI agent harness engineering: tools, patterns, evals, memory, MCP, permissions, observability, and o... |
| 25 | [CaviraOSS/LongMemory](https://github.com/CaviraOSS/LongMemory) | 4,556 | 513 | 12.12 | 20251019 | 20261018 | Apache-2.0 | - | Local persistent memory store for LLM applications including claude desktop, github copilot, codex, antigravity, etc. |

172 more ranked repositories are in `repos.tsv`.

### agent-memory: quiet or archived

| Rank | Repo | Stars | Forks | Stars/day | Created | Last push | Licence | Flags | Description |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [pashpashpash/vault-ai](https://github.com/pashpashpash/vault-ai) | 3,385 | 291 | 2.62 | 20230418 | 20250708 | MIT | quiet | OP Vault ChatGPT: Give ChatGPT long-term memory using the OP Stack (OpenAI + Pinecone Vector Database). Upload your o... |
| 2 | [memodb-io/memobase](https://github.com/memodb-io/memobase) | 2,942 | 237 | 3.74 | 20240903 | 20260111 | Apache-2.0 | quiet | User Profile-Based Long-Term Memory for AI Chatbot Applications. |
| 3 | [lucidrains/titans-pytorch](https://github.com/lucidrains/titans-pytorch) | 2,000 | 210 | 3.03 | 20250108 | 20260713 | MIT | quiet | Unofficial implementation of Titans, SOTA memory for transformers, in Pytorch |
| 4 | [zhu1090093659/deepseek-pp](https://github.com/zhu1090093659/deepseek-pp) | 1,852 | 294 | 9.96 | 20260427 | 20260813 | Apache-2.0 | archived | DeepSeek Web browser extension: AI agent workspace with MCP tools, memory, Skills, automation, web search, and conver... |
| 5 | [BAI-LAB/MemoryOS](https://github.com/BAI-LAB/MemoryOS) | 1,615 | 168 | 3.12 | 20250530 | 20260707 | Apache-2.0 | quiet | [EMNLP 2025 Oral] MemoryOS is designed to provide a memory operating system for personalized AI agents. |
| 6 | [agiresearch/A-mem](https://github.com/agiresearch/A-mem) (w) | 1,212 | 123 | 1.98 | 20250225 | 20251212 | MIT | quiet | A-MEM: Agentic Memory for LLM Agents |
| 7 | [shaneholloman/mcp-knowledge-graph](https://github.com/shaneholloman/mcp-knowledge-graph) | 886 | 102 | 1.29 | 20241209 | 20260529 | MIT | quiet | MCP server enabling persistent memory for Claude through a local knowledge graph - fork focused on local development |
| 8 | [Victorwz/LongMem](https://github.com/Victorwz/LongMem) | 829 | 73 | 0.67 | 20230612 | 20240330 | Apache-2.0 | quiet | Official implementation of our NeurIPS 2023 paper "Augmenting Language Models with Long-Term Memory". |
| 9 | [alash3al/stash](https://github.com/alash3al/stash) | 770 | 46 | 4.1 | 20260424 | 20260614 | Apache-2.0 | quiet | Stash — persistent memory layer for AI agents. Episodes, facts, and working context stored in Postgres. MCP server in... |
| 10 | [swarmclawai/swarmclaw](https://github.com/swarmclawai/swarmclaw) | 703 | 145 | 2.78 | 20260218 | 20260630 | MIT | quiet | Open-source self-hosted AI agent runtime and multi-agent framework for autonomous agent swarms. Agent memory, MCP too... |
| 11 | [jmerelnyc/Photo-agents](https://github.com/jmerelnyc/Photo-agents) | 665 | 22 | 3.72 | 20260504 | 20260703 | MIT | quiet | Autonomous self-evolving agents. Vision-grounded layered memory and self-written skills for LLM agents that operate y... |
| 12 | [Arvincreator/project-golem](https://github.com/Arvincreator/project-golem) | 641 | 104 | 2.35 | 20260130 | 20260622 | NOASSERTION | quiet | OS-level autonomous AI agent with long-term memory, multi-agent coordination, Titan Chronos scheduler & Moltbot Socia... |
| 13 | [memvid/claude-brain](https://github.com/memvid/claude-brain) | 581 | 60 | 1.84 | 20251218 | 20260119 | MIT | quiet | Give Claude Code photographic memory in ONE portable file. No database, no SQLite, no ChromaDB - just a single .mv2 f... |
| 14 | [NeoLi00/memX](https://github.com/NeoLi00/memX) | 403 | 3 | 2.3 | 20260508 | 20260526 | MIT | quiet | memX: self-learning, self-maintaining memory plugin for AI agents; native support for claude code, codex, and openclaw |
| 15 | [DEEP-PolyU/Awesome-GraphMemory](https://github.com/DEEP-PolyU/Awesome-GraphMemory) | 363 | 28 | 1.13 | 20251214 | 20260606 | none detected | quiet | A survey of Graph-based Agent Memory \| A curated list of resources (surveys, papers, benchmarks, and opensource proje... |
| 16 | [libraryofcelsus/Aetherius_AI_Assistant](https://github.com/libraryofcelsus/Aetherius_AI_Assistant) | 312 | 39 | 0.24 | 20230403 | 20240906 | NOASSERTION | quiet | A completely private, locally-operated Ai Assistant/Chatbot/Sub-Agent Framework with realistic Long Term Memory and t... |
| 17 | [TIMAN-group/PlugMem](https://github.com/TIMAN-group/PlugMem) | 306 | 31 | 1.17 | 20260209 | 20260709 | Apache-2.0 | quiet | ICML 2026 \| PALM@NeurIPS2026 Oral \| Plug-and-play long-term memory for LLM agents |
| 18 | [HezaoHezao/poirot](https://github.com/HezaoHezao/poirot) | 258 | 27 | 2.74 | 20260728 | 20260728 | MIT | quiet | Poirot is a deep research agent kernel built for those who care about how agents are architected. |
| 19 | [LearnPrompt/cc-harness-skills](https://github.com/LearnPrompt/cc-harness-skills) | 240 | 63 | 1.13 | 20260401 | 20260710 | MIT | quiet | Portable CC-inspired skills for memory, verification, multi-agent coordination, context compression, and proactive co... |
| 20 | [XortexAI/XMem](https://github.com/XortexAI/XMem) | 234 | 54 | 0.9 | 20260212 | 20260603 | BSD-3-Clause | archived, quiet | Xmem is a India's First open source multi-modal, multi-agentic long‑term memory layer for AI agents. |
| 21 | [graniet/kheish](https://github.com/graniet/kheish) | 217 | 18 | 0.32 | 20241211 | 20260726 | Apache-2.0 | quiet | Orchestration engine for long-running, tool-using AI agents |
| 22 | [nemori-ai/nemori](https://github.com/nemori-ai/nemori) | 217 | 23 | 0.45 | 20250630 | 20260416 | MIT | quiet | A minimalist MVP demonstrating a simple yet profound insight: aligning AI memory with human episodic memory granulari... |
| 23 | [kevin-hs-sohn/hipocampus](https://github.com/kevin-hs-sohn/hipocampus) | 211 | 12 | 0.92 | 20260315 | 20260608 | MIT | quiet | Drop-in memory harness for AI agents — 3-tier memory, compaction tree, hybrid search. One command to set up. Works wi... |
| 24 | [edwin-hao-ai/Awareness-Local](https://github.com/edwin-hao-ai/Awareness-Local) | 199 | 4 | 0.9 | 20260322 | 20260504 | MIT | quiet | Local-first AI agent memory — one command, works offline, no account needed. Give your Claude Code, Cursor, Windsurf,... |
| 25 | [Intina47/context-sync](https://github.com/Intina47/context-sync) | 190 | 19 | 0.5 | 20251016 | 20260411 | MIT | quiet | Local persistent memory store for LLM applications including continue.dev, cursor, claude desktop, github copilot, co... |

20 more quiet or archived repositories are in `repos.tsv`.

## markdown-kb

Markdown-native and 'LLM wiki' knowledge bases, Obsidian-style second brains for agents.

### markdown-kb: ranked (pushed within 90 days)

| Rank | Repo | Stars | Forks | Stars/day | Created | Last push | Licence | Flags | Description |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki) | 21,197 | 2,404 | 103.4 | 20260408 | 20261021 | NOASSERTION | - | LLM Wiki is a cross-platform desktop application that turns your documents into an organized, interlinked knowledge b... |
| 2 | [AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) | 16,002 | 1,579 | 77.68 | 20260407 | 20261025 | MIT | - | Self-organizing AI second brain for Obsidian + Claude Code. Drop any source and Claude reads, links, and files it int... |
| 3 | [breferrari/obsidian-mind](https://github.com/breferrari/obsidian-mind) | 5,460 | 611 | 22.47 | 20260228 | 20261017 | MIT | - | A self-organizing Obsidian vault that gives AI coding agents persistent memory. |
| 4 | [inkeep/open-knowledge](https://github.com/inkeep/open-knowledge) | 4,741 | 327 | 31.82 | 20260603 | 20261030 | GPL-3.0 | - | Beautiful, AI-native markdown IDE and LLM wiki |
| 5 | [basicmachines-co/basic-memory](https://github.com/basicmachines-co/basic-memory) (w) | 4,416 | 343 | 6.34 | 20241202 | 20261030 | AGPL-3.0 | - | AI conversations that actually remember. Never re-explain your project to your AI again. Join our Discord: https://di... |
| 6 | [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) (w) | 3,667 | 426 | 2.85 | 20230421 | 20261026 | MIT | - | A personal knowledge base that builds and maintains itself. Drop in sources — Claude (or Codex/Gemini) reads them, ex... |
| 7 | [Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki) (w) | 3,640 | 366 | 17.58 | 20260406 | 20261027 | MIT | - | Framework for AI agents to build and maintain a digital brain through Obsidian wiki \| Memory System for Agents |
| 8 | [atomicstrata/llm-wiki-compiler](https://github.com/atomicstrata/llm-wiki-compiler) | 2,225 | 237 | 10.75 | 20260405 | 20261019 | MIT | - | The knowledge compiler. Raw sources in, interlinked wiki out. Inspired by Karpathy's LLM Wiki pattern. |
| 9 | [nhaouari/obsidian-textgenerator-plugin](https://github.com/nhaouari/obsidian-textgenerator-plugin) | 1,995 | 175 | 1.17 | 20220227 | 20260806 | MIT | - | Text Generator is a versatile plugin for Obsidian that allows you to generate text content using various AI providers... |
| 10 | [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki) | 1,734 | 244 | 8.3 | 20260404 | 20261029 | Apache-2.0 | - | Open Source Implementation of Karpathy's LLM Wiki. Upload documents, connect your Claude account via MCP, and have it... |
| 11 | [PKU-DAIR/AutoSci](https://github.com/PKU-DAIR/AutoSci) | 1,715 | 215 | 8.41 | 20260409 | 20261030 | MIT | - | Karpathy's LLM-Wiki vision, fully realized — wiki-centric full-lifecycle AI research platform powered by Claude Code |
| 12 | [yuezhiai/jonex](https://github.com/yuezhiai/jonex) | 1,522 | 277 | 14.78 | 20260719 | 20261028 | NOASSERTION | - | All-in-One Multimodal Parsing Engine + Ontology-Powered, LLM Wiki-Driven AI-Ready Knowledge Engine |
| 13 | [nvk/llm-wiki](https://github.com/nvk/llm-wiki) | 1,486 | 143 | 7.14 | 20260404 | 20261025 | MIT | - | LLM-compiled knowledge bases for any AI agent. Parallel multi-agent research, thesis-driven investigation, source ing... |
| 14 | [s2b-dev/smart-second-brain](https://github.com/s2b-dev/smart-second-brain) | 1,333 | 119 | 1.19 | 20231002 | 20261013 | MIT | - | A free, open-source Obsidian plugin that makes your vault smarter: better search, an interactive knowledge graph, and... |
| 15 | [huytieu/COG-second-brain](https://github.com/huytieu/COG-second-brain) | 1,329 | 162 | 3.5 | 20251015 | 20261023 | MIT | - | Self-evolving second brain with 35 AI skills, 10 agents, and people CRM. Closed-loop harness: a V-model verification... |
| 16 | [chubbyguan/chubbyskills](https://github.com/chubbyguan/chubbyskills) | 1,289 | 153 | 8.95 | 20260608 | 20261014 | MIT | - | 把中文全渠道内容（抖音 / B站 / 小红书 / 公众号 / X / 播客）采集进个人知识库的 14 个 AI Skill：图文存图、视频转文字稿、字幕优先免 GPU、RSS/YouTube 订阅调度与每日情报简报，附带知识库 MCP... |
| 17 | [thClaws/thClaws](https://github.com/thClaws/thClaws) | 1,244 | 185 | 6.45 | 20260420 | 20261029 | Apache-2.0 | - | Open-source AI agent harness in native Rust — GUI, CLI, headless, and webapp from one binary. Multi-provider, MCP, sk... |
| 18 | [mateaix/mateclaw](https://github.com/mateaix/mateclaw) | 1,174 | 356 | 5.62 | 20260404 | 20261030 | Apache-2.0 | - | 🤖 MateClaw — Your second brain with Multi-Agent Orchestration, MCP Protocol, Skills & Memory, Dream, and Multi-Channe... |
| 19 | [undefined-ui/second-brain-os](https://github.com/undefined-ui/second-brain-os) | 1,167 | 193 | 22.02 | 20260907 | 20261014 | MIT | - | An AI second brain that maintains itself. Full guide, starter vault, agent skills and scripts for a self-organizing k... |
| 20 | [agents-flex/agents-flex](https://github.com/agents-flex/agents-flex) | 1,044 | 156 | 1.02 | 20240112 | 20261030 | Apache-2.0 | - | Agents-flex is A lightweight Java AI agent development framework (positioned as a counterpart to Spring AI). It suppo... |
| 21 | [Robinson-AI-Lab/FridayOS1.0](https://github.com/Robinson-AI-Lab/FridayOS1.0) | 880 | 85 | 6.15 | 20260609 | 20261030 | MIT | - | Local-first AI second brain & personal knowledge management: Six-Brain Markdown blueprint, Obsidian example vault, of... |
| 22 | [kiwifs/kiwifs](https://github.com/kiwifs/kiwifs) | 870 | 281 | 4.55 | 20260422 | 20261028 | NOASSERTION | - | Markdown filesystem for agents and teams. |
| 23 | [Railly/agentfiles](https://github.com/Railly/agentfiles) | 861 | 68 | 3.99 | 20260328 | 20260831 | MIT | - | Browse, create, and edit AI agent files across Claude Code, Cursor, Codex, and 12 coding tools — from Obsidian. |
| 24 | [GD4AI/obsidian-llm-wiki](https://github.com/GD4AI/obsidian-llm-wiki) | 753 | 92 | 4.03 | 20260426 | 20261030 | Apache-2.0 | - | Karpathy's LLM Wiki implementation plugin for Obsidian - turns notes and PDFs into a linked, LLM-powered knowledge ba... |
| 25 | [agarwalvishal/claude-chat-exporter](https://github.com/agarwalvishal/claude-chat-exporter) | 736 | 84 | 0.87 | 20240710 | 20261023 | MIT | - | One-click, privacy-first exporter for Claude.ai chats — clean Markdown with artifacts and attachments, ready for Obsi... |

38 more ranked repositories are in `repos.tsv`.

### markdown-kb: quiet or archived

| Rank | Repo | Stars | Forks | Stars/day | Created | Last push | Licence | Flags | Description |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [VectifyAI/OpenKB](https://github.com/VectifyAI/OpenKB) (w) | 4,831 | 503 | 23.11 | 20260404 | 20260722 | Apache-2.0 | quiet | OpenKB: Open LLM Knowledge Base |
| 2 | [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki) (w) | 2,643 | 310 | 12.71 | 20260405 | 20260723 | MIT | quiet | Agent Skills-compatible LLM wiki for Claude Code, Cursor, and Codex. Build a Karpathy-style knowledge base from raw s... |
| 3 | [sdyckjq-lab/llm-wiki-skill](https://github.com/sdyckjq-lab/llm-wiki-skill) | 2,573 | 301 | 12.37 | 20260405 | 20260727 | none detected | quiet | 基于 Karpathy llm-wiki 方法论的个人知识库构建 Skill，支持多平台！ |
| 4 | [ballred/obsidian-claude-pkm](https://github.com/ballred/obsidian-claude-pkm) | 1,886 | 125 | 4.21 | 20250807 | 20260218 | MIT | quiet | A complete starter kit for an Obsidian + Claude Code personal knowledge management system. |
| 5 | [tuan3w/obsidian-template](https://github.com/tuan3w/obsidian-template) | 1,138 | 150 | 0.6 | 20210829 | 20260321 | MIT | quiet | Starter templates for Obsidian |
| 6 | [kytmanov/obsidian-llm-wiki-local](https://github.com/kytmanov/obsidian-llm-wiki-local) | 845 | 126 | 4.1 | 20260407 | 20260526 | MIT | quiet | Karpathy’s LLM Wiki, 100% local with Ollama. Drop Markdown notes → AI extracts concepts → your Obsidian wiki auto-lin... |
| 7 | [NicholasSpisak/second-brain](https://github.com/NicholasSpisak/second-brain) | 765 | 114 | 3.7 | 20260406 | 20260407 | none detected | quiet | LLM-maintained personal knowledge base for Obsidian. Based on Andrej Karpathy's LLM Wiki pattern. |
| 8 | [jason-effi-lab/karpathy-llm-wiki-vault](https://github.com/jason-effi-lab/karpathy-llm-wiki-vault) | 735 | 227 | 3.67 | 20260413 | 20260413 | none detected | quiet | 基于 Karpathy LLM Wiki 理念构建的 SKILL 和 Obsidian 知识库，将碎片信息整理为结构化、互联的知识网络。 |
| 9 | [swarmclawai/swarmvault](https://github.com/swarmclawai/swarmvault) | 732 | 87 | 3.55 | 20260406 | 20260630 | MIT | quiet | The local-first LLM Wiki: open-source knowledge graph builder, RAG knowledge base, and agent memory store. Built on A... |
| 10 | [lewislulu/llm-wiki-skill](https://github.com/lewislulu/llm-wiki-skill) | 655 | 104 | 3.15 | 20260405 | 20260416 | none detected | quiet | Karpathy-style LLM knowledge base Agent Skill for OpenClaw/Codex. Experimental — will iterate over time. |
| 11 | [cclank/Hermes-Wiki](https://github.com/cclank/Hermes-Wiki) | 654 | 72 | 3.19 | 20260408 | 20260621 | none detected | quiet | Hermes agent + LLM Wiki + 源代码 完成 Hermes agent wiki |
| 12 | [iBlinkQ/llm-wiki-obsidian-blink](https://github.com/iBlinkQ/llm-wiki-obsidian-blink) | 648 | 109 | 3.19 | 20260410 | 20260413 | none detected | quiet | 一个基于 Andrej Karpathy 的 LLM Wiki 模式 实现的 Obsidian 知识库，利用 LLM 维护可复利的个人知识层。 |
| 13 | [Gremble-io/Detto](https://github.com/Gremble-io/Detto) | 521 | 24 | 2.37 | 20260324 | 20260722 | NOASSERTION | quiet | On-device meeting capture, dictation, and vault-native knowledge layer for macOS. Nothing leaves your Mac. |
| 14 | [nicksp/dotfiles](https://github.com/nicksp/dotfiles) | 473 | 101 | 0.12 | 20160320 | 20260609 | MIT | quiet | My personal dotfiles: Zsh, Git, VSCode, Obsidian, Ghostty, cmux, etc. |
| 15 | [Pratiyush/llm-wiki](https://github.com/Pratiyush/llm-wiki) | 400 | 57 | 1.95 | 20260408 | 20260618 | MIT | quiet | LLM-powered knowledge base from your Claude Code, Codex CLI, Copilot, Cursor & Gemini sessions. Karpathy's LLM Wiki p... |
| 16 | [runesleo/ai-health-vault](https://github.com/runesleo/ai-health-vault) | 351 | 82 | 1.6 | 20260325 | 20260427 | MIT | quiet | AI + Obsidian private health management system template |
| 17 | [gatelynch/llm-knowledge-base](https://github.com/gatelynch/llm-knowledge-base) | 341 | 90 | 1.64 | 20260405 | 20260406 | MIT | quiet | 參考自Andrej Kapathy的llm-wiki概念，把原始素材、LLM 編譯後的知識、 探索中的思考，以及最終作品明確分層管理 的個人知識庫系統。 |
| 18 | [Lyra-stellAI/BYO-LLM-WIKI](https://github.com/Lyra-stellAI/BYO-LLM-WIKI) | 280 | 4 | 1.71 | 20260518 | 20260729 | none detected | quiet | Build your own LLM-native WIKI (knowledge library). Search, extract, summarize, Q&A with contextual RAG, layered know... |
| 19 | [Ansub/wiki-os](https://github.com/Ansub/wiki-os) | 270 | 30 | 1.34 | 20260412 | 20260417 | MIT | quiet | UI Layer for Karpathy's LLM Wiki |
| 20 | [tonbistudio/llm-wiki](https://github.com/tonbistudio/llm-wiki) | 266 | 78 | 1.3 | 20260408 | 20260619 | MIT | quiet | Open-source template for building LLM-powered knowledge bases following Karpathy's LLM Wiki pattern |
| 21 | [luotwo/llm-wiki](https://github.com/luotwo/llm-wiki) | 228 | 39 | 1.1 | 20260405 | 20260626 | none detected | quiet | LLM Wiki - 用 LLM 构建持续积累的个人知识库，含 Claude Code Skill 和实战经验 |
| 22 | [mduongvandinh/llm-wiki](https://github.com/mduongvandinh/llm-wiki) | 221 | 95 | 1.07 | 20260407 | 20260416 | MIT | quiet | Hệ thống knowledge base cá nhân hoàn toàn tự động, vận hành bởi LLM. Dựa trên pattern LLM Wiki của Andrej Karpathy. |
| 23 | [balukosuri/llm-wiki-karpathy](https://github.com/balukosuri/llm-wiki-karpathy) | 220 | 85 | 1.07 | 20260407 | 20260407 | none detected | quiet | - |
| 24 | [Michael-OvO/obsidian-knowledge-agent](https://github.com/Michael-OvO/obsidian-knowledge-agent) | 206 | 13 | 1.36 | 20260531 | 20260627 | MIT | quiet | Agent-driven pipeline that turns raw material (PDFs, slides, syllabi, papers, URLs) into structured, teaching-quality... |
| 25 | [kfchou/wiki-skills](https://github.com/kfchou/wiki-skills) | 188 | 29 | 0.9 | 20260405 | 20260703 | MIT | quiet | LLM-maintained personal wiki skills for Claude Code — implements Karpathy's LLM Wiki pattern |

18 more quiet or archived repositories are in `repos.tsv`.

## adjacent

Code knowledge graphs, graph databases, RAG platforms.

### adjacent: ranked (pushed within 90 days)

| Rank | Repo | Stars | Forks | Stars/day | Created | Last push | Licence | Flags | Description |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [langgenius/dify](https://github.com/langgenius/dify) (w) | 160,019 | 25,286 | 123.38 | 20230412 | 20261030 | NOASSERTION | - | Build Agentic workflows, RAG pipelines, with rich AI model and tool support on one collaborative workspace. Deploy on... |
| 2 | [open-webui/open-webui](https://github.com/open-webui/open-webui) | 157,264 | 22,880 | 140.54 | 20231006 | 20261030 | NOASSERTION | - | User-friendly AI Interface (Supports Ollama, OpenAI API, ...) |
| 3 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 148,720 | 24,989 | 100.9 | 20221017 | 20261030 | MIT | - | The agent engineering platform. |
| 4 | [infiniflow/ragflow](https://github.com/infiniflow/ragflow) (w) | 93,206 | 11,183 | 88.51 | 20231212 | 20261030 | Apache-2.0 | - | RAGFlow is a leading open-source Retrieval-Augmented Generation (RAG) engine that fuses cutting-edge RAG with Agent c... |
| 5 | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) (w) | 91,699 | 11,892 | 129.15 | 20241119 | 20261029 | NOASSERTION | - | Model Context Protocol Servers |
| 6 | [Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) | 89,043 | 7,545 | 388.83 | 20260315 | 20261026 | MIT | fast-growth | Graphs that teach &gt; graphs that impress. Turn any code into an interactive knowledge graph you can explore, search, a... |
| 7 | [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) | 86,602 | 9,013 | 95.8 | 20240509 | 20261030 | Apache-2.0 | - | Open-source web crawler and scraper for LLMs and AI agents: any website into clean, LLM-ready Markdown. Run it yourse... |
| 8 | [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) | 85,424 | 10,624 | 204.36 | 20250907 | 20261013 | NOASSERTION | fast-growth | 📚 《从零开始构建智能体》——从零开始的智能体原理与实践教程 |
| 9 | [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) | 78,365 | 6,108 | 265.64 | 20260107 | 20261030 | Apache-2.0 | fast-growth | Compress tool outputs, logs, files, and RAG chunks before they reach the LLM. 20% fewer tokens for coding agents, 60-... |
| 10 | [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) | 75,999 | 5,025 | 267.6 | 20260118 | 20261030 | MIT | fast-growth | Pre-indexed code knowledge graph, auto syncs on code changes, for Claude Code, Codex, Gemini, Cursor, OpenCode, AntiG... |
| 11 | [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) (w) | 67,758 | 7,626 | 54.47 | 20230604 | 20261030 | MIT | - | Stop renting your intelligence. Own it with AnythingLLM. Everything you need for a powerful local-first agent experience |
| 12 | [pathwaycom/serviette](https://github.com/pathwaycom/serviette) | 58,751 | 1,537 | 49 | 20230719 | 20261016 | MIT | low-forks | A no-code RAG server that keeps answers in sync with your documents. Works with 8 vector databases. Built on Pathway. |
| 13 | [run-llama/llama_index](https://github.com/run-llama/llama_index) (w) | 52,746 | 8,480 | 36.18 | 20221102 | 20261026 | MIT | - | LlamaIndex is the document processing platform for AI |
| 14 | [jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot) | 48,346 | 16,221 | 16.7 | 20181126 | 20261028 | Apache-2.0 | - | 【低代码v2.0，一句话即可生成整个系统】企业级AI低代码平台，一键生成前后端代码甚至整个系统。 AI Skills 一句话画流程、设计表单、生成报表、大屏。内置 AI应用平台涵盖：AI聊天、知识库、流程编排、MCP插件等，兼容主流大... |
| 15 | [milvus-io/milvus](https://github.com/milvus-io/milvus) | 46,536 | 4,321 | 17.89 | 20190916 | 20261030 | Apache-2.0 | - | Milvus is a high-performance, cloud-native vector database built for scalable vector ANN search |
| 16 | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 44,173 | 7,602 | 37.5 | 20230809 | 20261030 | MIT | - | Build resilient agents. |
| 17 | [VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex) | 39,913 | 3,435 | 69.17 | 20250401 | 20261029 | MIT | - | 📑 PageIndex: Document Index for Vectorless, Reasoning-based RAG |
| 18 | [The-Vibe-Company/quivr](https://github.com/The-Vibe-Company/quivr) | 39,616 | 3,732 | 31.29 | 20230512 | 20261030 | MIT | - | An open-source engine that turns continuous content streams into search and monitoring. Durable ingestion, hybrid sea... |
| 19 | [khoj-ai/khoj](https://github.com/khoj-ai/khoj) (w) | 37,906 | 2,529 | 19.94 | 20210816 | 20260802 | AGPL-3.0 | - | Your AI second brain. Self-hostable. Get answers from the web or your docs. Build custom agents, schedule automations... |
| 20 | [ItzCrazyKns/Vane](https://github.com/ItzCrazyKns/Vane) | 37,860 | 4,213 | 40.54 | 20240409 | 20260901 | MIT | - | Vane is an AI-powered answering engine. |
| 21 | [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) | 36,578 | 3,877 | 200.98 | 20260501 | 20261028 | MIT | fast-growth | Turn any technical book PDF into a Claude Code skill — ready to study, reference, and use while you work. |
| 22 | [Tencent/WeKnora](https://github.com/Tencent/WeKnora) | 36,051 | 4,900 | 77.53 | 20250722 | 20261030 | NOASSERTION | - | Open-source LLM knowledge platform: turn raw documents into a queryable RAG, an autonomous reasoning agent, and a sel... |
| 23 | [datawhalechina/happy-llm](https://github.com/datawhalechina/happy-llm) | 34,659 | 3,275 | 39.16 | 20240528 | 20260808 | NOASSERTION | - | 📚 从零开始构建大模型 |
| 24 | [surrealdb/surrealdb](https://github.com/surrealdb/surrealdb) | 33,252 | 1,397 | 18.62 | 20211209 | 20261029 | NOASSERTION | - | A scalable, distributed, collaborative, document-graph database, for the realtime web |
| 25 | [onyx-dot-app/onyx](https://github.com/onyx-dot-app/onyx) | 33,105 | 4,679 | 25.82 | 20230427 | 20261030 | NOASSERTION | - | Open Source AI Platform - AI Chat with advanced features that works with every LLM |
| 29 | [deepset-ai/haystack](https://github.com/deepset-ai/haystack) (w) | 26,886 | 3,368 | 10.58 | 20191114 | 20261030 | Apache-2.0 | - | Open-source AI orchestration framework for building context-engineered, production-ready LLM applications. Design mod... |
| 66 | [vitali87/code-graph-rag](https://github.com/vitali87/code-graph-rag) (w) | 5,303 | 708 | 10.58 | 20250616 | 20261030 | MIT | - | The ultimate RAG for your monorepo. Query, understand, and edit multi-language codebases with the power of AI and kno... |

128 more ranked repositories are in `repos.tsv`.

### adjacent: quiet or archived

| Rank | Repo | Stars | Forks | Stars/day | Created | Last push | Licence | Flags | Description |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [chatchat-space/Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) | 38,715 | 6,255 | 29.58 | 20230331 | 20251110 | Apache-2.0 | quiet | Langchain-Chatchat（原Langchain-ChatGLM）基于 Langchain 与 ChatGLM, Qwen 与 Llama 等语言模型的 RAG 与 Agent 应用 \| Langchain-Chatchat... |
| 2 | [stanford-oval/storm](https://github.com/stanford-oval/storm) (w) | 31,753 | 2,997 | 33.42 | 20240324 | 20250930 | MIT | quiet | An LLM-powered knowledge curation system that researches a topic and generates a full-length report with citations. |
| 3 | [Cinnamon/kotaemon](https://github.com/Cinnamon/kotaemon) (w) | 25,840 | 2,167 | 27.23 | 20240325 | 20260714 | Apache-2.0 | quiet | An open-source RAG-based tool for chatting with your documents. |
| 4 | [vanna-ai/vanna](https://github.com/vanna-ai/vanna) | 23,802 | 2,549 | 18.8 | 20230513 | 20260202 | MIT | archived, quiet | 🤖 Chat with your SQL database 📊. Accurate Text-to-SQL Generation via LLMs using Agentic Retrieval 🔄. |
| 5 | [ConardLi/easy-dataset](https://github.com/ConardLi/easy-dataset) | 15,059 | 1,539 | 24.89 | 20250304 | 20260501 | NOASSERTION | quiet | A powerful tool for creating datasets for LLM fine-tuning 、RAG and Eval |
| 6 | [sigoden/aichat](https://github.com/sigoden/aichat) | 10,534 | 745 | 7.88 | 20230303 | 20260223 | Apache-2.0 | quiet | All-in-one LLM CLI tool featuring Shell Assistant, Chat-REPL, RAG, AI Tools & Agents, with access to OpenAI, Claude,... |
| 7 | [activeloopai/deeplake](https://github.com/activeloopai/deeplake) | 9,263 | 724 | 3.51 | 20190809 | 20260521 | Apache-2.0 | quiet | Deeplake is AI Data Runtime for Agents. It provides serverless postgres with a multimodal datalake, enabling scalable... |
| 8 | [SciPhi-AI/R2R](https://github.com/SciPhi-AI/R2R) (w) | 8,051 | 650 | 8.12 | 20240212 | 20251107 | MIT | quiet | SoTA production-ready AI retrieval system. Agentic Retrieval-Augmented Generation (RAG) with a RESTful API. |
| 9 | [postgresml/postgresml](https://github.com/postgresml/postgresml) | 6,826 | 364 | 4.1 | 20220411 | 20250701 | MIT | quiet | Postgres with GPUs for ML/AI apps. |
| 10 | [airweave-ai/airweave](https://github.com/airweave-ai/airweave) | 6,548 | 819 | 9.7 | 20241224 | 20260605 | MIT | archived, quiet | Open-source context retrieval layer for AI agents |
| 11 | [run-llama/rags](https://github.com/run-llama/rags) | 6,547 | 654 | 6.07 | 20231116 | 20240405 | MIT | quiet | Build ChatGPT over your data, all with natural language |
| 12 | [lavague-ai/LaVague](https://github.com/lavague-ai/LaVague) | 6,393 | 574 | 6.55 | 20240226 | 20250121 | Apache-2.0 | quiet | Large Action Model framework to develop AI Web Agents |
| 13 | [ashishps1/learn-ai-engineering](https://github.com/ashishps1/learn-ai-engineering) | 6,162 | 1,460 | 10.87 | 20250411 | 20260205 | GPL-3.0 | quiet | Learn AI and LLMs from scratch using free resources |
| 14 | [PySpur-Dev/pyspur](https://github.com/PySpur-Dev/pyspur) | 5,797 | 425 | 7.56 | 20240923 | 20260629 | Apache-2.0 | quiet | A visual playground for agentic workflows: Iterate over your agents 10x faster |
| 15 | [timescale/pgai](https://github.com/timescale/pgai) | 5,795 | 318 | 6.46 | 20240516 | 20260527 | PostgreSQL | archived, quiet | A suite of tools to develop RAG, semantic search, and other AI applications more easily with PostgreSQL |
| 16 | [PacktPublishing/LLM-Engineers-Handbook](https://github.com/PacktPublishing/LLM-Engineers-Handbook) | 5,408 | 1,326 | 5.79 | 20240409 | 20260422 | MIT | quiet | The LLM's practical guide: From the fundamentals to deploying advanced LLM and RAG apps to AWS using LLMOps best prac... |
| 17 | [TaskingAI/TaskingAI](https://github.com/TaskingAI/TaskingAI) | 5,408 | 357 | 5.27 | 20240108 | 20241202 | Apache-2.0 | quiet | The open source platform for AI-native application development. |
| 18 | [truefoundry/cognita](https://github.com/truefoundry/cognita) | 4,408 | 393 | 3.7 | 20230726 | 20260313 | Apache-2.0 | archived, quiet | RAG (Retrieval Augmented Generation) Framework for building modular, open source applications for production by TrueF... |
| 19 | [cozodb/cozo](https://github.com/cozodb/cozo) | 4,137 | 169 | 2.8 | 20221014 | 20241204 | MPL-2.0 | quiet | A transactional, relational-graph-vector database that uses Datalog for query. The hippocampus for AI! |
| 20 | [kuzudb/kuzu](https://github.com/kuzudb/kuzu) (w) | 4,018 | 532 | 1.81 | 20200926 | 20251010 | MIT | archived, quiet | Embedded property graph database built for speed. Vector search and full-text search built in. Implements Cypher. |
| 21 | [PeterH0323/Streamer-Sales](https://github.com/PeterH0323/Streamer-Sales) | 3,796 | 575 | 4.05 | 20240405 | 20250308 | AGPL-3.0 | quiet | Streamer-Sales 销冠 —— 卖货主播 LLM 大模型🛒🎁，一个能够根据给定的商品特点从激发用户购买意愿角度出发进行商品解说的卖货主播大模型。🚀⭐内含详细的数据生成流程❗ 📦另外还集成了 LMDeploy 加速推理🚀、RA... |
| 22 | [Dataherald/dataherald](https://github.com/Dataherald/dataherald) | 3,650 | 264 | 2.97 | 20230620 | 20240724 | Apache-2.0 | quiet | Interact with your SQL database, Natural Language to SQL using LLMs |
| 23 | [Meirtz/Awesome-Context-Engineering](https://github.com/Meirtz/Awesome-Context-Engineering) | 3,332 | 290 | 6.87 | 20250702 | 20260528 | MIT | quiet | 🔥 Comprehensive survey on Context Engineering: from prompt engineering to production-grade AI systems. hundreds of pa... |
| 24 | [jm199504/Financial-Knowledge-Graphs](https://github.com/jm199504/Financial-Knowledge-Graphs) | 3,132 | 566 | 1.17 | 20190627 | 20240707 | none detected | quiet | 小型金融知识图谱构建流程（neo4j / python / cypher / KG） |
| 25 | [decodingai-magazine/second-brain-ai-assistant-course](https://github.com/decodingai-magazine/second-brain-ai-assistant-course) | 3,131 | 528 | 4.68 | 20241230 | 20260406 | MIT | quiet | Learn to build your Second Brain AI assistant with LLMs, agents, RAG, fine-tuning, LLMOps and AI systems techniques. |

161 more quiet or archived repositories are in `repos.tsv`.

## Releases, recent commits and contributors

For the top 25 ranked repositories per category and every watchlist repository. Commits are on the default branch in the last 90 days, capped at 100.

| Category | Repo | Latest release | Commits (90 d) | Contributors |
|---|---|---|---|---|
| core | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | v0.9.97 (20261027) | 100+ | 374 |
| core | [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) (w) | v1.5.7 (20260902) | 100+ | 353 |
| core | [microsoft/graphrag](https://github.com/microsoft/graphrag) (w) | v3.3.0 (20261008) | 20 | 51 |
| core | [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph) | v2.3.9 (20260918) | 100+ | 143 |
| core | [HKUDS/RAG-Anything](https://github.com/HKUDS/RAG-Anything) (w) | v1.4.4 (20261028) | 100+ | 77 |
| core | [semantica-agi/semantica](https://github.com/semantica-agi/semantica) | v0.7.0 (20260922) | 100+ | 143 |
| core | [vesoft-inc/nebula](https://github.com/vesoft-inc/nebula) | v3.8.0 (20240517) | 2 | 120 |
| core | [cocoindex-io/cocoindex](https://github.com/cocoindex-io/cocoindex) | v1.0.26 (20261022) | 100+ | 100 |
| core | [adongwanai/AgentGuide](https://github.com/adongwanai/AgentGuide) | none | 27 | 6 |
| core | [trailhq/Trail-Code](https://github.com/trailhq/Trail-Code) | none | 100+ | 47 |
| core | [FalkorDB/FalkorDB](https://github.com/FalkorDB/FalkorDB) | v6.0.3 (20261022) | 100+ | 82 |
| core | [deeplethe/utopia](https://github.com/deeplethe/utopia) | none | 100+ | 31 |
| core | [xerrors/Yuxi](https://github.com/xerrors/Yuxi) | v0.7.2 (20260902) | 100+ | 63 |
| core | [potpie-ai/potpie](https://github.com/potpie-ai/potpie) | v2.0.1 (20260831) | 42 | 45 |
| core | [neo4j-labs/llm-graph-builder](https://github.com/neo4j-labs/llm-graph-builder) (w) | v0.8.7 (20260723) | 1 | 22 |
| core | [memgraph/memgraph](https://github.com/memgraph/memgraph) | v3.14.0 (20261021) | 100+ | 88 |
| core | [FlowElement-xinliuyuansu/m_flow](https://github.com/FlowElement-xinliuyuansu/m_flow) | v0.3.4 (20260412) | 1 | 8 |
| core | [yifanfeng97/Hyper-Extract](https://github.com/yifanfeng97/Hyper-Extract) | v0.11.0 (20261029) | 100+ | 20 |
| core | [OSU-NLP-Group/HippoRAG](https://github.com/OSU-NLP-Group/HippoRAG) (w) | v1.0.0 (20250227) | 10 | 20 |
| core | [pipeshub-ai/pipeshub-ai](https://github.com/pipeshub-ai/pipeshub-ai) | v1.0.0 (20261027) | 100+ | 85 |
| core | [GH05TCREW/pentestagent](https://github.com/GH05TCREW/pentestagent) | none | 13 | 13 |
| core | [robert-mcdermott/ai-knowledge-graph](https://github.com/robert-mcdermott/ai-knowledge-graph) | v0.8.0 (20260912) | 24 | 3 |
| core | [MemMachine/MemMachine](https://github.com/MemMachine/MemMachine) | v0.4.0 (20261008) | 39 | 49 |
| core | [pingcap/autoflow](https://github.com/pingcap/autoflow) | 0.4.0 (20250103) | 0 | 20 |
| core | [trustgraph-ai/trustgraph](https://github.com/trustgraph-ai/trustgraph) | v2.8.17 (20260908) | 99 | 31 |
| core | [neo4j/neo4j-graphrag-python](https://github.com/neo4j/neo4j-graphrag-python) (w) | 1.23.0 (20261028) | 100+ | 42 |
| core | [FalkorDB/GraphRAG-SDK](https://github.com/FalkorDB/GraphRAG-SDK) (w) | v1.5.0 (20261022) | 100+ | 11 |
| core | [OpenSPG/KAG](https://github.com/OpenSPG/KAG) (w) | v0.8.0 (20250628) | 0 | 25 |
| core | [gusye1234/nano-graphrag](https://github.com/gusye1234/nano-graphrag) (w) | v0.0.8 (20241001) | 0 | 20 |
| core | [circlemind-ai/fast-graphrag](https://github.com/circlemind-ai/fast-graphrag) (w) | none | 0 | 15 |
| core | [DEEP-PolyU/Awesome-GraphRAG](https://github.com/DEEP-PolyU/Awesome-GraphRAG) (w) | none | 0 | 12 |
| core | [HKUDS/MiniRAG](https://github.com/HKUDS/MiniRAG) (w) | v0.0.2 (20250227) | 0 | 16 |
| core | [TencentCloudADP/youtu-graphrag](https://github.com/TencentCloudADP/youtu-graphrag) (w) | v0.2.1 (20260226) | 0 | 11 |
| core | [LHRLAB/Graph-R1](https://github.com/LHRLAB/Graph-R1) (w) | none | 0 | 1 |
| core | [DEEP-PolyU/LinearRAG](https://github.com/DEEP-PolyU/LinearRAG) (w) | none | 0 | 6 |
| core | [chensyCN/LogicRAG](https://github.com/chensyCN/LogicRAG) (w) | none | 0 | 2 |
| core | [datastax/graph-rag](https://github.com/datastax/graph-rag) (w) | v0.8.0 (20250404) | 0 | 5 |
| agent-memory | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | v15.7.0 (20261030) | 100+ | 315 |
| agent-memory | [666ghj/MiroFish](https://github.com/666ghj/MiroFish) | v0.1.2 (20260307) | 7 | 19 |
| agent-memory | [mem0ai/mem0](https://github.com/mem0ai/mem0) (w) | ts-v3.3.1 (20260925) | 100+ | 411 |
| agent-memory | [bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book) | none | 100+ | 92 |
| agent-memory | [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | v1.1.0 (20261021) | 100+ | 291 |
| agent-memory | [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | v0.5.2.1 (20261027) | 100+ | 324 |
| agent-memory | [pingcap/tidb](https://github.com/pingcap/tidb) | v7.5.8 (20260917) | 100+ | 1,092 |
| agent-memory | [topoteretes/cognee](https://github.com/topoteretes/cognee) (w) | v1.6.6 (20261029) | 100+ | 333 |
| agent-memory | [getzep/graphiti](https://github.com/getzep/graphiti) (w) | v0.31.2 (20261020) | 100+ | 64 |
| agent-memory | [supermemoryai/supermemory](https://github.com/supermemoryai/supermemory) | server-v0.0.9 (20261012) | 100+ | 114 |
| agent-memory | [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | v2.0.3 (20261026) | 71 | 37 |
| agent-memory | [letta-ai/letta](https://github.com/letta-ai/letta) (w) | 0.16.8 (20260514) | 7 | 155 |
| agent-memory | [dolthub/dolt](https://github.com/dolthub/dolt) | v2.6.1 (20261026) | 100+ | 192 |
| agent-memory | [screenpipe/screenpipe](https://github.com/screenpipe/screenpipe) | app-v2.7.130 (20261028) | 100+ | 176 |
| agent-memory | [xerj-org/xerj](https://github.com/xerj-org/xerj) | v1.0.0-rc.100 (20261027) | 100+ | 106 |
| agent-memory | [MemoriLabs/Memori](https://github.com/MemoriLabs/Memori) | v3.3.6 (20260528) | 3 | 43 |
| agent-memory | [NevaMind-AI/memU](https://github.com/NevaMind-AI/memU) | v1.5.1 (20260323) | 52 | 49 |
| agent-memory | [EverMind-AI/EverOS](https://github.com/EverMind-AI/EverOS) | v1.5.1 (20261022) | 74 | 10 |
| agent-memory | [MemTensor/MemOS](https://github.com/MemTensor/MemOS) (w) | v2.0.34 (20260923) | 100+ | 103 |
| agent-memory | [TencentCloud/Octop](https://github.com/TencentCloud/Octop) | v1.0.3b1 (20261025) | 100+ | 74 |
| agent-memory | [plastic-labs/honcho](https://github.com/plastic-labs/honcho) | v3.5.0 (20261030) | 100+ | 74 |
| agent-memory | [julep-ai/julep](https://github.com/julep-ai/julep) | none | 0 | 4 |
| agent-memory | [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) | v0.20.0 (20261025) | 100+ | 53 |
| agent-memory | [ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) | none | 100+ | 10 |
| agent-memory | [CaviraOSS/LongMemory](https://github.com/CaviraOSS/LongMemory) | v1.3.0 (20251220) | 37 | 51 |
| agent-memory | [agiresearch/A-mem](https://github.com/agiresearch/A-mem) (w) | none | 0 | 6 |
| markdown-kb | [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki) | v0.6.13 (20261022) | 100+ | 43 |
| markdown-kb | [AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) | v3.0.1 (20261021) | 100+ | 11 |
| markdown-kb | [breferrari/obsidian-mind](https://github.com/breferrari/obsidian-mind) | v10.0.0 (20261012) | 100+ | 13 |
| markdown-kb | [inkeep/open-knowledge](https://github.com/inkeep/open-knowledge) | v0.89.0 (20261030) | 100+ | 15 |
| markdown-kb | [basicmachines-co/basic-memory](https://github.com/basicmachines-co/basic-memory) (w) | v1.0.0 (20261029) | 100+ | 57 |
| markdown-kb | [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) (w) | none | 15 | 8 |
| markdown-kb | [Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki) (w) | v2026.10.4 (20261027) | 100+ | 37 |
| markdown-kb | [atomicstrata/llm-wiki-compiler](https://github.com/atomicstrata/llm-wiki-compiler) | v1.5.0 (20261019) | 100+ | 17 |
| markdown-kb | [nhaouari/obsidian-textgenerator-plugin](https://github.com/nhaouari/obsidian-textgenerator-plugin) | 0.8.7 (20260427) | 3 | 28 |
| markdown-kb | [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki) | none | 20 | 5 |
| markdown-kb | [PKU-DAIR/AutoSci](https://github.com/PKU-DAIR/AutoSci) | none | 13 | 6 |
| markdown-kb | [yuezhiai/jonex](https://github.com/yuezhiai/jonex) | none | 47 | 11 |
| markdown-kb | [nvk/llm-wiki](https://github.com/nvk/llm-wiki) | v1.0.0 (20261024) | 100+ | 9 |
| markdown-kb | [s2b-dev/smart-second-brain](https://github.com/s2b-dev/smart-second-brain) | 2.3.0 (20260928) | 100+ | 15 |
| markdown-kb | [huytieu/COG-second-brain](https://github.com/huytieu/COG-second-brain) | v3.16.0 (20261023) | 15 | 6 |
| markdown-kb | [chubbyguan/chubbyskills](https://github.com/chubbyguan/chubbyskills) | v0.15.0 (20261008) | 76 | 8 |
| markdown-kb | [thClaws/thClaws](https://github.com/thClaws/thClaws) | v0.149.0 (20261029) | 65 | 32 |
| markdown-kb | [mateaix/mateclaw](https://github.com/mateaix/mateclaw) | v3.0.0 (20261027) | 100+ | 20 |
| markdown-kb | [undefined-ui/second-brain-os](https://github.com/undefined-ui/second-brain-os) | none | 43 | 1 |
| markdown-kb | [agents-flex/agents-flex](https://github.com/agents-flex/agents-flex) | v2.3.0 (20260917) | 100+ | 68 |
| markdown-kb | [Robinson-AI-Lab/FridayOS1.0](https://github.com/Robinson-AI-Lab/FridayOS1.0) | none | 88 | 3 |
| markdown-kb | [kiwifs/kiwifs](https://github.com/kiwifs/kiwifs) | v0.19.81 (20261028) | 85 | 20 |
| markdown-kb | [Railly/agentfiles](https://github.com/Railly/agentfiles) | 0.9.1 (20260831) | 14 | 10 |
| markdown-kb | [GD4AI/obsidian-llm-wiki](https://github.com/GD4AI/obsidian-llm-wiki) | 1.29.0 (20261028) | 100+ | 28 |
| markdown-kb | [agarwalvishal/claude-chat-exporter](https://github.com/agarwalvishal/claude-chat-exporter) | none | 9 | 1 |
| markdown-kb | [VectifyAI/OpenKB](https://github.com/VectifyAI/OpenKB) (w) | v0.4.5 (20260720) | 0 | 14 |
| markdown-kb | [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki) (w) | none | 0 | 1 |
| adjacent | [langgenius/dify](https://github.com/langgenius/dify) (w) | 1.18.0 (20261023) | 100+ | 1,592 |
| adjacent | [open-webui/open-webui](https://github.com/open-webui/open-webui) | v0.12.5 (20261029) | 100+ | 892 |
| adjacent | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | langchain-core==1.7.3 (20261029) | 100+ | 3,749 |
| adjacent | [infiniflow/ragflow](https://github.com/infiniflow/ragflow) (w) | v1.0.0-rc3 (20261030) | 100+ | 908 |
| adjacent | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) (w) | v2.2.0 (20261028) | 100+ | 1,072 |
| adjacent | [Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) | v2.9.0 (20260710) | 100+ | 75 |
| adjacent | [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) | v0.9.5 (20261014) | 100+ | 103 |
| adjacent | [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) | V1.0.3 (20260717) | 58 | 123 |
| adjacent | [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) | v0.42.0 (20261026) | 100+ | 359 |
| adjacent | [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) | v1.6.2 (20261003) | 100+ | 51 |
| adjacent | [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) (w) | v1.19.0 (20261026) | 100+ | 283 |
| adjacent | [pathwaycom/serviette](https://github.com/pathwaycom/serviette) | none | 5 | 27 |
| adjacent | [run-llama/llama_index](https://github.com/run-llama/llama_index) (w) | v0.14.25 (20260921) | 90 | 2,007 |
| adjacent | [jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot) | v3.9.5 (20260827) | 78 | 40 |
| adjacent | [milvus-io/milvus](https://github.com/milvus-io/milvus) | v3.0.5 (20261030) | 100+ | 394 |
| adjacent | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 1.2.18 (20261026) | 100+ | 294 |
| adjacent | [VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex) | v0.5.0 (20261029) | 100+ | 16 |
| adjacent | [The-Vibe-Company/quivr](https://github.com/The-Vibe-Company/quivr) | v2.0.2 (20261030) | 100+ | 120 |
| adjacent | [khoj-ai/khoj](https://github.com/khoj-ai/khoj) (w) | 2.0.0-beta.28 (20260326) | 2 | 76 |
| adjacent | [ItzCrazyKns/Vane](https://github.com/ItzCrazyKns/Vane) | v1.12.2 (20260410) | 1 | 50 |
| adjacent | [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) | v1.4.0 (20260810) | 100+ | 54 |
| adjacent | [Tencent/WeKnora](https://github.com/Tencent/WeKnora) | v0.9.0 (20261029) | 100+ | 346 |
| adjacent | [datawhalechina/happy-llm](https://github.com/datawhalechina/happy-llm) | v1.0.2 (20260129) | 3 | 33 |
| adjacent | [surrealdb/surrealdb](https://github.com/surrealdb/surrealdb) | v3.3.5 (20261029) | 3 | 184 |
| adjacent | [onyx-dot-app/onyx](https://github.com/onyx-dot-app/onyx) | v5.0.1 (20261026) | 100+ | 210 |
| adjacent | [deepset-ai/haystack](https://github.com/deepset-ai/haystack) (w) | v3.4.1 (20261021) | 100+ | 524 |
| adjacent | [vitali87/code-graph-rag](https://github.com/vitali87/code-graph-rag) (w) | v0.4.5 (20261030) | 100+ | 74 |
| adjacent | [stanford-oval/storm](https://github.com/stanford-oval/storm) (w) | v1.1.0 (20250123) | 0 | 26 |
| adjacent | [Cinnamon/kotaemon](https://github.com/Cinnamon/kotaemon) (w) | v0.12.0 (20260531) | 0 | 39 |
| adjacent | [SciPhi-AI/R2R](https://github.com/SciPhi-AI/R2R) (w) | v3.6.5 (20250606) | 0 | 63 |
| adjacent | [kuzudb/kuzu](https://github.com/kuzudb/kuzu) (w) | v0.11.3 (20251010) | 0 | 63 |

## Search queries

| Category | Query | Pass | Matches reported by GitHub | Returned |
|---|---|---|---|---|
| core | `topic:graphrag` | active | 48 | 48 |
| core | `topic:graphrag` | quiet | 37 | 37 |
| core | `topic:graph-rag` | active | 15 | 15 |
| core | `topic:graph-rag` | quiet | 6 | 6 |
| core | `topic:knowledge-graph topic:llm` | active | 77 | 77 |
| core | `topic:knowledge-graph topic:llm` | quiet | 40 | 40 |
| core | `topic:knowledge-graph topic:rag` | active | 63 | 63 |
| core | `topic:knowledge-graph topic:rag` | quiet | 25 | 25 |
| core | `"knowledge graph construction" in:name,description` | active | 1 | 1 |
| core | `"knowledge graph construction" in:name,description` | quiet | 13 | 13 |
| core | `text2cypher in:name,description,readme` | active | 5 | 5 |
| core | `text2cypher in:name,description,readme` | quiet | 7 | 7 |
| agent-memory | `topic:agent-memory` | active | 202 | 100 |
| agent-memory | `topic:agent-memory` | quiet | 20 | 20 |
| agent-memory | `topic:ai-memory` | active | 103 | 100 |
| agent-memory | `topic:ai-memory` | quiet | 18 | 18 |
| agent-memory | `topic:long-term-memory` | active | 70 | 70 |
| agent-memory | `topic:long-term-memory` | quiet | 20 | 20 |
| agent-memory | `topic:mcp-server knowledge graph in:description` | active | 13 | 13 |
| agent-memory | `topic:mcp-server knowledge graph in:description` | quiet | 2 | 2 |
| markdown-kb | `topic:llm-wiki` | active | 24 | 24 |
| markdown-kb | `topic:llm-wiki` | quiet | 8 | 8 |
| markdown-kb | `"llm wiki" in:name,description` | active | 32 | 32 |
| markdown-kb | `"llm wiki" in:name,description` | quiet | 31 | 31 |
| markdown-kb | `topic:obsidian topic:llm` | active | 27 | 27 |
| markdown-kb | `topic:obsidian topic:llm` | quiet | 10 | 10 |
| markdown-kb | `topic:obsidian topic:ai-agents` | active | 27 | 27 |
| markdown-kb | `topic:obsidian topic:ai-agents` | quiet | 8 | 8 |
| adjacent | `topic:graph-database` | active | 73 | 73 |
| adjacent | `topic:graph-database` | quiet | 64 | 64 |
| adjacent | `code knowledge graph in:description` | active | 27 | 27 |
| adjacent | `code knowledge graph in:description` | quiet | 39 | 39 |
| adjacent | `topic:rag topic:llm` | active | 379 | 100 |
| adjacent | `topic:rag topic:llm` | quiet | 248 | 100 |

Each query is run with `stars:>=100`; the *active* pass adds a `pushed:` date qualifier for the recent window and the *quiet* pass for the older one. A result list is capped at 100 per pass, so the quiet tables are a sample of what exists, not a census.

## Failures

None.
