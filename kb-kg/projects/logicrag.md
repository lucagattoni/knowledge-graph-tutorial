---
slug: logicrag
repo: chensyCN/LogicRAG
tier: deep
category: core
snapshot: 20261030 18:58 UTC
---

# LogicRAG

| | |
|---|---|
| Repository | https://github.com/chensyCN/LogicRAG (formerly named Agentic-RAG; the old name still redirects) [1][15] |
| Licence | GPL-3.0. The `LICENSE` file is the GNU General Public License version 3 text (dated 29 June 2007, 674 lines). The README names no licence and has no licence badge, so there is no disagreement to report. The file was added on 20260719; before that the repository had none (see "Changed since the July 2026 investigation") [1][4][5][6] |
| Language | Python [1] |
| Stars, forks | 241, 37 (read 20261030 18:58 UTC); 8 watchers [1] |
| Created, last push | 20250407 09:15 UTC, 20260719 10:34 UTC [1] |
| Latest release | none: the releases endpoint returns 404 and the tags list is empty (read 20261030 18:58 UTC) [2] |
| Status | quiet: last push is 103 days before the snapshot, outside the 90-day window. Not archived. 43 commits in all, 0 since 20260801 [1][3] |
| Paper, docs | arXiv 2508.06105, "You Don't Need Pre-built Graphs for RAG: Retrieval Augmented Generation with Adaptive Reasoning Structures"; v1 20250808, v2 20251117; arXiv comment "accepted to AAAI'26" [11]. No docs beyond the README [5] |

## What it is

LogicRAG is a research implementation of a query-time alternative to GraphRAG. It builds no graph over the
corpus. At question time an LLM breaks the question into sub-questions, a second step records which sub-question
depends on which, the sub-questions are put in dependency order, and each is retrieved for and checked in
turn, with the earlier results carried forward as a short running summary [7][13]. The repository is small
research code (`run.py`, `src/`, `config/`, bundled copies of three QA datasets and their corpora); GitHub lists
one contributor [1][3][10]. The package metadata still carries the old name "agentic-rag" [10]. All LLM calls go to one
OpenAI model, `gpt-4o-mini` by default, at temperature 0 and a 250-token output cap; retrieval is dense cosine
similarity over `sentence-transformers/all-MiniLM-L6-v2` embeddings [8][9][10].

## How it works

### Indexing

There is no LLM step at index time. The corpus is read from a JSON file, each document becomes one retrievable
unit (title plus text, no further chunking), and every unit is embedded once and cached to disk. The cache file
name depends only on the number of documents, not on their content [8]. The embedding pass is the only
index-time work.

### Query-time pipeline (as in the released code)

All of it is in `src/models/logic_rag.py`, method `answer_question` [7].

| Step | What happens | LLM calls |
|---|---|---|
| 1. Warm-up retrieval | Dense top-k retrieval on the raw question. One call summarises the chunks. A second call returns a JSON object with: an answerable flag, the missing information, a follow-up sub-query, a current understanding, a list of "dependency" strings, and a reason | 2 |
| 2. Easy exit | If the answerable flag is true, one call writes a terse final answer from the summary and the run ends with zero rounds | +1 (3 in all) |
| 3. Ordering | Otherwise the dependency strings go to one LLM call that returns index pairs "A depends on B". Local code orders the strings with a depth-first topological sort. The follow-up sub-query from step 1 is not used afterwards | +1 |
| 4. Solve loop | While rounds are below the cap and dependencies remain: retrieve for the current dependency string, fold the new chunks into the running summary (1 call), then ask whether the summary now answers the full question (1 call). If yes, stop. If no, move to the next dependency; the same one is never retried | 2 per round |
| 5. Synthesis | One call writes the final answer from the summary alone. If the cap or the list runs out first, it still answers from the summary | +1 |

Call counts, read from the code (not executed): easy path 3 calls and 1 retrieval; hard path 4 + 2R calls and
1 + R retrievals, where R is the number of rounds run (R is at most the round cap, default 3, so at most 10
calls) [7]. There is no keyword search, no reranker, and no per-sub-question answer object: the running summary
is the only state that moves forward [7][8].

Details that matter when reading the code:

- **No cycle detection.** The topological sort is a depth-first search with a visited set. If the model returns
  pairs that form a cycle, the sort returns some order without error and without a repair. Pair indices are
  only bounds-checked from above [7]. The paper says the graph "is verified via topological sorting to enforce
  acyclicity" [13]; the code does not do that.
- **Structured output is requested in the prompt, not enforced.** JSON is asked for in plain text and parsed
  with a repair function that handles two truncation patterns (a missing closing brace, a cut-off
  "current understanding" field). A commit message of 20250523 says the repair was added for broken JSON
  responses [3][9]. If the warm-up reply cannot be parsed, the code behaves as if the question were answerable
  and takes the easy path [7]. The pair-generation and per-round checks have no equivalent fallback in the code
  read; an unparsable reply there would fail inside the call path (by reading, not executed) [7].
- **API failures are swallowed.** The call wrapper that adds retry and rate limiting catches every exception
  inside itself and returns an empty string, so the retry decorator has nothing to retry and the "raw
  concatenation" fallback in the summary step is not reached by an API error (by reading, not executed) [9].
  The configured limit is 20 calls per minute [10].
- **A repeat filter exists but is off.** The class can skip chunks it has already retrieved, default off, and
  the command-line entry point does not expose it [7][10].
- **Dense retrieval over the whole matrix.** Cosine similarity of the query against every stored embedding,
  top-k by score, with a per-process cache keyed on the query string [8].

### Paper and code differ

The released code implements a simpler algorithm than the paper's Algorithm 1 [7][13].

| Paper mechanism | In the released code |
|---|---|
| Edges inferred by the LLM, acyclicity "verified via topological sorting" (Framework section) | One pair-generation call and a depth-first sort; no cycle check [7][13] |
| Few-shot prompting for decomposition (Framework section) | The prompts read contain no examples [7][13] |
| Graph pruning by unified subquery: merge all sub-problems of the same topological rank into one query, one retrieval per rank (Eq. 4, Algorithm 1 lines 9 to 11) | Absent. One dependency per round [7][13] |
| An intermediate answer stored per sub-problem, final answer composed from them (Algorithm 1 lines 14 and 21) | Absent. The final answer is written from the running summary [7][13] |
| Dynamic DAG augmentation: add new sub-problems and edges mid-run (Algorithm 1 lines 16 to 18) | Absent. The list never grows [7][13] |
| Rolling memory, `Mem(i) = Summarize(Mem(i-1) + retrieved(p_i))` (Eq. 3) | Present; the summary is rewritten by an LLM call in every round, with no size trigger [7][13] |
| Sampling without replacement (Figure 4) | Present as a cursor that always advances, per dependency. In the paper it operates on batches of same-rank sub-problems [7][13] |
| (Not described in the paper text read) Warm-up retrieval with an early exit | Present in code: step 1 and 2 above [7][13] |

Whether the paper's reported numbers were produced by the released code or by the Algorithm 1 variant is
**unstated** in the pages read. The Table 1 and Table 4 results below are therefore results of "LogicRAG as
published", not necessarily of this repository's code [13].

### The efficiency mechanisms

- **Rolling memory.** One text string, summarised again every round, capped to 250 output tokens, so the
  context the model sees per round does not grow with the number of chunks retrieved [7][10]. In the paper's
  Figure 6 discussion, accuracy shows diminishing returns beyond top-3 or top-5; LLM accuracy on HotpotQA
  saturates near top-10; on MuSiQue the gain is more gradual; and MuSiQue's average cost exceeds 6000 tokens at
  top-20 [13].
- **Sampling without replacement.** The paper observes that when the model may stay on the same sub-problem, it
  tends to emit near-duplicate sub-queries: word-level Jaccard similarity between the sub-queries of rounds 1
  and 2 is 0.53 to 0.68 across the three datasets, and between rounds 4 and 5 it is 0.84 to 0.92 (Figure 3
  values, measured with replacement allowed) [13].
  Forcing progress lowered tokens per question at similar accuracy (Figure 4 data labels, tokens with / without
  replacement; accuracy with / without):

  | Dataset | Tokens with | Tokens without | Change | Accuracy with / without |
  |---|---|---|---|---|
  | 2WikiMQA | 2437 | 1997 | -18% | 63.1 / 62.5 |
  | HotpotQA | 2097 | 1732 | -17% | 62.6 / 62.6 |
  | MuSiQue | 3873 | 2501 | -35% | 36.4 / 37.5 |

  The percentages are computed here from the printed values [13].
- **Round cap and top-k.** `--max-rounds` defaults to 3 and `--top-k` to 5 in the command line; the paper uses
  k = 3 [5][10][13]. On reaching the cap the code still writes a best-effort answer [7].
- **Easy questions.** The warm-up path is plain retrieval plus one sufficiency judgment, so a question judged
  answerable never builds an ordering. The judgment is a single un-calibrated LLM boolean [7]. The paper
  reports that 4-hop questions need fewer retrieval rounds on average than 3-hop ones, and attributes it to
  the LLM becoming "prematurely confident" on long queries and answering from partial information; it names
  this a trust-calibration challenge and does not propose a fix in the text read. The paper does not tie this
  to the code's warm-up gate, which the paper text read does not describe [13].

## Cost and operating profile

| Item | Value |
|---|---|
| Index-time LLM cost | None. One embedding pass over the corpus, cached [8] |
| Per-query LLM calls | 3 on the easy path; 4 + 2R on the hard path, at most 10 with the default cap of 3 (from the code, not measured) [7] |
| Per-call output | Capped at 250 tokens [10] |
| Per-query tokens (paper, 2WikiMQA, average) | LogicRAG 1777.9, VanillaRAG 489.7: about 3.6 times plain retrieval [12] |
| Per-query latency (paper, 2WikiMQA, average) | LogicRAG 9.83 s, VanillaRAG 4.28 s: about 2.3 times [12] |
| Needs | An OpenAI API key (read from the environment); PyTorch and sentence-transformers for embeddings; a GPU is optional (the paper's machine had an RTX 3090) [5][10][13] |
| Fully local? | Embeddings run locally. The LLM client is built for OpenAI with no base-URL setting in the config read. In April 2025 the author replied to an issue that a local OpenAI-compatible server needs edits to the client and model name and that built-in local support would follow "soon"; no such change is in the repository at the snapshot [6][9][10] |
| Persistence | Only the corpus embedding cache. Per-question reasoning (sorted dependencies, per-round queries and verdicts) is held in memory on the model object for the evaluation code to read; nothing is written to disk per query [7][8] |

## Evidence

All results below are the authors' own, from the paper, on `gpt-4o-mini` for generation and for the LLM judge,
with one embedding model for every method [12][13]. I found no independent evaluation in two web searches and
one repository search; that is not an exhaustive search [15][16].

**Setup.** Three multi-hop QA sets: HotpotQA, 2WikiMultiHopQA, MuSiQue (answerable). 1,000 validation questions
from each. The retrieval corpus for each is built, as in HippoRAG and IRCoT, from all supporting and
distractor passages of those questions: 9,221 passages (HotpotQA), 6,119 (2WikiMQA), 11,656 (MuSiQue). For
baselines that offer single-step and multi-step modes, the multi-step mode was used. Metrics: Str-Acc (gold
answer contained in the normalised output) and LLM-Acc (an LLM decides). Repeated runs, variance and
significance tests are **unstated** in the pages read (pages 8 and 10 of the PDF text were not returned by the
reader) [13].

**Accuracy (Table 1, Str-Acc / LLM-Acc)** [12][13]:

| Method | HotpotQA | 2WikiMQA | MuSiQue |
|---|---|---|---|
| VanillaRAG, top-5 | 44.1 / 53.9 | 46.7 / 45.6 | 21.0 / 23.6 |
| RAPTOR | 48.1 / 57.8 | 47.7 / 45.9 | 25.2 / 29.1 |
| LightRAG | 47.8 / 57.7 | 43.1 / 36.3 | 18.1 / 19.4 |
| GraphRAG | 39.6 / 45.2 | 46.3 / 43.3 | 16.5 / 23.1 |
| HippoRAG2 | **56.7** / 61.9 | 50.0 / 47.1 | 27.0 / 32.6 |
| LogicRAG | 54.8 / **62.6** | **64.7 / 62.5** | **30.4 / 37.5** |

On HotpotQA, LogicRAG is best on LLM-Acc and below HippoRAG2 on Str-Acc (54.8 against 56.7). The paper's text
says LogicRAG "outperforms all baselines by a significant margin across all datasets", which Table 1 does not
bear out on that cell. The largest margin is on 2WikiMQA: +14.7 points Str-Acc over HippoRAG2 [13].

**Accuracy by question type** is reported for LogicRAG only (Figure 5 discussion). HotpotQA: comparison 83%,
bridge 58%. 2WikiMQA: comparison 89%, bridge-comparison 67%, compositional 50% (44.4% of the questions),
inference 39%. MuSiQue accuracy falls as the number of hops rises. No per-type numbers for the baselines are
given, so the paper does not show *where* LogicRAG's margin over them comes from [13].

**Query-time cost (Table 4, 2WikiMQA, average per question; excludes graph construction)** [12]:

| Method | Time (s) | Tokens |
|---|---|---|
| ZeroShot | 5.88 | 216.2 |
| VanillaRAG | 4.28 | 489.7 |
| G-retriever | 12.50 | 1000.0 |
| RAPTOR | 5.79 | 2568.0 |
| HippoRAG | 6.30 | 2608.8 |
| HippoRAG2 | 5.89 | 2809.2 |
| GraphRAG | 13.05 | 4699.8 |
| LightRAG | 35.14 | 5730.6 |
| KGP | 70.72 | 11097.8 |
| **LogicRAG** | 9.83 | 1777.9 |

LogicRAG uses fewer tokens than every graph baseline in this table except G-retriever (1000.0), and is faster
than G-retriever, GraphRAG, LightRAG and KGP but slower than RAPTOR, HippoRAG and HippoRAG2. G-retriever has
the lowest Table 1 accuracy of the graph methods [12].

**Index-time cost (Figure 1).** The figure plots prompt tokens, completion tokens and runtime for graph
construction on 2WikiMQA for HippoRAG, RAPTOR, LightRAG and GraphRAG. The token axis is scaled in units of
10^7 and the runtime axis runs from 10^1 to 10^2 minutes; per-method values are not in the text layer. The paper
says preprocessing "often takes tens to hundreds of minutes" [13].

**Limits of the evidence.** Small corpora (6k to 12k passages) assembled from the questions' own passages; one
LLM family for generation and judging; baselines run by the authors; LLM-judged accuracy; and the paper-versus-
code gap above. The paper text read has no limitations section [13].

## Direction

The repository has no roadmap, no releases and no tags [2][5]. The core code (`logic_rag.py`, `utils.py`) last
changed on 20251110, a week before arXiv v2 [3]. Later commits edit the README (20251213, 20260508) and add the
licence (20260719) [3]. The owner closed the licence request the same day with a reply [6]. The only open item is a
pull request from the requester that adds a 21-line `LICENSE` file (contents not read); it has not been merged
[6]. Repository search returns other repositories with "LogicRAG" in the name, including
`zhouff000/LogicRAG-reproduction` (GPL-3.0, pushed 20260825) and `Imran2205/LogicRAG` ("Implementation of
Logic-RAG", pushed 20250516, before the paper's first version); I did not read them and their relation to this
project is unstated [15]. I found no successor paper from the authors and no rename beyond the earlier one
[16].

## Changed since the July 2026 investigation

The July investigation is dated 20260726 08:53 UTC. Everything below was read 20261030 18:58 to 19:04 UTC.

**Repository and paper**

- **Stars and forks:** 241 and 37, against about 234 and 36 in July [1].
- **Licence:** still GPL-3.0, and the July statement was right. New detail: the `LICENSE` file was added by the
  newest commit, 20260719 10:34 UTC, in answer to an issue opened 20260713 asking for an MIT or Apache licence.
  The owner replied that a GPL v3 licence had been added. The repository had no licence file before that date
  [3][4][6]. I did not check whether individual source files carry licence headers; the three code files read
  have none [7][8][9].
- **Activity:** 0 commits since 20260801; last push 20260719; no release or tag; not archived [1][2][3].
  "Maintained-but-frozen" (July) now reads as quiet: 103 days since the last push.
- **Code and README:** no change to the algorithm. The July reading was of the same code (last algorithm commit
  20251110). The README still shows the paper link, the key-features list and the usage example, and its
  last-commit badge still points at the old repository name [3][5].
- **Paper:** two arXiv versions only, v1 20250808 and v2 20251117; no v3. The README now links an OpenReview page
  for the AAAI'26 title (not fetched). The AAAI proceedings page returned HTTP 503 twice, so the AAAI
  publication record (a web-search summary gave March 2026) is unverified. Differences between v1 and v2 are
  unstated: I did not diff them. The v2 HTML and the v1-stamped PDF text give the same Table 1 and Table 4 values [11][12][13][14][16].
- **Successor or rename:** none found. The repository was renamed from Agentic-RAG earlier (redirect confirmed);
  this was already visible in July through the package name [1][10][15][16].

**July claims corrected in the body above**

| July statement | Correction | Basis |
|---|---|---|
| Hard path = "3 + 1 + 2 per round + 1" LLM calls | 4 + 2R. The "3" counted the easy path's answer call, which the hard path does not make before the loop; it was then counted again as the final call | Code reading [7] |
| Sampling without replacement cut tokens "~35%" | 35% on MuSiQue only; 18% on 2WikiMQA and 17% on HotpotQA | Figure 4 labels [13] |
| Accuracy "saturates at k=3-5" | The paper says diminishing returns beyond top-3 or top-5, saturation near top-10 for HotpotQA LLM accuracy, and a more gradual curve on MuSiQue | Figure 6 text [13] |
| LogicRAG is "cheaper than every graph method even ignoring their indexing cost" | Not true of G-retriever on tokens (1000.0 against 1777.9); and slower than RAPTOR, HippoRAG, HippoRAG2 | Table 4 [12] |
| Indexing cost "zero" | No LLM cost; one embedding pass with a disk cache | Code [8] |
| "Fallback on LLM failure is raw concatenation" | That fallback is not reached by an API error, because the call wrapper returns an empty string instead of raising (by reading) | Code [7][9] |
| Wins are largest "where questions are structurally compositional (2WikiMQA)" | An interpretation, not a paper finding. The paper gives per-type accuracy for LogicRAG only, and compositional is its weak spot on 2WikiMQA (50%, the largest category) | Figure 5 text [13] |
| The paper "documents the failure mode of that judge" (the warm-up gate) | The paper documents premature confidence on long queries but does not describe the warm-up gate in the text read; tying them together is an inference | Paper text [13] |
| Paper features absent from code: rank-merged queries and dynamic DAG growth | Confirmed. Also absent: per-sub-problem answers and few-shot decomposition prompts. Also true: the warm-up early exit is in the code but not in Algorithm 1 | Code and Algorithm 1 [7][13] |
| ~43 commits; setup name from a rename | Confirmed: 43 commits; package name still "agentic-rag" | [3][10] |

## Sources

1. https://api.github.com/repos/chensyCN/LogicRAG (and its /contributors list): stars, forks, watchers, licence field, archived flag, dates, language, open issue count, contributors (read 20261030 18:58 UTC)
2. https://api.github.com/repos/chensyCN/LogicRAG/releases/latest and /tags: 404 and empty list (read 20261030 18:58 UTC)
3. https://api.github.com/repos/chensyCN/LogicRAG/commits: full history of 43 commits, none since 20260801, per-file last-change dates, licence commit contents (read 20261030 18:58 UTC and 19:03 UTC)
4. https://github.com/chensyCN/LogicRAG/blob/main/LICENSE: GNU GPL version 3 text (read 20261030 18:58 UTC)
5. https://github.com/chensyCN/LogicRAG/blob/main/README.md: description, options, example, badges, citation (read 20261030 18:58 UTC)
6. https://github.com/chensyCN/LogicRAG/issues/1, /issues/2 and /pull/3: local-LLM question and reply (20250416), licence request and reply (20260713 to 20260719), open pull request (read 20261030 18:59 UTC and 19:02 UTC)
7. https://github.com/chensyCN/LogicRAG/blob/main/src/models/logic_rag.py: pipeline, ordering, loop, fallbacks (read 20261030 19:00 UTC)
8. https://github.com/chensyCN/LogicRAG/blob/main/src/models/base_rag.py: corpus loading, embedding cache, dense retrieval (read 20261030 19:00 UTC)
9. https://github.com/chensyCN/LogicRAG/blob/main/src/utils/utils.py: call wrapper, JSON repair, evaluation helpers (read 20261030 19:00 UTC)
10. https://github.com/chensyCN/LogicRAG/blob/main/config/config.py, setup.py, run.py, requirements.txt and src/main.py: model, token cap, rate limit, defaults, command-line options, package name (read 20261030 19:00 UTC)
11. https://arxiv.org/abs/2508.06105: version history, comment field, abstract (read 20261030 19:01 UTC)
12. https://arxiv.org/html/2508.06105v2: Table 1 and Table 4 values, as extracted by a page reader (read 20261030 19:01 UTC)
13. https://arxiv.org/pdf/2508.06105v2 (full text via the alphaXiv reader, page stamp reads v1): framework, Eq. 3 and 4, Algorithm 1, Figures 1, 3, 4, 5, 6, 7, Tables 1, 2, 4 (read 20261030 19:02 UTC)
14. https://ojs.aaai.org/index.php/AAAI/article/view/40278: HTTP 503 on two attempts, not read (attempted 20261030 19:01 UTC)
15. GitHub account listing for chensyCN, repository search for "LogicRAG", and the redirect from chensyCN/Agentic-RAG (read 20261030 19:01 UTC)
16. Two web searches for a successor or later paper (20261030 19:01 UTC and 19:02 UTC): none found
