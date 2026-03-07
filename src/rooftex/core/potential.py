"""Rooftop solar potential estimation.

Estimates maximum rooftop PV capacity from population, dwelling density,
and roof characteristics.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from rooftex.config import RooftopConfig


def calculate_potential(
    population: list[float],
    dwelling_density: float = 0.35,
    avg_roof_area: float = 50.0,
    suitable_fraction: float = 0.3,
    panel_efficiency: float = 0.20,
    solar_irradiance: float = 1000.0,
) -> list[float]:
    """Calculate rooftop solar potential based on population.

    Parameters
    ----------
    population : list[float]
        Population per node.
    dwelling_density : float
        Dwellings per capita.
    avg_roof_area : float
        Average roof area in m².
    suitable_fraction : float
        Fraction of roof suitable for solar.
    panel_efficiency : float
        Solar panel efficiency (0-1).
    solar_irradiance : float
        Peak solar irradiance in W/m².

    Returns
    -------
    list[float]
        Maximum potential in MW per node.
    """
    max_potential = []
    for pop in population:
        num_dwellings = pop * dwelling_density
        total_roof_area = num_dwellings * avg_roof_area * suitable_fraction
        peak_power_kw = total_roof_area * panel_efficiency * solar_irradiance / 1000
        max_potential.append(peak_power_kw / 1000)  # Convert to MW

    return max_potential


def calculate_potential_from_config(
    config: "RooftopConfig",
    urbanization_factors: np.ndarray | None = None,
    rng: np.random.Generator | None = None,
) -> list[float]:
    """Calculate potential from config, using system specs or randomized base values.

    Parameters
    ----------
    config : RooftopConfig
        Configuration with optional systems_per_node and avg_system_size_kw.
    urbanization_factors : np.ndarray or None
        Urbanization factor per node. Used for random potential generation.
    rng : np.random.Generator or None
        Random number generator.

    Returns
    -------
    list[float]
        Maximum potential per node in MW.
    """
    if rng is None:
        rng = np.random.default_rng()

    num_nodes = config.num_nodes

    if config.systems_per_node is not None and config.avg_system_size_kw is not None:
        systems = list(config.systems_per_node)
        sizes = list(config.avg_system_size_kw)

        while len(systems) < num_nodes:
            systems.append(systems[-1] if systems else 5000)
        while len(sizes) < num_nodes:
            sizes.append(sizes[-1] if sizes else 5.0)

        return [systems[i] * sizes[i] / 1000 for i in range(num_nodes)]

    # Random potential based on urbanization
    if urbanization_factors is None:
        urbanization_factors = rng.beta(2, 2, num_nodes)

    base_potential = 50 + rng.gamma(shape=2.0, scale=30.0, size=num_nodes)
    return list(base_potential * (0.5 + urbanization_factors))
