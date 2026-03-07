"""Cost learning curve and capacity integration for rooftop solar.

Models technology cost reduction over time and computes installed
capacity accounting for adoption dynamics and degradation.
"""

from __future__ import annotations

import numpy as np

from rooftex.config import LearningCurveConfig
from rooftex.results import LearningCurveResult


def compute_learning_curve(
    base_year: int,
    target_year: int,
    config: LearningCurveConfig | None = None,
    years: list[int] | None = None,
) -> list[tuple[int, float]]:
    """Compute cost trajectory using exponential learning curve.

    Parameters
    ----------
    base_year : int
        Base year (cost = base_cost_per_kw).
    target_year : int
        Final year to compute.
    config : LearningCurveConfig or None
        Cost parameters. Uses defaults if None.
    years : list[int] or None
        Specific years to evaluate. If None, evaluates every year.

    Returns
    -------
    list[tuple[int, float]]
        List of (year, cost_per_kw) tuples.
    """
    if config is None:
        config = LearningCurveConfig()

    if years is None:
        years = list(range(base_year, target_year + 1))

    result = []
    for year in years:
        years_diff = year - base_year
        cost_factor = (1 - config.cost_reduction_rate) ** years_diff
        cost = config.base_cost_per_kw * cost_factor
        result.append((year, cost))

    return result


def compute_installed_capacity(
    year: int,
    base_year: int,
    target_year: int,
    max_potential_mw: list[float],
    adoption_factors: np.ndarray,
    config: LearningCurveConfig | None = None,
) -> LearningCurveResult:
    """Compute installed capacity and cost at a specific year.

    Applies S-curve progress factor and degradation to the adoption-based
    capacity estimate.

    Parameters
    ----------
    year : int
        Year to evaluate.
    base_year : int
        Base year.
    target_year : int
        Target year for full adoption.
    max_potential_mw : list[float]
        Maximum potential per node in MW.
    adoption_factors : np.ndarray
        Adoption factors per node (from compute_adoption_curve).
    config : LearningCurveConfig or None
        Cost parameters. Uses defaults if None.

    Returns
    -------
    LearningCurveResult
        Installed capacity and cost information.
    """
    if config is None:
        config = LearningCurveConfig()

    years_diff = year - base_year

    # S-curve progress
    progress = min(1.0, years_diff / max(1, target_year - base_year))
    s_curve = 1.0 / (1.0 + np.exp(-10.0 * (progress - 0.5)))

    current_adoption = adoption_factors * s_curve

    # Installed capacity with degradation
    installed = np.array(max_potential_mw) * current_adoption
    degradation = 1.0 - (config.degradation_rate * years_diff / 2)
    installed = installed * degradation

    # Cost
    cost_factor = (1 - config.cost_reduction_rate) ** years_diff
    cost_per_kw = config.base_cost_per_kw * cost_factor

    return LearningCurveResult(
        year=year,
        cost_per_kw=cost_per_kw,
        cost_factor=cost_factor,
        installed_capacity_mw=installed,
        total_installed_mw=float(np.sum(installed)),
    )
