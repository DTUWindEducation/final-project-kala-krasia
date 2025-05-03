import sys
from windrose import WindroseAxes
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.data_loader import WindDataLoader, plot_wind_rose

# Load ERA5 dataset
loader = WindDataLoader("inputs")
loader.load_all()

def test_plot_wind_rose():
    input_dir = Path(__file__).resolve().parents[1] / "inputs"
    loader = WindDataLoader(input_dir)
    loader.load_all()

    target_lat = 55 + 31/60 + 47/3600
    target_lon = 7 + 54/60 + 22/3600

    wind_speed = loader.interpolate_location(target_lat, target_lon, height=100, kind="speed")
    wind_direction = loader.interpolate_location(target_lat, target_lon, height=100, kind="direction")

    assert wind_speed is not None and wind_direction is not None
    assert len(wind_speed) == len(wind_direction)
    assert np.all(wind_speed >= 0)
    assert np.all((wind_direction >= 0) & (wind_direction <= 360))
