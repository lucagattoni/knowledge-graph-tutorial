---
type: chapter
updated: 20261102 20:16 UTC
---

# Applied to Pinakes

This chapter answers one question: what did the field's work on [knowledge bases](../index/knowledge-base.md) and [knowledge graphs](../index/knowledge-graph.md) change in Pinakes, and what did Pinakes build, measure and leave unbuilt? It starts from what Pinakes is, says why it has a chapter here, states the rule for reusing other projects' work, and maps the four pages.

## What Pinakes is

Pinakes describes itself as "A portable, agent-first knowledge base. One directory = one KB." [1] A knowledge base is a plain directory. The user's documents are the source of truth. Next to each document sits a sidecar file (`.pnk.yaml`) that holds a stable ID, tags, links and provenance. The search index is a SQLite file under `.pinakes/`; it is derived, disposable and can always be rebuilt [1].

| Property | What Pinakes says | Source |
|---|---|---|
| Cost of search | [BM25](../index/bm25.md) (SQLite FTS5), local [embeddings](../index/embedding.md) and local [reranking](../index/reranking.md), fused and scored on the user's CPU; no API key needed to search | [1] |
| Who reasons | The caller's agent. The [MCP](../index/model-context-protocol.md) server lists four tools: `pinakes_search`, `pinakes_get`, `pinakes_links`, `pinakes_list_kbs` | [1] [2] |
| Money | Opt-in and capped. STATUS counts two paid entry points: the `claude-vision` extractor for scanned PDFs and `pnk ask --deep` | [1] [2] |
| Links between KBs | Sidecars carry `pnk://<kb-ulid>/<doc-ulid>` references; `pnk links` and `pinakes_links` walk them | [1] |
| Licence | Apache-2.0, from the `LICENSE` file | [3] [4] |

**Latest release and date.** Pinakes' STATUS.md states "Latest release: 0.32.9" and "last reviewed 20261102 15:19" [2]. Its ROADMAP records 0.32.9 as on PyPI as of 20261102 15:15 UTC [5]. STATUS calls itself "the only place in the repo that says what is built" [2]; this chapter follows it. The repository is public and its last push was 20261102 15:29 UTC [4]. A release number is a snapshot: re-read STATUS before relying on it.

## Why this documentation has a Pinakes chapter

Pinakes is maintained by the author of this documentation: both repositories sit under the same GitHub account [4][6]. The field chapters ([history](../history/README.md), [trends](../trends/README.md), [projects](../projects/README.md), papers, datasets, benchmarks) stay field-neutral: they say what a project or paper is, not what Pinakes should take from it. Anything that reads the field through Pinakes' needs lives here, and links back into the field chapters for the facts about other projects. One home per fact: a fact about another project is written once, in its own chapter.

## The licence gate

Pinakes is Apache-2.0 [3][4]. The rule recorded in the archive is: **ideas and measured results from other projects are free to reuse; source code under GPL or non-commercial terms is not** [7]. The archive's reason is that Pinakes ships a network service (the MCP server), so a copyleft or non-commercial licence in copied code would reach anyone embedding it [7]. The rule and its reason are this documentation's own record, not a Pinakes document: Pinakes' README, STATUS.md and ROADMAP.md do not state them [1][2][5]. It is the archive's reasoning, not legal advice.

The `LICENSE` file decides, not the README badge. Read now from the files:

| Project | `LICENSE` file says | Reading for Pinakes | Source |
|---|---|---|---|
| [LinearRAG](../../kb-kg/projects/linearrag.md) | GNU GPL version 3 | ideas and results only | [8] |
| [LogicRAG](../../kb-kg/projects/logicrag.md) | GNU GPL version 3 | ideas and results only | [9] |
| [Youtu-GraphRAG](../../kb-kg/projects/youtu-graphrag.md) | custom licence: academic purposes only, no "commercial or production purposes" | ideas and results only | [10] |

Youtu-GraphRAG's GitHub licence field reads `NOASSERTION`, so the repository metadata cannot settle it; the file can [10]. The archive's takeaways mark the same rule for every project it read [7].

## Map of the chapter

| Page | Question it answers |
|---|---|
| [The Pinakes graph approach](approach.md) | What is the approach, what has Pinakes built and measured against its own STATUS, what is the state of the seven recommendations (R1 to R7), and what did the in-house precedent ClaudeKB teach? |
| [Takeaways](takeaways.md) | Per project: what Pinakes took, what it left, and which licence gate applies |
| [Measurements](measurements.md) | What Pinakes has measured, with numbers, dates and the instrument |
| [Next](next.md) | What Pinakes should measure next, and what blocks each step |

## Where the archive is longer

The pre-rewrite pages stay as evidence: the [Pinakes notes](../../pinakes/README.md), the [approach decision record](../../pinakes/approach/PINAKES_APPROACH.md) and the [R1 to R7 file](../../pinakes/recommendations-r1-r7.md). Where they disagree with Pinakes' STATUS.md, STATUS wins; [the approach page](approach.md) lists the places.

## Sources

1. https://github.com/lucagattoni/pinakes/blob/main/README.md : self-description, directory layout, retrieval, tools, paid paths, licence line (read 20261102 19:37 UTC)
2. https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md : latest release 0.32.9, last reviewed 20261102 15:19; the MCP tool list; two paid entry points; "only place" statement (read 20261102 19:37 UTC)
3. https://github.com/lucagattoni/pinakes/blob/main/LICENSE : Apache License, Version 2.0 text (read 20261102 19:37 UTC)
4. https://github.com/lucagattoni/pinakes : GitHub repository API: public, licence `apache-2.0`, default branch `main`, last push 20261102 15:29 UTC (read 20261102 19:38 UTC)
5. https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md : 0.32.9 on PyPI as of 20261102 15:15 (read 20261102 19:37 UTC)
6. https://github.com/lucagattoni/knowledge-graph-tutorial : this documentation's repository, same account as [4] (read 20261102 19:38 UTC)
7. `pinakes/README.md` (repository path; the archive's own rule, written by the owner of this documentation) : the licence-gate wording and its reason; no Pinakes document states it, checked by searching [1], [2] and [5] for "copyleft", "GPL" and "non-commercial" with no match (STATUS.md and ROADMAP.md read 20261102 20:12 UTC, README.md read 20261102 20:12 UTC; page itself opened 20261102 19:37 UTC)
8. https://raw.githubusercontent.com/DEEP-PolyU/LinearRAG/main/LICENSE.txt : GNU GPL version 3 (read 20261102 19:39 UTC)
9. https://raw.githubusercontent.com/chensyCN/LogicRAG/main/LICENSE : GNU GPL version 3 (read 20261102 19:39 UTC)
10. https://raw.githubusercontent.com/TencentCloudADP/youtu-graphrag/main/LICENSE : academic-purposes-only clause; GitHub licence field `NOASSERTION` (read 20261102 19:39 UTC)
