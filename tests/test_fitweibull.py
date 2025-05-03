# examples/test_plot_weibull_distribution.py
import sys
from pathlib import Path
import matplotlib.pyplot as plt
# Fix path so Python finds your src/ folder
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.data_loader import fit_weibull, plot_wind_speed_distribution
from src.data_loader import WindDataLoader
# Initialize and load wind data
loader = WindDataLoader("inputs")
loader.load_all()

def test_plot_weibull_distribution():
    input_dir = Path(__file__).resolve().parents[1] / "inputs"
    loader = WindDataLoader(input_dir)
    loader.load_all()

    # Horns Rev 1 approximate coordinates
    target_lat = 55 + 31/60 + 47/3600  # 55.5297
    target_lon = 7 + 54/60 + 22/3600   # 7.9061

    # Get interpolated wind speed at 100m height
    wind_speed = loader.interpolate_location(target_lat, target_lon, height=100, kind="speed")

    # Fit Weibull distribution
    shape, scale = fit_weibull(wind_speed)

    # Check that shape and scale are positive
    assert shape > 0
    assert scale > 0

    # Plot (optional, comment out to avoid GUI issues during batch test)
    # plot_wind_speed_distribution(wind_speed, shape, scale)

def test_plot_weibull_runs():
    loader = WindDataLoader("inputs")
    loader.load_all()
    wind_speed = loader.compute_wind_speed(10)
    shape, scale = fit_weibull(wind_speed)
    plot_wind_speed_distribution(wind_speed, shape, scale)  # Just check no error
