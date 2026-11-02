---
type: project
repo: HKUDS/RAG-Anything
trends: [graph-based-rag]
updated: 20261102 23:17 UTC
---

# RAG-Anything

This page answers what RAG-Anything adds to LightRAG, how it handles content that is not text, what has been measured and by whom, and how it relates to LightRAG's own multimodal support. It is the multimodal member of the graph-based RAG (retrieval-augmented generation) trend.

| Field | Value |
|---|---|
| Repository | https://github.com/HKUDS/RAG-Anything |
| Licence | MIT, from the `LICENSE` file read through GitHub's licence endpoint; `pyproject.toml` also says MIT [2][6]. The README has no licence statement [5]. The default parser, MinerU, has a different licence (see Status and direction) [13]. |
| Trends | [Graph-based RAG](../trends/graph-based-rag.md) |

## What it is

RAG-Anything is a Python framework for multimodal [retrieval-augmented generation](../index/retrieval-augmented-generation.md). It parses PDFs, Office files, images and text, treats images, tables and equations with dedicated processors, and since v1.4.1 can take audio and video, opt-in and off by default [3][5]. The README says it is built on [LightRAG](./lightrag.md), and both live in the HKUDS GitHub organisation [5][10].

The paper (arXiv, 20251014) is by Guo, Ren, Xu, Zhang and Huang, at the University of Hong Kong [8][9].

### Relation to LightRAG

| | RAG-Anything | LightRAG |
|---|---|---|
| README news | 2026.06: "LightRAG enables multimodal RAG through native integration of RAG-Anything." [5] | 2026.05: "Merge RagAnything into LightRAG"; from v1.5 it "seamlessly integrates multimodal processing" [10] |
| Listing | Badge "Based on LightRAG" [5] | Still lists RAG-Anything under related projects as "Multimodal RAG" [10] |
| Code | Requires `lightrag-hku<1.5` [6][7] | v1.5.0 on 20260603; latest v1.5.7 on 20260902 [11] |

*Reading:* both READMEs say the capability now lives in LightRAG 1.5, yet RAG-Anything 1.4.4 ships against LightRAG below 1.5. No retirement notice was found in either README. Whether RAG-Anything will follow LightRAG 1.5 or be retired is **unstated**.

## How it works

1. A parser (MinerU by default, or Docling, or PaddleOCR) splits a document into text blocks, images, tables and equations [5]. Release v1.4.4 pins MinerU to 3.x [3][6].
2. Each non-text item goes to a modality processor. A [large language model](../index/large-language-model.md) or vision model describes it and extracts [entities](../index/entity.md) [5][9].
3. The paper builds two [knowledge graphs](../index/knowledge-graph.md), a cross-modal graph that grounds non-text units in their context and a text graph, then merges them by entity alignment [9]. The README adds "belongs_to" links that keep the document hierarchy [5].
4. Queries combine [vector similarity](../index/vector-search.md) with graph traversal [5]. Text modes are LightRAG's `hybrid`, `local`, `global` and `naive`; a VLM-enhanced mode sends retrieved images to a vision model [5]. The paper's experiments add a reranker, bge-reranker-v2-m3 [9].

The README mentions no [MCP](../index/model-context-protocol.md) (Model Context Protocol) interface and no roadmap [5]. Fully local operation is **unstated**.

## Evidence

First-party only. The graph systems in the paper's tables use a GPT-4o-mini backbone, MinerU parsing and text-embedding-3-large; GPT-4o-mini also grades the answers ([LLM-as-judge](../index/llm-as-judge.md)). The "GPT-4o-mini" row reads documents as page images, at most 50 pages [9].

| System | DocBench overall accuracy (%) | MMLongBench overall accuracy (%) |
|---|---|---|
| GPT-4o-mini on page images | 51.2 | 33.5 |
| LightRAG | 58.4 | 38.9 |
| MMGraphRAG | 61.0 | 37.7 |
| RAG-Anything | 63.4 | 42.8 |

DocBench has 1,102 questions and MMLongBench 1,082 [9]. The text reports a widening gap on long documents (68.2 against 54.6 at 101 to 200 pages, 68.8 against 55.0 above 200), in a passage comparing RAG-Anything with MMGraphRAG [9]. An ablation on DocBench gives 60.0 for a chunk-only variant, 62.4 without the reranker and 63.4 for the full system [9]. On DocBench's unanswerable questions RAG-Anything scores 46.0, MMGraphRAG 60.5 [9].

*Reading:* one model family answers and grades, and the evaluation sections read (3.1 to 3.3) report no confidence intervals or repeated runs, so gaps of one to five points are weak evidence. The abstract's "significant improvements" carries no number [8].

An arXiv search of abstracts for "RAG-Anything" found only the paper itself, so no independent evaluation was found; full texts were not searched [12]. The README reports no benchmark [5]. Longer notes: [archive entry](../../kb-kg/projects/rag-anything.md). Papers: [graph-based RAG paper page](../papers/graph-based-rag.md).

## Status and direction

- **Release:** v1.4.4, 20261028 07:03 UTC; PyPI lists the same version [3][7]. Seven releases from v1.3.0 (20260506) to v1.4.4 [3].
- **Activity, 20260804 to 20261102:** 100 commits on the default branch from 20260813 to 20261028, by 25 authors. 71 contributors in total, 96 open issues, 5 open pull requests [4].
- **Recent changes (release notes):** native MinerU 3.x content lists (v1.4.0, 20260902); audio and video, opt-in (v1.4.1, 20260902); a fix for a flaw in 1.4.1, where a Markdown image reference to any local file could be sent to the vision provider (v1.4.2, 20261006); a security fix (v1.4.3, 20261021): HTML was converted to PDF through LibreOffice, which fetched the remote URLs the page referenced and embedded local images, so HTML now needs Docling; MinerU 4 unsupported, Docling route for Python 3.14 (v1.4.4) [3].
- **Maintenance mode or hosted tier:** neither is stated [5]. The multimodal capability moved into LightRAG (above).
- **Roadmap:** **unstated**.
- **Licence caution:** MinerU's licence file is not classified by GitHub. It says Apache License 2.0 plus additional terms: a separate commercial licence is required above 100 million monthly active users or USD 20 million monthly revenue, and online services must state that MinerU is used [13]. Licences of other dependencies: **unstated**.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [LightRAG](lightrag.md)
- [Projects](README.md)

**Papers**

- [Papers: Graph-based RAG](../papers/graph-based-rag.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/HKUDS/RAG-Anything : repository metadata via `gh api` (archived flag, topics) (read 20261102 20:10 UTC)
2. https://github.com/HKUDS/RAG-Anything/blob/main/LICENSE : MIT text, via the licence endpoint (read 20261102 20:10 UTC)
3. https://github.com/HKUDS/RAG-Anything/releases : release list and notes for v1.3.0, v1.4.0 to v1.4.4; v1.4.1 audio/video "default off", v1.4.3 HTML security fix (read 20261102 20:10 UTC; v1.4.1 and v1.4.3 notes re-read 20261102 20:33 UTC)
4. https://github.com/HKUDS/RAG-Anything/commits/main : 100 commits since 20260804, 25 authors; contributors, issue and pull request counts via the API (read 20261102 20:13 UTC)
5. https://github.com/HKUDS/RAG-Anything/blob/main/README.md : description, news, architecture, query modes, parsers, no licence or roadmap text (read 20261102 20:10 UTC)
6. https://github.com/HKUDS/RAG-Anything/blob/main/pyproject.toml : MIT, `lightrag-hku<1.5`, MinerU pin (read 20261102 20:10 UTC)
7. https://pypi.org/pypi/raganything/json : version 1.4.4 uploaded 20261028, requirements (read 20261102 20:13 UTC)
8. https://arxiv.org/abs/2510.12323 : authors, first version 20251014, abstract (read 20261102 20:11 UTC)
9. https://arxiv.org/html/2510.12323 : affiliation, method, experimental setup, Tables 2 to 4, length results (read 20261102 20:11 UTC)
10. https://github.com/HKUDS/LightRAG/blob/main/README.md : news of the merge, v1.5 text, related projects (read 20261102 20:13 UTC)
11. https://github.com/HKUDS/LightRAG/releases : v1.5.0 (20260603) and v1.5.7 (20260902) (read 20261102 20:13 UTC)
12. https://arxiv.org/search/?query=%22RAG-Anything%22&searchtype=abstract : one result, the paper itself (read 20261102 20:14 UTC)
13. https://github.com/opendatalab/MinerU/blob/master/LICENSE.md : MinerU terms; GitHub reports "other" (read 20261102 20:18 UTC)
