"""Tkinter GUI for the Waveguide Propagation Simulator."""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from fields import generate_grid, mode_field
from modes import cutoff_frequency, guided_beta, guided_wavelength, is_propagating
from plot import draw_field_contour_on_axes


class WaveguideSimulatorGUI:
    """Simple Tkinter GUI that reuses existing simulation modules."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Waveguide Propagation Simulator")
        self.root.geometry("1100x680")

        self.canvas = None
        self.figure = None

        self._build_layout()

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        controls = ttk.LabelFrame(container, text="Simulation Parameters", padding=10)
        controls.pack(side=tk.LEFT, fill=tk.Y)

        plot_frame = ttk.LabelFrame(container, text="Field Visualization", padding=8)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.plot_frame = plot_frame

        self.entries = {}
        self._add_entry(controls, "a [m]", "0.02286", 0)
        self._add_entry(controls, "b [m]", "0.01016", 1)
        self._add_entry(controls, "Frequency [Hz]", "1e10", 2)
        self._add_entry(controls, "m", "1", 3)
        self._add_entry(controls, "n", "0", 4)
        self._add_entry(controls, "Grid Nx", "140", 5)
        self._add_entry(controls, "Grid Ny", "100", 6)

        ttk.Label(controls, text="Mode Type").grid(row=7, column=0, sticky="w", pady=4)
        self.mode_var = tk.StringVar(value="TE")
        mode_box = ttk.Combobox(
            controls,
            textvariable=self.mode_var,
            values=("TE", "TM"),
            state="readonly",
            width=18,
        )
        mode_box.grid(row=7, column=1, sticky="ew", pady=4)

        self.info_var = tk.StringVar(value="Ready.")
        info_label = ttk.Label(
            controls, textvariable=self.info_var, justify=tk.LEFT, foreground="#1f4d8b"
        )
        info_label.grid(row=8, column=0, columnspan=2, sticky="w", pady=(10, 6))

        simulate_btn = ttk.Button(controls, text="Start", command=self.simulate)
        simulate_btn.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        controls.columnconfigure(1, weight=1)

    def _add_entry(self, parent: ttk.Widget, label: str, default: str, row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        entry = ttk.Entry(parent, width=20)
        entry.insert(0, default)
        entry.grid(row=row, column=1, sticky="ew", pady=4)
        self.entries[label] = entry

    def _parse_inputs(self):
        try:
            a = float(self.entries["a [m]"].get())
            b = float(self.entries["b [m]"].get())
            frequency = float(self.entries["Frequency [Hz]"].get())
            m = int(self.entries["m"].get())
            n = int(self.entries["n"].get())
            nx = int(self.entries["Grid Nx"].get())
            ny = int(self.entries["Grid Ny"].get())
            mode_type = self.mode_var.get().upper()
        except ValueError as exc:
            raise ValueError(
                "Invalid input: please insert numeric values for all fields."
            ) from exc

        if a <= 0 or b <= 0:
            raise ValueError("Waveguide dimensions must satisfy a > 0 and b > 0.")
        if frequency <= 0:
            raise ValueError("Frequency must be > 0.")
        if m < 0 or n < 0:
            raise ValueError("Mode indices must satisfy m >= 0 and n >= 0.")
        if m == 0 and n == 0:
            raise ValueError("Mode indices cannot both be zero.")
        if nx < 2 or ny < 2:
            raise ValueError("Grid resolution must satisfy Nx >= 2 and Ny >= 2.")
        if mode_type not in {"TE", "TM"}:
            raise ValueError("Mode type must be TE or TM.")

        return a, b, frequency, m, n, nx, ny, mode_type

    def simulate(self) -> None:
        try:
            a, b, frequency, m, n, nx, ny, mode_type = self._parse_inputs()
            fc = cutoff_frequency(a, b, m, n)

            if not is_propagating(frequency, a, b, m, n):
                messagebox.showwarning(
                    "Propagation Error",
                    (
                        "Mode cannot propagate\n\n"
                        f"f = {frequency:.3e} Hz\n"
                        f"fc = {fc:.3e} Hz\n"
                        "Set a frequency above cutoff."
                    ),
                )
                self.info_var.set("Mode cannot propagate for selected parameters.")
                return

            beta = guided_beta(frequency, a, b, m, n)
            lambda_g = guided_wavelength(beta)
            omega = 2.0 * math.pi * frequency
            _, _, x_grid, y_grid = generate_grid(a, b, nx=nx, ny=ny)
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

            self._render_plot(x_grid, y_grid, field, mode_type, m, n)
            self.info_var.set(
                f"fc={fc:.3e} Hz | beta={beta:.3e} rad/m | lambda_g={lambda_g:.3e} m"
            )
        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc))
            self.info_var.set("Input validation error.")
        except Exception as exc:  # Broad catch for numerical/backend issues.
            messagebox.showerror("Simulation Error", f"Unexpected error: {exc}")
            self.info_var.set("Simulation failed.")

    def _render_plot(
        self,
        x_grid,
        y_grid,
        field,
        mode_type: str,
        m: int,
        n: int,
    ) -> None:
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
            self.figure = None

        self.figure = Figure(figsize=(7.5, 4.6), dpi=100)
        ax = self.figure.add_subplot(111)
        contour = draw_field_contour_on_axes(
            ax=ax,
            x_grid=x_grid,
            y_grid=y_grid,
            field=field,
            mode_type=mode_type,
            m=m,
            n=n,
            title_suffix="z=0 m, t=0 s",
        )
        cbar = self.figure.colorbar(contour, ax=ax)
        cbar.set_label(f"{mode_type.upper()} field amplitude")
        self.figure.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def main() -> None:
    root = tk.Tk()
    app = WaveguideSimulatorGUI(root)
    _ = app
    root.mainloop()


if __name__ == "__main__":
    main()
