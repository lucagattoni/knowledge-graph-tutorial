# Retrieval by reasoning over structure

**In one paragraph.** Some projects retrieve neither by vector similarity alone nor by expanding a graph with an algorithm. A language model reads a structure (a document tree, an index page, a list of query results) and decides what to read next, sometimes over several turns. The entries here hold five variants that differ in what is built at index time and what the model does at query time. Almost every positive number comes from the authors of the method. The third-party tests read so far test related systems or the idea in other forms, not a scored run of PageIndex's released code, and some of them find plain vector or dense retrieval ahead.

## What the direction claims

- PageIndex's README argues "similarity ≠ relevance" and replaces the vector index with LLM reasoning over a tree of sections [PageIndex](../projects/pageindex.md).
- The "LLM wiki" pattern (a gist of 20260404) says knowledge is compiled once into linked pages, and that an index file "avoids the need for embedding-based RAG infrastructure" at moderate scale (about 100 sources); the gist adds that "as the wiki grows you want proper search" [LLM Wiki](../projects/llm-wiki-nashsu.md). OpenKB's README says "No Vector DB" [OpenKB](../projects/openkb.md).
- LogicRAG's paper title is "You Don't Need Pre-built Graphs for RAG": it orders sub-questions by dependency at question time [LogicRAG](../projects/logicrag.md).
- Graph-R1 trains a small model with reinforcement learning to run a think, query, retrieve, rethink loop [Graph-R1](../projects/graph-r1.md).

The problem they answer: a fixed top-k lookup fits multi-hop questions and long structured documents badly, and building a graph first is costly. The [literature page](../literature/graph-rag-research.md) records the move away from prebuilding as its own reading of a table, "not a measured result".

### Variants and what they cost

| Variant | Projects | Cost at index time | Cost at query time |
|---|---|---|---|
| A. Tree built once, model walks it | PageIndex; OpenKB (PDFs of 20 pages or more); RAGFlow Tree and PageIndex; Dify Agent Knowledge Base | PageIndex Flash: layout statistics make the skeleton; an LLM expands large nodes and writes summaries; README: about $0.001 per page (the project's figure). Standard mode: an LLM checks each table-of-contents entry; cost unstated. RAGFlow, Dify: unstated | PageIndex: an agent loop of tool calls, up to 20 turns in its benchmark harness; cookbook figure $110 per 1,000 queries (Vectify's) |
| B. Index and wiki pages an LLM writes and reads | LLM Wiki; OpenKB (short documents) | At least two LLM calls per source; the gist says one source may touch 10 to 15 pages | A planner picks tools, capped at 4, 8 or 12 steps; keyword, optional vector and graph search sit underneath |
| C. Agent picks depth or next hop in a local store | agent-memory (Tigerless); Basic Memory | agent-memory: one host LLM process per batch of conversation. Basic Memory: LLM cost unstated | agent-memory: default recall has no LLM call; the agent opens a hit at a chosen depth. Basic Memory: `bm_context` walks links to depth 1 to 5 (default 1) |
| D. Multi-turn query loop | Graph-R1; LogicRAG | Graph-R1: one GPT-4o-mini pass over the corpus ($2.81, unit unresolved in the entry) plus training on 4 A100 GPUs. LogicRAG: none beyond embeddings | Graph-R1: no per-query LLM spend (local policy), 7.0 s, 2.3 to 2.5 turns. LogicRAG: 3 calls, or 4 + 2R on the hard path; 1,777.9 tokens against 489.7 for vanilla RAG (paper, 2WikiMQA) |
| E. Planner over a prebuilt graph | KAG | LLM builds the graph; cost unstated | Logical-form planning; cost unstated |
| Contrast: algorithm walks the graph | HippoRAG | 9.2M input and 3.0M output tokens, 99.5 min (paper, MuSiQue, 11,656 passages) | Personalized PageRank plus one small LLM filter call; 1.2 s against 0.3 s dense |

Reading: C is a boundary case. Ranked search finds candidates, and the model chooses only depth or hop. In the agent-memory code read, links are not followed at query time.

## Who is doing it

| Project | How it takes this direction | Status at 20261030 | Evidence it works (and who measured it) |
|---|---|---|---|
| [PageIndex](../projects/pageindex.md) | Variant A; vectorless tree plus agent loop | Active; v0.5.0 of 20261029; MIT | Vectify's own tests (below). No scored independent run of the released SDK |
| [OpenKB](../projects/openkb.md) | A and B; compiles a wiki; PageIndex for long PDFs | Quiet; last push 20260722; v0.4.5; Apache-2.0 | None: no benchmark in the README |
| [Graph-R1](../projects/graph-r1.md) | D; RL-trained loop over a hypergraph | Quiet; last push 20260430; no release; MIT | Authors' paper; RAGSearch (third party) |
| [LogicRAG](../projects/logicrag.md) | D; no graph, query-time dependency order | Quiet; last push 20260719; no release; GPL-3.0 | Authors' paper only |
| [HippoRAG](../projects/hipporag.md) | Contrast; Personalized PageRank, not a model, walks the graph | Active; last push 20261006; MIT | Authors' papers |
| [LLM Wiki](../projects/llm-wiki-nashsu.md) | B; Karpathy pattern; planner with tools | Active; v0.6.13 of 20261022; GPL-3.0 | One unexplained README figure; no independent test |
| [KAG](../projects/kag.md) | E; logical-form planning over a prebuilt graph | Quiet; last push 20260128; v0.8.0 of 20250628; Apache-2.0 | README claims "significantly better", with no numbers |
| [RAGFlow](../projects/ragflow.md) | A; Tree and PageIndex are compilation outputs; Agentic RAG modes | Active; v1.0.0-rc3 of 20261030; Apache-2.0 | None found in the sources read |
| [Dify](../projects/dify.md) | A; Agent Knowledge Base builds an outline, summaries and a graph | Active; 1.18.0 of 20261023 adds it as opt-in beta; modified Apache-2.0, not an SPDX licence | None found in the sources read |
| [agent-memory](../projects/tigerless-agent-memory.md) | C; layered reads (abstract, outline, full) | Active; no release; about 59 days old; MIT | Authors' LongMemEval-S study; not specific to the reading step |
| [Basic Memory](../projects/basic-memory.md) | C; hybrid search, graph walk by the client | Active; v1.0.0 of 20261029; AGPL-3.0 | Authors' internal matrix; not specific to the graph walk |

GPL and AGPL entries are read-only references here: ideas and results only.

The [papers page](../papers-benchmarks/README.md) (section 2.2) lists the same family at paper level, from abstracts: Search-R1 and Search-o1 (plain-text agent baselines), Think-on-Graph, GraphRAG-R1, GraphSearch, GraphWalker, PathRouter, Search-on-Graph-R1, MOSAIC (training-free) and RANGER (20261020). Repositories for GraphWalker, PathRouter, Search-on-Graph-R1, MOSAIC and RANGER are unstated; the page gives no results for any of them.

## Evidence for

| Who measured | Setup | Result | Caveat |
|---|---|---|---|
| Vectify (PageIndex's maker), cookbook, 20261016, `pageindex` 0.4.1 | 63 questions on five NVIDIA 10-Ks; vector baseline with top-k 10, 30, 50, 100 | PageIndex 100.0%; vector 54.0, 74.6, 79.4, 87.3% | Judge is a Claude model; one document type; vector costs priced without caching. Best of six embedding variants: 92.1% for $134 against PageIndex $110 per 1,000 queries |
| Vectify, Financial QA, 20261022 to 20261027 | 100 questions, 7,318 pages; only the model behind PageIndex varies | 98.7% at the top; lowest 65.7% | No baseline |
| Vectify, README | FinanceBench, 150 questions | 98.7%, against a "Vector RAG 50%" bar | The system measured is Mafin 2.5, not the SDK. 148 of 150 counts three label types as correct; the aligned label alone gives 136 of 150, 90.7% (the entry's arithmetic) |
| Graph-R1 authors | Six QA sets, 128 test questions each | Average F1 57.82 (7B) against 46.19 for Search-R1 | Baselines run without the 4096-token cap; text says 57.28, table 57.82; nothing above 7B tested |
| LogicRAG authors | HotpotQA, 2WikiMQA, MuSiQue, 1,000 questions each | 2WikiMQA LLM-Acc 62.5 against 47.1 for HippoRAG2 | Below HippoRAG2 on HotpotQA Str-Acc (54.8 against 56.7); GPT-4o-mini generates and judges |
| Fan et al., NYU Shanghai (RAGSearch, 20260401) | Dense RAG against five GraphRAG backends, single-shot and agentic | With the GraphSearch agent: HotpotQA 38.22 dense against 58.64 graph; agentic search narrows the gap, most with RL | Graph figure is best of five; the knowledge sources differ (Wikipedia dump against each question's own context) |
| RIT-RAG authors, 20261008 | FinanceBench, three generators | Their own "corpus-level PageIndex" baseline 72.0, 75.3, 66.7% against vanilla RAG at k=5 41.3, 49.3, 48.0% | Baseline written by the authors; their method scores higher still |

On the same Search-R1 and Graph-R1 pair, RAGSearch's three listed gaps are 17.66, 32.69 and 26.40 points of Contain-EM (computed from its row). The Graph-R1 paper's multi-hop F1 gaps are 11.84 to 23.82. The protocols differ and the two sets were not reconciled here.

## Evidence against, or limits

| Who measured | Setup | Result |
|---|---|---|
| Lumer et al., 2511.18177 | 150 questions over 1,200 SEC filings; vector agentic RAG against the authors' own node-based system, modelled on PageIndex | Vector system won 68% of comparisons; node preprocessing $30.62 per 10-K |
| Bao et al., 2610.30755 (20261022) | Conversation memory (LoCoMo, LongMemEval and others): raw dense retrieval plus rerank against 12 agentic memory systems | Raw retrieval first in 6 of 7 settings; ingestion of a 1M-token history 0.3 h against 3.2 to 27.0 h |
| Chen et al., 2606.25656 | STaRK-Prime, Claude 3.7 Sonnet | Agentic RAG with a document tool 0.6881 Hit@1; the same agent with a KG tool 0.6055 |
| Han et al., 2502.11371 | Unified protocol; null queries, 8B generator | Iterative retrieval cut Community-Local null accuracy from 80.07 to 50.50 (one GraphRAG variant) |
| Zarrinkia et al., 2603.14045 | KET-RAG on three multi-hop sets | Gold answer in context for 77% to 91% of questions; 73% to 84% of errors were reasoning failures |

Bao et al. and Zarrinkia et al. are abstract-only on the papers page; none of these five tests the PageIndex SDK.

Other limits recorded in the entries:

- Hashmi (arXiv 2604.14222) reports 0.900 against 0.845 for a tree method on four short documents, 22 queries; the paper calls it preliminary and says the tree system was given the target document and the vector system was not [PageIndex](../projects/pageindex.md).
- In RIT-RAG's PageIndex baseline a retriever first picks one document, so a wrong pick makes the evidence unreachable (the PageIndex entry's reading of that paper) [PageIndex](../projects/pageindex.md).
- Graph-R1 offers no trained weights; three open issues ask for them, none with an owner reply. Build needs an OpenAI key [Graph-R1](../projects/graph-r1.md).
- LogicRAG: the paper says the dependency graph is checked for cycles; the released code does not check [LogicRAG](../projects/logicrag.md).
- LLM Wiki: the one figure (recall 58.2% to 71.4% with vector search) has no dataset or definition [LLM Wiki](../projects/llm-wiki-nashsu.md).
- agent-memory: the README's numbers are in files no longer in the current tree; its first test of the Manage layer concluded it "could not have measured it" [agent-memory](../projects/tigerless-agent-memory.md).
- Basic Memory's matrix is marked "internal-only" [Basic Memory](../projects/basic-memory.md).

## What is unresolved

- **Structure or model?** Vectify's Financial QA varies only the model and gets 65.7% to 98.7%. How much of a result belongs to the tree and how much to the navigating model is not separated in any entry.
- **Matched cost.** In the cookbook the cheaper vector runs ($16 to $68 per 1,000 queries) score 54.0% to 79.4%, and PageIndex ($110) costs less only than the top-k 100 run ($135). Vector costs there are priced without prompt caching and PageIndex's include cache hits, so no entry holds a like-for-like cost comparison.
- **Other document types and scale.** PageIndex results are on annual reports (10-K) and one set of long-document questions without a baseline. Whole-corpus behaviour appears only in Lumer et al. (1,200 filings) and RIT-RAG's baseline, neither the SDK.
- **Where an index page stops working.** The gist gives no threshold ([timeline](../llm-era/README.md), open question 3).
- **Productised versions.** RAGFlow, Dify and KAG publish no figures in the sources read. Whether RAGFlow's PageIndex output uses Vectify's code is unstated.
- **Graph-R1's ceiling.** Nothing above 7B was tested. The untrained baseline (average F1 17.79 on two sets) is read in the entry, from the July note, as a model that cannot follow the loop protocol; the paper does not test a stronger untrained model.
- **Reasoning versus retrieval.** Zarrinkia et al. report that most errors are reasoning failures with the gold answer in context. Whether that holds for navigation-based systems is tested in no entry.

## Signals to watch

Each can be checked against the named source.

| Signal | Check |
|---|---|
| A scored run of PageIndex's SDK by someone other than Vectify | The `pageindex-rag-bench` harness read "Not yet run" at 20261030 [PageIndex](../projects/pageindex.md); the five arXiv papers listed there were not opened |
| FinanceBench re-run on the current SDK instead of Mafin 2.5 | PageIndex README and the evaluation repository (last pushed 20251020) |
| Dify's Agent Knowledge Base leaves beta or ships an evaluation | Dify release notes after 1.18.0 (20261023) |
| RAGFlow 1.0.0 final after rc3 (20261030), with docs on how Tree and PageIndex are read at query time | RAGFlow releases and `docs/` |
| Graph-R1 checkpoints or a Hugging Face release | Issues #19, #22, #24; commits after 20260430 |
| A commit to KAG or a release after v0.8.0 (20250628) | KAG commits (last push 20260128) |
| OpenKB 0.5.0 final (PyPI holds 0.5.0rc1, no GitHub release) | OpenKB releases |
| LLM Wiki publishes the data behind "58.2% to 71.4%" | README and issues |
| agent-memory's first release or a longitudinal test of Manage | Releases; `docs/TODO.md` |
| Basic Memory 1.0 re-run of its matrix | Benchmarks folder; the 1.0 docs say historical results "should not be relabeled as 1.0 results" |
| A later version of RAGSearch, with its efficiency appendix | arXiv 2604.09666 |

## Sources

Entries: [PageIndex](../projects/pageindex.md), [OpenKB](../projects/openkb.md), [Graph-R1](../projects/graph-r1.md), [LogicRAG](../projects/logicrag.md), [HippoRAG](../projects/hipporag.md), [LLM Wiki](../projects/llm-wiki-nashsu.md), [KAG](../projects/kag.md), [RAGFlow](../projects/ragflow.md), [Dify](../projects/dify.md), [agent-memory](../projects/tigerless-agent-memory.md), [Basic Memory](../projects/basic-memory.md).

Context pages: [papers and benchmarks](../papers-benchmarks/README.md) (section 2.2, the RAGSearch row, section 3), [what the research found](../literature/graph-rag-research.md) (sections 2.2 and 3), [timeline](../llm-era/README.md).

No page outside this repository was fetched for this page. Every figure above is read from the entries and context pages, which carry their own sources and read times. They were read for this page on 20261030, before 19:58 UTC.
