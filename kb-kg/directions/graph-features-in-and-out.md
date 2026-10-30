# Where graph features are being removed, and where they are being added

**In one paragraph.** Across the 21 entries covered here, eight record a dated act that removes, deprecates, archives or demotes a graph feature or a graph database, and about ten ship new graph-related features. Four of the eight removals come with a reason from the project; the other four state none. Where a reason is given, it concerns the project or its company (maintenance, a successor product, an unmaintained dependency), not a measured weakness of graphs. Several removals relocate a feature to a hosted tier or rename it, and most additions have no evaluation. No source read here is an independent evaluation of any single removal or addition.

## What the direction claims

No project states this as a direction. Each states only its own change, and this page puts the changes side by side. Terms used below:

- **Removed or deprecated:** code or an option deleted, or marked for deletion.
- **Demoted:** moved to an experimental namespace, an integration repository, a hosted-only tier, "maintenance mode" or a successor product.
- **Added:** a graph-related capability shipped since the entries were written, or placed on a stated roadmap.
- **Stated reason:** the project's own words, quoted. Anything else is **unstated**, or is marked **Reading** (my interpretation).

## Who is doing it

### Removed, deprecated, archived or demoted (dated acts)

| Project | What changed | Reason the project gives | Status at 20261030 | Evidence on the feature, and who measured |
|---|---|---|---|---|
| [Mem0](../projects/mem0.md) | 20260414, Python 2.0.0: external graph store deleted from open source (about 4,000 lines per the migration guide). A built-in Graph Memory stays on the Platform; it assigns no typed relationships | Unstated. The migration guide gives none and says the feature "is not being replaced by an OSS equivalent" [S1]. The April 2026 post does not mention graphs [S4] | Active; no release after 20260925 | Mem0's own paper: graph variant 68.44 against 66.88 for the base (+1.56), lower on single-hop and multi-hop. It concerns the deleted feature |
| [RAGFlow](../projects/ragflow.md) | v0.27.0, 20260819: GraphRAG and RAPTOR "deprecated and are no longer available in the UI"; "Graph and Tree" in Knowledge Compilation replace them; old content stays searchable | Unstated [S2] | Active; v1.0.0-rc3 20261030 | None in the entry |
| [Microsoft GraphRAG](../projects/microsoft-graphrag.md) | README notice of 20260814: "largely in maintenance mode", no new features or pull requests; bug fixes and CVE patches continue. LazyGraphRAG request closed "not planned" 20251118 | Quoted: "the capabilities of frontier models have changed dramatically" since July 2024, and the "portfolio of research projects has diversified" | v3.3.0, 20261008; not archived | Authors' paper and blog claims; no third-party evaluation read |
| [Graphiti](../projects/graphiti.md) | Kuzu driver deprecated in v0.29.2 (20260608); README: Kuzu "will be removed in a future release" | README: the upstream Kuzu project "is no longer maintained" | v0.31.2, 20261020 | Not applicable (database support) |
| [Kuzu](../projects/kuzu.md) | Repository archived 20251010; README: "working on something new" | Unstated. BetaKit reports an Apple purchase agreement of 20251009 and says Apple's motivation is unclear | Archived; fork Ladybug active | Not applicable |
| [LLM Graph Builder](../projects/llm-graph-builder.md) | Banner merged 20261016: "no longer actively developed, instead use Neo4j Document Intelligence in Aura"; Labs disclaimer 20261022 | A successor is named; Neo4j calls it "the next step" (summarised page). Why: unstated | v0.8.7, 20260723; small fixes continue | None found |
| [Zep](../projects/zep.md) | 20250402: server (Community Edition) no longer maintained; the repository now holds samples for Zep Cloud | Vendor's blog, read through a summary: open-core compromises and under-investment | Active as a samples repository | Not applicable |
| [Cognee](../projects/cognee.md) | v1.6.3, 20261007: `temporal_cognify` option removed (code keeps it as deprecated and ignored); dates become `Timestamp` nodes | Unstated. The notes list a breaking change and no reason [S3] | v1.6.6, 20261029 | Cognee's own reports only |

### Quiet repositories (no stated decision)

| Project | Observation | Reason | Status |
|---|---|---|---|
| [fast-graphrag](../projects/fast-graphrag.md) | Last push 20251101; last code change 20250621 | Unstated; the company's newest repositories are a browser agent | Not archived |
| [nano-graphrag](../projects/nano-graphrag.md) | Last push 20260127 | Unstated | Not archived |
| [datastax/graph-rag](../projects/datastax-graph-rag.md) | No commit since 20250505; a contributor wrote "i no longer have write access to this repo" | Unstated; whether the IBM acquisition caused it is unstated | Not archived |

### Added or extended

| Project | What was added | Reason the project gives | Evidence, and who measured |
|---|---|---|---|
| [Cognee](../projects/cognee.md) | LLM-free GLiNER extraction (20260913); opt-in OWL-RL reasoning (20261026); conflict-resolution API (20261029) | Unstated | Own BEAM and LoCoMo reports; none independent |
| [Graphiti](../projects/graphiti.md) | Combined extraction (v0.31.0, 20261014); "C2" prompt default; `GLiNER2Client`; embedded FalkorDB | Pull request 1964: moves improvements from Zep's internal fork upstream, without the features Zep keeps behind flags | Zep's internal evaluation: F1 0.638 against 0.628, which the pull request calls "inside the noise" |
| [Dify](../projects/dify.md) | 1.18.0, 20261023: Agent Knowledge Base, opt-in beta; docs and UI strings say it builds a knowledge graph at indexing; backend is a separate private repository | Unstated | None |
| [RAGFlow](../projects/ragflow.md) | Knowledge Compilation: Graph, Tree, PageIndex, Mindmap, Timeline, Wiki | Unstated | None |
| [Haystack](../projects/haystack.md) | In its integrations repository: FalkorDB text-to-Cypher retriever (documented 20261029), Cognee memory store; core has no graph component (path names only) | Unstated | None |
| [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md) | 1.23.0, 20261028; pipeline observers (1.20.0); builder still in the `experimental` namespace | Unstated | None |
| [TrustGraph](../projects/trustgraph.md) | Ontology RAG; SHACL and SPARQL access policies (v2.10 or later, CLI loading only) | Unstated | Ingest-speed figures only |
| [Semantica](../projects/semantica.md) | Bi-temporal facts, OWL and SHACL, W3C PROV-O provenance | Unstated | Authors' performance table only |
| [GraphRAG SDK](../projects/graphrag-sdk.md) | README roadmap: Agentic GraphRAG for 2026-Q3, dynamic traversal and temporal graph for Q4; agentic work still open | Unstated | Own score 71.48 against 55.39 for vector RAG; I could not check the rows |
| [M-flow](../projects/m-flow.md) | Graph, not vector similarity, decides relevance; KùzuDB listed among backends | Unstated | Own LoCoMo-10 score 81.8% against 79.4% for Cognee Cloud |

### No graph feature in the entry, or no change found

| Project | Observation |
|---|---|
| [LlamaIndex](../projects/llama-index.md) | `PropertyGraphIndex` is documented; guide last changed 20260720. README: "primary focus has shifted towards LlamaParse" (not graph-specific) |
| [AnythingLLM](../projects/anything-llm.md) | No graph feature found; none added or removed |
| [Letta](../projects/letta.md) | No graph in the entry. V1 server retired 20260816; `memory` and `memory_apply_patch` tools removed 20260925; memory is now a git repository of Markdown files. Reason: unstated |

## Evidence for

- Eight dated acts, listed above. Four give a reason (Microsoft GraphRAG, Graphiti, LLM Graph Builder, Zep) and four do not (Mem0, RAGFlow, Kuzu, Cognee). The LLM Graph Builder reason names a successor, not a cause.
- Kuzu's end reached dependants. Graphiti deprecated its driver; Cognee's code default is now `ladybug`, with `kuzu` accepted as an alias, and whether that package is the Kuzu fork was not checked ([Cognee](../projects/cognee.md)); Mem0 listed Kuzu among deleted drivers.
- Independent studies show limits of graph retrieval. Gains are mostly on multi-hop questions; one study found graph builds stopped at corpus sizes where BM25 was still scored; an abstract reports raw dense retrieval ahead of agentic memory systems in six of seven settings ([papers and benchmarks, section 3](../papers-benchmarks/README.md#3-does-a-graph-help)). **Reading:** no removal above cites any of this as its reason.
- **Reading:** four removals or limits sit beside a hosted counterpart named in the entries: Mem0's Platform graph, Zep's feature-flagged and proprietary parts, Cognee's GLiNER extractor labelled a demo with a licensed version, and Neo4j's Aura preview. This is a pattern in four entries, not a finding about motive.

## Evidence against, or limits

- This is not a census. The 21 entries were chosen by this repository, and the removal count depends on that choice.
- Dormancy is not a decision. The [timeline](../llm-era/README.md) says of fast-graphrag and nano-graphrag: "Dormancy, not a stated decision".
- Some removals relocate. RAGFlow still builds a Graph; Mem0 keeps shared-entity links; Microsoft GraphRAG is still patched.
- Additions are mostly unmeasured, and Graphiti's measured change is within its own stated noise. The reasons for additions are almost all unstated.
- Two vendor pages (Zep's blog, Neo4j's announcement) were read through summarising fetch tools in the entries; their wording is not verbatim.

## What is unresolved

- Why Mem0 deleted its graph store. **Reading:** the entry's cost table shows the old path added three LLM calls to `add()` and one to `search()`; no source says cost drove the removal.
- Whether RAGFlow's Graph in Knowledge Compilation uses the extraction of the deprecated GraphRAG: unstated.
- Whether Dify's graph is stored as a graph, and how it differs from the classic knowledge base: the backend is private.
- Whether the three quiet projects are finished by decision. The sources cannot show private channels.
- Whether Ladybug, Ryugraph or bighorn are drop-in replacements for Kuzu: unstated.

## Signals to watch

Each can be checked against the repository named.

- Graphiti: a release after v0.31.2 (20261020) that deletes the Kuzu driver.
- RAGFlow: the v1.0.0 release notes after rc3 (20261030); whether GraphRAG wording returns.
- Mem0: a release after Python 2.2.1 (20260925) that adds a reason, or a graph, to open source.
- Microsoft GraphRAG: the maintenance-mode notice (added 20260814) still present; any release after v3.3.0 (20261008).
- LLM Graph Builder: a release after v0.8.7, or archiving of the repository; Document Intelligence leaving preview.
- Cognee: the deprecated `temporal_cognify` argument deleted from code.
- GraphRAG SDK: issue 338 and the three agentic pull requests closed, and a release carrying them (2026-Q3 has ended).
- fast-graphrag, nano-graphrag, datastax/graph-rag: an archive flag or a commit, and datastax pull request 180 merged.
- Dify: Agent Knowledge Base leaving beta, or its KnowledgeFS repository becoming public.
- Any independent evaluation of a removed or added feature, naming the project.

## Sources

Entries: [Mem0](../projects/mem0.md), [RAGFlow](../projects/ragflow.md), [Dify](../projects/dify.md), [Letta](../projects/letta.md), [Zep](../projects/zep.md), [Kuzu](../projects/kuzu.md), [LLM Graph Builder](../projects/llm-graph-builder.md), [Microsoft GraphRAG](../projects/microsoft-graphrag.md), [Cognee](../projects/cognee.md), [Graphiti](../projects/graphiti.md), [TrustGraph](../projects/trustgraph.md), [Semantica](../projects/semantica.md), [LlamaIndex](../projects/llama-index.md), [Haystack](../projects/haystack.md), [AnythingLLM](../projects/anything-llm.md), [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md), [nano-graphrag](../projects/nano-graphrag.md), [fast-graphrag](../projects/fast-graphrag.md), [datastax/graph-rag](../projects/datastax-graph-rag.md), [GraphRAG SDK](../projects/graphrag-sdk.md), [M-flow](../projects/m-flow.md). Context: [papers and benchmarks](../papers-benchmarks/README.md), [LLM-era timeline](../llm-era/README.md).

Extra sources, read 20261030 19:57 to 19:58 UTC through a fetch tool that summarises the page:

- S1. https://github.com/mem0ai/mem0/blob/main/docs/migration/oss-v2-to-v3.mdx : removal list; no reason stated; "not being replaced by an OSS equivalent".
- S2. https://github.com/infiniflow/ragflow/blob/main/docs/release_notes.md : v0.27.0 deprecation wording; no reason stated (the last 576 characters of the page were not read).
- S3. https://github.com/topoteretes/cognee/releases/tag/v1.6.3 : `temporal_cognify` listed under breaking changes; no reason stated.
- S4. https://mem0.ai/blog/mem0-the-token-efficient-memory-algorithm : does not use the word "graph"; describes entity matching as a ranking signal.
