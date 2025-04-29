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

