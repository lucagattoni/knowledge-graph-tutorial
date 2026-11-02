---
type: benchmark
datasets: []
updated: 20261102 21:25 UTC
---

# EnterpriseRAG-Bench

EnterpriseRAG-Bench asks how well a [retrieval-augmented generation](../index/retrieval-augmented-generation.md) system answers questions over a company's internal documents: chat threads, email, tickets, wikis. It is a benchmark-first item, so its data is described here.

## What it tests

Lookups, multi-document reasoning, constrained retrieval, conflict resolution and recognising absent answers [1]. The authors say there is "no widely adopted dataset that realistically reflects the nature of company-internal knowledge" [1].

## Tasks, metrics and protocol

Four scores per question [1]: **correctness** (binary [LLM-judge](../index/llm-as-judge.md) verdict, lenient on style); **completeness** (share of the gold answer's atomic facts present); **document recall** (share of gold documents in the top 10 by default); **invalid extra documents** (a count). The leaderboard score is, per question, the completeness percentage if correct and zero otherwise, averaged [1][4]. The judge is GPT-5.4 at medium reasoning [3]. All submissions are scored against the first release's gold set; corrections wait for a new release [1].

## Datasets

Sun et al., 2026 (Onyx and UC Berkeley) [1].

- **Documents:** a synthetic company, "Redwood Inference", with 511,962 documents in nine sources, led by Slack 285,605, Gmail 121,390 and Linear 35,308 [1][3]. The independent study counts 511,957 plus two scaffold pages, 511,959, and 600.8 million tokens [5]. The totals are not reconciled.
- **Questions:** 500 in ten categories (basic 175, semantic 125, six more, then high level 10 and info not found 20) [2]. The last two have no gold documents [2]. A file of 100 metadata questions is off the leaderboard [2].
- **Made by:** human-guided scaffolding, high-fidelity project clusters, cheaper topic-based bulk generation, then noise: misfiled documents and near-duplicates with changed facts [1][2]. Gold sets were refined by pooling retrievers and a three-judge vote [1][5].
- **Licence:** MIT, from the `LICENSE` file (Copyright 2026 DanswerAI, Inc.) and the dataset tag [6][7][8]. Terms of the generating models: **unstated**.
- **Versions:** release v1.0.0 20260329; paper v1 20260505, v2 20260519 [1][9].

## Results

Each number re-read on 20261102. Blocks use different readers and judges; do not compare across them.

| System | Score | Metric | Who ran it | First-party? | Date | Source |
|---|---|---|---|---|---|---|
| BM25, top 10 | correctness 68.8, completeness 56.0, recall 68.4, extra 9.0 | percent | benchmark authors | yes | 20260519 | [1] |
| Vector (text-embedding-3-large) | 51.4, 42.9, 46.0, 9.3 | same | same | yes | 20260519 | [1] |
| Bash agent (low reasoning) | 60.6, 61.1, 55.8, 2.0 | same | same | yes | 20260519 | [1] |
| BM25 | 74.7 at 1,144 documents; 55.2 at 131,876; 50.5 at 511,959 | combined score | Wang et al. | independent | 20260731 | [5] |
| File-system agent | 77.4; 50.9; 30.7 | same | same | independent | 20260731 | [5] |
| DenseRAG | 58.1; 36.0; 29.9 | same | same | independent | 20260731 | [5] |
| HippoRAG 2 | 66.2; 41.0; no build beyond 131,876 | same | same | independent | 20260731 | [5] |
| LinearRAG; MS-GraphRAG; LightRAG | 46.2; 45.9; 48.0 at 1,144; builds stop at 131,876; 8,750; 2,254 | same | same | independent | 20260731 | [5] |
| codos.ai; Flexor.ai; CDL (top three of 35) | 92.64; 91.48; 90.91 | overall | the submitters | first-party each | board 20261026 | [4] |
| OpenAI File Search; RAGFlow; Azure AI Search | 61.03; 50.24; 48.42 | overall | **unstated** | **unstated** | board 20261026 | [4] |
| LlamaIndex (default configs); LangChain (default configs); Open WebUI + Chroma (bottom three of 35) | 27.20; 24.98; 24.89 | overall | **unstated** | **unstated** | board 20261026 | [4] |

The scaling study used a Qwen3.6-27B reader, top-5 chunks, 28 nested corpus sizes, one run per question [5]. Leaderboard entries must be reproducible, by an open guide or a closed sandbox; Onyx sells a RAG product and excludes itself [2].

*Reading:* in the independent study corpus size moves scores more than method: BM25 drops 24 points from 1,144 to 511,959 documents yet beats every method that built the full tier [5]. Graph builds stopped first, a cost result, not an accuracy one [5]. Whether the owner re-ran the leaderboard rows is **unstated**.

## Known problems

- **Synthetic, one company;** fit to real data is **unstated**. Authors list artefacts such as timestamps near 123456789 and "ACME" names [1].
- **Gold labels are "revisable hypotheses";** a gold set may be incomplete [1].
- **Lexical anchors:** the scaling study says questions carry exact keywords beside 326 mined "trap" documents, favouring exact matching. That is its reading [5].

## Used by

The paper has 11 citations (Semantic Scholar, read 20261102 20:01 UTC) [10]. Wang et al., *BM25 Wins at Scale* ([group page](../papers/graph-based-rag.md)), scoring [HippoRAG](../projects/hipporag.md), [LightRAG](../projects/lightrag.md) and [Microsoft GraphRAG](../projects/microsoft-graphrag.md) [5]. The leaderboard lists [RAGFlow](../projects/ragflow.md) [4]. Trends: [graph-based RAG](../trends/graph-based-rag.md), [plain-file knowledge](../trends/plain-file-knowledge.md). Terms: [BM25](../index/bm25.md), [vector search](../index/vector-search.md), [GraphRAG](../index/graphrag.md), [agent](../index/agent.md).

## Sources

1. https://arxiv.org/html/2605.05253 and https://arxiv.org/abs/2605.05253 : Sun et al., paper v2: abstract, metrics, Tables 6 and 9, generation, limitations (read 20261102 20:59 UTC)
2. https://raw.githubusercontent.com/onyx-dot-app/EnterpriseRAG-Bench/main/README.md : categories, extra questions, leaderboard rules, conflict note (read 20261102 20:59 UTC)
3. https://huggingface.co/datasets/onyx-dot-app/EnterpriseRAG-Bench/raw/main/README.md : card, per-source counts, judge, canary string (read 20261102 20:59 UTC)
4. https://onyx-dot-app-enterpriserag-bench-leaderboard.hf.space/ : 35 systems, last update 26 October 2026, score definition (read 20261102 20:59 UTC); https://huggingface.co/api/spaces/onyx-dot-app/EnterpriseRAG-Bench-Leaderboard : modified 20261026 (read 20261102 20:59 UTC); https://huggingface.co/spaces/onyx-dot-app/EnterpriseRAG-Bench-Leaderboard/raw/main/data/final_display_data/leaderboard.csv : the scores in the Results table (38 rows: 35 systems plus three benchmark baselines; top three 92.64, 91.48, 90.91; bottom three 27.2, 24.98, 24.89) (read 20261102 21:24 UTC)
5. https://arxiv.org/html/2607.26497 : Wang et al. (USTC, Metastone), *BM25 Wins at Scale*, v3 31 Jul 2026: setup, Table 1, traps (read 20261102 20:59 UTC)
6. https://raw.githubusercontent.com/onyx-dot-app/EnterpriseRAG-Bench/main/LICENSE : MIT text (read 20261102 20:59 UTC)
7. https://api.github.com/repos/onyx-dot-app/EnterpriseRAG-Bench : licence MIT, created 20260219, last push 20260903 (read 20261102 20:59 UTC)
8. https://huggingface.co/api/datasets/onyx-dot-app/EnterpriseRAG-Bench : tag `license:mit`, modified 20260508 (read 20261102 20:59 UTC)
9. https://api.github.com/repos/onyx-dot-app/EnterpriseRAG-Bench/releases : v1.0.0 published 20260329 (read 20261102 21:01 UTC)
10. https://api.semanticscholar.org/graph/v1/paper/batch : citationCount 11 for arXiv:2605.05253 (read 20261102 20:01 UTC)
