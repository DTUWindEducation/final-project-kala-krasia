import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Add src folder to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.data_loader import extrapolate_wind_log, compute_power_time_series

def test_extrapolate_wind_log():
    u_10m = np.array([5, 6, 7])
    z_ref = 10
    z_target = 90
    result = extrapolate_wind_log(u_10m, z_ref, z_target, z0=0.03)
    assert result.shape == u_10m.shape
    assert np.all(result > u_10m)  # Should increase with height