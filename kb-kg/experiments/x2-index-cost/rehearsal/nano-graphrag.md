# X2 rehearsal: nano-graphrag indexing against a stub model

**Step 0 of the [order and gates](../../README.md#order-and-gates). No model, no key, no money.** The 20 frozen X2 documents
([`documents.tsv`](../documents.tsv)) were indexed with nano-graphrag at its default settings while a loopback stub
([`tools/exp/stub_llm.py`](../../../../tools/exp/stub_llm.py)) answered in place of the model. The runner is
[`tools/exp/x2_nano_graphrag.py`](../../../../tools/exp/x2_nano_graphrag.py); every figure below is in
[`nano-graphrag.json`](nano-graphrag.json). Final run 20261102 10:45 UTC. Neither file holds article text.

Token counts are the stub's own: tiktoken `cl100k_base`, not any provider's. The builder itself chunks with `o200k_base`.
A count taken here is a count for the stub's answers; what depends on a real model is listed below.

## Build pinned

| What | Value | Source, read (UTC) |
|---|---|---|
| Build run | PyPI `nano-graphrag` 0.0.8.2, uploaded 20241019 13:06 UTC | `https://pypi.org/pypi/nano-graphrag/json`, 20261102 10:27 |
| Latest GitHub release | v0.0.8, 20241001 16:00 UTC (tag `cddcda71`) | `gh api repos/gusye1234/nano-graphrag/releases`, 20261102 10:27 |
| Head of `main` | `acb35c0`, 20260127 07:50 UTC, 22 commits after v0.0.8 | clone, `git log v0.0.8..HEAD`, 20261102 10:29 |
| 0.0.8.2 against v0.0.8 | Same files except the version string and the optional DSPy extractor (`entity_extraction/extract.py`, `module.py`). The v0.0.8 tag itself was not run | `cmp` against the tag, 20261102 10:29 |
| 0.0.8.2 against `main` | Byte-identical to main at `c061781` (20241010) except the `__version__` line; main's head differs in 9 files | `cmp`, 20261102 10:29 |
| Python | 3.12.16, macOS arm64 | `uv venv --python 3.12` |

## Licence

`LICENSE` in the installed distribution, at the v0.0.8 tag and at `acb35c0` is the same file (SHA-256
`e76d815c...2d959cd9`, 21 lines). It begins `MIT License`, blank, `Copyright (c) 2024 Gustavo Ye`. This matches the
[entry](../../../projects/nano-graphrag.md) (MIT, 21 lines, 2024), read 20261102 10:29 UTC. Caveats, not chased: the
dependencies' own metadata (not their `LICENSE` files) states Apache-2.0, MIT, BSD or similar for each direct dependency,
and states none for `hnswlib`. The default models are OpenAI-hosted (gpt-4o, gpt-4o-mini, text-embedding-3-small); their
terms were not read. No model weights are installed.

## Install on Apple Silicon

- **Pinned build, Python 3.12: installs and runs, no workaround.** `uv pip install nano-graphrag==0.0.8.2`, exit 0, 100
  packages, and uv printed no build step. `hnswlib` is sdist-only on PyPI; the installed copy is a locally built cp312
  arm64 wheel that uv took from its cache (where that entry came from is unstated). I chose 3.12 because `graspologic`
  3.4.4 declares `<3.13`; I did not check the other dependencies' bounds.
- **Python 3.13.18:** the install also exited 0 and the import works, with `hnswlib` and `numpy` 1.26.4 built from source.
  uv installed `graspologic` although its metadata says `<3.13`; why was not investigated. No scenario was run on 3.13.
  3.14 and 3.15 were not tried.
- **Head of `main` does not import after a clean install.** `nano_graphrag/_utils.py` line 17 has an unconditional
  `from transformers import AutoTokenizer`, and `transformers` is not in `requirements.txt`: `ModuleNotFoundError`.
  After `uv pip install transformers` (5.22.1) it runs; the head-of-main rows below used that.
- **One setup step:** the builder asks tiktoken for the `gpt-4o` vocabulary when it chunks, and tiktoken downloads it
  on first use. I fetched it once, before the offline runs, into a cache directory. The runs made no download.

## Numbers (shape B unless stated; documents inserted one at a time into one working directory)

Shape A, the smallest valid answer: extraction and the gleaning prompt answer `<|COMPLETE|>` (no entities, no relations).
Shape B: per chunk the 6 most frequent words that start with a capital letter, are at least 3 letters long and follow a
lowercase letter, comma, semicolon or colon plus one space (ties alphabetical; padded with hash-named items if fewer than
6) become entities of one of the four default types (chosen by a hash of the name), each with a one-sentence description
of about 30 tokens holding the chunk's first 12 words; 5 relations join entity i to i+1; the gleaning prompt answers
`<|COMPLETE|>`. So a chunk yields 6 entities and 5 relations (the builder's own progress line showed 294 and 245 for 49
chunks). Summary answers are fixed text and a loop check answers `NO`. Report answers are a fixed JSON with 5 findings. Runner header
has the full rule.

Columns: chat calls; calls by kind extraction / gleaning "continue" / description summary / community report; chat prompt
tokens; chat completion tokens (the stub's own text); embedding calls / inputs / tokens; graph nodes / edges / nodes in
the largest connected component / community reports stored. All measured, from the stub and the builder's storage.

| Case | Chat | Ext / cont / summ / report | Prompt tok | Compl. tok | Emb calls / inputs / tok | Graph |
|---|---|---|---|---|---|---|
| B, N=1 | 7 | 2 / 2 / 0 / 3 | 17,930 | 1,810 | 1 / 10 / 494 | 10 / 10 / 10 / 3 |
| B, N=5 | 21 | 9 / 9 / 0 / 3 | 60,948 | 5,858 | 5 / 43 / 2,137 | 43 / 44 / 10 / 3 |
| **B, N=20** | **146** | 49 / 49 / 0 / 48 | **421,152** | 38,504 | 20 / 234 / 12,202 | 224 / 234 / 110 / 29 |
| A, N=1 | 4 | 2 / 2 / 0 / 0 | 10,758 | 20 | 0 / 0 / 0 | none |
| A, N=5 | 18 | 9 / 9 / 0 / 0 | 49,798 | 90 | 0 / 0 / 0 | none |
| **A, N=20** | **98** | 49 / 49 / 0 / 0 | **280,428** | 490 | 0 / 0 / 0 | none |
| B, N=20, response cache off | 259 | 49 / 49 / 0 / 161 | 678,182 | 61,556 | 20 / 234 / 12,202 | 224 / 234 / 110 / 29 |
| B, N=20, one insert call for all 20 | 127 | 49 / 49 / 0 / 29 | 375,812 | 34,628 | 7 / 224 / 11,695 | 224 / 234 / 110 / 29 |
| B, N=20, head of `main` (`acb35c0`) | 146 | 49 / 49 / 0 / 48 | 421,152 | 38,504 | 20 / 234 / 12,202 | 224 / 234 / 110 / 29 |
| B, one insert, head of `main` | 127 | 49 / 49 / 0 / 29 | 375,812 | 34,628 | 7 / 224 / 11,695 | 224 / 234 / 110 / 29 |

By model name (measured): extraction, continue and report calls go to `gpt-4o` (the "best" slot), summaries would go
to `gpt-4o-mini` (none happened), embeddings to `text-embedding-3-small`. Every prompt's SHA-256 matches between the
pinned build and the head of `main` for both cases, so the default path made the same requests.

What the structure shows (arithmetic from the table and the JSON):
- 49 chunks for 20 documents: 41,786 `o200k_base` tokens, cut at a step of 1,100 tokens, `ceil(n/1100)` per document, summed
  to 49; the stub saw 49 extraction calls. Calls per document: 2 per chunk fixed, plus reports and embeddings.
- Fixed template per call (stub counter, empty chunk): extraction 1,933 tokens, continue 19, loop check 26, summary 117,
  community report 1,526. 49 x 1,933 = 94,717 of the 139,626 extraction prompt tokens.
- The "continue" call resends the first prompt and the model's first answer: 140,802 prompt tokens under shape A against
  169,024 under shape B, over the same 49 calls.
- Per-document inserts regenerate reports at every insert; nano-graphrag's own response cache absorbed 259 - 146 = 113 of
  them in this case. Of the 48 report calls, 26 came with document 19, the insert after which the largest component grew from 34 to 110 nodes.
  A single insert call made 29.
- Means per document at N=20 (arithmetic): 7.3 chat calls and 21,058 prompt tokens (B), 4.9 and 14,021 (A). They vary by
  document: chunks per document run from 1 to 5.

## What depends on the model

- *Not on the answers:* extraction calls (one per chunk), "continue" calls (one per chunk at the default gleaning of 1;
  no loop-check call is made at 1), extraction prompt tokens.
- *On the answers:* the prompt tokens of the "continue" calls; entities per chunk and so embedding inputs; whether any
  description summary happens (a merged description of 500 tokens or more; shape B had none); how many community reports
  there are (only the largest connected component is clustered: 110 of 224 nodes here) and how many the cache absorbs;
  loop-check calls if gleaning is raised above 1; retries (tenacity, 5 attempts, plus the OpenAI SDK's own
  `max_retries` = 2, measured); a report answer with no parsable JSON ends the insert (from reading the code, not run).

## Outbound attempts and telemetry

No connect attempt and no DNS lookup to a non-loopback address was recorded in any of the 7 scenario runs. Each run had a
dummy key, the stub's address, `HTTP_PROXY`/`HTTPS_PROXY` set to `http://127.0.0.1:9`, `NO_PROXY=127.0.0.1,localhost`, a
stripped environment, and a Python-level guard that records and refuses non-loopback connects. Positive control: a deliberate
`urllib` request failed at the proxy port and a raw socket to a documentation-range address was refused by the guard. No
networking or telemetry code is in `nano_graphrag/*.py` at 0.0.8.2 (grep); dependencies were not audited, and the head of
`main` adds Bedrock support, not audited. The guard does not see sockets opened in C code.

## Determinism

Two clean runs of the 20-document shape-B case: calls by kind, prompt and completion tokens, models, embedding inputs,
graph size and the sorted list of every prompt's SHA-256 are all identical (JSON key `determinism_perdoc_B_vs_repeat`).
The check was made to fail on purpose: a copy of the runner whose answers carry random bytes turned it red on prompt
tokens and prompt hashes, though the call counts stayed equal. `PYTHONHASHSEED` was left random.

## Not verified

Output tokens of real answers; how many summaries and reports a real graph triggers and their sizes; retries and
rate limits; whether a failed request is billed; quality; wall-clock time with a real model; an Anthropic route (the
request surface is chat completions with fixed model names, `response_format` json on reports, `max_tokens` 500 on
summaries, and an embeddings call that has no Anthropic counterpart); Python 3.13 and newer; the v0.0.8 tag itself; any
other platform. The graph in these runs comes from the stub's rule, not from text understanding: its connectivity, and
so the report counts, are not a forecast.

## Re-run

```
S=$SCRATCH   # a scratch directory outside the repository; corpus.json is the pinned MultiHop-RAG file
uv venv --python 3.12 $S/venv && uv pip install --python $S/venv/bin/python nano-graphrag==0.0.8.2
TIKTOKEN_CACHE_DIR=$S/tiktoken-cache $S/venv/bin/python -I -c "import tiktoken; tiktoken.encoding_for_model('gpt-4o'); tiktoken.get_encoding('cl100k_base')"
git clone https://github.com/gusye1234/nano-graphrag $S/clone && git -C $S/clone checkout acb35c0
uv venv --python 3.12 $S/venv-main && uv pip install --python $S/venv-main/bin/python $S/clone transformers
mkdir -p $S/home
env -i PATH=/usr/bin:/bin:/opt/homebrew/bin HOME=$S/home TIKTOKEN_CACHE_DIR=$S/tiktoken-cache \
  HTTP_PROXY=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 http_proxy=http://127.0.0.1:9 https_proxy=http://127.0.0.1:9 \
  NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost \
  $S/venv/bin/python tools/exp/x2_nano_graphrag.py --corpus $S/corpus.json \
  --documents kb-kg/experiments/x2-index-cost/documents.tsv \
  --out kb-kg/experiments/x2-index-cost/rehearsal/nano-graphrag.json --scratch $S/runs \
  --secondary head-acb35c0=$S/venv-main/bin/python
```

The runner takes about half a minute with warm caches. It refuses a corpus whose SHA-256 differs from the pin. Call dumps without text and the
working directories (which hold article text) stay under `--scratch`.
