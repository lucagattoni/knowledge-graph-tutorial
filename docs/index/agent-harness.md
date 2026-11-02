---
type: index
kind: concept
aliases: [harness, agent scaffolding]
updated: 20261102 22:49 UTC
---

# Agent harness

This entry says what authors mean by the harness around a language model, where the word's edge lies, and why several 2026 studies treat the harness as something to vary and measure. The sources read, all from 2025 and 2026, do not share one boundary.

## Definition

Sen and four co-authors (arXiv 2605.15184) define the agent harness as "the environment layer that manages the tool-calling loop": it builds the prompt, dispatches tool calls, receives results and decides whether to continue or give a final answer [1]. LangChain draws a wider line: "A harness is every piece of code, configuration, and execution logic that isn't the model itself", summed up as Agent = Model + Harness [2]. Anthropic calls the Claude Agent SDK "a powerful, general-purpose agent harness" [3]. All three describe software around the model, the part of an [agent](./agent.md) that is not the model itself.

## How it changed

- **20250929.** Anthropic renames the Claude Code SDK the Claude Agent SDK, writing that "the agent harness that powers Claude Code" can power other agents too (first-party) [4].
- **20251126.** Anthropic describes a harness for work that spans many context windows: an initializer agent sets up the environment and a coding agent makes incremental progress each session (first-party) [3].
- **20260310.** LangChain publishes its definition and component list: prompts, tools, skills, MCP servers, filesystem, sandbox, orchestration logic and hooks (first-party) [2].
- **20260324.** Anthropic reports a planner, generator and evaluator harness for long application builds (first-party) [5].
- **20260514.** Sen et al. compare grep and vector retrieval under one custom harness and three vendor command-line ones. Overall scores "still depend strongly on which harness and tool-calling style is used" [1].
- **20261030.** The [RAGFlow](../projects/ragflow.md) team reports that a harness with only BM25 and grep answers 85% of BrowseComp-Plus in its runs (first-party) [6].

Still moving: [Agentic search over raw data](../trends/agentic-search.md) and [Infrastructure and MCP](../trends/infrastructure-and-mcp.md).

## Where sources disagree

**Where the harness ends.** Sen et al. define a loop-control layer, yet they also list the system prompt, tool definitions and context construction among what a custom harness controls [1]. LangChain counts prompts, tools and skills inside the harness and admits "many messy ways to split the boundaries" [2]. Anthropic's November 2025 post names "the system prompt, set of tools, and overall agent harness" as if they were three things [3]. No source read sets a standard.

## Related

[Agent](./agent.md) · [tool use](./tool-use.md) · [context window](./context-window.md) · [agent memory](./agent-memory.md) · [Model Context Protocol](./model-context-protocol.md) · [Agent Skills](./agent-skills.md) · [AGENTS.md](./agents-md.md) · [grep](./grep.md) · [papers: agentic search](../papers/agentic-search.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agentic search over raw data: from building structure to letting the agent search](../trends/agentic-search.md)

**Papers**

- [Papers: Agentic search over raw data](../papers/agentic-search.md)

**Index**

- [Agent Skills](agent-skills.md)
- [AGENTS.md](agents-md.md)
- [grep](grep.md)
- [Knowledge compilation](knowledge-compilation.md)
- [Tool use](tool-use.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://arxiv.org/abs/2605.15184 : Sen, Kasturi, Lumer, Gulati, Subbiah, "Is Grep All You Need? How Agent Harnesses Reshape Agentic Search", submitted 14 May 2026; abstract (read 20261102 22:10 UTC) and full text, section 2.2 (read 20261102 22:11 UTC)
2. https://blog.langchain.com/the-anatomy-of-an-agent-harness/ : Trivedy, "The Anatomy of an Agent Harness", LangChain, 10 March 2026 (first-party; read 20261102 22:11 UTC)
3. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents : Young, "Effective harnesses for long-running agents", 26 November 2025; text and footnote 1 (first-party; read 20261102 22:10 UTC)
4. https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk : "Building agents with the Claude Agent SDK", 29 September 2025 (first-party; read 20261102 22:11 UTC)
5. https://www.anthropic.com/engineering/harness-design-long-running-apps : Rajasekaran, "Harness design for long-running application development", 24 March 2026 (first-party; read 20261102 22:10 UTC)
6. https://arxiv.org/abs/2610.41172 : Yu and 17 co-authors, "Context as Infrastructure", submitted 30 October 2026, abstract (first-party; read 20261102 22:11 UTC)
