[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zjSXGKeR)
# Our Great Package

Team: [ADD TEXT HERE!]

## Overview

[ADD TEXT HERE!]

## Quick-start guide

[ADD TEXT HERE!]

## Architecture

[ADD TEXT HERE!]

final-project/
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Load NetCDF4 files
│   ├── wind_analysis.py        # Wind speed, wind direction, extrapolation
│   ├── interpolation.py        # Spatial interpolation (for Horns Rev 1)
│   ├── statistics.py           # Weibull fitting
│   ├── plotting.py             # Plots (histogram, wind rose)
│   ├── aep_calculator.py       # AEP calculation
│
├── inputs/
│   ├── wind_data/              # Your NetCDF wind data here
│   │   ├── 1997-1999.nc
│   │   ├── 2000-2002.nc
│   │   └── etc.
│   ├── turbine_data/           # Your turbine CSV power curves
│       ├── NREL_5MW.csv
│       └── NREL_15MW.csv
│
├── examples/                   # Test scripts for your functions
│   ├── test_loader.py
│   ├── test_analysis.py
│   └── etc.
│
├── outputs/                    # Your generated plots
│
├── tests/                      # Formal unit tests
│
├── README.md
├── requirements.txt
└── .gitignore
ΜΗΝ ΞΕΧΑΣΟΥΜΕ PIP INSTALL XARRAY, NUMPY, netCDF4


## Peer review

[ADD TEXT HERE!]
