---
type: project
repo: neo4j-labs/llm-graph-builder
trends: [llm-kg-construction, graph-based-rag]
updated: 20261102 23:17 UTC
---

# Neo4j LLM Knowledge Graph Builder

This page answers what Neo4j's open-source graph builder does, what it has been measured on, and whether it is still developed. On the last point, its own banner says it is no longer actively developed and points to a hosted successor.

| Field | Value |
|---|---|
| Repository | https://github.com/neo4j-labs/llm-graph-builder |
| Licence | Apache-2.0. The `LICENSE` file matches the apache.org text line for line, apart from a leading blank line; the appendix placeholder "Copyright [yyyy] [name of copyright owner]" is unfilled, so no holder is named. GitHub's API reports Apache-2.0 [1][2][3]. The README states no licence [5]. |
| Trends | [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md); [Graph-based RAG](../trends/graph-based-rag.md) |

## What it is

A web application and REST API from the [Neo4j](./neo4j.md) Labs organisation. It splits unstructured sources (files, web pages, YouTube transcripts, cloud buckets) into chunks, has a [large language model](../index/large-language-model.md) extract [entities](../index/entity.md) and relationships from each chunk, and writes the chunks and the resulting [knowledge graph](../index/knowledge-graph.md) into a Neo4j database [5]. A chat panel answers questions over that database [5]. It needs Neo4j 5.23 or later with APOC; Aura is supported [5]. The backend is FastAPI with a React frontend [10]. See also [neo4j-graphrag-python](./neo4j-graphrag-python.md).

## How it works

Extraction is delegated to `LLMGraphTransformer` from `langchain-neo4j`, pinned at 0.11.0 [10]. The user may pass allowed node labels and relationship triples; with none, the model picks the types [10]. The extraction prompt and type filtering live in that library, not here [14].

| Stage | What happens | Source |
|---|---|---|
| Extraction | Chunk nodes with embeddings; `LLMGraphTransformer` per chunk group; entities labelled `__Entity__`, linked to their chunk | [10][13] |
| Deduplication | No automatic fuzzy merge. A candidate search (embedding similarity default 0.97) and an APOC merge run on request from the UI (user interface) | [10][13] |
| [Community detection](../index/community-detection.md) | Optional, needs Graph Data Science: Leiden clustering up to 3 levels, an LLM summary per community | [10][13] |
| Chat | Seven modes: `vector`, `fulltext`, `graph_vector`, `graph_vector_fulltext` (the code's default), `entity_vector`, `global_vector`, and `graph`, which has the model write [Cypher](../index/cypher.md) | [10] |

Community summaries are an optional post-processing task [10]. Three modes use [hybrid search](../index/hybrid-search.md) (vector plus keyword index) [10]. The `graph` mode is [text-to-query](../index/text-to-query.md) and runs with `allow_dangerous_requests` set to true [10]. Providers include OpenAI, Anthropic, Gemini, Ollama, OpenAI-compatible endpoints and Diffbot [5][10]. No MCP (Model Context Protocol) reference in `score.py` or `requirements.txt`; absence from the files read, not proof [10].

## Evidence

Everything published is first-party and small. Independent evaluations: none found; the archive's web searches of 20261030 returned none naming this tool (search results are leads, not sources) [16].

**Retriever comparison (first-party, undated).** The notebook `modes_comparison_RAGAS.ipynb` compares six chat modes on one PDF ("About Amazon"): 15 questions made by GPT-4, answers from `openai-gpt-3.5`, `ragas` 0.1.14. Text-to-Cypher is not among the six [11]. The project publishes no table; the means below are computed from its saved CSV on 20261102 [11]. The CSV labels the modes differently (for example "entity search+vector"); they are mapped here by name to the code's modes [10][11].

| Mode | Questions | Context precision | Context recall | Faithfulness | Answer correctness |
|---|---|---|---|---|---|
| vector | 15 | 0.867 | 0.964 | 0.782 | 0.707 |
| fulltext | 15 | 0.933 | 0.981 | 0.798 | 0.785 |
| graph_vector | 15 | 0.933 | 0.981 | 0.825 | 0.732 |
| graph_vector_fulltext | 15 | 0.933 | 0.981 | 0.882 | 0.729 |
| entity_vector | 14 | 0.714 | 0.433 | 0.423 | 0.706 |
| global_vector | 12 | 0.667 | 0.422 | 0.433 | 0.648 |

*Reading:* with 12 to 15 questions, one document, one answer model and no repeated runs, the four upper modes cannot be separated with confidence. The graph modes (0.73) sit near plain vector search (0.71) on answer correctness; fulltext, with no graph, scores highest (0.785).

**Other.** `LLM_Results_.csv` counts extracted nodes and relationships for one PDF page across models and a human list; it scores no correctness [11]. Neo4j's blog on the first 2025 release (published 20250205) lists the evaluation metrics but prints no scores in its text; images not read [15]. For the family's papers, see [the papers group](../papers/llm-kg-construction.md).

## Status and direction

| Item | State on 20261102 | Source |
|---|---|---|
| Latest release | v0.8.7, 20260723; none in the 90 days before the read; 18 releases in all | [4] |
| Commits since 20260804 | 1 on `main` (20261023); 18 on `dev`, 20260807 to 20261029 | [8] |
| Open | 37 issues, 24 pull requests | [9] |

The `dev` commits are maintenance: model lists, library updates, banner text [8]. The app header on `main` reads: "This project is no longer actively developed, instead use Neo4j Document Intelligence in Aura for free." [7] A Labs disclaimer says the project "is not intended or approved for use in production or pre-production environments" and promises no support [6].

The successor is hosted. Neo4j announced Document Intelligence on 20260601 as a preview in Aura. It says Labs packaged the pattern as this builder and Document Intelligence is "the next step". In the preview as read, a job takes up to 20 documents of 10 to 20 pages; the roadmap names larger jobs and API, CLI (command-line interface) and MCP access (the vendor's own announcement) [12]. A roadmap for this repository: unstated [5][6].

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Projects](README.md)
- [Semantica](semantica.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/neo4j-labs/llm-graph-builder : repository metadata, language, branches (read 20261102 20:10 UTC)
2. https://api.github.com/repos/neo4j-labs/llm-graph-builder/license : licence classification and the `LICENSE` text (read 20261102 20:10 UTC)
3. https://www.apache.org/licenses/LICENSE-2.0.txt : canonical text for the line comparison (read 20261102 20:10 UTC)
4. https://api.github.com/repos/neo4j-labs/llm-graph-builder/releases : 18 releases, dates (read 20261102 20:10 UTC)
5. https://github.com/neo4j-labs/llm-graph-builder/blob/main/README.md : description, prerequisites, providers, no licence statement (read 20261102 20:10 UTC)
6. https://github.com/neo4j-labs/llm-graph-builder/blob/main/LABS_DISCLAIMER.txt : Labs disclaimer (read 20261102 20:10 UTC)
7. https://github.com/neo4j-labs/llm-graph-builder/blob/main/frontend/src/components/Layout/Header.tsx : banner text (read 20261102 20:10 UTC)
8. https://api.github.com/repos/neo4j-labs/llm-graph-builder/commits : commits since 20260804 on `main` and `dev` (read 20261102 20:10 UTC)
9. https://api.github.com/search/issues : open issue and pull request counts for the repository (read 20261102 20:11 UTC)
10. https://github.com/neo4j-labs/llm-graph-builder/tree/main/backend : `score.py`, `src/llm.py`, `src/communities.py`, `src/graphDB_dataAccess.py`, `src/QA_integration.py`, `src/shared/constants.py`, `requirements.txt` (read 20261102 20:12 to 20:15 UTC)
11. https://github.com/neo4j-labs/llm-graph-builder/tree/main/experiments : `modes_comparison_RAGAS.ipynb`, `RAGAS_evaluation.csv`, `LLM_Results_.csv` (read 20261102 20:11 to 20:12 UTC; the CSV read again and the means recomputed 20261102 20:37 UTC)
12. https://neo4j.com/blog/genai/introducing-document-intelligence-from-documents-to-a-knowledge-graph-right-inside-aura/ : successor product, limits, roadmap; page dated 20260601, modified 20260707 (read 20261102 20:35 UTC)
13. https://github.com/neo4j-labs/llm-graph-builder/blob/main/backend/src/make_relationships.py : chunk and entity nodes and relations (read 20261030 19:30 UTC, via the archive page ../../kb-kg/projects/llm-graph-builder.md)
14. https://github.com/langchain-ai/langchain-neo4j/blob/libs/neo4j/v0.11.0/libs/neo4j/langchain_neo4j/graph_transformers/llm.py : extraction prompt and strict filtering (read 20261030 19:34 UTC, via the archive page ../../kb-kg/projects/llm-graph-builder.md)
15. https://neo4j.com/blog/developer/knowledge-graph-builder-first/ : first release of 2025; metrics listed, no scores in the text, 38 images not read; published 20250205, modified 20260604 (read 20261102 20:34 UTC)
16. Web searches (no single URL) for independent evaluations of the tool : none found naming it (read 20261030 19:32 to 19:34 UTC, via the archive page ../../kb-kg/projects/llm-graph-builder.md)
