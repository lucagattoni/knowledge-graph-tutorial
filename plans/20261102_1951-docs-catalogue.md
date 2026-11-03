# Catalogue for the new documentation

**Status: decided by the main session under the owner's delegation of 20261102 ("I trust you, create the entire
documentation right now"), written 20261102 19:51 UTC.** Each list below is final for the first edition; a
later change is a dated row in the chapter's `changes.tsv`. The evidence behind each decision is named; writers
re-verify every load-bearing fact against the primary source (spec section 6).

## Chapter 1: eras

Derived from the sources' shared boundary points. No source gives one scheme for all four threads or for
the whole span; the scheme below is this documentation's, built from the points that at least two sources
share, and the era pages say so. Where the sources disagree on a date, the page shows both.

Sources most used (all read 20261102 between 19:22 and 19:43 UTC by the eras researcher; writers re-read
what they cite):

| Id | Source | URL |
|---|---|---|
| S3 | Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: five periods (Advent, Foundations, Coming-of-Age, Web, Large Scale) | https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf |
| S4 | Hogan et al., "Knowledge Graphs", ACM Computing Surveys 54(4), arXiv 2003.02320 v6: Appendix A (history) | https://arxiv.org/pdf/2003.02320v6 |
| S5 | Gao et al., RAG survey, arXiv 2312.10997 | https://arxiv.org/pdf/2312.10997 |
| S6 | Hu et al., "Memory in the Age of AI Agents", arXiv 2512.13564 | https://arxiv.org/pdf/2512.13564 |
| S7 | Stonebraker and Pavlo, "What Goes Around Comes Around... And Around...", SIGMOD Record 53(2), 2024 | https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf |
| S8 | Codd, "A Relational Model of Data for Large Shared Data Banks", CACM 13(6), 1970 | https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf |
| S9 | Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE 100, 2012 | https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 |
| S10 | Lin, Nogueira, Yates, "Pretrained Transformers for Text Ranking: BERT and Beyond", arXiv 2010.06467 | https://arxiv.org/pdf/2010.06467 |
| S11 | McCarthy et al., Dartmouth proposal, 1955 | http://jmc.stanford.edu/articles/dartmouth/dartmouth.pdf |
| S12 | Sowa, "Semantic Networks" | https://www.jfsowa.com/pubs/semnet.htm |
| S13 | Stanford AI100 (2016), Appendix I, "A Short History of AI" | https://ai100.stanford.edu/2016-report/appendix-i-short-history-ai |
| S14 | Hitzler, "A Review of the Semantic Web Field", CACM 64(2), 2021: three phases | https://par.nsf.gov/servlets/purl/10292869 |
| S15 | Shadbolt, "Expert systems: a natural history", 1989 | https://eprints.soton.ac.uk/252374/1/A_Natural_History_of_Expert_Systems_1989.pdf |
| S16 | W3C Recommendation pages (RDF 1999 and 2004, OWL 2004, SPARQL 2008, SKOS 2009, OWL 2 2009/2012, SPARQL 1.1 2013, RDF 1.1 2014, SHACL 2017, JSON-LD; RDF 1.2, SPARQL 1.2, SHACL 1.2 drafts of 2026; the Semantic Web Activity page; Linked Data design note 2006) | https://www.w3.org/TR/ and https://www.w3.org/DesignIssues/LinkedData.html |
| S17 | Singhal, "Introducing the Knowledge Graph: things, not strings", Google, 20120516 | https://blog.google/products/search/introducing-knowledge-graph-things-not/ |
| S18 | Singh et al., Agentic RAG survey, arXiv 2501.09136 | https://arxiv.org/abs/2501.09136 |
| S19 | Pan et al., "Unifying Large Language Models and Knowledge Graphs: A Roadmap", arXiv 2306.08302 | https://arxiv.org/abs/2306.08302 |
| S21 | GQL standards committee page | https://www.gqlstandards.org/ |
| S22 | Feigenbaum, "The Art of Artificial Intelligence", IJCAI-77 | https://www.ijcai.org/Proceedings/77-2/Papers/092.pdf |
| S23 | Angles and Gutierrez, "Survey of Graph Database Models", ACM Computing Surveys 40(1), 2008 | https://users.dcc.uchile.cl/~cgutierr/papers/surveyGDB.pdf |

Independence: S3, S4 and S23 share an author. For knowledge and AI before 2010 the independent sources are
S12, S13, S14, S15, S22; for databases and search S7, S9, S10.

| Order | Slug | Title | Period | Starts because (shared point and sources) | Ends because |
|---|---|---|---|---|---|
| 1 | `advent` | The advent: machines that hold knowledge | 1950-1969 | "information retrieval" coined March 1950 (S9); the AI proposal of 1955 and the 1956 workshop (S11, S13); "semantic network" first used 1956 (S12, S3, S4) | the 1970s bring formal foundations for both data and knowledge (next row) |
| 2 | `formal-foundations` | Formal foundations | 1970-1979 | Codd's relational model, June 1970 (S8, S7, S3); S3's period "The 1970s"; frames 1974, Woods 1975, Brachman 1977 (S3, S4); idf 1972, vector space model 1975, probability ranking 1977 (S9) | expert systems become "a distinct line around the late 70's" (S15) and description logics start (1979-1985: S12, S3, S4) |
| 3 | `knowledge-systems` | Knowledge systems: boom and bust | 1980-1992 | S3's period "The 1980s"; XCON 1980, shells from 1979, national programmes 1981-1982 (S15); description logics (S12, S3, S4) | the Web enters data and search from 1993 (next row). The bust's date is disputed: mid-1980s (S13) against the beginning of the 1990s (S3); show both |
| 4 | `the-web` | The Web changes data and search | 1993-2000 | web search engines from late 1993 (S9); S3's period "The 1990s"; semi-structured data late 1990s (S7); first RDF draft 1997 and RDF Recommendation 19990222 (S14, S16) | the Semantic Web article of May 2001 "arguably marks the birth of the field" (S14; also S3, S12) |
| 5 | `semantic-web` | The semantic web and linked data | 2001-2011 | the 2001 article (S14, S3, S12); OWL and RDF 1.0 Recommendations 20040210 (S16); Linked Data 20060727 (S16); SPARQL 20080115 (S16); S14's phases "ontologies" then "Linked Data" | Google's Knowledge Graph 20120516, "a watershed moment" for the phrase (S17, S4) and the start of S14's third phase; schema.org 2011 and Wikidata 2012 (S14, S3) |
| 6 | `knowledge-graphs-at-scale` | Knowledge graphs at scale | 2012-2017 | as above | BERT, October 2018, which S10 treats as separating two "eras" of ranking; pretrained transformers lead to retrieval-augmented language models (S5, S19) |
| 7 | `language-models-meet-retrieval` | Language models meet retrieval | 2018-2022 | BERT 2018 (S10); REALM 20200210 and RAG 20200522 (arXiv, S19, S5) | ChatGPT, late 2022, "a pivotal moment" after which "Naive RAG" "gained prominence" (S5; S7 says "late 2022"; its exact date is unstated in the pages read: fetch OpenAI's announcement or a dated primary record) |
| 8 | `settled-since-2023` | What has settled since 2023 | 2023-present | only what became a standard or common practice after ChatGPT, under the owner's rule; for example GQL, ISO/IEC 39075, published 20240417 (S21), and SQL/PGQ in SQL:2023 (S7) | open: when a chapter 2 trend settles, it moves here with a dated change row |

Rules for the era writers:
- Chapter 1 holds what is settled: it became a standard, was absorbed into common practice, or was replaced by
  a successor. An item still moving (for example graph-based RAG, agent memory, the 2026 drafts of RDF 1.2,
  SPARQL 1.2 and SHACL 1.2) is named in one line with a link to chapter 2 (`../trends/README.md`), not told.
- Each era page covers the four threads where something happened: KB/KG (main), ontologies and the semantic
  web, databases and search, RAG and agent memory.
- Disagreements found by the research go into "Ideas and disputes": the expert-system bust date; the first use
  of "knowledge graph" (1972 versus 1973 inside S4; Bakker 1987 per S3); RDF's first standard (1999 versus
  2004); KL-ONE and description logics (1979, 1984, 1985); conceptual graphs (1976 versus 1979); Cyc's start year
  (unstated in the pages read; S4 says "since 1986"); what "naive RAG" means (S5 versus S18); whether dense
  retrieval replaced sparse (S7 versus S10, S5, S18); the fate of graph databases (S23 versus S7); whether
  ontologies "worked" (S14 versus S3); whether "knowledge graph" is a new idea or a reframing (S14, S3 versus S4).

## Chapter 2: trends

Decided 20261102 at about 20:25 UTC from the trends researcher's evidence (arXiv API counts in the window
20251102 to 20261102 against the year before, read 20261102 19:26 to 19:47 UTC; the GitHub snapshot of 20261030
19:54 UTC; READMEs read 19:37 to 19:52 UTC). Tests (decision T-3): **1, sustained activity** (active projects in the
snapshot, or a rising count of on-topic papers in the window; counts are keyword hits and noisy; growth is
compared with the controls: any LLM wording x1.38, any RAG wording x1.23, LLM-agent wording x2.50); **2,
distinctness** (what is built or stored, when a model is used, who steers retrieval, against the nearest
neighbour). Status values: `growing` (activity rising faster than the controls), `steady` (sustained near them),
`settling` (parts became standard or were absorbed).

| Order | Slug | Title (family: from X to Y) | Status | Test 1 evidence | Nearest neighbour and the difference | Merged in |
|---|---|---|---|---|---|---|
| 1 | `graph-based-rag` | Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones | steady | 20 active repos (LightRAG 40,443 stars; Microsoft GraphRAG 36,498); family papers 272 against 167 (x1.63); the GraphRAG README has said "largely in maintenance mode" since 20260814 | `llm-kg-construction` (same extraction step, but here the graph is an index for answering) and `code-knowledge-graphs` (graph built by a parser) | cheaper or lazy construction (LazyGraphRAG, LinearRAG, LLM-free graphs); multimodal graph RAG (LightRAG news "[2026.05] Merge RagAnything into LightRAG"); hypergraph variants |
| 2 | `llm-kg-construction` | Building knowledge graphs with LLMs: from fixed schemas to induced ones | steady | 75 papers against 64 (x1.2); 9 active repos, several ontology-first ones created in 2026 | `graph-based-rag`: the output is the typed graph or ontology as an asset, judged against human schemas | schema and ontology induction; ontology-grounded context graphs |
| 3 | `graph-query-generation` | Asking graphs in natural language: from hand-written queries to model-written Cypher and SPARQL | steady | 52 papers against 38 (x1.4); a named Text2Cypher retriever in Neo4j's GraphRAG package | `learned-graph-traversal`: translate once and let the engine execute, instead of a model walking the graph | text-to-SPARQL challenges |
| 4 | `learned-graph-traversal` | Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal | growing (papers only) | 44 papers against 18 (x2.4, about the agent control); no active project: every repository is quiet | `reasoning-over-structure`: a trained policy walks a graph, against a prompted model over a document tree | reinforcement-learned controllers for retrieval and memory operations |
| 5 | `reasoning-over-structure` | Vectorless retrieval: from similarity search to a model reasoning over a document tree | growing | PageIndex 39,913 stars, pushed the day of the snapshot; 19 papers against 4 (small base); RAGFlow's "Knowledge Compilation" (20260819) generates trees and PageIndex outputs | `plain-file-knowledge` (a model reads an index of pages) and `agentic-search` (nothing is built) | — |
| 6 | `agentic-search` | Agentic search over raw data: from building structure to letting the agent search | growing (papers only) | probe 151 against 26 (noisy); independent 2026 studies put raw retrieval or grep level with or ahead of built structures; no snapshot project matches (unstated) | `reasoning-over-structure` (a tree is built) and `code-knowledge-graphs` (grep against a graph) | — |
| 7 | `agent-memory` | Agent memory: from retrieving documents to remembering across sessions | growing | about 117 active repos (claude-mem 105,979; mem0 68,112; hindsight 56,614); 482 papers against 53 (x9.1) | `plain-file-knowledge` (memory kept as files) and `graph-based-rag` ("From RAG to Memory") | temporal knowledge graphs (Graphiti); write policies; governed and attackable memory (governance and provenance papers x8, poisoning and injection x15) |
| 8 | `plain-file-knowledge` | Plain files as agent knowledge: from databases and indexes to Markdown the model maintains | growing | "LLM wiki" papers 21 against 0; context-file papers (AGENTS.md, CLAUDE.md) 59 against 2; of 48 repos of the April 2026 wave, 20 still active | `agent-memory` (memory layers store extracted records) and `reasoning-over-structure` (the model reads index.md, then pages) | LLM wikis (Karpathy gist 20260404); context files; skills as procedural knowledge; knowledge compilation in products; the OKF format |
| 9 | `code-knowledge-graphs` | Code graphs for coding agents: from grep and file reads to parsed code graphs | growing | 28 active repos, four flagged fast-growth (Graphify 139,374; Understand-Anything 89,048; codegraph 76,004; codebase-memory-mcp 47,853); papers 13 against 1 | `graph-based-rag` (graph without an LLM) and `agentic-search` (grep) | — |
| 10 | `infrastructure-and-mcp` | Infrastructure and MCP: what knowledge systems run on, and how agents reach them | steady | theme chosen by the owner (T-2) | — | graph databases and their standards (GQL 2024, SQL/PGQ 2023); vector indexes in relational databases; MCP; RAG platforms |
| 11 | `features-in-and-out` | Graph features removed and added | steady | theme chosen by the owner (T-2) | — | dated removals and additions (Mem0's graph store, GraphRAG maintenance mode, LightRAG's merges, Kuzu archived and deprecated by Graphiti, licence moves tied to hosted features) |

Not trends of their own: temporal KGs (fails test 2 alone: time is a design axis of all memory, so a section of
`agent-memory`); multimodal graph RAG (absorbed into LightRAG); skills and knowledge compilation (sections of
`plain-file-knowledge`); evaluation and licensing (columns of the comparison table and a section in every trend,
decision T-6).

Candidate fundamental papers per trend (the papers chapter decides): see the trends researcher's evidence,
section 4 of each candidate; and the papers pool of wave 1.

Experiments that test a trend (link them from the trend page): X2 index cost and X3 matched-cost comparison:
`graph-based-rag` (X3 also `reasoning-over-structure`); X4 code graph against grep: `code-knowledge-graphs` and
`agentic-search`; X5 wiki size limit: `plain-file-knowledge`.

## Chapter 3: projects with a page

Test P-1, applied 20261102: **sustained activity** (pushed within 90 days of the 20261030 19:54 UTC snapshot, not
archived; 63 of the 77 archive projects pass) **and** use by a trend as a representative of a distinct approach.
Quiet research code (Graph-R1, Youtu-GraphRAG, LinearRAG, LogicRAG, MiniRAG, fast-graphrag, nano-graphrag, KAG,
A-mem, datastax graph-rag, DeepKE, OpenKB, karpathy-llm-wiki) and the archived Kuzu stay in the watch list and are
told through their trend and their papers.

| Trend | Project pages (archive slugs) |
|---|---|
| `graph-based-rag` | `microsoft-graphrag`, `lightrag`, `hipporag`, `rag-anything`, `graphrag-sdk`, `neo4j-graphrag-python` (also `graph-query-generation`) |
| `llm-kg-construction` | `llm-graph-builder` (pushed 1 day before the snapshot but 1 commit in 90 days: say so), `hyper-extract`, `gliner`, `ontogpt` |
| `reasoning-over-structure` | `pageindex`, `ragflow` (also `infrastructure-and-mcp`) |
| `agent-memory` | `mem0`, `hindsight`, `graphiti`, `cognee`, `letta`, `mirix`, `openviking` (also `plain-file-knowledge`), `claude-mem`, `memos` |
| `plain-file-knowledge` | `llm-wiki-nashsu`, `claude-obsidian`, `basic-memory`, `tigerless-agent-memory` |
| `code-knowledge-graphs` | `graphify`, `understand-anything`, `codegraph`, `codebase-memory-mcp`, `code-review-graph`, `code-graph-rag` (also `graph-query-generation`) |
| `infrastructure-and-mcp` | `neo4j`, `falkordb`, `memgraph`, `mcp-servers`, `llama-index`, `dify` |

37 pages. `learned-graph-traversal` and `agentic-search` have no project page (no active project passes). The watch
list (`docs/projects/watchlist.tsv`) holds all 77 archive projects and the in-scope repositories the trends research
found, each tagged with its trends.

## Chapter 4: papers

**Later change (20261102, about 23:15 UTC):** an independent audit found papers in this list that pass none of the four tests, and origin claims made without a search for earlier work. A fixer searched, and moved 14 papers to the groups' further reading with a stated reason each; the chapter now holds 68 fundamental papers. The final list is the chapter itself (`docs/papers/README.md`); the table below is the list as first decided.

Decided 20261102 at about 20:45 UTC from wave 1's five candidate pools (the tests of decision R-1; citation counts
from Semantic Scholar, OpenAlex or Crossref as each pool records, read 20261102 between 19:50 and 20:20 UTC). "Only
the really fundamental ones": a paper is listed when it passes a test **and** a reader of the chapter would miss it;
everything else that passed a test goes to "Further reading" of its group.

Rules:
- A paper whose main contribution is a dataset or a benchmark (HotpotQA, WebQuestions, FB15k-237, LoCoMo,
  LongMemEval, Text2KGBench) lives in chapters 5 and 6; the papers chapter names it in relation lines only. An
  evaluation study that reports a finding (GraphRAG-Bench "When to use graphs", RAG vs GraphRAG, BM25 Wins at Scale)
  is a paper.
- Standards (W3C, ISO) are index entries of kind standard, not papers.
- Blog posts and gists (LazyGraphRAG, the LLM Wiki gist, Aider's repository map, Anthropic's context-engineering post)
  are not papers; a group names them in its introduction when they are the origin of the line of work.
- Citation counts are carried over from the pools with their source and read time (the APIs rate-limited on
  20261102); a count is never compared across sources.

| Group | Fundamental papers (short name, year, id) | Further reading (at least) |
|---|---|---|
| `foundations` | **Quillian 1967** (semantic memory, doi 10.1002/bs.3830120511); **Codd 1970** (relational model); **Sparck Jones 1972** (idf); **Minsky 1974** (frames); **Woods 1975** (What's in a link); **Salton, Wong, Yang 1975** (vector space model); **Feigenbaum 1977** (knowledge engineering); **Brachman and Schmolze 1985** (KL-ONE); **Lenat et al. 1985** (Cyc); **Gruber 1993** (ontology); **Miller 1995** (WordNet; or Miller 1990, as the pool records); **Brin and Page 1998** (PageRank); **Robertson and Zaragoza 2009** (BM25 and the probabilistic relevance framework; the writer checks the pool, else Robertson et al. 1994, Okapi at TREC-3); **Berners-Lee, Hendler, Lassila 2001** (Semantic Web); **Auer et al. 2007** (DBpedia); **Suchanek et al. 2007** (YAGO); **Bollacker et al. 2008** (Freebase); **Bizer, Heath, Berners-Lee 2009** (Linked Data); **Bordes et al. 2013** (TransE); **Vrandecic and Kroetzsch 2014** (Wikidata); **Dong et al. 2014** (Knowledge Vault); **Francis et al. 2018** (Cypher); **Petroni et al. 2019** (LAMA, language models as knowledge bases); **Karpukhin et al. 2020** (DPR); **Guu et al. 2020** (REALM); **Lewis et al. 2020** (RAG); **Hogan et al. 2021** (Knowledge Graphs, arXiv 2003.02320); **Gao et al. 2023** (RAG survey, 2312.10997) | Robertson and Sparck Jones 1976; Luhn 1957; Maron and Kuhns 1960; Chen 1976; Newell 1982; Brachman and Levesque 1984; Banko et al. 2007 (Open IE); Carlson et al. 2010 (NELL); Angles and Gutierrez 2008; Ehrlinger and Woess 2016; Wang et al. 2017 (embedding survey); Schlichtkrull et al. 2017 (R-GCN); Yih et al. 2015 (STAGG); Borgeaud et al. 2021 (RETRO) |
| `graph-based-rag` | GraphRAG (2404.16130); LightRAG (2410.05779); HippoRAG (2405.14831); HippoRAG 2 (2502.14802); G-Retriever (2402.07630); KAG (2409.13731); Peng et al. GraphRAG survey (2408.08921); RAG vs GraphRAG (2502.11371); GraphRAG-Bench, "When to use graphs in RAG" (2506.05690); LinearRAG (2510.10114); RAG-Anything (2510.12323); BM25 Wins at Scale (2607.26497); RAGSearch (2604.09666) | Is GraphRAG Needed? (2606.25656); KET-RAG (2502.09304); MiniRAG (2501.06713); EffiRAG (2609.18099); Geometric Gain Graph (2609.19622); PathRAG; HyperGraphRAG |
| `llm-kg-construction` | Language Models are Open Knowledge Graphs (2010.11967); Pan et al., Unifying LLMs and KGs: a roadmap (2306.08302); Zhu et al., LLMs for KG construction and reasoning (2305.13168); EDC (2404.03868); AutoSchemaKG (2505.23628); Bian, LLM-empowered KG construction survey (2510.20345) | KGGen (2502.09956); Are LLMs effective KG constructors? (2510.11297); DIAL-KG (2603.20059); OntoKG (2604.02618) |
| `graph-query-generation` | Text2Cypher (2412.10064, as the LLM-era framing of the task; its data has pages in chapters 5 and 6); Text2Cypher across languages (2506.21445) if it passes a test; SPARQL-LLM (2512.14277) if it passes a test. At least two | SAGA (2607.14494); KG2Cypher (2606.27742); CypherGuard (2610.41755) |
| `learned-graph-traversal` | Knowledge Graph Prompting (2308.11730); Think-on-Graph (2307.07697); Search-R1 (2503.09516, the plain-text baseline); Graph-R1 (2507.21892); GraphRAG-R1 (2507.23581); Memory-R1 (2508.19828, reinforcement-learned memory operations) | GraphSearch (2509.22009); GraphWalker (2603.28533); PathRouter (2606.16409); Search-on-Graph-R1 (2607.18481) |
| `reasoning-over-structure` | RAPTOR (2401.18059, the tree-structured ancestor, with embeddings); LogicRAG, "You don't need pre-built graphs for RAG" (2508.06105); Lumer et al. (2511.18177); the RAGFlow-team study (2610.41172) if it passes a test | RIT-RAG (2610.11370); DecisionRAG (2610.35868) |
| `agentic-search` | ReAct (2210.03629); IRCoT (2212.10509); Self-RAG (2310.11511); Lost in the Middle (2307.03172); RAG or long-context LLMs (2407.16833); Is Grep All You Need? (2605.15184); ReFind (2608.12888) | Cache-Augmented Generation (2412.15605); Retrieval meets long context (2310.03025) |
| `agent-memory` | Generative Agents (2304.03442); MemGPT (2310.08560); CoALA (2309.02427); Zhang et al. memory survey (2404.13501); Zep (2501.13956); Mem0 (2504.19413); A-MEM (2502.12110); Hu et al., Memory in the Age of AI Agents (2512.13564); Bao et al., Naive RAG is stronger than we thought / Is complex agentic memory always needed? (2610.30755; give both titles and say which the arXiv record shows now) | MemoryBank (2305.10250); MemOS (2507.03724); Hindsight (2512.12818); Memory Tax (2610.34073); agent-native memory study (2606.24775); Bi-Temporal Memory Engine (2606.09900) |
| `plain-file-knowledge` | No founding paper: the founding text is a gist (20260404). Papers: the first on-topic papers of April 2026 (2604.11243 or 2604.12034, whichever passes origin); Single-round vector RAG against an LLM-compiled wiki (2605.18490); Filesystem-based memory for LLM agents (2607.26637). At least two | Progressive disclosure for LLM-maintained wikis (2607.04576); WikiSkill (2608.27454); 2512.05470 |
| `code-knowledge-graphs` | CodexGraph (2408.03910); RepoGraph (2410.14684); Codebase-Memory (2603.27277); AST-derived against LLM-extracted code graphs (2601.08773); How small coding agents use code graphs and embeddings (2610.33958) | RepoAtlas (2609.16936); LARGER (2605.16352) |

The two theme subchapters have no paper group; their papers (Cypher, the graph-database survey) are in
`foundations` or further reading.

## Chapter 5: datasets, and chapter 6: benchmarks

Decided 20261102 at about 20:45 UTC from wave 1's four pools (decisions D-1 to D-4, B-1). Selection (D-3): used by a
fundamental paper, used by a trend, or widely used (citation count of its paper, from a named source with its read
time). Split (D-2): an item gets **both** a dataset page and a benchmark page when its data is used beyond its own
protocol and it also defines an evaluation; a **benchmark-first** item (its data is used only inside its own protocol)
gets a benchmark page whose "Datasets" section describes its data; nothing is repeated between two pages. Pages of
one item share the slug in the two folders.

| Writer task | Dataset pages (`docs/datasets/`) | Benchmark pages (`docs/benchmarks/`) |
|---|---|---|
| 1 | `hotpotqa` | `hotpotqa` |
| 2 | `natural-questions` | `natural-questions` |
| 3 | `musique` | `musique` |
| 4 | `2wikimultihopqa` | `2wikimultihopqa` |
| 5 | `multihop-rag` | `multihop-rag` |
| 6 | `longmemeval` | `longmemeval` |
| 7 | `locomo` | `locomo` |
| 8 | `webquestionssp` | `webquestionssp` |
| 9 | `lc-quad` (LC-QuAD 1.0 and 2.0) | `lc-quad` |
| 10 | `ms-marco` | `ms-marco` |
| 11 | `fb15k-237`, `wn18rr` (each naming FB15k and WN18 as the predecessors withdrawn for test leakage) | `kg-link-prediction` (the filtered link-prediction protocol on FB15k-237, WN18RR, YAGO3-10) |
| 12 | `wikidata`, `freebase` | |
| 13 | `dbpedia`, `yago` | |
| 14 | `conceptnet`, `wordnet` | |
| 15 | `triviaqa`, `popqa` | |
| 16 | `simplequestions`, `complexwebquestions` | |
| 17 | `metaqa`, `grailqa` | |
| 18 | `wikipedia-dpr-kilt` (the Wikipedia snapshots used by DPR and KILT) | `kilt` |
| 19 | | `beir`, `frames` |
| 20 | | `crag`, `stark` |
| 21 | | `graphrag-bench-xiang`, `graphrag-bench-xiao` (two unrelated benchmarks with one name) |
| 22 | | `enterpriserag-bench`, `ragsearch` |
| 23 | `ultradomain` | `memoryagentbench` |
| 24 | | `text2kgbench`, `text2cypher` |
| 25 | | `ogb-link-prediction` (ogbl-wikikg2) |

26 dataset pages and 24 benchmark pages. Kinds on the datasets landing: knowledge graphs (`wikidata`, `dbpedia`,
`yago`, `freebase`, `conceptnet`, `wordnet`, `fb15k-237`, `wn18rr`); question sets (the rest except the corpora);
corpora (`wikipedia-dpr-kilt`; `ultradomain` is questions and corpus; `ms-marco` is questions and passages).
Considered and left to further mention: FB15k and WN18 (inside the pages above), YAGO3-10, Wikidata5M, CoDEx,
LoCoMo-Plus, AMA-Bench, EvoMemBench, WildGraphBench, Text2GraphQuery-Bench, CypherTurn, the TEXT2SPARQL challenge.

## The owner's review of the lists (20261103)

The owner went through all six lists with the assistant on 20261103, after the first edition was merged (decision D-33 in
`DECISIONS.md`). The lists above are approved except where this section changes them; each change is a dated row in the
chapter's `changes.tsv`.

| Chapter | The owner's decision | Change |
|---|---|---|
| 1, eras | Keep the eight eras and their boundaries | none |
| 2, trends | Keep all nine families and both themes, including the two that rest on paper counts alone (agentic graph retrieval, agentic search over raw data). The RDF 1.2, SPARQL 1.2 and SHACL 1.2 drafts were told nowhere though about ten pages pointed to the trends for them | **A new trend page, `semantic-web-standards`** (a tenth family; the themes move to orders 11 and 12) |
| 3, projects | 26 active projects had no page and no stated reason | **Five new pages** (supermemory, TencentDB-Agent-Memory, Memori, memU, EverOS, all agent memory; 42 pages in all) and a stated reason in the watch list for each of the other 21 |
| 4, papers | Keep the two one-paper groups (Text2Cypher; Knowledge Compounding). Keep the WordNet, YAGO, DBpedia, Freebase and Wikidata papers in Foundations | The papers chapter's rule names the exception |
| 5 and 6, datasets and benchmarks | Keep both lists; none of the considered items gets a page | none |

Answered later the same day, after the first part was merged (PR 2), on four open cases the first part left:

| Case | The owner's decision | Change |
|---|---|---|
| Open Knowledge Format: listed by the plain-files trend as a representative, but a specification with no project page | A sentence in the Projects chapter, no page | The chapter says why it has no page; its watch-list note records the decision |
| Semantica: 14,349 stars, no page, not named in the construction trend's section on ontology-grounded context graphs | A page, and name it in the trend | `docs/projects/semantica.md` (43 project pages in all); the trend names it |
| The Papers chapter has no group for the new trend (its table says one group per trend) | Add a group (the owner chose it over stating an exception) | `docs/papers/semantic-web-standards.md`: five papers by the same four tests, thirteen in further reading (73 papers in 11 groups) |
| The six new project pages run 1,200 to 1,550 words against the 500 to 900 target | Leave them | Listed under "Known limits" in `20261102_1935-docs-build-resume.md` |
