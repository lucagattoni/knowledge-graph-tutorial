# KB/KG reference (field-neutral)

This section describes the field. It does not depend on any one project's needs and does not
mention Pinakes except where Pinakes is itself one of the projects surveyed.

| Part | Question it answers | State |
|---|---|---|
| [`primer/`](primer/) | Where do the ideas of knowledge base and knowledge graph come from, before LLMs? | first draft, 20261030 |
| [`llm-era/`](llm-era/) | What changed from 2020 on, and in what order? | first draft, 20261030 |
| [`literature/`](literature/) | What does the research say about when graphs help retrieval? | first draft, 20261030 |
| [`projects/`](projects/) | What is each notable project, how does it work, and what does it cost? | 77 entries (22 deep, 55 cards), listed in [`projects/README.md`](projects/README.md) |
| [`landscape/`](landscape/) | Which projects are the most starred *and* active, as of a date? | tool built; two snapshots (20261030 19:13 and 19:54); selection made and approved |
| [`papers-benchmarks/`](papers-benchmarks/) | Which papers, surveys, benchmarks and datasets define the state of the art? | first draft, 20261030 |
| [`directions/`](directions/) | Which directions is the field trying, and what is the evidence for each? | nine first drafts, 20261030 |
| [`experiments/`](experiments/) | What should be tested next, and at what cost? | five proposals; none has run |

## Project categories

| Category | Scope |
|---|---|
| `core` | GraphRAG frameworks, KG construction from text, KG querying (including text-to-Cypher) |
| `agent-memory` | Memory layers and temporal knowledge graphs for agents |
| `markdown-kb` | Markdown-native and "LLM wiki" knowledge bases |
| `adjacent` | Code knowledge graphs, graph databases, RAG platforms |

## Entry tiers

- **deep**: architecture, cost profile, evidence and direction, read from the code and documentation.
- **card**: one page from the README, the repository metadata and the licence file.

Entries follow [`projects/_TEMPLATE.md`](projects/_TEMPLATE.md).
