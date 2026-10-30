---
slug: <slug>
repo: <owner/name>
tier: deep            # deep | card
category: core        # core | agent-memory | markdown-kb | adjacent
snapshot: YYYYMMDD HH:MM UTC
---

# <Project name>

<!--
Rules for every entry:
- Neutral. No "what X should take from this": that goes in pinakes/takeaways/.
- Every factual statement carries a [n] citation to the Sources list. If the sources are silent, write
  "unstated". Never fill a gap with a plausible default.
- Dates are UTC: YYYYMMDD HH:MM. Star counts and push dates carry the snapshot time.
- Licence comes from the LICENSE file. If the README badge disagrees, say so.
- No local paths, no private repository names, no personal addresses.
- tier: card keeps only the header table and these four sections, in this order: "What it is", "How it
  works" (at most 120 words), "Status and direction" (at most 80 words), "Sources". About 400 to 700
  words in all. Omit the other sections.
- tier: deep for an entry that did not begin as one of the July 2026 investigations omits
  "Changed since the July 2026 investigation". It may add "Recent changes" (the last 90 days) after
  "Direction".
-->

| | |
|---|---|
| Repository | <URL> |
| Licence | <SPDX id from the LICENSE file> |
| Language | |
| Stars, forks | <n>, <n> (snapshot) |
| Created, last push | <date>, <date> |
| Latest release | <tag, date> or none |
| Status | active (pushed within 90 days) / quiet / archived |
| Paper, docs | <links> |

## What it is

Three to five neutral sentences.

## How it works

Indexing, the graph or data model, retrieval, where an LLM is used at index time and at query time,
and how an agent talks to it (MCP, tools, SDK).

## Cost and operating profile

What it spends (LLM calls at index time, per query), what it needs (database, GPU, API keys), and
whether it can run entirely locally.

## Evidence

Published results, benchmarks and third-party evaluations, each with its source. "None published" is a
valid answer.

## Direction

Where it is heading, from its own roadmap, releases and recent commits.

## Changed since the July 2026 investigation

Deep entries that began as one of the July 2026 investigations only. Dated bullets; "no change found
(checked <date>)" is a valid answer.

## Sources

1. <URL>: what it supports (read YYYYMMDD HH:MM UTC)
