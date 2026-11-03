---
type: trend
shift: one-shot lookup -> learned multi-turn traversal
status: growing
order: 4
updated: 20261102 23:27 UTC
---

# Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal

This page answers what changes when a [large language model](../index/large-language-model.md) (LLM), not a fixed pipeline, decides which part of a [knowledge graph](../index/knowledge-graph.md) to read next, and when that model was trained for the job with [reinforcement learning](../index/reinforcement-learning.md) (RL). It says which repositories and papers do this, what has been measured and by whom. The activity is in papers: at the 20261030 snapshot no repository in this family was active [24], and the one outside benchmark that compares them finds a training-free [agent](../index/agent.md) ahead of a trained one on three [multi-hop question answering](../index/multi-hop-question-answering.md) sets [17].

> **Distinctive because** a model is trained to choose its next retrieval step over an existing graph, across several turns; the reward is mainly the final answer [4]. The nearest neighbour is [vectorless retrieval](./reasoning-over-structure.md): there an off-the-shelf model reasons through a document tree and nothing is trained [23].

## Why it emerged

The sourced facts come first. The abstract of Graph-R1 lists "fixed one-time retrieval" among the remaining problems of GraphRAG [3]; GraphRAG-R1's says query and retrieval are "largely based on pre-defined heuristics" [8]. Think-on-Graph (first version 20230715) has an LLM agent run beam search over a knowledge graph and calls itself a "training-free method" [7]. Search-R1 (first version 20250312) trained a model with reinforcement learning to write several search queries, and says prompting a model to use a search engine "is often suboptimal" [6]. Graph-R1 (20250729) and GraphRAG-R1 (20250731) train agents that retrieve from a graph [3][8]. In 2026 the work concentrates on the reward [12][14] and on cheaper training [10][13].

The earlier steps are told in chapter 1: [Language models meet retrieval](../history/language-models-meet-retrieval.md) dates REALM and RAG, which fixed retrieve-then-generate, and ReAct (20221006), in which a model interleaves reasoning with actions that reach external sources such as knowledge bases. The history adds the one-shot retrieve-then-generate pattern that this trend departs from.

*Reading:* three earlier pieces seem to have been combined: the known limit of one-shot graph retrieval, prompted graph walking (Think-on-Graph) and RL-trained search queries (Search-R1). The dates fit that order and Graph-R1 lists Search-R1 as a baseline [4]. No source read states the chain, though: neither abstract names Search-R1 or Think-on-Graph as an origin, and the Graph-R1 text, searched for it, does not mention Think-on-Graph [4]. No independent history of the move was found.

## Why it matters

Graph-R1's authors report two costs on [2WikiMultiHopQA](../datasets/2wikimultihopqa.md) (first-party). Building the hypergraph with GPT-4o-mini took 5.69 s and $2.81 against 6.76 s and $4.14 for HyperGraphRAG (the text says per 1K tokens, the table header per 1M). At query time Graph-R1 took 7.0 s and $0 generation cost against 9.6 s and $8.76 for HyperGraphRAG; the passage read does not say whether training hardware is counted [4]. The authors of Search-on-Graph-R1 say prompting a frontier model to explore a graph is "costly to deploy" and train an 8B model instead (first-party) [13]. [RAGSearch](../benchmarks/ragsearch.md) asks whether agentic search can reduce "the need for costly GraphRAG pipelines", which is a test of an assumption of the whole graph chapter [17].

*Reading:* the shift is from engineering a retrieval pipeline to training a policy. That cost moves from the index to the query is not shown: the graph is still built up front, training cost is outside the per-query figures, and RAGSearch finds GraphRAG "remains advantageous" for complex multi-hop reasoning "when its offline cost is amortized" [4][17].

## How it works

### The loop

The model reads the question, reasons, issues a retrieval action, reads the result and repeats until it answers. Graph-R1 calls this a "think, generate query, retrieve subgraph, rethink" cycle [5]; GraphWalker's agent emits a reasoning block, a tool call and the returned information at each turn [11].

### What the model may do

| Design | Action space | Example |
|---|---|---|
| Query only | writes a sub-query; code outside the model finds entities and facts | Graph-R1's search tool has one required argument, `query` [5] |
| Graph primitives | calls functions that expose edges | GraphWalker: `get_relations`, `get_triples` [11]; Search-on-Graph-R1: a live `Search` tool over Freebase [13] |
| Analyser sets bounds | a model fixes seeds, depth and stopping per question; nothing is trained | MOSAIC [16] |

### The graph

The graph comes first and is not this trend's contribution. Graph-R1 builds a knowledge [hypergraph](../index/hypergraph.md) with GPT-4o-mini extraction, using methods from [graph-based RAG](./graph-based-rag.md) [4]; the question-answering papers on [Freebase](../index/freebase.md) query an existing graph [13]. Here the trained policy, not the graph, is the part the papers contribute. Another way to walk a graph is an algorithm: [HippoRAG](../projects/hipporag.md) applies a [personalized PageRank](../index/personalized-pagerank.md)-style propagation, so a fixed procedure, not the model, chooses the hops [17]. GraphRAG-R1's own retrieval service is "based on" HippoRAG [25].

### Training

Graph-R1 trains with [GRPO](../index/grpo.md) (Group Relative Policy Optimization) and an outcome-directed reward [4]. GraphRAG-R1 adds two process-constrained reward functions [8], and RANGER lets an LLM score the paths a small policy takes [15]. The 2026 papers attack the answer-only reward. HyperGraphPro says outcome-level rewards are sparse and the retriever ignores graph topology [14]. PathRouter names "answer-path reward aliasing": a correct answer reached by a shortcut is rewarded [12]. GraphWalker and Search-on-Graph-R1 first run [supervised fine-tuning](../index/supervised-fine-tuning.md) (SFT) on synthetic or teacher trajectories, then a light RL stage [10][13]; the second builds its teacher trajectories by handing a frontier model each question's gold [SPARQL](../index/sparql.md) query [13]. Graph-R1 reports training on 4 A100 80 GB graphics processing units (GPUs) [4].

### Learned controllers for memory

A parallel strand trains the same kind of policy over an agent's [memory](../index/agent-memory.md) store. Memory-R1 trains a manager to choose ADD, UPDATE, DELETE or NOOP, with Proximal Policy Optimization (PPO) and GRPO and 152 training question pairs; its abstract calls most pipelines "static and heuristic-driven" [20]. Uni-Mem (20261021) learns memory construction and retrieval under one policy [21]. MemComposer (20261015) learns which memories to include, how many and in what order [22]. A counter-reading comes from another group: raw dense retrieval plus reranking ranked first in six of seven settings against compared agentic memory systems, on conversation benchmarks (abstract only) [19].

*Reading:* this strand is grouped here because the technique and the claim match: replace a fixed rule with a policy rewarded on task success. It is not a trend of its own because what it stores is the business of [agent memory](./agent-memory.md); only the learned controller is distinctive, and the store is not a graph.

## Representative projects

No repository here has a page in the projects chapter: none passed the activity test (pushed within 90 days of the 20261030 19:54 UTC snapshot) [24]. Stars are signals: the figures are from the snapshot, and a repository missing from it has none here; licences are from the LICENSE files; "last push" is the GitHub API value read 20261102 unless marked.

| Repository | Role | Licence | Stars | Last push |
|---|---|---|---|---|
| [LHRLAB/Graph-R1](https://github.com/LHRLAB/Graph-R1) | RL agent over a hypergraph; International Conference on Machine Learning (ICML) 2026 | MIT | 599 (snapshot 20261030 19:54 UTC) | 20261102 (two README-only commits); 20260430 in the 20261030 snapshot, 182 days [5][24] |
| [XuShuwenn/GraphWalker](https://github.com/XuShuwenn/GraphWalker) | SFT then RL on a knowledge graph; 7B weights on Hugging Face | MIT | not in the snapshot | 20260728 [11][30] |
| [ycygit/GraphRAG-R1](https://github.com/ycygit/GraphRAG-R1) | process-constrained RL; weights linked in README; release v1.0 | MIT | not in the snapshot | 20260228 [25][31] |
| [DataArcTech/GraphSearch](https://github.com/DataArcTech/GraphSearch) | training-free search workflow of six modules [9][17] | Apache-2.0 (the README badge says MIT) | not in the snapshot | 20260409 [28] |
| [PeterGriffinJin/Search-R1](https://github.com/PeterGriffinJin/Search-R1) | plain-text RL parent | Apache-2.0 | not in the snapshot | 20251113 [29] |
| [TencentCloudADP/youtu-graphrag](https://github.com/TencentCloudADP/youtu-graphrag) | prompted agentic retrieval with reflection; its README mentions no policy training | custom, academic use only (read-only reference) | 1,271 (snapshot 20261030 19:54 UTC) | 20260226 [24][27] |

Graph-R1 offers data and a pre-built hypergraph through a file-sharing link but no trained weights. Of its three open issues about checkpoints (20251127 to 20260827), two ask for the weights and one is a Hugging Face team member's invitation to host them there [5]. On 20261102 it received two commits, both to the README only [5]. The nearest active repository is [RManLuo/gfm-rag](https://github.com/RManLuo/gfm-rag), Apache-2.0, 309 stars at the 20261030 19:54 UTC snapshot: it trains a graph neural network as a one-shot retriever, so it is learned but not multi-turn [24][26].

## Fundamental papers

The papers chapter keeps five (Think-on-Graph, KGP, Search-R1, Graph-R1 and Memory-R1); GraphRAG-R1, GraphSearch and RAGSearch, named below, are in its further reading; see [the group page](../papers/learned-graph-traversal.md). The ones this page leans on: Think-on-Graph (2023) [7], the prompted precursor; Search-R1 (2025) [6], origin of the training recipe; Graph-R1 (2025) [3] and GraphRAG-R1 (2025) [8], its graph versions; GraphSearch (2025) [9], the training-free counterpart; RAGSearch (2026) [17], the evaluation of record.

## What is measured, and by whom

Datasets and benchmarks named: [HotpotQA](../datasets/hotpotqa.md), [2WikiMultiHopQA](../datasets/2wikimultihopqa.md) (2Wiki), [MuSiQue](../datasets/musique.md), [Natural Questions](../datasets/natural-questions.md) (NQ), [PopQA](../datasets/popqa.md), [TriviaQA](../datasets/triviaqa.md), [WebQSP](../datasets/webquestionssp.md), [ComplexWebQuestions](../datasets/complexwebquestions.md) (CWQ), [GrailQA](../datasets/grailqa.md), [STaRK](../benchmarks/stark.md)-Prime; most are multi-hop question answering sets. Experiments that test this trend: none.

| Study | Who ran it | Result | Caveat |
|---|---|---|---|
| Graph-R1 paper | first-party | average F1 (a score that balances precision and recall), Qwen2.5-7B-Instruct block of its Table 2: Graph-R1 57.82, Search-R1 46.19, standard retrieval-augmented generation (RAG) 15.89; 128 test questions per dataset [4] | the text says 57.28 where the table says 57.82, and compares with standard RAG 32.05, which is the GPT-4o-mini-based row, so it mixes two backbones [4] |
| RAGSearch | its four authors are not on Graph-R1's author list (names compared) | Contain-EM (contain exact match), 7B: Graph-R1 protocol with best of five graph backends against Search-R1 on dense retrieval: HotpotQA 53.42 vs 35.76, 2Wiki 66.25 vs 33.56, MuSiQue 40.82 vs 14.42; NQ 46.71 vs 48.72 [17] | best of five backends; dense side retrieves from a 2018 Wikipedia dump; the graph side's corpus is unstated in the passages read |
| RAGSearch, same table | same | training-free GraphSearch on the best graph backend: HotpotQA 58.64, 2Wiki 79.88, MuSiQue 55.26, above the trained Graph-R1 row on all three [17] | one benchmark; 7B backbones as labelled |
| Chen et al. (Association for Computational Linguistics, ACL, 2026, GEM Workshop) | its eight authors are on none of the author lists of Graph-R1, GraphRAG-R1, GraphWalker, GraphSearch, PathRouter or Search-on-Graph-R1 (names compared); it tests no trained policy | STaRK-Prime Hit@1 (the share of questions whose first result is correct): agent with a document tool 0.6881; same agent plus a predefined graph tool 0.6055 [18] | one dataset; tools prompted, not trained |
| GraphWalker | first-party | CWQ 79.6 [exact match](../index/exact-match.md) (EM), WebQSP 91.5 EM, "SOTA among agentic KGQA methods" (state of the art; [knowledge-graph question answering](../index/knowledge-base-question-answering.md)) [11] | README claim, own comparison |
| Search-on-Graph-R1 | first-party | 8B beats every frozen frontier-LLM system in its comparison [13] | abstract only |

## Assessment

*Reading:* the strength is a real design change. Retrieval becomes a learned sequence of moves, and 7B and 8B models are reported to manage it, with weights public for GraphWalker and GraphRAG-R1 [4][11][13][30][31]. The weaknesses are in the evidence. Nearly every positive number is first-party. The one outside benchmark shows the graph helping an RL agent on multi-hop sets, but its training-free agent beat the trained one, so training is not shown to be the source of the gain [17]. A tool-calling agent that gained a graph tool scored lower in another outside test [18]. Graph-R1's own protocol tests on 128 questions per dataset [4], whereas RAGSearch reports "results on full test sets" [17]. Reward design is still being patched [12][14].

On growth the data are thin. Keyword hits for the RL, knowledge-graph and agent query rose from 18 to 44 between two one-year windows [1]. Read by title with one rule for both windows, on-topic hits rose from 5 to 12, a rise like that of the LLM-agent control query, whose hits rose from 6,068 to 15,158 (2.5 times) [1][2]. These are counts of query hits, not of papers in the field, and the title calls are judgement; so the status growing rests on small, noisy counts, and the data show no growth beyond the general rise in agent papers. Heading: more reward and training recipes, plus a harder test of whether a trained policy beats a prompted one at matched cost, which no source here has run.

## Signals to watch

| Signal | Where to check |
|---|---|
| Graph-R1 weights published | issues #19, #22, #24 of the repository [5] |
| A repository in this family pushed within 90 days, with a release | the next GitHub snapshot [24] |
| Code for PathRouter, Search-on-Graph-R1, RANGER (no code link in the abstracts read) | their arXiv pages [12][13][15] |
| A matched-cost comparison of trained and prompted graph agents | a later version of RAGSearch [17] |
| Trained memory controllers (Memory-R1 and kin) inside a product | [agent memory](./agent-memory.md) |

## Sources

Keyword counts are "N results for query Q", not counts of papers in the field. Times are UTC, read 20261102.

1. https://export.arxiv.org/api/query : query `(abs:"reinforcement learning" OR abs:GRPO OR abs:"policy optimization") AND (abs:"knowledge graph" OR abs:GraphRAG OR abs:"graph retrieval" OR abs:"graph-based RAG") AND (abs:agent OR abs:agentic OR abs:"multi-turn")` with submittedDate 20251102 to 20261102 gave 44 results, 18 for 20241102 to 20251101. Titles read with one rule for both windows (on topic: an LLM or RL agent that retrieves from or reasons over a graph; borderline: graph or RL but not the traversal; not: other): 20251102 window 12 on topic, 12 borderline, 20 not (robotics, networking, code agents); 20241102 window 5, 5, 8. An earlier reading of the new titles gave about 13 on topic (read 20261102 20:52).
2. https://export.arxiv.org/api/query : query `(abs:agent OR abs:agents OR abs:agentic) AND (abs:LLM OR abs:LLMs OR abs:"language model" OR abs:"language models")`, same dates: 15,158 results against 6,068 (read 20261102 20:52).
3. https://arxiv.org/abs/2507.21892 : Graph-R1 abstract, v1 20250729, v2 20260602, "Accepted by ICML 2026 main conference" (read 20261102 20:50).
4. https://arxiv.org/html/2507.21892 : Table 2 (both backbone blocks), text on 57.28 and 32.05, 128 test instances, GPT-4o-mini construction, 4 A100 GPUs, construction and generation cost on 2Wiki, baselines list, outcome-directed reward (read 20261102 20:50).
5. https://github.com/LHRLAB/Graph-R1 : README, LICENSE (MIT), search tool, commits of 20261102 (README.md only), open issues #19, #22, #24, file-sharing links for data, no weights offered (GitHub API, read 20261102 20:53).
6. https://arxiv.org/abs/2503.09516 : Search-R1 abstract, v1 20250312 (read 20261102 20:50).
7. https://arxiv.org/abs/2307.07697 : Think-on-Graph abstract, v1 20230715 (read 20261102 20:50).
8. https://arxiv.org/abs/2507.23581 : GraphRAG-R1 abstract, v1 20250731 (read 20261102 20:50).
9. https://arxiv.org/abs/2509.22009 : GraphSearch abstract, "six modules" (read 20261102 20:50).
10. https://arxiv.org/abs/2603.28533 : GraphWalker abstract, COLM 2026 (read 20261102 20:51).
11. https://github.com/XuShuwenn/GraphWalker : README (tool names, results, weights link), LICENSE (MIT), last push (GitHub API, read 20261102 20:53; the star count read then is not used).
12. https://arxiv.org/abs/2606.16409 : PathRouter abstract (read 20261102 20:51).
13. https://arxiv.org/abs/2607.18481 : Search-on-Graph-R1 abstract (read 20261102 20:51).
14. https://arxiv.org/abs/2601.17755 : HyperGraphPro abstract (read 20261102 20:10).
15. https://arxiv.org/abs/2610.28010 : RANGER abstract (read 20261102 20:10).
16. https://arxiv.org/abs/2609.11065 : MOSAIC abstract (read 20261102 20:10).
17. https://arxiv.org/html/2604.09666 : RAGSearch, Table 1, setup text, abstract (training-free GraphSearch, "results on full test sets", offline cost), author list (read 20261102 20:51).
18. https://arxiv.org/html/2606.25656 : Chen et al., scenario table, STaRK-Prime, scenario 8 and 9; https://arxiv.org/abs/2606.25656 : author list and "Accepted to ACL 2026 GEM Workshop" (read 20261102 20:51).
19. https://arxiv.org/abs/2610.30755 : Raw-RAG ("Is Complex Agentic Memory Always Needed?") abstract (read 20261102 20:10).
20. https://arxiv.org/abs/2508.19828 : Memory-R1 abstract (read 20261102 20:10).
21. https://arxiv.org/abs/2610.29671 : Uni-Mem abstract (read 20261102 20:10).
22. https://arxiv.org/abs/2610.21091 : MemComposer abstract (read 20261102 20:10).
23. https://github.com/VectifyAI/PageIndex : README ("agentically search that tree with LLM reasoning"; chat model chosen by the user) (read 20261102 20:12).
24. ../../kb-kg/landscape/20261030_1954-github/repos.tsv : snapshot 20261030 19:54 UTC rows for stars, last push, days since push (read 20261102 20:54).
25. https://github.com/ycygit/GraphRAG-R1 : README (retrieval service "based on HippoRAG", weights link), LICENSE (MIT), release v1.0, last push (GitHub API, read 20261102 20:53; the star count read then is not used).
26. https://github.com/RManLuo/gfm-rag : README and licence (read 20261102 20:13).
27. https://github.com/TencentCloudADP/youtu-graphrag : README and LICENSE text (academic-use clause) (read 20261102 20:13).
28. https://github.com/DataArcTech/GraphSearch : LICENSE (Apache-2.0), README badge (MIT), last push (GitHub API, read 20261102 20:53; the star count read then is not used).
29. https://github.com/PeterGriffinJin/Search-R1 : LICENSE (Apache-2.0), last push (GitHub API, read 20261102 20:53; the star count read then is not used).
30. https://huggingface.co/api/models/xushuwen23/GraphWalker-7B : model exists, public, not gated (read 20261102 20:54).
31. https://huggingface.co/api/models/yuchuanyue/GraphRAG-R1 : model exists, public, not gated (read 20261102 20:54).
