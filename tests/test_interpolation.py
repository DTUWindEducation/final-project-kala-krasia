from pathlib import Path
import sys 

# Add the project root to the Python path to import from src
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.data_loader import WindDataLoader

# Set Horns Rev 1 coordinates (within the 4-point grid)
lat = 55.53
lon = 7.91

# Load the dataset
loader = WindDataLoader("inputs")
loader.load_all()

# Interpolate wind speed and direction at 10 m and 100 m
for height in [10, 100]:
    speed = loader.interpolate_location(lat, lon, height, kind="speed")
    direction = loader.interpolate_location(lat, lon, height, kind="direction")

    print(f"\n Interpolated wind speed at {height}m (first 5):\n{speed[:5]}")
    print(f" Interpolated wind direction at {height}m (first 5):\n{direction[:5]}")