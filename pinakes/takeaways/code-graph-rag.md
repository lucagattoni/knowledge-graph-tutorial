---
slug: code-graph-rag
neutral-entry: ../../kb-kg/projects/code-graph-rag.md
investigated: 20260726
updated: 20261030 19:08 UTC
licence-gate: open
---

# Code-Graph-RAG: what Pinakes takes from it

The facts about the project itself are in its [neutral entry](../../kb-kg/projects/code-graph-rag.md). This page
holds only the Pinakes-specific reading. Source numbers in square brackets refer to the Sources list of that entry.

## Verdict

Live evidence that a deterministic structural index with agent-driven navigation over MCP works, in a domain (code) with far denser edges than documents: take its guardrail catalogue, its two-step retrieval shape and its incremental-update idea; leave NL-to-Cypher inside the server, an agent inside the server, and write tools on the same surface. The July verdict (20260726) stands on the 20261030 re-check, with one supporting argument (infrastructure weight) now stale; see "Changed since July 2026".

The July investigation called this "the same pattern as Pinakes' R6 bet, in production for code": a deterministic structural index, and the agent does the traversal. See [R1-R7](../recommendations-r1-r7.md) for R6.

## What Pinakes takes

Each idea is from the July investigation. The design section named is the one the Pinakes docs say the feature implements, where they say so.

| Idea | Why it is useful, from the project's evidence | Pinakes feature it feeds |
|---|---|---|
| **Typed verbs instead of a query language.** The project's validators and prompt rules (no unbounded paths, `LIMIT`, no whole-node dumps, project scoping) exist because its graph verb is open-ended Cypher. Encode read-only, bounded, scoped access in the signature, and enforce the depth bound in code, not in a prompt | The project's guardrail list is an empirical catalogue of how agents misuse an open query surface: unbounded traversals, whole-node dumps, unscoped matches, unlimited listings [17][18] | `pinakes_links(doc_id, rel?, direction?, depth?)` ([DESIGN § 6.2](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md)) |
| **Double-capped results with an honest summary.** Row cap, then a token budget, then a field that tells the agent truncation happened so it narrows instead of retrying | `query_code_graph` caps rows (default 500) then tokens (default 16,000) and sets a `summary` [19][20] | Apply to search and links alike (the July recommendation) |
| **Two-step retrieval.** Search returns identifiers and light metadata; a second call fetches content | `semantic_search` then `get_code_snippet`; the project's own docs describe it as composing well [22][6] | `pinakes_search` then `pinakes_get` |
| **Cross-index enrichment.** Vector hits come back annotated from the graph, so the next hop needs no join by the agent | `semantic_search` hits carry qualified name and type [22] | Search hits could carry link counts or the relation types present, so `pinakes_links` is an informed next hop |
| **Hash-gated incremental reindex that keeps inbound edges.** Re-parse only changed files, keep edges from unchanged files | MD5 hash cache, inbound-edge capture and restore [21]; the project keys edges on qualified names, and Pinakes' permanent ULIDs are a stronger key | `pnk sync` (change detection) and the sidecar links |
| **Tool descriptions as the routing layer.** The agent picks the verb; no code-side router in MCP mode | Routing is steered only by tool-description wording [6] | Matches the plan of no in-engine router |

## What Pinakes leaves

| Item | Why it is left |
|---|---|
| **NL-to-Cypher inside the server** | An LLM inside a tool call breaks the free path, adds a failure mode, and duplicates intelligence the calling agent already has. The project itself now tells callers to prefer its deterministic tools and keeps `query_code_graph` for open-ended questions [6] |
| **An internal agent (`ask_agent`)** | An agent inside the server competes with the caller. Pinakes exposes verbs only |
| **Write tools on the same surface** (`write_file`, `surgical_replace_code`, `wipe_database`, and now `rename`, `change_signature`) | `docs/` belongs to the user; the MCP surface stays read-only. The project added a read-only mode that removes its write tools [6], which makes read-only the project's own optional posture |
| **Client-side over-fetch to scope vector hits** | A workaround for vector-store filter limits; a SQL `WHERE` clause makes it unnecessary [22] |
| **Infrastructure weight as a reason** | **Stale, no longer used as an argument.** In July the project required a Docker-hosted Memgraph plus Qdrant or Milvus. Its default is now an embedded SQLite file for both graph and vectors [5][8][10]. What still separates the two designs is scope: code needs open traversal over dense edges, while Pinakes' depth-bounded document links are covered by a bounded traversal over a links table |

## Where it landed in Pinakes

Source for what is built: Pinakes [STATUS](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md) (latest release 0.32.8, last reviewed 20261029 18:57, read 20261030 19:05 to 19:07 UTC), [ROADMAP](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md), [CLI](https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md) and [DESIGN](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md). Searched for this project by name (`code-graph-rag`, `cgr`, `memgraph`) in STATUS, ROADMAP and DESIGN: **no hit**. So the Pinakes documents do not credit this project for any feature; what follows matches each July idea to what Pinakes built, and says "unstated" where the documents do not connect the two.

| Idea | Built? | What the Pinakes documents say |
|---|---|---|
| Typed verbs, hard server-side depth cap, no query language | **Built, 0.5.0** | `pinakes_links` is on the MCP surface with the `pnk links` flags `--rel`, `--direction`, `--depth`; depth is "server-capped at 3"; ROADMAP 0.5.0: "Depth capped at 3 server-side, fan-out capped, no query language, ever." Whether the cap was taken from this project: unstated |
| Honest truncation signal | **Built for links** | `pnk links --json` returns `{document, neighbours, frontier, unresolved, truncated}` (CLI). A two-stage row cap then token budget for `pinakes_search`: not found in the documents read |
| Two-step retrieval | **Built** | The MCP surface is `pinakes_search`, `pinakes_get`, `pinakes_links`, `pinakes_list_kbs` (STATUS); `pinakes_get` takes the `doc_id` that search returns (CLI) |
| Cross-index enrichment (search hits carry link counts or relation types) | **Not built, or not found** | Searched STATUS, ROADMAP, CLI and DESIGN for link-count terms: no hit. Treat as not built |
| Hash-gated incremental reindex that keeps edges | **Built, as the base of `pnk sync`** | DESIGN: "walk sources, compare content hashes, re-process only what changed"; path unchanged and hash changed means "re-chunk and re-embed; keep the ID". IDs are permanent ULIDs ("never renumbered, never regenerated", ROADMAP), and authored links are stored in each document's sidecar, not in the derived index (ROADMAP 0.4.1, 0.5.0) |
| No in-engine router | **Built** | The MCP server offers four verbs and no reasoning tool |
| No internal agent on the MCP surface | **Built, with one CLI exception** | `pnk ask --deep` reasons and can spend, but "there is no MCP tool for this and a test asserts the server never loads the module" (CLI) |
| Read-only MCP surface | **Built** | The four MCP tools above read and traverse; the one link-authoring command (`pnk link`, 0.6.0) is a CLI command that writes into a source document's own sidecar (ROADMAP 0.6.0) |

Not built, for completeness: any Cypher or graph-database layer, which was never a goal; and a `context`-style budgeted slice around a document (the project added one after July, see below).

## Licence gate

Open. The `LICENSE` file is MIT, read from the live repository on 20261030 18:58 UTC; the July note also recorded MIT [3]. MIT is compatible with Pinakes' Apache-2.0 with the notice retained. Whether any code was copied from this project into Pinakes: unstated in the Pinakes documents read. Ideas and measured results are free to reuse; source needs the MIT notice.

## Changed since July 2026

Checked 20261030 (see the neutral entry for numbers and sources).

- **Verdict unchanged.** The project's later work supports two Pinakes choices. It added deterministic typed tools (`callers`, `callees`, `definition`, `resolve`, `importers`, and others) and tells its callers to prefer them over NL-to-Cypher [6]; that is the "typed verbs" argument made by the project itself. It also added a read-only server mode [6].
- **One July argument is now stale.** "Infra weight: Docker Memgraph + Qdrant/Milvus + torch against a single SQLite file" no longer separates the two: the project's default is an embedded SQLite file for the graph and for vectors [5][8][10]. Removed from the reasons above.
- **New input worth a decision: a budgeted context slice.** The project's `context(target, budget_tokens)` returns the target plus its callers' call lines, callees' signatures, linked tests and linked documentation, ranked by graph distance and trimmed to a token budget, with an `omitted` list that says why each skipped piece would have been included [11]. This is a closer model of the "honest summary" idea than the July row-cap-and-summary. Pinakes has no equivalent in the documents read. Whether a document-level slice would help is an open question for `pinakes/experiments/`; no experiment has been defined.
- **Overlap to watch: Markdown links.** The project now indexes Markdown documents: headings as `Section` nodes and relative links as `LINKS_TO` edges with `broken_links` listed per document [9]. Pinakes stores authored links in sidecars instead of deriving them from document text. The two designs answer the same question differently; no comparison has been run.
- **Overlap to watch: durable notes.** The project's `annotate` stores agent-written notes in the graph, anchored by content hash and graded EXACT, STALE, MOVED, AMBIGUOUS or LOST after each sync [6][9]. Pinakes' counterpart is the permanent-ULID sidecar link. Different mechanisms for edge survival across edits; no comparison has been run.
- **Evidence status.** The project now publishes self-measured retrieval figures (graph F1 0.91 against grep F1 0.54 on its own package) but no end-to-end agent result [26]. Pinakes' own measurement work is separate and is not affected.
- **The project is much bigger and faster-moving than in July** (more than twice the stars, 6,772 commits since 20260801), so any July statement about a small, stable codebase to read as a reference is out of date [1][4].
