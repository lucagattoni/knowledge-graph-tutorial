---
slug: pageindex
repo: VectifyAI/PageIndex
tier: deep
category: core
snapshot: 20261030 19:29 UTC
---

# PageIndex

Reading times: repository metadata, the release list, the licence file, the README and the directory tree at
20261030 19:29 UTC; source files between 19:29 and 19:36 UTC; the sibling and benchmark repositories between
19:30 and 19:35 UTC; the arXiv papers at 19:33 and 19:34 UTC. Pages on pageindex.ai and docs.pageindex.ai were
read through a fetch tool that returns an extract, not the raw page; each such source is marked "extract". Each
source below carries its own time.

| | |
|---|---|
| Repository | https://github.com/VectifyAI/PageIndex |
| Licence | MIT, from the `LICENSE` file ("Copyright (c) 2025 Vectify AI"); the file has one commit, the repository's first, 20250401 10:54 UTC [3]. GitHub's API and `pyproject.toml` also say MIT [1][9]. The README names no licence, so there is no badge to disagree [4]. |
| Language | Python [1] |
| Stars, forks | 39,913 and 3,435 (20261030 19:29 UTC) [1] |
| Created, last push | 20250401 10:53 UTC, 20261029 22:48 UTC [1] |
| Latest release | v0.5.0, 20261029 22:53 UTC [2] |
| Status | active (pushed within 90 days); not archived [1]. No flag in the 20261030 19:13 UTC snapshot [16]. |
| Paper, docs | No paper in the sources read. The README asks to be cited as a blog post, "PageIndex: Next-Generation Vectorless, Reasoning-based RAG", September 2025 [4]; the blog page is dated 19 September 2025 (extract) [29]. Docs: docs.pageindex.ai [4]. |

**Flag check.** The snapshot raised no flag (no `fast-growth`, `low-forks`, `quiet` or `archived`) [16]. The numbers
behind that: 8.61 forks per 100 stars, 69.17 stars per day over 577 days, 16 contributors [16][15]. GitHub's 153
"open issues" are 53 open issues and 100 open pull requests (20261030 19:35 UTC) [15]. The README's Updates list
dates its launches (SDK, Flash, Page Search API) [4]. These are heuristics and this entry draws no conclusion
from them.

## What it is

PageIndex is a Python SDK and command-line tool from Vectify AI for question answering over long documents
without a vector database [4][9]. At index time it builds a tree of a document's sections, each node holding a
title, an id, a page range and a summary [6]. At query time an LLM agent reads that tree and fetches the page
ranges it picks [4][12]. The README's argument is that "similarity ≠ relevance": it replaces the vector index with
LLM reasoning over the tree [4].

It builds no entity graph. In the ten SDK modules I fetched (client, local and cloud APIs, local chat, agent
tools, the classic and Markdown indexers, `utils.py`, `tree_optimize.py`, `flash/api.py`) the words "embedding",
"faiss" and "vector" do not occur; the roughly 80 files of the `flash/` package were not searched [12][10][11][7][8].
The tree follows the document's own headings, not extracted entities, which is the difference from the graph
projects in this reference. For the wider timeline see [`../llm-era/README.md`](../llm-era/README.md).

The SDK has two modes with one client: **local** (this repository, MIT, text PDFs only, your own LLM key) and
**cloud** (hosted by Vectify, needs a PageIndex API key) [4].

## How it works

### Building the tree

Three builders exist, plus the hosted one.

| Builder | Where the structure comes from | What an LLM does at index time | Input |
|---|---|---|---|
| **Flash**, the local default since 20260813 [13] | Layout statistics from a character-level PDF parse: font statistics, headers and footers, table-of-contents boilerplate, columns, numbering. Embedded PDF bookmarks are used "when trustworthy" [6][2][5] | Not for the skeleton. An LLM *expands* oversized nodes and writes node summaries [6][8][9] | text PDF |
| **Standard** (`mode="standard"`), the original pipeline | The LLM reads the pages [10] | Detects table-of-contents pages, extracts the table, maps entries to physical pages; with no usable table it generates the structure from page groups of up to 20,000 tokens; checks every title against its page; fixes errors; splits big nodes; writes summaries [10] | PDF |
| **Markdown** | `#` to `######` headings and bold-only lines, found by pattern; nodes carry a line number, not pages [11] | Optional summaries for nodes of at least 200 tokens (shorter nodes keep their text) [11] | `.md` through the CLI or function only [11][7] |
| **Cloud** | "Parsing, OCR, image understanding, tree-index construction" are done by Vectify [4] | Unstated | PDF, PPTX, Word [26] |

**Flash in detail.**

- *Skeleton:* the README says the tree "is extracted from the document layout without an LLM; the index model only
  summarizes and refines it" [4]. The Flash README adds that a run with summaries and optimisation off is fully
  LLM-free [6]. The result records its `toc_source`: `detected`, `bookmarks`, `hybrid`, `pages` or `unreadable` [6].
  Every page falls in some node: a hierarchy that starts late gets a `Preface` node, and a parent whose first child
  starts later gets an "(intro)" child [6].
- *Optimisation* is driven by a search-cost rule [8]. Cost is counted in pages; visiting a node costs one page. A
  node of more than 5 pages is *expanded* (the LLM lists the subsection headings printed inside it, "never invent
  or paraphrase one") only if routing plus the largest child is cheaper than scanning the whole node. A subtree is
  *merged* away, deterministically and without an LLM, if scanning the parent costs no more than navigating the
  subtree; the removed titles stay on the parent as `key_items` [8]. Frontier siblings that cover identical pages
  are collapsed [8].
- *Summaries* are written bottom-up. A leaf reads its own pages. A parent is composed from its children's summaries
  plus the pages no child covers. Each summary is capped at 150 words by default; a leaf shorter than the cap keeps
  its raw text; up to 128 calls run at once; reasoning effort defaults to "none" [9][2][6].
- *Claude subscription:* models named `claude-code/...` index through Claude Code in Flash mode only [2][10].

**Standard in detail.** It starts from the document's table of contents if one with page numbers is found, and
otherwise generates the structure from the page text [10]. After each attempt an LLM checks, entry by entry, that
the title appears on its page. At 100% the result is kept; above 60% the wrong entries are fixed in up to three
rounds; otherwise it falls back from "table with page numbers" to "table without page numbers" to "generated from
text" [10]. A leaf whose page range is wider than 10 pages and that holds at least 20,000 tokens is split again by
the LLM [10][9]. Document text is scrubbed of phrases such as "ignore previous instructions" and wrapped in
delimiter tags before it reaches the model [10].

The stored tree has the same shape in both modes since 20261001: `title`, `node_id`, `start_index`, `end_index`,
`summary`, optional `key_items`, and `nodes` [2][6]. In local mode it is kept as JSON files in a directory [12].

### Navigating the tree

Retrieval is an agent loop, not a ranking function [4][12]. The agent has four read tools [12]:

| Tool | Purpose |
|---|---|
| `browse_documents` | list the library (newest first, with names and descriptions) |
| `get_document` | check that a document is `completed` |
| `get_document_structure` | return the tree (titles, ids, page ranges, summaries, no page text); the description says it is *required* before reading any document over 20 pages |
| `get_page_content` | return the text of a page range; "tight, targeted page ranges, never the whole document" |

Tool answers are capped near 100,000 characters and the structure is paginated by `part` [12]. The instructions
tell the agent to rephrase and page through the whole library before saying a document is missing [12]. The chat
engine is built on the OpenAI Agents SDK, a base dependency [2][9]. The benchmark harness allowed up to 20 turns per
question [19]. Citations are page-level in local mode and block-level (page, box, type) in cloud [4][2].

The September 2025 blog describes the same loop in prose: read the tree, pick a section, read it, decide if it is
enough, follow in-document references such as "Appendix G", use earlier turns. It gives no numbers and does not say
how the tree is built (extract) [29].

Library-level discovery differs by mode. Cloud adds folders, metadata filters and "semantic relevance" ranking of
documents; how that ranking works is unstated. Local mode refuses `sort="relevance"` and leaves the model to match
names and descriptions itself [12]. For corpora of millions of documents the project describes a separate "PageIndex
File System": a tree of files above the document trees, in which an LLM decides at each node whether to open a
subtree, built on demand for the query; the post names "topic models or LLM-driven grouping" and gives no
benchmark (extract, 3 May 2026) [30]. The README calls it Cloud-only [4]; the post says it ships in PageIndex
Enterprise, with the managed Cloud edition "rolling out" [30].

### Formats and limits

| | Local (open source) | Cloud (hosted) |
|---|---|---|
| Formats | PDF only. Other extensions are refused [7][26] | PDF, PPTX and Word (extract) [26] |
| Scanned or image-only PDF | Refused: "no text layer ... run OCR before indexing" [7]. The README table lists OCR and image understanding as cloud-only [4] | OCR and image understanding [4] |
| Other refusals | Encrypted PDFs; PDFs whose pages are all blank; a flat "Page N" tree of more than 10 pages [7][6] | unstated |
| Size and page limits | None found in `local_api.py`, `client.py`, `cloud_api.py` or `flash/api.py`. Benchmarked up to 1,098 pages [6]; the cost comparison goes to 805 pages [4] | Unstated in the docs pages read [24][26][28]. Metadata is capped at 8 KB per document (extract) [26] |
| Markdown | Only through `run_pageindex.py --md_path` or `md_to_tree` [11] | unstated |
| Citations | page-level [4] | block-level [4] |

Request-level caps in the tools: up to 10,000 pages in one page request and up to 10,000 documents in one
`list_documents` call [12][7].

### Open source and hosted

| Piece | Status | Source |
|---|---|---|
| SDK, CLI, Flash, Standard and Markdown builders, local chat, agent tools | This repository, MIT | [3][5] |
| Cloud API: managed indexing with OCR and image understanding, storage, folders, metadata, block citations, MCP server, managed chat | Hosted by Vectify, API key. The repository holds the client modules (`cloud_api.py`, `mcp_bridge.py`), not the server | [4][5][27] |
| Cloud pricing | $10 free credits (about 1,000 pages), $0.01 per page indexed, $0.001 per active page per month after the first 1,000, no retrieval fee; extract | [28] |
| PageIndex App | Hosted "document analysis agent" | [4] |
| Page Search API (Oct '26) | Hosted; finds the pages that answer a question. How it scores pages beyond "reads every page against the question and gives each page a relevance from 0 to 1" is unstated | [4][22] |
| File System, dedicated or VPC deployment | Enterprise or Cloud only | [4][30] |
| Other repositories by the same organisation | `pageindex-mcp` (MIT, 407 stars), `ChatIndex` (Apache-2.0, 175), `ConDB` (Apache-2.0, 69), `OpenKB` (Apache-2.0, 4,831) | [35][23] |

The MCP docs page says the server answers over documents "already indexed in your PageIndex Cloud account" and
needs an API key (extract) [27]. From the SDK, `as_claude_mcp()`, `as_openai_tools()`, `as_anthropic_tools()` and
`agent_tools()` expose the same tool contract in-process; local clients get the subset that exists locally [2].
Cloud documents can be answered with your own model: page content then passes through your process to your
provider [2].

### Relationship to OpenKB

Only what the sources state:

- OpenKB "compiles raw documents into a structured, interlinked wiki-style knowledge base using LLMs, powered by
  PageIndex's vectorless, reasoning-based retrieval for long documents" [23].
- OpenKB reads short documents in full after converting them with markitdown. PDFs of 20 pages or more (setting
  `pageindex_threshold: 20`) go to PageIndex, and the LLM reads the tree [23].
- PageIndex runs locally by default; setting `PAGEINDEX_API_KEY` switches on the cloud for OCR, faster structure
  generation and larger indexing jobs [23].
- OpenKB's `pyproject.toml` pins `pageindex==0.3.0.dev3` [23]. That is a `.dev3` build, published as a GitHub
  release on 20260710 [2], before Flash was added on 20260730 [13]. OpenKB was last pushed 20260722 [23].
- OpenKB's README lists PageIndex in "The Stack" and calls the set of Vectify repositories "the PageIndex
  ecosystem" [23]. The docs' open-source page lists OpenKB the same way (extract) [25]. PageIndex's own README does
  not mention OpenKB [4].
- Who maintains OpenKB beyond "same GitHub organisation": unstated.

## Cost and operating profile

| Item | What the sources say |
|---|---|
| Index, Flash, local | The README: "about $0.001 per page" with `gpt-5.6-luna`, "a little over a dollar" for a 1,000-page book; 9 to 1,098 pages took roughly 13 seconds to 4.5 minutes [4]. Flash's own table, full optimisation: 9 pages, 8,715 input and 4,673 output tokens; 222 pages, 280,975 and 136,982; 1,098 pages, 1,587,265 and 646,958 [6]. All are the project's measurements |
| Index, Standard | Cost unstated. LLM calls grow with the number of table-of-contents entries (each is verified) and with large nodes split again [10] |
| Index, cloud | $0.01 per page (extract) [28] |
| Query | An agent loop of several tool calls; cost depends on the chat model. README: `chat=` "use the best model you can afford" [4]. Measured figures are in Evidence |
| Versus whole-document input | README: native PDF input costs 2.1x more at 52 pages and 16.6x at 420; at 805 pages the document no longer fits the context window [4] |
| Needs | Python 3.10 or later; an LLM key (OpenAI by default, LiteLLM providers, keyless OpenAI-compatible servers, or a Claude subscription through `claude-code/` models); no vector database and no server in local mode [2][9]. Default models when none is set: `gpt-6-luna` to index, `gpt-6-sol` to chat [2] |
| Entirely local | The SDK is local; the model need not be. The sources show local-model use only in a third-party harness with Ollama [34] (see Evidence) |
| Pins | `litellm` is held at 1.105.1 or newer and below 1.106; a comment in `pyproject.toml` says 1.107.0 "was malware". I did not verify that [9] |

**Model names.** The sources name the default index model `gpt-6-luna` (quickstart), `gpt-5.6-luna` (README
benchmarks, OSS benchmark), "GPT-6 Luna" (Financial QA) and "GPT-6.0 luna" (cookbook) [4][19][20][21]. None says
whether these are one model. This matters for the per-page price above.

## Evidence

All figures in the first table are Vectify's own, run by Vectify, on Vectify's repositories.

### The project's own results

| Claim | Dataset | Metric | Baseline | Who ran it | Note |
|---|---|---|---|---|---|
| "98.7% accuracy on FinanceBench" (README) [4] | FinanceBench public set; the result files hold 150 questions [17] | Accuracy. Answers judged by an LLM (`gpt-4o-2024-11-20`; a hybrid mode adds `o1-mini` and `o3-mini` and accepts a pass from any); ambiguous cases labelled by "expert human annotations" [17] | The README chart shows "Vector RAG 50%"; the configuration is unstated in the chart, the README and the evaluation repository [4][17] | Vectify | See below |
| 34 configurations of 19 LLMs on 100 questions over 40 10-K filings (README) [4]. The benchmark repository now says 37 configurations of 21 LLMs [19] | 100 questions, 7,318 pages, 8 companies; questions written by Claude Opus agents and checked by two further agents [19] | Share of answers covering every key point without contradiction; graders are Claude Opus 5.5, blind, a second grader on a seeded fifth, a third for disputes [19] | None: only the model behind PageIndex changes [19] | Vectify, 20261022 to 20261027 [19] | Top: Claude Opus 5.5 (max) 98.7% at $128.49 per 100 questions; Gemini 4 Argon (high) 98.0% at $29.27; lowest 65.7%; cheapest Pareto point 83.7% at $1.47 [19] |
| PageIndex 100.0% against vector search 54.0% to 87.3% (cookbook) [20] | 63 questions on five NVIDIA 10-Ks (fiscal 2022 to 2026) | Answer correct if it states every key point and contradicts nothing; judge Claude Opus 5.5, blind, agreed with the authors' blind grading on 314 of 315 answers [20] | Gemini Embedding 2, 512-token chunks, top-k 10, 30, 50, 100: 54.0, 74.6, 79.4, 87.3%. Same generator (GPT-6.0 sol, medium) [20] | Vectify, 20261016, `pageindex` 0.4.1 [20] | Query cost per 1,000 queries: PageIndex $110; vector $16, $42, $68, $135. Six-embedding variant: best vector run, Voyage 4 at top-k 100, 92.1% for $134 [20] |
| 85.5% to 100% on 62 questions (OSS benchmark) [21] | 62 plain-text questions over 34 PDFs (1,945 pages) from MMLongBench-Doc-V2; documents Flash refuses were excluded [21] | The MMLongBench-Doc-V2 judge [21] | None | Vectify, repository created 20260816 [21] | `gpt-5.6-luna` 85.5% to 96.8%, `gpt-5.6-terra` 90.3% to 100%, `gpt-5.6-sol` 96.8% to 100%, by reasoning effort; $0.0031 to $0.0819 per question [21] |
| Page Search API finds evidence pages (hosted product) [22] | 80 single-filing questions of the Financial QA set, 39 filings [22] | Evidence pages found in the top k [22] | Voyage 4 Large, Gemini Embedding 2, OpenAI text-embedding-3-large [22] | Vectify, created 20261026 [22] | Top 5: 93.2% against 65.5, 54.0, 47.5%; top 10: 97.5% against 83.8, 70.1, 68.0%. This is not the open-source SDK [22] |

**On the 98.7% figure.**

- The system measured is **Mafin 2.5**, which the evaluation repository calls "our latest RAG model on Financial
  reports, built on PageIndex", run on GPT-4o and on DeepSeek V3 [17]. The repository was created 20250219 and last
  pushed 20251020 [17]. It is not a measurement of the SDK at v0.5.0.
- The result files label each of the 150 answers: 136 `AL` (aligned), 6 `BE` (benchmark error), 5 `MVA` (multiple
  valid approaches), 2 `NAL` (not aligned), 1 `SEDC` (same evidence, different conclusion) [17]. The README does not
  give the formula. 148 of 150 is 98.7%, so the figure matches counting `BE`, `MVA` and `SEDC` as correct; counting
  only `AL` gives 136 of 150, 90.7% (my arithmetic).
- The repository's comparison table lists other vendors' numbers with source links: Quantly 94, Fintool 98 on 66.7%
  of the benchmark, ChatGPT 4o with search 31, Perplexity 45 [17]. I did not check those pages.
- The same number, 98.7%, tops the 2026 Financial QA benchmark. That is a different dataset and grader.

**Other limits of the project's own evidence.** The Financial QA and cookbook runs use Claude Opus models to write
questions or to grade, and both stay within one document type, annual reports (10-K) [19][20]. The cookbook's own
text calls five reports from one company "a hard case for retrieval" [20]. Vector costs there are priced without
prompt caching; PageIndex's include cache hits [20]. On those numbers the release headline "cheaper than vector RAG:
for both index and query" [2] holds against vector top-k 100 ($135) but not against top-k 10 to 50 ($16 to $68),
which score lower [20] (my reading).

### Independent evaluations

Three papers and one harness were read. None is a scored test of the released SDK.

| Source | What it ran | Result for tree-based retrieval | Caveat |
|---|---|---|---|
| Lumer et al., arXiv 2511.18177, 22 Nov 2025 [31] | Vector-based agentic RAG against "hierarchical node-based systems", 150 questions over 1,200 SEC filings, LLM-as-judge pairwise | Vector system won 68% of comparisons; latency 5.2 s against 5.98 s; node-based preprocessing $30.62 per 10-K [31] | The node system is the authors' own, modelled on PageIndex (the repository and the Mafin post are cited at its description). The text read does not say PageIndex code was run [31] |
| RIT-RAG, arXiv 2610.11370, 8 Oct 2026, v2 16 Oct [32] | "Corpus-level PageIndex" written by the authors as a baseline, with Claude Haiku 4.5, GPT-5-mini, GPT-5.6-Luna; Gemini 2.5 Flash as judge | FinanceBench (150 questions): PageIndex 72.0, 75.3, 66.7%; vanilla RAG at k=5: 41.3, 49.3, 48.0%; agentic search 74.0, 76.0, 75.3%; the authors' method 84.0, 84.0, 85.3%. Per query on FinanceBench with Haiku: 16.6 cents, 14 s; preprocessing $773.1 [32] | A retriever first picks one document and the agent then reads that document's table of contents, so a wrong pick makes the evidence unreachable. The authors propose a competing method [32] |
| Hashmi, arXiv 2604.14222, v2 28 Oct 2026 [33] | Own "Tree Reasoning" against vector RAG on four short documents, 22 queries, GPT-4o-mini as generator and judge | Tree Reasoning scored 0.900 against 0.845; the paper calls the results preliminary [33] | Not PageIndex. The paper's own limitations list says the tree system was given the target document and the vector system was not [33] |
| `pageindex-rag-bench`, a personal repository, created 20261011 [34] | Harness: PageIndex local against a pgvector baseline, same chat model and judge, 90 or 284 questions over 34 PDFs | None: "Not yet run"; no scored run committed [34] | It reports one demo, three attempts at one question with small Ollama models: PageIndex found the right page twice and never produced a formatted answer; the baseline answered each time. Three attempts is not a rate (the author's words) [34] |

The search also listed arXiv 2608.14841, 2607.23006, 2607.05764, 2609.08364 and 2608.07994 as possibly using
PageIndex as a baseline; I did not open them [36]. [`../papers-benchmarks/README.md`](../papers-benchmarks/README.md)
names neither FinanceBench nor PageIndex (checked 20261030 19:37 UTC) [37].

## Direction

No roadmap file is in the repository [5]. Direction, from the README's Updates list and the release notes:

- The SDK is the centre: local and cloud modes behind one client since August 2026; the v0.5.0 notes name "one
  client" for index, chat and agent integration [4][2].
- Flash became the local default and keeps getting fixes for scripts, filings and slide decks [4][13][2].
- Hosted products are added at the top of the README: Page Search API (Oct '26), PageIndex App, File System for
  large corpora [4].
- Agent use: the cloud MCP tool contract is mirrored in-process and kept in step with the cloud server [2][12].

## Recent changes

216 commits (182 without merges) landed between 20260731 19:00 and 20261029 UTC: 61 in August, 77 in September,
78 in October [13]. Release tags: 29 GitHub releases between 20260708 and 20261029, 5 of them marked pre-release [2].
Version numbers do not rise in date order: `v0.3.0.dev3` (20260710) comes before `v0.2.10` (20260819) [2]; the
reason is unstated. `pyproject.toml` on `main` still reads version 0.2.10, while PyPI's latest is 0.5.0 [9][14].

| Date (UTC) | Change |
|---|---|
| 20260730 to 20260802 | Flash added; two commits titled "Sync PageIndex Flash from private branch"; tree optimisation replaces thinning [13] |
| 20260811 to 20260813 | Local mode for the SDK (v0.2.9); agent tools and local chat (v0.2.10); Flash with full optimisation becomes the default local mode [13] |
| 20260910 | MCP prompts over the bridge, `chat(citations=True)` [13] |
| 20261001 | One tree shape for local and cloud; a breaking change to node fields [13][2] |
| 20261012 to 20261018 | Cheaper Flash indexing (v0.4.0); `claude-code/` models for subscription use (v0.4.2) [2] |
| 20261020 to 20261027 | Token usage reported for local runs; metadata schemas for cloud folders; README puts Page Search API first [13][2] |
| 20261029 | v0.5.0: reasoning kept across tool calls, retry rules follow the official SDKs, `extra_body` reaches every provider (breaking) [2] |

## Sources

1. https://api.github.com/repos/VectifyAI/PageIndex : stars, forks, licence field, dates, topics, archived (read 20261030 19:29 UTC)
2. https://github.com/VectifyAI/PageIndex/releases : `releases/latest` (v0.5.0 notes, 0.2.17 to 0.5.0 sections) and the list of 29 releases (read 20261030 19:29 UTC)
3. https://github.com/VectifyAI/PageIndex/blob/main/LICENSE : full MIT text and copyright line (read 20261030 19:29 UTC); the file's commit history, one commit (read 20261030 19:35 UTC)
4. https://github.com/VectifyAI/PageIndex/blob/main/README.md : claims, quickstart, benchmarks, local against cloud table, Updates (read 20261030 19:29 UTC)
5. https://github.com/VectifyAI/PageIndex/tree/main : recursive tree listing, 214 entries; no roadmap file (read 20261030 19:29 UTC)
6. https://github.com/VectifyAI/PageIndex/blob/main/pageindex/flash/README.md : Flash output, `toc_source`, benchmark table (read 20261030 19:29 UTC)
7. https://github.com/VectifyAI/PageIndex/blob/main/pageindex/flash/api.py and https://github.com/VectifyAI/PageIndex/blob/main/pageindex/local_api.py : PDF-only rule, refusals, flat-tree limit, `list_documents` limit (read 20261030 19:29 UTC)
8. https://github.com/VectifyAI/PageIndex/blob/main/pageindex/tree_optimize.py : merge and expand rules, prompt, constants (read 20261030 19:29 UTC)
9. https://github.com/VectifyAI/PageIndex/blob/main/pageindex/utils.py, https://github.com/VectifyAI/PageIndex/blob/main/pageindex/config.yaml and https://github.com/VectifyAI/PageIndex/blob/main/pyproject.toml : summary defaults, node limits, dependencies, version field (read 20261030 19:29 to 19:30 UTC)
10. https://github.com/VectifyAI/PageIndex/blob/main/pageindex/page_index_classic.py : Standard mode pipeline, fallbacks, verification, injection hardening (read 20261030 19:29 UTC)
11. https://github.com/VectifyAI/PageIndex/blob/main/pageindex/page_index_md.py and https://github.com/VectifyAI/PageIndex/blob/main/run_pageindex.py : Markdown builder, CLI modes and defaults (read 20261030 19:29 UTC)
12. https://github.com/VectifyAI/PageIndex/tree/main/pageindex : `agent_tools.py` (tool contract, instructions, limits), `local_chat.py`, `local_store.py`, `client.py`, `cloud_api.py` (read 20261030 19:29 to 19:36 UTC)
13. https://github.com/VectifyAI/PageIndex/commits/main : commit subjects since 20260731 19:00 UTC, 216 commits (read 20261030 19:31 UTC); commits before that date (read 20261030 19:35 UTC)
14. https://pypi.org/pypi/pageindex/json : latest version 0.5.0, licence MIT, release history (read 20261030 19:29 UTC)
15. GitHub search and contributors APIs for `VectifyAI/PageIndex` : 53 open issues, 100 open pull requests, 16 contributors (read 20261030 19:33 to 19:35 UTC)
16. [`../landscape/20261030_1913-github/repos.tsv`](../landscape/20261030_1913-github/repos.tsv) : snapshot row, flags column empty (snapshot 20261030 19:13 UTC; read 19:28 UTC)
17. https://github.com/VectifyAI/Mafin2.5-FinanceBench : README, `eval.py`, `human_evaluations/README.md`, `result_gpt4o.json`, `result_deepseekv3.json`, metadata (read 20261030 19:30 UTC)
18. https://pageindex.ai/blog/Mafin2.5 : extract; consistent with [17], gives no question count, judging method or baseline figures (read 20261030 19:32 UTC)
19. https://github.com/VectifyAI/pageindex-benchmarks : README, `financial-qa/README.md`, `financial-qa/METHOD.md` (read 20261030 19:31 UTC)
20. https://github.com/VectifyAI/PageIndex/tree/main/cookbook/pageindex-vs-vector-10k : both notebooks, markdown cells and saved output (read 20261030 19:32 UTC)
21. https://github.com/VectifyAI/PageIndex-OSS-Benchmark : README and results table (read 20261030 19:32 UTC)
22. https://github.com/VectifyAI/page-search-benchmark : README (read 20261030 19:32 UTC)
23. https://github.com/VectifyAI/OpenKB : README, metadata, `pyproject.toml`, licence file head (read 20261030 19:31 UTC)
24. https://docs.pageindex.ai/getting-started : extract; local against cloud (read 20261030 19:31 UTC)
25. https://docs.pageindex.ai/open-source : extract; list of the organisation's open-source repositories (read 20261030 19:31 UTC)
26. https://docs.pageindex.ai/sdk/documents : extract; formats, 8 KB metadata cap, statuses (read 20261030 19:32 UTC)
27. https://docs.pageindex.ai/mcp : extract; MCP needs cloud API key (read 20261030 19:35 UTC)
28. https://pageindex.ai/developer : extract; plans and prices; limits not stated (read 20261030 19:35 UTC)
29. https://pageindex.ai/blog/pageindex-intro : extract; retrieval loop in prose, 19 September 2025 (read 20261030 19:31 UTC)
30. https://pageindex.ai/blog/pageindex-filesystem : extract; File System, 3 May 2026 (read 20261030 19:33 UTC)
31. https://arxiv.org/abs/2511.18177 and https://arxiv.org/html/2511.18177 : Lumer et al., abstract, sections 3.1.3 and 3.2.2, discussion (read 20261030 19:34 UTC)
32. https://arxiv.org/abs/2610.11370 and https://arxiv.org/html/2610.11370 : RIT-RAG, Tables 1, 3, 8 and 9, appendix B.2 (read 20261030 19:33 to 19:34 UTC)
33. https://arxiv.org/abs/2604.14222 and https://arxiv.org/html/2604.14222 : Hashmi, sections 3.1 to 3.5, 4.1 and 5.5 (read 20261030 19:33 to 19:34 UTC)
34. https://github.com/SyedTashfin/pageindex-rag-bench : README and `docs/FINDINGS.md` (read 20261030 19:32 UTC)
35. https://github.com/VectifyAI/pageindex-mcp, https://github.com/VectifyAI/ChatIndex and https://github.com/VectifyAI/ConDB : repository metadata; `pageindex-mcp` README head (read 20261030 19:33 to 19:35 UTC)
36. Web searches "PageIndex vectorless RAG independent evaluation benchmark vs vector RAG" (19:32) and an arXiv-restricted search for PageIndex as a baseline (19:33): used only to find [31] to [34] and the unopened papers named above; no fact rests on the search summaries
37. [`../papers-benchmarks/README.md`](../papers-benchmarks/README.md) and [`../llm-era/README.md`](../llm-era/README.md) : searched for PageIndex and FinanceBench; none found (read 20261030 19:37 UTC)
