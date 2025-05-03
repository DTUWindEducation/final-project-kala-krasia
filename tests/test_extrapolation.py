# test_power_law.py
from pathlib import Path
import sys
import numpy as np
import pytest
# Add the project root (one level above this file) to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))
# import from src/
from src.data_loader import WindDataLoader
from src.data_loader import extrapolate_wind_speed
# Correct path 
loader = WindDataLoader("inputs")
dataset = loader.load_all()
def test_extrapolate_wind_speed_range():
    wind_speed_10m = np.array([5, 6, 7, 8, 9])
    result = extrapolate_wind_speed(wind_speed_10m, z_ref=10, z_target=90, alpha=0.14)
    assert result.shape == wind_speed_10m.shape
    assert np.all(result > wind_speed_10m)  # speeds should increase with height
import pytest
from src.data_loader import extrapolate_wind_speed

def test_extrapolate_invalid_height():
    with pytest.raises(ValueError):
        extrapolate_wind_speed(5, 0, 100)
