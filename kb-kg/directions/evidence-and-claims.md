# What is measured, by whom, and what is only claimed

**In one paragraph.** This page is about the evidence behind the numbers projects publish, not about a technique. In the entries read, every performance figure was produced by the project or its company, on a benchmark and setup it chose. The tables below sort 25 claims from 22 projects into three classes: a method is stated and a third party has measured the project or its method; the figure is self-reported with a method; the entry found a headline figure with no method or no baseline. Few claims have an independent check of the same claim. The independent studies in the papers file test graph methods, and some of the named systems, on other tasks. The page also tabulates the nine fast-growth repositories of the newest snapshot, as unvetted signals.

## What the direction claims

Projects offer numbers as the case for their approach. Four kinds recur: accuracy on public benchmarks (LoCoMo, LongMemEval, BEAM, FinanceBench, HotpotQA); token or cost savings against a baseline; win rates judged by an LLM; and attention signals such as stars. The [Cognee entry](../projects/cognee.md) records that the timeline treats headline memory scores in READMEs as the vendors' own. The question here is narrower: who measured it, was the method stated, did anyone else check.

Scope: I read the evidence sections of the entries named below and searched all 77 entries for "independent", "self-reported", "third-party" and "none found". The other entries are not tabulated; absence from a table says nothing about them.

## Who is doing it

Three voices are kept apart. "Claim" is what the project states. "Who measured it" and "Method stated?" are what the entry recorded. **Reading** marks my own interpretation.

### Class 1: a method is stated, and a third party has measured the project or its method

| Project | Claim | Who measured it | Method stated? | Independent check found? | Entry |
|---|---|---|---|---|---|
| mem0 (2026 algorithm) | LoCoMo 92.5, LongMemEval 94.4, BEAM 64.1 at 1M and 48.6 at 10M. The +0.9 and +1.0 steps over the April figures (computed in the entry) come with Temporal Reasoning, which the May post places on the Platform; open-source `search()` raises an error for `reference_date` | Mem0 | Partly: top 200, about 6,956 tokens. No page names the extraction, answering or judge model. LoCoMo size is 1,540 questions on two pages, "about 300" in the benchmark README | Partly. Bao et al. (20261022) audited the older 1.0.11 write policy and ran Raw-RAG, their own baseline, against 12 systems (LongMemEval: Mem0 66.40, Raw-RAG 87.53). No third-party run of the 2026 headline | [mem0](../projects/mem0.md) |
| mem0 (paper, April 2025) | LoCoMo 66.88 against OpenAI memory 52.90 (26% relative); p95 latency 91% lower and tokens 93% fewer than full context | Mem0 | Yes: GPT-4o-mini, LLM judge over 10 runs, judge name unstated. Full context scores higher (72.90) | Partly. Zep says Mem0 misconfigured Zep (75.14 against 65.99), a competitor's claim. The entry's arithmetic, weighting categories by question count, gives 62.14 | [mem0](../projects/mem0.md) |
| microsoft-graphrag | "Substantial improvements" in comprehensiveness and diversity (paper); dynamic community selection cuts token cost 77% (blog); LazyGraphRAG at 0.1% of full index cost and over 700 times lower query cost | Microsoft Research authors | Partly. Abstract gives no figures. Blog: 50 global questions, LLM-judged. LazyGraphRAG: 100 synthetic queries, "4%" stated against two different baselines, no code or prompts | The entry read none. Third-party studies of GraphRAG exist (below) but test other tasks | [microsoft-graphrag](../projects/microsoft-graphrag.md) |
| lightrag | Win share over NaiveRAG, RQ-RAG, HyDE and GraphRAG on four UltraDomain subsets (54.8% overall against GraphRAG on Agriculture; on Mix the baseline wins narrowly) | The authors | Partly: LLM judge, three criteria, LLM-written queries. Judge model, runs and variance unstated | The entry fetched none. LightRAG is a system under test in two third-party studies (below), neither using win share | [lightrag](../projects/lightrag.md) |
| pageindex | "98.7% accuracy on FinanceBench"; README chart shows "Vector RAG 50%" | Vectify | Partly. The system measured was Mafin 2.5, not the SDK at v0.5.0. LLM judge plus "expert human annotations". Vector baseline configuration unstated. 148 of 150 matches counting the BE, MVA and SEDC labels as correct; the aligned label alone gives 90.7% (entry's arithmetic) | No scored run of the SDK. RIT-RAG's authors, who propose a competing method, wrote a "corpus-level PageIndex": 72.0, 75.3, 66.7% on FinanceBench. A third-party harness is marked "Not yet run" | [pageindex](../projects/pageindex.md) |
| fast-graphrag | Vendor benchmark on 2wikimultihopQA subsets of 51 and 101 questions; HotpotQA (101) 0.84 against 0.78 for a plain vector index | The vendor | Partly: scripts and results are in the repository; HotpotQA code and data not found | Partly. GraphRAG-Bench (GPT-4o-mini): Fast-GraphRAG 56.95 against reranked basic RAG 60.92 on Novel fact retrieval, 60.93 against 64.73 on Medical, 48.55 against 42.93 on Novel complex reasoning. Its configuration is not stated | [fast-graphrag](../projects/fast-graphrag.md) |

### Class 2: self-reported, a method stated at least in part, no independent check found

| Project | Claim | Who measured it | Method stated? | Independent check found? | Entry |
|---|---|---|---|---|---|
| graphiti (Zep) | Deep Memory Retrieval 94.8% against MemGPT 93.4%; LongMemEval_s 71.2% against 60.2% full context (gpt-4o), lower latency | Zep team (paper) | Yes, with the paper's caveats: DMR is small and full conversation scores 94.4%; latency included network latency the baselines lacked; Zep fell below baseline on one question type | None. Mem0's CTO reported 58.44% for Zep's LoCoMo score; Zep put it at 75.14% after correcting its own 84%. Both vendor-reported | [graphiti](../projects/graphiti.md) |
| cognee | BEAM 100K 0.79; BEAM 10M 0.67; LoCoMo about 91% | Cognee | Yes, with limits it states: 20 questions, the 10M result in-sample; LoCoMo 1,762 of 1,986 questions, conversations used to develop the setup | None. arXiv 2610.30755 has no Cognee row; a Vectorize article (it sells Hindsight) says Cognee "has not published a LongMemEval score" | [cognee](../projects/cognee.md) |
| openviking | LoCoMo, agent's own memory to agent plus OpenViking: OpenClaw 24.20% to 82.08%, Hermes 33.38% to 82.86%, Claude Code 57.21% to 80.32% | OpenViking team (blog 20260529) | Partly. Blog gives no model names, question counts (except 50 ClawWork tasks) or judge; the guide says the report "does not pin every runtime parameter" | None. A review post says "nobody independent has re-run them" | [openviking](../projects/openviking.md) |
| codegraph | 88% fewer tool calls, 62% fewer tokens, 44% lower cost | The project | Partly: seven repositories, Claude Opus 4.8, median of four runs | None in the sources read | [codegraph](../projects/codegraph.md) |
| code-review-graph | Median 63x token reduction per question (35x to 358x); impact F1 0.69 | The project | Yes, six repositories. README calls the baseline "an upper bound no real agent pays" and impact recall of 1.0 circular | None in the sources read | [code-review-graph](../projects/code-review-graph.md) |
| code-graph-rag | Finding callers: graph F1 0.9116 against call-tuned grep 0.5358 (own package); django 0.957 against 0.789 | The project | Yes: scored against a Python `ast` oracle that favours name-based resolution. Agent-level results: none published | None; no dedicated search | [code-graph-rag](../projects/code-graph-rag.md) |
| graphify (`BENCHMARKS.md`) | LOCOMO recall@10 0.497 against mem0 0.048; QA accuracy 45.3% against supermemory 49.7% | The project | Partly: one model (Kimi K2.6), judge checked against a second at 90.6% agreement. Harness directories named in the commands are not in the tree | Third-party tests are small (one repository: 628 tokens against 13,659 to read a file). None repeats the benchmark | [graphify](../projects/graphify.md) |
| codebase-memory-mcp | Paper: 83% answer quality against 92% for a file-exploration agent, about 10x fewer tokens, 2.1x fewer tool calls, 31 repositories. README repeats the token and tool-call figures, not the quality figures; claims 162 languages, the paper describes 66 | Paper authors; the first author's name matches the main committer's | Abstract read only | Unstated: the card searched the README, not for independent checks | [codebase-memory-mcp](../projects/codebase-memory-mcp.md) |
| memori | README: 87% on LoCoMo at 721 tokens per query. Paper abstract: 81.95% at 1,294 tokens | The project | README: unstated. Paper: abstract only | None in the sources read | [memori](../projects/memori.md) |
| basic-memory | LongMemEval recall@5 0.951 against mem0 0.979; QA accuracy 0.583 against 0.450 | The project | Yes, with caveats: "internal-only", mem0 ran with `infer=false`, small answerer, judge-human agreement not measured | None found | [basic-memory](../projects/basic-memory.md) |
| minirag | arXiv v3 introduction: "consistently achieves state-of-the-art performance across all evaluation settings" | The authors | Yes: GPT-4o judge, three repeats. The claim does not match the paper's Table 1, where LightRAG leads with gpt-4o-mini on LiHua-World | None found | [minirag](../projects/minirag.md) |

[m-flow](../projects/m-flow.md) (81.8% against 79.4% for Cognee Cloud, from a benchmark repository in its own organisation), [mirix](../projects/mirix.md) (paper: 85.4% on LOCOMO, "99.9% lower storage", baseline unstated) and [a-mem](../projects/a-mem.md) publish their own results; each entry records no independent evaluation read. [memu](../projects/memu.md), [everos](../projects/everos.md), [memmachine](../projects/memmachine.md) and [semantica](../projects/semantica.md) publish no comparative result in the README.

### Class 3: a headline figure where the entry found no method or no baseline, or did not check

| Project | Claim | Who measured it | Method stated? | Independent check found? | Entry |
|---|---|---|---|---|---|
| graphify | README banner "Cut agent token spend by 80%" | Unstated | No: absent from `BENCHMARKS.md`, the docs and the pricing page; baseline unstated. The adding commit (20261010) is titled "cost-led Graphify Cloud headline (80% fewer tokens)" and adds no link or method | None. A HackerNoon author says he did not test it | [graphify](../projects/graphify.md) |
| llm-wiki-nashsu | README: "overall recall improved from 58.2% to 71.4% with vector search enabled" | The project | No dataset, question set, count or definition of recall; a code search for "58.2" finds only README files | None found | [llm-wiki-nashsu](../projects/llm-wiki-nashsu.md) |
| tencentdb-agent-memory | PersonaMem 48% without the system, 76% with it, labelled +59% (the figures give +58%, computed) | The project | No model, setup or run count | The card did not look | [tencentdb-agent-memory](../projects/tencentdb-agent-memory.md) |
| hindsight | README: state-of-the-art on LongMemEval, "independently reproduced" by two named institutions. Paper: 91.4% LongMemEval, 89.61% LoCoMo with a larger backbone | README: Vectorize. Paper authors: unstated | Paper: abstract only | The card did not locate the reproduction | [hindsight](../projects/hindsight.md) |
| memos | README table: LoCoMo 88.83, LongMemEval 89.20, eight other scores | The project; the table cites OmniMemEval, from the same GitHub organisation | Not described; no competitor scores listed | None in the sources read | [memos](../projects/memos.md) |
| cognee (comparison page) | BEAM 10M: 67% against Mem0 48.6% | Cognee | No date or evaluator; Cognee's settings unstated; score widgets show placeholder zeros | None | [cognee](../projects/cognee.md) |
| supermemory | README: first place on LongMemEval, LoCoMo and ConvoMem. Research page: 97% Recall@20 on LongMemEval-S | The project | Only for LongMemEval-S (gpt-4o judge); no scores for the other two | No third-party evaluation named | [supermemory](../projects/supermemory.md) |
| honcho | README: "has defined the Pareto Frontier of Agent Memory" | The project | Unchecked: the card points to an evals page it did not read | Unchecked | [honcho](../projects/honcho.md) |

**Reading.** LoCoMo appears in rows for mem0, cognee, graphify, memori, openviking, m-flow, basic-memory, mirix and hindsight. The [Mem0 entry](../projects/mem0.md) records a blog audit of LoCoMo itself (author's affiliation unstated): 99 score-corrupting errors in 1,540 questions, and a judge that accepted 62.81% of deliberately wrong answers. If that audit holds, it bears on every LoCoMo figure above; no entry tests it.

### Fast-growth repositories in the newest snapshot

The [snapshot of 20261030 19:13 UTC](../landscape/20261030_1913-github/README.md) flags `fast-growth` when stars per day reach 150. That is an average over the repository's life, not a trend, and it does not say how the stars arose. None of the nine carries another flag. Stars are unvetted signals; no conclusion is drawn.

| Repository | Stars | Created | Stars/day | Forks per 100 stars | Entry | Star timeline examined? | What the entry read |
|---|---|---|---|---|---|---|---|
| book-to-skill | 36,578 | 20260501 | 200.98 | 10.6 | none (left out: a converter) | no | n/a |
| claude-mem | 105,932 | 20250831 | 249.84 | 8.81 | [claude-mem](../projects/claude-mem.md) | No: endpoint returned 404 | 300 contributors; 2,268 of 2,320 issues closed; README has a Trendshift badge, a star-history chart and a section on a token "created by a 3rd party", unchecked |
| codegraph | 75,999 | 20260118 | 267.6 | 6.61 | [codegraph](../projects/codegraph.md) | Unstated | 49 contributors; no launch explanation |
| graphify | 139,356 | 20260403 | 663.6 | 9.53 | [graphify](../projects/graphify.md) | No: 404, also on a second repository | Forks, issues and pull requests created steadily from week one; one account holds 47% of listed contributions; 135 of 2,612 pull requests merged; outside counts: 7,311 (blog, about 20260407), 63.2K (20260608) |
| headroom | 78,365 | 20260107 | 265.64 | 7.79 | none (left out: context compression) | no | n/a |
| hello-agents | 85,424 | 20250907 | 204.36 | 12.44 | none (left out: a tutorial) | no | n/a |
| hindsight | 56,608 | 20251030 | 155.09 | 12.03 | [hindsight](../projects/hindsight.md) | No: 404 | 291 contributors; project posts give 20,000 stars on 20260814, 40,000 on 20260928, 50,000 on 20261015 |
| MiroFish | 82,864 | 20251126 | 245.16 | 15.12 | none (left out: a prediction engine) | no | n/a |
| Understand-Anything | 89,043 | 20260315 | 388.83 | 8.47 | [understand-anything](../projects/understand-anything.md) | Unstated | 64 contributors (snapshot lists 75, gap unexplained); Trendshift badge |

Three unflagged entries also could not read a star timeline: [openviking](../projects/openviking.md) (REST 404; the GraphQL count returned 0), [tigerless-agent-memory](../projects/tigerless-agent-memory.md) and [code-graph-rag](../projects/code-graph-rag.md) (both 404). Four of the nine have no entry, so no entry examined them. The [selection file](../landscape/20261030_1922-selection.md) notes the stargazer endpoint returned 404 for at least one repository.

## Evidence for

What lets a reader check a figure, as the entries record it:

- **Published harnesses and result files:** Cognee's BEAM and LoCoMo harnesses; Mem0's `memory-benchmarks` repository (Apache-2.0); fast-graphrag's scripts and results; code-graph-rag's oracle-scored tests; Basic Memory's matrix file.
- **Stated limits:** code-review-graph, Zep's paper, Cognee's report and OpenViking's benchmark guide each list their own weaknesses.
- **Independent studies of graph methods** ([papers and benchmarks, section 3](../papers-benchmarks/README.md#3-does-a-graph-help)):

| Study (who ran it) | Result as the file reports it | Limit the file records |
|---|---|---|
| Han et al. (authors of a GraphRAG survey) | Graph methods gain on multi-hop questions (about 3 points at 8B to about 9 at 70B); plain RAG matches or beats them on single-hop | One configuration; judge position bias |
| GraphRAG-Bench (Xiang et al.) | Novel, complex reasoning: RAG with rerank 42.93, HippoRAG2 53.38; fact retrieval 60.92 against 60.14 | Authors built the benchmark for denser graphs; Table 17 conflicts with Table 9 |
| RAGSearch (Fan et al.) | +27.23 on multi-hop, single-shot | Best of five graph variants against one dense baseline; different knowledge sources |
| BM25 Wins at Scale (Wang et al.) | At 1,144 documents BM25 74.7, HippoRAG 2 66.2, LightRAG 48.0, MS-GraphRAG 45.9; builds stopped at 2,254 (LightRAG) and 8,750 (MS-GraphRAG) documents | Synthetic corpus with exact lexical anchors |
| Is GraphRAG Needed? (AWS, Cisco) | Hit@1: text only 0.6147; GraphRAG on a KG computed from documents 0.5596 | One dataset, one LLM, single runs |
| Bao et al., agent memory | Raw-RAG first in six of seven settings, by 0.13 to 5.53 points | Abstract only; which systems count: unstated |

## Evidence against, or limits

- **Mismatches between a project's own documents:** PageIndex (a different system measured; 98.7% against 90.7% on one counting rule); tencentdb-agent-memory (+59% against +58%); Memori (87% against 81.95%); MiniRAG (claim against its own Table 1); mem0 (per-category LoCoMo scores differ between pages); graphify (`BENCHMARKS.md` names a shared embedder, the README says no embeddings). **Reading:** a mismatch is two documents disagreeing, not a finding that either number is wrong.
- **Baseline dependence:** a Graphify pull request of 20261011 changed the benchmark to measure the real answer, and one ratio moved from 11.0x to 1,893.5x ([graphify](../projects/graphify.md)).
- **What the benchmarks leave out** ([section 5](../papers-benchmarks/README.md#5-what-the-benchmarks-do-not-measure)):

| Dimension | State in the sources read |
|---|---|
| Build and query cost | Most accuracy benchmarks report none; graph builds did not finish at scale in one study |
| Corpus size | Evaluations "generally remain at a fixed, relatively small corpus size"; rankings changed with size |
| Graph structure in the corpus | Common sets have average entity-graph degree 0.60 to 0.86; GraphRAG-Bench's own sets 1.05 and 2.27 |
| Abstention, freshness | Only some sets test abstention; no study of answer quality after incremental updates was found |
| Retrieval against answer | Ground-truth entities 83.5% in retrieval, 47.9% in the answer |
| Judge reliability, variance | Verdicts changed with presentation order; several studies run each system once |

## What is unresolved

- Whether Mem0's headline holds on the open-source build without Temporal Reasoning: unstated.
- Whether the released PageIndex SDK has a scored independent run: none found.
- Whether any measurement sits behind Graphify's 80%: none found. Its 71.5x figure is not on the same baseline; 80% equals 5x.
- Whether the reproduction Hindsight's README names exists.
- Whether any LoCoMo score survives the audit above.
- Star timelines: six entries could not read one; two more state nothing.
- The papers file holds no study of Graphify, PageIndex, Cognee, Basic Memory or OpenViking, according to those entries.

## Signals to watch

Each can be checked against the repository or page named.

- A third-party run of Mem0's `memory-benchmarks` harness (created 20260330), or a Mem0 page naming the judge model.
- A scored run in the third-party harness the PageIndex entry reports as "Not yet run" (read 20261030), or a FinanceBench figure for the SDK.
- The Graphify README banner gaining a link or method for "80%" (the 20261010 commit added none).
- A page that locates the Virginia Tech and Washington Post reproduction Hindsight's README cites.
- A Cognee row in a later version of arXiv 2610.30755 (one version at 20261022).
- The next landscape snapshot: its `prev_stars` and `star_delta` columns show growth between snapshots; a stargazer endpoint that answers would allow a timeline check.
- A correction to the GraphRAG-Bench Table 17 caption (v3, 20260222).
- The codebase-memory-mcp README stating its 83% against 92% quality figures beside its token claims.

## Sources

Entries: [mem0](../projects/mem0.md), [pageindex](../projects/pageindex.md), [graphify](../projects/graphify.md), [cognee](../projects/cognee.md), [codebase-memory-mcp](../projects/codebase-memory-mcp.md), [hindsight](../projects/hindsight.md), [memos](../projects/memos.md), [tencentdb-agent-memory](../projects/tencentdb-agent-memory.md), [llm-wiki-nashsu](../projects/llm-wiki-nashsu.md), [lightrag](../projects/lightrag.md), [microsoft-graphrag](../projects/microsoft-graphrag.md), [graphiti](../projects/graphiti.md), [openviking](../projects/openviking.md), [fast-graphrag](../projects/fast-graphrag.md), [code-graph-rag](../projects/code-graph-rag.md), [basic-memory](../projects/basic-memory.md), [codegraph](../projects/codegraph.md), [code-review-graph](../projects/code-review-graph.md), [claude-mem](../projects/claude-mem.md), [understand-anything](../projects/understand-anything.md); the "What it is" paragraphs of the others linked above.

1. [Papers and benchmarks, sections 3 and 5](../papers-benchmarks/README.md) : independent studies and gaps; numbers copied from that file (read 20261030 19:59 UTC)
2. [Landscape snapshot README, 20261030 19:13](../landscape/20261030_1913-github/README.md) : flag rules (read 20261030 19:59 UTC)
3. [Landscape snapshot data](../landscape/20261030_1913-github/repos.tsv) : stars, creation dates, stars per day and forks per 100 stars of the nine flagged rows (read 20261030 19:59 UTC)
4. [Selection file](../landscape/20261030_1922-selection.md) : why four flagged repositories have no entry (read 20261030 19:59 UTC)
