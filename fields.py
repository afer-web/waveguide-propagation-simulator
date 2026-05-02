"""Field generation for TE/TM modes in a rectangular waveguide."""

from __future__ import annotations

import numpy as np

from modes import validate_mode_indices, validate_waveguide_dimensions


def generate_grid(a: float, b: float, nx: int = 120, ny: int = 90):
    """Generate 2D Cartesian grid (x, y, X, Y) for the waveguide cross-section."""
    validate_waveguide_dimensions(a, b)
    if nx < 2 or ny < 2:
        raise ValueError("Grid sizes nx and ny must both be >= 2.")

    x = np.linspace(0.0, a, nx)
    y = np.linspace(0.0, b, ny)
    x_grid, y_grid = np.meshgrid(x, y, indexing="xy")
    return x, y, x_grid, y_grid


def _field_spatial_profile(
    x_grid: np.ndarray,
    y_grid: np.ndarray,
    a: float,
    b: float,
    m: int,
    n: int,
) -> np.ndarray:
    return np.cos(m * np.pi * x_grid / a) * np.cos(n * np.pi * y_grid / b)


def mode_field(
    mode_type: str,
    x_grid: np.ndarray,
    y_grid: np.ndarray,
    a: float,
    b: float,
    m: int,
    n: int,
    beta: float,
    omega: float,
    z: float = 0.0,
    t: float = 0.0,
) -> np.ndarray:
    """
    Generate field map for TE and TM.

    Uses the shared scalar form:
    F = cos(m*pi*x/a) * cos(n*pi*y/b) * cos(beta*z - omega*t)
    where F represents Ez for TE or Hz for TM.
    """
    validate_waveguide_dimensions(a, b)
    validate_mode_indices(m, n)

    mode_key = mode_type.upper()
    if mode_key not in {"TE", "TM"}:
        raise ValueError("mode_type must be either 'TE' or 'TM'.")

    spatial = _field_spatial_profile(x_grid, y_grid, a, b, m, n)
    phase = np.cos(beta * z - omega * t)
    field = spatial * phase
    return field
