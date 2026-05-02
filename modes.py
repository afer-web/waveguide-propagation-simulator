"""Utilities for rectangular waveguide mode calculations."""

from __future__ import annotations

import math


C0 = 299_792_458.0
EPSILON = 1e-12


def validate_waveguide_dimensions(a: float, b: float) -> None:
    """Validate waveguide dimensions."""
    if a <= 0 or b <= 0:
        raise ValueError("Waveguide dimensions must satisfy a > 0 and b > 0.")


def validate_mode_indices(m: int, n: int) -> None:
    """Validate mode indices."""
    if m < 0 or n < 0:
        raise ValueError("Mode indices must satisfy m >= 0 and n >= 0.")
    if m == 0 and n == 0:
        raise ValueError("Mode indices cannot both be zero.")


def cutoff_frequency(a: float, b: float, m: int, n: int, c: float = C0) -> float:
    """
    Compute cutoff frequency:
    fc = (c / 2) * sqrt((m / a)^2 + (n / b)^2)
    """
    validate_waveguide_dimensions(a, b)
    validate_mode_indices(m, n)
    inside = (m / a) ** 2 + (n / b) ** 2
    return (c / 2.0) * math.sqrt(inside)


def wavenumber(frequency: float, c: float = C0) -> float:
    """Compute free-space wavenumber k0 = 2*pi*f/c."""
    if frequency <= 0:
        raise ValueError("Frequency must be > 0.")
    return 2.0 * math.pi * frequency / c


def guided_beta(
    frequency: float,
    a: float,
    b: float,
    m: int,
    n: int,
    c: float = C0,
) -> float:
    """
    Compute guided propagation constant:
    beta = sqrt(k0^2 - (m*pi/a)^2 - (n*pi/b)^2)
    """
    validate_waveguide_dimensions(a, b)
    validate_mode_indices(m, n)
    k0 = wavenumber(frequency, c)
    beta_sq = k0**2 - (m * math.pi / a) ** 2 - (n * math.pi / b) ** 2

    if beta_sq < -EPSILON:
        raise ValueError("Numerical result indicates evanescent mode (beta^2 < 0).")

    return math.sqrt(max(beta_sq, 0.0))


def guided_wavelength(beta: float) -> float:
    """Compute guided wavelength lambda_g = 2*pi/beta."""
    if beta <= EPSILON:
        raise ValueError("Guided wavelength undefined for beta <= 0.")
    return 2.0 * math.pi / beta


def is_propagating(
    frequency: float,
    a: float,
    b: float,
    m: int,
    n: int,
    c: float = C0,
) -> bool:
    """Return True if frequency is above cutoff."""
    fc = cutoff_frequency(a, b, m, n, c)
    return frequency > fc
