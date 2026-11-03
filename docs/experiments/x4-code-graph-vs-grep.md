---
type: page
order: 5
updated: 20261102 20:13 UTC
---

# X4: a code graph against grep

This page answers one question: does a [code graph](../index/code-graph.md) help a coding [agent](../index/agent.md) answer code questions more correctly, and not only with fewer tokens? It describes the design of the test, how its twenty questions and answers were fixed before anything was run, and what is still missing. **Nothing has been run on an agent or on a code-graph tool: this is groundwork, and there is no result yet** [21][26].

## The question

The Codebase-Memory paper (arXiv, 20260328) scored a graph tool against a file-exploration agent. It reports 83% answer quality for the graph tool against 92% for the explorer, at ten times fewer tokens and 2.1 times fewer tool calls, over 31 repositories [1]. Its authors are the developers of the tool it evaluates, so the result is first-party [1]. The open point, as the archive states it, is whether an agent solves coding questions better, not only cheaper, with a graph than with grep and glob [26][28]. This test is built to answer that for one narrow kind of question.

## Method

Two public repositories, ten questions each. The same agent runs in two conditions: with grep and glob only, and with one code-graph tool added through the [Model Context Protocol](../index/model-context-protocol.md). The planned tool is [codebase-memory-mcp](../projects/codebase-memory-mcp.md), MIT-licensed per its `LICENSE` file [8][26]; the repository is not archived and was last pushed 20261102 [9]. The run records tokens from the provider's usage fields, the number of tool calls, and correctness against answers derived by hand before any run [26].

Every question has one checkable answer: where something is defined, or which functions call it. The Flask question file states that each question text is given to the agent verbatim and that its `answer`, `scoring`, `why_not_trivial`, `target` and `scope_file` fields are never shown to the agent [24]. The Gin file states neither rule, so for Gin both are **unstated** [25].

## The repositories

| | Flask | Gin |
|---|---|---|
| Repository | [pallets/flask](https://github.com/pallets/flask), Python | [gin-gonic/gin](https://github.com/gin-gonic/gin), Go |
| Pinned commit | `49943b5a94413a530761350f04e896f76e8d620e`, committed 20261030 15:05 UTC [2] | `0f09c3a9b4626d9fe9979cf4d0521d6ae32ab646`, committed 20261010 04:20 UTC [3] |
| Licence (from the `LICENSE` file at the pin) | BSD-3-Clause [4][6] | MIT [5][7] |
| Scope of the questions | `src/flask/`, 24 Python files, 9,566 lines [22] | 59 non-test Go files in 7 packages [23] |

*Why these two.* The archive says they were chosen on 20261102 before any run, by a stated rule: permissively licensed, not archived, pushed in the last 90 days, mid-sized, one dynamic and one static language, and not among the projects surveyed in the archive [21]. Cobra was read and fails the activity rule: its last push is 20260711 [21][10]. Requests, Hono and got were also read; the archive does not say why they were set aside, and a re-read on 20261102 shows them active (last pushes 20261102, 20261101 and 20261030) and permissively licensed by the API's detected field [11][12][13], so the reason is **unstated**. The owner can veto the choice when the pilot is approved [21].

## The questions

Six are definition questions ("in which file and at which line is X defined"), fourteen are callers questions ("which functions directly call X"). Four callers questions are limited to the callers defined in one file: q09, q10, gin-06 and gin-10. A callers answer names each caller as `path::func` or `path::Class.method`. In Flask, a call inside a nested function counts for the outermost enclosing function; in Gin, a call inside a function literal counts for the enclosing named function [24][25].

| Question | Kind | Target | Key |
|---|---|---|---|
| q01 (pilot) | definition | `handle_url_build_error` | `src/flask/sansio/app.py:982` |
| q02 (pilot) | callers | `get_debug_flag` | 4 callers |
| q03 (pilot) | callers | `Flask.ensure_sync` | 12 callers |
| q04 | definition | the class behind `from flask import Blueprint` | `src/flask/blueprints.py:18` |
| q05 | callers | `send_from_directory`, defined in `helpers.py` | 2 callers |
| q06 | definition | `add_url_rule` found from a `Flask` instance, along the inheritance chain | `src/flask/sansio/app.py:606` (605 accepted) |
| q07 | callers | `Blueprint.register` of the sansio class | 2 callers |
| q08 | callers | `load_dotenv`, defined in `cli.py` | 2 callers |
| q09 | callers, only those in `cli.py` | `ScriptInfo.load_app` | 4 callers |
| q10 | callers, only those in `app.py` | `_CollectErrors.raise_any` | 2 callers |
| gin-01 (pilot) | definition | `Engine.handleHTTPRequest` | `gin.go:719` |
| gin-02 (pilot) | callers | `Context.hasRequestContext` | 4 callers |
| gin-03 (pilot) | callers | `RouterGroup.handle` | 11 callers |
| gin-04 | callers | `Context.Get` (a common name) | 4 callers |
| gin-05 | definition | `Engine.Handler` (a second `Handler` exists on `Context`) | `gin.go:257` |
| gin-06 | callers, only those in `binding/form_mapping.go` | `setWithProperType` | 3 callers (one is recursive) |
| gin-07 | callers | `responseWriter.WriteHeaderNow`, concrete receiver only | 6 callers |
| gin-08 | definition | `node.getValue` | `tree.go:418` (413 to 417, the doc comment, earns 0.5) |
| gin-09 | callers | `RouterGroup.GET` | 3 callers |
| gin-10 | callers, only those in `context.go` | `Context.Error` | 2 callers |

Source for the table: the two question files [24][25]. All twenty keys were read again against the pinned source for this page, on 20261102 between 20:09 and 20:11 UTC; the section "Checks after the freeze" says how [19][20]. The archive states that a single grep cannot answer six of the ten Flask questions and five of the ten Gin questions, and that this is deliberate [21]. *Reading:* that choice makes the set favour a tool that resolves names and types, and a reader should weigh a result with that in mind.

## How the answers were derived and frozen

Each answer was derived by methods that had to agree, and no code-graph or [knowledge-graph](../index/knowledge-graph.md) tool was used, because one such tool is what the test later measures [21][22][23].

| | Flask | Gin |
|---|---|---|
| Method 1 | ripgrep and reading; a text-only walk up the indentation finds the enclosing function | ripgrep and reading, with one fixed textual rule per question |
| Method 2 | Python's `ast` module, resolving imports, `self`, annotations and local assignments | a 271-line Go program on `go/types` |
| Method 3 | not used for the ten; a second fresh clone for the three pilot questions | `gopls references` and `gopls definition` |
| Disagreements | none between methods 1 and 2 | one fault in the author's own rule (a stray character gave zero callers, caught because a visible caller existed), and one real disagreement, gin-07, settled by reading |

Sources: [22][23]. The gin-07 case shows what the key encodes. `gopls` reports 8 callers of `responseWriter.WriteHeaderNow`, because it counts two calls made through an interface. The question text excludes interface calls, so the key is 6; a tool that follows interface dispatch will list two extra names, and the scoring rule says in advance that this is not credited [23].

The questions and keys were written down before any agent or tool was run (Flask file frozen 20261102 10:43 UTC; Gin derived 20261102 10:40 UTC) [24][25]. The files also fix the scoring rules ahead of time:

| | Flask | Gin |
|---|---|---|
| Callers | exact set match scores 1; partial credit is F1 | exact set match scores 1; otherwise the Jaccard index, recorded as partial credit and never counted as correct |
| Definition | exact path and accepted line scores 1; right path, wrong line 0.5 | exact path and line scores 1 (gin-08 also has a 0.5 window); anything else 0 |

Sources: [24][25]. The two files differ in layout and in the partial-credit measure, so a scorer must read each question's own `scoring` field or normalise first [21].

## Checks after the freeze

The archive records that the owner's assistant re-derived nine of the twenty answers on 20261102 between 10:44 and 10:50 UTC, on fresh clones at the pins, with plain `grep` and a nearest-enclosing-definition lookup that shares no code with the agents' tools: gin-01, gin-02, gin-03, gin-07, gin-09, and q01, q02, q03, q10. Every one equalled its key. That covers all six pilot answers. The other eleven rest on the original cross-checks [21].

For this page, the pinned source of both repositories was downloaded again on 20261102 at 20:09 UTC and every key was compared with it [19][20]:

- **Definition keys (six).** `def handle_url_build_error(` is on line 982 of `src/flask/sansio/app.py` (q01). `class Blueprint(SansioBlueprint):` is on line 18 of `src/flask/blueprints.py` (q04). `@setupmethod` is on line 605 and `def add_url_rule(` on line 606 of `src/flask/sansio/app.py` (q06). `func (engine *Engine) handleHTTPRequest(c *Context) {` is on line 719 and `func (engine *Engine) Handler() http.Handler {` on line 257 of `gin.go` (gin-01, gin-05). `func (n *node) getValue(` is on line 418 of `tree.go`, with its doc comment on lines 413 to 417 (gin-08). The lines of q01, q04, q06, gin-01 and gin-05 were also read through the GitHub contents API at 19:38 UTC [14][15][18].
- **Flask callers keys (seven).** A short Python program using the `ast` module found every call to the name, mapped it to the outermost enclosing function, and the sets equalled the keys for q03 (12 callers), q05, q07, q08, q09 and q10. Name matching also returned callers outside a key, which the key leaves out by its scope or its definition rule: a call in `ctx.py` (q10 is limited to `app.py`), the self-call in `helpers.py` (q05) and a `register` of another class in `json/tag.py` (q07, settled by reading). For q02 the four call lines are `app.py:723`, `cli.py:369`, `cli.py:972` and `sansio/app.py:493`, in `Flask.run`, `ScriptInfo.load_app`, `run_command` and `App.make_config`; a search of all of `src/flask/` found no fifth [16][17][14][19].
- **Gin callers keys (seven).** A text search found the call lines, and each line was mapped to the nearest preceding `func` line: gin-02 four lines in four methods, gin-03 eleven lines in eleven `RouterGroup` methods, gin-04 four, gin-06 three (one inside `setWithProperType` itself), gin-07 six concrete calls plus two through `c.Writer` that the key leaves out, gin-09 three, gin-10 two. The sets equalled the keys [20].

*Reading:* this second pass matches names and reads the enclosing function, which is weaker than the type-resolving methods in the archive. In particular, it does not resolve receiver types, so the gin-07 split between concrete and interface calls and the q06 inheritance chain rest on the archive's derivations [22][23], not on this check. It agrees with all twenty keys.

## The pilot

The pilot is chosen by position, never by result: the first three questions in each file, with a fixed shape written before any answer was derived: a definition, a callers question with at most five callers, and one with six to fifteen [21][24][25].

| Repository | Definition | Few callers | More callers |
|---|---|---|---|
| Flask | q01 | q02, 4 callers | q03, 12 callers |
| Gin | gin-01 | gin-02, 4 callers | gin-03, 11 callers |

The archive describes the pilot as "3 questions in 2 conditions" and as "6 agent runs" [26]. Three questions on each of two repositories in two conditions would be 12 runs (my arithmetic), so the archive's count and its pilot table do not agree, and which is meant is **unstated**. The archive also says agent runs vary from run to run, so a pilot measures cost and feasibility, not a result [26].

## What is missing

| Gap | Detail | Source |
|---|---|---|
| No scoring program | The rules are written and the key files load as YAML, but no program applies them. The check that a perfect answerer scores 100% and a random one lands near chance is still to do. | [21][22][26] |
| Question wording | Not tried on any agent, so it may be misread. | [21][22] |
| Static structure only | Dynamic dispatch, reflection, callbacks and generated code are outside the keys. | [21][22][23] |
| Partial independence | One agent ran all methods for each repository, and an early listing informed which targets were chosen. Methods 2 and 3 for Gin both rest on Go's type checker. | [21][23] |
| Helper programs | They live in a scratch directory and are not committed. Each answer can be reproduced with stock tools, and the commands are in the derivation pages. | [21][22][23] |
| Model, agent client, cap | The agent model and its tier, the agent client and the cap on cost are **unstated**; the model runs on the owner's key and the cap is the owner's to set. | [26][27] |
| Tool version and settings | Which version and configuration of the code-graph tool will run is **unstated**. | [26] |

*Reading:* the questions test lookup (definitions and direct callers) with a single correct answer. A result would say how well each condition finds those facts. It would not show that an agent fixes bugs or writes changes better, which is the wider sense of "helps beyond saving tokens". The archive itself calls the test "a small, owner-run test, not an independent evaluation" [26].

## Status

As of the archive pages read on 20261102 20:08 UTC [21][26][27]:

- The 20 questions and keys are frozen. 9 of the 20 keys were re-derived independently by the archive's method, and all 20 were read again against the pinned source for this page by name matching.
- No agent and no code-graph tool has run on them.
- The pilot needs the owner's yes with model, provider and cap before any paid step, under decision D-25 and the gate rule D-14 [26][27].
- The other experiments are on the [chapter page](README.md). The long evidence is in the archive: [overview](../../kb-kg/experiments/x4-code-graph-vs-grep/README.md), [Flask derivation](../../kb-kg/experiments/x4-code-graph-vs-grep/flask/derivation.md) and [Gin derivation](../../kb-kg/experiments/x4-code-graph-vs-grep/gin/derivation.md).

## Sources

Items 21 to 28 are archive pages (repository paths, which the site maps). They record the work of the archive's own sessions, so they have no earlier URL; the facts in them that rest on a public page are re-read in items 1 to 20.

1. https://arxiv.org/abs/2603.27277 : "Codebase-Memory: Tree-Sitter-Based Knowledge Graphs for LLM Code Exploration via MCP", Vogel and four co-authors, 20260328; abstract: 83% answer quality against 92% for a file-exploration agent, ten times fewer tokens, 2.1 times fewer tool calls, 31 repositories; "an open-source system" presented by its authors, so first-party (read 20261102 19:37 UTC)
2. https://api.github.com/repos/pallets/flask/commits/49943b5a94413a530761350f04e896f76e8d620e : the pinned Flask commit exists; committer date 2026-10-30T15:05:20Z (read 20261102 20:11 UTC)
3. https://api.github.com/repos/gin-gonic/gin/commits/0f09c3a9b4626d9fe9979cf4d0521d6ae32ab646 : the pinned Gin commit exists; committer date 2026-10-10T04:20:35Z (read 20261102 20:11 UTC)
4. https://api.github.com/repos/pallets/flask : not archived; licence detected as BSD-3-Clause; language Python. The licence in the table comes from the `LICENSE` file (source 6), not from this field (read 20261102 20:11 UTC)
5. https://api.github.com/repos/gin-gonic/gin : not archived; licence detected as MIT; language Go. The licence in the table comes from the `LICENSE` file (source 7), not from this field (read 20261102 20:11 UTC)
6. https://github.com/pallets/flask/blob/49943b5a94413a530761350f04e896f76e8d620e/LICENSE.txt : three-condition BSD text headed "Copyright 2010 Pallets" (read 20261102 19:37 UTC)
7. https://github.com/gin-gonic/gin/blob/0f09c3a9b4626d9fe9979cf4d0521d6ae32ab646/LICENSE : MIT text, "Copyright (c) 2014-present Manuel Martínez-Almeida"; SHA-256 `b104efb2c7700691650f27034e8541c5ae0ed9af54d884287f19a7467ca2fe7f`, equal to the value in the archive (read 20261102 19:37 UTC)
8. https://github.com/DeusData/codebase-memory-mcp/blob/main/LICENSE : MIT text, copyright 2025 DeusData (read 20261102 19:37 UTC)
9. https://api.github.com/repos/DeusData/codebase-memory-mcp : not archived; last push 2026-11-02T17:25:23Z (read 20261102 20:11 UTC)
10. https://api.github.com/repos/spf13/cobra : not archived; last push 2026-07-11T00:43:07Z; licence detected as Apache-2.0 (read 20261102 20:11 UTC)
11. https://api.github.com/repos/psf/requests : not archived; last push 2026-11-02T16:55:12Z; licence detected as Apache-2.0 (read 20261102 20:11 UTC)
12. https://api.github.com/repos/honojs/hono : not archived; last push 2026-11-01T02:52:19Z; licence detected as MIT (read 20261102 20:11 UTC)
13. https://api.github.com/repos/sindresorhus/got : not archived; last push 2026-10-30T08:46:04Z; licence detected as MIT (read 20261102 20:11 UTC)
14. https://api.github.com/repos/pallets/flask/contents/src/flask/sansio/app.py?ref=49943b5a94413a530761350f04e896f76e8d620e : lines 982 (`handle_url_build_error`), 605 and 606 (`add_url_rule`), 493 (`get_debug_flag()` call) (read 20261102 19:38 UTC)
15. https://api.github.com/repos/pallets/flask/contents/src/flask/blueprints.py?ref=49943b5a94413a530761350f04e896f76e8d620e : line 18 (`class Blueprint`) (read 20261102 19:38 UTC)
16. https://api.github.com/repos/pallets/flask/contents/src/flask/cli.py?ref=49943b5a94413a530761350f04e896f76e8d620e : lines 369 and 972 (`get_debug_flag()` calls) (read 20261102 19:38 UTC)
17. https://api.github.com/repos/pallets/flask/contents/src/flask/app.py?ref=49943b5a94413a530761350f04e896f76e8d620e : line 723 (`get_debug_flag()` call) (read 20261102 19:38 UTC)
18. https://api.github.com/repos/gin-gonic/gin/contents/gin.go?ref=0f09c3a9b4626d9fe9979cf4d0521d6ae32ab646 : lines 719 (`handleHTTPRequest`) and 257 (`Handler`) (read 20261102 19:38 UTC)
19. https://codeload.github.com/pallets/flask/tar.gz/49943b5a94413a530761350f04e896f76e8d620e : the whole pinned Flask tree, searched for all ten keys (read 20261102 20:09 UTC)
20. https://codeload.github.com/gin-gonic/gin/tar.gz/0f09c3a9b4626d9fe9979cf4d0521d6ae32ab646 : the whole pinned Gin tree, searched for all ten keys (read 20261102 20:09 UTC)
21. kb-kg/experiments/x4-code-graph-vs-grep/README.md : frozen items, selection rule, derivation methods, nine re-derived answers, limits (archive page written 20261102; its own read times are 20261102 10:27 to 10:50 UTC; read here 20261102 20:08 UTC)
22. kb-kg/experiments/x4-code-graph-vs-grep/flask/derivation.md : Flask pin, scope, methods 1 and 2, per-question results, dropped candidates, what the key does not cover (archive page; its own times are 20261102 10:27 to 10:44 UTC; read here 20261102 20:08 UTC)
23. kb-kg/experiments/x4-code-graph-vs-grep/gin/derivation.md : Gin pin, three methods, per-question results, the gin-07 disagreement, limits (archive page; its own times are 20261102 10:27 to 10:42 UTC; read here 20261102 20:08 UTC)
24. kb-kg/experiments/x4-code-graph-vs-grep/flask/questions.yaml : the ten Flask questions, keys and scoring rules, the header rule that `answer`, `scoring`, `why_not_trivial`, `target` and `scope_file` are never shown to an agent, frozen 20261102 10:43 UTC (read 20261102 20:08 UTC)
25. kb-kg/experiments/x4-code-graph-vs-grep/gin/questions.yaml : the ten Gin questions, keys and scoring rules, derived 20261102 10:40 UTC; its header has no rule on what is shown to an agent (read 20261102 20:08 UTC)
26. kb-kg/experiments/README.md : the X4 entry (question, method, "6 agent runs", cost unknown) and the Step 0 status (no scoring program, wording untried) (archive page; read here 20261102 20:08 UTC, on the newest main)
27. DECISIONS.md : row D-25, Step 0 built, what is not done, the owner's yes still needed for the first paid step (archive page; read here 20261102 20:08 UTC, on the newest main)
28. kb-kg/directions/code-knowledge-graphs.md : the survey of code-graph projects and the open question (archive page; read 20261102 19:36 UTC, unchanged on the newest main)
