# examples/test_plot_weibull_distribution.py
import sys
from pathlib import Path
import matplotlib.pyplot as plt
# Fix path so Python finds your src/ folder
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.data_loader import fit_weibull, plot_wind_speed_distribution
from src.data_loader import WindDataLoader
# Initialize and load wind data
loader = WindDataLoader("inputs")
loader.load_all()

# Horns Rev 1 approximate coordinates
target_lat = 55 + 31/60 + 47/3600  # 55.5297
target_lon = 7 + 54/60 + 22/3600   # 7.9061

# Get interpolated wind speed at 100m height
wind_speed = loader.interpolate_location(target_lat, target_lon, height=100, kind="speed")

# Fit Weibull distribution
shape, scale = fit_weibull(wind_speed)

# Plot histogram vs fitted Weibull
plot_wind_speed_distribution(wind_speed, shape, scale)

