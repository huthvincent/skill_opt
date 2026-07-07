"""Statistical primitives for admission gates and gate verdicts.

MANDATORY for all admission decisions (external review 2026-07-06 found a
Wald-interval artifact in a pilot gate: 0/3 -> 3/3 reported "+100pp LCB",
which is a zero-variance boundary artifact; Agresti-Caffo gives ~+10pp).

Rules:
  - NEVER use Wald intervals for proportions (they collapse at 0% / 100%).
  - Single proportion lower bound  -> clopper_pearson_lcb (exact, conservative)
  - Difference of two proportions  -> agresti_caffo_diff_lcb
  - Paired per-task data           -> paired_bootstrap_diff_lcb (preferred for
    our paired A/B micro-validation) or McNemar for verdict-only significance.
    CAVEAT: bootstrap degenerates when n_pairs < ~8 or all diffs identical
    (resampling identical values gives a zero-width interval) - at pilot scale
    use agresti_caffo_diff_lcb and report n explicitly.
  - Report BOTH the point estimate and the LCB; the gate decision uses the LCB.
  - Discovery vs confirmation: the same runs must never both select a candidate
    and report its effect size (winner's curse) - see PROPOSAL experiment rules.
"""
from __future__ import annotations

import math
import random

from scipy.stats import beta as _beta

Z95 = 1.6449  # one-sided 95%
Z90 = 1.2816  # one-sided 90%


def clopper_pearson_lcb(k: int, n: int, alpha: float = 0.05) -> float:
    """Exact one-sided lower bound for a single proportion k/n."""
    if n <= 0:
        raise ValueError("n must be positive")
    if k <= 0:
        return 0.0
    return float(_beta.ppf(alpha, k, n - k + 1))


def agresti_caffo_diff_lcb(k1: int, n1: int, k2: int, n2: int,
                           alpha: float = 0.05) -> float:
    """One-sided lower bound for p1 - p2 (arm1 = treatment, arm2 = control).

    Adds one success and one failure to each arm (Agresti-Caffo 2000) - well
    behaved at 0%/100% boundaries where Wald collapses to zero width.
    """
    if min(n1, n2) <= 0:
        raise ValueError("n must be positive")
    p1 = (k1 + 1) / (n1 + 2)
    p2 = (k2 + 1) / (n2 + 2)
    se = math.sqrt(p1 * (1 - p1) / (n1 + 2) + p2 * (1 - p2) / (n2 + 2))
    z = Z95 if abs(alpha - 0.05) < 1e-9 else abs(_norm_ppf(alpha))
    return (p1 - p2) - z * se


def paired_bootstrap_diff_lcb(pairs: list[tuple[float, float]],
                              alpha: float = 0.05, n_boot: int = 10000,
                              seed: int = 0) -> float:
    """One-sided lower bound for mean(treatment - control) over paired units
    (e.g. per-task success under with-entry vs without-entry, same seeds).
    Resamples task pairs with replacement - respects the pairing structure.
    """
    if not pairs:
        raise ValueError("pairs must be non-empty")
    rng = random.Random(seed)
    diffs = [t - c for t, c in pairs]
    means = []
    for _ in range(n_boot):
        sample = [diffs[rng.randrange(len(diffs))] for _ in range(len(diffs))]
        means.append(sum(sample) / len(sample))
    means.sort()
    return means[int(alpha * n_boot)]


def _norm_ppf(p: float) -> float:
    """Standard normal quantile (Acklam approximation; avoids importing more)."""
    if not 0 < p < 1:
        raise ValueError("p in (0,1)")
    # coefficients
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    if p > phigh:
        return -_norm_ppf(1 - p)
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
           (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)


if __name__ == "__main__":
    # the exact pilot case the review flagged: control 0/3, treatment 3/3
    print("pilot case 0/3 -> 3/3:")
    print("  Agresti-Caffo diff LCB (95%):",
          round(agresti_caffo_diff_lcb(3, 3, 0, 3), 3), "(NOT +1.0)")
    print("  paired bootstrap LCB:",
          round(paired_bootstrap_diff_lcb([(1, 0)] * 3), 3))
    print("  CP LCB of 3/3 alone:", round(clopper_pearson_lcb(3, 3), 3))
