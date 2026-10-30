# Who can build on what: licences, relicensing and cloud tiers

**In one paragraph.** For someone choosing a base for a knowledge-base or knowledge-graph system, the licence file, the hosted product and the contents of the open repository set what can be built on. Of 31 project entries, 12 carry a plain MIT or Apache-2.0 file, 9 a GPL or AGPL file, 6 a source-available or custom licence, and 4 a file that is edited, composite or unclear. Several projects changed licence, moved features to a hosted tier, or publish a repository without the engine. This page states licence terms as the entries read them; it gives no legal advice and does not say what any term means for a particular use.

## What the direction claims

No entry states a field-wide position. The claims are per project, in the project's own words:

- [OpenViking](../projects/openviking.md): the Apache-2.0 licence "imposes weak restrictions on commercial service providers"; the team wants "to require open-sourcing for high-value commercial derivative works", plans "a managed public cloud version", and wants to "balance community advancement with sustainable commercial development" (a Discussions post of 20260326).
- [Zep](../projects/zep.md): a blog post of 20250402 gives "open-core compromises and under-investment" as reasons for ending its Community Edition.
- [Graphify](../projects/graphify.md): the 20260722 relicensing commit says Apache-2.0 adds a patent grant and inbound-contribution terms.
- [Mem0](../projects/mem0.md): the README says the headline scores "reflect Mem0's managed platform, which includes proprietary optimizations not available in the open-source SDK".

The common shape is a source-visible core, with some features, a service, or commercial rights held back.

## Who is doing it

Licence is taken from each entry's reading of the `LICENSE` file, not from badges. In 12 of the 31 entries GitHub's licence field reads `NOASSERTION`, and in one it reads "Other" ([Youtu-GraphRAG](../projects/youtu-graphrag.md)). "Status" is the entry's, at 20261030.

### Permissive (MIT or Apache-2.0 file)

| Project | Licence file | Status | Hosted tier or parts outside the repository (entry's record) |
|---|---|---|---|
| [Mem0](../projects/mem0.md) | Apache-2.0 | active | Managed Platform; feature table below |
| [Graphify](../projects/graphify.md) | Apache-2.0; MIT until 20260722 22:50, `LICENSE-MIT` kept for earlier contributions | active | Graphify Cloud; its terms are unstated |
| [Letta](../projects/letta.md) | Apache-2.0; `letta-code` adds a brand-asset exclusion; PyPI licence field empty | server code declared retired; other repositories active | Letta Cloud under Terms of Service |
| [Zep](../projects/zep.md) | Apache-2.0 | active | Repository is examples for Zep Cloud; no engine |
| [Cognee](../projects/cognee.md) | Apache-2.0 | active | Cognee Cloud; two components under an enterprise licence |
| [Graphiti](../projects/graphiti.md) | Apache-2.0 | active | Zep service uses a graph database the vendor calls "proprietary" |
| [LLM Graph Builder](../projects/llm-graph-builder.md) | Apache-2.0 | not archived; app banner says "no longer actively developed" | Neo4j Labs: no support, not approved for production use |
| [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md) | Apache-2.0; some parts PSF License v2 (which files: not located) | active | Hosted tier: not covered by the card |
| [Kuzu](../projects/kuzu.md) | MIT | archived | Company note: "working on something new" |
| [CodeGraph](../projects/codegraph.md) | MIT | active | README announces a hosted platform, waitlist |
| [TencentDB Agent Memory](../projects/tencentdb-agent-memory.md) | MIT | active | None recorded |
| [Supermemory](../projects/supermemory.md) | MIT, repository only; SDK listed Apache-2.0 on npm and PyPI | active | Memory engine and local server not in the repository |

### Copyleft (GPL-3.0 or AGPL-3.0 file)

| Project | Licence file | Status | Hosted tier or parts outside the repository |
|---|---|---|---|
| [Neo4j](../projects/neo4j.md) | GPL-3.0 (Community Edition) | active | Enterprise Edition has closed-source components not in the repository; Aura is managed |
| [LLM Wiki (nashsu)](../projects/llm-wiki-nashsu.md) | GPL-3.0; "only" or "or later" unstated | active | None recorded |
| [OpenKnowledge](../projects/open-knowledge.md) | GPL-3.0 text; README and manifests say "or later" | active | None recorded |
| [LinearRAG](../projects/linearrag.md) | GPL-3.0 (`LICENSE.txt`); "only" or "or later" unstated | quiet | None |
| [LogicRAG](../projects/logicrag.md) | GPL-3.0 | quiet | None |
| [OpenViking](../projects/openviking.md) | AGPL-3.0; `ov_cli` and `examples/` Apache-2.0; some adapters MIT | active | "Self-Managed" edition "activated by a license key" |
| [Basic Memory](../projects/basic-memory.md) | AGPL-3.0 (`pyproject.toml` says "or later") | active | Basic Memory Cloud, $15 a month for beta subscribers; hosted-service code public or not: unstated |
| [Honcho](../projects/honcho.md) | AGPL-3.0, standard text | active | Managed service; no dual licence found |
| [Khoj](../projects/khoj.md) | AGPL-3.0 | active, at the 90-day edge | Banner: "Khoj Cloud is being deprecated on April 15, 2026" |

### Source-available or custom

| Project | Terms as written in the file (entry's quotation) | Status |
|---|---|---|
| [Dify](../projects/dify.md) | "Modified version of the Apache License 2.0" with conditions: a commercial licence "must be obtained" to operate a multi-tenant environment (one tenant is one workspace), or to remove the logo or copyright information in the console | active |
| [FalkorDB](../projects/falkordb.md) | One file holds the Server Side Public License v1, then the Elastic License 2.0; nothing says which applies to what. The README names only SSPLv1. | active |
| [Memgraph](../projects/memgraph.md) | Business Source License 1.1 (Community Edition) and the Memgraph Enterprise License; Change License Apache 2.0, Change Date written "2030-21-10". MEL terms: unstated (PDF not read as text). | active |
| [SurrealDB](../projects/surrealdb.md) | Business Source License 1.1 for "SurrealDB 3.0": no use "as a Database Service"; Change Date 2030-01-01, then Apache 2.0. Terms for 2.x: unstated. | active |
| [KiwiFS](../projects/kiwifs.md) | Business Source License 1.1: production use allowed unless offered as a commercial hosted "Competing Service"; each version converts to Apache-2.0 after four years | active |
| [Youtu-GraphRAG](../projects/youtu-graphrag.md) | Custom: "only for academic purposes ... refrain from using it for any commercial or production purposes under any circumstances". The README badge says MIT; the entry treats the file as the authority. | quiet |

### Unclear: edited, composite or ambiguous

| Project | What the entry records | Status |
|---|---|---|
| [Memori](../projects/memori.md) | Apache-2.0 reworded: no "sublicense" in the grant, a carve-out for works that interact only through public interfaces, other rewording. Legal effect not assessed. | quiet on main |
| [memU](../projects/memu.md) | Apache-2.0 text with MIT-style grant words in section 2; no file named `LICENSE` | active |
| [Hyper-Extract](../projects/hyper-extract.md) | Apache-2.0 text with small wording changes. Legal effect not assessed. | active |
| [MCP servers](../projects/mcp-servers.md) | Composite file: a "licensing transition from the MIT License to the Apache License, Version 2.0", CC-BY-4.0 for documentation. Which licence covers a given line of the memory server: unstated. | active |

## Evidence for

**Licence and licence-file events** (dates UTC, from the entries):

| Date | Project | Event |
|---|---|---|
| 20250402 | [Zep](../projects/zep.md) | Community Edition no longer maintained; the repository stays Apache-2.0 without updates (vendor's account) |
| 20251009 and 20251014 | [Kuzu](../projects/kuzu.md) | BetaKit, citing an EU filing, reports Apple agreed to buy Kuzu (20251009); The Register reports the company gave no statement beyond the archive note (20251014); the repository is archived |
| 20251201 | [LinearRAG](../projects/linearrag.md) | `LICENSE.txt` added after an issue asking; no licence file before |
| 20260330 | [OpenViking](../projects/openviking.md) | Apache-2.0 to AGPL-3.0 (commit `ce998873f9`, 614 files). v0.2.14 is the last Apache-2.0 release; v0.3.1 (20260331 07:15) the first with the change. Whether earlier contributors agreed: unstated. |
| 20260414 | [Mem0](../projects/mem0.md) | Graph store deleted from open source (2.0.0); docs of 20260805 and 20260811 recast graph memory as a Platform feature |
| 20260415 | [Khoj](../projects/khoj.md) | Date given in a banner (added 20260325 to 20260326) for deprecating Khoj Cloud; it mentions self-hosting |
| 20260719 | [LogicRAG](../projects/logicrag.md) | GPL-3.0 file added after an issue asking for MIT or Apache; no file before |
| 20260722 22:50 | [Graphify](../projects/graphify.md) | MIT to Apache-2.0; the project says no per-contributor consent is needed (its position, not assessed) |
| 20260802 | [FalkorDB](../projects/falkordb.md) | Commit migrating the default branch to the Rust engine adds a `LICENSE` file; the 4.22.3 tag has an SSPL-only file |

[Basic Memory](../projects/basic-memory.md) contributors sign a CLA assigning copyright to Basic Machines LLC, which "may license the Contributions under any license terms". For SurrealDB, Memgraph, KiwiFS, Dify and FalkorDB (before 20260802) the entries do not record an earlier licence, so whether they changed is unstated.

**Features held back or engines absent** (what the entry says the open repository lacks):

| Project | Not in the open repository |
|---|---|
| [Mem0](../projects/mem0.md) | Organisations and roles, native graph memory, temporal reasoning, memory decay, background consolidation, webhooks, hosted MCP server. The comparison page says the two "run the same core extraction and retrieval logic", while the README and blog posts say the best scores include optimisations open source lacks (the entry notes the tension). |
| [Supermemory](../projects/supermemory.md) | Memory engine and local server; the binary comes from "a separate, non-public codebase", free within a "lite license limit of 10,000 stored documents" |
| [Zep](../projects/zep.md), [Graphiti](../projects/graphiti.md) | No engine in `getzep/zep`. A pull request of 20261009 moves improvements from Zep's internal Graphiti fork upstream but leaves out flagged features (hyperedges, entity type hierarchy, batch extraction modes) and hooks needing Zep services. |
| [Letta](../projects/letta.md) | Source of the hosted API server (none found); "Cloud only": shared memory, remote client API, hosted MCP server, dynamic workflows |
| [Cognee](../projects/cognee.md) | Production GLiNER extractor and production Postgres graph adapter, "licensed product"; whether Enterprise versions of other features differ: unstated |
| [Dify](../projects/dify.md) | Backend of the Agent Knowledge Base (opt-in beta): a repository described as private |
| [Neo4j](../projects/neo4j.md), [Memgraph](../projects/memgraph.md) | Neo4j Enterprise: closed-source components. Memgraph: the README lists high availability, multi-tenancy, access control and SSO under "Enterprise", which it puts under the MEL. |
| [OpenViking](../projects/openviking.md) | Distributed deployment and official support in the Self-Managed edition; whether it is a commercial licence of the same code: unstated |
| [Graphify](../projects/graphify.md) | Cloud features such as PR reviews and cross-repository graphs; whether the hosted engine equals the CLI: unstated |
| [Memori](../projects/memori.md) | In the Python code read, conversations go to a hosted augmentation endpoint unless a base URL is set; README now stresses Cloud and Enterprise |
| [Youtu-GraphRAG](../projects/youtu-graphrag.md) | An Enterprise Edition on Tencent Cloud's ADP platform; whether it shares this codebase: unstated |

[CodeGraph](../projects/codegraph.md), [Basic Memory](../projects/basic-memory.md) and [KiwiFS](../projects/kiwifs.md) also describe hosted products (waitlist; Cloud; "KiwiFS Cloud", operator unstated).

## Evidence against, or limits

- **Not a rate.** These 31 entries were chosen for this question. The counts above describe them, not the field. The timeline's own reading is "a pattern of cloud tiers around open cores, not a mass retreat", with most core projects permissive ([timeline, section 3.5](../llm-era/README.md)).
- **Other changes run elsewhere.** [MCP servers](../projects/mcp-servers.md) is moving from MIT toward Apache-2.0, and [Graphify](../projects/graphify.md) moved from MIT to Apache-2.0.
- **Two events add a file, not a restriction.** [LinearRAG](../projects/linearrag.md) and [LogicRAG](../projects/logicrag.md) had no licence file before.
- **Sources disagree.** [Youtu-GraphRAG](../projects/youtu-graphrag.md): badge MIT, file academic-only. [OpenKnowledge](../projects/open-knowledge.md), [Basic Memory](../projects/basic-memory.md) and [Khoj](../projects/khoj.md): "or later" appears in manifests or the README, not the file. One third-party analysis still calls Graphify MIT. These are the entries' findings.
- **Reading:** because the GitHub field is `NOASSERTION` for 12 entries, a search or script that trusts it would not see the terms of FalkorDB, Memgraph, SurrealDB, KiwiFS or Dify.
- **Dependency licences.** Only the [LLM Graph Builder](../projects/llm-graph-builder.md) entry says they were not checked; for the rest it is unstated.

## What is unresolved

- Whether any change moved adoption, forks or contributions: no entry measures it.
- [FalkorDB](../projects/falkordb.md): which of SSPL and ELv2 applies to what.
- [Memgraph](../projects/memgraph.md): the MEL terms, and which files carry a MEL header.
- [SurrealDB](../projects/surrealdb.md): terms of the 2.x line, which still publishes releases.
- [OpenViking](../projects/openviking.md): the README sentence on "wholesale rewriting" is outside `LICENSE`; whether it is a term, a notice or a request is unstated.
- Whether hosted engines match the open code: Graphify, Mem0, Cognee, Youtu-GraphRAG (see the tables).
- "Only" or "or later" for [LLM Wiki](../projects/llm-wiki-nashsu.md) and [LinearRAG](../projects/linearrag.md).
- The legal effect of the edited Apache texts: assessed in no entry.

## Signals to watch

| Signal | How to check | Baseline |
|---|---|---|
| FalkorDB clarifies which licence covers what | Default-branch `LICENSE` and release tags after 6.0.0 | Two texts in one file, ELv2 from line 563 (20261030) |
| OpenViking publishes terms for Self-Managed or moves the README sentence into `LICENSE` | README and `LICENSE` | AGPL-3.0 file; README adds the sentence (20261030) |
| Graphify publishes Cloud terms or hosted code | Repository tree and site | Terms unstated; no hosted code found (20261030) |
| Mem0 changes its open-source versus Platform table | Project comparison page | Native graph memory "removed from 20260414" |
| Kuzu forks state their licences | Ladybug and ryugraph repositories | Fork licences not recorded in the entry |
| MCP servers completes its MIT-to-Apache transition | `LICENSE` opening paragraph | "Undergoing a licensing transition" (20261030) |
| KiwiFS v0.1.0 conversion date | The entry's arithmetic gives 20300424 | BSL 1.1, four-year term |
| Letta fills the PyPI licence field | PyPI metadata for `letta` | Empty (20261030) |

## Sources

Entries drawn on, each with its own read times and numbered sources:
[openviking](../projects/openviking.md), [graphify](../projects/graphify.md), [mem0](../projects/mem0.md), [supermemory](../projects/supermemory.md), [basic-memory](../projects/basic-memory.md), [dify](../projects/dify.md), [falkordb](../projects/falkordb.md), [memgraph](../projects/memgraph.md), [neo4j](../projects/neo4j.md), [surrealdb](../projects/surrealdb.md), [kiwifs](../projects/kiwifs.md), [memori](../projects/memori.md), [honcho](../projects/honcho.md), [khoj](../projects/khoj.md), [letta](../projects/letta.md), [zep](../projects/zep.md), [llm-wiki-nashsu](../projects/llm-wiki-nashsu.md), [open-knowledge](../projects/open-knowledge.md), [linearrag](../projects/linearrag.md), [logicrag](../projects/logicrag.md), [youtu-graphrag](../projects/youtu-graphrag.md), [kuzu](../projects/kuzu.md), [memu](../projects/memu.md), [neo4j-graphrag-python](../projects/neo4j-graphrag-python.md), [mcp-servers](../projects/mcp-servers.md), [hyper-extract](../projects/hyper-extract.md), [tencentdb-agent-memory](../projects/tencentdb-agent-memory.md), [llm-graph-builder](../projects/llm-graph-builder.md), [codegraph](../projects/codegraph.md), [cognee](../projects/cognee.md), [graphiti](../projects/graphiti.md).

Context: [timeline](../llm-era/README.md). No other source was fetched for this page; written 20261030 19:58 UTC from the entries as they stood.
