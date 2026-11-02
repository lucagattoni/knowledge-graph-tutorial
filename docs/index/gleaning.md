---
type: index
kind: concept
aliases: [gleanings, self-reflection pass]
updated: 20261102 21:16 UTC
---

# Gleaning

Gleaning is a second extraction pass in graph builders that use a language model. After the model has listed the entities of a chunk, it is asked whether it missed any, and may be asked to list more. Edge et al. describe it in the GraphRAG paper [1]; builders that also use it differ in how many passes they run.

## Definition

Edge et al. introduce it as a fix for a problem of chunk size: on a sample of HotPotQA, GPT-4 "extracted almost twice as many entity references" from 600-token chunks as from 2,400-token ones. After the first extraction, the authors give the entities back to the model, "prompting it to 'glean' any entities that it may have missed". The model is first asked a yes-or-no question about whether all entities were found. If it says no, a continuation prompt asks for the rest. This lets a builder use larger [chunks](./chunking.md) and fewer calls (first-party) [1].

## How it changed

- **20240424.** The [GraphRAG](./graphrag.md) paper (v1) describes the pass; the text read here is v2 [1].
- **Microsoft's implementation, as of 20261102.** It runs up to `max_gleanings` passes. Each sends a continuation prompt, and between passes a second prompt asks whether more entities remain. The loop stops at the maximum or when the answer is not "Y" [2]. The default is 1 [3]; the documentation calls the setting "the maximum number of gleaning cycles" [4]. See [Microsoft GraphRAG](../projects/microsoft-graphrag.md).
- **LightRAG, as of 20261102.** The setting `entity_extract_max_gleaning` defaults to 1 [5][6]. A source comment says the extra pass runs "only 1 time" when the setting is above zero [7]. See [LightRAG](../projects/lightrag.md). When each project adopted gleaning is **unstated** in the sources read.
- The cost of the extra calls is measured in the [index-cost experiment](../experiments/x2-index-cost.md). The family it belongs to is on the [graph-based RAG trend page](../trends/graph-based-rag.md).

## Where sources disagree

The name covers two behaviours. Microsoft's loop can run several passes and lets the model end it early [2]. LightRAG's comment says one extra pass, whatever positive number is set [7]. The GraphRAG paper itself writes the verb "glean", not a count [1].

## Related

[GraphRAG](./graphrag.md), [chunking](./chunking.md), [large language model](./large-language-model.md), [named-entity recognition](./named-entity-recognition.md), [knowledge graph](./knowledge-graph.md). Pages: [Microsoft GraphRAG](../projects/microsoft-graphrag.md), [LightRAG](../projects/lightrag.md), [graph-based RAG](../trends/graph-based-rag.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Experiments**

- [X2: the index cost of cheap graph builders](../experiments/x2-index-cost.md)

**Index**

- [GraphRAG](graphrag.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/html/2404.16130v2 : Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization", Appendix A.2 (v1 20240424, 10 authors; first-party; read 20261102 20:45 UTC)
2. https://raw.githubusercontent.com/microsoft/graphrag/main/packages/graphrag/graphrag/index/operations/extract_graph/graph_extractor.py : the gleaning loop and its two exit criteria (read 20261102 20:49 UTC)
3. https://raw.githubusercontent.com/microsoft/graphrag/main/packages/graphrag/graphrag/config/defaults.py : `max_gleanings: int = 1` in the graph and claim extraction defaults (read 20261102 20:46 UTC)
4. https://microsoft.github.io/graphrag/config/yaml/ : "The maximum number of gleaning cycles to use." (read 20261102 20:46 UTC)
5. https://raw.githubusercontent.com/HKUDS/LightRAG/main/lightrag/lightrag.py : field `entity_extract_max_gleaning` (read 20261102 20:49 UTC)
6. https://raw.githubusercontent.com/HKUDS/LightRAG/main/lightrag/constants.py : `DEFAULT_MAX_GLEANING = 1` (read 20261102 20:49 UTC)
7. https://raw.githubusercontent.com/HKUDS/LightRAG/main/lightrag/operate.py : comment "Process additional gleaning results only 1 time when entity_extract_max_gleaning is greater than zero." (read 20261102 20:49 UTC)
