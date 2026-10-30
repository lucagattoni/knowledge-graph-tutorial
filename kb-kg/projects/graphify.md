---
slug: graphify
repo: Graphify-Labs/graphify
tier: deep
category: adjacent
snapshot: 20261030 19:29 UTC
---

# Graphify

Reading times: repository metadata, README, licence files, `docs/`, `ARCHITECTURE.md` and `BENCHMARKS.md` were
read at 20261030 19:29 UTC; source files, release data and commit history between 19:30 and 19:36; web pages
between 19:33 and 19:37 (the time given for each source is the clock reading taken beside the call). The
first landscape snapshot row is in [`repos.tsv`](../landscape/20261030_1913-github/repos.tsv) [40].

| | |
|---|---|
| Repository | https://github.com/Graphify-Labs/graphify (earlier path `safishamsi/graphify`, which now resolves to the same repository) [1][34] |
| Licence | Apache-2.0, from the `LICENSE` file, which is the standard Apache 2.0 text with the appendix placeholder left unfilled [3]. `NOTICE` reads "Copyright 2026 Safi Shamsi and the Graphify contributors" and `LICENSE-MIT` keeps an MIT text for earlier contributions [4]. GitHub's API, the README badge and PyPI metadata agree (Apache-2.0) [1][6][33]. The project relicensed from MIT on 20260722 22:50 UTC (see "Licence history") [5]. |
| Language | Python (GitHub's primary language); tree-sitter grammars as dependencies [1][36] |
| Stars, forks | 139,363 and 13,291 (20261030 19:29 UTC) [1] |
| Created, last push | 20260403 15:49 UTC, 20261027 18:15 UTC [1]. The default branch is `v8` [1]. |
| Latest release | v0.9.97, 20261027 18:15 UTC [2] |
| Status | active (pushed 3 days before the read); not archived [1] |
| Paper, docs | No paper linked from the README [6]. Docs site https://docs.graphify.com [6]; a book, "The Memory Layer", is linked from the README [6]. |

## What it is

Graphify turns a folder of code, documents, SQL schemas, PDFs, images and audio or video into a knowledge
graph that an AI coding assistant queries instead of searching files [6]. It installs as a `/graphify` skill
for Claude Code and more than 20 other assistants, plus a `graphify` command line and an MCP server [6].
Code is parsed with tree-sitter and no LLM is involved; documents, PDFs and images go through a
model-driven "semantic pass" [6][7]. The graph is a NetworkX graph saved as `graph.json`, with an HTML view
and a Markdown report [6][7]. The same organisation sells Graphify Cloud, a hosted product [6][18]. The
README's description of itself is "Not a vector index. No embeddings, no vector store" [6].

The project is led by one maintainer: `.github/TEAM_MEMBERS` lists a single name and `CODEOWNERS` assigns
every path to the same account [30]. The organisation `Graphify-Labs` was created 20260628 [30]. The README
shows a "Y Combinator S26" badge, added by a commit of 20260522 [6][22]; the YC company page title reads "Graphify Labs: On-device Knowledge Graph engine for Enterprise Software", and I retrieved no more of that page [41].

## How it works

### Build: which parts use a parser and which use an LLM

The repository describes three passes [7]:

| Pass | Input | Method | LLM? |
|---|---|---|---|
| 1. Code structure | source files (README: about 40 languages; `docs/how-it-works.md` still says 25) [6][7] | tree-sitter parse, per-language extractors, a call-graph second pass for cross-file links; SQL tables, views, foreign keys and joins extracted deterministically [7][8] | No [6][7] |
| 2. Video and audio | media files | local transcription with faster-whisper; the prompt is seeded with the top "god nodes" [7] | No [7] |
| 3. Docs, papers, images | Markdown, PDF, images, transcripts | batches of files go to model subagents that return a JSON fragment of nodes and edges; fragments are merged [7][11] | Yes [7][11] |

The default route for pass 3 is the user's own assistant: the skill dispatches parallel subagents on whatever
model the session runs [11][37]. A second route, `graphify extract`, calls a provider API directly (Gemini,
Kimi, Claude, OpenAI, DeepSeek, Azure, Bedrock, Ollama or the `claude` binary) [6][37]. Setting
`GRAPHIFY_BACKEND=none` turns every LLM backend off and leaves a code-only graph [6]. Code files are not sent
to the semantic extractor in the normal pipeline [7]. Community names can come from hub-derived labels or from
the assistant or a configured backend [6][15].

Then the library runs detect, extract, build, cluster, analyse, report and export as separate modules [8].
Communities use the Leiden algorithm, with NetworkX Louvain as a fallback when the `leiden` extra is missing
[6][7]. Community detection uses graph structure only: the semantic-similarity edges the model emitted already
shape the clusters, and there is no embedding step [7]. Extracted files are cached by SHA-256 so re-runs skip
unchanged files [7].

### Nodes and edges

| Element | What exists, per the sources |
|---|---|
| Node kinds (`file_type`) | `code`, `document`, `paper`, `image`, `rationale`, `concept` [11]. Code nodes include files, classes, functions and methods; the committed sample graph shows `contains` and `method` links [25]. |
| Rationale nodes | `# NOTE:` and `# WHY:` style comments, docstrings and ADR or RFC citations become nodes linked to the code they explain (`rationale_for`) [6][32]. |
| Structural relations | `calls`, `imports`, `imports_from`, `inherits`, `mixes_in`, `uses`, `contains`, `method` [6][25] |
| Semantic relations | `implements`, `references`, `cites`, `conceptually_related_to`, `shares_data_with`, `semantically_similar_to`, `rationale_for` [11] |
| Hyperedges | groups of three or more nodes, at most 3 per chunk, kept under the graph's `hyperedges` entry [7][11] |
| Edge attributes | relation, confidence label, `confidence_score`, source file, source location, weight [8][11] |
| Confidence labels | `EXTRACTED` (explicit in source, score 1.0), `INFERRED` (score from a fixed rubric of 0.55 to 0.95), `AMBIGUOUS` (flagged for review) [7][11] |
| Node ids | derived from the full repo-relative path plus the symbol name, lower-case [11] |

`INFERRED` does not always mean a model produced the edge. The architecture notes say a call-graph second
pass emits `INFERRED` `calls` edges from static evidence, and the docs site says the same [8][15]. For
documents the label is the model's own inference [7][11]. The graph's `directed` flag is false but arc
order carries direction, kept in `_src` and `_tgt` markers; a plain NetworkX load loses it, so the project
supplies its own loader [8].

### Storage

Output goes to a `graphify-out/` folder: `graph.json` (NetworkX node-link format, with a schema version and
the producing Graphify version), `graph.html`, `GRAPH_REPORT.md`, a cache folder and optional extras [6][7].
There is no database in the default path. Exporters exist for Obsidian, SVG, GraphML, Cypher, a wiki of
Markdown articles, canvas files and a call-flow HTML; Neo4j and FalkorDB push are optional extras [8][6][36].

### How an agent queries it

| Route | How | Notes |
|---|---|---|
| Slash command | `/graphify query "..."`, `/graphify path A B`, `/graphify explain X` (Codex uses `$graphify`) [6] | The skill first asks the assistant to pick up to 12 tokens from the graph's own label vocabulary, because the matcher is case-folded substring plus IDF with no stemming or synonyms [12]. |
| CLI | `graphify query`, `graphify path`, `graphify explain`; exit code 0 for an answer, 3 for an ambiguous name, 4 for no match [6] | An ambiguous name is refused with candidates listed, not guessed [6]. |
| MCP | `graphify-mcp` entry point, stdio or HTTP transport; ten tools [10][36] | `query_graph`, `get_node`, `get_neighbors`, `get_community`, `god_nodes`, `graph_stats`, `shortest_path`, `list_prs`, `get_pr_impact`, `triage_prs`; each takes an optional project path [10][20]. |
| Always-on nudge | `graphify claude install` and equivalents [6] | On hook platforms (Claude Code, Gemini CLI) a hook fires before search-style tool calls; elsewhere instruction files carry the rule. The Claude Code text tells the agent to run `graphify query` before its first grep and to repeat the rule in subagent prompts [6][13]. |

What comes back is text, not a file. `query_graph` finds seed nodes by keyword scoring (IDF weights and a
trigram prefilter), expands them by breadth-first search (default, depth 3, maximum 6) or depth-first search,
and prints one line per node with source file, line and community, then one line per edge with its relation,
confidence tag and location [10]. Seeds come first, then nodes by hop distance. Output is cut at a token budget
(default 2,000, about 3 characters per token in the code) with a visible "TRUNCATED" notice [10]. The query
path in `serve.py` contains no embedding code; a comment notes that an external ranker could supply start
nodes through a `seeds` argument [10]. Every query is logged locally as JSON Lines unless disabled [6].

## Cost and operating profile

| Item | Reported |
|---|---|
| Code-only graph | No LLM, no API key, runs offline; the project's claim [6]. A third-party run on `httpx` (about 17,750 lines) took 2.1 s fresh and 1.6 s incremental, with "Token cost: 0 input, 0 output" in the report footer [26]. |
| Docs, PDFs, images | One-time model cost per file batch, on the session model or a configured provider [6][11]. The maintainer's 52-file sample report states 6,000 input and 3,500 output tokens [25]. A third-party run on Graphify's own 540-file, 844,497-word repository measured 1,533,913 tokens for the semantic build and about 8,875 tokens per query, and estimated that duplicated generated content inflated the build 2.5 to 4 times; one run, one author [27]. |
| Needs | Python 3.10 or newer; uv or pipx; no database; optional extras for PDF, Office, video, MCP, Neo4j, FalkorDB, SQL and providers [6][36]. |
| Fully local? | Yes for code and for video and audio; for documents only with `--backend ollama` [6]. |
| Telemetry | The README states none; a local query log is on by default [6]. |
| Hosted product | Free $0, Pro $15 a month, Teams $29 to $40 a seat a month, Enterprise by quote and self-hosted "early access" (docs pricing page) [19]. |

## Evidence

### What the project publishes

`BENCHMARKS.md` (header "Last updated: 2026-07-05", yet it reports a check dated 2026-10-05) was run by the
project on its own harness [9]. Every system used one model (Kimi K2.6) and a judge validated against a second
judge at 90.6% agreement (Cohen's kappa 0.81) [9]:

| Suite | n | Graphify | Others, as reported |
|---|---|---|---|
| LOCOMO recall@10 | 300 | 0.497 | BM25 0.362, supermemory 0.149, mem0 0.048 [9] |
| LOCOMO QA accuracy | 300 | 45.3% | supermemory 49.7%, BM25 31.3%, mem0 27.3% [9] |
| LongMemEval-S QA accuracy | 50 | 76% | dense RAG 76%, mem0 70% [9] |
| ERPNext key-fact coverage, fixed coding agent | 6 | 82.0% | grep and read baseline 70.8% [9] |
| INFERRED cross-file edges, FastAPI | 12 | all 12 correct, manual spot-check of 20261005 | none [9] |

Three points limit what these show. The ERPNext arm has six questions [9]. The harness directories named in the
reproduction commands (`memory/`, `crosstool/`) are not in the `v8` tree, and none of the organisation's ten
public repositories is a benchmark harness by name or description (19:37) [8][9][34]. An outside user opened issue 3690 on
20260920 saying `BENCHMARKS.md` was a 404 on `main` and that the headline numbers measure conversational
memory, not code graphs; a commit of 20261005 added the code result [23]. Also, `BENCHMARKS.md` credits "a deterministic graph plus hybrid
retrieval" and a shared local embedder (BGE-m3) [9], while the README says there are no embeddings [6] and the
shipped query path has none [10]. The harness adapter that produced the headline
row was not available to read.

No independent evaluation appears in [`papers-benchmarks`](../papers-benchmarks/README.md), which does not
mention Graphify [40].

### Third-party tests found

| Source | What it did | Result |
|---|---|---|
| HackerNoon, Ishank Choudhary, 20261021 [26] | Ran the CLI on `httpx` without the skill, semantic pass or Cloud | 2,233 nodes, 4,453 edges; 88% `EXTRACTED`, 12% `INFERRED`; `explain` on one class cost 628 tokens against 13,659 to read the file; "surprising connections" less useful; says the graph points to lines but does not hold code. One lookup, one repository. |
| `graphify-on-graphify` repository, 20260606 [27] | Ran Graphify on its own source | `graphify benchmark` printed 46.5x on a baseline the author calls synthetic; about 127x against the real word count; 2.3 to 9x against an assumed agent baseline of 20,000 to 80,000 tokens. One of five test queries missed. Zero stars, no licence. |

### Token-saving claims

The README banner reads "Cut agent token spend by 80%" and ties it to Graphify Cloud; the same figure is in a
callout and in the Cloud section [6]. The lines were added in one commit on 20261010 13:34 UTC, whose message
is "cost-led Graphify Cloud headline (80% fewer tokens)"; the diff adds no link, method or baseline [22]. I
found no measurement behind it:

| Figure | Where | Measured by | Baseline | Method published |
|---|---|---|---|---|
| 80% fewer tokens | README banner, callout, Cloud section [6] | unstated | unstated | no: absent from `BENCHMARKS.md`, `docs/`, the pricing page and the hosted-versus-local page [7][9][18][19] |
| 71.5x per query | `docs/how-it-works.md`, glossary [7][17] | the maintainer, on a 52-file corpus dated 20260404 | reading all files (about 123,488 estimated tokens) against an average BFS answer of about 1,726 tokens [25] | yes, in `worked/karpathy-repos/review.md`; the same review gives 8.8x for the code-only subset [25] |
| 136.8x and 83.6x | docs token-benchmark page [16] | `graphify benchmark` | estimated whole-corpus tokens | yes; the page calls the baseline "an estimate, not a measured prompt" and says it measures tokens, not answer quality [16] |
| about 140K tokens per query | `BENCHMARKS.md`, ERPNext arm [9] | the maintainer | the stuffing alternative "roughly 20x"; the grep arm's tokens are unstated | partial |
| 628 against 13,659 tokens | HackerNoon [26] | a third party | reading one file | yes |

How the built-in ratio is computed: corpus words times 100 over 75 gives a "naive" token count (or nodes times
50 words if no word count is supplied), divided by the average size of five fixed `query_graph` answers
(characters over 4) [14][16]. A pull request of 20261011 changed the benchmark to measure the real
`query_graph` answer; its description shows ratios moving (for example one Django graph from 11.0x to
1,893.5x), so the figure depends on the baseline and the budget [24]. The project's glossary page presents 71.5x
as a worked example, says savings "depend entirely on your repo", and says an assistant that greps selectively
will see less [17]. For scale: 80% fewer tokens equals 5x; 71.5x equals 98.6% fewer. The two are not on the
same baseline.

Other readers: a blog dated 20260408 repeats 71.5x with no method [28]; the HackerNoon author says he did not
test the 80% claim [26]; issue 4749 (20261024), titled "Token 80% reduction" in Korean, contains one line that
translates as "it seems this would be a paid plan" (my translation) [24]. The llm-era note records the same
disagreement with agents that navigate by grep and glob [40], and no source I read measured the two against each
other.

## Open source and cloud

| | Graphify CLI (this repository) | Graphify Cloud |
|---|---|---|
| Licence | Apache-2.0 [3] | hosted service; terms unstated in the sources read |
| Where the graph is built | on the user's machine into `graphify-out/` [18] | indexed from the default branch of GitHub or GitLab repositories, refreshed on each push [18] |
| Query access | slash command, CLI, local MCP server [6][10] | hosted MCP at `api.graphify.com/mcp` with OAuth [18] |
| Extras | `graphify prs` PR dashboard, wiki, merges of graphs [6] | PR reviews, learning from `@graphify` replies, formal verification of changed functions, shared agent memory, cross-repository graphs, Sentry and Jira connectors [6][18] |

The docs say both "give your assistant the same kind of code graph"; whether the engines are the same is
unstated [18]. The repository's top-level layout (`graphify/`, `tests/`, `tools/`, `docs/`, `worked/`,
`scripts/`) holds no hosted-service code that I found [1][8]. The licence applies to the repository, not to the hosted
service.

What the README leads with, in order: logo; a Trendshift badge; a language switcher; a badge row that includes
"Graphify Cloud" and "Y Combinator S26"; then a bold banner, "Cut agent token spend by 80%. Graphify Cloud is
always-on memory...", with a free 14-day trial link; and only then the `/graphify` description and three
bullets for the open-source tool [6]. Until the 20261010 commit the banner said Cloud "keeps this graph
always-on across your whole SDLC" [22]. The CLI also prints a one-time pointer to Cloud after `graphify extract`
in an interactive terminal (commit of 20261009; opt out with `GRAPHIFY_NO_TIPS` or `GRAPHIFY_NO_CTA`) [22][39].
The website's home page presents both: a hosted product and the open-source engine, "Apache 2.0, no account, no
telemetry" [21].

## Licence history

| Date (UTC) | Event |
|---|---|
| 20260403 15:49 | Repository created [1] |
| 20260406 15:06 | First `LICENSE` commit, "v3: MIT license" [5] |
| 20260722 22:50 | "chore: relicense from MIT to Apache-2.0": `LICENSE` replaced, `LICENSE-MIT` and `NOTICE` added, `pyproject` set to Apache-2.0 [5] |

The commit message gives the project's reasons and legal claim: Apache adds a patent grant, a patent-retaliation
clause and inbound-contribution terms, and "MIT's sublicense right permits relicensing the combined work, so
this needs no per-contributor consent"; earlier contributions "remain available under those terms" [5]. That is
the project's position; I did not assess it. One third-party analysis still describes the project as MIT-licensed [27]; the current `LICENSE` file is Apache-2.0. Whether any licence
text existed before 20260406 is unstated by the `LICENSE` history, which starts that day [5].

## The growth flag

The first snapshot flags the repository `fast-growth`: 139,356 stars, 210 days old, 663.6 stars a day,
9.53 forks per 100 stars (20261030 19:13 UTC) [40]. The flag is a heuristic; I did not re-derive its rule.
Nothing below concludes anything about how the stars arose.

| Measure | Value (read time) |
|---|---|
| Stars, forks, watchers | 139,363; 13,291; 412 subscribers (19:29) [1]. Stars per fork 10.5; 9.54 forks per 100 stars. |
| Contributors | 353 non-anonymous accounts (19:36); the snapshot lists 374 by a method not re-derived [30][40]. The top account holds 1,224 of 2,585 listed contributions (47%); the top ten hold 1,736 (67%); 198 accounts have one contribution [30]. |
| Commits | 2,625 on `v8`; 1,297 since 20260801, of which the maintainer made 296 and the next four accounts 178, 57, 50 and 47 [32]. 709 subject lines begin with "fix" [32]. |
| Issues and pull requests | 729 open issues, 1,397 closed; 940 open PRs, 135 merged, 1,537 closed unmerged (19:31) [30]. The fix for issue 3690 appears as a commit carrying a "cherry picked from" line [23], and PR 4348 shows as closed, not merged, while its change is in the code [14][24]; I did not measure how common this is. |
| Releases | 243 GitHub releases from 20260405 to 20261027 (70, 52, 27, 28, 22, 20, 24 per month, April to October) [2]; 265 PyPI releases [33] |
| PyPI downloads | pypistats.org: 76,657 last day, 481,313 last week, 1,630,115 last month; about 9.4 million over a 180-day window, mirrors excluded (19:38). The count includes automated installs; unquantified [33]. |

Issue and PR creation per month [30]:

| Period | Issues | PRs |
|---|---|---|
| 20260403 to 20260410 | 98 | 86 |
| 20260411 to 20260430 | 208 | 194 |
| May | 225 | 209 |
| June | 210 | 234 |
| July | 398 | 371 |
| August | 403 | 479 |
| September | 275 | 428 |
| October (to 30th) | 309 | 611 |

Forks over time (the n-th fork's creation time, from the fork list sorted oldest first, 19:31) [31]:

| Fork number | Created (UTC) | Fork number | Created (UTC) |
|---|---|---|---|
| 1 | 20260405 18:03 | 6,901 | 20260624 08:08 |
| 101 | 20260406 21:21 | 8,901 | 20260723 18:52 |
| 901 | 20260408 09:45 | 10,901 | 20260902 21:32 |
| 1,901 | 20260410 22:30 | 12,901 | 20261025 13:50 |
| 3,901 | 20260429 00:15 | 13,201 | 20261029 05:25 |
| 5,901 | 20260604 13:53 | | |

Dated star counts from outside the repository (approximate dates and counts) [28][29]:

| Source and date | Stars | Forks | Implied average since the previous row |
|---|---|---|---|
| Blog, 20260408: "four days after its first commit" (about 20260407) [28] | 7,311 | 762 | |
| Augment Code article, published 20260608, updated 20260618 [29] | 63.2K | 6.5K | about 780 to 900 a day (arithmetic on the two rows) |
| Repository API, 20261030 [1] | 139,363 | 13,291 | about 530 to 570 a day |

How the launch happened, as far as sources show: the first commit, "feat: core pipeline", is dated 20260403
17:56 UTC, two hours after the repository was created [32]. The first README opens by citing Andrej Karpathy
describing a `/raw` folder of papers, tweets and screenshots that becomes opaque [32]. The first GitHub release
(tagged v1.0.0) is 20260405 21:45; the next is tagged v0.2.0, so tag numbers do not rise in order [2][32]. The
blog of 20260408 says Karpathy asked for such a tool "earlier this week" and that Graphify appeared "forty-eight
hours later"; I did not check Karpathy's original post [28]. I found no launch post, Hacker News thread or press
item in two web searches. The Trendshift badge is in the README [6].

What I could not do: GitHub's stargazer list returned HTTP 404 for this repository and for another repository
tried (20261030 19:31), so I could not sample star timestamps [35]. The evidence read supports these statements and no
more: forks, issues and pull requests were created steadily from the first week; one account holds 47% of listed
contributions; GitHub shows 135 merged of 2,612 pull requests; and the dated star counts above rise steeply
from the first week.

## Direction

I found no roadmap file in the repository tree [8]; the sources are the release notes and commits [39]. The maintainer's work since July has two
visible strands. One is correctness of the extractors and the graph: 709 of 1,297 commit subjects since
20260801 begin with "fix", the AST cache schema is at version 29 in 0.9.97, and recent notes cover
CommonMark parsing, credential redaction in rationale labels and fixes to the SystemVerilog, OCaml, COBOL, Razor and
Terraform extractors [2][32]. The other is the hosted product and its surroundings: the README
re-led with Cloud on 20261010, the CLI pointer followed on 20261009, the organisation added plugin and MCP
documentation repositories in August to October, and two new repositories, `REAgraph` and `rea`, in October [22][34]. The
project asks contributors to disclose AI assistance in a `Co-Authored-By` trailer [38]; the relicence and the
"80% fewer tokens" commits each carry such a trailer naming Claude Opus 4.8 [5][22].

### Recent changes (about 90 days)

| Date (UTC) | Change |
|---|---|
| 20260722 | Relicensed from MIT to Apache-2.0 [5] |
| 20260920 to 20261005 | Issue 3690 on missing code benchmarks; code result added to `BENCHMARKS.md` [23] |
| 20261009 | CLI prints a one-time Cloud pointer after `graphify extract` [22] |
| 20261010 | README trimmed and re-led with the "80% fewer tokens" Cloud banner [22] |
| 20261011 | `graphify benchmark` changed to count the real `query_graph` answer (PR 4348 closed unmerged, change visible in the code) [14][24] |
| 20261012 | Opt-in LLM backend selection and a switch to disable all backends [22] |
| 20261027 | v0.9.97: rationale-label credential redaction, a floor on a dependency with a published CVE, CommonMark fixes [2] |

## Sources

1. https://api.github.com/repos/Graphify-Labs/graphify: stars, forks, subscribers, issue count, licence field, dates, default branch, topics (read 20261030 19:29 UTC)
2. https://github.com/Graphify-Labs/graphify/releases (API `releases/latest` and `releases`): v0.9.97 notes, 243 releases, earliest tags and monthly counts (read 20261030 19:30 UTC)
3. https://github.com/Graphify-Labs/graphify/blob/v8/LICENSE: Apache License 2.0 text, 202 lines, appendix placeholder unfilled (read 20261030 19:29 UTC)
4. https://github.com/Graphify-Labs/graphify/blob/v8/NOTICE and https://github.com/Graphify-Labs/graphify/blob/v8/LICENSE-MIT: copyright lines and retained MIT text (read 20261030 19:29 UTC)
5. Commit `ba7f9ea9` (relicense) and commit lists for `LICENSE`, `LICENSE-MIT`, `NOTICE`, via the commits API (read 20261030 19:30 UTC)
6. https://github.com/Graphify-Labs/graphify/blob/v8/README.md: pitch, claims, install, query commands, privacy, Cloud section (read 20261030 19:29 UTC)
7. https://github.com/Graphify-Labs/graphify/blob/v8/docs/how-it-works.md: three passes, confidence rubric, 71.5x, graph format (read 20261030 19:29 UTC)
8. https://github.com/Graphify-Labs/graphify/blob/v8/ARCHITECTURE.md and the repository tree (`git/trees/v8`): pipeline modules, schema, edge direction, exporters (read 20261030 19:29 UTC)
9. https://github.com/Graphify-Labs/graphify/blob/v8/BENCHMARKS.md: harness, results, fairness rules, reproduction commands (read 20261030 19:29 UTC)
10. https://github.com/Graphify-Labs/graphify/blob/v8/graphify/serve.py: MCP tools, query scoring, output format, token budget (read 20261030 19:30 UTC)
11. https://github.com/Graphify-Labs/graphify/blob/v8/graphify/skills/claude/references/extraction-spec.md: extraction subagent prompt and schema (read 20261030 19:30 UTC)
12. https://github.com/Graphify-Labs/graphify/blob/v8/graphify/skills/claude/references/query.md: slash-command query flow and vocabulary expansion (read 20261030 19:38 UTC)
13. https://github.com/Graphify-Labs/graphify/blob/v8/graphify/always_on/claude-md.md: always-on rule text for Claude Code (read 20261030 19:38 UTC)
14. https://github.com/Graphify-Labs/graphify/blob/v8/graphify/benchmark.py: how the token ratio is computed (read 20261030 19:33 UTC)
15. https://docs.graphify.com/concepts/architecture: build stages, INFERRED meaning, storage (read 20261030 19:33 UTC)
16. https://docs.graphify.com/open-source/features/token-benchmark.md: benchmark method and caveats (read 20261030 19:34 UTC)
17. https://graphify.com/glossary/token-reduction: 71.5x as a worked example, with caveats (read 20261030 19:34 UTC)
18. https://docs.graphify.com/platform/graphify-vs-local.md: hosted versus CLI (read 20261030 19:34 UTC)
19. https://docs.graphify.com/platform/support/pricing.md: plans and prices (read 20261030 19:34 UTC)
20. https://docs.graphify.com/open-source/features/mcp-tools.md: ten MCP tools (read 20261030 19:34 UTC)
21. https://www.graphify.com: home page, hosted and open-source offers (read 20261030 19:33 UTC)
22. Commits to `README.md` (302) via the commits API, including `01d23d06` (80% headline, 20261010 13:34) and `6efd06c5` (YC badge), and the Cloud-pointer commit of 20261009 (read 20261030 19:35 UTC)
23. https://github.com/Graphify-Labs/graphify/issues/3690 and commit `2ce4a207`: benchmark critique and fix (read 20261030 19:35 UTC)
24. https://github.com/Graphify-Labs/graphify/issues/4749 and https://github.com/Graphify-Labs/graphify/pull/4348: the "Token 80% reduction" issue; the benchmark-counting change (read 20261030 19:35 UTC)
25. https://github.com/Graphify-Labs/graphify/tree/v8/worked/karpathy-repos (README, review, report, graph.json): the 71.5x worked example (read 20261030 19:38 UTC)
26. https://hackernoon.com/i-tested-graphify-on-a-real-python-repo-heres-what-happened: third-party test, 20261021 (read 20261030 19:35 UTC; key numbers confirmed in the page source)
27. https://github.com/az9713/graphify-on-graphify: third-party analysis, README figures confirmed (read 20261030 19:35 UTC)
28. https://themenonlab.blog/blog/graphify-knowledge-graph-claude-code-karpathy: blog of 20260408, Karpathy link, 7,311 stars (read 20261030 19:37 UTC)
29. https://www.augmentcode.com/learn/graphify-63k-stars-knowledge-graphs: article of 20260608, 63.2K stars (read 20261030 19:37 UTC)
30. Contributors, issue and PR counts by search API, `TEAM_MEMBERS`, `CODEOWNERS`, organisation API (read 20261030 19:31 and 19:36 UTC)
31. Fork list sorted oldest first, sampled pages 1 to 133 (read 20261030 19:31 UTC)
32. Commits API on `v8`: oldest commits, the window since 20260801 with 1,297 commits, the first README and release notes of v0.2.0 and v1.0.0 (read 20261030 19:32 to 19:34 UTC)
33. https://pypi.org/pypi/graphifyy/json and https://pypistats.org/api/packages/graphifyy/recent: releases, licence expression, downloads (read 20261030 19:38 UTC)
34. Organisation repository list and branch list, and a request to `safishamsi/graphify` (read 20261030 19:31 and 19:37 UTC)
35. Stargazer endpoint, returned HTTP 404 for this repository and for another repository tried (read 20261030 19:31 UTC)
36. https://github.com/Graphify-Labs/graphify/blob/v8/pyproject.toml: dependencies, extras, scripts (read 20261030 19:37 UTC)
37. https://github.com/Graphify-Labs/graphify/blob/v8/graphify/llm.py: direct-API extraction route (read 20261030 19:37 UTC)
38. https://github.com/Graphify-Labs/graphify/blob/v8/CONTRIBUTING.md: AI-disclosure rule (read 20261030 19:36 UTC)
39. https://github.com/Graphify-Labs/graphify/blob/v8/CHANGELOG.md: release notes, Cloud-pointer entry (read 20261030 19:33 and 19:39 UTC)
40. Local: [`repos.tsv`](../landscape/20261030_1913-github/repos.tsv) (row read 20261030 19:28 UTC); [`llm-era/README.md`](../llm-era/README.md); [`papers-benchmarks/README.md`](../papers-benchmarks/README.md) (no Graphify entry)
41. https://www.ycombinator.com/companies/graphify-labs: page title "Graphify Labs: On-device Knowledge Graph engine for Enterprise Software | Y Combinator"; no further text retrieved (read 20261030 19:37 UTC)
