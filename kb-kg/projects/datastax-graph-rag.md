---
slug: datastax-graph-rag
repo: datastax/graph-rag
tier: deep
category: core
snapshot: 20261030 18:58 UTC
---

# datastax/graph-rag (graph-retriever)

| | |
|---|---|
| Repository | https://github.com/datastax/graph-rag [1] |
| Licence | Apache-2.0, from the `LICENSE` file at the repository root; the GitHub licence field agrees [1][3] |
| Language | Python (3.10 or newer declared) [1][6] |
| Stars, forks | 91, 29 (20261030 18:58 UTC) [1] |
| Created, last push | 20250108 10:01 UTC, 20250505 19:04 UTC [1] |
| Latest release | v0.8.0, published 20250404 12:52 UTC [4] |
| Status | quiet: not archived, no push for 543 days at the snapshot (see "Changed since the July 2026 investigation") [1][5] |
| Paper, docs | No paper. Docs site: https://datastax.github.io/graph-rag/ [1][12] |

## What it is

A small Python library, published as two packages: `graph-retriever` (the core, usable in any Python
application) and `langchain-graph-retriever` (LangChain bindings) [2]. It adds graph traversal to an
**existing** vector store by using only document metadata: no re-ingestion, no LLM-based extraction
and no separate graph database [2][8]. Retrieval is a vector search for seed documents followed by
iterative edge expansion, where "follow an edge" is compiled into a metadata-filtered similarity
search against the same store [6][8]. At the snapshot the core package has 24 Python files and 3,132
lines including docstrings, and the LangChain package 19 files and 2,559 lines [5][6].

## How it works

### The metadata edge model

Defined in `edges/metadata.py` and `edges/_base.py` [6].

- **Declaration.** An edge is an `EdgeSpec`, a `(source_field, target_field)` pair. The source is read
  from the *outgoing* document's metadata; the target names the field matched on the *incoming*
  document. The exact string `"$id"` stands for the document ID (an older `Id` placeholder class is
  marked deprecated in favour of it) [6]. Examples from the guide [8]:

  | Spec | Meaning |
  |---|---|
  | `("cites", "$id")` | follow citations out, by ID |
  | `("$id", "cites")` | find the documents that cite this one (the reverse direction is the flipped pair) |
  | `("keywords", "keywords")` | shared-value, undirected |
  | `("authors", "primary_author")` | shared-value, asymmetric |
  | `("cites", "cites")` | documents with citations in common |

- **Runtime form.** Each document yields `Edges(incoming, outgoing)`. An outgoing edge is expressed as
  the *incoming* edge it matches: `MetadataEdge(incoming_field, value)`, which matches nodes where
  `metadata[field] == value`, or `metadata[field] CONTAINS value` if the metadata is a collection; or
  `IdEdge(id)`, which matches `node.id == id` [6]. Traversal is therefore a value-equality join
  computed on demand; the files read contain no stored edge table [6].
- **Metadata shapes.** Scalars (`str`, `bool`, `int`, `float`, `complex`, `bytes`) or iterables of
  scalars. Any other value raises a warning and is skipped. Nested keys are read with dot paths [6].
- **Escape hatch.** `edges` may instead be any `EdgeFunction: Content -> Edges`, for metadata that is
  not in joinable shape. Edges are an argument of `traverse()`, not part of the index, so they can
  differ from one query to the next [6][8].
- **README syntax.** The README quick-start writes `edges = [("mentions", "id"), "entities"]` [2]. In
  `metadata.py` only `"$id"` selects the document ID, and each list item is unpacked as a pair, so the
  README example does not match the source or the guide (read, not executed) [6][8].

### The traversal loop

Core loop: `traversal.py`, `_Traversal.traverse` [6].

1. Seed: `store.search_with_embedding(query, k=start_k)`, plus optional `initial_root_ids` fetched with
   `get()`. Seeds are at depth 0.
2. `strategy.iteration(nodes, tracker)`: the strategy decides what to keep and what to expand.
3. Stop when `select_k` is reached or nothing is queued for expansion (`NodeTracker._should_stop_traversal`).
4. `select_next_edges()` collects the outgoing edges of the queued nodes **minus edges already visited**
   (`_visited_edges`), so one shared value, such as a popular keyword, is expanded once for the whole
   traversal. It also records the minimum depth per edge (`_edge_depths`); a new node's depth is the
   minimum over its matched incoming edges.
5. `_fetch_adjacent()` calls `Adapter.adjacent()`. In the base adapter, each `MetadataEdge` becomes a
   filtered similarity search with `k=adjacent_k`, and the `IdEdge`s are fetched with one `get(ids)`.
   The merged results are de-duplicated and cut to the top `adjacent_k` by cosine similarity to the
   query (`utils/top_k.py`) [6]. The strategy docstring describes `adjacent_k` as "documents to fetch
   for each outgoing edge"; in the base adapter the final cut is applied to the merged result of one
   iteration, not per edge. The Astra adapter overrides `adjacent` and also ends with `top_k` [6].

`NodeTracker` (`strategies/base.py`) is the whole strategy API: `select(nodes)` adds to the results,
`traverse(nodes)` queues for expansion (enforcing the visited set and `max_depth`),
`select_and_traverse(nodes)` does both, and `num_remaining` is the `select_k` budget left. Selection
and expansion are separate, so a strategy may expand without keeping, or keep without expanding [6].

Knobs on `Strategy` [6]:

| Knob | Default | Meaning |
|---|---|---|
| `select_k` | 5 | total results (`k` is a deprecated alias) |
| `start_k` | 4 | seeds from vector search |
| `adjacent_k` | 10 | neighbours fetched per expansion step |
| `max_depth` | `None` | depth bound |
| `max_traverse` | `None` | declared and documented, but a search of the files read finds it only in the `Strategy` definition and docstring: the traversal loop never reads it |

### The strategies

| Strategy | Behaviour |
|---|---|
| `Eager` (`strategies/eager.py`) | `tracker.select_and_traverse(nodes)`: selects and expands everything, so plain breadth-first until `select_k` or exhaustion [6] |
| `Mmr` (`strategies/mmr.py`) | Best-first, not breadth-first. Keeps a candidate pool with embeddings; score is `lambda_mult * sim(query)` minus `(1 - lambda_mult) * max sim(already selected)`, with `lambda_mult` defaulting to 0.5. Each iteration pops the single best candidate, selects it and expands only its edges, so the frontier itself is MMR-guided. `min_mmr_score` ends the traversal early. All local numeric work, no model call [6] |
| `Scored` (`strategies/scored.py`) | A user callable `scorer(Node) -> float`; a max-heap; pops up to `per_iteration_limit` nodes per round; `finalize_nodes` re-sorts by score [6] |

Seeds come from vector search only; the files read contain no keyword (BM25) or hybrid search [6].

### The LazyGraphRAG example

`docs/examples/lazy-graph-rag.ipynb` [9]. The index step uses no LLM. 2wikimultihop articles get
`metadata["mentions"]` (link structure from the dataset) and `metadata["entities"]` from a local spaCy
NER transformer (`SpacyNERTransformer`, with the `en_core_web_sm` model). The notebook's introduction
says keyword extraction uses a local KeyBERT model and a code comment says GLiNER; the code itself
uses spaCy [9]. The chain, per query:

1. Traversing retrieval: `GraphRetriever(edges=[("mentions","$id"), ("entities","entities")], k=100,
   start_k=30, adjacent_k=20, max_depth=3)`, which returns about 100 documents.
2. Build an in-memory networkx `DiGraph` over just the retrieved documents with the same edge function
   (`document_graph.py:create_graph`: index documents by incoming edge, then materialise the outgoing
   matches) [7].
3. Communities by iterated Girvan-Newman, keeping the partition until modularity stops improving
   (`_best_communities`, `group_by_community`) [7].
4. One gpt-4o structured-output call per community, extracting query-relevant claims (`claim`,
   `source_id`).
5. One gpt-4o call per claim for relevance in the style of RankRAG: the prompt forces a `True` or
   `False` next token, and the rank is the probability of `True` read from the logprobs
   (`compute_rank`).
6. Keep the top-ranked claims up to a token budget (`max_tokens=1000`), then one final answer call over
   the claim list [9].

"Lazy" here means that all graph analysis (communities, claim extraction) happens after retrieval, on a
subgraph of about 100 nodes, with the question already known [9].

### Integration surface

- **Python API.** `traverse()` and `atraverse()` in `graph-retriever`; `GraphRetriever`, a LangChain
  `BaseRetriever`, in `langchain-graph-retriever` [6][8].
- **Store adapters** in the LangChain package: Astra DB, Cassandra, Chroma, OpenSearch and the
  LangChain in-memory store, plus a generic LangChain adapter and an `inference` module that picks the
  adapter from the store's class [5][7].
- **Document transformers** that populate metadata: spaCy, GLiNER and KeyBERT entity or keyword
  extraction, HTML hyperlinks, a parent-path field, and a shredding transformer [5][8].
- **Migration path** from LangChain's `GraphVectorStore` (which stored `Link` objects in
  `metadata["links"]`) to plain metadata fields plus the retriever [8].
- **Agents.** The notebook's conclusion says an agent could choose between vector-only search and
  different traversals per question and promises a future post [9]. A branch named `mcp` has a latest
  commit "initial add of mcp server project" (20250402 15:21 UTC); `main` lists no MCP file [5].
  An MCP server is not part of the released packages (unstated whether the branch works).

## Cost and operating profile

| Phase | Spend | Source |
|---|---|---|
| Index | Embeddings only (in the notebook, an OpenAI embedding model into Astra DB) plus a local NER or keyword model. No LLM call. | [9] |
| Traversal | No LLM in `graph-retriever`: the traversal code calls only the store adapter and cosine similarity. Per query, one seed search plus, in the base adapter, one filtered search per new `MetadataEdge` and one `get` per batch of `IdEdge`s. Adapters may batch differently. | [6] |
| LazyGraphRAG chain | Per query: 1 query embedding, one extraction call per community (each carrying the community text), one ranking call per claim, one answer call. The count of communities and claims is unmeasured; the call count is derived from the notebook code, not from a run. | [9] |

- **Needs.** An existing vector store with a supported adapter, and documents whose metadata already
  holds joinable values; for the example chain, an OpenAI key and an Astra DB endpoint and token [9].
- **Local operation.** Traversal itself needs no external service beyond the vector store. Whether the
  example chain runs fully locally is unstated; it is written against OpenAI and Astra DB [9].
- **The authors' cost comparison.** For the Wikipedia dataset in the notebook (the code comment gives
  about 6 million documents for the full set) the authors "estimated it would have taken $70k" to build
  a knowledge graph with LangChain's `LLMGraphTransformer` example, "while the document graph was
  basically free" [9]. The notebook gives no method, model or token count for the estimate: unstated.

## Evidence

| Item | What it shows | Source |
|---|---|---|
| Notebook comparison | One question ("Why are Bermudan sloop ships widely prized compared to other ships?"). The graph chain returns an answer with two reasons and source IDs; the plain vector retriever answers that the documents do not state the reasons. A single stored output; which dataset size was loaded is unstated. | [9] |
| Test suite | A CI comment on a pull request at commit `260c556f` (20250219) reports 449 tests, 443 passed, 6 skipped, 0 failed, and 93.024% line coverage. | [10] |
| Retrieval-quality benchmark | None found in the README, the guide pages `edges`, `strategies`, `traversal` and `migration`, or the LazyGraphRAG notebook. The other two example notebooks and the DataStax announcement post were not read (the post returned HTTP 500). | [2][8][9] |
| Third-party evaluation | None found in this run (one web search, 20261030). | [13] |

## Direction

The README roadmap lists two items: support more vector stores, and support LazyGraphRAG "on the
retrieved documents" [2]. Open issues and branches point the same way [10]:

- #126 (20250206): move the community and networkx functionality into `graph_retriever` (today it is in
  the LangChain package [7]).
- #123 (20250206): weights or priorities on edges and when fetching adjacent nodes.
- #107 (20250204): a `min_score` option.
- #124 (20250206): a combined adjacent query for OpenSearch.
- Open items #181 (20251112, "Support milvus") and #183 (20251201, "Metadata Extraction with OpenAI models or models from OpenAI compatible API endpoints"); whether each is an issue or a pull request was not checked.
- Unmerged branches: `multi-field-edges` (last commit 20250219; its pull request #146 was closed
  unmerged on 20260630 08:37 UTC), `mcp` (20250402), `data-modeling` (20250225), `pacp` (20250123).

No commit has landed on `main` since 20250505 [5], so none of these has shipped.

## Changed since the July 2026 investigation

The July note was written on 20260726 08:52 UTC. Everything below was read on 20261030 between 18:58 and
19:06 UTC.

- **Activity.** Zero commits since 20260801 (the GitHub API returned an empty list), and zero since 20250506 [5]. The last commit
  on `main` is the merge of pull request #177 on 20250505 19:03 UTC, and the last push to any branch is
  the documentation deployment that followed (`gh-pages`, 20250505 19:04 UTC) [1][5]. The last release
  is still v0.8.0 (20250404); PyPI shows 0.8.0 as latest for both packages [4][11].
- **Numbers.** 91 stars (July: about 89) and 29 forks (July: unstated), 11 open issues and pull requests
  counted together, subscribers 3 [1]. The repository metadata `updated_at` reads 20260813 09:37 UTC; the
  cause is unstated and no commit corresponds to it [1][5].
- **Archived, deprecated, renamed, superseded.** None found. The archived flag is false; the README, the
  docs-site landing page, the PyPI page and the LangChain integration page carry no deprecation,
  archival or successor notice [1][2][11][12][13]. A search found no renamed or successor repository.
  DataStax's own Astra DB tutorials for Graph RAG in TypeScript, C# and Java implement their own
  `GraphRetriever` class and do not mention this library; their footer reads "Copyright IBM
  Corporation 2026" [14]. No company statement about winding the project down was found.
- **Maintainer signals.** The README still says "Graph RAG is under active development" [2]; that is
  stale given the push dates. On 20251113 a top contributor (second by commit count, and author
  of the v0.8.0 release) wrote on an open pull request: "i no longer have write access to this repo" [10].
  That pull request (#180, a fix for an import error with newer Chroma versions, open since 20251021)
  collected repeated requests to merge through 20260122 and is unmerged; pull requests #179 and #182 on
  the same Chroma import problem are also open [10]. Five accounts appear in the contributor list; the
  top two have 115 and 56 contributions [10]. The latest dated human activity found is pull
  request #146 being closed by its author on 20260630 08:37 UTC without a merge [10]. Comment threads
  were not all scanned, so later comments elsewhere are possible; no commit, release or tag exists after 2025.
- **Company context, corrected.** The July note said the silence began "right after IBM's acquisition of
  DataStax (announced 20250225)". IBM's agreement was reported on 25 February 2025 and the close was
  announced on 28 May 2025 [15][16]. The last push (20250505) is therefore about ten weeks after the
  announcement and about three weeks before the close, not after the acquisition. Whether the
  acquisition caused the silence is unstated in any source read.
- **README and architecture.** Unchanged: there is no commit after July, so the code analysed in July is
  the code at the snapshot. The README roadmap still lists LazyGraphRAG as future work, while the repository
  already ships the example notebook and `create_graph` / `group_by_community` [2][7][9].
- **July claims checked against the code, and corrected in the body where wrong.**
  - Size. July wrote that the core package is about 10 files and 2k lines. That is wrong: it is 24
    Python files and 3,132 lines (2,575 non-blank, non-comment lines, docstrings included) in
    `graph-retriever`, plus 19 files and 2,559 lines in the LangChain package [5][6].
  - Entity extraction by a local spaCy NER transformer: confirmed in the code. The notebook's own prose
    names KeyBERT and a comment names GLiNER; the body now records the inconsistency [9].
  - `max_traverse` never read by the loop: confirmed [6].
  - Per-edge cap: the docs say `adjacent_k` applies to each outgoing edge, while the base adapter cuts
    the merged result of one iteration to `adjacent_k`. The body now states both [6].
  - The README quick-start edge syntax does not match the source. Added to the body [2][6].
  - The $70k figure is an estimate by the notebook's authors with no stated method. The body now says so [9].

## Sources

Every read below was made on 20261030 between 18:58 UTC (the first call, which took the repository
metadata of item 1) and 19:06 UTC (the last). The clock was not read between those two calls, so each
item after the first carries the range instead of a guessed minute.

1. https://github.com/datastax/graph-rag, repository metadata through `gh api repos/datastax/graph-rag`: stars, forks, licence field, archived flag, created and pushed dates, topics, issue count (read 20261030 18:58 UTC)
2. https://github.com/datastax/graph-rag/blob/main/README.md: description, quick-start, roadmap, licence statement referring to a `LICENSE.txt` file that does not exist (the file is `LICENSE`) (read 20261030, 18:58 to 19:06 UTC)
3. https://github.com/datastax/graph-rag/blob/main/LICENSE: full Apache License 2.0 text, appendix unfilled (read 20261030, 18:58 to 19:06 UTC)
4. https://github.com/datastax/graph-rag/releases: v0.8.0 (published 20250404 12:52 UTC), v0.7.0, v0.6.3, v0.6.2, v0.6.1; no later release or tag (read 20261030, 18:58 to 19:06 UTC)
5. https://github.com/datastax/graph-rag/commits/main: 189 commits on `main`, last 20250505 19:03 UTC; the query `since=2026-08-01` returned none; repository tree listing with 183 files (read 20261030, 18:58 to 19:06 UTC)
6. https://github.com/datastax/graph-rag/tree/main/packages/graph-retriever/src/graph_retriever: `edges/metadata.py`, `edges/_base.py`, `traversal.py`, `strategies/{base,eager,mmr,scored}.py`, `adapters/base.py`, `utils/top_k.py`, and `packages/graph-retriever/pyproject.toml` (read 20261030, 18:58 to 19:06 UTC)
7. https://github.com/datastax/graph-rag/blob/main/packages/langchain-graph-retriever/src/langchain_graph_retriever/document_graph.py (and `adapters/astra.py`, `graph_retriever.py`): `create_graph`, `_best_communities`, `group_by_community` (read 20261030, 18:58 to 19:06 UTC)
8. https://github.com/datastax/graph-rag/tree/main/docs/guide: `edges.md`, `strategies.md`, `traversal.md`, `migration.md` (read 20261030, 18:58 to 19:06 UTC)
9. https://github.com/datastax/graph-rag/blob/main/docs/examples/lazy-graph-rag.ipynb: the LazyGraphRAG chain, the $70k estimate, the single-question comparison (read 20261030, 18:58 to 19:06 UTC)
10. https://github.com/datastax/graph-rag/issues and /pulls: issues #107, #123, #124, #126, #170, #178, #181 and #183 (the last two not classified); pull requests #146 (closed 20260630 08:37 UTC, not merged), #177, #179, #180, #182 and the comments on #146, #178, #180; contributors; branches (read 20261030, 18:58 to 19:06 UTC)
11. https://pypi.org/project/langchain-graph-retriever/ and https://pypi.org/project/graph-retriever/ (JSON API): latest 0.8.0 released 20250404, Apache-2.0, no deprecation note (read 20261030, 18:58 to 19:06 UTC)
12. https://datastax.github.io/graph-rag/: docs-site landing page; no deprecation, archival or successor notice, no version or news date (read 20261030, 18:58 to 19:06 UTC)
13. https://docs.langchain.com/oss/python/integrations/retrievers/graph_rag: LangChain integration page; install command, link to this repository, no deprecation notice, no date (read 20261030, 18:58 to 19:06 UTC); plus one web search for the library and 2026 news that found no release notes or third-party evaluation (20261030, 18:58 to 19:06 UTC)
14. https://docs.datastax.com/en/astra-db-serverless/tutorials/graph-rag-typescript.html: own `GraphRetriever` class, no reference to this library, footer "Copyright IBM Corporation 2026" (read 20261030, 18:58 to 19:06 UTC)
15. https://www.dbta.com/Editorial/News-Flashes/IBM-Officially-Closes-Acquisition-of-DataStax-169711.aspx: article dated 28 May 2025 reporting that DataStax announced its acquisition by IBM is closed (read 20261030, 18:58 to 19:06 UTC)
16. Web search result summary for "IBM completes acquisition of DataStax" (20261030, 18:58 to 19:06 UTC): reports that IBM agreed to acquire DataStax on 25 February 2025 and that the deal closed on 28 May 2025. A search summary, not a fetched primary page. Source 15 (dated 28 May 2025) confirms that the close had been announced by then; the 25 February 2025 announcement date rests on this summary and on the July note only
