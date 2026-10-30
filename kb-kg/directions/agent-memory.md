# Memory layers and temporal graphs for agents

**In one paragraph.** A large share of open-source activity in this field now concerns memory for agents rather than retrieval over documents: systems that keep what an agent learned across sessions and decide what to update or drop. Eighteen projects in this repository take five routes: extract facts, build a temporal graph, let the agent manage its own memory, keep memory as files, or sell it as a hosted platform. Nearly all published scores in the entries come from the project's own team or a competitor, mostly on two conversational benchmarks (LoCoMo, LongMemEval), with setups that differ between projects. The independent studies in the entries find plain retrieval or long-context baselines competitive with the memory systems, and the entries found no independent evaluation of several of the largest projects.

## What the direction claims

Its proponents say a context window is not memory: an agent that works across days needs facts, preferences and history that survive the session, stay current when the world changes, and cost fewer tokens than replaying the transcript. The open question, framed on the [papers and benchmarks page](../papers-benchmarks/README.md#32-graph-memory-against-plain-retrieval-for-agents), is whether a graph or a memory layer beats plain retrieval for agents.

### Five design families

Projects sit in more than one family; each appears where its entry puts the weight.

| Family | What it stores | How it decides to update or forget (as the entries describe it) |
|---|---|---|
| Extract and store facts | Short fact-like records with embeddings; some add typed layers (profile, episodes, observations, L0 to L3 refinement) | [Mem0](../projects/mem0.md) 2.x only adds; it drops a new memory whose text hash matches a retrieved neighbour; update and delete are caller-driven. [Honcho](../projects/honcho.md) has a background "dreamer" that consolidates. [Hindsight](../projects/hindsight.md) consolidates facts into "observations" and refreshes "mental models" in the background. Forgetting rule unstated for Memori, MemMachine, claude-mem and TencentDB Agent Memory |
| Temporal knowledge graph | Entities, facts as edges with validity dates, and the episodes they came from | [Graphiti](../projects/graphiti.md): a contradiction never deletes; the older edge gets `invalid_at` and `expired_at`, and deletion is explicit tooling. [Cognee](../projects/cognee.md): `improve` includes a conflict-review stage that needs an LLM, and `forget` exists. Mem0's old graph variant marked conflicting relations invalid; the open source deleted it on 20260414 |
| Self-managed memory | Notes or files the model writes itself | [Letta](../projects/letta.md): the agent edits its memory files with file tools; message history is immutable; "dreaming" subagents work in the background. [A-mem](../projects/a-mem.md): one LLM call per new note decides whether to link it or rewrite its five nearest neighbours. [MIRIX](../projects/mirix.md): one agent per memory type, and an `auto_dream` endpoint that merges duplicates and resolves stale entries |
| Filesystem or Markdown | Files in a tree or git repository; indexes are derived | [OpenViking](../projects/openviking.md): an LLM loop returns add, update, delete and link operations at session commit, logged in `memory_diff.json`. [EverOS](../projects/everos.md): Markdown is the record; a merge job is off by default. [memU](../projects/memu.md): the host agent decides whether to write or patch a file. Letta's current memory is a git repository of Markdown |
| Hosted platform | The same API as a paid service, with features the open code lacks | Set by the vendor. Mem0, Zep, Supermemory, Cognee, Honcho, MemOS, Memori, Letta and OpenViking all have a hosted edition. Mem0's Platform adds opt-in decay, a "Dream" merge and temporal reasoning that the open source lacks; Zep's engine differs from open Graphiti; [Supermemory](../projects/supermemory.md)'s memory engine is not in its public repository |

Reading: background "dreaming" or consolidation recurs in at least six entries (Letta, Supermemory, Honcho, Mem0 Platform, MIRIX, OpenViking). The entries record no measurement of what any of them does to answer quality.

## Who is doing it

Attention, computed in this run from the 20261030 19:13 UTC snapshot (924 repositories, 4,410,610 stars, category assigned by search hits, not relevance) [S1]: agent-memory holds 242 repositories and 916,099 stars (20.8%); core 235 and 558,835 (12.7%); markdown-kb 106 and 116,328 (2.6%); adjacent (code graphs, graph databases, RAG platforms) 341 and 2,819,348 (63.9%). The selection file moves Graphify (139,356 stars) from core to adjacent, which would give core 9.5% and adjacent 67.1% (computed); other reassignments were not recomputed. Reading: agent memory holds more stars than the document-focused core category and fewer than adjacent. Stars are unvetted signals; the snapshot README says they are not evidence of quality.

| Project | How it takes this direction | Status at 20261030 | Evidence it works (and who measured it) |
|---|---|---|---|
| [mem0](../projects/mem0.md) | Extract and store; one extraction call, add only; graph store removed from open source | Active; 68,112 stars; Apache-2.0; Python 2.2.1 on 20260925, none since | Own paper: LoCoMo judge score 66.88 against 72.90 for full context. Own 2026 claim: LoCoMo 92.5 on the Platform stack, models unnamed |
| [cognee](../projects/cognee.md) | Graph, vector and relational stores; remember, recall, improve, forget | Active; 32,932 stars; Apache-2.0; v1.6.6 on 20261029 | Own reports: BEAM 100K 0.79, 10M 0.67; LoCoMo about 91% on 1,762 of 1,986 questions. Its entry found no independent run; MemoryAgentBench lists it at 20.6 overall (per the Letta entry) |
| [graphiti](../projects/graphiti.md) | Temporal graph with bi-temporal edges; now calls itself a "context graph" framework | Active; 32,372 stars; Apache-2.0; v0.31.2 on 20261020 | Zep paper (authors): LongMemEval_s 63.8 against 55.4 for full context (gpt-4o-mini). Its entry found no independent evaluation; MemoryAgentBench lists Zep at 24.0 (per the Letta entry) |
| [zep](../projects/zep.md) | Samples repository for the hosted Zep service; engine is Graphiti | Active as samples; 4,984 stars; Apache-2.0 | Benchmark folder for LoCoMo and LongMemEval; no score in the part read |
| [letta](../projects/letta.md) | Self-managed memory in a git repository of Markdown (MemFS) | Old repository's code retired; `letta-code` active, 3,741 stars | Own: LoCoMo 74.0 with a file-tool agent (20250812); FrontierMemory 73.3 (Letta Research). No independent evaluation of the current memory found |
| [openviking](../projects/openviking.md) | Virtual filesystem for memory, resources and skills; AGPL-3.0 since 20260330 | Active; 41,196 stars; v0.5.2.1 on 20261027 | Own blog: LoCoMo 24.20% to 82.08% with an agent (OpenClaw). No independent re-run found |
| [supermemory](../projects/supermemory.md) | Hosted engine: fact extraction, profiles, claimed temporal vector-graph store | Active; 31,471 stars; MIT repository, engine not public | Own README: 95% Recall@15 on LongMemEval; research page 97% Recall@20 (second-hand read). No third party named |
| [hindsight](../projects/hindsight.md) | Retain, recall, reflect over typed memories | Active; 56,612 stars; MIT; v1.1.0 on 20261021 | Own paper: LongMemEval 91.4%, LoCoMo 89.61% (larger backbone); 83.6% with a 20B model. The independent reproduction its README names was not located by the entry |
| [claude-mem](../projects/claude-mem.md) | Hooks capture a coding agent's tool use; compressed log in SQLite plus Chroma | Active; 105,952 stars; Apache-2.0 open core | README has no benchmark or paper |
| [tencentdb-agent-memory](../projects/tencentdb-agent-memory.md) | Layers L0 to L3 plus Wiki and Code-Graph; team-shared | Active; 30,258 stars; MIT; v2.0.3 | Own README: PersonaMem 48% to 76%, no model or setup named |
| [memos](../projects/memos.md) | "Memory operating system"; MemCube; local plugin with L1 to L3 layers | Active; 12,200 stars; Apache-2.0 | Own README: LoCoMo 88.83, LongMemEval 89.20, no competitor scores; the paper's abstract reports no experiments |
| [memori](../projects/memori.md) | Wrapped LLM client extracts facts and triples | Quiet on main since June; 17,241 stars; v3.3.6 on 20260528 | Own: README 87% on LoCoMo at 721 tokens; paper abstract 81.95% at 1,294 tokens |
| [memu](../projects/memu.md) | Host agent writes Markdown memories and skills; embedding-only retrieval | Active; 14,581 stars; v1.5.1, v2.0.0 beta | README gives no benchmark |
| [everos](../projects/everos.md) | Markdown record with derived SQLite and LanceDB indexes | Active; 13,721 stars; Apache-2.0; v1.5.1 | README states no result; a benchmark runner exists |
| [honcho](../projects/honcho.md) | Peers, a deriver and a dreamer; AGPL-3.0 | Active; 7,837 stars; v3.5.0 on 20261030 | README claims the "Pareto Frontier"; its evals page was not fetched |
| [memmachine](../projects/memmachine.md) | Episodic, profile and working memory; query-routing agent | 3,078 stars; v0.4.0 on 20261008; default branch idle since 20261012 | README gives no result; evaluation scripts exist |
| [a-mem](../projects/a-mem.md) | Zettelkasten-style notes that link and rewrite each other | Quiet; 1,212 stars; last push 20251212 | Paper (NeurIPS 2025) claims gains; Mem0's paper (a competitor) re-ran it at 48.38 |
| [mirix](../projects/mirix.md) | Six memory types, one agent each | Active; 3,456 stars; 7 commits on main since 20260801 | Own paper: 85.4% on LOCOMO, 35% over a RAG baseline on ScreenshotVQA. MemoryAgentBench lists it at 26.2 overall (per the Letta entry) |

## Evidence for

- **Fewer tokens and lower latency than replaying everything.** Mem0's paper (own) reports 1,764 memory tokens and 1.440 s p95 against 26,031 and 17.117 s for full context on LoCoMo ([mem0](../projects/mem0.md)). The Zep paper (own) reports 1.6k tokens and 3.20 s against 115k and 31.3 s on LongMemEval_s ([graphiti](../projects/graphiti.md)).
- **Some accuracy gains over full context.** In the Zep paper, 63.8% against 55.4% (gpt-4o-mini) and 71.2% against 60.2% (gpt-4o), most on preference and temporal-reasoning questions ([graphiti](../projects/graphiti.md)). In Mem0's paper the graph variant is higher on temporal questions, 58.13 against 55.51 ([mem0](../projects/mem0.md)).
- **A simpler write path did better in one audit.** Bao et al. (independent of Mem0) found UPDATE and DELETE were 4.39% of 33,902 write decisions on LoCoMo; replacing them with ADD and NONE moved accuracy from 67.36 to 69.42. Mem0 later made `add()` add-only; the audit used the older policy and did not test the new pipeline ([mem0](../projects/mem0.md)).
- **A file-tool agent scored well.** Letta reports 74.0% on LoCoMo against the 68.5% that it says Mem0 reported for its graph variant (competitor-run, GPT-4o mini) ([letta](../projects/letta.md)).

## Evidence against, or limits

- **Plain retrieval is competitive.** Bao et al. (2610.30755, 20261022) report raw dense retrieval plus reranking first in six of seven benchmark-model settings, by 0.13 to 5.53 points; on LongMemEval it scored 87.53 against 66.40 for Mem0. The authors propose that baseline, and the entry could not tell which Mem0 cells they re-ran ([mem0](../projects/mem0.md), [papers and benchmarks](../papers-benchmarks/README.md#32-graph-memory-against-plain-retrieval-for-agents)).
- **Full context beat the memory layer on accuracy** in Mem0's own paper (72.90 against 66.88 and 68.44). Zep fell below full context on `single-session-assistant` questions ([mem0](../projects/mem0.md), [graphiti](../projects/graphiti.md)).
- **Memory systems scored below plain baselines in MemoryAgentBench** (ICLR 2026, run by the benchmark's authors, 22 rows, GPT-4o-mini): overall long-context 42.2, BM25 41.5, MemGPT 28.3, MIRIX 26.2, Zep 24.0, Mem0 21.1, Cognee 20.6; MemGPT scored 15.5 on selective forgetting. Letta's version was unstated ([letta](../projects/letta.md)).
- **The yardsticks are contested.** An audit found 99 score-corrupting errors in 1,540 LoCoMo questions (6.4%), and the judge accepted 62.81% of deliberately wrong, topically close answers; the author's affiliation is unstated ([mem0](../projects/mem0.md)). LoCoMo question counts differ between sources in the entries (1,540; about 300; 1,986 with 143 flagged and 96 open-domain removed) ([mem0](../projects/mem0.md), [cognee](../projects/cognee.md)). Zep's LoCoMo score went from 84% to 75.14% after Mem0 disputed it (Mem0 replicated 58.44%); both are vendors ([graphiti](../projects/graphiti.md)).
- **Results belong to code that has changed.** Mem0's graph evidence concerns a feature the open source deleted, and its best 2026 numbers use "proprietary optimizations" of the Platform. Letta's published runs use the retired server ([mem0](../projects/mem0.md), [letta](../projects/letta.md)).
- **Maintenance and terms vary.** A-mem: no push since 20251212. Memori: main nearly idle since June. MemMachine: default branch idle since 20261012. Zep ended its Community Edition on 20250402. OpenViking and Honcho are AGPL-3.0; Memori and memU use reworded Apache text that GitHub does not recognise ([a-mem](../projects/a-mem.md), [memori](../projects/memori.md), [memmachine](../projects/memmachine.md), [zep](../projects/zep.md), [openviking](../projects/openviking.md), [honcho](../projects/honcho.md), [memu](../projects/memu.md)).
- **Cost and exposure.** Graphiti needs an LLM at every ingest and its reference servers have no authentication ([graphiti](../projects/graphiti.md)). Memori's code posts conversations to a hosted endpoint unless a base URL is set ([memori](../projects/memori.md)). Mem0 and Graphiti send telemetry by default.

## What is unresolved

- **Do graphs help agent memory?** The graph variant is +1.56 points in Mem0's own paper; no independent graph-memory study is in the entries. In document studies, graphs win on multi-hop questions ([papers and benchmarks](../papers-benchmarks/README.md#33-reading-across-the-rows)).
- **Same benchmark, different numbers.** Mem0 on MemoryAgentBench is 21.1 overall in one source and 41.28 or 41.95 in Bao et al.; the entries do not say whether the setups are comparable ([letta](../projects/letta.md), [mem0](../projects/mem0.md)).
- **Forgetting is barely measured.** Few benchmarks cover updates or deletion (MemoryAgentBench, RECON, GateMem), and no study of decay or consolidation is in the entries ([papers and benchmarks](../papers-benchmarks/README.md)).
- **Coding-agent memory** (claude-mem, memU, Letta Code, OpenViking plugins): the entries hold no evaluation on coding tasks.
- **Unnamed stacks.** Mem0's and OpenViking's 2026 pages do not name the answering or judge model.

## Signals to watch

- A paper or repository that re-runs Graphiti or Zep, Cognee, OpenViking or Hindsight on LoCoMo, LongMemEval or MemoryAgentBench without a stake in the result (check arXiv and the [papers and benchmarks](../papers-benchmarks/README.md) page).
- A second version of Bao et al. 2610.30755, or Mem0's answer on which cells were re-run.
- Mem0: a release after Python 2.2.1 (20260925); `reference_date` working in open-source `search()`; third-party reruns of `mem0ai/memory-benchmarks`.
- Hindsight: the Virginia Tech or Washington Post reproduction its README names, located and read.
- Letta: any published evaluation of MemFS.
- Graphiti: Kuzu removal; further Zep-fork features merged upstream (PR #1964 merged 20261009); a release after v0.31.2.
- Quiet projects: a push to A-mem after 20251212, a Memori release after v3.3.6 (20260528), a MemMachine default-branch commit after 20261012.
- A second snapshot (`tools/gh_snapshot.py`) to compare the category sums above.

## Sources

Entries: [mem0](../projects/mem0.md), [cognee](../projects/cognee.md), [graphiti](../projects/graphiti.md), [letta](../projects/letta.md), [openviking](../projects/openviking.md), [supermemory](../projects/supermemory.md), [hindsight](../projects/hindsight.md), [claude-mem](../projects/claude-mem.md), [tencentdb-agent-memory](../projects/tencentdb-agent-memory.md), [memos](../projects/memos.md), [memori](../projects/memori.md), [memu](../projects/memu.md), [everos](../projects/everos.md), [honcho](../projects/honcho.md), [memmachine](../projects/memmachine.md), [a-mem](../projects/a-mem.md), [mirix](../projects/mirix.md), [zep](../projects/zep.md).

Context pages: [papers and benchmarks, sections 3.2 and 4.3](../papers-benchmarks/README.md), [LLM-era timeline](../llm-era/README.md), [what the research says](../literature/graph-rag-research.md).

- S1. [Landscape snapshot 20261030 19:13 UTC, `repos.tsv`](../landscape/20261030_1913-github/repos.tsv) and [selection file](../landscape/20261030_1922-selection.md): star sums and shares by category, computed by summing the `stars` column per `category` over all 924 rows; Graphify's reassignment from the selection file (read 20261030 19:56 UTC).
