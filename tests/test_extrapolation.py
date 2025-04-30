# test_power_law.py
from pathlib import Path
import sys
import numpy as np
# Add the project root (one level above this file) to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))
# import from src/
from src.data_loader import WindDataLoader
from src.data_loader import extrapolate_wind_speed
# Correct path 
loader = WindDataLoader("inputs")
dataset = loader.load_all()
# Example: Wind speeds at 10 meters
wind_speed_10m = np.array([5, 6, 7, 8, 9])  # m/s

# Reference height
z_ref = 10  # meters

# Target height (example: 90 meters, NREL 5MW hub height)
z_target = 90  # meters

# Assume typical offshore shear exponent
alpha = 0.14

# Extrapolate wind speeds
wind_speed_90m = extrapolate_wind_speed(wind_speed_10m, z_ref, z_target, alpha)

# Print results
print("Wind speeds at 10m:", wind_speed_10m)
print(f"Extrapolated wind speeds at {z_target}m:", wind_speed_90m)

# Plot for visualization
"""plt.figure()
plt.plot(wind_speed_10m, label="10m Wind Speeds")
plt.plot(wind_speed_90m, label=f"{z_target}m Extrapolated Speeds", linestyle='--')
plt.xlabel("Sample Points")
plt.ylabel("Wind Speed (m/s)")
plt.title("Wind Speed Extrapolation using Power Law")
plt.legend()
plt.grid(True)
plt.show()"""
