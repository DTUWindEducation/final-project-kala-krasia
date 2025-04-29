import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.data_loader import WindDataLoader
from src.wind_analysis import WindAnalysis

# Load data
loader = WindDataLoader("inputs/wind_resource_assessment/inputs/")
dataset = loader.load_all()

# Create WindAnalysis object
analysis = WindAnalysis(dataset)

# Compute wind direction at 100 meters
wind_dir_100 = analysis.compute_wind_direction(100)

print(f"First 5 wind direction values at 100m: {wind_dir_100[:5]}")
