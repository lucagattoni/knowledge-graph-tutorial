---
type: index
kind: standard
aliases: [README for agents]
updated: 20261102 22:49 UTC
---

# AGENTS.md

This entry says what the AGENTS.md convention is, when it started, who holds it now, and what two 2026 studies and one product's documentation say about using it. It is a file-naming convention, not a versioned specification.

## Definition

The project site describes AGENTS.md as "a simple, open format for guiding coding agents" and compares it to a README for agents: "a dedicated, predictable place to provide the context and instructions" they need [1]. It has no required fields: "AGENTS.md is just standard Markdown" [1]. In a large repository a nested file may sit in each package, and the closest one to the edited file wins; an explicit instruction in the user's chat overrides every file [1]. The Linux Foundation calls it "a simple, universal standard" [2]. A versioned specification: unstated; the repository has no releases or tags [3].

## How it changed

- **20250510.** The Codex repository of OpenAI commits "migrate to AGENTS.md", replacing a file called `codex.md` (first-party; the earliest commit a search of that repository returned) [4].
- **20250819.** The repository `agentsmd/agents.md` is created under the MIT licence, with copyright held by OpenAI [3].
- **20251209.** The Linux Foundation forms the Agentic AI Foundation with three founding projects, among them AGENTS.md, and reports adoption by "more than 60,000 open source projects and agent frameworks" [2]; the project site, a first-party source, still says "over 60k" on 20261102 [1]. Era: [What has settled since 2023](../history/settled-since-2023.md).
- **20260212.** Gloaguen and four co-authors publish a first version of "Evaluating AGENTS.md" (latest version 20260929) [5].
- **20260918.** Claude Code 2.1.277 adds AGENTS.md support: in a project with no CLAUDE.md it reads AGENTS.md instead (first-party) [6][7].
- **20261022.** Zarzycki's census of 22,854 popular, active GitHub repositories finds agent instructions, counted as a root AGENTS.md or CLAUDE.md, in 26.3% of them [8].

Still moving: [Plain files as agent knowledge](../trends/plain-file-knowledge.md) and [Infrastructure and MCP](../trends/infrastructure-and-mcp.md).

## Where sources disagree

**When it began.** The Linux Foundation says "Released by OpenAI in August 2025" [2]. The Codex commit above is about three months earlier [4]. The repository dates from 20250819 [3]. The site gives no date [1].

**Whether it helps.** The site presents the file as help for agents [1]. Gloaguen et al. find that providing context files "does not generally improve task success rates" while raising inference cost by over 20% on average; they add that such files are useful for specifying non-standard coding practices [5].

**Who reads it.** Claude Code by default reads AGENTS.md only when no CLAUDE.md exists; with both, it reads CLAUDE.md only [7]. The census finds that where both exist, CLAUDE.md usually points to AGENTS.md [8].

## Related

[Agent Skills](./agent-skills.md) · [agent harness](./agent-harness.md) · [Model Context Protocol](./model-context-protocol.md) · [LLM wiki](./llm-wiki.md) · [Plain files as agent knowledge](../trends/plain-file-knowledge.md) · [Infrastructure and MCP](../trends/infrastructure-and-mcp.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)

**Index**

- [Agent harness](agent-harness.md)
- [Agent Skills](agent-skills.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://agents.md/ : project site: description, FAQ (no required fields, nearest file wins), "over 60k", stewardship (first-party; read 20261102 22:13 UTC)
2. https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation : Linux Foundation, 9 December 2025: founding projects, "Released by OpenAI in August 2025", "more than 60,000" (read 20261102 22:15 UTC)
3. https://github.com/agentsmd/agents.md : repository data via the GitHub API: created 2025-08-19, MIT LICENSE ("Copyright (c) 2025 OpenAI"), no releases or tags (read 20261102 22:13 UTC)
4. https://github.com/openai/codex/commit/3104d81b7bdcc7b1f7dc47fe1b17e40e44780423 : commit "fix: migrate to AGENTS.md (#764)", 2025-05-10 22:57 UTC; found by a commit search ordered by date, which is not exhaustive (first-party; read 20261102 22:14 UTC)
5. https://arxiv.org/abs/2602.11988 : Gloaguen, Mündler-Sasahara, Müller, Raychev, Vechev, "Evaluating AGENTS.md", v1 12 February 2026, v3 29 September 2026, abstract (read 20261102 22:13 UTC)
6. https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md : entry 2.1.277, "Added AGENTS.md support"; the release date 2026-09-18 comes from https://github.com/anthropics/claude-code/releases/tag/v2.1.277 (first-party; read 20261102 22:13 UTC)
7. https://code.claude.com/docs/en/memory : Claude Code documentation, "How Claude remembers your project", section "AGENTS.md" (first-party; read 20261102 22:13 UTC)
8. https://arxiv.org/abs/2610.31715 : Zarzycki, "What Open-Source Projects Tell Their Coding Agents", v1 22 October 2026, abstract (read 20261102 22:13 UTC)
