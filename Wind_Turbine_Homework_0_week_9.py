import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 1. Load power curve data from the CSV
csv_path = "LEANWIND_Reference_8MW_164.csv"  # Make sure this file is in your working directory
df = pd.read_csv(csv_path)

# Extract wind speed and power columns
power_curve_data = df[["Wind Speed [m/s]", "Power [kW]"]].to_numpy()


# 2. Define the classes

class GeneralWindTurbine:
    def __init__(self, rotor_diameter, hub_height, rated_power, v_in, v_rated, v_out, name=None):
        self.rotor_diameter = rotor_diameter  # in meters
        self.hub_height = hub_height          # in meters
        self.rated_power = rated_power        # in kW
        self.v_in = v_in                      # cut-in wind speed in m/s
        self.v_rated = v_rated                # rated wind speed in m/s
        self.v_out = v_out                    # cut-out wind speed in m/s
        self.name = name                      # optional name

    def get_power(self, v):
        if v < self.v_in or v > self.v_out:
            return 0
        elif self.v_in <= v < self.v_rated:
            return self.rated_power * (v / self.v_rated) ** 3
        else:    #self.v_rated <= v <= self.v_out 
            return self.rated_power
        
class WindTurbine(GeneralWindTurbine):
    def __init__(self, rotor_diameter, hub_height, rated_power, v_in, v_rated, v_out, power_curve_data, name=None):
        super().__init__(rotor_diameter, hub_height, rated_power, v_in, v_rated, v_out, name)
        self.power_curve_data = power_curve_data  # numpy array of shape (n, 2)
    
    def get_power(self, v):
        #Interpolate using the power curve
        wind_speeds = self.power_curve_data[:, 0]
        power_values = self.power_curve_data[:, 1]
        
        if v < wind_speeds[0] or v > wind_speeds[-1]:
            return 0
        else: 
            return float(np.interp(v, wind_speeds, power_values))
        
# 3. LEANWIND 8MW 164

rotor_diameter = 164       # meters
hub_height = 110           # meters
rated_power = 8000         # kW
v_in = 4.0                 # cut-in wind speed [m/s]
v_rated = 12.5             # rated wind speed [m/s]
v_out = 25.0               # cut-out wind speed [m/s]

# 4. Create objects from both classes
general_turbine = GeneralWindTurbine(
    rotor_diameter, hub_height, rated_power,
    v_in, v_rated, v_out, name="LEANWIND_8MW_General"
)

wind_turbine = WindTurbine(
    rotor_diameter, hub_height, rated_power,
    v_in, v_rated, v_out,
    power_curve_data, name="LEANWIND_8MW_Interpolated"
)

# Step 4: Generate power curves
wind_speeds = np.linspace(0, 30, 300)
general_power = [general_turbine.get_power(v) for v in wind_speeds]
interpolated_power = [wind_turbine.get_power(v) for v in wind_speeds]

# Step 5: Plot comparison
plt.figure(figsize=(10, 6))
plt.plot(wind_speeds, general_power, label='GeneralWindTurbine (Analytical)', linestyle='--')
plt.plot(wind_speeds, interpolated_power, label='WindTurbine (Interpolated)', linestyle='-')
plt.xlabel('Wind Speed [m/s]')
plt.ylabel('Power Output [kW]')
plt.title('Comparison of Power Curves: LEANWIND 8MW Turbine')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()