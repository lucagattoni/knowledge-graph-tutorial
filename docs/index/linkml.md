---
type: index
kind: system
aliases: [Linked Data Modeling Language, Linked Open Data Modeling Language]
updated: 20261102 22:23 UTC
---

# LinkML

This entry says what LinkML is, where it began, and how it connects to ontology-grounded extraction with language models. The tool that uses it for extraction has its own page, linked below.

## Definition

LinkML is "a flexible modeling language" for writing schemas, called models, in YAML that describe the structure of data [1]. Models are built from classes and slots [1]. The project describes two interlocking parts: a standard for representing schemas, data dictionaries and metadata, and a reference tool stack, written in Python, that acts on schemas [1]. Generators turn one schema into JSON Schema, SHACL, ShEx, OWL, JSON-LD contexts, SQL, Pydantic and other forms; the site counts "30+" output formats [1][2]. The language is itself defined in LinkML [1]. The repository licence is Apache-2.0, from its LICENSE file [3].

## How it changed

- **20210316.** The `linkml/linkml` repository is created on GitHub [3].
- **20210324.** The earliest `linkml` release PyPI lists, 0.0.2, is uploaded [4].
- **September 2021.** Moxon and 13 co-authors present a four-page paper at ICBO 2021 (16 to 18 September, pages 148 to 151) titled "The Linked Data Modeling Language (LinkML): A General-Purpose Data Modeling Framework Grounded in Machine-Readable Semantics" [5].
- **20251212.** GigaScience publishes online "LinkML: an open data modeling framework" by Moxon et al. (volume 15, print date 20260121) [6]. The site cites it as 2026;15:giaf152 (first-party) [2].
- **20261013.** Release v1.12.1, the latest at the read time [3][4].
- **20261102 (read date).** The LinkML site lists OntoGPT among its ecosystem tools, for extracting "LinkML-compliant data" from text with language models (first-party) [2]. See [OntoGPT](../projects/ontogpt.md) and [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

Who uses LinkML beyond the project's own list is **unstated** in the sources read; the site's own list of users is first-party [2].

## Where sources disagree

**The expansion of the name.** The project site and the 2021 paper title say "Linked Data Modeling Language" [2][5]. The GitHub description and the PyPI summary say "Linked Open Data Modeling Language" [3][4].

## Related

- Entries: [schema](./schema.md), [ontology](./ontology.md), [OWL](./owl.md), [SHACL](./shacl.md), [RDF](./rdf.md), [JSON-LD](./json-ld.md), [entity linking](./entity-linking.md), [schema induction](./schema-induction.md), [large language model](./large-language-model.md).
- Project: [OntoGPT](../projects/ontogpt.md). Trend: [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Projects**

- [OntoGPT](../projects/ontogpt.md)

**Index**

- [Schema](schema.md)
- [Schema induction](schema-induction.md)

<!-- END GENERATED: appears-in -->

## Sources

Read times are UTC.

1. https://linkml.io/linkml/intro/overview.html : "LinkML at a glance": YAML schemas, classes and slots, two interlocking parts, generators, self-definition (first-party; read 20261102 22:08 UTC)
2. https://linkml.io/ : project home page: expansion of the name, "30+" output formats, ecosystem tools including OntoGPT, citation of the GigaScience paper (first-party; read 20261102 22:08 UTC)
3. https://api.github.com/repos/linkml/linkml : GitHub record: created 2021-03-16, description, licence Apache-2.0; the LICENSE file begins "Apache License Version 2.0"; the release list shows v1.12.1 published 2026-10-13 (first-party; read 20261102 22:09 and 22:14 UTC)
4. https://pypi.org/pypi/linkml/json : PyPI record: summary, release list (earliest 0.0.2 uploaded 2021-03-24, latest 1.12.1) (first-party; read 20261102 22:08 UTC)
5. https://ceur-ws.org/Vol-3073/ : CEUR-WS volume 3073, Proceedings of ICBO 2021 (Bozen-Bolzano, 16-18 September 2021): the LinkML paper, pages 148-151, 14 authors (read 20261102 22:09 UTC)
6. https://api.crossref.org/works/10.1093/gigascience/giaf152 : Crossref record: title, GigaScience volume 15, online 2025-12-12, print 2026-01-21, first author Moxon (read 20261102 22:09 UTC)
