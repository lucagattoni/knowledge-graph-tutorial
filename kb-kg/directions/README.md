# Directions: what the field is trying

**Status:** first draft, written 20261030. Nine pages, each built from the project entries in
[`../projects/`](../projects/README.md) and from the [papers and benchmarks](../papers-benchmarks/README.md)
page. Each page keeps three voices apart: what a project **claims**, what was **measured** and by whom, and a
marked **Reading**. None ranks projects, recommends one, or says which direction is winning.

| Page | The question it answers | What its own summary says |
|---|---|---|
| [From eager LLM-built graphs to cheaper ones](eager-to-lazy-graphs.md) | How are projects cutting the cost of building a graph with an LLM? | Five routes. Nearly every figure is the authors' own, and no study compares the five on one corpus. |
| [Where graph features are removed and added](graph-features-in-and-out.md) | Which projects dropped or added a graph feature, and why? | Eight dated removals across 21 entries; four give a reason, and it concerns the project or company, not a measured weakness of graphs. |
| [Memory layers and temporal graphs for agents](agent-memory.md) | What are the design families for agent memory, and what has been measured? | Eighteen projects in five families. Scores are mostly first-party, on two conversational benchmarks. |
| [Markdown files as the knowledge base](plain-files-and-wikis.md) | What do the file-based knowledge bases share, and where do they differ? | Nineteen entries; eight were created or repurposed between 20260404 and 20260408 after an "LLM wiki" gist. |
| [Retrieval by reasoning over structure](reasoning-retrieval.md) | What happens when a model navigates structure instead of using vectors or a graph algorithm? | Five variants. Almost every positive number comes from the method's authors. |
| [Code knowledge graphs for coding agents](code-knowledge-graphs.md) | How do the 2026 code-graph projects build and query their graphs? | Six projects. Savings claims run from 62% fewer tokens to ratios of 63x to 136.8x against different baselines. |
| [Who can build on what](open-core-and-licensing.md) | What do the licences and hosted tiers permit, and what changed? | Of 31 entries, 12 permissive, 9 GPL or AGPL, 6 source-available or custom, 4 unclear. |
| [Graph databases, embedded stores and MCP](infrastructure-and-protocols.md) | What do the projects run on, and how do they reach agents? | The embedded graph database Kuzu was archived on 20251010; no entry measures one storage choice against another. |
| [What is measured and what is only claimed](evidence-and-claims.md) | Which performance claims have a stated method and an independent check? | Twenty-five claims from 22 projects, sorted into three classes; few have an independent check. |

## What recurs across the pages

*Reading, not a finding of any one page.*

- **The numbers are mostly first-party.** Six of the nine pages say so for their own area:
  [eager-to-lazy-graphs](eager-to-lazy-graphs.md), [agent-memory](agent-memory.md),
  [plain-files-and-wikis](plain-files-and-wikis.md), [reasoning-retrieval](reasoning-retrieval.md),
  [code-knowledge-graphs](code-knowledge-graphs.md) and [evidence-and-claims](evidence-and-claims.md).
- **Independent studies, where they exist, are mixed and often favour a plain baseline.** Three pages
  record outside results that put plain or reranked vector retrieval, or long-context baselines, level with or
  ahead of the more elaborate system on some tasks: [agent-memory](agent-memory.md),
  [reasoning-retrieval](reasoning-retrieval.md) and [eager-to-lazy-graphs](eager-to-lazy-graphs.md). Each limits
  that to the setups it read; none says graphs do not help.
- **When graph features leave, the stated reasons are about the project.** The page on
  [graph features](graph-features-in-and-out.md) finds maintenance, successor products and unmaintained
  dependencies, not measured weaknesses, among the reasons given, and four removals give none.
- **What is open depends on the business model.** [Open core and licensing](open-core-and-licensing.md)
  records relicensing, features reserved for a hosted tier, and repositories published without their engine.
- **MCP recurs.** The [infrastructure page](infrastructure-and-protocols.md) counts 13 of the 16 entries
  behind it (databases, memory systems and file-based projects together) as exposing an MCP server, and says
  the count is its own computation. The [file-based projects](plain-files-and-wikis.md) are described as pairing
  a derived index with an agent interface, "often MCP".
- **Star counts are the weakest signal here.** The first snapshot flags nine repositories as fast-growing (the second flags ten, adding
  [codebase-memory-mcp](../projects/codebase-memory-mcp.md), which entered the watchlist in between). Several
  entries report that the stargazers endpoint returned 404, so no star timeline was examined for them, and no page
  concludes anything about how the stars arose.

## Limits of this section

- These are first drafts, several well over their length target, and written the day the entries were.
- The selection of projects is one editor's, made from a search with incomplete recall; see
  [the selection](../landscape/20261030_1922-selection.md) for what was left out and why.
- Every page ends with dated *signals to watch*. Re-run
  [`tools/gh_snapshot.py`](../../tools/gh_snapshot.py) and re-read those signals before relying on a
  page after a few weeks: the [timeline](../llm-era/README.md) shows how much changed in 2026 alone.
