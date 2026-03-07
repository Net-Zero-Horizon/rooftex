"""Configuration dataclasses for RoofteX."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RooftopConfig:
    """Configuration for rooftop solar profile generation.

    Parameters
    ----------
    num_nodes : int
        Number of nodes in the system.
    hours : int
        Number of hours to simulate (default 8760 = 1 year).
    base_year : int
        Base year for adoption calculation.
    target_year : int
        Target year for projections.
    adoption_scenario : str
        Adoption scenario: 'low', 'medium', or 'high'.
    weather_variability : str
        Weather variability level: 'low', 'normal', or 'high'.
    seed : int or None
        Random seed for reproducibility.
    performance_ratio : float
        Overall PV system performance ratio (0-1).
    initial_adoption : list[float] or None
        Initial adoption fraction per node. If None, defaults to 0.05.
    systems_per_node : list[int] or None
        Number of potential rooftop systems per node.
    avg_system_size_kw : list[float] or None
        Average system size in kW per node.
    adoption_rates : dict[str, float] or None
        Custom adoption rate per scenario. Defaults to low=0.05, medium=0.08, high=0.12.
    max_adoption : dict[str, float] or None
        Maximum adoption fraction per scenario. Defaults to low=0.30, medium=0.50, high=0.70.
    """

    num_nodes: int = 1
    hours: int = 8760
    base_year: int = 2024
    target_year: int = 2050
    adoption_scenario: str = "medium"
    weather_variability: str = "normal"
    seed: Optional[int] = None
    performance_ratio: float = 0.75
    initial_adoption: Optional[list[float]] = None
    systems_per_node: Optional[list[int]] = None
    avg_system_size_kw: Optional[list[float]] = None
    adoption_rates: Optional[dict[str, float]] = None
    max_adoption: Optional[dict[str, float]] = None


@dataclass
class LearningCurveConfig:
    """Configuration for cost learning curve projections.

    Parameters
    ----------
    base_cost_per_kw : float
        Base installation cost in $/kW.
    cost_reduction_rate : float
        Annual cost reduction rate (learning rate).
    degradation_rate : float
        Annual panel degradation rate.
    o_and_m_cost : float
        Annual O&M cost in $/kW.
    """

    base_cost_per_kw: float = 1200.0
    cost_reduction_rate: float = 0.08
    degradation_rate: float = 0.005
    o_and_m_cost: float = 20.0
