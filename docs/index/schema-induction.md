---
type: index
kind: concept
aliases: [ontology induction, schema generation, schema discovery, schema extraction]
updated: 20261102 22:52 UTC
---

# Schema induction

This entry answers what "schema induction" means, how the term is used before and after language models, and which tools now do it by default. No source read gives one definition, so the uses are shown side by side.

## Definition

The sources read use the term for deriving a [schema](./schema.md) from text or data instead of taking it from a person's design [1][2]. SCOPE's authors frame the task as "corpus-to-schema induction" and note that "most extraction systems assume the schema is already available" [2]. AutoSchemaKG describes a system that extracts triples and induces schemas "directly from text" [1]. Hogan et al. describe two older routes: an emergent schema extracted from the graph itself, and ontology learning from text [3].

## How it changed

- **2009.** Chambers and Jurafsky learn "narrative schemas", event sequences with participant roles, using no "predefined classes of events or roles" (ACL-IJCNLP, 2 to 7 August) [4]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **20240405.** EDC builds "a succinct self-generated schema" when none is predefined, then canonicalizes it [5].
- **20250529.** AutoSchemaKG builds graphs of 900+ million nodes from over 50 million documents and reports 92% "semantic alignment with human-crafted schemas" (first-party) [1].
- **20250703.** neo4j-graphrag-python 1.8.0 adds LLM schema extraction, on by default when the user gives no schema (first-party changelog) [6]. The schema is extracted once from the input text and guides every chunk [7]. See [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md).
- **20260320.** DIAL-KG induces new schemas "from validated knowledge" in a closed loop (first-party) [8].
- **20260520.** SCOPE and SCION (arXiv lists v1 on this date, although the identifier 2607 points to July) offer a benchmark built from 24 public extraction sources; the authors say their results are not "claims that induced schemas surpass human ontology design" [2].

Still moving: [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

## Where sources disagree

**What is induced.** Different things: event sets with roles [4]; schema graphs whose core target is event types and argument roles [2]; categories of entities and events [1]; node types, relationship types and patterns [7].

**Does it match people?** AutoSchemaKG's authors report 92% alignment with human schemas [1]; SCOPE's authors score against normalized targets and disclaim any claim to beat human design [2]. An independent comparison of induced and human-made schemas on one corpus is unstated in the sources read.

## Related

[Schema](./schema.md) · [relation extraction](./relation-extraction.md) · [ontology](./ontology.md) · [taxonomy](./taxonomy.md) · [LinkML](./linkml.md). Projects: [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md); [OntoGPT](../projects/ontogpt.md) takes a given schema instead. Benchmark: [Text2KGBench](../benchmarks/text2kgbench.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Projects**

- [Semantica](../projects/semantica.md)

**Papers**

- [Papers: Building knowledge graphs with LLMs](../papers/llm-kg-construction.md)

**Index**

- [LinkML](linkml.md)
- [Relation extraction](relation-extraction.md)
- [Schema](schema.md)
- [Taxonomy](taxonomy.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2505.23628 : Bai et al., AutoSchemaKG, v1 29 May 2025, v3 1 August 2025: abstract (read 20261102 22:09 UTC)
2. https://arxiv.org/abs/2607.21610 : Hu et al., "SCOPE and SCION", abstract; the listing gives v1 as 20 May 2026 although the identifier suggests July 2026, unreconciled; the arXiv API record gives the same v1 time, 2026-05-20T04:43:02Z (read 20261102 22:09 UTC; API record read 20261102 22:42 UTC)
3. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", ACM Computing Surveys 54(4), 2021, arXiv v6: section 3.1.3 (emergent schema) and 6.5.2 (ontology learning) (read 20261102 22:06 UTC)
4. https://aclanthology.org/P09-1068.pdf : Chambers and Jurafsky, "Unsupervised Learning of Narrative Schemas and their Participants", ACL-IJCNLP 2009: abstract (read 20261102 22:09 UTC)
5. https://arxiv.org/abs/2404.03868 : Zhang and Soh, EDC, v1 5 April 2024, EMNLP 2024: abstract (read 20261102 22:09 UTC)
6. https://github.com/neo4j/neo4j-graphrag-python/blob/main/CHANGELOG.md : entry 1.8.0, "when the user provides no schema, the automatic schema extraction is enabled by default"; release 1.8.0 published 20250703 15:05 UTC per the GitHub release endpoint through gh (changelog read 20261102 22:15 UTC; release date read 20261102 22:18 UTC)
7. https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_kg_builder.html : "Schema Parameter Behavior" (EXTRACTED is the default; FREE bypasses extraction); also `kg_builder.py` on the main branch, `schema` defaults to None (docs read 20261102 22:09 UTC; code read 20261102 22:15 UTC)
8. https://arxiv.org/abs/2603.20059 : Bao et al., DIAL-KG, v1 20 March 2026, DASFAA 2026: abstract (read 20261102 22:09 UTC)
