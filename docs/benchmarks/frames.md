---
type: benchmark
datasets: []
updated: 20261102 21:27 UTC
---

# FRAMES

This page answers what FRAMES measures, how its 824 questions were made, and what the published scores show. FRAMES has no dataset page, because its data is used only inside its own protocol; the data is described below. Its paper has 211 citations (Semantic Scholar, read 20261102 20:01 UTC) [8]. The only end-to-end scores found are first-party.

## What it tests

[Retrieval-augmented generation](../index/retrieval-augmented-generation.md) end to end: factuality, retrieval and reasoning in one score, where earlier sets such as [HotpotQA](hotpotqa.md) and [MuSiQue](musique.md) test them apart [1]. It appeared at NAACL 2025 [1][2].

## Tasks, metrics and protocol

- **Task.** Answer a free-form question that needs 2 to 15 Wikipedia articles [1].
- **Metric.** Accuracy, judged by an LLM that compares the answer with the gold one. Against human grading it scored 0.96 accuracy and Cohen's kappa 0.889, with Gemini-Pro-1.5-0514 as judge ([LLM-as-judge](../index/llm-as-judge.md)) [1].
- **Settings.** Naive prompt (no retrieval); [BM25](../index/bm25.md) retrieval of 2 or 4 articles; oracle prompt with all gold articles, which the authors call the upper bound; and a multi-step loop in which the model writes k queries per step for n steps, each returning n_docs BM25 articles from a Wikipedia dump whose date is **unstated** [1].

## Datasets

**What it contains.** 824 questions, each with a gold answer and the list of articles needed. About 36% need two articles, 35% three, 16% four. Reasoning types: multiple constraints (about 36%), numerical (about 20%), tabular, temporal, post-processing; a question can have several [1].

**How it was made.** LLM-written questions were tried first and dropped: over 30% were hallucinated. Vetted human annotators then wrote the questions. Three months later the answers were re-checked and 5.5% were removed as no longer true. Questions were anchored to a date ("As of August 1, 2024") and yes/no questions were removed [1].

**Licence and versions.** The card header says `apache-2.0`; the repository holds only the card, `test.tsv` and `.gitattributes`, so no licence file backs it. The terms of the linked Wikipedia text are **unstated**. One release; paper v1 20240919, v3 20250124; card last modified 20241015 [1][3][4].

## Results

Accuracy on all 824 questions unless stated. Gemma2-27b, Llama3.2-3B and Qwen2.5-3B score 0.308, 0.115 and 0.095 with the naive prompt [1].

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Gemini-Pro-1.5-0514: naive; BM25 2 docs; BM25 4 docs; oracle | 0.408; 0.452; 0.474; 0.729 | accuracy | FRAMES authors | yes | 20250124 (v3) | [1] |
| Same model, multi-step (k, n, n_docs = 5, 5, 10) with search-planning instructions | 0.66 | accuracy | FRAMES authors | yes | 20250124 | [1] (Figure 4 caption; model from the Figure 3(b) caption) |
| Gemini-Flash-1.5-0514: naive; BM25 4 docs; oracle | 0.263; 0.315; 0.665 | accuracy | FRAMES authors | yes | 20250124 | [1] |
| BM25-and-grep agent harness, MiniMax M3 | 91% | accuracy, LLM judge | RAGFlow team | yes, for RAGFlow | 20261030 | [5][7] |
| Same harness plus RAPTOR-style tree, PageIndex-style outline, LLM wiki or entity graph | no detectable gain; the outline "harmful at FRAMES scale" | accuracy against the plain harness | RAGFlow team | yes | 20261030 | [5] |
| Three LLMs given the linked articles, 81 questions | 97.5% to 98.8% | Avg@3 accuracy | Tao et al. (Tencent, Peking University) | no | 20260929 | [6] |

The [RAGFlow](../projects/ragflow.md) project is the repository `infiniflow/ragflow` [7]; the paper's authors are mostly at InfiniFlow Inc. (infiniflow.ai addresses) and say the system is implemented in that project [5]. Its figures come from single runs with no confidence intervals; its token results use 200 questions, and the sample behind the 91% is **unstated** [5]. The authors built the outline themselves and did not use the PageIndex SDK [5]. No leaderboard exists in the paper, card or repository files [1][3].

*Reading:* a first-party agentic harness with a newer model passes the 2024 oracle score (0.729). Model, judge and sample differ from the paper, so the gap is not due to the loop alone, and no independent confirmation was found.

## Known problems

- **Contamination and coverage.** Wikipedia text may be in training data, and the questions may not match real queries [1].
- **Answers expire.** They are tied to a stated date, and 5.5% already failed after three months [1].
- **Judge dependence.** Scores rest on an LLM autorater; the 2026 study names only "an LLM judge" [1][5].
- **Weak hop dependence.** Tao et al. removed one inferred reasoning step at a time from 81 questions with their articles supplied. Removing one step's evidence stopped a correct answer in only 6.6% to 8.1% of cases. The cohort is selected, has entity answers only, and caps articles at 24,000 characters; it is not the full set [6].
- **Card errors.** The card lists `size_categories: n>1T` and the title "Who are I or you" [3].

## Used by

The RAGFlow study above, which compares a [PageIndex](../projects/pageindex.md)-style outline; it is cited on the [reasoning-over-structure](../trends/reasoning-over-structure.md) and [agentic-search](../trends/agentic-search.md) trend pages. Papers: [agentic search](../papers/agentic-search.md).

## Sources

1. https://arxiv.org/html/2409.12941 : FRAMES paper v3: construction, statistics, Table 3, Figures 3 and 4 captions, Algorithm 1, limitations (read 20261102 20:53 UTC; captions re-read 20261102 21:24 UTC)
2. https://arxiv.org/abs/2409.12941 : submission history, NAACL 2025 note (read 20261102 20:53 UTC)
3. https://huggingface.co/datasets/google/frames-benchmark/raw/main/README.md and https://huggingface.co/api/datasets/google/frames-benchmark : card, file list, dates (read 20261102 20:53 UTC)
4. Same API record: created 20240919, last modified 20241015 (read 20261102 20:53 UTC)
5. https://arxiv.org/html/2610.41172 and https://arxiv.org/abs/2610.41172 : Yu et al. (RAGFlow team), v1 20261030: 91%, Table 3, sample sizes, limits, author affiliations and the RAGFlow footnote (read 20261102 20:56 UTC; affiliations re-read 20261102 21:24 UTC)
6. https://arxiv.org/html/2609.36984 : Tao et al., RealHop, v1 20260929: section 6.2, appendix I.4 (read 20261102 20:57 UTC)
7. https://api.github.com/repos/infiniflow/ragflow : repository identity only: the name infiniflow/ragflow (read 20261102 20:58 UTC)
8. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 211 (read 20261102 20:01 UTC, carried from the dataset and benchmark candidate pool)
