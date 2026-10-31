# Knowledge bases and knowledge graphs: a reference

How the ideas of *knowledge base* (KB) and *knowledge graph* (KG) have evolved, what the state of
the art is, and which directions are being tried, with a focus on using LLMs and agents to build and
query them.

**Status:** work in progress, started 20261030 18:53 UTC. Nothing here is final until its section
says so. [`RESUME.md`](RESUME.md) holds the current state; [`DECISIONS.md`](DECISIONS.md) holds what was
decided and why.

## Two sections, kept apart

| Section | What it holds | Rule |
|---|---|---|
| [`kb-kg/`](kb-kg/README.md) | The field-neutral reference: a short pre-LLM primer, the LLM era, a dated landscape of projects, papers and benchmarks, the directions being tried, and experiments worth running. | Nothing in it depends on any one project's needs. |
| [`pinakes/`](pinakes/README.md) | Development notes for [Pinakes](https://github.com/lucagattoni/pinakes): what it took from the field, what it tests, what it should test next. | Everything here points *into* `kb-kg/` for the facts about other projects. |

## Conventions

- **Every timestamp is UTC**, written `YYYYMMDD HH:MM`. A figure without a date is not a figure.
- **Every statement about a project cites a source and the time it was read.** Where the source is
  silent the entry says **unstated**; it is never filled with a plausible default.
- **Stars are a signal, not a verdict.** Rankings use stars among repositories pushed in the last 90
  days, and growth that looks inorganic is flagged, not hidden.
- **Licences are read from the `LICENSE` file**, not the README badge. A project whose licence
  forbids copying its code is a read-only reference; ideas and measured results are free to reuse,
  source is not.
- **New dated files** carry a `YYYYMMDD_HHMM-` prefix.

## Layout

```
kb-kg/
  primer/              pre-LLM lineage of KBs and KGs
  llm-era/             the LLM era: timeline and the shifts in approach
  literature/          what the research literature says
  projects/            one entry per project (deep dive or short card)
  landscape/           dated GitHub snapshots, produced by tools/gh_snapshot.py
  papers-benchmarks/   papers, surveys, benchmarks and datasets
  directions/          what the field is trying, grouped by direction
  experiments/         what to test next, each with its cost stated first
pinakes/
  takeaways/           per project: what Pinakes took and left
  approach/            the Pinakes graph approach (design decision layer)
  precedent/           earlier in-house work
  experiments/         what Pinakes tests, and what it measured
tools/                 snapshot, projects-index and snapshot-description scripts, and the public-safety gate
```

## Licence

Apache-2.0 for the text and the code. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE): quoted third-party text and data fetched from other services keep their own terms.
