from pathlib import Path
import sys
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

# Add the project root to the system path BEFORE imports
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.data_loader import (
    WindDataLoader,
    extrapolate_wind_speed,
    fit_weibull,
    plot_wind_speed_distribution,
    plot_wind_rose,
    compute_aep
)

#Create output directory

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

#Initialize the loader
loader = WindDataLoader("inputs")
loader.load_all()

# Compute data
speed_10 = loader.compute_wind_speed(10)
speed_100 = loader.compute_wind_speed(100)
dir_10 = loader.compute_wind_direction(10)
dir_100 = loader.compute_wind_direction(100)

#Save calculated values to outputs

with open(output_dir/"outputs.txt", "w") as f:    
    f.write("WindSpeed_10m\tWindSpeed_100m\tWindDir_10m\tWindDir_100m\n")
    for ws10, ws100, wd10, wd100 in zip(
        speed_10.flatten(),
        speed_100.flatten(),
        dir_10.flatten(),
        dir_100.flatten(),
    ):
        f.write(f"{ws10:.2f}\t{ws100:.2f}\t{wd10:.2f}\t{wd100:.2f}\n")

print("Full time series saved to outputs/outputs.txt")


# Interpolate to Horns Rev 1 location
lat_hr1, lon_hr1 = 55.5297, 7.9061
interp_speed_100 = loader.interpolate_location(lat_hr1, lon_hr1, 100, kind="speed")
interp_dir_100 = loader.interpolate_location(lat_hr1, lon_hr1, 100, kind="direction")
print("Interpolation at Horns Rev 1")

# Extrapolate to 90m using power law
speed_90 = extrapolate_wind_speed(speed_100, 100, 90, alpha=0.14)
print("Extrapolated wind speed to 90m using power law")

# Fit Weibull distribution to 100m speed
turbine_speed = interp_speed_100
shape, scale = fit_weibull(turbine_speed)
print(f"Weibull fit done: shape = {shape:.2f}, scale = {scale:.2f}")

# Save wind speed distribution (histogram + Weibull fit)
fig1 = plot_wind_speed_distribution(turbine_speed, shape, scale)
fig1.savefig(output_dir / "wind_speed_distribution.png")
print("Saved wind_speed_distribution.png to outputs/")

# Save wind rose plot
directions = interp_dir_100
fig2 = plot_wind_rose(turbine_speed, directions)
fig2.savefig(output_dir / "wind_rose.png")
print("Saved wind_rose.png to /outputs")

# Load turbine power curve from CSV
curve_df = pd.read_csv("inputs/NREL_Reference_5MW_126.csv")
curve_wind = curve_df.iloc[:, 0].values
curve_power = curve_df.iloc[:, 1].values
print("Power curve loaded from CSV")

# Compute AEP
AEP_MWh = compute_aep(turbine_speed, curve_wind, curve_power)
print(f"Estimated AEP: {AEP_MWh:.2f} MWh/year")


# Save results to text file
with open(output_dir / "summary.txt", "w") as f:
    f.write("Wind Resource Assessment Summary\n")
    f.write("=" * 40 + "\n")
    f.write(f"Weibull shape (k): {shape:.2f}\n")
    f.write(f"Weibull scale (A): {scale:.2f}\n")
    f.write(f"Estimated AEP: {AEP_MWh:.2f} MWh/year\n")
print("Summary written to outputs/summary.txt")

print("\nAll calculations and visualizations completed successfully.")
sys.stdout.flush()
plt.show()