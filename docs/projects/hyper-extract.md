---
type: project
repo: yifanfeng97/Hyper-Extract
trends: [llm-kg-construction]
updated: 20261102 23:17 UTC
---

# Hyper-Extract

This page answers what Hyper-Extract builds from documents, how it is put together, and how much evidence stands behind it. The repository was created on 20260107 [1]. It moves fast, with one account behind over half of the commits since 20260804 [6], and it has no published evaluation.

| Field | Value |
|---|---|
| Repository | https://github.com/yifanfeng97/Hyper-Extract |
| Licence | The Apache License 2.0 text with small wording changes. GitHub cannot classify the file and reports `NOASSERTION` [1][2]. A word-by-word comparison with the apache.org text finds 11 differing spans: the definitions of "License", "Contribution" and "Contributor", clause 4(d), the end of section 4, section 5 and the appendix line, which reads "Copyright [2026] [Yifan Feng]" with the brackets left in [2][3]. README, `pyproject.toml` and PyPI all say Apache-2.0 [5][9]. Legal effect of the changes: not assessed. |
| Trends | [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md) |

## What it is

A command-line tool (`he`) and Python library that turns documents into structured knowledge with a [large language model](../index/large-language-model.md) [5]. The output is not only a [knowledge graph](../index/knowledge-graph.md): the README names nine "knowledge structures", from lists and sets to graphs, [hypergraphs](../index/hypergraph.md), temporal, spatial and spatio-temporal graphs [5]. A YAML template or a named method fixes what to extract [5]. The result is a saved directory that can be searched, updated, and exported to Obsidian, GraphML, CSV, JSON-LD or [Cypher](../index/cypher.md) [5]. The README claims 80+ templates in six domains; the repository tree holds 40 preset files in seven folders; the one opened declares `language: [zh, en]`. How the README counts is unstated [5][10]. For the papers behind the family, see [the papers group](../papers/llm-kg-construction.md).

## How it works

The README describes three layers: auto-types (the nine structures), methods (extraction and retrieval algorithms) and templates [5]. The docs list ten methods, from a chunk-and-embed baseline (`chunk_rag`) through `itext2kg`, `kg_gen` and `atom` to `graph_rag`, `light_rag`, `hyper_rag`, `hypergraph_rag` and `cog_rag`; the README says "11+" [5][8].

| Step | What the docs and code say | Source |
|---|---|---|
| [Chunking](../index/chunking.md) | Default 2,048 characters with 256 overlap | [8] |
| Extraction | Chunks go to the model in parallel with structured output; the model must support function calling ([tool use](../index/tool-use.md)) | [5][8] |
| Merge | A merger deduplicates entities; the methods read use the merger of the `ontomem` package | [8][10] |
| Index | `faiss-cpu` is a dependency; [embeddings](../index/embedding.md) serve [vector search](../index/vector-search.md) | [5][9] |
| Provenance | `feed` adds a document under a named source; removing or re-feeding that source rolls its facts back | [5] |

A failed chunk is skipped by default and recorded in `ka.extraction_failures`; a constructor option can abort instead [8]. The `chunk_rag` method embeds only, so it costs no extraction call; the docs advise starting there and paying for `graph_rag` only if questions are multi-hop [8]. The `graph_rag` and `light_rag` methods are modules of this repository, and `graph_rag` optionally imports Leiden clustering ([community detection](../index/community-detection.md)) from `graspologic`; whether they reproduce [Microsoft GraphRAG](./microsoft-graphrag.md) or [LightRAG](./lightrag.md) faithfully was not checked [10]. Providers named: OpenAI, Anthropic, Gemini, DeepSeek, Alibaba Bailian and a local vLLM server [5]. An optional stdio [MCP](../index/model-context-protocol.md) (Model Context Protocol) server offers nine tools and is read and export only [5][8].

## Evidence

None published. There is no paper and no benchmark in the README, `pyproject.toml` or the docs read [5][8][9]. The docs call their method-choice page "a decision aid, not an evaluation framework" and say it defines no metrics [8]. The README has a feature table against GraphRAG, LightRAG, KG-Gen and ATOM: it marks which structures each tool supports, scores nothing and is the project's own claim (first-party) [5]. Independent evaluation: none found; the archive page reports none (its method is not recorded there) [11]. A search of the arXiv API for the phrase "Hyper-Extract" in any field returned 0 entries on 20261102 [12]; the README has no arXiv link, citation block or BibTeX entry [5].

## Status and direction

| Item | State on 20261102 | Source |
|---|---|---|
| Latest release | v0.11.0, 20261029; PyPI lists 0.11.0, classifier "Development Status :: 3 - Alpha" | [4][9] |
| Releases | 21 in all, the first v0.1.1 (20260404); 15 in the 90 days before the read | [4] |
| Commits since 20260804 | 231: 16 in August, 192 in September, 23 in October | [6] |
| Authors | 124 commits from the owner account, 58 and 40 from two others | [6] |
| Open | 1 issue, 8 pull requests | [7] |

*Reading:* the pace has dropped from the September burst, and over half of the commits come from one account, a concentration risk. The release notes read as hardening: v0.11.0 repairs a regression in v0.10.5 that broke seven shipped presets, and earlier ones fix Cypher export and silent chunk failures [8]. A roadmap: unstated. Nothing in the README or docs read says the project is in maintenance mode or has a hosted tier [5][8].

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Projects](README.md)

**Index**

- [Hypergraph](../index/hypergraph.md)
- [Provenance](../index/provenance.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/yifanfeng97/Hyper-Extract : repository metadata, default branch, archived flag, creation date 20260107 (read 20261102 20:10 UTC; creation date read again 20:34 UTC)
2. https://api.github.com/repos/yifanfeng97/Hyper-Extract/license : `NOASSERTION` classification and the `LICENSE` text, 200 lines (read 20261102 20:10 UTC; compared again 20:35 UTC)
3. https://www.apache.org/licenses/LICENSE-2.0.txt : canonical text for the word-by-word comparison (read 20261102 20:10 UTC; read again 20:34 UTC)
4. https://api.github.com/repos/yifanfeng97/Hyper-Extract/releases : 21 releases, tags and dates (read 20261102 20:10 UTC; the count, the first and the 90-day count checked again 20:35 UTC)
5. https://github.com/yifanfeng97/Hyper-Extract/blob/main/README.md : description, structures, methods, providers, MCP tools, feature table, licence line (read 20261102 20:10 UTC; searched again for arXiv, citation and BibTeX references 20:38 UTC)
6. https://api.github.com/repos/yifanfeng97/Hyper-Extract/commits : commits since 20260804 by month and author account (read 20261102 20:10 UTC)
7. https://api.github.com/search/issues : open issue and pull request counts (read 20261102 20:13 UTC)
8. https://github.com/yifanfeng97/Hyper-Extract/tree/main/docs/en : `concepts/methods.md`, `concepts/choosing-a-method.md`, `concepts/architecture.md`, `mcp.md`, `news.md` (read 20261102 20:12 UTC)
9. https://github.com/yifanfeng97/Hyper-Extract/blob/main/pyproject.toml and https://pypi.org/pypi/hyperextract/json : dependencies, classifiers, licence field, version (read 20261102 20:13 UTC)
10. https://github.com/yifanfeng97/Hyper-Extract/tree/main/hyperextract : the file tree, `methods/rag/graph_rag.py`, `methods/rag/light_rag.py`, the preset templates (read 20261102 20:14 UTC)
11. https://github.com/yifanfeng97/Hyper-Extract : "no benchmark and no independent evaluation was found" (read 20261030 19:44 UTC, via the archive page ../../kb-kg/projects/hyper-extract.md)
12. https://export.arxiv.org/api/query?search_query=all:%22Hyper-Extract%22 : arXiv API search of all fields for the phrase, 0 results (read 20261102 20:38 UTC)
