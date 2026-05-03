![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-00A86B?style=for-the-badge&logo=plotly&logoColor=white)
![RF Engineering](https://img.shields.io/badge/RF%20Engineering-8A2BE2?style=for-the-badge&logo=google-scholar&logoColor=white)

# Waveguide Propagation Simulator

Python project for simulating electromagnetic mode propagation (TE/TM) in a rectangular waveguide, with both static field plots and Matplotlib animations.

<img width="1101" height="710" alt="immagine" src="https://github.com/user-attachments/assets/2559c0b9-6662-430e-a8ce-c56d83216bd7" />

## Technical Description

The simulator computes waveguide modal parameters and field distributions on a 2D cross-section `(x, y)`, while supporting phase evolution through:

- propagation direction `z`
- time `t`

It is designed as a modular codebase:

- `modes.py`: mode physics, cutoff, propagation constants, validation
- `fields.py`: grid generation and electromagnetic scalar field generation
- `plot.py`: static `contourf` visualization (`viridis`)
- `animate.py`: animated propagation with `FuncAnimation`
- `main.py`: executable entry point and orchestration

## Textual Formulas Used

Cutoff frequency:

`fc = (c / 2) * sqrt((m / a)^2 + (n / b)^2)`

Guided wavenumber:

`beta = sqrt(k0^2 - (m*pi/a)^2 - (n*pi/b)^2)`

Free-space wavenumber:

`k0 = 2*pi*f/c`

Guided wavelength:

`lambda_g = 2*pi / beta`

Field model (scalar form used for visualization):

`Ez = cos(m*pi*x/a) * cos(n*pi*y/b) * cos(beta*z - omega*t)`

For TM visualization, the same scalar structure is used as `Hz`.

## Project Structure

```text
waveguide-propagation-simulator/
├── main.py
├── modes.py
├── fields.py
├── animate.py
├── plot.py
└── README.md
```

## Requirements

- Python 3.9+
- `numpy`
- `matplotlib`

Install dependencies:

```bash
pip install numpy matplotlib
```

## How To Run

Run the main simulation with GUI:

```bash
python gui.py
```
or without GUI:

```bash
python main.py
```

The default setup in `main.py`:

- defines waveguide dimensions `a, b`
- sets operating frequency and mode indices `(m, n)`
- checks propagation condition (`f > fc`)
- computes modal quantities (`fc`, `beta`, `lambda_g`)
- renders a static `contourf` field plot
- optionally starts animation

## Animation Generation

You can launch animation from `main.py` by setting:

`ENABLE_ANIMATION = True`

or run directly:

```bash
python animate.py
```

Configurable parameters include:

- number of frames
- frame interval/speed
- mode indices `(m, n)`
- frequency
- waveguide dimensions `(a, b)`
- sweep axis (`time` or `z`)

## Validation and Numerical Safety

Implemented checks:

- if `frequency < cutoff`, print: `Mode cannot propagate`
- mode indices constrained to `m >= 0` and `n >= 0`
- dimensions constrained to `a > 0` and `b > 0`
- numerical handling for `beta^2` near zero (floating-point tolerance)

## Example Output

Console output (example):

```text
Selected mode: TE(1,0)
Cutoff frequency fc = 6.557e+09 Hz
Operating frequency f = 1.000e+10 Hz
Guided wavenumber beta = 1.582e+02 rad/m
Guided wavelength lambda_g = 3.971e-02 m
```

## Screenshot Placeholder

Replace this section with project screenshots or animation captures:

- `docs/static_te10.png` (placeholder)
- `docs/animation_te10.gif` (placeholder)

## Future Extensions

- add full vector field components (`Ex, Ey, Hz` for TE and `Hx, Hy, Ez` for TM)
- support lossy conductors and dielectric-filled waveguides
- export animations to GIF/MP4 automatically
- add interactive parameter controls (sliders/widgets)
- include unit tests for physics validation
