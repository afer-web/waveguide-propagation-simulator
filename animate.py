"""Matplotlib animation for waveguide mode propagation."""

from __future__ import annotations

import math

import matplotlib.animation as animation
import matplotlib.pyplot as plt

from fields import generate_grid, mode_field
from modes import C0, cutoff_frequency, guided_beta, is_propagating


def animate_mode(
    mode_type: str,
    a: float,
    b: float,
    frequency: float,
    m: int,
    n: int,
    num_frames: int = 120,
    interval_ms: int = 40,
    sweep: str = "time",
    z_span: float = 0.2,
    t_span: float = 1e-9,
    nx: int = 120,
    ny: int = 90,
) -> animation.FuncAnimation:
    """
    Animate field evolution either in time or along z.

    sweep='time'  -> vary t, keep z fixed at 0
    sweep='z'     -> vary z, keep t fixed at 0
    """
    fc = cutoff_frequency(a, b, m, n)
    if not is_propagating(frequency, a, b, m, n):
        raise ValueError(
            f"Mode cannot propagate: frequency={frequency:.3e} Hz < cutoff={fc:.3e} Hz"
        )

    beta = guided_beta(frequency, a, b, m, n)
    omega = 2.0 * math.pi * frequency
    _, _, x_grid, y_grid = generate_grid(a, b, nx=nx, ny=ny)

    fig, ax = plt.subplots(figsize=(8, 4))
    initial_field = mode_field(
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

    image = ax.imshow(
        initial_field,
        extent=[0.0, a, 0.0, b],
        origin="lower",
        cmap="viridis",
        aspect="auto",
        animated=True,
    )
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label(f"{mode_type.upper()} field amplitude")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    title = ax.set_title("")

    def _update(frame: int):
        if sweep.lower() == "time":
            t = frame * (t_span / max(num_frames - 1, 1))
            z = 0.0
            dynamic_label = f"t={t:.2e} s"
        elif sweep.lower() == "z":
            z = frame * (z_span / max(num_frames - 1, 1))
            t = 0.0
            dynamic_label = f"z={z:.3e} m"
        else:
            raise ValueError("sweep must be either 'time' or 'z'.")

        frame_field = mode_field(
            mode_type=mode_type,
            x_grid=x_grid,
            y_grid=y_grid,
            a=a,
            b=b,
            m=m,
            n=n,
            beta=beta,
            omega=omega,
            z=z,
            t=t,
        )
        image.set_data(frame_field)
        title.set_text(
            f"{mode_type.upper()}({m},{n}) | f={frequency:.3e} Hz | {dynamic_label}"
        )
        return image, title

    ani = animation.FuncAnimation(
        fig,
        _update,
        frames=num_frames,
        interval=interval_ms,
        blit=False,
        repeat=True,
    )
    plt.tight_layout()
    plt.show()
    return ani


if __name__ == "__main__":
    animate_mode(
        mode_type="TE",
        a=0.02286,
        b=0.01016,
        frequency=10e9,
        m=1,
        n=0,
        num_frames=140,
        interval_ms=35,
        sweep="time",
    )
