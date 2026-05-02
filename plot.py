"""Static plotting utilities for waveguide fields."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


def draw_field_contour_on_axes(
    ax,
    x_grid: np.ndarray,
    y_grid: np.ndarray,
    field: np.ndarray,
    mode_type: str,
    m: int,
    n: int,
    title_suffix: str = "",
    levels: int = 60,
):
    """Draw a contourf field map on an existing matplotlib Axes."""
    contour = ax.contourf(x_grid, y_grid, field, levels=levels, cmap="viridis")
    mode_label = f"{mode_type.upper()}({m},{n})"
    suffix = f" - {title_suffix}" if title_suffix else ""
    ax.set_title(f"Rectangular Waveguide Mode {mode_label}{suffix}")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_aspect("equal")
    return contour


def plot_field_contour(
    x_grid: np.ndarray,
    y_grid: np.ndarray,
    field: np.ndarray,
    mode_type: str,
    m: int,
    n: int,
    title_suffix: str = "",
    levels: int = 60,
) -> None:
    """Create a 2D contourf plot with viridis colormap."""
    fig, ax = plt.subplots(figsize=(8, 4))
    contour = draw_field_contour_on_axes(
        ax=ax,
        x_grid=x_grid,
        y_grid=y_grid,
        field=field,
        mode_type=mode_type,
        m=m,
        n=n,
        title_suffix=title_suffix,
        levels=levels,
    )
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label(f"{mode_type.upper()} field amplitude")
    fig.tight_layout()
    plt.show()
