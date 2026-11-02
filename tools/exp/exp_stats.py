"""Small statistics for the experiments: an exact paired sign test, Wilson intervals, a seeded paired bootstrap.

Standard library only. Each function is checked in test_exp_stats.py against an independent oracle (brute-force
enumeration, or a root solve of the defining equation), not against a copy of its own formula.

    paired_counts(a, b)        -> (b_only, a_only): questions only B got right, questions only A got right
    sign_test(b_only, a_only)  -> exact two-sided p-value under "each discordant pair is a fair coin"
    wilson(successes, n, z)    -> (low, high) interval for a proportion
    bootstrap_mean_diff(xs, ys, resamples, seed, level) -> (mean difference, low, high), paired, percentile method

What these do not do: they say nothing about whether a comparison is fair, whether questions are independent, or
whether the sample is large enough to matter. They only compute the number asked for.
"""

from __future__ import annotations

import math
import random
from typing import Sequence


def paired_counts(a: Sequence[bool], b: Sequence[bool]) -> tuple[int, int]:
    """Discordant pairs of two runs on the same questions: (right only in b, right only in a)."""
    if len(a) != len(b):
        raise ValueError("the two runs must cover the same questions")
    b_only = sum(1 for x, y in zip(a, b) if y and not x)
    a_only = sum(1 for x, y in zip(a, b) if x and not y)
    return b_only, a_only


def sign_test(b_only: int, a_only: int) -> float:
    """Exact two-sided sign test on the discordant pairs. No discordant pair gives p = 1."""
    if b_only < 0 or a_only < 0:
        raise ValueError("counts cannot be negative")
    n = b_only + a_only
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, k) for k in range(0, min(b_only, a_only) + 1))
    return min(1.0, 2 * tail / 2**n)


def wilson(successes: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Wilson score interval for a proportion (default: 95%)."""
    if n <= 0 or not 0 <= successes <= n:
        raise ValueError("need 0 <= successes <= n and n > 0")
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def bootstrap_mean_diff(
    xs: Sequence[float], ys: Sequence[float], resamples: int = 2000, seed: int = 1, level: float = 0.95
) -> tuple[float, float, float]:
    """Paired percentile bootstrap of mean(ys - xs). Same seed, same answer, on any machine."""
    if len(xs) != len(ys) or not xs:
        raise ValueError("need two non-empty samples of the same length")
    if not 0 < level < 1 or resamples < 1:
        raise ValueError("bad level or resamples")
    diffs = [y - x for x, y in zip(xs, ys)]
    n = len(diffs)
    rng = random.Random(seed)
    means = sorted(sum(diffs[rng.randrange(n)] for _ in range(n)) / n for _ in range(resamples))
    lo_i = int(math.floor((1 - level) / 2 * resamples))
    hi_i = min(resamples - 1, int(math.ceil((1 + level) / 2 * resamples)) - 1)
    return sum(diffs) / n, means[lo_i], means[hi_i]
