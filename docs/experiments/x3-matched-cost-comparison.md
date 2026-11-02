---
type: page
order: 4
updated: 20261102 20:17 UTC
---

# X3: Matched-cost comparison

X3 asks which retrieval route is cheaper at equal accuracy on one corpus. It is a proposal: nothing has run and no money has been approved. It may not start before [X2](x2-index-cost.md) has measured what building a graph costs per document, and it needs the owner's explicit yes with cost, model and data stated first.

## The question

Two gaps in the archive's direction pages. The page on cheaper graph builders ends its summary with "no study compares the five routes on one corpus" [1]. The page on retrieval by reasoning over structure says that "no entry holds a like-for-like cost comparison" [2]. Both are statements about what the archive read up to 20261030, not about everything published.

The proposal: build the same question set's corpus four ways, answer the same questions, and report accuracy by query type and the tokens spent on indexing and on each query [3].

## Why it matters

Cost figures in the archive cannot be set side by side, because each is priced under its own rules. One concrete case, first-party (the project's own authors): a notebook in the [PageIndex](../projects/pageindex.md) repository compares PageIndex with [vector search](../index/vector-search.md) on 63 questions about one company's annual reports for fiscal 2022 to 2026. PageIndex answers 100.0%. Vector search answers 54.0%, 74.6%, 79.4% and 87.3% at 10, 30, 50 and 100 retrieved chunks. Costs per 1,000 queries are $110 for PageIndex and $16 to $135 for the four vector runs [4]. The notebook states its pricing rule: vector search is priced without the prompt cache, because a deployment answers each question with one call, while PageIndex keeps the cache hits between the agent's turns on one question [4]. The rule is stated and argued, so this is a choice rather than an error, but it means the two columns do not measure the same thing.

*Reading:* until every route is priced under one stated rule, a cost comparison across routes says little. X3's job is to apply one rule to all four.

Nearby work exists, and it differs from X3:

- A controlled study by Wang and others varies one corpus over 28 sizes (1,144 to 511,959 documents) with one reader model and compares [BM25](../index/bm25.md), dense retrieval, [graph-based methods](../index/graphrag.md) and a file-system agent on accuracy and on build and query tokens. It reports that BM25 leads at larger sizes and that graph builds did not finish at scale [5]. Its corpus is a synthetic one: a fictional company's wiki pages, chat threads, tickets, e-mail and similar documents, not news [5].
- Han and others compare [RAG](../index/retrieval-augmented-generation.md) with GraphRAG variants under one protocol, including on [MultiHop-RAG](../datasets/multihop-rag.md). On that dataset they report construction time of 135 s for RAG, 5,560 s and 7,702 s for the two GraphRAG variants. These are seconds, not tokens or money [6].

## Method

As proposed [3]:

| Condition | What it is |
|---|---|
| 1 | BM25 alone |
| 2 | A free [hybrid retriever](../index/hybrid-search.md) with [reranking](../index/reranking.md) |
| 3 | One cheap graph builder taken from X2 |
| 4 | One navigation-based method, where a model reads a structure and decides what to read next |

One corpus and one question set. Accuracy is reported by query type: the proposal names inference, comparison, temporal and null queries. Tokens are reported for indexing and per query. The proposal's own risk note is that a navigation method's index cost depends on caching, so "cost must be priced the same way for every condition" [3].

Unstated in the proposal: which graph builder (the X2 candidates are [LightRAG](../projects/lightrag.md), [nano-graphrag](../../kb-kg/projects/nano-graphrag.md), [fast-graphrag](../../kb-kg/projects/fast-graphrag.md) and [Microsoft GraphRAG](../projects/microsoft-graphrag.md) [3]); which navigation method (the archive lists five variants and the proposal picks none [2]); the number of questions; the answering model; the judge; the number of runs per cell; how many chunks are retrieved.

## Data

The proposal has no Data line. Its method names four query types, which match [MultiHop-RAG](../datasets/multihop-rag.md), and X2 draws its documents from MultiHop-RAG [3]. So MultiHop-RAG is the likely corpus. **The proposal does not say so, and the choice is unstated.**

What the dataset holds, counted from its files on 20261102 [7][8]:

| Item | Value |
|---|---|
| Corpus | 609 news articles, about 1.06 million words by whitespace split (counted for this page from the corpus file; mean 1,746 per article) |
| Queries | 2,556: comparison 856, inference 816, temporal 583, null 301 |
| Evidence | 2 articles for 1,079 queries, 3 for 778, 4 for 398; null queries have no evidence |
| Licence | ODC-BY, declared in the repository README and in the Hugging Face dataset card. The repository root holds no LICENSE file (checked in its file listing; the GitHub licence endpoint answers 404) [7][8] |

Source paper: Tang and Yang, *MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries*, arXiv 2401.15391, first version 20240127 [9]. The evaluation side (tasks, metrics, results) is on the [benchmark page](../benchmarks/multihop-rag.md); the data side is on the [dataset page](../datasets/multihop-rag.md).

## Models

Unstated in the proposal. The owner's constraints from D-24 apply [3][10]: runs only on the owner's Apple Silicon Macs; OpenAI's and Anthropic's hosted models are both acceptable and so is a local model; one model per comparison, so a repeat on the other provider is a separate, labelled run with its own yes; prices are read from the provider's pages when a run is approved, not taken from memory.

## Cost

Set after X2. The proposal's rule: X2's per-document figure times the corpus size, plus query-time tokens, and the owner should not approve it before X2 has run [3]. No figure exists and no cap has been proposed. If the whole MultiHop-RAG corpus were used, the multiplier would be 609 articles (arithmetic from the count above, not an estimate).

## Status

Not started, as of 20261102. It waits for three things.

- **X2's per-document figure.** X2 pass A measured calls and tokens per document on one local model for every builder: LightRAG to 20 documents, fast-graphrag and Microsoft GraphRAG to 5, nano-graphrag failed on document 1. A second local model ran LightRAG alone, to 5 documents. Nothing paid has run, there is no hosted-model figure, and the archive notes that a hosted model will differ [11][10].
- **A BM25-alone baseline.** The order table says X3 needs it [3].
- **The owner's yes** with model, provider, corpus and cap, one experiment at a time (D-14) [3][10]. The recommended order is X2, X4, X3, X5 (D-24) [10].

## What it would change

The cheaper-graphs page asks whether a cheaper graph beats a plain baseline per question type [1]. The reasoning-retrieval page lists matched cost as an open gap [2]. A finished X3 would give each a measured answer for one corpus, one builder and one navigation method, with the setup stated. It would not give a verdict on a family of methods.

## What it cannot show

- **A family.** One graph builder and one navigation method stand for themselves, not for all graph or navigation methods.
- **Other corpora.** MultiHop-RAG is short news articles, in English (the dataset card's language field is `en`), with questions built for multi-hop retrieval [6][7][9]. *Reading:* the archive's published results for tree-style navigation are on long structured documents such as annual reports [2][4], so a navigation method may have little structure to use in 609 short articles, and a weak result there would say little about long documents.
- **Prices that last.** A hosted run is priced on the day it runs. A local run measures time and tokens, not money.
- **Independence.** The owner runs it on the owner's machine, with a small set and few runs. It would be first-party and would say so.
- **Why a method wins or loses.** It reports accuracy and tokens, not the cause.

## Sources

1. [Cheaper-graphs direction page of the archive](../../kb-kg/directions/eager-to-lazy-graphs.md) : the five routes and the statement that no study compares them on one corpus (read 20261102 19:44 UTC, from the archive's text of 20261030)
2. [Reasoning-retrieval direction page of the archive](../../kb-kg/directions/reasoning-retrieval.md) : the "like-for-like" statement, the five navigation variants, results on annual reports (read 20261102 19:44 UTC, from the archive's text of 20261030)
3. [Experiments record of the archive](../../kb-kg/experiments/README.md) : the X3 proposal, the order table, the X2 candidates, the need for a BM25-alone baseline (read 20261102 19:36 UTC at commit `f2e87e6`; the X3 section was unchanged at `8f780f8` and at `66fe6c0`, checked 20:15 UTC)
4. https://raw.githubusercontent.com/VectifyAI/PageIndex/main/cookbook/pageindex-vs-vector-10k/pageindex-vs-vector-10k.ipynb : the 63 questions, the accuracy figures, the five costs per 1,000 queries, the pricing rule (read 20261102 19:41 UTC)
5. https://arxiv.org/abs/2607.26497 and https://arxiv.org/html/2607.26497v3 : Wang and others, *BM25 Wins at Scale*, v3 20260731: 28 nested corpus sizes, one reader, EnterpriseRAG-Bench, metered build and query tokens (read 20261102 19:39 and 19:41 UTC)
6. https://arxiv.org/abs/2502.11371 and https://arxiv.org/html/2502.11371v3 : Han and others, *RAG vs. GraphRAG*, v3 20260304: unified protocol; Table 4 construction times on MultiHop-RAG; dataset description with four query types (read 20261102 19:39 and 19:46 UTC)
7. https://huggingface.co/datasets/yixuantt/MultiHopRAG : dataset card (licence ODC-BY, language `en`, 2556 queries, evidence in 2 to 4 documents) and the files `corpus.json` and `MultiHopRAG.json`, counted with Python (read 20261102 19:40 UTC; card re-read 20:15 UTC)
8. https://github.com/yixuantt/MultiHop-RAG : README (ODC-BY statement), root file listing without a LICENSE file, licence endpoint 404 (read 20261102 19:40 UTC)
9. https://arxiv.org/abs/2401.15391 : the MultiHop-RAG paper, first version 20240127 (read 20261102 19:39 UTC)
10. [Decisions record of the archive](../../DECISIONS.md) : D-14 (one yes at a time), D-24 (constraints and order), D-27 and D-28 (pass A results) (read 20261102 19:36 UTC at `f2e87e6`; D-27 at `8f780f8`, 19:46 UTC; D-28 at `66fe6c0`, 20:15 UTC)
11. [X2 pass-A page of the archive](../../kb-kg/experiments/x2-index-cost/pass-a-local-model.md) : what pass A measured on two local models and what it cannot show (read 20261102 20:15 UTC at `66fe6c0`, the archive's main branch)
