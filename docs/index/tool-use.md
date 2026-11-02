---
type: index
kind: concept
aliases: [function calling, tool calling]
updated: 20261102 22:23 UTC
---

# Tool use

This entry says what "tool use" means for a language model, who runs the call, and the dated steps from research papers to a standard feature of model APIs.

## Definition

Anthropic's documentation says tool use (also called function calling) lets Claude call functions that the developer defines or Anthropic provides. The model decides when to call a tool and returns a structured call, which the application runs (client tools) or Anthropic runs (server tools) [1]. OpenAI's guide gives the same idea two names: "function calling (also known as tool calling)" [2]. In both, the model outputs a structured request, not the action itself [1][5].

## How it changed

- **20230209.** Toolformer is "a model trained to decide which APIs to call, when to call them, what arguments to pass" and how to use the results [3]. Era: [What has settled since 2023](../history/settled-since-2023.md).
- **20230524.** Gorilla, a fine-tuned LLaMA-based model, is reported to beat GPT-4 at writing API calls (first-party) [4].
- **20230613.** OpenAI adds function calling to the Chat Completions API: developers describe functions and the model may output a JSON object with the arguments (first-party) [5].
- **20231106.** OpenAI deprecates the Chat Completions `functions` parameter in favour of `tools` [6].
- **20240530.** Anthropic makes tool use generally available across the Claude 3 models (first-party) [7].
- **20241125.** Anthropic open-sources the Model Context Protocol for connecting assistants to tools and data (first-party) [8]. See [Model Context Protocol](./model-context-protocol.md).
- **20250311.** OpenAI's Responses API adds built-in tools: web search, file search and computer use (first-party) [9].
- **20251124.** Anthropic adds a Tool Search Tool, Programmatic Tool Calling and Tool Use Examples; it reports that tool search preserves 191,300 tokens of context against 122,800 when every definition loads upfront (first-party) [10]. Still moving: [Infrastructure and MCP](../trends/infrastructure-and-mcp.md).

## Where sources disagree

**What the name covers.** The two vendors treat the names as synonyms [1][2]. Research use differs: Toolformer's tools are external APIs that the trained model itself decides to call [3], while in the vendor APIs the application sends tool definitions with each request and runs the call [1][5]. *Reading:* one name covers a trained skill and a request protocol; read it as each source defines it.

## Related

[Agent](./agent.md), [Model Context Protocol](./model-context-protocol.md), [agent harness](./agent-harness.md), [large language model](./large-language-model.md), [context window](./context-window.md), [fine-tuning](./fine-tuning.md), [text-to-query](./text-to-query.md). Project: [mcp-servers](../projects/mcp-servers.md). Trends: [Infrastructure and MCP](../trends/infrastructure-and-mcp.md), [Agentic search](../trends/agentic-search.md). Papers: [agentic search group](../papers/agentic-search.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

**Projects**

- [Hyper-Extract](../projects/hyper-extract.md)
- [PageIndex](../projects/pageindex.md)

**Index**

- [Agent](agent.md)
- [Agent harness](agent-harness.md)
- [Agent Skills](agent-skills.md)
- [Chain-of-thought](chain-of-thought.md)
- [grep](grep.md)
- [Tree index](tree-index.md)
- [Vectorless retrieval](vectorless-retrieval.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview : Anthropic, "Tool use with Claude": definition, client and server tools (first-party; read 20261102 22:08 UTC)
2. https://platform.openai.com/docs/guides/function-calling : OpenAI, "Function calling": "function calling (also known as tool calling)" (first-party; read 20261102 22:08 UTC)
3. https://arxiv.org/abs/2302.04761 : Schick et al., "Toolformer", 8 authors, submitted 9 February 2023, abstract (read 20261102 22:08 UTC)
4. https://arxiv.org/abs/2305.15334 : Patil et al., "Gorilla: Large Language Model Connected with Massive APIs", submitted 24 May 2023, abstract (first-party; read 20261102 22:08 UTC)
5. https://web.archive.org/web/2023/https://openai.com/blog/function-calling-and-other-api-updates : OpenAI, "Function calling and other API updates", 13 June 2023 (Wayback copy; the openai.com page answered HTTP 403) (first-party; read 20261102 22:08 UTC)
6. https://platform.openai.com/docs/changelog : OpenAI API changelog, November 2023 entry "Deprecated the Chat Completions functions parameter in favor of tools" (read 20261102 22:08 UTC)
7. https://www.anthropic.com/news/tool-use-ga : Anthropic, "Claude can now use tools", 30 May 2024, general availability across Claude 3 (first-party; read 20261102 22:08 UTC)
8. https://www.anthropic.com/news/model-context-protocol : Anthropic, "Introducing the Model Context Protocol", 25 November 2024 (first-party; read 20261102 22:08 UTC)
9. https://web.archive.org/web/2025/https://openai.com/index/new-tools-for-building-agents/ : OpenAI, "New tools for building agents", 11 March 2025 (Wayback copy; the openai.com page answered HTTP 403) (first-party; read 20261102 22:08 UTC)
10. https://www.anthropic.com/engineering/advanced-tool-use : Anthropic, "Introducing advanced tool use on the Claude Developer Platform", 24 November 2025 (first-party; read 20261102 22:08 UTC)
