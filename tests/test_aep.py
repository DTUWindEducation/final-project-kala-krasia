# examples/test_aep.py

import sys
from pathlib import Path
import pandas as pd

# Add src/ to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.data_loader import WindDataLoader, compute_aep, extrapolate_wind_speed

# Load wind data
loader = WindDataLoader("inputs")
loader.load_all()

# Horns Rev 1 location
target_lat = 55 + 31/60 + 47/3600  # 55.5297
target_lon = 7 + 54/60 + 22/3600   # 7.9061

# Get wind speed at 10m, then extrapolate to 90m
wind_10m = loader.interpolate_location(target_lat, target_lon, 10, kind="speed")
wind_90m = extrapolate_wind_speed(wind_10m, 10, 90)

# Load power curve
turbine_file = "inputs/NREL_Reference_5MW_126.csv"
power_curve = pd.read_csv(turbine_file)

# Find correct column names
for col in power_curve.columns:
    if "wind" in col.lower():
        wind_col = col
    if "power" in col.lower():
        power_col = col

power_curve_wind = power_curve[wind_col].values
power_curve_power = power_curve[power_col].values

# Compute AEP
aep_mwh = compute_aep(wind_90m, power_curve_wind, power_curve_power)

print(f"AEP for NREL 5MW at 90m hub height = {aep_mwh:.2f} MWh/year")
