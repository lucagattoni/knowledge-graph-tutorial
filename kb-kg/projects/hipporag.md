---
slug: hipporag
repo: OSU-NLP-Group/HippoRAG
tier: deep
category: core
snapshot: 20261030 18:58 UTC
---

# HippoRAG (HippoRAG 2)

| | |
|---|---|
| Repository | https://github.com/OSU-NLP-Group/HippoRAG |
| Licence | MIT, from the `LICENSE` file ("Copyright (c) 2025 OSU Natural Language Processing"); no conflict with the API metadata or the package manifests [1][2][12][13] |
| Language | Python 3.10 or newer [1][12] |
| Stars, forks | 4,083 stars, 437 forks (read 20261030 18:58 UTC) [1] |
| Created, last push | 20240523 23:07 UTC, 20261006 21:03 UTC [1] |
| Latest release | `v1.0.0`, titled "HippoRAG 1", published 20250227 17:29 UTC; the only release and the only tag. The package version in `pyproject.toml` is `2.0.0a5` (alpha), with no GitHub release [3][12] |
| Status | active: last push 24 days before the snapshot; not archived [1] |
| Paper, docs | HippoRAG (NeurIPS 2024) https://arxiv.org/abs/2405.14831 [16]; HippoRAG 2, "From RAG to Memory" (ICML 2025) https://arxiv.org/abs/2502.14802 [14]; the README is the documentation [6] |

## What it is

A graph-augmented retrieval framework presented as a model of hippocampal long-term memory. An LLM
(the "neocortex" in the paper's analogy) builds a schema-less open knowledge graph at index time. At
query time, Personalized PageRank (PPR) over that graph performs multi-hop retrieval in one step [15][17].

HippoRAG 2's stated design choice differs from GraphRAG-style systems. It uses the graph only to
re-rank existing passages, rather than expanding the corpus with LLM-generated summaries. The paper
reports that this lets it beat a strong dense retriever (NV-Embed-v2, 7B) on multi-hop tasks while not
losing on simple factual QA. The abstract claims "a 7% improvement in associative memory tasks over the
state-of-the-art embedding model" [15].

Since the July 2026 investigation the repository has also become an MCP server and a Claude Code
plugin (see the last section) [6].

## How it works

### What gets indexed

Per passage (code in `src/hipporag/HippoRAG.py`, defaults in `src/hipporag/utils/config_utils.py::BaseConfig`) [7][9]:

1. **OpenIE triples via an LLM.** The July reading found a two-step flow, named-entity recognition first
   and then triples seeded with those entities, using 1-shot prompting; schema-less. The current config
   still has separate token limits for the two calls (`openie_ner_max_tokens`, `openie_triple_max_tokens`)
   [6][9]. The prompt templates were not modified in the diff between the July baseline and 20261030 [5];
   the 1-shot detail was not re-read in this run. This is the expensive, LLM-required part.
2. **Phrase nodes** (ids prefixed `entity-`, a hash of the text) are the triples' subjects and objects.
   **Relation edges** connect them; July found the weight to be the co-occurrence count [7].
3. **Passage nodes** (`chunk-` ids) with **context edges** ("contains", weight 1.0) to every phrase
   extracted from the passage. New in HippoRAG 2 [7][15].
4. **Synonym edges.** A k-nearest-neighbour search over phrase-node embeddings adds an edge when cosine
   similarity is at least `synonymy_edge_sim_threshold = 0.8`; the edge weight is the similarity. The
   config sets `synonymy_edge_topk = 2047`, but the loop in `add_synonymy_edges` stops after about 100
   accepted neighbours per phrase node (`num_nns >= 100` now; `> 100` at the July baseline), so 2047 is
   an upper bound on candidates, not the degree [8][9]. No LLM is involved.
5. **Embeddings** are stored for phrases, for facts (triples) and for passages. The default encoder is
   `nvidia/NV-Embed-v2`, with normalised output; the default LLM name in `BaseConfig` is `gpt-4o-mini`
   [9]. The graph is **undirected** (`is_directed_graph = False`) and held in python-igraph [7][9].
6. **Edge merging (current code).** When the same node pair carries several contributions, one edge is
   stored with `weight = max(sum of fact counts, 1.0 if a passage edge, synonym score)` and an
   `edge_kind` label such as `fact+synonym` [7]. How the July baseline merged them was not compared.

Scale in the paper (Table 10, MuSiQue, 11,656 passages) [15]:

| | Llama-3.3-70B-Instruct | GPT-4o-mini |
|---|---|---|
| Phrase nodes | 85,288 | 101,641 |
| Passage nodes | 11,656 | 11,656 |
| Relation edges | 140,830 | 125,903 |
| Context edges | 132,586 | 146,293 |
| Synonym edges | 1,125,951 | 1,304,605 |
| Total edges | 1,399,367 | 1,576,801 |

Synonym edges are about 8 times the relation edges in the first column (computed from the table).

What needs an LLM and what does not: triples and relation edges need an LLM. Synonym edges need only a
local embedder. The passage-to-phrase edges follow mechanically once the node sets exist.

The v1 ablation (Table 5 of the HippoRAG paper, average recall@5) shows how much the LLM matters for
triple extraction [17]:

| OpenIE extractor | Avg R@5 |
|---|---|
| Full HippoRAG (extractor LLM not identified in the text read) | 72.9 |
| Llama-3.1-70B-Instruct | 72.5 |
| Llama-3.1-8B-Instruct | 67.8 |
| REBEL (small end-to-end OpenIE model) | 58.4 |

The July notes called the 8B result "nearly on par"; the 5.1-point gap does not support that wording,
and only the 70B model is close to the full configuration.

### The PPR mechanism

Query flow: `HippoRAG.retrieve()` calls `graph_search_with_fact_entities()`, which calls `run_ppr()`.
All of it is in `src/hipporag/HippoRAG.py` [7]; the parameters below are identical at the July
baseline commit and at the snapshot [8][9].

1. **Query to triple.** The query is embedded and compared with all fact embeddings (`get_fact_scores()`).
   This replaces HippoRAG 1's query-NER step. With normalised embeddings the scores are cosines.
2. **Recognition-memory filter.** The top candidate facts pass through an LLM filter (`rerank_facts()`,
   `DSPyFilter` in `src/hipporag/rerank.py`), keeping at most `linking_top_k = 5` triples [7][9][10].
3. **Phrase seed weights.** Each phrase node in a surviving triple receives the average of the fact scores
   of the filtered triples it appears in. Each fact score is first divided by the number of passages the
   phrase is linked to (`len(ent_node_to_chunk_ids[phrase])`), a node-specificity damper in the style of
   inverse document frequency, so ubiquitous entities do not dominate. HippoRAG 1 called this node
   specificity, `s_i = |P_i|^-1`, and its ablation lowered average R@5 from 72.9 to 70.9 [17]. At most
   five phrase seeds are kept (`get_top_k_weights`) [7].
4. **Passage seed weights.** Every passage node is a seed. `dense_passage_retrieval()` scores all
   passages against the query. The scores are then **min-max normalised per query** (all ones if every
   score is equal; `min_max_normalize` in `utils/misc_utils.py`) and multiplied by
   `passage_node_weight = 0.05` [7][11]. The July notes described this step without the normalisation;
   the normalisation was already in the July baseline code [8]. Seeding every passage, not only the top
   k, is deliberate in the code; the July notes recorded the authors' rationale as letting probability
   flow along multi-hop chains (July reading of the paper, not re-verified).
5. **Reset vector.** `node_weights = phrase_weights + passage_weights`, unnormalised; igraph normalises
   it internally [7].
6. **PPR call** (`run_ppr()`) [7]:
   ```python
   self.graph.personalized_pagerank(
       vertices=range(n),
       damping=0.5,
       directed=False,
       weights="weight",
       reset=reset_prob,
       implementation="prpack",
   )
   ```
   The `damping` default is 0.5 (`BaseConfig.damping`). HippoRAG 1 reports tuning it on 100 MuSiQue
   training examples, and describes the value as the probability that the walk restarts from the query
   nodes; Table 13 of the HippoRAG 2 paper lists 0.5 as well [15][17]. A damping of 0.5 gives a short,
   local diffusion, unlike the 0.85 usual for global PageRank (arithmetic on the stated value, not a
   claim from the paper). The current config validation requires `0 < damping < 1` [9].
7. **Passage ranking.** The final score is the raw PPR probability at each passage node, sorted
   descending. There is no later fusion with dense scores. Dense retrieval enters only through the reset
   vector. HippoRAG 1 had combined graph and dense scores outside the walk; HippoRAG 2 replaced that with
   passage-node seeding [7].
8. **Fallback.** If the filter returns zero triples, `retrieve()` returns the dense-retrieval ranking and
   skips graph search [7]. In the paper's error analysis (Appendix E, 100 samples with recall@5 below
   1.0), 18% of the samples were left with zero triples after filtering and used the dense results [15].
   The July notes attributed the analysis to MuSiQue; the dataset was not re-checked.

HippoRAG 1 mechanics, for contrast: seeds were the graph nodes nearest (cosine) to the NER entities of
the query, with uniform reset probability times node specificity; there were no passage nodes; a
passage's score was the sum of PPR probabilities of the phrases occurring in it (July reading of the
v1 paper, section 2.3; only node specificity was re-checked, in [17]).

### HippoRAG 1 to 2: what changed

| Change | Mechanism | Evidence (Table 4 of the HippoRAG 2 paper, average R@5 over MuSiQue, 2Wiki, HotpotQA) [15] |
|---|---|---|
| Passage nodes in the graph ("dense-sparse integration") | passages become nodes with "contains" edges; dense scores seed them | 87.1 with them, 81.0 without. The paper's Table 3 puts HippoRAG (reproduced) at 44.4 NQ R@5 against 78.0 for HippoRAG 2 |
| Query-to-triple linking | embed the whole query and compare it with fact embeddings, instead of NER then node lookup | query-to-triple 87.1; NER-to-node 74.6; query-to-node 59.6 |
| Recognition-memory filter | an LLM filters candidate triples before seeding | 87.1 with the filter, 86.4 without (73.0 / 90.7 / 95.4 per dataset); small on average |

The passage-node sweep (Table 5, R@5) is flat to mildly declining: MuSiQue 79.9 / 80.5 / 79.8 / 78.4 /
77.9 and NQ 75.6 / 76.9 / 76.9 / 76.7 / 76.4 at weights 0.01 / 0.05 / 0.1 / 0.3 / 0.5. The default 0.05 is
the best MuSiQue value and tied for best on NQ [15].

### Agent interface

New since the July investigation: an MCP server (`hipporag-mcp`, extra
`hipporag[mcp]`) with five tools, `retrieve`, `rag_qa`, `index`, `delete` and `index_stats`, plus a
`hipporag://config` resource, over stdio or Streamable HTTP (no authentication on HTTP); and a Claude
Code plugin that bundles it with a skill and an `/hipporag:index-folder` command [6][13]. Details are in
the last section.

## Cost and operating profile

**Indexing and query cost, from the paper** (Appendix F, Table 12; MuSiQue, 11,656 passages;
Llama-3.3-70B-Instruct served by vLLM on four NVIDIA H100 GPUs) [15]:

| Method | Input tokens | Output tokens | Indexing time (min) |
|---|---|---|---|
| HippoRAG 2 | 9.2M | 3.0M | 99.5 |
| RAPTOR | 1.7M | 0.2M | 100.5 |
| LightRAG | 68.5M | 18.3M | 235.0 |
| GraphRAG | 115.5M | 36.1M | 277.0 |

- Per passage this is about 790 input and 260 output tokens (computed: 9.2M and 3.0M over 11,656).
- GraphRAG needs 12.5 times HippoRAG 2's input tokens (the table gives 1255.4%).
- The README says HippoRAG 2 uses "significantly fewer resources for offline indexing compared to other
  graph-based solutions such as GraphRAG, RAPTOR, and LightRAG" [6]. In Table 12 RAPTOR uses fewer
  tokens (18.5% of HippoRAG 2's input) and about the same indexing time, so the README claim does not
  hold for RAPTOR on the token measure [15].
- Query time: 1.2 s per query against 0.3 s for the dense baseline. "QA GPU memory" is 9.9 GB for
  HippoRAG 2 (RAPTOR 1.4, LightRAG 4.5, GraphRAG 3.7) [15]. The July notes said the memory is mostly
  fact embeddings; the text read here does not say, so treat that as unverified. How much of the 1.2 s
  is the PPR call alone is **unstated** in the sources read; the code logs it separately (`ppr_time`)
  [7].
- Query-time LLM use is one small filter call per query [7].

**What it needs.** The README documents three routes [6]:

| Route | Needs |
|---|---|
| OpenAI | `OPENAI_API_KEY`; the quick start uses `gpt-4o-mini` and `text-embedding-3-small`, with no GPU |
| Any OpenAI-compatible endpoint (local vLLM, hosted gateways), Azure OpenAI, Amazon Bedrock | endpoint and key settings; token usage must be reported by the endpoint or HippoRAG refuses to cache the response |
| Local | vLLM with `Llama-3.3-70B-Instruct` (the README example uses `--tensor-parallel-size 2`) plus a local embedder such as `nvidia/NV-Embed-v2` (7B); `openie_mode='offline'` batches OpenIE, which the README says can be more than 3 times faster than the online vLLM server |

Embeddings are stored in local Parquet files by default, or in Qdrant, ChromaDB or Milvus (Milvus Lite
needs no server) [6][9]. The default dependencies pin `torch==2.5.1` and `python_igraph==0.11.8` [12].

**Where it does not win.** Table 3 (passage recall@5) [15]:

| Method | NQ | PopQA |
|---|---|---|
| HippoRAG (reproduced, i.e. v1 re-run by the HippoRAG 2 authors) | 44.4 | 53.8 |
| HippoRAG 2 | 78.0 | 51.7 |
| NV-Embed-v2 (7B) | 75.4 | 51.0 |
| GritLM-7B | 76.6 | 50.1 |

On PopQA, an entity-centric simple-QA set, HippoRAG 1 has the highest value among the rows read, and
HippoRAG 2 is 0.7 above NV-Embed-v2. On NQ it is 2.6 above NV-Embed-v2. The graph pays off on multi-hop
and associative queries: R@5 gains over NV-Embed-v2 of 5.0% on MuSiQue and 13.9% on 2Wiki, as the
paper's text writes them (whether these are absolute points or relative is not stated in what was read)
[15]. The paper reports GraphRAG and LightRAG below plain dense retrieval on simple QA (July reading of
the paper, not re-verified). HippoRAG 2's passage nodes are the design element aimed at that regression.

## Evidence

All of it is the authors' own, from the two papers; no third-party evaluation was searched for in this
run.

| Result | Source |
|---|---|
| Average QA F1 (Table 2): HippoRAG 2 59.8, NV-Embed-v2 57.0; text reports +9.5% F1 on 2Wiki and +3.1% on LV-Eval | [15] |
| Passage recall@5 (Table 3): +5.0% on MuSiQue, +13.9% on 2Wiki over NV-Embed-v2 | [15] |
| Ablations (Table 4) and the reset-weight sweep (Table 5) as above | [15] |
| Error analysis (Appendix E, 100 samples with recall@5 below 1.0): in 26% no supporting-passage phrase matches after filtering, against 7% before filtering; 8% show a drop in the share of supporting-passage phrases after filtering; 18% end with zero triples. The paper calls triple filtering and graph search "the two main sources of errors" | [15] |
| HippoRAG 1 extractor ablation (Table 5 of the v1 paper): 72.9 / 72.5 / 67.8 / 58.4 as tabulated above; node specificity removed 70.9 | [17] |
| Hyperparameters (Table 13): PPR damping 0.5, synonym threshold 0.8, temperature 0.0; triple filter keeps the top 5 triples | [15] |

The two papers' numbers were read from arXiv's HTML versions through a summarising fetch, and every
figure that the July notes also carried agreed with it. The README points to datasets on Hugging Face
and ships OpenIE results for a MuSiQue sample under `outputs/musique` [6].

## Direction

The README's own TODO list has three items, all ticked: more embedding models, embedding endpoints and
vector-database integration [6]. No roadmap beyond that is stated. The commit history since the July
baseline shows the direction in practice [4][5]:

- provider plumbing: a generic OpenAI-compatible path with per-component API keys, named gateway
  prefixes (frozen), Amazon Bedrock and its Mantle endpoint, Azure deployment settings;
- index integrity: an `index_manifest.json` that binds persisted vectors and OpenIE state to the
  endpoint, model, normalisation and component identity, so that incompatible indexes are rejected
  rather than mixed (package version 2.0.0a5) [6];
- vector-store backends (Milvus, Qdrant, ChromaDB) and a large regression test suite;
- agent access: an MCP server and a Claude Code plugin marketplace.

The retrieval algorithm itself, as listed above, did not change in this period. The core paper work
stayed at HippoRAG 2.

## Changed since the July 2026 investigation

The July notes were written on 20260725 15:32 UTC from the repository as it stood after the commit of
20260724 16:59 UTC (`e37fba2af1`). Checked 20261030 18:58 to 19:02 UTC.

- **Stars and forks.** July: 3,886 stars. Now: 4,083 stars (+197 in about 97 days), 437 forks (forks were
  not recorded in July) [1].
- **Licence.** MIT in July, MIT now; the `LICENSE` file, the API field and the manifests agree [1][2][12][13].
- **Activity.** 13 commits since 20260725 (10 since 20260801), the last on 20261006 21:03 UTC. Nine are
  by one committer who is an author of both papers (three of the nine are merge commits), four by three
  outside contributors; the API lists 15 contributors in total
  [1][4]. Nothing was pushed in the 24 days before the snapshot. The compare view shows 62 files changed,
  mainly under `src/hipporag/`; `HippoRAG.py` grew by 755 added and 293 removed lines [5].
- **Not archived, not renamed, no successor found.** `full_name` is unchanged, there is no parent
  repository, and the organisation's repository list holds no second HippoRAG project [1][19]. A web
  search found no HippoRAG 3 or later paper from the group [18].
- **Papers.** HippoRAG 2 (arXiv 2502.14802) has two versions, v1 of 20250220 and v2 of 20250619, noted as
  ICML 2025. HippoRAG 1 (arXiv 2405.14831) has three, the latest of 20250114, noted as NeurIPS 2024
  [14][16]. No newer version since July.
- **Release.** Still only `v1.0.0` ("HippoRAG 1", 20250227). The package declares `2.0.0a5` [3][12].
- **The retrieval algorithm is unchanged.** Damping 0.5, `passage_node_weight` 0.05,
  `linking_top_k` 5, synonym threshold 0.8, `is_directed_graph` False, the `prpack` PPR call, division
  of the fact score by the passage count, and the dense fallback are all the same at the July baseline
  and now [7][8][9]. The July summary of the algorithm holds, with two corrections made above in the body:
  the dense scores are min-max normalised before the 0.05 factor, and synonym-edge construction stops at
  about 100 neighbours per node.
- **Corrections to July statements made in the body.** (a) "Llama-3.1-8B nearly on par with GPT-3.5": the
  8B result is 5.1 R@5 points below the full configuration; the paper text read does not name the full
  configuration's LLM, so the GPT-3.5 comparison is unverified. (b) "Query-time memory mostly fact
  embeddings": unverified. (c) RAPTOR: the July notes did not tabulate it; Table 12 shows it cheaper in
  tokens than HippoRAG 2, which contradicts the README's general claim. (d) The 18% and 26% error figures
  are shares of 100 analysed samples with recall below 1.0, not shares of all failures, and the dataset
  is unconfirmed.
- **Security fix in the filter.** At the July baseline `rerank.py` parsed the LLM's matched-fact string
  with Python `eval()`. On 20260728 a contributor changed it to `ast.literal_eval`, with the commit
  message "prevent arbitrary code execution (CWE-95)" [4][10]. A later commit (20260903) titled "fix(openie,
  dependencies): restore openai sdk version constraint and remove ast.literal_eval" touched the OpenIE
  path; its diff was not read [4]. Anyone who read or copied the July code should know the `eval()`
  version existed.
- **State checks replace asserts.** The "no phrases found" assertion in graph search is now a
  `StateConsistencyError`, and the config validates `linking_top_k >= 0`, `0 < damping < 1` and similar
  ranges [7][9].
- **New agent surface.** An MCP server (`src/hipporag/mcp_server.py`, added 20261001) with tools
  `retrieve` (returns passages with scores and source metadata; the plugin skill says it makes no LLM
  call), `rag_qa` (adds a server-side LLM answer), `index` (accepts plain strings or `{text, source_id,
  metadata}`; passages already indexed are skipped, and the server does not chunk), `delete` (by exact
  text or `source_id`) and `index_stats`. A `--read_only` flag disables `index` and `delete`; the HTTP
  transport has no authentication. On 20261006 the repository added a Claude Code plugin and marketplace
  manifest (`plugins/hipporag`, version `2.0.0-alpha.5`, MIT) whose skill tells the agent to confirm with
  the user before indexing more than about 50 passages, because each new passage costs one LLM
  extraction call [6][13]. Neither existed in July.
- **Incremental indexing and deletion.** `index()` and `delete()` exist in the current code and the
  README describes skipping already-indexed passages; the integration tests list "incremental updates and
  deletion" [6][7]. Whether July's code supported incremental updates was not compared.
- **README.** Rewritten around the new surfaces: OpenAI-compatible endpoints and gateways, Bedrock
  (including Mantle), MCP server, plugin, vector-store backends, an "Upgrading existing indexes"
  section (indexes without a manifest are rejected; re-index into a fresh directory) and updated default
  OpenIE output limits (2,048 NER and 4,096 triple tokens, up from 512 and 2,048 in earlier development
  builds) [6]. Vector-store backends (including Milvus, added 20260706) already existed at the July
  baseline [8][9]; the July notes did not mention them. The larger OpenIE limits may raise output-token
  counts for reasoning models; the effect on the paper's Table 12 figures is **unstated**.

## Sources

Times are UTC. Sources 1 to 13 are GitHub API or raw-file reads; 14 to 17 are arXiv pages; "baseline" is
commit `e37fba2af1`, the last before the July read.

1. https://api.github.com/repos/OSU-NLP-Group/HippoRAG and `/contributors`: stars, forks, licence field, archived flag, dates, open issue and PR count (8), contributor count (15) (read 20261030 18:58 UTC)
2. https://github.com/OSU-NLP-Group/HippoRAG/blob/main/LICENSE: MIT text and copyright line (read 20261030 18:58 UTC)
3. https://api.github.com/repos/OSU-NLP-Group/HippoRAG/releases and `/tags`: one release, `v1.0.0` (read 20261030 18:58 UTC)
4. https://api.github.com/repos/OSU-NLP-Group/HippoRAG/commits?since=2026-07-25T00:00:00Z: 13 commits, authors, dates, messages (read 20261030 18:59 UTC)
5. https://api.github.com/repos/OSU-NLP-Group/HippoRAG/compare/e37fba2af1...main: 62 changed files since the baseline (read 20261030 19:00 UTC)
6. https://github.com/OSU-NLP-Group/HippoRAG/blob/main/README.md: installation routes, MCP server, plugin, vector stores, upgrade notes, TODO list (read 20261030 18:59 UTC)
7. https://github.com/OSU-NLP-Group/HippoRAG/blob/main/src/hipporag/HippoRAG.py: indexing, edge construction, retrieval, seed weighting, PPR call, fallback (read 20261030 19:00 UTC)
8. The same file at commit `e37fba2af1`, https://github.com/OSU-NLP-Group/HippoRAG/blob/e37fba2af1/src/hipporag/HippoRAG.py: the July baseline, for comparison (read 20261030 19:00 UTC)
9. https://github.com/OSU-NLP-Group/HippoRAG/blob/main/src/hipporag/utils/config_utils.py, and the same file at the baseline: defaults and validation (read 20261030 19:00 UTC)
10. https://github.com/OSU-NLP-Group/HippoRAG/blob/main/src/hipporag/rerank.py, and the same file at the baseline: `eval` to `ast.literal_eval` (read 20261030 19:00 UTC)
11. https://github.com/OSU-NLP-Group/HippoRAG/blob/main/src/hipporag/utils/misc_utils.py: `min_max_normalize` (read 20261030 19:00 UTC)
12. https://github.com/OSU-NLP-Group/HippoRAG/blob/main/pyproject.toml: version 2.0.0a5, dependencies, MCP entry point (read 20261030 19:01 UTC)
13. https://github.com/OSU-NLP-Group/HippoRAG/blob/main/plugins/hipporag/.claude-plugin/plugin.json and `plugins/hipporag/skills/hipporag-memory/SKILL.md`: plugin manifest and tool-use guidance (read 20261030 19:01 UTC)
14. https://arxiv.org/abs/2502.14802: HippoRAG 2 title, authors, ICML 2025 note, version history (read 20261030 19:01 UTC)
15. https://arxiv.org/html/2502.14802v2: Tables 2 to 5, 10, 12, 13, Appendix E; first 100,000 of 100,619 characters read, through a summarising fetch (read 20261030 19:01 UTC)
16. https://arxiv.org/abs/2405.14831: HippoRAG title, authors, NeurIPS 2024 note, version history (read 20261030 19:01 UTC)
17. https://arxiv.org/html/2405.14831v3: Table 5 ablations, damping and threshold tuning, node specificity; first 100,000 of 126,509 characters read, through a summarising fetch (read 20261030 19:01 UTC)
18. Web search "HippoRAG 3 OSU NLP Group new paper 2026 successor": no successor paper found (run 20261030 19:00 UTC)
19. https://api.github.com/orgs/OSU-NLP-Group/repos: no other repository matching "hippo", "rag" or "memory" (read 20261030 19:01 UTC)
20. The July 2026 investigation notes for this project (the document this entry grew from; written 20260725 15:32 UTC; not publicly linked). Used only for statements marked "July reading" or "July notes", which were not re-verified.
