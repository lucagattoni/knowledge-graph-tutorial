# The LLM era: how knowledge bases and knowledge graphs changed, 2020 to October 2026

**Status:** first full draft, written 20261030 19:08 UTC. Covers 20200522 to 20261030. Every fact cites a
numbered source in the [source list](#sources) with the time it was read. Where the sources are silent
the text says **unstated**.

## Three kinds of date

This page keeps three dates apart. The table says which one it means in each row.

| Kind | What it is | Where it comes from |
|---|---|---|
| **Paper** | The arXiv `published` field: the day version 1 was submitted | arXiv API (S3) |
| **Repo created** | The `created_at` field of the GitHub repository | GitHub API (S2) |
| **Release / post** | A tagged release, a spec revision tag, a blog post or a commit | The release list, the post, the commit log |

A repository can be created long before its first release (GraphRAG: 20240327 and 20240702), and a
paper can come before or after its code (HippoRAG: same day).

## 1. The arc in one screen

The phase boundaries are the author's judgement from the table below, not a date the sources state.

| Phase | Dates | What happened |
|---|---|---|
| 1. Retrieval is attached to language models | 20200522 to 20221231 | The RAG paper names the pattern. ReAct (20221006), then the LangChain and LlamaIndex repositories appear in late 2022. |
| 2. Agents and memory-as-a-system | 20230101 to 20231231 | Self-RAG and MemGPT frame the model as something that decides what to read and what to remember. Aider ships a graph-ranked repository map for code. |
| 3. Graph-based RAG and the protocol | 2024 | GraphRAG (paper, then code), HippoRAG, LightRAG, HybridRAG. LazyGraphRAG (20241125) answers the indexing cost. MCP is announced the same day. |
| 4. Cost correction, then agent memory | 20250101 to 20250928 | Zep/Graphiti, A-MEM and Mem0 move the target from documents to agent memory. Surveys and GraphRAG-Bench question when a graph helps. "Context engineering" becomes a term. |
| 5. Files, skills and standards | 20250929 to 20251231 | Anthropic ships a file-based memory tool and Agent Skills. MCP moves to the Linux Foundation. Kuzu, an embedded graph database, is archived. |
| 6. Code graphs and the LLM wiki | 20260101 to 20260727 | OpenViking (a filesystem for agent context), code-graph MCP servers, GraphRAG v3, Karpathy's LLM Wiki gist, Graphify, Google's OKF format. |
| 7. Consolidation and commercialisation | 20260728 to 20261030 | MCP revision 2026-07-28 drops sessions and deprecates Sampling. Open-source memory and graph projects add cloud tiers or stronger licences. Markdown-first memory projects multiply. |

## 2. Timeline

"Why it mattered" is the author's reading of the cited facts. Where only a title was read, the row says so.
Star counts are as of the time the repository was read (20261030 18:59 to 19:03 UTC).

| Date (UTC day) | Event | Why it mattered | Source |
|---|---|---|---|
| 20200522 | **Paper.** "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (arXiv 2005.11401). | Origin of the term RAG used in every later row. Only the title was read; method details unstated. | S3 |
| 20221006 | **Paper.** "ReAct: Synergizing Reasoning and Acting in Language Models" (2210.03629). | Interleaving reasoning with actions is the loop that agentic retrieval later uses. Author's reading; abstract not read. | S3 |
| 20221017 | **Repo created.** `langchain-ai/langchain`. 148,719 stars, MIT. | Largest general LLM-application framework in the list read. Whether it ships GraphRAG support: unstated. | S2 |
| 20221102 | **Repo created.** `run-llama/llama_index`. 52,746 stars, MIT. | Second general framework in the list. Same caveat: graph support unstated. | S2 |
| 20231011 | **Repo created.** `letta-ai/letta`. 25,294 stars, Apache-2.0. Latest tagged release in the list read: 0.16.8 on 20260514. | The repo exists the day before the MemGPT paper. The rename from MemGPT to Letta is not stated in the sources read. | S2, S26 |
| 20231012 | **Paper.** "MemGPT: Towards LLMs as Operating Systems" (2310.08560). | Title frames the context window as managed memory. Abstract not read. The Zep paper (20250120) names MemGPT as the system it compares against. | S3 |
| 20231017 | **Paper.** "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection" (2310.11511). | An early case of the model judging its own retrieval. Title only. | S3 |
| 20231022 | **Blog post.** Aider's "repository map". | Source files as graph nodes ranked by dependency, symbols extracted with tree-sitter, sent with every change request within a token budget. The earliest code-graph-for-LLM item in this list. | S15 |
| 20240227 | **Paper.** "Evaluating Very Long-Term Conversational Memory of LLM Agents" (2402.17753), the LoCoMo benchmark. | A conversational-memory benchmark that later memory systems report against (Mem0 README, 202604). Title only. | S3, S20 |
| 20240327 | **Repo created.** `microsoft/graphrag`. 36,498 stars, MIT. | Creation date only. Whether the repo was private before 20240702 is unstated. | S2 |
| 20240424 | **Paper.** "From Local to Global: A Graph RAG Approach to Query-Focused Summarization" (2404.16130). | The GraphRAG paper. Title only; the method is described in the 20240702 post. | S3 |
| 20240523 | **Paper and repo created, same day.** "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models" (2405.14831); `OSU-NLP-Group/HippoRAG`, 4,083 stars, MIT. | Early use of "long-term memory" in the title of a graph-retrieval paper. Title only. | S3, S2 |
| 20240702 | **Blog post and first release.** Microsoft: GraphRAG "is now available" on GitHub; it "uses a large language model (LLM) to automate the extraction of a rich knowledge graph". The oldest release in the list is v0.1.1, same day. | The eager design: an LLM reads the whole corpus first and builds the graph before any question. This is the cost that later rows try to remove. | S22, S12 |
| 20240808 | **Repo created.** `getzep/graphiti`. 32,372 stars, Apache-2.0. | The temporal knowledge-graph engine behind Zep (per the Zep paper, 20250120). | S2, S3 |
| 20240809 | **Paper.** "HybridRAG: Integrating Knowledge Graphs and Vector Retrieval Augmented Generation" (2408.04948). | Hybrid vector-plus-graph retrieval gets a name. Title only. | S3 |
| 20240815 | **Paper.** "Graph Retrieval-Augmented Generation: A Survey" (2408.08921). | First survey in the list read that treats GraphRAG as a field. Title only. | S3 |
| 20241002 | **Repo created.** `HKUDS/LightRAG`. 40,443 stars, MIT; pushed 20261029. | Still active 25 months later: the eager, LLM-extracted graph did not disappear. | S2 |
| 20241008 | **Paper.** "LightRAG: Simple and Fast Retrieval-Augmented Generation" (2410.05779). | The paper follows the repo by six days. Title only. | S3 |
| 20241014 | **Paper.** "LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory" (2410.10813). | The second memory benchmark that later systems report against. Title only. | S3, S20 |
| 20241119 | **Repo created.** `modelcontextprotocol/servers`. 91,699 stars. | Reference servers appear six days before the announcement. | S2 |
| 20241125 | **Blog post.** Anthropic introduces MCP, "an open standard that enables developers to build secure, two-way connections between their data sources and AI-powered tools". Early adopters named: Block and Apollo. | Tools and data sources get one protocol, which later lets an agent traverse a knowledge base by tool calls. | S4 |
| 20241125 | **Blog post.** Microsoft: LazyGraphRAG. Indexing cost "identical to vector RAG and 0.1% of the costs of full GraphRAG"; comparable quality to GraphRAG global search at "more than 700 times lower query cost". Defers all LLM use to query time. | The lazy answer to the cost of the eager graph. Microsoft's own figures; no independent replication read. | S6 |
| 20241211 | **Release.** GraphRAG v1.0.0. | First stable major version, five months after the first release. | S12 |
| 20241213 | **Paper.** "Text2Cypher: Bridging Natural Language and Graph Databases" (2412.10064). | Names natural-language-to-Cypher as its own task. Title only. | S3 |
| 20241220 | **Paper.** "Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks" (2412.15605). | Argues from the title for preloading knowledge into a long context instead of retrieving. A retreat from retrieval itself. Title only. | S3 |
| 20250115 | **Paper.** "Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG" (2501.09136). | Abstract: traditional RAG is "constrained by static workflows"; agents add "reflection, planning, tool use, and multi-agent collaboration". | S3, S24 |
| 20250120 | **Paper.** "Zep: A Temporal Knowledge Graph Architecture for Agent Memory" (2501.13956). | The graph engine (Graphiti) is aimed at "ongoing conversations and business data", not static documents. Claims to beat MemGPT on the DMR benchmark; the authors' own claim. | S3, S24 |
| 20250217 | **Paper.** "A-MEM: Agentic Memory for LLM Agents" (2502.12110). | Memory organised by the agent. Title only. Repo `agiresearch/A-mem` created 20250225; last push 20251212. | S3, S2 |
| 20250217 | **Paper.** "RAG vs. GraphRAG: A Systematic Evaluation and Key Insights" (2502.11371). | Abstract: GraphRAG evaluations used "heterogeneous evaluation protocols", so a systematic comparison on text benchmarks was lacking. | S3, S24 |
| 20250220 | **Paper.** "From RAG to Memory: Non-Parametric Continual Learning for Large Language Models" (2502.14802), HippoRAG 2. | The title states the shift from document retrieval to memory. Title only. | S3 |
| 20250225 | **Release.** GraphRAG v2.0.0. | Second major version, 11 months after the repository was created. | S12 |
| 20250312 | **Paper.** "Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning" (2503.09516). | Retrieval calls learned by reinforcement learning, not fixed by a pipeline. Title only. | S3 |
| 20250326 | **Spec revision tag.** MCP `2025-03-26`. The 20260728 changelog says the HTTP+SSE transport has been "deprecated since protocol version 2025-03-26". | The transport that remote servers use changes here. | S11, S18 |
| 20250428 | **Paper.** "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory" (2504.19413). | Abstract: a memory architecture that extracts, consolidates and retrieves facts, plus "an enhanced variant that leverages graph-based memory representations". The graph is the optional variant. | S3, S24 |
| 20250606 | **Paper.** "When to use Graphs in RAG: A Comprehensive Analysis for Graph Retrieval-Augmented Generation" (2506.05690), GraphRAG-Bench. | Abstract: "recent studies report that GraphRAG frequently underperforms vanilla RAG on many real-world tasks". The strongest published doubt in the list read. | S3, S24 |
| 20250606 | **Repo created.** `HKUDS/RAG-Anything`. 24,322 stars, MIT. | Multimodal RAG from the LightRAG team. Merged into LightRAG in 202605 (see below), yet the repo stays active (pushed 20261028). | S2, S20 |
| 20250618 | **Spec revision tag.** MCP `2025-06-18`. | Contents not read here. | S11 |
| 20250627 | **Blog post.** Simon Willison on "context engineering". He quotes Tobi Lutke ("the art of providing all the context for the task to be plausibly solvable by the LLM") and Andrej Karpathy ("the delicate art and science of filling the context window with just the right information for the next step"). Dates of those two posts: unstated. | The term that replaces "prompt engineering" for agent builders and puts memory and retrieval under one heading. | S17 |
| 20250819 | **Repo created.** `agentsmd/agents.md`. 25,220 stars, MIT. | A plain-file convention for telling agents about a project; Karpathy's gist later calls `CLAUDE.md` or `AGENTS.md` "a configuration document". The repo's own description was not read. | S2, S5, S10 |
| 20250929 | **Blog post.** Anthropic: the memory tool lets Claude "store and consult information outside the context window through a file-based system", "entirely client-side", in "a dedicated memory directory stored in your infrastructure". Context editing clears stale tool results. | A vendor ships agent memory as files the developer owns, not as a graph or a hosted store. | S16 |
| 20250929 | **Blog post.** Anthropic: "Effective context engineering for AI agents". Defines it as "curating and maintaining the optimal set of tokens". Agents keep "lightweight identifiers" and load data at runtime; in Claude Code "glob and grep" retrieve files "just-in-time". | A first-party statement that a coding agent navigates by tools, not by pre-computed embeddings alone. | S7 |
| 20251006 | **Paper.** "Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models" (2510.04618). | Context treated as something an agent edits over time. Title only. | S3 |
| 20251010 | **Retreat.** Kuzu, an embedded property-graph database with Cypher, full-text and vector indexes, is archived (`kuzudb/kuzu`, MIT). The README says "Kuzu is working on something new!". BetaKit: on 20251009 "Apple struck an agreement to buy all shares and hire select employees of Kuzu"; the repository "was archived on Oct. 10"; the company site is no longer operational. BetaKit published 20260212. | An embedded graph database leaves open development within a day of the deal. The README says prior releases "will continue to be usable in the same way"; no later release is stated. | S9, S21, S2 |
| 20251016 | **Blog post.** Anthropic: Agent Skills. "Skills are folders that include instructions, scripts, and resources that Claude can load when needed"; Claude "loads only the minimal information and files needed". Updated 20251218. The `anthropics/skills` repo was created 20250922; 185,156 stars; GitHub reports no licence for the repo, so its licence is unstated. | Knowledge and procedure packaged as files and loaded on demand. | S23, S2 |
| 20251030 | **Repo created.** `vectorize-io/hindsight`. 56,603 stars, MIT. README: "retain / recall / reflect" operations and "mental models & knowledge pages". It claims to eliminate "the shortcomings of alternative techniques such as RAG and knowledge graph"; that is the vendor's claim. | An agent-memory system that sets itself against both RAG and graphs. | S2, S20 |
| 20251101 | **Quiet retreat.** `circlemind-ai/fast-graphrag` (3,967 stars, MIT) last pushed 20251101, not archived. | A 2024 "cheaper GraphRAG" project with no push for 12 months. `gusye1234/nano-graphrag` last pushed 20260127. Dormancy, not a stated decision. | S2 |
| 20251125 | **Spec revision tag.** MCP `2025-11-25`. | The base for the 2026 changes below. | S11, S18 |
| 20251209 | **Blog post.** MCP donated to the Agentic AI Foundation under the Linux Foundation, with Block's goose and OpenAI's AGENTS.md as the other founding projects. Anthropic's figures: "Over 97 million monthly SDK downloads, 10,000 active servers". | The protocol leaves single-vendor control. The figures are Anthropic's. | S5 |
| 20251214 | **Paper.** "Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects" (2512.12818). | The paper behind the repo created 20251030. Title only. | S3 |
| 20251215 | **Paper.** "Memory in the Age of AI Agents" (2512.13564), a survey. | Abstract: the field "has become increasingly fragmented"; it separates agent memory from "LLM memory, retrieval augmented generation (RAG), and context engineering". | S3, S24 |
| 20260105 | **Repo created.** `volcengine/OpenViking`. 41,198 stars. README: "a context database for AI agents", with `viking://` as "one filesystem for knowledge, memory, and skills"; sessions become Markdown files. | A database that presents itself as a filesystem. | S2, S20 |
| 20260105 | **Paper.** "SimpleMem: Efficient Lifelong Memory for LLM Agents" (2601.02553). | Abstract: compresses interactions into "compact, multi-view indexed memory units" to cut token cost. Not a graph. | S3, S24 |
| 20260128 | **Release.** GraphRAG v3.0.0: "Monorepo restructure" into packages (cache, chunking, input, llm, storage, vectors). Requires `graphrag init --force`. | A restructure, not a retreat: Microsoft's project is still shipping (v3.3.0 on 20261008). | S12 |
| 20260224 | **Repo created.** `DeusData/codebase-memory-mcp`. 47,853 stars, MIT. "A persistent local knowledge graph" of code, docs, config and infrastructure, 17 MCP tools, "source analysis and graph storage run on your machine". | A code knowledge graph delivered as an MCP server for coding agents. | S2, S20 |
| 20260226 | **Repo created.** `tirth8205/code-review-graph`. 32,508 stars, MIT. "Local-first code intelligence graph for MCP and CLI" (GitHub description). | Second code-graph MCP project created within two days. | S1, S2 |
| 20260330 | **Licence change.** `volcengine/OpenViking`: commit "change the main lisence to AGPL-3.0 (#1085)". The LICENSE file is the AGPL v3. The earlier licence is unstated in the sources read. | A stronger copyleft licence on a fast-growing agent-memory project. | S20 |
| 20260403 | **Repo created.** `Graphify-Labs/graphify`. 139,349 stars, Apache-2.0 (LICENSE file confirms). README: code is parsed with tree-sitter, "deterministic, no LLM"; edges tagged `EXTRACTED` or `INFERRED`; "Not a vector index". It also advertises Graphify Cloud and a Y Combinator S26 badge. | Code graph without LLM extraction, next to a paid cloud tier. See the star-growth flag below. | S2, S8 |
| 20260404 | **Gist.** Karpathy's "LLM Wiki" (page shows "Created April 4, 2026 16:25", time zone unstated). The LLM "incrementally builds and maintains a persistent wiki"; "the knowledge is compiled once and then kept current, not re-derived on every query"; the index file "avoids the need for embedding-based RAG infrastructure" and "at small scale the index file is enough, but as the wiki grows you want proper search". | Names the Markdown-wiki pattern and sets the scale caveat itself. | S10 |
| 20260404 to 20260603 | **Repos created, the LLM-wiki wave.** `lucasastorian/llmwiki` (20260404, 1,734 stars), `Astro-Han/karpathy-llm-wiki` (20260405, 2,642), `Ar9av/obsidian-wiki` (20260406, 3,640), `AgriciDaniel/claude-obsidian` (20260407, 16,002, MIT), `inkeep/open-knowledge` (20260603, 4,741). | Implementations appear within hours to three days of the gist. | S1, S1b, S2 |
| 202604 (day unstated) | **README section.** Mem0: "New Memory Algorithm (April 2026)". "Single-pass ADD-only extraction -- one LLM call, no UPDATE/DELETE"; entity linking; semantic, BM25 and entity signals fused. Self-reported: LoCoMo 71.4 to 92.5, LongMemEval 67.8 to 94.4. Scores "reflect Mem0's managed platform, which includes proprietary optimizations not available in the open-source". `mem0ai/mem0`: 68,112 stars, Apache-2.0. | The new write path is append-only, and the best numbers belong to the paid platform. What the previous algorithm did on writes: unstated in this README section. | S20, S2 |
| 20260504 | **Repo created.** `GoogleCloudPlatform/knowledge-catalog` (Apache-2.0; its README says "not an official Google product" and that Knowledge Catalog is "formerly Dataplex"). It holds the Open Knowledge Format v0.2 specification: "a directory of markdown files with YAML frontmatter. There is no schema registry, no central authority, and no required tooling." | A Google Cloud repository publishes plain Markdown with front matter as a knowledge format. When OKF v0.1 and v0.2 were first published: unstated. | S2, S14 |
| 202605 (day unstated) | **README news.** LightRAG: "Merge RagAnything into LightRAG" (2026.05); role-specific LLM settings including an EXTRACT role; OpenSearch as a storage backend (2026.03). | The eager LLM-extracted graph is still the core of the project; the two sibling projects merge. | S20 |
| 20260529 / 20260728 | **Spec revision.** MCP `2026-07-28`: release candidate 20260529, stable 20260728. Removes protocol-level sessions and the `initialize` handshake ("Make MCP stateless"); adds `server/discover`; moves tasks into an extension. **Deprecates** Roots, Sampling and Logging, and Dynamic Client Registration in favour of Client ID Metadata Documents. | The protocol gets simpler to host and loses the server-to-model call (Sampling) that some memory servers could have used. The changelog gives no reason for the deprecations. | S11, S18 |
| by 20261030 (change date unstated) | **State of `getzep/zep`.** README: the repository "is **not** Zep's product or service"; it holds "example code, framework integrations, and tools" for Zep Cloud, and points to Graphiti for "the open-source temporal knowledge graph framework that powers Zep". A commit on 20260729 deprecates the Zep MCP server README. 4,984 stars against 32,372 for Graphiti. | The hosted product is Cloud only; the open-source weight sits in Graphiti. | S13, S25, S2 |
| 20260901 | **Repo created.** `tigerless-labs/agent-memory`. 4,381 stars. "Long-term memory runtime for AI agents: plain Markdown as the source of truth, local ranked retrieval" (GitHub description). | Markdown-first memory as a product category. | S1 |
| 20260905 | **Repo created.** `okf-memory/okf-agent-memory`. MIT. Git-native memory in OKF v0.2 files, an MCP server (`okf_search`, `okf_show`, `okf_create`, `okf_validate`) and in-memory BM25 search. The README names two failure modes: a monolithic `AGENTS.md`/`CLAUDE.md`, and facts in a vector database that agents never search for. | Files, a standard format and a protocol meet in one small project. | S14, S1 |
| 20261007 | **Repo created.** `HelixDB/helix-foundry`. 1,854 stars, Apache-2.0. "Connect your company's data, let an agent draft an ontology over it, and load it into HelixDB as one graph" (GitHub description). | An agent writes the ontology and a graph database holds the result: the graph path is alive in October 2026. | S1, S2 |
| 20261008 | **Release.** GraphRAG v3.3.0. | Microsoft's GraphRAG is still maintained 22 months after v1.0.0. Whether LazyGraphRAG is in the open-source package: unstated. | S12 |

### Repositories created in 2026, by stars

GitHub search, `created:>2026-01-01`, topics `knowledge-graph`, `graphrag`, `agent-memory`, `mcp`
(S1, 20261030 18:58 UTC). Stars per day is stars divided by days since creation, an average, not a
recent rate. For comparison: `mem0ai/mem0` averages about 55 per day since 20230620 and
`microsoft/graphrag` about 39 per day since 20240327.

| Repository | Created | Stars | Per day | What it is (GitHub description) |
|---|---|---|---|---|
| `Graphify-Labs/graphify` | 20260403 | 139,344 | about 660 | Code, docs, SQL, PDFs into a queryable knowledge graph |
| `Egonex-AI/Understand-Anything` | 20260315 | 89,041 | about 390 | Any code into an interactive knowledge graph |
| `DeusData/codebase-memory-mcp` | 20260224 | 47,853 | about 190 | Local code intelligence for agents |
| `volcengine/OpenViking` | 20260105 | 41,198 | about 140 | Context database for agents |
| `tirth8205/code-review-graph` | 20260226 | 32,508 | about 130 | Local-first code intelligence graph |
| `xerj-org/xerj` | 20260630 | 17,683 | about 145 | AI search engine and MCP server for agents |
| `AgriciDaniel/claude-obsidian` | 20260407 | 16,001 | about 78 | Obsidian "second brain" kept by Claude Code |

**Flag.** Graphify gained about 660 stars per day on average over 210 days, 12 times Mem0's average.
Nine of the 15 repositories in the `knowledge-graph` result (by their GitHub descriptions) are code-intelligence, coding-agent or Obsidian second-brain tools.
I did not test whether the growth is organic (no stargazer timeline was sampled). Treat the counts as
attention, not as quality or adoption.

## 3. Shifts in approach

For each shift: what moved, evidence for, evidence against, and what the evidence supports.

### 3.1 From eager LLM-built graphs to cheaper or lazier graphs

| | Evidence |
|---|---|
| **For** | LazyGraphRAG: indexing cost "identical to vector RAG and 0.1% of the costs of full GraphRAG", all LLM use deferred to query time (S6). Graphify builds code graphs with tree-sitter, "deterministic, no LLM" (S8). Aider did the same for code in 20231022 (S15). Mem0's April 2026 algorithm uses "one LLM call" per write (S20). `zilliztech/vector-graph-rag`, created 20260205, 263 stars: "Graph RAG with pure vector search" (S1). SimpleMem compresses instead of building a graph (S24). |
| **Against** | LightRAG, an eager LLM-extraction design, is the most-starred document-graph project (40,443) and still adds features in 2026 (S2, S20). GraphRAG v3.3.0 shipped 20261008 and a v3 rewrite shipped 20260128 (S12). Whether LazyGraphRAG reached the open-source package: unstated. All LazyGraphRAG figures are Microsoft's own (S6). `fast-graphrag` and `nano-graphrag`, two "cheaper GraphRAG" projects, are quiet (S2). |
| **Reading** | The cost pressure is real, and the lazy and deterministic variants are well supported for **code** (no LLM needed). For **prose**, eager LLM extraction is still the dominant open-source design by stars. No independent comparison of lazy against eager was read. |

### 3.2 From graphs for documents to memory for agents

| | Evidence |
|---|---|
| **For** | Titles and abstracts move from "RAG" to "memory": HippoRAG 2 "From RAG to Memory" (20250220), Zep "for Agent Memory" (20250120), A-MEM, Mem0, Hindsight, SimpleMem (S3, S24). A December 2025 survey treats agent memory as separate from RAG and context engineering (S24). Stars: Mem0 68,112, Hindsight 56,603, OpenViking 41,198, against 36,498 for GraphRAG (S2). Graphiti is the engine of Zep's agent-memory paper (S3, S24). |
| **Against** | Memory claims rest on two conversational benchmarks, LoCoMo and LongMemEval, and the headline scores in READMEs are the vendors' own (S20). Mem0 says its best scores need "proprietary optimizations not available in the open-source" (S20). Mem0's April 2026 write path is append-only ("no UPDATE/DELETE") while its 20250428 paper abstract describes "consolidating" memories, so the write policy is not settled (S20, S24). In the Mem0 paper the graph is the optional variant (S24); the April 2026 README lists entity linking among its retrieval signals and does not mention a graph store (S20). Hindsight says it eliminates the shortcomings of "knowledge graph" approaches (S20). Document-side graph work continues: LightRAG merged RAG-Anything, GraphRAG v3.3.0 (S12, S20). |
| **Reading** | Attention moved to memory. The graph is no longer the default memory structure: of the memory systems whose abstracts or READMEs I read, only Zep/Graphiti puts a temporal graph at the centre. Whether memory helps more than long context is unmeasured in the sources read. |

### 3.3 From databases to plain files

| | Evidence |
|---|---|
| **For** | Karpathy's LLM Wiki: Markdown, an index file, no embedding infrastructure at small scale (S10). Anthropic's memory tool is file-based and client-side (S16); Agent Skills are folders (S23); AGENTS.md is a plain-file convention (S5, S10). Google's OKF is "a directory of markdown files with YAML frontmatter" (S14). Four 2026 projects are Markdown-based by their descriptions: `tigerless-labs/agent-memory`, `okf-memory/okf-agent-memory`, `Ar9av/obsidian-wiki`, `claude-obsidian` (S1, S14). Kuzu, an embedded graph database, was archived (S9, S21). OpenViking presents a database as a filesystem (S20). |
| **Against** | Karpathy himself: "as the wiki grows you want proper search" (S10), with no size given. OpenViking and Graphify keep indexes and graphs underneath the file view (S8, S20). Code-graph servers persist graphs, not files (S20). `helix-foundry` loads an agent-drafted ontology into a graph database in October 2026 (S1). LightRAG added OpenSearch as a backend in March 2026 (S20). Many of the file-based projects are weeks old: no long-run evidence. |
| **Reading** | Strong evidence of a files-first fashion for personal and per-project knowledge and for agent instructions. No evidence at corpus sizes where a wiki index stops being enough. The Kuzu archive shows the cost of depending on a single embedded engine; it does not show that graph databases are unneeded. |

### 3.4 From fixed retrieval pipelines to agent-driven traversal over tools (MCP)

| | Evidence |
|---|---|
| **For** | MCP launched 20241125 (S4); by 20251209 Anthropic reports "10,000 active servers" (S5); `modelcontextprotocol/servers` has 91,699 stars (S2). Anthropic's 20250929 post has agents hold identifiers and fetch with glob and grep "just-in-time" (S7). The Agentic RAG survey abstract (S24), and the titles of Self-RAG and Search-R1 (S3), put the retrieval decision in the model. Code-graph and memory projects ship as MCP servers: codebase-memory-mcp (17 tools), okf-agent-memory (S20, S14). |
| **Against** | The 2026-07-28 revision removes sessions and the handshake and deprecates Sampling, Roots and Logging; the changelog gives no reasons (S18). "Don't Do RAG" (CAG) argues for preloading over retrieval (S3). Graphify advertises "Cut agent token spend by 80%" for a graph the agent queries instead of grepping (S8); Anthropic describes its own coding agent navigating by grep and glob (S7). These two positions disagree and I read no independent measurement of either. The 10,000-server figure is Anthropic's. |
| **Reading** | The direction is well supported by the protocol's adoption. The sources read do not measure whether agent-driven traversal beats a fixed pipeline on cost or accuracy. |

### 3.5 From open projects to commercial tiers and tighter licences

| | Evidence |
|---|---|
| **For** | OpenViking moved to AGPL-3.0 on 20260330 (S20). `getzep/zep` is now examples for Zep Cloud (S13). Mem0's best numbers belong to the managed platform (S20). Graphify's README leads with Graphify Cloud (S8). Kuzu's team joined Apple and the engine stopped (S21). |
| **Against** | Most of the core projects keep permissive licences: GraphRAG, LightRAG and HippoRAG are MIT; Graphiti, Mem0 and Letta are Apache-2.0 (S2). MCP moved toward Apache-2.0, with a foundation (S19, S5). |
| **Reading** | A pattern of cloud tiers around open cores, not a mass retreat. Each retreat above is a single event; there are too few to call a rate. |

### 3.6 Code is handled apart from prose

| | Evidence |
|---|---|
| **For** | Code graphs are built by parsers, not LLMs (Aider 20231022, Graphify, codebase-memory-mcp) and are the fastest-growing 2026 category by stars (S15, S8, S20, S1). |
| **Against** | Anthropic's own coding agent uses grep and glob (S7). Whether a code graph beats grep for an agent: no measurement read. |
| **Reading** | A separate track, with deterministic extraction. Its value over plain search is open. |

## 4. Open questions

| # | Question | Why the evidence does not settle it | What would settle it |
|---|---|---|---|
| 1 | Does a graph beat plain retrieval for agent memory under independent evaluation? | GraphRAG-Bench reports GraphRAG "frequently underperforms vanilla RAG" (S24). The memory scores read are vendor-reported on LoCoMo and LongMemEval (S20). | One harness, several systems, same model, run by a third party. |
| 2 | Is LazyGraphRAG in the open-source `microsoft/graphrag` package? | The release notes and README were not read for it. | Read the package docs and release notes. |
| 3 | At what size does an LLM wiki with an index file stop working? | Karpathy gives no threshold (S10). | A size sweep with a fixed question set. |
| 4 | Is the 2026 star growth organic? | Graphify, 139,349 stars in 210 days; I sampled no stargazer timeline. Two repositories (`modelcontextprotocol/modelcontextprotocol` and `GoogleCloudPlatform/knowledge-catalog`) returned the identical star count 9,568 within three minutes; I left both counts out. | Sample stargazer timestamps; re-read the two counts. |
| 5 | Does a code graph beat grep for coding agents? | Opposing claims, no measurement (S8, S7). | Same tasks, same agent, graph tool on and off, tokens and success recorded. |
| 6 | Which memory write path holds over months: append-only, update and delete, or bi-temporal invalidation? | Mem0's April 2026 algorithm is append-only (S20); Zep's paper describes a temporal graph "maintaining historical relationships" (S24). No long-horizon comparison read. | A long-horizon test with contradicting facts. |
| 7 | Does stateless MCP change how knowledge-base servers keep state? | The changelog says servers "use explicit, server-minted handles passed as ordinary tool arguments" (S18); effects on memory servers: unstated. | Read the servers' migration notes after 202608. |
| 8 | Which storage engines are safe to depend on? | Kuzu stopped; OpenViking relicensed; Zep narrowed its open source (S9, S20, S13). Three events, no rate. | Track archived, relicensed and renamed repositories over time (the landscape snapshots). |
| 9 | Did the `anthropics/skills` repository have a repo-level licence? | GitHub reports none (S2); the LICENSE file was not read. | Read the file. |

## What was not checked

- For many papers only the title and v1 date were read (marked "Title only"). Abstracts were read for the
  seven papers cited as S24.
- Web search summaries were used to find leads and were not cited. Every cited web claim comes from a page
  fetched in this run.
- The Karpathy gist date comes from the fetched page; the GitHub gist API failed twice (HTTP 502).
- Star counts and licence identifiers come from the GitHub API; the licence file text was read only for
  MCP, OpenViking and Graphify.
- Read times below are the clock reading of the batch of calls the read belonged to; the true time is within
  two minutes after.

## Sources

| # | What | URL | Read (UTC) |
|---|---|---|---|
| S1 | GitHub repository search, `created:>2026-01-01` with topics `knowledge-graph`, `graphrag`, `agent-memory`, `mcp`+`knowledge-graph` | https://api.github.com/search/repositories | 20261030 18:58 |
| S1b | Same search, topic `llm-wiki` | https://api.github.com/search/repositories | 20261030 19:03 |
| S2 | GitHub repository metadata (`created_at`, `pushed_at`, stars, licence, archived), one call per repository | https://api.github.com/repos/OWNER/REPO | 20261030 18:59 and 19:02 |
| S3 | arXiv API, `published` field (version 1 date) and titles | https://export.arxiv.org/api/query | 20261030 18:59, 19:01, 19:02 |
| S4 | Anthropic, "Introducing the Model Context Protocol", 20241125 | https://www.anthropic.com/news/model-context-protocol | 20261030 18:59 |
| S5 | MCP blog, "MCP joins the Agentic AI Foundation", 20251209 | https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/ | 20261030 18:59 |
| S6 | Microsoft Research, LazyGraphRAG, 20241125 | https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ | 20261030 18:59 |
| S7 | Anthropic, "Effective context engineering for AI agents", 20250929 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 20261030 18:59 |
| S8 | Graphify README and LICENSE | https://github.com/Graphify-Labs/graphify | 20261030 19:00 |
| S9 | Kuzu README (archive notice) | https://github.com/kuzudb/kuzu | 20261030 19:00 |
| S10 | Karpathy, "LLM Wiki" gist | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f | 20261030 19:01 |
| S11 | MCP specification repository, release list | https://api.github.com/repos/modelcontextprotocol/modelcontextprotocol/releases | 20261030 19:01 |
| S12 | `microsoft/graphrag` release list and v3.0.0 notes | https://github.com/microsoft/graphrag/releases | 20261030 19:01 and 19:02 |
| S13 | `getzep/zep` README | https://github.com/getzep/zep | 20261030 19:01 |
| S14 | OKF agent memory README, OKF v0.2 specification, Knowledge Catalog README | https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md and https://github.com/okf-memory/okf-agent-memory | 20261030 19:01 to 19:03 |
| S15 | Aider, "Building a better repository map with tree sitter", 20231022 | https://aider.chat/2023/10/22/repomap.html | 20261030 19:01 |
| S16 | Anthropic, context management and memory tool, 20250929 | https://claude.com/blog/context-management | 20261030 19:02 |
| S17 | Simon Willison, "Context engineering", 20250627 | https://simonwillison.net/2025/Jun/27/context-engineering/ | 20261030 19:02 |
| S18 | MCP `2026-07-28` release notes and changelog | https://modelcontextprotocol.io/specification/2026-07-28/changelog | 20261030 19:02 and 19:04 |
| S19 | MCP repository LICENSE (MIT to Apache-2.0 transition) | https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/LICENSE | 20261030 19:02 |
| S20 | READMEs of codebase-memory-mcp, OpenViking (with LICENSE and its commit log), Hindsight, Mem0, LightRAG | https://github.com/DeusData/codebase-memory-mcp , https://github.com/volcengine/OpenViking , https://github.com/vectorize-io/hindsight , https://github.com/mem0ai/mem0 , https://github.com/HKUDS/LightRAG | 20261030 19:03 |
| S21 | BetaKit, Apple and Kuzu, published 20260212 | https://betakit.com/apple-strikes-deal-to-acquire-canadian-database-software-startup-kuzu/ | 20261030 19:03 |
| S22 | Microsoft Research, "GraphRAG: new tool for complex data discovery now on GitHub", 20240702 | https://www.microsoft.com/en-us/research/blog/graphrag-new-tool-for-complex-data-discovery-now-on-github/ | 20261030 19:03 |
| S23 | Anthropic, Agent Skills, 20251016 (updated 20251218) | https://claude.com/blog/skills | 20261030 19:04 |
| S24 | arXiv abstracts (first 900 characters) of 2506.05690, 2502.11371, 2504.19413, 2501.13956, 2601.02553, 2512.13564, 2501.09136 | https://export.arxiv.org/api/query | 20261030 19:02 |
| S25 | `getzep/zep` commit log (messages matching "deprecat", "community edition", "archive") | https://api.github.com/repos/getzep/zep/commits | 20261030 19:02 |
| S26 | `letta-ai/letta` release list (three newest) | https://api.github.com/repos/letta-ai/letta/releases | 20261030 19:02 |
