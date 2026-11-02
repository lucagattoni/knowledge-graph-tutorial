---
type: benchmark
datasets: []
updated: 20261102 21:06 UTC
---

# CRAG

This page answers what the CRAG benchmark (Comprehensive RAG Benchmark, Meta, 2024) measures, how it is scored, and what the published numbers show. CRAG has no dataset page of its own, because its data is used mainly inside its own protocol (two later papers reuse parts of it, see Known problems and Used by); the data is described below. Its paper has 160 citations (Semantic Scholar, read 20261102 20:01 UTC) [11].

## What it tests

It tests whether a [retrieval-augmented generation](../index/retrieval-augmented-generation.md) system answers factual questions correctly and says "I don't know" instead of inventing an answer. Questions span five domains, popular and rare entities, and answers that change in seconds or stay fixed for years. Retrieval comes from two sources at once, web pages and [knowledge-graph](../index/knowledge-graph.md) APIs; the authors say [Natural Questions](natural-questions.md), [MS MARCO](ms-marco.md) and [TriviaQA](../datasets/triviaqa.md) use only one [1].

## Tasks, metrics and protocol

- **Task 1:** answer from up to five web pages. **Task 2:** add mock knowledge-graph APIs. **Task 3:** 50 pages plus the APIs, so ranking matters. All three share the same questions [1].
- **Score:** perfect 1, acceptable 0.5, missing 0, incorrect -1; "truthfulness" is the mean. Auto-eval merges perfect and acceptable (1 / 0 / -1) and averages two [LLM judges](../index/llm-as-judge.md), gpt-3.5-turbo-0125 and Llama 3 70B, which agree with human grading at F1 94.7% and 98.9% [1]. The repository's evaluator uses the 1 / 0 / -1 scheme [2].
- **Splits:** validation 30%, public test 30%, private 40%. Only the first two are released (2,706 examples); the private part decided the KDD Cup 2024 winners [1].

## Datasets

**Contents.** 4,409 question-answer pairs: finance 1,039, sports 833, music 624, movie 1,125, open 788. Eight question types, from simple (1,205) to [multi-hop](../index/multi-hop-question-answering.md) (382) and false premise (525). Answers are real-time (437), fast-changing (564), slow-changing (1,007) or static (2,401). 2,425 questions come from web content and 1,984 from knowledge graphs [1]. Retrieval content: up to 50 stored HTML pages per question from the Brave Search API (220K pages in all), mock graphs with 2.6 million entities, and 38 mock APIs [1].

**Made.** Graph questions: 600+ templates filled with entities sampled by popularity. Web questions: annotators wrote user-style questions and built answers from search results. Questions were paraphrased; ground truths were checked by hand [1].

**Versions.** Paper v1 20240607, v2 20241101 [1]. The repository files are named `dev_v4`; how that maps to the paper's release is unstated [3]. Last push 20250614 [4].

**Licence.** The LICENSE file is CC BY-NC 4.0; GitHub reports "Other" [2][4]. Non-commercial, so a read-only reference for this project.

## Results

Three scales appear; rows are comparable only within a block.

| System | Score | Metric, set | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| GPT-4 Turbo, no retrieval | accuracy 33.5, hallucination 13.5, truthfulness 20.0 | auto-eval, public test (1,335 questions) | CRAG authors | yes | 20241101 | [1] |
| GPT-4 Turbo / Llama 3 70B Instruct, Task 3 | 43.6, 30.1, 13.4 / 40.6, 31.6, 9.1 | same | CRAG authors | yes | 20241101 | [1] |
| Copilot Pro | truthfulness 50.6 (60.5 traffic-weighted) | human eval, products queried 20240512 to 20240702 | CRAG authors | yes (third-party products) | 20241101 | [1] |
| Gemini Advanced; ChatGPT Plus; Meta SG; Perplexity.ai | 49.3 (59.3); 41.5 (41.8); 41.4 (50.5); 34.9 (45.9) | same | CRAG authors | yes | 20241101 | [1] |
| Team db3, first on all three tasks | 28.4 / 42.7 / 47.8 (Tasks 1 / 2 / 3) | score as reported by the team; scale and test set not defined in the paper | the team | independent of the authors; first-party for its system | 20240913 | [5][6] |
| CacheRAG; re-runs of apex and db3 | truthfulness 0.711; 0.536; 0.379 | KG questions only (578; the paper calls them the CRAG KG "private testing set", which split that is, is unstated), no web pages; all three on a DeepSeek-V3-0324 base, web input of apex and db3 set to "<EMPTY>" | CacheRAG authors | two authors share names with CRAG authors; same people unstated | 20260428 (v4 20260608) | [7] |

*Reading:* retrieval alone did not make answers trustworthy. For GPT-4 Turbo it raised accuracy from 33.5 to 43.6 but cut truthfulness from 20.0 to 13.4, because hallucinations rose [1]. The authors warn that industry and straightforward rows are not fully comparable (different retrieval access; human against auto-eval) [1]. The 2026 row uses a subset without web pages, and apex and db3 there are not the KDD Cup systems as submitted, so it says little about the whole [7].

## Known problems

- **Retrieval left out.** The tasks do not test first-stage retrieval over the whole corpus; the 220K pages can serve as a corpus, but "does not match the entire web" [1].
- **Incomplete coverage.** Estimated web recall is 85% with 50 pages and about 69% with five; the paper says this lets it test whether systems admit "I don't know". In straightforward runs, over 30% of questions had the answer in the results but cut by the context window [1]. *Reading:* some wrong answers therefore reflect missing evidence, not a weak reader.
- **Hidden final test.** The private 40% is not released; the KDD Cup scale is undefined in the sources read, and the AIcrowd page gives podiums without scores [5][6]. CacheRAG calls its 578-question set the "private testing set"; which split that is, is unstated [7].
- **Misuse.** One 2025 paper builds its knowledge graph from the CRAG question-answer pairs and compares with the 63% that the CRAG paper gives for industry systems; that is not a like-for-like result [1][10].
- **Name clashes.** "CRAG" is also Corrective Retrieval Augmented Generation, an unrelated method [9]. CRAG-MM (October 2025) is a multimodal, multi-turn successor from some of the same authors, used for KDD Cup 2025 [8].

## Used by

KDD Cup 2024 entrants, among them db3 [5] and APEX (second on Tasks 2 and 3) [12]; CacheRAG, which also reports [WebQSP](webquestionssp.md) [7]. Entries that write API calls for the graph relate to [Asking graphs in natural language](../trends/graph-query-generation.md).

## Sources

1. https://arxiv.org/html/2406.04744 : CRAG paper v2 (20241101): data, tasks, scoring, Tables 3 to 6, Section 4 recall estimate, Appendix A.2.3, A.4.1, A.5 (read 20261102 21:28 UTC)
2. https://raw.githubusercontent.com/facebookresearch/CRAG/main/README.md and https://raw.githubusercontent.com/facebookresearch/CRAG/main/LICENSE : evaluator, CC BY-NC 4.0 (read 20261102 20:54 UTC)
3. https://raw.githubusercontent.com/facebookresearch/CRAG/main/docs/dataset.md : files `dev_v4`, schema, query time (read 20261102 21:28 UTC)
4. GitHub API for facebookresearch/CRAG : licence "Other", last push 20250614 (read 20261102 20:54 UTC)
5. https://arxiv.org/abs/2410.00005 : db3 winning solution, scores 28.4 / 42.7 / 47.8, no scale or leaderboard named in the text (read 20261102 21:28 UTC)
6. https://www.aicrowd.com/challenges/meta-comprehensive-rag-benchmark-kdd-cup-2024/winners : podiums per task, no scores (read 20261102 20:55 UTC)
7. https://arxiv.org/html/2604.26176v4 : CacheRAG v4, Table 1, Appendix A.1 and A.3 (read 20261102 21:28 UTC)
8. https://arxiv.org/abs/2510.26160 : CRAG-MM abstract (read 20261102 20:55 UTC)
9. https://arxiv.org/abs/2401.15884 : Corrective Retrieval Augmented Generation abstract (read 20261102 20:56 UTC)
10. https://arxiv.org/html/2510.19181v1 : graph built from the question-answer pairs, 63% comparison (read 20261102 20:56 UTC)
11. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 160 for arXiv 2406.04744 (read 20261102 20:01 UTC, carried over from the research notes)
12. https://arxiv.org/abs/2409.15337 : APEX, second on Tasks 2 and 3 (read 20261102 20:56 UTC)
