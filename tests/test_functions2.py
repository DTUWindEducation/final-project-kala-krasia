import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Add src folder to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.data_loader import extrapolate_wind_log, compute_power_time_series

def test_compute_power_time_series():
    wind_curve = np.array([0, 3, 5, 10, 15, 25])
    power_curve = np.array([0, 0, 500, 1500, 4000, 0])
    test_speeds = np.array([4, 7, 11, 14, 20, 24])

    result = compute_power_time_series(test_speeds, wind_curve, power_curve)
    assert result.shape == test_speeds.shape
    assert np.all(result >= 0)  # No negative power
    assert np.max(result) <= 4000

