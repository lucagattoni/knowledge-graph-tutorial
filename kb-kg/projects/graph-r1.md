---
slug: graph-r1
repo: LHRLAB/Graph-R1
tier: deep
category: core
snapshot: 20261030 18:58 UTC
---

# Graph-R1

How to read the markers. **[n]** is a numbered source at the end, with the time it was read.
**(J)** marks a statement carried over from the July 2026 investigation [18] (written 20260725 15:30 UTC),
which cited the paper section named beside it; this run did not re-read that section. **(computed)** marks
arithmetic done here on figures quoted from a source. **Unstated** means the sources read say nothing.

| | |
|---|---|
| Repository | https://github.com/LHRLAB/Graph-R1 [1] |
| Licence | MIT, from the `LICENSE` file ("Copyright (c) 2025 Haoran Luo") [2]. The README states no licence, so there is nothing to disagree with [3]. |
| Language | Python (GitHub primary language) [1] |
| Stars, forks | 599, 76 (20261030 18:58 UTC) [1] |
| Created, last push | 20250311 05:49 UTC, 20260430 22:56 UTC [1] |
| Latest release | none: the latest-release call returned 404 and the tag list was empty (20261030 18:58 UTC) [7] |
| Status | quiet: 183 days since the last push at the snapshot (computed); not archived [1] |
| Paper, docs | arXiv 2507.21892 [11]; ICML 2026 proceedings, PMLR 306:82220-82240 [14]; the README is the only documentation [3] |

## What it is

Graph-R1 is the official code release of the paper "Graph-R1: Towards Agentic GraphRAG Framework via
End-to-end Reinforcement Learning" (Luo et al.) [3][11]. A small language model (Qwen2.5 at 1.5B, 3B or 7B)
is trained with reinforcement learning (GRPO) to run a multi-turn loop of think, query, retrieve, rethink
and answer against a knowledge hypergraph built from the corpus [12][13]. The authors describe it as the
first agentic GraphRAG framework trained end to end with reinforcement learning [13]; that priority claim is
theirs and was not checked. The paper is listed as accepted at the ICML 2026 main conference [11][14].
The repository is research code: one contributor account with 103 commits [1], and the ten most recent
commit messages are all the single word "add" [4].

## How it works

### The agentic loop

| Element | What the sources say |
|---|---|
| Policy | One LLM, hierarchical: a free-text reflection that judges whether knowledge is sufficient; an intent (`query then retrieve`, or `answer`); and a content part, either a retrieval query or the final answer [12][13]. |
| Who retrieves | The environment. The model emits natural-language sub-queries only; entity matching, hyperedge similarity and fusion run inside the environment (J, §4.1-4.2). The repository's search tool lists `query` as its required argument [10]. No graph-walking primitive (expand a node, follow an edge) is exposed to the model (J). |
| Wire format | `<think>...</think>`, then either `<query>{"query": "..."}</query>` or `<answer>...</answer>`; results return in a `<knowledge>` block as a JSON list of facts, each with a `<coherence>` score (J, App. A). The retrieval code builds exactly that shape: a list of `{"<knowledge>": fact, "<coherence>": score rounded to 3 places}` [8]. |
| What one retrieval returns | The top-k n-ary relational facts: natural-language sentences with their entity sets, not a subgraph object, paths or node identifiers (J). Knowledge stays in language space. The README's wording is "retrieve subgraph" [3]; the code returns scored fact strings [8]. |
| Termination | The model chooses `answer` instead of `query`; there is also a hard cap of T turns [13]. The value of T is **unstated** in the sources read. Trained models average 2.3 to 2.5 turns [13]. No environment-side stop signal (J). |
| Facts per turn | The paper's hyperparameter table gives Top-K = 5 retrieved items per turn [12]. The retrieval server in the repository pre-selects 5 entities and 5 hyperedges from FAISS and passes `top_k=10` to the query call [9]. Which value the reported runs used is **unstated**. |

### The hypergraph it traverses

- **Construction.** Documents are split into 1200-token chunks with 50 tokens of overlap. GPT-4o-mini does
  n-ary relation extraction: each chunk yields facts `(h_i, V_hi)`, where `h_i` is a natural-language
  sentence (a "knowledge segment") that becomes a hyperedge connecting the entity set `V_hi` [12]. Entities and
  hyperedges are embedded with bge-large-en-v1.5 into two vector bases [12]. Entities carry name, type and
  description (J, App. J); the code stores an `entity_name` per entity [9].
- **Reading of the design.** A hyperedge is a sentence with linked entities. The fact text is kept verbatim,
  so the graph acts as an index over sentences, not a replacement for them (J, consistent with [12]).
- **Relation to the predecessor.** The same group's HyperGraphRAG supplied the extraction approach [3][17]. The
  paper credits itself with improvements in parallelisation, prompt efficiency, storage layout and
  vectorisation relative to HyperGraphRAG, without figures in the section read [12]. The July note adds that
  the confidence-scoring step of HyperGraphRAG's prompt is dropped to save cost (J); not re-verified.
- **Size on 2WikiMultiHopQA.** 120,499 nodes and 98,073 hyperedges [12].
- **Build entry points.** `script_build.py` builds the hypergraph (needs an OpenAI key for the extractor);
  the README also offers a pre-built hypergraph for download from a file-sharing service [3].

### Retrieval

- **Dual path, fused by reciprocal rank.** (1) Entity-based: extract entities from the query, find similar
  entity nodes, collect their hyperedges. (2) Direct: embed the query and find similar hyperedges. The two
  ranked fact lists are merged by reciprocal rank aggregation, and the top-k facts are returned [12].
- **What the code does.** Each list contributes `1/(position+1)` for every position a fact occupies, scores are
  summed, the facts are sorted and cut to `top_k`, and the sum is returned as `<coherence>` [8]. A fact that
  appears several times in a list is counted each time, because the loop adds per occurrence [8]
  (computed from the code as read). The score is therefore a fusion score, not a similarity.
- **Retrieval service.** `script_api.py` serves retrieval over HTTP on port 8001. It embeds queries with
  bge-large-en-v1.5 on CPU and searches two FAISS indices, entities and hyperedges [3][9]. The training tool
  posts the batch of queries to that service [10].

### Training

| Setting | Value | Source |
|---|---|---|
| Algorithm | GRPO; the README also ships scripts for REINFORCE++ and PPO | [3][12] |
| Script settings | `adv_estimator=grpo`, KL loss coefficient 0.001 (`low_var_kl`), rollout `n_repeat=5`, train batch 128, prompt, response and tool-response limits 4096, 1 epoch, 4 GPUs per node | [10] |
| Data | Six datasets: 2WikiMultiHopQA, HotpotQA, Musique, NQ, PopQA, TriviaQA. 5,120 training and 128 test instances per dataset. One model is trained per dataset | [3][12] |
| Hardware | "4 NVIDIA A100 GPUs (80GB)" in the paper [12]. The README says the Qwen2.5-3B quick start needs 4 x 48GB GPUs [3] | [3][12] |
| Reward | Trajectory-level: a format reward capped at 1.0 for well-formed steps plus an answer reward, token-level F1 against the gold answer, **granted only when the format is valid** [12][13]. Exact form `R(tau) = -1.0 + R_format + I{R_format = 1.0} * R_answer`, with 0.5 per well-formed step (J, §4.3) | [12][13] |

## Cost and operating profile

| Item | Figure | Source |
|---|---|---|
| Build, 2WikiMultiHopQA | One paid LLM pass (GPT-4o-mini) over the whole corpus. 5.69 s per 1K tokens and $2.81. The table header says the cost is per 1M tokens; the paper's body text says "$2.81 per 1K tokens". The paper contradicts itself and the unit is **unresolved** here | [12][13] |
| Build, baselines (same table) | GraphRAG 8.04 s and $3.35 (7,771 nodes, 4,863 edges); HyperGraphRAG 6.76 s and $4.14 (173,575 nodes, 114,426 edges) | [12] |
| Embedding after build | About 219K items, the sum of nodes and hyperedges (computed from [12]) | [12] |
| Query | Generation cost $0 per 1K queries and 7.0 s per query, against $8.76 per 1K queries and 9.6 s for HyperGraphRAG (GPT-4o-mini) and $3.97 for GraphRAG | [12][13] |
| What "$0" covers | Per-query LLM spend only. The policy runs locally and retrieval runs on a local service [3][9]. Whether hardware cost is counted is **unstated** | [3][9][12] |
| Training | 4 x A100 80GB reported [12]; wall-clock or GPU-hours **unstated** (an open issue asks, #9, 20250818; its replies were not read [6]) | [6][12] |
| Software | Python 3.11.11, PyTorch 2.4.0 (cu124), flash-attn, a `verl/` directory in the repository (described in July as a fork of verl, not re-checked) | [3] |
| Fully local? | Query time yes, once the policy and the hypergraph exist. Build needs an OpenAI API key unless the pre-built hypergraph is downloaded. Datasets and the pre-built hypergraph are hosted on a file-sharing service, not on Hugging Face | [3] |
| Trained weights | No download is offered in the README [3]. Three open issues ask for checkpoints or a Hugging Face release: #19 (20251127), #22 (20260604, from a Hugging Face staff member) and #24 (20260827). No reply from the repository owner was found in their comments (read 20261030) | [3][6] |

## Evidence

All figures are from the paper's v2 text [12][13] unless marked. The paper's own evaluation is the only
evidence found; see the end of this section for third-party work.

**Main results, token-level F1 (paper Table 2, 7B backbones; HyperGraphRAG and StandardRAG use GPT-4o-mini)** [12]

| Method | 2Wiki | HotpotQA | Musique | NQ | PopQA | TriviaQA | Average |
|---|---|---|---|---|---|---|---|
| **Graph-R1 (Qwen2.5-7B)** | 65.04 | 62.69 | 46.17 | 49.87 | 51.22 | 71.93 | **57.82** |
| Search-R1 (7B) | 41.29 | 50.85 | 22.35 | 45.88 | 50.76 | 65.98 | 46.19 |
| R1-Searcher (7B) | 33.96 | 46.36 | 16.63 | 44.93 | 47.12 | 64.76 | 42.29 |
| HyperGraphRAG (GPT-4o-mini) | 21.14 | 37.46 | 20.40 | 22.95 | 29.48 | 44.95 | 29.40 |
| StandardRAG (GPT-4o-mini) | 22.31 | 46.70 | 17.31 | 26.85 | 30.58 | 48.55 | 32.05 |

- **Margin over Search-R1** (computed): 2Wiki +23.75, HotpotQA +11.84, Musique +23.82, NQ +3.99, PopQA +0.46,
  TriviaQA +5.95. The smallest margins are on NQ and PopQA; the July note called these the single-hop sets
  (J, not verified), where the graph adds least.
- **Small test sets.** Each dataset has 128 test instances [12]. One instance is 1/128 = 0.78 points of an
  averaged per-question score (computed), so the PopQA margin of 0.46 is smaller than one question. The paper
  reports no confidence intervals or repeated seeds in the sections read.
- **Text and table disagree.** The body text gives 57.28 F1 for Qwen2.5-7B; Table 2 gives 57.82 [12].
- **Baselines are not equal-budget.** Maximum length is 4096 for the trained models and unlimited for the
  baselines (Table 3) [12]. Graph-R1 is trained per dataset on that dataset's own training split [12].
- **Scale.** Average F1 of 40.09, 51.26 and 57.82 at 1.5B, 3B and 7B; the gap to other RL baselines widens
  with size [13].
- **Ablation.** Removing knowledge construction, multi-turn interaction or reinforcement learning each lowers
  performance; removing RL costs the most [13]. The "w/o R.L." run (same prompt, same graph, untrained model)
  scores average F1 10.74 at 3B and 17.79 at 7B [12]. The 17.79 equals the mean of the two per-dataset values
  listed, 2Wiki 18.25 and HotpotQA 17.33 (computed), so it is a two-dataset average, not a six-dataset one. The
  matching trained figure on those two datasets is 63.87 (computed from Table 2). Hypergraph knowledge with RL
  gave the highest ceiling compared with chunk knowledge or binary-relation graphs [13].
- **What the untrained collapse measures.** A 7B model that cannot follow the loop protocol. This reading is
  the July note's (J); the paper does not test a stronger untrained model.
- **RL algorithm.** GRPO beat REINFORCE++ and PPO; the numbers were not in the sections read [13].
- **Qwen3-4B.** A model already tuned with RL "tends to over-rely on its own internal reasoning" and its
  "overall performance ceiling appears slightly lower"; the numbers sit in a figure not described in the text
  read [12]. The paper tests no model larger than 7B.
- **Efficiency.** Trained models write shorter responses (1200-1500 tokens) and take more turns (2.3 to 2.5)
  than baselines, and reach high F1 with a moderate amount of retrieved content [13].
- **Generation quality.** Seven dimensions; Graph-R1 beats the other RL baselines. Overall 82.4 against 70.3 for
  Search-R1; correctness 86.9, relevance 95.2, logical coherence 88.5 [13]. The judge is **unstated** in the
  sections read. The July note reported "diversity" as the lowest dimension at 51.7 (J, not re-verified).
- **Out of distribution.** Graph-R1 beat Search-R1 when trained on one dataset and tested on others; OOD to
  in-distribution ratios were often above 85 percent and sometimes above 90 percent. In zero-shot tests on five
  specialised sets (medicine, agriculture, computer science, law, mixed), the 3B model beat Search-R1 3B; the
  numbers were not in the sections read [13].
- **Third-party evidence.** None found in this pass. A January 2026 arXiv paper by other authors, HyperGraphPro,
  targets the same agentic hypergraph-RAG setting with progress-aware rewards; its abstract page does not say
  whether it builds on Graph-R1 [15]. An open issue (#7, 20250810) asks why iterative or multi-round retrieval
  baselines were not compared; the owner's reply, read 20261030, says Search-R1 and R1-Searcher are multi-turn
  methods and Graph-R1 adds fine-grained hypergraph representation [6].

## Direction

The README states no roadmap [3]. The repository has no release and no tag [7]. Its only 2026 commit
(20260430 22:56 UTC) changed `README.md` alone (2 lines added, 3 removed), adding the "ICML 2026" label and
the author list [5]. No commit has landed since 20260801 [4]. The API reports 17 open items (issues and pull requests together), several asking for
trained checkpoints and Hugging Face artifacts [1][6]. The same author's earlier HyperGraphRAG repository
was pushed on 20260512, after Graph-R1's last push [17]. No successor project, rename or move was found [1][17].

## Changed since the July 2026 investigation

Read 20261030 18:58 to 19:04 UTC. The July investigation [18] was written 20260725 15:30 UTC.

- **Stars and forks.** 599 stars and 76 forks at 20261030 18:58 UTC [1]. July: about 584 stars and 76 forks.
  Plus about 15 stars in 97 days (computed); forks unchanged.
- **Licence.** Still MIT, read from the `LICENSE` file [2]. No change.
- **Archived.** No [1].
- **Activity.** Last push is still 20260430 22:56 UTC; zero commits since 20260801 [1][4]. July's "one commit in
  2026 (20260430)" still holds. The status is now **quiet** (183 days, computed), where the July note called it
  effectively unmaintained.
- **Release.** None [7].
- **README and architecture.** The only 2026 commit edited the README header and nothing in the code [5]. The
  July analysis of the loop, the hypergraph and the retrieval is not affected. The code read this run
  agrees with it on the wire keys, the reciprocal-rank fusion and the two FAISS indices [8][9].
- **Venue.** July already named ICML 2026. Now confirmed by the arXiv comment field ("Accepted by ICML 2026
  main conference") and by a proceedings entry, PMLR volume 306, pages 82220-82240 [11][14]. The conference
  dates in the proceedings BibTeX are 06 to 11 July [14].
- **Paper versions.** v1 dated 20250729 15:01 UTC, v2 dated 20260602 20:20 UTC; no v3 [11]. The July note
  already cited v2. No change log between versions was visible [12].
- **Correction: facts per turn.** July stated k = 5 per turn as the setting. The paper's table says 5 [12],
  but the repository's retrieval server passes `top_k=10` [9]. Both are stated above; the value used in the
  reported runs is unstated.
- **Correction: cost unit.** July wrote "$2.81 per 1M tokens". The table header says per 1M tokens and the
  paper's text says per 1K tokens [12]. The unit is unresolved; the body now states both.
- **Correction: ablation average.** July wrote "17.8 F1 avg vs 63.9 trained", which reads as a six-dataset
  average. It is a two-dataset average (2Wiki and HotpotQA); the six-dataset trained average is 57.82 [12].
- **Added caveats.** The test sets hold 128 instances each, the paper's text and table disagree on the headline
  average (57.28 against 57.82), and baselines run without the 4096-token cap [12]. None of these was in the
  July note.
- **Not carried over.** July's inference that a frontier model "already possesses most of what GRPO instills"
  is not in the paper, which tests nothing above 7B [12][13]. It is a judgement, not a finding, so it is not
  carried into this entry.
- **Checkpoints.** July did not mention them. Three open issues now ask for trained weights; none has an owner
  reply [6].
- **Successor or rename.** None found. HyperGraphPro (Jan 2026, other authors) is a related follow-up whose link
  to Graph-R1 is unstated on its abstract page [15]. A web search result listed it under the name
  "ProGraph-R1", the title is "HyperGraphPro" on the abstract page; this entry uses the abstract page [15][16].

## Sources

1. https://github.com/LHRLAB/Graph-R1 : repository metadata (stars, forks, licence field, archived flag, dates, topics, description, open-issue count, contributors) through the GitHub API (read 20261030 18:58 UTC)
2. https://github.com/LHRLAB/Graph-R1/blob/main/LICENSE : MIT text and copyright line (read 20261030 18:58 UTC)
3. https://github.com/LHRLAB/Graph-R1/blob/main/README.md : overview, install steps, quick start, hardware note, download links, acknowledgements (read 20261030 18:58 UTC)
4. https://github.com/LHRLAB/Graph-R1/commits/main : commit list, zero commits since 20260801, one in 2026, commit messages (read 20261030 18:58 UTC)
5. https://github.com/LHRLAB/Graph-R1/commit/e44dbff : the 20260430 commit and its README patch (read 20261030 19:03 UTC)
6. https://github.com/LHRLAB/Graph-R1/issues : open issues #7, #9, #19, #22, #24 and their comments (read 20261030 18:59 to 19:03 UTC)
7. https://github.com/LHRLAB/Graph-R1/releases : no latest release (404) and an empty tag list (read 20261030 18:58 UTC)
8. https://github.com/LHRLAB/Graph-R1/blob/main/graphr1/operate.py : fusion and the `<knowledge>`/`<coherence>` output (read 20261030 19:01 UTC)
9. https://github.com/LHRLAB/Graph-R1/blob/main/script_api.py : retrieval server, first 80 lines only (read 20261030 19:01 UTC)
10. https://github.com/LHRLAB/Graph-R1/blob/main/run_grpo.sh and https://github.com/LHRLAB/Graph-R1/blob/main/agent/tool/tools/search_tool.py : training settings and the search tool (read 20261030 19:02 UTC)
11. https://arxiv.org/abs/2507.21892 : authors, submission history v1 and v2, comments field, journal reference (read 20261030 18:59 UTC)
12. https://arxiv.org/html/2507.21892 : paper v2 full text, two fetches summarised by a small model, so figures are as returned and the PDF was not opened; Table 2, Table 3, Table 6a, ablation, Appendix D, G, J, K (read 20261030 19:00 UTC)
13. https://www.alphaxiv.org/abs/2507.21892 : generated report on the paper, used for the method summary, the scale results and the generation-quality figures (read 20261030 18:59 UTC)
14. https://proceedings.mlr.press/v306/luo26c.html : ICML 2026 proceedings entry, PMLR 306:82220-82240, conference dates in the BibTeX (read 20261030 19:00 UTC)
15. https://arxiv.org/abs/2601.17755 : HyperGraphPro, authors, submission history, abstract (read 20261030 19:00 UTC)
16. Web search "Graph-R1 agentic GraphRAG reinforcement learning LHRLAB follow-up successor 2026": result list only; it named the ICML poster page https://icml.cc/virtual/2026/poster/63269 (not opened) and the follow-up under the name "ProGraph-R1" (searched 20261030 19:00 UTC)
17. https://github.com/LHRLAB?tab=repositories : the owner's repositories by last push, through the GitHub API; HyperGraphRAG pushed 20260512, no repository named as a successor (read 20261030 19:01 UTC)
18. The July 2026 investigation of this project (20260725 15:30 UTC), the document this entry replaces; no public URL. Used for the (J) statements, which are not re-verified.
