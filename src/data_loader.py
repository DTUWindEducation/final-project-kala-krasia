from pathlib import Path
import xarray as xr
import numpy as np
from scipy.stats import weibull_min
import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes
class WindDataLoader:
    """
    A class to load and process ERA5 wind data from NetCDF4 files.
    """
    def __init__(self, directory):
        """
        Initialize the loader with a directory containing NetCDF4 files.

        Parameters:
        -----------
        directory : str or Path
            Path to folder containing ERA5 .nc files.
        """
        self.directory = Path(directory)
        self.dataset = None

    def load_all(self):
        
        """
        Load and concatenate all NetCDF files in the directory.
            Returns:
        --------
        xarray.Dataset
            Combined dataset with all years.
        """
        files = sorted(self.directory.glob("*.nc"))  # Uses pathlib globbing

        if not files:

            raise FileNotFoundError(f"No .nc files found in {self.directory.resolve()}")

        datasets = [xr.open_dataset(str(file.resolve()), engine="h5netcdf", decode_timedelta=True) for file in files]


        self.dataset = xr.concat(datasets, dim="time")
        return self.dataset
    
    def compute_wind_speed(self, height):

        """
        Compute wind speed time series at specified height (10 or 100 m).

        Parameters:
        -----------
        height : int
            Either 10 or 100.

        Returns:
        --------
        np.ndarray
            Wind speed time series.
        """
        if self.dataset is None:
            raise RuntimeError("No dataset loaded. Run `load_all()` first.")
        if height not in [10, 100]:
            raise ValueError("Height must be 10 or 100 meters.")
        u = self.dataset[f"u{height}"]
        v = self.dataset[f"v{height}"]
        wind_speed = np.sqrt(u**2 + v**2)
        return wind_speed.values

    def compute_wind_direction(self, height):
        """
    Compute wind direction time series at specified height (10 or 100 m).

    Parameters:
    -----------
    height : int
        Either 10 or 100.

    Returns:
    --------
    np.ndarray
        Wind direction time series in degrees (0°-360°).
    """
        if self.dataset is None:
            raise RuntimeError("No dataset loaded. Run `load_all()` first.")
        if height not in [10, 100]:
            raise ValueError("Height must be 10 or 100 meters.")
        u = self.dataset[f"u{height}"]
        v = self.dataset[f"v{height}"]

        direction = (np.degrees(np.arctan2(u, v)) + 360) % 360
        return direction.values
    
    def interpolate_location(self, target_lat, target_lon, height, kind="speed"):
        """
    Interpolate wind speed or direction time series at a given location inside the 4 corners.

    Parameters:
    -----------
    target_lat : float
        Latitude of the desired point (e.g., Horns Rev 1).
    target_lon : float
        Longitude of the desired point.
    height : int
        Height to use (10 or 100 meters).
    kind : str
        "speed" or "direction". Choose what to interpolate.

    Returns:
    --------
    np.ndarray
        Interpolated time series at the given location.
    """
        if kind not in ["speed", "direction"]:
            raise ValueError("kind must be speed or direction")
        if height not in [10, 100]:
            raise ValueError("Height must be 10 or 100 m")
        if self.dataset is None:
            raise RuntimeError("No dataset loaded. Run 'load_all()' first")
        
        #The coordinates of the 4 corners
        lat_min = 55.5
        lat_max = 55.75
        lon_min = 7.75
        lon_max = 8

        # Normalize the position inside the box
        x = (target_lon - lon_min) / (lon_max - lon_min)
        y = (target_lat - lat_min) / (lat_max - lat_min)
        
        
        # Load data depending on "kind"
        if kind == "speed":
            u = self.dataset[f"u{height}"]
            v = self.dataset[f"v{height}"]
            quantity = np.sqrt(u**2 + v**2)  # Wind speed
        elif kind == "direction":
            u = self.dataset[f"u{height}"]
            v = self.dataset[f"v{height}"]
            quantity = (np.arctan2(u, v) * (180/np.pi)) % 360  # Wind direction and convert to degrees

        # Find 4 corner points
        quantity_11 = quantity.sel(latitude=lat_max, longitude=lon_min, method="nearest")
        quantity_21 = quantity.sel(latitude=lat_max, longitude=lon_max, method="nearest")
        quantity_12 = quantity.sel(latitude=lat_min, longitude=lon_min, method="nearest")
        quantity_22 = quantity.sel(latitude=lat_min, longitude=lon_max, method="nearest")

        # Apply bilinear interpolation
        interpolated = (
            (1 - x) * (1 - y) * quantity_11 +
            x * (1 - y) * quantity_21 +
            (1 - x) * y * quantity_12 +
            x * y * quantity_22
        )

        return interpolated.values

# power_law.py

def extrapolate_wind_speed(u_ref, z_ref, z_target, alpha=0.14):
    """
    Extrapolate wind speed to a different height using the power law profile.

    Parameters:
    -----------
    u_ref : float or np.ndarray
        Wind speed at the reference height [m/s].
    z_ref : float
        Reference height [m].
    z_target : float
        Target height to extrapolate to [m].
    alpha : float
        Power law exponent (default is 0.14, typical for neutral conditions).

    Returns:
    --------
    float or np.ndarray
        Wind speed at the target height [m/s].
    """
    if z_ref <= 0 or z_target <= 0:
        raise ValueError("Heights must be positive numbers.")
    if alpha < 0:
        raise ValueError("Alpha should be non-negative.")

    u_target = u_ref * (z_target / z_ref) ** alpha
    return u_target

def fit_weibull(wind_speeds):
    wind_speeds_clean = wind_speeds.flatten()
    wind_speeds_clean = wind_speeds_clean[~np.isnan(wind_speeds_clean)]
    shape, loc, scale = weibull_min.fit(wind_speeds_clean, floc=0)
    return shape, scale

def plot_wind_speed_distribution(wind_speeds, shape, scale, bins=30):
    wind_speeds_clean = wind_speeds.flatten()
    wind_speeds_clean = wind_speeds_clean[~np.isnan(wind_speeds_clean)]
    plt.figure()
    plt.hist(wind_speeds_clean, bins=bins, density=True, alpha=0.6, label="Histogram")
    u = np.linspace(0, np.max(wind_speeds_clean), 100)
    pdf = weibull_min.pdf(u, shape, scale=scale)
    plt.plot(u, pdf, 'r-', label=f"Weibull Fit\nk={shape:.2f}, A={scale:.2f}")
    plt.xlabel("Wind Speed (m/s)")
    plt.ylabel("Probability Density")
    plt.title("Wind Speed Distribution with Weibull Fit")
    plt.legend()
    plt.grid(True)
    plt.show()
def plot_wind_rose(wind_speeds, wind_directions, num_sectors=16):
    ax = WindroseAxes.from_ax()
    ax.bar(wind_directions, wind_speeds, normed=True, opening=0.8, edgecolor='white', nsector=num_sectors)
    ax.set_legend()
    plt.title("Wind Rose Diagram")
    #plt.tight_layout()
    plt.show()
def compute_aep(wind_speeds, power_curve_wind, power_curve_power, availability=1.0):
    """
    Compute AEP from wind speed time series and a turbine power curve.

    Parameters:
        wind_speeds (np.ndarray): Wind speed time series [m/s].
        power_curve_wind (np.ndarray): Wind speeds from the power curve [m/s].
        power_curve_power (np.ndarray): Corresponding power outputs [kW].
        availability (float): Turbine availability factor (default = 1.0).

    Returns:
        float: Annual Energy Production in MWh.
    """
    wind_speeds_clean = wind_speeds.flatten()
    wind_speeds_clean = wind_speeds_clean[~np.isnan(wind_speeds_clean)]
    power_output = np.interp(wind_speeds_clean, power_curve_wind, power_curve_power)
    total_energy_kwh = np.sum(power_output) * availability
    return total_energy_kwh / 1000  # Convert to MWh
def extrapolate_wind_log(u_ref, z_ref, z_target, z0=0.03):
    """
    Extrapolate wind speed using the logarithmic profile.

    Parameters:
        u_ref (float or np.ndarray): Wind speed at reference height [m/s]
        z_ref (float): Reference height [m]
        z_target (float): Target height [m]
        z0 (float): Surface roughness length [m] (default = 0.03 for offshore)

    Returns:
        float or np.ndarray: Wind speed at z_target [m/s]
    """
    if z_ref <= z0 or z_target <= z0:
        raise ValueError("Heights must be greater than roughness length z0.")
    return u_ref * np.log(z_target / z0) / np.log(z_ref / z0)

# Extra Function 2: Compute time series power output from wind speeds
def compute_power_time_series(wind_speeds, power_curve_wind, power_curve_power):
    """
    Compute turbine power output time series from wind speeds using the power curve.

    Parameters:
        wind_speeds (np.ndarray): Wind speed time series [m/s].
        power_curve_wind (np.ndarray): Wind speed values in the power curve [m/s].
        power_curve_power (np.ndarray): Corresponding power outputs [kW].

    Returns:
        np.ndarray: Power output time series [kW].
    """
    wind_speeds_clean = wind_speeds.flatten()
    wind_speeds_clean = wind_speeds_clean[~np.isnan(wind_speeds_clean)]
    return np.interp(wind_speeds_clean, power_curve_wind, power_curve_power)
