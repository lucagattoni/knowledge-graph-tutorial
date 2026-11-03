---
type: project
repo: semantica-agi/semantica
trends: [llm-kg-construction, agent-memory]
updated: 20261103 09:58 UTC
---

# Semantica

This page answers what Semantica is, which of its README claims the code supports, and who has measured it. It puts an [ontology](../index/ontology.md), time-stamped facts and recorded decisions under an AI agent. The only scores published are the authors' own, and they measure speed, not quality.

| Field | Value |
|---|---|
| Repository | https://github.com/semantica-agi/semantica [1] |
| Licence | MIT, from the `LICENSE` file: 21 lines, "Copyright (c) 2026 Semantica", identical to the SPDX MIT text once whitespace is ignored [2]. GitHub, `pyproject.toml`, the README and PyPI also say MIT [1][3][5][7]. It is permissive, so the code is not a read-only reference. |
| Trends | [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md) · [Agent memory](../trends/agent-memory.md) |

## What it is

Semantica is a Python package with a command line, a REST API, two MCP ([Model Context Protocol](../index/model-context-protocol.md)) servers and a browser workbench [3][11]. The README calls it "Graph-Native Infrastructure for Context and Accountable AI Systems", a layer beneath an existing [language model](../index/large-language-model.md), vector store and agent framework [3]. The pitch is aimed at regulated domains: facts keep [provenance](../index/provenance.md), and each agent decision is a graph node with causal links; the README says audit trails "fall out of that structure for free" [3]. An "Enterprise" section offers support and services; prices and terms are **unstated** [3].

*Against the chapter.* The [trend page](../trends/llm-kg-construction.md) groups Helix Foundry, Carrel, OntoBricks and CortexDB as ontology-grounded context graphs for agents [19]. Semantica's README describes the same kind of asset; its code applies the ontology after extraction (below). [Graphiti](./graphiti.md) sets `invalid_at` and `expired_at` on an edge that a contradicting fact supersedes; Semantica has the time model, but a search of the package found no step that closes a fact when a contradicting one arrives (below) [19][10]. [OntoGPT](./ontogpt.md) fixes the schema first and grounds names to ontology identifiers; [Cognee](./cognee.md) can ground entities to an OWL file [19]. [Neo4j's graph builder](./llm-graph-builder.md) lets the model pick types unless given a schema [19]; Semantica's default extractors use no large language model [9].

## How it works

The pipeline runs ingest, parse, normalize, split, extract, conflict detection and deduplication into a graph, with ontology, reasoning, provenance and decisions on top. Storage is RDF stores (Oxigraph, Blazegraph, Jena, RDF4J), property-graph stores ([Neo4j](./neo4j.md), [FalkorDB](./falkordb.md), Apache AGE, Neptune) or vector stores [3]. The table sets README claims against the source at commit `4b6de4e` (20261103 05:29 UTC).

| README claim | What the code shows | Source |
|---|---|---|
| No LLM required to build the graph | True of the default path, which uses no large language model. Entities come from spaCy's small model `en_core_web_sm` (an optional extra) or, without it, pattern matching and regular expressions. Relations default to `pattern`; if that returns nothing, a fallback links entities within 100 characters as `related_to` at confidence 0.5 and, as a last resort, adjacent entities at 0.3. LLMs are opt-in (`method="llm"`). | [3][9] |
| [OWL](../index/owl.md) and SHACL ontologies | Real. `OntologyGenerator` infers classes and properties from the entities and relations it is given; `OWLGenerator` writes OWL (Turtle by default); `LLMOntologyGenerator` drafts one from text. [SHACL](../index/shacl.md) shapes are generated from it and checked with pySHACL (optional extra `shacl`) by `OntologyEngine.validate_graph` and `semantica validate shacl`. | [8] |
| `OntologyValidator().validate()`, commented "Validate against SHACL shapes" | A placeholder. It warns only when a dictionary lacks `classes` or `properties`; a file path is not checked. Its consistency and satisfiability branches are `pass`, under "Placeholder implementation for now", so the README's printed `consistent=True, satisfiable=True` is the dataclass default. The `reasoner="hermit"` default only reaches a log message, and `owlready2` is in no dependency list. The same code sits behind `semantica ontology validate` ("Check the generated ontology for consistency and satisfiability") and the ontology quality gate. The real SHACL check is a separate path; the repository's own reference page calls a `validate_graph` that `OntologyValidator` lacks. | [3][8] |
| Ontology-constrained extraction | After extraction only. `SchemaValidator` filters entities and relations by concept, predicate, domain and range, and `bootstrap_schema` induces a draft ontology ([schema induction](../index/schema-induction.md)). No extractor takes an ontology (only plain lists of types), the CLI `extract` has no ontology option, and the one pipeline template that mentions ontology infers classes from extracted entities. A text search finds no caller of either function in the package and no registry or string-keyed dispatch naming them; both are exported for user code. | [9] |
| [Bi-temporal](../index/bi-temporal-model.md) facts, "time travel" | `BiTemporalFact`, a normalising wrapper over plain relationship dictionaries, has `valid_from`, `valid_until`, `recorded_at` and `superseded_at`; `TemporalGraphQuery` takes a `time_axis` (valid, transaction or both). `ContextGraph.state_at` uses valid time only; its node and edge classes carry only `valid_from` and `valid_until`. Only `TemporalVersionManager.apply_revision` sets `superseded_at`, and nothing in `semantica/` calls it; `ContextGraph.retract_node` closes a validity window by explicit call and has no caller either. The `conflicts` package can pick the newest of two values but sets no time bound. | [10] |
| MCP server with 15 tools (the README table) | `semantica-mcp`, the README's start command, runs a server defining 16 (the table omits `link_decisions`) and none of the four document tools of the v0.7.0 notes. `semantica mcp start` runs a second package, `semantica_mcp`, with 22 including those four; 13 names are shared. | [3][11] |

Reasoning offers forward chaining, Rete (a rule-matching algorithm), [Datalog](../index/datalog.md) and [SPARQL](../index/sparql.md); the README calls its Rete matcher "intentionally simple in this release" [3]. SPARQL execution is new in 0.7.0: `execute_query` earlier returned an empty result, and from 0.6.7 raised `NotImplementedError` [6]. Retrieval has `local`, `global`, `drift` and `hybrid` modes; global and DRIFT answer from model-written [community reports](../index/community-report.md), under the names [Microsoft GraphRAG](./microsoft-graphrag.md) uses [3][19]. `AgentMemory` stores and retrieves items by vector similarity and updates the graph [12].

## Evidence

Every number the project publishes is first-party.

| Claim | Stated setup | Check |
|---|---|---|
| Node search 24 ms to 0.004 ms (6,000 times) | v0.5.0, one 118,000-node graph, 64 GB | RELEASE_NOTES give the same pair for "Indexed Search" [3][13] |
| Deduplication 6.98 times; candidate generation 63.6% faster | Same heading; the footnote calls them "historical measurements" | CHANGELOG, 0.3.0-beta (20260307, before 0.5.0): 0.259 s to 0.094 s "for 100 entities"; 83 ms against 579 ms for "Semantic Relationship Deduplication v2" (synonym mapping, hash matching), size not given [3][6] |
| Embedding cache 10 times | "revision-based cache" | RELEASE_NOTES: "10x+" for repeated requests, no setup [13] |

No extraction, retrieval or question-answering result appears in the README, the docs home page or the CHANGELOG [3][6][16]. A benchmark harness in the tree has adapters for Semantica, Mem0, Graphiti and Cognee. Its README says "no result table is published yet" [12].

**Independent evaluations: none found** (20261103). The arXiv API (titles, abstracts and metadata, not full text) returned four records for `semantica`, none this project, and none for `semantica-agi`, `getsemantica` or combinations with "context graph", ontology, provenance, benchmark, decision or "agent memory" [17]. A paper search (nine candidates) named no Semantica study [17]. Web searches returned the project's pages, aggregators and write-ups with no measurement of their own: a self-described "hands-on review" (20260818) repeats the README table and calls the 6,000 times "not a portable benchmark"; a company blog and a services firm's listing report none. One Medium article could not be read [18].

## Status and direction

*Release.* v0.7.0, 20260922 11:18 UTC, is GitHub's latest release and PyPI's latest version; none since (42 days) [4][5]. `main` already reads 0.8.0 in `pyproject.toml` and `CITATION.cff`, whose release date 20260905 is the v0.6.8 tag's day [4][7]. The README says Python 3.10 support "ended in 0.8.0", which is not released [3].

*Activity.* 1,065 commits to `main` from 20260804 to 20261103 (computed): 526 in August (from the 4th), 385 in September, 147 in October, 7 since 1 November; per day, October ran at about a quarter of August. 128 linked accounts wrote them; the busiest wrote 325 [14]. At 20261103 09:47 UTC: 73 open issues, 57 open pull requests, 138 contributors [15]. `main` was still at `4b6de4e` at 09:41 UTC [1].

*Direction.* Unreleased work adds trust-tier grading of retrieved context, snapshot-consistent context assembly, a relational-schema mapper and evaluators that score decisions as they are recorded [6]. The README and `docs/community.md` mention a roadmap, the latter "the public roadmap" on GitHub; no roadmap file, label or issue was found, so its content is **unstated** [1][3].

*Reading:* a broad, fast-moving project whose README describes more than the code does in at least one place (the ontology validator, which also sits behind a CLI command). This rests on the code read at `4b6de4e` and on CHANGELOG entries that record placeholders being replaced, among them SPARQL execution and a "stability" metric that was a constant [6][8]. It is a provenance and decision layer on a conventional extraction pipeline, not the "Ontology first" row of the trend's table. The default extractors' quality is **unstated**: no source measures it.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)

**Projects**

- [Projects](README.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://api.github.com/repos/semantica-agi/semantica : description, topics, archived flag (false), licence field, creation date 20250625, default branch, `/commits/main` (head `4b6de4e`, 20261103 05:29 UTC), `/labels` and an issue search for "roadmap" (none); `.../contents/` root listing (no roadmap file) (read 20261103 09:41 UTC; labels and search 09:47 UTC)
2. https://api.github.com/repos/semantica-agi/semantica/license and https://api.github.com/licenses/mit : the `LICENSE` text (21 lines, "Copyright (c) 2026 Semantica") compared with the SPDX MIT text, whitespace ignored, "[year] [fullname]" filled: identical; checked again on a fresh shallow clone (read 20261103 09:41 UTC)
3. https://github.com/semantica-agi/semantica/blob/main/README.md : self-description, pipeline, storage, claims (lines 69 to 71 on audit trails, 560 Rete note, 721 validator example, 1178 to 1187 performance table and footnote, 1401 to 1435 MCP tool table, 1511 to 1537 v0.7.0 and Python notes, 1599 Enterprise section), plus `docs/community.md` line 63 (roadmap mention) (read 20261103 09:40 UTC, fresh shallow clone at `4b6de4e`)
4. https://api.github.com/repos/semantica-agi/semantica/releases , `/releases/latest` and `/tags` : v0.7.0 (20260922 11:18 UTC) latest; v0.6.5 to v0.6.8 dated 20260811, 20260820, 20260828, 20260905 (read 20261103 09:41 UTC)
5. https://pypi.org/pypi/semantica/json : latest 0.7.0, MIT, `requires_python` `>=3.10,<3.14`, upload 20260922 (read 20261103 09:41 UTC)
6. https://github.com/semantica-agi/semantica/blob/main/CHANGELOG.md : Unreleased section (line 10); 0.7.0 entry on `SPARQLReasoner.execute_query` (line 238); 0.6.7 entries on `execute_query` and `analyze_evolution` (lines 673 and 675); 0.3.0-beta deduplication entries (lines 1957 and 1959), at commit `4b6de4e` (read 20261103 09:40 UTC)
7. https://github.com/semantica-agi/semantica/blob/4b6de4e/pyproject.toml and `CITATION.cff` : version 0.8.0, `requires-python >=3.11,<3.14`, 22 core dependencies, MIT, `shacl` extra (line 124), entry point `semantica-mcp = "semantica.mcp_server:main"` (line 333), `semantica_mcp*` packaged (line 338); `date-released: 2026-09-05` (`main` at commit `4b6de4e`, fresh shallow clone, read 20261103 09:40 UTC)
8. https://github.com/semantica-agi/semantica/blob/4b6de4e/ plus `semantica/ontology/ontology_validator.py` (module docstring lines 1 to 5; `validate`, line 326; placeholder comment at 340, `pass` at 350 and 354, `reasoner="hermit"` at 307, used at 336 in a log message; `ValidationResult` defaults, lines 291 to 297; `run_shacl_validation`, line 148), `ontology/engine.py` (`validate_graph`, line 313; `validate`, line 597), `ontology/quality_gate.py` (line 194), `ontology/owl_generator.py`, `ontology/ontology_generator.py`, `ontology/llm_generator.py`, `cli.py` (`ontology validate`, lines 4894 to 4925; `validate shacl`, line 4650) and `docs/reference/ontology.md` (line 163); HermiT and owlready2 occur in docstrings (`ontology/__init__.py` line 15, `ontology_generator.py` line 64, `methods.py` line 53, validator lines 5 and 341), the package guide `ontology_usage.md`, the `reasoner` default, and in no dependency or lock file; same commit (read 20261103 09:40 UTC)
9. https://github.com/semantica-agi/semantica/blob/4b6de4e/ plus `semantica/semantic_extract/ner_extractor.py` (default method `ml`, line 124; regular expressions from line 1327), `methods.py` (`extract_entities_ml` falls back to pattern extraction), `named_entity_recognizer.py` (line 100), `relation_extractor.py` (default `pattern`, line 85; co-occurrence at 0.5, lines 573 to 590; last resort at lines 484 to 486 and from 505), `schema.py`, `schema_validator.py`, `llm_extraction.py`, `ontology/bootstrap_schema.py`, `cli.py` (`extract` options, line 2827) and `pipeline/pipeline_templates.py` (lines 203 to 239); a text search of the whole clone found `SchemaValidator`, `ExtractionSchema` and `bootstrap_schema` only in those files, two package `__init__` exports (lazy table in `semantic_extract/__init__.py`), tests, the README and the CHANGELOG; "ontology" in `semantic_extract/` outside the two schema files occurs once, in a docstring (read 20261103 09:40 UTC)
10. https://github.com/semantica-agi/semantica/blob/4b6de4e/ plus `semantica/kg/temporal_model.py` (`BiTemporalFact`, line 28), `kg/temporal_query.py` (`time_axis`, lines 114 and 800; `apply_revision`, line 1401, sets `superseded_at` at line 1440), `context/context_graph.py` (node and edge classes, lines 420 and 463; `is_active`, line 431; `retract_node`, line 2700; `state_at`, line 3757) and `conflicts/*.py`; a text search of `semantica/` found one assignment of `superseded_at` (in `apply_revision`) and no caller of `apply_revision(` or `retract_node`; the other `valid_until` assignments are constructors, loaders and caller-supplied values (including the Explorer session), bounds extracted from text (`semantic_extract/methods.py` line 2381) and a default read from the provenance revision chain (`provenance/manager.py` line 957) (read 20261103 09:40 UTC)
11. https://github.com/semantica-agi/semantica/blob/4b6de4e/ plus `semantica/mcp_server/__init__.py` (`TOOLS` from line 706: 16 names, none of the four document tools), `semantica_mcp/mcp/tools/*.py` (decisions 6, export 2, extraction 3, graph 5, reasoning 2, retrieval 4 = 22 names, counted by syntax tree, including `store_document`, `retrieve_context`, `update_document`, `remove_document`), `semantica/cli.py` (`mcp start` runs `semantica_mcp.mcp.server`, about line 6929) (read 20261103 09:40 UTC)
12. https://github.com/semantica-agi/semantica/blob/4b6de4e/ plus `semantica/benchmarks/README.md` (harness, datasets, adapters, "no result table is published yet") and `semantica/context/agent_memory.py` (module docstring; `store`, `retrieve`, `forget`) (read 20261103 09:40 UTC)
13. https://github.com/semantica-agi/semantica/blob/4b6de4e/RELEASE_NOTES.md (the 0.5.0 notes; lines 49 and 106 to 107): the "Indexed Search" and "Performance Benchmarks" entries (read 20261103 09:40 UTC)
14. https://api.github.com/repos/semantica-agi/semantica/commits?since=2026-08-04T00:00:00Z : 1,065 commits, paged; dates, authors, subjects (read 20261103 09:47 UTC; the writer's count of 09:26 UTC was the same)
15. https://api.github.com/search/issues (open issues 73, open pull requests 57 for the repository) and `.../contributors` (138) (read 20261103 09:47 UTC)
16. https://docs.getsemantica.ai/ : home page; no benchmark or comparison published (read 20261103 09:48 UTC)
17. https://export.arxiv.org/api/query : `all:"semantica"` (4 records, none this project), `all:"semantica-agi"`, `all:"getsemantica"` (0), and `semantica` combined with "context graph", ontology, "knowledge graph", provenance, decision, benchmark, "agent memory" (0) (read 20261103 09:50 UTC); a paper-discovery query (alphaXiv) for Semantica with context graph, provenance and ontology, nine candidates, none about this project (read 20261103 09:52 UTC)
18. Web searches of 20261103 for reviews, benchmarks and comparisons (results are leads); https://andrew.ooo/posts/semantica-review-graph-native-audit-trails-ai-agents/ (20260818, "Hands-on review"; repeats the README table, runs `semantica doctor` only); https://dev.co/ai/frameworks/semantica (a services firm's listing, editorial ratings, no measurement); https://zentor.ai/blog/what-is-semantica (a company blog, 20260810, updated 20261021: describes the README, reports no benchmark); https://blog.gopenai.com/semantica-the-missing-graph-layer-for-ai-agents-4225c9ae4a92 (HTTP 403, not read) (read 20261103 09:51 UTC to 09:53 UTC)
19. Pages of this documentation, for what each states: [the trend](../trends/llm-kg-construction.md) (section "Ontology-grounded context graphs"), [Graphiti](./graphiti.md), [OntoGPT](./ontogpt.md), [Cognee](./cognee.md), [Neo4j LLM Graph Builder](./llm-graph-builder.md), [Microsoft GraphRAG](./microsoft-graphrag.md) (read 20261103 09:34 UTC)

Further reading in the archive: [Semantica entry](../../kb-kg/projects/semantica.md). Papers: [LLM knowledge-graph construction group](../papers/llm-kg-construction.md).
