---
type: dataset
kinds: [questions, corpus]
updated: 20261102 21:38 UTC
---

# UltraDomain

UltraDomain is a set of very long documents, each with high-level questions that need a reading of the whole text. It came out in September 2024 with the MemoRAG paper, which calls it "the UltraDomain benchmark" [1][2]. This page covers contents, sizes, source texts, licence and weak points. It has no benchmark page here: the paper fixes F1 for Fin and Legal and states no metric for Misc, so scores stay in the papers under Used by [2].

## What it contains

Contexts come from 428 college textbooks across 18 domains, from financial reports ("Fin") and from legal contracts ("Legal"); a "Misc" set is described as mixed contexts of the specialised sets [2]. For each context a [large language model](../index/large-language-model.md) (GPT-4) wrote high-level question-answer pairs "that require a comprehensive understanding of the full context" [2]. The repository holds 20 JSON-lines files: 17 textbook domains plus `fin`, `legal` and `mix` [3]. The paper's 18 domains include Religion (no file) and Computer (the repository has `cs`); whether these match is unstated [2][3].

Records carry `input` (the question), `answers`, `context`, `length`, `context_id`, `_id`, `label` and `meta` (five `agriculture.jsonl` records checked) [5]. `mix.jsonl`, read whole, has 130 records over 61 contexts, all labelled `longbench` (musique, 2wikimqa, qasper and others): LongBench-style items, not mixed textbook passages [2][5].

## Size and versions

| Part | Samples | Context length | Source |
|---|---|---|---|
| 18 textbook domains | 3,240 | 32,793 to 1,071,342; average 150,684 | [2] |
| Fin | 345 | average 40,625 | [2] |
| Legal | 438 | average 51,413 | [2] |

No table names the length unit; likely tokens [2][5]. The appendix gives 3,240 samples in total, which equals the textbook total alone, and Xiang et al. list 2,500 questions; unreconciled [2][8]. LightRAG measured four subsets of 10 to 94 documents and 0.6 to 5.1 million tokens [7]. The Hugging Face repository (2.17 GB) was created 20240906 and last changed 20240909 [3][4]. The paper's version 3 is dated 20250409, so a match with the data is unstated [1][4].

## Licence

The dataset card says Apache-2.0 and nothing else; the MemoRAG repository's `LICENSE` file is Apache-2.0 [3][6]. Neither upstream Hugging Face dataset below carries a licence in its metadata, and no source says on what terms the financial reports were obtained [10][11]. *Reading:* the card covers what the authors added; for the source texts the rights are unproven.

## How it was made

Text spans of up to 128K tokens went to GPT-4, which wrote the pairs. Six graduate students kept questions that are "not directly searchable" and judged answer quality, leaving the 3,240 samples the paper reports [2]. References are model-written with a human filter. Source texts, as far as the paper says:

- **Textbooks:** the Hugging Face dataset `P1ayer-1/books-3-textbooks` (Appendix C footnote): 5,437 rows, card text "More Information needed", last changed 20230729. How the 428 were chosen is unstated [2][10].
- **Legal contracts:** Appendix C names no source. Appendix B, on the separate training set, names `albertvillanova/legal_contracts` (placeholder card, last changed 20211210). Use by Legal is unstated [2][11].
- **Financial reports:** Appendix C names no source. In Appendix B the link after "financial reports are from this repository" is the same legal_contracts address, apparently a copied link. Unstated [2].

## Used by

| Paper | Use of UltraDomain | First-party? |
|---|---|---|
| MemoRAG, WWW 2025 ([repository](https://github.com/qhjqhj00/MemoRAG)) [1][2] | Introduced it. Fin and Legal use F1 (Table 3); Misc has no stated metric; the other 18 sets appear in a figure only. Its baselines share one small generator but GraphRAG runs on GPT-4o, so rows are not like for like | yes |
| [LightRAG](../papers/graph-based-rag.md) [7] | Used the contexts, wrote its own questions, judged pairwise with GPT-4o-mini. Win rates: [LightRAG page](../projects/lightrag.md) | yes |
| Xiang et al. [8] | Calls it an existing benchmark with a sparse entity graph: [GraphRAG-Bench (Xiang)](../benchmarks/graphrag-bench-xiang.md) | no, a rival benchmark |

Trend: [graph-based RAG](../trends/graph-based-rag.md). Independent comparison on the released questions: unstated. Citations: 30 (MemoRAG) and 209 (LightRAG) in OpenAlex, read 20261102 20:04 and carried over [9]; the MemoRAG repository had 2,270 stars on 20261102 [6].

## Known problems

- **Two meanings of "on UltraDomain".** LightRAG asked a model for 5 users, 5 tasks per user and 5 questions per task: 125 questions per subset, judged on comprehensiveness, diversity, empowerment and overall [7]. Its score is not a score on the released questions.
- **The Mix file is LongBench items,** unlike the paper's description and LightRAG's ("literary, biographical, and philosophical texts") [2][5][7].
- **Narrow question type, sparse graph.** Xiang et al. class 97% of the questions as "Contextual Summarize" and report 170.6 entities on average and an average degree of 0.86 [8]. They built a competing benchmark, so this is a critique from an interested party.

## Sources

1. https://arxiv.org/abs/2409.05591 : MemoRAG abstract page: "theWebConf 2025", v1 20240909, v3 20250409 (read 20261102 21:34 UTC)
2. https://arxiv.org/html/2409.05591 : MemoRAG v3 full text: section 3.1, Appendices B and C (footnote, source links), Tables 1, 3, 4; "UltraDomain benchmark" wording; generator choice (read 20261102 21:30 UTC)
3. https://huggingface.co/datasets/TommyChien/UltraDomain : dataset card (`license: apache-2.0`, text points to the MemoRAG repository), API metadata, file list (read 20261102 21:34 UTC)
4. https://huggingface.co/api/datasets/TommyChien/UltraDomain/tree/main : file sizes; commit list ending 20240909 (read 20261102 21:04 UTC)
5. https://huggingface.co/datasets/TommyChien/UltraDomain/resolve/main/mix.jsonl : whole file counted; first 4 MB of `agriculture.jsonl` (five complete records) read for fields (read 20261102 21:04 UTC)
6. https://github.com/qhjqhj00/MemoRAG : `LICENSE` Apache-2.0, README dataset pointer, 2,270 stars, last push 20250911 (read 20261102 21:33 UTC)
7. https://arxiv.org/html/2410.05779 : LightRAG v3 (20250428): sections 4.1 and 7.1, Table 4 (subset sizes), question generation, GPT-4o-mini judge (read 20261102 21:34 UTC)
8. https://arxiv.org/html/2506.05690 : Xiang et al. v3 (20260222): introduction, Table 9 and appendix text on question and corpus statistics (read 20261102 21:03 UTC)
9. https://api.openalex.org/works/doi:10.48550/arxiv.2409.05591 and https://api.openalex.org/works/doi:10.48550/arxiv.2410.05779 : citation counts 30 and 209, carried over from the same day's research (read 20261102 20:04 UTC, not re-queried)
10. https://huggingface.co/api/datasets/P1ayer-1/books-3-textbooks : metadata: 5,437 rows, no licence key, card text "More Information needed", last modified 20230729 (read 20261102 21:30 UTC)
11. https://huggingface.co/api/datasets/albertvillanova/legal_contracts : metadata: no licence key, placeholder description, last modified 20211210 (read 20261102 21:30 UTC)
