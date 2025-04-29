import numpy as np

class WindAnalysis:
    """
    A class to perform basic wind data analysis:
    - Compute wind direction
    """

    def __init__(self, dataset):
        """
        Initialize with a loaded ERA5 dataset.

        Parameters
        ----------
        dataset : xarray.Dataset
            The dataset containing u and v wind components.
        """
        self.dataset = dataset

    def compute_wind_direction(self, height):
        """
        Compute wind direction at specified height (10 or 100 meters).

        Parameters
        ----------
        height : int
            Either 10 or 100.

        Returns
        -------
        np.ndarray
            Wind direction time series in degrees [0°, 360°].
        """
        if height not in [10, 100]:
            raise ValueError("Height must be either 10 or 100 meters.")

        u = self.dataset[f"u{height}"]
        v = self.dataset[f"v{height}"]

        # Calculate wind direction
        wind_dir_rad = np.arctan2(u, v)  # radians
        wind_dir_deg = np.degrees(wind_dir_rad)  # convert to degrees

        # Convert from [-180, 180] to [0, 360]
        wind_dir_deg = (wind_dir_deg + 360) % 360

        return wind_dir_deg.values
