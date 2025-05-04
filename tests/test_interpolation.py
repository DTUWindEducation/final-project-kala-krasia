from pathlib import Path
import sys 
import numpy as np
import pytest
# Add the project root to the Python path to import from src
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.data_loader import WindDataLoader
loader = WindDataLoader("inputs")
loader.load_all()
lat = 55.53
lon = 7.91

def test_interpolation_within_box():

    
    for height in [10, 100]:
        speed = loader.interpolate_location(lat, lon, height, kind="speed")
        direction = loader.interpolate_location(lat, lon, height, kind="direction")

        assert speed is not None and len(speed) > 0
        assert direction is not None and len(direction) > 0
        assert np.all(speed > 0)
        assert np.all((direction >= 0) & (direction <= 360))

def test_interpolate_location_invalid_kind():
    loader = WindDataLoader("inputs")
    loader.load_all()
    with pytest.raises(ValueError):
        loader.interpolate_location(55.53, 7.91, 10, kind="unknown")