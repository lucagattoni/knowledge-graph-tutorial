---
slug: ontogpt
repo: monarch-initiative/ontogpt
tier: card
category: core
snapshot: 20261030 19:39 UTC
---

# OntoGPT

| | |
|---|---|
| Repository | https://github.com/monarch-initiative/ontogpt [1] |
| Licence | BSD-3-Clause, from the `LICENSE` file (28 lines: copyright notice, three conditions, disclaimer; read in full) [2]. `pyproject.toml` says "BSD-3"; the README has no licence section [3][8]. |
| Language | Python package; GitHub's primary language is Jupyter Notebook (12.8 MB of notebooks, 1.9 MB of Python) [1] |
| Stars, forks | 1,080, 126 (20261030 19:39 UTC; not in the landscape snapshot, so no heuristic flag) [1] |
| Created, last push | 20230103 16:53 UTC, 20260910 16:36 UTC [1] |
| Latest release | v1.2.0, 20260909 20:58 UTC; the previous one, v1.1.1, is 20260407 [4]. PyPI also has 1.2.0 [5]. |
| Status | active (pushed 50 days before the read, within 90 days); not archived [1] |
| Paper, docs | SPIRES paper, Bioinformatics 40(3), March 2024, doi 10.1093/bioinformatics/btae104 [6]; docs at https://monarch-initiative.github.io/ontogpt/ [1][7] |

## What it is

A Python package, part of the Monarch Initiative, that extracts structured information from text with LLMs, instruction prompts and ontology-based grounding [3]. Its main method is SPIRES: given a LinkML schema and free text, it returns knowledge that conforms to the schema, as JSON, YAML, RDF or OWL, without training data [7]. The paper's abstract claims accuracy "comparable to the mid-range of existing Relation Extraction methods" and far better identifier grounding than an LLM alone [6]. Reported figures: 98 of 100 random GO terms grounded correctly with GPT-3.5-turbo against 3 without SPIRES; on the BC5CDR task, F-scores of 36.64 to 43.80, "just below the average" of the 18 original teams [6]. The paper dates from March 2024; I found no later or outside evaluation, and the README gives no figures [3].

## How it works

The user supplies a LinkML schema (a template; the repository holds 71 template files) and annotators for entity fields. SPIRES prompts the LLM one class at a time, with only that class's fields, then parses the reply [3][7][10]. The model is asked for names, not identifiers; names are grounded through OAK annotators, and each identifier is validated against its ontology, repaired where possible or rewritten with an `AUTO:` prefix [3][7]. LiteLLM reaches many providers; Ollama runs local models; LiteLLM caches responses on disk [3][7]. Interfaces: command line, Python, a basic web app and four Agent Skills [3][11]; no path in the repository tree mentions MCP [10].

## Status and direction

Active, with no commit since 20260910: 38 commits on main since 20260801, all in September; 55 releases since v0.1.0 (20230105); 31 contributors, 69 open issues, 11 open pull requests [4][9]. Recent commit subjects cover a "Why OntoGPT?" README section, identifier-rejection handling in the mapper and a new `pet_breed` template [9]. Roadmap: unstated.

## Sources

1. https://github.com/monarch-initiative/ontogpt : repository metadata and language bytes via the GitHub API (read 20261030 19:39 and 19:44 UTC)
2. https://github.com/monarch-initiative/ontogpt/blob/main/LICENSE : BSD 3-clause text (read 20261030 19:40 UTC)
3. https://github.com/monarch-initiative/ontogpt/blob/main/README.md : description, "Why OntoGPT?", model APIs, citation (read 20261030 19:39 UTC)
4. https://github.com/monarch-initiative/ontogpt/releases : 55 releases, v0.1.0 to v1.2.0 (read 20261030 19:40 UTC)
5. https://pypi.org/pypi/ontogpt/json : version 1.2.0, upload 20260909 20:58 UTC (read 20261030 19:40 UTC)
6. https://pmc.ncbi.nlm.nih.gov/articles/PMC10924283/ : the SPIRES paper, abstract and full text read through the Europe PMC REST service (read 20261030 19:44 UTC)
7. https://github.com/monarch-initiative/ontogpt/blob/main/docs/operation.md : working mechanism and term validation; also `docs/index.md` and `docs/evaluations.md` (read 20261030 19:44 UTC)
8. https://github.com/monarch-initiative/ontogpt/blob/main/pyproject.toml : version and licence field (read 20261030 19:44 UTC)
9. https://github.com/monarch-initiative/ontogpt/commits/main : commits since 20260801, contributors, open issues and pull requests (read 20261030 19:40 UTC)
10. https://github.com/monarch-initiative/ontogpt/tree/main/src/ontogpt/templates : template file count (71 YAML files) and a search of all 521 file paths for "mcp" (none), from the repository tree (read 20261030 19:44 UTC)
11. https://github.com/monarch-initiative/ontogpt/blob/main/skills/README.md : the four Agent Skills (read 20261030 19:44 UTC)
