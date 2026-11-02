---
type: dataset
kinds: [corpus]
benchmark: kilt
updated: 20261102 21:05 UTC
---

# Wikipedia snapshots of DPR and KILT

This page answers what the two processed copies of English Wikipedia behind DPR and KILT contain, how large they are, who may use them and what is wrong with them. They are two datasets, not one. The tasks, scores and results that use the KILT copy are on [the KILT benchmark page](../benchmarks/kilt.md).

## What it contains

- **DPR passages.** The English Wikipedia dump of 20 December 2018, cleaned with the code released with DrQA. That step removes tables, infoboxes, lists and disambiguation pages. The text is then cut into disjoint blocks of 100 words, and each block is prefixed with its article title [1][3].
- **KILT knowledge source.** The dump of 1 August 2019 [5]. One JSON record per page: title, page id, a list of paragraph strings, a list of hyperlink anchors, categories, a history field and Wikidata information [5]. The paragraph list keeps list items and section headers, so lists are present here and absent from the DPR copy [4].

## Size and versions

| Copy | Size | Source |
|---|---|---|
| DPR passages (`psgs_w100.tsv.gz`) | 21,015,324 passages; file 4,694,541,059 bytes | [1][2] |
| DPR on Hugging Face (`wiki_dpr`) | 21,015,300 rows, each with a 768-dimension [embedding](../index/embedding.md); 78,419,248,156 bytes | [3] |
| KILT knowledge source | 5,903,530 pages; one JSON file of 34.76 GiB (37,318,876,722 bytes) | [5][12] |
| KILT on Hugging Face (`kilt_wikipedia`) | 5,903,530 rows; 29,372,535,718 bytes | [6] |
| KILT text cut into 100-word passages | 22,220,793 passages, lists left out | [4] |

In the KILT paper, 1,642,311 pages (about 28%) hold knowledge that some KILT instance needs [4]. The DPR repository added a better Natural Questions checkpoint and Wikipedia embeddings in March 2021 [2]. Both repositories are archived and read-only: KILT was last pushed on 20220331 and DPR on 20230406 [2][5].

## Licence

- **Wikipedia text.** Wikimedia's dump terms: "all original textual content is licensed under the GNU Free Documentation License (GFDL) and the Creative Commons Attribution-Share-Alike 4.0 License". Some text is under the Creative Commons licence only, and some authors use other licences [8].
- **DPR.** The repository `LICENSE` is Creative Commons Attribution-NonCommercial 4.0, and the README says "DPR is CC-BY-NC 4.0 licensed as of now" [2]. The `wiki_dpr` card header repeats `cc-by-nc-4.0` [3]. Whether that label covers the passage file itself is **unstated**. GitHub reports the repository licence as "NOASSERTION" [2].
- **KILT.** The repository says "KILT is MIT licensed" and the `LICENSE` file is the MIT text [5]. The `kilt_tasks` card header says `mit`, but its licensing section reads "[Needs More Information]". The `kilt_wikipedia` card has no licence field, and its licensing section reads "[More Information Needed]" [6]. The challenge terms on the evaluation site put the annotations under the licence terms of the Wikipedia article pages or, where those are unavailable, CC BY-SA 3.0, and point to the KILT GitHub page for the full terms [7]; that README holds no such text [5].

*Reading:* the DPR copy is labelled non-commercial; the KILT copy carries two statements (MIT for the repository, share-alike for the data). For commercial use, treat the text as share-alike Wikipedia text and ask the authors about the rest.

## How it was made

DPR took the dump date from earlier work (Lee et al., 2019) and the 100-word cut from Wang et al. (2019); overlapping blocks, which Wang et al. also propose, were not found better [1].

KILT chose one snapshot so that every task's evidence can be mapped to it: tasks tied to different Wikipedia versions force re-indexing, and a model pre-trained on one snapshot may need retraining for another [4]. How the evidence was mapped is on [the benchmark page](../benchmarks/kilt.md).

## Used by

- **Papers.** [DPR](../papers/foundations.md) (Karpukhin et al., 2020) trains and tests five question sets on the DPR passages [1]. Its OpenAlex citation count is 3,593 (EMNLP record, read 20261102 20:03 to 20:04 UTC) [13]. The KILT paper runs DPR on its own source [4]. The PopQA paper retrieves from a December 2018 dump [9]. CoRAG (Wang et al.) retrieves from KILT's Wikipedia [11]. RAGSearch (2026) uses "the 2018 Wikipedia dump" of the DPR paper for its dense baseline [10]; see [the graph-based RAG papers](../papers/graph-based-rag.md) and [the trend](../trends/graph-based-rag.md).
- **Datasets.** [Natural Questions](natural-questions.md) and [TriviaQA](triviaqa.md) in their open-domain form, [PopQA](popqa.md).
- **Benchmarks.** [KILT](../benchmarks/kilt.md), [Natural Questions](../benchmarks/natural-questions.md), [RAGSearch](../benchmarks/ragsearch.md).

## Known problems

- **Different dumps in one field.** Each family uses its own: [HotpotQA](hotpotqa.md) 1 October 2017 [14], [2WikiMultiHopQA](2wikimultihopqa.md) 1 January 2020 [15], PopQA December 2018 [9], DPR 20 December 2018 [1], KILT 1 August 2019 [5]. Scores built on different dumps are not directly comparable.
- **DPR cleaning drops structure.** Answers that sit in tables, infoboxes or lists are unreachable by design [1]. [The Natural Questions page](natural-questions.md) gives the share of table answers in that set.
- **The passage unit is not fixed.** The same KILT source is 22.2 million passages under the KILT paper's 100-word cut [4] and about 36 million in CoRAG [11]. The split CoRAG cites (Maillard et al., 2021) was not read for this page, so the reason is **unstated**.
- **Counts disagree slightly.** 21,015,324 passages in the paper, 21,015,300 rows on Hugging Face; the reason is **unstated** [1][3].
- **Licences clash.** A non-commercial label on text that is share-alike at its origin; how the two combine is **unstated** by the authors [2][8].
- **Age.** Both dumps predate 2020, so later changes to Wikipedia are missing. Whether current models saw them in training is **unstated** (see [contamination](../index/data-contamination.md)).

## Sources

1. https://arxiv.org/abs/2004.04906 : DPR paper v3 (30 Sep 2020), full text at arxiv.org/html/2004.04906: Section 4.1, Table 1, Table 2 (read 20261102 20:54 UTC)
2. https://github.com/facebookresearch/DPR : README, `LICENSE` (CC BY-NC 4.0), `dpr/data/download_data.py` (resource `data.wikipedia_split.psgs_w100`, 100-word segments, no overlap), `gh api` metadata (archived, last push 20230406, licence "NOASSERTION"), and the size of `https://dl.fbaipublicfiles.com/dpr/wikipedia_split/psgs_w100.tsv.gz` from its HTTP header (read 20261102 20:54 to 20:57 UTC)
3. https://huggingface.co/datasets/facebook/wiki_dpr : card (licence, dump date, rows, embedding size) and API (read 20261102 20:54 UTC)
4. https://arxiv.org/abs/2009.02252 : KILT paper v4 (27 May 2021), full text at arxiv.org/html/2009.02252: knowledge source, retrieval baselines footnote, Figure 2, appendix "Wikipedia Representation" (read 20261102 20:53 UTC)
5. https://github.com/facebookresearch/KILT : README (snapshot, 5,903,530 pages, record structure, "KILT is MIT licensed"), `LICENSE` (MIT), `gh api` metadata (archived, last push 20220331) (read 20261102 20:53 UTC)
6. https://huggingface.co/datasets/facebook/kilt_wikipedia and https://huggingface.co/datasets/facebook/kilt_tasks : cards and API (rows, bytes, licence fields, file list) (read 20261102 20:54 UTC)
7. https://eval.ai/api/challenges/challenge/689/ : the KILT challenge record, terms and conditions (read 20261102 20:55 UTC)
8. https://dumps.wikimedia.org/legal.html : licence of dump text (read 20261102 20:54 UTC)
9. https://arxiv.org/abs/2212.10511 : PopQA paper, full text: "We use Wikipedia dump from December 2018" (read 20261102 20:57 UTC)
10. https://arxiv.org/abs/2604.09666 : Fan et al., RAGSearch, v1 (1 Apr 2026), full text: setup, dense RAG backend (read 20261102 20:57 UTC)
11. https://arxiv.org/abs/2501.14342 : CoRAG v3 (10 Oct 2025), full text: Section 4.1 (read 20261102 20:56 UTC)
12. http://dl.fbaipublicfiles.com/KILT/kilt_knowledgesource.json : size from the HTTP header, 37,318,876,722 bytes (read 20261102 20:57 UTC)
13. https://api.openalex.org/works/doi:10.18653/v1/2020.emnlp-main.550 : citation count 3,593 (read 20261102 20:03 to 20:04 UTC, by the research pool of this documentation)
14. https://arxiv.org/abs/1809.09600 : HotpotQA paper, full text at arxiv.org/html/1809.09600, Appendix A.1: "We downloaded the dump of English Wikipedia of October 1, 2017" (read 20261102 21:28 UTC)
15. https://arxiv.org/abs/2011.01060 : 2WikiMultiHopQA paper, full text at arxiv.org/html/2011.01060, Appendix A.1: "We downloaded the dump of English Wikipedia on January 1, 2020" (read 20261102 21:28 UTC)
