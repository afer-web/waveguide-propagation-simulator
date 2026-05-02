"""Entry point for the Waveguide Propagation Simulator project."""

from __future__ import annotations

import math

from animate import animate_mode
from fields import generate_grid, mode_field
from modes import cutoff_frequency, guided_beta, guided_wavelength, is_propagating
from plot import plot_field_contour


def run_simulation(
    a: float,
    b: float,
    frequency: float,
    m: int,
    n: int,
    mode_type: str = "TE",
    run_animation: bool = False,
) -> None:
    """Run static analysis and optionally launch animation."""
    fc = cutoff_frequency(a, b, m, n)
    print(f"Selected mode: {mode_type.upper()}({m},{n})")
    print(f"Cutoff frequency fc = {fc:.3e} Hz")

    if not is_propagating(frequency, a, b, m, n):
        print("Mode cannot propagate")
        return

    beta = guided_beta(frequency, a, b, m, n)
    lambda_g = guided_wavelength(beta)
    omega = 2.0 * math.pi * frequency

    print(f"Operating frequency f = {frequency:.3e} Hz")
    print(f"Guided wavenumber beta = {beta:.3e} rad/m")
    print(f"Guided wavelength lambda_g = {lambda_g:.3e} m")

    _, _, x_grid, y_grid = generate_grid(a, b, nx=140, ny=100)
    field = mode_field(
        mode_type=mode_type,
        x_grid=x_grid,
        y_grid=y_grid,
        a=a,
        b=b,
        m=m,
        n=n,
        beta=beta,
        omega=omega,
        z=0.0,
        t=0.0,
    )
    plot_field_contour(
        x_grid=x_grid,
        y_grid=y_grid,
        field=field,
        mode_type=mode_type,
        m=m,
        n=n,
        title_suffix="z=0 m, t=0 s",
    )

    if run_animation:
        animate_mode(
            mode_type=mode_type,
            a=a,
            b=b,
            frequency=frequency,
            m=m,
            n=n,
            num_frames=150,
            interval_ms=35,
            sweep="time",
        )


if __name__ == "__main__":
    # Default WR-90-like rectangular waveguide dimensions.
    A = 0.02286  # [m]
    B = 0.01016  # [m]
    FREQ = 10e9  # [Hz]
    M = 1
    N = 0
    MODE = "TE"
    ENABLE_ANIMATION = True

    run_simulation(
        a=A,
        b=B,
        frequency=FREQ,
        m=M,
        n=N,
        mode_type=MODE,
        run_animation=ENABLE_ANIMATION,
    )
