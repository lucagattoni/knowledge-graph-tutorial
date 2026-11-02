---
type: index
kind: concept
aliases: []
updated: 20261102 22:53 UTC
---

# Knowledge compilation

This entry says what "knowledge compilation" means. The phrase has an older meaning in logic-based AI and a newer one in retrieval products, which this documentation uses. The newer use dates from 2026 and is still moving.

## Definition

**In logic.** Darwiche and Marquis describe compiling a propositional theory off-line into a target language, which is then used on-line to answer many queries in polynomial time. The motivation is to "push as much of the computational overhead into the off-line phase" as possible [1]. **In retrieval products.** [RAGFlow](../projects/ragflow.md)'s guide says knowledge compilation "converts unstructured documents into structured knowledge content": a language model reads the documents and, from a chosen template, writes artifacts such as a graph, tree, page index, mind map, timeline or wiki [2]. In both senses the work is done once, ahead of the queries. The logic sense comes with proofs about which queries the result supports [1]; the product guides read give none [2][3].

## How it changed

- **1987 to 1999.** Darwiche and Marquis say the field "has emerged recently" and list work from Reiter and de Kleer (1987) to Darwiche (1999) [1]. See [Knowledge systems](../history/knowledge-systems.md).
- **200209.** Their "map" ranks target languages by size and by the queries each supports in polynomial time (*JAIR* 17) [1].
- **20260404.** Karpathy's gist on the [LLM wiki](./llm-wiki.md) says the knowledge "is compiled once and then kept current" [4]. On 20260405 a repository calling itself "The knowledge compiler" is created [5].
- **20260819.** RAGFlow's README announces Knowledge Compilation (first-party) [3]. See [RAGFlow](../projects/ragflow.md).
- **20261030.** A preprint presenting RAGFlow's pipeline (first-party) reports that a BM25-and-grep harness answers 85% of BrowseComp-Plus, and that "structural artifacts gave no detectable accuracy gain on FRAMES". It calls compilation "a supply layer" [6]. Still moving: [Plain files as agent knowledge](../trends/plain-file-knowledge.md).

## Where sources disagree

**Two meanings.** Darwiche and Marquis require a target language with proven properties [1]. The product guides list artifact types and give no such property; the guide lists six types, the README seven (it adds skills) [2][3].

**Does compiling help accuracy?** The gist says compiling avoids re-deriving at every query [4]. The RAGFlow preprint finds no accuracy gain on FRAMES under a good harness and says a PageIndex-style outline "degraded at scale", while reporting token savings [6]. The [LLM wiki](./llm-wiki.md) entry gives further, conflicting cost results.

## Related

[LLM wiki](./llm-wiki.md), [tree index](./tree-index.md), [vectorless retrieval](./vectorless-retrieval.md), [RAPTOR](./raptor.md), [Agent Skills](./agent-skills.md), [agent harness](./agent-harness.md), [retrieval-augmented generation](./retrieval-augmented-generation.md), [GraphRAG](./graphrag.md), [chunking](./chunking.md). Projects: [RAGFlow](../projects/ragflow.md), [PageIndex](../projects/pageindex.md). Trends and papers: [plain files as agent knowledge](../trends/plain-file-knowledge.md), [vectorless retrieval](../trends/reasoning-over-structure.md), [agentic search](../trends/agentic-search.md), [papers](../papers/plain-file-knowledge.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)

**Index**

- [RAPTOR](raptor.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/1106.1819 : Darwiche and Marquis, "A Knowledge Compilation Map", Journal of Artificial Intelligence Research 17 (2002) 229-264, submitted 12/01, published 9/02: abstract and introduction (read 20261102 22:18 UTC); https://arxiv.org/abs/1106.1819 : arXiv listing, 9 Jun 2011 (read 20261102 22:18 UTC)
2. https://github.com/infiniflow/ragflow/blob/main/docs/guides/knowledge_compilation/overview.md : RAGFlow guide, overview: definition, six artifact types and templates (first-party; read 20261102 22:18 UTC)
3. https://github.com/infiniflow/ragflow/blob/main/README.md : news line "2026-08-19 Introduced Knowledge Compilation to generate Wikis, Graphs, Trees, PageIndex, Mind Maps, Timelines, and Skills" and the Knowledge Compilation feature list (first-party; read 20261102 22:18 UTC)
4. https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw : "LLM Wiki" gist, "compiled once and then kept current"; creation date 2026-04-04T16:25:13Z from https://api.github.com/gists/442a6bf555914893e9891c11519de94f/commits (first-party; read 20261102 22:19 UTC)
5. https://github.com/atomicstrata/llm-wiki-compiler : repository description "The knowledge compiler. Raw sources in, interlinked wiki out.", created 2026-04-05T19:53:06Z, from the repository API (first-party; read 20261102 22:19 UTC)
6. https://arxiv.org/abs/2610.41172 : Yu et al., "Context as Infrastructure: Knowledge Compilation for Retrieval in Agentic Systems with Harnesses", submitted 30 Oct 2026, abstract (first-party; read 20261102 22:14 UTC)
