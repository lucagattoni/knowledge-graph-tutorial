---
slug: open-knowledge-format
repo: GoogleCloudPlatform/open-knowledge-format
tier: card
category: markdown-kb
snapshot: 20261030 19:40 UTC
---

# Open Knowledge Format (OKF)

| | |
|---|---|
| Repository | https://github.com/GoogleCloudPlatform/open-knowledge-format [1] |
| Licence | Apache-2.0, from `LICENSE.md` (Apache License 2.0 text; head and tail read) [2]. The API field agrees [1]; the README states no licence [3]. |
| Language | A specification in Markdown. GitHub's primary language is HTML (bundled viewer pages); the reference agent is Python [1][3] |
| Stars, forks | 1,177, 85 (20261030 19:40 UTC). The repository is not in the landscape snapshot of 20261030 19:13 UTC [1] |
| Created, last push | 20260811 18:29 UTC, 20260821 20:08 UTC [1] |
| Latest release | none: no releases or tags. The version is declared in the document: 0.2 [1][5] |
| Status | active by the 90-day rule (70 days since the last push); not archived [1] |
| Paper, docs | `SPEC.md`; announcement post on the Google Cloud blog, 20260612 [4][5] |

## What it is

A specification, not software. It defines a "bundle": a directory of Markdown files with YAML frontmatter that describes the knowledge around data and systems, meant to be written by people or agents and read by either [5]. The text says it has "no schema registry, no central authority, and no required tooling", and that it does not fix a taxonomy of types or prescribe storage and serving [5]. The same repository holds a Python reference agent (it writes bundles from BigQuery metadata and web pages with Gemini), a viewer and four sample bundles, which the README calls proofs of concept: "the format itself is the contribution" [3]. A third-party page notes this OKF is not the Open Knowledge Foundation, which shares the initials [7].

## How it works

A bundle is a directory; a file's path without `.md` is its concept ID [5]. Each file opens with YAML frontmatter; `type` is the only required key, `title`, `description`, `resource` and `tags` are recommended, and unknown keys must be tolerated [5]. `index.md` (a listing, with no frontmatter except `okf_version` at the root) and `log.md` (dated history) are reserved [5]. Links are ordinary Markdown links; their meaning sits in the prose around them [5]. v0.1 (a draft, announced June 2026) had a `timestamp` key and a `# Citations` list [4][9]. v0.2 replaces them with `generated` and a `sources` list, and adds `verified` (three trust tiers), `status`, `stale_after` and an Attested Computation type [5].

## Status and direction

Google Cloud publishes it [1][4]. No standards body or foundation is named in the README, spec, contribution guide or announcement [3][4][5][6]; a third-party page of 20260826 agrees [7]. Spec changes need an issue first and a Google CLA [6]. Six commits, one account; the v0.2 text changed on 20260820 with no version bump [1][10]. 43 open items; none of 105 comments since the last push is from an owner, member or collaborator [1][8]. Direction: unstated.

## Sources

1. https://github.com/GoogleCloudPlatform/open-knowledge-format : repository metadata, releases, tags, commits, contributors via the GitHub API (read 20261030 19:40 to 19:46 UTC)
2. https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/LICENSE.md : Apache License 2.0 text (read 20261030 19:40 to 19:46 UTC)
3. https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/README.md : scope statement, reference agent, samples (read 20261030 19:40 to 19:46 UTC)
4. https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/ : announcement of 20260612, read through the fetch tool's summary, not the raw page (read 20261030 19:40 to 19:46 UTC)
5. https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md : v0.2 text, sections 1 to 13 (read 20261030 19:40 to 19:46 UTC)
6. https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/CONTRIBUTING.md : contribution rules and CLA (read 20261030 19:40 to 19:46 UTC)
7. https://ppc.land/okf/ : third-party article dated 20260826 on governance, read through the fetch tool's summary (read 20261030 19:40 to 19:46 UTC)
8. https://github.com/GoogleCloudPlatform/open-knowledge-format/issues : issues, pull requests and 105 comments with author roles via the GitHub API (read 20261030 19:40 to 19:46 UTC)
9. https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/09f3301/okf/SPEC.md : the v0.1 draft, read to section 8; the `okf/` directory carries a banner calling itself a frozen snapshot, and its `SPEC.md` is identical to source 5 (read 20261030 19:40 to 19:46 UTC)
10. https://github.com/GoogleCloudPlatform/open-knowledge-format/issues/24 : issue on the unversioned timestamp change; commit 3dc3029 (read 20261030 19:40 to 19:46 UTC)
