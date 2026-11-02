# X2: the measured index cost of cheap graph builders

**Status: groundwork in progress (Step 0 of the [order and gates](../README.md#order-and-gates)). Nothing paid has
run.** This directory holds what is frozen before any model sees it, and later the rehearsal and pilot results.

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

What a stub count can and cannot show is in the stub's own header: prompt sizes and output-independent call counts are
exact for the given input; anything driven by what a model says (gleaning loops, retries, summaries that trigger only
when text grows) depends on the answers the stub gives, so it is a count *for those answers*.
