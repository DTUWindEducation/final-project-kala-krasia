[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zjSXGKeR)
# Our Great Package

Team: [ADD TEXT HERE!]

## Overview

[ADD TEXT HERE!]

## Quick-start guide

[ADD TEXT HERE!]

## Architecture

[ADD TEXT HERE!]

wind-resource-assessment/
├── src/
│   ├── __init__.py
│   ├── data_loader.py        # load and preprocess ERA5 NetCDF data
│   ├── wind_analysis.py      # wind speed, direction, interpolation, vertical extrapolation
│   ├── distribution.py       # Weibull fit and histogram
│   ├── plotting.py           # wind rose, distribution plots
│   └── aep.py                # AEP calculation using turbine power curves
│
├── inputs/                   # NetCDF + turbine power curve CSVs
│   └── ...
├── examples/                 # Scripts that demonstrate your functionality
│   └── ...
├── tests/                    # Tests (e.g., pytest)
│   └── ...
├── README.md
├── requirements.txt
└── .gitignore


## Peer review

[ADD TEXT HERE!]
