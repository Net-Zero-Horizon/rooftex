"""Stochastic rooftop solar profile generation.

Generates hourly availability profiles with bell-curve solar patterns,
weather variability, and cloud events.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from rooftex.config import RooftopConfig
from rooftex.core.adoption import compute_adoption_curve
from rooftex.core.potential import calculate_potential_from_config
from rooftex.results import RooftopResult


# Weather variance maps
_WEATHER_VARIANCE = {"low": 0.05, "normal": 0.15, "high": 0.25}
_NODE_VARIANCE = {"low": 0.10, "normal": 0.20, "high": 0.30}


def generate_base_profile(hours: int, performance_ratio: float = 0.75) -> np.ndarray:
    """Generate a base bell-shaped solar profile.

    Parameters
    ----------
    hours : int
        Number of hours to simulate.
    performance_ratio : float
        System performance ratio (0-1).

    Returns
    -------
    np.ndarray
        Base solar profile, shape (hours,).
    """
    hours_mod = np.arange(hours) % 24
    profile = np.zeros(hours)

    daylight = (hours_mod >= 6) & (hours_mod <= 18)
    profile[daylight] = np.sin(np.pi * (hours_mod[daylight] - 6) / 12)

    return profile * performance_ratio


def generate_cloud_pattern(
    hours: int,
    cloud_probability: float = 0.3,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Generate stochastic cloud patterns.

    Parameters
    ----------
    hours : int
        Number of hours.
    cloud_probability : float
        Daily probability of cloud events.
    rng : np.random.Generator or None
        Random number generator.

    Returns
    -------
    np.ndarray
        Cloud attenuation pattern, shape (hours,). Values in [0, 1].
    """
    if rng is None:
        rng = np.random.default_rng()

    num_days = max(1, hours // 24)
    pattern = np.zeros(hours)

    for day in range(num_days):
        if rng.random() < cloud_probability:
            cloud_start = rng.integers(6, 16)
            cloud_duration = rng.integers(1, 4)
            cloud_intensity = rng.uniform(0.3, 0.7)
            day_offset = day * 24
            for h in range(cloud_start, min(cloud_start + cloud_duration, 24)):
                idx = day_offset + h
                if idx < hours:
                    pattern[idx] = cloud_intensity

    return pattern


def generate_profiles(config: RooftopConfig) -> RooftopResult:
    """Generate stochastic rooftop solar availability profiles.

    Creates hourly availability matrices with weather variability, cloud
    patterns, and node-specific factors. Also computes adoption curves
    and maximum potential.

    Parameters
    ----------
    config : RooftopConfig
        Configuration parameters.

    Returns
    -------
    RooftopResult
        Result containing availability matrix, adoption factors, and potentials.
    """
    rng = np.random.default_rng(config.seed)

    num_nodes = config.num_nodes
    hours = config.hours

    # Base solar profile
    base_profile = generate_base_profile(hours, config.performance_ratio)

    # Weather variability
    weather_var = _WEATHER_VARIANCE.get(config.weather_variability, 0.15)
    node_var = _NODE_VARIANCE.get(config.weather_variability, 0.20)

    # Urbanization factors
    urbanization = rng.beta(2, 2, num_nodes)

    # Maximum potential
    max_potential = calculate_potential_from_config(config, urbanization, rng)

    # Daily weather component (shared across nodes)
    num_days = max(1, hours // 24)
    daily_weather = np.clip(
        rng.normal(1.0, weather_var, num_days), 0.2, 1.8
    )
    daily_weather = np.repeat(daily_weather, 24)[:hours]

    # Generate availability per node
    availability = np.zeros((hours, num_nodes))

    for node in range(num_nodes):
        node_factor = float(np.clip(rng.normal(1.0, node_var), 0.6, 1.4))
        hourly_noise = rng.normal(0, 0.05, hours)
        cloud_pattern = generate_cloud_pattern(hours, rng=rng)

        for h in range(hours):
            raw = (
                base_profile[h]
                * node_factor
                * daily_weather[h]
                * (1 - cloud_pattern[h])
                + hourly_noise[h]
            )
            availability[h, node] = max(0.0, min(1.0, raw))

    # Adoption factors
    adoption = compute_adoption_curve(
        num_nodes=num_nodes,
        base_year=config.base_year,
        target_year=config.target_year,
        adoption_scenario=config.adoption_scenario,
        initial_adoption=config.initial_adoption,
        adoption_rates=config.adoption_rates,
        max_adoption=config.max_adoption,
        urbanization_factors=urbanization,
        rng=rng,
    )

    return RooftopResult(
        availability=availability,
        adoption_factors=adoption,
        max_potential_mw=max_potential,
    )
