---
type: dataset
kinds: [questions]
benchmark: lc-quad
updated: 20261102 21:29 UTC
---

# LC-QuAD

This page answers what the two LC-QuAD sets contain, how large they are, who may use them, and how they were made. LC-QuAD 1.0 (2017) pairs 5,000 questions with [SPARQL](../index/sparql.md) queries over [DBpedia](dbpedia.md) [1]; LC-QuAD 2.0 (2019) has about 30,000 over [Wikidata](wikidata.md) and DBpedia [2]. Scores and protocols are on [the LC-QuAD benchmark page](../benchmarks/lc-quad.md).

## What it contains

Every item is an English question and the SPARQL query that answers it. The target graph is not shipped: a user must host the right DBpedia or Wikidata version [1][2][3].

- **LC-QuAD 1.0** items carry a corrected final question, an automatically generated "intermediary question", a template id and the query [3]. 18% of the questions are simple (one triple); 18.06% use COUNT and 9.57% are boolean; there is no OPTIONAL or UNION [1].
- **LC-QuAD 2.0** items carry the template question (NNQT), a crowdsourced verbalisation, a paraphrase of it, and queries for Wikidata and for DBpedia 2018 [2][7]. There are ten question types, among them qualifier facts, two-intention, boolean, count, ranking, string operation and temporal. The paper calls it the first dataset to use Wikidata qualifiers [2].

## Size and versions

| | LC-QuAD 1.0 | LC-QuAD 2.0 |
|---|---|---|
| Questions | 5,000 [1] | "30,000" in the paper [2]; 30,226 in later papers [9][10] |
| Split | 4:1 train and test, that is 4,000 and 1,000 [3][17] | 24,180 train and 6,046 test [8][9] |
| Entities, relations | 5,042 entities, 615 predicates [1] | 21,258 entities, 1,310 relations [2] |
| Templates | 38 [1] | 22 in the paper [2]; 30 in a later count [11] |
| Target graph | DBpedia 2016-04 [1][3] | Wikidata and DBpedia 2018 [2] |
| Released | 20170501 first version; train and test files 20180619 [3] | 20190412 full file; train and test files 20190702 [6] |

Papers disagree on how many 2.0 rows are usable. A Hugging Face mirror loads 19,293 train and 4,781 test rows, 24,074 in all, and gives no reason [7]. Another count is 30,225 [11]. One study dropped 2,502 rows (8.2%) of 30,226 for quality [9]. Another dropped invalid or slow queries and test queries with no result on an August 2023 Wikidata dump, leaving 21,504 train and 5,361 test rows [10]. A derived set, LC-QuAD 3.0, adds frame annotations to 2.0 [11].

## Licence

The licence differs between the places the authors published the data.

| Set | Statement | Where |
|---|---|---|
| 1.0 | CC BY 4.0 | figshare records, read now [5]; the paper says the same [1] |
| 1.0 | GPL-3.0: "released with a GPL 3.0 License", with a `LICENSE.txt` of GPL-3.0 | GitHub README and file, `data` branch [3] |
| 2.0 | CC BY 4.0 | figshare records, read now [6]; the paper says the same [2] |
| 2.0 | CC BY 3.0 | Hugging Face mirror card [7] |
| 2.0 | no `LICENSE` file; the README is one sentence | GitHub [4] |

*Reading:* the authors' figshare records and papers say CC BY 4.0 for both sets, the best-supported answer. Because 1.0 also carries a GPL-3.0 statement, this documentation treats it as a read-only reference and quotes no questions or queries.

## How it was made

**1.0.** The authors chose seed entities and a whitelist of 615 DBpedia predicates, cut a two-hop subgraph around each seed, and filled SPARQL templates from it. Each query became a template question; three authors corrected its grammar and an independent reviewer checked every one. Correction took about 48 seconds a question and review about 20, against about 94 to verbalise a bare query [1].

**2.0.** Seed entities come from Wikipedia "Vital articles" (level 5), to avoid too many people [2]. Queries are filled from templates and turned into template questions by rule. Crowd workers on Amazon Mechanical Turk verbalise each one, paraphrase the verbalisation, and check both steps [2].

## Used by

- **Papers.** Query-building studies [8], a ChatGPT and GPT-4 comparison on 26,975 questions of 2.0 [12], an agentic text-to-SPARQL paper on 826 of them [13], and an entity-linking study [9]. Semantic Scholar citation counts (read 20261102 20:00 UTC, carried over from the research notes, not re-queried): 308 for 1.0 and 276 for 2.0 [14]. See [the query-generation papers](../papers/graph-query-generation.md).
- **Trend.** [Asking graphs in natural language](../trends/graph-query-generation.md).
- **Benchmark.** [LC-QuAD](../benchmarks/lc-quad.md); a community board lists 76 rows for 1.0 [15].
- **Challenge.** The TEXT2SPARQL challenge supplied "LC-QuAD" (cited as Trivedi et al. 2017, that is 1.0) as an example pool, "a template-generated KGQA corpus" [16].
- **Related sets.** The papers compare with [WebQuestionsSP](webquestionssp.md), [ComplexWebQuestions](complexwebquestions.md) and [SimpleQuestions](simplequestions.md) [1][2].

## Known problems

- **The target graph moved.** The public DBpedia endpoint no longer serves 2016-04, so many 1.0 queries return nothing and the maintainers advise a local copy [3]. For 2.0, the original Wikidata dump is gone; only 4,211 of the 6,046 test queries still returned an answer on a 2021 dump [8].
- **Template structure repeats.** In 1.0, every query structure in the test set also occurs in the training set [17].
- **Crowd text is uneven.** Null, empty or "NA" questions, questions that copy the template text, and questions that give the answer away were found in 2.0 [9]. Another study saw misspellings and poor fluency [10].
- **No working official site.** The project website `lc-quad.sda.tech`, linked from the 1.0 README [3], failed to connect on 20261102 20:48 and 21:26 UTC [18]; the 2.0 construction detail rests on the paper alone.
- **Memorisation.** Whether language models saw the 2.0 text: **unstated**; one study flags it as possible [10].

## Sources

1. http://jens-lehmann.org/files/2017/iswc_lcquad.pdf : LC-QuAD 1.0 paper (Trivedi, Maheshwari, Dubey, Lehmann; ISWC 2017), full text: size, statistics, workflow, figshare CC BY 4.0 (read 20261102 20:42 UTC)
2. http://jens-lehmann.org/files/2019/iswc_lcquad2.pdf : LC-QuAD 2.0 paper (Dubey, Banerjee, Abdelkawi, Lehmann; ISWC 2019), full text: abstract, workflow, statistics, question types, CC BY 4.0 (read 20261102 20:42 UTC)
3. https://github.com/AskNowQA/LC-QuAD : `data` branch README (80:20 split; changelog 0.1.0 of 20170501 and 0.1.3 of 20180619; link to the website), `LICENSE.txt` (GPL-3.0); GitHub API: 98 stars, last push 20230905 (README re-read 20261102 21:25 UTC; other items read 20:41 UTC)
4. https://github.com/AskNowQA/LC-QuAD2.0 : README (one sentence), file list, no LICENSE (404 from the licence endpoint) (read 20261102 21:25 UTC)
5. https://api.figshare.com/v2/articles/5006084 : LC-QuAD 1.0 question file `data_set.json`, CC BY 4.0, published 20171023; the same endpoint for the other five articles of the project (ids 5006090, 5008283, 5008286, 5311399, 5818452): each CC BY 4.0 (read 20261102 21:22 UTC)
6. https://api.figshare.com/v2/articles/7988147 : LC-QuAD 2.0 full file `lcquad_2_0.json`, CC BY 4.0, published 20190412; the same endpoint for ids 8479055 (train) and 8479052 (test): CC BY 4.0, published 20190702 (read 20261102 21:22 UTC)
7. https://huggingface.co/datasets/mohnish/lc_quad : card (fields, splits 19,293 and 4,781, `cc-by-3.0`) and API metadata (read 20261102 20:41 UTC)
8. https://arxiv.org/pdf/2204.12793 : Banerjee et al., "Modern Baselines for SPARQL Semantic Parsing", SIGIR 2022, v3 of 20230914: Section 4 datasets (4:1, 24,180 and 6,046), Section 5 (4,211) (re-read 20261102 21:23 UTC)
9. https://arxiv.org/pdf/2107.02865 : Diomedi and Hogan, v1 of 20210706: quality issues, 2,502 of 30,226 dropped (read 20261102 20:44 UTC)
10. https://ceur-ws.org/Vol-4108/paper4.pdf : Labate et al., Wikidata workshop at ISWC 2025, published 20251125: Section 3.1.1 (read 20261102 20:46 UTC)
11. https://arxiv.org/pdf/2503.22144 : FRASE, v1 (20250328): Table 1, LC-QuAD 3.0 (read 20261102 20:45 UTC)
12. https://arxiv.org/pdf/2303.07992 : Tan et al., v3 of 20230920: Table 2, collected size 26,975 (re-read 20261102 21:24 UTC)
13. https://arxiv.org/pdf/2607.14494 : SAGA, v1 of 20260716: Datasets paragraph, 826 test questions (re-read 20261102 21:26 UTC)
14. https://api.semanticscholar.org/graph/v1/paper/batch?fields=citationCount : citationCount for DOIs 10.1007/978-3-319-68204-4_22 (308) and 10.1007/978-3-030-30796-7_5 (276), read 20261102 20:00 UTC via the research notes of this documentation; not re-queried
15. https://raw.githubusercontent.com/KGQA/leaderboard/gh-pages/dbpedia/lcquad.md : community board, 76 table rows for 1.0; last commit touching it 20230430 (read 20261102 20:42 UTC)
16. https://arxiv.org/pdf/2512.14277 : SPARQL-LLM, Section 4.1.1 and reference [34] (Trivedi et al. 2017) (re-read 20261102 21:25 UTC)
17. https://arxiv.org/pdf/2502.03992 : Jiang et al. (2025), Table II (LC-QuAD 1.0: 4,000 train, 1,000 test) and Table III (22 train and 21 test structures, 0 unseen in test) (re-read 20261102 21:24 UTC)
18. http://lc-quad.sda.tech/ : failed to connect, port 80 (tried 20261102 20:48 and 21:26 UTC)
