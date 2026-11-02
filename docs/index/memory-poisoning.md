---
type: index
kind: concept
aliases: [memory injection, memory and context poisoning]
updated: 20261102 22:48 UTC
---

# Memory poisoning

This entry says what memory poisoning is and which dated papers and guides named it. It is a security term for agents that keep records between steps or sessions.

## Definition

OWASP's guide to agentic threats lists "Memory Poisoning" as threat T1: "exploiting an AI's memory systems, both short and long-term, to introduce malicious or false data and exploit the agent's context" [1][2]. It goes beyond static data poisoning to real-time poisoning of persistent agent memory [2]. The 2026 OWASP Top 10 for agentic applications lists "Memory & Context Poisoning" (ASI06), which it maps to T1: corruption of summaries, embeddings and RAG stores that propagates across sessions [4].

## How it changed

- **20240212.** Zou et al. submit PoisonedRAG: five malicious texts per question, injected into a RAG knowledge database of millions, gave 90% attack success (first-party) [5].
- **20240717.** Chen et al. submit AgentPoison, "the first backdoor attack targeting generic and RAG-based LLM agents by poisoning their long-term memory or RAG knowledge base": above 80% average success at a poison rate below 0.1% (first-party) [6].
- **20250217.** OWASP's threat guide page is dated this day; the guide's version 1.0 is dated February 2025. Its T1 description and its sentence on static data poisoning read the same as in version 1.1, December 2025, the file served now [1][2][9].
- **20250305.** Dong et al. submit MINJA: records planted "by only interacting with the agent via queries and output observations", without direct access to the memory bank (first-party). Version 5 is dated 20260212 [7].
- **20251209.** OWASP publishes the Top 10 for Agentic Applications 2026, with ASI06 [3][4].
- **20261010.** Pan et al. submit MemForm, a benchmark with five formation interfaces (content, evidence, scope, selection, path). Six models showed broad susceptibility at all five; the defences tested mitigated incompletely (first-party) [8].

Still moving: see [Agent memory](../trends/agent-memory.md).

## Where sources disagree

**What counts as memory.** OWASP T1 covers short- and long-term memory [2]; ASI06 adds RAG stores and embeddings [4]; AgentPoison targets "long-term memory or RAG knowledge base" [6]; PoisonedRAG only the knowledge database [5]. MemForm says earlier work sorts the problem "by attack channels, corruption patterns, or lifecycle stages" [8].

**Attacker access.** MINJA assumes no direct write access [7]. No source read gives one threat model.

## Related

[agent memory](./agent-memory.md) · [agent](./agent.md) · [retrieval-augmented generation](./retrieval-augmented-generation.md) · [embedding](./embedding.md) · trend: [Agent memory](../trends/agent-memory.md) · papers: [agent memory](../papers/agent-memory.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Agent memory: from retrieving documents to remembering across sessions](../trends/agent-memory.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/ : OWASP page "Agentic AI - Threats and Mitigations", dated 17 February 2025 (read 20261102 22:07 UTC)
2. https://genai.owasp.org/download/45674/?tmstv=1739819891 : the guide as served now, version 1.1, December 2025: T1 Memory Poisoning, the data-poisoning contrast, scenarios (read 20261102 22:07 UTC)
3. https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ : OWASP page, dated 9 December 2025 (read 20261102 22:07 UTC)
4. https://genai.owasp.org/download/52117/?tmstv=1765059207 : OWASP Top 10 for Agentic Applications 2026, December 2025: ASI06 description (read 20261102 22:08 UTC)
5. https://arxiv.org/abs/2402.07867 : Zou, Geng, Wang, Jia, "PoisonedRAG", v1 20240212 (v3 read), abstract (first-party; read 20261102 22:07 UTC)
6. https://arxiv.org/abs/2407.12784 : Chen et al. (5 authors), "AgentPoison", 20240717, abstract (first-party; read 20261102 22:07 UTC)
7. https://arxiv.org/abs/2503.03704 : Dong et al. (8 authors), MINJA, v1 5 Mar 2025, v5 12 Feb 2026, abstract (first-party; read 20261102 22:07 UTC)
8. https://arxiv.org/abs/2610.14431 : Pan et al. (7 authors), "MemForm", 20261010, abstract (first-party; read 20261102 22:07 UTC)
9. https://web.archive.org/web/20250405120008id_/https://genai.owasp.org/download/45674/ : Internet Archive capture of 20250405 12:00 UTC of the same OWASP guide, version 1.0, February 2025: T1 description and the static-data-poisoning sentence (read 20261102 22:48 UTC)
