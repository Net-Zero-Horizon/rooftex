# RoofteX — Rooftop Solar eXchange

[![Tests](https://github.com/msotocalvo/rooftex/actions/workflows/tests.yml/badge.svg)](https://github.com/msotocalvo/rooftex/actions/workflows/tests.yml)
[![DOI](https://zenodo.org/badge/1175040710.svg)](https://doi.org/10.5281/zenodo.18898422)

A Python library for rooftop solar potential assessment, adoption dynamics modeling,
and stochastic availability profile generation.

## Features

- **Rooftop Potential**: Estimate maximum rooftop PV capacity from population and dwelling data
- **Adoption Dynamics**: S-curve adoption modeling with urbanization and scenario parameters
- **Profile Generation**: Stochastic hourly solar profiles with cloud patterns and weather variability
- **Cost Learning Curve**: Technology cost projection with degradation and learning rates

## Installation

```bash
pip install rooftex
```

## Quick Start

```python
from rooftex import RooftopConfig, generate_profiles, calculate_potential

# Estimate potential from population
potential = calculate_potential(population=[50000, 30000, 80000])

# Generate hourly availability profiles
config = RooftopConfig(
    num_nodes=3,
    hours=8760,
    adoption_scenario="medium",
    target_year=2040,
)
result = generate_profiles(config)
print(result.availability.shape)      # (8760, 3)
print(result.adoption_factors.mean())  # ~0.3
```

## License

MIT
