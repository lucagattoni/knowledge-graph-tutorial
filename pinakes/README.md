# Pinakes development notes

[Pinakes](https://github.com/lucagattoni/pinakes) is a portable, agent-first knowledge base: one
directory is one KB, your documents are the source of truth, and the search index is derived and
disposable. This section records how the field's work informs it. The facts about other projects live
in [`../kb-kg/`](../kb-kg/README.md); this section links to them.

The authoritative statement of what Pinakes *has built* is its own
[`STATUS.md`](https://github.com/lucagattoni/pinakes/blob/main/docs/STATUS.md). Everything here that
disagrees with it is out of date.

| Part | What it holds | State |
|---|---|---|
| [`approach/`](approach/) | The Pinakes graph approach: lazy, agent-driven, budget-tunable. The design decision layer, moved from Pinakes' `docs/graph/`. | in progress |
| [`recommendations-r1-r7.md`](recommendations-r1-r7.md) | The seven recommendations drawn from the literature review. | in progress |
| [`takeaways/`](takeaways/) | Per project: what Pinakes took, what it left, and the licence gate. | in progress |
| [`precedent/`](precedent/) | Earlier in-house work that Pinakes follows. | in progress |
| [`experiments/`](experiments/) | What Pinakes has measured and what it should measure next. | not started |

## Licence gate

Some projects the research read are not safe to copy from. Pinakes is Apache-2.0 and its server is a
network service, so a copyleft or non-commercial licence would reach anyone embedding it.
**Ideas and measured results are free to reuse; source code is not.** The entries under
[`takeaways/`](takeaways/) mark each project accordingly.
