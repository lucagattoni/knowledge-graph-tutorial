---
type: trend
shift: fixed schemas -> induced ones
status: steady
order: 2
updated: 20261103 10:36 UTC
---

# Building knowledge graphs with LLMs: from fixed schemas to induced ones

This page answers: when a [large language model](../index/large-language-model.md) (LLM) turns text into a [knowledge graph](../index/knowledge-graph.md), who decides which types of entity and relation exist, and is that decision moving from people to models? It covers the construction step as a product in its own right. The use of such graphs to answer questions is told in [Graph-based RAG](./graph-based-rag.md), where a graph feeds retrieval-augmented generation ([RAG](../index/retrieval-augmented-generation.md)).

> **Distinctive because** the thing built and judged is the typed graph or [ontology](../index/ontology.md) itself, kept as an asset and scored against human-made schemas [3][10]. The nearest neighbour, [graph-based RAG](./graph-based-rag.md), runs the same extraction step, but there the graph is an index judged by the answers it supports.

## Why it emerged

A graph needs a [schema](../index/schema.md): the entity and relation types it may hold. In the 2023 work this page starts from, people wrote it and the extractor followed it. SPIRES (202304) used a model zero-shot but still took "a detailed, user-defined knowledge schema" as input [4]. [Text2KGBench](../benchmarks/text2kgbench.md) (202308) made the given ontology the test: extracted facts must respect its concepts, relations and domain and range constraints [5].

The authors of the later work name the given schema as the obstacle. EDC (202404) says a schema placed in the prompt can exceed the model's context window, and that sometimes no predefined schema exists, so it builds "a succinct self-generated schema" [1]. AutoSchemaKG (202505) describes "fully autonomous knowledge graph construction that eliminates the need for predefined schemas" and reports a graph family of 900+ million nodes and 5.9 billion edges built from over 50 million documents [3] (first-party). Earlier automatic construction, before language models, is told in [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).

*Reading:* the order of events fits the story of a schema that people wrote and models then replaced. Its turning point rests on motivation sentences written by the method authors [1][3]; no source read compares the two eras on one task.

## Why it matters

Pan et al. state that knowledge graphs "are difficult to construct and evolving by nature" [15]. A 2026 industrial study names two costs: "scarcity of annotated resources" and "the complexity of ontology engineering workflows" [12]. The SCOPE paper says "most extraction systems assume the schema is already available" [10]. If a model can propose the schema, the human step shrinks to review. A second cost is trust: a flat store of extracted triples keeps "little record of who owns a fact, why it was admitted" [11].

## How it works

All variants chunk text, ask a model for entities and relations ([relation extraction](../index/relation-extraction.md)), then deal with three problems: which types exist, which names are the same thing, and which facts to trust. Graph-based RAG runs the same extraction step: a model extracts entities and relationships from each text chunk [24]. Several papers here also report question-answering scores [3][11], so the line between the two trends is the object of study, not a ban on retrieval.

| Position | Who supplies the schema | Examples | Source |
|---|---|---|---|
| Given first | A person, before extraction | [OntoGPT](../projects/ontogpt.md) (LinkML schema; names grounded to ontology identifiers and validated); [Hyper-Extract](../projects/hyper-extract.md) (80+ YAML templates); [GLiNER](../projects/gliner.md) (entity labels given at run time to a small encoder model that identifies "any type of entity", for [named-entity recognition](../index/named-entity-recognition.md)) | [23][20][22][16] |
| Optional | A person, if they choose to | [Neo4j LLM Graph Builder](../projects/llm-graph-builder.md) (a custom schema of node and relationship labels can be set in the extraction settings; what it does without one is **unstated** in the README read) | [32] |
| Induced | The model, during or after extraction | EDC (extract, define, canonicalize); AutoSchemaKG (conceptualization into semantic categories); DIAL-KG (new schemas induced from validated knowledge, closed loop); MAGG (types induced from document content, but its main test runs on a fixed schema; see the measurements below) | [1][3][7][11] |
| Ontology first | A designed or agent-drafted ontology, then constrained extraction | OntoKG (schema designed first; 34.0M nodes and 61.2M edges from a 202601 Wikidata dump, first-party); [Helix Foundry](https://github.com/HelixDB/helix-foundry) (an agent drafts the ontology, a person reviews it) | [8][25] |

Three repeated steps follow extraction.

- **Canonicalize.** EDC canonicalizes after extraction [1]; KGGen clusters related entities to reduce sparsity [2]; "Better Later Than Sooner" canonicalizes types and predicates by embedding and defers correction of ontology violations to one post-extraction pass, which it says avoids repeated model calls [9].
- **Ground and validate.** OntoGPT asks the model for names, not identifiers, grounds them against ontologies and marks failures with an `AUTO:` prefix [23].
- **Record provenance.** Hyper-Extract keeps every source attributed so a document can be rolled back [20]; Helix Foundry keeps the row or quote each value came from [25].

### Schema and ontology induction

Merged here from the candidate list. It is the Induced row of the table above. *Reading:* it is not a trend of its own because it fails the distinctness test: it changes where the schema comes from, not what is stored, when a model is used or who steers. That origin is this family's shift. SCOPE (202605) benchmarks the step on its own, building gold schemas from 24 public extraction sources [10].

### Ontology-grounded context graphs

Merged here too. Projects from 2025 and 2026 put an ontology under a graph meant for agents. Two keep the origin of facts. Helix Foundry (created 20261007) loads values that keep the table row or quote they came from [25]. Carrel ("Ontology-Augmented Generation") retains sources, time information and conflict indicators; its learn-an-ontology Agent Loop plugin is "not yet implemented" [26]. The other two say nothing of provenance in the READMEs read. OntoBricks maps Databricks tables to a graph with [OWL](../index/owl.md) (Web Ontology Language), R2RML (a mapping language from relational tables to RDF) and [SPARQL](../index/sparql.md) [27]. CortexDB (created 20250807) lists a "Palantir-style ontology with governed actions" beside memory and a knowledge graph in the [Resource Description Framework](../index/rdf.md) (RDF) in one SQLite file [28]. Semantica, the largest of this kind in the snapshot (14,349 stars), has a [project page](../projects/semantica.md) that sets its README against its code [39].

*Reading:* they belong to this family because the asset they build is a typed graph under an ontology. How agents read the graph afterwards is [Agent memory](./agent-memory.md) or Graph-based RAG. "Context graph" is mostly a label: the wording ("context graph" in an abstract or title) returned 34 results for 20251102 to 20261102 against 9 the year before (read 20261102 21:21 UTC), but the titles are mostly about other graph topics, and only a few use it for an enterprise knowledge structure for agents, such as "Context Graphs for Proactive Enterprise Agents" (2607.07721) [17]. No source read defines it.

## Representative projects

Stars are from the snapshot of 20261030 19:54 UTC [18]; they are signals, not verdicts. Licences are as GitHub's licence endpoint reports them for each LICENSE file, read 20261102 21:20 UTC [30]; the Hyper-Extract LICENSE text was also read [21].

| Project | Position | Licence | Stars | Note |
|---|---|---|---|---|
| [Neo4j LLM Graph Builder](../projects/llm-graph-builder.md) | Schema optional | Apache-2.0 | 5,289 | Pushed 20261029 (snapshot), yet only 1 commit in 90 days on the default branch; the `dev` branch had 18 since 20260801 [18][19]. Its header banner, added by pull request 1644 into the `dev` branch (merged 20261016), says it is "no longer actively developed" [19] |
| [Hyper-Extract](../projects/hyper-extract.md) | Given first (templates); KG-Gen among its methods | Apache-2.0 text; GitHub reports NOASSERTION (the archive notes wording changes) | 4,207 | Created 20260107; 21 releases, latest v0.11.0 on 20261029 [20][21] |
| [GLiNER](../projects/gliner.md) | Given first (run-time labels); component | Apache-2.0 | 4,184 | Joint entity and relation model for graph building [22] |
| [OntoGPT](../projects/ontogpt.md) | Given first (LinkML) | BSD-3-Clause | 1,080 | Last push 20260910 [23] |
| [AutoSchemaKG](https://github.com/HKUST-KnowComp/AutoSchemaKG) | Induced | MIT | 845 | Quiet: no push for 184 days at the snapshot [18][29] |
| [kg-gen](https://github.com/stair-lab/kg-gen) | Schema step unstated; clusters entities | README says MIT; no LICENSE file found | 1,289 | Quiet: no push for 219 days at the snapshot [18][31] |
| [Helix Foundry](https://github.com/HelixDB/helix-foundry) | Ontology first | Apache-2.0 | 1,854 | Created 20261007 [18][25] |
| [Carrel](https://github.com/FengZhenfei/carrel) | Ontology first | MIT | 653 | Created 20260928 [18][26] |
| [Semantica](../projects/semantica.md) | Ontology promised; applied after extraction in the code read | MIT | 14,349 | Page added at the owner's review of 20261103; the README is set against the code there [18][39] |

*Reading:* of the first four projects with a page, three need a schema or label list from a person (Hyper-Extract templates, GLiNER labels, OntoGPT LinkML), and the most-starred of them, LLM Graph Builder, makes it optional. Semantica, added at the owner's review of 20261103 with more stars than any of the four, promises an ontology under its graph, but in the code read the ontology is applied after extraction, not before it [39]. The quiet code is AutoSchemaKG (induced) and kg-gen (no schema step stated); the active repositories are ontology first and young. Neo4j's own banner points users of its reference tool to a hosted service, Neo4j Document Intelligence in Aura [19].

## Fundamental papers

The relations among these are on the group page [Building knowledge graphs with LLMs: papers](../papers/llm-kg-construction.md), which keeps five of them (AutoSchemaKG is in its further reading):

- **Language Models are Open KGs (2020):** a graph built from pre-trained language models "without human supervision" [33].
- **Zhu et al. (2023):** LLMs tested for graph construction on eight datasets; GPT-4 judged a better inference assistant than few-shot extractor [34].
- **Pan et al. (2023):** the roadmap joining language models and graphs, construction among its parts [15].
- **EDC (2024):** extract, define, canonicalize, with a self-generated schema when none is given [1].
- **AutoSchemaKG (2025):** schema induction at web scale [3].
- **Bian survey (2025):** separates schema-based from schema-free paradigms [35].

SPIRES (2023) [4], KGGen (2025) [2] and the benchmark paper Text2KGBench (2023) [5] are used on this page but are not on that list; the last has its entry in [Benchmarks](../benchmarks/text2kgbench.md).

## What is measured, and by whom

No experiment in this repository tests this trend; see [Experiments](../experiments/README.md). Every result below is from the authors of the method or of the benchmark. An independent comparison of induced against human schemas on one corpus is **unstated** in the sources read.

| Result | Benchmark or data | Run by | Source |
|---|---|---|---|
| Induced schemas reach 92% semantic alignment with human-crafted ones; beats baselines on [multi-hop questions](../index/multi-hop-question-answering.md) | ATLAS graphs | AutoSchemaKG authors (first-party) | [3] |
| KGGen outperforms other extractors | MINE, released with KGGen | KGGen authors (first-party) | [2] |
| Seven frontier models give relevant, document-faithful triples zero-shot | CMW-Lit, built by the authors | Chen et al. (first-party data) | [6] |
| SCION-lite has the highest F1 (a score that balances precision and recall) among the baselines and references its abstract lists; the authors say the results are not "claims that induced schemas surpass human ontology design" | SCOPE | SCOPE authors (first-party) | [10] |
| MAGG: +47% strict triple F1 over flat insertion. Run in fixed-schema mode, so it measures governed admission of triples, not schema induction | SciERC | MAGG authors (first-party) | [11] |
| MAGG: +9.0 exact match over [Microsoft GraphRAG](../projects/microsoft-graphrag.md). A question-answering comparison, not a test of the induced schema | [MuSiQue](../datasets/musique.md) | MAGG authors (first-party) | [11] |
| Reflection-based extraction best on comprehensiveness, precision and relevance, single-pass best on faithfulness; [LLM judges](../index/llm-as-judge.md) with bias controls a reliable, cheaper alternative to human annotation | FinReflectKG-EvalBench | benchmark authors (first-party) | [14] |
| Task A semantic graph similarity 0.7416; no non-taxonomic relations extracted | LLMs4OL 2026 challenge | one entrant, self-reported | [13] |

The MAGG paper says it does not "separately evaluate induced domain quality", so the quality of MAGG's induced types is **unstated** [11].

## Assessment

*Reading:* the shift is real in papers and thin in mature code. Strengths: the schema step has its own benchmarks (Text2KGBench, MINE, SCOPE) and the cost argument is concrete. Weaknesses: every number above is first-party or one entrant's self-report; induced schemas are scored against human schemas, so agreement measures resemblance, not usefulness; and among the most-starred tools, those that need a schema take it from a person (Hyper-Extract templates, GLiNER labels, OntoGPT LinkML [22][20][23]), while the most-starred of all, LLM Graph Builder, leaves it optional [32]. One vendor package goes further: the `SimpleKGPipeline` of [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md) has had the LLM extract the schema by default, when the user gives none, since version 1.8.0 (published 20250703) [36][37][38]; how often users keep the extracted schema is **unstated**. The likely path is a hybrid: a drafted schema with a review step. Helix Foundry describes a person reviewing an agent's draft [25]; MAGG keeps a review step but gives it to LLM reviewer agents, "not human experts" [11]. No source read tests this forecast.

*Reading:* volume. The keyword query in Sources 17 returned 75 results for 20251102 to 20261102 against 64 the year before (x1.17); the any-LLM control grew x1.38 (44,692 against 32,396), read 20261102 21:21 UTC. The topic grew no faster than the field, so the status is steady. By hand on 20261102 21:23 UTC, 13 of the newest 40 titles name graph construction, ontology learning or schema generation, and about 7 more are borderline. Keyword hits are not "papers in the field".

## Signals to watch

- Whether other active, non-research projects follow neo4j-graphrag-python, which ships LLM schema extraction as its default when no schema is given [36][37][38], and whether users keep the schema it extracts.
- An independent comparison of induced and given schemas on one corpus and one downstream task.
- Whether Neo4j's Graph Builder is wound down in favour of its hosted service [19], and whether Carrel's Agent Loop is built [26].
- Whether "context graph" gains a definition beyond a label.

## Sources

1. https://arxiv.org/abs/2404.03868 : EDC, abstract (read 20261102 21:23 UTC)
2. https://arxiv.org/abs/2502.09956 : KGGen and MINE, abstract (read 20261102 21:23 UTC)
3. https://arxiv.org/abs/2505.23628 : AutoSchemaKG, abstract (read 20261102 21:23 UTC)
4. https://arxiv.org/abs/2304.02711 : SPIRES, abstract (read 20261102 21:23 UTC)
5. https://arxiv.org/abs/2308.02357 : Text2KGBench, abstract (read 20261102 21:23 UTC)
6. https://arxiv.org/abs/2510.11297 : Are LLMs effective KG constructors, abstract (read 20261102 21:23 UTC)
7. https://arxiv.org/abs/2603.20059 : DIAL-KG, abstract (read 20261102 21:23 UTC)
8. https://arxiv.org/abs/2604.02618 : OntoKG, abstract (read 20261102 21:19 UTC)
9. https://arxiv.org/abs/2605.29168 : Better Later Than Sooner, abstract (read 20261102 21:23 UTC)
10. https://arxiv.org/abs/2607.21610 : SCOPE and SCION, abstract (read 20261102 21:19 UTC)
11. https://arxiv.org/abs/2608.28642 : MAGG, abstract and full text (PDF): LLM reviewer agents, fixed-schema mode on SciERC, limitations (read 20261102 21:19 UTC)
12. https://arxiv.org/abs/2609.31663 : ontology-driven construction, power-grid reports, abstract (read 20261102 21:23 UTC)
13. https://arxiv.org/abs/2608.27101 : LLMs4OL 2026 entry, abstract (read 20261102 21:23 UTC)
14. https://arxiv.org/abs/2510.05710 : FinReflectKG-EvalBench, abstract, read directly through the arXiv API (read 20261102 21:19 UTC)
15. https://arxiv.org/abs/2306.08302 : Pan et al., roadmap, abstract (read 20261102 21:23 UTC)
16. https://arxiv.org/abs/2311.08526 : GLiNER, abstract: a compact model that identifies "any type of entity" (read 20261102 21:23 UTC)
17. https://export.arxiv.org/api/query : N = totalResults of `(abs:"schema induction" OR abs:"ontology induction" OR abs:"schema-free" OR abs:"schema generation" OR abs:"ontology generation" OR abs:"knowledge graph construction" OR abs:"ontology learning" OR abs:"schema discovery") AND (abs:LLM OR abs:LLMs OR abs:"large language model" OR abs:"large language models")` with submittedDate 202511020000 to 202611022359: 75, and 202411020000 to 202511012359: 64; control `(abs:LLM OR abs:LLMs OR abs:"large language model" OR abs:"large language models")` alone: 44,692 against 32,396; `abs:"context graph" OR abs:"context graphs" OR ti:"context graph" OR ti:"context graphs"`: 34 against 9; the 40 newest results of the first query, sorted by submission date, read by title (all read 20261102 21:21 to 21:23 UTC; the first run on 20261102 19:27 to 20:28 UTC gave the same counts)
18. kb-kg/landscape/20261030_1954-github/repos.tsv : stars, push dates, commits in 90 days (snapshot 20261030 19:54 UTC; read 20261102 21:20 UTC)
19. https://github.com/neo4j-labs/llm-graph-builder : `frontend/src/components/Layout/Header.tsx` banner text; pull request 1644, base branch `dev`, merged 20261016 06:03 UTC; commit counts since 20260801 on `main` and `dev` (read 20261102 20:12 UTC; pull request and banner text in `main` re-read 20261102 21:20 UTC)
20. https://github.com/yifanfeng97/Hyper-Extract/blob/main/README.md : templates, methods, provenance (read 20261102 20:11 UTC)
21. https://github.com/yifanfeng97/Hyper-Extract/blob/main/LICENSE : Apache License 2.0 text (read 20261102 21:20 UTC); wording changes noted on the archive page kb-kg/projects/hyper-extract.md (read 20261030 19:44 UTC); https://api.github.com/repos/yifanfeng97/Hyper-Extract/releases : 21 releases, latest v0.11.0 (read 20261102 21:20 UTC; the latest-release call was run again 20261102 22:52 UTC with the same result, published 20261029)
22. https://github.com/urchade/GLiNER/blob/main/README.md : run-time labels, joint relation extraction (read 20261102 21:20 UTC)
23. https://github.com/monarch-initiative/ontogpt/blob/main/README.md : LinkML schema, grounding, `AUTO:` prefix (read 20261102 20:11 UTC)
24. https://github.com/microsoft/graphrag/blob/main/docs/index/default_dataflow.md : per-text-unit entity and relationship extraction by the LLM (read 20261102 20:13 UTC)
25. https://github.com/HelixDB/helix-foundry/blob/main/README.md : ontology agent drafts, "Review the draft", values keep their row or quote (read 20261102 21:20 UTC)
26. https://github.com/FengZhenfei/carrel/blob/main/README.md : ontology-augmented generation, sources retained, Agent Loop status (read 20261102 21:20 UTC)
27. https://github.com/databrickslabs/ontobricks/blob/main/README.md : Databricks tables to a graph; OWL, R2RML, SPARQL (read 20261102 21:20 UTC)
28. https://github.com/liliang-cn/cortexdb/blob/main/README.md : "Palantir-style ontology with governed actions"; memory and graph in one SQLite file; RDF knowledge graph (read 20261102 21:20 UTC)
29. https://github.com/HKUST-KnowComp/AutoSchemaKG : repository metadata and LICENSE (read 20261102 21:20 UTC)
30. https://api.github.com/repos/neo4j-labs/llm-graph-builder/license, https://api.github.com/repos/yifanfeng97/Hyper-Extract/license, https://api.github.com/repos/urchade/GLiNER/license, https://api.github.com/repos/monarch-initiative/ontogpt/license, https://api.github.com/repos/HKUST-KnowComp/AutoSchemaKG/license, https://api.github.com/repos/HelixDB/helix-foundry/license, https://api.github.com/repos/FengZhenfei/carrel/license : LICENSE file name and SPDX id for each repository in the table (read 20261102 21:20 UTC)
31. https://github.com/stair-lab/kg-gen : repository metadata; the licence endpoint returned none; the README ends "The MIT License." (read 20261102 21:20 UTC)
32. https://github.com/neo4j-labs/llm-graph-builder/blob/main/README.md : schema support: a custom schema can be set in the settings (read 20261102 21:20 UTC)
33. https://arxiv.org/abs/2010.11967 : Language Models are Open Knowledge Graphs, abstract (read 20261102 21:22 UTC)
34. https://arxiv.org/abs/2305.13168 : Zhu et al., LLMs for knowledge graph construction and reasoning, abstract (read 20261102 21:22 UTC)
35. https://arxiv.org/abs/2510.20345 : Bian, LLM-empowered knowledge graph construction survey, abstract (read 20261102 21:22 UTC)
36. https://github.com/neo4j/neo4j-graphrag-python/blob/main/CHANGELOG.md : 1.8.0: "Added support for automatic schema extraction from text using LLMs. In the `SimpleKGPipeline`, when the user provides no schema, the automatic schema extraction is enabled by default." (read 20261102 22:24 UTC)
37. https://github.com/neo4j/neo4j-graphrag-python/releases : the release list through the GitHub API: 1.8.0 published 2025-07-03 15:05 UTC (read 20261102 22:24 UTC)
38. https://github.com/neo4j/neo4j-graphrag-python/blob/main/src/neo4j_graphrag/experimental/pipeline/config/template_pipeline/simple_kg_builder.py : `EXTRACTED` is "same as no schema, schema will be extracted by LLM" (read 20261102 22:30 UTC)
39. [Semantica](../projects/semantica.md), the project page of this documentation, written from primary sources read on 20261103 and checked by a second agent: licence, ontology and temporal features read against the code, no independent evaluation found; stars from the snapshot [18]
