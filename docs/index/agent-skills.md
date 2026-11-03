---
type: index
kind: standard
aliases: [Skills, SKILL.md]
updated: 20261102 22:49 UTC
---

# Agent Skills

This entry says what the Agent Skills format is, who started it and who holds it now, and where a product's own rules differ from the specification. The specification page carries no version number, so dates below come from announcements and the repository history.

## Definition

The specification defines a skill as "a directory containing, at minimum, a SKILL.md file" [1]. The file opens with YAML front matter and continues in Markdown. Two fields are required: `name` (up to 64 characters, lowercase alphanumerics and hyphens, matching the directory name) and `description` (up to 1024 characters, saying what the skill does and when to use it) [1]. Optional fields are `license`, `compatibility`, `metadata` and `allowed-tools`, the last marked experimental [1]. Optional folders hold `scripts/`, `references/` and `assets/` [1]. Agents load a skill in stages: name and description at startup (about 100 tokens), the full instructions on activation (under 5000 tokens recommended), other files only when needed [1]. The overview calls it "a lightweight, open format" [2].

## How it changed

- **20251016.** Anthropic announces Skills: "folders that include instructions, scripts, and resources that Claude can load when needed" (first-party) [3].
- **20251216.** The repository `agentskills/agentskills` is created with a README only; its first documentation commit follows on 20251218, with a `docs/LICENSE` file holding the CC BY 4.0 text [4].
- **20251218.** Anthropic adds an update to its announcement: Agent Skills published "as an open standard for cross-platform portability" (first-party) [3].
- **20260205.** A top-level `LICENSE` file (Apache-2.0) is added; the README says code is under Apache 2.0 and documentation under CC-BY-4.0 [4].
- **20260804.** The latest of 19 commits to the specification page so far clarifies `metadata`; no release or tag marks any of them [4].
- **20261022.** Agent Skills, contributed by Anthropic, joins the Agentic AI Foundation as one of four new projects the Linux Foundation announces that day, bringing the foundation to ten [5]. Still moving: [Plain files as agent knowledge](../trends/plain-file-knowledge.md).

The overview says the format was "originally developed by Anthropic, released as an open standard" [2]. Status of a versioned specification: unstated.

## Where sources disagree

**Required fields.** The specification marks `name` and `description` as required [1]. Claude Code's reference marks `name` optional (it defaults to the directory name) and `description` only recommended [6]. Claude Code says its skills "follow the Agent Skills open standard" and add features of its own, such as invocation control and subagent execution [6].

**The `allowed-tools` format.** The specification gives a space-separated string and warns that support varies [1]. Claude Code accepts a space- or comma-separated string, or a YAML list [6].

## Related

[AGENTS.md](./agents-md.md) · [agent harness](./agent-harness.md) · [Model Context Protocol](./model-context-protocol.md) · [tool use](./tool-use.md) · [context window](./context-window.md) · [Plain files as agent knowledge](../trends/plain-file-knowledge.md) · [Infrastructure and MCP](../trends/infrastructure-and-mcp.md) · [claude-obsidian](../projects/claude-obsidian.md) · [OntoGPT](../projects/ontogpt.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Plain files as agent knowledge: from databases and indexes to Markdown the model maintains](../trends/plain-file-knowledge.md)

**Projects**

- [claude-obsidian](../projects/claude-obsidian.md)

**Index**

- [Agent harness](agent-harness.md)
- [AGENTS.md](agents-md.md)
- [Knowledge compilation](knowledge-compilation.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://agentskills.io/specification : Agent Skills specification: directory, front matter fields, progressive disclosure (read 20261102 22:11 UTC)
2. https://agentskills.io/ : Agent Skills overview: "lightweight, open format"; "Open development" paragraph (read 20261102 22:12 UTC)
3. https://claude.com/blog/skills : Anthropic, "Introducing Agent Skills", 16 October 2025, with the update of 18 December 2025 (first-party; read 20261102 22:12 UTC)
4. https://github.com/agentskills/agentskills : repository data via the GitHub API: created 2025-12-16 (first commit holds a README only), `docs/LICENSE` (CC BY 4.0 text) from the first documentation commit of 2025-12-18, top-level Apache-2.0 `LICENSE` added 2026-02-05, README licence section, no releases or tags, 19 commits to `docs/specification.mdx` from 2025-12-18 to 2026-08-04 (read 20261102 22:12 UTC; licence history re-read 20261102 22:49 UTC)
5. https://www.linuxfoundation.org/press/agentic-ai-foundation-announces-four-new-projects-agent-skills-open-responses-openenv-and-opensandbox : Linux Foundation, 22 October 2026: Agent Skills contributed by Anthropic; ten hosted projects (read 20261102 22:15 UTC)
6. https://code.claude.com/docs/en/skills : Claude Code documentation, "Extend Claude with skills": the statement on the standard and front matter reference (first-party; read 20261102 22:12 UTC)
