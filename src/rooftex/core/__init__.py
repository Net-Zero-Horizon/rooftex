"""Core rooftop solar computation modules."""

from .adoption import compute_adoption_curve
from .profiles import generate_profiles
from .potential import calculate_potential

__all__ = [
    "compute_adoption_curve",
    "generate_profiles",
    "calculate_potential",
]
