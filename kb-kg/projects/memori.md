---
slug: memori
repo: MemoriLabs/Memori
tier: card
category: agent-memory
snapshot: 20261030 19:39 UTC
---

# Memori

| | |
|---|---|
| Repository | https://github.com/MemoriLabs/Memori [1] |
| Licence | GitHub reports `NOASSERTION` [1]. The `LICENSE` file is the Apache License 2.0 reworded, not the standard text. Compared word by word with apache.org [2][3], it differs in: (1) the copyright grant lists "use, reproduce, modify, distribute, and prepare Derivative Works" and display and perform "in all media and formats", but not "sublicense"; (2) "Work" and "Derivative Works" carve out separate works that interact only through public interfaces; (3) section 9 reads "Accepting Warranty or Support", without the "While redistributing" condition; (4) smaller rewordings in the "Licensor" definition and section 4(c); (5) the appendix line is unfilled, "[2025] [Memori Team]". The patent, redistribution, trademark, disclaimer and liability sections match the standard text. A reading, not legal advice. README, PyPI and npm say Apache 2.0 [4][8]. |
| Language | Python (GitHub primary language); also a TypeScript SDK and a Rust core [1][11] |
| Stars, forks | 17,241, 3,757 (20261030 19:39 UTC) [1] |
| Created, last push | 20250724 07:07 UTC, 20261003 01:33 UTC [1] |
| Latest release | v3.3.6, 20260528 01:01 UTC, 155 days before the read; PyPI also ends at 3.3.6 [6][8] |
| Status | pushed 27 days before the read (within 90 days) but quiet on main, see below; not archived [1] |
| Paper, docs | arXiv 2603.19935 [5]; docs at https://memorilabs.ai/docs [4] |

## What it is

Memori describes itself as agent-native memory infrastructure: an LLM-agnostic layer that turns agent execution and conversation into structured, persistent state [1]. Its Python and TypeScript SDKs wrap an LLM client and capture memory automatically, with storage in Memori Cloud or in the user's own database (BYODB) [4][9]. The README claims 87% accuracy on LoCoMo at 721 tokens per query [4]. The paper's abstract (v1, 20 March 2026) gives 81.95% at 1,294 tokens, and a commit of 20260728 updated the README with "new LoCoMo benchmark numbers" [5][7]. No third-party evaluation appears in the sources read.

## How it works

Memories are scoped by entity (user), process (agent) and session [4]. After each call through the wrapped client, a background augmentation step extracts facts, preferences, skills, events and semantic triples, deduplicates them and stores them with embeddings generated locally by a Rust core [9][11]. In the Python code read, the conversation is posted to a hosted `sdk/augmentation` endpoint on a memorilabs.ai host unless a base URL is configured, although the BYODB pages say extracted data is stored in the user's database [9][10]. Recall injects relevant memories into later prompts, or an agent calls recall tools [4]. Other routes: an MCP endpoint, OpenClaw and Hermes plugins [4].

## Status and direction

Quiet on main since June. Commits on main per month: 64, 53, 91 (March to May), 17 (June), then 2, 1, 2 (July to September), none in October [7]. The three since 20260801 are two README edits adding an Enterprise section and one bug fix [7]. The README now stresses Memori Cloud and Enterprise [4]. 26 open pull requests, 18 open issues; the six most recently updated items are open, none from an owner or member [7]. Roadmap: unstated.

## Sources

1. https://github.com/MemoriLabs/Memori : repository metadata via the GitHub API, file tree (read 20261030 19:39 UTC)
2. https://github.com/MemoriLabs/Memori/blob/main/LICENSE : the licence text compared (read 20261030 19:39 UTC)
3. https://www.apache.org/licenses/LICENSE-2.0.txt : reference text (read 20261030 19:42 UTC)
4. https://github.com/MemoriLabs/Memori/blob/main/README.md : description, benchmark claims, plugins, MCP, Enterprise and licence sections (read 20261030 19:39 UTC)
5. https://arxiv.org/abs/2603.19935 : paper abstract, via the fetch tool (read 20261030 19:43 UTC)
6. https://github.com/MemoriLabs/Memori/releases : 38 releases, via the releases API (read 20261030 19:39 UTC)
7. https://github.com/MemoriLabs/Memori/commits/main : commits per month since 20260301, open pull request and issue counts, latest activity (read 20261030 19:41 UTC and 19:45 UTC)
8. https://pypi.org/pypi/memori/json and https://registry.npmjs.org/@memorilabs/memori : versions, dates, licence metadata (read 20261030 19:45 UTC)
9. https://github.com/MemoriLabs/Memori/tree/main/docs/memori-byodb/concepts : the architecture and advanced-augmentation pages (read 20261030 19:42 UTC and 19:43 UTC)
10. https://github.com/MemoriLabs/Memori/tree/main/memori : the Python SDK's network and augmentation modules (read 20261030 19:43 UTC)
11. https://github.com/MemoriLabs/Memori/tree/main/core : Rust core README; changelog on local embeddings (read 20261030 19:42 UTC)
