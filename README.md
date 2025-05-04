[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zjSXGKeR)

# Wind Resource Assessment Package

**Team:** Ioanna Mouxtinou, [Insert other contributors]

---

## Overview

This project delivers a comprehensive Python package for assessing wind resources using ERA5 reanalysis data. Built as part of the DTU MSc course [46120 Scientific Programming for Wind Energy](https://kurser.dtu.dk/course/46120), the package supports every stage of wind resource assessment — from raw data processing to Annual Energy Production (AEP) estimation.

The analysis focuses on the Horns Rev 1 offshore wind farm, using ERA5 hourly wind data (10 m and 100 m heights) from 1997 to 2023. The system combines scientific methods (Weibull fitting, interpolation, shear modeling) with practical energy metrics (AEP via turbine power curves).

---

## Quick-start Guide

Follow the steps below to run the full analysis pipeline from scratch:

### 1. Clone the Repository
```bash
git clone https://github.com/your_username/final-project.git
cd final-project
```

### 2. Install Dependencies

Install all required Python packages:
```bash
pip install -r requirements.txt
```
*Minimum required packages:* `xarray`, `numpy`, `pandas`, `matplotlib`, `scipy`, `windrose`, `netCDF4`, `h5netcdf`

### 3. Run the Main Script
```bash
python examples/main.py
```
This runs the full pipeline: load ERA5 data, compute wind metrics, interpolate, fit Weibull distribution, plot results, and compute AEP.

### 4. View Results

Check the `outputs/` folder for:
- **`outputs.txt`** – Full wind speed and direction time series.
- **`summary.txt`** – Weibull shape/scale parameters and AEP estimate.
- **`wind_rose.png`** – Frequency of wind directions.
- **`wind_speed_distribution.png`** – Histogram + Weibull fit of wind speed.

### 5. Run Unit Tests (Optional)
```bash
pytest tests/
```
Tests ensure accuracy of extrapolation, Weibull fitting, AEP computation, and data loading.

---

## Architecture

The project is modular, structured into logical components:

```
final-project/
├── src/                        # Core implementation
│   ├── __init__.py
│   ├── data_loader.py          # Load & parse NetCDF files using xarray
│   ├── wind_analysis.py        # Wind speed/direction computation, power/log extrapolation
│   ├── interpolation.py        # Spatial bilinear interpolation
│   ├── statistics.py           # Weibull fitting using SciPy
│   ├── plotting.py             # Create wind rose and wind speed plots
│   ├── aep_calculator.py       # Compute AEP from wind & power curve
│
├── inputs/                     # Input data
│   ├── wind_data/
│   │   ├── 1997-1999.nc        # Hourly ERA5 wind components (u/v)
│   │   ├── 2000-2002.nc
│   │   └── ...
│   ├── turbine_data/
│       ├── NREL_5MW.csv        # Power curve (hub: 90 m)
│       └── NREL_15MW.csv       # Power curve (hub: 150 m)
│
├── examples/                   # Usage demos
│   ├── main.py                 # End-to-end example
│   ├── test_loader.py          # Example loader check
│   ├── test_analysis.py        # Example analysis test
│
├── outputs/                    # Generated visual and textual results
│   ├── outputs.txt
│   ├── summary.txt
│   ├── wind_rose.png
│   ├── wind_speed_distribution.png
│
├── tests/                      # Formal unit tests for validation
│   ├── test_aep.py
│   ├── test_weibull.py
│   └── ...
│
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── .gitignore
```

---

## Peer Review Criteria

### Code Structure
- Organized into logical, reusable modules.
- Easy to navigate and extend for other turbines or datasets.

### Required Functionality
- All 8 core features are implemented:
  - Wind speed & direction computation
  - Spatial interpolation
  - Height extrapolation (power law & log law)
  - Weibull fit
  - Plotting: wind rose & histogram
  - AEP estimation

### Extra Features
- Power output time series
- Logarithmic profile extrapolation

### Usability
- Simple to install and run with one command.
- Informative visual and textual outputs.

### Testing
- Unit tests provided for all major functions.
- Ensures reliable and reproducible outputs.

---

This package is fully aligned with wind industry workflows and serves as a solid foundation for site screening, pre-feasibility studies, or educational purposes.
