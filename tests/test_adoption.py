"""Tests for rooftex.core.adoption."""

import numpy as np
import pytest

from rooftex.core.adoption import compute_adoption_curve


class TestAdoptionCurve:
    def test_basic_shape(self):
        result = compute_adoption_curve(
            num_nodes=3,
            base_year=2024,
            target_year=2050,
            rng=np.random.default_rng(42),
        )
        assert result.shape == (3,)
        assert np.all(result >= 0)
        assert np.all(result <= 1)

    def test_higher_scenario_more_adoption(self):
        rng_low = np.random.default_rng(42)
        rng_high = np.random.default_rng(42)
        low = compute_adoption_curve(
            num_nodes=5, base_year=2024, target_year=2050,
            adoption_scenario="low", rng=rng_low,
        )
        high = compute_adoption_curve(
            num_nodes=5, base_year=2024, target_year=2050,
            adoption_scenario="high", rng=rng_high,
        )
        assert np.mean(high) > np.mean(low)

    def test_reproducibility(self):
        a = compute_adoption_curve(
            num_nodes=3, base_year=2024, target_year=2050,
            rng=np.random.default_rng(99),
        )
        b = compute_adoption_curve(
            num_nodes=3, base_year=2024, target_year=2050,
            rng=np.random.default_rng(99),
        )
        np.testing.assert_array_equal(a, b)

    def test_custom_initial_adoption(self):
        result = compute_adoption_curve(
            num_nodes=2, base_year=2024, target_year=2050,
            initial_adoption=[0.1, 0.2],
            rng=np.random.default_rng(42),
        )
        assert result.shape == (2,)

    def test_custom_urbanization(self):
        urban = np.array([0.9, 0.1])
        result = compute_adoption_curve(
            num_nodes=2, base_year=2024, target_year=2050,
            urbanization_factors=urban,
            rng=np.random.default_rng(42),
        )
        # Higher urbanization → higher adoption
        assert result[0] > result[1]
