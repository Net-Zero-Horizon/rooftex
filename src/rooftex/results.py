"""Result dataclasses for RoofteX."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass
class RooftopResult:
    """Result of rooftop solar profile generation.

    Attributes
    ----------
    availability : np.ndarray
        Hourly availability matrix, shape (hours, num_nodes). Values in [0, 1].
    adoption_factors : np.ndarray
        Adoption factor per node at the target year.
    max_potential_mw : list[float]
        Maximum rooftop PV potential per node in MW.
    """

    availability: Any  # np.ndarray (hours, num_nodes)
    adoption_factors: Any  # np.ndarray (num_nodes,)
    max_potential_mw: list[float]

    def compute_statistics(self) -> dict:
        """Compute summary statistics.

        Returns
        -------
        dict
            Dictionary with mean_cf, peak_cf, mean_adoption, total_potential_mw.
        """
        avail = np.asarray(self.availability)
        return {
            "mean_cf": float(np.nanmean(avail[avail > 0])) if np.any(avail > 0) else 0.0,
            "peak_cf": float(np.nanmax(avail)),
            "mean_adoption": float(np.mean(self.adoption_factors)),
            "total_potential_mw": sum(self.max_potential_mw),
        }

    def to_dict(self) -> dict:
        """Convert result to dictionary."""
        return {
            "availability": np.asarray(self.availability).tolist(),
            "adoption_factors": np.asarray(self.adoption_factors).tolist(),
            "max_potential_mw": list(self.max_potential_mw),
            "statistics": self.compute_statistics(),
        }


@dataclass
class LearningCurveResult:
    """Result of cost learning curve computation.

    Attributes
    ----------
    year : int
        Target year.
    cost_per_kw : float
        Projected cost in $/kW.
    cost_factor : float
        Cost reduction factor relative to base year.
    installed_capacity_mw : np.ndarray
        Installed capacity per node in MW.
    total_installed_mw : float
        Total installed capacity in MW.
    """

    year: int
    cost_per_kw: float
    cost_factor: float
    installed_capacity_mw: Any  # np.ndarray
    total_installed_mw: float
