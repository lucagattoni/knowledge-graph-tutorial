"""Tests for tools/exp/exp_stats.py. Standard library only. Each check uses an oracle that does not share the code's formula.

Run from the repository root:

    uv run python -m unittest tools/exp/test_exp_stats.py
"""

from __future__ import annotations

import itertools
import math
import random
import sys
import unittest
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import exp_stats as st  # noqa: E402


def sign_p_by_enumeration(b_only: int, a_only: int) -> Fraction:
    """Oracle: list every one of the 2^n equally likely outcomes of n fair coins and count the ones at least as extreme."""
    n = b_only + a_only
    if n == 0:
        return Fraction(1)
    observed = min(b_only, a_only)
    extreme = 0
    for outcome in itertools.product((0, 1), repeat=n):
        heads = sum(outcome)
        if min(heads, n - heads) <= observed:
            extreme += 1
    return min(Fraction(1), Fraction(extreme, 2**n))


def wilson_by_bisection(successes: int, n: int, z: float) -> tuple[float, float]:
    """Oracle: the Wilson interval is the set of p0 with |phat - p0| <= z*sqrt(p0(1-p0)/n). Find its two ends numerically."""
    phat = successes / n

    def inside(p0: float) -> bool:
        return abs(phat - p0) <= z * math.sqrt(p0 * (1 - p0) / n) + 1e-15

    def edge(lo: float, hi: float, want_inside_at_hi: bool) -> float:
        for _ in range(200):
            mid = (lo + hi) / 2
            if inside(mid) == want_inside_at_hi:
                hi = mid
            else:
                lo = mid
        return (lo + hi) / 2

    low = edge(0.0, phat, True) if phat > 0 else 0.0
    high = edge(phat, 1.0, False) if phat < 1 else 1.0
    return low, high


class SignTestTests(unittest.TestCase):
    def test_matches_brute_force_enumeration_for_every_small_case(self) -> None:
        for b in range(0, 9):
            for a in range(0, 9):
                with self.subTest(b=b, a=a):
                    self.assertAlmostEqual(st.sign_test(b, a), float(sign_p_by_enumeration(b, a)), places=12)

    def test_symmetric_and_one_when_balanced_or_empty(self) -> None:
        self.assertEqual(st.sign_test(7, 3), st.sign_test(3, 7))
        self.assertEqual(st.sign_test(5, 5), 1.0)
        self.assertEqual(st.sign_test(0, 0), 1.0)

    def test_extreme_case_is_two_over_two_to_the_n(self) -> None:
        self.assertAlmostEqual(st.sign_test(12, 0), 2 / 2**12, places=15)

    def test_a_p_value_never_exceeds_one(self) -> None:
        self.assertEqual(st.sign_test(1, 1), 1.0)

    def test_negative_counts_are_refused(self) -> None:
        with self.assertRaises(ValueError):
            st.sign_test(-1, 3)


class PairedCountsTests(unittest.TestCase):
    def test_counts_discordant_pairs_in_the_right_direction(self) -> None:
        a = [True, True, False, False, True]
        b = [True, False, True, True, True]
        self.assertEqual(st.paired_counts(a, b), (2, 1))

    def test_different_lengths_are_refused(self) -> None:
        with self.assertRaises(ValueError):
            st.paired_counts([True], [True, False])


class WilsonTests(unittest.TestCase):
    def test_matches_the_defining_equation_across_many_cases(self) -> None:
        z = 1.959963984540054
        for n in (1, 2, 5, 10, 37, 100, 1000):
            for k in sorted({0, 1, n // 3, n // 2, n - 1, n}):
                with self.subTest(n=n, k=k):
                    lo, hi = st.wilson(k, n, z)
                    olo, ohi = wilson_by_bisection(k, n, z)
                    self.assertAlmostEqual(lo, olo, places=7)
                    self.assertAlmostEqual(hi, ohi, places=7)

    def test_perfect_and_empty_answerers_hit_the_edges_without_leaving_zero_one(self) -> None:
        lo, hi = st.wilson(20, 20)
        self.assertEqual(hi, 1.0)
        self.assertLess(lo, 1.0)
        lo, hi = st.wilson(0, 20)
        self.assertEqual(lo, 0.0)
        self.assertGreater(hi, 0.0)

    def test_bounds_stay_inside_zero_one_for_every_sample_size_up_to_500(self) -> None:
        for n in range(1, 501):
            for k in (0, n, n // 2):
                lo, hi = st.wilson(k, n)
                self.assertTrue(0.0 <= lo <= hi <= 1.0, (n, k, lo, hi))

    def test_a_random_answerer_gets_an_interval_around_one_half(self) -> None:
        rng = random.Random(7)
        hits = sum(rng.random() < 0.5 for _ in range(400))
        lo, hi = st.wilson(hits, 400)
        self.assertLess(lo, 0.5)
        self.assertGreater(hi, 0.5)

    def test_bad_arguments_are_refused(self) -> None:
        for args in ((-1, 5), (6, 5), (0, 0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                st.wilson(*args)


class BootstrapTests(unittest.TestCase):
    def test_same_seed_gives_the_same_answer_and_a_different_seed_does_not(self) -> None:
        # Thirty distinct differences, so two unseeded runs cannot agree by landing on the same few values.
        xs = [0.1 * i for i in range(30)]
        ys = [x + math.sin(i + 1) for i, x in enumerate(xs)]
        for _ in range(5):
            self.assertEqual(st.bootstrap_mean_diff(xs, ys, seed=3), st.bootstrap_mean_diff(xs, ys, seed=3))
        self.assertNotEqual(st.bootstrap_mean_diff(xs, ys, seed=3), st.bootstrap_mean_diff(xs, ys, seed=4))

    def test_the_mean_is_exact_and_the_interval_brackets_it(self) -> None:
        xs = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        ys = [2.0, 2.5, 3.5, 4.0, 6.5, 6.0]
        mean, lo, hi = st.bootstrap_mean_diff(xs, ys, resamples=4000)
        self.assertAlmostEqual(mean, sum(y - x for x, y in zip(xs, ys)) / 6, places=12)
        self.assertLessEqual(lo, mean)
        self.assertGreaterEqual(hi, mean)

    def test_identical_runs_give_a_point_at_zero(self) -> None:
        xs = [1.0, 2.0, 3.0]
        self.assertEqual(st.bootstrap_mean_diff(xs, xs), (0.0, 0.0, 0.0))

    def test_a_constant_shift_gives_a_point_at_the_shift(self) -> None:
        xs = [1.0, 2.0, 3.0, 4.0]
        mean, lo, hi = st.bootstrap_mean_diff(xs, [x + 2 for x in xs])
        self.assertEqual((mean, lo, hi), (2.0, 2.0, 2.0))

    def test_bad_arguments_are_refused(self) -> None:
        for args in (([], []), ([1.0], [1.0, 2.0])):
            with self.subTest(args=args), self.assertRaises(ValueError):
                st.bootstrap_mean_diff(*args)


if __name__ == "__main__":
    unittest.main()
