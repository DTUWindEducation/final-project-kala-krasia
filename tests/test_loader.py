from pathlib import Path
import sys

# Add the project root (one level above this file) to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# import from src/
from src.data_loader import WindDataLoader

# Correct path 
loader = WindDataLoader("inputs")

dataset = loader.load_all()

#Compute wind speed at 10 meters
wind_speed_10 = loader.compute_wind_speed(10)
print("First 5 wind speeds at 10m:", wind_speed_10[:5])

# Compute wind speed at 100 meters
wind_speed_100 = loader.compute_wind_speed(100)
print("First 5 wind speeds at 100m:", wind_speed_100[:5])

# Wind direction at 10m
wind_direction_10 = loader.compute_wind_direction(10)
print("First 5 wind directions at 10m:", wind_direction_10[:5])

# Wind direction at 100m
wind_direction_100 = loader.compute_wind_direction(100)
print("First 5 wind directions at 100m:", wind_direction_100[:5])