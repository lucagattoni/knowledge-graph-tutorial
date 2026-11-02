# X2 rehearsal: fast-graphrag against a stub model

**Run 20261102 10:48 UTC (Step 0, part d). A stub stood in for the model: no key, no model, no money, no outbound
network.** Background on the project: [`fast-graphrag` entry](../../../projects/fast-graphrag.md) (a lead, re-checked
below). Runner: [`tools/exp/x2_fast_graphrag.py`](../../../../tools/exp/x2_fast_graphrag.py). Machine-readable results:
[`fast-graphrag.json`](fast-graphrag.json). Documents: the 20 in [`documents.tsv`](../documents.tsv) (191,571
characters). The article text is in no file here.

**Token counts are the stub's own** (tiktoken `cl100k_base`), not any provider's. The library itself looks up the
tokenizer for `gpt-4o-mini` (its default model), which is a different one (`o200k_base`, from the library's own log
line). A count here is a count *for the stub's answers*; the shapes are defined below.

## What was pinned and installed

| Item | Value | Source, read (UTC) |
|---|---|---|
| Pinned code | Commit `23b3a1bef64338faf9f35c521a20465dbd09419f` of `main`, committed 2025-11-01T20:45:24Z, version string 0.0.5 | GitHub API `commits` and `pyproject.toml`, 20261102 10:27 |
| Why a commit | No GitHub release or tag (both lists empty). Latest PyPI release is 0.0.5, uploaded 2025-04-04T08:16:22Z, about 19 months before the read; `pushed_at` is 2025-11-01T20:45:25Z, `archived` false | GitHub API and `pypi.org/pypi/fast-graphrag/json`, 20261102 10:27 (PyPI re-read 10:43) |
| PyPI 0.0.5 vs the commit | Also installed and run. Its `fast_graphrag/` differs in one file, `_graphrag.py` (the query path, an optional `response_model` argument). Every indexing file is byte-identical. The same runner gave identical calls by kind, prompt tokens and embedding requests and inputs in all nine runs | `diff -rq` 20261102 10:35; re-run 10:40 (output kept in scratch) |
| Python, OS | CPython 3.12.16 (the package allows `>=3.10,<3.13`), macOS arm64 | `pyproject.toml`, PyPI metadata; installed environment |
| Install | `uv` 0.13.6, 120 packages resolved, about 6 s. Binary wheels for everything except `hnswlib` 0.8.0, built from its source distribution with the Xcode command line tools' compiler, no workaround. No failure | install log, 20261102 10:28 |
| Dependencies | The package requires the `google-genai`, `vertexai` and `voyageai` SDKs and `sentencepiece` whether or not they are used | `pyproject.toml` at the commit |

## Licence

`LICENSE` at the pinned commit: first lines "MIT License", then "Copyright (c) 2024 circlemind-ai"; SHA-256
`1774ff2102ad79d99d731ed90e1f64116695115133efd78c29a73d2939033875`. The copy in the installed distribution
(`dist-info/licenses/LICENSE`) is byte-identical, and so is the one in the PyPI 0.0.5 wheel (read 20261102 10:28 to
10:36). **It matches the entry** (MIT, copyright line "2024 circlemind-ai"). PyPI's own `license` field is `null` and its
classifiers name no licence (read 10:43), so the PyPI page alone would not show it. Not chased: the licences of the 119
dependencies.

## The numbers

Shape B is the plausible answer; A1 is the smallest answer the library can finish on; BL is B with longer entity
descriptions. All three are 20 documents indexed one at a time into one working directory (a fresh one per run); rows
are cumulative after N documents. Calls are chat calls: `x + y` means x extraction calls plus y description-summary
calls. Completion tokens are the stub's count of its own answers, so they price nothing. Embedding tokens are summed
per input.

| Shape | N | Chat calls | Prompt tokens | Completion tokens (stub's) | Embedding requests | Embedding inputs | Embedding tokens |
|---|---|---|---|---|---|---|---|
| B | 1 | 3 | 6,831 | 932 | 1 | 17 | 317 |
| B | 5 | 15 | 34,125 | 4,670 | 5 | 73 | 1,424 |
| B | 20 | **80** | **187,783** | 24,704 | 21 | 374 | 7,737 |
| A1 | 1 | 3 | 6,831 | 93 | 1 | 1 | 13 |
| A1 | 5 | 15 | 34,125 | 465 | 5 | 5 | 93 |
| A1 | 20 | 80 | 187,783 | 2,480 | 20 | 20 | 970 |
| BL | 1 | 3 | 6,831 | 1,545 | 1 | 17 | 929 |
| BL | 5 | 15 + 2 | 34,704 | 7,877 | 5 | 73 | 4,372 |
| BL | 20 | 80 + 41 | 199,771 | 43,309 | 21 | 374 | 22,049 |

Arithmetic from the table and the JSON, not separate measurements:
- 80 chunks from 191,571 characters, so 2,395 characters per chunk; 4.0 extraction calls per document (range 2 to 9).
  Extraction calls equalled the library's own chunk count in every document of every run.
- 2,347 prompt tokens per extraction call (187,783 / 80). The chunk text alone is 46,421 tokens (580 per call), so
  about 1,767 per call is fixed: instructions, one worked example and the JSON schema that the `instructor` layer adds
  to the system message.
- A summary call is about 292 prompt tokens (11,988 / 41, BL). One edge-grouping call over 18 facts was 615 prompt tokens
  (probe E6 below).
- 18.7 embedding inputs per document (374 / 20; range 10 to 38). Batches hold at most 32 inputs, so document 16 (38
  inputs) took 2 requests and every other one took 1 (checked in every document of the B run).

**Shapes, exactly.** B: for each chunk, the first six distinct capitalised words of at least four letters that do not
also occur in lower case in that chunk are the entities (6 per chunk in all 80 chunks), entity i has type
`ENTITY_TYPES[i mod 5]` and the description "NAME is discussed in the passage." (about 35 characters), and
relationship i links entity i to entity i+1 (5 per chunk). A summary request is answered with the first 256
characters of the text it was asked to summarise; an edge-grouping request with no groups. A1: one entity per chunk
(name ENTITY, description "."), no relationships. BL: B with 200-character descriptions. The library's three user-side
strings were: a domain sentence for news articles, three generic example queries, and five entity types
(Organization, Person, Product, Place, Event); they are in the JSON. They change prompt size, and the library has no
defaults for them.

### Probes (small, to check the reading of the code; not defaults)

| Probe | Documents | Result |
|---|---|---|
| Shape A: no entities, no relationships (the smallest valid answer) | 1 | 3 extraction calls, 6,831 prompt tokens, then **`insert` raises** `RuntimeError: Wrong dimensionality of the vectors` (an empty entity list reaches the vector index as a one-dimensional array). No embedding request. This is why A1 exists |
| E6: two entities and six relationships between them in every chunk | 1 | 3 extraction calls and **1 edge-grouping call** (615 prompt tokens, 18 facts); 18 relations stored |
| Gleaning set to 1, and to 2 (`max_gleaning_steps`) | 1 each | **No extra call in either: 3 calls, the same as the default.** Each chunk logs `Error during gleaning: 'domain'`: the continuation prompt is formatted with no arguments, and its system text needs `{domain}` (a `KeyError`, checked directly). The error is caught, so the first extraction is kept |
| An answer that is not JSON | 1 | 9 calls for 3 chunks (6 are retries, 3 attempts per call), 24,294 prompt tokens (3.6 times the 6,831 of valid answers: each retry resends the failed answer and an error message). Then the document is **dropped without an exception**: 0 entities, 0 chunks stored. The run took about 9 s against about 2 s for the others: the retry wait |

## How indexing is structured (read from the installed source, 20261102 10:28 to 10:34 UTC)

`GraphRAG.insert` per document: chunk, drop chunks already stored, one extraction call per new chunk (all chunks of a
document at once), merge the chunk graphs into a per-document graph, then merge that into the main graph, then embed the
entities that were upserted, then link near-duplicate entities, then store the chunks.

| Piece | Reading | Depends on the model's answers? |
|---|---|---|
| Chunking | Windows of 800 "tokens" times `TOKEN_TO_CHAR_RATIO` = **4** (`_utils.py`) = 3,200 characters, overlap 100 times 4 = 400. A text no longer than one window stays whole. Measured chunk sizes 292 to 3,191 characters. The entry had the ratio as unstated | No |
| Extraction | One chat call per chunk, `response_format` JSON object, 2 messages (system, user), the schema appended by `instructor`. No `temperature`, no `max_tokens` | The count: no. Up to 3 attempts per call if the answer cannot be parsed (measured) |
| Description summary | A call when a merged entity description exceeds 512 characters. Both the per-document merge and the main-graph merge can trigger it. Sent with `max_tokens: null` | **Yes.** 0 calls with B (35-character descriptions), 41 with BL (200 characters) |
| Edge grouping | A call per entity pair when the existing plus new edges between them exceed 5 | **Yes.** 0 calls in B and A1; 1 in E6 |
| Gleaning | Off by default (`max_gleaning_steps` 0). Turning it on sends no extra call here (probe above). The entry reads "2n calls per chunk"; that does not happen at this commit | n/a |
| Embeddings | Only upserted entities, text `[TYPE] NAME` plus the description, `text-embedding-3-small`, 1,536 dimensions sent, 32 inputs per request, requests in parallel; chunks are never embedded | **Yes** (how many distinct entity names): 374 inputs with B, 20 with A1 |
| Identity edges | The 3 nearest entities are looked up and an "is" edge is added above similarity 0.9; no model call | No call. The stub's vectors are hash-derived, so none was added (400 relations = 5 per chunk times 80 chunks) |
| Defaults seen | LLM `gpt-4o-mini`; embedding `text-embedding-3-small`; LLM concurrency limit 1,024 (`CONCURRENT_TASK_LIMIT`); embedding limiter 500 requests per minute; OpenAI SDK default of 2 retries on top of the library's 3 attempts | n/a |

## Outbound attempts

The runner starts each run in a child process with an empty environment plus a dummy key, `HTTP_PROXY`, `HTTPS_PROXY`
and `ALL_PROXY` pointing at a closed port (`http://127.0.0.1:9`) and `NO_PROXY=127.0.0.1,localhost`. Inside the child a
guard records every name lookup or connection beyond loopback and refuses it, and records connections to the closed
proxy port.
- **One attempt per run, nine in nine runs, all the same:** at start-up the library calls
  `tiktoken.encoding_for_model("gpt-4o-mini")`, which tries to download `o200k_base.tiktoken` from
  `openaipublic.blob.core.windows.net`. It went to the closed proxy port and failed; the library logged "failed to load
  tokenizer ... Falling back to naive tokenization". Nothing on the indexing path calls the tokenizer (`count_tokens`
  has no caller in the package), so the counts are unaffected. With a network the file would be fetched once.
- **No other attempt and no telemetry seen.** The guard sees Python-level connections only.
- Setup note: the stub's own tokenizer file (`cl100k_base`) was fetched once by me, outside any builder run, into a
  cache directory the runner is pointed at. Without it the stub falls back to characters / 4 and says so.

## Determinism

Shape B was run twice, in separate processes and fresh working directories, the hash seed not fixed. **Identical:** calls
by kind, prompt tokens, completion tokens, embedding requests, inputs and tokens, all 20 per-document rows, the multiset
of the 101 prompt hashes (80 + 21 embedding requests), and the graph totals (349 entities, 400 relations, 80 chunks).
The comparison was tested to turn red: it reports a difference for B against A1 and BL, and for B with one prompt token
altered in one document.
In BL, where concurrent summary calls are in play, chat calls and prompt tokens were identical in 8 runs (the runner's
own run on each of two installs, and 6 further runs of the child process). The stub's embedding token count moved by 1 (22,326 or 22,327): the stub counts a request as one
newline-joined text, and the order of entities inside a batch follows which summary call returns first. The per-input
sum (22,049) did not move.

## What a stub cannot tell (unmeasured)

- Output tokens of real answers; the stub's completion counts are its own.
- How long a real model's entity descriptions are, hence how many summary calls a real graph triggers: 0 and 41 above
  are two assumptions, not a range. The same holds for edge-grouping calls, which need more than 5 edges on one pair.
- How often a real model's answer fails to parse (each failure costs up to 3 calls and, after the third, the
  document is lost without an error).
- Provider errors: the stub always answers 200, so the OpenAI SDK's retries on 429 or 5xx and the library's nested
  attempts were not exercised. The SDK's retry log lines counted 0.
- Identity edges, query-time calls and quality. Entity-name repeats across documents are far rarer under B than a
  real corpus would give (349 distinct names from 480 mentions).
- Whether the request shape (`response_format` JSON mode on every chat call, `max_tokens: null` on summary calls)
  works through a provider's OpenAI-compatibility layer: not checked against any provider's documentation.
- The licences of the dependencies, and whether the project is maintained (the entry's subject, not this page's).

## Re-run

From the repository root, with `$SCRATCH` any scratch directory and `CORPUS` the MultiHop-RAG `corpus.json` whose
SHA-256 is pinned in [`documents.tsv`](../documents.tsv) (the runner refuses another):

```
uv venv --python 3.12 $SCRATCH/venv
git clone https://github.com/circlemind-ai/fast-graphrag $SCRATCH/src
git -C $SCRATCH/src checkout 23b3a1bef64338faf9f35c521a20465dbd09419f
uv pip install --python $SCRATCH/venv/bin/python $SCRATCH/src
TIKTOKEN_CACHE_DIR=$SCRATCH/tiktoken-cache $SCRATCH/venv/bin/python -c "import tiktoken; tiktoken.get_encoding('cl100k_base')"
mkdir -p $SCRATCH/home
env -i PATH=/usr/bin:/bin:/opt/homebrew/bin HOME=$SCRATCH/home $SCRATCH/venv/bin/python tools/exp/x2_fast_graphrag.py \
  --corpus $CORPUS --documents kb-kg/experiments/x2-index-cost/documents.tsv \
  --out kb-kg/experiments/x2-index-cost/rehearsal/fast-graphrag.json --scratch $SCRATCH/run \
  --source-dir $SCRATCH/src --tiktoken-cache $SCRATCH/tiktoken-cache
```

It takes about 30 s and exits 1 if any run's process fails. `$SCRATCH/run` must not exist. The text-bearing debug logs
(`calls_with_text_DEBUG.jsonl` per run) stay under `$SCRATCH/run/runs/`.
