# Resume

Last updated 20261030 19:44 UTC. Deep entries committed so far (9 of 10): llm-graph-builder, tigerless-agent-memory,
pageindex, mem0, llm-wiki-nashsu, graphify, openviking, cognee, basic-memory. Still running: letta, and the 13 card batches. Decisions: [`DECISIONS.md`](DECISIONS.md). Branch:
`worktree-20261030_1852-kb-kg-docs-scaffold` (private remote; nothing is on `main` yet).

## Done and committed

| Commit | What |
|---|---|
| `2d95ad9` | Scaffold, templates, public-safety gate |
| `718d8e8` | `kb-kg/`: primer, LLM-era timeline, literature review, papers and benchmarks |
| `ddf740c` | 12 July investigations, each split into `kb-kg/projects/` and `pinakes/takeaways/` |
| `f1ddbfd` | `pinakes/`: approach record, recommendations R1 to R7, ClaudeKB precedent |
| `c8bf9c2` | Project `CLAUDE.md`, added at the owner's yes |
| `abc6be7` | `tools/gh_snapshot.py`, 57 tests, mutation-checked on the 90-day rule |
| `bcd1b3d` | First landscape snapshot, 20261030 19:13 UTC: 924 repositories, data only |
| `d955525` | `pinakes/experiments/`: what Pinakes has measured and how it decides |
| `f49c44d` | Proposed project selection; seven missed projects added to the watchlist |
| `b1fd9d2` | The card form defined in the entry template |
| `0426230` | Four pilot cards: kuzu, claude-mem, tencentdb-agent-memory, openkb |

## Running (wave B, started about 19:30 UTC)

The owner approved the [selection](kb-kg/landscape/20261030_1922-selection.md) with a pilot first. The
pilot (4 hard-case cards) cost 159,932 tokens and 59 tool calls; it is reviewed and committed (`0426230`).

- **10 deep entries** (one file each in `kb-kg/projects/`): mem0, cognee, openviking, letta, pageindex,
  llm-wiki-nashsu, basic-memory, tigerless-agent-memory, graphify, llm-graph-builder.
- **10 card batches of 4**, 40 cards, by slug: rag-anything, semantica, yuxi, hyper-extract; m-flow,
  nano-graphrag, kag, neo4j-graphrag-python; graphrag-sdk, ai-knowledge-graph, trustgraph, ontogpt;
  gliner, deepke, a-mem, mirix; supermemory, hindsight, memos, memori; memu, everos, honcho, memmachine;
  zep, claude-obsidian, obsidian-mind, open-knowledge; llm-wiki-agent, obsidian-wiki, llm-wiki-compiler,
  llmwiki-lucasastorian; karpathy-llm-wiki, okf-agent-memory, open-knowledge-format, kiwifs;
  understand-anything, codegraph, codebase-memory-mcp, code-review-graph.

## Launched late: the platform allows 20 concurrent writers

These three batches were refused at 19:30 and **launched at about 19:40 to 19:45 UTC as slots freed** (11, 12
and 13 all running). Do not launch them again; check `kb-kg/projects/` for their files first. If a restart
finds them missing, relaunch from this table (brief: `wave-b-brief.md` in the session scratchpad, or rewrite
it from `kb-kg/projects/_TEMPLATE.md` and the rules in `CLAUDE.md`). Card form, one file each,
`kb-kg/projects/<slug>.md`, category `adjacent`, graph databases and platforms covered only for what
bears on KBs and KGs built or queried with LLMs:

| Batch | Slug: repo | Note |
|---|---|---|
| 11 | neo4j: neo4j/neo4j | GPL-3.0 community edition; say what other editions exist as the project states it |
| 11 | falkordb: FalkorDB/FalkorDB | licence NOASSERTION: read the file |
| 11 | memgraph: memgraph/memgraph | licence NOASSERTION: read the file |
| 11 | surrealdb: surrealdb/surrealdb | licence NOASSERTION: read the file |
| 12 | dify: langgenius/dify | NOASSERTION; the licence may add conditions: quote them |
| 12 | ragflow: infiniflow/ragflow | what it says about GraphRAG support |
| 12 | llama-index: run-llama/llama_index | the property-graph index, if documented |
| 12 | anything-llm: Mintplex-Labs/anything-llm | |
| 13 | haystack: deepset-ai/haystack | document stores, retrieval, graph support, MCP only |
| 13 | khoj: khoj-ai/khoj | AGPL-3.0; about 89 days since the last push: do not conclude abandonment |
| 13 | mcp-servers: modelcontextprotocol/servers | NOASSERTION; focus on the reference memory server if it exists |

## Next, in order

1. Wave B: review each finished entry against the live API as in wave A (headline facts for every one;
   deeper claims rest on the cited sources), run the gate and the link check, commit one unit at a time.
   Launch the three batches listed above as slots free. Then update `kb-kg/projects/` index and the
   `kb-kg/README.md` status row.
2. Re-run `uv run tools/gh_snapshot.py` after wave B: it picks up the seven watchlist additions and
   produces the first comparison with an earlier snapshot.
3. Wave C: `kb-kg/directions/` (what the field is trying, grouped by direction), the experiments worth
   running next (each states its cost, models and data first and waits for the owner's yes), and the
   Pinakes page on what to test next.
4. Licence for this repository's text, a full content check, then the owner's explicit yes to make it
   public. Only after that: the *historical* banner and link on Pinakes' `docs/graph/`.

## Debts that are written down so they are not lost

- **Unverified items.** Every entry lists its own "not verified" items. Across entries the largest are:
  six literature figures marked unverifiable (`kb-kg/literature/`); whether LazyGraphRAG is in the
  open-source package; many 2026 papers read as title or abstract only; whether the star growth of the
  fastest repositories is organic; the primer's first-use dates for "knowledge base" and for Cyc.
- **Snapshot recall is incomplete.** Seven expected projects were missed by its searches (now on the
  watchlist). Treat the snapshot as a dated sample, not a census.
- **Inconsistencies in Pinakes' own documents**, found while writing `pinakes/experiments/`, to report
  upstream when the owner allows editing Pinakes:
  - the scanned-PDF extraction run costs EUR 0.43 in `STATUS.md` and `MEASUREMENT-RUN.md` but EUR 0.11 in
    `DESIGN.md` (confirmed);
  - `STATUS.md` gives the corpus 107 411 non-transit edges at line 586 and 107 802 at line 631 for the
    same 106 506 sibling edges (confirmed);
  - not re-derived by me: no recorded result for the graph-gate re-run approved 20260825; no labelled
    re-extraction trigger in `audit.py`; a defect count of five against six for the deep-loop report tool.
- **Gate coverage.** `tools/check_public_safe.sh` scans the working tree, not the staged set.
- **A rename in Pinakes.** Another session working in the Pinakes repository told this one (20261030) that
  it is renaming "the template release" in Pinakes' CLAUDE.md and `docs/` and will not edit
  `docs/graph/PINAKES_APPROACH.md`. This repository's copy, `pinakes/approach/PINAKES_APPROACH.md`, and
  `pinakes/recommendations-r1-r7.md` use the old name in places. Re-read them against Pinakes'
  `docs/STATUS.md` once that rename lands, and update the names here. Nothing was changed yet.
- **Benchmark repository.** Describe it, link it only once the API reports it public (it did not at
  20261030 18:52 UTC).

## Not to do

- Do not make the repository public, or touch the Pinakes repository, without the owner's explicit
  yes at that step.
- Do not name private repositories anywhere in this repository.
