---
slug: tigerless-agent-memory
repo: tigerless-labs/agent-memory
tier: deep
category: markdown-kb
snapshot: 20261030 19:29 UTC
---

# agent-memory (Tigerless Labs)

Reading times: repository metadata, `LICENSE`, README and `CLAUDE.md` at 20261030 19:29 UTC; source files and
design documents between 19:29 and 19:30 UTC; contributors, commits, issues and CI at 19:31 to 19:36 UTC;
historical commit trees and the experiment ledger at 19:32 to 19:33 UTC. Star and fork counts were read again at
19:34 UTC and had not changed. Each source below carries its own time.

| | |
|---|---|
| Repository | https://github.com/tigerless-labs/agent-memory |
| Licence | MIT, from the `LICENSE` file ("Copyright (c) 2026 Tigerless Labs") [3]. GitHub's API reports MIT [1]. The README ends with a link to `LICENSE` and its badges name no licence, so nothing disagrees [4]. The first commit trees I listed (20260903, 20260904) show no `LICENSE` entry; "Add the MIT license" was committed 20260908 19:41 UTC and merged by PR #25 on 20260909 13:11 UTC [18][20]. |
| Language | Python 3.12 or newer. Six packages in a uv workspace: `core`, `cli`, `mcp`, `adapters`, `executor`, `harness`. The core declares no runtime dependencies [7][8]. |
| Stars, forks | 4,381 and 199 (20261030 19:29 UTC); 96 watchers [1] |
| Created, last push | 20260901 21:52 UTC, 20261030 14:02 UTC [1] |
| Latest release | none: no GitHub release and no tag [2]. The version string in `pyproject.toml` and in the MCP server is 0.1.0 [7][14]. The README says "There is no release on PyPI yet" [4]. |
| Status | active (pushed 0 days before the snapshot); not archived [1][24]. No snapshot flag is set; see "Star growth" below. |
| Paper, docs | no paper. README, `CLAUDE.md` (the invariants), seven design documents and fifteen plans under `docs/` [4][5][8]. The README points to `docs/experiments.md` and `experiments/`, which are not in the current tree; see "Evidence" [4][8]. |

The landscape snapshot files this repository under `agent-memory` (rank 27 in that category's ranked table) [24];
this entry files it under `markdown-kb` because its own description puts plain Markdown first [1].

## What it is

agent-memory is a long-term memory runtime for AI agents. Its description reads "plain Markdown as the source of
truth, local ranked retrieval, and an independent sleep-time Manage layer", and says Claude Code and Codex share
one store and that no API key is needed [1]. A memory is one Markdown file with YAML-style front matter; a SQLite
index beside the files is a cache that can be deleted and rebuilt [4]. The project is about two months old: first
commit 20260901 21:52 UTC [17]. It places itself between two kinds of agent memory: a "retrieval engine"
(embeddings, graph, ranking) and a "filesystem" the agent reads directly, and says it combines the two in one
store [4]. The [LLM-era timeline](../llm-era/README.md) describes the period from 20260728 as one in which
"Markdown-first memory projects multiply".

## How it works

### 1. What the Markdown files hold, and who writes them

**The store.** A directory (default `~/agent-memory-store`, or `AGENT_MEMORY_STORE`) holds [4]:

| Path | Role |
|---|---|
| `MEMORY.md` | root index, one line per memory; the only text injected at session start |
| `config.toml` | every tunable; an unknown knob is refused at load |
| `schemas/` | one TOML file per memory type |
| `<type>/<group>/<name>.md` | the memories, placed by the schema |
| `archive/provenance/`, `archive/sessions/` | append-only evidence and full copies of session traces |
| `dream-reports/` | one Markdown report per sleep |
| `.index/`, `.state/` | rebuildable index (hash manifest, FTS5, access log); runtime state (watermark, locks) |

**What one file holds.** Front matter carries `name`, a one-sentence `abstract` (at most 240 characters by
default), `type`, `created`, `updated`, `valid_from`, `invalid_at`, `superseded_by`, `weight`, `author`, `links`,
`provenance` and the type's own fields; the body is free Markdown [4][11][13]. Nine factory types are written to
`schemas/` on first use: `profile`, `preference`, `entity`, `event`, `decision`, `procedure`, `fact`,
`experience`, `reference` [13]. A schema names the key fields that give identity (same key, same file), the
field that names the sub-directory, and a write mode (`upsert`, or `add_only` for `event`) [13]. One file is the
invalidation atom: it is active or it has an `invalid_at`; replaced and deleted files stay on disk [4][5].

**Who writes.** Four writers, all through one validated write path (stated as Invariant 2) [5]:

| Writer | How | Source |
|---|---|---|
| A reasoner at conversation boundaries | Hooks copy the session trace into `archive/sessions/`. A detached process then runs a "distillation": a reasoner reads a batch of the conversation and, with a toolkit of `recall`, `read` and `submit_operations`, proposes memory operations. The core validates and writes them. | [4][15][16] |
| The working agent | `mem record`, `correct`, `supersede`, `merge`, `delete`, or the equivalent MCP tools. The skill tells the agent to write directly "only for what a boundary would miss" | [4][6][14] |
| The sleep-time Manage pass | rewrites weights and dates in front matter, adds links, moves files between group directories, merges or supersedes duplicates | [12] |
| The human | not a required writer. The files are plain Markdown, so the user can edit them: a file that fails validation after an outside edit leaves the retrieval projection and stays intact on disk. The human confirms proposals (`mem decide`) and runs the physical removal command (`mem gc`). | [4][9][12] |

So the content is mostly written by a model through the host's CLI, not by the human. Whether users edit memories
by hand in practice is **unstated**.

### 2. Retrieval and ranking

Recall is deterministic and has no model call or network access in its default configuration [4][11].

1. **Eligibility first.** By default only files without `invalid_at` are searched. `--as-of <date>` also searches
   the history surface and keeps files whose validity interval contains that date [11].
2. **Lexical match.** The query is cut into ASCII word tokens and joined with OR; SQLite FTS5 returns BM25 scores
   over chunks of each memory's abstract and body. An abstract match is weighted 2.0 and a body match 1.0. The
   candidate pool is the result limit times ten; the default limit is 8 [11].
3. **Optional dense match.** With `vector_enabled = true` (default false), the optional `fastembed` extra embeds
   chunks with `BAAI/bge-small-en-v1.5` by default. The vectors are stored in SQLite and compared by brute-force
   cosine in Python. The BM25 and vector lists are fused by reciprocal-rank fusion with k = 60 [7][11]. The first
   use may download the model; `AGENT_MEMORY_OFFLINE=1` loads from the local cache only [4].
4. **Score.** `relevance x weight x recency`. Weight comes from front matter (initial 1.0, floor 0.05, ceiling
   5.0). Recency halves every 180 days and never drops below 0.25 [11].
5. **Output.** An L0 list: one-line abstract, path, anchor, score. The agent then opens a hit at a chosen depth
   (`read --level abstract`, `outline` or full), or calls `context`, which opens the top four entries in full, or
   `trace`, which opens the raw messages a memory cites [4][11]. The raw sessions are not searched [4].

An optional `cjk` extra segments Chinese text with `jieba` before indexing [4][11].

**Three read tracks**, in the project's words: a `MEMORY.md` injection at session start (an 8,192-byte budget, at
most 120 lines, active memories with weight of at least 0.75, heaviest first); recall; and the directory tree
read with `ls` and `grep` [4][11].

**The graph.** The README says relations "live as links inside the memories" and that `links` "carry the graph
without a graph database" [4]. In the code, links are a front-matter list that is validated at write time
(distinct, active, same store) and used when memories are merged. Manage adds a link between two memories that
were returned together by at least two recall events [12][13]. `recall.py`, `context.py` and the link handling in
`store.py` contain no step that follows links at query time [11][13]. In the code I read, then, the graph is
metadata, not a retrieval path. Other modules were not searched exhaustively.

**Network and keys.** Default recall needs neither. The vector extra needs a network once to fetch the model
unless the cache is filled. The write and sleep steps need a model; see "Cost and operating profile" [4][16].

### 3. The agent interface

| Surface | What it is | Source |
|---|---|---|
| CLI `mem` | the full surface: `record`, `recall`, `context`, `read`, `trace`, `correct`, `supersede`, `merge`, `delete`, `feedback`, `rebuild`, `inspect`, `export`, `import`, `sleep`, `proposals`, `decide`, `gc`, `cron`, `setup`, `doctor` | [12] |
| `mem-mcp` | a hand-written JSON-RPC stdio server (protocol version string "2025-06-18", server version 0.1.0) with nine tools: `memory_recall`, `memory_read`, `memory_trace`, `memory_record`, `memory_correct`, `memory_supersede`, `memory_merge`, `memory_delete`, `memory_feedback`. `context`, `sleep` and the proposal ledger have no MCP tool. It is installed only if `--mcp` is passed to setup. | [4][14] |
| `mem-hook` | lifecycle hooks: `SessionStart` injects `MEMORY.md`; `Stop` and `SessionEnd` capture and trigger distillation; `PreCompact` evicts. Codex has no `SessionEnd` mapping. A hook always exits 0 and logs trouble to the store. | [15] |
| Skill | `SKILL.md`, installed by setup, tells the agent when to call `mem context` and how to write | [6][15] |

`mem setup --host claude-code | codex | muse-code` merges hooks into the host's settings file, installs the skill,
runs a live preflight and prints `status: READY` only if the check passes [4][15]. It is a configuration
installer, not a packaged plugin. Hermes is a reasoner host and an interoperability-test host, not a `setup`
target [15][16]. One open issue asks for opencode support; it has no comments [18].

### 4. Consolidation and forgetting

The README calls this the "Manage layer" and the project's `CLAUDE.md` calls it the "wedge" [4][5]. A sleep runs
in order [12]:

| Step | What it does |
|---|---|
| Deterministic ("T0") | normalise dates; settle weights; add co-occurrence links; supersede exact duplicates (identical abstract, body, type, fields, author, links, provenance); merge directory names that differ only in spelling; cluster directories that hold five or more files sharing two or more words |
| Draft proposals | merge or supersede when abstract word overlap (Jaccard) is at least 0.75; split a file with three or more `##` sections cited from two or more sessions; abstract review for abstracts under three words or over 240 characters; delete for a memory with no recorded access and weight at the floor |
| Judged ("T1") | a reasoner can accept or reject open proposals, and only those; any reply that does not parse as a verdict on an open proposal is discarded. Accepted verdicts are applied through the normal write path, with a source-hash check, up to caps per sleep: 3 merges, 5 supersedes, 2 splits, 3 deletes |
| Record | a Markdown dream report; one git commit per sleep if the store is inside a git work tree and `git_commit` is on |

**Forgetting is by value, in three layers.** (a) Ranking: weight and the 180-day recency decay lower a memory's
score without removing it [11]. (b) Weight: each new read since the last sleep adds 0.5 (counted up to 3 per
sleep); a memory idle for 30 days loses 0.1 per sleep [11][12]. Below 0.75 it drops out of the injected
`MEMORY.md` [11]. (c) End of validity: a "delete" ends the memory's validity and keeps the file for `--as-of`
queries; only `mem gc`, "human-run", removes files, and Manage cannot reach it [12].

**A tension to note.** The README says `mem sleep` applies T0 and "T1 files a proposal", and that "deletion only
ever arrives as a proposal you confirm" [4]. In `manage.py` a reasoner's accepted verdict is applied inside the
sleep, including for delete proposals (up to 3 per sleep), and the effect is to end validity, not to remove the
file [12]. The two statements agree only if "deletion" means physical removal. `CLAUDE.md` states the narrower
rule: T1 "only creates new files or marks old ones invalid" [5]. The README speaks of "authority tiers" and the
September write-up of a "tier gate"; I found no tier setting in the default configuration I read [4][11][21].

**When it runs.** The first sleep needs three completed sessions; later ones need 24 hours and three new
sessions. Hooks check this after a distillation, a detached one-shot worker takes a claim, and an optional
user-installed cron entry can add a wall-clock wake-up. There is no resident process: with no cron entry and no
active host, a due sleep waits for the next lifecycle event [9][11].

## Cost and operating profile

| Question | Answer | Source |
|---|---|---|
| Needs | Python 3.12 or newer, uv, a host CLI that is installed and signed in (`claude`, `codex`, `hermes` or `muse`) | [4][16] |
| LLM calls at read time | none by default | [4][11] |
| LLM calls at write time | one headless host process per batch of conversation; the host runs its own tool loop against the memory toolkit over stdio MCP, with its built-in tools and its own memory switched off. Up to three negotiation rounds and one repair round; input is cut into batches of at most 24,000 characters. Triggers: boundary, 20 pending messages, about 4,000 tokens, or 900 seconds idle. | [11][13][16] |
| LLM calls at sleep time | one reviewer run per sleep when proposals exist (in native mode, one isolated host process); bounded to 8 steps and 24 tool calls by default | [11][12] |
| API keys | the library holds none and "contains no LLM client" (Invariant 5); it shells out to the host CLI [5][16]. The host's own login is still needed. An optional "endpoint" reasoner reads `GEMINI_API_KEY` or uses `gcloud` for Vertex; Muse Code through OpenRouter needs `OPENROUTER_API_KEY` | [4][16] |
| Fully local? | storage, index and default recall are local. Distillation and sleep send conversation batches and proposal text to whatever model the host uses, so they are local only if the host's model is. Unstated whether any host was tested with a local model. | [4][16] |
| Privacy | `archive/sessions/` holds full copies of session traces. An issue filed 20261027 reported that bare provider keys were archived verbatim; PR #117, merged 20261029 11:29 UTC, redacts them before the archive. A Hermes route that lets a provider train on prompts is refused unless `host_allow_data_training = true`. | [4][18] |
| Measured cost (project's own) | 30.6 memories and 483 s of host time per episode on one benchmark arm; exam time of 14.1 s and 15.5 s for the two systems compared; a 13x spread in memories per episode across three hosts on identical instructions; native tool mode took a median 14 s against 33 s for the text protocol on one scenario (Haiku) | [10][21] |

## Evidence

### Published results (all first-party)

The README's "Proof it works" reports one study [4]: LongMemEval-S with the haystack cut to 12 sessions per
episode, 120 episodes, Claude Code with Haiku 4.5 as host, one calibrated Sonnet 5 judge, two exam replays per
arm.

| Arm | Pooled accuracy |
|---|---|
| agent-memory | 127/240 = 52.9% |
| MemCore (a system the README does not describe) | 86/240 = 35.8% |
| no memory | 7/120 = 5.8% |

The README says the bounded haystack makes the numbers not comparable to published LongMemEval scores and that
the system-to-system row is end-to-end, so it "licenses no attribution to either half" [4]. See the
[benchmark overview](../papers-benchmarks/README.md) for LongMemEval and LoCoMo.

I checked the numbers against the ledger committed on 20260902 to 20260904 (commit `c5a7fc5`) [21]. They match,
and the ledger adds context the README omits:

- The same system, on the same 120 episodes, scored between 48.3% and 66.7% across seven configurations; the
  project's own protocol says two rows closer than about seven answers "are not distinguishable" and that a row
  with one replay "establishes nothing" [21][22].
- One row, list width 24 at 66.7%, is marked "claim retracted" [21].
- The comparison used MemCore driven by its skill text, not its plugin; the project says this licenses no
  statement about which component is better [21].
- The multi-host claim (9 of 9 writer and reader pairs pass; 2/36 rising to 13/36 correct) rests on 12 episodes
  per host and no single host reaches significance [21].

Other README figures: optional vector fusion raised Recall@5 from 79.0% to 86.6% on a fixed 120-query set while
median latency rose from 5.1 ms to 139.2 ms; fixed-context answer replays showed no end-to-end gain (17/24 against
18/24; 28/36 against 27/36). A Chinese check with 5 memories and 10 queries went from 2/10 to 9/10 with the `cjk`
tokenizer [4]. The corpus size behind the latency figure is **unstated**, and I could not verify these from the
current tree.

**The headline feature has the weakest evidence.** The project's first Manage study (P11, n=24) concluded "Not
measurably, and this round could not have measured it": at the shipped similarity threshold a 3,600-entry corpus
produced 10 proposals, and only 6 of the 24 exam episodes had any accepted decision [21]. At a looser threshold
(0.35) a Haiku reviewer rejected 96 of 132 proposals (73%) [21]. The write-up named a longitudinal protocol (sessions and sleeps
alternating while the clock advances) as what the question needs [21]. Whether a later round ran is **unstated**; the
experiment tree was removed from tracking on 20260908 [20].

**Where the evidence lives.** The README says the protocol, ledger and raw run records are in `docs/experiments.md`
and `experiments/` "in the working tree" and "ship with the source, not with git history" [4]. The current tree
holds neither [8]. `.gitignore` lists both `docs/` and `experiments/` [7]. History shows `experiments/` was
committed 20260902 to 20260904 (a truncated listing at one commit shows more than 46,000 entries under
`experiments/runs`), then untracked on 20260908 13:19 UTC; the old commits remain reachable from `main` [17][20].
So a reader of the current tree cannot check the README's numbers; a reader willing to open commit `c5a7fc5` can,
and the protocol document there is in Chinese [20][22].

### Independent evaluation

None found. One web search for the project on 20261030 19:34 UTC returned no page that names it, which is weak
evidence. The [papers and benchmarks page](../papers-benchmarks/README.md) lists no study of it. The closest to an
outside check is a set of issues from other users (below).

### Tests and CI

- 104 test files: 79 unit, 23 system, 2 red-team (memory poisoning); 24 of them are named regression tests [8].
- CI runs on every push to `main` and every pull request, on Ubuntu and Windows: lint, type check and tests with a
  coverage floor of 85% [7].
- The latest `main` run (push 20261030 14:02 UTC, commit `75531cd`) passed on both systems. The Ubuntu log shows
  1,085 passed, 12 skipped, and 90.02% coverage of 8,921 statements [19]. Coverage is lowest in the adapter layer:
  `openrouter.py` 53%, `doctor.py` 76%, `setup.py` 74%; `recall.py` is 99% and `manage.py` 93% [19].
- An outside issue (#116, filed 20261027, closed 20261029) states that at an earlier commit no test referenced
  `hook_entry.py`, `doctor.py` or `capture.py`. I did not check that commit. The current tree has a regression test
  for capture redaction and CI covers `capture.py` fully [8][18][19].
- The TODO says the live-host checks are opt-in; ordinary CI uses a deterministic stand-in host [10]. How many of
  the 12 skips are live tests is **unstated**.

### Maturity: contributors, issues, releases

| Measure | Value (read 20261030 19:31 to 19:36 UTC) | Source |
|---|---|---|
| Commits on `main` | 324 in 59 days, including merge commits; 93 in the first ISO week, 38 to 47 per week in the last three | [17] |
| Contributors | 18 named by the API; the top two account for 252 of 319 contributions (79%) | [17] |
| Pull requests | 107: 75 merged (by 17 authors), 16 open, 16 closed unmerged; 25 distinct authors | [18] |
| Issues | 10 opened by 10 users, 9 closed; the open one is the opencode request | [18] |
| Releases | none; no tags; version 0.1.0 throughout | [2][7] |

The 9 closed issues are mostly bug reports: a race in correction, path prefix matching in scoped recall, an import
that could write outside the store, a non-atomic ledger append, empty slugs for non-ASCII text, a front-matter
round-trip defect, Windows test failures, an MCP crash on a time-zone-less date, and the secrets issue above [18].
All nine were closed; five were opened on 20260905 and 20260906 [18]. Some PR branches carry a `codex/` prefix and six
commits are authored as "OpenAI Codex"; `CLAUDE.md` addresses coding agents and says the owner merges [5][17].

### What two months of history can and cannot show

| Can show | Cannot show |
|---|---|
| The design was implemented fast and mostly as documented in the parts I read | Whether stores stay healthy after months. By arithmetic from the defaults, weight decay needs 30 idle days and ten idle sleeps to reach the floor; the recency half-life (180 days) is three times the repository's age |
| CI passes on two operating systems with a 90% coverage figure | Format stability. Version is 0.1.0, there is a migration module, and fixes for config and schema round-trips landed in October [9][18] |
| Outside users report real defects and some are fixed within days | Whether the Manage layer helps. The project's own first test could not tell [21] |
| Activity is continuing: commits in every week since launch, from 6 to 93 per week | Staying power of the maintainers, or support for hosts beyond four |
| | Scale. Vector search reads every chunk in Python; the corpus behind the one latency figure is unstated [11] |
| | The PyPI route: the names `agent-memory-core`, `-cli` and `-mcp` already belong to unrelated projects (below) |

**A packaging hazard.** The README says to install from a checkout. At 20261030 19:34 UTC PyPI holds
`agent-memory-core` 0.1.0 (uploaded 20260222) described as a "Markdown + ChromaDB vectors + NetworkX graph"
system from a different repository, with no `vector` extra; `agent-memory-cli` and `agent-memory-mcp` are also
other projects [23]. The README's optional-vector section says "Install `agent-memory-core[vector]`" and, in the
same sentence, offers `uv sync --extra vector` from the workspace [4]. The PyPI form would not install this
project. I installed nothing.

### Star growth

The snapshot records 4,381 stars, 75.53 stars per day (4,381 over an age of 58 whole days), 4.54 forks per 100
stars, and no flag [24]. The snapshot tool flags `fast-growth` at 150 or more stars per day and `low-forks` only at
5,000 or more stars with under 3 forks per 100 stars; this repository is under both limits [25]. These flags are
heuristics. Dividing by the exact age gives about 74 stars per day.

What I could check: 199 forks, 96 watchers, 18 contributors, 25 pull request authors, 10 issue reporters [1][17][18].
The README explains no launch, and with no releases there are no release notes [2][4]. I could not obtain the daily
star curve: the stargazers endpoint returned HTTP 404 to my token on 20261030 19:33 UTC [26]. So the evidence shows
an average of about 74 stars per day over 59 days and a community of forks, reporters and contributors; it does not
show whether growth was steady or came in bursts. I draw no conclusion about the cause.

## Direction

From `docs/TODO.md`, the plans and open pull requests [8][10][18]:

- **Manage safety:** confirmation and host-level authorisation for permanent removal, import and cross-store
  changes ("CLI labels alone do not identify a human"); keeping the earlier text of a split or corrected memory;
  recovery of interrupted multi-file operations outside version control.
- **Write path:** a per-run Write trace and a durable job queue instead of fire-and-forget launch. Open PRs add
  reusable reasoner sessions (#105) and opt-in bounded evidence recall (#112).
- **Hosts and evaluation:** keep live Hermes and Muse Code checks in release checks; verify Codex hooks end to end;
  measure native-tool distillation and run a write-side benchmark round. An open request asks for opencode.
- **Release:** no date, release plan or PyPI plan is stated beyond "no release on PyPI yet" [4].

## Recent changes

The repository is 59 days old, so its whole history falls inside the last 90 days. Times are UTC merge or commit
times [17][18][20].

- 20260908 13:19: `experiments/` removed from tracking. 20260909 13:11: MIT licence merged (PR #25).
- 20261012 15:50: Write and Manage reasoners become separately configurable (#100).
- 20261014 13:20: event-driven automatic Dreaming without a daemon (#101).
- 20261015 15:10: Write becomes a standard tool-use agent over one toolkit (#106); native Muse (20261016 15:07, #107)
  and Hermes (20261016 17:10, #108) execution follow.
- 20261021 12:44: bounded native agent review of Manage proposals (#111).
- 20261029: provider credentials redacted before the archive (11:29, #117); native Windows support (11:41, #113);
  optional CJK tokenizer (14:53, #104).
- 20261030 morning: six hardening pull requests merged (#79, #93, #76, #85, #72, #53): migration, Unicode framing,
  co-occurrence counting, session indices, duplicate-keeper revalidation.

## Sources

1. https://api.github.com/repos/tigerless-labs/agent-memory : description, stars, forks, watchers, dates, licence
   field, topics, archived flag (read 20261030 19:29 UTC; counts again 19:34 UTC)
2. https://api.github.com/repos/tigerless-labs/agent-memory/releases/latest (HTTP 404), `.../releases` and `.../tags`
   (both empty) : no release, no tag (read 20261030 19:29 and 19:31 UTC)
3. https://github.com/tigerless-labs/agent-memory/blob/main/LICENSE via the contents API : MIT text and copyright line (read 20261030 19:29 UTC)
4. https://github.com/tigerless-labs/agent-memory/blob/main/README.md : design claims, store layout, interface, install, results, licence link (read 20261030
   19:29 UTC)
5. https://github.com/tigerless-labs/agent-memory/blob/main/CLAUDE.md : invariants and working rules (read 20261030 19:29 UTC)
6. https://github.com/tigerless-labs/agent-memory/blob/main/skills/agent-memory/SKILL.md : agent-facing write and read guidance (read 20261030 19:29 UTC)
7. https://github.com/tigerless-labs/agent-memory/blob/main/.gitignore, https://github.com/tigerless-labs/agent-memory/blob/main/pyproject.toml, https://github.com/tigerless-labs/agent-memory/blob/main/.github/workflows/ci.yml,
   https://github.com/tigerless-labs/agent-memory/blob/main/packages/core/pyproject.toml, https://github.com/tigerless-labs/agent-memory/blob/main/packages/executor/pyproject.toml : ignore rules, version,
   extras, CI definition (read 20261030 19:29 UTC; package files 19:34 UTC)
8. https://api.github.com/repos/tigerless-labs/agent-memory/git/trees/HEAD?recursive=1 : file layout, test and source counts (read 20261030 19:29 UTC)
9. https://github.com/tigerless-labs/agent-memory/blob/main/docs/design/event-driven-auto-dreaming.md, https://github.com/tigerless-labs/agent-memory/blob/main/docs/design/management-operation-boundaries.md,
   https://github.com/tigerless-labs/agent-memory/blob/main/docs/design/index.md : sleep scheduling, validity rules, hand edits (read 20261030 19:29 UTC)
10. https://github.com/tigerless-labs/agent-memory/blob/main/docs/TODO.md : open follow-ups and a latency figure (read 20261030 19:29 UTC)
11. https://github.com/tigerless-labs/agent-memory/blob/main/packages/core/src/agent_memory/core/ `config.py`, `recall.py`, `search_index.py`,
    `vector_index.py`, `embeddings.py`, `tokenization.py`, `memory_md.py`, `injection.py` : defaults, ranking, vector
    fusion, injection (read 20261030 19:29 to 19:30 UTC)
12. same folder: `manage.py`, `reasoning.py`, `store.py` (the `gc` method), and
    https://github.com/tigerless-labs/agent-memory/blob/main/packages/cli/src/agent_memory/cli/main.py : sleep steps, proposals, caps, `decide`, `gc` (read
    20261030 19:30 UTC)
13. same folder: `schema.py`, `record.py`, `chunking.py`, `indexer.py`, `triggers.py`, `distill.py`, `context.py` :
    types, front matter, links, triggers, distillation flow (read 20261030 19:30 UTC)
14. https://github.com/tigerless-labs/agent-memory/blob/main/packages/mcp/src/agent_memory/mcp/server.py and `tools.py` : MCP server and nine tools (read
    20261030 19:30 UTC)
15. https://github.com/tigerless-labs/agent-memory/blob/main/packages/adapters/src/agent_memory/adapters/ `hook_entry.py`, `moments.py`, `setup.py`,
    `host_setup.py`, `auto_dream.py` : hooks, host dialects, setup, automatic Dreaming (read 20261030 19:30 UTC)
16. https://github.com/tigerless-labs/agent-memory/blob/main/packages/executor/src/agent_memory/executor/ `hosts.py`, `reasoners.py`, `selection.py`,
    `credentials.py` : host CLIs as reasoners, endpoint reasoner and its keys (read 20261030 19:30 to 19:31 UTC)
17. https://api.github.com/repos/tigerless-labs/agent-memory/contributors and `.../commits?per_page=100` (all pages) :
    18 contributors, 324 commits, weekly counts (read 20261030 19:31 UTC)
18. https://api.github.com/repos/tigerless-labs/agent-memory/issues?state=all (all pages), `.../issues/116`, `.../issues/52`,
    `.../pulls/117` : issue and pull request counts, titles, dates, merge times (read 20261030 19:31 UTC; counts of
    authors 19:36 UTC)
19. https://api.github.com/repos/tigerless-labs/agent-memory/actions/runs and the job log of run 41068383784 :
    CI results and coverage table (read 20261030 19:31 to 19:32 UTC)
20. https://api.github.com/repos/tigerless-labs/agent-memory/git/trees/<sha>?recursive=1 for commits `3cd5151` (20260903), `c5a7fc5` (20260904), `6e1b2fe` (20260908) :
    experiment tree committed and later untracked (read 20261030 19:32 UTC)
21. https://github.com/tigerless-labs/agent-memory/blob/c5a7fc59452ac29d2be8c653be4f5b71465dce21/experiments/results/ `index.md`, `p10-memcore.md`,
    `p11-manage.md`, `p1-generality.md`, and `experiments/README.md` at that commit : ledger, system comparison,
    Manage study (read 20261030 19:32 UTC)
22. https://github.com/tigerless-labs/agent-memory/blob/3cd5151f7d174ba4ed34fa594c0c45a4baae3fcd/docs/experiments.md : experiment protocol (read 20261030
    19:33 UTC)
23. https://pypi.org/pypi/agent-memory-core/json, https://pypi.org/pypi/agent-memory-cli/json,
    https://pypi.org/pypi/agent-memory-mcp/json : unrelated packages holding these names; the first lists
    https://github.com/Jakebot-ops/agent-memory-core as its repository (read 20261030 19:34 UTC)
24. [`repos.tsv`](../landscape/20261030_1913-github/repos.tsv), row `tigerless-labs/agent-memory` : snapshot values
    (file produced 20261030 19:13 UTC; row read 20261030 19:29 UTC)
25. [`tools/gh_snapshot.py`](../../tools/gh_snapshot.py), class `Thresholds` and `compute_flags` : flag thresholds
    (read 20261030 19:34 UTC)
26. https://api.github.com/repos/tigerless-labs/agent-memory/stargazers (HTTP 404 to the token used) : no star
    time series available (attempted 20261030 19:33 UTC)
