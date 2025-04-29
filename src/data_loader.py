from pathlib import Path
import xarray as xr
import numpy as np
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
