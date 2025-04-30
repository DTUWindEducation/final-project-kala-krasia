import sys
from windrose import WindroseAxes
from pathlib import Path
import matplotlib.pyplot as plt
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.data_loader import WindDataLoader, plot_wind_rose

# Load ERA5 dataset
loader = WindDataLoader("inputs")
loader.load_all()

# Horns Rev 1 location
target_lat = 55 + 31/60 + 47/3600
target_lon = 7 + 54/60 + 22/3600

# Get wind speed and direction at 100m
wind_speed = loader.interpolate_location(target_lat, target_lon, height=100, kind="speed")
wind_direction = loader.interpolate_location(target_lat, target_lon, height=100, kind="direction")

# Plot wind rose
plot_wind_rose(wind_speed, wind_direction)
