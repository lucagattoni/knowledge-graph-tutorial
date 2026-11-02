# X2 rehearsal: LightRAG indexing against a stub model

**Status: Step 0 groundwork. No model was called and no key was used.** This page counts what LightRAG's *indexing*
sends to a model and to an embedding endpoint when it indexes the 20 frozen [X2 documents](../documents.tsv), with a
loopback stub answering. Machine-readable results: [`lightrag.json`](lightrag.json). Runner:
[`tools/exp/x2_lightrag.py`](../../../../tools/exp/x2_lightrag.py). Read and run 20261102 10:27 to 10:38 UTC.

## What was pinned

| Item | Value | Source (read UTC) |
|---|---|---|
| Package | `lightrag-hku` 1.5.7, from the wheel on PyPI | PyPI JSON, uploaded 20260902 07:24 (read 20261102 10:27) |
| GitHub release | v1.5.7, published 20260902 07:23; tag commit `28ff1b05f2ac3f3e6fa14dd2cd33656579bd0c9c` | GitHub releases API and ref API (read 20261102 10:27) |
| Why not newer | It is the latest stable release; the head of `main` (`aaebfe1b`, 20261014 14:55) is newer but unreleased, and was not used | GitHub commits API (read 20261102 10:35) |
| Python | 3.12.16 (uv-managed CPython), arm64, macOS | `uv venv --python 3.12`, 20261102 10:27 |
| Other versions | openai 3.42.1, tiktoken 0.14.0, nano-vectordb 0.0.4.3, networkx 3.7, numpy 2.5.4, tenacity 9.1.4, pipmaster 1.2.2 | `lightrag.json` (`dependency_versions`) |
| Stub tokenizer | tiktoken `cl100k_base`. Not any provider's tokenizer; LightRAG's own chunker counts with `o200k_base` | `lightrag.json` |

## Licence

The `LICENSE` file at tag v1.5.7 and the one shipped in the wheel are byte-identical (SHA-256
`0c16924564059e493c86854574660a47ed1dcc2a476ba7b5f949d3f2f73a1984`, read 20261102 10:35 UTC). Its first lines are
"MIT License" and "Copyright (c) 2025 LightRAG Team". This matches the [entry](../../../projects/lightrag.md) (MIT, read
20261030). Caveats noticed, not chased: `tiktoken` fetches its vocabulary files from OpenAI's storage at first use and
their terms were not checked; the other 62 installed packages were not audited for licence.

## The numbers

Documents were indexed one at a time with `LightRAG.ainsert`, awaited in turn, into one working directory. The stub's
totals were read after 1, 5 and 20 documents. Defaults were used throughout (read from the constructed object): fixed-token
chunks of 1,200 tokens with 100 overlap, gleaning 1, 4 concurrent model calls, embedding batches of 10, JSON extraction
mode off. "Chat prompt tokens" are the stub's cl100k counts of everything sent in the request.

| Run | Docs | Chunks | Extraction calls | Gleaning calls | Summary calls | Chat calls | Chat prompt tokens | Embedding calls | Embedding inputs (chunks / entities / relations) | Embedding tokens |
|---|---|---|---|---|---|---|---|---|---|---|
| Shape B | 1 | 2 | 2 | 2 | 0 | 4 | 11,558 | 3 | 20 (2 / 9 / 9) | 1,969 |
| Shape B | 5 | 9 | 9 | 9 | 0 | 18 | 53,448 | 15 | 91 (9 / 41 / 41) | 9,590 |
| Shape B | 20 | 49 | 49 | 49 | 0 | 98 | 299,901 | 80 | 497 (49 / 223 / 225) | 56,967 |
| Shape A | 1 | 2 | 2 | 2 | 0 | 4 | 10,780 | 1 | 2 (2 / 0 / 0) | 1,490 |
| Shape A | 5 | 9 | 9 | 9 | 0 | 18 | 49,902 | 5 | 9 (9 / 0 / 0) | 7,400 |
| Shape A | 20 | 49 | 49 | 49 | 0 | 98 | 281,020 | 20 | 49 (49 / 0 / 0) | 44,957 |
| Probe H (not a shape) | 20 | 49 | 49 | 49 | 6 | 104 | 307,049 | 91 | 552 (49 / 243 / 260) | 59,483 |

- **Shape A** is the smallest valid answer: the completion delimiter only, so no entities and no relations, for both
  the extraction and the gleaning call.
- **Shape B** is a plausible answer. From each chunk, the 6 most frequent capitalised words that do not start a sentence
  (ties by first appearance; padded with the most frequent long lowercase words if fewer than 6) become 6 entities of
  one of six types (by a hash of the name), and consecutive pairs of them become 5 relations. Descriptions are one fixed
  sentence per item that includes the chunk's word count. The gleaning call is answered with the delimiter only
  ("nothing missed"), so the extraction answer is the whole result. A summary call, if one is made, is answered with one
  fixed sentence. The responder was written once and not tuned. The resulting graph has 207 entities and 224
  relations (stored sizes; the most-shared entity appears in 4 chunks).
- **Probe H** is shape B plus one extra entity (`Hubentity`) and one relation to it in every chunk. It exists only to
  show the summary-on-merge path working and being counted; it is not a prediction of what a real model's graph does.
  In one execution, all 6 summary calls were for that one entity (read from the working directory's cache).
- **Deterministic.** B1 and B2 are the identical 20-document shape-B run from two clean working directories. Calls by
  kind, prompt tokens by kind, embedding calls and inputs by kind, the per-document breakdown and the stored sizes are
  equal at N = 1, 5 and 20, and so is an order-free fingerprint of all 98 + 80 calls (path, prompt hash, token counts).
  B1 and B2 gave the same fingerprint in each of two full executions of the driver (four shape-B runs in all).
- **One determinism caveat, seen only in the probe.** Five executions of probe H gave identical call counts and token
  totals every time but three different call fingerprints. Of the executions I compared call by call, the one call that
  differed was an embedding call of 8 inputs and 162 tokens: same size, different text. The cause was not traced. Descriptions are
  ordered by an integer-seconds timestamp (`operate.py`, `_merge_nodes_then_upsert`), so ordering that depends on the
  clock is a hypothesis; it was not tested.

Arithmetic from the table (not measured separately): 98 chat calls for 49 chunks is exactly 2 per chunk when no summary
fires. Mean chat prompt tokens per chunk: 5,735 in shape A and 6,120 in shape B. Total chat prompt tokens are 6.25 times
(A) and 6.67 times (B) the 44,957 tokens of chunk text. The fixed part of an extraction call is the system prompt
(1,497 tokens) plus the user-prompt template (252), 1,749 tokens before the chunk text (measured by formatting the
shipped default prompts and counting them with the stub's tokenizer); the gleaning call repeats that, the first answer
and a 397-token continue prompt. Mean chunk text is 917 tokens (cl100k) in this corpus.

## What depends on the model's answers, and what does not

| Item | Depends on the model? | What the code and the runs show |
|---|---|---|
| Number of chunks | No | Fixed-token chunker; 49 chunks from 20 documents |
| Initial extraction calls | No | Exactly 1 per chunk |
| Gleaning calls | Almost no | Exactly 1 per chunk, even when the first answer was empty (shape A). In 1.5.7 the gleaning setting is on or off, not a count: `operate.py` lines 4217 to 4218 run one pass if it is above 0, and a run with `MAX_GLEANING` 1, 2 and 3 gave 2 gleaning calls each for the first document's 2 chunks. It is skipped only if its input would exceed `MAX_EXTRACT_INPUT_TOKENS` (20,480; `operate.py` line 4247), which needs a very large first answer, or if the same prompt is already in the cache |
| Gleaning prompt size | Yes | It contains the first answer (shape A 3,069 tokens a call on average, shape B 3,454) |
| Summary calls on merge | Yes, entirely | `_handle_entity_relation_summary` (`operate.py` line 372) calls the model only when an entity or relation has 8 or more description fragments (`force_llm_summary_on_merge`) or its descriptions total 1,200 or more tokens, and in several map-reduce rounds above 12,000 tokens. Shape B made none (no entity in more than 4 chunks); probe H made 6. A real model's descriptions are longer and its entities repeat differently, so this count is unmeasured |
| Entity and relation embedding inputs | Yes | Vectors are buffered and embedded when the document's storage is flushed, in batches of 10 with up to 8 in flight, so an entity touched by 3 documents is embedded 3 times (223 inputs for 207 stored entities in shape B). Chunk embeddings (49 inputs) do not depend on answers |
| Retries | Yes | The OpenAI binding retries up to 3 attempts on rate limits, 5xx, timeouts and empty responses (`llm/openai.py`, tenacity `stop_after_attempt(3)`); a retry is an extra request the logical counts above do not show |
| Cache hits | Input-dependent | Calls are keyed by prompt hash; a repeated prompt, or re-indexing in the same working directory, makes no call. The runs therefore start from clean directories |
| Malformed answers | Yes | A record with the wrong number of fields is dropped with a warning; nothing is asked again |
| Output tokens, quality | Yes | The stub's completion token counts are for its own answers and are not a measurement of any model |

## Install, run and outbound findings

- **Install worked on Apple Silicon.** `uv pip install --only-binary :all: lightrag-hku==1.5.7 tiktoken` installed 58
  packages, all from wheels, with no source build; the native modules (numpy) are arm64. All four scenarios together
  took 12 s on the stub (20261102 10:36:58 to 10:37:10 UTC).
- **Workaround 1: `openai` is not a base dependency.** The base install lists `openai` only under the `api` extra, but
  `lightrag/llm/openai.py` imports it and, if it is missing, runs `pip install openai` itself through `pipmaster`
  (lines 11 to 13). I installed `openai` first (5 more packages) so no package was installed at run time. The same
  pattern is in the other provider bindings (for example `anthropic.py`, which installs `anthropic` on demand; not run).
- **Workaround 2: tiktoken needs its vocabulary files.** Without a cache and with the dead proxy, `get_encoding` failed
  with a `ProxyError` naming `openaipublic.blob.core.windows.net`. The two vocabularies were downloaded once with network
  access on 20261102 10:30 UTC into a cache directory named by `TIKTOKEN_CACHE_DIR`, which the runs then used offline.
- **Outbound attempts during the runs: none.** The runs used a minimal environment with `HTTP_PROXY` and `HTTPS_PROXY`
  pointing at a closed local port and `NO_PROXY=127.0.0.1,localhost`; LightRAG was pointed at the stub through its own
  `OPENAI_API_BASE` setting with a dummy key. A Python audit hook recorded every socket connection and name lookup
  that was not to the stub: none in any of the four scenarios. A self-test connect to the closed port was recorded in
  every worker, so the hook does fire. Each run started 3 or 4 subprocesses, all `uname` or `file`, called from `platform`
  inside the OpenAI client (for its platform headers); no `pip`. LightRAG's Langfuse tracing turns on only if two Langfuse
  environment variables are set (`llm/openai.py`); they were not.
- **Provider note (a lead, not run).** LightRAG ships native chat bindings including `llm/anthropic.py`; its
  `anthropic_embed` is a deprecated alias that forwards to Voyage AI, so an Anthropic-only run would still need an
  embedding provider. For X2's gateway question this means an OpenAI-protocol path (used here) exists without a
  translation layer; the Anthropic path was only read, not tried.

## Corrections the entry may want

The [LightRAG entry](../../../projects/lightrag.md) says extraction makes "up to `entity_extract_max_gleaning` further
'please continue' calls per chunk". In 1.5.7 it makes at most one, whatever the setting (see the table above). At the
default of 1 the entry's "N to 2N calls for N chunks" holds, and the rehearsal measured exactly 2N for N = 49. The entry
also said the default chunking strategy was unstated: for `ainsert` it is fixed-token (the method's own docstring).
The server path chooses a strategy per document and its default was not read.

## Limits

- One shape-B responder written once, and one machine. Counts that depend on answers are counts for these answers only.
- Not rehearsed: query-time calls; the server and WebUI path (`max_parallel_insert` of 3 would index documents in
  parallel, which could change merge order and summary counts); the recursive, vector-semantic and paragraph chunkers
  (the vector one embeds during chunking); JSON extraction mode; any storage other than the default JSON, NanoVectorDB
  and NetworkX files; multimodal analysis (no model calls from it appeared for plain text).
- Prompt-token counts are the stub's tiktoken counts, not a provider's. Relation-description summaries were never
  triggered in any run. The other 62 installed packages and the vocabulary files were not licence-checked.
- The per-call dumps (hashes and sizes only, no text) stay in the scratch directory; `lightrag.json` carries their
  fingerprints.

## Run it again

The runner needs the environment below (paths are placeholders: `$SCRATCH` is any scratch directory, `$CORPUS` the
pinned `corpus.json` whose SHA-256 the runner checks).

```
uv venv --python 3.12 $SCRATCH/venv
uv pip install --python $SCRATCH/venv/bin/python --only-binary :all: lightrag-hku==1.5.7 tiktoken 'openai>=2.0.0,<4.0.0'
mkdir -p $SCRATCH/home/tmp $SCRATCH/tiktoken-cache
TIKTOKEN_CACHE_DIR=$SCRATCH/tiktoken-cache $SCRATCH/venv/bin/python -I -c "import tiktoken; [tiktoken.get_encoding(n) for n in ('o200k_base','cl100k_base')]"   # needs network, once
env -i PATH=/usr/bin:/bin:/opt/homebrew/bin HOME=$SCRATCH/home TMPDIR=$SCRATCH/home/tmp \
  TIKTOKEN_CACHE_DIR=$SCRATCH/tiktoken-cache HTTP_PROXY=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 \
  NO_PROXY=127.0.0.1,localhost \
  $SCRATCH/venv/bin/python -I tools/exp/x2_lightrag.py --corpus $CORPUS \
  --documents kb-kg/experiments/x2-index-cost/documents.tsv \
  --out kb-kg/experiments/x2-index-cost/rehearsal/lightrag.json --workroot $SCRATCH/work
```
