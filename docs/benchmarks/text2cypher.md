---
type: benchmark
datasets: []
updated: 20261102 21:32 UTC
---

# Text2Cypher

This page answers how well a [language model](../index/large-language-model.md) turns a question and a graph schema into a [Cypher](../index/cypher.md) query, and how the Neo4j Text2Cypher benchmark scores that. Its data are used only inside this benchmark, so they are described here. Every absolute score on the original test split comes from the dataset's owner, except two single-pass runs by an outside team.

## What it tests

Given a natural-language question and the schema of a [property graph](../index/property-graph.md) in a [graph database](../index/graph-database.md), produce the Cypher query that answers it [1]. The paper frames this as a way to reach a [knowledge graph](../index/knowledge-graph.md) without knowing Cypher, and expects the approach to carry over to GQL [1]. The authors are at [Neo4j](../projects/neo4j.md); first version 20241213, published at the GenAIK workshop, January 2025 [1][2].

## Tasks, metrics and protocol

- **Input and output.** Question, schema, reference Cypher, source alias, database alias, index [1][3]. A fixed instruction tells the model to use only the schema's relationship types and properties [1].
- **Translation-based evaluation.** The generated query is compared with the reference as text [1].
- **Execution-based evaluation.** Both queries run on the target database; outputs become strings, sorted, and the same metrics apply. It needs a live database: 2,471 of 4,833 test rows (51.12%) have one [1].
- **Metrics.** Many were computed; the headline pair is Google-BLEU for translation and Exact Match for execution [1].
- **Models.** Table 2 lists 14 benchmarked models (4 previously fine-tuned, 4 open-weight, 6 closed); six were then fine-tuned on the training split [1].

## Datasets

- **Contents and size.** English rows of question, schema and Cypher. 44,387 instances: 39,554 train and 4,833 test (about 89% and 11%). With database access: 22,093 train and 2,471 test [1][3].
- **How it was made.** The authors found 25 resources and used 16 [1]. The Hugging Face card lists 12 sources: synthetic sets from GPT-4o, GPT-4 Turbo, Gemini and Claude Opus over demo databases, a functional Cypher generator, crowdsourced questions, an earlier 2023 Neo4j set, Neo4j's RAG-evaluation sets, three Hugging Face sets and Cy-Spider [3]. Why 16 and 12 differ is unstated. Cleaning: strip back-ticks, drop junk questions, deduplicate on question and Cypher, drop queries that fail `EXPLAIN` on a local Neo4j. Files named "train" went to train, "test" or "dev" to test, the rest split 90:10 [1].
- **Versions.** `text2cypher-2024v1`, created 20240830 [3]. A `2025v1` set was created 20250307; its card holds only a licence and a size band, so its contents are **unstated** [4]. A translated test set (Spanish, Turkish) has 4,783 rows per language after 50 masking failures [9].
- **Licence.** The 2024v1 card says Apache-2.0 [3], as does the translated set [10]. The `neo4j-labs/text2cypher` `LICENSE` file is CC0-1.0 [5]. The upstream sources' own licences are **unstated** on the card [3].

## Results

The main paper's absolute scores are in a figure that was not machine-readable [1]. The rows below are stated in text or tables.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| Llama-3.1-8B-Instruct, fine-tuned on the full training split | translation 0.7585 / 0.3642; execution 0.2534 / 0.2740 | Google-BLEU / Exact Match | M. G. Ozsoy (Neo4j) | yes | 20250508 | [8] |
| Same, 16,173 random rows | translation 0.6971 / 0.2048; execution 0.2121 / 0.2550 | same | same | yes | 20250508 | [8] |
| Same, best hard-example subset (best per column) | translation 0.7140 / 0.2599; execution 0.2473 / 0.2639 | same | same | yes | 20250508 | [8] |
| Same model, multilingual fine-tune, translated test set | 0.86 English, 0.85 Spanish, 0.83 Turkish | ROUGE-L, translation | Ozsoy and Tai (Neo4j) | yes | 20250904 | [9] |
| Fine-tuned GPT-4o and GPT-4o-mini | above 30 percent | Exact Match, execution | Neo4j authors | yes | 20241115 | [7] |
| Six fine-tuned models against their own baselines | change in Google-BLEU / Exact Match, all "about": Gemini-1.0-Pro +0.34 / +0.11; Gemini-1.5-Flash +0.27 / +0.09; GPT-4o-mini +0.20 / +0.06; GPT-4o +0.18 / +0.01; Llama-3.1-8B +0.14 / +0.11; Gemma-2-9B +0.13 / +0.07 | same | Neo4j authors | yes | 20241213 | [1] |
| Claude Sonnet 4, single pass, prompting only | 0.4743 | execution Google-BLEU, 2,471 rows | outside team (LAST-CQ) | no | 20260911 | [11] |
| DeepSeek-Chat, single pass, prompting only | 0.5212 | same | same | no | 20260911 | [11] |
| GPT-4o, GPT-4o-mini, Gemini 1.5 Pro, Gemini 1.5 Flash, prompting only | 0.5270; 0.4180; 0.4100; 0.4018 | execution Google-BLEU, 2,471 rows | Neo4j (Ozsoy et al.) figures, copied by the outside team, not re-run | yes, by origin; the table is the outside team's | original date unstated; copied in a paper of 20260911 | [11] |

*Reading:* the two outside runs are the only results not made by the dataset's owner, and they are prompting-only. They sit above the fine-tuned Llama's execution Google-BLEU of 0.2534 [8], although both use the same name and the same 2,471 rows; the sources do not say why the levels differ. The last row's figures were not re-run: [11] says it takes the Neo4j team's "reported prompting-only figures" and does not name the table or figure. [1] shows its baseline results only in a figure (Figure 4) that was not machine-readable, so the origin of these four numbers is unchecked here. Compare rows within a source only.

## Known problems

- **String metrics.** Google-BLEU and Exact Match penalise equivalent queries. Neo4j's own error analysis lists "wrong ground truth" among five common error groups, finds `MAX` against `ORDER BY` and several valid paths, and plans parse-tree evaluation; it gives no rate of noisy rows [6].
- **Where models fail.** Most on the synthetic sources `functional`, `gemini` and `gpt4o`, and on the recommendations, companies and neoflix databases [6].
- **Overlap metrics.** On the 1,917 model-query pairs that LAST-CQ's correction agent touched (six models pooled, not distinct queries), the outside team finds Google-BLEU above set-based F1 on 65.9% of pairs and below it on 3.1%. Of the same pairs, 230 (12.0%) have an empty reference result, and the benchmark's Google-BLEU credits a non-empty output against an empty reference with 1.0 [11]. The sample is not the whole test split.
- **Leakage.** The paper warns that one question may have two Cypher answers across train and test, that paraphrases may inflate fine-tuned scores, and that public data may enter pre-training [1]. One earlier fine-tuned model had seen 14.4% of the test data [1].
- **Static set against deployment.** A 2026 preprint argues a useful benchmark "reflects the questions users and agents actually ask of that graph" and generates one from a live graph [13].

## Used by

Text2Cypher Across Languages, which translates the questions [9]; a Neo4j study on pruning the training set to hard examples [8]; LAST-CQ, which uses the 2,471 executable rows unmodified and calls it "the only publicly available Text-to-Cypher benchmark with live databases for execution-based evaluation" [11]; Text2GraphQuery-Bench, which draws query patterns from 10 of its 16 databases (4 domains) [12]. See the trend [Asking graphs in natural language](../trends/graph-query-generation.md) and its [papers group](../papers/graph-query-generation.md). Signals: 73 citations for the paper and 3 for the multilingual one (Semantic Scholar, read 20261102 20:00 UTC, carried over, floors) [14]; repository 245 stars, last push 20261009, labelled experimental [5]; 413 downloads on the 2024v1 card, window unstated [3].

## Sources

1. https://arxiv.org/abs/2412.10064 and https://arxiv.org/html/2412.10064 : task, data, cleaning, split, metrics, 14 models, Table 5, risks (read 20261102 21:00 UTC)
2. https://aclanthology.org/2025.genaik-1.11/ : GenAIK 2025, pages 100-108 (read 20261102 21:05 UTC)
3. https://huggingface.co/api/datasets/neo4j/text2cypher-2024v1 and its README : splits, licence, fields, 12 sources, downloads, likes (read 20261102 21:00 UTC; README source table re-read 20261102 21:28 UTC)
4. https://huggingface.co/api/datasets/neo4j/text2cypher-2025v1 and its README : created 20250307, licence line only (read 20261102 21:00 UTC)
5. https://github.com/neo4j-labs/text2cypher : `LICENSE` CC0-1.0, 245 stars, pushed 20261009, experimental (read 20261102 21:05 UTC)
6. https://neo4j.com/blog/developer/text2cypher-model-struggles-dataset-improvements/ : error analysis, 20250303 (read 20261102 21:00 UTC)
7. https://neo4j.com/blog/developer/fine-tuned-text2cypher-2024-model/ : fine-tuned GPT-4o results, 20241115 (read 20261102 21:05 UTC)
8. https://arxiv.org/html/2505.05122v1 : data pruning, Table 1 (read 20261102 21:05 UTC)
9. https://arxiv.org/abs/2506.21445 and https://arxiv.org/html/2506.21445v2 : translated set, 4,783 rows, ROUGE-L (read 20261102 21:04 UTC)
10. https://huggingface.co/api/datasets/mgoNeo4j/translated_text2cypher24_testset : licence apache-2.0 (read 20261102 21:06 UTC)
11. https://arxiv.org/html/2609.12746 : LAST-CQ, Table 2, baseline provenance (copied versus run), the 1,917 pooled pairs, the 65.9% and 230 figures, 20260911 (read 20261102 21:05 UTC; re-read from the PDF 20261102 21:29 UTC)
12. https://arxiv.org/html/2602.11745v2 : Text2GraphQuery-Bench, section 4.2 and Table 1, dataset reuse (read 20261102 21:04 UTC; section 4.2 re-read from the PDF 20261102 21:30 UTC)
13. https://arxiv.org/abs/2606.08481 : PIPE-Cypher abstract, 20260607 (read 20261102 21:01 UTC)
14. Semantic Scholar batch API, `citationCount` for arXiv 2412.10064 (73) and 2506.21445 (3) (read 20261102 20:00 UTC; carried over from that day's research pool, a working file outside the repository; not re-queried; floors)
