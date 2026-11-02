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
| [`approach/`](approach/) | The Pinakes graph approach: lazy, agent-driven, budget-tunable. The design decision layer, moved from Pinakes' `docs/graph/`. | moved; status block added 20261030 |
| [`recommendations-r1-r7.md`](recommendations-r1-r7.md) | The seven recommendations drawn from the literature review. | moved; status per recommendation added 20261030 |
| [`takeaways/`](takeaways/) | Per project: what Pinakes took, what it left, and the licence gate. | 12 entries |
| [`precedent/`](precedent/) | Earlier in-house work that Pinakes follows. | ClaudeKB moved and updated |
| [`experiments/`](experiments/) | What Pinakes has measured and what it should measure next. | measured results written; [four proposals](experiments/next.md) for what to measure next: P1 answered, the [P4 pilot](experiments/p4-deep-pilot.md) run, P2 blocked, P3's free-path half in the public [benchmark repository](experiments/datasets-benchmark.md) |

## Licence gate

Some projects the research read are not safe to copy from. Pinakes is Apache-2.0 and its server is a
network service, so a copyleft or non-commercial licence would reach anyone embedding it.
**Ideas and measured results are free to reuse; source code is not.** The entries under
[`takeaways/`](takeaways/) mark each project accordingly.
