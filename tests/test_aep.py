import sys
from pathlib import Path
import pandas as pd
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.data_loader import WindDataLoader, compute_aep, extrapolate_wind_speed
# Correct path 
loader = WindDataLoader("inputs")
dataset = loader.load_all()
def test_compute_aep():
    input_dir = Path(__file__).resolve().parents[1] / "inputs"
    loader = WindDataLoader(input_dir)
    loader.load_all()

    # Horns Rev 1 coordinates
    lat = 55 + 31/60 + 47/3600
    lon = 7 + 54/60 + 22/3600

    wind = loader.interpolate_location(lat, lon, height=10, kind="speed")
    wind_hub = extrapolate_wind_speed(wind, 10, 90)

    df = pd.read_csv(input_dir / "NREL_Reference_5MW_126.csv")
    power_curve_wind = df.iloc[:, 0].values
    power_curve_power = df.iloc[:, 1].values

    aep = compute_aep(wind_hub, power_curve_wind, power_curve_power)

    assert aep > 0
