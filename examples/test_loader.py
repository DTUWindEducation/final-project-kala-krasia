
from pathlib import Path
import xarray as xr
import numpy as np 
from src.data_loader import WindDataLoader

# Correct path (3 folders deep)
loader = WindDataLoader("inputs/wind_resource_assessment/inputs/")

dataset = loader.load_all()

wind_speed_100 = loader.compute_wind_speed(100)

print(wind_speed_100[:5])
