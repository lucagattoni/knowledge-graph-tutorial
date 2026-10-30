---
slug: claudekb
investigated: 20260725 15:31 (second pass 20260726 08:52), local time as written then
updated: 20261030 19:06 UTC
live-check: 20261030 18:58 to 19:04 UTC
licence-gate: open (MIT, read from the LICENSE file)
---

# ClaudeKB: the in-house precedent

## What this page is

ClaudeKB is the owner's own earlier project: a **blueprint** for a fleet of docs-as-code knowledge
bases that AI agents write and maintain. Its public repository is
[lucagattoni/ClaudeKB](https://github.com/lucagattoni/ClaudeKB). This page is the July 2026
investigation of it, moved here from Pinakes and kept at full depth, with three additions at the top:
what changed in the repository since July, where the investigation's proposals landed in Pinakes, and
what the Open Knowledge Format is (ClaudeKB's research aligned its frontmatter with it).

It is **not** split into a neutral entry plus a takeaways page, because it is in-house work and belongs
to the Pinakes section. The field-neutral entries for *external* projects are in
[`../../kb-kg/projects/`](../../kb-kg/projects/) and their Pinakes reading is in
[`../takeaways/`](../takeaways/). The design these lessons fed is in
[`../approach/PINAKES_APPROACH.md`](../approach/PINAKES_APPROACH.md).

| Item | Value | Source |
|---|---|---|
| Original investigation | 20260725 15:31, second pass 20260726 08:52. Pinakes' ROADMAP says its timestamps up to 20260804 11:32 are local (Europe/Rome) and were never converted, so these two are local time | [S17] |
| Repository | public, not archived, default branch `main` (the only branch) | [S1] |
| Licence | MIT. The `LICENSE` file says MIT, copyright 2026; the API says the same; the README has no badge and says "See LICENSE" | [S1] [S4] |
| Latest release | v0.4.0, published 20260712 17:20 UTC | [S2] |
| Stars / forks | 0 / 0 | [S1] |
| Verdict on the July conclusions | unchanged: nothing in the repository moved after 20260712 | [S3] |

The July text below uses the tense and names of July. It calls unbuilt Pinakes work by plan names
(`pnk adopt`, "graph channel"); the section [Where it landed in Pinakes](#where-it-landed-in-pinakes)
says what exists.

## Changed since July 2026

Checked 20261030 18:58 to 19:04 UTC against the live repository, a fresh shallow clone of `main`
(commit `1f5694e`) and the GitHub API.

| Question | Finding | Source |
|---|---|---|
| Last push | `pushed_at` 20260712 17:20:24 UTC. The head commit "Release 0.4.0" was committed 20260712 17:20:22 UTC. That is **13 days before** the July investigation began (20260725) | [S1] [S3] |
| Releases | Six, `v0.1.0` to `v0.4.0`, all published on 20260712 between 16:09 and 17:20 UTC. `v0.4.0` is the latest. None since | [S2] |
| Commits since 20260801 | **None.** The API query `commits?since=2026-08-01T00:00:00Z` returned an empty list | [S3] |
| Open issues or pull requests | None (the issues-and-PRs list is empty; one branch only) | [S1] |
| Architecture changed? | **No.** `src/kbtool/` still holds 11 Python modules with 1,157 lines (July: "~1,150 lines across 11 modules"). `validators.run_all` still runs the nine validators the July text describes. `cli.py` still defines the eight subcommands. The ownership boundary, gate and playbooks are as described. Because no commit post-dates 20260712, nothing the July pass could have read from the published repository can have changed. Whether the July pass read an unpushed local copy: **unstated** | [S6] [S3] |
| Deferred retrieval layer built? | **No.** The roadmap still lists, under "Future extensions (designed for, not built)": unified cross-KB search, an MCP / RAG retrieval layer ("evaluate reusing an existing local-first tool (e.g. Basic Memory) before building"), offline reading, a backlinks emitter, and a split public/private build. A search of `src/` for `mcp` finds nothing | [S5] [S6] |
| Backlinks emitter built? | **No.** `backlink` occurs in `src/` zero times. It occurs only in the roadmap, the architecture spec's deferral (D13) and the research notes | [S5] [S6] |
| Next steps named by the roadmap | A second real KB, and a docs polish / MkDocs preview of the guide | [S5] |
| Where the repository lives | The old URL `github.com/lucagattoni/ClaudeKB` now answers **HTTP 301** to a repository under a separate organisation account. The API's canonical name differs from `lucagattoni/ClaudeKB`. That organisation was created 20260712 14:15 UTC, the day the repository was created (08:47 UTC). When the move happened: **unstated** | [S1] |
| Small differences from the July text | The architecture spec's iteration log lists passes 0 (draft) to 10; the July text says "9 review passes". Pass 10 is a post-launch fix entry (20260712 16:54), so 9 matches passes 1 to 9 (my reading, not stated). The July text refers to a private `docs/private/` decision record; that directory is absent from the public tree, and the 0.3.0 changelog entry says the private record "moved out of the tracked tree" | [S7] [S8] |
| The standard it aligns with | The Open Knowledge Format moved from v0.1 (June 2026) to v0.2 on 20260724, and now lives in its own repository. ClaudeKB has not followed. See the OKF section below | [S10] [S12] |

**Effect on the July conclusions.** None of them depended on a ClaudeKB change, and none has been
overtaken by one. The one open question the July text raised, whether Pinakes could serve as the
deferred retrieval layer, has not been tested from either side: ClaudeKB has built no layer, and
Pinakes has built no adapter (below).

## Where it landed in Pinakes

Sources: Pinakes' `STATUS.md` (latest release **0.32.8**, "last reviewed 20261029 18:57" in its own
header, v0.32.8 published on PyPI per its ROADMAP 20261029 18:53 UTC) and `ROADMAP.md`, plus
`CLI.md`, `DESIGN.md` and the changelog where those two are silent. Read 20261030 19:00 to 19:04 UTC
from a checkout of the public repository whose head matches the repository's last push. STATUS says it
is "the only place in the repo that says what is built" [S16].

| July proposal or lesson | State on 20261030 | Evidence |
|---|---|---|
| **Pinakes as ClaudeKB's deferred retrieval layer**; fleet of ClaudeKB KBs indexed | **Not built, not mentioned.** Neither `STATUS.md` nor `ROADMAP.md` contains the word ClaudeKB. The graph release's plan named "a hand-adopted ClaudeKB corpus as second KB"; the second corpus actually built and measured is [`pinakes-corpus-rfc`](https://github.com/lucagattoni/pinakes-corpus-rfc) (300 RFCs), not a ClaudeKB-templated KB. Whether `pinakes_list_kbs` can be seeded from `kb.yml` files: **unstated** | [S16] [S17] [S22] |
| **`pnk adopt`**: generate sidecars from frontmatter, resolve `kb://` links to ULID edges | **Does not exist.** Pinakes' public [`docs/README.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/README.md) says it is unimplemented, and that which release owns it is D-8 of the template-release plan, unanswered. Its changelog (0.32.0) records that `grep -rn '"adopt"' src/` returned 0 hits; the same search on 20261030 19:01 UTC at the head again returned nothing. A note added to the approach document on 20260825 says the template release **closed at 0.22.0 without it** and that the release row naming it "did not happen". `frontmatter` does not occur in `STATUS.md`, `ROADMAP.md` or `DESIGN.md` | [S20] [S22] |
| Nearest shipped pieces to adoption | `pnk init` **adopts a directory that already has content** and never overwrites a file it finds (0.14.0). `pnk sync` mints a sidecar, with a permanent ULID, for each document. `pnk upgrade --apply` "adopts" template hunks into `pinakes.toml` (0.20.0) and refuses the whole run on any conflict. The last is a different meaning of the word and has nothing to do with ClaudeKB | [S16] [S17] [S18] |
| **Link authoring** (lessons 1 and 9: agents write strict link syntax if a tool resolves names to ULIDs) | **Shipped, in a different shape.** `pnk link` (0.6.0) writes one `links[]` entry into the source document's own **sidecar**, resolves aliases and `self` to ULIDs before anything reaches disk, and never mints a sidecar. `pnk links` and the MCP tool `pinakes_links` traverse both directions (0.5.0, depth capped at 3). A reverse scan records what other KBs link in. `pnk ask --deep` ends by **printing** `links[]` entries its own citations propose (0.26.0); it never writes them, and `--write-suggestions` is "deferred and unplanned". DESIGN gives sidecars as the one mechanism, not in-text links, because a PDF cannot carry a wikilink and source documents are not mutated; it states the cost: "nobody hand-writes YAML per document". Whether Pinakes reads Markdown links in document bodies as edges: **unstated** in the documents read | [S16] [S17] [S19] |
| Do agents then author such links reliably? | **Not measured** in anything read. No measurement of agent link authoring appears in `STATUS.md` | [S16] |
| **Lesson 1**: authored links are sparse, precious signal; nudge rather than assume density | Measured on the RFC corpus only: **53.3% (160 of 300)** documents carry an authored link, the median out-degree is **1**, the worst is **86** (one hub). STATUS calls the approach document's "sparse, precious" claim "half right". The links there come from RFC headers (`obsoletes`, `updates`), not from agents writing under a gate, so the measurement does not test the July lesson that agents under a gate write minimal links (my reading). `pnk doctor` reports **link coverage as a ratio** and dangling links (0.6.0); it is a report, not a gate | [S16] [S18] |
| **A structural gate** (a `pnk check` for unlinked documents, unused tags, dangling `pnk://` targets) | **No `pnk check` command.** The nearest is `pnk doctor`, a health report that lists orphaned sidecars (a sidecar with no document: a different thing from an unlinked document), duplicate IDs, dangling links, link coverage and the highest-degree edge hubs. `--prune`, which deletes orphaned sidecars, is the only thing it can change. Whether any `doctor` finding blocks a commit or a sync: **unstated** in the section read. A document with no links is visible only as a lower coverage ratio | [S16] [S18] |
| Secret scan in the gate; publishing and access control | **Not found.** A search of `STATUS.md` for `secret` returns nothing, and publishing a KB is not described there. Related but different: `pnk init` reports a `.pinakes/` that git already tracks, because it holds the user's verbatim questions (0.30.3, which STATUS lists as "on `main`, unreleased") | [S16] |
| **Lesson 7**: make linking a precondition of writing (ingest playbook, `CLAUDE.md` contract) | **Not built.** The word "playbook" occurs zero times in `STATUS.md`, `ROADMAP.md` and `GUIDE.md`. No rule of the form "link it or the gate fails" is described | [S16] [S17] |
| **Free structural edges and the graph channel** (lessons 1, 3, 8; ClaudeKB as "best-case corpus" for PPR) | **Built and measured; the channel ships off.** The graph release (0.11.0, `schema_version` 3, which forces a rebuild; there are no migrations by design) derives a `nodes`/`edges` graph over chunk, document, tag, heading and directory nodes, and `doctor` reports the highest-degree hubs. The expansion channel `graph_channel` defaults **off** because its gate failed on the RFC corpus: of 20 multi-hop questions, **0 improved and 3 regressed**, p = 1.0000 (20260804 22:52). STATUS' finding: "reachable ≠ retrievable". The PPR channel is "the graph release, staged": eval-gated, "never scheduled", not built. The July prediction that a ClaudeKB corpus is the best case for the channel: **untested**, because no ClaudeKB corpus was measured | [S16] [S17] |
| **Lesson 8**: "derivable nearly for free" never ships without a consumer | Pinakes' structural edges have a consumer (the fusion channel), and are built; the consumer is off by default. ClaudeKB's backlinks emitter still has no consumer and is still unbuilt. Pinakes answers the reader's question differently: `pnk links --direction` shows what connects to a document | [S16] [S17] [S5] |
| **Lesson 3**: ULID identity beats path identity | In place: the sidecar holds the document's permanent ULID, `doctor` reports duplicate IDs, and `pnk link` resolves to ULIDs before writing. Not tested against a ClaudeKB-style rename | [S18] [S17] |
| **Lesson 4**: a curated vocabulary prevents noise cliques in the shared-tag edge | Hub reporting shipped. A per-KB controlled vocabulary or a high-degree-tag penalty: not found. The one measurement points the same way as the lesson: on the RFC corpus the harm came from document-level transit into `co-located` (262 edges) and `shared-tag` (643 edges) hubs, which "pull whole documents' chunks into the fusion". Those tags came from the RFC Editor's keywords, not a curated vocabulary | [S16] |
| **Lesson 5**: lazy semantic work as a batch, explicit, persisted pass | The deep release (0.23.0 to 0.26.0): `pnk ask --deep` is explicit, priced and refused before the first call against three budget windows, and keeps the free path free. Its results are printed for review, not written back. A scheduled `lint`-style maintenance pass: **not found** | [S16] |
| **Migrations** (ClaudeKB ships them; Pinakes' invariant is none) | Unchanged. A derived-index change means `pnk sync --rebuild`, which is free. The template ecosystem (0.21.0) covers `pinakes.toml` only: `pnk upgrade --apply` is "the only thing in Pinakes that rewrites a `pinakes.toml` after `pnk init`". What happens on a **sidecar** schema change: **unstated** | [S16] |
| **Open Knowledge Format** | **Not taken up.** `okf` and `open knowledge format` occur nowhere in Pinakes' `docs/` (outside the July investigations), `CHANGELOG.md`, `README.md`, `plans/` or `src/` (searched 20261030 19:03 UTC). Whether Pinakes sidecars could carry OKF fields: **unstated** | [S16] |

**Net.** The generic mechanisms the lessons pointed at exist: sidecar link authoring with ULID
resolution, link traversal both ways, a derived structural graph, a hub report, and a budgeted,
explicit semantic pass. The ClaudeKB-specific path does not: no `pnk adopt`, no frontmatter-to-sidecar
generation, no `kb://` resolution, no seeding of a fleet from `kb.yml` files, no measurement on a
ClaudeKB corpus. The one
result that bears on the July bet, the graph channel, was measured on a different corpus and came out
negative.

## Open Knowledge Format: what it is and who defines it

ClaudeKB's research aligned its frontmatter with the Open Knowledge Format (OKF), and the July text
calls ClaudeKB's frontmatter "a deliberate OKF superset". Everything below was read on 20261030 and
only what the sources say is stated.

**What it is.** The v0.2 specification calls OKF "an open, human- and agent-friendly format for
representing knowledge": a **directory of Markdown files with YAML frontmatter**, a "bundle", with "no
schema registry, no central authority, and no required tooling" [S10]. That sentence is about types
and tooling: §4.1 says `type` values "are not registered centrally". It does not say who controls the
specification.

| Property | What the spec says | Source |
|---|---|---|
| Required key | `type` only. A concept carrying just `type` is conformant. Consumers "MUST tolerate unknown types" | [S10] §4.1 |
| Recommended keys | `title`, `description`, `resource`, `tags` | [S10] §4.1 |
| Reserved files | `index.md` (directory listing, no frontmatter) and `log.md` (change history) at any level | [S10] §3.1, §8, §9 |
| Links | Standard Markdown links, bundle-root-absolute or relative. Consumers must not reject a bundle for broken links, unknown keys, unknown types, missing optional fields or missing `index.md` | [S10] §6, §11 |
| Conformance | Parseable frontmatter on every non-reserved `.md`, a non-empty `type`, reserved files in the right structure | [S10] §11 |
| Versioning | `<major>.<minor>`; a bundle may declare `okf_version: "0.2"` in the **bundle-root `index.md`**, the only `index.md` that may carry frontmatter | [S10] §8, §12 |

**Who defines it.**

| Fact | Source |
|---|---|
| Announced in a Google Cloud blog post of **20260612** by the Google Cloud Data Cloud team (the page's own date and byline, as returned by the fetch), as "an open specification that formalizes the LLM-wiki pattern". It calls OKF "a starting point, not a finished standard" | [S13] |
| The specification is published in the GitHub organisation `GoogleCloudPlatform`. v0.1 and then v0.2 lived in `GoogleCloudPlatform/knowledge-catalog` under `okf/`; the commit "migrate format and tooling to Open Knowledge Format v0.2" is dated **20260724 16:45 UTC** | [S12] |
| A dedicated repository, `GoogleCloudPlatform/open-knowledge-format`, was created **20260811**. The `okf/` copy in `knowledge-catalog` now carries a banner: it "is a frozen snapshot, no longer maintained". Both repositories report Apache-2.0 through the API, and the dedicated repository's `LICENSE.md` is the Apache 2.0 text; it had 1,177 stars on 20261030 | [S11] [S12] |
| Contribution rule: spec changes "are held to a higher bar"; open an issue before a pull request; a Contributor License Agreement is required | [S11] |
| Governance: the spec, README, CONTRIBUTING file and blog post name **no standards body and no multi-party process**. They present OKF as "vendor-neutral" with Google as its publisher and maintainer. I found no other governing body in the pages read | [S10] [S11] [S13] |
| Text changed after v0.2 without a new version number: commits dated 20260820 (dedicated repository) and 20260821 (`knowledge-catalog`) "make every timestamp an ISO 8601 datetime with an explicit offset"; in the dedicated repository two further commits drop timestamp conformance text from §5 and §11. `SPEC.md` still reads "Version 0.2" | [S11] [S12] |

**What v0.2 changed from v0.1** (spec §13) [S10]. Breaking: `timestamp` is superseded by
`generated: {by, at}`, and the body `# Citations` list by a `sources` frontmatter field. Additive:
trust and provenance families (`sources` with credibility signals, `generated`, `verified`), lifecycle
keys (`status`, `stale_after`), a new concept type `Attested Computation`, and an actor convention
(`<producer>/<version>`, `human:<id>`, `process:<id>`).

**Third-party projects that say they implement v0.2.** Two found by search and checked through the
GitHub API and their READMEs. Neither is in the `GoogleCloudPlatform` organisation, and their
conformance claims were **not tested** here.

| Project | Claim in its README | Licence | Created | Last push | Stars | Source |
|---|---|---|---|---|---|---|
| `W4G1/okf` | "A pure-Rust implementation, library and CLI toolkit for the Open Knowledge Format (OKF) v0.2" | Apache-2.0 | 20260616 | 20260904 | 29 | [S14] |
| `bushans/okfgen` | "Tracks the OKF v0.2 spec; every bundle it emits passes its own conformance validator"; repository description: "Based on Google's OKF Spec" | Apache-2.0 | 20260701 | 20261007 | 0 | [S15] |

I could not tell which project the phrase "Google OKF v0.2" came from; both fit.

**How ClaudeKB relates to OKF today.** ClaudeKB's research note 02 analysed SPEC **v0.1** on 20260712
("Google, June 2026") [S9], and the repository has not changed since. Read against v0.2:

| Point | ClaudeKB (code read 20261030) | OKF v0.2 | Compatible? |
|---|---|---|---|
| Required key | `type`, `title`, `description` on every page under `docs/` except `index.md` and `log.md` | `type` only | Yes: ClaudeKB's rule is stricter |
| Unknown frontmatter keys | Allowed and preserved (`additionalProperties: true`) | Must be preserved | Yes |
| Reserved files | `index.md` and `log.md` **must have no frontmatter**: `check_frontmatter` reports an error if one has any | The bundle-root `index.md` **may** carry `okf_version` | **No.** A bundle that declares `okf_version` would fail ClaudeKB's gate |
| `status` key | Enum `draft`, `review`, `published`, `archived` | Enum `draft`, `stable`, `deprecated`, default `stable` | **Same key, different values.** Only `draft` overlaps. Not a §11 conformance failure, which asks for little, but a §5 "SHOULD" mismatch |
| Dates | None stored; dates derive from git history (D6) | `generated.at` replaces `timestamp`; ISO 8601 with offset | Not aligned. The build appends a footer line "Last updated: <date> from git history" to each page (architecture spec, preprocess step 3, which says this "satisfies OKF `timestamp` recommendation"); it adds no `timestamp` or `generated` frontmatter field. Whether the built output meets v0.2: **unstated** |
| Provenance and trust | No `sources`, `generated`, `verified`, `stale_after`, `okf_version` anywhere outside the research notes | First-class in v0.2 | Not adopted |
| Broken links | Build error (strict producer) | Consumers must tolerate | Compatible by the producer / consumer split the research chose (F2.2) |

Research note 02 itself flagged this risk: "Watch OKF evolution (v0.1 to v1): joining now means
tracking a moving spec" [S9].

---

# The July 2026 investigation

*Everything below is the July text. Its content is unchanged. The edits are: links rewritten to the
new layout (STATUS.md now points to its public URL); "the user" now reads "the owner"; the literature
review is linked at its new home; three short "as of July" or "status on 20261030" notes (marked in
italics) are added under the two tables and the "Answer" paragraph of the deferred-layer section; and
the key-sources list gains a line saying where the paths resolve. Statements in it were read from the
ClaudeKB repository on 20260725 and 20260726 (local time). Those re-checked on 20261030 are in the
sections above.*

> **Version numbers and plan names below reflect the convention in use when this was written.** Unbuilt
> work is now **named, not numbered**
> ([STATUS.md](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md)). This record is left
> as it was.

**Repo:** https://github.com/lucagattoni/ClaudeKB · **Investigated:** 20260725 15:31 · second pass
(playbooks, kbtool, decisions, research, retrieval-layer fit): 20260726 08:52

## What it is

ClaudeKB is not a knowledge base — it is a **blueprint**: a copier template plus a small Python
toolchain (`kbtool`, ~1,150 lines across 11 modules in `src/kbtool/`) that scaffolds and upgrades a
fleet of independent KB repos. Each generated KB is a standalone git repo of Markdown under
`docs/`, validated by a strict gate (`kbtool check`), built by a static site generator (Zensical,
with an mkdocs-material fallback), and deployed as a private-by-default static site behind
Cloudflare Access. Agents write to it by **direct commits to main**; Workers Builds re-runs the
gate on push and deploys only if green. The KB never depends on the blueprint at runtime — kbtool
travels inside each KB as a vendored wheel, playbooks ship as package data, and a checksum manifest
(`blueprint-checksums.json`) enforces the blueprint-owned vs KB-owned file boundary.

Reached v0.4.0 in a single day of adversarial-review-driven design (9 review passes recorded in
`docs/architecture.md`'s iteration log); KB #1 went live end-to-end and drove two post-launch fixes.

## How knowledge is structured

- **Pages**: long-form Markdown under `docs/`, one concept per page. Required frontmatter on every
  page (`type`, `title`, `description`), validated against a JSON Schema plus a per-KB controlled
  vocabulary (`vocab.yml` lists allowed `type`s and `tags`). `index.md`/`log.md` are frontmatter-free
  by convention (Open Knowledge Format alignment). No date fields — dates derive from git history.
- **Links are plain Markdown and human/agent-authored**: intra-KB bundle-root-absolute
  (`[X](/concepts/alpha.md)`); cross-KB via a logical scheme `kb://<kb-name>/<path>.md`, rewritten
  at build time to a real URL (`https://kb-<name>.<domain>/<url-path>`). One shared implementation
  (`src/kbtool/links.py`) serves both the validator and the preprocessor.
- **Graph-ness is enforced, not just permitted.** Two structural validators make the corpus a
  connected graph by construction (`src/kbtool/validators.py`):
  - `check_index_reachability` — every page must be reachable from `docs/index.md` by following
    intra-KB links (BFS over the link graph). Orphans are build **errors**.
  - `check_nav` — every page must appear in the curated `nav.yml` (explicitly or via a glob
    section). Missing-from-nav is an error.

  So there is a real link graph, but no backlinks, no typed edges, no graph queries — a
  "backlinks emitter" derived from the validator's link graph is explicitly deferred
  (`docs/guide/roadmap.md`).
- **Catalog and log**: `docs/index.md` is a hand-curated catalog (the graph's root); `docs/log.md`
  is an append-only change log with a git union-merge driver so parallel agent sessions both land.

## How retrieval actually happens

There is **no retrieval engine**. Three mechanisms, none ranked:

1. **The agent reads files.** The session ritual (`template/CLAUDE.md`) starts every session with
   "read `docs/index.md` and the tail of `docs/log.md`" — the catalog is the entry point, then the
   agent navigates links or greps. Retrieval quality is entirely the agent's navigation plus the
   curator's discipline in keeping `index.md` honest.
2. **Client-side site search** for human readers: the SSG emits a `search.json` lexical index
   (kept behind the login on private KBs). Nothing consumes it programmatically.
3. **Structure as recall insurance**: the orphan check guarantees anything ingested is findable by
   walking from the index — retrieval-by-navigation cannot silently lose a page.

Cross-KB search, an MCP/RAG layer, and backlinks are all named as "future extensions (designed
for, not built)" — the design's stated bet is that plain Markdown in git is "directly ingestible
by future retrieval layers" (`README.md`, `docs/guide/what-is-claudekb.md`).

## The agent's role: Claude as the engine

ClaudeKB inverts Pinakes' architecture. Pinakes is an engine Claude calls as tools; ClaudeKB is
**Claude as the engine over plain files**, with code confined to validation and plumbing:

- All intelligence — deciding create-vs-extend, writing, linking, curating the index, semantic
  maintenance — is delegated to the agent via *prose contracts*: a checksummed, blueprint-owned
  `CLAUDE.md` (session ritual, conventions) plus a KB-owned `CLAUDE-KB.md` (topic, page types),
  and versioned playbooks printed by `kbtool playbook <ingest|lint|upgrade|access-dns-setup>`.
- Code never touches meaning; it enforces *shape*: schema, link resolution, reachability, nav
  coverage, append-only log, ownership checksums, secret scan, Markdown lint.
- Where the agent can't be trusted, the design uses **structural guarantees over conventions**
  (the blueprint CLAUDE.md's first working principle): the deploy gate re-runs everything in CI, so
  a contract-violating commit lands in git but never deploys.
- Even corpus health is an agent job: the `lint` playbook is a scheduled agent session doing a
  semantic pass — contradictions, staleness, "orphan-in-spirit" pages, missing cross-references.

## Guardrails and publishing

- **Two independent visibility axes** (`docs/guide/public-and-private-kbs.md`): repo visibility
  (GitHub — exposes source, full history, commit emails) vs site visibility (Cloudflare Access —
  exposes rendered content). The guide enumerates all four combinations and their exposures.
- **Secret scan in the gate** (v0.4.0, `src/kbtool/secrets.py`): scans `docs/**/*.md` for
  private-key blocks and provider token shapes (AWS/GitHub/Google/Slack). High-confidence match =
  **error on a public KB** (deploy blocked), **warning on a private one** — so you learn before
  ever flipping it public. Personal emails and generic `key = <long value>` assignments are always
  warnings; example/noreply addresses are ignored; `kbtool-allow-secret` on a line suppresses.
- **Publish-safe identity**: the scaffold sets the KB's git email to a GitHub noreply so history is
  safe if the repo ever goes public; the publish checklist demands vetting *history*, not just the
  tree.
- **Partial-public split**: only `docs/public/**` is world-readable on a private site; documented
  residual leaks (global nav exposes private page *titles*; `kb://` links to private KBs reveal
  their existence and paths) are accepted and written down rather than hidden.
- **`kbtool verify-access`** probes the live site anonymously and asserts behaviour matches the
  `kb.yml` record — repo as source of truth, dashboard as cache.
- The secret scan even has a committed adversarial fixture: `docs/concepts/leaky.md` is a page
  carrying a fake GitHub token with `kbtool-allow-secret` markers on every line — the allow
  mechanism dogfooded on the blueprint's own docs.

## The playbooks, one by one

Five prose procedures constitute the *entire* authoring and operations layer. Four ship inside the
kbtool wheel (`src/kbtool/data/playbooks/`, printed by `kbtool playbook <name>` so the procedure is
always version-matched to the installed tool); one lives in the blueprint (`playbooks/scaffold-kb.md`)
because it runs before any KB exists.

**`ingest`** (`src/kbtool/data/playbooks/ingest.md`) — the fully-specified authoring workflow.
Seven steps, each a concrete obligation:

1. **Create vs extend** — prefer extending an existing page when the knowledge belongs to an
   existing concept; create a new page only for a distinct concept. The *criteria* (page types,
   when each applies) are delegated to the KB-owned `CLAUDE-KB.md` — the playbook carries the
   decision procedure, the KB carries the taxonomy.
2. **Write with schema** — required frontmatter `type` (in `vocab.yml`), `title`, `description`;
   optional validated `tags`/`status`; link rules restated inline (root-absolute intra-KB, `kb://`
   cross-KB, media placement); no date fields ever (git supplies dates at build).
3. **Link it from `docs/index.md`** — directly or via a page already reachable from the index.
   This is the graph-building obligation: every ingest must attach the new node to the connected
   component, because the orphan validator fails the gate otherwise.
4. **Add to `nav.yml`** — explicitly or confirm a glob section already covers it.
5. **Append a `docs/log.md` entry** (`## <YYYYMMDD HH:MM> ingest | <summary>`), never editing
   earlier entries.
6. `kbtool check` — fix every error.
7. Commit, `kbtool push`.

The constraint structure is notable: steps 3–4 mean an agent *cannot* add knowledge without also
doing graph and navigation maintenance — curation is not a separate virtue, it is a precondition
of landing the write. This is the piece Pinakes' authoring story lacks.

**`lint`** (`src/kbtool/data/playbooks/lint.md`) — scheduled health pass, explicitly split into a
**structural pass** (deterministic: `kbtool check`, a lychee external-link sweep kept out of the
deploy gate because external flakiness must never block deploys, and a spot-check of `kb://`
targets, which are unresolvable at build time by design) and a **semantic pass** (agent judgement:
contradictions, staleness, orphans-in-spirit, missing cross-references, gaps — fix the unambiguous,
file the rest as `status: review`, log the session).

**`upgrade`** (`src/kbtool/data/playbooks/upgrade.md`) — read the CHANGELOG between recorded and
target blueprint versions; `copier update` (copier itself version-pinned); conflicts expected
*only* where the ownership boundary was violated, resolved favouring the blueprint; run any
content-migration playbooks the CHANGELOG names; gate, commit, push, log.

**`access-dns-setup`** (`src/kbtool/data/playbooks/access-dns-setup.md`) — dashboard steps for the
private Allow app plus the `/public` and `/assets` Bypass apps, each mirrored in `kb.yml`'s
`platform:` record; skipped for `visibility: public` KBs; verified by `kbtool verify-access`.

**`scaffold-kb`** (`playbooks/scaffold-kb.md`) — one-time org/Zero-Trust prerequisites, then per
KB: create private repo → `copier copy` at a pinned tag → `uv lock`, git init, **set noreply
commit identity** → local gate must pass before first push → wire Workers Builds → access playbook
→ log entry. No central registry: the fleet is discoverable only via each repo's `kb.yml`.

## kbtool, command by command

The full CLI surface (`src/kbtool/cli.py` — argparse, eight subcommands):

| Command | Mechanism | Graph-relevant? |
|---|---|---|
| `check` | Runs all nine validators in `validators.py:run_all`; warnings print, any error exits 1 | **Yes** — see below |
| `build` / `ci` | `check` → preprocess → Zensical strict build → post-build assertions (`build.py`); `ci` is the alias Workers Builds invokes | Preprocess rewrites the link graph to URLs |
| `serve` | Preprocess + SSG live preview of the `.build/` copy | — |
| `push` | `git pull --rebase --autostash` then push, 3 attempts with backoff (`vcs.py:push`) — the parallel-writer story | — |
| `status` | Working-tree cleanliness + last deploy result read from the GitHub check-runs API via `gh` (the auth agents actually have), falling back to wrangler, then a dashboard nudge (`vcs.py:status`) | — |
| `verify-access` | Anonymous stdlib probes of the live site asserted against `kb.yml` (`verify.py`) | — |
| `playbook <name>` | Prints version-matched package-data procedure | — |

Graph-relevant internals: `links.py` is the single link-model implementation — a Markdown
link/image regex, `kb://` parser, fragment splitter, and the source-path→URL mapping — shared by
three consumers so they cannot drift: `validators.check_links` (target existence, docs-escape,
public→private warnings), `validators.check_index_reachability` (BFS over intra-KB links from
`index.md`; unreached pages are errors), and `preprocess.py` (rewrites for the SSG). `nav.py`
expands curated-plus-glob nav and computes coverage. This is a complete, tested link-graph
extractor for exactly the corpus format Pinakes would ingest — worth reading before writing
Pinakes' own Markdown edge extractor.

## The design decisions, through a Pinakes lens

The full D1–D18 record is private (`docs/private/`, not consulted); the decisions are however
cited inline throughout `docs/architecture.md` and the blueprint `CLAUDE.md`, enough to
reconstruct the ones that matter here:

- **D5 — direct-to-main + deploy gate, no PRs.** Agents commit straight to main; correctness comes
  from re-running every validator in CI before deploy, plus rebase-retry push and a union-merged
  log for concurrency. A red commit lands in history but never ships.
- **D6 — no stored dates; git is the metadata source.** Timestamps are *derived* (injected at
  build from `git log`), never authored. Mild contrast with Pinakes, whose sidecars *store*
  provenance — ClaudeKB's stance is "derive what git already knows"; Pinakes should keep derivable
  fields out of sidecars for the same reason.
- **D7 — public/private split is structural** (a subtree), not per-page metadata.
- **D12 — link forms.** Bundle-root-absolute intra-KB; a *logical* cross-KB scheme (`kb://`)
  resolved at build time so the URL scheme can change without touching content. Note what it does
  **not** do: identity is still the *path*. The indirection protects against hosting changes, not
  renames. **Contradicts Pinakes' bet** (permanent ULIDs) — and ClaudeKB's own docs admit the
  consequence (redirect files on moves, capped by platform limits; lint sweeps for breakage).
- **D13 — backlinks deferred** even though the validator already builds the link graph; the
  research explicitly noted backlinks were "derivable nearly for free" (`docs/research/06-quartz.md`
  F6.1) and it still never got built. Deferral gravity is real.
- **D14/D15/D16 — SSG-independence, single-home toolchain, playbooks as package data.** Everything
  meaningful is own-code over plain files; the SSG is a swappable last step. Same instinct as
  Pinakes' "engine over committed files, index disposable".
- **D17 — repo as source of truth, dashboard as cache.** Platform state is recorded in `kb.yml`
  and *verified* against reality (`verify-access`), never treated as authoritative elsewhere.
- **D18 — cross-KB conventions are the public API** (blueprint `CLAUDE.md`): the URL scheme,
  `kb://` resolution, and `kb.yml` format change only with a MAJOR release plus migration. Mirrors
  Pinakes' fixed-naming table (`pnk://`, sidecar suffix) — the owner has twice arrived at
  "cross-KB addressing is the contract you must never casually break".
- **Explicitly opposite bet: migrations.** ClaudeKB ships upgrade machinery (copier `_migrations`,
  content-migration playbooks, a CI upgrade test per release) as a core feature; Pinakes'
  invariant is "never write a migration" (schema bump → rebuild). Both are coherent — ClaudeKB
  migrates *committed content conventions* across a fleet, Pinakes' derived state is disposable —
  but the day a *sidecar* schema changes, Pinakes meets exactly the problem ClaudeKB built
  machinery for, with none. Worth stating in Pinakes' docs as a known accepted edge.

## What ClaudeKB's own research concluded (docs/research/, docs/concepts/)

Eleven research docs plus a synthesis (`docs/research/SYNTHESIS.md`) survey ~18 tools; those
bearing on retrieval/graph (mechanisms only; nothing personal in these files):

- **llm-wiki pattern** (`03-llm-wiki-pattern.md`): the adopted operating model — raw sources /
  wiki / schema layers; ingest–query–lint operations; "queries compound into content". F3.5
  decided **standard path links over wikilinks** because "our writers are agents that handle
  paths fine" — direct support for expecting agents to write `pnk://` ULID links, tool-assisted.
- **Open Knowledge Format** (`02-open-knowledge-format.md`): frontmatter is a deliberate OKF
  superset for agent-ecosystem interop; unknown frontmatter keys must be preserved (F2.1) —
  exactly the hook a later retrieval layer (or Pinakes) can use to add metadata without breaking
  anything. F2.2's "strict producer, permissive consumer" split fits Pinakes' ingester too.
- **Quartz** (`06-quartz.md`): backlinks/previews/graph-view define the personal-KB reader bar
  (F6.1); backlinks judged trivially derivable from the already-built link graph. F6.3: nothing in
  the digital-garden world handles schemas, gates, fleets, or agent workflows — the same
  competitive gap Pinakes occupies on the retrieval side.
- **Basic Memory** (`09-basic-memory.md`) — the direct study of the *future retrieval layer*:
  **F9.1** validates "MCP layer over plain Markdown, no export step, added later without changing
  content" as a product pattern; **F9.2** prescribes the tool taxonomy — separate read / search /
  context-build tools, "not one mega-search" — and floats reusing an existing tool over building;
  **F9.3** warns against importing a conversational micro-note format into curated long-form KBs.
- **Synthesis** (`SYNTHESIS.md`): the KB-CLAUDE.md contract "does more for write consistency than
  CI" (F3.1); the per-KB manifest is *designed for* future unified-search consumers (F8.1), and
  spec §5.3 promises them exactly two files — `kb.yml` and `.copier-answers.yml` — nothing else.

Alignment with Pinakes' GRAPH_RAG conclusions (the literature review, now under
[`../../kb-kg/literature/`](../../kb-kg/literature/)): strong on "plain files + derived layers",
"free structural signal first", "semantic passes are scheduled maintenance, not query-time"; the one
place ClaudeKB's research points elsewhere is F9.2's "evaluate reuse (Basic Memory) before
building" — Pinakes *is* the build decision, defensible via F9.3 (workload mismatch: Basic Memory
targets conversational memory capture, not ranked retrieval with confidence over curated corpora).

## ClaudeKB vs Pinakes, dimension by dimension

| Dimension | ClaudeKB | Pinakes |
|---|---|---|
| Source of truth | Markdown + frontmatter in git, per-KB repo | Source docs + `.pnk.yaml` sidecars in git |
| Index | None (SSG `search.json` for humans only) | SQLite (`.pinakes/index.db`), disposable, rebuilt free |
| Retrieval | Agent navigation from a curated index + grep | BM25 + local embeddings + RRF + rerank + confidence |
| Linking/graph | Untyped Markdown links; reachability + nav enforced; `kb://` cross-KB | Typed sidecar links (`rel: cites`), `pnk://` ULIDs; free structural edges planned |
| Link stability | Path-based — a rename breaks inbound links (redirects `_redirects` for URL moves) | ULIDs permanent by invariant; paths can churn |
| Multi-hop | Agent follows links across reads | Caller's agent composes `pinakes_*` tools |
| Cost model | Free infra (Cloudflare free tier); "cost" is agent tokens per read/write session | Free path sacred; paid only in explicit `pnk ask --deep` |
| Portability | Very high — any SSG, any Markdown consumer; SSG-independent by design | High for content; index/rerank need Python + models |
| Agent role | The engine: writes, curates, retrieves, maintains | A client: calls tools; engine ranks and abstains |
| Publishing | First-class: build → deploy → Access gating, public subtree | Out of scope (engine only, repo public but KBs private) |
| Consistency enforcement | Deploy gate re-runs all validators in CI | Local checks; index rebuild tolerant |

(Pinakes column as of July. "Free structural edges planned" has since shipped as the graph release;
see [Where it landed](#where-it-landed-in-pinakes).)

The deepest difference: **where recall lives**. ClaudeKB buys recall structurally at *write* time
(nothing may exist unlinked, vocab is controlled, the index page is curated every session) and
spends agent tokens at *read* time. Pinakes buys recall computationally at read time (lexical +
semantic + rerank) and lets write-time metadata be sparse. ClaudeKB's retrieval degrades with
corpus size and agent context limits; Pinakes' degrades with index staleness and model quality.

## What ClaudeKB does better or more simply

- **Zero-infrastructure retrieval at small scale.** For a few dozen pages, "read the curated index,
  follow links" is genuinely competitive with hybrid search — no models, no index, no schema
  version, nothing to rebuild. Pinakes should stay honest that its machinery pays off only past
  the corpus size where an agent can no longer hold the catalog in context.
- **Anti-rot is enforced, not hoped for.** Orphan pages and unnavigable content are *build
  failures*. Pinakes currently has no equivalent pressure: a doc with an empty sidecar and no links
  indexes fine and just ranks poorly. A `pnk check`-style structural gate (unlinked doc, unused
  tag, dangling `pnk://` target) is cheap and proven valuable here.
- **The write path is fully specified.** Ingest playbook + session ritual + append-only log gives
  every agent session the same shape and makes parallel sessions merge-safe (union-merge log,
  rebase-retry push). Pinakes specifies the engine precisely but the *authoring* workflow much less.
- **Secret scanning sits in the gate**, severity keyed to visibility, with a per-line allow marker
  — directly liftable into Pinakes for any KB that might ever be published.
- **Ownership boundary machinery** (vendored wheel, checksums, copier update) solves fleet-wide
  upgrades — a problem Pinakes sidesteps by being one installed package, but will meet if manifest
  or sidecar schemas ever evolve across many KBs (Pinakes' "no migrations" invariant is the
  opposite bet; ClaudeKB shows what the migration-machinery path costs).
- **Publishing and access control exist at all** — Pinakes has no story for sharing a KB.

## The deferred retrieval layer — and whether Pinakes is it

**What ClaudeKB envisioned.** The architecture spec's non-goals (§1) and the roadmap defer three
retrieval extensions, "designed for, not built": (1) **unified cross-KB search** — "an aggregator
that reads each KB's `kb.yml` and merges per-KB search indexes"; (2) an **MCP/RAG retrieval
layer** over the Markdown — with an explicit instruction to "evaluate reusing an existing
local-first tool (e.g. Basic Memory) before building" (F9.2); (3) a **backlinks emitter** from
the validator's link graph. The stated constraints, assembled from the docs: it must sit *over*
plain Markdown with no export step and no content changes (F9.1); it may rely on OKF-conformant
frontmatter for typed metadata "for free" (F9.1); fleet discovery goes through each repo's
`kb.yml` and `.copier-answers.yml` — the only two files promised to consumers (spec §5.3); per-KB
independence must survive (no shared runtime); and the tool surface should separate read / search /
context-build rather than one mega-search (F9.2). Nothing about ranking, confidence, or cost was
ever specified — the layer was deferred before those questions were reached.

**Does Pinakes fit that spec?** Point by point, against a locally checked-out fleet of KB repos:

| ClaudeKB expectation | Pinakes today | Gap / adapter |
|---|---|---|
| Layer over plain Markdown, no export, content unchanged | Indexes source docs in place; `.pinakes/` derived and disposable | Sidecar files are *new committed files* — see blocker 1 |
| Typed metadata from frontmatter | Sidecars carry tags/provenance; frontmatter not currently the source | Adapter: ingest `type`/`title`/`description`/`tags` from frontmatter into generated sidecars |
| Fleet discovery via `kb.yml` | `pinakes_list_kbs` over configured KB roots | Adapter: a fleet config mapping checkout paths, seeded by reading each `kb.yml` |
| Separate read/search/context tools | `pinakes_search` / `pinakes_get` / planned `pinakes_links` — matches F9.2's taxonomy exactly | None — this is the shape ClaudeKB's own research prescribed |
| Per-KB independence | One index per KB, cross-KB only via `pnk://` links | None |
| Backlinks emitter | `pinakes_links` + authored/structural edges answers it strictly better | None |
| Local-first, no platform API | Fully local, free path sacred | None |

(Pinakes column as of July. `pinakes_links` has since shipped, in 0.5.0.)

**Concrete mapping of the data model:**

- **Markdown + frontmatter → docs/ + sidecars.** Frontmatter carries enough to *generate* a
  sidecar mechanically: `tags` (already curated against `vocab.yml`), `type`→ a tag or typed
  field, title/description → search metadata, git → provenance. What frontmatter cannot supply is
  the **ULID** — identity must be minted at adoption time and *persisted in the KB repo*, because
  Pinakes' invariant makes ULIDs permanent while the index is disposable; an index-only ULID would
  be regenerated on rebuild and break every inbound `pnk://` link. Two legal homes: a generated
  `<file>.pnk.yaml` sidecar (invisible to every kbtool validator — they all glob `*.md` only:
  `kb.py:content_markdown_files`, `check_nav`, `check_index_reachability`), or a `pnk_ulid`
  frontmatter key (explicitly legal: unknown keys are allowed and preserved, spec §5.1 / OKF
  F2.1). Either way the adapter must commit and push — through `kbtool push`, respecting the gate.
- **`kb://` path links → `pnk://` ULID links.** Fully translatable *at index time*: the very thing
  ClaudeKB cannot do at per-KB build time (cross-KB targets unresolvable, spec §5.2) a fleet-wide
  indexer does trivially, since it has all checkouts: `kb://<name>/<path>.md` → look up `<name>`
  in the fleet registry → resolve `<path>` in that checkout → that doc's ULID. Store the edge by
  ULID; the source file keeps its `kb://` form untouched. Renames then break ClaudeKB's *build*
  resolution but not Pinakes' graph — the edge re-resolves or survives via the sidecar ULID.
  Dangling targets are warnings, matching OKF's tolerate-broken-links consumer stance (F2.2).
- **`vocab.yml` → shared-tag edges.** The controlled vocabulary is exactly the precondition
  Pinakes' shared-tag edge needs to avoid noise cliques; a ClaudeKB fleet arrives pre-curated.
- **The enforced link graph → PPR channel.** `kbtool`'s gate guarantees a connected graph rooted
  at `index.md` — so authored-link edges exist *in every ClaudeKB KB by construction*, unusually
  dense for a real-world corpus, and `index.md`'s out-edges give a natural, human-curated
  teleport prior for Personalized PageRank. ClaudeKB is arguably the *best-case* corpus for
  Pinakes' planned graph channel.

**Blockers (real but small):**

1. **Write-back ceremony.** First adoption must mint ULIDs and commit ~one sidecar per page into
   each KB repo. Legal under the ownership rule (paths absent from the template are KB-owned,
   spec §4) and invisible to the gate, but it is a new bot-write path and needs the session ritual
   treatment (check → commit → push).
2. **Sidecars deploy.** `docs/` is copied wholesale into the site build (`preprocess.py` step 1);
   on a public-*site* KB, `.pnk.yaml` files under `docs/` would ship as world-readable static
   files — a structure leak, not a content leak. Adapter: extend the KB's ignore handling, or
   keep sidecars out of `docs/` (Pinakes-side layout option), or accept it for private sites.
3. **Two metadata homes.** Frontmatter stays authoritative in ClaudeKB KBs (its gate validates
   it); generated sidecars must be derived-except-ULID and refreshed at index time, never
   hand-divergent. A one-way sync rule, stated once, closes this.
4. **No manifest.** Each KB needs a `pinakes.toml` (or a fleet-level registry outside the repos
   pointing at checkouts + `kb.yml`s). Trivial.

**Answer: yes — Pinakes is a credible, near-drop-in implementation of ClaudeKB's deferred layer.**
Nothing in the ClaudeKB blueprint needs to change; every input Pinakes wants is already present
(OKF frontmatter, curated vocab, an enforced link graph, a per-KB manifest) or mechanically
generatable, and the MCP tool taxonomy Pinakes already chose is the one ClaudeKB's research
prescribed. The one principled tension is F9.2's "reuse before build" — answered by F9.3's own
workload-mismatch finding plus everything Basic Memory lacks that Pinakes defines itself by:
ranked hybrid retrieval, calibrated confidence/abstention, and a sacred free path. The cheap
proof-of-fit would be a `pnk adopt` pass over a scaffolded demo KB: generate sidecars from
frontmatter, resolve `kb://` links to ULID edges, index, and measure the graph channel against
the golden set.

*Status of this answer on 20261030:* a July judgement, never tested. `pnk adopt` was not built, no
proof-of-fit run exists in the documents read, and the "OKF-conformant frontmatter" premise is weaker
against v0.2 (see the OKF section above: `okf_version` and `status` do not line up).

## What its experience teaches Pinakes' graph plans

1. **Humans don't author rich links; agents under a gate do author minimal ones.** ClaudeKB gets
   real links written only because a validator *fails the build* without them — and even then it
   demands only reachability, the weakest useful property. Untyped "reachable-from-index" links
   were achievable; nobody built backlinks or typed edges even with the link graph already parsed
   in the validator. Lesson: Pinakes' plan to lean on **free structural edges** (headings,
   co-location, shared tags) rather than hand-authored `links:` entries is the right default;
   treat authored typed links as sparse, precious signal, and consider a check that *nudges*
   (warn on zero-link docs) rather than assuming density.
2. **Agent-driven navigation over plain files works — at fleet-of-small-KBs scale, and because
   the entry point is curated.** The session ritual's "read index.md first" is a hand-maintained
   PageRank prior. It breaks down on: (a) corpus size (the catalog outgrows context; grep replaces
   navigation and precision collapses), (b) cross-KB queries (deliberately unresolvable at
   validation time; unified search deferred), (c) anything needing *ranking* — navigation finds a
   page or doesn't; there is no confidence, no top-k, no abstention. These three failure modes are
   exactly Pinakes' reason to exist; the comparison confirms the niche rather than undermining it.
3. **Path-based identity is ClaudeKB's structural weakness and Pinakes' strongest call.** `kb://`
   links break on file moves (redirect files patch the URL side only, capped by platform limits);
   `pnk://` ULIDs make the graph rename-proof. Any Pinakes graph channel (PPR over edges) inherits
   this robustness for free — edges over ULIDs survive refactors that would sever ClaudeKB's graph.
4. **Curated vocabulary beats folksonomy for the shared-tag edge.** ClaudeKB validates every tag
   against `vocab.yml` precisely to stop tag sprawl. If Pinakes builds shared-tag edges, uncurated
   tags will produce dense noise cliques; a per-KB controlled vocabulary (or an edge-weight
   penalty on high-degree tags) is the proven countermeasure.
5. **Lazy semantic work as a scheduled agent pass is viable.** The `lint` playbook (agent hunts
   contradictions and missing cross-references monthly) is precedent for Pinakes' "lazy LLM
   extraction written back to sidecars": batch, explicit, results persisted in git — not
   per-query magic. It also confirms such passes are a *maintenance* cost model, safely outside
   the free path.
6. **Enforce graph invariants at write time, verify at read time.** ClaudeKB's split — structural
   validators in the gate, semantic sweeps scheduled — maps cleanly onto Pinakes: cheap checks
   (dangling `pnk://`, orphan docs) belong in an indexing-time gate; expensive graph maintenance
   belongs in explicit commands, never inside `pnk search`.
7. **Make linking a precondition of writing, not a virtue** (second-pass, from the ingest
   playbook). ClaudeKB's ingest steps 3–4 mean a write *cannot land* without attaching the new
   node to the graph and the nav. If Pinakes ever ships an authoring/ingest workflow (or a
   `CLAUDE.md` contract for KBs it indexes), the single highest-leverage rule to copy is "link it
   from the catalog or an already-reachable page, or the gate fails" — that one obligation is what
   made ClaudeKB's corpus a usable graph.
8. **"Derivable nearly for free" still never ships without a consumer** (second-pass, D13 +
   F6.1). Backlinks were identified as trivially derivable from an already-built link graph, and
   were still deferred indefinitely — because nothing *consumed* them. Pinakes' structural edges
   have a consumer from day one (the retrieval fusion / PPR channel); that, not implementation
   cost, is the real difference that will make them ship. Corollary: don't build graph outputs
   (backlink lists, exports) before the consumer exists.
9. **Agents handle strict link syntax fine — with the contract stated once** (second-pass,
   F3.5/F6.2). ClaudeKB rejected wikilinks *because its writers are agents*: path bookkeeping that
   annoys humans is free for a model following a documented convention plus a validator. The same
   argument says agents will reliably author `pnk://<ulid>/<ulid>` links **if** a tool resolves
   names→ULIDs for them (`pinakes_search`/`pinakes_get` already do) and a check catches malformed
   ones. Don't design the sidecar link format down to human ergonomics.

## Key sources of the July investigation

Paths are relative to the root of the ClaudeKB repository, as read on 20260725 and 20260726. Browse
them at https://github.com/lucagattoni/ClaudeKB/blob/main/ followed by the path.

- README.md
- docs/architecture.md (spec, D1–D18, iteration log)
- docs/guide/what-is-claudekb.md
- docs/guide/using-a-kb.md
- docs/guide/public-and-private-kbs.md
- docs/guide/roadmap.md
- template/CLAUDE.md (the agent contract)
- CLAUDE.md (blueprint repo rules, D18)
- src/kbtool/{cli,validators,links,secrets,preprocess,vcs,kb,nav,verify,build}.py
- src/kbtool/data/playbooks/{ingest,lint,upgrade,access-dns-setup}.md
- playbooks/scaffold-kb.md
- docs/research/{SYNTHESIS,02-open-knowledge-format,03-llm-wiki-pattern,06-quartz,09-basic-memory}.md
- docs/concepts/leaky.md (secret-scan fixture)
- CHANGELOG.md (v0.1.0–v0.4.0)

*(ClaudeKB's private decision record — `docs/private/` — was not consulted for this document; the
public architecture spec and guides cover everything cited. Deployed-instance hostnames use the
repo's own `example.com` parameterization; no real domains appear here.)*

---

## Sources for the 20261030 sections

All read 20261030, times UTC. "API" means the GitHub REST API called with the `gh` client.

| # | Source | Read | What was taken |
|---|---|---|---|
| S1 | https://github.com/lucagattoni/ClaudeKB (API `repos/…/ClaudeKB`, branches, issues; the old URL answers a 301 redirect) | 20261030 18:58 UTC | visibility, `pushed_at`, `created_at`, archived flag, stars, forks, licence field, one branch, no issues, new canonical owner |
| S2 | https://github.com/lucagattoni/ClaudeKB/releases (API `releases`, `tags`) | 20261030 18:58 UTC | six releases and tags, publish times |
| S3 | https://github.com/lucagattoni/ClaudeKB/commits/main (API `commits?since=2026-08-01T00:00:00Z`, and the five newest) | 20261030 18:58 UTC | empty list since 20260801; head commit `1f5694e` at 20260712 17:20:22 UTC |
| S4 | https://github.com/lucagattoni/ClaudeKB/blob/main/LICENSE | 20261030 18:58 UTC | MIT License, copyright 2026 |
| S5 | https://github.com/lucagattoni/ClaudeKB/blob/main/docs/guide/roadmap.md | 20261030 18:58 UTC | Done, Next, Deferred and "Future extensions (designed for, not built)" |
| S6 | https://github.com/lucagattoni/ClaudeKB/tree/main/src/kbtool (shallow clone at `1f5694e`), including `validators.py`, `cli.py`, `kb.py`, `data/frontmatter.schema.json` | 20261030 18:58 to 18:59 UTC | line count 1,157 over 11 modules; nine validators in `run_all`; eight subcommands; no `mcp` or `backlink` in `src/`; reserved-file rule; schema |
| S7 | https://github.com/lucagattoni/ClaudeKB/blob/main/docs/architecture.md | 20261030 18:59 UTC | iteration log passes 0 to 10; §5.1 frontmatter rules |
| S8 | https://github.com/lucagattoni/ClaudeKB/blob/main/CHANGELOG.md | 20261030 18:58 UTC | 0.3.0 and 0.4.0 entries; "moved out of the tracked tree" |
| S9 | https://github.com/lucagattoni/ClaudeKB/blob/main/docs/research/02-open-knowledge-format.md | 20261030 18:59 UTC | analysed OKF v0.1 on 20260712; findings F2.1 to F2.5 |
| S10 | https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md | 20261030 18:59 UTC | OKF v0.2 text: §3.1, §4.1, §5.4, §6, §8, §11, §12, §13 |
| S11 | https://github.com/GoogleCloudPlatform/open-knowledge-format (API metadata, README, CONTRIBUTING.md, LICENSE.md, commits) | 20261030 18:59 UTC | created 20260811; Apache-2.0; 1,177 stars; contribution rules; 20260820 and 20260821 commits |
| S12 | https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf (README banner; API commits for path `okf`) | 20261030 18:59 UTC | frozen-snapshot banner; v0.2 migration commit 20260724 16:45 UTC; 20260821 commits |
| S13 | https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/ | 20261030 19:00 UTC | announcement date 20260612, team byline, wording, no governance statement (read through the fetch tool's summary, not the raw page) |
| S14 | https://github.com/W4G1/okf (API metadata and README) | 20261030 19:00 UTC | v0.2 claim; Apache-2.0; dates; stars |
| S15 | https://github.com/bushans/okfgen (API metadata and README) | 20261030 19:00 UTC | v0.2 claim; Apache-2.0; dates; stars |
| S16 | https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md | 20261030 19:00 to 19:04 UTC | command and capability tables, unbuilt-work table, measured numbers; header "Latest release: 0.32.8, last reviewed 20261029 18:57"; the public file's first lines were also read through the API at 19:02 and match |
| S17 | https://github.com/lucagattoni/pinakes/blob/main/docs/ROADMAP.md | 20261030 19:00 to 19:04 UTC | timestamp note; entries 0.5.0, 0.6.0; "Where things stand" |
| S18 | https://github.com/lucagattoni/pinakes/blob/main/docs/CLI.md (`pnk doctor`) | 20261030 19:02 UTC | what `doctor` checks and what `--prune` changes; the sidecar holds the permanent ULID |
| S19 | https://github.com/lucagattoni/pinakes/blob/main/docs/DESIGN.md | 20261030 19:03 UTC | why sidecars rather than in-text links; the stated cost |
| S20 | https://github.com/lucagattoni/pinakes/blob/main/docs/README.md and https://github.com/lucagattoni/pinakes/blob/main/CHANGELOG.md (0.32.0 entry) | 20261030 19:01 UTC | `pnk adopt` unimplemented, owner release unanswered; the `grep` result recorded there |
| S21 | https://github.com/lucagattoni/pinakes/releases (API `releases/latest`) | 20261030 19:02 UTC | v0.32.8 published 20261029 18:53 UTC |
| S22 | The Pinakes approach document, sections 8 and 10 (now [`../approach/PINAKES_APPROACH.md`](../approach/PINAKES_APPROACH.md)), including the note added 20260825 | 20261030 19:02 UTC | the proposal of `pnk adopt`; "hand-adopted ClaudeKB corpus as second KB"; the template release closed at 0.22.0 without it |
