[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zjSXGKeR)

# Wind Resource Assessment Package

**Team:** Kala Krasia  
**Authors:** Paraskevi Simiti, Ioanna Fouskari  
**Course:** [46120 Scientific Programming for Wind Energy – DTU](https://kurser.dtu.dk/course/46120)

## Overview

This Python package performs a complete wind resource assessment workflow using ERA5 reanalysis data. It includes everything from raw wind data processing to energy estimation and visualization.

The analysis focuses on **Horns Rev 1**, using ERA5 hourly wind component data (u and v) at 10 m and 100 m heights from **1997 to 2008**. The pipeline includes:

- Wind speed & direction computation  
- Spatial bilinear interpolation  
- Height extrapolation (Power law & Log law)  
- Weibull fitting  
- Wind rose and distribution plotting  
- AEP estimation using power curves  


## Quick-start Guide

Follow the steps below to run the full analysis pipeline from scratch:

### 1. Clone the Repository
```bash
git clone https://github.com/DTUWindEducation/final-project-kala-krasia.git
cd final-project-kala-krasia
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

Check the `outputs/` directory for:
- **`outputs.txt`** – Full wind speed and direction time series.
- **`summary.txt`** – Weibull shape/scale parameters and AEP estimate.
- **`wind_rose.png`** – Frequency of wind directions.
- **`wind_speed_distribution.png`** – Wind speed histogram with overlaid Weibull fit.

### 5. Run Unit Tests (Optional)
```bash
pytest tests/
```
Tests ensure accuracy of extrapolation, Weibull fitting, AEP computation, and data loading.

---

## Architecture

The project is modular, structured into logical components:

```
final-project-kala-krasia/
├── src/                        # Core logic and utilities
│   └── data_loader.py          # All main functions:
│                               # - Load NetCDF files
│                               # - Wind speed/direction
│                               # - Interpolation & extrapolation
│                               # - Weibull fit & plotting
│                               # - AEP calculation
│
├── examples/                   # Execution scripts
│   └── main.py                 # End-to-end pipeline
│
├── inputs/                     # Input data
│   ├── 1997-1999.nc            # ERA5 reanalysis (u/v at 10m and 100m)
│   ├── 2000-2002.nc
│   ├── 2003-2005.nc
│   ├── 2006-2008.nc
│   ├── NREL_Reference_5MW_126.csv   # Power curve (hub height: 90 m)
│   └── NREL_Reference_15MW_240.csv  # Power curve (hub height: 150 m)
│
├── outputs/                     # Automatically generated results
│   ├── outputs.txt
│   ├── summary.txt
│   ├── wind_rose.png
│   └── wind_speed_distribution.png
│
├── tests/                       # Unit tests
│   ├── test_aep.py
│   ├── test_extrapolation.py
│   ├── test_fitweibull.py
│   ├── test_functions1.py
│   ├── test_functions2.py
│   ├── test_interpolation.py
│   ├── test_loader.py
│   ├── test_weibull.py
│   └── test_windrose.py
│
├── pyproject.toml               # Project metadata and dependencies
├── requirements.txt             # Dependency list
├── LICENSE                     
├── .gitignore
└── README.md                    # This file 
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
