import xarray as xr
import numpy as np
def calculate_climatology_for_period(file_list, variable, start_date, end_date, preprocess=None):
    """
    Calculate climatology for a preselected period from a list of files.

    Parameters:
    - file_list: List of file paths to open.
    - variable: Variable name to select from the dataset.
    - start_date: Start date for the period (e.g., "1990-01-01").
    - end_date: End date for the period (e.g., "1990-12-31").
    - preprocess: Optional preprocess function for xarray.open_mfdataset.

    Returns:
    - Climatology (e.g., mean) for the selected period.
    """
    def _select_time(ds):
        """Preprocess function to select the desired time period."""
        ds= ds.sel(time=slice(start_date, end_date))
        if variable in ["r01mm","r10mm","r20mm","cdd","avg_lds_wt1","max_lds_wt1","nd_thre_cold_tn0","nd_thre_cold_tn20","nd_thre_hot_tx30","nd_thre_rain50","nd_thre_rain100","nhw_tx40_dur6","nhw_tx40_dur3"]:
            ds[variable].values = ds[variable].values.astype('timedelta64[D]')
            ds[variable] = ds[variable] / np.timedelta64(1, 'D')
        return ds

    # Use the provided preprocess function or the default time selection
    if preprocess is None:

        preprocess = _select_time

    # Open the dataset
    ds = xr.open_mfdataset(file_list, preprocess=preprocess,concat_dim='time', combine='nested')

    # Calculate climatology (e.g., mean)
    climatology = ds[variable].mean(dim="time")

    if "units" not in ds[variable].attrs:
        units="days"
    else:
        units=ds[variable].attrs["units"]
    return climatology, units