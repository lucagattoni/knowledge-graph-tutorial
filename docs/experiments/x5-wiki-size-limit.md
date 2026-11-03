---
type: page
order: 6
updated: 20261102 20:17 UTC
---

# X5: Wiki size limit

X5 asks at what size a wiki that a model navigates through one index page stops working. It is a proposal: nothing is frozen for it and nothing has run. It is the last and heaviest of the five experiments, and it waits for [X2](x2-index-cost.md) and [X4](x4-code-graph-vs-grep.md) to show what a model run costs here.

## The question

The pattern comes from a gist titled "LLM Wiki", created 20260404 16:25 UTC [1]. A model builds and maintains a [wiki](../index/llm-wiki.md) of linked Markdown files, and an `index.md` catalogues every page "with a link, a one-line summary" [1]. To answer a question the model reads the index first, then opens pages. The gist says this "works surprisingly well at moderate scale (~100 sources, ~hundreds of pages)" and "avoids the need for [embedding-based RAG](../index/retrieval-augmented-generation.md) infrastructure". It adds that "as the wiki grows you want proper search", and it gives no threshold and no measurement behind either figure [1].

The archive's page on Markdown-file knowledge bases lists "at what size does an index-only wiki stop working?" as its first unresolved item and asks, among its signals to watch, for "a size sweep of an index-only wiki with a fixed question set" [2]. X5 is that sweep.

## Why it matters

Several projects in the archive build on the gist [2]. The gist's size guidance is the approximate figure above. No entry on the archive's page reports an independent run of its own project, and the quality figures it gives for the entries are the projects' own (first-party); the outside tests the archive found concern the legacy MemGPT, not the current Letta Code [2]. A builder choosing between an index page and a search layer therefore has no measured size at which to switch.

The nearest outside evidence is a size sweep of a different thing. Wang and others vary one synthetic enterprise corpus over 28 nested sizes, from 1,144 to 511,959 documents (1.7M to 601M tokens), with one reader model [3][4]. Their file-system [agent](../index/agent.md) explores raw files with three tools (`list_dir`, `grep`, `read_doc`) and has no index page [4]. It has the higher point estimate at the smallest tiers: 77.4 against [BM25](../index/bm25.md)'s 74.7 on the official combined score at 1,144 documents, where the 95% intervals (73.9 to 80.8 and 71.4 to 77.9) overlap [4]. Around 10 million corpus tokens BM25 overtakes the agent, and at the full corpus the scores are 30.7 for the agent and 50.5 for BM25 [3][4]. At the smallest tier the agent used 226K tokens per question against 5.8K for BM25 [4]. The study does not test a wiki that a model compiled, and its smallest tier is larger than the largest size X5 proposes.

*Reading:* that study shows that an agent which explores files loses to plain keyword ranking as a corpus grows, in that setup. It does not say where an index page starts to fail, because an index page and a file listing behave differently as they grow.

## Method

As proposed [5]:

- Markdown corpora of 10, 30, 100 and 300 pages, taken from a public set.
- A model answers fixed questions by reading an index page and then the pages it picks.
- The outcome measures are accuracy and tokens against corpus size, with BM25 as the baseline.

Unstated in the proposal: which public set; who writes the index page and whether a model compiles the pages (the proposal takes pages "from a public set" and does not mention a compile step); the questions and their answer key; the grader; the number of runs per size; the model; and what counts as "stops working". Before a run the plan would have to fix that last rule in writing, since a size curve alone does not name a break.

One mechanism a sweep can expose, stated by the gist's own description: the index lists every page, so it grows with the corpus, and the model reads all of it before choosing a page [1].

*Reading:* the largest size, 300 pages, sits inside the gist's own "hundreds of pages". A sweep that stops there may show no failure, and the proposal does not say what the result would mean if nothing breaks.

## Data

Unstated. The proposal names no corpus and the archive's record freezes nothing for X5 [5]. Frozen inputs exist for X2 (20 documents) and X4 (20 questions with hand-derived answers) only [5]. The rules for every experiment record the dataset version and its licence, so a corpus's licence would be read before a run [5].

## Models

Unstated: the proposal says only "a model to navigate" [5]. The owner's constraints from D-24 apply: runs only on the owner's Apple Silicon Macs; OpenAI's and Anthropic's hosted models and a local model are all acceptable; one model per comparison, so a repeat on the other provider is a separate, labelled run with its own yes; prices are read from the provider's pages when a run is approved [5][6].

## Cost

Unknown before a pilot. The proposal calls X5 the largest of the five because cost scales with corpus size times the number of questions. It would run last, after X2 and X4 have shown what a model run costs here [5]. The order table gives the cost as "set from X2 and X4" [5]. No cap has been proposed.

## Status

Proposal only, as of 20261102. It waits for:

- **X2 and X4 results.** X2 pass A has measured calls and tokens per document for the graph builders on one local model, and for LightRAG alone on a second local model; nothing paid has run [7]. X4 has frozen questions and answers but no agent has run on them [5].
- **A corpus and a frozen question set**, chosen and written down before any model sees them, as Step 0 did for X2 and X4 [5].
- **The owner's yes** with model, provider, corpus and cap, one experiment at a time (D-14). The recommended order is X2, X4, X3, X5 (D-24) [5][6].

## What it would change

The archive's first unresolved item on Markdown-file knowledge bases would have one measured size curve for one setup [2]. The gist's "moderate scale" would get one number under stated conditions: a model, a corpus type, a question set, a rule for "stops working". The page that reports it would still not be a threshold for wikis in general.

## What it cannot show

- **A general threshold.** One model, one corpus type and one question set give a size for that setup only.
- **Whether a model-compiled wiki behaves the same.** The proposal takes existing pages; it says nothing of a compile step, so it may test the navigation half of the gist's pattern and not the compiled-knowledge half [1][5].
- **Whether an index page beats search.** The BM25 baseline answers a different question: whether the index page matches plain ranking on the same pages.
- **Link-following, human edits or months of use.** The archive lists these as separate open questions on its page, and the proposal does not test them [2][5].
- **Independence.** The owner would run it on the owner's machine with a small set. It would be first-party and would say so.

## Sources

1. https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw : the gist's text: the index catalogue, the "moderate scale" sentence, the "proper search" sentence, no measurement or threshold; https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f : creation time 2026-04-04T16:25:13Z (read 20261102 19:39 and 19:41 UTC)
2. [Markdown-files direction page of the archive](../../kb-kg/directions/plain-files-and-wikis.md) : the first unresolved item, the signal to watch, the first-party status of the entries' figures, the outside tests that ran the legacy MemGPT, the other open questions (read 20261102 20:15 UTC, from the archive's text of 20261030)
3. https://arxiv.org/abs/2607.26497 : Wang and others, *BM25 Wins at Scale*, v3 20260731: abstract with the 28 tiers, the 10-million-token crossover and the 39-times query tokens; v3 revised 20260731 (read 20261102 20:15 UTC)
4. https://arxiv.org/html/2607.26497v3 : the corpus ladder (1,144 to 511,959 documents; 1.7M to 601M tokens), the shared reader, the file-system agent's tools, the score table (77.4 and 74.7 at 1,144 documents; 30.7 and 50.5 at full scale), the overlapping 95% intervals of section 4.2 and the 226K and 5.8K tokens per question (read 20261102 20:14 UTC)
5. [Experiments record of the archive](../../kb-kg/experiments/README.md) : the X5 proposal, the order table, what is frozen (read 20261102 19:36 UTC at commit `f2e87e6`; the X5 section was unchanged at `8f780f8` and at `66fe6c0`, checked 20:15 UTC)
6. [Decisions record of the archive](../../DECISIONS.md) : D-14 and D-24 (read 20261102 19:36 UTC at `f2e87e6`)
7. [X2 pass-A page of the archive](../../kb-kg/experiments/x2-index-cost/pass-a-local-model.md) : pass A done for two local models (every builder on the first, LightRAG alone on the second), nothing paid (read 20261102 20:15 UTC at `66fe6c0`, the archive's main branch)
