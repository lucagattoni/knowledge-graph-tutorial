"""Free pre-flight for a pass-B stage (plan item F4): expected tokens times price, against the stage's limits and the ledger.

Run before each paid stage, and again before each run of a stage:

    python passb_preflight.py --stage B --builders lightrag,fast --ledger-dir DIR [--stage-spent X] [--multiplier 2]

It prints a small table (expected tokens, prices, the estimate, the stage limit and "stop at", what the ledger shows spent,
the cap to put in the gateway config) and exits 1 when the estimate does not fit, 0 when it does, 2 on a usage error
(bad numbers, a ledger directory that does not exist, a stage spend larger than the ledger total).

Where the numbers come from (kb-kg/experiments/x2-index-cost/pass-b-plan.md, written 20261102, and the pass-A results):

* Prices: `gpt-6-luna`, USD per million tokens, input 0.10 and output 0.50, read 20261102 20:20 UTC from OpenAI's pricing
  page. They are parameters; the run script's real config wins over these defaults.
* Total cap USD 3.00 (the owner's choice, 20261102 20:49 UTC, "gpt-6-luna, USD 3"). Stage limits A 0.10, B 0.20, C 0.60,
  D 1.50 (the plan's proposal, with the cap).
* Central token estimates, (input, output) for ONE run of the stage, per builder, from pass A's measured tokens
  (`granite4.2:8b`'s tokenizer, scaled by characters for C and D; the plan's "What it costs" section). A hosted model's
  counts differ, so these bracket the real ones and do not equal them.
* "Stop at" = the lower of the stage limit and 3 times the stage's central estimate (all four builders, output x1, the
  plan's prices), the estimate rounded to the mill first, as the plan's table states it (B: 3 x 0.030 = 0.09). Stage A is
  the exception: its USD 0.02 is an upper bound for at most 12 calls, not a central estimate, and the plan gives it
  "stop at" 0.10 (its limit); 3 x 0.02 would be 0.06.

`allowance` is what THIS run may spend, `max(0, min(stage_limit - spent_in_stage, total_cap - spent_total))`; `cap_for_gateway`
is `spent_total + allowance`, the CUMULATIVE cap to write into the gateway config, because a gateway started with `--resume`
compares its cap with the whole log's spend (the ledger is shared by all stages).

Standard library only; Decimal throughout.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Mapping, Sequence

MILLION = Decimal(1_000_000)
PRICE_IN = Decimal("0.10")      # USD per million input tokens, gpt-6-luna, read 20261102 20:20 UTC (plan, "Facts")
PRICE_OUT = Decimal("0.50")     # USD per million output tokens, same source
TOTAL_CAP = Decimal("3.00")     # owner's choice, 20261102 20:49 UTC
STAGE_LIMITS = {"A": Decimal("0.10"), "B": Decimal("0.20"), "C": Decimal("0.60"), "D": Decimal("1.50")}  # plan, decision 2
STOP_AT_FACTOR = Decimal(3)     # plan, "Stage ... Stop at is the lower of the stage limit and 3 times the central estimate"
A_ESTIMATE = Decimal("0.02")    # plan: stage A is at most 12 calls, "at most 0.02"
RUNS_PER_STAGE = {"A": 1, "B": 1, "C": 2, "D": 1}  # plan: stage C is two independent runs
BOUND_ONLY_STAGES = frozenset({"A"})  # the estimate is an upper bound; "stop at" is the limit itself
MILL = Decimal("0.001")
BUILDER_ORDER = ("lightrag", "fast", "ms", "nano")  # decision 5's order; "fast" = fast-graphrag, "ms" = Microsoft GraphRAG
# (input_tokens, output_tokens) for one run: B = 1 document, C = 5 documents, D = 20 documents (plan, "What it costs")
CENTRAL_ESTIMATES: dict[str, dict[str, tuple[int, int]]] = {
    "B": {"lightrag": (14595, 3296), "fast": (13902, 5601), "ms": (43594, 22889), "nano": (15391, 10815)},
    "C": {"lightrag": (66543, 24290), "fast": (52264, 19457), "ms": (107005, 70204), "nano": (105288, 54750)},
    "D": {"lightrag": (401109, 135391), "fast": (331955, 124603), "ms": (631330, 414204), "nano": (421152, 218999)},
}


class UnknownInput(ValueError):
    """A stage or builder the tables do not have: a refusal for `check`, an error for the other functions."""


@dataclass(frozen=True)
class Result:
    ok: bool
    reason: str                        # "fits ..." when ok, otherwise every reason joined with "; "
    estimate: Decimal | None           # USD for this run; None when the stage or a builder is unknown
    stop_at: Decimal | None            # None when the stage is unknown
    cap_for_gateway: Decimal | None    # spent_total + allowance: the cumulative cap for the gateway config; None when the stage is unknown
    allowance: Decimal | None = None   # what THIS run may spend; None when the stage is unknown


def _number(value: Any, name: str, *, positive: bool = False) -> Decimal:
    if isinstance(value, bool):
        raise ValueError(f"{name}: {value!r} is not a number")
    try:
        out = Decimal(str(value).strip()) if not isinstance(value, Decimal) else value
    except InvalidOperation:
        raise ValueError(f"{name}: {value!r} is not a number") from None
    if not out.is_finite() or out < 0 or (positive and out == 0):
        raise ValueError(f"{name}: a {'positive' if positive else 'non-negative'} number is required, got {value!r}")
    return out


def money(value: Decimal) -> str:
    """USD for display: at most six decimals, at least two, no exponent (0.09, 0.0031075, 1.071752)."""
    text = format(value.quantize(Decimal("0.000001"), ROUND_HALF_UP), "f").rstrip("0")
    whole, _, frac = text.partition(".")
    return f"{whole}.{frac.ljust(2, '0')}"


def _known_stage(stage: str) -> None:
    if stage not in STAGE_LIMITS:
        raise UnknownInput(f"unknown stage {stage!r}; the stages are {', '.join(STAGE_LIMITS)}")


def _known(stage: str, builders: Sequence[str]) -> list[str]:
    _known_stage(stage)
    if stage in BOUND_ONLY_STAGES:
        return []
    if isinstance(builders, str) or not builders:
        raise UnknownInput(f"stage {stage}: no builders given (choose from {', '.join(BUILDER_ORDER)})")
    unknown = [b for b in builders if b not in CENTRAL_ESTIMATES[stage]]
    if unknown:
        raise UnknownInput(f"stage {stage}: unknown builder(s) {unknown!r} (choose from {', '.join(BUILDER_ORDER)})")
    if len(set(builders)) != len(builders):
        raise UnknownInput(f"stage {stage}: a builder is listed twice in {list(builders)!r}")
    return list(builders)


def run_tokens(stage: str, builders: Sequence[str], multiplier: Any = 1) -> tuple[Decimal, Decimal]:
    """(input, output) tokens expected for ONE run of the stage; the multiplier scales the output tokens only."""
    factor = _number(multiplier, "multiplier", positive=True)
    chosen = _known(stage, builders)
    tokens_in = sum((Decimal(CENTRAL_ESTIMATES[stage][b][0]) for b in chosen), Decimal(0))
    tokens_out = sum((Decimal(CENTRAL_ESTIMATES[stage][b][1]) for b in chosen), Decimal(0)) * factor
    return tokens_in, tokens_out


def run_estimate(stage: str, builders: Sequence[str], price_in: Any = PRICE_IN, price_out: Any = PRICE_OUT,
                 multiplier: Any = 1) -> Decimal:
    """USD for ONE run of the stage (stage A: the fixed USD 0.02, whatever the arguments)."""
    p_in, p_out = _number(price_in, "price_in"), _number(price_out, "price_out")
    if stage in BOUND_ONLY_STAGES:
        _number(multiplier, "multiplier", positive=True)
        return A_ESTIMATE
    tokens_in, tokens_out = run_tokens(stage, builders, multiplier)
    return (tokens_in * p_in + tokens_out * p_out) / MILLION


def estimate(stage: str, builders: Sequence[str], price_in: Any = PRICE_IN, price_out: Any = PRICE_OUT,
             multiplier: Any = 1) -> Decimal:
    """USD for the whole stage: one run times the stage's number of runs (C is two runs)."""
    one = run_estimate(stage, builders, price_in, price_out, multiplier)
    return one * RUNS_PER_STAGE[stage]


def stop_at(stage: str, price_in: Any = PRICE_IN, price_out: Any = PRICE_OUT) -> Decimal:
    """The lower of the stage limit and 3 times the stage's central estimate (all four builders, output x1)."""
    _known_stage(stage)
    limit = STAGE_LIMITS[stage]
    if stage in BOUND_ONLY_STAGES:
        return limit
    central = estimate(stage, BUILDER_ORDER, price_in, price_out, 1).quantize(MILL, ROUND_HALF_UP)
    return min(limit, STOP_AT_FACTOR * central)


def check(stage: str, builders: Sequence[str], spent_total: Any, spent_in_stage: Any, total_cap: Any = TOTAL_CAP,
          price_in: Any = PRICE_IN, price_out: Any = PRICE_OUT, multiplier: Any = 1) -> Result:
    """Does ONE run of `stage` with `builders` fit? Refuses (ok False) when the stage or a builder is unknown, when
    `spent_in_stage` plus the run's estimate passes the stage's "stop at", or when `spent_total` plus it passes the total
    cap. `multiplier` scales the output tokens (the plan's x0.5, x1 and x2 cases). The result also carries `allowance` (what
    this run may spend) and `cap_for_gateway` (spent_total + allowance, the cumulative cap for the gateway config). Numbers
    that make no sense (negative spend, a stage spend above the total, a multiplier of 0) raise ValueError."""
    total = _number(spent_total, "spent_total")
    in_stage = _number(spent_in_stage, "spent_in_stage")
    cap = _number(total_cap, "total_cap")
    if in_stage > total:
        raise ValueError(f"spent_in_stage {in_stage} is more than spent_total {total}")
    _number(price_in, "price_in"), _number(price_out, "price_out"), _number(multiplier, "multiplier", positive=True)
    try:
        run = run_estimate(stage, builders, price_in, price_out, multiplier)
        stop = stop_at(stage, price_in, price_out)
    except UnknownInput as exc:
        if stage not in STAGE_LIMITS:
            return Result(False, str(exc), None, None, None, None)
        allowance = max(Decimal(0), min(STAGE_LIMITS[stage] - in_stage, cap - total))
        return Result(False, str(exc), None, stop_at(stage, price_in, price_out), total + allowance, allowance)
    allowance = max(Decimal(0), min(STAGE_LIMITS[stage] - in_stage, cap - total))
    gateway_cap = total + allowance
    reasons = []
    if in_stage + run > stop:
        reasons.append(f"stage {stage}: USD {money(in_stage)} already spent in the stage + USD {money(run)} for this run "
                       f"= USD {money(in_stage + run)}, over its stop at USD {money(stop)}")
    if total + run > cap:
        reasons.append(f"total: USD {money(total)} already spent + USD {money(run)} for this run "
                       f"= USD {money(total + run)}, over the total cap USD {money(cap)}")
    if reasons:
        return Result(False, "; ".join(reasons), run, stop, gateway_cap, allowance)
    return Result(True, f"fits: USD {money(in_stage + run)} in the stage of a stop at USD {money(stop)}, "
                        f"USD {money(total + run)} in total of a cap of USD {money(cap)}", run, stop, gateway_cap,
                  allowance)


def ledger_spent(ledger_dir: str | Path, log_name: str = "meter.jsonl") -> tuple[Decimal, int]:
    """(sum of `cost` over the records of `LEDGER_DIR/meter.jsonl`, number of lines whose cost could not be read).
    A missing file means nothing has been spent yet. Costs are decimal strings; a JSON number is read exactly too. A line
    that is not JSON (a half-written last line included) or has no readable cost is counted, not skipped silently."""
    path = Path(ledger_dir) / log_name
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        return Decimal(0), 0
    total, unreadable = Decimal(0), 0
    for line in data.decode("utf-8", "replace").split("\n"):
        if not line.strip():
            continue
        try:
            record = json.loads(line, parse_float=Decimal)
            cost = record["cost"]
            if isinstance(cost, bool):
                raise ValueError
            value = cost if isinstance(cost, Decimal) else Decimal(str(cost).strip())
            if not value.is_finite():
                raise ValueError
        except (ValueError, KeyError, TypeError, InvalidOperation, RecursionError):
            unreadable += 1
            continue
        total += value
    return total, unreadable


def _table(rows: Sequence[tuple[str, str]]) -> str:
    width = max(len(k) for k, _ in rows)
    return "\n".join(f"  {k.ljust(width)}  {v}" for k, v in rows)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="passb_preflight.py",
        description="Print what a pass-B stage run is expected to cost and refuse (exit 1) when it does not fit; exit 2 "
                    "on a usage error.")
    p.add_argument("--stage", required=True, help="A, B, C or D")
    p.add_argument("--builders", default="", help="comma-separated: lightrag, fast, ms, nano (not needed for stage A)")
    p.add_argument("--ledger-dir", required=True, help="the gateway directory holding meter.jsonl")
    p.add_argument("--stage-spent", default="0", help="USD already spent in this stage (stage C: the first run's cost)")
    p.add_argument("--multiplier", default="1", help="scales the output tokens: 0.5, 1 or 2")
    p.add_argument("--total-cap", default=str(TOTAL_CAP))
    p.add_argument("--price-in", default=str(PRICE_IN), help="USD per million input tokens")
    p.add_argument("--price-out", default=str(PRICE_OUT), help="USD per million output tokens")
    return p


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    stage = args.stage.strip().upper()
    builders = [b.strip().lower() for b in args.builders.split(",") if b.strip()]
    if not Path(args.ledger_dir).is_dir():
        parser.error(f"--ledger-dir {args.ledger_dir!r} is not a directory (a typo would read as nothing spent)")
    try:
        stage_spent = _number(args.stage_spent, "--stage-spent")
        cap = _number(args.total_cap, "--total-cap")
        price_in, price_out = _number(args.price_in, "--price-in"), _number(args.price_out, "--price-out")
        multiplier = _number(args.multiplier, "--multiplier", positive=True)
        spent_total, unreadable = ledger_spent(args.ledger_dir)
        result = check(stage, builders, spent_total, stage_spent, cap, price_in, price_out, multiplier)
    except ValueError as exc:
        parser.error(str(exc))

    rows: list[tuple[str, str]] = []
    try:
        if stage in BOUND_ONLY_STAGES:
            rows.append(("expected tokens, one run", "none (stage A has a fixed estimate)"))
        else:
            tokens_in, tokens_out = run_tokens(stage, builders, multiplier)
            rows.append(("expected tokens, one run", f"input {tokens_in:,.0f}   output {tokens_out:,.0f}"
                                                      f"   (output x{multiplier.normalize():f})"))
    except UnknownInput:
        rows.append(("expected tokens, one run", "unknown"))
    rows += [
        ("price per million tokens", f"input {price_in:f}   output {price_out:f}   (USD)"),
        ("estimate for this run", "unknown" if result.estimate is None else f"USD {money(result.estimate)}"),
        ("stage limit", f"USD {STAGE_LIMITS[stage]:f}" if stage in STAGE_LIMITS else "unknown"),
        ("stop at", "unknown" if result.stop_at is None else f"USD {money(result.stop_at)}"),
        ("spent in this stage", f"USD {money(stage_spent)}"),
        ("spent in the ledger", f"USD {money(spent_total)} of a total cap of USD {money(cap)}"),
        ("allowance for this run", "unknown" if result.allowance is None else f"USD {money(result.allowance)}"
                                   "   (what this run may spend)"),
        ("cap for the gateway config", "unknown" if result.cap_for_gateway is None else f"USD {money(result.cap_for_gateway)}"
                                       "   (cumulative: spent in the ledger + allowance)"),
    ]
    print(f"pass-B pre-flight: stage {stage}, builders {','.join(builders) or '-'}")
    print(_table(rows))
    refused = not result.ok
    reason = result.reason
    if unreadable:
        refused = True
        reason = f"the ledger has {unreadable} line(s) whose cost cannot be read, so the spend is unknown" \
                 + ("" if result.ok else "; " + reason)
    print(f"  verdict  {'REFUSED: ' + reason if refused else 'OK, ' + reason}")
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
