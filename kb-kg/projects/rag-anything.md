---
slug: rag-anything
repo: HKUDS/RAG-Anything
tier: card
category: core
snapshot: 20261030 19:39 UTC
---

# RAG-Anything

| | |
|---|---|
| Repository | https://github.com/HKUDS/RAG-Anything [1] |
| Licence | MIT, from the `LICENSE` file (21 lines; head and tail read) [2]. `pyproject.toml` also says MIT [6]. The README has no licence statement, so no badge disagrees [3]. |
| Language | Python [1] |
| Stars, forks | 24,322, 2,845 (20261030 19:39 UTC) [1] |
| Created, last push | 20250606 06:47 UTC, 20261028 07:20 UTC [1] |
| Latest release | v1.4.4, 20261028 07:03 UTC; PyPI lists 1.4.4 [1][10] |
| Status | active; not archived. No flag in the landscape snapshot (47.6 stars per day, 11.7 forks per 100 stars; heuristics) [1][11] |
| Paper, docs | arXiv 2510.12323, submitted 20251014 [8]; the README and a `docs/` directory [3] |

## What it is

RAG-Anything calls itself an all-in-one multimodal RAG system built on LightRAG: it parses PDFs, Office files, images and text, handles images, tables and equations with dedicated processors, and answers over text and multimodal content together [3]. It sits in the HKUDS organisation, as does LightRAG [1][4]; see the [LightRAG entry](lightrag.md). The paper abstract claims "significant gains" on multimodal benchmarks, largest on long documents, but names no benchmark and no number; the full paper was not read [8]. The README reports no benchmark; no independent evaluation was found [3]. A user report in an open issue puts ingestion at about 24 LLM calls per image block; not measured here [9].

**Relationship to LightRAG: the two repositories say different things.**

| | RAG-Anything README [3] | LightRAG README [4] |
|---|---|---|
| Statement | News 2026.06: "LightRAG enables multimodal RAG through native integration of RAG-Anything". Badge: "Based on LightRAG". | News 2026.05: "Merge RagAnything into LightRAG". Also: "Starting with v1.5, LightRAG seamlessly integrates multimodal processing". |
| Listing | n/a | Still under Related Projects as "Multimodal RAG" |
| Retirement notice | None found | None found |

In code, RAG-Anything 1.4.4 declares `lightrag-hku<1.5` [6][10]. LightRAG v1.5.0 came out on 20260603 [5]. So the published package targets LightRAG releases before 1.5. Whether RAG-Anything will follow LightRAG 1.5 or be retired: unstated.

## How it works

A parser (MinerU, Docling or PaddleOCR) splits a document into text blocks, images, tables and equations [3]. Each non-text item goes to a modality processor, which calls an LLM or vision model to describe it and extract entities [3]. Entities, cross-modal relations and document-hierarchy links are written into a LightRAG graph beside the text [3]. Queries use LightRAG's hybrid, local, global and naive modes, an optional VLM-enhanced mode, and a call that takes a table or equation with the question [3]. Audio and video processors arrived on 20260902 [7]. No MCP interface is mentioned. Fully local operation: unstated; examples for Ollama, LM Studio and vLLM exist [12].

## Status and direction

Active. 100 commits since 20260801, mostly fixes to parsing, batch ingestion and equations [7]. Seven releases from v1.3.0 (20260506) to v1.4.4 [7]. 96 open issues and 1 open pull request (20261030 19:45 UTC); 71 contributors listed [13][14]. Roadmap: unstated.

## Sources

1. https://github.com/HKUDS/RAG-Anything : repository metadata via the GitHub API (read 20261030 19:39 UTC)
2. https://github.com/HKUDS/RAG-Anything/blob/main/LICENSE : MIT text (read 20261030 19:39 UTC)
3. https://github.com/HKUDS/RAG-Anything/blob/main/README.md : description, news, architecture, query modes (read 20261030 19:39 UTC)
4. https://github.com/HKUDS/LightRAG/blob/main/README.md : news on the merge and v1.5; Related Projects (read 20261030 19:39 UTC)
5. https://github.com/HKUDS/LightRAG/releases : v1.5.0 release date (read 20261030 19:40 UTC)
6. https://github.com/HKUDS/RAG-Anything/blob/main/pyproject.toml : dependency `lightrag-hku<1.5`, licence field (read 20261030 19:40 UTC)
7. https://github.com/HKUDS/RAG-Anything/commits/main : commit subjects, 100 commits since 20260801, release dates (read 20261030 19:40 UTC)
8. https://arxiv.org/abs/2510.12323 : title, authors, date, abstract (read 20261030 19:40 UTC)
9. https://github.com/HKUDS/RAG-Anything/issues/348 : user-reported LLM calls per image block (read 20261030 19:40 UTC)
10. https://pypi.org/pypi/raganything/json : version 1.4.4 and its dependency list (read 20261030 19:40 UTC)
11. [Landscape snapshot](../landscape/20261030_1913-github/repos.tsv) : stars per day, forks per 100 stars, flags (20261030 19:13 UTC)
12. https://github.com/HKUDS/RAG-Anything/tree/main/examples : example scripts (read 20261030 19:41 UTC)
13. https://github.com/HKUDS/RAG-Anything/graphs/contributors : contributor count via the API (read 20261030 19:40 UTC)
14. https://github.com/HKUDS/RAG-Anything/issues : open issue and pull request counts via the search API (read 20261030 19:45 UTC)
