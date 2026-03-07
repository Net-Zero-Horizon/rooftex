"""Tests for rooftex.core.profiles."""

import numpy as np
import pytest

from rooftex.config import RooftopConfig
from rooftex.core.profiles import generate_base_profile, generate_cloud_pattern, generate_profiles


class TestBaseProfile:
    def test_shape(self):
        profile = generate_base_profile(8760)
        assert profile.shape == (8760,)

    def test_nighttime_zero(self):
        profile = generate_base_profile(24)
        # Hours 0-5 and 19-23 should be zero
        assert profile[0] == 0.0
        assert profile[3] == 0.0
        assert profile[23] == 0.0

    def test_peak_at_noon(self):
        profile = generate_base_profile(24, performance_ratio=1.0)
        assert profile[12] == pytest.approx(1.0, abs=0.01)

    def test_performance_ratio(self):
        p1 = generate_base_profile(24, performance_ratio=1.0)
        p075 = generate_base_profile(24, performance_ratio=0.75)
        np.testing.assert_allclose(p075, p1 * 0.75)


class TestCloudPattern:
    def test_shape(self):
        pattern = generate_cloud_pattern(8760, rng=np.random.default_rng(42))
        assert pattern.shape == (8760,)

    def test_values_range(self):
        pattern = generate_cloud_pattern(8760, rng=np.random.default_rng(42))
        assert np.all(pattern >= 0)
        assert np.all(pattern < 1)

    def test_zero_probability(self):
        pattern = generate_cloud_pattern(8760, cloud_probability=0.0, rng=np.random.default_rng(42))
        assert np.all(pattern == 0)


class TestGenerateProfiles:
    def test_basic(self):
        config = RooftopConfig(num_nodes=3, hours=48, seed=42)
        result = generate_profiles(config)
        assert result.availability.shape == (48, 3)
        assert result.adoption_factors.shape == (3,)
        assert len(result.max_potential_mw) == 3

    def test_values_bounded(self):
        config = RooftopConfig(num_nodes=2, hours=8760, seed=42)
        result = generate_profiles(config)
        assert np.all(result.availability >= 0)
        assert np.all(result.availability <= 1)

    def test_reproducibility(self):
        config = RooftopConfig(num_nodes=2, hours=168, seed=99)
        r1 = generate_profiles(config)
        r2 = generate_profiles(config)
        np.testing.assert_array_equal(r1.availability, r2.availability)

    def test_statistics(self):
        config = RooftopConfig(num_nodes=3, hours=8760, seed=42)
        result = generate_profiles(config)
        stats = result.compute_statistics()
        assert "mean_cf" in stats
        assert "peak_cf" in stats
        assert stats["mean_cf"] > 0
        assert stats["total_potential_mw"] > 0

    def test_custom_systems(self):
        config = RooftopConfig(
            num_nodes=2,
            hours=48,
            seed=42,
            systems_per_node=[1000, 2000],
            avg_system_size_kw=[5.0, 4.0],
        )
        result = generate_profiles(config)
        # Node 0: 1000 * 5.0 / 1000 = 5 MW
        # Node 1: 2000 * 4.0 / 1000 = 8 MW
        assert result.max_potential_mw[0] == pytest.approx(5.0)
        assert result.max_potential_mw[1] == pytest.approx(8.0)
