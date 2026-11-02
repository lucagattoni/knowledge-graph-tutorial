---
type: dataset
kinds: [questions, corpus]
benchmark: 2wikimultihopqa
updated: 20261102 21:25 UTC
---

# 2WikiMultiHopQA

2WikiMultiHopQA is a set of 192,606 [multi-hop questions](../index/multi-hop-question-answering.md) over Wikipedia article summaries, each with the [triples](../index/triple.md) from [Wikidata](wikidata.md) that give its reasoning path [1]. Its first arXiv version is dated 20201102 [2]. This page describes the data: what is in it, how big it is, who may use it, and how it was made. Its evaluation (tasks, metrics, results) is on [the benchmark page](../benchmarks/2wikimultihopqa.md).

## What it contains

- **Questions.** Four types, all generated from hand-written templates: comparison, inference, compositional and bridge-comparison [1]. An inference question uses a logical rule over two facts ("Who is the maternal grandfather of Abraham Lincoln?"); a compositional question chains two relations that have no such rule [1].
- **Context.** Ten paragraphs per question: the gold ones plus distractors. Each paragraph is the short summary at the top of a Wikipedia article [1].
- **Supporting facts.** The sentences the answer comes from, in the format of [HotpotQA](hotpotqa.md) [1][3].
- **Evidence.** A list of Wikidata triples (subject, relation, object) that spell out the reasoning path. This is what the paper adds over HotpotQA [1].
- **Later fields.** `evidences_id` and `answer_id` (Wikidata identifiers) on 20201208; every article's hyperlink mentions on 20210407 [3].

So the data has three layers: a question set, a text corpus, and Wikidata evidence triples per question.

## Size and versions

| Part | Count | Source |
|---|---|---|
| Examples (total) | 192,606 | [1] Table 1 |
| train-medium / train-hard | 154,878 / 12,576 | [1] |
| dev / test | 12,576 / 12,576 | [1] |
| Comparison / inference / compositional / bridge-comparison | 57,989 / 7,478 / 86,979 / 40,160 | [1] Table 2 |
| Source dumps | English Wikipedia of 20200101; Wikidata of 20191231; 5,950,475 entities | [1] Appendix A.1 |

Yes/no answers are 31.2% of all answers [1]. Releases: 20201208 (identifiers, evaluation script v1.1) and 20210407 (fixed sentence segmentation, hyperlink file); the files are linked from Dropbox [3]. A Hugging Face copy, `xanhho/2WikiMultihopQA`, calls itself an "official mirror" [5]; who owns that account is unstated.

## Licence

**Data licence: unstated.** The evidence:

- The repository `LICENSE` is Apache-2.0 [4]. The README names no licence for the data [3].
- The paper is CC BY 4.0, which covers the paper text [1].
- The Hugging Face copy tags `apache-2.0` [5]; that is a third-party label, not the authors' statement.
- The sources underneath have their own terms: Wikipedia text is CC BY-SA 4.0 and GFDL [6]; Wikidata structured data is CC0 [7]. Whether the share-alike term reaches this dataset is unstated in the sources read.

## How it was made

1. **Templates.** Comparison templates come from [named-entity-recognition](../index/named-entity-recognition.md) tags on the 17,456 comparison questions in HotpotQA's training set, rewritten by hand for the 50 most popular entity types. There are 799 compositional and 62 bridge-comparison templates [1].
2. **Facts.** Entities and relations come from Wikidata, and the answer must appear in the Wikipedia summary. The authors kept properties they judged consistent between Wikipedia and Wikidata and checked doubtful cases by hand; a later check still found mismatches (see Known problems) [1].
3. **Rules.** Inference questions use 28 logical rules found with the AMIE rule-mining system and checked by hand [1].
4. **Distractors.** Eight per question (six for bridge-comparison), picked from the top 50 [tf-idf](../index/tf-idf.md) results by entity type [1].
5. **Splits.** A single-hop model cut the data: questions it solved became train-medium; the rest were split into train-hard, dev and test. Yes and no answers were balanced and ambiguous questions dropped [1].

## Used by

- **Projects (paper experiments).** [HippoRAG 2](../papers/graph-based-rag.md) draws 1,000 random 2Wiki queries [11]. Graph-R1 lists it among six datasets [13]; LinearRAG, LogicRAG and Youtu-GraphRAG among three multi-hop sets [14][15][17]; MiniRAG in the ACL 2026 version only, not in arXiv v3 [16]. Archive pages: [Graph-R1](../../kb-kg/projects/graph-r1.md), [LinearRAG](../../kb-kg/projects/linearrag.md), [LogicRAG](../../kb-kg/projects/logicrag.md), [MiniRAG](../../kb-kg/projects/minirag.md), [Youtu-GraphRAG](../../kb-kg/projects/youtu-graphrag.md); project page [HippoRAG](../projects/hipporag.md).
- **Trends.** [Graph-based RAG](../trends/graph-based-rag.md) and [learned graph traversal](../trends/learned-graph-traversal.md) (Graph-R1 trains a retrieval agent) [13].
- **Benchmarks.** [2WikiMultiHopQA](../benchmarks/2wikimultihopqa.md); [RAGSearch](../benchmarks/ragsearch.md), which uses the full dev set [9]; [GraphRAG-Bench (Xiang)](../benchmarks/graphrag-bench-xiang.md), for corpus statistics [10].
- **Datasets.** The [MuSiQue](musique.md) paper compares itself with this set [8].
- **Usage signal.** 279 citations of the paper in OpenAlex, one source on one day [12].

## Known problems

- **Templates.** Questions come from a limited rule set. The MuSiQue authors say hand-authored composition rules make it "easy for large language models" [8].
- **Few inference questions.** Only 7,478, because the authors kept relations with a single Wikidata value [1].
- **Wikipedia and Wikidata disagree.** In a hand check of 100 training samples, eight had a mismatch between the article and the triple [1].
- **Sparse entity graph.** In the corpus statistics of Xiang et al., this set has an average node degree of 0.64 and 0.40 of entities non-isolated, against 2.27 and 0.66 for GraphRAG-Bench (novel), a set built for graph methods [10].
- **Pretraining overlap with Wikipedia: unstated.**

## Sources

1. https://arxiv.org/pdf/2011.01060 : paper v2 (Ho, Nguyen, Sugawara, Aizawa; COLING 2020): contents, construction, sizes, question types, mismatch check, templates (read 20261102 20:41 UTC; Appendix A.1 and Section 5.4 re-read 20261102 21:22 UTC)
2. https://export.arxiv.org/api/query?id_list=2011.01060 : arXiv record, first version published 20201102, v2 20201112 (read 20261102 21:21 UTC)
3. https://raw.githubusercontent.com/Alab-NII/2wikimultihop/main/README.md : fields, updates 20201208 and 20210407, Dropbox links (read 20261102 21:17 UTC)
4. https://github.com/Alab-NII/2wikimultihop/blob/main/LICENSE : Apache-2.0, confirmed by the repository metadata via the GitHub API (read 20261102 20:44 UTC)
5. https://huggingface.co/datasets/xanhho/2WikiMultihopQA : card text and `apache-2.0` tag (read 20261102 20:44 UTC)
6. https://en.wikipedia.org/wiki/Wikipedia:Copyrights : CC BY-SA 4.0 and GFDL for Wikipedia text (read 20261102 20:44 UTC)
7. https://www.wikidata.org/wiki/Wikidata:Licensing : structured data is CC0 (read 20261102 20:44 UTC)
8. https://arxiv.org/pdf/2108.00573 : MuSiQue paper v3, related-work sentence on 2Wiki (read 20261102 20:41 UTC)
9. https://arxiv.org/pdf/2604.09666 : RAGSearch v1 (20260401), Appendix A (read 20261102 20:41 UTC)
10. https://arxiv.org/html/2506.05690v3 : Xiang et al. v3 (20260222), corpus-statistics table in Appendix E (read 20261102 21:21 UTC)
11. https://arxiv.org/pdf/2502.14802 : HippoRAG 2 v2 (20250619), setup text (read 20261102 20:43 UTC)
12. OpenAlex count 279 for DOI 10.18653/v1/2020.coling-main.580 (read 20261102 20:04 UTC, carried over from the candidate pool; not re-queried)
13. https://arxiv.org/html/2507.21892 : Graph-R1, Section 5.1 (six datasets including 2WikiMultiHopQA) (read 20261102 21:19 UTC)
14. https://arxiv.org/html/2510.10114v4 : LinearRAG v4, evaluation setup (read 20261102 21:19 UTC)
15. https://arxiv.org/html/2508.06105v2 : LogicRAG v2, datasets paragraph (read 20261102 21:19 UTC)
16. https://aclanthology.org/2026.acl-long.1721.pdf : MiniRAG, ACL 2026 camera-ready, Table 1 (2wikimultihopqa block); https://arxiv.org/html/2501.06713v3 : arXiv v3 text has no mention (read 20261102 21:20 UTC)
17. https://arxiv.org/html/2508.19855v3 : Youtu-GraphRAG v3, experimental setup (read 20261102 21:19 UTC)
