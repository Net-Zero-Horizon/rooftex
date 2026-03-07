"""
RoofteX — Rooftop Solar eXchange

A Python library for rooftop solar potential assessment, adoption dynamics,
and stochastic availability profile generation.

Modules:
- rooftex.core: Adoption curves, solar profiles, rooftop potential
- rooftex.economics: Cost learning curves and integration
- rooftex.config: Configuration dataclasses
"""

__version__ = "0.1.0"
__author__ = "RoofteX Development Team"

from .config import RooftopConfig
from .results import RooftopResult

from .core.adoption import compute_adoption_curve
from .core.profiles import generate_profiles
from .core.potential import calculate_potential

from .economics.learning_curve import compute_learning_curve, compute_installed_capacity

__all__ = [
    "__version__",
    # Config
    "RooftopConfig",
    # Results
    "RooftopResult",
    # Core
    "compute_adoption_curve",
    "generate_profiles",
    "calculate_potential",
    # Economics
    "compute_learning_curve",
    "compute_installed_capacity",
]
