---
slug: linearrag
repo: DEEP-PolyU/LinearRAG
tier: deep
category: core
snapshot: 20261030 19:02 UTC
---

# LinearRAG

> **Reading notes.** Sources are numbered [n] and listed at the end with the time each was read.
> Numbers marked "July 2026 investigation" come from the earlier investigation of 20260725 and were
> not re-read in this run. Licence is read from the LICENSE file. No code from the repository is
> reproduced here; mechanisms are described as ideas.

| | |
|---|---|
| Repository | https://github.com/DEEP-PolyU/LinearRAG [1] |
| Licence | GPL-3.0, from `LICENSE.txt` (read 20261030 18:58 UTC) [3]; the README states no licence, so there is no badge to disagree with [2] |
| Language | Python [1] |
| Stars, forks | 566, 68 (20261030 19:02 UTC) [1] |
| Created, last push | 20251027 02:16 UTC, 20260705 00:55 UTC [1] |
| Latest release | none: the releases endpoint returns Not Found and the tags list is empty (20261030 18:58 UTC) [1] |
| Status | quiet: last push 117 days before the snapshot, not archived [1] |
| Paper, docs | arXiv:2510.10114, current version v4 of 20251109 [8]; ICLR 2026 poster [10]; docs are the README only [2] |

## What it is

LinearRAG is a research implementation of graph retrieval-augmented generation that builds its graph
with no LLM call at index time and none at retrieval time [5][9]. The paper's argument is that LLM
relation extraction is the cost and the noise source of GraphRAG, so it builds a "relation-free"
graph (the "Tri-Graph") from named-entity recognition and embeddings only [8][9]. Passages are
connected through the entities they mention, and the relation between two entities stays in the
passage text for the answering LLM to read [9]. The code is small: one main class of about 670 lines
in `src/LinearRAG.py`, plus an NER wrapper, an embedding store, a config class, an evaluator and a
driver script [1][5]. It was published as a paper on 20251011 and as code on 20251027 [1][2][8].

## How it works

### Indexing

1. **Input.** The caller supplies the passages. The driver script reads a flat list of pre-made
   chunks per dataset and prefixes each with its integer index [7]. Chunking is not part of the
   library code read [5][7].
2. **Entities.** A spaCy model runs over each passage. The default is `en_core_web_trf`; the README
   names `en_core_sci_scibert` for the medical dataset [2][4][7]. Entities labelled ORDINAL or
   CARDINAL are dropped; everything else is kept [6]. The entity node is the raw surface string,
   with no normalisation or alias merging, so "Einstein" and "Albert Einstein" are separate nodes [6].
3. **Sentences.** Sentences come from the same spaCy parse. A sentence is recorded only if it holds at
   least one retained entity [6]. (The paper describes punctuation-based sentence splitting [9]; the
   code reads sentence boundaries from the spaCy parse [6].)
4. **Graph.** The graph object (igraph, undirected) holds only entity nodes and passage nodes [5].
   Sentences are not graph nodes: the sentence-to-entity links live in separate lookup structures,
   sparse matrices in the vectorized mode [5]. A third-party count agrees: a corpus with about 7,000
   passages gave about 223,000 graph vertices, close to its 216,000 entities plus the passages [14].
5. **Edges.** Two kinds only [5]:
   - passage to entity, weighted by that entity's share of all counted entity occurrences in the
     passage, counted by plain string match;
   - passage to next passage, weight 1.0, where "next" is decided by the integer prefix on the
     passage text. The maintainers call this an optional trick, unnecessary when all chunks come from
     different documents [13].
   There are no entity-to-entity edges, no relation edges and no similarity-threshold edges at build
   time [5]. The paper's equations 1 and 2 describe binary indicator matrices for passage-entity and
   sentence-entity links [9]; the code weights the passage-entity edges, so paper and code differ here.
6. **Embeddings.** Passages, entities and sentences are all embedded, by default with
   `all-mpnet-base-v2`, and stored as parquet [4][5][9]. The "semantic linking" of the README is not an
   edge type: semantics enter only at query time, through these embeddings [2][5].
7. **Persistence and updates.** The graph is written as GraphML. NER results are cached as JSON keyed
   by passage hash, so a later run sends only new passages to NER [5]. The graph is then reassembled
   from the whole cached result, so the incremental part is the NER step [5]. In the file read, the
   state needed for retrieval is built by the indexing call; it contains no function that loads the
   saved GraphML [5].

### Retrieval

1. **Seeds.** NER runs on the question. Each question entity is matched to its nearest corpus entity
   by embedding similarity, with no minimum similarity, and the similarity becomes its seed score [5].
   If the question has no entity, the graph is bypassed and plain dense retrieval returns the top 5
   passages [5].
2. **Entity activation ("semantic bridging").** This is score propagation, not PageRank [5][9]. For
   a few rounds, each active entity above a threshold looks at its not-yet-used sentences, keeps the
   ones most similar to the question, and passes its score, multiplied by the sentence's similarity to
   the question, to every entity in those sentences. Scores below the threshold are dropped and a
   sentence is consumed once [5]. Every hop therefore passes through a sentence that resembles the
   question. At the default `max_iterations` of 3 the loop makes two propagation rounds, not three
   [5]. Scores accumulate by addition across hops in the code, while the paper's equation 5 takes an
   elementwise maximum with the previous activation [5][9].
3. **Passage scoring.** Each passage gets a dense-similarity term (min-max normalised, times a
   `passage_ratio` of 1.5 in the config class and 2 in the driver script) plus the log of one plus a
   sum over activated entities. Each entity contributes its activation times the log of one plus its
   occurrence count in the passage (found by lower-cased substring match), divided by its hop tier [4][5][7].
   The result is scaled by `passage_node_weight` (0.05) to become the reset mass on passage nodes [4][5].
4. **Personalized PageRank.** igraph runs PPR over the entity-passage graph, with the entity
   activations and scaled passage scores as the reset vector, and ranks passages by the result. The
   top 5 go to the reader. Default damping is 0.5 in code; the paper says "typically 0.85" [4][5][9].
5. **Answering.** A separate LLM call reads the 5 passages with a fixed reading-comprehension prompt.
   The README and driver default to `gpt-4o-mini` [2][5][7].
6. **Vectorized variant.** A flag switches the activation step to a torch sparse-matrix version,
   which the README recommends for GPU acceleration [2][5]. A third-party issue reported clearly worse
   retrieval from it on a 7,000-passage corpus. The maintainers attributed this to a difference in how
   top-k sentences were selected and committed an update on 20260110 [11][14]. Whether the two
   implementations now give the same results was not tested here.
7. **Optional attribute boost.** A flag, off by default, boosts passages that share a keyword with the
   question from a fixed list (for example "born", "capital", "founded"). It was added by an outside
   contributor on 20260303 for questions that name a hub entity and ask for one attribute [4][15][17].
   A pull request to revert it was closed without merging, so the option is still on the main branch [4][17].

### What the entity edges capture and miss

- **Captured.** Topical bridges between passages that have no structural relationship: two documents
  in different places, with no authored link, that both mention the same entity become two hops apart
  [5][9]. This is the connector for multi-hop questions of the 2Wiki and MuSiQue kind [9].
- **Missed.** Document hierarchy: passages are a flat list, and the only sequence information is the
  optional numbered-neighbour edge [5][13]. Entity edges inherit NER errors and surface-form
  fragmentation [6]. Questions with no named entity, and vague conceptual questions, get plain dense
  retrieval [5][15]. A third-party report finds the fallback is frequent on the medical dataset with
  the default spaCy model; a maintainer replied that the medical subset now uses the scientific
  model [16].
- **Hub entities.** A question that names a very well-connected entity and asks for one attribute
  seeds only that entity; the graph then ranks by connectivity, not by the attribute. This was the
  report that led to the optional boost [15].

## Cost and operating profile

| Item | Figure | Source |
|---|---|---|
| LLM calls at index time | none; the LLM object is used only for answering and for judging in the evaluator | [5][7] |
| Prompt and completion tokens, indexing and retrieval, 2Wiki | 0 and 0 | [9] Table 2, read 20261030 19:00 UTC |
| Indexing time, 2Wiki | 249.78 s, against 534.60 s (E2GraphRAG), 936.00 s (HippoRAG), 1147.01 s (HippoRAG2), 1202.77 s (GFM-RAG), 1323.57 s (RAPTOR), 4933.22 s (LightRAG) | [9] Table 2 |
| Indexing time, 5M and 10M tokens (ATLAS-Wiki) | 1409.95 s and 3084.38 s, against RAPTOR 18033.75 s and 46430.96 s, HippoRAG 6032.46 s and 13815 s | [9] Table 6 |
| Average retrieval time, 2Wiki | 0.093 s, against 0.053 s (E2GraphRAG) and 0.062 s (RAPTOR) | [9] Table 2 |
| Index size, one third-party corpus | 32 MB of text, about 7,000 passages, about 162,000 sentences, about 216,000 entities, about 1,200,000 edges | [14] |
| spaCy model sizes (wheel files, version 3.6.x) | `en_core_web_trf` 460,293,616 bytes (about 439 MiB); `en_core_web_sm` 12,803,313 bytes | [18] |

- **Speed-ups.** My arithmetic on Table 2: indexing is 2.1x faster than E2GraphRAG, 3.7x than
  HippoRAG, 4.6x than HippoRAG2, 4.8x than GFM-RAG, 5.3x than RAPTOR and 19.7x than LightRAG. At 10M
  tokens it is 15.1x faster than RAPTOR (the paper's figure, which my division reproduces) and 4.5x
  than HippoRAG [9].
- **Hardware.** The July 2026 investigation recorded an RTX 4090 for these timings; the extracts read
  in this run do not state the hardware, so it is **unstated** here. The driver script loads the
  embedding model on `cuda` unconditionally, so a CPU-only run needs a change to the script [7].
- **Index volume.** Sentences and entities are embedded as well as passages, so the vector count is far
  above the passage count: about 378,000 sentence and entity vectors against about 7,000 passages in
  the corpus of [14]. The July 2026 investigation estimated this at "2 to 3 times the embedding work of
  a passages-only index"; that was an estimate, not a measurement, and was written before the code
  was re-read to establish that only entity-bearing sentences are stored. No measurement of the
  embedding cost exists in the sources read: **unstated**.
- **Query cost grows with corpus size.** For each query the code scores every passage by
  dense similarity and by substring-counting every activated entity in every passage, then runs PPR
  over the whole graph [5]. The paper states retrieval complexity as linear in the number of
  passages [9]. The 0.093 s figure is for the 2Wiki corpus; query time at 5M or 10M tokens is
  **unstated** in the extracts read [9].
- **Dependencies.** Python 3.9 is "preferred" [2]. Pins include `spacy==3.6.1`,
  `sentence-transformers==2.2.2`, `python-igraph==0.11.8` and `numpy==1.21.0` [7]. The driver
  hard-codes `CUDA_VISIBLE_DEVICES` to one device [7].
- **Runs locally?** Indexing and retrieval do. Answer generation and the accuracy judge call an
  OpenAI-style endpoint: the README asks for an API key and a base URL [2]. Whether an open-weight
  model works is **unstated** (an issue on the topic exists and is closed; its content was not read) [11].
- **Config versus driver defaults.** The config class and the driver script disagree. Config:
  `iteration_threshold` 0.5, `top_k_sentence` 1, `passage_ratio` 1.5. Driver: 0.4, 3 and 2 [4][7].
  A result depends on which entry point is used.

## Evidence

### Published results (paper v4, read 20261030 19:00 UTC) [9]

Setup: HotpotQA, 2WikiMultiHopQA and MuSiQue use the HippoRAG corpus with 1,000 questions sampled from
each validation set; the medical subset of GraphRAG-Bench is the fourth dataset. Top-k is 5.
`gpt-4o-mini` generates and judges. The paper (as read) does not say how passages were produced [9].

Table 1, Contain-Acc / GPT-Acc, in percent:

| Dataset | LinearRAG | HippoRAG2 | GFM-RAG | LightRAG |
|---|---|---|---|---|
| HotpotQA | 64.30 / 66.50 | 62.90 / 64.30 | 62.70 / 65.60 | 60.30 / 59.50 |
| 2Wiki | 70.20 / 63.70 | 62.70 / 55.00 | 66.80 / 59.60 | 55.20 / 39.00 |
| MuSiQue | 33.90 / 37.00 | 31.00 / 35.00 | 29.90 / 34.60 | 27.40 / 28.60 |
| Medical (GPT-Acc only) | 63.72 | 60.77 | 56.07 | 54.36 |

Table 2 (2Wiki), average of Contain-Acc and GPT-Acc: LinearRAG 66.95, HippoRAG 63.00, GFM-RAG 63.20,
HippoRAG2 58.85, LightRAG 47.10, RAPTOR 46.10, E2GraphRAG 46.20. The two fastest retrievers
(E2GraphRAG, RAPTOR) score about 21 points lower [9].

Table 4 (GraphRAG-Bench medical, Recall / Relevance, percent). The definitions of the two metrics
were not read.

| Task | LinearRAG | Vanilla RAG (top 5) | GFM-RAG |
|---|---|---|---|
| Fact retrieval | 88.86 / 86.09 | 86.24 / 63.71 | 90.08 / 57.90 |
| Complex reasoning | 87.03 / 81.58 | 84.97 / 84.11 | 85.03 / 33.06 |
| Contextual summarization | 89.13 / 87.89 | 84.14 / 89.94 | 78.62 / 40.14 |
| Creative generation | 89.08 / 72.74 | 44.88 / 58.73 | 83.51 / 22.87 |

LinearRAG's relevance is below plain dense retrieval on complex reasoning (81.58 against 84.11) and on
contextual summarization (87.89 against 89.94), and its fact-retrieval recall is below GFM-RAG's
(88.86 against 90.08) [9].

Ablation (Figure 4): the text defines two variants, one without entity activation and one without
global importance aggregation (the PPR stage), and says both modules are critical. The values are in
the figure only and were not read in this run [9]. The July 2026 investigation read the loss from
removing either stage as about 2 to 3 points; that was not re-checked. Neither variant isolates the
entity edges themselves [9].

Complexity statement (Appendix D): construction and memory O(|P|·T), retrieval O(|P|), where P is the
passage set and T the average passage length [9].

Hyperparameters named in the paper: damping typically 0.85, up to about 4 iterations, a pruning
threshold δ stated as 4 for 2Wiki, and a "small" λ for the dense term, for example 0.05 [9]. The code
uses scores that are products of cosine similarities, so a threshold of 4 could never be reached; the
likely intent is 0.4 (my inference, not confirmed by the authors). How the paper's λ maps onto the code's
`passage_ratio` and `passage_node_weight` is not established.

### Third-party evidence

| Report | What it says | State at 20261030 | Source |
|---|---|---|---|
| Issue #25, "Reproducibility concerns", opened 20260507 | An outside researcher reports that results fall when the benchmarks' original passage splits are used instead of the authors'. Their EM figures, original split against the authors' split: HotpotQA 34.0 against 44.5, MuSiQue 16.4 against 21.3, 2Wiki 34.0 against 46.3. They changed `top_k_sentence` to 5 and also report results below a BM25 baseline at the setting of 1. Other participants add that the released dataset merges the original paragraphs into longer chunks and ask for EM and F1, standard deviations and a chunk-size sensitivity analysis | open, 8 comments | [16] |
| Maintainer reply, 20260518 | The original passages were merged and re-split by fixed token length to mimic unsegmented corpora, and all baselines used the same chunking. The medical subset now uses the scientific spaCy model, which reduces dense-retrieval fallback | recorded in the thread | [16] |
| Issue #17, opened 20260108 | Vectorized and loop retrieval give different results; the vectorized one is much worse on a 7,000-passage corpus. Maintainers named a top-k selection difference | closed; code updated 20260110 | [14][11] |
| Issue #19, opened 20260128 | Hub-entity attribute questions return high-connectivity passages instead of the attribute | closed; optional boost added | [15][17] |
| Issue #15, opened 20251230 | Adjacent edges are in the code but not in the paper; repeated indexing calls doubled edges. Maintainers: adjacency is optional; a fix followed in a commit named "fix add edges" dated 20260103 | closed; fix effect not verified | [13][11] |

The figures in the first row are the issue author's claims. They were not reproduced here. They show
that reported accuracy depends on the passage split, which the maintainers state they changed on
purpose and the paper (as read) does not describe [9][16].

## Direction

The repository has no roadmap or to-do list. The README news lists later work from the same group,
which is other projects (for example MemGraphRAG, LegalGraphRAG, LogicRAG and a GraphRAG benchmark),
not a successor to this one [2]. A web search for a successor or extension found none (20261030
19:00 UTC) [19]. The only commits since the March merge are README edits; the latest is dated
20260705 [11]. Three issues are open: a parameter question for MuSiQue with the vectorized mode, the
reproducibility thread, and a suggestion to add a troubleshooting reference [11].

## Changed since the July 2026 investigation

The July investigation is dated 20260725 15:34 UTC. Figures from it are "July" below.

- **Stars and forks.** July: about 526 stars and 61 forks. Now 566 and 68 (20261030 19:02 UTC), up
  about 40 and 7 in 97 days [1]. Nothing in the pattern looks inorganic.
- **Licence: unchanged, now read from the file.** `LICENSE.txt` is the standard GPL version 3 text, with
  the placeholder line "Copyright (2024) anonymous" [3]. It was added on 20251201, hours after a user
  asked in issue #13 and a maintainer answered that the code is GPL v3 [12][11]. The repository has no
  file named `LICENSE`; GitHub detects GPL-3.0 from `LICENSE.txt` [1][3]. Whether the project means "version
  3 only" or "version 3 or later" is **unstated**: the files read carry no per-file notice [3][5].
- **Activity.** No commit after 20260801; the last push and last commit are 20260705 00:55 UTC, a
  README edit. The last change to code was the merge on 20260304 [11]. With no push for 117 days, the
  project has aged from July's "active-ish" into **quiet**; nothing happened to cause it.
- **Archived, renamed, released.** Not archived; no rename; no release or tag [1].
- **Paper.** arXiv v4 (20251109) is still the latest version; no newer version [8]. The ICLR 2026
  poster is confirmed: session on 20260424, 15:15 to 17:45 UTC-3 [10]. The arXiv page itself carries no venue line [8][9].
- **Successor.** None found [2][19].
- **README and architecture.** The method description is unchanged. The README gained news items about
  unrelated projects of the group. Its "GitHub" badge links to a repository that the authenticated
  API reports as Not Found [2].
- **Issues.** None opened since the July investigation: the newest, #26, is dated 20260602. July did
  not record #25 (reproducibility, opened 20260507, still open), which is the main fact about the
  evidence above that July left out [11][16].
- **Corrections to the July text.** These are mistakes or imprecisions in the July investigation,
  now corrected in the body, not changes in the repository:
  1. July said all edges are "binary co-occurrence". The passage-entity edges are weighted by share of
     entity occurrences in the passage; only the sentence-entity links are binary [5].
  2. July said up to 3 propagation iterations. The default makes 2 rounds [5].
  3. July said all sentences are embedded. Only sentences with at least one retained entity are [6].
  4. July described the adjacent-passage edge as automatic. It depends on an integer prefix on the
     passage text, which the driver script adds, and the maintainers call it optional [5][7][13].
  5. July folded the paper's λ of 0.05 into the code's `passage_node_weight`. The code has two separate
     parameters, `passage_ratio` and `passage_node_weight`, and the mapping is not established [4][9].
  6. July gave "about 0.1 s" per query without noting that the code scans all passages per query [5][9].
  7. July called the main file a "1000-line class". The file read has 672 lines [5].
  8. July's "about 440 MB" for `en_core_web_trf` matches the 3.6.1 wheel (460 MB, 439 MiB) [18].
     July's "RoBERTa-based" is **unstated** in the sources read here.
  9. July did not record that the paper's results are the authors' own, on a passage split the authors
     chose and the paper (as read) does not describe, and that one outside report disputes the
     margin [16].
- **Not re-checked.** The July claims about the RTX 4090 and the 2 to 3 point ablation loss. They are
  marked as such in the body.

## Sources

1. https://api.github.com/repos/DEEP-PolyU/LinearRAG (also `/contributors`, `/releases/latest`, `/tags`): stars, forks, licence detection, archived flag, dates, no release, 5 contributors, 49 commits on the default branch (read 20261030 18:58 UTC; stars and forks re-read 20261030 19:02 UTC)
2. https://github.com/DEEP-PolyU/LinearRAG/blob/main/readme.md: description, install steps, news, defaults, API-key requirement (read 20261030 18:58 UTC)
3. https://github.com/DEEP-PolyU/LinearRAG/blob/main/LICENSE.txt: GPL version 3 text, copyright line, file history (read 20261030 18:58 UTC)
4. https://github.com/DEEP-PolyU/LinearRAG/blob/main/src/config.py: default parameters (read 20261030 18:59 UTC)
5. https://github.com/DEEP-PolyU/LinearRAG/blob/main/src/LinearRAG.py: indexing, graph, activation, passage scoring, PPR, fallback (read 20261030 19:00 UTC)
6. https://github.com/DEEP-PolyU/LinearRAG/blob/main/src/ner.py: entity and sentence extraction (read 20261030 19:00 UTC)
7. https://github.com/DEEP-PolyU/LinearRAG/blob/main/run.py, `src/evaluate.py`, `requirements.txt`: driver defaults, index prefixing, CUDA settings, evaluation metrics, pins (read 20261030 19:01 UTC)
8. https://arxiv.org/abs/2510.10114: title, authors, versions v1 to v4 with dates (read 20261030 18:59 UTC)
9. https://arxiv.org/html/2510.10114v4: method, Tables 1, 2, 4 and 6, appendix statements, setup (read 20261030 19:00 and 19:01 UTC; the last 1,508 characters of the page were not read; figures are not in the text extract)
10. https://iclr.cc/virtual/2026/poster/10007603: ICLR 2026 poster listing and session time (read 20261030 19:01 UTC)
11. https://github.com/DEEP-PolyU/LinearRAG/commits/main and the issues list: commit history, per-file history, issue and pull-request states (read 20261030 18:58 to 19:00 UTC)
12. https://github.com/DEEP-PolyU/LinearRAG/issues/13: licence question and maintainer answer (read 20261030 18:59 UTC)
13. https://github.com/DEEP-PolyU/LinearRAG/issues/15: adjacent-passage edges and repeated indexing (read 20261030 19:00 UTC)
14. https://github.com/DEEP-PolyU/LinearRAG/issues/17: vectorized versus loop retrieval; corpus size figures (read 20261030 18:59 UTC)
15. https://github.com/DEEP-PolyU/LinearRAG/issues/19: hub-entity attribute questions (read 20261030 19:00 UTC)
16. https://github.com/DEEP-PolyU/LinearRAG/issues/25: reproducibility thread and maintainer reply (read 20261030 19:00 UTC)
17. https://github.com/DEEP-PolyU/LinearRAG/pull/21 and https://github.com/DEEP-PolyU/LinearRAG/pull/23: attribute fallback added; revert closed without merge (read 20261030 18:59 UTC)
18. https://github.com/explosion/spacy-models/releases/tag/en_core_web_trf-3.6.1 (and the `en_core_web_sm-3.6.0` release): wheel sizes (read 20261030 19:01 UTC)
19. Web search "LinearRAG relation-free graph retrieval DEEP-PolyU successor OR follow-up OR extension 2026": no successor found; returned only the paper and its ICLR listing (run 20261030 19:00 UTC)
