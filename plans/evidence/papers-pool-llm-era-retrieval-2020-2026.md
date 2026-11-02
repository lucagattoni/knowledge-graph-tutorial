# Candidate fundamental papers: retrieval and graph-based retrieval in the LLM era (2020 to 2026)

Researcher output for the papers chapter. Written 20261102 (UTC), metadata and citation counts read 20261102 19:45 to 20:30 UTC.

**Area:** retrieval-augmented generation and its surveys; graph-based RAG; lazy or cheaper graph construction; reasoning over structure without vectors; agentic and reinforcement-learned retrieval and graph traversal; long context versus retrieval; independent evaluations of when a graph helps.

## Method and caveats

- **Tests (decision R-1):** origin, turning point (independent evaluations count), widely built on, survey of record. A paper is listed with the tests it passes and the evidence for each. Where only a count supports a test, the count is in the entry's header line.
- **Metadata:** title, authors, first-version date, comments and abstract come from the arXiv API (export.arxiv.org), read at the time stated in each entry. "Venue" is what the arXiv record says (journal reference or authors' comment) plus the Semantic Scholar venue field when a count was obtained from it; "none stated" means the record names none, not that the paper is unpublished.
- **Citation counts:** Semantic Scholar Graph API, batch endpoint by arXiv id, read 20261102 20:20 UTC (HTTP 429 from 20:03 until then; no key). Counts are as of that time and move daily. They count citations to the paper as Semantic Scholar merges its versions. OpenAlex (DOI of the arXiv record) was also read at 20:03 UTC and is far lower for the same papers (for example 3,048 against 20,475 for RAG, 13 against 1,742 for Search-R1) because it counts only the arXiv record; it is not used here.
- **Widely built on:** applied only where the count is 500 or more. This threshold is the researcher's choice for this file, not the project's; the owner can move it. A paper under 500 may still pass another test.
- **Recent papers (2026):** no citation count is meaningful yet. Entries in 2026 pass only on the independent-evaluation criterion and are marked as too recent to be tested by time.
- **Read depth:** "abstract only" means the arXiv abstract. "alphaXiv report" is an AI-generated summary of the full text served by the alphaXiv tool; numbers taken from it are second-hand and are labelled so. "Full text" means the alphaXiv text extraction was searched for the cited passages. Claims marked first-party come from a paper's own authors.
- **Not read:** the PDFs themselves. Search-engine summaries were used only as leads.
- **Carried over from the archive:** statements marked "archive" come from kb-kg pages written by an earlier run (read 20261030) and were not re-fetched here.
- **Name collision:** two benchmarks are called GraphRAG-Bench (2506.05690, proposed; 2506.02404, not proposed).

## Summary table (strongest first)

| # | Paper | arXiv id | Year | Tests passed | Citations |
|---|---|---|---|---|---|
| 1 | RAG | 2005.11401 | 2020 | origin, widely-built-on | 20475 |
| 2 | DPR | 2004.04906 | 2020 | origin, widely-built-on | 7702 |
| 3 | Lost in the Middle | 2307.03172 | 2023 | turning-point, widely-built-on | 5799 |
| 4 | RAG survey (Gao) | 2312.10997 | 2023 | survey-of-record, widely-built-on | 4421 |
| 5 | REALM | 2002.08909 | 2020 | origin, widely-built-on | 3596 |
| 6 | Self-RAG | 2310.11511 | 2023 | origin, widely-built-on | 3006 |
| 7 | GraphRAG | 2404.16130 | 2024 | origin, widely-built-on | 2489 |
| 8 | Search-R1 | 2503.09516 | 2025 | origin, widely-built-on | 1742 |
| 9 | RETRO | 2112.04426 | 2021 | origin, widely-built-on | 2015 |
| 10 | IRCoT | 2212.10509 | 2022 | origin, widely-built-on | 1479 |
| 11 | RAG survey (Fan) | 2405.06211 | 2024 | survey-of-record, widely-built-on | 1245 |
| 12 | RAPTOR | 2401.18059 | 2024 | origin, widely-built-on | 840 |
| 13 | GraphRAG survey (Peng) | 2408.08921 | 2024 | survey-of-record, widely-built-on | 695 |
| 14 | LightRAG | 2410.05779 | 2024 | origin, widely-built-on | 577 |
| 15 | HippoRAG | 2405.14831 | 2024 | origin | 437 |
| 16 | G-Retriever | 2402.07630 | 2024 | origin | 417 |
| 17 | Think-on-Graph | 2307.07697 | 2023 | origin | 373 |
| 18 | HippoRAG 2 | 2502.14802 | 2025 | turning-point | 284 |
| 19 | RAG or Long-Context LLMs | 2407.16833 | 2024 | turning-point | 199 |
| 20 | Retrieval meets Long Context | 2310.03025 | 2023 | turning-point | 158 |
| 21 | KAG | 2409.13731 | 2024 | origin | 152 |
| 22 | RAG vs GraphRAG | 2502.11371 | 2025 | turning-point | 118 |
| 23 | Cache-Augmented Generation | 2412.15605 | 2024 | origin | 86 |
| 24 | Graph-R1 | 2507.21892 | 2025 | origin | 64 |
| 25 | GraphRAG-Bench (When to use graphs) | 2506.05690 | 2025 | turning-point | 60 |
| 26 | LinearRAG | 2510.10114 | 2025 | origin | 70 |
| 27 | LogicRAG | 2508.06105 | 2025 | origin | 41 |
| 28 | RAGSearch | 2604.09666 | 2026 | turning-point | 1 |
| 29 | BM25 Wins at Scale | 2607.26497 | 2026 | turning-point | 2 |
| 30 | Is GraphRAG Needed? | 2606.25656 | 2026 | turning-point | 2 |

## Candidates

## 1. RAG (2020) — arXiv 2005.11401

- **Title:** Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
- **Authors:** Patrick Lewis, Ethan Perez, Aleksandra Piktus (12 in total) [1]
- **Venue:** arXiv comment: "Accepted at NeurIPS 2020" [1]
- **First version:** 20200522 [1]
- **Link:** https://arxiv.org/abs/2005.11401
- **Citations:** 20475, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Names and defines the pattern. Abstract [1]: "We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG)", and prior retrieval-augmented models had "only been investigated for extractive downstream tasks". The primer (kb-kg/primer/README.md) and llm-era archive pages also treat it as the origin of the term RAG.
  - *widely-built-on:* Cited 20475 times in Semantic Scholar Graph API (read 20261102 20:20 UTC) [2]. Threshold applied in this file: 500 or more.
- **Idea:** A pre-trained seq2seq model (parametric memory) is combined with a dense vector index of Wikipedia (non-parametric memory) read by a pre-trained neural retriever. Two formulations are compared: one conditions on the same retrieved passages for the whole sequence, the other can use different passages per token. Fine-tuned, it sets the state of the art on three open-domain QA tasks and generates more specific, diverse and factual text than a parametric-only baseline [1].
- **Relations:**
  - builds on REALM (2002.08909): the full text says REALM and ORQA "combine masked language models with a differentiable retriever" and cites REALM as prior retrieval-based memory [3].
  - builds on DPR (2004.04906): "We use a pre-trained bi-encoder from DPR to initialize our retriever and to build the document index" [3].
  - answered by Self-RAG (2310.11511): its abstract objects to "indiscriminately retrieving ... a fixed number of retrieved passages" [4].
  - mapped by the RAG surveys: Gao et al. (2312.10997) describe the progression of "Naive RAG, the Advanced RAG, and the Modular RAG" paradigms [5].
- **Read:** Full text (alphaXiv extraction, grepped for the retriever and prior-work passages) and abstract. Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2005.11401 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2005.11401 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 20475 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2005.11401 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)
  4. https://arxiv.org/abs/2310.11511 : abstract of the paper named in the text (arXiv API, read 20261102 19:45 UTC)
  5. https://arxiv.org/abs/2312.10997 : abstract of the paper named in the text (arXiv API, read 20261102 19:45 UTC)

## 2. DPR (2020) — arXiv 2004.04906

- **Title:** Dense Passage Retrieval for Open-Domain Question Answering
- **Authors:** Vladimir Karpukhin, Barlas Oğuz, Sewon Min (8 in total) [1]
- **Venue:** arXiv comment: "EMNLP 2020" [1]
- **First version:** 20200410 [1]
- **Link:** https://arxiv.org/abs/2004.04906
- **Citations:** 7702, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Abstract [1]: shows that retrieval "can be practically implemented using dense representations alone", with a dual-encoder trained on few question-passage pairs; it beat a Lucene-BM25 system by 9 to 19 points absolute in top-20 accuracy.
  - *widely-built-on:* Cited 7702 times in Semantic Scholar Graph API (read 20261102 20:20 UTC) [2]. Threshold applied in this file: 500 or more.
- **Idea:** Open-domain QA retrieval with a simple dual encoder: learned dense passage and question embeddings, trained from a small number of pairs, replace sparse TF-IDF or BM25 retrieval. It outperforms a strong BM25 baseline on top-20 passage accuracy and sets new end-to-end QA results [1].
- **Relations:**
  - built on by RAG (2005.11401): RAG initialises its retriever and document index from a pre-trained DPR bi-encoder [3].
  - answered much later by BM25 Wins at Scale (2607.26497): that study finds BM25 ahead of dense retrieval at every tier above about 10 million corpus tokens and dense retrieval "consistently less accurate" at shared tiers [4].
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2004.04906 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2004.04906 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 7702 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2005.11401 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)
  4. https://www.alphaxiv.org/abs/2607.26497 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)

## 3. Lost in the Middle (2023) — arXiv 2307.03172

- **Title:** Lost in the Middle: How Language Models Use Long Contexts
- **Authors:** Nelson F. Liu, Kevin Lin, John Hewitt (7 in total) [1]
- **Venue:** arXiv comment: "18 pages, 16 figures. Accepted for publication in Transactions of the Association for Computational Linguistics (TACL), 2023" [1]
- **First version:** 20230706 [1]
- **Link:** https://arxiv.org/abs/2307.03172
- **Citations:** 5799, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *turning-point:* The result most cited when long context is weighed against retrieval: performance "can degrade significantly when changing the position of relevant information" and is lowest when it sits in the middle, "even for explicitly long-context models" [1]. It moved the argument from window size to how the window is used.
  - *widely-built-on:* Cited 5799 times in Semantic Scholar Graph API (read 20261102 20:20 UTC) [2]. Threshold applied in this file: 500 or more.
- **Idea:** Two tasks, multi-document QA and key-value retrieval, are used to test how language models use long input contexts. Accuracy is highest when the relevant item is at the start or end of the context and drops when it is in the middle. The paper offers new evaluation protocols for long-context models [1].
- **Relations:**
  - evaluated by the long-context-versus-retrieval studies: Xu et al. (2310.03025) and Li et al. (2407.16833) test whether retrieval or a long window serves better; the Li abstract describes long-context LLMs that 'understand long contexts directly' [3]. Neither abstract cites Lost in the Middle; unstated whether the full texts do.
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2307.03172 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2307.03172 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 5799 (read 20261102 20:20 UTC)
  3. https://arxiv.org/abs/2407.16833 : abstract of the paper named in the text (arXiv API, read 20261102 19:45 UTC)

## 4. RAG survey (Gao) (2023) — arXiv 2312.10997

- **Title:** Retrieval-Augmented Generation for Large Language Models: A Survey
- **Authors:** Yunfan Gao, Yun Xiong, Xinyu Gao (10 in total) [1]
- **Venue:** arXiv comment: "Ongoing Work" [1]
- **First version:** 20231218 [1]
- **Link:** https://arxiv.org/abs/2312.10997
- **Citations:** 4421, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *survey-of-record:* The survey most often used to map the RAG field: it organises the work into Naive RAG, Advanced RAG and Modular RAG and into retrieval, generation and augmentation techniques [1]. Weighting by citations: see the count above, the highest of the RAG surveys read.
  - *widely-built-on:* Cited 4421 times in Semantic Scholar Graph API (read 20261102 20:20 UTC) [2]. Threshold applied in this file: 500 or more.
- **Idea:** A review of RAG as a response to hallucination, outdated knowledge and untraceable reasoning in LLMs. It describes the progression of paradigms (Naive, Advanced, Modular), the three-part foundation (retrieval, generation, augmentation), the technologies in each, and evaluation frameworks and benchmarks [1].
- **Relations:**
  - surveys the pattern named by RAG (2005.11401): the abstract defines RAG as 'incorporating knowledge from external databases' [1].
  - alternative surveys: Fan et al. (2405.06211, KDD 2024) and Wu et al. (2407.13193); the GraphRAG-specific surveys are listed separately.
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2312.10997 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2312.10997 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 4421 (read 20261102 20:20 UTC)

## 5. REALM (2020) — arXiv 2002.08909

- **Title:** REALM: Retrieval-Augmented Language Model Pre-Training
- **Authors:** Kelvin Guu, Kenton Lee, Zora Tung (5 in total) [1]
- **Venue:** Semantic Scholar venue field (not checked against the paper): International Conference on Machine Learning [1]
- **First version:** 20200210 [1]
- **Link:** https://arxiv.org/abs/2002.08909
- **Citations:** 3596, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Abstract [1]: "For the first time, we show how to pre-train such a knowledge retriever in an unsupervised manner", using masked language modelling and back-propagating through retrieval over millions of documents. It introduces retrieval-augmented language-model pre-training.
  - *widely-built-on:* Cited 3596 times in Semantic Scholar Graph API (read 20261102 20:20 UTC) [2]. Threshold applied in this file: 500 or more.
- **Idea:** Augments language-model pre-training with a latent knowledge retriever that retrieves and attends over documents from a corpus such as Wikipedia during pre-training, fine-tuning and inference. The retriever is trained without labels, with masked-word prediction as the learning signal. On three open-domain QA benchmarks it beats prior explicit and implicit knowledge-storage models [1].
- **Relations:**
  - built on by RAG (2005.11401): the RAG full text names REALM and ORQA as models that combine a masked language model with a differentiable retriever, and RAG adds generation ('extractive' only before) [3].
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2002.08909 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2002.08909 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 3596 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2005.11401 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)

## 6. Self-RAG (2023) — arXiv 2310.11511

- **Title:** Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection
- **Authors:** Akari Asai, Zeqiu Wu, Yizhong Wang (5 in total) [1]
- **Venue:** arXiv comment: "30 pages, 2 figures, 12 tables" [1]
- **First version:** 20231017 [1]
- **Link:** https://arxiv.org/abs/2310.11511
- **Citations:** 3006, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Introduces learned, on-demand retrieval with self-critique: "a new framework called Self-Reflective Retrieval-Augmented Generation (Self-RAG)" in which one LM "adaptively retrieves passages on-demand" and reflects with special reflection tokens [1].
  - *widely-built-on:* Cited 3006 times in Semantic Scholar Graph API (read 20261102 20:20 UTC) [2]. Threshold applied in this file: 500 or more.
- **Idea:** Instead of retrieving a fixed number of passages every time, one LM is trained to decide when to retrieve, and to generate and critique its output and the passages with special reflection tokens. The tokens make behaviour controllable at inference time [1].
- **Relations:**
  - answers RAG (2005.11401): the abstract criticises 'indiscriminately retrieving and incorporating a fixed number of retrieved passages, regardless of whether retrieval is necessary' [1].
  - precedes the agentic and reinforcement-learned retrievers (Search-R1, 2503.09516; Graph-R1, 2507.21892), which also let the model decide when to retrieve; the papers read do not cite each other (abstracts).
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2310.11511 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2310.11511 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 3006 (read 20261102 20:20 UTC)

## 7. GraphRAG (2024) — arXiv 2404.16130

- **Title:** From Local to Global: A Graph RAG Approach to Query-Focused Summarization
- **Authors:** Darren Edge, Ha Trinh, Newman Cheng (10 in total) [1]
- **Venue:** Semantic Scholar venue field (not checked against the paper): arXiv.org [1]
- **First version:** 20240424 [1]
- **Link:** https://arxiv.org/abs/2404.16130
- **Citations:** 2489, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Introduces the named approach: "GraphRAG", an LLM-built entity knowledge graph plus pregenerated community summaries, aimed at global questions over a corpus that RAG "fails on" [1]. Microsoft's release repository and 20240702 post are described on the llm-era archive page.
  - *widely-built-on:* Cited 2489 times in Semantic Scholar Graph API (read 20261102 20:20 UTC) [2]. Threshold applied in this file: 500 or more.
- **Idea:** Vector RAG fails on global questions such as 'What are the main themes in the dataset?', which are query-focused summarisation tasks. GraphRAG has an LLM extract an entity knowledge graph from the documents, then pregenerate summaries for every community of closely related entities. At query time each community summary yields a partial answer and the partial answers are summarised into a final one. On corpora around 1 million tokens it improves comprehensiveness and diversity over a conventional RAG baseline [1].
- **Relations:**
  - answers RAG (2005.11401): global sensemaking questions are the case where passage retrieval fails (abstract) [1].
  - answered by LightRAG (2410.05779): its report states LightRAG 'consistently outperformed GraphRAG' on UltraDomain with far fewer retrieval tokens (<100 against 610,000 on the Legal set), per the authors [3].
  - answered by LinearRAG, LogicRAG (2510.10114, 2508.06105) on the cost of building the graph [4].
  - evaluated by RAG vs GraphRAG (2502.11371), which runs Community-GraphRAG Local and Global and finds Global 'often struggles on QA' [5]; by GraphRAG-Bench (2506.05690); by BM25 Wins at Scale (2607.26497), where MS-GraphRAG's full-scale build is estimated at 7.9 billion tokens [6]; and used as a backend in RAGSearch (2604.09666).
- **Read:** Abstract only (arXiv API record); behaviour in later evaluations from the alphaXiv reports and full text noted in the relations. Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2404.16130 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2404.16130 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 2489 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2410.05779 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)
  4. arXiv API records of the other papers named in this entry (abstracts; read 20261102 19:45 to 19:59 UTC)
  5. https://www.alphaxiv.org/abs/2502.11371 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)
  6. https://www.alphaxiv.org/abs/2607.26497 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)

## 8. Search-R1 (2025) — arXiv 2503.09516

- **Title:** Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning
- **Authors:** Bowen Jin, Hansi Zeng, Zhenrui Yue (8 in total) [1]
- **Venue:** arXiv comment: "31 pages" [1]
- **First version:** 20250312 [1]
- **Link:** https://arxiv.org/abs/2503.09516
- **Citations:** 1742, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Introduces learning multi-turn search by reinforcement learning with only an outcome reward and "retrieved token masking for stable RL training"; "improves performance by 41% (Qwen2.5-7B) and 20% (Qwen2.5-3B) over various RAG baselines" (first-party) [1].
  - *widely-built-on:* Cited 1742 times in Semantic Scholar Graph API (read 20261102 20:20 UTC) [2]. Threshold applied in this file: 500 or more.
- **Idea:** Prompting a strong LLM to use a search engine is often suboptimal. Search-R1 extends reinforcement learning for reasoning so the LLM learns to generate several search queries during step-by-step reasoning with real-time retrieval, trained with a simple outcome-based reward over multi-turn trajectories. Code and checkpoints are public [1].
- **Relations:**
  - used as the plain-text RL baseline by Graph-R1 (2507.21892): average F1 46.19 for Search-R1 against 57.82 for Graph-R1 on Qwen2.5-7B (first-party) [3], and as an RL backend in RAGSearch (2604.09666) [4].
  - compared with training-free agentic search (Search-o1, 2501.05366) in RAGSearch, where well-designed training-free workflows (GraphSearch) 'often outperform' the RL-trained Search-R1 and Graph-R1 variants [4].
- **Read:** Abstract; baseline role from the alphaXiv reports of Graph-R1 and RAGSearch. Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2503.09516 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2503.09516 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 1742 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2507.21892 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)
  4. https://www.alphaxiv.org/abs/2604.09666 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)

## 9. RETRO (2021) — arXiv 2112.04426

- **Title:** Improving language models by retrieving from trillions of tokens
- **Authors:** Sebastian Borgeaud, Arthur Mensch, Jordan Hoffmann (28 in total) [1]
- **Venue:** arXiv comment: "Fix incorrect reported numbers in Table 14" [1]
- **First version:** 20211208 [1]
- **Link:** https://arxiv.org/abs/2112.04426
- **Citations:** 2015, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Origin of retrieval-enhanced language modelling at pre-training scale: conditioning on chunks retrieved from a "2 trillion token database" gives GPT-3-level results on the Pile "despite using 25x fewer parameters" [1].
  - *widely-built-on:* Cited 2015 times in Semantic Scholar Graph API (read 20261102 20:20 UTC) [2]. Threshold applied in this file: 500 or more.
- **Idea:** A Retrieval-Enhanced Transformer (RETRO) conditions an auto-regressive language model on document chunks retrieved from a large corpus by local similarity to the preceding tokens. It uses a frozen BERT retriever, a differentiable encoder and chunked cross-attention. It is usually trained from scratch but existing transformers can be retrofitted [1].
- **Relations:**
  - same family as REALM (2002.08909) and RAG (2005.11401): knowledge kept outside the weights; RETRO puts retrieval into pre-training at much larger scale, where RAG fine-tunes a pretrained generator with a retriever. The RETRO abstract does not cite either (abstract only; unstated whether the full text does).
  - followed by Atlas (2208.03299, few-shot retrieval-augmented language model; not proposed, see the last section).
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2112.04426 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2112.04426 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 2015 (read 20261102 20:20 UTC)

## 10. IRCoT (2022) — arXiv 2212.10509

- **Title:** Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions
- **Authors:** Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot (4 in total) [1]
- **Venue:** arXiv comment: "ACL'23 Camera Ready" [1]
- **First version:** 20221220 [1]
- **Link:** https://arxiv.org/abs/2212.10509
- **Citations:** 1479, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Origin of interleaving retrieval with reasoning steps: "what to retrieve depends on what has already been derived", so it "interleaves retrieval with steps (sentences) in a CoT"; up to 21 points better retrieval and 15 points better QA on four multi-hop datasets (first-party) [1] (ACL 2023 per the arXiv comment).
  - *widely-built-on:* Cited 1479 times in Semantic Scholar Graph API (read 20261102 20:20 UTC) [2]. Threshold applied in this file: 500 or more.
- **Idea:** One-step retrieve-and-read is insufficient for multi-step question answering. IRCoT alternates between generating a chain-of-thought sentence and retrieving with it, using the retrieved text to improve the next step. It needs no extra training and works with GPT-3 and with Flan-T5-large [1].
- **Relations:**
  - answers one-step RAG (2005.11401): the abstract calls the one-step retrieve-and-read approach "insufficient for multi-step QA" [1].
  - answered by HippoRAG (2405.14831): single-step retrieval with HippoRAG matches or beats IRCoT while being 10 to 30 times cheaper and 6 to 13 times faster (first-party) [3].
  - ancestor of the agentic-retrieval line (Search-o1, 2501.05366; Search-R1, 2503.09516; Graph-R1, 2507.21892) in which the model decides what to retrieve next; none of those abstracts cites IRCoT (unstated for the full texts).
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:58 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2212.10509 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2212.10509 (read 20261102 19:58 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 1479 (read 20261102 20:20 UTC)
  3. https://arxiv.org/abs/2405.14831 : abstract of the paper named in the text (arXiv API, read 20261102 19:45 UTC)

## 11. RAG survey (Fan) (2024) — arXiv 2405.06211

- **Title:** A Survey on RAG Meeting LLMs: Towards Retrieval-Augmented Large Language Models
- **Authors:** Wenqi Fan, Yujuan Ding, Liangbo Ning (8 in total) [1]
- **Venue:** arXiv comment: "This is the long version of the corresponding survey paper accepted by KDD2024" [1]
- **First version:** 20240510 [1]
- **Link:** https://arxiv.org/abs/2405.06211
- **Citations:** 1245, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *survey-of-record:* Second survey of record for RA-LLMs; arXiv comment [1]: "long version of the corresponding survey paper accepted by KDD2024". It reviews architectures, training strategies and applications of retrieval-augmented LLMs. Selected on its citation count (see above) next to Gao et al.
  - *widely-built-on:* Cited 1245 times in Semantic Scholar Graph API (read 20261102 20:20 UTC) [2]. Threshold applied in this file: 500 or more.
- **Idea:** Reviews retrieval-augmented large language models (RA-LLMs) from three technical perspectives: architectures, training strategies and applications; it also discusses challenges and future directions [1].
- **Relations:**
  - parallel to the Gao et al. survey (2312.10997); neither cites the other in what was read (abstracts only).
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2405.06211 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2405.06211 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 1245 (read 20261102 20:20 UTC)

## 12. RAPTOR (2024) — arXiv 2401.18059

- **Title:** RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval
- **Authors:** Parth Sarthi, Salman Abdullah, Aditi Tuli (6 in total) [1]
- **Venue:** Semantic Scholar venue field (not checked against the paper): International Conference on Learning Representations [1]
- **First version:** 20240131 [1]
- **Link:** https://arxiv.org/abs/2401.18059
- **Citations:** 840, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Origin of tree-organised retrieval: "recursively embedding, clustering, and summarizing chunks of text, constructing a tree with differing levels of summarization from the bottom up"; retrieval spans all levels [1]. It is the tree-based backend in later GraphRAG comparisons.
  - *widely-built-on:* Cited 840 times in Semantic Scholar Graph API (read 20261102 20:20 UTC) [2]. Threshold applied in this file: 500 or more.
- **Idea:** Most retrieval returns short contiguous chunks, which limits holistic understanding of a long document. RAPTOR clusters and summarises chunks recursively into a tree and retrieves across levels of abstraction. Coupled with GPT-4 it improves the best QuALITY accuracy by 20% absolute (first-party) [1].
- **Relations:**
  - same problem as GraphRAG (2404.16130): both pre-compute summaries over groups of chunks; RAPTOR clusters by embedding, GraphRAG by entity community [3].
  - evaluated as a tree-based baseline in RAG vs GraphRAG (2502.11371), GraphRAG-Bench (2506.05690) and RAGSearch (2604.09666); LinearRAG reports 12.8 and 15.1 times faster indexing than RAPTOR on 5M and 10M-token subsets [4].
- **Read:** Abstract only (arXiv API record); later use from the evaluation reports. Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2401.18059 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2401.18059 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 840 (read 20261102 20:20 UTC)
  3. arXiv API records of the other papers named in this entry (abstracts; read 20261102 19:45 to 19:59 UTC)
  4. alphaXiv reports of the evaluation papers named in this entry (derived summaries; read 20261102 20:00 to 20:06 UTC)

## 13. GraphRAG survey (Peng) (2024) — arXiv 2408.08921

- **Title:** Graph Retrieval-Augmented Generation: A Survey
- **Authors:** Boci Peng, Yun Zhu, Yongchao Liu (8 in total) [1]
- **Venue:** arXiv comment: "Ongoing work. Compared to the first version, several references have been added and a GitHub repository link has been provided" [1]
- **First version:** 20240815 [1]
- **Link:** https://arxiv.org/abs/2408.08921
- **Citations:** 695, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *survey-of-record:* Abstract [1]: "the first comprehensive overview of GraphRAG methodologies"; its three-stage workflow (graph-based indexing, graph-guided retrieval, graph-enhanced generation) is its organising frame. It is the earliest of the three GraphRAG surveys read (20240815). Among the three GraphRAG surveys read it has the most citations (see the count above against 2501.00309 and 2501.13958 in the last section).
  - *widely-built-on:* Cited 695 times in Semantic Scholar Graph API (read 20261102 20:20 UTC) [2]. Threshold applied in this file: 500 or more.
- **Idea:** Formalises the GraphRAG workflow as Graph-Based Indexing, Graph-Guided Retrieval and Graph-Enhanced Generation, outlines the core technologies and training methods at each stage, then covers downstream tasks, application domains, evaluation methodologies and industrial use cases; keeps a public paper repository [1].
- **Relations:**
  - parallel surveys: Han et al. (2501.00309) and Zhang et al. (2501.13958); the three are the surveys listed by the archive page kb-kg/papers-benchmarks/README.md.
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2408.08921 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2408.08921 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 695 (read 20261102 20:20 UTC)

## 14. LightRAG (2024) — arXiv 2410.05779

- **Title:** LightRAG: Simple and Fast Retrieval-Augmented Generation
- **Authors:** Zirui Guo, Lianghao Xia, Yanhua Yu (5 in total) [1]
- **Venue:** Semantic Scholar venue field (not checked against the paper): Conference on Empirical Methods in Natural Language Processing [1]
- **First version:** 20241008 [1]
- **Link:** https://arxiv.org/abs/2410.05779
- **Citations:** 577, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Introduced the dual-level (low-level entity, high-level theme) graph retrieval and an incremental graph-update algorithm [1]; the project is the most-starred document-graph repository in the archive (kb-kg/literature/graph-rag-research.md, 40,443 stars on 20261030).
  - *widely-built-on:* Cited 577 times in Semantic Scholar Graph API (read 20261102 20:20 UTC) [2]. Threshold applied in this file: 500 or more.
- **Idea:** Puts a graph structure into the text index. An LLM extracts entities and relations from chunks, profiles each into a key-value pair, and merges duplicates. Retrieval is dual-level: low-level keywords match entities, high-level keywords match relations/themes, with vector search over the keys and one-hop neighbours added. New documents are merged into the graph by union, so the index is not rebuilt [1] [3].
- **Relations:**
  - answers GraphRAG (2404.16130): the report states LightRAG replaces community traversal with vector lookup, using under 100 tokens and one API call per query against 610,000 tokens for GraphRAG on the Legal dataset (first-party) [3].
  - evaluated by GraphRAG-Bench (2506.05690), BM25 Wins at Scale (2607.26497; super-linear build, 'failing to complete at 2,826 documents') [4]; LinearRAG (2510.10114) reports LightRAG indexing at 4,933 s on 2Wiki against 250 s for itself [5].
- **Read:** Abstract and alphaXiv report (20261102 20:03). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2410.05779 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2410.05779 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 577 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2410.05779 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)
  4. https://www.alphaxiv.org/abs/2607.26497 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)
  5. https://www.alphaxiv.org/abs/2510.10114 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)

## 15. HippoRAG (2024) — arXiv 2405.14831

- **Title:** HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models
- **Authors:** Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu (5 in total) [1]
- **Venue:** arXiv comment: "NeurIPS 2024. Code and data: https://github.com/OSU-NLP-Group/HippoRAG" [1]
- **First version:** 20240523 [1]
- **Link:** https://arxiv.org/abs/2405.14831
- **Citations:** 437, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Origin of Personalized-PageRank retrieval over an LLM-built knowledge graph for RAG: "synergistically orchestrates LLMs, knowledge graphs, and the Personalized PageRank algorithm" [1] (NeurIPS 2024 per the arXiv comment).
- **Idea:** Inspired by the hippocampal indexing theory of human long-term memory. An LLM builds a knowledge graph from the corpus; at query time Personalized PageRank spreads from the query's entities to find relevant passages. On multi-hop QA it beats the then state of the art by up to 20%, and single-step retrieval matches or beats iterative retrieval such as IRCoT while being 10 to 30 times cheaper and 6 to 13 times faster, per the authors [1].
- **Relations:**
  - built on by HippoRAG 2 (2502.14802): 'builds upon the Personalized PageRank algorithm used in HippoRAG' [3].
  - answers iterative retrieval such as IRCoT (2212.10509, interleaving retrieval with chain-of-thought): abstract claims 10 to 30 times cheaper and 6 to 13 times faster, first-party [1].
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2405.14831 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2405.14831 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 437 (read 20261102 20:20 UTC)
  3. https://arxiv.org/abs/2502.14802 : abstract of the paper named in the text (arXiv API, read 20261102 19:45 UTC)

## 16. G-Retriever (2024) — arXiv 2402.07630

- **Title:** G-Retriever: Retrieval-Augmented Generation for Textual Graph Understanding and Question Answering
- **Authors:** Xiaoxin He, Yijun Tian, Yifei Sun (8 in total) [1]
- **Venue:** Semantic Scholar venue field (not checked against the paper): Neural Information Processing Systems [1]
- **First version:** 20240212 [1]
- **Link:** https://arxiv.org/abs/2402.07630
- **Citations:** 417, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Abstract [1]: "the first retrieval-augmented generation (RAG) approach for general textual graphs", casting retrieval as a Prize-Collecting Steiner Tree problem, with a GraphQA benchmark.
- **Idea:** Lets a user 'chat with' a graph whose nodes and edges carry text (scene graphs, commonsense and knowledge graphs). Retrieval over the graph is posed as a Prize-Collecting Steiner Tree optimisation, so graphs larger than the LLM context can be used and hallucination is resisted; the model is tuned by soft prompting. Outperforms baselines on textual-graph tasks from several domains [1].
- **Relations:**
  - evaluated as a baseline by LinearRAG (2510.10114), whose report says G-Retriever and LightRAG "incur significant time costs and LLM token consumption" in indexing and retrieval [3].
  - different input from GraphRAG (2404.16130): G-Retriever starts from an existing textual graph, GraphRAG from raw text; the two lines meet in HippoRAG (2405.14831), which builds the graph from text with an LLM [4].
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2402.07630 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2402.07630 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 417 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2510.10114 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)
  4. arXiv API records of the other papers named in this entry (abstracts; read 20261102 19:45 to 19:59 UTC)

## 17. Think-on-Graph (2023) — arXiv 2307.07697

- **Title:** Think-on-Graph: Deep and Responsible Reasoning of Large Language Model on Knowledge Graph
- **Authors:** Jiashuo Sun, Chengjin Xu, Lumingyuan Tang (9 in total) [1]
- **Venue:** arXiv comment: "Accepted by ICLR 2024" [1]
- **First version:** 20230715 [1]
- **Link:** https://arxiv.org/abs/2307.07697
- **Citations:** 373, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Introduces the "LLM ⊗ KG" paradigm in which the LLM is "an agent to interactively explore related entities and relations on KGs" with beam search over reasoning paths, training-free [1] (ICLR 2024 per the arXiv comment).
- **Idea:** Large language models hallucinate on deep, knowledge-intensive reasoning. Think-on-Graph (ToG) treats the LLM as an agent that iteratively runs beam search on a knowledge graph, discovers the most promising reasoning paths and returns the answer. It needs no training, works with different LLMs and KGs, and the authors report small models beating GPT-4 in some cases [1].
- **Relations:**
  - same agent-explores-a-graph pattern, later trained end to end by Graph-R1 (2507.21892) on an LLM-built hypergraph and GraphRAG-R1 (2507.23581); the Graph-R1 abstract frames retrieval as 'multi-turn agent-environment interaction' [3]. Neither abstract cites ToG; unstated whether the full texts do.
  - follow-ups by other groups in the same line, not proposed here: Think-on-Graph 2.0 (2407.10805), Reasoning on Graphs (2310.01061), Graph-constrained Reasoning (2410.13080).
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2307.07697 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2307.07697 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 373 (read 20261102 20:20 UTC)
  3. https://arxiv.org/abs/2507.21892 : abstract of the paper named in the text (arXiv API, read 20261102 19:45 UTC)

## 18. HippoRAG 2 (2025) — arXiv 2502.14802

- **Title:** From RAG to Memory: Non-Parametric Continual Learning for Large Language Models
- **Authors:** Bernal Jiménez Gutiérrez, Yiheng Shu, Weijian Qi (5 in total) [1]
- **Venue:** arXiv comment: "ICML 2025. Code and data are available at: https://github.com/OSU-NLP-Group/HippoRAG" [1]
- **First version:** 20250220 [1]
- **Link:** https://arxiv.org/abs/2502.14802
- **Citations:** 284, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *turning-point:* Answers the dispute over whether structure-augmented RAG loses on plain facts: the abstract says structure-augmented RAG "drops considerably below standard RAG" on basic factual memory, and HippoRAG 2 is built to beat standard RAG on factual, sense-making and associative tasks together [1]. In the independent evaluations read it is the best graph backend: RAGSearch finds it gives "the largest gains over dense RAG" [3]; RAG vs GraphRAG lists it among the methods that 'excel on multi-hop queries' [4].
- **Idea:** Frames RAG as a route to non-parametric continual learning. HippoRAG 2 keeps Personalized PageRank from HippoRAG and adds deeper passage integration and more effective online use of an LLM. It reports a 7% improvement over the state-of-the-art embedding model on associative-memory tasks, together with better factual and sense-making memory (first-party, ICML 2025 per the arXiv comment) [1].
- **Relations:**
  - builds on HippoRAG (2405.14831): HippoRAG 2 "builds upon the Personalized PageRank algorithm used in HippoRAG" [1].
  - answers GraphRAG-style methods: the abstract says 'recent RAG approaches augment vector embeddings with various structures like knowledge graphs' but fall below standard RAG on basic factual tasks [1].
  - evaluated by RAG vs GraphRAG (2502.11371), GraphRAG-Bench (2506.05690; HippoRAG2 'led in Context Relevance' on the novel set), RAGSearch (2604.09666) and BM25 Wins at Scale (2607.26497; build estimated at 2.9 billion generative tokens at full scale and 15 points below BM25 at 155M corpus tokens) [5].
- **Read:** Abstract; results as reported in the alphaXiv reports of the evaluation papers. Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2502.14802 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2502.14802 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 284 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2604.09666 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)
  4. https://www.alphaxiv.org/abs/2502.11371 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)
  5. alphaXiv reports of the evaluation papers named in this entry (derived summaries; read 20261102 20:00 to 20:06 UTC)

## 19. RAG or Long-Context LLMs (2024) — arXiv 2407.16833

- **Title:** Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach
- **Authors:** Zhuowan Li, Cheng Li, Mingyang Zhang (5 in total) [1]
- **Venue:** arXiv comment: "Accepted to EMNLP 2024 industry track" [1]
- **First version:** 20240723 [1]
- **Link:** https://arxiv.org/abs/2407.16833
- **Citations:** 199, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *turning-point:* Frames the decision as routing: "when resourced sufficiently, LC consistently outperforms RAG" on average, but RAG "remains a distinct advantage" in cost; proposes Self-Route to send each query to RAG or long context [1] (EMNLP 2024 industry track per the arXiv comment).
- **Idea:** Benchmarks RAG against long-context (LC) LLMs on public datasets with three recent LLMs. LC wins on average performance if resources allow, RAG is much cheaper, and Self-Route lets the model decide which path to use for each query, cutting cost at near-LC quality [1].
- **Relations:**
  - answers Retrieval meets Long Context (2310.03025): both ask whether retrieval or a long window is better; the Li result favours LC on accuracy where Xu et al. favour retrieval on compute [3].
  - answered by Cache-Augmented Generation (2412.15605), which removes retrieval for small corpora by preloading them into the long context [4].
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2407.16833 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2407.16833 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 199 (read 20261102 20:20 UTC)
  3. arXiv API records of the other papers named in this entry (abstracts; read 20261102 19:45 to 19:59 UTC)
  4. https://arxiv.org/abs/2412.15605 : abstract of the paper named in the text (arXiv API, read 20261102 19:45 UTC)

## 20. Retrieval meets Long Context (2023) — arXiv 2310.03025

- **Title:** Retrieval meets Long Context Large Language Models
- **Authors:** Peng Xu, Wei Ping, Xianchao Wu (10 in total) [1]
- **Venue:** arXiv comment: "Published at ICLR 2024" [1]
- **First version:** 20231004 [1]
- **Link:** https://arxiv.org/abs/2310.03025
- **Citations:** 158, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *turning-point:* An early controlled comparison (ICLR 2024 per the arXiv comment [1]): a 4K-window LLM with simple retrieval is "comparable" to a fine-tuned 16K-window LLM at much less compute, and retrieval helps "regardless of their extended context window sizes" [1].
- **Idea:** Compares retrieval augmentation with extended context windows on a proprietary 43B GPT and Llama2-70B over nine long-context tasks. Retrieval with a short window matches a fine-tuned long window at lower cost, and retrieval still adds to long-window models [1].
- **Relations:**
  - answered from the other side by Li et al. (2407.16833): with enough resources long context "consistently outperforms RAG" on average, but at higher cost [3].
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2310.03025 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2310.03025 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 158 (read 20261102 20:20 UTC)
  3. https://arxiv.org/abs/2407.16833 : abstract of the paper named in the text (arXiv API, read 20261102 19:45 UTC)

## 21. KAG (2024) — arXiv 2409.13731

- **Title:** KAG: Boosting LLMs in Professional Domains via Knowledge Augmented Generation
- **Authors:** Lei Liang, Mengshu Sun, Zhengke Gui (19 in total) [1]
- **Venue:** arXiv comment: "33 pages" [1]
- **First version:** 20240910 [1]
- **Link:** https://arxiv.org/abs/2409.13731
- **Citations:** 152, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Names Knowledge Augmented Generation and argues vector similarity differs from reasoning relevance and is blind to numbers, time and rules; five components incl. "mutual-indexing between knowledge graphs and original chunks" and a "logical-form-guided hybrid reasoning engine" [1]. Deployed in two Ant Group services (first-party) [1].
- **Idea:** A domain knowledge service framework for professional settings that combines a knowledge graph with vector retrieval: LLM-friendly knowledge representation, mutual indexing of KG and chunks, a logical-form-guided hybrid reasoner, semantic alignment, and model-capability enhancement. Reported relative F1 gains of 19.6% on 2Wiki and 33.5% on HotpotQA over state-of-the-art RAG, and applied to E-Government and E-Health Q&A (first-party) [1].
- **Relations:**
  - grouped with GraphRAG, LightRAG, StructRAG as an early GraphRAG effort in GraphRAG-Bench (2506.05690) [3].
  - different emphasis from the Microsoft/HKU line: a logic and schema engine, closer to the symbolic KB/KG tradition than to community summaries (reading of the abstract).
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2409.13731 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2409.13731 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 152 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2409.13731 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)

## 22. RAG vs GraphRAG (2025) — arXiv 2502.11371

- **Title:** RAG vs. GraphRAG: A Systematic Evaluation and Key Insights
- **Authors:** Haoyu Han, Li Ma, Yu Wang (12 in total) [1]
- **Venue:** Semantic Scholar venue field (not checked against the paper): Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2 [1]
- **First version:** 20250217 [1]
- **Link:** https://arxiv.org/abs/2502.11371
- **Citations:** 118, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *turning-point:* Independent, unified comparison on text benchmarks: RAG "excels on detailed single-hop queries"; GraphRAG methods "excel on multi-hop queries"; the Global community variant 'often struggles on QA' [3]. It supplied the first controlled evidence that neither side wins everywhere, before GraphRAG-Bench.
- **Idea:** GraphRAG systems for text were tailored to particular tasks and datasets with heterogeneous evaluation protocols. This paper standardises preprocessing, retrieval and generation settings and compares RAG with GraphRAG (KG-GraphRAG, Community-GraphRAG Local and Global, HippoRAG2, RAPTOR) on question answering and query-based summarisation, then explores selecting or integrating the two paradigms for consistent gains [1] [3].
- **Relations:**
  - evaluates GraphRAG (2404.16130; the 'Community-GraphRAG' variants), HippoRAG 2 (2502.14802) and RAPTOR (2401.18059), each as a representative method [3].
  - answered by GraphRAG-Bench (2506.05690), which adds tasks and a graded benchmark; related findings in RAGSearch (2604.09666).
  - run by the authors of the Han et al. GraphRAG survey (2501.00309) per the arXiv author lists.
- **Read:** Abstract and full text (alphaXiv extraction, grepped for method list and findings, 20261102 20:06). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2502.11371 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2502.11371 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 118 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2502.11371 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)

## 23. Cache-Augmented Generation (2024) — arXiv 2412.15605

- **Title:** Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks
- **Authors:** Brian J Chan, Chao-Ting Chen, Jui-Hung Cheng (4 in total) [1]
- **Venue:** arXiv comment: "5 pages, accepted by the Web Conference 2025 (WWW '25) as a short paper" [1]
- **First version:** 20241220 [1]
- **Link:** https://arxiv.org/abs/2412.15605
- **Citations:** 86, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Proposes cache-augmented generation (CAG) as "an alternative paradigm" that bypasses real-time retrieval by preloading the knowledge into the long context and caching runtime parameters [1]. The llm-era archive page already lists it as a retreat from retrieval itself.
- **Idea:** For corpora small enough to fit, preload all relevant documents into an LLM's extended context and cache its key-value state, then answer without any retrieval step. The paper reports no retrieval latency and fewer retrieval errors, with benchmarks where long-context LLMs outperform or complement traditional RAG [1].
- **Relations:**
  - answers RAG (2005.11401): the abstract lists RAG's 'retrieval latency, potential errors in document selection, and increased system complexity' [1].
  - bounded by the long-context studies (2407.16833; 2307.03172): preloading depends on the model using the whole window.
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2412.15605 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2412.15605 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 86 (read 20261102 20:20 UTC)

## 24. Graph-R1 (2025) — arXiv 2507.21892

- **Title:** Graph-R1: Towards Agentic GraphRAG Framework via End-to-end Reinforcement Learning
- **Authors:** Haoran Luo, Haihong E, Guanting Chen (11 in total) [1]
- **Venue:** journal reference: ICML 2026; arXiv comment: "Accepted by ICML 2026 main conference" [1]
- **First version:** 20250729 [1]
- **Link:** https://arxiv.org/abs/2507.21892
- **Citations:** 64, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Abstract [1]: "the first agentic GraphRAG framework via end-to-end reinforcement learning" (ICML 2026 main conference per the arXiv record), with a lightweight hypergraph and retrieval as multi-turn agent-environment interaction.
- **Idea:** GraphRAG methods have high construction cost, fixed one-time retrieval, and depend on long-context reasoning and prompt design. Graph-R1 builds a lightweight knowledge hypergraph (n-ary facts), lets the agent think, query, retrieve and rethink over several turns, and trains it with an end-to-end reward (GRPO) combining answer and format. It beats traditional GraphRAG and RL-enhanced RAG on standard RAG datasets, per the authors [1].
- **Relations:**
  - builds on Search-R1 (2503.09516): RL multi-turn search is the baseline it improves on (average F1 57.82 against 46.19 on Qwen2.5-7B, first-party) [3].
  - evaluated by RAGSearch (2604.09666): RL-based agents with a HippoRAG2 backend reach the strongest results on HotpotQA, PopQA and 2Wiki, but 'GraphSearch-based systems, despite being training-free, often outperform' Search-R1 and Graph-R1 [4].
- **Read:** Abstract and alphaXiv report (20261102 20:00). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2507.21892 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2507.21892 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 64 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2507.21892 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)
  4. https://www.alphaxiv.org/abs/2604.09666 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)

## 25. GraphRAG-Bench (When to use graphs) (2025) — arXiv 2506.05690

- **Title:** When to use Graphs in RAG: A Comprehensive Analysis for Graph Retrieval-Augmented Generation
- **Authors:** Zhishang Xiang, Chuanjie Wu, Qinggang Zhang (7 in total) [1]
- **Venue:** arXiv comment: "All resources and analyses are collected at https://github.com/GraphRAG-Bench/GraphRAG-Benchmark" [1]
- **First version:** 20250606 [1]
- **Link:** https://arxiv.org/abs/2506.05690
- **Citations:** 60, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *turning-point:* States the question the field then organised around: "recent studies report that GraphRAG frequently underperforms vanilla RAG on many real-world tasks" and builds a four-level benchmark to find when graphs help [1] (ICLR 2026 per the alphaXiv report, which is a secondary source; the arXiv page names no venue).
- **Idea:** GraphRAG-Bench has tasks of rising difficulty (fact retrieval, complex reasoning, contextual summarisation, creative generation) over two corpora (NCCN medical guidelines and pre-20th-century novels) with stage-by-stage metrics: graph construction, retrieval, generation. Plain RAG matches or beats GraphRAG on simple fact retrieval; GraphRAG wins on complex reasoning, summarisation and creative tasks, at the cost of prompt inflation [1] [3].
- **Relations:**
  - evaluates seven GraphRAG frameworks, among them MS-GraphRAG (2404.16130), HippoRAG (2405.14831), HippoRAG2 (2502.14802), LightRAG (2410.05779), RAPTOR (2401.18059), KAG (2409.13731), against RAG with and without reranking [3].
  - not to be confused with a different benchmark of the same name (2506.02404, Xiao et al., domain-specific college-level questions); both appeared June 2025 [4].
  - answered by RAGSearch (2604.09666), which asks whether agentic search removes the need for graphs.
- **Read:** Abstract and alphaXiv report (20261102 20:01). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2506.05690 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2506.05690 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 60 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2506.05690 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)
  4. arXiv API records of the other papers named in this entry (abstracts; read 20261102 19:45 to 19:59 UTC)

## 26. LinearRAG (2025) — arXiv 2510.10114

- **Title:** LinearRAG: Linear Graph Retrieval Augmented Generation on Large-scale Corpora
- **Authors:** Luyao Zhuang, Shengyuan Chen, Yilin Xiao (8 in total) [1]
- **Venue:** Semantic Scholar venue field (not checked against the paper): arXiv.org [1]
- **First version:** 20251011 [1]
- **Link:** https://arxiv.org/abs/2510.10114
- **Citations:** 70, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Origin of the relation-free, token-free graph: "constructs a relation-free hierarchical graph, termed Tri-Graph, using only lightweight entity extraction and semantic linking", linear in corpus size, "no extra token consumption" [1]. In BM25 Wins at Scale it is the only graph method with zero generative build calls [3].
- **Idea:** Relation extraction by LLM is unstable and costly and gives noisy graphs. LinearRAG builds a Tri-Graph of passages, sentences and entities from lightweight named-entity recognition only, then retrieves in two stages: entity activation by semantic bridging, then passage ranking by Personalized PageRank over the activated entities. Reported on four datasets, first-party [1] [4].
- **Relations:**
  - answers LightRAG (2410.05779), G-Retriever (2402.07630), GraphRAG (2404.16130): the report's cost table has LightRAG indexing at 4,933 s against 250 s for LinearRAG on 2Wiki (first-party) [4].
  - builds on HippoRAG (2405.14831) in the retrieval step (Personalized PageRank) and uses HippoRAG2 as its strongest baseline; a case study where HippoRAG2 fails because of a relation missing from its extracted triples [4].
  - evaluated by BM25 Wins at Scale (2607.26497): 'finishing within 1.8 points of MS-GraphRAG and LightRAG at the bedrock' with no generative build calls [3]; and as a backend in RAGSearch (2604.09666).
- **Read:** Abstract and alphaXiv report (20261102 20:03). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2510.10114 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2510.10114 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 70 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2607.26497 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)
  4. https://www.alphaxiv.org/abs/2510.10114 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)

## 27. LogicRAG (2025) — arXiv 2508.06105

- **Title:** You Don't Need Pre-built Graphs for RAG: Retrieval Augmented Generation with Adaptive Reasoning Structures
- **Authors:** Shengyuan Chen, Chuang Zhou, Zheng Yuan (9 in total) [1]
- **Venue:** arXiv comment: "This work has been accepted to AAAI'26" [1]
- **First version:** 20250808 [1]
- **Link:** https://arxiv.org/abs/2508.06105
- **Citations:** 41, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *origin:* Proposes reasoning structure built at query time with no offline graph: it "dynamically extracts reasoning structures at inference time to guide adaptive retrieval without any pre-built graph" [1] (AAAI 2026 per the arXiv comment). The archive page kb-kg/literature/graph-rag-research.md names it as the "no pre-built graph" paper.
- **Idea:** Pre-built GraphRAG graphs carry an "overwhelming token cost and update latency" and may not match the logic a query needs. LogicRAG splits the query into subproblems, models their dependencies as a directed acyclic graph, orders them by topological sort, and prunes the graph and the context to cut tokens [1].
- **Relations:**
  - answers GraphRAG (2404.16130) and the pre-built-graph family (LightRAG 2410.05779, HippoRAG 2405.14831): 'existing GraphRAG methods rely on a costly process to transform the corpus into a graph' [1].
  - same direction, cheaper graph at index time, by LinearRAG (2510.10114): relation-free, token-free graph; the two share authors (Shengyuan Chen) per the arXiv records.
- **Read:** Abstract only (arXiv API record). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2508.06105 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2508.06105 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 41 (read 20261102 20:20 UTC)

## 28. RAGSearch (2026) — arXiv 2604.09666

- **Title:** Do We Still Need GraphRAG? Benchmarking RAG and GraphRAG for Agentic Search Systems
- **Authors:** Dongzhe Fan, Zheyi Xue, Siyuan Liu (4 in total) [1]
- **Venue:** Semantic Scholar venue field (not checked against the paper): arXiv.org [1]
- **First version:** 20260401 [1]
- **Link:** https://arxiv.org/abs/2604.09666
- **Citations:** 1, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *turning-point:* Independent test of the cost argument: "can agentic search compensate for the absence of explicit graph structure"; answer: it narrows the gap, especially with RL, but GraphRAG "remains advantageous for complex multi-hop reasoning" and is more stable [1] [3]. Appeared 20260401, too recent for a citation count to mean much.
- **Idea:** RAGSearch runs dense RAG and five GraphRAG backends (GraphRAG, RAPTOR, HippoRAG2, HyperGraphRAG, LinearRAG) under four agentic search systems (Search-o1, GraphSearch, Search-R1, Graph-R1) on six QA sets with full dev/test splits, and reports accuracy, offline cost, online efficiency and stability. Single-shot, GraphRAG gains +0.47 on general QA and +27.23 on multi-hop QA over dense RAG; GraphSearch reduces the multi-hop gap by 32.3% relative; HippoRAG2 gives the largest gains [3].
- **Relations:**
  - evaluates GraphRAG (2404.16130), RAPTOR (2401.18059), HippoRAG 2 (2502.14802), LinearRAG (2510.10114), HyperGraphRAG (2503.21322) as backends, and Search-R1 (2503.09516), Graph-R1 (2507.21892), Search-o1 (2501.05366) as agents [3].
  - answers GraphRAG-Bench (2506.05690) and RAG vs GraphRAG (2502.11371) by adding the agentic setting; its conclusions are that dense RAG with a good agentic workflow is competitive on general QA while construction costs reach 1.72 hours and USD 13.19 per 1M tokens [3].
- **Read:** Abstract and alphaXiv report (20261102 20:00). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2604.09666 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2604.09666 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 1 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2604.09666 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)

## 29. BM25 Wins at Scale (2026) — arXiv 2607.26497

- **Title:** BM25 Wins at Scale: A Scaling Study of Retrieval-Augmented Generation Paradigms
- **Authors:** Pengyu Wang, Benfeng Xu, Shaohan Wang (8 in total) [1]
- **Venue:** Semantic Scholar venue field (not checked against the paper): arXiv.org [1]
- **First version:** 20260729 [1]
- **Link:** https://arxiv.org/abs/2607.26497
- **Citations:** 2, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *turning-point:* Independent scaling test across 28 nested corpus sizes (1,144 to 511,959 documents) with one reader and one judge: "Around 10 million corpus tokens, BM25 overtakes" the File-System Agent and leads at every larger tier, by nearly 20 points at full scale; graph methods hit "construction walls" and stay below BM25 where they could be built [1]. Dated 20260729: no citation record yet.
- **Idea:** Seven pipelines from four paradigms (BM25; dense RAG; graph: HippoRAG 2, MS-GraphRAG, LightRAG, LinearRAG; a File-System Agent using list, grep, read tools) are run on EnterpriseRAG-Bench (500 questions, 511,959 documents). Agency works best after ranked discovery: the Agent+BM25 control reaches 69.4% at full scale against 50.5% for BM25 alone and 30.7% for the raw-file agent. Fitted build costs: HippoRAG 2 about 2.9 billion tokens, MS-GraphRAG 7.9 billion, LightRAG 102 billion (extrapolated) [3].
- **Relations:**
  - evaluates HippoRAG 2 (2502.14802), GraphRAG (2404.16130), LightRAG (2410.05779) and LinearRAG (2510.10114) at scale [3].
  - answers the claim of Search-R1 / agentic retrieval (2503.09516 and the RAGSearch line, 2604.09666) that agents replace structure: its Agent+BM25 control shows agents add most after global ranking, not in place of it [1].
  - answers DPR (2004.04906): dense retrieval 'remains efficient but less accurate' than BM25 at shared tiers [1].
- **Read:** Abstract and alphaXiv report (20261102 20:01). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2607.26497 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2607.26497 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 2 (read 20261102 20:20 UTC)
  3. https://www.alphaxiv.org/abs/2607.26497 : alphaXiv extraction or AI-generated report of the paper (a derived summary of the full text, so numbers from it are second-hand) (read 20261102 20:00 to 20:06 UTC)

## 30. Is GraphRAG Needed? (2026) — arXiv 2606.25656

- **Title:** Is GraphRAG Needed? From Basic RAG to Graph-/Agentic Solutions with Context Optimization
- **Authors:** Long Chen, Ryan Razkenari, Yuxuan Zhou (8 in total) [1]
- **Venue:** arXiv comment: "Accepted to ACL 2026 GEM Workshop" [1]
- **First version:** 20260624 [1]
- **Link:** https://arxiv.org/abs/2606.25656
- **Citations:** 2, Semantic Scholar Graph API (api.semanticscholar.org/graph/v1/paper/batch, arXiv id), read 20261102 20:20 UTC [2]
- **Tests passed:**
  - *turning-point:* Independent comparison of nine standardised RAG scenarios on semi-structured knowledge bases; "retrieval-generation gap where expanded retrieval does not proportionally improve generation quality", so retrieval-oriented metrics "overstate advanced retrieval benefits"; also a context-engineering method cutting tokens 19% to 53% [1] (ACL 2026 GEM Workshop per the arXiv comment). Dated 20260624.
- **Idea:** Compares regular RAG, GraphRAG, Modular RAG and Agentic RAG in nine standard scenarios that range from document retrieval to hybrid text-graph retrieval, predefined or computed knowledge graphs, agentic planning and agent-graph integration. The archive page reports Hit@1 0.6147 for text only, 0.6972 with 1-hop relations, 0.6422 for GraphRAG with a predefined KG and lower for a KG computed from the documents (carried over, not re-read) [1].
- **Relations:**
  - a companion of RAGSearch (2604.09666) and GraphRAG-Bench (2506.05690) on the same question from the production side (authors at AWS and Cisco per the arXiv record).
- **Read:** Abstract only (arXiv API record); numbers carried from the archive page kb-kg/papers-benchmarks/README.md (read 20261030 by an earlier run). Metadata read 20261102 19:45 UTC from the arXiv API.
- **Sources:**
  1. https://arxiv.org/abs/2606.25656 : title, authors, dates, comment, abstract, via the arXiv API https://export.arxiv.org/api/query?id_list=2606.25656 (read 20261102 19:45 UTC)
  2. https://api.semanticscholar.org/graph/v1/paper/batch : citation count 2 (read 20261102 20:20 UTC)

## Considered and not proposed

Each line: short name, arXiv id, citation count where one was obtained (source in the header), and why it is left out. Left-out papers are candidates for the "Further reading" list of their group.

- **Earlier retrieval-augmented language models.** Atlas (2208.03299, 1468 citations): few-shot retrieval-augmented language model, a refinement of the REALM and RAG recipe; strong on citations, so a first pick for the group's Further reading. In-Context RALM (2302.00083, 1187 citations): retrieval by prepending passages with no training; an idea now taken for granted.
- **Adaptive retrieval variants.** FLARE, Active RAG (2305.06983, 950 citations): retrieval triggered by low-confidence tokens; Self-RAG is proposed as the representative of adaptive retrieval. CRAG, Corrective RAG (2401.15884, 345 citations): a corrective step after retrieval; an incremental variant. ReAct (2210.03629, 13331 citations): reasoning with tool actions; belongs to the agents area (another researcher), mentioned here only as the frame RAGSearch's agent loop is "inspired by" (RAGSearch report).
- **RAG surveys and evaluations beyond the two proposed.** RAG for NLP survey (2407.13193, 184 citations) and the agentic RAG surveys (2501.09136, 470 citations; 2507.09477, 62 citations): narrower or later than Gao et al. and Fan et al. RAGAS (2309.15217, 1296 citations), RGB (2309.01431, 729 citations), FlashRAG (2405.13576, 262 citations), Searching for Best Practices in RAG (2407.01219, 218 citations): evaluation tooling for plain RAG, outside the question of when a graph helps.
- **Graph-based RAG methods not proposed.** GNN-RAG (2405.20139, 190 citations), StructRAG (2410.08815, 104 citations), GFM-RAG (2502.01113, 64 citations), HyperGraphRAG (2503.21322, 97 citations), MiniRAG (2501.06713, 41 citations), Youtu-GraphRAG (2508.19855, 32 citations), HybridRAG (2408.04948, 251 citations): variants on the graph-retrieval theme, each used as a backend or baseline but none reported by an independent study as the turning point. PathRAG (2502.14902, 104 citations): flow-based path pruning, an improvement on LightRAG-style indexes; revisit if later evaluations adopt it. RoG (2310.01061, 591 citations), Think-on-Graph 2.0 (2407.10805, 113 citations), Graph-constrained Reasoning (2410.13080, 92 citations), KGP (2308.11730, 384 citations), GraphReader (2406.14550, 67 citations): KG question answering with an LLM; neighbours of Think-on-Graph, which is proposed as the origin.
- **Cheaper graph construction, not proposed.** KET-RAG (2502.09304, 60 citations): multi-granular indexing for lower cost; EcphoryRAG (2510.08958, 5 citations): single author, abstract-level claims only (see kb-kg/literature/graph-rag-research.md ledger V13); G3RAG (2609.19622, 0 citations) and When Is Graph Structure Worth Its Cost (2609.18099, 0 citations): September 2026, too recent for a record, kept as watch-list items. **LazyGraphRAG** (Microsoft Research blog, 20241125): the origin of the lazy approach (index cost "identical to vector RAG and 0.1% of the costs of full GraphRAG", archive page), but a blog post with no paper; it belongs to the trend and project pages, not to this list.
- **Agentic and reinforcement-learned retrieval, not proposed.** Search-o1 (2501.05366, 497 citations): training-free agentic search, a baseline in RAGSearch. R1-Searcher (2503.05592, 324 citations), ReSearch (2503.19470, 136 citations), DeepResearcher (2504.03160, 307 citations): parallel RL-search papers; Search-R1 is proposed as the representative. GraphRAG-R1 (2507.23581, 15 citations): RL for GraphRAG with process-constrained rewards, concurrent with Graph-R1 and no independent study of it was read.
- **Reasoning over structure without vectors.** PageIndex-style vectorless retrieval: no paper found; the search returned blogs only (Microsoft Tech Community post, PyPI page, blogs), so nothing to propose. DeepRead (2602.05014, 10 citations), Retriever-Free Retrieval (2610.35868, 0 citations), RIT-RAG (2610.11370): document-structure navigation papers from 2026, abstract level, too recent. Is Grep All You Need (2605.15184, 24 citations): compares grep with vector retrieval in agent harnesses on a 116-question LongMemEval sample; its abstract says grep "generally yields higher accuracy" in experiment 1 but overall scores depend on the harness; a small study, so left for further reading next to BM25 Wins at Scale.
- **Long context versus retrieval, not proposed.** Long Context vs RAG for LLMs (2501.01880, 33 citations): re-examines the same comparison as Li et al.; LongRAG (2406.15319, 163 citations): retrieves long units to suit long-context readers; a method, not a settlement of the dispute.
- **Memory-agent evaluations.** Is Complex Agentic Memory Always Needed (2610.30755, 0 citations): the same finding as BM25 Wins at Scale in the agent-memory setting (Raw-RAG first in six of seven settings, per its abstract); belongs to the agent-memory researcher's list.
- **Surveys of KG and LLM combined.** Unifying LLMs and KGs, a roadmap (2306.08302): named as a lead in kb-kg/papers-benchmarks/README.md; outside my area (LLM and KG roadmaps) and left to the researcher covering the KB/KG side of the LLM era. No count obtained in this run.
- **GraphRAG-Bench (Xiao et al.), 2506.02404 (36 citations).** A different benchmark with the same name as the proposed Xiang et al. paper (domain-specific, college-level questions, nine GraphRAG methods per its abstract). Kept out to avoid two entries under one name; list it in the group's further reading with the name collision stated.
- **GraphRAG surveys beyond the one of record.** Han et al. (2501.00309, 307 citations) and Zhang et al. (2501.13958, 169 citations): both read at abstract level, both below Peng et al. in citations; Further reading. Han et al. share authors with RAG vs GraphRAG (2502.11371).
- **In-depth Analysis of Graph-based RAG in a Unified Framework** (2503.04338, 76 citations, VLDB per Semantic Scholar): an independent comparison among graph-based methods, not graph against plain RAG; abstract level only, so left to Further reading next to RAG vs GraphRAG.
