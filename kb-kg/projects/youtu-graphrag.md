---
slug: youtu-graphrag
repo: TencentCloudADP/youtu-graphrag
tier: deep
category: core
snapshot: 20261030 18:58 UTC
---

# Youtu-GraphRAG

| | |
|---|---|
| Repository | https://github.com/TencentCloudADP/youtu-graphrag |
| Licence | Custom "Youtu-GraphRAG License" (not an SPDX id; GitHub reports "Other"). Use is limited to academic purposes; commercial and production use is forbidden. **The README badge says MIT; the `LICENSE` file says otherwise, and the file is the authority.** [1][4][5] |
| Language | Python [1] |
| Stars, forks | 1,271 stars, 190 forks (20261030 18:58 UTC) [1] |
| Created, last push | 20250901 02:52 UTC, 20260226 12:57 UTC [1] |
| Latest release | v0.2.1, 20260226 12:40 UTC (four tags in all: v0.1.0, v0.1.1, v0.2.0, v0.2.1) [2] |
| Status | **quiet**: the last push was 246 days before the snapshot, outside the 90-day window. Not archived. 60 open items (51 issues, 9 pull requests) [1][3][18] |
| Paper, docs | arXiv 2508.19855, current version v3 of 20250903 [6][7]. The README and the repository description state acceptance at ICLR 2026 [1][5]. Dataset: AnonyRAG on Hugging Face [19]. A `FULLGUIDE.md` is linked from the README and was not read [5] |

## What it is

Youtu-GraphRAG is a GraphRAG framework from Tencent Youtu Lab in which one declared graph schema drives both
graph construction and retrieval. At index time the schema bounds an LLM extraction step; at query time the
same schema guides how a question is split into sub-questions [5][7]. The index is a four-level "knowledge tree"
(attributes, relation triples, keywords, communities) [7]. Retrieval is embedding based, and an iterative
retrieve-and-reflect loop sits on top [7][14]. It ships as a FastAPI web application plus a command-line entry
point, installable with Docker or a Python 3.10 environment [5][14][15]. The same paper introduces AnonyRAG, a
benchmark with anonymised entities [7][19].

## How it works

### The seed schema

- **Format.** One JSON file per dataset with three flat lists: entity types, relations, attribute types. The demo
  schema has 10 entity types (person, location, organization, event, object, concept, time_period,
  creative_work, biological_entity, natural_phenomenon), 12 relations (is_a, part_of, located_in, created_by,
  used_by, participates_in, related_to, belongs_to, influences, precedes, arrives_in, comparable_to) and 11
  attribute types (name, date, size, type, description, status, quantity, value, position, duration, time) [9].
  The paper writes it as S = (S_e, S_r, S_attr) (Eq. 1) [7].
- **How it enters extraction.** The construction code serialises the schema to JSON and places it, with the text
  chunk, into the extraction prompt [10]. The paper describes this as constrained generation that reduces the
  search space to S_e x S_r x S_attr (Eq. 2) and says open-ended extraction (OpenIE or a free LLM) "would
  inevitably introduce noise and irrelevant trivia" [7].
- **What the shipped prompt actually says.** In the `general` and `general_agent` construction prompts the model
  is told to *prioritise* the schema and, where the text does not fit, to "extract the valuable knowledge as
  needed" [8]. So in the code the schema is a strong hint, not a hard filter. The paper's wording is stronger than
  the prompt. Other prompt variants (`novel`, `novel_eng`) were not read [8].
- **Schema expansion.** In agent mode (the configured default) [8] the extraction response may carry a
  `new_schema_types` field naming new entity types, relations and attributes. The builder adds every suggestion
  that is not already in the schema and writes the merged schema back to the dataset's JSON file [10]. Two
  qualifications from the code: (1) the write-back only happens for five dataset names (hotpot, 2wiki, musique,
  novel, graphrag-bench); for any other name the function returns without changing anything [10]; (2) no code
  path checks a confidence value. The paper describes a confidence threshold mu (Eq. 3) and "selectively
  incorporates only high-confidence patterns" [7]. The only threshold in the repository is a sentence inside the
  agent-mode prompt telling the model that the bar for adding a type is 0.9; the model, not the code, applies it [8].
  An external user reports that this prompt-only gate does not hold on a large corpus (see Evidence) [16].

### The four-level knowledge tree

Paper Eq. 8 defines the tree; the builder produces it as follows [7][10][11].

| Level | Content | Built by | LLM involved? |
|---|---|---|---|
| L1 | Attribute nodes: an entity and one typed attribute value | The extraction call | Yes (same single call as L2) |
| L2 | Entity-relation triples (head, relation, tail) | The extraction call | Yes (same call) |
| L3 | Keywords: up to 5 entities per community, ranked by a mix of normalised degree and cosine similarity to the community's mean embedding | Tree-community module | No |
| L4 | Community nodes with an LLM-written name and summary, linked to their members by a `member_of` relation | Tree-community module | Yes, batched: 5 communities per prompt, communities of 2 or more members only |

### Dually perceived community detection

- The similarity of two nodes is a weighted mix: `struct_weight` x Jaccard overlap of adjacency (structure) plus
  (1 - `struct_weight`) x cosine similarity of embeddings built from the nodes' triples (semantics). The shipped
  value of `struct_weight` is 0.3 [8][11]. The paper calls this "dual perception" (Eqs. 4-7) [7].
- Clusters start from a fast embedding-based clustering, then are merged pairwise when their similarity is at
  least 0.5 and the merged size stays at or below 100 members. The configured cap on the total number of
  communities is 100 [8][11]. (Two different "100" limits: members per merged cluster, and communities in total.)
- No LLM is used for the clustering itself. The LLM only names and summarises the finished communities [11].
- The tree supports top-down filtering (start at community summaries) and bottom-up reasoning (entity and triple
  granularity) [7]. The README claims it "performs better than traditional Leiden and Louvain algorithms" [5]. The
  ablation in Table 3 removes community detection altogether; it does not compare against Leiden or Louvain [7].

### The agentic retriever

- **Decomposition.** One LLM call receives the question and the schema JSON and returns 2 to 3 sub-questions plus
  `involved_types` (the node, relation and attribute types the question touches). Simple questions come back as
  a single sub-question [8][12]. The listed types are then passed to retrieval to filter candidates [14].
- **Retrieval per sub-question.** Embedding search (FAISS) and graph expansion; the retriever module makes no LLM
  call except an answer-generation helper [13]. The paper lists four parallel routes (Eq. 10): entity matching,
  triple matching, community filtering, and depth-first path traversal with maximum depth d = 5 [7]. The shipped
  default (`recall_paths: 2`) runs two parallel paths, one over nodes and relations (which includes a path search
  with maximum depth 2) and one over triples only [8][13]. The retriever file never mentions "community" by name,
  which is consistent with level-4 nodes being retrieved as ordinary graph nodes; this was not traced [13].
  Sub-questions run in parallel [14].
- **Iterative reflection (IRCoT style).** An initial answer is generated from the merged sub-question context
  (retrying up to 20 times on an empty or failed response). Then, up to `retrieval.agent.max_steps` times (5 in
  the shipped config), one LLM call sees triples, chunks and earlier thoughts and must end either with a final
  answer or with a new query. A new query triggers another embedding retrieval; the loop also stops when no new
  query appears or the query repeats [8][14]. The fallback value of `max_steps` in `app.py` was not read.
- **LLM calls per question.** 1 (decompose) + 1 (initial answer) + at most 5 reflection calls: **2 to 7**, more
  only through retries. Retrieval itself calls no LLM once the index exists [13][14].

### How an agent or a person talks to it

A FastAPI web application on port 8000 with a visual interface, and a command-line program with argument parsing
[5][14][15]. The README mentions no MCP server, SDK or tool-calling interface: **unstated** for those [5].
The four-level tree can be exported for visualisation in Neo4j [5]. The LLM is any OpenAI-format endpoint set in a
`.env` file (the README example uses DeepSeek) [5].

## Cost and operating profile

**Construction.**

- **One extraction call per chunk.** A single call returns attributes, triples, entity types and optional schema
  expansions together [10]. Community naming adds batched calls (5 communities each) [11].
- **Chunk size.** `chunk_size` is 5,000 tokens with 200 overlap [8][10]. It applies only to corpora outside the
  `datasets_no_chunk` list. The listed names (hotpot, 2wiki, musique, graphrag-bench, annoy_chs, annoy_eng, demo)
  are processed one corpus item per chunk [8][10]. So on the paper's benchmark corpora the number of extraction
  calls equals the number of passages, not the number of 5,000-token windows.
- **Parallelism.** 32 worker threads in the shipped config [8]; the paper also runs 32-thread concurrent inference [7].
- **Community stage.** The paper reports that community detection consumed "no more than 10,000 tokens on any
  dataset" [7].

**Per query.** 2 to 7 LLM calls (above) [13][14]. In agent mode the construction step also grows the prompt with the
schema (see Evidence, issue 168) [16].

**Published cost claims.**

| Claim | Where | Detail |
|---|---|---|
| "up to 90.71% saving of token costs" and "16.62% higher accuracy" over state-of-the-art baselines | Paper abstract, v3 [7] | The pages read do not say which baseline, dataset or unit gives 90.71% or whether 16.62% is relative or absolute: **unstated** |
| "33.6% lower token cost" and "16.62% higher accuracy" | README headline [5] | The README and the paper abstract give different savings figures; the README's 33.6% has no source in the paper pages read |
| "up to an order of magnitude fewer tokens during graph construction" | Paper, section 4.4 [7] | Figure 6 plots construction tokens (axis ticks 1M to 128M) against accuracy for six benchmarks; the plotted values were not readable from the text |
| Lowest construction token use on all six datasets, time efficient on five | Paper, Figure 5a [7] | Compared with five baselines, DeepSeek-V3-0324, 32 threads |

**Mechanisms the code supports.** One combined extraction call per chunk; no per-element LLM summarisation in
the construction path read; community naming batched; keywords computed without an LLM [10][11]. **Mechanism
the code does not fully support:** the schema bounds the output only softly (see above), so token savings from
"schema-bounded" output depend on the model following a prompt hint. Statements in earlier notes about how other
systems spend tokens (several passes for entity descriptions, relation summaries, community reports) are not
re-verified here; see those systems' own entries.

**What it needs.** Python 3.10 (or Docker) and a long dependency list: PyTorch 2.6.0, transformers 4.51.1,
sentence-transformers 2.3.1, faiss-cpu 1.9.0, spaCy 3.7.5 (the config names `en_core_web_lg`), the MinerU PDF
parser (`magic-pdf`) and its layout models, Apache Tika (a Java service), FastAPI, and the OpenAI client [8][15].
The release notes for v0.2.1 mention a Java install step [2]. Neo4j is not required; the README offers a Neo4j import for visualising the tree [5].

**Runs locally?** Embeddings are `all-MiniLM-L6-v2` on CPU [8], so only the LLM is remote. Any
OpenAI-compatible endpoint works [5]; an external user ran agent-mode construction against a local vLLM server
with Qwen3-14B [16]. No hosted service is required by the README [5].

## Evidence

All numbers below are the authors' own, from the paper (v3) [7]. The authors state they re-ran every baseline
under the same settings: DeepSeek-V3-0324 and Qwen3-32B as base models, `all-MiniLM-L6-v2` as embedding model, and
DeepSeek-V3-0324 as the judge of answer similarity [7]. Table 2 is captioned "based on DeepSeek", so the judge and
the generator appear to be the same model; the paper does not spell it out.

**Benchmarks.** Six: HotpotQA, 2WikiMultiHopQA (2Wiki), MuSiQue, GraphRAG-Bench (textbook corpora), and the
authors' AnonyRAG-CHS and AnonyRAG-ENG (the paper's tables print "Annoy") [7].
A dual-mode evaluation ("open": the model may use its own knowledge; "reject": it must refuse when retrieval is
insufficient) is applied to HotpotQA, 2Wiki and MuSiQue [7].

**Table 2, top-10 accuracy, DeepSeek** [7]:

| Method | Hotpot open | Hotpot reject | 2Wiki open | 2Wiki reject | MuSiQue open | MuSiQue reject | G-Bench | Anony-CHS | Anony-ENG |
|---|---|---|---|---|---|---|---|---|---|
| Naive RAG | 79.40 | 68.00 | 67.60 | 33.70 | 45.58 | 26.73 | 71.22 | 12.08 | 38.93 |
| RAPTOR | 78.20 | 67.10 | 67.40 | 36.40 | 45.88 | 30.03 | 72.79 | 11.77 | 33.99 |
| G-Retriever | 49.90 | 5.90 | 38.00 | 3.80 | 23.50 | 1.70 | 70.24 | 5.38 | 5.50 |
| LightRAG | 71.98 | 58.10 | 65.70 | 38.10 | 39.40 | 22.90 | 69.74 | 8.58 | 18.90 |
| GraphRAG | 54.30 | 23.70 | 40.00 | 9.80 | 30.20 | 16.00 | 61.39 | 21.37 | 38.36 |
| HippoRAG | 78.20 | 69.40 | 77.10 | 61.10 | 45.20 | 30.90 | 70.14 | 34.01 | 40.12 |
| HippoRAG-IRCoT | 78.10 | 70.20 | 77.70 | 60.70 | 44.40 | 31.60 | 72.89 | 36.19 | 41.42 |
| HippoRAG2 | 79.40 | 70.40 | 74.60 | 45.80 | 49.10 | 34.00 | 77.21 | 13.52 | 37.24 |
| Youtu-GraphRAG without agent | 80.50 | 72.10 | 72.10 | 54.40 | 49.80 | 38.30 | 80.55 | 35.17 | 40.54 |
| **Youtu-GraphRAG** | **83.40** | **78.90** | **82.30** | **72.60** | **52.10** | **46.90** | **83.50** | **38.08** | **42.57** |

- Youtu-GraphRAG is highest in every column of Table 2.
- Margin over the strongest *other* method, computed from the table: open mode +4.0 (HotpotQA), +4.6 (2Wiki),
  +3.0 (MuSiQue), +6.3 (GraphRAG-Bench); reject mode +8.5, +11.5, +12.9; AnonyRAG +1.9 (CHS) and +1.2 (ENG). The
  paper's text says "4~8 points" in open mode and "8~12" in reject mode [7]; the MuSiQue open margin in the table
  is 3.0, below the stated range, and the MuSiQue reject margin is 12.9, above it.
- Absolute accuracy on the anonymised sets stays low: 38.08 and 42.57 at top-10 [7].
- **The agent matters on the anonymised sets.** Without the agent the model scores 35.17 (CHS) and 40.54 (ENG),
  below HippoRAG-IRCoT (36.19, 41.42) but above plain HippoRAG (34.01, 40.12) [7].
- Plain HotpotQA in open mode: 83.4 against 79.4 for HippoRAG2 and for naive RAG, a 4.0-point margin [7].

**Table 3, ablations** (full model: 81.20 / 77.60 / 47.50 / 86.54 / 42.88 / 43.26 on HotpotQA, 2Wiki, MuSiQue,
GraphRAG-Bench, AnonyRAG-CHS, AnonyRAG-ENG). The caption does not say the top-k; the paper text ties 43.26 to
"top-20 accuracy", so Table 3 is probably top-20 [7]. Differences from the full model, computed from the table:

| Variant | HotpotQA | 2Wiki | MuSiQue | G-Bench | Anony-CHS | Anony-ENG |
|---|---|---|---|---|---|---|
| without community detection | -1.70 | -2.50 | -3.50 | -1.52 | -2.91 | -3.34 |
| without agent | -5.90 | **-19.80** | -7.50 | -5.01 | -5.28 | -3.21 |
| without schema guidance | -4.10 | -4.20 | -1.90 | -3.04 | **-7.27** | -2.94 |

The paper concludes that agent reasoning is "most critical for multi-hop inference" and that schema guidance
"plays a vital role in low-resource and domain-specific scenarios" [7]. The largest schema drop (7.27) is on
AnonyRAG-CHS. Note: "without schema guidance" is the paper's variant; whether it removes the schema from the prompt
only or from retrieval too is unstated in the pages read.

**AnonyRAG** (Hugging Face `Youtu-Graph/AnonyRAG`) [19][7]. Specific entity types (people, places) are replaced
with anonymous tokens so that pretrained knowledge cannot answer for free. The dataset card, read 20261030 19:01 UTC:

| Item | Value |
|---|---|
| Questions | 1,397 in total: 688 Chinese (CHS) and 709 English (ENG), one test split |
| Source texts | Four public-domain novels: Water Margin, Dream of the Red Chamber, Moby-Dick, Middlemarch |
| Tasks | Objective (multiple choice) and subjective; the subjective ones are the "Anonymity Reversion" task (infer the original names behind the tokens). Simple (4 hops or fewer) and complex (more than 4 hops) |
| Generation | DeepSeek-V3-0324 (per the card) |
| Dataset licence | cc-by-nc-4.0 (non-commercial) |
| Downloads | about 1,027 in the month before the read |

**Caveats on the evidence.**

- Authors' own benchmark, authors' own baseline reproductions, apparently a same-model judge. No independent evaluation was
  found in this run. The search was one web search plus the repository's issues; it is not exhaustive [22][18].
- Absolute accuracy on anonymised and MuSiQue-style compositional data stays at about 40 to 52 percent [7].
- Qwen3-32B results are named as a base model but were not in the pages read: **unstated** here [7].

**Independent report on schema expansion.** Issue 168 (opened 20261004, no maintainer reply at the read, 0
comments) describes agent-mode construction with Qwen3-14B on MuSiQue (11,656 passages). Starting from the shipped
seed schema of 10 node types, 12 relation types and 11 attribute types, after 681 passages the schema had grown
to 523 node types, 1,539 relation types and 1,198 attribute types, about 19,595 tokens of JSON. An extraction
prompt reached 20,029 tokens and the user stopped the run at their own 20,000-token limit. The reporter asks
whether the 0.9 threshold is enforced only through prompting and says attribute suggestions arrive as strings that
contain values rather than as type names [16]. This is one user's report, unreproduced here; it matches the code
reading above (no code-level acceptance check).

## Direction

- **Release cadence.** Four releases from v0.1.0 to v0.2.1; v0.2.1 (20260226) adds a Chinese frontend option,
  dynamic retrieval display, upload encoding detection, parsers for several document formats and Java install
  support [2].
- **Commits.** About 207 commits on the default branch, 11 contributors; the last commits (20260225 and 20260226)
  replace bare exception handlers, fix retrieval slowdown from overly large chunks and update the README news [3].
  **No commits after 20260226** [1][3].
- **Open work.** Nine open pull requests, three from July to September 2026 (configurable LLM settings, restricting
  schema type filtering to matching nodes, returning node IDs from one-hop triples), none merged at the read [18].
  Issue 169 (20261020) asks the maintainers to enable private vulnerability reporting and says the reporter found
  an unauthenticated problem in the backend HTTP API; no details are public and the repository has no security
  policy per the reporter [17].
- **Enterprise edition.** The README says an Enterprise Edition GraphRAG launched on Tencent Cloud's ADP platform
  in February 2026 [5]. Tencent Cloud's documentation page (last updated 20260410) presents GraphRAG as a Knowledge
  Base feature enabled by a toggle, notes that graph construction "consumes a significant amount of tokens", and
  does not mention the open-source project: whether the product shares this codebase is **unstated** [20].
- **Roadmap.** No roadmap file or stated plan found in the README; **unstated** [5].
- **Sibling projects** in the same organisation include a general agent framework (4,630 stars) and Youtu-RAG
  (created 20260129, pushed 20261008) [21]. Neither is described in the sources as a successor to this repository.

## Changed since the July 2026 investigation

The July note was written 20260726 08:52 UTC. Checked 20261030 18:58 to 19:03 UTC.

- **Stars and forks.** 1,223 stars and 183 forks (July) to 1,271 and 190: +48 stars in 96 days, about 0.5 per day,
  against about 3.0 per day averaged since creation (1,271 over 424 days) [1]. No sign of inorganic growth was
  looked for beyond these rates; **unstated**.
- **Activity.** No commits since 20260226, and none since 20260801 [3]. **Correction:** the July note called the
  project "active". Its last push was already 150 days old on 20260726, so it was outside the 90-day window then
  and is **quiet** now (246 days).
- **Open items.** 57 in July; 60 now (51 issues and 9 pull requests) [18].
- **Licence.** Unchanged. The `LICENSE` file has one commit in its history, the initial commit of 20250902, and its
  text is as follows. The operative sentence: "You agree to use the Youtu-GraphRAG only for academic purposes, and
  refrain from using it for any commercial or production purposes under any circumstances." The preceding
  paragraph grants broad permissions (use, copy, modify, merge, publish, distribute, sublicense) "without
  restriction", and this sentence is a condition attached to them. The README badge still says MIT [4][5]. GitHub
  reports the licence as "Other" with no SPDX identifier [1]. The AnonyRAG dataset is separately cc-by-nc-4.0 [19].
- **Paper.** Still arXiv v3 (3 September 2025) on the abstract page at the read. No newer version, journal
  reference or ICLR comment appears there; the ICLR 2026 claim rests on the README news (January 2026) and the
  repository description [1][5][6]. The OpenReview record was not checked.
- **README.** Same two news items as in the July note (Enterprise Edition, ICLR acceptance) and the same claims
  [5][3]. Contact addresses in the README are not reproduced here.
- **Corrections to July claims from re-reading the code and paper.** (1) The extraction prompt asks the model to
  prioritise the schema and allows extraction outside it; the "may only emit triples whose types appear in S" wording
  is the paper's, not the prompt's [8][7]. (2) The schema write-back runs only for five named datasets [10].
  (3) "The code applies no threshold": true of code, but the agent prompt states a 0.9 threshold the model is
  asked to apply [8][10]. (4) Chunks of 5,000 tokens apply only to datasets outside the no-chunk list, so benchmark
  corpora are processed per passage [8][10]. (5) The community cap "100" is two limits: 100 members per merged
  cluster and a configured total of 100 communities; community naming batches 5 communities per call [8][11].
  (6) The default retrieval runs two parallel paths with a depth-2 path search, against the paper's four routes and
  d = 5 [7][8][13]. (7) The ablation "without agent" is below HippoRAG-IRCoT, not below every HippoRAG variant
  [7]. (8) Installation is Docker or a Python 3.10 pip environment; "conda" was not found in the README [5].
- **New evidence since July.** Issue 168 (20261004), the unbounded schema growth report above [16]; issue 169
  (20261020), the vulnerability-reporting request [17].
- **Successor, rename.** None found: the repository is still `TencentCloudADP/youtu-graphrag`, the stated homepage
  is the arXiv paper, and one web search found no successor or second version [1][22].

## Sources

All times are UTC, taken from the system clock to the minute. Reads within one batch can differ by up to two minutes.

1. https://api.github.com/repos/TencentCloudADP/youtu-graphrag : stars, forks, licence field, archived flag, created and pushed dates, topics, homepage (read 20261030 18:58 UTC)
2. https://api.github.com/repos/TencentCloudADP/youtu-graphrag/releases/latest and `/tags` : release v0.2.1 notes and tag list (read 20261030 18:58 UTC)
3. https://api.github.com/repos/TencentCloudADP/youtu-graphrag/commits : commits since 20260801 (none), latest commits; contributors and commit count (read 20261030 18:58 UTC; counts 19:02 UTC)
4. https://github.com/TencentCloudADP/youtu-graphrag/blob/main/LICENSE : licence text; history of the file via the commits API for that path (read 20261030 18:58 UTC)
5. https://github.com/TencentCloudADP/youtu-graphrag/blob/main/README.md : README, badge, news, claims, quick start (read 20261030 18:58 UTC)
6. https://arxiv.org/abs/2508.19855 : submission history v1 to v3, comments field (read 20261030 19:00 UTC)
7. https://arxiv.org/pdf/2508.19855v3 : paper text, Eqs. 1-10, Tables 2 and 3, sections 4.1 to 4.6 (read 20261030 19:00 UTC)
8. https://github.com/TencentCloudADP/youtu-graphrag/blob/main/config/base_config.yaml : chunk size, workers, struct_weight, max_steps, prompts, retrieval settings (read 20261030 18:59 UTC)
9. https://github.com/TencentCloudADP/youtu-graphrag/blob/main/schemas/demo.json : demo seed schema (read 20261030 18:59 UTC)
10. https://github.com/TencentCloudADP/youtu-graphrag/blob/main/models/constructor/kt_gen.py : chunking, extraction call, schema update, community stage (read 20261030 18:59 UTC)
11. https://github.com/TencentCloudADP/youtu-graphrag/blob/main/utils/tree_comm.py : similarity mix, merge rules, community naming batches, keywords (read 20261030 18:59 UTC)
12. https://github.com/TencentCloudADP/youtu-graphrag/blob/main/models/retriever/agentic_decomposer.py : decomposition call (read 20261030 18:59 UTC)
13. https://github.com/TencentCloudADP/youtu-graphrag/blob/main/models/retriever/enhanced_kt_retriever.py : retrieval paths, LLM use in the retriever (read 20261030 18:59 UTC)
14. https://github.com/TencentCloudADP/youtu-graphrag/blob/main/main.py : initial answer, IRCoT loop, command-line options (read 20261030 18:59 UTC)
15. https://github.com/TencentCloudADP/youtu-graphrag/blob/main/requirements.txt : dependencies (read 20261030 18:59 UTC)
16. https://github.com/TencentCloudADP/youtu-graphrag/issues/168 : external report of schema growth (read 20261030 19:01 UTC)
17. https://github.com/TencentCloudADP/youtu-graphrag/issues/169 : vulnerability-reporting request (read 20261030 19:01 UTC)
18. https://github.com/TencentCloudADP/youtu-graphrag/pulls and issue search for this repository : open issue and pull-request counts, open pull requests (read 20261030 19:02 UTC)
19. https://huggingface.co/datasets/Youtu-Graph/AnonyRAG : AnonyRAG dataset card (read 20261030 19:01 UTC)
20. https://www.tencentcloud.com/document/product/1254/78733 : Tencent Cloud documentation page on GraphRAG in the knowledge base (read 20261030 19:01 UTC)
21. https://github.com/TencentCloudADP : organisation repository list and the Youtu-RAG repository metadata (read 20261030 19:01 UTC)
22. Web search "Youtu-GraphRAG Tencent ICLR 2026 successor ... Enterprise Edition": no successor or second version found (run 20261030 19:01 UTC)
