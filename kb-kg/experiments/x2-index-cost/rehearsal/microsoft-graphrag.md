# X2 rehearsal: Microsoft GraphRAG indexing against a stub model

Part of Step 0 of the [order and gates](../../README.md#order-and-gates). No model, no key, no money: GraphRAG's
`graphrag index` was pointed at a loopback stub that answers in the format its prompts demand, and the stub counted
what arrived. Background on the project is in [its entry](../../../projects/microsoft-graphrag.md). Machine-readable
results, with every number below and the sources: [`microsoft-graphrag.json`](microsoft-graphrag.json). The runner is
[`tools/exp/x2_microsoft_graphrag.py`](../../../../tools/exp/x2_microsoft_graphrag.py). Run 20261102 10:46 to 10:48 UTC.

**Read this first.** Prompt and completion tokens are the stub's tiktoken `cl100k_base` counts, not any provider's.
Completion tokens are the length of the stub's own fixed answers, so they say nothing about a real model. Everything
that depends on what a model answers is a count *for the stub's answers* (shape B below), not a prediction.

## What was run

| Item | Value | Source, read at (UTC) |
|---|---|---|
| Builder, version | `graphrag` 3.3.0 (with its seven sibling packages at 3.3.0), the latest GitHub release, published 20261008 18:28 UTC | `gh release list`, 20261102 10:27 |
| Tag commit | `5faaaf4f5685fa2056fa8c3bf9342cb089f2942f` | GitHub API, 20261102 10:27 |
| Python, machine | CPython 3.12.16 (uv), Apple Silicon arm64; the package supports 3.11 to 3.13 | PyPI JSON, 20261102 10:27 |
| Method, settings | Standard method; the `settings.yaml` that `graphrag init` writes, plus one `api_base` line per model | runner, `measured.settings` |
| Documents | the first N of the 20 in [`documents.tsv`](../documents.tsv), article `body` only, one `.txt` each | corpus SHA-256 checked by the runner |
| Chunks | N=1: 2, N=5: 9, N=20: 47 (1,200-token chunks with 100 overlap in `o200k_base` tokens; 44,486 tokens in all at N=20) | GraphRAG's own `text_units` table |

GraphRAG indexes in batch, so N = 1, 5 and 20 are three separate runs from clean directories, not three readings of
one run.

## Results: shape B, N = 1, 5 and 20

Shape B is a plausible answer: per chunk 6 entities and 5 relationships, names taken deterministically from the
chunk's capitalised words so some repeat across chunks (exact definition at the end of this page). Each cell is calls
/ prompt tokens unless it says otherwise.

| | N=1 | N=5 | N=20 | Per chunk or corpus-level |
|---|---|---|---|---|
| Connectivity test the CLI makes first (chat) | 1 / 11 | 1 / 11 | 1 / 11 | once per run |
| Extraction, first call | 2 / 4,961 | 9 / 23,018 | 47 / 126,435 | per chunk |
| Gleaning continuation | 2 / 5,770 | 9 / 26,607 | 47 / 144,793 | per chunk |
| Gleaning loop-check | 0 | 0 | 0 | never called at the default of one gleaning |
| Entity description summaries | 1 / 160 | 5 / 792 | 51 / 8,414 | corpus-level |
| Relationship description summaries | 0 | 1 / 173 | 7 / 1,168 | corpus-level |
| Community reports | 3 / 6,344 | 4 / 8,449 | 54 / 119,943 | corpus-level |
| **Chat total: calls / prompt / completion** | **9 / 17,246 / 1,525** | **29 / 59,050 / 4,418** | **207 / 400,764 / 31,371** | |
| Embeddings, chunk text (calls / inputs / tokens) | 1 / 2 / 1,490 | 1 / 9 / 7,401 | 6 / 47 / 44,885 | per chunk |
| Embeddings, entity descriptions | 1 / 11 / 183 | 4 / 49 / 797 | 13 / 203 / 3,256 | corpus-level |
| Embeddings, community reports | 1 / 3 / 516 | 1 / 4 / 686 | 4 / 54 / 9,246 | corpus-level |
| Embeddings, 1-input test the CLI makes first | 1 / 1 / 9 | 1 / 1 / 9 | 1 / 1 / 9 | once per run |
| **Embeddings total: calls / inputs / tokens** | **4 / 17 / 2,198** | **7 / 63 / 8,893** | **24 / 305 / 57,396** | |
| Graph the stub's answers produced | 11 entities, 10 relationships | 49, 44 | 203, 228 | |
| Communities (= reports), by level 0 / 1 | 3 (3 / 0) | 4 (4 / 0) | 54 (16 / 38) | |
| Entities that sit in a level-0 community | 11 | 15 | 185 | |

Arithmetic from the table, not measured separately. Chat calls per document, leaving out the one connectivity test:
8.0 at N=1, 5.6 at N=5, 10.3 at N=20. Chat prompt tokens per document, same exclusion: about 17,235, 11,808 and
20,038. At N=20 the shares of chat prompt tokens are extraction plus gleaning 67.7%, summaries 2.4%, reports 29.9%.
These do not rise steadily with N: the chunk-level rows are exactly 2 calls per chunk (4, 18, 94), but the
corpus-level rows follow the graph the answers produced. At N=5 only 15 of 49 entities are in a community (GraphRAG
clusters the largest connected component only), so only 4 reports are written; at N=20, 185 of 203 are, in two levels,
so 54. A different answer shape gives different corpus-level rows, as the next table shows.

## Other response shapes, N = 20

| | Shape B (above) | Shape A: bare answers, no entities | Shape A2: same 2 entities, 1 relationship every chunk |
|---|---|---|---|
| Exit status | 0 | **1** (pipeline stops after extraction) | 0 |
| Chat calls / prompt tokens | 207 / 400,764 | 95 / 254,714 | 96 / 259,617 |
| Completion tokens as the stub counted | 31,371 | 472 | 3,639 |
| Extraction, first call | 47 / 126,435 | 47 / 126,435 | 47 / 126,435 |
| Gleaning continuation | 47 / 144,793 | 47 / 128,268 | 47 / 131,182 |
| Summaries (entity + relationship) | 51 + 7 | 0 | 0 |
| Community reports | 54 / 119,943 | 0 | 1 / 1,989 |
| Embedding inputs / tokens | 305 / 57,396 | 1 / 9 | 51 / 45,077 |

Shape A is the brief's "smallest valid answer". GraphRAG does not complete on it: with no entity in any chunk it logs
"Graph Extraction failed. No entities detected during extraction." and stops, having spent the 2 calls per chunk (94
calls) and the connectivity test. Shape A2 is an addition of mine, the smallest answer found that lets the run finish:
it gives a floor for the corpus-level rows (no summaries because every description is identical and so de-duplicates,
one community, one report). It is a bound, not a typical case.

What the three shapes show: the first extraction call's prompt (47 calls, 126,435 tokens) is identical under all three,
because it holds only the instructions and the chunk. The continuation call's prompt is not, because it carries the
first answer: 128,268, 131,182 or 144,793 tokens for the same 47 calls.

## Other checks

| Check | Result |
|---|---|
| Determinism: shape B, N=20, run twice from clean directories | Identical: calls by kind, prompt tokens, completion tokens, embedding calls, inputs and tokens, and the multiset of per-call prompt SHA-256 hashes. The comparison function was checked to flag a one-token change and a changed hash. The whole runner was also run four times; the printed totals of every run matched across invocations. |
| LLM cache on versus off (`--no-cache`), shape B, N=20 | Identical counts (207 chat calls, 400,764 prompt tokens): no two prompts repeat within a first run, so the cache saves nothing the first time. |
| Re-run of the same 20 documents from the cache the first run left | 1 chat call and 1 embedding input in all: the two connectivity tests. Every chat and embedding call was served from the cache. This is the effect of the cache on a retry or a repeat run with identical answers; it says nothing about a re-run where the model's answers differ. |
| Calls the stub could not classify | 0 in every run |
| Embedding calls split by field match the table row counts | yes in every run that reached embedding |

## Depends on what the model answers

| Count | Depends on the answers? |
|---|---|
| Extraction calls and their prompt tokens | No: 1 per chunk, fixed prompt of about 1,736 tokens plus the chunk (64.5% of the extraction input at N=20, arithmetic). |
| Gleaning continuation calls at the default | No: exactly 1 per chunk. Their prompt tokens do, because the first answer is in them. |
| Gleaning loop-check calls | None at the default. With `max_gleanings` of 2 or more, each continues only if the reply is exactly `Y`: 3 to 2g calls per chunk. |
| Summary calls | Yes: one per entity or relationship seen with two or more distinct descriptions anywhere in the corpus; more passes if their text exceeds 4,000 tokens. Under shape B all descriptions differ by chunk, which is an upper-leaning choice. |
| Community report calls | Yes: one per community at every level, from the graph the answers produced, largest connected component only. Prompts swap in sub-community reports if a community's rows exceed 8,000 tokens; never reached here (largest prompt 2,637). |
| Embedding inputs | Chunks: no. Entities and reports: yes. |
| Whether the run completes | Yes: no entity or no relationship in the whole corpus stops it (measured, shape A). |
| Retries | Failed calls are retried by the transport layer (up to 7 by its class default); an extraction call that still fails leaves that chunk with no graph and the run goes on. The stub never fails, so none of this ran. |
| Output tokens | Unmeasured. The client sets no `max_tokens` or temperature at these defaults (seen in the request bodies); the report length limit of 2,000 is text in the prompt only. |

## Licence

`LICENSE` in the installed `graphrag` 3.3.0 wheel (same file, same SHA-256 `c2cfccb8…5383`, in all eight packages) and
at tag v3.3.0, read 20261102 10:27 UTC: first lines "MIT License" and "Copyright (c) Microsoft Corporation." This
matches the entry (MIT, read 20261030). Caveats noticed, not chased: `litellm`, the model client it pulls in, has a
LICENSE that names a separate licence for an `enterprise/` directory and no such directory is in the installed
package; a scan of the declared metadata of all 139 installed distributions (10:38 UTC) names no GPL, AGPL,
commercial or non-commercial term, but reads metadata, not each file. No model weights are used here.

## Install, Apple Silicon, outbound

- **Install** worked first time: `uv pip install 'graphrag==3.3.0' tiktoken --only-binary :all:` exited 0, 139
  distributions, all wheels (arm64 or universal2 for the native ones: lancedb, graspologic-native, numpy, pandas,
  pyarrow, spacy, litellm), no source build, no compiler. **It runs on Apple Silicon**: all nine runs completed (the
  one with exit 1 is shape A, by design).
- **One workaround, outside GraphRAG:** tiktoken downloads its tables on first use, so they were fetched once by hand
  into a cache directory the runs read, otherwise a run with no network fails at chunking.
- **Outbound attempts:** exactly one seen: `CONNECT raw.githubusercontent.com:443`, made by LiteLLM at import to fetch
  its price table; it falls back to a bundled copy when refused (one warning line in every run's log).
  `LITELLM_LOCAL_MODEL_COST_MAP=True` switches it off; it was left unset so the attempt would show. No telemetry code
  was found in GraphRAG's eight packages. Every run also had a macOS `sandbox-exec` profile that denies all outbound
  connections except to loopback, which the runner tests before use (loopback connects, a documentation-range address
  gets `PermissionError`); `sandbox-exec` is deprecated by Apple but worked here.
- **The CLI makes two calls the pipeline does not:** a chat connectivity test and a one-string embedding test before
  indexing, each configured model (`--skip-validation` skips them). They are in the totals above and shown separately.

## Limits

- The stub answers instantly and never errs, so wall-clock time (about 5 to 26 seconds, GraphRAG's own processing),
  retries, rate limits and malformed replies are not tested. Real answer lengths, graph size, summary and report
  counts, report parse failures and quality are unmeasured.
- Shape B has 6 entities and 5 relationships per chunk because the brief asked for about that; a real model may name
  far more, and entity count drives the summary, report and entity-embedding rows.
- Not run: the Fast method, `graphrag update` (incremental), claim extraction, `max_gleanings` above 1, Python 3.11 or
  3.13, any query mode, and an Anthropic model through LiteLLM (including whether the `json_schema` response format
  the report step sends is accepted, and where embeddings would come from). Nothing was checked against either
  provider's current documentation.
- One document order and one corpus: the first N of the frozen 20. The N=1, 5, 20 rows are one draw each, not rates.

## Response shapes, exactly

- **B.** Extraction answer: the 6 capitalised words of the chunk (three or more letters, upper-cased) with the smallest
  SHA-256, as entities; the type is one of the four default types chosen from the hash of the name; the description
  is "NAME is discussed in passage" plus the chunk's SHA-256 prefix. The 5 relationships chain the 6 entities in hash
  order with a weight of 5 to 9 from the hash of the pair, and descriptions carrying the same prefix. The format and the
  closing marker follow the prompt's own examples. Gleaning answer: the completion marker only. Loop-check: `N`.
  Summary: one fixed sentence. Report: one fixed-size JSON report with 5 findings, titled from a hash of the prompt.
- **A.** Extraction and gleaning answers are the bare completion marker; the connectivity test answers "Hello World".
- **A2.** Every extraction answer is the same 2 entities (identical descriptions) and 1 relationship; gleaning is the
  completion marker; reports as in B.

## Re-run

```
SCRATCH=<a scratch directory>; ENV=$SCRATCH/microsoft-graphrag        # the corpus is $SCRATCH/exp-data/corpus.json
uv venv --python 3.12 $ENV/venv
uv pip install --python $ENV/venv/bin/python 'graphrag==3.3.0' tiktoken --only-binary :all:
mkdir -p $ENV/home $ENV/tiktoken_cache
env -i PATH=/usr/bin:/bin HOME=$ENV/home TIKTOKEN_CACHE_DIR=$ENV/tiktoken_cache \
  $ENV/venv/bin/python -I -c "import tiktoken; tiktoken.get_encoding('o200k_base'); tiktoken.get_encoding('cl100k_base')"   # needs network, once
env -i PATH=/usr/bin:/bin:/opt/homebrew/bin HOME=$ENV/home $ENV/venv/bin/python -I tools/exp/x2_microsoft_graphrag.py \
  --corpus $SCRATCH/exp-data/corpus.json --documents kb-kg/experiments/x2-index-cost/documents.tsv \
  --workdir $ENV/work --tiktoken-cache $ENV/tiktoken_cache \
  --out kb-kg/experiments/x2-index-cost/rehearsal/microsoft-graphrag.json
```

About 3 minutes. The runner rewrites the `measured` key of the JSON and keeps the `hand_recorded` key. Article text
exists only under `--workdir`.
