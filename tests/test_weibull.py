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
# examples/test_fit_weibull.py
u10 = loader.compute_wind_speed(10)

shape, scale = fit_weibull(u10)

print(f"Weibull parameters: Shape (k) = {shape:.2f}, Scale (A) = {scale:.2f}")
