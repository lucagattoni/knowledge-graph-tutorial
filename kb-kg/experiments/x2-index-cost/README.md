# X2: the measured index cost of cheap graph builders

**Status: Step 0 groundwork (the [order and gates](../README.md#order-and-gates)) is done for the documents and the four free
rehearsals. Nothing paid has run.** This directory holds what is frozen before any model sees it, the rehearsal results, and later the
pilot results.

## What is frozen

| Item | Value |
|---|---|
| Documents | The 20 articles of the MultiHop-RAG corpus whose SHA-256 of the URL is smallest, listed in [`documents.tsv`](documents.tsv) |
| Rule | Fixed before the result was looked at. It involves no random generator and no judgement. Made by [`tools/exp/x2_select_documents.py`](../../../tools/exp/x2_select_documents.py), which refuses a corpus file whose hash differs from the pin |
| Corpus | `corpus.json` at Hugging Face revision `71ac0d0bd1f951d2d6b70311f7d2ae404e1ffa82`, SHA-256 `20b61b5ab84de84a927420c5d265b7ec8d859ae49980699958a787ade9e4d28f`. The pin comes from the manifest of the public benchmark repository, which verified it. I downloaded the file 20261102 10:20 UTC and the hash matched |
| Size of the 20 | 191,571 characters and 32,453 words (mean 9,579 characters). The whole corpus is 609 articles and 6,297,171 characters (median article 7,836), so the 20 are about 3.0% of it (my arithmetic) |
| Mix | technology 6, sports 6, science 3, entertainment 3, business 2 |
| Licence | The dataset is ODC-By 1.0. The news text comes from publishers whose own terms were not checked, so **the article text is never committed**, here or in any log. Only identifiers and sizes are |

## Groundwork tools

| Tool | What it is | Tests |
|---|---|---|
| [`tools/exp/x2_select_documents.py`](../../../tools/exp/x2_select_documents.py) | Makes `documents.tsv` | 7 |
| [`tools/exp/stub_llm.py`](../../../tools/exp/stub_llm.py) | A loopback stub of an OpenAI-compatible model server, used to count a builder's calls and prompt tokens without spending anything | 8; one of them failed on first run because the listen queue was 5 and a burst of 20 parallel calls was undercounted, and it passes only with the queue raised to 256 (breaking that on purpose turns it red again) |
| [`tools/exp/exp_stats.py`](../../../tools/exp/exp_stats.py) | An exact paired sign test, Wilson intervals and a seeded paired bootstrap, for the later comparisons | 17, each checked against an independent oracle (brute-force enumeration, a root solve of the defining equation); 7 deliberate mutants, all killed in three runs. The first run let one survive (the interval's upper clamp, which a property test over 500 sample sizes now guards: 157 cases leave [0, 1] by an ulp without it) and one test was weak (a seed check that two unseeded runs could pass by chance), both fixed |
| [`tools/metering_gateway.py`](../../../tools/metering_gateway.py) ([doc](../../../tools/metering_gateway.md)) | A local proxy that every hosted-model call of a later experiment passes through, for the OpenAI and Anthropic protocols: it logs the provider's own usage in one record, refuses a call that could take spend past a cap before forwarding anything, and keeps the real key to itself. Standard library only. **Never used against a real provider** | 78 unit tests. The agent's 47 deliberate mutants were all killed; I ran 11 of my own on the ledger, the reservation bound, the cost arithmetic, the Host check and the key-shape check, all killed (my first harness run had a red baseline, so its verdicts were void; fixed and rerun). Its first lock-removal mutant survived, because CPython rarely switches threads inside a short critical section; a test with a deliberately slow ledger now kills it |
| [`tools/exp/gateway_sdk_e2e_openai.py`](../../../tools/exp/gateway_sdk_e2e_openai.py) and [`..._anthropic.py`](../../../tools/exp/gateway_sdk_e2e_anthropic.py) | End-to-end checks with the real OpenAI and Anthropic Python SDKs pointed at the gateway, against a fake provider that records what it receives: chat, streaming, embeddings, the client's dummy key replaced by the real one, exact costs, a 429 refusal that forwards nothing, spend never over the cap, the key in no file | 17 and 12 checks, all passing. Four mutants of the gateway (cap check removed, stream usage not requested, key not swapped, spend never charged) each turn one of them red. They cross a seam the unit tests do not (the SDKs' own serialisation), but not TLS or a real provider's responses |

What a stub count can and cannot show is in the stub's own header: prompt sizes and output-independent call counts are
exact for the given input; anything driven by what a model says (gleaning loops, retries, summaries that trigger only
when text grows) depends on the answers the stub gives, so it is a count *for those answers*.

## The rehearsals, side by side

Each builder indexed the 20 documents against the stub model with no key and no network, on its own defaults and in
a plausible answer shape ("shape B": about 6 entities and 5 relations per chunk). Details, pins, licence findings and
limits are on each builder's page; every figure below is in that page's JSON, and I reproduced each JSON with a fresh
run on 20261102 (see the commits).

| Builder | Version run | Installs on Apple Silicon | Chunks for the 20 | Chat calls | Chat prompt tokens | Per document (arithmetic) | Embedding inputs |
|---|---|---|---|---|---|---|---|
| [LightRAG](rehearsal/lightrag.md) | `lightrag-hku` 1.5.7 | Yes, wheels; `openai` must be added | 49 | 98 | 299,901 | 4.9 calls, 14,995 tokens | 497 |
| [nano-graphrag](rehearsal/nano-graphrag.md) | PyPI 0.0.8.2 | Yes, with one local build (`hnswlib`); the head of `main` fails to import without `transformers` | 49 | 146 | 421,152 | 7.3 calls, 21,058 tokens | 234 |
| [Microsoft GraphRAG](rehearsal/microsoft-graphrag.md) | `graphrag` 3.3.0 | Yes, wheels only | 47 | 207 | 400,764 | 10.3 calls, 20,038 tokens (without the CLI's connectivity test) | 305 |
| [fast-graphrag](rehearsal/fast-graphrag.md) | commit `23b3a1b` (no release or tag; last push 20251101) | Yes, one local build (`hnswlib`) | 80 | 80 | 187,783 | 4.0 calls, 9,389 tokens | 374 |

All four licences were read from the `LICENSE` file and are MIT. For each, the file's hash was the same in the installed
package and at the release tag or pinned commit.

**How to read the table, and how not to.**
- **This is not a like-for-like comparison.** Each builder runs on its own defaults, so chunk sizes differ (LightRAG,
  nano-graphrag and Microsoft GraphRAG use 1,200-token chunks; fast-graphrag uses 3,200-character windows, 80 chunks
  for the same text). The shape-B answer was written separately for each builder's required output format, so the
  nominal shape is the same but the text is not.
- **Only the input side is counted, and tokens are the stub's** (tiktoken `cl100k_base`, not any provider's). Output
  tokens are unmeasured, so no cost can be derived from this table yet. Pass A of the pilot, on a local model, is what
  measures them.
- **Some counts depend on what a model says.** Chunk and extraction counts do not. Entity and relation summaries,
  community reports (which follow graph connectivity) and the size of a "continue" prompt (which carries the first
  answer) do. Microsoft GraphRAG's reports (54) and nano-graphrag's (48) are counts for the stub's answers; LightRAG made
  none and fast-graphrag none with short descriptions, 41 with 200-character ones.
- **One surprise worth keeping:** fast-graphrag's gleaning never adds a call at the pinned commit, because the
  continuation prompt cannot be formatted, so its documented "2n calls" does not happen. LightRAG's gleaning is one pass
  whatever the setting, not up to n.
- **The smallest valid answer (no entities) is not valid for two builders:** fast-graphrag raises on it and Microsoft
  GraphRAG stops after extraction. A floor shape with one entity per chunk was used for them instead.

**What the pilot's gate will need from this.** The next paid step is the pilot on a hosted model under a cap. The table
gives the number of calls and the input size the pilot must expect per builder, so its cap can be set from measured
prompt sizes, with output tokens as the one unmeasured term. Which builders are worth a paid pass is the owner's call;
the table does not rank them.
