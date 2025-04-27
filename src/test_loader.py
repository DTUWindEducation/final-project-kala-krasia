from inputs.wind_data import WindDataLoader

# Load one of the NetCDF files (update path if needed)
filepath = 

# Create object
loader = WindDataLoader(filepath)

# Run method to compute wind speed at 100m
ws_100 = loader.compute_wind_speed(100)

print(f"Loaded wind speed time series of length: {len(ws_100)}")
print(f"First 5 values: {ws_100[:5]}")
