"""Compatibility import for the shared build123d construction helpers.

Part modules retain their existing ``from geometry import ...`` imports.
Implementations live in the repository's reusable ``tools/`` directory.
"""
from __future__ import annotations
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[2] / 'tools'
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cad_geometry import cone, cylinder, polygon_xz, radial_profile, rectangular_prism, rounded_prism

__all__ = ('cone', 'cylinder', 'polygon_xz', 'radial_profile',
           'rectangular_prism', 'rounded_prism')
