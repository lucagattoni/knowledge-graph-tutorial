"""Tests for tools/exp/passb_preflight.py. Standard library only; no network, no model, no key.

Run from the repository root:

    uv run python -m unittest tools/exp/test_passb_preflight.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import passb_preflight as pf  # noqa: E402

SCRIPT = HERE / "passb_preflight.py"
ALL = ["lightrag", "fast", "ms", "nano"]
D = Decimal


def near(test: unittest.TestCase, value: Decimal, expected: str, tolerance: str = "0.001") -> None:
    test.assertLessEqual(abs(value - D(expected)), D(tolerance), f"{value} is not within {tolerance} of {expected}")


class EstimateTests(unittest.TestCase):
    def test_stage_totals_match_the_plans_table(self):
        near(self, pf.estimate("B", ALL), "0.030")
        near(self, pf.run_estimate("C", ALL), "0.117")
        near(self, pf.estimate("C", ALL), "0.235")
        near(self, pf.estimate("D", ALL), "0.625")

    def test_the_central_estimates_are_the_plans_numbers(self):
        # copied from the plan's cost section (pass-A tokens, scaled by characters), written here a second time on purpose
        self.assertEqual(pf.CENTRAL_ESTIMATES, {
            "B": {"lightrag": (14595, 3296), "fast": (13902, 5601), "ms": (43594, 22889), "nano": (15391, 10815)},
            "C": {"lightrag": (66543, 24290), "fast": (52264, 19457), "ms": (107005, 70204), "nano": (105288, 54750)},
            "D": {"lightrag": (401109, 135391), "fast": (331955, 124603), "ms": (631330, 414204), "nano": (421152, 218999)},
        })
        self.assertEqual(pf.run_tokens("B", ALL), (D(87482), D(42601)))
        self.assertEqual(pf.run_tokens("C", ALL), (D(331100), D(168701)))
        self.assertEqual(pf.run_tokens("D", ALL), (D(1785546), D(893197)))
        self.assertEqual(pf.RUNS_PER_STAGE, {"A": 1, "B": 1, "C": 2, "D": 1})
        self.assertEqual(pf.A_ESTIMATE, D("0.02"))

    def test_stage_c_is_two_runs_and_the_others_one(self):
        self.assertEqual(pf.estimate("C", ALL), 2 * pf.run_estimate("C", ALL))
        for stage in "BD":
            self.assertEqual(pf.estimate(stage, ALL), pf.run_estimate(stage, ALL))

    def test_each_builder_at_twenty_documents_matches_the_plans_table(self):
        for builder, expected in (("lightrag", "0.108"), ("fast", "0.095"), ("ms", "0.270"), ("nano", "0.152")):
            with self.subTest(builder):
                near(self, pf.estimate("D", [builder]), expected)

    def test_the_output_multiplier_cases(self):
        near(self, pf.estimate("D", ALL, multiplier=D("0.5")), "0.402")
        near(self, pf.estimate("D", ALL, multiplier=1), "0.625")
        near(self, pf.estimate("D", ALL, multiplier=2), "1.072")
        near(self, pf.estimate("B", ALL, multiplier=2), "0.051")
        near(self, pf.estimate("C", ALL, multiplier=2), "0.404")

    def test_arithmetic_is_exact_decimal(self):
        # (14595 x 0.10 + 3296 x 0.50) / 1,000,000, one document of LightRAG
        self.assertEqual(pf.estimate("B", ["lightrag"]), D("0.0031075"))
        self.assertEqual(pf.run_tokens("B", ["lightrag", "fast"]), (D(28497), D(8897)))
        self.assertEqual(pf.run_tokens("B", ["lightrag", "fast"], 2), (D(28497), D(17794)))

    def test_prices_are_parameters(self):
        self.assertEqual(pf.estimate("B", ["lightrag"], D("0.2"), D("1.0")), D("0.006215"))
        self.assertEqual(pf.estimate("B", ["lightrag"], 0, 0), D(0))

    def test_stage_a_is_a_fixed_two_cents(self):
        for builders in ([], ALL, ["lightrag"]):
            self.assertEqual(pf.estimate("A", builders), D("0.02"))
            self.assertEqual(pf.estimate("A", builders, 5, 5, 3), D("0.02"))

    def test_unknown_inputs_raise_for_the_plain_functions(self):
        for stage, builders in (("Z", ALL), ("B", ["gpt"]), ("B", []), ("B", ["fast", "fast"]), ("b", ALL)):
            with self.subTest(stage=stage, builders=builders), self.assertRaises(pf.UnknownInput):
                pf.estimate(stage, builders)

    def test_nonsense_numbers_raise(self):
        for kw in ({"multiplier": 0}, {"multiplier": -1}, {"price_in": -1}, {"price_out": "x"}, {"multiplier": "NaN"},
                   {"multiplier": True}):
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                pf.estimate("B", ALL, **kw)


class StopAtTests(unittest.TestCase):
    def test_the_plans_stop_at_values_come_out_of_the_formula(self):
        self.assertEqual(pf.stop_at("A"), D("0.10"))
        self.assertEqual(pf.stop_at("B"), D("0.09"))
        self.assertEqual(pf.stop_at("C"), D("0.60"))
        self.assertEqual(pf.stop_at("D"), D("1.50"))

    def test_it_is_the_lower_of_the_limit_and_three_times_the_central_estimate(self):
        # at twice the price, B's central estimate rounds to 0.060 and three times that, 0.18, is below its limit of 0.20
        self.assertEqual(pf.stop_at("B", D("0.2"), D("1.0")), D("0.18"))
        # at four times the price three times the estimate is above the limit, so the limit wins
        self.assertEqual(pf.stop_at("B", D("0.4"), D("2.0")), D("0.20"))
        # at a tenth of the price C and D are bounded by three times their estimate, not by their limits
        self.assertEqual(pf.stop_at("C", D("0.01"), D("0.05")), D("0.069"))   # 3 x 0.023 (0.0234921 rounded to the mill)
        self.assertEqual(pf.stop_at("D", D("0.01"), D("0.05")), D("0.189"))   # 3 x 0.063 (0.0625153 rounded to the mill)

    def test_it_does_not_depend_on_which_builders_a_run_uses(self):
        self.assertEqual(pf.check("B", ["lightrag"], 0, 0).stop_at, pf.check("B", ALL, 0, 0).stop_at)

    def test_the_limits_and_the_cap(self):
        self.assertEqual(pf.STAGE_LIMITS, {"A": D("0.10"), "B": D("0.20"), "C": D("0.60"), "D": D("1.50")})
        self.assertEqual(pf.TOTAL_CAP, D("3.00"))
        self.assertEqual((pf.PRICE_IN, pf.PRICE_OUT), (D("0.10"), D("0.50")))

    def test_an_unknown_stage_is_an_error(self):
        with self.assertRaises(pf.UnknownInput):
            pf.stop_at("E")


class CheckTests(unittest.TestCase):
    def test_a_run_that_fits_is_ok(self):
        result = pf.check("B", ["lightrag"], 0, 0)
        self.assertTrue(result.ok)
        self.assertTrue(result.reason.startswith("fits"))
        self.assertEqual((result.estimate, result.stop_at, result.cap_for_gateway), (D("0.0031075"), D("0.09"), D("0.20")))

    def test_refused_when_the_stage_would_pass_its_stop_at(self):
        result = pf.check("B", ALL, D("0.06"), D("0.06"))
        self.assertFalse(result.ok)
        self.assertIn("stage B", result.reason)
        self.assertNotIn("total cap", result.reason)
        self.assertTrue(pf.check("B", ALL, D("0.059"), D("0.059")).ok)

    def test_the_stage_boundary_is_exact(self):
        run = pf.estimate("B", ["lightrag"])  # 0.0031075
        ok = pf.check("B", ["lightrag"], D("0.09") - run, D("0.09") - run)
        self.assertTrue(ok.ok, ok.reason)  # reaching the stop at exactly is allowed
        over = pf.check("B", ["lightrag"], D("0.09") - run + D("0.0000001"), D("0.09") - run + D("0.0000001"))
        self.assertFalse(over.ok)

    def test_refused_when_the_total_cap_would_be_passed(self):
        result = pf.check("D", ["lightrag"], D("2.95"), D("0"))
        self.assertFalse(result.ok)
        self.assertIn("total", result.reason)
        self.assertNotIn("stage D:", result.reason)

    def test_the_total_boundary_is_exact(self):
        run = pf.estimate("B", ["lightrag"])
        self.assertTrue(pf.check("B", ["lightrag"], 0, 0, total_cap=run).ok)
        self.assertFalse(pf.check("B", ["lightrag"], 0, 0, total_cap=run - D("0.0000001")).ok)
        self.assertTrue(pf.check("B", ["lightrag"], D("1"), 0, total_cap=D("1") + run).ok)
        self.assertFalse(pf.check("B", ["lightrag"], D("1.0000001"), 0, total_cap=D("1") + run).ok)

    def test_both_reasons_are_given_when_both_fail(self):
        result = pf.check("D", ALL, D("2.9"), D("1.0"))
        self.assertFalse(result.ok)
        self.assertIn("stage D", result.reason)
        self.assertIn("total", result.reason)

    def test_unknown_stage_or_builder_is_a_refusal_not_an_exception(self):
        for stage, builders in (("Z", ALL), ("B", ["gpt"]), ("B", []), ("B", ["fast", "fast"]), ("c", ALL)):
            with self.subTest(stage=stage, builders=builders):
                result = pf.check(stage, builders, 0, 0)
                self.assertFalse(result.ok)
                self.assertIsNone(result.estimate)
        self.assertIsNone(pf.check("Z", ALL, 0, 0).stop_at)
        self.assertIsNone(pf.check("Z", ALL, 0, 0).cap_for_gateway)
        self.assertEqual(pf.check("B", ["gpt"], 0, 0).stop_at, D("0.09"))
        self.assertIn("unknown stage", pf.check("Z", ALL, 0, 0).reason)
        self.assertIn("gpt", pf.check("B", ["gpt"], 0, 0).reason)

    def test_stage_a_needs_no_builders(self):
        result = pf.check("A", [], 0, 0)
        self.assertTrue(result.ok)
        self.assertEqual((result.estimate, result.stop_at, result.cap_for_gateway), (D("0.02"), D("0.10"), D("0.10")))
        self.assertFalse(pf.check("A", [], D("0.09"), D("0.09")).ok)  # 0.09 + 0.02 is over the stop at 0.10
        self.assertTrue(pf.check("A", [], D("0.08"), D("0.08")).ok)

    def test_the_multiplier_scales_the_output_tokens(self):
        self.assertTrue(pf.check("B", ALL, D("0.045"), D("0.045"), multiplier=1).ok)       # 0.045 + 0.0300 <= 0.09
        self.assertFalse(pf.check("B", ALL, D("0.045"), D("0.045"), multiplier=2).ok)      # 0.045 + 0.0513 > 0.09
        near(self, pf.check("B", ALL, 0, 0, multiplier=2).estimate, "0.051")
        near(self, pf.check("B", ALL, 0, 0, multiplier=D("0.5")).estimate, "0.019")

    def test_stage_c_is_checked_one_run_at_a_time_against_what_the_stage_has_spent(self):
        first = pf.check("C", ALL, 0, 0)
        near(self, first.estimate, "0.117")
        self.assertTrue(first.ok)
        second = pf.check("C", ALL, D("0.12"), D("0.12"))
        self.assertTrue(second.ok)
        self.assertFalse(pf.check("C", ALL, D("0.50"), D("0.50")).ok)  # 0.50 + 0.117 is over the stop at 0.60

    def test_inputs_that_make_no_sense_raise(self):
        for args in ((-1, 0), (0, -1), (D("0.5"), D("0.6")), ("x", 0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                pf.check("B", ALL, *args)
        with self.assertRaises(ValueError):
            pf.check("B", ALL, 0, 0, multiplier=0)
        with self.assertRaises(ValueError):
            pf.check("B", ALL, 0, 0, total_cap=-1)


class GatewayCapTests(unittest.TestCase):
    """`allowance` is what this run may spend; `cap_for_gateway` is `spent_total + allowance`, the cumulative cap."""

    def pair(self, result):
        return result.allowance, result.cap_for_gateway

    def test_the_stage_limit_is_the_allowance_at_the_start_and_the_cap_is_that_on_top_of_nothing(self):
        for stage, limit in (("A", "0.10"), ("B", "0.20"), ("C", "0.60"), ("D", "1.50")):
            with self.subTest(stage):
                self.assertEqual(self.pair(pf.check(stage, ["lightrag"], 0, 0)), (D(limit), D(limit)))

    def test_after_spend_in_earlier_stages_the_cap_is_the_spend_plus_the_stage_limit(self):
        # stage A spent 0.02 and nothing yet in stage B: B may spend its 0.20 on top, so the log may reach 0.22
        self.assertEqual(self.pair(pf.check("B", ["lightrag"], D("0.02"), 0)), (D("0.20"), D("0.22")))
        # A and B spent 0.02 + 0.03; stage C starts: its allowance is its limit, the cumulative cap 0.65
        self.assertEqual(self.pair(pf.check("C", ["lightrag"], D("0.05"), 0)), (D("0.60"), D("0.65")))
        # stage D after A, B, C
        self.assertEqual(self.pair(pf.check("D", ["lightrag"], D("0.32"), 0)), (D("1.50"), D("1.82")))

    def test_the_second_run_of_stage_c_has_what_the_first_run_left_of_the_stage_limit(self):
        # earlier stages 0.05, the first run of C spent 0.12: the ledger shows 0.17, the stage 0.12
        result = pf.check("C", ALL, D("0.17"), D("0.12"))
        self.assertTrue(result.ok, result.reason)
        self.assertEqual(self.pair(result), (D("0.48"), D("0.65")))  # 0.60 - 0.12, and 0.17 + 0.48

    def test_the_stage_limit_binds_when_most_of_it_is_spent(self):
        # stage B has spent 0.15 of its 0.20; the ledger shows 0.50 (plenty of the total cap left)
        self.assertEqual(self.pair(pf.check("B", ["lightrag"], D("0.50"), D("0.15"))), (D("0.05"), D("0.55")))

    def test_the_total_cap_binds_when_spent_total_is_close_to_it(self):
        self.assertEqual(self.pair(pf.check("D", ["lightrag"], D("2.95"), 0)), (D("0.05"), D("3.00")))
        self.assertEqual(self.pair(pf.check("D", ["lightrag"], D("2.90"), D("1.0"))), (D("0.10"), D("3.00")))
        self.assertEqual(self.pair(pf.check("C", ["lightrag"], D("2.4"), 0)), (D("0.60"), D("3.00")))   # both bind at once
        self.assertEqual(self.pair(pf.check("C", ["lightrag"], D("2.5"), 0)), (D("0.50"), D("3.00")))

    def test_the_total_cap_is_a_parameter(self):
        self.assertEqual(self.pair(pf.check("D", ["lightrag"], D("0.5"), 0, total_cap=D("1.0"))), (D("0.5"), D("1.0")))

    def test_the_cap_for_the_gateway_never_passes_the_total_cap_while_anything_is_left(self):
        for spent in ("0", "0.5", "1.7", "2.99", "3.00"):
            for stage in "ABCD":
                with self.subTest(stage=stage, spent=spent):
                    result = pf.check(stage, ["lightrag"], D(spent), 0)
                    self.assertLessEqual(result.cap_for_gateway, D("3.00"))
                    self.assertEqual(result.cap_for_gateway, D(spent) + result.allowance)

    def test_nothing_is_allowed_when_the_stage_limit_is_used_up(self):
        for in_stage in ("0.20", "0.25"):
            result = pf.check("B", ["lightrag"], D("0.5"), D(in_stage))
            self.assertEqual(self.pair(result), (D(0), D("0.5")))
            self.assertFalse(result.ok)

    def test_nothing_is_allowed_when_the_total_is_spent_or_passed(self):
        for spent in ("3.00", "3.20"):
            result = pf.check("B", ["lightrag"], D(spent), 0)
            self.assertEqual(self.pair(result), (D(0), D(spent)))
            self.assertFalse(result.ok)

    def test_with_nothing_allowed_any_positive_estimate_is_refused(self):
        exhausted = [("B", D("0.5"), D("0.20")), ("C", D("1"), D("0.60")), ("D", D("2"), D("1.50")), ("A", D("0.5"), D("0.10")),
                     ("B", D("3.00"), 0), ("D", D("3.01"), D("1"))]
        for stage, total, in_stage in exhausted:
            for builders in (["lightrag"], ALL, ["fast"]):
                for multiplier in (D("0.5"), 1, 2):
                    with self.subTest(stage=stage, total=total, in_stage=in_stage, builders=builders, multiplier=multiplier):
                        result = pf.check(stage, builders, total, in_stage, multiplier=multiplier)
                        self.assertEqual(result.allowance, D(0))
                        self.assertGreater(result.estimate, 0)
                        self.assertFalse(result.ok, result.reason)

    def test_whatever_fits_is_within_the_allowance(self):
        spends = [D(x) for x in ("0", "0.02", "0.1", "0.45", "1.0", "2.5", "2.9", "2.99")]
        for stage in "ABCD":
            for total in spends:
                for in_stage in [D(0), total / 2, total]:
                    result = pf.check(stage, ALL if stage != "A" else [], total, in_stage)
                    if result.ok:
                        self.assertLessEqual(result.estimate, result.allowance, (stage, total, in_stage))

    def test_an_unknown_builder_still_gets_the_allowance_and_an_unknown_stage_gets_none(self):
        result = pf.check("B", ["gpt"], D("0.5"), D("0.15"))
        self.assertFalse(result.ok)
        self.assertEqual(self.pair(result), (D("0.05"), D("0.55")))
        result = pf.check("Z", ALL, 0, 0)
        self.assertEqual(self.pair(result), (None, None))


class LedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)

    def write(self, *lines: object, end: bool = True) -> None:
        text = "\n".join(line if isinstance(line, str) else json.dumps(line) for line in lines) + ("\n" if end else "")
        (self.dir / "meter.jsonl").write_text(text)

    def test_a_missing_file_means_nothing_spent(self):
        self.assertEqual(pf.ledger_spent(self.dir), (D(0), 0))

    def test_the_sum_of_cost_in_decimal(self):
        self.write({"cost": "0.1"}, {"cost": "0.2", "other": 1}, {"cost": "0"}, {"cost": 0.7})
        total, unreadable = pf.ledger_spent(self.dir)
        self.assertEqual((total, unreadable), (D("1.0"), 0))
        self.assertIsInstance(total, D)

    def test_blank_lines_are_ignored(self):
        self.write({"cost": "0.1"}, "", "   ", {"cost": "0.2"})
        self.assertEqual(pf.ledger_spent(self.dir), (D("0.3"), 0))

    def test_unreadable_lines_are_counted_not_skipped_silently(self):
        self.write({"cost": "0.1"}, "not json", {"nocost": 1}, {"cost": "abc"}, {"cost": None}, {"cost": True},
                   {"cost": "NaN"}, [1, 2])
        self.assertEqual(pf.ledger_spent(self.dir), (D("0.1"), 7))

    def test_an_unfinished_last_line_is_counted(self):
        self.write({"cost": "0.1"}, '{"cost": "0.2', end=False)
        total, unreadable = pf.ledger_spent(self.dir)
        self.assertEqual((total, unreadable), (D("0.1"), 1))


def run_cli(*args: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, env=env, timeout=60)


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)

    def ledger(self, *costs: str) -> None:
        (self.dir / "meter.jsonl").write_text("".join(json.dumps({"cost": c}) + "\n" for c in costs))

    def cli(self, *args: str) -> subprocess.CompletedProcess:
        return run_cli("--ledger-dir", str(self.dir), *args)

    def test_exit_0_and_a_table_when_it_fits(self):
        self.ledger("0.02")
        done = self.cli("--stage", "B", "--builders", "lightrag,fast")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        for text in ("expected tokens", "input 28,497", "output 8,897", "price per million", "estimate for this run",
                     "0.007298", "stage limit", "stop at", "0.09", "spent in this stage", "spent in the ledger", "0.02",
                     "cap for the gateway config", "0.20", "OK"):
            self.assertIn(text, done.stdout)

    def test_a_missing_ledger_file_in_an_existing_directory_means_nothing_spent(self):
        done = self.cli("--stage", "B", "--builders", "lightrag")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertIn("USD 0.00 of a total cap of USD 3.00", done.stdout)

    def test_exit_1_when_the_stage_would_pass_its_stop_at(self):
        self.ledger("0.07")
        done = self.cli("--stage", "B", "--builders", "lightrag,fast,ms,nano", "--stage-spent", "0.07")
        self.assertEqual(done.returncode, 1, done.stdout + done.stderr)
        self.assertIn("REFUSED", done.stdout)
        self.assertIn("stop at", done.stdout)

    def test_exit_1_when_the_total_cap_would_be_passed(self):
        self.ledger("2.95")
        done = self.cli("--stage", "D", "--builders", "lightrag")
        self.assertEqual(done.returncode, 1, done.stdout + done.stderr)
        self.assertIn("total cap", done.stdout)
        self.assertIn("allowance for this run", done.stdout)
        self.assertRegex(done.stdout, r"allowance for this run\s+USD 0\.05\b")
        self.assertRegex(done.stdout, r"cap for the gateway config\s+USD 3\.00\b")
        self.assertIn("cumulative", done.stdout)

    def test_the_table_shows_the_allowance_and_the_cumulative_cap(self):
        self.ledger("0.05", "0.12")
        done = self.cli("--stage", "C", "--builders", "lightrag", "--stage-spent", "0.12")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertRegex(done.stdout, r"allowance for this run\s+USD 0\.48\b")
        self.assertRegex(done.stdout, r"cap for the gateway config\s+USD 0\.65\b")

    def test_the_multiplier_option(self):
        self.ledger("0.045")
        base = ["--stage", "B", "--builders", "lightrag,fast,ms,nano", "--stage-spent", "0.045"]
        self.assertEqual(self.cli(*base).returncode, 0)
        self.assertEqual(self.cli(*base, "--multiplier", "2").returncode, 1)

    def test_prices_and_cap_options(self):
        self.ledger("0")
        base = ["--stage", "D", "--builders", "lightrag"]
        self.assertEqual(self.cli(*base).returncode, 0)
        self.assertEqual(self.cli(*base, "--total-cap", "0.05").returncode, 1)
        self.assertEqual(self.cli(*base, "--price-in", "10", "--price-out", "50").returncode, 1)

    def test_exit_1_for_an_unknown_stage_or_builder(self):
        self.assertEqual(self.cli("--stage", "E", "--builders", "lightrag").returncode, 1)
        self.assertEqual(self.cli("--stage", "B", "--builders", "lightrag,gpt").returncode, 1)
        self.assertEqual(self.cli("--stage", "B").returncode, 1)

    def test_stage_a_needs_no_builders_and_letters_may_be_lowercase(self):
        done = self.cli("--stage", "a")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        done = self.cli("--stage", "b", "--builders", "LightRAG, Fast")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)

    def test_exit_1_when_the_ledger_has_lines_it_cannot_read(self):
        (self.dir / "meter.jsonl").write_text('{"cost": "0.01"}\nthis is not a record\n')
        done = self.cli("--stage", "B", "--builders", "lightrag")
        self.assertEqual(done.returncode, 1, done.stdout + done.stderr)
        self.assertIn("cannot be read", done.stdout)

    def test_exit_2_on_usage_errors(self):
        self.ledger("0.5")
        cases = {
            "no arguments": [],
            "no ledger dir": ["--stage", "B", "--builders", "lightrag"],
            "ledger dir is not there": ["--stage", "B", "--builders", "lightrag", "--ledger-dir", str(self.dir / "typo")],
            "stage spend is not a number": ["--stage", "B", "--builders", "lightrag", "--stage-spent", "lots"],
            "stage spend is negative": ["--stage", "B", "--builders", "lightrag", "--stage-spent", "-1"],
            "stage spend above the ledger": ["--stage", "B", "--builders", "lightrag", "--stage-spent", "0.6"],
            "multiplier 0": ["--stage", "B", "--builders", "lightrag", "--multiplier", "0"],
            "price is not a number": ["--stage", "B", "--builders", "lightrag", "--price-in", "cheap"],
            "cap is not a number": ["--stage", "B", "--builders", "lightrag", "--total-cap", "x"],
        }
        for label, args in cases.items():
            with self.subTest(label):
                prefix = [] if label in ("no ledger dir", "ledger dir is not there") else ["--ledger-dir", str(self.dir)]
                done = run_cli(*prefix, *args)
                self.assertEqual(done.returncode, 2, done.stdout + done.stderr)


if __name__ == "__main__":
    unittest.main()
