import numpy as np
import sys
from pathlib import Path
# Add the project root (one level above this file) to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))
# import from src/
from src.data_loader import WindDataLoader
from src.data_loader import fit_weibull
# Correct path 
loader = WindDataLoader("inputs")
dataset = loader.load_all()
def test_fit_weibull():
    input_dir = Path(__file__).resolve().parents[1] / "inputs"
    loader = WindDataLoader(input_dir)
    loader.load_all()

    u10 = loader.compute_wind_speed(10)
    shape, scale = fit_weibull(u10)

    assert shape > 0
    assert scale > 0
    assert isinstance(shape, float)
    assert isinstance(scale, float)
