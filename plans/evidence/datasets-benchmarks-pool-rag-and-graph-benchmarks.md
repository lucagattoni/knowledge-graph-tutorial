# Candidate pool: retrieval and graph-RAG benchmarks (datasets and benchmarks chapters)

Researcher notes, written 20261102 (UTC) for the writers of `docs/datasets/` and `docs/benchmarks/`. Every fact carries a source number `[n]`; the list with read times is at the end. All reads were done on 20261102 between 19:47 and 20:02 UTC. Where the sources are silent the text says **unstated**. First-party = run or published by the benchmark's own authors or by the system's own authors.

Twelve items, slug form as in the spec:

| Slug | Role | Dataset kinds | Paper (arXiv) | Citations (Semantic Scholar, read 20261102 20:01 UTC) [52] |
|---|---|---|---|---|
| `kilt` | both | questions, corpus | 2009.02252 | 939 |
| `beir` | both | questions, corpus | 2104.08663 | 2,235 |
| `crag` | both | kg, questions, corpus | 2406.04744 | 160 |
| `frames` | both | questions | 2409.12941 | 211 |
| `stark` | both | kg, questions, corpus | 2404.13207 | 94 |
| `graphrag-bench-xiang` | both | questions, corpus | 2506.05690 | 60 |
| `graphrag-bench-xiao` | both | questions, corpus | 2506.02404 | 36 |
| `wildgraphbench` | both | questions, corpus | 2602.02053 | 2 |
| `enterprise-rag-bench` | both | questions, corpus | 2605.05253 | 11 |
| `ragsearch` | benchmark only (no data of its own) | none | 2604.09666 | 1 |
| `multihop-rag` | both | questions, corpus | 2401.15391 | 353 |
| `hotpotqa` | both | questions, corpus | 1809.09600 | 5,972 |

Notes on the table. Semantic Scholar was rate-limited (HTTP 429) on single-paper calls; one batch call at 20:01 returned all twelve [52]. OpenAlex looked up by the arXiv DOI at 19:48 returned far lower numbers (for example BEIR 45, HotpotQA 97), because it counts only the arXiv record, not the published version; do not use those. The names `GraphRAG-Bench` are shared by two unrelated benchmarks; the slugs end in the first author. Pairs to link, not repeat: each dataset page and its benchmark page share a slug (`kilt`, `beir`, ...); the benchmark page holds tasks, metrics and results, the dataset page holds content, size, licence and construction.

Archive pages that use each item (grep of `kb-kg/`, `pinakes/`, root files, 20261102 20:01 UTC [55]): KILT 0 files; BEIR 0; CRAG 1 (`kb-kg/papers-benchmarks/README.md`); FRAMES 2 (that page and `kb-kg/projects/khoj.md`); STaRK 2 (that page and `kb-kg/directions/reasoning-retrieval.md`); GraphRAG-Bench 15 files, both benchmarks mixed (for example `kb-kg/literature/graph-rag-research.md`, `kb-kg/llm-era/README.md`, `kb-kg/projects/microsoft-graphrag.md`, `kb-kg/projects/linearrag.md`); WildGraphBench 1; EnterpriseRAG 1; RAGSearch 3 (`kb-kg/directions/reasoning-retrieval.md`, `kb-kg/directions/evidence-and-claims.md`, `kb-kg/papers-benchmarks/README.md`); MultiHop-RAG 10 (including `pinakes/experiments/datasets-benchmark.md`, `kb-kg/experiments/x2-index-cost/README.md`, `kb-kg/projects/minirag.md`); HotpotQA 13 (for example `kb-kg/projects/hipporag.md`, `kb-kg/projects/graph-r1.md`, `kb-kg/projects/linearrag.md`). KILT and BEIR have no archive page: they enter the pool because other pool items cite them as the older unified benchmarks (EnterpriseRAG-Bench cites both [35]; the HotpotQA and MultiHop-RAG papers compare to them [6]).

---

## 1. KILT (`kilt`), both

### Dataset

**What it contains.** A benchmark of eleven existing datasets in five tasks (fact checking: FEVER; entity linking: AIDA CoNLL-YAGO, WNED-WIKI, WNED-CWEB; slot filling: T-REx, Zero Shot RE; open-domain QA: Natural Questions, HotpotQA, TriviaQA, ELI5; dialogue: Wizard of Wikipedia), all re-aligned to one Wikipedia snapshot with provenance spans [1]. Every instance is a JSON line with id, input, output and provenance [1]. The knowledge source is a single file, `kilt_knowledgesource.json`, 34.76 GiB, 5,903,530 pages, built on the 2019/08/01 Wikipedia dump [2].

**Size and versions.** About 3.2 million instances over the eleven datasets [1]. Paper v4 is dated 20210527; the first version dates from September 2020 (arXiv id 2009) [1]. Entity-linking training data of 9 million extra instances from Wikipedia hyperlinks is released [1]. Test sets are not public; they are scored on an EvalAI challenge [1]. Repository last pushed 20220331 and archived (read-only) [5].

**Licence.** Code and the KILT files: the repository README states "KILT is MIT licensed" and the LICENSE file is the MIT text [2][3]. The Hugging Face card for `facebook/kilt_tasks` carries `license: mit` in its header but its "Licensing Information" section reads "[Needs More Information]"; the card for `facebook/kilt_wikipedia` says the same [4]. The terms of the eleven source datasets are not restated by KILT; for the ones also in BEIR, that paper lists FEVER and NQ as CC BY-SA 3.0 and HotpotQA as CC BY-SA 4.0 [6]. Whether the MIT label covers the redistributed Wikipedia text and source-dataset records is **unstated**.

**How it was made.** Each source dataset's Wikipedia provenance was mapped onto the 2019 snapshot by title and redirect matching, then by finding the span with the highest BLEU; dev and test items with BLEU below 0.5 for any provenance span were removed (on average 18% of dev/test for all tasks except entity linking); train sets were kept whole [1]. An Amazon Mechanical Turk campaign added provenance for Natural Questions (dev, test) and collected it from scratch for ELI5; mean provenance pages per NQ question rose from 1 to 1.57; Cohen's kappa between annotators was 0.3 for NQ and 0.1 for ELI5; ELI5 got provenance for 1,507 dev and 600 test items [1]. The NQ test set is a held-out portion obtained from the NQ authors [1].

**Used by.** Cited as a unified benchmark by BEIR and EnterpriseRAG-Bench [6][35]. No archive page [55]. Hugging Face lists it as source of `kilt_tasks` configs [4].

**Known problems.** In-KB only: every instance is answerable from the snapshot, so no unanswerable items (stated by the authors) [1]. Provenance is not exhaustive because Wikipedia is redundant (stated) [1]. Low annotator agreement on the added provenance (kappa 0.3 and 0.1) [1]. The snapshot is from 2019 [1]. Repository archived since 2022 [5]. Slot-filling can be gamed by title lookup, the authors note, so they treat it as a test of general models [1].

### Benchmark

**What it tests.** Whether one model and one index can serve many knowledge-intensive tasks, and whether it can name the evidence for its output [1].

**Tasks, metrics and protocol.** Five tasks (above). Downstream metrics by output format: Accuracy (discrete outputs), Exact Match (extractive and short abstractive), ROUGE-L (ELI5), F1 (Wizard of Wikipedia) [1]. Retrieval metric: page-level R-Precision [1]. Combined "KILT scores": a point is awarded only if the system ranks a complete provenance page set first (R-Precision = 1) [1]. Test predictions are uploaded to the EvalAI challenge (challenge page 689) [1].

**Datasets.** The eleven above, on the 5.9M-article snapshot [1].

**Results.** First-party only in the pages read. Independent leaderboard rows could not be read: the EvalAI page is rendered by script and returned no data on 20261102 [57].

| System | Score | Metric (test set) | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| RAG (Lewis et al.) | 86.31 / 72.62 / 48.07 / 47.61 | Accuracy: FEVER / AIDA / WNED-WIKI / WNED-CWEB | KILT authors | yes | paper v4, 20210527 | [1] |
| RAG | 59.2 / 44.74 | Accuracy: T-REx / zsRE | KILT authors | yes | same | [1] |
| RAG | 44.39 / 26.97 / 71.27 | EM: NQ / HotpotQA / TriviaQA | KILT authors | yes | same | [1] |
| RAG | 14.05 / 13.11 | ROUGE-L ELI5 / F1 WoW | KILT authors | yes | same | [1] |
| RAG, KILT scores | 53.45 FEVER, 23.12 T-REx, 36.83 zsRE, 32.69 NQ, 3.21 HotpotQA, 38.13 TriviaQA, 1.69 ELI5, 8.75 WoW | KILT-AC / KILT-EM / KILT-RL / KILT-F1 | KILT authors | yes | same | [1] |
| BART + DPR | 86.74 FEVER, 41.27 NQ, 25.18 HotpotQA, 58.55 TriviaQA | downstream | KILT authors | yes | same | [1] |
| Multi-task DPR | R-Precision 74.48 FEVER, 59.42 NQ, 42.92 HotpotQA, 61.49 TriviaQA | page R-Precision | KILT authors | yes | same | [1] |

Reading across the rows (labelled as my reading): the gap between downstream score and KILT score is large (HotpotQA EM 26.97 against KILT-EM 3.21 for RAG); the authors say the same, "generally low absolute numbers" [1].

**Known problems.** As for the dataset; plus the public leaderboard could not be checked, so current standing is **unstated**.

**Used by.** See dataset.

---

## 2. BEIR (`beir`), both

### Dataset

**What it contains.** Eighteen public retrieval datasets in nine tasks (fact checking, citation prediction, duplicate-question retrieval, argument retrieval, news retrieval, question answering, tweet retrieval, bio-medical IR, entity retrieval), plus MS MARCO as an in-domain reference (19 in the tables) [6]. Corpus sizes run from 3.6 thousand documents (NFCorpus 3,633) to 15 million (BioASQ 14,914,602); query counts per test set from 49 to 13,145 [6].

**Size and versions.** Table 1 of the paper gives per-dataset train/dev/test pairs, corpus size, relevant documents per query, query and document length [6]. Paper v4 is dated 20211021 [6]. The GitHub repository moved from `UKPLab/beir` (named in the paper) to `beir-cellar/beir`; last push 20251016 [9]. Four datasets (BioASQ, Signal-1M, TREC-NEWS, Robust04) are marked as not directly downloadable in the README and need a licence or reproduction scripts [7].

**Licence.** Library: Apache-2.0 [9]. Data: the Hugging Face card declares `cc-by-sa-4.0` [8], but the paper's Appendix E lists per-dataset terms that differ: MS MARCO "MIT License for non-commercial research purposes"; FEVER, NQ, DBPedia, Signal-1M CC BY-SA 3.0; TREC-NEWS, Robust04, BioASQ "under Copyright"; ArguAna and Touché-2020 CC BY 4.0; CQADupStack Apache-2.0; SciFact CC BY-NC 2.0; SCIDOCS GPL v3.0; HotpotQA CC BY-SA 4.0; TREC-COVID a "Dataset License Agreement"; four datasets (NFCorpus, FiQA-2018, Quora, Climate-FEVER) state no licence [6]. The README says the authors "do not ... claim that you have license to use the dataset" and put the check on the user [7]. So the card label does not describe the parts.

**How it was made.** Selection, not creation: public datasets were converted to one format (corpus, queries, qrels) and the authors report trying to balance tasks so that question answering does not dominate [6]. For TREC-COVID the authors added missing relevance judgements by hand to test lexical bias [6].

**Used by.** Cited as a baseline benchmark in the EnterpriseRAG-Bench paper [35] and compared with KILT in the paper [6]. No archive page [55].

**Known problems.** The authors flag a strong lexical bias, since lexical systems were used when judgements were made, which disadvantages non-lexical systems; their manual TREC-COVID re-annotation raised non-lexical scores [6]. Mixed and partly missing licences (above). Several datasets cannot be redistributed [7].

### Benchmark

**What it tests.** Zero-shot out-of-distribution generalisation of retrieval models: train elsewhere (mostly MS MARCO), test on the 18 sets [6].

**Tasks, metrics and protocol.** Primary metric nDCG@10; Recall@100 also reported [6]. Ten systems from five families: lexical (BM25 via Anserini), sparse (DeepCT, SPARTA, docT5query), dense (DPR, ANCE, TAS-B, GenQ), late interaction (ColBERT), re-ranking (BM25 + cross-encoder) [6].

**Datasets.** The 18 above [6].

**Results.** First-party paper results, Table 2 (nDCG@10, zero-shot) [6]:

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| BM25 | 0.656 TREC-COVID, 0.603 HotpotQA, 0.367 Touché-2020, 0.465 BioASQ | nDCG@10 | BEIR authors | yes | 20211021 (v4) | [6] |
| BM25 + cross-encoder | 0.757, 0.707, 0.271, 0.523 (same four sets) | nDCG@10 | BEIR authors | yes | same | [6] |
| TAS-B (dense) | 0.481, 0.584, 0.162, 0.383 | nDCG@10 | BEIR authors | yes | same | [6] |
| DPR (dense) | 0.332, 0.391, 0.131, 0.127 | nDCG@10 | BEIR authors | yes | same | [6] |
| Average against BM25 (last row of Table 2) | BM25+CE +11%; docT5query +1.6%; DPR -47.7% (column order taken from the table header) | relative nDCG@10 | BEIR authors | yes | same | [6] |

The authors' conclusion: BM25 is a robust baseline; re-ranking and late interaction do best at high cost [6].

Independent: an "official" self-service leaderboard exists on EvalAI (challenge 1897); the wiki page that points to it was last edited 20230110 and the older Google Sheets leaderboards are marked deprecated; no rows are on the wiki [11]. A SIGIR 2024 resource paper by Kamalloo, Thakur, Lassance and three others (6 authors) supplies reproducible reference models and the leaderboard; only the abstract was read, so no numbers from it [10]. Current leaderboard rows: **not read**.

**Known problems.** As above (lexical bias, licences). Query length: all datasets except ArguAna have short queries [6].

**Used by.** See dataset.

---

## 3. CRAG (`crag`), both

### Dataset

**What it contains.** 4,409 question-answer pairs in five domains (finance 1,039, sports 833, music 624, movie 1,125, open 788) and eight question types (simple 1,205; simple with condition 689; set 403; comparison 536; aggregation 489; multi-hop 382; post-processing heavy 180; false premise 525), with four dynamism classes (real-time 437, fast-changing 564, slow-changing 1,007, static 2,401) [12]. Retrieval content: up to 50 stored HTML pages per question from the Brave Search API (220K pages in all), mock knowledge graphs with 2.6 million entities, and 38 mock APIs [12]. 2,425 questions come from web content and 1,984 from knowledge graphs, split by entity popularity 661 head, 658 torso, 665 tail [12].

**Size and versions.** Paper v2 dated 20241101 [12]. Released files in the repository are named `dev_v4` (QA pairs and pages) [14]. The released set is the validation and public-test parts (30% + 30% of the benchmark, 2,706 examples in stage 1 of the challenge); 40% was held out as a private test for the KDD Cup 2024 [12]. Repository last pushed 20250614 [14][15].

**Licence.** The LICENSE file is CC BY-NC 4.0 (Attribution-NonCommercial 4.0 International); the README states the same [13]. GitHub's API reports the licence as "Other" (not recognised as an SPDX id) [15]. Non-commercial: read-only reference for the project.

**How it was made.** KG questions: 600+ templates filled with entities sampled by popularity; web questions: annotators wrote user-style questions and built QA pairs from search results; questions were paraphrased and ground truths manually verified [12]. Snapshots of web and KG data were taken at question time to keep real-time questions answerable [12].

**Used by.** KDD Cup 2024 Meta CRAG challenge [12][17]. One archive page lists it (papers-benchmarks) [55]. Used by no other pool item.

**Known problems.** The authors state that the three tasks do not evaluate first-stage retrieval over the whole corpus; the 220K pages can be used as a corpus for that, but it "does not match the entire web" [12]. Estimated web-search recall is 85% with 50 pages and 69% for the top 5, so many questions are unanswerable from the five pages of Tasks 1 and 2 by design [12]. Over 30% of questions had the answer in retrieval results but cut by the context window [12]. Time-sensitive answers date (snapshot dated at collection) [12].

### Benchmark

**What it tests.** Factual QA with RAG over web pages and KG APIs, including honesty about missing information [12].

**Tasks, metrics and protocol.** Task 1: summarise from five provided pages. Task 2: add KG mock APIs. Task 3: 50 pages plus APIs, so ranking matters [12]. Each answer is perfect (1), acceptable (0.5), missing (0) or incorrect (-1); "truthfulness" is the mean. Auto-eval merges perfect and acceptable, scores accurate 1, missing 0, incorrect -1, with two LLM judges (gpt-3.5-turbo-0125 and Llama 3 70B) averaged; agreement with human grading F1 94.7% and 98.9% [12]. The repository's evaluator uses the 1/0/-1 scheme [13].

**Datasets.** The CRAG set above.

**Results.**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| GPT-4 Turbo, LLM only | accuracy 33.5, hallucination 13.5, missing 53.0, truthfulness 20.0 | auto-eval, public test (1,335 questions) | CRAG authors (Meta) | yes | v2 20241101 | [12] |
| GPT-4 Turbo, Task 3 | accuracy 43.6, hallucination 30.1, truthfulness 13.4 | same | CRAG authors | yes | same | [12] |
| Llama 3 70B Instruct, Task 3 | accuracy 40.6, hallucination 31.6, truthfulness 9.1 | same | CRAG authors | yes | same | [12] |
| Copilot Pro (industry system) | perfect 62.6, truthfulness 50.6 (equal weights); 60.5 traffic-weighted | human eval | CRAG authors, queried products | yes (authors ran third-party products) | same | [12] |
| Gemini Advanced | truthfulness 49.3 (59.3 traffic-weighted) | human eval | CRAG authors | yes | same | [12] |
| ChatGPT Plus | 41.5 (41.8) | human eval | CRAG authors | yes | same | [12] |
| Meta SG | 41.4 (50.5) | human eval | CRAG authors | yes | same | [12] |
| Perplexity.ai | 34.9 (45.9) | human eval | CRAG authors | yes | same | [12] |
| Team db3, KDD Cup 2024 | 28.4% / 42.7% / 47.8% on tasks 1 / 2 / 3, first place on all three | challenge score, private test; scale not defined in the abstract | challenge team (own report) | independent of the benchmark authors, first-party for its own system | report 20240913 | [16][17] |

The paper itself warns that the industry rows and the straightforward rows are not fully comparable (different retrieval access; auto-eval versus human-eval) [12]. Per-task podiums (second and third places: Task 1 md_dh, ElectricSheep; Task 2 APEX, md_dh; Task 3 APEX, vslyu-team) are on the AIcrowd winners page, which shows no scores [17].

**Known problems.** See dataset. Industry-system rows are a snapshot of products in mid-2024.

**Used by.** KDD Cup 2024 [12][17].

---

## 4. FRAMES (`frames`), both

### Dataset

**What it contains.** 824 multi-hop questions that need 2 to 15 Wikipedia articles (about 36% need two, 35% three, 16% four), each with a gold answer and its list of articles, labelled with reasoning types: multiple constraints (about 36%), numerical (about 20%), tabular, temporal, post-processing; a question can have several [18][19].

**Size and versions.** One release, 824 items (paper v3, 20250124) [18][19].

**Licence.** Hugging Face card header: `license: apache-2.0` [19]. No separate LICENSE file for the data was read.

**How it was made.** LLM-generated questions were tried first and rejected (more than 30% hallucinated); then vetted human annotators wrote questions from multiple articles, labelled reasoning types; three months later answers were re-annotated and 5.5% were dropped for being no longer true; questions were rewritten with a date ("As of August 1, 2024") to remove freshness ambiguity; yes/no questions were removed [18].

**Used by.** Not used by any other item in the pool [55]; the archive mentions it on two pages [55].

**Known problems.** Authors name possible pre-training contamination (Wikipedia is in training data) and limited coverage of real-world queries [18]. Answers are tied to a date. The dataset card has apparent errors: `size_categories: n>1T` and `pretty_name: Who are I or you` [19].

### Benchmark

**What it tests.** Factuality, retrieval and reasoning together in end-to-end RAG [18].

**Tasks, metrics and protocol.** Accuracy of the final free-form answer judged by an LLM autorater (agreement with human grading 0.96, Cohen's kappa 0.889 with Gemini-Pro-1.5-0514 as rater) [18]. Settings: naive prompt, BM25-retrieved articles (2 or 4), oracle prompt with all gold articles, and a multi-step pipeline (k queries per step over n steps, BM25, n_docs per query) [18].

**Datasets.** FRAMES (above), Wikipedia dump with BM25 [18].

**Results.** First-party only.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Gemini-Pro-1.5-0514, naive prompt | 0.408 | accuracy | FRAMES authors (Google DeepMind) | yes | paper v3, 20250124 | [18] |
| same, BM25-R 2 docs / 4 docs | 0.452 / 0.474 | accuracy | same | yes | same | [18] |
| same, oracle prompt | 0.729 | accuracy | same | yes | same | [18] |
| same, multi-step (k,n,n_docs = 5,5,10) | 0.66 | accuracy | same | yes | same | [18] |
| Gemini-Flash-1.5-0514 naive / BM25-4 / oracle | 0.263 / 0.315 / 0.665 | accuracy | same | yes | same | [18] |
| Gemma2-27b, Llama3.2-3B, Qwen2.5-3B naive | 0.308, 0.115, 0.095 | accuracy | same | yes | same | [18] |

No independent result was found in the sources read; a web search returned only restatements of these numbers and a vendor page, which are leads, not sources [58].

**Known problems.** Models are from 2024 and the numbers predate newer models; judge dependence (LLM autorater) [18].

---

## 5. STaRK (`stark`), both

### Dataset

**What it contains.** Three semi-structured knowledge bases, each a knowledge graph plus free text per node, with retrieval queries whose answers are sets of nodes. STaRK-Amazon: 1,035,542 entities, 9,443,802 relations, 592M tokens; STaRK-MAG: 1,872,968 entities, 39,802,116 relations, 213M tokens; STaRK-Prime (biomedicine, from PrimeKG): 129,375 entities, 8,100,498 relations, 32M tokens [20]. Queries: synthesised 9,100 (Amazon), 13,323 (MAG), 11,204 (Prime), split train/val/test roughly 0.55-0.65 / 0.17-0.20 / 0.18-0.25; plus human-written test-only queries 81, 84 and 98 [20].

**Size and versions.** Paper v3 20241020; human-generated queries were added in May 2024; leaderboard opened October 2024 [20][22]. Repository last pushed 20260206 [23].

**Licence.** Hugging Face dataset card `cc-by-4.0` [21]; code MIT (LICENSE; GitHub API) [22][23]. The paper says it "adhered to the licenses of each public resource" and names sources: Amazon Product Reviews and Q&A, ogbn-mag, MAG, PrimeKG with Orphanet, DrugBank, Reactome, Ensembl, NCBI Entrez, Uniprot, UCSC, CPDB [20]. Whether CC BY 4.0 fits each source's terms is **unstated**.

**How it was made.** A four-step synthesis: sample a relational template, extract textual properties of a sampled gold entity with an LLM, merge into a natural query, then filter the answer set so that every candidate satisfies both textual and relational parts [20]. Human check on naturalness, diversity, practicality: average positive rates 78.7%, 71.0%, 76.4% (non-negative 94.1%, 85.3%, 89.4%) [20].

**Used by.** Chen et al. (AWS, Cisco), STaRK-Prime, human-generated queries [51]; two archive pages [55].

**Known problems.** Synthesised queries may be harder or easier than human ones; the paper finds human-written queries generally scored higher [20]. Human-written sets are small (81 to 98). Ground truth built by automatic plus manual filtering [20].

### Benchmark

**What it tests.** Retrieval that must satisfy textual and relational requirements together [20].

**Tasks, metrics and protocol.** Given a knowledge graph, documents and a query, return the set of matching nodes. Hit@1, Hit@5, Recall@20, MRR [20]. Baselines in five classes: BM25; DPR, ANCE, QAGNN; LLM dense retrievers (ada-002, voyage-large-2-instruct, LLM2Vec, GritLM-7b); multivector (multi-ada-002, ColBERTv2); LLM rerankers (Claude 3 Opus, GPT-4 Turbo) on top-20 ada-002 results, run on a random 10% of the test queries because of cost [20].

**Datasets.** The three STaRK knowledge bases.

**Results.**

| System | Score (Hit@1) | Metric / set | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| BM25 | Amazon 44.94, MAG 25.85, Prime 12.75 | Hit@1, full synthesised test | STaRK authors | yes | v3, 20241020 | [20] |
| GritLM-7b | 42.08, 37.90, 15.57 | same | same | yes | same | [20] |
| ColBERTv2 | 46.10, 31.18, 11.75 | same | same | yes | same | [20] |
| ada-002 | 39.16, 29.08, 12.63 | same | same | yes | same | [20] |
| GPT-4 reranker (10% sample) | 44.79, 40.90, 18.28 | same | same | yes | same | [20] |
| Claude 3 reranker (10% sample) | 45.49, 36.54, 17.79 | same | same | yes | same | [20] |
| Claude 3.7 Sonnet, documents only (RAG with LLM answer and entity selection) | 0.6147 | Hit@1, STaRK-Prime human-generated queries, end-to-end generation metric | Chen et al., AWS and Cisco | independent of STaRK authors | 20260624 | [51] |
| same, documents plus 1-hop relation lists | 0.6972 | same | same | independent | same | [51] |
| same, GraphRAG with KG computed from the documents | 0.5596 | same | same | independent | same | [51] |
| same, GraphRAG with predefined KG and vector search (100 paths, 5 entity subgraphs) | 0.6422 | same | same | independent | same | [51] |
| same, GraphRAG with predefined KG only | 0.1376 | same | same | independent | same | [51] |
| same, agent with document tool only / with added KG tool | 0.6881 / 0.6055 | same | same | independent | same | [51] |

Caveat: the Chen et al. metric scores the LLM's final entity list, not the raw ranking, so its Hit@1 is not comparable with Table 6 of the STaRK paper (the authors say so) [51]. Its test-set size is **unstated**; the STaRK paper gives 98 human-written Prime queries, but the Hit@1 values are multiples of 1/109, so the set used is not 98 (my inference) [20][51]. Official leaderboard on a Hugging Face space (`snap-stanford/stark-leaderboard`): the space returned HTTP 503 at 20:00 and 20:01, so rows are **not read** [59].

**Known problems.** Latency on million-entity bases (Table 8 of the paper) [20]; the rerankers were evaluated on 10% samples only [20].

**Used by.** See dataset.

---

## 6. GraphRAG-Bench, Xiang et al. (`graphrag-bench-xiang`), both

### Dataset

**What it contains.** Two corpora with question sets: Medical (NCCN clinical guidelines) and Novel (pre-20th-century novels from Project Gutenberg, lesser-known works chosen to limit overlap with LLM training data) [24]. Questions in four levels: fact retrieval, complex reasoning, contextual summarise, creative generation [24]. Released question files: Novel 2,010 and Medical 2,062 items (my count on 20261102 19:54, files `novel_questions.json` and `medical_questions.json`) [26]. Per level, Novel: 971 / 610 / 362 / 67; Medical: 1,098 / 509 / 289 / 166 (my count) [26].

**Size and versions.** The paper states 4,076 questions [24]; the released files sum to 4,072 (mismatch of 4; the Hugging Face dataset was last modified 20250713, the paper's v3 is 20260222, so the files may be an older version; unstated) [24][26]. Corpus sizes: Novel about 1,132k tokens (paper's "Large" tier = full dataset), a small tier of about 56k tokens (one book) [24]. Entity-graph statistics (Table 9): Novel average degree 2.27, 66% non-isolated entities; Medical 1.05, 48%; against 0.86 for UltraDomain [24].

**Licence.** Code repository: MIT (LICENSE file, copyright XMU-DeepLIT) [25]. The Hugging Face dataset card declares no licence field; its badge points to the MIT licence of the code repository [26]. The NCCN guideline text is a publisher's document; the redistribution terms are **unstated** in the paper and card. Novel texts come from Project Gutenberg [24].

**How it was made.** Six stages: corpus collection; ontology/logic mining with GPT-4.1; evidence collection as subgraphs and multi-hop chains; question generation matched to evidence structure (difficulty set by knowledge breadth and reasoning depth); check and correct (questions discarded if the evidence cannot be derived from the corpus, with model plus human checking); refinement with GPT-4.1 adding background context to each question [24].

**Used by.** Cited as a GraphRAG benchmark by WildGraphBench, which also uses it in its graph-density comparison [32]; the archive records a RAGU paper (July 2026) that ran it [53]. Fifteen archive pages mention a GraphRAG-Bench [55].

**Known problems.** (1) The paper's Table 12 (Novel under three corpus sizes) has a small-tier RAG row 64.73 / 58.64 / 65.75 / 60.61 that equals the Medical "RAG with rerank" row of Table 2, not the Novel row (60.92 / 42.93 / 51.30 / 38.26); the text then claims RAG degrades from 58.64 to 43.20, which depends on that row (re-checked in v3 on 20261102 19:48) [24]. (2) Question counts differ between paper and released files (above) [24][26]. (3) The ontologies and questions are built with GPT-4.1, so the set inherits that model's view [24]. (4) The benchmark was designed to have denser graphs than HotpotQA-type sets, which favours graph methods by construction (my reading of the paper's own motivation) [24]. (5) Another team measures this benchmark's graph as "structurally sparse" under the LightRAG pipeline (average degree lower than WildGraphBench) [32].

### Benchmark

**What it tests.** When graphs help RAG: graph construction, retrieval and generation, over tasks of increasing difficulty [24].

**Tasks, metrics and protocol.** Generation: accuracy and ROUGE-L (levels 1 and 2), accuracy and evidence coverage (level 3), accuracy, faithfulness score and coverage (level 4). Retrieval: context relevance and evidence recall. Graph quality: node count, edge count, average degree, clustering coefficient. Main table uses GPT-4o-mini as generator [24]. Seven GraphRAG frameworks plus RAG with and without rerank [24].

**Datasets.** Novel and Medical, with scaled corpus tiers [24].

**Results.** Accuracy, GPT-4o-mini (Table 2 of v3, Novel / Medical) [24]:

| System | Fact | Complex reasoning | Summarise | Creative | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|---|---|
| RAG with rerank, Novel | 60.92 | 42.93 | 51.30 | 38.26 | benchmark authors | yes | v3 20260222 | [24] |
| HippoRAG2, Novel | 60.14 | 53.38 | 64.10 | 48.28 | benchmark authors | yes (other team's method) | same | [24] |
| MS-GraphRAG, Novel | 49.29 | 50.93 | 64.40 | 39.10 | benchmark authors | yes | same | [24] |
| LightRAG, Novel | 58.62 | 49.07 | 48.85 | 23.80 | benchmark authors | yes | same | [24] |
| RAG with rerank, Medical | 64.73 | 58.64 | 65.75 | 60.61 | benchmark authors | yes | same | [24] |
| HippoRAG2, Medical | 66.28 | 61.98 | 63.08 | 68.05 | benchmark authors | yes | same | [24] |
| LightRAG, Medical | 63.32 | 61.32 | 63.14 | 67.91 | benchmark authors | yes | same | [24] |

Live leaderboard (CSV behind `graphrag-bench.github.io`, read 20261102 19:59; repository commits to 20261027): 21 rows Novel and 21 rows Medical, with a month-level Date column, a Link per row, and the paper's own baselines included; the rows added later are submissions by third parties and vendors, each pointing at the submitter's own page or paper, so they are first-party for the submitter; whether the maintainers re-ran any is **unstated** [27].

| System (Novel average, all four levels) | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| KnowCosmos (Galaxybase) | 70.34 | leaderboard average | submitter | yes | 2025.09 | [27] |
| Sapient-Bodhi-GraphRAG | 66.30 | same | submitter | yes | 2026.10 | [27] |
| GraphRAG-SDK (FalkorDB) | 66.09 | same | submitter | yes | 2026.08 | [27] |
| KT-MOSAIC | 64.28 | same | submitter (arXiv 2609.11065) | yes | 2026.09 | [27] |
| HippoRAG2 | 56.48 | same | benchmark authors | yes | 2025.02 (method date) | [27] |
| RAG (w rerank) | 48.35 | same | benchmark authors | yes | n/a | [27] |
| RAPTOR | 43.24 | same | benchmark authors | yes | 2024.01 | [27] |

Independent: Han et al. and WildGraphBench re-use the benchmark's corpus statistics but not its leaderboard [32][49]. The archive also records a July 2026 analysis (RAGU) that ran HippoRAG 2 on the Medical set; not re-verified here [53].

**Known problems.** As in the dataset section; the leaderboard has no uniform protocol check for submitted rows (unstated) [27].

---

## 7. GraphRAG-Bench, Xiao et al. (`graphrag-bench-xiao`), both

### Dataset

**What it contains.** 1,018 college-level questions in five formats (fill-in-blank, multiple choice with 4 options, multi-select 2 to 4 of 4, true/false, open-ended) across 16 computer-science topics, each with a gold rationale; a corpus of 7 million words from 20 textbooks parsed into markdown and structured JSON [28][29]. Question files FB, MC, MS, OE, TF in the repository [29]. (The archive's table said the question count was unstated from the abstract; the introduction and README give it.)

**Size and versions.** Paper v3 dated 20250620; repository last pushed 20250801; the Hugging Face dataset moved from `jeremycp3/GraphRAG-Bench` to `Awesome-GraphRAG/GraphRAG-Bench` (redirect seen 20261102 19:58) [28][29][30].

**Licence.** Repository: no LICENSE file, GitHub API licence null [29]. Hugging Face card: "This dataset can only be used for academic research and cannot be used for any commercial purposes. It is prohibited to distribute or modify the content of the dataset." [30]. So it is non-commercial and no-redistribution: a read-only reference for the project. The corpus is parsed text of 20 copyrighted textbooks; the card does not name the books' licences (unstated).

**How it was made.** From more than 100 CS publications over 16 subfields the authors picked 20 textbooks, parsed the PDFs (PyMuPDF; OCR for scanned pages; layout and extraction models), and domain experts screened and refined 1,018 questions [28].

**Used by.** Cited by WildGraphBench [32]; leaderboard of nine GraphRAG methods [31].

**Known problems.** Questions need college-level maths, programming and proofs, so graph retrieval cannot help some of them (the authors find all GraphRAG methods lower accuracy on mathematics) [28]. Redistribution of the corpus is prohibited by the card. No question-level split by difficulty.

### Benchmark

**What it tests.** Whether graph structure improves reasoning, not only retrieval; scores the answer and a rationale [28].

**Tasks, metrics and protocol.** Answer accuracy per question type; reasoning score R (match to gold rationale) and AR (rationale correct when the answer is correct); graph construction, retrieval, generation reported separately; nine GraphRAG methods with GPT-4o-mini [28].

**Datasets.** The 1,018 questions on the 20-textbook corpus [28].

**Results.** Average accuracy over the five formats, GPT-4o-mini base (Table 4) [28]; the official leaderboard (deep-polyu.github.io/RAG, read 20261102 19:58) repeats exactly these 12 rows with no later entries [31].

| System | Average accuracy | Average R / AR | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| RAPTOR | 73.58 | 60.81 / 45.53 | benchmark authors | yes | paper v3 20250620 | [28][31] |
| HippoRAG | 72.64 | 60.90 / 44.55 | same | yes | same | [28][31] |
| GraphRAG (Microsoft) | 72.50 | 59.43 / 43.30 | same | yes | same | [28][31] |
| GFM-RAG | 72.10 | 60.36 / 44.30 | same | yes | same | [28][31] |
| KGP | 71.86 | 58.74 / 42.22 | same | yes | same | [28][31] |
| TF-IDF (plain retrieval) | 71.71 | 57.61 / 42.38 | same | yes | same | [28][31] |
| ToG | 71.71 | 60.17 / 44.01 | same | yes | same | [28][31] |
| BM25 (plain retrieval) | 71.66 | 59.18 / 44.15 | same | yes | same | [28][31] |
| LightRAG | 71.22 | 60.46 / 43.81 | same | yes | same | [28][31] |
| GPT-4o-mini, no retrieval | 70.68 | 55.45 / 39.78 | same | yes | same | [28][31] |
| G-Retriever | 69.84 | 60.17 / 43.66 | same | yes | same | [28][31] |
| DALK | 69.30 | 58.89 / 42.12 | same | yes | same | [28][31] |

Reading (labelled): on answer accuracy the spread is 4 points and plain TF-IDF and BM25 are inside it; the larger gap is in rationale scores, where every graph method beats no retrieval [28]. The leaderboard "Date" column holds each method's release date, not run date (for example RAPTOR 2025-01-31) [31].

**Known problems.** One generator (GPT-4o-mini) in the main table; single run (unstated number of runs) [28]. The leaderboard has not been extended since the paper [31].

**Used by.** See dataset.

---

## 8. WildGraphBench (`wildgraphbench`), both

### Dataset

**What it contains.** For 12 top-level Wikipedia topics, one article each with many references: the crawled reference pages as the retrieval corpus (raw text including boilerplate), the Wikipedia statements as gold facts, and questions of three kinds [32][33]. Topics and article: Culture (Marvel Cinematic Universe), Geography (United States), Health (COVID-19 pandemic), History (World War II), Human activities (2022 FIFA World Cup), Mathematics (Prime number), Nature (2012 Pacific typhoon season), People (Donald Trump), Philosophy (Authoritarian socialism), Religion (Persecution of Muslims), Society (Human), Technology (Steam service) [33].

**Size and versions.** 1,197 questions: 667 single-fact, 191 multi-fact, 339 summary (paper Table 1 and README) [32][33]. The abstract and introduction say "1,100" questions, which is a mismatch with Table 1 (1,197) [32]. Reference pages per article from 50 (Prime number) to 547 (Donald Trump) [33]. Paper v2 20260203; ACL 2026 Findings per the README; repository created 20260202, last push 20260511 [32][33][34].

**Licence.** Repository and Hugging Face dataset: Apache-2.0 (LICENSE file is the Apache text; HF tag `license:apache-2.0`) [33][34]. The paper states the cited web pages remain under their own terms, the benchmark is research-only, and "any redistribution or derivatives should comply with the original access conditions" [32]. So the Apache label does not cover the third-party page text.

**How it was made.** References were fetched with jina.ai (archive copies used if the page failed); the Wikipedia article was split into leaf sections; sentences with citations were rewritten by an LLM into clean statements; statements with one reference make single-fact questions, with at least two references and an LLM-judged requirement that at least two are jointly needed make multi-fact questions; summary questions come from whole leaf sections, written without the section text [32].

**Used by.** The "BM25 Wins at Scale" study is by the same first author and affiliations, so it is not independent of this benchmark [50][32]. No archive page beyond the papers-benchmarks page [55].

**Known problems.** Gold facts come from Wikipedia and inherit its editorial gaps and errors; LLM judging and statement matching may be biased (authors' limitations) [32]. The corpus contains noise, bias, outdated claims, toxic language and possibly personal data (authors' risk note) [32]. Wording leaks from another table: the paper's text refers to "the Novel Dataset" and "the people subset" for Table 2, which suggests copy-over from GraphRAG-Bench; Table 2 itself appears to be the full set (my reading) [32]. Only 12 articles in total; per-domain counts are very uneven (for example 36 questions for History, one multi-fact) [33].

### Benchmark

**What it tests.** GraphRAG on long, noisy, heterogeneous web evidence: retrieval and aggregation across sources [32].

**Tasks, metrics and protocol.** Single-fact and multi-fact: LLM judge says whether the answer equals the gold statement; accuracy. Summary: statement-level recall, precision and F1 against the leaf section's gold statements. Setup: chunks of 1,200 tokens with 100 overlap, top-5 (QA) and top-10 (summary), gpt-4o-mini for graph building and answering, gpt-5-mini as judge [32]. Human performance measured on the people subset [32].

**Datasets.** WildGraphBench corpus [32].

**Results.** All from the benchmark authors (Table 2 of v2; also the repository README) [32][33].

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| HippoRAG2 | avg 64.33; single 71.51; multi 39.27 | accuracy | benchmark authors | yes | v2 20260203 | [32][33] |
| NaiveRAG | avg 59.79; single 66.87; multi 35.08; summary F1 15.84 (recall 13.54, best) | accuracy / F1 | same | yes | same | [32][33] |
| MS GraphRAG (global) | multi 47.64 (best); avg 54.54; summary F1 13.78 | same | same | yes | same | [32][33] |
| LightRAG (hybrid) | avg 56.76; multi 40.84; F1 14.61 | same | same | yes | same | [32][33] |
| BM25 | avg 36.83; F1 12.66 | same | same | yes | same | [32][33] |
| LinearRAG | avg 44.87; precision 29.20 (best) | same | same | yes | same | [32][33] |
| MS GraphRAG (local) | avg 38.23 | same | same | yes | same | [32][33] |
| Fast-GraphRAG | avg 33.56 | same | same | yes | same | [32][33] |
| Human, people subset | avg 85.66; single 89.61; multi 71.88; F1 15.30 | same | benchmark authors, graduate-level annotators | yes | same | [32] |

Reading (labelled): graph methods win on multi-fact only for MS GraphRAG (global) and a few others; on summaries the plain NaiveRAG has the best F1, and no system approaches human recall (38.59 for humans against under 14 for systems) [32]. No independent result found. Number of runs per cell: **unstated**.

**Known problems.** As in the dataset section; top-k fixed per task; one generator [32].

**Used by.** See dataset.

---

## 9. EnterpriseRAG-Bench (`enterprise-rag-bench`), both

### Dataset

**What it contains.** A synthetic company ("Redwood Inference", an AI inference service) with documents in nine source types and 500 questions in ten categories (basic 175, semantic 125, intra-document reasoning 40, project related 40, constrained 30, conflicting info 20, completeness 20, miscellaneous 20, high level 10, info not found 20) [35][36]. Documents per source from the Hugging Face card: Slack 285,605; Gmail 121,390; Linear 35,308; Google Drive 25,108; HubSpot 15,017; Fireflies 10,173; GitHub 8,052; Jira 6,120; Confluence 5,189 [36]. Each question has a gold answer, atomic answer facts and gold document ids (none for high-level and info-not-found) [35][36]. An extra 100 metadata-dependent questions are in a separate file and excluded from the leaderboard [37].

**Size and versions.** Document total: the card's sum is 511,962, the paper's full tier 511,962, the abstract "approximately 500,000" [35][36]; the independent scaling study counts 511,957 documents plus 2 scaffold files = 511,959 [50]. The three counts differ by up to 5. Release v1.0.0; paper v2 20260519; dataset card last modified 20260508 [35][38][39]. Repository created 20260219, last push 20260903 [37].

**Licence.** MIT on the Hugging Face dataset (tag `license:mit`) and code (LICENSE file; README "Code_License MIT") [36][37][38]. The data is synthetic text generated by LLMs; the generating models' output terms are not discussed (unstated). The card carries a canary string against training-set inclusion [36].

**How it was made.** Scaffolding by human plus LLM (company overview, initiatives, employee directory, source structure, `agents.md` format files); high-fidelity generation of project clusters (each project about 100 documents) with cross-document awareness; high-volume generation by topic scaffolding with at most 500 documents per leaf topic (without scaffolding an LLM judge found over 40% of 100 documents had a close sibling); then four noise types (random shuffle, LLM shuffle, near-duplicates with changed facts, miscellaneous files); questions from three families of generation flows; quality checks by LLM conformance checks, pooling of three retrievers (BM25, vector, bash agent) and three-judge consensus, and over-generation with discarding of corrected questions [35].

**Used by.** The "BM25 Wins at Scale" study [50]; leaderboard of 35 systems [39].

**Known problems.** (Authors) Synthetic, one company, flattened JSON; LLM artefacts such as timestamps converging on 123456789 and "ACME" names; high-volume documents reference people absent from the directory; the corpus is more internally similar than Onyx's real data, so it behaves like a larger corpus; gold labels are "revisable hypotheses" and a question's gold set may be incomplete [35]. (Independent) The scaling study says questions carry exact lexical anchors and "trap" documents (326 mined traps, 99 lures), which favour exact matching; this is the study's reading [50]. Onyx, the authors, sells a RAG product and excludes itself from the leaderboard [37].

### Benchmark

**What it tests.** Retrieval and answering over company-internal knowledge, including conflicts, completeness and absence [35].

**Tasks, metrics and protocol.** Per question: correctness (binary, lenient judge), completeness (fraction of atomic facts present), document recall (Recall@10 by default), invalid extra documents (count). Leaderboard ranks by the mean of correctness times completeness. GPT-5.4 (medium reasoning) is generator and judge in the paper. The gold set is fixed per release so scores stay comparable [35][36].

**Datasets.** The corpus and 500 questions above.

**Results.** Paper baselines (top-10 documents, GPT-5.4) [35]:

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| BM25 (OpenSearch) | correctness 68.8, completeness 56.0, recall 68.4, invalid extra 9.0 | percent | benchmark authors (Onyx) | yes | v2 20260519 | [35] |
| Vector (text-embedding-3-large) | 51.4, 42.9, 46.0, 9.3 | same | same | yes | same | [35] |
| Bash agent (GPT-5.4, low reasoning) | 60.6, 61.1, 55.8, 2.0 | same | same | yes | same | [35] |

Independent scaling study (Wang et al., USTC and Metastone; Qwen3.6-27B reader, top-5, official combined score; 500 questions; 28 nested corpus tiers) [50]:

| System | Combined score by corpus size | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|
| BM25 | 74.7 at 1,144 docs; 55.2 at 131,876; 50.5 at 511,959 | Wang et al. | independent of Onyx | v3 20260731 | [50] |
| File-system agent | 77.4 at 1,144; 50.9 at 131,876; 30.7 full | same | independent | same | [50] |
| DenseRAG | 58.1; 36.0; 29.9 | same | independent | same | [50] |
| HippoRAG 2 | 66.2 at 1,144; 41.0 at 131,876; no build beyond | same | independent | same | [50] |
| LinearRAG | 46.2; 29.8 | same | independent | same | [50] |
| MS-GraphRAG | 45.9 at 1,144; no build beyond 8,750 docs | same | independent | same | [50] |
| LightRAG | 48.0 at 1,144; no build beyond 2,254 docs | same | independent | same | [50] |

Live leaderboard (Hugging Face space, "Total systems: 35 | Last Update: 26 October 2026", read 20261102 19:59). Ranking by Overall Score; submitters are named on the page; the page does not say who ran each system or when; entries must be reproducible (open source guide or a closed sandbox) per the README; first-party for each submitter, and for the third-party products (OpenAI File Search, Azure AI Search, Vertex AI Search, Amazon Q Kendra, LangChain, LlamaIndex defaults) who ran them is **unstated** [39][37].

| System | Overall | Correctness | Completeness | Recall | Invalid extra docs | Source |
|---|---|---|---|---|---|---|
| codos.ai | 92.64 | 94.4 | 95.16 | 96.45 | 0.62 | [39] |
| Flexor.ai (+ GPT-6.1 Sol) | 91.48 | 93.0 | 94.37 | 93.62 | 0.52 | [39] |
| CDL (Causal Dynamics Lab) | 90.91 | 92.4 | 94.37 | 93.13 | 0.24 | [39] |
| Mixedbread (+ Opus 5) | 86.58 | 89.8 | 90.62 | 94.28 | 0.39 | [39] |
| Minimal RAG | 75.92 | 86.0 | 79.99 | 85.51 | 0.43 | [39] |
| OpenAI File Search | 61.03 | 69.8 | 67.87 | 71.65 | 15.7 | [39] |
| Amazon Q (Kendra) | 48.96 | 55.4 | 60.65 | 70.38 | 1.49 | [39] |
| Azure AI Search | 48.42 | 56.4 | 57.63 | 64.25 | 3.25 | [39] |
| LlamaIndex (default configs) | 27.2 | 32.4 | 37.76 | 30.56 | 1.49 | [39] |
| Open WebUI + Chroma | 24.89 | 32.4 | 35.86 | 43.23 | 2.62 | [39] |

Reading (labelled): the paper's three baselines are not on the leaderboard under those names, so leaderboard scores cannot be compared with the paper's baseline table without re-running; the top three scores are above 90, which suggests the question set is near saturation for tuned systems (my inference from the spread, 24.89 to 92.64) [39].

**Known problems.** See dataset. The three document counts differ [35][36][50]. The scaling study's reader and judge differ from the paper's, so scores differ [50].

**Used by.** See dataset.

---

## 10. RAGSearch (`ragsearch`), benchmark only

No data of its own. It re-uses six QA datasets (NQ, PopQA, TriviaQA; HotpotQA, 2WikiMultiHopQA, MuSiQue) in the form used by Search-R1 and FlashRAG (full dev/test sets) and builds the GraphRAG indexes from each question's context [40]. Dataset-page slug not needed; link the benchmark page to `hotpotqa` and to the underlying sets.

### Benchmark

**What it tests.** Whether agentic multi-round search removes the need for an offline-built graph [40].

**Tasks, metrics and protocol.** One dense-RAG backend and five GraphRAG backends (GraphRAG, RAPTOR, HippoRAG2, HyperGraphRAG, LinearRAG) under three inference modes: single-shot, training-free agentic (Search-o1, GraphSearch), RL-based (Search-R1 versus Graph-R1). Backbone Qwen2.5-7B (training-free also 32B; RL 3B and 7B); graph building with GPT-4o-mini; RL trained on HotpotQA and NQ (5,000 samples), with the other four sets cross-domain. Metrics Contain Exact Match and F1; offline construction cost and online cost also reported [40].

**Datasets.** NQ (3,610 test), PopQA (14,267), TriviaQA (11,313), HotpotQA (dev 7,405), 2Wiki, MuSiQue [40].

**Results.** Table 1, Contain EM, Qwen2.5-7B; "best GraphRAG" means the best of five variants per cell [40]:

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Single-shot, dense | HotpotQA 19.00, 2Wiki 35.53, MuSiQue 20.99 | Contain EM | RAGSearch authors (NYU Shanghai) | yes | v1 20260401 | [40] |
| Single-shot, best GraphRAG | 46.70, 62.56, 47.95 (gap about +27.7, +27.0, +27.0) | same | same | yes | same | [40] |
| Single-shot, general QA (NQ / PopQA / TriviaQA) dense vs best GraphRAG | 46.62 vs 48.31; 32.14 vs 32.82; 58.60 vs 57.65 | same | same | yes | same | [40] |
| GraphSearch agent, dense | 38.22 HotpotQA, 47.43 2Wiki, 13.33 MuSiQue | same | same | yes | same | [40] |
| GraphSearch agent, best GraphRAG | 58.64, 79.88, 55.26 | same | same | yes | same | [40] |
| Search-R1-7B | 35.76, 33.56, 14.42 | same | same | yes | same | [40] |
| Graph-R1-7B | 53.42, 66.25, 40.82 | same | same | yes | same | [40] |

The paper reports an average multi-hop gap of +27.23 in single-shot (and +26.59 for the training-free GraphSearch comparison) [40].

**Known problems.** The comparison mixes knowledge sources: the dense backend retrieves from the 2018 Wikipedia dump, while all GraphRAG backends use each question's own context as the document ("we utilize the context of each question as the document", Appendix) [40]. How much of the gap this explains is **unstated** in the paper. The GraphRAG figure is the best of five variants against one dense baseline [40]. The repository README (installation and run commands only; no licence file; GitHub API licence null) does not cite the paper id [41]. The page footnotes carry unfilled ACM template text ("Conference: Make sure to enter the correct conference title"), so the venue is **unstated** [40].

**Used by.** Three archive pages [55]. Independent replication: none found.

---

## 11. MultiHop-RAG (`multihop-rag`), both

### Dataset

**What it contains.** A knowledge base of 609 English news articles (mediastack API, 26 September to 25 December 2023 in the corpus file; average 2,046 tokens; categories technology 172, sports 211, entertainment 114, business 81, science 21, health 10) and 2,556 multi-hop queries with answers and evidence lists (comparison 856, inference 816, temporal 583, null 301) [42][45]. Evidence counts in the released file: 2 documents 1,079, 3 documents 778, 4 documents 398, none 301 (my count, 20261102 19:54); the paper's Table 4 gives 1,078, 779, 398 [42][45].

**Size and versions.** Paper v1 20240127 (COLM 2024 per the README); repository last push 20260916 [42][43]. Whether the data files changed since v1 is **unstated**; the one-item difference in the evidence counts hints that they did [42][45].

**Licence.** README: "MultiHop-RAG is licensed under ODC-BY"; Hugging Face card `license: odc-by` [43][44]. The repository has no LICENSE file (GitHub API licence null) [43]. The news text comes from publishers whose own terms were not checked here; the Pinakes benchmark page says the same [54].

**How it was made.** News articles of at least 1,024 tokens; a fact-or-opinion classifier extracted evidence; GPT-4 paraphrased evidence into claims with bridge entities and topics (checked with UniEval); claims sharing a bridge (2 to 4 claims) were turned into queries by GPT-4 per query type; null queries were made with non-existent entities and fictional sources; quality was checked by manual review of a sample and by GPT-4 against four criteria [42].

**Used by.** Han et al. (RAG vs GraphRAG) [49]; Pinakes datasets benchmark (owner's own run) [54]; GraphRAG-Bench (Xiang) as a comparison corpus [24]; FRAMES's comparison table [18]; ten archive pages [55].

**Known problems.** The authors: answers limited to yes/no, entity names or before/after; at most four evidence items; only a basic RAG framework tested [42]. Queries and answers are GPT-4 generated and were not fully verified; the 301 null queries are worded differently from answerable ones (144 of 301 mention a "letter" against 0 of the answerable; 184 of 301 contain "Considering the information" against 2; 211 of 301 name no news outlet against 14), per the Pinakes README as read by the archive; I did not re-count those [54]. Entity-graph density of the corpus is low (average degree 0.76) per Xiang et al. [24].

### Benchmark

**What it tests.** Retrieval and reasoning over several documents for four query types, including refusing when evidence is missing [42].

**Tasks, metrics and protocol.** Retrieval: MAP@K, MRR@K, Hit@K on the evidence (null queries excluded), chunks of 256 tokens, LlamaIndex, with and without bge-reranker-large. Generation: accuracy against the short gold answer. Two settings: retrieved chunks (top-6, under 2,048 tokens) and ground-truth chunks [42].

**Datasets.** The 609-article base and 2,556 queries.

**Results.**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| voyage-02 + bge-reranker-large | Hits@10 0.7467; Hits@4 0.6625 (best retrieval) | retrieval | benchmark authors | yes | v1 20240127 | [42] |
| GPT-4, retrieved chunks / ground-truth chunks | 0.56 / 0.89 | accuracy | same | yes | same | [42] |
| Claude-2.1 | 0.52 / 0.56 | accuracy | same | yes | same | [42] |
| Llama-2-70b-chat | 0.28 / 0.32 | accuracy | same | yes | same | [42] |
| RAG (Llama 3.1-8B generator, 256-token chunks, top-10) | overall 67.02; null 96.01 | accuracy | Han et al. (MSU, Oregon, UTA, Meta, IBM) | independent | v3 20260304 | [49] |
| HippoRAG2 (8B) | overall 70.27 | accuracy | Han et al. | independent (own method not theirs) | same | [49] |
| Community-GraphRAG Local (8B) | overall 69.01; null 80.07 | accuracy | Han et al. | independent | same | [49] |
| Community-GraphRAG Global (8B) | overall 64.40; null 19.27 | accuracy | Han et al. | independent | same | [49] |
| RAG (70B) | 65.77 | accuracy | Han et al. | independent | same | [49] |
| Community-GraphRAG Local, graph built by GPT-4o-mini / GPT-4o (70B) | 71.17 / 75.08 | accuracy | Han et al. | independent | same | [49] |
| Pinakes 0.32.8, free search | every gold article in first 8 passages: 43.4% of 2,255 answerable questions | custom retrieval measure | Pinakes owner (the project owner of this documentation) | first-party for Pinakes, independent of MultiHop-RAG's authors | 20261031 | [54] |

Han et al. use the full 2,556 queries and show that 13.6% of queries only GraphRAG answered correctly against 11.6% only RAG (from the archive; not re-counted) [49][53]. On the temporal type RAG scores 30.70 against 50.60 for Community-GraphRAG Local (8B) [49].

**Known problems.** As in dataset; generation accuracy mixes retrieval and reasoning unless the ground-truth setting is used [42]. Null-query difficulty is inflated by wording tells (above) [54].

**Used by.** See dataset.

---

## 12. HotpotQA (`hotpotqa`), both

### Dataset

**What it contains.** 112,779 Wikipedia-based question-answer pairs that need two supporting paragraphs, each with sentence-level supporting facts, plus a new type of factoid comparison questions [46]. Splits: train-easy 18,089 (single-hop), train-medium 56,814, train-hard 15,661, dev 7,405, test-distractor 7,405, test-fullwiki 7,405 [46]. Two settings: distractor (2 gold + 8 bigram-TF-IDF distractor paragraphs) and fullwiki (first paragraphs of all Wikipedia articles) [46]. A processed Wikipedia is released as the fullwiki corpus [47].

**Size and versions.** Paper v1 20180925 (EMNLP 2018) [46]. BEIR re-uses it with 5,233,329 corpus passages and 7,405 test queries [6]. KILT re-uses the fullwiki setting [1].

**Licence.** The dataset page: "HotpotQA is distributed under a CC BY-SA 4.0 License"; the processed Wikipedia is also CC BY-SA 4.0; Hugging Face card says the same [47][48]. The code repository `hotpotqa/hotpot` is Apache-2.0 [56].

**How it was made.** Amazon Mechanical Turk workers wrote questions over pairs of Wikipedia paragraphs: 75% from a hyperlink edge between two articles, 25% comparison questions over two entities sampled from curated Wikipedia lists (half of them yes/no); workers also marked the supporting sentences. Splits by difficulty: train-easy holds mostly single-hop examples from the top contributors; a baseline model trained by three-fold cross-validation answered 60% of the rest with high confidence (train-medium); the remaining "hard" examples were split into train-hard, dev, test-distractor and test-fullwiki [46].

**Used by.** KILT, BEIR, RAGSearch, Han et al., GraphRAG-Bench comparison tables and 13 archive pages [1][6][24][40][49][55].

**Known problems.** Authors: train-medium has a different mix of reasoning types than the hard splits [46]. Other studies in the pool: HotpotQA corpora have low entity-graph density (average degree 0.65) and mostly short fact questions (78.2% classified as fact retrieval), which gives graph methods little to use [24]; only 65.8% of answer entities appear in the KG built by one pipeline [49 via the archive page, not re-checked] [53]. Wikipedia is in LLM training data; contamination control is **unstated** (the authors of MultiHop-RAG make the same point) [42].

### Benchmark

**What it tests.** Multi-hop reasoning and explainability: answer plus the supporting facts [46].

**Tasks, metrics and protocol.** Answer EM and F1, supporting-fact EM and F1, and joint EM and F1, in distractor and fullwiki settings [46][47].

**Datasets.** HotpotQA dev/test; fullwiki Wikipedia [46][47].

**Results.**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Baseline model, distractor test | answer EM 45.46 / F1 58.99; support EM 22.24 / F1 66.62; joint EM 12.04 / F1 41.37 | EM / F1 | HotpotQA authors | yes | paper v1 20180925 | [46] |
| Baseline model, fullwiki test | answer EM 25.23 / F1 34.40; joint F1 17.85 | EM / F1 | same | yes | same | [46] |
| Beam Retrieval (BUPT and Tencent), distractor leaderboard rank 1 | answer EM 72.69 / F1 85.04; support EM 66.25 / F1 90.09; joint EM 50.53 / F1 77.54 | EM / F1 | submitters, on the official leaderboard | self-reported by submitters, scored by the maintainers' evaluation (maintainer verification of each row: unstated) | 20230807 | [47] |
| AISO (ICT, CAS), fullwiki leaderboard rank 1 | answer EM 67.46 / F1 80.52; support EM 61.17 / F1 86.02; joint EM 44.87 / F1 72.00 | same | submitters | self-reported | 20210510 | [47] |
| Chain-of-Skills, fullwiki rank 2 | answer EM 67.38 / F1 80.14; joint EM 45.65 | same | CMU, Microsoft, UIUC | self-reported | 20230131 | [47] |
| RAG with Llama 3.1-8B, 1,000 hard bridge questions | F1 60.04 | F1 | Han et al. | independent | v3 20260304 | [49] |
| HippoRAG2 (same setting) | F1 63.01 | F1 | Han et al. | independent | same | [49] |
| Community-GraphRAG Local (same setting) | F1 61.66 | F1 | Han et al. | independent | same | [49] |
| Search-R1-7B / Graph-R1-7B | Contain EM 35.76 / 53.42 | Contain EM | RAGSearch authors | independent of HotpotQA authors; Graph-R1 is another team's method | 20260401 | [40] |
| BM25 (zero-shot, BEIR setting) | nDCG@10 0.603; BM25 + cross-encoder 0.707 | nDCG@10 | BEIR authors | independent | 20211021 | [6] |

The leaderboards are separate for the distractor and fullwiki settings, ranked by the page's order (not by one metric) [47].

**Known problems.** As in dataset; the leaderboard's last distractor entry is dated 20230807, so the field has moved to other sets [47]. The numbers of different studies use different metrics (EM/F1, Contain EM, nDCG), so they cannot be put in one column [6][40][46][49].

**Used by.** See dataset.

---

## Cross-item notes for the chapter landing writers

1. The pool has two groups: retrieval benchmarks that predate the LLM era (KILT, BEIR, HotpotQA) and RAG or GraphRAG benchmarks from 2024 to 2026 (the others). Two benchmarks (EnterpriseRAG-Bench, GraphRAG-Bench Xiang) keep live leaderboards with later self-submitted rows; two (KILT, BEIR) have EvalAI leaderboards that could not be read; STaRK's leaderboard space was unavailable (HTTP 503) [57][59].
2. Licences that block reuse of data: CRAG (CC BY-NC 4.0), GraphRAG-Bench Xiao (academic only, no redistribution), BEIR (mixed, some GPL/NC/copyright parts). Treat these as read-only references [13][30][6].
3. Counts that disagree between sources, to flag on the pages: WildGraphBench 1,100 against 1,197; GraphRAG-Bench Xiang 4,076 against 4,072; EnterpriseRAG-Bench 511,962 / 511,959 / 511,957; MultiHop-RAG evidence counts 1,078 / 779 against 1,079 / 778 [32][26][35][36][50][42][45].
4. A correction to the archive page `kb-kg/papers-benchmarks/README.md`: the question count of GraphRAG-Bench Xiao (1,018) and its corpus (20 textbooks, 7 million words) are stated in the paper; the archive said "unstated". Its Table-9 and Table-17 numbers for Xiang et al. correspond to Tables 2 and 12 in the current v3 HTML; the Table 12 problem is confirmed [24][53].
5. Independence: the "BM25 Wins at Scale" study and WildGraphBench share first author and affiliations (USTC, Metastone), so use that study as independent only for EnterpriseRAG-Bench [50][32].

## Sources

Read times are UTC on 20261102. Where one fetch script served several sources, the time shown is the script's start clock; the batch ended within the minute or the next.

1. https://arxiv.org/html/2009.02252 : KILT paper v4 full text (tasks, sizes, metrics, Tables 1 to 5, annotation campaign) (read 20261102 19:48 UTC)
2. https://raw.githubusercontent.com/facebookresearch/KILT/main/README.md : knowledge source file size and snapshot date, "KILT is MIT licensed" (read 20261102 19:50 UTC)
3. https://raw.githubusercontent.com/facebookresearch/KILT/main/LICENSE : MIT text (read 20261102 19:50 UTC)
4. https://huggingface.co/datasets/facebook/kilt_tasks/raw/main/README.md and https://huggingface.co/datasets/facebook/kilt_wikipedia/raw/main/README.md : card header `license: mit`, licensing section "Needs More Information" (read 20261102 19:50 UTC)
5. https://api.github.com/repos/facebookresearch/KILT : archived true, last push 20220331, MIT (read 20261102 19:49 UTC)
6. https://arxiv.org/html/2104.08663 : BEIR paper v4 full text (datasets, Table 1, Table 2, Appendix E licences) (read 20261102 19:48 UTC)
7. https://raw.githubusercontent.com/beir-cellar/beir/main/README.md : dataset table with non-downloadable sets, disclaimer, leaderboard link (read 20261102 19:50 UTC)
8. https://huggingface.co/datasets/BeIR/beir/raw/main/README.md : card `license: cc-by-sa-4.0` (read 20261102 19:50 UTC)
9. https://api.github.com/repos/beir-cellar/beir : Apache-2.0, last push 20251016 (read 20261102 19:49 UTC)
10. https://arxiv.org/abs/2306.07471 : "Resources for Brewing BEIR" abstract (read 20261102 20:02 UTC)
11. https://github.com/beir-cellar/beir/wiki/Leaderboard : leaderboard on EvalAI, wiki last edited 20230110 (read 20261102 20:02 UTC)
12. https://arxiv.org/html/2406.04744 : CRAG paper v2 full text (read 20261102 19:48 UTC)
13. https://raw.githubusercontent.com/facebookresearch/CRAG/main/README.md and https://raw.githubusercontent.com/facebookresearch/CRAG/main/LICENSE : scoring, CC BY-NC 4.0 (read 20261102 19:50 UTC; LICENSE re-read 19:52)
14. https://raw.githubusercontent.com/facebookresearch/CRAG/main/docs/dataset.md and the commits API : dev_v4 files, last commits June 2025 (read 20261102 19:52 UTC)
15. https://api.github.com/repos/facebookresearch/CRAG : licence "Other", last push 20250614 (read 20261102 19:49 UTC)
16. https://arxiv.org/abs/2410.00005 : Winning Solution For Meta KDD Cup' 24, abstract with scores (read 20261102 20:02 UTC)
17. https://www.aicrowd.com/challenges/meta-comprehensive-rag-benchmark-kdd-cup-2024/winners : podium per task, no scores (read 20261102 20:02 UTC)
18. https://arxiv.org/html/2409.12941 : FRAMES paper v3 full text (read 20261102 19:48 UTC)
19. https://huggingface.co/datasets/google/frames-benchmark/raw/main/README.md : card, apache-2.0, baselines (read 20261102 19:50 UTC)
20. https://arxiv.org/html/2404.13207 : STaRK paper v3 full text (read 20261102 19:48 UTC)
21. https://huggingface.co/datasets/snap-stanford/stark/raw/main/README.md : card `cc-by-4.0` (read 20261102 19:50 UTC)
22. https://raw.githubusercontent.com/snap-stanford/stark/main/README.md : news items, MIT badge, leaderboard link (read 20261102 19:50 UTC)
23. https://api.github.com/repos/snap-stanford/stark : MIT, last push 20260206 (read 20261102 19:49 UTC)
24. https://arxiv.org/html/2506.05690 : GraphRAG-Bench (Xiang et al.) v3 full text (read 20261102 19:48 UTC)
25. https://raw.githubusercontent.com/GraphRAG-Bench/GraphRAG-Benchmark/main/README.md and LICENSE : MIT, leaderboards (read 20261102 19:50 UTC)
26. https://huggingface.co/datasets/GraphRAG-Bench/GraphRAG-Bench (card, API, `novel_questions.json`, `medical_questions.json`) : no licence field, last modified 20250713, question counts (read 20261102 19:53 to 19:54 UTC)
27. https://graphrag-bench.github.io/story_data.csv and medical_data.csv, and the leaderboard repository commits : live leaderboard rows (read 20261102 19:59 UTC)
28. https://arxiv.org/html/2506.02404 : GraphRAG-Bench (Xiao et al.) v3 full text (read 20261102 19:48 UTC)
29. https://raw.githubusercontent.com/jeremycp3/GraphRAG-Bench/main/README.md and repository API : no licence file, last push 20250801 (read 20261102 19:58 UTC)
30. https://huggingface.co/datasets/jeremycp3/GraphRAG-Bench/raw/main/README.md : academic-only licence text (read 20261102 19:58 UTC)
31. https://deep-polyu.github.io/RAG/ : official leaderboard, 12 rows (read 20261102 19:58 UTC)
32. https://arxiv.org/html/2602.02053 : WildGraphBench v2 full text (read 20261102 19:48 UTC)
33. https://raw.githubusercontent.com/BstWPY/WildGraphBench/main/README.md and LICENSE : Apache-2.0, 1,197 questions, per-domain table (read 20261102 19:50 UTC)
34. https://huggingface.co/api/datasets/Bstwpy/WildGraphBench and https://api.github.com/repos/BstWPY/WildGraphBench : `license:apache-2.0`, dates (read 20261102 19:53 UTC; GitHub API 19:49)
35. https://arxiv.org/html/2605.05253 : EnterpriseRAG-Bench v2 full text (read 20261102 19:48 UTC)
36. https://huggingface.co/datasets/onyx-dot-app/EnterpriseRAG-Bench/raw/main/README.md : card, per-source counts, metric definition (read 20261102 19:50 UTC)
37. https://raw.githubusercontent.com/onyx-dot-app/EnterpriseRAG-Bench/main/README.md and LICENSE; https://api.github.com/repos/onyx-dot-app/EnterpriseRAG-Bench : MIT, extra 100 questions, leaderboard rules (read 20261102 19:50 UTC; API 19:49)
38. https://huggingface.co/api/datasets/onyx-dot-app/EnterpriseRAG-Bench : `license:mit`, last modified 20260508 (read 20261102 19:53 UTC)
39. https://onyx-dot-app-enterpriserag-bench-leaderboard.hf.space/ and https://huggingface.co/api/spaces/onyx-dot-app/EnterpriseRAG-Bench-Leaderboard : 35 systems, last update 26 October 2026 (read 20261102 19:59 UTC)
40. https://arxiv.org/html/2604.09666 : RAGSearch v1 full text (read 20261102 19:48 UTC)
41. https://raw.githubusercontent.com/FanDongzhe123/RAGSearch/main/README.md and repository API : install and run steps only, licence null (read 20261102 19:50 UTC; API 19:49)
42. https://arxiv.org/html/2401.15391 : MultiHop-RAG v1 full text (read 20261102 19:48 UTC)
43. https://raw.githubusercontent.com/yixuantt/MultiHop-RAG/main/README.md and repository API : ODC-BY statement, no LICENSE file (read 20261102 19:50 UTC; API 19:49)
44. https://huggingface.co/datasets/yixuantt/MultiHopRAG/raw/main/README.md : `license: odc-by` (read 20261102 19:50 UTC)
45. https://huggingface.co/datasets/yixuantt/MultiHopRAG/resolve/main/MultiHopRAG.json and corpus.json : my counts of query types, evidence lengths, corpus categories and dates (read 20261102 19:54 UTC)
46. https://arxiv.org/html/1809.09600 : HotpotQA paper v1 full text (read 20261102 19:48 UTC)
47. https://hotpotqa.github.io/ : licence, leaderboards (distractor and fullwiki) (read 20261102 19:50 UTC)
48. https://huggingface.co/datasets/hotpotqa/hotpot_qa/raw/main/README.md : card, CC BY-SA 4.0 (read 20261102 19:50 UTC)
49. https://arxiv.org/html/2502.11371 : Han et al., RAG vs. GraphRAG, v3 full text (Tables 1, 2, 5, 9) (read 20261102 19:55 UTC)
50. https://arxiv.org/html/2607.26497 : Wang et al., BM25 Wins at Scale, v3 (Table 1, Table 2, setup) (read 20261102 19:55 UTC)
51. https://arxiv.org/html/2606.25656 : Chen et al., Is GraphRAG Needed?, v1 (Table 1, setup) (read 20261102 19:55 UTC)
52. https://api.semanticscholar.org/graph/v1/paper/batch (citationCount for the twelve arXiv ids) (read 20261102 20:01 UTC; four single calls earlier at 19:48 to 19:57 agreed: KILT 939, FRAMES 211, Xiang 60, MultiHop-RAG 353)
53. Archive page `kb-kg/papers-benchmarks/README.md` and `kb-kg/literature/graph-rag-research.md`, used as leads and re-checked against the primary sources above (read 20261102 19:47 UTC)
54. Archive page `pinakes/experiments/datasets-benchmark.md`, which quotes the Pinakes datasets-benchmark README as read 20261102 08:54 UTC (its figures are the owner's; not re-run here; read 20261102 19:47 UTC)
55. Grep of `kb-kg/`, `pinakes/` and root documents for each name (usage evidence) (run 20261102 20:01 UTC)
56. https://api.github.com/repos/hotpotqa/hotpot : Apache-2.0, last push 20210426 (read 20261102 19:49 UTC)
57. https://eval.ai/web/challenges/challenge-page/689/leaderboard through a page-reading tool : no data returned, so KILT leaderboard rows not read (read 20261102 20:01 UTC)
58. Web search for FRAMES independent results (leads only; no source adopted) (run 20261102 20:01 UTC)
59. https://snap-stanford-stark-leaderboard.hf.space/ : HTTP 503 twice (20:00, 20:01); https://huggingface.co/api/spaces/snap-stanford/stark-leaderboard confirms the space exists, last modified 20260909 (read 20261102 19:59 UTC)

Not verified in this run: KILT and BEIR EvalAI leaderboard rows; STaRK leaderboard rows; whether the CRAG KDD Cup score scale equals truthfulness; the 13.6% / 11.6% unique-win figures and the 65.8% entity coverage (quoted from the archive, marked as such); whether the GraphRAG-Bench (Xiang) Hugging Face files predate paper v3; Hugging Face Hub dataset card for FRAMES licence beyond the header; the SIGIR 2024 BEIR resource paper's numbers.
