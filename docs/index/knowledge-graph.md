---
type: index
kind: concept
aliases: [KG]
updated: 20261102 21:22 UTC
---

# Knowledge graph

This entry says what "knowledge graph" means, where the phrase first appears, and how its use changed after 2012.

## Definition

Hogan et al. (ACM Computing Surveys 54(4), 2021; arXiv version 6 of 11 September 2021) adopt an inclusive definition: a knowledge graph is "a graph of data intended to accumulate and convey knowledge of the real world", whose nodes stand for entities of interest and whose edges stand for relations between them [1][5]. Hogan et al. write that "the modern incarnation of the phrase stems from the 2012 announcement of the Google Knowledge Graph" [1]. That announcement says the Knowledge Graph "understands real-world entities and their relationships to one another: things, not strings" [2].

## How it changed

- From the 1940s: the phrase appears in publications with an unrelated meaning [1].
- 1972: Schneider's paper on computerised instruction uses a directed graph of units of knowledge for a student to acquire; Hogan et al. call it the first reference of relevance to the modern meaning [1].
- 1986-1988: Rada, Bakker (1987, a thesis) and Stokman and de Vries define knowledge graphs [1]; Gutierrez and Sequeda call Bakker's thesis "the first systematic study with the term" [3].
- 20120516: Google announces the Knowledge Graph (first-party) [2]; its launch sizes are given in the Google entry. Hogan et al. date the modern phrase to it [1]. See [Google Knowledge Graph](./google-knowledge-graph.md).
- 2016: Ehrlinger and Woess find "the lack of a common core" among definitions and propose one with a reasoner [4].
- 20230614: Pan et al. propose three ways to combine language models and knowledge graphs [6].
- 20250120: Zep builds agent memory on Graphiti, a "temporally-aware knowledge graph engine" (first-party) [7]; see [agent memory](../trends/agent-memory.md).
- 20250529: AutoSchemaKG reports graphs of 900+ million nodes built from over 50 million documents (first-party) [8]; see [LLM graph construction](../trends/llm-kg-construction.md).

Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).

## Where sources disagree

The first use. Hogan et al. write "since at least 1972" in the introduction and "Schneider (1973)" in the appendix; one reference, which the list dates 1973 and ties to a conference of April 1972 [1]. Gutierrez and Sequeda start from Bakker (1987) [3].

The definition. Hogan et al. call it "contentious" and stay inclusive; Ehrlinger and Woess require that a knowledge graph "acquires and integrates information into an ontology and applies a reasoner" [1][4].

## Related

[Knowledge base](./knowledge-base.md), [ontology](./ontology.md), [semantic network](./semantic-network.md), [property graph](./property-graph.md), [knowledge graph embedding](./knowledge-graph-embedding.md), [temporal knowledge graph](./temporal-knowledge-graph.md), [GraphRAG](./graphrag.md), [Google Knowledge Graph](./google-knowledge-graph.md). Data: [Wikidata](../datasets/wikidata.md), [DBpedia](../datasets/dbpedia.md). Project: [Graphiti](../projects/graphiti.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Formal foundations](../history/formal-foundations.md)
- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [Knowledge systems: boom and bust](../history/knowledge-systems.md)
- [Language models meet retrieval (2018-2022)](../history/language-models-meet-retrieval.md)
- [The advent: machines that hold knowledge](../history/advent.md)
- [The Web changes data and search](../history/the-web.md)
- [What has settled since 2023 (2023-present)](../history/settled-since-2023.md)

**Trends**

- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)
- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)
- [Graph-based RAG: from eager LLM-built graphs to cheaper, lazier ones](../trends/graph-based-rag.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Code-Graph-RAG](../projects/code-graph-rag.md)
- [Cognee](../projects/cognee.md)
- [Dify](../projects/dify.md)
- [Graphify](../projects/graphify.md)
- [GraphRAG SDK](../projects/graphrag-sdk.md)
- [HippoRAG](../projects/hipporag.md)
- [Hyper-Extract](../projects/hyper-extract.md)
- [LightRAG](../projects/lightrag.md)
- [MCP reference servers](../projects/mcp-servers.md)
- [Microsoft GraphRAG](../projects/microsoft-graphrag.md)
- [MIRIX](../projects/mirix.md)
- [Neo4j LLM Knowledge Graph Builder](../projects/llm-graph-builder.md)
- [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md)
- [OpenViking](../projects/openviking.md)
- [PageIndex](../projects/pageindex.md)
- [Projects](../projects/README.md)
- [RAG-Anything](../projects/rag-anything.md)
- [Understand Anything](../projects/understand-anything.md)

**Papers**

- [Papers](../papers/README.md)
- [Papers: Agentic graph retrieval](../papers/learned-graph-traversal.md)
- [Papers: Building knowledge graphs with LLMs](../papers/llm-kg-construction.md)
- [Papers: foundations](../papers/foundations.md)
- [Papers: Graph-based RAG](../papers/graph-based-rag.md)

**Datasets**

- [ConceptNet](../datasets/conceptnet.md)
- [Datasets](../datasets/README.md)
- [Freebase](../datasets/freebase.md)
- [MetaQA](../datasets/metaqa.md)
- [Wikidata](../datasets/wikidata.md)

**Benchmarks**

- [CRAG](../benchmarks/crag.md)
- [Knowledge graph link prediction](../benchmarks/kg-link-prediction.md)
- [STaRK](../benchmarks/stark.md)
- [Text2Cypher](../benchmarks/text2cypher.md)

**Experiments**

- [Experiments evidence: status log](../experiments/evidence/status.md)
- [X2: the index cost of cheap graph builders](../experiments/x2-index-cost.md)
- [X4: a code graph against grep](../experiments/x4-code-graph-vs-grep.md)

**Applied to Pinakes**

- [Applied to Pinakes](../applied-to-pinakes/README.md)
- [The Pinakes graph approach](../applied-to-pinakes/approach.md)

**Index**

- [Closed-world assumption](closed-world-assumption.md)
- [Code graph](code-graph.md)
- [Community detection](community-detection.md)
- [Community report](community-report.md)
- [ConceptNet](conceptnet.md)
- [Conceptual graph](conceptual-graph.md)
- [Datalog](datalog.md)
- [DBpedia](dbpedia.md)
- [Distant supervision](distant-supervision.md)
- [Entity](entity.md)
- [Entity linking](entity-linking.md)
- [Entity-relationship model](entity-relationship-model.md)
- [Freebase](freebase.md)
- [Gleaning](gleaning.md)
- [Google Knowledge Graph](google-knowledge-graph.md)
- [Graph database](graph-database.md)
- [GraphRAG](graphrag.md)
- [Hypergraph](hypergraph.md)
- [Knowledge base](knowledge-base.md)
- [Knowledge graph completion](knowledge-graph-completion.md)
- [Knowledge graph embedding](knowledge-graph-embedding.md)
- [Knowledge representation](knowledge-representation.md)
- [Knowledge-base question answering](knowledge-base-question-answering.md)
- [Large language model](large-language-model.md)
- [Linked data](linked-data.md)
- [Multi-hop question answering](multi-hop-question-answering.md)
- [Named-entity recognition](named-entity-recognition.md)
- [Ontology](ontology.md)
- [PageRank](pagerank.md)
- [Personalized PageRank](personalized-pagerank.md)
- [Property graph](property-graph.md)
- [Provenance](provenance.md)
- [RDF](rdf.md)
- [Relation extraction](relation-extraction.md)
- [Schema](schema.md)
- [schema.org](schema-org.md)
- [Semantic network](semantic-network.md)
- [Semantic Web](semantic-web.md)
- [Semi-structured data](semi-structured-data.md)
- [Temporal knowledge graph](temporal-knowledge-graph.md)
- [Triple](triple.md)
- [Wikidata](wikidata.md)
- [WordNet](wordnet.md)
- [YAGO](yago.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/pdf/2003.02320v6 : Hogan et al., "Knowledge Graphs", ACM Computing Surveys 54(4), 2021: introduction (definition, "contentious", 1972), Appendix A.2 (1940s, Schneider, Rada, Bakker, Stokman and de Vries), reference [465] (read 20261102 21:21 UTC)
2. https://blog.google/products/search/introducing-knowledge-graph-things-not/ : Singhal, Google, 16 May 2012 (first-party; read 20261102 20:44 UTC)
3. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: Bakker's thesis (read 20261102 20:45 UTC)
4. https://ceur-ws.org/Vol-1695/paper4.pdf : Ehrlinger and Woess, "Towards a Definition of Knowledge Graphs", SEMANTiCS 2016 Posters and Demos: section 2 and section 4 (read 20261102 20:47 UTC)
5. https://arxiv.org/abs/2003.02320 : arXiv listing of Hogan et al.: v1 4 March 2020, v6 11 September 2021, 18 authors (read 20261102 20:50 UTC)
6. https://arxiv.org/abs/2306.08302 : Pan et al., "Unifying Large Language Models and Knowledge Graphs: A Roadmap", first submitted 14 June 2023, abstract (read 20261102 20:50 UTC)
7. https://arxiv.org/abs/2501.13956 : Rasmussen et al., "Zep: A Temporal Knowledge Graph Architecture for Agent Memory", first submitted 20 January 2025, abstract (first-party; read 20261102 20:50 UTC)
8. https://arxiv.org/abs/2505.23628 : Bai et al., AutoSchemaKG, first submitted 29 May 2025, abstract (first-party; read 20261102 20:50 UTC)
