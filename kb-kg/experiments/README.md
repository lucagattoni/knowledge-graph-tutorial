# Experiments worth running next

**Status: X1 has run; X2 pass A has run on a local model (free); X2 pass B, the paid pilot, has run its first three stages (the owner approved stages A to C, D-34; USD 0.263 on 20261103, [results](x2-index-cost/pass-b-results.md));
stage D has not; X3 to X5 are proposals and nothing in them has run.** Each experiment needs the owner's
explicit yes, one at a time (decision D-14 in [`DECISIONS.md`](../../DECISIONS.md)). Every proposal states its cost, models and data
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

## Order and gates

**Decided 20261102: a slim plan, not a full one.** Each proposal below already states its question, method, data
and risks, and each paid one gets its own pre-registered plan, written before its first paid call (the pattern of the
first paid pilot), once the owner has approved its cost, model and data. A long plan now would restate that with
numbers nobody has measured yet. What was missing was the order, the shared groundwork and how to test the
instruments. That is this section.

**Constraints from the owner (20261102).** Runs happen only on the owner's Apple Silicon Macs: this Mac by default,
another one only through an `ssh` command the owner approves each time, and no cloud or rented hardware. The
repository is public but is the owner's own notebook, so there is no packaging for outside replication; the
records below are enough for the owner to repeat a run, and the public-safety rules still apply. Hosted models are
acceptable, both OpenAI's and Anthropic's, and the experiments must be able to run on either. **One model per
comparison:** builders compared on different models are confounded, so a repeat on the other provider is a separate,
labelled run with its own yes. The exact model and its prices are read from the provider's pages when a run is
approved, not taken from memory. The free alternative is a local model: this Mac (Apple Silicon, 32 GB, 12 cores)
has Ollama with only an embedding model pulled (read 20261102 10:14 UTC), so a local chat model would first have to
be chosen and downloaded.

| Step | What | Money | Why it comes here |
|---|---|---|---|
| 0 | **Free groundwork.** (a) A local metering gateway that every hosted call passes through, for either provider: it logs the provider's usage fields per call, puts them in one common record, and refuses a call past a cap. Most builders speak the OpenAI protocol, so running one on an Anthropic model needs either a provider-side compatibility layer or a translation in the gateway; the rehearsal finds out which, per builder, from the provider's current documentation. (b) The candidate builders installed in throwaway environments, versions pinned, licences read from the `LICENSE` files. (c) Question sets and answer keys frozen before any model sees them. (d) A dress rehearsal of X2 against a stub model, which counts calls and prompt tokens per document. | None | Every paid step reuses it. The rehearsal removes the biggest unknown (calls and input tokens per document) before money is asked for. |
| 1 | **X2 pilot,** in two passes: A on a local model (free), B on a hosted small model under the owner's cap. | The owner's cap | The cheapest and most repeatable. It fills the first gap on the [eager-to-lazy page](../directions/eager-to-lazy-graphs.md), and its per-document figure prices X3. |
| 2 | **X4 pilot** (3 questions, 2 conditions, 2 repositories). | The owner's cap | Independent of X2 and small (6 agent runs). Agent runs vary from run to run, so a pilot measures cost and feasibility, not a result. |
| 3 | **X3.** | Set from X2 | It needs X2's per-document cost and a baseline that uses BM25 alone. It is the largest of the runs that bear on a decision. |
| 4 | **X5.** | Set from X2 and X4 | The heaviest: it scales with corpus size times questions. |

**Gates between steps.** After each step I report the measured cost and what the instrument could not show. The next
step starts only on the owner's explicit yes (D-14), stating cost, model and data first. A step does not start just
because the one before it worked.

**Step 0 status, 20261102: built, with the gaps below.** (a) The [metering gateway](../../tools/metering_gateway.md)
exists for both providers and has been exercised with the real OpenAI and Anthropic SDKs against fake providers. (b) and
(d) Four builders were installed in throwaway environments and rehearsed against a stub; the
[results side by side](x2-index-cost/README.md#the-rehearsals-side-by-side) are on the X2 page. (c) The 20 X2 documents
and the 20 X4 questions with their answers are [frozen](x4-code-graph-vs-grep/README.md). **Not done:** the gateway has
never been used against a real provider or with a builder; no scoring program exists for X4's answers, so the check that a
perfect answerer scores 100% and a random one lands near chance is still to do; no output tokens have been measured, so no
cost can be derived yet; and the question wording has not been tried on any agent.

**How the instruments are tested before any money is spent.**
- *The gateway,* against a stub upstream: counted usage equals the stub's reported usage; the call that would pass the
  cap is refused and nothing is forwarded; an upstream error or a 401 counts as zero; a builder configured with only
  the gateway's address and a dummy key cannot reach the provider another way. Then break the cap check on purpose;
  the test must turn red.
- *The builders,* against the stub: calls and prompt tokens per document are identical across two runs; each
  installs and runs on Apple Silicon. Output tokens cannot be known from a stub; pass A measured them for one local model (4 to 16 times the stub's, [page](x2-index-cost/pass-a-local-model.md#results-of-the-longer-runs)), and a hosted model will differ.
- *The scoring,* before any model run: the answer keys are derived by hand; a perfect answerer scores 100% and a
  random one lands near chance; the paired sign test matches a known table.
- *Lessons from the first paid pilot, built in:* read the free pre-flight estimate first; check the key's shape
  (one key, not two pasted together) without printing it; run long jobs in the background with a log; stop at the
  first failure and report it.

**What this does not decide:** which builders (the entries suggest [LightRAG](../projects/lightrag.md) and
[Microsoft GraphRAG](../projects/microsoft-graphrag.md), whose latest releases are dated 20260902 and 20261008;
[nano-graphrag](../projects/nano-graphrag.md)'s last GitHub release is dated 20241001 and
[fast-graphrag](../projects/fast-graphrag.md)'s last push was 363 days before 20261030, so the rehearsal decides
whether they are worth a paid pass); which model, provider or cap; the agent client for X4, chosen when its pilot is
approved. All four builders are MIT per their `LICENSE` files, read 20261030. A new key is needed for any hosted run:
the one used for the first paid pilot was deleted at the owner's request, and each run's key is separate and, if the
provider's console offers a per-project spend limit, limited there as well as at the gateway.

## Rules that apply to every experiment

- **Third-party code is untrusted.** Each experiment runs other projects' code. I would install it in a
  throwaway environment under the scratch directory. A hosted run gives that code only a dummy key and the
  gateway's address; the real key stays with the gateway process and is never written into this repository or
  printed (if it is kept in a file, that file has mode 600 and sits outside any repository, as in decision D-20).
  Projects under GPL, AGPL or non-commercial terms are run for measurement only; no code from them enters this
  repository.
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
- **Models.** One small model, the owner's choice; OpenAI and Anthropic models are both acceptable (owner,
  20261102), one per comparison. A local model
  would make the pilot free in money and slower in time: this Mac runs Ollama but holds only an embedding model
  today (read 20261102 10:14 UTC).
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

A yes to Step 0, the free groundwork, which costs nothing. Then, only after its rehearsal has produced numbers: which
local chat model to pull, if any; and for each paid step, its own yes with the model, the provider and the cap
(D-14).
