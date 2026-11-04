---
type: index
kind: concept
aliases: [context length, context size]
updated: 20261102 21:23 UTC
---

# Context window

The context window is the amount of text a language model can take into account in one request, counted in tokens. Everything the model reads and writes in that request has to fit inside it.

## Definition

Anthropic's documentation defines the "context window" as all the text a language model can reference when generating a response, including the response itself. It calls it a "working memory" for the model, distinct from the training corpus (first-party) [1]. The limit is counted in [tokens](./token.md). The GPT-3 paper fixes it as an architecture setting, "a context window of nctx = 2048 tokens" for all its models, which caps how many few-shot examples can be placed in a prompt [2].

## How it changed

- **20200528.** The GPT-3 preprint fixes the window at 2048 tokens for every model size [2]. Era: [Language models meet retrieval](../history/language-models-meet-retrieval.md).
- **20230511.** Anthropic says it expanded Claude's window from 9K to 100K tokens, "around 75,000 words" (first-party) [3].
- **20230706.** Liu et al. find that models do not reliably use information across long inputs; performance is worst when the relevant passage sits in the middle [4]. See [the papers group on agentic search](../papers/agentic-search.md).
- **202311.** OpenAI's GPT-4 Turbo is described as having a long context window "up to 128k tokens" [5].
- **20240215.** Google gives Gemini 1.5 Pro a standard 128,000-token window and lets a limited group of developers try up to 1 million tokens (first-party) [6].
- **20250929.** Anthropic writes that recall drops as the window fills ("context rot") and that context is "a finite resource with diminishing marginal returns" (first-party) [7].
- **20261102 (read time).** Anthropic lists 1M-token windows for its current models and 200k for older ones, and offers server-side compaction in beta for long conversations (first-party) [1].

Still moving: [agent memory](../trends/agent-memory.md), [agentic search](../trends/agentic-search.md).

## Where sources disagree

Li and four co-authors report that, with enough resources, long-context models beat [retrieval-augmented generation](./retrieval-augmented-generation.md) on average, while retrieval costs much less (20240723) [8]. Liu et al. [4] and Anthropic [7] stress that use of a long window degrades. The studies use different models and tasks. *Reading:* all agree that choosing what goes in the window matters; they differ on how much retrieval is still needed.

## Related

[Token](./token.md), [large language model](./large-language-model.md), [retrieval-augmented generation](./retrieval-augmented-generation.md), [chunking](./chunking.md), [agent memory](./agent-memory.md), [transformer](./transformer.md). Papers: [agentic search group](../papers/agentic-search.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)
- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Projects**

- [Letta](../projects/letta.md)

**Papers**

- [Papers: Agent memory](../papers/agent-memory.md)
- [Papers: Agentic search over raw data](../papers/agentic-search.md)
- [Papers: Graph-based RAG](../papers/graph-based-rag.md)

**Experiments**

- [X2 evidence: pass A on local models](../experiments/evidence/x2-pass-a.md)

**Index**

- [Agent harness](agent-harness.md)
- [Agent memory](agent-memory.md)
- [Agent Skills](agent-skills.md)
- [Chunking](chunking.md)
- [Community report](community-report.md)
- [Large language model](large-language-model.md)
- [Prompt caching](prompt-caching.md)
- [Retrieval-augmented generation](retrieval-augmented-generation.md)
- [Token](token.md)
- [Tool use](tool-use.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://platform.claude.com/docs/en/build-with-claude/context-windows : definition; 1M-token windows by model; compaction beta (first-party; read 20261102 20:44 UTC)
2. https://arxiv.org/abs/2005.14165 : Brown et al., "Language Models are Few-Shot Learners", v1 20200528; nctx = 2048 for all models, read in the v4 PDF (read 20261102 20:50 UTC)
3. https://www.anthropic.com/news/100k-context-windows : Anthropic, 20230511, 9K to 100K tokens (first-party; read 20261102 20:44 UTC)
4. https://arxiv.org/abs/2307.03172 : Liu et al., "Lost in the Middle: How Language Models Use Long Contexts", v1 20230706 (read 20261102 20:44 UTC)
5. https://arxiv.org/abs/2303.18223 : Zhao et al., "A Survey of Large Language Models": GPT-4 Turbo, November 2023, "up to 128k tokens" (read 20261102 20:52 UTC)
6. https://blog.google/technology/ai/google-gemini-next-generation-model-february-2024/ : Google, 20240215, Gemini 1.5 Pro 128,000 standard and up to 1 million tokens (first-party; read 20261102 20:50 UTC)
7. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents : Anthropic, 20250929, context rot and finite attention budget (first-party; read 20261102 20:52 UTC)
8. https://arxiv.org/abs/2407.16833 : Li et al., "Retrieval Augmented Generation or Long-Context LLMs?", v1 20240723 (read 20261102 20:52 UTC)
