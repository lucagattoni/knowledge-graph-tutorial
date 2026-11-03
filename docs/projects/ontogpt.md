---
type: project
repo: monarch-initiative/ontogpt
trends: [llm-kg-construction]
updated: 20261102 23:17 UTC
---

# OntoGPT

This page answers what OntoGPT is, how its SPIRES method turns text into schema-shaped, ontology-grounded data, what its authors measured, and what the repository shows about its current state. It is the schema-first end of the trend on [building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

| Field | Value |
|---|---|
| Repository | https://github.com/monarch-initiative/ontogpt |
| Licence | BSD-3-Clause, from the `LICENSE` file: 28 lines, a 2022 copyright notice naming seven authors, three conditions and a disclaimer, read in full [2]. GitHub classifies it the same way [2]. |
| Trends | [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md) |

## What it is

OntoGPT is a Python package from the Monarch Initiative. It extracts structured information from text with [large language models](../index/large-language-model.md), instruction prompts and [ontology](../index/ontology.md)-based grounding [3]. Its main method is SPIRES (Structured Prompt Interrogation and Recursive Extraction of Semantics). The user gives a [LinkML](../index/linkml.md) schema and a text. The package returns data that conforms to the schema, as YAML, JSON, RDF or OWL, with no training data [3][4][7]. The paper presents it as zero-shot learning [7].

*Reading:* the trend title runs from fixed schemas to induced ones. OntoGPT is the fixed-schema case: a person writes the schema, the model fills it. The sources read mention no schema induction. For the small-model alternative see [GLiNER](./gliner.md).

## How it works

1. The user supplies a LinkML schema, called a template. The repository holds 71 template files [10]. Entity fields are tagged with annotators for grounding, which is [entity linking](../index/entity-linking.md) to ontology terms [3][4].
2. SPIRES prompts the model one class at a time, with only that class's fields. Each prompt stays small, and the assembled output conforms to the whole schema [3].
3. The model is asked for names, not identifiers. Names are grounded against the real ontology through OAK annotators. A name that cannot be grounded gets the `AUTO:` prefix instead of a guess [3].
4. Since v1.2.0, `linkml-term-validator` checks every grounded identifier: does the term exist, is it obsolete, does the extracted label match its label or a synonym. Invalid identifiers are repaired in a fixed order, from the obsolete term's own replacement, to re-grounding, to a label search. The decisions are written to a `validation` section. It is on by default for the extraction commands and off with `--no-validate-terms` [4].

LiteLLM reaches many providers and caches responses on disk. Local models run through Ollama with an `ollama/` model prefix. Without `--model`, the README says the default is `gpt-5.5` [3][4]. The interfaces are a command line, Python, a basic web app and four Agent Skills, which teach a coding agent to extract, pick a template, write a template and troubleshoot [3][6]. MCP (Model Context Protocol): unstated; none of the 600 paths in the repository tree contains "mcp" [10].

## Evidence

All published results are first-party: the SPIRES paper (Bioinformatics 40(3), March 2024) is by the package's authors [7]. The README gives no figures [3].

| Test | Result | Setup |
|---|---|---|
| Grounding 100 random GO terms | 98 correct (GPT-3.5-turbo); 97 correct (GPT-4-turbo) | SPIRES |
| Same, without SPIRES | 3 correct | GPT-3.5-turbo alone |
| BC5CDR chemical-induces-disease triples, F-score | 41.16 (precision 0.43, recall 0.39) | GPT-3.5-turbo, with chunking |
| Same | 36.64 (precision 0.63, recall 0.26) | GPT-3.5-turbo, no chunking |
| Same | 43.80 (precision 0.69, recall 0.32) | no chunking; the model is not named in the sentence read |

The BC5CDR test used all 500 test abstracts and 1,066 triples, with no task-specific training [7]. The authors place the result "just below the average" of the 18 original challenge teams. They note that the best score in that challenge was 0.57, from a model trained on carefully engineered examples [7]. The abstract calls SPIRES accuracy "comparable to the mid-range of existing Relation Extraction methods" [7]. The documentation lists the same test as `EvalCTD`, with 500 inputs and a subset run by default [5].

The paper is from 2024. The term-validation step, and the default models in the README, date from September 2026 [4][9]. So the paper's grounding figure describes an earlier pipeline. No evaluation of the new step and no independent evaluation appears in the sources read. The wider papers are in the [papers group](../papers/llm-kg-construction.md).

## Status and direction

Active, in bursts. The latest release is v1.2.0, 20260909 20:58 UTC. Before it came v1.1.1 (20260407), v1.1.0 (20260325) and v1.0.19 (20260130); 55 releases in all [8][10].

In the 90 days since 20260804 the repository took 38 commits on `main`. All fall on 20260909 and 20260910 (32 and 6), after about five weeks with none in the window [9]. The commits refresh dependencies and default models, harden the LiteLLM client, add the Agent Skills and the term validation, add a "Why OntoGPT?" README section and a `pet_breed` template [9]. There are 27 contributors by the GitHub count (anonymous excluded), 69 open issues and 11 open pull requests [1][10].

The new README section says a modern LLM (large language model) can extract structured data alone, and lists what OntoGPT adds: grounding, schema adherence in small prompts, repeatable batch runs, ready templates and "functions for agents" [3]. That is the authors' positioning. *Reading:* the project is turning from a stand-alone extractor into a step an agent calls. The README shows no maintenance-mode notice and no hosted tier. Roadmap: unstated.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [GLiNER](gliner.md)
- [Projects](README.md)
- [Semantica](semantica.md)

**Index**

- [Agent Skills](../index/agent-skills.md)
- [Entity linking](../index/entity-linking.md)
- [LinkML](../index/linkml.md)
- [Ontology](../index/ontology.md)
- [Schema](../index/schema.md)
- [Schema induction](../index/schema-induction.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/monarch-initiative/ontogpt : repository metadata by `gh api` (archived flag, open issue count) (read 20261102 20:09 UTC)
2. https://github.com/monarch-initiative/ontogpt/blob/main/LICENSE : licence file by `gh api .../license`: BSD 3-clause text, GitHub classification (read 20261102 20:09 UTC)
3. https://github.com/monarch-initiative/ontogpt/blob/main/README.md : description, "Why OntoGPT?", model APIs, default model, Agent Skills, citation (read 20261102 20:09 UTC)
4. https://github.com/monarch-initiative/ontogpt/blob/main/docs/operation.md : working mechanism, term validation, local models, caching (read 20261102 20:11 UTC)
5. https://github.com/monarch-initiative/ontogpt/blob/main/docs/evaluations.md : the BC5CDR evaluation `EvalCTD`, 500 inputs, subset by default (read 20261102 20:11 UTC)
6. https://github.com/monarch-initiative/ontogpt/blob/main/skills/README.md : the four Agent Skills (read 20261102 20:11 UTC)
7. https://pmc.ncbi.nlm.nih.gov/articles/PMC10924283/ : the SPIRES paper, doi 10.1093/bioinformatics/btae104; abstract and full text read through the Europe PMC REST service (read 20261102 20:10 UTC)
8. https://github.com/monarch-initiative/ontogpt/releases : latest release v1.2.0 and the eight newest releases by `gh api` (read 20261102 20:09 UTC)
9. https://github.com/monarch-initiative/ontogpt/commits/main : 38 commits since 20260804 with dates and subjects (read 20261102 20:09 UTC)
10. https://github.com/monarch-initiative/ontogpt : repository tree (600 paths, 71 template files, none containing "mcp"), counts of contributors, open pull requests and releases by `gh api` (read 20261102 20:11 UTC)
