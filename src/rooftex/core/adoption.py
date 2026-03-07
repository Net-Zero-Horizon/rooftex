"""S-curve adoption dynamics for rooftop solar.

Models technology adoption using logistic (S-curve) functions with
urbanization factors and scenario-dependent parameters.
"""

from __future__ import annotations

import numpy as np


# Default adoption rates per scenario
_DEFAULT_ADOPTION_RATES = {
    "low": 0.05,
    "medium": 0.08,
    "high": 0.12,
}

# Default maximum adoption per scenario
_DEFAULT_MAX_ADOPTION = {
    "low": 0.30,
    "medium": 0.50,
    "high": 0.70,
}


def compute_adoption_curve(
    num_nodes: int,
    base_year: int,
    target_year: int,
    adoption_scenario: str = "medium",
    initial_adoption: list[float] | None = None,
    adoption_rates: dict[str, float] | None = None,
    max_adoption: dict[str, float] | None = None,
    urbanization_factors: np.ndarray | None = None,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Compute adoption factors at the target year using S-curve dynamics.

    Each node gets a logistic adoption curve influenced by its urbanization
    factor and the chosen scenario.

    Parameters
    ----------
    num_nodes : int
        Number of nodes.
    base_year : int
        Base year for adoption calculation.
    target_year : int
        Year at which to evaluate adoption.
    adoption_scenario : str
        Scenario: 'low', 'medium', or 'high'.
    initial_adoption : list[float] or None
        Initial adoption fraction per node. Defaults to 0.05.
    adoption_rates : dict[str, float] or None
        Custom adoption rates per scenario.
    max_adoption : dict[str, float] or None
        Maximum adoption fraction per scenario.
    urbanization_factors : np.ndarray or None
        Urbanization factor per node in [0, 1]. If None, drawn from Beta(2,2).
    rng : np.random.Generator or None
        Random number generator.

    Returns
    -------
    np.ndarray
        Adoption factors per node at target_year, shape (num_nodes,).
    """
    if rng is None:
        rng = np.random.default_rng()

    rates = adoption_rates or _DEFAULT_ADOPTION_RATES
    max_adopt = max_adoption or _DEFAULT_MAX_ADOPTION

    adoption_rate = rates.get(adoption_scenario, 0.08)
    max_adoption_val = max_adopt.get(adoption_scenario, 0.50)

    years_diff = target_year - base_year

    # Initial adoption per node
    if initial_adoption is not None:
        init = list(initial_adoption)
        while len(init) < num_nodes:
            init.append(init[-1] if init else 0.05)
    else:
        init = [0.05] * num_nodes

    # Urbanization
    if urbanization_factors is None:
        urbanization_factors = rng.beta(2, 2, num_nodes)
    else:
        urbanization_factors = np.asarray(urbanization_factors)

    adoption = np.zeros(num_nodes)
    for node in range(num_nodes):
        node_max = min(0.9, max_adoption_val * (0.8 + 0.4 * urbanization_factors[node]))
        mid_point = base_year + years_diff * (0.4 + 0.2 * rng.random())
        growth_rate = adoption_rate * (0.8 + 0.4 * urbanization_factors[node])

        adoption[node] = node_max / (1 + np.exp(-growth_rate * (target_year - mid_point)))

    return adoption
