---
slug: lightrag
neutral-entry: ../../kb-kg/projects/lightrag.md
investigated: 20260725
updated: 20261030 19:06 UTC
licence-gate: open
---

# LightRAG: what Pinakes takes from it

The facts about the project itself are in its [neutral entry](../../kb-kg/projects/lightrag.md). This page
holds only the Pinakes-specific reading.

How this page was checked: the Pinakes documents named below were read from a local checkout between
20261030 18:58 and 19:03 UTC. Its `STATUS.md` header reads "Latest release: 0.32.8 · last reviewed 20261029
18:57"; the public `main` may be newer. The documents are
[`STATUS.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md),
[`ROADMAP.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md),
[`CLI.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md) and
[`DESIGN.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md).

## Verdict

LightRAG is a cost model to avoid and a source of two cheap retrieval ideas; as of Pinakes 0.32.8 neither idea is
built in LightRAG's form, and the nearest built relative (the graph expansion channel) was measured and ships off.

## What Pinakes takes

The July reading kept five ideas on file, plus two confirmations. The design area each feeds is named in the
third column.

| # | Idea (LightRAG mechanism) | Feeds | July plan |
|---|---|---|---|
| T1 | **Caller-supplied keywords.** `QueryParam.hl_keywords` and `ll_keywords` make the keyword LLM call unnecessary when the caller passes them. | The MCP surface and the [free pipeline](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md#41-the-free-pipeline-every-query-0) | Optional `entities=[]` and `concepts=[]` on `pinakes_search`: entity-ish terms go to FTS5 and link-graph lookups, concept-ish terms to embedding search. The calling agent does the split in its own reasoning, at no cost. |
| T2 | **Edges as a retrieval channel.** `relationships_vdb` indexes relations, so search can land on an edge, not only a node. | The graph release | Render `links` rows and structural edges to text and index them in FTS5 or embeddings: LightRAG's channel without its LLM, free at build time. |
| T3 | **Context-only retrieval.** `only_need_context` returns context and skips the answer call. | The MCP surface | Every retrieval surface returns context, never a generated answer, "even for `--deep`". |
| T4 | **Rebuild from stored artifacts.** `rebuild_knowledge_from_chunks` re-derives graph state from cached extraction results without a model call; `_combine_descriptions_dedup` stops re-extraction from piling up duplicate facts. | Lazy extraction, if it ever lands | Copy the shape, but keep the artifacts in committed sidecars, not an opaque cache; copy the duplicate guard. |
| T5 | **A hash-keyed document-status queue** (`DocStatusStorage.get_doc_by_content_hash`). | [Sync semantics](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md#64-sync-semantics-the-part-that-silently-corrupts-a-kb-if-left-vague) | A clean pattern for making `pnk sync` resumable. |

Two confirmations the July note drew, both judgements of that reading:

- LightRAG's whole cost centre is the sync-time extraction pipeline Pinakes had ruled out. Its mitigation, an
  extraction cache that makes rebuilds free, is a hidden approximation of writing extraction results back into
  sidecars, except that LightRAG's copy is internal state that cannot be committed.
- Reciprocal-rank fusion plus a local cross-encoder was judged ahead of LightRAG's round-robin fusion. No
  head-to-head measurement of the two appears in either the July note or the Pinakes documents read.

## What Pinakes leaves

| Left | Why (July reading) |
|---|---|
| Eager per-chunk LLM extraction, gleaning and LLM merge-summaries | Breaks the free path and the no-sync-time-extraction decision. July also called it LightRAG's own scaling problem. |
| A mandatory LLM keyword call at query time in every graph mode | With caller-supplied keywords it is unnecessary; no LLM should sit between the user and retrieval. |
| Rerank through "hosted APIs only" | July: Pinakes' local cross-encoder is "strictly better" for the free path. **Update:** LightRAG's rerank endpoint can be self-hosted (see the neutral entry), so the remaining difference is that Pinakes reranks in process with no separate server. "Strictly better" is unmeasured. |
| Three separate vector indexes and a pluggable storage layer with many bindings | A single SQLite file is simpler. |
| Exact-name entity merging | If extraction ever exists, name-match-only merging silently forks entities (July example: "LightRAG" and "LightRAG framework"). Not to be copied. |
| Five or more query modes pushed onto the caller with no router | Pinakes has one `search` and lets the agent compose tools, so no modes are invented. |

## Where it landed in Pinakes

State as of Pinakes 0.32.8. "Not built" means the documents read do not list it as built.

| # | Built? | What the documents say |
|---|---|---|
| T1 keyword slots | **Not built** | The documented `pinakes_search` arguments are `query`, `kb?`, `tags?`, `path_prefix?`, `source_type?`, `k?` ([CLI.md, `pnk serve`](https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md)); there is no `entities` or `concepts`. `STATUS.md`, `ROADMAP.md` and `DESIGN.md` do not list the slots as built or scheduled. No document read records a decision to drop them, so whether they were declined or merely never scheduled is **unstated**. |
| T2 edges as a channel | **Nearest thing built, a different mechanism; the LightRAG form is untested** | The graph release (0.11.0, `schema_version` 3) derives a `nodes`/`edges` table over chunk, document, tag, heading and directory nodes and adds an expansion channel, `[retrieval] graph_channel`. Its gate ran on 20260804 22:52: the multi-hop column of STATUS reads 7/20 with the channel off and 4/20 with it on; 0 questions improved and 3 regressed, p = 1.0000. **`expand` ships `off`.** Finding recorded: "reachable is not retrievable" ([STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md#did-the-expansion-channel-earn-its-default--no-measured-20260804-2252)). This measures graph expansion, not an index of edge text in FTS5 or embeddings, so it is no evidence about T2 as written. Further channels (personalised PageRank, the `[ner]` extra) are "not built", gated on measurement and not scheduled ([ROADMAP](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md)). |
| T3 context only | **Held on the free surface; not held for `--deep`** | `pnk search` and the four MCP tools (`pinakes_search`, `pinakes_get`, `pinakes_links`, `pinakes_list_kbs`) return cited passages, documents, link neighbours or the list of KBs; none is documented as generating an answer. `pnk ask` "never synthesises an answer" without `--deep` ([CLI.md](https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md)). `pnk ask --deep`, shipped in 0.24.0 and working against the live API since 0.25.1, is a paid opt-in command that does synthesise an answer ([STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md)). So the July wish "even for `--deep`" was not carried through; `--deep` is not among the MCP tools. |
| T4 rebuild from artifacts | **Partly, and not for graph facts** | There is no graph-fact extraction to rebuild. The same shape exists for PDF text: `--rebuild` re-chunks a paid document from the extraction cache, and "a rebuild never spends" (decision D-15, [ROADMAP](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md)). The lazy, agent-driven path is the deep release (0.24.0 to 0.26.0); it does not write its discoveries back by itself: 0.26.0 prints suggested `links[]` entries (`rel: co-cited`, `origin: deep`) for the user to paste into a sidecar, and `--write-suggestions` is "not planned". A run transcript is stored under `.pinakes/deep/<operation_id>.json` (0.25.0). The duplicate-fact guard has nothing to guard. |
| T5 resumable sync | **Not traced to LightRAG** | No document read connects any sync behaviour to LightRAG. Adjacent facts: since 0.10.0 an interrupted first sync is reported by `pnk doctor` as `WARN sync completeness` with the remedy `pnk sync` (not `--rebuild`, which would discard the embeddings already written), and `pnk sync` prints live progress ([STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md)). |
| Leaves | **Held** | No eager LLM graph extraction exists. STATUS names two paid entry points, the `claude-vision` PDF extractor and `pnk ask --deep`; a KB spends only when its manifest or a command asks for it. `pnk search` is "BM25 + vector cosine + RRF fusion + optional local rerank" ([ROADMAP](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md)); the index is SQLite (same document, 0.1.0 row). |

## Licence gate

**Open.** LightRAG is MIT-licensed, read from its `LICENSE` file on 20261030 18:58 UTC (see the neutral entry).
Pinakes is Apache-2.0 ([Pinakes README](../README.md)). The MIT text allows copying if the copyright and permission
notice stay with the copied portions. Whether any LightRAG code was copied is **unstated**; the July reading took
ideas only. Ideas and measured results are free to reuse; source is not covered by this page.

## Changed since July 2026

- 20261030: no change found in the licence (MIT) or in the repository's status (not archived, not renamed).
  Details are in the neutral entry's changed section.
- 20261030: the rerank "leave" is restated above. LightRAG's rerank is no longer fairly described as hosted-only; the
  verdict is unchanged.
- 20261030: T1's source mechanism is unchanged. `get_keywords_from_query` still returns the caller's
  `hl_keywords` and `ll_keywords` without an LLM call when either list is non-empty, and LightRAG added a
  separate `KEYWORD` model role in May 2026.
- 20261030: **open item.** T1 and T2, the two retrieval ideas the July reading rated worth taking, have no recorded
  decision in the Pinakes documents read: not built, not declined, not scheduled. The decision is the owner's.
- The verdict is unchanged.
