---
type: trend
shift: n/a -> n/a
status: steady
order: 12
updated: 20261103 01:52 UTC
---

# Graph features removed and added

This page answers a narrow question: which graph features have projects taken out or added in 2025 and 2026, and what reason did each project give? It lists dated acts from eleven repositories, then asks what pattern they make, and where a licence or a hosted product sits beside them. Most projects give no reason. No source read here is an independent test of any single removal or addition.

> **Distinctive because** it follows dated acts across projects, whatever family each belongs to, instead of one family of approaches. It has no nearest neighbour in the catalogue; [infrastructure and MCP](./infrastructure-and-mcp.md) (the [Model Context Protocol](../index/model-context-protocol.md)) is the other theme page.

## What it covers

A **removal** is code or an option deleted or marked for deletion. A **demotion** is a feature moved to a hosted tier, to maintenance mode, or to a successor product. An **addition** is a capability that touches how a graph is built, stored or kept, announced in a release note, a merged pull request or a README news entry (each row says which). A **reason** is a cause the project states in its own words; a status such as "no ETA", or the naming of a successor, is not a cause. Anything else is marked *no reason given*.

This is a theme page, not a family of approaches: the owner chose it (decision T-2), so it has no growth test and its `shift` is `n/a -> n/a`. It is not a census. The eleven repositories were picked from the archive's list of projects with dated acts, and the counts describe that choice, not the field. The families these projects belong to are on [graph-based RAG](./graph-based-rag.md) (retrieval-augmented generation, [RAG](../index/retrieval-augmented-generation.md)) and [agent memory](./agent-memory.md); the [graph databases](../index/graph-database.md) underneath are on [infrastructure and MCP](./infrastructure-and-mcp.md).

## Graph features removed or demoted

| Date | Project | What changed | Reason given | Source |
|---|---|---|---|---|
| 20250402 | [Zep](https://github.com/getzep/zep) | Community Edition no longer maintained; the repository now holds examples for Zep Cloud | The company's post: "design choices in one limiting the other" in its [open-core](../index/open-core.md) model; it kept Graphiti as its open-source effort [15][16] | [15][16] |
| 20251010 | [Kuzu](https://github.com/kuzudb/kuzu) | Repository archived (last push and last release v0.11.3 that day; the date the flag was set is unstated) | README: "Kuzu is working on something new!" No other reason | [13] |
| 20251118 | [Microsoft GraphRAG](../projects/microsoft-graphrag.md) | Issue "When will LazyGraphRAG arrive?" closed as not planned | Maintainer: "no ETA so I'm going to close the issue" (ETA: estimated time of arrival) | [9] |
| 20260414 | [Mem0](../projects/mem0.md) | Python 2.0.0 deletes the external graph-store drivers (Neo4j, Memgraph, Kuzu, Apache AGE, Neptune), about 4,000 lines; graph memory becomes a Platform feature, "not being replaced by an OSS equivalent" (open-source software). The release is labelled 20260414 in the changelog and published on GitHub 20260416 | No reason given | [3][4] |
| 20260608 | [Graphiti](../projects/graphiti.md) | Kuzu driver marked deprecated (v0.29.2); the README says it "will be removed in a future release" | The upstream Kuzu project "is no longer maintained" | [10][11] |
| 20260814 | Microsoft GraphRAG | README notice: "largely in maintenance mode", no new pull requests or features; bug fixes and patches for CVEs (Common Vulnerabilities and Exposures, public security-flaw records) continue | "the capabilities of frontier models have changed dramatically" since July 2024 and the project portfolio "has diversified" | [8] |
| 20260819 | [RAGFlow](../projects/ragflow.md) | v0.27.0: [GraphRAG](../index/graphrag.md) and RAPTOR "deprecated and are no longer available in the UI" (user interface); Graph and Tree in Knowledge Compilation replace them; old content stays searchable | No reason given | [7] |
| 20260918 | [Cognee](../projects/cognee.md) | v1.6.0 lists as a breaking change: "GLiNER removed from default Docker image". The current README says the `cognee/cognee` image ships with the GLiNER runtime baked in, so the removal was later undone or changed; when is unstated | No reason given | [18][19] |
| 20261007 | Cognee | v1.6.3 removes the `temporal_cognify` option | No reason given | [17] |
| 20261023 | [LLM Graph Builder](../projects/llm-graph-builder.md) | Banner in the app on the main branch: "no longer actively developed", use Neo4j Document Intelligence in Aura. The previous version of that file (20260721) has no banner | A successor is named; why is unstated | [14] |

*Reading:* ten acts. Three give a cause, and it concerns the company, a dependency or the model landscape (Zep, Graphiti, GraphRAG). Seven name no cause: one gives only "no ETA" (counted here as no cause), one names a successor (the LLM Graph Builder banner), and five say nothing (Kuzu beyond "working on something new", Mem0, RAGFlow, and two Cognee acts). None says that graphs retrieve worse. The acts also differ in kind. Kuzu is a database, and its end reached dependants: Graphiti deprecated its driver and Mem0 deleted it with the others [10][3]. Mem0 deleted a store but added [entity links](../index/entity-linking.md), which its README describes as extracted, embedded and linked across memories [5]. Whether entity links stand in for graph memory is not settled by the vendor: the changelog says graph memory "now runs natively as built-in entity linking" [4], while the migration guide calls the entity collection "separate from and unrelated to graph memory" and says OSS "has no graph memory replacement" [3]. RAGFlow swapped one graph method for several, and its README lists Graphs next to Wikis, Trees and PageIndex [7]. So the rows show relocation (to a platform or a successor) and substitution more than a plain retreat; for Mem0 the vendor's own pages disagree on which it is.

## Graph features added

| Date | Project | What was added | Reason given | Source |
|---|---|---|---|---|
| 2026.03 | [LightRAG](../projects/lightrag.md) | OpenSearch as a unified storage backend; a README news entry with the month only, no release cited (a storage option, not a graph method as such) | No reason given | [20] |
| 2026.05 | LightRAG | "Merge RagAnything into LightRAG": multimodal parsing through MinerU or Docling; a README news entry with the month only, no release cited (it widens the inputs that feed the graph) | No reason given; RAG-Anything remains a separate repository | [20] |
| 20260414 | Mem0 | Entity extraction with spaCy, a second vector collection for entity links, [hybrid search](../index/hybrid-search.md); one extraction call instead of two | No reason given | [4] |
| 20260819 | RAGFlow | Knowledge Compilation: Wiki, Graph, Tree, PageIndex, Mindmap, Timeline, Skills | No reason given | [7] |
| 20260918 | Cognee | v1.6.0, "keyless" workflows: [large language model](../index/large-language-model.md) (LLM) stages skip cleanly when no key is set, and local model downloads are announced. The release notes do not say that GLiNER extraction starts here; the same release removes GLiNER from the default Docker image (removals table) | No reason given | [18] |
| 20261009 | Graphiti | Pull request 1964 merged (release v0.31.0, 20261014): Zep's fork improvements moved upstream, with combined node and edge extraction, one LLM call per episode in bulk mode | Stated: move the fork's improvements upstream, leaving out features Zep "releases behind feature flags" | [11][12] |
| 20261029 | Cognee | v1.6.6: a durable API to resolve conflicting facts, conflict review on by default | No reason given | [18] |

*Reading:* the additions point at three levers. One is cost: extraction by a small local model with no LLM key (Cognee; its README names the [GLiNER](../projects/gliner.md) model, a [named-entity recognition](../index/named-entity-recognition.md) model, for this and does not date it [19]), spaCy instead of a model call (Mem0), one call instead of two (Graphiti, Mem0). The cost problem is told on [graph-based RAG](./graph-based-rag.md). Another is more inputs (LightRAG's merge). The third is upkeep of a changing graph (Cognee's conflict API; compare time in [agent memory](./agent-memory.md)). No row cites a measurement as its reason.

## Licence moves and hosted counterparts

Licences below come from each `LICENSE` file [2]; the commit history of that file was read for all eleven repositories and for claude-mem [33][34]. Three rows record a licence change: OpenViking, Graphify and claude-mem. claude-mem is outside the eleven, because it has no graph feature act on this page; it is here because its move sits beside reserved commercial parts. The other rows record a hosted or licensed counterpart beside an unchanged licence: the `LICENSE` histories of Mem0, Cognee and Graphiti show no change since 2024, and those of RAGFlow, LightRAG, Microsoft GraphRAG, LLM Graph Builder, Zep and Kuzu show no change of licence type in 2025 and 2026 (Kuzu's file was edited for the year only) [33][34]. The same pass over the other repositories with a project page found three more moves, outside this page's scope: MIRIX (MIT to Apache-2.0, 20250711), the MCP servers repository (MIT to a composite with Apache-2.0 for new contributions, 20260112) and FalkorDB (an SSPL-only `LICENSE.txt` replaced by a `LICENSE` holding the Server Side Public License and the Elastic License 2.0, 20260802) [34]. The commit titles of those three give no reason. Legal effect is not assessed.

| Date of the act | Project | Licence file now | Held back or moved | Reason given | Source |
|---|---|---|---|---|---|
| 20260414 (graph move; no licence change) | Mem0 | Apache-2.0 | Graph memory is Platform-only; the README says top scores "reflect Mem0's managed platform", with "proprietary optimizations not available in the open-source SDK" (software development kit) | None for the graph move | [3][5] |
| 20260330 | [OpenViking](../projects/openviking.md) | AGPL-3.0, the GNU Affero General Public License version 3 (Apache-2.0 before) | The README lists Managed SaaS (software as a service) and Self-Managed editions; Self-Managed "adds distributed deployment and official support, activated by a license key" | The team's post of 20260326: the Apache-2.0 licence "imposes weak restrictions on commercial service providers" | [21][22] |
| 20260508 | [claude-mem](../projects/claude-mem.md) | Apache-2.0 (AGPL-3.0 from 20250911 to 20260508; a binary licence before) | Hosted cloud, team sync, enterprise features, premium knowledge agents and private evaluations are "reserved outside the Apache-2.0 public implementation"; its server v0.1 ships none of them | The commit that replaced the file (a server-beta change) does not mention licensing; the licence page, undated, says Apache-2.0 suits a layer "embedded broadly inside developer tools, local agents, MCP clients" | [34] |
| 20260722 | [Graphify](../projects/graphify.md) | Apache-2.0 (MIT before; MIT text kept) | The README leads with Graphify Cloud, an "always-on" layer | The commit: Apache-2.0 adds a patent grant, a patent-retaliation clause and inbound-contribution terms. It does not mention the Cloud | [23][24] |
| none found (no licence change) | Cognee | Apache-2.0 | The README calls the bundled GLiNER extractor "a demo"; the Postgres graph store is a demo too, with the production version "a licensed product" | Not stated | [19] |
| 20250402 and 20261009 (no licence change) | Zep and Graphiti | Apache-2.0 | Zep's own engine is not in the repository; Graphiti's README contrasts Zep's graph database service with "Bring your own"; pull request 1964 leaves out flagged features | See the removals table | [10][12][16] |

*Reading:* every project in this table has a hosted or licensed counterpart that its README, page or post points to. Three of the seven projects (OpenViking, Graphify, claude-mem) relicensed, and the reasons they state are about commercial service providers (OpenViking), patents (Graphify) and broad embedding (claude-mem), not about graphs. The directions differ: OpenViking moved to a copyleft licence, Graphify and claude-mem to Apache-2.0. Whether the Cloud product motivated the Graphify change is unstated, and so is whether the hosted engines equal the open code. This is a pattern across six rows (seven projects), not a finding about motive.

## Why it emerged

The sources give causes for only some acts, so this section lists them and does not infer the rest. Zep named its [open-core](../index/open-core.md) design [15]. Graphiti named an upstream database that ended [10][11]. Microsoft named a change in frontier models [8]. OpenViking named commercial service providers [21], Graphify named patent terms [23], and claude-mem's licence page names broad embedding [34]. Cognee, RAGFlow, LightRAG and the Mem0 graph move gave none in the pages read. Whether a common cause sits behind the dated acts is unstated.

Chapter 1 gives the background on what had already settled: the ISO graph-query standards, the dispute over whether specialised graph databases survive, and the sources' own view that graph-based retrieval, agent memory and protocols are still fragmented. It is on [what has settled since 2023](../history/settled-since-2023.md); the acts above are part of what is still moving.

## Why it matters

A reader who builds on an open graph component needs to know which parts are still moving. Two dependants acted after Kuzu was archived (20251010): Mem0 deleted its driver with the others (20260414) and Graphiti deprecated its driver (20260608) [3][4][10][13]. Several features sit behind a platform or a licence key [3][22][24], so the open code may not equal what a vendor reports: the Mem0 README says its top scores come from the managed platform [5]. *Reading:* the dated record is a useful check on a project's direction, and it is only a record of acts, not of their effect on retrieval (see below).

## Representative projects

| Project | Strand | Licence (LICENSE file) | Stars at 20261030 19:54 UTC |
|---|---|---|---|
| [Graphify](../projects/graphify.md) | licence | Apache-2.0 [2] | 139,374, flagged fast-growth [1] |
| [RAGFlow](../projects/ragflow.md) | removal, addition | Apache-2.0 [2] | 93,209 [1] |
| [Mem0](../projects/mem0.md) | removal, licence | Apache-2.0 [2] | 68,112 [1] |
| [OpenViking](../projects/openviking.md) | licence | AGPL-3.0 [2] | 41,197 [1] |
| [LightRAG](../projects/lightrag.md) | addition | MIT [2] | 40,443 [1] |
| [Microsoft GraphRAG](../projects/microsoft-graphrag.md) | demotion | MIT [2] | 36,498 [1] |
| [Cognee](../projects/cognee.md) | removal, addition | Apache-2.0 [2] | 32,934 [1] |
| [Graphiti](../projects/graphiti.md) | removal, addition | Apache-2.0 [2] | 32,373 [1] |
| [LLM Graph Builder](../projects/llm-graph-builder.md) | demotion | Apache-2.0 [2] | 5,289 (one commit in 90 days) [1] |
| Zep | demotion | Apache-2.0 [2] | 4,984 [1] |
| Kuzu | archived | MIT [2] | 4,018 [1] |

Stars are signals, not verdicts.

## What is measured, and by whom

No project in the tables ran a before-and-after test of the feature it removed or added. The nearest first-party number concerns a graph variant of Mem0 in the paper; whether that variant is the external graph store later deleted is unstated in the sources read. The independent studies below test [retrieval-augmented generation](../index/retrieval-augmented-generation.md) and memory designs in general. I read abstracts only. Experiments in this documentation that test this trend: none (see [experiments](../experiments/README.md)). Benchmarks named: [LoCoMo](../datasets/locomo.md) [6][31], GraphRAG-Bench [28], [MemoryAgentBench](../benchmarks/memoryagentbench.md) [31].

| Who ran it | Result | First-party? |
|---|---|---|
| Mem0 authors, paper, LoCoMo | graph variant "around 2% higher overall score than the base" [6] | first-party; whether the variant is the deleted store is unstated |
| Han and 11 more authors, version 3 of 20260304 | a unified evaluation protocol; results "highlight the distinct strengths of RAG and GraphRAG across different tasks" (mixed, no overall winner) [27] | not by the systems' authors, as far as the abstract shows |
| Xiang and 6 more, GraphRAG-Bench | notes that "GraphRAG frequently underperforms vanilla RAG on many real-world tasks"; builds a benchmark to find when graphs help [28] | no |
| Wang and 7 more, 20260729 | at 28 corpus sizes, "graph-based RAG encounters construction walls before deployment scale"; [BM25](../index/bm25.md) leads at every larger shared size [30] | no |
| Bao and 5 more, 20261022 | raw dense retrieval plus reranking ranks first in six of seven settings against agentic memory systems [31] | no |
| He and 10 more, 20261025 | "many dedicated memory systems underperform naive RAG" [32] | no |
| Zhou and 7 more, 20260623 | 12 memory systems, five workloads: "no single architecture dominates" [29] | no |

The papers behind the families are in the [papers chapter](../papers/README.md); the origin papers are GraphRAG [25] and LightRAG [26].

## Assessment

*Reading:* strengths. The record is dated, public and checkable: each act above sits in a release note, a commit or a README. Taken together the acts show open graph code being moved, swapped or demoted more often than ended outright (Kuzu is the one archived project; Mem0 deleted its OSS graph store). Additions in LightRAG, Cognee and Graphiti run beside removals elsewhere.

*Reading:* weaknesses. Seven of ten removals (counting "no ETA" as no cause) and six of seven additions name no cause, so motive is guesswork. Independent studies are mixed: [27] reports distinct strengths of RAG and GraphRAG by task, and [30] reports a scale effect (graph-based RAG hits construction walls and BM25 leads at larger sizes); the abstracts do not single out fact lookup. The removals do not cite these studies. The two things that coincide most often are a hosted product and a dropped open feature, and no source links them.

*Reading:* where it is heading. Expect more graph features to sit behind a platform or a licence key, and cheaper extraction to spread in the open code. Status is `steady`: acts keep arriving, none is settled.

## Signals to watch

- Graphiti deleting the Kuzu driver (latest release read: v0.31.2, 20261020) [10].
- RAGFlow's v1.0.0 notes after v1.0.0-rc3 (20261030); whether GraphRAG wording returns [7].
- Microsoft GraphRAG: the notice staying, and any release after v3.3.0 (20261008) [8].
- Mem0: a release after ts-v3.3.1 (20260925) that restores a graph option or gives a reason [4].
- LLM Graph Builder: archiving, or a release after v0.8.7 (20260723) [14].
- OpenViking publishing terms for Self-Managed; Graphify publishing Cloud terms [22][24].
- Any independent evaluation naming a removed or added feature.

## Sources

1. ../../kb-kg/landscape/20261030_1954-github/repos.tsv (a repository path in the archive, not a URL; the site maps it) : stars and flags (snapshot 20261030 19:54 UTC; read 20261102 20:20 UTC)
2. https://api.github.com/repos/OWNER/NAME/license (one call per repository, through the authenticated CLI; OWNER/NAME is each of mem0ai/mem0, infiniflow/ragflow, microsoft/graphrag, getzep/graphiti, kuzudb/kuzu, neo4j-labs/llm-graph-builder, getzep/zep, topoteretes/cognee, HKUDS/LightRAG, Graphify-Labs/graphify, volcengine/OpenViking) : licence of each LICENSE file (read 20261102 20:20 to 20:21 UTC)
3. https://github.com/mem0ai/mem0/blob/main/docs/migration/oss-v2-to-v3.mdx : graph memory Platform-only, drivers removed, about 4000 lines, "not being replaced by an OSS equivalent"; entity collection "separate from and unrelated to graph memory"; "OSS has no graph memory replacement" (re-read 20261102 20:40 UTC)
4. https://github.com/mem0ai/mem0/blob/main/docs/changelog/sdk.mdx : v2.0.0 labelled 2026-04-14; entity extraction and hybrid search; "Graph memory now runs natively as built-in entity linking"; GitHub release v2.0.0 published 2026-04-16 and ts-v3.3.1 on 2026-09-25 via the releases endpoint (changelog re-read 20261102 20:40 UTC; release dates read 20261102 20:21 UTC)
5. https://github.com/mem0ai/mem0 : README: entity linking, "proprietary optimizations" caveat (re-read 20261102 20:42 UTC)
6. https://arxiv.org/abs/2504.19413 : Mem0 (Chhikara, Khant, Aryan and 2 more; 20250428), abstract only; it speaks of "an enhanced variant" with graph-based memory and does not link it to the later OSS store (re-read 20261102 20:41 UTC)
7. https://github.com/infiniflow/ragflow/blob/main/docs/release_notes.md and the README : v0.27.0 released 20260819, deprecation wording, Knowledge Compilation; v1.0.0-rc3 20261030 (read 20261102 20:22 UTC)
8. https://github.com/microsoft/graphrag : README notice; commit 21f7bdf "Add notice. (#2486)", 2026-08-14 15:08 UTC; release v3.3.0 (read 20261102 20:22 UTC)
9. https://github.com/microsoft/graphrag/issues/1512 : closed not planned 2025-11-18; maintainer comment (read 20261102 20:28 UTC)
10. https://github.com/getzep/graphiti : README: Kuzu deprecated, supported databases, Zep graph database service; release v0.31.2 (read 20261102 20:21 UTC)
11. https://github.com/getzep/graphiti/releases : v0.29.2 (2026-06-08, pull request 1548 "mark Kuzu deprecated") and v0.31.0 (2026-10-14) notes (read 20261102 20:29 UTC)
12. https://github.com/getzep/graphiti/pull/1964 : merged 2026-10-09; scope and excluded flagged features (read 20261102 20:24 UTC)
13. https://github.com/kuzudb/kuzu : README note; archived; v0.11.3 on 2025-10-10 (read 20261102 20:22 UTC)
14. https://github.com/neo4j-labs/llm-graph-builder : `frontend/src/components/Layout/Header.tsx` and commit a728de68 of 2026-10-23; the 20260721 version lacks the banner; README and Labs disclaimer; release v0.8.7 (read 20261102 20:22 to 20:27 UTC)
15. https://blog.getzep.com/announcing-a-new-direction-for-zeps-open-source-strategy/ : Zep's post of 2025-04-02 (updated 2026-06-03): open-core reasons (read 20261102 20:23 UTC)
16. https://github.com/getzep/zep : README (Zep Cloud examples) and commit 6a9ce060 "Deprecation notice", 2025-04-02 (read 20261102 20:23 UTC)
17. https://github.com/topoteretes/cognee/releases/tag/v1.6.3 : released 2026-10-07; `temporal_cognify` removed (read 20261102 20:23 UTC)
18. https://api.github.com/repos/topoteretes/cognee/releases/tags/v1.6.0 and https://github.com/topoteretes/cognee/releases : v1.6.0 (2026-09-18, keyless workflows; breaking change "GLiNER removed from default Docker image") (v1.6.0 notes re-read 20261102 20:40 UTC); v1.6.6 (2026-10-29, conflict resolution) (read 20261102 20:24 UTC)
19. https://github.com/topoteretes/cognee : README: GLiNER extraction with no LLM key (undated), image "ships with the GLiNER runtime baked in", "demo", "licensed product" (re-read 20261102 20:40 UTC)
20. https://github.com/HKUDS/LightRAG : README news: 2026.03 OpenSearch, 2026.05 merge of RAG-Anything; news entries, not releases (re-read 20261102 20:40 UTC)
21. https://github.com/volcengine/OpenViking/discussions/992 : relicensing plan of 2026-03-26 (read 20261102 20:24 UTC)
22. https://github.com/volcengine/OpenViking : commit ce998873f9 (2026-03-30) and README: editions and licences (read 20261102 20:24 UTC)
23. https://github.com/Graphify-Labs/graphify : commit ba7f9ea9d8, 2026-07-22 22:50 UTC, "relicense from MIT to Apache-2.0" (read 20261102 20:23 UTC)
24. https://github.com/Graphify-Labs/graphify : README: Graphify Cloud (read 20261102 20:23 UTC)
25. https://arxiv.org/abs/2404.16130 : From Local to Global, GraphRAG (Edge, Trinh, Cheng and 7 more; 20240424) (read 20261102 20:26 UTC)
26. https://arxiv.org/abs/2410.05779 : LightRAG (Guo, Xia, Yu and 2 more; 20241008) (read 20261102 20:26 UTC)
27. https://arxiv.org/abs/2502.11371v3 : RAG vs. GraphRAG (Han, Ma, Wang and 9 more; v1 20250217, v3 20260304), abstract of v3 only (re-read 20261102 20:41 UTC)
28. https://arxiv.org/abs/2506.05690 : When to use Graphs in RAG (Xiang, Wu, Zhang and 4 more; 20250606), abstract (read 20261102 20:26 UTC)
29. https://arxiv.org/abs/2606.24775 : Are We Ready For An Agent-Native Memory System? (Zhou, Zhou, Han and 5 more; 20260623), abstract (read 20261102 20:26 UTC)
30. https://arxiv.org/abs/2607.26497 : BM25 Wins at Scale (Wang, Xu, Wang and 5 more; 20260729), abstract of v3 (re-read 20261102 20:41 UTC)
31. https://arxiv.org/abs/2610.30755 : Is Complex Agentic Memory Always Needed? (Bao, Zhang, Zhang and 3 more; 20261022), abstract; names LoCoMo and MemoryAgentBench (re-read 20261102 20:42 UTC)
32. https://arxiv.org/abs/2610.34073 : Memory Tax (He, Zhoubian, Yang and 8 more; 20261025), abstract (read 20261102 20:26 UTC)
33. https://api.github.com/repos/OWNER/NAME/commits?path=LICENSE (authenticated CLI; OWNER/NAME is each of mem0ai/mem0, topoteretes/cognee, getzep/graphiti, infiniflow/ragflow, HKUDS/LightRAG, microsoft/graphrag, Graphify-Labs/graphify, volcengine/OpenViking) : dates and messages of licence commits (read 20261102 20:24 to 20:28 UTC; Mem0, Cognee and Graphiti re-read 20:42 UTC: last licence commits 2024)
34. https://api.github.com/repos/OWNER/NAME/commits?path=LICENSE and the file text at each commit (authenticated CLI; a scripted pass over the 37 repositories of the projects chapter and getzep/zep, kuzudb/kuzu and LadybugDB/ladybug, the last eight commits of each file) : thedotmack/claude-mem, binary licence 20250906, compiled-form licence 20250909, AGPL-3.0 20250911 and 20251003, Apache-2.0 20260508 08:20 UTC (commit 36b0929f, a server-beta change), and its `docs/license.md` ("Why Apache-2.0?", "Reserved commercial/private areas"); Mirix-AI/MIRIX, MIT 20250416, Apache-2.0 20250711 (a5944e0c); modelcontextprotocol/servers, MIT 20250816, composite 20260112 22:50 UTC (6b36e3c2, "update licensing to Apache 2.0 for new contributions"); FalkorDB/FalkorDB, commit 1665fbd9 of 20260802 18:12 UTC, `LICENSE` added (655 lines) and `LICENSE.txt` removed (557 lines); no change of licence type in 2025 and 2026 for Zep, Kuzu (year edit 20250916), Mem0, Cognee, Graphiti, RAGFlow, LightRAG, Microsoft GraphRAG and LLM Graph Builder (read 20261102 22:56 to 22:59 UTC)
