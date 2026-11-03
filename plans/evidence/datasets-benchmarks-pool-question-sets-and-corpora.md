# Candidate pool: question sets and text corpora (datasets and benchmarks)

Researcher file for the datasets and benchmarks chapters. Written 20261102 (UTC), by the researcher for the area "question sets and text corpora". Sources are numbered `[n]` and listed at the end with read times. Clock readings: 19:46 to 20:19 UTC on 20261102.

**How to read this file**

- One section per item. Each states its role (dataset, benchmark or both), the slug, the dataset kinds (`kg`, `questions`, `corpus`) and then every template field of its role(s).
- "unstated" means the sources read say nothing. It is never a guess.
- Licence: a repository `LICENSE` file covers the repository's code unless the file or README says it covers the data. Where a data licence comes only from a Hugging Face dataset card, that is said. Several datasets have no data licence statement from their authors that I could read.
- Results tables: "first-party" = run by the authors of the dataset, the benchmark or the method being scored. Nothing here is a re-run by me.
- Citation counts: OpenAlex `cited_by_count` (read 20261102 20:03 to 20:04 UTC) and Semantic Scholar `citationCount` where the API answered (it returned HTTP 429 for most calls; see the table near the end). The two services count different record sets, so the numbers are not comparable across rows. A DOI of the published version and the arXiv DOI are different OpenAlex records.
- Archive pages ("used by in the archive") come from a text search of `kb-kg/`, `pinakes/`, `DECISIONS.md`, `RESUME.md`, `README.md` on 20261102 about 20:00 UTC; it lists at most 14 files per name. Landscape snapshot files (`kb-kg/landscape/*`) match only because repository descriptions contain the name; they are not counted as evidence of use.
- Lead pages: `kb-kg/papers-benchmarks/README.md` sections 3 to 5 and `pinakes/experiments/datasets-benchmark.md` were read in full and every number I reuse was re-checked against the primary paper. `kb-kg/literature/graph-rag-research.md` was **not** read in this pass.

---

## 1. Natural Questions

- Slug: `natural-questions`. Role: **both**. Kinds: `questions`, `corpus` (annotated Wikipedia pages).

### Dataset

**What it contains.** Real, anonymised, aggregated queries issued to Google search, filtered by simple heuristics so that they read as questions; each is paired with a Wikipedia page from the top five search results, and an annotator marks a long answer (typically a paragraph), a short answer (one or more entities) if present, or null [7]. Each example holds the rendered HTML of the whole page plus a token list, long-answer candidates and annotations (`long_answer`, `short_answers`, `yes_no_answer`) [28].

**Size and versions.** 307,373 training examples with a single annotation, 7,830 development examples and 7,842 test examples, the last two with 5-way annotation [7]. The repository README states "307,372" in one sentence and "307,373" in another [28]. Of the training set, 152,148 have a long answer, 110,724 a short answer (106,926 span sets, 3,798 yes/no) [28]. A simplified training file (text already extracted) exists [28]. The test set is sequestered: evaluation needs a Docker image uploaded to the competition site [28]. Wikipedia snapshot date of the pages: **unstated** in the sources read.

**Licence.** Dataset: CC BY-SA 3.0 per the Hugging Face card [29]; the official data page did not render in my fetch (it returned only "Loading...") [60]. The GitHub `LICENSE` is Apache-2.0 and covers the repository code; the README contains no data licence [28].

**How it was made.** Queries sampled from the search stream with heuristics that discard non-questions and keep queries of 8 words or more that are questions; query plus the Wikipedia page from the top 5 results go to a human annotation task [7]. Evaluation data is annotated five times, which the authors justify in the paper's Section 5 [7]. The paper reports a human upper bound of 87.2 F1 (long answer) and 75.7 F1 (short answer) from a "super-annotator" [7] (the README rounds to 87% and 76% [28]).

**Used by.** Seed single-hop questions for MuSiQue [5][34]; one of the 11 KILT datasets [16]; trained and tested in DPR [15]; evaluated in Han et al. [22] and RAGSearch [23]; in the archive: `kb-kg/papers-benchmarks/README.md`, `kb-kg/projects/hipporag.md`, `graph-r1.md`, `minirag.md`, `openviking.md`, `pinakes/takeaways/hipporag.md` [55].

**Known problems.**
- Annotators disagree: the paper introduces 5-way annotation and metrics tolerant of it because a single annotation is noisy [7].
- The PopQA authors found NQ dominated by high-popularity subject entities, with hard-to-identify relation types [2].
- NQ questions reused as MuSiQue seeds may appear in NQ training data; MuSiQue releases the IDs to avoid leakage [34].
- Contamination of LLM pretraining data: **unstated** in the sources read.

### Benchmark

**What it tests.** Reading a whole Wikipedia page to find the smallest passage that answers a real search question, and the short answer inside it [7][28].

**Tasks, metrics and protocol.** Long-answer identification (a paragraph, table, list or row) and short-answer extraction (span set or yes/no); precision, recall and F1 against 5-way annotations on dev and test [7]. Test predictions go through a hidden-test competition site [28]. In the open-domain variant (question only, retrieve from a Wikipedia corpus), systems are scored on retrieval accuracy or exact match; see the results table.

**Datasets.** `natural-questions`; Wikipedia snapshots in `wikipedia-dpr-kilt`.

**Results** (dated by publication; "n/a" = not applicable)

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| DecAtt + DocReader | long answer F1 54.8 (dev) / 55.0 (test); short answer F1 31.4 / 31.5 | P/R/F1, 5-way annotations | NQ authors | yes | 2019 (TACL; exact date unstated) | [7] Table 3 |
| DocumentQA | long answer F1 46.1 / 45.7; short answer F1 35.7 / 35.1 | same | NQ authors | yes | 2019 | [7] Table 3 |
| Single annotator / super-annotator | long 73.4 / 87.2; short 57.5 / 75.7 | F1 | NQ authors | yes | 2019 | [7] Table 3 (human rows are on a sample of the 25-way data) |
| DPR (single-dataset training) vs BM25 | top-20 retrieval accuracy 78.4 vs 59.1 (top-100: 85.4 vs 73.7) | share of questions with an answer string in the top-k passages | DPR authors | first-party for DPR | EMNLP 2020; arXiv v3 20200930 | [15] Table 2 |
| RAG; BART + DPR (KILT NQ test, held-out part) | 44.39; 41.27 | exact match | KILT authors | first-party for KILT (RAG's authors overlap with KILT's) | v4 20210527 | [16] Table 3 |
| Vanilla RAG; Community-GraphRAG (Local); HippoRAG2 | 64.78; 63.01; 61.03 | F1; NQ treated as a single-document QA task with one RAG index per document; number of questions **unstated** in the pages read | Han et al. (neither NQ's nor those methods' authors) | independent | v3 20260304 | [22] Table 1, appendix A.1 |
| Qwen2.5-7B single-shot: dense vs best of five GraphRAG backends | 46.62 vs 48.31 | Contain-EM | Fan et al. (NYU Shanghai) | independent | 20260401 | [23] Table 1 |

**Known problems (benchmark).** The hidden test needs an uploaded container [28]. Retrieval-accuracy numbers (DPR) measure whether the answer string occurs in the passage, not whether it answers [15] (stated definition: "percentage of top 20/100 retrieved passages that contain the answer").

**Usage evidence.** OpenAlex 2,070 (TACL DOI 10.1162/tacl_a_00276, read 20261102 20:03); Semantic Scholar 5,455 (same DOI, read 20261102 20:05) [53][54].

---

## 2. TriviaQA

- Slug: `triviaqa`. Role: **both**. Kinds: `questions`, `corpus` (evidence documents).

### Dataset

**What it contains.** 95,956 question-answer pairs written by trivia enthusiasts (from 14 trivia and quiz-league sites), with 662,659 automatically gathered evidence documents, six per question on average, from Wikipedia pages of entities linked in the question and from Bing web search results [1]. Over 650K question-answer-evidence triples [1].

**Size and versions.** Reading-comprehension version: Wikipedia domain train 61,888 / dev 7,993 / test 7,701 questions; Web domain 76,496 / 9,951 / 9,509 [1]. Verified (human-checked) subsets: Wikipedia dev 297 and test 584, Web dev 322 and test 733 [1]; the introduction describes a clean human-annotated subset of 1,975 question-document-answer triples [1]. The full unfiltered release has 110,495 question-answer pairs and 740K evidence documents [1]; the project page says "110K" for the unfiltered download and lists RC (2.5G) and unfiltered (604M) archives [30].

**Licence.** No licence is stated: the project page says only "The University of Washington does not own the copyright of the questions and documents included in TriviaQA" [30]; the Hugging Face card sets `license: unknown` and repeats that sentence [30]. The GitHub repository named in my lead returned 404, so no code licence was read [30].

**How it was made.** Question-answer pairs scraped from 14 trivia sites; questions under four tokens removed [1]. Evidence: top 50 Bing results per question (trivia sites excluded), top 10 crawled; plus Wikipedia pages for entities found by the TAGME entity linker; evidence documents lacking the answer string were dropped, so the evidence is "distant supervision" [1]. Random split 80% / 10% / 10% [1].

**Used by.** One of the 11 KILT datasets [16]; one of five datasets for DPR [15]; part of the six sets of RAGSearch [23]; in the archive: `kb-kg/papers-benchmarks/README.md`, `kb-kg/projects/graph-r1.md`, `minirag.md` [55].

**Known problems.**
- Distant supervision is noisy: a human annotator found the evidence sufficient for 79.7% (Wikipedia) and 75.4% (Web) of questions [1]; in a 100-error sample of BiDAF, 19 had no evidence in any provided document and 3 had incorrect ground truth [1].
- Questions can contain clues not covered by the documents [1].
- Copyright of questions and documents is not UW's; redistribution rights are **unstated** [30].

### Benchmark

**What it tests.** Reading comprehension over long evidence documents with compositional questions, and (as used later) open-domain QA [1][15].

**Tasks, metrics and protocol.** Exact match and F1 as in SQuAD; Wikipedia domain scored per question, Web domain per document; extra scores on the verified subsets [1]. Test evaluation through a CodaLab leaderboard [30].

**Datasets.** `triviaqa`; Wikipedia snapshot for open-domain use (`wikipedia-dpr-kilt`).

**Results**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| BiDAF (Wikipedia domain) | 40.32 EM / 45.91 F1 test; human 79.7% | EM, F1 | TriviaQA authors | yes | 20170513 (v2) | [1] Tables 7, text |
| Entity classifier (Wikipedia) | 22.45 EM / 26.52 F1 test | EM, F1 | TriviaQA authors | yes | 20170513 | [1] Table 7 |
| DPR single vs BM25 | 79.4 vs 66.9 (top-20 retrieval accuracy) | retrieval accuracy | DPR authors | first-party for DPR | v3 20200930 | [15] Table 2 |
| RAG; BART + DPR (KILT TQA) | 71.27; 58.55 | exact match | KILT authors | first-party | 20210527 | [16] Table 3 |
| Qwen2.5-7B single-shot dense vs best GraphRAG | 58.60 vs 57.65 (lower) | Contain-EM | Fan et al. | independent | 20260401 | [23] Table 1 |

**Known problems (benchmark).** Verified subsets are small (a few hundred questions) [1]. Whether a score gap reflects retrieval or reading cannot be told from EM alone (the paper's own error analysis: paraphrase 29, insufficient evidence 19, multi-sentence reasoning 18 of 100 sampled errors) [1].

**Usage evidence.** OpenAlex 1,651 (ACL DOI 10.18653/v1/p17-1147, 20261102 20:03); Semantic Scholar: 429, no value [53][54].

---

## 3. PopQA

- Slug: `popqa`. Role: **both**. Kinds: `questions`, `kg` (questions are generated from Wikidata triples).

### Dataset

**What it contains.** About 14k entity-centric open-domain questions about long-tail entities. Each carries Wikidata IDs for subject, property and object, answer aliases, the subject's and object's Wikipedia page-view popularity, and a relation type [2][31]. 16 relation types, with 14,267 questions in the aggregate figure of the paper [2].

**Size and versions.** The paper says "14k questions" (abstract) and shows an aggregate n of 14,267 [2]; the Hugging Face viewer lists a single `test` split of 14.3k rows [31]; the authors ran "14,282 questions" through GPT-3 [2] (the three counts differ slightly; I did not reconcile them). Version tags: **unstated**.

**Licence.** No data licence read. The repository `LICENSE` is MIT (Copyright 2023 Alex Mallen) and covers the repository [31]; the Hugging Face card text was not retrievable and the API metadata has no licence field [31].

**How it was made.** Triples of 16 relation types are sampled from Wikidata, with higher weight on popular entities (inclusion test uses the subject alias's term frequency in an 800 MB sample of C4), at most 2,000 triples per relation; each triple is turned into a question with a hand-written template per relation (for example "What is [subj]'s occupation?"); popularity is the number of Wikipedia monthly page views [2].

**Used by.** Adaptive Retrieval in its own paper [2]; RAGSearch (one of six sets) [23]; in the archive: `kb-kg/papers-benchmarks/README.md`, `kb-kg/projects/graph-r1.md`, `hipporag.md`, `pinakes/takeaways/hipporag.md` [55].

**Known problems.**
- Some relation types are guessable without knowing the fact (nationality-like relations; "country" shows high accuracy with no popularity trend) [2].
- Question templates are fixed per relation [2].
- Wikidata and the page-view snapshot are from the paper's date; later drift is **unstated**.
- Contamination: **unstated**.

### Benchmark

**What it tests.** Whether a language model has memorised a fact about an entity of given popularity, and when retrieval helps or hurts [2].

**Tasks, metrics and protocol.** Closed-book and retrieval-augmented open-domain QA; accuracy = any gold alias is a substring of the prediction; 15-shot prompts for GPT-Neo and OPT, zero-shot for GPT-3; retrieval from the December 2018 Wikipedia dump, top-1 passage, with BM25 or Contriever [2].

**Datasets.** `popqa`; Wikipedia dump of December 2018 (`wikipedia-dpr-kilt`).

**Results**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| GPT-3 davinci-003 (vanilla) | 35% overall; 19% on the 4,000 least popular questions | accuracy | PopQA authors | yes | v4 20230702 | [2] |
| GPT-Neo 20B vanilla | 25% overall | accuracy | PopQA authors | yes | v4 | [2] |
| Contriever on top of davinci-003 | +7 points | accuracy | PopQA authors | yes | v4 | [2] |
| Qwen2.5-7B single-shot: dense vs best GraphRAG | 32.14 vs 32.82 | Contain-EM | Fan et al. | independent | 20260401 | [23] Table 1 |

**Known problems (benchmark).** Single-hop only; retrieval hurt 10% of questions where the model was already right (recall@1 of 0.14 on those) [2].

**Usage evidence.** OpenAlex 342 (ACL DOI 10.18653/v1/2023.acl-long.546, 20261102 20:04); Semantic Scholar: not obtained [53][54].

---
## 4. HotpotQA

- Slug: `hotpotqa`. Role: **both**. Kinds: `questions`, `corpus` (Wikipedia paragraphs as context).

### Dataset

**What it contains.** About 113k Wikipedia-based question-answer pairs that need two supporting documents, with the supporting sentences marked ("supporting facts"), a bridge type (an entity links two paragraphs) and a comparison type (two entities compared, including yes/no) [3]. Each example also has a `level` (easy, medium, hard) and a `type` field [32].

**Size and versions.** 112,779 valid examples: train-easy 18,089; train-medium 56,814; train-hard 15,661; dev 7,405; test-distractor 7,405; test-fullwiki 7,405 [3]. Files: train v1.1, dev distractor v1, dev fullwiki v1, test fullwiki v1 (the fullwiki test file holds retrieved context, no answers) [32]. Context: in the distractor setting 2 gold paragraphs plus 8 distractors retrieved with bigram tf-idf; in the fullwiki setting the first paragraphs of all Wikipedia articles (over 5,000,000 paragraphs) [3]. Wikipedia source: dump of 1 October 2017 [3].

**Licence.** CC BY-SA 4.0 for the data and Apache-2.0 for the code, stated in the repository README and on the project page; the Hugging Face card agrees [32]. The repository has no `LICENSE` file at the root (404) [32].

**How it was made.** Crowdsourcing on Amazon Mechanical Turk through ParlAI. A hyperlink graph of first paragraphs of all articles gives paragraph pairs; bridge entities restricted to hand-curated pages (591 categories curated), comparison pairs drawn from 42 curated lists of similar entities; 75% bridge and 25% comparison, half of the comparisons yes/no. Workers also marked supporting facts. To keep dev/test hard, a model separated "train-easy" (single-hop) and "train-medium" (answered correctly with high confidence in 3-fold cross validation) from the hard rest, which was split into train-hard, dev and the two tests [3].

**Used by.** Part of KILT [16]; compared in MuSiQue and 2Wiki papers as the earlier multi-hop set [4][5]; Han et al. (1,000 hard bridge questions from dev) [22]; RAGSearch [23]; Xiang et al. measured its entity-graph density [20]; in the archive: `kb-kg/papers-benchmarks/README.md`, `kb-kg/projects/fast-graphrag.md`, `graph-r1.md`, `hipporag.md`, `linearrag.md`, `logicrag.md`, `memmachine.md`, `openviking.md`, `youtu-graphrag.md`, `pinakes/takeaways/logicrag.md` [55].

**Known problems.**
- Many questions do not need multi-hop reasoning: "single-hop reasoning can solve much more of the dataset than previously thought" (Min et al., 2019) [50]; the MuSiQue and 2Wiki papers repeat this [4][5].
- By the authors' own analysis of dev/test, about 6% of sampled questions are single-hop and 2% unanswerable [3].
- Dev and test contain only the "hard" examples as judged by a 2018 model, so difficulty is relative to that model [3].
- Context is a 2017 Wikipedia snapshot [3]; fullwiki retrieval uses only first paragraphs [3].
- Supporting-fact agreement between crowd workers is lower than answer agreement [3].

### Benchmark

**What it tests.** Multi-document reasoning with explainable evidence [3].

**Tasks, metrics and protocol.** Answer span or yes/no; supporting-fact prediction; two settings: distractor (10 paragraphs given) and fullwiki (retrieve from Wikipedia). Metrics: answer EM and F1, supporting-fact EM and F1, joint EM and F1 (joint F1 uses the product of answer and support precision and recall) [3]. Fullwiki test submissions go to an evaluation server; distractor test requires code in a Docker environment [32].

**Datasets.** `hotpotqa`.

**Results**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Baseline, distractor, test | answer EM 45.46 / F1 58.99; support EM 22.24 / F1 66.62; joint EM 12.04 / F1 41.37 | EM, F1 | HotpotQA authors | yes | 20180925 | [3] Table 4 |
| Baseline, fullwiki, test | answer EM 25.23 / F1 34.40; joint EM 2.63 / F1 17.85 | EM, F1 | HotpotQA authors | yes | 20180925 | [3] Table 4 |
| Human (1,000 sampled examples) | answer EM 83.60 / F1 91.40; joint F1 82.55 | EM, F1 | HotpotQA authors | yes | 20180925 | [3] Table 8 |
| Beam Retrieval, distractor (leaderboard rank 1) | answer EM 72.69 / F1 85.04; support F1 90.09; joint EM 50.53 / F1 77.54 | EM, F1 | BUPT and Tencent (submitter named on the board) | no (external team; board run by the dataset authors) | 20230807 | [32] project page, read 20261102 about 20:02 |
| AISO, fullwiki (leaderboard rank 1) | answer EM 67.46 / F1 80.52; joint F1 72.00 | EM, F1 | Institute of Computing Technology, CAS | no | 20210510 | [32] |
| Vanilla RAG; Community-GraphRAG (Local); HippoRAG2 (Llama-3.1-8B, 1,000 hard bridge questions) | F1 60.04; 61.66; 63.01 | F1 | Han et al. | independent | v3 20260304 | [22] Table 1 |
| Qwen2.5-7B single-shot: dense vs best of five GraphRAG backends | 19.00 vs 46.70 | Contain-EM | Fan et al. | independent (the dense backend retrieves from the 2018 Wikipedia dump, the GraphRAG backends from each question's own context, per the paper's setup text) | 20260401 | [23] Table 1 |
| GraphSearch agent, dense vs best GraphRAG | 38.22 vs 58.64 | Contain-EM | Fan et al. | independent | 20260401 | [23] Table 1 |
| Search-R1 vs Graph-R1 (RL agents) | 35.76 vs 53.42 | Contain-EM | Fan et al. | independent of both methods | 20260401 | [23] Table 1 |

**Known problems (benchmark).** Leaderboard top entries are single systems whose submission protocols differ between distractor and fullwiki [32]. The 8B-versus-70B and sample choices in Han et al. are the authors' [22]. The gap in Fan et al. mixes a retrieval-backend difference (Wikipedia dump versus per-question context) with the GraphRAG effect [23].

**Usage evidence.** OpenAlex 1,807 (ACL DOI 10.18653/v1/d18-1259, 20261102 20:04) and 97 for the arXiv-DOI record, 20:03; Semantic Scholar: not obtained [53][54].

---

## 5. 2WikiMultiHopQA

- Slug: `2wikimultihopqa`. Role: **both**. Kinds: `questions`, `corpus`, `kg` (each question carries Wikidata evidence triples).

### Dataset

**What it contains.** Multi-hop questions over Wikipedia article summaries, built from the intersection of Wikipedia and Wikidata. Each example has the question, answer, context paragraphs, sentence-level supporting facts and an `evidences` list of Wikidata triples (subject, relation, object) giving the reasoning path; later versions add `evidences_id` and `answer_id` [4][33]. Four question types: comparison, inference, compositional, bridge-comparison [4].

**Size and versions.** 192,606 examples: train-medium 154,878; train-hard 12,576; dev 12,576; test 12,576. By type: comparison 57,989; inference 7,478; compositional 86,979; bridge-comparison 40,160 [4]. Source dumps: English Wikipedia of 1 January 2020 and Wikidata of 31 December 2019, 5,950,475 entities [4]. Releases: 8 December 2020 (`evidences_id`, `answer_id`, new evaluation script v1.1); 7 April 2021 (fixed sentence segmentation; `para_with_hyperlink.zip`) [33]. Files are hosted on Dropbox [33].

**Licence.** The repository `LICENSE` is Apache-2.0 [33]. The README states no data licence [33]. The paper is CC BY 4.0, which covers the paper [4]. Data licence: **unstated**.

**How it was made.** Hand-written question templates (comparison templates derived from NER-tagged HotpotQA comparison questions; 799 compositional templates; 62 bridge-comparison templates), combined with Wikidata facts and 28 manually checked logical rules (found with AMIE) for inference questions. Only properties with consistent Wikipedia and Wikidata values are used. A single-hop model splits the data: questions it solves become train-medium; the rest go to train-hard, dev and test. Yes and no answers are balanced; ambiguous cases are discarded. Distractors: 8 (6 for bridge-comparison) via bigram tf-idf [4].

**Used by.** Seed for MuSiQue comparisons [5]; RAGSearch [23]; Xiang et al. (graph density) [20]; in the archive: `kb-kg/papers-benchmarks/README.md`, `kb-kg/projects/graph-r1.md`, `hipporag.md`, `linearrag.md`, `logicrag.md`, `minirag.md`, `youtu-graphrag.md`, `pinakes/takeaways/logicrag.md` [55].

**Known problems.**
- Questions are template-generated; the MuSiQue authors say hand-authored composition rules make it "easy for large language models" and show higher cheatability scores than MuSiQue (DiRe answer 63.4 versus 37.8) [5].
- Inference questions are few (7,478) because the authors keep only relations with a single Wikidata value [4].
- Wikipedia and Wikidata disagree on some properties (for example occupation), so those were checked by hand [4].
- Yes/no is 31.2% of answers [4].
- Entities are the most popular ones (top-50 types for comparison) [4].

### Benchmark

**What it tests.** Multi-hop reasoning with an explicit reasoning path [4].

**Tasks, metrics and protocol.** Answer prediction, sentence-level supporting facts and evidence-triple generation; EM and F1 for each plus joint scores over all three [4]. Test predictions are scored by the authors on request [33].

**Datasets.** `2wikimultihopqa`.

**Results**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Baseline (HotpotQA model) | answer EM 34.14 / F1 40.95; joint F1 26.76 (paper Table 4, with the earlier evaluation); README board: answer EM 36.53 / F1 43.93, joint F1 5.41 | EM, F1 | 2Wiki authors | yes | 20201025 | [4] Table 4; [33] leaderboard |
| Beam Retrieval | answer EM 88.47 / F1 90.87; support F1 98.15 | EM, F1 | external team, listed by the dataset authors | no | 20230802 | [33] leaderboard |
| NA-Reviewer | answer EM 76.73 / F1 81.91; joint F1 65.23 | EM, F1 | external | no | 20211029 | [33] |
| Qwen2.5-7B single-shot: dense vs best GraphRAG | 35.53 vs 62.56 | Contain-EM | Fan et al. | independent | 20260401 | [23] Table 1 |
| GraphSearch agent: dense vs best GraphRAG | 47.43 vs 79.88 | Contain-EM | Fan et al. | independent | 20260401 | [23] Table 1 |
| Search-R1 vs Graph-R1 | 33.56 vs 66.25 | Contain-EM | Fan et al. | independent | 20260401 | [23] Table 1 |

**Known problems (benchmark).** Leaderboard rows in the README mix dates and metric availability (some rows have no evidence metrics, marked x) [33]. The README leaderboard is hand-maintained "contact us" submission, not a live board [33].

**Usage evidence.** OpenAlex 279 (COLING DOI 10.18653/v1/2020.coling-main.580, 20261102 20:04); 2 for the arXiv-DOI record is not read; Semantic Scholar: not obtained [53][54].

---

## 6. MuSiQue

- Slug: `musique`. Role: **both**. Kinds: `questions`, `corpus` (paragraph contexts).

### Dataset

**What it contains.** 2- to 4-hop questions composed from pairs of single-hop questions, each with 20 paragraphs of context (supporting plus distractors), the decomposition into single-hop questions with their answers and supporting paragraphs, and six reasoning-graph shapes. Two variants: MuSiQue-Ans (answerable) and MuSiQue-Full (each answerable question paired with an unanswerable one) [5].

**Size and versions.** MuSiQue-Ans 24,814 questions: train 19,938 (2-hop 14,376; 3-hop 4,387; 4-hop 1,175), dev 2,417, test 2,459. MuSiQue-Full has twice as many [5]. Version tag v1.0 in file names; the release also contains the IDs of the single-hop questions used in dev/test [34].

**Licence.** CC BY 4.0, stated in the README and the repository `LICENSE` [34]. The seed datasets (SQuAD, Natural Questions, MLQA, T-REx, Zero Shot RE) have their own licences, which I did not read [5][34].

**How it was made.** Starts from 2,017K single-hop questions from five Wikipedia-based datasets; model filters keep 760K good ones; composable pairs (answer of one is a named entity in the other) give 12M two-hop candidates, filtered to 3.2M "connected" ones with Longformer-based checks; chains become 2-4 hop DAGs; train/dev/test are split to minimise overlap of questions, answers and paragraphs; 17 qualified MTurk workers wrote the composed questions (about 11K USD); the Full variant adds unanswerable contrasts [5].

**Used by.** Part of RAGSearch's six sets [23]; compared with HotpotQA and 2Wiki in its own paper [5]; Xiang et al. (graph density) [20]; in the archive: `kb-kg/papers-benchmarks/README.md`, `kb-kg/projects/cognee.md`, `graph-r1.md`, `hipporag.md`, `linearrag.md`, `logicrag.md`, `youtu-graphrag.md`, `pinakes/recommendations-r1-r7.md`, `pinakes/takeaways/hipporag.md`, `logicrag.md` [55].

**Known problems.**
- Seed single-hop questions appear in the training data of NQ, SQuAD and others, so a model trained on them may see MuSiQue dev/test sub-questions; the README tells users to exclude those IDs [34].
- Candidate pairs are selected by model filters (Longformer, RoBERTa, UnifiedQA), so the set inherits those models' blind spots; workers pruned 8% of candidate pairs in the composition step [5].
- Wikipedia-only; contamination of pretraining data: **unstated**.

### Benchmark

**What it tests.** Connected multi-step reasoning; it is built to resist shortcuts [5].

**Tasks, metrics and protocol.** Answer F1 and EM plus support-paragraph F1 for Ans; for Full, answer plus sufficiency (An+Sf, Sp+Sf) over pairs [5]. Two leaderboards (Answerable, Full) hosted at leaderboard.allenai.org [34]; the host did not resolve on 20261102 (`ENOTFOUND`), so no leaderboard rows were read.

**Datasets.** `musique`.

**Results**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Human (MuSiQue-Ans) | answer F1 78.0, support F1 93.9 | F1 | MuSiQue authors | yes | v3 20220505 | [5] Table 4 |
| Select-and-Answer (best multihop model, dev) | answer F1 47.3, support F1 72.3 | F1 | MuSiQue authors | yes | 20220505 | [5] Table 4 |
| Select-and-Answer, test | MuSiQue-Ans answer F1 52.3, support 75.2; MuSiQue-Full An+Sf 34.8, Sp+Sf 42.1 | F1 | MuSiQue authors | yes | 20220505 | [5] Table 5 |
| Single-paragraph model (1-Para) | answer F1 32.0 (HotpotQA 64.8) | F1 | MuSiQue authors | yes | 20220505 | [5] Table 4 |
| Qwen2.5-7B single-shot: dense vs best GraphRAG | 20.99 vs 47.95 | Contain-EM | Fan et al. | independent | 20260401 | [23] Table 1 |
| GraphSearch agent: dense vs best GraphRAG | 13.33 vs 55.26 | Contain-EM | Fan et al. | independent | 20260401 | [23] Table 1 |
| Search-R1 vs Graph-R1 | 14.42 vs 40.82 | Contain-EM | Fan et al. | independent | 20260401 | [23] Table 1 |

**Known problems (benchmark).** Leaderboard not reachable in this run; only first-party numbers from the original paper (2020-era models) and one independent study could be read. Fan et al.'s dense-versus-GraphRAG gap mixes knowledge sources (see item 4) [23].

**Usage evidence.** OpenAlex 286 (TACL DOI 10.1162/tacl_a_00475, 20261102 20:04); Semantic Scholar: not obtained [53][54].

---

## 7. MultiHop-RAG

- Slug: `multihop-rag`. Role: **both**. Kinds: `questions`, `corpus` (news articles).

### Dataset

**What it contains.** A knowledge base of 609 English news articles (category, publication date, author, source, URL, body) and 2,556 multi-hop queries with answers and 2-4 evidence passages each, in four types: inference, comparison, temporal and null (unanswerable) [6]. Queries name the news source, so they use document metadata [6].

**Size and versions.** Queries: inference 816; comparison 856; temporal 583; null 301. Evidence per query (paper): 2 documents 1,078; 3 documents 779; 4 documents 398; 301 null [6]. My count of the released file on 20261102 20:11: 2,556 queries, 609 documents, evidence lists of length 2 = 1,079, 3 = 778, 4 = 398, 0 = 301 (one query differs between 2 and 3 documents from the paper's Table 4), 49 distinct sources, publication dates 2023-09-26 to 2023-12-25 [35][6]. Hugging Face data files: `MultiHopRAG.json`, `corpus.json` [35].

**Licence.** ODC-By 1.0 for the dataset, stated in the README and the Hugging Face card; the repository has no `LICENSE` file (404) [35]. The news text belongs to publishers whose own terms were not checked (Pinakes notes the same gap) [57].

**How it was made.** News from the mediastack API between 26 September and 26 December 2023, kept if at least 1,024 tokens; a trained model extracts factual or opinion sentences as evidence; GPT-4 rewrites evidence into claims with a bridge entity and bridge topic; claim sets of 2 to 4 claims go back to GPT-4 to write a query of each type; null queries use fictional entities and sources. Quality control: manual review of a sample and a GPT-4 check against four criteria [6]. The 2023 date range was chosen so articles postdate common LLM cut-offs [6].

**Used by.** Han et al. [22]; the Pinakes datasets benchmark (this project's own harness) [57]; Xiang et al. (graph density) [20]; in the archive: `kb-kg/papers-benchmarks/README.md`, `kb-kg/experiments/x2-index-cost/*`, `kb-kg/projects/minirag.md`, `pinakes/experiments/*` [55].

**Known problems.**
- Queries and answers were generated by GPT-4 and only a sample was reviewed [6]; the Pinakes benchmark note records that its harness did not check them either [57].
- The null queries are written differently from the answerable ones. I re-counted on the released file: "letter" appears in 144 of 301 null queries (47.8%) and in 0 of 2,255 answerable ones; "Considering the information" in 184 null (61.1%) and 2 answerable (0.1%) [35]. This matches the Pinakes note [57].
- Ground-truth answers are restricted to yes/no, entity names or "before/after" [6].
- Only news from three months; publisher rights unclear [6][57].

### Benchmark

**What it tests.** Retrieval and answering across several documents, with metadata and with unanswerable queries [6].

**Tasks, metrics and protocol.** Retrieval: MAP@K, MRR@K, Hit@K against evidence (null queries excluded); generation: accuracy of a final answer, once with retrieved chunks and once with gold evidence. The paper chunks documents at 256 tokens and uses LlamaIndex [6].

**Datasets.** `multihop-rag`.

**Results**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| voyage-02 + bge-reranker-large | Hits@10 0.7467; Hits@4 0.6625; MRR@10 0.586 | retrieval | MultiHop-RAG authors | yes | 20240127 | [6] Table 5 |
| GPT-4 | accuracy 0.56 with retrieved chunks; 0.89 with gold evidence | accuracy | MultiHop-RAG authors | yes | 20240127 | [6] Table 6 |
| Llama-2-70b-chat / Mixtral-8x7B | 0.28 / 0.32 retrieved; 0.32 / 0.36 gold | accuracy | MultiHop-RAG authors | yes | 20240127 | [6] Table 6 |
| Vanilla RAG, Llama-3.1-8B (overall; null) | 67.02; 96.01 | accuracy | Han et al. | independent | v3 20260304 | [22] Table 2 |
| Community-GraphRAG (Local) (overall; null) | 69.01; 80.07 | accuracy | Han et al. | independent | 20260304 | [22] Table 2 |
| Community-GraphRAG (Global) (overall; null) | 64.40; 19.27 | accuracy | Han et al. | independent | 20260304 | [22] Table 2 |
| HippoRAG2 (overall; null) | 70.27; 85.71 | accuracy | Han et al. | independent | 20260304 | [22] Table 2 |
| Llama-3.1-70B: no graph; graph built by GPT-4o-mini; by GPT-4o | 65.77; 71.17; 75.08 | accuracy | Han et al. | independent | 20260304 | [22] Table 5 |
| Pinakes 0.32.8 free search: every gold article in the first 8 passages | 43.4% (at least one: 96.8%) | share of 2,255 answerable questions | the owner of this project | first-party (not independent; not re-run here) | 20261030 to 31 | [57] |

**Known problems (benchmark).** The paper's generation test gives retrieved chunks to the model (top 6, at most 2,048 tokens), so it mixes retrieval and reading [6]. Han et al. find stronger graph-building models help only on temporal and comparison queries and that null accuracy drops for graph methods [22].

**Usage evidence.** OpenAlex 23 (arXiv DOI record, 20261102 20:04); Semantic Scholar: not obtained [53][54].

---
## 8. SimpleQuestions

- Slug: `simplequestions`. Role: **both**. Kinds: `questions`, `kg` (questions are tied to Freebase facts; the paper also defines Freebase subsets FB2M and FB5M).

### Dataset

**What it contains.** 108,442 natural-language questions written by human English-speaking annotators, each paired with one Freebase fact (subject, relationship, object) that answers it; the answer is the object [8].

**Size and versions.** Random split 70% train (75,910), 10% validation (10,845) and 20% test (the remainder, 21,687 by my subtraction) [8]. Background KBs: FB2M (2,150,604 entities; 6,701 relationships; 14,180,937 atomic facts), FB5M (4,904,397; 7,523; 22,441,880), and Reverb as a secondary source (2,044,752 entities; 601,360 relationships; 14,338,214 facts) [8]. Later versions or releases: **unstated** in the sources read.

**Licence.** The authors' own data page was not read. The Hugging Face mirror `fbougares/simple_questions_v2` (an uploader's copy) is tagged CC BY 3.0 [36]. Treat that as unconfirmed.

**How it was made.** Facts were taken from FB2M with undefined relationship types (containing "freebase") removed; facts were sampled with a probability that depends on relationship frequency so that rare relationships are not swamped; annotators saw the fact with Freebase hyperlinks and wrote a question whose answer is the object, told to vary phrasing among similar relationships [8].

**Used by.** KBQA work on Freebase; the TriviaQA authors cite it as a KB-QA set [1]. In the archive: no page matched `SimpleQuestions` [55].

**Known problems.**
- Ambiguity in the data bounds accuracy at 83.4% ("ambiguity in the data bounds performance on this benchmark at 83.4%", Petrochuk and Zettlemoyer 2018) [51].
- Questions cover only single facts and the head of the relationship distribution [8].
- Depends on a Freebase subset; the paper's own table lists the subsets' sizes [8].

### Benchmark

**What it tests.** Single-fact question answering over a KB at scale [8].

**Tasks, metrics and protocol.** Given a question, return the object entity of the matching fact; accuracy (the paper reports it as a percentage) with FB2M or FB5M as the memory; WebQuestions F1 and Reverb accuracy are reported alongside [8].

**Datasets.** `simplequestions`; WebQuestions and Reverb appear as co-training sets in the paper [8].

**Results**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Memory Networks, FB2M, trained on WebQuestions + SimpleQuestions + paraphrases | 62.7 | accuracy | SimpleQuestions authors | yes | 20150605 | [8] Table 4 |
| Memory Networks, FB5M, ensemble of 5 | 63.9 | accuracy | same | yes | 20150605 | [8] Table 4 |
| Memory Networks, FB5M, subgraph candidate generation | 62.9 | accuracy | same | yes | 20150605 | [8] Table 4 |
| Upper bound from data ambiguity | 83.4 | accuracy | Petrochuk and Zettlemoyer | independent | 20180424 | [51] |

No independent system table was read; later systems exist but were not read in this run. **Unstated.**

**Known problems (benchmark).** The 83.4% ceiling shows leaderboard gains beyond it cannot be real answers [51].

**Usage evidence.** OpenAlex 528 (arXiv-DOI record, 20261102 20:04); Semantic Scholar: not obtained [53][54].

---

## 9. WebQuestionsSP (WebQSP)

- Slug: `webquestionssp`. Role: **both**. Kinds: `questions`, `kg` (Freebase queries).

### Dataset

**What it contains.** Semantic-parse annotations for questions of WebQuestions that Freebase can answer: SPARQL queries with Freebase identifiers [9]. The original WebQuestions has under 6,000 questions built from the Google Suggest API [8].

**Size and versions.** Full parses for 4,737 questions; the remaining 18.5% of WebQuestions are marked "not answerable"; the Microsoft download also holds partial annotations for 1,073 more, an evaluation script, STAGG output, a document and labelling instructions; version 1.0, listed "Date Published 7/15/2024", 4.2 MB [9][37]. Train and test split sizes: **unstated** in the pages read (the community copy `rmanluo/RoG-webqsp` on Hugging Face has 2,826 train, 246 validation and 1,628 test rows, 4,700 in total, which is a processed derivative, not the original) [58].

**Licence.** **Unstated.** The Microsoft page states no licence or dataset terms (only a generic site "Terms of use" link) [37].

**How it was made.** Annotators produced SPARQL parses for WebQuestions questions; the paper studies the cost and benefit of such labels and adds a stricter definition of "answerable" (answerable by SPARQL rather than by extraction from text) [9]. Who the annotators were and their agreement: **unstated** in the parts read.

**Used by.** Seed for ComplexWebQuestions [10]; in the archive: no page matched `WebQSP` or `WebQuestions` [55].

**Known problems.**
- 18.5% of the original questions were dropped as not answerable on Freebase [9].
- The data page carries no licence [37].

### Benchmark

**What it tests.** KBQA with full semantic parses versus answer-only supervision [9].

**Tasks, metrics and protocol.** Answer set F1 (average F1, precision, recall, accuracy) on the test set [9].

**Datasets.** `webquestionssp`.

**Results**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| STAGG trained on answers only | avg F1 66.8 (precision 67.3, recall 73.1, accuracy 58.8) | F1 | WebQSP authors | yes | ACL 2016 | [9] Table 1 |
| STAGG trained with semantic parses | avg F1 71.7 (precision 70.9, recall 80.3, accuracy 63.9) | F1 | WebQSP authors | yes | ACL 2016 | [9] Table 1 |

No independent comparison was read. **Unstated.**

**Known problems (benchmark).** Only first-party numbers read.

**Usage evidence.** OpenAlex 492 (ACL DOI 10.18653/v1/p16-2033, 20261102 20:04); Semantic Scholar: not obtained [53][54].

---

## 10. ComplexWebQuestions

- Slug: `complexwebquestions`. Role: **both**. Kinds: `questions`, `corpus` (web snippets), `kg`.

### Dataset

**What it contains.** 34,689 complex questions with answers, web snippets and SPARQL queries over Freebase, produced by extending WebQuestionsSP queries with conjunctions, superlatives, comparatives and compositions [10].

**Size and versions.** 34,689 examples in the paper [10]. Train, dev and test counts are not in the text I read. The community copy `rmanluo/RoG-cwq` on Hugging Face (a processed derivative) has 27,639 train, 3,519 validation and 3,531 test rows, which also sum to 34,689 [58]. The two project-page addresses I tried returned 404 [59].

**Licence.** **Unstated.** The project pages I tried were not reachable (404) [59]; a Hugging Face mirror `drt/complex_web_questions` is tagged Apache-2.0 by its uploader, which says nothing about the original [58].

**How it was made.** Sample question-query pairs from WebQuestionsSP; automatically build more complex SPARQL queries; turn them into machine-generated questions; have Amazon Mechanical Turk workers paraphrase them into natural language, validated by one or two further workers, with a bonus for diversity; about 0.11 USD per question [10].

**Used by.** Cited by HotpotQA and 2Wiki as KB-based multi-hop datasets [3][4]; in the archive: no page matched `ComplexWebQuestions` [55].

**Known problems.**
- Questions come from a limited set of query templates, so diversity is bounded by the KB schema (HotpotQA authors make this point about KB-based sets) [3].
- Workers shortened the machine-generated questions on average (16 to 13.18 words) [10].
- Because KB facts can be incomplete, some questions may be answerable from a single sentence (HotpotQA authors, on KB-based sets) [3].

### Benchmark

**What it tests.** Answering complex questions by decomposing them and combining a search engine with a reading-comprehension model [10].

**Tasks, metrics and protocol.** precision@1 on dev and test [10].

**Datasets.** `complexwebquestions`.

**Results**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| SimpQA | 20.4 dev / 20.8 test | precision@1 | CWQ authors | yes | 20180318 | [10] Table 4 |
| SplitQA | 29.0 / 27.5 | precision@1 | CWQ authors | yes | 20180318 | [10] Table 4 |
| SplitQA oracle | 34.0 / 33.7 | precision@1 | CWQ authors | yes | 20180318 | [10] Table 4 |
| RCQA / SplitRCQA | 18.7 / 21.5 dev; 18.6 / 22.0 test | precision@1 | CWQ authors | yes | 20180318 | [10] Table 4 |
| Human (limited time) | 63.0 | precision@1 | CWQ authors | yes | 20180318 | [10] |

No independent comparison was read. **Unstated.**

**Known problems (benchmark).** Only the first-party baseline table was read.

**Usage evidence.** OpenAlex 520 (NAACL DOI 10.18653/v1/n18-1059, 20261102 20:04); Semantic Scholar: not obtained [53][54].

---

## 11. MetaQA

- Slug: `metaqa`. Role: **both**. Kinds: `questions`, `kg` (movie knowledge base `kb.txt`).

### Dataset

**What it contains.** More than 400K movie-domain questions in three hop depths (1-hop, 2-hop, 3-hop), each in a text version, a paraphrased version ("NTM") and, for the 1-hop vanilla set, audio; all questions are generated from the WikiMovies knowledge base, supplied as triples `subject|relation|object` [38][11]. Entities in questions are marked with square brackets [38].

**Size and versions.** Questions: 1-hop train 96,106 / dev 9,992 / test 9,947; 2-hop 118,980 / 14,872 / 14,872; 3-hop 114,196 / 14,274 / 14,274 [38]. The 1-hop set derives from the `wiki_entities` branch of WikiMovies minus ambiguous-entity questions; 2-hop has 21 question types and 3-hop 15, with 10 text templates each [38]. Knowledge-base size: **unstated** in the texts read. Versions: the paper has five arXiv versions (latest stamp 27 November 2017); dataset versioning **unstated** [11].

**Licence.** "Released under the Creative Commons Public License. A copy is included with the data" [38]; the specific variant is **unstated** here and the repository has no `LICENSE` file (404). The data is hosted on Google Drive [38].

**How it was made.** 2-hop and 3-hop questions are generated from KB paths with templates; the paraphrase set translates each vanilla question to French and back; the audio set uses a text-to-speech API [38].

**Used by.** Named as a multi-hop KB dataset in the 2Wiki paper [4]; in the archive: no page matched `MetaQA` [55].

**Known problems.**
- Questions are template-generated, so language and relation variety are narrow [38].
- A large share of test questions can be answered by memorising training question-answer pairs: the share of new entity pairs in test is 34.5% (1-hop), 28.6% (2-hop), 32.2% (3-hop) [11].
- Single domain (movies) [38].

### Benchmark

**What it tests.** Multi-hop reasoning over a KG with and without labelled topic entities, text and audio [11].

**Tasks, metrics and protocol.** Hits@1 on test; settings Vanilla (all topic entities labelled), Vanilla-EU (5% labelled), NTM-EU and Audio-EU [11].

**Datasets.** `metaqa`.

**Results**

| System | Score (1-hop / 2-hop / 3-hop) | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| VRN, Vanilla | 97.5 / 89.9 / 62.5 | hits@1 | MetaQA authors | yes | AAAI 2018; arXiv v5 stamp 20171127 (v1 date unstated) | [11] Table 1 |
| Bordes et al. QA system, Vanilla | 95.7 / 81.8 / 28.4 | hits@1 | MetaQA authors | yes (baseline run by them) | same | [11] Table 1 |
| KV-MemNN, Vanilla | 95.8 / 25.1 / 10.1 | hits@1 | MetaQA authors | yes | same | [11] Table 1 |
| VRN, Vanilla-EU | 82.0 / 75.6 / 38.3 | hits@1 | MetaQA authors | yes | same | [11] Table 1 |
| Supervised embedding, Vanilla-EU | 18.1 / 23.2 / 25.3 | hits@1 | MetaQA authors | yes | same | [11] Table 1 |

No independent comparison was read.

**Known problems (benchmark).** Supervised embedding does better in the unlabelled setting because it memorises pairs, which the authors themselves call weak generalisation [11].

**Usage evidence.** OpenAlex 490 (arXiv-DOI record, 20261102 20:04); Semantic Scholar: not obtained [53][54].

---

## 12. LC-QuAD 2.0

- Slug: `lc-quad-2`. Role: **both**. Kinds: `questions`, `kg` (queries target Wikidata and DBpedia 2018).

### Dataset

**What it contains.** Natural-language questions with corresponding SPARQL queries for Wikidata and DBpedia (2018 version); fields include `NNQT_question`, `question`, `paraphrased_question`, `template`, `template_index`, `subgraph`, `sparql_wikidata`, `sparql_dbpedia18` [39].

**Size and versions.** The card says "30,000 pairs"; the same card's splits are train 19,293 and test 4,781, 24,074 in all, which does not add up to 30,000 and is **unexplained** in the card [39]. Version tags: **unstated**.

**Licence.** CC BY 3.0, stated on the Hugging Face card (copy `mohnish/lc_quad`) [39]. The authors' GitHub repository `AskNowQA/LC-QuAD2.0` has no `LICENSE` file and its README is one sentence [39]. Treat the licence as unconfirmed by the authors.

**How it was made.** The card's metadata says the annotations were crowdsourced and lists the template fields above; the ISWC 2019 paper (Dubey, Banerjee, Abdelkawi, Lehmann) is paywalled and the abstract is elided in Semantic Scholar [39][54]. Full construction process: **unstated** here.

**Used by.** In the archive: no page matched `LC-QuAD` [55].

**Known problems.** The card lists "Other Known Limitations" as "More Information Needed" [39]. The official website `lc-quad.sda.tech` refused the connection on 20261102 20:07 [39]. Split counts conflict with the stated size (above).

### Benchmark

**What it tests.** Translating complex questions into SPARQL over Wikidata or DBpedia [39].

**Tasks, metrics and protocol.** Question-to-SPARQL generation; metrics: **unstated** in what I read.

**Datasets.** `lc-quad-2`.

**Results.** None read. **Unstated.**

**Known problems (benchmark).** No results table could be sourced in this pass.

**Usage evidence.** OpenAlex 194 (Springer DOI 10.1007/978-3-030-30796-7_5, 20261102 20:04); Semantic Scholar 276 (same DOI, 20261102 20:08) [53][54].

---

## 13. GrailQA

- Slug: `grailqa`. Role: **both**. Kinds: `questions`, `kg` (Freebase ontology and logical forms).

### Dataset

**What it contains.** 64,331 crowdsourced questions over Freebase, each with answers and logical forms in several syntaxes (SPARQL, S-expression, graph query), covering all 86 domains of Freebase Commons, with up to 4 relations and functions such as counting, comparatives and superlatives [12][40].

**Size and versions.** Train 44,337; validation 6,763; test 13,231 (about 70/10/20). In validation and test, 50% of questions come from held-out domains (zero-shot), 25% from canonical logical forms not seen in training (compositional) and 25% sampled from training (i.i.d.); 5 domains are held out for validation and 10 for test [12]. The repository also ships processed Freebase ontology files, entity-linking results and cached SPARQL results [40]. The project page gives the download size as about 120 MB and hosts the leaderboards [40].

**Licence.** The project page states CC BY-SA 4.0 for the dataset; the repository `LICENSE` is Apache-2.0 and covers the code; the paper is CC BY 4.0 [40][12].

**How it was made.** Canonical logical forms are sampled from the Freebase graph, turned into canonical questions, and paraphrased by native-English Amazon Mechanical Turk workers (at least 95% approval rate) with automatic and manual quality control; entity surface forms were mined from the web and used in questions; 6,685 crowd workers contributed [12].

**Used by.** In the archive: no page matched `GrailQA` [55].

**Known problems.** Running the baselines needs a local Freebase in a Virtuoso triple store [40]. The leaderboard page shows inconsistent submitter attribution ("Anonymous" for two of three top rows) [40 site].

### Benchmark

**What it tests.** Three levels of generalisation for KBQA: i.i.d., compositional and zero-shot [12].

**Tasks, metrics and protocol.** Predict the logical form or answer; exact match (EM) of logical forms and answer F1; separate scores per generalisation level. The leaderboard ranks by F1 [12][40].

**Datasets.** `grailqa`.

**Results**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| SG-KBQA (leaderboard rank 1, overall) | EM 79.140, F1 84.403; compositional EM 77.875, F1 85.064; zero-shot EM 75.364, F1 80.792 | EM, F1 | University of Melbourne (overall row; the other two rows say "Anonymous") | no | 20240913 | [40 site] (23 entries per board) |
| Ranking (BERT) | overall EM 50.6, F1 58.0; i.i.d. 59.9 / 67.0; compositional 45.5 / 53.9; zero-shot 48.6 / 55.7 | EM, F1 | GrailQA authors | yes | WWW 2021; arXiv v6 stamp 20210222 (v1 date unstated) | [12] Table 3 |
| Transduction (BERT) | overall EM 33.3, F1 36.8; zero-shot 25.7 / 29.3 | EM, F1 | GrailQA authors | yes | same | [12] Table 3 |
| QGG (reference system) | overall F1 36.7; i.i.d. 40.5; compositional 33.0; zero-shot 36.6 | F1 | GrailQA authors (run of an earlier system) | yes | same | [12] Table 3 |

**Known problems (benchmark).** Single leader on all three boards (same system name); ranking by F1 only [40 site].

**Usage evidence.** OpenAlex 183 (ACM DOI 10.1145/3442381.3449992, 20261102 20:04); Semantic Scholar: not obtained [53][54].

---
## 14. LoCoMo

- Slug: `locomo`. Role: **both**. Kinds: `questions`, `corpus` (long multi-session conversations).
- **Licence flag: non-commercial.** Treat as a read-only reference (ideas and results only, no data reuse) under the project rule.

### Dataset

**What it contains.** Very long conversations between two simulated speakers, each with a persona and a timeline of events, with shared images (not released), plus annotations for question answering, event summarisation and multimodal dialogue [13][41]. The released JSON has, per conversation: `conversation` (sessions with dates), `qa`, `event_summary`, `observation`, `session_summary`, `sample_id` [41].

**Size and versions.** The paper (arXiv v1 27 February 2024) describes 50 dialogues of about 300 turns and 9K tokens on average, up to 35 sessions [13]. The repository now says "The benchmark consists of ten conversations" in `data/locomo10.json`, adds "The initial release contained 50 conversations" and that this release is a subset of the first arXiv version's conversations; images are not released [41]. My count of the file read on 20261102 19:52: 10 conversations; 272 sessions (19 to 32 per conversation); 5,882 turns; 1,986 QA items; by `category` code 1: 282, 2: 321, 3: 96, 4: 841, 5: 446; 444 QA items have no `answer` key [41]. The paper names five reasoning types (single-hop, multi-hop, temporal, open-domain/commonsense, adversarial) [13]; which code maps to which type is **unstated** in the pages read.

**Licence.** `LICENSE.txt` in the repository is Creative Commons Attribution-NonCommercial 4.0 (its first line reads "Attribution-NonCommercial 4.0 International") [41]. The README and project page add no separate data statement; the project page mentions no licence [41].

**How it was made.** A machine-human pipeline: LLM agents given a persona and a temporal event graph generate the sessions, can share and react to images, and use a memory of past sessions; human annotators then fix long-range inconsistencies, drop irrelevant images and verify that dialogue is grounded in the events [13][41].

**Used by.** Mem0 paper [26]; Bao et al. [25]; derived sets (LoCoMo-Plus, "When Users Don't Ask") per the archive lead; in the archive: `kb-kg/directions/agent-memory.md`, `eager-to-lazy-graphs.md`, `evidence-and-claims.md`, `graph-features-in-and-out.md`, `infrastructure-and-protocols.md`, `plain-files-and-wikis.md`, `reasoning-retrieval.md`, `kb-kg/literature/graph-rag-research.md`, `kb-kg/llm-era/README.md`, `kb-kg/papers-benchmarks/README.md` [55].

**Known problems.**
- The public data is a 10-conversation subset of the 50 in the paper, so older and newer numbers may not be comparable [13][41].
- 444 of 1,986 QA items have no `answer` field in the released file, so a scorer must handle them (they are the adversarial items by count: 446 in category 5; this match is my inference) [41].
- Conversations are about 9K tokens, short enough that a long-context model can read all of it; full-context rows score 72.90 (Mem0 paper) and 72.30 / 80.60 (Bao et al., two readers) [26][25].
- Neither Mem0's Table 1 nor Bao et al.'s Table 3 reports the adversarial category; both show four categories [26][25].
- The scoring differs by paper: F1 [13], LLM-as-a-judge [26], accuracy [25].

### Benchmark

**What it tests.** Memory of very long multi-session dialogue [13].

**Tasks, metrics and protocol.** Question answering (F1 on the answer; recall@k for retrieval), event summarisation (ROUGE, FactScore) and multimodal dialogue generation [13]. The repository ships QA scripts for several model APIs and a RAG QA script with `gpt-3.5-turbo`; the summarisation and multimodal evaluations are marked "Coming soon!" [41].

**Datasets.** `locomo`.

**Results** (QA only)

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Human | overall 87.9 (single-hop 95.1, multi-hop 85.8, temporal 92.6, open-domain 75.4, adversarial 89.4) | F1 | LoCoMo authors | yes | 20240227 | [13] Table 2 |
| GPT-3.5-turbo-16K, 16K context | overall 37.8 | F1 | LoCoMo authors | yes | 20240227 | [13] Table 2 |
| GPT-4-turbo, 4,096 context | overall 32.1 (adversarial 70.2) | F1 | LoCoMo authors | yes | 20240227 | [13] Table 2 |
| GPT-3.5-turbo-16K with dialog-turn RAG, top-25 | overall 35.8; recall@25 79.9 | F1; recall | LoCoMo authors | yes | 20240227 | [13] Table 3 |
| Mem0 | 66.88 overall (single 67.13, multi 51.15, open 72.93, temporal 55.51) | LLM-as-a-judge | Mem0 team | **first-party** (the system's authors) | 20250428 | [26] Tables 1, 2 |
| Mem0g (graph variant) | 68.44 overall | LLM-as-a-judge | Mem0 team | first-party | 20250428 | [26] Table 2 |
| Zep; LangMem; OpenAI memory; A-Mem | 65.99; 58.10; 52.90; 48.38 | LLM-as-a-judge | Mem0 team (competitors' systems run by Mem0's authors) | not the systems' authors, but the paper's authors have a product in the table | 20250428 | [26] Table 2 |
| Full context | 72.90 | LLM-as-a-judge | Mem0 team | first-party | 20250428 | [26] Table 2 |
| RAW-RAG (raw history, dense retrieval + reranker), GPT-4o-mini / GPT-4.1-mini reader | 89.07 / 93.70 overall | accuracy | Bao et al. | first-party for RAW-RAG | 20261022 | [25] Table 3 |
| Full-context, same readers | 72.30 / 80.60 | accuracy | Bao et al. | independent | 20261022 | [25] Table 3 |
| MemMachine; EverMemOS; SimpleMem | 88.12 / 91.69; 86.76 / 93.05; 78.25 / 83.87 | accuracy | Bao et al. (rows may be reported figures, not re-runs; the Mem0 row equals the Mem0 paper's own numbers, so that row at least is copied) | independent of those systems | 20261022 | [25] Table 3 |

**Known problems (benchmark).** Judge model, prompt and category handling differ between the Mem0 and Bao et al. setups, so rows across papers are not comparable [26][25]. All rows for named memory products come from papers whose authors have an interest in the outcome [26][25].

**Usage evidence.** OpenAlex 96 (ACL DOI 10.18653/v1/2024.acl-long.747, 20261102 20:04); Semantic Scholar: not obtained [53][54].

---

## 15. LongMemEval

- Slug: `longmemeval`. Role: **both**. Kinds: `questions`, `corpus` (chat histories).

### Dataset

**What it contains.** 500 manually created questions that each need information from one or more task-oriented user-assistant dialogues placed inside a longer chat history. Five abilities: information extraction, multi-session reasoning, temporal reasoning, knowledge updates and abstention. Question types in the data include single-session user, single-session assistant, single-session preference, multi-session, knowledge update and temporal reasoning [14].

**Size and versions.** Three standard settings: `longmemeval_oracle` (evidence sessions only), `longmemeval_s` (about 115k tokens per problem) and `longmemeval_m` (500 sessions, about 1.5 million tokens) [14]. The Hugging Face repository `xiaowu0162/longmemeval-cleaned` "replaces the original LongMemEval dataset" and "removes noisy history sessions that interfere with the answer correctness" (card text, last modified 20250919); it holds the splits `longmemeval_oracle`, `longmemeval_s_cleaned`, `longmemeval_m_cleaned` [42]. The paper is v2 of 4 March 2025 [14]. How many sessions were removed: **unstated** here (the card links a spreadsheet I did not open).

**Licence.** MIT, on the Hugging Face card and in the repository `LICENSE` (Copyright 2024 Di Wu) [42]. The history sessions come from simulated chats and "publicly released chat sessions" (Figure 2 of the paper); their own licences are **unstated** [14].

**How it was made.** Question construction: an LLM proposes seed question-answer pairs from user-attribute paragraphs (164 attributes in five categories), then human experts filter and rewrite all questions and decompose each answer into evidence statements with optional timestamps. Each evidence statement is embedded in a task-oriented session created by LLM self-chat and edited by humans, with the evidence stated indirectly. At test time the full history is assembled to a configurable length from evidence sessions and non-conflicting history sessions [14].

**Used by.** Zep paper [27]; Bao et al. [25]; in the archive: `kb-kg/directions/agent-memory.md`, `evidence-and-claims.md`, `infrastructure-and-protocols.md`, `plain-files-and-wikis.md`, `reasoning-retrieval.md`, `kb-kg/literature/graph-rag-research.md`, `kb-kg/llm-era/README.md`, `kb-kg/papers-benchmarks/README.md`, `kb-kg/projects/basic-memory.md`, `cognee.md` [55].

**Known problems.**
- The original release contained noisy history sessions; the cleaned release replaced it (above) [42]. Numbers from before and after may differ; by how much is **unstated**.
- Simulated chats and LLM-edited sessions differ from real conversations [14].
- Scores rely on an LLM evaluator reported to agree with human experts more than 97% of the time [14].

### Benchmark

**What it tests.** Long-term interactive memory of chat assistants across the five abilities [14].

**Tasks, metrics and protocol.** Answer the question given the history; accuracy by an LLM judge (the repository script takes `gpt-4o` as the judge model); retrieval variants report recall@k and downstream accuracy [14][42].

**Datasets.** `longmemeval` (oracle, S, M).

**Results**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| GPT-4o, oracle vs LongMemEval_S, no Chain-of-Note | 0.870 vs 0.606 (30.3% drop) | accuracy | LongMemEval authors | yes | v2 20250304 | [14] |
| Llama 3.1 70B Instruct | 0.744 vs 0.334 (55.1% drop) | accuracy | LongMemEval authors | yes | 20250304 | [14] |
| ChatGPT and Coze with GPT-4o (memory features) | accuracy drops of 37% and 64% against offline reading | accuracy | LongMemEval authors | yes | 20250304 | [14] |
| Zep (gpt-4o-mini; gpt-4o) vs full-context | 63.8% vs 55.4%; 71.2% vs 60.2% | accuracy | Zep team | **first-party** | 20250120 | [27] |
| RAW-RAG (GPT-4.1-mini reader) | 87.53 overall | accuracy | Bao et al. | first-party for RAW-RAG | 20261022 | [25] Table 3 |
| Full-context, same reader | 65.60 overall | accuracy | Bao et al. | independent | 20261022 | [25] Table 3 |
| Memora; EverMemOS; EMem; MemOS | 87.40; 83.00; 83.00; 77.80 | accuracy | Bao et al. (reported or re-run: unstated) | independent of those systems | 20261022 | [25] Table 3 |

(In Bao et al.'s Table 3 the LongMemEval block, with columns S-U., S-A., S-P., M-S., KU., TR. and Overall, is headed GPT-4.1-mini [25].)

**Known problems (benchmark).** The Zep paper's baselines and judge are its authors' choices [27]. Cleaned versus original release (above). Rows from different papers use different readers [14][25][27].

**Usage evidence.** OpenAlex 4 (arXiv-DOI record, 20261102 20:04; the ICLR version is not indexed there); Semantic Scholar: not obtained [53][54].

---

## 16. Wikipedia snapshots used by DPR and KILT

- Slug: `wikipedia-dpr-kilt`. Role: **dataset**. Kinds: `corpus`.
- The benchmark that uses the KILT snapshot is the next item (`kilt`).

### Dataset

**What it contains.** Two processed English-Wikipedia corpora used as retrieval collections for open-domain QA:
1. **DPR passages.** Wikipedia dump of 20 December 2018, text cleaned with the DrQA preprocessing code (which removes semi-structured data such as tables, infoboxes, lists and disambiguation pages), split into disjoint blocks of 100 words, each prefixed with its article title [15][43].
2. **KILT knowledge source.** Wikipedia dump of 1 August 2019 (2019/08/01), stored per article with paragraph lists, anchors and history, with the 11 KILT datasets mapped onto it [16][44].

**Size and versions.** DPR: 21,015,324 passages [15]; the Hugging Face copy `facebook/wiki_dpr` shows 21,015,300 rows with 768-dimensional DPR embeddings [43]. KILT: 5.9M articles [16]; the Hugging Face copy lists 5,903,530 rows (about 29.4 GB) for `2019-08-01`; the original JSON is 34.76 GiB [44]. Other snapshots used by sibling datasets: HotpotQA 1 October 2017 [3]; 2WikiMultiHopQA 1 January 2020 (Wikipedia) and 31 December 2019 (Wikidata) [4]; PopQA retrieval December 2018 [2]. A 2021 DPR release added a better NQ checkpoint and Wikipedia embeddings [43].

**Licence.** Wikipedia text: "all original textual content is licensed under the GNU Free Documentation License"; some is available only under Creative Commons, some authors use other licences (Wikimedia dumps legal page) [49]. The DPR repository (and the `wiki_dpr` card) are CC BY-NC 4.0, so the processed DPR passages carry a non-commercial label in this release [43]. KILT: repository MIT; `kilt_tasks` card MIT; the `kilt_wikipedia` card has no licence text [44].

**How it was made.** DPR: DrQA-style extraction, then 100-word blocks (following Wang et al. 2019) [15]. KILT: a fixed 2019 snapshot chosen so every task's evidence can be aligned to one source; the alignment strategy is in the appendix, not read [16].

**Used by.** DPR, KILT, PopQA's retrieval, RAGSearch's dense backend (2018 dump) [15][16][2][23]. In the archive: no page matched `DPR` or `KILT` [55].

**Known problems.**
- Two snapshots one year apart: results using different ones are not directly comparable [15][16].
- The DPR cleaning drops tables, lists and infoboxes, so questions whose answers live there become unanswerable by design [15].
- Wikipedia text is share-alike while the DPR release is NC; combined redistribution terms are **unstated** by the authors.
- Snapshots are old relative to LLM training data; contamination: **unstated**.

---

## 17. KILT

- Slug: `kilt`. Role: **benchmark**. Datasets: `wikipedia-dpr-kilt` (knowledge source), plus 11 component datasets (NQ, HotpotQA and TriviaQA are items in this file).

### Benchmark

**What it tests.** Knowledge-intensive tasks (fact checking, entity linking, slot filling, open-domain QA, dialogue) all grounded in one Wikipedia snapshot, so retrieval and reading can be compared across tasks [16].

**Tasks, metrics and protocol.** 11 datasets over 5 tasks: FEVER (fact checking); AIDA CoNLL-YAGO, WNED-WIKI, WNED-CWEB (entity linking); T-REx, Zero Shot RE (slot filling); Natural Questions, HotpotQA, TriviaQA, ELI5 (open-domain QA); Wizard of Wikipedia (dialogue). Downstream metrics (accuracy, exact match, ROUGE-L, F1), page-level R-Precision for retrieval, and KILT scores that count a downstream hit only when the right provenance page is retrieved. A new portion of NQ held out originally serves as the KILT NQ test set [16]. The repository carries the files and a leaderboard hook; leaderboard rows were not read [44].

**Datasets.** `wikipedia-dpr-kilt` (KILT snapshot); NQ, HotpotQA, TriviaQA and others as listed.

**Results** (downstream test, selected columns)

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| RAG | FEVER 86.31; NQ 44.39; HotpotQA 26.97; TriviaQA 71.27; T-REx 59.2; zsRE 44.74; ELI5 14.05 (ROUGE-L); WoW 13.11 (F1) | accuracy / EM / RL / F1 | KILT authors | yes (RAG's authors overlap with KILT's) | v4 20210527 | [16] Table 3 |
| BART + DPR | FEVER 86.74; NQ 41.27; HotpotQA 25.18; TriviaQA 58.55; T-REx 59.16; zsRE 30.43 | same | KILT authors | yes | 20210527 | [16] Table 3 |
| BART large (no retrieval) | FEVER 78.93; NQ 21.75; HotpotQA 15.37; TriviaQA 32.39 | same | KILT authors | yes | 20210527 | [16] Table 3 |
| Task-specific BERT + DPR | FEVER 69.68; NQ 38.64; HotpotQA 11.29; TriviaQA 70.38 | same | KILT authors | yes | 20210527 | [16] Table 3 |

No independent KILT study was read.

**Known problems.** Mapping every dataset to one 2019 snapshot means some original evidence is not found in the new snapshot (the paper's appendix covers this; not read) [16]. The knowledge source is 34.76 GiB [44].

**Used by.** Not in the archive [55].

**Usage evidence.** OpenAlex 357 (NAACL DOI 10.18653/v1/2021.naacl-main.200, 20261102 20:04); Semantic Scholar: not obtained [53][54].

---
## 18. MS MARCO

- Slug: `ms-marco`. Role: **both**. Kinds: `questions`, `corpus`.
- **Licence flag: non-commercial research only.** Treat as a read-only reference.

### Dataset

**What it contains.** Anonymised real search queries from Bing (and Cortana), each with passages extracted by Bing from retrieved web documents, human-written answers, and marks of supporting passages; unanswerable questions are kept [17]. The collection grew into a family: a QnA set, an NLGEN set, passage ranking, document ranking, keyphrase extraction, and ORCAS click data [45].

**Size and versions.** The paper (v3) states 1,010,916 questions, 8,841,823 passages from 3,563,535 web documents and 182,669 human-rewritten answers [17]. The project page gives: passage ranking 8.8 million passages; document ranking 3.2 million documents; first QnA set 100,000 real questions; QnA v2.1 over 1,000,000 queries; NLGEN 180,000; keyphrase 148,124 documents; ORCAS 20 million clicks [45]. Changelog on the page: V1.0 (2016-12-01 if the page's day-first pattern holds; the page prints "12.01.2016"), V2.0 (2018-03-01), V2.1 (2018-04-23), ranking set based on v2.1 (2018-10-26), ORCAS (2020-07-30), document ranking (2020-08-11), QnA, NLGEN and OpenKP tasks retired (2020-10-23) [45]. The passage-ranking release has 808,731 train, 101,093 dev and 101,092 eval queries, each with about 1,000 BM25 candidate passages, with relevance labels from the `is_selected` flag; the sets would be around 35% smaller without queries that have no answer [45 README].
**Licence.** "The MS MARCO datasets are intended for non-commercial research purposes only"; no licence or IP rights extended; provided as is; rights end on violation [45]. The `MSMARCO-Passage-Ranking` repository is MIT (Microsoft) and covers the repository [45].

**How it was made.** Queries sampled from Bing logs and anonymised; Bing retrieves documents and extracts passages; crowd-sourced editors write answers from the passages in complete sentences, mark supporting passages (not exhaustive) and may mark a question unanswerable [17]. For passage ranking, ~8.8M unique passages were pooled and BM25 run per query; the original 3.5M source URLs were re-scraped in March 2018 and many domains were lost with the delay [45 README].

**Used by.** Contriever is fine-tuned on MS MARCO (cited in the PopQA paper) [2]; compared in TriviaQA and HotpotQA papers as an independent-question set [1][3]. In the archive: no page matched `MS MARCO` [55].

**Known problems.**
- Relevance labels are sparse (editors need not mark all supporting passages) [17].
- Evaluation-design pitfalls are discussed by the MS MARCO and TREC DL organisers: "best" run versus robust usefulness [52].
- Many queries have no answer [45 README].
- Source documents were scraped after a delay, so some pages differ from what Bing saw [45 README].

### Benchmark

**What it tests.** Machine reading comprehension and ranking of passages or documents for real search queries [17][45].

**Tasks, metrics and protocol.** Three tasks in the paper (answer synthesis, passage-level answers, ranking); the ranking track re-ranks the 1,000 BM25 candidates per query and is scored with MRR@10; the QnA track used Rouge-L and BLEU-1 [17][45]. The site calls the QnA and NLGEN leaderboards closed on 2020-10-23; the passage and document leaderboards are marked "RETIRED" with an end date of 2023-01-01, although the retirement text says submissions "will continue as usual" (inconsistent) [45].

**Datasets.** `ms-marco`.

**Results**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Multi-doc Enriched BERT (QnA leaderboard, top) | 0.540 | Rouge-L | submitter **unstated** on the page; board run by Microsoft | the board is Microsoft's own | board closed 20201023 | [45] |

Passage-ranking leaderboard rows were not readable (the page is script-rendered and returned only its title). No independent table was read. **Unstated.**

**Known problems (benchmark).** Closed or retired leaderboards; inconsistent status text [45]. MRR@10 depends on sparse labels [17][52].

**Usage evidence.** OpenAlex 1,190 (arXiv-DOI record, 20261102 20:04); Semantic Scholar: not obtained [53][54].

---

## 19. UltraDomain

- Slug: `ultradomain`. Role: **both** (thin). Kinds: `questions`, `corpus`.

### Dataset

**What it contains.** Long contexts from three kinds of source, each with LLM-generated high-level question-answer pairs that need a comprehensive reading of the context: (1) college textbooks across 18 domains (natural sciences, humanities, social sciences); (2) financial reports (Fin); (3) legal contracts (Leg); plus a Misc set that mixes contexts of the specialised sets [18]. Contexts reach up to one million tokens [18].

**Size and versions.** MemoRAG's appendix table for the textbook domains totals 3,240 evaluation samples (Technology 240, Biology 220, Religion 220, Fiction 220, Psychology 200, Music 200, Art 200, Philosophy 200, Health 180, History 180, Literature 180, Biography 180, Politics 180, Mathematics 160, Physics 160, Cooking 120, Agriculture 100, Computer 100); contexts range from 32,793 to 1,071,342 in the table's length unit, average 150,684; separate rows give Fin 345 samples and Legal 438 samples [18]. Xiang et al. list UltraDomain as "2500" questions [20]. These counts are not reconciled in the sources read. The Hugging Face repository holds 20 files: agriculture, art, biography, biology, cooking, cs, fiction, fin, health, history, legal, literature, mathematics, mix, music, philosophy, physics, politics, psychology, technology; there is no `religion` file although the paper's table has a Religion row [47]. LightRAG used four subsets (Agriculture, CS, Legal, Mix), each 600,000 to 5,000,000 tokens, and says the data is "sourced from 428 college textbooks" in 18 domains [19].

**Licence.** The Hugging Face card says Apache-2.0 and gives no other statement; the MemoRAG repository is Apache-2.0 [47]. The paper's footnote points the textbook source to a Hugging Face dataset named `books-3-textbooks`; whether those texts may be redistributed is **unstated** [18].

**How it was made.** 428 college textbooks across 18 domains, financial reports and legal contracts; text spans up to 128K tokens were given to GPT-4 to write high-level QA pairs; six graduate students reviewed the pairs by selecting questions that are not directly searchable and by judging answer quality, which left 3,240 samples [18].

**Used by.** MemoRAG [18]; LightRAG (contexts only) [19]; Xiang et al. (compared) [20]; EffiRAG (per the archive lead; not re-read). In the archive: `kb-kg/directions/eager-to-lazy-graphs.md`, `evidence-and-claims.md`, `kb-kg/literature/graph-rag-research.md`, `kb-kg/papers-benchmarks/README.md`, `kb-kg/projects/lightrag.md` [55].

**Known problems.**
- LightRAG did **not** use UltraDomain's questions: it asks an LLM to make 5 users, 5 tasks per user and 5 questions per task, 125 questions per dataset, and judges answers pairwise with an LLM [19]. A result "on UltraDomain" can mean either the original questions or this self-made set.
- Question counts differ between sources (3,240 versus 2,500) [18][20].
- Questions and answers are GPT-4 generated with a small human review [18].
- About 97% of UltraDomain questions are of the "contextual summarise" type, and its entity graph is sparse (average degree 0.86) [20].
- Source-text rights unclear (above).

### Benchmark

**What it tests.** Long-context and global-sensemaking question answering [18][19].

**Tasks, metrics and protocol.** MemoRAG reports its UltraDomain results in a figure (F1-style scores; values not extracted). LightRAG's protocol: pairwise LLM preference on four dimensions (comprehensiveness, diversity, empowerment, overall), reported as win rates [18][19].

**Datasets.** `ultradomain`.

**Results**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| LightRAG vs NaiveRAG, "Overall" win rate for LightRAG | Agriculture 67.6%, CS 61.2%, Legal 84.8%, Mix 60.0% | pairwise LLM preference | LightRAG authors | **first-party** (own method, own question set) | v3 20250428 | [19] Table 1 |
| LightRAG vs GraphRAG, "Overall" win rate for LightRAG | 54.8%, 52.0%, 52.8%, 49.6% | same | LightRAG authors | first-party | v3 20250428 | [19] Table 1 |
| LightRAG vs HyDE, "Overall" | 75.2%, 58.4%, 73.6%, 57.6% | same | LightRAG authors | first-party | 20250428 | [19] Table 1 |

Only first-party numbers were read; an independent comparison on the original UltraDomain questions: **unstated**.

**Known problems (benchmark).** LLM pairwise judging; results depend on question generation by the same authors [19].

**Usage evidence.** OpenAlex 30 for MemoRAG (arXiv-DOI record), 209 for LightRAG (20261102 20:04); Semantic Scholar: not obtained [53][54].

---

## 20. GraphRAG-Bench (Xiang et al.)

- Slug: `graphrag-bench-xiang`. Role: **both**. Kinds: `questions`, `corpus`.
- Name clash: a second, unrelated "GraphRAG-Bench" exists (Xiao et al., arXiv 2506.02404, per the archive lead; not re-read). Cite by first author.

### Dataset

**What it contains.** Two corpora and their questions: **Novel**, pre-20th-century novels from Project Gutenberg, chosen for being lesser known to limit pretraining overlap and for narrative ambiguity; **Medical**, NCCN clinical guidelines, chosen for dense hierarchical structure. Four question levels: fact retrieval, complex reasoning, contextual summarisation, creative generation. Each question has an answer, evidence text and evidence triples or relations [20][47].

**Size and versions.** The paper's comparison table gives 4,076 questions [20]. The released question files hold 2,010 (Novel) and 2,062 (Medical) = 4,072, counted on 20261102 20:16 [47]. Novel by type: Fact Retrieval 971, Complex Reasoning 610, Contextual Summarize 362, Creative Generation 67; Medical: 1,098, 509, 289, 166 [47]. Corpus files `Datasets/Corpus/novel.json` (4,848,652 bytes) and `medical.json` (1,055,158 bytes) [47]. The paper's legal and financial corpus statistics (72.7K documents, 295.58M tokens; 2,207 reports, 115.86M tokens) are suggestions for extension, not part of the release [20]. Paper version v3 22 February 2026 (ICLR 2026) [20]. The repository says the benchmark was accepted at ICLR'26 (news 2026-01-26) [47].

**Licence.** Repository `LICENSE` is MIT (Copyright 2025 XMU-DeepLIT) and covers the repository; the Hugging Face card metadata carries no licence field [47]. Gutenberg novels and NCCN guidelines have their own terms; redistribution rights **unstated**.

**How it was made.** Corpora selected as above; ontologies built with GPT-4.1 (vertical hierarchies and horizontal dependencies); evidence collected as dense subgraphs and multi-hop chains; questions generated per level and refined by GPT-4.1 from evidence segments; final confirmation by advanced models plus human checking [20].

**Used by.** Its own paper [20]. In the archive: `kb-kg/papers-benchmarks/README.md`, `kb-kg/literature/graph-rag-research.md`, `kb-kg/directions/eager-to-lazy-graphs.md`, `evidence-and-claims.md`, `infrastructure-and-protocols.md`, `kb-kg/projects/fast-graphrag.md`, `graphrag-sdk.md`, `lightrag.md`, `linearrag.md` [55].

**Known problems.**
- Paper counts 4,076 questions; the released files hold 4,072 [20][47].
- Ontologies and questions are LLM-generated (GPT-4.1) [20].
- The entity-graph density of the two corpora (average degree 1.05 and 2.27) was designed to exceed HotpotQA-type sets (0.60 to 0.86), so it favours graph methods by construction [20].
- The `kb-kg/papers-benchmarks/README.md` lead flags a Table 17 inconsistency in the paper; I did not re-check it [55].

### Benchmark

**What it tests.** Whether graph structure helps at four levels of task difficulty, and where in the pipeline (graph building, retrieval, generation) a method fails [20].

**Tasks, metrics and protocol.** Generation: accuracy, ROUGE-L, coverage, faithfulness score; retrieval: context recall and relevance, evidence recall; fixed generator GPT-4o-mini; 11 GraphRAG frameworks and two plain-RAG baselines [20].

**Datasets.** `graphrag-bench-xiang` (Novel, Medical).

**Results** (Table 9, accuracy, GPT-4o-mini generator, benchmark authors)

| System (Novel) | Fact retrieval | Complex reasoning | Contextual summarise | Creative generation |
|---|---|---|---|---|
| RAG with rerank | 60.92 | 42.93 | 51.30 | 38.26 |
| HippoRAG2 | 60.14 | 53.38 | 64.10 | 48.28 |
| MS-GraphRAG (local) | 49.29 | 50.93 | 64.40 | 39.10 |
| LightRAG | 58.62 | 49.07 | 48.85 | 23.80 |

| System (Medical) | Fact retrieval | Complex reasoning | Contextual summarise | Creative generation |
|---|---|---|---|---|
| RAG with rerank | 64.73 | 58.64 | 65.75 | 60.61 |
| HippoRAG2 | 66.28 | 61.98 | 63.08 | 68.05 |
| LightRAG | 63.32 | 61.32 | 63.14 | 67.91 |
| MS-GraphRAG (local) | 38.63 | 47.04 | 41.87 | 53.11 |

All rows: who ran it = Xiang et al. (the benchmark's authors; the GraphRAG methods are third-party code, so not first-party for those methods, first-party for the benchmark); date = v3 20260222; source [20] Table 9. The independent reading of these numbers is in the archive lead (not re-derived). No separate independent study on this benchmark was read.

**Known problems (benchmark).** Single generator; LLM-based metrics (answer accuracy mixes embedding similarity with statement-level checks, weight 0.75) [20].

**Usage evidence.** OpenAlex 4 (arXiv-DOI record, 20261102 20:04); Semantic Scholar: not obtained [53][54].

---

## 21. EnterpriseRAG-Bench

- Slug: `enterpriserag-bench`. Role: **both**. Kinds: `questions`, `corpus`.

### Dataset

**What it contains.** A synthetic company's internal data: about 500,000 documents across nine source types (Slack, Gmail, Linear, Google Drive, HubSpot, Fireflies, GitHub, Jira, Confluence) and 500 questions in ten categories, with noise such as misfiled documents, near-duplicates and conflicting information [21][48].

**Size and versions.** Paper v2 (19 May 2026) Table 9: Slack 285,605; Gmail 121,390; Linear 35,308; Google Drive 25,108; HubSpot 15,017; Fireflies 10,173; GitHub 8,052; Jira 6,120; Confluence 5,189; total 511,962 [21]. Questions: Basic 175, Semantic 125, Intra-Doc Reasoning 40, Project Related 40, Constrained 30, Conflicting Info 20, Completeness 20, Miscellaneous 20, High Level 10, Info Not Found 20 = 500 [21]. Other sources give the total as 511,959 (the BM25 study, 1,144 to 511,959 documents in 28 tiers, 1.7M to 601M tokens) [24] and 511,957 (the archive lead) [55]. The three totals are not reconciled; the study of [24] says its full tier "holds 511,959 documents" after treating some overview pages as scaffolds. Hugging Face metadata last modified 20260508 [48].

**Licence.** The README badge says "Code License MIT" and the repository `LICENSE` is MIT (Copyright 2026 DanswerAI); the Hugging Face metadata lists `mit` for the dataset [48]. The data statement beyond that: **unstated**.

**How it was made.** Human-in-the-loop scaffolding (company overview, initiatives, employee directory, source structure), then LLM generation with cross-document coherence, a realistic volume distribution, noise injected after generation (random and LLM-driven), and internal terminology; questions are created by families that look at the corpus; a three-judge consensus process pools evidence to find missing gold documents [21][48]. The generation framework is released so teams can make their own variants [21].

**Used by.** BM25 Wins at Scale [24]. In the archive: `kb-kg/papers-benchmarks/README.md` only [55].

**Known problems.**
- Synthetic and from one generated company; fit to real enterprise data: **unstated** [21].
- During generation an LLM judge "flagged over 40%" of the items it examined as having a very close sibling (the exact unit and stage are in the paper's generation section, which I read only in part), so the authors added counter-measures [21].
- The study of [24] says questions carry exact lexical anchors and near-miss "trap" documents, which favours lexical matching (that is its claim, not a verified fact about the dataset).
- The publisher (Onyx) sells a RAG product and excludes itself from the leaderboard to avoid a conflict of interest [48].
- Total document count differs between three sources (above).

### Benchmark

**What it tests.** Retrieval and answering over company-internal data: lookups, multi-document reasoning, constrained retrieval, conflict resolution and recognising absent information [21].

**Tasks, metrics and protocol.** Correctness (LLM judge against the gold answer, lenient on style), completeness (fraction of gold facts present), document recall, and "invalid extra documents"; a leaderboard on Hugging Face Spaces; High Level and Info Not Found questions are excluded from the leaderboard because their evaluation criteria differ; submissions need reproducibility and go through the maintainers [21][48].

**Datasets.** `enterpriserag-bench`.

**Results**

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| BM25 | correctness 68.8; completeness 56.0; document recall 68.4; invalid extra docs 9.0 | percent | benchmark authors (Onyx, UC Berkeley) | first-party | v2 20260519 | [21] Table 6 |
| Vector search (text-embedding-3-large) | 51.4; 42.9; 46.0; 9.3 | same | benchmark authors | first-party | 20260519 | [21] Table 6 |
| Bash agent (GPT-5.4, low reasoning) | 60.6; 61.1; 55.8; 2.0 | same | benchmark authors | first-party | 20260519 | [21] Table 6 |
| BM25, official combined score by corpus size | 74.7 at 1,144 documents; 55.2 at 131,876; 50.5 at 511,959 | official combined score (completeness-gated correctness) | Wang et al. (USTC, Metastone) | independent | v3 20260731 | [24] Table 1 |
| File-System Agent | 77.4; 50.9; 30.7 | same | Wang et al. | independent | 20260731 | [24] |
| DenseRAG (Qwen3-Embedding-0.6B) | 58.1; 36.0; 29.9 | same | Wang et al. | independent | 20260731 | [24] |
| HippoRAG 2 | 66.2; 41.0; not built | same | Wang et al. | independent | 20260731 | [24] |
| LinearRAG | 46.2; 29.8; not built | same | Wang et al. | independent | 20260731 | [24] |
| MS-GraphRAG | 45.9 at 1,144 (builds stopped at 8,750 documents) | same | Wang et al. | independent | 20260731 | [24] |
| LightRAG | 48.0 at 1,144 (builds stopped at 2,254 documents) | same | Wang et al. | independent | 20260731 | [24] |

The two studies use different readers (GPT-5.4 versus Qwen3.6-27B) and different scores, so the benchmark paper's table and the scaling study's table are not comparable [21][24].

**Known problems (benchmark).** Single run per question in the scaling study; one reader [24]. Exclusion of the two non-retrieval categories from the leaderboard [48].

**Usage evidence.** OpenAlex 0 (arXiv-DOI record, 20261102 20:04); Semantic Scholar: not obtained [53][54].

---
## 22. Usage evidence: paper citation counts

Counts of the item's paper. OpenAlex via the DOI of the published version when one exists, else the arXiv DOI (the two records differ: for HotpotQA the arXiv-DOI record showed 97 and the ACL record 1,807). Semantic Scholar answered only twice; the API returned HTTP 429 in about 12 rounds of retries (waits of 25 to 45 s) from 19:46 to 20:19 UTC and one batch request at 20:19, so the other rows are empty. Retry later with `https://api.semanticscholar.org/graph/v1/paper/arXiv:<id>?fields=citationCount,title,year`. [53][54]

| Slug | Paper | OpenAlex | Record used (read 20261102 20:03 to 20:04 UTC) | Semantic Scholar (read) |
|---|---|---|---|---|
| natural-questions | Kwiatkowski et al., TACL 2019 | 2,070 | DOI 10.1162/tacl_a_00276 | 5,455 (20:05) |
| triviaqa | Joshi et al., ACL 2017 | 1,651 | DOI 10.18653/v1/p17-1147 | not obtained |
| popqa | Mallen et al., ACL 2023 | 342 | DOI 10.18653/v1/2023.acl-long.546 | not obtained |
| hotpotqa | Yang et al., EMNLP 2018 | 1,807 | DOI 10.18653/v1/d18-1259 (arXiv-DOI record: 97) | not obtained |
| 2wikimultihopqa | Ho et al., COLING 2020 | 279 | DOI 10.18653/v1/2020.coling-main.580 | not obtained |
| musique | Trivedi et al., TACL 2022 | 286 | DOI 10.1162/tacl_a_00475 | not obtained |
| multihop-rag | Tang and Yang, COLM 2024 | 23 | arXiv DOI 10.48550/arxiv.2401.15391 | not obtained |
| simplequestions | Bordes et al., 2015 | 528 | arXiv DOI 10.48550/arxiv.1506.02075 | not obtained |
| webquestionssp | Yih et al., ACL 2016 | 492 | DOI 10.18653/v1/p16-2033 | not obtained |
| complexwebquestions | Talmor and Berant, NAACL 2018 | 520 | DOI 10.18653/v1/n18-1059 | not obtained |
| metaqa | Zhang et al., AAAI 2018 | 490 | arXiv DOI 10.48550/arxiv.1709.04071 | not obtained |
| lc-quad-2 | Dubey et al., ISWC 2019 | 194 | DOI 10.1007/978-3-030-30796-7_5 | 276 (20:08) |
| grailqa | Gu et al., WWW 2021 | 183 | DOI 10.1145/3442381.3449992 | not obtained |
| locomo | Maharana et al., ACL 2024 | 96 | DOI 10.18653/v1/2024.acl-long.747 | not obtained |
| longmemeval | Wu et al., ICLR 2025 | 4 | arXiv DOI (ICLR record not indexed) | not obtained |
| wikipedia-dpr-kilt / DPR paper | Karpukhin et al., EMNLP 2020 | 3,593 | DOI 10.18653/v1/2020.emnlp-main.550 | not obtained |
| kilt | Petroni et al., NAACL 2021 | 357 | DOI 10.18653/v1/2021.naacl-main.200 | not obtained |
| ms-marco | Bajaj et al., 2016 | 1,190 | arXiv DOI 10.48550/arxiv.1611.09268 | not obtained |
| ultradomain / MemoRAG | Qian et al., WWW 2025 | 30 | arXiv DOI 10.48550/arxiv.2409.05591 | not obtained |
| ultradomain / LightRAG (uses its contexts) | Guo et al. | 209 | arXiv DOI 10.48550/arxiv.2410.05779 | not obtained |
| graphrag-bench-xiang | Xiang et al., ICLR 2026 | 4 | arXiv DOI 10.48550/arxiv.2506.05690 | not obtained |
| enterpriserag-bench | Sun et al., 2026 | 0 | arXiv DOI 10.48550/arxiv.2605.05253 | not obtained |

Reading: the old Wikipedia-based QA sets have thousands of citations (NQ, TriviaQA, HotpotQA, DPR); the 2024 to 2026 RAG and memory sets have tens or fewer in OpenAlex, which says they are new, not that they are weak. Use is better shown by who evaluates on them (the "Used by" lines) than by these counts.

---

## 23. Flags for the page writers (conflicts and gaps found)

| # | Item | Flag | Sources |
|---|---|---|---|
| 1 | `natural-questions` | Training size appears as 307,372 and 307,373 in one README; data licence only from a Hugging Face card; official page did not render | [28][29][60] |
| 2 | `triviaqa` | No licence; UW says it does not own the copyright; the GitHub repo named in leads returned 404 | [30] |
| 3 | `popqa` | Row count stated three ways (14k, 14,267, 14,282); no data licence | [2][31] |
| 4 | `2wikimultihopqa` | No data licence; data on Dropbox | [33] |
| 5 | `multihop-rag` | One evidence-count cell differs between paper (1,078/779) and file (1,079/778); publishers' rights unchecked | [6][35][57] |
| 6 | `simplequestions` | Licence only from a third-party Hugging Face mirror | [36] |
| 7 | `webquestionssp` | No licence on the Microsoft page; split sizes not read | [37] |
| 8 | `complexwebquestions` | Project pages unreachable; split sizes only from a derivative copy; no licence | [58][59] |
| 9 | `metaqa` | "Creative Commons Public License" without a variant; KB size not read | [38] |
| 10 | `lc-quad-2` | 30,000 stated, 24,074 in the card's splits; official site refused connection; construction text paywalled | [39] |
| 11 | `locomo` | Non-commercial licence; 10 conversations released against 50 in the paper; 444 QA items without an `answer` key | [13][41] |
| 12 | `longmemeval` | Original release replaced by a "cleaned" release; number of removed sessions unstated | [42] |
| 13 | `ms-marco` | Non-commercial; leaderboard pages script-rendered, rows not read | [45] |
| 14 | `ultradomain` | 3,240 samples (MemoRAG) versus 2,500 (Xiang); `religion` domain in the paper table, no such file in the Hugging Face repo; LightRAG uses its own 125 questions per subset on UltraDomain contexts | [18][19][20][47] |
| 15 | `graphrag-bench-xiang` | 4,076 questions in the paper versus 4,072 in the released files; two unrelated benchmarks share the name | [20][47] |
| 16 | `enterpriserag-bench` | Total documents 511,962 (paper Table 9) versus 511,959 (scaling study) versus 511,957 (archive lead) | [21][24][55] |
| 17 | `wikipedia-dpr-kilt` | CC BY-NC label on the DPR passages versus share-alike Wikipedia text | [43][49] |
| 18 | all KGQA sets | No archive page mentions SimpleQuestions, WebQuestionsSP, ComplexWebQuestions, MetaQA, LC-QuAD, GrailQA, DPR, KILT or MS MARCO; "used by" for them rests on the primary papers only | [55] |

Archive lead corrections found while re-verifying: the lead's RAGSearch row said the Search-R1 versus Graph-R1 pairs were "not labelled by dataset"; the paper's Table 1 does label them (HotpotQA 35.76 versus 53.42; 2Wiki 33.56 versus 66.25; MuSiQue 14.42 versus 40.82) [23][55]. All other Han et al., RAGSearch, BM25-Wins and GraphRAG-Bench numbers copied from the lead matched the papers I re-read (Han et al. Tables 1, 2 and 5; RAGSearch Table 1; BM25 Wins Table 1; GraphRAG-Bench Table 9) [22][23][24][20].

---

## Sources

Numbering is stable within this file. "[n README]", "[n site]", "[n card]" and "[n API]" point to the repository README, project site, Hugging Face card, or Hugging Face/GitHub API part of source n. All times are UTC on 20261102 and come from `date -u "+%Y%m%d %H:%M"` readings taken before and after each group of fetches; where a fetch was not clocked individually, a window of neighbouring readings is given. Downloaded files were kept in their own folder and read as text (PDFs through `pypdf` run with `python3 -I`); no downloaded code was run.

Papers (full text unless noted)

1. https://arxiv.org/abs/1705.03551 : TriviaQA paper v2; construction, sizes, baselines, error analysis (full text via alphaXiv; read 20261102 19:49 to 19:50)
2. https://arxiv.org/abs/2212.10511 : PopQA paper v4; construction, results (alphaXiv full text; 19:49 to 19:50)
3. https://arxiv.org/abs/1809.09600 : HotpotQA paper v1; construction, splits, results (alphaXiv; 19:49 to 19:50)
4. https://arxiv.org/abs/2011.01060 : 2WikiMultiHopQA paper v2; construction, sizes, results (alphaXiv; 19:49 to 19:50)
5. https://arxiv.org/abs/2108.00573 : MuSiQue paper v3; construction, sizes, results (alphaXiv; 19:49 to 19:50)
6. https://arxiv.org/abs/2401.15391 : MultiHop-RAG paper v1; construction, sizes, results (alphaXiv; 19:49 to 19:50)
7. https://aclanthology.org/Q19-1026.pdf : Natural Questions paper (TACL); sizes, collection, baseline table (PDF text; 19:51)
8. https://arxiv.org/pdf/1506.02075 : SimpleQuestions paper v1; construction, KBs, Table 4 (PDF text; 19:50)
9. https://aclanthology.org/P16-2033.pdf : WebQuestionsSP paper; 4,737 parses, Table 1 (PDF text; 19:51)
10. https://arxiv.org/pdf/1803.06643 : ComplexWebQuestions paper v1; construction, Table 4 (PDF text; 19:50)
11. https://arxiv.org/pdf/1709.04071 : MetaQA paper (latest stamp v5); Table 1, Table 4 (PDF text; 19:50)
12. https://arxiv.org/pdf/2011.07743 : GrailQA paper (stamp v6); construction, split, Table 3 (PDF text; 19:50)
13. https://arxiv.org/pdf/2402.17753 : LoCoMo paper v1; pipeline, Tables 2 and 3 (PDF text; 19:50)
14. https://arxiv.org/pdf/2410.10813 : LongMemEval paper v2; construction, abilities, results (PDF text; 19:51)
15. https://arxiv.org/pdf/2004.04906 : DPR paper v3; Wikipedia processing, Table 2 (PDF text; 19:51)
16. https://arxiv.org/pdf/2009.02252 : KILT paper v4; snapshot, datasets, Table 3 (PDF text; 19:51)
17. https://arxiv.org/pdf/1611.09268 : MS MARCO paper v3; construction, sizes (PDF text; 19:51)
18. https://arxiv.org/pdf/2409.05591 : MemoRAG paper v3; UltraDomain appendix C and tables (PDF text; 19:51)
19. https://arxiv.org/pdf/2410.05779 : LightRAG paper v3; evaluation setup, Table 1 (PDF text; 19:51)
20. https://arxiv.org/pdf/2506.05690 : GraphRAG-Bench (Xiang et al.) v3 22 February 2026; construction, Tables 9, 12, 13, 14 (PDF text; 19:51)
21. https://arxiv.org/pdf/2605.05253 : EnterpriseRAG-Bench v2 19 May 2026; Tables 1, 2, 6, 9 (PDF text; 19:51)
22. https://arxiv.org/pdf/2502.11371 : Han et al., RAG vs. GraphRAG v3 4 March 2026; Tables 1, 2, 5 (PDF text; 19:51)
23. https://arxiv.org/pdf/2604.09666 : Fan et al., RAGSearch v1 1 April 2026; Table 1 (PDF text; 19:51)
24. https://arxiv.org/pdf/2607.26497 : Wang et al., BM25 Wins at Scale v3 31 July 2026; Table 1 (PDF text; 19:51)
25. https://arxiv.org/pdf/2610.30755 : Bao et al. v1 22 October 2026; Tables 1 and 3 (PDF text; 19:51)
26. https://arxiv.org/pdf/2504.19413 : Mem0 paper v1; Tables 1 and 2 (PDF text; 19:51)
27. https://arxiv.org/pdf/2501.13956 : Zep paper v1; DMR and LongMemEval tables (PDF text; 19:51)

Repositories, project pages, dataset cards

28. https://github.com/google-research-datasets/natural-questions : README (statistics, format) and `LICENSE` (Apache-2.0) via raw.githubusercontent.com (read 19:48)
29. https://huggingface.co/datasets/google-research-datasets/natural_questions : card (licence CC BY-SA 3.0) and API metadata (19:48 API, 19:52 card)
30. http://nlp.cs.washington.edu/triviaqa/ : project page, WebFetch (20:08 to 20:10); https://huggingface.co/datasets/mandarjoshi/trivia_qa card (licence unknown; copyright sentence) and API (19:48, 19:52)
31. https://github.com/AlexTMallen/adaptive-retrieval : README and MIT `LICENSE` (19:48); https://huggingface.co/datasets/akariasai/PopQA API metadata (19:48) and page via WebFetch (20:08 to 20:10)
32. https://github.com/hotpotqa/hotpot : README (licence statement, files) (19:48); https://hotpotqa.github.io/ : project page and leaderboard via WebFetch (20:05 to 20:07); https://huggingface.co/datasets/hotpotqa/hotpot_qa card (19:52)
33. https://github.com/Alab-NII/2wikimultihop : README (updates, leaderboard) and Apache-2.0 `LICENSE` (19:48)
34. https://github.com/StonyBrookNLP/musique : README (CC BY 4.0, usage caution, leaderboards) and `LICENSE` (19:48)
35. https://github.com/yixuantt/MultiHop-RAG : README (ODC-BY) (19:48); https://huggingface.co/datasets/yixuantt/MultiHopRAG card and API (19:48, 19:52); released `MultiHopRAG.json` and `corpus.json` downloaded and counted by my script (20:11)
36. https://huggingface.co/datasets/fbougares/simple_questions_v2 : card of a mirror (CC BY 3.0) (19:48 API, 19:52 card)
37. https://www.microsoft.com/en-us/download/details.aspx?id=52763 : WebQSP download page via WebFetch (19:53 to 19:55)
38. https://github.com/yuyuz/MetaQA : README (counts, licence sentence, construction) (19:48)
39. https://huggingface.co/datasets/mohnish/lc_quad : card (LC-QuAD 2.0 text, CC BY 3.0, splits) (19:52); https://github.com/AskNowQA/LC-QuAD2.0 : README (19:48) and page via WebFetch (20:08 to 20:10); http://lc-quad.sda.tech/ refused connection (20:07); Springer chapter 10.1007/978-3-030-30796-7_5 paywalled; Semantic Scholar record with elided abstract (20:08)
40. https://github.com/dki-lab/GrailQA : README and Apache-2.0 `LICENSE` (19:48); https://dki-lab.github.io/GrailQA/ : project page (CC BY-SA 4.0, leaderboards) via WebFetch (19:51 to 19:52)
41. https://snap-research.github.io/locomo/ and https://github.com/snap-research/locomo : pages via WebFetch (19:51 to 19:52); `LICENSE.txt` (CC BY-NC 4.0) and `data/locomo10.json` downloaded from raw.githubusercontent.com (19:52) and counted by my script
42. https://github.com/xiaowu0162/LongMemEval : README and MIT `LICENSE` (19:48); https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned : card and API (19:48, 19:52)
43. https://github.com/facebookresearch/DPR : README and CC BY-NC 4.0 `LICENSE` (19:48); https://huggingface.co/datasets/facebook/wiki_dpr : card and API (19:48, 19:52)
44. https://github.com/facebookresearch/KILT : README (knowledge source, files) and MIT `LICENSE` (19:48); https://huggingface.co/datasets/facebook/kilt_wikipedia and https://huggingface.co/datasets/facebook/kilt_tasks : cards and API (19:48, 19:52)
45. https://microsoft.github.io/msmarco/ : site (sizes, changelog, terms) via WebFetch (19:53 to 19:55); https://github.com/microsoft/MSMARCO-Passage-Ranking : README and MIT `LICENSE` (19:48); leaderboard page https://microsoft.github.io/MSMARCO-Passage-Ranking-Submissions/leaderboard/ returned only a title (20:10 to 20:11)
46. (unused number, kept so the other numbers do not move)
47. https://huggingface.co/datasets/TommyChien/UltraDomain : card (Apache-2.0) and file list (19:48, 19:52); https://github.com/qhjqhj00/MemoRAG README (19:48); https://github.com/GraphRAG-Bench/GraphRAG-Benchmark README and MIT `LICENSE` (19:48); https://huggingface.co/datasets/GraphRAG-Bench/GraphRAG-Bench card, file list, and question files downloaded and counted by my script (20:16). (Sources for UltraDomain and GraphRAG-Bench are combined under this number; the text says which.)
48. https://github.com/onyx-dot-app/EnterpriseRAG-Bench : README (categories, leaderboard rules, conflict-of-interest note) and MIT `LICENSE` (19:48); https://huggingface.co/datasets/onyx-dot-app/EnterpriseRAG-Bench API metadata (19:48) and card (19:52)
49. https://dumps.wikimedia.org/legal.html : licences of dump text via WebFetch (20:05 to 20:07)
50. https://arxiv.org/abs/1906.02900 : Min et al., Compositional Questions Do Not Necessitate Multi-hop Reasoning, abstract via WebFetch (20:05 to 20:07)
51. https://arxiv.org/abs/1804.08798 : Petrochuk and Zettlemoyer, SimpleQuestions Nearly Solved, abstract via WebFetch (20:05 to 20:07)
52. https://arxiv.org/abs/2105.04021 : Craswell et al., MS MARCO: Benchmarking Ranking Models in the Large-Data Regime, abstract via WebFetch (20:05 to 20:07)
53. https://api.openalex.org/works/doi:<doi> : citation counts (read 20:03 to 20:04); an earlier arXiv-DOI batch at 19:47 returned some counts and HTTP 429 for others
54. https://api.semanticscholar.org/graph/v1/paper/<id>?fields=citationCount,title,year : two answers (20:05, 20:08); HTTP 429 otherwise
55. Local archive pages (read-only): `kb-kg/papers-benchmarks/README.md` (read in full 19:46 to 19:47) and a text search of `kb-kg/`, `pinakes/`, `DECISIONS.md`, `RESUME.md`, `README.md` (about 20:00)
56. (unused number)
57. `pinakes/experiments/datasets-benchmark.md` : the Pinakes benchmark note (read in full 19:46 to 19:47); its figures are first-party and were not re-run
58. https://huggingface.co/api/datasets/rmanluo/RoG-webqsp , .../rmanluo/RoG-cwq , .../drt/complex_web_questions : metadata of community copies (19:48)
59. https://www.tau-nlp.sites.tau.ac.il/compwebq and https://www.tau-nlp.org/compwebq : both HTTP 404 via WebFetch (19:53 to 19:55)
60. https://ai.google.com/research/NaturalQuestions and .../dataset : WebFetch returned only "Loading..." (19:53 to 19:55; again 20:08 to 20:10)

Not verified in this pass: the Semantic Scholar counts (above); the licences of seed and source texts (SQuAD, T-REx, Gutenberg, NCCN, news publishers, the textbook set behind UltraDomain); `kb-kg/literature/graph-rag-research.md` (not read); results of third-party systems on WebQSP, ComplexWebQuestions, MetaQA, LC-QuAD 2.0 and the MuSiQue leaderboard.
