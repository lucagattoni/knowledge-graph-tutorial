---
slug: youtu-graphrag
neutral-entry: ../../kb-kg/projects/youtu-graphrag.md
investigated: 20260726
updated: 20261030 19:06 UTC
licence-gate: read-only reference (LICENSE limits use to academic purposes and forbids commercial and production use; README badge says MIT; LICENSE unchanged since 20250902; re-verified 20261030 18:58 UTC)
---

# Youtu-GraphRAG: what Pinakes takes from it

The facts about the project itself are in its [neutral entry](../../kb-kg/projects/youtu-graphrag.md). This page
holds only the Pinakes-specific reading. Numbered references like [7] point to that entry's Sources list.

## Verdict

Read for ideas, never vendor code: a declared seed schema that bounds LLM graph extraction is the idea worth
keeping on file, and Pinakes has not built it; the licence closes the code.

## What Pinakes takes

| # | Idea | Pinakes design section it feeds | Note after the July 2026 re-check |
|---|---|---|---|
| 1 | **Seed schema as the extraction budget instrument.** If lazy (`--deep`) extraction ever lands (recommendation R5, see [recommendations](../recommendations-r1-r7.md)), bound it with a template-shipped three-list schema (entity types, relations, attribute types) injected into the extraction prompt. It caps output size and semantic drift, and it is declarative, so it can be audited in the repository like any Pinakes template. The July example was a `research-papers` template carrying `{author, paper, venue, method, dataset}` and `{cites, extends, evaluates_on, authored_by}`. | Templates; the `--deep` loop ([DESIGN](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md) section 4.3 and section 5) | **Add a code-side check.** The shipped prompt only asks the model to prioritise the schema and allows extraction outside it [8]. If Pinakes bounds extraction by schema, it must validate the output against the schema in code and not rely on the prompt. |
| 2 | **One combined extraction call per large chunk**, returning entities, relations and attributes as one JSON, with no separate description or summary passes. | Same as 1 | Confirmed in the code [10]. |
| 3 | **Schema expansion as explicit, reviewable writes.** Youtu-GraphRAG writes proposed new types back into the schema file. The Pinakes version would propose them as a diff the user commits, matching R5's "write results back into committed sidecars", and would add the confidence gate the paper describes. | Sidecars; the `--deep` write-back rule | **Strengthened.** The gate the paper describes does not exist in code, and an external user reports 10 node types growing to 523 after 681 passages, with the prompt reaching about 20,000 tokens [16]. Ungated expansion is a measured failure, not a hypothetical one. |
| 4 | **Naming the schema types a query touches** (`involved_types`) in the decomposition step, then filtering retrieval candidates by type: a cheap precision gain for a possible structural channel. | The staged graph channels (PPR, `[ner]`) | Idea kept on file. Depends on a schema that does not exist yet (see 1). |
| 5 | **AnonyRAG's framing for the golden-set evaluation.** Measure on content the model cannot already know; report reject (abstain) accuracy separately from open accuracy. A personal KB is naturally "anonymous" to the model, so anonymised-corpus numbers are the honest ones, and on those even the best system is weak (38.08 and 42.57 at top-10 [7]). | Evaluation (golden set; false-abstain and false-confidence rates) | The metric already existed; see "Where it landed". |
| 6 | **Thesis confirmation.** Unbounded LLM graph construction is the cost sink, and the fix is declared structure up front. Their schema is the construction-side analogue of Pinakes' typed sidecar `links[]` vocabulary. | Design rationale (free path / paid path split) | Still holds, with the caveat in 1: the savings figures (90.71% in the paper, 33.6% in the README) have no stated baseline in the pages read [7][5]. Do not cite either as evidence for a Pinakes decision. |
| 7 | **Cheap retrieval after an expensive build.** Embeddings, FAISS and graph walks cost nothing per query; the LLM runs only to decompose and reflect (2 to 7 calls). This mirrors Pinakes' free-path / paid-path split, and their IRCoT loop with a step cap is the counterpart of a bounded `--deep` loop. Pinakes adds what they lack: cost reservation and a spend ledger. | Free path vs paid path; `--deep` | Confirmed [13][14]. |
| 8 | **Community summaries as L4 nodes retrieved like any other node**: a lightweight alternative to Microsoft GraphRAG's expensive community reports. | None scheduled | Idea kept on file only. |

## What Pinakes leaves

| What | Why |
|---|---|
| **The code** | Academic-only licence; see the gate below. |
| **The dependency weight** | PyTorch, transformers, sentence-transformers, FAISS, spaCy, MinerU, Apache Tika (Java), FastAPI, and Neo4j for visualisation, Docker first [15][5]. Antithetical to Pinakes' light-core rule. |
| **Eager whole-corpus extraction** | Every chunk reaches the LLM at build time [10]. That breaks the free path. Pinakes takes the schema idea but would apply it lazily and query-scoped (R5), never corpus-wide. |
| **Ungated schema auto-expansion** | The code accepts every non-duplicate type the model suggests [10]. With no human in the loop the schema drifts, and issue 168 shows it growing without bound on one corpus [16]. Pinakes keeps the user as the commit gate. |
| **The four-level tree as storage** | Communities and keywords are derived state. If ever wanted they belong in the disposable `.pinakes/` directory, not in the document model. |

## Where it landed in Pinakes

Read 20261030 19:02 to 19:03 UTC. Latest release at that read: 0.32.8, with STATUS "last reviewed 20261029 18:57".
The authority is Pinakes' [STATUS.md](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md); the
[ROADMAP.md](https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md) and
[DESIGN.md](https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md) give the history and the design.

| Idea from the project | What Pinakes built | Where it says so |
|---|---|---|
| Seed schema shipped in a template and injected into LLM extraction (take 1) | **Not built.** Pinakes has no LLM entity or relation extraction. "Extraction" in STATUS means PDF text extraction (the free `pypdfium2` extractor and the opt-in paid `claude-vision` extractor). `pnk init` ships one template, `notes`; at 0.22.0 "a second template is a no-go", so the July `research-papers` example does not exist. A search of STATUS, ROADMAP and DESIGN for "R5", "seed schema" and entity extraction found nothing. | STATUS, the `pnk init` row and the 0.22.0 row |
| Lazy, schema-bounded extraction under `--deep` (R5) | **Not built.** `pnk ask --deep` shipped in 0.24.0 and has worked against the live API since 0.25.1. Its loop decomposes the question, searches each part, answers from the merged evidence and re-folds. It extracts no entities and uses no schema. | STATUS, the `pnk ask --deep` row |
| One combined extraction call per chunk (take 2) | Not applicable: no extraction call exists. | n/a |
| Schema expansion as a reviewable diff the user commits (take 3) | **Nearest thing: printed link suggestions, not schema types.** Since 0.26.0 a `--deep` run ends by printing `links[]` entries (`rel: co-cited`, `origin: deep`) that its own citations propose, for the user to review and commit. It prints and never writes. `--write-suggestions` is deferred and unplanned. A document cannot talk the model into a suggestion, because suggestions come from passage numbers the response schema bounds. | STATUS, the 0.26.0 row; ROADMAP, "The deep release" |
| Type-filtered retrieval from `involved_types` (take 4) | **Not built.** The PPR channel and the `[ner]` extra are staged, "eval-gated, never scheduled", with deliberately no implementation plan. The structural expansion channel that was built (schema_version 3, `[retrieval] graph_channel`) did not pass its gate on the 300-RFC corpus on 20260804 and ships `off`. | STATUS, release roadmap and "Did the expansion channel earn its default"; ROADMAP, "The graph release, staged" |
| Bounded retrieve-reflect loop with a step cap (take 7) | **Built, in a different form.** The `--deep` loop is bounded by `[deep] max_rounds` and three `[budget]` windows. It is priced and refused before the first call, confirmed once, and reserved and reconciled per call. Every paid run writes a transcript. The paid-path allowlist is complete at two entries (the `claude-vision` extractor and `--deep`). | STATUS, the `pnk ask --deep` and deep-round estimator rows; ROADMAP |
| Reject/abstain accuracy reported separately (take 5) | **Built, as a related metric.** The July note named Pinakes' false-abstain rate as the match. The golden set has a no-answer class, and the evaluation reports false-abstain and false-confidence rates; these are not the same measure as the paper's reject-mode accuracy. Demo KB, 74 questions, `[light]` models, 20260801 12:14: false-abstain 0.015, false-confidence 0.25 (STATUS holds later runs). | STATUS, "Measured numbers"; DESIGN, the confidence heuristic |
| An anonymised-entity corpus (AnonyRAG style) | **Not built.** No mention of anonymised evaluation corpora in STATUS, ROADMAP or DESIGN. The demo KB is a synthetic corpus written for the purpose, for "zero licensing risk" and better test signal than found text. | DESIGN, the golden-set section |
| Eager whole-corpus extraction (left) | Pinakes does not do it. The free path stays free; the only paid paths are the two above. | STATUS; ROADMAP |

## Licence gate

**Read-only reference.** The operative sentence of the project's `LICENSE`, re-read 20261030 18:58 UTC: "You agree
to use the Youtu-GraphRAG only for academic purposes, and refrain from using it for any commercial or production
purposes under any circumstances." [4] The README badge says MIT; the `LICENSE` file governs. Pinakes is
Apache-2.0 and its server is a network service, so copying this code would reach anyone who embeds Pinakes.
**Ideas and measured results are free to reuse; source is not.** This page and the neutral entry describe ideas and
published numbers only and quote no code. The AnonyRAG dataset is separately licensed cc-by-nc-4.0 [19], so it
cannot be vendored into a commercial Pinakes artefact either.

## Changed since July 2026

Checked 20261030 18:58 to 19:06 UTC. Details and sources are in the neutral entry's "Changed since the July 2026
investigation".

- **Verdict: unchanged.** Nothing found alters it.
- **Licence gate: unchanged and re-verified.** The `LICENSE` file has had one commit since 20250902. The MIT badge
  in the README is still wrong.
- **Strengthened leave.** Issue 168 (20261004) is the first outside evidence that ungated schema expansion fails on a
  large corpus [16]. It supports "Pinakes keeps the user as the commit gate".
- **New caution on take 1.** The July note read "the LLM may only emit triples whose types appear in S" as how the
  code works. That wording is the paper's; the prompt allows extraction outside the schema [8][7]. Any Pinakes design
  that uses a seed schema as a budget bound needs an enforced check.
- **Project status.** Quiet since 20260226 (246 days); the July note called it active. This does not change what is
  worth reading, but a read-only reference is unlikely to see fixes for the schema-growth issue.
- **Pinakes side.** Take 7's "cost reservation plus spend ledger" is now shipped and measured (the `--deep` release,
  0.24.0 to 0.26.0); takes 1 to 4 remain unbuilt.

## Sources

Pinakes documents, read 20261030 19:02 to 19:03 UTC:

- https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md : release 0.32.8, the `pnk init`, `pnk ask --deep`, deep-round estimator and extraction rows, the 0.22.0 and 0.26.0 rows, "Measured numbers", the expansion-channel result
- https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md : "The graph release, staged", "The deep release", the paid-path allowlist
- https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md : sections 4.3, 5, the golden-set and confidence-heuristic passages, the release-order table

Project facts: the numbered references [4] to [19] are the Sources of the
[neutral entry](../../kb-kg/projects/youtu-graphrag.md).
