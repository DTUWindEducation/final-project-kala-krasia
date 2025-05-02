from pathlib import Path
import sys
import numpy as np
# Add the project root (one level above this file) to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# import from src/
from src.data_loader import WindDataLoader

# Correct path 
loader = WindDataLoader("inputs")

dataset = loader.load_all()
def test_wind_speed_and_direction():
    input_dir = Path(__file__).resolve().parents[1] / "inputs"
    loader = WindDataLoader(input_dir)
    loader.load_all()

    for height in [10, 100]:
        speed = loader.compute_wind_speed(height)
        direction = loader.compute_wind_direction(height)

        assert speed is not None and len(speed) > 0
        assert direction is not None and len(direction) > 0
        assert np.all(speed > 0)
        assert np.all((direction >= 0) & (direction <= 360))