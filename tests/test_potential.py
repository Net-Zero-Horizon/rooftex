"""Tests for rooftex.core.potential."""

import pytest

from rooftex.core.potential import calculate_potential


class TestCalculatePotential:
    def test_basic(self):
        result = calculate_potential(population=[100000])
        assert len(result) == 1
        assert result[0] > 0

    def test_multiple_nodes(self):
        result = calculate_potential(population=[50000, 100000, 200000])
        assert len(result) == 3
        # Larger population → more potential
        assert result[0] < result[1] < result[2]

    def test_linear_scaling(self):
        r1 = calculate_potential(population=[50000])
        r2 = calculate_potential(population=[100000])
        assert r2[0] == pytest.approx(r1[0] * 2, rel=1e-10)

    def test_custom_params(self):
        result = calculate_potential(
            population=[100000],
            dwelling_density=0.5,
            avg_roof_area=40.0,
            suitable_fraction=0.25,
            panel_efficiency=0.22,
            solar_irradiance=1000.0,
        )
        # 100000 * 0.5 = 50000 dwellings
        # 50000 * 40 * 0.25 = 500000 m² suitable
        # 500000 * 0.22 * 1000 / 1000 = 110000 kW = 110 MW
        assert result[0] == pytest.approx(110.0)

    def test_zero_population(self):
        result = calculate_potential(population=[0])
        assert result[0] == 0.0
