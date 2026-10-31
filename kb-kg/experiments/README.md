# Experiments worth running next

**Status: proposals only. Nothing here has run.** Each experiment needs the owner's explicit yes, one at a
time (decision D-14 in [`DECISIONS.md`](../../DECISIONS.md)). Every proposal states its cost, models and data
first. Where a cost cannot be known before a pilot, the proposal says so and asks for a **cap on the pilot**,
not for a budget on the whole experiment.

Each proposal answers a question the [direction pages](../directions/README.md) leave open.

| ID | Question it answers | Needs | Cost | Start with |
|---|---|---|---|---|
| X1 | How unusual are the fast-growth repositories, as a description? | Nothing new | None (local, no model) | The two snapshots already in this repository |
| X2 | What does it actually cost to build a graph, per document, with each cheap builder? | A small model, the owner's key or a local model | **Unknown until a pilot** | 20 documents, a few builders, a cap |
| X3 | Which route is cheaper at equal accuracy on one corpus? | X2's numbers first | Set after X2 | Do not start before X2 |
| X4 | Does a code graph help an agent beyond saving tokens? | A model for an agent, the owner's key | **Unknown until a pilot** | 3 questions in 2 conditions on 2 repositories, a cap |
| X5 | At what size does an index-only wiki stop working? | A model to navigate | **Unknown until a pilot** | Last; the heaviest |

## Rules that apply to every experiment

- **Third-party code is untrusted.** Each experiment runs other projects' code. I would install it in a
  throwaway environment under the scratch directory, with only the one scoped API key the owner names set in
  that process's environment, never written to a file. Projects under GPL, AGPL or non-commercial terms are
  run for measurement only; no code from them enters this repository.
- **Costs are measured, not estimated.** Token counts come from the provider's usage fields, recorded per
  call. A figure derived from them is labelled as arithmetic.
- **Everything is recorded.** Tool versions and commit hashes, the model name as the provider reports it, the
  dataset version and its licence, the date, and the raw logs. A result without these is not a result.
- **No verdicts.** An experiment reports numbers, the setup and what the setup cannot show.

## X1: Describe the snapshots

- **Question.** The [evidence page](../directions/evidence-and-claims.md) flags nine repositories as
  fast-growing in the first snapshot (ten in the second) and cannot say whether the growth is organic. How do they sit among the 931 repositories in
  the newest [snapshot](../landscape/20261030_1954-github/README.md) on stars per day, forks per 100 stars,
  contributors and issues?
- **Method.** Percentiles and a table from `repos.tsv`. No model, no new API calls.
- **Data.** The two snapshots already committed.
- **Cost.** None beyond local compute.
- **What it would change.** It gives the flag context. It cannot tell organic growth from inflated growth, and
  the page would say so.
- **Ran 20261031 16:00 UTC.** Output: [`x1-snapshot-distributions/`](x1-snapshot-distributions/README.md),
  made by `tools/describe_snapshot.py` (14 tests; a deliberate break of its tie rule turned 3 red). No model, no
  network, no money. Among the 552 ranked repositories of the second snapshot, the ten flagged repositories sit
  at the 95th to 99th percentile on stars, by construction at the 98th to 100th on stars per day, between the
  15th and 75th on forks per 100 stars, and between the 25th and 91st on contributors where recorded. This is a
  description of this set; it does not say whether any growth is organic.

## X2: The measured index cost of cheap graph builders (pilot)

- **Question.** "Measured index cost is absent from most card entries" is the first gap on the
  [eager-to-lazy page](../directions/eager-to-lazy-graphs.md). How many LLM calls and tokens does each builder
  use per document, on the same documents, with the same model?
- **Method.** Build a graph for the same 20 documents with each of a few permissively licensed builders (the
  candidates from the entries are [LightRAG](../projects/lightrag.md), [nano-graphrag](../projects/nano-graphrag.md),
  [fast-graphrag](../projects/fast-graphrag.md) and [Microsoft GraphRAG](../projects/microsoft-graphrag.md); the
  owner picks), one fixed small model, default settings. Record calls, input and output tokens, and wall-clock
  time per document. **No quality measurement in this step.**
- **Data.** The documents of MultiHop-RAG, a public news dataset (2,556 queries; evidence in 2 to 4 documents,
  per the [papers page](../papers-benchmarks/README.md)). Its licence is **unstated in what I read**: I would
  read it before downloading anything.
- **Models.** One small model, the owner's choice. Whether a local model is available on the owner's machine is
  **unstated**; a local model would make the pilot free in money and slower in time.
- **Cost.** **Unknown before the pilot.** That is the point of it. The pilot is 20 documents times a few
  builders. The cap is the owner's number; I will not propose one without a measured per-document figure.
- **Output.** `kb-kg/experiments/x2-index-cost/`: raw usage logs, a table of calls and tokens per document,
  and the exact settings.
- **What it would change.** The "unstated" index-cost cells in the eager-to-lazy page become measured, for the
  builders run. It does not say which is better.
- **Risks.** Defaults differ between builders, so "same settings" means each builder's own defaults, said so.
  Extrapolating 20 documents to a corpus is arithmetic and is labelled so.

## X3: A matched-cost comparison on one corpus (after X2)

- **Question.** "No study compares the five routes on one corpus" (eager-to-lazy) and "no entry holds a
  like-for-like cost comparison" ([reasoning retrieval](../directions/reasoning-retrieval.md)).
- **Method.** One corpus, one question set, four conditions: BM25, a free hybrid retriever with reranking, one
  cheap graph builder from X2, and one navigation-based method. Report accuracy by query type (the dataset has
  inference, comparison, temporal and null queries) and tokens for indexing and per query.
- **Cost.** Set after X2: X2's per-document figure times the corpus size, plus query-time tokens. **Do not
  approve before X2 has run.**
- **Risks.** A navigation method's index cost depends on caching; cost must be priced the same way for every
  condition, which the existing entries do not do.

## X4: Does a code graph beat grep, beyond saving tokens? (pilot)

- **Question.** The first unresolved item on the [code graphs page](../directions/code-knowledge-graphs.md):
  whether an agent solves coding tasks better, not only cheaper, with a graph than with grep and glob.
- **Method.** Two public repositories, 10 questions each with answers a person can check (where a function is
  defined, what calls it), an agent with grep and glob against the same agent with one code-graph tool
  ([codebase-memory-mcp](../projects/codebase-memory-mcp.md), MIT per its entry). Record tokens from usage
  fields, tool calls, and correctness against answers I derive by hand before running. **Pilot: 3 questions in
  2 conditions.**
- **Models.** An agent model on the owner's key; which tier is the owner's choice and **unstated** so far.
- **Cost.** **Unknown before the pilot.** The pilot is 6 agent runs; the cap is the owner's.
- **Output.** A results file with the questions, the hand-derived answers, logs and the tool versions.
- **What it would change.** The page would hold one more comparison, with the setup stated. It would still be
  a small, owner-run test, not an independent evaluation, and says so.

## X5: At what size does an index-only wiki stop working?

- **Question.** The first unresolved item on the [files and wikis page](../directions/plain-files-and-wikis.md).
- **Method.** Markdown corpora of 10, 30, 100 and 300 pages from a public set; a model answers fixed questions
  by reading an index page and then pages; accuracy and tokens against corpus size, with BM25 as the baseline.
- **Cost.** **Unknown before a pilot**, and the largest of the five because it scales with size times
  questions. I would run it last and only after X2 and X4 have shown what a model run costs here.

## What I need from you

Which of X1, X2 and X4 to start (X3 and X5 wait), which model and provider each may use (and whether a local
model is available), the cap for each pilot, and a yes for each one separately.
