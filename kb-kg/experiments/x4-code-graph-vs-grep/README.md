# X4: does a code graph help an agent beyond saving tokens?

**Status: groundwork. The questions and their answers are frozen; no agent and no code-graph tool has been run on
them.** This directory holds the part of [X4](../README.md#x4-does-a-code-graph-beat-grep-beyond-saving-tokens-pilot) that
must be fixed before anything is measured, so the comparison cannot be bent toward either side.

## What is frozen

| | Flask | Gin |
|---|---|---|
| Repository | [`pallets/flask`](https://github.com/pallets/flask), Python | [`gin-gonic/gin`](https://github.com/gin-gonic/gin), Go |
| Pinned commit | `49943b5a94413a530761350f04e896f76e8d620e` (committed 20261030 15:05 UTC) | `0f09c3a9b4626d9fe9979cf4d0521d6ae32ab646` (committed 20261010 04:20 UTC) |
| Licence (from the `LICENSE` file at the commit) | BSD-3-Clause | MIT |
| Questions | [`flask/questions.yaml`](flask/questions.yaml), 10 | [`gin/questions.yaml`](gin/questions.yaml), 10 |
| How the answers were derived | [`flask/derivation.md`](flask/derivation.md) | [`gin/derivation.md`](gin/derivation.md) |
| Pilot (first three in file order) | q01 a definition, q02 a callers question with 4 callers, q03 a callers question with 12 | gin-01 a definition, gin-02 with 4 callers, gin-03 with 11 |

**Why these two.** Chosen by me on 20261102 before any run, by a stated rule: permissively licensed, not archived, pushed
in the last 90 days, mid-sized, different languages (a dynamic one and a static one), and not among the surveyed
projects. Candidates read that day: Flask, Requests, Cobra, Hono, got and Gin. Cobra fails the activity rule (last push
20260711). The owner can veto the choice when the pilot is approved.

**The pilot is chosen by position, never by result.** Questions 1 to 3 in file order, with a fixed shape
(definition, few callers, more callers), written before any answer was derived.

## How the answers were derived, and what I checked myself

Each answer was derived by independent methods that had to agree: ripgrep and reading the code; a program-analysis
method (Python's `ast` for Flask; `go/types` and `gopls` for Gin); and a third check on a second fresh clone for the
pilot. No code-graph or knowledge-graph tool was used, because one such tool is what X4 later tests. The derivations are
in the two `derivation.md` files, including the candidates dropped as ambiguous and every disagreement and how it was
settled.

**Re-derived by me, 20261102 10:44 to 10:50 UTC**, on fresh clones at the pins, with plain `grep` and a lookup of the nearest
enclosing definition that shares no code with the agents' tools: Gin gin-01, gin-02, gin-03, gin-07 and gin-09; Flask
q01, q02, q03 and q10. Every one equals its key. That is nine of twenty answers, including all six pilot answers. The
other eleven rest on the agents' own cross-checks.

## What the frozen files do not settle

- **They test static structure only.** Dynamic dispatch, reflection, callbacks and generated code are outside the keys;
  Gin's gin-07 states the one dispatch rule it needs (calls through an interface are excluded by the question text; a
  tool that follows interface dispatch will list two more).
- **Independence is partial.** One agent ran all the methods for each repository, and an early listing from one method
  informed which targets were chosen. Methods 2 and 3 for Gin both rest on Go's type checker.
- **The question wording has not been tested on any agent.** Neither has the scoring: no scoring program exists yet,
  and the plan's check that a perfect answerer scores 100% and a random one lands near chance is still to do. It belongs
  to the step that runs the pilot.
- **The two files lay out answers differently** (Flask keeps a callers answer as `{count, callers}`; Gin keeps a list and
  an `answer_count`; the partial-credit rules differ by question and are written in each question's `scoring` field).
  The top-level keys were made equal (`pinned_commit`, `pilot_question_ids`). A scorer must read each question by its own
  `scoring` text, or normalise first.
- **The helper programs live in a scratch directory and are not committed** (a 271-line Go program and some Python).
  Each answer can be reproduced with stock tools, and the commands are at the end of each `derivation.md`; the helpers'
  SHA-256 values are in the Gin file.
- **A shared name does not make a question easy or hard.** Five of the ten Gin questions and six of the ten Flask
  questions cannot be answered by a single grep, which is deliberate.
